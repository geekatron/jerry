# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""NodeRotated domain event.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode


@dataclass(frozen=True)
class NodeRotated:
    """Domain event raised when a proxy node is rotated out and replaced.

    Attributes:
        old_node_id: Provider-assigned ID of the destroyed node.
        new_node: The replacement proxy node.
        engagement_id: Owning engagement.
        reason: Human-readable rotation reason.
        occurred_at: UTC timestamp of the event.
    """

    old_node_id: str
    new_node: ProxyNode
    engagement_id: str
    reason: str
    occurred_at: datetime
