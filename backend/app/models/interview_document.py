from __future__ import annotations

import importlib
from datetime import datetime, timezone
from typing import Optional
from app.models.enums import DocumentType

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.interview_session import InterviewSession

session_module = importlib.import_module("app.db.session")
Base = session_module.Base
session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="documents")


class InterviewDocument(Base):
    __tablename__ = "interview_documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    document_type: Mapped[Optional[DocumentType]] = mapped_column(String(50), nullable=True, index=True)  # Should use DocumentType enum
    original_filename: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stored_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(nullable=True)
    storage_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
