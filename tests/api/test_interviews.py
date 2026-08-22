from unittest.mock import Mock

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.enums import DocumentType
from app.models.interview_session import InterviewStatus, InterviewSession
from app.repositories.interview_document_repository import (
    InterviewDocumentRepository,
)
from app.repositories.interview_session_repository import (
    InterviewSessionRepository,
)


def test_process_documents_returns_processed_documents(
    ai_test_client: TestClient,
    db_session: Session,
    mock_document_understanding_service: Mock,
) -> None:
    mock_document_understanding_service.understand_document.side_effect = [
        Mock(
            document_type=DocumentType.CV,
            extracted_text="Peter Parker CV content",
        ),
        Mock(
            document_type=DocumentType.JOB_DESCRIPTION,
            extracted_text="Software engineer role requirements",
        ),
    ]

    response = ai_test_client.post(
        "/api/v1/interviews",
        files={
            "cv": (
                "peter-parker-cv.txt",
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
    assert cv["original_filename"] == "peter-parker-cv.txt"

    assert job_description["document_type"] == "job_description"
    assert job_description["original_filename"] == "job-description.txt"

    assert (
        mock_document_understanding_service.understand_document.call_count
        == 2
    )

    session_repository = InterviewSessionRepository(db_session)
    document_repository = InterviewDocumentRepository(db_session)

    session = session_repository.get_by_public_id(body["session_id"])

    assert session is not None
    assert session.status == InterviewStatus.CREATED

    documents = document_repository.get_by_interview_session_id(session.id)

    assert len(documents) == 2

    assert documents[0].extracted_text == "Peter Parker CV content"
    assert documents[1].extracted_text == (
        "Software engineer role requirements"
    )
    
def test_start_interview_returns_first_question(
    ai_test_client: TestClient,
    db_session: Session,
) -> None:
    session_repository = InterviewSessionRepository(db_session)

    session = session_repository.create(
        InterviewSession(
            interview_session_id="session-start-api",
            status=InterviewStatus.CREATED,
        )
    )

    response = ai_test_client.post(
        f"/api/v1/interviews/{session.interview_session_id}/start",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["session_id"] == session.interview_session_id
    assert body["question"]["id"] == 1
    assert body["question"]["text"]

    db_session.expire_all()

    refreshed_session = session_repository.get_by_public_id(
        session.interview_session_id,
    )

    assert refreshed_session is not None
    assert refreshed_session.status == InterviewStatus.ACTIVE