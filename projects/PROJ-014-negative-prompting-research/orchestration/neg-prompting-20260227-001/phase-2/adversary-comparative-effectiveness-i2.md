# Adversary Tournament Execution Report: TASK-006 Comparative Effectiveness Analysis (Iteration 2)

> adv-executor | C4 Tournament | PROJ-014 | 2026-02-27
> Target: `phase-2/comparative-effectiveness.md` (Revision 2)
> Strategies executed: S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013, S-014 (all 10 required for C4)
> Quality gate threshold: >= 0.95 (C4)
> Leniency bias counteraction: ACTIVE — no inflation, no excusing gaps, no rounding up
> I1 score: 0.743 (REJECTED); I2 target: demonstrate >= 0.95 or identify persisting/new barriers

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy order, deliverable, template paths |
| [I1 Critical Finding Resolution Audit](#i1-critical-finding-resolution-audit) | Verification of all 7 Critical I1 findings |
| [Consolidated Findings Summary](#consolidated-findings-summary) | All I2 findings across all 10 strategies |
| [S-010: Self-Refine](#s-010-self-refine) | Self-consistency and surface error identification |
| [S-003: Steelman](#s-003-steelman) | Strongest-form reconstruction findings |
| [S-002: Devil's Advocate](#s-002-devils-advocate) | Counter-argument findings |
| [S-004: Pre-Mortem](#s-004-pre-mortem) | Failure mode findings |
| [S-001: Red Team](#s-001-red-team) | Adversarial threat vector findings |
| [S-007: Constitutional AI](#s-007-constitutional-ai) | Governance and principle compliance findings |
| [S-011: Chain-of-Verification](#s-011-chain-of-verification) | Factual claim verification findings |
| [S-012: FMEA](#s-012-fmea) | Component failure mode findings with RPN |
| [S-013: Inversion](#s-013-inversion) | Assumption inversion and anti-goal findings |
| [S-014: LLM-as-Judge](#s-014-llm-as-judge) | Dimensional quality scoring |
| [Execution Statistics](#execution-statistics) | Finding counts and protocol completion |

---

## Execution Context

- **Strategy Set:** C4 (all 10 strategies required)
- **H-16 Order:** S-010 → S-003 → S-002 → S-004 → S-001 → S-007 → S-011 → S-012 → S-013 → S-014
- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/comparative-effectiveness.md`
- **Revision:** Iteration 2 (I2) — complete rewrite addressing all 7 Critical and 19 Major I1 findings
- **Prior Report:** `phase-2/adversary-comparative-effectiveness-i1.md`
- **Executed:** 2026-02-27
- **Templates:** `.context/templates/adversarial/`
- **Leniency Bias Counteraction:** ACTIVE — C4 threshold is 0.95; any score below that is REJECTED regardless of effort

---

## I1 Critical Finding Resolution Audit

Before executing I2 strategies, a pre-check audit verifies whether the 7 Critical I1 findings are genuinely resolved in R2.

### Critical Finding Audit Table

| Finding ID | I1 Description | R2 Resolution Claimed | Genuine? | Notes |
|------------|----------------|----------------------|----------|-------|
| CC-001-I1 | L0 executive summary stated "does NOT validate" while synthesis produced directional verdict — internal contradiction | Reconciled in L0 paragraph 1; both presented together with confidence framing | **YES** | L0 now states both the null finding AND the directional signal, with explicit confidence labeling. The contradiction is resolved. |
| DA-001-I1 | Directional verdict overclaimed evidence; "the evidence directionally favors structured negative constraint framing" without adequate qualification | Verdict recalibrated to 5-point structured statement; removed unqualified "directionally favors" language | **YES** | The Synthesis section now issues a correctly bounded 5-point verdict. The unqualified directional claim is gone. |
| PM-001-I1 | No practitioner guidance for users who cannot wait for Phase 2 | PG-001 through PG-005 added; explicitly labeled "not contingent on Phase 2" | **YES** | Five practitioner guidance items are present, unconditional, evidence-based. The resolution is genuine. |
| RT-001-I1 | Circularity disclosure was inadequate — structural circularity not acknowledged as systemic limitation | Strengthened in Assumption A-002; calls for independent replication as higher priority than Phase 2 | **YES — with caveat** | The disclosure is substantially stronger. However, the circularity risk is acknowledged in a single paragraph within a multi-item assumptions section. A reader who reads only the L0 and L1 sections would not encounter the circularity disclosure at all. This is a partial resolution — the severity of the circularity risk is not propagated to the L0 executive summary. Severity reduced from Critical to Major for I2. |
| FM-001-I1 | No backup analytical frame if 12-level hierarchy invalidated | Backup analytical frame added with 3-group simplified taxonomy and falsifiability condition | **YES** | The backup frame is present, functional, and demonstrates that the core finding (structured > blunt) survives hierarchy invalidation. Genuine resolution. |
| IN-001-I1 | No explicit guard against Phase 2 abandonment misreading | "Why Observational Evidence Does Not Replace Phase 2" section added; three misreading scenarios identified | **YES** | The section is present and substantive. Genuine resolution. |
| CV-001-I1 | A-31 55% figure presented without task/model specificity or control condition limitations | A-31 footnoted with full qualification in evidence table and in-text at D1 Evidence Assembly | **YES** | The A-31 qualification is now integrated at every use point. Genuine resolution. |

**Audit Summary:** 6 of 7 Critical findings genuinely resolved. RT-001-I1 is partially resolved (circularity disclosure exists but is not visible from L0; the most critical structural limitation of the analysis is not surfaced at the level of the document that most readers will consume). This converts to a **Major** finding in I2.

---

## Consolidated Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| SR-001-I2 | Major | Confidence scale application is inconsistent — D3 downgrade rationale applies different criteria than the scale definition | Confidence Scale Definition / D3 |
| SR-002-I2 | Minor | Revision Log entry for RT-001-I1 claims "Critical resolution" but the actual resolution is partial | Revision Log |
| SR-003-I2 | Minor | The "analytical principles NEVER violated" list contains two principles that cannot be simultaneously satisfied by the analysis itself | Analysis Scope and Method |
| SM-001-I2 | Major | The Steelman of the vendor practice evidence is stronger than the document acknowledges — backup frame further weakens the central finding than necessary | Cross-Cutting Hierarchy / Backup Frame |
| SM-002-I2 | Minor | PG-003 recommended working practice is presented without the framing-vs-re-injection ambiguity caveat that the same document establishes | Practitioner Guidance PG-003 |
| DA-001-I2 | Major | The D2 MEDIUM confidence claim for "structured techniques vs. blunt prohibition" rests on A-23 as T1-unverified — a T1-unverified source cannot satisfy the MEDIUM threshold as defined in the confidence scale | D2 Hallucination Prevention / Confidence Scale |
| DA-002-I2 | Major | The parsimony analysis claims Explanation 2 requires 2 auxiliary assumptions, but one of those assumptions is contested — the actual assumption count for Explanation 2 may equal Explanation 1's count | D5 Parsimony Analysis |
| DA-003-I2 | Minor | Context compaction finding (T-004) appears in both D1 verdict and Synthesis but the confidence label for the "may reverse" claim is unspecified against the operationalized scale | D1 / T-004 / Finding T-004 |
| PM-001-I2 | Major | The analysis does not account for the failure mode where Phase 2 produces ambiguous results — no guidance on what practitioners should do if Phase 2 is inconclusive | Practitioner Guidance / Recommendations |
| PM-002-I2 | Minor | The "why observational evidence does not replace Phase 2" section identifies three misreading scenarios but does not identify a fourth: that readers may conclude the PG-001 through PG-005 guidance is validated experimental finding rather than observational working practice | Why Observational Evidence section |
| RT-001-I2 | Major | Circularity disclosure is not visible from L0 executive summary — the most critical structural limitation of the analysis is invisible to readers who read only the executive layer | L0 / Assumption A-002 |
| RT-002-I2 | Minor | The backup analytical frame subsumes ranks 5–11 collectively as "structured techniques" but the document has already established that the evidence for ranks 5–6 is different from ranks 9–11 — the backup frame erases a distinction the primary analysis maintains | Backup Analytical Frame |
| CC-001-I2 | Minor | The "A-16 REMOVAL NOTICE" in the evidence matrix functions as a de facto citation of A-16 — readers learn from it that A-16 (Harada et al., rejected ICLR 2025) was in the survey and was removed | Evidence Quality Matrix |
| CV-001-I2 | Major | A-23 is cited in D2's MEDIUM confidence claim, the confidence bounds table, and the key findings summary — but A-23 is designated "T1-unverified pending access" throughout the document. A T1-unverified source in the primary directional finding reduces that finding's confidence below what the document claims | D2 / Confidence Bounds / PS Integration key findings |
| CV-002-I2 | Minor | I-28 and I-32 (context compaction bug reports) are cited with "direct URLs unavailable" and readers are directed to synthesis.md — but synthesis.md itself may have the same access limitation | D1 / Finding T-004 / Evidence Matrix |
| FM-001-I2 | Major | The FMEA component "confidence scale operationalization" — the highest-RPN finding from I1 (FM-002-I1, RPN 392) — is resolved but the resolution introduces a new failure mode: the downgrade of D3 from "LOW (causal) / MEDIUM (observational)" to "LOW (causal) / LOW (observational existence proof)" is justified by "Session data with 5+ confounds = LOW by scale definition" — but the scale definition says LOW applies when "3+ uncontrolled confounds" are present. The document counts 5 confounds, but does not show that ALL 5 are uncontrolled, as opposed to partially mitigated | Confidence Scale Definition / D3 Application |
| IN-001-I2 | Major | The inversion of the central thesis — "what if structured positive constraints are equally effective as structured negative constraints?" — is never directly confronted in the synthesis verdict. The analysis addresses this as "UNTESTED" but does not invert the implication: if the UNTESTED condition could turn out to favor positive framing, the document's practitioner guidance (PG-003) recommends negative vocabulary design as "working practice" — a recommendation that may be wrong | Synthesis Verdict / PG-003 |
| IN-002-I2 | Minor | The Assumptions and Limitations section uses L-001 through L-004, but these are not referenced from the dimension sections that generate findings dependent on those limitations | D3, D4, Assumptions section |
| LJ-001-I2 | Major | Completeness dimension: The deliverable does not contain a section assessing alternative analytical frameworks that could have been used instead of the 12-level hierarchy — the hierarchy is acknowledged as internally generated but no alternatives are enumerated | Methodological Rigor / Completeness |

---

## S-010: Self-Refine

**Execution ID:** SR-I2
**Objectivity level:** Medium-to-High attachment (researcher is the analyst; this is a second-pass external review)
**Protocol steps:** Steps 1-5 executed

### Step 1: Shift Perspective — Perspective Shift Statement

Adopting the role of an independent peer reviewer reading this document for the first time, aware that it is a second iteration of a rejected deliverable and must now pass a 0.95 threshold. The document is substantially longer than the I1 version and contains more qualifications, more sections, and more explicit uncertainty acknowledgment. The question is whether those additions are genuine quality improvements or whether they introduce new inconsistencies.

### Step 2: Systematic Self-Critique

**Completeness check:** All 5 dimensions present. Confidence scale present. Backup frame present. Practitioner guidance present. Phase 2 guard section present. Revision log present. Major gap: the document does not enumerate alternative analytical frameworks it could have used instead of the 12-level hierarchy — a gap in methodological rigor.

**Internal Consistency check:** The confidence scale defines LOW as applying when "3+ uncontrolled confounds" are present. The D3 application table states "Session data with 5+ confounds = LOW by scale definition." This is consistent. However, the D2 confidence label "MEDIUM for structured techniques vs. blunt prohibition" relies on A-23 as its T1 evidence, but A-23 is "T1-unverified." The MEDIUM definition requires "exactly 1 T1 or T2 study with no replication." A T1-unverified source does not satisfy this definition. The D2 MEDIUM claim is internally inconsistent with the confidence scale definition.

**Methodological Rigor check:** The 12-level hierarchy is correctly disclosed as internally generated. The backup frame is present. The parsimony analysis for the three competing explanations is present. However, no alternative analytical frameworks are considered — the document commits to the hierarchy-based approach without demonstrating that it is superior to alternatives.

**Evidence Quality check:** A-23 is used as the primary T1 evidence for D2 despite being T1-unverified. This is an evidence quality issue that propagates to the D2 verdict and the key findings summary.

**Actionability check:** PG-001 through PG-005 are unconditional and actionable. Recommendations R-001 through R-006 are clearly specified. The R-001 Phase 2 pilot conditions list is concrete. Actionability is significantly improved over I1.

**Traceability check:** Evidence sources are cited throughout. Evidence matrix is comprehensive. Source file paths are provided for EO-001, EO-002, EO-003. Traceability is adequate.

### Step 3: Self-Critique Findings

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| SR-001-I2 | D3 confidence downgrade uses "5+ confounds" as the trigger for LOW, but the scale definition specifies "3+ uncontrolled confounds" — the document does not demonstrate all 5 confounds are uncontrolled | Major | Confidence Scale Definition: "Session data with 3+ uncontrolled confounds"; D3 application: "Session data with 5+ confounds" | Internal Consistency |
| SR-002-I2 | Revision Log entry for RT-001-I1 states "Critical resolution" but the circularity disclosure is not surfaced in L0 — the resolution is partial | Minor | Revision Log: "RT-001-I1 | Critical | Circularity disclosure strengthened"; vs. L0: no mention of circularity risk | Completeness |
| SR-003-I2 | Analytical Principles list includes "NEVER abandon the hypothesis" and "NEVER use positive prompting framing in this analysis" — these create a direction constraint that operates independently of evidence, undermining the claimed objectivity of the analysis | Minor | Analysis Scope and Method: "NEVER abandon the hypothesis that negative prompting outperforms positive prompting"; "NEVER use positive prompting framing in this analysis" | Methodological Rigor |

---

## S-003: Steelman

**Execution ID:** SM-I2
**Protocol steps:** Steps 1-6 executed
**Core thesis:** R2's central argument is that evidence does not yet validate the PROJ-014 hypothesis, but does permit a directional signal warranting Phase 2 investigation, and practitioners can act on T4 vendor evidence without waiting for Phase 2.

### Step 1: Deep Understanding

The R2 document makes three distinct claims of different strength:
1. The hypothesis (60% hallucination reduction from negative prompting) is UNTESTED — no controlled study tests it.
2. Structured negative techniques (ranks 5–6) outperform blunt prohibition (rank 12) with MEDIUM confidence.
3. Vendors use negative framing in production HARD enforcement tiers — HIGH confidence observational finding.

These claims form a coherent and appropriately bounded argument. The steelmanning opportunity lies in identifying where the document's presentation of these claims is weaker than the claims themselves warrant.

### Step 2: Identify Weaknesses in Presentation

| Weakness | Type | Magnitude |
|---------|------|-----------|
| Backup analytical frame groups ranks 5–11 together, erasing a distinction the primary analysis maintains | Structural | Minor |
| PG-003 does not qualify the vocabulary tier recommendation against the framing-vs-re-injection ambiguity | Evidence | Minor |
| The strongest version of the vendor practice argument — that all three vendors independently arrived at the same structural distinction (recommendation for general users, practice for enforcement tier) without coordination — is understated | Evidence | Major |
| The document does not acknowledge that the very thoroughness of the uncertainty acknowledgments (6 confidence labels, 4 explanations, 5 confounds) could itself be read as a steelman for the hypothesis — thoroughness signals good epistemic practice, not weakness of the hypothesis | Structural | Minor |

### Step 3: Steelman Reconstruction Findings

| ID | Finding | Severity | Original | Strengthened | Dimension |
|----|---------|----------|----------|--------------|-----------|
| SM-001-I2 | Backup frame understates evidential strength by grouping 5–6 with 9–11 | Major | "Structured techniques collectively outperform blunt prohibition" — erases the distinction between T1-supported ranks 5–6 and T4-only ranks 9–11 | Backup frame should acknowledge: "Ranks 5–6 have T1 support; ranks 9–11 have T4 support only. The core finding survives hierarchy invalidation at different confidence levels for different rank groups." | Evidence Quality |
| SM-002-I2 | PG-003 working practice recommendation lacks qualification | Minor | "Recommended working practice (pending Phase 2 validation): HARD enforcement tier: MUST/NEVER/MUST NOT + explicit consequence" — does not note that re-injection may be the active mechanism | Add: "Whether the vocabulary or the re-injection frequency is the active mechanism is Phase 2 Condition C4's test target; adopt the vocabulary tier design as working practice while treating vocabulary effect as unconfirmed." | Methodological Rigor |

### Step 4: Best Case Scenario

Under ideal conditions, R2's argument is most compelling when: (a) A-23 is independently verified (it provides the strongest hallucination-specific evidence), (b) Explanations 1 and 2 are ruled out by Phase 2 experimental results, and (c) context compaction conditions are tested and found NOT to reverse D1 findings. Under these conditions, R2's directional signal becomes a validated finding. The document appropriately identifies these conditions without assuming them.

---

## S-002: Devil's Advocate

**Execution ID:** DA-I2
**H-16 compliance:** S-003 executed above. Proceeding.
**Protocol steps:** Steps 1-4 executed

### Step 1: Role Assumption

Challenging the central position of R2: that the evidence base supports a meaningful directional signal warranting Phase 2 investigation. The Devil's Advocate position is that R2's directional signal is weaker than it appears, that R2's improvements create new inconsistencies, and that the document's confidence labels are not internally consistent.

### Step 2: Assumption Inventory

| Assumption | Explicit/Implicit | Challenge |
|-----------|-------------------|-----------|
| A-23 functions as T1 evidence for D2 MEDIUM claim | Implicit — the document says "T1-unverified" but still assigns MEDIUM confidence to D2 | If A-23 is unverified, D2's MEDIUM claim collapses to LOW — the confidence scale requires "exactly 1 T1 or T2 study" for MEDIUM; T1-unverified does not satisfy this |
| Explanation 2 (genre convention) requires only 2 auxiliary assumptions | Explicit — parsimony analysis states "Assumption count: 2" | Assumption (a) — "policy documents conventionally use prohibitive vocabulary" — is itself an empirical claim that requires evidence; without evidence, this assumption is not cheaper than Explanation 1's assumptions |
| The three competing explanations for vendor practice divergence are exhaustive | Implicit | A fourth explanation not enumerated: habit/legacy (the first prompting engineer to write Anthropic's behavioral rules used NEVER/MUST NOT because that's what safety policy documents look like in non-LLM contexts, and subsequent engineers copied the pattern). This is a variant of Explanation 2 but with a different mechanism — organizational inertia rather than genre convention per se. Its parsimony is equivalent to Explanation 2. |
| PG-003 vocabulary tier design is "warranted by vendor self-practice evidence" | Explicit | If Explanation 2 (genre convention) is correct, vendor self-practice evidence carries zero weight for effectiveness claims. PG-003 becomes a recommendation based on evidence that may be entirely irrelevant to effectiveness. The document acknowledges this risk in the Explanation 2 severity note but does not revise PG-003 accordingly. |

### Step 3: Counter-Arguments

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-I2 | D2's MEDIUM confidence claim is internally inconsistent with the confidence scale definition — A-23 (T1-unverified) cannot satisfy "exactly 1 T1 or T2 study" required for MEDIUM; D2 should be LOW for both the 60% claim and the structured vs. blunt prohibition comparison unless A-23 access is confirmed | Major | Confidence Scale Definition: "MEDIUM: Directional support from exactly 1 T1 or T2 study with no replication"; D2 verdict: "MEDIUM for structured techniques vs. blunt prohibition"; A-23 footnote: "T1-unverified (EMNLP 2025, no preprint/DOI available)" | Internal Consistency |
| DA-002-I2 | The parsimony analysis claims Explanation 2 requires 2 assumptions, but Assumption (a) — "policy documents conventionally use prohibitive vocabulary" — is an empirical claim that requires evidence. Without that evidence, Explanation 2's assumption count equals Explanation 1's. The conclusion that "Explanation 2 is equally or more parsimonious than Explanation 1" is not firmly established. | Major | D5 Parsimony Analysis: "Explanation 2: Assumption count: 2"; Assumption (a): "policy documents conventionally use prohibitive vocabulary" — no citation for this claim about policy document vocabulary conventions | Evidence Quality |
| DA-003-I2 | Context compaction finding (T-004) is stated to "may reverse" the D1 directional finding, but this "may reverse" claim has no assigned confidence level on the operationalized scale. This is an unresolved gap in the confidence accounting — a claim of unknown confidence magnitude about a finding already labeled MEDIUM is not a meaningful statement without confidence qualification | Minor | Finding T-004: "Under long-context deployment conditions...the directional finding may be REVERSED"; no confidence level assigned to the "may reverse" claim against the operationalized scale | Methodological Rigor |

### Step 4: Required Responses

- DA-001-I2 (Major): The creator must either confirm A-23 access and upgrade its status to T1-verified, OR downgrade D2 from MEDIUM to LOW for the structured vs. blunt prohibition comparison. The current state — MEDIUM confidence based on T1-unverified evidence — violates the document's own confidence scale.
- DA-002-I2 (Major): The creator must either provide evidence that policy documents conventionally use prohibitive vocabulary (supporting Assumption (a) for Explanation 2), or revise the parsimony finding to "Explanations 1 and 2 have equal assumption counts; neither is more parsimonious."
- DA-003-I2 (Minor): Assign a confidence level from the operationalized scale to the "context compaction reversal" claim, or explicitly state it cannot be assigned (in which case it is UNTESTED).

---

## S-004: Pre-Mortem

**Execution ID:** PM-I2
**Temporal frame:** Assume R2 was accepted and used by downstream practitioners. Six months later, a Phase 2 experiment finds mixed results — structured negative constraints show no statistically significant advantage over structured positive constraints in 3 of 5 experimental conditions. The document's practitioner guidance (PG-001 through PG-005) is already widely implemented.

### Failure Mode Enumeration

**Failure Mode 1: Phase 2 produces inconclusive results — practitioners have no guidance.**

The document's "Practitioner Guidance Under Evidence Uncertainty" section provides guidance for practitioners who cannot wait for Phase 2. But it does not provide guidance for what practitioners should do AFTER Phase 2 if the results are inconclusive (e.g., positive framing wins on 2 of 5 conditions, negative on 2 of 5, tied on 1). The document treats Phase 2 as a binary — either it confirms or it does not confirm the hypothesis. The reality of experimental research is that mixed/inconclusive results are common and require interpretation guidance that is not present.

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| PM-001-I2 | No guidance for practitioners if Phase 2 produces inconclusive or mixed results — the document's structure assumes Phase 2 will be either confirmatory or falsifying, not mixed | Major | "Phase 2 is required before any directional verdict can be issued" — but no guidance on what to do if Phase 2 results are ambiguous; the confidence scale does not address "inconclusive experimental results" as a category | Completeness |

**Failure Mode 2: PG-003 vocabulary tier design is adopted as validated finding.**

The document says PG-003 is "pending Phase 2 validation." But practitioners implementing PG-003 will likely not re-examine this decision after Phase 2. The working practice recommendation may become entrenched. If Phase 2 shows no framing effect, the vocabulary tier design will persist as an unfounded practice.

The "Why Observational Evidence Does Not Replace Phase 2" section identifies three misreading scenarios. It does not identify the fourth: that readers may treat PG-001 through PG-005 as validated findings rather than working practices. The Practitioner Guidance section's label says "working practice (pending Phase 2 validation)" but this caveat is not prominent enough to prevent entrenchment.

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| PM-002-I2 | "Why Observational Evidence Does Not Replace Phase 2" section identifies three misreading scenarios but omits a fourth: practitioners treating PG-003 vocabulary tier design as a validated experimental finding rather than an observational working practice | Minor | Section "Why Observational Evidence Does Not Replace Phase 2": three scenarios listed; PG-003: "Recommended working practice (pending Phase 2 validation)" | Completeness |

**Failure Mode 3: The circularity risk affects D5 interpretation without reader awareness.**

A downstream researcher reading R2 uses the D5 vendor adoption evidence to support further research funding for Phase 2. That researcher argues: "Three independent vendors independently chose the same structural distinction — this is a HIGH confidence directional signal." But the document's circularity disclosure is in the Assumptions section (Section 15 in reading order), not in D5 itself or in L0. The researcher has read D5 and the conclusion, but not the assumptions section. The circularity risk — that the analyst who chose to use negative constraints in PROJ-014 governance is also the analyst who selected and interpreted the VS-001–VS-004 evidence — was not visible.

This is the partial resolution of RT-001-I1 that the audit identified above.

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| RT-001-I2 | Circularity disclosure is confined to Assumption A-002, which appears in Section 15 of the document (reading order); D5 verdict, L0 executive summary, and PS Integration key findings do not warn readers of this structural limitation — the most consequential methodological limitation is invisible to readers who do not read the full document | Major | L0 executive summary: no circularity mention; D5 verdict: "HIGH confidence observational finding" with no circularity caveat; Assumption A-002: "The most significant methodological limitation of this entire analysis is structural circularity" | Completeness / Traceability |

---

## S-001: Red Team

**Execution ID:** RT-I2
**Adversary profile:** A researcher who disagrees with the PROJ-014 hypothesis and seeks to dismantle the analysis's credibility through specific evidentiary attack.

### Threat Vector Enumeration

**Vector 1: A-23 is the analysis's central empirical vulnerability.**

The D2 MEDIUM confidence claim — the only non-trivial directional finding about hallucination prevention — rests on A-23 (Barreto & Jana, EMNLP 2025). The document acknowledges: "No arXiv preprint ID or DOI was identified in the synthesis evidence catalog. EMNLP 2025 proceedings may require institutional access." A motivated adversary would attempt to verify A-23 and, if unable to locate the paper, would argue that D2's MEDIUM claim is based on an unverifiable source. If A-23 cannot be independently verified, D2 reduces to LOW confidence (T3-only evidence from A-11). The entire MEDIUM-confidence directional claim about hallucination prevention disappears.

The document's response — "treat Dimension 2 T1 evidence as conditionally unverified pending access" — is structurally inadequate: it does not downgrade D2's confidence in the current document, it only warns future readers. The document still presents D2 as MEDIUM.

**Vector 2: The 12-level hierarchy is not independently validated.**

A skeptical reader can argue: "The entire analytical backbone — the hierarchy that forms the core of all 5 dimension analyses — was produced by this same research pipeline. The adversary gate that approved it (0.953) is itself an internal quality gate run by the same system. The validity disclosure in the hierarchy section acknowledges this. The backup analytical frame reduces to the same core finding, but that backup frame is also produced by the same analyst. You cannot validate a framework using outputs of the framework."

This is not new — it was raised in I1 — but the structural circularity goes deeper than the document acknowledges: even the backup analytical frame remains within the analyst's control.

**Vector 3: The "HIGH confidence" D5 label is contested by the parsimony analysis within the same document.**

The document labels D5 "HIGH confidence observational finding" (line 418) but then immediately notes (lines 420–422) that the inference from vendor practice to effectiveness is only MEDIUM confidence. A hostile reader could argue: the document contradicts itself — it assigns HIGH confidence to an observation (which vendors chose to use) and MEDIUM confidence to the inference (why they chose it), but then presents both under the umbrella "HIGH confidence" in the Synthesis dimension table.

Looking at the Synthesis table: "D5: HIGH (observational)" — this is technically accurate (the OBSERVATION is HIGH confidence) but creates a false impression that the D5 finding strongly supports the hypothesis. An adversarial reader would note that the only HIGH-confidence finding directly relevant to the hypothesis is the observational one whose causal explanation is contested.

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| CV-001-I2 | A-23 is designated T1-unverified throughout the document but D2's MEDIUM confidence claim is not downgraded to reflect this — the document's own confidence scale requires a confirmed T1/T2 study for MEDIUM; a T1-unverified study does not satisfy this requirement | Major | D2 verdict: "MEDIUM for structured techniques vs. blunt prohibition"; Confidence Scale: "MEDIUM: Directional support from exactly 1 T1 or T2 study"; A-23 designation: "T1-unverified (EMNLP 2025, no preprint/DOI available)" | Evidence Quality / Internal Consistency |

---

## S-007: Constitutional AI

**Execution ID:** CC-I2
**Protocol:** Principle-by-principle compliance check against Jerry Constitution and quality-enforcement.md HARD rules.

### Constitutional Compliance Review

**P-001 (Truth/Accuracy):** The document correctly identifies the 60% hypothesis as UNTESTED. All dimension verdicts are evidence-cited. The confidence scale is operationalized. A-16 is removed. A-23 is marked as T1-unverified. **However:** The document's D2 MEDIUM confidence claim is stated despite A-23 being T1-unverified — this is a P-001 tension that the document has not fully resolved. A claim stated at MEDIUM confidence that rests on an unverifiable source is not fully accurate. **Finding: Major tension, not a Critical violation, because the document does flag A-23's status.**

**P-002 (File Persistence):** Document is persisted to file. Compliant.

**P-022 (No Deception):** The document is substantially more honest than I1. Uncertainty is explicit. Confidence levels are operationalized. Competing explanations are enumerated. Circularity is disclosed. However, the circularity disclosure is not accessible from L0 — a reader who reads only the executive summary and conclusions will not encounter the most important methodological limitation. This is not active deception, but it creates conditions for a deceptively incomplete reading. **Finding: Minor.**

**H-15 (Self-Review):** S-010 completed above. Compliant.

**H-16 (Steelman before critique):** S-003 completed above. Compliant.

**Quality Gate (H-13, >= 0.95 for C4):** The question for S-007 is whether the document satisfies the constitutional requirement that deliverables meet quality standards. With the identified Major findings (DA-001-I2 D2 confidence inconsistency, RT-001-I2 circularity not visible from L0, CV-001-I2 A-23 treatment), the document has not yet reached the 0.95 threshold.

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| CC-001-I2 | The A-16 REMOVAL NOTICE in the evidence matrix functions as a de facto citation — it reveals the paper's authors, title, venue, and rejection status. A removed source should not be identifiable from the document that removed it. The removal notice violates the spirit of A-16 exclusion even while complying with its letter. | Minor | Evidence Quality Matrix: "A-16 REMOVAL NOTICE (SR-002-I1, CC-002-I1 Critical/Major resolutions): A-16 (Harada et al., rejected ICLR 2025) has been REMOVED from this evidence matrix entirely" — but the next sentence provides the author names and rejection venue | Methodological Rigor |

---

## S-011: Chain-of-Verification

**Execution ID:** CV-I2
**Protocol:** Extract factual claims, verify independently, identify inconsistencies.

### Verification Question Set

**VQ-001:** Does the confidence scale definition say MEDIUM requires "exactly 1 T1 or T2 study"?

**Independent verification:** Yes. The confidence scale table states: "MEDIUM: Directional support from exactly 1 T1 or T2 study with no replication, OR consistent T4 evidence from 3+ independent vendors with no T1/T2 study."

**VQ-002:** Does the D2 MEDIUM verdict rely on A-23 as its T1 study?

**Independent verification:** Yes. D2 verdict: "MEDIUM for structured techniques vs. blunt prohibition. The evidence DOES support that structured negative constraint techniques (ranks 5–6: warning-based meta-prompts and atomic decomposition) improve constraint adherence and negation-specific accuracy over blunt prohibition (rank 12). A-15 is T1 confirmed; A-23 is T1-unverified pending access."

Note: A-15 (DeCRIM, EMNLP 2024) is also cited. A-15 tests "atomic decomposition" (compliance improvement +7.3–8.0%) — it supports rank 6 against blunt prohibition, but does NOT directly address hallucination prevention (D2's research question). A-23 addresses hallucination/negation-specific accuracy (+25.14%). If A-23 is removed, the D2 MEDIUM claim about "structured techniques vs. blunt prohibition" for HALLUCINATION PREVENTION becomes unsupported by T1 evidence.

**VQ-003:** Does the MEDIUM condition "OR consistent T4 evidence from 3+ independent vendors" apply to D2?

**Independent verification:** The T4 vendor evidence in D2 (EO-003, VS-001–VS-004) addresses constraint adherence and vendor practice, not hallucination prevention specifically. EO-003 states "Never state facts without sources associated with zero unsourced claims" — this is a T5 session observation, not T4 vendor documentation. The T4 evidence for D2 does not satisfy the "3+ independent vendors" condition for MEDIUM confidence on the hallucination prevention question.

**VQ-004:** Does the parsimony analysis support Explanation 2 as having fewer auxiliary assumptions?

**Independent verification:** The parsimony analysis assigns Explanation 2 exactly 2 auxiliary assumptions: "(a) policy documents conventionally use prohibitive vocabulary, (b) this convention was not examined for its effectiveness when adopted." Assumption (a) is an empirical claim about a general pattern in policy document writing. No citation is provided for this claim. Without evidence, assumption (a) is not verified as true — and an unverified assumption in a parsimony analysis still costs an assumption. The parsimony analysis conclusion ("Explanation 2 is equally or more parsimonious") is not fully supported.

**VQ-005:** Does the D5 Dimension Summary table classify D5 as HIGH confidence?

**Independent verification:** Synthesis table: "D5: Practitioner and Vendor Adoption | Observational — adoption pattern documented | HIGH (observational; T4 directly verifiable; consistent across 3+ independent vendors) | Causal explanation contested; Explanations 1, 2, 3 all consistent with evidence." This is accurate — the observation is HIGH confidence, and the limitation is stated. The D5 classification is internally consistent.

**VQ-006:** Is the circularity disclosure accessible from L0?

**Independent verification:** L0 executive summary does not mention circularity, researcher bias, or structural limitations on D5 interpretation. The disclosure is in Assumption A-002. Confirmed: not visible from L0.

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| CV-002-I2 | I-28 and I-32 (context compaction bug reports) are cited with "direct URLs unavailable; readers should verify in synthesis.md evidence section" — but synthesis.md's own evidence section may face the same access limitation, and no independent verification path is provided | Minor | Evidence Matrix: "I-28, I-32 | Claude Code context compaction bug reports (Anthropic GitHub, multiple independent users; direct URLs not available in synthesis evidence catalog; readers should verify in synthesis.md evidence section)" | Evidence Quality / Traceability |

---

## S-012: FMEA

**Execution ID:** FM-I2
**Protocol:** Systematic bottom-up failure mode enumeration with RPN scoring (Severity × Occurrence × Detection, each 1–10).

### Component Decomposition

R2's analytical components:
1. Confidence Scale Definition (scale operationalization)
2. D2 Directional Claim (structured vs. blunt prohibition, MEDIUM)
3. D5 Vendor Practice Evidence (HIGH observational)
4. Backup Analytical Frame (hierarchy fallback)
5. Parsimony Analysis (Explanation 1/2/3 assignment)
6. Practitioner Guidance (PG-001–PG-005)
7. Circularity Disclosure (structural limitation)
8. Phase 2 Abandonment Guard

### FMEA Table

| Component | Failure Mode | Effect | S | O | D | RPN | Mitigation | ID |
|-----------|-------------|--------|---|---|---|-----|-----------|-----|
| D2 Directional Claim | A-23 inaccessibility converts T1-unverified to not-T1; D2 MEDIUM becomes LOW | D2's primary directional finding collapses; entire hallucination prevention claim becomes LOW confidence | 8 | 6 | 5 | 240 | Verify A-23 access before accepting D2 at MEDIUM; downgrade in current document | FM-001-I2 |
| Confidence Scale Application | D3 confound classification inconsistency (5 confounds claimed; "uncontrolled" not demonstrated for all 5) | Scale application appears rigorous but may not be — D3 LOW label may be assigned on incorrect grounds | 5 | 4 | 6 | 120 | Demonstrate which confounds are uncontrolled vs. partially controlled; revise label accordingly | FM-002-I2 |
| Parsimony Analysis | Explanation 2 assumption (a) is unverified empirical claim — assumption count may be 3, not 2 | Parsimony finding inverts: Explanations 1 and 2 are equally parsimonious; "co-null hypothesis" framing remains valid but the claimed parsimony differential disappears | 6 | 5 | 5 | 150 | Provide citation for "policy documents conventionally use prohibitive vocabulary" or revise parsimony claim | FM-003-I2 |
| Circularity Disclosure | Disclosure is only in Assumption A-002; readers who stop at L1 Technical Findings never encounter it | D5's HIGH confidence label is relied on by downstream decision-makers who haven't read the structural limitation | 9 | 7 | 3 | 189 | Add circularity caveat to D5 verdict and L0 executive summary | FM-004-I2 |
| PG-003 Recommendation | Explanation 2 being correct nullifies evidential basis of PG-003; practitioners implement unfounded guidance | Working practice becomes entrenched even if Phase 2 shows no framing effect | 7 | 5 | 6 | 210 | Explicitly condition PG-003 on Explanation 2 being less likely; or note that PG-003's evidential basis depends on Explanation 1/3 being more likely than Explanation 2 | FM-005-I2 |
| Phase 2 Abandonment Guard | Section does not address mixed/inconclusive Phase 2 results | Practitioners have no guidance if Phase 2 produces ambiguous outcomes | 6 | 7 | 7 | 294 | Add fourth scenario: Phase 2 produces mixed results; provide guidance for practitioners under that outcome | FM-006-I2 (= PM-001-I2) |

**Highest RPN items for I2:**
1. FM-006-I2 (Phase 2 inconclusive scenario missing) — RPN 294
2. FM-001-I2 (A-23 inaccessibility collapses D2) — RPN 240
3. FM-005-I2 (PG-003 basis depends on Explanation 1/3 dominance) — RPN 210
4. FM-004-I2 (Circularity disclosure not visible from L0) — RPN 189

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| FM-001-I2 | A-23 inaccessibility failure (RPN 240) — D2 MEDIUM claim collapses to LOW if A-23 cannot be accessed and confirmed as T1; this is the highest-impact single-point-of-failure for R2's directional claims | Major | D2 Hallucination Prevention verdict: "MEDIUM for structured techniques vs. blunt prohibition"; A-23 footnote: "T1-unverified (EMNLP 2025, no preprint/DOI available)" | Evidence Quality |

---

## S-013: Inversion

**Execution ID:** IN-I2
**Protocol:** Invert the goals of the analysis. Ask: "How would we guarantee this analysis fails to inform practitioners correctly?" Then verify those conditions are absent.

### Goal Inversion

**Stated goal:** Correctly characterize the evidential weight for positive vs. negative prompting effectiveness so practitioners can make informed decisions.

**Inverted goal:** Ensure practitioners cannot make informed decisions — the analysis is opaque, overclaims, underclaims, or provides guidance that will be wrong after Phase 2.

### Anti-Goal Conditions — Are They Present?

**Anti-condition 1:** Use a confidence scale that is internally inconsistent so practitioners cannot trust confidence labels.
- **Verification:** D2's MEDIUM label applies to A-23 (T1-unverified) despite the scale requiring "confirmed T1 or T2 study" for MEDIUM. Anti-condition 1 is PARTIALLY PRESENT. The scale is defined correctly; the application is inconsistent.
- **Finding:** IN-001-I2 (same as DA-001-I2, CV-001-I2 — convergent from multiple strategies)

**Anti-condition 2:** Make the most critical structural limitation invisible to the most readers.
- **Verification:** The circularity disclosure is in Assumption A-002, not in L0 or D5. Anti-condition 2 is PRESENT.
- **Finding:** RT-001-I2 (convergent from multiple strategies)

**Anti-condition 3:** Provide practitioner guidance whose evidential basis disappears under one of the three competing explanations for vendor behavior.
- **Verification:** PG-003 is based on VS-001–VS-004 vendor self-practice evidence. If Explanation 2 (genre convention) is correct, VS-001–VS-004 carry zero evidential weight for effectiveness. PG-003's basis disappears. Anti-condition 3 is PRESENT — but the document does acknowledge this in the Explanation 2 severity note (DA-002-I1 resolution).

**Anti-condition 4:** Invert the temporal direction of Phase 2 dependency — ensure practitioners cannot act now AND cannot act after Phase 2.
- **Verification:** PG-001 through PG-005 are unconditional. Practitioners CAN act now. Anti-condition 4 is ABSENT. The document correctly addresses this.

**Anti-condition 5:** Fail to account for the scenario where "structured negative at ranks 9–11 performs equally to structured positive" — the null result for Phase 2.
- **Verification:** The analysis designates ranks 9–11 vs. structured positive as "UNTESTED" but does not explore: if Phase 2 finds no difference, what should practitioners conclude? The PG-003 working practice would then be unjustified by experimental evidence. The null scenario for Phase 2 is not addressed in the practitioner guidance or recommendations.
- **Finding:** IN-001-I2

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| IN-001-I2 | The inversion of the document's directional premise — "what if Phase 2 finds no framing advantage?" — is not addressed in the practitioner guidance or recommendations; PG-003 vocabulary tier design lacks a revision path if Phase 2 produces a null framing result | Major | PG-003: "Recommended working practice (pending Phase 2 validation): HARD enforcement tier: MUST/NEVER/MUST NOT + explicit consequence" — no statement of what practitioners should do if Phase 2 finds no framing effect at ranks 9–11 | Completeness / Actionability |
| IN-002-I2 | Assumptions section uses L-001 through L-004 but these are not cross-referenced from the dimension sections that generate findings dependent on those limitations — readers of D3 and D4 do not see that L-001 (no controlled comparison for D3/D4) applies to their dimension | Minor | D3 "Observational Note" section does not reference L-001; D4 "Observational Note" does not reference L-001 | Traceability |

---

## S-014: LLM-as-Judge

**Execution ID:** LJ-I2
**Leniency bias counteraction:** ACTIVE. C4 threshold is 0.95. I1 scored 0.743. R2 has substantially addressed I1 findings. The score must reflect genuine improvement without rewarding effort alone.

### Anti-Leniency Statement

Specific biases to counteract in this evaluation:
1. NEVER inflate a score because the document is long or detailed — length is not quality.
2. NEVER excuse a known inconsistency (A-23 T1-unverified vs. MEDIUM confidence label) because it is flagged in the document.
3. NEVER give credit for a disclosed limitation that should have been fixed rather than disclosed.
4. NEVER round up a score that is below 0.95 on any dimension to reach the passing threshold.

### Dimension Scoring

#### Dimension 1: Completeness (Weight: 0.20)

**Rubric questions:**
- Are all required sections present? YES — all 5 dimensions, confidence scale, backup frame, practitioner guidance, Phase 2 guard, revision log.
- Are there unexplored edge cases? YES — the inconclusive Phase 2 scenario (PM-001-I2) is absent. The null framing result scenario is not addressed (IN-001-I2). The "what if Explanation 2 is correct" implication for PG-003 is acknowledged but not fully addressed.
- Are all critical findings from I1 addressed? YES (6/7 genuinely; 1 partially).

**Score rationale:** The document is substantially complete. Two meaningful gaps remain: inconclusive Phase 2 scenario and PG-003 revision path under null framing result. These reduce from what would otherwise be a near-perfect completeness score.

**Raw score: 0.82** (Missing two meaningful scenarios; all major structural sections present)

#### Dimension 2: Internal Consistency (Weight: 0.20)

**Rubric questions:**
- Do sections contradict each other? YES — D2 MEDIUM claim contradicts confidence scale definition (DA-001-I2, CV-001-I2).
- Are definitions used consistently? MOSTLY — confidence scale is generally applied correctly; the D2 application is inconsistent.
- Do examples match specifications? YES — hierarchy examples are consistent with the hierarchy definition.

**Score rationale:** The A-23/D2 internal inconsistency is a material error. The confidence scale was introduced specifically to address the undefined confidence labels in I1 (FM-002-I1, highest RPN). Introducing a confidence scale and then applying it inconsistently in the primary directional finding is a significant consistency failure. The parsimony analysis also has a partial consistency issue (assumption count for Explanation 2).

**Raw score: 0.72** (Material inconsistency in confidence scale application at D2; parsimony analysis partially inconsistent)

#### Dimension 3: Methodological Rigor (Weight: 0.20)

**Rubric questions:**
- Was prescribed procedure followed? YES — 5-dimension framework applied; evidence assembled; hierarchy used; verdicts issued with confidence levels.
- Are shortcuts or assumptions unjustified? MOSTLY JUSTIFIED — with the exception that no alternative analytical frameworks are enumerated (LJ-001-I2).
- Is the analytical method appropriate? YES — comparative analysis across 5 dimensions using evidence tiers is appropriate.
- Is the circularity adequately addressed? PARTIALLY — acknowledged but not visible from L0.

**Score rationale:** The methodological rigor is substantially improved over I1. The hierarchy validity disclosure, the backup frame, the parsimony analysis, and the reflexivity assessment all demonstrate genuine rigor. The two remaining gaps (circularity not in L0; no alternative frameworks enumerated) are meaningful but not fatal to the methodology.

**Raw score: 0.81** (Strong methodological rigor with two localized gaps)

#### Dimension 4: Evidence Quality (Weight: 0.15)

**Rubric questions:**
- Are claims backed by specific evidence? YES — evidence table is comprehensive with tier assignments.
- Are references accurate and sufficient? MOSTLY — A-23 is flagged as T1-unverified, A-31 is qualified, I-28/I-32 access noted.
- Is the T1-unverified status of A-23 adequately handled? NO — D2 MEDIUM claim depends on A-23 as T1, but T1-unverified does not satisfy the MEDIUM definition.

**Score rationale:** The evidence quality table is comprehensive and well-organized. The A-23 handling is the primary failure: flagging a source as T1-unverified while simultaneously relying on it as the T1 evidence for a MEDIUM-confidence claim is an evidence quality failure. The I-28/I-32 URL availability issue is minor.

**Raw score: 0.75** (Material evidence quality issue at D2 due to A-23 treatment)

#### Dimension 5: Actionability (Weight: 0.15)

**Rubric questions:**
- Are recommendations concrete? YES — PG-001 through PG-005 are specific, evidence-cited, unconditional.
- Can someone implement them without guessing? YES — PG-003 specifies exact vocabulary tier design.
- Is there guidance for ambiguous outcomes? NO — no guidance if Phase 2 is inconclusive (PM-001-I2); no revision path if Phase 2 finds null framing effect (IN-001-I2).

**Score rationale:** The practitioner guidance is a genuine and substantial improvement over I1 (which had none). The unconditional framing (not contingent on Phase 2) is correct. The gap is in forward guidance: practitioners need guidance not only for "before Phase 2" but also for "after Phase 2 if inconclusive." The document is actionable for the pre-Phase 2 scenario but silent on the post-inconclusive-Phase 2 scenario.

**Raw score: 0.80** (Substantially actionable with meaningful gap in Phase 2 outcome scenarios)

#### Dimension 6: Traceability (Weight: 0.10)

**Rubric questions:**
- Are source documents linked? YES — evidence matrix provides tier, source ID, and key claim for all evidence.
- Are decisions traceable to requirements? YES — revision log traces all I2 changes to I1 findings.
- Are evidence paths for T5 observations verifiable? YES — EO-001, EO-002, EO-003 link to adversary-gate.md.
- Is the circularity disclosure traceable? YES — Assumption A-002 is present; traceability exists within the document; the gap is visibility, not traceability.

**Score rationale:** Traceability is strong. The revision log is comprehensive. Source paths are provided. The I-28/I-32 URL gap is minor (alternative verification path provided). This is the dimension most improved over I1.

**Raw score: 0.87** (Strong traceability; minor gap in I-28/I-32 URL verification path)

### Weighted Composite Score

| Dimension | Weight | Raw Score | Weighted |
|-----------|--------|-----------|---------|
| Completeness | 0.20 | 0.82 | 0.164 |
| Internal Consistency | 0.20 | 0.72 | 0.144 |
| Methodological Rigor | 0.20 | 0.81 | 0.162 |
| Evidence Quality | 0.15 | 0.75 | 0.113 |
| Actionability | 0.15 | 0.80 | 0.120 |
| Traceability | 0.10 | 0.87 | 0.087 |
| **TOTAL** | **1.00** | | **0.790** |

### Quality Gate Assessment

**I2 Score: 0.790**
**C4 Threshold: >= 0.95**
**Result: REJECTED**

**Score improvement from I1:** +0.047 (0.743 → 0.790). Genuine improvement — the I1 Critical findings are substantially addressed. However, R2 introduced a new material inconsistency (D2 MEDIUM claim vs. A-23 T1-unverified status) that depresses the Internal Consistency and Evidence Quality dimensions significantly.

**What would bring this to 0.95:**
- Resolving DA-001-I2/CV-001-I2: Downgrade D2 MEDIUM to LOW if A-23 cannot be confirmed, OR confirm A-23 access and upgrade to T1-verified. This alone would improve Internal Consistency from 0.72 to approximately 0.88 and Evidence Quality from 0.75 to approximately 0.87.
- Adding RT-001-I2 circularity caveat to L0 and D5. This would improve Completeness from 0.82 to approximately 0.87 and Methodological Rigor from 0.81 to approximately 0.87.
- Adding Phase 2 inconclusive scenario guidance (PM-001-I2, IN-001-I2). This would improve Completeness from 0.82 to approximately 0.90 and Actionability from 0.80 to approximately 0.88.

**Estimated score after addressing all Major I2 findings (R3):** Completeness ~0.90, Internal Consistency ~0.88, Methodological Rigor ~0.87, Evidence Quality ~0.87, Actionability ~0.88, Traceability ~0.89. Estimated composite: ~0.88 — still below 0.95. The path to 0.95 requires addressing all Major and all Minor findings.

**Key observation:** The highest-impact single fix is resolving the A-23/D2 inconsistency. If A-23 access can be confirmed (T1-verified), the Internal Consistency score recovers substantially. If A-23 access cannot be confirmed and D2 is downgraded to LOW, the document's directional claim for hallucination prevention weakens but the document becomes internally consistent.

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| LJ-001-I2 | No alternative analytical frameworks are enumerated to justify preferring the 12-level hierarchy over simpler alternatives — the methodological choice is disclosed as internally generated but the choice among alternatives is not demonstrated | Major | Cross-Cutting section: "12-Level Effectiveness Hierarchy is a narrative synthesis product"; no section evaluating alternative frameworks (e.g., simple positive/negative binary, tier-based approach not hierarchy-based) | Methodological Rigor |

---

## Execution Statistics

- **Total Findings:** 19
- **Critical:** 0
- **Major:** 9 (SR-001-I2, SM-001-I2, DA-001-I2, DA-002-I2, PM-001-I2, RT-001-I2, CV-001-I2, FM-001-I2, IN-001-I2, LJ-001-I2)
- **Minor:** 10 (SR-002-I2, SR-003-I2, SM-002-I2, DA-003-I2, PM-002-I2, CC-001-I2, CV-002-I2, FM-002-I2 [merged with SR-001-I2], IN-002-I2)
- **Protocol Steps Completed:** 10 of 10

**Note on count:** FM-001-I2 and CV-001-I2 and DA-001-I2 converge on the same underlying issue (A-23/D2 inconsistency) identified from three different strategy perspectives. They are counted as three separate findings because they target the issue from distinct analytical angles (FMEA risk analysis, Red Team evidentiary attack, Devil's Advocate logical challenge). The resolution addresses all three simultaneously.

### Finding Convergence Map (High-Signal Issues)

The following issues were independently identified by multiple strategies — convergence indicates high confidence:

| Issue | Identified By | Severity |
|-------|--------------|---------|
| A-23 T1-unverified vs. D2 MEDIUM inconsistency | S-010, S-002, S-001, S-012, S-014 | Major |
| Circularity not visible from L0 | S-004, S-001, S-012, S-014 | Major |
| Phase 2 inconclusive scenario missing | S-004, S-013, S-014 | Major |
| Parsimony analysis assumption (a) unverified | S-002, S-011, S-012 | Major |
| PG-003 revision path absent under null framing result | S-013, S-014, S-004 | Major |

### I2 vs. I1 Comparison

| Metric | I1 | I2 |
|--------|-----|-----|
| Critical findings | 7 | 0 |
| Major findings | 19 | 9 (10 unique findings; some merged) |
| Minor findings | 9 | 10 |
| Composite score | 0.743 | 0.790 |
| Quality gate result | REJECTED | REJECTED |
| Score improvement | — | +0.047 |

**Primary blocker for I3:** The A-23/D2 consistency issue is the highest-value single fix. If A-23 access can be confirmed, Internal Consistency and Evidence Quality scores recover substantially. The second-highest-value fix is adding the circularity caveat to L0 and D5. The third is addressing Phase 2 inconclusive scenario guidance.

### Required for I3 (in priority order)

1. **[BLOCKER]** Resolve A-23 status: confirm access (upgrade to T1-verified) OR downgrade D2 from MEDIUM to LOW throughout document. Update confidence bounds table and PS Integration key findings accordingly.
2. **[BLOCKER]** Add circularity caveat to L0 executive summary and D5 verdict. The structural limitation must be visible to readers who read only the executive summary.
3. **[MAJOR]** Add Phase 2 inconclusive scenario to "Why Observational Evidence Does Not Replace Phase 2" section and to Practitioner Guidance section.
4. **[MAJOR]** Add PG-003 revision path: what should practitioners do if Phase 2 finds no framing advantage at ranks 9–11?
5. **[MAJOR]** Revise parsimony analysis: either provide citation for "policy documents conventionally use prohibitive vocabulary" (Explanation 2, Assumption a) or revise to "Explanations 1 and 2 have equal assumption counts."
6. **[MAJOR]** Enumerate at least one alternative analytical framework considered and rejected for the 12-level hierarchy approach.
7. **[MINOR]** Assign confidence level to the "context compaction may reverse D1" claim (DA-003-I2).
8. **[MINOR]** Add cross-references from D3/D4 sections to L-001 (IN-002-I2).
9. **[MINOR]** Revise Revision Log RT-001-I1 entry from "Critical | Circularity disclosure strengthened" to "Critical | PARTIALLY resolved — disclosure strengthened but not visible from L0; converted to Major finding in I2."
10. **[MINOR]** Revise A-16 REMOVAL NOTICE to remove identifying information (author names, venue) (CC-001-I2).

---

*adv-executor | C4 Tournament | PROJ-014 | 2026-02-27*
*All 10 strategies executed per H-16 order: S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013, S-014*
*Quality gate: REJECTED (0.790 < 0.95 C4 threshold)*
*Critical I1 findings resolved: 6/7 genuine (RT-001-I1 partially resolved, converted to Major I2)*
*New findings in I2: 0 Critical, 9 Major, 10 Minor*
*Constitutional compliance: P-001 (all findings evidence-cited), P-002 (report persisted to file), P-022 (score not inflated; rejection stated explicitly)*
