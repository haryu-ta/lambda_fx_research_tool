"""Test configuration and fixtures."""

import os
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_env(monkeypatch):
    """Set up mock environment variables for tests.

    Args:
        monkeypatch: pytest monkeypatch fixture

    Yields:
        Dictionary of mock environment variables
    """
    env_vars = {
        "EXCHANGE_RATE_API_KEY": "test-api-key-12345",
        "LINE_CHANNEL_ACCESS_TOKEN": "test-channel-token-xyz",
        "LINE_TO_USER_ID": "test-user-id-abc",
        "LOG_LEVEL": "INFO",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    yield env_vars


@pytest.fixture(autouse=True)
def reset_config_singleton():
    """Reset singleton config between tests to avoid cross-test contamination."""
    import src.config

    src.config._config = None
    yield
    src.config._config = None


@pytest.fixture
def mock_lambda_context():
    """Create a mock Lambda context.

    Returns:
        Mocked LambdaContext object
    """
    context = MagicMock()
    context.aws_request_id = "test-request-id-123"
    context.function_name = "test-function"
    context.memory_limit_in_mb = 128
    context.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789:function:test"
    context.get_remaining_time_in_millis = MagicMock(return_value=30000)
    return context


@pytest.fixture
def mock_exchange_rate_response():
    """Create a mock ExchangeRate-API response.

    Returns:
        Dictionary representing valid API response
    """
    return {
        "result": "success",
        "base_code": "USD",
        "time_last_update_utc": "2026-05-17T12:00:00Z",
        "conversion_rates": {
            "JPY": 150.25,
        },
    }


@pytest.fixture
def mock_exchange_rate_error_response():
    """Create a mock ExchangeRate-API error response.

    Returns:
        Dictionary representing error API response
    """
    return {
        "result": "error",
        "error-type": "invalid-key",
    }


@pytest.fixture
def mock_line_push_success_response():
    """Create a mock LINE Messaging API push success response.

    Returns:
        Dictionary representing successful push response
    """
    return {"message": "message sent"}


@pytest.fixture
def mock_requests_post(mocker):
    """Mock requests.post for external API calls.

    Args:
        mocker: pytest-mock fixture

    Returns:
        Mocked requests.post callable
    """
    mock = mocker.patch("requests.post")
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = {"result": "success"}
    return mock


@pytest.fixture
def mock_requests_get(mocker):
    """Mock requests.get for external API calls.

    Args:
        mocker: pytest-mock fixture

    Returns:
        Mocked requests.get callable
    """
    mock = mocker.patch("requests.get")
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = {"result": "success"}
    return mock
