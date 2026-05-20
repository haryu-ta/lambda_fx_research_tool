"""Lambda function entry point for FX Rate LINE Notification."""

from datetime import datetime, timezone, timedelta
from typing import Any, Dict

from aws_lambda_powertools.utilities.typing import LambdaContext

from src.config import ConfigError, get_config
from src.exchange_service import (
    ExchangeRateApiError,
    ExchangeRateDataError,
    ExchangeRateError,
    create_exchange_service,
)
from src.line_service import LineServiceError, create_line_service
from src.logger import (
    create_execution_id,
    get_logger,
    log_config_error,
    log_execution_start,
    log_line_push_failure,
    log_line_push_success,
    log_rate_fetch_failure,
    log_rate_fetch_success,
    log_validation_error,
)


def _get_jst_time_hhmm() -> str:
    """Get current time in HH:MM format (JST).

    Returns:
        Time string in HH:MM format
    """
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    now_jst = now_utc + timedelta(hours=9)
    return now_jst.strftime("%H:%M")


def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """AWS Lambda handler for FX Rate notification.

    This is the entry point for scheduled Lambda invocations via EventBridge.
    It orchestrates the exchange rate fetch, message formatting, and LINE push.

    Args:
        event: Lambda event (EventBridge scheduled event)
        context: Lambda context object

    Returns:
        Dict with statusCode and body
    """
    # Initialize
    execution_id = create_execution_id()
    logger = get_logger()
    log_execution_start(logger, execution_id, event, context)

    try:
        # 1. Validate configuration
        try:
            config = get_config()
        except ConfigError as e:
            log_config_error(logger, execution_id, str(e))
            return {
                "statusCode": 500,
                "body": f"Configuration error: {str(e)}",
            }

        # Get JST time for display
        display_time = _get_jst_time_hhmm()

        # 2. Fetch exchange rate
        try:
            exchange_service = create_exchange_service(config)
            rate_snapshot = exchange_service.fetch_rate()

            # Validate rate
            if rate_snapshot.rate is None or rate_snapshot.rate <= 0:
                log_validation_error(
                    logger,
                    execution_id,
                    "Invalid exchange rate value",
                    {"rate": rate_snapshot.rate},
                )
                # Send error notification: invalid rate
                line_service = create_line_service(config)
                error_msg = line_service.format_fx_data_unavailable_message(display_time)
                error_msg.to_user_id = config.line_to_user_id
                line_service.send_push_message(error_msg)
                return {
                    "statusCode": 400,
                    "body": "Invalid exchange rate",
                }

        except ExchangeRateDataError as e:
            log_validation_error(logger, execution_id, str(e))
            try:
                line_service = create_line_service(config)
                error_msg = line_service.format_fx_data_unavailable_message(display_time)
                error_msg.to_user_id = config.line_to_user_id
                line_service.send_push_message(error_msg)
            except LineServiceError as le:
                log_line_push_failure(logger, execution_id, str(le), {"original_error": str(e)})
            return {
                "statusCode": 400,
                "body": f"Invalid exchange rate data: {str(e)}",
            }

        except ExchangeRateApiError as e:
            log_rate_fetch_failure(logger, execution_id, str(e))
            # Send error notification: FX API error
            try:
                line_service = create_line_service(config)
                error_msg = line_service.format_fx_api_error_message(display_time)
                error_msg.to_user_id = config.line_to_user_id
                line_service.send_push_message(error_msg)
            except LineServiceError as le:
                log_line_push_failure(logger, execution_id, str(le), {"original_error": str(e)})
            return {
                "statusCode": 500,
                "body": f"Exchange rate fetch failed: {str(e)}",
            }

        except ExchangeRateError as e:
            log_rate_fetch_failure(logger, execution_id, str(e))
            return {
                "statusCode": 500,
                "body": f"Exchange rate fetch failed: {str(e)}",
            }

        log_rate_fetch_success(
            logger,
            execution_id,
            rate_snapshot.rate,
            rate_snapshot.provider_timestamp or "N/A",
        )

        # 3. Format and send success notification
        try:
            line_service = create_line_service(config)
            success_msg = line_service.format_success_message(rate_snapshot.rate, display_time)
            success_msg.to_user_id = config.line_to_user_id
            line_service.send_push_message(success_msg)

            log_line_push_success(logger, execution_id, success_msg.text, display_time)

            return {
                "statusCode": 200,
                "body": "Notification sent successfully",
            }

        except LineServiceError as e:
            log_line_push_failure(logger, execution_id, str(e))
            return {
                "statusCode": 500,
                "body": f"LINE push failed: {str(e)}",
            }

    except Exception as e:
        logger.error(
            "Unexpected Lambda execution error",
            extra={
                "execution_id": execution_id,
                "error": str(e),
                "error_type": type(e).__name__,
            },
        )
        return {
            "statusCode": 500,
            "body": f"Unexpected error: {str(e)}",
        }
