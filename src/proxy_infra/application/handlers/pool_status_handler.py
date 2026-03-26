# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""PoolStatusHandler — application handler for PoolStatusQuery.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.application.queries.pool_status_query import PoolStatusQuery
    from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode


class PoolStatusHandler:
    """Handles PoolStatusQuery to return a flat list of nodes.

    Returns a list of ProxyNode instances rather than ProxyPool wrappers to
    keep the query result flat and JSON-serialisable at the CLI layer.
    ProxyPool construction (if needed for manifest operations) is deferred to
    the caller.

    The handler does NOT import infrastructure adapters — it operates only
    through the ProxyProvisionerPort interface (H-07 application-layer rule).

    References:
        - ADR-PROJ023-008: Application handler pattern
    """

    def __init__(self, provisioner: ProxyProvisionerPort) -> None:
        """Initialize PoolStatusHandler with the provisioner port.

        Args:
            provisioner: ProxyProvisionerPort implementation to query.
        """
        self._provisioner = provisioner

    def handle(self, query: PoolStatusQuery) -> list[ProxyNode]:
        """Execute a pool status query.

        Calls ``self._provisioner.list_instances(engagement_id)`` to fetch
        the current node list for the queried engagement.

        Args:
            query: The pool status query with optional engagement_id filter
                and verbosity flag.  An empty engagement_id returns all nodes
                visible to the provisioner.

        Returns:
            List of ProxyNode instances matching the query filter.
        """
        return self._provisioner.list_instances(query.engagement_id)
