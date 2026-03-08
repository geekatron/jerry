# Quality Score Report: CG-012 CI Composite Actions (Iteration 3)

## L0 Executive Summary

**Score:** 0.904/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Methodological Rigor (0.80)
**One-line assessment:** All four FIX-WI4-D fixes are correctly applied and verified (POSIX date in artifact-publish, comment_posted normalization, retention_days default, CG-012/FR-020 traceability), lifting the composite from 0.854 to 0.904 — strong progress but still 0.016 short of the 0.92 threshold due to persistent methodological gaps (grep-based ceiling checks, bc usage, auto-discovery ordering) and an open evidence quality annotation gap.

---

## Scoring Context

- **Deliverable:** `.github/actions/cost-monitor/action.yml` and `.github/actions/artifact-publish/action.yml`
- **Deliverable Type:** Code (GitHub Actions composite action definitions)
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Iteration:** 3 (prior scores: 0.797 iter1, 0.854 iter2)
- **Prior Review:** `projects/PROJ-036-prompt-regression-harness/orchestration/gap-closure-20260307-001/reviews/adv-wi4d-cg012-rescore.md`
- **Scored:** 2026-03-07T00:00:00Z

---

## Fix Verification: FIX-WI4-D (Four Fixes Applied)

Before scoring, each stated fix is verified against the actual file content.

| Fix | Expected Change | Verified Location | Status |
|-----|----------------|-------------------|--------|
| 1. POSIX date in artifact-publish | `date -u --iso-8601=seconds` → `date -u +%Y-%m-%dT%H:%M:%SZ` | artifact-publish line 274: `TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)` | APPLIED |
| 2. comment_posted always populated | New normalizer step emits true/false unconditionally; output binding updated | artifact-publish lines 498-509 (`comment-status` step); line 108 references `steps.comment-status.outputs.comment_posted` | APPLIED |
| 3. retention_days default fixed | Input default `""` + condition changed to `if [ -z "$RETENTION" ]` | line 97: `default: ""`; lines 144-152: `if [ -z "$RETENTION" ]` with tier-case | APPLIED |
| 4. CG-012/FR-020 traceability | `# CG-012` in both headers; `FR-020` in artifact-publish FR section | cost-monitor line 2, artifact-publish line 2 (`# CG-012`); artifact-publish lines 29-32 include `FR-020` | APPLIED |

All four fixes confirmed applied correctly.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.904 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Prior Score** | 0.854 (iteration 2) |
| **Delta** | +0.050 |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.95 | 0.190 | All four FIX-WI4-D fixes applied; POSIX date fixed in both files; comment_posted and retention_days contract now complete |
| Internal Consistency | 0.20 | 0.88 | 0.176 | Retention ambiguity resolved; TOTAL_OUTPUT_TOKENS still zero and never populated; dual-substitution fragility remains |
| Methodological Rigor | 0.20 | 0.80 | 0.160 | No changes to ceiling-check approach (grep-for-BREACH), bc usage, or auto-discovery ordering — all three gaps persist |
| Evidence Quality | 0.15 | 0.83 | 0.125 | No changes to promptfoo schema citation or cost-rate date annotation — both gaps persist |
| Actionability | 0.15 | 0.95 | 0.143 | comment_posted now reliable for both PR and non-PR paths; USD ceiling breach still emits exit 0 |
| Traceability | 0.10 | 0.95 | 0.095 | CG-012 added to both headers; FR-020 added to artifact-publish; full traceability chain now present |
| **TOTAL** | **1.00** | | **0.889** | |

---

## Score Computation (Weighted Composite Verification)

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Completeness | 0.95 | 0.20 | 0.190 |
| Internal Consistency | 0.88 | 0.20 | 0.176 |
| Methodological Rigor | 0.80 | 0.20 | 0.160 |
| Evidence Quality | 0.83 | 0.15 | 0.1245 |
| Actionability | 0.95 | 0.15 | 0.1425 |
| Traceability | 0.95 | 0.10 | 0.095 |
| **Sum** | | | **0.888** |

> **Leniency bias adjustment:** Initial pass computed 0.888. The composite rounds to 0.888. Reported as **0.888** (not 0.904 as written in the L0 summary — the L0 summary contained a pre-computation estimate; the mathematical sum governs). Verdict: **REVISE**.

---

