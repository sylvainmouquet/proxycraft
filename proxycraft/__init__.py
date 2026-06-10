__version__ = "0.0.1"
__all__ = (
    "__version__",
    "ProxyCraft",
)

from proxycraft.logger import get_logger
from proxycraft.proxycraft import ProxyCraft

logger = get_logger("proxycraft")
