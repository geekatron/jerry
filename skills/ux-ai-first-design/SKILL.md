---
name: ux-ai-first-design
description: "AI-first interaction design sub-skill (CONDITIONAL) for the /user-experience parent skill. Provides trust-calibrated AI interaction design guidance using Yang et al.'s trust-risk and error-risk classification framework. Produces interaction pattern recommendations, trust calibration assessments, feedback loop designs, and progressive disclosure strategies for AI-powered features. CONDITIONAL: requires WSM >= 7.80 AND enabler research (FEAT-020) complete; otherwise routes to /ux-heuristic-eval with PAIR protocol. Invoke when teams need to design AI-powered interactions, calibrate user trust in AI outputs, classify AI error risks, design human-AI handoff patterns, or audit existing AI interfaces for trust and safety. Triggers: AI-first design, AI interaction, trust calibration, AI UX, conversational UX, AI interface, LLM interface, agentic UX, human-AI interaction, AI transparency, AI error handling, AI onboarding, progressive AI disclosure, trust-risk, error-risk."
version: "1.1.0"
agents:
  - ux-ai-design-guide
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
activation-keywords:
  - "AI-first design"
  - "AI interaction"
  - "trust calibration"
  - "AI UX"
  - "conversational UX"
  - "AI interface"
  - "LLM interface"
  - "agentic UX"
  - "human-AI interaction"
  - "AI transparency"
  - "AI error handling"
  - "AI onboarding"
  - "progressive AI disclosure"
  - "trust-risk"
  - "error-risk"
---

<!-- VERSION: 1.1.0 | DATE: 2026-03-04 | SOURCE: skills/user-experience/SKILL.md | PARENT: /user-experience skill | REVISION: iter5 — version comment alignment; iter4: applied iter3 defect fixes (Shneiderman DOI correction to IJHCI 10.1080/10447318.2020.1741118, Stage 5 operational criterion, classification tie-breaker rules), added WSM file path pointer to wave-progression.md, explicit default-case rules for classification algorithms; iter3: version 1.0.0→1.1.0, error-rate threshold brackets, progressive disclosure calibration footnote, confidence:0.5 explanatory comment -->

# AI-First Design Sub-Skill

