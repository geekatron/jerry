# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Unit tests for ContainerLifecycleManager.

Tests CLM-001 (Docker reality check), CLM-002 (worktree isolation),
CLM-003 (safe teardown), and CLM-005 (volume cleanup).
Uses a mock adapter to avoid real Docker calls.

Naming: test_{scenario}_when_{condition}_then_{expected}
Distribution: 60% happy / 30% negative / 10% edge
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import yaml

from src.tool_exec.infrastructure.container_lifecycle.cluster_state import ClusterState
from src.tool_exec.infrastructure.container_lifecycle.container_lifecycle_manager import (
    ContainerLifecycleManager,
)
from src.tool_exec.infrastructure.container_lifecycle.docker_compose_adapter import (
    DockerComposeAdapter,
)
from src.tool_exec.infrastructure.container_lifecycle.service_status import ServiceStatus
from src.tool_exec.infrastructure.container_lifecycle.session_state import SessionState


@pytest.fixture()
def project_root(tmp_path: Path) -> Path:
    """Create a temp project root with tool-exec.yaml."""
    config_dir = tmp_path / "skills" / "rainbow" / "config"
    config_dir.mkdir(parents=True)
    config = {
        "container": {"health_check_timeout": 5},
        "zone_compose_files": {
            "rainbow-supply-chain": "skills/rainbow-supply-chain/tests/docker/docker-compose.yml",
            "blue-team": "skills/blue-team/tests/docker/docker-compose.yml",
            "rainbow-exploit": "skills/rainbow-exploit/tests/docker/docker-compose.yml",
        },
    }
    (config_dir / "tool-exec.yaml").write_text(yaml.dump(config))
    (tmp_path / "work").mkdir()
    return tmp_path


@pytest.fixture()
def mock_adapter() -> MagicMock:
    """Create a mock DockerComposeAdapter."""
    adapter = MagicMock(spec=DockerComposeAdapter)
    adapter.is_docker_available.return_value = True
    adapter.project_name = "rainbow-test1234"
    return adapter


@pytest.fixture()
def clm(project_root: Path, mock_adapter: MagicMock) -> ContainerLifecycleManager:
    """Create a CLM with mock adapter."""
    return ContainerLifecycleManager(
        project_root=project_root,
        adapter=mock_adapter,
    )


def _running_services(*names: str) -> list[ServiceStatus]:
    """Helper: create a list of running ServiceStatus objects."""
    return [ServiceStatus(name=n, state="running", health="healthy") for n in names]


# =============================================================================
# Happy path (60%)
# =============================================================================


