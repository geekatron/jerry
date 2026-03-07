# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Integration tests for jerry.testing.layer4_stats — Layer4Pipeline.

Tests the end-to-end pipeline orchestration across:
    - Smoke mode (structural checks only, no statistics)
    - Full mode (multi-metric statistical comparison)
    - InsufficientSamplesError handling

The Layer4Pipeline depends on BaselinePersistencePort and ReportOutputPort
via hexagonal port interfaces.  These tests inject mock adapters to isolate
the pipeline orchestration logic from filesystem and LLM dependencies.

No real BaselineStore or ReportGenerator is instantiated.
No file I/O is performed (output paths omitted).

References:
    - FR-018: CI/CD exit codes (0/1/2)
    - FR-019: One-way dependency rule (stats.py -> types.py only)
    - H-20: 90% line coverage target
    - behavioral-contracts.md Section D.6: ComparisonReport schema
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from jerry.testing.layer4_stats import Layer4Pipeline
from jerry.testing.stats import InsufficientSamplesError
from jerry.testing.types import (
    BonferroniConfig,
    ComparisonReport,
    EvaluationMode,
    MergeDecision,
    RegressionClass,
)

# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------


def _make_scores(n: int, value: float = 0.93) -> list[float]:
    """Return a list of ``n`` scores alternating around ``value``.

    Alternating pattern ensures Wilcoxon variation requirement is satisfied
    (stats.py rejects all-identical arrays via InvalidScoreArrayError).
    """
    return [value if i % 2 == 0 else value - 0.02 for i in range(n)]


def _make_comparison_report(
    classification: str = "NO_REGRESSION",
    merge_recommendation: str = MergeDecision.ALLOW.value,
    dimension_driver: str | None = None,
    evaluation_mode: str = "Full",
    agent: str = "ps-researcher",
) -> ComparisonReport:
    """Construct a minimal ComparisonReport for test assertions."""
    return ComparisonReport(
        evaluation_mode=evaluation_mode,
        agent=agent,
        prompt_version_baseline="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
        prompt_version_candidate="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
        n_baseline=30,
        n_candidate=30,
        timestamp="2026-03-07T12:00:00Z",
        classification=classification,
        merge_recommendation=merge_recommendation,
        dimension_driver=dimension_driver,
        narrative="Test narrative.",
        per_metric_results={},
        multi_metric_result=None,
    )


