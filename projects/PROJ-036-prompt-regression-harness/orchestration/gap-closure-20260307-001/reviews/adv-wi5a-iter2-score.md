# Quality Score Report: WI5-A Unit Test Suite (tests/prompt-regression/unit/) — Iteration 2

## L0 Executive Summary

**Score:** 0.872/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Methodological Rigor (0.82)
**One-line assessment:** The `pytestmark` marker gap is fully closed and CG references are meaningfully improved, but BDD naming was applied selectively (only enum-value tests renamed) leaving the majority of behavioral test methods still non-BDD, and the `_VALID_VERSION_KEY` 7-char hash discrepancy remains unresolved.

---

## Scoring Context

- **Deliverable:** `tests/prompt-regression/unit/` (6 targeted files: test_baselines.py, test_types.py, test_debiasing.py, test_metamorphic_base.py, test_stats.py, test_version_keys.py)
- **Deliverable Type:** Code (unit test suite for prompt regression harness)
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.836 (iteration 1)
- **Scored:** 2026-03-07T12:00:00Z
- **Iteration:** 2 (re-score after FIX-WI5-A)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.872 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |
| **Delta from Iteration 1** | +0.036 |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.91 | 0.182 | pytestmark fix confirmed in all 6 files; CG-002, CG-005, CG-027 added; behavioral-contracts.md full path added |
| Internal Consistency | 0.20 | 0.88 | 0.176 | Logic unchanged and still consistent; naming style cohort split remains but is reduced |
| Methodological Rigor | 0.20 | 0.82 | 0.164 | BDD _should_ adoption is partial: 0% in test_baselines.py/test_debiasing.py, 8% in test_stats.py, 13% in test_metamorphic_base.py |
| Evidence Quality | 0.15 | 0.90 | 0.135 | CG references substantively improved across all 6 files; behavioral-contracts.md path now fully qualified |
| Actionability | 0.15 | 0.87 | 0.131 | Marker fix resolves pytest -m unit gap; BDD naming and _VALID_VERSION_KEY discrepancy remain concrete open items |
| Traceability | 0.10 | 0.84 | 0.084 | Markers now present (machine-queryable); CG IDs added; FR IDs in class docstrings still thin in test_stats.py and test_debiasing.py |
| **TOTAL** | **1.00** | | **0.872** | |

---

## Detailed Dimension Analysis

### Completeness (0.91/1.00)

**Evidence:**

The two highest-priority completeness gaps from iteration 1 are confirmed closed:

1. `pytestmark = [pytest.mark.unit]` is present at module level in all 6 targeted files:
   - test_baselines.py line 36: `pytestmark = [pytest.mark.unit]`
   - test_types.py line 27: `pytestmark = [pytest.mark.unit]`
   - test_debiasing.py line 25: `pytestmark = [pytest.mark.unit]`
   - test_metamorphic_base.py line 30: `pytestmark = [pytest.mark.unit]`
   - test_stats.py line 30: `pytestmark = [pytest.mark.unit]`
   - test_version_keys.py line 32: `pytestmark = [pytest.mark.unit]`

2. CG reference additions confirmed:
   - test_baselines.py (lines 21-27): Added CG-002 and CG-027 to module docstring references block, with inline comment on line 61: "A valid version key: 7+ lowercase hex chars, colon, non-empty path (CG-027)"
   - test_types.py (line 15): Added CG-005 to references block
   - test_stats.py (line 18): Added CG-001 to references block
   - test_version_keys.py (line 21): Added CG-027 to references block
   - test_debiasing.py (lines 17-18): Added full repo-relative path for behavioral-contracts.md
   - test_metamorphic_base.py (lines 18-19): Added full repo-relative path for behavioral-contracts.md

**Gaps:**

