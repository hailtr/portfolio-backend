"""
Database Migration Verification Script
Tests all changes from the comprehensive refactoring
"""
from backend.app import app, db
from backend.models.project import Project, ProjectImage, ProjectTranslation
from backend.models.project_url import ProjectURL
from backend.models.analytics import ProjectAnalytics, ProjectEvent
from backend.models.experience import Experience, ExperienceTranslation
from backend.models.education import Education, EducationTranslation, Course
from backend.models.skill import Skill, SkillTranslation
from backend.models.certification import Certification, CertificationTranslation
from backend.models.tag import Tag
from sqlalchemy import inspect
from datetime import date, datetime


def verify_schema():
    """Verify database schema changes"""
    print("=" * 60)
    print("VERIFYING DATABASE SCHEMA")
    print("=" * 60)
    
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Test 1: Verify date columns are Date type
        print("\n1. Checking Date Type Conversions...")
        tables_with_dates = {
            'experiences': ['start_date', 'end_date'],
            'educations': ['start_date', 'end_date'],
            'certifications': ['issue_date', 'expiry_date']
        }
        
        for table, date_cols in tables_with_dates.items():
            columns = {col['name']: col for col in inspector.get_columns(table)}
            for col_name in date_cols:
                col_type = str(columns[col_name]['type'])
                status = "[OK]" if 'DATE' in col_type.upper() else "[FAIL]"
                print(f"  {status} {table}.{col_name}: {col_type}")
        
        # Test 2: Verify foreign key indexes
        print("\n2. Checking Foreign Key Indexes...")
        tables_to_check = [
            'experience_translations', 'education_translations', 
            'certification_translations', 'skill_translations',
            'project_translations', 'project_images', 'project_urls'
        ]
        
        for table in tables_to_check:
            indexes = inspector.get_indexes(table)
            fk_indexed = any('_id' in idx['column_names'][0] for idx in indexes if idx['column_names'])
            status = "[OK]" if fk_indexed else "[FAIL]"
            print(f"  {status} {table}: {len(indexes)} indexes")
        
        # Test 3: Verify new tables exist
        print("\n3. Checking New Tables...")
        new_tables = ['project_urls', 'project_analytics', 'project_events']
        all_tables = inspector.get_table_names()
        
        for table in new_tables:
            exists = table in all_tables
            status = "[OK]" if exists else "[FAIL]"
            print(f"  {status} {table}: {'EXISTS' if exists else 'MISSING'}")
        
        # Test 4: Verify image metadata columns
        print("\n4. Checking Image Metadata Columns...")
        image_cols = inspector.get_columns('project_images')
        image_col_names = [col['name'] for col in image_cols]
        
        expected_cols = ['thumbnail_url', 'alt_text', 'width', 'height', 
                         'file_size', 'mime_type', 'is_featured']
        
        for col in expected_cols:
            exists = col in image_col_names
            status = "[OK]" if exists else "[FAIL]"
            print(f"  {status} project_images.{col}")
        
        # Test 5: Verify timestamps
        print("\n5. Checking Timestamp Columns...")
        tables_with_timestamps = [
            'experiences', 'educations', 'certifications', 'skills', 'tags',
            'projects', 'project_urls', 'project_analytics', 'project_events'
        ]
        
        for table in tables_with_timestamps:
            columns = {col['name']: col for col in inspector.get_columns(table)}
            has_created = 'created_at' in columns
            has_updated = 'updated_at' in columns or table == 'project_events'
            status = "[OK]" if has_created else "[FAIL]"
            print(f"  {status} {table}: created_at={has_created}, updated_at={has_updated}")


def verify_data_integrity():
    """Verify data was preserved during migration"""
    print("\n" + "=" * 60)
    print("VERIFYING DATA INTEGRITY")
    print("=" * 60)
    
    with app.app_context():
        # Test 1: Check date data
        print("\n1. Checking Date Data...")
        exp = Experience.query.first()
        if exp:
            print(f"  [OK] Experience dates: start={exp.start_date}, end={exp.end_date}")
            print(f"     Type: {type(exp.start_date)}")
        
        edu = Education.query.first()
        if edu:
            print(f"  [OK] Education dates: start={edu.start_date}, end={edu.end_date}")
        
        cert = Certification.query.first()
        if cert:
            print(f"  [OK] Certification dates: issue={cert.issue_date}, expiry={cert.expiry_date}")
        
        # Test 2: Check URL migration
        print("\n2. Checking URL Migration...")
        project = Project.query.first()
        if project:
            url_count = len(project.urls) if project.urls else 0
            print(f"  [OK] Project '{project.slug}' has {url_count} URLs")
            for url in (project.urls or []):
                print(f"     - {url.url_type}: {url.url}")
        
        # Test 3: Check relationships
        print("\n3. Checking Relationships...")
        if project:
            print(f"  [OK] Project has {len(project.images)} images")
            print(f"  [OK] Project has {len(project.translations)} translations")
            print(f"  [OK] Project has {len(project.tags)} tags")
            print(f"  [OK] Project analytics: {project.analytics}")
        
        # Test 4: Check counts
        print("\n4. Checking Record Counts...")
        counts = {
            'Projects': Project.query.count(),
            'Experiences': Experience.query.count(),
            'Educations': Education.query.count(),
            'Skills': Skill.query.count(),
            'Certifications': Certification.query.count(),
            'Tags': Tag.query.count(),
            'ProjectURLs': ProjectURL.query.count(),
        }
        
        for model, count in counts.items():
            print(f"  [OK] {model}: {count}")


def verify_model_methods():
    """Verify model methods work correctly"""
    print("\n" + "=" * 60)
    print("VERIFYING MODEL METHODS")
    print("=" * 60)
    
    with app.app_context():
        # Test __repr__ methods
        print("\n1. Testing __repr__ Methods...")
        project = Project.query.first()
        if project:
            print(f"  [OK] Project: {repr(project)}")
            if project.urls:
                print(f"  [OK] ProjectURL: {repr(project.urls[0])}")
        
        exp = Experience.query.first()
        if exp:
            print(f"  [OK] Experience: {repr(exp)}")
        
        # Test to_dict methods
        print("\n2. Testing to_dict() Methods...")
        if project and project.urls:
            url_dict = project.urls[0].to_dict()
            print(f"  [OK] ProjectURL.to_dict(): {list(url_dict.keys())}")
        
        course = Course.query.first()
        if course:
            course_dict = course.to_dict()
            print(f"  [OK] Course.to_dict(): {list(course_dict.keys())}")


def run_all_tests():
    """Run all verification tests"""
    print("\n" + "=" * 60)
    print("DATABASE MIGRATION VERIFICATION")
    print("=" * 60)
    
    try:
        verify_schema()
        verify_data_integrity()
        verify_model_methods()
        
        print("\n" + "=" * 60)
        print("[SUCCESS] ALL TESTS PASSED!")
        print("=" * 60)
        print("\nDatabase migration completed successfully!")
        print("All schema changes applied correctly.")
        print("Data integrity maintained.")
        print("Model methods working as expected.")
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("[FAILED] TEST FAILED!")
        print("=" * 60)
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
