"""Integration test for LINE push failure path."""

from unittest.mock import MagicMock

from src.lambda_function import lambda_handler


def test_lambda_line_failure_returns_500(
    mock_env,
    mock_lambda_context,
    mock_requests_get,
    mock_requests_post,
    mock_exchange_rate_response,
):
    mock_requests_get.return_value = MagicMock(
        status_code=200, json=lambda: mock_exchange_rate_response
    )
    mock_requests_post.return_value = MagicMock(status_code=401, text="Unauthorized")

    result = lambda_handler({}, mock_lambda_context)

    assert result["statusCode"] == 500
    assert "line push failed" in result["body"].lower()
