import pytest

from proxycraft import ProxyCraft


@pytest.mark.asyncio
async def test_proxycraft_load_file_config():
    proxycraft = ProxyCraft(config_file="proxycraft/default.json")
    assert proxycraft.config.name == "ProxyCraft"
