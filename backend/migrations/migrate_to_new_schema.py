"""
Migration script to transfer data from Entity table to new schema.
Run this ONCE after creating new tables.

Usage:
    python -m backend.migrations.migrate_to_new_schema
"""

from backend import db, create_app
from backend.models.entity import Entity
from backend.models.translation import EntityTranslation
from backend.models.project import Project, ProjectImage, ProjectTranslation
from backend.models.experience import Experience, ExperienceTranslation
from backend.models.education import Education, EducationTranslation, Course
from backend.models.skill import Skill, SkillTranslation
from backend.models.profile import Profile, ProfileTranslation
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
    print(f"Migrating project: {entity.slug}")
    
    # Create project
    project = Project(
        slug=entity.slug,
        category=entity.meta.get("category") if entity.meta else None,
        url=entity.meta.get("url") if entity.meta else None,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
    db.session.add(project)
    db.session.flush()  # Get project.id
    
    # Migrate images
    if entity.meta and entity.meta.get("images"):
        images_data = entity.meta["images"]
        
        # Handle both old format {desktop, mobile} and new format [...]
        if isinstance(images_data, dict):
            # Old format
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
            # New format
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
    print(f"Migrating experience: {entity.slug}")
    
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
            title=trans.subtitle,  # Job title
            subtitle=trans.title,  # Company name (swap if needed)
            description=trans.description,
        )
        db.session.add(et)


def migrate_education(entity):
    """Migrate an education entity"""
    print(f"Migrating education: {entity.slug}")
    
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
    print(f"Migrating skill: {entity.slug}")
    
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


def migrate_profile(entity):
    """Migrate a profile entity"""
    print(f"Migrating profile: {entity.slug}")
    
    profile = Profile(
        slug=entity.slug,
        name=entity.meta.get("name", "") if entity.meta else "",
        email=entity.meta.get("email") if entity.meta else None,
        location=entity.meta.get("location") if entity.meta else None,
        avatar_url=entity.meta.get("avatar_url") if entity.meta else None,
        social_links=entity.meta.get("social_links") if entity.meta else None,
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
            role=trans.subtitle,
            tagline=trans.summary,
            bio=trans.description,
        )
        db.session.add(pt)


def run_migration():
    """Main migration function"""
    from backend.app import app
    
    with app.app_context():
        print("Starting migration...")
        
        # Create all new tables
        print("Creating new tables...")
        db.create_all()
        
        # Get all entities
        entities = Entity.query.all()
        print(f"Found {len(entities)} entities to migrate")
        
        # Migrate by type
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
                elif entity.type == "profile":
                    migrate_profile(entity)
                else:
                    print(f"Unknown type: {entity.type} for {entity.slug}")
            except Exception as e:
                print(f"Error migrating {entity.slug}: {e}")
                db.session.rollback()
                raise
        
        # Commit all changes
        print("Committing changes...")
        db.session.commit()
        
        print("Migration complete!")
        print(f"Projects: {Project.query.count()}")
        print(f"Experiences: {Experience.query.count()}")
        print(f"Education: {Education.query.count()}")
        print(f"Skills: {Skill.query.count()}")
        print(f"Profiles: {Profile.query.count()}")
        print(f"Tags: {Tag.query.count()}")


if __name__ == "__main__":
    run_migration()
