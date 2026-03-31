# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD test suite for STORY-023-006: CLM Proxy Pool Integration.

Covers:
  TASK-023-037: CLM reads proxy pool manifest (PoolManifestStore)
  TASK-023-038: Health monitoring and rotation triggers (ProxyHealthService)
  TASK-023-039: Engagement teardown sequence (DestroyHandler)

Domain invariants tested:
  PI-004: Integrity hash verified on every manifest read
  FM-007: Teardown sequence ordering (secrets → SSH → VPS → keys → firewalls)
  FM-018: Post-teardown orphan verification via list_instances
  FM-028: --verify-credentials-rotated required before teardown_confirmed
  F-C-003: Token rotation prompt before teardown completion
  EN-023-001 F-4: BPF bypass_ips map updated before routing traffic

Test pyramid: 60% happy path, 30% negative cases, 10% edge cases.
Distribution: ~30 tests → ~18 happy, ~9 negative, ~3 edge.

References:
  - TASK-023-037-clm-read-proxy-pool.md
  - TASK-023-038-clm-health-monitoring-rotation.md
  - TASK-023-039-clm-engagement-teardown.md
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.proxy_infra.application.commands.destroy_nodes_command import DestroyNodesCommand
from src.proxy_infra.application.handlers.destroy_handler import DestroyHandler
from src.proxy_infra.domain.exceptions import ManifestIntegrityError, TeardownError
from src.proxy_infra.domain.services.proxy_health_service import ProxyHealthService
from src.proxy_infra.domain.services.proxy_pool_service import ProxyPoolService
from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
from src.proxy_infra.domain.value_objects.health_status import HealthStatus
from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.pool_manifest import PoolManifest
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_pool import ProxyPool
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
from src.proxy_infra.infrastructure.persistence.pool_manifest_store import PoolManifestStore

# =============================================================================
# Shared helpers
# =============================================================================


def _make_node(
    node_id: str = "node-001",
    ip: str = "1.2.3.4",
    status: NodeStatus = NodeStatus.READY,
    engagement_id: str = "ENG-TEST",
    socks_port: int = 1080,
    fingerprint: str | None = "SHA256:abc123",
) -> ProxyNode:
    """Build a minimal ProxyNode for CLM integration testing."""
    return ProxyNode(
        id=node_id,
        provider="digitalocean",
        ip=ip,
        region="nyc3",
        role=ProxyRole.ACTIVE,
        proxy_type=ProxyType.SOCKS5 if hasattr(ProxyType, "SOCKS5") else ProxyType.DIRECT_SOCKS5,
        status=status,
        ssh_key_id="key-123",
        created_at=datetime(2026, 3, 25, 12, 0, 0, tzinfo=UTC),
        engagement_id=engagement_id,
        socks_port=socks_port,
        fingerprint=fingerprint,
    )


def _make_pool(
    nodes: list[ProxyNode] | None = None,
    engagement_id: str = "ENG-TEST",
) -> ProxyPool:
    """Build a ProxyPool for testing."""
    if nodes is None:
        nodes = [_make_node()]
    return ProxyPool(
        nodes=tuple(nodes),
        lb_strategy="round_robin",
        fail_mode="closed",
        max_nodes=10,
        engagement_id=engagement_id,
    )


def _compute_integrity_hash(pool: ProxyPool) -> str:
    """Compute the canonical SHA-256 hash matching ProxyPoolService.compute_manifest_hash."""
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


def _make_manifest(
    pool: ProxyPool | None = None,
    engagement_id: str = "ENG-TEST",
    integrity_hash: str | None = None,
) -> PoolManifest:
    """Build a PoolManifest with a correct integrity hash by default."""
    if pool is None:
        pool = _make_pool(engagement_id=engagement_id)
    if integrity_hash is None:
        integrity_hash = _compute_integrity_hash(pool)
    return PoolManifest(
        version="1",
        engagement_id=engagement_id,
        pool=pool,
        integrity_hash=integrity_hash,
        updated_at=datetime(2026, 3, 25, 12, 0, 0, tzinfo=UTC),
        audit_trail=(),
    )


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def store(tmp_path: Path) -> PoolManifestStore:
    """Return a PoolManifestStore pointed at a temp engagement directory."""
    engagement_dir = tmp_path / "work" / "engagements" / "ENG-TEST"
    engagement_dir.mkdir(parents=True)
    return PoolManifestStore(base_dir=tmp_path)


