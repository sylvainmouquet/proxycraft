import pytest

from pyprox import PyProx


@pytest.mark.asyncio
async def test_pyprox_load_file_config():
    pyprox = PyProx(config_file="pyprox/default.json")
    assert pyprox.config.name == "PyProx"
