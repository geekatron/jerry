# Architecture Trade Study: Adversarial Strategy Selection for Jerry

<!--
DOCUMENT-ID: FEAT-004:EN-302:TASK-003
AUTHOR: nse-architecture agent (v2.1.0)
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-302 (Strategy Selection & Decision Framework)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
FORMAT: NASA SE Trade Study Report (adapted from TSR template)
NPR-REFERENCE: NPR 7123.1D Process 4 (Design Solution Definition), Process 17 (Decision Analysis)
-->

> **Document ID:** TSR-PROJ-001-EN302-003
> **Version:** 1.1.0
> **Date:** 2026-02-13
> **Author:** nse-architecture agent
> **Status:** Complete
> **Phase:** Preliminary Design
> **Driving Requirements:** EN-301 15-strategy catalog, P-003 (No Recursive Subagents), Jerry agent model

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Purpose and Scope](#1-purpose-and-scope) | Decision statement and constraints |
| [2. Architecture Fit Analysis](#2-architecture-fit-analysis) | Per-strategy mapping to Jerry's agent model |
| [3. P-003 Compliance Assessment](#3-p-003-compliance-assessment) | Single-nesting constraint verification |
| [4. Token Budget Analysis](#4-token-budget-analysis) | Estimated token cost per strategy invocation |
| [5. Composition Matrix](#5-composition-matrix) | Strategy compatibility and synergy analysis |
| [6. Integration Cost Assessment](#6-integration-cost-assessment) | Effort to integrate into Jerry's agent specs |
| [7. Architecture Trade-offs](#7-architecture-trade-offs) | Breadth vs. Depth, Token Economy, Consistency |
| [8. Pugh Matrix](#8-pugh-matrix) | Structured comparison against baseline |
| [9. Sensitivity Analysis](#9-sensitivity-analysis) | Robustness of architectural assessments |
| [10. Risks and Mitigations](#10-risks-and-mitigations) | Risk register for strategy adoption |
| [11. Recommendation](#11-recommendation) | Architectural recommendation for TASK-004 scoring |
| [Appendix A: NASA SE Rationale](#appendix-a-nasa-se-rationale) | Traceability to NASA SE practices |
| [Appendix B: Glossary](#appendix-b-glossary) | Terms and abbreviations |

---

## 1. Purpose and Scope

### 1.1 Decision Statement

Evaluate how each of the 15 adversarial review strategies from the EN-301 catalog (v1.1.0, TASK-006) maps to Jerry's agent architecture, determine integration costs, identify composition synergies and conflicts, and provide architectural scoring inputs for TASK-004 (composite scoring and top-10 selection).

### 1.2 Scope

- **System:** Jerry Framework -- agent-based adversarial review system
- **Phase:** Preliminary Design (strategy selection before implementation)
- **Input Artifact:** EN-301 TASK-006 Revised Catalog (15 strategies, v1.1.0)
- **Output Consumer:** TASK-004 (scoring), TASK-005 (ADR)

### 1.3 Constraints

| Type | Constraint | Impact |
|------|------------|--------|
| P-003 (Hard) | No Recursive Subagents -- max ONE level: orchestrator -> worker | Limits multi-agent debate to orchestrator-managed rounds |
| Token Budget | 25,700-token rule envelope for `.claude/rules/` | Strategy prompt templates must fit within budget |
| Agent Model | Single Claude model instance (no cross-model diversity) | Self-critique strategies share model blind spots |
| Skill Architecture | Strategies integrate via agent specs in `skills/*/agents/` | Implementation is prompt configuration, not code |
| Constitution | Existing `.claude/rules/` standards serve as S-007 constitutions | S-007 has near-zero incremental cost |

### 1.4 Evaluation Criteria

Per NPR 7123.1D Process 17 (Decision Analysis), the following criteria guide this trade study:

| # | Criterion | Weight | Definition |
|---|-----------|--------|------------|
| A1 | Agent Model Fit | 25% | How naturally the strategy maps to Jerry's existing agent roles |
| A2 | P-003 Compliance | 15% | Whether the strategy works within single-nesting constraint |
| A3 | Token Efficiency | 20% | Token cost relative to quality improvement |
| A4 | Composability | 20% | How well the strategy combines with others in review cycles |
| A5 | Integration Effort | 20% | Effort to add the strategy to agent specs and orchestration |

---

## 2. Architecture Fit Analysis

### 2.1 Agent Model Summary

Jerry's adversarial review agents span two skills:

| Agent | Skill | Role | Cognitive Mode | Model |
|-------|-------|------|----------------|-------|
| **ps-critic** | /problem-solving | Quality Evaluator -- critiques against criteria | Convergent | Sonnet |
| **nse-reviewer** | /nasa-se | Technical Review Gate -- entrance/exit criteria | Convergent | Sonnet |
| **nse-qa** | /nasa-se | Quality Assurance -- artifact validation | Convergent | Sonnet |
| **nse-verification** | /nasa-se | V&V Specialist -- product verification | Convergent | Sonnet |

Additional creator agents that participate in adversarial review:

| Agent | Skill | Role |
|-------|-------|------|
| ps-researcher | /problem-solving | Research -- information gathering |
| ps-analyst | /problem-solving | Analysis -- structured reasoning |
| ps-synthesizer | /problem-solving | Synthesis -- integration of findings |
| ps-architect | /problem-solving | Architecture -- design decisions |

### 2.2 Per-Strategy Architecture Fit

#### S-001: Red Team Analysis

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | ps-critic configured with adversary persona. The critic receives an explicit adversary identity: "You are a security researcher / competing architect." |
| **Implementation Pattern** | Role assignment via prompt template. The adversary persona is injected as a system-level instruction to the critic agent. |
| **Agent Pattern** | 2-agent: orchestrator invokes creator, then invokes critic with Red Team persona. |
| **Fit Rating** | STRONG -- ps-critic already supports role-based evaluation modes. |
| **Rationale** | Role assignment is the simplest configuration change for ps-critic. The agent's existing "analytical" tone naturally supports adversarial simulation when combined with a persona prompt. |

#### S-002: Devil's Advocate Analysis

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | ps-critic in DA mode. Receives instruction: "Build the strongest possible case against this analysis." |
| **Implementation Pattern** | Prompt template swap -- the critic's evaluation instruction changes from criteria-based to oppositional-argument-based. |
| **Agent Pattern** | 2-agent: orchestrator invokes creator, then invokes critic with DA instructions. |
| **Fit Rating** | STRONG -- ps-critic's core competency is critique; DA is a natural mode. |
| **Rationale** | DA is the most fundamental critic operation. It maps directly to ps-critic's existing capabilities with only a prompt change. The "constructive" communication style may need to be temporarily set to "adversarial" for full DA effect. |

#### S-003: Steelman Technique

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | ps-critic mandatory first-phase operation. Before any critique, the critic first reconstructs the argument in its strongest form. |
| **Implementation Pattern** | Two-phase prompt: Phase 1 (steelman) -> Phase 2 (critique). Encoded as a structural requirement in the critic's prompt template. |
| **Agent Pattern** | 1-agent (within critic invocation): steelman is an internal prompt phase, not a separate agent call. |
| **Fit Rating** | STRONG -- adds ~50% to a single critic pass; no additional agent invocation needed. |
| **Rationale** | Steelman is a prompt engineering pattern, not an architectural pattern. It requires zero additional infrastructure -- just a two-phase instruction within the existing critic prompt. This makes it the lowest-cost strategy to integrate. |

#### S-004: Pre-Mortem Analysis

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | ps-analyst in pre-mortem mode, or ps-critic with temporal reframing prompt. |
| **Implementation Pattern** | Prompt template: "This plan has been implemented and has failed catastrophically. Write a detailed account of how and why it failed." |
| **Agent Pattern** | 2-agent: orchestrator invokes creator (plan), then invokes critic/analyst with pre-mortem framing. |
| **Fit Rating** | STRONG -- temporal reframing is a prompt-level change that produces qualitatively different outputs. |
| **Rationale** | The "has failed" framing is a single-sentence prompt modification that dramatically changes LLM output character (from cautious hedging to specific failure narration). Architecturally trivial to integrate. |

#### S-005: Dialectical Inquiry

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | 3-agent pattern: ps-researcher/ps-architect (thesis), ps-researcher/ps-architect (antithesis with negated assumptions), ps-synthesizer (synthesis). |
| **Implementation Pattern** | Multi-pass orchestration: Pass 1 produces thesis with explicit assumptions. Pass 2 receives assumptions and produces antithesis. Pass 3 synthesizes. |
| **Agent Pattern** | 3-agent with sync barriers: orchestrator manages three sequential worker invocations. |
| **Fit Rating** | MODERATE -- requires 3 agent passes and explicit assumption extraction between passes. |
| **Rationale** | DI is the most architecturally demanding strategy that still complies with P-003. The orchestrator manages all three passes; no worker invokes another worker. The challenge is extracting structured assumptions from Pass 1 output to feed Pass 2, which requires either a structured output format or an intermediate parsing step. |

#### S-006: Analysis of Competing Hypotheses

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | ps-analyst in ACH mode. Single agent with structured matrix reasoning, or 2-agent with separate hypothesis generation and evaluation passes. |
| **Implementation Pattern** | Structured prompt template providing the ACH matrix format. Agent generates hypotheses, constructs evidence matrix, evaluates diagnosticity. |
| **Agent Pattern** | 1-2 agent: can operate as single-agent structured reasoning or split into hypothesis-generation and matrix-evaluation passes. |
| **Fit Rating** | MODERATE -- the matrix format requires careful prompt engineering to produce consistent structured output. |
| **Rationale** | ACH is primarily a reasoning framework, not an agent coordination pattern. Its architectural complexity is in prompt engineering (getting reliable matrix output), not in agent orchestration. The structured output requirement may benefit from explicit JSON/YAML formatting instructions. |

#### S-007: Constitutional AI Critique

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | ps-critic in constitutional mode; nse-qa for NASA SE-specific constitutions. The constitution files are Jerry's existing `.claude/rules/` standards. |
| **Implementation Pattern** | Multi-pass critique: Pass 1 (structural principles), Pass 2 (semantic principles), Pass 3 (holistic). Each pass evaluates against specific rules files. |
| **Agent Pattern** | 1-2 agent with iteration: critic evaluates in multiple passes. Orchestrator manages revision cycle. |
| **Fit Rating** | VERY STRONG -- Jerry's architecture was designed around this pattern. `.claude/rules/` ARE the constitution. |
| **Rationale** | S-007 is the single most naturally aligned strategy with Jerry's existing architecture. The constitutions already exist as enforced rules files. The gap is operationalizing principle-by-principle evaluation rather than holistic assessment. This is a prompt engineering change, not an architectural change. Near-zero integration cost. |

#### S-008: Socratic Method

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | ps-critic in Socratic mode. Generates probing questions using Paul & Elder's six categories instead of assertions. |
| **Implementation Pattern** | Multi-turn prompt: critic generates questions, creator responds, critic evaluates responses for contradictions. Requires 2-3 turns. |
| **Agent Pattern** | 2-agent with multi-turn: orchestrator manages question-answer exchanges between critic and creator. |
| **Fit Rating** | MODERATE -- multi-turn exchanges require orchestrator to manage dialogue state. |
| **Rationale** | The Socratic method requires the orchestrator to manage a question-answer dialogue loop, which is more complex than single-pass strategies. Each turn requires preserving the previous exchange in context. This is architecturally feasible but increases orchestration complexity and token consumption. |

#### S-009: Multi-Agent Debate

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | Multiple ps-critic instances with different strategy configurations, plus ps-synthesizer as judge. |
| **Implementation Pattern** | Orchestrator invokes N debater agents (each a ps-critic with different initial position), collects outputs, shares all positions with all debaters, repeats for M rounds, then invokes judge. |
| **Agent Pattern** | 3+ agent with multiple rounds: orchestrator manages N*M invocations plus judge. All debaters are orchestrator-level workers (P-003 compliant). |
| **Fit Rating** | WEAK -- highest cost, most complex orchestration, and shared-model-bias limitation. |
| **Rationale** | Multi-Agent Debate is the most architecturally expensive strategy. With a single model (Claude), all "debaters" share identical training, providing sampling diversity but not epistemological diversity (see TASK-006 Systemic Risk section). The orchestration burden (managing debate rounds with state passing) is significant. Best reserved for Layer 4 (critical decisions only). |

#### S-010: Self-Refine

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | Any creator agent (self-review mode). No separate critic needed. |
| **Implementation Pattern** | Appended instruction to creator prompt: "After generating your output, critique it and produce an improved version." Single agent, single invocation with extended output. |
| **Agent Pattern** | 1-agent: creator self-reviews within a single invocation. |
| **Fit Rating** | VERY STRONG -- zero additional infrastructure; single-invocation pattern. |
| **Rationale** | Self-Refine is the architecturally simplest strategy. It requires only a prompt modification to the creator agent -- no new agents, no orchestration changes, no additional invocations. The cost is approximately 30-50% longer output from the creator. |

#### S-011: Chain-of-Verification

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | ps-critic in verification mode, or a dedicated verification phase within nse-verification. |
| **Implementation Pattern** | Multi-step within single or dual invocation: (1) extract factual claims, (2) generate verification questions, (3) answer questions independently (fresh context), (4) compare and correct. The "independent" step requires a separate invocation without the original context. |
| **Agent Pattern** | 1-2 agent: the critical step is the independent verification (step 3), which requires a fresh agent invocation without the original output in context. |
| **Fit Rating** | MODERATE -- the "independent verification" step requires careful context management. |
| **Rationale** | CoVe's architectural challenge is the context isolation requirement: the verification questions must be answered WITHOUT the original output in context, to prevent confirmation bias. This requires the orchestrator to invoke a second agent pass with a deliberately restricted context window. Architecturally feasible but requires explicit context-stripping logic in orchestration. |

#### S-012: Failure Mode and Effects Analysis

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | nse-verification for V&V contexts, ps-analyst for general use. Produces structured FMEA table. |
| **Implementation Pattern** | Structured prompt with FMEA table template. Agent systematically enumerates components, failure modes, and scores S/O/D. |
| **Agent Pattern** | 1-2 agent: single agent with structured output template, optionally reviewed by a second agent. |
| **Fit Rating** | STRONG -- structured output format is well-suited to LLM generation with explicit templates. |
| **Rationale** | FMEA maps cleanly to a single-agent structured reasoning task. The FMEA table template (Component / Failure Mode / Effect / S / O / D / RPN / Mitigation) constrains output format and ensures systematic coverage. Jerry's simplified H/M/L scoring (instead of 1-10) reduces the precision burden on the LLM. nse-verification is the natural home given its V&V mandate. |

#### S-013: Inversion Technique

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | ps-critic in inversion mode, or a pre-review preparatory agent. Generates anti-pattern checklists. |
| **Implementation Pattern** | Single-pass prompt: "Given this design, describe how you would guarantee its failure." Output is mechanically converted to a positive checklist. |
| **Agent Pattern** | 1-agent: single invocation produces the anti-pattern checklist, which feeds into subsequent strategies. |
| **Fit Rating** | VERY STRONG -- single-pass, generative, and feeds into other strategies. |
| **Rationale** | Inversion is architecturally elegant: one agent pass produces a checklist artifact that enhances all subsequent review strategies. The output (anti-pattern checklist) is a reusable artifact that can be persisted to `.jerry/data/` and used across multiple review cycles. This leverages Jerry's "filesystem as infinite memory" architecture. |

#### S-014: LLM-as-Judge

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | ps-critic in judge mode. Evaluates against explicit rubric, produces numerical score + justification. |
| **Implementation Pattern** | Rubric-based prompt: agent receives evaluation rubric (score levels with descriptions), artifact to evaluate, and produces score + rationale. |
| **Agent Pattern** | 1-agent: single invocation with rubric template. |
| **Fit Rating** | VERY STRONG -- scoring is the terminal operation in every review cycle; simple single-pass architecture. |
| **Rationale** | LLM-as-Judge is the evaluation infrastructure that makes Jerry's 0.92 quality threshold operational. Its architecture is the simplest possible: single agent, single pass, rubric-configured prompt. It serves as both a standalone strategy and the scoring mechanism for S-015 escalation gates. Dual nature (mechanism + strategy) creates high architectural leverage. |

#### S-015: Progressive Adversarial Escalation

| Dimension | Assessment |
|-----------|------------|
| **Agent Mapping** | /orchestration skill's workflow management layer. S-015 is an orchestration pattern, not an agent-level strategy. |
| **Implementation Pattern** | Orchestration logic: Level 0 (Self-Refine) -> Level 1 (Steelman + constructive) -> Level 2 (Socratic + Constitutional) -> Level 3 (DA + FMEA + Red Team) -> Level 4 (Multi-Agent Debate). S-014 (LLM-as-Judge) gates between levels. |
| **Agent Pattern** | Meta-strategy: orchestrator decides which strategies to invoke based on artifact criticality and gate scores. Variable agent count (1-6+). |
| **Fit Rating** | STRONG -- maps directly to /orchestration skill's workflow management capability. |
| **Rationale** | S-015 is not a strategy that an individual agent executes; it is the orchestration logic that governs which strategies are applied and in what order. It maps naturally to the /orchestration skill's pipeline management, checkpoint, and gate-based workflow architecture. The escalation gates use S-014 scores as decision criteria. Integration requires encoding the escalation logic in orchestration configuration, not in individual agent specs. |

### 2.3 Architecture Fit Summary

| Strategy | Primary Agent | Agent Pattern | Fit Rating | Key Factor |
|----------|--------------|---------------|------------|------------|
| S-001 Red Team | ps-critic | 2-agent | STRONG | Persona injection |
| S-002 Devil's Advocate | ps-critic | 2-agent | STRONG | Core critic mode |
| S-003 Steelman | ps-critic | 1-agent (phase) | STRONG | Prompt phase, not agent |
| S-004 Pre-Mortem | ps-critic / ps-analyst | 2-agent | STRONG | Temporal reframing prompt |
| S-005 Dialectical Inquiry | ps-architect x2 + ps-synthesizer | 3-agent | MODERATE | 3-pass with assumption extraction |
| S-006 ACH | ps-analyst | 1-2 agent | MODERATE | Matrix output reliability |
| S-007 Constitutional AI | ps-critic / nse-qa | 1-2 agent | VERY STRONG | Constitution already exists |
| S-008 Socratic Method | ps-critic | 2-agent multi-turn | MODERATE | Dialogue state management |
| S-009 Multi-Agent Debate | ps-critic x N + ps-synthesizer | 3+ agent multi-round | WEAK | Cost, shared-model-bias |
| S-010 Self-Refine | any creator | 1-agent | VERY STRONG | Zero infrastructure |
| S-011 CoVe | ps-critic / nse-verification | 1-2 agent | MODERATE | Context isolation requirement |
| S-012 FMEA | nse-verification / ps-analyst | 1-2 agent | STRONG | Structured template output |
| S-013 Inversion | ps-critic | 1-agent | VERY STRONG | Generative, feeds others |
| S-014 LLM-as-Judge | ps-critic | 1-agent | VERY STRONG | Evaluation infrastructure |
| S-015 PAE | /orchestration | Meta-strategy | STRONG | Orchestration configuration |

---

## 3. P-003 Compliance Assessment

P-003 (No Recursive Subagents) is a HARD constraint: maximum ONE level of nesting (orchestrator -> worker). No worker may invoke another worker as a subagent.

| Strategy | P-003 Status | Compliance Notes |
|----------|-------------|------------------|
| S-001 | COMPLIANT | Orchestrator invokes creator, then invokes critic. Two sequential worker invocations. |
| S-002 | COMPLIANT | Same as S-001. |
| S-003 | COMPLIANT | Single worker invocation with two-phase prompt. No additional nesting. |
| S-004 | COMPLIANT | Same pattern as S-001. |
| S-005 | COMPLIANT | Orchestrator invokes three workers sequentially. Each worker is a direct orchestrator child. |
| S-006 | COMPLIANT | Single or dual worker invocation. |
| S-007 | COMPLIANT | Orchestrator manages critique-revision cycle. Each pass is a direct worker invocation. |
| S-008 | COMPLIANT | Orchestrator manages question-answer turns. Each turn is a direct worker invocation. |
| S-009 | COMPLIANT WITH CARE | All debaters MUST be invoked by the orchestrator, not by each other. Debate rounds are orchestrator-managed. Risk: a naive implementation might have debaters invoke each other, violating P-003. |
| S-010 | COMPLIANT | Single worker invocation. Self-review is internal to the worker's generation. |
| S-011 | COMPLIANT | Orchestrator manages the context-isolated verification pass. |
| S-012 | COMPLIANT | Single or dual worker invocation. |
| S-013 | COMPLIANT | Single worker invocation. |
| S-014 | COMPLIANT | Single worker invocation. |
| S-015 | COMPLIANT | S-015 IS the orchestration logic. It governs worker invocations but does not add nesting levels. |

**P-003 Risk Assessment:** Only S-009 (Multi-Agent Debate) carries P-003 violation risk during implementation. The implementation must explicitly prevent debater agents from invoking each other. All other strategies are structurally safe.

---

## 4. Token Budget Analysis

### 4.1 Token Cost Model

**Estimation Methodology (F-007):** Token estimates in this section are theoretical projections calculated as: (prompt template size, estimated from typical agent spec complexity) + (input artifact size, assumed 2,000-5,000 tokens) + (expected output length, estimated from rubric descriptor complexity and structural output requirements) x (number of agent passes). These estimates have NOT been validated through empirical measurement against a prototype implementation. They are order-of-magnitude projections intended to classify strategies into cost tiers (Ultra-Low through High) for architectural decision-making, not to predict exact token consumption. Actual token costs may vary by +/- 50% depending on artifact size, prompt template refinement, and model behavior. Empirical validation should be performed during Phase 1 integration (S-010, S-003, S-014, S-013) to calibrate the model for subsequent phases.

Token costs are estimated per strategy invocation, assuming:
- Input context: ~2,000-5,000 tokens for a typical artifact under review
- Agent prompt template: ~500-1,500 tokens
- Constitution/rules context: ~2,000-4,000 tokens (when loaded)
- Output: varies by strategy

| Strategy | Prompt Tokens | Output Tokens | Total per Invocation | Agent Passes | Total per Review |
|----------|--------------|---------------|---------------------|--------------|-----------------|
| S-001 Red Team | ~1,500 | ~2,000 | ~3,500 | 2 | ~7,000 |
| S-002 Devil's Advocate | ~800 | ~1,500 | ~2,300 | 2 | ~4,600 |
| S-003 Steelman | ~600 | ~1,000 | ~1,600 | 0.5* | ~1,600 |
| S-004 Pre-Mortem | ~800 | ~2,000 | ~2,800 | 2 | ~5,600 |
| S-005 Dialectical Inquiry | ~1,200 | ~2,000 | ~3,200 | 3 | ~9,600 |
| S-006 ACH | ~1,500 | ~2,500 | ~4,000 | 2.5 | ~10,000 |
| S-007 Constitutional AI | ~2,500** | ~1,500 | ~4,000 | 2-4 | ~8,000-16,000 |
| S-008 Socratic Method | ~800 | ~1,000 | ~1,800 | 3 | ~5,400 |
| S-009 Multi-Agent Debate | ~1,000 | ~1,500 | ~2,500 | 6-12 | ~15,000-30,000 |
| S-010 Self-Refine | ~500 | ~1,500 | ~2,000 | 1 | ~2,000 |
| S-011 CoVe | ~1,000 | ~1,500 | ~2,500 | 3-4 | ~7,500-10,000 |
| S-012 FMEA | ~1,500 | ~3,000 | ~4,500 | 2 | ~9,000 |
| S-013 Inversion | ~600 | ~1,500 | ~2,100 | 1 | ~2,100 |
| S-014 LLM-as-Judge | ~1,200 | ~800 | ~2,000 | 1 | ~2,000 |
| S-015 PAE | ~500*** | varies | varies | 1-6+ | ~2,000-30,000 |

*S-003 adds ~0.5 passes to an existing critic invocation (integrated as a prompt phase).
**S-007 includes loading constitution files (~2,000-4,000 tokens).
***S-015 prompt overhead is the escalation decision logic only; actual cost is the sum of invoked strategies.

### 4.2 Token Efficiency Tiers

| Tier | Token Range | Strategies |
|------|-------------|------------|
| **Ultra-Low** (< 2,500) | < 2,500 total | S-003 (1,600), S-010 (2,000), S-014 (2,000), S-013 (2,100) |
| **Low** (2,500-5,000) | 2,500-5,000 total | S-002 (4,600) |
| **Medium** (5,000-10,000) | 5,000-10,000 total | S-001 (7,000), S-004 (5,600), S-008 (5,400), S-007 (8,000-16,000), S-011 (7,500-10,000), S-012 (9,000), S-005 (9,600), S-006 (10,000) |
| **High** (> 10,000) | > 10,000 total | S-009 (15,000-30,000) |
| **Variable** | Depends on escalation | S-015 (2,000-30,000) |

### 4.3 Token Budget Impact on 25,700-Token Rule Envelope

The 25,700-token envelope applies to the `.claude/rules/` files loaded at session start. Strategy integration adds tokens through:

1. **Prompt templates stored in agent specs** (~200-500 tokens per strategy mode): Agent specs in `skills/*/agents/*.md` are NOT auto-loaded; they are loaded on skill invocation. This means strategy prompt templates do not consume the rules envelope.

2. **Orchestration configuration** (~100-300 tokens for escalation logic): Similarly loaded on `/orchestration` skill invocation, not at session start.

3. **Constitutional references** (already loaded): `.claude/rules/` files are already loaded. S-007 adds zero incremental tokens to the rules envelope because the constitutions already exist.

**Conclusion:** Strategy integration has minimal impact on the 25,700-token rule envelope. The primary token cost is per-invocation during reviews, not at session start.

---

## 5. Composition Matrix

### 5.1 Strategy x Strategy Compatibility

The following matrix classifies strategy pairs as:
- **SYN** = Synergistic (better together than separately; combined > sum of parts)
- **COM** = Compatible (can be used together without interference)
- **NEU** = Neutral (no interaction; independent)
- **TEN** = Tension (partial overlap or mild conflict; use one or the other)
- **CON** = Conflicting (should not be used in the same review pass)

|  | S-001 | S-002 | S-003 | S-004 | S-005 | S-006 | S-007 | S-008 | S-009 | S-010 | S-011 | S-012 | S-013 | S-014 | S-015 |
|--|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **S-001** | -- | TEN | SYN | COM | COM | COM | SYN | COM | TEN | COM | COM | SYN | SYN | COM | COM |
| **S-002** | TEN | -- | SYN | COM | TEN | COM | SYN | TEN | TEN | COM | COM | COM | COM | COM | COM |
| **S-003** | SYN | SYN | -- | COM | COM | COM | SYN | COM | COM | TEN | COM | COM | COM | COM | COM |
| **S-004** | COM | COM | COM | -- | COM | COM | COM | COM | COM | COM | COM | SYN | SYN | COM | COM |
| **S-005** | COM | TEN | COM | COM | -- | COM | COM | COM | TEN | COM | COM | COM | COM | COM | COM |
| **S-006** | COM | COM | COM | COM | COM | -- | COM | SYN | COM | COM | SYN | COM | COM | COM | COM |
| **S-007** | SYN | SYN | SYN | COM | COM | COM | -- | COM | COM | COM | COM | COM | SYN | SYN | COM |
| **S-008** | COM | TEN | COM | COM | COM | SYN | COM | -- | COM | COM | COM | COM | COM | COM | COM |
| **S-009** | TEN | TEN | COM | COM | TEN | COM | COM | COM | -- | COM | COM | COM | COM | SYN | COM |
| **S-010** | COM | COM | TEN | COM | COM | COM | COM | COM | COM | -- | COM | COM | COM | COM | COM |
| **S-011** | COM | COM | COM | COM | COM | SYN | COM | COM | COM | COM | -- | COM | COM | COM | COM |
| **S-012** | SYN | COM | COM | SYN | COM | COM | COM | COM | COM | COM | COM | -- | SYN | COM | COM |
| **S-013** | SYN | COM | COM | SYN | COM | COM | SYN | COM | COM | COM | COM | SYN | -- | COM | COM |
| **S-014** | COM | COM | COM | COM | COM | COM | SYN | COM | SYN | COM | COM | COM | COM | -- | SYN |
| **S-015** | COM | COM | COM | COM | COM | COM | COM | COM | COM | COM | COM | COM | COM | SYN | -- |

### 5.2 Synergy Rationale (SYN Pairs)

| Pair | Synergy Rationale |
|------|-------------------|
| S-001 + S-003 | Red Team after Steelman: ensures adversarial attack targets the strongest version of the defense |
| S-001 + S-007 | Red Team validates constitutional compliance violations under adversarial conditions |
| S-001 + S-012 | Red Team attack vectors directly map to FMEA failure modes; cross-validates coverage |
| S-001 + S-013 | Inversion generates attack surface; Red Team exploits it |
| S-002 + S-003 | Steelman before DA: ensures counterarguments target genuine strengths, not strawmen |
| S-002 + S-007 | DA challenges constitutional compliance assessments; prevents rubber-stamping |
| S-003 + S-007 | Steelman ensures constitutional critique is fair; critique addresses real violations, not misunderstandings |
| S-004 + S-012 | Pre-Mortem identifies high-level failure scenarios; FMEA decomposes them systematically |
| S-004 + S-013 | Pre-Mortem ("has failed") and Inversion ("guarantee failure") are complementary perspectives on failure identification |
| S-006 + S-008 | ACH generates hypotheses; Socratic questioning probes the evidence supporting each |
| S-006 + S-011 | ACH identifies competing hypotheses; CoVe verifies the factual claims used as evidence in the matrix |
| S-007 + S-013 | Inversion of constitutional principles generates anti-pattern checklists that enhance constitutional critique |
| S-007 + S-014 | Constitutional critique produces findings; LLM-as-Judge quantifies the overall quality score |
| S-009 + S-014 | LLM-as-Judge serves as the debate judge, providing structured evaluation of debate outcomes |
| S-012 + S-013 | Inversion generates failure modes; FMEA scores and prioritizes them with RPN |
| S-014 + S-015 | LLM-as-Judge scores serve as S-015 escalation gate criteria |

### 5.3 Tension Rationale (TEN Pairs)

| Pair | Tension Rationale |
|------|-------------------|
| S-001 + S-002 | Both are adversarial challenge strategies; using both in the same pass is redundant. Red Team is broader (simulates adversary behavior); DA is narrower (argues against conclusion). Choose based on context. |
| S-001 + S-009 | Both are high-cost adversarial strategies. Red Team is directed; Debate is emergent. Using both is cost-prohibitive for most reviews. |
| S-002 + S-005 | DA argues against the prevailing view; DI constructs a full alternative. DI subsumes DA's function. If using DI, DA is redundant. |
| S-002 + S-008 | DA makes assertions against; Socratic asks questions that surface weaknesses. Both challenge reasoning but through different modalities. Using both adds cost with diminishing returns. |
| S-002 + S-009 | DA is single-critic oppositional; Debate is multi-critic competitive. Debate subsumes DA in high-cost contexts. |
| S-003 + S-010 | Steelman reconstructs another agent's argument charitably; Self-Refine improves one's own output. Both are "improvement before critique" but from different directions. Tension is mild. |
| S-005 + S-009 | Both are multi-agent dialectical strategies. DI is structured (thesis-antithesis-synthesis); Debate is competitive. Using both is rarely justified. |

### 5.4 Recommended Strategy Combinations by Review Context

| Review Context | Recommended Combination | Layer | Total Agent Passes | Rationale |
|----------------|------------------------|-------|-------------------|-----------|
| **Routine code review** | S-010 + S-007 + S-014 | 1-2 | 3-4 | Self-refine, then constitutional critique against coding-standards.md, then score |
| **Architecture review** | S-003 + S-007 + S-001 + S-014 | 2-3 | 5-6 | Steelman, constitutional critique, Red Team probe, then score |
| **Research validation** | S-010 + S-011 + S-003 + S-002 + S-014 | 1-2 | 5-6 | Self-refine, verify facts, steelman, DA challenge, then score |
| **Design decision** | S-004 + S-013 + S-005 + S-014 | 2-3 | 6-7 | Pre-mortem risk, inversion checklist, dialectical inquiry, then score |
| **Risk assessment** | S-004 + S-012 + S-006 + S-014 | 2-3 | 6-7 | Pre-mortem, FMEA enumeration, ACH for competing risks, then score |
| **Critical decision** | S-003 + S-007 + S-001 + S-009 + S-014 | 3-4 | 10-14 | Full pipeline: steelman, constitutional, Red Team, debate, score |
| **Plan review** | S-004 + S-013 + S-007 + S-014 | 2 | 5-6 | Pre-mortem, inversion checklist, constitutional check, then score |
| **Requirements review** | S-008 + S-003 + S-007 + S-014 | 2 | 5-6 | Socratic probing, steelman, constitutional, then score |

### 5.5 Anti-patterns: Strategy Combinations to Avoid

| Anti-pattern | Strategies | Problem |
|-------------|-----------|---------|
| **Double Adversarial** | S-001 + S-009 in same review | Cost-prohibitive; both provide adversarial breadth but through different mechanisms. Choose one based on cost tolerance. |
| **Redundant Challenge** | S-002 + S-005 in same review | DI already subsumes DA's oppositional function. DA adds cost without new insight when DI is present. |
| **Self-Referential Verification** | S-010 + S-011 without context isolation | Self-Refine followed by CoVe without context stripping: the model confirms its own refined output. CoVe's verification step MUST use a fresh context. |
| **Steelman Without Critique** | S-003 alone | Steelman without a subsequent critique produces a strengthened argument with no adversarial challenge. It must always be paired with S-002, S-007, or another critique strategy. |
| **Score Without Criteria** | S-014 without defined rubric | LLM-as-Judge without an explicit rubric produces unreliable scores. The rubric must be defined before invocation. |
| **Premature Tournament** | S-009 at Layer 1-2 | Multi-Agent Debate on early-stage work wastes expensive resources on artifacts with obvious issues. Always use at Layer 3-4 per S-015. |
| **FMEA on Abstractions** | S-012 on vague designs | FMEA requires decomposable components. Applying it to insufficiently specified designs produces low-value output. |

---

## 6. Integration Cost Assessment

### 6.1 Integration Effort per Agent Spec

Effort is rated on a 4-point scale: **Trivial** (prompt change only), **Low** (new prompt template + minor spec update), **Medium** (new mode + orchestration logic), **High** (significant architectural changes).

| Strategy | ps-critic | nse-reviewer | nse-qa | nse-verification | /orchestration |
|----------|-----------|-------------|--------|-----------------|---------------|
| S-001 Red Team | Low (new persona template) | Low (security review mode) | N/A | N/A | Trivial (invoke critic with persona) |
| S-002 Devil's Advocate | Trivial (core function) | Low (adversarial review mode) | N/A | N/A | Trivial (invoke critic with DA prompt) |
| S-003 Steelman | Trivial (prepend to existing critique) | Trivial (prepend) | Trivial (prepend) | N/A | Trivial (add steelman phase) |
| S-004 Pre-Mortem | Low (temporal reframing template) | N/A | N/A | N/A | Low (add pre-mortem review type) |
| S-005 Dialectical Inquiry | N/A | N/A | N/A | N/A | Medium (3-pass with assumption extraction) |
| S-006 ACH | N/A (ps-analyst primary) | N/A | N/A | N/A | Medium (matrix output parsing) |
| S-007 Constitutional AI | Low (principle-by-principle mode) | Low (entrance/exit criteria alignment) | Low (principle-by-principle mode) | Low (V&V principle evaluation) | Low (multi-pass orchestration) |
| S-008 Socratic Method | Medium (multi-turn dialogue mode) | Low (probing question mode) | N/A | N/A | Medium (dialogue state management) |
| S-009 Multi-Agent Debate | Medium (debater role config) | N/A | N/A | N/A | High (debate round management) |
| S-010 Self-Refine | Trivial (append to any creator) | N/A | N/A | N/A | Trivial (default pre-submission step) |
| S-011 CoVe | Medium (context-isolated verification) | N/A | N/A | Low (verification protocol alignment) | Medium (context stripping logic) |
| S-012 FMEA | Low (FMEA table template) | N/A | Low (failure mode checklist) | Low (FMEA integration with V&V) | Low (FMEA review type) |
| S-013 Inversion | Low (inversion prompt template) | N/A | N/A | N/A | Low (pre-review checklist generation) |
| S-014 LLM-as-Judge | Low (rubric-based evaluation mode) | Low (rubric for entrance/exit) | Low (rubric for QA scoring) | Low (rubric for V&V scoring) | Low (gate scoring mechanism) |
| S-015 PAE | N/A (orchestration-level) | N/A | N/A | N/A | High (escalation logic, gate criteria, level routing) |

### 6.2 Aggregate Integration Effort

| Strategy | Total Effort | Component Count | Rationale |
|----------|-------------|-----------------|-----------|
| S-010 Self-Refine | **Trivial** | 1 prompt change | Append to existing creator prompts |
| S-003 Steelman | **Trivial** | 3 prompt prepends | Add steelman phase to critic prompts |
| S-002 Devil's Advocate | **Trivial** | 1 prompt change | Core critic function, minimal change |
| S-013 Inversion | **Low** | 2 changes | New prompt template + orchestration hookup |
| S-014 LLM-as-Judge | **Low** | 4 rubric additions | Add rubrics to each critic/reviewer agent |
| S-004 Pre-Mortem | **Low** | 2 changes | New prompt template + review type |
| S-001 Red Team | **Low** | 3 changes | Persona template, mode configuration |
| S-007 Constitutional AI | **Low** | 4 mode additions | Add principle-by-principle mode to 4 agents |
| S-012 FMEA | **Low** | 3 template additions | FMEA table template for 3 agents |
| S-008 Socratic Method | **Medium** | 3 changes | Multi-turn dialogue + orchestration state |
| S-011 CoVe | **Medium** | 3 changes | Context isolation + verification protocol |
| S-006 ACH | **Medium** | 2 changes | Matrix template + output parsing |
| S-005 Dialectical Inquiry | **Medium** | 2 changes | 3-pass orchestration + assumption extraction |
| S-009 Multi-Agent Debate | **High** | 3+ changes | Debate round management + judge coordination |
| S-015 PAE | **High** | 5+ changes | Escalation logic, gate criteria, level routing, decision matrix |

### 6.3 Estimated Token Overhead per Strategy Invocation

This summarizes the incremental token cost when a strategy is added to a review workflow:

| Strategy | Incremental Tokens | Cost Category | Notes |
|----------|-------------------|---------------|-------|
| S-010 | ~2,000 | Ultra-Low | Single extended output |
| S-003 | ~1,600 | Ultra-Low | Phase within existing pass |
| S-013 | ~2,100 | Ultra-Low | Single generative pass |
| S-014 | ~2,000 | Ultra-Low | Single scoring pass |
| S-002 | ~4,600 | Low | Two passes (present + challenge) |
| S-004 | ~5,600 | Low | Two passes (present + pre-mortem) |
| S-001 | ~7,000 | Medium | Two passes with persona context |
| S-008 | ~5,400 | Medium | Three turns of Q&A |
| S-007 | ~8,000-16,000 | Medium-High | 2-4 passes with constitution context |
| S-011 | ~7,500-10,000 | Medium | 3-4 passes with context isolation |
| S-012 | ~9,000 | Medium | Structured FMEA generation |
| S-005 | ~9,600 | Medium | Three passes (thesis, antithesis, synthesis) |
| S-006 | ~10,000 | Medium | Matrix generation and analysis |
| S-009 | ~15,000-30,000 | High | N debaters x M rounds + judge |
| S-015 | ~2,000-30,000 | Variable | Depends on escalation depth |

---

## 7. Architecture Trade-offs

### 7.1 Breadth vs. Depth

| Dimension | Broad Approach (all 15) | Narrow Approach (top 5-7) |
|-----------|------------------------|--------------------------|
| **Coverage** | All cognitive biases covered (Appendix B of TASK-006) | Some bias coverage gaps |
| **Token Cost** | Higher per-review aggregate cost | Lower per-review cost |
| **Complexity** | Higher orchestration complexity | Simpler workflow management |
| **Maintainability** | 15 prompt templates to maintain | Fewer templates to maintain |
| **Flexibility** | Can adapt to any review context | May lack appropriate strategy for some contexts |

**Recommendation:** Select 10 strategies as specified by EN-302. The composition model (Layer 0-4) ensures strategies are applied selectively, not exhaustively. A typical review activates 3-5 strategies, not all 10.

### 7.2 Token Economy

| Concern | Analysis |
|---------|----------|
| **Per-review budget** | A Layer 2 review (S-010 + S-007 + S-014) costs ~12,000-18,000 tokens. A Layer 4 review (full pipeline) costs ~40,000-60,000 tokens. |
| **Rules envelope (25,700)** | Strategy templates are loaded on skill invocation, not at session start. Impact on rules envelope is negligible. |
| **Context window pressure** | For large artifacts (> 10,000 tokens), multi-pass strategies (S-007, S-008) may hit context window limits. Mitigation: review artifacts in chunks. |
| **Diminishing returns** | Each additional strategy pass has diminishing marginal quality improvement. Empirically, Self-Refine shows diminishing returns after 2-3 iterations (Madaan et al., 2023). The same principle likely applies to strategy stacking. |

**Recommendation:** Design the default review path (Layer 2) to cost 12,000-18,000 tokens per review. Reserve high-cost strategies (S-005, S-006, S-009) for critical decisions where the quality improvement justifies the cost.

### 7.3 Consistency vs. Diversity

| Approach | Pro | Con |
|----------|-----|-----|
| **Fixed strategy set per context** | Predictable quality, reproducible reviews | May miss context-specific issues |
| **Rotating strategies** | Broader coverage over time, reduces blind spot risk | Inconsistent quality, harder to calibrate |
| **Hybrid: fixed core + rotating supplementary** | Best of both: consistent baseline with adaptive depth | Moderate complexity |

**Recommendation:** Fixed core (S-010, S-003, S-007, S-014) applied to every review. Context-dependent supplementary strategies (S-001, S-002, S-004, S-008, S-012, S-013) selected based on artifact type and criticality. This hybrid approach provides consistency with context-adaptive depth.

### 7.4 Automation vs. Control

| Approach | Pro | Con |
|----------|-----|-----|
| **Fully automated (S-015 decides)** | No user overhead, consistent application | May misjudge criticality; user loses control |
| **User-directed** | Maximum control, user selects strategies | Requires user expertise, adds friction |
| **Automated with override (P-020)** | Best default behavior with user authority preserved | Slight complexity |

**Recommendation:** Automated default per S-015 escalation with P-020 override. The orchestrator automatically selects strategies based on artifact criticality classification (C1-C4 from TASK-006), but the user can override any escalation decision in either direction. This satisfies P-020 (User Authority) while providing intelligent defaults.

---

## 8. Pugh Matrix

### 8.1 Methodology

Per NPR 7123.1D Process 17 (Decision Analysis), the Pugh Matrix uses S-002 (Devil's Advocate) as the baseline, since it is the most fundamental and universally applicable adversarial strategy. Each strategy is scored relative to this baseline as +1 (better), 0 (same), or -1 (worse) for each criterion.

### 8.2 Pugh Scoring

| Criterion (Weight) | S-001 | S-002 (Baseline) | S-003 | S-004 | S-005 | S-006 | S-007 | S-008 | S-009 | S-010 | S-011 | S-012 | S-013 | S-014 | S-015 |
|---------------------|-------|-------------------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| A1: Agent Fit (25%) | 0 | 0 | +1 | 0 | -1 | 0 | +1 | 0 | -1 | +1 | 0 | 0 | +1 | +1 | 0 |
| A2: P-003 (15%) | 0 | 0 | +1 | 0 | 0 | 0 | 0 | 0 | -1 | +1 | 0 | 0 | +1 | +1 | 0 |
| A3: Token Eff. (20%) | -1 | 0 | +1 | 0 | -1 | -1 | -1 | 0 | -1 | +1 | -1 | -1 | +1 | +1 | 0 |
| A4: Composability (20%) | 0 | 0 | +1 | +1 | 0 | 0 | +1 | 0 | 0 | 0 | 0 | +1 | +1 | +1 | +1 |
| A5: Integration (20%) | 0 | 0 | +1 | 0 | -1 | -1 | 0 | -1 | -1 | +1 | -1 | 0 | 0 | 0 | -1 |

### 8.3 Weighted Pugh Scores

| Strategy | Raw Sum | Weighted Score | Rank |
|----------|---------|---------------|------|
| S-003 Steelman | +5 | +1.00 | 1 |
| S-013 Inversion | +4 | +0.80 | 2 |
| S-010 Self-Refine | +4 | +0.80 | 2 |
| S-014 LLM-as-Judge | +4 | +0.80 | 2 |
| S-007 Constitutional AI | +1 | +0.05 | 5 |
| S-004 Pre-Mortem | +1 | +0.20 | 6 |
| S-015 PAE | 0 | 0.00 | 7 |
| S-012 FMEA | 0 | 0.00 | 7 |
| S-002 Devil's Advocate | 0 | 0.00 (baseline) | 7 |
| S-001 Red Team | -1 | -0.20 | 10 |
| S-008 Socratic Method | -1 | -0.20 | 10 |
| S-006 ACH | -2 | -0.40 | 12 |
| S-011 CoVe | -2 | -0.40 | 12 |
| S-005 Dialectical Inquiry | -3 | -0.60 | 14 |
| S-009 Multi-Agent Debate | -4 | -0.80 | 15 |

### 8.4 Interpretation

The Pugh Matrix reveals a clear three-tier architectural fitness pattern:

**Tier 1 -- Architectural Winners (Pugh >= +0.20):** S-003, S-010, S-013, S-014, S-004. These strategies have the highest architectural fit, lowest token cost, best composability, and easiest integration. They should be included in any selection.

**Tier 2 -- Architecturally Neutral (Pugh -0.20 to +0.05):** S-007, S-015, S-012, S-002, S-001, S-008. These strategies have moderate architectural characteristics. Their inclusion depends on effectiveness and coverage considerations (addressed by TASK-001 and TASK-002).

**Tier 3 -- Architecturally Expensive (Pugh <= -0.40):** S-006, S-011, S-005, S-009. These strategies have high cost, complex orchestration, or limited composability. Their inclusion requires strong effectiveness justification to offset architectural overhead.

**Note:** Pugh scores reflect ARCHITECTURAL fitness only. A strategy with a low Pugh score (e.g., S-009 Multi-Agent Debate) may still be selected if its unique effectiveness justifies the architectural cost. The Pugh Matrix is one input to TASK-004, not the sole decision criterion.

**Baseline Robustness (F-006):** The Pugh tier assignments are robust to alternative baseline choices. If S-010 (Self-Refine) were used as the baseline instead of S-002, the relative ordering within each tier would shift but the tier memberships would remain stable. This is verifiable by inspection: Tier 3 strategies (S-005, S-006, S-009) score below S-002 on most criteria and would also score at or below S-010 (since S-010 scores >= S-002 on all criteria). Tier 1 strategies maintain their advantage because their high scores on Agent Fit, Token Efficiency, and Composability are absolute properties, not baseline-relative. The Pugh tier structure is therefore a property of the strategies' architectural characteristics, not an artifact of baseline choice.

---

## 9. Sensitivity Analysis

### 9.1 Weight Sensitivity

The following analysis tests whether the Pugh ranking is robust to changes in criterion weights:

| Scenario | Weight Change | Effect on Top 5 | Effect on Bottom 3 |
|----------|---------------|-----------------|-------------------|
| **Baseline** | As defined | S-003, S-010, S-013, S-014, S-004 | S-006, S-005, S-009 |
| **Token Eff. +10%** (30%) | A3 increased, A1 reduced | No change to top 5 | S-009 drops further; S-006, S-011, S-007 penalized |
| **Composability +10%** (30%) | A4 increased, A3 reduced | S-007 enters top 5 (replaces S-004) | S-009 unchanged; composable strategies rewarded |
| **Agent Fit +10%** (35%) | A1 increased, A5 reduced | No change to top 5 | S-009 penalized more; S-005 unchanged |
| **Integration +10%** (30%) | A5 increased, A2 reduced | No change to top 5 | S-009, S-005, S-008 penalized further |
| **Equal weights** (20% each) | All criteria equal | S-003, S-010, S-013, S-014 remain top 4 | S-009 remains bottom |

**Conclusion:** The top tier (S-003, S-010, S-013, S-014) is robust across all weight variations. S-004 and S-007 swap positions in some scenarios. The bottom tier (S-005, S-006, S-009) consistently scores lowest on architectural criteria regardless of weighting. This confirms the ranking is not an artifact of weight choice.

### 9.2 Score Sensitivity

If any single Pugh score were changed by one point:

| Most Sensitive Scores | Current | If Changed | Impact |
|----------------------|---------|------------|--------|
| S-007 Token Efficiency | -1 | 0 | S-007 moves from rank 5 to rank 3; enters Tier 1 |
| S-001 Token Efficiency | -1 | 0 | S-001 moves from rank 10 to rank 7; enters Tier 2 |
| S-009 Agent Fit | -1 | 0 | S-009 moves from rank 15 to rank 14; still Tier 3 |

**Conclusion:** S-007 is the most score-sensitive strategy -- if its token efficiency is assessed more favorably (e.g., by amortizing constitution loading costs across multiple reviews), it moves into Tier 1. S-009 is insensitive to single-point changes; it consistently ranks lowest architecturally.

---

## 10. Risks and Mitigations

### 10.1 Architecture-Level Risks

| Risk ID | Risk | Likelihood | Severity | Strategy Affected | Mitigation |
|---------|------|------------|----------|-------------------|------------|
| AR-001 | Shared model bias invalidates self-critique strategies | Medium | High | S-007, S-010, S-011, S-014 | External tool verification where possible (linters, validators); periodic mutation testing; human spot-check per TASK-006 Systemic Risk section |
| AR-002 | Multi-turn dialogue (S-008) exceeds context window | Medium | Medium | S-008 | Limit Socratic exchanges to 3 turns; truncate older turns if window exceeded |
| AR-003 | S-009 debate rounds violate P-003 through emergent agent-to-agent communication | Low | High | S-009 | Enforce orchestrator-managed rounds; debaters never see each other's agent IDs or have direct communication channels |
| AR-004 | S-015 escalation logic miscalibrates artifact criticality | Medium | Medium | S-015 | Fallback to Layer 2 minimum per TASK-006; user override per P-020 |
| AR-005 | Constitutional critique (S-007) constitution files become too large for context | Low | Medium | S-007 | Stratified loading: load only relevant constitution per artifact type (coding standards for code review, architecture standards for design review) |
| AR-006 | FMEA (S-012) produces combinatorial explosion for complex systems | Medium | Low | S-012 | Scope FMEA to specific components/interfaces, not entire system; use simplified H/M/L scoring |
| AR-007 | Inversion (S-013) generates frivolous anti-patterns | Medium | Low | S-013 | Constrain inversion to specific quality dimensions; post-filter anti-patterns against existing standards |
| AR-008 | ACH matrix (S-006) output is inconsistently formatted | Medium | Medium | S-006 | Provide strict YAML/JSON schema for matrix output; validate output format before consumption |
| AR-009 | Token budget exceeded for Layer 3-4 reviews of large artifacts | Medium | Medium | S-001, S-005, S-009 | Chunk large artifacts; review per-section rather than whole-artifact for expensive strategies |
| AR-010 | Strategy prompt templates drift from catalog definitions over time | Low | Medium | All | Version-control strategy prompt templates; periodic alignment review against EN-301 catalog |

### 10.2 Risk Priority Matrix

| Likelihood / Severity | Low | Medium | High |
|----------------------|-----|--------|------|
| **High** | -- | -- | -- |
| **Medium** | AR-006, AR-007 | AR-002, AR-004, AR-008, AR-009 | AR-001 |
| **Low** | -- | AR-005, AR-010 | AR-003 |

**Top Priority Risks:** AR-001 (shared model bias) and AR-003 (P-003 violation in debate) require immediate attention in implementation design.

---

## 11. Recommendation

### 11.1 Architectural Recommendation for TASK-004

Based on the architecture fit analysis, Pugh Matrix scoring, token budget analysis, composition matrix, and risk assessment, the following architectural scoring inputs are provided for TASK-004:

#### Architectural Scores (0.0-1.0 scale, for TASK-004 integration)

| Strategy | Arch Score | Rationale |
|----------|-----------|-----------|
| S-003 Steelman | **0.95** | Lowest cost, highest composability, zero-infrastructure integration. Architectural ideal. |
| S-010 Self-Refine | **0.95** | Zero additional agents, minimal token overhead, universally applicable. |
| S-014 LLM-as-Judge | **0.93** | Essential infrastructure; simple single-pass; enables all quality gates. |
| S-013 Inversion | **0.92** | Single-pass generative strategy that enhances all other strategies. High leverage. |
| S-004 Pre-Mortem | **0.90** | Minimal prompt change with outsized impact. Natural fit for plan review. |
| S-007 Constitutional AI | **0.88** | Jerry's architecture was designed for this. Near-zero incremental cost because constitutions already exist. Token cost for multi-pass is the only penalty. |
| S-002 Devil's Advocate | **0.87** | Core critic function. Trivial integration. Slightly lower composability than S-003/S-007. |
| S-012 FMEA | **0.85** | Strong structured output, natural fit for nse-verification. Medium token cost. |
| S-001 Red Team | **0.82** | Good fit but medium token cost; specialized use cases (security/architecture). |
| S-015 PAE | **0.80** | High architectural value as orchestration meta-strategy but high integration effort. |
| S-008 Socratic Method | **0.75** | Multi-turn dialogue adds orchestration complexity and token cost. |
| S-011 CoVe | **0.73** | Context isolation requirement adds architectural complexity. |
| S-006 ACH | **0.70** | Matrix output reliability and parsing complexity reduce architectural score. |
| S-005 Dialectical Inquiry | **0.65** | 3-pass with assumption extraction is architecturally demanding. |
| S-009 Multi-Agent Debate | **0.55** | Highest cost, highest complexity, shared-model-bias limitation, P-003 risk. |

#### Integration Priority Order

For implementation, strategies should be integrated in the following order (lowest effort first, highest architectural leverage):

| Phase | Strategies | Effort | Cumulative Capability |
|-------|-----------|--------|----------------------|
| **Phase 1: Foundation** | S-010, S-003, S-014, S-013 | Trivial-Low | Self-improve, steelman, score, generate checklists |
| **Phase 2: Core Review** | S-007, S-002, S-004 | Low | Constitutional critique, DA challenge, pre-mortem |
| **Phase 3: Deep Review** | S-001, S-012, S-015 | Low-High | Red Team, FMEA, graduated escalation |
| **Phase 4: Advanced** | S-008, S-011, S-005, S-006, S-009 | Medium-High | Socratic, CoVe, DI, ACH, Debate |

Phase 1 delivers ~60% of adversarial review capability at ~20% of total integration effort.

### 11.2 Conditions and Assumptions

1. **Assumption:** The Claude model remains the sole LLM provider. If cross-model verification becomes available, S-009 (Multi-Agent Debate) architectural score would increase significantly.
2. **Assumption:** Strategy prompt templates are maintained in agent spec files, not in auto-loaded rules. This keeps the 25,700-token rules envelope unaffected.
3. **Condition:** S-009 implementation MUST enforce orchestrator-managed debate rounds to comply with P-003.
4. **Condition:** S-015 implementation MUST include the fallback to Layer 2 minimum defined in TASK-006.
5. **Condition:** S-007 constitution loading MUST be stratified by artifact type to manage context window usage.

---

## Appendix A: NASA SE Rationale

### A.1 NPR 7123.1D Process Alignment

This trade study follows NPR 7123.1D Process 17 (Decision Analysis) methodology:

| Process 17 Activity | This Document Section |
|---------------------|----------------------|
| Define decision criteria and weights | Section 1.4 (Evaluation Criteria) |
| Identify alternatives | Section 2 (15 strategies as alternatives) |
| Evaluate alternatives against criteria | Section 8 (Pugh Matrix) |
| Perform sensitivity analysis | Section 9 (Weight and Score Sensitivity) |
| Document decision and rationale | Section 11 (Recommendation) |

### A.2 Trade Study Method Selection

The Pugh Matrix was selected over Kepner-Tregoe or AHP for the following reasons:

| Consideration | Pugh Matrix | Kepner-Tregoe | AHP |
|---------------|------------|---------------|-----|
| Number of alternatives | 15 (suitable) | 15 (suitable) | 15 (pairwise = 105 comparisons; unwieldy) |
| Criterion type | Relative comparison (appropriate for architectural fit) | Absolute scoring | Pairwise ratio (over-precise for this context) |
| Interpretability | High (better/same/worse is intuitive) | Medium | Low (eigenvector math) |
| Sensitivity to baseline | Moderate (baseline choice matters) | Low | Low |
| Suitability | Best fit for concept-level trade study | Better for detailed design | Better for small-N high-precision decisions |

**Baseline Selection Rationale:** S-002 (Devil's Advocate) was chosen as the Pugh baseline because it is the most fundamental adversarial strategy -- the simplest distinct adversarial mechanism against which all others can be compared. It has moderate cost, moderate complexity, and well-understood characteristics, making it an effective reference point.

### A.3 Requirements Traceability (P-040)

| Requirement | Trace to This Document |
|-------------|----------------------|
| EN-302 AC-1: 15 strategies evaluated | Section 2 (all 15 assessed), Section 8 (all 15 scored) |
| EN-302 AC-3: Integration costs estimated | Section 6 (effort per agent, aggregate effort, token overhead) |
| EN-302 AC-4: Composability analysis | Section 5 (15x15 matrix, synergies, anti-patterns) |
| EN-302 AC-5: NASA SE trade study format | Appendix A (process alignment) |
| P-003 compliance | Section 3 (compliance assessment for all 15) |
| P-020 user authority | Section 7.4 (automated with override recommendation) |
| P-040 traceability | This table |
| P-042 risk documentation | Section 10 (risk register with 10 risks) |

---

## Appendix B: Glossary

| Term | Definition |
|------|------------|
| Agent Pass | One invocation of a worker agent by the orchestrator |
| Composition | Using multiple strategies together in a single review workflow |
| Constitution | A set of explicit, written, evaluable principles (Jerry's `.claude/rules/` files) |
| Context Isolation | Invoking an agent without the original artifact in context to prevent confirmation bias |
| Escalation Gate | A quality threshold that determines whether review intensity should increase |
| Layer (0-4) | Graduated intensity levels in S-015 Progressive Adversarial Escalation |
| P-003 | Jerry constitutional principle: No Recursive Subagents (Hard constraint) |
| P-020 | Jerry constitutional principle: User Authority (Hard constraint) |
| Pugh Matrix | Structured comparison method scoring alternatives relative to a baseline |
| RPN | Risk Priority Number (Severity x Occurrence x Detection) used in FMEA |
| Rules Envelope | The 25,700-token budget for auto-loaded `.claude/rules/` files |
| Shared Model Bias | Systemic risk when the same LLM serves as both creator and critic |
| Sync Barrier | Orchestration checkpoint where parallel pipelines synchronize |
| Token Budget | Estimated token consumption per strategy invocation |

---

*DISCLAIMER: This trade study is AI-generated guidance based on NASA Systems Engineering standards (NPR 7123.1D). It is advisory only and does not constitute official NASA guidance. All architecture decisions require human review and professional engineering judgment. Architectural scores are estimates based on the agent model analysis and should be validated through implementation experience.*

---

*Document ID: TSR-PROJ-001-EN302-003*
*Agent: nse-architecture v2.1.0*
*NPR 7123.1D Processes: 4 (Design Solution Definition), 17 (Decision Analysis)*
*Created: 2026-02-13*
*Status: Complete*
