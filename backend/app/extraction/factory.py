from app.extraction.docx_extractor import DocxDocumentTextExtractor
from app.extraction.extractor import DocumentTextExtractor
from app.extraction.pdf_extractor import PdfDocumentTextExtractor
from app.extraction.txt_extractor import TxtDocumentTextExtractor


class DocumentTextExtractorFactory:
    def __init__(self) -> None:
        self._extractors: dict[str, DocumentTextExtractor] = {
            "application/pdf": PdfDocumentTextExtractor(),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": (
                DocxDocumentTextExtractor()
            ),
            "text/plain": TxtDocumentTextExtractor(),
        }

    def get_extractor(self, mime_type: str) -> DocumentTextExtractor:
        try:
            return self._extractors[mime_type]
        except KeyError:
            raise ValueError(
                f"Unsupported document MIME type: '{mime_type}'"
            )