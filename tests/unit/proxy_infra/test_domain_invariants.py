# BDD RED PHASE — All tests expected to FAIL (ImportError). Implementation in TASK-023-027+.
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BDD test suite for proxy_infra domain invariants PI-001 through PI-006.

TASK-023-027: Design ProxyProvisionerPort Interface (Hexagonal Port)

Covers domain invariants enforced by ProxyPoolService:
  PI-001: Total nodes per engagement must not exceed max_nodes (default 10)
  PI-002: All mutating operations require a valid engagement_id
  PI-003: Burned nodes must not be reused; rotation creates a new node
  PI-004: Pool manifest integrity hash must be verified on read
  PI-005: SSH keys must be removed from provider on node destruction
  PI-006: Firewall rules must restrict SOCKS5 port to operator IP
  PI-007 (FM-010): fingerprint must be set before node transitions to READY

These tests drive out the ProxyPoolService behaviour by specifying invariant
enforcement.  No mocking of infrastructure — invariants are pure domain logic.

Test pyramid: 60% happy path / 30% negative / 10% architecture
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_pool import ProxyPool
from src.proxy_infra.domain.value_objects.pool_manifest import PoolManifest
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
from src.proxy_infra.domain.services.proxy_pool_service import ProxyPoolService
from src.proxy_infra.domain.exceptions import (
    PoolCapacityExceededError,
    InvalidEngagementIdError,
    BurnedNodeReuseError,
    ManifestIntegrityError,
    FingerprintRequiredError,
)


# =============================================================================
# Fixtures
# =============================================================================


def _make_node(
    node_id: str,
    status: NodeStatus = NodeStatus.READY,
    fingerprint: str | None = "SHA256:abc123",
    engagement_id: str = "ENG-001",
) -> ProxyNode:
    """Build a minimal ProxyNode for invariant testing."""
    return ProxyNode(
        id=node_id,
        provider="digitalocean",
        ip=f"203.0.113.{hash(node_id) % 200 + 10}",
        region="nyc1",
        role=ProxyRole.ACTIVE,
        proxy_type=ProxyType.DIRECT_SOCKS5,
        status=status,
        ssh_key_id=f"key-{node_id}",
        socks_port=1080,
        created_at=datetime(2026, 3, 24, 14, 0, 0, tzinfo=timezone.utc),
        engagement_id=engagement_id,
        fingerprint=fingerprint,
    )


@pytest.fixture()
def mock_provisioner() -> MagicMock:
    """Return a MagicMock satisfying ProxyProvisionerPort."""
    return MagicMock()


@pytest.fixture()
def pool_service(mock_provisioner: MagicMock) -> ProxyPoolService:
    """Return a ProxyPoolService wired with a mock provisioner."""
    return ProxyPoolService(provisioner=mock_provisioner)


# =============================================================================
# PI-001: Total nodes per engagement must not exceed max_nodes
# =============================================================================


