# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProxyPoolService — domain service orchestrating proxy pool lifecycle.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.ports.credential_store_port import CredentialStorePort
    from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
    from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
    from src.proxy_infra.domain.value_objects.pool_manifest import PoolManifest
    from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
    from src.proxy_infra.domain.value_objects.proxy_pool import ProxyPool


class ProxyPoolService:
    """Orchestrates proxy pool lifecycle operations.

    Coordinates provisioning, rotation, and destruction through the
    ProxyProvisionerPort, applying domain invariants:

    - PI-001: Max nodes per engagement
    - PI-002: Engagement scope requirement
    - PI-003: Burned-node detection and automatic rotation
    - PI-004: Pool manifest integrity maintenance
    - PI-005: SSH key cleanup on destroy
    - PI-006: Firewall rule defaults
    - PI-007: Audit log for all mutations

    References:
        - ADR-PROJ023-008: Domain service design
    """

    def __init__(
        self,
        provisioner: ProxyProvisionerPort,
        credential_store: CredentialStorePort,
    ) -> None:
        """Initialize ProxyPoolService with required port adapters.

        Args:
            provisioner: Cloud provider provisioner port implementation.
            credential_store: Credential storage port implementation.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def provision(self, config: ProvisionConfig) -> list[ProxyNode]:
        """Provision new proxy nodes and add them to the pool.

        Enforces PI-001 (max nodes), PI-002 (engagement scope),
        PI-006 (firewall defaults), and PI-007 (audit log).

        Args:
            config: Provisioning parameters including count, region, and role.

        Returns:
            List of newly provisioned ProxyNode instances.

        Raises:
            PoolLimitExceededError: If provision would exceed max_nodes (PI-001).
            EngagementScopeError: If engagement_id is missing (PI-002).
            ProvisionError: If the cloud provider returns an error.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def destroy(self, engagement_id: str, node_ids: list[str] | None = None) -> DestroyResult:
        """Destroy proxy nodes and clean up associated resources.

        Enforces PI-002 (engagement scope), PI-005 (SSH key cleanup),
        and PI-007 (audit log).

        Args:
            engagement_id: Owning engagement identifier (PI-002).
            node_ids: Specific node IDs to destroy, or None to destroy all
                nodes for the engagement.

        Returns:
            DestroyResult with success/failure details per node.

        Raises:
            EngagementScopeError: If engagement_id is missing (PI-002).
            TeardownError: If cleanup fails for one or more nodes.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def rotate(self, engagement_id: str, node_id: str, reason: str = "") -> ProxyNode:
        """Rotate a proxy node by provisioning a replacement before destroying the old one.

        Enforces PI-003 (burned-node no reuse): provisions replacement first,
        then destroys the original node.

        Args:
            engagement_id: Owning engagement identifier (PI-002).
            node_id: Provider-assigned ID of the node to rotate out.
            reason: Human-readable rotation reason for the audit log.

        Returns:
            The newly provisioned replacement ProxyNode.

        Raises:
            EngagementScopeError: If engagement_id is missing (PI-002).
            ProvisionError: If replacement provisioning fails.
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def get_pool(self, engagement_id: str) -> ProxyPool:
        """Return the current pool snapshot for an engagement.

        Args:
            engagement_id: Owning engagement identifier.

        Returns:
            Current ProxyPool snapshot.

        Raises:
            EngagementScopeError: If engagement_id is missing (PI-002).
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")

    def get_manifest(self, engagement_id: str) -> PoolManifest:
        """Return the current pool manifest for an engagement.

        Verifies integrity hash before returning (PI-004).

        Args:
            engagement_id: Owning engagement identifier.

        Returns:
            PoolManifest with integrity-verified pool state.

        Raises:
            ManifestIntegrityError: If integrity check fails (PI-004).
            EngagementScopeError: If engagement_id is missing (PI-002).
        """
        raise NotImplementedError("TASK-023-027: not yet implemented")
