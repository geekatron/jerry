# Quality Score Report: WI5-A Unit Test Suite (tests/prompt-regression/unit/)

## L0 Executive Summary

**Score:** 0.836/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.72)
**One-line assessment:** A well-isolated, extensively documented test suite that earns strong marks for consistency and rigor, but is held back by inconsistent `@pytest.mark.unit` marker coverage across older test files, partial BDD naming compliance (CG-020 adherence is file-dependent), and missing CG requirement cross-references in several files.

---

## Scoring Context

- **Deliverable:** `tests/prompt-regression/unit/` (15 test files + conftest.py)
- **Deliverable Type:** Code (unit test suite for prompt regression harness)
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 1 (first review)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.836 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | 15 files covering all CG gaps; marker and naming gaps in ~6 older files |
| Internal Consistency | 0.20 | 0.87 | 0.174 | No contradictions in logic; minor inconsistency in marker and naming style across file cohorts |
| Methodological Rigor | 0.20 | 0.86 | 0.172 | BDD test-first pattern applied in newer files; inconsistently applied in 6 of 15 files |
| Evidence Quality | 0.15 | 0.88 | 0.132 | Docstrings present on all test methods; module-level references to CG/FR IDs present in most files |
| Actionability | 0.15 | 0.80 | 0.120 | Clear improvement path exists; gaps are concrete and enumerable |
| Traceability | 0.10 | 0.72 | 0.072 | Inconsistent FR/CG cross-references; 6 files reference H-20 only; marker gaps prevent automated test-type queries |
| **TOTAL** | **1.00** | | **0.836** | |

---

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence:**

The suite spans 15 test files and covers all five CG requirements under evaluation:

- **CG-019 (Test isolation):** Every test class avoids external service calls. `tmp_path` and `monkeypatch` are used throughout for filesystem isolation. The `@pytest.mark.unit` marker is declared on tests in the newer files (test_exceptions.py, test_promptfoo_extractor.py, test_output_truncation.py, test_path_validation.py, test_gha_output_sanitization.py, test_version_key_validation.py, test_resolve_model.py, test_layer2_evaluation.py).
- **CG-020 (Test naming):** BDD-style `test_{what}_should_{expected}` naming is applied consistently in the 8 files listed above. However, test_stats.py, test_types.py, test_debiasing.py, test_metamorphic_base.py, test_baselines.py, and test_version_keys.py use `test_{description}` (e.g., `test_compare_versions_similar_arrays_not_blocking`, `test_baseline_record_is_mutable`, `test_mr_result_frozen`) without the `_should_` BDD particle.
- **CG-021 (Metric name resolution):** Fully addressed in `test_promptfoo_extractor.py::TestMetricNameResolution` — three tests cover `assertion.metric` > `assertion.type` > `"unnamed"` precedence (lines 342–398).
- **CG-022 (Exception hierarchy):** Fully addressed in `test_exceptions.py` — 15 tests covering all three exception classes, inheritance isolation, context defaults, and message formatting.
- **CG-026 (90% line coverage):** No coverage report available for direct verification. The breadth of branch testing is high: error paths, boundary values, empty inputs, invalid types, and degenerate cases (e.g., all-identical arrays in test_stats.py::TestCompareVersionsIdenticalArrays) are consistently tested.

**Gaps:**

- Six test files (test_stats.py, test_types.py, test_debiasing.py, test_metamorphic_base.py, test_baselines.py, test_version_keys.py) do not use `@pytest.mark.unit` on individual test methods. At class level in these files the marker is absent entirely, meaning `pytest -m unit` would not run these tests.
- The `evaluator` fixture in conftest.py (session-scoped, CG-011) performs lazy imports of `DeepEvalAdapter` and `DebiasingStrategy` — no unit tests verify the fixture itself fails safely when `ANTHROPIC_API_KEY` is absent, which the fixture docstring claims it raises `EvaluationConfigError`.

**Improvement Path:**

Add `@pytest.mark.unit` to all test classes in the six files listed above, or apply the marker at the module level via `pytestmark = [pytest.mark.unit]`. Add a test for the fixture's `EvaluationConfigError` behaviour under missing API key.

