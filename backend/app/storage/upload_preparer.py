from fastapi import UploadFile

from app.core.config import settings
from app.storage.prepared_upload import PreparedUpload
from app.storage.upload_size import validate_upload_size


class UploadPreparer:
    """Read an uploaded file once, enforcing the maximum size."""

    def prepare(self, file: UploadFile) -> PreparedUpload:
        file.file.seek(0)

        content = file.file.read(
            settings.max_upload_size_bytes + 1
        )
        validate_upload_size(len(content))

        return PreparedUpload(
            filename=file.filename if file.filename is not None else "",
            content_type=file.content_type,
            content=content,
        )