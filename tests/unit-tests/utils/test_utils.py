from proxycraft import ProxyCraft
from proxycraft.config.models import Config
from proxycraft.utils.utils import check_path
import pytest
import json


@pytest.mark.asyncio
async def test_check_path():
    # Check if the full config path exists
    config = """
    {
  "version": "1.0",
  "name": "Check Path",
  "middlewares": {
    "security": {
      "ip_filter": {
        "enabled": true,
        "blacklist": [
          "*.0.0.2"
        ]
      }
    }
   },
  "endpoints": [
    {
      "prefix": "/",
      "match": "**/*",
      "backends": {
        "https": {
          "url": "https://jsonplaceholder.typicode.com/posts"
        }
      },
      "upstream": {
        "proxy": {
          "enabled": true
        }
      }
    }
  ]
}
"""

    proxycraft: ProxyCraft = ProxyCraft(config=Config(**json.loads(config)))
    if check_path(proxycraft.config, "middlewares.security.ip_filter.enabled"):
        enabled = proxycraft.config.middlewares.security.ip_filter.enabled
        print(f"Cache enabled: {enabled}")

    # Multiple checks
    config_paths_exists = [
        "middlewares.security.ip_filter.enabled",
        "middlewares.security.ip_filter",
        "middlewares.security",
        "middlewares",
    ]

    config_paths_not_exists = [
        "middlewares.security.ip_filter.none",
        "middlewares.security.none",
        "middlewares.none",
        "none",
    ]

    for path in config_paths_exists:
        exists = check_path(proxycraft.config, path)
        assert exists is True, path

    for path in config_paths_not_exists:
        exists = check_path(proxycraft.config, path)
        assert exists is False, path
