"""Dump current tags + experience descriptions for planning the content compress."""
from backend.app import app
from backend.models.tag import Tag
from backend.models.experience import Experience

with app.app_context():
    tags = Tag.query.order_by(Tag.category, Tag.name).all()
    print(f"=== {len(tags)} TAGS ===")
    for t in tags:
        print(f"  id={t.id:<4} slug={t.slug:<30} cat={t.category or '-':<15} name={t.name}")

    print(f"\n=== EXPERIENCES (tags + description preview) ===")
    exps = Experience.query.order_by(Experience.start_date.desc()).all()
    for e in exps:
        print(f"\n[{e.slug}]  ({e.start_date}..{e.end_date})  tags={[t.name for t in e.tags]}")
        for tr in e.translations:
            if tr.lang == "en":
                desc = tr.description or ""
                print(f"  EN description ({len(desc)} chars):")
                for line in desc.strip().split("\n"):
                    print(f"    {line[:120]}")
