"""HTTP stdlib compatibility for Python versions before 3.11."""

from __future__ import annotations

import sys
from enum import Enum

if sys.version_info >= (3, 11):
    from http import HTTPMethod
else:

    class HTTPMethod(str, Enum):
        CONNECT = "CONNECT"
        DELETE = "DELETE"
        GET = "GET"
        HEAD = "HEAD"
        OPTIONS = "OPTIONS"
        PATCH = "PATCH"
        POST = "POST"
        PUT = "PUT"
        TRACE = "TRACE"
