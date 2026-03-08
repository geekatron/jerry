# Quality Score Report: CG-008 Promptfoo Score Extractor (Re-score, Iteration 2)

## L0 Executive Summary
**Score:** 0.870/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Actionability (0.78)
**One-line assessment:** The 14-unit-test addition materially closes the Evidence Quality gap from 0.60 to 0.85, lifting the composite from 0.801 to 0.870, but three uncovered edge cases (bool score, uppercase CANDIDATE, missing __version__ key), the unresolved bool subclass methodological gap in the implementation, and the silent empty-result return keep the deliverable below the 0.92 threshold; targeted fixes to these three remaining items would push the composite above 0.92.

---

## Scoring Context
- **Deliverable:** `jerry/testing/extraction/promptfoo_extractor.py`, `jerry/testing/extraction/__init__.py`, `tests/prompt-regression/unit/test_promptfoo_extractor.py`
- **Deliverable Type:** Code
- **Criticality Level:** C2 (Standard — adapter layer addition, reversible in <1 day)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.801 (iteration 1, 2026-03-07)
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 2

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.870 |
| **Threshold** | 0.92 (H-13) |
| **Delta from Prior** | +0.069 (0.801 → 0.870) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | Implementation unchanged; all 8 CG-008 requirements present; empty-result-list warning gap persists (no WARNING emitted when result_list is []). |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Tests confirm the module docstring contracts (version discrimination, metric precedence, error types) match implementation; no contradictions. |
| Methodological Rigor | 0.20 | 0.88 | 0.176 | Bool subclass gap unresolved in implementation (isinstance(True, (int, float)) passes); no test covers this case; test methodology itself is sound (tmp_path, caplog, class organization). |
| Evidence Quality | 0.15 | 0.85 | 0.128 | 14 unit tests cover 4 error paths, 5 happy-path variants, 2 out-of-range skip cases, 3 metric-resolution cases; three edge cases remain untested: bool score, uppercase CANDIDATE, missing __version__ key. |
| Actionability | 0.15 | 0.78 | 0.117 | Tests provide runnable validation and fixture helpers (_make_result, _write_promptfoo_json); silent {} return on empty result_list remains; no sample fixture JSON file. |
| Traceability | 0.10 | 0.85 | 0.085 | Test file references CG-008 and CG-021 explicitly; SPDX and copyright present; implementation still lacks cross-reference to behavioral contracts or STORY-036-002. |
| **TOTAL** | **1.00** | | **0.870** | |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**

The implementation is unchanged from iteration 1. All 8 CG-008 functional requirements remain fully implemented in `promptfoo_extractor.py`:

1. `extract_score_arrays(promptfoo_json_path: Path) -> dict[str, tuple[ScoreArray, ScoreArray]]` — exact signature at lines 94-96.
2. Per-metric `(head_scores, base_scores)` tuple output via `defaultdict(list)` accumulation at lines 199-298.
3. Version discrimination via `_VERSION_VAR_KEY = "__version__"` (line 83) and `_HEAD_VERSION_VALUES = frozenset({"head", "candidate"})` (line 86).
4. Three-step metric name resolution via `_resolve_metric_name` (lines 328-368).
5. `FileNotFoundError` for missing file at lines 161-163.
6. `ValueError` for invalid JSON and missing `results.results` structure at lines 170-194.
7. `WARNING`-level logs for malformed entries at lines 204, 238, 247, 261, 272, 286, 291.
8. H-07, H-10, H-11 compliance documented and implemented throughout.

The test file's header confirms intent to reach 90% line coverage (H-20 reference). The 14 tests cover the primary execution paths. However, coverage of the private helper `_resolve_metric_name` via indirect calls does not test the exact lines for the debug log paths within that helper.

**Gaps:**

- Empty `result_list` case: function returns `{}` with only an INFO log ("0 result entries") — no WARNING. This is a persistent gap from iteration 1. The test `test_empty_results_list_should_return_empty_dict` validates the `{}` return but does not assert a WARNING log, effectively confirming the absence of a warning as accepted behavior rather than requiring one.
- The 90% line coverage claim in the test docstring (`H-20: BDD test-first (90% line coverage target)`) is stated as a target, not a measured result. No coverage report is referenced.

**Improvement Path:**

Add `logger.warning("extract_score_arrays: zero result entries in %s — file may be empty or stale.", promptfoo_json_path.name)` after the structural validation block. This closes the empty-result gap and would raise Completeness to 0.93.

---

### Internal Consistency (0.92/1.00)

**Evidence:**

