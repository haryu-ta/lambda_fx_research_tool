"""Configuration and environment variable management."""

import os
from typing import Optional


class ConfigError(Exception):
    """Raised when required configuration is missing or invalid."""

    pass


class Config:
    """Application configuration loaded from environment variables."""

    def __init__(self):
        """Initialize configuration and validate all required variables."""
        self.exchange_rate_api_key = self._get_required_env("EXCHANGE_RATE_API_KEY")
        self.exchange_rate_provider = self.validate_exchange_rate_provider(
            self._get_optional_env("EXCHANGE_RATE_PROVIDER", "open_exchange_rates")
        )
        self.exchange_rate_base_url = self._get_optional_env(
            "OPEN_EXCHANGE_RATES_BASE_URL",
            "https://openexchangerates.org/api/latest.json",
        )
        self.line_channel_access_token = self._get_required_env("LINE_CHANNEL_ACCESS_TOKEN")
        self.line_to_user_id = self._get_required_env("LINE_TO_USER_ID")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    @staticmethod
    def _get_required_env(name: str) -> str:
        """Get a required environment variable.

        Args:
            name: Environment variable name

        Returns:
            The environment variable value

        Raises:
            ConfigError: If the variable is not set or is empty
        """
        value = os.getenv(name)
        if not value or not value.strip():
            raise ConfigError(
                f"Required environment variable '{name}' is not set or is empty. "
                f"Please set it in your environment or .env file."
            )
        return value

    @staticmethod
    def _get_optional_env(name: str, default: Optional[str] = None) -> Optional[str]:
        """Get an optional environment variable.

        Args:
            name: Environment variable name
            default: Default value if not set

        Returns:
            The environment variable value or default
        """
        return os.getenv(name, default)

    @staticmethod
    def validate_schedule_timezone(timezone_name: str) -> str:
        """Validate schedule timezone.

        Args:
            timezone_name: Timezone name to validate

        Returns:
            The validated timezone name

        Raises:
            ConfigError: If timezone is not Asia/Tokyo
        """
        if timezone_name != "Asia/Tokyo":
            raise ConfigError("Schedule timezone must be 'Asia/Tokyo'.")
        return timezone_name

    @staticmethod
    def validate_exchange_rate_provider(provider_name: Optional[str]) -> str:
        """Validate exchange rate provider.

        Args:
            provider_name: Provider name to validate

        Returns:
            Normalized provider name

        Raises:
            ConfigError: If provider is unsupported
        """
        normalized = (provider_name or "").strip().lower()
        if normalized != "open_exchange_rates":
            raise ConfigError("EXCHANGE_RATE_PROVIDER must be 'open_exchange_rates'.")
        return normalized


# Singleton instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance.

    Raises:
        ConfigError: If configuration is invalid

    Returns:
        The Config instance
    """
    global _config
    if _config is None:
        _config = Config()
    return _config
