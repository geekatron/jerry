# Quality Score Report: WI5-B — Integration Tests (All 3 Files, Iteration 2)

## L0 Executive Summary
**Score:** 0.924/1.00 | **Verdict:** PASS | **Weakest Dimension:** Evidence Quality (0.86)
**One-line assessment:** Iteration 2 addresses the four highest-priority gaps from iteration 1 — extraction error paths, FR-020 quality gate rejection (with bonus boundary-condition test), module-level `pytestmark`, and `os.getcwd` monkeypatch — bringing the composite above the 0.92 threshold; three minor residual gaps (dead-code block still present, `GITHUB_OUTPUT`-absent branch untested, `debiasing_strategy` assertion absent in smoke test) prevent a higher score but do not block acceptance.

---

## Scoring Context
- **Deliverable:** `tests/prompt-regression/integration/test_layer4_pipeline.py`, `tests/prompt-regression/integration/test_evaluator_construction.py`, `tests/prompt-regression/conftest.py` (plus co-scored `test_pipeline_smoke.py`)
- **Deliverable Type:** Code (integration test suite)
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 2 (re-score after FIX-WI5-B)
- **Prior Score:** 0.896 REVISE (iteration 1)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.924 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | All 6 structural scenarios covered; `TestScoreExtractionErrorPaths` and `TestBaselineStoreQualityGateRejection` (with boundary test) added; dead-code block at lines 285-286 of `test_pipeline_smoke.py` still present; `GITHUB_OUTPUT`-absent branch still missing. |
| Internal Consistency | 0.20 | 0.94 | 0.188 | Naming conventions, FR citations, and docstring structure remain coherent across all files; `TestConftestEvaluatorFixture` still not renamed; `debiasing_strategy` assertion still absent in smoke test's evaluator test. |
| Methodological Rigor | 0.20 | 0.96 | 0.192 | `pytestmark = [pytest.mark.integration]` at module level in `test_layer4_pipeline.py` (line 33) closes the primary methodological gap; `os.getcwd` monkeypatch applied in all three `TestPersistReport` tests; all other existing patterns (monkeypatch, tmp_path, dc_replace, mock port injection) intact. |
| Evidence Quality | 0.15 | 0.86 | 0.129 | `TestScoreExtractionErrorPaths` adds `FileNotFoundError` and `ValueError` coverage; `TestBaselineStoreQualityGateRejection` adds below-threshold rejection and exact-boundary boundary tests; `GITHUB_OUTPUT`-absent branch still unverified; `debiasing_strategy` not asserted in smoke evaluator test. |
| Actionability | 0.15 | 0.92 | 0.138 | Module-level `pytestmark` ensures CI engineers running `-m integration` now capture `test_layer4_pipeline.py`; extraction error tests provide clear failure diagnostics; FR-020 rejection test uses `match="quality gate"` for diagnostic precision; dead-code block at lines 285-286 still slightly reduces living-documentation clarity. |
| Traceability | 0.10 | 0.93 | 0.093 | `WI-5B` reference added to `test_layer4_pipeline.py` module docstring (line 22) and `test_pipeline_smoke.py` (line 27); `FR-020` explicitly cited in `test_pipeline_smoke.py` References (line 24); `H-20` present in `test_layer4_pipeline.py` (line 21); `WI-5B` and `CG-026` absent from `test_evaluator_construction.py` and `conftest.py`. |
| **TOTAL** | **1.00** | | **0.924** | |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence:**

All six structural scenarios declared in the module docstrings are implemented. The four original scenarios from iteration 1 remain intact. Two new scenario classes were added in `test_pipeline_smoke.py`:

- **`TestScoreExtractionErrorPaths`** (lines 332-384): Two tests — `test_extract_score_arrays_missing_file_should_raise_file_not_found` (nonexistent path raises `FileNotFoundError`) and `test_extract_score_arrays_invalid_json_should_raise_value_error` (syntactically invalid JSON raises `ValueError`). Both tests are `@pytest.mark.integration` decorated and use `tmp_path` for file system isolation.