- The `_VALID_VERSION_KEY = "abc1234:skills/ps-researcher.md"` constant in test_baselines.py (line 62) remains a 7-character abbreviated hash. The iteration 2 fix added the CG-027 comment explaining this is a relaxed BaselineStore format, which partially resolves the discrepancy. However, the constant itself is unchanged from iteration 1 — the comment explains the divergence but does not close it. The prior score report (Priority 4 recommendation) asked for an explanatory comment, which is now present, so this item is partially resolved.
- The conftest.py `evaluator` fixture contract test (Priority 5 recommendation from iteration 1) was not added. This remains a completeness gap: no test verifies `EvaluationConfigError` is raised on missing `ANTHROPIC_API_KEY`.

**Improvement Path:**

Add a `test_evaluator_fixture_raises_on_missing_api_key` test in conftest.py or a dedicated fixture test file using `monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)`. This is a low-effort, high-value addition for the remaining completeness gap.

---

### Internal Consistency (0.88/1.00)

**Evidence:**

No logical contradictions have been introduced. The QUALITY_PASS_THRESHOLD = 0.92 alignment across test_stats.py, test_metrics.py, and test_layer2_evaluation.py is preserved. The `EvaluationMode` cross-validation in test_version_keys.py::TestEvaluationModeVersionKeys.test_local_enum_members_match_canonical_types is intact and still passes (confirmed by reading the logic: it imports both local and canonical EvaluationMode and asserts name/value identity).

The naming style cohort division is reduced by iteration 2: test_types.py now has BDD naming applied to ~43% of its methods (all enum-value checks), which is a meaningful improvement. However, the two cohorts (BDD vs. descriptive) now exist within individual files rather than just between files, which is a minor regression in internal consistency — within test_types.py, `test_smoke_value_should_equal_smoke_string` sits next to `test_evaluation_mode_is_str_enum` (no `_should_`), `test_all_six_members_present` (no `_should_`), `test_wilcoxon_result_frozen` (no `_should_`). This creates within-file style inconsistency that was not present in iteration 1 (where all 6 files had uniform descriptive style).

**Gaps:**

- Within-file BDD/non-BDD mixing in test_types.py, test_metamorphic_base.py, test_version_keys.py, and test_stats.py creates an inconsistency that did not exist before the partial rename. In iteration 1, the 6 files had consistent descriptive naming; in iteration 2, they have mixed naming with no clear pattern for which tests got renamed and which did not.
- The duplicated `DebiasingStrategy.reset_rng()` test between test_debiasing.py and test_layer2_evaluation.py (iteration 1 Priority 6 recommendation) was not consolidated.

**Improvement Path:**

Complete the BDD rename uniformly within each file, or revert the partial renames to restore within-file consistency. Complete-rename is preferred per CG-020.

---

### Methodological Rigor (0.82/1.00)

**Evidence:**

The fix description states "Renamed test methods to BDD-style `test_X_should_Y` naming convention." The evidence does not support this claim broadly. Actual BDD adoption rates by file:

- **test_stats.py**: 4 of ~52 methods use `_should_` (TestNamedConstants only — lines 89, 93, 97, 101). The 48 remaining behavioral tests (TestCompareVersionsNoRegression, TestCompareVersionsRegression, TestCompareVersionsImprovement, TestCompareVersionsInsufficientSamples, TestCompareVersionsInvalidScores, TestWilsonScoreIntervals, TestMergeDecisionFromClassification, TestBonferroniCorrection, TestStatsDependencyGuard) use descriptive naming: e.g., `test_compare_versions_similar_arrays_not_blocking`, `test_merge_decision_regression_blocks`, `test_stats_py_no_forbidden_imports`.
- **test_baselines.py**: 0 of 21 methods use `_should_`. All 21 test methods (e.g., `test_store_and_retrieve_round_trip`, `test_store_returns_baseline_record`, `test_retrieve_invalidated_raises`) remain in descriptive style.
- **test_debiasing.py**: 0 of ~28 methods use `_should_`. All use descriptive style: `test_default_construction_succeeds`, `test_shuffle_criteria_changes_order`, `test_randomize_positions_returns_result`.
- **test_metamorphic_base.py**: 5 of ~38 methods use `_should_` (TestMRViolationSeverity only — enum member value checks). The remaining ~33 methods (TestMRResult, TestValidateInputs*, TestStatisticalHelpers, TestParaphraseConsistency, TestNegationHandling) use descriptive names: `test_mr_result_frozen`, `test_insufficient_samples_raises`, `test_mean_helper`.
- **test_version_keys.py**: 3 of ~40 methods use `_should_` (TestEvaluationModeVersionKeys only). The remaining ~37 behavioral tests (TestVersionKeyValidConstruction, TestVersionKeyShortHashRejected, TestVersionKeyPathTraversalRejected, TestVersionKeyFromString, TestBaselineMetadataMinimumRuns, TestValidateBaselineVersionKey, TestVersionKeyRegistry, TestBuildVersionKeyMocked) use descriptive names.
- **test_types.py**: 18 of ~42 methods use `_should_` (all enum-value tests). The remaining ~24 tests (TestBaselineRecord, TestWilcoxonResult, TestWilsonResult, TestBonferroniConfig, TestRegressionResult, TestMultiMetricResult, TestScoreArray) use descriptive names.

