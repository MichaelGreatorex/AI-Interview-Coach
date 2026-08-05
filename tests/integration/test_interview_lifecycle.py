from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.repositories.interview_document_repository import InterviewDocumentRepository
from app.repositories.interview_response_repository import InterviewResponseRepository
from app.repositories.interview_session_repository import InterviewSessionRepository


def test_interview_lifecycle_persists_response_and_cleans_up_session(
	client: TestClient,
	db_session: Session,
) -> None:
	start_response = client.post(
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

	assert start_response.status_code == 201
	start_body = start_response.json()

	session_repository = InterviewSessionRepository(db_session)
	document_repository = InterviewDocumentRepository(db_session)
	response_repository = InterviewResponseRepository(db_session)

	session = session_repository.get_by_public_id(start_body["session_id"])

	assert session is not None
	session_id = session.id
	public_id = session.interview_session_id

	stored_documents = document_repository.get_by_interview_session_id(session_id)
	assert len(stored_documents) == 2
	stored_paths = [Path(document.storage_path) for document in stored_documents]
	assert all(path.exists() for path in stored_paths)

	submit_response = client.post(
		f"/api/v1/sessions/{public_id}/responses",
		json={
			"question_id": start_body["question"]["id"],
			"question_text": start_body["question"]["text"],
			"answer": "I have led several backend projects.",
		},
	)

	assert submit_response.status_code == 201
	assert len(response_repository.get_for_session(session_id)) == 1

	delete_response = client.delete(f"/api/v1/sessions/{public_id}")

	assert delete_response.status_code == 204

	db_session.expire_all()

	assert session_repository.get_by_public_id(public_id) is None
	assert document_repository.get_by_interview_session_id(session_id) == []
	assert response_repository.get_for_session(session_id) == []
	assert all(not path.exists() for path in stored_paths)
