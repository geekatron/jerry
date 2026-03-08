# Quality Score Report: CG-008 Promptfoo Score Extractor

## L0 Executive Summary
**Score:** 0.801/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.60)
**One-line assessment:** The implementation is well-structured and functionally complete against CG-008 requirements, but no unit tests exist for the module, leaving the Evidence Quality and Actionability dimensions significantly below threshold; targeted test additions and a minor docstring refinement on the private helper would raise the composite above 0.92.

---

## Scoring Context
- **Deliverable:** `jerry/testing/extraction/__init__.py` and `jerry/testing/extraction/promptfoo_extractor.py`
- **Deliverable Type:** Code
- **Criticality Level:** C2 (Standard — adapter layer addition, reversible in <1 day)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.801 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | All 8 CG-008 requirements implemented; minor gap: `_resolve_metric_name` lacks a type hint on the return in its stub form in `__init__.py` re-export (no re-export gap found on closer inspection); `__init__.py` correctly re-exports only `extract_score_arrays`. |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Module docstring, function docstring, inline comments, and behavior all agree; version discrimination values documented in module header (`"head"`, `"candidate"`) match the constant `_HEAD_VERSION_VALUES`; metric resolution precedence in docstring (3 steps) matches `_resolve_metric_name` logic exactly. |
| Methodological Rigor | 0.20 | 0.88 | 0.176 | Hexagonal adapter pattern applied correctly (`extraction` package, inbound adapter depends on domain type `ScoreArray`); `defaultdict` accumulation followed by union + sort is sound; `from __future__ import annotations` present; `bool` guard `isinstance(raw_score, (int, float))` correctly excludes `bool` subclass — wait, `bool` is a subclass of `int` in Python, so `True`/`False` would pass the isinstance check and evaluate to 1.0 or 0.0 (within range). This is an unaddressed edge case where boolean scores could silently be treated as numeric 1.0/0.0 rather than flagged as unexpected data. Score docked slightly for this subtle methodological gap. |
| Evidence Quality | 0.15 | 0.60 | 0.090 | No unit tests exist anywhere in the test suite for `promptfoo_extractor.py` or the `extraction` package (confirmed by glob and grep of `tests/` — no `test_promptfoo*`, `test_extraction*`, or `test_extract_score*` files). The gap-closure prompt (WORK ITEM 4) places test creation in STORY-036-004 Creator A/B rather than in the CG-008 work item itself, meaning tests are deferred. The implementation has no executable proof-of-correctness at the time of this score. This is a material gap for an adapter whose correctness is critical to the statistical pipeline. |
| Actionability | 0.15 | 0.72 | 0.108 | The function signature and return type are clear and immediately usable by downstream callers (`layer4_stats.compare_versions`). The `__init__.py` public API re-export enables `from jerry.testing.extraction import extract_score_arrays` per H-10. The logging `info` call at exit gives operators visibility. Gap: no example fixture file or reference to a sample promptfoo JSON structure beyond the inline docstring pseudo-JSON, and the code path for `result_list` being an empty list returns `{}` silently (documented, but a caller that passes a valid-but-empty file gets no warning). |
| Traceability | 0.10 | 0.83 | 0.083 | Both files carry `# CG-008` tag. `# SPDX-License-Identifier: Apache-2.0` and copyright present. Module docstrings explicitly reference H-07, H-10, H-11. The `ScoreArray` type is imported from `jerry.testing.types` (domain type), traceable to `types.py` line 381. Partial gap: no reference to the behavioral contracts document or CG-008 acceptance criteria in either file, and the gap-closure-prompt CG-008 requirement list is not cross-referenced. |
| **TOTAL** | **1.00** | | **0.801** | |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**

All 8 CG-008 functional requirements are present and correctly implemented:

