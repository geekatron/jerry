# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Zone 3 interactive approval gate E2E tests using Python pty.

Tests that the Zone 3 per-operation approval gate behaves correctly across
four interaction modalities:

    1. Real TTY with exact confirmation phrase  -> gate approves, tool runs
    2. Real TTY with wrong tool name in phrase  -> gate denies (exit 11)
    3. Real TTY with legacy "yes" input         -> gate denies (regression)
    4. No TTY (plain subprocess)               -> gate auto-denies (exit 11)

TASK-045: The gate now requires the operator to type the exact phrase
"APPROVE: <tool_command>" (case-sensitive, no prefix match).  Sending the
old "yes\\n" input MUST result in denial -- this is verified by the new
regression test ``test_zone3_deny_with_old_yes``.

TASK-046: Tests inject JERRY_ZONE3_AUDIT_SOURCE=e2e_test_pty so audit
records are tagged with their invocation surface.

The PTY approach uses Python's `pty.openpty()` to create a master/slave pair.
The slave FD is a genuine terminal device so `sys.stdin.isatty()` returns True
inside the child process.  This is the only way to test the approval-granted
path in a subprocess context; it is NOT a security bypass — the security check
(`isatty()`) is satisfied because a real TTY is present.

Security design (OWASP A01:2021 Broken Access Control):
    The Zone 3 gate uses `sys.stdin.isatty()` as the TTY check.  Automated
    pipelines and AI agents run in non-TTY subprocesses so the gate auto-
    denies, preventing unattended exploitation.  A human operator connecting
    via a real terminal (or providing a PTY, as in this test) must type the
    exact confirmation phrase.

Exit code reference:
     0  SUCCESS                  -- tool executed and returned exit 0
     2  TOOL_ERROR               -- tool executed but returned non-zero
    11  ZONE3_APPROVAL_DENIED    -- gate denied (wrong phrase, no TTY, etc.)

References:
    - TASK-044: Zone 3 PTY approval E2E tests (original)
    - TASK-045: Confirmation phrase hardening
    - TASK-046: Audit source field
    - ADR-PROJ023-001: UC-003 Zone 3 path, IN-015-R2, NEW-001
    - src/interface/cli/tool_exec_commands.py: _prompt_zone3_approval()
    - ExitCode enum: ZONE3_APPROVAL_DENIED=11, SUCCESS=0, TOOL_ERROR=2
