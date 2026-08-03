import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_interview_session_returns_201():
    response = client.post(
        "/api/v1/sessions",
        json={},
    )

    assert response.status_code == 201

    body = response.json()

    assert "session" in body

    session = body["session"]

    assert session["status"] == "created"
    assert session["candidate_name"] is None
    assert session["job_title"] is None
    assert session["created_at"] is not None

    # Validate that a UUID was returned
    uuid.UUID(session["interview_session_id"])
    
def test_create_interview_session_with_candidate_name_and_job_title_returns_201():
    response = client.post(
        "/api/v1/sessions",
        json={"candidate_name": "John Doe", "job_title": "Software Engineer"},
    )

    assert response.status_code == 201

    body = response.json()

    assert "session" in body

    session = body["session"]

    assert session["status"] == "created"
    assert session["candidate_name"] == "John Doe"
    assert session["job_title"] == "Software Engineer"
    assert session["created_at"] is not None

    # Validate that a UUID was returned
    uuid.UUID(session["interview_session_id"])