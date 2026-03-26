# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProxyPool value object — immutable snapshot of the current proxy pool state.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode


@dataclass(frozen=True)
class ProxyPool:
    """Immutable snapshot of the current proxy pool state.

    Attributes:
        nodes: All nodes in the pool.
        lb_strategy: Load balancing strategy ("random", "round_robin", "phase_sticky").
        fail_mode: Behavior on all-nodes-down ("closed" = fail-safe, "open" = fail-through).
        max_nodes: Per-engagement maximum (enforced by PI-001).
        engagement_id: Owning engagement.
    """

    nodes: tuple[ProxyNode, ...]
    lb_strategy: str = "round_robin"
    fail_mode: str = "closed"
    max_nodes: int = 10
    engagement_id: str = ""
