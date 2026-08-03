from fastapi import UploadFile
from app.models.enums import DocumentType
from app.models.interview_document import InterviewDocument
from app.repositories.interview_document_repository import (
    InterviewDocumentRepository,
)
from app.repositories.interview_session_repository import (
    InterviewSessionRepository,
)
from app.storage.provider import StorageProvider


class DocumentService:
    def __init__(
        self,
        session_repository: InterviewSessionRepository,
        document_repository: InterviewDocumentRepository,
        storage_provider: StorageProvider,
    ) -> None:
        self._session_repository = session_repository
        self._repository = document_repository
        self._storage_provider = storage_provider

    def upload_document(
        self,
        interview_session_id: str,
        document_type: DocumentType,
        file: UploadFile,
    ) -> InterviewDocument:

        interview_session = self._session_repository.get_by_public_id(
            interview_session_id
        )

        if interview_session is None:
            raise ValueError(
                f"Interview session '{interview_session_id}' does not exist"
            )

        stored_file = self._storage_provider.store(file)

        interview_document = InterviewDocument(
            interview_session_id=interview_session.id,
            document_type=document_type,
            original_filename=stored_file.original_filename,
            stored_filename=stored_file.stored_filename,
            mime_type=stored_file.mime_type,
            file_size=stored_file.file_size,
            storage_path=stored_file.storage_path,
        )

        return self._repository.create(interview_document)