- **`TestBaselineStoreQualityGateRejection`** (lines 392-471): Two tests — `test_store_below_quality_threshold_should_raise_value_error` (`[0.50] * 30`, `match="quality gate"`) and `test_store_at_quality_threshold_boundary_should_succeed` (`[0.92] * 30`, asserts `record.mean_score == 0.92`). The boundary test was not requested in iteration 1 and represents additional completeness beyond the minimum. Total test count grows from ~33 to ~37.

The `module docstring` of `test_pipeline_smoke.py` was updated (lines 13-14) to list the two new scenarios explicitly: "extract_score_arrays() error paths: missing file and invalid JSON" and "BaselineStore FR-020 quality gate rejection path" — consistent with the declaration-coverage contract.

**Gaps:**

- **Dead-code block still present** (`test_pipeline_smoke.py` lines 285-286): `scores = [0.93 if i % 2 == 0 else 0.93 for i in range(30)]` (always 0.93 both branches, never different) is still followed immediately by `scores = [0.93] * 30`. The comment at line 284 now reads `# N=30, alternating to satisfy non-identical constraint, mean = 0.93` which is still incorrect — the list comprehension does not alternate. The fix was to change the comment on line 286 (`# Use a simpler uniform high-quality score list for round-trip clarity.`) acknowledging the replacement, but the dead first assignment remains unreachable code that misrepresents the test's intent.

- **`GITHUB_OUTPUT`-absent branch still unverified**: No test for `os.environ.get("GITHUB_OUTPUT")` returning `None`. The `TestEmitGhaOutputs` class in `test_layer4_pipeline.py` still covers only the set+writable and set+unwritable paths.

**Improvement Path:**

Remove the dead comprehension at `test_pipeline_smoke.py` line 285; keep only `scores = [0.93] * 30` with a corrected comment. Add `TestEmitGhaOutputsEnvVarNotSet` to `test_layer4_pipeline.py`.

---

### Internal Consistency (0.94/1.00)

**Evidence:**

Naming conventions remain consistent across all test files. All three integration test files and `conftest.py` use `from __future__ import annotations` (line 1), SPDX headers (line 1-2), and structured docstrings with `References:` blocks.

FR citations in the new classes are internally consistent with the contracts being exercised:
- `TestScoreExtractionErrorPaths` cites `WI-5B`, `CG-026`, `H-20`, `OWASP INPVAL` — all directly applicable to extraction error coverage.
- `TestBaselineStoreQualityGateRejection` cites `FR-020`, `WI-5B`, `CG-026`, `H-20` — all directly applicable.
- The `match="quality gate"` parameter in `pytest.raises` is consistent with the class docstring's claim that "a descriptive ValueError is raised."

The `pytestmark = [pytest.mark.integration]` at module level in `test_layer4_pipeline.py` (line 33) is consistent with the `@pytest.mark.integration` decorator pattern used in `test_pipeline_smoke.py` and `test_evaluator_construction.py`. Module-level declaration is the more idiomatic approach and is correctly used here.

**Gaps:**

- `TestConftestEvaluatorFixture` in `test_pipeline_smoke.py` is still not renamed to `TestDeepEvalAdapterConstruction`. This naming inconsistency with `test_evaluator_construction.py`'s `TestAdapterConstruction` persists from iteration 1. Score unchanged from iteration 1 for this sub-dimension.

- `test_conftest_evaluator_fixture_should_return_configured_adapter` (`test_pipeline_smoke.py` line 99) still does not assert `debiasing_strategy`, creating an asymmetry with `test_evaluator_construction.py` line 86 which asserts `isinstance(adapter.debiasing_strategy, DebiasingStrategy)`. The two tests are notionally covering the same construction contract; the asymmetry reduces consistency.

**Improvement Path:**

Rename `TestConftestEvaluatorFixture` to `TestDeepEvalAdapterConstruction`. Add `isinstance(adapter.debiasing_strategy, DebiasingStrategy)` assertion to `test_conftest_evaluator_fixture_should_return_configured_adapter`.

---

### Methodological Rigor (0.96/1.00)

**Evidence:**

The primary methodological gap from iteration 1 is resolved:

- `pytestmark = [pytest.mark.integration]` at module level in `test_layer4_pipeline.py` (line 33). The comment on the same line — `# H-20: 90% line coverage target. WI-5B: integration marker enforcement.` — is methodologically appropriate. This declaration applies the integration marker to all 10 test classes uniformly without requiring per-class decorator repetition.

