import shutil
import tempfile
from pathlib import Path
from typing import Generator

import app.models
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

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
