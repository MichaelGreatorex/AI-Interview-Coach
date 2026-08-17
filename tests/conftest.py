import shutil
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import Mock
from app.ai.document_understanding_service import (DocumentUnderstandingService)
from app.ai.models import AiDocumentUnderstandingResult, AiDocumentType
from app.api.dependencies import get_document_understanding_service


import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.ai.openai_client import get_openai_client
from app.core.config import settings
from app.db.session import Base, get_engine, get_session_factory
from app.main import app


@pytest.fixture(autouse=True)
def reset_test_state(mock_document_understanding_service: Mock) -> Generator[None, None, None]:
    previous_environment = settings.environment
    settings.environment = "test"

    app.dependency_overrides[
            get_document_understanding_service
        ] = lambda: mock_document_understanding_service

    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    uploads_dir = Path(tempfile.gettempdir()) / "ai-interview-coach"
    if uploads_dir.exists():
        shutil.rmtree(uploads_dir)

    yield

    if uploads_dir.exists():
        shutil.rmtree(uploads_dir)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    settings.environment = previous_environment
    
    app.dependency_overrides.clear()
    settings.environment = previous_environment


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    session_factory = get_session_factory()
    session = session_factory()

    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def mock_document_understanding_service() -> Mock:
    service = Mock(spec=DocumentUnderstandingService)

    def understand_document(file_path: Path, mime_type: str):
        if "job" in file_path.name.lower():
            return AiDocumentUnderstandingResult(
                document_type=AiDocumentType.JOB_DESCRIPTION,
                extracted_text="Test job description",
            )

        return AiDocumentUnderstandingResult(
            document_type=AiDocumentType.CV,
            extracted_text="Test CV content",
        )

    service.understand_document.side_effect = understand_document

    return service