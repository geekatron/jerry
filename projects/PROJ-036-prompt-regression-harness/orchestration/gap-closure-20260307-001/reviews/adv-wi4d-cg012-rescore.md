# Quality Score Report: CG-012 CI Composite Actions (Iteration 2 Re-score)

## L0 Executive Summary

**Score:** 0.854/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.78)
**One-line assessment:** The four highest-priority gaps from iteration 1 are resolved (outputs blocks in both actions, halting-contradiction header fixed, POSIX date fix in cost-monitor), lifting the score from 0.797 to 0.854, but the remaining four dimensions each retain at least one unresolved gap that keeps the composite below the 0.92 threshold — the retention-override ambiguity, GNU date in artifact-publish, traceability omissions, and evidence-quality annotations are all still open.

---

## Scoring Context

- **Deliverable:** `.github/actions/cost-monitor/action.yml` and `.github/actions/artifact-publish/action.yml`
- **Deliverable Type:** Code (GitHub Actions composite action definitions)
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Iteration:** 2 (prior score: 0.797 REVISE, 2026-03-07)
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.854 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Prior Score** | 0.797 (iteration 1) |
| **Delta** | +0.057 |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | Outputs blocks added to both actions; cost-monitor date fixed; artifact-publish `--iso-8601` remains on line 272 |
| Internal Consistency | 0.20 | 0.78 | 0.156 | Halting contradiction resolved; retention-override ambiguity and dual-substitution fragility remain |
| Methodological Rigor | 0.20 | 0.80 | 0.160 | No changes to ceiling-check approach, bc usage, or auto-discovery ordering — all iteration 1 gaps persist |
| Evidence Quality | 0.15 | 0.83 | 0.125 | No changes to promptfoo schema citation or cost-rate date annotation — both gaps persist |
| Actionability | 0.15 | 0.88 | 0.132 | Outputs blocks resolve the primary actionability gap; exit-0 on USD breach and network prereqs remain |
| Traceability | 0.10 | 0.87 | 0.087 | No changes — CG-012 ID still absent from both files; FR-020 still absent from artifact-publish |
| **TOTAL** | **1.00** | | **0.854** | |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**

Revisions resolved both completeness gaps from iteration 1:

1. **Outputs blocks added — both actions.** cost-monitor now declares `outputs:` at lines 58-67 with three outputs: `budget_status`, `estimated_cost_usd`, `total_tokens_k`, each referencing `${{ steps.enforce-ceiling.outputs.* }}`. artifact-publish declares `outputs:` at lines 97-106 with three outputs: `verdict` (from `steps.upload`), `artifact_name` (from `steps.upload`), and `comment_posted` (from `steps.pr-comment`).

2. **POSIX date fix applied to cost-monitor.** Line 86 uses `date -u +%s` (POSIX-portable). Line 106 uses `$(date -u +%Y-%m-%dT%H:%M:%SZ)` (POSIX-portable). Both occurrences in cost-monitor are fixed.

**Gaps:**

1. **artifact-publish line 272 still uses `--iso-8601=seconds`.** The metadata generation step at line 272: `TIMESTAMP=$(date -u --iso-8601=seconds)`. This is the GNU-only flag. It was fixed in cost-monitor but not in artifact-publish. This is a partial fix — one of two files still has the portability defect.

**Improvement Path:**

Replace `date -u --iso-8601=seconds` on artifact-publish line 272 with `date -u +%Y-%m-%dT%H:%M:%SZ`.

---

### Internal Consistency (0.78/1.00)

**Evidence:**

Revision resolved the primary contradiction:

1. **Halting contradiction resolved.** cost-monitor header comment at line 27 now reads: `# MC-20: Per-workflow budget ceiling ($5 Standard, $50 Full) — alerts on breach (does not halt; see CG-012)`. The description field at lines 38-39 says "Enforces per-workflow budget ceilings and alerts on threshold breach." This is now behaviorally consistent with the implementation at lines 294-300 which explicitly does not exit 1.

**Gaps:**

1. **Retention-override ambiguity persists.** artifact-publish lines 142-150 still override `RETENTION` to tier-based defaults when the value equals "30". A caller who explicitly passes `retention_days: "30"` for a full-tier run will silently receive 90 days instead. The condition `if [ "$RETENTION" = "30" ]` cannot distinguish "caller used the default" from "caller intentionally specified 30 days." This is an input contract violation.

2. **Dual-substitution fragility persists.** artifact-publish line 287 (`'${TIMESTAMP}'` where `TIMESTAMP` is set at line 272 from `date -u --iso-8601=seconds`) and line 275 (`'${SHA}'` where `SHA="${{ github.sha }}"`) mix GHA expression substitution (applied by GHA before bash runs) with bash variable substitution (applied at bash runtime). This works in the current environment but is architecturally fragile — the outer Python f-string at line 277 (`uv run python -c "...`) is a multi-substitution context where the layering is not obvious from reading. No changes were made to this pattern.

