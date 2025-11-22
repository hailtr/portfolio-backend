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
