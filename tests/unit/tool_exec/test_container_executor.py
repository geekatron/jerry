# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for ContainerExecutor."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.tool_exec.domain.services.credential_filter import CredentialFilterService
from src.tool_exec.infrastructure.adapters.container_executor import ContainerExecutor


class TestContainerExecutorCommandBuilding:
    """Tests for docker compose exec command construction."""

    @patch("src.tool_exec.infrastructure.adapters.container_executor.subprocess.run")
    def test_builds_basic_command(self, mock_run: MagicMock) -> None:
        """Builds correct docker compose exec command."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        executor = ContainerExecutor(credential_filter=CredentialFilterService())
        executor.execute(
            tool_command="nuclei",
            tool_args=["-u", "example.com"],
            service="recon-pipeline",
            compose_file="/path/to/docker-compose.yml",
        )

        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert cmd[0] == "docker"
        assert cmd[1] == "compose"
        assert "-f" in cmd
        assert "/path/to/docker-compose.yml" in cmd
        assert "exec" in cmd
        assert "-T" in cmd
        assert "recon-pipeline" in cmd
        assert "nuclei" in cmd
        assert "-u" in cmd
        assert "example.com" in cmd

    @patch("src.tool_exec.infrastructure.adapters.container_executor.subprocess.run")
    def test_docker_not_found_returns_exit_3(self, mock_run: MagicMock) -> None:
        """Missing docker returns exit code 3."""
        mock_run.side_effect = FileNotFoundError()

        executor = ContainerExecutor(credential_filter=CredentialFilterService())
        result = executor.execute(
            tool_command="nuclei",
            service="recon-pipeline",
        )

        assert result.exit_code == 3
        assert "docker" in result.stderr.lower()

    @patch("src.tool_exec.infrastructure.adapters.container_executor.subprocess.run")
    def test_container_not_running_returns_exit_3(self, mock_run: MagicMock) -> None:
        """Container not running returns exit code 3."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="service 'recon-pipeline' is not running",
        )

        executor = ContainerExecutor(credential_filter=CredentialFilterService())
        result = executor.execute(
            tool_command="nuclei",
            service="recon-pipeline",
        )

        assert result.exit_code == 3

    @patch("src.tool_exec.infrastructure.adapters.container_executor.subprocess.run")
    def test_timeout_returns_exit_2(self, mock_run: MagicMock) -> None:
        """Timed-out container execution returns exit code 2."""
        import subprocess

        mock_run.side_effect = subprocess.TimeoutExpired(cmd="docker", timeout=300)

        executor = ContainerExecutor(credential_filter=CredentialFilterService())
        result = executor.execute(
            tool_command="nuclei",
            service="recon-pipeline",
            timeout=300,
        )

        assert result.exit_code == 2


class TestContainerExecutorHealthCheck:
    """Tests for container health check."""

    @patch("src.tool_exec.infrastructure.adapters.container_executor.subprocess.run")
    def test_healthy_service(self, mock_run: MagicMock) -> None:
        """Health check returns True for running service."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="recon-pipeline\n",
            stderr="",
        )

        executor = ContainerExecutor(credential_filter=CredentialFilterService())
        assert executor.health_check("recon-pipeline") is True

    @patch("src.tool_exec.infrastructure.adapters.container_executor.subprocess.run")
    def test_unhealthy_service(self, mock_run: MagicMock) -> None:
        """Health check returns False for stopped service."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr="",
        )

        executor = ContainerExecutor(credential_filter=CredentialFilterService())
        assert executor.health_check("recon-pipeline") is False

    @patch("src.tool_exec.infrastructure.adapters.container_executor.subprocess.run")
    def test_docker_unavailable(self, mock_run: MagicMock) -> None:
        """Health check returns False when docker is not available."""
        mock_run.side_effect = FileNotFoundError()

        executor = ContainerExecutor(credential_filter=CredentialFilterService())
        assert executor.health_check("recon-pipeline") is False


class TestContainerExecutorFinding004:
    """Tests for FINDING-004 (CWE-200): credential filter applied to stderr.

    Mirrors TestLocalExecutorFinding004 for the container execution path.
    """

    @patch("src.tool_exec.infrastructure.adapters.container_executor.subprocess.run")
    def test_credential_in_stderr_triggers_detection(self, mock_run: MagicMock) -> None:
        """Credential in stderr triggers detection and sets exit code 4 (FINDING-004).

        DA-002/CV-005 (FIX-1): Inline redaction -- the credential token is
        replaced with [CREDENTIAL-REDACTED] in the filtered stderr output.
        """
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="clean stdout",
            stderr="password=longpassword1",
        )

        cred_filter = CredentialFilterService()
        executor = ContainerExecutor(credential_filter=cred_filter)
        result = executor.execute(
            tool_command="msfconsole",
            service="exploit-framework",
        )

        assert result.credential_detected is True
        assert result.exit_code == 4
        assert "[CREDENTIAL-REDACTED]" in result.stderr

    @patch("src.tool_exec.infrastructure.adapters.container_executor.subprocess.run")
    def test_credential_in_stderr_filters_stderr_output(self, mock_run: MagicMock) -> None:
        """Detected credential in stderr is redacted in the returned stderr field."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr="password=longpassword1",
        )

        cred_filter = CredentialFilterService()
        executor = ContainerExecutor(credential_filter=cred_filter)
        result = executor.execute(
            tool_command="tool",
            service="service",
        )

        assert "longpassword1" not in result.stderr

    @patch("src.tool_exec.infrastructure.adapters.container_executor.subprocess.run")
    def test_clean_stderr_passes_through(self, mock_run: MagicMock) -> None:
        """Clean stderr without credentials passes through unchanged."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="stdout data",
            stderr="info: scan completed",
        )

        cred_filter = CredentialFilterService()
        executor = ContainerExecutor(credential_filter=cred_filter)
        result = executor.execute(
            tool_command="nuclei",
            service="recon-pipeline",
        )

        assert result.credential_detected is False
        assert result.stderr == "info: scan completed"

    @patch("src.tool_exec.infrastructure.adapters.container_executor.subprocess.run")
    def test_raw_stderr_preserved(self, mock_run: MagicMock) -> None:
        """raw_stderr carries original unfiltered stderr (needed for quarantine)."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr="password=longpassword1",
        )

        cred_filter = CredentialFilterService()
        executor = ContainerExecutor(credential_filter=cred_filter)
        result = executor.execute(
            tool_command="tool",
            service="service",
        )

        assert result.raw_stderr == "password=longpassword1"
