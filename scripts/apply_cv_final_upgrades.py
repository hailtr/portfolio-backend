"""Apply the final three CV upgrades post-DeepSeek review:

1. IUGT education: set current=True so the CV shows "Expected Graduation 2026"
   instead of the raw 05/2026 date.

2. US Retail — specify LLM tooling (Gemini + Claude) in the 1,350-objects
   migration bullet. Replaces the vague "LLM tooling".

3. Profile bio — append a one-line "open to permanent" signal to both EN and ES
   so hiring managers at target teams know you're open to staying long-term.
"""
from backend.app import app
from backend import db
from backend.models.education import Education
from backend.models.experience import Experience
from backend.models.profile import Profile


# ============================================================
# 1. IUGT → current=True
# ============================================================
IUGT_SLUG = "iugt-tsu"


# ============================================================
# 2. US Retail — LLM tooling specificity
# ============================================================
US_RETAIL_SLUG = "us-retail-data-architect-contract"
LLM_REPLACEMENTS = {
    "en": (
        "using Python + LLM tooling I built",
        "using Python + Gemini and Claude tooling I built",
    ),
    "es": (
        "usando herramientas Python + LLM que construí",
        "usando herramientas Python + Gemini y Claude que construí",
    ),
}


# ============================================================
# 3. Profile bio — "open to permanent" line
# ============================================================
OPEN_EN = (
    " Open to the right senior/lead role with a team that wants a builder, "
    "not a button-pusher."
)
OPEN_ES = (
    " Abierto al rol senior/lead correcto con un equipo que busca un builder, "
    "no un presiona-botones."
)


with app.app_context():
    # --------------------------------------------------------
    # 1. IUGT current=True
    # --------------------------------------------------------
    print("=" * 80)
    print("1. IUGT → current=True")
    print("=" * 80)
    iugt = Education.query.filter_by(slug=IUGT_SLUG).first()
    if not iugt:
        print(f"  SKIP: {IUGT_SLUG} not found")
    else:
        print(f"  BEFORE: current={iugt.current}  end_date={iugt.end_date}")
        iugt.current = True
        print(f"  AFTER:  current={iugt.current}  end_date={iugt.end_date}")

    # --------------------------------------------------------
    # 2. US Retail LLM specificity
    # --------------------------------------------------------
    print("\n" + "=" * 80)
    print("2. US Retail — Gemini + Claude specificity")
    print("=" * 80)
    us = Experience.query.filter_by(slug=US_RETAIL_SLUG).first()
    if not us:
        print(f"  SKIP: {US_RETAIL_SLUG} not found")
    else:
        for tr in us.translations:
            old_fragment, new_fragment = LLM_REPLACEMENTS[tr.lang]
            if old_fragment in (tr.description or ""):
                tr.description = tr.description.replace(old_fragment, new_fragment)
                print(f"  [{tr.lang}] REPLACED")
                print(f"    {old_fragment!r}")
                print(f"      -> {new_fragment!r}")
            else:
                print(f"  [{tr.lang}] fragment not found — skipping")

    # --------------------------------------------------------
    # 3. Profile bio — append open-to-permanent line
    # --------------------------------------------------------
    print("\n" + "=" * 80)
    print("3. Profile bio — open to permanent")
    print("=" * 80)
    p = Profile.query.first()
    if not p:
        print("  SKIP: no profile found")
    else:
        for tr in p.translations:
            addition = OPEN_EN if tr.lang == "en" else OPEN_ES
            if addition.strip() in (tr.bio or ""):
                print(f"  [{tr.lang}] already present — skipping")
                continue
            tr.bio = (tr.bio or "").rstrip() + addition
            print(f"  [{tr.lang}] appended")
            print(f"    ...{tr.bio[-180:]!r}")

    db.session.commit()

    # --------------------------------------------------------
    # Verify
    # --------------------------------------------------------
    print("\n" + "=" * 80)
    print("VERIFY")
    print("=" * 80)
    iugt = Education.query.filter_by(slug=IUGT_SLUG).first()
    print(f"  IUGT: current={iugt.current}")

    us = Experience.query.filter_by(slug=US_RETAIL_SLUG).first()
    for tr in us.translations:
        for line in (tr.description or "").split("\n"):
            if "Gemini" in line or "LLM" in line:
                print(f"  US Retail [{tr.lang}]: ...{line.strip()[:120]}...")

    p = Profile.query.first()
    for tr in p.translations:
        print(f"  Profile [{tr.lang}] last 100 chars: ...{(tr.bio or '')[-100:]!r}")

    # Invalidate caches
    try:
        from backend.services.cv_cache import invalidate_all_cv_cache
        invalidate_all_cv_cache()
        print("\n  CV caches invalidated")
    except Exception as e:
        print(f"\n  (cache invalidation skipped: {e})")