class TestEnsureClustersHappyPath:
    """ensure_clusters_running — normal operations."""

    def test_ensure_clusters_when_docker_confirms_running_then_skips_startup(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """CLM-001: If Docker says running, skip build/up."""
        mock_adapter.get_running_services.return_value = _running_services("scanner")

        results = clm.ensure_clusters_running(["rainbow-supply-chain"])

        assert results[0].state == ClusterState.RUNNING
        mock_adapter.compose_build.assert_not_called()
        mock_adapter.compose_up.assert_not_called()

    def test_ensure_clusters_when_not_running_then_builds_and_starts(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """Normal startup: build, up, wait for health."""
        mock_adapter.get_running_services.side_effect = [
            [],  # verify: not running
            _running_services("scanner"),  # post-start services
            _running_services("scanner"),  # final check
        ]
        mock_adapter.wait_for_health.return_value = True

        results = clm.ensure_clusters_running(["rainbow-supply-chain"])

        assert results[0].state == ClusterState.RUNNING
        mock_adapter.compose_build.assert_called_once()
        mock_adapter.compose_up.assert_called_once()

    def test_ensure_clusters_when_multiple_requested_then_all_started(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """Multiple clusters requested — each gets started independently."""
        mock_adapter.get_running_services.side_effect = [
            [],  # supply-chain verify
            _running_services("scanner"),  # supply-chain post-start
            _running_services("scanner"),  # supply-chain final
            [],  # blue-team verify
            _running_services("detection"),  # blue-team post-start
            _running_services("detection"),  # blue-team final
        ]
        mock_adapter.wait_for_health.return_value = True

        results = clm.ensure_clusters_running(["rainbow-supply-chain", "blue-team"])

        assert len(results) == 2
        assert all(r.state == ClusterState.RUNNING for r in results)
        assert mock_adapter.compose_build.call_count == 2

    def test_ensure_clusters_when_started_then_persists_state_file(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock, project_root: Path
    ) -> None:
        """Session state file is written after startup."""
        mock_adapter.get_running_services.side_effect = [
            [],
            _running_services("scanner"),
            _running_services("scanner"),
        ]
        mock_adapter.wait_for_health.return_value = True

        clm.ensure_clusters_running(["rainbow-supply-chain"])

        state_files = list((project_root / "work").glob(".rainbow-session-state-*"))
        assert len(state_files) == 1

    def test_ensure_clusters_when_already_running_then_returns_current_services(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """Already-running cluster returns its service list."""
        services = _running_services("scanner", "envoy-z1")
        mock_adapter.get_running_services.return_value = services

        results = clm.ensure_clusters_running(["rainbow-supply-chain"])

        assert len(results[0].services) == 2
        assert results[0].services[0].name == "scanner"

    def test_ensure_clusters_when_custom_timeout_then_passes_to_health_check(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """Custom health_check_timeout is forwarded to wait_for_health."""
        mock_adapter.get_running_services.side_effect = [
            [],
            _running_services("scanner"),
            _running_services("scanner"),
        ]
        mock_adapter.wait_for_health.return_value = True

        clm.ensure_clusters_running(["rainbow-supply-chain"], health_check_timeout=60)

        _, kwargs = mock_adapter.wait_for_health.call_args
        assert kwargs["max_wait"] == 60


class TestTeardownHappyPath:
    """teardown — normal operations."""

    def test_teardown_when_all_down_then_deletes_state_file(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """CLM-003: State file deleted after Docker confirms zero containers."""
        # Setup: start a cluster to create state
        mock_adapter.get_running_services.side_effect = [
            [],
            _running_services("scanner"),
            _running_services("scanner"),
        ]
        mock_adapter.wait_for_health.return_value = True
        clm.ensure_clusters_running(["rainbow-supply-chain"])

        # Teardown: compose down succeeds, verify shows zero
        mock_adapter.get_running_services.side_effect = [
            [],  # post-down verify
        ]
        mock_adapter.list_project_volumes.return_value = []

        result = clm.teardown()

        assert result.state_file_deleted is True
        assert "rainbow-supply-chain" in result.clusters_torn_down
        assert result.errors == []

    def test_teardown_when_volumes_exist_then_removes_and_reports(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """CLM-005: Volumes removed during teardown."""
        mock_adapter.get_running_services.side_effect = [
            [],
            _running_services("scanner"),
            _running_services("scanner"),
        ]
        mock_adapter.wait_for_health.return_value = True
        clm.ensure_clusters_running(["rainbow-supply-chain"])

        mock_adapter.get_running_services.side_effect = [
            [],
        ]
        mock_adapter.list_project_volumes.return_value = ["rainbow-test_pgdata"]
        mock_adapter.remove_volumes.return_value = ["rainbow-test_pgdata"]

        result = clm.teardown()

        assert "rainbow-test_pgdata" in result.volumes_removed


class TestWorktreeIsolationInCLM:
    """CLM-002: Worktree isolation via compose project name."""

    def test_clm_when_created_then_project_name_is_worktree_specific(
        self, clm: ContainerLifecycleManager
    ) -> None:
        """Compose project name has worktree hash, not bare 'rainbow'."""
        assert clm.compose_project_name.startswith("rainbow-")
        assert clm.compose_project_name != "rainbow"

    def test_clm_when_different_roots_then_different_project_names(self, tmp_path: Path) -> None:
        """Two CLMs with different roots get different project names."""
        root_a, root_b = tmp_path / "a", tmp_path / "b"
        for root in (root_a, root_b):
            cfg = root / "skills" / "rainbow" / "config"
            cfg.mkdir(parents=True)
            (cfg / "tool-exec.yaml").write_text(yaml.dump({"zone_compose_files": {}}))

        clm_a = ContainerLifecycleManager(project_root=root_a)
        clm_b = ContainerLifecycleManager(project_root=root_b)
        assert clm_a.compose_project_name != clm_b.compose_project_name


class TestSessionStateHappyPath:
    """Session state serialization."""

    def test_session_state_when_round_tripped_then_preserves_all_fields(self) -> None:
        """SessionState survives to_dict -> from_dict round trip."""
        original = SessionState(
            pid=12345,
            compose_project_name="rainbow-abc12345",
            clusters={"supply-chain": "running"},
            engagement_id="RBW-0001",
            created_at=1234567890.0,
        )
        restored = SessionState.from_dict(original.to_dict())

        assert restored.pid == original.pid
        assert restored.compose_project_name == original.compose_project_name
        assert restored.clusters == original.clusters
        assert restored.engagement_id == original.engagement_id
        assert restored.created_at == original.created_at

    def test_session_state_when_defaults_used_then_has_empty_clusters(self) -> None:
        """Default SessionState has empty clusters and no engagement."""
        state = SessionState(pid=1, compose_project_name="rainbow-x")
        assert state.clusters == {}
        assert state.engagement_id is None
        assert state.created_at == 0.0

    def test_session_state_when_from_dict_with_missing_keys_then_uses_defaults(
        self,
    ) -> None:
        """from_dict handles partial data gracefully."""
        state = SessionState.from_dict({"pid": 999})
        assert state.pid == 999
        assert state.compose_project_name == ""
        assert state.clusters == {}


class TestConfigLoadingHappyPath:
    """Config loading from tool-exec.yaml."""

    def test_clm_when_config_loaded_then_returns_compose_files(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """CLM reads zone_compose_files from config correctly."""
        mock_adapter.is_docker_available.return_value = True
        mock_adapter.get_running_services.return_value = _running_services("scanner")

        # If it resolves the cluster name, config was loaded
        results = clm.ensure_clusters_running(["rainbow-supply-chain"])
        assert (
            results[0].compose_file == "skills/rainbow-supply-chain/tests/docker/docker-compose.yml"
        )


# =============================================================================
# Negative (30%)
# =============================================================================


class TestEnsureClustersNegative:
    """ensure_clusters_running — failure cases."""

    def test_ensure_clusters_when_docker_unavailable_then_returns_error(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """ERROR state when Docker daemon is unreachable."""
        mock_adapter.is_docker_available.return_value = False

        results = clm.ensure_clusters_running(["rainbow-supply-chain"])

        assert results[0].state == ClusterState.ERROR
        assert "not available" in results[0].error

    def test_ensure_clusters_when_unknown_cluster_then_returns_error(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """ERROR state for cluster name not in config."""
        results = clm.ensure_clusters_running(["nonexistent-cluster"])

        assert results[0].state == ClusterState.ERROR
        assert "Unknown cluster" in results[0].error

    def test_ensure_clusters_when_docker_says_exited_then_restarts(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """CLM-001: Containers exited — restart them."""
        mock_adapter.get_running_services.side_effect = [
            [ServiceStatus(name="scanner", state="exited", health="none")],  # verify
            _running_services("scanner"),  # post-start
            _running_services("scanner"),  # final
        ]
        mock_adapter.wait_for_health.return_value = True

        results = clm.ensure_clusters_running(["rainbow-supply-chain"])

        assert results[0].state == ClusterState.RUNNING
        mock_adapter.compose_build.assert_called_once()

    def test_ensure_clusters_when_build_fails_then_returns_error(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """CalledProcessError during build returns ERROR."""
        mock_adapter.get_running_services.return_value = []
        mock_adapter.compose_build.side_effect = subprocess.CalledProcessError(1, "docker")

        results = clm.ensure_clusters_running(["rainbow-supply-chain"])

        assert results[0].state == ClusterState.ERROR
        assert "Failed to start" in results[0].error

    def test_ensure_clusters_when_startup_times_out_then_returns_error(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """TimeoutExpired during startup returns ERROR."""
        mock_adapter.get_running_services.return_value = []
        mock_adapter.compose_build.side_effect = subprocess.TimeoutExpired("docker", 600)

        results = clm.ensure_clusters_running(["rainbow-supply-chain"])

        assert results[0].state == ClusterState.ERROR
        assert "timed out" in results[0].error

    def test_ensure_clusters_when_health_check_fails_then_returns_unhealthy(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """Services that never become healthy produce UNHEALTHY state."""
        mock_adapter.get_running_services.side_effect = [
            [],
            [ServiceStatus(name="scanner", state="running", health="starting")],
            [ServiceStatus(name="scanner", state="running", health="unhealthy")],
        ]
        mock_adapter.wait_for_health.return_value = False

        results = clm.ensure_clusters_running(["rainbow-supply-chain"], health_check_timeout=1)

        assert results[0].state == ClusterState.UNHEALTHY


class TestTeardownNegative:
    """teardown — failure cases."""

    def test_teardown_when_containers_still_running_then_keeps_state_file(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """CLM-003: State file preserved when Docker shows containers still up."""
        mock_adapter.get_running_services.side_effect = [
            [],
            _running_services("scanner"),
            _running_services("scanner"),
        ]
        mock_adapter.wait_for_health.return_value = True
        clm.ensure_clusters_running(["rainbow-supply-chain"])

        mock_adapter.get_running_services.side_effect = [
            _running_services("scanner"),  # still running after down!
        ]
        mock_adapter.list_project_volumes.return_value = []

        result = clm.teardown()

        assert result.state_file_deleted is False
        assert any("CLM-003" in e for e in result.errors)

    def test_teardown_when_compose_down_raises_then_keeps_state_file(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """State file preserved when compose down fails."""
        mock_adapter.get_running_services.side_effect = [
            [],
            _running_services("scanner"),
            _running_services("scanner"),
        ]
        mock_adapter.wait_for_health.return_value = True
        clm.ensure_clusters_running(["rainbow-supply-chain"])

        mock_adapter.compose_down.side_effect = subprocess.CalledProcessError(1, "docker")
        mock_adapter.list_project_volumes.return_value = []

        result = clm.teardown()

        assert result.state_file_deleted is False
        assert any("compose down failed" in e for e in result.errors)

    def test_teardown_when_volume_removal_fails_then_reports_clm005_error(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """CLM-005: Failed volume removal is reported."""
        mock_adapter.get_running_services.side_effect = [
            [],
            _running_services("scanner"),
            _running_services("scanner"),
        ]
        mock_adapter.wait_for_health.return_value = True
        clm.ensure_clusters_running(["rainbow-supply-chain"])

        mock_adapter.get_running_services.side_effect = [
            [],
        ]
        mock_adapter.list_project_volumes.return_value = ["stuck-vol"]
        mock_adapter.remove_volumes.return_value = []

        result = clm.teardown()

        assert any("CLM-005" in e for e in result.errors)


# =============================================================================
# Edge (10%)
# =============================================================================


class TestEnsureClustersEdge:
    """ensure_clusters_running — edge cases."""

    def test_ensure_clusters_when_empty_list_then_returns_empty(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """Empty cluster list produces empty result."""
        results = clm.ensure_clusters_running([])
        assert results == []

    def test_ensure_clusters_when_compose_down_timeout_then_keeps_state(
        self, clm: ContainerLifecycleManager, mock_adapter: MagicMock
    ) -> None:
        """Timeout during compose down keeps state file for retry."""
        mock_adapter.get_running_services.side_effect = [
            [],
            _running_services("scanner"),
            _running_services("scanner"),
        ]
        mock_adapter.wait_for_health.return_value = True
        clm.ensure_clusters_running(["rainbow-supply-chain"])

        mock_adapter.compose_down.side_effect = subprocess.TimeoutExpired("docker", 60)
        mock_adapter.list_project_volumes.return_value = []

        result = clm.teardown()

        assert result.state_file_deleted is False
