from fastapi import UploadFile
from fastapi import HTTPException, status

from app.models.enums import DocumentType
from app.models.interview_session import InterviewSession

from app.schemas.submit_interview_response_request import (
    SubmitInterviewResponseRequest,
)

from app.services.document_service import DocumentService
from app.services.interview_engine import InterviewEngine
from app.services.interview_response_service import InterviewResponseService
from app.services.interview_session_service import InterviewSessionService

from app.services.models.interview_document_processing_result import (
    InterviewDocumentProcessingResult,
)
from app.services.models.interview_start_result import InterviewStartResult

from app.schemas.submit_interview_response_response import (
    SubmitInterviewResponseResponse,
)


class InterviewWorkflowService:

    def __init__(
        self,
        session_service: InterviewSessionService,
        document_service: DocumentService,
        response_service: InterviewResponseService,
        interview_engine: InterviewEngine,
    ) -> None:
        self._session_service = session_service
        self._document_service = document_service
        self._response_service = response_service
        self._interview_engine = interview_engine

    def process_documents(
        self,
        cv_file: UploadFile,
        job_description_file: UploadFile,
    ) -> InterviewDocumentProcessingResult:

        session = self._session_service.create_session()

        cv_document = self._document_service.upload_document_for_session(
            session=session,
            document_type=DocumentType.CV,
            file=cv_file,
        )

        job_description_document = (
            self._document_service.upload_document_for_session(
                session=session,
                document_type=DocumentType.JOB_DESCRIPTION,
                file=job_description_file,
            )
        )

        return InterviewDocumentProcessingResult(
            session=session,
            documents=[
                cv_document,
                job_description_document,
            ],
        )

    def start_interview(
        self,
        interview_session_id: str,
    ) -> InterviewStartResult:
        session = self._session_service.get_by_public_id(
            interview_session_id,
        )

        if session is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Interview session "
                    f"'{interview_session_id}' does not exist"
                ),
            )

        question = self._interview_engine.get_first_question()

        if question is None:
            raise ValueError(
                "No interview questions are configured",
            )

        self._session_service.activate_session(session)

        return InterviewStartResult(
            session=session,
            question=question,
        )

    def submit_response(
        self,
        interview_session_id: str,
        request: SubmitInterviewResponseRequest,
    ) -> SubmitInterviewResponseResponse:

        session = self._session_service.get_by_public_id(
            interview_session_id,
        )

        if session is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Interview session "
                    f"'{interview_session_id}' does not exist"
                ),
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

        next_question = self._interview_engine.get_next_question(
            responses,
        )

        if next_question is None:
            self._session_service.complete_session(session)

            return SubmitInterviewResponseResponse(
                interview_complete=True,
                next_question=None,
            )

        self._session_service.activate_session(session)

        return SubmitInterviewResponseResponse(
            interview_complete=False,
            next_question=next_question,
        )