def _make_smoke_report(
    classification: str = "STRUCTURAL_PASS",
    merge_recommendation: str = MergeDecision.ALLOW.value,
) -> ComparisonReport:
    """Construct a minimal smoke-mode ComparisonReport."""
    return ComparisonReport(
        evaluation_mode="Smoke",
        agent="ps-researcher",
        prompt_version_baseline="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
        prompt_version_candidate="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
        n_baseline=1,
        n_candidate=1,
        timestamp="2026-03-07T12:00:00Z",
        classification=classification,
        merge_recommendation=merge_recommendation,
        dimension_driver=None,
        narrative="Smoke mode structural check only.",
        per_metric_results={},
        multi_metric_result=None,
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_store() -> MagicMock:
    """Return a MagicMock satisfying the BaselinePersistencePort interface."""
    store = MagicMock()
    store.retrieve.return_value = None
    store.audit.return_value = []
    store.invalidate.return_value = 0
    return store


@pytest.fixture
def mock_generator() -> MagicMock:
    """Return a MagicMock satisfying the ReportOutputPort interface."""
    gen = MagicMock()
    gen.smoke_mode_report.return_value = _make_smoke_report()
    gen.from_single_metric.return_value = _make_comparison_report()
    gen.from_multi_metric.return_value = _make_comparison_report()
    gen.to_json.return_value = "{}"
    gen.to_markdown.return_value = "# Report"
    return gen


@pytest.fixture
def pipeline(mock_store: MagicMock, mock_generator: MagicMock) -> Layer4Pipeline:
    """Return a Layer4Pipeline with mocked ports."""
    return Layer4Pipeline(
        baseline_store=mock_store,
        report_generator=mock_generator,
    )


# ---------------------------------------------------------------------------
# Smoke mode tests
# ---------------------------------------------------------------------------


class TestPipelineSmokeMode:
    """Layer4Pipeline.run() in EvaluationMode.SMOKE mode.

    Smoke mode must:
    - Skip statistical comparison entirely.
    - Call generator.smoke_mode_report() with the agent_id, version_key_a,
      and structural_violations.
    - Return exit code 0 when no violations.
    - Return exit code 1 when violations are present.
    """

    def test_pipeline_smoke_mode_no_violations_returns_zero(
        self,
        pipeline: Layer4Pipeline,
        mock_generator: MagicMock,
    ) -> None:
        """Smoke mode with no structural violations must return exit code 0."""
        exit_code = pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={},
            evaluation_mode=EvaluationMode.SMOKE,
            structural_violations=[],
        )

        assert exit_code == 0

    def test_pipeline_smoke_mode_with_violations_returns_one(
        self,
        mock_store: MagicMock,
        mock_generator: MagicMock,
    ) -> None:
        """Smoke mode with structural violations must return exit code 1."""
        mock_generator.smoke_mode_report.return_value = _make_smoke_report(
            classification="STRUCTURAL_FAIL",
            merge_recommendation=MergeDecision.BLOCK.value,
        )
        p = Layer4Pipeline(baseline_store=mock_store, report_generator=mock_generator)

        exit_code = p.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={},
            evaluation_mode=EvaluationMode.SMOKE,
            structural_violations=["Section A: missing output files."],
        )

        assert exit_code == 1

    def test_pipeline_smoke_mode_calls_smoke_report_generator(
        self,
        pipeline: Layer4Pipeline,
        mock_generator: MagicMock,
    ) -> None:
        """Smoke mode must delegate to generator.smoke_mode_report()."""
        version_key = "aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md"
        violations = ["Missing output-files section."]

        pipeline.run(
            agent_id="ps-researcher",
            version_key_a=version_key,
            version_key_b=version_key,
            metric_scores={},
            evaluation_mode=EvaluationMode.SMOKE,
            structural_violations=violations,
        )

        mock_generator.smoke_mode_report.assert_called_once_with(
            "ps-researcher",
            version_key,
            violations,
        )

    def test_pipeline_smoke_mode_skips_statistical_comparison(
        self,
        pipeline: Layer4Pipeline,
        mock_generator: MagicMock,
    ) -> None:
        """Smoke mode must NOT call from_single_metric or from_multi_metric."""
        pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={},
            evaluation_mode=EvaluationMode.SMOKE,
        )

        mock_generator.from_single_metric.assert_not_called()
        mock_generator.from_multi_metric.assert_not_called()

    def test_pipeline_smoke_mode_default_violations_empty(
        self,
        pipeline: Layer4Pipeline,
        mock_generator: MagicMock,
    ) -> None:
        """Smoke mode with no structural_violations kwarg defaults to empty list."""
        pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={},
            evaluation_mode=EvaluationMode.SMOKE,
        )

        # The generator should have been called with an empty violations list.
        args, _ = mock_generator.smoke_mode_report.call_args
        assert args[2] == []


# ---------------------------------------------------------------------------
# Full mode tests
# ---------------------------------------------------------------------------


