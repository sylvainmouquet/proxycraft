import pytest

from proxycraft.shared.infrastructure.logging import get_logger

logger = get_logger(__name__)


@pytest.mark.asyncio
async def test_logger():
    logger.debug("debug message")
    logger.info("info message")
    logger.error("error message")
    logger.exception(Exception("exception message"))
