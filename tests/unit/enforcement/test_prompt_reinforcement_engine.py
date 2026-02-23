# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

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

    def test_parse_markers_when_no_tokens_field_then_still_parses(self) -> None:
        """Markers without deprecated tokens field should parse correctly (EN-002 R4)."""
        content = '<!-- L2-REINJECT: rank=3, content="Rule without tokens field." -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 1
        assert markers[0]["rank"] == 3
        assert markers[0]["content"] == "Rule without tokens field."
        assert "tokens" not in markers[0]

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

    def test_parse_markers_when_content_too_long_then_rejects(self) -> None:
        """C-06: Content exceeding max length should be rejected."""
        long_content = "x" * 501
        content = f'<!-- L2-REINJECT: rank=1, tokens=200, content="{long_content}" -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 0

    def test_parse_markers_when_content_has_html_comment_then_rejects(self) -> None:
        """C-06: Content containing HTML comment delimiters should be rejected."""
        content = '<!-- L2-REINJECT: rank=1, tokens=20, content="Inject --> escape" -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 0

    def test_parse_markers_when_content_has_script_tag_then_rejects(self) -> None:
        """C-06: Content containing script tags should be rejected."""
        content = '<!-- L2-REINJECT: rank=1, tokens=20, content="<script>alert(1)</script>" -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 0

    def test_parse_markers_when_content_at_max_length_then_accepts(self) -> None:
        """C-06: Content exactly at max length should be accepted."""
        exact_content = "x" * 500
        content = f'<!-- L2-REINJECT: rank=1, tokens=200, content="{exact_content}" -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 1

    def test_parse_markers_when_content_has_mixed_case_script_then_rejects(self) -> None:
        """C-06: Case-insensitive matching should reject mixed-case script tags."""
        content = '<!-- L2-REINJECT: rank=1, tokens=20, content="<ScRiPt>alert(1)</ScRiPt>" -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 0

    def test_parse_markers_when_content_has_iframe_then_rejects(self) -> None:
        """C-06: Content containing iframe tags should be rejected."""
        content = '<!-- L2-REINJECT: rank=1, tokens=20, content="<iframe src=x>" -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 0

    def test_parse_markers_when_content_has_object_tag_then_rejects(self) -> None:
        """C-06: Content containing object tags should be rejected."""
        content = '<!-- L2-REINJECT: rank=1, tokens=20, content="<object data=x>" -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 0

    def test_parse_markers_when_content_has_embed_tag_then_rejects(self) -> None:
        """C-06: Content containing embed tags should be rejected."""
        content = '<!-- L2-REINJECT: rank=1, tokens=20, content="<EMBED src=x>" -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 0

    def test_parse_markers_when_content_has_javascript_uri_then_rejects(self) -> None:
        """C-06: Content containing javascript: URI scheme should be rejected."""
        content = '<!-- L2-REINJECT: rank=1, tokens=20, content="JavaScript:void(0)" -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 0

    def test_parse_markers_when_content_has_data_html_uri_then_rejects(self) -> None:
        """C-06: Content containing data:text/html URI should be rejected."""
        content = '<!-- L2-REINJECT: rank=1, tokens=20, content="data:text/html,payload" -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 0

    def test_parse_markers_when_content_has_svg_tag_then_rejects(self) -> None:
        """C-06: Content containing svg tags should be rejected (eng-security F-01)."""
        content = '<!-- L2-REINJECT: rank=1, tokens=20, content="<svg onload=alert(1)>" -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 0

    def test_parse_markers_when_content_has_event_handler_then_rejects(self) -> None:
        """C-06: Content containing inline event handlers should be rejected (eng-security F-01)."""
        content = '<!-- L2-REINJECT: rank=1, tokens=20, content="<img onerror=alert(1)>" -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 0

    def test_parse_markers_when_content_has_mixed_case_event_handler_then_rejects(self) -> None:
        """C-06: Case-insensitive event handler detection."""
        content = '<!-- L2-REINJECT: rank=1, tokens=20, content="<div OnMouseOver=x>" -->'
        markers = PromptReinforcementEngine._parse_reinject_markers(content)
        assert len(markers) == 0

    def test_parse_markers_when_oversized_content_then_logs_warning(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """C-06: Rejected oversized markers should log a warning."""
        long_content = "x" * 501
        content = f'<!-- L2-REINJECT: rank=1, tokens=200, content="{long_content}" -->'
        with caplog.at_level("WARNING"):
            PromptReinforcementEngine._parse_reinject_markers(content)
        assert "C-06" in caplog.text
        assert "content length" in caplog.text

    def test_parse_markers_when_injection_detected_then_logs_warning(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """C-06: Rejected injection markers should log a warning."""
        content = '<!-- L2-REINJECT: rank=1, tokens=20, content="<script>bad</script>" -->'
        with caplog.at_level("WARNING"):
            PromptReinforcementEngine._parse_reinject_markers(content)
        assert "C-06" in caplog.text
        assert "injection pattern" in caplog.text


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
    """Tests for 850-token budget constraint verification (EN-002: updated from 600)."""

    def test_budget_enforcement_when_default_budget_then_within_limit(
        self, engine: PromptReinforcementEngine
    ) -> None:
        """Generated reinforcement should fit within 850-token budget (EN-002)."""
        result = engine.generate_reinforcement()
        assert result.token_estimate <= 850

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

    def test_generate_reinforcement_when_empty_directory_then_returns_empty(
        self, tmp_path: Path
    ) -> None:
        """Empty directory (no .md files) should return empty reinforcement."""
        engine = PromptReinforcementEngine(rules_path=tmp_path)
        result = engine.generate_reinforcement()

        assert result.preamble == ""
        assert result.items_included == 0


# =============================================================================
# TestMultiFileReading
# =============================================================================


class TestMultiFileReading:
    """Tests for reading L2-REINJECT markers from multiple files in a directory."""

    def test_multi_file_when_directory_with_multiple_md_files_then_reads_all(
        self, tmp_path: Path
    ) -> None:
        """Directory with multiple .md files should extract markers from all."""
        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()

        # File 1: quality-enforcement.md with 2 markers
        (rules_dir / "quality-enforcement.md").write_text(
            '<!-- L2-REINJECT: rank=1, tokens=50, content="Constitutional: P-003, P-020, P-022." -->\n'
            '<!-- L2-REINJECT: rank=2, tokens=90, content="Quality gate >= 0.92 for C2+." -->\n',
            encoding="utf-8",
        )

        # File 2: architecture-standards.md with 1 marker
        (rules_dir / "architecture-standards.md").write_text(
            '<!-- L2-REINJECT: rank=4, tokens=60, content="domain/ MUST NOT import application/." -->\n',
            encoding="utf-8",
        )

        # File 3: testing-standards.md with 1 marker
        (rules_dir / "testing-standards.md").write_text(
            '<!-- L2-REINJECT: rank=5, tokens=40, content="Test before implement (BDD Red phase)." -->\n',
            encoding="utf-8",
        )

        engine = PromptReinforcementEngine(rules_path=rules_dir, token_budget=850)
        result = engine.generate_reinforcement()

        assert result.items_total == 4
        assert result.items_included == 4
        assert "Constitutional" in result.preamble
        assert "Quality gate" in result.preamble
        assert "domain/" in result.preamble
        assert "Test before implement" in result.preamble

    def test_multi_file_when_directory_then_markers_sorted_by_rank_across_files(
        self, tmp_path: Path
    ) -> None:
        """Markers from different files should be sorted by rank globally."""
        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()

        # File with rank 5
        (rules_dir / "z_last_alphabetically.md").write_text(
            '<!-- L2-REINJECT: rank=1, tokens=20, content="First by rank." -->\n',
            encoding="utf-8",
        )

        # File with rank 1 (alphabetically first but rank higher)
        (rules_dir / "a_first_alphabetically.md").write_text(
            '<!-- L2-REINJECT: rank=5, tokens=20, content="Last by rank." -->\n',
            encoding="utf-8",
        )

        engine = PromptReinforcementEngine(rules_path=rules_dir, token_budget=850)
        result = engine.generate_reinforcement()

        # rank=1 should come before rank=5 regardless of file order
        assert result.preamble.index("First by rank") < result.preamble.index("Last by rank")

    def test_multi_file_when_directory_with_non_md_files_then_ignores_them(
        self, tmp_path: Path
    ) -> None:
        """Non-.md files in the directory should be ignored."""
        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()

        (rules_dir / "rules.md").write_text(
            '<!-- L2-REINJECT: rank=1, tokens=20, content="From md file." -->\n',
            encoding="utf-8",
        )
        (rules_dir / "config.yaml").write_text(
            '<!-- L2-REINJECT: rank=2, tokens=20, content="From yaml file." -->\n',
            encoding="utf-8",
        )

        engine = PromptReinforcementEngine(rules_path=rules_dir, token_budget=850)
        result = engine.generate_reinforcement()

        assert result.items_total == 1
        assert "From md file" in result.preamble
        assert "From yaml file" not in result.preamble

    def test_multi_file_when_single_file_path_then_backward_compatible(
        self, rules_file: Path
    ) -> None:
        """Passing a single file path should still work (backward compat)."""
        engine = PromptReinforcementEngine(rules_path=rules_file, token_budget=850)
        result = engine.generate_reinforcement()

        assert result.items_total == 4
        assert result.items_included > 0


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
