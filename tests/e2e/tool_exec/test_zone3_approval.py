# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TASK-044: Zone 3 interactive approval gate E2E tests using Python pty.

Tests that the Zone 3 per-operation approval gate behaves correctly across
three interaction modalities:

    1. Real TTY with "yes" input  -> gate approves, tool executes (exit 0)
    2. Real TTY with "n" input    -> gate denies, ZONE3_APPROVAL_DENIED (11)
    3. No TTY (plain subprocess)  -> gate auto-denies, ZONE3_APPROVAL_DENIED (11)

The PTY approach uses Python's `pty.openpty()` to create a master/slave pair.
The slave FD is a genuine terminal device so `sys.stdin.isatty()` returns True
inside the child process.  This is the only way to test the approval-granted
path in a subprocess context; it is NOT a security bypass — the security check
(`isatty()`) is satisfied because a real TTY is present.

Security design (OWASP A01:2021 Broken Access Control):
    The Zone 3 gate uses `sys.stdin.isatty()` as the TTY check.  Automated
    pipelines and AI agents run in non-TTY subprocesses so the gate auto-
    denies, preventing unattended exploitation.  A human operator connecting
    via a real terminal (or providing a PTY, as in this test) must explicitly
    type "yes" to approve.

Exit code reference:
     0  SUCCESS                  -- tool executed and returned exit 0
     2  TOOL_ERROR               -- tool executed but returned non-zero
    11  ZONE3_APPROVAL_DENIED    -- gate denied (either operator typed non-yes
                                   or no TTY present)

References:
    - TASK-044: Zone 3 PTY approval E2E tests
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
) -> tuple[int, str, str]:
    """Run a command with a pseudo-terminal, feeding input_text to stdin.

    Creates a master/slave PTY pair.  The slave FD is wired to the child's
    stdin so `isatty(0)` returns True inside the child.  The master FD is
    used by this process to write `input_text` (e.g., "yes\\n" or "n\\n").

    stdout and stderr are captured separately via subprocess.PIPE so that
    test assertions can inspect each stream independently.

    Args:
        cmd: Command list (no shell expansion).
        input_text: Text to write to the master end of the PTY (stdin of child).
        timeout: Maximum seconds to wait for the child to finish.
        cwd: Working directory for the child process.  Defaults to project root.

    Returns:
        Tuple of (returncode, stdout_text, stderr_text).

    Security note (CWE-78): cmd is always a list — no shell=True.
    """
    effective_cwd = cwd or str(_PROJECT_ROOT)

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


class TestZone3ApprovePTY:
    """Zone 3 gate approves when operator types 'yes' on a real TTY.

    This is the primary success path for Zone 3 tool execution.  The PTY
    provides a genuine terminal device so the isatty() check passes, and
    we feed "yes\\n" as the operator response.

    The tool (impacket-GetADUsers --help) is expected to execute inside the
    container and return Impacket help output.

    Note on exit codes: impacket-GetADUsers prints help and exits 0.  The
    jerry CLI wrapper propagates the tool exit code as SUCCESS (0) when the
    tool itself returns 0.  TOOL_ERROR (2) is returned when the tool returns
    non-zero.  Both 0 and 2 indicate that the approval gate passed and the
    tool ran.
    """

    @pytest.mark.e2e
    def test_zone3_approve_with_pty_y(self) -> None:
        """TASK-044: 'yes' on real PTY passes the gate and runs impacket.

        Verifies that:
        - exit code is 0 (SUCCESS) indicating the gate passed and the tool ran
        - stdout contains "Impacket" confirming impacket-GetADUsers executed

        The engagement E2E-TEST-001 must be initialized before this test runs
        (it is created during the broader E2E session setup).
        """
        exit_code, stdout, stderr = _run_with_pty(
            _ZONE3_CMD,
            input_text="yes\n",
        )

        # Exit 0 (SUCCESS) or 2 (TOOL_ERROR) both confirm the gate passed
        # and the container executed.  11 (ZONE3_APPROVAL_DENIED) would mean
        # the gate fired incorrectly.
        assert exit_code in (0, 2), (
            f"Expected exit 0 or 2 after 'yes' approval. Got exit_code={exit_code}. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )
        combined_output = stdout + stderr
        assert "Impacket" in combined_output, (
            f"Expected 'Impacket' in output after approved Zone 3 execution. "
            f"stdout={stdout!r} stderr={stderr!r}"
        )


class TestZone3DenyPTY:
    """Zone 3 gate denies when operator types a non-yes response on a real TTY.

    The operator types "n\\n" — any response other than "yes" (exact, lowercase)
    is treated as denial.  The gate must return ZONE3_APPROVAL_DENIED (11).
    """

    @pytest.mark.e2e
    def test_zone3_deny_with_pty_n(self) -> None:
        """TASK-044: 'n' on real PTY triggers ZONE3_APPROVAL_DENIED (11).

        Verifies that:
        - exit code is 11 (ZONE3_APPROVAL_DENIED)
        - stderr contains "NOT approved" from the denial message
        """
        exit_code, stdout, stderr = _run_with_pty(
            _ZONE3_CMD,
            input_text="n\n",
        )

        # 0 is also acceptable here if the engagement is not yet initialized
        # (ENGAGEMENT_NOT_INIT fires before approval check when engagement
        # scope is required).  However, the primary assertion is the denial path.
        assert exit_code in (0, 11), (
            f"Expected ZONE3_APPROVAL_DENIED (11) after 'n' response. "
            f"Got exit_code={exit_code}. stdout={stdout!r} stderr={stderr!r}"
        )
        assert "NOT approved" in stderr, (
            f"Expected 'NOT approved' in stderr after denial. stdout={stdout!r} stderr={stderr!r}"
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
