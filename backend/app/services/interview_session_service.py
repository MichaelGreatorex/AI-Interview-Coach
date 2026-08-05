from uuid import uuid4
from fastapi import HTTPException, status

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

    def get_by_public_id(
        self,
        interview_session_id: str,
    ) -> InterviewSession | None:

        return self._repository.get_by_public_id(
            interview_session_id,
        )

    def delete_session(
        self,
        interview_session_id: str,
    ) -> None:

        session = self.get_by_public_id(
            interview_session_id,
        )

        if session is None:
            raise HTTPException(
                status_code=404,
                detail=f"Interview session '{interview_session_id}' does not exist",
            )

        self._document_service.delete_documents_for_session(
            session,
        )

        self._repository.delete(
            session,
        )