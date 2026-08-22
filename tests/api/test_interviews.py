from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.models.enums import DocumentType

from app.repositories.interview_document_repository import InterviewDocumentRepository
from app.repositories.interview_session_repository import InterviewSessionRepository

from app.db.session import get_db


def test_process_documents_returns_processed_documents(
    ai_test_client: TestClient,
    mock_document_understanding_service: Mock,
) -> None:
    response = ai_test_client.post(
        "/api/v1/interviews",
        files={
            "cv": (
                "cv.txt",
                b"candidate cv content",
                "text/plain",
            ),
            "job_description": (
                "job-description.txt",
                b"role requirements",
                "text/plain",
            ),
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["session_id"]
    assert len(body["documents"]) == 2

    cv = body["documents"][0]
    job_description = body["documents"][1]

    assert cv["document_type"] == "cv"
    assert cv["original_filename"] == "cv.txt"
    assert cv["extracted_text"] == (
        "John Doe\n"
        "Senior Software Engineer\n"
        "Python, C#, AWS"
    )

    assert job_description["document_type"] == "job_description"
    assert job_description["original_filename"] == "job-description.txt"
    assert job_description["extracted_text"] == (
        "Senior Software Engineer\n"
        "Requirements\n"
        "Python, C#, AWS"
    )

    assert (
        mock_document_understanding_service.understand_document.call_count
        == 2
    )