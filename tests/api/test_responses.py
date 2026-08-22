from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

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


def test_submit_interview_response_returns_200(client: TestClient, db_session: Session) -> None:
	session = create_session(db_session, "session-response-api")

	response = client.post(
		f"/api/v1/sessions/{session.interview_session_id}/responses",
		json={
			"question_id": 1,
			"question_text": "Tell me about yourself.",
			"answer": "I am a software engineer.",
		},
	)

	assert response.status_code == 200

	body = response.json()
	assert body["interview_complete"] is False
	assert isinstance(body["next_question"], dict)
	assert isinstance(body["next_question"]["id"], int)
	assert body["next_question"]["text"]


def test_submit_interview_response_validates_request_body(client: TestClient) -> None:
	response = client.post(
		"/api/v1/sessions/any-session/responses",
		json={
			"question_id": 1,
			"question_text": "Tell me about yourself.",
		},
	)

	assert response.status_code == 422
 
def test_save_response_returns_existing_response_if_already_present(client: TestClient, db_session: Session) -> None:
	session = create_session(db_session, "session-response-api-duplicate")
	response_repository = InterviewResponseRepository(db_session)

	# Submit the first response
	response1 = client.post(
		f"/api/v1/sessions/{session.interview_session_id}/responses",
		json={
			"question_id": 1,
			"question_text": "Tell me about yourself.",
			"answer": "I am a software engineer.",
		},
	)

	assert response1.status_code == 200
	body1 = response1.json()

	# Submit the same response again
	response2 = client.post(
		f"/api/v1/sessions/{session.interview_session_id}/responses",
		json={
			"question_id": 1,
			"question_text": "Tell me about yourself.",
			"answer": "I am a software engineer.",
		},
	)

	assert response2.status_code == 200
	body2 = response2.json()

	assert body1["interview_complete"] is False
	assert body2["interview_complete"] is False

	# Duplicate submissions are idempotent and should not create extra rows.
	persisted_responses = response_repository.get_for_session(session.id)
	assert len(persisted_responses) == 1
	assert persisted_responses[0].question_id == 1

def test_submit_interview_responses_progress_through_interview(
    client: TestClient,
    db_session: Session,
) -> None:
    session = create_session(
        db_session,
        "session-response-lifecycle",
    )

    session_id = session.interview_session_id

    response_1 = client.post(
        f"/api/v1/sessions/{session_id}/responses",
        json={
            "question_id": 1,
            "question_text": "Tell me about yourself.",
            "answer": "I am a software engineer.",
        },
    )

    assert response_1.status_code == 200

    body_1 = response_1.json()

    assert body_1["interview_complete"] is False
    assert body_1["next_question"]["id"] == 2

    response_2 = client.post(
        f"/api/v1/sessions/{session_id}/responses",
        json={
            "question_id": 2,
            "question_text": body_1["next_question"]["text"],
            "answer": "I designed a distributed system.",
        },
    )

    assert response_2.status_code == 200

    body_2 = response_2.json()

    assert body_2["interview_complete"] is False
    assert body_2["next_question"]["id"] == 3

    response_3 = client.post(
        f"/api/v1/sessions/{session_id}/responses",
        json={
            "question_id": 3,
            "question_text": body_2["next_question"]["text"],
            "answer": "I handled a difficult technical challenge.",
        },
    )

    assert response_3.status_code == 200

    body_3 = response_3.json()

    assert body_3["interview_complete"] is True
    assert body_3["next_question"] is None
    
    response_repository = InterviewResponseRepository(db_session)
    session_repository = InterviewSessionRepository(db_session)

    persisted_responses = response_repository.get_for_session(
        session.id,
    )

    assert len(persisted_responses) == 3
    assert [r.question_id for r in persisted_responses] == [1, 2, 3]

    db_session.expire_all()

    refreshed_session = session_repository.get_by_public_id(
        session_id,
    )

    assert refreshed_session is not None
    assert refreshed_session.status == InterviewStatus.COMPLETED