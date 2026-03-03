# Strategy Execution Report: C4 Tournament — Supplemental Vendor Evidence Report

## Execution Context

- **Strategy:** All 10 Strategies (C4 Tournament Mode)
- **Templates:** `.context/templates/adversarial/s-{010,003,002,004,001,007,011,012,013,014}-*.md`
- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/supplemental-vendor-evidence.md`
- **Executed:** 2026-02-27T00:00:00Z
- **Iteration:** I1 (first tournament pass)
- **Criticality:** C4 Critical
- **Quality Threshold:** >= 0.95 (project PLAN.md constraint)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [S-010 Self-Refine](#s-010-self-refine) | Self-review findings |
| [S-003 Steelman](#s-003-steelman) | Strongest-form reconstruction |
| [S-002 Devil's Advocate](#s-002-devils-advocate) | Counter-arguments |
| [S-004 Pre-Mortem](#s-004-pre-mortem) | Future failure analysis |
| [S-001 Red Team](#s-001-red-team) | Adversarial attack vectors |
| [S-007 Constitutional AI](#s-007-constitutional-ai) | Governance compliance |
| [S-011 Chain-of-Verification](#s-011-chain-of-verification) | Factual claim verification |
| [S-012 FMEA](#s-012-fmea) | Component failure mode analysis |
| [S-013 Inversion](#s-013-inversion) | Assumption stress-testing |
| [S-014 LLM-as-Judge](#s-014-llm-as-judge) | Final scoring and verdict |
| [Tournament Summary](#tournament-summary) | Consolidated findings and verdict |

---

## S-010 Self-Refine

**Strategy:** S-010 Self-Refine
**Deliverable:** supplemental-vendor-evidence.md
**Criticality:** C4
**Iteration:** 1 of tournament
**Finding Prefix:** SR

### Objectivity Check

This is an external review agent, not the deliverable's creator. Full objectivity is achieved. Proceeding directly to systematic critique.

### Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-i1 | The count of negative constraint instances (33) is stated in the document body but the summary table at the end says 33, while the running count in the table headers and the footer say "33 observable negative constraint instances" — however the table lists NC-001 through NC-033 which is exactly 33. Count is internally consistent, but the document says "32 NEVER/MUST NOT/FORBIDDEN/DO NOT instances" in the Section navigation table (line 17) while the body says 33. | Major | Nav table line 17: "32 NEVER/MUST NOT/FORBIDDEN/DO NOT instances across 10 rule files"; body line 94: "33 observable negative constraint instances" | Internal Consistency |
| SR-002-i1 | The document makes the inferential leap that negative constraint language is "used" because it "works better" — but this causal inference is explicitly disclaimed in the What Cannot Be Inferred section. The Implications for the Hypothesis section nevertheless uses language that implies causality ("is the mechanism through which major AI vendors achieve reliable behavioral compliance"). | Major | Lines 372-373: "negative constraint framing...is the mechanism through which major AI vendors achieve reliable behavioral compliance" — asserting mechanism without causal evidence | Methodological Rigor |
| SR-003-i1 | The L2-REINJECT mechanism is described as making rules "immune" to context rot, but the L2-REINJECT content is itself expressed as negative constraints. The claim that L2 re-injection is what makes rules immune is cited to quality-enforcement.md's enforcement architecture table. This is verifiable and should be checked. | Minor | Lines 112-113: "The rules most resistant to context rot are the ones that use negative constraint language" — the causality direction needs checking; it may be that L2 re-injection causes immunity, not the negative phrasing. | Evidence Quality |
| SR-004-i1 | The Section 5 experimental design proposes 50 matched prompt pairs as the minimum for adequate statistical power, citing a "power calculation: detect 15% effect with 80% power at alpha=0.05" but does not show the actual power calculation. A 15% effect on a binary outcome requires substantially more than 50 pairs under standard assumptions. | Major | Line 308: "Sample size: 50 matched prompt pairs minimum — Power calculation: detect 15% effect with 80% power at alpha=0.05" — the sample size appears to be substantially underpowered for the stated effect size and alpha | Methodological Rigor |
| SR-005-i1 | Finding EO-001 characterizes the quality score trajectory as evidence of negative-constraint prompting effectiveness, but explicitly disclaims causality. However, the Implications section then uses this trajectory as part of the evidence base for the "stronger hypothesis." This creates an internal tension between the careful epistemic framing and the hypothesis upgrading. | Minor | Lines 291-296: retrospective comparison is presented as "directional signal only" but lines 375-378 treat it as sufficient to motivate a "stronger hypothesis" | Internal Consistency |

### Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| SR-001-i1 | Major | Navigation table says 32 instances; body says 33 | Section nav vs. Evidence Category 1 |
| SR-002-i1 | Major | Mechanism claim stated without causal support | Implications for the Hypothesis |
| SR-003-i1 | Minor | Causality direction of L2 immunity needs verification | Evidence Category 1 (VS-002) |
| SR-004-i1 | Major | Sample size calculation not shown; likely underpowered | Controlled A/B Experimental Design |
| SR-005-i1 | Minor | Tension between epistemic caution and hypothesis upgrade | Implications / Retrospective Comparison |

### Scoring Impact (Self-Refine Assessment)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | All four evidence categories present; experimental design detailed; implications explicit |
| Internal Consistency | 0.20 | Negative | SR-001 (32 vs 33 count discrepancy); SR-005 (epistemic framing tension) |
| Methodological Rigor | 0.20 | Negative | SR-002 (mechanism claim without causation); SR-004 (undocumented power calculation) |
| Evidence Quality | 0.15 | Positive | Most evidence specifically cited; file paths and line numbers provided |
| Actionability | 0.15 | Positive | Phase 2 experimental design is detailed and operationalized |
| Traceability | 0.10 | Positive | Most findings traceable to source files with line numbers |

---

## S-003 Steelman

**Strategy:** S-003 Steelman Technique
**Finding Prefix:** SM
**H-16 Compliance:** S-010 completed; S-003 now strengthens before downstream critique

### Step 1: Deep Understanding

The core thesis: Direct observation of Anthropic's own production system (Claude Code behavioral rules) reveals that negative constraint language (NEVER, MUST NOT, FORBIDDEN) is the enforcement vocabulary for the highest-criticality behavioral rules, while positive framing is reserved for lower-priority guidance. This constitutes a "practitioner's gap" — engineering practice contradicting published guidance — that motivates Phase 2 controlled testing.

### Improvement Findings Table

| ID | Improvement | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|--------------|-----------|
| SM-001-i1 | Resolve 32 vs 33 count inconsistency in navigation table | Critical | Nav table says "32 NEVER/MUST NOT/FORBIDDEN/DO NOT instances" | Should say "33 observable negative constraint instances across 10 rule files" to match body count | Internal Consistency |
| SM-002-i1 | Reframe mechanism claim as inference, not conclusion | Major | "is the mechanism through which major AI vendors achieve reliable behavioral compliance" | "appears to function as the mechanism...based on the observable correlation between negative vocabulary and enforcement tier. The causal direction cannot be established from observation alone." | Methodological Rigor |
| SM-003-i1 | Add power calculation derivation for n=50 sample size | Major | "Power calculation: detect 15% effect with 80% power at alpha=0.05" (no derivation) | Add footnote or inline derivation. Note: for McNemar's test on paired binary outcomes with expected proportion difference of 0.15, n=50 achieves approximately 55-60% power at alpha=0.05, not 80%. The honest sample size should be n=120+ for 80% power at 15% effect. | Methodological Rigor |
| SM-004-i1 | Strengthen the Innovator's Gap argument with a direct analogy | Minor | Publication bias argument is correctly framed but sparse | Add explicit analogy: "This is the same information asymmetry that makes trade secrets more valuable than published patents — the most effective techniques are the least published." | Evidence Quality |
| SM-005-i1 | Add explicit epistemic status declarations to each finding | Minor | Findings mix observation, inference, and logical argument without explicit labels | Prepend each finding with [OBSERVATION], [INFERENCE], or [LOGICAL ARGUMENT] to make the epistemic status immediately clear | Methodological Rigor |

### Best Case Scenario

The Steelman version of this report is strongest when: (1) the 32/33 count discrepancy is resolved; (2) all causal language is replaced with observational/inferential language; (3) the sample size calculation either shows the math or honestly revises the n upward. Under these conditions, the report makes a compelling and epistemically honest case that there is a structural gap in the published literature — precisely because production systems use the opposite of what they recommend — and that this gap motivates controlled Phase 2 testing.

---

## S-002 Devil's Advocate

**Strategy:** S-002 Devil's Advocate
**H-16 Compliance:** S-003 Steelman applied (confirmed above)
**Finding Prefix:** DA

### Role Assumption

I adopt the adversarial role: arguing against the report's core claims. The deliverable being challenged is the supplemental-vendor-evidence.md. Criticality: C4.

### Step 2: Assumption Inventory

**Explicit assumptions:**
- A1: Anthropic's behavioral engineering practice contradicts its published guidance
- A2: Production system direct observation is higher-tier evidence than academic literature
- A3: The Jerry Framework constitutes a meaningful production system
- A4: The L2-REINJECT mechanism makes negative-framed rules more reliable
- A5: Publication bias asymmetrically under-represents positive findings about negative prompting

**Implicit assumptions:**
- A6: The "innovator's gap" actually exists (not just a narrative device)
- A7: The 33 instances constitute a meaningful sample of Anthropic's design philosophy (vs. artifacts of the specific framework domain)
- A8: Anthropic engineers chose negative framing deliberately rather than by convention or author preference

### Step 3: Counter-Arguments

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-i1 | The "practitioner contradicts its own guidance" framing is unfalsifiable — any production system that uses negative constraints could be explained as "they know something they don't publish," making this argument vacuous | Critical | The argument structure at lines 106-114 assumes that divergence between recommendation and practice is evidence that practice is more effective. But divergence could also be explained by historical convention, domain specificity, or that the engineers writing rules are different from those writing guidance documentation. | Methodological Rigor |
| DA-002-i1 | The "Jerry Framework as production system" evidence is weakened by the fact that the Jerry Framework's rules were written by the same user who is conducting this research — this is not independent observation | Major | Lines 144-152 (JF-001): "each NEVER and MUST NOT exists because positive framing was insufficient" — but this claim about WHY the rules were written this way is asserted without documentation of the decision history. The researcher is interpreting their own design choices as evidence. | Evidence Quality |
| DA-003-i1 | The document claims "33 instances across 10 rule files" but the navigation table says 32. If the document cannot accurately count the core evidence in its own table, readers should question whether the cataloging methodology is reliable | Major | Nav table vs. body (SR-001 confirmed): numerical inconsistency in the primary evidence count undermines the document's claim to systematic direct observation | Evidence Quality |
| DA-004-i1 | The PLAN.md evidence (JF-002) is self-referential in a problematic way: the project owner used negative constraints, therefore negative constraints are effective. This is both an N=1 observation and a conflict of interest — the researcher is citing their own behavior as evidence supporting their hypothesis | Major | Lines 156-180: The argument that PLAN.md using negative constraints is evidence for negative constraint effectiveness conflates "I chose to use them" with "they work better than alternatives" | Methodological Rigor |
| DA-005-i1 | The session empirical observations (EO-001, EO-002, EO-003) cannot be attributed to negative prompting because the sessions also involved specialized skill agents, quality gates, structured templates, and multiple other control mechanisms. Negative prompting is at most one of many variables | Major | Lines 200-226: The quality trajectory (0.83 → 0.953) and zero constraint violations could be explained by the quality gate mechanism, specialized agents, structured templates, or skilled user design — not specifically by negative vs. positive framing | Evidence Quality |
| DA-006-i1 | The claim "Absence of published evidence is not evidence of absence" (line 39) is used to motivate the report, but the report itself then argues from absence (absence of positive framing in HARD rules = negative framing is better). The epistemological ground rule the report sets is not applied consistently | Major | Line 39 vs. the entire VS-001/VS-002 argument: the report correctly warns against absence-of-evidence reasoning, then uses presence-of-negative-framing-in-enforcement-tier to infer superiority of negative framing | Internal Consistency |
| DA-007-i1 | The comparison between AGREE-4 (prohibition unreliable) and the HARD rule enforcement tier may be a category error: academic studies test model instruction following, while HARD rules are read by Claude at runtime as part of its own operational context — these are fundamentally different mechanisms | Minor | Lines 256-269 (IG-002): The taxonomy claim that HARD rule negative constraints are "unstudied" is plausible, but the implication that this means they work better than studied alternatives is not supported | Methodological Rigor |

### Step 4: Response Requirements

**P0 (Critical — must resolve before acceptance):**
- DA-001: The report must demonstrate that the design divergence (recommendation vs. practice) is evidential rather than vacuous. This requires showing either (a) documentation of Anthropic engineers explicitly choosing negative framing over positive alternatives, or (b) acknowledging this as a limitation and limiting the claim to "observable correlation" rather than "engineering decision based on what works."

**P1 (Major — should resolve):**
- DA-002: Acknowledge that the Jerry Framework evidence is the researcher's own design choices; reframe as "practitioner self-report" rather than independent observation
- DA-003: Resolve the 32/33 count discrepancy immediately; it is an obvious credibility gap
- DA-004: Acknowledge the self-referential nature of PLAN.md evidence explicitly
- DA-005: Acknowledge that session quality improvements could be explained by multiple variables, not specifically negative prompting
- DA-006: Apply the epistemological ground rule consistently by noting where the document itself uses absence-of-positive-framing as evidence

**P2 (Minor — may resolve):**
- DA-007: Clarify the scope of the AGREE-4/HARD rule comparison more carefully

---

## S-004 Pre-Mortem

**Strategy:** S-004 Pre-Mortem Analysis
**H-16 Compliance:** S-003 Steelman confirmed
**Finding Prefix:** PM

### Failure Declaration

It is August 2026. The supplemental vendor evidence report was rejected by the Phase 2 research team as inadequate to motivate the controlled experiment. The PROJ-014 research project has stalled. We are investigating why the supplemental evidence failed to make its case.

### Failure Cause Inventory

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-i1 | The 32/33 count discrepancy was noticed by reviewers and used to dismiss the entire evidence catalog as carelessly assembled | Process | High | Critical | P0 | Evidence Quality |
| PM-002-i1 | The "Anthropic contradicts its own guidance" argument was dismissed as unfalsifiable or as a category error (different audiences, different purposes) without the report having anticipated this objection | Assumption | High | Major | P1 | Methodological Rigor |
| PM-003-i1 | The Phase 2 experimental design's sample size (n=50) was criticized by a statistician as inadequate; the missing power calculation made it impossible to defend | Technical | Medium | Critical | P0 | Methodological Rigor |
| PM-004-i1 | The session empirical evidence (EO-001 through EO-003) was rejected as confounded — reviewers noted that quality trajectory improvements could be caused by specialized agents, templates, or quality gates rather than negative prompting specifically | Assumption | High | Major | P1 | Evidence Quality |
| PM-005-i1 | The self-referential nature of the Jerry Framework evidence (researcher's own design) undermined credibility; the report failed because it did not acknowledge this as a limitation | Process | Medium | Major | P1 | Internal Consistency |
| PM-006-i1 | The "Innovator's Gap" argument was rejected as unfalsifiable — by design, its core claim (effective techniques are not published) cannot be verified | Assumption | Medium | Major | P1 | Methodological Rigor |
| PM-007-i1 | The hypothesis reformulations at the end of the document (three reframings) confused reviewers about what Phase 2 is actually testing | Process | Low | Minor | P2 | Actionability |

### Mitigation Plan

**P0 (Critical):**
- PM-001-i1: Fix 32/33 count immediately before any further review
- PM-003-i1: Either show the power calculation supporting n=50 or revise upward to n=120+ with correct derivation

**P1 (Major):**
- PM-002-i1: Add a section explicitly addressing "alternative explanations for the divergence between recommendation and practice" — the report should anticipate the most obvious counterargument
- PM-004-i1: Add explicit confound acknowledgment to EO-001: list all variables (agents, templates, quality gates) that co-varied with the negative-constraint regime and note that they cannot be isolated
- PM-005-i1: Reframe Jerry Framework evidence as "practitioner self-report about design intent" rather than independent production system observation
- PM-006-i1: Bound the Innovator's Gap argument more carefully — limit it to "explaining why the literature null finding is expected, not why negative prompting works"

---

## S-001 Red Team

**Strategy:** S-001 Red Team Analysis
**H-16 Compliance:** S-003 Steelman confirmed
**Finding Prefix:** RT

### Threat Actor Profile

**Goal:** Discredit the supplemental evidence report and prevent the Phase 2 experiment from being funded/executed.
**Capability:** A methodology-literate critic with knowledge of research design, statistics, and epistemology who has read the Barrier 1 synthesis.
**Motivation:** The critic believes the hypothesis is motivated reasoning and wants to show that the evidence base is fabricated from circular self-reference.

### Attack Vector Inventory

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-------------------|
| RT-001-i1 | Circular self-reference attack: The report cites the Jerry Framework (the researcher's own system) as "production evidence," then cites PLAN.md (the researcher's own choices) as evidence, then cites EO-001 (the researcher's own session) as evidence — the entire evidence base is the researcher observing themselves | Boundary | High | Critical | P0 | Missing | Evidence Quality |
| RT-002-i1 | Unfalsifiability attack: The Innovator's Gap argument (IG-001) is structurally unfalsifiable. The claim "effective techniques are not published" cannot be verified or refuted. An adversary can exploit this to dismiss the entire Section 4 argument | Ambiguity | High | Major | P1 | Partial (acknowledged as inference) | Methodological Rigor |
| RT-003-i1 | Count manipulation attack: The 32/33 discrepancy can be used to challenge the entire NC-001 through NC-033 catalog. If the count is wrong in the header, which instances were missed or double-counted? | Boundary | High | Major | P1 | Missing | Evidence Quality |
| RT-004-i1 | Confound exploitation: EO-001 quality trajectory can be explained entirely by the adversary quality gate mechanism (the very mechanism the PROJ-014 project has built to enforce quality) — negative prompting is confounded with structured adversarial review | Circumvention | High | Major | P1 | Partial (explicitly disclaimed but then cited anyway) | Methodological Rigor |
| RT-005-i1 | Selection bias attack: The report only examines Claude Code behavioral rules (one system, one vendor, one use case). An adversary would demand: "Show me the positive-framing enforcement systems that also work." | Ambiguity | Medium | Minor | P2 | Partial (Innovator's Gap argument provides partial defense) | Completeness |

### Countermeasures

**P0:**
- RT-001-i1: The self-referential evidence base is the most critical vulnerability. The report must explicitly acknowledge it as a limitation and explicitly label all three evidence sources (Jerry Framework, PLAN.md, Session EO) as "practitioner self-report" — then argue that practitioner self-report is valuable even if not independent. The current framing attempts to present self-report as "direct observation" which is technically accurate but glosses over the independence problem.

**P1:**
- RT-002-i1: Bound the Innovator's Gap to explanatory use only (explaining the literature null finding); remove any implication that it constitutes positive evidence for negative prompting effectiveness
- RT-003-i1: Fix 32/33 count and add a note acknowledging the discrepancy was caught in review
- RT-004-i1: Explicitly acknowledge that EO-001 cannot distinguish the effect of negative prompting from the effect of the C4 adversarial quality gate

---

## S-007 Constitutional AI Critique

**Strategy:** S-007 Constitutional AI Critique
**Finding Prefix:** CC
**Constitutional Context:** quality-enforcement.md H-01 through H-33, Jerry Constitution P-001 through P-043, markdown-navigation-standards.md

### Applicable Principles

For a supplemental evidence report (document deliverable):
- H-23 (NAV-001): Navigation table required for documents >30 lines
- H-31 (Ambiguity): Claims should be unambiguous; scope should be clear
- P-001 (Truth/Accuracy): All factual claims must be accurate
- P-004 (Provenance): Source attribution for all evidence
- P-011 (Evidence-Based): Evidence must support claims
- P-022 (No Deception): Must not misrepresent confidence, capabilities, or findings

### Principle-by-Principle Evaluation

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-i1 | H-23 Navigation Table | HARD | Compliant | Navigation table present at lines 10-22 | N/A |
| CC-002-i1 | P-001 (Truth/Accuracy) — Count Discrepancy | HARD | Major | Navigation table says "32 NEVER/MUST NOT/FORBIDDEN/DO NOT instances" while body says "33 observable negative constraint instances" — one of these is inaccurate | Internal Consistency |
| CC-003-i1 | P-001 (Truth/Accuracy) — Power Calculation | HARD | Major | "Power calculation: detect 15% effect with 80% power at alpha=0.05" citing n=50 — standard power analysis for paired binary data (McNemar's test) with 15% effect at alpha=0.05 and 80% power requires approximately n=115-130, not n=50. The stated sample size is materially incorrect if the power claim is accurate | Methodological Rigor |
| CC-004-i1 | P-011 (Evidence-Based) — Mechanism Claim | MEDIUM | Major | Lines 372-373: "is the mechanism through which major AI vendors achieve reliable behavioral compliance" — this causal mechanism claim is not supported by the evidence presented (which is observational correlation only) | Evidence Quality |
| CC-005-i1 | P-022 (No Deception) — Epistemic Framing | SOFT | Minor | The document has an excellent "What cannot be inferred" section but the Implications section then uses language that goes slightly beyond what can be inferred from the evidence | Methodological Rigor |
| CC-006-i1 | P-004 (Provenance) — EO Evidence | MEDIUM | Compliant | Session empirical evidence is attributed to adversary-gate.md and synthesis.md with line numbers | N/A |
| CC-007-i1 | H-23 Anchor Links | HARD | Compliant | Navigation table uses anchor links | N/A |

### Constitutional Compliance Score

Violations: 0 Critical + 2 Major (CC-002, CC-003, CC-004 counted at MEDIUM for P-011) + 1 Minor (CC-005)
Score: 1.00 - (0 × 0.10) - (2 × 0.05) - (1 × 0.02) = 1.00 - 0.10 - 0.02 = **0.88 (REVISE)**

Note: The two Major findings (CC-002 count error; CC-003 power calculation error) are factual accuracy concerns that can be corrected without structural change to the document.

---

## S-011 Chain-of-Verification

**Strategy:** S-011 Chain-of-Verification
**Finding Prefix:** CV
**Claims Extracted:** 12 | **Independently Verifiable:** 8 | **Requiring Source Access:** 4

### Claim Inventory and Verification

| ID | Claim (from deliverable) | Source | Result | Severity |
|----|--------------------------|--------|--------|----------|
| CV-001-i1 | "32 NEVER/MUST NOT/FORBIDDEN/DO NOT instances across 10 rule files" (nav table) | Nav table vs. body | MATERIAL DISCREPANCY — body says 33; table NC-001 through NC-033 confirms 33 | Major |
| CV-002-i1 | "Synthesis from I-1/C-1 (Anthropic prompting docs, platform.claude.com) and C-2 (Anthropic prompt engineering blog, claude.com/blog)" (line 101) | Synthesis.md Group I catalog | Partially verifiable — synthesis.md is referenced as a source but independently verifying I-1/C-1 designations would require reading synthesis.md directly; document accepts on faith | Minor |
| CV-003-i1 | "power calculation: detect 15% effect with 80% power at alpha=0.05" supporting n=50 (line 308) | Statistical methods textbook / power analysis | MATERIAL DISCREPANCY — McNemar's test with 15% effect (proportion difference), alpha=0.05, power=0.80 requires approximately n=115-130 matched pairs, not 50. The claim as stated is statistically incorrect. | Critical |
| CV-004-i1 | "L2-REINJECT mechanism is explicitly documented in quality-enforcement.md (enforcement architecture table) as 'Immune' to context rot" (line 112) | quality-enforcement.md enforcement architecture table | VERIFIED — quality-enforcement.md enforcement architecture table shows L2 as "Immune" and L1 as "Vulnerable" | Compliant |
| CV-005-i1 | "Score trajectory 0.83 → 0.90 → 0.93 → 0.953 (PASS)" (line 197-198, EO-001) | adversary-gate.md lines 36-41 | Referenced but not independently verifiable without reading adversary-gate.md; accepted as stated | Minor |
| CV-006-i1 | HARD tier vocabulary: "MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL — Cannot override — <= 25" (line 121) | quality-enforcement.md Tier Vocabulary section | VERIFIED — quality-enforcement.md Tier Vocabulary table contains this exact text | Compliant |
| CV-007-i1 | "33 observable negative constraint instances across 10 rule files" (line 94) | NC-001 through NC-033 table | VERIFIED — counting NC-001 through NC-033 in the table yields exactly 33 entries | Compliant |
| CV-008-i1 | "synthesis.md AGREE-4...user expertise: expert prompt engineers who understand model-specific constraint design may achieve better compliance with prohibition-style instructions than non-expert users. None of the studies cited in AGREE-4 control for this variable." (lines 252-255) | synthesis.md AGREE-4, lines 284-285 | Referenced line numbers provided; accepted as stated | Minor |

### Finding Details

**CV-001-i1: Navigation Table Count Discrepancy [MAJOR]**

- **Claim (deliverable):** Navigation table, line 17: "32 NEVER/MUST NOT/FORBIDDEN/DO NOT instances across 10 rule files"
- **Independent verification:** Body line 94 says "33 observable negative constraint instances"; the NC table runs NC-001 through NC-033 = 33 entries
- **Discrepancy:** Navigation table is off by one (32 vs 33). The body is correct; the navigation table was not updated.
- **Correction:** Change nav table line 17 to: "33 NEVER/MUST NOT/FORBIDDEN/DO NOT instances across 10 rule files"

**CV-003-i1: Sample Size Power Calculation [CRITICAL]**

- **Claim (deliverable):** Line 308: "Sample size: 50 matched prompt pairs minimum — Power calculation: detect 15% effect with 80% power at alpha=0.05"
- **Independent verification:** For McNemar's test on paired binary outcomes, power analysis with discordant pair proportion (p_12 + p_21) needs to be estimated. With a 15% overall effect difference and a conservative estimate of 30% discordant pairs, n=50 achieves approximately 55-60% power. Achieving 80% power requires approximately n=115-130. (Standard formula: n ≈ (z_α + z_β)² / (p_12 + p_21) where z_0.05 = 1.96, z_0.20 = 0.84.)
- **Discrepancy:** The document states n=50 achieves 80% power at 15% effect with alpha=0.05. This is incorrect by approximately a factor of 2.5.
- **Correction:** Either (a) correct n to ~120+ with derivation, or (b) remove the power claim and state "n=50 as preliminary/pilot estimate" with acknowledgment that a formal power calculation requires empirical estimation of the discordant pair proportion from a pilot study.

---

## S-012 FMEA

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Finding Prefix:** FM
**Elements Analyzed:** 8 | **Failure Modes Identified:** 14

### Element Decomposition

| Element | Description |
|---------|-------------|
| E1 | Epistemic Framing section |
| E2 | Evidence Category 1 (VS-001 through VS-004) |
| E3 | Evidence Category 2 (JF-001, JF-002) |
| E4 | Evidence Category 3 (EO-001 through EO-003) |
| E5 | Evidence Category 4 (IG-001 through IG-003) |
| E6 | Controlled A/B Experimental Design |
| E7 | Implications for the Hypothesis |
| E8 | Summary Evidence Table |

### FMEA Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|---------------------|
| FM-001-i1 | E2 (VS-001 catalog) | Incorrect count in nav table (32 vs 33): a reader's first impression of the evidence catalog is inaccurate | 6 | 10 | 3 | 180 | Major | Evidence Quality |
| FM-002-i1 | E6 (A/B design) | Power calculation claim is factually incorrect (n=50 does not achieve 80% power for 15% effect) | 9 | 9 | 4 | 324 | Critical | Methodological Rigor |
| FM-003-i1 | E3 (JF-001) | Self-referential evidence: researcher's own design choices cited as independent production evidence | 7 | 8 | 5 | 280 | Critical | Evidence Quality |
| FM-004-i1 | E7 (Implications) | Mechanism claim asserted without causal support ("is the mechanism through which...") | 7 | 7 | 4 | 196 | Major | Methodological Rigor |
| FM-005-i1 | E4 (EO-001) | Confounding variables not isolated: quality gate, specialized agents, templates co-vary with negative prompting | 7 | 9 | 5 | 315 | Critical | Evidence Quality |
| FM-006-i1 | E5 (IG-001) | Innovator's Gap argument is unfalsifiable — cannot be distinguished from motivated reasoning | 6 | 7 | 6 | 252 | Critical | Methodological Rigor |
| FM-007-i1 | E1 (Epistemic Framing) | "Epistemological ground rule" in the framing (absence≠absence) is not applied consistently in the document itself | 5 | 6 | 5 | 150 | Major | Internal Consistency |
| FM-008-i1 | E6 (A/B design) | Condition C7 (positive-only baseline) vs. C3 (positive equivalent of C2) are conflated — the "structural positive equivalent" to HARD-tier negative constraints may not simply be positive paraphrases | 5 | 5 | 6 | 150 | Major | Completeness |
| FM-009-i1 | E8 (Summary Table) | Evidence Tier column labels are inconsistently applied: VS-004 is "Direct observation" but JF-002 is "Direct observation" — yet JF-002 involves a researcher citing their own artifact | 4 | 4 | 7 | 112 | Major | Internal Consistency |
| FM-010-i1 | E7 (Implications) | Three competing reframings at end of document without clear guidance on which Phase 2 should prioritize | 4 | 5 | 6 | 120 | Minor | Actionability |

### Critical Findings Details

**FM-002-i1: Power Calculation Error [CRITICAL, RPN=324]**
- **Element:** Experimental Design section, line 308
- **Effect:** Phase 2 experiment designed around n=50 would be substantially underpowered; results would be statistically inconclusive even if genuine effects exist
- **Corrective Action:** Show derivation for n calculation OR state n=50 as "preliminary estimate pending pilot data" with acknowledgment of uncertainty

**FM-003-i1: Self-Referential Evidence [CRITICAL, RPN=280]**
- **Element:** Evidence Category 2 (JF-001)
- **Effect:** The independence of the "production system observation" is compromised; the report relies on the researcher observing their own system and interpreting their own design choices
- **Corrective Action:** Reframe JF-001 as "practitioner self-report" not "direct observation"; acknowledge limitation; argue that practitioner self-report is still valid evidence of a type

**FM-005-i1: Confounding Variables Unacknowledged [CRITICAL, RPN=315]**
- **Element:** Evidence Category 3 (EO-001)
- **Effect:** Quality trajectory improvement (0.83 → 0.953) is cited as supporting evidence, but cannot be attributed to negative prompting without isolating it from other causal factors
- **Corrective Action:** Add explicit confound table: list all variables co-present in the PROJ-014 session (specialized agents, C4 quality gate, structured templates, adversarial tournament) and explicitly state that session evidence cannot isolate the contribution of negative prompting framing

**FM-006-i1: Unfalsifiable IG Argument [CRITICAL, RPN=252]**
- **Element:** Innovator's Gap section
- **Effect:** An unfalsifiable argument cannot be evidence; it can only be narrative framing. If cited as evidence by Phase 2 researchers, it will damage credibility.
- **Corrective Action:** Reframe Innovator's Gap as "explanatory context for the literature null finding" rather than as evidence for the hypothesis

---

## S-013 Inversion

**Strategy:** S-013 Inversion Technique
**Finding Prefix:** IN

### Goals Stated

1. G1: Establish that the vendor self-practice evidence is meaningful and warrants Phase 2 testing
2. G2: Document four evidence categories that the survey methodology could not structurally capture
3. G3: Propose a Phase 2 experimental design that closes the evidence gap
4. G4: Appropriately bound what the supplemental evidence does and does not establish

### Anti-Goals (Inversion)

"To guarantee this report fails to justify Phase 2 testing":
- Cite evidence that is entirely self-generated by the researcher
- Make the primary evidence count wrong (32 vs 33)
- Present a statistically invalid experimental design
- Assert causality without controlling confounds
- Build the argument on unfalsifiable premises

**Assessment:** The report has partially realized three of these five anti-goal conditions (self-generated evidence with insufficient labeling, incorrect count, invalid power calculation). The causality claim is partially realized (mechanism language in Implications). The unfalsifiable premise (Innovator's Gap) is partially addressed by labeling it as inference.

### Assumption Map and Stress-Test

| ID | Assumption | Type | Confidence | Inversion | Severity | Affected Dimension |
|----|------------|------|------------|-----------|----------|--------------------|
| IN-001-i1 | Production system observation is higher evidence tier than published literature | Methodological | Medium | If this tier assignment is wrong (production system obs = anecdote), entire VS/JF evidence category is downgraded to anecdote | Critical | Methodological Rigor |
| IN-002-i1 | Anthropic engineers chose negative framing deliberately rather than by convention | Methodological | Low | If they chose it by convention (e.g., "NEVER" is standard legal/policy language), then VS-002 has no evidential weight | Major | Evidence Quality |
| IN-003-i1 | The gap between Anthropic's recommendation and practice is observable and meaningful | Observational | High | Partially validated by direct file observation; this assumption holds | Compliant | N/A |
| IN-004-i1 | n=50 matched pairs is sufficient for the proposed statistical test | Statistical | Low | Power analysis shows n=50 is insufficient (see CV-003); assumption fails | Critical | Methodological Rigor |
| IN-005-i1 | The Jerry Framework constitutes a "production system" in the relevant sense | Definitional | Medium | If "production system" requires multi-user deployment, external users, or independent maintenance, the Jerry Framework may not qualify | Major | Evidence Quality |
| IN-006-i1 | The Innovator's Gap exists in general (effective NLP techniques are not published) | Empirical | Low | This is not empirically verifiable by definition; treating it as an assumption reveals it is actually an assertion | Major | Methodological Rigor |

### Finding Details

**IN-001-i1: Production System Evidence Tier [CRITICAL]**

The document asserts that direct observation of a production system is "the highest tier of empirical evidence in engineering disciplines" (line 37). This claim requires defense:
- In engineering, "production system observation" is indeed considered strong evidence when the system is independently deployed at scale, the observer is independent, and the observations are replicable
- In this case: the "production system" is small-scale (one user), the observer is the designer, and the observations are not replicable by independent parties
- **Mitigation:** Explicitly defend the evidence tier claim or downgrade it. State: "Production system observation has high evidential value when (a) the system operates at scale, (b) the observer is independent, and (c) observations are replicable. This report's evidence meets condition (c) — the rule files can be independently read — but is limited on conditions (a) and (b). Its evidential value lies in demonstrating that the mechanism exists and has been deliberately engineered, not in establishing effectiveness."

**IN-004-i1: Statistical Power [CRITICAL]**

The n=50 assumption fails stress-testing. See CV-003 for the power calculation. This is the most immediately correctable critical finding.

**IN-002-i1: Deliberate Choice vs. Convention [MAJOR]**

The argument that Anthropic's use of NEVER/MUST NOT is an "engineering decision based on what works" (line 108) assumes deliberate choice over convention. Alternative: legal and policy documents routinely use "NEVER" and "MUST NOT" for reasons of precision and unambiguity, not because they have been shown to be more effective than positive framing in the target domain. The report should acknowledge this alternative explanation.

---

## S-014 LLM-as-Judge

**Strategy:** S-014 LLM-as-Judge
**Finding Prefix:** LJ
**Deliverable Type:** Supplemental Research Evidence Report
**Criticality:** C4

### Leniency Bias Counteraction Statement

This is a C4 tournament review with a threshold of 0.95. I will apply the rubric strictly. When uncertain between adjacent scores, I will choose the lower score. I will not give credit for intentions — only for what is demonstrated in the document.

### Step 2: Per-Dimension Scoring

**Dimension 1: Completeness (weight: 0.20)**

The document covers four distinct evidence categories with clear structure. All findings are documented with source citations. The experimental design is detailed and operationalized. The "What Cannot Be Inferred" section demonstrates epistemic completeness. A navigation table is present.

Gaps: The power calculation is missing (critical for completeness of the experimental design section). The confound acknowledgment for session evidence is stated in "What cannot be inferred" but not elaborated per confound variable. The self-referential nature of the evidence base is not explicitly labeled in the evidence categories themselves.

Score: **0.86/1.00** — Strong coverage overall; power calculation gap and confound detail gap reduce from exceptional to strong.

**Dimension 2: Internal Consistency (weight: 0.20)**

Major finding: The navigation table says 32 instances; the body says 33. This is an internal numerical inconsistency in the primary evidence count.

Secondary finding: The epistemological ground rule ("absence of evidence is not evidence of absence") is stated in the framing but then appears to be inconsistently applied in the Implications section, which uses the negative-constraint evidence presence to imply effectiveness.

The "What cannot be inferred" section is well-handled and consistent with the epistemic framing — this is a strength.

Score: **0.82/1.00** — The 32/33 discrepancy and epistemological framing tension are material inconsistencies that prevent a higher score despite otherwise good internal logic.

**Dimension 3: Methodological Rigor (weight: 0.20)**

Strengths: The four evidence categories are clearly defined and scoped. The distinction between "what can be observed" and "what cannot be inferred" is methodologically sound. The AGREE-5 taxonomy from synthesis.md is correctly applied to position the Jerry Framework evidence. The H-16 ordering of evidence presentation (observation before interpretation) is followed.

Weaknesses: The power calculation error (n=50 for 80% power at 15% effect is incorrect by approximately 2.5x). The mechanism claim in the Implications section asserts causality from observational data. The evidence tier claim for production system observation is asserted without defense of the tiers used. The self-referential evidence is presented without independent-observer qualification.

Score: **0.80/1.00** — Multiple methodological issues: power calculation error (most severe), mechanism claim overcorrection, undefended evidence tier hierarchy.

**Dimension 4: Evidence Quality (weight: 0.15)**

Strengths: The NC-001 through NC-033 catalog is methodical and fully cited with file names and line numbers. The VS-002 finding correctly distinguishes between published guidance and engineering practice. The EO-001 through EO-003 evidence is appropriately caveated.

Weaknesses: The primary evidence base (Jerry Framework, PLAN.md, session observations) is generated by the researcher themselves. This is not hidden — it is presented as direct observation — but the independence limitation is not explicitly labeled. This is the most significant evidence quality concern: the document presents self-generated evidence as "production system observation" without adequately flagging the independence problem.

Score: **0.82/1.00** — Substantial evidence well-cited; independence limitation of self-generated evidence is partially addressed but needs more explicit treatment.

**Dimension 5: Actionability (weight: 0.15)**

Strengths: The Phase 2 experimental design is highly operationalized: conditions C1-C7 are defined, primary and secondary outcome measures are specified, sample size stated, statistical tests named. The three hypothesis reframings provide Phase 2 design inputs. The "What does not establish" section at the end is actionable for reviewers.

Weaknesses: The n=50 sample size is incorrect (see above); acting on this would produce an underpowered study. The three competing hypothesis reframings at the end do not specify which should be the primary Phase 2 question vs. secondary. This creates ambiguity for the team executing Phase 2.

Score: **0.88/1.00** — Strong actionability for the experimental design; reduced by the incorrect sample size and ambiguity about primary vs. secondary hypothesis.

**Dimension 6: Traceability (weight: 0.10)**

Strengths: Most evidence is cited with specific file paths and line numbers (NC-001 through NC-033 with file names; JF-002 with PLAN.md lines 36-48; EO-001 with adversary-gate.md lines 36-41). The Summary Evidence Table at the end consolidates all 12 findings with source attribution. The provenance back to the Barrier 1 synthesis is clear.

Weaknesses: The I-1/C-1, C-2 designations (line 101) reference synthesis.md's catalog but a reader would need to read synthesis.md to verify these attributions. Minor in context.

Score: **0.92/1.00** — Strong traceability with specific file and line citations; minor gap in synthesis catalog traceability.

### Step 3: Weighted Composite

```
Completeness:          0.86 × 0.20 = 0.172
Internal Consistency:  0.82 × 0.20 = 0.164
Methodological Rigor:  0.80 × 0.20 = 0.160
Evidence Quality:      0.82 × 0.15 = 0.123
Actionability:         0.88 × 0.15 = 0.132
Traceability:          0.92 × 0.10 = 0.092

