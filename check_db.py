from backend.app import app
from backend.models.entity import Entity
from sqlalchemy.orm import joinedload

app.app_context().push()

# Check profile
profile = Entity.query.options(joinedload(Entity.translations)).filter_by(
    type='profile', slug='rafael-ortiz-profile'
).first()

if profile:
    print("Profile found!")
    print(f"Profile meta: {profile.meta}")
    print("\nTranslations:")
    for t in profile.translations:
        print(f"  - {t.lang}:")
        print(f"      title: {t.title}")
        print(f"      subtitle: {t.subtitle}")
        print(f"      summary: {t.summary[:80] if t.summary else 'EMPTY'}...")
else:
    print("NO PROFILE FOUND")

# Check skills with English translations
print("\n\nChecking skills with English translations:")
skills_en = Entity.query.options(joinedload(Entity.translations)).filter_by(type='skill').all()
skills_with_en = [s for s in skills_en if any(t.lang == 'en' for t in s.translations)]
print(f"Total skills: {len(skills_en)}")
print(f"Skills with EN translation: {len(skills_with_en)}")

if len(skills_with_en) > 0:
    print("\nFirst 3 skills with EN:")
    for skill in skills_with_en[:3]:
        en_trans = next((t for t in skill.translations if t.lang == 'en'), None)
        print(f"  - {en_trans.title if en_trans else 'NO TITLE'}")

