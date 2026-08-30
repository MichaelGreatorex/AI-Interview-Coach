from app.storage.exceptions import InvalidDocumentUploadError
from app.storage.prepared_upload import PreparedUpload


class DocumentContentValidator:
    """Validate that uploaded bytes are consistent with their content type."""

    def validate(self, upload: PreparedUpload) -> None:
        if upload.content_type == "application/pdf":
            self._validate_pdf(upload)

        elif upload.content_type == "application/msword":
            self._validate_doc(upload)

        elif (
            upload.content_type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            self._validate_docx(upload)

        elif upload.content_type == "text/plain":
            return

    @staticmethod
    def _validate_pdf(upload: PreparedUpload) -> None:
        if not upload.content.startswith(b"%PDF-"):
            raise InvalidDocumentUploadError(
                "Uploaded file content does not match its declared "
                "document type"
            )

    @staticmethod
    def _validate_doc(upload: PreparedUpload) -> None:
        # OLE Compound File signature used by legacy .doc files.
        if not upload.content.startswith(
            b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
        ):
            raise InvalidDocumentUploadError(
                "Uploaded file content does not match its declared "
                "document type"
            )

    @staticmethod
    def _validate_docx(upload: PreparedUpload) -> None:
        # DOCX is a ZIP-based Open XML package.
        if not upload.content.startswith(b"PK\x03\x04"):
            raise InvalidDocumentUploadError(
                "Uploaded file content does not match its declared "
                "document type"
            )