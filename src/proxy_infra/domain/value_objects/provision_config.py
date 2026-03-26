# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProvisionConfig value object — parameters for proxy node provisioning.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.firewall_rule import FirewallRule
    from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
    from src.proxy_infra.domain.value_objects.proxy_type import ProxyType

#: Maximum number of proxy nodes per engagement (RATELIMIT-006).
_MAX_NODES_PER_ENGAGEMENT: int = 10


@dataclass(frozen=True)
class ProvisionConfig:
    """Immutable provisioning parameters for one or more proxy nodes.

    Attributes:
        provider: Cloud provider name (e.g., "digitalocean").
        region: Provider region identifier (e.g., "nyc1").
        engagement_id: Owning engagement (PI-002 enforcement point).
        engagement_tag: Tag applied to all resources for orphan detection (ISOLATION-001).
        count: Number of nodes to provision (max 10 per RATELIMIT-006).
        role: Operational role to assign to provisioned nodes.
        proxy_type: Transport mechanism for provisioned nodes.
        ssh_public_key: OpenSSH public key to upload and authorize.
        operator_ip: Operator egress IP for firewall allowlisting.
        image: Provider OS image identifier (e.g., "ubuntu-24-04-x64").
        size: Provider instance size identifier (e.g., "s-1vcpu-1gb").
        socks_port: SOCKS5 listening port.
        provisioning_delay_seconds: Seconds to wait between provision() calls (RATELIMIT-001).
    """

    provider: str
    region: str
    engagement_id: str
    engagement_tag: str
    count: int
    role: ProxyRole
    proxy_type: ProxyType
    ssh_public_key: str
    operator_ip: str
    image: str = "ubuntu-24-04-x64"
    size: str = "s-1vcpu-1gb"
    socks_port: int = 1080
    provisioning_delay_seconds: int = 15

    def __post_init__(self) -> None:
        """Enforce domain invariants on construction.

        Raises:
            ValueError: If engagement_tag is empty (ISOLATION-001) or count exceeds
                the maximum allowed per engagement (RATELIMIT-006).
        """
        if not self.engagement_tag:
            raise ValueError(
                "engagement_tag must not be empty — ISOLATION-001: engagement tag "
                "is required for resource isolation and orphan detection (ORPHAN-003)"
            )
        if self.count > _MAX_NODES_PER_ENGAGEMENT:
            raise ValueError(
                f"count={self.count} exceeds maximum of {_MAX_NODES_PER_ENGAGEMENT} "
                f"nodes per engagement — RATELIMIT-006"
            )
