from uuid import uuid4

from app.models.interview_session import InterviewSession, InterviewStatus
from app.repositories.interview_session_repository import (
    InterviewSessionRepository,
)


class InterviewSessionService:
    def __init__(self, repository: InterviewSessionRepository) -> None:
        self._repository = repository

    def create_session(self) -> InterviewSession:
        interview_session = InterviewSession(
            interview_session_id=str(uuid4()),
            status=InterviewStatus.CREATED,
        )

        return self._repository.create(interview_session)