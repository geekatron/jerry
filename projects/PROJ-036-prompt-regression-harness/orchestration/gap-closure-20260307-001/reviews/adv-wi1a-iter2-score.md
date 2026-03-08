# Quality Score Report: CG-001 CLI Entry Point — layer4_stats.py (Iteration 2)

## L0 Executive Summary
**Score:** 0.879/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.81)
**One-line assessment:** The `main()` argparse implementation is structurally complete and CI-aligned, but zero FR citations appear in the `main()` docstring (FR-015/016/017/018 absent), CG-002 is not referenced from `main()`, and the hardcoded CWD-relative `BaselineStore` path is a portability gap — fix traceability and evidence dimensions to reach threshold.

## Scoring Context
- **Deliverable:** `/Users/evorun/workspace/jerry/jerry/testing/layer4_stats.py` (`main()` function and `__main__` block, lines 520–664)
- **Deliverable Type:** Code (Layer 4 statistical engine — CLI entry point)
- **Criticality Level:** C2 (reversible, < 10 files, internal harness)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.883 REVISE (iteration 1, `baselines/store.py` — note: prior scored a different file; this is the first independent score of `layer4_stats.py main()`)
- **Iteration:** 2
- **Scored:** 2026-03-07T00:00:00Z

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.879 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — prior review `adv-wi1-cg002-score.md` findings checked against current code |

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | All 9 CG-001 flags present; `__main__` block correct; pipeline.run() deferred via TODO(CG-008); hardcoded CWD-relative store path is a portability gap |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Tier choices match EvaluationMode enum; version key construction consistent with FR-004; exit codes uniform; no contradictions detected |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | Canonical argparse pattern; fail-fast validation; specific exception catching; H-10/H-11/H-07 compliant; hardcoded CWD-relative path reduces rigor |
| Evidence Quality | 0.15 | 0.81 | 0.122 | FR-018 cited in `_emit_gha_outputs()` and `_exit_code()`; `main()` docstring contains zero FR citations (FR-015/016/017/018 absent); no CG-002 cross-reference |
| Actionability | 0.15 | 0.90 | 0.135 | `--help` functional; log configuration block outputs full argument summary; TODO(CG-008/CG-010) references are specific; pipeline does not execute (acknowledged stub) |
| Traceability | 0.10 | 0.82 | 0.082 | Section comment cites CG-001 (line 521); CG-018A/B inline (lines 482, 493, 599); `main()` docstring has zero FR citations; CG-002 absent from `main()`; `--bonferroni-k` not cited against FR-017 |
| **TOTAL** | **1.00** | | **0.879** | |

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence:**
All 9 flags present and correctly typed:
- `--agent` (required=True) — line 549
- `--tier` (required=True, choices: smoke|standard|full) — line 554
- `--results-file` (required=True) — line 560
- `--head-sha` (required=True) — line 565
- `--base-sha` (default=None, optional) — line 570
- `--agent-file` (default=None, optional) — line 575
- `--bonferroni-k` (type=int, default=None, optional) — line 580
- `--output-report` (default=None, optional) — line 586
- `--output-markdown` (default=None, optional) — line 591

The `if __name__ == "__main__": sys.exit(main())` block is present at lines 661–664. The `sys.exit()` wrapping is correct — ensures the integer return from `main()` propagates to the shell exit code.

Post-parse validation is present and correctly ordered:
1. Agent ID format regex `^[a-z][a-z0-9_-]*$` at lines 599–607 (CG-018B) — fail-fast before any I/O
2. Results file existence check at lines 609–613
3. Results file JSON validity check at lines 615–619 with `json.JSONDecodeError` specificity

`Layer4Pipeline` is instantiated at lines 635–638. `BaselineStore` is lazily imported (line 635) and constructed. This is the correct dependency injection pattern.

**Gaps:**
1. `pipeline.run()` is NOT called. The TODO at lines 654–656 explicitly defers this to CG-008/CG-010. The stub is acknowledged and documented, but the full CG-001 acceptance criterion (call `run()` with arguments mapped from parsed flags) is not satisfied. This is the largest incompleteness in the deliverable.
2. `BaselineStore(Path("baselines/data"))` at line 637 is CWD-relative. If the CLI is invoked from any directory other than the project root, the baseline store resolves to the wrong path. Neither a `--store-root` flag nor a `__file__`-relative anchor is provided. CG-001 did not explicitly require this, but it is a practical completeness gap for a CLI entry point.
3. The `--tier` value is parsed into `args.tier` but there is no mapping to `EvaluationMode` anywhere in `main()`. When CG-008 wires `pipeline.run()`, this mapping must be constructed. The deferred comment does not draft the mapping inline, leaving a latent incompleteness for the CG-008 implementer.

