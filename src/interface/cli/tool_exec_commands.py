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
    - FIX-1 (DA-002/CV-005): quarantine_output wired; inline redaction in filter
    - FIX-2 (FM-032): Zone 3 approval gate enforced before execution
    - FIX-3 (FM-002): Zone 3 container enforcement -- local mode rejected
    - FIX-4 (RT-001): Strict-mode bypass via empty env var closed
    - FIX-7 (CV-013): --list-families and --list-tools management commands
    - FIX-8 (RT-003/SR-003): Quarantine file chmod 0o600 after write
    - FIX-9 (CC-002): Service instantiation via create_tool_exec_handler() factory
    - FIX-11 (SR-001): Config path from registry, not hardcoded
    - FIX-12 (IN-009): ModeResolverService receives family env_var_prefix
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


# ---------------------------------------------------------------------------
# FIX-9 (CC-002): Composition root factory
# ---------------------------------------------------------------------------


def create_tool_exec_handler(project_root: Path) -> dict[str, Any]:
    """Composition root factory for the tool exec pipeline services.

    Instantiates and wires together all services required for tool execution.
    Separates service construction from the CLI handler logic, following the
    Dependency Inversion Principle and the composition root pattern (CC-002).

    Args:
        project_root: Resolved project root path used to locate registries
            and engagement directories.

    Returns:
        Mapping of service name to instance:
            - 'loader': FamilyRegistryLoader
            - 'engagement_init': EngagementInitializer
            - 'credential_filter': CredentialFilterService
    """
    registry_path = project_root / "tool_families.yaml"
    return {
        "loader": FamilyRegistryLoader(registry_path),
        "engagement_init": EngagementInitializer(base_dir=project_root / "work" / "engagements"),
        "credential_filter": CredentialFilterService(),
    }


# ---------------------------------------------------------------------------
# Input validation helpers
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Main CLI handler
# ---------------------------------------------------------------------------


