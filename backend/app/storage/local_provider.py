from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import BACKEND_DIR, settings
from app.storage.models import StoredFile
from app.storage.provider import StorageProvider
from app.storage.exceptions import FileTooLargeError


class LocalStorageProvider(StorageProvider):
    """Store uploaded files on local disk under storage/uploads."""

    CHUNK_SIZE = 64 * 1024

    def __init__(self, uploads_dir: Path | None = None) -> None:
        self._uploads_dir = (
            uploads_dir
            or (BACKEND_DIR / "storage" / "uploads")
        )

    def store(self, file: UploadFile) -> StoredFile:
        self._uploads_dir.mkdir(parents=True, exist_ok=True)

        original_filename = file.filename or "upload"
        extension = "".join(Path(original_filename).suffixes)
        stored_filename = f"{uuid4()}{extension}"
        destination_path = self._uploads_dir / stored_filename

        file.file.seek(0)

        total_size = 0

        try:
            with destination_path.open("wb") as output:
                while True:
                    chunk = file.file.read(self.CHUNK_SIZE)

                    if not chunk:
                        break

                    total_size += len(chunk)

                    if total_size > settings.max_upload_size_bytes:
                        raise FileTooLargeError(
                            f"File exceeds maximum allowed size of "
                            f"{settings.max_upload_size_bytes} bytes"
                        )

                    output.write(chunk)

        except Exception:
            if destination_path.exists():
                destination_path.unlink()

            raise

        return StoredFile(
            original_filename=original_filename,
            stored_filename=stored_filename,
            storage_path=str(destination_path),
            mime_type=file.content_type or "application/octet-stream",
            file_size=total_size,
        )

    def delete(self, stored_file: StoredFile) -> None:
        file_path = Path(stored_file.storage_path)

        if file_path.exists():
            file_path.unlink()