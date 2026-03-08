# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

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

    @staticmethod
    def _validate_output_path(path: Path) -> Path:
        """Validate that an output path is within safe boundaries (CG-025).

        Resolves the path to its absolute form and verifies it is contained
        within the current working directory.  Paths that resolve outside the
        CWD (e.g., via ``../`` traversal sequences) are rejected to prevent
        accidental or malicious writes to arbitrary filesystem locations.

        Args:
            path: The output path to validate.

        Returns:
            The resolved absolute Path when validation passes.

        Raises:
            ValueError: If the resolved path escapes the current working
                        directory (path traversal rejected).
        """
        resolved = path.resolve()
        cwd = Path.cwd().resolve()
        if not resolved.is_relative_to(cwd):
            raise ValueError(
                f"Output path {path} resolves to {resolved} which is outside "
                f"the working directory {cwd}. Path traversal rejected (CG-025)."
            )
        return resolved

    def _persist_report(
        self,
        report: ComparisonReport,
        json_path: Path | None,
        markdown_path: Path | None,
    ) -> None:
        """Write JSON and Markdown reports to disk if paths are provided.

        Validates each path against the current working directory before
        writing to prevent path traversal writes (CG-025).

        Args:
            report:        The ComparisonReport to persist.
            json_path:     Destination path for JSON report.
            markdown_path: Destination path for Markdown report.

        Raises:
            ValueError: If either path resolves outside the working directory.
        """
        if json_path is not None:
            safe_json = self._validate_output_path(json_path)
            safe_json.parent.mkdir(parents=True, exist_ok=True)
            safe_json.write_text(self._gen.to_json(report), encoding="utf-8")
            logger.info("JSON report written to %s.", safe_json)

        if markdown_path is not None:
            safe_md = self._validate_output_path(markdown_path)
            safe_md.parent.mkdir(parents=True, exist_ok=True)
            safe_md.write_text(self._gen.to_markdown(report), encoding="utf-8")
            logger.info("Markdown report written to %s.", safe_md)

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
                        # CG-018A: Sanitize newlines to prevent GHA output format
                        # corruption. Newlines in values break the key=value\n
                        # protocol that GitHub Actions uses to parse workflow outputs.
                        safe_value = str(value).replace("\n", " ").replace("\r", " ")
                        fh.write(f"{key}={safe_value}\n")
            except OSError as exc:
                logger.warning("Failed to write GHA outputs: %s", exc)
        else:
            # Local development — emit to stdout for debugging.
            # Uses plain key=value format (GHA ::set-output is deprecated).
            for key, value in outputs.items():
                # CG-018A: Sanitize newlines in logged values as well.
                safe_value = str(value).replace("\n", " ").replace("\r", " ")
                logger.info("GHA_OUTPUT %s=%s", key, safe_value)

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


# ------------------------------------------------------------------
# CLI entry point (CG-001)
# ------------------------------------------------------------------