---

### Internal Consistency (0.87/1.00)

**Evidence:**

No logical contradictions exist within the suite. The S-014 PASS threshold of 0.92 is consistently used across test_metrics.py, test_layer2_evaluation.py, and test_stats.py. The `QUALITY_PASS_THRESHOLD == 0.92` constant assertion in test_stats.py::TestNamedConstants (line 92) and the `classify_composite(0.92) == "PASS"` assertion in test_metrics.py (line 140) and test_layer2_evaluation.py (line 537) are all aligned.

The `EvaluationMode.SMOKE / STANDARD / FULL` value assertions in test_types.py and test_version_keys.py::TestEvaluationModeVersionKeys are consistent, and test_version_keys.py::test_local_enum_members_match_canonical_types explicitly cross-validates the two enum definitions.

The conftest.py docstring correctly references FR-006 and FR-021.

**Gaps:**

- Two file cohorts exist with different naming conventions (BDD `_should_` vs. descriptive), which is a style inconsistency rather than a logic contradiction, but it creates a perception of inconsistent standards application.
- `test_debiasing.py` and `test_layer2_evaluation.py` both test `DebiasingStrategy` and contain overlapping tests (e.g., `test_reset_rng_reproduces_sequence` in both files). This duplication is not contradictory but is minor internal redundancy.

**Improvement Path:**

Standardize naming convention across all 15 files. Consolidate the duplicated `DebiasingStrategy.reset_rng()` tests between test_debiasing.py and test_layer2_evaluation.py.

---

### Methodological Rigor (0.86/1.00)

**Evidence:**

The suite applies rigorous testing methodology in several demonstrable ways:

1. **Boundary value analysis:** Every numeric constraint is tested at both valid and invalid boundaries. Examples: `test_compare_versions_alpha_too_high` / `test_compare_versions_alpha_too_low` in test_stats.py (lines 291–303); `test_swap_probability_boundary_zero` / `test_swap_probability_boundary_one` in test_debiasing.py (lines 86–94).
2. **Error message content assertions:** Tests verify that exception messages contain specific tokens (`"40"`, `"abbreviated"`, `"Smoke mode"`, `"CG-027"`) not just that exceptions are raised. This ensures error quality, not just error presence.
3. **Static dependency guard:** `TestStatsDependencyGuard.test_stats_py_no_forbidden_imports` (test_stats.py lines 527–561) uses `ast.parse()` to enforce FR-019 one-way dependency at test time.
4. **Parametrized invariant testing:** `TestPerAgentCriteriaInvariants` in test_layer2_evaluation.py (lines 631–730) applies 5 parametrized test cases across all 5 per-agent criteria sets.
5. **Monkeypatching for isolation:** `TestBuildVersionKeyMocked` in test_version_keys.py uses `monkeypatch.setattr` to test non-git paths without real subprocess calls.

**Gaps:**

- The `_should_` BDD naming pattern is present in only 8 of 15 files. Per CG-020 and H-20, the pattern `test_{what}_should_{expected}` is the project standard. Six of the older files (test_stats.py, test_types.py, test_debiasing.py, test_metamorphic_base.py, test_baselines.py, test_version_keys.py) use a descriptive but non-BDD form.
- The conftest.py `evaluator` fixture includes a session-scoped lazy import. No test validates that the fixture itself meets its contractual postconditions (error on missing key). This is a methodology gap — contract testing is incomplete for the shared fixture.

**Improvement Path:**

Rename test methods in the 6 non-BDD files to use the `test_{what}_should_{expected}` pattern. Add a parametrized test verifying the `evaluator` fixture's contract under missing `ANTHROPIC_API_KEY`.

---

### Evidence Quality (0.88/1.00)

**Evidence:**

All 15 files include module-level docstrings with: what is being tested, isolation guarantee ("No LLM calls performed"), and references to CG/FR IDs. Examples:

