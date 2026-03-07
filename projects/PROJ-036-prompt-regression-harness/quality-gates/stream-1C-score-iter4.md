# Quality Score Report: Stream 1C -- Baseline Generation Protocol (Iteration 4)

## L0 Executive Summary

**Score:** 0.939/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality / Traceability (0.93)
**One-line assessment:** Fix 1 (rounding arithmetic) is partially effective -- protocol.md is now internally consistent, but `example-run.json` retains `"weighted_composite": 0.749`, leaving a cross-file discrepancy that keeps Internal Consistency at 0.95; Fix 2 (glob path) is replaced by a deferred-resolution footnote that is honest but does not resolve the sigma data provenance gap; composite 0.939 falls below the 0.94 stream threshold.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/baselines/` (protocol.md v1.3.0 + 3 schemas + example-run.json + 5 prompt YAML files = 10 files scored as a unit)
- **Deliverable Type:** Protocol/Schema/Prompt set (hybrid)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 4 (scored independently; iter3 score was 0.938)
- **Stream Threshold:** 0.94
- **Prior Score:** 0.938 (iter3)
- **Strategy Findings Incorporated:** Yes -- iter3 adv-scorer report used only to verify which fixes to check, not to inflate scores

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.939 |
| **Stream Threshold** | 0.94 |
| **H-13 Threshold** | 0.92 |
| **Verdict** | REVISE (below 0.94 stream threshold) |
| **Strategy Findings Incorporated** | Yes -- iter3 report (fix verification only) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | All 5 agents, full lifecycle phases, 8 script interfaces with docstrings, G-Eval criteria; Group 3 scripts remain unimplemented stubs |
| Internal Consistency | 0.20 | 0.95 | 0.190 | Protocol.md rounding footnote now fully self-consistent (0.744 via traced arithmetic); but example-run.json retains 0.749 and its composite_verification note still says "stored as 0.749" -- cross-file discrepancy blocks further increase |
| Methodological Rigor | 0.20 | 0.94 | 0.188 | Three independent statistical arguments; Dror et al. [6] adds NLP-specific justification for Wilcoxon; Noether limitation disclosed; Monte Carlo simulation still absent |
| Evidence Quality | 0.15 | 0.93 | 0.1395 | Six complete citations with stable URLs; [^proj017-path] footnote replaces glob with honest deferred-resolution disclosure; sigma data source remains unconfirmed; cost estimate rates unstated |
| Actionability | 0.15 | 0.94 | 0.141 | --eval-mode skip to "not_evaluated" mapping documented; 8 script interfaces with docstrings; Group 3 script stubs absent -- Phase 0 still fails at execution |
| Traceability | 0.10 | 0.93 | 0.093 | ADR-001 qualified as PROJ-035; behavior IDs linked in all 5 prompts; [^proj017-path] footnote now documents ambiguity explicitly; sigma data source path remains unresolved |
| **TOTAL** | **1.00** | | **0.9375** | |

**Composite verification:**
(0.93 * 0.20) + (0.95 * 0.20) + (0.94 * 0.20) + (0.93 * 0.15) + (0.94 * 0.15) + (0.93 * 0.10)
= 0.186 + 0.190 + 0.188 + 0.1395 + 0.141 + 0.093
= **0.9375**

Rounded to 3 decimal places: **0.938**. Rounded to 2 decimal places for display: **0.94** -- but the exact value is 0.9375, which is below the 0.94 stream threshold. The verdict is **REVISE**.

> **Anti-leniency note on rounding:** The computed exact value is 0.9375. The stream threshold is 0.94. 0.9375 < 0.94. No rounding convention converts 0.9375 to a value that meets 0.94. REVISE is the correct verdict.

---

## Fix Verification Checklist (Iter4 Targeted Fixes)

| Iter4 Fix | Applied? | Effective? | Evidence |
|-----------|----------|------------|----------|
| Fix 1a: Correct `weighted_composite` in schema table (protocol.md) from 0.749 to 0.744 | YES | YES | Protocol.md line 358: `\| \`scores.weighted_composite\` \| number \| ... \| \`0.744\`` |
| Fix 1b: Correct `weighted_composite` in JSON code block (protocol.md inline) from 0.749 to 0.744 | YES | YES | Protocol.md line 751: `"weighted_composite": 0.744` |
| Fix 1c: Correct rounding footnote arithmetic to trace 0.1065 -> 0.107 -> sum 0.744 | YES | YES | Protocol.md line 775: full banker's rounding trace, sum 0.164+0.156+0.150+0.107+0.102+0.065=0.744, delta of 0.0005 explained |
| Fix 1d: Correct `weighted_composite` in `example-run.json` from 0.749 to 0.744 | NO | NO | `schemas/examples/example-run.json` line 28: `"weighted_composite": 0.749` -- unchanged |
| Fix 1e: Correct composite_verification metadata note in `example-run.json` | NO | NO | Line 46: `"composite_verification": "...= 0.7435 (stored as 0.749 due to per-step rounding...)"` -- still claims 0.749 |
| Fix 2: Replace PROJ-017 glob path with concrete footnote | YES | PARTIAL | Protocol.md line 70 now references `[^proj017-path]`; line 1113 footnote documents the path ambiguity and defers to implementing engineer; glob removed but sigma data source remains unresolved |

