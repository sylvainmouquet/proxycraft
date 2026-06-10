# Demonstration
import logging

import pytest

from proxycraft.networking.connection_pooling.http_client import HTTPClient
from proxycraft.networking.connection_pooling.tracing.default_trace_handler import (
    TraceHandlers,
)

# Setup logging to see trace output
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

trace_config = TraceHandlers(
    enable_logging=True,
    logger_name="test_http_client",
    log_level=logging.INFO,
)


@pytest.mark.asyncio
async def test_http_client_one_client():
    async with HTTPClient(trace_handlers=trace_config) as client:
        async with client.session.get("https://httpbin.org/get") as resp:
            print(f"{resp.status}")

        async with client.session.get("https://httpbin.org/get") as resp:
            print(f"{resp.status}")


@pytest.mark.asyncio
async def test_http_client_closes_dedicated_connector():
    async with HTTPClient(connector_strategy="dedicated") as client:
        connector = client.tcp_connector
        assert connector is not None
        assert not connector.closed

    assert connector.closed


@pytest.mark.asyncio
async def test_http_client_two_clients():
    async with HTTPClient(trace_handlers=trace_config) as client:
        async with client.session.get("https://httpbin.org/get") as resp:
            print(f"{resp.status}")

    async with HTTPClient(trace_handlers=trace_config) as client2:
        async with client2.session.get("https://httpbin.org/get") as resp:
            print(f"{resp.status}")
