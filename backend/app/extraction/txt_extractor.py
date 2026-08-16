from pathlib import Path

from app.extraction.extractor import DocumentTextExtractor


class TxtDocumentTextExtractor(DocumentTextExtractor):

    def extract(
        self,
        file_path: Path,
    ) -> str:
        return file_path.read_text(
            encoding="utf-8",
        )