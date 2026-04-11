"""Bust CV caches after template/CSS or content changes."""
from backend.app import app
from backend.services.cv_cache import invalidate_all_cv_cache, get_cache_stats

with app.app_context():
    before = get_cache_stats()
    invalidate_all_cv_cache()
    after = get_cache_stats()
    print(f"before: {before}")
    print(f"after:  {after}")
