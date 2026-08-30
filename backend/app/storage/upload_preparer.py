from fastapi import UploadFile

from app.core.config import settings
from app.storage.exceptions import FileTooLargeError
from app.storage.prepared_upload import PreparedUpload


class UploadPreparer:
    """Read an uploaded file once, enforcing the maximum size."""

    def prepare(self, file: UploadFile) -> PreparedUpload:
        file.file.seek(0)

        content = file.file.read(
            settings.max_upload_size_bytes + 1
        )

        if len(content) > settings.max_upload_size_bytes:
            raise FileTooLargeError(
                "File exceeds maximum allowed size of "
                f"{settings.max_upload_size_bytes} bytes"
            )

        return PreparedUpload(
            filename=file.filename or "upload",
            content_type=file.content_type,
            content=content,
        )