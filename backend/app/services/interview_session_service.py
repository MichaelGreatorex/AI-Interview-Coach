from uuid import uuid4

from app.models.interview_session import InterviewSession, InterviewStatus
from app.repositories.interview_session_repository import (
    InterviewSessionRepository,
)
from app.services.document_service import DocumentService


class InterviewSessionService:
    
    def __init__(
        self,
        repository: InterviewSessionRepository,
        document_service: DocumentService,
    ):
        self._repository = repository
        self._document_service = document_service

    def create_session(self) -> InterviewSession:
        interview_session = InterviewSession(
            interview_session_id=str(uuid4()),
            status=InterviewStatus.CREATED,
        )

        return self._repository.create(interview_session)
    
    def delete_session(
        self,
        interview_session_id: str,
    ) -> None:

        session = self._repository.get_by_public_id(
            interview_session_id,
        )

        # idempotent delete: if the session does not exist, we do nothing
        if session is None:
            return

        self._document_service.delete_documents_for_session(
            session,
        )

        self._repository.delete(
            session,
        )