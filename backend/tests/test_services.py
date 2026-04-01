"""Tests for service layer utilities."""
import json


def test_cache_key_with_lang(app):
    """Test language-aware cache key generation."""
    from backend.services.cache_service import cache_key_with_lang

    with app.test_request_context("/api/projects?lang=en&category=work"):
        key = cache_key_with_lang()
        assert "en" in key
        assert "/api/projects" in key
        assert "work" in key


def test_cache_key_simple(app):
    """Test simple cache key generation."""
    from backend.services.cache_service import cache_key_simple

    with app.test_request_context("/api/health"):
        key = cache_key_simple()
        assert key == "/api/health"


def test_cv_cache_hash(app):
    """Test CV data hash generation for cache invalidation."""
    from backend.services.cv_cache import get_cv_data_hash

    data1 = {"basics": {"name": "Test"}, "work": []}
    data2 = {"basics": {"name": "Test"}, "work": []}
    data3 = {"basics": {"name": "Changed"}, "work": []}

    hash1 = get_cv_data_hash(data1)
    hash2 = get_cv_data_hash(data2)
    hash3 = get_cv_data_hash(data3)

    assert hash1 == hash2  # Same data = same hash
    assert hash1 != hash3  # Different data = different hash


def test_cv_cache_set_get(app):
    """Test CV cache set and get operations."""
    from backend.services.cv_cache import (
        get_cached_cv, set_cached_cv, invalidate_all_cv_cache
    )

    with app.app_context():
        invalidate_all_cv_cache()

        cv_data = {"basics": {"name": "Test"}}
        set_cached_cv("en", cv_data)
        cached = get_cached_cv("en")
        assert cached == cv_data

        # Different lang should miss
        assert get_cached_cv("es") is None


def test_cv_pdf_cache(app):
    """Test PDF cache set and get operations."""
    from backend.services.cv_cache import (
        get_cached_pdf, set_cached_pdf, invalidate_all_cv_cache
    )

    with app.app_context():
        invalidate_all_cv_cache()

        cv_data = {"basics": {"name": "Test"}}
        pdf_bytes = b"%PDF-1.4 fake content"

        set_cached_pdf("en", cv_data, pdf_bytes)
        cached, hit = get_cached_pdf("en", cv_data)
        assert hit is True
        assert cached == pdf_bytes

        # Different data should miss
        different_data = {"basics": {"name": "Changed"}}
        cached2, hit2 = get_cached_pdf("en", different_data)
        assert hit2 is False


def test_cv_cache_invalidation(app):
    """Test cache invalidation clears all entries."""
    from backend.services.cv_cache import (
        set_cached_cv, get_cached_cv, invalidate_all_cv_cache
    )

    with app.app_context():
        set_cached_cv("en", {"test": True})
        set_cached_cv("es", {"test": True})

        invalidate_all_cv_cache()

        assert get_cached_cv("en") is None
        assert get_cached_cv("es") is None


def test_cache_stats(app):
    """Test cache statistics reporting."""
    from backend.services.cv_cache import (
        get_cache_stats, set_cached_cv, invalidate_all_cv_cache
    )

    with app.app_context():
        invalidate_all_cv_cache()
        stats = get_cache_stats()
        assert stats["cv_data_entries"] == 0
        assert stats["pdf_entries"] == 0

        set_cached_cv("en", {"test": True})
        stats = get_cache_stats()
        assert stats["cv_data_entries"] == 1


def test_check_cache_health(app):
    """Test cache health check."""
    from backend.services.cache_service import check_cache_health

    with app.app_context():
        result = check_cache_health()
        assert result is True
