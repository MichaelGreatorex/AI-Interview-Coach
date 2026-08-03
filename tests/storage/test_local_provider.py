
from io import BytesIO
from pathlib import Path
from uuid import UUID

from fastapi import UploadFile

from app.storage.local_provider import LocalStorageProvider


def create_upload_file() -> UploadFile:
    return UploadFile(
        filename="cv.pdf",
        file=BytesIO(b"My fake CV"),
        headers={"content-type": "application/pdf"},
    )


def test_store_writes_upload_and_returns_metadata(tmp_path: Path) -> None:
    provider = LocalStorageProvider(uploads_dir=tmp_path / "storage" / "uploads")
    upload = create_upload_file()

    stored = provider.store(upload)

    stored_path = Path(stored.storage_path)

    assert stored.original_filename == "cv.pdf"
    assert stored.stored_filename.endswith(".pdf")
    assert stored_path.exists()
    assert stored_path.read_bytes() == b"My fake CV"
    assert stored_path.name == stored.stored_filename
    assert stored.mime_type == "application/pdf"
    assert stored.file_size == len(b"My fake CV")

    UUID(stored_path.stem)