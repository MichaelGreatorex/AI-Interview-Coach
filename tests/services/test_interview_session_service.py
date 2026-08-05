from uuid import UUID
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.models.interview_session import InterviewSession, InterviewStatus
from app.services.interview_session_service import InterviewSessionService


def create_session() -> InterviewSession:
	return InterviewSession(
		id=11,
		interview_session_id="session-123",
		status=InterviewStatus.CREATED,
	)


def test_create_session_generates_public_id_and_persists_created_status() -> None:
	repository = Mock()
	document_service = Mock()
	repository.create.side_effect = lambda interview_session: interview_session

	service = InterviewSessionService(
		repository=repository,
		document_service=document_service,
	)

	created = service.create_session()

	repository.create.assert_called_once()
	persisted = repository.create.call_args.args[0]

	UUID(persisted.interview_session_id)
	assert persisted.status == InterviewStatus.CREATED
	assert created is persisted


def test_get_by_public_id_returns_repository_result() -> None:
	repository = Mock()
	document_service = Mock()
	expected = create_session()
	repository.get_by_public_id.return_value = expected

	service = InterviewSessionService(
		repository=repository,
		document_service=document_service,
	)

	session = service.get_by_public_id("session-123")

	repository.get_by_public_id.assert_called_once_with("session-123")
	assert session is expected


def test_delete_session_removes_documents_then_deletes_session() -> None:
	repository = Mock()
	document_service = Mock()
	session = create_session()
	repository.get_by_public_id.return_value = session

	service = InterviewSessionService(
		repository=repository,
		document_service=document_service,
	)

	service.delete_session("session-123")

	document_service.delete_documents_for_session.assert_called_once_with(session)
	repository.delete.assert_called_once_with(session)


def test_delete_session_raises_404_when_session_does_not_exist() -> None:
	repository = Mock()
	document_service = Mock()
	repository.get_by_public_id.return_value = None

	service = InterviewSessionService(
		repository=repository,
		document_service=document_service,
	)

	with pytest.raises(HTTPException) as exc_info:
		service.delete_session("missing-session")

	assert exc_info.value.status_code == 404
	assert exc_info.value.detail == "Interview session 'missing-session' does not exist"
	document_service.delete_documents_for_session.assert_not_called()
	repository.delete.assert_not_called()
