# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Integration tests for ContainerLifecycleManager.

These tests exercise the DockerComposeAdapter against a real Docker daemon.
They require Docker to be running and are skipped when Docker is unavailable.

Naming: test_{scenario}_when_{condition}_then_{expected}
Marker: @pytest.mark.integration
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

from src.tool_exec.infrastructure.container_lifecycle.docker_compose_adapter import (
    DockerComposeAdapter,
)
from src.tool_exec.infrastructure.container_lifecycle.worktree_isolation import (
    derive_compose_project_name,
)


def _docker_available() -> bool:
    """Check if Docker daemon is reachable."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not _docker_available(), reason="Docker daemon not available"),
]


@pytest.fixture()
def project_root(tmp_path: Path) -> Path:
    """Create a temp project root with a minimal compose file."""
    compose_dir = tmp_path / "test-cluster"
    compose_dir.mkdir()
    compose_data = {
        "services": {
            "alpine-test": {
                "image": "alpine:3.19",
                "command": ["sleep", "30"],
            }
        }
    }
    (compose_dir / "docker-compose.yml").write_text(
        yaml.dump(compose_data, default_flow_style=False)
    )
    return tmp_path


@pytest.fixture()
def adapter(project_root: Path) -> DockerComposeAdapter:
    """Create an adapter with a unique project name for test isolation."""
    project_name = f"rainbow-inttest-{id(project_root) % 10000:04d}"
    return DockerComposeAdapter(project_root, project_name)


@pytest.fixture(autouse=True)
def cleanup_containers(adapter: DockerComposeAdapter, project_root: Path) -> None:
    """Ensure containers are torn down after each test."""
    yield  # type: ignore[misc]
    # Best-effort cleanup
    try:
        adapter.compose_down("test-cluster/docker-compose.yml")
    except Exception:  # noqa: BLE001
        pass


class TestAdapterDockerReality:
    """Integration: DockerComposeAdapter against real Docker."""

    def test_is_docker_available_when_daemon_running_then_returns_true(
        self, adapter: DockerComposeAdapter
    ) -> None:
        """Real Docker daemon is reachable (guarded by skipif)."""
        assert adapter.is_docker_available() is True

    def test_get_services_when_no_containers_running_then_returns_empty(
        self, adapter: DockerComposeAdapter
    ) -> None:
        """No containers for this project = empty service list."""
        services = adapter.get_running_services("test-cluster/docker-compose.yml")
        assert services == []

    def test_compose_up_when_called_then_starts_container(
        self, adapter: DockerComposeAdapter
    ) -> None:
        """docker compose up actually starts a container visible in ps."""
        adapter.compose_up("test-cluster/docker-compose.yml")
        services = adapter.get_running_services("test-cluster/docker-compose.yml")
        assert len(services) >= 1
        assert any(s.state == "running" for s in services)

    def test_compose_down_when_called_then_removes_containers(
        self, adapter: DockerComposeAdapter
    ) -> None:
        """docker compose down removes all containers."""
        adapter.compose_up("test-cluster/docker-compose.yml")
        adapter.compose_down("test-cluster/docker-compose.yml")
        services = adapter.get_running_services("test-cluster/docker-compose.yml")
        running = [s for s in services if s.state == "running"]
        assert running == []

    def test_wait_for_health_when_service_running_then_returns_true(
        self, adapter: DockerComposeAdapter
    ) -> None:
        """wait_for_health returns True for a running service (no healthcheck)."""
        adapter.compose_up("test-cluster/docker-compose.yml")
        result = adapter.wait_for_health(
            "test-cluster/docker-compose.yml", "alpine-test", max_wait=10
        )
        assert result is True

    def test_list_volumes_when_no_volumes_then_returns_empty(
        self, adapter: DockerComposeAdapter
    ) -> None:
        """No project volumes when none were created."""
        volumes = adapter.list_project_volumes()
        assert volumes == []


class TestWorktreeIsolationReal:
    """Integration: worktree isolation produces usable project names."""

    def test_derive_name_when_real_repo_then_produces_valid_compose_name(self) -> None:
        """Derived name works as a real Docker Compose project name."""
        name = derive_compose_project_name()
        assert name.startswith("rainbow-")
        # Docker Compose project names must be lowercase alphanumeric + hyphens
        assert all(c.isalnum() or c == "-" for c in name)
