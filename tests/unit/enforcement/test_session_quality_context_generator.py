# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for SessionQualityContextGenerator and QualityContext.

Tests cover preamble generation, exact content verification, token budget
enforcement, dataclass immutability, and token estimation accuracy.

Test naming follows BDD convention:
    test_{scenario}_when_{condition}_then_{expected}

References:
    - EN-706: SessionStart Quality Context Injection
    - EPIC-002 EN-405/TASK-006: Quality preamble specification
"""

from __future__ import annotations

import pytest

from src.infrastructure.internal.enforcement.quality_context import (
    QualityContext,
)
from src.infrastructure.internal.enforcement.session_quality_context_generator import (
    SessionQualityContextGenerator,
)

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def generator() -> SessionQualityContextGenerator:
    """Create a SessionQualityContextGenerator instance."""
    return SessionQualityContextGenerator()


@pytest.fixture
def quality_context(generator: SessionQualityContextGenerator) -> QualityContext:
    """Generate a QualityContext from the generator."""
    return generator.generate()


# =============================================================================
# TestGenerate: Full generation produces correct structure
# =============================================================================


class TestGenerate:
    """Tests for the generate() method producing complete output."""

    def test_generate_when_called_then_returns_quality_context(
        self, generator: SessionQualityContextGenerator
    ) -> None:
        """generate() returns a QualityContext instance."""
        result = generator.generate()

        assert isinstance(result, QualityContext)

    def test_generate_when_called_then_preamble_is_nonempty_string(
        self, quality_context: QualityContext
    ) -> None:
        """generate() produces a non-empty preamble string."""
        assert isinstance(quality_context.preamble, str)
        assert len(quality_context.preamble) > 0

    def test_generate_when_called_then_includes_all_four_sections(
        self, quality_context: QualityContext
    ) -> None:
        """generate() reports 4 sections included."""
        assert quality_context.sections_included == 4

    def test_generate_when_called_then_token_estimate_is_positive(
        self, quality_context: QualityContext
    ) -> None:
        """generate() produces a positive token estimate."""
        assert quality_context.token_estimate > 0

    def test_generate_when_called_then_preamble_starts_with_quality_framework_tag(
        self, quality_context: QualityContext
    ) -> None:
        """Preamble starts with the quality-framework XML opening tag."""
        assert quality_context.preamble.startswith('<quality-framework version="1.0">')

    def test_generate_when_called_then_preamble_ends_with_closing_tag(
        self, quality_context: QualityContext
    ) -> None:
        """Preamble ends with the quality-framework XML closing tag."""
        assert quality_context.preamble.rstrip().endswith("</quality-framework>")

    def test_generate_when_called_multiple_times_then_returns_identical_results(
        self, generator: SessionQualityContextGenerator
    ) -> None:
        """Multiple calls produce identical results (deterministic)."""
        result1 = generator.generate()
        result2 = generator.generate()

        assert result1.preamble == result2.preamble
        assert result1.token_estimate == result2.token_estimate
        assert result1.sections_included == result2.sections_included


# =============================================================================
# TestPreambleContent: Exact content verification
# =============================================================================


class TestPreambleContent:
    """Tests for exact preamble content verification."""

    def test_preamble_content_when_generated_then_contains_quality_gate_section(
        self, quality_context: QualityContext
    ) -> None:
        """Preamble contains the quality-gate section."""
        assert "<quality-gate>" in quality_context.preamble
        assert "</quality-gate>" in quality_context.preamble

    def test_preamble_content_when_generated_then_contains_constitutional_principles_section(
        self, quality_context: QualityContext
    ) -> None:
        """Preamble contains the constitutional-principles section."""
        assert "<constitutional-principles>" in quality_context.preamble
        assert "</constitutional-principles>" in quality_context.preamble

    def test_preamble_content_when_generated_then_contains_adversarial_strategies_section(
        self, quality_context: QualityContext
    ) -> None:
        """Preamble contains the adversarial-strategies section."""
        assert "<adversarial-strategies>" in quality_context.preamble
        assert "</adversarial-strategies>" in quality_context.preamble

    def test_preamble_content_when_generated_then_contains_decision_criticality_section(
        self, quality_context: QualityContext
    ) -> None:
        """Preamble contains the decision-criticality section."""
        assert "<decision-criticality>" in quality_context.preamble
        assert "</decision-criticality>" in quality_context.preamble

    def test_preamble_content_when_generated_then_contains_quality_target(
        self, quality_context: QualityContext
    ) -> None:
        """Preamble specifies the 0.92 quality target."""
        assert ">= 0.92" in quality_context.preamble

    def test_preamble_content_when_generated_then_contains_hard_constraints(
        self, quality_context: QualityContext
    ) -> None:
        """Preamble contains all three HARD constitutional principles."""
        assert "P-003" in quality_context.preamble
        assert "P-020" in quality_context.preamble
        assert "P-022" in quality_context.preamble

    def test_preamble_content_when_generated_then_contains_all_ten_strategies(
        self, quality_context: QualityContext
    ) -> None:
        """Preamble contains all 10 adversarial strategies."""
        expected_strategies = [
            "S-014",
            "S-007",
            "S-010",
            "S-003",
            "S-002",
            "S-013",
            "S-004",
            "S-012",
            "S-011",
            "S-001",
        ]
        for strategy in expected_strategies:
            assert strategy in quality_context.preamble, (
                f"Strategy {strategy} missing from preamble"
            )

    def test_preamble_content_when_generated_then_contains_all_criticality_levels(
        self, quality_context: QualityContext
    ) -> None:
        """Preamble contains all four criticality levels C1-C4."""
        assert "C1 (Routine)" in quality_context.preamble
        assert "C2 (Standard)" in quality_context.preamble
        assert "C3 (Significant)" in quality_context.preamble
        assert "C4 (Critical)" in quality_context.preamble

    def test_preamble_content_when_generated_then_contains_uv_constraint(
        self, quality_context: QualityContext
    ) -> None:
        """Preamble references UV-only Python environment constraint."""
        assert "UV only" in quality_context.preamble
        assert "uv run" in quality_context.preamble

    def test_preamble_content_when_generated_then_contains_auto_escalate_rules(
        self, quality_context: QualityContext
    ) -> None:
        """Preamble contains AUTO-ESCALATE rules for governance."""
        assert "AUTO-ESCALATE" in quality_context.preamble
        assert "governance files/rules -> C3+" in quality_context.preamble


# =============================================================================
# TestTokenBudget: Preamble under 700 tokens
# =============================================================================


class TestTokenBudget:
    """Tests for token budget constraint enforcement."""

    def test_token_budget_when_generated_then_under_700_tokens(
        self, quality_context: QualityContext
    ) -> None:
        """Preamble token estimate stays under the 700-token budget."""
        assert quality_context.token_estimate <= 700

    def test_token_budget_when_generated_then_estimate_is_reasonable(
        self, quality_context: QualityContext
    ) -> None:
        """Token estimate is within a reasonable range (not trivially small)."""
        # The preamble is substantial XML (~1800 chars), so tokens should be > 200
        assert quality_context.token_estimate > 200


# =============================================================================
# TestQualityContext: Frozen dataclass behavior
# =============================================================================


class TestQualityContext:
    """Tests for QualityContext dataclass immutability."""

    def test_quality_context_when_created_then_attributes_accessible(self) -> None:
        """QualityContext attributes are accessible after creation."""
        ctx = QualityContext(
            preamble="<test/>",
            token_estimate=10,
            sections_included=1,
        )

        assert ctx.preamble == "<test/>"
        assert ctx.token_estimate == 10
        assert ctx.sections_included == 1

    def test_quality_context_when_frozen_then_mutation_raises_error(self) -> None:
        """QualityContext is immutable (frozen dataclass)."""
        ctx = QualityContext(
            preamble="<test/>",
            token_estimate=10,
            sections_included=1,
        )

        with pytest.raises(AttributeError):
            ctx.preamble = "modified"  # type: ignore[misc]

    def test_quality_context_when_same_values_then_equal(self) -> None:
        """QualityContext instances with identical values are equal."""
        ctx1 = QualityContext(preamble="<a/>", token_estimate=5, sections_included=1)
        ctx2 = QualityContext(preamble="<a/>", token_estimate=5, sections_included=1)

        assert ctx1 == ctx2


# =============================================================================
# TestEstimateTokens: Token estimation accuracy
# =============================================================================


class TestEstimateTokens:
    """Tests for the _estimate_tokens static method."""

    def test_estimate_tokens_when_empty_string_then_returns_zero(self) -> None:
        """Empty string produces zero token estimate."""
        result = SessionQualityContextGenerator._estimate_tokens("")

        assert result == 0

    def test_estimate_tokens_when_short_string_then_returns_small_value(self) -> None:
        """Short string produces a proportionally small token estimate."""
        # 40 chars -> 40/4 * 0.83 = 8.3 -> 8
        result = SessionQualityContextGenerator._estimate_tokens("a" * 40)

        assert result == 8

    def test_estimate_tokens_when_known_length_then_matches_formula(self) -> None:
        """Token estimate matches the chars/4 * 0.83 formula exactly."""
        text = "x" * 100
        expected = int(100 / 4 * 0.83)  # 20

        result = SessionQualityContextGenerator._estimate_tokens(text)

        assert result == expected

    def test_estimate_tokens_when_realistic_xml_then_reasonable_estimate(self) -> None:
        """Realistic XML content produces a reasonable token estimate."""
        xml_content = "<section>\n  Some content with spaces and tags.\n</section>"
        result = SessionQualityContextGenerator._estimate_tokens(xml_content)

        # Should be positive and reasonable for ~56 chars
        assert result > 0
        assert result < 50

    def test_estimate_tokens_when_returns_integer_then_type_is_int(self) -> None:
        """Token estimate is always an integer (not float)."""
        result = SessionQualityContextGenerator._estimate_tokens("test string")

        assert isinstance(result, int)
