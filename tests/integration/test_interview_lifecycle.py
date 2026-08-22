from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.interview_session import InterviewStatus
from app.repositories.interview_document_repository import (
    InterviewDocumentRepository,
)
from app.repositories.interview_response_repository import (
    InterviewResponseRepository,
)
from app.repositories.interview_session_repository import (
    InterviewSessionRepository,
)


def test_interview_lifecycle_persists_responses_and_cleans_up_session(
    ai_test_client: TestClient,
    db_session: Session,
) -> None:
    # 1. Upload and process the documents.
    process_response = ai_test_client.post(
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

    assert process_response.status_code == 201

    process_body = process_response.json()

    assert process_body["session_id"]
    assert len(process_body["documents"]) == 2

    session_repository = InterviewSessionRepository(db_session)
    document_repository = InterviewDocumentRepository(db_session)
    response_repository = InterviewResponseRepository(db_session)

    # 2. Verify the session and documents were persisted.
    session = session_repository.get_by_public_id(
        process_body["session_id"],
    )

    assert session is not None
    assert session.status == InterviewStatus.CREATED

    session_id = session.id
    public_id = session.interview_session_id

    stored_documents = document_repository.get_by_interview_session_id(
        session_id,
    )

    assert len(stored_documents) == 2
    assert all(document.extracted_text for document in stored_documents)

    stored_paths = [
        Path(document.storage_path)
        for document in stored_documents
    ]

    assert all(path.exists() for path in stored_paths)

    # 3. Start the interview.
    start_response = ai_test_client.post(
        f"/api/v1/interviews/{public_id}/start",
    )

    assert start_response.status_code == 200

    start_body = start_response.json()

    assert start_body["session_id"] == public_id
    assert start_body["question"]["id"] == 1
    assert start_body["question"]["text"]

    db_session.expire_all()

    session = session_repository.get_by_public_id(public_id)

    assert session is not None
    assert session.status == InterviewStatus.ACTIVE

    # 4. Submit all three interview responses.
    question = start_body["question"]

    answers = {
        1: "I have led several backend projects.",
        2: "I designed and implemented a distributed system.",
        3: "I resolved a difficult technical challenge by breaking it down.",
    }

    for question_id in (1, 2, 3):
        submit_response = ai_test_client.post(
            f"/api/v1/sessions/{public_id}/responses",
            json={
                "question_id": question["id"],
                "question_text": question["text"],
                "answer": answers[question_id],
            },
        )

        assert submit_response.status_code == 200

        submit_body = submit_response.json()

        if question_id < 3:
            assert submit_body["interview_complete"] is False
            assert submit_body["next_question"] is not None
            assert submit_body["next_question"]["id"] == question_id + 1

            question = submit_body["next_question"]

        else:
            assert submit_body["interview_complete"] is True
            assert submit_body["next_question"] is None

    # 5. Verify all three responses were persisted and the interview completed.
    stored_responses = response_repository.get_for_session(
        session_id,
    )

    assert len(stored_responses) == 3
    assert [response.question_id for response in stored_responses] == [1, 2, 3]

    assert stored_responses[0].answer == (
        "I have led several backend projects."
    )

    assert stored_responses[1].answer == (
        "I designed and implemented a distributed system."
    )

    assert stored_responses[2].answer == (
        "I resolved a difficult technical challenge by breaking it down."
    )

    db_session.expire_all()

    session = session_repository.get_by_public_id(public_id)

    assert session is not None
    assert session.status == InterviewStatus.COMPLETED

    # 6. Delete the interview session.
    delete_response = ai_test_client.delete(
        f"/api/v1/sessions/{public_id}",
    )

    assert delete_response.status_code == 204

    # 7. Verify everything belonging to the interview was cleaned up.
    db_session.expire_all()

    assert session_repository.get_by_public_id(public_id) is None
    assert document_repository.get_by_interview_session_id(session_id) == []
    assert response_repository.get_for_session(session_id) == []
    assert all(not path.exists() for path in stored_paths)