3. **`TOTAL_OUTPUT_TOKENS` initialized to zero and never updated** (cost-monitor line 134: `TOTAL_OUTPUT_TOKENS=0`; line 166: `TOTAL_TOKENS=$((TOTAL_INPUT_TOKENS + TOTAL_OUTPUT_TOKENS))`). The variable is initialized but the parsing loop populates only `TOTAL_INPUT_TOKENS`. Adding input and output tokens will always produce the same result as taking input tokens alone. This was present in iteration 1 and remains. The comment at line 116 ("Reads token counts from promptfoo output and DeepEval evaluation logs") implies both should be extracted, but only input tokens are parsed.

**Improvement Path:**

Fix the retention override by using an empty string as the `retention_days` default and always applying tier-based logic when the value is empty or when a `retention_auto_detect: "true"` input flag is set. Address or remove `TOTAL_OUTPUT_TOKENS` to make the token counting semantics explicit. Document the dual-substitution pattern or refactor `SHA` to arrive via bash variable set before the Python block.

---

### Methodological Rigor (0.80/1.00)

**Evidence:**

No changes were made to the methodology in either file. The multi-step structure, token extraction logic, and ceiling enforcement approach are identical to iteration 1. The sound aspects documented in iteration 1 remain present.

**Gaps:**

1. **Ceiling check via stdout string parsing is unchanged.** cost-monitor still launches two separate `uv run python` subprocesses (the token ceiling check at lines 214-231 and the cost ceiling check at lines 234-251) that print "BREACH" or "OK" and are then grep'd. The silent-failure mode — where a Python error produces no stdout and grep finds no "BREACH", allowing a ceiling breach to go undetected — is unaddressed.

2. **`bc` without availability check persists.** Line 167: `$(echo "scale=1; $TOTAL_TOKENS / 1000" | bc 2>/dev/null || echo "0.0")`. `uv run python` is used for all other numeric operations in the file; `bc` is inconsistent and adds an unnecessary dependency.

3. **Auto-discovery tier-prefix ordering persists.** artifact-publish attempts `report-full-${AGENT}.json` before `report-${AGENT}.json` regardless of the current tier. In a smoke evaluation with a shared results directory containing a stale full-tier report, the wrong report could be picked up silently.

**Improvement Path:**

Same as iteration 1: replace stdout-string ceiling checks with exit-code-based Python, replace `bc` with Python, add tier prefix to auto-discovery candidate order.

---

### Evidence Quality (0.83/1.00)

**Evidence:**

No changes to evidence annotations in either file. All strong aspects from iteration 1 remain (FR/MC citations, SHA-pinned references with version comments, cost estimation rationale comment, PR comment citing FR-015/FR-016/FR-017).

**Gaps:**

1. **Promptfoo schema version undocumented.** cost-monitor lines 140-158 parse `data.results[].promptResult.tokenUsage` without citing which promptfoo version or schema version this structure corresponds to. This gap is unaddressed.

2. **Cost estimation rates have no date.** Lines 169-178 estimate cost using `$3/MTok input, $15/MTok output` without a "rates as of {date}" annotation. These rates are time-sensitive and will become inaccurate silently.

**Improvement Path:**

Same as iteration 1: add promptfoo schema version citation; add "rates as of {date}" to cost estimation constants.

---

### Actionability (0.88/1.00)

**Evidence:**

The primary actionability gap from iteration 1 is resolved:

1. **Outputs blocks added — consuming workflows can now reference outputs.** cost-monitor exposes `budget_status`, `estimated_cost_usd`, `total_tokens_k` — a downstream step can do `if: steps.cost-monitor.outputs.budget_status == 'WITHIN_BUDGET'`. artifact-publish exposes `verdict`, `artifact_name`, `comment_posted`. The step IDs are present (`id: enforce-ceiling` in cost-monitor, `id: upload` and `id: pr-comment` in artifact-publish). The `core.setOutput('comment_posted', 'true')` call at artifact-publish line 442 correctly populates the output when a PR comment is posted.

**Gaps:**

1. **`comment_posted` output has no false-case assignment.** artifact-publish sets `comment_posted=true` inside the `pr-comment` step when the comment is posted. However, when `pr_number == '0'` (non-PR context), the `pr-comment` step is skipped entirely via `if: inputs.pr_number != '0'`. A skipped step does not emit any output — `steps.pr-comment.outputs.comment_posted` will be empty string, not `"false"`. A caller comparing against `"false"` for conditional logic will get a silent mismatch. The `comment_posted` output is only reliably populated for the `true` path.

2. **Cost ceiling breach non-actionable via step failure detection.** cost-monitor still emits `::error::` but returns exit 0 on USD ceiling breach (lines 295-300). A caller using `if: failure()` after the cost-monitor step will not trigger on a USD ceiling breach. This limits automated enforcement to inspection of the `budget_status` output (now available) — which is an improvement over iteration 1, but a caller still cannot use the simpler `if: failure()` pattern.

3. **Network requirements for `github-script` undocumented.** artifact-publish does not document that the PR comment step requires outbound HTTPS to `api.github.com`. Self-hosted runner operators with restricted egress have no guidance.

**Improvement Path:**

