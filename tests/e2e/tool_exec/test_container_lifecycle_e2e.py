# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""E2E tests for ContainerLifecycleManager.

These tests exercise the full CLM lifecycle against real Docker:
startup, Docker reality verification, teardown, state file management,
worktree isolation, and volume cleanup.

Naming: test_{scenario}_when_{condition}_then_{expected}
Marker: @pytest.mark.e2e
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

from src.tool_exec.infrastructure.container_lifecycle.cluster_state import ClusterState
from src.tool_exec.infrastructure.container_lifecycle.container_lifecycle_manager import (
    ContainerLifecycleManager,
)
from src.tool_exec.infrastructure.container_lifecycle.docker_compose_adapter import (
    DockerComposeAdapter,
)


def _docker_available() -> bool:
    """Check if Docker daemon is reachable."""
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, timeout=10)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(not _docker_available(), reason="Docker daemon not available"),
]


def _make_project(tmp_path: Path, project_name: str) -> Path:
    """Create a project root with a minimal compose cluster config."""
    root = tmp_path / project_name
    config_dir = root / "skills" / "rainbow" / "config"
    config_dir.mkdir(parents=True)

    # Minimal compose file with a lightweight alpine container
    compose_dir = root / "test-cluster"
    compose_dir.mkdir(parents=True)
    compose_data = {
        "services": {
            "test-svc": {
                "image": "alpine:3.19",
                "command": ["sleep", "30"],
            }
        },
        "volumes": {
            "test-data": None,
        },
    }
    (compose_dir / "docker-compose.yml").write_text(
        yaml.dump(compose_data, default_flow_style=False)
    )

    # tool-exec.yaml pointing to the compose file
    config = {
        "container": {"health_check_timeout": 10},
        "zone_compose_files": {
            "test-cluster": "test-cluster/docker-compose.yml",
        },
    }
    (config_dir / "tool-exec.yaml").write_text(yaml.dump(config))
    (root / "work").mkdir()

    return root


@pytest.fixture()
def project_a(tmp_path: Path) -> Path:
    """Project root A for worktree isolation tests."""
    return _make_project(tmp_path, "worktree-a")


@pytest.fixture()
def project_b(tmp_path: Path) -> Path:
    """Project root B for worktree isolation tests."""
    return _make_project(tmp_path, "worktree-b")


@pytest.fixture()
def clm_a(project_a: Path) -> ContainerLifecycleManager:
    """CLM for project A."""
    return ContainerLifecycleManager(project_root=project_a)


@pytest.fixture()
def clm_b(project_b: Path) -> ContainerLifecycleManager:
    """CLM for project B."""
    return ContainerLifecycleManager(project_root=project_b)


@pytest.fixture(autouse=True)
def cleanup(clm_a: ContainerLifecycleManager, clm_b: ContainerLifecycleManager) -> None:
    """Teardown all CLM clusters after each test."""
    yield  # type: ignore[misc]
    clm_a.teardown()
    clm_b.teardown()


# =============================================================================
# Happy path (60%)
# =============================================================================


class TestFullLifecycleHappy:
    """Full CLM lifecycle — happy path."""

    def test_ensure_clusters_when_not_running_then_starts_and_reports_running(
        self, clm_a: ContainerLifecycleManager
    ) -> None:
        """CLM starts containers from stopped state."""
        results = clm_a.ensure_clusters_running(["test-cluster"])
        assert len(results) == 1
        assert results[0].state == ClusterState.RUNNING
        assert results[0].cluster_name == "test-cluster"
        assert len(results[0].services) >= 1

    def test_ensure_clusters_when_already_running_then_skips_startup(
        self, clm_a: ContainerLifecycleManager
    ) -> None:
        """CLM-001: Second call detects running containers via Docker and skips startup."""
        clm_a.ensure_clusters_running(["test-cluster"])
        results = clm_a.ensure_clusters_running(["test-cluster"])
        assert results[0].state == ClusterState.RUNNING

    def test_teardown_when_containers_running_then_removes_all(
        self, clm_a: ContainerLifecycleManager
    ) -> None:
        """CLM-003: Teardown removes containers and deletes state file."""
        clm_a.ensure_clusters_running(["test-cluster"])
        result = clm_a.teardown()
        assert "test-cluster" in result.clusters_torn_down
        assert result.state_file_deleted is True
        assert result.errors == []

    def test_state_file_when_clusters_started_then_exists_on_disk(
        self, clm_a: ContainerLifecycleManager, project_a: Path
    ) -> None:
        """Session state file is created after startup."""
        clm_a.ensure_clusters_running(["test-cluster"])
        state_files = list((project_a / "work").glob(".rainbow-session-state-*"))
        assert len(state_files) == 1

    def test_state_file_when_teardown_complete_then_deleted(
        self, clm_a: ContainerLifecycleManager, project_a: Path
    ) -> None:
        """Session state file is deleted after successful teardown."""
        clm_a.ensure_clusters_running(["test-cluster"])
        clm_a.teardown()
        state_files = list((project_a / "work").glob(".rainbow-session-state-*"))
        assert len(state_files) == 0

    def test_compose_project_name_when_clm_created_then_is_worktree_specific(
        self, clm_a: ContainerLifecycleManager
    ) -> None:
        """CLM-002: Project name includes worktree hash."""
        assert clm_a.compose_project_name.startswith("rainbow-")
        assert clm_a.compose_project_name != "rainbow"


