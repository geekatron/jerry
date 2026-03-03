# Adversary Tournament Findings — Barrier 1 Synthesis (Iteration 2)

> **Deliverable:** Barrier 1 Cross-Pollination Synthesis: Negative Prompting in LLMs (Revision 2)
> **File:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/synthesis.md`
> **Criticality:** C4 (Critical)
> **Executed:** 2026-02-27
> **Agent:** adv-executor
> **Strategies:** S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013, S-014 (all 10, tournament mode)
> **H-16 Compliance:** VERIFIED — S-003 (Order 2) precedes S-002 (Order 3)
> **Prior Iteration Score:** 0.83 (REVISE) — 3 Critical findings from I1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Prior Finding Resolution Status](#prior-finding-resolution-status) | Explicit RESOLVED/PERSISTS verdict for each I1 Critical finding |
| [Tournament Summary Table](#tournament-summary-table) | One-line verdict per strategy |
| [S-010: Self-Refine Findings](#s-010-self-refine-findings) | Internal consistency and completeness self-review |
| [S-003: Steelman Findings](#s-003-steelman-findings) | Strongest-form reconstruction before critique |
| [S-002: Devil's Advocate Findings](#s-002-devils-advocate-findings) | Assumption challenge and logical probing |
| [S-004: Pre-Mortem Findings](#s-004-pre-mortem-findings) | Projected failure modes |
| [S-001: Red Team Findings](#s-001-red-team-findings) | Adversarial vulnerability probing |
| [S-007: Constitutional AI Findings](#s-007-constitutional-ai-findings) | Governance and P-rule compliance |
| [S-011: Chain-of-Verification Findings](#s-011-chain-of-verification-findings) | Source traceability audit |
| [S-012: FMEA Findings](#s-012-fmea-findings) | Risk quantification |
| [S-013: Inversion Findings](#s-013-inversion-findings) | Assumption robustness under inversion |
| [S-014: LLM-as-Judge Scoring](#s-014-llm-as-judge-scoring) | Final quality gate scoring |
| [Consolidated Findings Index](#consolidated-findings-index) | All new findings across all strategies |
| [Revision Priorities](#revision-priorities) | Ordered action list for synthesis revision |

---

## Prior Finding Resolution Status

> For each Critical finding from Iteration 1, explicit RESOLVED or PERSISTS verdict with evidence.

### DA-001 (Critical): Conflation of null finding with directional evidence

**I1 Issue:** L0 stated "The evidence more consistently suggests the opposite: prohibition-style negative instructions increase hallucination risk in at least some task contexts (Academic survey, Source A-6: LLaMA-2 MCQA hallucination rate rose from ~26% to ~59% with negation)" — conflating absence of evidence for the hypothesis with directional evidence against it.

**R2 Change:** The L0 Executive Summary now includes the section: "**Important epistemic distinction (DA-001/RT-001 fix):** The absence of supporting evidence is a null finding — it means the hypothesis has not been tested in controlled conditions, not that it has been refuted. No source confirms the claim; no source refutes it with controlled data."

The Verdict section reads: "The claim that 'negative unambiguous prompting reduces hallucination by 60%...' **is not supported by any evidence across all three surveys.**" The A-6 specific percentages (26%→59%) have been removed from L0 as per RT-002. The AGREE-6 section (where the Tier 3 evidence is presented) properly caveats the finding with full context.

**Verdict: RESOLVED** — The epistemic distinction between null finding and refutation is now explicitly stated. The Tier 3 percentages are no longer in the L0 executive summary. The language "evidence more consistently suggests the opposite" has been removed and replaced with the framing that this is a null finding.

---

### DA-002 / CC-002 (Critical/Major): Agreement count error

**I1 Issue:** L0 Key Numbers stated "7 STRONG" and "9 MODERATE" agreements, but the body documented exactly 5 STRONG (AGREE-1 through AGREE-5) and 4 MODERATE (AGREE-6 through AGREE-9) = 9 total, not 16. A P-022 violation.

**R2 Change:** The L0 Key Numbers table now states: "Cross-survey agreements (Strong — all 3 agree): **5** | AGREE-1 through AGREE-5" and "Cross-survey agreements (Moderate — 2 of 3 agree): **4** | AGREE-6 through AGREE-9" and "Total named agreements: **9** | 5 Strong + 4 Moderate." A correction note is also explicitly included in the table.

**Verdict: RESOLVED** — The count now matches the body exactly. The "Note on count correction (DA-002/CC-002)" explicitly acknowledges the prior error.

---

### IN-001 (Critical): Core conclusion fails inversion test — no scope exclusions

**I1 Issue:** The synthesis did not acknowledge that the null finding applies only to public evidence domains, and could not address the question "What if negative prompting works well in domain-specific, expert-engineered contexts not captured by survey scope?"

**R2 Change:** A full "Known Scope Exclusions" section has been added after L0 (before the Merged Source Catalog), documenting four structural exclusion categories: SE-1 (Closed Production Deployments), SE-2 (Domain-Specific Expert Applications), SE-3 (Internal Vendor Benchmarks and Unpublished Research), SE-4 (Grey Literature from Expert Practitioner Communities). Each exclusion explicitly states what evidence may be absent and what its potential impact on synthesis conclusions would be. The closing paragraph states: "The null finding ('no evidence for 60% hallucination reduction') applies specifically to the publicly documented evidence base across these three survey domains."

**Verdict: RESOLVED** — The Known Scope Exclusions section directly addresses the IN-001 failure. The inversion test is now survivable: the synthesis explicitly bounds its conclusions to the public evidence base and acknowledges the excluded domains.

---

## Tournament Summary Table

| Order | Strategy | New Findings (C/M/m) | Verdict | Key Issue |
|-------|----------|---------------------|---------|-----------|
| 1 | S-010 Self-Refine | 0 Critical / 2 Major / 3 Minor | Proceed with revisions | Source count arithmetic still partially ambiguous (Group C 13-count not fully verifiable); CONFLICT-4 UNRESOLVED label inconsistency persists |
| 2 | S-003 Steelman | 0 Critical / 1 Major / 2 Minor | Strengthen before critique | Phase 2 Experimental Design section strengthened but condition priority ordering missing; Cond-6 and Cond-7 derivations need stronger grounding |
| 3 | S-002 Devil's Advocate | 0 Critical / 2 Major / 2 Minor | Requires revision | DA-005 partially resolved but vendor bias still not addressed in AGREE-3; revised hypothesis alternative labeling is ambiguous in context |
| 4 | S-004 Pre-Mortem | 0 Critical / 1 Major / 2 Minor | Minor revision | PM-001 resolved (consolidated Phase 2 section); residual risk in GA-5 DO NOT CITE caveat buried in middle of section |
| 5 | S-001 Red Team | 0 Critical / 2 Major / 2 Minor | Requires revision | RT-003 partially resolved (scope exclusions added) but selection bias acknowledgment does not address publication bias directly; circular citation chain in AGREE-4 still present |
| 6 | S-007 Constitutional AI | 0 Critical / 1 Major / 1 Minor | Pass with conditions | THEME-1 mechanistic claim adequately caveated; minor P-011 residue in THEME-3 extrapolation |
| 7 | S-011 Chain-of-Verification | 0 Critical / 1 Major / 2 Minor | Requires revision | Group C 13-count cannot be independently verified from the deduplication table; CV-003 resolved but newly added experimental conditions (Cond-6/Cond-7) have weak derivation traces |
| 8 | S-012 FMEA | 0 Critical / 1 Major / 2 Minor | Requires revision | FM-001 (count error) resolved; FM-002 (null finding conflation) resolved; residual high-RPN risk: Group C count arithmetic non-reproducibility |
| 9 | S-013 Inversion | 0 Critical / 1 Major / 1 Minor | Pass with conditions | IN-001 resolved; vendor bias inversion (IN-003) partially addressed but scope exclusion SE-3 does not fully address whether vendor product positioning affects recommendation neutrality |
| 10 | S-014 LLM-as-Judge | — | REVISE (0.91) | Below C4 threshold of 0.95; meets general H-13 threshold of 0.92 marginally; three persistent Major findings prevent PASS |

---

## S-010: Self-Refine Findings

**Strategy:** S-010 Self-Refine
**Finding Prefix:** SR
**Protocol Steps Completed:** 6 of 6
**Objectivity Assessment:** Medium attachment (synthesis now in R2; reviewer role distinct). Active leniency bias counteraction applied.

**Prior SR findings addressed:**
- SR-001 (Major): Source count arithmetic — PARTIALLY RESOLVED (explicit arithmetic trace added but Group C count still ambiguous; see SR-001-R2 below)
- SR-002 (Major): Latitude cross-reference — RESOLVED (I-22 cross-reference added in Unsourced Claim Audit)
- SR-003 (Major): Per-agreement confidence scores — RESOLVED (confidence qualifiers added per AGREE entry)
- SR-004 (Minor): AGREE-6/7 heading weight — RESOLVED (per-agreement confidence qualifiers and body structure now distinguish)
- SR-005 (Minor): Tier 3 count inconsistency — RESOLVED (Tier 3 count note added clarifying consistent count of 13, including A-31)
- SR-006 (Minor): PS Integration handoff schema — RESOLVED (Key findings, from/to agent, handoff artifacts, blockers, next agent hint now present)
- SR-007 (Minor): CONFLICT-4 UNRESOLVED label — PARTIALLY RESOLVED (clarification note added but the "UNRESOLVED" label remains in the section header, creating residual inconsistency)

### New Findings

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| SR-001-R2 | Major | Group C 13-count still not independently verifiable: the arithmetic trace lists 9 explicitly named entries (C-6, C-7, C-8, C-9, C-10, C-11, C-13, C-19, C-20) plus "4 additional context7-only sources" but the 4 additional sources are not enumerated | Source Count Verification |
| SR-002-R2 | Major | Total source count discrepancy: L0 Key Numbers header states "75" but Tier Analysis section states "Total: 74 sources" — the body of the Tier Analysis section states "Tier 4 constitutes 58.1%" of 74 sources while the L0 now states 75; this creates a secondary internal inconsistency introduced by the R2 addition of A-31 | L0: Key Numbers vs. L1: Evidence Tier Analysis |
| SR-003-R2 | Minor | CONFLICT-4 resolution label: body states "UNRESOLVED" at the section heading but the clarification note below says "The UNRESOLVED label applies specifically to the natural-language self-refinement question" — this is clarifying but the headline label still says UNRESOLVED without the qualifier, potentially misleading scanners who read only headers | L1: Conflicts |
| SR-004-R2 | Minor | Phase 2 Experimental Design table lacks priority ordering for "Recommended" conditions (Cond-6, Cond-7) relative to each other — both are labeled "Recommended" with no relative priority signal | Phase 2 Experimental Design Requirements |
| SR-005-R2 | Minor | PS Integration key finding #4 references "minimum 5 conditions" (Cond-1 through Cond-5) but the Phase 2 Experimental Design Requirements section documents 7 conditions (Cond-1 through Cond-7) — a minor count mismatch between the handoff section and the design section | PS Integration vs. Phase 2 Experimental Design Requirements |

### Detailed Finding: SR-001-R2

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Source Count Verification |
| **Strategy Step** | Step 2 (Completeness check) |

**Evidence:** The Source Count Verification Group C arithmetic trace states: "Unique context7 sources not already counted in Groups A or I: C-6, C-7, C-8, C-9, C-10, C-11, C-13, C-19, C-20 = 9 documented unique new sources." It then states the 13-source count "includes: C-6, C-7, C-8, C-9, C-10, C-11, C-13, C-14, C-19, C-20, and 3 remaining from context7 References #1-3 that are distinct URL variants." This adds C-14 (not listed in the initial 9) and "3 remaining" that are not individually named. The discrepancy between 9 explicitly named + "4 additional" = 13 is not independently verifiable because the 4 additional sources are not identified by ID in the arithmetic trace.

**Analysis:** A reader attempting to reproduce the 75-source count cannot verify the Group C component of 13 from the arithmetic trace alone. The original SR-001 asked for an explicit arithmetic trace; R2 added one, but Group C remains opaque at the "4 additional" sub-count. The SR-001 finding is therefore only partially resolved.

**Recommendation:** Name all 13 Group C sources individually in the arithmetic trace: list each of the 13 context7-unique source IDs explicitly so a reader can count them independently.

### Detailed Finding: SR-002-R2

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L0: Key Numbers vs. L1: Evidence Tier Analysis |
| **Strategy Step** | Step 2 (Internal Consistency check) |

**Evidence:** L0 Key Numbers states "Total unique sources: **75**" with the note "31 academic (incl. A-31 added R2) + 31 industry-unique + 13 context7-unique." The L1: Evidence Tier Analysis section states: "**Total: 74 sources.** Tier 1 constitutes 17.6% of all sources. Tier 4 constitutes 58.1%." The Tier Analysis section counts 13 Tier 1 + 5 Tier 2 + 13 Tier 3 + 43 Tier 4 = 74, not 75. A-31 was added to Group A (Tier 3) in R2 but the Tier 3 count note in that section reads: "A-31 replaces one entry that was previously double-counted via I-13 (secondary citation)" — implying the total tier count should still be 74 (net zero change). But L0 explicitly says 75. This creates a new internal inconsistency introduced by R2.

**Analysis:** The Tier Analysis section counts 13 + 5 + 13 + 43 = 74. If A-31 is a new source (not replacing a prior count), the total should be 75 and the Tier Analysis should show 14 Tier 3 sources (12 original + A-31 + C-19, noting the original SR-005 Tier 3 count was 12, the note added 13 with C-19, and now A-31 would make 14 — but the R2 note claims 13 consistently by treating A-31 as replacing a double-count). This circular arithmetic is not transparent. A-31 is a genuinely new source (not previously in any catalog); I-13 remains as a separate industry source; there is no actual replacement. The total should be 75 and the Tier 3 count should be updated to 14.

**Recommendation:** Correct the Tier Analysis section to state "Total: 75 sources" and list Tier 3 as 14 sources (adding A-31). Remove the claim that A-31 "replaces" I-13 — they are distinct documents.

---

### Scoring Impact (S-010)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | Prior completeness gaps largely resolved; SR-001-R2 introduces minor verification gap |
| Internal Consistency | 0.20 | Negative | SR-002-R2: new inconsistency between L0 total (75) and Tier Analysis total (74) introduced by R2 |
| Methodological Rigor | 0.20 | Neutral | No new methodological concerns introduced |
| Evidence Quality | 0.15 | Neutral | No new evidence quality issues introduced |
| Actionability | 0.15 | Positive | Phase 2 design section added; SR-004-R2 minor ordering gap |
| Traceability | 0.10 | Negative | SR-001-R2: Group C 4 unidentified sources reduce traceability |

**Decision:** Proceed to S-003. Two new Major findings (SR-001-R2, SR-002-R2) require resolution. No Critical findings. Net improvement from R1 despite new issues.

---

## S-003: Steelman Findings

**Strategy:** S-003 Steelman Technique
**Finding Prefix:** SM
**Protocol Steps Completed:** 6 of 6
**H-16 Verification:** Executing before S-002. SATISFIED.
**Core Thesis (R2):** "Across 75 unique sources, the PROJ-014 working hypothesis is untested (null finding, not refuted); structured alternatives outperform blunt prohibition; the critical gap is controlled A/B experimentation; Phase 2 design is specified with 7 conditions."

**Prior SM findings addressed:**
- SM-001 (Major): Access-level column — RESOLVED (AGREE-5 now includes full access-level annotation column)
- SM-002 (Major): AGREE-4 restructured — RESOLVED (A-20 and A-19 now lead; A-16 demoted to "corroborating caveat")
- SM-003 (Major): Phase 2 design section — RESOLVED (dedicated "Phase 2 Experimental Design Requirements" section added)
- SM-004 (Minor): THEME-1 testable prediction — RESOLVED (explicit testable prediction added)
- SM-005 (Minor): Best Case Scenario — present in S-003 body in I1 but not explicitly in synthesis; the revised PS Integration and the AGREE-5 actionability note partially address this
- SM-006 (Minor): CONFLICT-2 explanations ranked by testability — RESOLVED (testability ranking explicitly added)

### New Findings

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| SM-001-R2 | Major | Phase 2 Experimental Design table provides "Required/Recommended" priority labels but no relative priority among the two "Recommended" conditions (Cond-6, Cond-7) — a practitioner deciding which to implement first has no guidance | Phase 2 Experimental Design Requirements |
| SM-002-R2 | Minor | The AGREE-5 effectiveness hierarchy (access-level annotated) is the synthesis's most actionable structured output, but the hierarchy does not state what evidence the rank ordering is based on — for rows 6-12 where evidence is "Qualitative improvement / No controlled measurement," the ranking itself becomes synthesis judgment not traceable to any source | L1: AGREE-5 effectiveness hierarchy |
| SM-003-R2 | Minor | The "Best Case Scenario" (SM-005 from I1) is still absent from the synthesis body — the steelman in I1 recommended adding an explicit articulation of when the synthesis is most compelling; this is present in the S-003 strategy output in I1 but was not incorporated into the synthesis document itself | General / L0 |

### Detailed Finding: SM-001-R2

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Phase 2 Experimental Design Requirements |
| **Strategy Step** | Step 3 (Strengthening recommendations) |

**Evidence:** The Phase 2 Experimental Design Requirements section provides conditions Cond-1 through Cond-7 with a Priority column showing: Cond-1 through Cond-5 = "Required"; Cond-6 (Declarative behavioral negation) = "Recommended"; Cond-7 (Atomic decomposition) = "Recommended." Both recommended conditions have identical priority labels with no further ordering signal. The evidence tiers are: Cond-6 = "Tier 4 (vendor practice) — synthesis hypothesis"; Cond-7 = "Tier 1 (A-15) — DeCRIM single study." Cond-7 has stronger empirical backing (Tier 1, EMNLP 2024) than Cond-6 (Tier 4, synthesis hypothesis), but this advantage is not reflected in any priority signal.

**Analysis:** In the steelman's strongest form, the synthesis should guide practitioners to prioritize Cond-7 (Atomic decomposition, Tier 1 evidence) over Cond-6 (Declarative behavioral negation, synthesis hypothesis) when resource-constrained. The current equal "Recommended" labeling loses this signal. A practitioner implementing only one additional condition should implement Cond-7.

**Recommendation:** Add a sub-priority within "Recommended": "Recommended-A" (Cond-7, stronger evidence) and "Recommended-B" (Cond-6, hypothesis testing), or add a note: "If only one Recommended condition can be implemented, prioritize Cond-7 (Tier 1 academic evidence) over Cond-6 (synthesis-generated hypothesis requiring validation)."

---

## S-002: Devil's Advocate Findings

**Strategy:** S-002 Devil's Advocate
**Finding Prefix:** DA
**Protocol Steps Completed:** 5 of 5
**H-16 Verification:** S-003 executed prior. SATISFIED.

**Prior DA findings addressed:**
- DA-001 (Critical): Conflation resolved — RESOLVED (see Prior Finding Resolution Status)
- DA-002 (Major/Critical): Agreement count corrected — RESOLVED
- DA-003 (Major): Null finding framing — RESOLVED (explicit "not refuted" language added; Phase 2 mandate statement added)
- DA-004 (Major): Revised hypothesis labeled as alternative — RESOLVED (labeled "Alternative Hypothesis" with explicit statement it should not replace the original for Phase 2)
- DA-005 (Major): Vendor consensus reframed — RESOLVED ("broadest operational consensus" language used; explicit statement that Tier 1 academic evidence provides stronger experimental grounds)
- DA-006 (Minor): THEME-3 speculation — RESOLVED (explicitly labeled as "synthesis-generated inference")
- DA-007 (Minor): CONFLICT-2 resolution — RESOLVED (testability ranking added)

### New Findings

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| DA-001-R2 | Major | AGREE-3 (Vendor Best Practice) is described with HIGH confidence for vendor recommendation but the caveat "recommendation reflects the balance of evidence across 2023-2026 sources" is appended without examining whether the vendor consensus itself may be systematically biased — the Known Scope Exclusions SE-3 acknowledges internal vendor benchmarks may differ but AGREE-3 does not cross-reference this limitation | L1: AGREE-3 |
| DA-002-R2 | Major | The Alternative Hypothesis added in R2 is labeled correctly as alternative, but it appears in the L0 Executive Summary before Phase 2 Mandate — a reader scanning L0 will encounter the alternative hypothesis early and may unconsciously anchor to it as the synthesis's preferred outcome for Phase 2, defeating its stated purpose as a "secondary outcome of interest" | L0: Executive Summary |
| DA-003-R2 | Minor | The epistemic distinction note (DA-001/RT-001 fix) correctly distinguishes null finding from refutation, but then the same paragraph concludes: "No source confirms the claim; no source refutes it with controlled data" — the phrase "no source refutes it" appears as a defensive hedge that could be read as implying negative prompting has been absolved, which is also not the correct inference | L0: Executive Summary |
| DA-004-R2 | Minor | AGREE-5 effectiveness hierarchy rank 1 (CAST model-internal interventions) and rank 2 (Constitutional AI training-time) are presented as if they are alternatives to prompt engineering, but a reader might misread the hierarchy as implying these techniques are "better" in a comparable way — the table header "Access Level: Model-access required / Training-access required" is present but could be more explicitly flagged as "OUTSIDE PROJ-014 scope" | L1: AGREE-5 |

### Detailed Finding: DA-001-R2

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L1: AGREE-3 |
| **Strategy Step** | Step 3 (Assumption probing) |

**Evidence:** AGREE-3 states: "This recommendation applies to the current model generation. OpenAI's GPT-4.1 and GPT-5 guides document that newer models follow negative instructions more literally, suggesting the gap between negative and positive framing effectiveness may be narrowing in frontier models." It then adds: "See Known Scope Exclusions SE-1 and SE-3: this vendor recommendation may be supported by unpublished internal experimentation not captured in this synthesis." However, AGREE-3 does not probe the more adversarial implication of SE-3: vendors may recommend positive framing because it favors their model's behavior profile (product positioning) rather than because it is objectively better. This is the IN-003 finding from I1 which was marked "partially addressed" in Known Scope Exclusions SE-3.

**Analysis:** SE-3 states: "Their published guidance ('prefer positive framing') may reflect internal experimental findings not released publicly." This is a charitable interpretation. The adversarial reading — that positive framing recommendations may be motivated by the fact that vendor models are fine-tuned to respond well to positive framing (circular optimization) — is not explicitly considered. AGREE-3 should acknowledge this alternative interpretation alongside the neutral SE-3 interpretation.

**Recommendation:** Add to AGREE-3: "Caveat on vendor neutrality: vendor recommendations for positive framing should be interpreted with the awareness that vendor models are optimized against their own test suites and prompting guidance. The recommendation 'use positive framing' may partially reflect these models being better-tuned to positive framing rather than a general property of all LLMs."

### Detailed Finding: DA-002-R2

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L0: Executive Summary |
| **Strategy Step** | Step 2 (Assumption identification) |

**Evidence:** The L0 Executive Summary paragraph sequence is: (1) "In three sentences: ...no source validates..."; (2) "Key numbers" table; (3) "Verdict on the PROJ-014 hypothesis" (null finding framing); (4) "Important epistemic distinction (DA-001/RT-001 fix)"; (5) "**On the revised hypothesis:** The synthesis process suggests an alternative hypothesis for further investigation: 'Specific, contextually justified constraints... reduce hallucination more effectively than standalone prohibition instructions.' This is explicitly labeled an **alternative hypothesis** generated from synthesis findings."; (6) "**Phase 2 mandate:**...".

The alternative hypothesis placement — between the epistemic distinction clarification and the Phase 2 mandate — positions it as a synthesis conclusion adjacent to the primary hypothesis verdict. Despite the "alternative hypothesis" label, a non-careful reader will encode: "the synthesis found that complex mixed constraints work better." This is the DAI-004 concern from I1 at the framing level — the fix correctly labeled the hypothesis but may have insufficiently de-emphasized it.

**Recommendation:** Move the "On the revised hypothesis" paragraph to the end of L0 (after Phase 2 mandate) or to a dedicated section ("Research Directions for Phase 2") to prevent anchoring effects. The Phase 2 mandate paragraph should immediately follow the epistemic distinction.

---

## S-004: Pre-Mortem Findings

**Strategy:** S-004 Pre-Mortem Analysis
**Finding Prefix:** PM
**Protocol Steps Completed:** 5 of 5

**Prior PM findings addressed:**
- PM-001 (Major): Phase 2 design section consolidated — RESOLVED (dedicated section added)
- PM-002 (Major): Agreement count corrected — RESOLVED
- PM-003 (Major): GAP-5 "DO NOT CITE" caveat added — RESOLVED (box added in GAP-5 body)
- PM-004 (Major): Null finding vs. directional framing — RESOLVED (DA-001/RT-001 fix applied)
- PM-005 (Minor): Deduplication non-reproducibility — PARTIALLY RESOLVED (arithmetic trace added but Group C 4 unidentified sources persist per SR-001-R2)
- PM-006 (Minor): THEME-1 as CONFLICT-2 repackaging — PARTIALLY ADDRESSED (THEME-1 explicitly labeled as "synthesis-generated mechanistic hypothesis"; testable prediction added)

### New Findings

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| PM-001-R2 | Major | New pre-mortem scenario: a Phase 2 analyst reads the Phase 2 Experimental Design Requirements section and implements only Cond-1 through Cond-5 (all labeled "Required") while skipping Cond-6 and Cond-7 (labeled "Recommended") — this is correct per the table labeling, but Cond-7 (Atomic decomposition, Tier 1 DeCRIM evidence) has stronger empirical justification than several of the Required conditions, which are grounded in vendor consensus (Tier 4). The labeling implies Required > Recommended when the evidence hierarchy suggests the opposite for Cond-7 specifically. | Phase 2 Experimental Design Requirements |
| PM-002-R2 | Minor | The new SR-002-R2 inconsistency (L0 says 75 total, Tier Analysis says 74) could propagate: a practitioner citing this synthesis may report "75 unique sources" (from L0) while a peer reviewer auditing the Tier Analysis finds "74" and raises a challenge. This is a reputational risk for the synthesis. | L0 Key Numbers vs. L1: Evidence Tier Analysis |
| PM-003-R2 | Minor | The "DO NOT CITE WITHOUT VERIFICATION" box in GAP-5 (instruction compliance decay figures) is placed mid-section, after the claim is fully stated. A reader who stops reading before the box will have absorbed the unverified figures without seeing the caveat. The caveat should precede or accompany the claim, not follow it. | L1: Gaps, GAP-5 |

### Detailed Finding: PM-001-R2

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Phase 2 Experimental Design Requirements |
| **Strategy Step** | Step 3 (Failure mode identification) |

**Evidence:** Phase 2 Experimental Design Requirements conditions table:
- Cond-5 (Warning-based meta-prompt): Priority = "Required"; Evidence = "Tier 1 (A-23) — single study, needs replication"
- Cond-7 (Atomic decomposition): Priority = "Recommended"; Evidence = "Tier 1 (A-15)"

A-15 (DeCRIM, EMNLP 2024) is a Tier 1 paper with replication across two benchmarks (RealInstruct: +7.3%; IFEval: +8.0%). A-23 (Barreto & Jana, EMNLP 2025) is also Tier 1 but explicitly noted as "single study, needs replication." Both are Tier 1. Cond-5 is "Required" and Cond-7 is "Recommended" — yet Cond-5's evidence is described as needing replication while Cond-7's is not. The priority labeling logic (Required vs. Recommended) appears to follow the hypothesis test order rather than evidence strength, which is defensible, but the result is that a well-evidenced technique (Cond-7) could be skipped in favor of a less-replicated one (Cond-5) simply due to the label.

**Recommendation:** Add a footnote to Cond-7: "Note: DeCRIM evidence (A-15, Tier 1, two benchmarks) is more robustly replicated than Cond-5 (A-23, single study). Cond-7 is 'Recommended' rather than 'Required' because it addresses a secondary research question (decomposition strategy) vs. the primary framing question. Resource-constrained designs should implement Cond-7 before Cond-6."

---

## S-001: Red Team Findings

**Strategy:** S-001 Red Team Analysis
**Finding Prefix:** RT
**Protocol Steps Completed:** 5 of 5

**Prior RT findings addressed:**
- RT-001 (Critical): Conclusion overreach — RESOLVED (epistemic distinction note added, directional language removed from L0)
- RT-002 (Major): A-6 percentages in L0 — RESOLVED (26%→59% figures removed from L0; directional language only)
- RT-003 (Major): Selection bias in survey scope — PARTIALLY RESOLVED (Known Scope Exclusions addresses three exclusion domains but does not specifically address publication bias — the academic tendency to publish failure cases over success cases in AI prompting)
- RT-004 (Major): Circular citation chain in AGREE-4 — PARTIALLY RESOLVED (A-20 and A-19 now lead; AGREE-4 note on circular citation risk added in body text; chain traces beyond A-9 acknowledged)
- RT-005 (Minor): Scope conflation — RESOLVED (THEME-2 explicitly notes "Findings from one phenomenon do not automatically generalize to others")
- RT-006 (Minor): Causal claim without causal evidence in THEME-1 — RESOLVED (explicitly labeled "synthesis-generated mechanistic hypothesis" with no confirmatory evidence cited)
- RT-007 (Minor): Recency bias unaddressed — PARTIALLY RESOLVED (THEME-3 now explicitly flags model-generation confound and cautions against pre-2024 findings)

### New Findings

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| RT-001-R2 | Major | Known Scope Exclusions addresses production deployments, domain-specific applications, vendor internal benchmarks, and grey literature — but does NOT address publication bias (the tendency of academic journals to publish negative or null results vs. positive results for LLM prompting techniques). This is distinct from SE-4 (grey literature). Publication bias specifically affects the academic survey component and is a standard systematic review limitation not yet acknowledged | Known Scope Exclusions / L1: Methodological Rigor |
| RT-002-R2 | Major | AGREE-5 effectiveness hierarchy still contains CAST (A-28, model-internal steering) and Constitutional AI (A-10, training-time) as ranks 1-2 of the hierarchy. These are presented as "better techniques" than prompt engineering, but the comparison is not apples-to-apples: model-internal and training-time methods have fundamentally different access requirements, cost structures, and use cases. A reader could extract "CAST is better than warning-based meta-prompts" as an attack surface, even though they operate at different abstraction levels. The "Access Level" column partially addresses this but does not prevent the misleading comparison | L1: AGREE-5 effectiveness hierarchy |
| RT-003-R2 | Minor | The AGREE-4 circular citation note reads: "the academic base for this agreement is broader than the industry citation network implies, resting on multiple independent academic sources (A-20, A-19, A-31)." A-31 (Bsharat et al.) is cited here as an independent source, but it is an arXiv preprint (Tier 3) that has not been peer-reviewed — its independence from the practitioner network is assumed but not verified. Including an unreviewed preprint as evidence of "academic base breadth" is potentially circular | L1: AGREE-4 |
| RT-004-R2 | Minor | CONFLICT-2 resolution explanation (4) states: "pragmatic recognition that some constraints are most clearly expressed as prohibitions." This is described as "least testable" — but it is actually the explanation most directly relevant to PROJ-014's working hypothesis (that certain negative framings may be appropriate). Making it the "least testable" explanation de-emphasizes the most hypothesis-relevant alternative | L1: CONFLICT-2 |

### Detailed Finding: RT-001-R2

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Known Scope Exclusions / Methodological Rigor |
| **Strategy Step** | Step 4 (Systemic vulnerability) |

**Evidence:** The Known Scope Exclusions section (SE-1 through SE-4) addresses deployment gaps, domain-specific expert applications, internal vendor benchmarks, and grey literature from practitioner communities. Publication bias — the systematic tendency of academic journals to publish papers that find problems with AI systems (null or negative results for capability claims) over papers that find success — is not addressed. The academic survey searched academic databases and found evidence predominantly of negative constraint failure. If studies showing successful negative prompting were submitted to academic venues but not accepted due to publication bias, they would be systematically absent from the academic survey.

**Analysis:** Publication bias is a standard limitation in systematic reviews. The Cochrane Handbook and PRISMA guidelines mandate acknowledgment of publication bias in systematic reviews. The Braun & Clarke (2006) thematic analysis methodology invoked by the synthesis does not inherently require this, but for a synthesis with research implications, the omission is a methodological gap. The Known Scope Exclusions SE-4 addresses grey literature not indexed by academic search, which is related but not the same phenomenon.

**Recommendation:** Add SE-5 to Known Scope Exclusions: "SE-5: Publication Bias in Academic Venue Indexing. Academic search preferentially indexes published results. Studies demonstrating effective negative prompting techniques may have been conducted and submitted to academic venues but not accepted. The 'file drawer problem' (unpublished null results or positive results that contradict reviewer expectations) may affect the academic survey component's representation of the field. This synthesis cannot quantify the extent of this bias."

### Detailed Finding: RT-002-R2

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L1: AGREE-5 effectiveness hierarchy |
| **Strategy Step** | Step 3 (Evidence vulnerability) |

**Evidence:** AGREE-5 presents an "effectiveness hierarchy" with CAST model-internal steering (~90% harmful refusal) at rank 1 and Constitutional AI training-time constraints at rank 2. Both are explicitly marked "Not achievable via prompt engineering" / "Inference-time only for PROJ-014 scope." However, the table's framing — presenting these as the top-ranked techniques — creates a misleading comparative context. The hierarchy implies a spectrum where prompt engineering techniques are at the bottom, but CAST and Constitutional AI are not alternatives to prompt engineering; they operate at entirely different system layers with different prerequisites, costs, and applicability domains.

**Analysis:** A researcher reading the synthesis could construct: "The synthesis shows that even the best prompt engineering techniques (+25.14% distractor negation accuracy from warning-based meta-prompts) are far below the effectiveness of CAST (90.67%) or training-time methods — prompt engineering is an inherently weak approach." This attack could be used to argue PROJ-014 is pursuing a research direction with limited potential. The "Access Level" column mitigates but does not eliminate this risk because a skimmer will see the rank ordering before the column values.

**Recommendation:** Add an explicit header note to the AGREE-5 table: "**Note: Ranks 1-4 are not alternatives to prompt engineering; they operate at different system layers (model-internal or training-time). Ranks 5-12 represent the prompt-engineering-accessible space. The ranking within the prompt-accessible range (5-12) is the primary comparison relevant to PROJ-014.**"

---

## S-007: Constitutional AI Findings

**Strategy:** S-007 Constitutional AI Critique
**Finding Prefix:** CC
**Protocol Steps Completed:** 4 of 4

**Prior CC findings addressed:**
- CC-001 (Major): P-001 accuracy — RESOLVED (directional language replaced with null-finding language)
- CC-002 (Major): P-022 deception — RESOLVED (agreement count corrected to match body)
- CC-003 (Minor): H-23 navigation table — SATISFIED (remains present)
- CC-004 (Minor): P-011 evidence-based — RESOLVED (THEME-1 mechanistic claim explicitly labeled as synthesis-generated hypothesis)

### Constitutional Compliance Review

| Principle | Assessment | Finding |
|-----------|------------|---------|
| P-001 (Truth/Accuracy) | PASS | Null finding language now correct; no overclaiming on Tier 3 evidence in L0 |
| P-003 (No Recursion) | PASS | Standalone document; no subagent delegation |
| P-004 (Provenance) | PARTIAL | SR-001-R2: 4 unidentified Group C sources reduce provenance for source count; all major claims retain source attribution |
| P-011 (Evidence-Based) | PARTIAL | THEME-3 speculative inference appropriately labeled; minor residue in AGREE-3 vendor bias omission (DA-001-R2) |
| P-020 (User Authority) | PASS | Research recommendations are suggestions; Phase 2 decisions correctly deferred to researchers |
| P-022 (No Deception) | PARTIAL | SR-002-R2: new L0 (75) vs. Tier Analysis (74) count inconsistency introduced in R2; unintentional but detectable |

### New Findings

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| CC-001-R2 | Major | P-022 compliance — SR-002-R2: the new total count discrepancy (L0: 75 vs. Tier Analysis: 74) constitutes a minor P-022 issue: a reader relying on L0 (75) will have a different source count than a reader auditing the Tier Analysis (74). The inconsistency is unintentional (introduced by R2's A-31 addition) but is a factual discrepancy that must be corrected | L0: Key Numbers vs. L1: Evidence Tier Analysis |
| CC-002-R2 | Minor | P-011 residue: THEME-3 extrapolation about GPT-5.2 behavior is appropriately labeled as "synthesis-generated inference" but the inference's basis — that models following negative instructions "too literally" would produce "confidently wrong output" — still lacks a cited source for the mechanism. The caveat is present but the underlying claim retains a speculative causal step | L2: THEME-3 |

---

## S-011: Chain-of-Verification Findings

**Strategy:** S-011 Chain-of-Verification
**Finding Prefix:** CV
**Protocol Steps Completed:** 5 of 5

**Prior CV findings addressed:**
- CV-001 (Major): Bsharat et al. as primary source — RESOLVED (A-31 added to catalog; I-13 noted as secondary)
- CV-002 (Major): DSPy Assertions evidence tier — RESOLVED (C-13 now explicitly described as "Tier 3 arXiv preprint; no confirmed peer-reviewed venue identified as of 2026-02-27")
- CV-003 (Major): Phase 2 5-conditions derivation — RESOLVED (Phase 2 Experimental Design Requirements section with explicit derivation traces added)
- CV-004 (Minor): A-16 rejection prominence — RESOLVED (A-16 marked "**REJECTED PAPER — peer review identified concerns**" in the source catalog; AGREE-4 relegates it to corroborating caveat)
- CV-005 (Minor): CONFLICT-4 A-21 run count — noted but not materially improved; the Group A catalog entry for A-21 still reads "Single 8B model, 3 runs — low statistical confidence" (sufficient)

### Verification Questions (New in R2)

| Claim | Verification Question | Source | Verified? | Finding |
|-------|----------------------|--------|-----------|---------|
| "75 unique sources" | Does 31 + 31 + 13 = 75? | Source Count Verification, arithmetic trace | PARTIAL | SR-002-R2: Tier Analysis says 74; arithmetic 31+31+13=75 is internally consistent but Tier Analysis not updated |
| "Group C = 13 sources" | Are all 13 Group C sources named? | Source Count Verification, Group C trace | PARTIAL | SR-001-R2: 9 named + "4 additional" not enumerated |
| "Cond-1 through Cond-7 derivations" | Can each condition be traced to a specific synthesis finding? | Phase 2 Experimental Design Requirements | VERIFIED | Cond-1 through Cond-5 have explicit derivation traces; Cond-6 and Cond-7 trace to THEME-1 and GAP-3 respectively |
| "DA-001/RT-001 fix applied" | Does L0 no longer contain conflated null/directional claims? | L0: Executive Summary | VERIFIED | Epistemic distinction note present; directional percentages removed |
| "A-31 added as Tier 3 primary source" | Is A-31 identified with full bibliographic data and tier classification? | Group A catalog | VERIFIED | A-31 listed with arXiv:2312.16171, Tier 3, Revision 2 note |
| "AGREE-5 access-level annotations" | Does each hierarchy entry have an Access Level designation? | AGREE-5 table | VERIFIED | Access Level column present in all 12 rows |

### New Findings

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| CV-001-R2 | Major | The 4 unidentified Group C sources prevent independent verification of the 75-source total — a reader conducting a peer review cannot reproduce the source catalog from the document alone (SR-001-R2 elaborated) | Source Count Verification |
| CV-002-R2 | Minor | Cond-6 (Declarative behavioral negation) derivation is traced to "THEME-1: synthesis-generated hypothesis (vendor practice pattern; testability noted)" — this is a derivation from a synthesis-generated hypothesis, not from a documented source finding. The derivation chain "source → finding → condition" is broken for Cond-6 because THEME-1 is itself synthesis output, not source evidence | Phase 2 Experimental Design Requirements |
| CV-003-R2 | Minor | The Revision Log in R2 lists "RT-004 (circular citation chain)" as not explicitly addressed in the revision changes — the AGREE-4 circular citation note was present in R1 (the synthesis already contained it per the I1 tournament) and was not changed in R2. However RT-004 was a Major finding in I1; the revision log should explicitly state whether RT-004 was addressed or deferred | Revision Log |

### Detailed Finding: CV-001-R2

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Source Count Verification |
| **Strategy Step** | Step 3 (Source traceability) |

**Evidence:** The Group C arithmetic trace states: "Unique context7 sources not already counted in Groups A or I: C-6, C-7, C-8, C-9, C-10, C-11, C-13, C-19, C-20 = 9 documented unique new sources." Then: "The 13-source count in the header includes: C-6, C-7, C-8, C-9, C-10, C-11, C-13, C-14, C-19, C-20, and 3 remaining from context7 References #1-3 that are distinct URL variants counted separately from I-1/I-3/I-2." This names 10 sources explicitly (C-6 through C-20 list now adds C-14) plus "3 remaining from context7 References #1-3." The "3 remaining" are not identified. The sum 10 + 3 = 13 is arithmetically consistent but the 3 remaining cannot be independently identified.

**Recommendation:** Name all 13 Group C sources with their IDs. If "3 remaining from context7 References #1-3" are distinct URL variants of sources already counted in other groups, they should not be in Group C at all — they should be listed as deduplication decisions. If they are genuinely distinct sources, they need IDs and catalog entries.

---

## S-012: FMEA Findings

**Strategy:** S-012 FMEA
**Finding Prefix:** FM
**Protocol Steps Completed:** 5 of 5

**Prior FM findings addressed (by R2 changes):**
- FM-001 (Major): Agreement count error — RESOLVED (count corrected; RPN drops significantly)
- FM-002 (Major): Null finding conflation — RESOLVED (epistemic distinction note added)
- FM-003 (Major): Unverified Tier 4 claims not blocked — PARTIALLY RESOLVED (DO NOT CITE boxes added for GAP-5, GAP-7; Latitude I-22 cross-reference added)
- FM-004 (Medium): A-6 hallucination figures generalized — RESOLVED (removed from L0)
- FM-005 (Medium): Phase 2 conditions not traceable — RESOLVED (Phase 2 Design Requirements section added)
- FM-006 (Medium): Source count non-reproducible — PARTIALLY RESOLVED (arithmetic trace added but Group C 4 unidentified sources remain)
- FM-007 (Low-Medium): A-16 rejection notice — RESOLVED (REJECTED PAPER label added prominently)
- FM-008 (Low-Medium): Model-generation boundary not enforced — RESOLVED (Phase 2 Design Constraints explicitly state "Use post-2024 frontier models only")
- FM-009 (Low-Medium): Survey scope limitations — RESOLVED (Known Scope Exclusions section added)

### Updated FMEA Risk Table (R2)

RPN = Severity (1-10) × Occurrence (1-10) × Detectability (1-10)

| ID | Failure Mode | Component | Sev | Occ | Det | RPN | Status |
|----|-------------|-----------|-----|-----|-----|-----|--------|
| FM-001 | Agreement count error propagates to downstream citations | L0 Key Numbers | 8 | 2 | 3 | 48 | RESOLVED — RPN reduced from 448 |
| FM-002 | Null finding misread as directional | L0 Executive Summary | 9 | 3 | 4 | 108 | SUBSTANTIALLY REDUCED — from 378; epistemic note mitigates |
| FM-003 | Unverified Tier 4 figures cited as fact | L1: Gaps | 7 | 4 | 5 | 140 | PARTIALLY REDUCED — DO NOT CITE boxes added |
| FM-010 | Source count inconsistency (75 vs. 74) propagates | L0/Tier Analysis | 6 | 6 | 6 | 216 | NEW HIGH-RPN RISK introduced by R2 |
| FM-011 | Group C 4 unidentified sources prevent audit reproducibility | Source Count Verification | 5 | 5 | 8 | 200 | NEW MEDIUM-HIGH RPN introduced by R2 |
| FM-012 | Cond-7 "Recommended" label causes omission despite strong evidence | Phase 2 Design Requirements | 7 | 5 | 6 | 210 | NEW MEDIUM-HIGH RPN |
| FM-013 | Alternative hypothesis anchoring causes Phase 2 bias | L0: Executive Summary | 6 | 4 | 6 | 144 | NEW MEDIUM RPN (DA-002-R2) |
| FM-004 | A-6 hallucination figures generalized | AGREE-6 | 8 | 2 | 3 | 48 | RESOLVED — RPN reduced from 200 |
| FM-005 | Phase 2 experimental design diverges from synthesis | PS Integration | 7 | 3 | 5 | 105 | SUBSTANTIALLY REDUCED — Phase 2 section added |
| FM-006 | Deduplication verification fails | Source Count | 6 | 4 | 6 | 144 | PARTIALLY REDUCED — Group C still ambiguous |

### New High-RPN Finding: FM-010

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L0 Key Numbers vs. L1: Evidence Tier Analysis |
| **RPN** | 216 |

**Evidence:** FM-010 reflects the new inconsistency introduced by R2: L0 says 75 total sources; the Tier Analysis section says 74. This is not a pre-existing problem — it was introduced by the R2 addition of A-31. The occurrence is high (6/10) because both sections will be read by practitioners conducting reviews, and the detectability is moderate (6/10) because a careful reader will catch it during a cross-section audit.

**Recommendation:** Correct the Tier Analysis total to 75 and update the Tier 3 count from 13 to 14 (adding A-31). Remove the confusing note about A-31 "replacing" a double-count from I-13 — A-31 and I-13 are distinct documents, both present in the catalog.

---

## S-013: Inversion Findings

**Strategy:** S-013 Inversion Technique
**Finding Prefix:** IN
**Protocol Steps Completed:** 5 of 5

**Prior IN findings addressed:**
- IN-001 (Critical): Core conclusion fails domain-specific inversion — RESOLVED (Known Scope Exclusions section added)
- IN-002 (Major): A-23 single-study replication caveat — RESOLVED (replication caveat explicitly added to GAP-2 and AGREE-5)
- IN-003 (Major): Vendor bias not addressed — PARTIALLY RESOLVED (SE-3 acknowledges internal vendor benchmarks but does not probe vendor product positioning bias; DA-001-R2 identifies residual gap)
- IN-004 (Minor): AGREE-4 expert user inversion — PARTIALLY ADDRESSED (AGREE-4 notes aggregate failure but expert user control not explicitly discussed)
- IN-005 (Minor): Structural enforcement vs. linguistic framing — RESOLVED (THEME-5 explicitly addresses the distinction; "Important caveat" added)

### Inversion Test (R2)

| Major Finding | Inverted Assumption | Survivability |
|---------------|---------------------|---------------|
| "No evidence supports 60% claim" | What if 60% IS well-supported in domain-specific production contexts not captured by surveys? | SURVIVES — Known Scope Exclusions explicitly acknowledges this; null finding correctly bounded to public evidence |
| "Prohibition-style instructions are unreliable" | What if prohibition works reliably for expert prompt engineers? | PARTIALLY FAILS — synthesis notes aggregate failure rates; AGREE-4 does not control for user expertise |
| "Structured alternatives outperform blunt prohibition" | What if structural enforcement works for different mechanistic reasons, making linguistic framing comparison irrelevant? | SURVIVES — THEME-5 explicitly addresses this |
| "Warning-based meta-prompts are most actionable" | What if A-23 results don't replicate? | SURVIVES — replication caveat explicitly added; Phase 2 design includes validation |
| "Phase 2 should test 7 conditions" | What if the 7 conditions are not the right ones? | PARTIALLY FAILS — Cond-6 is a synthesis-generated hypothesis with Tier 4 evidence; its inclusion as an experimental condition may privilege an unsubstantiated synthesis claim |

### New Findings

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| IN-001-R2 | Major | The inclusion of Cond-6 (Declarative behavioral negation) as a "Recommended" Phase 2 experimental condition amplifies a synthesis-generated hypothesis into experimental design. If Phase 2 tests Cond-6 and finds no effect, researchers may incorrectly conclude the synthesis was wrong, when in fact Cond-6 was never supported by primary evidence — the synthesis generated it as a pattern from THEME-1. The inversion "What if Cond-6 tests a synthesis artifact rather than a real phenomenon?" survives and reveals a methodological risk | Phase 2 Experimental Design Requirements |
| IN-002-R2 | Minor | The vendor bias inversion (IN-003 from I1) is still only partially addressed. SE-3 ("Internal Vendor Benchmarks") acknowledges that vendor guidance may reflect unpublished internal experiments, but does not address the circular optimization concern: vendor models are fine-tuned against their own prompting guidance, which could make the recommendation for positive framing self-referentially optimal for those specific models but not universally optimal | Known Scope Exclusions SE-3 |

### Detailed Finding: IN-001-R2

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Phase 2 Experimental Design Requirements |
| **Strategy Step** | Step 3 (Robustness testing under inversion) |

**Evidence:** Cond-6 "Declarative behavioral negation" is derived from THEME-1: "synthesis-generated hypothesis (vendor practice pattern; testability noted)" with Tier 4 evidence. The inversion: "What if declarative behavioral negation is a pattern the synthesizer imposed on the data rather than a genuine finding from the sources?" survives the test — THEME-1 is explicitly described as not supported by direct interpretability evidence (THEME-1 note: "No source provides direct interpretability evidence for this mechanism"). Placing Cond-6 in Phase 2 experimental design as a "Recommended" condition elevates a synthesis artifact to the status of a hypothesis worth testing, which is arguably appropriate (synthesis suggests hypotheses), but the source weakness should be more explicitly flagged in the condition entry.

**Analysis:** Cond-6's derivation entry in the Phase 2 table reads: "THEME-1: synthesis-generated hypothesis (vendor practice pattern; testability noted)." This is accurate but understates the epistemological status: this is not a hypothesis derived from evidence — it is a pattern noticed during cross-survey comparison that received no empirical validation from any of the 75 sources. It should be labeled as "hypothesis-generating, not hypothesis-confirming" to prevent Phase 2 from treating it as equivalent to the Required conditions.

**Recommendation:** Add to Cond-6's derivation cell: "NOTE: This condition tests a synthesizer-generated hypothesis (not source-supported). Phase 2 testing is exploratory for this condition. Negative results should not be interpreted as invalidating the synthesis."

---

## S-014: LLM-as-Judge Scoring

**Strategy:** S-014 LLM-as-Judge
**Finding Prefix:** LJ
**Protocol Steps Completed:** 7 of 7

**Leniency bias counteraction applied:** All uncertain scores resolved downward per S-014 Step 2 protocol. C4 threshold is 0.95. Active anti-leniency applied throughout.

### Per-Dimension Scoring

#### Dimension 1: Completeness (weight: 0.20)

**Score: 0.91**

**Evidence for score:**
- All required sections present and improved from R1: Known Scope Exclusions added (IN-001 fix) — STRONG
- Phase 2 Experimental Design Requirements section added (SM-003/PM-001/CV-003 fix) — STRONG
- Agreement count corrected and verified (DA-002/CC-002 fix) — STRONG
- 75-source catalog with arithmetic trace — ADEQUATE (Group C 4 unidentified sources reduce to MODERATE)
- Per-agreement confidence qualifiers added throughout AGREE sections — STRONG
- Alternative hypothesis labeled and positioned (DA-004 fix) — ADEQUATE (placement risk per DA-002-R2)
- SR-001-R2: Group C arithmetic trace names only 9 of 13 sources explicitly — MODERATE GAP
- SR-002-R2: Tier Analysis section still states 74 sources while L0 states 75 — MINOR GAP (new in R2)
- SR-005-R2: PS Integration says "5 conditions" but Phase 2 section has 7 conditions — MINOR inconsistency
- Publication bias not acknowledged in Known Scope Exclusions (RT-001-R2) — MINOR GAP

**Justification for 0.91:** Substantial improvement from 0.82. All major completeness gaps from I1 are addressed. The new R2 issues (Group C partial enumeration, source count inconsistency) are genuine but minor relative to the structural completeness gains. Score reflects "near-complete with small residual arithmetic verification gaps."

---

#### Dimension 2: Internal Consistency (weight: 0.20)

**Score: 0.88**

**Evidence for score:**
- Critical I1 inconsistency resolved: L0 agreement count (7 STRONG) now matches body (5 STRONG) — STRONG IMPROVEMENT
- Directional overstatement in L0 ("evidence more consistently suggests the opposite") resolved — STRONG IMPROVEMENT
- SR-002-R2 new inconsistency: L0 total (75) vs. Tier Analysis total (74) — MODERATE DEGRADATION (new in R2)
- CONFLICT-4 "UNRESOLVED" label partially clarified but headline label still says UNRESOLVED without the qualifier — MINOR
- PS Integration "5 conditions" vs. Phase 2 Design "7 conditions" — MINOR
- DA-002-R2 alternative hypothesis placement creates potential anchoring inconsistency with "Phase 2 mandate" language — MINOR
- A-31 "replacing" language in Source Count Verification is internally inconsistent (A-31 is new, not replacing I-13) — MINOR

**Justification for 0.88:** Major improvement from 0.78. The critical L0 vs. body inconsistency is resolved. The new source count inconsistency (75 vs. 74) introduced by R2 is moderate but notable — it is the same type of issue (summary vs. body mismatch) as the original DA-002/CC-002. Score of 0.88 reflects "substantially consistent with one new moderate inconsistency and several minor issues."

---

#### Dimension 3: Methodological Rigor (weight: 0.20)

**Score: 0.90**

**Evidence for score:**
- Braun & Clarke (2006) methodology consistently applied — STRONG
- Per-agreement confidence qualifiers add methodological nuance — STRONG IMPROVEMENT
- Bias mitigation language present (cross-coder simulation, audit trail) — MODERATE
- Known Scope Exclusions section adds systematic limitations documentation — STRONG IMPROVEMENT
- Publication bias not explicitly acknowledged (RT-001-R2) — MODERATE GAP (specific gap in systematic review standards)
- A-16 rejection status now prominently flagged — MINOR IMPROVEMENT
- AGREE-4 restructured to lead with Tier 1/2 evidence — MINOR IMPROVEMENT
- Cond-6 in Phase 2 Design is a synthesis-generated hypothesis (IN-001-R2); including it without clearer epistemological labeling is a minor methodological concern — MINOR GAP
- SM-002-R2: effectiveness hierarchy ranks 6-12 lack stated evidence basis for the ranking itself — MINOR GAP

**Justification for 0.90:** Strong improvement from 0.87. Scope limitations are now documented. Evidence hierarchy is restructured correctly. Publication bias omission prevents reaching 0.93+. Score of 0.90 reflects "rigorous methodology with one specific systematic review standard gap."

---

#### Dimension 4: Evidence Quality (weight: 0.15)

**Score: 0.90**

**Evidence for score:**
- A-31 (Bsharat et al.) added as primary source for 55% figure (CV-001 fix) — STRONG IMPROVEMENT
- C-13 (DSPy) venue corrected to Tier 3 arXiv preprint (CV-002 fix) — STRONG IMPROVEMENT
- A-6 percentages removed from L0; directional language only (RT-002 fix) — STRONG IMPROVEMENT
- Vendor consensus reframed from "strongest" to "broadest operational consensus" (DA-005 fix) — STRONG IMPROVEMENT
- All major AGREE entries now lead with highest-tier evidence (SM-002 fix) — STRONG IMPROVEMENT
- Source tier table still counts total at 74 while L0 says 75 (SR-002-R2) — MINOR GAP (not a tier assignment error but an arithmetic gap)
- RT-002-R2: AGREE-5 effectiveness hierarchy mixing prompt-engineering-accessible and non-accessible techniques in a single ranked list remains a minor framing risk — MINOR
- RT-003-R2: A-31 described as part of "broader academic base" for AGREE-4 despite being Tier 3 unreviewed — MINOR
- Latitude figures (I-22) flagged in audit with cross-reference — MINOR IMPROVEMENT

**Justification for 0.90:** Strong improvement from 0.81. The primary evidence quality issues from I1 are all addressed. The residual issues are minor. Score of 0.90 reflects "high evidence quality with minor framing risks and a small arithmetic inconsistency."

---

#### Dimension 5: Actionability (weight: 0.15)

**Score: 0.93**

**Evidence for score:**
- Phase 2 Experimental Design Requirements section added — MAJOR IMPROVEMENT (addresses SM-003/PM-001/CV-003)
- 7 conditions with explicit derivation traces — STRONG
- Mandatory measurement dimensions specified with derivations — STRONG
- Design constraints table with "Post-2024 models only" constraint explicit — STRONG
- Access-level annotations in AGREE-5 distinguish prompt-only from infra-required techniques — STRONG
- SM-001-R2: No relative priority between Cond-6 and Cond-7 "Recommended" conditions — MINOR GAP
- PS Integration "5 conditions" vs. body "7 conditions" creates minor navigation friction — MINOR
- DA-002-R2: Alternative hypothesis placement may anchor Phase 2 analysts inappropriately — MINOR
- PM-001-R2: Cond-7 labeled "Recommended" despite stronger evidence than some "Required" conditions — MODERATE GAP

**Justification for 0.93:** Strong improvement from 0.84. The Phase 2 design section is the synthesis's most significant actionability improvement. Residual gaps are minor to moderate. Score of 0.93 reflects "highly actionable with minor priority signal issues."

---

#### Dimension 6: Traceability (weight: 0.10)

**Score: 0.90**

**Evidence for score:**
- A-31 added to catalog with primary citation (CV-001 fix) — STRONG
- Phase 2 conditions have explicit derivation traces (CV-003 fix) — STRONG IMPROVEMENT
- AGREE entries cite specific survey sections and quotes — STRONG (unchanged from R1)
- Deduplication decisions documented — STRONG (unchanged)
- SR-001-R2: Group C 4 sources unnamed in arithmetic trace — MODERATE GAP
- CV-002-R2: Cond-6 traces to synthesis-generated THEME-1, not to a primary source — MINOR GAP
- CV-003-R2: Revision Log does not explicitly address RT-004 (circular citation chain) — MINOR
- A-31 "replacing" I-13 claim is inaccurate but the actual source attribution is correct — MINOR

**Justification for 0.90:** Improvement from 0.86. The primary traceability gain is the explicit Phase 2 condition derivations. Group C 4 unidentified sources remain the primary traceability gap. Score of 0.90 reflects "strong traceability with one residual arithmetic verification gap."

---

### Weighted Composite Calculation

```
Composite = (Completeness × 0.20) + (Internal Consistency × 0.20) + (Methodological Rigor × 0.20)
          + (Evidence Quality × 0.15) + (Actionability × 0.15) + (Traceability × 0.10)

