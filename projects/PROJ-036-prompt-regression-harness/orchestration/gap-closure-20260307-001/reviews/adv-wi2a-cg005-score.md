# Quality Score Report: CG-005 Typed Exception Hierarchy

## L0 Executive Summary
**Score:** 0.89/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.87)
**One-line assessment:** The exception hierarchy is well-designed and consistently applied across the primary evaluation paths, but a constructor-level guard in `DeepEvalAdapter.__post_init__` raises stdlib `EnvironmentError` instead of `EvaluationConfigError`, creating a completeness and consistency gap that prevents the PASS threshold.

## Scoring Context
- **Deliverable:** Three files — `jerry/testing/evaluation/exceptions.py`, `jerry/testing/evaluation/jerry_geval_deepeval_metric.py`, `jerry/testing/evaluation/deepeval_adapter.py`
- **Deliverable Type:** Code
- **Criticality Level:** C2 (Standard — reversible in one day, 3-10 files)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.8910 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No — scored directly from source files |

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.87 | 0.1740 | All 3 exception classes exist and catch blocks are typed, but `__post_init__` raises `EnvironmentError` instead of `EvaluationConfigError` |
| Internal Consistency | 0.20 | 0.88 | 0.1760 | Recovery strategy (propagate/log+0.0/log+0.0) applied consistently; bare `Exception` last-resort wraps into `EvaluationScoringError` in one file but not the other |
| Methodological Rigor | 0.20 | 0.90 | 0.1800 | Three-tier semantic model is sound; PAT-001 pre-batch check and 20% zero-fraction post-batch check are rigorous; H-11 fully met across all public methods |
| Evidence Quality | 0.15 | 0.88 | 0.1320 | Strong inline citations (CG-005, FR-006, FR-021, PAT-001); rationale for `EnvironmentError` vs. `EvaluationConfigError` in `__post_init__` is not documented |
| Actionability | 0.15 | 0.92 | 0.1380 | Error messages include remediation steps; context dicts provide structured diagnostics; 20% zero-fraction message names common causes |
| Traceability | 0.10 | 0.91 | 0.0910 | Module docstrings reference requirement IDs; CG-013/CG-024 noted inline; `EnvironmentError` choice in `__post_init__` lacks traceability reference |
| **TOTAL** | **1.00** | | **0.8910** | |

## Detailed Dimension Analysis

### Completeness (0.87/1.00)

**Evidence:**
All three required exception classes are present in `exceptions.py` with correct semantic boundaries and the `context: dict[str, str]` field. The four-level catch hierarchy (`EvaluationConfigError` re-raise, `EvaluationAPIError` log+continue, `EvaluationScoringError` log+continue, bare `Exception` wrap+surface) is applied in:
- `jerry_geval_deepeval_metric.py` `_evaluate_synchronously` (lines 243-268)
- `jerry_geval_deepeval_metric.py` `evaluate_criteria` (lines 333-374)
- `deepeval_adapter.py` `evaluate_batch` (lines 459-498)

H-10 compliance rationale is explicitly documented in `exceptions.py` module docstring. Pre-batch health check raises `EvaluationConfigError` for all four config failure conditions (empty model_name, empty criteria, empty outputs, missing ANTHROPIC_API_KEY). Post-batch 20% zero-fraction check raises `EvaluationScoringError` correctly.

**Gaps:**
`DeepEvalAdapter.__post_init__` (lines 158-163 of `deepeval_adapter.py`) raises `EnvironmentError` for the missing `ANTHROPIC_API_KEY` condition:
```python
raise EnvironmentError(
    f"ANTHROPIC_API_KEY environment variable is required..."
)
```
CG-005 required that config errors use `EvaluationConfigError` (non-retryable, CI must fail). `EnvironmentError` is a stdlib exception outside the typed hierarchy, meaning any caller catching `EvaluationConfigError` at the constructor boundary will not intercept this error. The `_pre_batch_health_check` method also checks this condition and correctly raises `EvaluationConfigError`, but the `__post_init__` guard fires first during construction.

**Improvement Path:**
Change `EnvironmentError` in `__post_init__` to `EvaluationConfigError` with the same message and a `context={"field": "ANTHROPIC_API_KEY", "model_name": self.model_name}` dict. Ensure the import is present in `deepeval_adapter.py` (it already is, line 76-80).

---

### Internal Consistency (0.88/1.00)

**Evidence:**
The recovery semantics are applied consistently across all named catch sites:
- `EvaluationConfigError`: always `raise` (never swallowed in any catch block).
- `EvaluationAPIError`: always `logger.warning(...); return 0.0` or `continue` (never re-raised).
- `EvaluationScoringError`: always `logger.warning(...); continue` or `append(0.0)` (never re-raised except at the systemic failure post-batch check, which is intentional).

