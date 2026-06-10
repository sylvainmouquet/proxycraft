import asyncio
from contextlib import asynccontextmanager
import time
import uuid

import aiohttp
from aiohttp import ClientTimeout

from proxycraft.shared.infrastructure.logging import get_logger

logger = get_logger(__name__)


class ConnectionPoolingSession:
    def __init__(self, timeout: float):
        self._session = None
        self._session_lock = asyncio.Lock()
        self.connection_reuse_count = 0
        self.connection_create_count = 0
        self.request_count = 0
        self._connection_map = {}
        self.timeout = timeout
        self.tcp_connector = None

    async def _on_request_start(self, session, context, params):
        request_id = str(uuid.uuid4())[:8]
        context.request_id = request_id
        context.start_time = time.perf_counter()
        self.request_count += 1
        logger.info(
            "HTTP request started",
            request_id=request_id,
            method=params.method,
            url=str(params.url),
        )

    async def _on_request_end(self, session, context, params):
        duration_ms = round((time.perf_counter() - context.start_time) * 1000)
        logger.info(
            "HTTP request completed",
            request_id=context.request_id,
            duration_ms=duration_ms,
            request_count=self.request_count,
            connections_created=self.connection_create_count,
            connections_reused=self.connection_reuse_count,
        )

    async def _on_connection_create_start(self, session, context, params):
        request_id = getattr(context, "request_id", "unknown")
        logger.debug(
            "Creating new connection",
            request_id=request_id,
        )

    async def _on_connection_create_end(self, session, context, params):
        self.connection_create_count += 1
        conn_key = "a"  # id(params.transport)
        request_id = getattr(context, "request_id", "unknown")
        self._connection_map[conn_key] = {
            "created_at": time.perf_counter(),
            "request_id": request_id,
            "use_count": 1,
        }
        logger.debug(
            "New connection created",
            connection_key=conn_key,
            request_id=request_id,
        )

    async def _on_connection_reuse(self, session, context, params):
        self.connection_reuse_count += 1
        conn_key = "a"  # id(params.transport)
        request_id = getattr(context, "request_id", "unknown")
        if conn_key in self._connection_map:
            self._connection_map[conn_key]["use_count"] += 1
            age_s = time.perf_counter() - self._connection_map[conn_key]["created_at"]
            use_count = self._connection_map[conn_key]["use_count"]
            logger.debug(
                "Connection reused",
                connection_key=conn_key,
                request_id=request_id,
                use_count=use_count,
                age_s=round(age_s, 1),
                timeout_s=self.timeout,
            )
        else:
            logger.debug(
                "Reusing untracked connection",
                connection_key=conn_key,
            )

    @asynccontextmanager
    async def get_session(self):
        """Get the shared client session, creating it if needed."""
        if self._session is None:
            async with self._session_lock:
                if self._session is None:
                    self.tcp_connector = aiohttp.TCPConnector(
                        ssl=True, keepalive_timeout=75, limit=10
                    )
                    trace_config = aiohttp.TraceConfig()
                    trace_config.on_request_start.append(self._on_request_start)
                    trace_config.on_request_end.append(self._on_request_end)
                    trace_config.on_connection_create_start.append(
                        self._on_connection_create_start
                    )
                    trace_config.on_connection_create_end.append(
                        self._on_connection_create_end
                    )
                    trace_config.on_connection_reuseconn.append(
                        self._on_connection_reuse
                    )

                    timeout = ClientTimeout(
                        total=60,
                        connect=10,
                        sock_read=15,
                        sock_connect=10,
                    )

                    self._session = aiohttp.ClientSession(
                        connector=self.tcp_connector,
                        trace_configs=[trace_config],
                        timeout=timeout,
                    )

        try:
            yield self._session
        except Exception:
            logger.exception("HTTP session error")
            raise

    async def close(self):
        """Close the session when shutting down."""
        if self._session is not None:
            await self._session.close()
            self._session = None
        if self.tcp_connector is not None:
            await self.tcp_connector.close()
            self.tcp_connector = None


class ConnectionPooling:
    def __init__(self):
        self.connection_pool_sessions: dict[str, ConnectionPoolingSession] = {}

    def append_new_client_session(self, key, timeout):
        self.connection_pool_sessions[key] = ConnectionPoolingSession(timeout)

    async def close(self):
        for key in self.connection_pool_sessions:
            await self.connection_pool_sessions[key].close()
