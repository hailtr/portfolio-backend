"""
CV routes for displaying and generating PDF resumes.

Uses PostgreSQL with caching, falls back to JSON file if database not available.
"""

from flask import Blueprint, render_template, request, send_file, jsonify
from backend import db
from backend.services.cv_cache import get_cached_cv, set_cached_cv, invalidate_cv_cache
import json
import os

# Import PDF service (will work on Railway/Linux)
from backend.services.pdf_service import PDFService

# Lazy import CV models (may not exist yet)
try:
    from backend.models.cv import CVProfile
    CV_MODEL_AVAILABLE = True
except ImportError:
    CV_MODEL_AVAILABLE = False

cv_bp = Blueprint('cv', __name__)


def get_cv_data_from_db(lang='es', profile_slug='default'):
    """Get CV data from PostgreSQL database"""
    if not CV_MODEL_AVAILABLE:
        return None
    
    try:
        profile = CVProfile.query.filter_by(slug=profile_slug, is_active=True).first()
        if not profile:
            return None
        
        return profile.to_dict(lang)
    except Exception:
        # Database error, fall back to JSON
        return None


def get_cv_data_from_json(lang='es'):
    """Load CV data from backend/data/resume.json (fallback)"""
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'data', 
        'resume.json'
    )
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
        return resume_data.get(lang, resume_data.get('es', {}))
    except Exception:
        return {}


def build_cv_from_entities(lang='es'):
    """Build JSON Resume format from database entities"""
    from backend.models.entity import Entity
    from sqlalchemy.orm import joinedload
    
    try:
        # Get profile entity for dynamic data
        profile_entity = Entity.query.options(joinedload(Entity.translations)).filter_by(type='profile', slug='rafael-ortiz-profile').first()
        
        # Default values
        name = "Rafael Ortiz"
        label = ""
        email = "lustigrfortiz@gmail.com"
        phone = "+58 424-2700455"
        summary = ""
        location = {"city": "Caracas", "region": "Distrito Capital", "countryCode": "VE"}
        profiles = []
        
        # Override with profile entity if exists
        if profile_entity:
            # Get name from meta (not from translation.title which is the role)
            if profile_entity.meta and 'name' in profile_entity.meta:
                name = profile_entity.meta['name']
            
            profile_trans = next((t for t in profile_entity.translations if t.lang == lang), None)
            if profile_trans:
                # title is the role, subtitle is tagline, summary is summary
                if profile_trans.title:
                    label = profile_trans.title  # This is the role (Data Engineer)
                if profile_trans.summary:
                    summary = profile_trans.summary
            
            if profile_entity.meta:
                email = profile_entity.meta.get('email', email)
                phone = profile_entity.meta.get('phone', phone)
                if 'location' in profile_entity.meta:
                    loc = profile_entity.meta['location']
                    location = {
                        "city": loc.get('city', ''),
                        "region": loc.get('region', ''),
                        "countryCode": loc.get('country', '')[:2].upper() if loc.get('country') else ''
                    }
                if 'social' in profile_entity.meta:
                    social = profile_entity.meta['social']
                    if 'linkedin' in social:
                        profiles.append({"network": "LinkedIn", "username": "", "url": social['linkedin']})
                    if 'github' in social:
                        profiles.append({"network": "GitHub", "username": "", "url": social['github']})
                    if 'website' in social:
                        profiles.append({"network": "Website", "username": "", "url": social['website']})
        
        cv_data = {
            "basics": {
                "name": name,
                "label": label,
                "email": email,
                "phone": phone,
                "summary": summary,
                "location": location,
                "profiles": profiles
            },
            "work": [],
            "skills": [],
            "education": [],
            "awards": [],
            "languages": [],
            "interests": []
        }
        
        # Get work experience
        work_entities = Entity.query.options(joinedload(Entity.translations)).filter_by(type='experience').all()
        for entity in work_entities:
            if not entity.meta.get('show_in_cv', True):
                continue
                
            translation = next((t for t in entity.translations if t.lang == lang), None)
            if not translation:
                continue
            
            work_item = {
                "company": entity.meta.get('company', ''),
                "position": translation.title,
                "url": entity.meta.get('company_url', ''),
                "startDate": entity.meta.get('startDate', ''),
                "endDate": entity.meta.get('endDate', ''),
                "summary": translation.summary,
                "highlights": translation.content.get('highlights', []) if translation.content else []
            }
            cv_data["work"].append(work_item)
        
        # Get skills - group by category with levels
        skill_entities = Entity.query.options(joinedload(Entity.translations)).filter_by(type='skill').all()
        skills_by_category = {}
        
        # Level name translations
        level_names = {
            'advanced': 'Avanzado' if lang == 'es' else 'Advanced',
            'intermediate': 'Intermedio' if lang == 'es' else 'Intermediate',
            'beginner': 'Básico' if lang == 'es' else 'Beginner'
        }
        
        for entity in skill_entities:
            if not entity.meta.get('show_in_cv', True):
                continue
                
            translation = next((t for t in entity.translations if t.lang == lang), None)
            if not translation:
                continue
            
            # Group skills by category with level
            category = entity.meta.get('category', 'other')
            if category not in skills_by_category:
                skills_by_category[category] = []
            
            # Format: "Python (Advanced)" or just "Python" if no level
            level = entity.meta.get('level', '')
            level_display = level_names.get(level, level) if level else ''
            skill_display = f"{translation.title} ({level_display})" if level_display else translation.title
            
            skills_by_category[category].append(skill_display)
        
        # Convert to CV format with ATS-optimized categories
        category_names = {
            'languages': 'Lenguajes de Programación' if lang == 'es' else 'Programming Languages',
            'data-engineering': 'Ingeniería de Datos' if lang == 'es' else 'Data Engineering',
            'databases': 'Bases de Datos' if lang == 'es' else 'Databases & Warehouses',
            'cloud': 'Plataformas Cloud' if lang == 'es' else 'Cloud Platforms',
            'devops': 'DevOps & Herramientas' if lang == 'es' else 'DevOps & Tools',
            'visualization': 'Visualización de Datos' if lang == 'es' else 'Data Visualization',
            'other': 'Otras Habilidades' if lang == 'es' else 'Other Skills'
        }
        
        # Order categories for ATS optimization (languages first!)
        category_order = ['languages', 'data-engineering', 'databases', 'cloud', 'devops', 'visualization', 'other']
        
        for category in category_order:
            if category in skills_by_category:
                skill_item = {
                    "name": category_names.get(category, category),
                    "keywords": skills_by_category[category]
                }
                cv_data["skills"].append(skill_item)
        
        # Get education
        edu_entities = Entity.query.options(joinedload(Entity.translations)).filter_by(type='education').all()
        for entity in edu_entities:
            if not entity.meta.get('show_in_cv', True):
                continue
                
            translation = next((t for t in entity.translations if t.lang == lang), None)
            if not translation:
                continue
            
            edu_item = {
                "institution": translation.title,
                "area": translation.summary,
                "studyType": translation.subtitle,
                "startDate": entity.meta.get('startDate', ''),
                "endDate": entity.meta.get('endDate', 'Actualidad' if lang == 'es' else 'Present'),
                "location": entity.meta.get('location', ''),
                "gpa": entity.meta.get('gpa', ''),
                "courses": entity.meta.get('courses', [])
            }
            cv_data["education"].append(edu_item)
        
        # Get certifications as awards
        cert_entities = Entity.query.options(joinedload(Entity.translations)).filter_by(type='certification').all()
        for entity in cert_entities:
            if not entity.meta.get('show_in_cv', True):
                continue
                
            translation = next((t for t in entity.translations if t.lang == lang), None)
            if not translation:
                continue
            
            award_item = {
                "title": translation.title,
                "date": entity.meta.get('issue_date', ''),
                "awarder": translation.subtitle,
                "summary": translation.summary,
                "link": entity.meta.get('credential_url', '')
            }
            cv_data["awards"].append(award_item)
        
        # Static data for now (can be made dynamic later)
        cv_data["languages"] = [
            {"language": "Español" if lang == 'es' else "Spanish", "fluency": "Nativo" if lang == 'es' else "Native"},
            {"language": "Inglés" if lang == 'es' else "English", "fluency": "Fluido" if lang == 'es' else "Fluent"}
        ]
        
        # Only return if we have meaningful content with proper name and summary
        # This ensures we fall back to JSON if database doesn't have proper translations
        has_content = (
            cv_data["basics"]["name"] and 
            cv_data["basics"]["name"] != "" and
            cv_data["basics"]["summary"] and
            len(cv_data["skills"]) > 0
        )
        return cv_data if has_content else None
        
    except Exception as e:
        import logging
        logging.error(f"Failed to build CV from entities: {e}")
        return None


