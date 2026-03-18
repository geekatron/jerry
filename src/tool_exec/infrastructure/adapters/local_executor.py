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
from src.tool_exec.domain.value_objects.exit_codes import ExitCode

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
        credential_filter: CredentialFilterService,
    ) -> None:
        """Initialize the local executor.

        IN-017-R2: credential_filter is now a required parameter. Removing the
        ``= None`` default closes the bypass path where a caller could
        instantiate LocalExecutor without a filter and silently skip all
        credential detection. The composition root MUST supply a
        CredentialFilterService instance; there is no legitimate use case for
        filterless local execution in production.

        Args:
            credential_filter: Credential filter service applied to both stdout
                and stderr. Required -- no default (IN-017-R2).
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
        #
        # IN-017-R2: credential_filter is now required, so no is-None guard needed.
        # PM-003-R2 / FIX-10: Wrap filter_output() in try/except RuntimeError so
        # that strict-mode violations surface as STRICT_MODE_VIOLATION (9) rather
        # than propagating an unhandled exception to the caller.
        try:
            stdout_filter_result = self._credential_filter.filter_output(
                raw_stdout, no_filter=no_filter
            )
            stderr_filter_result = self._credential_filter.filter_output(
                raw_stderr, no_filter=no_filter
            )
        except RuntimeError:
            # PM-003-R2: no_filter=True with strict_mode=True raises RuntimeError.
            # Convert to STRICT_MODE_VIOLATION so the CLI can return exit code 9.
            return ExecutionResult(
                exit_code=int(ExitCode.STRICT_MODE_VIOLATION),
                stdout="",
                stderr="[CREDENTIAL-FILTER] Strict mode violation: --no-filter forbidden.",
                raw_stdout=raw_stdout,
                raw_stderr=raw_stderr,
            )

        detected = stdout_filter_result.detected or stderr_filter_result.detected
        # FIX-17: Normalize non-zero tool exit codes to TOOL_ERROR (2)
        # to comply with BC-01/BC-02. Exit code 4 overrides when credential
        # detected; otherwise tool errors map to exit code 2 (TOOL_ERROR).
        if detected:
            exit_code = int(ExitCode.CREDENTIAL_DETECTED)
        elif result.returncode != 0:
            exit_code = int(ExitCode.TOOL_ERROR)
        else:
            exit_code = int(ExitCode.SUCCESS)
        # RT-R2-004: Use the detecting stream's filter_result for match_info.
        # If stderr triggered detection, use stderr_filter_result so the pattern
        # and line_number in the quarantine record point to the actual match.
        detecting_filter_result = (
            stderr_filter_result if stderr_filter_result.detected else stdout_filter_result
        )
        return ExecutionResult(
            exit_code=exit_code,
            stdout=stdout_filter_result.filtered_output,
            stderr=stderr_filter_result.filtered_output,
            raw_stdout=raw_stdout,
            raw_stderr=raw_stderr,
            credential_detected=detected,
            filter_result=detecting_filter_result,
        )
