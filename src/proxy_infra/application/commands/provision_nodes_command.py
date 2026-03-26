# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProvisionNodesCommand — application-layer command for proxy node provisioning.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
    from src.proxy_infra.domain.value_objects.proxy_type import ProxyType


@dataclass(frozen=True)
class ProvisionNodesCommand:
    """Command to provision one or more proxy nodes for an engagement.

    Attributes:
        engagement_id: Owning engagement identifier (PI-002).
        provider: Cloud provider name (e.g., "digitalocean").
        count: Number of nodes to provision (default 1).
        regions: Provider region identifiers to distribute nodes across.
        role: Operational role for provisioned nodes.
        proxy_type: Transport mechanism for provisioned nodes.
    """

    engagement_id: str
    provider: str
    count: int = 1
    regions: tuple[str, ...] = field(default_factory=tuple)
    role: ProxyRole | None = None
    proxy_type: ProxyType | None = None
