from io import BytesIO
from urllib import response
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import pytest
from fastapi import UploadFile

from app.core.config import settings
from app.services.document_upload_validator import DocumentUploadValidator
from app.storage.exceptions import FileTooLargeError
from app.models.interview_session import InterviewSession
from app.repositories.interview_session_repository import InterviewSessionRepository
from tests.conftest import db_session


def create_upload_file(
    *,
    filename: str,
    content: bytes,
    content_type: str | None,
) -> UploadFile:
    headers = {}
    if content_type is not None:
        headers["content-type"] = content_type

    return UploadFile(
        filename=filename,
        file=BytesIO(content),
        headers=headers,
    )


def test_validate_accepts_valid_cv_upload() -> None:
    validator = DocumentUploadValidator()

    cv_file = create_upload_file(
        filename="cv.pdf",
        content=b"candidate cv content",
        content_type="application/pdf",
    )

    validator.validate(cv_file)


def test_validate_accepts_valid_job_description_upload() -> None:
    validator = DocumentUploadValidator()

    job_description_file = create_upload_file(
        filename="job-description.docx",
        content=b"job description content",
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
    )

    validator.validate(job_description_file)


def test_validate_rejects_oversized_file(monkeypatch: pytest.MonkeyPatch) -> None:
    validator = DocumentUploadValidator()
    monkeypatch.setattr(settings, "max_upload_size_bytes", 4)

    oversized_file = create_upload_file(
        filename="cv.pdf",
        content=b"12345",
        content_type="application/pdf",
    )

    with pytest.raises(FileTooLargeError):
        validator.validate(oversized_file)


def test_validate_rejects_empty_file() -> None:
    validator = DocumentUploadValidator()

    empty_file = create_upload_file(
        filename="cv.pdf",
        content=b"",
        content_type="application/pdf",
    )

    with pytest.raises(ValueError, match="must not be empty"):
        validator.validate(empty_file)


def test_validate_rejects_malformed_upload_without_content_type() -> None:
    validator = DocumentUploadValidator()

    malformed_file = create_upload_file(
        filename="cv.pdf",
        content=b"valid content",
        content_type=None,
    )

    with pytest.raises(ValueError, match="Unsupported document type"):
        validator.validate(malformed_file)


def test_validate_rejects_malformed_upload_with_blank_filename() -> None:
    validator = DocumentUploadValidator()

    malformed_file = create_upload_file(
        filename="   ",
        content=b"valid content",
        content_type="application/pdf",
    )

    with pytest.raises(ValueError, match="must have a filename"):
        validator.validate(malformed_file)
        

def test_process_documents_rejects_oversized_upload_without_creating_session(
    ai_test_client: TestClient,
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        settings,
        "max_upload_size_bytes",
        10,
    )

    response = ai_test_client.post(
        "/api/v1/interviews",
        files={
            "cv": (
                "cv.pdf",
                b"this file is too large",
                "application/pdf",
            ),
            "job_description": (
                "job-description.pdf",
                b"valid",
                "application/pdf",
            ),
        },
    )

    assert response.status_code == 413
    assert response.json() == {
        "detail": "File exceeds maximum allowed size of 10 bytes",
    }

    sessions = db_session.query(InterviewSession).all()

    assert sessions == []
