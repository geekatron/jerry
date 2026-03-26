# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""PoolCapacityExceededError domain exception for proxy infrastructure."""

from __future__ import annotations


class PoolCapacityExceededError(Exception):
    """Raised when a provision request would exceed max_nodes for the engagement (PI-001).

    Alias for the canonical PoolLimitExceededError; exposed under the test-contract
    name so that consumer code importing either name receives the same semantics.
    """
