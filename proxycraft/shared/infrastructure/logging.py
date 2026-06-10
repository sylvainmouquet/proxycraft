import logging
import sys

import structlog
from structlog.typing import FilteringBoundLogger


def setup_structlog(
    log_level: str = "INFO",
    json_logs: bool = True,
    include_timestamp: bool = True,
) -> None:
    """
    Configure structlog for structured logging.

    Call once at application startup. Module loggers are created with
    ``get_logger(__name__)`` and accept structured fields as keyword arguments.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_logs: Whether to output logs in JSON format
        include_timestamp: Whether to include timestamps in logs
    """

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )

    processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.CallsiteParameterAdder(
            parameters=[
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
            ]
        ),
    ]

    if include_timestamp:
        processors.append(structlog.processors.TimeStamper(fmt="ISO", utc=True))

    if json_logs:
        processors.extend(
            [structlog.processors.dict_tracebacks, structlog.processors.JSONRenderer()]
        )
    else:
        processors.extend([structlog.dev.ConsoleRenderer(colors=True)])

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        context_class=dict,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> FilteringBoundLogger:
    """
    Return a structured logger for the calling module.

    Usage::

        from proxycraft.shared.infrastructure.logging import get_logger

        logger = get_logger(__name__)

    Pass context as keyword arguments (equivalent to ``extra={}``)::

        logger.info(
            "API request completed",
            method="GET",
            endpoint="/documents",
            status_code=200,
            duration_ms=152,
        )
    """
    return structlog.get_logger(name)
