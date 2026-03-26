# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProxyNode value object — immutable representation of a provisioned proxy node.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.node_status import NodeStatus
    from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
    from src.proxy_infra.domain.value_objects.proxy_type import ProxyType


@dataclass(frozen=True)
class ProxyNode:
    """Immutable representation of a provisioned proxy node.

    Attributes:
        id: Provider-assigned unique identifier.
        provider: Cloud provider name (e.g., "digitalocean").
        ip: Public IPv4 address.
        region: Provider-specific region identifier.
        role: Operational role within the engagement.
        proxy_type: Transport mechanism.
        status: Current lifecycle state.
        ssh_key_id: Provider-side SSH key identifier.
        socks_port: SOCKS5 listening port (default 1080).
        created_at: UTC timestamp of provisioning.
        engagement_id: Scoped to a specific engagement.
        fingerprint: SSH host key fingerprint for verification.
    """

    id: str
    provider: str
    ip: str
    region: str
    role: ProxyRole
    proxy_type: ProxyType
    status: NodeStatus
    ssh_key_id: str
    created_at: datetime
    engagement_id: str
    socks_port: int = 1080
    fingerprint: str | None = None
