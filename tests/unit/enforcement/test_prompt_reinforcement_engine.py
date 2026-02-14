"""
Unit tests for PromptReinforcementEngine and ReinforcementContent.

Tests cover L2-REINJECT marker parsing, token estimation, reinforcement
generation with budget enforcement, error handling (fail-open), and
the ReinforcementContent frozen dataclass behavior.

Test naming follows BDD convention:
    test_{scenario}_when_{condition}_then_{expected}

References:
    - EN-705: L2 Per-Prompt Reinforcement Hook
    - ADR-EPIC002-002: 5-layer enforcement architecture
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.infrastructure.internal.enforcement.prompt_reinforcement_engine import (
    PromptReinforcementEngine,
)
from src.infrastructure.internal.enforcement.reinforcement_content import (
    ReinforcementContent,
)

# =============================================================================
# Sample L2-REINJECT content for tests
# =============================================================================

SAMPLE_QUALITY_ENFORCEMENT = """\
# Quality Enforcement -- Single Source of Truth

<!-- VERSION: 1.2.0 | DATE: 2026-02-14 -->

> Canonical constants for the quality framework.

## HARD Rule Index

<!-- L2-REINJECT: rank=2, tokens=90, content="Quality gate >= 0.92 weighted composite for C2+ deliverables (H-13). Creator-critic-revision cycle REQUIRED, minimum 3 iterations (H-14). Below threshold = REJECTED." -->

<!-- L2-REINJECT: rank=5, tokens=30, content="Self-review REQUIRED before presenting any deliverable (H-15, S-010)." -->

<!-- L2-REINJECT: rank=8, tokens=40, content="Governance escalation REQUIRED per AE rules (H-19). Touches .context/rules/ = auto-C3. Touches constitution = auto-C4." -->

| ID | Rule | Source |
|----|------|--------|
| H-01 | No recursive subagents | P-003 |

## Quality Gate

<!-- L2-REINJECT: rank=6, tokens=100, content="Criticality levels: C1 Routine (reversible 1 session, HARD only). C2 Standard (reversible 1 day, HARD+MEDIUM). C3 Significant (>1 day, all tiers). C4 Critical (irreversible, all tiers + tournament). AE-002: .context/rules/ = auto-C3. AE-001/AE-004: constitution/baselined ADR = auto-C4." -->

