"""
REST API endpoints for portfolio data.
Refactored to use proper relational models.
"""

from flask import Blueprint, jsonify, request
from backend import db
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from backend.models.project import Project, ProjectTranslation
from backend.models.experience import Experience, ExperienceTranslation
from backend.models.education import Education, EducationTranslation
from backend.models.skill import Skill, SkillTranslation
from backend.models.profile import Profile, ProfileTranslation
from backend.models.certification import Certification, CertificationTranslation
from backend.models.tag import Tag
from backend.services.cache_service import cache_response, cache_key_with_lang, cache_key_simple
from backend.utils.rate_limit import api_rate_limit, generous_rate_limit
import os
import json

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health", methods=["GET"])
@generous_rate_limit()
def health_check():
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503


# ==========================================
# PROJECTS
# ==========================================

@api_bp.route("/projects", methods=["GET"])
@api_rate_limit()
@cache_response(timeout=300, key_func=cache_key_with_lang)
def get_projects():
    lang = request.args.get("lang", "es")
    category = request.args.get("category")

    query = Project.query.options(
        joinedload(Project.translations),
        joinedload(Project.images),
        joinedload(Project.tags),
        joinedload(Project.urls)
    )

    if category:
        query = query.filter(Project.category == category)

    projects = query.order_by(desc(Project.created_at)).all()
    
    result = []
    for p in projects:
        trans = next((t for t in p.translations if t.lang == lang), None)
        if not trans and p.translations:
            trans = p.translations[0]
            
        if trans:
            # Sort images by order
            images = sorted(p.images, key=lambda x: x.order)
            
            # Find preview video (gif or video type)
            preview_video = next((img.url for img in images if img.type in ['video', 'gif']), None)
            
            # Serialize URLs
            urls = [
                {
                    "type": url.url_type,
                    "url": url.url,
                    "label": url.label,
                    "order": url.order
                } for url in sorted(p.urls or [], key=lambda x: x.order)
            ]
            
            result.append({
                "id": p.id,
                "slug": p.slug,
                "category": p.category,
                "urls": urls,
                "title": trans.title,
                "subtitle": trans.subtitle,
                "summary": trans.summary,
                "description": trans.description,
                "content": trans.content,
                "tags": [t.name for t in p.tags],
                "images": [{
                    "url": img.url,
                    "type": img.type,
                    "caption": img.caption,
                    "order": img.order,
                    "thumbnail_url": img.thumbnail_url,
                    "alt_text": img.alt_text,
                    "width": img.width,
                    "height": img.height,
                    "is_featured": img.is_featured
                } for img in images],
                # Backward compatibility fields
                "desktop_image": images[0].url if images else None,
                "mobile_image": images[1].url if len(images) > 1 else None,
                "preview_video": preview_video,
                "created_at": p.created_at.isoformat() if p.created_at else None
            })
            
    return jsonify(result), 200


@api_bp.route("/projects/<slug>", methods=["GET"])
@api_rate_limit()
@cache_response(timeout=300, key_func=cache_key_with_lang)
def get_project(slug):
    lang = request.args.get("lang", "es")
    
    project = Project.query.options(
        joinedload(Project.translations),
        joinedload(Project.images),
        joinedload(Project.tags),
        joinedload(Project.urls)
    ).filter_by(slug=slug).first()
    
    if not project:
        return jsonify({"error": "Project not found"}), 404
        
    trans = next((t for t in project.translations if t.lang == lang), None)
    if not trans and project.translations:
        trans = project.translations[0]
        
    images = sorted(project.images, key=lambda x: x.order)
    preview_video = next((img.url for img in images if img.type in ['video', 'gif']), None)
    
    # Serialize URLs
    urls = [
        {
            "type": url.url_type,
            "url": url.url,
            "label": url.label,
            "order": url.order
        } for url in sorted(project.urls or [], key=lambda x: x.order)
    ]
    
    return jsonify({
        "id": project.id,
        "slug": project.slug,
        "category": project.category,
        "urls": urls,
        "title": trans.title if trans else "",
        "subtitle": trans.subtitle if trans else "",
        "summary": trans.summary if trans else "",
        "description": trans.description if trans else "",
        "content": trans.content if trans else {},
        "tags": [t.name for t in project.tags],
        "images": [{
            "url": img.url,
            "type": img.type,
            "caption": img.caption,
            "order": img.order,
            "thumbnail_url": img.thumbnail_url,
            "alt_text": img.alt_text,
            "width": img.width,
            "height": img.height,
            "is_featured": img.is_featured
        } for img in images],
        "preview_video": preview_video,
        "desktop_image": images[0].url if images else None,
        "mobile_image": images[1].url if len(images) > 1 else None,
        "created_at": project.created_at.isoformat() if project.created_at else None
    }), 200


# ==========================================
# EXPERIENCE
# ==========================================

