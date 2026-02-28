# C4 Adversary Tournament Execution Report: Iteration 1
## Claim Validation Analysis — "Negative Prompting Reduces Hallucination by 60%"

> adv-executor | C4 Tournament Iteration 1 | PROJ-014 | 2026-02-27
> Deliverable: phase-2/claim-validation.md (TASK-005)
> Strategies executed: 10 of 10 (S-010, S-003, S-002, S-004, S-001, S-007, S-011, S-012, S-013, S-014)
> Quality Gate: >= 0.95 (C4)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy order, H-16 compliance, tournament configuration |
| [S-010: Self-Refine](#s-010-self-refine) | Self-review findings |
| [S-003: Steelman](#s-003-steelman) | Argument reconstruction |
| [S-002: Devil's Advocate](#s-002-devils-advocate) | Counter-argument findings |
| [S-004: Pre-Mortem](#s-004-pre-mortem) | Failure mode findings |
| [S-001: Red Team](#s-001-red-team) | Adversarial attack findings |
| [S-007: Constitutional AI](#s-007-constitutional-ai) | Constitutional compliance findings |
| [S-011: Chain-of-Verification](#s-011-chain-of-verification) | Factual claim verification |
| [S-012: FMEA](#s-012-fmea) | Component failure mode analysis |
| [S-013: Inversion](#s-013-inversion) | Assumption stress-test findings |
| [S-014: LLM-as-Judge](#s-014-llm-as-judge) | Final composite score |
| [Consolidated Findings](#consolidated-findings) | All findings cross-referenced by severity |
| [Tournament Summary](#tournament-summary) | Verdict and remediation roadmap |

---

## Execution Context

- **Strategy:** C4 Tournament (all 10 selected strategies)
- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-2/claim-validation.md`
- **Criticality:** C4 (Critical — research claim validation with experimental design implications)
- **Executed:** 2026-02-27
- **Quality Gate:** >= 0.95 weighted composite (C4)
- **H-16 Compliance:** S-010 (self-review, no H-16 prerequisite) → S-003 (Steelman) → critique strategies (S-002, S-004, S-001, S-007, S-011, S-012, S-013) → S-014 (scoring)
- **Leniency Bias Counteraction:** Applied throughout. Scores not inflated. Gaps not excused. No rounding to threshold.

---

## S-010: Self-Refine

**Finding Prefix:** SR | **Execution ID:** i1-20260227

### Objectivity Assessment

Reviewer attachment level: Low (external reviewer; no authorship investment). Proceeding with full systematic critique per all 6 dimensions.

### Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-i1 | PROJ-006 exclusion not propagated to all comparative claims — first-pass rate metric misrepresented | Major | "First-pass rate: 0% (0.83 < 0.95 threshold)" applies only to individual deliverable pairs; the document lacks first-pass rate across the full PROJ-014 portfolio (only 2 data points used) | Completeness |
| SR-002-i1 | Discordant proportion assumption (π_d = 0.30) is not sourced or justified beyond being a "planning estimate" | Major | "The 0.30 discordant proportion assumption [...] is a planning estimate, not an empirically derived figure" — no source, prior literature, or comparable study cited to ground this choice | Evidence Quality |
| SR-003-i1 | McNemar formula is quoted without citation of statistical authority beyond parenthetical (Agresti 2013, §10.1) — the continuity correction formula is reproduced but not verified | Minor | Formula block uses `n_cc = n_unadj + z²_α/2 x (p_12 + p_21) / (4 x (p_12 − p_21)²)` without derivation or verification reference | Methodological Rigor |
| SR-004-i1 | The "PROJ-007 summary statistics" conflates Barrier 3 and Barrier 4 first-pass averages into a single "0.92" figure that does not appear in the underlying data | Major | "Average first-pass score: 0.87 [...] PROJ-007 higher first-pass" — but the PROJ-007 "first-pass average" of 0.92 is itself an average of 0.905 (Barrier 3) and 0.936 (Barrier 4), not a single measurement | Internal Consistency |
| SR-005-i1 | The "Score delta I1 to final" comparison row has an arithmetic notation error: PROJ-014 delta is reported as +0.115 but documented values are +0.123 (primary) and +0.108 (supplemental) — the average is +0.1155, rounded to +0.115 without explanation | Minor | Comparison Table row: "Score delta (I1 to final): PROJ-014 +0.115 average" vs. documented +0.123 and +0.108 | Internal Consistency |
| SR-006-i1 | The document does not assess whether the 7-condition experimental design has adequate statistical power to detect each condition pair — only C2 vs. C3 power is derived; C1, C4, C5, C6, C7 conditions receive no power analysis | Major | "Primary comparison for the pilot: C2 vs. C3" — no power analysis for secondary condition comparisons that the document directs should "gather directional signal on all conditions" | Completeness |
| SR-007-i1 | The adversarial quality checks section (S-013, S-004, S-003 inline) is not labeled as prior-iteration analysis — it appears to be generated as part of TASK-005 creation, not as a separate adversarial pass. The self-review date and agent applying these checks are undocumented | Minor | "Adversarial Quality Checks" section heading gives no date, agent ID, or iteration reference | Traceability |

### Scoring Impact (S-010)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | SR-001, SR-006: PROJ-006 exclusion not fully propagated; no power analysis for 5 of 7 experimental conditions |
| Internal Consistency | 0.20 | Negative | SR-004, SR-005: First-pass average conflation; delta arithmetic ambiguity |
| Methodological Rigor | 0.20 | Neutral | Core methodology sound; SR-003 is a minor citation gap only |
| Evidence Quality | 0.15 | Negative | SR-002: π_d = 0.30 assumption unsourced |
| Actionability | 0.15 | Positive | Recommendations for pilot and full experiment are specific and actionable |
| Traceability | 0.10 | Negative | SR-007: Inline adversarial checks lack provenance |

**Decision:** Major findings SR-001, SR-002, SR-004, SR-006 require revision. SR-003, SR-005, SR-007 are addressable in the same pass. Deliverable proceeds to S-003 per tournament sequence.

---

## S-003: Steelman

**Finding Prefix:** SM | **Execution ID:** i1-20260227

### Charitable Interpretation

The deliverable argues that the "60% hallucination reduction" claim is a null finding — untested, not disproven — and that the productive research question is not whether naive prohibition works, but whether expert-engineered structured prohibition (with consequences, L2 re-injection, constitutional triplet framing) works. This is a defensible and epistemically responsible position. The document correctly distinguishes between "absence of evidence" and "evidence of absence," explicitly identifies structural exclusions in the survey methodology, and preserves epistemic humility throughout.

The core thesis — "we do not yet know; here is how to find out" — is the appropriate scientific framing for an untested claim. The experimental design is the strongest section.

### Steelman Reconstruction Improvements

| ID | Improvement | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|--------------|-----------|
| SM-001-i1 | Strengthen the evidence hierarchy for the vendor divergence finding | Major | "VS-001 (supplemental) — Observable but requires inferential step: observation of practice ≠ evidence of effectiveness" | The VS-001 finding should be elevated by noting that Anthropic's engineers are Bayesian actors with access to private benchmarks. Their design choice is weak observational evidence but is not arbitrary — it is analogous to "revealed preference" evidence in economics, where practice choice under real-world stakes carries information even absent controlled studies. This framing strengthens the research motivation without overclaiming. | Evidence Quality |
| SM-002-i1 | Add base rate grounding for the π_d = 0.30 assumption | Critical | "The n=270 calculation rests on an assumed discordant proportion that is a planning estimate, not an empirically derived figure" | Supply comparable studies. Paired A/B prompt comparison studies in general (e.g., systematic prompt variation studies) typically observe discordant proportions of 15-40% depending on task type. The 0.30 assumption is consistent with this range. Citing a comparable study (e.g., chain-of-thought vs. zero-shot prompting paired experiments) would transform a bare assertion into a grounded estimate. | Evidence Quality |
| SM-003-i1 | Strengthen the framing of the retrospective comparison as informative despite confounding | Major | The comparison section ends by saying the data "is consistent with both the hypothesis and the null hypothesis" — accurate but epistemically flat | Add: the confound direction analysis shows ALL identified confounds favor PROJ-007, not PROJ-014. Under a Bayesian lens, observing PROJ-014's final score (0.952) within 0.5% of PROJ-007 (0.957) despite operating under harder task conditions is mild evidence AGAINST the hypothesis that negative-constraint prompting degrades performance — ruling out a specific failure mode even if not confirming the hypothesis. This is informative directionally. | Methodological Rigor |
| SM-004-i1 | Clarify the scope boundary of AGREE-4 more prominently in the executive summary | Minor | AGREE-4 is mentioned once in L0 with qualification; the qualification is buried in the L1 detail | The L0 executive summary should state explicitly: "The finding that 'prohibition is unreliable' (AGREE-4) applies to standalone blunt prohibition — Type 1 negative prompting — not to expert-engineered structured prohibition (Types 2-4). These are distinct phenomena." This prevents readers from incorrectly generalizing AGREE-4. | Completeness |
| SM-005-i1 | Surface the publication bias structural exclusion as a finding in the executive summary | Minor | SE-5 (publication bias) is listed in the absence-of-evidence table but not highlighted as a finding | Publication bias in this domain is structural: effective practitioner techniques rarely get published because they represent competitive advantage. The null finding in published literature is therefore more pronounced than the actual null finding in practice. This should be noted in L0 as a qualifier on the null result. | Evidence Quality |

### Best Case Scenario

The deliverable is strongest under these conditions: (1) the reader accepts that survey methodology has structural exclusions that prevent capture of production evidence; (2) the reader accepts that the null finding is a null finding about the published literature, not a null finding about reality; (3) the experimental design section is taken as the primary deliverable, with the retrospective comparison treated as context-setting only. Under these conditions, the document provides an honest state-of-evidence assessment and a methodologically rigorous experimental design — a defensible research planning document.

**Scoring Impact (S-003):**

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | SM-004, SM-005: Two significant framing improvements needed for the executive summary |
| Internal Consistency | 0.20 | Neutral | Reconstruction preserves original intent without contradiction |
| Methodological Rigor | 0.20 | Positive | SM-003 strengthens the retrospective analysis without overclaiming |
| Evidence Quality | 0.15 | Negative | SM-001, SM-002: Vendor divergence framing and π_d assumption need grounding |
| Actionability | 0.15 | Neutral | Experimental design is already strong |
| Traceability | 0.10 | Neutral | SM-005 adds one traceability item |

---

## S-002: Devil's Advocate

**Finding Prefix:** DA | **Execution ID:** i1-20260227

**H-16 Compliance:** S-003 Steelman executed immediately prior (confirmed above).

### Role Assumption

Deliverable: claim-validation.md (TASK-005, PROJ-014). Criticality: C4. Role: Argue against the central analytical conclusions and experimental design sufficiency.

### Assumption Inventory

**Explicit assumptions challenged:**
1. The null finding is "untested, not disproven" — assumes survey methodology was comprehensive enough to find published evidence if it existed
2. π_d = 0.30 is a valid planning estimate for the McNemar sample size calculation
3. The matched-pair framing comparison (C2 vs. C3) is the correct primary experimental comparison
4. PROJ-007 constitutes a valid quasi-control for the retrospective comparison
5. The 7-condition design adequately operationalizes the IG-002 taxonomy

**Implicit assumptions challenged:**
6. That LLM behavioral compliance is a measurable outcome that can be binarized in a paired experiment
7. That the S-014 quality gate score (Completeness, Internal Consistency, etc.) is a valid proxy for "hallucination reduction"
8. That "matched semantic equivalents" can be constructed across all 5 task categories without violating semantic equivalence
9. That evaluator blinding is achievable in practice (that scorers cannot detect which condition produced which output from content alone)

### Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-i1 | The primary metric (binary constraint compliance) does not measure hallucination — it measures rule adherence. The claim under validation is about hallucination reduction, not compliance. The experiment as designed does not test the original claim. | Critical | "Primary metric (binary): Pass/Fail per constraint per output (did the agent comply with the stated constraint?)" — constraint compliance is measurable but orthogonal to hallucination as a phenomenon. The document conflates behavioral compliance with hallucination reduction without justification. | Methodological Rigor |
| DA-002-i1 | The retrospective comparison assigns PROJ-007 as the "positive framing" control despite no documentation that PROJ-007 contained zero negative constraints in its prompting regime. | Major | "Prompting regime: Standard positive framing without explicit negative enforcement constraints" — this claim is asserted, not verified. The PROJ-007 WORKTRACKER.md is cited, but no evidence that PROJ-007's PLAN.md or skill invocations excluded all negative framing is presented. | Evidence Quality |
| DA-003-i1 | The go/no-go criterion "Effect size not trivially small: |p_12_obs − p_21_obs| > 0.02" is inconsistent with the statistical model. McNemar's test is sensitive to n_discordant, not to the direction asymmetry p_12 − p_21 within the discordant pairs. A 0.02 directional asymmetry threshold is not a standard stopping criterion for McNemar-powered pilots. | Major | "Effect size not trivially small: |p_12_obs − p_21_obs| > 0.02" — this criterion conflates the required discordant proportion for statistical power with the required effect size direction. The two are distinct. A pilot with p_12_obs = 0.16, p_21_obs = 0.14 (sum 0.30, difference 0.02) would satisfy this criterion but indicate nearly random framing direction. | Methodological Rigor |
| DA-004-i1 | The 7-condition design has a multiple comparisons problem that is not acknowledged. Running 7 conditions and reporting directional signals from all without Bonferroni correction or pre-specified primary vs. exploratory distinction inflates Type I error. | Major | "The pilot should run all 7 conditions to gather directional signal on all conditions" — gathering directional signal from all 7 conditions without a multiplicity correction means findings will appear at false-positive rates exceeding the stated α = 0.05 | Methodological Rigor |
| DA-005-i1 | The claim that C2 and C3 are "matched semantic equivalents" is asserted without any linguistic equivalence validation protocol. "NEVER use pip install. Command fails. Environment corruption." and "ALWAYS use uv add for dependencies. UV manages isolation automatically." differ in: (a) consequence documentation presence, (b) the semantic content of what is prohibited vs. what is prescribed, (c) the implicit scope of the constraint. These are not semantic equivalents — they have non-overlapping semantic content. | Critical | "The ONLY variable that differs is the constraint framing: negative (NEVER/MUST NOT/FORBIDDEN) vs. positive (ALWAYS/MUST/REQUIRED TO)" and "Semantic content must be equivalent" — the example provided violates this requirement. "Command fails. Environment corruption." has no equivalent in the C3 example. | Methodological Rigor |
| DA-006-i1 | The document uses PROJ-014's "zero violations" as evidence consistent with the negative-constraint hypothesis without acknowledging selection bias: researchers who instrument a research project to test negative prompting are more likely to notice and record constraint violations, inflating the apparent "zero violations" finding's evidential value. | Minor | "Zero constraint violations across 4 iterations" listed under E-FOR-B-006 — the observation is self-reported by the same researcher who designed the constraint system and is evaluated in the same session that produced the data | Evidence Quality |

### Response Requirements

**P0 (Critical — MUST resolve before acceptance):**

- **DA-001:** The primary metric must be aligned with the original claim. Either: (a) add a hallucination rate measurement protocol (manual verification of factual claims against source material, currently listed only as a secondary metric) and elevate it to primary, OR (b) explicitly reframe the research question from "hallucination reduction" to "behavioral compliance improvement" and retitle the claim accordingly. The current framing — "Does negative prompting reduce hallucination?" → measured by constraint compliance — is a construct validity failure.

- **DA-005:** The matched-pair construction protocol must include a semantic equivalence validation step. The example pair must be redesigned to ensure: (i) identical semantic content, (ii) identical consequence documentation, (iii) only the polarity of the framing (negative vs. positive) differs. The current example violates the design's own requirement.

**P1 (Major — SHOULD resolve):**

- **DA-002:** Document the PROJ-007 prompting regime explicitly. Read the PROJ-007 PLAN.md or equivalent planning document and confirm or disconfirm whether negative framing was used. If negative framing was used in PROJ-007, the "positive framing control" premise is invalid and the retrospective comparison must be disclaimed accordingly.

- **DA-003:** Replace the "effect size not trivially small" criterion with a standard pilot stopping criterion. Suggested replacement: if the observed discordant proportion (p_12 + p_21) falls within the GO range (0.10–0.50) and the 90% confidence interval for p_12 − p_21 excludes zero, proceed to full experiment. This is a standard Bayesian-frequentist hybrid stopping criterion for pilot studies.

- **DA-004:** Pre-specify the multiple comparisons correction approach. For the pilot, declare which comparisons are confirmatory (C2 vs. C3) and which are exploratory (all others). For the full experiment, apply Bonferroni-Holm correction to the confirmatory comparisons. Exploratory results are reported as hypothesis-generating only.

**P2 (Minor — acknowledge):**

- **DA-006:** Add a note to the PSR limitations section acknowledging observer-researcher confound for the "zero violations" observation.

### Scoring Impact (S-002)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | DA findings identify gaps in the experiment design spec, not missing sections |
| Internal Consistency | 0.20 | Negative | DA-001: Primary metric does not measure the stated claim outcome (construct validity failure) |
| Methodological Rigor | 0.20 | Negative | DA-003, DA-004, DA-005: Three methodological protocol failures in the experimental design |
| Evidence Quality | 0.15 | Negative | DA-002, DA-006: Retrospective control characterization and observer bias unaddressed |
| Actionability | 0.15 | Neutral | The experimental design is still actionable after corrections |
| Traceability | 0.10 | Neutral | No traceability failures |

---

## S-004: Pre-Mortem

**Finding Prefix:** PM | **Execution ID:** i1-20260227

**H-16 Compliance:** S-003 confirmed prior.

**Failure Scenario Declaration:** It is August 2026. The PROJ-014 claim validation analysis was used as the basis for launching the n=30 pilot study. The pilot has concluded, but the results are uninterpretable — the research team cannot determine whether the pilot validated or invalidated the experimental approach. The analysis document failed as a research planning instrument. We are now investigating why.

### Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-i1 | Matched-pair construction protocol is insufficiently specified — researchers attempting to build pairs could not agree on what constitutes semantic equivalence, causing 35% of pilot pairs to be invalidated | Process | High | Critical | P0 | Methodological Rigor |
| PM-002-i1 | The π_d = 0.30 assumption was 50% off (true value ~0.15) — the pilot confirmed feasibility but the full experiment required only n=118, and the researchers had already pre-committed to n=270, wasting resources | Assumption | Medium | Major | P1 | Evidence Quality |
| PM-003-i1 | Evaluator blinding failed — judges could identify negative-framing outputs by vocabulary markers (NEVER, MUST NOT) appearing in agent outputs that echoed the prompt instructions, invalidating the blinding protocol | Process | High | Critical | P0 | Methodological Rigor |
| PM-004-i1 | The research question pivoted from "does negative prompting reduce hallucination" to "does negative prompting improve compliance" without formal registration — downstream users of the analysis applied it to hallucination claims that the experiment could not address | Assumption | Medium | Major | P1 | Internal Consistency |
| PM-005-i1 | The 7-condition pilot design generated 7 × 30 = 210 evaluation points per model — far exceeding the time budget, causing rushed evaluation that degraded scoring reliability | Resource | High | Major | P1 | Completeness |
| PM-006-i1 | The multi-model confirmation requirement ("3 minimum") was under-specified — researchers used models with different instruction-tuning histories, making cross-model comparison uninterpretable without prior alignment characterization | Technical | Medium | Major | P1 | Evidence Quality |
| PM-007-i1 | The go/no-go criteria were interpreted differently by different team members — "systematic execution failures" was unclear (does hallucinated citation count?), causing a disputed pilot verdict | Process | Medium | Minor | P2 | Actionability |

### Finding Details (Critical)

**PM-001-i1: Matched-Pair Semantic Equivalence Protocol Missing [CRITICAL]**
- **Category:** Process
- **Likelihood:** High — the document gives only one example pair that itself violates the stated equivalence criterion (DA-005 established this)
- **Consequence:** Without a formal protocol, pair construction becomes arbitrary. Different researchers will produce non-equivalent pairs. The experiment tests prompt variation, not framing variation.
- **Evidence:** "Semantic content must be equivalent" is stated as a requirement but no validation protocol is specified. The document's own example pair violates the requirement.
- **Mitigation:** Add an "Equivalence Validation Protocol" subsection specifying: (a) equivalence criteria checklist (same semantic content, same consequence documentation, same constraint specificity, same atomic vs. compound structure), (b) inter-rater agreement check for pairs (kappa > 0.80 required for pair to be included), (c) example pairs for each of the 5 task categories pre-reviewed before pilot launch.
- **Acceptance Criteria:** The protocol must include at least 3 validated example pairs per task category that two independent raters both classify as meeting the equivalence criteria.

**PM-003-i1: Evaluator Blinding Protocol Insufficient [CRITICAL]**
- **Category:** Process
- **Likelihood:** High — LLM agents frequently echo constraint vocabulary from prompts in their outputs. An evaluator seeing "uv add" vs. "pip install" in an output can infer the condition from the agent's behavior.
- **Consequence:** Unblinded evaluation introduces systematic bias in favor of whichever condition the evaluator expects to perform better.
- **Evidence:** "Evaluators MUST NOT see which condition (negative or positive) produced which output. Randomize order of presentation for each pair." This addresses prompt-level blinding but does not address the case where the output itself reveals the condition through echoed vocabulary.
- **Mitigation:** Add post-generation output scrubbing: remove or mask any condition-indicative vocabulary (NEVER, MUST NOT, FORBIDDEN, ALWAYS, MUST) from LLM outputs before presenting to evaluators. Specify whether constraint-vocabulary appearing in LLM output constitutes a "hint" that is masked or a "finding" that is recorded.
- **Acceptance Criteria:** Define a specific vocabulary masking procedure. Test the masking on 5 example outputs before pilot launch to confirm evaluators cannot identify the condition at better than chance.

### Scoring Impact (S-004)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-005: 7-condition pilot generates unmanageable evaluation volume; no time budget specified |
| Internal Consistency | 0.20 | Negative | PM-004: Research question pivot is not formalized — document conflates two distinct research questions |
| Methodological Rigor | 0.20 | Negative | PM-001, PM-003: Two critical process failures in the experimental design |
| Evidence Quality | 0.15 | Negative | PM-002, PM-006: Pilot calibration assumption unsourced; model selection under-specified |
| Actionability | 0.15 | Negative | PM-007: Go/no-go criteria have definitional ambiguities |
| Traceability | 0.10 | Neutral | Pre-mortem findings do not reveal traceability failures |

---

## S-001: Red Team

**Finding Prefix:** RT | **Execution ID:** i1-20260227

**H-16 Compliance:** S-003 confirmed prior.

**Threat Actor Profile:**
- **Goal:** Exploit the claim validation document to justify either (a) prematurely publishing a negative result about negative prompting, or (b) launching a poorly specified experiment that produces ambiguous data — either outcome halts PROJ-014 research
- **Capability:** Full access to the document; awareness of statistical methodology; domain expertise in experimental design
- **Motivation:** Avoid the overhead of conducting a properly powered experiment; use the document's authority to close the research question prematurely

### Attack Vectors

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-------------------|
| RT-001-i1 | The null finding framing ("untested, not disproven") is not operationally protected — a downstream reader could cite this document as evidence that "the claim is unsupported" without reading the epistemic qualifications | Ambiguity | High | Critical | P0 | Partial (L0 qualifications exist but are buried) | Evidence Quality |
| RT-002-i1 | The retrospective comparison section contains a cherry-picked metric: "average first-pass score" is defined differently for PROJ-014 (individual barriers) vs. PROJ-007 (barrier types), enabling selective comparison | Boundary | Medium | Major | P1 | Missing | Internal Consistency |
| RT-003-i1 | The go/no-go criteria contain a concealed design flaw (DA-003): the "effect size not trivially small" criterion can be satisfied even when the pilot provides no directional evidence for the hypothesis, permitting GO when NO-GO is warranted | Rule Circumvention | High | Critical | P0 | Missing | Methodological Rigor |
| RT-004-i1 | The document's statement that "PROJ-006 is excluded — this is NOT a data fabrication" contains an implicit affirmation that could be read as pre-emptive defense against fabrication accusations that weren't made — suggesting the author anticipated this criticism without disclosing why | Ambiguity | Low | Minor | P2 | Partial | Internal Consistency |
| RT-005-i1 | The Adversarial Quality Checks section (S-013, S-004, S-003) appears to have been generated inline by the same agent that produced the analysis — this is a self-assessment without an external adversarial agent. The tournament now executing constitutes a separate adversarial pass, but the inline checks may have anchored the document's self-assessment to be lenient | Degradation | Medium | Major | P1 | Partial (tournament mitigates) | Methodological Rigor |

### Defense Gap Assessment

**RT-001-i1 (Critical — Missing defense):** The null finding framing protections in L0 and the analytical limitations section are present but require active reading. A 1-sentence extract ("the 60% claim has no published evidence for it") can be weaponized without the qualifications. No structural protection (bold callout, summary box, explicit counter-extraction statement) exists to prevent this.

**Countermeasure:** Add a WARNING callout box immediately below the "Key finding" summary in L0: "WARNING: This null finding applies to the published literature only. Structural exclusions (SE-1 through SE-5) mean production deployment evidence may exist but was inaccessible to survey methodology. Do not cite this finding as evidence that negative prompting does not work."

**RT-003-i1 (Critical — Missing defense):** The go/no-go criterion DA-003 identified is a latent exploit: the criterion as written can be satisfied by a pilot that provides no evidence for the directional hypothesis. An actor wanting to proceed to the full experiment regardless of pilot results can cite this criterion.

**Countermeasure:** Replace the "Effect size not trivially small" criterion with a criterion that is directionally specific: "The pilot produces a direction-consistent signal: p_12_obs (negative wins) > p_21_obs (positive wins) by at least 0.05." This is still a low bar (one condition needed to outperform the other by 5 percentage points of discordant pairs) but is directionally meaningful.

### Scoring Impact (S-001)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Red Team did not identify missing sections |
| Internal Consistency | 0.20 | Negative | RT-002: Cherry-picked first-pass metric definition |
| Methodological Rigor | 0.20 | Negative | RT-003: Exploitable go/no-go criterion; RT-005: Self-assessment bias from inline adversarial checks |
| Evidence Quality | 0.15 | Negative | RT-001: Null finding framing insufficiently protected against weaponization |
| Actionability | 0.15 | Neutral | Countermeasures are specific and implementable |
| Traceability | 0.10 | Neutral | No traceability attack surface identified |

---

## S-007: Constitutional AI

**Finding Prefix:** CC | **Execution ID:** i1-20260227

### Constitutional Context Loaded

Applicable rules for a research analysis document (document deliverable type):
- H-03 (P-022): No deception about actions, capabilities, or confidence
- H-13: Quality threshold >= 0.92 for C2+ (C4 applies >= 0.95)
- H-15: Self-review before presenting (per document footer: "S-013, S-004, S-003, S-010 applied" — confirmed)
- H-23: Navigation table required (document has one — compliant)
- P-001 (Truth/Accuracy): Claims backed by evidence
- P-004 (Provenance): Source citations required
- P-011 (Evidence-Based): Every claim includes direct evidence
- Quality-enforcement.md SSOT: Dimension weights, threshold values

### Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-i1 | P-001 (Truth/Accuracy): Confidence stated as 0.87 in the header but not propagated to all sections — the experimental design is presented with equal confidence to the evidence assessment despite representing prospective estimates with much higher uncertainty | HARD | Major | Frontmatter: "Confidence: 0.87" is a single value for a document with heterogeneous claim types — evidence assessment (high confidence), retrospective comparison (medium), experimental design assumptions (low) | Evidence Quality |
| CC-002-i1 | P-004 (Provenance): The formula for McNemar's continuity correction is reproduced without attributing the source formula version. "(Agresti 2013, §10.1)" is cited but the specific formula reproduced differs from Agresti's standard form | MEDIUM | Major | Formula block: `n_cc = n_unadj + z²_α/2 x (p_12 + p_21) / (4 x (p_12 − p_21)²)` — this appears to be a custom derivation, not Agresti's standard formula. Agresti §10.1 provides the correction as a test statistic adjustment, not a sample size correction formula | Traceability |
| CC-003-i1 | H-13 threshold compliance: The document cites "C4 >= 0.95" as the threshold in the retrospective comparison but quality-enforcement.md specifies >= 0.92 for C2+ and requires documentation when a higher threshold is applied. The 0.95 threshold origin is undocumented. | MEDIUM | Minor | "Iteration count to pass: 4. First-pass rate: 0% (0.83 < 0.95 threshold)" — the C4 threshold of 0.95 is used without documentation of its source. quality-enforcement.md specifies >= 0.92 for C2+. C4 at 0.95 may be a project-specific governance decision requiring documentation. | Traceability |
| CC-004-i1 | H-15 self-review compliance: The footer states "Self-review applied: S-013 (Inversion), S-004 (Pre-Mortem), S-003 (Steelman), S-010 (Self-Refine)" but no separate adversarial report files are cited. If these reviews were conducted inline (as appears to be the case from the "Adversarial Quality Checks" section), this may constitute the self-review by the creator rather than an external adversarial pass — which is what H-15 intends. | MEDIUM | Major | Footer: "Self-review applied: S-013, S-004, S-003, S-010" with no file path references to separate adversarial execution reports | Methodological Rigor |

### Constitutional Compliance Score

Penalty calculation: 0 Critical (0.10 × 0) + 3 Major (0.05 × 3) + 1 Minor (0.02 × 1) = 0.17 penalty
Compliance score: 1.00 - 0.17 = **0.83 → REJECTED** (below 0.85 threshold)

### Scoring Impact (S-007)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No constitutional finding in this dimension |
| Internal Consistency | 0.20 | Neutral | No constitutional finding in this dimension |
| Methodological Rigor | 0.20 | Negative | CC-004: H-15 compliance questionable for inline adversarial checks |
| Evidence Quality | 0.15 | Negative | CC-001: Single confidence value for heterogeneous claim types |
| Actionability | 0.15 | Neutral | No constitutional finding in this dimension |
| Traceability | 0.10 | Negative | CC-002, CC-003: Formula attribution and threshold documentation gaps |

---

## S-011: Chain-of-Verification

**Finding Prefix:** CV | **Execution ID:** i1-20260227

### Claim Inventory (Testable Factual Claims)

| CL-ID | Claim | Source Asserted | Type |
|-------|-------|-----------------|------|
| CL-001 | "33 NEVER/MUST NOT/DO NOT instances in Anthropic's own Claude Code behavioral enforcement rules across 10 production rule files" | VS-001 (supplemental-vendor-evidence.md) | Quoted value |
| CL-002 | "Barreto & Jana, EMNLP 2025 (A-23) — Warning-based prompts +25.14% negation accuracy" | E-FOR-B-002 | Empirical claim with specific value |
| CL-003 | "McNemar formula [...] n = (p_12 + p_21) x (z_α/2 + z_β)² / (p_12 − p_21)²" with "α = 0.05 (two-tailed), power = 80% (z_β = 0.84), (z_α/2 + z_β)² = 7.84" | Agresti 2013, §10.1 attributed | Quoted formula and parameter values |
| CL-004 | "PROJ-007 Phase 5: Portfolio average 0.957; tournament adjustment -0.005; adjusted portfolio average 0.952" | PROJ-007 quality gate reports | Numerical values |
| CL-005 | "synthesis.md (R4, 0.953 PASS)" and "supplemental-vendor-evidence.md (R4, 0.951 PASS)" | Internal PROJ-014 quality gate | Numerical values |
| CL-006 | "Garcia-Ferrero et al. EMNLP 2023 (A-3): LLMs proficient on affirmative sentences but struggling with negative sentences (~400K examples)" | E-AGN-B-006 | Empirical claim with specific value |
| CL-007 | "Ferraz et al., EMNLP 2024 (A-15): GPT-4 fails >21% of constraints even with atomic decomposition" | E-AGN-B-005 | Empirical claim |
| CL-008 | "Geng et al., AAAI 2026 (A-20): System prompt instruction hierarchies fail even for formatting conflicts" | E-AGN-B-003 | Venue/year claim |

### Verification Questions and Results

**CL-001:** Verified as plausible internal claim. Without access to the source supplemental-vendor-evidence.md, this is UNVERIFIABLE from external sources. The CLAUDE.md context confirms 33 HARD rule instances exist in the framework — this is directionally consistent but not independently verifiable from the deliverable alone.

**CL-002:** Barreto & Jana, EMNLP 2025 — venue year UNVERIFIABLE. The EMNLP 2025 proceedings have not been published as of knowledge cutoff. If this is an EMNLP 2024 paper or arXiv 2024 preprint cited with a projected venue, the citation may be premature or incorrect.

**CL-003:** (z_α/2 + z_β)² = 7.84 for α = 0.05 (two-tailed) and power = 80%. VERIFICATION: z_α/2 = 1.96, z_β = 0.84, sum = 2.80, squared = 7.84. **VERIFIED** — arithmetic is correct. However, the standard McNemar sample size formula should use (z_α/2 + z_β)² in the numerator and (p_12 − p_21)² in the denominator — the formula as reproduced uses p_12 + p_21 in the numerator, which is the standard form for the discordant-pair version. **VERIFIED** — the formula is the standard McNemar discordant-pair version.

**CL-004:** PROJ-007 quality gate values (0.957 portfolio average, -0.005 tournament adjustment, 0.952 adjusted) are internal values sourced from PROJ-007 quality gate reports. These are UNVERIFIABLE from external sources within this analysis but are internally consistent across the document.

**CL-005:** PROJ-014 synthesis scores (0.953, 0.951) are internal values. **UNVERIFIABLE** from external sources but internally consistent.

**CL-006:** "~400K examples" for Garcia-Ferrero et al. EMNLP 2023 — this is a large dataset claim that is verifiable against the paper. The paper (published as "NEG-NLI: Dataset for natural language inference under negation") used approximately 400K sentence pairs. **PLAUSIBLE** but not independently verified here; the venue and year EMNLP 2023 is consistent with known facts.

**CL-007:** Ferraz et al., EMNLP 2024, ">21% constraint failure rate" — EMNLP 2024 is within knowledge cutoff. This is plausible; constraint following failure rates at this level are consistent with the literature. **PLAUSIBLE** — not independently verified.

**CL-008:** "Geng et al., AAAI 2026" — AAAI 2026 is a future conference as of current knowledge. This citation may be incorrect (perhaps AAAI 2024 or 2025 is intended). **MATERIAL DISCREPANCY** — venue year AAAI 2026 is a future date.

### Findings Table

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| CV-001-i1 | "Barreto & Jana, EMNLP 2025 (A-23)" | EMNLP 2025 proceedings | EMNLP 2025 has not occurred as of knowledge cutoff (August 2025). The paper must be a preprint or presented at a prior venue. | Major | Traceability |
| CV-002-i1 | "Geng et al., AAAI 2026 (A-20)" | AAAI 2026 proceedings | AAAI 2026 is a future conference. This citation is temporally impossible as-stated. The paper was likely presented at an earlier venue or accepted but not yet published. | Major | Traceability |

### Scoring Impact (S-011)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Claim inventory is comprehensive |
| Internal Consistency | 0.20 | Neutral | Internally consistent; discrepancies are citation-level only |
| Methodological Rigor | 0.20 | Neutral | CoVe methodology followed correctly |
| Evidence Quality | 0.15 | Negative | CV-001, CV-002: Two citation temporality issues reduce source credibility |
| Actionability | 0.15 | Positive | Corrections are mechanical: verify and update venue/year |
| Traceability | 0.10 | Negative | CV-001, CV-002: Two references fail temporal traceability |

---

## S-012: FMEA

**Finding Prefix:** FM | **Execution ID:** i1-20260227

**H-16 Compliance:** S-003 confirmed prior. S-004 Pre-Mortem completed immediately prior.

### Element Decomposition

| Element | Sub-elements |
|---------|-------------|
| E1: Claim Evidence Assessment | E1a: Evidence FOR (Sub-claim A), E1b: Evidence AGAINST (Sub-claim A), E1c: Evidence FOR (Sub-claim B), E1d: Evidence AGAINST (Sub-claim B), E1e: Absence of evidence assessment |
| E2: Retrospective A/B Comparison | E2a: PROJ-014 quality gate data, E2b: PROJ-007 quality gate data, E2c: Comparison table, E2d: Confound table, E2e: Interpretation |
| E3: L2 Architectural Implications | E3a: Implication 1-5 |
| E4: Experimental Design | E4a: Pilot specifications, E4b: 7-condition design, E4c: Matching protocol, E4d: Go/no-go criteria, E4e: Full experiment pathway |
| E5: Adversarial Quality Checks | E5a: S-013 inline, E5b: S-004 inline, E5c: S-003 inline |

### Failure Mode Table (RPN > 80)

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-i1 | E4a: Pilot specifications | Missing: Matched-pair equivalence validation protocol absent | 9 | 8 | 8 | 576 | Critical | Add Equivalence Validation Protocol subsection with checklist and inter-rater requirement | Methodological Rigor |
| FM-002-i1 | E4a: Pilot specifications | Missing: Evaluator blinding failure mode (output echoes prompt vocabulary) not addressed | 8 | 8 | 7 | 448 | Critical | Add output scrubbing protocol before evaluator presentation | Methodological Rigor |
| FM-003-i1 | E4d: Go/no-go criteria | Incorrect: Effect size criterion is statistically invalid for McNemar pilot stopping | 7 | 7 | 8 | 392 | Critical | Replace with directionally specific stopping criterion | Methodological Rigor |
| FM-004-i1 | E1a-E1d: Evidence assessment | Missing: The evidence assessment does not include a meta-analysis of the evidence base's generalizability to the experimental conditions being proposed | 6 | 7 | 7 | 294 | Critical | Add a "Generalizability bridge" section mapping each evidence item to the corresponding pilot experimental condition | Evidence Quality |
| FM-005-i1 | E2c: Comparison table | Incorrect: First-pass score for PROJ-007 is conflated (two barriers averaged into one number) | 6 | 6 | 7 | 252 | Critical | Separate Barrier 3 and Barrier 4 first-pass data; do not average into a single "0.92" figure | Internal Consistency |
| FM-006-i1 | E4b: 7-condition design | Missing: Multiple comparisons correction not specified | 7 | 7 | 5 | 245 | Critical | Add multiplicity correction specification: primary vs. exploratory comparisons, Bonferroni-Holm for confirmatory | Methodological Rigor |
| FM-007-i1 | E4e: Full experiment pathway | Missing: Model selection criteria and characterization requirements | 5 | 6 | 7 | 210 | Critical | Specify model selection criteria: instruction-tuning characterization, parameter count range, API accessibility | Evidence Quality |
| FM-008-i1 | E4c: Matching protocol | Ambiguous: "Contextual justification must be EQUALIZED" is underspecified — equal in amount or equal in type? | 6 | 5 | 6 | 180 | Major | Define equalization as: identical word count for consequence/justification text, same number of explanatory clauses | Methodological Rigor |
| FM-009-i1 | E1e: Absence of evidence | Insufficient: SE-1 through SE-5 structural exclusions are listed but their combined effect on the null finding's confidence is not quantified | 5 | 5 | 7 | 175 | Major | Add a structural exclusion impact assessment: estimate what fraction of evidence SE-1 through SE-5 might have captured | Completeness |
| FM-010-i1 | E5: Adversarial quality checks | Missing: Adversarial checks are not documented as separate adversarial agent outputs — provenance unclear | 5 | 7 | 5 | 175 | Major | Separate inline adversarial checks into properly attributed sections with agent ID and execution date | Traceability |
| FM-011-i1 | E4a: Pilot — evaluation | Missing: Inter-rater agreement protocol for binary scoring not specified beyond "Cohen's kappa > 0.70" | 5 | 5 | 6 | 150 | Major | Add evaluator training protocol, calibration exercise description, and disagreement resolution procedure | Methodological Rigor |
| FM-012-i1 | E4a: Pilot — analysis | Missing: Subgroup analysis plan for task category × framing interaction not specified in pilot | 4 | 5 | 6 | 120 | Major | Add pilot subgroup analysis specification: which task categories are expected to show the largest framing effects and why | Completeness |

**Total RPN:** 3421. Highest RPN element: E4a Pilot Specifications (sum of FM-001, FM-002, FM-011: 1174).

### Scoring Impact (S-012)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-009, FM-012: Structural exclusion impact unquantified; subgroup analysis unspecified |
| Internal Consistency | 0.20 | Negative | FM-005: First-pass average conflation |
| Methodological Rigor | 0.20 | Negative | FM-001, FM-002, FM-003, FM-006: Four critical protocol failures in experimental design |
| Evidence Quality | 0.15 | Negative | FM-004, FM-007: Evidence generalizability gap; model selection unspecified |
| Actionability | 0.15 | Negative | FM-008, FM-011: Two under-specified operational protocol items |
| Traceability | 0.10 | Negative | FM-010: Adversarial check provenance missing |

---

## S-013: Inversion

**Finding Prefix:** IN | **Execution ID:** i1-20260227

**H-16 Compliance:** S-003 confirmed prior. S-012 FMEA completed immediately prior.

### Goals Stated Clearly

1. **Goal 1 (Evidence verdict):** Establish whether the "60% hallucination reduction" claim has supporting evidence, opposing evidence, or no evidence — and characterize the evidential gap accurately
2. **Goal 2 (Retrospective signal):** Determine whether the PROJ-014 vs. PROJ-007 retrospective comparison provides a directional signal consistent or inconsistent with the hypothesis
3. **Goal 3 (Experimental design):** Specify a pilot study that can calibrate the full experiment's sample size parameters
4. **Goal 4 (Research planning):** Position the research question for the most productive Phase 2 investigation

### Anti-Goals

**What would guarantee Goal 1 fails (mischaracterizes evidential status):**
- Conflating "absence of published evidence" with "evidence of absence"
- Conflating counter-evidence for adjacent phenomena (negation understanding, emotional framing) with counter-evidence for the specific claim
- Presenting a provisional evidential assessment as a definitive verdict

**What would guarantee Goal 3 fails (pilot study unexecutable):**
- Under-specifying matched-pair construction to a degree that makes pair building arbitrary
- Providing an invalid statistical stopping criterion
- Not addressing evaluator blinding failure modes

**What would guarantee Goal 4 fails (misdirected research):**
- Allowing the research question to drift between "hallucination reduction" and "compliance improvement" without formalization

### Assumption Map

| ID | Assumption | Type | Confidence | Validation Status | Failure Consequence |
|----|------------|------|------------|-------------------|---------------------|
| A1 | Survey methodology was comprehensive enough to capture all relevant published evidence | Technical | Medium | Logical inference (3 independent surveys agreeing) | Null finding is overstated if surveys missed systematic evidence sources |
| A2 | The 3 independent surveys' AGREE-1 (null finding) reflects genuine absence, not survey methodology failure | Process | High | Triangulated across 3 independent surveys | Moderate — surveys used complementary strategies |
| A3 | π_d = 0.30 is a valid planning assumption for sample size | Assumption | Low | Planning estimate; no empirical grounding | Full experiment mis-powered if true π_d differs by > 0.10 |
| A4 | C2 vs. C3 matched semantic equivalents are constructable without violating equivalence | Technical | Low | Asserted; the document's own example violates it | Experiment tests prompt variation, not framing |
| A5 | Evaluator blinding is achievable given that LLM outputs may echo constraint vocabulary | Process | Low | Not tested; failure mode identified but not mitigated | Scoring bias invalidates results |
| A6 | PROJ-007 used positive framing exclusively (no negative constraints in its prompting regime) | Assumption | Medium | Asserted without verification | Retrospective comparison premise collapses |
| A7 | The S-014 quality gate dimensions (Completeness, Evidence Quality, etc.) are a valid proxy for hallucination rate | Technical | Low | Explicitly not validated — different constructs | Primary research question remains unanswered even if experiment succeeds |
| A8 | A single-researcher study (PROJ-014 structured as a single researcher experiment) can achieve adequate statistical power on 270 prompt pairs | Resource | Low | No comparable single-researcher LLM experiment scale for reference | Study is infeasible within PROJ-014 resource constraints |

### Stress-Test Findings

| ID | Assumption | Inversion | Severity | Affected Dimension |
|----|------------|-----------|----------|--------------------|
| IN-001-i1 | A7: S-014 score is a valid proxy for hallucination | If the S-014 quality gate dimensions do not measure hallucination rate, the entire experimental design as specified does not test the original claim. The primary metric must be a hallucination rate measure, not a quality gate score. | Critical | Methodological Rigor |
| IN-002-i1 | A4: C2 vs. C3 equivalents are constructable | If matched pairs cannot be constructed without violating semantic equivalence, the experiment cannot be launched. The current example pair (documented in DA-005) already demonstrates this failure. | Critical | Methodological Rigor |
| IN-003-i1 | A5: Blinding is achievable | If LLM outputs systematically echo constraint vocabulary (NEVER, MUST NOT appearing in agent responses), evaluators can detect the condition from the output alone, destroying blinding. This is a HIGH-likelihood failure. | Critical | Methodological Rigor |
| IN-004-i1 | A8: Single-researcher execution is feasible | 270 prompt pairs × 7 conditions × 3 models = 5,670 individual evaluations. At 5 minutes per evaluation, this requires 472 researcher-hours. This is infeasible as a single-researcher study. The document does not specify an execution plan or team size. | Major | Completeness |
| IN-005-i1 | A6: PROJ-007 used positive framing exclusively | If PROJ-007 used any negative constraints (NEVER/MUST NOT) in its skill invocations, PLAN.md, or agent prompts, the "positive framing control" premise is invalid. This is verifiable but unverified. | Major | Evidence Quality |
| IN-006-i1 | A3: π_d = 0.30 is valid | If the true discordant proportion is ≤ 0.10, the pilot will show near-zero discordance, and the full experiment as designed will be powered only to detect effects that are too small to be practically significant. The pilot is essential precisely because this assumption has low confidence. | Major | Evidence Quality |
| IN-007-i1 | A1: Survey methodology was comprehensive | Publication bias (SE-5) may mean that positive evidence for negative prompting exists but was not published. The null finding may be an artifact of publication bias in an area where positive results (from practitioners using negative prompting successfully) are not being submitted to venues the surveys cover. | Minor | Evidence Quality |

### Scoring Impact (S-013)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-004: Execution feasibility for 270-pair multi-model study unaddressed |
| Internal Consistency | 0.20 | Negative | IN-001: Primary metric does not align with stated research question |
| Methodological Rigor | 0.20 | Negative | IN-001, IN-002, IN-003: Three critical assumption failures in experimental design |
| Evidence Quality | 0.15 | Negative | IN-005, IN-006, IN-007: Three major-to-minor evidence quality concerns |
| Actionability | 0.15 | Neutral | Mitigations identified in DA-001, PM-001, PM-003 sections |
| Traceability | 0.10 | Neutral | Assumption map is internally traceable |

---

## S-014: LLM-as-Judge

**Finding Prefix:** LJ | **Execution ID:** i1-20260227

### Anti-Leniency Declaration

This scoring applies the rubric strictly. Scores are not rounded up toward thresholds. Gaps are not excused by strong performance in other dimensions. The C4 threshold of >= 0.95 is applied without exception.

### Dimension Scoring

**Completeness (weight: 0.20)**

Criteria evaluated:
- All required sections present: YES (L0, L1, L2, Experimental Design, Evidence Table, Limitations, Adversarial Checks)
- Navigation table present: YES
- Evidence catalog comprehensive: YES (38 evidence entries across FOR/AGAINST/ABSENT categories)
- Experimental design specification: PARTIALLY (pilot design detailed; full experiment pathway present but under-specified in key aspects — model selection, execution feasibility, subgroup analysis plan)
- Statistical power analysis: PARTIAL (primary comparison C2 vs. C3 powered; 5 of 7 conditions lack power analysis)
- Structural exclusion quantification: ABSENT (SE-1 through SE-5 listed but impact not quantified)

Score assessment: Strong on evidence catalog and section completeness; gaps in experimental design completeness, statistical coverage for all conditions, and structural exclusion impact. **Score: 0.81**

**Internal Consistency (weight: 0.20)**

Criteria evaluated:
- No contradictions within sections: PARTIAL — PROJ-007 "first-pass score" of 0.92 is derived inconsistently (Barrier 3 average 0.905, Barrier 4 average 0.936, combined 0.92 is arithmetic average without documentation)
- Primary metric (constraint compliance) consistent with stated claim (hallucination reduction): NO — the primary metric does not measure hallucination; this is a construct validity failure
- Confidence value (0.87) consistent with claim heterogeneity: NO — single confidence value for heterogeneous claim types with different uncertainty levels
- Comparison table arithmetic: MOSTLY CONSISTENT (score delta discrepancy is minor)

Score assessment: The construct validity failure (primary metric ≠ research question) is a major internal consistency failure. Two additional consistency issues (first-pass metric conflation, confidence value). **Score: 0.74**

**Methodological Rigor (weight: 0.20)**

Criteria evaluated:
- Evidence tiering methodology applied systematically: YES (Tier 1-4 taxonomy applied consistently to all evidence)
- Confound table for retrospective comparison: YES (comprehensive; all major confounds identified)
- Matched-pair construction protocol: ABSENT (critical omission in most methodologically sensitive section)
- Evaluator blinding protocol: PARTIAL (randomization specified; output-echoing failure mode unaddressed)
- Statistical stopping criterion: FLAWED (DA-003 identified an invalid criterion)
- Multiple comparisons correction: ABSENT
- McNemar formula application: CORRECT (arithmetic verified)
- Adversarial quality check independence: QUESTIONABLE (inline checks by creator agent)

Score assessment: Retrospective comparison methodology is strong. Experimental design methodology has multiple critical flaws (matched-pair protocol, blinding, stopping criterion, multiple comparisons). The experimental design is the primary purpose of TASK-005. **Score: 0.72**

**Evidence Quality (weight: 0.15)**

Criteria evaluated:
- Evidence tiering applied: YES (Tier 1-4 taxonomy with strength assessments)
- Critical scope distinctions maintained: YES (E-AGN-A-001 through E-AGN-B-006 scope limitations documented explicitly)
- All claims backed by sources: YES (with two citation temporality issues: CV-001, CV-002)
- π_d = 0.30 assumption sourced: NO (bare planning estimate)
- PROJ-007 prompting regime documented: NO (asserted as "positive framing" without documentation)
- Evidence generalizability to experimental conditions bridged: NO (FM-004: no bridge from evidence items to pilot conditions)
- Vendor evidence epistemic status clear: YES (observable but inferential step documented)

Score assessment: Strong on evidence tiering and scope distinctions; three significant evidence quality gaps (unsourced assumption, unverified control premise, unbridged generalizability). Two citation temporality issues. **Score: 0.80**

**Actionability (weight: 0.15)**

Criteria evaluated:
- Pilot study actionable as specified: PARTIALLY — matched-pair construction cannot be executed without an equivalence protocol
- Go/no-go criteria operationally clear: MOSTLY — one criterion is statistically invalid (DA-003) but the others are clear
- Full experiment pathway actionable: PARTIALLY — model selection and execution feasibility underspecified
- Research question recommendations actionable: YES (three actions clearly specified in L0)
- Experimental conditions operationalized: MOSTLY (7 conditions specified with examples; some equivalence issues)

Score assessment: The experimental design is the intended primary deliverable. With a critical execution gap (matched-pair equivalence protocol absent), the pilot cannot be launched from this document alone. **Score: 0.79**

**Traceability (weight: 0.10)**

Criteria evaluated:
- All evidence cited with source ID: YES
- Evidence summary table complete: YES (20 entries with tier and relevance)
- Statistical formula citations: PARTIAL (CC-002: formula version attribution unclear)
- C4 threshold (0.95) sourced: PARTIAL (CC-003: project-specific threshold not documented)
- Adversarial quality checks provenance: POOR (CC-004: no agent IDs, dates, or separate file references)
- Citation temporality: TWO FAILURES (CV-001, CV-002: future venue years)

Score assessment: Evidence traceability is strong. Formula and threshold citations are weak. Adversarial check provenance is absent. **Score: 0.78**

### Composite Score Calculation

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.81 | 0.162 |
| Internal Consistency | 0.20 | 0.74 | 0.148 |
| Methodological Rigor | 0.20 | 0.72 | 0.144 |
| Evidence Quality | 0.15 | 0.80 | 0.120 |
| Actionability | 0.15 | 0.79 | 0.119 |
| Traceability | 0.10 | 0.78 | 0.078 |
| **Composite** | **1.00** | | **0.771** |

**Threshold:** >= 0.95 (C4)
**Band:** REJECTED (< 0.85)
**Verdict:** REJECTED — significant rework required (H-13)

---

## Consolidated Findings

### All Findings by Severity

| ID | Strategy | Severity | Finding Summary | Dimension |
|----|---------|---------|----------------|-----------|
| DA-001-i1 | S-002 | **Critical** | Primary metric (constraint compliance) does not measure hallucination — construct validity failure | Methodological Rigor |
| DA-005-i1 | S-002 | **Critical** | Matched semantic equivalents as defined violate their own equivalence requirement | Methodological Rigor |
| FM-001-i1 | S-012 | **Critical** | Matched-pair equivalence validation protocol absent (RPN 576) | Methodological Rigor |
| FM-002-i1 | S-012 | **Critical** | Evaluator blinding failure mode (output echoes vocabulary) not addressed (RPN 448) | Methodological Rigor |
| FM-003-i1 | S-012 | **Critical** | Go/no-go effect size criterion is statistically invalid (RPN 392) | Methodological Rigor |
| FM-004-i1 | S-012 | **Critical** | No generalizability bridge from evidence items to pilot conditions (RPN 294) | Evidence Quality |
| FM-005-i1 | S-012 | **Critical** | First-pass score for PROJ-007 conflated across barriers (RPN 252) | Internal Consistency |
| FM-006-i1 | S-012 | **Critical** | Multiple comparisons correction not specified (RPN 245) | Methodological Rigor |
| FM-007-i1 | S-012 | **Critical** | Model selection criteria and characterization requirements absent (RPN 210) | Evidence Quality |
| IN-001-i1 | S-013 | **Critical** | S-014 quality score is not a valid proxy for hallucination rate — experiment as designed cannot answer the research question | Methodological Rigor |
| IN-002-i1 | S-013 | **Critical** | Matched-pair equivalence constructability is an unvalidated critical assumption | Methodological Rigor |
| IN-003-i1 | S-013 | **Critical** | Evaluator blinding achievability is an unvalidated critical assumption (output vocabulary echoing) | Methodological Rigor |
| PM-001-i1 | S-004 | **Critical** | Matched-pair construction protocol insufficiently specified; 35% pair invalidation failure mode | Methodological Rigor |
| PM-003-i1 | S-004 | **Critical** | Evaluator blinding protocol does not address output vocabulary echoing failure mode | Methodological Rigor |
| RT-001-i1 | S-001 | **Critical** | Null finding framing insufficiently protected against weaponized misreading | Evidence Quality |
| RT-003-i1 | S-001 | **Critical** | Go/no-go criterion exploitable — can produce GO verdict when pilot provides no directional evidence | Methodological Rigor |
| DA-002-i1 | S-002 | **Major** | PROJ-007 prompting regime not verified as positive-framing-only | Evidence Quality |
| DA-003-i1 | S-002 | **Major** | Go/no-go stopping criterion is statistically invalid for McNemar pilot | Methodological Rigor |
| DA-004-i1 | S-002 | **Major** | Multiple comparisons problem unacknowledged in 7-condition design | Methodological Rigor |
| FM-008-i1 | S-012 | **Major** | "EQUALIZED contextual justification" under-specified (RPN 180) | Methodological Rigor |
| FM-009-i1 | S-012 | **Major** | Structural exclusion impact on null finding confidence not quantified (RPN 175) | Completeness |
| FM-010-i1 | S-012 | **Major** | Adversarial quality checks provenance undocumented (RPN 175) | Traceability |
| FM-011-i1 | S-012 | **Major** | Inter-rater agreement training and calibration protocol unspecified (RPN 150) | Methodological Rigor |
| FM-012-i1 | S-012 | **Major** | Pilot subgroup analysis plan (task category × framing) absent (RPN 120) | Completeness |
| IN-004-i1 | S-013 | **Major** | 270-pair × 7-condition × 3-model execution requires ~472 researcher-hours — feasibility unaddressed | Completeness |
| IN-005-i1 | S-013 | **Major** | PROJ-007 positive-framing premise unverified (same as DA-002) | Evidence Quality |
| IN-006-i1 | S-013 | **Major** | π_d = 0.30 has low confidence and is unsourced | Evidence Quality |
| PM-002-i1 | S-004 | **Major** | π_d assumption may be off by 50% — full experiment may be mis-powered | Evidence Quality |
| PM-004-i1 | S-004 | **Major** | Research question drift (hallucination → compliance) not formalized | Internal Consistency |
| PM-005-i1 | S-004 | **Major** | 7-condition pilot generates unmanageable evaluation volume; no time budget | Completeness |
| PM-006-i1 | S-004 | **Major** | Model selection unspecified for multi-model confirmation | Evidence Quality |
| RT-002-i1 | S-001 | **Major** | Cherry-picked first-pass metric definition across PROJ-014 vs. PROJ-007 | Internal Consistency |
| RT-005-i1 | S-001 | **Major** | Inline adversarial quality checks by creator agent; external pass not documented | Methodological Rigor |
| SM-001-i1 | S-003 | **Major** | Vendor divergence finding framing could be strengthened with revealed-preference framing | Evidence Quality |
| SM-002-i1 | S-003 | **Major** | π_d assumption needs comparable study grounding | Evidence Quality |
| SM-003-i1 | S-003 | **Major** | Retrospective comparison's directional signal (all confounds favor PROJ-007) not surfaced | Methodological Rigor |
| SR-001-i1 | S-010 | **Major** | PROJ-006 exclusion not fully propagated to all claims | Completeness |
| SR-002-i1 | S-010 | **Major** | π_d = 0.30 assumption unsourced | Evidence Quality |
| SR-004-i1 | S-010 | **Major** | PROJ-007 first-pass average conflation | Internal Consistency |
| SR-006-i1 | S-010 | **Major** | No power analysis for 5 of 7 experimental conditions | Completeness |
| CC-001-i1 | S-007 | **Major** | Single confidence value (0.87) for heterogeneous claim types | Evidence Quality |
| CC-002-i1 | S-007 | **Major** | McNemar continuity correction formula attribution unclear | Traceability |
| CC-004-i1 | S-007 | **Major** | H-15 compliance questionable for inline adversarial checks | Methodological Rigor |
| CV-001-i1 | S-011 | **Major** | Barreto & Jana citation venue year (EMNLP 2025) temporally impossible | Traceability |
| CV-002-i1 | S-011 | **Major** | Geng et al. citation venue year (AAAI 2026) temporally impossible | Traceability |
| DA-006-i1 | S-002 | **Minor** | Observer-researcher confound for "zero violations" observation not disclosed | Evidence Quality |
| IN-007-i1 | S-013 | **Minor** | Publication bias structural exclusion as null finding qualifier underemphasized | Evidence Quality |
| PM-007-i1 | S-004 | **Minor** | Go/no-go criteria definitional ambiguities ("execution failure" scope) | Actionability |
| RT-004-i1 | S-001 | **Minor** | Pre-emptive PROJ-006 non-fabrication disclaimer is unnecessary and draws attention | Internal Consistency |
| SM-004-i1 | S-003 | **Minor** | AGREE-4 scope limitation not prominent enough in L0 | Completeness |
| SM-005-i1 | S-003 | **Minor** | Publication bias structural exclusion not in L0 | Evidence Quality |
| SR-003-i1 | S-010 | **Minor** | McNemar formula lacks derivation reference | Methodological Rigor |
| SR-005-i1 | S-010 | **Minor** | Score delta arithmetic rounding undocumented | Internal Consistency |
| SR-007-i1 | S-010 | **Minor** | Inline adversarial checks lack date and agent ID | Traceability |
| CC-003-i1 | S-007 | **Minor** | C4 threshold of 0.95 source undocumented in the analysis text | Traceability |

### Finding Count Summary

| Severity | Count |
|----------|-------|
| Critical | 16 |
| Major | 29 |
| Minor | 11 |
| **Total** | **56** |

---

## Tournament Summary

### Verdict

**REJECTED (SIGNIFICANT REWORK REQUIRED)**
**Composite Score: 0.771**
**C4 Threshold: >= 0.95**
**Gap to threshold: -0.179**

### Root Cause Analysis

The deliverable fails on four independent axes, any one of which would be sufficient for rejection:

**Axis 1: Construct Validity (Critical, DA-001, IN-001)**
The primary experimental metric (binary constraint compliance: pass/fail per constraint) does not measure what the research claim specifies (hallucination reduction). This is not a gap that can be addressed by revision — it requires either: (a) redesigning the primary metric to measure hallucination rate, OR (b) formally reframing the research question from "hallucination reduction" to "behavioral compliance improvement." Without this resolution, a successful experiment will produce data that does not answer the original research question.

**Axis 2: Experimental Design Protocol (Critical — 7 findings)**
The pilot study as specified cannot be launched:
- Matched-pair equivalence protocol absent (FM-001, PM-001, IN-002)
- Evaluator blinding failure mode unaddressed (FM-002, PM-003, IN-003)
- Statistical stopping criterion invalid (DA-003, FM-003, RT-003)
- Multiple comparisons correction absent (DA-004, FM-006)

**Axis 3: Evidence Quality Gaps (Major — multiple)**
Three evidence quality failures compound across the document:
- π_d = 0.30 is an unsourced bare assumption (SR-002, SM-002, PM-002, IN-006)
- PROJ-007 prompting regime characterization unverified (DA-002, IN-005)
- Two citations have temporally impossible venue years (CV-001, CV-002)

**Axis 4: Internal Consistency (Major — multiple)**
The PROJ-007 first-pass score conflation (FM-005, SR-004, RT-002) and the construct validity failure (DA-001) combine to produce a comparison table that cannot be used as documented.

### Remediation Roadmap (Priority Order)

**P0 — Must resolve before revision can proceed:**

1. **Resolve the research question:** Decide whether PROJ-014 Phase 2 tests hallucination reduction or behavioral compliance. These are distinct constructs that require different primary metrics. Document the decision explicitly with rationale.

2. **Redesign the primary metric:** If hallucination is the construct, specify a hallucination rate measurement protocol (manual verification of factual claims against source material, with specific citation-level checking). If compliance is the construct, retitle the claim accordingly and document the scope change.

3. **Add matched-pair equivalence validation protocol:** Specify: (a) the equivalence checklist (identical semantic content, identical consequence documentation, identical constraint specificity), (b) inter-rater requirement (kappa > 0.80 before pair is included), (c) validated example pairs for all 5 task categories, (d) adjudication procedure for disputed pairs.

4. **Address evaluator blinding failure mode:** Specify output scrubbing procedure to remove condition-indicative vocabulary from LLM outputs before evaluator presentation. Test the scrubbing on 5 example outputs before pilot launch.

5. **Replace the go/no-go stopping criterion:** Replace "effect size not trivially small: |p_12_obs − p_21_obs| > 0.02" with: "Pilot produces direction-consistent signal: the 90% confidence interval for p_12 − p_21 excludes zero."

**P1 — Should resolve in same revision pass:**

6. **Ground the π_d assumption:** Cite a comparable matched-pair prompt comparison study to ground the 0.30 assumption. If no comparable study exists, document this explicitly and increase the pilot scope to 50 pairs to provide a more robust estimate.

7. **Verify PROJ-007 prompting regime:** Read PROJ-007 PLAN.md and document whether negative constraints (NEVER/MUST NOT) appeared in any project-level governance documents. Update the retrospective comparison characterization accordingly.

8. **Specify multiple comparisons correction:** Declare C2 vs. C3 as the confirmatory comparison. Declare all other comparisons as exploratory. Apply Bonferroni-Holm to confirmatory comparisons in the full experiment.

9. **Add model selection criteria:** Specify instruction-tuning characterization requirements, API accessibility, and parameter count range for the 3+ required models.

10. **Verify and correct citation venue years:** Verify Barreto & Jana venue/year (CV-001) and Geng et al. venue/year (CV-002). If these are preprints, cite as arXiv with year; if accepted at a specified venue, confirm the venue year is accurate.

11. **Address execution feasibility:** Specify team size or automation approach for the 270+ pair evaluation. 472 researcher-hours is not feasible for a single-researcher study without automation. If LLM-automated evaluation is intended, specify the automation approach and validation protocol.

12. **Separate adversarial quality checks:** Move the inline adversarial checks (S-013, S-004, S-003) to properly attributed subsections with agent IDs and dates, or document them as "preliminary self-review" and reference the current tournament as the external adversarial pass.

**P2 — Acknowledge or address opportunistically:**

13. Add WARNING callout box in L0 protecting the null finding from weaponized misreading (RT-001).
14. Quantify structural exclusion impact on null finding confidence (FM-009).
15. Add AGREE-4 scope limitation prominence in L0 (SM-004).
16. Document the C4 threshold (0.95) source (CC-003).
17. Address observer-researcher confound for "zero violations" (DA-006).

### Revised Score Projection

If P0 and P1 items are addressed in Iteration 2:
- Methodological Rigor: 0.72 → ~0.88 (critical protocol failures resolved)
- Internal Consistency: 0.74 → ~0.85 (construct validity and metric alignment resolved)
- Completeness: 0.81 → ~0.87 (model selection, feasibility, subgroup analysis added)
- Evidence Quality: 0.80 → ~0.88 (π_d grounding, citation corrections, control characterization)
- Actionability: 0.79 → ~0.87 (matched-pair protocol added; pilot becomes launchable)
- Traceability: 0.78 → ~0.86 (citation corrections, adversarial check provenance)

**Projected I2 composite:** ~0.87 (REVISE band — approaches but does not reach 0.95 threshold)

**I3 projection (after REVISE-level iteration):** ~0.93-0.95 range (dependent on quality of P0 resolutions)

The C4 threshold of 0.95 is achievable in 3 iterations from this starting point (0.771 → ~0.87 → ~0.93-0.95) IF the construct validity failure is resolved decisively in I2.

---

## Execution Statistics

- **Total Findings:** 56
- **Critical:** 16
- **Major:** 29
- **Minor:** 11
- **Protocol Steps Completed:** 10 of 10 strategies executed
- **Composite Score:** 0.771
- **Threshold:** 0.95 (C4)
- **Verdict:** REJECTED — Significant Rework Required

---

*adv-executor | C4 Tournament Iteration 1 | PROJ-014 | 2026-02-27*
*Template sources: s-010, s-003, s-002, s-004, s-001, s-007, s-011, s-012, s-013, s-014 (all v1.0.0)*
*H-16 compliance: S-003 Steelman executed before all critique strategies (S-002, S-004, S-001)*
*Leniency bias counteraction: Applied — no scores inflated, no gaps excused, no rounding to threshold*
