# Quality Score Report: WI5-B — Integration Tests (All 3 Files, Iteration 1)

## L0 Executive Summary
**Score:** 0.896/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.78)
**One-line assessment:** A substantially expanded integration suite (~33 tests, 3 files, ~1,545 lines) covers all major pipeline contracts with strong hermetic isolation, precise FR/CG traceability, and deep Layer4Pipeline branch coverage, but fails to test extraction error paths (FileNotFoundError, ValueError), the FR-020 baseline quality-gate rejection path, and the GHA output GITHUB_OUTPUT environment-variable-absent branch; these evidence gaps prevent Evidence Quality from reaching 0.9+ and hold the composite below threshold.

---

## Scoring Context
- **Deliverable:** `tests/prompt-regression/integration/` (3 files: `test_pipeline_smoke.py`, `test_evaluator_construction.py`, `test_layer4_pipeline.py`) + `tests/prompt-regression/conftest.py`
- **Deliverable Type:** Code (integration test suite)
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 1 (first review of full 3-file scope)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.896 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | All 4 original scenarios plus 10 Layer4Pipeline test classes; extraction error paths and FR-020 rejection path absent; dead-code block in store round-trip. |
| Internal Consistency | 0.20 | 0.94 | 0.188 | Naming conventions, docstring references, and FR citations are coherent across all 3 files and ~33 tests; one mild name mismatch in TestConftestEvaluatorFixture. |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | Correct markers, monkeypatch hermeticity, tmp_path isolation, mock port injection for Layer4Pipeline, N=20/30 floors respected, dc_replace used to reach MARGINAL branch. |
| Evidence Quality | 0.15 | 0.78 | 0.117 | Real module wiring confirmed in smoke + evaluator files; Layer4Pipeline tests use mock ports (correct but reduces end-to-end depth); extraction error paths and FR-020 gate rejection untested; GITHUB_OUTPUT-absent branch not verified. |
| Actionability | 0.15 | 0.91 | 0.137 | Diagnostic assertion messages throughout; class docstrings state scope and isolation contract; markers enable selective CI execution; specific improvement path is clear. |
| Traceability | 0.10 | 0.92 | 0.092 | SPDX/copyright present; FR-004/009/014/015/017/018/019/020/021/CG-005 cited; behavioral-contracts.md Section D.6 cited; @pytest.mark.integration registered. |
| **TOTAL** | **1.00** | | **0.896** | |

---

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence:**

The module docstring of `test_pipeline_smoke.py` (lines 6–14) declares four structural integration scenarios; all four are implemented:

1. **Evaluator fixture construction** — `TestConftestEvaluatorFixture.test_conftest_evaluator_fixture_should_return_configured_adapter` (`test_pipeline_smoke.py` line 95). Constructs `DeepEvalAdapter` with monkeypatched key and asserts `isinstance` and `model_name` attribute.

2. **Score array extraction** — `TestScoreArrayExtractionFromSampleData.test_score_array_extraction_from_sample_data` (`test_pipeline_smoke.py` line 144). Writes minimal promptfoo JSON to `tmp_path`, calls `extract_score_arrays()`, asserts head/base split for "composite_score".

3. **Layer 4 pipeline smoke** — `TestLayer4PipelineSmokeWithScoreArrays.test_layer4_pipeline_smoke_with_score_arrays` (`test_pipeline_smoke.py` line 198). Calls `compare_versions()` with N=20 alternating arrays and asserts `isinstance(result, RegressionResult)`.

4. **BaselineStore round-trip** — `TestBaselineStoreRoundtrip.test_baseline_store_roundtrip` (`test_pipeline_smoke.py` line 259). Stores N=30 scores, retrieves them, asserts `version_key`, `agent_id`, `metric_id`, `scores`, and `baseline_status == "active"`.

5. **Adapter construction** — `TestAdapterConstruction` in `test_evaluator_construction.py` (lines 45–124): two tests covering the success path (with key) and failure path (without key, `EvaluationConfigError` raised and message contains `"ANTHROPIC_API_KEY"`).