class TestPipelineFullMode:
    """Layer4Pipeline.run() in EvaluationMode.FULL mode.

    Full mode must:
    - Invoke the statistical comparison pipeline.
    - For single-metric input, call from_single_metric (no Bonferroni).
    - For multi-metric input, call from_multi_metric (Bonferroni applied).
    - Map NO_REGRESSION -> exit 0, REGRESSION -> exit 1, MARGINAL -> exit 2.
    """

    def test_pipeline_full_mode_single_metric_no_regression_returns_zero(
        self,
        pipeline: Layer4Pipeline,
        mock_generator: MagicMock,
    ) -> None:
        """Full mode single-metric NO_REGRESSION must return exit code 0."""
        scores = _make_scores(30)
        mock_generator.from_single_metric.return_value = _make_comparison_report(
            classification="NO_REGRESSION",
            merge_recommendation=MergeDecision.ALLOW.value,
        )

        exit_code = pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={"composite_score": (scores, scores[::-1])},
            evaluation_mode=EvaluationMode.FULL,
        )

        assert exit_code == 0

    def test_pipeline_full_mode_regression_returns_one(
        self,
        pipeline: Layer4Pipeline,
        mock_generator: MagicMock,
    ) -> None:
        """Full mode REGRESSION classification must return exit code 1."""
        scores = _make_scores(30)
        mock_generator.from_single_metric.return_value = _make_comparison_report(
            classification="REGRESSION",
            merge_recommendation=MergeDecision.BLOCK.value,
        )

        exit_code = pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={"composite_score": (scores, scores[::-1])},
            evaluation_mode=EvaluationMode.FULL,
        )

        assert exit_code == 1

    def test_pipeline_full_mode_marginal_returns_two(
        self,
        pipeline: Layer4Pipeline,
        mock_generator: MagicMock,
    ) -> None:
        """Full mode MARGINAL classification must return exit code 2."""
        scores = _make_scores(30)
        mock_generator.from_single_metric.return_value = _make_comparison_report(
            classification="MARGINAL",
            merge_recommendation=MergeDecision.ALLOW_WITH_WARNING.value,
        )

        exit_code = pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-regression/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={"composite_score": (scores, scores[::-1])},
            evaluation_mode=EvaluationMode.FULL,
        )

        assert exit_code == 2

    def test_pipeline_full_mode_improvement_returns_allow_with_warning(
        self,
        pipeline: Layer4Pipeline,
        mock_generator: MagicMock,
    ) -> None:
        """Full mode IMPROVEMENT classification must return exit code 2 (ALLOW_WITH_WARNING).

        FR-018: IMPROVEMENT maps to ALLOW_WITH_WARNING merge decision.
        The exit code resolves via the merge_recommendation field on the
        ComparisonReport, NOT the RegressionClass directly.
        ALLOW_WITH_WARNING -> exit 2 per FR-018.
        """
        scores = _make_scores(30)
        mock_generator.from_single_metric.return_value = _make_comparison_report(
            classification="IMPROVEMENT",
            merge_recommendation=MergeDecision.ALLOW_WITH_WARNING.value,
        )

        exit_code = pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={"composite_score": (scores, scores[::-1])},
            evaluation_mode=EvaluationMode.FULL,
        )

        # IMPROVEMENT maps to ALLOW_WITH_WARNING but the exit code resolves via
        # the merge_recommendation value on the ComparisonReport, NOT the
        # RegressionClass. ALLOW_WITH_WARNING -> exit 2 per FR-018.
        assert exit_code == 2

    def test_pipeline_full_mode_single_metric_calls_from_single_metric(
        self,
        pipeline: Layer4Pipeline,
        mock_generator: MagicMock,
    ) -> None:
        """Full mode single-metric must delegate to from_single_metric, not from_multi_metric."""
        scores = _make_scores(30)

        pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={"composite_score": (scores, scores[::-1])},
            evaluation_mode=EvaluationMode.FULL,
        )

        mock_generator.from_single_metric.assert_called_once()
        mock_generator.from_multi_metric.assert_not_called()

    def test_pipeline_full_mode_multi_metric_calls_from_multi_metric(
        self,
        pipeline: Layer4Pipeline,
        mock_generator: MagicMock,
    ) -> None:
        """Full mode multi-metric must delegate to from_multi_metric with Bonferroni."""
        scores = _make_scores(30)
        multi_report = _make_comparison_report(
            classification="NO_REGRESSION",
            merge_recommendation=MergeDecision.ALLOW.value,
        )
        mock_generator.from_multi_metric.return_value = multi_report

        pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={
                "completeness": (scores, scores[::-1]),
                "internal_consistency": (scores[::-1], scores),
            },
            evaluation_mode=EvaluationMode.FULL,
        )

        mock_generator.from_multi_metric.assert_called_once()
        mock_generator.from_single_metric.assert_not_called()

    def test_pipeline_full_mode_no_bonferroni_uses_single_path(
        self,
        pipeline: Layer4Pipeline,
        mock_generator: MagicMock,
    ) -> None:
        """apply_bonferroni=False on multi-metric forces single-metric path."""
        scores = _make_scores(30)

        pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={
                "completeness": (scores, scores[::-1]),
                "internal_consistency": (scores[::-1], scores),
            },
            evaluation_mode=EvaluationMode.FULL,
            apply_bonferroni=False,
        )

        # apply_bonferroni=False triggers the single-metric code path
        # (first metric extracted via next(iter(...))).
        mock_generator.from_single_metric.assert_called_once()
        mock_generator.from_multi_metric.assert_not_called()


