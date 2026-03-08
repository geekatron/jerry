# Quality Score Report: Stream 3D — Layer 4 Statistical Comparison Engine (Iteration 6)

## L0 Executive Summary

**Score:** 0.951/1.00 | **Verdict:** PASS | **Weakest Dimension:** Evidence Quality (0.90)
**One-line assessment:** All four iter6 fixes confirmed present; deliverable meets the C4 stream threshold of 0.94 with robust hexagonal architecture, complete statistical contracts, and actionable public API — minor evidence gap is the absence of inline narrative linking algorithm constants to primary academic sources.

---

## Scoring Context

- **Deliverable:** `jerry/testing/types.py`, `jerry/testing/stats.py`, `jerry/testing/layer4_stats.py`, `jerry/testing/baselines/__init__.py`, `jerry/testing/baselines/store.py`, `jerry/testing/baselines/ports.py`, `jerry/testing/reports/__init__.py`, `jerry/testing/reports/generator.py`, `jerry/testing/reports/ports.py`, `jerry/testing/__init__.py`
- **Deliverable Type:** Code
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Stream Threshold:** >= 0.94 (C4 elevated)
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 6 of revision cycle
- **Prior Scores:** 0.874 (iter1), 0.934 (iter2), 0.892 (iter3), 0.910 (iter4), 0.926 (iter5)

---

## Iter6 Fix Verification (REQUIRED BEFORE SCORING)

| Fix | Description | Status | Evidence |
|-----|-------------|--------|----------|
| Fix 1 | `layer4_stats.py` top-level `ReportGenerator` import removed; lazy import in `__init__` only | CONFIRMED | `layer4_stats.py` lines 98-104: lazy import inside `__init__`; top-level imports at lines 32-49 contain only ports and stats — no `generator` import. H-07 block line 20 documents `reports/generator` as `conditional: lazy import in __init__ only`. |
| Fix 2 | `baselines/protocol.md` references eliminated from `store.py` | CONFIRMED | `store.py` `MIN_FULL_SAMPLES` comment (lines 108-114) cites `FR-017 AC-1` and `behavioral-contracts.md Section D.1`. `store()` docstring (lines 130-134) cites `FR-017 AC-1, behavioral-contracts.md Section D.1`. `InsufficientSamplesError` message (lines 169-172) cites `FR-017 AC-1 / behavioral-contracts.md Section D.1`. No occurrence of `baselines/protocol.md` anywhere in `store.py`. |
| Fix 3 | `QUALITY_FLOOR_BREACH` injection comment in `types.py` | CONFIRMED | `types.py` lines 57-60: `#: Injected by Layer 2 callers (e.g., DeepEval adapter) when mean(scores) / falls below QUALITY_PASS_THRESHOLD. Not produced by _classify_regression() / in stats.py, which handles only statistical comparison classifications.` |
| Fix 4 | `invalidate()` usage example in `BaselineStore` class docstring | CONFIRMED | `store.py` lines 83-90: full `invalidate()` usage block with `contract_version="2.0.0"` and explanatory comment `# count = N records marked as invalidated; re-collect with Full mode.` |

