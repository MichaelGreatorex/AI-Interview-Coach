from uuid import uuid4
from fastapi import HTTPException, status

from app.schemas.submit_interview_response_response import SubmitInterviewResponseResponse

from app.services.interview_response_service import InterviewResponseService
from app.services.interview_engine import InterviewEngine
from app.services.document_service import DocumentService

from app.models.interview_start_result import InterviewStartResult
from app.models.interview_session import InterviewSession, InterviewStatus

from app.repositories.interview_session_repository import InterviewSessionRepository


class InterviewSessionService:

    def __init__(
        self,
        repository: InterviewSessionRepository,
        document_service: DocumentService,
        response_service: InterviewResponseService | None = None,
        interview_engine: InterviewEngine | None = None,
    ) -> None:
        self._repository = repository
        self._response_service = response_service
        self._interview_engine = interview_engine
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
        
    def submit_response(
        self,
        interview_session_id: str,
        request,
    ) -> SubmitInterviewResponseResponse:

        session = self.get_by_public_id(
            interview_session_id,
        )

        if session is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Interview session '{interview_session_id}' does not exist",
            )

        self._response_service.save_response(
            session.id,
            request.question_id,
            request.question_text,
            request.answer,
        )

        responses = self._response_service.get_responses_for_session(
            session.id,
        )
        
        print(
            "DEBUG:",
            {
                "session_id": session.id,
                "response_count": len(responses),
                "response_question_ids": [r.question_id for r in responses],
                "available_question_ids": [q.id for q in self._interview_engine.questions],
            }
        )


        next_question = self._interview_engine.get_next_question(
            responses,
        )
        
        print(
            "DEBUG NEXT QUESTION:",
            next_question,
        )

        if next_question is None:
            session.status = InterviewStatus.COMPLETED
            self._repository.update(session)

            return SubmitInterviewResponseResponse(
                interview_complete=True,
                next_question=None,
            )

        session.status = InterviewStatus.ACTIVE
        self._repository.update(session)

        return SubmitInterviewResponseResponse(
            interview_complete=False,
            next_question=next_question,
        )