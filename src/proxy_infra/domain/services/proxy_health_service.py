# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProxyHealthService — domain service for health monitoring and burned-node detection.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.ports.proxy_health_port import ProxyHealthPort
    from src.proxy_infra.domain.value_objects.health_status import HealthStatus
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
    from src.proxy_infra.domain.value_objects.proxy_pool import ProxyPool


class ProxyHealthService:
    """Domain service for proxy node health monitoring and burned-node detection.

    Periodically checks node reachability, SOCKS5 port availability, and
    SSH daemon responsiveness. Detects burned (detected/blacklisted) nodes
    and triggers rotation via ProxyPoolService.

    References:
        - ADR-PROJ023-008: Health monitoring configuration
    """

    def __init__(self, health_port: ProxyHealthPort) -> None:
        """Initialize ProxyHealthService with a health monitoring port.

        Args:
            health_port: Health monitoring port implementation.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def check_pool(self, pool: ProxyPool) -> list[HealthStatus]:
        """Run health checks on all nodes in the pool.

        Args:
            pool: The proxy pool whose nodes should be checked.

        Returns:
            List of HealthStatus results, one per node.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def check_node(self, node: ProxyNode) -> HealthStatus:
        """Run a health check on a single proxy node.

        Args:
            node: The proxy node to check.

        Returns:
            HealthStatus with probe results and timestamp.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def detect_burned_nodes(self, pool: ProxyPool) -> list[ProxyNode]:
        """Identify nodes that have been detected or blacklisted.

        Args:
            pool: The proxy pool to scan for burned nodes.

        Returns:
            List of ProxyNode instances that are burned and should be rotated.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
