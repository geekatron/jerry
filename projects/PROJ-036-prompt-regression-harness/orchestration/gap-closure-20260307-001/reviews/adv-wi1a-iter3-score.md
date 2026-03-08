# Quality Score Report: CG-001 CLI Entry Point — layer4_stats.py (Iteration 3)

## L0 Executive Summary
**Score:** 0.899/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.85)
**One-line assessment:** All four targeted fixes are confirmed present — FR-015/016/017/018 in the docstring, CG-002 comment block, `# FR-017` on `--bonferroni-k`, `# FR-005` on `--tier` — closing the traceability gap significantly, but the FR citation quality in the docstring is incomplete (FR-015 and FR-016 citations are semantically misassigned to Wilcoxon/Wilson CI respectively when the docstring describes them as "score arrays compared across metrics" and "Wilcoxon signed-rank applied per metric," not precisely what FR-015/016 specify), the CWD-relative `BaselineStore` path portability gap persists, and `pipeline.run()` is still a stub — keeping the composite below the 0.92 threshold.

## Scoring Context
- **Deliverable:** `/Users/evorun/workspace/jerry/jerry/testing/layer4_stats.py` (`main()` function and FR traceability citations, lines 520–677)
- **Deliverable Type:** Code (Layer 4 statistical engine — CLI entry point)
- **Criticality Level:** C2 (reversible, < 10 files, internal harness)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.879 REVISE (iteration 2, `adv-wi1a-iter2-score.md`)
- **Iteration:** 3
- **Scored:** 2026-03-07T00:00:00Z

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.899 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — iteration 2 findings verified line-by-line |

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | All 9 flags present; `__main__` block correct; pipeline.run() still a stub (acknowledged, CG-008); CWD-relative BaselineStore path persists |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Tier choices match EvaluationMode; version key construction consistent; exit codes uniform; no contradictions detected |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | Canonical argparse pattern; fail-fast ordering; specific exception catching; H-07/H-10/H-11 compliant; CWD-relative path persists |
| Evidence Quality | 0.15 | 0.85 | 0.128 | FR-015/016/017/018 now in docstring References block; FR-015/016 descriptions are semantically imprecise; CG-002 cross-reference confirmed; inline FR citations on two args confirmed |
| Actionability | 0.15 | 0.90 | 0.135 | `--help` functional; log block complete; TODO(CG-008/CG-010) specific; help texts for `--tier` and `--bonferroni-k` still terse |
| Traceability | 0.10 | 0.90 | 0.090 | FR-015/016/017/018 in docstring; CG-002 comment block at BaselineStore; # FR-017 and # FR-005 inline comments confirmed; CWD-relative path still uncommented as to project-root assumption |
| **TOTAL** | **1.00** | | **0.899** | |

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence:**
All 9 argparse flags are present and correctly typed (verified against lines 557–603):
- `--agent` (required=True) — line 557
- `--tier` (required=True, choices: smoke|standard|full) — line 562
- `--results-file` (required=True) — line 568
- `--head-sha` (required=True) — line 573
- `--base-sha` (default=None) — line 578
- `--agent-file` (default=None) — line 583
- `--bonferroni-k` (type=int, default=None) — line 588
- `--output-report` (default=None) — line 594
- `--output-markdown` (default=None) — line 599

The `if __name__ == "__main__": sys.exit(main())` block is present at lines 673–676. Post-parse validation is present in correct fail-fast order: agent ID regex (line 611) → file existence (line 619) → JSON validity (line 624).

`Layer4Pipeline` is constructed at line 650. `BaselineStore` is lazily imported (line 647) and constructed at line 649.

