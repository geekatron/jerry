# Quality Score Report: CG-012 CI Composite Action Stubs

## L0 Executive Summary

**Score:** 0.797/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Actionability (0.78)
**One-line assessment:** Both composite actions implement the required functional scope with strong FR/MC traceability and a full auto-discovery pipeline, but the absence of an `outputs:` block in both actions, a documented contradiction between the cost-monitor header promise ("alerts and halts") and the actual non-halting behavior, and a GNU-specific `date` flag that will fail on macOS runners keep the composite well below the 0.92 threshold.

---

## Scoring Context

- **Deliverable:** `.github/actions/cost-monitor/action.yml` and `.github/actions/artifact-publish/action.yml`
- **Deliverable Type:** Code (GitHub Actions composite action definitions)
- **Criticality Level:** C2
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.797 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.82 | 0.164 | All major functional areas present; outputs block absent from both actions; GNU-only date flag |
| Internal Consistency | 0.20 | 0.72 | 0.144 | Header says "alerts and halts" but code explicitly does not exit 1; retention override logic silently overrides caller-supplied "30" |
| Methodological Rigor | 0.20 | 0.80 | 0.160 | Multi-step structure is sound; ceiling check via stdout string parsing is fragile; bc fallback lacks quotes |
| Evidence Quality | 0.15 | 0.83 | 0.125 | FR/MC citations throughout; SHA pins with version comments; promptfoo schema version undocumented |
| Actionability | 0.15 | 0.78 | 0.117 | Good usage examples and error messages; callers cannot use cost or status as downstream inputs due to missing outputs block |
| Traceability | 0.10 | 0.87 | 0.087 | FR-005, FR-018, MC-20, MC-30, MC-37 cited consistently; CG-012 work item ID absent from both files |
| **TOTAL** | **1.00** | | **0.797** | |

---

## Detailed Dimension Analysis

### Completeness (0.82/1.00)

**Evidence:**

cost-monitor implements:
- Start phase: records start time to `GITHUB_ENV`, writes markdown table to `GITHUB_STEP_SUMMARY` (lines 65-96)
- Stop phase: reads token counts from `tests/prompt-regression/results/${TIER}-${AGENT}.json` and `smoke-${AGENT}.json` (lines 117-153); handles two promptfoo output shapes (list vs. dict)
- USD estimation: documented 70%/30% input/output split at claude-sonnet rates (lines 160-167)
- Ceiling enforcement: `::warning::` for token breach, `::error::` for USD breach (lines 210-239)
- Structured cost record written to JSON for downstream artifact collection (lines 258-274)
- Phase validation: non-start/non-stop inputs exit 1 (lines 288-293)

artifact-publish implements:
- File auto-discovery: three-tier candidate search per file type (lines 162-207)
- Metadata generation: agent, tier, commit SHA, timestamp, verdict, p-value (lines 266-306)
- Artifact upload: 4 separate upload steps with `actions/upload-artifact@ea165f8d65b6e75b540449bea1e5c8c7e45e428` (SHA-pinned, v4.6.2)
- PR comment posting: `actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea` (SHA-pinned, v7.0.1)
- Tier-appropriate retention: smoke=7, standard=30, full=90 days (lines 132-138)
- Non-PR step summary fallback (lines 427-470)

**Gaps:**

1. Neither action declares an `outputs:` block. cost-monitor writes `COST_MONITOR_TOTAL_TOKENS`, `COST_MONITOR_ESTIMATED_COST`, and `COST_MONITOR_TOTAL_TOKENS_K` to `GITHUB_ENV` but does not expose them as composite action outputs. Callers cannot reference `steps.cost-monitor.outputs.estimated_cost` or `steps.cost-monitor.outputs.budget_status` from the consuming workflow. artifact-publish similarly exposes nothing as outputs (verdict, retention, run_id computed internally but unreachable by callers).

2. `date -u --iso-8601=seconds` (cost-monitor line 95; artifact-publish line 261) uses a GNU coreutils flag (`--iso-8601`) that is not available on macOS runners. GitHub-hosted runners default to `ubuntu-latest`, so this is safe for the current pipeline, but cross-platform portability is broken. The POSIX-portable form is `date -u +%Y-%m-%dT%H:%M:%SZ`.

