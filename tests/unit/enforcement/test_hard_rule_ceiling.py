# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for the HARD rule ceiling enforcement script.

Validates that the L5 CI gate correctly counts HARD rules and enforces
the ceiling from quality-enforcement.md.

References:
    - EN-002: HARD Rule Budget Enforcement Improvements
    - TASK-027: Add L5 CI enforcement gate for HARD rule ceiling
"""

from __future__ import annotations

import pytest

from scripts.check_hard_rule_ceiling import count_hard_rules, read_ceiling

# --- Fixtures ---

SAMPLE_QE_CONTENT = """\
## HARD Rule Index

> These are the authoritative HARD rules.

| ID | Rule | Source |
|----|------|--------|
| H-01 | No recursive subagents | P-003 |
| H-02 | User authority | P-020 |
| H-03 | No deception | P-022 |
| H-04 | Active project | CLAUDE.md |
| H-05 | UV only | python-environment |

---

## Quality Gate

Some other content.

## Tier Vocabulary

| Tier | Keywords | Override | Max Count |
|------|----------|----------|-----------|
| **HARD** | MUST, SHALL | Cannot override | <= 25 |
| **MEDIUM** | SHOULD | Documented justification | Unlimited |
"""


# --- count_hard_rules ---


class TestCountHardRules:
    """Tests for count_hard_rules function."""

    def test_count_when_valid_content_then_returns_correct_count(self) -> None:
        result = count_hard_rules(SAMPLE_QE_CONTENT)
        assert result == 5

    def test_count_when_duplicate_ids_then_counts_unique_only(self) -> None:
        content = SAMPLE_QE_CONTENT.replace(
            "| H-05 | UV only | python-environment |",
            "| H-05 | UV only | python-environment |\n| H-05 | UV duplicate | python-environment |",
        )
        result = count_hard_rules(content)
        assert result == 5

    def test_count_when_no_rules_then_returns_zero(self) -> None:
        content = """\
## HARD Rule Index

> No rules yet.

| ID | Rule | Source |
|----|------|--------|

---

## Quality Gate
"""
        result = count_hard_rules(content)
        assert result == 0

    def test_count_when_section_missing_then_exits(self) -> None:
        with pytest.raises(SystemExit):
            count_hard_rules("## Some Other Section\n\nContent here.")

    def test_count_when_compound_rule_then_counts_as_one(self) -> None:
        content = """\
## HARD Rule Index

| ID | Rule | Source |
|----|------|--------|
| H-07 | Architecture layer isolation (domain, application, composition root) | architecture-standards |
| H-10 | One class per file | architecture-standards |

---

## Quality Gate
"""
        result = count_hard_rules(content)
        assert result == 2


# --- read_ceiling ---


class TestReadCeiling:
    """Tests for read_ceiling function."""

    def test_ceiling_when_valid_content_then_returns_value(self) -> None:
        result = read_ceiling(SAMPLE_QE_CONTENT)
        assert result == 25

    def test_ceiling_when_different_value_then_returns_it(self) -> None:
        # M-08: Value must be <= _ABSOLUTE_MAX_CEILING (35)
        content = SAMPLE_QE_CONTENT.replace("<= 25", "<= 35")
        result = read_ceiling(content)
        assert result == 35

    def test_ceiling_when_exceeds_absolute_max_then_exits(self) -> None:
        # M-08: Independent hard stop prevents self-referential bypass
        content = SAMPLE_QE_CONTENT.replace("<= 25", "<= 40")
        with pytest.raises(SystemExit):
            read_ceiling(content)

    def test_ceiling_when_missing_then_exits(self) -> None:
        with pytest.raises(SystemExit):
            read_ceiling("## Tier Vocabulary\n\nNo table here.")


# --- Integration: ceiling vs count ---


class TestCeilingEnforcement:
    """Integration tests for ceiling enforcement logic."""

    def test_enforcement_when_count_within_ceiling_then_passes(self) -> None:
        count = count_hard_rules(SAMPLE_QE_CONTENT)
        ceiling = read_ceiling(SAMPLE_QE_CONTENT)
        assert count <= ceiling

    def test_enforcement_when_count_exceeds_ceiling_then_fails(self) -> None:
        # Create content with 26 rules but ceiling of 25
        rules = "\n".join(f"| H-{i:02d} | Rule {i} | source |" for i in range(1, 27))
        content = f"""\
## HARD Rule Index

| ID | Rule | Source |
|----|------|--------|
{rules}

---

## Tier Vocabulary

| Tier | Keywords | Override | Max Count |
|------|----------|----------|-----------|
| **HARD** | MUST | Cannot override | <= 25 |
"""
        count = count_hard_rules(content)
        ceiling = read_ceiling(content)
        assert count > ceiling
        assert count == 26


# --- Validate against actual quality-enforcement.md ---


class TestActualFile:
    """Validate the ceiling check against the real quality-enforcement.md."""

    def test_actual_file_count_within_ceiling(self) -> None:
        """The actual HARD rule count must not exceed the ceiling."""
        from pathlib import Path

        qe_path = Path(".context/rules/quality-enforcement.md")
        if not qe_path.exists():
            pytest.skip("quality-enforcement.md not found")

        content = qe_path.read_text(encoding="utf-8")
        count = count_hard_rules(content)
        ceiling = read_ceiling(content)

        assert count <= ceiling, (
            f"HARD rule count ({count}) exceeds ceiling ({ceiling}). "
            f"Consolidate rules or use exception mechanism per EN-002."
        )