**Gaps:**
1. `pipeline.run()` is NOT called. The TODO at lines 666–667 defers this to CG-008/CG-010. This is acknowledged and documented, but the full CG-001 acceptance criterion — executing the pipeline — remains unsatisfied. This is a structural incompleteness that cannot be scored away by traceability improvements.
2. `BaselineStore(Path("baselines/data"))` at line 649 is CWD-relative. A CLI invoked from any directory other than the project root resolves the store incorrectly. The new CG-002 comment block (lines 643–646) acknowledges this path but does not anchor it to `__file__`.
3. No `EvaluationMode` mapping from `args.tier` is drafted at the TODO site, leaving a latent gap for the CG-008 implementer.

**Improvement Path:**
The stub limitation is blocked by CG-008 by design — score is held at 0.88 for this reason. Fixing `Path("baselines/data")` to `Path(__file__).parents[3] / "baselines" / "data"` would raise to 0.90. Adding a sketched `pipeline.run()` call at the TODO site would raise to 0.91.

---

### Internal Consistency (0.92/1.00)

**Evidence:**
- `--tier` choices `["smoke", "standard", "full"]` align exactly with `EvaluationMode` enum values imported at line 45 (SMOKE, STANDARD, FULL). No mismatch.
- Agent ID regex `^[a-z][a-z0-9_-]*$` is consistent with the docstring example `'ps-researcher'` and the pattern used in `baselines/store.py`.
- Version key construction at lines 630–640: `{head_sha}:{agent_file}` or `{head_sha}` fallback — consistent with `VERSION_KEY_PATTERN` in `baselines/store.py` and FR-004 format.
- Exit code semantics: `return 1` on three validation errors (lines 615, 621, 627); `return 0` at line 670. Consistent with `-> int` annotation and FR-018 exit code table.
- New docstring References block: FR-015 is described as "Metric comparison — score arrays compared across metrics" and FR-016 as "Paired statistical tests — Wilcoxon signed-rank applied per metric." These descriptions are consistent with the actual `_run_statistical()` logic and the Wilcoxon usage in `stats.py`. The inline `# FR-005` comment at line 566 is consistent with the `--tier` flag's three-choice constraint.

**Gaps:**
- `args.tier` is parsed but no `EvaluationMode` conversion appears in `main()`. When CG-008 wires `pipeline.run()`, the mapping must be added. Not a current contradiction — deferred gap acknowledged.
- `args.output_report` (flag) vs `output_json_path` (API parameter name) naming discrepancy persists. Not a contradiction in the current code, but a future wiring risk for CG-008/CG-010.

**Improvement Path:**
No active contradictions. Score remains at 0.92. Adding a comment at the TODO drafting the tier-to-EvaluationMode mapping would raise to 0.94.

---

### Methodological Rigor (0.90/1.00)

**Evidence:**
- Argparse follows canonical Python pattern: parser construction, all arguments registered before `parse_args()`, then validation, then dispatch. No argument is referenced before parsing completes.
- `logging.basicConfig()` is called at lines 549–552 as the first substantive operation in `main()`, before any parsing or I/O.
- Fail-fast ordering: agent ID regex (cheap, line 611) → file existence (line 619) → JSON validity (line 624). More expensive checks deferred until cheap checks pass.
- `json.JSONDecodeError` at line 625 — not bare `Exception`. Correct.
- Deferred imports (`argparse`, `json as json_mod`, `re`, `sys`) at lines 544–547 — grouped, consistently deferred per H-07.
- Lazy import of `BaselineStore` at line 647 inside `main()` — consistent with the `__init__` pattern for `ReportGenerator` at line 104. Prevents top-level concrete-adapter import.
- H-10 compliance: one class (`Layer4Pipeline`) in this file. H-11 compliance: `main()` has docstring with `Returns:` section. H-07 compliance: module top-level imports restricted to ports and domain types.

**Gaps:**
- `BaselineStore(Path("baselines/data"))` at line 649 is CWD-relative. The new CG-002 comment block (lines 643–646) explains the intent ("agreed storage root for persisted score records") but does not acknowledge the CWD dependency or add a `__file__`-relative anchor. A CI developer invoking the CLI from a non-root directory will encounter a silent path resolution error.
- `main()` docstring does not draft the intended `pipeline.run()` invocation or `EvaluationMode` mapping at the TODO site. A CG-008 implementer must infer the wiring from context.

