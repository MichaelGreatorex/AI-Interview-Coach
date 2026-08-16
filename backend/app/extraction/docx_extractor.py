from pathlib import Path

from docx import Document


from app.extraction.extractor import DocumentTextExtractor

class DocxDocumentTextExtractor(DocumentTextExtractor):
    def extract(self, file_path: Path) -> str:
        document = Document(file_path)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)