The 14 new tests act as a consistency verification suite: they test the exact behavioral contracts stated in the module docstring and confirm the implementation matches the documentation.

Specific consistency validations the tests perform:
- `test_valid_json_with_head_and_base_should_return_correct_split`: confirms docstring claim that head/base arrays contain only their respective scores.
- `test_candidate_tag_should_be_classified_as_head`: confirms docstring claim that `"candidate"` (lowercase) populates head_scores.
- `test_unknown_version_tag_should_be_classified_as_base`: confirms "all other values treated as base" claim.
- `test_assertion_metric_field_should_take_precedence_over_type`: confirms step 1 of metric resolution.
- `test_missing_metric_field_should_fall_back_to_assertion_type`: confirms step 2.
- `test_missing_both_metric_and_type_should_use_unnamed`: confirms step 3.
- Error tests confirm ValueError error type matches the docstring `Raises` section.

The `__init__.py` re-export (`from jerry.testing.extraction import extract_score_arrays`) is tested implicitly by the test import at line 31 (`from jerry.testing.extraction.promptfoo_extractor import extract_score_arrays`). Note: the test imports directly from the implementation module, not from the package `__init__`, which is a minor consistency gap — the public API surface is `jerry.testing.extraction.extract_score_arrays` per the `__init__.py`, but the test bypasses the package-level re-export.

**Gaps:**

Minor: The test imports `from jerry.testing.extraction.promptfoo_extractor import extract_score_arrays` rather than `from jerry.testing.extraction import extract_score_arrays`. Both work identically, but testing via the package-level import would verify the `__init__.py` re-export chain rather than just the module directly.

**Improvement Path:**

Score is already at the high-water mark for this deliverable. Changing the test import to use the package-level public API would be a cosmetic improvement. No targeted action needed for this dimension to reach threshold.

---

### Methodological Rigor (0.88/1.00)

**Evidence:**

The implementation's methodological soundness is unchanged from iteration 1. The test suite's own methodology is sound:

- **Class-based test organization**: four `Test*` classes separating concerns (file I/O errors, happy path, skipping logic, metric name resolution). Each class has a clear responsibility.
- **`tmp_path` fixture**: all file operations use pytest's `tmp_path` for automatic filesystem isolation and cleanup. No shared mutable state between tests.
- **`caplog` for log assertions**: `test_out_of_range_score_above_1_should_be_skipped_with_warning` uses `caplog.at_level(logging.WARNING, logger="jerry.testing.extraction.promptfoo_extractor")` and asserts that a record with `"outside"` in the message exists. This is the correct pattern for verifying logger output.
- **Builder helpers**: `_make_result` and `_write_promptfoo_json` reduce duplication without abstraction overhead. Both carry docstrings and type hints per H-11.
- **`@pytest.mark.unit` markers**: all 14 tests carry the marker, enabling selective test runs.
- **Descriptive test method names**: follow the `test_{what}_should_{expected}` pattern consistently. All docstrings explain the "why."

**Persistent gap (implementation, not tests):**

The `bool` subclass edge case in the implementation at line 270 remains unresolved:
```python
if not isinstance(raw_score, (int, float)):
```
`isinstance(True, (int, float))` returns `True` in Python because `bool` is a subclass of `int`. A promptfoo result with `"score": true` (a valid JSON boolean, distinct from `1.0`) passes this check, converts to `float(True) = 1.0`, and is silently accepted. No test in the new test file covers this edge case. The prior score report's Improvement Recommendation 2 specified adding `not isinstance(raw_score, bool)` before this check. This was not implemented.

**Improvement Path:**

Add `not isinstance(raw_score, bool)` guard before the numeric type check at line 270. Simultaneously add a test: `test_boolean_score_should_be_skipped_with_warning`. These two changes would raise Methodological Rigor to 0.92+.

---

### Evidence Quality (0.85/1.00)

**Evidence:**

This dimension moves from 0.60 (zero tests) to 0.85 with 14 unit tests now present and passing. The improvement represents the closure of the primary gap identified in iteration 1.

Test coverage by behavioral contract:

