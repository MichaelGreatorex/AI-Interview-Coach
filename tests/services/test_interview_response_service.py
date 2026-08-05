from unittest.mock import Mock

from app.models.interview_response import InterviewResponse
from app.services.interview_response_service import (
    InterviewResponseService,
)

def test_save_response_creates_response() -> None:

    repository = Mock()

    expected = InterviewResponse(
        interview_session_id=1,
        question_id=1,
        question_text="Tell me about yourself",
        answer="My answer",
    )

    repository.create.return_value = expected
    repository.get_by_session_and_question.return_value = None

    service = InterviewResponseService(repository)

    response = service.save_response(
        session_id=1,
        question_id=1,
        question_text="Tell me about yourself",
        answer="My answer",
    )

    repository.create.assert_called_once()

    created = repository.create.call_args.args[0]

    assert created.interview_session_id == 1
    assert created.question_id == 1
    assert created.question_text == "Tell me about yourself"
    assert created.answer == "My answer"

    assert response is expected
    
def test_get_responses_for_session_returns_repository_result() -> None:

    repository: Mock = Mock()

    expected = [
        Mock(spec=InterviewResponse),
        Mock(spec=InterviewResponse),
    ]

    repository.get_for_session.return_value = expected

    service = InterviewResponseService(repository)

    responses = service.get_responses_for_session(123)

    repository.get_for_session.assert_called_once_with(123)

    assert responses == expected