@api_bp.route("/experience", methods=["GET"])
@api_rate_limit()
@cache_response(timeout=300, key_func=cache_key_with_lang)
def get_experience():
    lang = request.args.get("lang", "es")
    
    exps = Experience.query.options(
        joinedload(Experience.translations),
        joinedload(Experience.tags)
    ).order_by(desc(Experience.start_date)).all()
    
    result = []
    for e in exps:
        trans = next((t for t in e.translations if t.lang == lang), None)
        if not trans and e.translations:
            trans = e.translations[0]
            
        if trans:
            result.append({
                "id": e.id,
                "slug": e.slug,
                "company": trans.title,  # Title holds Company Name in DB
                "location": e.location,
                "startDate": e.start_date,
                "endDate": e.end_date,
                "current": e.current,
                "title": trans.subtitle,  # Subtitle holds Job Role in DB
                "description": trans.description,
                "tags": [t.name for t in e.tags]
            })
            
    return jsonify(result), 200


# ==========================================
# EDUCATION
# ==========================================

@api_bp.route("/education", methods=["GET"])
@api_rate_limit()
@cache_response(timeout=300, key_func=cache_key_with_lang)
def get_education():
    lang = request.args.get("lang", "es")
    
    edus = Education.query.options(
        joinedload(Education.translations),
        joinedload(Education.courses)
    ).order_by(desc(Education.start_date)).all()
    
    result = []
    for e in edus:
        trans = next((t for t in e.translations if t.lang == lang), None)
        if not trans and e.translations:
            trans = e.translations[0]
            
        if trans:
            result.append({
                "id": e.id,
                "slug": e.slug,
                "institution": e.institution,
                "location": e.location,
                "startDate": e.start_date,
                "endDate": e.end_date,
                "current": e.current,
                "title": trans.title,  # Degree
                "subtitle": trans.subtitle, # Field
                "description": trans.description,
                "courses": [c.name for c in sorted(e.courses, key=lambda x: x.order)]
            })
            
    return jsonify(result), 200


# ==========================================
# SKILLS
# ==========================================

@api_bp.route("/skills", methods=["GET"])
@api_rate_limit()
@cache_response(timeout=300, key_func=cache_key_with_lang)
def get_skills():
    lang = request.args.get("lang", "es")
    
    skills = Skill.query.options(
        joinedload(Skill.translations)
    ).order_by(Skill.order).all()
    
    result = []
    for s in skills:
        trans = next((t for t in s.translations if t.lang == lang), None)
        if not trans and s.translations:
            trans = s.translations[0]
            
        if trans:
            result.append({
                "id": s.id,
                "slug": s.slug,
                "icon_url": s.icon_url,
                "proficiency": s.proficiency,
                "category": s.category,
                "name": trans.name,
                "description": trans.description
            })
            
    return jsonify(result), 200


# ==========================================
# CERTIFICATIONS
# ==========================================

@api_bp.route("/certifications", methods=["GET"])
@api_rate_limit()
@cache_response(timeout=300, key_func=cache_key_with_lang)
def get_certifications():
    lang = request.args.get("lang", "es")
    
    certs = Certification.query.options(
        joinedload(Certification.translations)
    ).order_by(desc(Certification.issue_date)).all()
    
    result = []
    for c in certs:
        trans = next((t for t in c.translations if t.lang == lang), None)
        if not trans and c.translations:
            trans = c.translations[0]
            
        if trans:
            result.append({
                "id": c.id,
                "slug": c.slug,
                "issuer": c.issuer,
                "issueDate": c.issue_date,
                "expiryDate": c.expiry_date,
                "url": c.credential_url,
                "title": trans.title,
                "description": trans.description
            })
            
    return jsonify(result), 200


# ==========================================
# PROFILE
# ==========================================

@api_bp.route("/profile", methods=["GET"])
@api_rate_limit()
@cache_response(timeout=300, key_func=cache_key_with_lang)
def get_profile():
    lang = request.args.get("lang", "es")
    
    profile = Profile.query.options(
        joinedload(Profile.translations)
    ).first()  # Assuming single profile
    
    if not profile:
        return jsonify({"error": "Profile not found"}), 404
        
    trans = next((t for t in profile.translations if t.lang == lang), None)
    if not trans and profile.translations:
        trans = profile.translations[0]
        
    return jsonify({
        "name": profile.name,
        "email": profile.email,
        "location": profile.location,
        "avatar_url": profile.avatar_url,
        "social": profile.social_links,
        "role": trans.role if trans else "",
        "tagline": trans.tagline if trans else "",
        "bio": trans.bio if trans else ""
    }), 200


# ==========================================
# CV (Legacy/File based)
# ==========================================

@api_bp.route("/cv", methods=["GET"])
@api_rate_limit()
@cache_response(timeout=600, key_func=cache_key_with_lang)
def get_cv():
    lang = request.args.get("lang", "es")
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "resume.json"
    )
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            resume_data = json.load(f)
        return jsonify(resume_data.get(lang, resume_data.get("es", {}))), 200
    except Exception as e:
        return jsonify({"error": "CV data not found"}), 404
