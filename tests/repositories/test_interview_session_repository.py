from sqlalchemy.orm import Session

from app.models.interview_session import InterviewSession, InterviewStatus
from app.repositories.interview_session_repository import InterviewSessionRepository


def test_create_and_get_by_public_id_round_trip(db_session: Session) -> None:
	repository = InterviewSessionRepository(db_session)

	created = repository.create(
		InterviewSession(
			interview_session_id="session-abc",
			status=InterviewStatus.CREATED,
		)
	)

	fetched = repository.get_by_public_id("session-abc")

	assert created.id is not None
	assert fetched is not None
	assert fetched.id == created.id
	assert fetched.status == InterviewStatus.CREATED


def test_delete_removes_session(db_session: Session) -> None:
	repository = InterviewSessionRepository(db_session)
	created = repository.create(
		InterviewSession(
			interview_session_id="session-delete",
			status=InterviewStatus.CREATED,
		)
	)

	repository.delete(created)

	assert repository.get_by_public_id("session-delete") is None
