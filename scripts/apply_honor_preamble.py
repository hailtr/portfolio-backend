"""Prepend a verb-based leadership preamble to the HONOR experience.

At HONOR (Solutions Engineer, full-time) Rafael owned the entire
Excel-to-Fabric migration end-to-end: lakehouse architecture, Power BI
semantic model with RLS, AND built the supporting Flask operational app
from scratch. Current bullets describe the WORK but don't signal the
OWNERSHIP. Fix: add a one-line preamble that hits "Led" and "owned"
keywords without claiming a formal title (his title was Solutions
Engineer, not Lead).
"""
from backend.app import app
from backend import db
from backend.models.experience import Experience


HONOR_SLUG = "honor-solutions-engineer"

PREAMBLE = {
    "en": (
        "Led the Excel-to-Fabric migration for 1,200+ stores end-to-end "
        "\u2014 owned the lakehouse architecture, the Power BI semantic "
        "model with Row-Level Security, and built the supporting Flask "
        "operational app from scratch."
    ),
    "es": (
        "Lider\u00e9 de extremo a extremo la migraci\u00f3n Excel \u2192 "
        "Fabric para m\u00e1s de 1.200 tiendas \u2014 arquitectura del "
        "lakehouse, modelo sem\u00e1ntico de Power BI con Row-Level Security, "
        "y constru\u00ed desde cero la app operacional en Flask que la soporta."
    ),
}

MARKERS = {
    "en": "Led the Excel-to-Fabric migration for 1,200+ stores end-to-end",
    "es": "Lider\u00e9 de extremo a extremo la migraci\u00f3n Excel",
}


with app.app_context():
    print("=" * 80)
    print("HONOR \u2014 leadership preamble")
    print("=" * 80)
    honor = Experience.query.filter_by(slug=HONOR_SLUG).first()
    if not honor:
        print(f"  SKIP: {HONOR_SLUG} not found")
    else:
        for tr in honor.translations:
            marker = MARKERS[tr.lang]
            if marker in (tr.description or ""):
                print(f"  [{tr.lang}] preamble already present \u2014 skipping")
                continue
            preamble = PREAMBLE[tr.lang]
            tr.description = f"{preamble}\n\n{tr.description or ''}".rstrip() + "\n"
            print(f"  [{tr.lang}] PREPENDED preamble")
            print(f"    {preamble[:120]}...")

    db.session.commit()

    print("\n" + "=" * 80)
    print("VERIFY")
    print("=" * 80)
    honor = Experience.query.filter_by(slug=HONOR_SLUG).first()
    for tr in honor.translations:
        first_line = (tr.description or "").strip().split("\n", 1)[0]
        print(f"  HONOR [{tr.lang}]: {first_line[:140]}")

    try:
        from backend.services.cv_cache import invalidate_all_cv_cache
        invalidate_all_cv_cache()
        print("\n  CV caches invalidated")
    except Exception as e:
        print(f"\n  (cache invalidation skipped: {e})")
