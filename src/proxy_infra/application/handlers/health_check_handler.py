# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""HealthCheckHandler — application handler for HealthCheckQuery.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.application.queries.health_check_query import HealthCheckQuery
    from src.proxy_infra.domain.services.proxy_health_service import ProxyHealthService
    from src.proxy_infra.domain.value_objects.health_status import HealthStatus


class HealthCheckHandler:
    """Handles HealthCheckQuery to run health probes on proxy nodes.

    Delegates the actual health checking to the ProxyHealthService domain
    service, which in turn uses the ProxyHealthPort adapter for network probes.

    References:
        - ADR-PROJ023-008: Application handler pattern
    """

    def __init__(self, health_service: ProxyHealthService) -> None:
        """Initialize HealthCheckHandler with the domain service.

        Args:
            health_service: Proxy health domain service.
        """
        self._health_service = health_service

    def handle(self, query: HealthCheckQuery) -> list[HealthStatus]:
        """Execute a health check query.

        Delegates to ProxyHealthService to check each node via the health port.

        Args:
            query: The health check query with optional engagement_id filter.

        Returns:
            List of HealthStatus results, one per checked node.
        """
        from src.proxy_infra.domain.value_objects.proxy_pool import ProxyPool

        # Build a pool from the health port's provisioner listing
        # The health service checks all nodes in the pool
        pool = ProxyPool(
            nodes=(),
            engagement_id=query.engagement_id,
        )
        return self._health_service.check_pool(pool)