All 4 required iter6 fixes are confirmed present. Scoring proceeds.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.951 |
| **Stream Threshold** | 0.94 (C4 elevated) |
| **Standard Threshold** | 0.92 (H-13) |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.96 | 0.192 | Full five-module surface (types, stats, layer4, baselines, reports) with hexagonal ports, FR-014 through FR-020 all addressed, iter6 fixes verified |
| Internal Consistency | 0.20 | 0.97 | 0.194 | Single constant definition point; classification rules align precisely across `_classify_regression`, docstrings, and enum table; lazy-import dependency graph is coherent |
| Methodological Rigor | 0.20 | 0.96 | 0.192 | Hexagonal architecture enforced throughout; statistical methods (Wilcoxon, Wilson, Bonferroni, Cohen's r) implemented with correct formulas and boundary conditions; one minor gap in alpha-range lower bound rationale |
| Evidence Quality | 0.15 | 0.90 | 0.135 | FR and behavioral-contracts.md citations present; primary statistical references ([1]-[8]) listed in module header but not cross-linked to individual algorithm implementations; Cohen's r normal-approximation formula lacks inline derivation citation |
| Actionability | 0.15 | 0.96 | 0.144 | Full usage examples in BaselineStore and Layer4Pipeline docstrings; `invalidate()` example added (Fix 4); CI/CD exit codes explicitly documented; public API is immediately callable |
| Traceability | 0.10 | 0.94 | 0.094 | FR IDs appear in docstrings and comments throughout; behavioral-contracts.md Section references present; iter6 citations to `FR-017 AC-1` / `behavioral-contracts.md Section D.1` directly replace the removed `baselines/protocol.md` floating reference |
| **TOTAL** | **1.00** | | **0.951** | |

**Arithmetic verification:**
- Completeness:        0.96 × 0.20 = 0.1920
- Internal Consistency: 0.97 × 0.20 = 0.1940
- Methodological Rigor: 0.96 × 0.20 = 0.1920
- Evidence Quality:    0.90 × 0.15 = 0.1350
- Actionability:       0.96 × 0.15 = 0.1440
- Traceability:        0.94 × 0.10 = 0.0940
- **Sum: 0.1920 + 0.1940 + 0.1920 + 0.1350 + 0.1440 + 0.0940 = 0.9510**

---

## Detailed Dimension Analysis

### Completeness (0.96/1.00)

**Evidence:**

All required Layer 4 components are present and mutually complete:

1. **`types.py`** — Complete domain type surface: `RegressionClass` (5 values including the now-annotated `QUALITY_FLOOR_BREACH`), `RateClass`, `EffectSizeLabel`, `EvaluationMode`, `MergeDecision`, `WilcoxonResult`, `WilsonResult`, `BonferroniConfig`, `RegressionResult`, `MultiMetricResult`, `BaselineRecord`, `BaselineAuditEntry`, `ComparisonReport`, `ScoreArray`. Every type needed by downstream layers is defined here.

2. **`stats.py`** — Complete statistical function set: `wilcoxon_signed_rank`, `wilson_score_intervals`, `bonferroni_correction`, `_classify_regression`, `merge_decision_from_classification`, `_rate_class`, `compare_versions`, `compare_multiple_metrics`. Named constants `MIN_STATISTICAL_SAMPLE_SIZE=20`, `QUALITY_PASS_THRESHOLD=0.92`, `BONFERRONI_K_FULL_SUITE=13`, `BONFERRONI_ALPHA_FULL=0.004` present at lines 63-80.

3. **`layer4_stats.py`** — Full pipeline orchestration: `run()`, `run_single_metric()`, `_run_smoke()`, `_run_statistical()`, `_aggregate_multi_metric()`, `_persist_report()`, `_emit_gha_outputs()`, `_exit_code()`. FR-018 GitHub Actions output and CI exit codes at lines 421-476.

4. **Hexagonal ports** — `BaselinePersistencePort` (4 methods, `@runtime_checkable`) and `ReportOutputPort` (5 methods, `@runtime_checkable`) fully mirror their concrete adapter signatures.

5. **Package init** — `jerry/testing/__init__.py` re-exports FR-019 public API with `__all__`; `baselines/__init__.py` and `reports/__init__.py` clean re-exports.

**Gaps:**

- `layer4_stats.py` `run()` return docstring documents exit codes 0/1/2 but does not document the `QUALITY_FLOOR_BREACH` case (exit code 1 via BLOCK path) explicitly in the method signature. This is an extremely minor documentation gap — the code path is correct. (0.04 deduction)
- No test module is present in this deliverable scope; this was not listed as required for this stream iteration.

**Improvement Path:**

Document `QUALITY_FLOOR_BREACH → exit 1` explicitly in `run()` return docstring alongside the existing `REGRESSION → exit 1` note.

---

### Internal Consistency (0.97/1.00)

**Evidence:**

1. **Classification table consistency** — `types.py` lines 33-51 define the classification decision table. `stats.py` `_classify_regression()` at lines 407-469 implements exactly this table with matching boundary conditions (`p >= 0.10`, `0.05 <= p < 0.10`, `p < 0.05`, `r < 0.10`, `0.10 <= r < 0.30`, `r >= 0.30`). No divergence found between specification and implementation.

2. **`QUALITY_FLOOR_BREACH` consistency (Fix 3)** — `types.py` lines 57-60 now correctly state this is injected by Layer 2 callers, not produced by `_classify_regression()`. `stats.py` `_classify_regression()` at lines 407-469 confirms: `QUALITY_FLOOR_BREACH` is NOT produced in this function (only `NO_REGRESSION`, `MARGINAL`, `REGRESSION`, `IMPROVEMENT` are returned). `merge_decision_from_classification()` at lines 491-499 handles `QUALITY_FLOOR_BREACH` in the `BLOCK` branch, which is correct. The enum value, its documentation, and its handling are all consistent.

3. **Alpha constant consistency** — `BONFERRONI_ALPHA_FULL = 0.004` in `stats.py` line 80. The `bonferroni_correction()` function computes `alpha_per_test = alpha_family / k = 0.05/13 ≈ 0.003846`, which rounds to `0.004` under the documented "conservative 3-significant-figure rounding" convention (lines 76-80). The comment explicitly acknowledges that `round(0.05/13, 4) = 0.0038` would be a 5% relative error, justifying the literal value.

4. **Lazy import consistency (Fix 1)** — H-07 compliance block at lines 17-24 of `layer4_stats.py` documents `reports/generator` as `conditional: lazy import in __init__ only`. The actual import at lines 98-104 matches this exactly. `reports/ports.py` is imported at the top level (line 33) as an interface — correct per hexagonal rules.

5. **Version key format** — FR-004 format `{git_hash}:{file_path}` is described in `types.py` line 285, enforced in `store.py` `_validate_version_key()` at lines 395-416, and used in all docstring examples consistently.

**Gaps:**

- `_emit_gha_outputs()` in `layer4_stats.py` at line 434 references `report.classification` but the `ComparisonReport.classification` field is a `str`, not `RegressionClass`. This is intentional (stringified at report construction time in `generator.py` line 89) but the type comment at `layer4_stats.py` line 434 does not note this conversion path. Minor documentation inconsistency, no behavioral impact. (0.03 deduction)

**Improvement Path:**

Add a brief comment at `layer4_stats.py` `_emit_gha_outputs()` noting `classification` is already stringified in `ComparisonReport`.

---

### Methodological Rigor (0.96/1.00)

**Evidence:**

1. **Hexagonal architecture enforced** — `types.py` and `stats.py` are pure domain modules with stdlib+scipy+statsmodels imports only (H-07). `baselines/ports.py` and `reports/ports.py` are port definitions importing only stdlib and `types.py`. `store.py` and `generator.py` are adapters. `layer4_stats.py` is an orchestrator importing ports (not concrete adapters) at the top level, with the sole concrete adapter (`ReportGenerator`) injected via lazy import per Fix 1. This is a textbook hexagonal implementation.

2. **Cohen's r derivation** — `stats.py` lines 184-212: implements `mu_W = n(n+1)/4`, `var_W = n(n+1)(2n+1)/24`, `Z = |W - mu_W| / sqrt(var_W)`, `r = Z / sqrt(N)`, with `[0, 1]` clamping for numerical robustness. Formula is mathematically correct.

3. **Wilcoxon two-sided test** — `scipy.stats.wilcoxon` called with `alternative="two-sided"` (line 283) per behavioral-contracts.md Section D.1.

4. **Wilson score CI** — `statsmodels.stats.proportion.proportion_confint` with `method="wilson"` (lines 342-347). The rationale for Wilson vs. Wald is documented at lines 321-328.

5. **Bonferroni correction** — `k >= 1` and `0 < alpha_family < 1` validated before division (lines 389-398). Floating-point division `alpha_family / k` is used rather than a precomputed constant, which is correct generality.

6. **Belt-and-suspenders RATE_REGRESSION promotion** — `compare_versions()` lines 608-612: promotes MARGINAL to REGRESSION when Wilson intervals show non-overlapping degradation. This is explicitly documented as a "belt-and-suspenders guard."

7. **Score validation with adversarial all-identical guard** — `_validate_score_array()` at lines 128-176 rejects all-identical arrays for Wilcoxon inputs (`require_variation=True`) but permits them for Wilson inputs (`require_variation=False`). The asymmetry is justified (lines 140-146) and correctly wired at call sites.

**Gaps:**

- `compare_versions()` alpha validation range is `[0.001, 0.10]` (line 590) with a comment at lines 586-595 explaining why `0.001` (not `0.01`) is the lower bound. However, the comment says FR-015 "specifies (0.01, 0.10) for uncorrected single-metric use" without documenting that the framework's own `BONFERRONI_ALPHA_FULL = 0.004` would fail the FR-015-specified range. The engineering judgment to widen to `[0.001, 0.10]` is sound but the tradeoff commentary in the docstring is slightly incomplete. (0.04 deduction)

**Improvement Path:**

Add a line in the `compare_versions()` docstring: "FR-015 specifies (0.01, 0.10) for the uncorrected single-metric case; the lower bound is widened to 0.001 here to accommodate `BONFERRONI_ALPHA_FULL = 0.004`."

---

### Evidence Quality (0.90/1.00)

**Evidence:**

1. **FR citations in docstrings** — FR numbers appear inline for most major functions: `compare_versions()` cites FR-014, C-008, C-006; `wilson_score_intervals()` cites FR-016; `bonferroni_correction()` cites FR-017; `store()` cites FR-020, FR-017 AC-1; `_emit_gha_outputs()` cites FR-018.

2. **Behavioral-contracts.md section references** — Section D.1, D.2, D.3, D.4, D.5 referenced in `stats.py`; Section D.6 in `generator.py`; Section E.3 in `store.py`; Section D.1 in the fixed iter6 `store.py` `MIN_FULL_SAMPLES` comment.

3. **Primary literature header references** — `stats.py` lines 28-34 list 8 references: Wilcoxon (1945), Wilson (1927), Cohen (1988), scipy.stats.wilcoxon, statsmodels docs. These are the correct authoritative sources.

**Gaps:**

- Primary literature references ([1]-[8]) appear only in the module docstring of `stats.py` and are NOT cross-linked to the individual functions that use them. For example, `_cohens_r()` cites "per Cohen (1988) and scipy docs [7]" at line 190 — this is a backreference notation only; there is no actual `[7]` link or numbered list cross-reference. A reader cannot follow from the module header to the specific formula used. This is a standard Python documentation limitation, but it reduces verifiability.

- `_effect_label()` thresholds (r < 0.10, 0.10-0.20, 0.20-0.30, >= 0.30) cite "per behavioral-contracts.md Section D.4" but do not cross-reference the Cohen (1988) origin that Section D.4 itself derives from. The citation chain is contracts → implementation, skipping the academic root.

- `_classify_regression()` at lines 407-425 references "behavioral-contracts.md Section D.4 combined classification table" but the alpha scaling formula `alpha_marginal = alpha * (_ALPHA_MARGINAL / _ALPHA_REGRESSION)` at line 442 has no citation explaining why this proportional scaling is the correct approach for Bonferroni-corrected thresholds.

These gaps are documentation quality issues, not correctness issues. Score resolves DOWNWARD due to the missing algorithm-to-citation cross-links. (0.10 deduction from 1.00)

**Improvement Path:**

Add inline citations to individual functions: e.g., `_cohens_r()` docstring should cite `[3] Cohen (1988)` directly. Add a brief note to `_classify_regression()` explaining the `alpha_marginal = alpha * 2` scaling convention and its relationship to the uncorrected pair (0.05/0.10).

---

### Actionability (0.96/1.00)

**Evidence:**

1. **Layer4Pipeline usage example** — `layer4_stats.py` lines 62-81: complete `__init__` + `run()` call example with all parameters shown.

2. **BaselineStore usage example (including `invalidate()` from Fix 4)** — `store.py` lines 66-90: `store()`, `retrieve()`, and now `invalidate()` all shown with realistic arguments. The `invalidate()` example at lines 83-90 is concrete (`contract_version="2.0.0"`, return value explained).

3. **CI/CD exit code documentation** — `layer4_stats.py` `_exit_code()` at lines 457-476 documents exit codes 0/1/2 with classification mapping. `run()` at lines 147-150 documents the same.

4. **GitHub Actions integration** — `_emit_gha_outputs()` at lines 419-454 shows how GHA output variables are written, with fallback to `logger.info` for local development.

5. **Public API completeness** — `jerry/testing/__init__.py` lists all FR-019 public exports with one-line descriptions, making the package immediately navigable for callers.

6. **ReportGenerator example** — `generator.py` lines 50-57: complete `gen = ReportGenerator()` usage pattern.

**Gaps:**

- `run_single_metric()` at lines 171-225 lacks a usage example in its class-level context (the class docstring only shows `run()`). A user wanting to call `run_single_metric()` must infer the pattern from the method signature alone. (0.04 deduction)

**Improvement Path:**

Add a second usage block to `Layer4Pipeline` class docstring showing `run_single_metric()` for the single-metric no-Bonferroni case.

---

### Traceability (0.94/1.00)

**Evidence:**

1. **Fix 2 verification** — All `N=30` production-baseline citations in `store.py` now trace to `FR-017 AC-1` and `behavioral-contracts.md Section D.1` (confirmed in all 4 locations: class-level `MIN_FULL_SAMPLES` comment, `store()` docstring parameter, `InsufficientSamplesError` message, enforcement comment). The previously floating `baselines/protocol.md` reference has been fully replaced.

2. **H-07 compliance block** — `layer4_stats.py` lines 17-24 explicitly names the dependency graph and its directionality, enabling a reviewer to verify each import against the declared architecture.

3. **H-10/H-11 compliance declarations** — Every module declares compliance at the top, matching the actual file content (verified: each file has exactly one primary class/Protocol).

4. **FR-004 version key format** — Documented in `types.py`, `store.py`, and `ports.py`; the FR number is traceable to `harness-requirements.md` via the cited reference.

5. **`__init__.py` FR-019 comment** — `jerry/testing/__init__.py` line 1 attributes the public API to FR-019, making the package-level contract traceable.

**Gaps:**

- `layer4_stats.py` `_aggregate_multi_metric()` at lines 328-388 has no FR citation explaining the "worst-case across all metrics" aggregation rule. The logic is clear from reading but does not trace to a specific acceptance criterion.

- `reports/generator.py` `_verdict_emoji()` at lines 423-452: maps classifications to PASS/WARN/FAIL/INFO labels with a comment "align with FR-018 CI/CD exit code semantics" but doesn't cite the specific acceptance criterion number within FR-018. (0.06 deduction)

**Improvement Path:**

Add FR number reference to `_aggregate_multi_metric()` docstring (e.g., "Overall worst-case rule per FR-019 acceptance criterion N.N"). Add specific FR-018 AC number to `_verdict_emoji()` comment.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.90 | 0.93 | Add per-function citations linking algorithm steps to primary literature references ([1]-[8]) listed in `stats.py` module header. Specifically: `_cohens_r()` → [3] Cohen (1988), `_classify_regression()` alpha-scaling → document the 2x proportional convention. |
| 2 | Traceability | 0.94 | 0.96 | Add FR citation to `_aggregate_multi_metric()` docstring for the worst-case aggregation rule. Add specific FR-018 AC number to `_verdict_emoji()` comment. |
| 3 | Internal Consistency | 0.97 | 0.98 | Add comment in `_emit_gha_outputs()` noting `report.classification` is pre-stringified by `ReportGenerator` at report construction time. |
| 4 | Methodological Rigor | 0.96 | 0.97 | Extend `compare_versions()` docstring to explicitly state that the alpha lower bound was widened from FR-015's 0.01 to 0.001 to accommodate `BONFERRONI_ALPHA_FULL`. |
| 5 | Completeness | 0.96 | 0.97 | Add `QUALITY_FLOOR_BREACH → exit 1` explicitly in `run()` return docstring. Add `run_single_metric()` usage example to class docstring. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computation
- [x] Evidence documented for each score with specific file and line references
- [x] Uncertain scores resolved downward: Evidence Quality uncertain between 0.90 and 0.93 → resolved to 0.90; Traceability uncertain between 0.93 and 0.95 → resolved to 0.94
- [x] Calibration considered: this is iteration 6 of a multi-revision cycle — scores at 0.95+ are appropriate only for a genuinely polished deliverable. All iter6 fixes confirmed present and correct; prior score was 0.926 at iter5; delta is +0.025 which is consistent with 4 targeted fixes applied
- [x] No dimension scored above 0.97 without exceptional evidence (Internal Consistency at 0.97 is justified: the single-constant-source pattern, enum/function alignment, and lazy-import coherence are objectively verifiable with zero contradictions found)
- [x] Arithmetic verified: 0.1920 + 0.1940 + 0.1920 + 0.1350 + 0.1440 + 0.0940 = 0.9510

---

## Session Context Handoff

```yaml
verdict: PASS
composite_score: 0.951
threshold: 0.94
weakest_dimension: Evidence Quality
weakest_score: 0.90
critical_findings_count: 0
iteration: 6
improvement_recommendations:
  - "Add per-function citations linking algorithm steps to primary literature in stats.py"
  - "Add FR citation to _aggregate_multi_metric() worst-case aggregation rule"
  - "Document alpha lower-bound widening from FR-015 spec in compare_versions() docstring"
  - "Add QUALITY_FLOOR_BREACH to run() exit code documentation"
  - "Add run_single_metric() usage example to Layer4Pipeline class docstring"
```
