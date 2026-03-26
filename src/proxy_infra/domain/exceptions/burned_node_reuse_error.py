# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BurnedNodeReuseError domain exception for proxy infrastructure."""

from __future__ import annotations


class BurnedNodeReuseError(Exception):
    """Raised when an attempt is made to route traffic through a burned node (PI-003)."""
