# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD test suite for proxy_infra CLI command functions.

STORY-023-003: CLI Proxy Management Commands
Tasks covered:
  - TASK-023-023: Design CLI command structure
  - TASK-023-024: Implement jerry proxy provision
  - TASK-023-025: Implement jerry proxy status/rotate/destroy
  - TASK-023-045: Implement jerry proxy gc

Covers:
  - provision_command: creates nodes via mocked adapter, runs pre-flight
  - status_command: returns node list, no pre-flight, audit entry written
  - rotate_command: provision-before-destroy (PI-003), pre-flight runs
  - destroy_command: destroys listed nodes, pre-flight runs, audit entry written
  - gc_command --dry-run: lists orphans without destroying
  - gc_command --confirm: destroys orphans, audit entry written
  - Pre-flight runs before every mutation (provision, rotate, destroy, gc --confirm)
  - Pre-flight is NOT run for read-only operations (status, gc --dry-run)
  - H-07: interface layer imports only, no infrastructure leaks into tests
  - H-10: one public class per test class (structure rule satisfied)

Test pyramid: 60% happy path / 30% negative / 10% architecture/edge cases
Naming convention: test_{scenario}_when_{condition}_then_{expected}
"""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, call, patch

import pytest

from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
from src.proxy_infra.infrastructure.persistence.audit_log_store import AuditLogStore
from src.proxy_infra.interface.cli.proxy_commands import (
    destroy_command,
    gc_command,
    provision_command,
    rotate_command,
    status_command,
)


# =============================================================================
# Shared fixtures
# =============================================================================


@pytest.fixture()
def audit_store(tmp_path: Path) -> AuditLogStore:
    """AuditLogStore writing to a temp directory."""
    return AuditLogStore(base_log_dir=tmp_path)


@pytest.fixture()
def sample_node() -> ProxyNode:
    """A READY proxy node for use in adapter mocks."""
    return ProxyNode(
        id="do-111",
        provider="digitalocean",
        ip="1.2.3.4",
        region="nyc1",
        role=ProxyRole.ACTIVE,
        proxy_type=ProxyType.DIRECT_SOCKS5,
        status=NodeStatus.READY,
        ssh_key_id="key-1",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        engagement_id="ENG-001",
    )


@pytest.fixture()
def sample_config() -> ProvisionConfig:
    """Minimal ProvisionConfig for a single node."""
    return ProvisionConfig(
        provider="digitalocean",
        region="nyc1",
        engagement_id="ENG-001",
        engagement_tag="ENG-001",
        count=1,
        role=ProxyRole.ACTIVE,
        proxy_type=ProxyType.DIRECT_SOCKS5,
        ssh_public_key="ssh-rsa AAAA...",
        operator_ip="10.0.0.1",
    )


def _make_adapter(
    nodes: list[ProxyNode] | None = None,
    destroy_result: DestroyResult | None = None,
    has_preflight: bool = False,
) -> MagicMock:
    """Build a MagicMock adapter with sensible defaults.

    Args:
        nodes: Nodes returned by list_instances() and provision().
        destroy_result: Result returned by destroy(). Defaults to all-success.
        has_preflight: When True, attach a mock pre-flight checker.

    Returns:
        Configured MagicMock adapter.
    """
    adapter = MagicMock()
    adapter.provision.return_value = nodes or []
    adapter.list_instances.return_value = nodes or []
    adapter.destroy.return_value = destroy_result or DestroyResult(
        destroyed=[n.id for n in (nodes or [])], failed=[]
    )
    if has_preflight:
        adapter._preflight = MagicMock()
    else:
        # Ensure _preflight is absent (getattr fallback returns None)
        del adapter._preflight
    return adapter


# =============================================================================
# Happy path: provision_command
# =============================================================================


@pytest.mark.unit
class TestProvisionCommand:
    """Happy-path tests for provision_command."""

    def test_provision_when_adapter_succeeds_then_returns_nodes(
        self,
        sample_config: ProvisionConfig,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """provision_command returns the list of nodes from the adapter."""
        adapter = _make_adapter(nodes=[sample_node])

        result = provision_command(sample_config, adapter, audit_store)

        assert result == [sample_node]
        adapter.provision.assert_called_once_with(sample_config)

    def test_provision_when_count_is_three_then_returns_three_nodes(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """provision_command returns all nodes when count > 1."""
        nodes = [
            ProxyNode(
                id=f"do-{i}",
                provider="digitalocean",
                ip=f"1.2.3.{i}",
                region="nyc1",
                role=ProxyRole.ACTIVE,
                proxy_type=ProxyType.DIRECT_SOCKS5,
                status=NodeStatus.CONFIGURING,
                ssh_key_id=f"key-{i}",
                created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                engagement_id="ENG-001",
            )
            for i in range(3)
        ]
        config = ProvisionConfig(
            provider="digitalocean",
            region="nyc1",
            engagement_id="ENG-001",
            engagement_tag="ENG-001",
            count=3,
            role=ProxyRole.ACTIVE,
            proxy_type=ProxyType.DIRECT_SOCKS5,
            ssh_public_key="ssh-rsa AAAA...",
            operator_ip="10.0.0.1",
        )
        adapter = _make_adapter(nodes=nodes)

        result = provision_command(config, adapter, audit_store)

        assert len(result) == 3

    def test_provision_when_called_then_audit_entry_written_per_node(
        self,
        sample_config: ProvisionConfig,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
        tmp_path: Path,
    ) -> None:
        """provision_command writes one audit entry per returned node."""
        adapter = _make_adapter(nodes=[sample_node])

        provision_command(sample_config, adapter, audit_store)

        log_path = tmp_path / "ENG-001" / "provisioner.jsonl"
        assert log_path.exists()
        entries = [json.loads(line) for line in log_path.read_text().splitlines()]
        assert len(entries) == 1
        assert entries[0]["action"] == "provision"
        assert entries[0]["resource_id"] == "do-111"

    def test_provision_when_adapter_has_preflight_then_preflight_runs(
        self,
        sample_config: ProvisionConfig,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """provision_command triggers pre-flight when the adapter has one."""
        adapter = _make_adapter(nodes=[sample_node], has_preflight=True)

        provision_command(sample_config, adapter, audit_store)

        adapter._preflight.run.assert_called_once()

    def test_provision_when_adapter_has_no_preflight_then_no_error(
        self,
        sample_config: ProvisionConfig,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """provision_command does not fail when no pre-flight checker is attached."""
        adapter = _make_adapter(nodes=[sample_node], has_preflight=False)

        # Should not raise
        result = provision_command(sample_config, adapter, audit_store)
        assert result == [sample_node]

    def test_provision_when_zero_nodes_returned_then_empty_list(
        self,
        sample_config: ProvisionConfig,
        audit_store: AuditLogStore,
    ) -> None:
        """provision_command returns [] when the adapter returns no nodes."""
        adapter = _make_adapter(nodes=[])

        result = provision_command(sample_config, adapter, audit_store)

        assert result == []


# =============================================================================
# Happy path: status_command
# =============================================================================


@pytest.mark.unit
class TestStatusCommand:
    """Happy-path tests for status_command."""

    def test_status_when_nodes_exist_then_returns_node_list(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """status_command returns all nodes for the engagement."""
        adapter = _make_adapter(nodes=[sample_node])

        result = status_command("ENG-001", adapter, audit_store)

        assert result == [sample_node]
        adapter.list_instances.assert_called_once_with("ENG-001")

    def test_status_when_no_nodes_then_returns_empty_list(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """status_command returns [] when there are no active nodes."""
        adapter = _make_adapter(nodes=[])

        result = status_command("ENG-002", adapter, audit_store)

        assert result == []

    def test_status_when_called_then_audit_entry_written(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
        tmp_path: Path,
    ) -> None:
        """status_command appends a list_instances audit entry."""
        adapter = _make_adapter(nodes=[sample_node])

        status_command("ENG-001", adapter, audit_store)

        log_path = tmp_path / "ENG-001" / "provisioner.jsonl"
        assert log_path.exists()
        entries = [json.loads(line) for line in log_path.read_text().splitlines()]
        assert any(e["action"] == "list_instances" for e in entries)

    def test_status_when_adapter_has_preflight_then_preflight_not_called(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """status_command does NOT run pre-flight — it is a read-only operation."""
        adapter = _make_adapter(nodes=[sample_node], has_preflight=True)

        status_command("ENG-001", adapter, audit_store)

        adapter._preflight.run.assert_not_called()

    def test_status_when_multiple_engagements_exist_then_filters_by_id(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """status_command passes the engagement_id to list_instances (not empty)."""
        adapter = _make_adapter(nodes=[])

        status_command("ENG-SPECIFIC", adapter, audit_store)

        adapter.list_instances.assert_called_once_with("ENG-SPECIFIC")


# =============================================================================
# Happy path: rotate_command
# =============================================================================


@pytest.mark.unit
class TestRotateCommand:
    """Happy-path tests for rotate_command."""

    def test_rotate_when_config_provided_then_provisions_before_destroy(
        self,
        sample_config: ProvisionConfig,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """rotate_command provisions a replacement before destroying the original (PI-003)."""
        replacement = ProxyNode(
            id="do-999",
            provider="digitalocean",
            ip="5.6.7.8",
            region="nyc1",
            role=ProxyRole.ACTIVE,
            proxy_type=ProxyType.DIRECT_SOCKS5,
            status=NodeStatus.CONFIGURING,
            ssh_key_id="key-new",
            created_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
            engagement_id="ENG-001",
        )
        adapter = _make_adapter(nodes=[replacement], has_preflight=True)
        adapter.destroy.return_value = DestroyResult(destroyed=["do-111"], failed=[])

        result = rotate_command("ENG-001", "do-111", adapter, audit_store, config=sample_config)

        # Provision must be called before destroy (PI-003 ordering)
        provision_call_index = [str(c) for c in adapter.mock_calls].index(
            str(call.provision(sample_config))
        )
        destroy_call_index = [str(c) for c in adapter.mock_calls].index(
            str(call.destroy(["do-111"]))
        )
        assert provision_call_index < destroy_call_index
        assert result.id == "do-999"

    def test_rotate_when_config_provided_then_preflight_runs(
        self,
        sample_config: ProvisionConfig,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """rotate_command triggers pre-flight before any mutating operation."""
        adapter = _make_adapter(nodes=[sample_node], has_preflight=True)

        rotate_command("ENG-001", "do-111", adapter, audit_store, config=sample_config)

        adapter._preflight.run.assert_called_once()

    def test_rotate_when_no_config_then_only_destroys_and_returns_sentinel(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """rotate_command without config destroys the node and returns a sentinel ProxyNode."""
        adapter = _make_adapter(nodes=[], has_preflight=False)
        adapter.destroy.return_value = DestroyResult(destroyed=["do-111"], failed=[])

        result = rotate_command("ENG-001", "do-111", adapter, audit_store, config=None)

        adapter.provision.assert_not_called()
        adapter.destroy.assert_called_once_with(["do-111"])
        assert result.id == "do-111"
        assert result.status == NodeStatus.DESTROYED

    def test_rotate_when_called_then_audit_entry_written(
        self,
        sample_config: ProvisionConfig,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
        tmp_path: Path,
    ) -> None:
        """rotate_command writes audit entries for both provision and rotate."""
        adapter = _make_adapter(nodes=[sample_node], has_preflight=False)
        adapter.destroy.return_value = DestroyResult(destroyed=["do-111"], failed=[])

        rotate_command("ENG-001", "do-111", adapter, audit_store, config=sample_config)

        log_path = tmp_path / "ENG-001" / "provisioner.jsonl"
        assert log_path.exists()
        entries = [json.loads(line) for line in log_path.read_text().splitlines()]
        actions = {e["action"] for e in entries}
        assert "provision" in actions
        assert "rotate" in actions


# =============================================================================
# Happy path: destroy_command
# =============================================================================


@pytest.mark.unit
class TestDestroyCommand:
    """Happy-path tests for destroy_command."""

    def test_destroy_when_node_ids_provided_then_destroys_only_those_nodes(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """destroy_command destroys only the specified node IDs."""
        adapter = _make_adapter(nodes=[sample_node])
        adapter.destroy.return_value = DestroyResult(destroyed=["do-111"], failed=[])

        result = destroy_command("ENG-001", adapter, audit_store, node_ids=["do-111"])

        adapter.destroy.assert_called_once_with(["do-111"])
        assert result.destroyed == ["do-111"]
        assert result.failed == []

    def test_destroy_when_no_node_ids_then_queries_and_destroys_all(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """destroy_command with no node_ids discovers and destroys all nodes."""
        adapter = _make_adapter(nodes=[sample_node])
        adapter.destroy.return_value = DestroyResult(destroyed=["do-111"], failed=[])

        result = destroy_command("ENG-001", adapter, audit_store, node_ids=None)

        adapter.list_instances.assert_called_once_with("ENG-001")
        adapter.destroy.assert_called_once_with(["do-111"])
        assert result.is_all_successful

    def test_destroy_when_no_nodes_found_then_returns_empty_result(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """destroy_command returns empty DestroyResult when there are no nodes."""
        adapter = _make_adapter(nodes=[])

        result = destroy_command("ENG-001", adapter, audit_store)

        adapter.destroy.assert_not_called()
        assert result.destroyed == []
        assert result.failed == []

    def test_destroy_when_called_then_preflight_runs(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """destroy_command triggers pre-flight before destroying."""
        adapter = _make_adapter(nodes=[sample_node], has_preflight=True)
        adapter.destroy.return_value = DestroyResult(destroyed=["do-111"], failed=[])

        destroy_command("ENG-001", adapter, audit_store, node_ids=["do-111"])

        adapter._preflight.run.assert_called_once()

    def test_destroy_when_called_then_audit_entry_written(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
        tmp_path: Path,
    ) -> None:
        """destroy_command appends a destroy audit entry."""
        adapter = _make_adapter(nodes=[sample_node])
        adapter.destroy.return_value = DestroyResult(destroyed=["do-111"], failed=[])

        destroy_command("ENG-001", adapter, audit_store, node_ids=["do-111"])

        log_path = tmp_path / "ENG-001" / "provisioner.jsonl"
        entries = [json.loads(line) for line in log_path.read_text().splitlines()]
        assert any(e["action"] == "destroy" for e in entries)

    def test_destroy_when_partial_failure_then_result_reflects_failures(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """destroy_command preserves partial failure information from the adapter."""
        adapter = _make_adapter(nodes=[])
        adapter.destroy.return_value = DestroyResult(
            destroyed=["do-111"], failed=["do-222"]
        )

        result = destroy_command("ENG-001", adapter, audit_store, node_ids=["do-111", "do-222"])

        assert result.destroyed == ["do-111"]
        assert result.failed == ["do-222"]
        assert not result.is_all_successful


# =============================================================================
# Happy path: gc_command (dry-run and confirm)
# =============================================================================


@pytest.mark.unit
class TestGcCommandDryRun:
    """Happy-path tests for gc_command in dry-run mode."""

    def test_gc_dry_run_when_orphans_exist_then_returns_orphan_ids(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """gc_command --dry-run returns the list of orphaned node IDs."""
        adapter = _make_adapter(nodes=[sample_node])

        result = gc_command("ENG-001", adapter, audit_store, dry_run=True)

        assert result == ["do-111"]

    def test_gc_dry_run_when_no_orphans_then_returns_empty_list(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """gc_command --dry-run returns [] when no orphans are found."""
        adapter = _make_adapter(nodes=[])

        result = gc_command("ENG-001", adapter, audit_store, dry_run=True)

        assert result == []

    def test_gc_dry_run_when_called_then_no_resources_destroyed(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """gc_command --dry-run never calls adapter.destroy()."""
        adapter = _make_adapter(nodes=[sample_node])

        gc_command("ENG-001", adapter, audit_store, dry_run=True)

        adapter.destroy.assert_not_called()

    def test_gc_dry_run_when_called_then_preflight_not_run(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """gc_command --dry-run does not trigger pre-flight (read-only operation)."""
        adapter = _make_adapter(nodes=[sample_node], has_preflight=True)

        gc_command("ENG-001", adapter, audit_store, dry_run=True)

        adapter._preflight.run.assert_not_called()

    def test_gc_dry_run_when_called_then_audit_entry_written(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
        tmp_path: Path,
    ) -> None:
        """gc_command --dry-run appends a list_instances audit entry."""
        adapter = _make_adapter(nodes=[sample_node])

        gc_command("ENG-001", adapter, audit_store, dry_run=True)

        log_path = tmp_path / "ENG-001" / "provisioner.jsonl"
        assert log_path.exists()

    def test_gc_dry_run_when_multiple_orphans_then_all_returned(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """gc_command --dry-run returns all orphan IDs when multiple nodes exist."""
        nodes = [
            ProxyNode(
                id=f"do-{i}",
                provider="digitalocean",
                ip=f"1.2.3.{i}",
                region="nyc1",
                role=ProxyRole.ACTIVE,
                proxy_type=ProxyType.DIRECT_SOCKS5,
                status=NodeStatus.READY,
                ssh_key_id=f"key-{i}",
                created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                engagement_id="ENG-CRASHED",
            )
            for i in range(3)
        ]
        adapter = _make_adapter(nodes=nodes)

        result = gc_command("ENG-CRASHED", adapter, audit_store, dry_run=True)

        assert result == ["do-0", "do-1", "do-2"]


@pytest.mark.unit
class TestGcCommandConfirm:
    """Happy-path tests for gc_command in confirm (destructive) mode."""

    def test_gc_confirm_when_orphans_exist_then_destroys_them(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """gc_command --confirm calls adapter.destroy() with all orphan IDs."""
        adapter = _make_adapter(nodes=[sample_node], has_preflight=False)
        adapter.destroy.return_value = DestroyResult(destroyed=["do-111"], failed=[])

        result = gc_command("ENG-001", adapter, audit_store, dry_run=False)

        adapter.destroy.assert_called_once_with(["do-111"])
        assert result == ["do-111"]

    def test_gc_confirm_when_no_orphans_then_destroy_not_called(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """gc_command --confirm does not call destroy when there are no orphans."""
        adapter = _make_adapter(nodes=[])

        gc_command("ENG-001", adapter, audit_store, dry_run=False)

        adapter.destroy.assert_not_called()

    def test_gc_confirm_when_called_then_preflight_runs(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """gc_command --confirm triggers pre-flight (Zone 3 approval gate)."""
        adapter = _make_adapter(nodes=[sample_node], has_preflight=True)
        adapter.destroy.return_value = DestroyResult(destroyed=["do-111"], failed=[])

        gc_command("ENG-001", adapter, audit_store, dry_run=False)

        adapter._preflight.run.assert_called_once()

    def test_gc_confirm_when_called_then_audit_entry_written(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
        tmp_path: Path,
    ) -> None:
        """gc_command --confirm appends a destroy audit entry."""
        adapter = _make_adapter(nodes=[sample_node], has_preflight=False)
        adapter.destroy.return_value = DestroyResult(destroyed=["do-111"], failed=[])

        gc_command("ENG-001", adapter, audit_store, dry_run=False)

        log_path = tmp_path / "ENG-001" / "provisioner.jsonl"
        entries = [json.loads(line) for line in log_path.read_text().splitlines()]
        assert any(e["action"] == "destroy" for e in entries)

    def test_gc_confirm_when_called_then_returns_destroyed_ids(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """gc_command --confirm returns the list of IDs that were destroyed."""
        nodes = [
            ProxyNode(
                id="do-a",
                provider="digitalocean",
                ip="9.9.9.1",
                region="ams1",
                role=ProxyRole.RECON,
                proxy_type=ProxyType.SSH_TUNNEL,
                status=NodeStatus.READY,
                ssh_key_id="k1",
                created_at=datetime(2026, 2, 1, tzinfo=timezone.utc),
                engagement_id="ENG-002",
            ),
            ProxyNode(
                id="do-b",
                provider="digitalocean",
                ip="9.9.9.2",
                region="ams1",
                role=ProxyRole.RECON,
                proxy_type=ProxyType.SSH_TUNNEL,
                status=NodeStatus.READY,
                ssh_key_id="k2",
                created_at=datetime(2026, 2, 1, tzinfo=timezone.utc),
                engagement_id="ENG-002",
            ),
        ]
        adapter = _make_adapter(nodes=nodes, has_preflight=False)
        adapter.destroy.return_value = DestroyResult(destroyed=["do-a", "do-b"], failed=[])

        result = gc_command("ENG-002", adapter, audit_store, dry_run=False)

        assert set(result) == {"do-a", "do-b"}


# =============================================================================
# Negative cases: pre-flight propagates exceptions
# =============================================================================


@pytest.mark.unit
class TestPreflightPropagation:
    """Tests that pre-flight failures are propagated to the caller."""

    def test_provision_when_preflight_raises_then_provision_not_called(
        self,
        sample_config: ProvisionConfig,
        audit_store: AuditLogStore,
    ) -> None:
        """provision_command does not call adapter.provision() when pre-flight fails."""
        from src.proxy_infra.domain.exceptions.api_key_expired_error import ApiKeyExpiredError

        adapter = _make_adapter(nodes=[], has_preflight=True)
        adapter._preflight.run.side_effect = ApiKeyExpiredError(
            provider="digitalocean", detail="token revoked"
        )

        with pytest.raises(ApiKeyExpiredError):
            provision_command(sample_config, adapter, audit_store)

        adapter.provision.assert_not_called()

    def test_destroy_when_preflight_raises_then_destroy_not_called(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """destroy_command does not call adapter.destroy() when pre-flight fails."""
        from src.proxy_infra.domain.exceptions.api_key_permission_error import (
            ApiKeyPermissionError,
        )

        adapter = _make_adapter(nodes=[], has_preflight=True)
        adapter._preflight.run.side_effect = ApiKeyPermissionError(
            provider="digitalocean", detail="insufficient scope"
        )

        with pytest.raises(ApiKeyPermissionError):
            destroy_command("ENG-001", adapter, audit_store, node_ids=["do-111"])

        adapter.destroy.assert_not_called()

    def test_gc_confirm_when_preflight_raises_then_destroy_not_called(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """gc_command --confirm does not destroy when pre-flight fails."""
        from src.proxy_infra.domain.exceptions.api_key_expired_error import ApiKeyExpiredError

        adapter = _make_adapter(nodes=[sample_node], has_preflight=True)
        adapter._preflight.run.side_effect = ApiKeyExpiredError(
            provider="digitalocean", detail="expired"
        )

        with pytest.raises(ApiKeyExpiredError):
            gc_command("ENG-001", adapter, audit_store, dry_run=False)

        adapter.destroy.assert_not_called()

    def test_rotate_when_preflight_raises_then_provision_not_called(
        self,
        sample_config: ProvisionConfig,
        audit_store: AuditLogStore,
    ) -> None:
        """rotate_command does not provision when pre-flight fails."""
        from src.proxy_infra.domain.exceptions.api_key_expired_error import ApiKeyExpiredError

        adapter = _make_adapter(nodes=[], has_preflight=True)
        adapter._preflight.run.side_effect = ApiKeyExpiredError(
            provider="digitalocean", detail="expired"
        )

        with pytest.raises(ApiKeyExpiredError):
            rotate_command("ENG-001", "do-111", adapter, audit_store, config=sample_config)

        adapter.provision.assert_not_called()


# =============================================================================
# Negative cases: adapter failures
# =============================================================================


@pytest.mark.unit
class TestAdapterFailurePropagation:
    """Tests that adapter errors are not silently swallowed."""

    def test_provision_when_adapter_raises_then_exception_propagates(
        self,
        sample_config: ProvisionConfig,
        audit_store: AuditLogStore,
    ) -> None:
        """provision_command propagates ProvisionError from the adapter."""
        from src.proxy_infra.domain.exceptions.provision_error import ProvisionError

        adapter = _make_adapter(nodes=[])
        adapter.provision.side_effect = ProvisionError("droplet creation failed")

        with pytest.raises(ProvisionError, match="droplet creation failed"):
            provision_command(sample_config, adapter, audit_store)

    def test_destroy_when_adapter_raises_then_exception_propagates(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """destroy_command propagates unexpected adapter exceptions."""
        adapter = _make_adapter(nodes=[])
        adapter.destroy.side_effect = RuntimeError("API unavailable")

        with pytest.raises(RuntimeError, match="API unavailable"):
            destroy_command("ENG-001", adapter, audit_store, node_ids=["do-111"])

    def test_status_when_list_instances_raises_then_exception_propagates(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """status_command propagates adapter exceptions for list_instances."""
        adapter = _make_adapter(nodes=[])
        adapter.list_instances.side_effect = RuntimeError("network error")

        with pytest.raises(RuntimeError, match="network error"):
            status_command("ENG-001", adapter, audit_store)


# =============================================================================
# Architecture / edge cases
# =============================================================================


@pytest.mark.unit
class TestCliCommandArchitecture:
    """Architecture and edge-case tests for the CLI command layer."""

    def test_proxy_commands_module_importable_from_interface_layer(self) -> None:
        """The proxy_commands module is reachable via the interface.cli path (H-07)."""
        import importlib

        mod = importlib.import_module("src.proxy_infra.interface.cli.proxy_commands")
        assert hasattr(mod, "provision_command")
        assert hasattr(mod, "status_command")
        assert hasattr(mod, "rotate_command")
        assert hasattr(mod, "destroy_command")
        assert hasattr(mod, "gc_command")

    def test_proxy_commands_module_does_not_import_pydo(self) -> None:
        """proxy_commands.py must not import pydo or other infra SDK packages."""
        import importlib
        import sys

        # Remove from cache to get a clean import graph
        key = "src.proxy_infra.interface.cli.proxy_commands"
        sys.modules.pop(key, None)

        mod = importlib.import_module(key)
        src = importlib.util.find_spec(key)
        if src and src.origin:
            module_text = Path(src.origin).read_text()
            assert "import pydo" not in module_text
            assert "from pydo" not in module_text

    def test_provision_command_function_has_type_annotations(self) -> None:
        """provision_command has complete return type annotation (H-11)."""
        import inspect
        from src.proxy_infra.interface.cli.proxy_commands import provision_command as fn

        hints = fn.__annotations__
        assert "return" in hints

    def test_gc_dry_run_uses_engagement_tag_filter_not_global_list(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """gc_command calls list_instances(tag), never list_nodes() (ISOLATION-002)."""
        adapter = _make_adapter(nodes=[sample_node])

        gc_command("ENG-001", adapter, audit_store, dry_run=True)

        adapter.list_nodes.assert_not_called()
        adapter.list_instances.assert_called_once_with("ENG-001")

    def test_gc_confirm_uses_engagement_tag_filter_not_global_list(
        self,
        sample_node: ProxyNode,
        audit_store: AuditLogStore,
    ) -> None:
        """gc_command --confirm calls list_instances(tag), never list_nodes() (ISOLATION-002)."""
        adapter = _make_adapter(nodes=[sample_node])
        adapter.destroy.return_value = DestroyResult(destroyed=["do-111"], failed=[])

        gc_command("ENG-001", adapter, audit_store, dry_run=False)

        adapter.list_nodes.assert_not_called()

    def test_destroy_with_empty_node_ids_list_calls_list_instances(
        self,
        audit_store: AuditLogStore,
    ) -> None:
        """destroy_command with empty list resolves via list_instances, not list_nodes."""
        adapter = _make_adapter(nodes=[])

        destroy_command("ENG-001", adapter, audit_store, node_ids=[])

        adapter.list_instances.assert_called_once_with("ENG-001")
        adapter.list_nodes.assert_not_called()