- test_exceptions.py docstring (lines 1–16): references CG-005, H-20.
- test_promptfoo_extractor.py (lines 1–21): references CG-008, CG-021, H-20.
- test_stats.py (lines 1–22): references FR-014, FR-015, FR-016, FR-017, H-20.
- test_layer2_evaluation.py (lines 1–26): references FR-006, FR-007, FR-021, H-20.

All test methods have individual docstrings that explain the assertion intent. The docstrings in newer files follow a 3-sentence structure: assertion claim, design rationale, consequence.

Helper factories are documented with Args/Returns sections (e.g., `_make_result()` in test_promptfoo_extractor.py lines 39–73; `_make_scores_varying()` in test_stats.py lines 58–60).

**Gaps:**

- Six older files (test_stats.py, test_types.py, test_debiasing.py, test_metamorphic_base.py, test_baselines.py, test_version_keys.py) reference only `H-20` in their module docstrings without citing the specific CG requirement being closed. For example, test_baselines.py (line 22) mentions `FR-004`, `FR-020`, `FR-014`, and `H-20` — which is adequate — but test_types.py (line 11) only references `H-07` and `H-20` without citing CG requirements (the types module predates the CG numbering scheme, but the omission is still a traceability gap).
- test_metamorphic_base.py references `behavioral-contracts.md §B.5` and `Section C` but does not include the full path to the contracts document in its references block. This makes the reference non-navigable without prior context.

**Improvement Path:**

Add CG requirement IDs to module-level references in the 6 older files where applicable. Expand the behavioral-contracts.md reference in test_metamorphic_base.py to include the full repository path.

---

### Actionability (0.80/1.00)

**Evidence:**

