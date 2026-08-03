from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.repositories.interview_session_repository import (
    InterviewSessionRepository,
)
from app.repositories.interview_document_repository import (
    InterviewDocumentRepository,
)

from app.services.interview_session_service import (
    InterviewSessionService,
)
from app.services.document_service import DocumentService

from app.storage.local_provider import LocalStorageProvider
from app.storage.provider import StorageProvider

def get_interview_session_repository(
    db: Session = Depends(get_db),
) -> InterviewSessionRepository:
    return InterviewSessionRepository(db)

def get_interview_document_repository(
    db: Session = Depends(get_db),
) -> InterviewDocumentRepository:
    return InterviewDocumentRepository(db)

def get_storage_provider() -> StorageProvider:
    return LocalStorageProvider()

def get_interview_session_service(
    repository: InterviewSessionRepository = Depends(
        get_interview_session_repository,
    ),
) -> InterviewSessionService:
    return InterviewSessionService(repository)

InterviewSessionServiceDependency = Annotated[
    InterviewSessionService,
    Depends(get_interview_session_service),
]

def get_document_service(
    session_repository: InterviewSessionRepository = Depends(
        get_interview_session_repository,
    ),
    document_repository: InterviewDocumentRepository = Depends(
        get_interview_document_repository,
    ),
    storage_provider: StorageProvider = Depends(
        get_storage_provider,
    ),
) -> DocumentService:
    return DocumentService(
        session_repository=session_repository,
        document_repository=document_repository,
        storage_provider=storage_provider,
    )

DocumentServiceDependency = Annotated[
    DocumentService,
    Depends(get_document_service),
]