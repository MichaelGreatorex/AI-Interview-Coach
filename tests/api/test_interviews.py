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
from app.models.interview_document import InterviewDocument


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


def test_update_document_text_returns_200(
    ai_test_client: TestClient,
    db_session: Session,
) -> None:
    session_repository = InterviewSessionRepository(db_session)
    document_repository = InterviewDocumentRepository(db_session)

    session = session_repository.create(
        InterviewSession(
            interview_session_id="session-update-document-api",
            status=InterviewStatus.CREATED,
        )
    )

    document = document_repository.create(
        InterviewDocument(
            interview_session_id=session.id,
            document_type=DocumentType.CV,
            original_filename="cv.txt",
            stored_filename="stored-cv.txt",
            mime_type="text/plain",
            file_size=42,
            storage_path="/tmp/stored-cv.txt",
            extracted_text="Old text",
        )
    )

    response = ai_test_client.patch(
        (
            f"/api/v1/interviews/{session.interview_session_id}"
            f"/documents/{document.id}"
        ),
        json={
            "extracted_text": "Updated text from inspect view",
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["id"] == document.id
    assert body["extracted_text"] == "Updated text from inspect view"

    db_session.expire_all()
    updated = document_repository.get_by_id(document.id)

    assert updated is not None
    assert updated.extracted_text == "Updated text from inspect view"


def test_update_document_text_rejects_document_from_another_session(
    ai_test_client: TestClient,
    db_session: Session,
) -> None:
    session_repository = InterviewSessionRepository(db_session)
    document_repository = InterviewDocumentRepository(db_session)

    owner_session = session_repository.create(
        InterviewSession(
            interview_session_id="session-owner",
            status=InterviewStatus.CREATED,
        )
    )

    other_session = session_repository.create(
        InterviewSession(
            interview_session_id="session-other",
            status=InterviewStatus.CREATED,
        )
    )

    document = document_repository.create(
        InterviewDocument(
            interview_session_id=owner_session.id,
            document_type=DocumentType.CV,
            original_filename="cv.txt",
            stored_filename="stored-cv.txt",
            mime_type="text/plain",
            file_size=42,
            storage_path="/tmp/stored-cv.txt",
            extracted_text="Owner text",
        )
    )

    response = ai_test_client.patch(
        (
            f"/api/v1/interviews/{other_session.interview_session_id}"
            f"/documents/{document.id}"
        ),
        json={
            "extracted_text": "Should be rejected",
        },
    )

    assert response.status_code == 404
    assert "does not belong to interview session" in response.json()["detail"]
    
    db_session.expire_all()

    unchanged = document_repository.get_by_id(document.id)

    assert unchanged is not None
    assert unchanged.extracted_text == "Owner text"

    
def test_update_document_text_returns_404_for_missing_document(
    ai_test_client: TestClient,
    db_session: Session,
) -> None:
    session_repository = InterviewSessionRepository(db_session)

    session = session_repository.create(
        InterviewSession(
            interview_session_id="session-missing-document",
            status=InterviewStatus.CREATED,
        )
    )

    response = ai_test_client.patch(
        (
            f"/api/v1/interviews/{session.interview_session_id}"
            "/documents/999999"
        ),
        json={
            "extracted_text": "Should not be saved",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == ("Interview document '999999' does not exist")