1. `extract_score_arrays(promptfoo_json_path: Path) -> dict[str, tuple[ScoreArray, ScoreArray]]` — exact signature match (lines 94-96 of `promptfoo_extractor.py`).
2. Parses promptfoo results JSON into per-metric `(head_scores, base_scores)` arrays — implemented via `head_buckets` / `base_buckets` `defaultdict(list)` pattern (lines 199-298).
3. Version discrimination via `__version__` variable in `vars` dict — `_VERSION_VAR_KEY = "__version__"` constant (line 83); reads `vars_dict.get(_VERSION_VAR_KEY, "")` (line 216); discriminates using `_HEAD_VERSION_VALUES = frozenset({"head", "candidate"})` (line 86).
4. Metric name resolution: `assertion.metric` -> `assertion.type` -> `"unnamed"` — `_resolve_metric_name` helper (lines 328-368) implements exactly this three-step precedence.
5. `FileNotFoundError` for missing file — raised at line 161-163.
6. `ValueError` for structural issues — raised at lines 170-194 for invalid JSON and missing `results.results`.
7. `WARNING`-level logs for malformed entries — `logger.warning(...)` at lines 204, 238, 247, 261, 272, 286, 291.
8. H-07 compliance (adapter layer) — package is `jerry.testing.extraction`; it imports from `jerry.testing.types` (domain) but does not export to domain; module docstring explicitly documents this constraint.
9. H-10 compliance — one primary public function per file; `_resolve_metric_name` is a private helper, not a second primary function.
10. H-11 compliance — `extract_score_arrays` has full type hints and a docstring spanning lines 97-156. `_resolve_metric_name` has type hints and a docstring (lines 330-345).

**Gaps:**

- The `__init__.py` module docstring (line 23) states the public API is `extract_score_arrays` only, which is correct. No gap there. Minor: `OSError` is listed in the `extract_score_arrays` docstring `Raises` section but is not explicitly raised by the function — it would bubble from `Path.read_text()`. This is technically correct (documenting pass-through exceptions) but could mislead a caller reviewing only the signature. Not a completeness gap, but noted.
- Empty-file scenario: if `result_list` is `[]`, the function returns `{}` (documented). No warning is logged for an empty-but-valid file. This is a minor completeness gap relative to "robust error handling" expectation.

**Improvement Path:**

Log a `WARNING` when `result_list` is empty (zero entries is likely anomalous). The score would reach 0.93 with this plus tests passing.

---

### Internal Consistency (0.92/1.00)

**Evidence:**

The module-level docstring (lines 6-65) describes:
- Version discrimination with accepted values `"head"`, `"candidate"` (case-insensitive).
- Three-step metric name resolution.
- Entry skipping with `WARNING` for malformed entries; `ValueError` for structural failures.

All three match the implementation precisely:
- `_HEAD_VERSION_VALUES = frozenset({"head", "candidate"})` at line 86; `version_tag = str(raw_tag).strip().lower()` at line 216; `is_head = version_tag in _HEAD_VERSION_VALUES` at line 231.
- `_resolve_metric_name` implements step 1 (lines 348-350), step 2 (lines 352-361), step 3 (line 367) exactly as documented.
- Warning vs. ValueError boundary: malformed grading result entries use `logger.warning` + `continue`; missing `results.results` list uses `raise ValueError`. Consistent.

The `__init__.py` re-export is consistent with the public API claim in both file docstrings.

**Gaps:**

None material. One cosmetic inconsistency: the module docstring says "Entries missing `__version__` are treated as base and a debug-level log is emitted" but the implementation emits `logger.debug` for missing `__version__` (line 225-229), which is precisely debug-level. No inconsistency.

**Improvement Path:**

Score is already strong. No targeted improvement needed for this dimension to reach threshold in isolation.

---

### Methodological Rigor (0.88/1.00)

**Evidence:**

Sound methodology throughout:

- **Structural validation before processing**: two-step validation (`top_results` dict check, then `result_list` list check) at lines 178-194 before iteration. Order is correct.
- **Guard against non-dict entries**: `isinstance(entry, dict)` at line 203 prevents `AttributeError` on `.get()` calls.
- **Score range enforcement**: explicit `not (0.0 <= score <= 1.0)` check at line 283; skipped with WARNING rather than silently clamped (per docstring design intent).
- **`defaultdict(list)` accumulation**: correct pattern for grouping; union of keys via `set(head_buckets.keys()) | set(base_buckets.keys())` at line 303 ensures metrics seen in only one bucket appear in output.
- **Deterministic output ordering**: `sorted(all_metric_names)` at line 306 produces reproducible key ordering.
- **Stateless design**: no module-level mutable state; function is idempotent and safe to call multiple times per docstring line 155-156.
- **`from __future__ import annotations`**: present at line 67; correct for forward reference safety.

