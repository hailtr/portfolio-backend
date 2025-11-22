"""
REST API endpoints for portfolio data.

These endpoints serve JSON data to the React frontend.
All endpoints are public (no authentication required for reading).

Features:
- Caching: Responses cached for 5 minutes (configurable per endpoint)
- Rate Limiting: Protects against abuse
- Query Optimization: Eager loading to reduce DB queries
"""

from flask import Blueprint, jsonify, request
from backend.models.entity import Entity
from backend.models.translation import EntityTranslation
from backend import db
from sqlalchemy import desc, or_
from sqlalchemy.orm import joinedload
import json
import os
from backend.services.cache_service import (
    cache_response,
    cache_key_with_lang,
    cache_key_simple,
)
from backend.utils.rate_limit import (
    api_rate_limit,
    generous_rate_limit,
    strict_rate_limit,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health", methods=["GET"])
@generous_rate_limit()  # More generous for health checks
def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        JSON with status and database connectivity
    """
    try:
        # Test database connection
        db.session.execute(db.text("SELECT 1"))
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return (
            jsonify(
                {"status": "unhealthy", "database": "disconnected", "error": str(e)}
            ),
            503,
        )


@api_bp.route("/entities", methods=["GET"])
@api_rate_limit()  # 100 requests per minute
@cache_response(timeout=300, key_func=cache_key_with_lang)  # Cache for 5 minutes
def get_entities():
    """
    Get all entities with translations.

    Query Parameters:
        - lang: Language code (e.g., 'es', 'en'). Defaults to 'es'
        - type: Filter by entity type (e.g., 'project', 'experience')
        - category: Filter by category

    Returns:
        JSON array of entities with translations

    Performance:
        - Cached for 5 minutes
        - Rate limited to 100 req/min
        - Uses eager loading for translations
    """
    lang = request.args.get("lang", "es")
    entity_type = request.args.get("type")
    category = request.args.get("category")

    # Build query with eager loading (reduces N+1 queries)
    query = Entity.query.options(joinedload(Entity.translations))

    if entity_type:
        query = query.filter(Entity.type == entity_type)

    if category:
        query = query.filter(Entity.meta["category"].astext == category)

    # Order by most recent
    query = query.order_by(desc(Entity.created_at))

    entities = query.all()

    result = []
    for entity in entities:
        # Find translation for requested language
        translation = next((t for t in entity.translations if t.lang == lang), None)

        # Fallback to any available translation if requested lang not found
        if not translation and entity.translations:
            translation = entity.translations[0]

        if translation:
            # Extract images from meta
            images = entity.meta.get("images", {}) if entity.meta else {}

            entity_data = {
                "id": entity.id,
                "slug": entity.slug,
                "type": entity.type,
                "category": entity.meta.get("category") if entity.meta else None,
                "tags": entity.meta.get("tags", []) if entity.meta else [],
                "desktop_image": images.get("desktop"),
                "mobile_image": images.get("mobile"),
                "preview_video": images.get("preview_video"),
                "title": translation.title,
                "subtitle": translation.subtitle,
                "description": translation.description,
                "summary": translation.summary,
                "content": translation.content,
                "created_at": (
                    entity.created_at.isoformat() if entity.created_at else None
                ),
                "updated_at": (
                    entity.updated_at.isoformat() if entity.updated_at else None
                ),
                # Additional fields for work experience and education cards
                "company": entity.meta.get("company", "") if entity.meta else "",
                "location": entity.meta.get("location", "") if entity.meta else "",
                "institution": (
                    entity.meta.get("institution", "") if entity.meta else ""
                ),
                "startDate": entity.meta.get("startDate", "") if entity.meta else "",
                "endDate": entity.meta.get("endDate", "") if entity.meta else "",
                "current": entity.meta.get("current", False) if entity.meta else False,
                "courses": entity.meta.get("courses", []) if entity.meta else [],
            }
            result.append(entity_data)

    return jsonify(result), 200


@api_bp.route("/entities/<slug>", methods=["GET"])
@api_rate_limit()  # 100 requests per minute
@cache_response(timeout=300, key_func=cache_key_with_lang)  # Cache for 5 minutes
def get_entity_by_slug(slug):
    """
    Get a single entity by slug with translations.

    Query Parameters:
        - lang: Language code (e.g., 'es', 'en'). Defaults to 'es'

    Returns:
        JSON object with entity data and all available translations

    Performance:
        - Cached for 5 minutes
        - Rate limited to 100 req/min
        - Uses eager loading for translations
    """
    lang = request.args.get("lang", "es")

    # Eager load translations to avoid N+1 queries
    entity = (
        Entity.query.options(joinedload(Entity.translations))
        .filter_by(slug=slug)
        .first()
    )

    if not entity:
        return jsonify({"error": "Entity not found", "slug": slug}), 404

    # Get all translations
    translations_data = {}
    for translation in entity.translations:
        translations_data[translation.lang] = {
            "title": translation.title,
            "subtitle": translation.subtitle,
            "description": translation.description,
            "summary": translation.summary,
            "content": translation.content,
        }

    # Get primary translation for requested language
    primary_translation = translations_data.get(lang)

    # Fallback to first available if requested lang not found
    if not primary_translation and translations_data:
        primary_translation = next(iter(translations_data.values()))

    # Extract images from meta
    images = entity.meta.get("images", {}) if entity.meta else {}

    result = {
        "id": entity.id,
        "slug": entity.slug,
        "type": entity.type,
        "category": entity.meta.get("category") if entity.meta else None,
        "tags": entity.meta.get("tags", []) if entity.meta else [],
        "desktop_image": images.get("desktop"),
        "mobile_image": images.get("mobile"),
        "preview_video": images.get("preview_video"),
        "created_at": entity.created_at.isoformat() if entity.created_at else None,
        "updated_at": entity.updated_at.isoformat() if entity.updated_at else None,
        "translations": translations_data,
        "current": primary_translation,
    }

    return jsonify(result), 200


@api_bp.route("/languages", methods=["GET"])
@generous_rate_limit()  # 300 requests per minute (lightweight endpoint)
@cache_response(timeout=600, key_func=cache_key_simple)  # Cache for 10 minutes
def get_available_languages():
    """
    Get list of available languages in the system.

    Returns:
        JSON array of language codes

    Performance:
        - Cached for 10 minutes (changes infrequently)
        - Rate limited to 300 req/min
    """
    # Query distinct languages from translations
    languages = db.session.query(EntityTranslation.lang).distinct().all()
    lang_codes = [lang[0] for lang in languages]

    return jsonify({"languages": lang_codes, "count": len(lang_codes)}), 200


@api_bp.route("/categories", methods=["GET"])
@generous_rate_limit()  # 300 requests per minute (lightweight endpoint)
@cache_response(timeout=600, key_func=cache_key_with_lang)  # Cache for 10 minutes
def get_categories():
    """
    Get list of all categories used in entities.

    Query Parameters:
        - type: Filter categories by entity type

    Returns:
        JSON array of unique categories

    Performance:
        - Cached for 10 minutes (changes infrequently)
        - Rate limited to 300 req/min
    """
    entity_type = request.args.get("type")

    query = Entity.query
    if entity_type:
        query = query.filter(Entity.type == entity_type)

    entities = query.all()

    # Extract unique categories
    categories = set()
    for entity in entities:
        if entity.meta and "category" in entity.meta:
            categories.add(entity.meta["category"])

    return (
        jsonify({"categories": sorted(list(categories)), "count": len(categories)}),
        200,
    )


@api_bp.route("/tags", methods=["GET"])
@generous_rate_limit()  # 300 requests per minute (lightweight endpoint)
@cache_response(timeout=600, key_func=cache_key_simple)  # Cache for 10 minutes
def get_tags():
    """
    Get list of all tags used in entities.

    Returns:
        JSON array of unique tags with usage count

    Performance:
        - Cached for 10 minutes (changes infrequently)
        - Rate limited to 300 req/min
    """
    entities = Entity.query.all()

    # Count tag occurrences
    tag_counts = {}
    for entity in entities:
        if entity.meta and "tags" in entity.meta:
            for tag in entity.meta["tags"]:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

    # Sort by count (descending)
    sorted_tags = sorted(
        [{"tag": tag, "count": count} for tag, count in tag_counts.items()],
        key=lambda x: x["count"],
        reverse=True,
    )

    return jsonify({"tags": sorted_tags, "total": len(sorted_tags)}), 200


@api_bp.route("/profile", methods=["GET"])
@generous_rate_limit()  # 300 requests per minute (lightweight endpoint)
@cache_response(timeout=600, key_func=cache_key_with_lang)  # Cache for 10 minutes
def get_profile():
    """
    Get profile/hero information for frontend.

    Query Parameters:
        - lang: Language code (e.g., 'es', 'en'). Defaults to 'es'

    Returns:
        JSON object with profile data (name, role, tagline, location, social links)

    Performance:
        - Cached for 10 minutes
        - Rate limited to 300 req/min
    """
    lang = request.args.get("lang", "es")

    # Get profile entity
    profile_entity = (
        Entity.query.options(joinedload(Entity.translations))
        .filter_by(type="profile", slug="rafael-ortiz-profile")
        .first()
    )

    if not profile_entity:
        return jsonify({"error": "Profile not found"}), 404

    # Get translation
    translation = next((t for t in profile_entity.translations if t.lang == lang), None)
    if not translation and profile_entity.translations:
        translation = profile_entity.translations[0]

    if not translation:
        return jsonify({"error": "Profile translation not found"}), 404

    # Build response
    # Mapping: title=role, subtitle=tagline, summary=CV summary (not sent to hero)
    profile_data = {
        "name": (
            profile_entity.meta.get("name", "Rafael Ortiz")
            if profile_entity.meta
            else "Rafael Ortiz"
        ),
        "role": translation.title,  # "Data Engineer"
        "tagline": translation.subtitle,  # Short one-liner
        "location": (
            profile_entity.meta.get("location", {}) if profile_entity.meta else {}
        ),
        "email": profile_entity.meta.get("email", "") if profile_entity.meta else "",
        "phone": profile_entity.meta.get("phone", "") if profile_entity.meta else "",
        "social": profile_entity.meta.get("social", {}) if profile_entity.meta else {},
    }

    return jsonify(profile_data), 200


@api_bp.route("/cv", methods=["GET"])
@api_rate_limit()  # 100 requests per minute
@cache_response(timeout=600, key_func=cache_key_with_lang)  # Cache for 10 minutes
def get_cv():
    """
    Get CV/Resume data.

    Query Parameters:
        - lang: Language code (e.g., 'es', 'en'). Defaults to 'es'

    Returns:
        JSON object with CV data in JSON Resume format

    Performance:
        - Cached for 10 minutes (changes infrequently)
        - Rate limited to 100 req/min
    """
    lang = request.args.get("lang", "es")

    # Load resume.json from backend/data folder
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "resume.json"
    )

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            resume_data = json.load(f)

        # Return the requested language version
        if lang in resume_data:
            return jsonify(resume_data[lang]), 200
        else:
            # Fallback to 'es' if requested language not found
            return jsonify(resume_data.get("es", {})), 200

    except FileNotFoundError:
        return (
            jsonify(
                {
                    "error": "CV data not found",
                    "message": "resume.json file not found in backend/data folder",
                }
            ),
            404,
        )
    except json.JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Server error", "message": str(e)}), 500


# Error handlers for API blueprint
@api_bp.errorhandler(404)
def api_not_found(error):
    return jsonify({"error": "Not found", "message": str(error)}), 404


@api_bp.errorhandler(500)
def api_server_error(error):
    return jsonify({"error": "Internal server error", "message": str(error)}), 500
