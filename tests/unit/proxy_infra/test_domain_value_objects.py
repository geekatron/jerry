# BDD RED PHASE — All tests expected to FAIL (ImportError). Implementation in TASK-023-027+.
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BDD test suite for proxy_infra domain value objects.

TASK-023-027: Design ProxyProvisionerPort Interface (Hexagonal Port)

Covers:
  - NodeStatus enum: all states present, str-enum behaviour
  - ProxyRole, ProxyType enums: all values present
  - ProxyNode frozen dataclass: field presence, immutability
  - ProxyPool frozen dataclass: field presence, default values
  - PoolManifest frozen dataclass: integrity_hash field, version field
  - FirewallRule frozen dataclass: required fields

Test pyramid: 60% happy path / 30% negative / 10% architecture
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_pool import ProxyPool
from src.proxy_infra.domain.value_objects.pool_manifest import PoolManifest
from src.proxy_infra.domain.value_objects.firewall_rule import FirewallRule


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def sample_proxy_node() -> ProxyNode:
    """Return a minimal valid ProxyNode in READY status with fingerprint set."""
    return ProxyNode(
        id="do-12345",
        provider="digitalocean",
        ip="203.0.113.10",
        region="nyc1",
        role=ProxyRole.ACTIVE,
        proxy_type=ProxyType.DIRECT_SOCKS5,
        status=NodeStatus.READY,
        ssh_key_id="key-98765",
        socks_port=1080,
        created_at=datetime(2026, 3, 24, 14, 0, 0, tzinfo=timezone.utc),
        engagement_id="ENG-001",
        fingerprint="SHA256:abc123def456",
    )


@pytest.fixture()
def sample_proxy_pool(sample_proxy_node: ProxyNode) -> ProxyPool:
    """Return a minimal valid ProxyPool with one READY node."""
    return ProxyPool(
        nodes=(sample_proxy_node,),
        engagement_id="ENG-001",
    )


# =============================================================================
# Happy path: NodeStatus enum
# =============================================================================


@pytest.mark.unit
class TestNodeStatus:
    """Verify NodeStatus enum defines the full proxy node lifecycle."""

    def test_all_lifecycle_states_present(self) -> None:
        """NodeStatus must define all states from the design: PROVISIONING through DESTROYED."""
        required_states = {
            "PROVISIONING",
            "CONFIGURING",
            "READY",
            "UNHEALTHY",
            "BURNED",
            "ROTATING",
            "DESTROYING",
            "DESTROYED",
        }
        actual_states = {s.name for s in NodeStatus}
        assert required_states <= actual_states, (
            f"NodeStatus is missing states: {required_states - actual_states} — "
            f"all lifecycle states are needed for ProxyPoolService to manage node transitions"
        )

    def test_node_status_is_str_enum(self) -> None:
        """NodeStatus must subclass str so it serialises cleanly to YAML/JSON.

        The pool manifest is written as YAML and must round-trip without
        special serialisation logic.
        """
        assert issubclass(NodeStatus, str), (
            "NodeStatus must be a str Enum — pool manifest serialisation "
            "requires statuses to serialise as plain strings, not enum objects"
        )

    def test_node_status_ready_value_is_lowercase_string(self) -> None:
        """NodeStatus.READY must have value 'ready' for YAML manifest compatibility."""
        assert NodeStatus.READY == "ready", (
            "NodeStatus.READY must equal the string 'ready' — "
            "the pool manifest YAML uses lowercase string values"
        )

    def test_node_status_burned_value_is_lowercase_string(self) -> None:
        """NodeStatus.BURNED must have value 'burned'."""
        assert NodeStatus.BURNED == "burned", (
            "NodeStatus.BURNED must equal 'burned' — consistent with manifest YAML"
        )

    def test_node_status_can_be_compared_to_string(self) -> None:
        """NodeStatus values can be compared to plain strings (str Enum property)."""
        assert NodeStatus.PROVISIONING == "provisioning", (
            "NodeStatus must compare equal to equivalent string — "
            "simplifies manifest loading without explicit enum conversion"
        )


# =============================================================================
# Happy path: ProxyRole and ProxyType enums
# =============================================================================


