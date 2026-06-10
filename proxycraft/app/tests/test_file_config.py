import pytest

from proxycraft.app.proxycraft import ProxyCraft


@pytest.mark.asyncio
async def test_load_config():
    proxycraft = ProxyCraft(
        config_file="proxycraft/features/configuration/default.json"
    )
    assert proxycraft.config.name == "ProxyCraft"
