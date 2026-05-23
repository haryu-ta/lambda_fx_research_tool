"""Integration test for invalid FX data path."""

from unittest.mock import MagicMock

from src.lambda_function import lambda_handler


def test_lambda_fx_data_invalid_sends_unavailable_message(
    mock_env, mock_lambda_context, mock_requests_get, mock_requests_post
):
    mock_requests_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "result": "success",
            "base_code": "USD",
            "conversion_rates": {"JPY": 0},
            "time_last_update_utc": "2026-05-17T12:00:00Z",
        },
    )
    mock_requests_post.return_value = MagicMock(status_code=200, json=lambda: {"message": "sent"})

    result = lambda_handler({}, mock_lambda_context)

    assert result["statusCode"] == 400
    assert "invalid exchange rate data" in result["body"].lower()
    sent_text = mock_requests_post.call_args.kwargs["json"]["messages"][0]["text"]
    assert sent_text.endswith("為替情報取得できず")
