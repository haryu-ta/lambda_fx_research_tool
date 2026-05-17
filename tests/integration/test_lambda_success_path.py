"""Integration test for Lambda success path."""

from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

import pytest

from src.lambda_function import lambda_handler


def test_lambda_success_path(mock_env, mock_lambda_context, mock_requests_post, mock_exchange_rate_response):
    """Test successful Lambda execution end-to-end."""
    # Mock both exchange rate and LINE APIs
    mock_responses = [
        MagicMock(status_code=200, json=lambda: mock_exchange_rate_response),  # Exchange rate API
        MagicMock(status_code=200, json=lambda: {"message": "sent"}),  # LINE API
    ]
    mock_requests_post.side_effect = mock_responses

    # Execute Lambda
    event = {}
    result = lambda_handler(event, mock_lambda_context)

    # Verify success
    assert result["statusCode"] == 200
    assert "successfully" in result["body"].lower()

    # Verify both APIs were called
    assert mock_requests_post.call_count == 2


def test_lambda_exchange_rate_api_failure(mock_env, mock_lambda_context, mock_requests_post):
    """Test Lambda execution when exchange rate API fails."""
    # First call fails (exchange rate), second succeeds (error notification)
    failure_response = MagicMock(status_code=200, json=lambda: {"result": "error", "error-type": "invalid-key"})
    success_response = MagicMock(status_code=200, json=lambda: {"message": "sent"})
    mock_requests_post.side_effect = [failure_response, success_response]

    event = {}
    result = lambda_handler(event, mock_lambda_context)

    # Verify failure
    assert result["statusCode"] == 500
    assert "exchange rate fetch failed" in result["body"].lower()

    # Verify error notification was sent
    assert mock_requests_post.call_count == 2


def test_lambda_missing_config(mock_lambda_context, mock_requests_post, monkeypatch):
    """Test Lambda execution with missing configuration."""
    # Remove all required env vars
    monkeypatch.delenv("EXCHANGE_RATE_API_KEY", raising=False)
    monkeypatch.delenv("LINE_CHANNEL_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("LINE_TO_USER_ID", raising=False)

    # Reset the config singleton
    import src.config
    src.config._config = None

    event = {}
    result = lambda_handler(event, mock_lambda_context)

    # Verify config error
    assert result["statusCode"] == 500
    assert "configuration error" in result["body"].lower()


def test_lambda_invalid_rate_value(mock_env, mock_lambda_context, mock_requests_post):
    """Test Lambda execution with invalid exchange rate value."""
    # Mock API response with zero/negative rate
    invalid_response = MagicMock(
        status_code=200,
        json=lambda: {
            "result": "success",
            "base_code": "USD",
            "conversion_rates": {"JPY": 0},  # Invalid: zero rate
            "time_last_update_utc": "2026-05-17T12:00:00Z",
        },
    )
    success_response = MagicMock(status_code=200, json=lambda: {"message": "sent"})
    mock_requests_post.side_effect = [invalid_response, success_response]

    event = {}
    result = lambda_handler(event, mock_lambda_context)

    # Verify failure with invalid rate message
    assert result["statusCode"] == 400
    assert "exchange rate" in result["body"].lower()

    # Verify error notification was sent
    assert mock_requests_post.call_count == 2


def test_lambda_line_api_failure(mock_env, mock_lambda_context, mock_requests_post, mock_exchange_rate_response):
    """Test Lambda execution when LINE API fails."""
    # First call succeeds (exchange rate), second fails (LINE push)
    success_response = MagicMock(status_code=200, json=lambda: mock_exchange_rate_response)
    failure_response = MagicMock(status_code=401, text="Unauthorized")
    mock_requests_post.side_effect = [success_response, failure_response]

    event = {}
    result = lambda_handler(event, mock_lambda_context)

    # Verify LINE failure
    assert result["statusCode"] == 500
    assert "line push failed" in result["body"].lower()