- `monkeypatch.setattr("os.getcwd", lambda: str(tmp_path))` is applied in all three `TestPersistReport` tests (`test_persist_report_writes_json`, `test_persist_report_writes_markdown`, `test_persist_report_creates_parent_dirs`) at lines 790, 815, 840. This closes the path-validation fragility that was noted in the iteration 1 context.

All existing methodological strengths from iteration 1 persist: `tmp_path` isolation for all file-based tests, `monkeypatch.setenv/delenv` with `raising=False`, `dc_replace` for the MARGINAL branch, N=20/30 floor compliance, and mock port injection for pipeline orchestration isolation.

The two new error-path test classes (`TestScoreExtractionErrorPaths`, `TestBaselineStoreQualityGateRejection`) follow the same methodological conventions: they import the function under test at the top of the test method (for clarity of scope), use `tmp_path` for file system isolation, and use `pytest.raises` with `match=` parameters where the exception message is assertable.

The boundary condition test `test_store_at_quality_threshold_boundary_should_succeed` demonstrates methodological maturity: asserting `abs(record.mean_score - 0.92) < 1e-9` rather than `== 0.92` handles floating-point representation correctly.

**Gaps:**

- Dead-code block at `test_pipeline_smoke.py` lines 285-286 (all-same comprehension immediately overwritten). This is a minor self-documentation gap in an otherwise well-documented test, not a functional defect. Score increases from 0.93 to 0.96 because the primary methodological gap (missing `pytestmark`) is resolved.

**Improvement Path:**

Remove dead comprehension at line 285. Residual gap is minor and does not affect functional correctness or CI behavior.

---

### Evidence Quality (0.86/1.00)

**Evidence:**

Three of the five evidence gaps identified in iteration 1 are resolved:

1. **Extraction error paths closed**: `TestScoreExtractionErrorPaths` tests both `FileNotFoundError` (nonexistent path) and `ValueError` (invalid JSON). The `ValueError` test writes syntactically invalid JSON (`"{ this is not valid JSON !!!"`) and calls the extractor — this exercises the real parsing code path.

2. **FR-020 rejection path closed**: `TestBaselineStoreQualityGateRejection` tests below-threshold rejection (`[0.50] * 30`, `match="quality gate"`) and boundary acceptance (`[0.92] * 30`, asserting `mean_score == 0.92`). The `match="quality gate"` parameter verifies that the error message contains a meaningful diagnostic term — this is a stronger evidence assertion than just catching any `ValueError`.

3. **`os.getcwd` monkeypatch applied**: `TestPersistReport` tests now monkeypatch `os.getcwd` before invoking the pipeline, making the path validation logic hermetic.

**Gaps:**

- **`GITHUB_OUTPUT`-absent branch still unverified**: `TestEmitGhaOutputs` in `test_layer4_pipeline.py` tests the set+writable path (dimension_driver and key=value format tests) and the set+unwritable path (OSError swallowed). The branch where `os.environ.get("GITHUB_OUTPUT")` returns `None` is not tested. This is the smallest remaining evidence gap — the silent-skip behavior is architecturally expected, but untested.

- **`debiasing_strategy` assertion absent in `test_conftest_evaluator_fixture_should_return_configured_adapter`**: The smoke file's evaluator construction test asserts `isinstance(adapter, DeepEvalAdapter)` and `adapter.model_name` but not `isinstance(adapter.debiasing_strategy, DebiasingStrategy)`. The parallel test in `test_evaluator_construction.py` line 86 does assert this. The evidence for debiasing wiring (FR-021) is incomplete in `test_pipeline_smoke.py`.

- **Layer4Pipeline tests use mock ports**: This is an architecturally sound choice (noted in iteration 1 as acceptable), not a gap to remediate. The real serialization paths are covered by other test classes. This does not reduce the score further in iteration 2.

**Improvement Path:**

Add `TestEmitGhaOutputsEnvVarNotSet` to `test_layer4_pipeline.py`. Add `debiasing_strategy` assertion to `test_conftest_evaluator_fixture_should_return_configured_adapter`.

---

### Actionability (0.92/1.00)

**Evidence:**

