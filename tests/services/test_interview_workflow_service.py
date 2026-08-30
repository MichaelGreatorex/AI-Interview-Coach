from io import BytesIO
from unittest.mock import Mock, call

from fastapi import UploadFile

from app.models.enums import DocumentType
from app.models.interview_session import InterviewSession, InterviewStatus
from app.schemas.interview_question import InterviewQuestion
from app.services.interview_workflow_service import InterviewWorkflowService
from app.storage.upload_preparer import UploadPreparer
from app.storage.prepared_upload import PreparedUpload


def create_upload_file(
    filename: str,
    content_type: str = "application/pdf",
) -> UploadFile:
    return UploadFile(
        filename=filename,
        file=BytesIO(b"content"),
        headers={"content-type": content_type},
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
    interview_engine = Mock()
    response_service = Mock()
    document_upload_validator = Mock()
    upload_preparer = Mock(spec=UploadPreparer)

    session = create_session()

    cv_document = Mock()
    job_description_document = Mock()

    session_service.create_session.return_value = session

    document_service.upload_document_for_session.side_effect = [
        cv_document,
        job_description_document,
    ]

    cv_file = create_upload_file("cv.pdf")
    job_description_file = create_upload_file("job-description.pdf")

    cv_upload = PreparedUpload(
        filename="cv.pdf",
        content_type="application/pdf",
        content=b"content",
    )

    job_description_upload = PreparedUpload(
        filename="job-description.pdf",
        content_type="application/pdf",
        content=b"content",
    )

    upload_preparer.prepare.side_effect = [
        cv_upload,
        job_description_upload,
    ]

    service = InterviewWorkflowService(
        session_service=session_service,
        document_service=document_service,
        response_service=response_service,
        interview_engine=interview_engine,
        document_upload_validator=document_upload_validator,
        upload_preparer=upload_preparer,
    )

    result = service.process_documents(
        cv_file=cv_file,
        job_description_file=job_description_file,
    )

    session_service.create_session.assert_called_once_with()

    assert upload_preparer.prepare.call_args_list == [
        call(cv_file),
        call(job_description_file),
    ]

    assert document_upload_validator.validate.call_args_list == [
        call(cv_upload),
        call(job_description_upload),
    ]

    assert document_service.upload_document_for_session.call_args_list == [
        call(
            session=session,
            document_type=DocumentType.CV,
            upload=cv_upload,
        ),
        call(
            session=session,
            document_type=DocumentType.JOB_DESCRIPTION,
            upload=job_description_upload,
        ),
    ]

    interview_engine.get_first_question.assert_not_called()

    assert result.session is session
    assert result.documents == [
        cv_document,
        job_description_document,
    ]


def test_start_interview_generates_first_question() -> None:
    session_service = Mock()
    document_service = Mock()
    response_service = Mock()
    interview_engine = Mock()
    document_upload_validator = Mock()
    upload_preparer = Mock(spec=UploadPreparer)

    session = create_session()

    session_service.get_by_public_id.return_value = session

    question = InterviewQuestion(
        id=1,
        text="Tell me about yourself.",
    )

    interview_engine.get_first_question.return_value = question

    service = InterviewWorkflowService(
        session_service=session_service,
        document_service=document_service,
        response_service=response_service,
        interview_engine=interview_engine,
        document_upload_validator=document_upload_validator,
        upload_preparer=upload_preparer,
    )

    result = service.start_interview(
        interview_session_id=session.interview_session_id,
    )

    session_service.get_by_public_id.assert_called_once_with(
        session.interview_session_id,
    )

    interview_engine.get_first_question.assert_called_once_with()

    session_service.activate_session.assert_called_once_with(session)

    session_service.create_session.assert_not_called()
    document_service.upload_document_for_session.assert_not_called()
    response_service.save_response.assert_not_called()

    assert result.session is session
    assert result.question is question