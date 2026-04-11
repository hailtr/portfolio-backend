"""
CV routes for displaying and generating PDF resumes.
"""

import json
import io
import os
import traceback
import re

from flask import Blueprint, render_template, request, send_file, jsonify, current_app
from backend import db
from backend.models.profile import Profile
from backend.models.experience import Experience
from backend.models.education import Education
from backend.models.skill import Skill, SkillCategory
from backend.models.certification import Certification
from backend.services.pdf_service import PDFService
from sqlalchemy import desc

cv_bp = Blueprint("cv", __name__)


def _inject_css_into_html(html_content, css_path):
    """Inject CSS file contents into HTML, replacing the link tag."""
    if not os.path.exists(css_path):
        return html_content

    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()

    font_import = "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');\n"
    css_content = font_import + css_content

    result = re.sub(
        r'<link[^>]*href="[^"]*cv\.css"[^>]*>',
        f'<style>{css_content}</style>',
        html_content
    )
    if '<style>' not in result:
        result = result.replace('</head>', f'<style>{css_content}</style></head>')

    return result


@cv_bp.route('/cv/guide')
def cv_guide():
    """Render the static CV guide with placeholder content."""
    return render_template('cv_guide.html')


@cv_bp.route('/cv/guide/pdf')
def cv_guide_pdf():
    """Generate PDF for the CV guide."""
    try:
        html_content = render_template('cv_guide.html')
        css_path = os.path.join(current_app.static_folder, 'styles', 'cv.css')
        html_content = _inject_css_into_html(html_content, css_path)

        from weasyprint import HTML
        pdf_bytes = HTML(string=html_content, base_url=request.url_root).write_pdf()

        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='CV_Guide_Template.pdf'
        )
    except Exception as e:
        current_app.logger.error(f"CV guide PDF error: {traceback.format_exc()}")
        return jsonify({"error": "PDF generation failed"}), 500


def format_date(date_obj, lang="es"):
    """Format date based on language"""
    if not date_obj:
        return ""

    if lang == "es":
        return date_obj.strftime("%m/%Y")
    else:
        return date_obj.strftime("%b %Y")


