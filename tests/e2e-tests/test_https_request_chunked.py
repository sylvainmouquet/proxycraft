from proxycraft import ProxyCraft
import pytest
from proxycraft.features.configuration.models import Config
import httpx
import logging


@pytest.mark.asyncio
async def test_https_request_chunked(proxycraft_app_lifespan):
    config = {
        "version": "1.0",
        "name": "ProxyCraft",
        "server": {"type": "uvicorn"},
        "endpoints": [
            {
                "prefix": "/",
                "match": "**/*",
                "backends": [
                    {
                        "https": {
                            "id": "primary",
                            "url": "https://httpbun.com",
                            "ssl": True,
                            "mode": "stream",
                        }
                    }
                ],
                "upstream": {
                    "proxy": {
                        "enabled": True,
                    }
                },
            }
        ],
    }

    proxycraft: ProxyCraft = ProxyCraft(config=Config(**config))

    async with proxycraft_app_lifespan(proxycraft.app) as app:
        transport = httpx.ASGITransport(app=app)
        timeout = httpx.Timeout(300.0)  # 5 minutes

        async with httpx.AsyncClient(
            transport=transport, base_url="http://testserver", timeout=timeout
        ) as client:
            async with client.stream(
                "GET",
                "/drip-lines",
                headers={"Accept": "application/text-stream"},
            ) as response:
                logging.info(f"Status code {response.status_code}")
                chunked = ""
                async for chunk in response.aiter_lines():
                    chunked += chunk
                    logging.info(f"Lined {chunk}")

        assert chunked == "**********"