**Improvement Path:**
Fix `Path("baselines/data")` to `Path(__file__).parents[3] / "baselines" / "data"` or add a comment noting the CWD requirement. Add a commented sketch of `pipeline.run()`. Score would increase from 0.90 to 0.92.

---

### Evidence Quality (0.85/1.00)

**Evidence:**
Confirmed additions in iteration 3 (verified by direct line inspection):

1. **FR-015/016/017/018 in References block (lines 536–543):** All four FRs are now cited in the `main()` docstring. Specifically:
   - Line 539: `FR-015: Metric comparison — score arrays compared across metrics.`
   - Line 540: `FR-016: Paired statistical tests — Wilcoxon signed-rank applied per metric.`
   - Line 541: `FR-017: Bonferroni correction — --bonferroni-k controls the correction factor.`
   - Line 542: `FR-018: Report generation — --output-report and --output-markdown drive artifact paths.`
   This directly addresses the most critical gap from iteration 2 (zero FR citations in `main()` docstring).

2. **CG-001 and CG-002 in References block (lines 537–538):**
   - Line 537: `CG-001: main() argparse entry point (gap-analysis-20260307-001).`
   - Line 538: `CG-002: BaselineStore integration (gap-closure-20260307-001).`
   CG-002 cross-reference is now present.

3. **Inline `# FR-017` comment on `--bonferroni-k` (line 592):** Confirmed — `help="Bonferroni K override (optional).",  # FR-017: Bonferroni correction factor.`

4. **Inline `# FR-005` comment on `--tier` (line 566):** Confirmed — `help="Evaluation tier.",  # FR-005: Tiered evaluation mode (SMOKE/STANDARD/FULL).`

**Gaps remaining after iteration 3 fixes:**

1. **FR-015 and FR-016 description quality.** The References block describes FR-015 as "Metric comparison — score arrays compared across metrics" and FR-016 as "Paired statistical tests — Wilcoxon signed-rank applied per metric." These descriptions explain what the code does (internal implementation detail) rather than what the FRs require (the acceptance criteria). FR-015 should cite what it defines for the CLI (e.g., "CLI must accept multi-metric score arrays as input") and FR-016 what test it mandates (e.g., "Wilcoxon signed-rank test required as the primary non-parametric test"). The current phrasing reads as implementation narrative rather than requirements traceability. This is a precision gap — the citations exist, but their informational quality is below 0.9+ rubric standard ("All claims with credible citations").

2. **FR-018 description is also slightly imprecise.** Line 542 states "FR-018: Report generation — --output-report and --output-markdown drive artifact paths." FR-018 is the exit code + GHA outputs requirement, not the report generation requirement. The `--output-report` and `--output-markdown` flags drive artifact paths, but the primary FR-018 deliverable is CI/CD exit signals and `$GITHUB_OUTPUT` writes. The description undersells the exit code semantics.

3. **`BaselineStore` CWD-relative path remains undocumented as a runtime assumption.** The new CG-002 comment (lines 643–646) explains the storage root intent but does not warn that `baselines/data` is CWD-relative at runtime. A developer reading the evidence cannot determine from the file alone whether this is intentional or an oversight.

4. The `--tier` inline comment at line 566 is placed inside the `help=` string as a trailing comment, which is syntactically correct but structurally unusual — the comment is on the same line as the `help=` kwarg, not as a standalone comment above the `add_argument()` call. This reduces readability slightly but is not a blocker.

**Improvement Path:**
Revise FR-015 citation to: "FR-015: Multi-metric score comparison — CLI must accept and route multiple metric score arrays to the pipeline." Revise FR-016 to: "FR-016: Wilcoxon signed-rank test — mandated as the primary non-parametric test for paired score comparison." Revise FR-018 to: "FR-018: CI/CD integration — exit codes (0/1/2) and $GITHUB_OUTPUT writes for verdict, merge_recommendation, agent, evaluation_mode." Add a CWD note to the `BaselineStore` comment: "NB: This path is CWD-relative; invoke from project root or pass an absolute path." Score would increase from 0.85 to 0.89.