**Improvement Path:**
The stub limitation (gap 1) is blocked on CG-008 by design — within that scope, score is appropriate at 0.88. Fixing the `Path("baselines/data")` to `__file__`-relative would raise score to 0.90. Adding the intended `EvaluationMode` mapping as a comment at the TODO would raise to 0.91.

---

### Internal Consistency (0.92/1.00)

**Evidence:**
- `--tier` choices `["smoke", "standard", "full"]` align exactly with `EvaluationMode` enum values imported at line 46 (`EvaluationMode` is imported from `jerry.testing.types`, which defines SMOKE, STANDARD, FULL). No mismatch.
- Agent ID regex `^[a-z][a-z0-9_-]*$` is consistent with the `ps-researcher` example in the docstring and the pattern used in `baselines/store.py`.
- Version key construction (lines 621–632): `{head_sha}:{agent_file}` or `{head_sha}` fallback is consistent with the FR-004 format documented in `baselines/store.py` and the `VERSION_KEY_PATTERN` regex.
- Exit code semantics: `return 1` on validation errors at lines 607, 613, 618; `return 0` on success at line 658. Consistent with the `-> int` type annotation and the FR-018 exit code table.
- `BaselineStore` is constructed the same way in both `layer4_stats.py::main()` (line 637) and `baselines/store.py::main()` (line 564) — `Path("baselines/data")`. Consistent across files, though both share the same portability concern.

**Gaps:**
- `args.tier` is parsed but no corresponding `EvaluationMode` conversion appears in `main()`. The pipeline is not yet called, so this is not a current inconsistency — however, if `pipeline.run()` is wired in CG-008 without this mapping, the call would be incorrect. The absence of a drafted mapping is a minor future-consistency risk.
- `args.output_report` is passed to argparse with `help="Path for JSON report output (optional)."` but the `Layer4Pipeline.run()` parameter is named `output_json_path`. The naming discrepancy (report vs json_path) between the CLI flag and the API parameter could cause wiring confusion in CG-008/CG-010, though it is not a current inconsistency.

**Improvement Path:**
The current code has no active contradictions. Score is 0.92. Adding a comment drafting the tier-to-EvaluationMode mapping at the TODO site, and noting the flag-to-parameter name mapping, would raise to 0.94.

---

### Methodological Rigor (0.90/1.00)

**Evidence:**
- Argparse follows canonical Python pattern: parser construction, all arguments registered before `parse_args()`, then validation, then dispatch. No argument is referenced before parsing completes.
- `logging.basicConfig()` is called at lines 541–544 as the first substantive operation in `main()`, before any argument parsing or I/O. This ensures all subsequent `logger.*` calls within `main()` are captured.
- Fail-fast ordering: agent ID format check (line 599) → file existence (line 609) → file validity (line 615). More expensive checks (file I/O) are deferred until cheap checks (regex) pass.
- Exception specificity: `json.JSONDecodeError` at line 617 — not bare `Exception`. Correct.
- Deferred imports (`argparse`, `json as json_mod`, `re`, `sys`) are grouped at lines 536–539 — consistently deferred to avoid polluting the module's top-level import graph (H-07 compliance: adapter module remains import-clean for programmatic use).
- Lazy import of `BaselineStore` at line 635 inside `main()` — consistent with the pattern used by `__init__` at line 104 for `ReportGenerator`. This prevents a top-level concrete-adapter import at module load.
- H-10 compliance: exactly one class (`Layer4Pipeline`) in this file. `main()` is a module-level function, not a class. No violation.
- H-11 compliance: `main()` has a docstring (lines 526–535) with `Returns:` section specifying exit code semantics.
- H-07 compliance: module top-level imports are restricted to ports (`BaselinePersistencePort`, `ReportOutputPort`) and domain types. Concrete adapters are deferred.

**Gaps:**
- `BaselineStore(Path("baselines/data"))` at line 637 is relative to CWD at runtime. A CLI invoked as `uv run python -m jerry.testing.layer4_stats --agent ps-researcher --tier full --results-file results.json --head-sha abc1234` from any directory other than the project root will construct the store at the wrong path. A `__file__`-relative anchor (e.g., `Path(__file__).parents[3] / "baselines" / "data"`) or a `--store-root` CLI flag would be more rigorous.
- The `main()` docstring states it "will be wired in CG-008/CG-010" but does not document what the wiring will look like. A developer implementing CG-008 must infer the intended `pipeline.run()` invocation from context, increasing implementation risk.

