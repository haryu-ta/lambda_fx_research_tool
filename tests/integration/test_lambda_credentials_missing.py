"""Integration test for missing credentials path."""

from src.lambda_function import lambda_handler


def test_lambda_credentials_missing_returns_config_error(mock_lambda_context, monkeypatch):
    monkeypatch.delenv("EXCHANGE_RATE_API_KEY", raising=False)
    monkeypatch.delenv("LINE_CHANNEL_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("LINE_TO_USER_ID", raising=False)

    result = lambda_handler({}, mock_lambda_context)

    assert result["statusCode"] == 500
    assert "configuration error" in result["body"].lower()
