"""Dump full experience content for review."""
from backend.app import app
from backend.models.experience import Experience
from sqlalchemy import desc

with app.app_context():
    experiences = Experience.query.order_by(desc(Experience.start_date)).all()
    print(f"Total experiences: {len(experiences)}\n")
    print("=" * 100)
    for exp in experiences:
        print(f"\nSLUG:     {exp.slug}")
        print(f"COMPANY:  {exp.company}")
        print(f"LOCATION: {exp.location}")
        print(f"DATES:    {exp.start_date} to {exp.end_date} (current={exp.current})")
        for trans in exp.translations:
            print(f"\n  --- [{trans.lang}] ---")
            print(f"  TITLE:    {trans.title}")
            print(f"  SUBTITLE: {trans.subtitle}")
            print(f"  DESCRIPTION:")
            if trans.description:
                for line in trans.description.split('\n'):
                    print(f"    {line}")
            else:
                print("    (empty)")
        print("\n" + "=" * 100)
