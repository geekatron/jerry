"""Pytest configuration for Jerry Framework tests."""
from __future__ import annotations

import sys
from pathlib import Path

# Add src to Python path for imports - this runs at module load time,
# before pytest_configure, which should help with early imports
_src_path = str(Path(__file__).parent.parent / "src")
if _src_path not in sys.path:
    sys.path.insert(0, _src_path)


def pytest_configure(config):
    """Ensure src is in Python path before test collection."""
    src_path = str(Path(__file__).parent.parent / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