Across all 6 files: approximately 30 of ~215 total test methods use BDD `_should_` naming, a compliance rate of ~14%. CG-020 requires `test_{what}_should_{expected}` for all methods. The pattern applied was: rename enum-value assertion tests (which fit the pattern cleanly) but leave behavioral, structural, and error-path tests in descriptive form.

**Positive preservation:** The rigorous testing methodology from iteration 1 is fully preserved — boundary value analysis, error message content assertions, static AST-based dependency guard, parametrized invariants, monkeypatching for isolation.

**Gaps:**

- ~86% of test methods in the 6 targeted files remain non-BDD, directly violating CG-020. This is the primary methodological gap and the reason this dimension cannot score above 0.85.
- The pattern is inconsistent within files: same test class may have BDD-named enum checks next to non-BDD behavioral tests, reducing the signal clarity of the naming convention.

**Improvement Path:**

Rename all remaining non-BDD test methods across the 6 files. Estimated scope: ~185 method renames. Examples:
- `test_compare_versions_similar_arrays_not_blocking` → `test_compare_versions_with_similar_arrays_should_not_block_merge`
- `test_store_and_retrieve_round_trip` → `test_store_and_retrieve_should_return_equivalent_data`
- `test_shuffle_criteria_changes_order` → `test_shuffle_criteria_should_change_element_order`

---

### Evidence Quality (0.90/1.00)

**Evidence:**

The CG reference additions are substantive and accurate:

- test_baselines.py module docstring (lines 21-27): Added CG-002 (BaselineStore persistence) and CG-027 (VERSION_KEY_PATTERN regex). The inline comment on line 61 (`"# A valid version key: 7+ lowercase hex chars, colon, non-empty path (CG-027)"`) correctly characterizes the relaxed regex used by BaselineStore.
- test_types.py module docstring (line 15): Added CG-005 (typed exception hierarchy and domain type definitions). This is correct — test_types.py tests types.py which is part of the CG-005 domain type infrastructure.
- test_stats.py module docstring (line 18): Added CG-001 (statistical engine public API coverage). Accurate.
- test_version_keys.py module docstring (lines 21): Added CG-027 (VERSION_KEY_PATTERN). Accurate — version_keys.py implements this pattern.
- test_debiasing.py (lines 16-18): The behavioral-contracts.md reference now includes the full path `projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md`. This resolves the non-navigable reference from iteration 1.
- test_metamorphic_base.py (lines 17-19): Similarly fixed — now reads `(projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md)`.

All individual test docstrings preserve the 3-sentence structure: assertion claim, design rationale, consequence. Helper factory methods retain Args/Returns documentation.

**Gaps:**

- Class-level docstrings in test_stats.py's behavioral test classes (TestCompareVersionsNoRegression, TestCompareVersionsRegression, etc.) still use free-text descriptions without FR ID citations in the class docstring itself. The module docstring cites FR-014 through FR-017, but the class docstrings do not trace individual classes to specific FR AC numbers.
- test_debiasing.py class docstrings cite "FR-021 AC-1" inline in some test docstrings (`(FR-021 AC-1)`) but not in the class-level docstrings (`class TestShuffleCriteria:` has no FR ID).