Composite = 0.172 + 0.164 + 0.160 + 0.123 + 0.132 + 0.092 = 0.843
```

**Composite Score: 0.84**

### Step 4: Verdict

Threshold: >= 0.95 (project PLAN.md C4 standard)
Standard H-13 threshold: >= 0.92

Score 0.84 is below both thresholds.
Verdict: **REVISE**

No dimension has a Critical finding (score <= 0.50), so no override applies. The lowest dimension is Methodological Rigor (0.80), followed by Internal Consistency and Evidence Quality (0.82 each).

### Step 5: Improvement Recommendations

Priority-ordered by weighted impact:

| Priority | Dimension | Current Score | Target | Recommendation |
|----------|-----------|---------------|--------|----------------|
| 1 | Methodological Rigor (0.20) | 0.80 | 0.90+ | (a) Fix power calculation: correct n=50 to n~120+ with derivation OR state as "preliminary estimate"; (b) Replace mechanism language "is the mechanism through which" with "appears consistent with the hypothesis that..."; (c) Defend the evidence tier hierarchy for production system observation |
| 2 | Internal Consistency (0.20) | 0.82 | 0.90+ | Fix 32/33 count discrepancy in navigation table; add note about epistemological ground rule consistency |
| 3 | Evidence Quality (0.15) | 0.82 | 0.90+ | Explicitly label self-generated evidence (Jerry Framework, PLAN.md, session EO) as "practitioner self-report" and address the independence limitation directly in the evidence presentation |
| 4 | Completeness (0.20) | 0.86 | 0.92+ | Add confound table to EO-001 listing all co-varying variables in the PROJ-014 session |
| 5 | Actionability (0.15) | 0.88 | 0.92+ | Clarify which hypothesis reframing is primary for Phase 2; fix n if power calculation corrected |

---

## Tournament Summary

## Findings Summary

| ID | Severity | Finding | Source Strategy | Section |
|----|----------|---------|-----------------|---------|
| SR-001-i1 / CV-001-i1 | Major | Nav table says 32 instances; body says 33 | S-010, S-011 | Navigation table vs. Evidence Category 1 |
| CV-003-i1 / FM-002-i1 | **Critical** | Power calculation n=50 is statistically incorrect for stated effect/power/alpha | S-011, S-012 | Controlled A/B Experimental Design |
| FM-003-i1 / RT-001-i1 | **Critical** | Self-referential evidence base lacks independence labeling | S-012, S-001 | Evidence Categories 2, 3 |
| FM-005-i1 / DA-005-i1 | **Critical** | Session EO evidence confounded; causal attribution to negative prompting not possible | S-012, S-002 | Evidence Category 3 |
| FM-006-i1 / RT-002-i1 | **Critical** | Innovator's Gap argument is unfalsifiable; must be reframed from evidence to narrative context | S-012, S-001 | Evidence Category 4 |
| DA-001-i1 | **Critical** | Practitioner-contradicts-guidance framing may be unfalsifiable without alternative explanation | S-002 | Evidence Category 1 (VS-002) |
| SR-002-i1 / CC-004-i1 | Major | Mechanism claim asserts causality not supported by observational evidence | S-010, S-007 | Implications for the Hypothesis |
| IN-001-i1 | Major | Evidence tier claim for production system observation is asserted without defense | S-013 | Epistemic Framing |
| IN-002-i1 / DA-002-i1 | Major | "Deliberate choice" vs. "convention" not addressed; alternative explanation for NEVER/MUST NOT vocabulary not considered | S-013, S-002 | Evidence Category 1 (VS-002) |
| DA-004-i1 | Major | PLAN.md evidence is self-referential (researcher citing own behavior as evidence) | S-002 | Evidence Category 2 (JF-002) |
| PM-002-i1 | Major | Most damaging counterargument (divergence = different audiences, not evidence of effectiveness) not preempted | S-004 | Evidence Category 1 |
| FM-007-i1 / DA-006-i1 | Major | Epistemological ground rule not applied consistently within the document itself | S-012, S-002 | Epistemic Framing vs. Implications |
| SR-004-i1 / CC-003-i1 | Major | Power calculation stated without derivation; n=50 is underpowered | S-010, S-007 | Controlled A/B Design |
| FM-009-i1 | Minor | Summary Evidence Table "Evidence Tier" labels inconsistent (self-generated obs vs. external obs conflated) | S-012 | Summary Evidence Table |
| SR-005-i1 | Minor | Tension between epistemic caution in body and hypothesis upgrade in Implications | S-010 | Implications |
| IN-005-i1 | Minor | Jerry Framework as "production system" — definitional scope not defended | S-013 | Evidence Category 2 |

## S-014 Score Card

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.86 | 0.172 |
| Internal Consistency | 0.20 | 0.82 | 0.164 |
| Methodological Rigor | 0.20 | 0.80 | 0.160 |
| Evidence Quality | 0.15 | 0.82 | 0.123 |
| Actionability | 0.15 | 0.88 | 0.132 |
| Traceability | 0.10 | 0.92 | 0.092 |
| **Composite** | **1.00** | **0.84** | **0.843** |

## Verdict: REVISE

**Threshold:** 0.95 (project PLAN.md) / 0.92 (H-13 standard)
**Score:** 0.84
**Result:** BELOW THRESHOLD — REVISE

The deliverable is substantively strong in its core architecture: the four evidence categories are well-structured, the evidence is specifically cited, the experimental design is operationalized, and the epistemic caution in the "What cannot be inferred" section is exemplary. The deficiencies are concentrated in methodological rigor and consistency, and are correctable.

## Prioritized Fix List for I2 Revision

The following fixes are ordered by weighted impact on the composite score. Addressing items 1-5 should be sufficient to reach the 0.92 threshold; items 1-7 should reach or exceed 0.95.

**Priority 1 — CRITICAL — Fix Power Calculation (Methodological Rigor +0.08-0.10)**

The n=50 sample size claim with 80% power at 15% effect and alpha=0.05 is statistically incorrect. McNemar's test for paired binary outcomes with these parameters requires approximately n=115-130 matched pairs. Either:
- (a) Correct the sample size to n=120 minimum with the derivation shown, or
- (b) Replace the power claim with: "n=50 as a preliminary estimate for pilot feasibility; formal power analysis requires empirical estimation of the discordant pair proportion from a pilot study of 20-30 pairs"

**Priority 2 — CRITICAL — Resolve Count Discrepancy (Internal Consistency +0.06-0.08)**

Change navigation table line 17 from "32 NEVER/MUST NOT/FORBIDDEN/DO NOT instances" to "33 NEVER/MUST NOT/FORBIDDEN/DO NOT instances across 10 rule files" to match the body count and the NC-001 through NC-033 table.

**Priority 3 — CRITICAL — Label Evidence Independence Limitation (Evidence Quality +0.05-0.07)**

Add an explicit "Evidence Independence Note" at the top of Evidence Categories 2 and 3:
- For JF-001/JF-002: "Note: This evidence is practitioner self-report. The researcher is citing their own design choices. This is not independent observation. Its evidential value is as documented design intent, not as external validation."
- For EO-001/EO-002/EO-003: Add a confound table: "Variables co-present in PROJ-014 session that may explain quality outcomes: (a) Specialized skill agents, (b) C4 adversarial quality gate (10-strategy tournament), (c) Structured templates and protocols, (d) Negative-constraint prompting regime. Session evidence cannot isolate contribution (d) from (a)-(c)."

**Priority 4 — CRITICAL — Reframe Innovator's Gap from Evidence to Context (Methodological Rigor +0.04)**

Change the Innovator's Gap section header/framing from "Evidence Category 4" to "Contextual Framing" or "Explanatory Context" and add a sentence at the top of IG-001: "The following section explains why the literature null finding (Barrier 1 synthesis) does not refute the hypothesis; it does not constitute direct evidence that negative prompting works. It is structural context for interpreting the absence of published evidence."

**Priority 5 — CRITICAL — Preempt Alternative Explanation for Practitioner/Guidance Divergence (Methodological Rigor +0.03-0.04)**

In VS-002, add an "Alternative Explanations" subsection explicitly addressing:
- "The divergence could be explained by: (1) Different audiences — guidance for novice users, enforcement for system designers; (2) Different purposes — guidance for one-shot prompting, enforcement for persistent behavioral compliance; (3) Convention — legal/policy documents traditionally use NEVER/MUST NOT for precision. These alternatives do not refute the main observation but should be acknowledged before concluding that the divergence constitutes evidence of effectiveness."

**Priority 6 — MAJOR — Replace Mechanism Language with Observational Language (Methodological Rigor +0.03)**

Replace lines 372-373: "are the primary mechanism by which LLM behavioral compliance is achieved in production systems" with: "appear to function as the primary enforcement mechanism in at least one production system (the Jerry Framework), consistent with the hypothesis that structured negative constraints improve behavioral compliance. Whether this generalizes to other systems requires the Phase 2 experiment."

**Priority 7 — MAJOR — Defend Evidence Tier Hierarchy (Methodological Rigor +0.02-0.03)**

Add a sentence to the Epistemic Framing section defending the claim that production system observation is "highest tier of empirical evidence in engineering disciplines": "This tier ranking applies when: (a) the system is deployed at scale with real users and consequences, (b) the observer is independent from the system designer, and (c) the observations are replicable. The evidence in this report satisfies condition (c) — the rule files are publicly readable — but is limited on conditions (a) and (b). Its evidential value is as documented engineering practice, not as statistical proof of effectiveness."

## Execution Statistics

- **Total Findings:** 16 (across all strategies)
- **Critical:** 5 (power calculation error, self-referential evidence labeling, session confounds, IG unfalsifiability, guidance-practice divergence framing)
- **Major:** 9
- **Minor:** 2
- **Protocol Steps Completed:** All 10 strategies (S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013, S-014)
- **H-16 Compliance:** Confirmed — S-003 executed before S-002, S-004, S-001
- **Composite Score (I1):** 0.84
- **Threshold:** 0.95 (project) / 0.92 (H-13)
- **Verdict:** REVISE

---

*adv-executor | PROJ-014 | Barrier 1 Supplemental C4 Tournament | 2026-02-27*
*Strategy execution report persisted per P-002*
*H-15 self-review applied: findings have specific evidence, severity classifications are justified, identifiers follow prefix format, summary table matches detailed findings, no findings minimized*
