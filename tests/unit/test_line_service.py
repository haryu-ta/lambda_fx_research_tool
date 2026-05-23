"""Unit tests for line_service.py"""

import pytest
import requests

from src.line_service import LineServiceError, LineService
from src.models import NotificationMessage, NotificationMessageType


def test_format_success_message():
    """Test success message formatting."""
    service = LineService(channel_access_token="test-token")

    message = service.format_success_message(150.25, "09:00")

    assert message.message_type == NotificationMessageType.SUCCESS
    assert message.text == "09:00時点\n        1ドル = 150.25 円"
    assert message.display_time_hhmm == "09:00"


def test_format_fx_api_error_message():
    """Test FX API error message formatting."""
    service = LineService(channel_access_token="test-token")

    message = service.format_fx_api_error_message("14:30")

    assert message.message_type == NotificationMessageType.FX_API_NG
    assert message.text == "14:30時点  為替API　実行NG"


def test_format_fx_data_unavailable_message():
    """Test FX data unavailable message formatting."""
    service = LineService(channel_access_token="test-token")

    message = service.format_fx_data_unavailable_message("12:00")

    assert message.message_type == NotificationMessageType.FX_DATA_UNAVAILABLE
    assert message.text == "12:00時点  為替情報取得できず"


def test_format_fx_info_error_message():
    """Test FX info error message formatting."""
    service = LineService(channel_access_token="test-token")

    message = service.format_fx_info_error_message("18:45")

    assert message.message_type == NotificationMessageType.FX_INFO_NG
    assert message.text == "18:45時点  為替情報取得NG"


def test_send_push_message_success(mock_requests_post):
    """Test successful push message send."""
    mock_requests_post.return_value.status_code = 200

    service = LineService(channel_access_token="test-token")
    message = NotificationMessage(
        message_type=NotificationMessageType.SUCCESS,
        text="09:00時点  1ドル = 150.25 円",
        display_time_hhmm="09:00",
        to_user_id="test-user-id",
    )

    result = service.send_push_message(message)

    assert result is True
    mock_requests_post.assert_called_once()
    call_kwargs = mock_requests_post.call_args.kwargs
    assert call_kwargs["json"]["to"] == "test-user-id"
    assert call_kwargs["json"]["messages"][0]["text"] == "09:00時点  1ドル = 150.25 円"


def test_send_push_message_api_error(mock_requests_post):
    """Test push message send with API error."""
    mock_requests_post.return_value.status_code = 401
    mock_requests_post.return_value.text = "Unauthorized"

    service = LineService(channel_access_token="invalid-token")
    message = NotificationMessage(
        message_type=NotificationMessageType.SUCCESS,
        text="Test message",
        display_time_hhmm="09:00",
        to_user_id="test-user-id",
    )

    with pytest.raises(LineServiceError) as exc_info:
        service.send_push_message(message)

    assert "401" in str(exc_info.value)


def test_send_push_message_timeout(mock_requests_post):
    """Test push message send with timeout."""
    mock_requests_post.side_effect = requests.Timeout("Request timeout")

    service = LineService(channel_access_token="test-token")
    message = NotificationMessage(
        message_type=NotificationMessageType.SUCCESS,
        text="Test message",
        display_time_hhmm="09:00",
        to_user_id="test-user-id",
    )

    with pytest.raises(LineServiceError) as exc_info:
        service.send_push_message(message)

    assert "timeout" in str(exc_info.value).lower()
