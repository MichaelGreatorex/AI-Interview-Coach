import pytest

from app.storage.document_content_validator import DocumentContentValidator
from app.storage.prepared_upload import PreparedUpload


def create_upload(
    *,
    content_type: str,
    content: bytes,
    filename: str = "document",
) -> PreparedUpload:
    return PreparedUpload(
        filename=filename,
        content_type=content_type,
        content=content,
    )


def test_accepts_valid_pdf() -> None:
    validator = DocumentContentValidator()

    upload = create_upload(
        filename="cv.pdf",
        content_type="application/pdf",
        content=b"%PDF-1.7\nsome pdf content",
    )

    validator.validate(upload)


def test_rejects_pdf_with_invalid_content() -> None:
    validator = DocumentContentValidator()

    upload = create_upload(
        filename="cv.pdf",
        content_type="application/pdf",
        content=b"this is not actually a PDF",
    )

    with pytest.raises(
        ValueError,
        match="does not match its declared document type",
    ):
        validator.validate(upload)


def test_accepts_valid_doc() -> None:
    validator = DocumentContentValidator()

    upload = create_upload(
        filename="cv.doc",
        content_type="application/msword",
        content=b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"doc content",
    )

    validator.validate(upload)


def test_rejects_doc_with_invalid_content() -> None:
    validator = DocumentContentValidator()

    upload = create_upload(
        filename="cv.doc",
        content_type="application/msword",
        content=b"this is not actually a DOC file",
    )

    with pytest.raises(
        ValueError,
        match="does not match its declared document type",
    ):
        validator.validate(upload)


def test_accepts_valid_docx() -> None:
    validator = DocumentContentValidator()

    upload = create_upload(
        filename="cv.docx",
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
        content=b"PK\x03\x04" + b"docx content",
    )

    validator.validate(upload)


def test_rejects_docx_with_invalid_content() -> None:
    validator = DocumentContentValidator()

    upload = create_upload(
        filename="cv.docx",
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
        content=b"this is not actually a DOCX file",
    )

    with pytest.raises(
        ValueError,
        match="does not match its declared document type",
    ):
        validator.validate(upload)


def test_accepts_plain_text_without_content_signature() -> None:
    validator = DocumentContentValidator()

    upload = create_upload(
        filename="cv.txt",
        content_type="text/plain",
        content=b"This is a plain text CV.",
    )

    validator.validate(upload)