**Critical gap from Fix 1:** The iter4 revision note in the protocol footer (line 1118) claims "corrected weighted_composite from 0.749 to 0.744 in JSON record." This was applied to the inline JSON code block inside protocol.md but NOT to the standalone `example-run.json` file. The `example-run.json` is the machine-readable artifact that validators and downstream tooling will consume. Its `weighted_composite: 0.749` and composite_verification note contradict the corrected protocol.md values. The fix is incomplete.

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Rubric criteria for 0.9+:** All requirements addressed with depth.

**Evidence:**

Unchanged from iter3. The deliverable covers all 14 navigation sections, all 5 agent prompt files with G-Eval criteria, all 8 script interfaces with docstrings and argument signatures, sample run record in two forms (protocol.md inline and example-run.json), and full lifecycle phases 0-6. The iter4 revision made no structural additions to completeness.

**Gaps:**

The Group 3 scripts remain unimplemented (stubs/interfaces only). The iter4 changes did not address this. A practitioner cannot execute Phase 0 Step 0.4 (`validate_environment.py`) without implementing the script. For a protocol whose status is "READY FOR EXECUTION," this is the dominant completeness residual, unchanged since iter1.

**Why score is held at 0.93 and not raised:**

No completeness-impacting changes were made in iter4. Leniency rule: when no change occurs, score does not drift upward.

**Improvement Path:**

Implement trivial script stubs (`sys.exit(1)` with "Not yet implemented") for all 8 scripts. Score would move toward 0.95+.

---

### Internal Consistency (0.95/1.00)

**Rubric criteria for 0.9+:** No contradictions, all claims aligned.

**Evidence for current score:**

The iter4 rounding fix was applied to three locations in protocol.md, and all three are now internally consistent:

1. **Schema table (line 358):** `0.744` -- corrected from 0.749.
2. **Inline JSON code block (line 751):** `0.744` -- corrected from 0.749.
3. **Rounding footnote (line 775):** The full arithmetic chain is now traced: `0.71 * 0.15 = 0.1065`, banker's rounding rounds 0.1065 to 0.107 (the trailing 5 rounds up), then `0.164 + 0.156 + 0.150 + 0.107 + 0.102 + 0.065 = 0.744`. The delta of 0.0005 from the unrounded sum (0.7435) is explained as accumulated rounding artifact. This is mathematically correct and self-verifying.

The protocol.md internal arithmetic chain is now fully traceable and self-consistent.

**Residual gap blocking higher score:**

`example-run.json` -- the standalone JSON artifact at `schemas/examples/example-run.json` -- still contains `"weighted_composite": 0.749` (line 28) and the metadata composite_verification field still reads "stored as 0.749 due to per-step rounding in reference implementation" (line 46). This file contradicts the corrected protocol.md values. The 10-file deliverable is scored as a unit; a cross-file contradiction between `example-run.json` and the corrected protocol.md prevents this dimension from moving above 0.95.

The iter4 fix is incomplete: it corrected protocol.md but not the JSON artifact that the fix explicitly claimed to correct ("corrected weighted_composite from 0.749 to 0.744 in JSON record" -- protocol.md line 1118 footer).

**Why 0.95 is retained rather than lowered:**