def main() -> int:
    """CLI entry point for the Layer 4 statistical comparison pipeline.

    Parses command-line arguments matching the GitHub Actions workflow
    invocation flags (prompt-regression-full.yml, prompt-regression-standard.yml)
    and initialises the pipeline.  Pipeline execution is wired via
    extract_score_arrays() and pipeline.run() (CG-001/CG-002).

    Returns:
        Exit code: 0 (pass), 1 (regression/error), 2 (marginal) per FR-018.

    References:
        CG-001: main() argparse entry point (gap-analysis-20260307-001).
        CG-002: BaselineStore integration (gap-closure-20260307-001).
        FR-015: Per-agent score extraction and comparison — CLI must accept and route
                multiple metric score arrays to the pipeline for comparison.
        FR-016: Statistical significance testing with Wilcoxon signed-rank — mandated
                as the primary non-parametric test for paired score comparison.
        FR-017: Bonferroni correction for multiple comparisons — --bonferroni-k overrides
                the correction factor (default: 13 for full tier, metric count otherwise).
        FR-018: CI/CD exit codes and GHA outputs — exit 0 (pass), exit 1 (regression),
                exit 2 (marginal warning); $GITHUB_OUTPUT writes for verdict,
                merge_recommendation, agent, evaluation_mode.
    """
    import argparse  # noqa: PLC0415
    import json as json_mod  # noqa: PLC0415
    import re  # noqa: PLC0415

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Layer 4 statistical comparison pipeline for prompt regression harness.",
    )
    parser.add_argument(
        "--agent",
        required=True,
        help="Agent ID string (e.g., 'ps-researcher').",
    )
    parser.add_argument(
        "--tier",
        required=True,
        choices=["smoke", "standard", "full"],
        help=(
            "Evaluation tier: smoke (structural checks only, no statistical tests),"
            " standard (default, all agents, Wilcoxon per metric, k=metric count),"
            " full (N>=30 statistical baseline, Bonferroni k=13 per FR-017)."
        ),  # FR-005: Tiered evaluation mode (SMOKE/STANDARD/FULL).
    )
    parser.add_argument(
        "--results-file",
        required=True,
        help="Path to promptfoo results JSON file.",
    )
    parser.add_argument(
        "--head-sha",
        required=True,
        help="Git HEAD commit SHA.",
    )
    parser.add_argument(
        "--base-sha",
        default=None,
        help="Git base commit SHA for comparison (optional).",
    )
    parser.add_argument(
        "--agent-file",
        default=None,
        help="Agent definition file path for version key construction (optional).",
    )
    parser.add_argument(
        "--bonferroni-k",
        type=int,
        default=None,
        help=(
            "Number of simultaneous comparisons for Bonferroni correction;"
            " defaults to 13 for full tier or metric count for standard tier."
            " See FR-017."
        ),  # FR-017: Bonferroni correction factor.
    )
    parser.add_argument(
        "--output-report",
        default=None,
        help="Path for JSON report output (optional).",
    )
    parser.add_argument(
        "--output-markdown",
        default=None,
        help="Path for Markdown report output (optional).",
    )

    args = parser.parse_args()

    # --- CG-018B: Validate agent ID format before constructing the pipeline ---
    # agent_id must start with a lowercase letter and contain only lowercase
    # alphanumerics, hyphens, and underscores.  This prevents injection of
    # malformed identifiers into log messages, GHA outputs, and filesystem paths.
    if not re.match(r"^[a-z][a-z0-9_-]*$", args.agent):
        logger.error("Invalid agent ID format: %s (must match ^[a-z][a-z0-9_-]*$)", args.agent)
        return 1

    # --- Validate results file exists and is valid JSON ---
    results_path = Path(args.results_file)
    if not results_path.exists():
        logger.error("Results file does not exist: %s", results_path)
        return 1

    try:
        json_mod.loads(results_path.read_text(encoding="utf-8"))
    except json_mod.JSONDecodeError as exc:
        logger.error("Results file is not valid JSON: %s — %s", results_path, exc)
        return 1

    # --- Construct version keys ---
    if args.agent_file:
        head_version_key = f"{args.head_sha}:{args.agent_file}"
    else:
        head_version_key = args.head_sha

    base_version_key: str | None = None
    if args.base_sha:
        if args.agent_file:
            base_version_key = f"{args.base_sha}:{args.agent_file}"
        else:
            base_version_key = args.base_sha

    # --- Create pipeline instance ---
    # CG-002: BaselineStore is constructed here with the conventional baselines/data
    # directory.  This path is the agreed storage root for persisted score records
    # (gap-closure-20260307-001).  Path is anchored to the package root via __file__
    # to remain correct regardless of the caller's working directory.
    from jerry.testing.baselines.store import BaselineStore  # noqa: PLC0415

    store = BaselineStore(
        Path(__file__).parents[3] / "baselines" / "data"
    )  # NB: __file__-relative; independent of CWD.
    pipeline = Layer4Pipeline(baseline_store=store)

    # --- Log configuration ---
    logger.info("Layer 4 pipeline initialised.")
    logger.info("  agent:            %s", args.agent)
    logger.info("  tier:             %s", args.tier)
    logger.info("  results-file:     %s", results_path)
    logger.info("  head-sha:         %s", args.head_sha)
    logger.info("  base-sha:         %s", args.base_sha)
    logger.info("  agent-file:       %s", args.agent_file)
    logger.info("  head-version-key: %s", head_version_key)
    logger.info("  base-version-key: %s", base_version_key)
    logger.info("  bonferroni-k:     %s", args.bonferroni_k)
    logger.info("  output-report:    %s", args.output_report)
    logger.info("  output-markdown:  %s", args.output_markdown)

    # --- Extract score arrays from results file (CG-008) ---
    # extract_score_arrays returns {metric: (head_scores, base_scores)}.
    # pipeline.run() expects metric_scores as {metric: (scores_a, scores_b)}
    # where a=baseline (base) and b=candidate (head).  Swap accordingly.
    from jerry.testing.extraction.promptfoo_extractor import extract_score_arrays  # noqa: PLC0415

    try:
        raw_arrays = extract_score_arrays(results_path)
    except (FileNotFoundError, ValueError) as exc:
        logger.error("Failed to extract score arrays from results file: %s", exc)
        return 1

    # Swap (head, base) → (base, head) to match pipeline.run() convention (a=baseline).
    metric_scores = {
        metric: (base_scores, head_scores)
        for metric, (head_scores, base_scores) in raw_arrays.items()
    }

    # --- Map tier string to EvaluationMode enum ---
    evaluation_mode = EvaluationMode[args.tier.upper()]  # smoke→SMOKE, standard→STANDARD, full→FULL

    # --- Resolve output paths (CG-010) ---
    output_json_path = Path(args.output_report) if args.output_report else None
    output_markdown_path = Path(args.output_markdown) if args.output_markdown else None

    # --- Execute pipeline (FR-015, FR-016, FR-017, FR-018) ---
    # For SMOKE tier: metric_scores is not consumed by _run_smoke(); version_key_a
    # is used as the structural check key.  For STANDARD/FULL: metric_scores drives
    # Wilcoxon comparison with optional Bonferroni correction.
    exit_code = pipeline.run(
        agent_id=args.agent,
        version_key_a=base_version_key or head_version_key,
        version_key_b=head_version_key,
        metric_scores=metric_scores,
        evaluation_mode=evaluation_mode,
        bonferroni_k=args.bonferroni_k,
        output_json_path=output_json_path,
        output_markdown_path=output_markdown_path,
    )

    return exit_code


if __name__ == "__main__":
    import sys  # noqa: PLC0415

    sys.exit(main())