**Improvement Path:**

Add FR ID annotations to class-level docstrings in test_stats.py and test_debiasing.py class docstrings, e.g., `"""Tests for compare_versions() — covers FR-014, FR-015 (Wilcoxon)."""`

---

### Actionability (0.87/1.00)

**Evidence:**

The highest-impact actionability fix from iteration 1 is confirmed: `pytestmark = [pytest.mark.unit]` at module level means `pytest -m unit` now discovers all tests across all 6 files. The `pytest -m unit` command no longer silently skips ~60% of the test suite.

The improvements needed remain concrete and enumerable: BDD rename of ~185 methods, evaluator fixture contract test, class-docstring FR ID additions.

**Gaps:**

- The `_VALID_VERSION_KEY = "abc1234:skills/ps-researcher.md"` constant (test_baselines.py line 62) uses a 7-character hash. The added comment explains the discrepancy: `"# A valid version key: 7+ lowercase hex chars, colon, non-empty path (CG-027)"`. This satisfies the documentation aspect but the constant still uses an abbreviated format that differs from the 40-char requirement in test_version_keys.py. A developer reading test_baselines.py alongside test_version_keys.py will still encounter the format inconsistency; only the comment explains why.
- The incomplete BDD rename leaves ~185 method names to be changed, reducing the maintenance clarity benefit that BDD naming provides.

**Improvement Path:**

For the version key: update the `_VALID_VERSION_KEY` comment to explicitly state that BaselineStore accepts 7+ hex chars per CG-027 while VersionKey requires exactly 40 chars per FR-004, and consider adding a companion `_FULL_VALID_KEY = "a" * 40 + ":skills/ps-researcher.md"` constant to make the distinction explicit in the code rather than only in comments.

---

### Traceability (0.84/1.00)

**Evidence:**

The marker fix is the largest traceability improvement: all 6 files now carry `pytestmark = [pytest.mark.unit]`, meaning `pytest --collect-only -m unit` will enumerate every test in the targeted files. This resolves the primary traceability failure from iteration 1.

CG ID additions improve requirement traceability:
- test_baselines.py: CG-002, CG-027 added to module docstring
- test_types.py: CG-005 added
- test_stats.py: CG-001 added
- test_version_keys.py: CG-027 added
- test_debiasing.py: behavioral-contracts.md full path added
- test_metamorphic_base.py: behavioral-contracts.md full path added

**Gaps:**

- In test_stats.py, FR IDs appear in the module docstring (FR-014, FR-015, FR-016, FR-017) but individual test class docstrings contain free-text descriptions only: `class TestCompareVersionsNoRegression:` docstring says "compare_versions() correctly classifies stable arrays" with no FR citation. The per-class traceability link is missing.
- In test_debiasing.py, AC IDs ("FR-021 AC-1", "FR-021 AC-2", "FR-021 AC-3") appear in individual test method docstrings of TestShuffleCriteria and TestRandomizeCandidatePositions, but not in the class docstrings: `class TestShuffleCriteria:` has no FR-021 reference.
- test_baselines.py has no CG IDs in class docstrings (TestBaselineStoreStore, TestBaselineStoreRetrieve, TestBaselineStoreAudit, TestBaselineStoreInvalidate). The module docstring references CG-002 and CG-027, but individual test classes do not trace to specific acceptance criteria.

**Improvement Path:**

