from io import BytesIO
from unittest.mock import Mock, call

from fastapi import UploadFile

from app.models.enums import DocumentType
from app.models.interview_session import InterviewSession, InterviewStatus
from app.schemas.interview_question import InterviewQuestion
from app.services.interview_workflow_service import InterviewWorkflowService

def create_upload_file(filename: str) -> UploadFile:
    return UploadFile(
        filename=filename,
        file=BytesIO(b"content"),
    )


def create_session() -> InterviewSession:
    return InterviewSession(
        id=1,
        interview_session_id="session-123",
        status=InterviewStatus.CREATED,
    )

def test_process_documents_creates_session_and_processes_both_documents() -> None:
    session_service = Mock()
    document_service = Mock()
    generation_service = Mock()

    session = create_session()

    cv_document = Mock()
    job_description_document = Mock()

    session_service.create_session.return_value = session

    document_service.upload_document_for_session.side_effect = [
        cv_document,
        job_description_document,
    ]

    service = InterviewWorkflowService(
        session_service=session_service,
        document_service=document_service,
        generation_service=generation_service,
    )

    cv_file = create_upload_file("cv.pdf")
    job_description_file = create_upload_file("job-description.pdf")

    result = service.process_documents(
        cv_file=cv_file,
        job_description_file=job_description_file,
    )

    session_service.create_session.assert_called_once_with()

    assert document_service.upload_document_for_session.call_args_list == [
        call(
            session=session,
            document_type=DocumentType.CV,
            file=cv_file,
        ),
        call(
            session=session,
            document_type=DocumentType.JOB_DESCRIPTION,
            file=job_description_file,
        ),
    ]

    generation_service.get_first_question.assert_not_called()

    assert result.session is session
    assert result.documents == [
        cv_document,
        job_description_document,
    ]
    
    def test_start_interview_generates_first_question() -> None:
        session_service = Mock()
        document_service = Mock()
        generation_service = Mock()

        session = create_session()

        question = InterviewQuestion(
            id=1,
            text="Tell me about yourself.",
        )

        generation_service.get_first_question.return_value = question

        service = InterviewWorkflowService(
            session_service=session_service,
            document_service=document_service,
            generation_service=generation_service,
        )

        result = service.start_interview(session=session)

        generation_service.get_first_question.assert_called_once_with()

        session_service.create_session.assert_not_called()
        document_service.upload_document_for_session.assert_not_called()

        assert result.session is session
        assert result.question is question