
import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend import database


# Create a separate test database
@pytest.fixture
def client(tmp_path, monkeypatch):
    test_database = tmp_path / "test_careertrack.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_database
    )

    database.create_tables()

    with TestClient(app) as test_client:
        yield test_client


# TEST 1: Homepage
def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "Backend is running"


# TEST 2: Health check
def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# TEST 3: Empty database
def test_empty_applications(client):
    response = client.get("/applications")

    assert response.status_code == 200
    assert response.json() == []


# TEST 4: Create application
def test_create_application(client):
    application = {
        "company": "NVIDIA",
        "position": "Software Engineering Intern",
        "status": "Applied"
    }

    response = client.post(
        "/applications",
        json=application
    )

    assert response.status_code == 201

    applications = client.get("/applications").json()

    assert len(applications) == 1
    assert applications[0]["company"] == "NVIDIA"
    assert applications[0]["status"] == "Applied"


# TEST 5: Update application
def test_update_application(client):
    application = {
        "company": "Boeing",
        "position": "Firmware Intern",
        "status": "Saved"
    }

    client.post("/applications", json=application)

    application["status"] = "Interview"

    response = client.put(
        "/applications/1",
        json=application
    )

    assert response.status_code == 200

    applications = client.get("/applications").json()

    assert applications[0]["status"] == "Interview"


# TEST 6: Delete application
def test_delete_application(client):
    application = {
        "company": "SpaceX",
        "position": "Software Intern",
        "status": "Saved"
    }

    client.post("/applications", json=application)

    response = client.delete("/applications/1")

    assert response.status_code == 200
    assert client.get("/applications").json() == []


# TEST 7: Invalid application
def test_invalid_application(client):
    response = client.post(
        "/applications",
        json={"company": "NVIDIA"}
    )

    assert response.status_code == 422


# TEST 8: Update nonexistent application
def test_update_missing_application(client):
    response = client.put(
        "/applications/999",
        json={
            "company": "Example",
            "position": "Intern",
            "status": "Saved"
        }
    )

    assert response.status_code == 404


# TEST 9: Delete nonexistent application
def test_delete_missing_application(client):
    response = client.delete("/applications/999")

    assert response.status_code == 404


# TEST 10: Reject blank company names
def test_blank_company(client):
    response = client.post(
        "/applications",
        json={
            "company": "   ",
            "position": "Software Engineering Intern"
        }
    )

    assert response.status_code == 422
    assert client.get("/applications").json() == []


# TEST 11: Reject invalid application status
def test_invalid_status(client):
    response = client.post(
        "/applications",
        json={
            "company": "NVIDIA",
            "position": "Software Engineering Intern",
            "status": "Pending Approval"
        }
    )

    assert response.status_code == 422


# TEST 12: Reject invalid calendar date
def test_invalid_date(client):
    response = client.post(
        "/applications",
        json={
            "company": "Boeing",
            "position": "Firmware Intern",
            "date_applied": "2026-02-30"
        }
    )

    assert response.status_code == 422


# TEST 13: Reject company names that are too long
def test_company_too_long(client):
    response = client.post(
        "/applications",
        json={
            "company": "A" * 201,
            "position": "Software Engineering Intern"
        }
    )

    assert response.status_code == 422

