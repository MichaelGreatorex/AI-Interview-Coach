from pathlib import Path
from unittest.mock import Mock

import pytest

from app.ai.document_understanding_service import DocumentUnderstandingService
from app.ai.models import AiDocumentType, AiDocumentUnderstandingResult


def test_understand_document_returns_ai_result(tmp_path: Path) -> None:
    document = tmp_path / "cv.pdf"
    document.write_bytes(b"fake pdf content")

    openai_client = Mock()

    uploaded_file = Mock()
    uploaded_file.id = "file-123"

    parsed_result = AiDocumentUnderstandingResult(
        document_type=AiDocumentType.CV,
        extracted_text="JOHN DOE\n\nEXPERIENCE\nSenior Software Engineer",
    )

    openai_client.client.files.create.return_value = uploaded_file

    response = Mock()
    response.output_parsed = parsed_result

    openai_client.client.responses.parse.return_value = response

    service = DocumentUnderstandingService(openai_client)

    result = service.understand_document(
        file_path=document,
        mime_type="application/pdf",
    )

    assert result == parsed_result
    
def test_understand_document_uploads_original_file(
    tmp_path: Path,
) -> None:
    document = tmp_path / "cv.pdf"
    document.write_bytes(b"fake pdf content")

    openai_client = Mock()

    uploaded_file = Mock()
    uploaded_file.id = "file-123"

    def capture_upload(*args, **kwargs):
        uploaded_file_object = kwargs["file"]

        assert uploaded_file_object.name == str(document)
        assert uploaded_file_object.read() == b"fake pdf content"

        return uploaded_file

    openai_client.client.files.create.side_effect = capture_upload

    response = Mock()
    response.output_parsed = AiDocumentUnderstandingResult(
        document_type=AiDocumentType.CV,
        extracted_text="John Doe\nSenior Software Engineer",
    )

    openai_client.client.responses.parse.return_value = response

    service = DocumentUnderstandingService(openai_client)

    result = service.understand_document(
        file_path=document,
        mime_type="application/pdf",
    )

    openai_client.client.files.create.assert_called_once()

    assert result.document_type == AiDocumentType.CV
    assert result.extracted_text == "John Doe\nSenior Software Engineer"

def test_understand_document_raises_when_openai_returns_no_result(
    tmp_path: Path,
) -> None:
    document = tmp_path / "document.pdf"
    document.write_bytes(b"fake pdf content")

    openai_client = Mock()

    uploaded_file = Mock()
    uploaded_file.id = "file-123"

    openai_client.client.files.create.return_value = uploaded_file

    response = Mock()
    response.output_parsed = None

    openai_client.client.responses.parse.return_value = response

    service = DocumentUnderstandingService(openai_client)

    with pytest.raises(
        ValueError,
        match="OpenAI returned no document understanding result",
    ):
        service.understand_document(
            file_path=document,
            mime_type="application/pdf",
        )
        
def test_actual_document_type_is_identified_by_ai(
    tmp_path: Path,
) -> None:
    document = tmp_path / "wrongly-labelled.pdf"
    document.write_bytes(b"fake pdf content")

    openai_client = Mock()

    uploaded_file = Mock()
    uploaded_file.id = "file-123"

    openai_client.client.files.create.return_value = uploaded_file

    response = Mock()
    response.output_parsed = AiDocumentUnderstandingResult(
        document_type=AiDocumentType.JOB_DESCRIPTION,
        extracted_text="Senior Software Engineer\n\nRequirements...",
    )

    openai_client.client.responses.parse.return_value = response

    service = DocumentUnderstandingService(openai_client)

    result = service.understand_document(
        file_path=document,
        mime_type="application/pdf",
    )

    assert result.document_type == AiDocumentType.JOB_DESCRIPTION