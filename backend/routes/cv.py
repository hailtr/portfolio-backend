"""
CV routes for displaying and generating PDF resumes.
"""

from flask import Blueprint, render_template, request, send_file, jsonify, current_app
from backend import db
from backend.models.profile import Profile
from backend.models.experience import Experience
from backend.models.education import Education
from backend.models.skill import Skill
from backend.models.certification import Certification
from backend.services.pdf_service import PDFService
from sqlalchemy import desc
import json
import os

cv_bp = Blueprint("cv", __name__)

def build_cv_from_models(lang="es"):
    """Build JSON Resume format from database models"""
    from sqlalchemy.orm import joinedload
    
    current_app.logger.info(f"Building CV for language: {lang}")
    try:
        # 1. Fetch Profile with eager loading
        profile = Profile.query.options(joinedload(Profile.translations)).first()
        if not profile:
            return None

        # Get translation
        p_trans = next((t for t in profile.translations if t.lang == lang), None)
        # Fallback to any translation if specific lang not found
        if not p_trans and profile.translations:
            p_trans = profile.translations[0]

        # Parse location and social links
        location_data = profile.location if isinstance(profile.location, dict) else {}
        if isinstance(profile.location, str):
            try:
                location_data = json.loads(profile.location)
            except:
                location_data = {}

        social_data = profile.social_links if isinstance(profile.social_links, dict) else {}
        if isinstance(profile.social_links, str):
            try:
                social_data = json.loads(profile.social_links)
            except:
                social_data = {}

        profiles_list = []
        for network, url in social_data.items():
            if url:
                profiles_list.append({
                    "network": network.capitalize(),
                    "username": "",
                    "url": url
                })

        # Get summary - use bio if available, otherwise tagline
        summary = ""
        if p_trans:
            summary = p_trans.bio or p_trans.tagline or ""
            current_app.logger.info(f"Profile summary length: {len(summary)}, has bio: {bool(p_trans.bio)}, has tagline: {bool(p_trans.tagline)}")
        
        cv_data = {
            "basics": {
                "name": profile.name,
                "label": p_trans.role if p_trans else "",
                "email": profile.email or "",
                "phone": location_data.get("phone", ""),  # Try to get phone from location data
                "summary": summary,
                "image": profile.avatar_url,
                "location": {
                    "city": location_data.get("city", ""),
                    "region": location_data.get("region", ""),
                    "countryCode": location_data.get("country", "")[:2].upper() if location_data.get("country") else ""
                },
                "profiles": profiles_list
            },
            "work": [],
            "education": [],
            "skills": [],
            "awards": [],
            "languages": [],
            "interests": []
        }

        # 2. Fetch Experience with eager loading
        experiences = Experience.query.options(joinedload(Experience.translations)).order_by(desc(Experience.start_date)).all()
        for exp in experiences:
            trans = next((t for t in exp.translations if t.lang == lang), None)
            if not trans: continue

            # Parse description to extract summary and highlights
            # Description might contain bullet points (lines starting with -, *, or •)
            summary = ""
            highlights = []
            
            if trans.description:
                lines = trans.description.strip().split('\n')
                summary_lines = []
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    # Check if line is a bullet point
                    if line.startswith(('-', '*', '•', '·')):
                        # Remove bullet marker and add to highlights
                        highlights.append(line.lstrip('-*•· ').strip())
                    else:
                        # Add to summary if we haven't started collecting highlights yet
                        if not highlights:
                            summary_lines.append(line)
                        else:
                            # If we already have highlights, this might be a continuation
                            highlights.append(line)
                
                summary = ' '.join(summary_lines)

            cv_data["work"].append({
                "company": trans.title,  # Using title as Company Name based on user preference
                "position": trans.subtitle,  # Using subtitle as Role
                "url": "",  # Experience model doesn't have URL explicitly
                "startDate": exp.start_date.strftime("%Y-%m-%d") if exp.start_date else "",
                "endDate": exp.end_date.strftime("%Y-%m-%d") if exp.end_date else "",
                "summary": summary,
                "highlights": highlights
            })

        # 3. Fetch Education with eager loading
        educations = Education.query.options(
            joinedload(Education.translations),
            joinedload(Education.courses)
        ).order_by(desc(Education.start_date)).all()
        for edu in educations:
            trans = next((t for t in edu.translations if t.lang == lang), None)
            if not trans: continue

            # Extract course names from Course objects
            course_names = [course.name for course in sorted(edu.courses, key=lambda c: c.order)] if edu.courses else []
            
            cv_data["education"].append({
                "institution": edu.institution,
                "area": trans.subtitle, # Field of Study
                "studyType": trans.title, # Degree
                "startDate": edu.start_date.strftime("%Y-%m-%d") if edu.start_date else "",
                "endDate": edu.end_date.strftime("%Y-%m-%d") if edu.end_date else "",
                "location": edu.location,
                "courses": course_names
            })

        # 4. Fetch Skills with eager loading
        skills = Skill.query.options(joinedload(Skill.translations)).order_by(Skill.order).all()
        skills_by_category = {}
        
        # Helper for category names
        category_map = {
            "languages": "Lenguajes" if lang == "es" else "Languages",
            "frameworks": "Frameworks",
            "tools": "Herramientas" if lang == "es" else "Tools",
            "databases": "Bases de Datos" if lang == "es" else "Databases",
            "cloud": "Cloud",
            "other": "Otros" if lang == "es" else "Other"
        }

        for skill in skills:
            trans = next((t for t in skill.translations if t.lang == lang), None)
            name = trans.name if trans else skill.slug
            
            cat = skill.category.lower() if skill.category else "other"
            if cat not in skills_by_category:
                skills_by_category[cat] = []
            
            skills_by_category[cat].append(name)

        for cat, keywords in skills_by_category.items():
            cv_data["skills"].append({
                "name": category_map.get(cat, cat.capitalize()),
                "keywords": keywords
            })

        # 5. Fetch Certifications (Awards) with eager loading
        certs = Certification.query.options(joinedload(Certification.translations)).order_by(desc(Certification.issue_date)).all()
        for cert in certs:
            trans = next((t for t in cert.translations if t.lang == lang), None)
            if not trans: continue

            cv_data["awards"].append({
                "title": trans.title,
                "date": cert.issue_date.strftime("%Y-%m-%d") if cert.issue_date else "",
                "awarder": cert.issuer,
                "summary": trans.description,
                "link": cert.credential_url
            })

        # 6. Languages (Hardcoded for now as they aren't in a model yet, or use Skills?)
        # User has 'languages' in skills usually, but CV template expects separate 'languages' key
        # We can try to extract from skills if category is 'languages'
        # For now, let's leave it empty or add a default
        cv_data["languages"] = [
            {
                "language": "Español" if lang == "es" else "Spanish",
                "fluency": "Nativo" if lang == "es" else "Native"
            },
            {
                "language": "Inglés" if lang == "es" else "English",
                "fluency": "Fluido" if lang == "es" else "Fluent" # Assumption
            }
        ]

        return cv_data

    except Exception as e:
        import traceback
        current_app.logger.error(f"Error building CV: {e}")
        current_app.logger.error(traceback.format_exc())
        raise e