**Threshold:** >= 0.92 weighted composite score
"""


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def rules_file(tmp_path: Path) -> Path:
    """Create a quality-enforcement.md file with L2-REINJECT markers."""
    rules_path = tmp_path / "quality-enforcement.md"
    rules_path.write_text(SAMPLE_QUALITY_ENFORCEMENT, encoding="utf-8")
    return rules_path


@pytest.fixture
def engine(rules_file: Path) -> PromptReinforcementEngine:
    """Create a PromptReinforcementEngine with the test rules file."""
    return PromptReinforcementEngine(rules_path=rules_file)


# =============================================================================
# TestParseReinjectMarkers
# =============================================================================


class TestParseReinjectMarkers:
    """Tests for parsing L2-REINJECT HTML comments from content."""

    def test_parse_markers_when_valid_content_then_extracts_all(self) -> None:
        """All valid L2-REINJECT markers should be extracted."""
        markers = PromptReinforcementEngine._parse_reinject_markers(SAMPLE_QUALITY_ENFORCEMENT)
        assert len(markers) == 4

    def test_parse_markers_when_valid_content_then_sorted_by_rank(self) -> None:
        """Markers should be sorted by rank ascending."""
        markers = PromptReinforcementEngine._parse_reinject_markers(SAMPLE_QUALITY_ENFORCEMENT)
        ranks = [m["rank"] for m in markers]
        assert ranks == sorted(ranks)
        assert ranks == [2, 5, 6, 8]

    def test_parse_markers_when_valid_content_then_preserves_content(self) -> None:
        """Marker content strings should be preserved exactly."""
        markers = PromptReinforcementEngine._parse_reinject_markers(SAMPLE_QUALITY_ENFORCEMENT)
        # First marker (rank=2) content
        assert "Quality gate >= 0.92" in str(markers[0]["content"])
        assert "H-13" in str(markers[0]["content"])

    def test_parse_markers_when_valid_content_then_extracts_tokens(self) -> None:
        """Token values should be extracted as integers."""
        markers = PromptReinforcementEngine._parse_reinject_markers(SAMPLE_QUALITY_ENFORCEMENT)
        token_values = [m["tokens"] for m in markers]
        assert token_values == [90, 30, 100, 40]

    def test_parse_markers_when_empty_content_then_returns_empty(self) -> None:
        """Empty content should return an empty list."""
        markers = PromptReinforcementEngine._parse_reinject_markers("")
        assert markers == []

    def test_parse_markers_when_no_markers_then_returns_empty(self) -> None:
        """Content without L2-REINJECT markers should return empty list."""
        content = "# Just a heading\n\nSome text without markers."
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert markers == []

    def test_parse_markers_when_malformed_marker_then_skips_it(self) -> None:
        """Malformed markers should be silently skipped."""
        content = (
            '<!-- L2-REINJECT: rank=1, tokens=10, content="Valid marker." -->\n'
            '<!-- L2-REINJECT: rank=bad, tokens=10, content="Bad rank." -->\n'
            '<!-- L2-REINJECT: rank=3, tokens=10, content="Another valid." -->\n'
        )
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 2
        assert markers[0]["rank"] == 1
        assert markers[1]["rank"] == 3

    def test_parse_markers_when_single_marker_then_returns_one(self) -> None:
        """A single valid marker should be returned in a list of one."""
        content = '<!-- L2-REINJECT: rank=1, tokens=20, content="Single item." -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 1
        assert markers[0]["content"] == "Single item."
        assert markers[0]["rank"] == 1
        assert markers[0]["tokens"] == 20


# =============================================================================
# TestEstimateTokens
# =============================================================================


class TestEstimateTokens:
    """Tests for token estimation using chars/4 * 0.83 formula."""

    def test_estimate_tokens_when_empty_text_then_returns_zero(self) -> None:
        """Empty text should return 0 tokens."""
        assert PromptReinforcementEngine._estimate_tokens("") == 0

    def test_estimate_tokens_when_short_text_then_returns_positive(self) -> None:
        """Short text should return a positive token count."""
        result = PromptReinforcementEngine._estimate_tokens("Hello world")
        assert result > 0

    def test_estimate_tokens_when_known_length_then_matches_formula(self) -> None:
        """Token count should follow the chars/4 * 0.83 formula."""
        # 100 chars -> 100/4 * 0.83 = 20.75 -> ceil = 21
        text = "x" * 100
        result = PromptReinforcementEngine._estimate_tokens(text)
        assert result == 21

    def test_estimate_tokens_when_exact_division_then_no_extra(self) -> None:
        """When formula gives exact integer, no rounding-up should occur."""
        # Need chars/4 * 0.83 to be exact integer
        # 400 chars -> 400/4 * 0.83 = 83.0 -> 83 (no rounding)
        text = "x" * 400
        result = PromptReinforcementEngine._estimate_tokens(text)
        assert result == 83

    def test_estimate_tokens_when_single_char_then_returns_one(self) -> None:
        """A single character should return 1 token (ceil of fraction)."""
        result = PromptReinforcementEngine._estimate_tokens("x")
        # 1/4 * 0.83 = 0.2075 -> ceil = 1
        assert result == 1

    def test_estimate_tokens_when_four_chars_then_correct(self) -> None:
        """Four characters should give a known token count."""
        result = PromptReinforcementEngine._estimate_tokens("abcd")
        # 4/4 * 0.83 = 0.83 -> ceil = 1
        assert result == 1


# =============================================================================
# TestGenerateReinforcement
# =============================================================================


class TestGenerateReinforcement:
    """Tests for full reinforcement generation."""

    def test_generate_reinforcement_when_valid_file_then_returns_content(
        self, engine: PromptReinforcementEngine
    ) -> None:
        """Engine should return non-empty reinforcement from valid rules file."""
        result = engine.generate_reinforcement()
        assert result.preamble != ""
        assert result.items_included > 0
        assert result.items_total == 4

    def test_generate_reinforcement_when_valid_file_then_includes_ranked_items(
        self, engine: PromptReinforcementEngine
    ) -> None:
        """Preamble should include content from L2-REINJECT markers."""
        result = engine.generate_reinforcement()
        # rank=2 item should be included (highest priority)
        assert "Quality gate >= 0.92" in result.preamble

    def test_generate_reinforcement_when_valid_file_then_token_estimate_positive(
        self, engine: PromptReinforcementEngine
    ) -> None:
        """Token estimate should be positive for non-empty preamble."""
        result = engine.generate_reinforcement()
        assert result.token_estimate > 0

    def test_generate_reinforcement_when_valid_file_then_items_total_correct(
        self, engine: PromptReinforcementEngine
    ) -> None:
        """items_total should reflect all markers found, not just included."""
        result = engine.generate_reinforcement()
        assert result.items_total == 4

    def test_generate_reinforcement_when_called_twice_then_same_result(
        self, engine: PromptReinforcementEngine
    ) -> None:
        """Engine should produce deterministic results across calls."""
        result1 = engine.generate_reinforcement()
        result2 = engine.generate_reinforcement()
        assert result1.preamble == result2.preamble
        assert result1.token_estimate == result2.token_estimate
        assert result1.items_included == result2.items_included


# =============================================================================
# TestBudgetEnforcement
# =============================================================================


class TestBudgetEnforcement:
    """Tests for 600-token budget constraint verification."""

    def test_budget_enforcement_when_default_budget_then_within_limit(
        self, engine: PromptReinforcementEngine
    ) -> None:
        """Generated reinforcement should fit within 600-token budget."""
        result = engine.generate_reinforcement()
        assert result.token_estimate <= 600

    def test_budget_enforcement_when_tiny_budget_then_limits_items(self, rules_file: Path) -> None:
        """A very small budget should limit how many items are included."""
        engine = PromptReinforcementEngine(rules_path=rules_file, token_budget=10)
        result = engine.generate_reinforcement()
        # With only 10 tokens, should include very few or no items
        assert result.items_included < 4

    def test_budget_enforcement_when_zero_budget_then_empty_preamble(
        self, rules_file: Path
    ) -> None:
        """A zero-token budget should produce an empty preamble."""
        engine = PromptReinforcementEngine(rules_path=rules_file, token_budget=0)
        result = engine.generate_reinforcement()
        assert result.preamble == ""
        assert result.items_included == 0
        assert result.token_estimate == 0

    def test_budget_enforcement_when_large_budget_then_includes_all(self, rules_file: Path) -> None:
        """A very large budget should include all items."""
        engine = PromptReinforcementEngine(rules_path=rules_file, token_budget=10000)
        result = engine.generate_reinforcement()
        assert result.items_included == result.items_total
        assert result.items_included == 4

    def test_budget_enforcement_when_exact_budget_for_first_item_then_includes_one(
        self, tmp_path: Path
    ) -> None:
        """Budget exactly matching one item should include exactly one."""
        content = (
            '<!-- L2-REINJECT: rank=1, tokens=10, content="Short." -->\n'
            '<!-- L2-REINJECT: rank=2, tokens=10, content="Another short." -->\n'
        )
        rules_path = tmp_path / "quality-enforcement.md"
        rules_path.write_text(content, encoding="utf-8")

        # "Short." = 6 chars -> 6/4*0.83 = 1.245 -> 2 tokens
        # Set budget to 2 to exactly fit the first item
        engine = PromptReinforcementEngine(rules_path=rules_path, token_budget=2)
        result = engine.generate_reinforcement()
        assert result.items_included >= 1


# =============================================================================
# TestErrorHandling
# =============================================================================


class TestErrorHandling:
    """Tests for fail-open error handling."""

    def test_generate_reinforcement_when_missing_file_then_returns_empty(
        self, tmp_path: Path
    ) -> None:
        """Missing rules file should return empty reinforcement (fail-open)."""
        nonexistent = tmp_path / "nonexistent.md"
        engine = PromptReinforcementEngine(rules_path=nonexistent)
        result = engine.generate_reinforcement()

        assert result.preamble == ""
        assert result.token_estimate == 0
        assert result.items_included == 0
        assert result.items_total == 0

    def test_generate_reinforcement_when_empty_file_then_returns_empty(
        self, tmp_path: Path
    ) -> None:
        """Empty rules file should return empty reinforcement."""
        empty_file = tmp_path / "quality-enforcement.md"
        empty_file.write_text("", encoding="utf-8")
        engine = PromptReinforcementEngine(rules_path=empty_file)
        result = engine.generate_reinforcement()

        assert result.preamble == ""
        assert result.items_included == 0

    def test_generate_reinforcement_when_no_markers_in_file_then_returns_empty(
        self, tmp_path: Path
    ) -> None:
        """File without L2-REINJECT markers should return empty reinforcement."""
        no_markers = tmp_path / "quality-enforcement.md"
        no_markers.write_text(
            "# Quality Rules\n\nJust regular content, no markers.\n",
            encoding="utf-8",
        )
        engine = PromptReinforcementEngine(rules_path=no_markers)
        result = engine.generate_reinforcement()

        assert result.preamble == ""
        assert result.items_included == 0
        assert result.items_total == 0

    def test_generate_reinforcement_when_all_malformed_markers_then_returns_empty(
        self, tmp_path: Path
    ) -> None:
        """File with only malformed markers should return empty reinforcement."""
        malformed = tmp_path / "quality-enforcement.md"
        malformed.write_text(
            '<!-- L2-REINJECT: rank=bad, tokens=bad, content="Broken." -->\n'
            "<!-- L2-REINJECT: missing everything -->\n"
            "<!-- Not even a reinject marker -->\n",
            encoding="utf-8",
        )
        engine = PromptReinforcementEngine(rules_path=malformed)
        result = engine.generate_reinforcement()

        assert result.preamble == ""
        assert result.items_included == 0

    def test_generate_reinforcement_when_directory_as_path_then_returns_empty(
        self, tmp_path: Path
    ) -> None:
        """Passing a directory instead of file should return empty (fail-open)."""
        engine = PromptReinforcementEngine(rules_path=tmp_path)
        result = engine.generate_reinforcement()

        assert result.preamble == ""
        assert result.items_included == 0


# =============================================================================
# TestReinforcementContent
# =============================================================================


class TestReinforcementContent:
    """Tests for the ReinforcementContent frozen dataclass."""

    def test_reinforcement_content_when_created_then_attributes_accessible(self) -> None:
        """ReinforcementContent should expose all attributes."""
        rc = ReinforcementContent(
            preamble="Test preamble",
            token_estimate=42,
            items_included=2,
            items_total=5,
        )
        assert rc.preamble == "Test preamble"
        assert rc.token_estimate == 42
        assert rc.items_included == 2
        assert rc.items_total == 5

    def test_reinforcement_content_when_frozen_then_immutable(self) -> None:
        """ReinforcementContent should be immutable (frozen dataclass)."""
        rc = ReinforcementContent(
            preamble="Test",
            token_estimate=10,
            items_included=1,
            items_total=1,
        )
        with pytest.raises(Exception):
            rc.preamble = "Modified"  # type: ignore[misc]

    def test_reinforcement_content_when_equal_values_then_equal(self) -> None:
        """Two ReinforcementContent with same values should be equal."""
        rc1 = ReinforcementContent(
            preamble="Same",
            token_estimate=10,
            items_included=1,
            items_total=2,
        )
        rc2 = ReinforcementContent(
            preamble="Same",
            token_estimate=10,
            items_included=1,
            items_total=2,
        )
        assert rc1 == rc2

    def test_reinforcement_content_when_empty_preamble_then_valid(self) -> None:
        """Empty preamble should be a valid ReinforcementContent."""
        rc = ReinforcementContent(
            preamble="",
            token_estimate=0,
            items_included=0,
            items_total=0,
        )
        assert rc.preamble == ""
        assert rc.token_estimate == 0
