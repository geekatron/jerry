# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Container executor for running tools via Docker Compose.

Executes tools inside Docker containers using `docker compose exec`,
providing isolation for security-sensitive operations. Applies the same
credential filter and evidence pipeline as the local executor.

References:
    - ADR-PROJ023-001: Container Execution Mode
    - TASK-005: ContainerExecutor
    - CC-001: H-10 one-class-per-file (ContainerExecutionResult extracted)
"""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

from src.tool_exec.domain.value_objects.container_execution_result import (
    ContainerExecutionResult,
)
from src.tool_exec.domain.value_objects.exit_codes import ExitCode

if TYPE_CHECKING:
    from src.tool_exec.domain.services.credential_filter import (
        CredentialFilterService,
    )


class ContainerExecutor:
    """Executes tools inside Docker containers via docker compose exec.

    Constructs the docker compose exec command with the appropriate
    compose file, service name, and exec flags (-T for non-interactive).
    """

    def __init__(
        self,
        credential_filter: CredentialFilterService,
        project_root: str | None = None,
    ) -> None:
        """Initialize the container executor.

        IN-017-R2: credential_filter is now a required parameter. Removing the
        ``= None`` default closes the bypass path where a caller could
        instantiate ContainerExecutor without a filter and silently skip all
        credential detection. The composition root MUST supply a
        CredentialFilterService instance.

        Args:
            credential_filter: Credential filter service applied to both stdout
                and stderr. Required -- no default (IN-017-R2).
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
        strict_mode: bool = True,
        proxy_env: dict[str, str] | None = None,
    ) -> ContainerExecutionResult:
        """Execute a tool command inside a Docker container.

        Constructs and runs:
            docker compose -f <compose_file> exec <flags> <service> <tool> <args>

        FIX-R3-1 (PM-001-R3): strict_mode is now threaded from the CLI handler
        so the resolved JERRY_STRICT_MODE value is honoured by the executor.
        Previously the executor always called filter_output(strict_mode=True)
        using the hard-coded default, meaning JERRY_STRICT_MODE=false + --no-filter
        would pass the CLI guard but the executor would still raise RuntimeError.

        Args:
            tool_command: The tool binary to execute inside the container.
            tool_args: Optional arguments to pass to the tool.
            service: Docker Compose service name.
            compose_file: Path to docker-compose.yml, relative to project root.
            timeout: Maximum execution time in seconds.
            no_filter: If True, skip credential filtering.
                FORBIDDEN when strict_mode=True (PM-002, FIX-13).
            exec_flags: Additional docker compose exec flags (e.g., ['-T']).
            strict_mode: Whether strict mode is active. Injected by the CLI
                handler from the resolved JERRY_STRICT_MODE env var. When True
                and no_filter=True, filter_output raises RuntimeError (PM-002).
                Default True to keep safe behaviour when called without the CLI.
            proxy_env: Optional dict of proxy environment variables to inject
                into the container via ``docker compose exec -e``. T13-022:
                Used to pass Envoy proxy config (HTTP_PROXY, HTTPS_PROXY,
                NO_PROXY) dynamically per engagement scope. When None, the
                container uses whatever proxy env is defined in the compose file.

        Note (DA-R4-002): This executor does NOT enforce Zone 3 security policy
            gates (approval, container requirement, engagement scope). Those gates
            live in the CLI handler (tool_exec_commands.py). Direct callers of this
            method are responsible for enforcing security policy before execution.

        Returns:
            ContainerExecutionResult with captured output and exit code.
        """
        cmd = self._build_command(
            tool_command=tool_command,
            tool_args=tool_args or [],
            service=service,
            compose_file=compose_file,
            exec_flags=exec_flags or ["-T"],
            proxy_env=proxy_env,
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
        #
        # IN-017-R2: credential_filter is now required, so no is-None guard needed.
        # PM-003-R2 / FIX-10: Wrap filter_output() in try/except RuntimeError so
        # that strict-mode violations surface as STRICT_MODE_VIOLATION (9).
        try:
            stdout_filter_result = self._credential_filter.filter_output(
                raw_stdout, no_filter=no_filter, strict_mode=strict_mode
            )
            stderr_filter_result = self._credential_filter.filter_output(
                raw_stderr, no_filter=no_filter, strict_mode=strict_mode
            )
        except RuntimeError:
            return ContainerExecutionResult(
                exit_code=int(ExitCode.STRICT_MODE_VIOLATION),
                stdout="",
                stderr="[CREDENTIAL-FILTER] Strict mode violation: --no-filter forbidden.",
                raw_stdout=raw_stdout,
                raw_stderr=raw_stderr,
                container_service=service,
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
        detecting_filter_result = (
            stderr_filter_result if stderr_filter_result.detected else stdout_filter_result
        )
        return ContainerExecutionResult(
            exit_code=exit_code,
            stdout=stdout_filter_result.filtered_output,
            stderr=stderr_filter_result.filtered_output,
            raw_stdout=raw_stdout,
            raw_stderr=raw_stderr,
            credential_detected=detected,
            filter_result=detecting_filter_result,
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
        proxy_env: dict[str, str] | None = None,
    ) -> list[str]:
        """Build the docker compose exec command.

        T13-022: When proxy_env is provided, injects ``-e KEY=VALUE`` flags
        into the ``docker compose exec`` command. These override the container's
        environment variables for that execution only, allowing per-engagement
        Envoy proxy configuration without modifying the compose file.

        The ``-e`` flags are placed AFTER exec_flags but BEFORE the service
        name, matching docker compose exec's option parsing order.

        Args:
            tool_command: Tool binary name.
            tool_args: Tool arguments.
            service: Docker Compose service name.
            compose_file: Path to compose file.
            exec_flags: Flags for docker compose exec.
            proxy_env: Optional proxy env vars to inject via ``-e``.

        Returns:
            Complete command as a list of strings.
        """
        cmd = ["docker", "compose"]

        if compose_file:
            cmd.extend(["-f", compose_file])

        cmd.append("exec")

        # VULN-002 mitigation: Reject caller-supplied exec_flags that contain
        # -e or --env, which could override proxy settings or inject arbitrary
        # environment variables into the container execution context.
        for flag in exec_flags:
            if flag in ("-e", "--env") or flag.startswith("-e=") or flag.startswith("--env="):
                msg = (
                    f"exec_flags cannot contain environment variable flags ({flag}). "
                    f"Use proxy_env parameter instead."
                )
                raise ValueError(msg)
        cmd.extend(exec_flags)

        # T13-022: Inject proxy environment variables via -e flags.
        # These override the compose-file-defined env vars for this execution.
        # Proxy env values are derived from _ZONE_PROXY_MAP constants in the
        # CLI handler (VULN-001 mitigation: never from user input).
        if proxy_env:
            for key, value in sorted(proxy_env.items()):
                cmd.extend(["-e", f"{key}={value}"])

        cmd.append(service)
        cmd.append(tool_command)
        cmd.extend(tool_args)

        return cmd
