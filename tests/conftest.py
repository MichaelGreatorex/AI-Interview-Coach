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
def reset_test_state() -> Generator[None, None, None]:
    previous_environment = settings.environment
    settings.environment = "test"

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


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    yield TestClient(app)


@pytest.fixture
def mock_document_understanding_service() -> Mock:
    service = Mock(spec=DocumentUnderstandingService)

    service.understand_document.side_effect = [
        AiDocumentUnderstandingResult(
            document_type=AiDocumentType.CV,
            extracted_text=(
                "John Doe\n"
                "Senior Software Engineer\n"
                "Python, C#, AWS"
            ),
        ),
        AiDocumentUnderstandingResult(
            document_type=AiDocumentType.JOB_DESCRIPTION,
            extracted_text=(
                "Senior Software Engineer\n"
                "Requirements\n"
                "Python, C#, AWS"
            ),
        ),
    ]

    return service


@pytest.fixture
def ai_test_client(
    mock_document_understanding_service: Mock,
) -> Generator[TestClient, None, None]:
    app.dependency_overrides[
        get_document_understanding_service
    ] = lambda: mock_document_understanding_service

    yield TestClient(app)

    app.dependency_overrides.pop(
        get_document_understanding_service,
        None,
    )


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    session_factory = get_session_factory()
    session = session_factory()

    try:
        yield session
    finally:
        session.close()