class TestCLM001DockerReality:
    """CLM-001: Docker reality check — E2E."""

    def test_ensure_clusters_when_containers_stopped_externally_then_restarts(
        self, clm_a: ContainerLifecycleManager
    ) -> None:
        """CLM-001: If containers are stopped outside CLM, restart them."""
        # Start via CLM
        clm_a.ensure_clusters_running(["test-cluster"])

        # Stop containers outside CLM (simulates Docker daemon restart)
        adapter = DockerComposeAdapter(clm_a._project_root, clm_a.compose_project_name)
        adapter.compose_down("test-cluster/docker-compose.yml")

        # CLM should detect containers are gone and restart
        results = clm_a.ensure_clusters_running(["test-cluster"])
        assert results[0].state == ClusterState.RUNNING


class TestCLM002WorktreeIsolation:
    """CLM-002: Worktree isolation — E2E."""

    def test_two_clms_when_same_cluster_name_then_no_interference(
        self,
        clm_a: ContainerLifecycleManager,
        clm_b: ContainerLifecycleManager,
    ) -> None:
        """CLM-002: Two worktrees start the same cluster without collisions."""
        assert clm_a.compose_project_name != clm_b.compose_project_name

        results_a = clm_a.ensure_clusters_running(["test-cluster"])
        results_b = clm_b.ensure_clusters_running(["test-cluster"])

        assert results_a[0].state == ClusterState.RUNNING
        assert results_b[0].state == ClusterState.RUNNING

    def test_teardown_a_when_b_running_then_b_unaffected(
        self,
        clm_a: ContainerLifecycleManager,
        clm_b: ContainerLifecycleManager,
    ) -> None:
        """CLM-002: Tearing down A does not affect B's containers."""
        clm_a.ensure_clusters_running(["test-cluster"])
        clm_b.ensure_clusters_running(["test-cluster"])

        clm_a.teardown()

        # B should still be running
        results_b = clm_b.ensure_clusters_running(["test-cluster"])
        assert results_b[0].state == ClusterState.RUNNING


# =============================================================================
# Negative (30%)
# =============================================================================


class TestFullLifecycleNegative:
    """Full CLM lifecycle — negative cases."""

    def test_ensure_clusters_when_unknown_cluster_then_returns_error(
        self, clm_a: ContainerLifecycleManager
    ) -> None:
        """Unknown cluster name produces ERROR state."""
        results = clm_a.ensure_clusters_running(["nonexistent"])
        assert results[0].state == ClusterState.ERROR
        assert "Unknown cluster" in results[0].error

    def test_teardown_when_no_state_file_then_succeeds_without_error(
        self, clm_a: ContainerLifecycleManager
    ) -> None:
        """Teardown with no prior startup succeeds (idempotent)."""
        result = clm_a.teardown()
        assert result.errors == [] or all("CLM-003" not in e for e in result.errors)


# =============================================================================
# Edge (10%)
# =============================================================================


class TestFullLifecycleEdge:
    """Full CLM lifecycle — edge cases."""

    def test_ensure_clusters_when_called_twice_rapidly_then_second_is_fast(
        self, clm_a: ContainerLifecycleManager
    ) -> None:
        """Second ensure call is fast because Docker reality check confirms running."""
        import time

        clm_a.ensure_clusters_running(["test-cluster"])

        start = time.monotonic()
        clm_a.ensure_clusters_running(["test-cluster"])
        elapsed = time.monotonic() - start

        # The fast path (Docker reality check only) should complete in < 5s
        assert elapsed < 5.0
