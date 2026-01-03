import pytest

from pyprox.pyprox import PyProx


@pytest.mark.asyncio
async def test_load_config():
    pyprox = PyProx(config_file="pyprox/default.json")
    assert pyprox.config.name == "PyProx"
