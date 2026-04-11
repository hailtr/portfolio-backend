"""Check HONOR experience description and Skills section for BigQuery/Snowflake."""
from backend.app import app
from backend.models.experience import Experience
from backend.models.skill import Skill, SkillCategory


with app.app_context():
    print("=== HONOR ===")
    honor = Experience.query.filter_by(slug="honor-solutions-engineer").first()
    if not honor:
        print("  NOT FOUND")
    else:
        for t in honor.translations:
            print(f"\n--- lang={t.lang} ---")
            print(f"title={t.title!r}")
            print("description:")
            print(t.description)
            print("---END---")

    print("\n\n=== SKILLS ===")
    from backend.models.skill import SkillTranslation
    for cat in SkillCategory.query.order_by(SkillCategory.order).all():
        cat_name = next((t.name for t in cat.translations if t.lang == "en"), cat.slug)
        print(f"\n[{cat.slug}] {cat_name}")
        skills = Skill.query.filter_by(category_id=cat.id).order_by(Skill.order).all()
        for s in skills:
            en_name = next((t.name for t in s.translations if t.lang == "en"), s.slug)
            vis = "CV" if s.is_visible_cv else "--"
            print(f"  {s.order:3d} [{vis}] {en_name}")