Add FR/CG ID citations to class-level docstrings in test_stats.py and test_debiasing.py. For test_baselines.py, add CG-002 citation to the TestBaselineStoreStore and TestBaselineStoreAudit class docstrings.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Methodological Rigor | 0.82 | 0.90 | Complete BDD rename: rename the ~185 remaining test methods across test_baselines.py (21 methods), test_debiasing.py (~28 methods), test_stats.py (~48 remaining), test_metamorphic_base.py (~33 remaining), test_version_keys.py (~37 remaining), test_types.py (~24 remaining) to use `test_{what}_should_{expected}` per CG-020. This is a bulk rename with no logic changes. |
| 2 | Traceability | 0.84 | 0.92 | Add FR/CG ID citations to class-level docstrings in the 6 files: test_stats.py class docstrings (FR-014 through FR-017 per class), test_debiasing.py class docstrings (FR-021 AC-1/AC-2/AC-3), test_baselines.py class docstrings (CG-002 per class). |
| 3 | Completeness | 0.91 | 0.95 | Add `test_evaluator_fixture_raises_on_missing_api_key` in conftest.py or a dedicated fixture test, using `monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)` to verify `EvaluationConfigError` is raised when model name contains "claude". |
| 4 | Internal Consistency | 0.88 | 0.92 | Consolidate duplicated `DebiasingStrategy.reset_rng()` tests between test_debiasing.py::TestResetRng and test_layer2_evaluation.py::TestDebiasingStrategy. Retain the more comprehensive version; add a comment explaining the deliberate consolidation. |
| 5 | Actionability | 0.87 | 0.92 | In test_baselines.py, add a companion constant alongside `_VALID_VERSION_KEY`: `_FULL_VALID_VERSION_KEY = "a" * 40 + ":skills/ps-researcher.md"` and use it for tests that specifically validate full-SHA enforcement vs. the 7-char BaselineStore relaxed format. Add an inline comment distinguishing the two patterns. |

---

## Iteration Delta Analysis

| Dimension | Iter 1 Score | Iter 2 Score | Delta | Change Driver |
|-----------|-------------|-------------|-------|---------------|
| Completeness | 0.88 | 0.91 | +0.03 | pytestmark fix; CG references added across all 6 files |
| Internal Consistency | 0.87 | 0.88 | +0.01 | Logic unchanged; within-file mixing is a minor regression offset by cross-file improvement |
| Methodological Rigor | 0.86 | 0.82 | -0.04 | BDD rename applied to ~14% of methods only; within-file style mixing is a new inconsistency |
| Evidence Quality | 0.88 | 0.90 | +0.02 | CG IDs added; behavioral-contracts.md paths fully qualified |
| Actionability | 0.80 | 0.87 | +0.07 | Marker fix closes the pytest -m unit gap (highest-impact actionability fix) |
| Traceability | 0.72 | 0.84 | +0.12 | Markers make tests machine-queryable; CG IDs improve requirement traceability |
| **Composite** | **0.836** | **0.872** | **+0.036** | |

**Note on Methodological Rigor regression:** The iteration 1 score of 0.86 reflected a situation where all 6 files had uniform descriptive naming (a consistent but non-BDD style). Iteration 2 applied BDD naming selectively (only enum-value tests), creating within-file style mixing that is more inconsistent than the prior uniform-but-non-compliant state. The score reflects the net negative of partial compliance against CG-020. A full rename would recover this dimension to 0.90+.

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented with specific file references and line numbers for every score
- [x] Uncertain scores resolved downward: Methodological Rigor at 0.82 (considered 0.84; resolved downward because the within-file mixing introduced by partial rename is a new quality regression, not just a gap)
- [x] Iteration calibration considered: score increase of +0.036 is proportionate to the fixes applied (marker gap closed = large traceability/actionability gain; BDD partial = small/negative methodological gain)
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] BDD adoption was verified by grep count before scoring Methodological Rigor; claim "renamed test methods to BDD-style" was evaluated against actual file evidence, not the fix description alone

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.872
threshold: 0.92
weakest_dimension: methodological_rigor
weakest_score: 0.82
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Complete BDD rename: ~185 remaining test methods across 6 files to test_{what}_should_{expected} per CG-020"
  - "Add FR/CG ID citations to class-level docstrings in test_stats.py, test_debiasing.py, test_baselines.py"
  - "Add evaluator fixture contract test: monkeypatch.delenv ANTHROPIC_API_KEY and assert EvaluationConfigError"
  - "Consolidate duplicated DebiasingStrategy.reset_rng() tests between test_debiasing.py and test_layer2_evaluation.py"
  - "Add _FULL_VALID_VERSION_KEY companion constant in test_baselines.py to distinguish BaselineStore vs VersionKey hash formats"
```