The `pytestmark` fix directly improves actionability for CI engineers: `uv run pytest -m integration` now captures all tests in `test_layer4_pipeline.py`, which was the critical CI gap. This is a high-actionability improvement.

The new error-path tests use actionable assertion diagnostics:
- `test_extract_score_arrays_missing_file_should_raise_file_not_found`: uses `pytest.raises(FileNotFoundError)` — the exception type is itself the diagnostic.
- `test_store_below_quality_threshold_should_raise_value_error`: uses `pytest.raises(ValueError, match="quality gate")` — the `match` parameter means that if the gate string is removed from the error message, the test fails with a clear message identifying the regex mismatch.

Module docstring of `test_pipeline_smoke.py` was updated to enumerate all six test scenarios, improving navigability.

**Gaps:**

- Dead-code block at lines 285-286 of `test_pipeline_smoke.py` still reduces actionability as living documentation. A developer reading the test sees `scores = [0.93 if i % 2 == 0 else 0.93 for i in range(30)]` (always 0.93, never alternating) followed by `scores = [0.93] * 30`. The comment sequence (lines 284 and 286) provides some clarification but the dead assignment remains confusing.

- `test_layer4_pipeline_smoke_with_score_arrays` in `test_pipeline_smoke.py` still only asserts `isinstance(result, RegressionResult)`. The docstring does not note that field-level assertions are delegated to `test_layer4_pipeline.py`. This is a minor documentation gap noted in iteration 1 that was not addressed.

**Improvement Path:**

Remove dead comprehension at line 285. Add one-sentence delegation note to `test_layer4_pipeline_smoke_with_score_arrays` docstring.

---

### Traceability (0.93/1.00)

**Evidence:**

Traceability improved across two files:

- `test_layer4_pipeline.py` module docstring now includes `WI-5B: FIX-WI5-B integration marker enforcement` (line 22) — closes the WI-5B reference gap for this file. `H-20` was already present (line 21). `FR-020` is NOT explicitly listed in `test_layer4_pipeline.py`'s References section (FR-018, FR-019, H-20, WI-5B, and `behavioral-contracts.md Section D.6` are present). This is acceptable since `test_layer4_pipeline.py` does not directly test the FR-020 quality gate.

- `test_pipeline_smoke.py` module docstring now includes `WI-5B` (line 27), `CG-026` (line 27), and explicitly lists `FR-020` (line 24). The docstring now lists all six referenced specifications including the two new ones. The new test classes also carry their own `References:` blocks pointing to `WI-5B`, `CG-026`, `FR-020`, and `OWASP INPVAL`.

SPDX headers and copyright remain present in all files. `@pytest.mark.integration` registered in `pyproject.toml` — traceability chain from test to pyproject is intact.

**Gaps:**

- `WI-5B` reference is absent from `test_evaluator_construction.py` module docstring. This file was not modified in iteration 2 and retains its iteration 1 traceability. Since the evaluator construction tests were not in scope for FIX-WI5-B, this is a lower-priority gap.

- `WI-5B` and `CG-026` references absent from `conftest.py`. The conftest was not modified in iteration 2. Its traceability is adequate for its scope (FR-004, FR-006, FR-021 cited).

- `CG-026` is absent from `test_layer4_pipeline.py`'s References section. This was noted in iteration 1 and was not added. The file cites H-20 (which covers coverage targets) but not the specific constraint identifier `CG-026`.

**Improvement Path:**

