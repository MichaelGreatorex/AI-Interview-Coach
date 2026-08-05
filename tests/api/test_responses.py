from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.interview_session import InterviewSession, InterviewStatus
from app.repositories.interview_session_repository import InterviewSessionRepository


def create_session(db_session: Session, public_id: str) -> InterviewSession:
	return InterviewSessionRepository(db_session).create(
		InterviewSession(
			interview_session_id=public_id,
			status=InterviewStatus.CREATED,
		)
	)


def test_submit_interview_response_returns_201(client: TestClient, db_session: Session) -> None:
	session = create_session(db_session, "session-response-api")

	response = client.post(
		f"/api/v1/sessions/{session.interview_session_id}/responses",
		json={
			"question_id": 1,
			"question_text": "Tell me about yourself.",
			"answer": "I am a software engineer.",
		},
	)

	assert response.status_code == 201

	body = response.json()
	assert isinstance(body["id"], int)
	assert body["question_id"] == 1
	assert body["question_text"] == "Tell me about yourself."
	assert body["answer"] == "I am a software engineer."
	assert body["created_at"]


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

	# Submit the first response
	response1 = client.post(
		f"/api/v1/sessions/{session.interview_session_id}/responses",
		json={
			"question_id": 1,
			"question_text": "Tell me about yourself.",
			"answer": "I am a software engineer.",
		},
	)

	assert response1.status_code == 201
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

	assert response2.status_code == 201
	body2 = response2.json()

	# The second response should return the existing response
	assert body1["id"] == body2["id"]