3. The CG-012 requirements specify "SHA-pinned action references where possible." Both actions SHA-pin `upload-artifact` and `github-script`. However, `actions/checkout` is not used in either action, and no other external actions are used — so the SHA-pinning requirement is fully satisfied for all referenced external actions. This is not a gap.

**Improvement Path:**

Add `outputs:` block to both actions. For cost-monitor: expose `budget_status`, `estimated_cost_usd`, `total_tokens_k`. For artifact-publish: expose `verdict`, `artifact_names`. Replace `--iso-8601=seconds` with `+%Y-%m-%dT%H:%M:%SZ`.

---

### Internal Consistency (0.72/1.00)

**Evidence:**

Consistent aspects:
- `agent_id` / `agent_name` dual-input strategy is handled consistently in artifact-publish: `agent_id` takes precedence, fallback to `agent_name`, error if both empty (lines 109-116).
- Retention tier defaults (7/30/90) are consistent between the file header comment (lines 19-22) and the bash case statement (lines 133-138).
- The `BUDGET_ICON` variable is used consistently throughout the stop phase.

**Gaps:**

1. **Critical contradiction — halting behavior:** cost-monitor header (line 5-6) states the action "alerts and halts on breach." The `description:` field (line 39) states "Enforces per-workflow budget ceilings." However, lines 277-283 contain an explicit developer comment: "We do NOT exit 1 here. The evaluation result is the primary gate. Cost ceiling breach is reported but does not override the regression verdict." The action emits `::error::` annotations but returns exit code 0 on USD ceiling breach. This is a meaningful behavioral contradiction between the stated contract and the implementation.

2. **Retention override silently swallows caller intent:** In artifact-publish, lines 131-138 override `RETENTION` if the value equals "30" (the default). A caller who intentionally passes `retention_days: "30"` expecting 30 days for a full-tier run will silently have that overridden to 90. The condition `if [ "$RETENTION" = "30" ]` cannot distinguish "caller used the default" from "caller explicitly chose 30 days." This is an input contract violation.

3. **Metadata output path mixes bash variable expansion with Python f-string:** Line 301 in artifact-publish: `output_path = f'tests/prompt-regression/results/metadata-${AGENT}.json'` — the `${AGENT}` is bash-substituted before the Python runs (this works), but `${{ github.sha }}` on line 263 appears inside a `uv run python -c "..."` block where GHA expression substitution is applied to the run block contents before bash executes it. This works but creates a mixing of two substitution passes that is architecturally fragile and could silently break if the action is ever called in a context where GHA expressions are not resolved.

**Improvement Path:**

Resolve the halting contradiction: either change the header to say "alerts only" or implement actual exit-1 behavior on USD ceiling breach. Fix the retention override logic to distinguish explicit "30" from default "30" (e.g., use a separate `retention_auto_detect` boolean input or use an empty default and always apply tier logic). Document the dual-substitution pattern or refactor to pass `SHA` as a bash variable.

---

### Methodological Rigor (0.80/1.00)

**Evidence:**

Sound aspects:
- Multi-step composite structure separates concerns correctly: resolve → autodiscover → validate → metadata → upload → PR comment.
- Token extraction handles both `results` as list and as dict (lines 133-146 of cost-monitor) — this shows awareness of promptfoo output format variance.
- Phase input validation with explicit exit 1 on invalid phase (lines 288-293 of cost-monitor) is correct defensive programming.
- Artifact validation uses an array accumulator (`MISSING=()`) and warns without blocking (soft failure, correct for the use case).
- `uv run python` is used consistently throughout, satisfying H-05.
- `if-no-files-found: warn` on all upload steps is appropriate — allows graceful degradation when optional files are absent.

**Gaps:**

