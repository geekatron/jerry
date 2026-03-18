# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Family registry loader for dynamic plugin discovery.

Loads tool_families.yaml, dynamically imports resolver modules via importlib,
and validates that each resolver implements the ToolFamilyResolverPort interface.

References:
    - ADR-PROJ023-001: Multi-family plugin architecture
    - TASK-001D: FamilyRegistryLoader
    - SR-005 (FIX-15): Per-entry key validation with clear error messages
    - DA-004/IN-004 (FIX-16): Explicit priority field for auto-detection ordering
"""

from __future__ import annotations

import importlib
import logging
import re
from pathlib import Path

import yaml

from src.tool_exec.domain.ports.tool_family_resolver_port import (
    ToolFamilyResolverPort,
)
from src.tool_exec.domain.value_objects.tool_family_info import ToolFamilyInfo

logger = logging.getLogger(__name__)

# M-01 (T-01, DREAD 38, CRITICAL): Module path allowlist.
# Only modules under these prefixes are permitted for importlib.import_module().
# This prevents arbitrary code execution if tool_families.yaml is compromised.
# OWASP A08:2021 Data Integrity Failures -- restrict dynamic imports to known-good paths.
_ALLOWED_MODULE_PREFIXES: tuple[str, ...] = ("src.tool_exec.infrastructure.adapters.",)

# FINDING-003 (CWE-94): Resolver class name validation pattern.
# Constrains getattr() to CamelCase Python class identifiers (2-64 characters).
# Prevents arbitrary module attribute access (e.g., __builtins__, subprocess, open)
# via a tampered resolver_class value in tool_families.yaml. The module path
# allowlist (M-01) guards the module; this guard closes the class-name dimension.
# Pattern: starts with uppercase letter, followed by 1-63 alphanumeric chars.
_CLASS_NAME_PATTERN: re.Pattern[str] = re.compile(r"^[A-Z][a-zA-Z0-9]{1,63}$")

# SR-005 (FIX-15): Required keys for each family entry in tool_families.yaml.
_REQUIRED_FAMILY_KEYS: tuple[str, ...] = (
    "name",
    "resolver_module",
    "resolver_class",
    "config_path",
)


class FamilyRegistryLoader:
    """Loads and instantiates tool family resolver plugins.

    Reads tool_families.yaml, imports each resolver module via importlib,
    validates that the resolver class implements ToolFamilyResolverPort,
    and returns a mapping of family name to resolver instance.

    The loader is designed for use at CLI startup time. It does not cache
    results; each call to load() produces fresh resolver instances.

    Families are sorted by their explicit priority field (ascending: lower
    value = higher priority) for deterministic auto-detection ordering
    (DA-004/IN-004, FIX-16).

    Security: Module import paths are validated against _ALLOWED_MODULE_PREFIXES
    before importlib.import_module() is called (M-01, T-01 mitigation).
    """

    def __init__(self, registry_path: str | Path) -> None:
        """Initialize the loader with the path to tool_families.yaml.

        Args:
            registry_path: Path to the tool families registry YAML file.
        """
        self._registry_path = Path(registry_path)

    def load(self) -> dict[str, ToolFamilyResolverPort]:
        """Load all enabled family resolvers from the registry.

        Reads tool_families.yaml, imports each enabled resolver module,
        instantiates the resolver class, and validates it implements the
        ToolFamilyResolverPort interface.

        Families are sorted by priority (ascending) before loading so that
        auto-detection ordering is deterministic and does not depend on YAML
        dict insertion order (DA-004/IN-004, FIX-16).

        Returns:
            Mapping of family name to resolver instance, including only
            families marked as enabled.

        Raises:
            FileNotFoundError: If tool_families.yaml does not exist.
            ValueError: If the YAML is malformed or a resolver does not
                implement ToolFamilyResolverPort.
        """
        families = self._parse_registry()
        # FIX-16: Sort by priority ascending so lower priority number = checked first.
        families.sort(key=lambda fi: fi.priority)
        resolvers: dict[str, ToolFamilyResolverPort] = {}

        attempted = 0
        for family_info in families:
            if not family_info.enabled:
                logger.info("Skipping disabled family: %s", family_info.name)
                continue

            attempted += 1
            try:
                resolver = self._load_resolver(family_info)
                resolvers[family_info.name] = resolver
                logger.info("Loaded family resolver: %s", family_info.name)
            except Exception:
                # NEW-002 (FM-005): Skip a single failing family rather than
                # halting all loading. A malformed or missing resolver for one
                # family must not prevent the CLI from using other valid families.
                # After the loop, if ALL attempted families failed, raise so the
                # caller can surface a meaningful error. A partial load is acceptable.
                logger.exception(
                    "Failed to load family resolver: %s -- skipping this family",
                    family_info.name,
                )
                continue

        # Only raise if at least one enabled family was attempted and ALL failed.
        # If there are no enabled families (attempted == 0), return empty dict --
        # the caller (handle_tool_exec) will surface a FAMILY_NOT_FOUND error
        # when no family can resolve the tool command.
        if attempted > 0 and not resolvers:
            msg = (
                "No family resolvers could be loaded. All enabled families failed "
                "to initialize. Check the logs above for per-family error details."
            )
            raise ValueError(msg)

        return resolvers

    def list_families(self, project_root: Path | None = None) -> list[ToolFamilyInfo]:
        """List all registered families without loading resolvers.

        CV-013B: When project_root is provided, attempts to load each family's
        config file and populate tool_count from the tool_resolution entries.
        If a config file is unreadable or the registry path is not relative to
        project_root, tool_count is left as None and displayed as '?' in the CLI.

        Args:
            project_root: Optional project root Path used to resolve relative
                config_path values and count tool_resolution entries for
                --list-families display (UC-004 Step 3).

        Returns:
            List of ToolFamilyInfo for all families in the registry,
            sorted by priority ascending.

        Raises:
            FileNotFoundError: If tool_families.yaml does not exist.
        """
        families = self._parse_registry()
        families.sort(key=lambda fi: fi.priority)

        if project_root is not None:
            enriched: list[ToolFamilyInfo] = []
            for fi in families:
                tool_count = self._count_tools(fi.config_path, project_root)
                # ToolFamilyInfo is frozen; reconstruct with tool_count populated
                enriched.append(
                    ToolFamilyInfo(
                        name=fi.name,
                        description=fi.description,
                        resolver_module=fi.resolver_module,
                        resolver_class=fi.resolver_class,
                        config_path=fi.config_path,
                        enabled=fi.enabled,
                        priority=fi.priority,
                        tool_count=tool_count,
                    )
                )
            return enriched

        return families

    def _count_tools(self, config_path: str, project_root: Path) -> int | None:
        """Attempt to count tool_resolution entries in a family config file.

        CV-013B: Called by list_families() to populate ToolFamilyInfo.tool_count
        for --list-families display (UC-004 Step 3). Returns None when the config
        file cannot be read (missing, malformed, or not YAML).

        Args:
            config_path: Family config path, relative to project_root.
            project_root: Absolute project root for path resolution.

        Returns:
            Number of tool_resolution entries, or None if unreadable.
        """
        try:
            resolved = project_root / config_path
            with open(resolved, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if isinstance(data, dict):
                return len(data.get("tool_resolution", []))
        except Exception:
            pass
        return None

    def _parse_registry(self) -> list[ToolFamilyInfo]:
        """Parse tool_families.yaml into ToolFamilyInfo objects.

        SR-005 (FIX-15): Validates that each family entry contains all
        required keys before constructing ToolFamilyInfo. Missing keys
        produce clear error messages identifying the entry index and the
        missing key name.

        Returns:
            List of ToolFamilyInfo for each entry in the registry.

        Raises:
            FileNotFoundError: If the registry file does not exist.
            ValueError: If the YAML is malformed or a required key is missing.
        """
        if not self._registry_path.exists():
            msg = f"Family registry not found: {self._registry_path}"
            raise FileNotFoundError(msg)

        with open(self._registry_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict) or "families" not in data:
            msg = (
                f"Family registry must be a YAML mapping with a 'families' key. "
                f"Got: {type(data).__name__}"
            )
            raise ValueError(msg)

        families: list[ToolFamilyInfo] = []
        for idx, entry in enumerate(data["families"]):
            # SR-005 (FIX-15): Per-entry validation with clear error messages.
            for required_key in _REQUIRED_FAMILY_KEYS:
                if required_key not in entry:
                    entry_name = entry.get("name", f"<entry #{idx}>")
                    msg = (
                        f"Family registry entry '{entry_name}' (index {idx}) "
                        f"is missing required key: '{required_key}'. "
                        f"Required keys: {', '.join(_REQUIRED_FAMILY_KEYS)}."
                    )
                    raise ValueError(msg)

            families.append(
                ToolFamilyInfo(
                    name=entry["name"],
                    description=entry.get("description", ""),
                    resolver_module=entry["resolver_module"],
                    resolver_class=entry["resolver_class"],
                    config_path=entry["config_path"],
                    enabled=entry.get("enabled", True),
                    # DA-004/IN-004 (FIX-16): Explicit priority for ordering.
                    # Default 100 keeps existing entries at low priority.
                    priority=entry.get("priority", 100),
                )
            )

        return families

    def _validate_class_name(self, class_name: str) -> None:
        """Validate a resolver class name against a CamelCase identifier pattern.

        FINDING-003 (CWE-94): Prevents getattr() from retrieving arbitrary module
        attributes via a tampered resolver_class string in tool_families.yaml.
        Enforcing a CamelCase pattern (^[A-Z][a-zA-Z0-9]{1,63}$) excludes dunder
        attributes (__builtins__, __file__), lowercase module imports (subprocess,
        os), and any non-identifier string. Call this after _validate_module_path()
        and BEFORE getattr() so the attribute is never accessed with an invalid name.

        Args:
            class_name: The resolver class name from tool_families.yaml.

        Raises:
            ValueError: If the class name does not match the CamelCase pattern.
        """
        if not _CLASS_NAME_PATTERN.match(class_name):
            msg = (
                f"Resolver class name '{class_name}' is invalid. "
                "Must be a CamelCase Python identifier (2-64 characters, "
                "starting with an uppercase letter, containing only letters and digits)."
            )
            raise ValueError(msg)

    def _validate_module_path(self, module_path: str) -> None:
        """Validate that a module path is within the allowed prefix set.

        This is the M-01 mitigation for T-01 (importlib arbitrary code execution).
        Calling importlib.import_module() on an attacker-controlled module path
        executes arbitrary Python at import time -- before any interface check
        can run. The allowlist gate must execute BEFORE the import call.

        Args:
            module_path: Dotted Python module path from tool_families.yaml.

        Raises:
            ValueError: If the module path is not within an allowed prefix.
        """
        if not any(module_path.startswith(prefix) for prefix in _ALLOWED_MODULE_PREFIXES):
            msg = (
                f"Module path '{module_path}' is not in the allowed prefix list. "
                f"Allowed prefixes: {_ALLOWED_MODULE_PREFIXES}. "
                f"Only modules under src.tool_exec.infrastructure.adapters. "
                f"may be loaded as family resolvers."
            )
            raise ValueError(msg)

    def _load_resolver(self, family_info: ToolFamilyInfo) -> ToolFamilyResolverPort:
        """Dynamically import and instantiate a resolver.

        Validates the module path against the allowlist BEFORE calling
        importlib.import_module(). This prevents arbitrary code execution
        if tool_families.yaml is modified to reference a malicious module
        (T-01 mitigation, DREAD 38 -> 18 post-mitigation).

        Args:
            family_info: Family descriptor with module and class names.

        Returns:
            Instantiated resolver implementing ToolFamilyResolverPort.

        Raises:
            ImportError: If the resolver module cannot be imported.
            AttributeError: If the resolver class is not found in the module.
            ValueError: If the module path is outside the allowed prefix list,
                or if the resolver does not implement ToolFamilyResolverPort.
        """
        # M-01: Validate module path against allowlist BEFORE import.
        # The issubclass check on line below runs AFTER import -- the damage
        # from malicious __init__.py code is done at import time. Guard first.
        self._validate_module_path(family_info.resolver_module)
        # FINDING-003 (CWE-94): Validate class name against CamelCase pattern
        # BEFORE getattr(). Constrains attribute access to class identifiers only,
        # preventing retrieval of dunder attributes, module-level imports, or
        # arbitrary callables from the allowed module.
        self._validate_class_name(family_info.resolver_class)
        module = importlib.import_module(family_info.resolver_module)
        resolver_cls = getattr(module, family_info.resolver_class)

        if not issubclass(resolver_cls, ToolFamilyResolverPort):
            msg = (
                f"Resolver class {family_info.resolver_class} in module "
                f"{family_info.resolver_module} does not implement "
                f"ToolFamilyResolverPort"
            )
            raise ValueError(msg)

        # SR-005: Resolve config_path to absolute using the registry file's parent
        # directory as the base. Relative paths in tool_families.yaml are relative
        # to the project root (where the registry lives), not to cwd.
        config_path = family_info.config_path
        if not Path(config_path).is_absolute():
            config_path = str((self._registry_path.parent / config_path).resolve())
        return resolver_cls(config_path=config_path)  # type: ignore[call-arg]