The intra-protocol.md consistency is now strong. The cross-file discrepancy with example-run.json is a real gap but the protocol.md rounding footnote is now demonstrably self-consistent and technically correct. Holding at 0.95 (not raising to 0.96 as targeted, not lowering from iter3's 0.95) reflects the partial fix effectiveness.

**Improvement Path:**

Update `schemas/examples/example-run.json` line 28 to `"weighted_composite": 0.744` and update the `composite_verification` metadata note to reflect the corrected value. This single-file change would close the cross-file inconsistency.

---

### Methodological Rigor (0.94/1.00)

**Rubric criteria for 0.9+:** Rigorous methodology, well-structured.

**Evidence:**

Unchanged from iter3. Three independent statistical arguments remain intact. Dror et al. [6] adds NLP-literature justification for Wilcoxon over parametric tests. The Note on [3] (line 1107) correctly explains Noether's formula is a conservative lower bound due to the sign test / Wilcoxon ARE of 3/pi ≈ 0.955. The Note on [6] (line 1109) documents the Dror et al. finding precisely.

Iter4 made no changes to the statistical methodology sections. The score is unchanged at 0.94.

**Residual gap:**

Monte Carlo power simulation for the Wilcoxon test at N=30, sigma=0.10 remains absent. The Noether formula provides only a conservative lower bound (~78% power). An empirical simulation would replace this with an actual Wilcoxon power estimate. This was Priority 3 in iter3 and remains unaddressed.

**Improvement Path:**

Add Monte Carlo simulation result: "10,000-iteration simulation confirms approximately X% power for Wilcoxon signed-rank at N=30 and sigma=0.10." Would move dimension to 0.97+.

---

### Evidence Quality (0.93/1.00)

**Rubric criteria for 0.9+:** All claims with credible citations.

**Evidence:**

Six citations [1]-[6] remain complete and unchanged from iter3. The Dror et al. [6] ACL 2018 citation with stable ACL Anthology URL is intact.

The iter4 Fix 2 replaced the glob pattern `projects/PROJ-017-*/orchestration/*/phase-5/` with inline text plus a `[^proj017-path]` footnote. The footnote (line 1113) reads: "PROJ-017 Phase 5 sigma data: the exact file path depends on which PROJ-017 workstream produced the Phase 5 evaluation (the repository contains both `PROJ-017-llm-skill-testing` and `PROJ-017-portability`). The estimated sigma range 0.08-0.12 is the calibration input for this protocol regardless of exact file location; the implementing engineer should confirm the path during initial harness setup by inspecting the applicable PROJ-017 orchestration directory for phase-5 score output files."

**Assessment of Fix 2:**

This is an honest, informative improvement over the prior glob pattern. It acknowledges the ambiguity, identifies the source of the ambiguity (two candidate PROJ-017 directories), and makes clear that the sigma range is the operative calibration input regardless of path. The path confirmation is deferred to implementation time with explicit instructions. This is a legitimate documentation approach for a data source whose location requires runtime discovery.

However, it does not resolve the core evidence quality gap: the sigma estimates underpinning N=30 are still not traceable to a specific, readable file. A reader cannot independently verify the 0.08-0.12 sigma range without running an implementation-time lookup. The rubric criterion for 0.9+ is "all claims with credible citations" -- the sigma claims now have better disclosure of their sourcing status but remain unverified.

**Score held at 0.93** (not raised to 0.94 as targeted): The footnote is an improvement in disclosure quality but the underlying citation gap (unresolvable path) persists. Cost estimate token rates also remain unstated.

**Why not below 0.93:**

The six formal citations [1]-[6] are complete and credible. The sigma disclosure now explicitly flags the path-confirmation requirement rather than presenting a glob as if it were a resolvable reference. The honest footnote is a genuine improvement over a misleading glob.

**Improvement Path:**

Confirm which PROJ-017 directory contains the Phase 5 evaluation data and replace the deferred footnote with an exact file path (e.g., `projects/PROJ-017-llm-skill-testing/orchestration/phase5-eval-20260220/score-summaries/agent-score-stdev.json`). Add input/output token rates used for cost estimates.

---

### Actionability (0.94/1.00)

**Rubric criteria for 0.9+:** Clear, specific, implementable actions.

**Evidence:**

Unchanged from iter3. The `--eval-mode skip` to `"not_evaluated"` mapping documentation (line 362) remains present. All 8 script interfaces with docstrings and default flags remain intact. H-05-compliant Step 0.5 is unchanged. G-Eval criteria strings are in directly usable format.

Iter4 made no changes to actionability-relevant content. The score is unchanged at 0.94.

**Residual gap:**

Scripts remain unimplemented. A practitioner following this protocol reaches a hard stop at Phase 0 Step 0.4 (`validate_environment.py`). The `re_evaluate.py` script referenced in the `--eval-mode skip` mapping documentation is also unimplemented.

**Improvement Path:**

Same as Completeness: implement trivial script stubs to enable Phase 0 execution.

---

### Traceability (0.93/1.00)

**Rubric criteria for 0.9+:** Full traceability chain.

**Evidence:**

The three iter1 traceability fixes (ADR-001 qualified as PROJ-035, quality-enforcement.md cited in Data Collection Schema, behavior IDs linked to behavioral-contracts.md in all 5 prompt files) remain resolved from iter2 and intact.

The iter4 [^proj017-path] footnote (line 1113) is an improvement for traceability: it documents why the exact path is not available at authoring time (two candidate PROJ-017 directories), which is more traceable than a glob that could match multiple directories. The footnote now makes the traceability gap explicit and actionable.

The footer (line 1119) retains the evidence basis declaration linking the protocol to PROJ-035 ADR-001, PROJ-017 Phase 5, and all four cited statistical references.

**Residual gap:**

The PROJ-017 Phase 5 sigma data source remains the primary traceability residual. The footnote improves transparency but the trace chain from the sigma claim to verifiable data remains broken. The `behavioral-contracts.md` file existence and section structure (A.1, B, C as referenced in all 5 prompt files) cannot be confirmed from this scoring context.

**Score held at 0.93:** The [^proj017-path] footnote is a genuine improvement in honesty about the traceability gap but does not close it. The score matches iter3 because the underlying gap persists, differently disclosed.

**Improvement Path:**

Same as Evidence Quality: resolve the PROJ-017 path to an exact file. Confirm `contracts/behavioral-contracts.md` exists with Sections A, B, C.

---

## Anti-Leniency Assessment

### Calibration Check

The 0.94 stream threshold is higher than the standard H-13 threshold (0.92). Scores that would PASS the H-13 gate may still REVISE under the stream threshold. This is the operative condition: the deliverable at 0.9375 (exact) clears H-13 but falls 0.0025 short of the 0.94 stream threshold.

### Dimension-by-Dimension Leniency Check

**Internal Consistency (held at 0.95, not raised to 0.96):**

The iter4 fix was expected to raise Internal Consistency from 0.95 to 0.96. The fix partially succeeded: protocol.md is now internally self-consistent with verifiable arithmetic. However, `example-run.json` retains 0.749, contradicting the corrected protocol.md. Under the rubric criterion "no contradictions, all claims aligned," a cross-file contradiction between the standalone JSON artifact and the protocol document is a real, specific contradiction. Holding at 0.95 is correct; raising to 0.96 is not supported.

**Evidence Quality (held at 0.93, not raised to 0.94):**

The iter4 fix was expected to raise Evidence Quality from 0.93 to 0.94. The fix improved disclosure of the path ambiguity via a clear footnote. However, the sigma data source remains unresolvable without implementation-time discovery. "All claims with credible citations" -- the sigma claim's citation now has a disclosure gap rather than a glob, which is better disclosure but not resolution. Holding at 0.93 is correct.

**Composite arithmetic temptation:**

0.9375 could be rounded to 0.938, which visually approximates 0.94 (two decimal places). The stream threshold is 0.94, not 0.938. Anti-leniency rule: when uncertain between adjacent scores, choose the lower interpretation. 0.9375 < 0.94 is unambiguous; no favorable rounding applies.

### Specific Leniency Temptations Counteracted

1. **"The rounding fix is mostly right."** The protocol.md arithmetic is now clean and correct. Temptation: award 0.96 on Internal Consistency for the quality of the fix. Held at 0.95 because the JSON artifact was not updated, creating a concrete, specific cross-file contradiction that the rubric addresses directly.

2. **"The footnote is better than a glob."** The [^proj017-path] footnote is genuinely better than a glob: it is honest, it identifies the source of ambiguity, and it provides implementation-time resolution instructions. Temptation: award 0.94 on Evidence Quality. Held at 0.93 because the underlying evidence (sigma estimates) remains unverified against a specific readable file.

3. **"0.9375 rounds to 0.94."** Strictly false when the threshold is 0.94 (not 0.93x). 0.9375 < 0.94 is the arithmetic fact. REVISE is the required verdict.

4. **"Iter4 made real improvements."** This is true and appropriate for future iterations. Fix 1 protocol.md component is a genuine, clean improvement. Fix 2 is a genuine improvement in transparency. These improvements are reflected in the scores not decreasing from iter3, despite the incomplete fix. They are not sufficient to cross the 0.94 threshold.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.95 | 0.96 | Update `schemas/examples/example-run.json` line 28 to `"weighted_composite": 0.744` and update the `composite_verification` metadata note (line 46) to reflect the corrected per-step rounding sum. This is the single highest-leverage change -- it completes the Fix 1 that was partially applied and closes the only cross-file arithmetic contradiction. Composite impact: +0.002 weighted. |
| 2 | Evidence Quality | 0.93 | 0.94 | Resolve the PROJ-017 Phase 5 sigma data path from the `[^proj017-path]` footnote to an exact file path by inspecting the repository. Replace the deferred footnote with a concrete path (e.g., `projects/PROJ-017-llm-skill-testing/.../phase-5/score-stdev.json`). Add input/output token rates used for cost estimates. Composite impact: +0.0015 weighted. |
| 3 | Traceability | 0.93 | 0.94 | Confirm `contracts/behavioral-contracts.md` exists and contains Sections A, B, C as referenced in all 5 prompt YAML files. Provide the exact PROJ-017 Phase 5 path. Composite impact: +0.001 weighted. |
| 4 | Methodological Rigor | 0.94 | 0.96 | Add Monte Carlo power simulation result for Wilcoxon at N=30, sigma=0.10. Replaces conservative Noether bound with empirical estimate. Composite impact: +0.004 weighted. |
| 5 | Completeness / Actionability | 0.93 / 0.94 | 0.95+ | Implement trivial script stubs for all 8 scripts (sys.exit(1) with "Not yet implemented") so Phase 0 Step 0.4 is at minimum runnable. Composite impact: +0.003 weighted. |

**Minimum path to 0.94 stream threshold:**

Priority 1 alone (fix example-run.json) raises Internal Consistency from 0.95 to 0.96, adding +0.002 to the weighted composite (0.9375 + 0.002 = 0.9395). This is still below 0.94.

Priority 1 + Priority 2 raises Evidence Quality from 0.93 to 0.94, adding +0.0015. Total: 0.9395 + 0.0015 = 0.941. This crosses the 0.94 stream threshold.

**Recommended iter5 target:** Fix Priority 1 (example-run.json) and Priority 2 (PROJ-017 path resolution). Expected iter5 composite: ~0.941, verdict PASS.

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Internal Consistency held at 0.95 not raised; Evidence Quality held at 0.93 not raised)
- [x] First-draft calibration not applicable (this is iteration 4; scored against rubric, not iteration-relative)
- [x] No dimension scored above 0.95 without exceptional evidence (Internal Consistency is the highest at 0.95; the cap is justified by the protocol.md self-consistency, held back by the example-run.json contradiction)
- [x] Composite threshold not rounded favorably (0.9375 < 0.94 is the exact comparison; REVISE not PASS)

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.9375
threshold_stream: 0.94
threshold_h13: 0.92
weakest_dimension: evidence_quality
weakest_score: 0.93
critical_findings_count: 0
iteration: 4
improvement_recommendations:
  - "PRIORITY 1: Update example-run.json weighted_composite from 0.749 to 0.744 and correct composite_verification metadata note -- Fix 1 was applied to protocol.md but not to the JSON artifact"
  - "PRIORITY 2: Resolve PROJ-017 Phase 5 sigma data exact file path from the deferred [^proj017-path] footnote to a concrete, verifiable path"
  - "PRIORITY 3: Confirm contracts/behavioral-contracts.md exists with Sections A, B, C as referenced in all 5 prompt YAML files"
  - "Add Monte Carlo power simulation result for Wilcoxon at N=30 to replace conservative Noether bound"
  - "Implement trivial script stubs for all 8 scripts to close Phase 0 execution gap"
minimum_iter5_path: "Fix example-run.json (P1) + resolve PROJ-017 path (P2) = estimated composite 0.941, crossing 0.94 threshold"
```

---

*Score Report Version: 1.0*
*Scoring Agent: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Produced: 2026-03-07*
*Stream: 1C -- Baseline Capture Protocol and Schemas*
*Iteration: 4 of N*
