from pathlib import Path

import pytest

from proxycraft import ProxyCraft

DEFAULT_CONFIG_FILE = (
    Path(__file__).parent.parent.parent / "proxycraft/default.json"
).as_posix()


@pytest.mark.asyncio
async def test_routing_selector_valid():
    proxycraft = ProxyCraft(config_file=DEFAULT_CONFIG_FILE)

    paths = [
        "/github-api",
        "/github-api/",
        "/github-api/demo",
        "/github-api/demo/demo",
        "/github-api/demo/demo/demo",
        "/github-api/demo/demo/demo/demo",
    ]

    for path in paths:
        assert (
            proxycraft.routing_selector.find_endpoint(path).backends[0].https[0].url
            == "https://api.github.com"
        )


@pytest.mark.asyncio
async def test_routing_selector_invalid():
    proxycraft = ProxyCraft(config_file=DEFAULT_CONFIG_FILE)

    star_paths = ["", "/", "unknown"]

    for path in star_paths:
        assert (
            proxycraft.routing_selector.find_endpoint(path).backends[0].https
            is not None
        )
        assert (
            proxycraft.routing_selector.find_endpoint(path).backends[0].https.url
            == "https://sandbox.api.service.nhs.uk/hello-world/hello/world$"
        )
