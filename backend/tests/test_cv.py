"""Tests for CV generation from database models."""


def test_build_cv_from_models_es(client, seed_data):
    """Test CV generation in Spanish."""
    from backend.routes.cv import build_cv_from_models

    cv = build_cv_from_models(lang="es")
    assert cv is not None
    assert cv["basics"]["name"] == "Test User"
    assert cv["basics"]["email"] == "test@example.com"
    assert len(cv["work"]) >= 1
    assert len(cv["education"]) >= 1
    assert len(cv["skills"]) >= 1


def test_build_cv_from_models_en(client, seed_data):
    """Test CV generation in English."""
    from backend.routes.cv import build_cv_from_models

    cv = build_cv_from_models(lang="en")
    assert cv is not None
    assert cv["basics"]["label"] == "Engineer"
    assert len(cv["languages"]) == 2


def test_build_cv_no_profile(client):
    """Test CV generation with no profile returns None."""
    from backend.routes.cv import build_cv_from_models

    cv = build_cv_from_models(lang="es")
    assert cv is None


def test_build_cv_certifications(client, seed_data):
    """Test that certifications are included in CV."""
    from backend.routes.cv import build_cv_from_models

    cv = build_cv_from_models(lang="en")
    assert "certifications" in cv
    assert len(cv["certifications"]) >= 1
    assert cv["certifications"][0]["title"] == "Certification"


def test_build_cv_work_experience_format(client, seed_data):
    """Test work experience format in CV."""
    from backend.routes.cv import build_cv_from_models

    cv = build_cv_from_models(lang="en")
    work = cv["work"]
    assert len(work) >= 1
    entry = work[0]
    assert "company" in entry
    assert "position" in entry
    assert "startDate" in entry
    assert "highlights" in entry


def test_build_cv_education_format(client, seed_data):
    """Test education format in CV."""
    from backend.routes.cv import build_cv_from_models

    cv = build_cv_from_models(lang="en")
    edu = cv["education"]
    assert len(edu) >= 1
    entry = edu[0]
    assert "institution" in entry
    assert "studyType" in entry
    assert "courses" in entry
    assert "Algorithms" in entry["courses"]


def test_build_cv_skills_categories(client, seed_data):
    """Test skills are grouped by category in CV."""
    from backend.routes.cv import build_cv_from_models

    cv = build_cv_from_models(lang="en")
    skills = cv["skills"]
    assert len(skills) >= 1
    assert skills[0]["name"] == "Languages"
    assert "Python" in skills[0]["keywords"]


def test_cv_view_endpoint(client, seed_data):
    """Test the /cv HTML view endpoint."""
    response = client.get("/cv?lang=en")
    assert response.status_code == 200


def test_cv_view_no_data(client):
    """Test /cv endpoint with no profile data."""
    response = client.get("/cv?lang=es")
    assert response.status_code == 404
