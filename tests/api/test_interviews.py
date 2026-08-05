from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_start_interview_returns_201():
    response = client.post(
        "/api/v1/interviews",
        files={
            "cv": ("cv.txt", b"candidate cv content", "text/plain"),
            "job_description": (
                "job-description.txt",
                b"role requirements",
                "text/plain",
            ),
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert "session_id" in body
    assert isinstance(body["session_id"], str)
    assert body["session_id"]
    assert "question" in body
    assert isinstance(body["question"], dict)
    assert body["question"]["id"] == 1
    assert body["question"]["text"]