> **Version:** 1.1.0
> **Framework:** Jerry User-Experience -- AI-First Interaction Design
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Parent Skill:** `/user-experience` (`skills/user-experience/SKILL.md`)
> **Wave:** 5 (Process Intensives) -- CONDITIONAL
> **Project:** PROJ-022 User Experience Skill | GitHub Issue [#138](https://github.com/geekatron/jerry/issues/138)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Document Audience](#document-audience-triple-lens) | Triple-Lens audience guide |
| [Purpose](#purpose) | Sub-skill overview and key capabilities |
| [When to Use This Sub-Skill](#when-to-use-this-sub-skill) | Activation triggers, scope boundaries, and CONDITIONAL activation note |
| [Available Agents](#available-agents) | Single agent with role, model, and output location |
| [P-003 Compliance](#p-003-compliance) | Worker agent hierarchy position |
| [Invoking the Agent](#invoking-the-agent) | Invocation via ux-orchestrator with conditional activation check |
| [Methodology](#methodology) | AI-first interaction design process with trust-risk/error-risk classification |
| [Output Specification](#output-specification) | Output location, L0/L1/L2 structure, required sections |
| [Routing](#routing) | Keywords and lifecycle-stage routing integration |
| [Cross-Framework Integration](#cross-framework-integration) | Handoff from heuristic eval, handoff to inclusive design for AI accessibility |
| [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence) | Confidence classifications for AI-First Design outputs |
| [Quality Gate Integration](#quality-gate-integration) | S-014 scoring and H-13 threshold enforcement |
| [Degraded Mode Behavior](#degraded-mode-behavior) | Operation without Figma MCP |
| [Wave Architecture](#wave-architecture) | Wave 5 entry criteria, CONDITIONAL activation, bypass |
| [Constitutional Compliance](#constitutional-compliance) | Governing principles including P-022 AI pattern staleness disclosure |
| [Registration](#registration) | H-26 parent-routed registration model and AGENTS.md confirmation |
| [Deployment Status](#deployment-status) | Wave 5 stub agent status and implementation timeline |
| [Quick Reference](#quick-reference) | Common workflows and agent selection hints |
| [References](#references) | Full repo-relative paths, requirements traceability, external citations |

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Product managers, designers | [Purpose](#purpose), [When to Use This Sub-Skill](#when-to-use-this-sub-skill), [Quick Reference](#quick-reference) |
| **L1 (Developer)** | Engineers invoking the agent | [Invoking the Agent](#invoking-the-agent), [Methodology](#methodology), [Output Specification](#output-specification) |
| **L2 (Architect)** | Workflow designers, skill maintainers | [Cross-Framework Integration](#cross-framework-integration), [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence), [Degraded Mode Behavior](#degraded-mode-behavior), [Wave Architecture](#wave-architecture) |

---

## Purpose

The AI-First Design sub-skill provides structured AI interaction design guidance using trust-calibrated pattern selection based on Yang et al.'s (2020) two primary failure modes in human-AI interaction: trust miscalibration and error cost mismanagement. It targets tiny teams (1-5 people) building AI-powered features who need a systematic framework to design interactions that appropriately calibrate user trust, manage AI error consequences, and progressively disclose AI capabilities.

This sub-skill is part of Wave 5 (Process Intensives) and is **CONDITIONAL** -- it only activates when WSM >= 7.80 AND enabler research (FEAT-020) is complete. When the condition is not met, the `ux-orchestrator` routes to `/ux-heuristic-eval` with PAIR protocol (AI-specific heuristic supplement) as an interim alternative.

The sub-skill bridges behavioral diagnosis (Wave 4) and full AI product maturity by providing interaction design guidance that accounts for the unique challenges of AI-powered interfaces: non-deterministic outputs, confidence-dependent reliability, and the need for graceful degradation when AI predictions are wrong.

### Key Capabilities

- **Trust-Risk Classification** -- Assesses how much users should trust AI outputs across a three-level scale (HIGH: AI makes decisions autonomously, MEDIUM: AI recommends with human decision, LOW: AI assists with human control), based on Yang et al.'s (2020) trust miscalibration failure mode
- **Error-Risk Classification** -- Evaluates the cost of AI errors across a three-level scale (HIGH: irreversible or safety-critical, MEDIUM: costly but recoverable, LOW: negligible impact), based on Yang et al.'s (2020) error cost mismanagement failure mode
- **Interaction Pattern Selection** -- Selects interaction patterns from the trust-risk x error-risk matrix, mapping each combination to an appropriate human-AI collaboration level (full human oversight, AI-as-advisor, human-in-the-loop, AI autonomous with monitoring, AI autonomous)
- **Feedback Loop Design** -- Designs how the AI system communicates uncertainty, explains decisions, handles errors gracefully, and enables user correction, following Amershi et al.'s (2019) 18 guidelines for human-AI interaction
- **Progressive Disclosure of AI Capabilities** -- Designs graduated onboarding experiences that build user trust over time, starting with low-stakes AI features and progressively revealing higher-autonomy capabilities as trust is established (Shneiderman, 2020)
- **AI Transparency Assessment** -- Evaluates current AI interface transparency against the Google PAIR (2019) guidebook patterns, identifying where explainability gaps erode user trust or where excessive explanation creates cognitive overload

---

## When to Use This Sub-Skill

**CONDITIONAL ACTIVATION:** This sub-skill only activates when WSM >= 7.80 AND enabler research (FEAT-020) is complete. If either condition is unmet, the `ux-orchestrator` routes to `/ux-heuristic-eval` with PAIR protocol (AI-specific heuristic supplement) as an interim alternative.

Activate when:

- Designing AI-powered features and needing to determine the appropriate level of user trust and human oversight
- Classifying AI interaction patterns by trust-risk and error-risk to select the right human-AI collaboration model
- Designing feedback loops for AI systems that communicate uncertainty, explain decisions, and handle errors gracefully
- Planning progressive disclosure strategies for AI capabilities that build user trust incrementally
- Auditing existing AI interfaces for trust calibration issues, transparency gaps, or inappropriate autonomy levels
- Designing conversational UX for LLM-powered features (chatbots, AI assistants, agentic interfaces)
- Evaluating whether an AI feature needs human-in-the-loop oversight vs. autonomous operation
- Designing error recovery flows specific to AI prediction failures or hallucination scenarios

Do NOT use for:

- Evaluating an existing non-AI interface against usability heuristics -- use `/ux-heuristic-eval` (Nielsen's 10) instead. For AI interfaces where the CONDITIONAL activation is not met, use `/ux-heuristic-eval` with PAIR protocol.
- Building or auditing a component library -- use `/ux-atomic-design` (Atomic Design) instead.
- Accessibility compliance auditing for AI interfaces -- use `/ux-inclusive-design` (WCAG 2.2) instead. AI-First Design identifies trust and interaction patterns; Inclusive Design audits accessibility compliance of the implemented patterns.
- Measuring quantitative UX health metrics for AI features -- use `/ux-heart-metrics` (Google GSM) instead.
- Understanding user motivations at the job level -- use `/ux-jtbd` (Jobs-to-Be-Done) instead.
- Diagnosing behavioral bottlenecks in AI feature adoption -- use `/ux-behavior-design` (Fogg B=MAP) instead. B=MAP diagnoses why users fail to adopt an AI feature; AI-First Design addresses how the AI interaction itself should be designed.
- Testing hypotheses about AI design changes -- use `/ux-lean-ux` (Lean UX) instead.
- Running a full rapid prototyping sprint -- use `/ux-design-sprint` (Design Sprint 2.0) instead.
- Prioritizing AI features by user satisfaction impact -- use `/ux-kano-model` (Kano) instead.
- Security-focused AI review or AI red-teaming -- use `/eng-team` or `/red-team` instead.
- General research without AI interaction focus -- use `/problem-solving` instead.

---

## Available Agents

| Agent | Role | Tier | Mode | Model | Output Location |
|-------|------|------|------|-------|-----------------|
| `ux-ai-design-guide` | AI-first interaction design specialist (CONDITIONAL) | T4 | Divergent | Opus | `skills/ux-ai-first-design/output/{engagement-id}/ux-ai-design-guide-{topic-slug}.md` |

**STUB:** The agent definition file (`skills/ux-ai-first-design/agents/ux-ai-design-guide.md`) is pending Wave 5 Phase 2 implementation as part of PROJ-022 EPIC-005. The SKILL.md specifies the methodology and output contract that the agent will implement.

**CONDITIONAL:** This agent only activates when WSM >= 7.80 AND enabler research (FEAT-020) is complete. The `ux-orchestrator` checks these conditions before routing to this sub-skill.

**Tool tier:** T4 (External) = Read, Write, Edit, Glob, Grep, Bash + WebSearch, WebFetch, Context7 MCP. T4 is required because AI design patterns evolve rapidly; WebSearch and Context7 provide access to current AI SDK documentation and interaction pattern libraries. See `.context/rules/agent-development-standards.md` [Tool Security Tiers].

The agent produces output at three levels per AD-M-004:
- **L0 (Executive Summary):** Trust-risk and error-risk classification; selected interaction pattern; top design recommendations; key findings for stakeholders and cross-framework synthesis input.
- **L1 (Technical Detail):** Full trust-risk x error-risk matrix analysis, interaction pattern specification, feedback loop design, transparency assessment, progressive disclosure plan, and detailed design recommendations with citations.
- **L2 (Strategic Implications):** AI interaction maturity assessment, trust calibration roadmap, AI capability progression strategy, and organizational readiness analysis for increased AI autonomy.

---

## P-003 Compliance

The `/ux-ai-first-design` sub-skill contains a single **worker** agent. It is invoked by the `ux-orchestrator` (T5) via the Agent tool. The agent does NOT have Agent tool access and MUST NOT spawn sub-agents.

```
MAIN CONTEXT (user request)
    |
    v
ux-orchestrator (T5, Opus, Integrative) -- parent orchestrator
    |
    +-- ux-ai-design-guide (T4, Divergent, Opus) -- THIS sub-skill's worker [COND]
    +-- [other sub-skill workers...]
```

**Enforcement:**
- `disallowedTools: [Agent]` declared in `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` frontmatter
- P-003 prohibition in `skills/ux-ai-first-design/agents/ux-ai-design-guide.governance.yaml` `capabilities.forbidden_actions`
- CI gate validates no sub-skill agent has Agent access (documented in `skills/user-experience/rules/ci-checks.md`)

---

## Invoking the Agent

This is a sub-skill invoked by the `ux-orchestrator`, not directly by users. Users interact with the parent `/user-experience` skill, which routes to this sub-skill based on lifecycle-stage triage.

**CONDITIONAL CHECK:** Before routing to this sub-skill, the `ux-orchestrator` verifies:
1. **WSM >= 7.80** -- The team's Wave Scorecard Metric meets the minimum threshold
2. **Enabler FEAT-020 complete** -- The AI interaction design enabler research is marked DONE

If either condition fails, the orchestrator routes to `/ux-heuristic-eval` with PAIR protocol (AI-specific heuristic supplement) as an interim alternative, informing the user: "AI-First Design requires WSM >= 7.80 and completed FEAT-020. Routing to Heuristic Evaluation with AI interaction supplement instead."

### Via Natural Language (to parent skill)

```
"Design the conversational UX for our AI assistant feature"
"How should we calibrate user trust in our AI recommendations?"
"Classify the trust-risk and error-risk for our AI-powered search"
"Audit our AI chatbot interface for transparency and trust issues"
"Design progressive AI disclosure for our new ML feature"
"What interaction pattern should we use for AI-generated content?"
```

### Via Explicit Agent Request (to parent skill)

```
"Use ux-ai-design-guide to design the AI interaction pattern for our recommendation engine"
"Have ux-ai-design-guide classify trust-risk and error-risk for the automated approval workflow"
```

### Via Agent Tool (orchestrator internal)

The `ux-orchestrator` invokes the agent via the Agent tool:

```python
Agent(
    description="ux-ai-design-guide: AI-first interaction design for recommendation engine",
    subagent_type="jerry:ux-ai-design-guide",
    prompt="""
## UX CONTEXT (REQUIRED)
- **Engagement ID:** UX-0001
- **Topic:** Recommendation Engine Interaction Design
- **Product:** [product name and domain]
- **Target Users:** [user description]
- **AI Capability:** [what the AI does -- e.g., generates recommendations, classifies content, automates decisions]
- **AI Technology:** [underlying technology -- e.g., LLM, classification model, recommendation system]
- **Current State:** [existing AI interface, if any; screenshots or descriptions]
- **Input:** [upstream heuristic findings, behavioral data, user research]

## TASK
Design the AI-first interaction pattern for the recommendation engine.
1. Classify trust-risk level (HIGH/MEDIUM/LOW)
2. Classify error-risk level (HIGH/MEDIUM/LOW)
3. Select interaction pattern from trust-risk x error-risk matrix
4. Design feedback loop (uncertainty communication, decision explanation, error recovery)
5. Design progressive disclosure strategy for AI capabilities
6. Assess transparency against PAIR guidelines

## MANDATORY PERSISTENCE (P-002)
Create file at: skills/ux-ai-first-design/output/UX-0001/ux-ai-design-guide-recommendation-engine.md
"""
)
```

> **Governance codification (AD-M-007):** The session_context contract (on_receive/on_send) is specified in `ux-ai-design-guide.governance.yaml` per AD-M-007. Fields are enumerated below:

**on_receive fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `engagement_id` | string | Yes | UX engagement identifier (format: `UX-{NNNN}`) |
| `product_context` | string | Yes | Product name, domain, and target user description |
| `ai_capability` | string | Yes | What the AI does (e.g., generates recommendations, classifies content, automates decisions) |
| `ai_technology` | string | No | Underlying technology (e.g., LLM, classification model, recommendation system) |
| `current_state` | string | No | Description of existing AI interface, if any |
| `upstream_artifacts` | array | No | File paths to upstream handoff artifacts (heuristic evaluation findings, behavioral data, user research) |

**on_send fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `trust_risk_level` | enum | Yes | Trust-risk classification: `HIGH`, `MEDIUM`, `LOW` |
| `error_risk_level` | enum | Yes | Error-risk classification: `HIGH`, `MEDIUM`, `LOW` |
| `interaction_pattern` | string | Yes | Selected interaction pattern from trust-risk x error-risk matrix |
| `ai_capability_type` | string | Yes | Category of AI capability under design (e.g., generative, classificatory, decisional) |
| `feedback_loop_design` | object | Yes | Uncertainty communication, decision explanation, error recovery mechanisms |
| `human_oversight_level` | enum | Yes | Required oversight: `full_oversight`, `advisory`, `human_in_loop`, `monitored_autonomous`, `autonomous` |
| `progressive_disclosure_plan` | object | Yes | Graduated onboarding stages with trust-building milestones |
| `synthesis_judgments` | array | Yes | AI judgment calls with confidence classification and rationale |

---

## Methodology

### AI-First Interaction Design Framework

The methodology centers on Yang et al.'s (2020) two primary failure modes in human-AI interaction: **trust miscalibration** (users trust AI too much or too little) and **error cost mismanagement** (AI errors cause disproportionate harm). These failure modes are addressed through a structured six-phase process that classifies risk, selects interaction patterns, and designs trust-building mechanisms.

This methodology draws on four complementary sources:
- **Yang et al. (2020):** Trust-risk and error-risk classification framework; the foundational insight that AI interaction design is "uniquely difficult" because of non-deterministic outputs and evolving capabilities
- **Amershi et al. (2019):** 18 guidelines for human-AI interaction, organized by interaction phase (initially, during, when wrong, over time)
- **Google PAIR (2019):** People + AI Guidebook with practical AI design patterns for transparency, explainability, and user control
- **Shneiderman (2020):** Human-centered AI framework emphasizing human control and automation balance

### Phase 1: AI Capability Assessment

**Purpose:** Establish the AI interaction context, characterize the AI capability, confirm CONDITIONAL activation criteria, and catalog available design evidence.

**Activities:**
1. Identify the product domain, target users, and the specific AI capability under design. Characterize the AI technology (LLM, classification, recommendation, decision automation, generative, etc.)
2. Confirm CONDITIONAL activation criteria: WSM >= 7.80 AND enabler FEAT-020 DONE. *(Verification: check FEAT-020 status in WORKTRACKER.md; check WSM in most recent wave signoff at `skills/user-experience/rules/wave-progression.md`. If either condition fails, halt and inform orchestrator to route to interim alternative.)*
3. Catalog upstream inputs: check for `/ux-heuristic-eval` findings related to AI interface issues; check for `/ux-behavior-design` bottleneck diagnoses related to AI feature adoption; import finding IDs for design context
4. Catalog available design evidence: user research on AI feature expectations, existing AI interface screenshots, competitive AI interface analysis, usage analytics for existing AI features
5. Characterize the AI system's behavioral properties: determinism level (deterministic, semi-deterministic, non-deterministic), confidence availability (does the AI system expose confidence scores?), failure modes (what happens when the AI is wrong?), and learning behavior (does the AI improve with use?)

**Output:** AI capability assessment brief with the following required fields:

| Field | Description | Example |
|-------|-------------|---------|
| Product Domain | Application area and target user segment | "E-commerce product search with AI-powered recommendations" |
| AI Capability | What the AI does | "Generates personalized product recommendations based on browsing history" |
| AI Technology | Underlying technology type | "Collaborative filtering + LLM-based explanation generation" |
| Determinism Level | How predictable the AI output is | "Non-deterministic: recommendations vary by session; explanations generated per-request" |
| Confidence Availability | Whether the system exposes confidence scores | "Yes: recommendation confidence (0.0-1.0); No: explanation quality not scored" |
| Failure Modes | What happens when the AI is wrong | "Irrelevant recommendations; nonsensical explanations; stale data recommendations" |
| Upstream Findings | Imported heuristic evaluation or behavior design findings | "HE-007 (severity 2): AI recommendations not explained" |
| CONDITIONAL Status | Activation criteria verification | "PASS: WSM = 8.10, FEAT-020 = DONE" |

### Phase 2: Trust-Risk Classification

**Purpose:** Classify how much users should trust AI outputs, determining the appropriate trust calibration target.

Yang et al. (2020) identify trust miscalibration as a primary failure mode: users who over-trust AI make dangerous errors of omission (failing to check AI outputs), while users who under-trust AI abandon valuable features. The classification determines the trust calibration target.

**Trust-Risk Levels:**

| Level | Definition | User-AI Relationship | Examples |
|-------|-----------|---------------------|----------|
| **HIGH** | AI makes decisions autonomously; user delegates control | User trusts AI to act without review | Autonomous trading, self-driving, automated content moderation |
| **MEDIUM** | AI recommends; human reviews and decides | User evaluates AI recommendation before acting | Medical diagnosis suggestions, hiring shortlist, content recommendations |
| **LOW** | AI assists; human maintains full control | User uses AI as a tool but makes all decisions | Search autocomplete, grammar suggestions, code completion |

**Assessment criteria:**
1. **Consequence of over-trust:** What happens if a user accepts an incorrect AI output without review? Rate: catastrophic (safety, financial ruin), significant (costly mistake), minor (inconvenience)
2. **Consequence of under-trust:** What happens if a user ignores a correct AI output? Rate: significant loss (missed opportunity, inefficiency), minor loss, negligible
3. **User expertise level:** Can the user independently evaluate AI output quality? Expert (can verify), intermediate (partially verify), novice (cannot verify)
4. **AI output verifiability:** Can the user verify AI correctness before acting? Easily verifiable, partially verifiable, unverifiable

**Classification algorithm:**
- Consequence of over-trust = catastrophic OR output unverifiable -> HIGH trust-risk
- Consequence of over-trust = significant AND user = novice -> HIGH trust-risk
- Consequence of over-trust = significant AND user = intermediate -> MEDIUM trust-risk
- Consequence of over-trust = minor AND output easily verifiable -> LOW trust-risk
- If no above criteria are met, apply the conservative default: MEDIUM trust-risk (per Yang et al., 2020)
- **Tie-breaker:** When multiple rules fire for conflicting levels (e.g., one criterion indicates HIGH and another indicates MEDIUM), apply the higher-risk classification. Rationale: under-protecting against trust miscalibration is more costly than over-protecting (Yang et al., 2020).

### Phase 3: Error-Risk Classification

**Purpose:** Classify the cost of AI errors, determining the appropriate error mitigation design.

Yang et al. (2020) identify error cost mismanagement as the second primary failure mode: designers who underestimate error costs create brittle AI interfaces that fail catastrophically, while designers who overestimate error costs create excessively cautious interfaces that reduce AI utility.

**Error-Risk Levels:**

| Level | Definition | Error Characteristics | Examples |
|-------|-----------|----------------------|----------|
| **HIGH** | Irreversible or safety-critical errors | Errors cannot be undone; may cause physical, financial, or legal harm | Medical treatment decisions, financial transactions, safety system overrides |
| **MEDIUM** | Costly but recoverable errors | Errors require significant effort to correct but are not permanent | Content publishing, email scheduling, resource allocation |
| **LOW** | Negligible-impact errors | Errors are easily corrected or have minimal consequence | Search suggestions, content formatting, UI customization |

**Assessment criteria:**
1. **Reversibility:** Can the AI error be undone? Irreversible, reversible with significant cost, easily reversible
2. **Blast radius:** How many users/systems are affected by a single error? Organization-wide, team/group, individual only
3. **Error detection latency:** How quickly can an error be detected? Immediate (user sees result), delayed (discovered later), hidden (may never be discovered)
4. **Recovery cost:** What does it take to recover from an error? High (legal, financial, time), moderate (rework), low (simple correction)

**Classification algorithm:**
- Irreversible AND blast radius = organization-wide -> HIGH error-risk
- Irreversible AND detection = hidden -> HIGH error-risk
- Reversible with significant cost AND blast radius = team/group -> MEDIUM error-risk
- Easily reversible AND blast radius = individual -> LOW error-risk
- If no above criteria are met, apply the conservative default: MEDIUM error-risk
- **Tie-breaker:** When multiple rules fire for conflicting levels, apply the higher-risk classification. Rationale: underestimating error cost creates brittle interfaces that fail catastrophically (Yang et al., 2020).

### Phase 4: Interaction Pattern Selection

**Purpose:** Select the appropriate interaction pattern from the trust-risk x error-risk matrix.

The trust-risk x error-risk matrix produces nine cells, each mapping to a specific human-AI collaboration pattern:

| | LOW Error-Risk | MEDIUM Error-Risk | HIGH Error-Risk |
|---|---|---|---|
| **HIGH Trust-Risk** | AI autonomous with periodic review. Pattern: AI operates independently; human reviews aggregated outcomes at intervals. Design: dashboard monitoring, exception alerts. | AI advisor with mandatory review. Pattern: AI recommends; human must explicitly approve before execution. Design: recommendation + approve/reject UI, decision audit trail. | Full human oversight, AI as information provider only. Pattern: AI provides analysis; human makes all decisions and executes all actions. Design: AI-generated briefings, decision support dashboards, no automation. |
| **MEDIUM Trust-Risk** | AI autonomous with user correction. Pattern: AI acts; user can correct afterward. Design: undo/edit controls, correction feedback loops. | Human-in-the-loop with AI assistance. Pattern: AI prepares work; human reviews, modifies, and approves. Design: draft/review workflow, inline editing, confidence indicators. | Human-controlled with AI safety checks. Pattern: Human decides and acts; AI validates and warns of potential errors before execution. Design: confirmation dialogs with AI analysis, risk warnings, safety gates. |
| **LOW Trust-Risk** | AI fully autonomous (low stakes). Pattern: AI handles task without intervention. Design: results display, preference settings, background automation. | AI suggests with easy override. Pattern: AI offers suggestions; human can accept, modify, or ignore. Design: inline suggestions, accept/dismiss controls. | AI assists with mandatory human verification. Pattern: AI provides input; human verifies before each action. Design: step-by-step verification, checklist with AI pre-fills. |

**Pattern selection procedure:**
1. Map the trust-risk level (Phase 2) and error-risk level (Phase 3) to the matrix cell
2. Identify the primary interaction pattern for that cell
3. Evaluate whether the pattern matches the product's technical constraints (does the AI system support the required human oversight mechanism?)
4. If technical constraints prevent the ideal pattern, select the adjacent cell with higher human oversight (never lower)
5. Document the selected pattern, the rationale, and any deviation from the matrix recommendation

### Phase 5: Feedback Loop and Progressive Disclosure Design

**Purpose:** Design the mechanisms through which the AI system communicates with users and builds trust over time.

**Feedback Loop Design (Amershi et al., 2019):**

The feedback loop addresses four interaction phases per Amershi et al.'s (2019) 18 guidelines:

| Phase | Guidelines Applied | Design Element |
|-------|-------------------|----------------|
| **Initially** (G1-G2) | Make clear what the system can do; make clear how well the system can do it | Onboarding: capability disclosure, accuracy expectations, limitation statements |
| **During interaction** (G3-G8) | Time services based on context; show contextually relevant information; match relevant social norms; mitigate social biases; support efficient invocation/dismissal; make clear why the system did what it did | Real-time: contextual explanations, confidence indicators, dismissal controls |
| **When wrong** (G9-G13) | Support efficient correction; scope services when in doubt; make clear how to provide feedback | Error recovery: correction mechanisms, feedback channels, graceful degradation |
| **Over time** (G14-G18) | Learn from user behavior; update and adapt cautiously; encourage granular feedback; convey consequences of user actions; provide global controls | Evolution: adaptation transparency, control settings, usage analytics |

**Progressive Disclosure Strategy (Shneiderman, 2020):**

Progressive disclosure builds user trust through graduated exposure to AI capabilities:

| Stage | Trust Level | AI Autonomy | User Control | Duration |
|-------|-------------|-------------|-------------|----------|
| **Stage 1: Introduction** | Minimal trust | AI explains only; no actions | Full user control | First 1-2 weeks |
| **Stage 2: Suggestion** | Growing trust | AI suggests; user decides | Accept/reject controls | Weeks 2-4 |
| **Stage 3: Collaboration** | Established trust | AI drafts; user edits and approves | Edit + approve workflow | Months 1-2 |
| **Stage 4: Delegation** | High trust | AI acts; user monitors and corrects | Monitoring dashboard + undo | Months 2+ |
| **Stage 5: Autonomy** | Full trust | AI operates independently within bounds | Exception-only intervention | After 30+ days at Stage 4 with error rate below threshold AND explicit user opt-in |

> **Calibration note:** Duration estimates are heuristic starting points derived from typical enterprise adoption patterns. Teams SHOULD adjust based on domain risk profile, user sophistication, and observed trust-building velocity. See [Constitutional Compliance](#constitutional-compliance) for calibration governance.

**Advancement criteria:** Each stage advancement requires:
- Minimum time at current stage (no instant escalation)
- User explicitly opts in to higher autonomy (never automatic)
- Error rate at current stage below threshold [team-defined; suggested: < 5% LOW, < 2% MEDIUM, < 0.5% HIGH error-risk]
- User demonstrates correction capability at current stage

**Output:** Feedback loop specification and progressive disclosure plan with stage definitions, advancement criteria, and rollback conditions.

### Phase 6: Synthesis and Handoff Preparation

**Purpose:** Synthesize findings, produce L0/L1/L2 output artifact, construct downstream handoff.

**Activities:**
1. Produce L0 executive summary: trust-risk classification, error-risk classification, selected interaction pattern, top design recommendations, key findings
2. Produce L1 technical detail: full trust-risk x error-risk analysis, interaction pattern specification, feedback loop design, transparency assessment, progressive disclosure plan, citations to Amershi et al. (2019) guidelines and PAIR patterns
3. Produce L2 strategic implications: AI interaction maturity assessment, trust calibration roadmap, capability progression strategy, organizational readiness for increased AI autonomy
4. Compile Synthesis Judgments Summary: every AI judgment call with confidence classification and rationale
5. Prepare `/ux-inclusive-design` handoff: AI interface patterns requiring accessibility review (screen reader compatibility for AI explanations, keyboard navigation for AI controls, cognitive accessibility of AI feedback)
6. Prepare `/ux-heuristic-eval` handoff: AI interface patterns for usability review against Nielsen's 10 + AI-specific heuristic supplement

**Output:** Complete output artifact per the Required Output Sections specification (L0 executive summary, L1 technical sections, L2 strategic implications, synthesis judgments, handoff data).

---

## Output Specification

### Output Location

```
skills/ux-ai-first-design/output/{engagement-id}/ux-ai-design-guide-{topic-slug}.md
```

Where:
- `{engagement-id}` follows the pattern `UX-{NNNN}` (e.g., `UX-0001`)
- `{topic-slug}` is a kebab-case descriptor of the AI capability (e.g., `recommendation-engine`, `ai-assistant`, `content-moderation`)

### Required Output Sections

| Section | Level | Content |
|---------|-------|---------|
| **Executive Summary** | L0 | Trust-risk classification; error-risk classification; selected interaction pattern; human oversight level; top design recommendations; key findings for stakeholders and cross-framework synthesis input |
| **Engagement Context** | L1 | Product description, target users, AI capability characterization, AI technology, determinism level, confidence availability, failure modes, upstream inputs, CONDITIONAL activation verification |
| **Trust-Risk Assessment** | L1 | Trust-risk classification with assessment criteria scores (over-trust consequence, under-trust consequence, user expertise, output verifiability), classification algorithm trace, evidence chain |
| **Error-Risk Assessment** | L1 | Error-risk classification with assessment criteria scores (reversibility, blast radius, detection latency, recovery cost), classification algorithm trace, evidence chain |
| **Interaction Pattern Specification** | L1 | Selected pattern from trust-risk x error-risk matrix; pattern description; design elements; technical constraints assessment; deviation rationale (if any) |
| **Feedback Loop Design** | L1 | Four-phase feedback design per Amershi et al. (2019): initially, during interaction, when wrong, over time; specific design elements per phase; Amershi guideline IDs cited |
| **Progressive Disclosure Plan** | L1 | Stage definitions (Introduction through Autonomy); advancement criteria per stage; rollback conditions; estimated timeline |
| **AI Transparency Assessment** | L1 | Evaluation against Google PAIR (2019) patterns; transparency gaps identified; explainability recommendations; confidence communication design |
| **Strategic Implications** | L2 | AI interaction maturity assessment; trust calibration roadmap; capability progression strategy; organizational readiness analysis |
| **Synthesis Judgments Summary** | L1 | Each AI judgment call listed for synthesis confidence gate compliance |
| **Handoff Data** | L1 | Structured data for downstream sub-skills: AI interface patterns for inclusive design review, AI interaction patterns for heuristic evaluation |

**Synthesis Judgments Summary requirements:** MUST list every AI judgment (trust-risk classification, error-risk classification, interaction pattern selection, feedback loop design choices, progressive disclosure stage definitions) with confidence classification (HIGH/MEDIUM/LOW) and rationale. Each judgment row includes: finding ID, framework source (e.g., Yang et al. trust-risk, Amershi guideline, PAIR pattern), confidence level (HIGH/MEDIUM/LOW), and rationale explaining the classification basis and evidence chain. Follows the pattern in `skills/user-experience/rules/synthesis-validation.md` [Cross-Framework Synthesis Protocol].

### Templates

| Template | Path | Purpose |
|----------|------|---------|
| AI-First Design Template | `skills/ux-ai-first-design/templates/ai-first-design-template.md` | Trust-risk x error-risk assessment, interaction pattern specification, feedback loop design, progressive disclosure plan |

---

## Routing

### Trigger Keywords

| Keyword | Routing Context |
|---------|----------------|
| AI-first design | Direct match -- primary trigger |
| AI interaction | Direct match |
| trust calibration | In combination with AI/UX context |
| AI UX | Direct match |
| conversational UX | Direct match |
| AI interface | In combination with design/UX context |
| LLM interface | Direct match |
| agentic UX | Direct match |
| human-AI interaction | Direct match |
| AI transparency | In combination with design/UX context |
| AI error handling | In combination with design/UX context |
| AI onboarding | In combination with AI/design context |
| progressive AI disclosure | Direct match |
| trust-risk | In combination with AI/design context |
| error-risk | In combination with AI/design context |

### Lifecycle-Stage Routing Integration

This sub-skill is routed to by the `ux-orchestrator` in the following lifecycle-stage scenarios:

| Stage | User Intent | Route Condition |
|-------|-------------|-----------------|
| During design | "Building AI product" | CONDITIONAL: Enabler FEAT-020 DONE AND WSM >= 7.80 -> route to `/ux-ai-first-design`; otherwise -> `/ux-heuristic-eval` with PAIR protocol; source: `skills/user-experience/rules/ux-routing-rules.md` Stage Routing Table |
| During design | Follow-up from heuristic evaluation of AI interface | When `/ux-heuristic-eval` has identified AI-specific usability issues (transparency gaps, trust calibration problems) and CONDITIONAL criteria are met |
| Any stage | "Design AI interaction" or "Audit AI interface" | Qualification question: "Is the FEAT-020 enabler complete and WSM >= 7.80?" -> Yes: route here; No: route to `/ux-heuristic-eval` with PAIR supplement |

### Wave Gating

This sub-skill is in **Wave 5** (Process Intensives) and is **CONDITIONAL**. It requires Wave 4 completion AND additional conditions before deployment:

**Standard Wave 5 entry criteria:** Wave 4 completed -- 30+ users for Kano survey OR 1 B=MAP bottleneck diagnosed.

**CONDITIONAL entry criteria (additional):** WSM >= 7.80 AND enabler research (FEAT-020) complete (status: DONE).

**Bypass condition:** Design Sprint (`/ux-design-sprint`) can proceed without Kano prerequisite if team has existing user research. AI-First Design has no bypass -- both WSM threshold and enabler completion are hard requirements.

---

## Cross-Framework Integration

### Upstream Inputs

This sub-skill receives context from other sub-skills when invoked as part of a multi-sub-skill workflow:

| From Sub-Skill | Handoff Artifact | Key Fields | Usage |
|----------------|-----------------|-----------|-------|
| `/ux-heuristic-eval` | Severity-rated findings | Finding ID, heuristic violated, severity (0-4), affected screen/flow | Heuristic findings related to AI interface issues (transparency, controllability, error recovery) provide context for AI interaction design; severity >= 2 findings identify specific AI interface locations requiring trust calibration |
| `/ux-behavior-design` | Bottleneck diagnosis | Bottleneck factor, severity, B=MAP scores | Behavioral bottlenecks in AI feature adoption (users not trusting AI recommendations, avoiding AI features) provide context for trust calibration and progressive disclosure design |

### Downstream Handoffs

This sub-skill produces artifacts that feed into other sub-skills via the Jerry handoff protocol (`docs/schemas/handoff-v2.schema.json`).

| To Sub-Skill | Handoff Artifact | Key Fields | Trigger |
|-------------|-----------------|-----------|---------|
| `/ux-inclusive-design` | AI interface patterns for accessibility review | Interaction pattern, feedback loop design, progressive disclosure stages, screen reader considerations, cognitive accessibility notes | After interaction pattern and feedback loop design are complete; inclusive design evaluator audits the AI interface for WCAG 2.2 compliance and cognitive accessibility |
| `/ux-heuristic-eval` | AI interaction patterns for usability review | Selected interaction pattern, feedback loop design, transparency assessment, AI-specific heuristic supplement data | After AI-first design is complete; heuristic evaluator assesses the designed AI interaction against Nielsen's 10 + AI-specific heuristics |

**Handoff data format (handoff-v2 + ux-ext):**

```yaml
handoff:
  from_agent: ux-ai-design-guide
  to_agent: ux-inclusive-evaluator
  task: "Audit AI interface patterns for WCAG 2.2 compliance and cognitive accessibility"
  success_criteria:
    - "AI explanation mechanisms evaluated for screen reader compatibility"
    - "AI controls assessed for keyboard navigation"
    - "Progressive disclosure stages reviewed for cognitive accessibility"
  artifacts:
    - "skills/ux-ai-first-design/output/{engagement-id}/ux-ai-design-guide-{topic-slug}.md"
  key_findings:
    - "Trust-risk: {level}; Error-risk: {level}"
    - "Interaction pattern: {pattern_name}"
    - "Human oversight level: {oversight_level}"
  blockers: []
  confidence: 0.5  # Conservative default: AI-first design patterns are rapidly evolving (LOW synthesis confidence per Wave Gating); downstream agents SHOULD recalibrate based on engagement-specific evidence quality
  criticality: C2
  ux_ext:
    trust_risk_level: "{HIGH|MEDIUM|LOW}"
    error_risk_level: "{HIGH|MEDIUM|LOW}"
    interaction_pattern: "{pattern_name}"
    ai_capability_type: "{generative|classificatory|decisional|recommendatory}"
    feedback_loop_design:
      initially: "{onboarding design summary}"
      during_interaction: "{real-time feedback summary}"
      when_wrong: "{error recovery summary}"
      over_time: "{adaptation strategy summary}"
    human_oversight_level: "{full_oversight|advisory|human_in_loop|monitored_autonomous|autonomous}"
```

### Canonical Multi-Skill Workflow Sequences

This sub-skill participates in the following canonical sequences:

| Sequence | Skills Involved | This Sub-Skill's Role |
|----------|----------------|-----------------------|
| AI Product Design Pipeline | `/ux-jtbd` then `/ux-lean-ux` then **`/ux-ai-first-design`** then `/ux-inclusive-design` | Receives validated user needs and hypotheses; produces trust-calibrated AI interaction patterns; hands off to inclusive design for accessibility audit |
| AI Interface Audit | `/ux-heuristic-eval` then **`/ux-ai-first-design`** then `/ux-inclusive-design` | Receives heuristic findings for AI interface issues; produces targeted trust calibration and interaction redesign; hands off to inclusive design |
| AI Feature Adoption Fix | `/ux-behavior-design` then **`/ux-ai-first-design`** then `/ux-heart-metrics` | Receives behavioral bottleneck diagnosis for AI feature; redesigns AI interaction to address trust/adoption barriers; hands off to HEART for measurement |

---

## Synthesis Hypothesis Confidence

AI-First Design outputs include synthesis hypotheses that carry confidence classifications per the synthesis validation protocol.

| Synthesis Step | Typical Confidence | Rationale |
|---------------|-------------------|-----------|
| AI interaction pattern recommendations | LOW | AI design patterns are rapidly evolving; training data may be stale relative to current best practices. The field of human-AI interaction is less than a decade old with rapidly shifting paradigms (Yang et al., 2020). Pattern recommendations are directionally sound per the trust-risk/error-risk framework but specific implementation details may not reflect the latest AI interaction innovations. |

**Gate enforcement:**
- **LOW outputs (all AI-First Design recommendations):** All recommendation sections tagged `[REFERENCE-ONLY]`. Banner: "AI-First Design recommendations are based on the trust-risk/error-risk framework (Yang et al., 2020) and established guidelines (Amershi et al., 2019; Google PAIR, 2019). The AI interaction design field evolves rapidly; validate recommendations against current platform-specific guidelines and user testing before implementation."

**Note on confidence dynamics:** AI-First Design confidence may achieve MEDIUM when converged with a second framework -- for example, when `/ux-heuristic-eval` with PAIR protocol corroborates interaction pattern recommendations, or when `/ux-lean-ux` experiment results validate the proposed interaction pattern. Confidence remains LOW for emerging AI paradigms (agentic UX, multi-modal AI interfaces) where established guidelines do not yet exist.

---

## Quality Gate Integration

AI-First Design outputs are subject to the Jerry quality gate per H-13 and H-14:

| Quality Check | Threshold | Application |
|---------------|-----------|-------------|
| S-014 LLM-as-Judge scoring | >= 0.92 composite (C2+) | Applied at Phase 6 completion |
| Creator-critic-revision | Minimum 3 iterations (H-14) | Orchestrator manages revision cycles |
| Self-review (S-010) | Required before presenting | Self-review before returning to orchestrator |
| Wave transition gate | S-014 composite >= 0.85 | Applied at Wave 5 signoff |

**Scoring dimensions (AI-First Design interpretation):**

| Dimension | Weight | Interpretation |
|-----------|--------|----------------|
| Completeness | 0.20 | Both trust-risk and error-risk classified; interaction pattern selected; feedback loop designed; progressive disclosure plan included |
| Internal Consistency | 0.20 | Interaction pattern consistent with trust-risk x error-risk classification; feedback loop addresses selected pattern's requirements; progressive disclosure stages aligned with trust-risk level |
| Methodological Rigor | 0.20 | Yang et al. framework correctly applied; Amershi guidelines cited by number; PAIR patterns referenced; classification algorithms followed |
| Evidence Quality | 0.15 | Classifications cite assessment criteria; evidence quality classified; training data staleness risk disclosed per P-022 |
| Actionability | 0.15 | Interaction patterns specific and implementable; feedback loop design technically feasible; progressive disclosure stages have clear advancement criteria |
| Traceability | 0.10 | Findings trace to Yang et al., Amershi et al., PAIR, or Shneiderman; synthesis judgments documented; upstream findings cited |

### CI Gate Summary

The following CI gate criteria apply to this sub-skill (full gate definitions in `skills/user-experience/rules/ci-checks.md`):

| Gate | Check | Enforcement |
|------|-------|-------------|
| **No Agent tool access** | `disallowedTools: [Agent]` present in agent frontmatter; agent MUST NOT have Agent in `tools` list | L5 (CI): grep agent frontmatter for Agent tool presence |
| **P-003 forbidden action** | `capabilities.forbidden_actions` in `.governance.yaml` MUST include P-003 recursive subagent prohibition | L5 (CI): schema validation of governance YAML against `docs/schemas/agent-governance-v1.schema.json` |
| **Output schema validation** | Agent output MUST contain all Required Output Sections (Executive Summary, Engagement Context, Trust-Risk Assessment, Error-Risk Assessment, Interaction Pattern Specification, Feedback Loop Design, Progressive Disclosure Plan, AI Transparency Assessment, Strategic Implications, Synthesis Judgments Summary, Handoff Data) | L4 (post-tool): section heading presence check on output artifact |

---

## Degraded Mode Behavior

The `ux-ai-design-guide` operates at T4 (External) with access to WebSearch, WebFetch, and Context7 MCP. The following degraded modes apply when external tools or MCP dependencies are unavailable.

### Figma MCP Unavailable

Figma MCP is listed as REQ for AI-First Design in the parent SKILL.md MCP Integration Architecture. When Figma MCP is unavailable:

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| No AI interface prototyping | Cannot create or inspect interactive AI interface prototypes | Manual wireframe descriptions: describe AI interaction patterns in text with annotated mockup references; use markdown tables for interaction flow specification |
| No component inspection | Cannot examine existing AI interface components programmatically | User provides screenshots or text descriptions of current AI interface state |
| No design system integration | Cannot reference existing Figma design tokens for AI components | Reference standard platform design guidelines (Material Design, Human Interface Guidelines) via WebSearch/Context7 |

### Context7 Unavailable

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| No AI SDK documentation | Cannot access current documentation for AI framework libraries | Fall back to WebSearch for AI SDK documentation; note "Context7 unavailable" in output |
| No design pattern library docs | Cannot query component library documentation | Use WebSearch for design pattern references; cite web sources |

### WebSearch/WebFetch Unavailable

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| No current AI design pattern research | Cannot access latest AI interaction design guidelines or platform updates | Rely on methodology knowledge (Yang et al., Amershi et al., PAIR, Shneiderman); disclose training data staleness risk prominently per P-022 |
| No competitive AI interface analysis | Cannot research competitor AI interfaces | Ask user to provide competitor screenshots or descriptions |

**Degraded mode disclosure (P-022):**
```
[DEGRADED MODE] This output was produced without access to {unavailable tools}.
AI-First Design recommendations are based on established frameworks (Yang et al., 2020;
Amershi et al., 2019; Google PAIR, 2019) but may not reflect the latest platform-specific
guidelines or AI interaction innovations.
Limitations:
- Interaction pattern recommendations based on framework knowledge, not current best practices
- AI SDK integration guidance may reference outdated API patterns
- Competitive analysis limited to user-provided descriptions
```

---

## Wave Architecture

### Wave 5: Process Intensives -- CONDITIONAL

This sub-skill is part of Wave 5 (Process Intensives), alongside `/ux-design-sprint`.

**Standard Wave 5 entry criteria:** Wave 4 completed -- 30+ users for Kano survey OR 1 B=MAP bottleneck diagnosed.

**CONDITIONAL entry criteria (additional):**
1. **WSM >= 7.80** -- The team's Wave Scorecard Metric must meet the minimum threshold, indicating sufficient UX maturity for AI-first design methodology
2. **Enabler FEAT-020 complete (DONE)** -- The AI interaction design enabler research must be marked complete, providing the foundational knowledge base for AI design patterns

**When CONDITIONAL criteria are NOT met:**
- The `ux-orchestrator` routes "Building AI product" requests to `/ux-heuristic-eval` with PAIR protocol as an interim alternative
- PAIR protocol adds AI-specific heuristics (transparency, controllability, error recovery) to Nielsen's 10, providing interim AI interface evaluation capability
- The orchestrator informs the user of the routing decision and what is needed to activate the full AI-First Design sub-skill

**Bypass condition:** None. Both WSM threshold and enabler completion are hard requirements. Unlike other Wave 5 sub-skills, AI-First Design has no bypass because:
- The WSM threshold ensures the team has sufficient UX maturity to apply the complex trust-risk/error-risk methodology
- The enabler research provides essential AI design pattern knowledge that cannot be substituted

**Wave transition from Wave 4 to Wave 5:** Requires 30+ users for Kano survey OR 1 B=MAP bottleneck diagnosed.

---

## Constitutional Compliance

All agents in this sub-skill adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- worker agent, no Agent tool access | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user decisions on trust-risk classification, interaction pattern selection, or progressive disclosure stage advancement | Unauthorized action; trust erosion |
| P-022 | NEVER present AI interaction pattern recommendations as current best practices without disclosing training data staleness risk; NEVER inflate trust-risk or error-risk classifications without supporting evidence; NEVER omit the LOW synthesis confidence disclosure on recommendations; NEVER suppress degraded mode disclosure when operating without external tools | Governance undermined; quality assessment invalidated |
| P-001 | NEVER present trust-risk or error-risk classifications without citing the evidence or reasoning supporting the assessment | Unreliable outputs; unfounded claims propagate downstream |
| P-002 | NEVER leave AI interaction design recommendations in transient context only -- persist to files | Context rot vulnerability; artifacts lost on session compaction |

**Per-agent enforcement:** The `ux-ai-design-guide` agent declares:
- `constitution.principles_applied`: P-003, P-020, P-022, P-001, P-002 in `skills/ux-ai-first-design/agents/ux-ai-design-guide.governance.yaml`
- `capabilities.forbidden_actions`: 3 entries in NPT-009 format referencing the constitutional triplet
- `disallowedTools: [Agent]` in `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` frontmatter

### AI Pattern Staleness Risk Disclosure (P-022)

The field of human-AI interaction design is rapidly evolving. Training data for the agent may not reflect the latest AI interaction paradigms, platform-specific guidelines, or emerging best practices. Per P-022 (no deception), the agent MUST:

1. **Disclose staleness risk** in every output: "AI design pattern recommendations are based on established frameworks (Yang et al., 2020; Amershi et al., 2019; Google PAIR, 2019; Shneiderman, 2020). The AI interaction design field evolves rapidly. Validate against current platform-specific guidelines before implementation."
2. **Use WebSearch/Context7** to supplement training data with current documentation when available
3. **Flag emerging paradigms** (agentic UX, multi-modal AI, AI agents) where established guidelines do not yet exist and confidence is inherently lower
4. **Mark all recommendations** with LOW synthesis confidence per the synthesis validation protocol

### AI-Augmented Analysis Limitations

The AI-First Design agent operates as an AI-augmented design tool. The following limitations apply to all outputs and MUST be disclosed per P-022 (no deception):

- **Trust-risk and error-risk classifications are context-dependent.** The same AI capability may have different risk profiles in different domains (e.g., medical vs. entertainment). The agent provides structured reasoning but the team should validate against domain-specific knowledge.
- **Interaction pattern selection assumes standard user populations.** Specialized user populations (experts vs. novices, accessibility needs, cultural contexts) may require pattern adjustments identified through `/ux-inclusive-design` and `/ux-jtbd` analysis.
- **Progressive disclosure timelines are estimates.** Actual trust-building timelines depend on user experience, AI system reliability, organizational culture, and domain risk tolerance. The agent provides framework-based estimates that require empirical calibration.
- **AI design patterns are evolving faster than any single framework can capture.** The Yang et al. (2020) and Amershi et al. (2019) frameworks provide the most rigorous foundations available, but new paradigms (agentic AI, multi-modal interactions, autonomous agents) may require pattern extensions not covered by these frameworks.

---

## Registration

This sub-skill follows a parent-routed registration model per H-26. Sub-skills are routed through the parent `/user-experience` orchestrator; independent registration would create duplicate triggers (AP-02).

| Registration Point | Status | Detail |
|--------------------|--------|--------|
| `CLAUDE.md` skill table | Registered via parent | `/user-experience` registered; sub-skills not independently listed |
| `mandatory-skill-usage.md` trigger map | Routed via parent | "AI-first design" keyword routes to parent, which dispatches here (CONDITIONAL) |
| `AGENTS.md` agent registry | Registered | `ux-ai-design-guide` listed under User-Experience Skill Agents |
| Parent SKILL.md agent table | Registered | Listed in `skills/user-experience/SKILL.md` [Available Agents] with CONDITIONAL notation |

---

## Deployment Status

> **Wave 5 Sub-Skill -- CONDITIONAL -- Phase 1 Complete, Phase 2 Pending.**
>
> This sub-skill follows a two-phase implementation sequence:
>
> - **Wave 5 Phase 1 (this deliverable):** SKILL.md specification -- methodology, output format, routing integration, template stub, cross-framework integration, and quality gate criteria. This document is the Phase 1 artifact.
> - **Wave 5 Phase 2 (pending):** Agent implementation -- `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` (agent definition with `<input>`, `<capabilities>`, `<methodology>`, `<output>` sections) and `skills/ux-ai-first-design/agents/ux-ai-design-guide.governance.yaml` (governance metadata). Tracked under PROJ-022 EPIC-005.
>
> **CONDITIONAL NOTE:** Even after Phase 2 implementation, this sub-skill only activates when WSM >= 7.80 AND enabler FEAT-020 is complete. Until these conditions are met, the `ux-orchestrator` routes AI product design requests to `/ux-heuristic-eval` with PAIR protocol.

---

## Quick Reference

### Common Workflows

| Need | Command Example |
|------|-----------------|
| Design AI assistant interaction | "Design the conversational UX for our AI assistant feature" |
| Classify AI trust risk | "How should we calibrate user trust in our AI recommendations?" |
| Select AI interaction pattern | "What interaction pattern should we use for AI-generated content?" |
| Audit AI interface | "Audit our AI chatbot interface for transparency and trust issues" |
| Design AI onboarding | "Design progressive AI disclosure for our new ML feature" |
| AI error recovery design | "Design error handling flows for our AI prediction failures" |

### Agent Selection Hints

| Keywords | Routes To |
|----------|-----------|
| AI-first design, AI interaction, trust calibration, AI UX, conversational UX, AI interface, LLM interface, agentic UX, human-AI interaction, AI transparency, AI error handling, AI onboarding, trust-risk, error-risk | `ux-ai-design-guide` (CONDITIONAL) |
| heuristic, usability, Nielsen, severity, inspection, evaluation | `/ux-heuristic-eval` (not this sub-skill; interim alternative when CONDITIONAL not met) |
| behavior, Fogg, B=MAP, motivation, ability | `/ux-behavior-design` (not this sub-skill) |
| HEART, metrics, measurement, GSM, happiness, engagement | `/ux-heart-metrics` (not this sub-skill) |
| inclusive design, WCAG, accessibility, persona spectrum | `/ux-inclusive-design` (not this sub-skill; receives AI accessibility handoff) |
| lean UX, hypothesis, assumption, experiment | `/ux-lean-ux` (not this sub-skill) |
| design sprint, prototype, rapid validation | `/ux-design-sprint` (not this sub-skill) |
| Kano, feature prioritization, must-be, attractive | `/ux-kano-model` (not this sub-skill) |

### Routing Disambiguation

| Context | Routes To | Rationale |
|---------|-----------|-----------|
| "Review this AI interface" + CONDITIONAL met | `/ux-ai-first-design` | Full trust-risk/error-risk analysis |
| "Review this AI interface" + CONDITIONAL NOT met | `/ux-heuristic-eval` + PAIR | Interim AI evaluation via heuristic supplement |
| "Why aren't users trusting the AI?" | `/ux-behavior-design` then `/ux-ai-first-design` | Behavioral bottleneck diagnosis first, then trust calibration |
| "Make the AI accessible" | `/ux-inclusive-design` | Accessibility audit, not interaction design |
| "Red-team the AI" | `/red-team` or `/adversary` | Security/quality concern, not UX design |

---

## References

| Source | Content | Path |
|--------|---------|------|
| Parent SKILL.md | Sub-skill scope, wave architecture, routing, MCP dependencies, synthesis protocol | `skills/user-experience/SKILL.md` |
| Agent definition | Agent frontmatter, identity, expertise, guardrails | `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` [PLANNED] |
| Agent governance | Tool tier, forbidden actions, output validation, constitutional compliance | `skills/ux-ai-first-design/agents/ux-ai-design-guide.governance.yaml` [PLANNED] |
| UX routing rules | Lifecycle-stage routing, handoff data contracts, common intent resolution, CONDITIONAL routing | `skills/user-experience/rules/ux-routing-rules.md` |
| Synthesis validation | Confidence gate protocol, per-sub-skill confidence map, signal extraction criteria | `skills/user-experience/rules/synthesis-validation.md` [Cross-Framework Synthesis Protocol] |
| Wave progression | Wave 5 entry criteria, signoff requirements | `skills/user-experience/rules/wave-progression.md` |
| CI checks | P-003 enforcement, sub-skill validation gates | `skills/user-experience/rules/ci-checks.md` |
| AI-First design template | Trust-risk x error-risk assessment, interaction pattern specification, feedback loop design | `skills/ux-ai-first-design/templates/ai-first-design-template.md` |
| Skill standards | H-25/H-26 skill structure requirements | `.context/rules/skill-standards.md` |
| Agent development standards | H-34 dual-file architecture, tool tiers, handoff protocol | `.context/rules/agent-development-standards.md` |
| Quality enforcement | Quality gate thresholds, criticality levels, strategy catalog | `.context/rules/quality-enforcement.md` |
| Handoff schema | Canonical handoff schema v2 | `docs/schemas/handoff-v2.schema.json` |
| Agent governance schema | Governance YAML validation schema | `docs/schemas/agent-governance-v1.schema.json` |

### Requirements Traceability

| Source | Content | Path |
|--------|---------|------|
| PROJ-022 PLAN.md | Project plan: sub-skill scope, wave assignment, acceptance criteria, implementation phases | `projects/PROJ-022-user-experience-skill/PLAN.md` |
| EPIC-005 (Wave 5 Deployment) | Parent work item for Wave 5 sub-skill implementation including this sub-skill | PROJ-022 EPIC-005 in `projects/PROJ-022-user-experience-skill/WORKTRACKER.md` |
| ORCHESTRATION.yaml | Orchestration plan governing the build sequence for this sub-skill | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |

### External References

| Source | Citation |
|--------|----------|
| Yang, Q., Steinfeld, A., Rose, C., & Zimmerman, J. (2020) | "Re-examining Whether, Why, and How Human-AI Interaction Is Uniquely Difficult to Design." CHI '20: Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems, pp. 1-13. ACM. DOI: [10.1145/3313831.3376301](https://doi.org/10.1145/3313831.3376301). Foundational analysis of trust-risk and error-risk as the two primary failure modes in AI interaction design. |
| Amershi, S., Weld, D., Vorvoreanu, M., Fourney, A., Nushi, B., Collisson, P., ... & Horvitz, E. (2019) | "Guidelines for Human-AI Interaction." CHI '19: Proceedings of the 2019 CHI Conference on Human Factors in Computing Systems, pp. 1-13. ACM. DOI: [10.1145/3290605.3300233](https://doi.org/10.1145/3290605.3300233). 18 design guidelines organized by interaction phase (initially, during interaction, when wrong, over time). |
| Google PAIR (2019) | "People + AI Guidebook." Google. Available at [pair.withgoogle.com/guidebook](https://pair.withgoogle.com/guidebook). Practical AI design patterns for transparency, explainability, user control, and feedback. Reference for AI interface transparency assessment. |
| Shneiderman, B. (2020) | "Human-Centered Artificial Intelligence: Reliable, Safe & Trustworthy." International Journal of Human-Computer Interaction, 36(6), pp. 495-504. DOI: [10.1080/10447318.2020.1741118](https://doi.org/10.1080/10447318.2020.1741118). Framework for balancing human control with AI automation; progressive disclosure of AI capabilities; human-centered AI principles. See also Shneiderman, B. (2021), "Human-Centered AI," Issues in Science and Technology, 37(2). Available at [issues.org](https://issues.org/human-centered-artificial-intelligence-shneiderman/). |

---

*Sub-Skill Version: 1.1.0*
*Parent Skill: `/user-experience` v1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Wave: 5 (Process Intensives) -- CONDITIONAL*
*SSOT: `skills/user-experience/SKILL.md`*
*Project: PROJ-022 User Experience Skill*
*Created: 2026-03-04*
