from unittest.mock import patch

import pytest

from app.ai.openai_client import OpenAIClient


def test_openai_client_requires_api_key() -> None:
    with patch(
        "app.ai.openai_client.settings.openai_api_key",
        None,
    ):
        with pytest.raises(
            ValueError,
            match="OpenAI API key is not configured",
        ):
            OpenAIClient()


def test_openai_client_creates_sdk_client() -> None:
    with patch(
        "app.ai.openai_client.OpenAI",
    ) as openai_mock:
        with patch(
            "app.ai.openai_client.settings.openai_api_key",
            "test-api-key",
        ):
            client = OpenAIClient()

    openai_mock.assert_called_once_with(
        api_key="test-api-key",
    )
    assert client.client is openai_mock.return_value