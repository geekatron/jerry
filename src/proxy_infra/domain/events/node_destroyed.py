# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""NodeDestroyed domain event.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class NodeDestroyed:
    """Domain event raised when a proxy node is successfully destroyed.

    Attributes:
        node_id: Provider-assigned identifier of the destroyed node.
        engagement_id: Owning engagement.
        reason: Human-readable reason for destruction.
        occurred_at: UTC timestamp of the event.
    """

    node_id: str
    engagement_id: str
    reason: str
    occurred_at: datetime
