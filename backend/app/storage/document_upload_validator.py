from app.storage.document_content_validator import DocumentContentValidator
from app.storage.exceptions import InvalidDocumentUploadError
from app.storage.prepared_upload import PreparedUpload
from app.storage.upload_size import validate_upload_size


class DocumentUploadValidator:
    """Validate uploaded documents before an interview session is created."""

    def __init__(
        self,
        document_content_validator: DocumentContentValidator,
    ) -> None:
        self._document_content_validator = document_content_validator

    def validate(self, upload: PreparedUpload) -> None:
        self._validate_filename(upload)
        self._validate_size(upload)
        self._validate_content_type(upload)
        self._document_content_validator.validate(upload)

    @staticmethod
    def _validate_filename(upload: PreparedUpload) -> None:
        if not upload.filename or not upload.filename.strip():
            raise InvalidDocumentUploadError(
                "Uploaded document must have a filename"
            )

    @staticmethod
    def _validate_size(upload: PreparedUpload) -> None:
        if upload.file_size == 0:
            raise InvalidDocumentUploadError(
                "Uploaded document must not be empty"
            )

        validate_upload_size(upload.file_size)

    @staticmethod
    def _validate_content_type(upload: PreparedUpload) -> None:
        allowed_content_types = {
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
        }

        if upload.content_type not in allowed_content_types:
            raise InvalidDocumentUploadError(
                f"Unsupported document type: {upload.content_type}"
            )