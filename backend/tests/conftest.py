import pytest
import os
from datetime import date

# Force SQLite before any app imports
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["RATELIMIT_ENABLED"] = "False"

from backend.app import app as flask_app
from backend import db as _db
from backend.services.cache_service import cache
from sqlalchemy.pool import StaticPool


@pytest.fixture(scope="session")
def app():
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_ENGINE_OPTIONS": {
            "poolclass": StaticPool,
            "connect_args": {"check_same_thread": False},
        },
        "RATELIMIT_ENABLED": False,
        "WTF_CSRF_ENABLED": False,
        "SERVER_NAME": "localhost",
    })

    # Recreate engine with new options
    with flask_app.app_context():
        _db.engine.dispose()

    # Disable rate limiting for tests
    from backend.utils import rate_limit
    rate_limit.limiter = None

    yield flask_app


@pytest.fixture(autouse=True)
def setup_db(app):
    """Create tables before each test, drop after. Clear cache to avoid stale responses."""
    with app.app_context():
        cache.clear()
        _db.create_all()
        yield
        _db.session.remove()
        _db.drop_all()
        cache.clear()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def seed_data(app):
    """Seed minimal test data for all entity types."""
    from backend.models.profile import Profile, ProfileTranslation
    from backend.models.project import Project, ProjectTranslation, ProjectImage
    from backend.models.project_url import ProjectURL
    from backend.models.experience import Experience, ExperienceTranslation
    from backend.models.education import Education, EducationTranslation, Course
    from backend.models.skill import Skill, SkillTranslation, SkillCategory, SkillCategoryTranslation
    from backend.models.certification import Certification, CertificationTranslation
    from backend.models.tag import Tag

    # Profile
    profile = Profile(slug="test-profile", name="Test User", email="test@example.com",
                      location={"city": "Madrid", "country": "Spain"},
                      avatar_url="https://example.com/avatar.jpg",
                      social_links={"github": "https://github.com/test"})
    profile.translations.append(ProfileTranslation(lang="es", role="Ingeniero", tagline="Hola", bio="Bio en español"))
    profile.translations.append(ProfileTranslation(lang="en", role="Engineer", tagline="Hello", bio="Bio in English"))
    _db.session.add(profile)

    # Tag
    tag = Tag(name="Python", slug="python")
    _db.session.add(tag)

    # Project
    project = Project(slug="test-project", category="project", is_featured_cv=True)
    project.translations.append(ProjectTranslation(
        lang="es", title="Proyecto Test", subtitle="Subtítulo",
        description="<p>Descripción</p>", summary="Resumen", content={}
    ))
    project.translations.append(ProjectTranslation(
        lang="en", title="Test Project", subtitle="Subtitle",
        description="<p>Description</p>", summary="Summary", content={}
    ))
    project.images.append(ProjectImage(url="https://example.com/img.jpg", type="image", order=0, is_featured=True))
    project.urls.append(ProjectURL(url_type="github", url="https://github.com/test/project", order=0))
    project.tags.append(tag)
    _db.session.add(project)

    # Experience
    exp = Experience(slug="test-exp", company="TestCo", location="Madrid",
                     start_date=date(2023, 1, 1), end_date=None, current=True)
    exp.translations.append(ExperienceTranslation(lang="es", title="TestCo", subtitle="Dev", description="- Logro 1\n- Logro 2"))
    exp.translations.append(ExperienceTranslation(lang="en", title="TestCo", subtitle="Dev", description="- Achievement 1\n- Achievement 2"))
    _db.session.add(exp)

    # Education
    edu = Education(slug="test-edu", institution="Test University", location="Madrid",
                    start_date=date(2020, 9, 1), end_date=date(2024, 6, 1), current=False)
    edu.translations.append(EducationTranslation(lang="es", title="Grado", subtitle="Informática", description="Desc"))
    edu.translations.append(EducationTranslation(lang="en", title="Degree", subtitle="CS", description="Desc"))
    edu.courses.append(Course(name="Algorithms", order=0))
    _db.session.add(edu)

    # Skill Category
    cat = SkillCategory(slug="languages", order=0)
    cat.translations.append(SkillCategoryTranslation(lang="es", name="Lenguajes"))
    cat.translations.append(SkillCategoryTranslation(lang="en", name="Languages"))
    _db.session.add(cat)
    _db.session.flush()

    # Skill
    skill = Skill(slug="python", icon_url="/svg/python.svg", proficiency=90,
                   category_id=cat.id, is_visible_cv=True, is_visible_portfolio=True, order=0)
    skill.translations.append(SkillTranslation(lang="es", name="Python", description="Lenguaje"))
    skill.translations.append(SkillTranslation(lang="en", name="Python", description="Language"))
    _db.session.add(skill)

    # Certification
    cert = Certification(slug="test-cert", issuer="TestOrg",
                         issue_date=date(2024, 1, 1), credential_url="https://example.com/cert")
    cert.translations.append(CertificationTranslation(lang="es", title="Certificación", description="Desc ES"))
    cert.translations.append(CertificationTranslation(lang="en", title="Certification", description="Desc EN"))
    _db.session.add(cert)

    _db.session.commit()

    return {
        "profile": profile,
        "project": project,
        "experience": exp,
        "education": edu,
        "skill": skill,
        "skill_category": cat,
        "certification": cert,
        "tag": tag,
    }
