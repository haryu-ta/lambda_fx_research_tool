"""Unit tests for error message formatting."""

from src.line_service import LineService
from src.models import NotificationMessageType


def test_fx_api_error_message_contract():
    service = LineService(channel_access_token="test-token")
    msg = service.format_fx_api_error_message("09:00")

    assert msg.message_type == NotificationMessageType.FX_API_NG
    assert msg.text == "09:00時点  為替API　実行NG"


def test_fx_data_unavailable_message_contract():
    service = LineService(channel_access_token="test-token")
    msg = service.format_fx_data_unavailable_message("09:00")

    assert msg.message_type == NotificationMessageType.FX_DATA_UNAVAILABLE
    assert msg.text == "09:00時点  為替情報取得できず"


def test_fx_info_error_message_contract():
    service = LineService(channel_access_token="test-token")
    msg = service.format_fx_info_error_message("09:00")

    assert msg.message_type == NotificationMessageType.FX_INFO_NG
    assert msg.text == "09:00時点  為替情報取得NG"
