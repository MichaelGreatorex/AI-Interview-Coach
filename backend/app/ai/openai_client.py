from openai import OpenAI

from app.core.config import settings


class OpenAIClient:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key is not configured")

        self._client = OpenAI(
            api_key=settings.openai_api_key,
        )

    @property
    def client(self) -> OpenAI:
        return self._client