# ---------------------------------------------------------------------------
# InsufficientSamplesError handling
# ---------------------------------------------------------------------------


class TestPipelineInsufficientSamples:
    """Layer4Pipeline.run() gracefully handles InsufficientSamplesError.

    When the score arrays are too small (N < 20 for FULL mode), the
    statistical engine raises InsufficientSamplesError.  The pipeline
    must not swallow this exception — it should propagate to the caller
    so that the CI/CD harness can emit a meaningful diagnostic.
    """

    def test_pipeline_insufficient_samples_propagates_error(
        self,
        pipeline: Layer4Pipeline,
    ) -> None:
        """InsufficientSamplesError from stats.py must propagate from run().

        FR-014: N >= 20 enforcement. When score arrays have N < 20, the
        statistical engine must raise InsufficientSamplesError with the
        exact message format specified by FR-014.
        """
        short_scores = _make_scores(5)  # N=5, well below the N=20 minimum

        with pytest.raises(InsufficientSamplesError):
            pipeline.run(
                agent_id="ps-researcher",
                version_key_a=("aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md"),
                version_key_b=("bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md"),
                metric_scores={"composite_score": (short_scores, short_scores[::-1])},
                evaluation_mode=EvaluationMode.FULL,
            )

    def test_pipeline_insufficient_samples_error_is_value_error_subclass(
        self,
        pipeline: Layer4Pipeline,
    ) -> None:
        """InsufficientSamplesError must be a ValueError subclass (contract).

        FR-014: InsufficientSamplesError inherits from ValueError so that
        callers catching ValueError also catch this specific error.
        """
        short_scores = _make_scores(5)

        with pytest.raises(ValueError):
            pipeline.run(
                agent_id="ps-researcher",
                version_key_a=("aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md"),
                version_key_b=("bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md"),
                metric_scores={"composite_score": (short_scores, short_scores[::-1])},
                evaluation_mode=EvaluationMode.FULL,
            )

    def test_pipeline_smoke_mode_ignores_score_arrays(
        self,
        pipeline: Layer4Pipeline,
        mock_generator: MagicMock,
    ) -> None:
        """Smoke mode must never raise InsufficientSamplesError (no statistics run)."""
        short_scores = _make_scores(1)  # N=1, far below minimum

        # Smoke mode must not touch metric_scores at all.
        exit_code = pipeline.run(
            agent_id="ps-researcher",
            version_key_a=("aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md"),
            version_key_b=("aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md"),
            metric_scores={"composite_score": (short_scores, short_scores)},
            evaluation_mode=EvaluationMode.SMOKE,
        )

        assert exit_code in (0, 1)


# ---------------------------------------------------------------------------
# run_single_metric() tests
# ---------------------------------------------------------------------------


class TestPipelineRunSingleMetric:
    """Layer4Pipeline.run_single_metric() convenience wrapper.

    Exercised separately from run() to test the (result, report) return contract.
    """

    def test_run_single_metric_returns_tuple(
        self,
        pipeline: Layer4Pipeline,
        mock_generator: MagicMock,
    ) -> None:
        """run_single_metric() must return (RegressionResult, ComparisonReport)."""
        scores = _make_scores(30)
        report = _make_comparison_report()
        mock_generator.from_single_metric.return_value = report

        result, returned_report = pipeline.run_single_metric(
            agent_id="ps-researcher",
            metric_id="composite_score",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            scores_a=scores,
            scores_b=scores[::-1],
            evaluation_mode=EvaluationMode.FULL,
        )

        assert returned_report is report
        # result is a RegressionResult from compare_versions() in stats.py.
        from jerry.testing.types import RegressionResult  # noqa: PLC0415

        assert isinstance(result, RegressionResult)

    def test_run_single_metric_insufficient_samples_raises(
        self,
        pipeline: Layer4Pipeline,
    ) -> None:
        """run_single_metric() must raise InsufficientSamplesError for N < 20."""
        short_scores = _make_scores(5)

        with pytest.raises(InsufficientSamplesError):
            pipeline.run_single_metric(
                agent_id="ps-researcher",
                metric_id="composite_score",
                version_key_a=("aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md"),
                version_key_b=("bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md"),
                scores_a=short_scores,
                scores_b=short_scores[::-1],
                evaluation_mode=EvaluationMode.FULL,
            )


