from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings
class Base(DeclarativeBase):
    pass

engine = None
SessionLocal = None


def get_database_url() -> Optional[str]:
    return settings.database_url


def get_engine():
    global engine, SessionLocal

    database_url = get_database_url()
    if not database_url:
        raise RuntimeError("Database URL is not configured")

    if engine is None:
        engine = create_engine(database_url, echo=settings.debug)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return engine


def get_session_local():
    get_engine()
    return SessionLocal
