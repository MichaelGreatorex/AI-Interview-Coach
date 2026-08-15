from pathlib import Path

from app.extraction.pdf_extractor import PdfDocumentTextExtractor


def test_extracts_text_from_pdf() -> None:
    file_path = (
        Path(__file__).parent.parent
        / "fixtures"
        / "documents"
        / "John Doe CV.pdf"
    )

    extractor = PdfDocumentTextExtractor()

    result = extractor.extract(file_path)
    
    print(repr(result))

    assert "Job Title, Company Name; City, County — 2022–Present " in result
    assert "no_reply@example.com" in result
    assert "University Name, City, County — Degree, Year" in result