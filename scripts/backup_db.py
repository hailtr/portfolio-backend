"""
Database backup script for Railway PostgreSQL
Creates a JSON backup of all portfolio data
"""
import json
import os
from datetime import datetime
from backend.models import db, Project, Experience, Education, Skill, Certification, Profile
from backend import create_app

def backup_database():
    """Create a JSON backup of all database tables"""
    app = create_app()
    
    with app.app_context():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backup_{timestamp}.json'
        
        backup_data = {
            'timestamp': timestamp,
            'projects': [],
            'experiences': [],
            'education': [],
            'skills': [],
            'certifications': [],
            'profile': None
        }
        
        # Backup Projects
        for p in Project.query.all():
            backup_data['projects'].append({
                'id': p.id,
                'slug': p.slug,
                'category': p.category,
                'url': p.url,
                'created_at': p.created_at.isoformat() if p.created_at else None,
                'translations': [{
                    'lang': t.lang,
                    'title': t.title,
                    'subtitle': t.subtitle,
                    'description': t.description,
                    'summary': t.summary,
                    'content': t.content
                } for t in p.translations],
                'images': [{
                    'url': img.url,
                    'type': img.type,
                    'caption': img.caption,
                    'order': img.order
                } for img in p.images],
                'tags': [{'name': tag.name, 'slug': tag.slug} for tag in p.tags]
            })
        
        # Backup Experiences
        for e in Experience.query.all():
            backup_data['experiences'].append({
                'id': e.id,
                'slug': e.slug,
                'company': e.company,
                'location': e.location,
                'start_date': e.start_date.isoformat() if e.start_date else None,
                'end_date': e.end_date.isoformat() if e.end_date else None,
                'current': e.current,
                'translations': [{
                    'lang': t.lang,
                    'title': t.title,
                    'description': t.description
                } for t in e.translations],
                'tags': [{'name': tag.name} for tag in e.tags]
            })
        
        # Backup Education
        for edu in Education.query.all():
            backup_data['education'].append({
                'id': edu.id,
                'slug': edu.slug,
                'institution': edu.institution,
                'location': edu.location,
                'start_date': edu.start_date.isoformat() if edu.start_date else None,
                'end_date': edu.end_date.isoformat() if edu.end_date else None,
                'courses': edu.courses,
                'translations': [{
                    'lang': t.lang,
                    'title': t.title,
                    'description': t.description
                } for t in edu.translations]
            })
        
        # Backup Skills
        for s in Skill.query.all():
            backup_data['skills'].append({
                'id': s.id,
                'name': s.name,
                'category': s.category,
                'proficiency': s.proficiency,
                'icon_url': s.icon_url
            })
        
        # Backup Certifications
        for c in Certification.query.all():
            backup_data['certifications'].append({
                'id': c.id,
                'slug': c.slug,
                'issuer': c.issuer,
                'issue_date': c.issue_date.isoformat() if c.issue_date else None,
                'expiry_date': c.expiry_date.isoformat() if c.expiry_date else None,
                'credential_url': c.credential_url,
                'translations': [{
                    'lang': t.lang,
                    'title': t.title,
                    'description': t.description
                } for t in c.translations]
            })
        
        # Backup Profile
        profile = Profile.query.first()
        if profile:
            backup_data['profile'] = {
                'id': profile.id,
                'name': profile.name,
                'email': profile.email,
                'location': profile.location,
                'social_links': profile.social_links,
                'translations': [{
                    'lang': t.lang,
                    'role': t.role,
                    'tagline': t.tagline,
                    'bio': t.bio
                } for t in profile.translations]
            }
        
        # Save to file
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Backup created successfully: {backup_file}")
        print(f"   Projects: {len(backup_data['projects'])}")
        print(f"   Experiences: {len(backup_data['experiences'])}")
        print(f"   Education: {len(backup_data['education'])}")
        print(f"   Skills: {len(backup_data['skills'])}")
        print(f"   Certifications: {len(backup_data['certifications'])}")
        
        return backup_file

if __name__ == '__main__':
    backup_database()
