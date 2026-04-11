"""Dump current skills structure for migration review."""
from backend.app import app
from backend.models.skill import Skill, SkillCategory, SkillCategoryTranslation, SkillTranslation

with app.app_context():
    cats = SkillCategory.query.order_by(SkillCategory.order).all()
    print(f"=== {len(cats)} CATEGORIES ===\n")
    for c in cats:
        en = next((t.name for t in c.translations if t.lang == "en"), "?")
        es = next((t.name for t in c.translations if t.lang == "es"), "?")
        print(f"  id={c.id:<3} slug={c.slug:<30} order={c.order:<4} en={en!r:<30} es={es!r}")
        for s in sorted(c.skills, key=lambda x: x.order):
            en_name = next((t.name for t in s.translations if t.lang == "en"), "?")
            es_name = next((t.name for t in s.translations if t.lang == "es"), "?")
            print(f"      skill id={s.id:<3} slug={s.slug:<35} order={s.order:<4} en={en_name!r:<35} es={es_name!r}  vis_cv={s.is_visible_cv}")
        print()

    # Also dump orphan skills (no category)
    orphans = Skill.query.filter(Skill.category_id.is_(None)).all()
    if orphans:
        print(f"=== {len(orphans)} ORPHAN SKILLS (no category) ===")
        for s in orphans:
            en_name = next((t.name for t in s.translations if t.lang == "en"), "?")
            print(f"  id={s.id:<3} slug={s.slug:<35} en={en_name!r}  vis_cv={s.is_visible_cv}")
