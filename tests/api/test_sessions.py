from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.interview_session import InterviewSession, InterviewStatus
from app.repositories.interview_session_repository import InterviewSessionRepository


def test_delete_session_returns_204_and_removes_session(
	client: TestClient,
	db_session: Session,
) -> None:
	repository = InterviewSessionRepository(db_session)
	session = repository.create(
		InterviewSession(
			interview_session_id="session-delete-api",
			status=InterviewStatus.CREATED,
		)
	)
	public_id = session.interview_session_id

	response = client.delete(f"/api/v1/sessions/{public_id}")

	db_session.expire_all()

	assert response.status_code == 204
	assert repository.get_by_public_id(public_id) is None


def test_delete_session_returns_404_for_missing_session(client: TestClient) -> None:
	response = client.delete("/api/v1/sessions/missing-session")

	assert response.status_code == 404
	assert response.json() == {
		"detail": "Interview session 'missing-session' does not exist",
	}