def handle_tool_exec(args: Any) -> int:
    """Handle the jerry tool exec command.

    Orchestrates the full tool execution pipeline:
    1. Load family registry and resolve tool command
    2. Determine execution mode
    3. Check security policy gates (Zone 3 approval, container enforcement)
    4. Check engagement requirements
    5. Execute tool (local or container)
    6. Apply credential filter
    7. Persist evidence (or quarantine credential-bearing output)
    8. Return exit code

    Args:
        args: Parsed argparse namespace with tool exec arguments.

    Returns:
        Exit code as integer.
    """
    # Check for management commands first (FIX-7: --list-families, --list-tools)
    list_families = getattr(args, "list_families", False)
    list_tools = getattr(args, "list_tools", None)
    if list_families or list_tools:
        return _handle_management_command(args)

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

    # FIX-4 (RT-001): Strict-mode bypass via empty env var closed.
    # Only explicitly "false", "0", or "no" disables strict mode.
    # Empty string, unset, or any other value keeps strict mode ON.
    # M-03 (T-06, DREAD 34, HIGH): Strict mode enforcement for --no-filter.
    # When JERRY_STRICT_MODE is true, --no-filter is FORBIDDEN. An AI agent
    # invoking `jerry tool exec --no-filter <tool>` would receive unfiltered
    # output including any credentials, bypassing all L1 credential protection.
    # OWASP A01:2021 Broken Access Control; NIST CSF PR.AC-1.
    if no_filter:
        strict_mode_env = os.environ.get("JERRY_STRICT_MODE", "true").lower()
        strict = strict_mode_env not in ("false", "0", "no")
        if strict:
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
            strict_mode_env,
        )

    # Handle --init-engagement before anything else
    if init_engagement:
        return _handle_init_engagement(init_engagement, project_root)

    # Load family registry (FIX-9: via factory)
    services = create_tool_exec_handler(project_root)
    loader: FamilyRegistryLoader = services["loader"]
    engagement_init: EngagementInitializer = services["engagement_init"]
    credential_filter: CredentialFilterService = services["credential_filter"]

    try:
        resolvers = loader.load()
    except FileNotFoundError:
        print(
            f"Error: Family registry not found: {project_root / 'tool_families.yaml'}",
            file=sys.stderr,
        )
        return ExitCode.FAMILY_NOT_FOUND
    except ValueError as e:
        # FIX-6 (CV-009): Use FAMILY_CONFIG_ERROR for malformed registry
        print(f"Error loading family registry: {e}", file=sys.stderr)
        return ExitCode.FAMILY_CONFIG_ERROR
    except Exception as e:
        print(f"Error loading family registry: {e}", file=sys.stderr)
        return ExitCode.FAMILY_CONFIG_ERROR

    # Build family router
    router = FamilyRouterService(resolvers)

    # Resolve tool command
    try:
        resolution = router.resolve(tool_command, family=family)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return ExitCode.UNKNOWN_TOOL

    # Get resolver and security policy
    resolver = resolvers.get(resolution.family)
    if resolver is None:
        # FIX-6 (CV-008): Use FAMILY_NOT_FOUND
        print(f"Error: Family '{resolution.family}' not found.", file=sys.stderr)
        return ExitCode.FAMILY_NOT_FOUND

    policy = resolver.security_policy(tool_command)

    # Extend credential filter with family-specific patterns
    if policy.credential_filter_patterns:
        credential_filter.extend_patterns(policy.credential_filter_patterns)

    # FIX-11 (SR-001): Resolve config path from registry, not hardcoded.
    # The registry entry's config_path is relative to the project root.
    family_info_list = loader.list_families()
    family_config_path: str | None = None
    for fi in family_info_list:
        if fi.name == resolution.family:
            family_config_path = str(project_root / fi.config_path)
            break

    # FIX-12 (IN-009): ModeResolverService receives family env_var_prefix.
    # The prefix is derived from the family name (uppercase).
    env_var_prefix = resolution.family.upper().replace("-", "_")
    mode_resolver = ModeResolverService(env_var_prefix=env_var_prefix)

    try:
        config: dict[str, Any] = {}
        if family_config_path is not None:
            try:
                config = resolver.load_config(family_config_path)
            except FileNotFoundError:
                config = {}
        config_mode = config.get("default_mode")
        mode = mode_resolver.resolve(cli_mode=cli_mode, config_mode=config_mode)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return ExitCode.MODE_UNSET

    # FIX-3 (FM-002): Zone 3 container enforcement.
    # If SecurityPolicy.container_required is True and the resolved mode is
    # 'local', reject the execution with a clear error. Zone 3 exploitation tools
    # MUST run inside a container for process isolation; allowing local mode
    # would bypass the container isolation guarantee (OWASP A04:2021).
    if policy.container_required and mode == "local":
        print(
            f"Error: Tool '{tool_command}' ({resolution.zone}) requires container "
            f"execution (container_required=True). "
            f"--mode local is not permitted for Zone 3 tools. "
            f"Use --mode container or set {mode_resolver.env_var_name}=container.",
            file=sys.stderr,
        )
        return ExitCode.ZONE3_CONTAINER_REQUIRED

    # Handle --health-check
    if health_check:
        return _handle_health_check(resolution, project_root)

    # FIX-2 (FM-032): Zone 3 approval gate.
    # If SecurityPolicy.requires_approval is True, prompt the user for explicit
    # confirmation before executing. AI agents that do not handle interactive
    # prompts will receive the rejection path (non-tty -> auto-deny).
    if policy.requires_approval:
        approved = _prompt_zone3_approval(tool_command, resolution.zone)
        if not approved:
            print(
                f"[SECURITY] Zone 3 execution of '{tool_command}' NOT approved. Aborting.",
                file=sys.stderr,
            )
            return ExitCode.ENGAGEMENT_NOT_INIT

    # Check engagement requirements
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

    # Handle credential quarantine (FIX-1: quarantine always wired on detection)
    credential_detected = result.get("credential_detected", False)
    if credential_detected and engagement_id:
        _quarantine_output(
            raw_output=result["raw_stdout"],
            tool_command=tool_command,
            engagement_id=engagement_id,
            engagement_init=engagement_init,
            match_info=result.get("match_info"),
        )

    # Persist evidence if engagement is active and no credential was detected
    if engagement_id and not credential_detected:
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

    # Print output
    if result["stdout"]:
        print(result["stdout"])
    if result["stderr"]:
        print(result["stderr"], file=sys.stderr)

    return result["exit_code"]


# ---------------------------------------------------------------------------
# Management commands (FIX-7: UC-004)
# ---------------------------------------------------------------------------