All tests are runnable via `uv run pytest tests/prompt-regression/unit/ -v --tb=short`. The test file structure is clear: one class per concern, named after the component under test. The conftest.py sys.path manipulation is correctly placed (per the docstring's own commentary on the iter2 fix). The `tmp_path` fixture is used uniformly for filesystem isolation, and `monkeypatch` is used for environment variable control.

The improvements needed are clearly enumerable (see Improvement Path sections above), making the path from current state to PASS verdict concrete.

**Gaps:**

- The `@pytest.mark.unit` gap in 6 files means `pytest -m unit` silently skips ~60% of the test suite. This is an actionability failure: a developer running `pytest -m unit` for fast iteration would get false confidence from a severely reduced test run.
- No `pytestmark` module-level declaration is used in any file; markers must be applied per-method. With 200+ test methods across 15 files, this creates significant maintenance surface.
- test_baselines.py uses `_VALID_VERSION_KEY = "abc1234:skills/ps-researcher.md"` which is a 7-char short SHA. The baseline store's own validation (`_validate_version_key`) accepts this, but the string does not match the 40-char full-SHA format required by VersionKey in test_version_keys.py. This cross-file inconsistency in test data format is a minor coherence issue that could confuse maintainers.

**Improvement Path:**

Add `pytestmark = [pytest.mark.unit]` at the module level in the 6 files missing it. Update test_baselines.py test data to use a consistent version key format with an explanatory comment that the BaselineStore accepts shorter SHAs (since it uses its own less-strict `VERSION_KEY_PATTERN`).

---

### Traceability (0.72/1.00)

**Evidence:**

The newer 8 files (test_exceptions.py, test_promptfoo_extractor.py, test_output_truncation.py, test_path_validation.py, test_gha_output_sanitization.py, test_version_key_validation.py, test_resolve_model.py, test_layer2_evaluation.py) have strong traceability:
- CG requirement IDs appear in module docstrings and individual test docstrings.
- Class docstrings reference the specific FR/CG being tested.
- Error match strings include requirement IDs (e.g., `match="CG-027"`, `match="CG-025"`, `match="Bedrock/Vertex"`).

**Gaps:**

The 6 older files (test_stats.py, test_types.py, test_debiasing.py, test_metamorphic_base.py, test_baselines.py, test_version_keys.py) have lower traceability:

1. **test_types.py:** References H-07 and H-20 only. No CG IDs. Types (BaselineRecord, RegressionResult, etc.) do not have FR IDs cited in their test classes.
2. **test_stats.py:** References FR-014 through FR-017 and H-20 in the module docstring, but test classes do not cite FR IDs in their class docstrings (only free-text descriptions like "FR-014: N >= 20 enforcement").
3. **test_debiasing.py:** References FR-021 and H-20 but AC IDs (AC-1, AC-2, AC-3) are used in individual test docstrings inconsistently — some say "(FR-021 AC-1)" inline, most do not.
4. **test_metamorphic_base.py:** References FR-010 and `behavioral-contracts.md Section C` but Section C path is incomplete (no repo-relative path).
5. **test_baselines.py:** References FR-004, FR-020, FR-014, H-20 — adequate but no CG IDs (the baselines module predates the CG numbering gap analysis).
6. **test_version_keys.py:** References FR-004 and OWASP/ASVS; no CG IDs. The `@pytest.mark.unit` gap also means these tests cannot be traced via marker query.

**Improvement Path:**

Add CG requirement IDs to class docstrings and module references in the 6 older files. Add the full repo-relative path for behavioral-contracts.md in test_metamorphic_base.py. Add `@pytest.mark.unit` so tests are queryable by marker.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.72 | 0.88 | Add `pytestmark = [pytest.mark.unit]` at module level in test_stats.py, test_types.py, test_debiasing.py, test_metamorphic_base.py, test_baselines.py, test_version_keys.py. This single change raises traceability (marker-queryable) and actionability (pytest -m unit finds all tests). |
| 2 | Methodological Rigor | 0.86 | 0.93 | Rename non-BDD test methods in the 6 older files to use `test_{what}_should_{expected}` per CG-020. This is a bulk rename, not a logic change. Estimated scope: ~120 method renames. |
| 3 | Traceability | 0.72 | 0.88 | Add CG requirement IDs to class docstrings in test_types.py, test_stats.py (FR-014/FR-015/FR-016/FR-017 → link to CG where applicable). Expand behavioral-contracts.md reference in test_metamorphic_base.py to include the full path `projects/PROJ-036-prompt-regression-harness/contracts/behavioral-contracts.md`. |
| 4 | Actionability | 0.80 | 0.88 | Update test_baselines.py version key test data comment to explain that `BaselineStore._validate_version_key` uses a relaxed 7-char-minimum regex (CG-027) distinct from the strict 40-char `VersionKey` used in test_version_keys.py. |
| 5 | Completeness | 0.88 | 0.93 | Add a test for conftest.py `evaluator` fixture: verify `EvaluationConfigError` is raised when `ANTHROPIC_API_KEY` is unset and model name contains "claude". Use `monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)`. |
| 6 | Internal Consistency | 0.87 | 0.92 | Consolidate duplicated `DebiasingStrategy.reset_rng()` tests between test_debiasing.py::TestResetRng and test_layer2_evaluation.py::TestDebiasingStrategy.test_reset_rng_produces_same_sequence — keep the more comprehensive version. |

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score with specific file references and line numbers
- [x] Uncertain scores resolved downward (Traceability was initially considered 0.75; resolved to 0.72 given the 6-file marker gap is systemic)
- [x] First-draft calibration considered — this is iteration 1; the composite 0.836 is appropriate for a well-written but partially compliant test suite
- [x] No dimension scored above 0.95 without exceptional evidence (highest is 0.88)

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.836
threshold: 0.92
weakest_dimension: traceability
weakest_score: 0.72
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Add pytestmark = [pytest.mark.unit] at module level in 6 older test files"
  - "Rename test methods in 6 older files to BDD test_{what}_should_{expected} pattern (CG-020)"
  - "Add CG requirement IDs to class docstrings in test_types.py, test_stats.py, test_metamorphic_base.py"
  - "Add full path for behavioral-contracts.md in test_metamorphic_base.py references"
  - "Add evaluator fixture contract test for EvaluationConfigError on missing API key"
  - "Consolidate duplicated DebiasingStrategy.reset_rng() tests between test_debiasing.py and test_layer2_evaluation.py"
```
