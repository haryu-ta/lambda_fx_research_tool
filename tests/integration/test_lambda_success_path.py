"""Integration test for Lambda success path."""

from unittest.mock import MagicMock

from src.lambda_function import lambda_handler


def test_lambda_success_path(
    mock_env,
    mock_lambda_context,
    mock_requests_get,
    mock_requests_post,
    mock_exchange_rate_response,
):
    """Test successful Lambda execution end-to-end."""
    mock_requests_get.return_value = MagicMock(
        status_code=200, json=lambda: mock_exchange_rate_response
    )
    mock_requests_post.return_value = MagicMock(status_code=200, json=lambda: {"message": "sent"})

    # Execute Lambda
    event = {}
    result = lambda_handler(event, mock_lambda_context)

    # Verify success
    assert result["statusCode"] == 200
    assert "successfully" in result["body"].lower()

    assert mock_requests_get.call_count == 1
    assert mock_requests_post.call_count == 1


def test_lambda_exchange_rate_api_failure(
    mock_env, mock_lambda_context, mock_requests_get, mock_requests_post
):
    """Test Lambda execution when exchange rate API fails."""
    mock_requests_get.return_value = MagicMock(
        status_code=200, json=lambda: {"result": "error", "error-type": "invalid-key"}
    )
    mock_requests_post.return_value = MagicMock(status_code=200, json=lambda: {"message": "sent"})

    event = {}
    result = lambda_handler(event, mock_lambda_context)

    # Verify failure
    assert result["statusCode"] == 500
    assert "exchange rate fetch failed" in result["body"].lower()

    assert mock_requests_get.call_count == 1
    assert mock_requests_post.call_count == 1


def test_lambda_missing_config(mock_lambda_context, monkeypatch):
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


def test_lambda_invalid_rate_value(
    mock_env, mock_lambda_context, mock_requests_get, mock_requests_post
):
    """Test Lambda execution with invalid exchange rate value."""
    invalid_response = MagicMock(
        status_code=200,
        json=lambda: {
            "result": "success",
            "base_code": "USD",
            "conversion_rates": {"JPY": 0},  # Invalid: zero rate
            "time_last_update_utc": "2026-05-17T12:00:00Z",
        },
    )
    mock_requests_get.return_value = invalid_response
    mock_requests_post.return_value = MagicMock(status_code=200, json=lambda: {"message": "sent"})

    event = {}
    result = lambda_handler(event, mock_lambda_context)

    # Verify failure with invalid rate message
    assert result["statusCode"] == 400
    assert "exchange rate" in result["body"].lower()

    assert mock_requests_get.call_count == 1
    assert mock_requests_post.call_count == 1


def test_lambda_line_api_failure(
    mock_env,
    mock_lambda_context,
    mock_requests_get,
    mock_requests_post,
    mock_exchange_rate_response,
):
    """Test Lambda execution when LINE API fails."""
    mock_requests_get.return_value = MagicMock(
        status_code=200, json=lambda: mock_exchange_rate_response
    )
    mock_requests_post.return_value = MagicMock(status_code=401, text="Unauthorized")

    event = {}
    result = lambda_handler(event, mock_lambda_context)

    # Verify LINE failure
    assert result["statusCode"] == 500
    assert "line push failed" in result["body"].lower()
