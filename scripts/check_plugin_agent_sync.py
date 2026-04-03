#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Plugin Agent Sync Drift Detection Script.

Compares agent .md files discovered on disk under skills/*/agents/ against
the agents array in .claude-plugin/plugin.json and reports any drift.

Drift categories:
  - On disk but NOT in plugin.json  (missing registration)
  - In plugin.json but NOT on disk  (stale / dangling reference)

Exit codes:
  0 -- In sync: every disk file is registered and every registration exists on disk.
  1 -- Drift detected: one or more missing or stale entries found.
  2 -- Parse / IO error: could not read plugin.json or discover files.

Usage:
    uv run python scripts/check_plugin_agent_sync.py
    uv run python scripts/check_plugin_agent_sync.py --json

References:
    - PROJ-024: Plugin/agent sync tactical work
    - H-05: UV-only execution (uv run)
    - H-11: Type annotations on public functions
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def get_project_root() -> Path:
    """Return the repository root directory.

    Resolves relative to this script's location: scripts/ is one level below root.

    Returns:
        Absolute path to the project root.
    """
    return Path(__file__).resolve().parent.parent


def discover_disk_agents(project_root: Path) -> set[str]:
    """Discover all agent .md files under skills/*/agents/ on disk.

    Excludes any paths containing '.graveyard' to avoid picking up retired agents.

    Args:
        project_root: Absolute path to the repository root.

    Returns:
        Set of paths in the canonical './skills/...' relative format used by plugin.json.
    """
    skills_root = project_root / "skills"
    if not skills_root.exists():
        return set()

    result: set[str] = set()
    for agent_file in skills_root.glob("*/agents/*.md"):
        # Exclude .graveyard directories anywhere in the path
        if ".graveyard" in agent_file.parts:
            continue
        # Normalise to the './skills/...' format used in plugin.json
        relative = "./" + agent_file.relative_to(project_root).as_posix()
        result.add(relative)

    return result


def read_plugin_agents(project_root: Path) -> set[str]:
    """Read the agents array from .claude-plugin/plugin.json.

    Args:
        project_root: Absolute path to the repository root.

    Returns:
        Set of agent path strings as declared in plugin.json.

    Raises:
        FileNotFoundError: If plugin.json does not exist.
        ValueError: If plugin.json is not valid JSON or lacks an 'agents' key.
    """
    plugin_path = project_root / ".claude-plugin" / "plugin.json"
    if not plugin_path.exists():
        raise FileNotFoundError(f"plugin.json not found at {plugin_path}")

    try:
        data: dict = json.loads(plugin_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in plugin.json: {exc}") from exc

    if "agents" not in data:
        raise ValueError("plugin.json does not contain an 'agents' key")

    return set(data["agents"])


def check_sync(
    disk_agents: set[str],
    plugin_agents: set[str],
) -> tuple[list[str], list[str]]:
    """Compare disk agents against plugin.json registrations.

    Args:
        disk_agents: Paths of agent files found on disk.
        plugin_agents: Paths declared in plugin.json agents array.

    Returns:
        Tuple of (missing_from_plugin, stale_in_plugin):
            missing_from_plugin -- on disk but not in plugin.json
            stale_in_plugin     -- in plugin.json but not on disk
    """
    missing_from_plugin = sorted(disk_agents - plugin_agents)
    stale_in_plugin = sorted(plugin_agents - disk_agents)
    return missing_from_plugin, stale_in_plugin


def build_json_report(
    missing_from_plugin: list[str],
    stale_in_plugin: list[str],
    disk_count: int,
    plugin_count: int,
) -> dict:
    """Build a structured JSON report of the sync check results.

    Args:
        missing_from_plugin: Agents on disk but absent from plugin.json.
        stale_in_plugin: Agents in plugin.json that have no file on disk.
        disk_count: Total agents discovered on disk.
        plugin_count: Total agents registered in plugin.json.

    Returns:
        Dictionary suitable for JSON serialisation.
    """
    in_sync = not missing_from_plugin and not stale_in_plugin
    return {
        "in_sync": in_sync,
        "disk_count": disk_count,
        "plugin_count": plugin_count,
        "missing_from_plugin": missing_from_plugin,
        "stale_in_plugin": stale_in_plugin,
    }


def main() -> int:
    """Run the plugin agent sync drift check.

    Returns:
        0 if in sync, 1 if drift detected, 2 on error.
    """
    parser = argparse.ArgumentParser(
        description="Check that skills/*/agents/*.md files match plugin.json agents array.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=("Exit codes:\n  0  In sync\n  1  Drift detected\n  2  Parse / IO error\n"),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON (suitable for CI consumption).",
    )
    args = parser.parse_args()

    project_root = get_project_root()

    try:
        disk_agents = discover_disk_agents(project_root)
        plugin_agents = read_plugin_agents(project_root)
    except (FileNotFoundError, ValueError) as exc:
        if args.json:
            print(json.dumps({"error": str(exc)}, indent=2))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    missing_from_plugin, stale_in_plugin = check_sync(disk_agents, plugin_agents)
    in_sync = not missing_from_plugin and not stale_in_plugin

    if args.json:
        report = build_json_report(
            missing_from_plugin,
            stale_in_plugin,
            len(disk_agents),
            len(plugin_agents),
        )
        print(json.dumps(report, indent=2))
        return 0 if in_sync else 1

    # Human-readable output
    print(f"Disk agents   : {len(disk_agents)}")
    print(f"Plugin agents : {len(plugin_agents)}")
    print()

    if missing_from_plugin:
        print(
            f"MISSING from plugin.json ({len(missing_from_plugin)} agent(s) on disk but not registered):"
        )
        for path in missing_from_plugin:
            print(f"  + {path}")
        print()

    if stale_in_plugin:
        print(
            f"STALE in plugin.json ({len(stale_in_plugin)} registration(s) with no file on disk):"
        )
        for path in stale_in_plugin:
            print(f"  - {path}")
        print()

    if in_sync:
        print(f"PASS: plugin.json is in sync with disk ({len(disk_agents)} agents).")
        return 0

    print("FAIL: plugin.json is out of sync with disk. Add missing entries or remove stale ones.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