Emit `comment_posted=false` unconditionally from a step that runs when `pr_number == '0'` (e.g., add to the non-PR summary step at line 447). Evaluate whether USD ceiling breach should be made exit-1 given that outputs now provide an alternative automation path. Add a comment documenting network requirements.

---

### Traceability (0.87/1.00)

**Evidence:**

No changes to traceability annotations in either file. All strong aspects from iteration 1 remain.

**Gaps:**

1. **CG-012 work item ID absent from both files.** Neither file header includes `# CG-012` to link the implementation artifact to its originating gap-closure work item. This gap is unaddressed.

2. **FR-020 absent from artifact-publish FR traceability section.** The file header cites FR-018, MC-30, MC-37 but not FR-020 (CI pipeline integration). FR-020 is cited in cost-monitor line 5 ("FR-020, T-20"). This asymmetry persists.

**Improvement Path:**

Same as iteration 1: add `# CG-012` to both file headers; add `FR-020` to artifact-publish FR traceability section.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.78 | 0.90 | Fix retention-override ambiguity: change `retention_days` default to empty string and apply tier defaults unconditionally when empty; this eliminates the caller-intent-vs-default ambiguity. |
| 2 | Completeness | 0.90 | 0.95 | Replace `date -u --iso-8601=seconds` on artifact-publish line 272 with `date -u +%Y-%m-%dT%H:%M:%SZ`. |
| 3 | Actionability | 0.88 | 0.94 | Emit `comment_posted=false` for non-PR context (add `echo "comment_posted=false" >> "$GITHUB_OUTPUT"` to the non-PR summary step). |
| 4 | Traceability | 0.87 | 0.93 | Add `# CG-012` to both file headers. Add `FR-020` to artifact-publish FR traceability section. |
| 5 | Internal Consistency | 0.78 | 0.90 | Remove or populate `TOTAL_OUTPUT_TOKENS` in cost-monitor — either extract output tokens from promptfoo output or rename the variable to make single-stream semantics explicit. |
| 6 | Methodological Rigor | 0.80 | 0.87 | Replace stdout-string ceiling checks (grep for "BREACH") with exit-code-based Python subprocess; replace `bc` call with `uv run python`. |
| 7 | Evidence Quality | 0.83 | 0.90 | Add promptfoo schema version citation at line 140 of cost-monitor. Add "rates as of 2026-03" annotation to cost estimation constants. |

---

## Iteration Delta Analysis

| Dimension | Iteration 1 | Iteration 2 | Delta | Change Driver |
|-----------|-------------|-------------|-------|---------------|
| Completeness | 0.82 | 0.90 | +0.08 | Outputs blocks added to both actions; cost-monitor date fixed |
| Internal Consistency | 0.72 | 0.78 | +0.06 | Halting contradiction resolved; retention-override and dual-substitution remain |
| Methodological Rigor | 0.80 | 0.80 | 0.00 | No changes applied to this dimension |
| Evidence Quality | 0.83 | 0.83 | 0.00 | No changes applied to this dimension |
| Actionability | 0.78 | 0.88 | +0.10 | Outputs blocks are the primary actionability mechanism |
| Traceability | 0.87 | 0.87 | 0.00 | No changes applied to this dimension |
| **Composite** | **0.797** | **0.854** | **+0.057** | |

**Gap to threshold:** 0.92 - 0.854 = 0.066. The remaining gap is concentrated in Internal Consistency (weight 0.20) and Methodological Rigor (weight 0.20). Closing retention-override alone (+0.12 on IC) would contribute ~0.024 to the composite. Closing the GNU date in artifact-publish (+0.05 on Completeness) contributes ~0.010. Combined, those two targeted fixes could close approximately 0.034 of the 0.066 gap. Full threshold clearance requires also addressing the three unchanged dimensions.

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite was computed
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Internal Consistency: 0.78, not 0.80; Actionability: 0.88, not 0.90, due to comment_posted false-path gap)
- [x] Iteration 2 calibration: composite 0.854 is within the expected 0.85-0.91 REVISE band for partially-revised work; not inflated to reflect intent rather than implementation
- [x] No dimension scored above 0.95 without exceptional evidence (highest is Completeness at 0.90)
- [x] Dimensions with zero revision received zero score improvement (Methodological Rigor, Evidence Quality, Traceability all unchanged at iteration 1 scores)

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.854
threshold: 0.92
weakest_dimension: Internal Consistency
weakest_score: 0.78
critical_findings_count: 0
iteration: 2
prior_score: 0.797
delta: +0.057
gap_to_threshold: 0.066
improvement_recommendations:
  - "Fix retention_days default to empty string in artifact-publish to eliminate caller-intent ambiguity"
  - "Replace date -u --iso-8601=seconds on artifact-publish line 272 with POSIX-portable form"
  - "Emit comment_posted=false in non-PR context step to make output reliable for both paths"
  - "Add CG-012 to both file headers; add FR-020 to artifact-publish FR traceability"
  - "Remove or populate TOTAL_OUTPUT_TOKENS in cost-monitor"
  - "Replace stdout-string ceiling checks with exit-code-based Python; replace bc with uv run python"
  - "Add promptfoo schema version citation and rates-as-of annotation to cost estimation"
```
