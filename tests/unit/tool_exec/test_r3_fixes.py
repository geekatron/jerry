# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""R3 Tournament Consensus Fix tests.

Covers the 3 findings from the W12-PHASE2-R3 tournament consensus:

  FIX-R3-1 (PM-001-R3): strict_mode not threaded to executors.
  FIX-R3-2 (PM-002-R3/RT-001/IN-021): Audit write failure silently swallowed.
  FIX-R3-3 (SR-002/CC-005/DA-R3-001/IN-022/PM-005): Health check and
             init-engagement bypass factory; unused mode_resolver in factory.

References:
    - W12-PHASE2-R3-FIX: Engagement ID
    - eng-backend-r3-fix.md: Full remediation record
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.interface.cli.tool_exec_commands import (
    _handle_health_check,
    _handle_init_engagement,
    _prompt_zone3_approval,
    _write_approval_audit,
    create_tool_exec_handler,
)
from src.tool_exec.domain.services.credential_filter import CredentialFilterService
from src.tool_exec.domain.services.engagement_initializer import EngagementInitializer
from src.tool_exec.domain.value_objects.exit_codes import ExitCode
from src.tool_exec.infrastructure.adapters.container_executor import ContainerExecutor
from src.tool_exec.infrastructure.adapters.local_executor import LocalExecutor

# =============================================================================
# FIX-R3-1: strict_mode not threaded to executors (PM-001-R3)
# =============================================================================


class TestR3Fix1StrictModeThreaded:
    """PM-001-R3: strict_mode resolved from env and threaded through executors."""

    def test_local_executor_execute_accepts_strict_mode_param(self) -> None:
        """LocalExecutor.execute() accepts strict_mode keyword argument."""
        flt = CredentialFilterService()
        executor = LocalExecutor(credential_filter=flt)
        # strict_mode=False + no_filter=True must not raise when env permits it
        # We test the signature: passing strict_mode=False should be accepted
        # without raising. Use a non-existent command so subprocess returns
        # FileNotFoundError which the executor converts to a clean result.
        result = executor.execute(
            tool_command="__nonexistent_jerry_test_tool__",
            strict_mode=False,
        )
        # FileNotFoundError path returns exit_code=1 with empty stdout/stderr
        assert result.exit_code == 1

    def test_local_executor_strict_mode_false_no_filter_does_not_raise(self) -> None:
        """With strict_mode=False + no_filter=True, executor does not raise RuntimeError.

        Previously the executor always called filter_output(strict_mode=True).
        When JERRY_STRICT_MODE=false, the CLI guard passed but the executor
        raised RuntimeError because it used the hard-coded default.
        """
        flt = MagicMock(spec=CredentialFilterService)
        flt.filter_output.return_value = MagicMock(
            detected=False,
            filtered_output="clean output",
            match=None,
        )
        executor = LocalExecutor(credential_filter=flt)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="clean output",
                stderr="",
                returncode=0,
            )
            result = executor.execute(
                tool_command="echo",
                tool_args=["hello"],
                no_filter=True,
                strict_mode=False,
            )

        # Verify filter_output was called with strict_mode=False, not True
        calls = flt.filter_output.call_args_list
        assert len(calls) >= 1
        for call in calls:
            kwargs = call.kwargs if call.kwargs else {}
            # strict_mode must have been passed as False
            assert kwargs.get("strict_mode", True) is False, (
                f"Expected strict_mode=False but got call: {call}"
            )
        assert result.exit_code == 0

    def test_container_executor_execute_accepts_strict_mode_param(self) -> None:
        """ContainerExecutor.execute() accepts strict_mode keyword argument."""
        flt = MagicMock(spec=CredentialFilterService)
        flt.filter_output.return_value = MagicMock(
            detected=False,
            filtered_output="",
            match=None,
        )
        executor = ContainerExecutor(credential_filter=flt, project_root="/tmp")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="",
                stderr="",
                returncode=0,
            )
            executor.execute(
                tool_command="nmap",
                service="nmap",
                strict_mode=False,
            )

        for call in flt.filter_output.call_args_list:
            kwargs = call.kwargs if call.kwargs else {}
            assert kwargs.get("strict_mode", True) is False, (
                f"Expected strict_mode=False but got call: {call}"
            )

    def test_local_executor_strict_mode_true_no_filter_raises_via_filter(self) -> None:
        """With strict_mode=True + no_filter=True, filter_output raises RuntimeError.

        The executor converts it to STRICT_MODE_VIOLATION (exit code 9).
        """
        flt = CredentialFilterService()
        executor = LocalExecutor(credential_filter=flt)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="some output",
                stderr="",
                returncode=0,
            )
            result = executor.execute(
                tool_command="echo",
                no_filter=True,
                strict_mode=True,
            )

        assert result.exit_code == int(ExitCode.STRICT_MODE_VIOLATION)

    def test_container_executor_strict_mode_true_no_filter_returns_violation(
        self,
    ) -> None:
        """ContainerExecutor: strict_mode=True + no_filter=True returns STRICT_MODE_VIOLATION."""
        flt = CredentialFilterService()
        executor = ContainerExecutor(credential_filter=flt, project_root="/tmp")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="some output",
                stderr="",
                returncode=0,
            )
            result = executor.execute(
                tool_command="nmap",
                service="nmap",
                no_filter=True,
                strict_mode=True,
            )

        assert result.exit_code == int(ExitCode.STRICT_MODE_VIOLATION)


