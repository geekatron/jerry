"""Layer 4 implementation verification script.

Verifies FR-014, FR-015, FR-016, FR-017, FR-020, C-006, C-008,
and the report generator against the behavioral contracts.

Run: uv run python projects/PROJ-036-prompt-regression-harness/work/verify_layer4.py
"""

import json as json_mod
import random
import sys
import tempfile
from pathlib import Path

# --- Add project root to path ---
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from jerry.testing.baselines.store import BaselineStore
from jerry.testing.reports.generator import ReportGenerator
from jerry.testing.stats import (
    BONFERRONI_ALPHA_FULL,
    BONFERRONI_K_FULL_SUITE,
    MIN_STATISTICAL_SAMPLE_SIZE,
    QUALITY_PASS_THRESHOLD,
    InsufficientSamplesError,
    bonferroni_correction,
    compare_multiple_metrics,
    compare_versions,
    wilson_score_intervals,
)
from jerry.testing.types import (
    EvaluationMode,
    MergeDecision,
    RegressionClass,
)

PASS = "PASS"
FAIL = "FAIL"
results: list[tuple[str, str]] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    status = PASS if condition else FAIL
    results.append((label, status))
    tag = "[PASS]" if condition else "[FAIL]"
    suffix = f"  {detail}" if detail else ""
    print(f"  {tag} {label}{suffix}")


def make_scores(mean_val: float, n: int, seed: int = 1, sigma: float = 0.04) -> list[float]:
    rng = random.Random(seed)
    return [min(1.0, max(0.0, mean_val + rng.gauss(0, sigma))) for _ in range(n)]


print("=" * 60)
print("Layer 4 Statistical Engine Verification")
print("=" * 60)
print()

# ---------------------------------------------------------------
# Constants (FR-014, FR-016, FR-017)
# ---------------------------------------------------------------
print("1. Named constants")
check("MIN_STATISTICAL_SAMPLE_SIZE == 20", MIN_STATISTICAL_SAMPLE_SIZE == 20)
check("QUALITY_PASS_THRESHOLD == 0.92", QUALITY_PASS_THRESHOLD == 0.92)
check("BONFERRONI_K_FULL_SUITE == 13", BONFERRONI_K_FULL_SUITE == 13)
check(
    "BONFERRONI_ALPHA_FULL == 0.05/13 (4 dp)",
    abs(BONFERRONI_ALPHA_FULL - round(0.05 / 13, 4)) < 1e-9,
    f"got {BONFERRONI_ALPHA_FULL}",
)
print()

# ---------------------------------------------------------------
# FR-014: N >= 20 enforcement (C-008)
# ---------------------------------------------------------------
print("2. FR-014 / C-008: N >= 20 enforcement")
try:
    compare_versions([0.9] * 19, [0.8] * 19)
    check("N=19 raises InsufficientSamplesError", False)
except InsufficientSamplesError as exc:
    msg = str(exc)
    check("N=19 raises InsufficientSamplesError", True)
    check("Error message contains 'N >= 20'", "N >= 20" in msg, msg[:80])
    check("Error message contains '19, 19'", "19, 19" in msg)
    check("Error message mentions Smoke mode", "Smoke mode" in msg)

# N=20 must succeed
sa = make_scores(0.88, 20, seed=10)
sb = make_scores(0.88, 20, seed=11)
try:
    r = compare_versions(sa, sb)
    check("N=20 accepted without error", True, f"cls={r.classification.value}")
except InsufficientSamplesError:
    check("N=20 accepted without error", False)
print()

# ---------------------------------------------------------------
# FR-015: Wilcoxon signed-rank comparison fields
# ---------------------------------------------------------------
print("3. FR-015: Wilcoxon signed-rank result fields")
sa30 = make_scores(0.87, 30, seed=1)
sb30 = make_scores(0.87, 30, seed=2)
result = compare_versions(
    sa30,
    sb30,
    metric_id="composite_score",
    agent_id="ps-researcher",
    version_key_a="abc1234:skills/ps-researcher.md",
    version_key_b="def5678:skills/ps-researcher.md",
    evaluation_mode=EvaluationMode.FULL,
)
check(
    "result.classification is RegressionClass", isinstance(result.classification, RegressionClass)
)
check(
    "result.wilcoxon.p_value in [0,1]",
    0.0 <= result.wilcoxon.p_value <= 1.0,
    f"p={result.wilcoxon.p_value:.4f}",
)
check(
    "result.wilcoxon.cohens_r in [0,1]",
    0.0 <= result.wilcoxon.cohens_r <= 1.0,
    f"r={result.wilcoxon.cohens_r:.4f}",
)
check("result.wilcoxon.statistic >= 0", result.wilcoxon.statistic >= 0)
check("result.wilcoxon.mean_a is float", isinstance(result.wilcoxon.mean_a, float))
check("result.wilcoxon.mean_b is float", isinstance(result.wilcoxon.mean_b, float))
check(
    "result.wilcoxon.mean_delta == mean_b - mean_a",
    abs(result.wilcoxon.mean_delta - (result.wilcoxon.mean_b - result.wilcoxon.mean_a)) < 1e-9,
)
check(
    "result has wilson_a and wilson_b", hasattr(result, "wilson_a") and hasattr(result, "wilson_b")
)
check("RegressionResult.n_a == 30", result.n_a == 30)
check("RegressionResult.n_b == 30", result.n_b == 30)
check("result.metric_id == 'composite_score'", result.metric_id == "composite_score")
check("result.agent_id == 'ps-researcher'", result.agent_id == "ps-researcher")
print()

