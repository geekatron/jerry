# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Local executor for running tools via subprocess.

Executes tools directly on the host system using subprocess.run,
capturing stdout and stderr. Applies credential filtering and
evidence persistence via the domain services.

References:
    - ADR-PROJ023-001: Local Execution Mode
    - TASK-004: LocalExecutor
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.tool_exec.domain.services.credential_filter import (
        CredentialFilterService,
        FilterResult,
    )


@dataclass
class ExecutionResult:
    """Result of executing a tool command.

    Attributes:
        exit_code: The process exit code.
        stdout: Captured standard output (may be filtered).
        stderr: Captured standard error.
        raw_stdout: Original unfiltered stdout.
        credential_detected: Whether the credential filter triggered.
        filter_result: Full credential filter result, or None if not applied.
    """

    exit_code: int
    stdout: str
    stderr: str
    raw_stdout: str
    credential_detected: bool = False
    filter_result: FilterResult | None = None


class LocalExecutor:
    """Executes tools locally via subprocess.

    Runs tool commands as child processes, captures their output, and
    applies the credential filter to stdout before returning results.
    Stderr is passed through unfiltered for debugging purposes.
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

        Args:
            tool_command: The tool binary name or path.
            tool_args: Optional list of arguments to pass to the tool.
            timeout: Maximum execution time in seconds. None for no limit.
            no_filter: If True, skip credential filtering on the output.

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
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                exit_code=2,
                stdout="",
                stderr=f"Tool execution timed out after {timeout}s: {tool_command}",
                raw_stdout="",
            )

        raw_stdout = result.stdout

        # Apply credential filter
        if self._credential_filter is not None and not no_filter:
            filter_result = self._credential_filter.filter_output(raw_stdout)
            return ExecutionResult(
                exit_code=4 if filter_result.detected else result.returncode,
                stdout=filter_result.filtered_output,
                stderr=result.stderr,
                raw_stdout=raw_stdout,
                credential_detected=filter_result.detected,
                filter_result=filter_result,
            )

        return ExecutionResult(
            exit_code=result.returncode,
            stdout=raw_stdout,
            stderr=result.stderr,
            raw_stdout=raw_stdout,
        )
