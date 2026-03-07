#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Fix governance YAML schema validation failures.

Issues:
1. output_filtering items are objects instead of strings
2. output.levels is a mapping instead of array
3. audience_level has invalid enum values

Usage: uv run python scripts/fix_governance_schema.py [--dry-run]
"""

import sys
from pathlib import Path

import yaml

AGENTS_ROOT = Path("skills")
VALID_AUDIENCE = {"adaptive", "expert", "intermediate", "beginner"}


def fix_output_filtering(data: dict) -> list[str]:
    """Convert object output_filtering items to strings."""
    changes = []
    guardrails = data.get("guardrails", {})
    if not isinstance(guardrails, dict):
        return changes
    filtering = guardrails.get("output_filtering", [])
    if not isinstance(filtering, list):
        return changes

    new_items = []
    changed = False
    for item in filtering:
        if isinstance(item, dict):
            # Convert {key: value} to just key as string
            for k in item:
                new_items.append(str(k))
            changed = True
        elif isinstance(item, str):
            new_items.append(item)
        else:
            new_items.append(str(item))
            changed = True

    if changed:
        guardrails["output_filtering"] = new_items
        changes.append("output_filtering: objects->strings")
    return changes


def fix_output_levels(data: dict) -> list[str]:
    """Convert mapping output.levels to array format."""
    changes = []
    output = data.get("output", {})
    if not isinstance(output, dict):
        return changes
    levels = output.get("levels")
    if levels is None:
        return changes

    # If it's already an array, check items
    if isinstance(levels, list):
        return changes

    # If it's a mapping like {L0: {name:..., content:...}}, convert to enum array
    if isinstance(levels, dict):
        enum_keys = []
        for k in levels:
            if k in ("L0", "L1", "L2"):
                enum_keys.append(k)
        if enum_keys:
            output["levels"] = enum_keys
            changes.append(f"output.levels: mapping->[{','.join(enum_keys)}]")
    return changes


def fix_audience_level(data: dict) -> list[str]:
    """Fix invalid audience_level values."""
    changes = []
    persona = data.get("persona", {})
    if not isinstance(persona, dict):
        return changes
    level = persona.get("audience_level")
    if level is not None and level not in VALID_AUDIENCE:
        persona["audience_level"] = "adaptive"
        changes.append(f"audience_level: '{level}'->'adaptive'")
    return changes


def fix_file(path: Path, dry_run: bool) -> tuple[bool, str]:
    """Fix a single governance file."""
    content = path.read_text(encoding="utf-8")
    data = yaml.safe_load(content)
    if not isinstance(data, dict):
        return False, f"SKIP: {path.name} (not a dict)"

    changes = []
    changes.extend(fix_output_filtering(data))
    changes.extend(fix_output_levels(data))
    changes.extend(fix_audience_level(data))

    if not changes:
        return True, f"OK: {path.name}"

    if dry_run:
        return True, f"DRY: {path.name} -> {', '.join(changes)}"

    # Preserve header comments
    header_lines = []
    for line in content.splitlines():
        if line.startswith("#") or line.strip() == "":
            header_lines.append(line)
        else:
            break
    header = "\n".join(header_lines) + "\n" if header_lines else ""

    new_yaml = yaml.dump(
        data, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120
    )
    path.write_text(header + new_yaml, encoding="utf-8")
    return True, f"FIXED: {path.name} -> {', '.join(changes)}"


def main():
    dry_run = "--dry-run" in sys.argv
    results = []

    for gov_file in sorted(AGENTS_ROOT.glob("*/agents/*.governance.yaml")):
        results.append(fix_file(gov_file, dry_run))

    fixed = sum(1 for _, m in results if m.startswith("FIXED"))
    ok = sum(1 for _, m in results if m.startswith("OK"))
    print(
        f"\n{'DRY RUN ' if dry_run else ''}Results: {fixed} fixed, {ok} unchanged, {len(results)} total"
    )
    for _, msg in results:
        if not msg.startswith("OK"):
            print(f"  {msg}")


if __name__ == "__main__":
    main()
