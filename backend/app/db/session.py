from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy.pool import StaticPool

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = None
SessionLocal = None


def get_database_url() -> Optional[str]:
    if settings.database_url:
        return settings.database_url

    if settings.environment != "production":
        return "sqlite:///:memory:"

    return None


def get_engine():
    global engine, SessionLocal

    database_url = get_database_url()
    if not database_url:
        raise RuntimeError("Database URL is not configured")

    if engine is None:
        engine_kwargs = {"echo": settings.debug}

        if database_url == "sqlite:///:memory:":
            engine_kwargs.update(
                {
                    "connect_args": {"check_same_thread": False},
                    "poolclass": StaticPool,
                }
            )

        engine = create_engine(
            database_url,
            **engine_kwargs,
        )

        SessionLocal = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False,
        )

        Base.metadata.create_all(bind=engine)

    return engine


def get_session_factory():
    get_engine()
    return SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session
    for the lifetime of a request.
    """
    SessionFactory = get_session_factory()

    db = SessionFactory()

    try:
        yield db
    finally:
        db.close()