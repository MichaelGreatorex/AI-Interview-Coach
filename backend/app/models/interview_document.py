from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.enums import DocumentType

if TYPE_CHECKING:
    from app.models.interview_session import InterviewSession


class InterviewDocument(Base):
    __tablename__ = "interview_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    interview_session_id: Mapped[int] = mapped_column(
        ForeignKey("interview_sessions.id"),
        nullable=False,
        index=True,
    )

    document_type: Mapped[DocumentType] = mapped_column(
        Enum(
            DocumentType,
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)

    stored_filename: Mapped[str] = mapped_column(String(255), nullable=False)

    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)

    file_size: Mapped[int] = mapped_column(nullable=False)

    storage_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    
    extracted_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    session: Mapped["InterviewSession"] = relationship(
        back_populates="documents",
    )