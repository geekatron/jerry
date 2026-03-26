# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""HealthStatus value object — result of a proxy node health check.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HealthStatus:
    """Immutable result of a proxy node health check.

    Attributes:
        node_id: Provider-assigned node identifier.
        reachable: True if the node responded to ICMP/TCP probe.
        socks_port_open: True if the SOCKS5 port is accepting connections.
        ssh_accessible: True if the SSH daemon is accepting connections.
        checked_at: UTC timestamp of the health check.
        error_message: Description of the failure, or None if healthy.
    """

    node_id: str
    reachable: bool
    socks_port_open: bool
    ssh_accessible: bool
    checked_at: datetime
    error_message: str | None = None

    @property
    def is_healthy(self) -> bool:
        """Return True when all health indicators pass.

        Returns:
            True when reachable, socks_port_open, and ssh_accessible are all True.
        """
        return self.reachable and self.socks_port_open and self.ssh_accessible
