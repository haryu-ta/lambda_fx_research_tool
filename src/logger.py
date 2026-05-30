"""Structured logging configuration using AWS Lambda Powertools."""

from datetime import datetime, timezone
import uuid
from typing import Any, Dict, Optional

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

# Global logger instance
_logger: Optional[Logger] = None


def _now_iso() -> str:
    """Return current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def get_logger() -> Logger:
    """Get the global logger instance.

    Returns:
        Logger instance configured with Lambda Powertools
    """
    global _logger
    if _logger is None:
        _logger = Logger()
    return _logger


def configure_logger(log_level: str = "INFO") -> Logger:
    """Configure the logger with specified level.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured Logger instance
    """
    logger = get_logger()
    logger.setLevel(log_level)
    return logger


def create_execution_id() -> str:
    """Generate a unique execution ID for this Lambda invocation.

    Returns:
        UUID string for tracking execution flow
    """
    return str(uuid.uuid4())


def log_execution_start(
    logger: Logger,
    execution_id: str,
    event: Dict[str, Any],
    context: Optional[LambdaContext] = None,
) -> None:
    """Log Lambda execution start with context.

    Args:
        logger: Logger instance
        execution_id: Unique execution ID
        event: Lambda event payload
        context: Lambda context object
    """
    logger.info(
        "Lambda execution started",
        extra={
            "execution_id": execution_id,
            "request_id": context.aws_request_id if context else "N/A",
            "function_name": context.function_name if context else "N/A",
            "event_type": "execution_start",
            "timestamp": _now_iso(),
            "details": {"event": event},
        },
    )


def log_rate_fetch_success(
    logger: Logger,
    execution_id: str,
    rate: float,
    timestamp: str,
    provider: str = "open_exchange_rates",
    mapping_details: Optional[Dict[str, Any]] = None,
) -> None:
    """Log successful exchange rate fetch.

    Args:
        logger: Logger instance
        execution_id: Unique execution ID
        rate: Fetched exchange rate
        timestamp: Fetch timestamp
    """
    logger.info(
        "Exchange rate fetched successfully",
        extra={
            "execution_id": execution_id,
            "rate": rate,
            "timestamp": timestamp,
            "provider": provider,
            "event_type": "rate_fetch",
            "details": {
                "result": "success",
                "mapping": mapping_details or {"source": "rates.JPY", "target": "rate"},
            },
        },
    )


def log_rate_fetch_failure(
    logger: Logger,
    execution_id: str,
    error_reason: str,
    provider: str = "open_exchange_rates",
    error_details: Optional[Dict[str, Any]] = None,
) -> None:
    """Log exchange rate fetch failure.

    Args:
        logger: Logger instance
        execution_id: Unique execution ID
        error_reason: Reason for failure
        error_details: Additional error details
    """
    logger.error(
        "Exchange rate fetch failed",
        extra={
            "execution_id": execution_id,
            "reason": error_reason,
            "timestamp": _now_iso(),
            "provider": provider,
            "event_type": "rate_fetch",
            "details": error_details or {},
        },
    )


def log_line_push_success(
    logger: Logger,
    execution_id: str,
    message_text: str,
    timestamp: str,
) -> None:
    """Log successful LINE message push.

    Args:
        logger: Logger instance
        execution_id: Unique execution ID
        message_text: Message sent
        timestamp: Send timestamp
    """
    logger.info(
        "LINE message pushed successfully",
        extra={
            "execution_id": execution_id,
            "message_preview": message_text[:50],  # First 50 chars
            "timestamp": timestamp,
            "event_type": "line_push",
            "details": {"result": "success"},
        },
    )


def log_line_push_failure(
    logger: Logger,
    execution_id: str,
    error_reason: str,
    error_details: Optional[Dict[str, Any]] = None,
) -> None:
    """Log LINE message push failure.

    Args:
        logger: Logger instance
        execution_id: Unique execution ID
        error_reason: Reason for failure
        error_details: Additional error details
    """
    logger.error(
        "LINE message push failed",
        extra={
            "execution_id": execution_id,
            "reason": error_reason,
            "timestamp": _now_iso(),
            "event_type": "line_push",
            "details": error_details or {},
        },
    )


def log_validation_error(
    logger: Logger,
    execution_id: str,
    error_reason: str,
    error_details: Optional[Dict[str, Any]] = None,
) -> None:
    """Log validation error.

    Args:
        logger: Logger instance
        execution_id: Unique execution ID
        error_reason: Reason for validation failure
        error_details: Additional error details
    """
    logger.error(
        "Validation error",
        extra={
            "execution_id": execution_id,
            "reason": error_reason,
            "timestamp": _now_iso(),
            "event_type": "validation_error",
            "details": error_details or {},
        },
    )


def log_config_error(
    logger: Logger,
    execution_id: str,
    error_reason: str,
    error_details: Optional[Dict[str, Any]] = None,
) -> None:
    """Log configuration error.

    Args:
        logger: Logger instance
        execution_id: Unique execution ID
        error_reason: Reason for configuration failure
        error_details: Additional error details
    """
    logger.error(
        "Configuration error",
        extra={
            "execution_id": execution_id,
            "reason": error_reason,
            "timestamp": _now_iso(),
            "event_type": "config_error",
            "details": error_details or {},
        },
    )
