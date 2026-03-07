# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Regression report generation for the Four-Layer Composite Test Harness.

Produces structured regression reports in Markdown (for GitHub PR comments)
and JSON (for CI/CD artifact archiving) formats per FR-018 and the JSON
schema defined in behavioral-contracts.md Section D.6.

Verdict classifications produced:
    NO_REGRESSION        — Pass; allow merge.
    MARGINAL             — Allow with warning annotation.
    REGRESSION           — Fail; block merge.
    IMPROVEMENT          — Allow with informational note.
    QUALITY_FLOOR_BREACH — Fail; agent systematically underperforms (Full only).
    STRUCTURAL ONLY      — Smoke mode label; no statistical validity.

Architecture:
    - Hexagonal layer: ADAPTER (outbound).
    - Depends on: jerry.testing.types, stdlib only.
    - MUST NOT be imported by domain modules (stats.py, types.py).

H-10 compliance: One class (ReportGenerator) defined in this file.
H-11 compliance: All public methods have type annotations and docstrings.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from jerry.testing.types import (
    BonferroniConfig,
    ComparisonReport,
    EvaluationMode,
    MergeDecision,
    MultiMetricResult,
    RegressionClass,
    RegressionResult,
)


class ReportGenerator:
    """Generates regression reports from Layer 4 statistical results.

    Supports three output formats:
        - Markdown:     For GitHub PR comments (FR-018).
        - JSON:         For CI/CD artifact archiving (FR-018, D.6 schema).
        - ComparisonReport: Structured Python object for programmatic use.

    Usage example::

        gen = ReportGenerator()
        result = compare_versions(scores_a, scores_b, ...)
        report = gen.from_single_metric(result)
        md = gen.to_markdown(report)
        js = gen.to_json(report)
    """

    # ------------------------------------------------------------------
    # Factory methods: build ComparisonReport from stat results
    # ------------------------------------------------------------------

    def from_single_metric(
        self,
        result: RegressionResult,
        *,
        structural_violations: list[str] | None = None,
    ) -> ComparisonReport:
        """Build a ComparisonReport from a single-metric RegressionResult.

        Args:
            result:                 The RegressionResult from compare_versions().
            structural_violations:  List of structural invariant violation
                                    descriptions, if any (Section A invariants).

        Returns:
            ComparisonReport with all required fields populated.
        """
        narrative = self._narrative_single(result, structural_violations or [])

        return ComparisonReport(
            evaluation_mode=result.evaluation_mode.value,
            agent=result.agent_id,
            prompt_version_baseline=result.version_key_a,
            prompt_version_candidate=result.version_key_b,
            n_baseline=result.n_a,
            n_candidate=result.n_b,
            timestamp=datetime.now(UTC).isoformat() + "Z",
            classification=result.classification.value,
            merge_recommendation=result.merge_decision.value,
            dimension_driver=result.dimension_driver,
            narrative=narrative,
            per_metric_results={result.metric_id: result},
            multi_metric_result=None,
        )

    def from_multi_metric(
        self,
        multi_result: MultiMetricResult,
        agent_id: str,
        version_key_a: str,
        version_key_b: str,
        evaluation_mode: EvaluationMode,
        *,
        structural_violations: list[str] | None = None,
    ) -> ComparisonReport:
        """Build a ComparisonReport from a multi-metric Bonferroni-corrected result.

        Args:
            multi_result:           The MultiMetricResult from compare_multiple_metrics().
            agent_id:               Target agent identifier.
            version_key_a:          Baseline version key.
            version_key_b:          Candidate version key.
            evaluation_mode:        Evaluation mode used.
            structural_violations:  Structural invariant violation descriptions.

        Returns:
            ComparisonReport with Bonferroni disclosure in narrative.
        """
        # Determine representative N from the first metric result.
        first = next(iter(multi_result.per_metric.values()))
        n_a = first.n_a
        n_b = first.n_b

        narrative = self._narrative_multi(multi_result, structural_violations or [])

        return ComparisonReport(
            evaluation_mode=evaluation_mode.value,
            agent=agent_id,
            prompt_version_baseline=version_key_a,
            prompt_version_candidate=version_key_b,
            n_baseline=n_a,
            n_candidate=n_b,
            timestamp=datetime.now(UTC).isoformat() + "Z",
            classification=multi_result.overall_classification.value,
            merge_recommendation=multi_result.merge_decision.value,
            dimension_driver=multi_result.dimension_driver,
            narrative=narrative,
            per_metric_results=dict(multi_result.per_metric),
            multi_metric_result=multi_result,
        )

    def smoke_mode_report(
        self,
        agent_id: str,
        version_key: str,
        structural_violations: list[str],
    ) -> ComparisonReport:
        """Build a STRUCTURAL ONLY report for Smoke mode evaluations.

        Smoke mode does not perform statistical comparison.  The report is
        explicitly labelled as "STRUCTURAL ONLY — not statistically valid"
        per FR-005 acceptance criteria.

        Args:
            agent_id:               Target agent identifier.
            version_key:            Version key of the evaluated prompt.
            structural_violations:  Structural invariant failures, if any.

        Returns:
            ComparisonReport with classification="STRUCTURAL ONLY".
        """
        has_violations = bool(structural_violations)
        classification = (
            RegressionClass.STRUCTURAL_FAIL.value if has_violations else "STRUCTURAL_PASS"
        )
        merge = MergeDecision.BLOCK.value if has_violations else MergeDecision.ALLOW.value
        violations_text = (
            "\n".join(f"  - {v}" for v in structural_violations) if has_violations else "  None"
        )
        narrative = (
            f"STRUCTURAL ONLY — not statistically valid.\n"
            f"Agent: {agent_id}  Version: {version_key}\n"
            f"Structural invariant violations:\n{violations_text}"
        )

        return ComparisonReport(
            evaluation_mode=EvaluationMode.SMOKE.value,
            agent=agent_id,
            prompt_version_baseline=version_key,
            prompt_version_candidate=version_key,
            n_baseline=1,
            n_candidate=1,
            timestamp=datetime.now(UTC).isoformat() + "Z",
            classification=classification,
            merge_recommendation=merge,
            dimension_driver=None,
            narrative=narrative,
            per_metric_results={},
            multi_metric_result=None,
        )

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_markdown(self, report: ComparisonReport) -> str:
        """Render a ComparisonReport as a GitHub PR comment in Markdown.

        Includes verdict, per-metric Wilcoxon results, Wilson confidence
        intervals per version per metric, and Bonferroni correction disclosure
        (FR-018 acceptance criteria).

        Args:
            report: The ComparisonReport to render.

        Returns:
            Markdown-formatted string suitable for a GitHub PR comment.
        """
        lines: list[str] = []

        verdict_emoji = self._verdict_emoji(report.classification)
        lines.append(f"## {verdict_emoji} Regression Analysis — {report.agent}")
        lines.append("")
        lines.append(
            f"**Mode:** {report.evaluation_mode}  "
            f"**Verdict:** `{report.classification}`  "
            f"**Merge:** `{report.merge_recommendation}`"
        )
        lines.append("")

        if report.evaluation_mode == EvaluationMode.SMOKE.value:
            lines.append("> **STRUCTURAL ONLY — not statistically valid.**")
            lines.append("")
            lines.append(report.narrative)
            return "\n".join(lines)

        # Version info
        lines.append("### Versions")
        lines.append(f"- **Baseline:** `{report.prompt_version_baseline}`  N={report.n_baseline}")
        lines.append(
            f"- **Candidate:** `{report.prompt_version_candidate}`  N={report.n_candidate}"
        )
        lines.append("")

        # Per-metric table
        if report.per_metric_results:
            lines.append("### Per-Metric Results")
            lines.append("")
            lines.append(
                "| Metric | p-value | Cohen's r | Effect | mean_A | mean_B | "
                "CI_A [lo, hi] | CI_B [lo, hi] | Classification |"
            )
            lines.append(
                "|--------|---------|-----------|--------|--------|--------|"
                "--------------|--------------|----------------|"
            )
            for metric_id, res in report.per_metric_results.items():
                w = res.wilcoxon
                wa = res.wilson_a
                wb = res.wilson_b
                ci_a = f"[{wa.ci_lower:.3f}, {wa.ci_upper:.3f}]"
                ci_b = f"[{wb.ci_lower:.3f}, {wb.ci_upper:.3f}]"
                lines.append(
                    f"| {metric_id} | {w.p_value:.4f} | {w.cohens_r:.3f} | "
                    f"{w.effect_label.value} | {w.mean_a:.3f} | {w.mean_b:.3f} | "
                    f"{ci_a} | {ci_b} | `{res.classification.value}` |"
                )
            lines.append("")

        # Bonferroni disclosure (FR-017 acceptance criterion)
        bc = self._find_bonferroni(report)
        if bc is not None:
            lines.append("### Bonferroni Correction")
            lines.append(f"> {bc.description}")
            lines.append("")

        # Wilson CI format per FR-016 acceptance criterion
        if report.per_metric_results:
            lines.append("### Wilson Score Confidence Intervals (95%)")
            for metric_id, res in report.per_metric_results.items():
                wa = res.wilson_a
                wb = res.wilson_b
                lines.append(
                    f"- **{metric_id}** "
                    f"Version A: [{wa.ci_lower:.3f}, {wa.ci_upper:.3f}]; "
                    f"Version B: [{wb.ci_lower:.3f}, {wb.ci_upper:.3f}]"
                )
            lines.append("")

        # Dimension driver
        if report.dimension_driver:
            lines.append(
                f"**Dimension driver:** `{report.dimension_driver}` "
                "(metric that drove the regression classification)"
            )
            lines.append("")

        # Narrative
        lines.append("### Narrative")
        lines.append(report.narrative)

        return "\n".join(lines)

    def to_json(self, report: ComparisonReport) -> str:
        """Serialise a ComparisonReport to JSON matching the D.6 schema.

        Produces a JSON string compatible with the regression report schema
        defined in behavioral-contracts.md Section D.6.

        Args:
            report: The ComparisonReport to serialise.

        Returns:
            Pretty-printed JSON string.
        """
        obj = self._report_to_dict(report)
        return json.dumps(obj, indent=2)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _narrative_single(
        self,
        result: RegressionResult,
        structural_violations: list[str],
    ) -> str:
        """Generate a human-readable narrative for a single-metric result.

        Args:
            result:                 RegressionResult.
            structural_violations:  Structural invariant failures.

        Returns:
            Narrative string.
        """
        w = result.wilcoxon
        cls = result.classification

        if cls == RegressionClass.REGRESSION:
            verb = "statistically significant regression"
        elif cls == RegressionClass.MARGINAL:
            verb = "marginal quality shift (monitor closely)"
        elif cls == RegressionClass.IMPROVEMENT:
            verb = "statistically significant improvement"
        elif cls == RegressionClass.QUALITY_FLOOR_BREACH:
            verb = "quality floor breach (systematic underperformance)"
        else:
            verb = "no statistically significant regression"

        parts = [
            f"Candidate prompt shows {verb} in {result.metric_id} "
            f"(p={w.p_value:.4f}, r={w.cohens_r:.3f}, "
            f"effect={w.effect_label.value}). "
            f"Mean composite score changed by {w.mean_delta:+.4f} "
            f"(A={w.mean_a:.4f} → B={w.mean_b:.4f})."
        ]

        if result.bonferroni:
            parts.append(result.bonferroni.description)

        if structural_violations:
            violation_list = "; ".join(structural_violations)
            parts.append(f"Structural invariant violations detected: {violation_list}.")

        return "  ".join(parts)

    def _narrative_multi(
        self,
        multi: MultiMetricResult,
        structural_violations: list[str],
    ) -> str:
        """Generate a narrative for a multi-metric Bonferroni-corrected result.

        Args:
            multi:                  MultiMetricResult.
            structural_violations:  Structural invariant failures.

        Returns:
            Narrative string.
        """
        driver_text = (
            f"Dimension driver: {multi.dimension_driver}. " if multi.dimension_driver else ""
        )
        regression_metrics = [
            mid
            for mid, r in multi.per_metric.items()
            if r.classification
            in (
                RegressionClass.REGRESSION,
                RegressionClass.QUALITY_FLOOR_BREACH,
            )
        ]
        if regression_metrics:
            regressed = ", ".join(regression_metrics)
            action = (
                f"Regression detected in: {regressed}. "
                "Recommend reviewing prompt changes that may have introduced "
                "degradation in the listed dimensions."
            )
        else:
            action = "No significant regression detected across evaluated metrics."

        parts = [f"{driver_text}{action} {multi.bonferroni.description}."]

        if structural_violations:
            violation_list = "; ".join(structural_violations)
            parts.append(f"Structural invariant violations: {violation_list}.")

        return "  ".join(parts)

    @staticmethod
    def _verdict_emoji(classification: str) -> str:
        """Map a classification string to a GitHub-compatible status emoji.

        Status labels (PASS/WARN/FAIL/INFO) align with FR-018 CI/CD exit code
        semantics (behavioral-contracts.md Section D.6) for PR comment display.

        Args:
            classification: Classification string value.

        Returns:
            Emoji prefix for the PR comment header.
        """
        mapping = {
            "NO_REGRESSION": "PASS",
            "STRUCTURAL_PASS": "PASS",
            "MARGINAL": "WARN",
            "IMPROVEMENT": "PASS",
            "REGRESSION": "FAIL",
            "QUALITY_FLOOR_BREACH": "FAIL",
            "STRUCTURAL_FAIL": "FAIL",
        }
        label = mapping.get(classification, "INFO")
        emoji_map = {
            "PASS": "\u2705",  # green check
            "WARN": "\u26a0\ufe0f",  # warning
            "FAIL": "\u274c",  # red X
            "INFO": "\u2139\ufe0f",  # info
        }
        return emoji_map.get(label, "\u2139\ufe0f")

    @staticmethod
    def _find_bonferroni(report: ComparisonReport) -> BonferroniConfig | None:
        """Extract BonferroniConfig from report if available.

        Args:
            report: The ComparisonReport to inspect.

        Returns:
            BonferroniConfig or None.
        """
        if report.multi_metric_result:
            return report.multi_metric_result.bonferroni
        for res in report.per_metric_results.values():
            if res.bonferroni:
                return res.bonferroni
        return None

    def _report_to_dict(self, report: ComparisonReport) -> dict[str, Any]:
        """Convert a ComparisonReport to a dict matching the D.6 JSON schema.

        The output structure mirrors the example JSON in behavioral-contracts.md
        Section D.6 with additional fields for completeness.

        Args:
            report: The ComparisonReport to convert.

        Returns:
            Dictionary ready for json.dumps().
        """
        per_metric: dict[str, Any] = {}
        for metric_id, res in report.per_metric_results.items():
            w = res.wilcoxon
            wa = res.wilson_a
            wb = res.wilson_b
            per_metric[metric_id] = {
                "statistic": w.statistic,
                "p_value": w.p_value,
                "mean_delta": w.mean_delta,
                "mean_a": w.mean_a,
                "mean_b": w.mean_b,
                "cohens_r": w.cohens_r,
                "effect_size_label": w.effect_label.value,
                "classification": res.classification.value,
                "rate_class": res.rate_class.value,
                "wilson_ci_baseline": {
                    "ci_lower": wa.ci_lower,
                    "ci_upper": wa.ci_upper,
                    "pass_rate": wa.pass_rate,
                    "n_pass": wa.n_pass,
                },
                "wilson_ci_candidate": {
                    "ci_lower": wb.ci_lower,
                    "ci_upper": wb.ci_upper,
                    "pass_rate": wb.pass_rate,
                    "n_pass": wb.n_pass,
                },
            }

        bc_dict: dict[str, Any] | None = None
        bc = self._find_bonferroni(report)
        if bc:
            bc_dict = {
                "k": bc.k,
                "alpha_family": bc.alpha_family,
                "alpha_per_test": bc.alpha_per_test,
                "description": bc.description,
            }

        return {
            "evaluation_mode": report.evaluation_mode,
            "agent": report.agent,
            "prompt_version_baseline": report.prompt_version_baseline,
            "prompt_version_candidate": report.prompt_version_candidate,
            "n_baseline": report.n_baseline,
            "n_candidate": report.n_candidate,
            "timestamp": report.timestamp,
            "classification": report.classification,
            "merge_recommendation": report.merge_recommendation,
            "dimension_driver": report.dimension_driver,
            "narrative": report.narrative,
            "bonferroni_corrected": bc_dict,
            "per_metric": per_metric,
        }
