import pytest

from proxycraft.proxycraft import ProxyCraft


@pytest.mark.asyncio
async def test_load_config():
    proxycraft = ProxyCraft(config_file="proxycraft/default.json")
    assert proxycraft.config.name == "ProxyCraft"
