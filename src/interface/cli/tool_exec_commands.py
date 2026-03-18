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

import dataclasses
import json
import logging
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.shared_kernel.exceptions import NotFoundError
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

    Instantiates and wires together ALL services required for tool execution.
    Separates service construction from the CLI handler logic, following the
    Dependency Inversion Principle and the composition root pattern (CC-002).

    CC-004-20260318: LocalExecutor and ContainerExecutor are now instantiated
    here, NOT inside _execute_local() or _execute_container(). Those helpers
    violated H-07(c) (composition root exclusivity) by constructing domain
    service dependencies inline. The factory is the single composition root
    for base service construction.

    IN-017-R2: CredentialFilterService is constructed first, then injected into
    both executors. Both executors now require a filter (no-None default) so the
    factory MUST supply it.

    DA-R4-001 (two-path topology): The factory produces the base composition
    for most invocations. However, ``handle_tool_exec`` applies a second path
    for invocations where the resolved family's ``SecurityPolicy`` carries
    family-specific credential filter patterns (PM-004-R3). In that path, a
    fresh invocation-scoped ``CredentialFilterService`` is created inline
    (``credential_filter.with_extra_patterns()``) and the executor references
    are rebound to new instances that hold this scoped filter. The factory's
    shared ``credential_filter``, ``local_executor``, and
    ``container_executor`` instances are NOT mutated. This is intentional:
    pattern bleed between families or concurrent invocations must be prevented.
    Callers that require the invocation-scoped filter must use the rebound
    local variables in ``handle_tool_exec``, not the factory dict values.

    Args:
        project_root: Resolved project root path used to locate registries
            and engagement directories.

    Returns:
        Mapping of service name to instance:
            - 'loader': FamilyRegistryLoader
            - 'engagement_init': EngagementInitializer
            - 'credential_filter': CredentialFilterService (base; may be
              superseded by an invocation-scoped instance in handle_tool_exec
              when family-specific patterns are present -- see DA-R4-001)
            - 'local_executor': LocalExecutor (with base credential_filter)
            - 'container_executor': ContainerExecutor (with base credential_filter)

        DA-R3-002: 'mode_resolver' is intentionally absent. handle_tool_exec
        constructs its own ModeResolverService with a family-specific
        env_var_prefix (FIX-12/IN-009). A default-prefix instance here was
        misleading and invited incorrect reuse.
    """
    registry_path = project_root / "tool_families.yaml"
    credential_filter = CredentialFilterService()
    return {
        "loader": FamilyRegistryLoader(registry_path),
        "engagement_init": EngagementInitializer(base_dir=project_root / "work" / "engagements"),
        "credential_filter": credential_filter,
        "local_executor": LocalExecutor(credential_filter=credential_filter),
        "container_executor": ContainerExecutor(
            credential_filter=credential_filter,
            project_root=str(project_root),
        ),
        # DA-R3-002: mode_resolver removed from factory. handle_tool_exec
        # constructs its own ModeResolverService with a family-specific
        # env_var_prefix after resolution (FIX-12/IN-009). Keeping a default
        # prefix instance here was misleading and invited incorrect reuse.
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
    # FM-033: Retrieve --zone override so it can be threaded to the security
    # policy lookup. Previously parsed but never consumed (dead argument).
    zone_override: str | None = getattr(args, "zone", None)

    project_root = _find_project_root()

    # FIX-R3-3 (SR-002/CC-005): Build all services via factory before any
    # sub-handler is called. Previously _handle_init_engagement constructed its
    # own EngagementInitializer inline and _handle_health_check constructed its
    # own ContainerExecutor + CredentialFilterService inline. Both violated
    # H-07(c) (composition root exclusivity) and created divergent instances that
    # bypassed the factory's wiring. The factory is lightweight (no I/O until
    # loader.load() is called) so constructing it here is safe.
    #
    # SR-003-R4: Services are now built BEFORE the no_filter audit block so that
    # engagement_init is available and _write_no_filter_audit() can call
    # engagement_init.evidence_dir() (which enforces _validate_id()) instead of
    # building the path manually. The factory has zero I/O at construction time,
    # so moving it earlier imposes no cost.
    services = create_tool_exec_handler(project_root)
    loader: FamilyRegistryLoader = services["loader"]
    engagement_init: EngagementInitializer = services["engagement_init"]
    credential_filter: CredentialFilterService = services["credential_filter"]
    local_executor: LocalExecutor = services["local_executor"]
    container_executor: ContainerExecutor = services["container_executor"]

    # FIX-4 (RT-001): Strict-mode bypass via empty env var closed.
    # Only explicitly "false", "0", or "no" disables strict mode.
    # Empty string, unset, or any other value keeps strict mode ON.
    # FIX-R3-1 (PM-001-R3): Resolve strict_mode unconditionally so it can be
    # threaded to _execute_local() and _execute_container(). Previously the
    # resolution only happened inside `if no_filter:`, so the executor always
    # received the hard-coded default strict_mode=True. When JERRY_STRICT_MODE
    # was false and --no-filter was passed, the CLI guard would pass (strict=False)
    # but the executor would still call filter_output(strict_mode=True) and raise
    # RuntimeError. Threading the resolved bool closes this inconsistency.
    # M-03 (T-06, DREAD 34, HIGH): Strict mode enforcement for --no-filter.
    # When JERRY_STRICT_MODE is true, --no-filter is FORBIDDEN. An AI agent
    # invoking `jerry tool exec --no-filter <tool>` would receive unfiltered
    # output including any credentials, bypassing all L1 credential protection.
    # OWASP A01:2021 Broken Access Control; NIST CSF PR.AC-1.
    strict_mode_env = os.environ.get("JERRY_STRICT_MODE", "true").lower()
    strict = strict_mode_env not in ("false", "0", "no")
    if no_filter:
        if strict:
            print(
                "Error: --no-filter is FORBIDDEN when JERRY_STRICT_MODE=true. "
                "Credential filtering cannot be disabled in strict mode. "
                "To allow --no-filter, set JERRY_STRICT_MODE=false (not recommended).",
                file=sys.stderr,
            )
            return ExitCode.STRICT_MODE_VIOLATION
        # Outside strict mode: log a warning but allow execution.
        # FM-001: Also write a durable audit record so the --no-filter invocation
        # leaves a persistent trace. logger.warning() is process-scoped and lost on
        # exit; the file-based audit survives the process.
        logger.warning(
            "[SECURITY-WARN] --no-filter passed with JERRY_STRICT_MODE=%s. "
            "Credential filtering is DISABLED for this invocation. "
            "Tool output may contain credentials.",
            strict_mode_env,
        )
        # FM-001 / SR-003-R4: Write durable audit record. engagement_init is now
        # available (services built before this block) so the audit path is
        # constructed via evidence_dir() which enforces _validate_id() (CWE-22).
        _write_no_filter_audit(
            tool_command=tool_command if tool_command else "<unknown>",
            engagement_id=getattr(args, "engagement_id", None),
            strict_mode_env=strict_mode_env,
            project_root=project_root,
            engagement_init=engagement_init,
        )

    # Handle --init-engagement before registry load
    if init_engagement:
        return _handle_init_engagement(init_engagement, engagement_init)

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
    # CV-008 fix: catch NotFoundError separately for explicit --family.
    # When --family is specified and not in registry, return FAMILY_NOT_FOUND (7).
    # When tool is not recognized by any family, return UNKNOWN_TOOL (1).
    try:
        resolution = router.resolve(tool_command, family=family)
    except NotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        if family:
            return ExitCode.FAMILY_NOT_FOUND
        return ExitCode.UNKNOWN_TOOL
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

    # FM-033: Apply --zone override to the security policy when provided.
    # The --zone flag was parsed but previously never consumed (dead argument).
    # When an operator explicitly sets --zone, the policy's zone-sensitive fields
    # are overridden so the correct engagement, approval, container, and network
    # constraints are enforced for the requested zone.
    #
    # Zone mapping mirrors RainbowToolResolver._ZONE_POLICIES:
    #   Zone 1: no engagement, no approval, no container, network=none
    #   Zone 2: engagement required, no approval, no container, network=restricted
    #   Zone 3: engagement required, approval required, container required, network=full
    #
    # The credential_filter_enabled field is intentionally not overridden: it is
    # determined by the family configuration, not by the zone selection.
    if zone_override is not None:
        _ZONE_OVERRIDE_FIELDS: dict[str, dict[str, Any]] = {
            "1": {
                "requires_engagement": False,
                "requires_approval": False,
                "container_required": False,
                "network_access": "none",
                "family_zone_label": "Zone 1",
            },
            "2": {
                "requires_engagement": True,
                "requires_approval": False,
                "container_required": False,
                "network_access": "restricted",
                "family_zone_label": "Zone 2",
            },
            "3": {
                "requires_engagement": True,
                "requires_approval": True,
                "container_required": True,
                "network_access": "full",
                "family_zone_label": "Zone 3",
            },
        }
        override_fields = _ZONE_OVERRIDE_FIELDS.get(zone_override)
        if override_fields is not None:
            policy = dataclasses.replace(policy, **override_fields)
            logger.info(
                "[SECURITY] --zone %s override applied to security policy for '%s'.",
                zone_override,
                tool_command,
            )

    # PM-004-R3: Create an invocation-scoped filter when family-specific patterns
    # are present, rather than mutating the shared singleton via extend_patterns().
    # This prevents pattern bleed between families or between multiple invocations
    # in the same process (e.g., test suite, future server mode).
    # The shared credential_filter from the factory remains the base; the
    # invocation_filter is a fresh instance with the extra patterns applied.
    if policy.credential_filter_patterns:
        invocation_filter = credential_filter.with_extra_patterns(policy.credential_filter_patterns)
        # Re-wire the executors to use the invocation-scoped filter for this request.
        # Only the executor instances used for this invocation are updated; the
        # factory's shared instances are not mutated.
        local_executor = LocalExecutor(credential_filter=invocation_filter)
        container_executor = ContainerExecutor(
            credential_filter=invocation_filter,
            project_root=str(project_root),
        )

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

    # CV-003 (UC-001 Extension 7b): Strict mode + Zone 2/3 + no explicit mode -> exit 6.
    # When JERRY_STRICT_MODE is active and the tool is Zone 2 or Zone 3, the operator
    # MUST provide an explicit mode selection (--mode flag or env var). Falling back
    # to the hardcoded default ('local') is not permitted in strict mode for these
    # zones because the appropriate execution environment is security-sensitive.
    # This gate runs after mode resolution so we have both zone and mode information.
    _zone_label = getattr(resolution, "zone", "") or ""
    _requires_explicit_mode = _zone_label in ("Zone 2", "Zone 3")
    _explicit_mode_provided = (
        cli_mode is not None
        or os.environ.get(mode_resolver.env_var_name) is not None
        or os.environ.get("JERRY_TOOL_MODE") is not None
    )
    if strict and _requires_explicit_mode and not _explicit_mode_provided:
        print(
            f"Error: Strict mode requires explicit mode selection for {_zone_label} tools. "
            "Use --mode local or --mode container.",
            file=sys.stderr,
        )
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

    # RT-R2-004: Handle --health-check BEFORE the Zone 3 approval gate.
    # Previously the health check came AFTER the approval prompt, meaning
    # an operator could not check container health without first approving
    # a Zone 3 execution. Health checks are informational -- they must not
    # require an exploitation approval.
    if health_check:
        return _handle_health_check(resolution, container_executor, project_root)

    # FIX-2 (FM-032): Zone 3 approval gate.
    # If SecurityPolicy.requires_approval is True, prompt the user for explicit
    # confirmation before executing. AI agents that do not handle interactive
    # prompts will receive the rejection path (non-tty -> auto-deny).
    if policy.requires_approval:
        approved = _prompt_zone3_approval(
            tool_command=tool_command,
            zone=resolution.zone,
            engagement_id=engagement_id,
            engagement_init=engagement_init,
        )
        if not approved:
            print(
                f"[SECURITY] Zone 3 execution of '{tool_command}' NOT approved. Aborting.",
                file=sys.stderr,
            )
            # IN-015-R2 / NEW-001: Use ZONE3_APPROVAL_DENIED (11), not
            # ENGAGEMENT_NOT_INIT (5). Conflating approval denial with
            # engagement-not-initialized produced ambiguous exit codes that
            # callers could not distinguish. ZONE3_APPROVAL_DENIED is unambiguous.
            return ExitCode.ZONE3_APPROVAL_DENIED

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

    # Execute tool (CC-004-20260318: pass pre-built executors from factory)
    if mode == "container":
        result = _execute_container(
            tool_command=tool_command,
            tool_args=tool_args,
            resolution=resolution,
            executor=container_executor,
            project_root=project_root,
            no_filter=no_filter,
            strict_mode=strict,
        )
    else:
        result = _execute_local(
            tool_command=tool_command,
            tool_args=tool_args,
            executor=local_executor,
            no_filter=no_filter,
            strict_mode=strict,
        )

    # Handle credential quarantine
    # RT-R2-002 / PM-006-R2: Quarantine fires unconditionally on credential
    # detection -- the engagement_id guard is removed. When no engagement is
    # active, a global fallback quarantine path (work/.credential-quarantine/)
    # is used so Zone 1 detections are never silently discarded.
    credential_detected = result.get("credential_detected", False)
    if credential_detected:
        _quarantine_output(
            raw_stdout=result["raw_stdout"],
            raw_stderr=result.get("raw_stderr", ""),
            tool_command=tool_command,
            engagement_id=engagement_id,
            engagement_init=engagement_init,
            project_root=project_root,
            match_info=result.get("match_info"),
        )

    # Persist evidence if engagement is active, no credential was detected,
    # and the family's security policy declares evidence_auto_persist=True.
    # CV-016 / UC-001 Step 10: Families opt in to evidence persistence via
    # SecurityPolicy.evidence_auto_persist. Default True preserves backward compat.
    if engagement_id and not credential_detected and policy.evidence_auto_persist:
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
            # CV-013B: Pass project_root so list_families() can populate
            # tool_count from each family's config file (UC-004 Step 3).
            families = loader.list_families(project_root=project_root)
        except FileNotFoundError:
            print(f"Error: Family registry not found: {registry_path}", file=sys.stderr)
            return ExitCode.FAMILY_NOT_FOUND
        except ValueError as e:
            print(f"Error parsing family registry: {e}", file=sys.stderr)
            return ExitCode.FAMILY_CONFIG_ERROR

        print("Registered tool families:")
        for fi in families:
            status = "enabled" if fi.enabled else "disabled"
            tool_count_str = str(fi.tool_count) if fi.tool_count is not None else "?"
            print(f"  {fi.name} [{status}] (priority={fi.priority}, tools={tool_count_str})")
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


def _handle_init_engagement(
    engagement_id: str,
    engagement_init: EngagementInitializer,
) -> int:
    """Initialize a new engagement directory.

    FIX-R3-3 (SR-002/CC-005): Receives a factory-built EngagementInitializer
    rather than constructing its own. Inline construction violated H-07(c)
    (composition root exclusivity) and bypassed the factory's wiring.

    CC-001-R4 (H-07): Reads USER/USERNAME from os.environ here (infrastructure
    boundary) and passes the resolved string to EngagementInitializer.initialize()
    so the domain service stays free of environment variable access.

    Args:
        engagement_id: The engagement identifier.
        engagement_init: Factory-built EngagementInitializer from composition root.

    Returns:
        Exit code.
    """
    # CC-001-R4: Resolve operator identity at the CLI boundary (infrastructure),
    # not inside the domain service. Pass the resolved string as a parameter.
    created_by: str = os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"
    try:
        path = engagement_init.initialize(engagement_id, created_by=created_by)
        print(f"Engagement initialized: {path}")
        return ExitCode.SUCCESS
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        # CV-011: Invalid engagement ID should return UNKNOWN_TOOL (1), not
        # ENGAGEMENT_NOT_INIT (5). Exit code 5 signals that the engagement
        # directory does not exist for a tool that needs it; a bad ID passed
        # to --init-engagement is a bad-input error (exit code 1).
        return ExitCode.UNKNOWN_TOOL


def _handle_health_check(
    resolution: Any,
    container_executor: ContainerExecutor,
    project_root: Path,
) -> int:
    """Check container health for the resolved tool's service.

    FIX-R3-3 (SR-002/CC-005): Receives a factory-built ContainerExecutor
    rather than constructing its own ContainerExecutor + CredentialFilterService
    inline. Inline construction violated H-07(c) (composition root exclusivity)
    and bypassed the factory's credential_filter wiring.

    Args:
        resolution: ToolResolutionEntry with container service info.
        container_executor: Factory-built ContainerExecutor from composition root.
        project_root: Project root used to build the absolute compose file path.

    Returns:
        Exit code.
    """
    if not resolution.container_service or not resolution.compose_file:
        print("No container service configured for this tool.")
        return ExitCode.SUCCESS

    compose_path = str(project_root / resolution.compose_file)
    healthy = container_executor.health_check(
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


def _prompt_zone3_approval(
    tool_command: str,
    zone: str,
    engagement_id: str | None,
    engagement_init: EngagementInitializer,
) -> bool:
    """Prompt the user for explicit Zone 3 per-operation approval.

    FM-032 (FIX-2): SecurityPolicy.requires_approval is declared for Zone 3
    but was previously never checked. This function enforces the gate by
    requesting interactive confirmation before any Zone 3 execution.

    Non-interactive environments (CI, AI agents) have stdin that is not a
    TTY. In such cases the prompt auto-denies to prevent unattended Zone 3
    execution without human review (OWASP A01:2021 Broken Access Control).

    IN-016-R2: Both approval and denial events are written to a persistent
    audit trail in the engagement directory (or a global audit trail if no
    engagement is active). This provides a tamper-evident record of who
    approved Zone 3 operations and when.

    Args:
        tool_command: The tool about to be executed.
        zone: The security zone label (e.g., 'Zone 3').
        engagement_id: Active engagement identifier (may be None).
        engagement_init: Engagement initializer used to locate audit directory.

    Returns:
        True if the user approves, False otherwise.
    """
    auto_deny = not sys.stdin.isatty()
    if auto_deny:
        logger.warning(
            "[SECURITY] Zone 3 approval gate: non-interactive stdin detected "
            "for '%s' (%s). Auto-denying to prevent unattended execution.",
            tool_command,
            zone,
        )
        _write_approval_audit(
            tool_command=tool_command,
            zone=zone,
            approved=False,
            reason="auto-deny: non-interactive stdin",
            engagement_id=engagement_id,
            engagement_init=engagement_init,
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
        _write_approval_audit(
            tool_command=tool_command,
            zone=zone,
            approved=False,
            reason="interrupted: EOFError/KeyboardInterrupt",
            engagement_id=engagement_id,
            engagement_init=engagement_init,
        )
        return False

    approved = answer == "yes"
    audit_ok = _write_approval_audit(
        tool_command=tool_command,
        zone=zone,
        approved=approved,
        reason="operator input",
        engagement_id=engagement_id,
        engagement_init=engagement_init,
    )
    # FIX-R3-2 (PM-002-R3/RT-001/IN-021): If the operator approved but the
    # audit record could not be written, deny the execution. Zone 3 execution
    # without a tamper-evident audit trail violates the engagement integrity
    # guarantee. Denial events do not need to block: a denied execution is
    # already safe regardless of whether the audit write succeeded.
    if approved and not audit_ok:
        print(
            "[SECURITY] Zone 3 execution DENIED: audit write failed. "
            "Cannot proceed without a tamper-evident approval record. "
            "Check file permissions on the audit directory.",
            file=sys.stderr,
        )
        return False
    return approved


def _write_approval_audit(
    tool_command: str,
    zone: str,
    approved: bool,
    reason: str,
    engagement_id: str | None,
    engagement_init: EngagementInitializer,
) -> bool:
    """Write a Zone 3 approval/denial event to the engagement audit trail.

    IN-016-R2: Provides persistent, tamper-evident record of Zone 3 approval
    decisions. Each event is written to a separate JSON file in the engagement
    audit directory. When no engagement is active, events are written to a
    global audit path (work/.zone3-audit/).

    FIX-R3-2 (PM-002-R3/RT-001/IN-021): Returns True on success, False on
    failure. When the audit write fails for an approved Zone 3 execution the
    caller MUST deny the execution -- proceeding without an audit record violates
    the tamper-evidence guarantee (OWASP A09:2021 Security Logging Failures).
    Denial events are best-effort: a failed denial audit is logged to stderr but
    never blocks the denial itself (denials are already safe).
    The except block also prints to stderr so audit failures are always visible
    in the operator console even when log output is suppressed.

    Args:
        tool_command: The tool for which approval was sought.
        zone: The security zone label.
        approved: True if the operation was approved, False if denied.
        reason: Human-readable reason for the decision.
        engagement_id: Active engagement identifier (may be None).
        engagement_init: Engagement initializer for directory resolution.

    Returns:
        True if the audit record was written successfully, False otherwise.
    """
    try:
        if engagement_id:
            audit_dir = engagement_init.evidence_dir(engagement_id).parent / "audit"
        else:
            # SR-003/PM-007-R3: Use public global_audit_dir() method instead of
            # accessing private _base_dir attribute across module boundary.
            # Eliminates Law of Demeter violation and decouples CLI from
            # EngagementInitializer internals.
            audit_dir = engagement_init.global_audit_dir()

        audit_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(str(audit_dir), 0o700)

        ts = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
        label = engagement_id or "no-engagement"
        audit_file = audit_dir / f"zone3-approval-{label}-{ts}.json"

        event: dict[str, Any] = {
            "timestamp": ts,
            "engagement_id": engagement_id,
            "tool_command": tool_command,
            "zone": zone,
            "approved": approved,
            "reason": reason,
        }
        audit_file.write_text(json.dumps(event, indent=2) + "\n", encoding="utf-8")
        os.chmod(str(audit_file), 0o600)

        logger.info(
            "[SECURITY] Zone 3 approval audit written: %s (approved=%s)",
            audit_file,
            approved,
        )
        return True
    except Exception:
        logger.exception("[SECURITY] Failed to write Zone 3 approval audit")
        print(
            "[SECURITY] CRITICAL: Zone 3 approval audit write FAILED. "
            "Audit trail cannot be established.",
            file=sys.stderr,
        )
        return False


def _write_no_filter_audit(
    tool_command: str,
    engagement_id: str | None,
    strict_mode_env: str,
    project_root: Path,
    engagement_init: EngagementInitializer | None = None,
) -> None:
    """Write a durable audit record for --no-filter invocations.

    FM-001 (RPN 280): When --no-filter is used with JERRY_STRICT_MODE=false,
    a persistent JSON audit file is written so there is a durable record that
    credential filtering was disabled for this invocation. logger.warning()
    alone is insufficient -- the log is process-scoped and lost on exit, leaving
    no forensic trail for a post-incident review.

    Audit location:
    - When an engagement is active: evidence_dir(engagement_id) from
      EngagementInitializer (SR-003-R4: path constructed via the service, not
      manually; prevents path traversal when engagement_id is validated by
      _validate_id() inside evidence_dir()).
    - When no engagement is active: work/security-events/ (global fallback).

    Best-effort: audit write failures are logged to stderr but NEVER block the
    execution. Strict mode was already verified to be off before this is called.

    Args:
        tool_command: The tool command being executed without filtering.
        engagement_id: Active engagement identifier, or None.
        strict_mode_env: The raw JERRY_STRICT_MODE env var value for the record.
        project_root: Project root path for locating audit directories.
        engagement_init: EngagementInitializer for validated path construction.
            SR-003-R4: Required when engagement_id is set so _validate_id() is
            called via evidence_dir(). When None, the global fallback path is used.
    """
    try:
        if engagement_id and engagement_init is not None:
            # SR-003-R4: Use engagement_init.evidence_dir() instead of building
            # the path manually. evidence_dir() calls _validate_id() internally,
            # which enforces the allowlist and prevents path traversal via
            # malformed engagement IDs. Manual construction (project_root /
            # "work" / "engagements" / engagement_id / "evidence") skipped that
            # validation gate (CWE-22).
            audit_dir = engagement_init.evidence_dir(engagement_id)
        else:
            # Global fallback: work/security-events/ when no engagement is active
            audit_dir = project_root / "work" / "security-events"

        audit_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
        audit_file = audit_dir / f"no-filter-audit-{ts}.json"

        event: dict[str, Any] = {
            "timestamp": ts,
            "event_type": "no_filter_invocation",
            "tool_command": tool_command,
            "engagement_id": engagement_id,
            "jerry_strict_mode": strict_mode_env,
            "warning": "Credential filtering was DISABLED for this invocation.",
        }
        audit_file.write_text(json.dumps(event, indent=2) + "\n", encoding="utf-8")
        os.chmod(str(audit_file), 0o600)

        logger.info("[SECURITY] --no-filter audit written: %s", audit_file)
    except Exception:
        logger.exception("[SECURITY] Failed to write --no-filter audit record")
        print(
            "[SECURITY] WARNING: --no-filter audit write failed. "
            "The unfiltered execution will proceed but no durable audit record was created.",
            file=sys.stderr,
        )


# ---------------------------------------------------------------------------
# Execution helpers
# ---------------------------------------------------------------------------


def _execute_local(
    tool_command: str,
    tool_args: list[str],
    executor: LocalExecutor,
    no_filter: bool,
    strict_mode: bool = True,
) -> dict[str, Any]:
    """Execute a tool locally.

    CC-004-20260318: Receives a pre-built LocalExecutor from the composition
    root rather than constructing one inline (H-07(c) compliance).

    FIX-R3-1 (PM-001-R3): strict_mode threaded through so the executor
    receives the CLI-resolved JERRY_STRICT_MODE value rather than the
    hard-coded True default.

    Args:
        tool_command: Tool binary name.
        tool_args: Tool arguments.
        executor: Pre-built LocalExecutor from the composition root factory.
        no_filter: Whether to skip filtering.
        strict_mode: Resolved JERRY_STRICT_MODE boolean from CLI handler.

    Returns:
        Dictionary with execution results, including raw_stderr (RT-R2-001).
    """
    result = executor.execute(
        tool_command=tool_command,
        tool_args=tool_args,
        no_filter=no_filter,
        strict_mode=strict_mode,
    )
    return {
        "exit_code": result.exit_code,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "raw_stdout": result.raw_stdout,
        # RT-R2-001: Include raw_stderr so _quarantine_output can persist both
        # streams. Previously raw_stderr was dropped here.
        "raw_stderr": result.raw_stderr,
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
    executor: ContainerExecutor,
    project_root: Path,
    no_filter: bool,
    strict_mode: bool = True,
) -> dict[str, Any]:
    """Execute a tool in a container.

    CC-004-20260318: Receives a pre-built ContainerExecutor from the
    composition root rather than constructing one inline (H-07(c) compliance).

    FIX-R3-1 (PM-001-R3): strict_mode threaded through so the executor
    receives the CLI-resolved JERRY_STRICT_MODE value rather than the
    hard-coded True default.

    Args:
        tool_command: Tool binary name.
        tool_args: Tool arguments.
        resolution: ToolResolutionEntry with container metadata.
        executor: Pre-built ContainerExecutor from the composition root factory.
        project_root: Path to the project root.
        no_filter: Whether to skip filtering.
        strict_mode: Resolved JERRY_STRICT_MODE boolean from CLI handler.

    Returns:
        Dictionary with execution results, including raw_stderr (RT-R2-001).
    """
    compose_path = None
    if resolution.compose_file:
        compose_path = str(project_root / resolution.compose_file)

    result = executor.execute(
        tool_command=tool_command,
        tool_args=tool_args,
        service=resolution.container_service or "",
        compose_file=compose_path,
        no_filter=no_filter,
        strict_mode=strict_mode,
    )

    return {
        "exit_code": result.exit_code,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "raw_stdout": result.raw_stdout,
        # RT-R2-001: Include raw_stderr so _quarantine_output can persist both
        # streams. Previously raw_stderr was dropped here.
        "raw_stderr": result.raw_stderr,
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
    raw_stdout: str,
    raw_stderr: str,
    tool_command: str,
    engagement_id: str | None,
    engagement_init: EngagementInitializer,
    project_root: Path,
    match_info: dict[str, Any] | None = None,
) -> None:
    """Quarantine output that triggered the credential filter.

    PM-006-R2 / RT-R2-002: This function fires unconditionally when
    credential_detected=True. The previous engagement_id guard meant that
    Zone 1 credential detections (no active engagement) were silently
    discarded -- the credential data was logged to the terminal and nothing
    was persisted. The fix removes the guard and routes to a global fallback
    quarantine path (work/.credential-quarantine/) when no engagement is active.

    RT-R2-001: Both raw_stdout and raw_stderr are quarantined. The previous
    implementation passed only raw_stdout, allowing credential-bearing stderr
    to escape quarantine even after FINDING-004 was fixed in the executors.

    FIX-8 (RT-003/SR-003): After writing both the raw output file and the
    meta file, os.chmod(file_path, 0o600) is called on each. The quarantine
    directory is also chmod'd to 0o700 after mkdir (SR-002-20260318).

    NEW-003: write_text() uses errors="replace" to prevent UnicodeEncodeError
    when credential-bearing output contains non-UTF-8 sequences.

    FIX-8 (RT-003/SR-003): os.chmod(file, 0o600) after each file write.
    NIST CSF PR.DS-1 (data-at-rest protection).

    Args:
        raw_stdout: Original unfiltered stdout from tool execution.
        raw_stderr: Original unfiltered stderr from tool execution (RT-R2-001).
        tool_command: Tool command that produced the output.
        engagement_id: Active engagement identifier. May be None when no
            engagement is active; in that case a global fallback quarantine
            path is used (PM-006-R2).
        engagement_init: Engagement initializer service.
        project_root: Project root path for fallback quarantine location.
        match_info: Details about the credential match.
    """
    hasher = EvidenceHasher()

    # PM-006-R2: Choose quarantine directory: engagement-scoped when available,
    # global fallback (work/.credential-quarantine/) when no engagement is active.
    if engagement_id:
        quarantine_dir = engagement_init.quarantine_dir(engagement_id)
    else:
        quarantine_dir = project_root / "work" / ".credential-quarantine"
        logger.warning(
            "[CREDENTIAL-FILTER] Credential detected with no active engagement. "
            "Quarantining to global fallback: %s",
            quarantine_dir,
        )

    quarantine_dir.mkdir(parents=True, exist_ok=True)
    # SR-002-20260318: chmod quarantine directory to 0o700 after creation.
    # mkdir creates dirs with mode modified by umask; force 0o700 explicitly.
    os.chmod(str(quarantine_dir), 0o700)

    # CV-006 / UC-005 DR-019: Use SHA-256 hash of raw output as filename stem.
    # Content-addressable naming provides deduplication (identical output produces
    # the same quarantine file) and removes the timestamp-collision risk (RT-004).
    # The hash is computed BEFORE writing so the filename reflects the file's
    # actual content.
    sha256_stdout = hasher.hash_string(raw_stdout)
    sha256_stderr = hasher.hash_string(raw_stderr)
    # PM-004-R4: Meta filename uses a compound hash of BOTH streams
    # (sha256(stdout + stderr)) instead of stdout hash alone. When a credential
    # appears only in stderr (e.g., a tool that logs secrets on stderr while
    # stdout is empty), the stdout-only hash is sha256("") for all such events --
    # a collision that causes successive stderr-only detections to silently
    # overwrite each other's meta file. The compound hash is distinct per
    # (stdout, stderr) pair, preserving all detections.
    sha256_compound = hasher.hash_string(raw_stdout + raw_stderr)
    quarantine_stdout_file = quarantine_dir / f"{sha256_stdout}.stdout.raw"
    quarantine_stderr_file = quarantine_dir / f"{sha256_stderr}.stderr.raw"
    meta_file = quarantine_dir / f"{sha256_compound}.meta.json"

    ts = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")

    # NEW-003: errors="replace" prevents UnicodeEncodeError on binary/mixed output.
    quarantine_stdout_file.write_text(raw_stdout, encoding="utf-8", errors="replace")
    os.chmod(str(quarantine_stdout_file), 0o600)

    quarantine_stderr_file.write_text(raw_stderr, encoding="utf-8", errors="replace")
    os.chmod(str(quarantine_stderr_file), 0o600)

    meta: dict[str, Any] = {
        "timestamp": ts,
        "engagement_id": engagement_id,
        "tool_command": tool_command,
        "detecting_layer": "L1-regex",
        "sha256_raw_stdout": sha256_stdout,
        "sha256_raw_stderr": sha256_stderr,
        # PM-004-R4: compound hash (sha256(stdout + stderr)) — used as meta
        # filename stem to prevent collision when only stderr carries the
        # credential (stdout is empty -> sha256_stdout is always sha256("")).
        "sha256_compound": sha256_compound,
        "quarantine_stdout_file": str(quarantine_stdout_file),
        "quarantine_stderr_file": str(quarantine_stderr_file),
    }
    if match_info:
        meta["matched_pattern"] = match_info.get("pattern", "")
        meta["detected_at_line"] = match_info.get("line_number", 0)

    meta_file.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8", errors="replace")
    # FIX-8 (RT-003/SR-003): Restrict meta file permissions too.
    os.chmod(str(meta_file), 0o600)

    print(
        f"[CREDENTIAL-FILTER] Output quarantined to: {quarantine_stdout_file}",
        file=sys.stderr,
    )