---

### Actionability (0.90/1.00)

**Evidence:**
- argparse `--help` is automatically available and will display all 9 flags with help strings.
- `required=True` on 4 flags produces self-explanatory argparse errors if any is missing.
- The log configuration block (lines 652–664) outputs a complete 10-field summary of parsed arguments — immediately actionable for debugging.
- `return 1` on validation errors is uniform and CI-detectable.
- `TODO(CG-008)` and `TODO(CG-010)` at lines 666–667 cite specific, trackable gap IDs.
- The CG-018B agent ID validation at line 613 provides the expected format in the error message.

**Gaps:**
1. `--tier` help text remains "Evaluation tier." The `# FR-005` inline comment adds context for a code reader but does not appear in `--help` output. A CI developer choosing between smoke, standard, and full has no in-CLI guidance on what each tier does.
2. `--bonferroni-k` help text remains "Bonferroni K override (optional)." The `# FR-017` inline comment adds context for a code reader but does not appear in `--help`. The default computation logic (13 for full tier, `len(metric_scores)` for standard) is invisible to a CLI user.
3. These two help text gaps were identified in iteration 2 and remain unaddressed in iteration 3. The scope of the FIX-WI1-A change was traceability comments — help text expansion was not in scope but is the remaining actionability gap.

**Improvement Path:**
Expand `--tier` help to: "Evaluation tier (smoke: structural checks only; standard: 10-sample LLM eval; full: full Bonferroni suite, N >= 20)." Expand `--bonferroni-k` help to: "Bonferroni K override (default: 13 for full tier per FR-017, or metric count for standard; optional)." Score would increase from 0.90 to 0.93.

---

### Traceability (0.90/1.00)

**Evidence:**
Present traceability after iteration 3 (specific lines):

- Line 521: `# CLI entry point (CG-001)` — section comment
- Lines 537–538: `CG-001` and `CG-002` in docstring References block
- Lines 539–542: `FR-015`, `FR-016`, `FR-017`, `FR-018` in docstring References block
- Line 566: `# FR-005: Tiered evaluation mode (SMOKE/STANDARD/FULL).` — inline on `--tier` help
- Line 592: `# FR-017: Bonferroni correction factor.` — inline on `--bonferroni-k` help
- Lines 607, 611, 614: `# CG-018B` comment block and validation
- Lines 643–646: CG-002 comment block explaining `BaselineStore` path intent
- Lines 666–667: `TODO(CG-008)` and `TODO(CG-010)` — forward references
- Lines 456–462: `_emit_gha_outputs()` docstring cites FR-018 twice
- Lines 498–510: `_exit_code()` docstring cites FR-018 with exit code table
- Lines 397, 419, 432: `_validate_output_path()` cites CG-025

The iteration 3 fixes directly address the four gaps that were the primary traceability failures in iteration 2. The traceability chain for `main()` is now:
- CG-001 → `main()` (section comment + docstring)
- CG-002 → `BaselineStore` (docstring + inline comment block)
- FR-015/016/017/018 → `main()` docstring References
- FR-005 → `--tier` flag (inline comment)
- FR-017 → `--bonferroni-k` flag (inline comment, also cited in References)

**Gaps remaining:**
1. The `BaselineStore(Path("baselines/data"))` at line 649 has a CG-002 comment explaining intent but no comment on the CWD-relativity assumption. A reviewer or automated traceability tool cannot determine from the file whether `baselines/data` is correct without knowing the invocation CWD. This is a minor gap — the comment is present but incomplete.
2. The `# FR-005` comment is placed inside the `help=` argument on the same line (line 566), which is syntactically valid but non-standard. If a future linter or traceability scraper looks for `# FR-XXX` comments preceding argument definitions (the standard pattern), this comment would be missed. The `# FR-017` placement at line 592 has the same structural issue.
3. FR-016 is not yet cited at the `_run_statistical()` method or at the `compare_versions()` call inside it, which is where Wilcoxon is actually invoked. The citation exists in `main()` docstring but does not trace to the execution point. This is an acceptable gap for iteration 3 scope — the requirement was to add FR citations to `main()`, not to all call sites.

