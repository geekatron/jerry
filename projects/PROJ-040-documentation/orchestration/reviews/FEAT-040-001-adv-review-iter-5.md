# Adversarial Review Report: FEAT-040-001 JTBD Analysis (Iter-5)

## Execution Context

- **Strategy Set:** S-007, S-002, S-014, S-004, S-012, S-013 (C3 required)
- **Deliverable:** `projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-001/ux-jtbd-analyst-output.md` (iter-5)
- **Criticality:** C3
- **Threshold:** 0.92
- **Iteration:** 5 of 7
- **Executed:** 2026-04-17
- **Self-Reported Score:** 0.922 (claimed PASS)

---

## Findings Summary

| ID | Strategy | Severity | Finding | Section |
|----|----------|----------|---------|---------|
| FM-001-iter5 | S-012 | Critical | Opportunity score arithmetic incorrect for Cat 3, Cat 4, Cat 5 — formula correctly stated but not correctly applied | Top 5 table + Category Derivations |
| FM-002-iter5 | S-012 | Major | ±2 band values inconsistent between Top 5 table and Category Derivations section for Cat 3, 4, 5 | Top 5 table vs L2 Derivations |
| FM-003-iter5 | S-012 | Major | Cat 3 derivation band "9–15" self-inconsistent with its stated score (13±2 = 11–15, not 9–15) | L2 Category Derivations — Cat 3 |
| PM-001-iter5 | S-004 | Major | Incorrect Cat 4 opportunity score (12 vs correct 15) causes systematic under-prioritization of UX Suite in tier analysis and downstream XP-01/XP-02 consumption | Top 5 + Tier-Clustering analysis |
| CC-001-iter5 | S-007 | Minor | XP-04 STOP GATE responsible party remains an unassigned placeholder ("[assign XP-04 owner]") | L1 Switch Force Analysis — STOP GATE |
| IN-001-iter5 | S-013 | Minor | Cat 3 ±2 range in derivation section implies Opp score of 13 but formula gives 14; tier-clustering Tier A/B assignment is based on the wrong score | L2 Category Derivations — Cat 3 |

---

## Detailed Findings

### FM-001-iter5: Opportunity Score Arithmetic Incorrect for Cat 3, Cat 4, Cat 5 [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Top 5 Job Categories table; L2 Category Opportunity Score Derivations |
| **Strategy Step** | S-012 FMEA — component verification of formula application |

**Evidence:**

The document states the Ulwick ODI formula as:
```
Opportunity Score = Importance + max(0, Importance − Satisfaction)
```

Applying this formula to the document's own I and S values:

| Category | I | S | Formula Applied | Stated Score | Error |
|----------|---|---|-----------------|--------------|-------|
| Cat 1 Structured Cognition | 9 | 3 | 9 + max(0, 9-3) = 9+6 = **15** | 15 | CORRECT |
| Cat 2 SDLC Methodology Chain | 8 | 2 | 8 + max(0, 8-2) = 8+6 = **14** | 14 | CORRECT |
| Cat 3 Workflow Management | 9 | 4 | 9 + max(0, 9-4) = 9+5 = **14** | 13 | **-1 ERROR** |
| Cat 4 UX Methodology Suite | 8 | 1 | 8 + max(0, 8-1) = 8+7 = **15** | 12 | **-3 ERROR** |
| Cat 5 Specialized Professional | 8 | 3 | 8 + max(0, 8-3) = 8+5 = **13** | 11 | **-2 ERROR** |

**Corrected ranking under proper arithmetic:**

| Rank | Category | Correct Opp Score | Stated Score |
|------|----------|-------------------|--------------|
| 1 (tie) | Cat 1 Structured Cognition | 15 | 15 |
| 1 (tie) | Cat 4 UX Methodology Suite | 15 | 12 |
| 3 (tie) | Cat 2 SDLC Methodology Chain | 14 | 14 |
| 3 (tie) | Cat 3 Workflow Management | 14 | 13 |
| 5 | Cat 5 Specialized Professional | 13 | 11 |

**Analysis:**

The formula is correctly stated in the Methodology section. Cat 1 and Cat 2 compute correctly. The errors in Cat 3–5 are arithmetic mistakes, not methodological ones. The consequences are severe:

1. Cat 4 (UX Suite) has a correct score of 15, tying Cat 1 for first place — not rank 4. The analysis that places it in Tier B (swappable with Cat 3) is incorrect. Cat 4 belongs in Tier A with Cat 1.
2. Cat 3 (Workflow Management) scores 14, not 13, tying Cat 2 — the tier separation between Tier A and Tier B shifts.
3. The tier-clustering analysis ("Tier A: Cat 1-2 stable top; Tier B: Cat 3-4 may swap") is inverted from what the correct arithmetic produces.
4. The self-score of 0.922 cannot be defensible given this error in the deliverable's central metric.