**Gaps:**

- **`bool` subclass edge case**: Python's `bool` is a subclass of `int`, so `isinstance(True, (int, float))` evaluates to `True`. A promptfoo entry with `"score": true` (valid JSON boolean) would pass the numeric check, convert to `float(True)` = `1.0`, and be accepted silently. This is likely unintended — boolean scores in a grading result are semantically different from numeric scores and should arguably be flagged with a WARNING or rejected. This is a subtle but real methodological gap because it violates the stated invariant that `score` must be "numeric."
- **No `OSError` handling at read time**: `promptfoo_json_path.read_text()` can raise `PermissionError` (a subclass of `OSError`) which is passed through to the caller. The docstring documents this correctly, so this is not a consistency gap but a methodological choice that reduces robustness for permission-denied scenarios. Minor.

**Improvement Path:**

Add `not isinstance(raw_score, bool)` to the numeric type check (line 270). This eliminates the `bool` subclass edge case and is a one-line fix. Score would reach 0.92+ on this dimension.

---

### Evidence Quality (0.60/1.00)

**Evidence:**

There are **zero unit tests** in the test suite for this module. A glob of `tests/` for `*promptfoo*`, `*extraction*`, and `*extract_score*` returned no results. A review of the work item dependency structure in `gap-closure-prompt.md` confirms that test creation (STORY-036-004 Creator B: "Score array extraction from sample promptfoo output") is intentionally deferred to a later work item.

The implementation has:
- A detailed docstring with an inline JSON example (lines 26-46) illustrating the expected promptfoo structure.
- An `Example::` block in the function docstring (lines 136-143).
- Inline comments at every major decision point.
- `logger.info` at function exit reporting metrics parsed (lines 311-318).

These are documentation artifacts, not executable evidence. They do not substitute for tests.

**Critical gap**: For an adapter that is the entry point of the statistical pipeline (its output feeds directly into `compare_versions()` in `stats.py`), the absence of tests means there is no machine-verifiable proof that:
- Head/base discrimination works correctly for edge cases (`"CANDIDATE"` uppercase, `""` empty, `None` missing).
- The metric name resolution three-step fallback produces `"unnamed"` for entries with no assertion.
- Score range rejection works for values like `-0.001` or `1.001`.
- Empty `result_list` returns `{}` without error.
- The structural `ValueError` is raised (not swallowed) for a file with `"results": []` at top-level (i.e., `results` key is a list, not a dict).

**Improvement Path:**

Create `tests/prompt-regression/unit/test_promptfoo_extractor.py` (or similar location) with at minimum:
1. Happy path: valid file with one head + one base entry, two metrics.
2. Version discrimination: `"CANDIDATE"` (uppercase) classified as head; missing `__version__` classified as base.
3. Metric name resolution: `assertion.metric` priority; `assertion.type` fallback; `"unnamed"` last resort.
4. Error handling: `FileNotFoundError` for nonexistent path; `ValueError` for invalid JSON; `ValueError` for missing `results.results`.
5. Score range: `score=-0.5` and `score=1.5` skipped with WARNING (not raised).
6. Boolean score: `score=True` behavior (whether treated as 1.0 or rejected).

This alone would raise Evidence Quality to 0.90+ and push the composite above 0.92.

---

### Actionability (0.72/1.00)

**Evidence:**

The module is immediately callable:
- Clean public API: `from jerry.testing.extraction import extract_score_arrays` per `__init__.py` line 25.
- Signature is self-explanatory: `(promptfoo_json_path: Path) -> dict[str, tuple[ScoreArray, ScoreArray]]`.
- Return type is clearly documented with named tuple elements (`head_scores`, `base_scores`).
- `Example::` block in docstring (lines 136-143) shows a two-line usage pattern.
- Exit log at lines 311-318 gives operators a summary of what was parsed.

**Gaps:**

