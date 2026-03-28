# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for SubprocessSshExecutor and CurlSocksVerifier concrete adapters.

TASK-023-073: SubprocessSshExecutor
TASK-023-074: CurlSocksVerifier

These test the real adapters (not mocks), but against localhost or
unreachable hosts to avoid requiring live infrastructure.
"""

from __future__ import annotations

from unittest.mock import patch, MagicMock

import subprocess
import pytest

from src.proxy_infra.infrastructure.ssh.subprocess_ssh_executor import (
    SubprocessSshExecutor,
    SshCommandResult,
)
from src.proxy_infra.infrastructure.ssh.curl_socks_verifier import (
    CurlSocksVerifier,
)


# =============================================================================
# SubprocessSshExecutor tests
# =============================================================================


class TestSubprocessSshExecutor:
    """Tests for the SSH subprocess executor."""

    def test_execute_returns_ssh_command_result(self) -> None:
        """Execute returns SshCommandResult with stdout and returncode."""
        executor = SubprocessSshExecutor(timeout=5)
        # Mock subprocess.run to simulate a successful SSH command
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="command output\n",
                returncode=0,
                stderr="",
            )
            result = executor.execute("10.0.0.1", "/tmp/key", "echo hello")

            assert isinstance(result, SshCommandResult)
            assert result.stdout == "command output\n"
            assert result.returncode == 0

    def test_execute_passes_correct_ssh_flags(self) -> None:
        """SSH command includes -i key, StrictHostKeyChecking, BatchMode."""
        executor = SubprocessSshExecutor(timeout=30)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=0, stderr="")
            executor.execute("1.2.3.4", "/path/to/key", "whoami")

            cmd = mock_run.call_args[0][0]
            assert "ssh" == cmd[0]
            assert "-i" in cmd
            assert "/path/to/key" in cmd
            assert "StrictHostKeyChecking=accept-new" in " ".join(cmd)
            assert "BatchMode=yes" in " ".join(cmd)
            assert "root@1.2.3.4" in cmd

    def test_execute_when_timeout_then_returns_negative_returncode(self) -> None:
        """Timeout produces returncode -1, not an exception."""
        executor = SubprocessSshExecutor(timeout=1)
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="ssh", timeout=1)):
            result = executor.execute("10.0.0.1", "/tmp/key", "sleep 60")
            assert result.returncode == -1
            assert "timed out" in result.stderr

    def test_execute_when_ssh_not_found_then_returns_error(self) -> None:
        """Missing ssh binary returns error, not exception."""
        executor = SubprocessSshExecutor()
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = executor.execute("10.0.0.1", "/tmp/key", "echo test")
            assert result.returncode == -1
            assert "not found" in result.stderr

    def test_execute_captures_stderr(self) -> None:
        """stderr from remote command is captured."""
        executor = SubprocessSshExecutor()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="",
                returncode=1,
                stderr="Permission denied",
            )
            result = executor.execute("10.0.0.1", "/tmp/key", "sudo rm -rf /")
            assert result.returncode == 1
            assert "Permission denied" in result.stderr

    def test_execute_uses_configurable_user(self) -> None:
        """SSH user is configurable."""
        executor = SubprocessSshExecutor(ssh_user="ubuntu")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=0, stderr="")
            executor.execute("10.0.0.1", "/tmp/key", "id")

            cmd = mock_run.call_args[0][0]
            assert "ubuntu@10.0.0.1" in cmd


# =============================================================================
# CurlSocksVerifier tests
# =============================================================================


class TestCurlSocksVerifier:
    """Tests for the SOCKS5 curl verifier."""

    def test_verify_when_curl_succeeds_with_ip_then_returns_true(self) -> None:
        """Valid IP response from curl = proxy working."""
        verifier = CurlSocksVerifier(timeout=5)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="159.203.44.10\n",
                returncode=0,
                stderr="",
            )
            assert verifier.verify("159.203.44.10", 1080, "user", "pass") is True

    def test_verify_when_curl_fails_then_returns_false(self) -> None:
        """Non-zero curl exit = proxy not working."""
        verifier = CurlSocksVerifier(timeout=5)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="",
                returncode=7,  # curl: connection refused
                stderr="Failed to connect",
            )
            assert verifier.verify("10.0.0.1", 1080, "user", "pass") is False

    def test_verify_when_response_not_ip_then_returns_false(self) -> None:
        """Non-IP response (e.g., HTML error page) = verification failure."""
        verifier = CurlSocksVerifier(timeout=5)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="<html>Error</html>",
                returncode=0,
                stderr="",
            )
            assert verifier.verify("10.0.0.1", 1080, "user", "pass") is False

    def test_verify_when_timeout_then_returns_false(self) -> None:
        """Curl timeout = proxy not responding."""
        verifier = CurlSocksVerifier(timeout=1)
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="curl", timeout=1)):
            assert verifier.verify("10.0.0.1", 1080, "user", "pass") is False

    def test_verify_passes_correct_curl_flags(self) -> None:
        """Curl command includes socks5-hostname, proxy-user, max-time."""
        verifier = CurlSocksVerifier(timeout=10)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="1.2.3.4", returncode=0, stderr="")
            verifier.verify("5.6.7.8", 1080, "jerry-abc", "secretpass")

            cmd = mock_run.call_args[0][0]
            assert "curl" == cmd[0]
            assert "--socks5-hostname" in cmd
            assert "5.6.7.8:1080" in cmd
            assert "--proxy-user" in cmd
            assert "jerry-abc:secretpass" in cmd

    def test_verify_when_curl_not_found_then_returns_false(self) -> None:
        """Missing curl binary returns False."""
        verifier = CurlSocksVerifier()
        with patch("subprocess.run", side_effect=FileNotFoundError):
            assert verifier.verify("10.0.0.1", 1080, "user", "pass") is False
