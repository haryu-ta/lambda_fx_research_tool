"""LINE Messaging API service for sending notifications."""

from datetime import datetime
from typing import Optional

import requests
from pydantic import ValidationError

from src.config import Config
from src.models import NotificationMessage, NotificationMessageType


class LineServiceError(Exception):
    """Raised when LINE service operation fails."""
    pass


class LineService:
    """Service for sending messages via LINE Messaging API."""

    BASE_URL = "https://api.line.me/v2/bot/message/push"
    DEFAULT_TIMEOUT = 10  # seconds

    def __init__(self, channel_access_token: str):
        """Initialize the service with channel access token.

        Args:
            channel_access_token: LINE Channel Access Token
        """
        self.channel_access_token = channel_access_token

    def send_push_message(self, message: NotificationMessage) -> bool:
        """Send a push message to a LINE user.

        Args:
            message: NotificationMessage to send

        Returns:
            True if message sent successfully

        Raises:
            LineServiceError: If push fails
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.channel_access_token}",
                "Content-Type": "application/json",
            }

            payload = {
                "to": message.to_user_id,
                "messages": [
                    {
                        "type": "text",
                        "text": message.text,
                    }
                ],
            }

            response = requests.post(
                self.BASE_URL,
                json=payload,
                headers=headers,
                timeout=self.DEFAULT_TIMEOUT,
            )

            # Check for successful response
            if response.status_code != 200:
                error_body = response.text
                raise LineServiceError(
                    f"LINE API error: status={response.status_code}, body={error_body}"
                )

            return True

        except requests.RequestException as e:
            if isinstance(e, requests.Timeout):
                raise LineServiceError(f"LINE API request timeout: {str(e)}")
            elif isinstance(e, requests.ConnectionError):
                raise LineServiceError(f"LINE API connection error: {str(e)}")
            else:
                raise LineServiceError(f"LINE API request failed: {str(e)}")

    def format_success_message(self, rate: float, timestamp_jst: str) -> NotificationMessage:
        """Format a success notification message.

        Args:
            rate: USD/JPY exchange rate
            timestamp_jst: Current time in HH:MM format (JST)

        Returns:
            NotificationMessage for success case

        Raises:
            NotificationMessageError: If message format is invalid
        """
        text = f"{timestamp_jst}時点  1ドル = {rate:.2f} 円"
        return NotificationMessage(
            message_type=NotificationMessageType.SUCCESS,
            text=text,
            display_time_hhmm=timestamp_jst,
            to_user_id="",  # Will be filled by caller
        )

    def format_fx_api_error_message(self, timestamp_jst: str) -> NotificationMessage:
        """Format FX API error notification message.

        Args:
            timestamp_jst: Current time in HH:MM format (JST)

        Returns:
            NotificationMessage for FX API error
        """
        text = f"{timestamp_jst}時点  為替API　実行NG"
        return NotificationMessage(
            message_type=NotificationMessageType.FX_API_NG,
            text=text,
            display_time_hhmm=timestamp_jst,
            to_user_id="",  # Will be filled by caller
        )

    def format_fx_data_unavailable_message(self, timestamp_jst: str) -> NotificationMessage:
        """Format FX data unavailable notification message.

        Args:
            timestamp_jst: Current time in HH:MM format (JST)

        Returns:
            NotificationMessage for FX data unavailable
        """
        text = f"{timestamp_jst}時点  為替情報取得できず"
        return NotificationMessage(
            message_type=NotificationMessageType.FX_DATA_UNAVAILABLE,
            text=text,
            display_time_hhmm=timestamp_jst,
            to_user_id="",  # Will be filled by caller
        )

    def format_fx_info_error_message(self, timestamp_jst: str) -> NotificationMessage:
        """Format FX info error notification message (missing/empty credentials).

        Args:
            timestamp_jst: Current time in HH:MM format (JST)

        Returns:
            NotificationMessage for FX info error
        """
        text = f"{timestamp_jst}時点  為替情報取得NG"
        return NotificationMessage(
            message_type=NotificationMessageType.FX_INFO_NG,
            text=text,
            display_time_hhmm=timestamp_jst,
            to_user_id="",  # Will be filled by caller
        )


def create_line_service(config: Config) -> LineService:
    """Factory function to create a LINE service.

    Args:
        config: Application configuration

    Returns:
        LineService instance
    """
    return LineService(channel_access_token=config.line_channel_access_token)