- **No sample fixture file**: the docstring shows a JSON schema inline but does not reference an actual sample file. A downstream developer integrating this into STORY-036-004's integration tests would need to construct a fixture from scratch, working only from the docstring schema. A sample `tests/fixtures/sample-promptfoo-results.json` would accelerate integration.
- **Silent empty return**: when `result_list` is `[]` (structurally valid but no data), the function returns `{}` with only an `info` log noting "0 result entries." A caller that does not check the return dict size could proceed to `compare_versions()` with empty arrays and encounter a different (less clear) error there. A WARNING for empty returns would make this actionable for operators.
- **No `__main__` block**: the gap-closure prompt's code execution validation for CG-008 is `uv run python -c "from jerry.testing.extraction.promptfoo_extractor import extract_score_arrays"` — an import-only check, not an invocation smoke test. No `if __name__ == "__main__"` block exists. This is consistent with the module being an adapter (not a standalone CLI), but limits testability without a test suite.

**Improvement Path:**

Add a WARNING log when `result_list` is empty. Add a sample fixture JSON file. These are low-effort additions that raise actionability to 0.88+.

---

### Traceability (0.83/1.00)

**Evidence:**

Present traceability artifacts:
- `# CG-008` comment at the top of both files (line 4 in each). Links implementation directly to the work item ID.
- `# SPDX-License-Identifier: Apache-2.0` + `# Copyright (c) 2026 Victor Lau` in both files. Provenance chain is clear.
- Module docstrings explicitly cite H-07 (adapter layer rule), H-10 (one function per file), H-11 (type hints + docstrings) — three of the four hard rules governing this code.
- `from jerry.testing.types import ScoreArray` — traceable to the domain type definition at `jerry/testing/types.py` line 381.
- The function return type `dict[str, tuple[ScoreArray, ScoreArray]]` matches the CG-008 specification exactly.

**Gaps:**

- No reference to the behavioral contracts document (`behavioral-contracts.md`) or the acceptance criteria for CG-008 beyond the `# CG-008` tag. A comment block referencing the contract section or the gap-analysis finding would close this gap.
- No reference to the PROJ-036 work item hierarchy (STORY-036-002, FEAT-036-003, EPIC-036-001) that contextualizes why this module exists. The `# CG-008` tag is minimal traceability but sufficient for identification.
- `_resolve_metric_name` private helper does not carry a `# CG-008` tag of its own, though it is covered by the module-level tag.

**Improvement Path:**

Add a single comment block near the module header referencing the acceptance criteria source. Raises traceability to 0.90+.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.60 | 0.90 | Create unit test file at `tests/prompt-regression/unit/test_promptfoo_extractor.py` with 6+ test cases covering: happy path, version discrimination edge cases, metric name resolution fallback chain, FileNotFoundError, ValueError structural checks, score range rejection, and boolean score behavior. This single action has the largest composite impact (+0.045). |
| 2 | Methodological Rigor | 0.88 | 0.93 | Add `not isinstance(raw_score, bool)` guard before the `isinstance(raw_score, (int, float))` check at line 270 to prevent silent acceptance of JSON boolean scores as numeric 0.0/1.0. One-line fix. |
| 3 | Actionability | 0.72 | 0.85 | Add `logger.warning(...)` when `result_list` is empty (after the structural validation block, before the accumulation loop). Prevents silent `{}` return from propagating to callers without a signal. |
| 4 | Completeness | 0.90 | 0.93 | Add WARNING log for empty `result_list` (overlaps with Recommendation 3). Optionally: add a sample fixture JSON file at `tests/fixtures/sample-promptfoo-results.json` for use by integration tests. |
| 5 | Traceability | 0.83 | 0.90 | Add a comment near the module header referencing the behavioral contracts section or the gap-closure work item context (STORY-036-002 > CG-008). |

---

## Leniency Bias Check
- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Evidence Quality debated between 0.60 and 0.65 — resolved to 0.60 given zero executable tests)
- [x] First-draft calibration considered (this is an initial implementation with no iteration history)
- [x] No dimension scored above 0.95 without exceptional evidence (highest is Internal Consistency at 0.92, which has strong supporting evidence)

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.801
threshold: 0.92
weakest_dimension: evidence_quality
weakest_score: 0.60
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Create unit tests for promptfoo_extractor.py (6+ cases: happy path, version discrimination, metric fallback, error handling, score range, bool guard)"
  - "Add `not isinstance(raw_score, bool)` guard at line 270 to prevent silent bool-as-numeric acceptance"
  - "Add WARNING log when result_list is empty (currently silent {} return)"
  - "Add comment referencing STORY-036-002 CG-008 acceptance criteria near module header"
```
