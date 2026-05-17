"""Data models for FX Rate LINE Notification."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator


class NotificationMessageType(str, Enum):
    """Enumeration of notification message types."""
    SUCCESS = "success"
    FX_API_NG = "fx_api_ng"
    FX_DATA_UNAVAILABLE = "fx_data_unavailable"
    FX_INFO_NG = "fx_info_ng"


class ExecutionLogLevel(str, Enum):
    """Enumeration of log levels."""
    INFO = "INFO"
    ERROR = "ERROR"


class ScheduleConfiguration(BaseModel):
    """Scheduled execution configuration model."""
    cron_expression: str = Field(..., description="EventBridge cron expression")
    timezone: str = Field(default="Asia/Tokyo", description="Timezone for schedule")
    retry_enabled: bool = Field(default=False, description="Auto-retry enabled flag")

    @validator("timezone")
    def validate_timezone(cls, v: str) -> str:
        """Validate that timezone is Asia/Tokyo.

        Args:
            v: Timezone value

        Returns:
            The validated timezone

        Raises:
            ValueError: If timezone is not Asia/Tokyo
        """
        if v != "Asia/Tokyo":
            raise ValueError("Only 'Asia/Tokyo' timezone is supported in v1")
        return v

    @validator("retry_enabled")
    def validate_retry_enabled(cls, v: bool) -> bool:
        """Validate that retry is disabled to prevent duplicate notifications.

        Args:
            v: Retry enabled flag

        Returns:
            False always (required by spec)

        Raises:
            ValueError: If retry_enabled is True
        """
        if v is True:
            raise ValueError("Automatic retry is disabled to prevent duplicate notifications")
        return False


class ExchangeRateSnapshot(BaseModel):
    """Normalized exchange rate API response model."""
    base_currency: str = Field(default="USD", description="Source currency")
    target_currency: str = Field(default="JPY", description="Target currency")
    rate: float = Field(..., description="Exchange rate (USD to JPY)")
    provider_timestamp: Optional[str] = Field(None, description="Provider timestamp")
    provider_status_code: int = Field(..., description="HTTP status code from provider")

    @validator("rate")
    def validate_rate(cls, v: float) -> float:
        """Validate that rate is a positive number.

        Args:
            v: Exchange rate value

        Returns:
            The validated rate

        Raises:
            ValueError: If rate is not positive
        """
        if v <= 0:
            raise ValueError("Exchange rate must be positive")
        return v


class NotificationMessage(BaseModel):
    """LINE notification message model."""
    message_type: NotificationMessageType = Field(..., description="Type of message")
    text: str = Field(..., description="Message text to send via LINE")
    display_time_hhmm: str = Field(..., description="Display time in HH:MM format (JST)")
    to_user_id: str = Field(..., description="LINE user ID recipient")

    @validator("display_time_hhmm")
    def validate_display_time(cls, v: str) -> str:
        """Validate HH:MM format.

        Args:
            v: Time string

        Returns:
            The validated time

        Raises:
            ValueError: If not in HH:MM format
        """
        if not isinstance(v, str) or len(v) != 5 or v[2] != ":":
            raise ValueError("display_time_hhmm must be in HH:MM format")
        try:
            hour, minute = v.split(":")
            h = int(hour)
            m = int(minute)
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError()
        except (ValueError, IndexError):
            raise ValueError("display_time_hhmm must be valid time (00:00-23:59)")
        return v


class ExecutionLogRecord(BaseModel):
    """Structured execution log record model."""
    execution_id: str = Field(..., description="Unique execution identifier")
    level: ExecutionLogLevel = Field(..., description="Log level")
    event_type: str = Field(..., description="Event type (rate_fetch, line_push, etc)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    details: Optional[dict] = Field(None, description="Additional event details")

    @validator("level")
    def validate_error_has_details(cls, v: ExecutionLogLevel, values: dict) -> ExecutionLogLevel:
        """Validate that ERROR logs include details.

        Args:
            v: Log level
            values: Other field values

        Returns:
            The validated level

        Raises:
            ValueError: If ERROR log without details
        """
        if v == ExecutionLogLevel.ERROR and not values.get("details"):
            raise ValueError("ERROR logs must include details")
        return v
