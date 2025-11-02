#!/usr/bin/env python
"""
Migration script to load data from gallery.json into the database.

This script:
1. Reads gallery.json
2. Creates Entity records for each project
3. Creates EntityTranslation records for each language
4. Handles duplicates (updates if slug exists)

Usage:
    python migrate_gallery.py
"""

import os
import sys
import json

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from backend import db
from backend.app import app
from backend.models.entity import Entity
from backend.models.translation import EntityTranslation

def load_gallery_json():
    """Load gallery.json file."""
    gallery_path = os.path.join(project_root, 'data', 'gallery.json')
    
    if not os.path.exists(gallery_path):
        print("❌ Error: gallery.json not found!")
        print(f"   Expected location: {gallery_path}")
        return None
    
    with open(gallery_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def migrate_data():
    """Migrate gallery.json data to database."""
    print("🚀 Starting migration from gallery.json to database...")
    print()
    
    # Load data
    data = load_gallery_json()
    if not data:
        return
    
    # Group by ID (slug) across languages
    projects_by_id = {}
    for lang, projects in data.items():
        for project in projects:
            project_id = project['id']
            if project_id not in projects_by_id:
                projects_by_id[project_id] = {}
            projects_by_id[project_id][lang] = project
    
    print(f"📊 Found {len(projects_by_id)} unique projects")
    print()
    
    # Migrate each project
    created_count = 0
    updated_count = 0
    
    with app.app_context():
        for project_id, languages in projects_by_id.items():
            # Get first language data for common fields
            first_lang = next(iter(languages.values()))
            
            # Check if entity already exists
            entity = Entity.query.filter_by(slug=project_id).first()
            
            if entity:
                print(f"📝 Updating: {project_id}")
                updated_count += 1
                # Clear existing translations
                entity.translations = []
            else:
                print(f"✨ Creating: {project_id}")
                created_count += 1
                entity = Entity(slug=project_id)
                db.session.add(entity)
            
            # Set common fields
            entity.type = 'project'  # All items in gallery are projects
            entity.meta = {
                'category': first_lang.get('category', ''),
                'tags': first_lang.get('tags', [])
            }
            
            # Handle images if present
            if 'images' in first_lang:
                entity.meta['images'] = first_lang['images']
            
            # Create translations for each language
            for lang, project_data in languages.items():
                translation = EntityTranslation(
                    lang=lang,
                    title=project_data.get('title', ''),
                    subtitle=project_data.get('subtitle', ''),
                    description=project_data.get('description', ''),
                    summary=project_data.get('description', '')[:200] if project_data.get('description') else '',
                    content={
                        'images': project_data.get('images', {}),
                        'category': project_data.get('category', '')
                    }
                )
                entity.translations.append(translation)
                print(f"  └─ Added translation: {lang}")
        
        # Commit all changes
        try:
            db.session.commit()
            print()
            print("✅ Migration completed successfully!")
            print(f"   - Created: {created_count} projects")
            print(f"   - Updated: {updated_count} projects")
            print(f"   - Total: {len(projects_by_id)} projects")
        except Exception as e:
            db.session.rollback()
            print()
            print("❌ Migration failed!")
            print(f"   Error: {e}")
            return False
    
    return True


def verify_migration():
    """Verify migration was successful."""
    print()
    print("🔍 Verifying migration...")
    
    with app.app_context():
        entities = Entity.query.all()
        translations = EntityTranslation.query.all()
        
        print(f"   - Entities in database: {len(entities)}")
        print(f"   - Translations in database: {len(translations)}")
        
        # Show sample
        if entities:
            print()
            print("📋 Sample entity:")
            entity = entities[0]
            print(f"   - ID: {entity.id}")
            print(f"   - Slug: {entity.slug}")
            print(f"   - Type: {entity.type}")
            print(f"   - Languages: {[t.lang for t in entity.translations]}")


if __name__ == '__main__':
    print("=" * 60)
    print("  GALLERY.JSON → DATABASE MIGRATION")
    print("=" * 60)
    print()
    
    with app.app_context():
        # Check database connection
        try:
            db.session.execute(db.text("SELECT 1"))
            print("✅ Database connection successful")
            print()
        except Exception as e:
            print("❌ Database connection failed!")
            print(f"   Error: {e}")
            print()
            print("💡 Make sure:")
            print("   1. Your .env file has correct DATABASE_URL")
            print("   2. PostgreSQL is running (or use SQLite for testing)")
            sys.exit(1)
        
        # Create tables if they don't exist
        print("🔧 Creating tables if needed...")
        db.create_all()
        print("✅ Tables ready")
        print()
    
    # Run migration
    success = migrate_data()
    
    if success:
        verify_migration()
        print()
        print("=" * 60)
        print("🎉 All done! Your data is now in the database.")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("⚠️  Migration completed with errors. Check logs above.")
        print("=" * 60)
        sys.exit(1)

