# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProvisionConfig value object — parameters for proxy node provisioning.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.firewall_rule import FirewallRule
    from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
    from src.proxy_infra.domain.value_objects.proxy_type import ProxyType


@dataclass(frozen=True)
class ProvisionConfig:
    """Immutable provisioning parameters for one or more proxy nodes.

    Attributes:
        provider: Cloud provider name (e.g., "digitalocean").
        engagement_id: Owning engagement (PI-002 enforcement point).
        count: Number of nodes to provision.
        regions: List of provider region identifiers to distribute nodes across.
        role: Operational role to assign to provisioned nodes.
        proxy_type: Transport mechanism for provisioned nodes.
        image: Provider OS image identifier (e.g., "ubuntu-24-04-x64").
        size: Provider instance size identifier (e.g., "s-1vcpu-1gb").
        socks_port: SOCKS5 listening port.
        firewall_rules: Firewall rules to apply to provisioned nodes.
        ssh_public_key: OpenSSH public key to upload and authorize.
    """

    provider: str
    engagement_id: str
    count: int
    regions: tuple[str, ...]
    role: ProxyRole
    proxy_type: ProxyType
    image: str = "ubuntu-24-04-x64"
    size: str = "s-1vcpu-1gb"
    socks_port: int = 1080
    firewall_rules: tuple[FirewallRule, ...] = field(default_factory=tuple)
    ssh_public_key: str = ""
