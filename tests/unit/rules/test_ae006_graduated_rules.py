# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for AE-006 graduated sub-rules in quality-enforcement.md.

Tests verify that the Auto-Escalation Rules table in
.context/rules/quality-enforcement.md contains the correct graduated
sub-rules AE-006a through AE-006e, and that the L2-REINJECT marker
for AE-006 graduated escalation exists with the correct content.

Also verifies the total L2-REINJECT token budget stays within 600
tokens (the per-prompt budget from ADR-EPIC002-002).

Test naming follows BDD convention:
    test_{scenario}_when_{condition}_then_{expected}

References:
    - ST-002: AE-006 Graduated Sub-Rules
    - PROJ-004: Context Resilience
    - ADR-EPIC002-002: 5-layer enforcement architecture (L2 budget: ~600/prompt)
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Fixture: load the quality-enforcement.md file once per test session
# ---------------------------------------------------------------------------

RULES_FILE = Path(__file__).parents[3] / ".context" / "rules" / "quality-enforcement.md"


@pytest.fixture(scope="module")
def quality_enforcement_content() -> str:
    """Load quality-enforcement.md content."""
    assert RULES_FILE.exists(), f"Rules file not found: {RULES_FILE}"
    return RULES_FILE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def auto_escalation_section(quality_enforcement_content: str) -> str:
    """Extract the Auto-Escalation Rules section from the document."""
    # Match from the ## Auto-Escalation Rules heading to the next --- separator
    match = re.search(
        r"## Auto-Escalation Rules\n(.*?)\n---",
        quality_enforcement_content,
        re.DOTALL,
    )
    assert match is not None, "Auto-Escalation Rules section not found in quality-enforcement.md"
    return match.group(0)


# ---------------------------------------------------------------------------
# Tests: AE-006 sub-rules presence
# ---------------------------------------------------------------------------


class TestAE006SubRulesExistence:
    """Verify AE-006a through AE-006e all exist in the Auto-Escalation Rules table."""

    @pytest.mark.parametrize(
        "sub_rule_id",
        ["AE-006a", "AE-006b", "AE-006c", "AE-006d", "AE-006e"],
    )
    def test_sub_rule_exists_when_parsing_table_then_found(
        self,
        auto_escalation_section: str,
        sub_rule_id: str,
    ) -> None:
        """Each AE-006 sub-rule must appear in the Auto-Escalation Rules table."""
        assert sub_rule_id in auto_escalation_section, (
            f"Sub-rule {sub_rule_id} not found in Auto-Escalation Rules section.\n"
            f"Section content:\n{auto_escalation_section}"
        )

    def test_original_ae006_replaced_when_parsing_table_then_not_found(
        self,
        auto_escalation_section: str,
    ) -> None:
        """The original monolithic AE-006 row must be replaced by sub-rules."""
        # The old row had exactly "| AE-006 |" — after replacement only sub-rules exist
        # We check that a bare "| AE-006 |" row (without letter suffix) is absent
        old_row_pattern = re.compile(r"\|\s*AE-006\s*\|")
        assert not old_row_pattern.search(auto_escalation_section), (
            "Original AE-006 row (without letter suffix) still present in table. "
            "It should be replaced by AE-006a through AE-006e."
        )


# ---------------------------------------------------------------------------
# Tests: AE-006a content
# ---------------------------------------------------------------------------


class TestAE006aContent:
    """Verify AE-006a maps to NOMINAL/LOW tier with no-action escalation."""

    def test_ae006a_references_nominal_when_parsing_then_found(
        self,
        auto_escalation_section: str,
    ) -> None:
        """AE-006a must reference NOMINAL tier."""
        assert "NOMINAL" in auto_escalation_section, (
            "AE-006a must reference NOMINAL tier in the Auto-Escalation Rules section."
        )

    def test_ae006a_references_low_when_parsing_then_found(
        self,
        auto_escalation_section: str,
    ) -> None:
        """AE-006a must reference LOW tier."""
        # Check the section contains LOW in the context of AE-006a
        lines = auto_escalation_section.splitlines()
        ae006a_lines = [line for line in lines if "AE-006a" in line]
        assert len(ae006a_lines) >= 1, "AE-006a row not found"
        assert "LOW" in ae006a_lines[0] or "LOW" in " ".join(ae006a_lines), (
            "AE-006a row must reference LOW tier."
        )


# ---------------------------------------------------------------------------
# Tests: AE-006b content
# ---------------------------------------------------------------------------


class TestAE006bContent:
    """Verify AE-006b maps to WARNING tier with log+checkpoint escalation."""

    def test_ae006b_references_warning_when_parsing_then_found(
        self,
        auto_escalation_section: str,
    ) -> None:
        """AE-006b must reference WARNING tier."""
        lines = auto_escalation_section.splitlines()
        ae006b_lines = [line for line in lines if "AE-006b" in line]
        assert len(ae006b_lines) >= 1, "AE-006b row not found"
        assert "WARNING" in " ".join(ae006b_lines), (
            "AE-006b row must reference WARNING tier."
        )


# ---------------------------------------------------------------------------
# Tests: AE-006c content
# ---------------------------------------------------------------------------


class TestAE006cContent:
    """Verify AE-006c maps to CRITICAL tier with auto-checkpoint escalation."""

    def test_ae006c_references_critical_when_parsing_then_found(
        self,
        auto_escalation_section: str,
    ) -> None:
        """AE-006c must reference CRITICAL tier."""
        lines = auto_escalation_section.splitlines()
        ae006c_lines = [line for line in lines if "AE-006c" in line]
        assert len(ae006c_lines) >= 1, "AE-006c row not found"
        assert "CRITICAL" in " ".join(ae006c_lines), (
            "AE-006c row must reference CRITICAL tier."
        )