**Improvement Path:**
Add `# NB: CWD-relative — invoke from project root` to the `BaselineStore(Path("baselines/data"))` line. Move inline FR comments to be standalone comment lines above the `add_argument()` calls (standard placement). Score would increase from 0.90 to 0.93.

---

## Prior Review Finding Verification

All four iteration 2 findings have been checked against the current code:

| Prior Finding | Status | Evidence |
|---------------|--------|---------|
| FR citations absent from `main()` docstring (FR-015/016/017/018) | **ADDRESSED** | Lines 539–542 contain all four FR citations in the References block. |
| CG-002 absent from `main()` | **ADDRESSED** | Line 538 cites CG-002 in docstring References; lines 643–646 contain a CG-002 comment block at the BaselineStore construction site. |
| `--bonferroni-k` not cited against FR-017 | **ADDRESSED** | Line 592 contains `# FR-017: Bonferroni correction factor.` as inline comment. |
| `--tier` not cited against FR-005 | **ADDRESSED** | Line 566 contains `# FR-005: Tiered evaluation mode (SMOKE/STANDARD/FULL).` as inline comment. |

Iteration 2 also identified three lower-priority gaps that were NOT in scope for FIX-WI1-A and remain unaddressed:

| Gap | Status | Evidence |
|-----|--------|---------|
| `BaselineStore(Path("baselines/data"))` CWD-relative portability | NOT ADDRESSED | `Path("baselines/data")` at line 649 unchanged; CG-002 comment acknowledges intent but not CWD dependency. |
| `--tier` help text lacks tier semantics | NOT ADDRESSED | `help="Evaluation tier."` at line 565 unchanged. |
| `--bonferroni-k` help text lacks default computation | NOT ADDRESSED | `help="Bonferroni K override (optional)."` at line 591 unchanged. |

Assessment: FIX-WI1-A fully addressed its stated scope (four traceability items). The three remaining gaps are from lower-priority recommendations not in the WI1-A scope. The composite score increase from 0.879 to 0.899 (+0.020) accurately reflects the targeted traceability improvements.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.85 | 0.90 | Revise FR-015/016/018 descriptions in docstring References block to cite acceptance criteria rather than implementation detail. Revise FR-018 to name exit codes + GHA outputs as the primary deliverable. Add CWD note to CG-002 BaselineStore comment. Pure docstring/comment changes. |
| 2 | Actionability | 0.90 | 0.93 | Expand `--tier` help to "(smoke: structural checks only; standard: 10-sample LLM eval; full: full Bonferroni suite, N >= 20)". Expand `--bonferroni-k` help to "(default: 13 for full tier per FR-017, or metric count for standard; optional)". Improves `--help` output quality. |
| 3 | Completeness | 0.88 | 0.91 | Fix `Path("baselines/data")` to `Path(__file__).parents[3] / "baselines" / "data"` or add a `--store-root` CLI flag. Eliminates CWD-relativity portability gap. |
| 4 | Methodological Rigor | 0.90 | 0.92 | At the TODO(CG-008) block, add a commented sketch of `pipeline.run()` showing `EvaluationMode[args.tier.upper()]` mapping and flag-to-parameter correspondence. Reduces CG-008 implementation risk. |
| 5 | Traceability | 0.90 | 0.93 | Move `# FR-005` and `# FR-017` inline comments to be standalone comment lines preceding their respective `add_argument()` calls (standard placement pattern). Add `# CWD-relative: invoke from project root` to `BaselineStore(Path("baselines/data"))`. |

**Estimated composite after all five priorities applied:**

