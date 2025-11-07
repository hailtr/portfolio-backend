"""
Rate Limiting Utilities

Provides access to the limiter instance for decorating routes.
"""

# This will be set by app.py after initialization
limiter = None


def init_limiter(limiter_instance):
    """Initialize the global limiter instance"""
    global limiter
    limiter = limiter_instance


# Common rate limit decorators
def api_rate_limit():
    """Standard rate limit for API endpoints: 100 requests per minute"""
    if limiter:
        return limiter.limit("100 per minute")
    return lambda f: f


def strict_rate_limit():
    """Strict rate limit for expensive operations: 10 requests per minute"""
    if limiter:
        return limiter.limit("10 per minute")
    return lambda f: f


def generous_rate_limit():
    """Generous rate limit for lightweight endpoints: 300 requests per minute"""
    if limiter:
        return limiter.limit("300 per minute")
    return lambda f: f

