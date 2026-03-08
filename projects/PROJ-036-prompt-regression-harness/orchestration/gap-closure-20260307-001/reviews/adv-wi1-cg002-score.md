# Quality Score Report: CG-002 __main__ Entry Point for baselines/store.py

## L0 Executive Summary
**Score:** 0.883/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.78)
**One-line assessment:** The `main()` implementation is structurally sound and CI-aligned on the flags that the workflow actually passes, but the store action's score-extraction body is a documented stub (TODO CG-008), the `retrieve` action requires `--commit-sha` but the workflow never calls retrieve, and key design decisions lack inline traceability citations — bring Evidence Quality and Traceability up and this passes.

## Scoring Context
- **Deliverable:** `/Users/evorun/workspace/jerry/jerry/testing/baselines/store.py` (lines 464–716)
- **Deliverable Type:** Code
- **Criticality Level:** C2 (reversible, <10 files, internal harness)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.883 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.87 | 0.174 | All 10 required flags present; store body is a TODO stub acknowledged in docstring |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Flags, choices, and action dispatch are internally coherent; no contradictions |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | Argparse, action-specific validation, logging, exit codes are well-structured |
| Evidence Quality | 0.15 | 0.78 | 0.117 | Docstring claims CI alignment but no inline citations; stub body lacks FR traceability |
| Actionability | 0.15 | 0.88 | 0.132 | Each action branch returns 0/1; retrieve/audit/invalidate are fully wired; store is explicitly deferred |
| Traceability | 0.10 | 0.76 | 0.076 | Module-level docstring cites CG requirements; main() has no FR/CG cross-references |
| **TOTAL** | **1.00** | | **0.883** | |

## Detailed Dimension Analysis

### Completeness (0.87/1.00)

**Evidence:**
All 10 flags specified in CG-002 are present and match the workflow invocation in `prompt-regression-full.yml` lines 392–400:
- `--action` (choices: store|retrieve|audit|invalidate) — matches `-m jerry.testing.baselines.store --action store`
- `--agent` — matches `--agent "${{ matrix.agent }}"`
- `--results-file` — matches `--results-file "tests/prompt-regression/results/full-${{ matrix.agent }}.json"`
- `--report-file` — matches `--report-file "tests/prompt-regression/results/report-full-${{ matrix.agent }}.json"`
- `--commit-sha` — matches `--commit-sha "${GITHUB_HEAD_SHA}"`
- `--tier` — matches `--tier full` (choices correctly include "full")
- `--reason` — matches `--reason "${TRIGGER_REASON}"`
- `--metric-id` (default: composite_score) — not passed by CI, default is appropriate
- `--agent-file` — not passed by CI, optional, correctly implemented
- `--contract-version` — not passed by CI for store, required only for invalidate

The `if __name__ == "__main__"` block is present at lines 712–715. The `sys.exit(main())` pattern is correct.

**Gaps:**
1. The `store` action body (lines 569–625) calls `BaselineStore` only to log and returns 0 without ever calling `store.store()`. The `TODO(CG-008)` comment documents this intentionally, but the function's docstring says it "dispatches to the appropriate BaselineStore method," which is not true for the store action — it dispatches only to logging. This is an acknowledged incompleteness per the gap-closure plan, not an undetected gap.
2. The `retrieve` action constructs the version key from `--commit-sha` but the workflow never invokes the retrieve action. The `--commit-sha` argument is marked `required=False` with no default, meaning a bare `--action retrieve --agent ps-researcher` invocation would reach the `else` branch and return 1 with an error. This is acceptable guard behavior but the docstring implies retrieval is fully implemented.
3. The store root is hardcoded to `projects/PROJ-036-prompt-regression-harness/baselines/data` (line 563). There is no `--store-root` or `--data-dir` flag, so the CLI is not useful outside the project root. CG-002 did not require this flag, so it is not a gap against spec, but it reduces generality.

**Improvement Path:**
Mark the store docstring accurately as "stub pending CG-008" or add a `NotImplementedError` comment consistent with the TODO. Score would increase from 0.87 to 0.90 with accurate docstring framing.

---

### Internal Consistency (0.92/1.00)

**Evidence:**
- The `choices=["store", "retrieve", "audit", "invalidate"]` on `--action` (line 492) exactly match the four `if args.action ==` dispatch branches (lines 569, 630, 666, 692). No action is dispatched without a branch; no branch handles an undeclared action.
- The action-specific validation block (lines 543–560) correctly validates that `--agent` is required for store/retrieve/invalidate, `--results-file`/`--commit-sha`/`--tier` are required for store, and `--contract-version` is required for invalidate. These requirements are consistent with the `BaselineStore` API signatures.
- The `--tier` choices (`["smoke", "standard", "full"]`) are consistent with `EvaluationMode` enum values implied by the module-level docstring. (Note: the enum is `EvaluationMode.FULL` and `EvaluationMode.STANDARD`; "smoke" is present in `--tier` choices but `EvaluationMode.SMOKE` existence is not verifiable from this file alone — minor cross-file consistency risk.)
- Exit code 0 on success, 1 on error is applied uniformly across all four action branches.
- The version key construction logic (`{commit_sha}:{agent_file}` or `{commit_sha}:{agent}`) is applied consistently in both `store` (lines 597–600) and `retrieve` (lines 632–636) branches.

