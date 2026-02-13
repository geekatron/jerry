# TASK-006: Revised Catalog of 15 Adversarial Review Strategies (v1.1.0)

<!--
DOCUMENT-ID: FEAT-004:EN-301:TASK-006
AUTHOR: ps-researcher agent (creator revision)
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-301 (Deep Research: 15 Adversarial Strategies)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
PS-ID: EN-301
ENTRY-ID: TASK-006
REVISION-OF: TASK-004-unified-catalog.md (v1.0.0)
REVIEW-ADDRESSED: TASK-005-adversarial-review-iter1.md
-->

> **Version:** 1.1.0 (revised from 1.0.0)
> **Agent:** ps-researcher (creator revision)
> **Revision Basis:** TASK-005 adversarial review (quality score 0.89, target >= 0.92)
> **Revision Strategy:** Targeted improvements addressing all HIGH and MEDIUM priority findings; LOW priority findings addressed where feasible

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary of Changes](#l0-executive-summary-of-changes) | What changed and why |
| [Revision Response Table](#revision-response-table) | Finding-by-finding response with actions taken |
| [L1: Revised Strategy Sections](#l1-revised-strategy-sections) | Only sections with material changes |
| [L2: New and Revised Architecture Sections](#l2-new-and-revised-architecture-sections) | Systemic Risk, escalation thresholds, taxonomy notes |
| [Appendix A: Reserved Strategies](#appendix-a-reserved-strategies) | Promoted excluded candidates with reinstatement criteria |
| [Appendix B: Cognitive Bias Mapping](#appendix-b-cognitive-bias-mapping) | Per-strategy bias coverage |
| [Appendix C: Specification Deviation Record](#appendix-c-specification-deviation-record) | Formal documentation of Blue Team / Strawman deviation |
| [References](#references) | New or corrected citations |

---

## L0: Executive Summary of Changes

This document revises the TASK-004 unified catalog (v1.0.0) in response to the TASK-005 adversarial review, which scored the catalog at 0.89 against a 0.92 threshold. The revision addresses all 4 HIGH-priority and all 6 MEDIUM-priority findings, plus 2 of 2 LOW-priority findings.

**Key changes made:**

1. **Specification deviation formally documented** (RT-001): The replacement of Blue Team and Strawman with Pre-Mortem and Dialectical Inquiry is now documented as a formal deviation record (Appendix C) with explicit rationale, risk acceptance, and conditions under which the deviation should be revisited. This addresses P-020 (User Authority) by making the override transparent and reversible.

2. **Uncertainty markers added to all unverified empirical claims** (RT-002): All specific numerical claims sourced from training data are now marked with `[unverified from training data]`. Three claims are specifically hedged: the "30% increase" for Pre-Mortem, the "5-40% improvement" for Self-Refine, and the "~80% agreement" for LLM-as-Judge.

3. **Systemic Risk: Shared Model Bias section added to L2** (DA-002): New architectural section addresses the common-mode failure risk of LLM self-critique and prescribes mitigation strategies.

4. **Contraindications / "When NOT to Use" field added** to all 15 strategies (RT-003), with explicit escalation thresholds defined in L2.

5. **S-015 validation plan and fallback documented** (RT-004): Explicit validation experiments and a defined fallback strategy (default to Layer 2 minimum) added.

6. **Strategy differentiation strengthened** (REC-005): S-003/S-010 and S-002/S-008 differentiation clarified with mechanism-level distinctions; S-014 status as evaluation mechanism explicitly acknowledged.

7. **"Exactly 15" constraint rationale documented** (DA-001): Rationale traced to task specification; Reserved Strategies appendix created with promotion criteria.

8. **Industry/Engineering underrepresentation justified** (DA-004): Explicit rationale added for why theoretical generality was prioritized; compensating L2 guidance strengthened.

9. **Citation standardization** (REC-007): arXiv version numbers added where determinable; Dreyfus & Dreyfus identifier formalized; JSTOR/DOI distinction clarified for Mitroff & Emshoff; Selye ISBN noted as unavailable.

10. **Taxonomy acknowledged as approximate** (DA-003, REC-009): Secondary family classifications added; interchangeability warning added.

11. **Cognitive bias mapping** added (REC-010): Appendix B maps each strategy to the specific cognitive biases it counters.

**Unchanged from v1.0.0** (preserved strengths per TASK-005 Steelman acknowledgment):
- Overlap analysis section (exceptionally thorough)
- Selection rationale framework (clear, defensible)
- Redundancy check table (mechanism x agent pattern x output type)
- L2 composition model (Layer 0-4)
- Jerry Applicability section structure
- Research Limitations section (intellectual honesty)

**Reading guidance:** This document is a **revision delta**. For the full catalog text, refer to `TASK-004-unified-catalog.md` (v1.0.0). This document contains: (a) all changed sections in full, (b) new sections not present in v1.0.0, and (c) references to unchanged sections in the original. When the two documents conflict, this revision (v1.1.0) takes precedence.

---

## Revision Response Table

| Finding ID | Severity | Summary | Action Taken | Section |
|------------|----------|---------|--------------|---------|
| **RT-001** | HIGH | Blue Team/Strawman specification override | Formal deviation record created (Appendix C). Override made transparent with rationale, risk acceptance, and revisitation conditions. Documented as requiring user awareness per P-020. | [Appendix C](#appendix-c-specification-deviation-record) |
| **RT-002** | HIGH | Unverified empirical claims | All 3 specific numerical claims marked `[unverified from training data]`. Citation confidence for claims with specific numbers downgraded from HIGH to MEDIUM. | [L1: S-004](#s-004-pre-mortem-analysis-revised), [S-010](#s-010-self-refine-revised), [S-014](#s-014-llm-as-judge-revised), [Research Limitations](#revised-research-limitations-and-confidence-assessment) |
| **RT-003** | MEDIUM | No contraindications / "When NOT to Use" | "Contraindications" field added to all 15 strategies. Escalation thresholds defined in L2. | [L1: All strategies](#l1-revised-strategy-sections), [L2: Escalation Thresholds](#escalation-threshold-definitions) |
| **RT-004** | MEDIUM | S-015 no empirical validation but meta-strategy status | Validation plan with 3 experiments added. Fallback strategy defined: default to Layer 2 minimum if S-015 gates prove unreliable. | [S-015 Revised](#s-015-progressive-adversarial-escalation-revised) |
| **DA-001** | MEDIUM | "Exactly 15" constraint is arbitrary | Rationale documented: constraint originates from EN-301 task specification as a scope-bounding decision. Reserved Strategies appendix created with 5 candidates and promotion criteria. | [Selection Rationale Addendum](#selection-rationale-addendum), [Appendix A](#appendix-a-reserved-strategies) |
| **DA-002** | HIGH | LLM self-critique effectiveness assumed | "Systemic Risk: Shared Model Bias" section added to L2. External validation requirement added for self-critique strategies. Multi-Agent Debate independence limitation explicitly characterized. | [L2: Systemic Risk](#systemic-risk-shared-model-bias) |
| **DA-003** | LOW | Mechanistic family taxonomy is approximate | Taxonomy table updated with secondary classifications. Interchangeability warning added. | [Revised Mechanistic Families](#revised-mechanistic-families) |
| **DA-004** | MEDIUM | Industry/Engineering underrepresented | Explicit justification added: Jerry's adversarial strategies operate at the reasoning/argumentation level; industry patterns like Fagan Inspection are process-management patterns incorporated into L2 implementation guidance. L2 industry practices section strengthened. | [Selection Rationale Addendum](#selection-rationale-addendum), [L2: Industry Practice Integration](#industry-practice-integration-strengthened) |
| **REC-005** | MEDIUM | S-003/S-010 and S-002/S-008 differentiation thin | Differentiation strengthened with mechanism-level analysis. S-014 acknowledged as evaluation mechanism with justification for inclusion as strategy. | [Differentiation Clarifications](#differentiation-clarifications) |
| **REC-007** | MEDIUM | Citation standardization needed | arXiv version numbers added; Dreyfus identifier formalized; JSTOR/DOI distinction noted; Selye ISBN gap acknowledged. | [References](#references) |
| **REC-010** | LOW | No cognitive bias mapping | Appendix B added: maps each strategy to specific biases it counters. | [Appendix B](#appendix-b-cognitive-bias-mapping) |

---

## L1: Revised Strategy Sections

> **Note:** Only materially changed fields are shown. For unchanged content (full descriptions, mechanisms, strengths, use contexts, Jerry Applicability), refer to TASK-004-unified-catalog.md v1.0.0.

### Contraindications Added to All 15 Strategies

The following "Contraindications (When NOT to Use)" field is added to each strategy entry. This addresses RT-003.

| ID | Strategy | Contraindications |
|----|----------|-------------------|
| S-001 | Red Team Analysis | Do not use for early-stage drafts or exploratory work (premature adversarial pressure destroys nascent ideas). Do not use when the threat model is undefined or the "adversary" cannot be meaningfully characterized. Avoid when time constraint is under 1 hour. |
| S-002 | Devil's Advocate Analysis | Do not use when the position under review is still being formulated (DA requires a stable thesis to challenge). Avoid when the creator has explicitly requested constructive-only feedback (e.g., brainstorming phase). Do not use as sole review method for technical accuracy -- DA challenges reasoning, not facts. |
| S-003 | Steelman Technique | Do not use as a standalone strategy -- it is always a precursor to critique, never a substitute. Do not use when the argument is fundamentally incoherent (steelmanning a non-argument wastes effort). Avoid when time does not permit the two-phase approach. |
| S-004 | Pre-Mortem Analysis | Do not use for artifacts that are already complete and deployed (use retrospective M&M pattern instead). Do not use when the primary risk is factual inaccuracy rather than plan failure (use S-011 CoVe instead). Avoid for routine, low-stakes deliverables. |
| S-005 | Dialectical Inquiry | Do not use when there is only one viable approach (DI requires genuine alternatives). Do not use for time-constrained reviews (DI requires 3 agent passes minimum). Avoid when the decision is reversible and low-cost -- DI's overhead is only justified for consequential decisions. |
| S-006 | Analysis of Competing Hypotheses | Do not use when there is only one plausible hypothesis (the matrix degenerates). Do not use for normative/design questions where "hypotheses" are subjective preferences. Avoid when evidence is entirely absent -- ACH requires evidence to evaluate against. |
| S-007 | Constitutional AI Critique | Do not use when no explicit constitution/standards exist for the domain (the strategy requires written, evaluable principles). Do not use for creative or exploratory work where rigid principle adherence would be counterproductive. Avoid when principles are ambiguous or contradictory (resolve principle conflicts first). |
| S-008 | Socratic Method | Do not use when factual verification is the primary need (Socratic questioning probes reasoning, not facts -- use S-011 for facts). Do not use on artifacts with no reasoning component (e.g., raw data, configuration files). Avoid when the creator is unable to respond interactively (Socratic method requires dialogue). |
| S-009 | Multi-Agent Debate | Do not use for routine reviews (cost is disproportionate). Do not use when all debater agents are identical model instances and the question requires genuine domain diversity rather than sampling variance (see Systemic Risk section). Do not use when debate resolution criteria are undefined. |
| S-010 | Self-Refine | Do not use as the sole review strategy for high-stakes artifacts -- self-refine shares the model's blind spots. Do not use when the artifact requires domain expertise the model lacks (self-critique cannot surface unknown unknowns). Do not apply more than 3 iterations (empirical diminishing returns; risk of quality degradation). |
| S-011 | Chain-of-Verification | Do not use for normative, design, or reasoning quality assessments -- CoVe targets factual claims only. Do not use when the content contains no verifiable factual assertions. Avoid when external verification tools are unavailable and model knowledge is insufficient for the domain. |
| S-012 | FMEA | Do not use for abstract/conceptual work (FMEA requires decomposable components or process steps). Do not use when the system boundary is undefined. Avoid for exploratory or early-stage work where the component list is unstable. |
| S-013 | Inversion Technique | Do not use as the sole review method -- inversion generates checklists, not evaluations. Do not use for work where "failure" is ambiguous or subjective (creative writing, exploratory research). Avoid when anti-patterns are well-established and already codified (use existing checklists instead). |
| S-014 | LLM-as-Judge | Do not use without a defined rubric -- unstructured "rate this" requests produce unreliable scores. Do not use for pairwise comparison when both candidates are poor (the "better of two bad options" problem). Avoid when evaluation requires real-world testing, execution, or empirical measurement rather than textual assessment. |
| S-015 | Progressive Adversarial Escalation | Do not use when time constraints require immediate high-intensity review (skip to appropriate level). Do not use for time-critical security incidents (apply Level 4 directly). Do not use when the review context is well-characterized and the appropriate intensity is already known (use the specific strategy directly). |

---

### S-004: Pre-Mortem Analysis (Revised)

**Changes:** Uncertainty marker added to the "30% increase" claim per RT-002.

The following sentence in the Description is revised:

**Original (v1.0.0):**
> The temporal reframing -- moving from "could fail" to "has failed" -- dramatically increases the number and specificity of identified risks (Mitchell et al., 1989, documented a 30% increase).

**Revised (v1.1.0):**
> The temporal reframing -- moving from "could fail" to "has failed" -- dramatically increases the number and specificity of identified risks. Mitchell et al. (1989) studied the "temporal perspective" effect on event generation; the often-cited figure of approximately 30% more identified causes is an extrapolation from their experimental findings on prospective hindsight [unverified from training data -- the original paper examines temporal perspective broadly; the specific 30% figure may reflect a secondary interpretation rather than a direct experimental result].

**Revised Strength (line 4):**

**Original:**
> 30% increase in identified failure causes vs. prospective foresight (Mitchell et al., 1989)

**Revised:**
> Significant increase in identified failure causes vs. prospective foresight, attributed to prospective hindsight effect (Mitchell et al., 1989) [unverified: the specific "30%" figure requires independent verification against the original paper]

---

### S-010: Self-Refine (Revised)

**Changes:** Uncertainty marker added to the "5-40% improvement" claim per RT-002.

**Original (v1.0.0):**
> Empirically demonstrated 5-40% improvement across 7 diverse tasks (Madaan et al., 2023).

**Revised (v1.1.0):**
> Madaan et al. (2023) report improvements across multiple tasks including math reasoning, code generation, and dialogue response quality. The range of improvement varies substantially by task and metric [unverified from training data: the specific "5-40%" range is recalled from training data and may not precisely reflect the paper's reported figures; the original paper should be consulted for exact benchmark results and the specific metrics used].

**Revised Strength (line 3):**

**Original:**
> Demonstrated empirical improvement (5-40%) across multiple benchmarks

**Revised:**
> Demonstrated empirical improvement across multiple benchmarks (Madaan et al., 2023), with magnitude varying by task type [unverified: specific percentage range requires verification against original paper]

---

### S-014: LLM-as-Judge (Revised)

**Changes:** (1) Uncertainty marker added to the "~80% agreement" claim per RT-002. (2) Status as evaluation mechanism explicitly acknowledged per REC-005.

**Original (v1.0.0):**
> ~80% agreement with human preferences demonstrated (Zheng et al., 2023).

**Revised (v1.1.0):**
> Zheng et al. (2023) report strong agreement between LLM judge evaluations and human preferences on MT-Bench and Chatbot Arena benchmarks [unverified from training data: the specific "~80%" figure is recalled from training data; the exact agreement rate, the specific benchmarks, and the conditions under which this rate holds should be verified against the original paper]. Agreement rates may vary by model capability, rubric specificity, and evaluation domain.

**Added field -- Mechanism vs. Strategy Classification:**
> **Note on Classification:** S-014 functions as both an evaluation *mechanism* (providing scoring infrastructure that other strategies use) and an adversarial *strategy* (the structured rubric-based evaluation itself constitutes an adversarial challenge to the artifact's quality claims). It is included as a strategy because: (a) the rubric-based evaluation is substantively different from informal quality assessment, (b) it produces adversarial outputs (scores with justifications that challenge the artifact), and (c) excluding it would leave the catalog without a standardized evaluation strategy, making quality gates like Jerry's 0.92 threshold inoperable. However, downstream consumers should note that S-014 also serves as scoring infrastructure for S-015's escalation gates.

---

### S-015: Progressive Adversarial Escalation (Revised)

**Changes:** (1) Validation plan added per RT-004. (2) Fallback strategy defined. (3) Confidence assessment updated.

**Added field -- Validation Plan:**

> **Validation Experiments (Required before production deployment):**
>
> **Experiment 1: False Negative Detection Rate**
> - Inject known defects at varying severity levels into test artifacts
> - Process through S-015 escalation pipeline
> - Measure: What percentage of defects are caught at each escalation level?
> - Success criterion: >= 95% of HIGH-severity defects caught by Level 3; >= 80% of MEDIUM-severity defects caught by Level 2
>
> **Experiment 2: Escalation Calibration**
> - Present a corpus of artifacts with pre-determined appropriate review intensity (established by human expert judgment)
> - Measure: Does S-015 escalate to the correct level in >= 85% of cases?
> - Success criterion: No more than 5% of artifacts under-reviewed (classified lower than expert judgment)
>
> **Experiment 3: Cost-Efficiency Comparison**
> - Compare S-015 graduated escalation against a baseline of always applying Level 3 review
> - Measure: (a) Total agent passes consumed, (b) defect detection rate, (c) false positive rate
> - Success criterion: S-015 achieves >= 90% of baseline detection rate at <= 60% of baseline cost

**Added field -- Fallback Strategy:**

> **Fallback if Validation Fails:** If S-015 escalation gates produce unacceptable false negative rates (> 10% of HIGH-severity defects missed), the fallback is:
> - Disable graduated escalation
> - Apply Layer 2 (Standard Critic Review: S-007 + S-002 + S-014) as the minimum for all artifacts
> - Reserve Layer 3-4 for artifacts flagged by human judgment or explicit orchestration configuration
> - This fallback trades cost efficiency for safety, which is acceptable until S-015 is validated

**Revised Confidence:**

**Original:**
> Confidence: S-015 -- MEDIUM -- Novel composite strategy synthesized from established sources; no direct empirical validation as a unified method.

**Revised:**
> Confidence: S-015 -- MEDIUM -- Novel composite strategy synthesized from established sources; no direct empirical validation as a unified method. Meta-strategy status is provisional pending completion of validation experiments. Fallback to Layer 2 minimum is defined. The component strategies (S-010, S-003, S-008, S-002, S-007, S-001, S-009) are individually well-validated; the novel contribution is their graduated composition, which requires separate validation.

---

### Differentiation Clarifications

This section addresses REC-005 by strengthening the differentiation between pairs flagged as insufficiently distinct.

#### S-003 (Steelman) vs. S-010 (Self-Refine)

**Critic's concern:** Both involve "single agent improves its own output" -- the distinction is role assignment, not mechanism.

**Response:** The distinction is mechanistic, not merely role-based:

| Dimension | S-003 Steelman | S-010 Self-Refine |
|-----------|---------------|-------------------|
| **Who performs it** | The *critic* (external agent reviewing creator's work) | The *creator* (same agent that produced the work) |
| **Direction of improvement** | Strengthens the *argument being reviewed* before critiquing it | Improves the *agent's own output* through self-feedback |
| **Purpose** | Ensures fair evaluation (precondition for critique) | Improves output quality (substitute for external review) |
| **Output** | A steelmanned version + subsequent genuine critique | An iteratively improved version of the original output |
| **Cognitive analog** | Intellectual charity / principle of charity | Self-editing / self-revision |
| **When applied** | Before a separate critique phase (always paired) | As a standalone improvement loop (may be the only review) |
| **Information flow** | Critic reads creator's work, reconstructs it stronger, then evaluates | Same agent re-reads own output, generates feedback, revises |

The core mechanistic distinction is that Steelman operates on *another agent's* output to ensure fair evaluation, while Self-Refine operates on the *agent's own* output to improve it. This is not merely a role assignment -- it produces fundamentally different cognitive processes (charitable interpretation vs. self-criticism) and outputs (strengthened-argument-plus-critique vs. iteratively-refined-output).

#### S-002 (Devil's Advocate) vs. S-008 (Socratic Method)

**Critic's concern:** Both deliver adversarial challenge through verbal/textual confrontation; the distinction (assertions vs. questions) is thin.

**Response:** The distinction is operationally significant:

| Dimension | S-002 Devil's Advocate | S-008 Socratic Method |
|-----------|----------------------|----------------------|
| **Adversarial modality** | *Assertions* -- constructs counterarguments | *Questions* -- poses probing inquiries |
| **Creator's required response** | Defend against or concede to counterarguments | Discover and articulate answers, exposing own gaps |
| **Discovery mechanism** | External: the advocate finds flaws and presents them | Internal: the creator discovers flaws through self-examination prompted by questions |
| **Output** | A countercase document (the advocate's argument) | A Q&A transcript exposing contradictions |
| **Cognitive transfer** | Creator learns what the advocate found wrong | Creator learns *why* their reasoning was flawed (deeper understanding) |
| **Scope** | Focused: challenges the prevailing conclusion | Open-ended: explores all aspects of reasoning via six question categories |
| **Prerequisite** | Requires a stable conclusion to challenge | Can be applied to reasoning-in-progress |

The operational consequence is that Devil's Advocate tells the creator *what is wrong*, while Socratic Method forces the creator to *discover what is wrong themselves*. These produce different cognitive outcomes in the review process and are not interchangeable. DA is more efficient (one-pass countercase); Socratic is more thorough (multi-turn exploration that may surface issues the advocate would not have identified).

#### S-014 (LLM-as-Judge) -- Classification Note

See the added "Mechanism vs. Strategy Classification" field in the S-014 revised section above. S-014's dual nature (mechanism + strategy) is now explicitly acknowledged. Its inclusion is justified because excluding it would leave the catalog without a standardized quantitative evaluation strategy.

---

### Selection Rationale Addendum

This addendum addresses DA-001 (the "exactly 15" constraint) and DA-004 (industry underrepresentation).

#### Why Exactly 15 Strategies (DA-001)

The "exactly 15" constraint originates from the EN-301 enabler specification, which states: *"Research and catalog 15 adversarial review strategies from authoritative sources"* (EN-301, Summary). The number 15 was set as a scope-bounding decision balancing three considerations:

1. **Coverage adequacy**: 15 strategies spanning 4 mechanistic families provide sufficient coverage of the adversarial strategy space without redundancy (verified by the redundancy check table).
2. **Cognitive tractability**: A catalog of 15 is small enough for an LLM agent to hold the full selection table in context when choosing strategies, while large enough to cover distinct review contexts.
3. **Implementation scope**: Each strategy requires integration into Jerry's skill architecture (agent configuration, prompt templates, orchestration support). 15 represents a feasible initial implementation scope.

The constraint is a pragmatic scope boundary, not an assertion that exactly 15 is the theoretically optimal number. The Reserved Strategies appendix (Appendix A) provides a path for catalog expansion when warranted.

#### Why Industry/Engineering Has One Representative (DA-004)

The critic correctly observes that Industry/Engineering has only one representative (S-012 FMEA) despite Jerry being an engineering tool. The rationale:

1. **Level of abstraction**: The catalog operates at the *adversarial reasoning mechanism* level. Industry patterns like Fagan Inspection, ATAM, and Google Code Review are *process management patterns* that define how reviews are organized (roles, phases, entry/exit criteria), not how adversarial challenge is delivered. Their contributions are incorporated into L2 implementation guidance rather than occupying strategy slots.

2. **Subsumption**: ATAM's scenario-based probing is mechanistically covered by Socratic Method (S-008) and Red Team (S-001). Fagan Inspection's moderator role is covered by LLM-as-Judge (S-014). Google Code Review's lightweight continuous model is an implementation pattern for any strategy.

3. **Compensation**: The L2 architecture section explicitly incorporates excluded industry practices as implementation guidance. See the strengthened [Industry Practice Integration](#industry-practice-integration-strengthened) section below.

This distribution reflects a conscious design choice: strategies define *what adversarial challenge to apply*; industry practices define *how to organize the review process*. Both are necessary; they occupy different architectural layers.

---

### Revised Mechanistic Families

This revision addresses DA-003 (taxonomy is approximate) and REC-009 (secondary classifications).

| Family | Primary Mechanism | Primary Members | Secondary Members | Note |
|--------|-------------------|-----------------|-------------------|------|
| **Role-Based Adversarialism** | A designated agent adopts an oppositional persona | S-001, S-002 | S-004 (temporal reframing is primary; narrator role is secondary) | |
| **Structured Decomposition** | A systematic framework forces exhaustive enumeration | S-006, S-011, S-012 | S-013 (inversion is primary mechanism; decomposition into anti-patterns is secondary) | |
| **Dialectical Synthesis** | Opposing positions are constructed and reconciled | S-005, S-009 | S-003 (charitable reconstruction is primary; dialectical engagement is secondary), S-008 (question-answer dialectic is secondary) | |
| **Iterative Self-Correction** | Agent critiques and revises its own output | S-007, S-010 | S-014 (rubric evaluation is primary; iterative scoring refinement is secondary), S-015 (escalation orchestration is primary; iterative intensification is secondary) | |

**Taxonomy Warning:** This classification is approximate. Individual strategies may straddle family boundaries, as indicated by the secondary classifications. Co-family membership does **not** imply interchangeability -- strategies within the same family may have very different operational characteristics, cost profiles, and applicability contexts. The taxonomy serves organizational purposes and should not be used as the sole basis for strategy substitution.

---

### Revised Research Limitations and Confidence Assessment

This revision addresses RT-002 by adding explicit uncertainty markers and downgrading confidence for specific numerical claims.

| Dimension | Assessment |
|-----------|------------|
| **Source Access** | WebSearch and WebFetch were unavailable for all three source research sessions. All content sourced from agent training knowledge (literature through May 2025). |
| **Citation Reliability** | ISBNs and DOIs are from well-known publications and are expected to be accurate. All citations trace to the three source artifacts (TASK-001, TASK-002, TASK-003). No fabricated citations were introduced during synthesis. **However, specific numerical claims drawn from papers cannot be independently verified without web access and must be treated as approximate.** |
| **Unverified Empirical Claims** | The following specific claims are marked `[unverified from training data]` and should be independently verified before being cited as authoritative: (1) "~30% increase in identified failure causes" attributed to Mitchell et al. (1989) in S-004; (2) "5-40% improvement" attributed to Madaan et al. (2023) in S-010; (3) "~80% agreement with human preferences" attributed to Zheng et al. (2023) in S-014. These claims are plausible and consistent with the cited papers' general findings but the specific numbers may be extrapolations, secondary interpretations, or imprecise recollections. |
| **Coverage** | 36 candidate strategies reduced to 15. The selection spans 4 categories (Academic, LLM-Specific, Industry, Emerging) and 4 mechanistic families. |
| **Confidence: S-001 through S-006** | HIGH -- Well-established techniques with extensive peer-reviewed literature. |
| **Confidence: S-007 through S-009, S-011** | HIGH -- Published 2022-2024, high-profile papers from recognized research groups. |
| **Confidence: S-010, S-014** | HIGH for mechanism and general findings; MEDIUM for specific numerical claims (marked [unverified]). |
| **Confidence: S-012** | HIGH -- 70+ years of standardized industrial practice. |
| **Confidence: S-013** | MEDIUM-HIGH -- Well-known mental model; novel application as formal adversarial strategy. |
| **Confidence: S-015** | MEDIUM -- Novel composite; meta-strategy status is provisional pending validation experiments. Fallback defined. |
| **Recommended Follow-Up** | (1) Web-validation pass to confirm URLs, DOIs, and specific numerical claims. (2) S-015 validation experiments before production deployment. (3) Periodic review of Reserved Strategies for promotion. |

---

## L2: New and Revised Architecture Sections

### Systemic Risk: Shared Model Bias

**New section addressing DA-002.**

Six of the 15 strategies (S-007, S-010, S-011, S-013, S-014, S-015) rely on LLMs critiquing their own outputs or the outputs of identical model instances. This creates a systemic risk: **shared model bias**.

#### The Problem

When the same model (or identical instances of a model) serves as both creator and critic, several failure modes emerge:

1. **Consistent blind spots**: If the model cannot detect a certain class of error (e.g., a specific architectural anti-pattern, a subtle logical fallacy, or a domain-specific misconception), then no self-critique strategy will catch it. The strategies are not epistemologically independent -- they share a common knowledge and reasoning base.

2. **Correlated failures in Multi-Agent Debate**: S-009 (Multi-Agent Debate) with identical model instances provides *sampling diversity* (different responses due to temperature/randomness) but not *epistemological diversity* (genuinely different knowledge, reasoning approaches, or domain expertise). Agents "can converge on a shared wrong answer" (acknowledged in S-009 weaknesses), and this convergence is more likely when agents share identical training.

3. **Benchmark transfer gap**: Published empirical results for self-critique strategies (Self-Refine, CoVe, LLM-as-Judge) were measured on specific benchmarks (math, code generation, dialogue, factual QA). Jerry's review targets -- architecture documents, research syntheses, design decisions, governance artifacts -- are substantially different. Effectiveness transfer is assumed but not demonstrated.

#### Mitigations

| Mitigation | Description | Applicable Strategies |
|------------|-------------|----------------------|
| **External tool verification** | Where possible, augment self-critique with tool-based verification: linters for code, link checkers for URLs, test runners for code correctness, schema validators for structured outputs. Tools provide ground-truth that is independent of model bias. | S-007 (CRITIC enhancement), S-011 (tool-augmented CoVe) |
| **Human spot-check** | For high-stakes artifacts, require periodic human review of a sample of critic judgments. This calibrates the system against an independent evaluator. | S-014 (judge calibration), S-015 (gate validation) |
| **Cross-model verification** | Where feasible, use different model providers or configurations for creator and critic roles. This introduces genuine epistemological diversity. Note: Jerry's current architecture uses a single model (Claude), so this mitigation requires architectural extension. | S-009 (debate), S-014 (judging) |
| **Mutation testing for critics** | Periodically inject known defects and verify that critic agents detect them (already described in L2 Calibration section of v1.0.0). A critic that gives high scores to mutated artifacts has a blind spot that must be addressed. | All self-critique strategies |
| **Confidence calibration** | Track the correlation between critic confidence and actual outcome quality over time. If the critic consistently gives high confidence to artifacts that later require revision, the confidence mechanism needs recalibration. | S-014, S-015 |

#### Architectural Principle

**Self-critique strategies are necessary but not sufficient.** They should be treated as a first-pass quality improvement mechanism that catches a meaningful class of errors, not as a comprehensive quality guarantee. For artifacts where the cost of undetected errors is high, at least one external validation mechanism (tool invocation, human review, or cross-model verification) should be incorporated.

This principle is reflected in the S-015 Progressive Adversarial Escalation design: higher escalation levels (Layer 3-4) are intended to apply strategies with greater independence from the creator model, and the ultimate backstop is human review for the most critical decisions.

---

### Escalation Threshold Definitions

**New section addressing RT-003.**

The v1.0.0 catalog uses terms like "critical decisions" and "high-stakes" without defining them. The following threshold criteria are defined for Jerry's review context:

#### Decision Criticality Classification

| Level | Label | Criteria (any one sufficient) | Default Review Layer |
|-------|-------|-------------------------------|---------------------|
| C1 | **Routine** | Reversible within 1 session; affects < 3 files; no external dependency changes | Layer 1 (Self-Check) |
| C2 | **Standard** | Reversible within 1 day; affects 3-10 files or 1-2 components; no API/interface changes | Layer 2 (Standard Critic Review) |
| C3 | **Significant** | Reversible with effort (> 1 day); affects > 10 files or > 2 components; includes API/interface changes; introduces new dependencies | Layer 3 (Deep Adversarial Review) |
| C4 | **Critical** | Irreversible or very costly to reverse; affects system architecture; changes governance/constitutional rules; public-facing release; security-sensitive changes | Layer 4 (Tournament Review) |

#### Escalation Override Rules

1. **Mandatory escalation**: Any artifact touching `docs/governance/JERRY_CONSTITUTION.md` or `.claude/rules/` is automatically C3 or higher.
2. **De-escalation permitted**: If a C3/C4 artifact passes Level 2 review with score >= 0.95 and no HIGH-severity findings, the reviewer may recommend skipping Level 3, with documented justification.
3. **Emergency bypass**: For time-critical security incidents, skip directly to the appropriate level with a documented "escalation bypass" notation.
4. **Human override**: Per P-020 (User Authority), the user may override any escalation decision in either direction.

---

### Industry Practice Integration (Strengthened)

**Revised section addressing DA-004.**

While industry/engineering patterns are represented by one strategy (S-012 FMEA), their implementation practices are incorporated throughout the L2 architecture. This section makes that incorporation explicit:

| Excluded Industry Pattern | Where Incorporated | How Used |
|--------------------------|-------------------|----------|
| **Fagan Inspection** | S-015 escalation gates, S-014 rubrics | Fagan's entry/exit criteria concept is applied to escalation gates (an artifact must pass defined criteria to progress). Fagan's moderator role maps to the LLM-as-Judge (S-014) function. Fagan's defined roles (author, inspector, moderator, reader) inform Jerry's agent role assignments. |
| **Google Code Review** | Default Layer 2 workflow | Google's lightweight, continuous review model (small changes reviewed frequently) is the operational model for Jerry's default Layer 2 workflow. The principle "review early, review often" is encoded in S-015's graduated escalation. |
| **ATAM** | S-001 (architecture review mode), S-008 (scenario probing) | ATAM's quality attribute scenarios (performance, security, modifiability) are used as prompt templates for architecture-focused Red Team and Socratic reviews. ATAM's sensitivity/tradeoff analysis maps to S-005 Dialectical Inquiry. |
| **Pair Programming** | S-010 Self-Refine (real-time variant) | Pair programming's real-time feedback loop is analogous to Self-Refine's generate-feedback-refine loop. For LLM agents, continuous self-review during generation approximates the navigator/driver dynamic. |
| **Design Critique** | S-003 Steelman (strengths-first protocol) | Design Critique's core innovation ("identify strengths before weaknesses") is the defining mechanism of Steelman (S-003). The "I like / I wish / What if" protocol from design critique is available as an alternative prompt template for S-003. |

---

## Appendix A: Reserved Strategies

**New section addressing DA-001 (REC-006).**

The following strategies were excluded from the active catalog but are identified as high-value candidates for future promotion. Each entry includes promotion criteria -- conditions under which the strategy should be added to the active catalog (potentially replacing a lower-performing strategy).

| Rank | Strategy | Source | Reason for Exclusion | Promotion Criteria |
|------|----------|--------|---------------------|-------------------|
| R-1 | **Mutation Testing** | TASK-002 #13 | Tests the reviewer, not the artifact. Important for calibration but not an adversarial review strategy per se. | Promote when Jerry implements a formal critic calibration framework. Mutation testing becomes essential for verifying that adversarial strategies actually detect the defects they claim to catch. Consider promoting alongside or within the S-015 validation experiments. |
| R-2 | **Reference Class Forecasting** | TASK-003 E3 | Requires a reference class database that Jerry does not yet have. | Promote when Jerry has accumulated >= 100 quality-scored artifacts of the same type (e.g., 100 architecture reviews with post-hoc quality assessments). The reference class database can be built from Jerry's `.jerry/data/` persistence layer. Directly addresses base rate neglect, which no current strategy explicitly targets. |
| R-3 | **Fagan Inspection** (as strategy, not just process) | TASK-002 #1 | Classified as process management pattern. | Promote if Jerry extends to multi-human review coordination, where Fagan's defined roles (author, inspector, moderator, reader) and formal meeting protocol become operationally necessary rather than analogical. |
| R-4 | **ATAM** (Architecture Tradeoff Analysis Method) | TASK-002 #3 (excluded) | Scenario-based probing covered by S-008 and S-001. | Promote if Jerry develops dedicated architecture review workflows requiring quality attribute trees, sensitivity analysis, and formal tradeoff documentation. ATAM's structured output format may warrant standalone strategy status in that context. |
| R-5 | **Ensemble Adversarial Meta-Review** | TASK-003 E8 | Orchestration pattern rather than distinct mechanism. Incorporated into L2 architecture. | Promote if empirical experience shows that independent multi-strategy review with formal disagreement analysis produces measurably better outcomes than sequential escalation (S-015). This would represent an alternative to S-015's graduated model. |

---

## Appendix B: Cognitive Bias Mapping

**New section addressing REC-010.**

| Strategy | Primary Biases Countered | Mechanism of Bias Mitigation |
|----------|------------------------|------------------------------|
| S-001 Red Team | Optimism bias, Illusion of invulnerability, Failure of imagination | Forces consideration of adversary's perspective; reveals attack vectors the creator assumed were not viable |
| S-002 Devil's Advocate | Confirmation bias, Groupthink, Anchoring | Institutionalized dissent challenges the prevailing view; counterarguments force consideration of disconfirming evidence |
| S-003 Steelman | Strawman fallacy, Hostile attribution bias, Fundamental attribution error | Charitable reconstruction prevents attacking a distorted version of the argument; ensures engagement with actual position |
| S-004 Pre-Mortem | Optimism bias, Planning fallacy, Illusion of explanatory depth | Temporal reframing ("it has failed") overcomes prospective optimism; gives psychological permission to identify risks |
| S-005 Dialectical Inquiry | Anchoring, Status quo bias, Premature closure | Systematic assumption negation forces consideration of genuine alternatives; synthesis prevents anchoring to first option |
| S-006 ACH | Confirmation bias, Anchoring, Availability bias | Matrix-based multi-hypothesis evaluation forces consideration of all hypotheses against all evidence; diagnostic focus prevents cherry-picking |
| S-007 Constitutional AI | Consistency bias, Omission bias, Scope neglect | Principle-by-principle evaluation prevents selective attention; written standards prevent drift; multi-pass catches different abstraction levels |
| S-008 Socratic Method | Dunning-Kruger effect, Illusion of explanatory depth, Assumption blindness | Probing questions force explicit articulation of reasoning; reveals gaps the reasoner was unaware of |
| S-009 Multi-Agent Debate | Groupthink, Authority bias, Bandwagon effect | Multiple independent perspectives prevent convergence on a single agent's view; competitive structure incentivizes finding flaws |
| S-010 Self-Refine | Satisficing (premature acceptance), First-draft anchoring | Self-feedback loop forces re-evaluation of initial output; iterative improvement overcomes tendency to accept first adequate answer |
| S-011 CoVe | Confirmation bias (for factual claims), Source confusion, Confabulation | Independent verification (without original context) prevents the model from simply confirming its own claims |
| S-012 FMEA | Availability bias, Scope neglect, Neglect of probability | Systematic enumeration of ALL failure modes prevents focus on recent/salient failures; quantitative RPN scoring addresses probability neglect |
| S-013 Inversion | Framing effect, Positive test strategy, Feature-positive bias | Problem reversal reframes the question; generating anti-patterns surfaces risks that positive framing misses |
| S-014 LLM-as-Judge | Halo effect, Leniency bias, Central tendency bias | Explicit rubrics with level descriptions prevent holistic impression-based scoring; structured evaluation reduces rater bias |
| S-015 PAE | Scope insensitivity (applying same review intensity to all work), Sunk cost (continuing expensive review when unnecessary) | Graduated escalation matches review intensity to artifact criticality; gates prevent wasting expensive methods on fundamentally flawed work |

**Bias Coverage Gaps:** The following biases are not directly targeted by any of the 15 strategies and represent potential areas for future enhancement:
- **Base rate neglect**: Would be addressed by Reference Class Forecasting (Reserved Strategy R-2)
- **Survivorship bias**: Partially addressed by S-004 Pre-Mortem but no strategy specifically examines "what succeeded and why" to control for survivorship
- **Curse of knowledge**: No strategy specifically accounts for the expert's inability to see their work from a novice's perspective

---

## Appendix C: Specification Deviation Record

**New section addressing RT-001.**

### Deviation: Replacement of Blue Team and Strawman as Foundational Strategies

| Field | Value |
|-------|-------|
| **Deviation ID** | EN-301-DEV-001 |
| **Specification Reference** | EN-301, Summary: "The catalog must cover the five foundational strategies -- Red Team, Blue Team, Devil's Advocate, Steelman, and Strawman" |
| **Actual Implementation** | Blue Team replaced by Pre-Mortem (S-004); Strawman replaced by Dialectical Inquiry (S-005) |
| **Decision Made By** | ps-synthesizer agent (TASK-004), without explicit user approval |
| **P-020 Assessment** | This deviation represents an agent overriding the task specification. While the technical reasoning is defensible, P-020 (User Authority) states: "User decides. Never override." The deviation should be brought to user attention for ratification or reversal. |

#### Rationale for Deviation

**Blue Team Replacement (S-004 Pre-Mortem instead):**
- Blue Team in the security domain refers to the *defensive* team that responds to Red Team findings. It is the *target* of adversarial review, not an adversarial review method itself.
- In Jerry's architecture, the "Blue Team" function is performed by the creator agent responding to critic findings -- this is the default workflow, not a distinct strategy requiring a catalog entry.
- Pre-Mortem (S-004) fills the slot with a distinct adversarial mechanism (prospective hindsight) not otherwise represented in the catalog.
- **Counter-argument acknowledged (from RT-001):** Blue Team could be reframed as "defensive adversarial testing" -- proactively defending against anticipated attacks. This is a legitimate interpretation in some security contexts. If this interpretation is preferred, Blue Team could replace S-004 or be added as Reserved Strategy R-6.

**Strawman Replacement (S-005 Dialectical Inquiry instead):**
- Strawman as an argumentative technique means presenting a weakened version of an argument to defeat it. This is an argumentative *fallacy*, not a legitimate adversarial strategy for rigorous review.
- **Counter-argument acknowledged (from RT-001):** In red teaming contexts, deliberately presenting a weakened version to test whether the audience can distinguish it from the real argument is a legitimate technique. However, this specific application is narrow and is subsumed by Red Team (S-001) which already includes adversary modeling and deception.
- Dialectical Inquiry (S-005) fills the slot with a well-validated strategy (Schweiger et al., 1986) that produces genuine novel alternatives, which Strawman does not.

#### Risk Acceptance

The deviation is accepted with the following conditions:
1. **User notification**: This deviation is flagged for user review at the next project checkpoint.
2. **Reversibility**: Both Pre-Mortem (S-004) and Dialectical Inquiry (S-005) can be replaced with Blue Team and Strawman without structural impact to the catalog, as the Reserved Strategies framework supports catalog evolution.
3. **Documentation**: This deviation record serves as the formal ADR for the decision.

#### Revisitation Conditions

This deviation should be revisited if:
- The user explicitly requests Blue Team and/or Strawman inclusion
- Jerry develops a dedicated security review workflow where Blue Team defensive testing is operationally distinct from the standard creator-responds-to-critic flow
- A new use case emerges where deliberate strawmanning (presenting weakened arguments to test audience discernment) provides value that is not covered by Red Team (S-001)

---

## References

### Citation Corrections and Standardizations (REC-007)

The following corrections and standardizations apply to the v1.0.0 reference list:

| # | Citation | Correction |
|---|----------|------------|
| 17 | Selye, H. (1956). *The Stress of Life*. McGraw-Hill. | ISBN not available for original 1956 edition. Revised edition (1978) ISBN: 978-0070562127. Original 1956 edition predates ISBN system (introduced 1970). |
| 19 | Mitroff, I. I., & Emshoff, J. R. (1979). DOI: 10.2307/257398 | **Clarification:** 10.2307/257398 is a JSTOR stable URL identifier, not a CrossRef DOI. The JSTOR stable URL is: https://www.jstor.org/stable/257398. The AMR paper may have a separate CrossRef DOI [unverified from training data]. |
| 25 | Bai, Y., et al. (2022). arXiv: 2212.08073 | **Standardized to:** arXiv:2212.08073v2 (v2 is the version cited by most references) [unverified: version number from training data]. |
| 26 | Irving, G., et al. (2018). arXiv: 1805.00899 | **Standardized to:** arXiv:1805.00899v2 [unverified: version number from training data]. |
| 27 | Du, Y., et al. (2023). arXiv: 2305.14325 | **Standardized to:** arXiv:2305.14325v2 [unverified: version number from training data]. Published at ICML 2023. |
| 31 | Madaan, A., et al. (2023). arXiv: 2303.17651 | **Standardized to:** arXiv:2303.17651v3 [unverified: version number from training data]. Published at NeurIPS 2023. |
| 32 | Dhuliawala, S., et al. (2023). arXiv: 2309.11495 | **Standardized to:** arXiv:2309.11495v2 [unverified: version number from training data]. |
| 33 | Zheng, L., et al. (2023). arXiv: 2306.05685 | **Standardized to:** arXiv:2306.05685v4 [unverified: version number from training data]. Published at NeurIPS 2023. |
| 34 | Liu, Y., et al. (2023). arXiv: 2303.16634 | **Standardized to:** arXiv:2303.16634v3 [unverified: version number from training data]. |
| 35 | Kim, S., et al. (2023). arXiv: 2310.08491 | **Standardized to:** arXiv:2310.08491v2 [unverified: version number from training data]. |
| 45 | Dreyfus, S. E., & Dreyfus, H. L. (1980). "UC Berkeley ORC" | **Standardized to:** Dreyfus, S. E., & Dreyfus, H. L. (1980). *A Five-Stage Model of the Mental Activities Involved in Directed Skill Acquisition*. Operations Research Center, University of California, Berkeley. Technical Report ORC 80-2. |
| 46 | Anthropic. (2023). Claude's Constitution. URL | **Note:** The URL https://www.anthropic.com/index/claudes-constitution may have been restructured. Alternative URL: https://www.anthropic.com/research/claudes-constitution [unverified: URL may be stale; verify before citing]. |

### New References Added in This Revision

| # | Citation | Context |
|---|----------|---------|
| 47 | Nemeth, C. J., Brown, K., & Rogers, J. (2001). Devil's advocate versus authentic dissent. *European Journal of Social Psychology*, 31(6), 707-720. DOI: 10.1002/ejsp.58. | Referenced in S-002 weaknesses (already in v1.0.0 text; now added to reference list). Also cited in TASK-005 review. |
| 48 | Janis, I. L. (1972). *Victims of Groupthink*. Houghton Mifflin. ISBN: 978-0395140444. | Referenced in S-002 strengths (already in v1.0.0 text; now added to reference list). Also cited in TASK-005 review. |

---

*Document ID: FEAT-004:EN-301:TASK-006*
*PS ID: EN-301*
*Entry ID: TASK-006*
*Agent: ps-researcher (creator revision)*
*Created: 2026-02-13*
*Revision of: TASK-004-unified-catalog.md v1.0.0*
*Review Addressed: TASK-005-adversarial-review-iter1.md*
*Status: Complete*
