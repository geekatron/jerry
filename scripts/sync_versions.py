#!/usr/bin/env python3
"""Validate and synchronize Jerry framework version across all locations.

This script reads the SSOT version from pyproject.toml and checks (or fixes)
all other version locations for consistency.

Usage:
    uv run python scripts/sync_versions.py --check   # CI/pre-commit: validate
    uv run python scripts/sync_versions.py --fix      # Developer: force-sync all files

Exit codes:
    0: All versions consistent (--check) or sync successful (--fix)
    1: Version drift detected (--check) or sync failed (--fix)

References:
    - EN-108: Version Bumping Strategy
    - TASK-002: Analysis - Version Locations and Sync Strategy

Note: marketplace.json top-level "version" is a marketplace schema version
(currently 1.0.0) and is intentionally NOT synced with the framework version.
Only plugins[0].version is synced (REV-1 from adversarial review).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def read_ssot_version(project_root: Path) -> str:
    """Read the authoritative version from pyproject.toml."""
    pyproject = project_root / "pyproject.toml"
    content = pyproject.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not match:
        print("ERROR: Could not find version in pyproject.toml")
        sys.exit(1)
    return match.group(1)


def check_plugin_json(project_root: Path, expected: str) -> tuple[bool, str]:
    """Check .claude-plugin/plugin.json version."""
    path = project_root / ".claude-plugin" / "plugin.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    actual = data.get("version", "MISSING")
    ok = actual == expected
    return ok, f"plugin.json: {actual}" + ("" if ok else f" (expected {expected})")


def check_marketplace_json(
    project_root: Path,
    expected: str,
) -> tuple[bool, str]:
    """Check .claude-plugin/marketplace.json plugins[0].version.

    Note: The top-level "version" field is the marketplace schema version
    and is intentionally NOT checked (REV-1).
    """
    path = project_root / ".claude-plugin" / "marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    plugins = data.get("plugins", [])
    if not plugins:
        return False, "marketplace.json: No plugins array found"

    plugin_version = plugins[0].get("version", "MISSING")
    ok = plugin_version == expected
    return ok, (
        f"marketplace.json plugins[0].version: {plugin_version}"
        + ("" if ok else f" (expected {expected})")
    )


def check_claude_md(project_root: Path, expected: str) -> tuple[bool, str]:
    """Check CLAUDE.md inline version reference."""
    path = project_root / "CLAUDE.md"
    content = path.read_text(encoding="utf-8")
    # Look for (vX.Y.Z) on a line containing **CLI**
    pattern = r"\*\*CLI\*\*\s+\(v(\d+\.\d+\.\d+[^)]*)\)"
    match = re.search(pattern, content)
    if not match:
        return True, "CLAUDE.md: No version reference found (OK)"
    actual = match.group(1)
    ok = actual == expected
    return ok, f"CLAUDE.md: v{actual}" + ("" if ok else f" (expected v{expected})")


def fix_plugin_json(project_root: Path, version: str) -> None:
    """Fix .claude-plugin/plugin.json version."""
    path = project_root / ".claude-plugin" / "plugin.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = version
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def fix_marketplace_json(project_root: Path, version: str) -> None:
    """Fix .claude-plugin/marketplace.json plugins[0].version.

    Note: Top-level "version" is NOT modified (marketplace schema version).
    """
    path = project_root / ".claude-plugin" / "marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("plugins"):
        data["plugins"][0]["version"] = version
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def fix_claude_md(project_root: Path, version: str) -> None:
    """Fix CLAUDE.md inline version reference."""
    path = project_root / "CLAUDE.md"
    content = path.read_text(encoding="utf-8")
    pattern = r"(\*\*CLI\*\*\s+)\(v\d+\.\d+\.\d+[^)]*\)"
    replacement = rf"\1(v{version})"
    new_content = re.sub(pattern, replacement, content, count=1)
    path.write_text(new_content, encoding="utf-8")


def main() -> int:
    """Run version sync check or fix."""
    if len(sys.argv) < 2 or sys.argv[1] not in ("--check", "--fix"):
        print("Usage: sync_versions.py [--check | --fix]")
        return 1

    mode = sys.argv[1]
    project_root = get_project_root()
    expected = read_ssot_version(project_root)

    print(f"SSOT version (pyproject.toml): {expected}")
    print(f"Mode: {mode}")
    print()

    if mode == "--check":
        all_ok = True
        checks = [
            check_plugin_json(project_root, expected),
            check_marketplace_json(project_root, expected),
            check_claude_md(project_root, expected),
        ]

        for ok, msg in checks:
            status = "OK" if ok else "DRIFT"
            print(f"  [{status}] {msg}")
            if not ok:
                all_ok = False

        print()
        if all_ok:
            print("All versions consistent.")
            return 0
        else:
            print("ERROR: Version drift detected!")
            print("Run: uv run python scripts/sync_versions.py --fix")
            return 1

    elif mode == "--fix":
        print(f"Syncing all files to version {expected}...")
        fix_plugin_json(project_root, expected)
        fix_marketplace_json(project_root, expected)
        fix_claude_md(project_root, expected)
        print("Done. All files synced.")
        print()
        print("Don't forget to stage the changes:")
        print("  git add .claude-plugin/plugin.json")
        print("  git add .claude-plugin/marketplace.json")
        print("  git add CLAUDE.md")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