# ---------------------------------------------------------------
# FR-016: Wilson score intervals
# ---------------------------------------------------------------
print("4. FR-016: Wilson score confidence intervals")
high_scores = make_scores(0.95, 30, seed=5, sigma=0.02)
wi = wilson_score_intervals(high_scores)
check("WilsonResult.ci_lower <= ci_upper", wi.ci_lower <= wi.ci_upper)
check("WilsonResult.ci_lower >= 0", wi.ci_lower >= 0.0)
check("WilsonResult.ci_upper <= 1", wi.ci_upper <= 1.0)
check("WilsonResult.n_total == 30", wi.n_total == 30)
check("WilsonResult.n_pass >= 0", wi.n_pass >= 0)
check("WilsonResult.pass_rate in [0,1]", 0.0 <= wi.pass_rate <= 1.0)
check(
    "WilsonResult.ci_width == ci_upper - ci_lower",
    abs(wi.ci_width - (wi.ci_upper - wi.ci_lower)) < 1e-9,
)
# RegressionResult includes CI in both versions
check("result.wilson_a.ci_lower >= 0", result.wilson_a.ci_lower >= 0.0)
check("result.wilson_b.ci_lower >= 0", result.wilson_b.ci_lower >= 0.0)
print()

# ---------------------------------------------------------------
# FR-017: Bonferroni correction (k=13)
# ---------------------------------------------------------------
print("5. FR-017: Bonferroni correction")
bc13 = bonferroni_correction(k=13)
check("bc13.k == 13", bc13.k == 13)
check("bc13.alpha_family == 0.05", bc13.alpha_family == 0.05)
check(
    "bc13.alpha_per_test == 0.05/13",
    abs(bc13.alpha_per_test - 0.05 / 13) < 1e-12,
    f"got {bc13.alpha_per_test:.8f}",
)
check(
    "description contains 'Bonferroni correction applied'",
    "Bonferroni correction applied" in bc13.description,
)
check("description contains 'K=13'", "K=13" in bc13.description)
check("description contains 'per-metric threshold'", "per-metric threshold" in bc13.description)

bc1 = bonferroni_correction(k=1)
check("k=1: alpha_per_test == 0.05", abs(bc1.alpha_per_test - 0.05) < 1e-12)

bc6 = bonferroni_correction(k=6)
check(
    "k=6: alpha_per_test == 0.05/6",
    abs(bc6.alpha_per_test - 0.05 / 6) < 1e-12,
    f"got {bc6.alpha_per_test:.6f}",
)
print()

# ---------------------------------------------------------------
# C-006: Regression detection via Wilcoxon (not point estimate)
# ---------------------------------------------------------------
print("6. C-006: Regression detection")
high = make_scores(0.90, 30, seed=99, sigma=0.03)
# Force a strong regression: shift all scores down by 0.12
low = [max(0.0, s - 0.12) for s in high]
reg_result = compare_versions(high, low, metric_id="completeness")
check(
    "Clear regression detected",
    reg_result.classification == RegressionClass.REGRESSION,
    f"cls={reg_result.classification.value}  p={reg_result.wilcoxon.p_value:.6f}",
)
check("Regression => BLOCK merge", reg_result.merge_decision == MergeDecision.BLOCK)

# No regression with identical distributions
same_a = make_scores(0.88, 30, seed=7)
same_b = make_scores(0.88, 30, seed=8)
stable_result = compare_versions(same_a, same_b)
check(
    "Similar distributions => not REGRESSION",
    stable_result.classification != RegressionClass.REGRESSION,
    f"cls={stable_result.classification.value}",
)
print()

