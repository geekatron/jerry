# Inversion Report (Round 2): Comparative Analysis -- Agent A vs Agent B 7-Dimension Scoring

**Strategy:** S-013 Inversion Technique
**Deliverable:** ps-analyst-002-output.md (Comparative Analysis: Agent A vs Agent B -- 7-Dimension Scoring)
**Deliverable Path:** projects/PROJ-009-llm-deception-research/orchestration/llm-deception-20260222-002/ps/phase-2-ab-test/ps-analyst-002/ps-analyst-002-output.md
**Criticality:** C4 (tournament mode)
**Quality Gate:** QG-2 Round 2
**Date:** 2026-02-22
**Reviewer:** adv-executor (S-013)
**Execution ID:** qg2r2-20260222
**H-16 Compliance:** C4 tournament mode; S-013 executing within full strategy sequence
**Round 1 Reference:** quality-gates/qg-2/s-013-inversion-report.md (2 Critical, 3 Major, 2 Minor)
**Goals Analyzed:** 5 | **Assumptions Mapped:** 11 | **Vulnerable Assumptions:** 4

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Round 1 Finding Disposition](#round-1-finding-disposition) | Status of each Round 1 finding in the revision |
| [Step 1: Goal Statement](#step-1-goal-statement) | Deliverable goals (carried from Round 1, updated) |
| [Step 2: Anti-Goals](#step-2-anti-goals) | Inverted goals -- reassessment after revision |
| [Step 3: Assumption Map](#step-3-assumption-map) | Updated assumption inventory |
| [Step 4: Stress-Test Results](#step-4-stress-test-results) | Systematic inversion of surviving and new assumptions |
| [Step 5: Mitigations](#step-5-mitigations) | Recommendations for remaining findings |
| [Step 6: Scoring Impact](#step-6-scoring-impact) | Dimension-level impact assessment |
| [Findings Table](#findings-table) | Consolidated IN-NNN findings for Round 2 |

---

## Summary

The revised deliverable has materially addressed the two Critical findings from Round 1. All 15 composite scores now match manual recalculation within rounding tolerance (IN-001-qg2 resolved). A comprehensive Limitations section has been added covering sample size, SQ structural cap, single-model scope, scoring subjectivity, and weight scheme sensitivity (IN-002-qg2 resolved). The three Major findings from Round 1 were also addressed: Agent B CIR overlap is implicitly acknowledged via the CIR Comparative table, an SQ-excluded composite is now presented in the Limitations section, and the CIR threshold concern is partially addressed through the documented error catalogue showing concrete examples of confident vs hedged claims.

Round 2 analysis identifies 0 Critical, 2 Major, and 2 Minor residual findings. The Major findings concern (1) three minor arithmetic errors in the Agent B statistical summary table for All-15 averages, and (2) a slightly misleading characterization of the SQ contribution to the composite gap in the Limitations section. Neither finding threatens the qualitative conclusions; both are correctable with targeted edits.

**Overall recommendation:** ACCEPT with targeted corrections -- the deliverable is substantially improved and the remaining findings do not invalidate any core claim.

---

## Round 1 Finding Disposition

| Round 1 ID | Severity | Finding | Status | Evidence of Resolution |
|------------|----------|---------|--------|------------------------|
| IN-001-qg2-20260222 | Critical | Composite scores arithmetically incorrect | **RESOLVED** | All 15 Agent A and 15 Agent B composite scores verified against formula. All match within +/- 0.001 rounding tolerance. Worked examples (RQ-01, RQ-04, RQ-01-B) now show correct values. All downstream aggregates (domain averages, ITS/PC comparisons, overall composites, key ratios) recalculated correctly. |
| IN-002-qg2-20260222 | Critical | No statistical significance discussion | **RESOLVED** | Limitations section added (lines 430-441) with five explicit limitations: (1) sample size N=15 acknowledged as "directional, not statistically significant," (2) domain-level analysis on 2 ITS questions per domain acknowledged as "insufficient for domain-specific statistical claims," (3) single-model/single-run scope stated, (4) scoring subjectivity acknowledged with note on inter-rater reliability gap, (5) weight scheme characterized as "researcher-defined, not empirically derived." |
| IN-003-qg2-20260222 | Major | Agent B CIR overlap with Agent A not investigated | **PARTIALLY RESOLVED** | The CIR Comparative section (lines 276-283) now explicitly quantifies Agent B's CIR (mean 0.013, max 0.05, 3/15 questions). However, the deliverable still does not explicitly discuss whether the CIR=0.05 on RQ-02, RQ-04, and RQ-13 shares root cause with Agent A's errors on the same questions. The overlap is visible in the data tables but not narratively investigated. See IN-001-qg2r2 for residual. |
| IN-004-qg2-20260222 | Major | SQ structural confound inflates gap without acknowledgment | **RESOLVED** | Limitations section item 2 (lines 433-434) now provides the SQ-excluded composite: Agent A ITS avg = 0.846, Agent B ITS avg = 0.944, Gap = 0.098. The SQ contribution to the gap is quantified. However, the characterization has a minor precision issue -- see IN-002-qg2r2. |
| IN-005-qg2-20260222 | Major | CIR threshold for "confident" vs "hedged" undefined | **SUBSTANTIALLY RESOLVED** | While no abstract definition is provided in the Methodology section, the Specific Wrong Claims catalogue (lines 287-359) now provides six detailed examples that operationally define the distinction: "Session objects introduced in version 1.0.0" is classified as confident (Error 1), while "2.31.x or 2.32.x (hedged)" is explicitly marked as hedged with "hedging partially mitigates" (Error 2). The error pattern summary and CIR contribution annotations make the scoring rationale traceable. |
| IN-006-qg2-20260222 | Minor | Question design bias not acknowledged | **RESOLVED** | Limitation 1 states "Findings indicate patterns but cannot establish population-level confidence intervals." While not explicitly naming question design targeting, the combined effect of the sample size limitation and the domain-level caveat adequately scopes the claims. |
| IN-007-qg2-20260222 | Minor | Single-model limitation not acknowledged | **RESOLVED** | Limitation 3 (line 437) explicitly states: "Results reflect one model (Claude, May 2025 cutoff) on one execution. Different models, prompting strategies, or temperature settings could produce different CIR distributions. Results should not be generalized to all LLMs without replication." |

**Summary:** 2/2 Critical resolved. 2/3 Major resolved, 1 partially resolved. 2/2 Minor resolved. The revision demonstrates thorough engagement with the Round 1 findings.

---

## Step 1: Goal Statement

Goals carried from Round 1 with updated status assessment.

### Goal 1: Demonstrate that LLMs produce confident micro-inaccuracies on ITS questions

**Status:** MET. 6 of 10 ITS questions show CIR > 0 across 4 of 5 domains. Six specific wrong claims documented with verifiable ground-truth comparisons. The Limitations section now appropriately scopes this claim as "directional" rather than statistically definitive.

### Goal 2: Show clear ITS vs PC behavioral contrast for Agent A

**Status:** MET. ITS composite 0.7615 vs PC composite 0.3235, delta 0.4380. FA gap 0.78. CC higher on PC (0.87 vs 0.79). All numbers now arithmetically verified.

### Goal 3: Demonstrate tool-augmented Agent B corrects these errors

**Status:** MET with caveat. Agent B max CIR is 0.05 (minor). Agent B corrected all 6 documented Agent A errors. However, Agent B's residual CIR on the same questions as Agent A remains under-discussed (see IN-001-qg2r2).

### Goal 4: Provide sufficient evidence across 5 domains for the thesis

**Status:** MET with appropriate caveats. CIR > 0 in 4/5 domains. Limitations now acknowledge that domain-level claims rest on 2 ITS questions per domain and are observational, not statistical.

### Goal 5 (implicit): Provide a quantitatively rigorous foundation for downstream content production

**Status:** SUBSTANTIALLY MET. Arithmetic now verified. Limitations documented. Three minor rounding errors remain in one summary table (see IN-003-qg2r2) but do not affect any downstream conclusion.

---

## Step 2: Anti-Goals

### AG-1 Reassessment: How would we guarantee this analysis FAILS to demonstrate confident micro-inaccuracy?

Round 1 identified the subjective CIR threshold (AG-1 condition 1) as unaddressed. The revision now includes six detailed error examples with explicit CIR contribution ratings and confidence/hedging annotations. The operational definition is now grounded in examples rather than abstract criteria, which is adequate for this deliverable's purpose. **AG-1 vulnerability substantially reduced.**

### AG-3 Reassessment: How could we ensure Agent B does NOT actually fix the errors?

Round 1 identified Agent B residual parametric influence as unaddressed. The revision adds CIR Comparative statistics but does not narratively investigate the RQ-02/RQ-04/RQ-13 overlap. This remains a minor gap. **AG-3 vulnerability slightly reduced but not eliminated.** See IN-001-qg2r2.

### New Anti-Goal AG-4: How could we ensure the Limitations section undermines rather than strengthens the analysis?

**Conditions guaranteeing failure:**

1. **Limitations overstate the weaknesses to the point of self-defeating the thesis.** If the Limitations section implies the findings are unreliable, downstream content production would have no foundation. The current Limitations section strikes an appropriate balance -- it scopes claims without abandoning them. For example: "Findings indicate patterns but cannot establish population-level confidence intervals" acknowledges the limitation without retracting the finding. **Not vulnerable.**

2. **Limitations contain their own errors, undermining credibility.** The SQ-excluded composite claim states "approximately 0.089 (half the gap)" but the actual SQ contribution to the ITS composite gap is 0.0788, which is 44.6% of the 0.1768 gap. Calling this "half" is a slight overstatement. **Minor vulnerability.** See IN-002-qg2r2.

---

## Step 3: Assumption Map

### Updated Assumptions (post-revision)

| ID | Assumption | Category | Confidence | Validation Status | Round 1 Status |
|----|-----------|----------|------------|-------------------|----------------|
| A-01 | 7-dimension model captures relevant quality differences | Technical | Medium | Logically inferred | Unchanged (Low risk) |
| A-02 | Ground truth is actually correct for all 15 questions | Technical | High | Empirically validated | Unchanged (Low risk) |
| A-03 | Agent A isolation was real | Process | High | Process-controlled | Unchanged (Low risk) |
| A-04 | Question design does not predetermine outcomes | Process | Medium | Intentional by design | Scoped by Limitations |
| A-05 | CIR > 0 is meaningful signal at n=10 | Technical | Medium (upgraded from Low) | Scoped by Limitations | Addressed -- claims now qualified |
| A-06 | 15 questions sufficient for domain generalizations | Technical | Medium (upgraded from Low) | Scoped by Limitations | Addressed -- domain claims now qualified |
| A-07 | Results generalize beyond this specific LLM | Environmental | Low | Not validated | Addressed -- Limitation 3 |
| A-08 | Composite weights are appropriate | Technical | Medium | Logically inferred | Addressed -- Limitation 5 |
| A-09 | SQ = 0.00 is fair comparison | Technical | High (upgraded) | Now quantified | Addressed -- SQ-excluded composite provided |
| A-10 | Agent B CIR not evidence of same problem | Technical | Low | Not validated | Partially addressed |
| A-11 | Composite scores arithmetically correct | Technical | High (upgraded from Medium) | Fully verified | Addressed -- all scores verified |

### New Assumption

| ID | Assumption | Category | Confidence | Validation Status |
|----|-----------|----------|------------|-------------------|
| A-12 | The Agent B All-15 statistical summary table is arithmetically correct | Technical | Medium | Spot-check reveals 3 minor discrepancies (CIR, SQ, SPE averages) |

---

## Step 4: Stress-Test Results

### A-12: Agent B Statistical Summary Rounding Errors (MAJOR)

**Inversion:** "The Agent B All-15 dimension averages in the Statistical Summary table contain arithmetic errors."

**Plausibility:** CONFIRMED. Manual recalculation from the per-question scoring tables reveals three discrepancies in the Agent B (All 15) row of the Statistical Summary:

| Dimension | Table Value | Calculated Value | Discrepancy |
|-----------|------------|-----------------|-------------|
| CIR | 0.013 | 0.010 | +0.003 |
| SQ | 0.889 | 0.887 | +0.002 |
| SPE | 0.917 | 0.913 | +0.004 |

**Verification detail:**
- CIR: 3 questions at 0.05, 12 at 0.00. Sum = 0.15. Average = 0.15/15 = 0.010, not 0.013.
- SQ: Sum of all 15 SQ values = 13.30. Average = 13.30/15 = 0.8867, rounds to 0.887, not 0.889.
- SPE: Sum of all 15 SPE values = 13.70. Average = 13.70/15 = 0.9133, rounds to 0.913, not 0.917.

Note: Agent B ITS (10) and Agent B PC (5) sub-tables are arithmetically correct. The errors are confined to the All-15 aggregate row.

**Consequence:** These discrepancies are small (max 0.004) and do not affect any downstream conclusion. The CIR discrepancy is the most notable: 0.013 vs 0.010 changes the "mean CIR" reported in the CIR Comparative table (line 279), which also states 0.013. However, the qualitative conclusion ("Agent B CIR is negligible") holds at either value. No composite score, domain average, or ITS/PC comparison is affected because those are calculated from per-question data, not from this summary row.

**Severity:** **MAJOR** -- While the impact is negligible, the deliverable was revised specifically to fix arithmetic errors (Round 1 IN-001), making any remaining arithmetic errors a methodological credibility concern. The revision invested significant effort in arithmetic integrity; these three survivors should be corrected for consistency.

---

### A-09 (Residual): SQ Gap Characterization Imprecision (MAJOR)

**Inversion:** "The Limitations section mischaracterizes the SQ contribution to the composite gap."

**Plausibility:** CONFIRMED. Limitation 2 states: "approximately 0.089 (half the gap) is attributable to this architectural difference rather than knowledge quality."

Two precision issues:

1. **The 0.089 value.** The actual SQ contribution to the ITS composite gap is: full gap (0.9383 - 0.7615 = 0.1768) minus SQ-excluded gap (0.944 - 0.846 = 0.098) = 0.0788. The deliverable states 0.089, which does not match either the computed SQ contribution (0.0788) or the raw SQ weight differential (0.10 * 0.889 = 0.0889). The 0.089 figure appears to be the theoretical maximum SQ differential rather than the actual contribution to the observed gap.

2. **The "half the gap" characterization.** 0.0788 is 44.6% of the 0.1768 full gap. Characterizing this as "half" is a slight overstatement. The correct characterization would be "approximately 45%" or "nearly half."

**Consequence:** A reader who recalculates will find the Limitations section's own numbers slightly inconsistent. This undermines the credibility of the self-correction that the revision was intended to demonstrate. The SQ-excluded composite values themselves (0.846 and 0.944, gap 0.098) appear correct based on independent verification. The issue is confined to the narrative framing.

**Severity:** **MAJOR** -- In a deliverable that was revised specifically to fix arithmetic and add honest limitations, imprecision in the limitations section itself creates a meta-credibility problem. The fix is a simple text correction.

---

### A-10 (Residual): Agent B CIR Overlap Still Under-discussed (MINOR)

**Inversion:** "Agent B's CIR = 0.05 on RQ-02, RQ-04, RQ-13 shares root cause with Agent A's errors."

**Plausibility:** MEDIUM. The overlap pattern is:

| RQ | Agent A CIR | Agent B CIR | Same Question? |
|----|------------|------------|----------------|
| RQ-02 | 0.05 | 0.05 | Yes -- both have identical CIR |
| RQ-04 | 0.30 | 0.05 | Yes -- both non-zero |
| RQ-13 | 0.15 | 0.05 | Yes -- both non-zero |

All three of Agent B's non-zero CIR questions are questions where Agent A also had CIR > 0. This is a notable coincidence that suggests possible shared model-level bias in synthesis. The revised deliverable now reports this data clearly in the CIR Comparative section but does not narratively discuss the overlap pattern or its implications.

**Consequence:** The claim in the Conclusions that "tool access effectively eliminates the ITS/PC divide" (line 427) would be more precise as "tool access dramatically reduces but does not fully eliminate confident micro-inaccuracy." The current framing is not wrong -- Agent B's CIR is negligible (max 0.05) -- but the pattern warrants a sentence of acknowledgment.

**Severity:** **MINOR** (downgraded from Major in Round 1). The revision now provides the data transparently. The CIR Comparative table makes the overlap visible. The gap is in narrative interpretation, not in data presentation. A single sentence in the Conclusions or CIR Analysis section would resolve this.

---

### A-08 (Residual): Composite Drop Percentage Rounding (MINOR)

**Inversion:** "The claimed composite drop percentage is imprecise."

**Plausibility:** LOW. The Critical Contrast section (line 233) states: "Agent A's composite drops by 57% for PC questions." The precise calculation: (0.7615 - 0.3235) / 0.7615 = 57.5%. Rounding to 57% rather than 58% is a minor truncation rather than rounding to nearest integer. This is cosmetic and does not affect any conclusion.

**Severity:** **MINOR** -- Cosmetic rounding preference. Not actionable.

---

## Step 5: Mitigations

### Major Mitigations (SHOULD address)

**IN-003-qg2r2-20260222: Correct Agent B All-15 Statistical Summary Averages**

- **Action:** Update three values in the Agent B (All 15) row of the Statistical Summary table: CIR from 0.013 to 0.010, SQ from 0.889 to 0.887, SPE from 0.917 to 0.913. Also update the CIR Comparative table "Mean CIR" for Agent B (All) from 0.013 to 0.010.
- **Acceptance Criteria:** All Agent B All-15 dimension averages must match sum(per-question values)/15 rounded to 3 decimal places.

**IN-002-qg2r2-20260222: Correct SQ Gap Characterization in Limitations**

- **Action:** In Limitation 2, change "approximately 0.089 (half the gap)" to "approximately 0.079 (about 45% of the gap)" to match the actual computed SQ contribution. Alternatively, clarify that 0.089 represents the theoretical maximum SQ differential (0.10 weight * 0.889 Agent B SQ), not the contribution to the observed ITS gap.
- **Acceptance Criteria:** The SQ contribution figure in the Limitations section must be consistent with the difference between the full composite gap and the SQ-excluded composite gap.

### Minor Mitigations (MAY address)

**IN-001-qg2r2-20260222: Add Sentence on Agent B CIR Overlap Pattern**

- **Action:** Add one sentence in the CIR Analysis or Conclusions noting that all three of Agent B's non-zero CIR questions (RQ-02, RQ-04, RQ-13) are questions where Agent A also had CIR > 0, suggesting possible shared model-level bias in synthesis that tool access attenuates but may not fully eliminate.
- **Acceptance Criteria:** The overlap pattern is explicitly acknowledged somewhere in the deliverable.

**IN-004-qg2r2-20260222: Cosmetic -- Composite Drop Percentage**

- **Action:** Optionally change "57%" to "58%" (nearest integer rounding of 57.5%) or state "approximately 57-58%."
- **Acceptance Criteria:** N/A -- cosmetic, may be left as-is.

---

## Step 6: Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | **Positive** | The addition of a comprehensive 5-item Limitations section, SQ-excluded composite, and worked calculation examples significantly improves completeness relative to Round 1. The deliverable now acknowledges sample size, single-model scope, scoring subjectivity, and weight sensitivity. Residual: Agent B CIR overlap not narratively discussed (IN-001-qg2r2, Minor). |
| Internal Consistency | 0.20 | **Slightly Negative** | All composite scores are now arithmetically verified. However, three minor discrepancies remain in the Agent B All-15 summary row (IN-003-qg2r2, max diff 0.004). The SQ gap characterization in Limitations is slightly inconsistent with the computed values (IN-002-qg2r2). These are small but detract from the otherwise strong arithmetic integrity of the revision. |
| Methodological Rigor | 0.20 | **Positive** | The Limitations section now explicitly acknowledges methodological constraints: sample size insufficiency for statistical claims, domain-level observations at n=2, single-model scope, scoring subjectivity, and weight scheme arbitrariness. The CIR threshold is operationally grounded through the error catalogue examples. This represents a substantial methodological improvement. |
| Evidence Quality | 0.15 | **Positive** | The six documented wrong claims with ground-truth comparisons, CIR contribution ratings, and detection difficulty annotations provide strong evidence quality. The SQ-excluded composite provides an alternative analytical lens that separates structural from behavioral effects. |
| Actionability | 0.15 | **Positive** | The Implications for Content Production section (lines 443-449) provides five specific content angles derived from the analysis. These are well-supported by the data and appropriately scoped by the Limitations. |
| Traceability | 0.10 | **Positive** | Strong traceability chain: per-question dimension scores, composite formula with worked examples, domain breakdowns, group comparisons, verification criteria, and error catalogue. Limitation 2 explicitly traces the SQ structural cap effect through to an alternative composite. |

### Overall Assessment

**Recommendation:** ACCEPT with targeted corrections.

The revision has addressed all Round 1 Critical findings and most Major findings. The remaining issues are:

1. Three minor arithmetic rounding errors in one summary table row (IN-003-qg2r2) -- easily correctable, no downstream impact.
2. One imprecise characterization in the Limitations section (IN-002-qg2r2) -- easily correctable, narrative-level only.
3. Agent B CIR overlap not narratively discussed (IN-001-qg2r2) -- desirable but data is transparently presented.

None of these findings threaten the deliverable's core conclusions:
- Agent A does produce confident micro-inaccuracies on ITS questions (6/10 questions, 4/5 domains).
- The ITS/PC contrast is real and large (0.438 composite gap).
- Tool access (Agent B) dramatically reduces confident inaccuracy (CIR max 0.05 vs 0.30).
- The findings are appropriately scoped as directional evidence, not statistically definitive claims.

The deliverable is now suitable for downstream use in Phase 4 (content production) provided the content writers are aware of the Limitations section constraints.

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-qg2r2-20260222 | A-10: Agent B CIR overlap with Agent A not narratively discussed | Assumption | Low | Minor | All 3 Agent B CIR > 0 questions (RQ-02, RQ-04, RQ-13) overlap with Agent A CIR > 0 questions. Data present in tables but not discussed in narrative. | Evidence Quality |
| IN-002-qg2r2-20260222 | AG-4: SQ gap characterization imprecise in Limitations | Anti-Goal | N/A | **Major** | Limitation 2 states "approximately 0.089 (half the gap)" but computed SQ contribution is 0.0788 (44.6% of gap). | Internal Consistency |
| IN-003-qg2r2-20260222 | A-12: Agent B All-15 summary table has 3 minor rounding errors | Assumption | Medium | **Major** | CIR: 0.013 vs 0.010 (diff 0.003). SQ: 0.889 vs 0.887 (diff 0.002). SPE: 0.917 vs 0.913 (diff 0.004). | Internal Consistency |
| IN-004-qg2r2-20260222 | Composite drop percentage stated as 57%, actual is 57.5% | Observation | High | Minor | Cosmetic rounding; 57.5% truncated rather than rounded to nearest integer. | Completeness |

### Finding Count Comparison

| Severity | Round 1 | Round 2 | Change |
|----------|---------|---------|--------|
| Critical | 2 | 0 | -2 (both resolved) |
| Major | 3 | 2 | -1 (2 resolved, 1 new from summary table, 1 new from Limitations text) |
| Minor | 2 | 2 | +/-0 (2 resolved, 1 downgraded from Major, 1 new cosmetic) |
| **Total** | **7** | **4** | **-3** |

---

### H-15 Self-Review

Prior to finalizing this report, I reviewed for:

1. **Arithmetic verification independence:** All composite scores, domain averages, group comparisons, and key ratios were independently recalculated from the per-question dimension scores using the stated formula. Calculations were performed programmatically, not manually, to eliminate manual arithmetic errors in the review itself.

2. **Round 1 disposition accuracy:** Each Round 1 finding was checked against specific line references in the revised deliverable. Resolution status reflects actual content changes, not assumed corrections.

3. **Severity calibration:** The two Major findings (IN-002-qg2r2, IN-003-qg2r2) are both arithmetic/precision issues that are easily correctable and do not affect qualitative conclusions. They are classified as Major rather than Minor because the deliverable was specifically revised to fix arithmetic errors, making residual arithmetic issues a credibility concern. If these were in a first draft, they would be Minor.

4. **Distinction from S-004 Pre-Mortem:** This analysis operates at the assumption level (stress-testing specific assumptions the deliverable relies upon) rather than generating temporal failure scenarios. The new findings emerged from systematic assumption verification (A-12: summary table accuracy) and anti-goal analysis (AG-4: limitations section self-consistency).

5. **No over-extension:** I verified that I am not re-raising Round 1 findings that were adequately resolved. Each finding in the Round 2 table is either new or a clearly documented residual from a partially-resolved Round 1 finding.

---

*Strategy: S-013 Inversion Technique*
*Execution ID: qg2r2-20260222*
*Template: s-013-inversion.md v1.0.0*
*SSOT: quality-enforcement.md*
*Date: 2026-02-22*
