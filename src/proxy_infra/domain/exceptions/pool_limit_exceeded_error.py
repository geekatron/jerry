# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""PoolLimitExceededError domain exception for proxy infrastructure."""

from __future__ import annotations


class PoolLimitExceededError(Exception):
    """Raised when a provision request would exceed max_nodes for the engagement (PI-001)."""
