# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""CLI handler for the jerry tool exec command.

Wires together the tool execution pipeline: family resolution, mode
resolution, execution (local or container), credential filtering,
evidence persistence, and engagement management.

References:
    - ADR-PROJ023-001: Rainbow Tool Executor Behavioral Contract
    - STORY-W12-001: Jerry tool exec CLI command
    - TASK-001: CLI subparser for jerry tool exec
"""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.tool_exec.domain.services.credential_filter import CredentialFilterService
from src.tool_exec.domain.services.engagement_initializer import (
    EngagementInitializer,
)
from src.tool_exec.domain.services.evidence_hasher import EvidenceHasher
from src.tool_exec.domain.services.family_router import FamilyRouterService
from src.tool_exec.domain.services.mode_resolver import ModeResolverService
from src.tool_exec.domain.value_objects.exit_codes import ExitCode
from src.tool_exec.infrastructure.adapters.container_executor import ContainerExecutor
from src.tool_exec.infrastructure.adapters.local_executor import LocalExecutor
from src.tool_exec.infrastructure.registry.family_registry_loader import (
    FamilyRegistryLoader,
)

logger = logging.getLogger(__name__)


def _validate_evidence_dir(evidence_dir_override: str, project_root: Path) -> Path:
    """Validate and canonicalize the --evidence-dir override path.

    FINDING-001 (CWE-22, High): The CLI --evidence-dir argument is user-supplied and
    must be canonicalized and contained within the project root before use. Without
    this check, an operator can pass relative traversal segments (../../tmp/exfil)
    or absolute out-of-tree paths that redirect evidence writes -- bypassing the
    engagement isolation model and the 0o700 quarantine permission protection.

    Canonicalization via .resolve() collapses symlinks and relative segments. The
    relative_to() check enforces project-root containment. Both steps are required:
    .resolve() alone does not reject an in-tree path; relative_to() alone does not
    handle symlinks or relative traversal.

    Args:
        evidence_dir_override: Raw --evidence-dir string from CLI arguments.
        project_root: Resolved project root path (the containment boundary).

    Returns:
        Resolved, canonicalized Path confirmed to be within project_root.

    Raises:
        ValueError: If the resolved path escapes the project root boundary.
    """
    resolved = Path(evidence_dir_override).resolve()
    try:
        resolved.relative_to(project_root.resolve())
    except ValueError as err:
        msg = (
            f"--evidence-dir '{evidence_dir_override}' resolves to '{resolved}', "
            f"which is outside the project root. "
            f"Evidence must be written under: {project_root}"
        )
        raise ValueError(msg) from err
    return resolved


def _find_project_root() -> Path:
    """Find the project root by walking up from cwd looking for .git or pyproject.toml.

    VF-002 mitigation: logs a warning when no project marker is found and
    the function falls back to cwd. This fallback weakens the --evidence-dir
    containment boundary (FINDING-001) because cwd in a CI ephemeral workspace
    or global installation may be a world-readable directory.

    Returns:
        Path to the project root directory.
    """
    current = Path.cwd()
    while current != current.parent:
        if (current / ".git").exists() or (current / "pyproject.toml").exists():
            return current
        current = current.parent
    logger.warning(
        "No .git or pyproject.toml found in parent directories. "
        "Falling back to cwd as project root: %s. "
        "Evidence containment boundary may be weaker than expected (VF-002).",
        Path.cwd(),
    )
    return Path.cwd()


def handle_tool_exec(args: Any) -> int:
    """Handle the jerry tool exec command.

    Orchestrates the full tool execution pipeline:
    1. Load family registry and resolve tool command
    2. Determine execution mode
    3. Check engagement requirements
    4. Execute tool (local or container)
    5. Apply credential filter
    6. Persist evidence
    7. Return exit code

    Args:
        args: Parsed argparse namespace with tool exec arguments.

    Returns:
        Exit code as integer.
    """
    tool_command = getattr(args, "tool_command", None)
    if tool_command is None:
        print("Error: No tool command specified. Use 'jerry tool exec --help'.")
        return ExitCode.UNKNOWN_TOOL

    tool_args = getattr(args, "tool_args", [])
    family = getattr(args, "family", None)
    cli_mode = getattr(args, "mode", None)
    engagement_id = getattr(args, "engagement_id", None)
    evidence_dir_override = getattr(args, "evidence_dir", None)
    init_engagement = getattr(args, "init_engagement", None)
    no_filter = getattr(args, "no_filter", False)
    health_check = getattr(args, "health_check", False)

    project_root = _find_project_root()

    # M-03 (T-06, DREAD 34, HIGH): Strict mode enforcement for --no-filter.
    # When JERRY_STRICT_MODE=true, --no-filter is FORBIDDEN. An AI agent
    # invoking `jerry tool exec --no-filter <tool>` would receive unfiltered
    # output including any credentials, bypassing all L1 credential protection.
    # OWASP A01:2021 Broken Access Control; NIST CSF PR.AC-1.
    if no_filter:
        strict_mode = os.environ.get("JERRY_STRICT_MODE", "true").lower()
        if strict_mode == "true":
            print(
                "Error: --no-filter is FORBIDDEN when JERRY_STRICT_MODE=true. "
                "Credential filtering cannot be disabled in strict mode. "
                "To allow --no-filter, set JERRY_STRICT_MODE=false (not recommended).",
                file=sys.stderr,
            )
            return ExitCode.STRICT_MODE_VIOLATION
        # Outside strict mode: log a warning but allow execution.
        logger.warning(
            "[SECURITY-WARN] --no-filter passed with JERRY_STRICT_MODE=%s. "
            "Credential filtering is DISABLED for this invocation. "
            "Tool output may contain credentials.",
            strict_mode,
        )

    # Handle --init-engagement before anything else
    if init_engagement:
        return _handle_init_engagement(init_engagement, project_root)

    # Load family registry
    registry_path = project_root / "tool_families.yaml"
    try:
        loader = FamilyRegistryLoader(registry_path)
        resolvers = loader.load()
    except FileNotFoundError:
        print(f"Error: Family registry not found: {registry_path}", file=sys.stderr)
        return ExitCode.UNKNOWN_TOOL
    except Exception as e:
        print(f"Error loading family registry: {e}", file=sys.stderr)
        return ExitCode.UNKNOWN_TOOL

    # Build family router
    router = FamilyRouterService(resolvers)

    # Resolve tool command
    try:
        resolution = router.resolve(tool_command, family=family)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return ExitCode.UNKNOWN_TOOL

    # Get security policy
    resolver = resolvers.get(resolution.family)
    if resolver is None:
        print(f"Error: Family '{resolution.family}' not found.", file=sys.stderr)
        return ExitCode.UNKNOWN_TOOL

    policy = resolver.security_policy(tool_command)

    # Resolve execution mode
    mode_resolver = ModeResolverService()
    try:
        config = resolver.load_config(
            str(project_root / "skills" / "rainbow" / "config" / "tool-exec.yaml")
        )
    except FileNotFoundError:
        config = {}
    config_mode = config.get("default_mode")
    try:
        mode = mode_resolver.resolve(cli_mode=cli_mode, config_mode=config_mode)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return ExitCode.MODE_UNSET

    # Handle --health-check
    if health_check:
        return _handle_health_check(resolution, project_root)

    # Check engagement requirements
    engagement_init = EngagementInitializer(base_dir=project_root / "work" / "engagements")
    if policy.requires_engagement:
        if engagement_id is None:
            print(
                f"Error: Tool '{tool_command}' ({resolution.zone}) requires "
                f"--engagement-id. Initialize with: "
                f"jerry tool exec --init-engagement <id>",
                file=sys.stderr,
            )
            return ExitCode.ENGAGEMENT_NOT_INIT
        if not engagement_init.is_initialized(engagement_id):
            print(
                f"Error: Engagement '{engagement_id}' not initialized. "
                f"Run: jerry tool exec --init-engagement {engagement_id}",
                file=sys.stderr,
            )
            return ExitCode.ENGAGEMENT_NOT_INIT

    # Set up credential filter
    credential_filter = CredentialFilterService()
    if policy.credential_filter_patterns:
        credential_filter.extend_patterns(policy.credential_filter_patterns)

    # Execute tool
    if mode == "container":
        result = _execute_container(
            tool_command=tool_command,
            tool_args=tool_args,
            resolution=resolution,
            credential_filter=credential_filter,
            project_root=project_root,
            no_filter=no_filter,
        )
    else:
        result = _execute_local(
            tool_command=tool_command,
            tool_args=tool_args,
            credential_filter=credential_filter,
            no_filter=no_filter,
        )

    # Persist evidence if engagement is active
    if engagement_id and not result.get("credential_detected", False):
        try:
            _persist_evidence(
                raw_output=result["raw_stdout"],
                filtered_output=result["stdout"],
                tool_command=tool_command,
                tool_args=tool_args,
                engagement_id=engagement_id,
                engagement_init=engagement_init,
                evidence_dir_override=evidence_dir_override,
                project_root=project_root,
            )
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return ExitCode.ENGAGEMENT_NOT_INIT

    # Handle credential quarantine
    if result.get("credential_detected", False) and engagement_id:
        _quarantine_output(
            raw_output=result["raw_stdout"],
            tool_command=tool_command,
            engagement_id=engagement_id,
            engagement_init=engagement_init,
            match_info=result.get("match_info"),
        )

    # Print output
    if result["stdout"]:
        print(result["stdout"])
    if result["stderr"]:
        print(result["stderr"], file=sys.stderr)

    return result["exit_code"]


def _handle_init_engagement(engagement_id: str, project_root: Path) -> int:
    """Initialize a new engagement directory.

    Args:
        engagement_id: The engagement identifier.
        project_root: Path to the project root.

    Returns:
        Exit code.
    """
    initializer = EngagementInitializer(base_dir=project_root / "work" / "engagements")
    try:
        path = initializer.initialize(engagement_id)
        print(f"Engagement initialized: {path}")
        return ExitCode.SUCCESS
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return ExitCode.ENGAGEMENT_NOT_INIT


def _handle_health_check(resolution: Any, project_root: Path) -> int:
    """Check container health for the resolved tool's service.

    Args:
        resolution: ToolResolutionEntry with container service info.
        project_root: Path to the project root.

    Returns:
        Exit code.
    """
    if not resolution.container_service or not resolution.compose_file:
        print("No container service configured for this tool.")
        return ExitCode.SUCCESS

    executor = ContainerExecutor(project_root=str(project_root))
    compose_path = str(project_root / resolution.compose_file)
    healthy = executor.health_check(
        service=resolution.container_service,
        compose_file=compose_path,
    )

    if healthy:
        print(f"Service '{resolution.container_service}' is running.")
        return ExitCode.SUCCESS
    else:
        print(
            f"Service '{resolution.container_service}' is NOT running.",
            file=sys.stderr,
        )
        return ExitCode.CONTAINER_NOT_RUNNING


def _execute_local(
    tool_command: str,
    tool_args: list[str],
    credential_filter: CredentialFilterService,
    no_filter: bool,
) -> dict[str, Any]:
    """Execute a tool locally.

    Args:
        tool_command: Tool binary name.
        tool_args: Tool arguments.
        credential_filter: Credential filter service.
        no_filter: Whether to skip filtering.

    Returns:
        Dictionary with execution results.
    """
    executor = LocalExecutor(credential_filter=credential_filter)
    result = executor.execute(
        tool_command=tool_command,
        tool_args=tool_args,
        no_filter=no_filter,
    )
    return {
        "exit_code": result.exit_code,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "raw_stdout": result.raw_stdout,
        "credential_detected": result.credential_detected,
        "match_info": (
            {
                "pattern": result.filter_result.match.pattern,
                "line_number": result.filter_result.match.line_number,
            }
            if result.filter_result and result.filter_result.match
            else None
        ),
    }


def _execute_container(
    tool_command: str,
    tool_args: list[str],
    resolution: Any,
    credential_filter: CredentialFilterService,
    project_root: Path,
    no_filter: bool,
) -> dict[str, Any]:
    """Execute a tool in a container.

    Args:
        tool_command: Tool binary name.
        tool_args: Tool arguments.
        resolution: ToolResolutionEntry with container metadata.
        credential_filter: Credential filter service.
        project_root: Path to the project root.
        no_filter: Whether to skip filtering.

    Returns:
        Dictionary with execution results.
    """
    executor = ContainerExecutor(
        credential_filter=credential_filter,
        project_root=str(project_root),
    )

    compose_path = None
    if resolution.compose_file:
        compose_path = str(project_root / resolution.compose_file)

    result = executor.execute(
        tool_command=tool_command,
        tool_args=tool_args,
        service=resolution.container_service or "",
        compose_file=compose_path,
        no_filter=no_filter,
    )

    return {
        "exit_code": result.exit_code,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "raw_stdout": result.raw_stdout,
        "credential_detected": result.credential_detected,
        "match_info": (
            {
                "pattern": result.filter_result.match.pattern,
                "line_number": result.filter_result.match.line_number,
            }
            if result.filter_result and result.filter_result.match
            else None
        ),
    }


def _persist_evidence(
    raw_output: str,
    filtered_output: str,
    tool_command: str,
    tool_args: list[str],
    engagement_id: str,
    engagement_init: EngagementInitializer,
    evidence_dir_override: str | None = None,
    project_root: Path | None = None,
) -> None:
    """Persist tool execution evidence with integrity hash.

    Args:
        raw_output: Original tool output.
        filtered_output: Output after credential filtering.
        tool_command: Tool command that was executed.
        tool_args: Tool arguments.
        engagement_id: Active engagement identifier.
        engagement_init: Engagement initializer service.
        evidence_dir_override: Optional override for evidence directory.
            FINDING-001 (CWE-22): When supplied, the path is canonicalized
            via .resolve() and verified to be within project_root before use.
        project_root: Project root path used as the containment boundary for
            evidence_dir_override validation. Required when evidence_dir_override
            is provided; defaults to cwd if not supplied.

    Raises:
        ValueError: If evidence_dir_override resolves outside project_root.
    """
    hasher = EvidenceHasher()

    if evidence_dir_override:
        # FINDING-001 (CWE-22, High): Canonicalize and enforce project-root
        # containment before creating or writing to the directory.
        # _validate_evidence_dir() calls Path.resolve() to collapse symlinks and
        # relative segments, then asserts relative_to(project_root) containment.
        effective_root = project_root if project_root is not None else Path.cwd()
        evidence_dir = _validate_evidence_dir(evidence_dir_override, effective_root)
        evidence_dir.mkdir(parents=True, exist_ok=True)
    else:
        evidence_dir = engagement_init.evidence_dir(engagement_id)

    ts = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
    evidence_file = evidence_dir / f"evidence-{engagement_id}-{ts}.txt"
    meta_file = evidence_dir / f"evidence-{engagement_id}-{ts}.meta.json"

    evidence_file.write_text(filtered_output, encoding="utf-8")

    meta = {
        "timestamp": ts,
        "engagement_id": engagement_id,
        "tool_command": tool_command,
        "tool_args": tool_args,
        "sha256_raw": hasher.hash_string(raw_output),
        "sha256_filtered": hasher.hash_string(filtered_output),
        "evidence_file": str(evidence_file),
    }
    meta_file.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


def _quarantine_output(
    raw_output: str,
    tool_command: str,
    engagement_id: str,
    engagement_init: EngagementInitializer,
    match_info: dict[str, Any] | None = None,
) -> None:
    """Quarantine output that triggered the credential filter.

    Args:
        raw_output: Original unfiltered output.
        tool_command: Tool command that produced the output.
        engagement_id: Active engagement identifier.
        engagement_init: Engagement initializer service.
        match_info: Details about the credential match.
    """
    hasher = EvidenceHasher()
    quarantine_dir = engagement_init.quarantine_dir(engagement_id)
    quarantine_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
    quarantine_file = quarantine_dir / f"quarantine-{engagement_id}-{ts}.txt"
    meta_file = quarantine_dir / f"quarantine-{engagement_id}-{ts}.meta.json"

    quarantine_file.write_text(raw_output, encoding="utf-8")

    meta: dict[str, Any] = {
        "timestamp": ts,
        "engagement_id": engagement_id,
        "tool_command": tool_command,
        "detecting_layer": "L1-regex",
        "sha256_raw": hasher.hash_string(raw_output),
        "quarantine_file": str(quarantine_file),
    }
    if match_info:
        meta["matched_pattern"] = match_info.get("pattern", "")
        meta["detected_at_line"] = match_info.get("line_number", 0)

    meta_file.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(
        f"[CREDENTIAL-FILTER] Output quarantined to: {quarantine_file}",
        file=sys.stderr,
    )
