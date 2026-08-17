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
    db_session: Session,
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

    assert "session_id" in body
    assert isinstance(body["session_id"], str)
    assert body["session_id"]

    assert "question" in body
    assert isinstance(body["question"], dict)
    assert body["question"]["id"] == 1
    assert body["question"]["text"]

    mock_document_understanding_service.understand_document.assert_called()
    assert (
        mock_document_understanding_service
        .understand_document
        .call_count
        == 2
    )

    calls = (
        mock_document_understanding_service
        .understand_document
        .call_args_list
    )

    assert calls[0].kwargs["mime_type"] == "text/plain"
    assert calls[1].kwargs["mime_type"] == "text/plain"

    assert calls[0].kwargs["file_path"].exists()
    assert calls[1].kwargs["file_path"].exists()

    session_repository = InterviewSessionRepository(db_session)
    document_repository = InterviewDocumentRepository(db_session)

    session = session_repository.get_by_public_id(
        body["session_id"],
    )

    assert session is not None

    documents = document_repository.get_by_interview_session_id(
        session.id,
    )

    assert len(documents) == 2

    assert documents[0].document_type == DocumentType.CV
    assert documents[0].extracted_text == (
        "John Doe\n"
        "Senior Software Engineer\n"
        "Python, C#, AWS"
    )

    assert documents[1].document_type == DocumentType.JOB_DESCRIPTION
    assert documents[1].extracted_text == (
        "Senior Software Engineer\n"
        "Requirements\n"
        "Python, C#, AWS"
    )