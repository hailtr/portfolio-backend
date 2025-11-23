"""
Simple migration runner - run from project root
Usage: python migrate.py
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import app, db
from backend.models.entity import Entity
from backend.models.translation import EntityTranslation
from backend.models.project import Project, ProjectImage, ProjectTranslation
from backend.models.experience import Experience, ExperienceTranslation
from backend.models.education import Education, EducationTranslation, Course
from backend.models.skill import Skill, SkillTranslation
from backend.models.profile import Profile, ProfileTranslation
from backend.models.certification import Certification, CertificationTranslation
from backend.models.tag import Tag
import json


def get_or_create_tag(tag_name):
    """Get existing tag or create new one"""
    tag = Tag.query.filter_by(name=tag_name).first()
    if not tag:
        slug = tag_name.lower().replace(" ", "-")
        tag = Tag(name=tag_name, slug=slug)
        db.session.add(tag)
    return tag


def migrate_project(entity):
    """Migrate a project entity"""
    print(f"  Migrating project: {entity.slug}")
    
    project = Project(
        slug=entity.slug,
        category=entity.meta.get("category") if entity.meta else None,
        url=entity.meta.get("url") if entity.meta else None,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
    db.session.add(project)
    db.session.flush()
    
    # Migrate images
    if entity.meta and entity.meta.get("images"):
        images_data = entity.meta["images"]
        
        if isinstance(images_data, dict):
            order = 0
            if images_data.get("desktop"):
                img = ProjectImage(
                    project_id=project.id,
                    url=images_data["desktop"],
                    type="image",
                    order=order,
                )
                db.session.add(img)
                order += 1
            if images_data.get("mobile"):
                img = ProjectImage(
                    project_id=project.id,
                    url=images_data["mobile"],
                    type="image",
                    order=order,
                )
                db.session.add(img)
        elif isinstance(images_data, list):
            for img_data in images_data:
                if isinstance(img_data, dict):
                    img = ProjectImage(
                        project_id=project.id,
                        url=img_data.get("url", ""),
                        type=img_data.get("type", "image"),
                        caption=img_data.get("caption", ""),
                        order=img_data.get("order", 0),
                    )
                    db.session.add(img)
    
    # Migrate tags
    if entity.meta and entity.meta.get("tags"):
        for tag_name in entity.meta["tags"]:
            tag = get_or_create_tag(tag_name)
            project.tags.append(tag)
    
    # Migrate translations
    for trans in entity.translations:
        pt = ProjectTranslation(
            project_id=project.id,
            lang=trans.lang,
            title=trans.title,
            subtitle=trans.subtitle,
            description=trans.description,
            summary=trans.summary,
            content=trans.content,
        )
        db.session.add(pt)


def migrate_experience(entity):
    """Migrate an experience entity"""
    print(f"  Migrating experience: {entity.slug}")
    
    exp = Experience(
        slug=entity.slug,
        company=entity.meta.get("institution") if entity.meta else None,
        location=entity.meta.get("location") if entity.meta else None,
        start_date=entity.meta.get("startDate") if entity.meta else None,
        end_date=entity.meta.get("endDate") if entity.meta else None,
        current=entity.meta.get("current", False) if entity.meta else False,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
    db.session.add(exp)
    db.session.flush()
    
    # Migrate tags
    if entity.meta and entity.meta.get("tags"):
        for tag_name in entity.meta["tags"]:
            tag = get_or_create_tag(tag_name)
            exp.tags.append(tag)
    
    # Migrate translations
    for trans in entity.translations:
        et = ExperienceTranslation(
            experience_id=exp.id,
            lang=trans.lang,
            title=trans.subtitle,
            subtitle=trans.title,
            description=trans.description,
        )
        db.session.add(et)


def migrate_education(entity):
    """Migrate an education entity"""
    print(f"  Migrating education: {entity.slug}")
    
    edu = Education(
        slug=entity.slug,
        institution=entity.meta.get("institution") if entity.meta else None,
        location=entity.meta.get("location") if entity.meta else None,
        start_date=entity.meta.get("startDate") if entity.meta else None,
        end_date=entity.meta.get("endDate") if entity.meta else None,
        current=entity.meta.get("current", False) if entity.meta else False,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
    db.session.add(edu)
    db.session.flush()
    
    # Migrate courses
    if entity.meta and entity.meta.get("courses"):
        for idx, course_name in enumerate(entity.meta["courses"]):
            course = Course(education_id=edu.id, name=course_name, order=idx)
            db.session.add(course)
    
    # Migrate translations
    for trans in entity.translations:
        et = EducationTranslation(
            education_id=edu.id,
            lang=trans.lang,
            title=trans.title,
            subtitle=trans.subtitle,
            description=trans.description,
        )
        db.session.add(et)


def migrate_skill(entity):
    """Migrate a skill entity"""
    print(f"  Migrating skill: {entity.slug}")
    
    skill = Skill(
        slug=entity.slug,
        icon_url=entity.meta.get("icon_url") if entity.meta else None,
        proficiency=entity.meta.get("proficiency", 50) if entity.meta else 50,
        category=entity.meta.get("category") if entity.meta else None,
        order=entity.meta.get("order", 0) if entity.meta else 0,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
    db.session.add(skill)
    db.session.flush()
    
    # Migrate translations
    for trans in entity.translations:
        st = SkillTranslation(
            skill_id=skill.id,
            lang=trans.lang,
            name=trans.title or entity.slug,
            description=trans.description,
        )
        db.session.add(st)


def migrate_certification(entity):
    """Migrate a certification entity"""
    print(f"  Migrating certification: {entity.slug}")
    
    cert = Certification(
        slug=entity.slug,
        issuer=entity.meta.get("issuer") if entity.meta else None,
        issue_date=entity.meta.get("issueDate") if entity.meta else None,
        expiry_date=entity.meta.get("expiryDate") if entity.meta else None,
        credential_url=entity.meta.get("url") if entity.meta else None,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
    db.session.add(cert)
    db.session.flush()
    
    # Migrate translations
    for trans in entity.translations:
        ct = CertificationTranslation(
            certification_id=cert.id,
            lang=trans.lang,
            title=trans.title,
            description=trans.description,
        )
        db.session.add(ct)

def migrate_profile(entity):
    """Migrate a profile entity"""
    print(f"  Migrating profile: {entity.slug}")
    
    # Handle social_links - it might be a dict or JSON string
    social_links = None
    if entity.meta and entity.meta.get("social"):
        social_data = entity.meta["social"]
        if isinstance(social_data, str):
            try:
                social_links = json.loads(social_data)
            except:
                social_links = social_data
        else:
            social_links = social_data
    
    profile = Profile(
        slug=entity.slug,
        name=entity.meta.get("name", "") if entity.meta else "",
        email=entity.meta.get("email") if entity.meta else None,
        location=entity.meta.get("location") if entity.meta else None,
        avatar_url=entity.meta.get("avatar_url") if entity.meta else None,
        social_links=social_links,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
    db.session.add(profile)
    db.session.flush()
    
    # Migrate translations
    for trans in entity.translations:
        pt = ProfileTranslation(
            profile_id=profile.id,
            lang=trans.lang,
            role=trans.title,
            tagline=trans.subtitle,
            bio=trans.description,
        )
        db.session.add(pt)


def run_migration():
    """Main migration function"""
    with app.app_context():
        print("=" * 60)
        print("STARTING DATABASE MIGRATION")
        print("=" * 60)
        
        # Create all new tables
        print("\n1. Creating new tables...")
        db.create_all()
        print("   ✓ Tables created")
        
        # Get all entities
        entities = Entity.query.all()
        print(f"\n2. Found {len(entities)} entities to migrate")
        
        # Count by type
        type_counts = {}
        for entity in entities:
            type_counts[entity.type] = type_counts.get(entity.type, 0) + 1
        
        for entity_type, count in type_counts.items():
            print(f"   - {entity_type}: {count}")
        
        # Migrate by type
        print("\n3. Migrating data...")
        for entity in entities:
            try:
                if entity.type == "project":
                    migrate_project(entity)
                elif entity.type == "experience":
                    migrate_experience(entity)
                elif entity.type == "education":
                    migrate_education(entity)
                elif entity.type == "skill":
                    migrate_skill(entity)
                elif entity.type == "certification":
                    migrate_certification(entity)
                elif entity.type == "profile":
                    migrate_profile(entity)
                else:
                    print(f"  ⚠ Unknown type: {entity.type} for {entity.slug}")
            except Exception as e:
                print(f"  ✗ Error migrating {entity.slug}: {e}")
                db.session.rollback()
                raise
        
        # Commit all changes
        print("\n4. Committing changes...")
        db.session.commit()
        print("   ✓ Committed")
        
        # Show results
        print("\n" + "=" * 60)
        print("MIGRATION COMPLETE!")
        print("=" * 60)
        print(f"Projects:    {Project.query.count()}")
        print(f"Experiences: {Experience.query.count()}")
        print(f"Education:   {Education.query.count()}")
        print(f"Skills:      {Skill.query.count()}")
        print(f"Certifications: {Certification.query.count()}")
        print(f"Profiles:    {Profile.query.count()}")
        print(f"Tags:        {Tag.query.count()}")
        print("=" * 60)


if __name__ == "__main__":
    run_migration()