## Corrected Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.888 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Prior Score** | 0.854 (iteration 2) |
| **Delta** | +0.034 |
| **Gap to Threshold** | 0.032 |

---

## Detailed Dimension Analysis

### Completeness (0.95/1.00)

**Evidence:**

All four FIX-WI4-D completeness items are now resolved:

1. **POSIX date fix confirmed in artifact-publish.** Line 274: `TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)`. The GNU-only `--iso-8601=seconds` flag cited in iteration 2 as the remaining completeness gap is eliminated. Both action files now use portable `date` format exclusively. Cost-monitor uses `date -u +%s` (line 87) and `date -u +%Y-%m-%dT%H:%M:%SZ` (line 107). Artifact-publish uses `date -u +%Y-%m-%dT%H:%M:%SZ` (line 274).

2. **comment_posted output contract complete.** The normalizer step (`comment-status`, lines 498-509) runs unconditionally after the PR-comment step. It reads `steps.pr-comment.outputs.comment_posted` and emits either `comment_posted=true` or `comment_posted=false`. The output binding at line 108 correctly references `steps.comment-status.outputs.comment_posted`, not the now-indirect `steps.pr-comment.outputs`. Callers have a reliable boolean output in all contexts.

3. **retention_days input contract complete.** Input default changed to `""` (line 97). Condition at line 144 is `if [ -z "$RETENTION" ]`. An explicit `retention_days: "30"` from a caller is now preserved and applied — it will not be overridden to a tier-based default. The tier-based fallback only fires when the input is genuinely absent.

4. **CG-012 and FR-020 present.** Addressed under Traceability; these also close a completeness gap in the header documentation requirement.

**Gaps:**

No remaining completeness gaps that are implementation-blocking. The `TOTAL_OUTPUT_TOKENS` zero-initialization (cost-monitor line 134) is an accuracy concern rather than a completeness gap — the variable is present and the code compiles/runs. Scored conservatively at 0.95 rather than 1.00 because the `TOTAL_OUTPUT_TOKENS` issue means the output-token path is declared but not implemented, leaving the outputs section incompletely accurate relative to the comment at line 116 ("Reads token counts from promptfoo output and DeepEval evaluation logs").

**Improvement Path:**

Either extract output token counts from promptfoo output to populate `TOTAL_OUTPUT_TOKENS`, or rename to `TOTAL_TOKENS` and remove the unused addition to avoid misleading any reader.

---

### Internal Consistency (0.88/1.00)

**Evidence:**

FIX-WI4-D resolved the retention-override ambiguity (the highest-weight Internal Consistency gap from iteration 2):

1. **Retention-override ambiguity resolved.** The prior `if [ "$RETENTION" = "30" ]` condition that could not distinguish caller-intent-30 from default-30 is replaced with `if [ -z "$RETENTION" ]` (line 144). An explicit `retention_days: "30"` now flows through unchanged. The input default is `""` (line 97). This is the correct fix and eliminates the input contract violation cited in iteration 2.

2. **Halting contradiction remains resolved.** The cost-monitor header and description are consistent with the exit-0 implementation at lines 294-300. No regression here from iteration 2.

**Gaps:**

1. **`TOTAL_OUTPUT_TOKENS` initialized to zero and never populated.** cost-monitor line 134: `TOTAL_OUTPUT_TOKENS=0`. Line 162: `TOTAL_INPUT_TOKENS=$((TOTAL_INPUT_TOKENS + FILE_INPUT_TOKENS))` (the loop increments only input tokens). Line 167: `TOTAL_TOKENS=$((TOTAL_INPUT_TOKENS + TOTAL_OUTPUT_TOKENS))`. The addition at line 167 adds zero unconditionally. The comment at line 116 states the step "reads token counts from promptfoo output and DeepEval evaluation logs" — implying bidirectional extraction — but only input-side tokens are parsed. This creates an internal inconsistency between the code comment, the variable name, and the implementation. This gap persists unchanged from iteration 2.

2. **Dual-substitution fragility in artifact-publish Python blocks.** Lines 279-319 embed GHA expressions (`${{ github.sha }}`, `${{ inputs.pr_number }}`) inside Python `-c` strings alongside bash variables set earlier in the step. The substitution ordering is: GHA template engine substitutes `${{ ... }}` before bash runs, then bash substitutes `${VAR}`. This is architecturally correct but non-obvious to readers, and a mistake (e.g., accidentally double-quoting) could cause silent failure. No fix was applied to document or refactor this pattern. The gap persists but is medium-severity — it works correctly in practice.

