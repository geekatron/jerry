# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau
"""Property test configuration — conditionally skip when hypothesis is not installed."""

try:
    import hypothesis  # noqa: F401
except ImportError:
    collect_ignore_glob = ["test_*.py"]
