"""Pathlib compatibility helpers for Python versions before 3.12."""

from __future__ import annotations

import sys
from pathlib import Path


def is_regular_file(path: Path) -> bool:
    """Return True when path exists and is a regular file, not a symlink."""
    if sys.version_info >= (3, 12):
        return path.is_file(follow_symlinks=False)
    return path.is_file() and not path.is_symlink()
