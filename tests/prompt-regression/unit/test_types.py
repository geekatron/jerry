# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for jerry.testing.types — domain type definitions.

Tests the data contracts for all types shared across harness layers:
    - EvaluationMode enum values
    - RegressionClass enum members
    - BaselineRecord immutability
    - RegressionResult field presence and types

No LLM calls or I/O performed. All tests are deterministic.

References:
    - H-07: Domain module types (stdlib-only imports)
    - H-20: 90% line coverage target
"""

from __future__ import annotations

import dataclasses
from datetime import UTC, datetime

import pytest

from jerry.testing.types import (
    BaselineRecord,
    BonferroniConfig,
    EffectSizeLabel,
    EvaluationMode,
    MergeDecision,
    MultiMetricResult,
    RateClass,
    RegressionClass,
    RegressionResult,
    ScoreArray,
    WilcoxonResult,
    WilsonResult,
)

# ---------------------------------------------------------------------------
# EvaluationMode
# ---------------------------------------------------------------------------


class TestEvaluationMode:
    """Verify EvaluationMode enum values match FR-005 specification."""

    def test_smoke_value(self) -> None:
        """EvaluationMode.SMOKE should have value 'Smoke'."""
        assert EvaluationMode.SMOKE.value == "Smoke"

    def test_standard_value(self) -> None:
        """EvaluationMode.STANDARD should have value 'Standard'."""
        assert EvaluationMode.STANDARD.value == "Standard"

    def test_full_value(self) -> None:
        """EvaluationMode.FULL should have value 'Full'."""
        assert EvaluationMode.FULL.value == "Full"

    def test_evaluation_mode_is_str_enum(self) -> None:
        """EvaluationMode members should compare equal to their string values."""
        assert EvaluationMode.SMOKE == "Smoke"
        assert EvaluationMode.STANDARD == "Standard"
        assert EvaluationMode.FULL == "Full"

    def test_evaluation_mode_from_value(self) -> None:
        """EvaluationMode instances should be constructable from their string value."""
        assert EvaluationMode("Smoke") == EvaluationMode.SMOKE
        assert EvaluationMode("Standard") == EvaluationMode.STANDARD
        assert EvaluationMode("Full") == EvaluationMode.FULL


# ---------------------------------------------------------------------------
# RegressionClass
# ---------------------------------------------------------------------------


class TestRegressionClass:
    """Verify RegressionClass has all six required members."""

    def test_no_regression_member(self) -> None:
        """RegressionClass must have NO_REGRESSION member."""
        assert RegressionClass.NO_REGRESSION.value == "NO_REGRESSION"

    def test_marginal_member(self) -> None:
        """RegressionClass must have MARGINAL member."""
        assert RegressionClass.MARGINAL.value == "MARGINAL"

    def test_regression_member(self) -> None:
        """RegressionClass must have REGRESSION member."""
        assert RegressionClass.REGRESSION.value == "REGRESSION"

    def test_improvement_member(self) -> None:
        """RegressionClass must have IMPROVEMENT member."""
        assert RegressionClass.IMPROVEMENT.value == "IMPROVEMENT"

    def test_quality_floor_breach_member(self) -> None:
        """RegressionClass must have QUALITY_FLOOR_BREACH member."""
        assert RegressionClass.QUALITY_FLOOR_BREACH.value == "QUALITY_FLOOR_BREACH"

    def test_structural_fail_member(self) -> None:
        """RegressionClass must have STRUCTURAL_FAIL member."""
        assert RegressionClass.STRUCTURAL_FAIL.value == "STRUCTURAL_FAIL"

    def test_all_six_members_present(self) -> None:
        """RegressionClass must have exactly 6 members (or more, but the 6 required ones)."""
        member_values = {m.value for m in RegressionClass}
        required = {
            "NO_REGRESSION",
            "MARGINAL",
            "REGRESSION",
            "IMPROVEMENT",
            "QUALITY_FLOOR_BREACH",
            "STRUCTURAL_FAIL",
        }
        assert required.issubset(member_values)


# ---------------------------------------------------------------------------
# RateClass
# ---------------------------------------------------------------------------


class TestRateClass:
    """Verify RateClass enum for Wilson interval comparison."""

    def test_rate_stable_value(self) -> None:
        """RateClass.RATE_STABLE should have value 'RATE_STABLE'."""
        assert RateClass.RATE_STABLE.value == "RATE_STABLE"

    def test_rate_regression_value(self) -> None:
        """RateClass.RATE_REGRESSION should have value 'RATE_REGRESSION'."""
        assert RateClass.RATE_REGRESSION.value == "RATE_REGRESSION"


# ---------------------------------------------------------------------------
# EffectSizeLabel
# ---------------------------------------------------------------------------


class TestEffectSizeLabel:
    """Verify EffectSizeLabel enum values."""

    def test_negligible_value(self) -> None:
        """EffectSizeLabel.NEGLIGIBLE should have value 'Negligible'."""
        assert EffectSizeLabel.NEGLIGIBLE.value == "Negligible"

    def test_small_value(self) -> None:
        """EffectSizeLabel.SMALL should have value 'Small'."""
        assert EffectSizeLabel.SMALL.value == "Small"

    def test_small_to_medium_value(self) -> None:
        """EffectSizeLabel.SMALL_TO_MEDIUM should have value 'Small-to-Medium'."""
        assert EffectSizeLabel.SMALL_TO_MEDIUM.value == "Small-to-Medium"

    def test_medium_to_large_value(self) -> None:
        """EffectSizeLabel.MEDIUM_TO_LARGE should have value 'Medium-to-Large'."""
        assert EffectSizeLabel.MEDIUM_TO_LARGE.value == "Medium-to-Large"


# ---------------------------------------------------------------------------
# MergeDecision
# ---------------------------------------------------------------------------


class TestMergeDecision:
    """Verify MergeDecision enum values."""

    def test_allow_value(self) -> None:
        """MergeDecision.ALLOW should have value 'ALLOW'."""
        assert MergeDecision.ALLOW.value == "ALLOW"

    def test_allow_with_warning_value(self) -> None:
        """MergeDecision.ALLOW_WITH_WARNING should have value 'ALLOW_WITH_WARNING'."""
        assert MergeDecision.ALLOW_WITH_WARNING.value == "ALLOW_WITH_WARNING"

    def test_block_value(self) -> None:
        """MergeDecision.BLOCK should have value 'BLOCK'."""
        assert MergeDecision.BLOCK.value == "BLOCK"


# ---------------------------------------------------------------------------
# BaselineRecord
# ---------------------------------------------------------------------------


class TestBaselineRecord:
    """BaselineRecord is a mutable dataclass (not frozen)."""

    def _make_record(self) -> BaselineRecord:
        """Return a fully populated BaselineRecord for testing."""
        return BaselineRecord(
            version_key="abc" * 13 + "a:skills/x/agents/y.md",
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=[0.93, 0.94, 0.92],
            mean_score=0.93,
            n_runs=3,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
            captured_at=datetime.now(UTC).isoformat(),
            baseline_status="active",
            invalidated_by=None,
        )

    def test_baseline_record_fields_present(self) -> None:
        """BaselineRecord must have all required fields."""
        record = self._make_record()
        assert record.version_key is not None
        assert record.agent_id == "ps-researcher"
        assert record.metric_id == "composite_score"
        assert isinstance(record.scores, list)
        assert record.baseline_status == "active"
        assert record.invalidated_by is None

    def test_baseline_record_is_mutable(self) -> None:
        """BaselineRecord is NOT frozen — it should allow field mutation."""
        record = self._make_record()
        record.baseline_status = "invalidated"
        assert record.baseline_status == "invalidated"

    def test_baseline_record_default_status(self) -> None:
        """BaselineRecord default baseline_status should be 'active'."""
        record = BaselineRecord(
            version_key="abc" * 13 + "a:skills/x/agents/y.md",
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=[0.93],
            mean_score=0.93,
            n_runs=1,
            evaluation_mode=EvaluationMode.STANDARD,
            model_version="claude-sonnet-4",
            captured_at=datetime.now(UTC).isoformat(),
        )
        assert record.baseline_status == "active"
        assert record.invalidated_by is None


# ---------------------------------------------------------------------------
# WilcoxonResult
# ---------------------------------------------------------------------------


class TestWilcoxonResult:
    """WilcoxonResult is a frozen dataclass with required fields."""

    def _make_wilcoxon_result(self) -> WilcoxonResult:
        return WilcoxonResult(
            statistic=150.0,
            p_value=0.12,
            n_pairs=30,
            cohens_r=0.08,
            effect_label=EffectSizeLabel.NEGLIGIBLE,
            mean_delta=0.01,
            mean_a=0.93,
            mean_b=0.94,
        )

    def test_wilcoxon_result_frozen(self) -> None:
        """WilcoxonResult should be immutable (frozen=True)."""
        result = self._make_wilcoxon_result()
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            result.p_value = 0.99  # type: ignore[misc]

    def test_wilcoxon_result_fields(self) -> None:
        """WilcoxonResult must expose all required fields with correct values."""
        result = self._make_wilcoxon_result()
        assert result.statistic == pytest.approx(150.0)
        assert result.p_value == pytest.approx(0.12)
        assert result.n_pairs == 30
        assert result.cohens_r == pytest.approx(0.08)
        assert result.effect_label == EffectSizeLabel.NEGLIGIBLE
        assert result.mean_delta == pytest.approx(0.01)
        assert result.mean_a == pytest.approx(0.93)
        assert result.mean_b == pytest.approx(0.94)


# ---------------------------------------------------------------------------
# WilsonResult
# ---------------------------------------------------------------------------


class TestWilsonResult:
    """WilsonResult is a frozen dataclass with confidence interval fields."""

    def _make_wilson_result(self) -> WilsonResult:
        return WilsonResult(
            n_total=30,
            n_pass=28,
            pass_rate=28 / 30,
            ci_lower=0.78,
            ci_upper=0.98,
            ci_width=0.20,
        )

    def test_wilson_result_frozen(self) -> None:
        """WilsonResult should be immutable (frozen=True)."""
        result = self._make_wilson_result()
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            result.pass_rate = 0.5  # type: ignore[misc]

    def test_wilson_result_fields(self) -> None:
        """WilsonResult must expose all confidence interval fields."""
        result = self._make_wilson_result()
        assert result.n_total == 30
        assert result.n_pass == 28
        assert 0.0 <= result.pass_rate <= 1.0
        assert result.ci_lower <= result.ci_upper
        assert result.ci_width == pytest.approx(result.ci_upper - result.ci_lower)


# ---------------------------------------------------------------------------
# BonferroniConfig
# ---------------------------------------------------------------------------


class TestBonferroniConfig:
    """BonferroniConfig is a frozen dataclass with a description property."""

    def test_bonferroni_config_description_property(self) -> None:
        """BonferroniConfig.description should include k and alpha values."""
        bc = BonferroniConfig(k=13, alpha_family=0.05, alpha_per_test=0.05 / 13)
        desc = bc.description
        assert "13" in desc
        assert "Bonferroni" in desc

    def test_bonferroni_config_frozen(self) -> None:
        """BonferroniConfig should be immutable (frozen=True)."""
        bc = BonferroniConfig(k=13, alpha_family=0.05, alpha_per_test=0.05 / 13)
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            bc.k = 5  # type: ignore[misc]


# ---------------------------------------------------------------------------
# RegressionResult
# ---------------------------------------------------------------------------


class TestRegressionResult:
    """RegressionResult is a frozen dataclass that consolidates all comparison output."""

    def _make_regression_result(self) -> RegressionResult:
        wilcoxon = WilcoxonResult(
            statistic=150.0,
            p_value=0.12,
            n_pairs=30,
            cohens_r=0.08,
            effect_label=EffectSizeLabel.NEGLIGIBLE,
            mean_delta=0.01,
            mean_a=0.93,
            mean_b=0.94,
        )
        wilson = WilsonResult(
            n_total=30,
            n_pass=28,
            pass_rate=28 / 30,
            ci_lower=0.78,
            ci_upper=0.98,
            ci_width=0.20,
        )
        return RegressionResult(
            classification=RegressionClass.NO_REGRESSION,
            rate_class=RateClass.RATE_STABLE,
            merge_decision=MergeDecision.ALLOW,
            wilcoxon=wilcoxon,
            wilson_a=wilson,
            wilson_b=wilson,
            bonferroni=None,
            alpha=0.05,
            evaluation_mode=EvaluationMode.FULL,
            metric_id="composite_score",
            agent_id="ps-researcher",
            version_key_a="a" * 40 + ":skills/x/agents/y.md",
            version_key_b="b" * 40 + ":skills/x/agents/y.md",
            n_a=30,
            n_b=30,
        )

    def test_regression_result_fields_present(self) -> None:
        """RegressionResult must expose all required fields."""
        result = self._make_regression_result()
        assert result.classification == RegressionClass.NO_REGRESSION
        assert result.merge_decision == MergeDecision.ALLOW
        assert result.n_a == 30
        assert result.n_b == 30
        assert result.metric_id == "composite_score"
        assert result.agent_id == "ps-researcher"
        assert result.bonferroni is None

    def test_regression_result_frozen(self) -> None:
        """RegressionResult should be immutable (frozen=True)."""
        result = self._make_regression_result()
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            result.classification = RegressionClass.REGRESSION  # type: ignore[misc]

    def test_regression_result_timestamp_populated(self) -> None:
        """RegressionResult.timestamp should be auto-populated with a non-empty string."""
        result = self._make_regression_result()
        assert isinstance(result.timestamp, str)
        assert len(result.timestamp) > 0

    def test_regression_result_dimension_driver_default_none(self) -> None:
        """RegressionResult.dimension_driver defaults to None."""
        result = self._make_regression_result()
        assert result.dimension_driver is None


# ---------------------------------------------------------------------------
# MultiMetricResult
# ---------------------------------------------------------------------------


class TestMultiMetricResult:
    """MultiMetricResult is a frozen dataclass for aggregated multi-metric results."""

    def _make_multi_metric_result(
        self, dimension_driver: str | None = "completeness"
    ) -> MultiMetricResult:
        """Return a fully populated MultiMetricResult for testing."""
        bc = BonferroniConfig(k=13, alpha_family=0.05, alpha_per_test=0.05 / 13)
        return MultiMetricResult(
            overall_classification=RegressionClass.NO_REGRESSION,
            merge_decision=MergeDecision.ALLOW,
            per_metric={},
            bonferroni=bc,
            dimension_driver=dimension_driver,
        )

    def test_multi_metric_result_instantiation(self) -> None:
        """MultiMetricResult should instantiate without error."""
        result = self._make_multi_metric_result()
        assert result is not None

    def test_multi_metric_result_fields_present(self) -> None:
        """MultiMetricResult must expose results, bonferroni, and dimension_driver fields
        with the exact values passed to the constructor."""
        result = self._make_multi_metric_result()
        assert result.per_metric == {}
        assert isinstance(result.bonferroni, BonferroniConfig)
        assert result.dimension_driver == "completeness"
        assert result.overall_classification == RegressionClass.NO_REGRESSION
        assert result.merge_decision == MergeDecision.ALLOW

    def test_multi_metric_result_is_frozen(self) -> None:
        """MultiMetricResult must be immutable (frozen=True)."""
        import dataclasses

        result = self._make_multi_metric_result()
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            result.overall_classification = RegressionClass.REGRESSION  # type: ignore[misc]

    def test_multi_metric_result_dimension_driver_none_default(self) -> None:
        """MultiMetricResult.dimension_driver=None should be accepted."""
        result = self._make_multi_metric_result(dimension_driver=None)
        assert result.dimension_driver is None

    def test_multi_metric_result_dimension_driver_set(self) -> None:
        """MultiMetricResult.dimension_driver should hold the provided metric ID."""
        result = self._make_multi_metric_result(dimension_driver="completeness")
        assert result.dimension_driver == "completeness"

    def test_multi_metric_result_per_metric_is_dict(self) -> None:
        """MultiMetricResult.per_metric must be a dict."""
        result = self._make_multi_metric_result()
        assert isinstance(result.per_metric, dict)

    def test_multi_metric_result_bonferroni_is_config(self) -> None:
        """MultiMetricResult.bonferroni must be a BonferroniConfig instance."""
        result = self._make_multi_metric_result()
        assert isinstance(result.bonferroni, BonferroniConfig)


# ---------------------------------------------------------------------------
# ScoreArray type alias
# ---------------------------------------------------------------------------


class TestScoreArray:
    """ScoreArray is a type alias for list[float]."""

    def test_score_array_is_list(self) -> None:
        """ScoreArray values should be valid as plain Python lists."""
        scores: ScoreArray = [0.93, 0.91, 0.95]
        assert isinstance(scores, list)
        assert all(isinstance(s, float) for s in scores)