6. **Layer4Pipeline full coverage** — `test_layer4_pipeline.py` provides ~25 tests across 10 classes: `TestPipelineSmokeMode` (5 tests: exit codes, delegation, skip stats, default violations), `TestPipelineFullMode` (7 tests: single/multi metric, NO_REGRESSION/REGRESSION/MARGINAL/IMPROVEMENT exit codes, Bonferroni routing), `TestPipelineInsufficientSamples` (3 tests: propagation, ValueError subclass, smoke ignores arrays), `TestPipelineRunSingleMetric` (2 tests: return tuple, insufficient samples), `TestExitCodeMapping` (3 tests: all three MergeDecision values), `TestAggregateMultiMetric` (4 tests: worst-case REGRESSION, no blocking, dimension driver, invariant), `TestPipelineLazyImport` (1 test: constructor without report_generator), `TestPersistReport` (3 tests: JSON write, Markdown write, parent-dir creation), `TestEmitGhaOutputs` (3 tests: dimension_driver branch, key=value format, OSError swallowed), `TestAggregateMultiMetricMarginalDriver` (1 test: MARGINAL branch with dc_replace override).

**Gaps:**

- **Extraction error paths** (`test_pipeline_smoke.py`): `extract_score_arrays()` is tested only in the happy path (one head + one base entry). No test exercises `FileNotFoundError` (nonexistent path) or `ValueError` (malformed JSON, wrong score range, missing metric key). The CG-008 adapter contract requires these error surfaces to be tested at the integration level.

- **FR-020 quality gate rejection** (`test_pipeline_smoke.py`): `TestBaselineStoreRoundtrip` uses `[0.93] * 30` (mean = 0.93, above the 0.92 gate). No test attempts `store()` with `[0.50] * 30` to verify the gate rejects or flags below-threshold baselines. The rejection path is untested.

- **Dead-code block** (`test_pipeline_smoke.py` lines 281–283): `scores = [0.93 if i % 2 == 0 else 0.93 for i in range(30)]` (always-0.93 both branches) is immediately overwritten by `scores = [0.93] * 30`. The comment "alternating to satisfy non-identical constraint" is incorrect for this test (the round-trip does not call `compare_versions()`). This reduces confidence in the test's design rationale.

- **`GITHUB_OUTPUT` absent branch** (`test_layer4_pipeline.py`): `TestEmitGhaOutputs` tests (a) when `GITHUB_OUTPUT` is set with a writable path, (b) when set with an unwritable path (OSError swallowed). No test verifies the branch where `GITHUB_OUTPUT` is not set at all (i.e., `os.environ.get("GITHUB_OUTPUT")` returns `None`). This branch presumably skips GHA output silently; its behaviour is unverified.

**Improvement Path:**

Add `TestScoreExtractionErrorPaths` with two tests for `FileNotFoundError` and structural `ValueError`. Add `TestBaselineStoreQualityGateRejection`. Remove or correct dead-code block. Add a smoke-mode `TestEmitGhaOutputsNotSet` test for missing `GITHUB_OUTPUT`.

---

### Internal Consistency (0.94/1.00)

**Evidence:**

Naming is consistent across all 33 tests: test method names follow `test_{what}_{expected_outcome}` or `test_{what}_{condition}` conventions throughout. All three files use `from __future__ import annotations` (line 1 of each). SPDX and copyright headers are present in all three test files and in `conftest.py`.

FR references in docstrings match the contracts being exercised: `test_layer4_pipeline.py` cites `FR-018` (exit codes), `FR-019` (one-way dependency rule), and `behavioral-contracts.md Section D.6` (ComparisonReport schema) — all of which are verifiable against the source modules.

The `TestExitCodeMapping` class (lines 574–612 in `test_layer4_pipeline.py`) tests `Layer4Pipeline._exit_code()` in isolation with three cases, matching the FR-018 contract exactly: BLOCK→1, ALLOW_WITH_WARNING→2, ALLOW→0.

The `TestAggregateMultiMetricMarginalDriver` test (line 983) uses `dataclasses.replace` to construct a `MARGINAL` result and asserts `multi.dimension_driver == "completeness"`, which is internally consistent: the dc_replace forces the classification branch; the aggregate must propagate the driver.

The mock factories `_make_comparison_report()` and `_make_smoke_report()` (lines 55–99) use realistic version keys (`"aaa" * 13 + "a:..."`) that conform to the `{7-40 hex}:{path}` FR-004 format (39 + 1 characters, valid hex).

**Gaps:**

- `TestConftestEvaluatorFixture` (`test_pipeline_smoke.py` line 87): The class name says "Conftest Evaluator Fixture" but the test constructs `DeepEvalAdapter` directly without using the `evaluator` fixture from `conftest.py`. The fixture under test is the adapter construction pattern used in `conftest.py`, not the conftest fixture itself. The name is mildly misleading (the corresponding test in `test_evaluator_construction.py` is named `TestAdapterConstruction`, which is more accurate).

