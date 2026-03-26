# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""PoolStatusQuery — application-layer query for proxy pool status.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PoolStatusQuery:
    """Query to retrieve the current status of a proxy pool.

    Attributes:
        engagement_id: Filter results to a specific engagement, or empty
            string to retrieve all pools.
        verbose: If True, include SSH details (fingerprints, key IDs) in output.
    """

    engagement_id: str = ""
    verbose: bool = False
