"""Unit tests for exchange_service.py"""

import pytest
import requests

from src.exchange_service import ExchangeRateError, ExchangeRateService


def test_fetch_rate_success(mock_requests_get, mock_exchange_rate_response):
    """Test successful exchange rate fetch."""
    mock_requests_get.return_value.json.return_value = mock_exchange_rate_response

    service = ExchangeRateService(api_key="test-key")
    snapshot = service.fetch_rate()

    assert snapshot.base_currency == "USD"
    assert snapshot.target_currency == "JPY"
    assert snapshot.rate == 150.25
    assert snapshot.provider_status_code == 200

    mock_requests_get.assert_called_once()


def test_fetch_rate_api_error(mock_requests_get, mock_exchange_rate_error_response):
    """Test exchange rate fetch with API error."""
    mock_requests_get.return_value.json.return_value = mock_exchange_rate_error_response

    service = ExchangeRateService(api_key="test-key")

    with pytest.raises(ExchangeRateError) as exc_info:
        service.fetch_rate()

    assert "API error" in str(exc_info.value)


def test_fetch_rate_missing_jpy(mock_requests_get):
    """Test exchange rate fetch with missing JPY rate."""
    mock_requests_get.return_value.json.return_value = {
        "result": "success",
        "base_code": "USD",
        "conversion_rates": {
            "EUR": 0.92,
            "GBP": 0.79,
        },
    }

    service = ExchangeRateService(api_key="test-key")

    with pytest.raises(ExchangeRateError) as exc_info:
        service.fetch_rate()

    assert "JPY rate not found" in str(exc_info.value)


def test_fetch_rate_timeout(mock_requests_get):
    """Test exchange rate fetch with timeout."""
    mock_requests_get.side_effect = requests.Timeout("Connection timeout")

    service = ExchangeRateService(api_key="test-key")

    with pytest.raises(ExchangeRateError) as exc_info:
        service.fetch_rate()

    assert "timeout" in str(exc_info.value).lower()


def test_fetch_rate_connection_error(mock_requests_get):
    """Test exchange rate fetch with connection error."""
    mock_requests_get.side_effect = requests.ConnectionError("Connection refused")

    service = ExchangeRateService(api_key="test-key")

    with pytest.raises(ExchangeRateError) as exc_info:
        service.fetch_rate()

    assert "connection error" in str(exc_info.value).lower()


def test_fetch_rate_http_error(mock_requests_get):
    """Test exchange rate fetch with HTTP error."""
    mock_requests_get.return_value.status_code = 401
    mock_requests_get.return_value.raise_for_status.side_effect = requests.HTTPError("Unauthorized")

    service = ExchangeRateService(api_key="invalid-key")

    with pytest.raises(ExchangeRateError) as exc_info:
        service.fetch_rate()

    assert "request failed" in str(exc_info.value).lower()
