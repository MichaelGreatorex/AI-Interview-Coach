from app.core.config import settings
from app.storage.exceptions import FileTooLargeError
from app.storage.prepared_upload import PreparedUpload


class DocumentUploadValidator:
    """Validate uploaded documents before an interview session is created."""

    def validate(self, upload: PreparedUpload) -> None:
        self._validate_filename(upload)
        self._validate_size(upload)
        self._validate_content_type(upload)

    @staticmethod
    def _validate_filename(upload: PreparedUpload) -> None:
        if not upload.filename or not upload.filename.strip():
            raise ValueError(
                "Uploaded document must have a filename"
            )

    @staticmethod
    def _validate_size(upload: PreparedUpload) -> None:
        if upload.file_size == 0:
            raise ValueError(
                "Uploaded document must not be empty"
            )

        if upload.file_size > settings.max_upload_size_bytes:
            raise FileTooLargeError(
                "File exceeds maximum allowed size of "
                f"{settings.max_upload_size_bytes} bytes"
            )

    @staticmethod
    def _validate_content_type(upload: PreparedUpload) -> None:
        allowed_content_types = {
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
        }

        if upload.content_type not in allowed_content_types:
            raise ValueError(
                f"Unsupported document type: {upload.content_type}"
            )