@pytest.mark.unit
class TestProxyRoleAndType:
    """Verify ProxyRole and ProxyType enums define all required variants."""

    def test_proxy_role_has_all_required_values(self) -> None:
        """ProxyRole must define RECON, ACTIVE, EXPLOIT, RESERVE."""
        required = {"RECON", "ACTIVE", "EXPLOIT", "RESERVE"}
        actual = {r.name for r in ProxyRole}
        assert required <= actual, (
            f"ProxyRole missing values: {required - actual} — "
            f"phase-gated IP assignment requires all four role types"
        )

    def test_proxy_type_has_ssh_tunnel_and_direct_socks5(self) -> None:
        """ProxyType must define SSH_TUNNEL and DIRECT_SOCKS5."""
        required = {"SSH_TUNNEL", "DIRECT_SOCKS5"}
        actual = {t.name for t in ProxyType}
        assert required <= actual, (
            f"ProxyType missing values: {required - actual} — "
            f"both transport mechanisms must be selectable at provision time"
        )

    def test_proxy_role_is_str_enum(self) -> None:
        """ProxyRole must subclass str for YAML manifest serialisation."""
        assert issubclass(ProxyRole, str), (
            "ProxyRole must be a str Enum — pool manifest requires string values"
        )

    def test_proxy_type_is_str_enum(self) -> None:
        """ProxyType must subclass str for YAML manifest serialisation."""
        assert issubclass(ProxyType, str), (
            "ProxyType must be a str Enum — pool manifest requires string values"
        )


# =============================================================================
# Happy path: ProxyNode frozen dataclass
# =============================================================================


@pytest.mark.unit
class TestProxyNode:
    """Verify ProxyNode value object fields, immutability, and fingerprint semantics."""

    def test_proxy_node_has_all_required_fields(
        self, sample_proxy_node: ProxyNode
    ) -> None:
        """ProxyNode must expose all fields defined in the design (Section 3.1)."""
        required_fields = {
            "id",
            "provider",
            "ip",
            "region",
            "role",
            "proxy_type",
            "status",
            "ssh_key_id",
            "socks_port",
            "created_at",
            "engagement_id",
            "fingerprint",
        }
        actual_fields = set(sample_proxy_node.__dataclass_fields__.keys())
        assert required_fields <= actual_fields, (
            f"ProxyNode missing fields: {required_fields - actual_fields} — "
            f"all fields are required for manifest serialisation and CLM integration"
        )

    def test_proxy_node_is_frozen(self, sample_proxy_node: ProxyNode) -> None:
        """ProxyNode must be a frozen dataclass — value objects are immutable."""
        with pytest.raises((AttributeError, TypeError)):
            sample_proxy_node.status = NodeStatus.BURNED  # type: ignore[misc]

    def test_proxy_node_fingerprint_defaults_to_none(self) -> None:
        """ProxyNode.fingerprint defaults to None when created pre-SSH-verification.

        Nodes transition through PROVISIONING and CONFIGURING before SSH
        is available.  fingerprint is None until the post-boot injection
        sequence runs and verifies the host key (PI-007 step 7).
        """
        node = ProxyNode(
            id="do-99999",
            provider="digitalocean",
            ip="203.0.113.99",
            region="sfo3",
            role=ProxyRole.RESERVE,
            proxy_type=ProxyType.SSH_TUNNEL,
            status=NodeStatus.PROVISIONING,
            ssh_key_id="key-11111",
            socks_port=1080,
            created_at=datetime(2026, 3, 24, 14, 0, 0, tzinfo=timezone.utc),
            engagement_id="ENG-002",
        )
        assert node.fingerprint is None, (
            "ProxyNode.fingerprint must default to None — "
            "fingerprint is only available after SSH host key verification"
        )

    def test_proxy_node_socks_port_default_is_1080(self) -> None:
        """ProxyNode.socks_port defaults to 1080 per the design."""
        node = ProxyNode(
            id="do-77777",
            provider="digitalocean",
            ip="203.0.113.77",
            region="ams3",
            role=ProxyRole.ACTIVE,
            proxy_type=ProxyType.DIRECT_SOCKS5,
            status=NodeStatus.READY,
            ssh_key_id="key-22222",
            created_at=datetime(2026, 3, 24, 14, 0, 0, tzinfo=timezone.utc),
            engagement_id="ENG-001",
            fingerprint="SHA256:xyz789",
        )
        assert node.socks_port == 1080, (
            "ProxyNode.socks_port must default to 1080 — "
            "standard SOCKS5 port used in firewall rules and microsocks config"
        )


