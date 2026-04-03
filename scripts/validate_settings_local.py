#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Validate .claude/settings.local.json against schema and skill registry.

Checks:
1. JSON schema validation against claude-code-settings-v1.schema.json
2. Skill entries match CLAUDE.md registered skills (drift detection)
3. No deprecated :* Bash syntax
4. No undocumented Skill(jerry:name) form

Usage:
    uv run python scripts/validate_settings_local.py
    uv run python scripts/validate_settings_local.py --check  # exit 1 on failure

References:
    - #181: Skill permission pattern cleanup
    - #182: Bash syntax migration
    - S-004 PM-001: Skill registry drift detection
    - S-004 PM-004: No automated validation gate
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def main() -> int:
    """Validate settings.local.json."""
    check_mode = "--check" in sys.argv
    project_root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    warnings: list[str] = []

    # --- Load files ---
    settings_path = project_root / ".claude" / "settings.local.json"
    schema_path = project_root / "docs" / "schemas" / "claude-code-settings-v1.schema.json"
    claude_md_path = project_root / "CLAUDE.md"

    if not settings_path.exists():
        print(f"SKIP: {settings_path} not found (gitignored, per-developer file)")
        return 0

    with open(settings_path) as f:
        settings = json.load(f)

    allow = settings.get("permissions", {}).get("allow", [])

    # --- Check 1: Schema validation ---
    if schema_path.exists():
        try:
            from jsonschema import Draft7Validator

            with open(schema_path) as f:
                schema = json.load(f)
            validator = Draft7Validator(schema)
            schema_errors = list(validator.iter_errors(settings))
            if schema_errors:
                for e in schema_errors:
                    errors.append(f"Schema: {e.json_path}: {e.message}")
        except ImportError:
            warnings.append("jsonschema not installed — schema validation skipped")
    else:
        warnings.append(f"Schema not found at {schema_path} — validation skipped")

    # --- Check 2: Skill registry drift ---
    if claude_md_path.exists():
        claude_md = claude_md_path.read_text()
        # Extract skill names from the skills table in CLAUDE.md
        # Pattern: | `/skill-name` |
        registered_skills = set(re.findall(r"\| `/([\w-]+)` \|", claude_md))
        # Extract Skill() entries from settings
        settings_skills = set()
        for entry in allow:
            m = re.match(r"Skill\((.+)\)", entry)
            if m:
                settings_skills.add(m.group(1))

        missing = registered_skills - settings_skills
        extra = settings_skills - registered_skills

        if missing:
            errors.append(f"Skills in CLAUDE.md but NOT in settings.local.json: {sorted(missing)}")
        if extra:
            warnings.append(f"Skills in settings.local.json but NOT in CLAUDE.md: {sorted(extra)}")

    # --- Check 3: Deprecated :* syntax ---
    colon_entries = [e for e in allow if ":*" in e]
    if colon_entries:
        errors.append(f"Deprecated :* syntax in {len(colon_entries)} entries: {colon_entries}")

    # --- Check 4: Undocumented Skill(jerry:name) form ---
    jerry_entries = [e for e in allow if "jerry:" in e]
    if jerry_entries:
        errors.append(
            f"Undocumented Skill(jerry:name) form in {len(jerry_entries)} entries: {jerry_entries}"
        )

    # --- Check 5: $schema field present ---
    if "$schema" not in settings:
        warnings.append("Missing $schema field — editor validation disabled")

    # --- Report ---
    print(f"Validated: {settings_path}")
    print(f"  Entries: {len(allow)}")
    print(f"  Skills: {sum(1 for e in allow if e.startswith('Skill('))}")
    print(f"  MCP: {sum(1 for e in allow if e.startswith('mcp__'))}")
    print(f"  Bash: {sum(1 for e in allow if e.startswith('Bash('))}")

    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        if check_mode:
            return 1
    else:
        print("\nAll checks passed.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
