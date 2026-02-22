#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
HARD Rule Ceiling Enforcement Script (EN-002, L5 Post-Hoc Verification).

Counts the number of HARD rules in the quality-enforcement.md HARD Rule Index
table and fails the build if the count exceeds the ceiling. This provides
deterministic L5 enforcement immune to context rot, preventing silent ceiling
breaches like the one that allowed the count to grow from 25 to 35 without
detection.

The ceiling is read from the Tier Vocabulary table in quality-enforcement.md
(the ``<= N`` value in the HARD row's Max Count column).

References:
    - EN-002: HARD Rule Budget Enforcement Improvements
    - DEC-001 D-004: Add L5 CI enforcement gate for HARD rule ceiling
    - quality-enforcement.md: SSOT for HARD rules and ceiling
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# M-08: Independent ceiling constant prevents self-referential bypass.
# Even if quality-enforcement.md's ceiling value is tampered with, the
# absolute maximum provides an independent hard stop. The SSOT ceiling
# MUST be <= this value. Changes to this constant require C4 review.
_ABSOLUTE_MAX_CEILING = 28


def find_quality_enforcement() -> Path:
    """Find quality-enforcement.md relative to the project root."""
    # Walk upward from CWD to find the project root
    current = Path.cwd()
    for parent in [current, *current.parents]:
        candidate = parent / ".context" / "rules" / "quality-enforcement.md"
        if candidate.exists():
            return candidate
    # Fallback: try relative to script location
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    return project_root / ".context" / "rules" / "quality-enforcement.md"


def count_hard_rules(content: str) -> int:
    """Count HARD rules in the HARD Rule Index table.

    Counts rows matching the pattern ``| H-NN |`` in the HARD Rule Index
    section. Only counts unique rule IDs to handle any accidental duplicates.

    Args:
        content: Full text content of quality-enforcement.md.

    Returns:
        Number of unique H-rule entries found.
    """
    # Find the HARD Rule Index section
    section_pattern = r"## HARD Rule Index\b"
    section_match = re.search(section_pattern, content)
    if not section_match:
        print("ERROR: Could not find '## HARD Rule Index' section", file=sys.stderr)
        sys.exit(2)

    # Extract content from section start to next ## heading
    section_start = section_match.end()
    next_section = re.search(r"\n## ", content[section_start:])
    section_end = section_start + next_section.start() if next_section else len(content)
    section_content = content[section_start:section_end]

    # Count unique H-rule IDs in table rows
    rule_ids: set[str] = set()
    for match in re.finditer(r"^\|\s*(H-\d+)\s*\|", section_content, re.MULTILINE):
        rule_ids.add(match.group(1))

    return len(rule_ids)


def read_ceiling(content: str) -> int:
    """Read the HARD rule ceiling from the Tier Vocabulary table.

    Looks for the HARD row in the Tier Vocabulary table and extracts the
    ``<= N`` value from the Max Count column.

    Args:
        content: Full text content of quality-enforcement.md.

    Returns:
        The ceiling value as an integer.
    """
    # Pattern: | **HARD** | ... | ... | <= N |
    ceiling_pattern = r"\|\s*\*\*HARD\*\*\s*\|.*?\|\s*<=\s*(\d+)\s*\|"
    match = re.search(ceiling_pattern, content)
    if not match:
        print("ERROR: Could not find HARD rule ceiling in Tier Vocabulary", file=sys.stderr)
        sys.exit(2)

    ceiling = int(match.group(1))

    # M-08: Independent hard stop prevents self-referential bypass.
    # If SSOT ceiling exceeds the absolute max, someone tampered with the file.
    if ceiling > _ABSOLUTE_MAX_CEILING:
        print(
            f"ERROR: SSOT ceiling ({ceiling}) exceeds absolute maximum "
            f"({_ABSOLUTE_MAX_CEILING}). Ceiling tampering suspected.",
            file=sys.stderr,
        )
        sys.exit(2)

    return ceiling


def main() -> int:
    """Run the HARD rule ceiling check.

    Returns:
        0 if count <= ceiling, 1 if count > ceiling, 2 on parse error.
    """
    qe_path = find_quality_enforcement()
    if not qe_path.exists():
        print(f"ERROR: quality-enforcement.md not found at {qe_path}", file=sys.stderr)
        return 2

    content = qe_path.read_text(encoding="utf-8")
    rule_count = count_hard_rules(content)
    ceiling = read_ceiling(content)

    if rule_count > ceiling:
        print(
            f"FAIL: HARD rule count ({rule_count}) exceeds ceiling ({ceiling}). "
            f"Consolidate rules or use the exception mechanism per EN-002.",
            file=sys.stderr,
        )
        return 1

    headroom = ceiling - rule_count
    print(
        f"PASS: HARD rule count = {rule_count}, ceiling = {ceiling}, "
        f"headroom = {headroom} slot{'s' if headroom != 1 else ''}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