The `# noqa: BLE001` suppression annotations are consistently applied to all bare `Exception` handlers in both files, signaling deliberate design rather than oversight.

**Gaps:**
In `jerry_geval_deepeval_metric.py`, the bare `Exception` handler in `_evaluate_synchronously` (lines 263-268) wraps the exception into `EvaluationScoringError` and re-raises it:
```python
except Exception as exc:  # noqa: BLE001 -- last resort; wrap and surface
    raise EvaluationScoringError(...) from exc
```
In `deepeval_adapter.py`, the bare `Exception` handler in `evaluate_batch` (lines 487-498) logs the warning and appends 0.0 without wrapping into `EvaluationScoringError`:
```python
except Exception as exc:  # noqa: BLE001 -- last resort; wrap and log
    logger.warning(...)
    for criterion in criteria:
        score_lists[criterion.name].append(0.0)
    score_lists["composite"].append(0.0)
```
These two last-resort handlers represent different behaviors for conceptually equivalent situations. The `jerry_geval_deepeval_metric.py` handler surfaces the error via `EvaluationScoringError` re-raise; the `deepeval_adapter.py` handler silently absorbs it into the score array with only a log message. Neither is wrong in isolation, but they are not symmetric.

Additionally, `__post_init__` raises `EnvironmentError` while all other config-error sites raise `EvaluationConfigError`.

**Improvement Path:**
Align `evaluate_batch`'s bare `Exception` handler with `_evaluate_synchronously`: either wrap and re-raise as `EvaluationScoringError`, or add a comment explicitly justifying why the batch context calls for a different behavior (absorb into 0.0 rather than propagate). The post-batch 20% check provides a safety net, so the absorb-and-log behavior may be intentional for per-output resilience — but this should be documented.

---

### Methodological Rigor (0.90/1.00)

