from sqlalchemy.orm import Session

from app.models.interview_response import InterviewResponse
from app.models.interview_session import InterviewSession, InterviewStatus
from app.repositories.interview_response_repository import InterviewResponseRepository
from app.repositories.interview_session_repository import InterviewSessionRepository


def create_session(db_session: Session, public_id: str) -> InterviewSession:
	return InterviewSessionRepository(db_session).create(
		InterviewSession(
			interview_session_id=public_id,
			status=InterviewStatus.CREATED,
		)
	)


def test_create_and_get_for_session_return_saved_responses(db_session: Session) -> None:
	session = create_session(db_session, "session-responses")
	repository = InterviewResponseRepository(db_session)

	first_response = repository.create(
		InterviewResponse(
			interview_session_id=session.id,
			question_id=1,
			question_text="Tell me about yourself.",
			answer="First answer",
		)
	)
	second_response = repository.create(
		InterviewResponse(
			interview_session_id=session.id,
			question_id=2,
			question_text="Why this role?",
			answer="Second answer",
		)
	)

	responses = repository.get_for_session(session.id)

	assert [response.id for response in responses] == [first_response.id, second_response.id]
	assert [response.question_id for response in responses] == [1, 2]


def test_delete_for_session_removes_only_target_session_responses(
	db_session: Session,
) -> None:
	target_session = create_session(db_session, "target-session")
	other_session = create_session(db_session, "other-session")
	repository = InterviewResponseRepository(db_session)

	repository.create(
		InterviewResponse(
			interview_session_id=target_session.id,
			question_id=1,
			question_text="Tell me about yourself.",
			answer="Target answer",
		)
	)
	repository.create(
		InterviewResponse(
			interview_session_id=other_session.id,
			question_id=2,
			question_text="Why this role?",
			answer="Other answer",
		)
	)

	repository.delete_for_session(target_session.id)

	assert repository.get_for_session(target_session.id) == []
	remaining = repository.get_for_session(other_session.id)
	assert len(remaining) == 1
	assert remaining[0].answer == "Other answer"
