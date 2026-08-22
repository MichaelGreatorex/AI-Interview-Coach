from fastapi import UploadFile

from app.services.document_service import DocumentService
from app.services.interview_session_service import InterviewSessionService
from app.services.interview_engine import InterviewEngine

from app.services.models.interview_document_processing_result import InterviewDocumentProcessingResult
from app.services.models.interview_start_result import InterviewStartResult

from app.models.enums import DocumentType
from app.models.interview_session import InterviewSession

class InterviewWorkflowService:

    def __init__(
        self,
        session_service: InterviewSessionService,
        document_service: DocumentService,
        generation_service: InterviewEngine,
    ) -> None:

        self._session_service = session_service
        self._document_service = document_service
        self._generation_service = generation_service
        
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
        session: InterviewSession,
    ) -> InterviewStartResult:

        # generate interview questions
        question = self._generation_service.get_first_question()

        return InterviewStartResult(session=session, question=question)