**Gaps:**
- The `--tier` choice `"smoke"` has no corresponding `EvaluationMode.SMOKE` referenced in the file. If the enum does not have a SMOKE value, passing `--tier smoke` to the store action would reach the `TODO(CG-008)` log and return 0 without error — a silent inconsistency. This is minor given the store action is a stub.

**Improvement Path:**
Verify `EvaluationMode` enum includes `SMOKE` or add a comment noting that `"smoke"` tier stores are no-ops pending CG-008. Score would increase from 0.92 to 0.93.

---

### Methodological Rigor (0.90/1.00)

**Evidence:**
- Argparse is constructed using a well-structured pattern: top-level parser, all flags declared before `parse_args()`, followed by action-specific validation, then action dispatch. This is the canonical Python CLI pattern.
- Logging is configured at the start of `main()` (line 479–482) with a timestamped format, before any application logic. Errors use `logger.error()` with structured format strings; info operations use `logger.info()`.
- Each error path returns an integer exit code (0 or 1) rather than raising exceptions, consistent with the declared return type `int`.
- The deferred implementation (store action stub) is clearly marked with `TODO(CG-008)` and a comment explaining the dependency (Layer 2 results adapter). This follows the documented stub pattern from the module-level docstring.
- H-10 compliance: `main()` is a module-level function, not a class. The file contains exactly one class (`BaselineStore`) and one entry point function. No violation.
- H-11 compliance: `main()` has a docstring (lines 465–473) with a `Returns:` section specifying exit code semantics.
- H-07 compliance: `main()` imports `argparse`, `json`, and `sys` inside the function body (lines 475–477) to avoid polluting the adapter module's top-level namespace. This is architecturally correct for a CLI entry point that should not add overhead to programmatic use of the adapter.

**Gaps:**
- The `main()` docstring type annotation is `-> int` (line 464) but the function can also return `None` implicitly if the fallback path (line 707) is somehow reached — however, line 709 always returns 1 before that, so this is not an actual gap.
- The `dataclasses` import at line 659 (`import dataclasses as dc`) is inside the `if args.action == "retrieve"` branch. This is functionally correct but inconsistent with the other deferred imports at the top of `main()`. Minor style inconsistency.

**Improvement Path:**
Move the `dataclasses` import to the top of `main()` with the other deferred imports. Score would increase from 0.90 to 0.91 — marginal improvement.

---

### Evidence Quality (0.78/1.00)

**Evidence:**
- The module-level docstring (lines 4–46) cites FR-020, FR-004, FR-005, FR-017, and H-10/H-11 compliance by name. These provide strong traceability for the `BaselineStore` class.
- The `main()` docstring states: "Parses command-line arguments matching the GitHub Actions workflow invocation flags (prompt-regression-full.yml)" — this is a direct citation.
- The `TODO(CG-008)` comment (line 615–624) cites the dependency explicitly.

**Gaps:**
1. The `main()` docstring does not cite which FR or CG requirement mandates the entry point. CG-002 is the source of this requirement but is not mentioned in the function or its docstring. A reviewer cannot determine from the file alone whether this function satisfies CG-002 fully.
2. The `--tier` choices include `"smoke"` but no FR or requirement reference explains why smoke is included. The full workflow only passes `--tier full`.
3. The store action body logs a series of `logger.info()` calls referencing `args.report_file` at line 607, but `args.report_file` may be `None` (it is optional). The code correctly handles `None` for the report loading (lines 582–594) but logs `args.report_file` directly at line 607 which would log `None` as a string — not an error, but evidence of incomplete validation logging.
4. The `--metric-id` default of `"composite_score"` is not cited against any FR or constant from `types.py`. If the canonical default changes, this hardcoded string would silently diverge.

**Improvement Path:**
Add `# CG-002` comment to the `main()` function definition. Cite FR-020 in the `--metric-id` help text. Replace `"composite_score"` with a reference to a named constant if one exists in `types.py`. Score would increase from 0.78 to 0.85.

---

### Actionability (0.88/1.00)

**Evidence:**
- Three of four action branches (`retrieve`, `audit`, `invalidate`) are fully wired to `BaselineStore` methods. A caller can invoke these actions from the CLI and receive real results.
- The `store` action acknowledges its stub status explicitly, returns 0 (success), and documents the dependency (CG-008). CI will not fail on this action; it will proceed without writing a baseline — which is the stated intent ("unblock CI").
- The `if __name__ == "__main__": sys.exit(main())` block (lines 712–715) means the module is directly invocable via `python -m jerry.testing.baselines.store` or `uv run python -m jerry.testing.baselines.store`.
- `--help` is automatically provided by argparse and will display all flags with their help text.

