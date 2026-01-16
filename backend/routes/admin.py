from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    current_app,
    make_response,
)
from sqlalchemy import text, desc
from backend import db
from backend.models.project import Project, ProjectImage, ProjectTranslation
from backend.models.project_url import ProjectURL
from backend.models.experience import Experience, ExperienceTranslation
from backend.models.education import Education, EducationTranslation, Course
from backend.models.skill import Skill, SkillTranslation, SkillCategory, SkillCategoryTranslation
from backend.models.profile import Profile, ProfileTranslation
from backend.models.certification import Certification, CertificationTranslation
from backend.models.tag import Tag
from backend.services.cloudinary_service import cloudinary_service
from backend.services.cache_service import invalidate_entities_cache
from backend.services.github_service import GitHubService
from backend.services.ai_service import AIProjectGenerator
import json
import os
import cloudinary.api
from auth.decorators import requires_login, requires_role

admin_bp = Blueprint("admin", __name__, template_folder="../../templates")


@admin_bp.route("/admin")
@requires_login
@requires_role("admin")
def admin_home():
    from sqlalchemy.orm import joinedload
    
    ready = request.args.get("ready")
    
    if ready == "true":
        try:
            # Force reconnection check
            db.session.execute(text("SELECT 1"))
            db.session.commit()

            # Fetch all data with eager loading to prevent N+1 queries
            projects_data = Project.query.options(
                joinedload(Project.translations),
                joinedload(Project.images),
                joinedload(Project.urls),
                joinedload(Project.tags)
            ).order_by(desc(Project.created_at)).all()
            
            experiences_data = Experience.query.options(
                joinedload(Experience.translations),
                joinedload(Experience.tags)
            ).order_by(desc(Experience.start_date)).all()
            
            education_data = Education.query.options(
                joinedload(Education.translations),
                joinedload(Education.courses)
            ).order_by(desc(Education.start_date)).all()
            
            skills_data = Skill.query.options(
                joinedload(Skill.translations)
            ).order_by(Skill.order).all()
            
            certifications_data = Certification.query.options(
                joinedload(Certification.translations)
            ).order_by(desc(Certification.issue_date)).all()
            
            skill_categories_data = SkillCategory.query.options(
                joinedload(SkillCategory.translations)
            ).order_by(SkillCategory.order).all()
            
            profile_data = Profile.query.options(
                joinedload(Profile.translations)
            ).first()

            # Helper to serialize objects
            def serialize(obj):
                if not obj: return None
                d = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
                # Handle dates
                for k, v in d.items():
                    if hasattr(v, 'isoformat'):
                        d[k] = v.isoformat()
                
                # Handle relationships
                if hasattr(obj, 'translations'):
                    d['translations'] = [{c.name: getattr(t, c.name) for c in t.__table__.columns} for t in obj.translations]
                
                if hasattr(obj, 'tags'):
                    d['tags'] = [{'id': t.id, 'name': t.name, 'slug': t.slug} for t in obj.tags]
                    
                if hasattr(obj, 'images'):
                    d['images'] = [{c.name: getattr(i, c.name) for c in i.__table__.columns} for i in obj.images]
                    
                if hasattr(obj, 'courses'):
                    d['courses'] = [c.name for c in sorted(obj.courses, key=lambda x: x.order)]

                if hasattr(obj, 'urls'):
                    d['urls'] = [{c.name: getattr(u, c.name) for c in u.__table__.columns} for u in sorted(obj.urls, key=lambda x: x.order)]
                    
                return d

            projects = [serialize(p) for p in projects_data]
            experiences = [serialize(e) for e in experiences_data]
            education = [serialize(e) for e in education_data]
            skills = [serialize(s) for s in skills_data]
            skill_categories = [serialize(sc) for sc in skill_categories_data]
            certifications = [serialize(c) for c in certifications_data]
            profile = serialize(profile_data) if profile_data else {}

            return render_template(
                "admin.html",
                projects=projects,
                experiences=experiences,
                education=education,
                skills=skills,
                skill_categories=skill_categories,
                certifications=certifications,
                profile=profile
            )

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            current_app.logger.error(f"Error loading admin data: {e}\n{error_details}")
            db.session.rollback()
            return render_template(
                "error.html", 
                error=f"Error loading data: {str(e)}",
                details=error_details
            )

    elif ready == "false":
        return render_template(
            "error.html", error="Database connection check failed."
        )

    return render_template("admin_base.html")