1. **Ceiling check via stdout string parsing:** cost-monitor launches two separate `uv run python` subprocesses (lines 202-212 and 222-232) that print "BREACH" or "OK" to stdout, which is then grep'd. This is functional but fragile. A simpler and more reliable approach would be arithmetic comparison in bash (`$(echo "${ACTUAL_K} > ${CEILING_K}" | bc)`) or a single Python script with exit codes. The current approach also uses `|| { echo "::warning::..."; }` to suppress errors, but if the Python script itself exits 0 with no output, the grep silently produces no match (no BREACH detected), which could mask errors.

2. **`bc` usage without availability check:** Line 156 of cost-monitor: `$(echo "scale=1; $TOTAL_TOKENS / 1000" | bc 2>/dev/null || echo "0.0")`. The `bc` utility is available on ubuntu-latest but is not guaranteed across all runner environments. The fallback to `0.0` is silent. A `uv run python` alternative (already used elsewhere in the file) would be more consistent.

3. **Auto-discovery candidate priority:** artifact-publish tries `report-full-${AGENT}.json` before `report-${AGENT}.json` (lines 166-170). The "full-" prefix suggests tier-specific output, but the auto-discovery does not constrain by tier. In a `smoke` evaluation, the action might accidentally pick up a stale `report-full-${AGENT}.json` from a previous `full` run if the results path is shared. A tier-aware discovery order would be safer.

**Improvement Path:**

Replace stdout-string ceiling checks with bash arithmetic or single Python exit-code approach. Replace `bc` with `uv run python` for consistency. Add tier prefix constraint to auto-discovery candidate order.

---

### Evidence Quality (0.83/1.00)

**Evidence:**

Strong aspects:
- FR traceability headers in both files cite specific requirement IDs: FR-005, FR-018, MC-20, MC-30, MC-37 (cost-monitor lines 31-33; artifact-publish lines 28-30).
- SHA-pinned references include version comments: `# v4.6.2` and `# v7.0.1` (artifact-publish lines 313, 322, 331, 339, 351).
- Token cost rate rationale is documented: "approximate: claude-sonnet $3/MTok input, $15/MTok output" with the 70%/30% split noted as a "conservative estimate" (lines 158-159 of cost-monitor).
- Retention policy tiers are documented in the file header with explicit day counts (artifact-publish lines 19-22).
- PR comment text cites statistical method standards: "Wilcoxon signed-rank + Wilson CIs + Bonferroni correction (FR-015, FR-016, FR-017)" (line 412 of artifact-publish).

**Gaps:**

1. The token extraction logic in cost-monitor (lines 132-148) parses a specific promptfoo JSON output structure (`data.results[].promptResult.tokenUsage`) without citing which promptfoo version or output schema this corresponds to. If promptfoo changes its output format, the extraction silently returns 0 — with no version constraint documented, this is an invisible dependency.

2. The cost estimation model (70/30 split, claude-sonnet rates) has no citation or date. These rates are time-sensitive; without a "as of {date}" note, the model will silently become inaccurate as Anthropic adjusts pricing.

**Improvement Path:**

Add a comment citing the promptfoo output schema version or link to the promptfoo documentation. Add a "rates as of {date}" annotation to the cost estimation constants.

---

### Actionability (0.78/1.00)

**Evidence:**

Strong aspects:
- Both files include complete `Usage:` example blocks in the header with realistic input values (cost-monitor lines 8-24; artifact-publish lines 8-16).
- Error messages include operator remediation guidance: "Review evaluation tier configuration and N_RUNS setting" (cost-monitor line 218), "Reduce N_RUNS, switch to a cheaper tier, or increase the ceiling" (line 238).
- artifact-publish `agent_id`/`agent_name` backward-compatibility design allows callers to migrate gradually.
- The `results_path` auto-discovery feature reduces caller boilerplate — callers can specify a directory rather than 3 separate file paths.

**Gaps:**

1. **No outputs block in either action** — this is the primary actionability gap. Downstream workflow steps cannot make conditional decisions based on cost-monitor's budget status or artifact-publish's verdict without reading files from disk. For example, a workflow cannot do `if: steps.cost-monitor.outputs.budget_status == 'WITHIN_BUDGET'` because no outputs are declared. This requires callers to parse `GITHUB_ENV` or disk files as workarounds.