**Improvement Path:**
Fix the `Path("baselines/data")` to a `__file__`-relative path or add a `--store-root` flag. Add a commented-out sketch of the `pipeline.run()` call to the TODO block. Score would increase from 0.90 to 0.92.

---

### Evidence Quality (0.81/1.00)

**Evidence:**
Strong evidence exists at the class and private method level:
- Module docstring (lines 4–27) cites FR-019 (one-way dependency rule) with an explicit dependency direction diagram.
- `_emit_gha_outputs()` docstring (lines 455–462) cites FR-018 twice, naming specific acceptance criteria.
- `_exit_code()` docstring (lines 498–510) cites FR-018 with the full exit code table (REGRESSION→1, MARGINAL→2, NO_REGRESSION→0).
- `_validate_output_path()` docstring (lines 396–421) cites CG-025.
- Inline comments cite CG-018A at lines 482 and 493, CG-018B at line 599.
- `_run_statistical()` and `_aggregate_multi_metric()` have well-documented `Returns:` and `Raises:` sections.

**Gaps:**
1. `main()` docstring (lines 526–535) contains zero FR citations. The function's CG-001 acceptance criteria require satisfying FR-015 (Wilcoxon CLI trigger), FR-016 (Wilson CI CLI trigger), FR-017 (Bonferroni CLI trigger), and FR-018 (exit code + GHA outputs). None of these are named anywhere in `main()` or its docstring. A code reviewer cannot determine from the file alone which requirements `main()` is meant to satisfy.
2. The `--bonferroni-k` argument (lines 580–585) has help text "Bonferroni K override (optional)." — no citation to FR-017, which is the FR that defines the Bonferroni correction requirement and hence the existence of this parameter.
3. The `--tier` argument (lines 554–559) has help text "Evaluation tier." — no citation to FR-005 (CLI tier interface), which mandates the three-tier (smoke/standard/full) CLI interface.
4. CG-002 is not referenced anywhere in `main()` or its docstring. CG-001 and CG-002 are companion gap items (CG-001: `layer4_stats.py` entry point; CG-002: `baselines/store.py` entry point). The absence of a cross-reference leaves the relationship between the two CLIs implicit.
5. The hardcoded `"composite_score"` string does not appear in `main()` directly — but the `main()` docstring does not cite the FR or type constant that defines the default metric. (This gap is more pronounced in `baselines/store.py::main()` where `--metric-id` has a hardcoded default.)

**Improvement Path:**
Add to `main()` docstring: "CG-001 CLI entry point. Satisfies: FR-015 (Wilcoxon), FR-016 (Wilson CI), FR-017 (Bonferroni), FR-018 (exit codes + GHA outputs). Related: CG-002 (baselines/store.py __main__)." Add `# FR-017` comment at `--bonferroni-k` definition (line 580). Add `# FR-005` comment at `--tier` definition (line 554). Score would increase from 0.81 to 0.87.

---

### Actionability (0.90/1.00)

**Evidence:**
- argparse `--help` is automatically available and will display all 9 flags with their help strings. The description "Layer 4 statistical comparison pipeline for prompt regression harness." is meaningful.
- `required=True` on `--agent`, `--tier`, `--results-file`, `--head-sha` means argparse auto-generates the error "the following arguments are required: --agent" with usage hint if any is missing — immediately actionable.
- The log configuration block (lines 640–652) outputs a full summary of all 10 parsed arguments. A developer running the CLI can immediately verify their invocation is interpreted correctly before any processing.
- `return 1` on validation errors is consistent and allows CI to detect the failure immediately via exit code.
- TODO comments (lines 654–655) cite specific CG IDs: `TODO(CG-008)` and `TODO(CG-010)` — directly traceable to the gap inventory. A developer implementing CG-008 knows exactly where to add the `pipeline.run()` call.
- The CG-018B agent ID validation at line 603 provides a specific error message with the expected format (`^[a-z][a-z0-9_-]*$`), enabling the user to self-correct.

**Gaps:**
1. `--tier` help text is "Evaluation tier." — does not explain what each tier means. A CI developer choosing between smoke, standard, and full has no in-CLI guidance. The difference between structural-check-only (smoke), 10-sample LLM evaluation (standard), and full Bonferroni suite (full) should be summarized in the help text.
2. `--bonferroni-k` help text is "Bonferroni K override (optional)." — does not mention the default values (13 for full mode per FR-017, or `len(metric_scores)` for standard mode). A developer who wants to understand or override this parameter must read the source code or `Layer4Pipeline.run()` docstring.
3. The pipeline does not actually run — acknowledged stub. A developer testing the end-to-end CLI will get a clean exit and log output but no statistical result, which may be surprising if the TODO is missed.