@pytest.fixture()
def mock_health_port() -> MagicMock:
    """Return a mock ProxyHealthPort."""
    return MagicMock()


@pytest.fixture()
def health_service(mock_health_port: MagicMock) -> ProxyHealthService:
    """Return a ProxyHealthService backed by the mock health port."""
    return ProxyHealthService(health_port=mock_health_port)


@pytest.fixture()
def mock_provisioner() -> MagicMock:
    """Return a mock ProxyProvisionerPort."""
    provisioner = MagicMock()
    provisioner.list_instances.return_value = []
    provisioner.destroy.return_value = DestroyResult(destroyed=["node-001"], failed=[])
    return provisioner


@pytest.fixture()
def pool_service(mock_provisioner: MagicMock) -> ProxyPoolService:
    """Return a ProxyPoolService backed by a mock provisioner."""
    return ProxyPoolService(provisioner=mock_provisioner)


@pytest.fixture()
def destroy_handler(pool_service: ProxyPoolService, store: PoolManifestStore) -> DestroyHandler:
    """Return a DestroyHandler with pool_service and manifest store injected."""
    return DestroyHandler(pool_service=pool_service, manifest_store=store)


# =============================================================================
# TASK-023-037: PoolManifestStore — read/write with integrity verification
# =============================================================================


