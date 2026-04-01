"""Tests for all public API endpoints."""


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "services" in data


def test_api_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


# --- Projects ---

def test_get_projects_empty(client):
    response = client.get("/api/projects?lang=es")
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_projects_es(client, seed_data):
    response = client.get("/api/projects?lang=es")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Proyecto Test"
    assert data[0]["slug"] == "test-project"
    assert "Python" in data[0]["tags"]


def test_get_projects_en(client, seed_data):
    response = client.get("/api/projects?lang=en")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Project"


def test_get_project_by_slug(client, seed_data):
    response = client.get("/api/projects/test-project?lang=en")
    assert response.status_code == 200
    data = response.get_json()
    assert data["slug"] == "test-project"
    assert data["title"] == "Test Project"
    assert len(data["urls"]) == 1
    assert len(data["images"]) == 1


def test_get_project_not_found(client, seed_data):
    response = client.get("/api/projects/nonexistent")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] is True
    assert data["status"] == 404


# --- Experience ---

def test_get_experience(client, seed_data):
    response = client.get("/api/experience?lang=es")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["slug"] == "test-exp"
    assert data[0]["current"] is True


def test_get_experience_en(client, seed_data):
    response = client.get("/api/experience?lang=en")
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["description"] == "- Achievement 1\n- Achievement 2"


# --- Education ---

def test_get_education(client, seed_data):
    response = client.get("/api/education?lang=es")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["institution"] == "Test University"
    assert "Algorithms" in data[0]["courses"]


def test_get_education_en(client, seed_data):
    response = client.get("/api/education?lang=en")
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["title"] == "Degree"
    assert data[0]["subtitle"] == "CS"


# --- Skills ---

def test_get_skills(client, seed_data):
    response = client.get("/api/skills?lang=es")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Python"
    assert data[0]["proficiency"] == 90
    assert data[0]["category"] == "Lenguajes"


def test_get_skills_en(client, seed_data):
    response = client.get("/api/skills?lang=en")
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["category"] == "Languages"


# --- Certifications ---

def test_get_certifications(client, seed_data):
    response = client.get("/api/certifications?lang=es")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["issuer"] == "TestOrg"
    assert data[0]["title"] == "Certificación"


def test_get_certifications_en(client, seed_data):
    response = client.get("/api/certifications?lang=en")
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["title"] == "Certification"


# --- Profile ---

def test_get_profile(client, seed_data):
    response = client.get("/api/profile?lang=es")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Test User"
    assert data["role"] == "Ingeniero"


def test_get_profile_en(client, seed_data):
    response = client.get("/api/profile?lang=en")
    assert response.status_code == 200
    data = response.get_json()
    assert data["role"] == "Engineer"
    assert data["tagline"] == "Hello"


def test_get_profile_not_found(client):
    response = client.get("/api/profile?lang=es")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] is True


# --- Error format consistency ---

def test_404_api_error_format(client):
    response = client.get("/api/nonexistent-endpoint")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] is True
    assert data["status"] == 404
    assert "message" in data
