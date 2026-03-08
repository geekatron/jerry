# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Phase 4 statistical comparison for PROJ-036 FEAT-036-004.

Runs Layer4Pipeline statistical analysis using baseline scores from Phase 3
(or Phase 2 self-comparison for pipeline validation).

Usage:
    uv run python scripts/baseline_stats.py \
        --output-dir projects/PROJ-036-prompt-regression-harness/orchestration/baseline-execution-20260308-001 \
        --agents ps-researcher,ps-architect

    # Pipeline validation mode (no Phase 3 data required):
    uv run python scripts/baseline_stats.py \
        --output-dir projects/PROJ-036-prompt-regression-harness/orchestration/baseline-execution-20260308-001 \
        --agents ps-researcher,ps-architect \
        --validation-mode
"""

from __future__ import annotations

import argparse
import json
import logging
from datetime import UTC, datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# S-014 dimension names
DIMENSIONS = [
    "completeness",
    "internal_consistency",
    "methodological_rigor",
    "evidence_quality",
    "actionability",
    "traceability",
]


def load_phase2_dimension_scores(
    output_dir: Path,
    agents: list[str],
) -> dict[str, dict[str, list[float]]]:
    """Load per-dimension scores from Phase 2 scoring traces.

    Returns: {agent_name: {dimension: [scores_per_prompt]}}
    """
    result: dict[str, dict[str, list[float]]] = {}

    for agent_name in agents:
        traces_dir = output_dir / "scoring-traces" / agent_name
        if not traces_dir.exists():
            logger.error("No scoring traces for %s at %s", agent_name, traces_dir)
            continue

        dim_scores: dict[str, list[float]] = {d: [] for d in DIMENSIONS}
        composites: list[float] = []

        # Find all scoring trace files
        trace_files = sorted(traces_dir.rglob("scoring-trace.json"))
        for trace_path in trace_files:
            trace = json.loads(trace_path.read_text(encoding="utf-8"))
            dims = trace.get("dimension_scores", {})
            for dim_name in DIMENSIONS:
                if dim_name in dims:
                    dim_scores[dim_name].append(dims[dim_name])
            composites.append(trace.get("composite_score", 0.0))

        dim_scores["composite"] = composites
        result[agent_name] = dim_scores
        logger.info(
            "%s: loaded %d prompts with %d dimensions",
            agent_name,
            len(composites),
            len(DIMENSIONS),
        )

    return result


def run_phase4_validation(
    agents: list[str],
    output_dir: Path,
) -> dict:
    """Run Phase 4 in validation mode using Phase 2 data.

    Since Phase 3 hasn't populated BaselineStore, this mode:
    1. Loads Phase 2 per-dimension scores
    2. Runs Wilcoxon signed-rank test (if N >= 20, otherwise documents insufficiency)
    3. Computes Wilson score CIs for pass rates
    4. Produces the statistical report

    For validation, baseline = candidate (self-comparison with small perturbation
    to avoid all-zero differences that defeat Wilcoxon).
    """
    from jerry.testing.stats import (
        MIN_STATISTICAL_SAMPLE_SIZE,
        QUALITY_PASS_THRESHOLD,
    )

    phase2_scores = load_phase2_dimension_scores(output_dir, agents)

    all_agent_results = {}

    for agent_name in agents:
        agent_scores = phase2_scores.get(agent_name, {})
        if not agent_scores:
            all_agent_results[agent_name] = {"error": "No Phase 2 scores found"}
            continue

        n_prompts = len(agent_scores.get("composite", []))
        agent_results = {
            "n_prompts": n_prompts,
            "n_minimum_required": MIN_STATISTICAL_SAMPLE_SIZE,
            "sufficient_n": n_prompts >= MIN_STATISTICAL_SAMPLE_SIZE,
            "dimensions": {},
        }

        for dim_name, scores in agent_scores.items():
            if not scores:
                continue

            n = len(scores)
            mean_score = sum(scores) / n
            pass_count = sum(1 for s in scores if s >= QUALITY_PASS_THRESHOLD)
            pass_rate = pass_count / n

            dim_result = {
                "n": n,
                "mean": round(mean_score, 4),
                "min": round(min(scores), 4),
                "max": round(max(scores), 4),
                "std": round(_std(scores), 4) if n > 1 else 0.0,
                "pass_count": pass_count,
                "pass_rate": round(pass_rate, 4),
                "quality_threshold": QUALITY_PASS_THRESHOLD,
                "scores": [round(s, 4) for s in scores],
            }

            # Compute Wilson CI if possible
            if n >= 1:
                try:
                    wilson = _compute_wilson_ci(pass_count, n)
                    dim_result["wilson_ci"] = wilson
                except Exception as e:
                    dim_result["wilson_ci_error"] = str(e)

            # Wilcoxon requires N >= 20 (can't do self-comparison anyway)
            if n < MIN_STATISTICAL_SAMPLE_SIZE:
                dim_result["wilcoxon"] = {
                    "status": "INSUFFICIENT_N",
                    "note": f"N={n} < {MIN_STATISTICAL_SAMPLE_SIZE}. "
                    "Wilcoxon requires Phase 3 data (N>=20).",
                }
            else:
                dim_result["wilcoxon"] = {
                    "status": "DEFERRED",
                    "note": "Self-comparison is not meaningful. "
                    "Requires Phase 3 baseline data for real comparison.",
                }

            # Classification
            if n < MIN_STATISTICAL_SAMPLE_SIZE:
                dim_result["classification"] = "INSUFFICIENT_DATA"
                dim_result["merge_decision"] = "DEFERRED"
            elif mean_score >= QUALITY_PASS_THRESHOLD:
                dim_result["classification"] = "NO_REGRESSION"
                dim_result["merge_decision"] = "ALLOW"
            else:
                dim_result["classification"] = "QUALITY_FLOOR_BREACH"
                dim_result["merge_decision"] = "BLOCK"

            agent_results["dimensions"][dim_name] = dim_result

        # Overall verdict
        classifications = [d["classification"] for d in agent_results["dimensions"].values()]
        if "QUALITY_FLOOR_BREACH" in classifications:
            agent_results["overall_classification"] = "QUALITY_FLOOR_BREACH"
            agent_results["overall_merge_decision"] = "BLOCK"
        elif "REGRESSION" in classifications:
            agent_results["overall_classification"] = "REGRESSION"
            agent_results["overall_merge_decision"] = "BLOCK"
        elif "MARGINAL" in classifications:
            agent_results["overall_classification"] = "MARGINAL"
            agent_results["overall_merge_decision"] = "ALLOW_WITH_WARNING"
        elif all(c == "INSUFFICIENT_DATA" for c in classifications):
            agent_results["overall_classification"] = "INSUFFICIENT_DATA"
            agent_results["overall_merge_decision"] = "DEFERRED"
        else:
            agent_results["overall_classification"] = "NO_REGRESSION"
            agent_results["overall_merge_decision"] = "ALLOW"

        all_agent_results[agent_name] = agent_results

    return all_agent_results


def run_phase4_full(
    agents: list[str],
    output_dir: Path,
    phase3_path: Path,
) -> dict:
    """Run Phase 4 with real Phase 3 MR data.

    Loads original and MR variant scores from Phase 3, then:
    1. Runs Wilcoxon signed-rank test on paired (original, MR-variant) scores
    2. Applies Bonferroni correction (k=2: MR-001 + MR-003)
    3. Computes Wilson score CIs for pass rates
    4. Classifies: NO_REGRESSION / MARGINAL / REGRESSION per MR relation
    """
    from scipy.stats import wilcoxon as scipy_wilcoxon

    from jerry.testing.stats import (
        MIN_STATISTICAL_SAMPLE_SIZE,
        QUALITY_PASS_THRESHOLD,
    )

    phase3_data = json.loads(phase3_path.read_text(encoding="utf-8"))
    phase3_agents = phase3_data.get("agents", {})

    # Bonferroni correction: k=2 tests (MR-001 + MR-003)
    bonferroni_k = 2
    alpha_family = 0.05
    alpha_corrected = alpha_family / bonferroni_k
    marginal_alpha = 0.10 / bonferroni_k

    all_agent_results = {}

    for agent_name in agents:
        agent_p3 = phase3_agents.get(agent_name)
        if not agent_p3:
            all_agent_results[agent_name] = {"error": "No Phase 3 data for this agent"}
            continue

        original_scores = agent_p3.get("original_scores", [])
        mr001_scores = agent_p3.get("mr001_scores", [])
        mr003_scores = agent_p3.get("mr003_scores", [])
        n = len(original_scores)

        agent_results = {
            "n_paired_observations": n,
            "n_minimum_required": MIN_STATISTICAL_SAMPLE_SIZE,
            "sufficient_n": n >= MIN_STATISTICAL_SAMPLE_SIZE,
            "bonferroni_k": bonferroni_k,
            "alpha_corrected": round(alpha_corrected, 6),
            "comparisons": {},
        }

        # Test MR-001: original vs paraphrase variant
        for mr_label, mr_scores in [("MR-001", mr001_scores), ("MR-003", mr003_scores)]:
            n_mr = min(n, len(mr_scores))
            if n_mr == 0:
                agent_results["comparisons"][mr_label] = {
                    "error": f"No {mr_label} scores available",
                }
                continue

            orig_paired = original_scores[:n_mr]
            mr_paired = mr_scores[:n_mr]

            mean_orig = sum(orig_paired) / n_mr
            mean_mr = sum(mr_paired) / n_mr
            mean_delta = mean_mr - mean_orig

            pass_count_orig = sum(1 for s in orig_paired if s >= QUALITY_PASS_THRESHOLD)
            pass_count_mr = sum(1 for s in mr_paired if s >= QUALITY_PASS_THRESHOLD)

            comp_result: dict = {
                "n": n_mr,
                "mean_original": round(mean_orig, 4),
                "mean_variant": round(mean_mr, 4),
                "mean_delta": round(mean_delta, 4),
                "std_original": round(_std(orig_paired), 4),
                "std_variant": round(_std(mr_paired), 4),
                "pass_rate_original": round(pass_count_orig / n_mr, 4),
                "pass_rate_variant": round(pass_count_mr / n_mr, 4),
                "quality_threshold": QUALITY_PASS_THRESHOLD,
            }

            # Wilson CI for original pass rate
            try:
                comp_result["wilson_ci_original"] = _compute_wilson_ci(
                    pass_count_orig,
                    n_mr,
                )
            except Exception as e:
                comp_result["wilson_ci_original_error"] = str(e)

            # Wilson CI for variant pass rate
            try:
                comp_result["wilson_ci_variant"] = _compute_wilson_ci(
                    pass_count_mr,
                    n_mr,
                )
            except Exception as e:
                comp_result["wilson_ci_variant_error"] = str(e)

            # Wilcoxon signed-rank test
            if n_mr < MIN_STATISTICAL_SAMPLE_SIZE:
                comp_result["wilcoxon"] = {
                    "status": "INSUFFICIENT_N",
                    "note": f"N={n_mr} < {MIN_STATISTICAL_SAMPLE_SIZE}.",
                }
                comp_result["classification"] = "INSUFFICIENT_DATA"
                comp_result["merge_decision"] = "DEFERRED"
            else:
                # Check if all differences are zero (Wilcoxon can't handle this)
                diffs = [m - o for o, m in zip(orig_paired, mr_paired, strict=False)]
                nonzero_diffs = [d for d in diffs if d != 0.0]

                if len(nonzero_diffs) == 0:
                    comp_result["wilcoxon"] = {
                        "status": "ALL_ZEROS",
                        "note": "All paired differences are zero. No quality change detected.",
                    }
                    comp_result["classification"] = "NO_REGRESSION"
                    comp_result["merge_decision"] = "ALLOW"
                else:
                    try:
                        stat, p_value = scipy_wilcoxon(
                            orig_paired,
                            mr_paired,
                            alternative="two-sided",
                        )
                        comp_result["wilcoxon"] = {
                            "status": "COMPUTED",
                            "statistic": round(float(stat), 4),
                            "p_value": round(float(p_value), 6),
                            "alpha_corrected": round(alpha_corrected, 6),
                            "significant": float(p_value) < alpha_corrected,
                            "marginal": (alpha_corrected <= float(p_value) < marginal_alpha),
                        }

                        # Classification
                        if float(p_value) < alpha_corrected and mean_delta < 0:
                            comp_result["classification"] = "REGRESSION"
                            comp_result["merge_decision"] = "BLOCK"
                        elif float(p_value) < alpha_corrected and mean_delta >= 0:
                            comp_result["classification"] = "IMPROVEMENT"
                            comp_result["merge_decision"] = "ALLOW"
                        elif alpha_corrected <= float(p_value) < marginal_alpha:
                            comp_result["classification"] = "MARGINAL"
                            comp_result["merge_decision"] = "ALLOW_WITH_WARNING"
                        else:
                            comp_result["classification"] = "NO_REGRESSION"
                            comp_result["merge_decision"] = "ALLOW"
                    except Exception as e:
                        comp_result["wilcoxon"] = {
                            "status": "ERROR",
                            "error": str(e),
                        }
                        comp_result["classification"] = "ERROR"
                        comp_result["merge_decision"] = "DEFERRED"

            agent_results["comparisons"][mr_label] = comp_result

        # Overall verdict across MR comparisons
        classifications = [
            c.get("classification", "UNKNOWN")
            for c in agent_results["comparisons"].values()
            if "classification" in c
        ]
        if "REGRESSION" in classifications:
            agent_results["overall_classification"] = "REGRESSION"
            agent_results["overall_merge_decision"] = "BLOCK"
        elif "MARGINAL" in classifications:
            agent_results["overall_classification"] = "MARGINAL"
            agent_results["overall_merge_decision"] = "ALLOW_WITH_WARNING"
        elif all(c == "INSUFFICIENT_DATA" for c in classifications):
            agent_results["overall_classification"] = "INSUFFICIENT_DATA"
            agent_results["overall_merge_decision"] = "DEFERRED"
        elif "ERROR" in classifications:
            agent_results["overall_classification"] = "ERROR"
            agent_results["overall_merge_decision"] = "DEFERRED"
        else:
            agent_results["overall_classification"] = "NO_REGRESSION"
            agent_results["overall_merge_decision"] = "ALLOW"

        # Include Phase 3 MR evaluation results for reference
        mr001_p3 = agent_p3.get("mr_001", {})
        mr003_p3 = agent_p3.get("mr_003", {})
        agent_results["phase3_mr_results"] = {
            "mr_001": mr001_p3,
            "mr_003": mr003_p3,
        }

        all_agent_results[agent_name] = agent_results
        logger.info(
            "%s: %s (%s) | N=%d | MR-001: %s | MR-003: %s",
            agent_name,
            agent_results["overall_classification"],
            agent_results["overall_merge_decision"],
            n,
            agent_results["comparisons"]
            .get("MR-001", {})
            .get(
                "classification",
                "?",
            ),
            agent_results["comparisons"]
            .get("MR-003", {})
            .get(
                "classification",
                "?",
            ),
        )

    return all_agent_results


def _std(scores: list[float]) -> float:
    """Sample standard deviation (Bessel-corrected)."""
    n = len(scores)
    if n < 2:
        return 0.0
    mean = sum(scores) / n
    variance = sum((s - mean) ** 2 for s in scores) / (n - 1)
    return variance**0.5


def _compute_wilson_ci(
    pass_count: int,
    n: int,
    alpha: float = 0.05,
) -> dict:
    """Compute Wilson score confidence interval for pass rate."""
    from statsmodels.stats.proportion import proportion_confint

    ci_lower, ci_upper = proportion_confint(
        count=pass_count,
        nobs=n,
        alpha=alpha,
        method="wilson",
    )
    pass_rate = pass_count / n if n > 0 else 0.0
    return {
        "pass_rate": round(pass_rate, 4),
        "ci_lower": round(ci_lower, 4),
        "ci_upper": round(ci_upper, 4),
        "ci_width": round(ci_upper - ci_lower, 4),
        "n": n,
        "pass_count": pass_count,
        "alpha": alpha,
        "method": "wilson",
    }


def generate_markdown_report(
    results: dict,
    output_dir: Path,
    validation_mode: bool,
) -> str:
    """Generate Phase 4 statistical report in markdown."""
    lines = [
        "# Phase 4 — Statistical Comparison Report",
        "",
        f"> **Generated:** {datetime.now(UTC).isoformat()}",
        f"> **Mode:** {'Pipeline Validation (Phase 2 self-analysis)' if validation_mode else 'Full Comparison'}",
        "",
    ]

    if validation_mode:
        lines.extend(
            [
                "## Validation Mode Notice",
                "",
                "This report uses Phase 2 scoring data for pipeline validation. ",
                "Phase 3 MR testing has not yet completed, so real baseline data ",
                "is not available for Wilcoxon signed-rank comparison. The statistics ",
                "below are descriptive only — not regression verdicts.",
                "",
                "**To run full Phase 4:** Complete Phase 3 (`baseline_mr_runner.py`), ",
                "then re-run this script without `--validation-mode`.",
                "",
            ]
        )

    for agent_name, agent_data in results["agents"].items():
        if "error" in agent_data:
            lines.extend([f"## {agent_name}", "", f"**Error:** {agent_data['error']}", ""])
            continue

        overall = agent_data.get("overall_classification", "UNKNOWN")
        merge = agent_data.get("overall_merge_decision", "UNKNOWN")

        lines.extend(
            [
                f"## {agent_name}",
                "",
                f"**Overall:** {overall} | **Merge:** {merge} | "
                f"**N:** {agent_data.get('n_prompts', 0)} prompts",
                "",
                "| Dimension | N | Mean | Min | Max | Std | Pass Rate | Wilson CI | Classification |",
                "|-----------|---|------|-----|-----|-----|-----------|----------|----------------|",
            ]
        )

        for dim_name, dim_data in agent_data.get("dimensions", {}).items():
            wilson = dim_data.get("wilson_ci", {})
            ci_str = (
                f"[{wilson.get('ci_lower', '?')}, {wilson.get('ci_upper', '?')}]"
                if wilson
                else "N/A"
            )
            lines.append(
                f"| {dim_name} | {dim_data['n']} | {dim_data['mean']} | "
                f"{dim_data['min']} | {dim_data['max']} | {dim_data['std']} | "
                f"{dim_data['pass_rate']} | {ci_str} | {dim_data['classification']} |"
            )

        lines.extend(
            [
                "",
                "### Wilcoxon Status",
                "",
            ]
        )

        for dim_name, dim_data in agent_data.get("dimensions", {}).items():
            wilcoxon = dim_data.get("wilcoxon", {})
            lines.append(
                f"- **{dim_name}:** {wilcoxon.get('status', 'UNKNOWN')} — "
                f"{wilcoxon.get('note', '')}"
            )

        lines.append("")

    # Bonferroni note
    lines.extend(
        [
            "## Bonferroni Correction",
            "",
            "When Phase 3 data is available, Bonferroni correction will be applied with:",
            "- k = 6 dimensions (or k = 13 for full suite including MRs)",
            "- alpha_family = 0.05",
            f"- alpha_per_test = 0.05 / 6 = {0.05 / 6:.4f} (6-dimension) or 0.05 / 13 = {0.05 / 13:.4f} (full suite)",
            "",
            "## Interpretation Guidance",
            "",
            "| Verdict | Meaning | Action |",
            "|---------|---------|--------|",
            "| NO_REGRESSION | No statistically significant quality decrease | Safe to merge |",
            "| MARGINAL | Borderline result | Review dimension drivers before merging |",
            "| REGRESSION | Significant quality decrease detected | Block merge; investigate |",
            "| QUALITY_FLOOR_BREACH | Mean score below 0.92 threshold | Block merge; quality too low |",
            "| INSUFFICIENT_DATA | N < 20 for Wilcoxon | Run Phase 3 to collect more data |",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    """CLI entry point for Phase 4 statistical comparison."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Phase 4 statistical comparison for PROJ-036.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--agents", required=True)
    parser.add_argument(
        "--validation-mode",
        action="store_true",
        help="Use Phase 2 data for pipeline validation (no Phase 3 required).",
    )
    parser.add_argument("--verify-only", action="store_true")

    args = parser.parse_args()

    repo_root = Path(__file__).parents[1]
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = repo_root / output_dir

    agents = [a.strip() for a in args.agents.split(",")]

    if args.verify_only:
        stats_path = output_dir / "phase4-stats.json"
        report_path = output_dir / "phase4-statistical-report.md"
        failures = []
        if not stats_path.exists():
            failures.append(f"MISSING: {stats_path}")
        if not report_path.exists():
            failures.append(f"MISSING: {report_path}")
        if stats_path.exists():
            stats = json.loads(stats_path.read_text(encoding="utf-8"))
            for agent_name in agents:
                if agent_name not in stats.get("agents", {}):
                    failures.append(f"MISSING agent {agent_name} in stats")
        if failures:
            logger.error("Verification FAILED with %d issue(s):", len(failures))
            for f in failures:
                logger.error("  - %s", f)
            return 1
        logger.info("Phase 4 verification PASSED.")
        return 0

    # Run statistical analysis
    if args.validation_mode:
        logger.info("Running in VALIDATION MODE (Phase 2 self-analysis)")
        agent_results = run_phase4_validation(agents, output_dir)
    else:
        # Try to load Phase 3 MR results for real Wilcoxon comparison
        phase3_path = output_dir / "phase3-mr-results.json"
        if phase3_path.exists():
            logger.info("Loading Phase 3 MR results from %s", phase3_path)
            agent_results = run_phase4_full(agents, output_dir, phase3_path)
        else:
            logger.warning(
                "No Phase 3 results found at %s. Falling back to validation mode.",
                phase3_path,
            )
            agent_results = run_phase4_validation(agents, output_dir)
            args.validation_mode = True

    # Persist stats JSON
    results = {
        "agents": agent_results,
        "validation_mode": args.validation_mode,
        "timestamp": datetime.now(UTC).isoformat(),
    }
    stats_path = output_dir / "phase4-stats.json"
    stats_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    logger.info("Stats: %s", stats_path)

    # Generate markdown report
    report = generate_markdown_report(results, output_dir, args.validation_mode)
    report_path = output_dir / "phase4-statistical-report.md"
    report_path.write_text(report, encoding="utf-8")
    logger.info("Report: %s", report_path)

    # Summary
    for agent_name, agent_data in agent_results.items():
        if "error" in agent_data:
            logger.info("%s: %s", agent_name, agent_data["error"])
        else:
            logger.info(
                "%s: %s (%s) | N=%d",
                agent_name,
                agent_data.get("overall_classification", "?"),
                agent_data.get("overall_merge_decision", "?"),
                agent_data.get("n_prompts", 0),
            )

    logger.info("Phase 4 COMPLETE.")
    return 0


if __name__ == "__main__":
    import sys  # noqa: PLC0415

    sys.exit(main())
