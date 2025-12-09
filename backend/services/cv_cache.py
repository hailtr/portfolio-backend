"""
CV Cache Service

Implements caching for CV data to reduce database queries.
Uses in-memory cache (can be upgraded to Redis later).
"""

from functools import wraps
import json
import hashlib
from datetime import datetime, timedelta

# Simple in-memory cache
# In production, replace with Redis
_cache = {}
_cache_ttl = timedelta(hours=1)  # Cache for 1 hour

# PDF cache with longer TTL (PDFs are expensive to generate)
_pdf_cache = {}
_pdf_cache_ttl = timedelta(hours=24)  # Cache PDFs for 24 hours


def get_cache_key(lang, profile_slug="default"):
    """Generate cache key"""
    return f"cv:{profile_slug}:{lang}"


def get_cached_cv(lang, profile_slug="default"):
    """Get CV from cache"""
    key = get_cache_key(lang, profile_slug)
    if key in _cache:
        data, timestamp = _cache[key]
        if datetime.now() - timestamp < _cache_ttl:
            return data
        else:
            # Expired, remove from cache
            del _cache[key]
    return None


def set_cached_cv(lang, cv_data, profile_slug="default"):
    """Store CV in cache"""
    key = get_cache_key(lang, profile_slug)
    _cache[key] = (cv_data, datetime.now())


def invalidate_cv_cache(profile_slug="default"):
    """Invalidate all cached CVs for a profile"""
    keys_to_remove = [k for k in _cache.keys() if k.startswith(f"cv:{profile_slug}:")]
    for key in keys_to_remove:
        del _cache[key]


def cv_cache(profile_slug="default"):
    """Decorator to cache CV data"""

    def decorator(func):
        @wraps(func)
        def wrapper(lang, *args, **kwargs):
            # Try cache first
            cached = get_cached_cv(lang, profile_slug)
            if cached is not None:
                return cached

            # Get from database
            cv_data = func(lang, *args, **kwargs)

            # Store in cache
            if cv_data:
                set_cached_cv(lang, cv_data, profile_slug)

            return cv_data

        return wrapper

    return decorator


# ============================================
# PDF Caching Functions
# ============================================

def get_cv_data_hash(cv_data):
    """
    Generate a hash of CV data to detect changes.
    When data changes, the hash changes, invalidating the cached PDF.
    """
    # Convert to JSON string and hash it
    data_str = json.dumps(cv_data, sort_keys=True, default=str)
    return hashlib.md5(data_str.encode()).hexdigest()


def get_pdf_cache_key(lang, data_hash):
    """Generate cache key for PDF"""
    return f"cv_pdf:{lang}:{data_hash}"


def get_cached_pdf(lang, cv_data):
    """
    Get cached PDF bytes if available and CV data hasn't changed.
    
    Returns:
        tuple: (pdf_bytes, cache_hit) - pdf_bytes is None if cache miss
    """
    data_hash = get_cv_data_hash(cv_data)
    key = get_pdf_cache_key(lang, data_hash)
    
    if key in _pdf_cache:
        pdf_bytes, timestamp = _pdf_cache[key]
        if datetime.now() - timestamp < _pdf_cache_ttl:
            return pdf_bytes, True
        else:
            # Expired, remove from cache
            del _pdf_cache[key]
    
    return None, False


def set_cached_pdf(lang, cv_data, pdf_bytes):
    """
    Store generated PDF in cache.
    
    Args:
        lang: Language code
        cv_data: The CV data dict (used to generate hash key)
        pdf_bytes: The PDF bytes to cache
    """
    data_hash = get_cv_data_hash(cv_data)
    key = get_pdf_cache_key(lang, data_hash)
    
    # Store the bytes value, not the BytesIO object
    if hasattr(pdf_bytes, 'getvalue'):
        pdf_bytes = pdf_bytes.getvalue()
    
    _pdf_cache[key] = (pdf_bytes, datetime.now())


def invalidate_pdf_cache():
    """Invalidate all cached PDFs"""
    global _pdf_cache
    _pdf_cache = {}


def invalidate_all_cv_cache():
    """Invalidate both CV data cache and PDF cache"""
    global _cache, _pdf_cache
    _cache = {}
    _pdf_cache = {}


def get_cache_stats():
    """Get cache statistics for monitoring"""
    return {
        "cv_data_entries": len(_cache),
        "pdf_entries": len(_pdf_cache),
        "cv_data_ttl_hours": _cache_ttl.total_seconds() / 3600,
        "pdf_ttl_hours": _pdf_cache_ttl.total_seconds() / 3600,
    }

