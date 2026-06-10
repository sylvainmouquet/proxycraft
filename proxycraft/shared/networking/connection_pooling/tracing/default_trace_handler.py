import uuid
import time
from typing import Dict, Optional, Callable
from dataclasses import dataclass

from proxycraft.shared.infrastructure.logging import get_logger

logger = get_logger(__name__)


@dataclass
class TraceHandlers:
    """Configuration for HTTP request tracing"""

    enable_logging: bool = True

    log_level: str = "INFO"
    logger_name: str = "proxycraft"
    # Custom trace callbacks
    on_request_start: Optional[Callable] = None
    on_request_end: Optional[Callable] = None
    on_request_exception: Optional[Callable] = None
    on_connection_create_start: Optional[Callable] = None
    on_connection_create_end: Optional[Callable] = None
    on_connection_reuseconn: Optional[Callable] = None
    on_dns_resolvehost_start: Optional[Callable] = None
    on_dns_resolvehost_end: Optional[Callable] = None


class DefaultTraceHandlers:
    """Default trace handlers for HTTP requests"""

    def __init__(self, config: TraceHandlers):
        self.config = config
        self._request_times: Dict = {}
        self._connection_times: Dict = {}
        self.connection_reuse_count = 0
        self.connection_create_count = 0
        self.request_count = 0

    async def on_request_start(self, session, trace_config_ctx, params):
        """Called when request starts"""
        request_id = str(uuid.uuid4())[:8]
        trace_config_ctx.request_id = request_id
        self._request_times[trace_config_ctx.request_id] = time.perf_counter()

        if self.config.enable_logging:
            logger.info(
                "HTTP request started",
                request_id=request_id,
                method=params.method,
                url=str(params.url),
            )

        if self.config.on_request_start:
            await self.config.on_request_start(session, trace_config_ctx, params)

    async def on_request_end(self, session, trace_config_ctx, params):
        """Called when request ends"""
        ctx_id = trace_config_ctx.request_id
        start_time = self._request_times.pop(ctx_id, None)
        duration_ms = (
            round((time.perf_counter() - start_time) * 1000) if start_time else 0
        )
        self.request_count += 1

        if self.config.enable_logging:
            logger.info(
                "HTTP request completed",
                request_id=ctx_id,
                method=params.method,
                url=str(params.url),
                status_code=params.response.status,
                duration_ms=duration_ms,
                request_count=self.request_count,
                connections_created=self.connection_create_count,
                connections_reused=self.connection_reuse_count,
            )

        if self.config.on_request_end:
            await self.config.on_request_end(session, trace_config_ctx, params)

    async def on_request_exception(self, session, trace_config_ctx, params):
        """Called when request raises an exception"""
        ctx_id = trace_config_ctx.request_id
        start_time = self._request_times.pop(ctx_id, None)
        duration_ms = (
            round((time.perf_counter() - start_time) * 1000) if start_time else 0
        )

        if self.config.enable_logging:
            logger.error(
                "HTTP request failed",
                request_id=ctx_id,
                method=params.method,
                url=str(params.url),
                duration_ms=duration_ms,
                error=str(params.exception),
            )

        if self.config.on_request_exception:
            await self.config.on_request_exception(session, trace_config_ctx, params)

    async def on_connection_create_start(self, session, trace_config_ctx, params):
        """Called when connection creation starts"""
        ctx_id = trace_config_ctx.request_id
        self._connection_times[ctx_id] = time.perf_counter()
        self.connection_create_count += 1

        if self.config.enable_logging:
            logger.debug(
                "Creating new connection",
                request_id=getattr(trace_config_ctx, "request_id", "unknown"),
            )

        if self.config.on_connection_create_start:
            await self.config.on_connection_create_start(
                session, trace_config_ctx, params
            )

    async def on_connection_create_end(self, session, trace_config_ctx, params):
        """Called when connection creation ends"""
        ctx_id = trace_config_ctx.request_id
        start_time = self._connection_times.pop(ctx_id, None)
        duration_ms = (
            round((time.perf_counter() - start_time) * 1000) if start_time else 0
        )

        if self.config.enable_logging:
            logger.debug(
                "Connection created",
                request_id=getattr(trace_config_ctx, "request_id", "unknown"),
                duration_ms=duration_ms,
            )

        if self.config.on_connection_create_end:
            await self.config.on_connection_create_end(
                session, trace_config_ctx, params
            )

    async def on_connection_reuseconn(self, session, trace_config_ctx, params):
        """Called when connection is reused"""
        self.connection_reuse_count += 1

        if self.config.enable_logging:
            logger.debug(
                "Connection reused",
                request_id=getattr(trace_config_ctx, "request_id", "unknown"),
            )

        if self.config.on_connection_reuseconn:
            await self.config.on_connection_reuseconn(session, trace_config_ctx, params)

    async def on_dns_resolvehost_start(self, session, trace_config_ctx, params):
        """Called when DNS resolution starts"""
        if self.config.enable_logging:
            logger.debug("DNS resolution started", host=params.host)

        if self.config.on_dns_resolvehost_start:
            await self.config.on_dns_resolvehost_start(
                session, trace_config_ctx, params
            )

    async def on_dns_resolvehost_end(self, session, trace_config_ctx, params):
        """Called when DNS resolution ends"""
        if self.config.enable_logging:
            logger.debug("DNS resolution completed", host=params.host)

        if self.config.on_dns_resolvehost_end:
            await self.config.on_dns_resolvehost_end(session, trace_config_ctx, params)
