"""
Import Normalized Portfolio Data

Imports your unified portfolio data (CV + Portfolio) into the database.

Usage:
    python scripts/import_normalized_portfolio.py
    python scripts/import_normalized_portfolio.py --file backend/data/my_data.json --dry-run
"""

import sys
import os
import json
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app, db
from backend.models.entity import Entity
from backend.models.translation import EntityTranslation
from backend.services.cache_service import invalidate_entities_cache


def import_profile(profile_data, metadata=None):
    """Import profile information"""
    print("\n👤 Importing profile...")

    entity = Entity.query.filter_by(slug="rafael-ortiz-profile").first()
    if not entity:
        entity = Entity()
        db.session.add(entity)
        print("  Creating profile")
    else:
        print("  Updating profile")
        entity.translations.clear()

    entity.slug = "rafael-ortiz-profile"
    entity.type = "profile"

    # Build meta with profile data
    entity.meta = {
        "name": profile_data.get("name"),
        "email": profile_data.get("email"),
        "phone": profile_data.get("phone"),
        "location": profile_data.get("location", {}),
        "social": profile_data.get("social", {}),
    }

    # Add metadata if provided
    if metadata:
        entity.meta["import_version"] = metadata.get("version")
        entity.meta["imported_at"] = datetime.utcnow().isoformat()
        entity.meta["cv_metadata"] = {
            "version": metadata.get("version"),
            "profile": metadata.get("profile"),
            "theme": metadata.get("theme"),
            "creationDate": metadata.get("creationDate"),
            "printCount": metadata.get("printCount", 0),
        }

    # Add translations (role, tagline, summary)
    for lang, trans in profile_data.get("translations", {}).items():
        t = EntityTranslation(
            lang=lang,
            title=trans.get("role", ""),  # Hero + CV role
            subtitle=trans.get("tagline", ""),  # Hero tagline
            summary=trans.get("summary", ""),  # CV summary
            description="",
            content={},
        )
        entity.translations.append(t)

    print("✅ Imported profile")
    return 1


def import_work_experience(work_items):
    """Import work experience"""
    print("\n💼 Importing work experience...")
    count = 0

    for item in work_items:
        entity = Entity.query.filter_by(slug=item["slug"]).first()
        if not entity:
            entity = Entity()
            db.session.add(entity)
            print(f"  Creating: {item['slug']}")
        else:
            print(f"  Updating: {item['slug']}")
            entity.translations.clear()

        entity.slug = item["slug"]
        entity.type = "experience"
        entity.meta = {
            "company": item.get("company"),
            "company_url": item.get("company_url"),
            "location": item.get("location"),
            "startDate": item.get("startDate"),
            "endDate": item.get("endDate"),
            "tags": item.get("tags", []),
            "images": item.get("images", {}),
            "show_in_portfolio": item.get("show_in_portfolio", True),
            "show_in_cv": item.get("show_in_cv", True),
        }

        # Add translations
        for lang, trans in item.get("translations", {}).items():
            t = EntityTranslation(
                lang=lang,
                title=trans.get("position", ""),  # Job title (portfolio + CV)
                subtitle=item.get("company", ""),  # Company (for cards)
                summary=trans.get("summary", ""),  # CV summary line
                description="",  # Not used for work
                content={"highlights": trans.get("highlights", [])},  # CV highlights
            )
            entity.translations.append(t)

        count += 1

    print(f"✅ Imported {count} work experiences")
    return count


def import_skills(skills):
    """Import skills"""
    print("\n🎯 Importing skills...")
    count = 0

    for item in skills:
        entity = Entity.query.filter_by(slug=item["slug"]).first()
        if not entity:
            entity = Entity()
            db.session.add(entity)
            print(f"  Creating: {item['slug']}")
        else:
            print(f"  Updating: {item['slug']}")
            entity.translations.clear()

        entity.slug = item["slug"]
        entity.type = "skill"
        entity.meta = {
            "name": item.get("name"),
            "category": item.get("category"),
            "level": item.get("level"),
            "show_in_cv": item.get("show_in_cv", True),
            "show_in_portfolio": item.get("show_in_portfolio", True),
        }

        # Skills don't need translations (name is same in all languages)
        # Create translation for BOTH languages since skill names are universal
        for lang in ["es", "en"]:
            t = EntityTranslation(
                lang=lang,
                title=item.get("name"),
                subtitle=item.get("level", ""),
                summary="",
                description="",
                content={},
            )
            entity.translations.append(t)

        count += 1

    print(f"✅ Imported {count} skills")
    return count


