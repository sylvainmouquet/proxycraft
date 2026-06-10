from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
import logging


class RetryException(Exception): ...


# config
MAX_ATTEMPTS = 5
MIN_TIME = 0.1  # in seconds
MAX_TIME = 0.2  # in seconds

SHOW_EXCEPTIONS = True

pytest_plugins = ["pytester"]

# For console output
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)


@pytest.fixture
def disable_logging_exception(mocker):
    if not SHOW_EXCEPTIONS:
        mocker.patch("logging.exception", lambda *args, **kwargs: None)


@pytest_asyncio.fixture(autouse=True)
async def cleanup_http_connectors():
    yield
    from proxycraft.networking.connection_pooling.http_client import (
        cleanup_all_connectors,
    )

    await cleanup_all_connectors()


@pytest.fixture
def proxycraft_app_lifespan():
    """Run Starlette lifespan around ASGI transport tests (httpx skips it by default)."""

    @asynccontextmanager
    async def _run(app):
        async with app.router.lifespan_context(app):
            yield app

    return _run
