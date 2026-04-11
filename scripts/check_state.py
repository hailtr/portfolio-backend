"""Quick state check for HONOR/Austranet contract status, IUGT current flag, and US Retail bullets."""
from backend.app import app
from backend.models.experience import Experience, ExperienceTranslation
from backend.models.education import Education
from backend.models.profile import Profile


with app.app_context():
    print("=== EDUCATION (all rows) ===")
    for edu in Education.query.all():
        print(f"  id={edu.id} slug={edu.slug}")
        print(f"    institution={edu.institution!r}")
        print(f"    current={edu.current}")
        print(f"    start={edu.start_date}  end={edu.end_date}")

    print("\n=== HONOR / Austranet company names ===")
    for slug in ["honor-solutions-engineer", "austranet-infra-data-engineer"]:
        e = Experience.query.filter_by(slug=slug).first()
        if not e:
            print(f"  NOT FOUND: {slug}")
            continue
        print(f"\n  {slug}")
        for tr in e.translations:
            print(f"    [{tr.lang}] company={tr.title!r}")

    print("\n=== US Retail description (search for 1,350) ===")
    us = Experience.query.filter_by(slug="us-retail-data-architect-contract").first()
    if us:
        for tr in us.translations:
            desc = tr.description or ""
            if "1,350" in desc or "1.350" in desc or "LLM" in desc:
                print(f"  [{tr.lang}]")
                for line in desc.split("\n"):
                    if "1,350" in line or "1.350" in line or "LLM" in line:
                        print(f"    >>> {line}")

    print("\n=== Profile bio ===")
    p = Profile.query.first()
    if p:
        for tr in p.translations:
            bio = (tr.bio or "")[:300]
            print(f"  [{tr.lang}] {bio!r}")
