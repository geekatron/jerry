# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Unit tests for DockerComposeAdapter.

Tests subprocess calls are constructed correctly using mock subprocess.
Naming: test_{scenario}_when_{condition}_then_{expected}
Distribution: 60% happy / 30% negative / 10% edge
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.tool_exec.infrastructure.container_lifecycle.docker_compose_adapter import (
    DockerComposeAdapter,
)


@pytest.fixture()
def adapter(tmp_path: Path) -> DockerComposeAdapter:
    """Create an adapter with a temp project root."""
    return DockerComposeAdapter(tmp_path, "rainbow-test1234")


# =============================================================================
# Happy path (60%)
# =============================================================================


class TestDockerAvailableHappy:
    """Docker availability — happy path."""

    @patch("subprocess.run")
    def test_is_docker_available_when_daemon_running_then_returns_true(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Docker available when docker info exits 0."""
        mock_run.return_value = MagicMock(returncode=0)
        assert adapter.is_docker_available() is True


class TestGetRunningServicesHappy:
    """Docker Compose ps query — happy path."""

    @patch("subprocess.run")
    def test_get_services_when_single_json_object_then_parses_service(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Parses single-object JSON output from docker compose ps."""
        data = {"Service": "scanner", "State": "running", "Health": "healthy"}
        mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps(data) + "\n")
        services = adapter.get_running_services("compose.yml")
        assert len(services) == 1
        assert services[0].name == "scanner"
        assert services[0].state == "running"
        assert services[0].health == "healthy"

    @patch("subprocess.run")
    def test_get_services_when_json_array_then_parses_all_services(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Parses JSON array output from newer Docker Compose versions."""
        data = [
            {"Service": "svc-a", "State": "running", "Health": "none"},
            {"Service": "svc-b", "State": "running", "Health": "healthy"},
        ]
        mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps(data) + "\n")
        services = adapter.get_running_services("compose.yml")
        assert len(services) == 2
        assert services[0].name == "svc-a"
        assert services[1].name == "svc-b"

    @patch("subprocess.run")
    def test_get_services_when_called_then_passes_project_name_flag(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Verifies -p project_name is passed to docker compose."""
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        adapter.get_running_services("compose.yml")
        args = mock_run.call_args[0][0]
        assert "-p" in args
        idx = args.index("-p")
        assert args[idx + 1] == "rainbow-test1234"


class TestComposeBuildHappy:
    """Compose build — happy path."""

    @patch("subprocess.run")
    def test_compose_build_when_called_then_runs_docker_compose_build(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Invokes docker compose build with project name."""
        mock_run.return_value = MagicMock(returncode=0)
        adapter.compose_build("path/to/compose.yml")
        args = mock_run.call_args[0][0]
        assert "build" in args
        assert "-p" in args

    @patch("subprocess.run")
    def test_compose_build_when_custom_timeout_then_uses_timeout(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Custom timeout is passed to subprocess."""
        mock_run.return_value = MagicMock(returncode=0)
        adapter.compose_build("compose.yml", timeout=300)
        assert mock_run.call_args[1]["timeout"] == 300


class TestComposeUpHappy:
    """Compose up — happy path."""

    @patch("subprocess.run")
    def test_compose_up_when_called_then_runs_detached(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Invokes docker compose up --detach."""
        mock_run.return_value = MagicMock(returncode=0)
        adapter.compose_up("compose.yml")
        args = mock_run.call_args[0][0]
        assert "up" in args
        assert "--detach" in args


class TestComposeDownHappy:
    """Compose down — happy path."""

    @patch("subprocess.run")
    def test_compose_down_when_called_then_removes_volumes_and_orphans(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Invokes docker compose down --volumes --remove-orphans."""
        mock_run.return_value = MagicMock(returncode=0)
        adapter.compose_down("compose.yml")
        args = mock_run.call_args[0][0]
        assert "down" in args
        assert "--volumes" in args
        assert "--remove-orphans" in args


class TestRemoveVolumesHappy:
    """Volume removal — happy path."""

    @patch("subprocess.run")
    def test_remove_volumes_when_all_succeed_then_returns_all(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Successfully removed volumes are all returned."""
        mock_run.return_value = MagicMock(returncode=0)
        removed = adapter.remove_volumes(["vol-a", "vol-b"])
        assert removed == ["vol-a", "vol-b"]

    @patch("subprocess.run")
    def test_remove_volumes_when_empty_list_then_returns_empty(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """No volumes to remove returns empty list without subprocess calls."""
        removed = adapter.remove_volumes([])
        assert removed == []
        mock_run.assert_not_called()


class TestListVolumesHappy:
    """Volume listing — happy path."""

    @patch("subprocess.run")
    def test_list_volumes_when_volumes_exist_then_returns_names(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Lists volumes matching project name filter."""
        mock_run.return_value = MagicMock(
            returncode=0, stdout="rainbow-test1234_pgdata\nrainbow-test1234_logs\n"
        )
        volumes = adapter.list_project_volumes()
        assert volumes == ["rainbow-test1234_pgdata", "rainbow-test1234_logs"]

    @patch("subprocess.run")
    def test_list_volumes_when_no_volumes_then_returns_empty(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Empty output when no project volumes exist."""
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        assert adapter.list_project_volumes() == []

    @patch("subprocess.run")
    def test_list_volumes_when_called_then_filters_by_project_name(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Verifies the --filter flag uses compose project name."""
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        adapter.list_project_volumes()
        args = mock_run.call_args[0][0]
        assert any("name=rainbow-test1234" in a for a in args)


class TestWaitForHealthHappy:
    """Health check polling — happy path."""

    @patch("subprocess.run")
    def test_wait_health_when_service_healthy_then_returns_true(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Returns True when service reports running+healthy."""
        data = {"Service": "scanner", "State": "running", "Health": "healthy"}
        mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps(data) + "\n")
        assert adapter.wait_for_health("compose.yml", "scanner", max_wait=2) is True

    @patch("subprocess.run")
    def test_wait_health_when_no_healthcheck_defined_then_returns_true(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Returns True when service is running with health='none' (no healthcheck)."""
        data = {"Service": "envoy", "State": "running", "Health": "none"}
        mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps(data) + "\n")
        assert adapter.wait_for_health("compose.yml", "envoy", max_wait=2) is True


class TestProjectNameProperty:
    """Project name accessor."""

    def test_project_name_when_accessed_then_returns_constructor_value(
        self, adapter: DockerComposeAdapter
    ) -> None:
        """Property returns the compose project name from constructor."""
        assert adapter.project_name == "rainbow-test1234"


# =============================================================================
# Negative (30%)
# =============================================================================


class TestDockerAvailableNegative:
    """Docker availability — negative cases."""

    @patch("subprocess.run")
    def test_is_docker_available_when_daemon_not_running_then_returns_false(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Docker unavailable when docker info exits non-zero."""
        mock_run.return_value = MagicMock(returncode=1)
        assert adapter.is_docker_available() is False

    @patch("subprocess.run", side_effect=FileNotFoundError)
    def test_is_docker_available_when_binary_missing_then_returns_false(
        self, _mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Docker unavailable when docker binary not found."""
        assert adapter.is_docker_available() is False

    @patch("subprocess.run", side_effect=subprocess.TimeoutExpired("docker", 10))
    def test_is_docker_available_when_timeout_then_returns_false(
        self, _mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Docker unavailable when docker info times out."""
        assert adapter.is_docker_available() is False


class TestGetRunningServicesNegative:
    """Docker Compose ps query — negative cases."""

    @patch("subprocess.run")
    def test_get_services_when_compose_fails_then_returns_empty(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Returns empty list when docker compose ps exits non-zero."""
        mock_run.return_value = MagicMock(returncode=1, stderr="error")
        assert adapter.get_running_services("compose.yml") == []

    @patch("subprocess.run")
    def test_get_services_when_no_containers_then_returns_empty(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Returns empty list when compose reports no containers."""
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        assert adapter.get_running_services("compose.yml") == []

    @patch("subprocess.run", side_effect=subprocess.TimeoutExpired("docker", 30))
    def test_get_services_when_timeout_then_returns_empty(
        self, _mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Returns empty list when docker compose ps times out."""
        assert adapter.get_running_services("compose.yml") == []

    @patch("subprocess.run", side_effect=FileNotFoundError)
    def test_get_services_when_docker_missing_then_returns_empty(
        self, _mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Returns empty list when docker binary not found."""
        assert adapter.get_running_services("compose.yml") == []


class TestRemoveVolumesNegative:
    """Volume removal — negative cases."""

    @patch("subprocess.run")
    def test_remove_volumes_when_partial_failure_then_returns_only_successes(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Only successfully removed volumes are returned."""
        mock_run.side_effect = [
            MagicMock(returncode=0),
            MagicMock(returncode=1, stderr="volume in use"),
        ]
        removed = adapter.remove_volumes(["vol-ok", "vol-fail"])
        assert removed == ["vol-ok"]

    @patch("subprocess.run", side_effect=subprocess.TimeoutExpired("docker", 30))
    def test_remove_volumes_when_timeout_then_returns_empty(
        self, _mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Timeout during volume removal returns empty list."""
        assert adapter.remove_volumes(["vol-a"]) == []


class TestListVolumesNegative:
    """Volume listing — negative cases."""

    @patch("subprocess.run")
    def test_list_volumes_when_docker_fails_then_returns_empty(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Returns empty list when docker volume ls fails."""
        mock_run.return_value = MagicMock(returncode=1)
        assert adapter.list_project_volumes() == []

    @patch("subprocess.run", side_effect=subprocess.TimeoutExpired("docker", 30))
    def test_list_volumes_when_timeout_then_returns_empty(
        self, _mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Returns empty list on timeout."""
        assert adapter.list_project_volumes() == []


class TestWaitForHealthNegative:
    """Health check polling — negative cases."""

    @patch("subprocess.run")
    def test_wait_health_when_service_never_starts_then_returns_false(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Returns False when service stays in 'starting' state."""
        data = {"Service": "scanner", "State": "starting", "Health": "starting"}
        mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps(data) + "\n")
        assert adapter.wait_for_health("compose.yml", "scanner", max_wait=1) is False


# =============================================================================
# Edge (10%)
# =============================================================================


class TestGetRunningServicesEdge:
    """Docker Compose ps query — edge cases."""

    @patch("subprocess.run")
    def test_get_services_when_malformed_json_then_skips_bad_lines(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Malformed JSON lines are skipped without crashing."""
        mock_run.return_value = MagicMock(returncode=0, stdout="not-json\n")
        assert adapter.get_running_services("compose.yml") == []

    @patch("subprocess.run")
    def test_get_services_when_name_field_used_then_falls_back(
        self, mock_run: MagicMock, adapter: DockerComposeAdapter
    ) -> None:
        """Handles Docker output using 'Name' instead of 'Service' key."""
        data = {"Name": "scanner-1", "State": "running", "Health": "none"}
        mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps(data) + "\n")
        services = adapter.get_running_services("compose.yml")
        assert services[0].name == "scanner-1"
