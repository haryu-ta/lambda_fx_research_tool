"""Exchange rate fetching service using Open Exchange Rates."""

import requests
from pydantic import ValidationError

from src.config import Config
from src.models import ExchangeRateSnapshot, OpenExchangeRateResponse


class ExchangeRateError(Exception):
    """Raised when exchange rate fetch fails."""

    pass


class ExchangeRateApiError(ExchangeRateError):
    """Raised when exchange rate provider API call fails."""

    pass


class ExchangeRateDataError(ExchangeRateError):
    """Raised when exchange rate provider data is invalid."""

    pass


class ExchangeRateService:
    """Service for fetching USD/JPY exchange rates."""

    BASE_URL = "https://openexchangerates.org/api/latest.json"
    DEFAULT_TIMEOUT = 10  # seconds

    def __init__(self, api_key: str, base_url: str = BASE_URL):
        """Initialize the service with API key.

        Args:
            api_key: Open Exchange Rates app_id
            base_url: API endpoint URL
        """
        self.api_key = api_key
        self.base_url = base_url

    def fetch_rate(self) -> ExchangeRateSnapshot:
        """Fetch the latest USD/JPY exchange rate.

        Returns:
            ExchangeRateSnapshot with rate data

        Raises:
            ExchangeRateError: If fetch fails or response is invalid
        """
        try:
            response = requests.get(
                self.base_url,
                params={"app_id": self.api_key, "base": "USD", "symbols": "JPY"},
                timeout=self.DEFAULT_TIMEOUT,
            )

            if response.status_code == 429:
                raise ExchangeRateApiError("API throttling detected")

            response.raise_for_status()

            data = response.json()

            provider_response = OpenExchangeRateResponse(**data)
            jpy_rate = provider_response.rates["JPY"]

            # Create and validate snapshot
            snapshot = ExchangeRateSnapshot(
                base_currency=provider_response.base,
                target_currency="JPY",
                rate=float(jpy_rate),
                provider_timestamp=str(provider_response.timestamp),
                provider_status_code=response.status_code,
            )

            return snapshot

        except ExchangeRateApiError:
            raise

        except requests.RequestException as e:
            response = getattr(e, "response", None)
            status_code = getattr(response, "status_code", None)

            if status_code == 429:
                raise ExchangeRateApiError("API throttling detected")

            if isinstance(e, requests.Timeout):
                raise ExchangeRateApiError(f"API request timeout: {str(e)}")
            elif isinstance(e, requests.ConnectionError):
                raise ExchangeRateApiError(f"API connection error: {str(e)}")
            else:
                suffix = f" (status={status_code})" if status_code else ""
                raise ExchangeRateApiError(f"API request failed{suffix}: {str(e)}")

        except (ValueError, KeyError) as e:
            raise ExchangeRateDataError(f"Invalid API response format: {str(e)}")

        except ValidationError as e:
            raise ExchangeRateDataError(f"Invalid exchange rate data: {str(e)}")


def create_exchange_service(config: Config) -> ExchangeRateService:
    """Factory function to create an exchange rate service.

    Args:
        config: Application configuration

    Returns:
        ExchangeRateService instance
    """
    return ExchangeRateService(
        api_key=config.exchange_rate_api_key,
        base_url=config.exchange_rate_base_url,
    )
