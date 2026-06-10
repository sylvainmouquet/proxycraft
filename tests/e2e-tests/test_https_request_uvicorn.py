from proxycraft import ProxyCraft
import pytest
from proxycraft.features.configuration.models import Config
import httpx
from http import HTTPStatus


@pytest.mark.asyncio
async def test_https_request(proxycraft_app_lifespan, posts_upstream_url):
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
                            "url": posts_upstream_url,
                            "ssl": False,
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
        async with httpx.AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            response = await client.get("/1")
            assert response.status_code == HTTPStatus.OK
            assert response.json()["id"] == 1

            response = await client.get("/20")
            assert response.status_code == HTTPStatus.OK
            assert response.json()["id"] == 20