# ---------------------------------------------------------------------------
# _exit_code() static method tests
# ---------------------------------------------------------------------------


class TestExitCodeMapping:
    """Layer4Pipeline._exit_code() maps merge_recommendation to int.

    FR-018 contract:
        BLOCK             -> 1
        ALLOW_WITH_WARNING -> 2
        ALLOW             -> 0
    """

    def test_exit_code_block_returns_one(self) -> None:
        """BLOCK recommendation must return exit code 1.

        FR-018: BLOCK merge recommendation maps to exit code 1 (CI/CD gate failure).
        """
        report = _make_comparison_report(
            merge_recommendation=MergeDecision.BLOCK.value,
        )
        assert Layer4Pipeline._exit_code(report) == 1

    def test_exit_code_allow_with_warning_returns_two(self) -> None:
        """ALLOW_WITH_WARNING recommendation must return exit code 2.

        FR-018: ALLOW_WITH_WARNING merge recommendation maps to exit code 2
        (CI/CD gate passes with warning; logged for developer visibility).
        """
        report = _make_comparison_report(
            merge_recommendation=MergeDecision.ALLOW_WITH_WARNING.value,
        )
        assert Layer4Pipeline._exit_code(report) == 2

    def test_exit_code_allow_returns_zero(self) -> None:
        """ALLOW recommendation must return exit code 0.

        FR-018: ALLOW merge recommendation maps to exit code 0 (CI/CD gate pass).
        """
        report = _make_comparison_report(
            merge_recommendation=MergeDecision.ALLOW.value,
        )
        assert Layer4Pipeline._exit_code(report) == 0


# ---------------------------------------------------------------------------
# _aggregate_multi_metric() static method tests
# ---------------------------------------------------------------------------


