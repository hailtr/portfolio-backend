"""Remove the UC Chile Coordinator Assistant experience — doesn't fit the senior data narrative."""
from backend.app import app
from backend import db
from backend.models.experience import Experience


with app.app_context():
    exp = Experience.query.filter_by(slug="uc-chile-coordinator").first()
    if not exp:
        exp = Experience.query.filter(Experience.slug.like("uc-chile%")).first()
    if not exp:
        print("ERROR: UC Chile experience not found (already deleted?)")
        raise SystemExit(1)

    print(f"DELETING: slug={exp.slug}, company={exp.company}, "
          f"dates={exp.start_date}..{exp.end_date}")
    print(f"Translations to be cascade-deleted: {len(exp.translations)}")

    db.session.delete(exp)
    db.session.commit()

    print("DELETED")

    # Verify
    remaining = Experience.query.order_by(Experience.start_date.desc()).all()
    print(f"\nRemaining experiences: {len(remaining)}")
    for e in remaining:
        print(f"  - {e.slug} ({e.start_date}..{e.end_date})")

    # Invalidate CV caches
    try:
        from backend.services.cv_cache import invalidate_all_cv_cache
        invalidate_all_cv_cache()
        print("\nCV caches invalidated")
    except Exception as e:
        print(f"(cache invalidation skipped: {e})")
