from fastapi import UploadFile

from app.core.config import settings
from app.storage.exceptions import FileTooLargeError


class DocumentUploadValidator:
    """Validate uploaded documents before an interview session is created."""

    def validate(self, file: UploadFile) -> None:
        self._validate_filename(file)
        self._validate_size(file)
        self._validate_content_type(file)

    @staticmethod
    def _validate_filename(file: UploadFile) -> None:
        if not file.filename or not file.filename.strip():
            raise ValueError(
                "Uploaded document must have a filename"
            )

    @staticmethod
    def _validate_size(file: UploadFile) -> None:
        file.file.seek(0)

        content = file.file.read()

        if not content:
            raise ValueError(
                "Uploaded document must not be empty"
            )

        if len(content) > settings.max_upload_size_bytes:
            raise FileTooLargeError(
                "File exceeds maximum allowed size of "
                f"{settings.max_upload_size_bytes} bytes"
            )

        file.file.seek(0)

    @staticmethod
    def _validate_content_type(file: UploadFile) -> None:
        allowed_content_types = {
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
        }

        if file.content_type not in allowed_content_types:
            raise ValueError(
                f"Unsupported document type: {file.content_type}"
            )