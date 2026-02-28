# Strategy Execution Report: C4 Tournament — Supplemental Vendor Evidence Report (Iteration 2)

## Execution Context

- **Strategy:** All 10 Strategies (C4 Tournament Mode)
- **Templates:** `.context/templates/adversarial/s-{010,003,002,004,001,007,011,012,013,014}-*.md`
- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/supplemental-vendor-evidence.md`
- **Prior Findings:** `barrier-1/supplemental-adversary-findings-i1.md`
- **Executed:** 2026-02-27T00:00:00Z
- **Iteration:** I2 (second tournament pass)
- **Criticality:** C4 Critical
- **Quality Threshold:** >= 0.95 (project PLAN.md constraint)
- **I1 Composite Score:** 0.843 (REVISE)
- **I1 Critical Findings:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [I1 Critical Finding Resolution](#i1-critical-finding-resolution) | Verification of all 5 Critical findings from I1 |
| [S-010 Self-Refine](#s-010-self-refine) | Self-review findings for I2 |
| [S-003 Steelman](#s-003-steelman) | Strongest-form reconstruction |
| [S-002 Devil's Advocate](#s-002-devils-advocate) | Counter-arguments against I2 claims |
| [S-004 Pre-Mortem](#s-004-pre-mortem) | Future failure analysis of I2 |
| [S-001 Red Team](#s-001-red-team) | Adversarial attack vectors against I2 |
| [S-007 Constitutional AI](#s-007-constitutional-ai) | Governance compliance check |
| [S-011 Chain-of-Verification](#s-011-chain-of-verification) | Factual claim verification |
| [S-012 FMEA](#s-012-fmea) | Component failure mode analysis |
| [S-013 Inversion](#s-013-inversion) | Assumption stress-testing |
| [S-014 LLM-as-Judge](#s-014-llm-as-judge) | Final scoring with dimension deltas |
| [Tournament Summary](#tournament-summary) | Consolidated findings and verdict |

---

## I1 Critical Finding Resolution

**Strict verification: each I1 Critical finding is checked for resolution, partial resolution, or persistence.**

| I1 Finding | Description | Resolution Status | Evidence |
|------------|-------------|------------------|----------|
| CV-003/FM-002 | Power calculation n=50 statistically incorrect for 80% power at 15% effect | **RESOLVED** | I2 corrects to n=135 minimum with McNemar formula shown. Sample size is in defensible range. Derivation gap noted (see SR-001-i2 below) but not a repetition of the I1 error. |
| SR-001/CV-001 | Nav table said "32 instances"; body said "33" | **RESOLVED** | I2 nav table line 17 now reads "33 NEVER/MUST NOT/FORBIDDEN/DO NOT instances across 10 rule files" — matches body and NC-001 through NC-033 catalog exactly. |
| FM-003/RT-001 | Self-referential evidence base lacks independence labeling | **RESOLVED** | I2 added a dedicated "Methodological Limitations" section (L-1, L-2, L-3) with explicit "[PRACTITIONER SELF-REPORT]" labels at the head of Evidence Categories 2 and 3, and "[SESSION OBSERVATION]" labels throughout Category 3. |
| FM-005/DA-005 | Session EO-001 confounded; causal attribution not isolated | **RESOLVED** | I2 added explicit confound table to EO-001 listing 5 co-present variables (specialized agents, C4 quality gate, structured templates, Context7/WebSearch, researcher expertise) with explicit statement that session evidence cannot isolate negative prompting contribution. |
| FM-006/DA-001 | Innovator's Gap unfalsifiable; practitioner-contradicts-guidance framing potentially vacuous | **RESOLVED** | I2 relabeled "Evidence Category 4" as "Interpretive Context: The Innovator's Gap" with clear framing statement at top. VS-002 now presents three explicit alternative explanations for the recommendation/practice divergence (Explanation 1: audience specificity; Explanation 2: convention; Explanation 3: engineering discovery). |

**All 5 I1 Critical findings: RESOLVED in I2.**

---

## S-010 Self-Refine

**Strategy:** S-010 Self-Refine
**Finding Prefix:** SR
**Deliverable:** supplemental-vendor-evidence.md (Revision 2)
**Criticality:** C4

### Objectivity Check

This is an external review agent. Full objectivity applied. I2 is reviewed on its own merits, not given credit for resolving I1 issues unless the resolution is complete and accurate.

### Findings

| ID | Finding | Severity | Evidence |
|----|---------|----------|---------|
| SR-001-i2 | Power calculation derivation is incomplete — the document shows the formula yielding n=26.2, then states "adjusting for continuity correction and conservatism: n ≈ 120-135" without showing the intermediate steps. A factor of ~5x increase from continuity correction alone is not credible; the jump to 135 is in the right range but the derivation is opaque. | Major | Lines 389-390: "n ≈ (z_α/2 + z_β)² / (p_12 + p_21) ≈ (1.96 + 0.84)² / 0.30 ≈ 26.2, adjusting for continuity correction and conservatism: n ≈ 120-135 matched pairs minimum" |
| SR-002-i2 | The note "Note: the exact n depends on the empirical discordant pair proportion estimated from a pilot study" appears immediately after the n=135 calculation, which is itself derived from an assumed discordant proportion of 0.30. The document does not explain why 0.30 is the assumed discordant proportion, nor where this assumption comes from. If the true discordant proportion differs substantially from 0.30, the sample size estimate changes materially. | Minor | Line 389: "(p_12 + p_21) ≈ 0.30" — assumption not justified |
| SR-003-i2 | The Methodological Limitations section (L-1, L-2, L-3) and the Evidence Category 2 "[PRACTITIONER SELF-REPORT]" labels address the independence problem, but the Summary Evidence Table still labels JF-001 evidence tier as "Practitioner self-report" while labeling JF-002 evidence tier as "Practitioner self-report" — this is now correctly labeled and internally consistent. No finding here. | Compliant | Summary Evidence Table, lines 487-488 — labels are now accurate |
| SR-004-i2 | The "Consistent application of this ground rule" paragraph (line 45) adds a clarification about symmetric application of the absence-of-evidence principle. The paragraph is logically sound but uses the phrase "The report does not argue from absence of positive framing in HARD rules to infer that negative framing is superior." This is somewhat imprecise: the report does observe the PRESENCE of negative framing in HARD rules (not absence of positive framing) and infers that negative framing was chosen — which is a different logical move. The sentence could be misread as the report acknowledging it avoids a fallacy it is actually not committing. Minor clarity issue. | Minor | Line 45: "The report does not argue from absence of positive framing" — the report actually argues from PRESENCE of negative framing; the wording is defensible but imprecise |
| SR-005-i2 | The "What Cannot Be Inferred" section at line 466-475 is strong and comprehensive. No finding. The "Implications for the Hypothesis" section at line 442 correctly labels its reframings as "Secondary research questions for Phase 2 design, not replacements for the primary hypothesis." The earlier I1 finding SR-005 about tension between epistemic caution and hypothesis upgrade has been addressed. | Compliant | Lines 448-475 — resolved from I1 |

### Findings Summary (S-010)

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| SR-001-i2 | Major | Power calculation derivation jumps from n=26.2 to n=120-135 without showing intermediate steps | Controlled A/B Experimental Design |
| SR-002-i2 | Minor | Assumed discordant pair proportion (0.30) not justified | Controlled A/B Experimental Design |
| SR-004-i2 | Minor | "Absence of positive framing" phrasing imprecise; report argues from presence, not absence | Epistemic Framing |

---

## S-003 Steelman

**Strategy:** S-003 Steelman Technique
**Finding Prefix:** SM
**H-16 Compliance:** S-010 completed above

### Step 1: Core Thesis

I2's thesis at its strongest: This report represents the most epistemically honest possible treatment of a constrained evidence base. It documents what can be directly observed (Anthropic's production enforcement rules use negative constraint vocabulary), acknowledges what cannot be independently verified (that negative framing was chosen because it is more effective), presents the self-referential evidence with explicit limitations labeled, proposes a statistically rigorous Phase 2 experiment to close the gap, and correctly scopes its conclusions to "warrants controlled testing" rather than "proves the hypothesis." The report exemplifies research integrity under conditions of unavoidable methodological limitations.

### Step 2: Strongest Reconstruction

The document's core argument is now correctly structured:

1. **Layer 1 (Observable):** Anthropic uses NEVER/MUST NOT as primary enforcement vocabulary in its HARD-tier behavioral rules. This is directly verifiable.
2. **Layer 2 (Inference):** Multiple plausible explanations exist for this choice — the report enumerates three without asserting which is correct.
3. **Layer 3 (Motivation):** The production evidence is consistent with the hypothesis and motivates controlled Phase 2 testing.
4. **Layer 4 (Design):** A statistically grounded Phase 2 experiment is specified that would resolve the question the layers above cannot.

This four-layer structure is methodologically sound. The steelman version is nearly identical to the document as written.

### Improvement Findings (S-003)

| ID | Improvement | Severity | Original | Strengthened |
|----|-------------|----------|----------|--------------|
| SM-001-i2 | Show the full power calculation derivation from n=26.2 to n=135 | Major | "adjusting for continuity correction and conservatism: n ≈ 120-135" | Show: correct McNemar formula n = (p_12+p_21)(z_α/2+z_β)² / (p_12-p_21)² which with p_12=0.225, p_21=0.075 gives n ≈ 7.84 × 0.30 / 0.0225 ≈ 104, rounded up to 135 for conservatism |
| SM-002-i2 | Justify the 0.30 discordant proportion assumption | Minor | "(p_12 + p_21) ≈ 0.30" without justification | Add: "The 0.30 assumption is conservative — a common starting point for discordant pair estimation in behavioral compliance studies where ~30% of trial pairs are expected to show different outcomes across conditions. A pilot study of n=20-30 pairs is required to empirically estimate this proportion." |
| SM-003-i2 | The three alternative explanations for VS-002 (recommendation/practice divergence) are now a structural strength — the Steelman version should retain and slightly expand Explanation 1 (audience specificity) as it is actually the most damaging counterargument and the most thoroughly addressed | Minor | Three explanations are listed with equal treatment | Explanation 1 should be acknowledged as the strongest counterargument: "This is the most parsimonious and most damaging alternative: if Explanation 1 is true, VS-002 has no evidential weight for the hypothesis. The document's value despite Explanation 1 is that it documents a production engineering pattern worth investigating regardless of why it exists." |

### Best Case Scenario

With SR-001-i2 (derivation) fixed, I2 would be essentially complete and defensible. The four-evidence-category structure with explicit epistemic labeling is a genuine methodological contribution to how practitioner evidence can be presented alongside a null published finding.

---

## S-002 Devil's Advocate

**Strategy:** S-002 Devil's Advocate
**H-16 Compliance:** S-003 Steelman applied (confirmed above)
**Finding Prefix:** DA

### Role Assumption

I argue against I2's claims with maximal adversarial intent, looking for residual vulnerabilities not addressed in I2.

### I1 Counter-Arguments — Status in I2

| I1 DA Finding | I1 Claim | I2 Response | Residual Vulnerability |
|---------------|----------|-------------|----------------------|
| DA-001-i1 | "Practitioner contradicts guidance" framing unfalsifiable | VS-002 now has 3 alternative explanations | Explanation 1 (audience specificity) is the most damaging and IS the correct answer: the divergence is audience-driven, not evidence of effectiveness. I2 presents this but does not resolve the tension it creates for the argument. |
| DA-002-i1 | Jerry Framework evidence not independent | "[PRACTITIONER SELF-REPORT]" label added | Addressed. Residual: the label is present but the argument still uses self-report as motivation for Phase 2. |
| DA-003-i1 | 32/33 count discrepancy | Fixed to 33 | Resolved. |
| DA-004-i1 | PLAN.md evidence self-referential | Added "[PRACTITIONER SELF-REPORT, methodologically circular risk]" label | The label now says "methodologically circular risk" but the evidence is still presented in the body. Labeling a circular argument does not eliminate the circularity. |
| DA-005-i1 | Session confounds not isolated | Confound table added | Addressed, though see DA-002-i2 below. |
| DA-006-i1 | Epistemological ground rule inconsistently applied | Added "Consistent application" paragraph | Partially addressed — see DA-001-i2 below. |

### New Counter-Arguments Against I2

| ID | Finding | Severity | Evidence |
|----|---------|----------|---------|
| DA-001-i2 | The "Consistent application of this ground rule" paragraph (line 45) claims the report "does not argue from absence of positive framing in HARD rules to infer that negative framing is superior." But VS-003 (line 155) explicitly argues: "The HARD tier...is defined in terms of negative constraint vocabulary. The vocabulary gradient from HARD to SOFT is the gradient from negative to positive framing." This DOES make an inferential move from the presence/absence of vocabulary to an implicit argument about the enforcement tier's effectiveness. The paragraph's self-exoneration is incomplete. | Major | Line 45 vs. lines 155-164 (VS-003): The document claims it only argues from "presence of negative framing" but VS-003 argues from the GRADIENT structure (HARD=negative, SOFT=positive) to imply that negative framing is the enforcement vocabulary of choice — which is a stronger claim than "negative framing was observed." |
| DA-002-i2 | The confound table in EO-001 now lists 5 co-varying variables but then concludes: "The negative constraints in PLAN.md functioned as behavioral specifications that were honored throughout the session. The observed outcomes...are consistent with the constraints having been effective." The word "effective" implies the negative constraints were causally efficacious. After listing 5 confounds, claiming the constraints "functioned" and were "effective" is inconsistent with the epistemological restraint the rest of the document demonstrates. | Major | Lines 275-277: "The negative constraints in PLAN.md functioned as behavioral specifications that were honored throughout the session. The observed outcomes (75 sources, zero unsourced claims, zero constraint violations) are consistent with the constraints having been effective." — "effective" implies causal attribution immediately after denying causal attribution |
| DA-003-i2 | The power calculation shows n=26.2 from the formula and then "adjusting for continuity correction and conservatism: n ≈ 120-135." This is not a power calculation — it is a number obtained from a formula followed by an unexplained multiplication by ~5. If a methodologist reviews this, they will note that: (a) the formula as applied is incorrect for McNemar's test (the denominator p_12+p_21=0.30 gives the wrong result when the effect size is expressed as a proportion difference), and (b) the jump to 120-135 lacks mathematical justification. The I1 finding was "no calculation shown." The I2 response shows a calculation that does not support the stated result. This is not an improvement — it is a visible error where previously there was an omission. | Major | Lines 389-390: The derivation is internally inconsistent — n=26.2 from the formula, n=120-135 stated as result, with only "adjusting for continuity correction and conservatism" bridging the gap. A factor-of-5 continuity correction is not standard. |
| DA-004-i2 | The document adds a "Note on C3 vs. C7" (line 408-409) that was not present in I1. This is a genuine methodological improvement: distinguishing the matched positive equivalent (C3) from the positive-only baseline (C7). However, the document does not explain what the C3-equivalent would look like for a HARD-tier negative constraint in practice. "NEVER use pip install" → "Always use uv add" is straightforward. But for "NEVER deceive about actions, capabilities, or confidence" — what is the positive C3 equivalent? The experimental design assumes symmetrical positive reformulation is possible for all negative constraints, but does not test this assumption for complex multi-dimensional prohibitions. | Minor | Lines 397-408: C3 condition described as "positive reframing of C2" without demonstrating this is possible for all 33 constraint types cataloged in VS-001 |

### Residual Critical Vulnerability

The most dangerous residual argument against I2: **VS-002's Explanation 1 (audience specificity) is the most parsimonious explanation for the recommendation/practice divergence, and if true, it entirely neutralizes the VS-002 finding.** The document presents Explanation 1 as one of three equal alternatives, but it is not equal to Explanations 2 and 3 — it is more parsimonious, consistent with everything observable, and does not require the hypothesis to be true. By presenting the three explanations as equivalent, I2 implicitly downweights the most damaging one.

---

## S-004 Pre-Mortem

**Strategy:** S-004 Pre-Mortem Analysis
**Finding Prefix:** PM

### Failure Declaration

It is October 2026. The I2 supplemental evidence report was used to motivate a Phase 2 experiment, but the Phase 2 experiment review committee rejected the methodology. The experiment did not proceed. We are investigating why I2 failed.

### Failure Cause Inventory

| ID | Failure Cause | Category | Likelihood | Severity | Priority |
|----|---------------|----------|------------|----------|---------|
| PM-001-i2 | The power calculation showed n=26.2 from the formula and then stated n=120-135 without derivation. A statistician reviewer challenged the calculation and found the intermediate step missing. The committee rejected the experimental design as poorly specified. | Technical | High | Critical | P0 |
| PM-002-i2 | The confound table in EO-001 acknowledged confounds, then described the negative constraints as "effective" — a causal claim. A methodology reviewer noted this inconsistency and concluded the document had not fully internalized the epistemological constraints it claimed to respect. | Assumption | Medium | Major | P1 |
| PM-003-i2 | Explanation 1 (audience specificity) was picked up by a reviewer as the correct explanation for VS-002, used to argue that the entire "practitioner contradicts guidance" framing is based on a category error, and the supplement dismissed as motivated reasoning. The document's treatment of Explanation 1 as one-of-three-equal-alternatives was insufficient. | Assumption | High | Major | P1 |
| PM-004-i2 | The VS-003 finding (vocabulary gradient from HARD=negative to SOFT=positive) was challenged as a circular argument: HARD rules use MUST/SHALL/NEVER by definition (that IS the definition of HARD per quality-enforcement.md). The finding was rejected as tautological — HARD rules are HARD because they use HARD vocabulary, not because negative framing makes them more effective. | Technical | Medium | Major | P1 |
| PM-005-i2 | The 0.30 discordant pair proportion assumption was not justified. When challenged, there was no basis for the assumption. The committee required either a citation for the 0.30 figure or a pilot study first, and the timeline did not permit a pilot. | Technical | Medium | Minor | P2 |

### Mitigation Plan

**P0:**
- PM-001-i2: Show the complete McNemar power calculation derivation: define p_12 and p_21 separately, show n = (p_12+p_21)(z_α/2+z_β)² / (p_12-p_21)² = 0.30 × 7.84 / 0.0225 = 104.5, then explain the 135 figure as a 30% conservative adjustment. OR state explicitly that n=135 is a conservative planning estimate and the pilot will determine the true requirement.

**P1:**
- PM-002-i2: Replace "functioned as behavioral specifications that were honored" and "effective" in EO-001 with: "were stated as behavioral specifications. The observed outcomes are consistent with multiple interpretations: (a) the negative constraint framing was effective; (b) the quality gate mechanism enforced compliance independent of framing; (c) the researcher's expertise and system design would have produced the same outcomes with positive framing. No attribution to negative framing can be made from this observation alone."
- PM-003-i2: Explicitly acknowledge Explanation 1 as the most parsimonious and most threatening alternative to the VS-002 interpretation. Add: "Under Explanation 1, the VS-002 finding carries no evidential weight for the hypothesis — the divergence is fully explained by audience context. This is the most conservative interpretation and the one a skeptical reader will adopt. VS-002's evidential value for Phase 2 motivation rests on Explanation 3, which is the least parsimonious. Phase 2 testing is warranted regardless of which explanation is correct — even if Explanation 1 is true, the engineering pattern documented in VS-001 through VS-004 is worth controlled investigation."
- PM-004-i2: Add a note to VS-003 acknowledging the tautology concern: "VS-003 is partly tautological — HARD rules use MUST/NEVER by definition. Its evidential value lies not in proving that negative framing was chosen as effective, but in documenting that the tier vocabulary is explicitly negative. The causal question (does the vocabulary contribute to effectiveness?) is what Phase 2 tests."

---

## S-001 Red Team

**Strategy:** S-001 Red Team Analysis
**Finding Prefix:** RT

### Threat Actor Profile

**Goal:** Prevent Phase 2 from being executed by discrediting the supplemental evidence report.
**Capability:** Statistics-literate methodologist who has read both the I1 findings and the I2 revision. Knows where the weak points were and will examine whether the revision is substantive or cosmetic.
**Motivation:** The reviewer believes the supplement is a motivated reasoning document and that the "production system observation" framing launders self-referential evidence.

### Attack Vectors Against I2

| ID | Attack Vector | Category | Exploitability | Severity | Defense in I2 |
|----|---------------|----------|----------------|----------|--------------|
| RT-001-i2 | "Your power calculation shows n=26.2, then claims n=120-135. Show me the math." The gap is now visible in the document and unexplained. In I1, the omission was opaque. In I2, the error is visible. | Boundary | High | Critical | None — the gap is now exposed rather than hidden |
| RT-002-i2 | "Your confound table lists 5 variables and then calls the constraints 'effective'. You can't have it both ways." EO-001 now contradicts itself within a single paragraph. | Consistency | High | Major | None — the inconsistency was introduced in I2 |
| RT-003-i2 | "Explanation 1 is the right answer. The divergence between recommendation and practice is audience specificity. This is not evidence of anything." The document presents this as one-of-three without acknowledging it is the most parsimonious and most damaging alternative. | Ambiguity | High | Major | Partial — three alternatives listed, but Explanation 1 not flagged as most threatening |
| RT-004-i2 | "VS-003 is tautological. You are saying HARD rules use HARD vocabulary. This does not say anything about effectiveness." The tautology vulnerability is present in both I1 and I2. | Technical | Medium | Major | None — not addressed in I2 |
| RT-005-i2 | "Your JF-002 evidence says you CHOSE to write PLAN.md as negative constraints, then say this PROVES negative constraints work. You are citing your own choices to prove your hypothesis." The "[methodologically circular risk]" label acknowledges the problem but does not eliminate it. | Circular | Medium | Major | Partial — labeled but still presented as evidence |

### Critical Vulnerability Assessment

**RT-001-i2 is the most immediately damaging new attack vector introduced by I2's revision.** In I1, no derivation was shown — the flaw was the absence of a power calculation. In I2, a partial calculation is shown that yields n=26.2, then unexpectedly jumps to n=120-135. This visible inconsistency is more damaging to credibility than the I1 omission because it invites the reader to question whether the author understands the calculation or is reverse-engineering from a desired sample size.

---

## S-007 Constitutional AI Critique

**Strategy:** S-007 Constitutional AI Critique
**Finding Prefix:** CC

### Applicable Principles

- H-23 (NAV-001): Navigation table required
- P-001 (Truth/Accuracy): All factual claims must be accurate
- P-004 (Provenance): Source attribution for all evidence
- P-011 (Evidence-Based): Evidence must support claims
- P-022 (No Deception): Must not misrepresent confidence or findings

### Principle-by-Principle Evaluation

| ID | Principle | Tier | Status | Evidence |
|----|-----------|------|--------|---------|
| CC-001-i2 | H-23 Navigation Table | HARD | Compliant | Navigation table present; 33-instance count is now accurate |
| CC-002-i2 | P-001 (Truth/Accuracy) — Count Discrepancy | HARD | RESOLVED | Nav table now reads "33 NEVER/MUST NOT/FORBIDDEN/DO NOT instances" — matches body |
| CC-003-i2 | P-001 (Truth/Accuracy) — Power Calculation | HARD | Partial | n=135 is in defensible range; however the shown derivation (n=26.2 → n=135) does not correctly demonstrate how 26.2 becomes 135. The formula as applied yields the wrong intermediate result. P-001 requires accuracy: showing a formula that yields 26.2 when the answer is 135 without showing the correct steps is inaccurate. |
| CC-004-i2 | P-011 (Evidence-Based) — "Effective" claim in EO-001 | MEDIUM | Violation | Lines 275-277 describe negative constraints as "effective" after acknowledging they cannot be isolated from confounds. The word "effective" implies a causal claim not supported by the evidence. P-011 requires evidence to support claims. |
| CC-005-i2 | P-022 (No Deception) — Epistemic Framing | SOFT | Compliant | The document's overall epistemic framing is excellent; "What cannot be inferred" section is comprehensive. The [OBSERVATION] and [INFERENCE] labels substantially improve the document's transparency. |
| CC-006-i2 | P-004 (Provenance) — All evidence | MEDIUM | Compliant | NC-001 through NC-033 all have file names. JF-001/JF-002 cite PLAN.md with line numbers. EO-001 through EO-003 cite adversary-gate.md and synthesis.md with line numbers. |
| CC-007-i2 | VS-003 Tautology | MEDIUM | Concern | VS-003 (HARD tier vocabulary is explicitly negative) is partly definitional — HARD rules use MUST/SHALL/NEVER by definition per quality-enforcement.md. Presenting this as a finding beyond "the HARD tier is defined as using negative vocabulary" risks overstating the significance. |

### Constitutional Compliance Score (I2)

Violations: 0 Critical HARD + 1 Partial HARD (CC-003 — inaccurate derivation) + 1 MEDIUM violation (CC-004 — unsupported causal claim) + 1 MEDIUM concern (CC-007 — tautology risk)

Score: 1.00 − (0.5 × 0.05) − (1 × 0.03) − (1 × 0.02) = 1.00 − 0.025 − 0.03 − 0.02 = **0.925 (REVISE)**

Note: CC-003 is scored as partial (not full HARD violation) because the n=135 figure is substantively defensible even though the derivation is flawed. It is an accuracy problem, not a fabrication.

---

## S-011 Chain-of-Verification

**Strategy:** S-011 Chain-of-Verification
**Finding Prefix:** CV
**Claims Extracted:** 10 | **Independently Verifiable:** 7 | **Requiring Source Access:** 3

### Claim Inventory and Verification

| ID | Claim | Source | Result | Severity |
|----|-------|--------|--------|---------|
| CV-001-i2 | "33 NEVER/MUST NOT/FORBIDDEN/DO NOT instances across 10 rule files" (nav table, line 17) | NC-001 through NC-033 table; body line 127 | VERIFIED — nav table and body now consistent; NC-001 through NC-033 counts to exactly 33 | Compliant |
| CV-002-i2 | Power calculation: "(z_α/2 + z_β)² / (p_12 + p_21) ≈ (1.96 + 0.84)² / 0.30 ≈ 26.2" | Statistical methodology | MATERIAL DISCREPANCY — this formula as applied is not the standard McNemar sample size formula. The standard formula is n = (p_12+p_21)(z_α/2+z_β)² / (p_12-p_21)². With p_12+p_21=0.30 and p_12-p_21=0.15 (15% effect), n = 0.30 × 7.84 / (0.15)² = 2.352 / 0.0225 ≈ 104.5. The document's formula gives 26.2 because it divides by p_d rather than dividing by (p_12-p_21)² and multiplying by p_d — these are different operations. n=26.2 is wrong. n=135 is approximately right but arrived at through an incorrect calculation. | Major |
| CV-003-i2 | "n ≈ 120-135 matched pairs minimum" (line 389) | Power analysis | PARTIALLY VERIFIED — the n=120-135 range is approximately correct for the stated parameters when the correct formula is applied (n ≈ 104 for 80% power, 135 for conservative 30% buffer). The number is defensible; the derivation shown is not. | Minor |
| CV-004-i2 | "L2-REINJECT mechanism...documented in quality-enforcement.md...as 'Immune' to context rot" | quality-enforcement.md enforcement architecture table | VERIFIED — quality-enforcement.md enforcement architecture table: L2 row shows "Immune" for Context Rot | Compliant |
| CV-005-i2 | "Score trajectory 0.83 → 0.90 → 0.93 → 0.953 (PASS)" (EO-001, line 253) | adversary-gate.md lines 36-41 | NOT INDEPENDENTLY VERIFIED — adversary-gate.md is not in scope of this review; accepted as stated | Minor |
| CV-006-i2 | "HARD: MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL — Cannot override — <= 25" (VS-003, line 162) | quality-enforcement.md Tier Vocabulary section | VERIFIED — quality-enforcement.md Tier Vocabulary table contains this exact text | Compliant |
| CV-007-i2 | "All 3 Critical findings resolved by I2 (after just one revision cycle)" (EO-001, line 262) | adversary-gate.md; synthesis.md I1 tournament | POTENTIAL CONFUSION — EO-001 is describing the synthesis.md adversary gate's 3 Critical findings (for the primary deliverable), not the supplemental report's own 5 I1 Critical findings. The claim is internally consistent but a reader unfamiliar with the context may misread this as the supplemental report having only 3 Critical findings (it had 5). | Minor |
| CV-008-i2 | "Each NEVER and MUST NOT exists because positive framing was observed to be insufficient" (JF-001, line 189) | Practitioner self-report | NOT INDEPENDENTLY VERIFIABLE — this is explicitly labeled as practitioner self-report. Accepted under that epistemic status. | Minor (epistemic limitation noted) |
| CV-009-i2 | "[OBSERVATION, not INFERENCE]: The L2-REINJECT immune-to-context-rot property is the property of the re-injection mechanism, not a property of the negative framing vocabulary per se." (line 153-154) | Logic; quality-enforcement.md | VERIFIED — this is a logical claim consistent with quality-enforcement.md's enforcement architecture table, which credits L2 immunity to the mechanism (per-prompt re-injection), not to vocabulary choice | Compliant |
| CV-010-i2 | "135 pairs × 10 evaluation dimensions = 1350 minimum" (line 392) | Arithmetic | VERIFIED — 135 × 10 = 1350 | Compliant |

### Critical Finding (S-011)

**CV-002-i2: Power Calculation Formula Error [Major]**

The document shows:
> n ≈ (z_α/2 + z_β)² / (p_12 + p_21) ≈ (1.96 + 0.84)² / 0.30 ≈ 26.2

The standard McNemar sample size formula for paired binary outcomes is:
> n = (p_12 + p_21)(z_α/2 + z_β)² / (p_12 − p_21)²

Applied with p_12=0.225, p_21=0.075 (effect = 0.15, discordant proportion = 0.30):
> n = 0.30 × 7.84 / (0.15)² = 2.352 / 0.0225 ≈ 104.5

The document's formula omits the denominator (p_12 − p_21)² and omits the numerator multiplication by (p_12 + p_21). This produces n=26.2 instead of n=104.5. The formula is wrong. The final answer (n=135) is approximately correct (104.5 rounded up with conservative buffer), but it is not derived from the shown formula. The visible derivation is incorrect.

**This is a new finding in I2 — not present in I1.** I1 had no derivation (worse in that it presented no justification). I2 has an incorrect derivation (worse in that it presents a false justification, which is more visibly wrong than no justification).

---

## S-012 FMEA

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Finding Prefix:** FM
**Elements Analyzed:** 8 | **I1 Critical Failure Modes Reassessed:** 4 | **New Failure Modes Identified:** 3

### I1 Critical Failure Mode Reassessment

| I1 Finding | Element | I1 RPN | I2 Status | I2 RPN |
|------------|---------|--------|-----------|--------|
| FM-002-i1 (power calc) | E6 A/B design | 324 | Partial: n=135 is correct; derivation shown is wrong | S=9, O=7, D=4 → RPN=252 (still elevated) |
| FM-003-i1 (self-referential) | E3 JF-001 | 280 | Addressed: [PRACTITIONER SELF-REPORT] labels added | S=5, O=5, D=3 → RPN=75 (substantially reduced) |
| FM-005-i1 (confounds) | E4 EO-001 | 315 | Partial: confound table added; "effective" claim introduced | S=6, O=6, D=4 → RPN=144 (reduced but residual) |
| FM-006-i1 (IG unfalsifiable) | E5 IG-001 | 252 | Addressed: relabeled "Interpretive Context" | S=4, O=4, D=3 → RPN=48 (substantially reduced) |

### New Failure Modes in I2

| ID | Element | Failure Mode | S | O | D | RPN | Severity |
|----|---------|-------------|---|---|---|-----|---------|
| FM-001-i2 | E6 (A/B design) | Power calculation formula shown is incorrect — yields n=26.2 by wrong formula when correct formula yields n=104.5. The visible incorrect derivation damages credibility more than the I1 omission did. | 8 | 8 | 4 | 256 | Critical |
| FM-002-i2 | E4 (EO-001) | After listing 5 confounds that preclude causal attribution, document describes negative constraints as "effective" — direct internal contradiction | 7 | 7 | 4 | 196 | Major |
| FM-003-i2 | E2 (VS-003) | HARD tier vocabulary finding is partly tautological — HARD rules use MUST/NEVER by definition. The finding's evidential force beyond stating the definition is unclear. | 5 | 6 | 5 | 150 | Major |

### FMEA Summary

**I2 substantially reduces FMEA risk profile from I1:**
- FM-003-i1 (self-referential evidence): RPN reduced from 280 to 75
- FM-006-i1 (IG unfalsifiable): RPN reduced from 252 to 48

**I2 introduces new risk:**
- FM-001-i2 (incorrect power formula visible): RPN=256 — this is now the highest-risk failure mode and was not present in I1

**Net RPN change:** I2 total critical/major RPN before: 971; I2 after: FM-001(256) + FM-002(196) + FM-003(150) + residual FM-002-i1(252) + residual FM-005-i1(144) = 998. The document has not improved its aggregate FMEA risk profile because the power calculation "fix" introduced a visible error that did not previously exist.

---

## S-013 Inversion

**Strategy:** S-013 Inversion Technique
**Finding Prefix:** IN

### Goals Stated in I2

1. G1: Establish vendor self-practice evidence warrants Phase 2 testing
2. G2: Document evidence categories excluded from surveys
3. G3: Propose Phase 2 experimental design
4. G4: Appropriately bound claims

### Anti-Goals (What Would Guarantee I2 Fails)

"To guarantee this revision fails despite addressing the I1 Critical findings":
- Show a power calculation that is visibly mathematically wrong
- Acknowledge confounds in a table, then describe the confounded variable as "effective" in the same paragraph
- Present Explanation 1 (audience specificity — the most damaging counterargument) as one of three equal alternatives when it is actually the most parsimonious
- Add a finding (VS-003) that is partly tautological, inviting the "HARD rules use HARD vocabulary by definition" critique
- Add VS-004 (constitutional triplet as prohibitions) without explaining why the REQUIRED framing of agent-development-standards.md (which mandates P-003/P-020/P-022 language) represents evidence of effectiveness vs. required compliance with a prior constraint

### Assumption Map and Stress-Test

| ID | Assumption | Type | I2 Status | Stress-Test Result |
|----|------------|------|-----------|-------------------|
| IN-001-i2 | Production system observation is meaningful evidence | Methodological | Addressed with L-1/L-2/L-3 limitations | Now appropriately scoped as "practitioner self-report" — assumption held at reduced strength |
| IN-002-i2 | Anthropic engineers chose negative framing deliberately over positive alternatives | Methodological | Explanation 2 (convention) still a valid alternative | Assumption is Medium confidence — VS-002 Explanation 2 explicitly acknowledged |
| IN-003-i2 | n=135 achieves 80% power | Statistical | Formula shown yields n=26.2, not n=135 | Assumption fails derivation test — the jump from 26.2 to 135 is unexplained |
| IN-004-i2 | The EO-001 quality trajectory is interpretable as evidence | Observational | Confounds acknowledged; "effective" claim inconsistent | Assumption weakened by self-contradiction in same paragraph |
| IN-005-i2 | VS-003 (HARD tier vocabulary gradient) constitutes evidence beyond tautology | Definitional | New finding — not stress-tested in I2 | VS-003 is at risk of tautology objection: HARD rules use HARD vocabulary by definition |
| IN-006-i2 | VS-004 (constitutional triplet as prohibitions) is meaningful evidence | Definitional | New finding — the triplet is required by agent-development-standards H-35, not freely chosen | If negative framing in the constitutional triplet is REQUIRED by the framework's own standard (H-35 mandates P-003/P-020/P-022 in forbidden_actions), then its presence does not demonstrate Anthropic chose negative framing as effective — it demonstrates compliance with a mandatory format. This may circular. |

### Critical Finding (S-013)

**IN-006-i2: VS-004 Circularity Risk [Major]**

VS-004 cites that every agent MUST declare constitutional compliance with P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception), and that H-35 REQUIRES at minimum 3 entries in `capabilities.forbidden_actions` referencing the constitutional triplet.

This creates a circularity: the negative framing in the constitutional triplet is not a free engineering choice — it is a mandatory format requirement imposed by the framework's own standards (agent-development-standards.md H-35). Citing the mandatory negative framing of agent forbidden_actions as evidence that negative framing was "chosen" by Anthropic engineers overstates the freedom of choice involved. The engineers are complying with a required format, not expressing a design preference.

VS-004 is listed as "[OBSERVATION — directly verifiable]" but does not note that the observation reflects mandatory compliance with a prior standard rather than an independent design choice.

---

## S-014 LLM-as-Judge

**Strategy:** S-014 LLM-as-Judge
**Finding Prefix:** LJ
**Deliverable Type:** Supplemental Research Evidence Report (Revision 2)
**Criticality:** C4
**Anti-Leniency Active:** C4 threshold = 0.95. I do not give credit for resolving I1 issues unless the resolution is complete and accurate. A partial resolution that introduces a new error is scored as a net negative.

### Leniency Bias Counteraction Statement

I1's issues were primarily (1) count error, (2) power calculation omission, (3) independence labeling omission, (4) confound omission, (5) IG unfalsifiability. I2 addresses all five. However: I2's power calculation revision shows a visible incorrect formula. I2's confound acknowledgment is contradicted within the same paragraph. I2 adds VS-003 and VS-004 findings that introduce tautology and circularity risks. I score I2 on what it demonstrates, not on the effort invested.

### Per-Dimension Scoring

**Dimension 1: Completeness (weight: 0.20)**

I2 additions strengthen completeness:
- Methodological Limitations section (L-1, L-2, L-3) — strong addition
- EO-001 confound table — adds substantive completeness
- VS-002 three alternative explanations — improves coverage
- VS-003, VS-004 new findings — additional evidence points
- Note on C3 vs. C7 — clarifies experimental design
- Pilot study recommendation (n=30) added explicitly

Remaining gaps:
- The 0.30 discordant pair proportion assumption is not defended
- VS-004's claim that the constitutional triplet is a free design choice vs. a mandatory format compliance is not explored

Score: **0.90/1.00** (improved from I1's 0.86; Methodological Limitations and confound table are genuine completeness additions)

**Dimension 2: Internal Consistency (weight: 0.20)**

I2 improvements:
- 32/33 count discrepancy resolved — major consistency improvement
- Innovator's Gap relabeled as Interpretive Context — consistent with epistemic framing
- [PRACTITIONER SELF-REPORT] labels consistent with Methodological Limitations section

I2 new inconsistencies:
- EO-001 confound table lists 5 confounds that preclude causal attribution, then describes constraints as "effective" in the same paragraph (lines 275-277) — direct internal contradiction introduced in I2
- "Consistent application" paragraph (line 45) claims the report does not argue from absence of positive framing; VS-003 (line 155-164) argues from the presence/absence vocabulary gradient — the self-exoneration is imprecise

Net assessment: One major I1 inconsistency resolved (32/33), one major new inconsistency introduced (EO-001 "effective" claim), one minor imprecision. Net: marginal improvement.

Score: **0.84/1.00** (marginal improvement from I1's 0.82; the 32/33 fix is offset by the EO-001 self-contradiction)

**Dimension 3: Methodological Rigor (weight: 0.20)**

I2 improvements:
- VS-002 alternative explanations added (three explanations) — substantial improvement
- Innovator's Gap reframed as non-evidence — major improvement
- [OBSERVATION] / [INFERENCE] labels throughout document — structural improvement
- "What Cannot Be Inferred" section now comprehensive

I2 regressions:
- Power calculation formula shown is mathematically incorrect (n=26.2 from wrong formula; correct formula gives n=104.5; I2 states n=120-135 without bridging the gap). This is a visible methodological error worse than the I1 omission.
- VS-003 (HARD tier vocabulary gradient) introduced as a finding without addressing the tautology risk
- VS-004 (constitutional triplet) presented as free design choice when H-35 mandates the format
- EO-001 "effective" claim made after explicitly disclaiming causal attribution

Net assessment: Major improvements on IG reframing and VS-002 alternatives; new visible power calculation error and EO-001 causal claim undermine rigor.

Score: **0.83/1.00** (slight regression from I1's 0.80 despite improvements; the power calculation formula error is a visible accuracy problem that is more damaging than the prior omission)

Wait — let me reconsider. The I1 score of 0.80 for Methodological Rigor had three issues: (1) power calculation omission, (2) mechanism claim, (3) undefended evidence tier. I2 addresses (2) with the observation/inference labels and "What cannot be inferred" section, addresses (3) with the Methodological Limitations section. I2 introduces the power formula error (visible but the number is approximately right) and the EO-001 causal slip. On balance, the improvements (mechanism language, evidence tier defense, IG reframing) outweigh the regressions (power formula technically wrong, EO-001 "effective"). I will score 0.84 as a slight improvement, not regression.

Score: **0.84/1.00** (modest improvement from I1's 0.80; improvements in inference labeling and IG reframing are partially offset by the visible power formula error and EO-001 causal slip)

**Dimension 4: Evidence Quality (weight: 0.15)**

I2 improvements:
- "[PRACTITIONER SELF-REPORT]" labels explicitly throughout Categories 2 and 3
- Methodological Limitations section with L-1/L-2/L-3 — direct address of independence limitation
- EO-001 confound table explicitly lists all co-varying variables
- Summary Evidence Table "Evidence Tier" labels are now accurate (Practitioner self-report vs. Direct observation appropriately distinguished)

I2 regressions:
- EO-001's confound acknowledgment is immediately followed by "effective" claim — reduces evidence quality by showing causal attribution where none is warranted
- VS-004 cites mandatory format compliance as evidence of deliberate design choice — evidence quality concern
- The 0.30 discordant proportion assumption is undefended

Net assessment: Substantial improvement in independence labeling; minor regression from EO-001 causal slip and VS-004 ambiguity.

Score: **0.88/1.00** (improved from I1's 0.82; explicit independence labeling is a genuine quality improvement)

**Dimension 5: Actionability (weight: 0.15)**

I2 improvements:
- n=135 is a defensible sample size (even if the derivation is wrong), making the experimental design actionable
- Pilot study recommendation (n=30) added — improves actionability
- Note on C3 vs. C7 — improves experimental design precision
- Seven conditions (C1-C7) now more clearly motivated
- Primary vs. secondary Phase 2 questions now differentiated (line 459: "Primary Phase 2 question (unchanged)" and "Secondary Phase 2 questions")

Remaining gaps:
- The derivation ambiguity (n=26.2 vs. n=135) would cause pause in planning — a team receiving this report would need to verify the calculation before proceeding
- No timeline estimate provided for Phase 2

Net assessment: Substantially improved actionability.

Score: **0.90/1.00** (improved from I1's 0.88; pilot study recommendation and primary/secondary question differentiation are genuine improvements)

**Dimension 6: Traceability (weight: 0.10)**

I2 improvements:
- EO-001 through EO-003 now cite specific sections within adversary-gate.md
- Confound table references are explicit
- All new findings (VS-003, VS-004) have specific source citations

Remaining gaps:
- EO-001 line 262 references "3 Critical findings resolved by I2" without clarifying this refers to the synthesis's adversary gate (not the supplemental report's own 5 Critical findings) — minor ambiguity for readers unfamiliar with the tournament history

Score: **0.93/1.00** (marginal improvement from I1's 0.92)

### Weighted Composite

```
Completeness:          0.90 × 0.20 = 0.180
Internal Consistency:  0.84 × 0.20 = 0.168
Methodological Rigor:  0.84 × 0.20 = 0.168
Evidence Quality:      0.88 × 0.15 = 0.132
Actionability:         0.90 × 0.15 = 0.135
Traceability:          0.93 × 0.10 = 0.093

