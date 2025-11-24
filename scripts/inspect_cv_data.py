"""
Quick script to inspect CV data in the database
Run with: python inspect_cv_data.py
"""

from backend import create_app, db
from backend.models.profile import Profile, ProfileTranslation
from backend.models.experience import Experience, ExperienceTranslation
from backend.models.education import Education, EducationTranslation
from backend.models.skill import Skill, SkillTranslation
from backend.models.certification import Certification, CertificationTranslation
import json

app = create_app()

with app.app_context():
    print("=" * 80)
    print("PROFILE DATA")
    print("=" * 80)
    
    profile = Profile.query.first()
    if profile:
        print(f"\nProfile: {profile.name}")
        print(f"Email: {profile.email}")
        print(f"Avatar URL: {profile.avatar_url}")
        print(f"Location: {profile.location}")
        print(f"Social Links: {profile.social_links}")
        
        print("\nTranslations:")
        for trans in profile.translations:
            print(f"\n  Language: {trans.lang}")
            print(f"  Role: {trans.role}")
            print(f"  Tagline: {trans.tagline}")
            print(f"  Bio: {trans.bio[:200] if trans.bio else 'None'}...")
    else:
        print("No profile found!")
    
    print("\n" + "=" * 80)
    print("EXPERIENCE DATA")
    print("=" * 80)
    
    experiences = Experience.query.all()
    for exp in experiences:
        print(f"\nExperience: {exp.slug}")
        print(f"Company: {exp.company}")
        print(f"Location: {exp.location}")
        print(f"Dates: {exp.start_date} to {exp.end_date}")
        
        print("\nTranslations:")
        for trans in exp.translations:
            print(f"\n  Language: {trans.lang}")
            print(f"  Title: {trans.title}")
            print(f"  Subtitle: {trans.subtitle}")
            print(f"  Description: {trans.description[:200] if trans.description else 'None'}...")
    
    print("\n" + "=" * 80)
    print("EDUCATION DATA")
    print("=" * 80)
    
    educations = Education.query.all()
    for edu in educations:
        print(f"\nEducation: {edu.slug}")
        print(f"Institution: {edu.institution}")
        print(f"Location: {edu.location}")
        print(f"Dates: {edu.start_date} to {edu.end_date}")
        
        print("\nTranslations:")
        for trans in edu.translations:
            print(f"\n  Language: {trans.lang}")
            print(f"  Title: {trans.title}")
            print(f"  Subtitle: {trans.subtitle}")
            print(f"  Description: {trans.description[:200] if trans.description else 'None'}...")
        
        print(f"\nCourses: {[c.name for c in edu.courses]}")
    
    print("\n" + "=" * 80)
    print("SKILLS DATA")
    print("=" * 80)
    
    skills = Skill.query.all()
    print(f"\nTotal skills: {len(skills)}")
    for skill in skills[:5]:  # Show first 5
        print(f"\nSkill: {skill.slug}")
        print(f"Category: {skill.category}")
        print(f"Proficiency: {skill.proficiency}")
        for trans in skill.translations:
            print(f"  {trans.lang}: {trans.name}")
    
    print("\n" + "=" * 80)
    print("CERTIFICATIONS DATA")
    print("=" * 80)
    
    certs = Certification.query.all()
    for cert in certs:
        print(f"\nCertification: {cert.slug}")
        print(f"Issuer: {cert.issuer}")
        print(f"Issue Date: {cert.issue_date}")
        
        print("\nTranslations:")
        for trans in cert.translations:
            print(f"\n  Language: {trans.lang}")
            print(f"  Title: {trans.title}")
            print(f"  Description: {trans.description[:100] if trans.description else 'None'}...")
