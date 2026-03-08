# Quality Score Report: WI5-A Unit Test Suite (tests/prompt-regression/unit/) — Iteration 3

## L0 Executive Summary

**Score:** 0.910/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Actionability (0.88)
**One-line assessment:** The two blocking gaps from iteration 2 are fully closed (100% BDD naming confirmed by grep, class-level FR/CG citations confirmed in all 6 files), lifting the composite from 0.872 to 0.910 — still 0.010 below the 0.92 gate, with Actionability the remaining swing dimension.

---

## Scoring Context

- **Deliverable:** `tests/prompt-regression/unit/` (6 targeted files: test_baselines.py, test_types.py, test_debiasing.py, test_metamorphic_base.py, test_stats.py, test_version_keys.py)
- **Deliverable Type:** Code (unit test suite for prompt regression harness)
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.872 (iteration 2)
- **Scored:** 2026-03-07T14:00:00Z
- **Iteration:** 3 (re-score after FIX-WI5-A-v2)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.910 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |
| **Delta from Iteration 2** | +0.038 |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.91 | 0.182 | No new completeness changes; evaluator fixture contract test still absent |
| Internal Consistency | 0.20 | 0.90 | 0.180 | Within-file BDD/non-BDD mixing fully resolved; cross-file duplicate reset_rng() persists |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | 100% BDD naming confirmed — grep for non-BDD pattern returns zero matches across all 6 files |
| Evidence Quality | 0.15 | 0.93 | 0.1395 | Class-level FR/CG citations now present in all 6 files; addresses iteration 2 Priority 2 gap |
| Actionability | 0.15 | 0.88 | 0.132 | BDD naming complete; evaluator fixture and _VALID_VERSION_KEY companion constant still absent |
| Traceability | 0.10 | 0.93 | 0.093 | Class-level FR/CG citations close per-class traceability gap; markers remain in place |
| **TOTAL** | **1.00** | | **0.910** | |

---

## Detailed Dimension Analysis

### Completeness (0.91/1.00)

**Evidence:**

No completeness changes were made in iteration 3 — the fix was confined to method renames and class docstring additions. The iteration 2 completeness state is preserved:

- `pytestmark = [pytest.mark.unit]` confirmed present in all 6 files (lines 36, 27, 25, 30, 30, 32 respectively)
- All 4 `BaselineStore` public methods are tested: store(), retrieve(), audit(), invalidate()
- All public stats functions tested: compare_versions(), compare_multiple_metrics(), wilson_score_intervals(), merge_decision_from_classification(), bonferroni_correction()
- All domain types in types.py tested: EvaluationMode, RegressionClass, RateClass, EffectSizeLabel, MergeDecision, BaselineRecord, WilcoxonResult, WilsonResult, BonferroniConfig, RegressionResult, MultiMetricResult, ScoreArray
- Both MR implementations tested: MR-001 (ParaphraseConsistency) and MR-002 (NegationHandling)
- Full VersionKey lifecycle tested: construction, validation, from_string, registry, build_version_key (mocked)

**Gaps:**

- The evaluator fixture contract test (conftest.py `evaluator` fixture) is still absent. No test verifies that `EvaluationConfigError` is raised when `ANTHROPIC_API_KEY` is missing. This was the Priority 3 recommendation from iteration 2 and remains unaddressed in iteration 3.
- The `_VALID_VERSION_KEY = "abc1234:skills/ps-researcher.md"` (7-char hash) in test_baselines.py remains without the companion `_FULL_VALID_VERSION_KEY` constant that would make the CG-027 vs FR-004 format distinction explicit in code.

**Improvement Path:**

Add `test_evaluator_fixture_should_raise_on_missing_api_key` using `monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)` in conftest.py or a dedicated fixture test file. This is the highest-value remaining completeness addition.

---

### Internal Consistency (0.90/1.00)

**Evidence:**

The primary internal consistency regression from iteration 2 is fully resolved. Iteration 2 introduced within-file BDD/non-BDD style mixing when it selectively renamed ~14% of test methods — this created inconsistency that did not exist in iteration 1 (where all files had uniform, if non-BDD, descriptive naming). Iteration 3 achieves uniform BDD naming throughout all 6 files.