def _handle_management_command(args: Any) -> int:
    """Handle --list-families and --list-tools management commands (UC-004).

    Args:
        args: Parsed argparse namespace.

    Returns:
        Exit code.
    """
    project_root = _find_project_root()
    registry_path = project_root / "tool_families.yaml"
    loader = FamilyRegistryLoader(registry_path)

    list_families = getattr(args, "list_families", False)
    list_tools = getattr(args, "list_tools", None)

    if list_families:
        try:
            families = loader.list_families()
        except FileNotFoundError:
            print(f"Error: Family registry not found: {registry_path}", file=sys.stderr)
            return ExitCode.FAMILY_NOT_FOUND
        except ValueError as e:
            print(f"Error parsing family registry: {e}", file=sys.stderr)
            return ExitCode.FAMILY_CONFIG_ERROR

        print("Registered tool families:")
        for fi in families:
            status = "enabled" if fi.enabled else "disabled"
            print(f"  {fi.name} [{status}] (priority={fi.priority})")
            print(f"    {fi.description}")
            print(f"    config: {fi.config_path}")
        return ExitCode.SUCCESS

    if list_tools is not None:
        # list_tools may be a family name string or True for all families
        family_filter = list_tools if isinstance(list_tools, str) and list_tools else None
        try:
            resolvers = loader.load()
        except FileNotFoundError:
            print(f"Error: Family registry not found: {registry_path}", file=sys.stderr)
            return ExitCode.FAMILY_NOT_FOUND
        except (ValueError, Exception) as e:
            print(f"Error loading family registry: {e}", file=sys.stderr)
            return ExitCode.FAMILY_CONFIG_ERROR

        for family_name, resolver in resolvers.items():
            if family_filter and family_name != family_filter:
                continue
            print(f"Family: {family_name}")
            # Load config and show tool resolution table
            family_info_list = loader.list_families()
            config_path: str | None = None
            for fi in family_info_list:
                if fi.name == family_name:
                    config_path = str(project_root / fi.config_path)
                    break
            if config_path:
                try:
                    config = resolver.load_config(config_path)
                    tools = config.get("tool_resolution", [])
                    for entry in tools:
                        prefix = entry.get("prefix", "?")
                        zone = entry.get("zone", "1")
                        service = entry.get("service", "local")
                        print(f"  {prefix}  (Zone {zone}, service={service})")
                except (FileNotFoundError, ValueError):
                    print("  (config not available)")
            print()
        return ExitCode.SUCCESS

    return ExitCode.SUCCESS


# ---------------------------------------------------------------------------
# Engagement management helpers
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Zone 3 approval gate (FIX-2)
# ---------------------------------------------------------------------------


def _prompt_zone3_approval(tool_command: str, zone: str) -> bool:
    """Prompt the user for explicit Zone 3 per-operation approval.

    FM-032 (FIX-2): SecurityPolicy.requires_approval is declared for Zone 3
    but was previously never checked. This function enforces the gate by
    requesting interactive confirmation before any Zone 3 execution.

    Non-interactive environments (CI, AI agents) have stdin that is not a
    TTY. In such cases the prompt auto-denies to prevent unattended Zone 3
    execution without human review (OWASP A01:2021 Broken Access Control).

    Args:
        tool_command: The tool about to be executed.
        zone: The security zone label (e.g., 'Zone 3').

    Returns:
        True if the user approves, False otherwise.
    """
    if not sys.stdin.isatty():
        logger.warning(
            "[SECURITY] Zone 3 approval gate: non-interactive stdin detected "
            "for '%s' (%s). Auto-denying to prevent unattended execution.",
            tool_command,
            zone,
        )
        return False

    print(
        f"\n[SECURITY] {zone} tool execution requires explicit approval.",
        file=sys.stderr,
    )
    print(f"  Tool: {tool_command}", file=sys.stderr)
    print(
        "  This tool performs active exploitation operations. "
        "Confirm only in an authorized engagement.",
        file=sys.stderr,
    )
    try:
        answer = input("  Approve? [yes/NO]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False
    return answer == "yes"


# ---------------------------------------------------------------------------
# Execution helpers
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Evidence persistence and quarantine
# ---------------------------------------------------------------------------


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

    FIX-1 (DA-002/CV-005): This function is now always called when
    credential_detected=True and an engagement is active.

    FIX-8 (RT-003/SR-003): After writing both the raw output file and the
    meta file, os.chmod(file_path, 0o600) is called on each. The quarantine
    directory is 0o700 (set in EngagementInitializer.initialize()), but files
    written inside it inherit the process umask (typically 0o644), making
    credential-bearing files world-readable. Setting 0o600 (owner read/write
    only) ensures credentials remain inaccessible to other users on multi-user
    systems. NIST CSF PR.DS-1 (data-at-rest protection).

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
    # FIX-8 (RT-003/SR-003): Restrict quarantine file to owner-only read/write.
    # The directory is 0o700, but files inherit umask (often 0o644). Force 0o600.
    os.chmod(str(quarantine_file), 0o600)

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
    # FIX-8 (RT-003/SR-003): Restrict meta file permissions too.
    os.chmod(str(meta_file), 0o600)

    print(
        f"[CREDENTIAL-FILTER] Output quarantined to: {quarantine_file}",
        file=sys.stderr,
    )