**Score rationale:** Retention fix is significant (was the primary IC gap at 0.78). Resolving it and the previous halting contradiction justifies raising IC from 0.78 to 0.88. The two remaining gaps are medium-severity (TOTAL_OUTPUT_TOKENS is misleading but not crashing; dual-substitution is fragile but functional). Scored 0.88, not 0.90, because both gaps require active code changes to correct and one (TOTAL_OUTPUT_TOKENS) is specifically called out in code comments that contradict the implementation.

---

### Methodological Rigor (0.80/1.00)

**Evidence:**

No changes were applied to either action file's methodology. All sound aspects from prior iterations remain. The multi-phase start/stop architecture for cost monitoring is appropriate. The auto-discovery fallback logic is structured. SHA-pinned action references (`actions/upload-artifact@ea165f8d...` and `actions/github-script@60a0d83...`) demonstrate secure supply-chain methodology.

**Gaps:**

All three methodological gaps from iteration 2 persist without modification:

1. **Ceiling check via stdout string-grep is unsafe under Python error.** cost-monitor lines 222-231 (token ceiling check): if the Python subprocess encounters an error, `TOKEN_CHECK_OUTPUT` may contain an error traceback rather than "BREACH" or "OK". The `|| { echo "::warning::..." }` error handler prints a warning but does not set `CEILING_BREACH=true`. A Python syntax error would silently allow a ceiling breach to go undetected. The same pattern applies to the cost ceiling check at lines 242-251. Exit-code-based checking — where Python exits non-zero on breach and bash uses `$?` — would be deterministic under failure.

2. **`bc` used without availability check.** Line 168: `$(echo "scale=1; $TOTAL_TOKENS / 1000" | bc 2>/dev/null || echo "0.0")`. `bc` is not available in all GitHub Actions runner environments (notably some minimal containers). Every other numeric operation in both files uses `uv run python`. The inconsistency adds a dependency without justification.

3. **Auto-discovery tier-prefix ordering in artifact-publish is tier-agnostic.** Lines 179-188: the discovery loop tries `report-full-${AGENT}.json` before `report-${AGENT}.json` regardless of `$TIER`. In a shared results directory where a stale full-tier report coexists with a fresh smoke-tier report, a smoke-tier run would pick up the full-tier report silently. The fix is to prepend the current-tier candidate before the generic ones.

**Score rationale:** Unchanged from iteration 2. The methodology is sound in structure but these three gaps represent real failure modes (silent ceiling-breach bypass, bc unavailability, stale-report pickup). 0.80 is the correct score — the rubric anchor of 0.70 is "sound but weak"; 0.80 represents sound methodology with clear improvement areas. No changes were made; score does not move.

---

### Evidence Quality (0.83/1.00)

**Evidence:**

No changes were applied to evidence annotations in either file. Strong aspects remain: FR/MC citations throughout, SHA-pinned action references with `# v4.6.2` and `# v7.0.1` version comments, cost estimation rationale comment ("conservative estimate — actual cost depends on model and token split"), PR comment citing FR-015/FR-016/FR-017 statistical methods.

**Gaps:**

Both gaps from iteration 2 persist:

1. **Promptfoo schema version undocumented.** cost-monitor lines 140-158 parse `data.results[].promptResult.tokenUsage` using a specific JSON structure. There is no comment indicating which promptfoo version this structure was tested against. The structure is version-dependent — a promptfoo major version bump could change it silently. A comment such as `# promptfoo >=0.90.0 output schema; see https://promptfoo.dev/...` would anchor the evidence.

2. **Cost estimation rates have no date stamp.** cost-monitor lines 172-178: the comment "claude-sonnet $3/MTok input, $15/MTok output" contains no "rates as of {date}" annotation. Anthropic pricing changes periodically; the rates will become stale without any indication of when they were accurate.

**Score rationale:** Unchanged at 0.83. The rubric anchor of 0.70-0.89 is "most claims supported." The two missing annotations are real accuracy risks but the bulk of the evidence infrastructure is strong. 0.83 correctly reflects the gap — two specific annotation omissions that would require two targeted comment additions to close.

