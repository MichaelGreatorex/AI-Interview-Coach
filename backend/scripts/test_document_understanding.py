from pathlib import Path

from app.ai.document_understanding_service import DocumentUnderstandingService
from app.ai.openai_client import OpenAIClient
from app.core.config import settings

from app.ai.models import AiDocumentUnderstandingResult


INPUT_COST_PER_MILLION = 0.40
OUTPUT_COST_PER_MILLION = 1.60


def main() -> None:
    documents = [
        (
            Path("../tests/fixtures/documents/Peter Parker CV.docx"),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        (
            Path("../tests/fixtures/documents/Akeneo JD.pdf"),
            "application/pdf",
        ),
    ]

    openai_client = OpenAIClient()
    service = DocumentUnderstandingService(openai_client)

    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0

    for document_path, mime_type in documents:
        if not document_path.exists():
            raise FileNotFoundError(
                f"Document not found: {document_path.resolve()}"
        )
        
        print(f"\n{'=' * 80}")
        print(f"Processing: {document_path.name}")
        print("=" * 80)

        # Upload the document.
        with document_path.open("rb") as file:
            uploaded_file = openai_client.client.files.create(
                file=file,
                purpose="user_data",
            )

        # Build the exact same request used by the service.
        response = openai_client.client.responses.parse(
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
                            "text": service._build_prompt(mime_type),
                        },
                    ],
                },
            ],
            text_format=AiDocumentUnderstandingResult
        )

        result = response.output_parsed

        if result is None:
            raise ValueError("OpenAI returned no document understanding result")

        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        total_tokens = response.usage.total_tokens

        input_cost = (
            input_tokens / 1_000_000
        ) * INPUT_COST_PER_MILLION

        output_cost = (
            output_tokens / 1_000_000
        ) * OUTPUT_COST_PER_MILLION

        request_cost = input_cost + output_cost

        total_input_tokens += input_tokens
        total_output_tokens += output_tokens
        total_cost += request_cost

        print(f"\nDocument type: {result.document_type.value}")

        print("\nExtracted text:")
        print(result.extracted_text)

        print("\nUsage:")
        print(f"  Input tokens:  {input_tokens:,}")
        print(f"  Output tokens: {output_tokens:,}")
        print(f"  Total tokens:  {total_tokens:,}")

        print("\nEstimated cost:")
        print(f"  Input:  ${input_cost:.6f}")
        print(f"  Output: ${output_cost:.6f}")
        print(f"  Total:  ${request_cost:.6f}")

    print(f"\n{'=' * 80}")
    print("TOTAL")
    print("=" * 80)

    print(f"Input tokens:  {total_input_tokens:,}")
    print(f"Output tokens: {total_output_tokens:,}")
    print(f"Total tokens:  {total_input_tokens + total_output_tokens:,}")
    print(f"Total cost:    ${total_cost:.6f}")


if __name__ == "__main__":
    main()