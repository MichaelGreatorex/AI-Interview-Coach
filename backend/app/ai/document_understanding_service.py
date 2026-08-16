from pathlib import Path

from app.ai.models import AiDocumentUnderstandingResult
from app.ai.openai_client import OpenAIClient
from app.core.config import settings


class DocumentUnderstandingService:
    def __init__(
        self,
        openai_client: OpenAIClient,
    ) -> None:
        self._openai_client = openai_client

    def understand_document(
        self,
        file_path: Path,
        mime_type: str,
    ) -> AiDocumentUnderstandingResult:
        with file_path.open("rb") as file:
            uploaded_file = self._openai_client.client.files.create(
                file=file,
                purpose="user_data",
            )

        response = self._openai_client.client.responses.parse(
            model=settings.openai_document_model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "file_id": uploaded_file.id,
                        },
                        {
                            "type": "input_text",
                            "text": self._build_prompt(mime_type),
                        },
                    ],
                },
            ],
            text_format=AiDocumentUnderstandingResult,
        )

        if response.output_parsed is None:
            raise ValueError(
                "OpenAI returned no document understanding result",
            )

        return response.output_parsed

    @staticmethod
    def _build_prompt(mime_type: str) -> str:
        return f"""
    You are processing a document for an AI interview coaching application.

    The document MIME type is: {mime_type}

    Independently determine what the document actually is.

    Classify the document as exactly one of:
    - cv
    - job_description
    - unknown

    A CV may use any structure chosen by its author. A candidate might organise
    their experience around employers, projects, clients, consultancy engagements,
    contracts, or other structures. Do not impose a standard CV schema.

    A job description may also use any structure and terminology chosen by its
    author. Preserve its natural organisation.

    Extract the meaningful content of the document into editable plain text.

    Preserve:
    - headings and section names
    - paragraphs
    - bullet points
    - lists
    - dates
    - job titles
    - company/client names
    - project names
    - qualifications
    - skills
    - responsibilities
    - requirements
    - other meaningful information

    Preserve the order and meaning of the source document.

    Do NOT:
    - invent information
    - summarise information that can instead be faithfully reproduced
    - rewrite the author's claims
    - improve or embellish the document
    - impose a predetermined CV or job-description structure
    - omit meaningful information merely because it does not fit a conventional CV
    or job-description format

    The extracted text will be shown to the user in an editable Inspect View and
    may subsequently become the source of truth for an AI interview.

    If the document is not meaningfully identifiable as a CV or job description,
    classify it as unknown.

    If the document contains no meaningful recoverable content, return an empty
    extracted_text value.
    """.strip()