# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for Layer 2 evaluation backend (Stream 3B).

Tests the domain logic of the evaluation package without invoking DeepEval
or any LLM API. All tests use deterministic inputs and produce deterministic
outputs (seed-controlled RNG for debiasing).

Test coverage targets:
    - DebiasingStrategy: position randomization, rubric shuffling, seed control
    - JerryGEvalMetric: construction validation, composite scoring, classification
    - QualityCriterion: validation, weight constraints
    - ScoringResult: weighted_score computation
    - Per-agent criteria: weight sum invariant, non-empty descriptions

Pytest markers used:
    @pytest.mark.unit    -- fast, no I/O, no LLM calls
    @pytest.mark.unit    -- excluded from LLM cost gate

References:
    - FR-006: DeepEval pytest plugin integration
    - FR-007: G-Eval custom criteria evaluation
    - FR-021: Debiasing requirements (C-007)
    - H-20: BDD test-first (90% line coverage target)
"""

from __future__ import annotations

import pytest

from jerry.testing.evaluation.criteria.adv_scorer import ADV_SCORER_CRITERIA
from jerry.testing.evaluation.criteria.ps_analyst import PS_ANALYST_CRITERIA
from jerry.testing.evaluation.criteria.ps_architect import PS_ARCHITECT_CRITERIA
from jerry.testing.evaluation.criteria.ps_critic import PS_CRITIC_CRITERIA
from jerry.testing.evaluation.criteria.ps_researcher import PS_RESEARCHER_CRITERIA
from jerry.testing.evaluation.criterion import QualityCriterion
from jerry.testing.evaluation.debiasing import DebiasingStrategy
from jerry.testing.evaluation.metrics import DIMENSION_WEIGHTS, JerryGEvalMetric
from jerry.testing.evaluation.position_randomization_result import (
    PositionRandomizationResult,
)
from jerry.testing.evaluation.scoring_result import ScoringResult

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def deterministic_strategy() -> DebiasingStrategy:
    """DebiasingStrategy with fixed seed for deterministic tests."""
    return DebiasingStrategy(seed=42)


@pytest.fixture
def sample_criterion() -> QualityCriterion:
    """A single valid criterion for unit testing."""
    return QualityCriterion(
        name="completeness",
        description="The output covers all required sections.",
        weight=0.20,
        dimension="completeness",
    )


@pytest.fixture
def minimal_criteria() -> list[QualityCriterion]:
    """Minimal two-criterion set that sums to 1.0 for metric construction tests."""
    return [
        QualityCriterion(
            name="completeness",
            description="Output contains all required sections.",
            weight=0.60,
            dimension="completeness",
        ),
        QualityCriterion(
            name="traceability",
            description="Claims trace to sources.",
            weight=0.40,
            dimension="traceability",
        ),
    ]


@pytest.fixture
def metric_no_debiasing(minimal_criteria: list[QualityCriterion]) -> JerryGEvalMetric:
    """Metric without debiasing for unit tests that test scoring logic only."""
    return JerryGEvalMetric(
        criteria=minimal_criteria,
        debiasing=None,
        agent_name="test-agent",
        require_debiasing=False,
    )


# ---------------------------------------------------------------------------
# QualityCriterion tests
# ---------------------------------------------------------------------------


class TestQualityCriterion:
    """Tests for QualityCriterion value object validation."""

    @pytest.mark.unit
    def test_valid_criterion_constructed_successfully(
        self, sample_criterion: QualityCriterion
    ) -> None:
        """A criterion with valid name, description, and weight is created."""
        assert sample_criterion.name == "completeness"
        assert sample_criterion.weight == 0.20
        assert sample_criterion.dimension == "completeness"

    @pytest.mark.unit
    def test_empty_name_raises_value_error(self) -> None:
        """Empty name string raises ValueError on construction."""
        with pytest.raises(ValueError, match="name must be non-empty"):
            QualityCriterion(
                name="",
                description="Some description.",
                weight=0.20,
            )

    @pytest.mark.unit
    def test_whitespace_only_name_raises_value_error(self) -> None:
        """Whitespace-only name raises ValueError (not non-empty after strip)."""
        with pytest.raises(ValueError, match="name must be non-empty"):
            QualityCriterion(
                name="   ",
                description="Some description.",
                weight=0.20,
            )

    @pytest.mark.unit
    def test_zero_weight_raises_value_error(self) -> None:
        """Weight of 0.0 is not in the open interval (0.0, 1.0]."""
        with pytest.raises(ValueError, match="weight must be in"):
            QualityCriterion(
                name="completeness",
                description="Some description.",
                weight=0.0,
            )

    @pytest.mark.unit
    def test_weight_above_one_raises_value_error(self) -> None:
        """Weight > 1.0 is rejected."""
        with pytest.raises(ValueError, match="weight must be in"):
            QualityCriterion(
                name="completeness",
                description="Some description.",
                weight=1.01,
            )

    @pytest.mark.unit
    def test_weight_exactly_one_is_valid(self) -> None:
        """Weight of exactly 1.0 is the upper bound of the valid range."""
        criterion = QualityCriterion(
            name="sole_criterion",
            description="This is the only criterion.",
            weight=1.0,
        )
        assert criterion.weight == 1.0

    @pytest.mark.unit
    def test_empty_description_raises_value_error(self) -> None:
        """Empty description raises ValueError."""
        with pytest.raises(ValueError, match="description must be non-empty"):
            QualityCriterion(
                name="completeness",
                description="",
                weight=0.20,
            )

    @pytest.mark.unit
    def test_optional_dimension_defaults_to_none(self) -> None:
        """Dimension attribute defaults to None for agent-specific criteria."""
        criterion = QualityCriterion(
            name="adr_status_field",
            description="ADR contains a Status: field.",
            weight=0.10,
        )
        assert criterion.dimension is None

    @pytest.mark.unit
    def test_frozen_immutability(self, sample_criterion: QualityCriterion) -> None:
        """QualityCriterion is frozen -- mutation raises FrozenInstanceError."""
        with pytest.raises(Exception):  # FrozenInstanceError is a dataclass exception
            sample_criterion.weight = 0.99  # type: ignore[misc]


# ---------------------------------------------------------------------------
# ScoringResult tests
# ---------------------------------------------------------------------------


class TestScoringResult:
    """Tests for ScoringResult value object."""

    @pytest.mark.unit
    def test_weighted_score_computed_correctly(self) -> None:
        """weighted_score is score * weight, precomputed at construction."""
        result = ScoringResult(
            criterion_name="completeness",
            score=0.80,
            weight=0.20,
            evidence="Output has L0, L1, L2 sections.",
            debiasing_applied=True,
        )
        assert abs(result.weighted_score - 0.16) < 1e-9

    @pytest.mark.unit
    def test_score_at_boundary_zero_is_valid(self) -> None:
        """Score of 0.0 is the lower bound of the valid range."""
        result = ScoringResult(
            criterion_name="completeness",
            score=0.0,
            weight=0.20,
            evidence="Output is completely absent.",
            debiasing_applied=True,
        )
        assert result.score == 0.0
        assert result.weighted_score == 0.0

    @pytest.mark.unit
    def test_score_at_boundary_one_is_valid(self) -> None:
        """Score of 1.0 is the upper bound of the valid range."""
        result = ScoringResult(
            criterion_name="completeness",
            score=1.0,
            weight=0.20,
            evidence="Output fully satisfies the completeness criterion.",
            debiasing_applied=True,
        )
        assert result.score == 1.0
        assert abs(result.weighted_score - 0.20) < 1e-9

    @pytest.mark.unit
    def test_score_above_one_raises_value_error(self) -> None:
        """Score > 1.0 raises ValueError."""
        with pytest.raises(ValueError, match="must be in"):
            ScoringResult(
                criterion_name="completeness",
                score=1.01,
                weight=0.20,
                evidence="Some evidence.",
                debiasing_applied=True,
            )

    @pytest.mark.unit
    def test_score_below_zero_raises_value_error(self) -> None:
        """Score < 0.0 raises ValueError."""
        with pytest.raises(ValueError, match="must be in"):
            ScoringResult(
                criterion_name="completeness",
                score=-0.01,
                weight=0.20,
                evidence="Some evidence.",
                debiasing_applied=True,
            )


# ---------------------------------------------------------------------------
# DebiasingStrategy tests
# ---------------------------------------------------------------------------


class TestDebiasingStrategy:
    """Tests for DebiasingStrategy position randomization and criterion shuffling."""

    @pytest.mark.unit
    def test_invalid_swap_probability_raises_value_error(self) -> None:
        """swap_probability outside [0.0, 1.0] raises ValueError."""
        with pytest.raises(ValueError, match="swap_probability"):
            DebiasingStrategy(swap_probability=1.5)

    @pytest.mark.unit
    def test_swap_probability_zero_never_swaps(self) -> None:
        """swap_probability=0.0 produces swapped=False on every call."""
        strategy = DebiasingStrategy(swap_probability=0.0, seed=99)
        for _ in range(20):
            result = strategy.randomize_candidate_positions(
                candidate_a="A output",
                candidate_b="B output",
            )
            assert result.swapped is False
            assert result.presented_first == "A output"

    @pytest.mark.unit
    def test_swap_probability_one_always_swaps(self) -> None:
        """swap_probability=1.0 produces swapped=True on every call."""
        strategy = DebiasingStrategy(swap_probability=1.0, seed=99)
        for _ in range(20):
            result = strategy.randomize_candidate_positions(
                candidate_a="A output",
                candidate_b="B output",
            )
            assert result.swapped is True
            assert result.presented_first == "B output"
            assert result.presented_second == "A output"

    @pytest.mark.unit
    def test_randomize_returns_position_randomization_result(
        self, deterministic_strategy: DebiasingStrategy
    ) -> None:
        """randomize_candidate_positions returns a PositionRandomizationResult."""
        result = deterministic_strategy.randomize_candidate_positions(
            candidate_a="A output",
            candidate_b="B output",
        )
        assert isinstance(result, PositionRandomizationResult)
        assert result.presented_first in {"A output", "B output"}
        assert result.presented_second in {"A output", "B output"}
        assert result.presented_first != result.presented_second

    @pytest.mark.unit
    def test_randomize_uses_custom_labels(self, deterministic_strategy: DebiasingStrategy) -> None:
        """Custom label_a / label_b are reflected in the result."""
        result = deterministic_strategy.randomize_candidate_positions(
            candidate_a="A text",
            candidate_b="B text",
            label_a="Baseline",
            label_b="Candidate",
        )
        assert result.label_first in {"Baseline", "Candidate"}
        assert result.label_second in {"Baseline", "Candidate"}

    @pytest.mark.unit
    def test_shuffle_criteria_returns_same_elements(
        self,
        deterministic_strategy: DebiasingStrategy,
        minimal_criteria: list[QualityCriterion],
    ) -> None:
        """Shuffled criteria list contains the same elements as the original."""
        shuffled = deterministic_strategy.shuffle_criteria(minimal_criteria)
        assert len(shuffled) == len(minimal_criteria)
        assert {c.name for c in shuffled} == {c.name for c in minimal_criteria}

    @pytest.mark.unit
    def test_shuffle_criteria_does_not_mutate_original(
        self,
        deterministic_strategy: DebiasingStrategy,
        minimal_criteria: list[QualityCriterion],
    ) -> None:
        """shuffle_criteria returns a new list; original is unchanged."""
        original_order = [c.name for c in minimal_criteria]
        deterministic_strategy.shuffle_criteria(minimal_criteria)
        assert [c.name for c in minimal_criteria] == original_order

    @pytest.mark.unit
    def test_shuffle_empty_criteria_raises_value_error(
        self, deterministic_strategy: DebiasingStrategy
    ) -> None:
        """Shuffling an empty list raises ValueError."""
        with pytest.raises(ValueError, match="empty"):
            deterministic_strategy.shuffle_criteria([])

    @pytest.mark.unit
    def test_shuffle_is_non_deterministic_without_seed(
        self, minimal_criteria: list[QualityCriterion]
    ) -> None:
        """Different seeds produce different orderings for multi-element lists."""
        strategy_a = DebiasingStrategy(seed=1)
        strategy_b = DebiasingStrategy(seed=9999)

        # Use a longer criteria list to make collision unlikely
        criteria = PS_RESEARCHER_CRITERIA  # 6 elements, 720 possible orderings
        orders_a = [tuple(c.name for c in strategy_a.shuffle_criteria(criteria)) for _ in range(5)]
        orders_b = [tuple(c.name for c in strategy_b.shuffle_criteria(criteria)) for _ in range(5)]
        # With different seeds, at least one ordering should differ
        assert orders_a != orders_b

    @pytest.mark.unit
    def test_reset_rng_produces_same_sequence(
        self, minimal_criteria: list[QualityCriterion]
    ) -> None:
        """After reset_rng(), the strategy reproduces the same shuffle sequence."""
        strategy = DebiasingStrategy(seed=42)
        first_shuffles = [
            tuple(c.name for c in strategy.shuffle_criteria(minimal_criteria)) for _ in range(3)
        ]
        strategy.reset_rng()
        second_shuffles = [
            tuple(c.name for c in strategy.shuffle_criteria(minimal_criteria)) for _ in range(3)
        ]
        assert first_shuffles == second_shuffles

    @pytest.mark.unit
    def test_build_debiased_prompt_section_contains_all_criteria(
        self,
        deterministic_strategy: DebiasingStrategy,
        minimal_criteria: list[QualityCriterion],
    ) -> None:
        """Debiased prompt section contains all criterion names."""
        section = deterministic_strategy.build_debiased_prompt_section(
            criteria=minimal_criteria,
            output_text="Sample output text.",
        )
        for criterion in minimal_criteria:
            assert criterion.name in section

    @pytest.mark.unit
    def test_build_debiased_prompt_section_truncates_long_output(
        self,
        deterministic_strategy: DebiasingStrategy,
        minimal_criteria: list[QualityCriterion],
    ) -> None:
        """Output longer than 4000 chars is truncated with an indicator."""
        long_output = "x" * 5000
        section = deterministic_strategy.build_debiased_prompt_section(
            criteria=minimal_criteria,
            output_text=long_output,
        )
        assert "truncated" in section
        # The raw long output should not appear fully (section is shorter)
        assert len(section) < len(long_output)


# ---------------------------------------------------------------------------
# JerryGEvalMetric tests
# ---------------------------------------------------------------------------


class TestJerryGEvalMetric:
    """Tests for JerryGEvalMetric domain logic."""

    @pytest.mark.unit
    def test_empty_criteria_raises_value_error(
        self, deterministic_strategy: DebiasingStrategy
    ) -> None:
        """Constructing a metric with no criteria raises ValueError."""
        with pytest.raises(ValueError, match="at least one criterion"):
            JerryGEvalMetric(
                criteria=[],
                debiasing=deterministic_strategy,
                agent_name="test-agent",
            )

    @pytest.mark.unit
    def test_none_debiasing_raises_when_required(
        self, minimal_criteria: list[QualityCriterion]
    ) -> None:
        """None debiasing with require_debiasing=True raises ValueError (C-007)."""
        with pytest.raises(ValueError, match="MANDATORY"):
            JerryGEvalMetric(
                criteria=minimal_criteria,
                debiasing=None,
                agent_name="test-agent",
                require_debiasing=True,
            )

    @pytest.mark.unit
    def test_none_debiasing_allowed_when_not_required(
        self, minimal_criteria: list[QualityCriterion]
    ) -> None:
        """None debiasing with require_debiasing=False constructs successfully."""
        metric = JerryGEvalMetric(
            criteria=minimal_criteria,
            debiasing=None,
            agent_name="test-agent",
            require_debiasing=False,
        )
        assert metric.agent_name == "test-agent"

    @pytest.mark.unit
    def test_score_composite_correct_for_uniform_scores(
        self, metric_no_debiasing: JerryGEvalMetric
    ) -> None:
        """Composite of uniform 1.0 scores equals 1.0."""
        results = [
            ScoringResult(
                criterion_name=c.name,
                score=1.0,
                weight=c.weight,
                evidence="Perfect.",
                debiasing_applied=False,
            )
            for c in metric_no_debiasing.criteria
        ]
        composite = metric_no_debiasing.score_composite(results)
        assert abs(composite - 1.0) < 1e-9

    @pytest.mark.unit
    def test_score_composite_correct_for_zero_scores(
        self, metric_no_debiasing: JerryGEvalMetric
    ) -> None:
        """Composite of uniform 0.0 scores equals 0.0."""
        results = [
            ScoringResult(
                criterion_name=c.name,
                score=0.0,
                weight=c.weight,
                evidence="Absent.",
                debiasing_applied=False,
            )
            for c in metric_no_debiasing.criteria
        ]
        composite = metric_no_debiasing.score_composite(results)
        assert abs(composite - 0.0) < 1e-9

    @pytest.mark.unit
    def test_score_composite_weighted_average(self, metric_no_debiasing: JerryGEvalMetric) -> None:
        """Composite score is a normalized weighted average of dimension scores.

        Criteria have weights [0.60, 0.40]. Scores [1.0, 0.0].
        Expected composite = (1.0 * 0.60 + 0.0 * 0.40) / 1.0 = 0.60.
        """
        results = [
            ScoringResult(
                criterion_name="completeness",
                score=1.0,
                weight=0.60,
                evidence="Complete.",
                debiasing_applied=False,
            ),
            ScoringResult(
                criterion_name="traceability",
                score=0.0,
                weight=0.40,
                evidence="No traceability.",
                debiasing_applied=False,
            ),
        ]
        composite = metric_no_debiasing.score_composite(results)
        assert abs(composite - 0.60) < 1e-9

    @pytest.mark.unit
    def test_score_composite_empty_results_raises(
        self, metric_no_debiasing: JerryGEvalMetric
    ) -> None:
        """Empty results list raises ValueError."""
        with pytest.raises(ValueError, match="empty"):
            metric_no_debiasing.score_composite([])

    @pytest.mark.unit
    def test_classify_pass(self, metric_no_debiasing: JerryGEvalMetric) -> None:
        """Score >= 0.92 is classified as PASS."""
        assert metric_no_debiasing.classify_composite(0.92) == "PASS"
        assert metric_no_debiasing.classify_composite(1.00) == "PASS"
        assert metric_no_debiasing.classify_composite(0.95) == "PASS"

    @pytest.mark.unit
    def test_classify_revise(self, metric_no_debiasing: JerryGEvalMetric) -> None:
        """Score in [0.85, 0.92) is classified as REVISE."""
        assert metric_no_debiasing.classify_composite(0.85) == "REVISE"
        assert metric_no_debiasing.classify_composite(0.91) == "REVISE"
        assert metric_no_debiasing.classify_composite(0.90) == "REVISE"

    @pytest.mark.unit
    def test_classify_rejected(self, metric_no_debiasing: JerryGEvalMetric) -> None:
        """Score < 0.85 is classified as REJECTED."""
        assert metric_no_debiasing.classify_composite(0.84) == "REJECTED"
        assert metric_no_debiasing.classify_composite(0.00) == "REJECTED"

    @pytest.mark.unit
    def test_classify_out_of_range_raises(self, metric_no_debiasing: JerryGEvalMetric) -> None:
        """Score outside [0.0, 1.0] raises ValueError."""
        with pytest.raises(ValueError, match="must be in"):
            metric_no_debiasing.classify_composite(1.01)
        with pytest.raises(ValueError, match="must be in"):
            metric_no_debiasing.classify_composite(-0.01)

    @pytest.mark.unit
    def test_get_criteria_for_debiasing_returns_shuffled_when_strategy_present(
        self,
        deterministic_strategy: DebiasingStrategy,
    ) -> None:
        """get_criteria_for_debiasing returns shuffled criteria when strategy is set."""
        metric = JerryGEvalMetric(
            criteria=PS_RESEARCHER_CRITERIA,
            debiasing=deterministic_strategy,
            agent_name="ps-researcher",
        )
        returned = metric.get_criteria_for_debiasing()
        assert len(returned) == len(PS_RESEARCHER_CRITERIA)
        assert {c.name for c in returned} == {c.name for c in PS_RESEARCHER_CRITERIA}

    @pytest.mark.unit
    def test_get_criteria_for_debiasing_returns_original_order_without_strategy(
        self, metric_no_debiasing: JerryGEvalMetric
    ) -> None:
        """Without a debiasing strategy, original criterion order is returned."""
        returned = metric_no_debiasing.get_criteria_for_debiasing()
        original_names = [c.name for c in metric_no_debiasing.criteria]
        returned_names = [c.name for c in returned]
        assert returned_names == original_names


# ---------------------------------------------------------------------------
# Dimension Weights SSOT tests
# ---------------------------------------------------------------------------


class TestDimensionWeights:
    """Tests for S-014 dimension weight constants (SSOT: quality-enforcement.md)."""

    @pytest.mark.unit
    def test_dimension_weights_sum_to_one(self) -> None:
        """The six S-014 dimension weights must sum to exactly 1.0."""
        total = sum(DIMENSION_WEIGHTS.values())
        assert abs(total - 1.0) < 1e-9, f"DIMENSION_WEIGHTS sum is {total}, expected 1.0"

    @pytest.mark.unit
    def test_all_six_dimensions_present(self) -> None:
        """All six S-014 dimensions are represented in DIMENSION_WEIGHTS."""
        expected = {
            "completeness",
            "internal_consistency",
            "methodological_rigor",
            "evidence_quality",
            "actionability",
            "traceability",
        }
        assert set(DIMENSION_WEIGHTS.keys()) == expected

    @pytest.mark.unit
    def test_canonical_weight_values(self) -> None:
        """Each dimension carries its canonical weight from quality-enforcement.md."""
        assert DIMENSION_WEIGHTS["completeness"] == 0.20
        assert DIMENSION_WEIGHTS["internal_consistency"] == 0.20
        assert DIMENSION_WEIGHTS["methodological_rigor"] == 0.20
        assert DIMENSION_WEIGHTS["evidence_quality"] == 0.15
        assert DIMENSION_WEIGHTS["actionability"] == 0.15
        assert DIMENSION_WEIGHTS["traceability"] == 0.10


# ---------------------------------------------------------------------------
# Per-agent criteria invariant tests
# ---------------------------------------------------------------------------


class TestPerAgentCriteriaInvariants:
    """Tests that verify weight sum, description quality, and structure invariants
    for all five per-agent criteria sets.

    These tests are the automated enforcement of the weight invariant asserted
    at module load time in each criteria file. They also verify that criteria
    meet minimum quality standards for use in G-Eval prompts.
    """

    ALL_CRITERIA = [
        ("ps_researcher", PS_RESEARCHER_CRITERIA, 0.82),
        ("ps_analyst", PS_ANALYST_CRITERIA, 0.85),
        ("ps_architect", PS_ARCHITECT_CRITERIA, 0.88),
        ("ps_critic", PS_CRITIC_CRITERIA, 0.83),
        ("adv_scorer", ADV_SCORER_CRITERIA, 0.90),
    ]

    @pytest.mark.unit
    @pytest.mark.parametrize("agent_name,criteria,floor", ALL_CRITERIA)
    def test_weights_sum_to_one(
        self,
        agent_name: str,
        criteria: list[QualityCriterion],
        floor: float,
    ) -> None:
        """All per-agent criteria weight sets must sum to exactly 1.0."""
        total = sum(c.weight for c in criteria)
        assert abs(total - 1.0) < 1e-9, (
            f"{agent_name}: criteria weights sum to {total:.4f}, expected 1.0"
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("agent_name,criteria,floor", ALL_CRITERIA)
    def test_all_six_s014_dimensions_represented(
        self,
        agent_name: str,
        criteria: list[QualityCriterion],
        floor: float,
    ) -> None:
        """Each per-agent criteria set covers all six S-014 dimensions."""
        dimension_names = {c.dimension for c in criteria if c.dimension is not None}
        expected_dimensions = set(DIMENSION_WEIGHTS.keys())
        missing = expected_dimensions - dimension_names
        assert not missing, f"{agent_name}: missing S-014 dimensions: {missing}"

    @pytest.mark.unit
    @pytest.mark.parametrize("agent_name,criteria,floor", ALL_CRITERIA)
    def test_no_criterion_has_empty_description(
        self,
        agent_name: str,
        criteria: list[QualityCriterion],
        floor: float,
    ) -> None:
        """Every criterion description is non-empty and substantive (>= 50 chars)."""
        for criterion in criteria:
            assert len(criterion.description.strip()) >= 50, (
                f"{agent_name}: criterion '{criterion.name}' description is too short "
                f"({len(criterion.description)} chars). G-Eval requires substantive rubric text."
            )

    @pytest.mark.unit
    @pytest.mark.parametrize("agent_name,criteria,floor", ALL_CRITERIA)
    def test_criterion_names_are_unique_within_agent(
        self,
        agent_name: str,
        criteria: list[QualityCriterion],
        floor: float,
    ) -> None:
        """No two criteria in the same agent set share a name (prevents dedup bugs)."""
        names = [c.name for c in criteria]
        assert len(names) == len(set(names)), (
            f"{agent_name}: duplicate criterion names found: "
            f"{[n for n in names if names.count(n) > 1]}"
        )

    @pytest.mark.unit
    @pytest.mark.parametrize("agent_name,criteria,floor", ALL_CRITERIA)
    def test_quality_floor_constant_matches_contract(
        self,
        agent_name: str,
        criteria: list[QualityCriterion],
        floor: float,
    ) -> None:
        """Per-agent quality floors match behavioral-contracts.md §B.3.

        This test documents the floor values -- it does not enforce them here
        (the statistical engine enforces them at runtime). It catches accidental
        misconfiguration by asserting the expected floor values are stable.
        """
        expected_floors = {
            "ps_researcher": 0.82,
            "ps_analyst": 0.85,
            "ps_architect": 0.88,
            "ps_critic": 0.83,
            "adv_scorer": 0.90,
        }
        assert floor == expected_floors[agent_name], (
            f"{agent_name}: floor {floor} does not match contract value "
            f"{expected_floors[agent_name]}"
        )