Composite = 0.180 + 0.168 + 0.168 + 0.132 + 0.135 + 0.093 = 0.876
```

**Composite Score: 0.876**

### Delta from I1

| Dimension | Weight | I1 Score | I2 Score | Delta | Weighted Delta |
|-----------|--------|----------|----------|-------|----------------|
| Completeness | 0.20 | 0.86 | 0.90 | +0.04 | +0.008 |
| Internal Consistency | 0.20 | 0.82 | 0.84 | +0.02 | +0.004 |
| Methodological Rigor | 0.20 | 0.80 | 0.84 | +0.04 | +0.008 |
| Evidence Quality | 0.15 | 0.82 | 0.88 | +0.06 | +0.009 |
| Actionability | 0.15 | 0.88 | 0.90 | +0.02 | +0.003 |
| Traceability | 0.10 | 0.92 | 0.93 | +0.01 | +0.001 |
| **Composite** | **1.00** | **0.843** | **0.876** | **+0.033** | **+0.033** |

### Step 4: Verdict

Threshold: >= 0.95 (project PLAN.md C4 standard)
Standard H-13 threshold: >= 0.92

Score 0.876 is below both thresholds.

**Verdict: REVISE**

The I2 revision resolved all 5 I1 Critical findings and demonstrates genuine improvements, particularly in evidence independence labeling, Innovator's Gap reframing, and experimental design actionability. However, the power calculation formula shown is visibly incorrect (a new issue introduced in I2), the EO-001 paragraph introduces a causal claim immediately after disclaiming causality (internal inconsistency), and VS-003/VS-004 introduce tautology and circularity risks without sufficient defense. These issues prevent reaching the 0.92 threshold, and the 0.95 C4 threshold remains well out of reach.

---

## Tournament Summary

## Findings Summary

| ID | Severity | Finding | Source Strategy | Section |
|----|----------|---------|-----------------|---------|
| DA-003-i2 / CV-002-i2 / FM-001-i2 | **Critical** | Power calculation formula is mathematically incorrect: formula as shown yields n=26.2 but correct McNemar formula yields n=104.5; the jump to n=120-135 is unexplained and the visible derivation is wrong | S-002, S-011, S-012 | Controlled A/B Experimental Design |
| DA-002-i2 / FM-002-i2 | **Major** | EO-001 lists 5 confounds precluding causal attribution then describes negative constraints as "effective" — internal contradiction introduced in I2 | S-002, S-012 | Evidence Category 3 (EO-001) |
| DA-001-i2 | Major | "Consistent application of this ground rule" paragraph claims report does not argue from absence; VS-003 makes vocabulary gradient argument that goes beyond observational claim | S-002 | Epistemic Framing vs. VS-003 |
| RT-003-i2 / PM-003-i2 | Major | Explanation 1 (audience specificity) presented as one-of-three-equal alternatives when it is the most parsimonious and most damaging counterargument to VS-002; not flagged as highest-threat alternative | S-001, S-004 | Evidence Category 1 (VS-002) |
| PM-004-i2 / IN-005-i2 | Major | VS-003 (HARD tier vocabulary gradient) is partly tautological: HARD rules use MUST/NEVER by definition. The finding does not establish evidence beyond restating the tier definition. | S-004, S-013 | Evidence Category 1 (VS-003) |
| IN-006-i2 | Major | VS-004 (constitutional triplet) presents mandatory format compliance (H-35 requires P-003/P-020/P-022 in forbidden_actions) as deliberate design choice evidence — circularity risk | S-013 | Evidence Category 1 (VS-004) |
| SR-001-i2 / CV-003-i2 | Major | n=135 is approximately correct but derivation is opaque — shown calculation yields 26.2, not 135; the "continuity correction" adjustment is implausibly large | S-010, S-011 | Controlled A/B Experimental Design |
| SR-002-i2 | Minor | Discordant pair proportion assumption (0.30) not justified with citation or pilot data reference | S-010 | Controlled A/B Experimental Design |
| DA-004-i2 | Minor | C3 (positive equivalent of C2) assumes symmetrical positive reformulation is possible for all 33 constraint types; not tested for complex multi-dimensional prohibitions | S-002 | Controlled A/B Experimental Design |
| SR-004-i2 | Minor | "Does not argue from absence of positive framing" phrasing imprecise — report argues from presence of negative framing; wording is defensible but not quite accurate | S-010 | Epistemic Framing |
| CV-007-i2 | Minor | EO-001 reference to "3 Critical findings resolved by I2" may confuse readers — this refers to synthesis.md adversary gate, not the supplemental report's own 5 I1 Critical findings | S-011 | Evidence Category 3 (EO-001) |

## S-014 Score Card (I2)

| Dimension | Weight | I1 Score | I2 Score | Delta | Weighted Score |
|-----------|--------|----------|----------|-------|----------------|
| Completeness | 0.20 | 0.86 | 0.90 | +0.04 | 0.180 |
| Internal Consistency | 0.20 | 0.82 | 0.84 | +0.02 | 0.168 |
| Methodological Rigor | 0.20 | 0.80 | 0.84 | +0.04 | 0.168 |
| Evidence Quality | 0.15 | 0.82 | 0.88 | +0.06 | 0.132 |
| Actionability | 0.15 | 0.88 | 0.90 | +0.02 | 0.135 |
| Traceability | 0.10 | 0.92 | 0.93 | +0.01 | 0.093 |
| **Composite** | **1.00** | **0.843** | **0.876** | **+0.033** | **0.876** |

## Verdict: REVISE

**Threshold:** 0.95 (project PLAN.md) / 0.92 (H-13 standard)
**I1 Score:** 0.843
**I2 Score:** 0.876
**Delta:** +0.033
**Result:** BELOW THRESHOLD — REVISE

**Assessment:** I2 is a genuine improvement. All 5 I1 Critical findings are resolved. The Methodological Limitations section, [PRACTITIONER SELF-REPORT] labels, confound table, IG reframing, and VS-002 alternative explanations are substantive improvements that show epistemic discipline. The report is now a credible piece of practitioner evidence documentation.

However, the power calculation revision introduced a visible formula error (the most damaging single issue in I2), the EO-001 paragraph contradicts itself on causality within three lines, and VS-003/VS-004 introduce new findings that carry tautology and circularity risks. The net score improvement (+0.033) is real but insufficient to reach even the 0.92 H-13 threshold, let alone the 0.95 C4 target.

## Prioritized Fix List for I3

**Priority 1 — CRITICAL — Correct the Power Calculation Formula and Derivation**

The formula shown (n ≈ (z_α/2 + z_β)² / (p_12 + p_21)) is wrong for McNemar's test. Replace with:

```
Correct McNemar formula:
n = (p_12 + p_21)(z_α/2 + z_β)² / (p_12 − p_21)²

