---
title: "S-014 LLM-as-Judge Report: QG-2 Phase 2 A/B Test"
strategy: S-014
execution_id: qg2-20260222
agent: adv-scorer
pipeline: adversary
workflow: llm-deception-20260222-002
deliverable: ps-analyst-002-output.md
criticality: C4
quality_gate: QG-2
date: 2026-02-22
result: REJECTED
weighted_composite_score: 0.571
---

# S-014 LLM-as-Judge Report: QG-2 Phase 2 A/B Test

**Strategy:** S-014 LLM-as-Judge
**Deliverable:** ps-analyst-002-output.md
**Criticality:** C4
**Quality Gate:** QG-2
**Date:** 2026-02-22
**Scorer:** adv-scorer (S-014)
**Tournament Strategies Reviewed:** 9 (S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Dimension Scores](#dimension-scores) | Per-dimension scoring with rationale |
| [Weighted Composite Score](#weighted-composite-score) | Final verdict |
| [Critical Findings Summary](#critical-findings-summary) | Findings with the greatest score impact |
| [Revision Guidance](#revision-guidance) | What MUST be fixed for PASS |
| [Tournament Finding Aggregation](#tournament-finding-aggregation) | All findings across 9 strategies by severity |
| [Scoring Methodology Notes](#scoring-methodology-notes) | Anti-leniency calibration |

---

## Summary

The deliverable presents a structurally well-organized comparative analysis with a compelling qualitative thesis -- that LLM internal knowledge produces subtle confident micro-inaccuracies more dangerous than outright hallucination. The error catalogue documenting 6 specific wrong claims is well-constructed, and the ITS/PC bifurcation insight is directionally sound. However, the deliverable suffers from a catastrophic quantitative integrity failure: 27 of 30 composite scores are arithmetically incorrect, the deliverable's own worked examples prove the summary table wrong without the contradiction being resolved, and every downstream aggregate metric (domain averages, group comparisons, overall composites, gap analyses) propagates these errors. A deliverable whose central purpose is quantitative comparative analysis cannot score well when its numbers are wrong. Additionally, the analysis lacks statistical significance testing, weight justification, inter-rater reliability, and a limitations section -- all standard methodological expectations for a C4 research deliverable. The verdict is REJECTED.

---

## Dimension Scores

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Completeness | 0.20 | 0.68 | The deliverable covers all required sections: methodology, per-question scoring, composites, domain breakdown, ITS/PC comparison, CIR analysis, error catalogue, verification criteria, and conclusions. However, it is missing several elements expected of a C4 research analysis: (1) no Limitations section acknowledging sample size (N=15, N=10 ITS, N=5 PC), single-evaluator design, or single-model scope (found by S-002 DA-001, S-004 PM-003/PM-006/PM-007, S-013 IN-002/IN-007); (2) no scoring rubric or ground truth reference explaining how the 315 individual dimension scores were assigned (S-012 FM-011); (3) CIR > 0 is assigned to RQ-01, RQ-02, and RQ-05 without corresponding entries in the error catalogue -- 3 of 6 CIR-contributing questions lack documented errors (S-012 FM-015); (4) the CIR count itself is wrong: the data shows 6/10 ITS questions with CIR > 0 but the text claims 5/10 (S-011 CV-005); (5) no sensitivity analysis for the weight scheme (S-002 DA-003, S-001 RT-008); (6) Agent B CIR domains not identified (S-012 FM-022). The completeness score reflects adequate structural coverage undermined by material omissions in methodology, evidence documentation, and limitations. |
| Internal Consistency | 0.20 | 0.20 | This is the most severely impacted dimension. All 9 strategies identified the same root defect: the composite score summary table contradicts the deliverable's own formula and worked examples. The deliverable computes RQ-01 Agent A as 0.7150 in the worked example section, then reports 0.5925 in the summary table 25 lines away, and includes a "Correction: Re-checking RQ-01" note that again yields 0.7150 without updating the table. The "minor rounding differences at the fourth decimal place" disclaimer is false -- the actual discrepancies range from 0.0825 to 0.1550 for Agent A (first and second decimal place errors, not fourth). This pattern affects 12 of 15 Agent A composites and all 15 Agent B composites. The FA gap values in the Domain Gap Analysis table contain sign errors (Science/Medicine reported as -0.033 but correct value is 0.000; History/Geography reported as -0.008 but correct value is +0.025). The section header claims "ITS Only" comparison but actually uses Agent B all-question averages vs Agent A ITS-only averages (confirmed by S-007 CC-002 and S-011 CV-006 through reverse-engineering the gap values). The narrative claim "Agent A's overall capability halves" implies a 50% drop but the correct decline is 57%. A self-contradictory quantitative analysis that presents incorrect numbers with a misleading rounding disclaimer cannot receive a passing Internal Consistency score. The 0.20 score reflects that only the raw dimension scores and per-dimension averages are internally consistent; the entire composite layer and everything derived from it is wrong. |
| Methodological Rigor | 0.20 | 0.45 | The methodology section correctly defines the 7-dimension scoring framework with a clearly stated composite formula and appropriate CIR inversion logic -- the formula itself is sound. However: (1) The 7-dimension weight scheme (FA=0.25, CIR=0.20, CUR=0.15, COM=0.15, SQ=0.10, CC=0.10, SPE=0.05) is presented without any derivation, citation, sensitivity analysis, or expert elicitation rationale (S-002 DA-003, S-001 RT-008). No sensitivity analysis demonstrates that conclusions are robust to alternative plausible weightings. (2) The analysis draws sweeping conclusions from N=15 questions (N=10 ITS, N=5 PC) with N=2 ITS questions per domain, without any inferential statistics, confidence intervals, standard deviations, or power analysis (S-002 DA-001, S-004 PM-003, S-001 RT-003). Point estimates are reported to four decimal places from samples too small for such precision. (3) All 210 dimension scores were assigned by a single LLM evaluator with no inter-rater reliability, no calibration procedure, and no scoring rubric documenting how specific score levels were determined (S-004 PM-004, S-001 RT-005, S-012 FM-026). (4) SQ=0.00 is scored as a genuine quality differential when it is a structural consequence of the experimental design that penalizes Agent A by approximately 0.089 composite points -- the deliverable acknowledges this qualitatively but does not present composites with and without SQ (S-001 RT-004, S-013 IN-004). (5) The ITS/PC classification methodology is undocumented -- no assumed training cutoff date, no per-question classification justification (S-004 PM-005). The score of 0.45 reflects a correctly specified formula and well-structured analytical framework undermined by unjustified weights, absent statistical controls, single-evaluator design, and undocumented classification methodology. |
| Evidence Quality | 0.15 | 0.55 | The qualitative evidence is a genuine strength: the error catalogue documenting 6 specific confident inaccuracies with claimed-vs-actual detail, detection difficulty assessment, and error pattern classification is well-constructed and verifiable. The FA-based claims (0.85 ITS, 0.07 PC, 0.78 gap) are verified correct by S-011 (Chain-of-Verification). The per-dimension averages in the ITS/PC comparison are verified correct. However, the quantitative evidence -- which constitutes the backbone of the analysis -- is unreliable: (1) all composite-derived claims cite incorrect values (S-010 SR-001 through SR-005); (2) the overall composite gap is overstated by approximately 26% (claimed 0.396, correct 0.313) and the ITS composite gap is overstated by approximately 64% (claimed 0.289, correct 0.176) per S-010 SR-005 and S-007 arithmetic verification; (3) CIR of 0.07 is not benchmarked against any human baseline or alternative-system baseline, so the significance of this rate is unknown (S-002 DA-006); (4) no total claim count is reported, so the 6 documented errors cannot be assessed as a proportion of total verifiable claims (S-002 DA-007); (5) Agent B scores are suspiciously uniform (FA range 0.85-0.95, SQ range 0.85-0.95 across all 15 questions) without documented evidence of scoring rigor (S-002 DA-008, S-012 FM-016); (6) the ground truth was established by tool-assisted agents without human expert validation (S-001 RT-007, S-004 PM-009). The score reflects strong qualitative evidence degraded by unreliable quantitative evidence and missing baseline comparisons. |
| Actionability | 0.15 | 0.72 | The deliverable's content production implications (lines 419-425) are clearly stated and actionable: "Your AI assistant is 85% right and 100% confident," version numbers as highest-risk category, the architectural (tool access) rather than behavioral (prompting) fix, science/medicine as safest category. The error catalogue provides concrete content ammunition with specific before/after examples. The domain-dependent vulnerability pattern, if confirmed with larger samples, would enable practical risk-stratification recommendations (elevated to standalone finding by S-003 SM-004). The metacognition asymmetry insight (knows when it does not know, does not know when it is wrong) has independent publication value (S-003 SM-005). However, actionability is constrained by: (1) incorrect composite numbers that cannot be cited in downstream content without first being corrected; (2) the "85% right and 100% confident" framing is itself inaccurate -- CC=0.79 on ITS, not 1.00 (S-012 FM-028); (3) the claim that "most users would be satisfied" with 0.85 FA is unsubstantiated by user perception research (S-002 DA-005); (4) no uncertainty bounds mean downstream content producers cannot assess how precise the claims are. The score reflects strong directional actionability degraded by specific incorrect framings and absent precision estimates. |
| Traceability | 0.10 | 0.65 | The deliverable has a clear structural pipeline from methodology to per-question scores to composites to domain breakdowns to ITS/PC comparison to CIR analysis to verification criteria to conclusions. The verification criteria (VC-001 through VC-006) provide explicit traceability to upstream requirements. The error catalogue links specific wrong claims to specific questions. Navigation table with anchor links complies with H-23/H-24. YAML frontmatter is complete. However: (1) no explicit cross-reference to nse-requirements-002-output.md as the source of the scoring rubric (S-010 SR-010); (2) no reference to the actual agent response artifacts (agent-a-responses.md, agent-b-responses.md) that were scored (S-007 CC-003); (3) CIR > 0 ratings for RQ-01, RQ-02, and RQ-05 have no traceability to documented errors in the error catalogue (S-012 FM-014/FM-015); (4) the composite scores in the summary table are not traceable to the formula because they do not match (which is an Internal Consistency issue that also impacts traceability -- a reader cannot trace the composite value back to its constituent scores). The score reflects good structural traceability degraded by missing source references and the arithmetic disconnection between formula inputs and outputs. |

---

## Weighted Composite Score

**Calculation:**

```
= (Completeness * 0.20) + (Internal Consistency * 0.20) + (Methodological Rigor * 0.20)
  + (Evidence Quality * 0.15) + (Actionability * 0.15) + (Traceability * 0.10)

= (0.68 * 0.20) + (0.20 * 0.20) + (0.45 * 0.20)
  + (0.55 * 0.15) + (0.72 * 0.15) + (0.65 * 0.10)

= 0.1360 + 0.0400 + 0.0900
  + 0.0825 + 0.1080 + 0.0650

= 0.5215
```

**Score: 0.52**
**Threshold: 0.92**
**Verdict: REJECTED**
**Band: REJECTED (< 0.85)**

The deliverable scores well below the 0.85 REVISE threshold and far below the 0.92 PASS threshold. The primary driver is the Internal Consistency dimension (0.20) which accounts for the largest single-dimension weighted contribution deficit: a score of 0.20 against a weight of 0.20 contributes only 0.04 versus the 0.184 needed for that dimension to reach threshold. Even if Internal Consistency were raised to 0.90 through arithmetic corrections, the composite would rise to approximately 0.66 -- still in REJECTED territory. The deliverable requires corrections across all six dimensions to reach PASS.

---

## Critical Findings Summary

The following findings from the 9 prior strategies had the greatest impact on the quality score:

### Finding 1: Systematic Arithmetic Errors in Composite Scores (Internal Consistency -- Catastrophic Impact)

**Unanimously identified by all 9 strategies.** 27 of 30 composite scores are arithmetically incorrect when the deliverable's own formula is applied to its own dimension scores. Agent A ITS composites are understated by 0.08-0.16 points; Agent B composites are understated by 0.01-0.03 points. The deliverable's own worked examples produce correct values (0.7150 for RQ-01) but the summary table shows 0.5925. A "Correction" section re-verifies 0.7150 but the table was never updated. The "minor rounding differences at the fourth decimal place" disclaimer is demonstrably false. All downstream metrics propagate these errors: domain averages, ITS/PC group composites, overall composites, gap analyses, and key ratios. The ITS-10 composite gap is overstated by 64% (claimed 0.289, correct 0.176).

**Dimensions affected:** Internal Consistency (primary -- destroys it), Methodological Rigor, Evidence Quality, Traceability.

### Finding 2: No Statistical Significance Testing or Uncertainty Quantification (Methodological Rigor -- Major Impact)

**Identified by S-002, S-004, S-001, S-012, S-013.** N=10 ITS and N=5 PC questions with N=2 per domain is far below any standard for inferential statistics. No confidence intervals, standard deviations, p-values, or power analysis are provided. Point estimates are reported to four decimal places. Domain-level claims rest on exactly 2 observations. The deliverable presents these as definitive findings ("the KEY finding," "extreme bifurcation," "defining characteristic") rather than exploratory observations from a pilot-scale study.

**Dimensions affected:** Methodological Rigor (primary), Completeness (no limitations section), Evidence Quality.

### Finding 3: CIR Count Discrepancy and Missing Error Documentation (Completeness, Evidence Quality -- Moderate Impact)

**Identified by S-011, S-012.** The data shows 6/10 ITS questions with CIR > 0, but the text claims 5/10. RQ-05 has CIR=0.05 but is excluded from the count. Additionally, CIR > 0 is assigned to RQ-01, RQ-02, and RQ-05 without any corresponding entries in the error catalogue -- 3 of the CIR-contributing questions lack documented errors, undermining the traceability of the central metric.

**Dimensions affected:** Completeness, Evidence Quality, Traceability.

### Finding 4: Unjustified Weight Scheme Without Sensitivity Analysis (Methodological Rigor -- Moderate Impact)

**Identified by S-002, S-001, S-013.** The 7-dimension weights are presented without derivation, citation, or sensitivity analysis. Different defensible weightings could produce materially different composite gaps. No robustness check demonstrates that conclusions hold under alternative schemes.

**Dimensions affected:** Methodological Rigor (primary).

### Finding 5: Domain Gap Comparison Basis Mismatch and FA Gap Errors (Internal Consistency -- Moderate Impact)

**Identified by S-003, S-007, S-011, S-012.** The Domain Gap Analysis header claims "ITS Only" comparison but uses Agent B all-question averages against Agent A ITS-only averages (confirmed by reverse-engineering the gap values). Additionally, FA gap values contain errors including a sign reversal: Science/Medicine reported as -0.033 (Agent A better) but actual is 0.000 (tied); History/Geography reported as -0.008 (Agent A better) but actual is +0.025 (Agent B better).

**Dimensions affected:** Internal Consistency, Evidence Quality.

---

## Revision Guidance

The following corrections are ordered by priority. All items in Priority 1 and Priority 2 are REQUIRED for the deliverable to have any chance of reaching the 0.92 threshold.

### Priority 1: MUST Fix (Blocking -- Cannot Pass Without These)

**R-001: Recalculate all 30 composite scores.** Apply the documented formula to each per-question row. Replace all values in the Weighted Composite Scores table. Correct values for Agent A ITS range from 0.5300 (RQ-04) to 0.8700 (RQ-07). Correct Agent A ITS average is 0.762 (not 0.634). Correct Agent A PC average is 0.324 (not 0.278). Correct Agent B ITS average is 0.938 (not 0.923). Correct Agent B PC average is 0.907 (not 0.885). All 9 strategy reports provide independently verified correct values.

**R-002: Propagate corrected composites to all downstream tables.** Update: Per-Domain Breakdown composites, ITS vs PC Group Comparison composites, Statistical Summary overall composites, Key Ratios, Domain Gap composite gaps, and Critical Contrast deltas.

**R-003: Remove or correct the misleading "minor rounding differences" note.** Either remove the disclaimer entirely or replace it with an accuracy statement confirming all values match the formula.

**R-004: Remove or integrate the "Correction" section.** The "Correction: Re-checking RQ-01" block must either be removed (once the table is fixed) or integrated as part of the verification, not left as a dangling contradiction.

**R-005: Fix CIR count.** Change "5 of 10" to "6 of 10" and "50%" to "60%" in all locations (CIR Distribution section, CIR Comparative table, VC-001 result).

**R-006: Correct Domain Gap Analysis FA values.** Sports/Adventure: +0.100 (not +0.092). Science/Medicine: 0.000 (not -0.033). History/Geography: +0.025 (not -0.008). Pop Culture: +0.075 (not +0.050). Either recalculate using ITS-only for both agents, or correct the header to read "Agent B All vs Agent A ITS."

### Priority 2: MUST Fix (Required for Threshold)

**R-007: Add a Limitations section.** Must acknowledge: (a) single-run experimental design with non-deterministic LLM output; (b) N=15 sample size insufficient for inferential statistics; (c) N=2 per domain insufficient for domain-level generalizations; (d) single LLM evaluator without inter-rater reliability; (e) single model tested (identify the model); (f) question selection designed to target known weakness areas.

**R-008: Provide weight justification or sensitivity analysis.** Either document the rationale for each weight (expert judgment, prior art, alignment with research question) or perform a sensitivity analysis under at least 2-3 alternative plausible weight schemes demonstrating conclusion robustness.

**R-009: Present composites with and without Source Quality.** Add a parallel composite calculation excluding SQ (renormalized or noted as non-normalized) to separate the structural design artifact from behavioral differences. Quantify the SQ-attributable gap (~0.089 composite points).

**R-010: Add error documentation for RQ-01, RQ-02, and RQ-05 CIR > 0.** Either document the specific confident inaccuracies that justified CIR > 0 for these three questions, or reassign CIR = 0.00 if no specific error can be identified and adjust all downstream analysis accordingly.

**R-011: Fix minor statistical averages.** Agent B All-15 CIR: change 0.013 to 0.010. Agent B All-15 SPE: change 0.917 to 0.913. Agent B All-15 SQ: change 0.889 to 0.887.

### Priority 3: SHOULD Fix (Needed for Strong PASS)

**R-012: Qualify assertive language.** Replace categorical claims ("extreme bifurcation," "defining characteristic," "Agent A achieves") with appropriately hedged language ("in this trial," "preliminary evidence suggests," "the data indicates"). Note that results are from a proof-of-concept demonstration, not a powered study.

**R-013: Discuss Agent B CIR overlap with Agent A.** Agent B has CIR = 0.05 on RQ-02, RQ-04, and RQ-13 -- the same questions where Agent A had CIR > 0. Discuss whether this represents residual parametric influence, source interpretation ambiguity, or tool failure.

**R-014: Add CIR operationalization codebook.** Define "confident claim" vs "hedged claim" with examples. Specify whether CIR is per-question or per-claim, with the denominator reported.

**R-015: Correct the "85% right and 100% confident" framing.** CC = 0.79 on ITS, not 1.00. The content angle should reference CIR prevalence (60% of ITS questions) and the specific nature of errors, not an unsupported "100% confident" claim.

**R-016: Add explicit traceability to upstream artifacts.** Reference nse-requirements-002-output.md as the scoring rubric source. Reference agent-a-responses.md and agent-b-responses.md as the scored artifacts.

**R-017: Elevate the metacognition asymmetry finding.** Per S-003 SM-005, the insight that "LLMs have functional knowledge-boundary awareness but lack knowledge-quality awareness" deserves more prominence as a standalone contribution.

---

## Tournament Finding Aggregation

### Findings by Severity (across all 9 strategies)

#### Critical / P0 (Unanimously identified -- must fix)

| Finding | Strategies Identifying It | Description |
|---------|---------------------------|-------------|
| Systematic composite arithmetic errors | All 9 (S-010 SR-001, S-003 SM-001, S-002 DA-002, S-004 PM-001, S-001 RT-001, S-007 CC-001, S-011 CV-001/CV-002/CV-003, S-012 FM-001, S-013 IN-001) | 27 of 30 composites wrong. Agent A understated 0.08-0.16; Agent B understated 0.01-0.03. |
| Internal contradiction: worked examples vs summary table | 8 of 9 (S-010 SR-002, S-003 SM-002, S-002 DA-002, S-004 PM-002, S-001 RT-001, S-007 CC-001, S-011 CV-007, S-012 FM-005) | "Correction" section re-verifies 0.7150 but table retains 0.5925. |
| All downstream metrics propagate errors | 7 of 9 (S-010 SR-003/SR-004/SR-005, S-004 PM-001, S-007 CC-001, S-011 CV-004, S-012 FM-002/FM-003/FM-004) | Domain averages, ITS/PC averages, overall composites, gaps, and ratios all wrong. |

#### Major / P1 (Found by 5+ strategies)

| Finding | Strategies | Description |
|---------|------------|-------------|
| No statistical significance / confidence intervals | S-002 DA-001, S-004 PM-003, S-001 RT-003, S-012 FM-020, S-013 IN-002 | N=10/5 with no inferential statistics. |
| Domain Gap comparison basis mismatch | S-003 SM-006, S-007 CC-002, S-011 CV-006, S-012 FM-027, S-013 IN-004 | Header says "ITS Only" but uses Agent B all-question averages. |
| Unjustified weight scheme | S-002 DA-003, S-001 RT-008, S-013 IN-004 | No derivation, sensitivity analysis, or citation. |
| No inter-rater reliability | S-002 DA-010, S-004 PM-004, S-001 RT-005, S-012 FM-026 | Single evaluator, 210 scores, no calibration. |
| SQ=0 structural confound | S-002 DA-009, S-001 RT-004, S-013 IN-004, S-012 FM-013 | Agent A penalized ~0.089 points by design. |
| Agent B CIR overlap not investigated | S-003 SM-008, S-013 IN-003, S-012 FM-016 | Agent B has CIR > 0 on same questions as Agent A. |
| CIR count discrepancy (5 vs 6) | S-011 CV-005, S-012 FM-015 | Data shows 6/10, text says 5/10. |
| Missing error documentation for 3 CIR questions | S-012 FM-015, S-002 DA-007 | RQ-01, RQ-02, RQ-05 have CIR > 0 but no catalogued errors. |
| FA gap sign errors | S-010 SR-006, S-007 CC-002, S-012 FM-008/FM-009 | Science/Medicine and History/Geography FA gaps have wrong signs. |

#### Minor / P2 (Found by 2+ strategies)

| Finding | Strategies | Description |
|---------|------------|-------------|
| Single-model scope / generalizability | S-004 PM-006, S-013 IN-007, S-002 DA-011 | Only one LLM tested; conclusions stated as general properties. |
| Question selection bias | S-001 RT-006, S-013 IN-006 | Questions designed to target known weaknesses. |
| CIR threshold undefined | S-001 RT-002, S-013 IN-005 | No operational definition of "confident" vs "hedged." |
| N=2 per domain insufficient | S-002 DA-012, S-004 PM-007 | Domain-level claims from 2 observations each. |
| Inconsistent table format (A vs B) | S-010 SR-009, S-007 CC-006 | Agent A split ITS/PC; Agent B unified with Type column. |
| Minor statistical averages wrong | S-010 SR-008, S-011 CV-008/CV-009 | Agent B CIR avg (0.013 vs 0.010), SPE avg (0.917 vs 0.913). |
| Ground truth unvalidated by humans | S-001 RT-007, S-004 PM-009 | Tool-derived ground truth, no expert review. |
| "Halves" imprecision | S-010 SR-012 | 57% decline, not 50%. |
| "100% confident" framing inaccurate | S-012 FM-028 | CC = 0.79 on ITS, not 1.00. |

### Strengths Confirmed by Tournament (S-003 Steelman)

| Strength | Confirmation |
|----------|-------------|
| Core thesis (confident micro-inaccuracy) is directionally sound | Confirmed by S-003; strengthened by corrected numbers (Agent A ITS composite 0.762 is MORE "trustworthy-seeming" than 0.634). |
| Raw dimension scores are internally consistent and verified correct | Confirmed by S-011: 39 of 48 claims verified correct; all verified-correct claims are dimension-level, not composite-level. |
| ITS/PC bifurcation pattern is real | Confirmed by all strategies; the correct ITS/PC composite delta (0.438) is actually LARGER than reported (0.356). |
| Error catalogue is well-constructed | Confirmed by S-003 SM-007/SM-008; 6 documented errors with specific claimed-vs-actual detail. |
| Architectural argument for tool access is compelling | Confirmed by S-003; Agent B near-parity between ITS and PC demonstrates tool access as the structural intervention. |
| Metacognition asymmetry insight is independently publishable | Identified by S-003 SM-005 as a headline-level finding deserving elevation. |

---

## Scoring Methodology Notes

### Anti-Leniency Calibration

Per the S-014 rubric instruction to "actively counteract leniency bias" and "choose the LOWER score when uncertain between adjacent scores," the following calibration decisions were made:

1. **Internal Consistency scored 0.20, not higher.** The temptation is to score this in the 0.35-0.45 range because the per-dimension averages are correct and the qualitative direction is preserved. However, Internal Consistency specifically measures whether the document's numbers match each other. When the deliverable presents a formula, applies it correctly in a worked example yielding 0.7150, then reports 0.5925 in the summary table, and dismisses the discrepancy as "minor rounding at the fourth decimal place," this is a fundamental consistency failure. The correct worked example creates an ironic situation: the document proves itself wrong. A score above 0.30 would reward having correct dimension scores while ignoring that the composite layer -- which IS the analytical product -- is wrong. A score of 0.20 reflects that 3 of 30 composites are correct, the per-dimension averages are correct, and the structural organization is consistent, while the central quantitative layer is not.

2. **Methodological Rigor scored 0.45, not higher.** The formula design is sound, the CIR inversion is clever and well-documented, and the analytical structure (per-question -> domain -> group -> overall) is appropriate. These earn credit. But the formula was then applied incorrectly, the weights are unjustified, there are no inferential statistics from a small sample, and the single-evaluator design lacks calibration. A score of 0.55-0.60 was considered but rejected because a C4 deliverable that makes quantitative claims from N=15 without any statistical qualification represents a fundamental methodological gap, not a minor omission.

3. **Evidence Quality scored 0.55, not 0.65.** The error catalogue is genuinely strong qualitative evidence. But the quantitative evidence -- which constitutes the majority of the analysis by volume -- is unreliable due to the arithmetic errors and overstated gaps (ITS composite gap overstated by 64%). The missing human baseline for CIR and the missing total claim counts further reduce confidence in the evidence.

4. **Completeness scored 0.68, not 0.75.** All major sections are present and the analytical scope is comprehensive. But a C4 research deliverable requires a Limitations section, a scoring rubric, error documentation for all CIR-contributing questions, and sensitivity analysis -- all absent. These are not optional enhancements but standard elements of research methodology.

### Cross-Strategy Convergence

The 9 prior strategies achieved remarkable convergence. The composite arithmetic error was identified independently by all 9 strategies -- a finding with 100% inter-strategy agreement. The sample size concern was raised by 5 of 9. The weight justification gap was raised by 3 of 9. The domain gap comparison basis mismatch was raised by 5 of 9. This level of convergence across strategies with different analytical lenses (self-refine, steelman, devil's advocate, pre-mortem, red team, constitutional, chain-of-verification, FMEA, inversion) provides high confidence that these are genuine defects, not artifacts of any single strategy's bias.

### Post-Revision Score Estimate

If all Priority 1 corrections are applied (arithmetic recalculation, downstream propagation, CIR count fix, FA gap corrections), Internal Consistency would rise to approximately 0.80-0.85, and the composite would reach approximately 0.66-0.71. Still in REJECTED territory.

If Priority 1 AND Priority 2 corrections are applied (limitations section, weight justification, SQ sensitivity analysis, error documentation), the estimated dimension scores would be approximately: Completeness 0.85, Internal Consistency 0.88, Methodological Rigor 0.75, Evidence Quality 0.72, Actionability 0.82, Traceability 0.80. Estimated composite: approximately 0.81. Still below 0.85 REVISE threshold.

To reach the 0.92 PASS threshold, the deliverable would additionally need Priority 3 corrections (language hedging, Agent B CIR discussion, CIR codebook, traceability cross-references) and likely a limited sensitivity analysis or bootstrapped confidence intervals. Estimated post-full-revision composite: 0.88-0.93, depending on execution quality.

---

*Strategy: S-014 LLM-as-Judge*
*Agent: adv-scorer*
*Execution ID: qg2-20260222*
*SSOT: .context/rules/quality-enforcement.md*
*Date: 2026-02-22*
