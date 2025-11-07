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


def get_cv_data(lang='es', profile_slug='default'):
    """
    Get CV data with caching.
    Priority: Cache -> Database -> JSON file
    """
    # Try cache first
    cached = get_cached_cv(lang, profile_slug)
    if cached:
        return cached
    
    # Try database
    cv_data = get_cv_data_from_db(lang, profile_slug)
    if cv_data:
        set_cached_cv(lang, cv_data, profile_slug)
        return cv_data
    
    # Fallback to JSON
    cv_data = get_cv_data_from_json(lang)
    if cv_data:
        # Cache JSON data too (shorter TTL could be set)
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