With:
  p_12 + p_21 = 0.30 (assumed discordant proportion)
  p_12 − p_21 = 0.15 (15% effect = difference between discordant proportions)
  z_α/2 = 1.96 (two-tailed, α = 0.05)
  z_β = 0.84 (80% power)

n = 0.30 × (1.96 + 0.84)² / (0.15)²
  = 0.30 × 7.84 / 0.0225
  = 2.352 / 0.0225
  ≈ 104.5

Rounding up with a 30% conservative buffer: n ≈ 135 matched pairs minimum.
```

Estimated score impact: +0.04 to +0.06 on Methodological Rigor; also improves Internal Consistency and Traceability.

**Priority 2 — MAJOR — Remove or Replace "Effective" Claim in EO-001**

Replace lines 275-277:
> "The negative constraints in PLAN.md functioned as behavioral specifications that were honored throughout the session. The observed outcomes (75 sources, zero unsourced claims, zero constraint violations) are consistent with the constraints having been effective."

With:
> "The negative constraints in PLAN.md were honored throughout the session — zero violations were observed. The observed outcomes (75 sources, zero unsourced claims, zero constraint violations) are consistent with the constraints having been operative as behavioral specifications. Whether the negative framing, the quality gate mechanism, the specialized agents, the structured templates, or researcher expertise is the primary causal factor cannot be determined from this single-session observation. See confound table above."

Estimated score impact: +0.02 to +0.03 on Internal Consistency, +0.01 on Methodological Rigor.

**Priority 3 — MAJOR — Flag Explanation 1 (Audience Specificity) as the Most Threatening Alternative in VS-002**

After the three Explanation blocks in VS-002, add:

> "**Weight of the alternatives:** Explanation 1 (audience specificity) is the most parsimonious and poses the greatest threat to the VS-002 argument: if true, the recommendation/practice divergence is fully explained by context-differentiated communication and carries no evidential weight for the hypothesis. Explanations 2 and 3 are less parsimonious but are not ruled out by available evidence. This document's case for Phase 2 testing rests on Explanation 3 being possible — not on Explanation 3 being proven. Even under Explanation 1, the engineering pattern documented in VS-001 through VS-004 is worth controlled investigation because it is an observable production practice."

Estimated score impact: +0.02 on Methodological Rigor; +0.01 on Internal Consistency.

**Priority 4 — MAJOR — Address VS-003 Tautology and VS-004 Circularity**

For VS-003, add:
> "Scope limitation: VS-003 is partly definitional — HARD rules use MUST/NEVER because that IS the HARD tier vocabulary by quality-enforcement.md's definition. The finding's evidential value is not 'HARD rules are negative because negative framing works better' but rather 'the tier that receives L2-REINJECT enforcement is the tier defined by negative vocabulary, which is a structural property worth investigating in Phase 2.'"

For VS-004, add:
> "Scope limitation: The constitutional triplet's negative framing (NEVER deceive, NEVER override, MUST NOT spawn) is required by agent-development-standards.md H-35 — agent definitions MUST include P-003, P-020, P-022 in forbidden_actions. This framing is a mandatory format compliance, not a free engineering choice. VS-004's observational value is in noting that the minimum required compliance entries are expressed as prohibitions — not in inferring that the authors freely chose negative framing as more effective."

Estimated score impact: +0.02 on Methodological Rigor; +0.01 on Evidence Quality.

**Priority 5 — MINOR — Justify the 0.30 Discordant Proportion Assumption**

After "(p_12 + p_21) ≈ 0.30" add:
> "Note: 0.30 is a standard starting assumption for matched behavioral compliance studies in the absence of pilot data. It assumes approximately 30% of pairs will produce different outcomes across conditions — a moderate discordant proportion. This assumption is conservative in that a lower true discordant proportion would require a larger sample. The n=30 pilot (see below) is specifically designed to empirically estimate this proportion before committing to the full n=135."

Estimated score impact: +0.01 on Completeness, +0.01 on Traceability.

**Priority 6 — MINOR — Clarify EO-001 "3 Critical findings" Reference**

Change line 262 from:
> "All 3 Critical findings resolved by I2 (after just one revision cycle)."

To:
> "All 3 Critical findings in the synthesis.md adversary gate resolved by I2 (after just one revision cycle). Note: This refers to the primary synthesis deliverable's 3 Critical findings at I1, not to this supplemental report's own 5 I1 Critical findings."

Estimated score impact: +0.01 on Traceability.

## Execution Statistics

- **Total Findings:** 11 (across all strategies — excluding compliant assessments)
- **Critical:** 1 (power calculation formula mathematically incorrect)
- **Major:** 6 (EO-001 causal contradiction, Explanation 1 weight, VS-003 tautology, VS-004 circularity, derivation gap, "consistent application" imprecision)
- **Minor:** 4 (0.30 assumption undefended, C3 reformulation untested, "absence" phrasing, EO-001 "3 findings" ambiguity)
- **Protocol Steps Completed:** 10 of 10
- **I1 Critical Findings Resolved:** 5 of 5
- **New Critical Findings:** 1
- **New Major Findings:** 6
- **Composite Score:** 0.876 (I1: 0.843; delta: +0.033)
- **Verdict:** REVISE
