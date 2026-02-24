#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Fix governance YAML files: correct tool_tier + ensure P-020 in constitution.

Usage: uv run python scripts/fix_governance.py [--dry-run]
"""

import re
import sys
from pathlib import Path

AGENTS_ROOT = Path("skills")


def compute_tier(md_path: Path) -> str:
    """Compute correct tool_tier from the .md file's official frontmatter."""
    content = md_path.read_text(encoding="utf-8")
    # Extract frontmatter
    if not content.startswith("---"):
        return "T1"
    m = re.search(r"\n---\s*\n", content[3:])
    if not m:
        return "T1"
    fm = content[3 : m.start() + 3]

    # Parse tools
    tools_match = re.search(r"^tools:\s*(.+)$", fm, re.MULTILINE)
    tools = set()
    if tools_match:
        tools = {t.strip() for t in tools_match.group(1).split(",")}

    # Parse mcpServers
    has_context7 = "context7:" in fm
    has_memory_keeper = "memory-keeper:" in fm

    # Tier algorithm (no agent should have Task after transform)
    if has_memory_keeper:
        return "T4"  # Persistent state is higher trust than external access
    if has_context7 or "WebSearch" in tools or "WebFetch" in tools:
        return "T3"
    if tools & {"Write", "Edit", "Bash"}:
        return "T2"
    return "T1"


def fix_governance(gov_path: Path, md_path: Path, dry_run: bool) -> tuple[bool, str]:
    """Fix a single governance YAML file."""
    if not gov_path.exists():
        return False, f"SKIP (no file): {gov_path}"
    if not md_path.exists():
        return False, f"SKIP (no md): {md_path}"

    content = gov_path.read_text(encoding="utf-8")
    original = content
    changes = []

    # Fix 1: Correct tool_tier
    correct_tier = compute_tier(md_path)
    tier_match = re.search(r"^tool_tier:\s*(\S+)", content, re.MULTILINE)
    if tier_match:
        current_tier = tier_match.group(1)
        if current_tier != correct_tier:
            content = content.replace(f"tool_tier: {current_tier}", f"tool_tier: {correct_tier}", 1)
            changes.append(f"tier {current_tier}->{correct_tier}")

    # Fix 2: Ensure P-020 in constitution.principles_applied
    if "P-020" not in content:
        # Find the principles_applied block and add P-020
        # Look for the pattern where P-003 or P-022 are listed
        if "principles_applied:" in content:
            # Add P-020 after P-003 line or before P-022 line
            p003_match = re.search(r"(  - '[^']*P-003[^']*')\n", content)
            if p003_match:
                insert_after = p003_match.end()
                p020_line = "  - 'P-020: User Authority (Hard)'\n"
                content = content[:insert_after] + p020_line + content[insert_after:]
                changes.append("added P-020 to constitution")
            else:
                # Try adding before P-022
                p022_match = re.search(r"(  - '[^']*P-022[^']*')", content)
                if p022_match:
                    insert_before = p022_match.start()
                    p020_line = "  - 'P-020: User Authority (Hard)'\n"
                    content = content[:insert_before] + p020_line + content[insert_before:]
                    changes.append("added P-020 to constitution")

    # Fix 3: Ensure P-020 reference in forbidden_actions
    if "forbidden_actions:" in content:
        fa_section = content[content.index("forbidden_actions:") :]
        if "P-020" not in fa_section.split("\n\n")[0]:
            # Find the line after "Spawn recursive subagents (P-003)"
            p003_fa = re.search(r"(  - Spawn recursive subagents \(P-003\))\n", content)
            if p003_fa:
                insert_after = p003_fa.end()
                p020_fa = "  - Override user decisions (P-020)\n"
                content = content[:insert_after] + p020_fa + content[insert_after:]
                changes.append("added P-020 to forbidden_actions")

    if content == original:
        return True, f"OK (no changes): {gov_path.name}"

    if dry_run:
        return True, f"DRY: {gov_path.name} -> {', '.join(changes)}"

    gov_path.write_text(content, encoding="utf-8")
    return True, f"FIXED: {gov_path.name} -> {', '.join(changes)}"


def main():
    dry_run = "--dry-run" in sys.argv
    results = []

    for agents_dir in sorted(AGENTS_ROOT.glob("*/agents/")):
        for gov_file in sorted(agents_dir.glob("*.governance.yaml")):
            md_file = gov_file.with_suffix("").with_suffix(".md")
            results.append(fix_governance(gov_file, md_file, dry_run))

    fixed = sum(1 for _, msg in results if msg.startswith("FIXED"))
    ok = sum(1 for _, msg in results if msg.startswith("OK"))
    dry = sum(1 for _, msg in results if msg.startswith("DRY"))
    skip = sum(1 for _, msg in results if msg.startswith("SKIP"))

    print(
        f"\n{'DRY RUN ' if dry_run else ''}Results: {fixed} fixed, {ok} unchanged, {dry} dry, {skip} skipped, {len(results)} total"
    )
    for _, msg in results:
        if not msg.startswith("OK"):
            print(f"  {msg}")


if __name__ == "__main__":
    main()