def build_cv_from_models(lang="es"):
    """Build JSON Resume format from database models"""
    from sqlalchemy.orm import joinedload

    current_app.logger.info(f"Building CV for language: {lang}")
    try:
        # 1. Fetch Profile
        profile = Profile.query.options(joinedload(Profile.translations)).first()
        if not profile:
            return None

        p_trans = next((t for t in profile.translations if t.lang == lang), None)
        if not p_trans and profile.translations:
            p_trans = profile.translations[0]

        # Parse location and social links
        location_data = profile.location if isinstance(profile.location, dict) else {}
        if isinstance(profile.location, str):
            try:
                location_data = json.loads(profile.location)
            except (json.JSONDecodeError, ValueError):
                location_data = {}

        social_data = profile.social_links if isinstance(profile.social_links, dict) else {}
        if isinstance(profile.social_links, str):
            try:
                social_data = json.loads(profile.social_links)
            except (json.JSONDecodeError, ValueError):
                social_data = {}

        profiles_list = []
        for network, url in social_data.items():
            if url:
                display_url = url.replace("https://", "").replace("http://", "").replace("www.", "")
                if display_url.endswith("/"):
                    display_url = display_url[:-1]

                profiles_list.append({
                    "network": network.capitalize(),
                    "username": display_url,
                    "url": url
                })

        summary = ""
        if p_trans:
            summary = p_trans.bio or p_trans.tagline or ""

        cv_data = {
            "basics": {
                "name": profile.name,
                "label": p_trans.role if p_trans else "",
                "email": profile.email or "",
                "phone": location_data.get("phone", ""),
                "summary": summary,
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
            "certifications": [],
            "languages": [],
        }

        # 2. Fetch Experience
        experiences = Experience.query.options(
            joinedload(Experience.translations),
            joinedload(Experience.tags),
        ).order_by(desc(Experience.start_date)).all()
        for exp in experiences:
            trans = next((t for t in exp.translations if t.lang == lang), None)
            if not trans: continue

            summary = ""
            highlights = []

            if trans.description:
                lines = trans.description.strip().split('\n')
                summary_lines = []

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith(('-', '*', '•', '·')):
                        highlights.append(line.lstrip('-*•· ').strip())
                    else:
                        if not highlights:
                            summary_lines.append(line)
                        else:
                            highlights.append(line)

                summary = ' '.join(summary_lines)

            end_date_display = ("Presente" if lang == "es" else "Present") if exp.current else format_date(exp.end_date, lang)

            tag_names = sorted([t.name for t in exp.tags]) if exp.tags else []

            cv_data["work"].append({
                "company": trans.title,
                "position": trans.subtitle,
                "startDate": format_date(exp.start_date, lang),
                "endDate": end_date_display,
                "location": exp.location,
                "summary": summary,
                "highlights": highlights,
                "tags": tag_names,
            })

        # 3. Fetch Education
        educations = Education.query.options(
            joinedload(Education.translations),
            joinedload(Education.courses)
        ).order_by(desc(Education.start_date)).all()
        for edu in educations:
            trans = next((t for t in edu.translations if t.lang == lang), None)
            if not trans: continue

            course_names = [course.name for course in sorted(edu.courses, key=lambda c: c.order)] if edu.courses else []

            if edu.current and edu.end_date:
                year = edu.end_date.strftime("%Y")
                end_date_display = f"Graduación Esperada {year}" if lang == "es" else f"Expected Graduation {year}"
            elif edu.current:
                end_date_display = "En Curso" if lang == "es" else "In Progress"
            else:
                end_date_display = format_date(edu.end_date, lang)

            cv_data["education"].append({
                "institution": edu.institution,
                "area": trans.subtitle,
                "studyType": trans.title,
                "startDate": format_date(edu.start_date, lang),
                "endDate": end_date_display,
                "location": edu.location,
                "courses": course_names
            })

        # 4. Fetch Skills
        skills = Skill.query.filter_by(is_visible_cv=True).options(
            joinedload(Skill.translations),
            joinedload(Skill.skill_category).joinedload(SkillCategory.translations)
        ).order_by(Skill.order).all()

        skills_by_category = {}

        for skill in skills:
            trans = next((t for t in skill.translations if t.lang == lang), None)
            name = trans.name if trans else skill.slug
            description = trans.description if trans else ""

            if skill.skill_category:
                cat_obj = skill.skill_category
                cat_trans = next((t for t in cat_obj.translations if t.lang == lang), None)
                cat_name = cat_trans.name if cat_trans else cat_obj.slug
                cat_slug = cat_obj.slug
                cat_order = cat_obj.order
            else:
                cat_name = "Other" if lang == "en" else "Otros"
                cat_slug = "other"
                cat_order = 999

            if cat_name not in skills_by_category:
                skills_by_category[cat_name] = {
                    "keywords": [], "entries": [],
                    "order": cat_order, "slug": cat_slug
                }

            skills_by_category[cat_name]["keywords"].append(name)
            skills_by_category[cat_name]["entries"].append({
                "name": name, "description": description,
                "proficiency": skill.proficiency or 50
            })

        sorted_categories = sorted(skills_by_category.items(), key=lambda x: x[1]["order"])

        SPOKEN_LANG_SLUGS = {"spoken-languages", "idiomas"}
        for cat_name, data in sorted_categories:
            if cat_name in ["Other", "Otros"]:
                continue

            if data.get("slug") in SPOKEN_LANG_SLUGS:
                for entry in data["entries"]:
                    cv_data["languages"].append({
                        "language": entry["name"],
                        "fluency": entry["description"] or ""
                    })
            else:
                cv_data["skills"].append({
                    "name": cat_name,
                    "keywords": data["keywords"],
                    "skill_items": [{"name": e["name"], "proficiency": e["proficiency"]}
                                    for e in data["entries"]]
                })

        # Fallback if no languages category exists in DB
        if not cv_data["languages"]:
            cv_data["languages"] = [
                {"language": "Español" if lang == "es" else "Spanish",
                 "fluency": "Nativo" if lang == "es" else "Native"},
                {"language": "Inglés" if lang == "es" else "English",
                 "fluency": "Fluido" if lang == "es" else "Fluent"}
            ]

        # 5. Fetch Certifications
        certs = Certification.query.options(joinedload(Certification.translations)).order_by(desc(Certification.issue_date)).all()
        for cert in certs:
            trans = next((t for t in cert.translations if t.lang == lang), None)
            if not trans: continue

            cv_data["certifications"].append({
                "title": trans.title,
                "date": format_date(cert.issue_date, lang),
                "awarder": cert.issuer,
                "summary": trans.description,
                "link": cert.credential_url
            })

        return cv_data

    except Exception as e:
        current_app.logger.error(f"Error building CV: {e}")
        current_app.logger.error(traceback.format_exc())
        raise


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

        from flask import make_response
        resp = make_response(render_template("cv.html", cv_data=cv_data, lang=lang))
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        resp.headers["Pragma"] = "no-cache"
        resp.headers["Expires"] = "0"
        return resp
    except Exception as e:
        current_app.logger.error(f"CV view error: {traceback.format_exc()}")
        return render_template("error.html", error="Error generating CV"), 500


@cv_bp.route("/cv/pdf", methods=["GET"])
def cv_pdf():
    """Generate and download CV PDF with caching"""
    try:
        from backend.services.cv_cache import get_cached_pdf, set_cached_pdf
        from io import BytesIO

        lang = request.args.get("lang", "es")
        preview = request.args.get("preview", "0") == "1"
        cv_data = build_cv_from_models(lang)

        if not cv_data:
            return jsonify({"error": "CV data not found"}), 404

        # Derive filename from profile name
        name_slug = cv_data["basics"]["name"].replace(" ", "_")
        filename = f"CV_{name_slug}_{lang}.pdf"

        # Check cache first
        cached_pdf, cache_hit = get_cached_pdf(lang, cv_data)
        if cache_hit and cached_pdf:
            current_app.logger.info(f"PDF cache HIT for lang={lang}")
            return send_file(
                BytesIO(cached_pdf),
                mimetype="application/pdf",
                as_attachment=not preview,
                download_name=filename,
            )

        # Cache miss - generate PDF
        current_app.logger.info(f"PDF cache MISS for lang={lang}, generating...")
        pdf_service = PDFService()
        pdf_bytes = pdf_service.generate_cv_pdf(cv_data, lang)

        set_cached_pdf(lang, cv_data, pdf_bytes)
        current_app.logger.info(f"PDF cached for lang={lang}")

        return send_file(
            pdf_bytes,
            mimetype="application/pdf",
            as_attachment=not preview,
            download_name=filename,
        )
    except Exception as e:
        current_app.logger.error(f"PDF generation error: {traceback.format_exc()}")
        return render_template("error.html"), 500


@cv_bp.route("/cv/clear-cache", methods=["POST"])
def clear_cv_cache():
    """Manually clear CV data and PDF caches"""
    try:
        from backend.services.cv_cache import invalidate_all_cv_cache, get_cache_stats

        stats_before = get_cache_stats()
        invalidate_all_cv_cache()
        stats_after = get_cache_stats()

        return jsonify({
            "success": True,
            "message": "CV and PDF caches cleared",
            "before": stats_before,
            "after": stats_after
        })
    except Exception as e:
        current_app.logger.error(f"Cache clear failed: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500