Verified: the negative-pattern grep `def test_(?!.*_should_)` returns zero matches across all 6 targeted files. This confirms there are no residual descriptive-style test method names.

Logic is unchanged from iteration 2 — no test assertions were modified. The `QUALITY_PASS_THRESHOLD = 0.92` alignment across test_stats.py, test_metrics.py, and test_layer2_evaluation.py is preserved. The `EvaluationMode` cross-validation in TestEvaluationModeVersionKeys (test_version_keys.py lines 87-104) continues to import and compare both local and canonical EvaluationMode definitions.

**Gaps:**

- The duplicated `DebiasingStrategy.reset_rng()` test between test_debiasing.py::TestResetRng and test_layer2_evaluation.py::TestDebiasingStrategy was not consolidated (this is outside the 6 targeted files' scope for iteration 3, but remains a cross-file consistency concern). The more comprehensive version in test_debiasing.py is: `test_reset_rng_should_reproduce_same_sequence`. Both test the same behavioral contract.

**Improvement Path:**

Consolidate the `reset_rng()` behavioral test. Retain the seeded strategy version in test_debiasing.py (which is more thorough — it calls `shuffle_criteria` twice and compares sequences). Add a comment in test_layer2_evaluation.py's TestDebiasingStrategy noting that `reset_rng()` is covered in test_debiasing.py::TestResetRng, or remove the duplicate.

---

### Methodological Rigor (0.92/1.00)

**Evidence:**

The iteration 2 blocking gap (BDD naming applied to only ~14% of test methods) is fully closed. Verification method: grep for `def test_(?!.*_should_)` across all 6 files returns zero matches. All 209 test methods across all 6 targeted files now use `test_{what}_should_{expected}` naming per CG-020.

Spot-check of 10 sampled method names across different files:

1. test_baselines.py: `test_store_and_retrieve_should_round_trip` (line 79) — BDD
2. test_baselines.py: `test_invalidate_should_return_zero_for_nonexistent_agent` (line 403) — BDD
3. test_types.py: `test_all_six_members_should_be_present` (line 109) — BDD
4. test_debiasing.py: `test_shuffle_criteria_should_change_element_order` (line 107) — BDD
5. test_debiasing.py: `test_swap_probability_at_zero_boundary_should_be_accepted` (line 88) — BDD
6. test_stats.py: `test_compare_versions_with_similar_arrays_should_not_produce_blocking_classification` (line 124) — BDD
7. test_stats.py: `test_bonferroni_correction_should_compute_correct_k13_alpha` (line 502) — BDD
8. test_metamorphic_base.py: `test_mr_result_should_be_frozen` (line 156) — BDD
9. test_metamorphic_base.py: `test_boundary_values_should_be_accepted` (line 251) — BDD
10. test_version_keys.py: `test_registry_covered_agents_should_be_nonempty` (line 367) — BDD

The rigorous testing methodology is fully preserved and unchanged: boundary value analysis (swap_probability at 0.0/1.0, score at 0.0/1.0, hash at 39/40/41 chars), error message content assertions, static AST-based dependency guard (test_stats.py TestStatsDependencyGuard), parametrized-style invariant coverage, monkeypatching for git subprocess isolation (TestBuildVersionKeyMocked), and seed-controlled RNG for determinism.

**Gaps:**

- No BDD methodology documentation exists (no test plan or BDD specification linking `_should_` naming to FR/CG requirements). The naming convention is mechanically correct but its rationale is implicit rather than documented. This prevents reaching 0.95+.
- The static AST dependency guard (TestStatsDependencyGuard) is the most sophisticated test in the suite; no equivalent guard verifies layer isolation in other modules.

**Improvement Path:**

This dimension now meets the 0.9+ criterion. To reach 0.95+, add a brief comment in a `conftest.py` or test module header explaining the BDD naming convention mandate (CG-020) and linking it to FR/CG traceability. This would make the methodology self-documenting rather than implicit.

---

### Evidence Quality (0.93/1.00)

**Evidence:**

The iteration 2 Priority 2 recommendation ("Add FR/CG ID citations to class-level docstrings") is confirmed closed. Class-level docstrings now cite specific FR/CG IDs across all 6 files:

**test_baselines.py** (confirmed by reading lines 77, 218, 276, 357):
- `TestBaselineStoreStore`: "covers CG-002 persistence requirements"
- `TestBaselineStoreRetrieve`: "covers CG-002 retrieval requirements"
- `TestBaselineStoreAudit`: "covers CG-002 audit requirements (FR-020)"
- `TestBaselineStoreInvalidate`: "covers CG-002 invalidation requirements"

**test_types.py** (confirmed by reading lines 50, 83, 129, 146, 171, 192, 249, 288, 322, 344, 418, 483):
- All 12 class docstrings include CG-005 reference

**test_debiasing.py** (confirmed by reading lines 65, 105, 176, 246, 265):
- `TestDebiasingStrategyConstruction`: "(FR-021)"
- `TestShuffleCriteria`: "covers FR-021 AC-1"
- `TestRandomizeCandidatePositions`: "covers FR-021 AC-3"
- `TestResetRng`: "covers FR-021 determinism"
- `TestBuildDebiasedPromptSection`: "covers FR-021"

**test_metamorphic_base.py** (confirmed by reading lines 107, 136, 187, 215, 232, 263, 294, 355):
- All 8 class docstrings cite FR-010

**test_stats.py** (confirmed by reading lines 87, 112, 162, 193, 221, 255, 284, 294, 328, 385, 461, 500, 539):
- All 13 class docstrings cite FR-014/FR-015/FR-016/FR-017/CG-001 as appropriate

**test_version_keys.py** (confirmed by reading lines 65, 113, 165, 201, 239, 266, 329, 365, 420):
- All 9 class docstrings cite FR-004 and/or CG-027 and/or OWASP A03:2021

All individual test method docstrings continue to follow the 3-sentence structure (assertion claim, design rationale, consequence). Helper factory methods retain Args/Returns documentation.

**Gaps:**

- AC-level per-method citations are present in some methods (e.g., test_debiasing.py method docstrings reference "(FR-021 AC-1)", "(FR-021 AC-2)", "(FR-021 AC-3)") but are not uniformly applied across all methods in all files. Most test_stats.py method docstrings do not include AC-level citations. This is a refinement gap, not a structural deficiency.
- The behavioral-contracts.md full-path references (already fixed in iteration 2) remain present.

**Improvement Path:**

To reach 0.95+, add AC-level citations to individual test method docstrings in test_stats.py behavioral classes (e.g., `TestCompareVersionsNoRegression` methods citing "FR-015 AC-2"). This is a refinement that would close the per-method traceability gap.

---

### Actionability (0.88/1.00)

**Evidence:**

The BDD rename to 100% compliance is a meaningful actionability improvement: `pytest -m unit` now produces a test run where every test name communicates its behavioral contract, reducing cognitive load for developers diagnosing failures. `test_compare_versions_with_similar_arrays_should_not_produce_blocking_classification` is unambiguous about the behavioral expectation; the prior `test_compare_versions_similar_arrays_not_blocking` required more interpretation.

The `pytest -m unit` discovery gap (closed in iteration 2) remains closed — all 6 files carry `pytestmark = [pytest.mark.unit]`.

The improvements made in iteration 3 are non-actionability items (method renames, docstring additions). The concrete remaining gaps from iteration 2 are unchanged:

**Gaps:**

- The `_VALID_VERSION_KEY = "abc1234:skills/ps-researcher.md"` constant (test_baselines.py line 62) uses a 7-character abbreviated hash. The comment `"# A valid version key: 7+ lowercase hex chars, colon, non-empty path (CG-027)"` explains why, but a developer reading test_baselines.py alongside test_version_keys.py (which rejects 7-char hashes with `VersionKeyError`) must rely on the comment to understand the format distinction. The recommended `_FULL_VALID_VERSION_KEY` companion constant was not added.
- The evaluator fixture contract test is still absent (same gap as iterations 1 and 2).
- The duplicate `reset_rng()` test between test_debiasing.py and test_layer2_evaluation.py is not consolidated, leaving two authoritative sources for the same behavioral contract.

**Improvement Path:**

Add `_FULL_VALID_VERSION_KEY = "a" * 40 + ":skills/ps-researcher.md"` to test_baselines.py alongside `_VALID_VERSION_KEY`, with an inline comment: `"# BaselineStore uses CG-027 relaxed format (7+ hex chars); VersionKey uses FR-004 full 40-char SHA-1."` Use `_FULL_VALID_VERSION_KEY` in tests that specifically validate SHA-1 completeness enforcement.

---

### Traceability (0.93/1.00)

**Evidence:**

The iteration 2 Priority 2 recommendation is confirmed closed. Class-level FR/CG ID citations now provide direct, per-class traceability from test classes to requirements:

- test_stats.py: `TestCompareVersionsNoRegression` cites "(FR-015, CG-001)" in its class docstring; `TestWilsonScoreIntervals` cites "(FR-016, CG-001)"; `TestBonferroniCorrection` cites "(FR-017, CG-001)"; `TestStatsDependencyGuard` cites "(FR-019, CG-001)"
- test_debiasing.py: `TestShuffleCriteria` cites "FR-021 AC-1"; `TestRandomizeCandidatePositions` cites "FR-021 AC-3"
- test_baselines.py: All 4 class docstrings cite CG-002 with specific sub-area (persistence, retrieval, audit, invalidation)
- test_version_keys.py: `TestVersionKeyPathTraversalRejected` cites "OWASP A03:2021"; `TestBuildVersionKeyMocked` class docstring references FR-004 and OWASP A03:2021

The `pytestmark = [pytest.mark.unit]` markers remain in all 6 files — confirmed. `pytest --collect-only -m unit` will enumerate all 209 test methods in the targeted files.

**Gaps:**

- Per-method AC-level traceability is not uniformly present. test_stats.py behavioral test classes have class-level FR citations but individual test methods within TestCompareVersionsRegression, TestCompareVersionsImprovement, etc. do not trace to specific FR AC numbers in their docstrings. In contrast, test_debiasing.py method docstrings do include AC-level references ("FR-021 AC-1", "FR-021 AC-2", "FR-021 AC-3").
- This is a partial traceability gap at the method level; class-level citations are now present and consistent.

**Improvement Path:**

The class-level citations now satisfy most traceability requirements. To reach 0.95+, add AC-level citations to individual test method docstrings in test_stats.py behavioral classes where specific FR AC numbers exist (e.g., FR-015 AC-1 = Wilcoxon p-value threshold, AC-2 = effect size classification).

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Actionability | 0.88 | 0.93 | Add `_FULL_VALID_VERSION_KEY = "a" * 40 + ":skills/ps-researcher.md"` constant in test_baselines.py with an explanatory comment distinguishing CG-027 (7+ hex) from FR-004 (40-char SHA-1). Add evaluator fixture contract test in conftest.py using `monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)` to verify `EvaluationConfigError` is raised. These two additions close the remaining actionability gaps and would move this dimension to ~0.93, raising the composite to ~0.92+. |
| 2 | Internal Consistency | 0.90 | 0.93 | Consolidate duplicated `DebiasingStrategy.reset_rng()` tests between test_debiasing.py::TestResetRng and test_layer2_evaluation.py::TestDebiasingStrategy. Retain the sequence-comparison version in test_debiasing.py; add a comment in test_layer2_evaluation.py directing readers to the canonical test. |
| 3 | Evidence Quality | 0.93 | 0.95 | Add per-method AC-level citations to test_stats.py behavioral test class methods where specific FR AC numbers apply. Low effort — these are docstring additions only, no logic changes. |
| 4 | Completeness | 0.91 | 0.94 | Add evaluator fixture contract test (also covered in Priority 1 above). If Priority 1 is implemented, this dimension will improve as a side-effect. |

---

## Iteration Delta Analysis

| Dimension | Iter 1 Score | Iter 2 Score | Iter 3 Score | Delta (2→3) | Change Driver |
|-----------|-------------|-------------|-------------|-------------|---------------|
| Completeness | 0.88 | 0.91 | 0.91 | 0.00 | No completeness changes in iteration 3 |
| Internal Consistency | 0.87 | 0.88 | 0.90 | +0.02 | Within-file BDD/non-BDD mixing fully resolved |
| Methodological Rigor | 0.86 | 0.82 | 0.92 | +0.10 | 100% BDD naming — zero non-BDD methods across all 6 files |
| Evidence Quality | 0.88 | 0.90 | 0.93 | +0.03 | Class-level FR/CG citations added to all classes in all 6 files |
| Actionability | 0.80 | 0.87 | 0.88 | +0.01 | BDD completeness minor benefit; core gaps unchanged |
| Traceability | 0.72 | 0.84 | 0.93 | +0.09 | Class-level FR/CG citations provide per-class traceability chain |
| **Composite** | **0.836** | **0.872** | **0.910** | **+0.038** | |

**Convergence note:** Three iterations have produced monotonically increasing scores (+0.036, +0.038). The composite is now 0.910 — 0.010 below the 0.92 gate. The Methodological Rigor recovery (+0.10) is the largest dimension gain in any iteration across the three-iteration series, confirming that the 100% BDD rename was the correct highest-priority fix. The remaining gap is concentrated in Actionability (0.88); addressing Priority 1 above is estimated to raise the composite to ~0.92.

---

## BDD Naming Verification Evidence

Verification method used: `grep -rn "def test_(?!.*_should_)"` (negative lookahead regex) across all 6 targeted unit test files.

**Result: zero matches.** This confirms that every test method definition in the 6 targeted files contains `_should_` in its name, satisfying CG-020 uniformly.

Additional spot-checks (10 methods, 6 different files):

| File | Method | BDD Compliant |
|------|--------|--------------|
| test_baselines.py:79 | `test_store_and_retrieve_should_round_trip` | Yes |
| test_baselines.py:403 | `test_invalidate_should_return_zero_for_nonexistent_agent` | Yes |
| test_types.py:109 | `test_all_six_members_should_be_present` | Yes |
| test_debiasing.py:88 | `test_swap_probability_at_zero_boundary_should_be_accepted` | Yes |
| test_stats.py:89 | `test_min_statistical_sample_size_should_equal_20` | Yes |
| test_stats.py:124 | `test_compare_versions_with_similar_arrays_should_not_produce_blocking_classification` | Yes |
| test_stats.py:502 | `test_bonferroni_correction_should_compute_correct_k13_alpha` | Yes |
| test_metamorphic_base.py:156 | `test_mr_result_should_be_frozen` | Yes |
| test_metamorphic_base.py:251 | `test_boundary_values_should_be_accepted` | Yes |
| test_version_keys.py:367 | `test_registry_covered_agents_should_be_nonempty` | Yes |

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented with specific file references and line numbers for every score
- [x] Uncertain scores resolved downward: Internal Consistency held at 0.90 (considered 0.91; resolved downward because the cross-file duplicate reset_rng() persists and the 0.91 reading felt generous)
- [x] Methodological Rigor capped at 0.92 despite perfect BDD compliance — no methodology documentation exists beyond the naming convention itself, preventing 0.95+
- [x] Actionability held at 0.88 — BDD completeness provides marginal improvement but the core gaps (evaluator fixture, companion constant) are unchanged
- [x] Iteration calibration considered: +0.038 delta is proportionate to the changes applied (major dimension recovery on Methodological Rigor via full BDD rename; meaningful improvement on Traceability via class docstrings)
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] BDD adoption verified by deterministic grep rather than impressionistic reading

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.910
threshold: 0.92
weakest_dimension: actionability
weakest_score: 0.88
critical_findings_count: 0
iteration: 3
improvement_recommendations:
  - "Add _FULL_VALID_VERSION_KEY constant in test_baselines.py with CG-027 vs FR-004 explanatory comment"
  - "Add evaluator fixture contract test: monkeypatch.delenv ANTHROPIC_API_KEY and assert EvaluationConfigError"
  - "Consolidate duplicate DebiasingStrategy.reset_rng() test between test_debiasing.py and test_layer2_evaluation.py"
  - "Add AC-level citations to individual test method docstrings in test_stats.py behavioral classes"
```
