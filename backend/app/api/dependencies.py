import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db

from app.repositories.interview_session_repository import InterviewSessionRepository
from app.repositories.interview_document_repository import InterviewDocumentRepository
from app.repositories.interview_response_repository import InterviewResponseRepository

from app.storage.local_provider import LocalStorageProvider
from app.storage.provider import StorageProvider

from app.services.document_service import DocumentService
from app.services.interview_session_service import InterviewSessionService
from app.services.interview_engine import InterviewEngine
from app.services.interview_workflow_service import InterviewWorkflowService
from app.services.interview_response_service import InterviewResponseService

def get_interview_session_repository(
    db: Session = Depends(get_db),
) -> InterviewSessionRepository:
    return InterviewSessionRepository(db)

def get_interview_document_repository(
    db: Session = Depends(get_db),
) -> InterviewDocumentRepository:
    return InterviewDocumentRepository(db)

def get_interview_response_repository(
    db: Session = Depends(get_db),
) -> InterviewResponseRepository:
    return InterviewResponseRepository(db)

def get_storage_provider() -> StorageProvider:
    if settings.environment == "test":
        uploads_dir = Path(tempfile.gettempdir()) / "ai-interview-coach" / "uploads"
        return LocalStorageProvider(uploads_dir=uploads_dir)

    return LocalStorageProvider()

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
    
def get_interview_response_service(
    repository: InterviewResponseRepository = Depends(
        get_interview_response_repository,
    ),
) -> InterviewResponseService:
    return InterviewResponseService(
        repository=repository,
    )
    
def get_interview_engine() -> InterviewEngine:
    return InterviewEngine()
    
def get_interview_session_service(
    repository: InterviewSessionRepository = Depends(
        get_interview_session_repository,
    ),
    document_service: DocumentService = Depends(
        get_document_service,
    ),
    response_service: InterviewResponseService = Depends(
        get_interview_response_service,
    ),
    interview_engine: InterviewEngine = Depends(
        get_interview_engine,
    ),
) -> InterviewSessionService:
    return InterviewSessionService(
        repository=repository,
        document_service=document_service,
        response_service=response_service,
        interview_engine=interview_engine,
    )

def get_interview_workflow_service(
    session_service: InterviewSessionService = Depends(
        get_interview_session_service,
    ),
    document_service: DocumentService = Depends(
        get_document_service,
    ),
    generation_service: InterviewEngine = Depends(
        get_interview_engine,
    ),
) -> InterviewWorkflowService:
    return InterviewWorkflowService(
        session_service=session_service,
        document_service=document_service,
        generation_service=generation_service,
    )


    
InterviewSessionServiceDependency = Annotated[
    InterviewSessionService,
    Depends(get_interview_session_service),
]
InterviewResponseServiceDependency = Annotated[
    InterviewResponseService,
    Depends(get_interview_response_service),
]

InterviewEngineDependency = Annotated[
    InterviewEngine,
    Depends(get_interview_engine),
]

DocumentServiceDependency = Annotated[
    DocumentService,
    Depends(get_document_service),
]

InterviewWorkflowServiceDependency = Annotated[
    InterviewWorkflowService,
    Depends(get_interview_workflow_service),
]