2. **cost-monitor ceiling breach is non-actionable:** The action emits `::error::` but returns exit 0. A calling workflow step that checks `if: failure()` after the cost-monitor step will not trigger. The only remediation available is inspecting the step summary manually — which is not automatable.

3. **artifact-publish does not validate `actions/github-script` is available** before attempting to post a PR comment. In environments where the action's runner does not have network access (e.g., self-hosted runners with restricted egress), the step will fail silently or with an unhelpful error. A pre-flight check or clear documentation of network requirements would make the action more actionable for self-hosted runner operators.

**Improvement Path:**

Add `outputs:` blocks to both actions. cost-monitor: `budget_status`, `estimated_cost_usd`, `total_tokens_k`, `breach`. artifact-publish: `verdict`, `comment_posted`. Implement exit-1 on USD ceiling breach if the design intent is to halt. Document network requirements for the PR comment step.

---

### Traceability (0.87/1.00)

**Evidence:**

Strong aspects:
- Both files open with structured FR/MC traceability tables in the file header comments.
- cost-monitor cites: FR-005 (tiered cost management), MC-20 (budget ceiling), MC-37 (audit trail).
- artifact-publish cites: FR-018 (regression report with PR integration), MC-30 (result persistence), MC-37 (audit trail).
- Inline comments reference the originating control at the point of implementation: `# MC-20: Enforce per-workflow budget ceilings` (line 183), `# MC-37: Every evaluation result artifact includes complete metadata` (lines 256-257).
- SHA-pinned action references are fully traceable to specific upstream releases.
- Stream identifier (3E: CI/CD Pipeline Setup) is declared in both files.
- The workflow file (`prompt-regression-standard.yml`) correctly invokes cost-monitor with matching parameters, confirming FR-020 CI pipeline integration compatibility.

**Gaps:**

1. **CG-012 work item ID is absent from both files.** All other scored deliverables in this orchestration run include their work item ID in file headers. The absence of `CG-012` prevents tracing these files back to the gap-closure work item from the file alone.

2. **FR-020 is cited in the file header of cost-monitor** (line 5: "FR-020, T-20") but is not cited in artifact-publish's FR traceability section, despite artifact-publish being equally required by FR-020 (CI pipeline integration).

**Improvement Path:**

Add `# CG-012` to the header comments of both files. Add `FR-020` to the artifact-publish FR traceability section.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.72 | 0.88 | Resolve cost-monitor halting contradiction: change header to "alerts only" or implement `exit 1` on USD ceiling breach (not just `::error::` annotation). |
| 2 | Completeness | 0.82 | 0.92 | Add `outputs:` block to both composite actions exposing budget_status/estimated_cost_usd/total_tokens_k (cost-monitor) and verdict/comment_posted (artifact-publish). |
| 3 | Internal Consistency | 0.72 | 0.88 | Fix retention override logic in artifact-publish: cannot distinguish caller-supplied "30" from default "30" — use empty default and always apply tier logic. |
| 4 | Completeness | 0.82 | 0.92 | Replace `date --iso-8601=seconds` with POSIX-portable `date +%Y-%m-%dT%H:%M:%SZ` in both files (both occurrences). |
| 5 | Methodological Rigor | 0.80 | 0.88 | Replace stdout-string ceiling check (grep for "BREACH") with a single Python script using exit codes, eliminating the silent-zero-output failure mode. |
| 6 | Traceability | 0.87 | 0.92 | Add `# CG-012` to header of both files. Add `FR-020` to artifact-publish FR traceability section. |
| 7 | Evidence Quality | 0.83 | 0.90 | Add promptfoo schema version citation to token extraction comment. Add "rates as of {date}" annotation to cost estimation constants. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite was computed
- [x] Evidence documented for each score with specific line references
- [x] Uncertain scores resolved downward (Internal Consistency: 0.72 not 0.75; Actionability: 0.78 not 0.80)
- [x] First-draft calibration considered — composite 0.797 is within the expected 0.70-0.84 REVISE band
- [x] No dimension scored above 0.95 without exceptional evidence (highest is Traceability at 0.87)
