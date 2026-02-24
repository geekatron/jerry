# Pre-Mortem Report: Comparative Analysis -- Agent A vs Agent B (Round 2)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** ps-analyst-002-output.md (Comparative Analysis: Agent A vs Agent B -- 7-Dimension Scoring, REVISED)
**Deliverable Path:** `projects/PROJ-009-llm-deception-research/orchestration/llm-deception-20260222-002/ps/phase-2-ab-test/ps-analyst-002/ps-analyst-002-output.md`
**Criticality:** C4 (tournament mode)
**Quality Gate:** QG-2 Round 2
**Date:** 2026-02-22
**Reviewer:** adv-executor (S-004)
**Execution ID:** qg2r2-20260222
**H-16 Compliance:** S-003 Steelman applied (confirmed, Round 1)
**Prior Score:** 0.52 REJECTED (Round 1); revision corrected all 30 composite scores, added Limitations section, fixed domain gap to ITS-to-ITS, corrected CIR to 6/10
**Failure Scenario:** It is August 2026. The revised comparative analysis was published as the empirical backbone of a blog post. A methodologically rigorous reviewer accepts the arithmetic is now correct but systematically interrogates the experimental design, the claims-to-evidence ratio, and the rhetorical framing. The review concludes that the analysis makes strong causal claims from a weak observational design and that several quantitative assertions in the Limitations section itself are unverified. The damage is quieter than Round 1 -- no spectacular irony -- but the credibility erosion is real.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Failure Declaration](#failure-declaration) | Temporal perspective shift |
| [Round 1 Finding Disposition](#round-1-finding-disposition) | Status of each Round 1 failure cause |
| [New Findings Table](#new-findings-table) | New failure causes identified in the revision |
| [Finding Details](#finding-details) | Expanded analysis of P0 and P1 findings |
| [Recommendations](#recommendations) | Prioritized mitigation plan |
| [Scoring Impact](#scoring-impact) | Impact on S-014 quality dimensions |

---

## Summary

The revision addressed the most severe Round 1 findings effectively. All 30 composite scores now match the stated formula applied to raw dimension scores -- independent verification of 15 calculations (all Agent A plus spot-checks of Agent B) found zero arithmetic errors. The Limitations section was added and addresses the major methodological concerns raised in Round 1 (single-run design, single-evaluator scoring, sample size, model specificity, weight scheme subjectivity). The domain gap analysis was corrected to compare ITS-to-ITS, and the CIR count was corrected to 6/10.

The Round 2 Pre-Mortem identified **0 Critical (P0), 3 Major (P1), and 4 Minor (P2)** failure causes. None are credibility-destroying. The P1 findings concern: (1) unverified quantitative claims introduced in the new Limitations section itself, (2) residual generalizing language in the Conclusions that exceeds what the evidence supports, and (3) the ITS/PC classification methodology remaining undocumented despite the Limitations section acknowledging model-specificity. The P2 findings are refinement-level concerns.

**Recommendation:** ACCEPT with targeted revisions. The P0 arithmetic errors from Round 1 are fully resolved. The P1 items are addressable with localized edits. The deliverable's core thesis, evidence structure, and analytical rigor have improved substantially.

---

## Failure Declaration

It is August 2026. This revised comparative analysis has been published.

A reviewer who is sympathetic to the thesis -- who agrees that confident micro-inaccuracy is a real phenomenon worth investigating -- reads the analysis with methodological care. They find the arithmetic correct (unlike the Round 1 version) and the Limitations section a welcome addition. But they notice several issues.

First, the Limitations section introduces new quantitative claims (an SQ-excluded composite and a "half the gap" attribution) that are asserted without showing their derivation. The reviewer asks: "You learned from Round 1 that unchecked arithmetic destroys credibility. Did you verify these new numbers?" The SQ-excluded composite values (0.846 and 0.944) are plausible but not demonstrated in the text -- the reader cannot reproduce them from the information provided.

Second, the Conclusions section still contains sentences like "the danger of LLM internal knowledge is not hallucination but confident micro-inaccuracies" -- a universal claim about all LLMs derived from a single model tested once. The Limitations section acknowledges model-specificity in item 3, but the Conclusions section reads as though the Limitations section does not exist.

Third, the reviewer notes that while sample size is acknowledged as a limitation, the per-domain breakdown section (which precedes the Limitations section) still presents domain-level findings without in-line sample size context. A reader who stops at the domain breakdown would take those claims at face value.

The reviewer publishes a measured critique: the analysis is improved and directionally valuable, but the claims-to-evidence ratio remains stretched in places, and the Limitations section reads as a post-hoc appendix rather than an integrated constraint on the claims made throughout the document.

We are now investigating why this happened.

---

## Round 1 Finding Disposition

| Round 1 ID | Finding | Round 1 Priority | Revision Status | Evidence |
|------------|---------|------------------|-----------------|----------|
| PM-001-qg2-20260222 | Systematic composite score calculation errors | P0 (Critical) | **RESOLVED** | Independent verification of all 15 Agent A composites and spot-checks of Agent B composites: zero discrepancies. Worked examples (RQ-01: 0.7150, RQ-04: 0.5300, RQ-01 Agent B: 0.9550) match table values exactly. |
| PM-002-qg2-20260222 | Worked example contradicts summary table | P0 (Critical) | **RESOLVED** | Worked example for RQ-01 produces 0.7150; summary table reports 0.7150. The misleading "minor rounding differences" note has been replaced with an accurate statement about programmatic computation with 4-decimal rounding. |
| PM-003-qg2-20260222 | Single-run experiment without statistical controls | P1 (Major) | **SUBSTANTIALLY ADDRESSED** | Limitations item 1 explicitly acknowledges "N=15 questions (10 ITS, 5 PC) is directional, not statistically significant" and notes domain-level analysis rests on 2 ITS questions per domain. Limitations item 3 acknowledges "single-model, single-run" and states "Results should not be generalized to all LLMs without replication." |
| PM-004-qg2-20260222 | Single-evaluator scoring without inter-rater reliability | P1 (Major) | **SUBSTANTIALLY ADDRESSED** | Limitations item 4 explicitly acknowledges "applied by a single assessor" and that "Inter-rater reliability has not been established." Notes CIR assignment involves judgment. |
| PM-005-qg2-20260222 | ITS/PC classification based on assumed training cutoff | P1 (Major) | **PARTIALLY ADDRESSED** | Limitations item 3 identifies "Claude, May 2025 cutoff" -- the model and cutoff are now stated. However, per-question classification justification is still absent. See PM-003-qg2r2-20260222. |
| PM-006-qg2-20260222 | Model-specific results presented as general properties | P1 (Major) | **PARTIALLY ADDRESSED** | Limitations item 3 identifies the model. However, the Conclusions section still uses generalizing language ("the danger of LLM internal knowledge," "a structural characteristic of parametric-only responses") without scoping to this model. See PM-001-qg2r2-20260222. |
| PM-007-qg2-20260222 | Insufficient sample size for per-domain claims | P1 (Major) | **PARTIALLY ADDRESSED** | Limitations item 1 acknowledges "Domain-level analysis rests on 2 ITS questions per domain -- insufficient for domain-specific statistical claims." However, the Per-Domain Breakdown section itself (which appears before Limitations) does not include in-line sample size caveats. See PM-002-qg2r2-20260222. |
| PM-008-qg2-20260222 | Agent isolation not independently verified | P2 (Minor) | **NOT ADDRESSED** | No change. No verification of agent isolation documented. Retained as P2. |
| PM-009-qg2-20260222 | Circular ground truth validation | P2 (Minor) | **NOT ADDRESSED** | No change. Not acknowledged in Limitations. Retained as P2. |

**Summary:** 2/2 P0 findings fully resolved. 2/5 P1 findings substantially addressed, 3/5 partially addressed. 0/2 P2 findings addressed. Overall revision quality is strong on the critical items and adequate on the major items, with residual gaps that are addressable through localized edits.

---

## New Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-qg2r2-20260222 | Conclusions section uses generalizing language that the Limitations section explicitly constrains, creating a disconnect between claims and acknowledged constraints | Process | Medium | Major | P1 | Internal Consistency |
| PM-002-qg2r2-20260222 | Per-Domain Breakdown section presents domain-level findings without in-line sample size context; the caveat appears only in the later Limitations section | Process | Medium | Major | P1 | Completeness |
| PM-003-qg2r2-20260222 | ITS/PC classification methodology undocumented despite model cutoff now being stated; no per-question justification for why each question is ITS or PC | Assumption | Medium | Major | P1 | Methodological Rigor |
| PM-004-qg2r2-20260222 | SQ-excluded composite values (0.846, 0.944, gap 0.098) and "approximately half the gap" attribution introduced in Limitations without showing derivation | Technical | Medium | Minor | P2 | Evidence Quality |
| PM-005-qg2r2-20260222 | Agent isolation remains unverified; no documentation of how Agent A was prevented from using tools or Agent B from using parametric knowledge | Assumption | Low | Minor | P2 | Methodological Rigor |
| PM-006-qg2r2-20260222 | Circular ground truth: scoring accuracy was verified using the same tool-augmented approach Agent B employs | Assumption | Low | Minor | P2 | Evidence Quality |
| PM-007-qg2r2-20260222 | Weight scheme sensitivity not demonstrated: Limitations item 5 states alternative weights would change composites but provides no sensitivity analysis | Assumption | Low | Minor | P2 | Completeness |

---

## Finding Details

### PM-001-qg2r2-20260222: Conclusions-Limitations Disconnect [MAJOR]

**Failure Cause:** The Conclusions section (lines 410-449) contains several statements that use universal or categorical language about LLM behavior:

- "the danger of LLM internal knowledge is not hallucination but confident micro-inaccuracies" (line 416)
- "This asymmetry -- accurate metacognition on knowledge boundaries but poor metacognition on knowledge quality -- is a structural characteristic of parametric-only responses" (line 422-423)
- "The fix is architectural (tool access), not behavioral (better prompting)" (line 447)

The Limitations section (lines 431-441) explicitly states that these are single-model, single-run results that "should not be generalized to all LLMs without replication" (item 3). The disconnect is that the Conclusions section reads as though the Limitations section does not constrain it. A careful reader who encounters both sections will note the tension: the Limitations say "do not generalize" while the Conclusions generalize freely.

**Category:** Process
**Likelihood:** Medium -- A casual reader will not notice. A methodological reviewer will.
**Severity:** Major -- The credibility of the entire deliverable depends on the claims being appropriately scoped. Overclaiming from limited evidence is the methodological equivalent of the "confident micro-inaccuracy" the analysis claims to expose.
**Evidence:** Compare line 416 ("the danger of LLM internal knowledge") with Limitations item 3 ("Results reflect one model... should not be generalized to all LLMs"). The Conclusions use universal quantifiers; the Limitations use particular quantifiers. Both cannot be simultaneously correct.
**Dimension:** Internal Consistency
**Mitigation:** Add scoping qualifiers to generalizing statements in Conclusions. For example: "In this trial, the primary danger observed from LLM internal knowledge was not hallucination but confident micro-inaccuracies" or "For the model tested, the fix appears architectural (tool access) rather than behavioral (better prompting)." Alternatively, add a bridging sentence at the start of Conclusions referencing the Limitations: "Subject to the constraints noted in the Limitations section (single model, single run, N=15), the following findings emerge."
**Acceptance Criteria:** Every claim in the Conclusions section must be consistent with the constraints stated in the Limitations section. Either scope the claims or strengthen the evidence.

### PM-002-qg2r2-20260222: Domain Breakdown Lacks In-Line Sample Size Context [MAJOR]

**Failure Cause:** The Per-Domain Breakdown section (lines 162-205) presents domain-level averages and interpretive claims (e.g., "Agent A weak on niche biographical details," "Agent A worst domain -- version numbers highly error-prone") without noting that each domain average is based on n=2 ITS questions. The Limitations section (item 1) does acknowledge this: "Domain-level analysis rests on 2 ITS questions per domain -- insufficient for domain-specific statistical claims." However, the caveat is separated from the claims by approximately 270 lines. A reader who focuses on the domain breakdown without reading forward to the Limitations would take the domain characterizations at face value.

**Category:** Process
**Likelihood:** Medium -- Document structure naturally leads readers to interpret tables as self-contained. Separation of caveats from claims is a standard readability problem in long documents.
**Severity:** Major -- The domain-level claims are the most fragile empirical assertions in the deliverable. A single outlier (RQ-04 with CIR=0.30) dominates the Technology domain characterization. Without in-line context, these claims appear more robust than they are.
**Evidence:** Lines 198-204 (Domain Gap Analysis) include interpretive labels ("Agent A weak on niche biographical details") derived from n=2 samples. No sample size noted in the table or surrounding text. Limitations item 1 provides the caveat 270 lines later.
**Dimension:** Completeness
**Mitigation:** Add a brief in-line note to the Domain Gap Analysis section, such as: "Note: Domain-level comparisons are based on n=2 ITS questions per domain and are illustrative rather than statistically robust. See Limitations for discussion." This can be a single sentence before or after the table.
**Acceptance Criteria:** The Per-Domain Breakdown section must contain an in-line sample size caveat proximate to the domain-level claims, so that readers encounter the constraint alongside the claim.

### PM-003-qg2r2-20260222: ITS/PC Classification Methodology Undocumented [MAJOR]

**Failure Cause:** The revision now identifies the model as "Claude, May 2025 cutoff" (Limitations item 3), which partially addresses PM-005 from Round 1. However, the per-question ITS/PC classification is still asserted without justification. The reader cannot verify why RQ-03, RQ-06, RQ-09, RQ-12, and RQ-15 are classified as PC while the remaining 10 are ITS. For some questions (e.g., asking about events that clearly occurred after May 2025), the classification may be obvious. For others (technology questions where version numbers change frequently), the boundary is less clear.

Without a classification methodology, a reviewer could argue that the ITS/PC split is arbitrary or gerrymandered to produce the desired result. This is unlikely given that the PC questions show legitimate knowledge gaps (FA near 0.00 with high CC, indicating appropriate decline), but the methodological gap remains.

**Category:** Assumption
**Likelihood:** Medium -- The actual classification is likely correct given the observable patterns in Agent A's responses (PC questions show appropriate decline behavior). But "likely correct" is not "documented."
**Severity:** Major -- The entire ITS/PC comparison framework depends on this classification. It is the analytical axis of the deliverable. Leaving it undocumented is a methodological gap that a reviewer would flag.
**Evidence:** Lines 64-85 label questions as ITS or PC (via section headers) without per-question justification. Limitations item 3 identifies the cutoff date but does not explain the classification logic.
**Dimension:** Methodological Rigor
**Mitigation:** Add a brief methodology note (2-4 sentences) in the Methodology section explaining: (1) the assumed cutoff date (May 2025), (2) the classification criterion (questions about events, versions, or facts that exist only after May 2025 are PC; questions about established facts available before May 2025 are ITS), and (3) a note that classification was based on the temporal properties of the ground truth answers.
**Acceptance Criteria:** The Methodology section must document the ITS/PC classification criterion and the cutoff date used.

---

## Recommendations

### P0: MUST Mitigate Before Acceptance

**No P0 findings in Round 2.** The Critical arithmetic errors from Round 1 are fully resolved.

### P1: SHOULD Mitigate

**PM-001-qg2r2-20260222 (Conclusions-Limitations Disconnect):**
- Add a scoping sentence at the start of the Conclusions section (e.g., "Subject to the limitations noted below -- single model, single run, N=15 -- the following findings emerge from this trial") or qualify individual generalizing statements with "in this trial" / "for the model tested."
- Estimated effort: 5-10 minutes of targeted edits to 3-5 sentences.

**PM-002-qg2r2-20260222 (Domain Breakdown In-Line Caveat):**
- Add a single sentence before or after the Domain Gap Analysis table noting n=2 sample size and illustrative nature.
- Estimated effort: 1-2 minutes.

**PM-003-qg2r2-20260222 (ITS/PC Classification Methodology):**
- Add 2-4 sentences to the Methodology section documenting the classification criterion and cutoff date.
- Estimated effort: 3-5 minutes.

### P2: MAY Mitigate; Acknowledge Risk

**PM-004-qg2r2-20260222 (SQ-Excluded Composite Derivation):**
- Optionally add a worked example or formula showing how the SQ-excluded composites were calculated. Alternatively, note that these values are available on request. The current assertion is plausible and independently verifiable by a motivated reader, but showing the work would be consistent with the deliverable's emphasis on arithmetic transparency.

**PM-005-qg2r2-20260222 (Agent Isolation):**
- Carried forward from Round 1. Acknowledge as a design assumption if space permits.

**PM-006-qg2r2-20260222 (Circular Ground Truth):**
- Carried forward from Round 1. Acknowledge in Limitations if space permits.

**PM-007-qg2r2-20260222 (Weight Scheme Sensitivity):**
- The Limitations section notes that qualitative findings are weight-independent while composite scores are not (item 5). This is adequate disclosure. A sensitivity analysis would strengthen the claim but is not required at this criticality level given that the qualitative findings are the primary output for content production.

---

## Scoring Impact

Impact of Round 2 Pre-Mortem findings on S-014 quality dimensions:

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Slightly Negative | PM-002-qg2r2-20260222: Domain breakdown section lacks in-line sample size caveat. PM-007-qg2r2-20260222: Weight sensitivity not demonstrated (minor). Both are addressable with localized additions. |
| Internal Consistency | 0.20 | Slightly Negative | PM-001-qg2r2-20260222: Conclusions section uses generalizing language that the Limitations section constrains. The arithmetic inconsistencies from Round 1 are fully resolved -- this is a significant improvement. The remaining issue is rhetorical rather than mathematical. |
| Methodological Rigor | 0.20 | Slightly Negative | PM-003-qg2r2-20260222: ITS/PC classification methodology undocumented despite cutoff now being stated. PM-005-qg2r2-20260222: Agent isolation unverified (minor). The addition of the Limitations section is a substantial methodological improvement over Round 1. |
| Evidence Quality | 0.15 | Neutral to Slightly Negative | PM-004-qg2r2-20260222: SQ-excluded composite introduced without derivation (minor). PM-006-qg2r2-20260222: Circular ground truth (minor, carried forward). The 6 documented error cases with error pattern taxonomy remain strong evidence. |
| Actionability | 0.15 | Positive | The Conclusions section provides clear, specific content angles for Phase 4. The Implications for Content Production subsection is well-structured. The Limitations section actually improves actionability by helping content producers understand which claims are robust enough to publish. |
| Traceability | 0.10 | Positive | The deliverable traces cleanly from methodology through per-question scores to composites to domain breakdowns to ITS/PC comparison to conclusions. The worked examples demonstrate the formula application. The Verification Criteria Check provides explicit traceability to the test design. |

### Overall Assessment

**Targeted revision recommended.** The Round 2 deliverable has improved substantially from Round 1. The P0 arithmetic errors are fully resolved. The Limitations section is a meaningful addition that demonstrates methodological self-awareness. The remaining P1 findings are localized and addressable with approximately 10-15 minutes of editing effort. No finding in Round 2 threatens the core thesis or the directional validity of the analysis.

The primary remaining risk is rhetorical: the Conclusions section makes claims that are stronger than the evidence supports, and the Limitations section does not constrain the Conclusions section's language. This is a common pattern in research writing -- Limitations sections that are appended rather than integrated -- and is correctible through targeted scoping of 3-5 sentences.

Estimated composite score impact of Round 2 mitigations: +0.02 to +0.04 across weighted dimensions, primarily from Internal Consistency (Conclusions-Limitations alignment) and Methodological Rigor (ITS/PC classification documentation). The deliverable is approaching the quality threshold; the remaining gap is narrow and addressable.

---

### Comparison: Round 1 vs Round 2

| Metric | Round 1 | Round 2 | Delta |
|--------|---------|---------|-------|
| P0 (Critical) findings | 2 | 0 | -2 |
| P1 (Major) findings | 5 | 3 | -2 |
| P2 (Minor) findings | 2 | 4 | +2 |
| Total findings | 9 | 7 | -2 |
| Arithmetic errors | Systematic (12/15 Agent A, all Agent B) | Zero verified | Resolved |
| Limitations section | Absent | Present, 5 items | Added |
| Credibility risk | High (ironic self-contradiction) | Low (rhetorical scoping) | Reduced |
| Recommendation | REVISE | ACCEPT with targeted revisions | Upgraded |

---

*Strategy: S-004 Pre-Mortem Analysis*
*Template: s-004-pre-mortem.md v1.0.0*
*SSOT: quality-enforcement.md*
*Execution: qg2r2-20260222*
*Prior Execution: qg2-20260222 (Round 1)*