def get_cv_data(lang='es', profile_slug='default'):
    """
    Get CV data with caching.
    Priority: Cache -> Database Entities -> Old CV Model -> JSON file
    """
    # Try cache first
    cached = get_cached_cv(lang, profile_slug)
    if cached:
        return cached
    
    # Try building from entities (new approach)
    cv_data = build_cv_from_entities(lang)
    if cv_data:
        set_cached_cv(lang, cv_data, profile_slug)
        return cv_data
    
    # Try old CV model (if exists)
    cv_data = get_cv_data_from_db(lang, profile_slug)
    if cv_data:
        set_cached_cv(lang, cv_data, profile_slug)
        return cv_data
    
    # Fallback to JSON file
    cv_data = get_cv_data_from_json(lang)
    if cv_data:
        set_cached_cv(lang, cv_data, profile_slug)
    
    return cv_data


@cv_bp.route('/cv', methods=['GET'])
def cv_view():
    """Render CV HTML page"""
    lang = request.args.get('lang', 'es')
    profile_slug = request.args.get('profile', 'default')
    cv_data = get_cv_data(lang, profile_slug)
    
    if not cv_data:
        return "CV data not found", 404
    
    return render_template('cv.html', cv_data=cv_data, lang=lang)


@cv_bp.route('/cv/pdf', methods=['GET'])
def cv_pdf():
    """Generate and download CV PDF"""
    lang = request.args.get('lang', 'es')
    profile_slug = request.args.get('profile', 'default')
    cv_data = get_cv_data(lang, profile_slug)
    
    if not cv_data:
        return jsonify({"error": "CV data not found"}), 404
    
    try:
        pdf_service = PDFService()
        pdf_bytes = pdf_service.generate_cv_pdf(cv_data, lang)
        
        filename = f'CV_Rafael_Ortiz_{lang}.pdf'
        
        return send_file(
            pdf_bytes,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    except RuntimeError as e:
        # PDF library not available (WeasyPrint needs system libraries on Railway)
        return jsonify({
            "error": "PDF generation not available",
            "message": str(e)
        }), 503
    except Exception as e:
        return jsonify({
            "error": "PDF generation failed",
            "message": str(e)
        }), 500