@admin_bp.route("/admin/check")
@requires_login
@requires_role("admin")
def admin_check():
    """Check database connectivity with retries."""
    retries = 3
    for attempt in range(retries):
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({"ready": True})
        except Exception as e:
            current_app.logger.warning(
                f"DB check failed (attempt {attempt + 1}/{retries}): {e}"
            )
            db.session.rollback()
            if attempt < retries - 1:
                import time
                time.sleep(1)
    return jsonify({"ready": False})


# ==========================================
# SAVE ENDPOINTS
# ==========================================

@admin_bp.route("/admin/save/project", methods=["POST"])
@requires_login
@requires_role("admin")
def save_project():
    # Retry logic for database connection issues (e.g., sleeping database)
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            # Test database connection before proceeding
            db.session.execute(text("SELECT 1"))
            db.session.commit()
            break  # Connection successful, proceed
        except Exception as e:
            current_app.logger.warning(
                f"Database connection attempt {attempt + 1}/{max_retries} failed: {e}"
            )
            db.session.rollback()
            if attempt < max_retries - 1:
                import time
                time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
            else:
                return jsonify({
                    "error": "Database connection failed after multiple retries. Please try again."
                }), 503
    
    try:
        data = request.json
        project_id = data.get("id")
        
        # Validation
        title_es = data.get("title_es")
        title_en = data.get("title_en")
        
        if not title_es and not title_en:
            return jsonify({"error": "Title (ES or EN) is required"}), 400
            
        # Auto-generate slug if missing
        slug = data.get("slug")
        if not slug:
            import re
            import unicodedata
            def slugify(value):
                value = str(value)
                value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
                value = re.sub(r'[^\w\s-]', '', value).lower()
                return re.sub(r'[-\s]+', '-', value).strip('-')
                
            base_slug = slugify(title_en or title_es)
            slug = base_slug
            # Ensure uniqueness
            counter = 1
            while Project.query.filter_by(slug=slug).first():
                if project_id: # If editing, check if it's the same project
                    existing = Project.query.filter_by(slug=slug).first()
                    if existing.id == project_id:
                        break
                slug = f"{base_slug}-{counter}"
                counter += 1
        
        if project_id:
            project = Project.query.get_or_404(project_id)
        else:
            project = Project()
            db.session.add(project)
        
        # Validate category
        category = data.get("category")
        if category and category not in ["project", "work", "study"]:
            return jsonify({"error": "Invalid category. Must be: project, work, or study"}), 400
        
        project.slug = slug
        project.category = category
        project.is_featured_cv = data.get("is_featured_cv", False)
        
        # Handle URLs - NEW: Use ProjectURL model
        # Delete existing URLs if updating
        if project_id:
            ProjectURL.query.filter_by(project_id=project.id).delete()
            db.session.flush()
        
        # Process URL data - support multiple formats for backward compatibility
        url_data = data.get("url") or data.get("urls", [])
        
        if url_data:
            # If it's a string (old format), try to parse it
            if isinstance(url_data, str):
                import json
                try:
                    # Try parsing as JSON
                    if url_data.startswith('{'):
                        parsed = json.loads(url_data)
                        # Convert old JSON format to new ProjectURL entries
                        for url_type, url_value in parsed.items():
                            if url_value:
                                project_url = ProjectURL(
                                    url_type=url_type,  # e.g., 'github', 'live'
                                    url=url_value,
                                    order=0 if url_type == 'github' else 1
                                )
                                project.urls.append(project_url)
                    else:
                        # Plain string URL - assume it's a live URL
                        project_url = ProjectURL(
                            url_type='live',
                            url=url_data,
                            order=0
                        )
                        project.urls.append(project_url)
                except json.JSONDecodeError:
                    # Not JSON, treat as plain URL
                    project_url = ProjectURL(
                        url_type='live',
                        url=url_data,
                        order=0
                    )
                    project.urls.append(project_url)
            
            # If it's a list (new format)
            elif isinstance(url_data, list):
                for idx, url_item in enumerate(url_data):
                    if isinstance(url_item, dict):
                        project_url = ProjectURL(
                            url_type=url_item.get('type', 'live'),
                            url=url_item.get('url'),
                            label=url_item.get('label'),
                            order=url_item.get('order', idx)
                        )
                        project.urls.append(project_url)
            
            # If it's a dict (new format, single URL)
            elif isinstance(url_data, dict):
                for url_type, url_value in url_data.items():
                    if url_value:
                        project_url = ProjectURL(
                            url_type=url_type,
                            url=url_value,
                            order=0 if url_type == 'github' else 1
                        )
                        project.urls.append(project_url)
        
        # Update translations - properly delete old ones first
        if project_id:
            # Delete existing translations explicitly
            ProjectTranslation.query.filter_by(project_id=project.id).delete()
            db.session.flush()  # Ensure deletion happens before insertion
        
        # Now add new translations
        for lang in ["es", "en"]:
            content = data.get(f"content_{lang}", {})
            t = ProjectTranslation(
                lang=lang,
                title=data.get(f"title_{lang}"),
                subtitle=data.get(f"subtitle_{lang}"),
                description=data.get(f"description_{lang}"),
                cv_description=data.get(f"cv_description_{lang}"),
                summary=data.get(f"summary_{lang}"),
                content=content
            )
            project.translations.append(t)
            
        # Update images
        if project_id:
            # Delete existing images explicitly
            ProjectImage.query.filter_by(project_id=project.id).delete()
            db.session.flush()
        
        for idx, img_data in enumerate(data.get("images", [])):
            img = ProjectImage(
                url=img_data["url"],
                type=img_data.get("type", "image"),
                caption=img_data.get("caption"),
                order=idx,
                # New metadata fields (optional)
                thumbnail_url=img_data.get("thumbnail_url"),
                alt_text=img_data.get("alt_text"),
                width=img_data.get("width"),
                height=img_data.get("height"),
                file_size=img_data.get("file_size"),
                mime_type=img_data.get("mime_type"),
                is_featured=img_data.get("is_featured", False)
            )
            project.images.append(img)
            
        # Update tags
        project.tags = []
        for tag_name in data.get("tags", []):
            if not tag_name: continue
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, slug=tag_name.lower().replace(" ", "-"))
                db.session.add(tag)
            project.tags.append(tag)
            
        db.session.commit()
        invalidate_entities_cache()
        return jsonify({"success": True, "id": project.id, "slug": project.slug}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/admin/delete/project/<int:project_id>", methods=["DELETE", "POST"])
@requires_login
@requires_role("admin")
def delete_project(project_id):
    """Delete a project and all related data (URLs, images, translations, tags)"""
    try:
        project = Project.query.get_or_404(project_id)
        
        # Cascade delete will handle:
        # - ProjectURL entries
        # - ProjectImage entries
        # - ProjectTranslation entries
        # - ProjectAnalytics
        # - ProjectEvent entries
        # Tags are many-to-many, so they won't be deleted
        
        db.session.delete(project)
        db.session.commit()
        invalidate_entities_cache()
        
        return jsonify({"success": True, "message": f"Project '{project.slug}' deleted"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/admin/save/experience", methods=["POST"])
@requires_login
@requires_role("admin")
def save_experience():
    try:
        data = request.json
        # Debug: Log incoming data for 'current' field
        current_app.logger.info(f"save_experience received: current={data.get('current')}, type={type(data.get('current'))}")
        exp_id = data.get("id")
        
        if exp_id:
            exp = Experience.query.get_or_404(exp_id)
        else:
            exp = Experience()
            db.session.add(exp)
        
        # Get company - preserve existing value if not provided during update
        company = data.get("company")
        if exp_id and company is None:
            company = exp.company  # Keep existing company if not provided
        exp.company = company
        
        exp.location = data.get("location")
        
        # Handle slug - auto-generate if not provided
        slug = data.get("slug")
        if not slug:
            # If updating and no new slug provided, keep the existing one
            if exp_id and exp.slug:
                slug = exp.slug
            else:
                # Generate slug from company + title
                import re
                import unicodedata
                def slugify(value):
                    value = str(value) if value else ""
                    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
                    value = re.sub(r'[^\w\s-]', '', value).lower()
                    return re.sub(r'[-\s]+', '-', value).strip('-')
                
                title = data.get("title_en") or data.get("title_es") or "experience"
                company_part = slugify(company) if company else ""
                title_part = slugify(title)
                
                if company_part:
                    base_slug = f"{company_part}-{title_part}" if title_part else company_part
                else:
                    base_slug = title_part or f"experience-{exp_id or 'new'}"
                
                slug = base_slug
                # Ensure uniqueness
                counter = 1
                while Experience.query.filter_by(slug=slug).first():
                    if exp_id:  # If editing, check if it's the same experience
                        existing = Experience.query.filter_by(slug=slug).first()
                        if existing.id == exp_id:
                            break
                    slug = f"{base_slug}-{counter}"
                    counter += 1
        
        exp.slug = slug
        exp.start_date = data.get("startDate")
        exp.end_date = data.get("endDate")
        exp.current = data.get("current", False)
        
        # Translations
        for lang in ["es", "en"]:
            translation = next((t for t in exp.translations if t.lang == lang), None)
            if translation:
                translation.title = data.get(f"title_{lang}")
                translation.description = data.get(f"description_{lang}")
            else:
                t = ExperienceTranslation(
                    lang=lang,
                    title=data.get(f"title_{lang}"), # Role
                    description=data.get(f"description_{lang}")
                )
                exp.translations.append(t)
            
        # Tags (Skills)
        exp.tags = []
        for tag_name in data.get("tags", []):
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, slug=tag_name.lower().replace(" ", "-"))
                db.session.add(tag)
            exp.tags.append(tag)
            
        db.session.commit()
        invalidate_entities_cache()
        return jsonify({"success": True, "id": exp.id}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/admin/save/education", methods=["POST"])
@requires_login
@requires_role("admin")
def save_education():
    try:
        data = request.json
        edu_id = data.get("id")
        
        if edu_id:
            edu = Education.query.get_or_404(edu_id)
        else:
            edu = Education()
            db.session.add(edu)
        
        # Preserve existing values during updates
        institution = data.get("institution")
        if edu_id and institution is None:
            institution = edu.institution
        edu.institution = institution
        
        location = data.get("location")
        if edu_id and location is None:
            location = edu.location
        edu.location = location
        
        edu.start_date = data.get("startDate")
        edu.end_date = data.get("endDate")
        edu.current = data.get("current", False)
        
        # Handle slug - auto-generate if not provided
        slug = data.get("slug")
        if not slug:
            if edu_id and edu.slug:
                slug = edu.slug  # Preserve existing slug during update
            else:
                # Auto-generate from institution and title
                import unicodedata
                import re
                
                def slugify(value):
                    value = str(value) if value else ""
                    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
                    value = re.sub(r'[^\w\s-]', '', value).lower()
                    return re.sub(r'[-\s]+', '-', value).strip('-')
                
                title = data.get("title_en") or data.get("title_es") or ""
                inst_part = slugify(institution) if institution else ""
                title_part = slugify(title)
                
                if inst_part:
                    base_slug = f"{inst_part}-{title_part}" if title_part else inst_part
                else:
                    base_slug = title_part or f"education-{edu_id or 'new'}"
                
                slug = base_slug
                # Ensure uniqueness
                counter = 1
                while Education.query.filter_by(slug=slug).first():
                    if edu_id:
                        existing = Education.query.filter_by(slug=slug).first()
                        if existing.id == edu_id:
                            break
                    slug = f"{base_slug}-{counter}"
                    counter += 1
        
        edu.slug = slug
        
        # Translations
        for lang in ["es", "en"]:
            translation = next((t for t in edu.translations if t.lang == lang), None)
            if translation:
                translation.title = data.get(f"title_{lang}")
                translation.subtitle = data.get(f"subtitle_{lang}")
                translation.description = data.get(f"description_{lang}")
            else:
                t = EducationTranslation(
                    lang=lang,
                    title=data.get(f"title_{lang}"), # Degree
                    subtitle=data.get(f"subtitle_{lang}"), # Field
                    description=data.get(f"description_{lang}")
                )
                edu.translations.append(t)
            
        # Courses
        edu.courses = []
        for idx, course_name in enumerate(data.get("courses", [])):
            c = Course(name=course_name, order=idx)
            edu.courses.append(c)
            
        db.session.commit()
        invalidate_entities_cache()
        return jsonify({"success": True, "id": edu.id}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/admin/save/skill", methods=["POST"])
@requires_login
@requires_role("admin")
def save_skill():
    try:
        data = request.json
        skill_id = data.get("id")
        
        if skill_id:
            skill = Skill.query.get_or_404(skill_id)
        else:
            skill = Skill()
            db.session.add(skill)
            
        # Handle slug
        slug = data.get("slug")
        if not slug:
            # If no slug provided, try to generate from name
            name = data.get("name_en") or data.get("name_es")
            if name:
                import re
                import unicodedata
                def slugify(value):
                    value = str(value)
                    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
                    value = re.sub(r'[^\w\s-]', '', value).lower()
                    return re.sub(r'[-\s]+', '-', value).strip('-')
                slug = slugify(name)
            elif not skill.slug:
                # Fallback for new skills without name (shouldn't happen with validation)
                import time
                slug = f"skill-{int(time.time())}"
        
        if slug:
            skill.slug = slug
        skill.icon_url = data.get("icon_url")
        skill.proficiency = data.get("proficiency", 50)
        skill.category_id = data.get("category_id")
        skill.is_visible_cv = data.get("is_visible_cv", True)
        skill.is_visible_portfolio = data.get("is_visible_portfolio", True)
        skill.order = data.get("order", 0)
        
        # Translations
        for lang in ["es", "en"]:
            translation = next((t for t in skill.translations if t.lang == lang), None)
            if translation:
                translation.name = data.get(f"name_{lang}", skill.slug)
                translation.description = data.get(f"description_{lang}")
            else:
                t = SkillTranslation(
                    lang=lang,
                    name=data.get(f"name_{lang}", skill.slug),
                    description=data.get(f"description_{lang}")
                )
                skill.translations.append(t)
            
        db.session.commit()
        invalidate_entities_cache()
        return jsonify({"success": True, "id": skill.id}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/admin/save/skill-category", methods=["POST"])
@requires_login
@requires_role("admin")
def save_skill_category():
    try:
        data = request.json
        cat_id = data.get("id")
        
        if cat_id:
            cat = SkillCategory.query.get_or_404(cat_id)
        else:
            cat = SkillCategory()
            db.session.add(cat)
            
        cat.slug = data.get("slug")
        cat.order = data.get("order", 0)
        
        # Translations
        for lang in ["es", "en"]:
            translation = next((t for t in cat.translations if t.lang == lang), None)
            if translation:
                translation.name = data.get(f"name_{lang}", cat.slug)
            else:
                t = SkillCategoryTranslation(
                    lang=lang,
                    name=data.get(f"name_{lang}", cat.slug)
                )
                cat.translations.append(t)
            
        db.session.commit()
        invalidate_entities_cache()
        return jsonify({"success": True, "id": cat.id}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/admin/save/certification", methods=["POST"])
@requires_login
@requires_role("admin")
def save_certification():
    try:
        data = request.json
        cert_id = data.get("id")
        
        if cert_id:
            cert = Certification.query.get_or_404(cert_id)
        else:
            cert = Certification()
            db.session.add(cert)
        
        # Preserve existing values during updates, auto-generate slug if needed
        issuer = data.get("issuer")
        if cert_id and issuer is None:
            issuer = cert.issuer
        cert.issuer = issuer
        
        cert.issue_date = data.get("issueDate")
        cert.expiry_date = data.get("expiryDate")
        cert.credential_url = data.get("url")
        
        # Handle slug - auto-generate if not provided
        slug = data.get("slug")
        if not slug:
            if cert_id and cert.slug:
                slug = cert.slug  # Preserve existing slug during update
            else:
                # Auto-generate from title
                import unicodedata
                import re
                
                def slugify(value):
                    value = str(value) if value else ""
                    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
                    value = re.sub(r'[^\w\s-]', '', value).lower()
                    return re.sub(r'[-\s]+', '-', value).strip('-')
                
                title = data.get("title_en") or data.get("title_es") or "certification"
                base_slug = slugify(title)
                
                slug = base_slug
                # Ensure uniqueness
                counter = 1
                while Certification.query.filter_by(slug=slug).first():
                    if cert_id:
                        existing = Certification.query.filter_by(slug=slug).first()
                        if existing.id == cert_id:
                            break
                    slug = f"{base_slug}-{counter}"
                    counter += 1
        
        cert.slug = slug
        
        # Translations
        for lang in ["es", "en"]:
            translation = next((t for t in cert.translations if t.lang == lang), None)
            if translation:
                translation.title = data.get(f"title_{lang}")
                translation.description = data.get(f"description_{lang}")
            else:
                t = CertificationTranslation(
                    lang=lang,
                    title=data.get(f"title_{lang}"),
                    description=data.get(f"description_{lang}")
                )
                cert.translations.append(t)
            
        db.session.commit()
        invalidate_entities_cache()
        return jsonify({"success": True, "id": cert.id}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/admin/save/profile", methods=["POST"])
@requires_login
@requires_role("admin")
def save_profile():
    try:
        data = request.json
        profile = Profile.query.first()
        if not profile:
            profile = Profile(slug="rafael-ortiz-profile")
            db.session.add(profile)
            
        profile.name = data.get("name")
        profile.email = data.get("email")
        profile.location = data.get("location") # JSON
        profile.avatar_url = data.get("avatar_url")
        profile.social_links = data.get("social") # JSON
        
        # Translations
        # Explicitly delete existing translations to avoid unique constraint violations
        if profile.id:
            ProfileTranslation.query.filter_by(profile_id=profile.id).delete()
            db.session.flush()
            
        profile.translations = []
        for lang in ["es", "en"]:
            t = ProfileTranslation(
                lang=lang,
                role=data.get(f"role_{lang}"),
                tagline=data.get(f"tagline_{lang}"),
                bio=data.get(f"bio_{lang}")
            )
            profile.translations.append(t)
            
        db.session.commit()
        invalidate_entities_cache()
        return jsonify({"success": True}), 200
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        current_app.logger.error(f"Error saving profile: {e}\n{error_details}")
        db.session.rollback()
        return jsonify({"error": f"Error saving profile: {str(e)}"}), 500


# ==========================================
# DELETE ENDPOINTS
# ==========================================

@admin_bp.route("/admin/delete/<type>/<int:id>", methods=["DELETE"])
@requires_login
@requires_role("admin")
def delete_item(type, id):
    try:
        if type == "project":
            item = Project.query.get_or_404(id)
        elif type == "experience":
            item = Experience.query.get_or_404(id)
        elif type == "education":
            item = Education.query.get_or_404(id)
        elif type == "skill":
            item = Skill.query.get_or_404(id)
        elif type == "certification":
            item = Certification.query.get_or_404(id)
        elif type == "skill-category":
            item = SkillCategory.query.get_or_404(id)
            # Unlink skills before deleting category
            for skill in item.skills:
                skill.category_id = None
                db.session.add(skill)
            
        db.session.delete(item)
        db.session.commit()
        invalidate_entities_cache()
        return jsonify({"success": True}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ==========================================
# UTILITY ENDPOINTS
# ==========================================



@admin_bp.route("/admin/upload-image", methods=["POST"])
@requires_login
@requires_role("admin")
def upload_image():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400
    
    file = request.files["file"]
    folder = request.form.get("folder", "portfolio")
    
    result = cloudinary_service.upload_image(file, folder=folder)
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 500


@admin_bp.route("/admin/delete-image", methods=["POST"])
@requires_login
@requires_role("admin")
def delete_image():
    data = request.get_json()
    public_id = data.get("public_id")
    
    if not public_id:
        return jsonify({"success": False, "error": "No public_id provided"}), 400
        
    result = cloudinary_service.delete_image(public_id)
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 500


@admin_bp.route("/admin/backup", methods=["GET"])
@requires_login
@requires_role("admin")
def backup_database():
    """Create a JSON backup of all database data"""
    try:
        from datetime import datetime
        from flask import make_response
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        backup_data = {
            'timestamp': timestamp,
            'version': '1.0',
            'projects': [],
            'experiences': [],
            'education': [],
            'skills': [],
            'certifications': [],
            'profile': None
        }
        
        # Backup Projects
        for p in Project.query.all():
            backup_data['projects'].append({
                'id': p.id,
                'slug': p.slug,
                'category': p.category,
                'is_featured_cv': p.is_featured_cv,
                'created_at': p.created_at.isoformat() if p.created_at else None,
                'translations': [{
                    'lang': t.lang,
                    'title': t.title,
                    'subtitle': t.subtitle,
                    'description': t.description,
                    'summary': t.summary,
                    'content': t.content,
                    'cv_description': getattr(t, 'cv_description', None)
                } for t in p.translations],
                'urls': [{
                    'url_type': u.url_type,
                    'url': u.url,
                    'order': u.order
                } for u in p.urls],
                'images': [{
                    'url': img.url,
                    'type': img.type,
                    'alt_text': getattr(img, 'alt_text', None),
                    'width': getattr(img, 'width', None),
                    'height': getattr(img, 'height', None),
                    'is_featured': getattr(img, 'is_featured', False),
                    'order': img.order
                } for img in p.images],
                'tags': [{'name': tag.name, 'slug': tag.slug} for tag in p.tags]
            })
        
        # Backup Experiences
        for e in Experience.query.all():
            backup_data['experiences'].append({
                'id': e.id,
                'slug': e.slug,
                'company': e.company,
                'location': e.location,
                'start_date': e.start_date if isinstance(e.start_date, str) else (e.start_date.isoformat() if e.start_date else None),
                'end_date': e.end_date if isinstance(e.end_date, str) else (e.end_date.isoformat() if e.end_date else None),
                'current': e.current,
                'translations': [{
                    'lang': t.lang,
                    'title': t.title,
                    'description': t.description
                } for t in e.translations],
                'tags': [{'name': tag.name} for tag in e.tags]
            })
        
        # Backup Education
        for edu in Education.query.all():
            backup_data['education'].append({
                'id': edu.id,
                'slug': edu.slug,
                'institution': edu.institution,
                'location': edu.location,
                'start_date': edu.start_date if isinstance(edu.start_date, str) else (edu.start_date.isoformat() if edu.start_date else None),
                'end_date': edu.end_date if isinstance(edu.end_date, str) else (edu.end_date.isoformat() if edu.end_date else None),
                'current': edu.current,
                'courses': [{'name': c.name, 'order': c.order} for c in edu.courses],
                'translations': [{
                    'lang': t.lang,
                    'title': t.title,
                    'description': t.description
                } for t in edu.translations]
            })
        
        # Backup Skill Categories
        backup_data['skill_categories'] = []
        for sc in SkillCategory.query.all():
            backup_data['skill_categories'].append({
                'id': sc.id,
                'slug': sc.slug,
                'order': sc.order,
                'translations': [{
                    'lang': t.lang,
                    'name': t.name
                } for t in sc.translations]
            })
        
        # Backup Skills
        for s in Skill.query.all():
            backup_data['skills'].append({
                'id': s.id,
                'slug': s.slug,
                'category': s.category,  # Legacy field
                'category_id': s.category_id,
                'proficiency': s.proficiency,
                'icon_url': s.icon_url,
                'is_visible_cv': s.is_visible_cv,
                'is_visible_portfolio': s.is_visible_portfolio,
                'order': s.order,
                'translations': [{
                    'lang': t.lang,
                    'name': t.name,
                    'description': t.description
                } for t in s.translations]
            })
        
        # Backup Certifications
        for c in Certification.query.all():
            backup_data['certifications'].append({
                'id': c.id,
                'slug': c.slug,
                'issuer': c.issuer,
                'issue_date': c.issue_date if isinstance(c.issue_date, str) else (c.issue_date.isoformat() if c.issue_date else None),
                'expiry_date': c.expiry_date if isinstance(c.expiry_date, str) else (c.expiry_date.isoformat() if c.expiry_date else None),
                'credential_url': c.credential_url,
                'translations': [{
                    'lang': t.lang,
                    'title': t.title,
                    'description': t.description
                } for t in c.translations]
            })
        
        # Backup Profile
        profile = Profile.query.first()
        if profile:
            backup_data['profile'] = {
                'id': profile.id,
                'name': profile.name,
                'email': profile.email,
                'location': profile.location,
                'social_links': profile.social_links,
                'translations': [{
                    'lang': t.lang,
                    'role': t.role,
                    'tagline': t.tagline,
                    'bio': t.bio
                } for t in profile.translations]
            }
        
        
        # Create response with JSON file download
        response = make_response(json.dumps(backup_data, indent=2, ensure_ascii=False))
        response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Disposition'] = f'attachment; filename=portfolio_backup_{timestamp}.json'
        
        return response
        
    except Exception as e:
        import traceback
        current_app.logger.error(f"Backup failed: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500



@admin_bp.route("/admin/cloudinary/browse", methods=["GET"])
@admin_bp.route("/admin/cloudinary/browse/<project_slug>", methods=["GET"])
@requires_login
@requires_role("admin")
def browse_cloudinary(project_slug=None):
    try:
        prefix = f"portfolio/{project_slug}/" if project_slug else "portfolio/"
        
        result = cloudinary.api.resources(
            type="upload",
            prefix=prefix,
            max_results=500,
            resource_type="image"
        )
        
        images = [{
            "public_id": r["public_id"],
            "url": r["secure_url"],
            "thumbnail": r.get("thumbnail_url", r["secure_url"]),
            "created_at": r.get("created_at")
        } for r in result.get("resources", [])]
        
        return jsonify({"success": True, "images": images}), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_bp.route("/admin/ai/import-github", methods=["POST"])
@requires_login
@requires_role("admin")
def import_github_project():
    """Import project content from GitHub using AI"""
    try:
        data = request.json
        github_url = data.get('github_url')
        
        if not github_url:
            return jsonify({"error": "GitHub URL is required"}), 400
        
        # 1. Fetch Repo Content
        github_service = GitHubService()
        repo_context = github_service.get_repo_content(github_url)
        
        model_name = data.get('model_name')
        
        # 2. Analyze with AI
        ai_service = AIProjectGenerator()
        generated_data = ai_service.analyze_github_repo(repo_context, repo_url=github_url, model_name=model_name)
        
        return jsonify({
            "success": True,
            "data": generated_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"GitHub Import failed: {str(e)}")
        return jsonify({"error": str(e)}), 500