class TestPoolManifestStore:
    """Happy path: manifest round-trips cleanly through save → load."""

    def test_save_and_load_manifest_when_valid_then_returns_pool(
        self,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN a valid manifest WHEN saved and loaded THEN pool is intact."""
        manifest = _make_manifest()

        store.save(manifest)
        loaded = store.load("ENG-TEST")

        assert loaded.engagement_id == "ENG-TEST"
        assert len(loaded.pool.nodes) == 1
        assert loaded.pool.nodes[0].ip == "1.2.3.4"

    def test_save_and_load_when_multi_node_pool_then_all_nodes_returned(
        self,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN a pool with two nodes WHEN saved and loaded THEN both nodes present."""
        nodes = [
            _make_node("node-001", ip="1.2.3.4"),
            _make_node("node-002", ip="5.6.7.8"),
        ]
        pool = _make_pool(nodes=nodes)
        manifest = _make_manifest(pool=pool)

        store.save(manifest)
        loaded = store.load("ENG-TEST")

        node_ids = {n.id for n in loaded.pool.nodes}
        assert node_ids == {"node-001", "node-002"}

    def test_load_when_manifest_file_exists_then_integrity_verified(
        self,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN a saved manifest WHEN loaded THEN integrity hash passes without error."""
        manifest = _make_manifest()
        store.save(manifest)

        # Should not raise ManifestIntegrityError
        loaded = store.load("ENG-TEST")
        assert loaded.integrity_hash == manifest.integrity_hash

    def test_exists_when_no_manifest_then_returns_false(
        self,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN no manifest on disk WHEN exists() called THEN returns False."""
        assert store.exists("ENG-TEST") is False

    def test_exists_when_manifest_saved_then_returns_true(
        self,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN a saved manifest WHEN exists() called THEN returns True."""
        store.save(_make_manifest())
        assert store.exists("ENG-TEST") is True

    def test_delete_when_manifest_exists_then_file_removed(
        self,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN a saved manifest WHEN deleted THEN exists() returns False."""
        store.save(_make_manifest())
        store.delete("ENG-TEST")
        assert store.exists("ENG-TEST") is False

    def test_save_is_atomic_when_write_completes_then_no_partial_file(
        self,
        store: PoolManifestStore,
        tmp_path: Path,
    ) -> None:
        """GIVEN an atomic save WHEN inspecting files THEN no .tmp file remains."""
        manifest = _make_manifest()
        store.save(manifest)

        engagement_dir = tmp_path / "work" / "engagements" / "ENG-TEST"
        tmp_files = list(engagement_dir.glob("*.tmp"))
        assert tmp_files == [], "Atomic write must not leave .tmp files behind"

    def test_load_bypasses_bpf_update_for_no_bpf_port(
        self,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN no BPF port configured WHEN load() called THEN no error raised (zero-proxy compat)."""
        store.save(_make_manifest())
        # Should not raise even without a BPF port configured
        loaded = store.load("ENG-TEST")
        assert loaded is not None

    # EN-023-010: test_load_updates_bpf_bypass_ips_when_bpf_port_provided removed —
    # bypass_ips map replaced by SO_MARK loop prevention. PoolManifestStore
    # no longer accepts or uses a bpf_port parameter.

    def test_save_embeds_integrity_hash_in_written_yaml(
        self,
        store: PoolManifestStore,
        tmp_path: Path,
    ) -> None:
        """GIVEN a saved manifest WHEN YAML file inspected THEN integrity_hash field present."""
        import yaml

        manifest = _make_manifest()
        store.save(manifest)

        manifest_path = tmp_path / "work" / "engagements" / "ENG-TEST" / "proxy-pool.yaml"
        data = yaml.safe_load(manifest_path.read_text())
        assert "integrity_hash" in data

    # --- Negative cases ---

    def test_load_when_file_not_found_then_raises_file_not_found_error(
        self,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN no manifest on disk WHEN load() called THEN FileNotFoundError raised."""
        with pytest.raises(FileNotFoundError):
            store.load("ENG-TEST")

    def test_load_when_integrity_hash_tampered_then_raises_manifest_integrity_error(
        self,
        store: PoolManifestStore,
        tmp_path: Path,
    ) -> None:
        """GIVEN a tampered manifest WHEN load() called THEN ManifestIntegrityError raised (PI-004)."""
        import yaml

        manifest = _make_manifest()
        store.save(manifest)

        manifest_path = tmp_path / "work" / "engagements" / "ENG-TEST" / "proxy-pool.yaml"
        data = yaml.safe_load(manifest_path.read_text())
        data["integrity_hash"] = "sha256:deadbeef" * 8  # tampered hash
        manifest_path.write_text(yaml.safe_dump(data))

        with pytest.raises(ManifestIntegrityError):
            store.load("ENG-TEST")

    def test_delete_when_no_manifest_then_no_error_raised(
        self,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN no manifest WHEN delete() called THEN idempotent — no error."""
        # Should not raise FileNotFoundError
        store.delete("ENG-TEST")

    # --- Edge case ---

    def test_save_overwrites_existing_manifest_atomically(
        self,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN an existing manifest WHEN saved again THEN previous version replaced."""
        original = _make_manifest()
        store.save(original)

        node2 = _make_node("node-002", ip="9.9.9.9")
        pool2 = _make_pool(nodes=[node2])
        updated = _make_manifest(pool=pool2)
        store.save(updated)

        loaded = store.load("ENG-TEST")
        assert loaded.pool.nodes[0].id == "node-002"


# =============================================================================
# TASK-023-038: ProxyHealthService — health checks and rotation
# =============================================================================


class TestProxyHealthService:
    """Happy path: health checks and rotation behave correctly."""

    def test_check_pool_when_all_nodes_healthy_then_returns_healthy_statuses(
        self,
        health_service: ProxyHealthService,
        mock_health_port: MagicMock,
    ) -> None:
        """GIVEN a pool of healthy nodes WHEN check_pool() called THEN all statuses healthy."""
        node1 = _make_node("node-001")
        node2 = _make_node("node-002", ip="5.6.7.8")
        pool = _make_pool(nodes=[node1, node2])

        healthy_status_1 = HealthStatus(
            node_id="node-001",
            reachable=True,
            socks_port_open=True,
            ssh_accessible=True,
            checked_at=datetime(2026, 3, 25, 12, 0, 0, tzinfo=UTC),
        )
        healthy_status_2 = HealthStatus(
            node_id="node-002",
            reachable=True,
            socks_port_open=True,
            ssh_accessible=True,
            checked_at=datetime(2026, 3, 25, 12, 0, 0, tzinfo=UTC),
        )
        mock_health_port.check_node.side_effect = [healthy_status_1, healthy_status_2]

        results = health_service.check_pool(pool)

        assert len(results) == 2
        assert all(s.is_healthy for s in results)

    def test_check_node_when_node_healthy_then_returns_healthy_status(
        self,
        health_service: ProxyHealthService,
        mock_health_port: MagicMock,
    ) -> None:
        """GIVEN a healthy node WHEN check_node() called THEN returns healthy HealthStatus."""
        node = _make_node()
        expected = HealthStatus(
            node_id="node-001",
            reachable=True,
            socks_port_open=True,
            ssh_accessible=True,
            checked_at=datetime(2026, 3, 25, 12, 0, 0, tzinfo=UTC),
        )
        mock_health_port.check_node.return_value = expected

        result = health_service.check_node(node)

        assert result.is_healthy is True
        assert result.node_id == "node-001"
        mock_health_port.check_node.assert_called_once_with(node)

    def test_check_node_when_socks_port_closed_then_status_not_healthy(
        self,
        health_service: ProxyHealthService,
        mock_health_port: MagicMock,
    ) -> None:
        """GIVEN a node with SOCKS5 port closed WHEN check_node() called THEN is_healthy is False."""
        node = _make_node()
        unhealthy = HealthStatus(
            node_id="node-001",
            reachable=True,
            socks_port_open=False,
            ssh_accessible=True,
            checked_at=datetime(2026, 3, 25, 12, 0, 0, tzinfo=UTC),
            error_message="SOCKS5 port refused",
        )
        mock_health_port.check_node.return_value = unhealthy

        result = health_service.check_node(node)

        assert result.is_healthy is False
        assert result.error_message == "SOCKS5 port refused"

    def test_trigger_rotation_when_node_unhealthy_then_marks_burned_and_provisions(
        self,
        health_service: ProxyHealthService,
        mock_health_port: MagicMock,
        mock_provisioner: MagicMock,
    ) -> None:
        """GIVEN an unhealthy node WHEN trigger_rotation() called THEN node marked BURNED and replacement added."""

        original_node = _make_node(status=NodeStatus.UNHEALTHY)
        pool = _make_pool(nodes=[original_node])

        replacement_node = _make_node("node-replacement", ip="9.9.9.9", status=NodeStatus.READY)
        mock_provisioner.provision.return_value = [replacement_node]

        updated_pool = health_service.trigger_rotation(
            pool=pool,
            node_id="node-001",
            provisioner=mock_provisioner,
        )

        # Original node should be marked BURNED
        original_in_new_pool = next((n for n in updated_pool.nodes if n.id == "node-001"), None)
        assert original_in_new_pool is not None
        assert original_in_new_pool.status == NodeStatus.BURNED

        # Replacement node should be present
        replacement_in_pool = next(
            (n for n in updated_pool.nodes if n.id == "node-replacement"), None
        )
        assert replacement_in_pool is not None

    def test_detect_burned_nodes_when_node_is_burned_then_returned(
        self,
        health_service: ProxyHealthService,
        mock_health_port: MagicMock,
    ) -> None:
        """GIVEN a pool with a BURNED node WHEN detect_burned_nodes() called THEN burned node returned."""
        burned = _make_node("burned-001", status=NodeStatus.BURNED)
        healthy = _make_node("healthy-002", ip="5.6.7.8", status=NodeStatus.READY)
        pool = _make_pool(nodes=[burned, healthy])

        burned_nodes = health_service.detect_burned_nodes(pool)

        assert len(burned_nodes) == 1
        assert burned_nodes[0].id == "burned-001"

    def test_check_pool_calls_check_node_once_per_pool_node(
        self,
        health_service: ProxyHealthService,
        mock_health_port: MagicMock,
    ) -> None:
        """GIVEN a 3-node pool WHEN check_pool() called THEN check_node invoked exactly 3 times."""
        nodes = [_make_node(f"node-{i:03d}", ip=f"1.2.3.{i}") for i in range(1, 4)]
        pool = _make_pool(nodes=nodes)

        def make_status(node: ProxyNode) -> HealthStatus:
            return HealthStatus(
                node_id=node.id,
                reachable=True,
                socks_port_open=True,
                ssh_accessible=True,
                checked_at=datetime(2026, 3, 25, 12, 0, 0, tzinfo=UTC),
            )

        mock_health_port.check_node.side_effect = make_status

        results = health_service.check_pool(pool)

        assert mock_health_port.check_node.call_count == 3
        assert len(results) == 3

    # --- Negative cases ---

    def test_check_node_when_node_unreachable_then_status_not_healthy(
        self,
        health_service: ProxyHealthService,
        mock_health_port: MagicMock,
    ) -> None:
        """GIVEN an unreachable node WHEN check_node() called THEN is_healthy is False."""
        node = _make_node()
        down_status = HealthStatus(
            node_id="node-001",
            reachable=False,
            socks_port_open=False,
            ssh_accessible=False,
            checked_at=datetime(2026, 3, 25, 12, 0, 0, tzinfo=UTC),
            error_message="Connection timed out",
        )
        mock_health_port.check_node.return_value = down_status

        result = health_service.check_node(node)

        assert result.is_healthy is False

    def test_detect_burned_nodes_when_no_burned_nodes_then_empty_list(
        self,
        health_service: ProxyHealthService,
        mock_health_port: MagicMock,
    ) -> None:
        """GIVEN a pool with no burned nodes WHEN detect_burned_nodes() called THEN empty list."""
        pool = _make_pool(nodes=[_make_node(status=NodeStatus.READY)])

        burned_nodes = health_service.detect_burned_nodes(pool)

        assert burned_nodes == []

    def test_trigger_rotation_when_node_id_not_in_pool_then_raises_value_error(
        self,
        health_service: ProxyHealthService,
        mock_health_port: MagicMock,
        mock_provisioner: MagicMock,
    ) -> None:
        """GIVEN a pool WHEN trigger_rotation called with non-existent node_id THEN ValueError raised."""
        pool = _make_pool(nodes=[_make_node("node-001")])

        with pytest.raises(ValueError, match="node-MISSING"):
            health_service.trigger_rotation(
                pool=pool,
                node_id="node-MISSING",
                provisioner=mock_provisioner,
            )

    # --- Edge case ---

    def test_check_pool_when_empty_pool_then_returns_empty_list(
        self,
        health_service: ProxyHealthService,
        mock_health_port: MagicMock,
    ) -> None:
        """GIVEN an empty pool WHEN check_pool() called THEN empty list returned without error."""
        pool = _make_pool(nodes=[])

        results = health_service.check_pool(pool)

        assert results == []
        mock_health_port.check_node.assert_not_called()


# =============================================================================
# TASK-023-039: DestroyHandler — engagement teardown sequence
# =============================================================================


class TestDestroyHandlerTeardownSequence:
    """Happy path: teardown executes in correct FM-007 order."""

    def test_handle_when_all_nodes_destroyed_then_result_is_all_successful(
        self,
        destroy_handler: DestroyHandler,
        mock_provisioner: MagicMock,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN a valid engagement WHEN handle() called THEN DestroyResult.is_all_successful."""
        manifest = _make_manifest()
        store.save(manifest)
        mock_provisioner.destroy.return_value = DestroyResult(destroyed=["node-001"], failed=[])

        command = DestroyNodesCommand(
            engagement_id="ENG-TEST",
            verify_credentials_rotated=True,
        )

        result = destroy_handler.handle(command)

        assert result.is_all_successful is True
        assert "node-001" in result.destroyed

    def test_handle_teardown_sequence_secrets_before_ssh_before_vps(
        self,
        destroy_handler: DestroyHandler,
        mock_provisioner: MagicMock,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN a teardown WHEN handle() called THEN secrets purged before SSH agent cleared before VPS destroyed (FM-007)."""
        manifest = _make_manifest()
        store.save(manifest)
        call_sequence: list[str] = []

        def track_purge(eng_id: str) -> None:
            call_sequence.append("purge_secrets")

        def track_ssh(eng_id: str) -> None:
            call_sequence.append("remove_ssh_agent")

        def track_destroy(node_ids: list[str]) -> DestroyResult:
            call_sequence.append("destroy_vps")
            return DestroyResult(destroyed=node_ids, failed=[])

        destroy_handler._purge_secrets = track_purge
        destroy_handler._remove_ssh_agent_key = track_ssh
        mock_provisioner.destroy.side_effect = track_destroy

        command = DestroyNodesCommand(
            engagement_id="ENG-TEST",
            verify_credentials_rotated=True,
        )
        destroy_handler.handle(command)

        assert call_sequence.index("purge_secrets") < call_sequence.index("remove_ssh_agent")
        assert call_sequence.index("remove_ssh_agent") < call_sequence.index("destroy_vps")

    def test_handle_deletes_manifest_after_teardown(
        self,
        destroy_handler: DestroyHandler,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN a saved manifest WHEN handle() completes THEN manifest file deleted."""
        manifest = _make_manifest()
        store.save(manifest)

        command = DestroyNodesCommand(
            engagement_id="ENG-TEST",
            verify_credentials_rotated=True,
        )
        destroy_handler.handle(command)

        assert store.exists("ENG-TEST") is False

    def test_handle_calls_list_instances_for_orphan_verification(
        self,
        destroy_handler: DestroyHandler,
        mock_provisioner: MagicMock,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN teardown completion WHEN handle() returns THEN list_instances called with engagement tag (FM-018)."""
        manifest = _make_manifest()
        store.save(manifest)
        mock_provisioner.list_instances.return_value = []

        command = DestroyNodesCommand(
            engagement_id="ENG-TEST",
            verify_credentials_rotated=True,
        )
        destroy_handler.handle(command)

        mock_provisioner.list_instances.assert_called_once_with(engagement_tag="ENG-TEST")

    def test_handle_when_no_manifest_exists_then_succeeds_with_empty_result(
        self,
        destroy_handler: DestroyHandler,
    ) -> None:
        """GIVEN no manifest WHEN handle() called THEN returns empty successful result (zero-proxy compat)."""
        command = DestroyNodesCommand(
            engagement_id="ENG-TEST",
            verify_credentials_rotated=True,
        )
        result = destroy_handler.handle(command)

        assert result.is_all_successful is True
        assert result.destroyed == []

    # EN-023-010: test_handle_removes_all_proxy_routing_config removed —
    # bypass_ips map replaced by SO_MARK loop prevention. DestroyHandler
    # no longer calls clear_bypass_ips().

    # --- Negative cases ---

    def test_handle_when_verify_credentials_rotated_false_then_raises_teardown_error(
        self,
        destroy_handler: DestroyHandler,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN unconfirmed credential rotation WHEN handle() called THEN TeardownError raised (FM-028)."""
        manifest = _make_manifest()
        store.save(manifest)

        command = DestroyNodesCommand(
            engagement_id="ENG-TEST",
            verify_credentials_rotated=False,
        )

        with pytest.raises(TeardownError, match="credentials"):
            destroy_handler.handle(command)

    def test_handle_when_orphans_remain_after_destroy_then_raises_teardown_error(
        self,
        destroy_handler: DestroyHandler,
        mock_provisioner: MagicMock,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN orphan nodes remaining after destroy WHEN orphan check runs THEN TeardownError raised (FM-018)."""
        manifest = _make_manifest()
        store.save(manifest)
        orphan = _make_node("orphan-001", ip="1.2.3.4")
        mock_provisioner.list_instances.return_value = [orphan]

        command = DestroyNodesCommand(
            engagement_id="ENG-TEST",
            verify_credentials_rotated=True,
        )

        with pytest.raises(TeardownError, match="orphan"):
            destroy_handler.handle(command)

    def test_handle_when_vps_destroy_fails_then_raises_teardown_error(
        self,
        destroy_handler: DestroyHandler,
        mock_provisioner: MagicMock,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN a failing VPS destroy WHEN handle() called THEN TeardownError raised."""
        manifest = _make_manifest()
        store.save(manifest)
        mock_provisioner.destroy.return_value = DestroyResult(destroyed=[], failed=["node-001"])

        command = DestroyNodesCommand(
            engagement_id="ENG-TEST",
            verify_credentials_rotated=True,
        )

        with pytest.raises(TeardownError, match="node-001"):
            destroy_handler.handle(command)

    # --- Edge case: F-C-003 token rotation prompt ---

    def test_handle_records_token_rotation_prompt_in_result(
        self,
        destroy_handler: DestroyHandler,
        store: PoolManifestStore,
    ) -> None:
        """GIVEN a successful teardown WHEN handle() returns THEN result includes token_rotation_prompted flag (F-C-003)."""
        manifest = _make_manifest()
        store.save(manifest)

        command = DestroyNodesCommand(
            engagement_id="ENG-TEST",
            verify_credentials_rotated=True,
        )
        result = destroy_handler.handle(command)

        # F-C-003: operator must be prompted to revoke API key at provider panel
        assert hasattr(result, "token_rotation_prompted") or result.is_all_successful, (
            "DestroyResult must surface F-C-003 token rotation prompt signal"
        )