Add `WI-5B` near the module header of `test_evaluator_construction.py`. Add `CG-026` to the References section of `test_layer4_pipeline.py`.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.86 | 0.90 | Add `TestEmitGhaOutputsEnvVarNotSet` to `test_layer4_pipeline.py`: use `monkeypatch.delenv("GITHUB_OUTPUT", raising=False)`, run `pipeline.run(...)`, assert no exception and exit code in (0, 1, 2). Closes silent-skip branch. |
| 2 | Completeness / Methodological Rigor | 0.93 | 0.96 | Remove dead comprehension at `test_pipeline_smoke.py` line 285 (`scores = [0.93 if i % 2 == 0 else 0.93 for i in range(30)]`). Keep only `scores = [0.93] * 30` with corrected comment. |
| 3 | Internal Consistency / Evidence Quality | 0.94 / 0.86 | 0.96 / 0.88 | Add `isinstance(adapter.debiasing_strategy, DebiasingStrategy)` assertion to `test_conftest_evaluator_fixture_should_return_configured_adapter` in `test_pipeline_smoke.py`. Closes asymmetry with `test_evaluator_construction.py` line 86. |
| 4 | Traceability | 0.93 | 0.96 | Add `# WI-5B: gap-closure-20260307-001` near the module header of `test_evaluator_construction.py`. Add `CG-026` to the References section of `test_layer4_pipeline.py`. |
| 5 | Internal Consistency | 0.94 | 0.96 | Rename `TestConftestEvaluatorFixture` to `TestDeepEvalAdapterConstruction` for naming consistency with `TestAdapterConstruction` in `test_evaluator_construction.py`. |
| 6 | Actionability | 0.92 | 0.94 | Add one-sentence note to `test_layer4_pipeline_smoke_with_score_arrays` docstring: "Field-level assertions (classification, p-value, effect size) are delegated to `test_layer4_pipeline.py`." |

---

## Leniency Bias Check
- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific file names and line numbers
- [x] Uncertain scores resolved downward: Evidence Quality debated between 0.86 and 0.89 — resolved to 0.86 given two remaining gaps (`GITHUB_OUTPUT`-absent branch and `debiasing_strategy` assertion); Completeness debated between 0.93 and 0.95 — resolved to 0.93 given dead-code block still present and `GITHUB_OUTPUT`-absent branch missing
- [x] Calibration check: iteration 2 of a C2 test suite that addressed 4 of 8 iteration-1 recommendations. 0.93-0.96 range for improved dimensions is consistent with the 0.85 calibration anchor (strong work with minor refinements) upgraded toward 0.92 (genuinely excellent). The composite at 0.924 reflects one dimension (Evidence Quality at 0.86) still holding the composite near-threshold.
- [x] No dimension scored above 0.96 without exceptional evidence: Methodological Rigor at 0.96 is justified by closure of the primary structural gap (pytestmark) plus all six identified methodological patterns confirmed intact; Internal Consistency at 0.94 reflects two persistent minor inconsistencies (rename, debiasing_strategy) that prevent 0.96

---

## Iteration-over-Iteration Delta

| Dimension | Iter 1 Score | Iter 2 Score | Delta | Driver |
|-----------|-------------|-------------|-------|--------|
| Completeness | 0.88 | 0.93 | +0.05 | `TestScoreExtractionErrorPaths` and `TestBaselineStoreQualityGateRejection` added; dead-code block remains |
| Internal Consistency | 0.94 | 0.94 | 0.00 | No regressions; rename and debiasing_strategy gaps persist |
| Methodological Rigor | 0.93 | 0.96 | +0.03 | `pytestmark` module-level declaration closes primary gap |
| Evidence Quality | 0.78 | 0.86 | +0.08 | Error paths and FR-020 rejection added; 2 gaps remain |
| Actionability | 0.91 | 0.92 | +0.01 | pytestmark improves CI coverage; dead-code minor drag |
| Traceability | 0.92 | 0.93 | +0.01 | WI-5B added to 2 files; evaluator_construction and conftest unchanged |
| **Composite** | **0.896** | **0.924** | **+0.028** | **REVISE → PASS** |

---

## Session Context (Handoff Schema)

```yaml
verdict: PASS
composite_score: 0.924
threshold: 0.92
weakest_dimension: evidence_quality
weakest_score: 0.86
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Add TestEmitGhaOutputsEnvVarNotSet: verify silent-skip branch when GITHUB_OUTPUT is absent (monkeypatch.delenv)"
  - "Remove dead comprehension at test_pipeline_smoke.py line 285; keep only scores = [0.93] * 30"
  - "Add debiasing_strategy assertion to test_conftest_evaluator_fixture_should_return_configured_adapter"
  - "Add WI-5B reference to test_evaluator_construction.py module docstring"
  - "Add CG-026 to test_layer4_pipeline.py References section"
  - "Rename TestConftestEvaluatorFixture to TestDeepEvalAdapterConstruction"
  - "Add field-level delegation note to test_layer4_pipeline_smoke_with_score_arrays docstring"
```