class TestAggregateMultiMetric:
    """Layer4Pipeline._aggregate_multi_metric() derives worst-case classification.

    Exercises the aggregation logic for multi-metric Bonferroni-corrected
    results.  RegressionResult instances are produced by compare_versions()
    so that all required fields are correctly populated without manual stub
    construction.
    """

    # Scores that produce a NO_REGRESSION result (similar arrays, high p-value).
    _SCORES_PASS = [0.93 if i % 2 == 0 else 0.91 for i in range(30)]
    # Scores that produce a REGRESSION result (clear directional shift).
    _SCORES_A_BASELINE = [0.95 if i % 2 == 0 else 0.93 for i in range(30)]
    _SCORES_B_REGRESSED = [0.70 if i % 2 == 0 else 0.68 for i in range(30)]

    def _make_bonferroni(self) -> BonferroniConfig:
        """Construct a minimal BonferroniConfig for aggregation tests."""
        return BonferroniConfig(
            k=2,
            alpha_family=0.05,
            alpha_per_test=0.025,
        )

    def _compare(
        self,
        scores_a: list[float],
        scores_b: list[float],
        metric_id: str = "composite_score",
    ) -> object:
        """Invoke compare_versions() to produce a real RegressionResult."""
        from jerry.testing.stats import compare_versions

        return compare_versions(
            scores_a,
            scores_b,
            metric_id=metric_id,
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            evaluation_mode=EvaluationMode.FULL,
        )

    def test_aggregate_worst_case_is_regression(self) -> None:
        """Overall classification must be REGRESSION when any metric regresses."""
        per_metric = {
            "completeness": self._compare(
                self._SCORES_PASS, self._SCORES_PASS, metric_id="completeness"
            ),
            "actionability": self._compare(
                self._SCORES_A_BASELINE, self._SCORES_B_REGRESSED, metric_id="actionability"
            ),
        }
        bonferroni = self._make_bonferroni()

        multi = Layer4Pipeline._aggregate_multi_metric(per_metric, bonferroni)

        assert multi.overall_classification == RegressionClass.REGRESSION

    def test_aggregate_no_blocking_when_all_pass(self) -> None:
        """Overall classification is non-blocking when all metrics pass.

        When no metric is classified as REGRESSION or QUALITY_FLOOR_BREACH,
        the overall classification must not be REGRESSION or STRUCTURAL_FAIL.
        It may be NO_REGRESSION, IMPROVEMENT, or MARGINAL depending on
        exact p-values; all of these are non-blocking outcomes.
        """
        per_metric = {
            "completeness": self._compare(
                self._SCORES_PASS, self._SCORES_PASS, metric_id="completeness"
            ),
            "actionability": self._compare(
                self._SCORES_PASS, self._SCORES_PASS, metric_id="actionability"
            ),
        }
        bonferroni = self._make_bonferroni()

        multi = Layer4Pipeline._aggregate_multi_metric(per_metric, bonferroni)

        blocking = {RegressionClass.REGRESSION, RegressionClass.STRUCTURAL_FAIL}
        assert multi.overall_classification not in blocking

    def test_aggregate_dimension_driver_set_on_regression(self) -> None:
        """Dimension driver must be set to the failing metric name on REGRESSION."""
        per_metric = {
            "completeness": self._compare(
                self._SCORES_PASS, self._SCORES_PASS, metric_id="completeness"
            ),
            "actionability": self._compare(
                self._SCORES_A_BASELINE, self._SCORES_B_REGRESSED, metric_id="actionability"
            ),
        }
        bonferroni = self._make_bonferroni()

        multi = Layer4Pipeline._aggregate_multi_metric(per_metric, bonferroni)

        assert multi.dimension_driver == "actionability"

    def test_aggregate_dimension_driver_consistent_with_classification(self) -> None:
        """Dimension driver must be consistent with overall_classification.

        When overall_classification is REGRESSION, dimension_driver names the
        driving metric.  When NO_REGRESSION or IMPROVEMENT, dimension_driver
        is None.  This test verifies the invariant using score pairs that may
        produce either classification depending on statistical power.
        """
        per_metric = {
            "completeness": self._compare(
                self._SCORES_A_BASELINE, self._SCORES_B_REGRESSED, metric_id="completeness"
            ),
        }
        bonferroni = self._make_bonferroni()

        multi = Layer4Pipeline._aggregate_multi_metric(per_metric, bonferroni)

        # The invariant: dimension_driver tracks overall_classification.
        if multi.overall_classification == RegressionClass.REGRESSION:
            assert multi.dimension_driver == "completeness"
        else:
            assert multi.dimension_driver is None


# ---------------------------------------------------------------------------
# Lazy import path: Layer4Pipeline without injected report_generator
# ---------------------------------------------------------------------------


class TestPipelineLazyImport:
    """Layer4Pipeline.__init__ creates a default ReportGenerator when none provided.

    This covers lines 102-104 (lazy import branch) in layer4_stats.py.
    The real ReportGenerator is imported; no LLM calls are made because
    smoke mode is used (no statistical computation).
    """

    def test_pipeline_constructs_without_report_generator(self, mock_store: MagicMock) -> None:
        """Layer4Pipeline must construct without report_generator argument.

        Uses smoke mode to avoid driving ReportGenerator's statistical methods,
        which require real score data and LLM infrastructure.
        """
        # Construct without injecting report_generator — triggers lazy import.
        p = Layer4Pipeline(baseline_store=mock_store)
        # If construction succeeded, the lazy import path was taken.
        assert p._gen is not None  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# _persist_report(): file write coverage
# ---------------------------------------------------------------------------


