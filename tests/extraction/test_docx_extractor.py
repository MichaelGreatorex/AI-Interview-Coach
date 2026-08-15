from pathlib import Path

from app.extraction.docx_extractor import DocxDocumentTextExtractor


def test_extracts_text_from_docx() -> None:
    file_path = (
        Path(__file__).parent.parent
        / "fixtures"
        / "documents"
        / "Peter Parker CV.docx"
    )

    extractor = DocxDocumentTextExtractor()

    result = extractor.extract(file_path)

    assert "Fought various villains, also saved some from other universes, collaborated with friends and other Spidermen etc." in result
    assert "Internship, OSCORP, New York — 2005-2019" in result