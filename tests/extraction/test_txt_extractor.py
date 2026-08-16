from pathlib import Path

from app.extraction.txt_extractor import TxtDocumentTextExtractor


def test_extracts_text_from_txt_file(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "example.txt"

    expected_text = (
        "Tell me about yourself.\n"
        "I am a software engineer with experience "
        "building secure applications."
    )

    file_path.write_text(
        expected_text,
        encoding="utf-8",
    )

    extractor = TxtDocumentTextExtractor()

    result = extractor.extract(file_path)

    assert result == expected_text