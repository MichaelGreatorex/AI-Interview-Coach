from pathlib import Path

import fitz

from app.extraction.extractor import DocumentTextExtractor


class PdfDocumentTextExtractor(DocumentTextExtractor):

    def extract(
        self,
        file_path: Path,
    ) -> str:
        with fitz.open(file_path) as document:
            pages = [
                page.get_text()
                for page in document
            ]

        return "\n".join(pages)