**Gaps:**
1. The `store` action returning 0 when no baseline is actually stored is a silent success. A downstream CI step checking for the existence of a new baseline file would find nothing and potentially not detect the gap. An explicit `logger.warning()` is present (lines 619–624), but the exit code does not signal partial completion.
2. The `retrieve` action prints `json.dumps(None)` (line 657) to stdout when no baseline is found. Callers expecting a non-null JSON object would need to handle this, but the behavior is not documented in the `main()` docstring.

**Improvement Path:**
Document the "no baseline written" behavior in the `main()` docstring for the `store` action. Add a `logger.warning()` at exit for clarity that the stub path was taken. Score would increase from 0.88 to 0.91.

---

### Traceability (0.76/1.00)

**Evidence:**
- The `BaselineStore` class and its methods have strong traceability: FR-020, FR-004, FR-005, FR-017 are cited by line in docstrings.
- The `_validate_version_key` method cites `CG-027` and `FR-004` explicitly.
- The module-level docstring links the file to the hexagonal architecture (ADAPTER outbound) per H-07.

**Gaps:**
1. `main()` has no CG-002 citation. The function implementing CG-002 does not reference CG-002.
2. The argparse flag definitions have `help=` strings but no FR or CG cross-references. A reader cannot determine which requirement mandates each flag without reading the gap-closure prompt or the workflow file.
3. The `store_root` hardcoding at line 563 (`projects/PROJ-036-prompt-regression-harness/baselines/data`) is not cited against any FR or architectural decision. If the path was changed, it would be unclear which requirement defined the original path.
4. The `_BASELINE_QUALITY_GATE` constant at module scope (line 78) is duplicated from `stats.QUALITY_PASS_THRESHOLD` with an explanatory comment, but `main()` does not reference this constant. The quality gate enforcement happens inside `BaselineStore.store()`, so `main()` is correct not to reference it — but the traceability chain from CI invocation to quality gate is implicit.

**Improvement Path:**
Add `# CG-002: main() entry point` comment at line 464. Add `# FR-004` comment where version key is constructed (lines 596–600). Add `# FR-020` comment where store_root is defined (line 563). Score would increase from 0.76 to 0.84.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.76 | 0.84 | Add `# CG-002` comment to `main()` definition; add `# FR-004` to version key construction (lines 596–600); add `# FR-020` to store_root definition (line 563). Pure comment additions — no logic change. |
| 2 | Evidence Quality | 0.78 | 0.85 | Add CG-002 to `main()` docstring. Replace hardcoded `"composite_score"` string with a named constant or cite the FR that defines this default. Add note about `None` logging for optional `--report-file`. |
| 3 | Completeness | 0.87 | 0.91 | Update `main()` docstring to accurately say the store action is a stub pending CG-008, not that it "dispatches to BaselineStore.store()". Document the "no baseline written" behavior explicitly. |
| 4 | Actionability | 0.88 | 0.91 | Add `logger.warning()` at the exit of the store stub path making it explicit that no baseline was written (the current `logger.info()` for TODO is present but could be clearer). Document `retrieve` returning `null` JSON when no record exists. |
| 5 | Internal Consistency | 0.92 | 0.93 | Verify `EvaluationMode.SMOKE` exists in the enum; if not, remove `"smoke"` from `--tier` choices or add a comment that smoke-tier store invocations fall through to the stub and return 0. |

**Estimated score after all recommendations applied:**
- Completeness: 0.91 | Internal Consistency: 0.93 | Methodological Rigor: 0.90
- Evidence Quality: 0.85 | Actionability: 0.91 | Traceability: 0.84
- Composite: (0.91×0.20)+(0.93×0.20)+(0.90×0.20)+(0.85×0.15)+(0.91×0.15)+(0.84×0.10)
- = 0.182 + 0.186 + 0.180 + 0.1275 + 0.1365 + 0.084 = **0.896**

The recommendations above are sufficient to close the REVISE gap if applied together with a minor raise in Methodological Rigor (moving the `dataclasses` import). To reach 0.92, the store action stub must either be replaced with real implementation (CG-008) or the scoring rubric must accept "intentional stub with clear documentation" as 0.90+ for Completeness — a CG-002 re-score after CG-008 is implemented would likely score 0.93+.

## Leniency Bias Check
- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Evidence Quality: chose 0.78 over 0.80 due to missing CG-002 citation in main(); Traceability: chose 0.76 over 0.80 due to no inline FR citations in argparse block)
- [x] First-draft calibration considered — this is a production gap-closure implementation, not a first draft; scored accordingly
- [x] No dimension scored above 0.95 without exceptional evidence (highest: Internal Consistency at 0.92, justified by exact flag-to-branch correspondence)

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.883
threshold: 0.92
weakest_dimension: Traceability
weakest_score: 0.76
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Add # CG-002 comment to main() at line 464 and # FR-004 at version key construction lines 596-600"
  - "Replace hardcoded 'composite_score' default with named constant or FR citation in Evidence Quality"
  - "Update main() docstring to accurately describe store action as stub pending CG-008"
  - "Add explicit logger.warning() that no baseline was written in store stub exit path"
  - "Verify EvaluationMode.SMOKE exists or remove 'smoke' from --tier choices"
```
