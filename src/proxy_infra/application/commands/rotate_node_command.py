# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""RotateNodeCommand — application-layer command for rotating a proxy node.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RotateNodeCommand:
    """Command to rotate a proxy node out of service and replace it.

    Provisions a replacement node before destroying the original (PI-003).

    Attributes:
        engagement_id: Owning engagement identifier (PI-002).
        node_id: Provider-assigned ID of the node to rotate out.
        reason: Human-readable rotation reason for the audit log.
    """

    engagement_id: str
    node_id: str
    reason: str = ""
