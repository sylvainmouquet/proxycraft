import asyncio
from contextvars import ContextVar

from aiohttp import TCPConnector


def get_context_connector() -> TCPConnector:
    """Get connector from async context"""
    connector = _connector_context.get()
    if connector is None:
        try:
            loop_id = id(asyncio.get_running_loop())
        except RuntimeError:
            loop_id = None

        if loop_id is not None:
            connector = _connectors_by_loop.get(loop_id)

        if connector is None or connector.closed:
            connector = TCPConnector(
                ssl=True,
                keepalive_timeout=75,
                limit=10,
                limit_per_host=5,
                # ssl_shutdown_timeout=SSL_SHUTDOWN_TIMEOUT
            )
            if loop_id is not None:
                _connectors_by_loop[loop_id] = connector

        _connector_context.set(connector)
    return connector


async def close_context_connector() -> None:
    """Close and reset the connector for the current async context."""
    connector = _connector_context.get()
    _connector_context.set(None)

    if connector is None:
        try:
            loop_id = id(asyncio.get_running_loop())
            connector = _connectors_by_loop.pop(loop_id, None)
        except RuntimeError:
            connector = None

    if connector is not None and not connector.closed:
        await connector.close()


async def close_all_context_connectors() -> None:
    """Close every loop-registered connector (used by test teardown)."""
    connectors = list(_connectors_by_loop.values())
    _connectors_by_loop.clear()
    _connector_context.set(None)

    for connector in connectors:
        if not connector.closed:
            await connector.close()


# ContextVar for async contexts (recommended for async apps)
_connector_context: ContextVar[TCPConnector | None] = ContextVar(
    "connector", default=None
)
_connectors_by_loop: dict[int, TCPConnector] = {}
