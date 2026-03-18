# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for LocalExecutor."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.tool_exec.domain.services.credential_filter import CredentialFilterService
from src.tool_exec.infrastructure.adapters.local_executor import LocalExecutor


class TestLocalExecutorBasic:
    """Tests for basic local execution."""

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_execute_captures_stdout(self, mock_run: MagicMock) -> None:
        """Executor captures stdout from the subprocess."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="scan results here",
            stderr="",
        )

        executor = LocalExecutor()
        result = executor.execute("echo", ["hello"])

        assert result.exit_code == 0
        assert result.stdout == "scan results here"
        assert result.raw_stdout == "scan results here"

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_execute_captures_stderr(self, mock_run: MagicMock) -> None:
        """Executor captures stderr from the subprocess."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="error message",
        )

        executor = LocalExecutor()
        result = executor.execute("bad-command")

        assert result.exit_code == 1
        assert result.stderr == "error message"

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_execute_passes_args(self, mock_run: MagicMock) -> None:
        """Executor passes tool args to subprocess."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        executor = LocalExecutor()
        executor.execute("nuclei", ["-t", "cves/", "-u", "example.com"])

        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert call_args == ["nuclei", "-t", "cves/", "-u", "example.com"]

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_tool_not_found_returns_exit_1(self, mock_run: MagicMock) -> None:
        """Missing tool binary returns exit code 1."""
        mock_run.side_effect = FileNotFoundError()

        executor = LocalExecutor()
        result = executor.execute("nonexistent-tool")

        assert result.exit_code == 1
        assert "not found" in result.stderr.lower()

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_timeout_returns_exit_2(self, mock_run: MagicMock) -> None:
        """Timed-out execution returns exit code 2."""
        import subprocess

        mock_run.side_effect = subprocess.TimeoutExpired(cmd="tool", timeout=300)

        executor = LocalExecutor()
        result = executor.execute("slow-tool", timeout=300)

        assert result.exit_code == 2
        assert "timed out" in result.stderr.lower()


class TestLocalExecutorCredentialFilter:
    """Tests for credential filter integration."""

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_credential_filter_triggers(self, mock_run: MagicMock) -> None:
        """Credential filter detects sensitive output.

        DA-002/CV-005 (FIX-1): Inline redaction -- the credential token is
        replaced with [CREDENTIAL-REDACTED] in the filtered output.
        """
        pw = "longpassword1"
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=f"password={pw}",
            stderr="",
        )

        cred_filter = CredentialFilterService()
        executor = LocalExecutor(credential_filter=cred_filter)
        result = executor.execute("tool")

        assert result.credential_detected is True
        assert result.exit_code == 4  # CREDENTIAL_DETECTED
        assert "[CREDENTIAL-REDACTED]" in result.stdout
        assert pw not in result.stdout

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_no_filter_flag_skips_filtering(self, mock_run: MagicMock) -> None:
        """--no-filter skips credential filtering."""
        pw = "longpassword1"
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=f"password={pw}",
            stderr="",
        )

        cred_filter = CredentialFilterService()
        executor = LocalExecutor(credential_filter=cred_filter)
        result = executor.execute("tool", no_filter=True)

        assert result.credential_detected is False
        assert result.exit_code == 0

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_clean_output_passes_through(self, mock_run: MagicMock) -> None:
        """Clean output passes through the filter unchanged."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="clean scan results",
            stderr="",
        )

        cred_filter = CredentialFilterService()
        executor = LocalExecutor(credential_filter=cred_filter)
        result = executor.execute("nuclei")

        assert result.credential_detected is False
        assert result.stdout == "clean scan results"
        assert result.exit_code == 0


class TestLocalExecutorFinding004:
    """Tests for FINDING-004 (CWE-200): credential filter applied to stderr.

    Before the fix the filter was applied only to stdout. Security tools routinely
    write credentials, session tokens, and key material to stderr. The fix applies
    the filter to both streams; if either triggers detection the exit code is 4
    (CREDENTIAL_DETECTED) and both streams are quarantined.
    """

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
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
        executor = LocalExecutor(credential_filter=cred_filter)
        result = executor.execute("msf")

        assert result.credential_detected is True
        assert result.exit_code == 4
        assert "[CREDENTIAL-REDACTED]" in result.stderr

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_credential_in_stderr_filters_stderr_output(self, mock_run: MagicMock) -> None:
        """Detected credential in stderr is redacted in the returned stderr field."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr="password=longpassword1",
        )

        cred_filter = CredentialFilterService()
        executor = LocalExecutor(credential_filter=cred_filter)
        result = executor.execute("tool")

        assert "longpassword1" not in result.stderr

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_credential_in_stdout_still_detected(self, mock_run: MagicMock) -> None:
        """Credential in stdout is still detected after the stderr fix (regression guard)."""
        pw = "longpassword1"
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=f"password={pw}",
            stderr="clean stderr",
        )

        cred_filter = CredentialFilterService()
        executor = LocalExecutor(credential_filter=cred_filter)
        result = executor.execute("tool")

        assert result.credential_detected is True
        assert result.exit_code == 4

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_clean_stderr_passes_through(self, mock_run: MagicMock) -> None:
        """Clean stderr without credentials passes through unchanged."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="stdout data",
            stderr="info: scan completed",
        )

        cred_filter = CredentialFilterService()
        executor = LocalExecutor(credential_filter=cred_filter)
        result = executor.execute("nuclei")

        assert result.credential_detected is False
        assert result.stderr == "info: scan completed"
        assert result.exit_code == 0

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_raw_stderr_preserved(self, mock_run: MagicMock) -> None:
        """raw_stderr carries original unfiltered stderr (needed for quarantine)."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr="password=longpassword1",
        )

        cred_filter = CredentialFilterService()
        executor = LocalExecutor(credential_filter=cred_filter)
        result = executor.execute("tool")

        assert result.raw_stderr == "password=longpassword1"

    @patch("src.tool_exec.infrastructure.adapters.local_executor.subprocess.run")
    def test_no_filter_skips_stderr_filtering(self, mock_run: MagicMock) -> None:
        """--no-filter skips filtering on stderr as well as stdout."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr="password=longpassword1",
        )

        cred_filter = CredentialFilterService()
        executor = LocalExecutor(credential_filter=cred_filter)
        result = executor.execute("tool", no_filter=True)

        assert result.credential_detected is False
        assert result.exit_code == 0
