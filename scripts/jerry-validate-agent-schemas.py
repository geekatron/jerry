#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Agent Schema CI Validation Script (PROJ-012 Phase 4, L5 Post-Hoc Verification).

Discovers all agent definition files under skills/*/agents/, extracts YAML
frontmatter, deep-merges with base defaults, validates against the canonical
JSON Schema, cross-references tools against TOOL_REGISTRY.yaml, and checks
H-35 constitutional triplet compliance.

Standalone: does NOT import from src/. All logic is inline.

Exit codes:
    0 -- All agents pass validation.
    1 -- One or more agents fail validation.
    2 -- Script-level error (missing files, parse failures).

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - H-34: Agent definition YAML MUST validate against JSON Schema
    - H-35: Constitutional triplet (P-003, P-020, P-022) REQUIRED
    - agent-development-standards.md: Canonical agent definition standards
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_CONSTITUTIONAL_TRIPLET = {"P-003", "P-020", "P-022"}

_SKIP_FILENAMES = {"README.md", "AGENTS.md"}
_SKIP_SUBSTRINGS = {"TEMPLATE", "EXTENSION"}


# ---------------------------------------------------------------------------
# Repo root discovery
# ---------------------------------------------------------------------------


def find_repo_root() -> Path:
    """Find the repository root by walking up from the script location.

    Looks for ``pyproject.toml`` as the sentinel file.

    Returns:
        Path to the repository root directory.

    Raises:
        SystemExit: If pyproject.toml is not found.
    """
    current = Path(__file__).resolve().parent
    for directory in [current, *current.parents]:
        if (directory / "pyproject.toml").exists():
            return directory
    print("ERROR: Could not find pyproject.toml (repo root)", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# YAML frontmatter extraction
# ---------------------------------------------------------------------------


def extract_frontmatter(agent_file: Path) -> dict[str, Any] | None:
    """Extract YAML frontmatter from an agent markdown file.

    Frontmatter is the content between the opening ``---`` and the
    closing ``---`` delimiters at the top of the file.

    Args:
        agent_file: Path to the agent ``.md`` file.

    Returns:
        Parsed YAML dict, or ``None`` if no valid frontmatter is found.
    """
    try:
        content = agent_file.read_text(encoding="utf-8")
    except OSError:
        return None

    if not content.startswith("---"):
        return None

    try:
        end_idx = content.index("---", 3)
    except ValueError:
        return None

    yaml_str = content[3:end_idx]
    try:
        data = yaml.safe_load(yaml_str)
    except yaml.YAMLError:
        return None

    if not isinstance(data, dict):
        return None

    return data


# ---------------------------------------------------------------------------
# Deep merge
# ---------------------------------------------------------------------------


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep-merge *override* into *base*.

    Merge semantics (per ``jerry-claude-agent-defaults.yaml``):
    - Scalars: override wins.
    - Objects (dicts): recursively deep-merged.
    - Arrays (lists): override replaces base entirely.

    Args:
        base: Base dictionary (modified in place).
        override: Override dictionary.

    Returns:
        Merged dictionary (same reference as *base*).
    """
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


# ---------------------------------------------------------------------------
# Agent file discovery
# ---------------------------------------------------------------------------


def discover_agent_files(skills_dir: Path) -> list[Path]:
    """Discover all agent definition ``.md`` files under ``skills/*/agents/``.

    Excludes README.md, AGENTS.md, and files containing TEMPLATE or EXTENSION
    in their name.

    Args:
        skills_dir: Path to the ``skills/`` directory.

    Returns:
        Sorted list of agent file paths.
    """
    if not skills_dir.is_dir():
        return []

    agents: list[Path] = []
    for agent_file in sorted(skills_dir.glob("*/agents/*.md")):
        if agent_file.name in _SKIP_FILENAMES:
            continue
        if any(sub in agent_file.name for sub in _SKIP_SUBSTRINGS):
            continue
        agents.append(agent_file)

    return agents


# ---------------------------------------------------------------------------
# Tool registry loading
# ---------------------------------------------------------------------------


def load_tool_registry(registry_path: Path) -> set[str]:
    """Load all known tool names from ``TOOL_REGISTRY.yaml``.

    Collects tool names from every category under the ``tools`` key.
    Handles multi-document YAML files by loading the first document only.

    Args:
        registry_path: Path to ``TOOL_REGISTRY.yaml``.

    Returns:
        Set of all registered tool name strings.
    """
    try:
        with open(registry_path, encoding="utf-8") as f:
            # TOOL_REGISTRY.yaml uses multi-document markers (---).
            # safe_load_all handles this; we only need the first document.
            data = next(yaml.safe_load_all(f), None)
    except (OSError, yaml.YAMLError) as exc:
        print(f"ERROR: Cannot load TOOL_REGISTRY.yaml: {exc}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(data, dict):
        print("ERROR: TOOL_REGISTRY.yaml top level is not a mapping", file=sys.stderr)
        sys.exit(2)

    tools_section = data.get("tools", {})
    known_tools: set[str] = set()
    for tool_map in tools_section.values():
        if isinstance(tool_map, dict):
            known_tools.update(tool_map.keys())

    return known_tools


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def validate_schema(
    composed: dict[str, Any],
    validator: Draft202012Validator,
) -> list[str]:
    """Validate composed agent config against JSON Schema.

    Args:
        composed: Fully merged agent configuration dict.
        validator: Pre-built JSON Schema validator.

    Returns:
        List of human-readable validation error strings.
    """
    errors: list[str] = []
    for error in validator.iter_errors(composed):
        path = ".".join(str(p) for p in error.absolute_path) or "(root)"
        errors.append(f"[schema] {path}: {error.message}")
    return errors


def validate_tools_against_registry(
    composed: dict[str, Any],
    known_tools: set[str],
) -> list[str]:
    """Cross-reference agent tools against TOOL_REGISTRY.yaml.

    Checks both ``capabilities.allowed_tools`` (Jerry governance layer) and
    the top-level ``tools`` field (Claude Code native layer).

    Args:
        composed: Fully merged agent configuration dict.
        known_tools: Set of tool names from TOOL_REGISTRY.yaml.

    Returns:
        List of error strings for unregistered tools.
    """
    errors: list[str] = []

    # Check capabilities.allowed_tools (Jerry governance)
    allowed = composed.get("capabilities", {}).get("allowed_tools", [])
    if isinstance(allowed, list):
        for tool in allowed:
            if isinstance(tool, str) and tool not in known_tools:
                errors.append(
                    f"[tool-registry] capabilities.allowed_tools: "
                    f"'{tool}' not found in TOOL_REGISTRY.yaml"
                )

    # Check top-level tools (Claude Code native)
    top_tools = composed.get("tools", [])
    if isinstance(top_tools, list):
        for tool in top_tools:
            if isinstance(tool, str) and tool not in known_tools:
                errors.append(f"[tool-registry] tools: '{tool}' not found in TOOL_REGISTRY.yaml")

    return errors


def validate_constitutional_triplet(composed: dict[str, Any]) -> list[str]:
    """Validate H-35 constitutional triplet compliance.

    Every agent MUST declare P-003, P-020, and P-022 in
    ``constitution.principles_applied``.

    Args:
        composed: Fully merged agent configuration dict.

    Returns:
        List of error strings for missing constitutional principles.
    """
    principles = composed.get("constitution", {}).get("principles_applied", [])
    if not isinstance(principles, list):
        return ["[H-35] constitution.principles_applied is not an array"]

    # Each principle entry is a string like "P-003: No Recursive Subagents (Hard)".
    # Extract the P-NNN prefix from each entry.
    found_codes: set[str] = set()
    for entry in principles:
        if isinstance(entry, str):
            # Match "P-NNN" at the start of the entry
            stripped = entry.strip()
            if stripped.startswith("P-"):
                # Extract up to the first non-digit-or-dash after "P-"
                code = stripped.split(":")[0].split(" ")[0].strip()
                found_codes.add(code)

    missing = _CONSTITUTIONAL_TRIPLET - found_codes
    if missing:
        sorted_missing = sorted(missing)
        return [f"[H-35] constitution.principles_applied missing: {', '.join(sorted_missing)}"]

    return []


# ---------------------------------------------------------------------------
# Per-agent validation
# ---------------------------------------------------------------------------


def validate_agent(
    agent_file: Path,
    defaults: dict[str, Any],
    validator: Draft202012Validator,
    known_tools: set[str],
) -> tuple[str, str, bool, list[str]]:
    """Run all validations on a single agent file.

    Args:
        agent_file: Path to the agent ``.md`` file.
        defaults: Base defaults dictionary (will be deep-copied).
        validator: JSON Schema validator instance.
        known_tools: Set of registered tool names from TOOL_REGISTRY.yaml.

    Returns:
        Tuple of (agent_name, file_path, is_valid, error_list).
    """
    agent_name = agent_file.stem
    file_path = str(agent_file)
    errors: list[str] = []

    # 1. Extract frontmatter
    frontmatter = extract_frontmatter(agent_file)
    if frontmatter is None:
        return (agent_name, file_path, False, ["No valid YAML frontmatter found"])

    # 2. Deep merge defaults + agent frontmatter
    composed = deep_merge(copy.deepcopy(defaults), frontmatter)

    # 3. Use the 'name' from composed config if available
    agent_name = composed.get("name", agent_name)

    # 4. Schema validation
    errors.extend(validate_schema(composed, validator))

    # 5. Tool registry cross-reference
    errors.extend(validate_tools_against_registry(composed, known_tools))

    # 6. H-35 constitutional triplet
    errors.extend(validate_constitutional_triplet(composed))

    is_valid = len(errors) == 0
    return (agent_name, file_path, is_valid, errors)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    """Run agent schema validation across all discovered agents.

    Returns:
        0 if all agents pass, 1 if any fail, 2 on script-level error.
    """
    repo_root = find_repo_root()

    # Resolve paths
    skills_dir = repo_root / "skills"
    schema_path = repo_root / "docs" / "schemas" / "jerry-claude-agent-definition-v1.schema.json"
    defaults_path = repo_root / "docs" / "schemas" / "jerry-claude-agent-defaults.yaml"
    registry_path = repo_root / "TOOL_REGISTRY.yaml"

    # Check required files exist
    missing: list[str] = []
    if not skills_dir.is_dir():
        missing.append(f"skills directory: {skills_dir}")
    if not schema_path.is_file():
        missing.append(f"JSON Schema: {schema_path}")
    if not defaults_path.is_file():
        missing.append(f"Base defaults: {defaults_path}")
    if not registry_path.is_file():
        missing.append(f"Tool registry: {registry_path}")

    if missing:
        for item in missing:
            print(f"ERROR: Required file not found: {item}", file=sys.stderr)
        return 2

    # Load schema
    try:
        with open(schema_path, encoding="utf-8") as f:
            schema = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: Cannot load JSON Schema: {exc}", file=sys.stderr)
        return 2

    # Load defaults
    try:
        with open(defaults_path, encoding="utf-8") as f:
            defaults = yaml.safe_load(f)
            if not isinstance(defaults, dict):
                defaults = {}
    except (OSError, yaml.YAMLError) as exc:
        print(f"ERROR: Cannot load base defaults: {exc}", file=sys.stderr)
        return 2

    # Build validator
    validator = Draft202012Validator(schema)

    # Load tool registry
    known_tools = load_tool_registry(registry_path)

    # Discover agents
    agent_files = discover_agent_files(skills_dir)
    if not agent_files:
        print("WARNING: No agent files found under skills/*/agents/")
        return 0

    # Validate each agent
    total = 0
    passed = 0
    failed = 0
    failure_details: list[tuple[str, str, list[str]]] = []

    for agent_file in agent_files:
        total += 1
        agent_name, file_path, is_valid, errors = validate_agent(
            agent_file, defaults, validator, known_tools
        )

        if is_valid:
            passed += 1
            print(f"  PASS  {agent_name} ({file_path})")
        else:
            failed += 1
            print(f"  FAIL  {agent_name} ({file_path})")
            for err in errors:
                print(f"        {err}")
            failure_details.append((agent_name, file_path, errors))

    # Summary
    print()
    print(f"{'=' * 60}")
    print("Agent Schema Validation Summary")
    print(f"{'=' * 60}")
    print(f"  Total agents:  {total}")
    print(f"  Passed:        {passed}")
    print(f"  Failed:        {failed}")
    print(f"{'=' * 60}")

    if failed > 0:
        print(
            f"\nFAIL: {failed} agent(s) failed validation. Fix errors above and re-run.",
            file=sys.stderr,
        )
        return 1

    print(f"\nPASS: All {total} agent(s) validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
