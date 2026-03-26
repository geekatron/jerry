# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""DestroyNodesCommand — application-layer command for proxy node destruction.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DestroyNodesCommand:
    """Command to destroy proxy nodes for an engagement.

    Attributes:
        engagement_id: Owning engagement identifier (PI-002).
        node_ids: Specific node IDs to destroy, or empty tuple to destroy all
            nodes for the engagement.
        force: Skip confirmation prompt when True.
    """

    engagement_id: str
    node_ids: tuple[str, ...] = field(default_factory=tuple)
    force: bool = False
