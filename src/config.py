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
