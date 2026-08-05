from io import BytesIO
from unittest.mock import Mock, call

from fastapi import UploadFile

from app.models.enums import DocumentType
from app.models.interview_session import InterviewSession, InterviewStatus
from app.services.interview_workflow_service import InterviewWorkflowService
from app.services.models.interview_question import InterviewQuestion


def create_upload_file(filename: str) -> UploadFile:
	return UploadFile(
		filename=filename,
		file=BytesIO(b"content"),
		headers={"content-type": "text/plain"},
	)


def test_start_interview_creates_session_uploads_documents_and_returns_question() -> None:
	session_service = Mock()
	document_service = Mock()
	generation_service = Mock()
	session = InterviewSession(
		id=3,
		interview_session_id="session-123",
		status=InterviewStatus.CREATED,
	)
	question = InterviewQuestion(id=1, text="Tell me about yourself.")
	cv_file = create_upload_file("cv.txt")
	job_description_file = create_upload_file("job.txt")

	session_service.create_session.return_value = session
	generation_service.get_first_question.return_value = question

	service = InterviewWorkflowService(
		session_service=session_service,
		document_service=document_service,
		generation_service=generation_service,
	)

	result = service.start_interview(
		cv_file=cv_file,
		job_description_file=job_description_file,
	)

	session_service.create_session.assert_called_once_with()
	assert document_service.upload_document_for_session.call_args_list == [
		call(session=session, document_type=DocumentType.CV, file=cv_file),
		call(
			session=session,
			document_type=DocumentType.JOB_DESCRIPTION,
			file=job_description_file,
		),
	]
	generation_service.get_first_question.assert_called_once_with()
	assert result.session is session
	assert result.question is question
