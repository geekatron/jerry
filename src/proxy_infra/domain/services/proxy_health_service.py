# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProxyHealthService — domain service for health monitoring and rotation triggers.

Periodically checks node reachability, SOCKS5 port availability, and SSH daemon
responsiveness. Detects burned (detected/blacklisted) nodes and orchestrates
rotation via the caller-supplied ProxyProvisionerPort.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
    - TASK-023-038: Implement CLM Health Monitoring + Rotation Triggers
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.proxy_infra.domain.value_objects.node_status import NodeStatus

if TYPE_CHECKING:
    from src.proxy_infra.domain.ports.proxy_health_port import ProxyHealthPort
    from src.proxy_infra.domain.value_objects.health_status import HealthStatus
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
    from src.proxy_infra.domain.value_objects.proxy_pool import ProxyPool


class ProxyHealthService:
    """Domain service for proxy node health monitoring and rotation triggering.

    Delegates the actual network probe to the ProxyHealthPort adapter (keeps the
    domain layer free of network I/O per H-07). Rotation creates a replacement
    node via the caller-supplied provisioner port and returns an updated
    ProxyPool with the original node marked BURNED.

    Invariants:
        PI-003: Burned nodes must never be reused for routing. Rotation marks
            the failed node BURNED and provisions a replacement.

    References:
        - ADR-PROJ023-008: Health monitoring service design
        - TASK-023-038: Rotation sequence requirements
    """

    def __init__(self, health_port: ProxyHealthPort) -> None:
        """Initialize ProxyHealthService with a health monitoring port.

        Args:
            health_port: Health monitoring port implementation that performs
                actual network probes (SOCKS5 reachability, SSH daemon checks).
        """
        self._health_port = health_port

    def check_pool(self, pool: ProxyPool) -> list[HealthStatus]:
        """Run health checks on all nodes in the pool.

        Delegates each per-node probe to the health_port. Returns one
        HealthStatus per node in pool.nodes order.

        Args:
            pool: The proxy pool whose nodes should be checked.

        Returns:
            List of HealthStatus results, one per node. Empty list if the
            pool contains no nodes.
        """
        return [self._health_port.check_node(node) for node in pool.nodes]

    def check_node(self, node: ProxyNode) -> HealthStatus:
        """Run a health check on a single proxy node.

        Args:
            node: The proxy node to check.

        Returns:
            HealthStatus with probe results and timestamp.
        """
        return self._health_port.check_node(node)

    def detect_burned_nodes(self, pool: ProxyPool) -> list[ProxyNode]:
        """Identify nodes whose status is BURNED in the pool.

        Only inspects the in-memory NodeStatus field. Callers wishing to
        consult external blacklists should do so via the health_port adapter.

        Args:
            pool: The proxy pool to scan for burned nodes.

        Returns:
            List of ProxyNode instances whose status is BURNED.
        """
        return [node for node in pool.nodes if node.status == NodeStatus.BURNED]

    def trigger_rotation(
        self,
        pool: ProxyPool,
        node_id: str,
        provisioner: Any,
    ) -> ProxyPool:
        """Mark a node as BURNED and provision a replacement node in the same pool.

        Finds the node with the given node_id, replaces it in the pool with a
        BURNED copy, provisions a replacement via the provisioner port, and
        returns an updated ProxyPool containing the burned original and the
        replacement.

        Args:
            pool: Current proxy pool snapshot.
            node_id: ID of the node to rotate out.
            provisioner: ProxyProvisionerPort implementation used to provision
                the replacement node.

        Returns:
            Updated ProxyPool with:
                - The original node status set to BURNED.
                - A new replacement node appended.

        Raises:
            ValueError: If node_id is not found in pool.nodes.
        """
        from dataclasses import replace as dc_replace

        from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig

        # Locate the node to rotate
        target = next((n for n in pool.nodes if n.id == node_id), None)
        if target is None:
            raise ValueError(
                f"Node {node_id!r} not found in pool for engagement "
                f"{pool.engagement_id!r}. Cannot trigger rotation for an "
                f"unknown node."
            )

        # Mark the node BURNED (PI-003)
        burned_node = dc_replace(target, status=NodeStatus.BURNED)

        # Build updated nodes list with burned node replacing original
        updated_nodes = tuple(
            burned_node if n.id == node_id else n for n in pool.nodes
        )

        # Provision replacement in same region/role/type
        config = ProvisionConfig(
            provider=target.provider,
            region=target.region,
            engagement_id=target.engagement_id,
            engagement_tag=target.engagement_id,
            count=1,
            role=target.role,
            proxy_type=target.proxy_type,
            ssh_public_key="",
            operator_ip="0.0.0.0",
        )
        replacement_nodes = provisioner.provision(config)

        # Append replacement to pool
        all_nodes = updated_nodes + tuple(replacement_nodes)

        return type(pool)(
            nodes=all_nodes,
            lb_strategy=pool.lb_strategy,
            fail_mode=pool.fail_mode,
            max_nodes=pool.max_nodes,
            engagement_id=pool.engagement_id,
        )
