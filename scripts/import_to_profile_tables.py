"""
Import portfolio data directly to Profile/Experience/Education/Skill/Certification tables
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app, db
from backend.models.profile import Profile, ProfileTranslation
from backend.models.experience import Experience, ExperienceTranslation
from backend.models.education import Education, EducationTranslation, Course
from backend.models.skill import Skill, SkillTranslation
from backend.models.certification import Certification, CertificationTranslation
from datetime import datetime

def import_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with app.app_context():
        print("Starting import...")
        
        # Import Profile
        print("\n[1/5] Importing Profile...")
        profile_data = data.get('profile', {})
        profile = Profile.query.first()
        if not profile:
            profile = Profile(slug='rafael-ortiz-profile')
            db.session.add(profile)
        
        profile.name = profile_data.get('name')
        profile.email = profile_data.get('email')
        profile.location = profile_data.get('location')
        profile.social_links = profile_data.get('social')
        
        # Clear existing translations
        for trans in profile.translations:
            db.session.delete(trans)
        db.session.flush()  # Flush to ensure deletions are processed
        
        # Add translations
        for lang, trans_data in profile_data.get('translations', {}).items():
            trans = ProfileTranslation(
                profile=profile,
                lang=lang,
                role=trans_data.get('role'),
                tagline=trans_data.get('tagline'),
                bio=trans_data.get('summary')
            )
            db.session.add(trans)
        
        print(f"  Profile: {profile.name}")
        
        # Import Experience
        print("\n[2/5] Importing Experience...")
        for exp_data in data.get('work_experience', []):
            exp = Experience.query.filter_by(slug=exp_data['slug']).first()
            if not exp:
                exp = Experience(slug=exp_data['slug'])
                db.session.add(exp)
            
            exp.company = exp_data.get('company')
            exp.location = exp_data.get('location')
            
            # Parse dates
            start_str = exp_data.get('startDate', '')
            end_str = exp_data.get('endDate', '')
            
            if start_str:
                try:
                    exp.start_date = datetime.strptime(start_str, '%Y-%m').date()
                except:
                    pass
            
            if end_str:
                try:
                    exp.end_date = datetime.strptime(end_str, '%Y-%m').date()
                except:
                    pass
            
            # Clear existing translations
            for trans in exp.translations:
                db.session.delete(trans)
            db.session.flush()
            
            # Add translations
            for lang, trans_data in exp_data.get('translations', {}).items():
                # Combine summary and highlights into description
                summary = trans_data.get('summary', '')
                highlights = trans_data.get('highlights', [])
                
                description_parts = []
                if summary:
                    description_parts.append(summary)
                if highlights:
                    description_parts.append('')  # Empty line
                    for highlight in highlights:
                        description_parts.append(f"- {highlight}")
                
                description = '\n'.join(description_parts)
                
                trans = ExperienceTranslation(
                    experience=exp,
                    lang=lang,
                    title=exp_data.get('company'),  # Company name in title
                    subtitle=trans_data.get('position'),  # Role in subtitle
                    description=description
                )
                db.session.add(trans)
            
            print(f"  {exp.slug}")
        
        # Import Education
        print("\n[3/5] Importing Education...")
        for edu_data in data.get('education', []):
            edu = Education.query.filter_by(slug=edu_data['slug']).first()
            if not edu:
                edu = Education(slug=edu_data['slug'])
                db.session.add(edu)
            
            edu.institution = edu_data.get('institution')
            edu.location = edu_data.get('location')
            edu.current = edu_data.get('current', False)
            
            # Parse dates
            start_str = edu_data.get('startDate', '')
            end_str = edu_data.get('endDate', '')
            
            if start_str:
                try:
                    edu.start_date = datetime.strptime(start_str, '%Y-%m').date()
                except:
                    pass
            
            if end_str:
                try:
                    edu.end_date = datetime.strptime(end_str, '%Y-%m').date()
                except:
                    pass
            
            # Clear existing translations and courses
            for trans in edu.translations:
                db.session.delete(trans)
            for course in edu.courses:
                db.session.delete(course)
            db.session.flush()
            
            # Add courses
            for idx, course_name in enumerate(edu_data.get('courses', [])):
                course = Course(education=edu, name=course_name, order=idx)
                db.session.add(course)
            
            # Add translations
            for lang, trans_data in edu_data.get('translations', {}).items():
                trans = EducationTranslation(
                    education=edu,
                    lang=lang,
                    title=trans_data.get('studyType'),  # Degree
                    subtitle=trans_data.get('area'),  # Field of study
                    description=''
                )
                db.session.add(trans)
            
            print(f"  {edu.slug}")
        
        # Import Skills
        print("\n[4/5] Importing Skills...")
        for idx, skill_data in enumerate(data.get('skills', [])):
            skill = Skill.query.filter_by(slug=skill_data['slug']).first()
            if not skill:
                skill = Skill(slug=skill_data['slug'])
                db.session.add(skill)
            
            skill.category = skill_data.get('category')
            skill.proficiency = 90 if skill_data.get('level') == 'advanced' else (70 if skill_data.get('level') == 'intermediate' else 50)
            skill.order = idx
            
            # Clear existing translations
            for trans in skill.translations:
                db.session.delete(trans)
            db.session.flush()
            
            # Add translations (same name for all languages)
            for lang in ['es', 'en']:
                trans = SkillTranslation(
                    skill=skill,
                    lang=lang,
                    name=skill_data.get('name')
                )
                db.session.add(trans)
            
            print(f"  {skill_data.get('name')}")
        
        # Import Certifications
        print("\n[5/5] Importing Certifications...")
        for cert_data in data.get('certifications', []):
            cert = Certification.query.filter_by(slug=cert_data['slug']).first()
            if not cert:
                cert = Certification(slug=cert_data['slug'])
                db.session.add(cert)
            
            cert.issuer = cert_data.get('issuer')
            cert.credential_url = cert_data.get('credential_url')
            
            # Parse date
            issue_str = cert_data.get('issue_date', '')
            if issue_str:
                try:
                    cert.issue_date = datetime.strptime(issue_str, '%Y-%m').date()
                except:
                    pass
            
            # Clear existing translations
            for trans in cert.translations:
                db.session.delete(trans)
            db.session.flush()
            
            # Add translations
            for lang, trans_data in cert_data.get('translations', {}).items():
                trans = CertificationTranslation(
                    certification=cert,
                    lang=lang,
                    title=trans_data.get('title'),
                    description=trans_data.get('description')
                )
                db.session.add(trans)
            
            print(f"  {cert.slug}")
        
        # Commit
        print("\nCommitting to database...")
        db.session.commit()
        print("\nImport complete!")
        print("\nCheck your CV at: http://localhost:5000/cv")

if __name__ == '__main__':
    import_data('backend/data/portfolio_normalized.json')
