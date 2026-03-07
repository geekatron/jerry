# SPDX-License-Identifier: Apache-2.0
"""Layer 4 pipeline orchestrator for the Four-Layer Composite Test Harness.

This module orchestrates the Layer 4 statistical comparison pipeline.  It
imports statistical functions exclusively from ``jerry.testing.stats`` — it
does NOT re-implement any statistical logic (FR-019 one-way dependency rule).

Responsibilities of this module (distinct from stats.py):
    - Orchestrate multi-metric comparison with Bonferroni correction.
    - Determine the overall classification and dimension driver.
    - Call the report generator (via ReportOutputPort).
    - Interact with the baseline store (via BaselinePersistencePort).
    - Format GitHub Actions output and exit codes for CI/CD integration.
    - Provide a single entry point for the Layer 4 pipeline stage.

Dependency direction (H-07 compliance):
    layer4_stats.py  →  stats.py        (allowed: adapter → domain)
    layer4_stats.py  →  types.py        (allowed: adapter → domain)
    layer4_stats.py  →  baselines/store (allowed: adapter → adapter via port)
    layer4_stats.py  →  reports/generator (conditional: lazy import in __init__ only)
    stats.py         ↛  layer4_stats.py (FORBIDDEN: domain must not import adapter)

H-10 compliance: One class (Layer4Pipeline) defined in this file.
H-11 compliance: All public methods have type annotations and docstrings.
"""

from __future__ import annotations

import logging
from pathlib import Path

from jerry.testing.baselines.ports import BaselinePersistencePort
from jerry.testing.reports.ports import ReportOutputPort
from jerry.testing.stats import (
    BONFERRONI_K_FULL_SUITE,
    compare_multiple_metrics,
    compare_versions,
    merge_decision_from_classification,
)
from jerry.testing.types import (
    BonferroniConfig,
    ComparisonReport,
    EvaluationMode,
    MergeDecision,
    MultiMetricResult,
    RegressionClass,
    RegressionResult,
    ScoreArray,
)

logger = logging.getLogger(__name__)


