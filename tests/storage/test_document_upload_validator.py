import pytest

from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import settings
from app.storage.document_upload_validator import DocumentUploadValidator
from app.storage.exceptions import FileTooLargeError
from app.storage.prepared_upload import PreparedUpload
from app.storage.document_content_validator import DocumentContentValidator


def create_prepared_upload(
    *,
    filename: str,
    content: bytes,
    content_type: str | None,
) -> PreparedUpload:
    return PreparedUpload(
        filename=filename,
        content_type=content_type,
        content=content,
    )


def test_validate_accepts_valid_cv_upload() -> None:
    validator = DocumentUploadValidator(
    document_content_validator=DocumentContentValidator(),
)

    cv_file = create_prepared_upload(
        filename="cv.pdf",
        content=b"%PDF-1.7\n",
        content_type="application/pdf",
    )

    validator.validate(cv_file)


def test_validate_accepts_valid_job_description_upload() -> None:
    validator = DocumentUploadValidator(
        document_content_validator=DocumentContentValidator(),
    )

    job_description_file = create_prepared_upload(
        filename="job-description.docx",
        content=b"PK\x03\x04",
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
    )

    validator.validate(job_description_file)


def test_validate_rejects_oversized_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = DocumentUploadValidator(
        document_content_validator=DocumentContentValidator(),
    )

    monkeypatch.setattr(
        settings,
        "max_upload_size_bytes",
        4,
    )

    oversized_file = create_prepared_upload(
        filename="cv.pdf",
        content=b"12345",
        content_type="application/pdf",
    )

    with pytest.raises(FileTooLargeError):
        validator.validate(oversized_file)


def test_validate_rejects_empty_file() -> None:
    validator = DocumentUploadValidator(
        document_content_validator=DocumentContentValidator(),
    )

    empty_file = create_prepared_upload(
        filename="cv.pdf",
        content=b"",
        content_type="application/pdf",
    )

    with pytest.raises(ValueError, match="must not be empty"):
        validator.validate(empty_file)


def test_validate_rejects_malformed_upload_without_content_type() -> None:
    validator = DocumentUploadValidator(
        document_content_validator=DocumentContentValidator(),
    )

    malformed_file = create_prepared_upload(
        filename="cv.pdf",
        content=b"valid content",
        content_type=None,
    )

    with pytest.raises(ValueError, match="Unsupported document type"):
        validator.validate(malformed_file)


def test_validate_rejects_malformed_upload_with_blank_filename() -> None:
    validator = DocumentUploadValidator(
        document_content_validator=DocumentContentValidator(),
    )

    malformed_file = create_prepared_upload(
        filename="   ",
        content=b"valid content",
        content_type="application/pdf",
    )

    with pytest.raises(ValueError, match="must have a filename"):
        validator.validate(malformed_file)
