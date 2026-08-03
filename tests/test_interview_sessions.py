import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_interview_session_returns_201():
    response = client.post(
        "/api/v1/interview-sessions",
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
        "/api/v1/interview-sessions",
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


def test_upload_document_to_session_returns_201():
    create_session_response = client.post(
        "/api/v1/sessions",
        json={"candidate_name": "Jane Doe", "job_title": "Data Scientist"},
    )

    assert create_session_response.status_code == 201

    session = create_session_response.json()["session"]
    session_id = session["interview_session_id"]

    upload_response = client.post(
        f"/api/v1/sessions/{session_id}/documents",
        data={"document_type": "cv"},
        files={"file": ("resume.txt", b"Experienced Python engineer", "text/plain")},
    )

    assert upload_response.status_code == 201

    body = upload_response.json()
    assert "document" in body

    document = body["document"]
    assert document["document_type"] == "cv"
    assert document["original_filename"] == "resume.txt"
    assert document["mime_type"] == "text/plain"
    assert document["file_size"] == len(b"Experienced Python engineer")
    assert document["interview_session_id"] > 0
    assert document["stored_filename"]
    assert document["created_at"] is not None
    assert document["updated_at"] is not None