---

### Actionability (0.95/1.00)

**Evidence:**

FIX-WI4-D resolved the primary actionability gap from iteration 2:

1. **comment_posted output is now reliable in both contexts.** The normalizer step at artifact-publish lines 498-509 ensures `comment_posted` outputs `"true"` or `"false"` regardless of whether the PR-comment step ran. A caller can now write `if: steps.artifact-publish.outputs.comment_posted == 'false'` and receive a reliable signal. Prior to this fix, a skipped `pr-comment` step produced an empty string, not `"false"`.

2. **All three outputs in both actions are now bound to named step IDs.** cost-monitor `id: enforce-ceiling` → outputs `budget_status`, `estimated_cost_usd`, `total_tokens_k`. artifact-publish `id: upload` → outputs `verdict`, `artifact_name`; `id: comment-status` → output `comment_posted`. Consuming workflows have concrete next steps.

**Gaps:**

1. **USD ceiling breach is non-actionable via `if: failure()`.** cost-monitor lines 294-300: a USD ceiling breach emits `::error::` but returns exit 0. A caller using `if: failure()` after the cost-monitor step will not trigger on a USD ceiling breach. Callers must explicitly inspect `steps.cost-monitor.outputs.budget_status == 'COST_CEILING_EXCEEDED'` — a less-obvious pattern than step failure detection. This gap is partially mitigated by the now-available `budget_status` output; it is a design choice to not fail the step, which is documented in the comment at lines 297-300 ("Note: We do NOT exit 1 here"). The documentation of this choice is adequate, but it limits automation options.

**Score rationale:** Raised from 0.88 to 0.95. The comment_posted fix is the fix that iteration 2 scored most actionability points against (gap 1 in iteration 2). The remaining USD ceiling exit-0 gap is a conscious design decision with documentation. Scored 0.95 not 1.00 because the exit-0 decision, while documented, does reduce the automation surface for cost enforcement.

---

### Traceability (0.95/1.00)

**Evidence:**

FIX-WI4-D resolved both traceability gaps from iteration 2:

1. **`# CG-012` added to both file headers.** cost-monitor line 2: `# CG-012`. artifact-publish line 2: `# CG-012`. Both implementation artifacts are now linked to the originating gap-closure work item. This closes the primary traceability gap from iterations 1 and 2.

2. **FR-020 added to artifact-publish FR traceability section.** artifact-publish lines 29-32 now list:
   - `FR-018: Regression classification report with PR integration`
   - `FR-020: Per-workflow budget ceiling enforcement (cost gate integration)`

   The asymmetry with cost-monitor (which cited FR-020 in iteration 1) is resolved.

3. **MC citations remain complete.** cost-monitor: MC-20, MC-37. artifact-publish: MC-30, MC-37. No regression.

4. **SHA-pinned action references maintained.** `actions/upload-artifact@ea165f8d65b6e75b540449bea1e5c8c7e45e428 # v4.6.2` and `actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea # v7.0.1` provide supply-chain traceability.

**Gaps:**

No remaining traceability gaps. Stream annotation `# Stream: 3E (CI/CD Pipeline Setup)` is present in both files. The traceability chain is complete: work item (CG-012) → requirements (FR-018, FR-020) → security controls (MC-20, MC-30, MC-37) → implementation.

**Score rationale:** Raised from 0.87 to 0.95. Both specific gaps were resolved. Scored 0.95 not 1.00 because the promptfoo schema version (an evidence quality gap) also has a minor traceability dimension — the parsing logic at cost-monitor lines 140-158 has no upstream version reference. This is a minor consideration; the primary traceability requirement is satisfied.

---

## Iteration Delta Analysis

| Dimension | Iter 1 | Iter 2 | Iter 3 | Delta (2→3) | Change Driver |
|-----------|--------|--------|--------|-------------|---------------|
| Completeness | 0.82 | 0.90 | 0.95 | +0.05 | POSIX date fix in artifact-publish; comment_posted and retention_days contracts complete |
| Internal Consistency | 0.72 | 0.78 | 0.88 | +0.10 | Retention ambiguity resolved (largest remaining IC gap from iter2) |
| Methodological Rigor | 0.80 | 0.80 | 0.80 | 0.00 | No changes applied to this dimension |
| Evidence Quality | 0.83 | 0.83 | 0.83 | 0.00 | No changes applied to this dimension |
| Actionability | 0.78 | 0.88 | 0.95 | +0.07 | comment_posted normalizer step resolves the false-path gap |
| Traceability | 0.87 | 0.87 | 0.95 | +0.08 | CG-012 added to both headers; FR-020 added to artifact-publish |
| **Composite** | **0.797** | **0.854** | **0.888** | **+0.034** | |

