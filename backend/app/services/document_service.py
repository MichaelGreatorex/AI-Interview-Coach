from fastapi import UploadFile
from app.models.enums import DocumentType
from app.models.interview_document import InterviewDocument
from app.models.interview_session import InterviewSession
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

        session = self._session_repository.get_by_public_id(
            interview_session_id
        )

        if session is None:
            raise ValueError(
                f"Interview session '{interview_session_id}' does not exist"
            )
            
        return self.upload_document_for_session(
            session=session,
            document_type=document_type,
            file=file,
        )

    
    def upload_document_for_session(
        self,
        session: InterviewSession,
        document_type: DocumentType,
        file: UploadFile,
    ) -> InterviewDocument:
        
        stored_document = self._storage_provider.store(file)

        interview_document = InterviewDocument(
            interview_session_id=session.id,
            document_type=document_type,
            original_filename=stored_document.original_filename,
            stored_filename=stored_document.stored_filename,
            mime_type=stored_document.mime_type,
            file_size=stored_document.file_size,
            storage_path=stored_document.storage_path,
        )
        
        return self._repository.create(interview_document)
    
    def delete_documents_for_session(
        self,
        session: InterviewSession,
    ) -> None:
        documents = self._repository.get_by_interview_session_id(session.id)
        for document in documents:
            self._storage_provider.delete(document)
            self._repository.delete(document)