# ---------------------------------------------------------------
# Multi-metric with Bonferroni
# ---------------------------------------------------------------
print("7. compare_multiple_metrics")
metrics = {
    "completeness": (make_scores(0.87, 30, seed=1), make_scores(0.87, 30, seed=2)),
    "consistency": (make_scores(0.88, 30, seed=3), make_scores(0.88, 30, seed=4)),
    "rigor": (make_scores(0.86, 30, seed=5), make_scores(0.86, 30, seed=6)),
}
per_metric, bc = compare_multiple_metrics(
    metrics,
    agent_id="ps-researcher",
    version_key_a="abc:skills/ps-researcher.md",
    version_key_b="def:skills/ps-researcher.md",
    k=BONFERRONI_K_FULL_SUITE,
)
check("per_metric has 3 entries", len(per_metric) == 3)
check("BonferroniConfig.k == 13", bc.k == 13)
check(
    "All per_metric results have bonferroni set",
    all(r.bonferroni is not None for r in per_metric.values()),
)
check(
    "All per_metric alpha == bc.alpha_per_test",
    all(abs(r.alpha - bc.alpha_per_test) < 1e-12 for r in per_metric.values()),
)
print()

# ---------------------------------------------------------------
# FR-020: BaselineStore quality gate
# ---------------------------------------------------------------
print("8. FR-020: BaselineStore quality gate")
with tempfile.TemporaryDirectory() as tmp:
    store = BaselineStore(Path(tmp))

    # Accept baseline with mean >= 0.92
    good = make_scores(0.94, 30, seed=20, sigma=0.02)
    rec = store.store(
        version_key="abc1234:skills/ps-researcher.md",
        agent_id="ps-researcher",
        metric_id="composite_score",
        scores=good,
        evaluation_mode=EvaluationMode.FULL,
        model_version="claude-sonnet-4-20250514",
    )
    check(
        "Good baseline accepted (mean >= 0.92)",
        rec.mean_score >= 0.92,
        f"mean={rec.mean_score:.4f}",
    )
    check("Stored record has correct agent_id", rec.agent_id == "ps-researcher")
    check("Stored record has n_runs=30", rec.n_runs == 30)
    check("baseline_status == 'active'", rec.baseline_status == "active")

    # FR-004: version_key format validated
    try:
        store.store(
            version_key="no-colon-here",
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=good,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4-20250514",
        )
        check("Invalid version_key raises ValueError", False)
    except ValueError:
        check("Invalid version_key raises ValueError", True)

    # Reject baseline with mean < 0.92
    bad = make_scores(0.80, 30, seed=21, sigma=0.03)
    try:
        store.store(
            version_key="bad123:skills/ps-researcher.md",
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=bad,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4-20250514",
        )
        check("Low-quality baseline rejected", False)
    except ValueError as exc:
        check("Low-quality baseline rejected", True, str(exc)[:60])

    # Audit
    entries = store.audit()
    check("audit returns list", isinstance(entries, list))
    check("audit has 1 entry (only good baseline stored)", len(entries) == 1)
    check("audit entry has version_key", entries[0].version_key != "")
    check("audit entry has mean_score", entries[0].mean_score > 0.0)
    check("audit entry has age_days", entries[0].age_days >= 0.0)

print()

# ---------------------------------------------------------------
# ReportGenerator
# ---------------------------------------------------------------
print("9. ReportGenerator")
gen = ReportGenerator()
report = gen.from_single_metric(result)
check("ComparisonReport.agent == 'ps-researcher'", report.agent == "ps-researcher")
check("ComparisonReport.classification is str", isinstance(report.classification, str))
check("ComparisonReport.merge_recommendation is str", isinstance(report.merge_recommendation, str))
check("ComparisonReport.narrative is str", isinstance(report.narrative, str))
check("ComparisonReport.per_metric_results non-empty", len(report.per_metric_results) > 0)

md = gen.to_markdown(report)
check("Markdown output is non-empty string", isinstance(md, str) and len(md) > 100)
check("Markdown contains agent name", "ps-researcher" in md)
check("Markdown contains classification", report.classification in md)

js = gen.to_json(report)
parsed = json_mod.loads(js)
check("JSON output parses correctly", isinstance(parsed, dict))
check("JSON has 'evaluation_mode' field", "evaluation_mode" in parsed)
check("JSON has 'classification' field", "classification" in parsed)
check("JSON has 'merge_recommendation' field", "merge_recommendation" in parsed)
check("JSON has 'per_metric' field", "per_metric" in parsed)
check("JSON has 'narrative' field", "narrative" in parsed)

# FR-018: REGRESSION verdict
regression_report = gen.from_single_metric(reg_result)
check(
    "REGRESSION report has BLOCK merge",
    regression_report.merge_recommendation == MergeDecision.BLOCK.value,
)
print()

# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------
print("=" * 60)
total = len(results)
passed = sum(1 for _, s in results if s == PASS)
failed = sum(1 for _, s in results if s == FAIL)
print(f"Results: {passed}/{total} passed, {failed} failed")
if failed:
    print("FAILED checks:")
    for label, status in results:
        if status == FAIL:
            print(f"  - {label}")
    sys.exit(1)
else:
    print("All checks: PASS")
    sys.exit(0)
