# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for jerry.testing.evaluation.debiasing — DebiasingStrategy.

Tests the debiasing component for position randomization and rubric shuffling:
    - shuffle_criteria(): criterion order changes, original list preserved
    - randomize_candidate_positions(): swapped flag, label assignment
    - reset_rng(): deterministic reproduction
    - Construction validation: swap_probability range

No LLM calls performed. Uses seed-controlled RNG for determinism.

References:
    - FR-021: Debiasing requirements (C-007)
    - behavioral-contracts.md §B.5: Score stability bounds
      (projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md)
    - H-20: 90% line coverage target
"""

from __future__ import annotations

import pytest

from jerry.testing.evaluation.criterion import QualityCriterion
from jerry.testing.evaluation.debiasing import DebiasingStrategy
from jerry.testing.evaluation.position_randomization_result import (
    PositionRandomizationResult,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_criteria() -> list[QualityCriterion]:
    """Return a list of 6 criteria matching the S-014 dimensions."""
    return [
        QualityCriterion(name="completeness", description="All sections present.", weight=0.20),
        QualityCriterion(
            name="internal_consistency", description="No contradictions.", weight=0.20
        ),
        QualityCriterion(name="methodological_rigor", description="Method followed.", weight=0.20),
        QualityCriterion(name="evidence_quality", description="Evidence cited.", weight=0.15),
        QualityCriterion(name="actionability", description="Actionable.", weight=0.15),
        QualityCriterion(name="traceability", description="Traceable.", weight=0.10),
    ]


@pytest.fixture
def seeded_strategy() -> DebiasingStrategy:
    """Return a DebiasingStrategy with fixed seed=42 for deterministic tests."""
    return DebiasingStrategy(seed=42)


# ---------------------------------------------------------------------------
# Construction validation
# ---------------------------------------------------------------------------


class TestDebiasingStrategyConstruction:
    """Tests for DebiasingStrategy construction and parameter validation."""

    def test_default_construction_succeeds(self) -> None:
        """Default DebiasingStrategy() should construct without error."""
        strategy = DebiasingStrategy()
        assert strategy.seed is None
        assert strategy.swap_probability == 0.5

    def test_seeded_construction_succeeds(self) -> None:
        """DebiasingStrategy with seed=42 should construct without error."""
        strategy = DebiasingStrategy(seed=42)
        assert strategy.seed == 42

    def test_swap_probability_above_one_raises(self) -> None:
        """swap_probability > 1.0 should raise ValueError."""
        with pytest.raises(ValueError):
            DebiasingStrategy(swap_probability=1.01)

    def test_swap_probability_below_zero_raises(self) -> None:
        """swap_probability < 0.0 should raise ValueError."""
        with pytest.raises(ValueError):
            DebiasingStrategy(swap_probability=-0.01)

    def test_swap_probability_boundary_zero(self) -> None:
        """swap_probability=0.0 should be accepted (never swap)."""
        strategy = DebiasingStrategy(swap_probability=0.0)
        assert strategy.swap_probability == 0.0

    def test_swap_probability_boundary_one(self) -> None:
        """swap_probability=1.0 should be accepted (always swap)."""
        strategy = DebiasingStrategy(swap_probability=1.0)
        assert strategy.swap_probability == 1.0


# ---------------------------------------------------------------------------
# shuffle_criteria()
# ---------------------------------------------------------------------------


class TestShuffleCriteria:
    """Tests for DebiasingStrategy.shuffle_criteria()."""

    def test_shuffle_criteria_changes_order(
        self,
        seeded_strategy: DebiasingStrategy,
        sample_criteria: list[QualityCriterion],
    ) -> None:
        """With a fixed seed, shuffled order should differ from original order (FR-021 AC-1)."""
        shuffled = seeded_strategy.shuffle_criteria(sample_criteria)
        # The set of names should be identical
        assert {c.name for c in shuffled} == {c.name for c in sample_criteria}
        # The order should differ (seed=42 produces a specific permutation)
        original_order = [c.name for c in sample_criteria]
        shuffled_order = [c.name for c in shuffled]
        # With 6 elements and seed=42 the order very likely differs
        # (probability of same order = 1/720 ≈ 0.14%)
        assert original_order != shuffled_order

    def test_shuffle_criteria_preserves_all_items(
        self,
        seeded_strategy: DebiasingStrategy,
        sample_criteria: list[QualityCriterion],
    ) -> None:
        """Shuffled list should contain exactly the same criteria (FR-021 AC-1)."""
        shuffled = seeded_strategy.shuffle_criteria(sample_criteria)
        assert len(shuffled) == len(sample_criteria)
        assert {c.name for c in shuffled} == {c.name for c in sample_criteria}

    def test_shuffle_criteria_does_not_mutate_original(
        self,
        seeded_strategy: DebiasingStrategy,
        sample_criteria: list[QualityCriterion],
    ) -> None:
        """shuffle_criteria() must not mutate the original list (FR-021 AC-2)."""
        original_names = [c.name for c in sample_criteria]
        _ = seeded_strategy.shuffle_criteria(sample_criteria)
        assert [c.name for c in sample_criteria] == original_names

    def test_shuffle_criteria_empty_raises(self, seeded_strategy: DebiasingStrategy) -> None:
        """Empty criteria list should raise ValueError."""
        with pytest.raises(ValueError):
            seeded_strategy.shuffle_criteria([])

    def test_shuffle_criteria_single_item_unchanged(
        self, seeded_strategy: DebiasingStrategy
    ) -> None:
        """Single criterion should remain the same after shuffling."""
        criterion = QualityCriterion(name="solo", description="Only one.", weight=0.20)
        shuffled = seeded_strategy.shuffle_criteria([criterion])
        assert len(shuffled) == 1
        assert shuffled[0].name == "solo"

    def test_shuffle_deterministic_with_seed(self, sample_criteria: list[QualityCriterion]) -> None:
        """Two strategies with the same seed should produce the same shuffle."""
        strategy_a = DebiasingStrategy(seed=99)
        strategy_b = DebiasingStrategy(seed=99)
        shuffled_a = [c.name for c in strategy_a.shuffle_criteria(sample_criteria)]
        shuffled_b = [c.name for c in strategy_b.shuffle_criteria(sample_criteria)]
        assert shuffled_a == shuffled_b


# ---------------------------------------------------------------------------
# randomize_candidate_positions()
# ---------------------------------------------------------------------------


class TestRandomizeCandidatePositions:
    """Tests for DebiasingStrategy.randomize_candidate_positions()."""

    def test_randomize_positions_returns_result(self, seeded_strategy: DebiasingStrategy) -> None:
        """randomize_candidate_positions() returns PositionRandomizationResult (FR-021 AC-3)."""
        result = seeded_strategy.randomize_candidate_positions(
            candidate_a="Output A", candidate_b="Output B"
        )
        assert isinstance(result, PositionRandomizationResult)

    def test_randomize_positions_both_candidates_present(
        self, seeded_strategy: DebiasingStrategy
    ) -> None:
        """Both candidates must appear in the result regardless of swap."""
        result = seeded_strategy.randomize_candidate_positions(
            candidate_a="Alpha", candidate_b="Beta"
        )
        candidates = {result.presented_first, result.presented_second}
        assert "Alpha" in candidates
        assert "Beta" in candidates

    def test_randomize_positions_never_swap_probability(self) -> None:
        """swap_probability=0.0 should never swap candidates (FR-021 AC-3)."""
        strategy = DebiasingStrategy(swap_probability=0.0, seed=42)
        result = strategy.randomize_candidate_positions(candidate_a="A", candidate_b="B")
        assert result.swapped is False
        assert result.presented_first == "A"
        assert result.presented_second == "B"

    def test_randomize_positions_always_swap_probability(self) -> None:
        """swap_probability=1.0 should always swap candidates."""
        strategy = DebiasingStrategy(swap_probability=1.0, seed=42)
        result = strategy.randomize_candidate_positions(candidate_a="A", candidate_b="B")
        assert result.swapped is True
        assert result.presented_first == "B"
        assert result.presented_second == "A"

    def test_randomize_positions_labels_preserved(self, seeded_strategy: DebiasingStrategy) -> None:
        """Labels should be correctly assigned to the (possibly swapped) candidates."""
        result = seeded_strategy.randomize_candidate_positions(
            candidate_a="Output A",
            candidate_b="Output B",
            label_a="Baseline",
            label_b="Candidate",
        )
        if result.swapped:
            assert result.label_first == "Candidate"
            assert result.label_second == "Baseline"
        else:
            assert result.label_first == "Baseline"
            assert result.label_second == "Candidate"

    def test_randomize_positions_deterministic_with_seed(self) -> None:
        """Two strategies with the same seed produce the same swap decision."""
        strategy_a = DebiasingStrategy(seed=77)
        strategy_b = DebiasingStrategy(seed=77)
        result_a = strategy_a.randomize_candidate_positions("A", "B")
        result_b = strategy_b.randomize_candidate_positions("A", "B")
        assert result_a.swapped == result_b.swapped


# ---------------------------------------------------------------------------
# reset_rng()
# ---------------------------------------------------------------------------


class TestResetRng:
    """Tests for DebiasingStrategy.reset_rng()."""

    def test_reset_rng_reproduces_sequence(self, sample_criteria: list[QualityCriterion]) -> None:
        """After reset_rng(), a seeded strategy should reproduce the same sequence."""
        strategy = DebiasingStrategy(seed=42)
        shuffled_first = [c.name for c in strategy.shuffle_criteria(sample_criteria)]
        strategy.reset_rng()
        shuffled_second = [c.name for c in strategy.shuffle_criteria(sample_criteria)]
        assert shuffled_first == shuffled_second


# ---------------------------------------------------------------------------
# build_debiased_prompt_section()
# ---------------------------------------------------------------------------


class TestBuildDebiasedPromptSection:
    """Tests for DebiasingStrategy.build_debiased_prompt_section()."""

    def test_prompt_section_contains_criteria(
        self,
        seeded_strategy: DebiasingStrategy,
        sample_criteria: list[QualityCriterion],
    ) -> None:
        """The generated prompt section should include each criterion name."""
        section = seeded_strategy.build_debiased_prompt_section(
            criteria=sample_criteria,
            output_text="Sample output text.",
        )
        for c in sample_criteria:
            assert c.name in section

    def test_prompt_section_truncates_long_output(
        self,
        seeded_strategy: DebiasingStrategy,
        sample_criteria: list[QualityCriterion],
    ) -> None:
        """Output text > 4000 chars should be truncated in the prompt section."""
        long_output = "x" * 5000
        section = seeded_strategy.build_debiased_prompt_section(
            criteria=sample_criteria,
            output_text=long_output,
        )
        assert "truncated" in section.lower()
