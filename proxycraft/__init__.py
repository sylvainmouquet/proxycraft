__version__ = "0.0.1"
__all__ = (
    "__version__",
    "ProxyCraft",
)

import logging

from proxycraft.proxycraft import ProxyCraft

logger = logging.getLogger("proxycraft")
logger.addHandler(logging.NullHandler())
