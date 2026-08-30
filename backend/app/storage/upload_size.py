from app.core.config import settings
from app.storage.exceptions import FileTooLargeError


def validate_upload_size(file_size: int) -> None:
    if file_size > settings.max_upload_size_bytes:
        raise FileTooLargeError(
            "File exceeds maximum allowed size of "
            f"{settings.max_upload_size_bytes} bytes"
        )