| Contract | Tests | Status |
|----------|-------|--------|
| FileNotFoundError for missing file | `test_missing_file_should_raise_file_not_found_error` | Covered |
| ValueError for invalid JSON | `test_invalid_json_file_should_raise_value_error` | Covered |
| ValueError for missing top-level `results` | `test_json_missing_results_key_should_raise_value_error` | Covered |
| ValueError for missing `results.results` list | `test_json_missing_inner_results_list_should_raise_value_error` | Covered |
| Head/base array split | `test_valid_json_with_head_and_base_should_return_correct_split` | Covered |
| `"candidate"` tag classified as head | `test_candidate_tag_should_be_classified_as_head` | Covered (lowercase) |
| Unknown tag classified as base | `test_unknown_version_tag_should_be_classified_as_base` | Covered |
| Empty result list returns {} | `test_empty_results_list_should_return_empty_dict` | Covered |
| Multiple metrics independently split | `test_multiple_metrics_should_be_independently_split` | Covered |
| Out-of-range score >1.0 skipped with WARNING | `test_out_of_range_score_above_1_should_be_skipped_with_warning` | Covered |
| Out-of-range score <0.0 skipped | `test_out_of_range_score_below_0_should_be_skipped_with_warning` | Covered |
| `assertion.metric` takes precedence over `assertion.type` | `test_assertion_metric_field_should_take_precedence_over_type` | Covered |
| `assertion.type` used as fallback | `test_missing_metric_field_should_fall_back_to_assertion_type` | Covered |
| `"unnamed"` as last resort | `test_missing_both_metric_and_type_should_use_unnamed` | Covered |
| `"CANDIDATE"` uppercase classified as head | — | **Not covered** |
| Missing `__version__` key (absent, not empty) | — | **Not covered** |
| `"score": true` (bool) skipped or accepted | — | **Not covered** |

The three uncovered edge cases prevent the score from reaching 0.90+. The rubric for 0.9+ Evidence Quality is "All claims with credible citations." Three documented behavioral claims (case-insensitive version matching, missing `__version__` handling, bool score behavior) lack executable evidence.

Additionally: the test for out-of-range <0.0 (`test_out_of_range_score_below_0_should_be_skipped_with_warning`) does not assert a WARNING log message, only that the score is absent from the output array. This is weaker than the >1.0 test which does verify the log.

**Improvement Path:**

Add three tests to close the remaining evidence gaps:
1. `test_uppercase_candidate_tag_should_be_classified_as_head` — uses `"CANDIDATE"` as the version tag.
2. `test_missing_version_key_should_be_classified_as_base` — uses a `vars` dict without the `__version__` key at all (not present, distinct from empty string).
3. `test_boolean_score_should_be_skipped_with_warning` — uses `"score": True` and asserts it is either skipped (with WARNING) or accepted as 1.0 (explicit behavior specification).

These three additions would raise Evidence Quality to approximately 0.92.

---

### Actionability (0.78/1.00)

**Evidence:**

The tests improve actionability materially:

- `_make_result` and `_write_promptfoo_json` helpers serve as concrete, runnable fixture patterns that a downstream developer can copy to write integration tests against a real promptfoo output file.
- The test invocation `uv run pytest tests/prompt-regression/unit/test_promptfoo_extractor.py -v --tb=short` provides an immediately runnable command.
- The class-based structure shows a developer how to extend test coverage.
- 14 tests give a developer confidence that the API works as documented before using it.

**Persistent gaps:**

- **Silent empty return**: when `result_list` is `[]`, the function returns `{}` with only an INFO log. A caller that feeds this `{}` to `compare_versions()` will encounter an opaque downstream error rather than a clear upstream signal. The test `test_empty_results_list_should_return_empty_dict` explicitly validates this behavior, meaning it is now confirmed-as-implemented rather than being flagged as a gap. However, from an operator perspective, a WARNING log here would still improve actionability.
- **No sample fixture file**: `tests/fixtures/sample-promptfoo-results.json` does not exist. A developer writing integration tests must construct fixtures from scratch using the docstring's inline JSON schema. The test helpers partially mitigate this by providing builder functions.
- **No coverage report**: the 90% line coverage target stated in the test file header is aspirational. No `pytest-cov` invocation or coverage report is provided. A developer cannot verify the coverage claim without running coverage tooling separately.

**Improvement Path:**

The single highest-impact actionability improvement is adding a WARNING log for empty `result_list`. This directly signals anomalous conditions to operators at runtime. Score would reach approximately 0.85.

---

### Traceability (0.85/1.00)

**Evidence:**

The test file adds meaningful traceability:

- Header docstring cites `CG-008: extract_score_arrays() function` — links tests to the work item they validate.
- Header docstring cites `CG-021: Metric name resolution precedence` — links the metric resolution tests to a separate acceptance criterion, demonstrating awareness of the requirement breakdown.
- Header docstring cites `H-20: BDD test-first (90% line coverage target)` — links the test methodology standard to the rule that mandates it.
- SPDX license identifier and copyright present in the test file header.