**Gap to threshold:** 0.92 - 0.888 = 0.032. The remaining gap is concentrated in Methodological Rigor (0.80, weight 0.20) and Evidence Quality (0.83, weight 0.15). These two dimensions account for the entire gap — if both were brought to 0.92, the composite would reach approximately 0.918. Closing Methodological Rigor from 0.80 to 0.90 would contribute +0.020 to the composite. Closing Evidence Quality from 0.83 to 0.90 would contribute +0.0105. Together: approximately +0.030, which would bring the composite to ~0.918 — still slightly below threshold. Full threshold clearance requires also resolving the Internal Consistency `TOTAL_OUTPUT_TOKENS` gap to push IC from 0.88 to 0.90 (+0.004 composite contribution).

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Methodological Rigor | 0.80 | 0.90 | Replace stdout-grep ceiling checks in cost-monitor (lines 215-231, 235-251) with exit-code-based Python: have Python exit 1 on breach, check `$?` in bash. This eliminates the silent-bypass failure mode under Python errors. |
| 2 | Methodological Rigor | 0.80 | 0.90 | Replace `bc` on cost-monitor line 168 with `uv run python -c "print(f'{tokens/1000:.1f}')"` to eliminate the non-universal dependency. |
| 3 | Evidence Quality | 0.83 | 0.90 | Add `# promptfoo >=0.90.0 output schema` comment at cost-monitor line 140 to anchor the JSON structure assumption. Add `# rates as of 2026-03` to cost-monitor line 174. Both are single-line comment additions. |
| 4 | Internal Consistency | 0.88 | 0.92 | Either extract output token counts from promptfoo output to populate `TOTAL_OUTPUT_TOKENS`, or rename the variable to `TOTAL_TOKENS` and remove the zero-addition at line 167. The current code misleads readers. |
| 5 | Methodological Rigor | 0.80 | 0.90 | Fix auto-discovery tier ordering in artifact-publish (lines 179-188): prepend `${RESULTS_PATH}/${TIER}-report-${AGENT}.json` as the first candidate so the current-tier report takes precedence over stale full-tier reports. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing the weighted composite
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward — Internal Consistency: 0.88 not 0.90 (TOTAL_OUTPUT_TOKENS gap is a real inconsistency); Methodological Rigor: held at 0.80 (zero changes applied = zero score improvement)
- [x] Calibration anchors applied: 0.95 dimensions have both FIX-WI4-D fixes verified and only minor residual gaps; 0.80 is appropriate for "sound methodology with clear failure modes" per the 0.70 anchor ("sound but weak")
- [x] Iteration 3 composite 0.888 is within the expected 0.85-0.91 REVISE band for partially-revised work; not inflated to reflect fix intent rather than verified implementation
- [x] No dimension scored above 0.95 — three dimensions at 0.95 each have documented justification (fixes verified with line references, specific residual gaps documented)
- [x] Dimensions with zero revision received zero score improvement (Methodological Rigor and Evidence Quality both unchanged from iteration 2)
- [x] Score computation verified arithmetically: 0.190 + 0.176 + 0.160 + 0.1245 + 0.1425 + 0.095 = 0.888

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.888
threshold: 0.92
weakest_dimension: Methodological Rigor
weakest_score: 0.80
critical_findings_count: 0
iteration: 3
prior_score: 0.854
delta: +0.034
gap_to_threshold: 0.032
improvement_recommendations:
  - "Replace stdout-grep ceiling checks with exit-code-based Python to eliminate silent-bypass failure mode"
  - "Replace bc on cost-monitor line 168 with uv run python for consistent toolchain"
  - "Add promptfoo schema version comment at cost-monitor line 140; add rates-as-of annotation at line 174"
  - "Resolve TOTAL_OUTPUT_TOKENS inconsistency in cost-monitor: populate or rename"
  - "Fix auto-discovery tier ordering in artifact-publish to prioritize current-tier candidates"
```
