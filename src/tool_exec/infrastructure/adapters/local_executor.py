# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Local executor for running tools via subprocess.

Executes tools directly on the host system using subprocess.run,
capturing stdout and stderr. Applies credential filtering to both
stdout and stderr via the domain services.

References:
    - ADR-PROJ023-001: Local Execution Mode
    - TASK-004: LocalExecutor
    - CC-001: H-10 one-class-per-file (ExecutionResult extracted)
    - SR-004: FIX-14 -- docstring corrected; stderr IS filtered (FINDING-004)
"""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

from src.tool_exec.domain.value_objects.execution_result import ExecutionResult

if TYPE_CHECKING:
    from src.tool_exec.domain.services.credential_filter import (
        CredentialFilterService,
    )


class LocalExecutor:
    """Executes tools locally via subprocess.

    Runs tool commands as child processes, captures their output, and
    applies the credential filter to both stdout and stderr before returning
    results. If either stream contains a credential, both streams are
    quarantined and exit code 4 (CREDENTIAL_DETECTED) is returned.

    SR-004 (FIX-14): Both stdout and stderr are filtered. The previous
    docstring incorrectly stated stderr was passed through unfiltered.
    """

    def __init__(
        self,
        credential_filter: CredentialFilterService | None = None,
    ) -> None:
        """Initialize the local executor.

        Args:
            credential_filter: Optional credential filter service. If None,
                no filtering is applied to tool output.
        """
        self._credential_filter = credential_filter

    def execute(
        self,
        tool_command: str,
        tool_args: list[str] | None = None,
        timeout: int | None = 300,
        no_filter: bool = False,
    ) -> ExecutionResult:
        """Execute a tool command locally via subprocess.

        Both stdout and stderr are filtered through the credential filter.
        If either stream triggers detection, both streams are redacted
        (FINDING-004, CWE-200) and exit code 4 (CREDENTIAL_DETECTED) is
        returned.

        Args:
            tool_command: The tool binary name or path.
            tool_args: Optional list of arguments to pass to the tool.
            timeout: Maximum execution time in seconds. None for no limit.
            no_filter: If True, skip credential filtering on the output.
                FORBIDDEN when JERRY_STRICT_MODE=true (PM-002, FIX-13).

        Returns:
            ExecutionResult with captured output and exit code.
        """
        cmd = [tool_command] + (tool_args or [])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except FileNotFoundError:
            return ExecutionResult(
                exit_code=1,
                stdout="",
                stderr=f"Tool not found: {tool_command}",
                raw_stdout="",
                raw_stderr="",
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                exit_code=2,
                stdout="",
                stderr=f"Tool execution timed out after {timeout}s: {tool_command}",
                raw_stdout="",
                raw_stderr="",
            )

        raw_stdout = result.stdout
        raw_stderr = result.stderr

        # FINDING-004 (CWE-200, Medium): Apply credential filter to BOTH stdout and
        # stderr. Security tools (Metasploit, Impacket, pwntools) routinely write
        # credentials, session tokens, and key material to stderr. Filtering only
        # stdout allowed credential-bearing stderr to bypass the L1 regex filter,
        # the quarantine pipeline, and the CREDENTIAL_DETECTED (exit code 4) signal.
        # If either stream triggers the filter, both streams are quarantined and the
        # exit code is set to 4 (CREDENTIAL_DETECTED).
        if self._credential_filter is not None and not no_filter:
            stdout_filter_result = self._credential_filter.filter_output(raw_stdout)
            stderr_filter_result = self._credential_filter.filter_output(raw_stderr)
            detected = stdout_filter_result.detected or stderr_filter_result.detected
            # FIX-17: Normalize non-zero tool exit codes to TOOL_ERROR (2)
            # to comply with BC-01/BC-02. Exit code 4 overrides when credential
            # detected; otherwise tool errors map to exit code 2 (TOOL_ERROR).
            if detected:
                exit_code = 4
            elif result.returncode != 0:
                exit_code = 2
            else:
                exit_code = 0
            return ExecutionResult(
                exit_code=exit_code,
                stdout=stdout_filter_result.filtered_output,
                stderr=stderr_filter_result.filtered_output,
                raw_stdout=raw_stdout,
                raw_stderr=raw_stderr,
                credential_detected=detected,
                filter_result=stdout_filter_result,
            )

        return ExecutionResult(
            exit_code=result.returncode,
            stdout=raw_stdout,
            stderr=raw_stderr,
            raw_stdout=raw_stdout,
            raw_stderr=raw_stderr,
        )