# ---------------------------------------------------------------------------
# Tests: AE-006d content
# ---------------------------------------------------------------------------


class TestAE006dContent:
    """Verify AE-006d maps to EMERGENCY tier with mandatory checkpoint escalation."""

    def test_ae006d_references_emergency_when_parsing_then_found(
        self,
        auto_escalation_section: str,
    ) -> None:
        """AE-006d must reference EMERGENCY tier."""
        lines = auto_escalation_section.splitlines()
        ae006d_lines = [line for line in lines if "AE-006d" in line]
        assert len(ae006d_lines) >= 1, "AE-006d row not found"
        assert "EMERGENCY" in " ".join(ae006d_lines), (
            "AE-006d row must reference EMERGENCY tier."
        )


# ---------------------------------------------------------------------------
# Tests: AE-006e content
# ---------------------------------------------------------------------------


class TestAE006eContent:
    """Verify AE-006e maps to compaction event with human escalation for C3+."""

    def test_ae006e_references_compaction_when_parsing_then_found(
        self,
        auto_escalation_section: str,
    ) -> None:
        """AE-006e must reference compaction event."""
        lines = auto_escalation_section.splitlines()
        ae006e_lines = [line for line in lines if "AE-006e" in line]
        assert len(ae006e_lines) >= 1, "AE-006e row not found"
        row_text = " ".join(ae006e_lines)
        assert "ompaction" in row_text, (
            "AE-006e row must reference compaction event (case-insensitive 'ompaction')."
        )

    def test_ae006e_references_c3_escalation_when_parsing_then_found(
        self,
        auto_escalation_section: str,
    ) -> None:
        """AE-006e must reference C3+ mandatory human escalation."""
        lines = auto_escalation_section.splitlines()
        ae006e_lines = [line for line in lines if "AE-006e" in line]
        assert len(ae006e_lines) >= 1, "AE-006e row not found"
        row_text = " ".join(ae006e_lines)
        assert "C3" in row_text, (
            "AE-006e row must reference C3+ escalation."
        )


# ---------------------------------------------------------------------------
# Tests: L2-REINJECT marker for AE-006 graduated escalation
# ---------------------------------------------------------------------------


class TestAE006L2ReInjectMarker:
    """Verify the L2-REINJECT marker for AE-006 graduated escalation exists."""

    def test_l2_reinject_ae006_marker_exists_when_parsing_then_found(
        self,
        quality_enforcement_content: str,
    ) -> None:
        """An L2-REINJECT marker summarising AE-006 graduated escalation must exist."""
        assert "AE-006 graduated escalation" in quality_enforcement_content, (
            "L2-REINJECT marker with 'AE-006 graduated escalation' content not found "
            "in quality-enforcement.md."
        )

    def test_l2_reinject_ae006_marker_references_tiers_when_parsing_then_found(
        self,
        quality_enforcement_content: str,
    ) -> None:
        """The AE-006 L2-REINJECT marker must reference the 5 threshold tiers."""
        # Find the L2-REINJECT line that contains AE-006 graduated escalation
        lines = quality_enforcement_content.splitlines()
        marker_lines = [
            line for line in lines
            if "L2-REINJECT" in line and "AE-006 graduated escalation" in line
        ]
        assert len(marker_lines) >= 1, (
            "No L2-REINJECT marker with 'AE-006 graduated escalation' found."
        )
        marker_text = marker_lines[0]
        for tier in ("NOMINAL", "WARNING", "CRITICAL", "EMERGENCY", "COMPACTION"):
            assert tier in marker_text, (
                f"AE-006 L2-REINJECT marker must reference tier '{tier}'. "
                f"Marker: {marker_text}"
            )

    def test_l2_reinject_ae006_uses_rank9_when_parsing_then_correct(
        self,
        quality_enforcement_content: str,
    ) -> None:
        """The AE-006 L2-REINJECT marker must use rank=9 to avoid collision with rank=8."""
        lines = quality_enforcement_content.splitlines()
        marker_lines = [
            line for line in lines
            if "L2-REINJECT" in line and "AE-006 graduated escalation" in line
        ]
        assert len(marker_lines) >= 1, (
            "No L2-REINJECT marker with 'AE-006 graduated escalation' found."
        )
        assert "rank=9" in marker_lines[0], (
            f"AE-006 L2-REINJECT marker must use rank=9. Found: {marker_lines[0]}"
        )


# ---------------------------------------------------------------------------
# Tests: Total L2-REINJECT token budget
# ---------------------------------------------------------------------------


class TestL2ReInjectTokenBudget:
    """Verify total L2-REINJECT token budget stays within 600 tokens."""

    def test_total_token_budget_within_limit_when_parsing_then_passes(
        self,
        quality_enforcement_content: str,
    ) -> None:
        """Sum of all L2-REINJECT token declarations must be <= 600."""
        # Extract all tokens=<N> values from L2-REINJECT markers
        token_pattern = re.compile(r"<!--\s*L2-REINJECT:.*?tokens=(\d+).*?-->")
        matches = token_pattern.findall(quality_enforcement_content)
        assert len(matches) > 0, (
            "No L2-REINJECT markers found in quality-enforcement.md."
        )
        total_tokens = sum(int(t) for t in matches)
        assert total_tokens <= 600, (
            f"Total L2-REINJECT token budget {total_tokens} exceeds 600-token limit. "
            f"Individual token values: {matches}"
        )