# =============================================================================
# Happy path: ProxyPool frozen dataclass
# =============================================================================


@pytest.mark.unit
class TestProxyPool:
    """Verify ProxyPool value object behaviour and defaults."""

    def test_proxy_pool_has_required_fields(
        self, sample_proxy_pool: ProxyPool
    ) -> None:
        """ProxyPool must have nodes, lb_strategy, fail_mode, max_nodes, engagement_id."""
        required_fields = {
            "nodes",
            "lb_strategy",
            "fail_mode",
            "max_nodes",
            "engagement_id",
        }
        actual_fields = set(sample_proxy_pool.__dataclass_fields__.keys())
        assert required_fields <= actual_fields, (
            f"ProxyPool missing fields: {required_fields - actual_fields}"
        )

    def test_proxy_pool_default_lb_strategy_is_round_robin(
        self, sample_proxy_pool: ProxyPool
    ) -> None:
        """ProxyPool lb_strategy defaults to 'round_robin'."""
        assert sample_proxy_pool.lb_strategy == "round_robin", (
            "ProxyPool.lb_strategy must default to 'round_robin' — "
            "balanced distribution across nodes for stealth"
        )

    def test_proxy_pool_default_fail_mode_is_closed(
        self, sample_proxy_pool: ProxyPool
    ) -> None:
        """ProxyPool fail_mode defaults to 'closed' (fail-safe).

        'closed' means: if all nodes go down, traffic is blocked rather than
        routed directly.  This prevents deanonymisation during node failures.
        """
        assert sample_proxy_pool.fail_mode == "closed", (
            "ProxyPool.fail_mode must default to 'closed' — "
            "fail-safe: traffic blocked when pool is empty to prevent deanonymisation"
        )

    def test_proxy_pool_default_max_nodes_is_10(
        self, sample_proxy_pool: ProxyPool
    ) -> None:
        """ProxyPool max_nodes defaults to 10 per RATELIMIT-006."""
        assert sample_proxy_pool.max_nodes == 10, (
            "ProxyPool.max_nodes must default to 10 — "
            "RATELIMIT-006: max nodes per engagement"
        )

    def test_proxy_pool_is_frozen(self, sample_proxy_pool: ProxyPool) -> None:
        """ProxyPool must be frozen — pool snapshots are immutable value objects."""
        with pytest.raises((AttributeError, TypeError)):
            sample_proxy_pool.lb_strategy = "random"  # type: ignore[misc]

    def test_proxy_pool_nodes_tuple_is_immutable(
        self, sample_proxy_pool: ProxyPool
    ) -> None:
        """ProxyPool.nodes must be a tuple (not list) to enforce immutability."""
        assert isinstance(sample_proxy_pool.nodes, tuple), (
            "ProxyPool.nodes must be a tuple, not a list — "
            "frozen dataclasses require immutable field types; list is mutable"
        )


# =============================================================================
# Happy path: PoolManifest frozen dataclass
# =============================================================================


