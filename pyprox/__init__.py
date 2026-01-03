__version__ = "1.0.0"
__all__ = (
    "__version__",
    "PyProx",
)

import logging

from pyprox.pyprox import PyProx

logger = logging.getLogger("pyprox")
logger.addHandler(logging.NullHandler())
