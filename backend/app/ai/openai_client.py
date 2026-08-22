from openai import DefaultHttpxClient, OpenAI

from app.core.config import settings


class OpenAIClient:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key is not configured")

        self._client = OpenAI(
            api_key=settings.openai_api_key,
            http_client=DefaultHttpxClient(trust_env=False),
        )

    @property
    def client(self) -> OpenAI:
        return self._client


def get_openai_client() -> OpenAIClient:
    return OpenAIClient()