- `test_pipeline_full_mode_no_bonferroni_uses_single_path` (`test_layer4_pipeline.py` line 412): The test passes `apply_bonferroni=False` on a two-metric `metric_scores` dict and asserts `from_single_metric.assert_called_once()`. The comment says "first metric extracted via `next(iter(...))`". If this is the actual code path, the fact that the metric chosen is implementation-order-dependent (dict iteration order) is not asserted — the test could silently succeed even if the wrong metric was selected. This is a minor consistency gap between the test's intent and its assertion scope.

**Improvement Path:**

Rename `TestConftestEvaluatorFixture` to `TestDeepEvalAdapterConstruction` (consistent with the `test_evaluator_construction.py` nomenclature). Add an assertion to `test_pipeline_full_mode_no_bonferroni_uses_single_path` capturing which metric was selected, or add a comment acknowledging implementation-order dependency.

---

### Methodological Rigor (0.93/1.00)

**Evidence:**

- `@pytest.mark.integration` applied at class level on all test classes in `test_pipeline_smoke.py` and `test_evaluator_construction.py`. In `test_layer4_pipeline.py`, the marker is NOT present (none of the 10 test classes carry `@pytest.mark.integration`). This is a notable structural choice — the file is not marked as integration despite testing the full `Layer4Pipeline` with injected mock ports. It may run under the default suite rather than the integration marker. This is not necessarily wrong (mock-injected tests may be considered unit-level by the project convention), but it is an inconsistency across the three integration test files.

- `monkeypatch.setenv / .delenv` used correctly in both files requiring env var manipulation. `raising=False` used appropriately on `delenv` to prevent test failure when the var was not set.

- `tmp_path` fixture used for file-based tests in all appropriate cases: score-array extraction (file write), BaselineStore round-trip (directory isolation), `_persist_report` tests (JSON/Markdown output), GHA output tests (github_output.txt).

- Mock port injection for `Layer4Pipeline` is methodologically sound: `mock_store` and `mock_generator` satisfy `BaselinePersistencePort` and `ReportOutputPort` interfaces via `MagicMock`. This correctly isolates the pipeline orchestration logic from filesystem and LLM dependencies, matching the test file's stated scope.

- N=20 floor for Wilcoxon respected in all Layer 4 full-mode tests: `_make_scores(30)` produces 30 entries; the alternating pattern (`value if i % 2 == 0 else value - 0.02`) ensures variation, avoiding `InvalidScoreArrayError`.

- `dc_replace` (`dataclasses.replace`) used in `TestAggregateMultiMetricMarginalDriver` (line 1008) to force a `MARGINAL` classification — a sound technique for exercising hard-to-reach statistical branches without fragile score engineering.

- `TestPipelineLazyImport` (line 754) explicitly names the coverage target: "lines 102-104 (lazy import branch) in layer4_stats.py". This level of specificity demonstrates the test was written with coverage analysis in mind.

- `TestPersistReport` tests use `monkeypatch.setattr("os.getcwd", ...)` to control the working directory — appropriate for path-relative tests.

**Gaps:**

- `test_layer4_pipeline.py` lacks `@pytest.mark.integration` on any test class. Given that the file is located in the `integration/` directory and tests a production module by name (`Layer4Pipeline`), the absence of the marker may cause these tests to run in the wrong CI gate. The `test_pipeline_smoke.py` and `test_evaluator_construction.py` both carry the marker; the omission in `test_layer4_pipeline.py` is inconsistent.

- `test_baseline_store_roundtrip` (lines 281–283): the dead-code alternating comprehension assigns to `scores` then immediately reassigns it. The comment "alternating to satisfy non-identical constraint" is methodologically incorrect for this test (the store round-trip does not call `compare_versions()`). Minor but reduces rigor of the test's self-documentation.

**Improvement Path:**

Add `@pytest.mark.integration` to all 10 test classes in `test_layer4_pipeline.py` (or add it at module level with a `pytestmark` declaration). Remove the dead-code block at `test_baseline_store_roundtrip` lines 281–283.

---

### Evidence Quality (0.78/1.00)

**Evidence:**

The suite demonstrates meaningful integration evidence in several areas:

- `extract_score_arrays()` called against a real JSON file written to disk (`test_pipeline_smoke.py` line 166) — real parsing logic exercised, not mocked.
- `compare_versions()` called with real score arrays (N=20 alternating) — actual Wilcoxon computation runs (`test_pipeline_smoke.py` line 229).
- `BaselineStore.store()` and `.retrieve()` called against a real `tmp_path` directory — real JSON serialization/deserialization exercised (`test_pipeline_smoke.py` lines 285–298).
- `DeepEvalAdapter.__post_init__` exercised in both success and failure paths across two test files.
- `Layer4Pipeline._exit_code()`, `Layer4Pipeline._aggregate_multi_metric()`, and `Layer4Pipeline.run()` all exercised against real `compare_versions()` return values in `TestAggregateMultiMetric` and `TestAggregateMultiMetricMarginalDriver` — not mocked.
- GHA output key=value format verified by regex pattern (`kv_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=.*$")`) against all lines, and the three required keys (`verdict`, `merge_recommendation`, `agent`) are asserted by name (`test_layer4_pipeline.py` lines 930–943).

**Gaps:**

- **Extraction error paths absent**: `extract_score_arrays()` is only tested in the happy path. No test verifies that a missing file raises `FileNotFoundError`, that structurally invalid JSON raises `ValueError`, or that out-of-range scores are rejected. These are observable integration contracts (the function's I/O boundary with the filesystem and the promptfoo schema); their absence is a meaningful evidence gap.

- **FR-020 quality gate rejection untested**: `BaselineStore.store()` with `[0.93] * 30` (mean 0.93) always passes the gate. There is no test confirming what happens with a below-threshold mean (e.g., `[0.50] * 30`). The FR-020 rejection contract is unverified at the integration level.

- **Layer4Pipeline tests use mock ports**: `TestPipelineSmokeMode`, `TestPipelineFullMode`, `TestPipelineInsufficientSamples`, `TestPipelineRunSingleMetric`, `TestExitCodeMapping`, `TestPersistReport`, `TestEmitGhaOutputs`, and `TestPipelineLazyImport` all inject `MagicMock` for `BaselinePersistencePort` and `ReportOutputPort`. This is architecturally correct for testing pipeline orchestration logic in isolation, but it means the actual report-generation wiring (real `ReportGenerator` serializing a real `ComparisonReport` to JSON/Markdown) is not exercised at the integration level. The real serialization path is covered only by `TestPipelineLazyImport` (which constructs the pipeline without injection but uses smoke mode), and by `TestAggregateMultiMetric` / `TestAggregateMultiMetricMarginalDriver` (which call `compare_versions()` directly but not `report_generator.from_multi_metric()`).

- **GITHUB_OUTPUT absent branch unverified**: `os.environ.get("GITHUB_OUTPUT")` returning `None` is not tested. The OSError branch (unwritable path) is tested, but the "env var not set at all" branch is not.

- **`debiasing_strategy` attribute not asserted in `test_conftest_evaluator_fixture_should_return_configured_adapter`** (`test_pipeline_smoke.py` line 95): `adapter.model_name` is asserted but `adapter.debiasing_strategy` is not, creating an asymmetry with `test_evaluator_construction.py` line 86 which does assert `isinstance(adapter.debiasing_strategy, DebiasingStrategy)`.

**Improvement Path:**

Add `TestScoreExtractionErrorPaths` (FileNotFoundError, ValueError). Add `TestBaselineStoreQualityGateRejection` (mean < 0.92). Add a test for missing `GITHUB_OUTPUT`. Add `debiasing_strategy` assertion to `test_conftest_evaluator_fixture_should_return_configured_adapter`.

---

### Actionability (0.91/1.00)

**Evidence:**

Assertion messages throughout all 33 tests embed expected vs. actual values in f-strings. Examples:

- `test_pipeline_smoke.py` line 175: `f"Head score array mismatch. Expected [0.85], got {head_scores}"`
- `test_pipeline_smoke.py` line 125: `f"model_name attribute must match the constructor argument; got {adapter.model_name!r}"`
- `test_layer4_pipeline.py` line 939: `"GHA output missing required key 'verdict'"`
- `test_layer4_pipeline.py` line 301: `(f"version_key mismatch: stored=..., retrieved=...")` pattern

Class-level docstrings clearly state scope and constraints (e.g., "No real BaselineStore or ReportGenerator is instantiated" at `test_layer4_pipeline.py` line 13). The `@pytest.mark.integration` marker on `test_pipeline_smoke.py` and `test_evaluator_construction.py` enables selective CI execution.

Module-level "References" sections in all three files connect tests to feature requirements, enabling a developer to determine which test covers which FR without reading each test body.

The `TestPipelineLazyImport` docstring (lines 747–751) explicitly identifies the coverage target lines: "Covers lines 102-104 (lazy import branch) in layer4_stats.py." This level of specificity enables a developer to verify coverage in a single step.

Similarly, `TestPersistReport` (lines 771–773) cites "lines 408-410, 413-417" and `TestEmitGhaOutputs` (lines 858–860) cites "lines 440, 444-449" — systematically mapping test intent to implementation lines.

**Gaps:**

- `test_layer4_pipeline_smoke_with_score_arrays` (`test_pipeline_smoke.py` line 239): asserts only `isinstance(result, RegressionResult)`. The docstring does not explain that field-level assertions are intentionally deferred to `test_layer4_pipeline.py`. A developer reading this in isolation may wonder whether the field assertions are missing by omission.

- `test_layer4_pipeline.py` lacks `@pytest.mark.integration` (as noted under Methodological Rigor). This reduces actionability for CI engineers who run `uv run pytest -m integration` expecting to capture all integration tests.

- The dead-code block at `test_pipeline_smoke.py` lines 281–283 reduces actionability of the test as living documentation: a developer reading it to understand the test's intent is misled by the incorrect comment about "alternating" arrays.

**Improvement Path:**

Add a one-sentence note to `test_layer4_pipeline_smoke_with_score_arrays` docstring: "Field-level assertions (classification, p-value, effect size) are delegated to `test_layer4_pipeline.py`." Add `@pytest.mark.integration` to `test_layer4_pipeline.py`. Remove dead-code block.

---

### Traceability (0.92/1.00)

**Evidence:**

- `# SPDX-License-Identifier: Apache-2.0` and `# Copyright (c) 2026 Victor Lau` present in all three integration test files and in `conftest.py` (lines 1–2 of each).

- Module-level docstrings cite the following FR and CG identifiers across the three files:
  - `test_pipeline_smoke.py`: FR-004, FR-009, FR-014, FR-020, H-11, H-20, OWASP INPVAL
  - `test_evaluator_construction.py`: FR-006, FR-021, CG-005, OWASP AUTHN, H-11, H-20
  - `test_layer4_pipeline.py`: FR-018, FR-019, H-20, behavioral-contracts.md Section D.6

- Per-test docstrings cite specific FR references governing each contract. For example:
  - `test_baseline_store_roundtrip` (line 260): "FR-020: BaselineStore quality gate (mean >= 0.92)"
  - `test_emit_gha_outputs_writes_to_github_output_file` (line 897): "FR-018: GitHub Actions requires strict key=value line format"
  - `test_pipeline_insufficient_samples_error_is_value_error_subclass` (line 474): "FR-014: InsufficientSamplesError inherits from ValueError"

- `_VERSION_KEY` constant (line 78 of `test_pipeline_smoke.py`): comment `# Format: "{7-40 lowercase hex}:{file_path}" per FR-004 / CG-027` traces the fixture format to its specification.

- `@pytest.mark.integration` registered in `pyproject.toml` (line 128: `"integration: marks integration tests (external dependencies)"`), creating a traceable test classification chain from test to pyproject.

- `behavioral-contracts.md Section D.6` cited in `test_layer4_pipeline.py` line 22 — the only file that references the behavioral contracts document; this is meaningful given the file tests `ComparisonReport` schema compliance.

**Gaps:**

- No reference to the gap-closure work item hierarchy (WI-5B, `gap-closure-20260307-001`) in any file header. The prior score for the 2-file scope noted this same gap; `test_layer4_pipeline.py` also lacks this traceability link.

- `_SAMPLE_PROMPTFOO_RESULTS` constant (line 45 of `test_pipeline_smoke.py`): documents the promptfoo structure inline but does not cite the promptfoo schema version or the behavioral contracts document section that defines the expected JSON shape (only `test_layer4_pipeline.py` cites `behavioral-contracts.md`).

- `test_layer4_pipeline.py` does not cite CG-026 (the 90% line coverage requirement), despite the fact that the test file's stated purpose includes driving coverage of `layer4_stats.py` branches. The prior files cite H-20.

**Improvement Path:**

Add `# WI-5B: gap-closure-20260307-001` near the module header of all three test files. Add a `behavioral-contracts.md` reference near `_SAMPLE_PROMPTFOO_RESULTS` in `test_pipeline_smoke.py`. Add H-20/CG-026 to the References section of `test_layer4_pipeline.py`.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.78 | 0.88 | Add `TestScoreExtractionErrorPaths` in `test_pipeline_smoke.py` with two tests: (a) `extract_score_arrays(nonexistent_path)` raises `FileNotFoundError`; (b) `extract_score_arrays(invalid_json_file)` raises `ValueError`. Closes the CG-008 observable-contract gap. Estimated composite impact: +0.016. |
| 2 | Evidence Quality | 0.78 | 0.88 | Add `TestBaselineStoreQualityGateRejection` in `test_pipeline_smoke.py` with `scores=[0.50]*30` and verify the FR-020 rejection contract (exception or status field). |
| 3 | Methodological Rigor | 0.93 | 0.96 | Add `@pytest.mark.integration` to all 10 test classes in `test_layer4_pipeline.py` (or use a module-level `pytestmark = pytest.mark.integration` declaration). This aligns the file with the project's integration marker convention. |
| 4 | Completeness | 0.88 | 0.93 | Remove dead-code block at `test_pipeline_smoke.py` lines 281–283. Replace the overwritten comprehension and its incorrect comment with a single `scores = [0.93] * 30` with corrected comment: "All-identical scores satisfy FR-020 quality gate; variation not required for round-trip." |
| 5 | Evidence Quality | 0.78 | 0.82 | Add `TestEmitGhaOutputsEnvVarNotSet` in `test_layer4_pipeline.py`: run `pipeline.run(...)` without setting `GITHUB_OUTPUT` (use `monkeypatch.delenv("GITHUB_OUTPUT", raising=False)`) and assert the call completes without raising. Closes the silent-skip branch. |
| 6 | Internal Consistency | 0.94 | 0.96 | Rename `TestConftestEvaluatorFixture` to `TestDeepEvalAdapterConstruction` (consistent with the parallel `test_evaluator_construction.py` naming). |
| 7 | Traceability | 0.92 | 0.95 | Add `# WI-5B: gap-closure-20260307-001` near the module header of all three test files. Add H-20/CG-026 to the References section of `test_layer4_pipeline.py` module docstring. |
| 8 | Actionability | 0.91 | 0.93 | Add one-sentence note to `test_layer4_pipeline_smoke_with_score_arrays` docstring: "Field-level assertions (classification, p-value, effect size) are delegated to `test_layer4_pipeline.py`." |

---

## Leniency Bias Check
- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific file names and line numbers
- [x] Uncertain scores resolved downward: Evidence Quality debated between 0.78 and 0.82 — resolved to 0.78 given three missing test areas (extraction errors, FR-020 rejection, GITHUB_OUTPUT absent); Completeness debated between 0.88 and 0.91 — resolved to 0.88 given dead-code and two missing negative paths
- [x] First-draft calibration considered: iteration 1 of full 3-file scope; 0.78 for Evidence Quality is consistent with good but incomplete first-draft coverage (real modules exercised in some paths, mocked in others, key error paths absent)
- [x] No dimension scored above 0.95 without exceptional evidence: Internal Consistency at 0.94 is justified by zero contradictions found across 33 tests, 3 files, ~1,545 lines; Methodological Rigor at 0.93 is justified by consistent use of established patterns (monkeypatch, tmp_path, dc_replace, mock port injection) across all files

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.896
threshold: 0.92
weakest_dimension: evidence_quality
weakest_score: 0.78
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Add TestScoreExtractionErrorPaths: FileNotFoundError and ValueError from extract_score_arrays() — closes CG-008 observable contract gap"
  - "Add TestBaselineStoreQualityGateRejection: scores=[0.50]*30 to verify FR-020 rejection path"
  - "Add @pytest.mark.integration to all test classes in test_layer4_pipeline.py (or use pytestmark at module level)"
  - "Remove dead-code block at test_pipeline_smoke.py lines 281-283 and correct comment"
  - "Add TestEmitGhaOutputsEnvVarNotSet: verify silent-skip branch when GITHUB_OUTPUT is absent"
  - "Rename TestConftestEvaluatorFixture to TestDeepEvalAdapterConstruction"
  - "Add WI-5B gap-closure-20260307-001 reference near module header of all three test files"
  - "Add note to test_layer4_pipeline_smoke_with_score_arrays docstring delegating field assertions to test_layer4_pipeline.py"
```