class TestPersistReport:
    """Layer4Pipeline._persist_report() writes JSON and Markdown to disk.

    Covers lines 408-410, 413-417 in layer4_stats.py.
    Uses tmp_path fixture for filesystem isolation.
    """

    def test_persist_report_writes_json(
        self,
        mock_store: MagicMock,
        mock_generator: MagicMock,
        tmp_path,
    ) -> None:
        """_persist_report() writes JSON file when json_path is provided."""
        scores = _make_scores(30)
        json_path = tmp_path / "report.json"

        pipeline = Layer4Pipeline(baseline_store=mock_store, report_generator=mock_generator)
        pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={"composite_score": (scores, scores[::-1])},
            evaluation_mode=EvaluationMode.FULL,
            output_json_path=json_path,
        )

        assert json_path.exists()
        assert json_path.read_text() == "{}"  # mock_generator.to_json returns "{}"

    def test_persist_report_writes_markdown(
        self,
        mock_store: MagicMock,
        mock_generator: MagicMock,
        tmp_path,
    ) -> None:
        """_persist_report() writes Markdown file when output_markdown_path is provided."""
        scores = _make_scores(30)
        md_path = tmp_path / "report.md"

        pipeline = Layer4Pipeline(baseline_store=mock_store, report_generator=mock_generator)
        pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={"composite_score": (scores, scores[::-1])},
            evaluation_mode=EvaluationMode.FULL,
            output_markdown_path=md_path,
        )

        assert md_path.exists()
        assert md_path.read_text() == "# Report"  # mock_generator.to_markdown returns "# Report"

    def test_persist_report_creates_parent_dirs(
        self,
        mock_store: MagicMock,
        mock_generator: MagicMock,
        tmp_path,
    ) -> None:
        """_persist_report() creates parent directories for JSON output."""
        scores = _make_scores(30)
        nested_json = tmp_path / "nested" / "deep" / "report.json"

        pipeline = Layer4Pipeline(baseline_store=mock_store, report_generator=mock_generator)
        pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={"composite_score": (scores, scores[::-1])},
            evaluation_mode=EvaluationMode.FULL,
            output_json_path=nested_json,
        )

        assert nested_json.exists()


# ---------------------------------------------------------------------------
# _emit_gha_outputs(): GHA output file and dimension_driver branch
# ---------------------------------------------------------------------------


class TestEmitGhaOutputs:
    """Layer4Pipeline._emit_gha_outputs() writes to GITHUB_OUTPUT when set.

    Covers lines 440, 444-449 in layer4_stats.py.
    """

    def test_emit_gha_outputs_with_dimension_driver(
        self,
        mock_store: MagicMock,
        mock_generator: MagicMock,
        tmp_path,
        monkeypatch,
    ) -> None:
        """When dimension_driver is set, it must be included in GHA outputs."""
        gha_output_file = tmp_path / "github_output.txt"
        monkeypatch.setenv("GITHUB_OUTPUT", str(gha_output_file))

        # Report with dimension_driver set — covers line 440.
        mock_generator.from_single_metric.return_value = _make_comparison_report(
            classification="REGRESSION",
            merge_recommendation=MergeDecision.BLOCK.value,
            dimension_driver="completeness",
        )

        scores = _make_scores(30)
        pipeline = Layer4Pipeline(baseline_store=mock_store, report_generator=mock_generator)
        pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={"composite_score": (scores, scores[::-1])},
            evaluation_mode=EvaluationMode.FULL,
        )

        output_text = gha_output_file.read_text()
        assert "dimension_driver=completeness" in output_text
        assert "verdict=REGRESSION" in output_text

    def test_emit_gha_outputs_writes_to_github_output_file(
        self,
        mock_store: MagicMock,
        mock_generator: MagicMock,
        tmp_path,
        monkeypatch,
    ) -> None:
        """GHA output file receives all required key=value lines.

        FR-018: GitHub Actions requires strict ``key=value`` line format.
        Each output must be on its own newline-terminated line with exactly
        one ``=`` separator between the key and value, with no surrounding
        whitespace in the key.  This format is consumed by the GHA runner to
        populate ``${{ steps.<id>.outputs.<key> }}`` expressions.
        """
        import re

        gha_output_file = tmp_path / "github_output.txt"
        monkeypatch.setenv("GITHUB_OUTPUT", str(gha_output_file))

        scores = _make_scores(30)
        pipeline = Layer4Pipeline(baseline_store=mock_store, report_generator=mock_generator)
        pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={"composite_score": (scores, scores[::-1])},
            evaluation_mode=EvaluationMode.FULL,
        )

        output_text = gha_output_file.read_text()
        lines = [ln for ln in output_text.splitlines() if ln.strip()]

        # Each non-empty line must match the strict GHA key=value format.
        # Key: identifier characters only (no whitespace).  Value: anything.
        kv_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=.*$")
        for line in lines:
            assert kv_pattern.match(line), (
                f"GHA output line does not conform to key=value format: {line!r}"
            )

        # FR-018: verify the three required output keys are present.
        keys_present = {ln.split("=", 1)[0] for ln in lines}
        assert "verdict" in keys_present, "GHA output missing required key 'verdict'"
        assert "merge_recommendation" in keys_present, (
            "GHA output missing required key 'merge_recommendation'"
        )
        assert "agent" in keys_present, "GHA output missing required key 'agent'"

    def test_emit_gha_outputs_oserror_does_not_raise(
        self,
        mock_store: MagicMock,
        mock_generator: MagicMock,
        monkeypatch,
    ) -> None:
        """OSError writing to GITHUB_OUTPUT must be swallowed (covers line 449)."""
        # Set GITHUB_OUTPUT to a path that cannot be written.
        monkeypatch.setenv("GITHUB_OUTPUT", "/nonexistent_dir/github_output.txt")

        scores = _make_scores(30)
        pipeline = Layer4Pipeline(baseline_store=mock_store, report_generator=mock_generator)

        # Must not raise — OSError is caught and logged.
        exit_code = pipeline.run(
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            metric_scores={"composite_score": (scores, scores[::-1])},
            evaluation_mode=EvaluationMode.FULL,
        )

        assert exit_code in (0, 1, 2)


