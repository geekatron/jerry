# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""NodeBurned domain event.

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
class NodeBurned:
    """Domain event raised when a proxy node is detected as burned (blocked/detected).

    Triggers the rotation workflow: a replacement node must be provisioned
    before the burned node is destroyed (PI-003).

    Attributes:
        node: The burned proxy node.
        engagement_id: Owning engagement.
        detection_source: Description of how the burn was detected.
        occurred_at: UTC timestamp of the event.
    """

    node: ProxyNode
    engagement_id: str
    detection_source: str
    occurred_at: datetime