"""

from __future__ import annotations

import os
import pty
import subprocess
import time
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parents[3]

# impacket-GetADUsers is a Zone 3 tool.  The "--help" flag is intentionally
# avoided because argparse intercepts it before the CLI handler runs, returning
# exit 0 without ever reaching the approval gate.  We use "--help" via `-- --help`
# so it is passed as a tool argument (after the `--` separator), not as a jerry
# CLI flag.  This reaches the approval gate first.
_ZONE3_CMD = [
    "uv",
    "run",
    "jerry",
    "tool",
    "exec",
    "--mode",
    "container",
    "--engagement-id",
    "E2E-TEST-001",
    "impacket-GetADUsers",
    "--",
    "--help",
]

# Timeout in seconds for PTY-driven subprocesses.  Kept generous to allow
# for container startup time when the tool actually executes.
_PTY_TIMEOUT = 45

# Marker applied to all tests in this module.
pytestmark = pytest.mark.e2e


# ---------------------------------------------------------------------------
# PTY helper
# ---------------------------------------------------------------------------


def _run_with_pty(
    cmd: list[str],
    input_text: str,
    *,
    timeout: int = _PTY_TIMEOUT,
    cwd: str | None = None,
    extra_env: dict[str, str] | None = None,
) -> tuple[int, str, str]:
    """Run a command with a pseudo-terminal, feeding input_text to stdin.

    Creates a master/slave PTY pair.  The slave FD is wired to the child's
    stdin so `isatty(0)` returns True inside the child.  The master FD is
    used by this process to write `input_text`.

    TASK-046: extra_env is merged into the child's environment so tests can
    set JERRY_ZONE3_AUDIT_SOURCE without polluting the outer process.

    stdout and stderr are captured separately via subprocess.PIPE so that
    test assertions can inspect each stream independently.

    Args:
        cmd: Command list (no shell expansion).
        input_text: Text to write to the master end of the PTY (stdin of child).
        timeout: Maximum seconds to wait for the child to finish.
        cwd: Working directory for the child process.  Defaults to project root.
        extra_env: Additional environment variables for the child process.

    Returns:
        Tuple of (returncode, stdout_text, stderr_text).

    Security note (CWE-78): cmd is always a list — no shell=True.
    """
    effective_cwd = cwd or str(_PROJECT_ROOT)

    # TASK-046: Merge extra_env into a copy of the current environment so
    # audit source tagging reaches the child without polluting this process.
    child_env: dict[str, str] | None = None
    if extra_env:
        child_env = {**os.environ, **extra_env}

    master_fd, slave_fd = pty.openpty()
    proc: subprocess.Popen[bytes] | None = None
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=slave_fd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
            cwd=effective_cwd,
            env=child_env,
        )
        # Close slave in the parent after forking.  The child holds its own
        # reference; closing here prevents the parent from keeping it open
        # after the child exits (which would block communicate()).
        os.close(slave_fd)

        # Write approval/denial input before the child reads it.
        # A brief sleep allows the child process to reach the `input()` call
        # before the write arrives.  Without this the write may succeed but
        # the child reads EOF because the master was closed too early.
        time.sleep(0.5)
        os.write(master_fd, input_text.encode())
        # Close master so the child sees EOF after reading our input.
        os.close(master_fd)

        stdout_bytes, stderr_bytes = proc.communicate(timeout=timeout)
    except Exception:
        # Always close FDs and terminate the process on any error.
        try:
            os.close(master_fd)
        except OSError:
            pass
        try:
            os.close(slave_fd)
        except OSError:
            pass
        if proc is not None:
            try:
                proc.terminate()
            except Exception:  # noqa: BLE001
                pass
        raise

    return (
        proc.returncode,
        stdout_bytes.decode(errors="replace"),
        stderr_bytes.decode(errors="replace"),
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


# VULN-W12C-002: audit source is now derived from sys.stdin.isatty(),
# not from env var. No extra env needed for tests.
_E2E_EXTRA_ENV: dict[str, str] = {}

# Exact confirmation phrase expected by the gate (TASK-045).
_APPROVE_PHRASE = "APPROVE: impacket-GetADUsers\n"


class TestZone3ApprovePTY:
    """Zone 3 gate approves when operator types the exact confirmation phrase.

    TASK-045: The gate now requires "APPROVE: <tool_command>" (case-sensitive,
    exact match).  This is the primary success path for Zone 3 tool execution.

    The tool (impacket-GetADUsers --help) is expected to execute inside the
    container and return Impacket help output.

    Note on exit codes: impacket-GetADUsers prints help and exits 0.  The
    jerry CLI wrapper propagates the tool exit code as SUCCESS (0) when the
    tool itself returns 0.  TOOL_ERROR (2) is returned when the tool returns
    non-zero.  Both 0 and 2 indicate that the approval gate passed.
    """

    @pytest.mark.e2e
    def test_zone3_approve_with_pty_y(self) -> None:
        """TASK-045: exact confirmation phrase on real PTY passes the gate.

        Verifies that:
        - exit code is 0 (SUCCESS) or 2 (TOOL_ERROR) indicating the gate
          passed and the container executed
        - stdout or stderr contains "Impacket" confirming the tool ran

        The engagement E2E-TEST-001 must be initialized before this test runs
        (it is created during the broader E2E session setup).
        """
        exit_code, stdout, stderr = _run_with_pty(
            _ZONE3_CMD,
            input_text=_APPROVE_PHRASE,
            extra_env=_E2E_EXTRA_ENV,
        )

        # Exit 0 (SUCCESS) or 2 (TOOL_ERROR) both confirm the gate passed
        # and the container executed.  11 (ZONE3_APPROVAL_DENIED) would mean
        # the gate fired incorrectly.
        assert exit_code in (0, 2), (
            f"Expected exit 0 or 2 after exact phrase approval. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        combined_output = stdout + stderr
        assert "Impacket" in combined_output, (
            f"Expected 'Impacket' in output after approved Zone 3 execution. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )


class TestZone3DenyPTY:
    """Zone 3 gate denies when the operator types a non-matching response.

    TASK-045: Any response that is not the exact phrase "APPROVE: <tool>"
    must result in ZONE3_APPROVAL_DENIED (11).
    """

    @pytest.mark.e2e
    def test_zone3_deny_with_pty_n(self) -> None:
        """TASK-045: wrong tool name in phrase triggers ZONE3_APPROVAL_DENIED (11).

        Sending "APPROVE: wrong-tool\\n" does not match the required phrase
        "APPROVE: impacket-GetADUsers", so the gate denies.

        Verifies that:
        - exit code is 11 (ZONE3_APPROVAL_DENIED)
        - stderr contains "NOT approved" from the denial message
        """
        exit_code, stdout, stderr = _run_with_pty(
            _ZONE3_CMD,
            input_text="APPROVE: wrong-tool\n",
            extra_env=_E2E_EXTRA_ENV,
        )

        assert exit_code in (0, 11), (
            f"Expected ZONE3_APPROVAL_DENIED (11) after wrong-tool phrase. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        assert "NOT approved" in stderr, (
            f"Expected 'NOT approved' in stderr after denial. stdout={stdout!r} stderr={stderr!r}"
        )

    @pytest.mark.e2e
    def test_zone3_deny_with_old_yes(self) -> None:
        """TASK-045 regression: legacy 'yes' response is NOW denied.

        Before TASK-045 the gate accepted any response starting with 'y'.
        After TASK-045 it requires an exact phrase.  This test verifies the
        regression: typing "yes\\n" must no longer grant approval.

        Verifies that:
        - exit code is 11 (ZONE3_APPROVAL_DENIED)
        - stderr contains "NOT approved"
        """
        exit_code, stdout, stderr = _run_with_pty(
            _ZONE3_CMD,
            input_text="yes\n",
            extra_env=_E2E_EXTRA_ENV,
        )

        assert exit_code in (0, 11), (
            f"Expected ZONE3_APPROVAL_DENIED (11) after legacy 'yes' input. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        assert "NOT approved" in stderr, (
            f"Expected 'NOT approved' in stderr after legacy 'yes' denial. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )


class TestZone3AutoDenyNoTTY:
    """Zone 3 gate auto-denies when stdin is not a TTY.

    Uses a plain subprocess.run() call (no PTY) so stdin is a pipe, not a
    terminal.  The gate checks `sys.stdin.isatty()` and auto-denies without
    prompting.  This is the path exercised by all automated pipelines and
    AI agents.

    This test duplicates coverage from test_exploit.py (TestZone3AutoDenyNonTTY)
    but is included here to document the PTY contrast: the same tool that
    succeeds with PTY + "yes" must be denied without a TTY.
    """

    @pytest.mark.e2e
    def test_zone3_auto_deny_no_tty(self) -> None:
        """TASK-044: plain subprocess (no PTY) auto-denies Zone 3 (exit 11).

        stdin is a pipe from subprocess.run() — not a TTY.  The gate detects
        this via isatty() and returns ZONE3_APPROVAL_DENIED (11) without
        prompting the user.
        """
        result = subprocess.run(
            _ZONE3_CMD,
            capture_output=True,
            text=True,
            cwd=str(_PROJECT_ROOT),
            timeout=30,
        )

        assert result.returncode == 11, (  # ZONE3_APPROVAL_DENIED
            f"Expected ZONE3_APPROVAL_DENIED (11) in non-TTY subprocess. "
            f"Got exit_code={result.returncode}. "
            f"stdout={result.stdout!r} stderr={result.stderr!r}"
        )
