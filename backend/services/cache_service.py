"""
Enhanced Cache Service

Supports both Redis (production) and in-memory (development/fallback).
Automatically falls back to in-memory if Redis is unavailable.
"""

import os
import logging
from functools import wraps
from flask_caching import Cache

logger = logging.getLogger(__name__)

# Cache configuration based on environment
REDIS_URL = os.getenv('REDIS_URL')

if REDIS_URL:
    # Production: Use Redis
    cache_config = {
        'CACHE_TYPE': 'RedisCache',
        'CACHE_REDIS_URL': REDIS_URL,
        'CACHE_DEFAULT_TIMEOUT': 300,  # 5 minutes default
        'CACHE_KEY_PREFIX': 'portfolio:',
    }
    logger.info("Cache configured with Redis")
else:
    # Development: Use simple in-memory cache
    cache_config = {
        'CACHE_TYPE': 'SimpleCache',
        'CACHE_DEFAULT_TIMEOUT': 300,  # 5 minutes default
    }
    logger.info("Cache configured with SimpleCache (in-memory)")

# Initialize cache instance (will be initialized with app later)
cache = Cache(config=cache_config)


def cache_key_with_lang(*args, **kwargs):
    """
    Generate cache key that includes language parameter.
    Use this for endpoints that support multiple languages.
    """
    from flask import request
    lang = request.args.get('lang', 'es')
    entity_type = request.args.get('type', 'all')
    category = request.args.get('category', 'all')
    return f"{request.path}:{lang}:{entity_type}:{category}"


def cache_key_simple():
    """
    Simple cache key based on request path only.
    Use for endpoints that don't have query parameters.
    """
    from flask import request
    return request.path


def invalidate_entities_cache():
    """
    Invalidate all entity-related cache entries.
    Call this when entities are created/updated/deleted.
    """
    try:
        # Delete all keys with 'entities' pattern
        if REDIS_URL:
            # Redis-specific invalidation
            import redis
            r = redis.from_url(REDIS_URL)
            keys = r.keys('portfolio:*/api/entities*')
            if keys:
                r.delete(*keys)
                logger.info(f"Invalidated {len(keys)} entity cache keys")
        else:
            # SimpleCache doesn't support pattern deletion, clear all
            cache.clear()
            logger.info("Cleared all cache (SimpleCache)")
    except Exception as e:
        logger.error(f"Failed to invalidate cache: {e}")


def cache_response(timeout=300, key_func=None):
    """
    Decorator to cache API responses.
    
    Args:
        timeout: Cache timeout in seconds (default 5 minutes)
        key_func: Function to generate cache key (default: uses full URL with query params)
    
    Usage:
        @cache_response(timeout=600, key_func=cache_key_with_lang)
        def get_entities():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                from flask import request
                cache_key = request.full_path
            
            # Try to get from cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                logger.debug(f"Cache HIT: {cache_key}")
                return cached_response
            
            # Cache miss, execute function
            logger.debug(f"Cache MISS: {cache_key}")
            response = f(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, response, timeout=timeout)
            
            return response
        return decorated_function
    return decorator


# Health check for cache
def check_cache_health():
    """Check if cache is working properly"""
    try:
        cache.set('health_check', 'ok', timeout=10)
        result = cache.get('health_check')
        return result == 'ok'
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        return False

