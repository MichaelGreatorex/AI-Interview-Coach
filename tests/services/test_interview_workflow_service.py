from io import BytesIO
from unittest.mock import Mock

import pytest
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


def test_start_interview_creates_session_and_processes_both_documents() -> None:
    session_service = Mock()
    document_service = Mock()
    generation_service = Mock()

    session = create_session()
    session_service.create_session.return_value = session

    generation_service.get_first_question.return_value = InterviewQuestion(
        id=1,
        text="Tell me about yourself.",
    )

    cv_file = create_upload_file("cv.pdf")
    job_description_file = create_upload_file("job-description.pdf")

    workflow_service = InterviewWorkflowService(
        session_service=session_service,
        document_service=document_service,
        generation_service=generation_service,
    )

    result = workflow_service.start_interview(
        cv_file=cv_file,
        job_description_file=job_description_file,
    )

    session_service.create_session.assert_called_once_with()

    assert document_service.upload_document_for_session.call_count == 2

    calls = document_service.upload_document_for_session.call_args_list

    assert calls[0].kwargs["session"] is session
    assert calls[0].kwargs["file"] is cv_file

    assert calls[1].kwargs["session"] is session
    assert calls[1].kwargs["file"] is job_description_file

    generation_service.get_first_question.assert_called_once_with()

    assert result.session is session
    assert result.question.id == 1
    assert result.question.text == "Tell me about yourself."


def test_start_interview_does_not_generate_question_when_document_processing_fails() -> None:
    session_service = Mock()
    document_service = Mock()
    generation_service = Mock()

    session = create_session()
    session_service.create_session.return_value = session

    document_service.upload_document_for_session.side_effect = ValueError(
        "Document understanding failed",
    )

    workflow_service = InterviewWorkflowService(
        session_service=session_service,
        document_service=document_service,
        generation_service=generation_service,
    )

    with pytest.raises(
        ValueError,
        match="Document understanding failed",
    ):
        workflow_service.start_interview(
            cv_file=create_upload_file("cv.pdf"),
            job_description_file=create_upload_file("job.pdf"),
        )

    generation_service.get_first_question.assert_not_called()


def test_start_interview_does_not_process_second_document_if_first_fails() -> None:
    session_service = Mock()
    document_service = Mock()
    generation_service = Mock()

    session = create_session()
    session_service.create_session.return_value = session

    document_service.upload_document_for_session.side_effect = ValueError(
        "Document understanding failed",
    )

    workflow_service = InterviewWorkflowService(
        session_service=session_service,
        document_service=document_service,
        generation_service=generation_service,
    )

    with pytest.raises(
        ValueError,
        match="Document understanding failed",
    ):
        workflow_service.start_interview(
            cv_file=create_upload_file("cv.pdf"),
            job_description_file=create_upload_file("job.pdf"),
        )

    assert document_service.upload_document_for_session.call_count == 1
    generation_service.get_first_question.assert_not_called()


def test_start_interview_passes_upload_field_types_to_document_service() -> None:
    session_service = Mock()
    document_service = Mock()
    generation_service = Mock()

    session = create_session()
    session_service.create_session.return_value = session

    generation_service.get_first_question.return_value = InterviewQuestion(
        id=1,
        text="Tell me about yourself.",
    )

    cv_file = create_upload_file("cv.pdf")
    job_description_file = create_upload_file("job.pdf")

    workflow_service = InterviewWorkflowService(
        session_service=session_service,
        document_service=document_service,
        generation_service=generation_service,
    )

    workflow_service.start_interview(
        cv_file=cv_file,
        job_description_file=job_description_file,
    )

    calls = document_service.upload_document_for_session.call_args_list

    assert calls[0].kwargs["document_type"] == DocumentType.CV
    assert calls[1].kwargs["document_type"] == DocumentType.JOB_DESCRIPTION