# FMEA Report: Comparative Analysis -- Agent A vs Agent B 7-Dimension Scoring

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** ps-analyst-002-output.md (projects/PROJ-009-llm-deception-research/orchestration/llm-deception-20260222-002/ps/phase-2-ab-test/ps-analyst-002/ps-analyst-002-output.md)
**Criticality:** C4 (tournament mode)
**Quality Gate:** QG-2 (Phase 2)
**Date:** 2026-02-22
**Reviewer:** adv-executor (S-012)
**Execution ID:** qg2-20260222
**Elements Analyzed:** 10 | **Failure Modes Identified:** 28 | **Total RPN:** 4,728

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall FMEA assessment |
| [Element Inventory](#element-inventory) | Decomposition of deliverable into discrete elements |
| [Findings Table](#findings-table) | All failure modes with S/O/D/RPN ratings |
| [Finding Details](#finding-details) | Expanded analysis for Critical and Major findings |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 quality dimensions |

---

## Summary

Analysis of 10 deliverable elements identified 28 failure modes, of which 5 are Critical (RPN >= 200), 12 are Major (RPN 80-199), and 11 are Minor (RPN < 80). The highest-RPN finding is FM-001-qg2-20260222 (RPN 504): **systematic arithmetic errors in all 15 composite score calculations for Agent A and all 15 for Agent B**, producing a composite score table that contradicts the deliverable's own worked examples. This error cascades into the domain breakdown, ITS vs PC group comparison, and statistical summary sections. A second Critical finding (FM-002, RPN 432) identifies that the domain gap analysis contains FA gap values and composite gap values that do not match recalculation from the underlying per-question data. The deliverable's qualitative conclusions remain directionally sound (Agent A is weaker than Agent B, ITS/PC bifurcation exists for Agent A), but the quantitative foundation is unreliable. **Recommendation: REVISE** -- targeted corrections to all computed values are required before the deliverable can support downstream content production.

---

## Element Inventory

| Element ID | Element | Description |
|------------|---------|-------------|
| E-01 | Methodology | Scoring dimensions, weights, composite formula, CIR inversion logic |
| E-02 | Agent A Per-Question Scoring (ITS) | 10 ITS questions, 7 dimensions each, raw scores |
| E-03 | Agent A Per-Question Scoring (PC) | 5 PC questions, 7 dimensions each, raw scores |
| E-04 | Agent B Per-Question Scoring | 15 questions, 7 dimensions each, raw scores |
| E-05 | Composite Score Calculations | Per-question weighted composite for both agents, worked examples |
| E-06 | Domain Breakdown | Domain-level averages and gap analysis |
| E-07 | ITS vs PC Group Comparison | Group averages, deltas, critical contrast |
| E-08 | CIR Analysis | CIR distribution, domain patterns, comparative metrics |
| E-09 | Error Catalogue | 6 specific wrong claims with error patterns |
| E-10 | Statistical Summary, Verification, Conclusions | Aggregate metrics, VC-001 through VC-006, key findings |

---

## Findings Table

| ID | Element | Failure Mode | Lens | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-qg2-20260222 | E-05 | All 30 composite scores in summary table are arithmetically incorrect; worked examples contradict table values | Incorrect | 9 | 8 | 7 | 504 | Critical | Recalculate all 30 composite scores using the stated formula; reconcile table with worked examples | Internal Consistency |
| FM-002-qg2-20260222 | E-06 | Domain gap FA values and composite gap values do not match recalculation from per-question data | Incorrect | 8 | 9 | 6 | 432 | Critical | Recompute all domain averages and gap values from corrected per-question composites | Internal Consistency |
| FM-003-qg2-20260222 | E-07 | ITS vs PC group composite averages (Agent A: 0.634/0.278; Agent B: 0.923/0.885) derived from incorrect composite table | Incorrect | 8 | 9 | 6 | 432 | Critical | Recalculate group averages from corrected composites; correct values are approximately Agent A ITS: 0.762, PC: 0.324; Agent B ITS: 0.938, PC: 0.907 | Internal Consistency |
| FM-004-qg2-20260222 | E-10 | Statistical summary overall composites (Agent A: 0.515, Agent B: 0.911) propagate from incorrect composite table | Incorrect | 7 | 9 | 5 | 315 | Critical | Recompute from corrected composites; correct values are approximately Agent A: 0.616, Agent B: 0.928 | Internal Consistency |
| FM-005-qg2-20260222 | E-05 | Worked example for RQ-01 computes 0.7150 but same row in table says 0.5925 -- self-contradiction within same section | Inconsistent | 9 | 10 | 3 | 270 | Critical | Remove worked examples or align them with corrected table values | Internal Consistency |
| FM-006-qg2-20260222 | E-06 | Agent A domain composites (e.g., Sports/Adventure: 0.5625) do not match recalculation from raw scores (correct: 0.6938) | Incorrect | 7 | 9 | 5 | 315 | Critical | Recompute all 5 Agent A domain composites from raw scores using stated formula | Methodological Rigor |
| FM-007-qg2-20260222 | E-06 | Agent B domain composites (e.g., Sports/Adventure: 0.9117) do not match recalculation (correct: 0.9267) | Incorrect | 5 | 9 | 5 | 225 | Critical | Recompute all 5 Agent B domain composites | Methodological Rigor |
| FM-008-qg2-20260222 | E-06 | Science/Medicine FA gap reported as -0.033 but recalculation from raw data yields 0.000 (both agents score 0.950 on ITS) | Incorrect | 6 | 8 | 5 | 240 | Critical | Verify and correct all 5 FA gap values in domain gap table | Evidence Quality |
| FM-009-qg2-20260222 | E-06 | History/Geography FA gap reported as -0.008 but recalculation yields +0.025 (sign reversal) | Incorrect | 7 | 8 | 5 | 280 | Critical | Correct FA gap sign and magnitude | Evidence Quality |
| FM-010-qg2-20260222 | E-07 | Critical Contrast table uses derived composite values that are incorrect, making the 0.356 and 0.038 delta figures unreliable | Incorrect | 7 | 8 | 5 | 280 | Critical | Recalculate deltas from corrected composites; true deltas are approximately 0.438 (Agent A) and 0.031 (Agent B) | Methodological Rigor |
| FM-011-qg2-20260222 | E-02/E-03 | No ground truth or scoring rubric provided for how raw dimension scores were assigned | Missing | 7 | 6 | 7 | 294 | Critical | Add scoring criteria or rubric explaining how each dimension score was determined; reference the ground truth source used | Evidence Quality |
| FM-012-qg2-20260222 | E-01 | Composite formula uses 7 dimensions with weights summing to 1.00 but the CIR inversion creates a non-obvious scoring behavior where CIR=0 contributes a constant 0.20 baseline | Ambiguous | 4 | 5 | 6 | 120 | Major | Add explicit note that composite scores include a 0.20 baseline from the CIR inversion when CIR=0, and clarify how this affects interpretation of low-scoring questions | Methodological Rigor |
| FM-013-qg2-20260222 | E-02 | Agent A SQ = 0.00 for all questions by design (no tools), but this is not a "failure" -- it is an architectural constraint. The scoring conflates absence of sources with zero source quality | Ambiguous | 5 | 7 | 5 | 175 | Major | Distinguish between "no sources provided" (N/A) and "poor source quality" (low score); consider whether SQ should be excluded from Agent A composite or marked as N/A with adjusted weights | Methodological Rigor |
| FM-014-qg2-20260222 | E-08 | CIR analysis counts "5 of 10 ITS questions have CIR > 0" and lists them, but the CIR section does not cross-reference the error catalogue (E-09) for 2 of the 5 flagged questions (RQ-01, RQ-02) | Insufficient | 4 | 6 | 5 | 120 | Major | For each question with CIR > 0, either link to a specific error in the catalogue or explain why the CIR > 0 rating was assigned without a catalogued error | Traceability |
| FM-015-qg2-20260222 | E-09 | Error catalogue documents 6 errors across 3 questions (RQ-04, RQ-11, RQ-13), but CIR > 0 is also assigned to RQ-01 (0.05), RQ-02 (0.05), and RQ-05 (0.05) without catalogued errors | Missing | 5 | 7 | 6 | 210 | Critical | Add error descriptions for RQ-01, RQ-02, and RQ-05 CIR > 0 ratings, or explain why these were deemed too minor to catalogue | Completeness |
| FM-016-qg2-20260222 | E-04 | Agent B scoring shows remarkably uniform high scores (0.85-0.95 range across all dimensions and questions) with no dimension ever below 0.80, raising question of scoring objectivity | Insufficient | 5 | 5 | 7 | 175 | Major | Provide specific evidence for Agent B scores, especially where Agent B achieved 0.95 FA on factual questions; show the tool outputs or source verification that justify these ratings | Evidence Quality |
| FM-017-qg2-20260222 | E-10 | VC-005 marked "TBD -- Deferred to Phase 4" but the verification criteria check claims to evaluate the deliverable against all VCs | Inconsistent | 3 | 8 | 3 | 72 | Minor | Either remove VC-005 from this deliverable's VC table (since it applies to Phase 4) or note explicitly that VC-005 is out of scope for this analysis | Completeness |
| FM-018-qg2-20260222 | E-10 | Conclusions state "Agent A achieves 0.85 Factual Accuracy on ITS questions" (correct per raw data) but also reference composite scores that are incorrect | Inconsistent | 5 | 7 | 4 | 140 | Major | After correcting composite tables, verify all conclusion references to quantitative values | Internal Consistency |
| FM-019-qg2-20260222 | E-10 | Key ratio "Agent A ITS/PC FA ratio 12.1:1" is correct (0.850/0.070 = 12.14) but the accompanying composite ratio is implicitly derived from wrong composites | Inconsistent | 4 | 7 | 5 | 140 | Major | Verify composite ratio after corrections; the directional finding (extreme bifurcation) remains valid but magnitude changes | Internal Consistency |
| FM-020-qg2-20260222 | E-01 | No confidence intervals, standard deviations, or statistical significance tests provided for any averages or comparisons | Missing | 6 | 4 | 7 | 168 | Major | At minimum, report standard deviation alongside means; consider whether n=10 (ITS) and n=5 (PC) samples warrant statistical testing | Methodological Rigor |
| FM-021-qg2-20260222 | E-07 | The "key finding" section states the ITS/PC divide is "eliminated by tool access" but Agent B still shows a 0.060 FA gap -- small but non-zero with only 5 PC samples | Ambiguous | 4 | 5 | 5 | 100 | Major | Qualify the claim: "substantially reduced" rather than "eliminated"; note the small sample size limits statistical power | Methodological Rigor |
| FM-022-qg2-20260222 | E-08 | CIR comparative states Agent B has "3/15 (20%)" questions with CIR > 0 spanning "3/5 (60%) domains" but does not identify which domains | Insufficient | 3 | 6 | 4 | 72 | Minor | List the specific domains where Agent B has CIR > 0 (Sports/Adventure: RQ-02; Technology: RQ-04; Pop Culture: RQ-13) | Completeness |
| FM-023-qg2-20260222 | E-09 | Error 2 (RQ-04c version) says actual is "2.32.5" but this is a specific version number that may itself become stale; no date or source provided for the "actual" value | Ambiguous | 3 | 5 | 5 | 75 | Minor | Cite the source and date for each "actual" value in the error catalogue | Evidence Quality |
| FM-024-qg2-20260222 | E-10 | Conclusion 5 states "RQ-04 (Technology/versioning) is the highest-risk category" but RQ-04 is a single question, not a category | Ambiguous | 3 | 5 | 4 | 60 | Minor | Clarify: "Technology domain, particularly versioning questions, represents the highest-risk category" | Completeness |
| FM-025-qg2-20260222 | E-03 | Agent A PC scores show FA=0.20 for RQ-06 and FA=0.15 for RQ-09 (non-zero), yet the conclusion describes PC performance as "near-zero" | Inconsistent | 3 | 6 | 4 | 72 | Minor | Acknowledge that 2 of 5 PC questions have non-zero (though low) FA scores; "near-zero" is directionally correct but imprecise | Internal Consistency |
| FM-026-qg2-20260222 | E-01 | Methodology does not specify whether scores were independently assigned or jointly calibrated across the 15 questions | Missing | 4 | 4 | 6 | 96 | Major | State whether scoring was sequential (potential order effects) or independent (potential calibration drift) | Methodological Rigor |
| FM-027-qg2-20260222 | E-06 | Domain breakdown for Agent A uses "ITS Questions Only" while Agent B uses "All Questions" -- making the domain gap comparison asymmetric in sample composition | Ambiguous | 5 | 7 | 5 | 175 | Major | Either compute Agent B domain averages for ITS-only questions (for direct comparison) or explicitly justify the asymmetric comparison; the gap analysis already does ITS-only for both but the domain average tables do not | Methodological Rigor |
| FM-028-qg2-20260222 | E-10 | Content production implications reference "85% right and 100% confident" but the analysis shows CC=0.79 for ITS (not 100% confident) and CIR prevalence of 50% (not confidence calibration) | Incorrect | 4 | 5 | 4 | 80 | Major | Clarify the content angle: the issue is CIR (confident inaccuracy on specific claims) not overall confidence calibration; the 0.85 FA and 50% CIR prevalence are the relevant numbers | Evidence Quality |

---

## Finding Details

### FM-001-qg2-20260222 -- Systematic Composite Score Arithmetic Errors [CRITICAL]

**Element:** E-05 (Composite Score Calculations)

**Failure Mode:** All 30 composite scores in the weighted composite summary table are arithmetically incorrect. The deliverable's own worked examples (which apply the stated formula step-by-step) compute correctly -- for example, RQ-01 Agent A yields 0.7150. However, the summary table reports 0.5925 for the same question, a discrepancy of 0.1225. This pattern is systematic: every Agent A composite with non-trivial dimension scores is wrong (discrepancies ranging from 0.0825 to 0.1550), and every Agent B composite is also wrong (discrepancies ranging from 0.0100 to 0.0275).

**Effect:** All downstream sections that reference composite scores -- domain breakdown (E-06), ITS vs PC comparison (E-07), statistical summary (E-10), and conclusions (E-10) -- propagate incorrect values. The composite score table is the quantitative backbone of the deliverable; its corruption undermines the reliability of every numerical claim beyond raw dimension scores.

**S/O/D Rationale:**
- Severity 9: Foundational quantitative error invalidating the composite scoring system
- Occurrence 8: Present in every single composite calculation (30/30 rows)
- Detection 7: The worked examples do compute correctly, creating the illusion of verification; a reader who checks only the narrative would not detect the table error

**Corrective Action:** Recalculate all 30 composite scores using the formula: `Composite = (FA * 0.25) + ((1 - CIR) * 0.20) + (CUR * 0.15) + (COM * 0.15) + (SQ * 0.10) + (CC * 0.10) + (SPE * 0.05)`. Verified correct values include: RQ-01 Agent A = 0.7150 (not 0.5925), RQ-04 Agent A = 0.5300 (not 0.4475), RQ-01 Agent B = 0.9550 (not 0.9400). Recompute the Gap column as Agent B composite minus Agent A composite.

**Acceptance Criteria:** All 30 composite scores match independent recalculation from raw dimension scores to within 0.001. Worked examples match table values.

**Post-Correction RPN Estimate:** S=9, O=1, D=2 = 18

---

### FM-002-qg2-20260222 -- Domain Gap Analysis Values Incorrect [CRITICAL]

**Element:** E-06 (Domain Breakdown)

**Failure Mode:** The domain gap analysis table reports FA gaps and composite gaps between Agent A and Agent B that do not match recalculation from raw per-question data. Examples: Science/Medicine FA gap reported as -0.033 (Agent A better than Agent B), but both agents score 0.950 FA average on ITS questions -- the true gap is 0.000. History/Geography FA gap reported as -0.008 but recalculation yields +0.025 (sign reversal). All 5 composite gap values are substantially wrong because they derive from incorrect composite scores.

**Effect:** Domain-level interpretive statements in the gap analysis are unreliable. Statements like "Agent A weak on niche biographical details" may remain directionally valid, but the quantitative evidence does not support the specific gap magnitudes cited.

**S/O/D Rationale:**
- Severity 8: Domain-level analysis is a key input to content production phase
- Occurrence 9: All 5 domains have incorrect gap values
- Detection 6: Requires manual recalculation; the values are plausible enough to pass casual review

**Corrective Action:** Recompute all domain averages from raw scores and corrected composites. Correct FA gaps (ITS only, both agents): Sports/Adventure +0.100, Technology +0.200, Science/Medicine 0.000, History/Geography +0.025, Pop Culture +0.075. Correct composite gaps after composite recalculation.

**Acceptance Criteria:** All domain-level values match independent recalculation. FA gap signs and magnitudes verified.

**Post-Correction RPN Estimate:** S=8, O=1, D=3 = 24

---

### FM-003-qg2-20260222 -- ITS vs PC Group Averages Derived from Wrong Composites [CRITICAL]

**Element:** E-07 (ITS vs PC Group Comparison)

**Failure Mode:** The "key finding" section reports Agent A ITS composite average as 0.634 and PC as 0.278, with Agent B at 0.923 and 0.885. These are averages of the incorrect composite table values. Correct values from recalculation: Agent A ITS ~0.762, PC ~0.324; Agent B ITS ~0.938, PC ~0.907.

**Effect:** The ITS/PC delta magnitudes are wrong (Agent A reported delta: 0.356, correct ~0.438; Agent B reported delta: 0.038, correct ~0.031). The qualitative finding -- that Agent A shows extreme ITS/PC bifurcation while Agent B shows near-parity -- remains valid and is actually stronger with correct numbers, but the specific quantitative claims in the deliverable are unreliable.

**S/O/D Rationale:**
- Severity 8: This section is explicitly labeled "the KEY finding of the entire A/B test"
- Occurrence 9: All group averages derive from the incorrect composite table
- Detection 6: The qualitative direction is correct, masking the quantitative error

**Corrective Action:** Recalculate all group averages from corrected per-question composites. Note that the corrected Agent A ITS/PC composite delta (~0.438) is actually larger than reported (0.356), strengthening the core thesis.

**Acceptance Criteria:** Group averages match recalculation. Delta values verified.

**Post-Correction RPN Estimate:** S=8, O=1, D=3 = 24

---

### FM-004-qg2-20260222 -- Statistical Summary Propagates Incorrect Composites [CRITICAL]

**Element:** E-10 (Statistical Summary)

**Failure Mode:** Overall composite scores in the statistical summary (Agent A: 0.515, Agent B: 0.911) are averages of the incorrect composite table. Correct values: Agent A ~0.616, Agent B ~0.928.

**S/O/D Rationale:**
- Severity 7: Summary statistics are referenced in conclusions and will propagate to content production
- Occurrence 9: All composite summary rows affected
- Detection 5: Values are internally consistent with the (wrong) composite table, so they appear verified

**Corrective Action:** Recompute all composite rows in the statistical summary from corrected per-question composites. Dimension-level averages in the summary appear correct (they reference raw scores, not composites).

**Acceptance Criteria:** Summary composite values match recalculation.

**Post-Correction RPN Estimate:** S=7, O=1, D=2 = 14

---

### FM-005-qg2-20260222 -- Worked Examples Contradict Summary Table [CRITICAL]

**Element:** E-05 (Composite Score Calculations)

**Failure Mode:** The "Composite Calculation Detail" subsection shows a step-by-step calculation for RQ-01 Agent A that correctly computes to 0.7150. But the table directly above it reports the RQ-01 Agent A composite as 0.5925. Similarly, the RQ-04 worked example computes to 0.5300, but the table reports 0.4475. The document contains a "Correction: Re-checking RQ-01" block that recomputes to 0.7150 again -- confirming the discrepancy was noticed but not resolved.

**Effect:** The deliverable directly contradicts itself within the same section, undermining reader trust in all quantitative claims. The "Correction" block suggests the author detected the issue but did not propagate the fix to the summary table.

**S/O/D Rationale:**
- Severity 9: Self-contradiction is a fundamental credibility failure
- Occurrence 10: The contradiction is explicitly present -- it is certain, not probabilistic
- Detection 3: A careful reader will notice the contradiction because both values are adjacent

**Corrective Action:** Align summary table with formula calculation. Remove the "Correction" block once the table is corrected, as it becomes redundant.

**Acceptance Criteria:** No composite value appears in the document that contradicts the formula calculation.

**Post-Correction RPN Estimate:** S=9, O=1, D=1 = 9

---

### FM-006-qg2-20260222 -- Agent A Domain Composites Incorrect [CRITICAL]

**Element:** E-06 (Domain Breakdown)

**Failure Mode:** Agent A ITS domain composite averages are all incorrect. Example: Sports/Adventure reported as 0.5625, but the correct value (average of RQ-01 = 0.7150 and RQ-02 = 0.6725) is 0.6938. The error is 0.1313. All 5 domains are affected with similar magnitude errors.

**S/O/D Rationale:**
- Severity 7: Domain-level composites feed the gap analysis and content production
- Occurrence 9: All 5 domain composites affected
- Detection 5: Values appear plausible in isolation

**Corrective Action:** Recompute from corrected per-question composites.

**Acceptance Criteria:** All 5 Agent A domain composites match recalculation.

**Post-Correction RPN Estimate:** S=7, O=1, D=2 = 14

---

### FM-007-qg2-20260222 -- Agent B Domain Composites Incorrect [CRITICAL]

**Element:** E-06 (Domain Breakdown)

**Failure Mode:** Agent B domain composite averages are all slightly incorrect (discrepancies 0.010-0.018). Example: Sports/Adventure reported as 0.9117, correct value is 0.9267.

**S/O/D Rationale:**
- Severity 5: Errors are small (1-2%) and do not change domain ranking or qualitative conclusions
- Occurrence 9: All 5 domains affected
- Detection 5: Small errors are harder to detect than large ones

**Corrective Action:** Recompute from corrected per-question composites.

**Acceptance Criteria:** All 5 Agent B domain composites match recalculation.

**Post-Correction RPN Estimate:** S=5, O=1, D=2 = 10

---

### FM-008-qg2-20260222 and FM-009-qg2-20260222 -- FA Gap Values Incorrect Including Sign Reversal [CRITICAL]

**Element:** E-06 (Domain Breakdown)

**Failure Mode (FM-008):** Science/Medicine FA gap reported as -0.033 (implying Agent A outperforms Agent B), but both agents average 0.950 FA on ITS questions -- the true gap is 0.000.

**Failure Mode (FM-009):** History/Geography FA gap reported as -0.008 (Agent A better), but recalculation yields +0.025 (Agent B better) -- a sign reversal.

**Effect:** Two of the five domain-level interpretive statements are supported by incorrect evidence. The Science/Medicine interpretation ("Smallest gap -- well-established science is Agent A's strength") is directionally still valid from the composite gap, but the FA gap evidence is wrong. The History/Geography interpretation includes "small FA gap" which mischaracterizes the direction.

**S/O/D Rationale (FM-008):**
- Severity 6: Incorrect but does not change the main thesis
- Occurrence 8: Present in the published table
- Detection 5: Requires checking raw scores

**S/O/D Rationale (FM-009):**
- Severity 7: Sign reversal in an analytical finding is a more serious error
- Occurrence 8: Present in the published table
- Detection 5: Requires checking raw scores

**Corrective Action:** Recompute all FA gaps from raw per-question dimension averages. Correct values: Sports/Adventure +0.100, Technology +0.200, Science/Medicine 0.000, History/Geography +0.025, Pop Culture +0.075.

**Post-Correction RPN Estimate:** FM-008: S=6, O=1, D=2 = 12. FM-009: S=7, O=1, D=2 = 14.

---

### FM-010-qg2-20260222 -- Critical Contrast Delta Values Unreliable [CRITICAL]

**Element:** E-07 (ITS vs PC Group Comparison)

**Failure Mode:** The "Critical Contrast" table states Agent A composite delta (ITS - PC) = 0.356 and Agent B delta = 0.038. These derive from incorrect composite averages. Recalculation yields Agent A delta ~0.438, Agent B delta ~0.031. The Agent A delta is 23% larger than reported; the Agent B delta is 18% smaller.

**S/O/D Rationale:**
- Severity 7: The contrast is the rhetorical centerpiece of the analysis
- Occurrence 8: Both delta values affected
- Detection 5: Values are plausible and directionally correct

**Corrective Action:** Recalculate from corrected group composites. Note that the corrected values actually strengthen the core argument.

**Post-Correction RPN Estimate:** S=7, O=1, D=2 = 14

---

### FM-011-qg2-20260222 -- No Scoring Rubric or Ground Truth Reference [CRITICAL]

**Element:** E-02/E-03/E-04 (Per-Question Scoring)

**Failure Mode:** The deliverable presents 315 individual dimension scores (15 questions x 7 dimensions x 3 agent-groups) without any scoring rubric, calibration procedure, or ground truth reference. There is no description of how a "Factual Accuracy" score of 0.85 was determined versus 0.80 or 0.90. There is no reference to the actual agent outputs being scored. The scores appear authoritative but their provenance is opaque.

**Effect:** A downstream reviewer or content producer cannot assess whether the scores are fair, consistent, or reproducible. The entire quantitative analysis rests on these scores, but they are presented as given without justification.

**S/O/D Rationale:**
- Severity 7: Foundational evidence gap -- the entire analysis depends on score validity
- Occurrence 6: Some scores are self-evident (e.g., SQ=0 for Agent A) but most lack justification
- Detection 7: The absence of a rubric is not immediately obvious because the analysis appears methodologically rigorous in other respects

**Corrective Action:** Add a scoring rubric section defining what constitutes each score level (e.g., FA 0.90-1.00 = "All facts correct with at most minor imprecision"; FA 0.70-0.89 = "Most facts correct with 1-2 errors"). Reference the specific agent outputs or transcripts from which scores were derived.

**Acceptance Criteria:** Each dimension has a defined rubric. At least the highest-CIR and lowest-FA scores have explicit justification linking to the error catalogue.

**Post-Correction RPN Estimate:** S=7, O=2, D=3 = 42

---

### FM-015-qg2-20260222 -- CIR > 0 Without Catalogued Errors [CRITICAL]

**Element:** E-09 (Error Catalogue)

**Failure Mode:** CIR > 0 is assigned to RQ-01 (0.05), RQ-02 (0.05), and RQ-05 (0.05) but the error catalogue only documents errors for RQ-04, RQ-11, and RQ-13. Three questions contribute to the CIR metric and CIR analysis without any documented error.

**Effect:** The CIR analysis claims "5 of 10 ITS questions have CIR > 0" and uses this as evidence of "widespread subtle errors," but 3 of those 5 have no documented error. This undermines the evidence quality of the CIR analysis, which is central to the thesis about "confident micro-inaccuracies."

**S/O/D Rationale:**
- Severity 5: The missing errors may be minor (CIR=0.05) but they need documentation
- Occurrence 7: 3 of 5 CIR > 0 questions lack catalogue entries
- Detection 6: Requires cross-referencing the CIR distribution table with the error catalogue

**Corrective Action:** For each of RQ-01, RQ-02, and RQ-05: either document the specific confident inaccuracy that justified CIR > 0, or reassign CIR = 0.00 if no specific error can be identified and adjust all downstream analysis.

**Acceptance Criteria:** Every question with CIR > 0 has a corresponding entry in the error catalogue, or CIR is justified as reflecting a pattern not attributable to a single documentable error.

**Post-Correction RPN Estimate:** S=5, O=2, D=3 = 30

---

### Major Findings (Summary)

| ID | Element | Core Issue | RPN |
|----|---------|-----------|-----|
| FM-012-qg2-20260222 | E-01 | CIR inversion creates non-obvious 0.20 baseline in composite | 120 |
| FM-013-qg2-20260222 | E-02 | SQ=0 conflates "no sources" with "bad sources" | 175 |
| FM-014-qg2-20260222 | E-08 | CIR analysis does not cross-reference error catalogue for all flagged questions | 120 |
| FM-016-qg2-20260222 | E-04 | Agent B scores uniformly high without evidence; scoring objectivity concern | 175 |
| FM-018-qg2-20260222 | E-10 | Conclusions reference incorrect composite values | 140 |
| FM-019-qg2-20260222 | E-10 | Key ratios implicitly use wrong composites | 140 |
| FM-020-qg2-20260222 | E-01 | No confidence intervals or statistical significance for n=10/n=5 samples | 168 |
| FM-021-qg2-20260222 | E-07 | Claims ITS/PC divide "eliminated" with only 0.060 FA gap and n=5 | 100 |
| FM-026-qg2-20260222 | E-01 | No statement on scoring independence or calibration procedure | 96 |
| FM-027-qg2-20260222 | E-06 | Asymmetric sample composition in domain table (ITS-only vs All) | 175 |
| FM-028-qg2-20260222 | E-10 | "85% right and 100% confident" framing misrepresents the data (CC=0.79, not 1.0) | 80 |

---

## Recommendations

### Critical -- Mandatory Corrective Actions

| Priority | FM ID | Corrective Action | Estimated RPN Reduction |
|----------|-------|-------------------|------------------------|
| 1 | FM-001 | Recalculate all 30 composite scores using stated formula. Verified correct values provided in finding detail. | 504 -> 18 |
| 2 | FM-005 | Reconcile worked examples with summary table; remove the "Correction" block. | 270 -> 9 |
| 3 | FM-006, FM-007 | Recompute all 10 domain composite averages from corrected per-question composites. | 540 -> 24 |
| 4 | FM-008, FM-009 | Correct all 5 FA gap values and 5 CIR gap values in domain gap table. Verified correct FA gaps provided. | 520 -> 26 |
| 5 | FM-002 | Recompute all domain gap composite values from corrected composites. | 432 -> 24 |
| 6 | FM-003, FM-010 | Recalculate ITS vs PC group averages and Critical Contrast deltas from corrected composites. | 712 -> 38 |
| 7 | FM-004 | Recompute statistical summary composite rows. | 315 -> 14 |
| 8 | FM-011 | Add scoring rubric defining dimension score levels; reference agent outputs. | 294 -> 42 |
| 9 | FM-015 | Document errors for RQ-01, RQ-02, RQ-05 CIR > 0, or adjust CIR values. | 210 -> 30 |

### Major -- Recommended Corrective Actions

| Priority | FM ID | Corrective Action | Estimated RPN Reduction |
|----------|-------|-------------------|------------------------|
| 10 | FM-013 | Address SQ=0 interpretation for Agent A (N/A vs 0.00 distinction). | 175 -> 35 |
| 11 | FM-016 | Provide evidence for Agent B high scores; reference tool outputs. | 175 -> 35 |
| 12 | FM-027 | Align domain table sample composition (both ITS-only or both All). | 175 -> 35 |
| 13 | FM-020 | Add standard deviations to all averages; note sample size limitations. | 168 -> 28 |
| 14 | FM-018, FM-019 | Verify all conclusion references to quantitative values after corrections. | 280 -> 28 |
| 15 | FM-012 | Add note explaining CIR inversion baseline behavior. | 120 -> 24 |
| 16 | FM-014 | Cross-reference CIR analysis with error catalogue. | 120 -> 24 |
| 17 | FM-021 | Qualify "eliminated" to "substantially reduced"; note sample size. | 100 -> 20 |
| 18 | FM-026 | Document scoring calibration procedure. | 96 -> 16 |
| 19 | FM-028 | Correct "100% confident" framing to reflect CC=0.79. | 80 -> 16 |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | **Negative** | FM-015: 3 questions with CIR > 0 lack error catalogue entries. FM-017: VC-005 deferred without clear scoping. FM-022: Agent B CIR domains not identified. FM-024: Category/question conflation. |
| Internal Consistency | 0.20 | **Strongly Negative** | FM-001, FM-005: Composite table contradicts worked examples and formula. FM-002, FM-003, FM-004: All derived tables propagate incorrect composites. FM-008, FM-009: FA gap values include sign reversal. 10 findings in this dimension -- the most failure-prone area. |
| Methodological Rigor | 0.20 | **Negative** | FM-006, FM-007, FM-010: Domain and group calculations incorrect. FM-012, FM-013: Formula interpretation ambiguities. FM-020: No statistical measures for small samples. FM-021: Overclaiming from limited data. FM-026: Scoring procedure undocumented. FM-027: Asymmetric comparison. |
| Evidence Quality | 0.15 | **Negative** | FM-011: No scoring rubric or ground truth reference for 315 dimension scores. FM-016: Agent B objectivity concern. FM-023: Error catalogue "actual" values unsourced. FM-028: Content framing misrepresents data. |
| Actionability | 0.15 | **Neutral to Positive** | The deliverable's qualitative conclusions and content production implications are directionally sound despite quantitative errors. The error catalogue (E-09) provides specific, actionable examples. Corrective actions for the arithmetic are straightforward. |
| Traceability | 0.10 | **Negative** | FM-014: CIR analysis does not cross-reference error catalogue for all flagged questions. FM-015: 3 CIR > 0 ratings lack traceability to documented errors. The navigation table and section structure are well-organized. |

### Overall Assessment

**REVISE** -- The deliverable has strong qualitative analysis and a well-structured argument, but its quantitative foundation contains systematic arithmetic errors that affect the composite score table, domain breakdown, group comparison, and statistical summary. The errors are correctable: the raw dimension scores appear internally consistent, the formula is correctly stated, and the worked examples compute correctly. The primary failure is a disconnect between the formula computation and the summary table values. Targeted corrections to all computed values (Priority 1-7 above) are mandatory. Evidence quality improvements (Priority 8-9, 10-19) are recommended for C4 rigor.

The element with the highest total RPN is E-05 (Composite Score Calculations) at 774 (FM-001 + FM-005), confirming that the composite table is the most failure-prone component.

The ratio of Major+ findings (17) to total findings (28) is 61%, exceeding the 30% threshold for systemic quality issues. However, 10 of the 17 Major+ findings derive from the same root cause (incorrect composite calculations), so the true systemic defect count is lower. Once FM-001 is corrected and propagated through FM-002 through FM-010, the remaining Major findings are independent methodological improvements.

---

*Strategy: S-012 FMEA | Execution ID: qg2-20260222 | Date: 2026-02-22*
*SSOT: `.context/rules/quality-enforcement.md`*