**Improvement Path:**
Expand `--tier` help to "(smoke: structural checks only, no statistics; standard: 10-sample LLM eval; full: full Bonferroni suite N >= 20)". Expand `--bonferroni-k` help to "(default: 13 for full tier per FR-017, or metric count for standard tier)". Score would increase from 0.90 to 0.93.

---

### Traceability (0.82/1.00)

**Evidence:**
Present traceability (specific lines):
- Line 521: `# CLI entry point (CG-001)` — section comment directly citing the gap item
- Line 482: `# CG-018A: Sanitize newlines to prevent GHA output format corruption`
- Line 493: `# CG-018A: Sanitize newlines in logged values as well`
- Line 599: `# --- CG-018B: Validate agent ID format before constructing the pipeline ---`
- Lines 397, 419, 432: CG-025 in `_validate_output_path()` docstring
- Lines 456–462: FR-018 cited twice in `_emit_gha_outputs()` docstring
- Lines 498–510: FR-018 with exit code table in `_exit_code()` docstring
- Lines 4–27: FR-019 in module docstring
- Lines 654–655: `TODO(CG-008)` and `TODO(CG-010)` — forward references to deferred work items

**Gaps:**
1. `main()` docstring (lines 526–535) contains zero FR citations. The section comment at line 521 cites CG-001 at the function-block level, but the function docstring itself does not name the FRs that define what this function must satisfy (FR-015, FR-016, FR-017, FR-018). A tool that extracts docstrings for compliance verification would find no FR traceability for `main()`.
2. CG-002 is absent from `main()`. The two entry points (CG-001 in `layer4_stats.py`, CG-002 in `baselines/store.py`) are companion items — a cross-reference comment or docstring mention would make the relationship navigable.
3. `--bonferroni-k` argument (line 580) is not cited against FR-017. The Bonferroni K parameter is defined by FR-017's acceptance criteria; a `# FR-017` comment at the argument definition would complete the traceability chain from FR → flag.
4. `--tier` argument (line 554) is not cited against FR-005. FR-005 mandates the three-tier CLI interface; a `# FR-005` comment at the argument definition would complete the chain.
5. `BaselineStore(Path("baselines/data"))` at line 637 is uncited. There is no comment explaining why this path is used (not relative to `__file__`, not from an environment variable, not from a constant). A reviewer cannot determine from the file alone whether this path is correct without reading the project layout.

**Improvement Path:**
Add "CG-001 entry point. Satisfies FR-015, FR-016, FR-017, FR-018. Related: CG-002 (`baselines/store.py`)." to `main()` docstring. Add `# FR-017` comment at `--bonferroni-k`. Add `# FR-005` comment at `--tier`. Add `# project-root-relative: CWD must be project root` comment at `BaselineStore(...)`. Score would increase from 0.82 to 0.90.

---

## Prior Review Finding Verification

The prior review for iteration 1 (`adv-wi1-cg002-score.md`) was for `baselines/store.py`, not `layer4_stats.py`. The `adv-wi1a-cg002-rescore.md` file scored `layer4_stats.py` and identified the same core gaps. Checking current code against those prior findings:

| Prior Finding | Status | Evidence |
|---------------|--------|---------|
| CG-002 citation absent from `main()` docstring | NOT ADDRESSED | `main()` docstring (lines 526–535) contains no CG-002 reference. Section comment at line 521 says CG-001 only. |
| FR citations absent from `main()` docstring (FR-015/016/017/018) | NOT ADDRESSED | Zero FR references appear in lines 526–535 or in the argparse block (lines 546–595). |
| `--tier` and `--bonferroni-k` help text should include semantics | NOT ADDRESSED | Help strings at lines 558 and 584 remain "Evaluation tier." and "Bonferroni K override (optional)." |
| `BaselineStore` hardcoded CWD-relative path | NOT ADDRESSED | `Path("baselines/data")` at line 637 remains unchanged. |