def import_education(education):
    """Import education"""
    print("\n🎓 Importing education...")
    count = 0

    for item in education:
        entity = Entity.query.filter_by(slug=item["slug"]).first()
        if not entity:
            entity = Entity()
            db.session.add(entity)
            print(f"  Creating: {item['slug']}")
        else:
            print(f"  Updating: {item['slug']}")
            entity.translations.clear()

        entity.slug = item["slug"]
        entity.type = "education"
        entity.meta = {
            "institution": item.get("institution"),
            "institution_url": item.get("institution_url"),
            "location": item.get("location"),
            "startDate": item.get("startDate"),
            "endDate": item.get("endDate"),
            "current": item.get("current", False),
            "courses": item.get("courses", []),
            "show_in_cv": item.get("show_in_cv", True),
            "show_in_portfolio": item.get("show_in_portfolio", True),
        }

        # Add translations
        # For education: title=area, subtitle=studyType (institution comes from meta)
        for lang, trans in item.get("translations", {}).items():
            t = EntityTranslation(
                lang=lang,
                title=trans.get("area", ""),  # "Informática" / "Computer Science"
                subtitle=trans.get("studyType", ""),  # "Técnico Superior Universitario"
                summary="",  # Not used for education cards
                description="",
                content={"courses": item.get("courses", [])},
            )
            entity.translations.append(t)

        count += 1

    print(f"✅ Imported {count} education entries")
    return count


def import_certifications(certs):
    """Import certifications"""
    print("\n📜 Importing certifications...")
    count = 0

    for item in certs:
        entity = Entity.query.filter_by(slug=item["slug"]).first()
        if not entity:
            entity = Entity()
            db.session.add(entity)
            print(f"  Creating: {item['slug']}")
        else:
            print(f"  Updating: {item['slug']}")
            entity.translations.clear()

        entity.slug = item["slug"]
        entity.type = "certification"
        entity.meta = {
            "issuer": item.get("issuer"),
            "issue_date": item.get("issue_date"),
            "credential_url": item.get("credential_url"),
            "show_in_cv": item.get("show_in_cv", True),
            "show_in_portfolio": item.get("show_in_portfolio", True),
        }

        # Add translations
        for lang, trans in item.get("translations", {}).items():
            t = EntityTranslation(
                lang=lang,
                title=trans.get("title", ""),
                subtitle=item.get("issuer", ""),
                summary=trans.get("description", ""),
                description="",
                content={},
            )
            entity.translations.append(t)

        count += 1

    print(f"✅ Imported {count} certifications")
    return count


def main():
    parser = argparse.ArgumentParser(description="Import normalized portfolio data")
    parser.add_argument(
        "--file",
        default="backend/data/portfolio_normalized.json",
        help="Path to JSON file",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    args = parser.parse_args()

    print("=" * 60)
    print("NORMALIZED PORTFOLIO DATA IMPORT")
    print("=" * 60)

    # Load JSON
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"\n✅ Loaded: {args.file}")
    except FileNotFoundError:
        print(f"\n❌ File not found: {args.file}")
        return 1
    except json.JSONDecodeError as e:
        print(f"\n❌ Invalid JSON: {e}")
        return 1

    with app.app_context():
        # Check database
        try:
            db.session.execute(db.text("SELECT 1"))
            print("✅ Database connected")
        except Exception as e:
            print(f"❌ Database error: {e}")
            return 1

        # Extract metadata
        metadata = data.get("metadata", {})
        if metadata:
            print(
                f"\n📋 Metadata: v{metadata.get('version', 'N/A')} - Profile: {metadata.get('profile', 'N/A')}"
            )

        # Import data
        total = 0

        if "profile" in data:
            total += import_profile(data["profile"], metadata)

        if "work_experience" in data:
            total += import_work_experience(data["work_experience"])

        if "skills" in data:
            total += import_skills(data["skills"])

        if "education" in data:
            total += import_education(data["education"])

        if "certifications" in data:
            total += import_certifications(data["certifications"])

        # Save or rollback
        if args.dry_run:
            print("\n🔍 DRY RUN - No changes saved")
            db.session.rollback()
        else:
            try:
                db.session.commit()
                print(f"\n✅ Successfully imported {total} items")

                # Invalidate cache
                invalidate_entities_cache()
                print("✅ Cache invalidated")

            except Exception as e:
                db.session.rollback()
                print(f"\n❌ Save failed: {e}")
                return 1

        print("\n" + "=" * 60)
        print("IMPORT COMPLETE!")
        print("=" * 60)

        if not args.dry_run:
            print("\nCheck your data:")
            print("  CV: http://localhost:5000/cv")
            print("  API: http://localhost:5000/api/entities")
            print("  Portfolio: http://localhost:5173")

        return 0


if __name__ == "__main__":
    sys.exit(main())
