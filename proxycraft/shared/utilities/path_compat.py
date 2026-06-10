"""Pathlib compatibility helpers."""

from __future__ import annotations

import stat
from pathlib import Path


def is_regular_file(path: Path) -> bool:
    """Return True when path exists and is a regular file, not a symlink."""
    try:
        return stat.S_ISREG(path.stat(follow_symlinks=False).st_mode)
    except OSError:
        return False
