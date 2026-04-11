"""Apply two CV updates:

1. US Retail — prepend a leadership preamble before the existing bullets so the
   role reads "Led architecture decisions... and mentored the Workato team"
   instead of a flat contributor summary. No formal title claim — verb-based.

2. Profile phone — fix country code from 0424-2700455 to +58424-2700455.
"""
from sqlalchemy.orm.attributes import flag_modified

from backend.app import app
from backend import db
from backend.models.experience import Experience
from backend.models.profile import Profile


# ============================================================
# 1. US Retail — leadership preamble
# ============================================================
US_RETAIL_SLUG = "us-retail-data-architect-contract"

PREAMBLE = {
    "en": (
        "Led architecture decisions across the full rebuild — Snowflake "
        "\u2192 ClickHouse, Workato \u2192 Airflow — and mentored the "
        "client's existing Workato team through the Airflow transition."
    ),
    "es": (
        "Lider\u00e9 las decisiones de arquitectura del rebuild completo — "
        "Snowflake \u2192 ClickHouse, Workato \u2192 Airflow — y mentoric\u00e9 "
        "al equipo Workato existente del cliente durante la transici\u00f3n a "
        "Airflow."
    ),
}

# Fragments that indicate the preamble is already applied (idempotency)
PREAMBLE_MARKERS = {
    "en": "Led architecture decisions across the full rebuild",
    "es": "Lider\u00e9 las decisiones de arquitectura del rebuild completo",
}


# ============================================================
# 2. Profile phone — country code fix
# ============================================================
OLD_PHONE = "0424-2700455"
NEW_PHONE = "+58424-2700455"


with app.app_context():
    # --------------------------------------------------------
    # 1. US Retail leadership preamble
    # --------------------------------------------------------
    print("=" * 80)
    print("1. US Retail \u2014 leadership preamble")
    print("=" * 80)
    us = Experience.query.filter_by(slug=US_RETAIL_SLUG).first()
    if not us:
        print(f"  SKIP: {US_RETAIL_SLUG} not found")
    else:
        for tr in us.translations:
            marker = PREAMBLE_MARKERS[tr.lang]
            if marker in (tr.description or ""):
                print(f"  [{tr.lang}] preamble already present \u2014 skipping")
                continue
            preamble = PREAMBLE[tr.lang]
            tr.description = f"{preamble}\n\n{tr.description or ''}".rstrip() + "\n"
            print(f"  [{tr.lang}] PREPENDED preamble")
            print(f"    {preamble[:100]}...")

    # --------------------------------------------------------
    # 2. Profile phone country code
    # --------------------------------------------------------
    print("\n" + "=" * 80)
    print("2. Profile phone \u2014 country code fix")
    print("=" * 80)
    p = Profile.query.first()
    if not p:
        print("  SKIP: no profile found")
    else:
        loc = dict(p.location or {})
        current_phone = loc.get("phone", "")
        print(f"  BEFORE: phone={current_phone!r}")
        if current_phone == NEW_PHONE:
            print("  already correct \u2014 skipping")
        elif current_phone == OLD_PHONE:
            loc["phone"] = NEW_PHONE
            p.location = loc
            flag_modified(p, "location")
            print(f"  AFTER:  phone={NEW_PHONE!r}")
        else:
            # Safety: if someone changed format, just prepend +58 if missing
            if current_phone and not current_phone.startswith("+"):
                loc["phone"] = "+58" + current_phone.lstrip("0")
                p.location = loc
                flag_modified(p, "location")
                print(f"  AFTER:  phone={loc['phone']!r} (heuristic +58 prepend)")
            else:
                print(f"  unexpected format \u2014 manual review needed")

    db.session.commit()

    # --------------------------------------------------------
    # Verify
    # --------------------------------------------------------
    print("\n" + "=" * 80)
    print("VERIFY")
    print("=" * 80)
    us = Experience.query.filter_by(slug=US_RETAIL_SLUG).first()
    for tr in us.translations:
        first_line = (tr.description or "").strip().split("\n", 1)[0]
        print(f"  US Retail [{tr.lang}] first line: {first_line[:120]}")

    p = Profile.query.first()
    print(f"  Profile phone: {(p.location or {}).get('phone', '')!r}")

    # Invalidate caches
    try:
        from backend.services.cv_cache import invalidate_all_cv_cache
        invalidate_all_cv_cache()
        print("\n  CV caches invalidated")
    except Exception as e:
        print(f"\n  (cache invalidation skipped: {e})")