**Assessment:** The prior findings are documented but the deliverable has not been revised to address them. The current code state is the same as the initial implementation for traceability and evidence dimensions.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.81 | 0.88 | Add to `main()` docstring: "CG-001 CLI entry point. Satisfies: FR-015 (Wilcoxon CLI), FR-016 (Wilson CI CLI), FR-017 (Bonferroni CLI), FR-018 (exit codes + GHA outputs). Related: CG-002 (`baselines/store.py` entry point)." No logic change — docstring edit only. |
| 2 | Traceability | 0.82 | 0.90 | (a) Same docstring addition as Priority 1. (b) Add `# FR-017` comment immediately before `--bonferroni-k` argument (line 580). (c) Add `# FR-005` comment immediately before `--tier` argument (line 554). (d) Add `# CWD-relative: invoke from project root` comment at `BaselineStore(Path("baselines/data"))` line 637. All pure comment additions. |
| 3 | Completeness | 0.88 | 0.91 | Change `Path("baselines/data")` at line 637 to a `__file__`-relative anchor: `Path(__file__).parents[3] / "baselines" / "data"` — or add a `--store-root` CLI flag. Eliminates the CWD-dependency portability gap. |
| 4 | Actionability | 0.90 | 0.93 | (a) Expand `--tier` help to "Evaluation tier (smoke: structural checks only; standard: 10-sample LLM eval; full: full Bonferroni suite, N >= 20)". (b) Expand `--bonferroni-k` help to "Bonferroni K override (default: 13 for full tier per FR-017, or metric count for standard tier; optional)." |
| 5 | Methodological Rigor | 0.90 | 0.92 | At the TODO(CG-008) block, add a commented sketch of the intended `pipeline.run()` call showing the `args.tier` → `EvaluationMode` mapping and flag-to-parameter correspondence. Reduces implementation risk for CG-008. |

**Estimated score after Priority 1–4 applied:**

| Dimension | Current | After P1–4 | Weight | Weighted Delta |
|-----------|---------|-----------|--------|---------------|
| Completeness | 0.88 | 0.91 | 0.20 | +0.006 |
| Internal Consistency | 0.92 | 0.93 | 0.20 | +0.002 |
| Methodological Rigor | 0.90 | 0.91 | 0.20 | +0.002 |
| Evidence Quality | 0.81 | 0.88 | 0.15 | +0.011 |
| Actionability | 0.90 | 0.93 | 0.15 | +0.005 |
| Traceability | 0.82 | 0.90 | 0.10 | +0.008 |
| **Composite** | **0.879** | **0.913** | | +0.034 |

Priorities 1–4 together produce an estimated composite of **0.913** — below the 0.92 threshold by 0.007. Priority 5 (Methodological Rigor from 0.90 → 0.92) adds 0.004, bringing the estimated composite to **0.917**. To reliably cross 0.92, the `pipeline.run()` wiring (CG-008) is the most impactful change — it would raise Completeness from 0.88 to 0.95+, adding ~0.014 to the composite.

**Conclusion:** Priorities 1–4 are comment-only changes that can be applied in minutes. They close approximately 80% of the gap to threshold. Full passage requires either CG-008 implementation or exceptionally high scores across all other dimensions after the comment additions.

---

## Leniency Bias Check
- [x] Each dimension scored independently
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Evidence Quality: chose 0.81 over 0.83 — no FR citations in `main()` docstring is a definitive absence, not ambiguous; Traceability: chose 0.82 over 0.84 — CG-002 absence confirmed by direct line inspection of lines 526–535)
- [x] First-draft calibration not applicable — this is a production gap-closure implementation scored to production standard
- [x] No dimension scored above 0.95 without exceptional evidence (highest: Internal Consistency at 0.92, justified by exact choices-to-enum correspondence and uniform exit code application)
- [x] Prior finding verification completed — all four prior gaps confirmed unaddressed in current code

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.879
threshold: 0.92
weakest_dimension: Evidence Quality
weakest_score: 0.81
second_weakest_dimension: Traceability
second_weakest_score: 0.82
critical_findings_count: 0
iteration: 2
prior_findings_addressed: 0
prior_findings_total: 4
improvement_recommendations:
  - "Add CG-001 + FR-015/016/017/018 + CG-002 cross-reference to main() docstring (Priority 1: Evidence Quality)"
  - "Add # FR-017 to --bonferroni-k arg, # FR-005 to --tier arg, CWD comment to BaselineStore path (Priority 2: Traceability)"
  - "Fix Path('baselines/data') to __file__-relative anchor or add --store-root flag (Priority 3: Completeness)"
  - "Expand --tier and --bonferroni-k help strings with tier semantics and default values (Priority 4: Actionability)"
  - "Add commented pipeline.run() sketch at TODO(CG-008) with EvaluationMode mapping (Priority 5: Methodological Rigor)"
estimated_post_revision_composite: 0.917
estimated_post_cg008_composite: 0.930
```