@cv_bp.route("/cv", methods=["GET"])
def cv_view():
    """Render CV HTML page"""
    try:
        lang = request.args.get("lang", "es")
        cv_data = build_cv_from_models(lang)

        if not cv_data:
             return render_template(
                "error.html",
                error="CV data not found. Please ensure your profile is set up in the Admin Panel."
            ), 404

        return render_template("cv.html", cv_data=cv_data, lang=lang)
    except Exception as e:
        import traceback
        return render_template(
            "error.html",
            error="Error generating CV",
            details=traceback.format_exc()
        ), 500


@cv_bp.route("/cv/pdf", methods=["GET"])
def cv_pdf():
    """Generate and download CV PDF"""
    try:
        lang = request.args.get("lang", "es")
        cv_data = build_cv_from_models(lang)

        if not cv_data:
            return jsonify({"error": "CV data not found"}), 404

        pdf_service = PDFService()
        pdf_bytes = pdf_service.generate_cv_pdf(cv_data, lang)

        filename = f"CV_Rafael_Ortiz_{lang}.pdf"

        return send_file(
            pdf_bytes,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename,
        )
    except Exception as e:
        import traceback
        return render_template(
            "error.html",
            error="Error generating PDF",
            details=traceback.format_exc()
        ), 500


@cv_bp.route("/cv/debug", methods=["GET"])
def cv_debug():
    """Debug endpoint to view raw CV data as JSON"""
    try:
        lang = request.args.get("lang", "es")
        cv_data = build_cv_from_models(lang)
        return jsonify(cv_data), 200
    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@cv_bp.route("/cv/inspect", methods=["GET"])
