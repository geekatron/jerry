# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Container executor for running tools via Docker Compose.

Executes tools inside Docker containers using `docker compose exec`,
providing isolation for security-sensitive operations. Applies the same
credential filter and evidence pipeline as the local executor.

References:
    - ADR-PROJ023-001: Container Execution Mode
    - TASK-005: ContainerExecutor
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
class ContainerExecutionResult:
    """Result of executing a tool command in a container.

    Attributes:
        exit_code: The process exit code.
        stdout: Captured standard output (may be filtered).
        stderr: Captured standard error (may be filtered).
        raw_stdout: Original unfiltered stdout.
        raw_stderr: Original unfiltered stderr.
            FINDING-004 (CWE-200): Introduced so that both streams can be
            quarantined when a credential is detected in either one.
        credential_detected: Whether the credential filter triggered on either stream.
        filter_result: Full credential filter result for stdout, or None if not applied.
        container_service: The Docker Compose service that ran the command.
    """

    exit_code: int
    stdout: str
    stderr: str
    raw_stdout: str
    raw_stderr: str = ""
    credential_detected: bool = False
    filter_result: FilterResult | None = None
    container_service: str = ""


class ContainerExecutor:
    """Executes tools inside Docker containers via docker compose exec.

    Constructs the docker compose exec command with the appropriate
    compose file, service name, and exec flags (-T for non-interactive).
    """

    def __init__(
        self,
        credential_filter: CredentialFilterService | None = None,
        project_root: str | None = None,
    ) -> None:
        """Initialize the container executor.

        Args:
            credential_filter: Optional credential filter service.
            project_root: Path to the project root for compose file resolution.
                If None, compose files are treated as relative to cwd.
        """
        self._credential_filter = credential_filter
        self._project_root = project_root

    def execute(
        self,
        tool_command: str,
        tool_args: list[str] | None = None,
        service: str = "",
        compose_file: str | None = None,
        timeout: int | None = 300,
        no_filter: bool = False,
        exec_flags: list[str] | None = None,
    ) -> ContainerExecutionResult:
        """Execute a tool command inside a Docker container.

        Constructs and runs:
            docker compose -f <compose_file> exec <flags> <service> <tool> <args>

        Args:
            tool_command: The tool binary to execute inside the container.
            tool_args: Optional arguments to pass to the tool.
            service: Docker Compose service name.
            compose_file: Path to docker-compose.yml, relative to project root.
            timeout: Maximum execution time in seconds.
            no_filter: If True, skip credential filtering.
            exec_flags: Additional docker compose exec flags (e.g., ['-T']).

        Returns:
            ContainerExecutionResult with captured output and exit code.
        """
        cmd = self._build_command(
            tool_command=tool_command,
            tool_args=tool_args or [],
            service=service,
            compose_file=compose_file,
            exec_flags=exec_flags or ["-T"],
        )

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except FileNotFoundError:
            return ContainerExecutionResult(
                exit_code=3,
                stdout="",
                stderr="docker compose not found. Is Docker installed?",
                raw_stdout="",
                raw_stderr="",
                container_service=service,
            )
        except subprocess.TimeoutExpired:
            return ContainerExecutionResult(
                exit_code=2,
                stdout="",
                stderr=f"Container execution timed out after {timeout}s",
                raw_stdout="",
                raw_stderr="",
                container_service=service,
            )

        raw_stdout = result.stdout
        raw_stderr = result.stderr

        # Check if container is not running (common docker compose exec error)
        if result.returncode != 0 and "is not running" in raw_stderr.lower():
            return ContainerExecutionResult(
                exit_code=3,
                stdout="",
                stderr=raw_stderr,
                raw_stdout="",
                raw_stderr=raw_stderr,
                container_service=service,
            )

        # FINDING-004 (CWE-200, Medium): Apply credential filter to BOTH stdout and
        # stderr. Container tools may write sensitive material to stderr. If either
        # stream triggers the filter, both streams are quarantined and exit code 4 is
        # returned. Mirrors the fix applied to LocalExecutor.
        if self._credential_filter is not None and not no_filter:
            stdout_filter_result = self._credential_filter.filter_output(raw_stdout)
            stderr_filter_result = self._credential_filter.filter_output(raw_stderr)
            detected = stdout_filter_result.detected or stderr_filter_result.detected
            return ContainerExecutionResult(
                exit_code=4 if detected else result.returncode,
                stdout=stdout_filter_result.filtered_output,
                stderr=stderr_filter_result.filtered_output,
                raw_stdout=raw_stdout,
                raw_stderr=raw_stderr,
                credential_detected=detected,
                filter_result=stdout_filter_result,
                container_service=service,
            )

        return ContainerExecutionResult(
            exit_code=result.returncode,
            stdout=raw_stdout,
            stderr=raw_stderr,
            raw_stdout=raw_stdout,
            raw_stderr=raw_stderr,
            container_service=service,
        )

    def health_check(
        self,
        service: str,
        compose_file: str | None = None,
    ) -> bool:
        """Check whether a container service is running.

        Args:
            service: Docker Compose service name.
            compose_file: Path to docker-compose.yml.

        Returns:
            True if the service is running, False otherwise.
        """
        cmd = ["docker", "compose"]
        if compose_file:
            cmd.extend(["-f", compose_file])
        cmd.extend(["ps", "--status=running", "--format", "{{.Service}}", service])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return service in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _build_command(
        self,
        tool_command: str,
        tool_args: list[str],
        service: str,
        compose_file: str | None,
        exec_flags: list[str],
    ) -> list[str]:
        """Build the docker compose exec command.

        Args:
            tool_command: Tool binary name.
            tool_args: Tool arguments.
            service: Docker Compose service name.
            compose_file: Path to compose file.
            exec_flags: Flags for docker compose exec.

        Returns:
            Complete command as a list of strings.
        """
        cmd = ["docker", "compose"]

        if compose_file:
            cmd.extend(["-f", compose_file])

        cmd.append("exec")
        cmd.extend(exec_flags)
        cmd.append(service)
        cmd.append(tool_command)
        cmd.extend(tool_args)

        return cmd