# =============================================================================
# FIX-R3-2: Audit write failure silently swallowed (PM-002-R3/RT-001/IN-021)
# =============================================================================


class TestR3Fix2AuditWriteFailure:
    """PM-002-R3/RT-001/IN-021: _write_approval_audit returns bool; approval
    denied when audit write fails."""

    def test_write_approval_audit_returns_true_on_success(self, tmp_path: Path) -> None:
        """_write_approval_audit returns True when the audit file is written."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        result = _write_approval_audit(
            tool_command="msfconsole",
            zone="Zone 3",
            approved=True,
            reason="operator input",
            engagement_id=None,
            engagement_init=init,
        )
        assert result is True

    def test_write_approval_audit_returns_false_on_write_failure(self, tmp_path: Path) -> None:
        """_write_approval_audit returns False when the write fails."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")

        with patch("builtins.open", side_effect=OSError("disk full")):
            with patch("pathlib.Path.write_text", side_effect=OSError("disk full")):
                with patch("pathlib.Path.mkdir"):
                    with patch("os.chmod"):
                        result = _write_approval_audit(
                            tool_command="msfconsole",
                            zone="Zone 3",
                            approved=True,
                            reason="operator input",
                            engagement_id=None,
                            engagement_init=init,
                        )
        assert result is False

    def test_prompt_zone3_approval_denies_when_approved_but_audit_fails(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """When operator approves but audit write fails, approval is denied.

        FIX-R3-2: Zone 3 MUST NOT execute without a tamper-evident audit record.
        """
        init = EngagementInitializer(base_dir=tmp_path / "engagements")

        with patch("sys.stdin") as mock_stdin:
            mock_stdin.isatty.return_value = True
            mock_stdin.readline.return_value = "yes\n"
            with patch("builtins.input", return_value="yes"):
                with patch(
                    "src.interface.cli.tool_exec_commands._write_approval_audit",
                    return_value=False,
                ):
                    result = _prompt_zone3_approval(
                        tool_command="msfconsole",
                        zone="Zone 3",
                        engagement_id=None,
                        engagement_init=init,
                    )

        assert result is False
        captured = capsys.readouterr()
        assert "audit write failed" in captured.err.lower() or "audit" in captured.err.lower()

    def test_prompt_zone3_approval_allows_denial_even_if_audit_fails(self, tmp_path: Path) -> None:
        """A denial is returned immediately even if the audit write fails.

        Denial events are already safe -- blocking a denial because the audit
        write failed would itself be a security regression.
        """
        init = EngagementInitializer(base_dir=tmp_path / "engagements")

        with patch("sys.stdin") as mock_stdin:
            mock_stdin.isatty.return_value = True
            with patch("builtins.input", return_value="no"):
                with patch(
                    "src.interface.cli.tool_exec_commands._write_approval_audit",
                    return_value=False,
                ):
                    result = _prompt_zone3_approval(
                        tool_command="msfconsole",
                        zone="Zone 3",
                        engagement_id=None,
                        engagement_init=init,
                    )

        # Denial must still be returned even when audit fails
        assert result is False

    def test_write_approval_audit_prints_stderr_on_failure(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """_write_approval_audit prints to stderr on failure (always visible)."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")

        with patch("pathlib.Path.write_text", side_effect=OSError("disk full")):
            with patch("pathlib.Path.mkdir"):
                with patch("os.chmod"):
                    _write_approval_audit(
                        tool_command="msfconsole",
                        zone="Zone 3",
                        approved=True,
                        reason="operator input",
                        engagement_id=None,
                        engagement_init=init,
                    )

        captured = capsys.readouterr()
        assert "audit" in captured.err.lower()


# =============================================================================
# FIX-R3-3: Health check and init-engagement bypass factory (SR-002/CC-005)
# =============================================================================


class TestR3Fix3FactoryCompliance:
    """SR-002/CC-005/DA-R3-001/IN-022/PM-005: Sub-handlers use factory services."""

    def test_factory_does_not_contain_mode_resolver(self, tmp_path: Path) -> None:
        """DA-R3-002: mode_resolver is not in the factory return value.

        handle_tool_exec constructs its own ModeResolverService with a
        family-specific env_var_prefix. A default-prefix instance in the
        factory is misleading and invites incorrect reuse.
        """
        (tmp_path / "tool_families.yaml").write_text("families: []\n")
        services = create_tool_exec_handler(tmp_path)
        assert "mode_resolver" not in services

    def test_handle_init_engagement_accepts_factory_built_initializer(self, tmp_path: Path) -> None:
        """_handle_init_engagement receives EngagementInitializer, not project_root.

        FIX-R3-3: The function signature now accepts a factory-built
        EngagementInitializer rather than constructing its own.
        """
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        result = _handle_init_engagement("ENG-001", init)
        assert result == int(ExitCode.SUCCESS)
        assert (tmp_path / "engagements" / "ENG-001").exists()

    def test_handle_init_engagement_bad_id_returns_unknown_tool(self, tmp_path: Path) -> None:
        """Bad engagement ID returns UNKNOWN_TOOL, not ENGAGEMENT_NOT_INIT."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        # Inject a ValueError via mock to simulate invalid ID
        with patch.object(init, "initialize", side_effect=ValueError("bad id")):
            result = _handle_init_engagement("BAD ID!", init)
        assert result == int(ExitCode.UNKNOWN_TOOL)

    def test_handle_health_check_uses_passed_container_executor(self, tmp_path: Path) -> None:
        """_handle_health_check uses the passed ContainerExecutor, not a new one.

        FIX-R3-3: Verify that the function delegates to the supplied executor's
        health_check method. If it constructed its own ContainerExecutor inline
        it would call health_check on the inline instance, not the mock.
        """
        mock_executor = MagicMock(spec=ContainerExecutor)
        mock_executor.health_check.return_value = True

        mock_resolution = MagicMock()
        mock_resolution.container_service = "nmap"
        mock_resolution.compose_file = "docker-compose.yml"

        result = _handle_health_check(mock_resolution, mock_executor, tmp_path)

        mock_executor.health_check.assert_called_once()
        assert result == int(ExitCode.SUCCESS)

    def test_handle_health_check_no_service_returns_success_without_calling_executor(
        self, tmp_path: Path
    ) -> None:
        """When no container_service is configured, health_check exits early."""
        mock_executor = MagicMock(spec=ContainerExecutor)

        mock_resolution = MagicMock()
        mock_resolution.container_service = None
        mock_resolution.compose_file = None

        result = _handle_health_check(mock_resolution, mock_executor, tmp_path)

        mock_executor.health_check.assert_not_called()
        assert result == int(ExitCode.SUCCESS)

    def test_handle_health_check_unhealthy_service_returns_container_not_running(
        self, tmp_path: Path
    ) -> None:
        """When health_check returns False, CONTAINER_NOT_RUNNING is returned."""
        mock_executor = MagicMock(spec=ContainerExecutor)
        mock_executor.health_check.return_value = False

        mock_resolution = MagicMock()
        mock_resolution.container_service = "nmap"
        mock_resolution.compose_file = "docker-compose.yml"

        result = _handle_health_check(mock_resolution, mock_executor, tmp_path)

        assert result == int(ExitCode.CONTAINER_NOT_RUNNING)
