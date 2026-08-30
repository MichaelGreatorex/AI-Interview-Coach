from app.core.config import Settings
import pytest


def test_settings_parse_comma_separated_allowed_origins() -> None:
    settings = Settings(allowed_origins="http://localhost:3000, https://example.com")

    assert settings.allowed_origins == ["http://localhost:3000", "https://example.com"]


def test_settings_parse_json_array_allowed_origins() -> None:
    settings = Settings(
        allowed_origins='["http://localhost:3000","http://frontend:3000"]',
    )

    assert settings.allowed_origins == [
        "http://localhost:3000",
        "http://frontend:3000",
    ]


def test_settings_convert_empty_strings_to_none_without_database_config() -> None:
    settings = Settings(
        openai_api_key="",
        s3_bucket_name="   ",
        database_url="",
        database_host=None,
        database_port=None,
        database_name=None,
        database_user=None,
        database_password=None,
    )

    assert settings.openai_api_key is None
    assert settings.s3_bucket_name is None
    assert settings.database_url is None


def test_settings_build_database_url_from_parts() -> None:
    settings = Settings(
        database_url="",
        database_host="postgres",
        database_port=5432,
        database_name="ai_interview_coach",
        database_user="ai_interview",
        database_password="local_pw",
    )

    assert settings.database_url is not None
    assert settings.database_url.startswith("postgresql://ai_interview:")
    assert "local_pw" in settings.database_url
    assert settings.database_url.endswith("@postgres:5432/ai_interview_coach")


def test_settings_require_openai_api_key_in_production() -> None:
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        Settings(
            environment="production",
            openai_api_key="",
            database_url="postgresql://user:pw@host:5432/db",
        )


def test_settings_require_database_config_in_production() -> None:
    with pytest.raises(ValueError, match="Database configuration"):
        Settings(
            environment="production",
            openai_api_key="test-key",
            database_url="",
            database_host=None,
            database_port=None,
            database_name=None,
            database_user=None,
            database_password=None,
        )


def test_settings_allow_production_when_required_values_are_set() -> None:
    settings = Settings(
        environment="production",
        openai_api_key="test-key",
        database_url="postgresql://user:pw@host:5432/db",
    )

    assert settings.environment == "production"