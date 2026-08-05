from app.models.interview_response import InterviewResponse
from app.repositories.interview_response_repository import (
    InterviewResponseRepository,
)
from app.models.interview_session import InterviewSession


class InterviewResponseService:

    def __init__(
        self,
        repository: InterviewResponseRepository,
    ) -> None:
        self._repository = repository

    def save_response(
        self,
        session_id: int,
        question_id: int,
        question_text: str,
        answer: str,
    ) -> InterviewResponse:
        
        existing = self._repository.get_by_session_and_question(
            session_id,
            question_id,
        )

        if existing is not None:
            return existing

        response = InterviewResponse(
            interview_session_id=session_id,
            question_id=question_id,
            question_text=question_text,
            answer=answer,
        )

        return self._repository.create(response)

    def get_responses_for_session(
        self,
        session_id: int,
    ) -> list[InterviewResponse]:

        return self._repository.get_for_session(session_id)