class Layer4Pipeline:
    """Orchestrates the Layer 4 statistical comparison pipeline.

    Entry point for the harness's statistical stage.  Accepts score arrays
    from Layer 2/3, runs the appropriate comparison (single-metric or
    multi-metric Bonferroni), generates the regression report, and emits
    CI/CD exit signals.

    Usage::

        pipeline = Layer4Pipeline(
            baseline_store=BaselineStore(Path("baselines/data")),
            report_generator=ReportGenerator(),
        )
        exit_code = pipeline.run(
            agent_id="ps-researcher",
            version_key_a="abc1234:skills/ps-researcher.md",
            version_key_b="def5678:skills/ps-researcher.md",
            metric_scores={
                "composite_score": (scores_baseline, scores_candidate),
                "completeness": (comp_a, comp_b),
                # ... up to 13 metrics for the full Bonferroni suite
            },
            evaluation_mode=EvaluationMode.FULL,
            output_json_path=Path("regression-report.json"),
            output_markdown_path=Path("regression-report.md"),
        )
        sys.exit(exit_code)
    """

    def __init__(
        self,
        baseline_store: BaselinePersistencePort,
        report_generator: ReportOutputPort | None = None,
    ) -> None:
        """Initialise the Layer 4 pipeline.

        Args:
            baseline_store:   BaselineStore adapter for persisting and
                              retrieving score records.
            report_generator: ReportGenerator to use.  A default instance
                              is created if not provided.
        """
        self._store = baseline_store
        if report_generator is None:
            # Lazy import: avoids a top-level concrete adapter import, keeping
            # the module's import graph restricted to ports (H-07 compliance).
            # Callers may inject any ReportOutputPort implementation to override.
            from jerry.testing.reports.generator import ReportGenerator  # noqa: PLC0415

            report_generator = ReportGenerator()
        self._gen = report_generator

    def run(
        self,
        agent_id: str,
        version_key_a: str,
        version_key_b: str,
        metric_scores: dict[str, tuple[ScoreArray, ScoreArray]],
        evaluation_mode: EvaluationMode,
        *,
        structural_violations: list[str] | None = None,
        output_json_path: Path | None = None,
        output_markdown_path: Path | None = None,
        apply_bonferroni: bool = True,
        bonferroni_k: int | None = None,
    ) -> int:
        """Execute the full Layer 4 pipeline for one agent evaluation.

        Compares baseline vs candidate score arrays across all supplied metrics
        with optional Bonferroni correction, generates the regression report,
        persists report artifacts, and returns the CI/CD exit code.

        Args:
            agent_id:               Target agent identifier.
            version_key_a:          Baseline version key ("{hash}:{path}").
            version_key_b:          Candidate version key.
            metric_scores:          Mapping of metric_id → (scores_a, scores_b).
                                    Each array must have N >= 20 for FULL mode.
            evaluation_mode:        Evaluation tier.
            structural_violations:  Structural invariant failures from Layer 2.
                                    If present, are included in the narrative.
            output_json_path:       If provided, writes the JSON regression
                                    report to this path.
            output_markdown_path:   If provided, writes the Markdown regression
                                    report to this path.
            apply_bonferroni:       Whether to apply Bonferroni correction for
                                    multi-metric comparisons.  Defaults to True.
            bonferroni_k:           Override for Bonferroni k.  Defaults to
                                    BONFERRONI_K_FULL_SUITE (13) for FULL mode,
                                    len(metric_scores) for STANDARD mode.

        Returns:
            Exit code for CI/CD:
                0 — NO_REGRESSION, IMPROVEMENT, STRUCTURAL_PASS
                1 — REGRESSION, QUALITY_FLOOR_BREACH, STRUCTURAL_FAIL
                2 — MARGINAL (warning; does not block merge)
        """
        if evaluation_mode == EvaluationMode.SMOKE:
            return self._run_smoke(agent_id, version_key_a, structural_violations or [])

        report = self._run_statistical(
            agent_id=agent_id,
            version_key_a=version_key_a,
            version_key_b=version_key_b,
            metric_scores=metric_scores,
            evaluation_mode=evaluation_mode,
            structural_violations=structural_violations or [],
            apply_bonferroni=apply_bonferroni,
            bonferroni_k=bonferroni_k,
        )

        self._persist_report(report, output_json_path, output_markdown_path)
        self._emit_gha_outputs(report)

        return self._exit_code(report)

    def run_single_metric(
        self,
        agent_id: str,
        metric_id: str,
        version_key_a: str,
        version_key_b: str,
        scores_a: ScoreArray,
        scores_b: ScoreArray,
        evaluation_mode: EvaluationMode = EvaluationMode.FULL,
        *,
        structural_violations: list[str] | None = None,
        output_json_path: Path | None = None,
        output_markdown_path: Path | None = None,
    ) -> tuple[RegressionResult, ComparisonReport]:
        """Run a single-metric comparison (no Bonferroni correction).

        Convenience wrapper for cases where only one metric is being compared.
        The Bonferroni correction is not applied; the uncorrected alpha=0.05
        is used.

        Args:
            agent_id:               Target agent identifier.
            metric_id:              Metric being compared.
            version_key_a:          Baseline version key.
            version_key_b:          Candidate version key.
            scores_a:               Baseline score array.
            scores_b:               Candidate score array.
            evaluation_mode:        Evaluation tier (must not be SMOKE).
            structural_violations:  Structural invariant failures.
            output_json_path:       Optional path to write JSON report.
            output_markdown_path:   Optional path to write Markdown report.

        Returns:
            Tuple of (RegressionResult, ComparisonReport).

        Raises:
            InsufficientSamplesError: If N < 20 for either array.
            InvalidScoreArrayError:   If array validation fails.
        """
        result = compare_versions(
            scores_a,
            scores_b,
            metric_id=metric_id,
            agent_id=agent_id,
            version_key_a=version_key_a,
            version_key_b=version_key_b,
            evaluation_mode=evaluation_mode,
        )
        report = self._gen.from_single_metric(
            result,
            structural_violations=structural_violations,
        )
        self._persist_report(report, output_json_path, output_markdown_path)
        self._emit_gha_outputs(report)
        return result, report

    # ------------------------------------------------------------------
    # Private pipeline stages
    # ------------------------------------------------------------------

    def _run_smoke(
        self,
        agent_id: str,
        version_key: str,
        structural_violations: list[str],
    ) -> int:
        """Execute Smoke mode: structural checks only, no statistics.

        Args:
            agent_id:               Agent identifier.
            version_key:            Version key of evaluated prompt.
            structural_violations:  Section A invariant failures.

        Returns:
            Exit code (0 for pass, 1 for structural failures).
        """
        report = self._gen.smoke_mode_report(agent_id, version_key, structural_violations)
        self._emit_gha_outputs(report)
        return 1 if structural_violations else 0

    def _run_statistical(
        self,
        agent_id: str,
        version_key_a: str,
        version_key_b: str,
        metric_scores: dict[str, tuple[ScoreArray, ScoreArray]],
        evaluation_mode: EvaluationMode,
        structural_violations: list[str],
        apply_bonferroni: bool,
        bonferroni_k: int | None,
    ) -> ComparisonReport:
        """Execute statistical comparison (STANDARD or FULL mode).

        For single-metric inputs, uses uncorrected alpha.  For multi-metric
        inputs, applies Bonferroni correction when apply_bonferroni=True.

        Args:
            agent_id:               Target agent identifier.
            version_key_a:          Baseline version key.
            version_key_b:          Candidate version key.
            metric_scores:          Per-metric (scores_a, scores_b) pairs.
            evaluation_mode:        STANDARD or FULL.
            structural_violations:  Structural invariant failures.
            apply_bonferroni:       Whether to apply Bonferroni.
            bonferroni_k:           Override for k in Bonferroni correction.

        Returns:
            ComparisonReport ready for serialisation and CI output.
        """
        if len(metric_scores) == 1 or not apply_bonferroni:
            # Single-metric path — no Bonferroni.
            metric_id, (sa, sb) = next(iter(metric_scores.items()))
            result = compare_versions(
                sa,
                sb,
                metric_id=metric_id,
                agent_id=agent_id,
                version_key_a=version_key_a,
                version_key_b=version_key_b,
                evaluation_mode=evaluation_mode,
            )
            return self._gen.from_single_metric(
                result,
                structural_violations=structural_violations,
            )

        # Multi-metric path — Bonferroni correction.
        effective_k = bonferroni_k
        if effective_k is None:
            effective_k = (
                BONFERRONI_K_FULL_SUITE
                if evaluation_mode == EvaluationMode.FULL
                else len(metric_scores)
            )

        per_metric, bc = compare_multiple_metrics(
            metric_scores,
            agent_id=agent_id,
            version_key_a=version_key_a,
            version_key_b=version_key_b,
            evaluation_mode=evaluation_mode,
            k=effective_k,
        )

        multi_result = self._aggregate_multi_metric(per_metric, bc)

        return self._gen.from_multi_metric(
            multi_result=multi_result,
            agent_id=agent_id,
            version_key_a=version_key_a,
            version_key_b=version_key_b,
            evaluation_mode=evaluation_mode,
            structural_violations=structural_violations,
        )

    @staticmethod
    def _aggregate_multi_metric(
        per_metric: dict[str, RegressionResult],
        bonferroni: BonferroniConfig,
    ) -> MultiMetricResult:
        """Derive the overall MultiMetricResult from individual metric results.

        Overall classification is the worst-case across all metrics.
        The dimension driver is the metric with the lowest p-value among
        those classified as REGRESSION or QUALITY_FLOOR_BREACH.

        Args:
            per_metric: Per-metric RegressionResult mapping.
            bonferroni: Bonferroni config used for the comparison.

        Returns:
            MultiMetricResult.
        """
        # Classification severity order (worst wins).
        severity: dict[RegressionClass, int] = {
            RegressionClass.NO_REGRESSION: 0,
            RegressionClass.IMPROVEMENT: 1,
            RegressionClass.MARGINAL: 2,
            RegressionClass.QUALITY_FLOOR_BREACH: 3,
            RegressionClass.REGRESSION: 4,
            RegressionClass.STRUCTURAL_FAIL: 5,
        }
        worst = RegressionClass.NO_REGRESSION
        for res in per_metric.values():
            if severity.get(res.classification, 0) > severity.get(worst, 0):
                worst = res.classification

        # Dimension driver: metric with lowest p-value among failing metrics.
        failing = [
            (mid, r)
            for mid, r in per_metric.items()
            if r.classification
            in (
                RegressionClass.REGRESSION,
                RegressionClass.QUALITY_FLOOR_BREACH,
            )
        ]
        if failing:
            driver = min(failing, key=lambda x: x[1].wilcoxon.p_value)[0]
        elif worst == RegressionClass.MARGINAL:
            # Use marginal metrics as driver when no full regression.
            marginal = [
                (mid, r)
                for mid, r in per_metric.items()
                if r.classification == RegressionClass.MARGINAL
            ]
            driver = min(marginal, key=lambda x: x[1].wilcoxon.p_value)[0] if marginal else None
        else:
            driver = None

        return MultiMetricResult(
            overall_classification=worst,
            merge_decision=merge_decision_from_classification(worst),
            per_metric=per_metric,
            bonferroni=bonferroni,
            dimension_driver=driver,
        )

    # ------------------------------------------------------------------
    # Artifact persistence and CI/CD integration
    # ------------------------------------------------------------------

    def _persist_report(
        self,
        report: ComparisonReport,
        json_path: Path | None,
        markdown_path: Path | None,
    ) -> None:
        """Write JSON and Markdown reports to disk if paths are provided.

        Args:
            report:        The ComparisonReport to persist.
            json_path:     Destination path for JSON report.
            markdown_path: Destination path for Markdown report.
        """
        if json_path is not None:
            json_path.parent.mkdir(parents=True, exist_ok=True)
            json_path.write_text(self._gen.to_json(report), encoding="utf-8")
            logger.info("JSON report written to %s.", json_path)

        if markdown_path is not None:
            markdown_path.parent.mkdir(parents=True, exist_ok=True)
            markdown_path.write_text(self._gen.to_markdown(report), encoding="utf-8")
            logger.info("Markdown report written to %s.", markdown_path)

    @staticmethod
    def _emit_gha_outputs(report: ComparisonReport) -> None:
        """Emit GitHub Actions workflow output variables (FR-018 CI/CD integration).

        Writes to the GHA output file when GITHUB_OUTPUT is set in the
        environment, enabling subsequent workflow steps to read the verdict
        per FR-018 acceptance criteria (exit code + structured outputs).
        Falls back to logger.info when not in a GHA context.

        Args:
            report: The ComparisonReport to emit.
        """
        import os  # noqa: PLC0415

        outputs = {
            "verdict": report.classification,
            "merge_recommendation": report.merge_recommendation,
            "agent": report.agent,
            "evaluation_mode": report.evaluation_mode,
        }
        if report.dimension_driver:
            outputs["dimension_driver"] = report.dimension_driver

        gha_output_file = os.environ.get("GITHUB_OUTPUT")
        if gha_output_file:
            try:
                with open(gha_output_file, "a", encoding="utf-8") as fh:
                    for key, value in outputs.items():
                        fh.write(f"{key}={value}\n")
            except OSError as exc:
                logger.warning("Failed to write GHA outputs: %s", exc)
        else:
            # Local development — emit to stdout for debugging.
            # Uses plain key=value format (GHA ::set-output is deprecated).
            for key, value in outputs.items():
                logger.info("GHA_OUTPUT %s=%s", key, value)

    @staticmethod
    def _exit_code(report: ComparisonReport) -> int:
        """Map merge recommendation to a CI/CD exit code.

        FR-018 acceptance criteria:
            REGRESSION → exit 1 (fail; block merge)
            MARGINAL   → exit 2 (warning; allow merge)
            NO_REGRESSION, IMPROVEMENT → exit 0 (pass)

        Args:
            report: ComparisonReport with merge_recommendation.

        Returns:
            Integer exit code (0, 1, or 2).
        """
        recommendation = report.merge_recommendation
        if recommendation == MergeDecision.BLOCK.value:
            return 1
        if recommendation == MergeDecision.ALLOW_WITH_WARNING.value:
            return 2
        return 0
