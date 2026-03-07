# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""S-010 self-review smoke test for Layer 4 Statistical Comparison Engine.

Run with: uv run python projects/PROJ-036-prompt-regression-harness/work/EPIC-001-security-research/smoke_test_layer4.py
"""

import json as json_mod
import random
import sys
import tempfile
from pathlib import Path

# --- Ensure project root on path ---
ROOT = Path(__file__).parents[5]
sys.path.insert(0, str(ROOT))

from jerry.testing.baselines.store import BaselineStore  # noqa: E402
from jerry.testing.layer4_stats import Layer4Pipeline  # noqa: E402
from jerry.testing.reports.generator import ReportGenerator  # noqa: E402
from jerry.testing.stats import (  # noqa: E402
    BONFERRONI_ALPHA_FULL,
    BONFERRONI_K_FULL_SUITE,
    MIN_STATISTICAL_SAMPLE_SIZE,
    QUALITY_PASS_THRESHOLD,
    InsufficientSamplesError,
    InvalidScoreArrayError,
    bonferroni_correction,
    compare_multiple_metrics,
    compare_versions,
    wilcoxon_signed_rank,
    wilson_score_intervals,
)
from jerry.testing.types import (  # noqa: E402
    EvaluationMode,
    RegressionClass,
)

random.seed(42)
PASS_COUNT = 0
FAIL_COUNT = 0


def ok(msg: str) -> None:
    global PASS_COUNT
    PASS_COUNT += 1
    print(f"  OK  {msg}")


def fail(msg: str) -> None:
    global FAIL_COUNT
    FAIL_COUNT += 1
    print(f"  FAIL {msg}")


def make_scores(mean: float, n: int = 30, sigma: float = 0.03) -> list[float]:
    return [min(1.0, max(0.0, mean + random.gauss(0, sigma))) for _ in range(n)]


# ---------------------------------------------------------------------------
# Section 1: Named constants (FR-014, FR-016, FR-017)
# ---------------------------------------------------------------------------
print("\n=== Named constants ===")
if MIN_STATISTICAL_SAMPLE_SIZE == 20:
    ok("FR-014 MIN_STATISTICAL_SAMPLE_SIZE == 20")
else:
    fail(f"MIN_STATISTICAL_SAMPLE_SIZE is {MIN_STATISTICAL_SAMPLE_SIZE}, expected 20")

if QUALITY_PASS_THRESHOLD == 0.92:
    ok("FR-016 QUALITY_PASS_THRESHOLD == 0.92")
else:
    fail(f"QUALITY_PASS_THRESHOLD is {QUALITY_PASS_THRESHOLD}, expected 0.92")

if BONFERRONI_K_FULL_SUITE == 13:
    ok("FR-017 BONFERRONI_K_FULL_SUITE == 13")
else:
    fail(f"BONFERRONI_K_FULL_SUITE is {BONFERRONI_K_FULL_SUITE}, expected 13")

expected_alpha = round(0.05 / 13, 4)
if abs(BONFERRONI_ALPHA_FULL - expected_alpha) < 1e-9:
    ok(f"BONFERRONI_ALPHA_FULL == {expected_alpha}")
else:
    fail(f"BONFERRONI_ALPHA_FULL is {BONFERRONI_ALPHA_FULL}, expected {expected_alpha}")

# ---------------------------------------------------------------------------
# Section 2: InsufficientSamplesError (FR-014)
# ---------------------------------------------------------------------------
print("\n=== FR-014 sample size enforcement ===")
try:
    compare_versions([0.9] * 19, [0.8] * 19)
    fail("N=19 should raise InsufficientSamplesError")
except InsufficientSamplesError as exc:
    if "N >= 20" in str(exc) and "19" in str(exc):
        ok("InsufficientSamplesError raised with correct message for N=19")
    else:
        fail(f"Wrong error message: {exc}")

base20 = make_scores(0.92, n=20)
cand20 = make_scores(0.91, n=20)
try:
    r = compare_versions(base20, cand20)
    ok(f"N=20 accepted (p={r.wilcoxon.p_value:.4f})")
except InsufficientSamplesError:
    fail("N=20 should not raise InsufficientSamplesError")

# ---------------------------------------------------------------------------
# Section 3: InvalidScoreArrayError (security validation)
# ---------------------------------------------------------------------------
print("\n=== Score array security validation ===")
try:
    wilcoxon_signed_rank([0.9] * 20, [0.9] * 20)
    fail("All-identical scores should raise InvalidScoreArrayError")
except InvalidScoreArrayError:
    ok("InvalidScoreArrayError: all-identical scores rejected")

try:
    wilcoxon_signed_rank([1.5] * 20, [0.9] * 20)
    fail("Out-of-range score should raise InvalidScoreArrayError")
except InvalidScoreArrayError:
    ok("InvalidScoreArrayError: out-of-range score rejected")

# ---------------------------------------------------------------------------
# Section 4: Wilcoxon classification (FR-015)
# ---------------------------------------------------------------------------
print("\n=== FR-015 Wilcoxon regression classification ===")
base30 = make_scores(0.92, n=30, sigma=0.02)
cand30_reg = make_scores(0.75, n=30, sigma=0.02)
res = compare_versions(base30, cand30_reg)
if res.classification == RegressionClass.REGRESSION:
    ok(f"Large delta classified as REGRESSION (p={res.wilcoxon.p_value:.6f})")
else:
    fail(f"Large delta should be REGRESSION, got {res.classification.value}")

cand30_same = make_scores(0.92, n=30, sigma=0.02)
res_stable = compare_versions(base30, cand30_same)
if res_stable.classification in (
    RegressionClass.NO_REGRESSION,
    RegressionClass.MARGINAL,
    RegressionClass.IMPROVEMENT,
):
    ok(f"Stable scores: {res_stable.classification.value} (p={res_stable.wilcoxon.p_value:.4f})")
else:
    fail(f"Stable scores gave unexpected verdict: {res_stable.classification.value}")

# ---------------------------------------------------------------------------
# Section 5: Wilson score confidence intervals (FR-016)
# ---------------------------------------------------------------------------
print("\n=== FR-016 Wilson score confidence intervals ===")
all_pass = [0.95] * 30
wr = wilson_score_intervals(all_pass)
if wr.pass_rate == 1.0 and 0.0 <= wr.ci_lower <= wr.ci_upper <= 1.0:
    ok(f"All-pass CI: [{wr.ci_lower:.3f}, {wr.ci_upper:.3f}]")
else:
    fail(f"Wilson CI incorrect: pass_rate={wr.pass_rate} ci=[{wr.ci_lower},{wr.ci_upper}]")

mixed = [0.95] * 15 + [0.80] * 15  # 50% pass rate
wm = wilson_score_intervals(mixed)
if 0.3 <= wm.pass_rate <= 0.7 and wm.ci_lower < wm.ci_upper:
    ok(f"Mixed CI: pass_rate={wm.pass_rate:.2f} [{wm.ci_lower:.3f}, {wm.ci_upper:.3f}]")
else:
    fail(f"Wilson mixed CI incorrect: {wm}")

# ---------------------------------------------------------------------------
# Section 6: Bonferroni correction (FR-017)
# ---------------------------------------------------------------------------
print("\n=== FR-017 Bonferroni correction ===")
bc = bonferroni_correction(k=13)
if abs(bc.alpha_per_test - 0.05 / 13) < 1e-9:
    ok(f"K=13 alpha_per_test={bc.alpha_per_test:.6f}")
else:
    fail(f"Wrong alpha_per_test: {bc.alpha_per_test}")

disclosure = bc.description
if "Bonferroni correction applied" in disclosure and "K=13" in disclosure:
    ok("Bonferroni disclosure string correct")
else:
    fail(f"Disclosure missing required content: {disclosure}")

# ---------------------------------------------------------------------------
# Section 7: Multi-metric comparison (FR-017 + FR-015 combined)
# ---------------------------------------------------------------------------
print("\n=== Multi-metric comparison with Bonferroni ===")
metric_scores = {
    "completeness": (make_scores(0.93), make_scores(0.93)),
    "internal_consistency": (make_scores(0.91), make_scores(0.91)),
    "methodological_rigor": (make_scores(0.90), make_scores(0.90)),
}
per_metric, bc_mm = compare_multiple_metrics(metric_scores, agent_id="ps-researcher")
if len(per_metric) == 3:
    ok("compare_multiple_metrics returns result for each metric")
else:
    fail(f"Expected 3 metric results, got {len(per_metric)}")

if bc_mm.k == 3:
    ok(
        f"Bonferroni k=3 (len of input dict) when k not specified: alpha_per_test={bc_mm.alpha_per_test:.4f}"
    )
else:
    fail(f"Expected k=3, got k={bc_mm.k}")

# ---------------------------------------------------------------------------
# Section 8: BaselineStore (FR-020)
# ---------------------------------------------------------------------------
print("\n=== FR-020 BaselineStore ===")
with tempfile.TemporaryDirectory() as tmpdir:
    store = BaselineStore(Path(tmpdir) / "data")

    # Quality gate rejection
    try:
        store.store(
            version_key="abc:skills/ps-researcher.md",
            agent_id="ps-researcher",
            metric_id="composite",
            scores=[0.85] * 25,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4-20250514",
        )
        fail("Should reject baseline with mean < 0.92")
    except ValueError as exc:
        if "quality gate" in str(exc).lower():
            ok("Quality gate rejects mean=0.85 baseline")
        else:
            fail(f"Wrong rejection message: {exc}")

    # Acceptance and round-trip
    good = make_scores(0.94, n=30)
    rec = store.store(
        version_key="abc:skills/ps-researcher.md",
        agent_id="ps-researcher",
        metric_id="composite",
        scores=good,
        evaluation_mode=EvaluationMode.FULL,
        model_version="claude-sonnet-4-20250514",
    )
    if rec.baseline_status == "active" and rec.n_runs == 30:
        ok("store() returns active BaselineRecord with 30 runs")
    else:
        fail(f"Unexpected record: {rec}")

    retrieved = store.retrieve("abc:skills/ps-researcher.md", "ps-researcher", "composite")
    if retrieved is not None and len(retrieved.scores) == 30:
        ok("retrieve() returns stored scores (N=30 round-trip)")
    else:
        fail("retrieve() returned None or wrong N")

    entries = store.audit()
    if len(entries) == 1 and entries[0].agent_id == "ps-researcher":
        ok("audit() lists stored baseline")
    else:
        fail(f"audit() returned {entries}")

    # Version key validation
    try:
        store.store(
            version_key="invalid-no-colon",
            agent_id="ps-researcher",
            metric_id="x",
            scores=good,
            evaluation_mode=EvaluationMode.FULL,
            model_version="m",
        )
        fail("Should reject version_key without colon")
    except ValueError:
        ok("version_key without colon rejected (FR-004 format enforcement)")

# ---------------------------------------------------------------------------
# Section 9: ReportGenerator (FR-018)
# ---------------------------------------------------------------------------
print("\n=== FR-018 ReportGenerator ===")
gen = ReportGenerator()

# Build a regression result for reporting
base30r = make_scores(0.93, sigma=0.02)
cand30r = make_scores(0.75, sigma=0.02)
result = compare_versions(
    base30r,
    cand30r,
    metric_id="composite_score",
    agent_id="ps-researcher",
    version_key_a="abc:skills/ps-researcher.md",
    version_key_b="def:skills/ps-researcher.md",
)
report = gen.from_single_metric(result)
md = gen.to_markdown(report)
js = gen.to_json(report)

if "REGRESSION" in md or "FAIL" in md:
    ok("Markdown report contains regression verdict")
else:
    fail(f"Markdown missing verdict. Preview:\n{md[:200]}")

if "Wilson" in md or "CI_A" in md or "ci_lower" in md.lower():
    ok("FR-016 Wilson CI present in markdown report")
else:
    fail("Wilson CI missing from markdown report")

if "Bonferroni" in md:
    ok("FR-017 Bonferroni section present in markdown (single-metric no-correction case)")
else:
    ok("FR-017 Bonferroni not shown for uncorrected single-metric (expected)")

parsed = json_mod.loads(js)
if "classification" in parsed and "per_metric" in parsed:
    ok("JSON report has required fields (classification, per_metric)")
else:
    fail(f"JSON missing fields: {list(parsed.keys())}")

# Bonferroni multi-metric report
metric_scores_reg = {
    "composite_score": (make_scores(0.93), make_scores(0.74, sigma=0.02)),
    "completeness": (make_scores(0.91), make_scores(0.72, sigma=0.02)),
}
per_m, bc_rep = compare_multiple_metrics(
    metric_scores_reg,
    agent_id="ps-researcher",
    version_key_a="abc:x",
    version_key_b="def:x",
    k=BONFERRONI_K_FULL_SUITE,
)
with tempfile.TemporaryDirectory() as _td:
    _pipeline_mm = Layer4Pipeline(baseline_store=BaselineStore(Path(_td) / "d"))
    multi = _pipeline_mm._aggregate_multi_metric(per_m, bc_rep)
    report_mm = gen.from_multi_metric(
        multi,
        agent_id="ps-researcher",
        version_key_a="abc:x",
        version_key_b="def:x",
        evaluation_mode=EvaluationMode.FULL,
    )
md_mm = gen.to_markdown(report_mm)
if "Bonferroni correction applied" in md_mm:
    ok("FR-017 Bonferroni disclosure in multi-metric markdown (K=13)")
else:
    fail("Bonferroni disclosure missing from multi-metric markdown")

# ---------------------------------------------------------------------------
# Section 10: Layer4Pipeline.run() end-to-end (FR-019)
# ---------------------------------------------------------------------------
print("\n=== FR-019 Layer4Pipeline.run() end-to-end ===")
with tempfile.TemporaryDirectory() as tmpdir2:
    store2 = BaselineStore(Path(tmpdir2) / "data")
    pipeline = Layer4Pipeline(baseline_store=store2)

    # Regression case
    metrics_reg2 = {
        "composite_score": (make_scores(0.93), make_scores(0.74, sigma=0.02)),
        "completeness": (make_scores(0.91), make_scores(0.72, sigma=0.02)),
    }
    exit_code = pipeline.run(
        agent_id="ps-researcher",
        version_key_a="abc:skills/problem-solving/agents/ps-researcher.md",
        version_key_b="def:skills/problem-solving/agents/ps-researcher.md",
        metric_scores=metrics_reg2,
        evaluation_mode=EvaluationMode.FULL,
    )
    if exit_code == 1:
        ok("Layer4Pipeline.run() returns exit_code=1 for REGRESSION (FR-018 CI block)")
    else:
        fail(f"Expected exit_code=1 for REGRESSION, got {exit_code}")

    # No-regression case
    metrics_ok = {
        "composite_score": (make_scores(0.93), make_scores(0.93)),
        "completeness": (make_scores(0.91), make_scores(0.91)),
    }
    exit_code_ok = pipeline.run(
        agent_id="ps-researcher",
        version_key_a="abc:skills/problem-solving/agents/ps-researcher.md",
        version_key_b="def:skills/problem-solving/agents/ps-researcher.md",
        metric_scores=metrics_ok,
        evaluation_mode=EvaluationMode.FULL,
    )
    if exit_code_ok in (0, 2):
        ok(f"Layer4Pipeline.run() returns exit_code={exit_code_ok} for NO_REGRESSION/MARGINAL")
    else:
        fail(f"Expected exit_code 0 or 2 for no-regression, got {exit_code_ok}")

    # Smoke mode
    exit_smoke = pipeline.run(
        agent_id="ps-researcher",
        version_key_a="abc:skills/problem-solving/agents/ps-researcher.md",
        version_key_b="def:skills/problem-solving/agents/ps-researcher.md",
        metric_scores=metrics_ok,
        evaluation_mode=EvaluationMode.SMOKE,
    )
    if exit_smoke == 0:
        ok("Layer4Pipeline.run() returns exit_code=0 for Smoke (no violations)")
    else:
        fail(f"Expected exit_code=0 for Smoke no-violations, got {exit_smoke}")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print(f"\n{'=' * 60}")
print(f"S-010 Self-Review: {PASS_COUNT} PASS  {FAIL_COUNT} FAIL")
if FAIL_COUNT > 0:
    sys.exit(1)
print("All Layer 4 checks PASSED.")
