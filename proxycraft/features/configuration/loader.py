import json
from threading import Lock

from proxycraft.features.configuration.models import Config
from proxycraft.shared.infrastructure.logging import get_logger

config_lock = Lock()
logger = get_logger(__name__)


def get_file_config(filepath: str) -> Config | None:
    with config_lock:
        try:
            with open(filepath) as f:
                json_loaded = json.load(f)
                config = Config(**json_loaded)
                config.endpoints.sort(key=lambda e: e.weight, reverse=True)
                logger.info(
                    "Configuration loaded",
                    filepath=filepath,
                    endpoint_count=len(config.endpoints),
                )
                return config
        except FileNotFoundError:
            logger.error("Configuration file not found", filepath=filepath)
            return None
