# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""HealthCheckQuery — application-layer query for proxy node health status.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthCheckQuery:
    """Query to run health checks on proxy nodes.

    Attributes:
        engagement_id: Filter health checks to a specific engagement, or
            empty string to check all active engagements.
    """

    engagement_id: str = ""
