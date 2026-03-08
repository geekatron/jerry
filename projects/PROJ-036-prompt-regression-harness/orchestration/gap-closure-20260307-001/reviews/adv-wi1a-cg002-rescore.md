# Quality Score Report: CG-001 CLI Entry Point for layer4_stats.py (Iteration 2)

## L0 Executive Summary
**Score:** 0.891/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.78)
**One-line assessment:** The `main()` implementation is structurally complete and CI-workflow-aligned, but the claimed revision (CG-002 traceability citation + FR references in docstring) is not present in the code — the docstring still contains zero FR citations and no CG-002 reference — holding Traceability and Evidence Quality below threshold.

## Scoring Context
- **Deliverable:** `/Users/evorun/workspace/jerry/jerry/testing/layer4_stats.py` (`main()` function and argparse block, lines 520–664)
- **Deliverable Type:** Code
- **Criticality Level:** C2 (reversible, < 10 files, internal harness)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.883 REVISE (iteration 1, `baselines/store.py` Creator B — NOTE: prior scored a different file)
- **Iteration:** 2 (first score of this specific deliverable; prior 0.883 was for Creator B's `baselines/store.py`)
- **Scored:** 2026-03-07T00:00:00Z

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.891 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — 3 prior review findings checked |

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | All 7 required CG-001 flags present; `if __name__` block correct; pipeline stub acknowledged with TODO |
| Internal Consistency | 0.20 | 0.93 | 0.186 | Flags, choices, validation, and dispatch are internally coherent; no contradictions found |
| Methodological Rigor | 0.20 | 0.91 | 0.182 | Canonical argparse pattern, structured logging, exit codes, agent ID regex, JSON validation all correct |
| Evidence Quality | 0.15 | 0.82 | 0.123 | FR-018 cited in `_emit_gha_outputs` and `_exit_code`; `main()` docstring and argparse help strings contain zero FR citations |
| Actionability | 0.15 | 0.91 | 0.137 | `--help` fully functional; pipeline instantiation proceeds to log configuration; CG-008/CG-010 deferred path is clearly documented |
| Traceability | 0.10 | 0.83 | 0.083 | CG-001 cited at section comment (line 521); CG-018A/B cited inline; CG-002 NOT in main() docstring; FR-005/FR-014/FR-015/FR-016/FR-017/FR-018 absent from main() |
| **TOTAL** | **1.00** | | **0.891** | |

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**
All 7 flags specified in the gap-closure prompt for CG-001 are present:
- `--agent` (required) — line 549
- `--tier` (required, choices: smoke|standard|full) — line 554
- `--results-file` (required) — line 560
- `--head-sha` (required) — line 565
- `--base-sha` (optional, default None) — line 570
- `--bonferroni-k` (optional int, default None) — line 580
- `--output-report` (optional, default None) — line 586
- `--output-markdown` (optional, default None) — line 591

Additionally, `--agent-file` (optional) is present at line 575. This exceeds the CG-001 minimum spec by one flag — correct and consistent with the workflow invocation pattern.

The `if __name__ == "__main__": sys.exit(main())` block is present at lines 661–664.

Post-parse validation includes:
- Agent ID format regex (`^[a-z][a-z0-9_-]*$`) at lines 599–607 (CG-018B)
- Results file existence check at lines 609–613
- Results file JSON validity check at lines 615–619

**Gaps:**
1. The gap-closure prompt specifies "instantiate Layer4Pipeline and call `run()`" as part of CG-001. The implementation instantiates `Layer4Pipeline` (line 638) but does NOT call `pipeline.run()`. The TODO at lines 654–656 defers this to CG-008/CG-010. This is an acknowledged stub, not an undetected gap — the docstring explicitly notes the dependency. However, the deliverable does not satisfy the full CG-001 acceptance criterion of calling `run()`.
2. The `--base-sha` flag is present but not required; the gap synthesis specifies it as an optional comparison parameter. The workflow always passes `--head-sha`; `--base-sha` is inferred from the previous commit. The optional handling is correct.

**Improvement Path:**
The stub limitation is a deferred dependency (CG-008). Within the scope of what is deliverable now (the argparse + pipeline instantiation without `run()`), the completeness score is appropriate at 0.90. Implementing `run()` wiring (CG-008) would raise this to 0.95+.

---

### Internal Consistency (0.93/1.00)

**Evidence:**
- The `--tier` choices (`["smoke", "standard", "full"]`) match the `EvaluationMode` enum values: `EvaluationMode.SMOKE`, `EvaluationMode.STANDARD`, `EvaluationMode.FULL` are imported from `jerry.testing.types` (line 46). The enum covers all three CLI tier values.
- The `--agent` validation regex (`^[a-z][a-z0-9_-]*$`) at line 603 is consistent with the examples in the docstring (`'ps-researcher'`) and the agent IDs used throughout the test suite.
- The version key construction logic (lines 621–632) is consistent: `{head_sha}:{agent_file}` when agent-file provided, `{head_sha}` alone otherwise. This mirrors the `BaselineStore` version key format in `baselines/store.py` (FR-004 contract).
- Exit code semantics: `return 1` on validation errors (lines 607, 613, 618), `return 0` on success (line 658) — consistent with the `-> int` return type annotation.
- The `Layer4Pipeline` is instantiated with `BaselineStore(Path("baselines/data"))` (line 637–638). This hardcoded path is consistent with the validation run artifacts described in the traceability matrix.

**Gaps:**
- `--tier` argument is parsed but never passed to `Layer4Pipeline`. The pipeline currently receives no tier parameter because `pipeline.run()` is not called. When CG-008 wires the run call, the tier must be mapped to `EvaluationMode`. This mapping is not yet drafted, creating a minor future-consistency risk. Not a current inconsistency since the pipeline is not yet called.

**Improvement Path:**
Add a comment at the TODO(CG-008) line showing the intended `EvaluationMode` mapping to document the deferred wiring plan. Score would increase from 0.93 to 0.94.

---

### Methodological Rigor (0.91/1.00)

**Evidence:**
- Argparse is constructed using the canonical pattern: parser declaration, all flags registered before `parse_args()`, then sequential validation, then dispatch. This ordering prevents any flag from being used before parsing completes.
- `logging.basicConfig()` is called at lines 541–544 before any application logic — correct placement ensuring all subsequent logger calls are captured.
- Agent ID validation uses a compiled-equivalent regex at line 603, applied before any further processing — fail-fast design.
- JSON validation of the results file (lines 615–619) uses `json_mod.loads()` on the full file content and catches `json.JSONDecodeError` specifically — not `Exception`. Correct exception specificity.
- `argparse.ArgumentParser` description (line 547) is meaningful: "Layer 4 statistical comparison pipeline for prompt regression harness." This appears in `--help` output.
- All deferred imports (`argparse`, `json`, `re`, `sys`) are grouped at the top of `main()` (lines 536–539) — consistent, not scattered through the function body.
- H-10 compliance: `main()` is a module-level function. The file contains exactly one class (`Layer4Pipeline`). No violation.
- H-11 compliance: `main()` has a docstring with a `Returns:` section.
- H-07 compliance: `main()` defers imports to function scope, preventing adapter-level pollution of module top-level imports.

**Gaps:**
- The `BaselineStore` is constructed with a hardcoded path `Path("baselines/data")` at line 637. This path is relative to the CWD at runtime, not relative to the module file. If the CLI is invoked from a directory other than the project root, the baseline store will look in the wrong location. This is a portability gap — not a methodology gap per se, but weakens the rigor of the path construction.

**Improvement Path:**
Change `Path("baselines/data")` to a path relative to the module file (e.g., `Path(__file__).parent.parent.parent / "baselines" / "data"`) or add a `--store-root` flag. Score would increase from 0.91 to 0.92.

---

### Evidence Quality (0.82/1.00)

**Evidence:**
Strong evidence exists at the class and method level:
- Module docstring (lines 4–27) cites FR-019 by name and explains the dependency direction rule.
- `_emit_gha_outputs()` docstring (lines 456–462) cites FR-018 twice with specific acceptance criteria.
- `_exit_code()` docstring (lines 499–510) cites FR-018 with enumerated exit codes.
- `_validate_output_path()` docstring (line 397) cites CG-025.
- Inline comments cite CG-018A (lines 482, 493) and CG-018B (line 599).

**Gaps:**
1. The `main()` docstring (lines 526–535) contains ZERO FR citations. The function implements CG-001 which requires satisfying FR-015, FR-016, FR-017, FR-018 (from the gap synthesis traceability table: CG-001 blocking FRs are FR-015, FR-016, FR-017, FR-018). None of these are named in the `main()` docstring.
2. The claimed revision for iteration 2 states "added FR references in docstring" — this is NOT reflected in the current code. The `main()` docstring is identical in structure and content to what would be expected from iteration 1: it mentions workflow file names but no FR numbers.
3. `--bonferroni-k` help text says "Bonferroni K override (optional)" but does not cite FR-017 (Bonferroni Correction) which defines this parameter's purpose.
4. `--tier` help text says "Evaluation tier" without citing FR-005 (CLI tier interface) which defines the tier selection requirement.
5. The `main()` docstring does NOT cite CG-002. The prior review finding explicitly called for adding CG-002 to the `main()` docstring (finding #1). Examining the current code, CG-002 is absent.

**Improvement Path:**
Add to the `main()` docstring: "Satisfies CG-001 (FR-015, FR-016, FR-017, FR-018 CLI integration). See also CG-002 (__main__ entry for baselines/store.py)." Add FR-017 to `--bonferroni-k` help text. Add FR-005 to `--tier` help text. Score would increase from 0.82 to 0.88.

---

### Actionability (0.91/1.00)

**Evidence:**
- `--help` is automatically provided by argparse. The description "Layer 4 statistical comparison pipeline for prompt regression harness." and all 9 flag help strings are meaningful and machine-renderable.
- Required flag enforcement: `--agent`, `--tier`, `--results-file`, `--head-sha` are all `required=True`. Missing any of these produces argparse's standard error message with usage, which is immediately actionable.
- The pipeline instantiation (lines 635–638) proceeds to the log configuration block (lines 640–652), which outputs a complete summary of all parsed arguments. A developer running the CLI can immediately verify their invocation.
- `return 0` (line 658) allows CI/CD systems to proceed.
- The TODO comments (lines 654–655) are tagged with specific CG IDs (CG-008, CG-010), making the deferred work directly traceable to the gap inventory.

**Gaps:**
1. `--help` flag descriptions for `--tier` do not enumerate what each tier value controls (smoke = structural checks only, standard = LLM evaluation, full = full Bonferroni suite). A CI developer who needs to choose a tier has no in-CLI guidance.
2. `--bonferroni-k` help says "Bonferroni K override (optional)" but does not mention the default (13 for FULL mode, len(metric_scores) for STANDARD mode). A developer who wants to understand this parameter must read the source code.
3. The pipeline does not actually run. A caller invoking the CLI will get log output but no statistical result. This is an acknowledged limitation (stub pending CG-008), but reduces actionability for end-to-end testing.

**Improvement Path:**
Expand `--tier` help to include "(smoke: structural only, standard: LLM eval, full: full Bonferroni suite)". Expand `--bonferroni-k` help to include "(default: 13 for full mode, metric count for standard)". Score would increase from 0.91 to 0.93.

---

### Traceability (0.83/1.00)

**Evidence:**
Present traceability:
- Section comment `# CLI entry point (CG-001)` at line 521 — direct CG reference for the function block.
- `# CG-018B: Validate agent ID format` at line 599 — inline CG reference for agent validation logic.
- `# CG-018A: Sanitize newlines` at lines 482, 493 — inline CG references for sanitization.
- `# CG-025` in `_validate_output_path()` at line 397, 419, 432.
- `# TODO(CG-008)` and `# TODO(CG-010)` at lines 654–655 — deferred CG references.
- FR-019 in module docstring. FR-018 in `_emit_gha_outputs()` and `_exit_code()`.

**Gaps:**
1. `main()` docstring does NOT cite CG-002. The prior review finding stated: "Add CG-002 to `main()` docstring." The claimed revision for iteration 2 states "added CG-002 traceability citation" — examining the current code, CG-002 is NOT in the `main()` docstring (lines 526–535). The closest mention of CG-002 is the TODO at line 531 which mentions "CG-008/CG-010" but not CG-002.
2. The gap synthesis explicitly lists CG-001's blocking FRs as FR-015, FR-016, FR-017, FR-018. None of these appear in the `main()` function (docstring or inline comments). A code reviewer cannot verify that `main()` satisfies its blocking requirements without consulting external documents.
3. The `--tier` choices are not cited against FR-005 (CLI tier interface requirement), which is the requirement that mandates the three-tier CLI interface.
4. The `--bonferroni-k` flag is not cited against FR-017 (Bonferroni Correction), which defines this override parameter.
5. The hardcoded `BaselineStore(Path("baselines/data"))` path (line 637) is not cited against any FR or architectural decision.

**Improvement Path:**
Add to `main()` docstring: "CG-001 entry point. Satisfies FR-015 (Wilcoxon CLI), FR-016 (Wilson CI CLI), FR-017 (Bonferroni CLI), FR-018 (exit code + GHA outputs). Related: CG-002 (baselines/store.py entry point)." Add `# FR-017` comment to the `--bonferroni-k` argument. Add `# FR-005` comment to the `--tier` argument. Score would increase from 0.83 to 0.90.

---

## Revision Finding Verification

The prior review findings called for three specific changes. Status against the current code:

| Finding | Status | Evidence |
|---------|--------|---------|
| 1. Missing CG-002 gap reference in code comments | NOT ADDRESSED | `main()` docstring (lines 526–535) contains no CG-002 citation. The section comment at line 521 says CG-001 only. |
| 2. Missing FR traceability (FR-005, FR-014) in docstring | NOT ADDRESSED | `main()` docstring contains zero FR citations. FR-005 and FR-014 appear nowhere in the `main()` function. |
| 3. --help output should document flag purposes | PARTIALLY ADDRESSED | Help strings are present and describe each flag in plain English. FR cross-references and tier semantics are absent from help strings. |

**Conclusion on revision:** The claimed revision (CG-002 citation + FR references in docstring) is NOT present in the current code as read. The `main()` function appears to be at the same traceability state as the initial implementation. Either the revision was not committed, was applied to a different location (e.g., a different comment block), or was reverted. The section-level CG-001 comment (line 521) and inline CG-018A/B references (lines 482, 493, 599) are present but these were likely in the original implementation given the other inline CG references throughout the file.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.83 | 0.91 | Add to `main()` docstring: "CG-001 entry point. Satisfies FR-015, FR-016, FR-017, FR-018. Related: CG-002 (baselines/store.py entry point)." Add `# FR-017` comment at `--bonferroni-k` argument (line 580). Add `# FR-005` comment at `--tier` argument (line 554). Pure comment additions — no logic change. |
| 2 | Evidence Quality | 0.82 | 0.89 | The same docstring addition from Priority 1 raises Evidence Quality. Additionally: add FR-014 cite where `--tier full` is handled (FR-014 mandates N >= 20 for FULL mode). |
| 3 | Completeness | 0.90 | 0.92 | The `BaselineStore` hardcoded path `Path("baselines/data")` at line 637 should be made project-root-relative. Change to `Path(__file__).parent.parent.parent / "baselines" / "data"` or add a `--store-root` flag. |
| 4 | Actionability | 0.91 | 0.93 | Expand `--tier` help text to "(smoke: structural checks only, standard: 10-sample LLM eval, full: full Bonferroni suite N>=20)". Expand `--bonferroni-k` help text to "(default: 13 for full tier per FR-017, metric count for standard tier)". |
| 5 | Internal Consistency | 0.93 | 0.94 | Add a comment at the `TODO(CG-008)` line showing the intended tier-to-EvaluationMode mapping to prevent future wiring mistakes: `# EvaluationMode.{tier.upper()} will be derived from args.tier`. |

**Estimated score after Priority 1–4 applied:**
- Completeness: 0.92 | Internal Consistency: 0.93 | Methodological Rigor: 0.91
- Evidence Quality: 0.89 | Actionability: 0.93 | Traceability: 0.91
- Composite: (0.92×0.20)+(0.93×0.20)+(0.91×0.20)+(0.89×0.15)+(0.93×0.15)+(0.91×0.10)
- = 0.184 + 0.186 + 0.182 + 0.1335 + 0.1395 + 0.091 = **0.916**

Priority 1–2 alone (docstring FR citations + CG-002 reference) would produce:
- Evidence Quality: 0.87 | Traceability: 0.90
- Composite delta: +0.050 (Evidence) + +0.070 (Traceability) against weighted contributions
- Estimated composite: 0.891 + (0.05×0.15) + (0.07×0.10) = 0.891 + 0.0075 + 0.007 = **0.906**

Priority 1–4 together reach **0.916** — still below 0.92. Priority 3 (BaselineStore path fix) is required to cross the threshold, or methodological rigor must improve above 0.91.

---

## Leniency Bias Check
- [x] Each dimension scored independently
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Evidence Quality: chose 0.82 over 0.84 due to zero FR citations in main() docstring and unconfirmed revision; Traceability: chose 0.83 over 0.85 due to CG-002 absence confirmed by direct code inspection)
- [x] First-draft calibration not applicable — this is iteration 2 of a production gap-closure implementation; scored to production standard
- [x] No dimension scored above 0.95 without exceptional evidence (highest: Internal Consistency at 0.93, justified by exact flag-to-validation correspondence)
- [x] Revision claim verified against actual code — claimed changes NOT found; scoring reflects actual code state, not claimed state

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.891
threshold: 0.92
weakest_dimension: Evidence Quality
weakest_score: 0.82
second_weakest_dimension: Traceability
second_weakest_score: 0.83
critical_findings_count: 0
iteration: 2
revision_claim_verified: false
revision_findings_status:
  - finding: "CG-002 citation in main() docstring"
    status: NOT_FOUND
    location_checked: "lines 526-535 (main() docstring)"
  - finding: "FR-005 and FR-014 references in docstring"
    status: NOT_FOUND
    location_checked: "lines 526-535 (main() docstring) and lines 549-595 (argparse block)"
  - finding: "--help flag purposes documented"
    status: PARTIAL
    location_checked: "argparse help= strings, lines 552-594"
improvement_recommendations:
  - "Add CG-001 + CG-002 + FR-015/016/017/018 citations to main() docstring (Priority 1: Traceability + Evidence Quality)"
  - "Add # FR-017 comment to --bonferroni-k arg definition (line 580)"
  - "Add # FR-005 comment to --tier arg definition (line 554)"
  - "Change BaselineStore path from Path('baselines/data') to project-root-relative path (Priority 3: Completeness)"
  - "Expand --tier and --bonferroni-k help strings with tier semantics and default values (Priority 4: Actionability)"
estimated_post_revision_score: 0.916
```
