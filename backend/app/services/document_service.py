from fastapi import UploadFile
from pathlib import Path

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
from app.extraction.factory import DocumentTextExtractorFactory




class DocumentService:
    def __init__(
        self,
        session_repository: InterviewSessionRepository,
        document_repository: InterviewDocumentRepository,
        storage_provider: StorageProvider,
        text_extractor_factory: DocumentTextExtractorFactory
    ) -> None:
        self._session_repository = session_repository
        self._repository = document_repository
        self._storage_provider = storage_provider
        self._text_extractor_factory = text_extractor_factory

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
        
        try:
            extractor = self._text_extractor_factory.get_extractor(stored_document.mime_type)
            extracted_text = extractor.extract(Path(stored_document.storage_path))
            interview_document = InterviewDocument(
                interview_session_id=session.id,
                document_type=document_type,
                original_filename=stored_document.original_filename,
                stored_filename=stored_document.stored_filename,
                mime_type=stored_document.mime_type,
                file_size=stored_document.file_size,
                storage_path=stored_document.storage_path,
                extracted_text=extracted_text,
            )
            
            return self._repository.create(interview_document)
        
        except Exception:
            # If extraction fails, delete the stored file and raise an error
            self._storage_provider.delete(stored_document)
            raise
    
    def delete_documents_for_session(
        self,
        session: InterviewSession,
    ) -> None:
        documents = self._repository.get_by_interview_session_id(session.id)
        for document in documents:
            self._storage_provider.delete(document)
            self._repository.delete(document)