**Evidence:**
The three-tier exception semantic model (config/API/scoring) is correctly grounded in distinct recovery strategies that map to real failure modes:
- `EvaluationConfigError` targets deterministic misconfiguration (won't self-heal).
- `EvaluationAPIError` targets transient failures (may self-heal on retry).
- `EvaluationScoringError` targets score calculation anomalies (recoverable via 0.0 fallback).

The `context: dict[str, str]` field on all three exception classes follows sound structured-diagnostics practice (machine-readable without embedding data into message strings). Type annotations use `from __future__ import annotations` consistently across all three files.

H-11 compliance (public function signatures + docstrings): All public methods across all three files have complete type annotations and docstrings. `evaluate_criteria`, `evaluate_batch`, `build_metric_for_agent`, `measure`, `a_measure`, `is_successful`, `_evaluate_synchronously`, and `_pre_batch_health_check` all have full `Args:`, `Returns:`, and `Raises:` sections where applicable.

The PAT-001 pre-batch health check pattern is structurally correct: it validates all four preconditions before any expensive API calls, preventing silent all-zero result arrays.

The post-batch 20% zero-fraction check (lines 504-522 of `deepeval_adapter.py`) is a meaningful systemic failure detector that surfaces batch-level degradation as a typed exception rather than returning silently degraded results.

**Gaps:**
The `__post_init__` guard in `DeepEvalAdapter` raises `EnvironmentError` instead of `EvaluationConfigError`. This is a methodological consistency gap: the designed methodology is a typed hierarchy for all error propagation in the evaluation layer; `EnvironmentError` bypasses that hierarchy at the earliest possible call site (construction).

**Improvement Path:**
Replace the `EnvironmentError` in `__post_init__` with `EvaluationConfigError`. No structural change to the check logic itself is needed.

---

### Evidence Quality (0.88/1.00)

**Evidence:**
Inline documentation is thorough and anchored to specific requirement IDs:
- Module docstrings in all three files reference CG-005, gap-analysis-20260307-001, FR-006, FR-007, FR-009, FR-021, C-007, H-07, H-10.
- Method docstrings include `Raises:` sections that name the specific exception types and conditions.
- `exceptions.py` includes `Examples:` sections in each class docstring, citing specific failure scenarios (HTTP 429, DNS failure, NaN score).
- The `_resolve_model` method cites CG-013 and CG-024 inline with the specific fix applied.
- `# noqa: BLE001 -- last resort; wrap and surface` and `# noqa: BLE001 -- last resort; wrap and log` comments document the deliberate exception broadening with rationale.
- `wrapped.__cause__ = exc` in `evaluate_criteria` preserves exception chaining for full traceback reconstruction.

**Gaps:**
The `__post_init__` method in `DeepEvalAdapter` raises `EnvironmentError` without any comment explaining why this differs from `EvaluationConfigError`. There is no annotation like `# stdlib EnvironmentError here: constructor runs before exceptions module is reliably importable` or any similar justification. This leaves reviewers uncertain whether the choice was intentional or an oversight.

**Improvement Path:**
Either change to `EvaluationConfigError` (preferred, closes the gap entirely), or add an explanatory comment documenting the deliberate use of the stdlib exception at this site.

---

### Actionability (0.92/1.00)

**Evidence:**
Error messages throughout the implementation are specific and include remediation guidance:
- `_pre_batch_health_check` ANTHROPIC_API_KEY message: `"Set it in .env or CI secrets before running the evaluation batch."` — immediate action specified.
- `_pre_batch_health_check` model_name message: `"Set a valid LLM model identifier (e.g., 'claude-sonnet-4-20250514') on the DeepEvalAdapter."` — example provided.
- Post-batch `EvaluationScoringError`: `"Common causes: API key invalid, model unavailable, rate limit exhausted, or DeepEval internal error on most outputs."` — triage guidance embedded.
- Logger warnings include agent name and criterion name, enabling precise debugging in log output.
- The `context` dict on all exception classes provides structured fields (key=field name, value=observed value) for programmatic inspection by callers.
- `_resolve_model` ValueError for Bedrock/Vertex identifiers includes the correct identifier format and a link to the gap analysis document.

**Gaps:**
Minor: the `__post_init__` `EnvironmentError` message does not reference the `EvaluationConfigError` type or note that `_pre_batch_health_check` provides a second check. This could confuse a caller who catches `EvaluationConfigError` but misses the constructor-level guard.

**Improvement Path:**
No change needed to actionability specifically — the messages are strong. The actionability gap is downstream of the completeness/consistency issue (using the wrong exception type).

---

### Traceability (0.91/1.00)

**Evidence:**
Traceability chain is strong across all three files:
- `exceptions.py` references `CG-005` and `gap-analysis-20260307-001` in the module docstring.
- `jerry_geval_deepeval_metric.py` references FR-006, FR-007, FR-021, C-007, H-07, H-10 in the module docstring and individual method docstrings.
- `deepeval_adapter.py` references FR-006, FR-007, FR-009, FR-021, C-007, H-07, H-10, PAT-001, CG-017 in the module docstring and inline comments.
- CG-013 and CG-024 are cited at the specific lines where those fixes are applied (`_resolve_model` method).
- Architecture decisions (dependency direction, H-10 one-class compliance) are documented at the module level.

**Gaps:**
The `__post_init__` `EnvironmentError` raise lacks a traceability reference. There is no comment like `# Note: pre-batch health check also validates this condition via EvaluationConfigError` or `# stdlib EnvironmentError by design (see issue X)`. The reader cannot trace why this exception type was chosen.

**Improvement Path:**
Replace with `EvaluationConfigError` (eliminating the traceability question entirely), or add a cross-reference comment explaining the relationship to `_pre_batch_health_check` and the typed hierarchy.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.87 | 0.92+ | Replace `EnvironmentError` in `DeepEvalAdapter.__post_init__` (lines 159-163 of `deepeval_adapter.py`) with `EvaluationConfigError`. Import is already present (line 76-80). Add `context={"field": "ANTHROPIC_API_KEY", "model_name": self.model_name}` to match the `_pre_batch_health_check` equivalent. |
| 2 | Internal Consistency | 0.88 | 0.92+ | Align the bare `Exception` last-resort handler in `evaluate_batch` with the pattern in `_evaluate_synchronously`. Either wrap into `EvaluationScoringError` before the 0.0 append, or add an explicit comment: `# Intentional: per-output absorption (not re-raise) because post-batch 20% check provides systemic detection.` |
| 3 | Evidence Quality | 0.88 | 0.90 | Add a comment to `__post_init__` explaining the exception type choice once P1 is resolved. If `EvaluationConfigError` is used, cite the typed hierarchy rationale. |
| 4 | Traceability | 0.91 | 0.93 | Once P1 is resolved, the traceability gap is closed automatically. No separate action needed. |

## Leniency Bias Check
- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Completeness rounded down to 0.87, not 0.90, due to the `EnvironmentError` gap)
- [x] First-draft calibration considered (this is a revised implementation, so 0.87-0.91 range is appropriate for near-threshold work)
- [x] No dimension scored above 0.95 without exceptional evidence (highest is Actionability at 0.92)

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.8910
threshold: 0.92
weakest_dimension: Completeness
weakest_score: 0.87
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Replace EnvironmentError with EvaluationConfigError in DeepEvalAdapter.__post_init__ (deepeval_adapter.py lines 159-163)"
  - "Align evaluate_batch bare Exception handler with _evaluate_synchronously: either wrap into EvaluationScoringError or add explicit comment justifying absorption behavior"
  - "Add explanatory comment to __post_init__ documenting exception type choice and relationship to _pre_batch_health_check"
```