This finding was not raised in any prior iteration (iter-1 through iter-4). The iter-4 review accepted Cat 3=13, Cat 4=12, Cat 5=11 without arithmetic verification. This is a new Critical finding surfaced by S-012 FMEA's systematic formula-application verification.

**Recommendation:**

Recompute all five opportunity scores using the stated formula. Apply correct scores:
- Cat 3: I=9, S=4 → Opp 14
- Cat 4: I=8, S=1 → Opp 15
- Cat 5: I=8, S=3 → Opp 13

Update the Top 5 table, ±2 bands, tier-clustering analysis, L0 Executive Summary, and all downstream references. The corrected ranking places Cat 4 (UX Suite) as a Tier A priority alongside Cat 1, not a Tier B middle-priority item.

---

### FM-002-iter5: ±2 Band Inconsistency Between Sections [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Top 5 Job Categories table vs L2 Category Opportunity Score Derivations |
| **Strategy Step** | S-012 FMEA — cross-section consistency check |

**Evidence:**

The Top 5 table and the L2 Category Derivations section state different ±2 bands for the same categories:

| Category | Band in Top 5 Table | Band in L2 Derivations | ±2 of Stated Score |
|----------|--------------------|-----------------------|--------------------|
| Cat 3 (Opp 13) | 11–15 | 9–15 | 11–15 |
| Cat 4 (Opp 12) | 10–14 | 8–14 | 10–14 |
| Cat 5 (Opp 11) | 9–13 | 7–13 | 9–13 |

The Top 5 table bands are arithmetically correct for the (wrong) stated scores. The Category Derivations bands are each expanded by 2 at the lower end — a consistent "extra -2" that has no basis in the methodology.

**Analysis:**

A downstream consumer reconciling the Top 5 table against the Category Derivations section will find contradictory band ranges. The Tier C analysis ("Cat 5 band 9–13 straddles the UNDERSERVED threshold") relies on the Top 5 table band; the derivation section shows 7–13, suggesting Cat 5 falls even further below threshold. These contradictions undermine trust in the entire quantitative framework even before the arithmetic errors in FM-001-iter5 are corrected.

**Recommendation:**

After correcting Opp scores per FM-001-iter5, apply ±2 consistently throughout both sections. All band references in the document must agree.

---

### FM-003-iter5: Cat 3 Derivation Band Self-Inconsistent [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L2 Category Opportunity Score Derivations — Cat 3 Workflow Management |
| **Strategy Step** | S-012 FMEA — element-level verification |

**Evidence:**

The Cat 3 derivation box header reads: "Cat 3 Workflow Management — Opp 13 [I=9, S=4, ±2 band 9–15]"

If Opp = 13 and uncertainty = ±2, then the band is 13-2=11 to 13+2=15, i.e., 11–15. The derivation box states 9–15. The lower bound is 2 units below the correct value (11) without explanation.

The same "extra -2 at lower bound" pattern appears in Cat 4 (10–14 correct for score 12, states 8–14) and Cat 5 (9–13 correct for score 11, states 7–13). This is a systematic application of a different uncertainty rule than stated (possibly ±3 at the lower bound only, or ±2 applied twice to the lower bound) that is never documented.

**Analysis:**

Even accepting the (incorrect) stated opportunity scores, the ±2 bands in the derivation section are not arithmetically consistent with the stated uncertainty rule. This is an independent consistency failure from FM-001-iter5. It was masked in the Top 5 table (which computes ±2 correctly from the stated scores) but exposed in the derivation section.

**Recommendation:**

Apply ±2 uniformly: lower bound = stated score - 2; upper bound = stated score + 2. No exceptions. After FM-001-iter5 is corrected, recalculate all bands from corrected scores.

---

### PM-001-iter5: Systematic Under-Prioritization of Cat 4 UX Suite [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Top 5 tier-clustering analysis; L0 Executive Summary |
| **Strategy Step** | S-004 Pre-Mortem — downstream failure scenario |

**Evidence:**

The tier-clustering analysis states:
> "Tier A (stable top): Cat 1 (band 13–17) and Cat 2 (band 12–16) overlap but Cat 1's lower bound (13) exceeds Cat 2's lower bound (12); directionally stable as top two."
> "Tier B (middle, may swap): Cat 3 (band 11–15) and Cat 4 (band 10–14) overlap fully."

The L0 Executive Summary does not mention Cat 4 as a high-priority item. The SDLC Methodology Chain (Cat 2) is called out as "Highest-value undocumented cluster" with a recommended doc sequence.

**Analysis:**

With corrected arithmetic (Cat 4 = 15, tied with Cat 1), the pre-mortem failure scenario is:

