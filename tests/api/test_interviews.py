from unittest.mock import Mock

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.enums import DocumentType
from app.repositories.interview_document_repository import (
    InterviewDocumentRepository,
)
from app.repositories.interview_session_repository import (
    InterviewSessionRepository,
)


def test_start_interview_returns_201(
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

    assert (
        mock_document_understanding_service.understand_document.call_count
        == 2
    )