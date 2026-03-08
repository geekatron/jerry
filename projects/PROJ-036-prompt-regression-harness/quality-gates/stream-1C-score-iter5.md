# Quality Score Report: Stream 1C -- Baseline Generation Protocol (Iteration 5)

## L0 Executive Summary

**Score:** 0.9395/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness / Evidence Quality / Traceability (tied at 0.93)
**One-line assessment:** The iter5 fix (example-run.json weighted_composite and composite_verification corrected from 0.749 to 0.744) is confirmed fully effective, closing the cross-file arithmetic contradiction that blocked Internal Consistency; IC rises from 0.95 to 0.96 and the composite moves from 0.9375 to 0.9395, but 0.9395 remains below the 0.94 stream threshold -- REVISE verdict stands by 0.0005.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/baselines/` (protocol.md v1.3.0 + 3 schemas + example-run.json + 5 prompt YAML files = 10 files scored as a unit)
- **Deliverable Type:** Protocol/Schema/Prompt set (hybrid)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 5 (scored independently; iter4 score was 0.9375)
- **Stream Threshold:** 0.94
- **H-13 Threshold:** 0.92
- **Prior Score:** 0.9375 (iter4)
- **Strategy Findings Incorporated:** Yes -- iter4 report used for fix verification context only, not to inflate scores

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.9395 |
| **Stream Threshold** | 0.94 |
| **H-13 Threshold** | 0.92 |
| **Verdict** | REVISE (below 0.94 stream threshold) |
| **Strategy Findings Incorporated** | Yes -- iter4 report (fix verification only) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.93 | 0.186 | All 5 agents, full lifecycle phases, 8 script interfaces with docstrings, G-Eval criteria; Group 3 scripts remain unimplemented stubs |
| Internal Consistency | 0.20 | 0.96 | 0.192 | Iter5 fix confirmed complete: example-run.json now reads 0.744 and composite_verification reflects per-step rounding sum; 0.749 appears only in revision history; minor metadata mismatch (frontmatter "Iteration: 3" vs. footer "Revision: Iteration 4") prevents reaching 0.97 |
| Methodological Rigor | 0.20 | 0.94 | 0.188 | Three independent statistical arguments; Dror et al. [6] NLP-specific justification intact; Monte Carlo simulation absent; unchanged from iter4 |
| Evidence Quality | 0.15 | 0.93 | 0.1395 | Six complete citations [1]-[6] with stable URLs; sigma data source remains unverifiable without implementation-time discovery; cost estimate token rates unstated; unchanged from iter4 |
| Actionability | 0.15 | 0.94 | 0.141 | --eval-mode skip mapping documented; 8 script interfaces with docstrings; scripts unimplemented (Phase 0 execution blocked); unchanged from iter4 |
| Traceability | 0.10 | 0.93 | 0.093 | ADR-001 qualified as PROJ-035; behavior IDs linked in all 5 prompts; [^proj017-path] footnote documents ambiguity; sigma trace remains unresolved; unchanged from iter4 |
| **TOTAL** | **1.00** | | **0.9395** | |

**Composite verification (exact arithmetic):**

```
(0.93 * 0.20) + (0.96 * 0.20) + (0.94 * 0.20) + (0.93 * 0.15) + (0.94 * 0.15) + (0.93 * 0.10)
= 0.186 + 0.192 + 0.188 + 0.1395 + 0.141 + 0.093
= 0.9395
```

**Exact value: 0.9395. Stream threshold: 0.94. 0.9395 < 0.94. Verdict: REVISE.**

> **Rounding note:** If each product is rounded to 3 decimal places before summation (as the protocol itself documents for stored weighted_composite values), the sum is: 0.186 + 0.192 + 0.188 + 0.140 + 0.141 + 0.093 = 0.940. The S-014 rubric specifies a direct weighted sum without per-step rounding. The unrounded sum governs adv-scorer arithmetic: 0.9395 < 0.94. Anti-leniency rule: when favorable rounding is available but not specified by the rubric, do not apply it. REVISE is the required verdict.

---

## Fix Verification Checklist (Iter5 Targeted Fix)

| Fix | Applied? | Effective? | Evidence |
|-----|----------|------------|----------|
| Update `example-run.json` line 28: `"weighted_composite": 0.744` | YES | YES | `schemas/examples/example-run.json` line 28: `"weighted_composite": 0.744` -- confirmed correct |
| Update `example-run.json` metadata: composite_verification note corrected | YES | YES | Line 46: `"composite_verification": "0.82*0.20 + 0.78*0.20 + 0.75*0.20 + 0.71*0.15 + 0.68*0.15 + 0.65*0.10 = 0.164 + 0.156 + 0.150 + 0.107 + 0.102 + 0.065 = 0.744 (per-step rounding: each product rounded to 3dp before summation)"` -- confirmed correct |
| Verify 0.749 appears only in revision history | YES | YES | Grep across entire `baselines/` directory: `0.749` appears exactly once, at `protocol.md` line 1118 in the revision history footnote (correct location) |

**Fix assessment:** The iter5 fix is complete, targeted, and effective. The cross-file arithmetic contradiction that blocked Internal Consistency from rising above 0.95 is now fully resolved. The fix is minimal and correct -- no side effects detected.

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Rubric criteria:** 0.9+: All requirements addressed with depth. 0.7-0.89: Most requirements addressed, minor gaps.

**Evidence:**

The deliverable covers all 14 navigation sections, all 5 agent prompt files with G-Eval evaluation criteria, all 8 script interfaces with docstrings and argument signatures, sample run record in both inline (protocol.md JSON code block) and standalone (example-run.json) forms, and full lifecycle phases 0-6 including refresh protocol, cost estimation, error handling, validation checks, and outputs produced.

No completeness-impacting changes were made in iter5. The iter5 fix was limited to example-run.json arithmetic corrections.

**Gaps:**

The Group 3 scripts remain unimplemented (docstring stubs only: `def main() -> None: ...`). A practitioner cannot execute Phase 0 Step 0.4 (`validate_environment.py`) without implementing the script. For a protocol whose status is "READY FOR EXECUTION," this represents a completeness gap between documentation readiness and execution readiness. This gap has been present since iter1 and is unchanged.

**Why 0.93 is held (not raised, not lowered):**

No changes to completeness-relevant content occurred in iter5. The score does not drift. 0.93 reflects: strong structural coverage across all sections (supports the score being above 0.92) while the unimplemented scripts prevent reaching 0.95 (which would require Phase 0 to be at minimum minimally runnable).

**Improvement Path:**

Implement trivial stubs (`sys.exit(1)` with "Not yet implemented" message) for all 8 scripts. This closes the Phase 0 execution gap and would move this dimension to 0.95+.

---

### Internal Consistency (0.96/1.00)

**Rubric criteria:** 0.9+: No contradictions, all claims aligned. 0.7-0.89: Minor inconsistencies.

**Evidence for score increase (0.95 -> 0.96):**

The iter5 fix is confirmed complete and effective across three verification points:

1. **`example-run.json` line 28:** `"weighted_composite": 0.744` -- corrected from 0.749.
2. **`example-run.json` line 46 composite_verification:** `"... = 0.744 (per-step rounding: each product rounded to 3dp before summation)"` -- corrected from prior text that referenced 0.749.
3. **Grep verification:** `0.749` appears exactly once in the entire `baselines/` directory tree -- at `protocol.md` line 1118 in the revision history section, which is the correct and expected location for documenting what was changed.

The cross-file contradiction between `example-run.json` and `protocol.md` that blocked Internal Consistency at 0.95 is now fully resolved. The 10-file deliverable is internally consistent on the arithmetic claim:

- `protocol.md` schema table: `0.744` (set in iter4)
- `protocol.md` inline JSON code block: `0.744` (set in iter4)
- `protocol.md` rounding footnote: verified arithmetic chain for 0.744 (set in iter4)
- `example-run.json`: `0.744` (set in iter5)
- `example-run.json` composite_verification: correct per-step rounding explanation for 0.744 (set in iter5)

**Residual preventing 0.97:**

A pre-existing metadata inconsistency persists: the protocol.md frontmatter reads `> **Iteration:** 3 (revised per adv-scorer findings; iter2 score 0.924; targeted evidence quality and consistency fixes)` while the protocol footer reads `*Revision: Iteration 4 (targeted arithmetic and evidence fixes...)*`. These two iteration labels are inconsistent -- the frontmatter was not updated when the iteration count changed. This is a metadata-level inconsistency, not a substantive claim contradiction, but under the rubric criterion "all claims aligned," it is a real discrepancy in the document. It was present in iter4 (where it was masked by the more significant 0.749/0.744 contradiction) and remains present in iter5.

**Why 0.96 (not 0.95, not 0.97):**

0.95 is no longer appropriate: the major arithmetic contradiction is resolved. 0.97 is not appropriate: the Iteration 3/4 metadata mismatch is a real, specific inconsistency in the document. Anti-leniency rule: uncertain score between 0.96 and 0.97 resolves downward to 0.96. 0.96 reflects: strong and now complete arithmetic consistency across all files (justifies +0.01 over iter4's 0.95) while one metadata-level misalignment prevents reaching 0.97.

**Improvement Path:**

Update protocol.md frontmatter to read `> **Iteration:** 5 (revised per adv-scorer iter5 findings; iter4 score 0.9375)` or equivalent, aligning the iteration label with the footer revision note. This closes the final metadata inconsistency and would support a score of 0.97.

---

### Methodological Rigor (0.94/1.00)

**Rubric criteria:** 0.9+: Rigorous methodology, well-structured.

**Evidence:**

Unchanged from iter4. Three independent statistical arguments remain intact:
- Argument 1: CLT applicability (Hollander et al. [1], Montgomery & Runger [2]) -- N=30 minimum for normal approximation validity.
- Argument 2: Wilcoxon power analysis (Noether [3]) -- N=20-32 across plausible sigma range; Noether formula explicitly noted as conservative lower bound for Wilcoxon due to ARE of 3/pi ≈ 0.955.
- Argument 3: Wilson score interval precision (Wilson [4], Agresti & Coull [5]) -- 21% width reduction vs. N=20.

Dror et al. [6] provides NLP-specific rationale for non-parametric tests when score distribution normality is unknown. The ARE explanation (line 105) is mathematically correct. The Noether formula application and its conservative-bound status are both stated explicitly.

The iter5 fix made no changes to methodology sections.

**Residual gap:**

Monte Carlo power simulation for Wilcoxon at N=30, sigma=0.10 remains absent. The Noether formula provides N=31.4 at sigma=0.10, meaning N=30 gives approximately 78% power -- the protocol explicitly acknowledges this "slight shortfall." An empirical simulation would replace this conservative bound with an actual Wilcoxon power estimate and strengthen the statistical case for N=30.

**Why 0.94 is held:**

No changes in iter5. Score does not drift.

**Improvement Path:**

Add Monte Carlo simulation result: "10,000-iteration simulation at N=30, sigma=0.10 confirms X% Wilcoxon power." Would move this dimension to 0.97+.

---

### Evidence Quality (0.93/1.00)

**Rubric criteria:** 0.9+: All claims with credible citations. 0.7-0.89: Most claims supported.

**Evidence:**

Six complete citations [1]-[6] remain intact with stable URLs. The Dror et al. [6] ACL Anthology URL (https://aclanthology.org/P18-1128) is a persistent identifier. Citations [1]-[5] are standard textbooks and journal articles.

The [^proj017-path] footnote (line 1113) remains as set in iter4. It provides honest disclosure that the sigma data source path requires implementation-time discovery, identifies the two candidate PROJ-017 directories, and states that the operative calibration input (sigma range 0.08-0.12) is valid regardless of exact path.

The iter5 fix made no changes to evidence content.

**Residual gap:**

The sigma estimates (0.08-0.12) underpinning the N=30 statistical arguments cannot be independently verified without implementation-time path lookup. "All claims with credible citations" -- the sigma claim's citation remains a deferred disclosure rather than a resolvable reference. Cost estimate token rates are also unstated (e.g., the cost/run estimates in the Cost Estimation section cite "March 2026 reference" but do not state the per-token rates used to compute them).

**Why 0.93 is held:**

No changes in iter5. Score does not drift.

**Improvement Path:**

Inspect the repository for the PROJ-017 Phase 5 output files (check `projects/PROJ-017-llm-skill-testing/` and `projects/PROJ-017-portability/` for phase-5 evaluation score data). Replace the deferred footnote with a concrete file path. Add the per-token rates used in cost estimates. These two changes would support raising Evidence Quality to 0.94.

---

### Actionability (0.94/1.00)

**Rubric criteria:** 0.9+: Clear, specific, implementable actions.

**Evidence:**

Unchanged from iter4. The `--eval-mode skip` to `"not_evaluated"` mapping is documented at line 362. All 8 script interfaces include docstrings with argument lists, behavior descriptions, and return semantics. Phase 0-6 step-by-step commands are concrete, runnable bash commands (with `uv run` compliance per H-05). The G-Eval criteria strings are in directly usable format as DeepEval constructor arguments. The baseline refresh protocol includes git tagging commands and archival steps.

The iter5 fix made no changes to actionability content.

**Residual gap:**

The 8 scripts remain unimplemented (`def main() -> None: ...` stubs). A practitioner following the protocol reaches a hard stop at Phase 0 Step 0.4 (`uv run python .../validate_environment.py`). The `re_evaluate.py` script referenced in the evaluation failure error handling section is also unimplemented.

**Why 0.94 is held:**

No changes in iter5. Score does not drift.

**Improvement Path:**

Same as Completeness: implement trivial script stubs to close the Phase 0 execution gap.

---

### Traceability (0.93/1.00)

**Rubric criteria:** 0.9+: Full traceability chain. 0.7-0.89: Most items traceable.

**Evidence:**

The three iter2 traceability fixes remain intact:
- ADR-001 qualified as PROJ-035 ADR-001 throughout the document.
- `.context/rules/quality-enforcement.md` cited in Data Collection Schema as SSOT for dimension weights.
- Behavior IDs (B-001 through B-005) linked to `contracts/behavioral-contracts.md` Sections A, B, C in all 5 prompt YAML files (verified in ps-researcher-prompts.yaml header at lines 19-23).

The [^proj017-path] footnote documents the traceability gap explicitly: two candidate PROJ-017 directories, implementation-time resolution required.

The iter5 fix made no changes to traceability content.

**Residual gap:**

The sigma claim's trace chain from protocol assertion to verifiable source data remains broken: the footnote is honest about the gap but does not close it. The `contracts/behavioral-contracts.md` file existence and Section A/B/C structure cannot be confirmed from this scoring context (the file path is referenced in all 5 prompt YAMLs but its existence is not verified in this deliverable unit).

**Why 0.93 is held:**

No changes in iter5. Score does not drift.

**Improvement Path:**

Confirm `contracts/behavioral-contracts.md` exists with Sections A, B, C as referenced. Resolve the PROJ-017 Phase 5 path. Both changes together would support raising Traceability to 0.94.

---

## Anti-Leniency Assessment

### Calibration Check

The 0.94 stream threshold is higher than the standard H-13 threshold (0.92). The deliverable at 0.9395 (exact) passes H-13 but falls 0.0005 short of the 0.94 stream threshold.

### Dimension-by-Dimension Leniency Check

**Internal Consistency (raised from 0.95 to 0.96):**

The iter5 fix is complete and effective. The specific cross-file contradiction cited by iter4 (example-run.json retaining 0.749) is resolved. Raising IC from 0.95 to 0.96 is the correct response to a complete, targeted fix that addresses exactly the cited gap. The calibration anchor for 0.96 is: "minor inconsistency remains" -- the Iteration 3/4 metadata mismatch is that remaining minor inconsistency, which prevents 0.97. The +0.01 increase is supported by the specific evidence that the major contradiction is gone.

**Temptation to raise IC to 0.97 (counteracted):**

At 0.97, the composite would be 0.9415 (PASS). The rationale for 0.97 would be: "only a metadata label mismatch remains, which is trivial." Counterargument: the rubric says "all claims aligned." Frontmatter "Iteration: 3" and footer "Revision: Iteration 4" are directly contradictory claims about which iteration this document represents. This is a real inconsistency even if minor. Anti-leniency rule: uncertain scores resolve downward. 0.96, not 0.97.

**All other dimensions (held at iter4 values):**

Completeness (0.93), Methodological Rigor (0.94), Evidence Quality (0.93), Actionability (0.94), Traceability (0.93): no changes were applied in iter5 to any of these dimensions. Scores do not drift upward without cause. All held.

### Rounding Temptation Analysis

Three rounding approaches yield different apparent verdicts:

| Method | Composite | Verdict |
|--------|-----------|---------|
| Exact unrounded sum | 0.9395 | REVISE (0.9395 < 0.94) |
| Per-step 3dp rounding (protocol convention) | 0.940 | PASS (0.940 = 0.94) |
| Display rounding to 2dp | 0.94 | Appears to be PASS |

The S-014 rubric specifies `composite = sum(dimension * weight)`. No per-step rounding is specified. The governing arithmetic is the exact unrounded sum: **0.9395 < 0.94. REVISE.**

The per-step 3dp rounding convention is the protocol's own method for computing scores that will be stored in run records -- it is not the adv-scorer's arithmetic method. Using it to manufacture a PASS verdict would be a violation of P-022 (no deception) and the anti-leniency mandate.

### Specific Leniency Temptations Counteracted

1. **"IC at 0.97 clears the threshold."** IC at 0.97 yields composite 0.9415, which passes the 0.94 threshold. The temptation is to award 0.97 because the remaining metadata mismatch is "just a label." Held at 0.96: the label mismatch is a real, specific inconsistency in frontmatter vs. footer claims about iteration number. The rubric criterion ("all claims aligned") makes no exception for metadata-level inconsistencies.

2. **"Per-step rounding gives 0.940 = PASS."** Per-step 3dp rounding yields exactly 0.940. The temptation is to apply the protocol's own rounding convention to reach a PASS verdict. Counteracted: adv-scorer arithmetic uses the standard weighted sum formula without per-step rounding. The exact value 0.9395 is below threshold.

3. **"The deliverable is clearly high quality and deserves to pass."** At iteration 5, this deliverable is genuinely excellent for a C4 protocol -- six citations, three statistical arguments, full lifecycle coverage, complete schema suite. Temptation: inflate scores to reflect that overall quality impression. Counteracted: dimension scores are assigned independently based on specific rubric evidence, not holistic impressions.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.96 | 0.97 | Update `protocol.md` frontmatter `Iteration:` label from "3" to "5" (or current correct iteration), resolving the frontmatter vs. footer iteration number mismatch. Composite impact: +0.002 weighted. This single change brings composite to 0.9415, crossing the 0.94 stream threshold. |
| 2 | Evidence Quality | 0.93 | 0.94 | Inspect the PROJ-017 orchestration directories to find the Phase 5 evaluation score data and replace the deferred [^proj017-path] footnote with a concrete file path. Add per-token rates used in cost estimates. Composite impact: +0.0015 weighted. |
| 3 | Traceability | 0.93 | 0.94 | Confirm `contracts/behavioral-contracts.md` exists and contains Sections A, B, C as referenced in all 5 prompt YAML files. Resolve the PROJ-017 Phase 5 path (same as Priority 2). Composite impact: +0.001 weighted. |
| 4 | Methodological Rigor | 0.94 | 0.96 | Add Monte Carlo power simulation result for Wilcoxon at N=30, sigma=0.10, replacing the conservative Noether bound with an empirical estimate. Composite impact: +0.004 weighted. |
| 5 | Completeness / Actionability | 0.93 / 0.94 | 0.95+ | Implement trivial script stubs (sys.exit(1) with "Not yet implemented") for all 8 scripts to allow Phase 0 Step 0.4 to be minimally runnable. Composite impact: +0.003 weighted. |

**Minimum path to 0.94 stream threshold:**

Priority 1 alone (fix frontmatter Iteration label) raises Internal Consistency from 0.96 to 0.97:
- New composite: 0.186 + 0.194 + 0.188 + 0.1395 + 0.141 + 0.093 = **0.9415**
- 0.9415 >= 0.94: **PASS**

This is a single-line change in protocol.md. It is the minimum path to clearing the 0.94 stream threshold.

---

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (IC held at 0.96 not 0.97; all unchanged dimensions held, not drifted upward)
- [x] First-draft calibration not applicable (iteration 5; scored against rubric, not iteration-relative)
- [x] No dimension scored above 0.96 without exceptional evidence (IC at 0.96 is the highest; supported by complete arithmetic consistency across all 10 files minus one metadata label mismatch)
- [x] Composite threshold not rounded favorably (exact sum 0.9395 < 0.94; per-step rounding convention not applied to adv-scorer arithmetic; REVISE not PASS)
- [x] IC increase (0.95 -> 0.96) proportional to the fix scope (complete resolution of one specific, cited contradiction; not over-rewarded to force a PASS)

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.9395
threshold_stream: 0.94
threshold_h13: 0.92
weakest_dimension: completeness_evidence_quality_traceability
weakest_score: 0.93
critical_findings_count: 0
iteration: 5
improvement_recommendations:
  - "PRIORITY 1 (MINIMUM PATH TO PASS): Update protocol.md frontmatter Iteration label from '3' to '5' -- single-line change closes the frontmatter vs. footer iteration number contradiction; raises IC from 0.96 to 0.97; composite becomes 0.9415 (PASS)"
  - "PRIORITY 2: Resolve PROJ-017 Phase 5 sigma data path from deferred footnote to exact file path by inspecting PROJ-017-llm-skill-testing and PROJ-017-portability directories"
  - "PRIORITY 3: Confirm contracts/behavioral-contracts.md exists with Sections A, B, C as referenced in all 5 prompt YAML files"
  - "Add Monte Carlo power simulation result for Wilcoxon at N=30 to replace conservative Noether bound"
  - "Implement trivial script stubs for all 8 scripts to close Phase 0 execution gap"
minimum_iter6_path: "Fix frontmatter Iteration label (P1, single-line) raises IC 0.96->0.97, composite 0.9395->0.9415, verdict PASS"
delta_from_iter4: "+0.002 (IC raised 0.95->0.96 due to confirmed example-run.json fix)"
delta_from_threshold: "-0.0005 (exactly 0.0005 below 0.94 stream threshold)"
```

---

*Score Report Version: 1.0*
*Scoring Agent: adv-scorer*
*Strategy: S-014 (LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Produced: 2026-03-07*
*Stream: 1C -- Baseline Capture Protocol and Schemas*
*Iteration: 5 of N*
