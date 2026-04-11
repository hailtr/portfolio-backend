"""Dump US Retail experience translations to confirm preamble insertion point."""
from backend.app import app
from backend.models.experience import Experience


with app.app_context():
    exp = Experience.query.filter_by(slug="us-retail-data-architect-contract").first()
    if not exp:
        print("NOT FOUND")
        for e in Experience.query.all():
            print(f"  slug={e.slug}")
    else:
        print(f"slug={exp.slug}")
        print(f"company={exp.company}")
        for t in exp.translations:
            print(f"\n--- lang={t.lang} ---")
            print(f"title={t.title!r}")
            print("description:")
            print(t.description)
            print("---END---")
