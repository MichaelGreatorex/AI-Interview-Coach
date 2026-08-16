import pytest

from app.extraction.docx_extractor import DocxDocumentTextExtractor
from app.extraction.factory import DocumentTextExtractorFactory
from app.extraction.pdf_extractor import PdfDocumentTextExtractor
from app.extraction.txt_extractor import TxtDocumentTextExtractor


def test_returns_pdf_extractor_for_pdf() -> None:
    factory = DocumentTextExtractorFactory()

    extractor = factory.get_extractor("application/pdf")

    assert isinstance(extractor, PdfDocumentTextExtractor)


def test_returns_docx_extractor_for_docx() -> None:
    factory = DocumentTextExtractorFactory()

    extractor = factory.get_extractor(
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    assert isinstance(extractor, DocxDocumentTextExtractor)


def test_returns_txt_extractor_for_plain_text() -> None:
    factory = DocumentTextExtractorFactory()

    extractor = factory.get_extractor("text/plain")

    assert isinstance(extractor, TxtDocumentTextExtractor)


def test_raises_for_unsupported_mime_type() -> None:
    factory = DocumentTextExtractorFactory()

    with pytest.raises(
        ValueError,
        match="Unsupported document MIME type: 'application/octet-stream'",
    ):
        factory.get_extractor("application/octet-stream")