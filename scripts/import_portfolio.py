"""
Import portfolio data from JSON template to database.
Usage: python scripts/import_portfolio.py
"""

import json
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app, db
from backend.models.profile import Profile, ProfileTranslation
from backend.models.experience import Experience, ExperienceTranslation
from backend.models.education import Education, EducationTranslation, Course
from backend.models.skill import Skill, SkillTranslation, SkillCategory, SkillCategoryTranslation
from backend.models.certification import Certification, CertificationTranslation
from backend.models.project import Project, ProjectTranslation, ProjectImage
from backend.models.project_url import ProjectURL
from backend.models.tag import Tag


def parse_date(date_str):
    """Parse date string in YYYY-MM format to date object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m").date()
    except:
        print(f"⚠️  Warning: Could not parse date '{date_str}', skipping")
        return None


def import_profile(data):
    """Import profile data"""
    print("📝 Importing profile...")
    
    profile = Profile(
        slug=data['slug'],
        name=data['name'],
        email=data.get('email'),
        location=data.get('location'),
        avatar_url=data.get('avatar_url'),
        social_links=data.get('social_links')
    )
    
    for lang, trans_data in data['translations'].items():
        trans = ProfileTranslation(
            lang=lang,
            role=trans_data.get('role'),
            tagline=trans_data.get('tagline'),
            bio=trans_data.get('bio')
        )
        profile.translations.append(trans)
    
    db.session.add(profile)
    print(f"   ✅ Profile: {profile.name}")


def import_experience(data_list):
    """Import experience data"""
    print(f"\\n💼 Importing {len(data_list)} experience entries...")
    
    for data in data_list:
        exp = Experience(
            slug=data['slug'],
            company=data['company'],
            location=data.get('location'),
            start_date=parse_date(data.get('start_date')),
            end_date=parse_date(data.get('end_date')),
            current=data.get('current', False)
        )
        
        # Add translations
        for lang, trans_data in data['translations'].items():
            trans = ExperienceTranslation(
                lang=lang,
                title=trans_data.get('title'),
                subtitle=trans_data.get('subtitle'),
                description=trans_data.get('description')
            )
            exp.translations.append(trans)
        
        # Add tags
        for tag_name in data.get('tags', []):
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                # Generate slug from tag name
                slug = tag_name.lower().replace(' ', '-').replace('.', '').replace('+', 'plus')
                tag = Tag(name=tag_name, slug=slug)
            exp.tags.append(tag)
        
        db.session.add(exp)
        print(f"   ✅ {exp.company}")


def import_education(data_list):
    """Import education data"""
    print(f"\\n🎓 Importing {len(data_list)} education entries...")
    
    for data in data_list:
        edu = Education(
            slug=data['slug'],
            institution=data['institution'],
            location=data.get('location'),
            start_date=parse_date(data.get('start_date')),
            end_date=parse_date(data.get('end_date')),
            current=data.get('current', False)
        )
        
        # Add translations
        for lang, trans_data in data['translations'].items():
            trans = EducationTranslation(
                lang=lang,
                title=trans_data.get('title'),
                subtitle=trans_data.get('subtitle'),
                description=trans_data.get('description')
            )
            edu.translations.append(trans)
        
        # Add courses
        for i, course_name in enumerate(data.get('courses', [])):
            course = Course(name=course_name, order=i)
            edu.courses.append(course)
        
        db.session.add(edu)
        print(f"   ✅ {edu.institution}")


def import_skill_categories(data_list):
    """Import skill categories"""
    print(f"\\n📁 Importing {len(data_list)} skill categories...")
    
    for data in data_list:
        cat = SkillCategory(
            slug=data['slug'],
            order=data.get('order', 0)
        )
        
        for lang, trans_data in data['translations'].items():
            trans = SkillCategoryTranslation(
                lang=lang,
                name=trans_data.get('name')
            )
            cat.translations.append(trans)
        
        db.session.add(cat)
        print(f"   ✅ {data['slug']}")


def import_skills(data_list):
    """Import skills"""
    print(f"\\n🛠️  Importing {len(data_list)} skills...")
    
    for data in data_list:
        # Find category
        category = SkillCategory.query.filter_by(slug=data.get('category_slug')).first()
        
        skill = Skill(
            slug=data['slug'],
            icon_url=data.get('icon_url'),
            proficiency=data.get('proficiency', 50),
            order=data.get('order', 0),
            is_visible_cv=data.get('is_visible_cv', True),
            category_id=category.id if category else None
        )
        
        for lang, trans_data in data['translations'].items():
            trans = SkillTranslation(
                lang=lang,
                name=trans_data.get('name'),
                description=trans_data.get('description')
            )
            skill.translations.append(trans)
        
        db.session.add(skill)
        print(f"   ✅ {data['slug']}")


def import_certifications(data_list):
    """Import certifications"""
    print(f"\\n🏆 Importing {len(data_list)} certifications...")
    
    for data in data_list:
        cert = Certification(
            slug=data['slug'],
            issuer=data['issuer'],
            issue_date=parse_date(data.get('issue_date')),
            expiry_date=parse_date(data.get('expiry_date')),
            credential_url=data.get('credential_url')
        )
        
        for lang, trans_data in data['translations'].items():
            trans = CertificationTranslation(
                lang=lang,
                title=trans_data.get('title'),
                description=trans_data.get('description')
            )
            cert.translations.append(trans)
        
        db.session.add(cert)
        print(f"   ✅ {data['slug']}")


def import_projects(data_list):
    """Import projects"""
    print(f"\\n🚀 Importing {len(data_list)} projects...")
    
    for data in data_list:
        project = Project(
            slug=data['slug'],
            category=data.get('category'),
            is_featured_cv=data.get('is_featured_cv', False)
        )
        
        # Add translations
        for lang, trans_data in data['translations'].items():
            trans = ProjectTranslation(
                lang=lang,
                title=trans_data.get('title'),
                subtitle=trans_data.get('subtitle'),
                summary=trans_data.get('summary'),
                description=trans_data.get('description'),
                cv_description=trans_data.get('cv_description'),
                content=trans_data.get('content')
            )
            project.translations.append(trans)
        
        # Add URLs
        for url_data in data.get('urls', []):
            url = ProjectURL(
                url_type=url_data.get('url_type'),
                url=url_data.get('url'),
                label=url_data.get('label'),
                order=url_data.get('order', 0)
            )
            project.urls.append(url)
        
        # Add images
        for img_data in data.get('images', []):
            img = ProjectImage(
                url=img_data.get('url'),
                type=img_data.get('type', 'image'),
                caption=img_data.get('caption'),
                order=img_data.get('order', 0),
                is_featured=img_data.get('is_featured', False),
                alt_text=img_data.get('alt_text'),
                thumbnail_url=img_data.get('thumbnail_url')
            )
            project.images.append(img)
        
        # Add tags
        for tag_name in data.get('tags', []):
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                # Generate slug from tag name
                slug = tag_name.lower().replace(' ', '-').replace('.', '').replace('+', 'plus')
                tag = Tag(name=tag_name, slug=slug)
            project.tags.append(tag)
        
        db.session.add(project)
        print(f"   ✅ {data['slug']}")


def main():
    """Main import function"""
    # Load JSON file
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'backend', 'data', 'import_template.json'
    )
    
    print(f"📂 Loading data from: {json_path}\\n")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with app.app_context():
        try:
            # Import in order (respecting dependencies)
            if 'profile' in data:
                import_profile(data['profile'])
            
            if 'experience' in data:
                import_experience(data['experience'])
            
            if 'education' in data:
                import_education(data['education'])
            
            if 'skill_categories' in data:
                import_skill_categories(data['skill_categories'])
            
            if 'skills' in data:
                import_skills(data['skills'])
            
            if 'certifications' in data:
                import_certifications(data['certifications'])
            
            if 'projects' in data:
                import_projects(data['projects'])
            
            # Commit all changes
            db.session.commit()
            print("\\n✅ Import completed successfully!\\n")
            print("🌐 View your data:")
            print("   Profile: /api/profile")
            print("   Projects: /api/projects")
            print("   CV: /cv\\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\\n❌ Import failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == '__main__':
    main()
