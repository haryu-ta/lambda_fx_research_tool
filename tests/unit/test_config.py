"""Unit tests for config.py"""

import pytest

from src.config import Config, ConfigError, get_config


def test_config_initialization_success(mock_env):
    """Test successful configuration initialization."""
    config = Config()

    assert config.exchange_rate_api_key == "test-api-key-12345"
    assert config.line_channel_access_token == "test-channel-token-xyz"
    assert config.line_to_user_id == "test-user-id-abc"


def test_config_missing_exchange_rate_key(monkeypatch):
    """Test configuration with missing exchange rate API key."""
    monkeypatch.delenv("EXCHANGE_RATE_API_KEY", raising=False)
    monkeypatch.setenv("LINE_CHANNEL_ACCESS_TOKEN", "test-token")
    monkeypatch.setenv("LINE_TO_USER_ID", "test-user")

    with pytest.raises(ConfigError) as exc_info:
        Config()

    assert "EXCHANGE_RATE_API_KEY" in str(exc_info.value)


def test_config_missing_line_token(monkeypatch):
    """Test configuration with missing LINE token."""
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "test-key")
    monkeypatch.delenv("LINE_CHANNEL_ACCESS_TOKEN", raising=False)
    monkeypatch.setenv("LINE_TO_USER_ID", "test-user")

    with pytest.raises(ConfigError) as exc_info:
        Config()

    assert "LINE_CHANNEL_ACCESS_TOKEN" in str(exc_info.value)


def test_config_missing_line_user_id(monkeypatch):
    """Test configuration with missing LINE user ID."""
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "test-key")
    monkeypatch.setenv("LINE_CHANNEL_ACCESS_TOKEN", "test-token")
    monkeypatch.delenv("LINE_TO_USER_ID", raising=False)

    with pytest.raises(ConfigError) as exc_info:
        Config()

    assert "LINE_TO_USER_ID" in str(exc_info.value)


def test_config_empty_value(monkeypatch):
    """Test configuration with empty environment variable value."""
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "")
    monkeypatch.setenv("LINE_CHANNEL_ACCESS_TOKEN", "test-token")
    monkeypatch.setenv("LINE_TO_USER_ID", "test-user")

    with pytest.raises(ConfigError) as exc_info:
        Config()

    assert "EXCHANGE_RATE_API_KEY" in str(exc_info.value)


def test_get_config_singleton(mock_env):
    """Test that get_config returns singleton instance."""
    config1 = get_config()
    config2 = get_config()

    assert config1 is config2