def cv_inspect():
    """Inspect actual database content for CV data"""
    try:
        from backend.models.profile import Profile
        from backend.models.experience import Experience
        from backend.models.education import Education
        from backend.models.skill import Skill
        from backend.models.certification import Certification
        
        output = []
        output.append("<html><head><style>")
        output.append("body { font-family: monospace; padding: 20px; background: #1e1e1e; color: #d4d4d4; }")
        output.append("h1 { color: #4ec9b0; }")
        output.append("h2 { color: #569cd6; margin-top: 30px; }")
        output.append("h3 { color: #dcdcaa; margin-top: 20px; }")
        output.append(".field { margin: 10px 0; }")
        output.append(".label { color: #9cdcfe; }")
        output.append(".value { color: #ce9178; }")
        output.append("pre { background: #2d2d2d; padding: 10px; border-radius: 5px; overflow-x: auto; }")
        output.append("</style></head><body>")
        
        output.append("<h1>CV Data Inspection</h1>")
        
        # Profile
        output.append("<h2>PROFILE</h2>")
        profile = Profile.query.first()
        if profile:
            output.append(f"<div class='field'><span class='label'>Name:</span> <span class='value'>{profile.name}</span></div>")
            output.append(f"<div class='field'><span class='label'>Email:</span> <span class='value'>{profile.email}</span></div>")
            output.append(f"<div class='field'><span class='label'>Avatar URL:</span> <span class='value'>{profile.avatar_url}</span></div>")
            output.append(f"<div class='field'><span class='label'>Location:</span> <span class='value'>{profile.location}</span></div>")
            output.append(f"<div class='field'><span class='label'>Social Links:</span> <span class='value'>{profile.social_links}</span></div>")
            
            for trans in profile.translations:
                output.append(f"<h3>Translation ({trans.lang})</h3>")
                output.append(f"<div class='field'><span class='label'>Role:</span> <span class='value'>{trans.role}</span></div>")
                output.append(f"<div class='field'><span class='label'>Tagline:</span> <span class='value'>{trans.tagline}</span></div>")
                output.append(f"<div class='field'><span class='label'>Bio:</span></div>")
                output.append(f"<pre>{trans.bio if trans.bio else 'None'}</pre>")
        else:
            output.append("<p>No profile found!</p>")
        
        # Experience
        output.append("<h2>EXPERIENCE</h2>")
        experiences = Experience.query.all()
        for exp in experiences:
            output.append(f"<h3>{exp.slug}</h3>")
            output.append(f"<div class='field'><span class='label'>Company:</span> <span class='value'>{exp.company}</span></div>")
            output.append(f"<div class='field'><span class='label'>Location:</span> <span class='value'>{exp.location}</span></div>")
            output.append(f"<div class='field'><span class='label'>Dates:</span> <span class='value'>{exp.start_date} to {exp.end_date}</span></div>")
            
            for trans in exp.translations:
                output.append(f"<h4>Translation ({trans.lang})</h4>")
                output.append(f"<div class='field'><span class='label'>Title:</span> <span class='value'>{trans.title}</span></div>")
                output.append(f"<div class='field'><span class='label'>Subtitle:</span> <span class='value'>{trans.subtitle}</span></div>")
                output.append(f"<div class='field'><span class='label'>Description:</span></div>")
                output.append(f"<pre>{trans.description if trans.description else 'None'}</pre>")
        
        # Education
        output.append("<h2>EDUCATION</h2>")
        educations = Education.query.all()
        for edu in educations:
            output.append(f"<h3>{edu.slug}</h3>")
            output.append(f"<div class='field'><span class='label'>Institution:</span> <span class='value'>{edu.institution}</span></div>")
            output.append(f"<div class='field'><span class='label'>Location:</span> <span class='value'>{edu.location}</span></div>")
            
            for trans in edu.translations:
                output.append(f"<h4>Translation ({trans.lang})</h4>")
                output.append(f"<div class='field'><span class='label'>Title:</span> <span class='value'>{trans.title}</span></div>")
                output.append(f"<div class='field'><span class='label'>Subtitle:</span> <span class='value'>{trans.subtitle}</span></div>")
        
        output.append("</body></html>")
        return ''.join(output)
        
    except Exception as e:
        import traceback
        return f"<pre>{traceback.format_exc()}</pre>", 500


