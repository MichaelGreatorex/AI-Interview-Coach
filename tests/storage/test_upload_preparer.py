from io import BytesIO

import pytest
from fastapi import UploadFile

from app.core.config import settings
from app.storage.exceptions import FileTooLargeError
from app.storage.upload_preparer import UploadPreparer


def create_upload_file(
    *,
    filename: str | None,
    content: bytes,
    content_type: str = "application/pdf",
) -> UploadFile:
    return UploadFile(
        filename=filename,
        file=BytesIO(content),
        headers={"content-type": content_type},
    )


def test_prepare_preserves_missing_filename_as_empty() -> None:
    preparer = UploadPreparer()

    upload = create_upload_file(
        filename=None,
        content=b"content",
    )

    prepared = preparer.prepare(upload)

    assert prepared.filename == ""


def test_prepare_rejects_oversized_upload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    preparer = UploadPreparer()
    monkeypatch.setattr(settings, "max_upload_size_bytes", 4)

    upload = create_upload_file(
        filename="cv.pdf",
        content=b"12345",
    )

    with pytest.raises(FileTooLargeError):
        preparer.prepare(upload)