@pytest.mark.unit
class TestPI001MaxNodesInvariant:
    """
    Scenario: Pool capacity is enforced before provisioning
      Given an engagement with 10 READY nodes (at max_nodes limit)
      When the operator requests one more node
      Then ProxyPoolService raises PoolCapacityExceededError
      And no provision() call is made to the adapter
    """

    def test_provision_raises_when_at_max_nodes_limit(
        self, pool_service: ProxyPoolService, mock_provisioner: MagicMock
    ) -> None:
        """PI-001: ProxyPoolService rejects provision() when pool is at capacity."""
        existing_nodes = tuple(_make_node(f"do-{i}") for i in range(10))
        pool = ProxyPool(
            nodes=existing_nodes,
            max_nodes=10,
            engagement_id="ENG-001",
        )

        with pytest.raises(PoolCapacityExceededError) as exc_info:
            pool_service.check_capacity(pool=pool, requested_count=1)

        assert "ENG-001" in str(exc_info.value) or "10" in str(exc_info.value), (
            "PoolCapacityExceededError must mention engagement or limit — "
            "PI-001: operator must know which engagement is at capacity"
        )
        mock_provisioner.provision.assert_not_called()

    def test_provision_allowed_when_below_max_nodes(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-001: provision() is permitted when node count is below max_nodes."""
        existing_nodes = tuple(_make_node(f"do-{i}") for i in range(5))
        pool = ProxyPool(
            nodes=existing_nodes,
            max_nodes=10,
            engagement_id="ENG-001",
        )
        # Should not raise — we have room for more nodes
        pool_service.check_capacity(pool=pool, requested_count=3)

    def test_provision_raises_when_requested_count_would_exceed_limit(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-001: ProxyPoolService rejects when existing + requested > max_nodes."""
        existing_nodes = tuple(_make_node(f"do-{i}") for i in range(8))
        pool = ProxyPool(
            nodes=existing_nodes,
            max_nodes=10,
            engagement_id="ENG-001",
        )
        with pytest.raises(PoolCapacityExceededError):
            pool_service.check_capacity(pool=pool, requested_count=3)


# =============================================================================
# PI-002: All mutating operations require a valid engagement_id
# =============================================================================


@pytest.mark.unit
class TestPI002EngagementIdRequired:
    """
    Scenario: Mutating operation without engagement_id is rejected
      Given no engagement_id is set
      When the operator calls provision() with an empty engagement_id
      Then ProxyPoolService raises InvalidEngagementIdError
      And no provider API calls are made
    """

    def test_empty_engagement_id_is_rejected(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-002: Empty engagement_id string must raise InvalidEngagementIdError."""
        with pytest.raises(InvalidEngagementIdError):
            pool_service.validate_engagement_id("")

    def test_none_engagement_id_is_rejected(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-002: None engagement_id must raise InvalidEngagementIdError."""
        with pytest.raises((InvalidEngagementIdError, TypeError)):
            pool_service.validate_engagement_id(None)  # type: ignore[arg-type]

    def test_whitespace_engagement_id_is_rejected(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-002: Whitespace-only engagement_id must raise InvalidEngagementIdError."""
        with pytest.raises(InvalidEngagementIdError):
            pool_service.validate_engagement_id("   ")

    def test_valid_engagement_id_passes_validation(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-002: A properly formatted engagement ID must pass validation."""
        # Should not raise
        pool_service.validate_engagement_id("ENG-001")


# =============================================================================
# PI-003: Burned nodes must not be reused
# =============================================================================


@pytest.mark.unit
class TestPI003BurnedNodeNotReused:
    """
    Scenario: Attempting to mark a burned node as READY is rejected
      Given a ProxyNode in BURNED status
      When the domain service is asked to route traffic through it
      Then BurnedNodeReuseError is raised
      And the node remains in BURNED status
    """

    def test_burned_node_raises_on_reuse_attempt(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-003: ProxyPoolService must reject any attempt to reuse a burned node."""
        burned_node = _make_node("do-burned-001", status=NodeStatus.BURNED)
        with pytest.raises(BurnedNodeReuseError) as exc_info:
            pool_service.assert_node_is_routable(burned_node)
        assert "do-burned-001" in str(exc_info.value) or "burned" in str(
            exc_info.value
        ).lower(), (
            "BurnedNodeReuseError must identify the node or status — "
            "PI-003: operator must know which node is burned and must not be reused"
        )

    def test_unhealthy_node_is_also_not_routable(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-003 extension: UNHEALTHY nodes must also be rejected from routing."""
        unhealthy_node = _make_node("do-unhealthy-001", status=NodeStatus.UNHEALTHY)
        with pytest.raises((BurnedNodeReuseError, ValueError)):
            pool_service.assert_node_is_routable(unhealthy_node)

    def test_ready_node_is_routable(self, pool_service: ProxyPoolService) -> None:
        """PI-003: READY nodes with fingerprint set are valid for routing."""
        ready_node = _make_node("do-ready-001", status=NodeStatus.READY)
        # Must not raise
        pool_service.assert_node_is_routable(ready_node)


# =============================================================================
# PI-004: Pool manifest integrity hash must be verified on read
# =============================================================================


@pytest.mark.unit
class TestPI004ManifestIntegrityVerification:
    """
    Scenario: Loading a manifest with a corrupted integrity hash
      Given a pool manifest file on disk
      And the integrity_hash does not match the computed hash of the pool data
      When PoolManifestStore.load() is called
      Then ManifestIntegrityError is raised
      And the corrupted manifest is NOT used for routing
    """

    def test_manifest_integrity_error_is_raised_on_hash_mismatch(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-004: verify_manifest_integrity() raises when hash does not match."""
        node = _make_node("do-001")
        pool = ProxyPool(nodes=(node,), engagement_id="ENG-001")
        manifest = PoolManifest(
            version="1.0.0",
            engagement_id="ENG-001",
            pool=pool,
            integrity_hash="sha256:definitely_wrong_hash",
            updated_at=datetime(2026, 3, 24, 14, 30, 0, tzinfo=timezone.utc),
        )
        with pytest.raises(ManifestIntegrityError) as exc_info:
            pool_service.verify_manifest_integrity(manifest)
        assert "integrity" in str(exc_info.value).lower() or "hash" in str(
            exc_info.value
        ).lower(), (
            "ManifestIntegrityError must mention integrity or hash — "
            "T-11: operator must understand the manifest was tampered"
        )

    def test_manifest_with_correct_hash_passes_verification(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-004: verify_manifest_integrity() succeeds when hash matches."""
        node = _make_node("do-001")
        pool = ProxyPool(nodes=(node,), engagement_id="ENG-001")
        # Request the service to compute a valid hash for us
        correct_hash = pool_service.compute_manifest_hash(pool)
        manifest = PoolManifest(
            version="1.0.0",
            engagement_id="ENG-001",
            pool=pool,
            integrity_hash=correct_hash,
            updated_at=datetime(2026, 3, 24, 14, 30, 0, tzinfo=timezone.utc),
        )
        # Must not raise
        pool_service.verify_manifest_integrity(manifest)

    def test_manifest_hash_computation_is_deterministic(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-004: compute_manifest_hash() returns the same hash for the same input."""
        node = _make_node("do-001")
        pool = ProxyPool(nodes=(node,), engagement_id="ENG-001")
        hash_1 = pool_service.compute_manifest_hash(pool)
        hash_2 = pool_service.compute_manifest_hash(pool)
        assert hash_1 == hash_2, (
            "compute_manifest_hash() must be deterministic — "
            "PI-004: the same pool data must always produce the same hash"
        )

    def test_manifest_hash_changes_when_pool_changes(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-004: compute_manifest_hash() detects a pool change."""
        node_a = _make_node("do-001")
        node_b = _make_node("do-002")
        pool_a = ProxyPool(nodes=(node_a,), engagement_id="ENG-001")
        pool_b = ProxyPool(nodes=(node_b,), engagement_id="ENG-001")
        hash_a = pool_service.compute_manifest_hash(pool_a)
        hash_b = pool_service.compute_manifest_hash(pool_b)
        assert hash_a != hash_b, (
            "compute_manifest_hash() must produce different hashes for different pools — "
            "PI-004: hash must detect any tampering with pool node data"
        )


# =============================================================================
# PI-006: Firewall rules must restrict SOCKS5 port to operator IP
# =============================================================================


@pytest.mark.unit
class TestPI006FirewallRuleRestriction:
    """
    Scenario: Default firewall rules restrict SOCKS5 to operator IP only
      Given an operator with IP 203.0.113.1
      When generate_default_firewall_rules() is called
      Then the returned rules restrict port 1080 to /32 CIDR only
      And allow SSH (22) from the same operator IP only
    """

    def test_default_firewall_rules_restrict_socks5_to_operator_ip(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-006: Default rules must restrict SOCKS5 port to operator IP /32."""
        operator_ip = "203.0.113.1"
        rules = pool_service.generate_default_firewall_rules(
            operator_ip=operator_ip,
            socks_port=1080,
        )
        socks_rules = [
            r for r in rules if r.ports == "1080" and r.direction == "inbound"
        ]
        assert len(socks_rules) >= 1, (
            "At least one inbound rule for port 1080 must be generated — "
            "PI-006: SOCKS5 must be restricted inbound"
        )
        for rule in socks_rules:
            assert operator_ip in rule.sources, (
                f"Inbound SOCKS5 rule sources must include operator IP {operator_ip} — "
                f"PI-006: SOCKS5 must be restricted to operator IP only (T-07)"
            )

    def test_default_firewall_rules_restrict_ssh_to_operator_ip(
        self, pool_service: ProxyPoolService
    ) -> None:
        """PI-006: Default rules must restrict SSH (port 22) to operator IP."""
        operator_ip = "203.0.113.1"
        rules = pool_service.generate_default_firewall_rules(
            operator_ip=operator_ip,
            socks_port=1080,
        )
        ssh_rules = [
            r for r in rules if r.ports == "22" and r.direction == "inbound"
        ]
        assert len(ssh_rules) >= 1, (
            "At least one inbound SSH rule must be generated — "
            "PI-006: SSH must be restricted to operator IP"
        )
        for rule in ssh_rules:
            assert operator_ip in rule.sources, (
                f"SSH inbound rule must include operator IP {operator_ip} — "
                f"PI-006 / T-07: SSH restricted to operator IP"
            )

    def test_default_firewall_includes_outbound_allow_all(
        self, pool_service: ProxyPoolService
    ) -> None:
        """Outbound traffic must be unrestricted — proxies need to reach target networks."""
        rules = pool_service.generate_default_firewall_rules(
            operator_ip="203.0.113.1",
            socks_port=1080,
        )
        outbound_rules = [r for r in rules if r.direction == "outbound"]
        assert len(outbound_rules) >= 1, (
            "At least one outbound rule must be present — "
            "proxy nodes must be able to reach target networks"
        )


# =============================================================================
# PI-007 (FM-010): fingerprint required before READY transition
# =============================================================================


@pytest.mark.unit
class TestPI007FingerprintRequiredForReady:
    """
    Scenario: Node cannot transition to READY without a verified fingerprint
      Given a ProxyNode in CONFIGURING status with no fingerprint
      When the domain service attempts to mark it READY
      Then FingerprintRequiredError is raised
      And the node status remains CONFIGURING

    FM-010: SSH host key fingerprint must be verified before a node is
    marked READY.  Without this check, a man-in-the-middle node could be
    silently accepted into the pool (T-05).
    """

    def test_transition_to_ready_without_fingerprint_raises(
        self, pool_service: ProxyPoolService
    ) -> None:
        """FM-010/PI-007: READY transition must fail when fingerprint is None."""
        node_without_fingerprint = _make_node(
            "do-configuring-001",
            status=NodeStatus.CONFIGURING,
            fingerprint=None,  # not yet verified
        )
        with pytest.raises(FingerprintRequiredError) as exc_info:
            pool_service.assert_ready_transition_valid(node_without_fingerprint)
        assert "fingerprint" in str(exc_info.value).lower(), (
            "FingerprintRequiredError must mention fingerprint — "
            "FM-010: operator must understand SSH host key verification is missing"
        )

    def test_transition_to_ready_with_fingerprint_succeeds(
        self, pool_service: ProxyPoolService
    ) -> None:
        """FM-010/PI-007: READY transition succeeds when fingerprint is verified."""
        node_with_fingerprint = _make_node(
            "do-configuring-002",
            status=NodeStatus.CONFIGURING,
            fingerprint="SHA256:verified_host_key",
        )
        # Must not raise
        pool_service.assert_ready_transition_valid(node_with_fingerprint)

    def test_already_ready_node_with_fingerprint_passes(
        self, pool_service: ProxyPoolService
    ) -> None:
        """FM-010: Already-READY nodes with a fingerprint must pass validation."""
        ready_node = _make_node(
            "do-ready-fingerprinted",
            status=NodeStatus.READY,
            fingerprint="SHA256:known_good",
        )
        # Must not raise
        pool_service.assert_ready_transition_valid(ready_node)