The implementation side retains the same traceability as iteration 1:
- `# CG-008` tags in both `promptfoo_extractor.py` and `__init__.py`.
- H-07, H-10, H-11 cited in module docstrings.
- No cross-reference to behavioral contracts document or STORY-036-002.

**Gaps:**

- The implementation still lacks a reference to the source behavioral contract (the gap-closure prompt or a `behavioral-contracts.md`). The `# CG-008` tag is sufficient for identification but not for navigating to the acceptance criteria.
- The test file cites CG-021 for metric name resolution but the implementation does not. This creates an asymmetry where a developer reading the implementation cannot easily locate the acceptance criteria that the CG-021 tests verify.

**Improvement Path:**

Add a comment block in `promptfoo_extractor.py` near the module header:
```python
# Acceptance criteria: PROJ-036 STORY-036-002 CG-008, CG-021
# See: projects/PROJ-036-prompt-regression-harness/orchestration/gap-closure-20260307-001/gap-closure-prompt.md
```
This single addition closes the traceability gap and would raise the score to 0.90.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.85 | 0.92 | Add 3 tests: (a) `"CANDIDATE"` uppercase as head tag, (b) missing `__version__` key (not present in vars), (c) `"score": true` (bool) behavior — skip with WARNING or explicitly document as accepted 1.0. Closes the 3 uncovered behavioral claims. |
| 2 | Methodological Rigor | 0.88 | 0.93 | Add `not isinstance(raw_score, bool)` guard before the `isinstance(raw_score, (int, float))` check at line 270. One-line fix in implementation; pair with test (a) from Recommendation 1. |
| 3 | Actionability | 0.78 | 0.86 | Add `logger.warning("extract_score_arrays: zero result entries in %s — file may be empty or stale.", promptfoo_json_path.name)` after structural validation block when `len(result_list) == 0`. Update `test_empty_results_list_should_return_empty_dict` to assert WARNING is emitted. |
| 4 | Traceability | 0.85 | 0.90 | Add comment block in `promptfoo_extractor.py` citing `STORY-036-002 CG-008, CG-021` and the gap-closure prompt path. |
| 5 | Completeness | 0.90 | 0.93 | Add WARNING log for empty result_list (overlaps with Recommendation 3). Consider adding `tests/fixtures/sample-promptfoo-results.json` as a reference fixture. |

**Expected composite after applying Recommendations 1-4:**

| Dimension | Current | Projected |
|-----------|---------|-----------|
| Completeness | 0.90 | 0.92 |
| Internal Consistency | 0.92 | 0.92 |
| Methodological Rigor | 0.88 | 0.93 |
| Evidence Quality | 0.85 | 0.93 |
| Actionability | 0.78 | 0.86 |
| Traceability | 0.85 | 0.90 |
| **Composite** | **0.870** | **~0.916** |

The projected composite of ~0.916 would cross the 0.92 threshold only with all four recommendations applied. Recommendations 1 and 2 together (Evidence Quality + Methodological Rigor) contribute the most: approximately +0.024 to the composite.

---

## Leniency Bias Check
- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific evidence from all three files
- [x] Uncertain scores resolved downward (Evidence Quality debated between 0.85 and 0.87 — resolved to 0.85 given three uncovered behavioral claims; Actionability debated between 0.78 and 0.80 — resolved to 0.78 given the silent empty return is now test-confirmed rather than fixed)
- [x] Prior iteration calibration considered (0.801 → 0.870 represents a 0.069 delta; the primary gap driver — Evidence Quality — moved from 0.60 to 0.85, which is proportional to adding 14 tests covering 11 of 14 behavioral claims)
- [x] No dimension scored above 0.95 without exceptional evidence (highest is Internal Consistency at 0.92, supported by 14 tests that verify the documented contracts)
- [x] Boolean score gap is doubly penalized: once in Methodological Rigor (implementation gap) and once in Evidence Quality (no test coverage) — this is correct because it represents two independent failures in two independent dimensions

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.870
threshold: 0.92
weakest_dimension: actionability
weakest_score: 0.78
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Add 3 tests: uppercase CANDIDATE tag, missing __version__ key, bool score behavior (Evidence Quality 0.85 -> 0.92)"
  - "Add not isinstance(raw_score, bool) guard at line 270 in implementation (Methodological Rigor 0.88 -> 0.93)"
  - "Add WARNING log when result_list is empty; update empty-list test to assert WARNING (Actionability 0.78 -> 0.86)"
  - "Add comment in promptfoo_extractor.py citing STORY-036-002 CG-008/CG-021 and gap-closure-prompt path (Traceability 0.85 -> 0.90)"
```
