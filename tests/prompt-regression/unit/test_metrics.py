# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for jerry.testing.evaluation.metrics — JerryGEvalMetric.

Tests the Layer 2 domain metric class and module-level constants:
    - DIMENSION_WEIGHTS: sum to 1.0, all six dimensions present
    - JerryGEvalMetric.score_composite(): weighted aggregation
    - JerryGEvalMetric.classify_composite(): quality band classification
    - JerryGEvalMetric construction validation

No LLM calls performed. Tests use deterministic ScoringResult inputs.

References:
    - FR-007: G-Eval custom criteria evaluation
    - quality-enforcement.md: S-014 LLM-as-Judge, 6-dimension weights
    - H-20: 90% line coverage target
"""

from __future__ import annotations

import pytest

from jerry.testing.evaluation.criterion import QualityCriterion
from jerry.testing.evaluation.debiasing import DebiasingStrategy
from jerry.testing.evaluation.metrics import (
    DIMENSION_WEIGHTS,
    JerryGEvalMetric,
)
from jerry.testing.evaluation.scoring_result import ScoringResult

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_criteria() -> list[QualityCriterion]:
    """Return the six S-014 canonical criteria matching DIMENSION_WEIGHTS."""
    return [
        QualityCriterion(
            name="completeness", description="All required sections present.", weight=0.20
        ),
        QualityCriterion(
            name="internal_consistency", description="No contradictions.", weight=0.20
        ),
        QualityCriterion(
            name="methodological_rigor", description="Methodology followed.", weight=0.20
        ),
        QualityCriterion(name="evidence_quality", description="Evidence cited.", weight=0.15),
        QualityCriterion(name="actionability", description="Actionable output.", weight=0.15),
        QualityCriterion(name="traceability", description="Findings traceable.", weight=0.10),
    ]


@pytest.fixture
def metric_no_debiasing(sample_criteria: list[QualityCriterion]) -> JerryGEvalMetric:
    """Return a JerryGEvalMetric without debiasing for unit testing."""
    return JerryGEvalMetric(
        criteria=sample_criteria,
        debiasing=None,
        agent_name="test-agent",
        require_debiasing=False,
    )


def _make_scoring_result(name: str, score: float, weight: float) -> ScoringResult:
    """Construct a ScoringResult for the given criterion, score, and weight."""
    return ScoringResult(
        criterion_name=name,
        score=score,
        weight=weight,
        evidence=f"Test evidence for {name}.",
        debiasing_applied=False,
    )


# ---------------------------------------------------------------------------
# DIMENSION_WEIGHTS
# ---------------------------------------------------------------------------


class TestDimensionWeights:
    """Verify DIMENSION_WEIGHTS matches quality-enforcement.md SSOT."""

    def test_dimension_weights_sum_to_one(self) -> None:
        """The six S-014 dimension weights must sum to exactly 1.0."""
        total = sum(DIMENSION_WEIGHTS.values())
        assert abs(total - 1.0) < 1e-9

    def test_completeness_weight(self) -> None:
        """Completeness weight must be 0.20."""
        assert DIMENSION_WEIGHTS["completeness"] == pytest.approx(0.20)

    def test_internal_consistency_weight(self) -> None:
        """Internal consistency weight must be 0.20."""
        assert DIMENSION_WEIGHTS["internal_consistency"] == pytest.approx(0.20)

    def test_methodological_rigor_weight(self) -> None:
        """Methodological rigor weight must be 0.20."""
        assert DIMENSION_WEIGHTS["methodological_rigor"] == pytest.approx(0.20)

    def test_evidence_quality_weight(self) -> None:
        """Evidence quality weight must be 0.15."""
        assert DIMENSION_WEIGHTS["evidence_quality"] == pytest.approx(0.15)

    def test_actionability_weight(self) -> None:
        """Actionability weight must be 0.15."""
        assert DIMENSION_WEIGHTS["actionability"] == pytest.approx(0.15)

    def test_traceability_weight(self) -> None:
        """Traceability weight must be 0.10."""
        assert DIMENSION_WEIGHTS["traceability"] == pytest.approx(0.10)

    def test_all_six_dimensions_present(self) -> None:
        """All six S-014 dimensions must be present in DIMENSION_WEIGHTS."""
        required = {
            "completeness",
            "internal_consistency",
            "methodological_rigor",
            "evidence_quality",
            "actionability",
            "traceability",
        }
        assert required == set(DIMENSION_WEIGHTS.keys())


# ---------------------------------------------------------------------------
# classify_composite()
# ---------------------------------------------------------------------------


class TestClassifyComposite:
    """JerryGEvalMetric.classify_composite() maps scores to quality bands."""

    def test_classify_composite_pass_at_threshold(
        self, metric_no_debiasing: JerryGEvalMetric
    ) -> None:
        """Score == 0.92 should return 'PASS'."""
        assert metric_no_debiasing.classify_composite(0.92) == "PASS"

    def test_classify_composite_pass_above_threshold(
        self, metric_no_debiasing: JerryGEvalMetric
    ) -> None:
        """Score > 0.92 should return 'PASS'."""
        assert metric_no_debiasing.classify_composite(0.95) == "PASS"
        assert metric_no_debiasing.classify_composite(1.0) == "PASS"

    def test_classify_composite_revise(self, metric_no_debiasing: JerryGEvalMetric) -> None:
        """0.85 <= score < 0.92 should return 'REVISE'."""
        assert metric_no_debiasing.classify_composite(0.91) == "REVISE"
        assert metric_no_debiasing.classify_composite(0.85) == "REVISE"

    def test_classify_composite_rejected_below_threshold(
        self, metric_no_debiasing: JerryGEvalMetric
    ) -> None:
        """Score < 0.85 should return 'REJECTED'."""
        assert metric_no_debiasing.classify_composite(0.84) == "REJECTED"
        assert metric_no_debiasing.classify_composite(0.0) == "REJECTED"

    def test_classify_composite_invalid_score_raises(
        self, metric_no_debiasing: JerryGEvalMetric
    ) -> None:
        """Score outside [0.0, 1.0] should raise ValueError."""
        with pytest.raises(ValueError):
            metric_no_debiasing.classify_composite(1.01)
        with pytest.raises(ValueError):
            metric_no_debiasing.classify_composite(-0.01)

    def test_classify_composite_boundary_zero(self, metric_no_debiasing: JerryGEvalMetric) -> None:
        """Score exactly 0.0 should return 'REJECTED'."""
        assert metric_no_debiasing.classify_composite(0.0) == "REJECTED"

    def test_classify_composite_boundary_one(self, metric_no_debiasing: JerryGEvalMetric) -> None:
        """Score exactly 1.0 should return 'PASS'."""
        assert metric_no_debiasing.classify_composite(1.0) == "PASS"


# ---------------------------------------------------------------------------
# score_composite()
# ---------------------------------------------------------------------------


class TestScoreComposite:
    """JerryGEvalMetric.score_composite() computes weighted composite correctly."""

    def test_score_composite_perfect_scores(self, metric_no_debiasing: JerryGEvalMetric) -> None:
        """All-1.0 scores should produce composite 1.0."""
        results = [
            _make_scoring_result("completeness", 1.0, 0.20),
            _make_scoring_result("internal_consistency", 1.0, 0.20),
            _make_scoring_result("methodological_rigor", 1.0, 0.20),
            _make_scoring_result("evidence_quality", 1.0, 0.15),
            _make_scoring_result("actionability", 1.0, 0.15),
            _make_scoring_result("traceability", 1.0, 0.10),
        ]
        score = metric_no_debiasing.score_composite(results)
        assert score == pytest.approx(1.0)

    def test_score_composite_zero_scores(self, metric_no_debiasing: JerryGEvalMetric) -> None:
        """All-0.0 scores should produce composite 0.0."""
        results = [
            _make_scoring_result("completeness", 0.0, 0.20),
            _make_scoring_result("internal_consistency", 0.0, 0.20),
        ]
        score = metric_no_debiasing.score_composite(results)
        assert score == pytest.approx(0.0)

    def test_score_composite_empty_raises(self, metric_no_debiasing: JerryGEvalMetric) -> None:
        """Empty results list should raise ValueError."""
        with pytest.raises(ValueError):
            metric_no_debiasing.score_composite([])

    def test_score_composite_in_range(self, metric_no_debiasing: JerryGEvalMetric) -> None:
        """Composite score must equal the exact weighted sum for deterministic inputs.

        Expected: (0.75*0.20 + 0.90*0.20 + 0.85*0.20 + 0.80*0.15 + 0.70*0.15 + 0.95*0.10)
                  / (0.20 + 0.20 + 0.20 + 0.15 + 0.15 + 0.10)
                = 0.820 / 1.00 = 0.820
        """
        results = [
            _make_scoring_result("completeness", 0.75, 0.20),
            _make_scoring_result("internal_consistency", 0.90, 0.20),
            _make_scoring_result("methodological_rigor", 0.85, 0.20),
            _make_scoring_result("evidence_quality", 0.80, 0.15),
            _make_scoring_result("actionability", 0.70, 0.15),
            _make_scoring_result("traceability", 0.95, 0.10),
        ]
        expected = (
            0.75 * 0.20 + 0.90 * 0.20 + 0.85 * 0.20 + 0.80 * 0.15 + 0.70 * 0.15 + 0.95 * 0.10
        ) / (0.20 + 0.20 + 0.20 + 0.15 + 0.15 + 0.10)
        score = metric_no_debiasing.score_composite(results)
        assert score == pytest.approx(expected)

    def test_score_composite_normalized_by_weight_sum(
        self, metric_no_debiasing: JerryGEvalMetric
    ) -> None:
        """Partial criterion set should normalize by actual weight sum."""
        # Only completeness (weight=0.20) and evidence_quality (weight=0.15)
        results = [
            _make_scoring_result("completeness", 1.0, 0.20),
            _make_scoring_result("evidence_quality", 1.0, 0.15),
        ]
        score = metric_no_debiasing.score_composite(results)
        # Normalized: (1.0*0.20 + 1.0*0.15) / (0.20 + 0.15) = 1.0
        assert score == pytest.approx(1.0)

    def test_score_composite_weighted_calculation(
        self, metric_no_debiasing: JerryGEvalMetric
    ) -> None:
        """Composite should equal sum(score*weight)/sum(weights)."""
        results = [
            _make_scoring_result("completeness", 0.80, 0.20),
            _make_scoring_result("traceability", 0.60, 0.10),
        ]
        expected = (0.80 * 0.20 + 0.60 * 0.10) / (0.20 + 0.10)
        score = metric_no_debiasing.score_composite(results)
        assert score == pytest.approx(expected)


# ---------------------------------------------------------------------------
# JerryGEvalMetric construction
# ---------------------------------------------------------------------------


class TestJerryGEvalMetricConstruction:
    """Tests for JerryGEvalMetric construction validation."""

    def test_construction_requires_criteria(self) -> None:
        """Empty criteria list should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            JerryGEvalMetric(
                criteria=[],
                debiasing=None,
                agent_name="test-agent",
                require_debiasing=False,
            )
        assert "criterion" in str(exc_info.value).lower()

    def test_construction_requires_debiasing_by_default(self) -> None:
        """require_debiasing=True (default) with debiasing=None should raise ValueError."""
        criterion = QualityCriterion(name="completeness", description="Test.", weight=0.20)
        with pytest.raises(ValueError) as exc_info:
            JerryGEvalMetric(
                criteria=[criterion],
                debiasing=None,
                agent_name="test-agent",
                require_debiasing=True,
            )
        assert "debiasing" in str(exc_info.value).lower() or "C-007" in str(exc_info.value)

    def test_construction_with_debiasing_succeeds(
        self, sample_criteria: list[QualityCriterion]
    ) -> None:
        """Construction with a DebiasingStrategy should not raise."""
        strategy = DebiasingStrategy(seed=42)
        metric = JerryGEvalMetric(
            criteria=sample_criteria,
            debiasing=strategy,
            agent_name="test-agent",
        )
        assert metric.agent_name == "test-agent"

    def test_get_criteria_for_debiasing_no_debiasing(
        self, metric_no_debiasing: JerryGEvalMetric, sample_criteria: list[QualityCriterion]
    ) -> None:
        """Without debiasing, get_criteria_for_debiasing returns original order."""
        result = metric_no_debiasing.get_criteria_for_debiasing()
        assert [c.name for c in result] == [c.name for c in sample_criteria]
