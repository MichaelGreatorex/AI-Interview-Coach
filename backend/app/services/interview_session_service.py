from uuid import uuid4

from app.models.interview_session import InterviewSession
from app.repositories.interview_session_repository import (
    InterviewSessionRepository,
)
from app.schemas.interview_session import CreateInterviewSessionRequest


class InterviewSessionService:
    def __init__(self, repository: InterviewSessionRepository):
        self._repository = repository

    def create_session(
        self,
        request: CreateInterviewSessionRequest,
    ) -> InterviewSession:
        interview_session = InterviewSession(
            interview_session_id=str(uuid4()),
            candidate_name=request.candidate_name,
            job_title=request.job_title,
            status="created",
        )

        return self._repository.create(interview_session)