# ---------------------------------------------------------------------------
# _aggregate_multi_metric(): MARGINAL dimension driver branch
# ---------------------------------------------------------------------------


class TestAggregateMultiMetricMarginalDriver:
    """_aggregate_multi_metric() sets dimension driver when overall is MARGINAL.

    Covers lines 373-378 in layer4_stats.py (the MARGINAL branch).
    This requires a metric classified as MARGINAL — not REGRESSION.
    MARGINAL occurs when: alpha <= p < alpha_marginal AND r >= EFFECT_SMALL.
    """

    def test_aggregate_marginal_sets_dimension_driver(self) -> None:
        """When overall classification is MARGINAL, dimension_driver must be set.

        We use compare_versions() to produce a result and then manually override
        the classification field to MARGINAL to trigger the branch, since
        producing exact MARGINAL conditions is statistically fragile.
        """
        from dataclasses import replace as dc_replace

        from jerry.testing.stats import compare_versions

        # Produce a real RegressionResult to get valid Wilcoxon/Wilson data.
        scores_a = [0.93 if i % 2 == 0 else 0.91 for i in range(30)]
        scores_b = [0.70 if i % 2 == 0 else 0.68 for i in range(30)]
        base_result = compare_versions(
            scores_a,
            scores_b,
            metric_id="completeness",
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-researcher.md",
            evaluation_mode=EvaluationMode.FULL,
        )

        # Override classification to MARGINAL to exercise the MARGINAL branch.
        marginal_result = dc_replace(
            base_result,
            classification=RegressionClass.MARGINAL,
            merge_decision=MergeDecision.ALLOW_WITH_WARNING,
        )

        bonferroni = BonferroniConfig(k=2, alpha_family=0.05, alpha_per_test=0.025)

        per_metric = {"completeness": marginal_result}
        multi = Layer4Pipeline._aggregate_multi_metric(per_metric, bonferroni)

        # Aggregation must preserve all input metric entries.
        assert len(multi.per_metric) == 1, (
            f"Expected 1 entry in per_metric, got {len(multi.per_metric)}"
        )

        # MARGINAL overall + MARGINAL metric → dimension_driver is set.
        assert multi.overall_classification == RegressionClass.MARGINAL
        assert multi.dimension_driver == "completeness"