@pytest.mark.unit
class TestPoolManifest:
    """Verify PoolManifest value object required fields and integrity semantics."""

    def test_pool_manifest_has_required_fields(
        self, sample_proxy_pool: ProxyPool
    ) -> None:
        """PoolManifest must have version, engagement_id, pool, integrity_hash, updated_at."""
        manifest = PoolManifest(
            version="1.0.0",
            engagement_id="ENG-001",
            pool=sample_proxy_pool,
            integrity_hash="sha256:a1b2c3d4e5f6",
            updated_at=datetime(2026, 3, 24, 14, 30, 0, tzinfo=timezone.utc),
        )
        required_fields = {
            "version",
            "engagement_id",
            "pool",
            "integrity_hash",
            "updated_at",
        }
        actual_fields = set(manifest.__dataclass_fields__.keys())
        assert required_fields <= actual_fields, (
            f"PoolManifest missing fields: {required_fields - actual_fields} — "
            f"CLM reads these fields to configure SOCKS5 load balancing"
        )

    def test_pool_manifest_integrity_hash_is_required(
        self, sample_proxy_pool: ProxyPool
    ) -> None:
        """PoolManifest.integrity_hash is required, not optional.

        T-11 (STRIDE): manifest tampering with wrong IPs could route traffic
        to attacker-controlled nodes.  SHA-256 integrity hash prevents this.
        """
        manifest = PoolManifest(
            version="1.0.0",
            engagement_id="ENG-001",
            pool=sample_proxy_pool,
            integrity_hash="sha256:deadbeef",
            updated_at=datetime(2026, 3, 24, 14, 30, 0, tzinfo=timezone.utc),
        )
        assert manifest.integrity_hash, (
            "PoolManifest.integrity_hash must be set — "
            "T-11: manifest tampering protection requires SHA-256 hash on every write"
        )

    def test_pool_manifest_is_frozen(self, sample_proxy_pool: ProxyPool) -> None:
        """PoolManifest must be frozen."""
        manifest = PoolManifest(
            version="1.0.0",
            engagement_id="ENG-001",
            pool=sample_proxy_pool,
            integrity_hash="sha256:abc",
            updated_at=datetime(2026, 3, 24, 14, 30, 0, tzinfo=timezone.utc),
        )
        with pytest.raises((AttributeError, TypeError)):
            manifest.integrity_hash = "sha256:tampered"  # type: ignore[misc]

    def test_pool_manifest_audit_trail_defaults_to_empty(
        self, sample_proxy_pool: ProxyPool
    ) -> None:
        """PoolManifest.audit_trail defaults to empty tuple."""
        manifest = PoolManifest(
            version="1.0.0",
            engagement_id="ENG-001",
            pool=sample_proxy_pool,
            integrity_hash="sha256:abc",
            updated_at=datetime(2026, 3, 24, 14, 30, 0, tzinfo=timezone.utc),
        )
        assert manifest.audit_trail == () or manifest.audit_trail == [], (
            "PoolManifest.audit_trail must default to empty — "
            "new manifests start with no operations in the trail"
        )


# =============================================================================
# Happy path: FirewallRule frozen dataclass
# =============================================================================


@pytest.mark.unit
class TestFirewallRule:
    """Verify FirewallRule value object field presence and immutability."""

    def test_firewall_rule_has_required_fields(self) -> None:
        """FirewallRule must have direction, protocol, ports, sources."""
        rule = FirewallRule(
            direction="inbound",
            protocol="tcp",
            ports="1080",
            sources="203.0.113.1/32",
        )
        assert rule.direction == "inbound", "FirewallRule.direction must be set"
        assert rule.protocol == "tcp", "FirewallRule.protocol must be set"
        assert rule.ports == "1080", "FirewallRule.ports must be set"
        assert rule.sources == "203.0.113.1/32", "FirewallRule.sources must be set"

    def test_firewall_rule_is_frozen(self) -> None:
        """FirewallRule must be frozen — rules are immutable once created."""
        rule = FirewallRule(
            direction="inbound",
            protocol="tcp",
            ports="22",
            sources="203.0.113.1/32",
        )
        with pytest.raises((AttributeError, TypeError)):
            rule.ports = "23"  # type: ignore[misc]

    def test_firewall_rule_ssh_port_restriction(self) -> None:
        """A FirewallRule for SSH on port 22 restricted to operator IP is constructible."""
        rule = FirewallRule(
            direction="inbound",
            protocol="tcp",
            ports="22",
            sources="203.0.113.1/32",
        )
        assert rule.ports == "22", (
            "FirewallRule must represent SSH port 22 restriction — "
            "T-07: firewall must restrict SSH to operator IP only"
        )

    def test_firewall_rule_port_range_is_valid_value(self) -> None:
        """FirewallRule.ports accepts a range string like '1080-1090'."""
        rule = FirewallRule(
            direction="inbound",
            protocol="tcp",
            ports="1080-1090",
            sources="203.0.113.0/24",
        )
        assert "1080-1090" in rule.ports, (
            "FirewallRule.ports must accept port range strings — "
            "multi-port SOCKS5 configurations require range notation"
        )