@cv_bp.route("/cv/data-check", methods=["GET"])
def data_check():
    """Check all possible locations for CV data"""
    try:
        from backend.models.cv import CVProfile
        from backend.models.profile import Profile
        from backend.models.experience import Experience
        
        result = {
            "cv_tables": {},
            "profile_tables": {},
            "experience_tables": {},
            "entity_tables": {}
        }
        
        # Check CV tables
        try:
            cv_profiles = CVProfile.query.all()
            result["cv_tables"]["count"] = len(cv_profiles)
            result["cv_tables"]["data"] = []
            for cv in cv_profiles:
                cv_data = {
                    "slug": cv.slug,
                    "email": cv.email,
                    "phone": cv.phone,
                    "translations": []
                }
                for trans in cv.translations:
                    cv_data["translations"].append({
                        "lang": trans.lang,
                        "name": trans.name,
                        "label": trans.label,
                        "summary": trans.summary
                    })
                
                cv_data["work_sections"] = len([s for s in cv.sections if s.section_type == 'work'])
                result["cv_tables"]["data"].append(cv_data)
        except Exception as e:
            result["cv_tables"]["error"] = str(e)
        
        # Check Profile tables
        try:
            profiles = Profile.query.all()
            result["profile_tables"]["count"] = len(profiles)
            result["profile_tables"]["data"] = []
            for p in profiles:
                p_data = {
                    "name": p.name,
                    "email": p.email,
                    "translations": []
                }
                for trans in p.translations:
                    p_data["translations"].append({
                        "lang": trans.lang,
                        "role": trans.role,
                        "tagline": trans.tagline,
                        "bio": trans.bio[:200] if trans.bio else None
                    })
                result["profile_tables"]["data"].append(p_data)
        except Exception as e:
            result["profile_tables"]["error"] = str(e)
        
        # Check Experience tables
        try:
            experiences = Experience.query.all()
            result["experience_tables"]["count"] = len(experiences)
            result["experience_tables"]["data"] = []
            for exp in experiences[:3]:  # First 3
                exp_data = {
                    "slug": exp.slug,
                    "company": exp.company,
                    "translations": []
                }
                for trans in exp.translations:
                    exp_data["translations"].append({
                        "lang": trans.lang,
                        "title": trans.title,
                        "subtitle": trans.subtitle,
                        "description": trans.description[:200] if trans.description else None
                    })
                result["experience_tables"]["data"].append(exp_data)
        except Exception as e:
            result["experience_tables"]["error"] = str(e)
        
        # Check Entity tables (carefully)
        try:
            # Try to import and query, but don't fail if it doesn't work
            from backend.models.entity import Entity
            entities = Entity.query.filter_by(type='profile').all()
            result["entity_tables"]["profile_count"] = len(entities)
            
            exp_entities = Entity.query.filter_by(type='experience').all()
            result["entity_tables"]["experience_count"] = len(exp_entities)
        except Exception as e:
            result["entity_tables"]["error"] = str(e)
        
        return jsonify(result), 200
        
    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500
