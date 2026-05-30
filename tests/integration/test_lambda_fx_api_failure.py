"""Integration test for FX API failure path."""

from unittest.mock import MagicMock
import requests

from src.lambda_function import lambda_handler


def test_lambda_fx_api_failure_sends_error_notification(
    mock_env, mock_lambda_context, mock_requests_get, mock_requests_post
):
    mock_requests_get.return_value = MagicMock(status_code=401, json=lambda: {})
    mock_requests_get.return_value.raise_for_status.side_effect = requests.HTTPError("Unauthorized")
    mock_requests_post.return_value = MagicMock(status_code=200, json=lambda: {"message": "sent"})

    result = lambda_handler({}, mock_lambda_context)

    assert result["statusCode"] == 500
    assert "exchange rate fetch failed" in result["body"].lower()
    sent_text = mock_requests_post.call_args.kwargs["json"]["messages"][0]["text"]
    assert sent_text.endswith("為替API　実行NG")
