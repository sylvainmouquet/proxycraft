__version__ = "0.0.1"
__all__ = (
    "__version__",
    "ProxyCraft",
)

from proxycraft.app.proxycraft import ProxyCraft
from proxycraft.shared.infrastructure.logging import get_logger

logger = get_logger("proxycraft")