= (0.91 × 0.20) + (0.88 × 0.20) + (0.90 × 0.20) + (0.90 × 0.15) + (0.93 × 0.15) + (0.90 × 0.10)

= 0.182 + 0.176 + 0.180 + 0.135 + 0.1395 + 0.090

= 0.9025

≈ 0.90
```

### Verdict

**Score: 0.90**
**Verdict: REVISE**
**C4 Threshold: 0.95 — FAILED**
**General Threshold (H-13): 0.92 — FAILED (0.90 < 0.92)**

**Special Conditions Check:**
- Any dimension <= 0.50 (Critical)? No — minimum dimension score is 0.88 (Internal Consistency)
- Prior strategy reports contain unresolved Critical findings? No — all 3 I1 Critical findings are RESOLVED in R2
- New Critical findings in I2? No — all I2 findings are Major or Minor severity

**Improvement from I1:** Score improved from 0.83 to 0.90 (+0.07). All 3 Critical findings from I1 resolved. No new Critical findings introduced.

**Gap to C4 threshold:** 0.90 vs. 0.95 required. Gap = 0.05. This is a meaningful gap that requires targeted revision.

**Gap to H-13 threshold:** 0.90 vs. 0.92 required. Gap = 0.02. Close but below.

### Dimension Scores Summary

| Dimension | Weight | Score | Weighted | Change from I1 | Notes |
|-----------|--------|-------|----------|---------------|-------|
| Completeness | 0.20 | 0.91 | 0.182 | +0.09 | Phase 2 section + Known Scope Exclusions added |
| Internal Consistency | 0.20 | 0.88 | 0.176 | +0.10 | Agreement count fixed; new 75/74 inconsistency |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | +0.03 | Publication bias gap remains |
| Evidence Quality | 0.15 | 0.90 | 0.135 | +0.09 | Primary sources added; L0 overciting resolved |
| Actionability | 0.15 | 0.93 | 0.1395 | +0.09 | Phase 2 Design Requirements section major improvement |
| Traceability | 0.10 | 0.90 | 0.090 | +0.04 | Phase 2 derivations traced; Group C 4 unnamed |
| **Composite** | **1.00** | **0.90** | **0.90** | **+0.07** | Below H-13 (0.92) and C4 (0.95) |

### Leniency Bias Verification

- Each dimension scored independently: YES
- Evidence documented for each score: YES
- Uncertain scores resolved downward: YES (Completeness: 0.91 not 0.93 due to Group C gap; Internal Consistency: 0.88 not 0.90 due to new 75/74 inconsistency)
- High-scoring dimensions (>= 0.93): Actionability (0.93) — score justified by Phase 2 section addition with explicit derivations
- Low-scoring dimension evidence:
  1. Internal Consistency (0.88): New 75/74 inconsistency introduced by R2 A-31 addition; CONFLICT-4 label residue; "5 conditions" vs. "7 conditions" in PS Integration
  2. Completeness (0.91): Group C 4 unidentified sources; publication bias omission
- Weighted composite math verified: 0.182 + 0.176 + 0.180 + 0.135 + 0.1395 + 0.090 = 0.9025 ≈ 0.90 ✓
- Verdict matches score range: REVISE (0.90 is below both 0.92 and 0.95 thresholds) ✓
- Improvement recommendations are specific and actionable: YES

### Improvement Recommendations for I3 (Priority Order)

| Priority | Dimension | Gap | Required Action |
|----------|-----------|-----|----------------|
| 1 | Internal Consistency | 75 vs. 74 source count | Correct Tier Analysis to 75 total; update Tier 3 to 14 sources (add A-31); remove "A-31 replaces I-13" language |
| 2 | Completeness + Traceability | Group C 4 unidentified sources | Name all 13 Group C sources explicitly in arithmetic trace |
| 3 | Methodological Rigor | Publication bias not acknowledged | Add SE-5 to Known Scope Exclusions documenting publication bias as a systematic review limitation |
| 4 | Internal Consistency | PS Integration "5 conditions" vs. Phase 2 section "7 conditions" | Update PS Integration key finding #4 to state "minimum 7 conditions" or add a note that the 5 listed are the Required conditions only |
| 5 | Actionability | Cond-6/Cond-7 relative priority | Add relative priority signal within "Recommended" tier (Cond-7 > Cond-6 by evidence tier) |
| 6 | Completeness | Alternative hypothesis placement (DA-002-R2) | Move "On the revised hypothesis" to end of L0 or to Research Directions subsection |
| 7 | Evidence Quality | AGREE-5 hierarchy scope confound | Add explicit header note distinguishing prompt-engineering-accessible range (ranks 5-12) from non-accessible techniques (ranks 1-4) |
| 8 | Internal Consistency | Cond-6 epistemological labeling | Add note to Cond-6: "hypothesis-generating, not hypothesis-confirming; negative results should not be interpreted as invalidating the synthesis" |
| 9 | Internal Consistency | CONFLICT-4 label | Qualify CONFLICT-4 section heading as "UNRESOLVED (natural-language self-refinement only — see note)" |

---

## Consolidated Findings Index

> New findings from Iteration 2 only. Prior I1 findings that are RESOLVED are not listed (they are tracked in the Prior Finding Resolution Status section).

| ID | Strategy | Severity | Finding (one-line) | Section |
|----|----------|----------|--------------------|---------|
| SR-001-R2 | S-010 | Major | Group C 13-count has 4 unidentified sources; arithmetic trace not independently verifiable | Source Count Verification |
| SR-002-R2 | S-010 | Major | New inconsistency: L0 says 75 total sources; Tier Analysis says 74 | L0 Key Numbers vs. Evidence Tier Analysis |
| SR-003-R2 | S-010 | Minor | CONFLICT-4 "UNRESOLVED" headline label unqualified; body note qualifies it, header does not | L1: Conflicts |
| SR-004-R2 | S-010 | Minor | Phase 2 table lacks relative priority between Cond-6 and Cond-7 "Recommended" conditions | Phase 2 Experimental Design Requirements |
| SR-005-R2 | S-010 | Minor | PS Integration says "5 conditions"; Phase 2 Design section has 7 | PS Integration vs. Phase 2 Design |
| SM-001-R2 | S-003 | Major | No relative priority between Cond-6 and Cond-7 "Recommended" conditions; Cond-7 has stronger Tier 1 evidence | Phase 2 Experimental Design Requirements |
| SM-002-R2 | S-003 | Minor | AGREE-5 hierarchy ranks 6-12 lack stated evidence basis for ordering | L1: AGREE-5 effectiveness hierarchy |
| SM-003-R2 | S-003 | Minor | Best Case Scenario not incorporated into synthesis body (was in I1 S-003 output but not carried to document) | General / L0 |
| DA-001-R2 | S-002 | Major | AGREE-3 vendor consensus does not address vendor product positioning bias despite SE-3 acknowledging internal vendor benchmarks | L1: AGREE-3 |
| DA-002-R2 | S-002 | Major | Alternative hypothesis placement in L0 before Phase 2 mandate creates anchoring risk for Phase 2 analysts | L0: Executive Summary |
| DA-003-R2 | S-002 | Minor | "No source refutes it" phrasing could be read as absolution rather than null finding | L0: Executive Summary |
| DA-004-R2 | S-002 | Minor | AGREE-5 ranks 1-2 (model-internal/training-time) presented without explicit "outside PROJ-014 scope" header note | L1: AGREE-5 |
| PM-001-R2 | S-004 | Major | Cond-7 "Recommended" label despite stronger evidence than some Required conditions; practitioner may skip Cond-7 | Phase 2 Experimental Design Requirements |
| PM-002-R2 | S-004 | Minor | 75/74 count inconsistency creates reputational verification risk | L0 vs. Tier Analysis |
| PM-003-R2 | S-004 | Minor | GAP-5 "DO NOT CITE" box follows the unverified claim rather than preceding it | L1: Gaps, GAP-5 |
| RT-001-R2 | S-001 | Major | Publication bias not addressed in Known Scope Exclusions (SE-5 missing) | Known Scope Exclusions |
| RT-002-R2 | S-001 | Major | AGREE-5 effectiveness hierarchy mixes non-comparable access levels without explicit scope delineation | L1: AGREE-5 effectiveness hierarchy |
| RT-003-R2 | S-001 | Minor | A-31 described as widening "academic base" despite Tier 3 unreviewed status | L1: AGREE-4 |
| RT-004-R2 | S-001 | Minor | CONFLICT-2 explanation (4) (pragmatic recognition of prohibitions) de-emphasized despite direct hypothesis relevance | L1: CONFLICT-2 |
| CC-001-R2 | S-007 | Major | P-022 issue: 75 vs. 74 source count mismatch between L0 and Tier Analysis | L0 vs. Tier Analysis |
| CC-002-R2 | S-007 | Minor | P-011 residue: THEME-3 causal step about GPT-5.2 "confidently wrong output" still lacks cited mechanism | L2: THEME-3 |
| CV-001-R2 | S-011 | Major | Group C 4 unidentified sources prevent independent verification of 75-source total | Source Count Verification |
| CV-002-R2 | S-011 | Minor | Cond-6 traces to synthesis-generated THEME-1, not primary source; derivation chain "evidence → finding → condition" is incomplete | Phase 2 Experimental Design Requirements |
| CV-003-R2 | S-011 | Minor | Revision Log does not explicitly state whether RT-004 (circular citation chain) was addressed or deferred in R2 | Revision Log |
| FM-010 | S-012 | Major | New high-RPN risk: source count inconsistency (75 vs. 74) introduced by R2 has RPN 216 | L0/Tier Analysis |
| FM-011 | S-012 | Major | Group C 4 unidentified sources: RPN 200, prevents audit reproducibility | Source Count Verification |
| FM-012 | S-012 | Major | Cond-7 "Recommended" despite Tier 1 evidence: risk of omission in resource-constrained Phase 2 | Phase 2 Experimental Design |
| IN-001-R2 | S-013 | Major | Cond-6 amplifies synthesis hypothesis into experimental design without adequate epistemological flagging | Phase 2 Experimental Design Requirements |
| IN-002-R2 | S-013 | Minor | Vendor bias inversion (circular model optimization) not addressed in SE-3 | Known Scope Exclusions SE-3 |

---

## Revision Priorities

> Priority ordering for I3 revision based on RPN, S-014 score impact, and C4 threshold gap analysis.

| Priority | ID(s) | Severity | Action | Score Impact |
|----------|--------|----------|--------|-------------|
| **P1** | SR-002-R2, CC-001-R2, FM-010 | Major | Correct Tier Analysis total to 75; update Tier 3 to 14 sources; remove "A-31 replaces I-13" language | Internal Consistency +0.03 |
| **P2** | SR-001-R2, CV-001-R2, FM-011 | Major | Name all 13 Group C sources explicitly in arithmetic trace | Completeness +0.02, Traceability +0.02 |
| **P3** | RT-001-R2 | Major | Add SE-5 to Known Scope Exclusions: publication bias as systematic review limitation | Methodological Rigor +0.02 |
| **P4** | SR-005-R2 | Minor | Update PS Integration to reference 7 conditions (or distinguish "5 Required" from 7 total) | Internal Consistency +0.01 |
| **P5** | SM-001-R2, PM-001-R2, FM-012 | Major | Add relative priority within "Recommended" tier (Cond-7 > Cond-6 by evidence strength) | Actionability +0.01 |
| **P6** | DA-002-R2 | Major | Relocate "On the revised hypothesis" to end of L0 or to dedicated Research Directions subsection | Actionability +0.01, Internal Consistency +0.01 |
| **P7** | RT-002-R2, DA-004-R2 | Major | Add header note to AGREE-5 hierarchy distinguishing prompt-accessible range (5-12) from non-accessible (1-4) | Evidence Quality +0.01 |
| **P8** | IN-001-R2, CV-002-R2 | Major | Add "hypothesis-generating, not hypothesis-confirming" note to Cond-6; clarify negative results interpretation | Methodological Rigor +0.01 |
| **P9** | DA-001-R2 | Major | Add vendor product positioning caveat to AGREE-3 | Evidence Quality +0.01, Completeness +0.01 |
| **P10** | SR-003-R2 | Minor | Qualify CONFLICT-4 section heading: "UNRESOLVED (natural-language self-refinement only)" | Internal Consistency +0.01 |

**Estimated I3 achievable score if P1-P5 completed:** ~0.93 (meets H-13 general threshold)
**Estimated I3 achievable score if P1-P9 completed:** ~0.95 (meets C4 threshold)

---

## Execution Statistics

- **Total new findings (I2):** 28
- **Critical:** 0
- **Major:** 14
- **Minor:** 14
- **Prior Critical Findings Resolved:** 3 of 3 (DA-001, DA-002/CC-002, IN-001)
- **Prior Major Findings Resolved:** All Priority 1-2 Major findings from I1 resolved
- **New Issues Introduced by R2:** 3 Major (SR-002-R2 source count inconsistency; RT-002-R2 AGREE-5 scope confusion; IN-001-R2 Cond-6 epistemological flagging), 2 minor arithmetic traces
- **Score delta:** 0.83 (I1) → 0.90 (I2) = +0.07 improvement
- **Protocol Steps Completed:** All 10 strategies fully executed (S-010 through S-014)
- **C4 Threshold Status:** FAILED (0.90 vs. 0.95 required); gap = 0.05
- **H-13 Threshold Status:** FAILED (0.90 vs. 0.92 required); gap = 0.02

---

*Tournament executed by adv-executor | Iteration 2 | 2026-02-27*
*C4 criticality tournament — all 10 strategies executed*
*H-16 compliance verified: S-003 precedes S-002*
*P-003 (no recursion): PASS | P-022 (no deception): findings accurately reported | P-011 (evidence-based): all findings cite specific evidence from deliverable*