| Dimension | Iter 3 | After P1–5 | Weight | Weighted Delta |
|-----------|--------|-----------|--------|---------------|
| Completeness | 0.88 | 0.91 | 0.20 | +0.006 |
| Internal Consistency | 0.92 | 0.93 | 0.20 | +0.002 |
| Methodological Rigor | 0.90 | 0.92 | 0.20 | +0.004 |
| Evidence Quality | 0.85 | 0.90 | 0.15 | +0.008 |
| Actionability | 0.90 | 0.93 | 0.15 | +0.005 |
| Traceability | 0.90 | 0.93 | 0.10 | +0.003 |
| **Composite** | **0.899** | **0.922** | | **+0.028** |

Estimated composite after all five priorities: **0.922** — above the 0.92 threshold by 0.002. This is the minimum viable improvement path. Priority 1 (Evidence Quality description refinement) and Priority 2 (help text expansion) together account for 0.013 of the 0.028 delta and are both comment-only changes. Note that the 0.922 estimate assumes the dimension scores reach the target values; borderline threshold crossing requires all five priorities to be applied cleanly.

To achieve a reliable margin above 0.92, the CG-008 implementation (wiring `pipeline.run()`) would raise Completeness from 0.88 toward 0.95+, adding ~0.014 to the composite and producing an estimated post-CG-008 composite of **0.936**.

---

## Leniency Bias Check
- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific line references (lines 521, 537–542, 549–552, 562–603, 607–627, 643–650, 666–667)
- [x] Uncertain scores resolved downward: Evidence Quality chose 0.85 over 0.87 — FR-015/016 description quality is a genuine precision gap, not merely stylistic; the descriptions explain implementation rather than acceptance criteria
- [x] Traceability chose 0.90 over 0.91 — the CWD comment absence and non-standard inline placement are confirmed gaps, not ambiguous
- [x] Completeness held at 0.88 — pipeline.run() stub is a structural incompleteness that cannot be offset by traceability improvements; held constant from iteration 2
- [x] Internal Consistency held at 0.92 — no new contradictions introduced; held at same score as iteration 2 (confirmed unchanged dimension)
- [x] Methodological Rigor held at 0.90 — CWD-relative path persists unchanged; held constant from iteration 2
- [x] Actionability held at 0.90 — help text gaps were out of scope for FIX-WI1-A; held constant from iteration 2
- [x] No dimension scored above 0.95 without exceptional evidence (highest: Internal Consistency at 0.92, Traceability at 0.90 — both justified by specific line evidence)
- [x] Score increase of +0.020 (0.879 → 0.899) is proportional to the four targeted improvements applied; would be suspicious if delta were larger

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.899
threshold: 0.92
weakest_dimension: Evidence Quality
weakest_score: 0.85
second_weakest_dimension: Completeness
second_weakest_score: 0.88
critical_findings_count: 0
iteration: 3
prior_findings_addressed: 4
prior_findings_total: 4
out_of_scope_gaps_remaining: 3
improvement_recommendations:
  - "Revise FR-015/016/018 docstring citations to state acceptance criteria, not implementation detail (Priority 1: Evidence Quality)"
  - "Expand --tier and --bonferroni-k help strings with tier semantics and FR-017 defaults (Priority 2: Actionability)"
  - "Fix Path('baselines/data') to __file__-relative anchor or add --store-root flag (Priority 3: Completeness)"
  - "Add commented pipeline.run() sketch at TODO(CG-008) with EvaluationMode mapping (Priority 4: Methodological Rigor)"
  - "Move # FR-005 and # FR-017 to standalone comment lines; add CWD note to BaselineStore (Priority 5: Traceability)"
estimated_post_p1_p5_composite: 0.922
estimated_post_cg008_composite: 0.936
gap_to_threshold: 0.021
minimum_viable_path: "Apply P1 (evidence quality description + CWD note) + P2 (help text expansion) — pure comment changes that together add ~0.013 to composite"
```
