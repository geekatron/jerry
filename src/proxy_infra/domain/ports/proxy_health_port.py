# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Port interface for proxy node health monitoring.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.health_status import HealthStatus
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode


class ProxyHealthPort(ABC):
    """Port interface for proxy node health monitoring and burned-node detection.

    Separates health checking concerns from provisioning concerns.
    Implementations may use network probes, provider API status endpoints,
    or external blacklist lookups depending on the detection strategy.

    References:
        - ADR-PROJ023-008: Health monitoring service design
    """

    @abstractmethod
    def check_node(self, node: ProxyNode) -> HealthStatus:
        """Perform a health check on a single proxy node.

        Verifies ICMP reachability, SOCKS5 port availability, and SSH
        daemon responsiveness.

        Args:
            node: The proxy node to check.

        Returns:
            HealthStatus with full probe results and timestamp.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    @abstractmethod
    def is_burned(self, node: ProxyNode) -> bool:
        """Determine whether a proxy node has been detected or blacklisted.

        Checks against known-bad IP databases and detection indicators
        to identify nodes that should be rotated out of the pool.

        Args:
            node: The proxy node to evaluate.

        Returns:
            True if the node shows signs of detection or blacklisting.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
