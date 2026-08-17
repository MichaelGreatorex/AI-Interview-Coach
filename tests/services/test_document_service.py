from io import BytesIO
from pathlib import Path
from unittest.mock import Mock, call

import pytest
from fastapi import UploadFile

from app.ai.models import AiDocumentType, AiDocumentUnderstandingResult
from app.models.enums import DocumentType
from app.models.interview_document import InterviewDocument
from app.models.interview_session import InterviewSession, InterviewStatus
from app.services.document_service import DocumentService
from app.storage.models import StoredFile


def create_upload_file(filename: str = "cv.pdf") -> UploadFile:
    return UploadFile(
        filename=filename,
        file=BytesIO(b"file content"),
        headers={"content-type": "application/pdf"},
    )


def create_session() -> InterviewSession:
    return InterviewSession(
        id=7,
        interview_session_id="session-123",
        status=InterviewStatus.CREATED,
    )


def test_upload_document_raises_when_session_is_missing() -> None:
    session_repository = Mock()
    document_repository = Mock()
    storage_provider = Mock()
    document_understanding_service = Mock()

    session_repository.get_by_public_id.return_value = None

    service = DocumentService(
        session_repository=session_repository,
        document_repository=document_repository,
        storage_provider=storage_provider,
        document_understanding_service=document_understanding_service,
    )

    with pytest.raises(
        ValueError,
        match="Interview session 'missing-session' does not exist",
    ):
        service.upload_document(
            interview_session_id="missing-session",
            document_type=DocumentType.CV,
            file=create_upload_file(),
        )

    storage_provider.store.assert_not_called()
    document_repository.create.assert_not_called()
    document_understanding_service.understand_document.assert_not_called()


def test_upload_document_for_session_stores_file_and_persists_metadata() -> None:
    session_repository = Mock()
    document_repository = Mock()
    storage_provider = Mock()
    document_understanding_service = Mock()

    upload = create_upload_file()
    session = create_session()

    storage_provider.store.return_value = StoredFile(
        original_filename="cv.pdf",
        stored_filename="stored-cv.pdf",
        storage_path="/tmp/stored-cv.pdf",
        mime_type="application/pdf",
        file_size=12,
    )

    document_understanding_service.understand_document.return_value = (
        AiDocumentUnderstandingResult(
            document_type=AiDocumentType.CV,
            extracted_text="Extracted document text",
        )
    )

    document_repository.create.side_effect = (
        lambda interview_document: interview_document
    )

    service = DocumentService(
        session_repository=session_repository,
        document_repository=document_repository,
        storage_provider=storage_provider,
        document_understanding_service=document_understanding_service,
    )

    created = service.upload_document_for_session(
        session=session,
        document_type=DocumentType.CV,
        file=upload,
    )

    storage_provider.store.assert_called_once_with(upload)

    document_understanding_service.understand_document.assert_called_once_with(
        file_path=Path("/tmp/stored-cv.pdf"),
        mime_type="application/pdf",
    )

    document_repository.create.assert_called_once()

    persisted = document_repository.create.call_args.args[0]

    assert persisted.interview_session_id == session.id
    assert persisted.document_type == DocumentType.CV
    assert persisted.original_filename == "cv.pdf"
    assert persisted.stored_filename == "stored-cv.pdf"
    assert persisted.mime_type == "application/pdf"
    assert persisted.file_size == 12
    assert persisted.storage_path == "/tmp/stored-cv.pdf"
    assert persisted.extracted_text == "Extracted document text"

    assert created is persisted


def test_delete_documents_for_session_deletes_files_and_records() -> None:
    session_repository = Mock()
    document_repository = Mock()
    storage_provider = Mock()
    document_understanding_service = Mock()

    session = create_session()

    documents = [
        InterviewDocument(
            id=1,
            interview_session_id=session.id,
            document_type=DocumentType.CV,
            original_filename="cv.pdf",
            stored_filename="stored-cv.pdf",
            mime_type="application/pdf",
            file_size=12,
            storage_path="/tmp/stored-cv.pdf",
        ),
        InterviewDocument(
            id=2,
            interview_session_id=session.id,
            document_type=DocumentType.JOB_DESCRIPTION,
            original_filename="job.pdf",
            stored_filename="stored-job.pdf",
            mime_type="application/pdf",
            file_size=24,
            storage_path="/tmp/stored-job.pdf",
        ),
    ]

    document_repository.get_by_interview_session_id.return_value = documents

    service = DocumentService(
        session_repository=session_repository,
        document_repository=document_repository,
        storage_provider=storage_provider,
        document_understanding_service=document_understanding_service,
    )

    service.delete_documents_for_session(session)

    document_repository.get_by_interview_session_id.assert_called_once_with(
        session.id,
    )

    assert storage_provider.delete.call_args_list == [
        call(documents[0]),
        call(documents[1]),
    ]

    assert document_repository.delete.call_args_list == [
        call(documents[0]),
        call(documents[1]),
    ]
    
def test_upload_document_preserves_ai_identified_document_type(tmp_path: Path,) -> None:
    session_repository = Mock()
    document_repository = Mock()
    storage_provider = Mock()
    document_understanding_service = Mock()

    session = create_session()

    storage_provider.store.return_value = StoredFile(
        original_filename="wrongly-uploaded.pdf",
        stored_filename="stored-document.pdf",
        storage_path="/tmp/stored-document.pdf",
        mime_type="application/pdf",
        file_size=12,
    )

    document_understanding_service.understand_document.return_value = (
        AiDocumentUnderstandingResult(
            document_type=AiDocumentType.JOB_DESCRIPTION,
            extracted_text="Senior Software Engineer\n\nRequirements...",
        )
    )

    document_repository.create.side_effect = (
        lambda interview_document: interview_document
    )

    service = DocumentService(
        session_repository=session_repository,
        document_repository=document_repository,
        storage_provider=storage_provider,
        document_understanding_service=document_understanding_service,
    )

    created = service.upload_document_for_session(
        session=session,
        document_type=DocumentType.CV,
        file=create_upload_file("wrongly-uploaded.pdf"),
    )

    assert created.extracted_text == (
        "Senior Software Engineer\n\nRequirements..."
    )
    assert created.document_type == DocumentType.JOB_DESCRIPTION