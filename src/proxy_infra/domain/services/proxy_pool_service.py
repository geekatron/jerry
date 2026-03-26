# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ProxyPoolService — domain service orchestrating proxy pool lifecycle.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING, Any

from src.proxy_infra.domain.exceptions.burned_node_reuse_error import BurnedNodeReuseError
from src.proxy_infra.domain.exceptions.fingerprint_required_error import FingerprintRequiredError
from src.proxy_infra.domain.exceptions.invalid_engagement_id_error import InvalidEngagementIdError
from src.proxy_infra.domain.exceptions.manifest_integrity_error import ManifestIntegrityError
from src.proxy_infra.domain.exceptions.pool_capacity_exceeded_error import PoolCapacityExceededError
from src.proxy_infra.domain.value_objects.firewall_rule import FirewallRule
from src.proxy_infra.domain.value_objects.node_status import NodeStatus

if TYPE_CHECKING:
    from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
    from src.proxy_infra.domain.value_objects.pool_manifest import PoolManifest
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
        credential_store: Any = None,
    ) -> None:
        """Initialize ProxyPoolService with required port adapters.

        Args:
            provisioner: Cloud provider provisioner port implementation.
            credential_store: Optional credential storage port implementation.
        """
        self._provisioner = provisioner
        self._credential_store = credential_store

    # -------------------------------------------------------------------------
    # PI-001: Capacity enforcement
    # -------------------------------------------------------------------------

    def check_capacity(self, pool: ProxyPool, requested_count: int) -> None:
        """Verify the pool has capacity for the requested number of new nodes (PI-001).

        Args:
            pool: Current pool snapshot including existing node count.
            requested_count: Number of new nodes the caller wants to add.

        Raises:
            PoolCapacityExceededError: If existing nodes + requested_count would
                exceed pool.max_nodes.
        """
        current_count = len(pool.nodes)
        if current_count + requested_count > pool.max_nodes:
            raise PoolCapacityExceededError(
                f"Pool capacity exceeded for engagement {pool.engagement_id!r}: "
                f"current={current_count}, requested={requested_count}, "
                f"max_nodes={pool.max_nodes}. "
                f"Rotate or destroy existing nodes before provisioning more."
            )

    # -------------------------------------------------------------------------
    # PI-002: Engagement scope validation
    # -------------------------------------------------------------------------

    def validate_engagement_id(self, engagement_id: str) -> None:
        """Validate that engagement_id is a non-empty, non-whitespace string (PI-002).

        Args:
            engagement_id: Engagement identifier to validate.

        Raises:
            InvalidEngagementIdError: If engagement_id is empty, whitespace-only,
                or otherwise invalid.
        """
        if not engagement_id or not engagement_id.strip():
            raise InvalidEngagementIdError(
                f"A valid engagement_id is required for all mutating operations (PI-002). "
                f"Received: {engagement_id!r}. "
                f"Provide a non-empty engagement ID such as 'ENG-001'."
            )

    # -------------------------------------------------------------------------
    # PI-003: Burned-node routing guard
    # -------------------------------------------------------------------------

    def assert_node_is_routable(self, node: ProxyNode) -> None:
        """Assert that a node is safe to route traffic through (PI-003).

        Burned nodes and unhealthy nodes must never receive traffic — a burned
        node has been detected or blocked by the target; routing through it
        risks deanonymisation.

        Args:
            node: The proxy node to check.

        Raises:
            BurnedNodeReuseError: If the node is BURNED or UNHEALTHY.
        """
        non_routable_statuses = {NodeStatus.BURNED, NodeStatus.UNHEALTHY}
        if node.status in non_routable_statuses:
            raise BurnedNodeReuseError(
                f"Node {node.id!r} cannot be used for routing: "
                f"status is {node.status.value!r}. "
                f"Burned and unhealthy nodes must be rotated, not reused (PI-003)."
            )

    # -------------------------------------------------------------------------
    # PI-004: Manifest integrity verification
    # -------------------------------------------------------------------------

    def compute_manifest_hash(self, pool: ProxyPool) -> str:
        """Compute a deterministic SHA-256 hash of the pool's node data (PI-004).

        The hash is derived from a canonical JSON serialisation of the pool
        nodes, sorted by node ID to ensure determinism regardless of insertion
        order.

        Args:
            pool: The pool whose node data to hash.

        Returns:
            Hex-encoded SHA-256 digest prefixed with 'sha256:'.
        """
        node_data = sorted(
            [
                {
                    "id": n.id,
                    "provider": n.provider,
                    "ip": n.ip,
                    "region": n.region,
                    "role": str(n.role),
                    "proxy_type": str(n.proxy_type),
                    "status": str(n.status),
                    "ssh_key_id": n.ssh_key_id,
                    "socks_port": n.socks_port,
                    "created_at": n.created_at.isoformat(),
                    "engagement_id": n.engagement_id,
                    "fingerprint": n.fingerprint,
                }
                for n in pool.nodes
            ],
            key=lambda x: x["id"],
        )
        payload = json.dumps(node_data, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return f"sha256:{digest}"

    def verify_manifest_integrity(self, manifest: PoolManifest) -> None:
        """Verify the manifest integrity hash against the pool data (PI-004).

        Args:
            manifest: The pool manifest to verify.

        Raises:
            ManifestIntegrityError: If the stored hash does not match the
                computed hash of the manifest's pool data.
        """
        expected_hash = self.compute_manifest_hash(manifest.pool)
        if manifest.integrity_hash != expected_hash:
            raise ManifestIntegrityError(
                f"Pool manifest integrity check failed for engagement "
                f"{manifest.engagement_id!r}. "
                f"Stored hash: {manifest.integrity_hash!r}. "
                f"Computed hash: {expected_hash!r}. "
                f"The manifest may have been tampered with (T-11)."
            )

    # -------------------------------------------------------------------------
    # PI-006: Firewall rule generation
    # -------------------------------------------------------------------------

    def generate_default_firewall_rules(
        self,
        operator_ip: str,
        socks_port: int,
    ) -> list[FirewallRule]:
        """Generate the default firewall rules restricting access to operator IP (PI-006).

        Rules restrict both SOCKS5 and SSH ingress to the operator's IP address
        only. Outbound traffic is unrestricted to allow proxies to reach target
        networks.

        Args:
            operator_ip: The operator's public IPv4 address (no CIDR suffix required;
                a /32 host route is applied automatically).
            socks_port: The SOCKS5 port to restrict.

        Returns:
            List of FirewallRule instances implementing the default security posture.
        """
        operator_cidr = f"{operator_ip}/32" if "/" not in operator_ip else operator_ip
        return [
            FirewallRule(
                direction="inbound",
                protocol="tcp",
                ports=str(socks_port),
                sources=operator_cidr,
            ),
            FirewallRule(
                direction="inbound",
                protocol="tcp",
                ports="22",
                sources=operator_cidr,
            ),
            FirewallRule(
                direction="outbound",
                protocol="tcp",
                ports="all",
                sources="0.0.0.0/0",
            ),
        ]

    # -------------------------------------------------------------------------
    # PI-007 / FM-010: Fingerprint gate for READY transition
    # -------------------------------------------------------------------------

    def assert_ready_transition_valid(self, node: ProxyNode) -> None:
        """Assert that a node may safely transition to or remain in READY status (FM-010 / PI-007).

        A node cannot be considered ready for routing until its SSH host key
        fingerprint has been verified out-of-band. Without this check, a
        man-in-the-middle droplet could be silently accepted into the pool (T-05).

        Args:
            node: The proxy node being evaluated for READY status.

        Raises:
            FingerprintRequiredError: If the node's fingerprint field is None.
        """
        if node.fingerprint is None:
            raise FingerprintRequiredError(
                f"Node {node.id!r} cannot transition to READY: "
                f"fingerprint has not been verified (FM-010 / PI-007). "
                f"Run SSH host key verification before marking the node as routable."
            )