1. XP-01 (Kano) allocates research budget based on this analysis, placing Cat 4 (UX Suite) at priority 4 under Cat 1, 2, and 3.
2. In reality, Cat 4 ties Cat 1 at score 15 and should be co-equal in Tier A.
3. The 11-skill UX Suite — the category with zero documentation coverage across all 11 skills and the highest discovery barrier — receives systematically lower investment than warranted.
4. When Cat 4 documentation is eventually identified as the correct Tier A priority, previous resource allocation decisions based on this analysis will require retrospective correction.

This is a pre-mortem failure with concrete downstream resource allocation consequences, caused entirely by arithmetic errors.

**Recommendation:**

After FM-001-iter5 correction: revise tier-clustering to place Cat 4 in Tier A alongside Cat 1. Update L0 Executive Summary to reflect Cat 4's true priority position.

---

### CC-001-iter5: STOP GATE Responsible Party Unassigned [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | L1 Switch Force Analysis — XP-04 Consumption Stop Gate |
| **Strategy Step** | S-007 Constitutional AI — P-001 accuracy check |

**Evidence:**

The STOP GATE block reads: "Gate status: OPEN. Responsible party: [assign XP-04 owner]."

The Validation Required section similarly omits a named owner for the A4/A6 validation protocol row.

**Analysis:**

The STOP GATE is operationally functional as a blocking signal. However, leaving the responsible party as a placeholder creates an accountability gap: when XP-04 is invoked, there is no named party to check with before proceeding. In a multi-agent pipeline, agents reading this document will see OPEN but have no routing target for escalation. The gate remains unresolvable until an owner is assigned.

This is a minor traceability gap (P-004) — the gate mechanism works, but the handoff target is incomplete.

**Recommendation:**

Replace "[assign XP-04 owner]" with either: (a) a named agent or persona responsible for XP-04 positioning work, or (b) a structural reference: "Responsible party: XP-04 work item owner (assign in worktracker before XP-04 kickoff)."

---

### IN-001-iter5: Tier-Clustering Analysis Derived from Incorrect Scores [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor (independent of FM-001-iter5 — documents the Inversion consequence) |
| **Section** | Top 5 ranking stability + tier-clustering |
| **Strategy Step** | S-013 Inversion — assumption stress-test |

**Evidence:**

Inversion test: "What if the opportunity scores are wrong?" Applied to the tier-clustering premise: "Cat 1 (band 13–17) and Cat 2 (band 12–16) are directionally stable as top two."

Inverting the assumption that scores are correct → Cat 4 correct score 15 ties Cat 1. Cat 1-2 are NOT the only Tier A members.

**Analysis:**

The tier-clustering analysis was a genuine improvement over iter-4's undifferentiated ranking. The logic (overlapping bands → tier grouping) is sound. However, the entire tier analysis is downstream of incorrect input values. The Inversion technique surfaces this: the analysis is internally valid given its inputs, but the inputs are incorrect, which propagates through all tier claims.

This finding is distinct from FM-001-iter5 in that it specifically addresses the assumption "my input scores are accurate" which the tier-clustering never stress-tested. The document should include: "Tier analysis validity depends on the accuracy of underlying I/S value assignments. I/S values are ±2 uncertain AND the Opp formula application has not been independently verified." After FM-001-iter5 correction, the tier analysis should note this dependency explicitly.

**Recommendation:**

After arithmetic correction, add a note to tier-clustering: "Tier assignments are contingent on the accuracy of I/S assignments (±2 stated uncertainty) AND on correct formula application. The formula application has been independently verified by iter-5 adversarial review."

---

## Probe Results

| Probe | Result |
|-------|--------|
| 1. STOP GATE actually blocking — checklist executable? | PASS — gate is present, prominent, checklist has numbered checkboxes; minor gap: responsible party unassigned (CC-001-iter5) |
| 2. SKILL.md citations per force: real quotes or placeholders? | PASS — genuine citations with version numbers and quoted text in all 5 force tables |
| 3. I/S derivation math: visible and defensible? | FAIL — derivation procedure visible and documented; arithmetic incorrect for Cat 3, 4, 5 (FM-001-iter5 Critical) |
| 4. Tier-clustering: correctly applied to uncertainty? | FAIL — logic is sound but input scores are wrong; tier assignments incorrect (PM-001-iter5 + IN-001-iter5) |
| 5. BLOCKED categories sequencing: actionable? | PASS — Cat 2 sequence (4 steps) and Cat 4 sequence (4 steps with wave logic) both concrete and correctly ordered |
| 6. Regressions from iter-4 passing content? | PASS — 30-skill table, actor differentiation, navigation table, switch trigger citations all intact |
| 7. Self-score 0.922 defensible? | FAIL — arithmetic errors in 3/5 central metrics; independent composite 0.844; self-score inflated by ~0.078 |

---

## S-014 Composite Scoring

### Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Basis |
|-----------|--------|-------|----------|----------------|
| Completeness | 0.20 | 0.88 | 0.176 | All sections present, citations per force, derivation boxes; arithmetic errors in 3/5 Opp scores create substantive gap in central metric completeness |
| Internal Consistency | 0.20 | 0.72 | 0.144 | Top 5 table and Category Derivations disagree on ±2 bands (FM-002-iter5); Cat 3 band self-inconsistent within derivation box (FM-003-iter5); formula stated correctly but applied incorrectly for Cat 3/4/5; tier-clustering contradicted by correct arithmetic |
| Methodological Rigor | 0.20 | 0.82 | 0.164 | Decision Matrix present; per-category derivations shown; force citations added; but formula application failure is a methodology execution failure despite correct framework documentation |
| Evidence Quality | 0.15 | 0.91 | 0.137 | Genuine improvement: SKILL.md version+quote citations throughout force tables; bias disclosures (A3 authorship, satisfaction proxy) explicit and specific; synthesis judgment inventory complete |
| Actionability | 0.15 | 0.87 | 0.131 | BLOCKED category sequences concrete; A4/A6 stop gate executable; tier-A/B/C guidance present; Cat 4 wrong score (12 vs correct 15) sends incorrect priority signal to downstream XP consumers |
| Traceability | 0.10 | 0.92 | 0.092 | SKILL.md citations with version numbers throughout; 11 synthesis judgments; I/S derivation steps traceable; formula source cited |
| **TOTAL** | **1.00** | | **0.844** | |

**Verification:** (0.88×0.20) + (0.72×0.20) + (0.82×0.20) + (0.91×0.15) + (0.87×0.15) + (0.92×0.10)
= 0.176 + 0.144 + 0.164 + 0.137 + 0.131 + 0.092 = **0.844**

**Weighted Composite: 0.844**

**Verdict: REJECTED (0.844 < 0.92 threshold) — regression from iter-4 (0.873)**

---

## Self-Score Defensibility Assessment

Self-reported 0.922 is NOT defensible. Independent composite: 0.844 (delta: -0.078).

The self-review correctly closed all 9 iter-4 blockers. The force citations, I/S derivation boxes, tier-clustering, sequencing, and STOP gate are genuine improvements. However, the arithmetic verification step — checking that each Opp score follows from the stated formula — was not performed. Opportunity scores for Cat 3, 4, 5 are each wrong by -1, -3, and -2 respectively. The errors are not consistent with any alternative formula; they appear to be transcription or calculation errors introduced at an unrecorded point in the revision history.

The self-score was achievable if the arithmetic had been verified. A single pass of formula-application checking would have caught FM-001-iter5.

The 0.844 composite is a regression from iter-4 (0.873) primarily because the arithmetic errors introduce new Internal Consistency failures not present in iter-4 (which accepted the wrong scores without surfacing them as errors).

---

## Iter-6 Priority Actions

**P0 (Critical — must fix before PASS):**

1. **FM-001-iter5:** Recompute Cat 3 (→14), Cat 4 (→15), Cat 5 (→13) using the stated formula I + max(0, I-S). Update Top 5 table, tier-clustering, L0 summary.

**P1 (Major — required for 0.92):**

2. **FM-002-iter5:** Reconcile ±2 bands between Top 5 table and Category Derivations section. Apply uniform: lower = score-2, upper = score+2.
3. **FM-003-iter5:** Fix Cat 3 derivation band from "9–15" to correct value (computed from corrected score).
4. **PM-001-iter5:** After arithmetic correction, revise tier-clustering to place Cat 4 in Tier A. Update L0 to call out UX Suite as co-equal Tier A priority with Structured Cognition. Revise "Highest-value undocumented cluster" language accordingly.

**P2 (Minor — recommended):**

5. **CC-001-iter5:** Assign or structurally reference responsible party for A4/A6 STOP GATE.
6. **IN-001-iter5:** Add post-correction note to tier-clustering acknowledging that tier assignments are contingent on verified formula application.

---

## Execution Statistics

- **Total Findings:** 6
- **Critical:** 1 (FM-001-iter5)
- **Major:** 3 (FM-002-iter5, FM-003-iter5, PM-001-iter5)
- **Minor:** 2 (CC-001-iter5, IN-001-iter5)
- **Protocol Steps Completed:** S-007 (5/5), S-002 (5/5), S-004 (4 failure scenarios), S-012 (6 FMEA rows), S-013 (2 inversions), S-014 (6 dimensions + composite)

---

*Iter-5 adversarial review. Iter-4 blockers: all 9 closed (PASS on prior blockers). New Critical: FM-001-iter5 arithmetic error invalidates Cat 3–5 scores and tier-clustering. Composite: 0.844. Verdict: REJECTED (regression from 0.873). Iter-6 requires arithmetic correction only (1 Critical, 3 Major, 2 Minor).*
