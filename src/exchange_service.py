"""Exchange rate fetching service using ExchangeRate-API."""

from datetime import datetime
from typing import Optional

import requests
from pydantic import ValidationError

from src.config import Config
from src.models import ExchangeRateSnapshot


class ExchangeRateError(Exception):
    """Raised when exchange rate fetch fails."""
    pass


class ExchangeRateService:
    """Service for fetching USD/JPY exchange rates."""

    BASE_URL = "https://v6.exchangerate-api.com/v6"
    DEFAULT_TIMEOUT = 10  # seconds

    def __init__(self, api_key: str):
        """Initialize the service with API key.

        Args:
            api_key: ExchangeRate-API key
        """
        self.api_key = api_key

    def fetch_rate(self) -> ExchangeRateSnapshot:
        """Fetch the latest USD/JPY exchange rate.

        Returns:
            ExchangeRateSnapshot with rate data

        Raises:
            ExchangeRateError: If fetch fails or response is invalid
        """
        try:
            # Call ExchangeRate-API
            url = f"{self.BASE_URL}/{self.api_key}/latest/USD"
            response = requests.get(url, timeout=self.DEFAULT_TIMEOUT)
            response.raise_for_status()

            data = response.json()

            # Validate response structure
            if data.get("result") != "success":
                error_type = data.get("error-type", "unknown")
                raise ExchangeRateError(f"API error: {error_type}")

            # Extract JPY rate
            rates = data.get("conversion_rates", {})
            jpy_rate = rates.get("JPY")

            if jpy_rate is None:
                raise ExchangeRateError("JPY rate not found in API response")

            # Create and validate snapshot
            snapshot = ExchangeRateSnapshot(
                base_currency=data.get("base_code", "USD"),
                target_currency="JPY",
                rate=float(jpy_rate),
                provider_timestamp=data.get("time_last_update_utc"),
                provider_status_code=response.status_code,
            )

            return snapshot

        except requests.RequestException as e:
            # Handle HTTP errors, timeouts, etc.
            if isinstance(e, requests.Timeout):
                raise ExchangeRateError(f"API request timeout: {str(e)}")
            elif isinstance(e, requests.ConnectionError):
                raise ExchangeRateError(f"API connection error: {str(e)}")
            else:
                raise ExchangeRateError(f"API request failed: {str(e)}")

        except (ValueError, KeyError) as e:
            # Handle JSON parsing errors
            raise ExchangeRateError(f"Invalid API response format: {str(e)}")

        except ValidationError as e:
            # Handle Pydantic validation errors
            raise ExchangeRateError(f"Invalid exchange rate data: {str(e)}")


def create_exchange_service(config: Config) -> ExchangeRateService:
    """Factory function to create an exchange rate service.

    Args:
        config: Application configuration

    Returns:
        ExchangeRateService instance
    """
    return ExchangeRateService(api_key=config.exchange_rate_api_key)
