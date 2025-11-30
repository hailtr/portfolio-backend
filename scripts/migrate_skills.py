import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app, db
from backend.models.skill import Skill, SkillCategory, SkillCategoryTranslation
from sqlalchemy import text

def migrate():
    with app.app_context():
        print("Starting Skills Migration...")
        
        # 1. Create new tables (SkillCategory, SkillCategoryTranslation)
        print("Creating new tables...")
        db.create_all()
        
        # 2. Add new columns to Skill table
        # 2. Add new columns to Skill table
        print("Adding columns to skills table...")
        with db.engine.connect() as conn:
            trans = conn.begin()
            try:
                # Check if columns exist first to avoid errors
                # Postgres specific check
                result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='skills' AND column_name='category_id'"))
                if not result.fetchone():
                    print("Adding category_id column...")
                    conn.execute(text("ALTER TABLE skills ADD COLUMN category_id INTEGER REFERENCES skill_categories(id)"))
                else:
                    print("category_id column already exists.")

                result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='skills' AND column_name='is_visible_cv'"))
                if not result.fetchone():
                    print("Adding is_visible_cv column...")
                    conn.execute(text("ALTER TABLE skills ADD COLUMN is_visible_cv BOOLEAN DEFAULT TRUE"))
                else:
                    print("is_visible_cv column already exists.")

                result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='skills' AND column_name='is_visible_portfolio'"))
                if not result.fetchone():
                    print("Adding is_visible_portfolio column...")
                    conn.execute(text("ALTER TABLE skills ADD COLUMN is_visible_portfolio BOOLEAN DEFAULT TRUE"))
                else:
                    print("is_visible_portfolio column already exists.")
                
                trans.commit()
                print("Schema update committed.")
            except Exception as e:
                trans.rollback()
                print(f"Error updating schema: {e}")
                raise e

        # 3. Migrate Data
        print("Migrating data...")
        skills = Skill.query.all()
        categories_cache = {}

        for skill in skills:
            # Initialize visibility flags if they are None (due to new column)
            if skill.is_visible_cv is None:
                skill.is_visible_cv = True
            if skill.is_visible_portfolio is None:
                skill.is_visible_portfolio = True

            if not skill.category:
                continue
            
            cat_name = skill.category.strip()
            
            # Get or Create Category
            if cat_name not in categories_cache:
                slug = cat_name.lower().replace(" ", "-").replace("/", "-")
                
                # Check DB
                cat = SkillCategory.query.filter_by(slug=slug).first()
                if not cat:
                    print(f"Creating category: {cat_name}")
                    cat = SkillCategory(slug=slug, order=0)
                    db.session.add(cat)
                    db.session.flush() # Get ID
                    
                    # Add translations
                    trans_es = SkillCategoryTranslation(category_id=cat.id, lang='es', name=cat_name)
                    trans_en = SkillCategoryTranslation(category_id=cat.id, lang='en', name=cat_name)
                    db.session.add(trans_es)
                    db.session.add(trans_en)
                
                categories_cache[cat_name] = cat
            
            # Assign Category ID
            skill.category_id = categories_cache[cat_name].id
        
        db.session.commit()
        print("Migration complete!")
        print(f"Total Skills: {len(skills)}")
        print(f"Total Categories: {len(categories_cache)}")

if __name__ == "__main__":
    migrate()
