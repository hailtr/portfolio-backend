"""
Quick script to check if you have projects in your database
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app, db
from backend.models.entity import Entity
from backend.models.translation import EntityTranslation

with app.app_context():
    print("=" * 60)
    print("DATABASE CHECK")
    print("=" * 60)

    # Check connection
    try:
        db.session.execute(db.text("SELECT 1"))
        print("✓ Database connected!")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        sys.exit(1)

    # Check entities
    entities = Entity.query.all()
    print(f"\nTotal entities in database: {len(entities)}")

    if len(entities) == 0:
        print("\n⚠️  NO PROJECTS FOUND!")
        print("This is why your gallery is empty.")
        print("\nTo fix:")
        print("1. Go to http://localhost:5000/google/login")
        print("2. Login as admin")
        print("3. Go to http://localhost:5000/admin")
        print("4. Create your first project")
    else:
        print("\n✓ Projects found:\n")
        for entity in entities:
            print(f"  - {entity.slug} ({entity.type})")
            translations = [t.lang for t in entity.translations]
            print(f"    Languages: {', '.join(translations)}")

    print("\n" + "=" * 60)
