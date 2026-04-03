---
name: ux-behavior-design
description: "Fogg Behavior Model B=MAP bottleneck diagnosis sub-skill for the /user-experience parent skill. Diagnoses why users fail to take desired actions by analyzing the three B=MAP factors (Motivation, Ability, Prompt) and identifying which factor falls below the action threshold. Produces bottleneck diagnoses, factor-level assessments, and intervention recommendations with synthesis confidence gates. Invoke when teams need to understand why users are not completing a specific action, diagnose behavioral bottlenecks, design behavior change interventions, or analyze post-launch user inaction patterns. Invoked by ux-orchestrator during Wave 4 lifecycle-stage routing or when user intent is \"Users not completing action\" during the \"After launch\" stage. Triggers: behavior design, B=MAP, Fogg model, behavior bottleneck, motivation analysis, ability analysis, prompt design, why users don't, user inaction, behavior diagnosis, tiny habits, action threshold."
version: "1.5.0"
agents:
  - ux-behavior-diagnostician
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
activation-keywords:
  - "behavior design"
  - "B=MAP"
  - "Fogg model"
  - "behavior bottleneck"
  - "motivation analysis"
  - "ability analysis"
  - "prompt design"
  - "why users don't"
  - "user inaction"
  - "behavior diagnosis"
  - "tiny habits"
  - "action threshold"
---

<!-- VERSION: 1.5.0 | DATE: 2026-03-04 | SOURCE: skills/user-experience/SKILL.md | PARENT: /user-experience skill | REVISION: iter6 — fix inline citation at line 364 from Chapter 3 to Chapters 14-15 for behavior statement format, resolving contradiction with References table -->

# Behavior Design Sub-Skill

> **Version:** 1.5.0
> **Framework:** Jerry User-Experience -- Behavior Design
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Parent Skill:** `/user-experience` (`skills/user-experience/SKILL.md`)
> **Wave:** 4 (Advanced Analytics)
> **Project:** PROJ-022 User Experience Skill | GitHub Issue [#138](https://github.com/geekatron/jerry/issues/138)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Document Audience](#document-audience-triple-lens) | Triple-Lens audience guide |
| [Purpose](#purpose) | Sub-skill overview and key capabilities |
| [When to Use This Sub-Skill](#when-to-use-this-sub-skill) | Activation triggers and scope boundaries |
| [Available Agents](#available-agents) | Single agent with role, model, and output location |
| [P-003 Compliance](#p-003-compliance) | Worker agent hierarchy position |
| [Invoking the Agent](#invoking-the-agent) | Invocation via ux-orchestrator |
| [Methodology](#methodology) | Fogg B=MAP framework, factor analysis, bottleneck identification, intervention design, 5-phase execution procedure |
| [Output Specification](#output-specification) | Output location, L0/L1/L2 structure, required sections |
| [Routing](#routing) | Keywords and lifecycle-stage routing integration |
| [Cross-Framework Integration](#cross-framework-integration) | Handoff from heuristic evaluation and to HEART metrics |
| [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence) | Confidence classifications for Behavior Design outputs |
| [Quality Gate Integration](#quality-gate-integration) | S-014 scoring and H-13 threshold enforcement |
| [Degraded Mode Behavior](#degraded-mode-behavior) | Operation without real-time behavioral data |
| [Wave Architecture](#wave-architecture) | Wave 4 entry criteria, bypass conditions |
| [Constitutional Compliance](#constitutional-compliance) | Governing principles and AI-augmented analysis limitations |
| [Registration](#registration) | H-26 parent-routed registration model and AGENTS.md confirmation |
| [Deployment Status](#deployment-status) | Wave 4 stub agent status and implementation timeline |
| [Quick Reference](#quick-reference) | Common workflows and agent selection hints |
| [References](#references) | Full repo-relative paths, requirements traceability, external citations |

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Product managers, designers | [Purpose](#purpose), [When to Use This Sub-Skill](#when-to-use-this-sub-skill), [Quick Reference](#quick-reference) |
| **L1 (Developer)** | Engineers invoking the agent | [Invoking the Agent](#invoking-the-agent), [Methodology](#methodology), [Output Specification](#output-specification) |
| **L2 (Architect)** | Workflow designers, skill maintainers | [Cross-Framework Integration](#cross-framework-integration), [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence), [Degraded Mode Behavior](#degraded-mode-behavior) |

---

## Purpose

The Behavior Design sub-skill provides structured behavioral bottleneck diagnosis using BJ Fogg's Behavior Model, commonly expressed as B=MAP: Behavior happens when Motivation, Ability, and a Prompt converge at the same moment (Fogg, 2009; Fogg, 2020). It targets tiny teams (1-5 people) who observe users failing to complete desired actions and need a systematic framework to identify which behavioral factor is the limiting constraint.

This sub-skill is part of Wave 4 (Advanced Analytics), requiring Wave 3 completion before deployment. It bridges design system construction (Wave 3) and process-intensive activities (Wave 5) by providing behavioral insight that explains why well-designed interfaces still fail to drive target user actions.

### Key Capabilities

- **B=MAP Factor Assessment** -- Systematically evaluates each of the three behavioral factors (Motivation, Ability, Prompt) for a target behavior, determining whether each factor is above or below the action threshold (Fogg, 2020)
- **Motivation Analysis** -- Analyzes intrinsic motivators (sensation, anticipation, belonging), extrinsic motivators (rewards, punishments, social proof), and social drivers (competition, collaboration, recognition) that influence user willingness to act
- **Ability Analysis** -- Evaluates the six Fogg simplicity factors (Time, Money, Physical Effort, Brain Cycles, Social Deviance, Non-Routine) to identify friction points that make the target behavior too difficult (Fogg, 2009)
- **Prompt Analysis** -- Classifies prompts into three types (Facilitator, Signal, Spark) and assesses whether the right prompt type is deployed at the right moment for the user's motivation-ability state (Fogg, 2009)
- **Bottleneck Identification** -- Determines which single factor (or combination) is the primary constraint preventing the target behavior, using a structured elimination algorithm
- **Intervention Design** -- Recommends targeted interventions that address the diagnosed bottleneck: motivation interventions for low-motivation bottlenecks, simplification for low-ability bottlenecks, or prompt redesign for missing/mistimed prompts

---

## When to Use This Sub-Skill

Activate when:

- Users are not completing a specific desired action and the team needs to understand why
- Diagnosing whether user inaction stems from insufficient motivation, excessive difficulty, or absent/mistimed prompts
- Analyzing post-launch behavioral data showing low conversion, abandonment, or incomplete task flows
- Designing behavior change interventions targeted at a specific bottleneck factor
- Investigating why a well-designed interface fails to drive the intended user action
- Providing behavioral root-cause analysis for urgent UX problems (CRISIS mode step 2)
- Evaluating whether a proposed feature change addresses the correct behavioral bottleneck
- Preparing behavioral diagnosis to feed into HEART metrics measurement

Do NOT use for:

- Evaluating an existing interface against usability heuristics -- use `/ux-heuristic-eval` (Nielsen's 10) instead. Use heuristic evaluation first, then Behavior Design to trace severe issues to behavioral root causes.
- Building or auditing a component library -- use `/ux-atomic-design` (Atomic Design) instead.
- Accessibility compliance auditing -- use `/ux-inclusive-design` (WCAG 2.2) instead.
- Measuring quantitative UX health metrics -- use `/ux-heart-metrics` (Google GSM) instead. Use Behavior Design first to diagnose, then HEART to measure improvement.
- Understanding user motivations at the job level -- use `/ux-jtbd` (Jobs-to-Be-Done) instead. JTBD identifies what users want; Behavior Design diagnoses why they fail to complete a specific action.
- Testing hypotheses about design changes -- use `/ux-lean-ux` (Lean UX) instead.
- Running a full rapid prototyping sprint -- use `/ux-design-sprint` (Design Sprint 2.0) instead.
- Prioritizing features by user satisfaction impact -- use `/ux-kano-model` (Kano) instead.
- Security-focused interface review -- use `/eng-team` instead.
- General research without behavioral UX focus -- use `/problem-solving` instead.

---

## Available Agents

| Agent | Role | Tier | Mode | Model | Output Location |
|-------|------|------|------|-------|-----------------|
| `ux-behavior-diagnostician` | Fogg B=MAP behavior bottleneck diagnostician | T2 | Convergent | Sonnet | `skills/ux-behavior-design/output/{engagement-id}/ux-behavior-diagnostician-{topic-slug}.md` |

**STUB:** The agent definition file (`skills/ux-behavior-design/agents/ux-behavior-diagnostician.md`) is pending Wave 4 Phase 2 implementation as part of PROJ-022 EPIC-004. The SKILL.md specifies the methodology and output contract that the agent will implement.

**Tool tier:** T2 (Read-Write) = Read, Write, Edit, Glob, Grep, Bash. No WebSearch, WebFetch, or Context7 MCP access -- the B=MAP methodology is self-contained. See `.context/rules/agent-development-standards.md` [Tool Security Tiers].

The agent produces output at three levels per AD-M-004:
- **L0 (Executive Summary):** Primary bottleneck identification (Motivation, Ability, or Prompt); severity assessment; top intervention recommendation; key findings for stakeholders and cross-framework synthesis input.
- **L1 (Technical Detail):** Full B=MAP factor assessment with evidence, simplicity factor breakdown, prompt type classification, bottleneck elimination algorithm trace, and detailed intervention recommendations.
- **L2 (Strategic Implications):** Behavioral pattern analysis across multiple target behaviors, systemic bottleneck trends, organizational behavior design maturity assessment, and behavior change roadmap.

---

## P-003 Compliance

The `/ux-behavior-design` sub-skill contains a single **worker** agent. It is invoked by the `ux-orchestrator` (T5) via the Agent tool. The agent does NOT have Agent tool access and MUST NOT spawn sub-agents.

```
MAIN CONTEXT (user request)
    |
    v
ux-orchestrator (T5, Opus, Integrative) -- parent orchestrator
    |
    +-- ux-behavior-diagnostician (T2, Convergent, Sonnet) -- THIS sub-skill's worker
    +-- [other sub-skill workers...]
```

**Enforcement:**
- `disallowedTools: [Agent]` declared in `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md` frontmatter
- P-003 prohibition in `skills/ux-behavior-design/agents/ux-behavior-diagnostician.governance.yaml` `capabilities.forbidden_actions`
- CI gate validates no sub-skill agent has Agent access (documented in `skills/user-experience/rules/ci-checks.md`)

---

## Invoking the Agent

This is a sub-skill invoked by the `ux-orchestrator`, not directly by users. Users interact with the parent `/user-experience` skill, which routes to this sub-skill based on lifecycle-stage triage.

### Via Natural Language (to parent skill)

```
"Why aren't users completing the checkout process?"
"Diagnose the behavioral bottleneck in our onboarding flow"
"Users see the CTA but don't click it -- what's blocking them?"
"Analyze motivation, ability, and prompts for the signup action"
"Why are users abandoning the form after filling out 3 of 5 fields?"
"What's preventing users from upgrading to the paid plan?"
```

### Via Explicit Agent Request (to parent skill)

```
"Use ux-behavior-diagnostician to diagnose why users abandon the payment form"
"Have ux-behavior-diagnostician analyze B=MAP factors for the onboarding tutorial"
```

### Via Agent Tool (orchestrator internal)

The `ux-orchestrator` invokes the agent via the Agent tool:

```python
Agent(
    description="ux-behavior-diagnostician: B=MAP bottleneck diagnosis for checkout abandonment",
    subagent_type="jerry:ux-behavior-diagnostician",
    prompt="""
## UX CONTEXT (REQUIRED)
- **Engagement ID:** UX-0001
- **Topic:** Checkout Abandonment Bottleneck Diagnosis
- **Product:** [product name and domain]
- **Target Users:** [user description]
- **Target Behavior:** [specific action users should take but are not taking]
- **Current Behavior Data:** [what users are doing instead, abandonment rates, funnel data]
- **Input:** [screenshots, flow descriptions, upstream heuristic findings]

## TASK
Diagnose the behavioral bottleneck preventing users from completing checkout.
1. Define the target behavior in specific, observable terms
2. Assess Motivation factors (intrinsic, extrinsic, social drivers)
3. Assess Ability factors (6 Fogg simplicity factors)
4. Assess Prompt factors (type, timing, placement)
5. Identify the primary bottleneck via elimination algorithm
6. Recommend targeted interventions for the diagnosed bottleneck

## MANDATORY PERSISTENCE (P-002)
Create file at: skills/ux-behavior-design/output/UX-0001/ux-behavior-diagnostician-checkout-abandonment.md
"""
)
```

> **Governance codification (AD-M-007):** The session_context contract (on_receive/on_send) is specified in `ux-behavior-diagnostician.governance.yaml` per AD-M-007. Fields are enumerated below:

**on_receive fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `engagement_id` | string | Yes | UX engagement identifier (format: `UX-{NNNN}`) |
| `product_context` | string | Yes | Product name, domain, and target user description |
| `target_behavior` | string | Yes | Specific, observable action users should take but are not taking (e.g., "click 'Complete Purchase' button on checkout page") |
| `current_behavior_data` | string | No | Observed user behavior: abandonment rates, funnel stage, click data, session recordings summary |
| `upstream_artifacts` | array | No | File paths to upstream handoff artifacts (heuristic evaluation severity-rated findings, screenshots, flow descriptions) |

**on_send fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `bottleneck_factor` | enum | Yes | Primary bottleneck: `motivation`, `ability`, `prompt`, or `multiple` |
| `bottleneck_severity` | enum | Yes | `critical` (never occurs), `major` (rare), `moderate` (inconsistent) |
| `motivation_assessment` | object | Yes | Intrinsic/extrinsic/social scores (1-5 each), overall above/below threshold |
| `ability_assessment` | object | Yes | Six simplicity factor scores (1-5 each), overall above/below threshold |
| `prompt_assessment` | object | Yes | Type (facilitator/signal/spark), timing, placement |
| `interventions` | array | Yes | Interventions with effort estimate and expected impact |
| `synthesis_judgments` | array | Yes | AI judgment calls with confidence classification and rationale |

---

## Methodology

### Fogg Behavior Model: B=MAP

The Fogg Behavior Model (Fogg, 2009, DOI: 10.1145/1541948.1541999; Fogg, 2020) states that **B=MAP**: behavior occurs when Motivation, Ability, and Prompt converge above their respective thresholds at the same moment. If any factor is missing or below the action threshold, the behavior does not occur -- all three factors must be simultaneously sufficient.

The model uses a motivation (Y-axis) vs. ability (X-axis) plane with a curved **action line**. A user with high motivation but high friction falls below the line; a user who finds the action easy but lacks motivation also falls below. The prompt must arrive when the user is above the action line (Fogg, 2009).

### Motivation Analysis

Motivation in the Fogg model operates through three core motivator pairs (Fogg, 2009):

| Motivator Pair | High End | Low End | Assessment Question |
|---------------|----------|---------|---------------------|
| **Sensation** | Pleasure | Pain | Does the action produce immediate pleasure or relieve pain? |
| **Anticipation** | Hope | Fear | Does the user hope for reward or fear consequence? |
| **Belonging** | Acceptance | Rejection | Does the action increase social standing or prevent exclusion? |

**Intrinsic motivators:** Internal drives (satisfaction, curiosity, mastery, autonomy). Durable but difficult to create through design alone (Fogg, 2020).

**Extrinsic motivators:** External incentives (rewards, punishments, progress indicators). Easier to design but less durable; decay when the incentive is removed (Fogg, 2020).

**Social drivers:** Peer influence (competition, collaboration, recognition, social proof). Operate through the belonging motivator pair (Fogg, 2009).

**Motivation assessment scale:** Each motivation dimension (intrinsic, extrinsic, social) is rated 1-5 based on available evidence:
- 1-2: Below threshold (motivation is likely the bottleneck)
- 3: At threshold (borderline; investigate further)
- 4-5: Above threshold (motivation is not the primary bottleneck)

### Ability Analysis: Six Simplicity Factors

Ability in the Fogg model is inversely related to simplicity. The six simplicity factors (Fogg, 2009) represent distinct dimensions of friction that can prevent a user from completing the target behavior:

| Factor | Definition | Assessment Question | Example Friction |
|--------|-----------|---------------------|------------------|
| **Time** | How long the behavior takes to complete | Does the action take more time than the user is willing to spend? | 12-field form when user expects 3 fields |
| **Money** | Financial cost of the behavior | Does the action require spending more money than the user expected? | Surprise shipping costs at checkout |
| **Physical Effort** | Bodily exertion required | Does the action require more physical effort than the user is willing to expend? | Requiring camera access, photo upload, manual data entry on mobile |
| **Brain Cycles** | Cognitive load required | Does the action require more thinking than the user is willing to invest? | Complex pricing tiers requiring comparison; unfamiliar terminology |
| **Social Deviance** | Degree to which the behavior violates social norms | Does the action require the user to do something socially unacceptable in their context? | Publicly sharing salary information; requesting social media permissions |
| **Non-Routine** | Degree to which the behavior departs from the user's established habits | Does the action require the user to change an existing habit or adopt a new workflow? | Switching from email-based workflow to an unfamiliar dashboard |

**Simplicity factor assessment scale:** Each factor is rated 1-5:
- 1-2: High friction (this factor is likely contributing to the bottleneck)
- 3: Moderate friction (borderline; warrants investigation)
- 4-5: Low friction (this factor is not the primary obstacle)

The **limiting simplicity factor** is the factor with the lowest score. Per Fogg (2009), ability is governed by the scarcest resource at the moment of the prompt -- improving any factor except the limiting one does not raise overall ability above the action threshold.

### Prompt Analysis

Prompts are the triggers that call users to action. The Fogg model identifies three prompt types, each appropriate for a specific motivation-ability state (Fogg, 2009):

| Prompt Type | User State | Mechanism | Design Implication |
|-------------|-----------|-----------|-------------------|
| **Spark** | High ability, low motivation | The prompt simultaneously triggers motivation (e.g., emotional appeal, social proof, fear of missing out) | User can do the action but needs a reason; the prompt provides that reason |
| **Facilitator** | High motivation, low ability | The prompt simultaneously reduces friction (e.g., pre-filled forms, one-click actions, simplified steps) | User wants to act but the action is too hard; the prompt makes it easier |
| **Signal** | High motivation, high ability | The prompt serves as a simple reminder or notification (e.g., bell icon, push notification, calendar reminder) | User is both willing and able; they just need a timely nudge |

**Prompt assessment dimensions:**

| Dimension | Assessment | Values |
|-----------|-----------|--------|
| **Type match** | Is the prompt type appropriate for the user's motivation-ability state? | Appropriate (correct type for state), Mismatched (wrong type -- e.g., signal prompt when facilitator is needed) |
| **Timing** | Does the prompt arrive when the user is ready to act? | Appropriate (arrives at the right moment), Mistimed (arrives too early or too late), Absent (no prompt exists) |
| **Placement** | Is the prompt visible and actionable when it fires? | Visible (user notices it), Hidden (below fold, in a submenu), Competing (surrounded by other CTAs that dilute attention) |

### Bottleneck Identification Algorithm

The diagnostician follows a structured elimination algorithm to identify the primary bottleneck:

**Step 1: Prompt Assessment (cheapest fix first)**
- Prompt absent, mistimed, or mismatched -> prompt is the primary bottleneck. A perfect motivation-ability combination produces zero behavior without a prompt (Fogg, 2020).
- Prompt present, timed, and type-appropriate -> proceed to Step 2.

**Step 2: Ability Assessment (most common bottleneck)**
- Calculate the limiting simplicity factor (lowest-scoring among six).
- Limiting factor scores 1-2 -> ability is the primary bottleneck. Ability is the most common bottleneck in digital products (Fogg, 2020).
- All factors score 3+ -> proceed to Step 3.

**Step 3: Motivation Assessment (hardest to change)**
- Majority of motivation dimensions score 1-2 -> motivation is the primary bottleneck.
- Motivation above threshold -> proceed to Step 4.

**Step 4: Multiple Bottleneck Assessment**
- Two or more factors at borderline (score 3) with none clearly below threshold -> classify as `multiple` bottleneck requiring coordinated interventions.

> **Algorithm ordering rationale:** The prompt-first, ability-second, motivation-third ordering follows Fogg's (2020) intervention difficulty gradient: prompts are cheapest to fix, ability is moderate, motivation is hardest.

### Intervention Design Recommendations

Based on the diagnosed bottleneck, the diagnostician recommends interventions targeted at the weakest factor:

| Bottleneck | Intervention Category | Example Interventions | Effort |
|-----------|----------------------|----------------------|--------|
| **Prompt** | Add, reposition, or retype the prompt | Add CTA where none exists; move above fold; change signal to spark for low-motivation users | Low |
| **Ability (Time)** | Reduce time required | Pre-fill fields; reduce steps; add progress indicators; offer express path | Low-Medium |
| **Ability (Money)** | Reduce or clarify cost | Show total upfront; offer free tier; defer payment | Medium |
| **Ability (Physical Effort)** | Reduce physical actions | Add autofill; one-click actions; optimize for mobile | Low-Medium |
| **Ability (Brain Cycles)** | Reduce cognitive load | Simplify language; add defaults; reduce choices; add tooltips | Medium |
| **Ability (Social Deviance)** | Normalize the behavior | Add social proof; anonymization options; privacy controls | Medium |
| **Ability (Non-Routine)** | Reduce habit disruption | Map to existing workflows; familiar UI patterns; transition guides | Medium-High |
| **Motivation** | Increase motivation via design | Social proof; gamification; loss aversion framing; progress visualization | High |
| **Multiple** | Coordinated multi-factor | Address lowest-scoring factor first; combine prompt redesign with simplification | High |

### Execution Phases

> **Note:** This execution procedure describes target behavior for the fully-implemented `ux-behavior-diagnostician` agent. The current agent definition is a Wave 4 stub; full implementation will follow this specification.

The diagnostician follows a 5-phase sequential workflow. Each phase produces intermediate artifacts that feed the next. This mirrors the Phase 1-5 structure established by the HEART metrics, Lean UX, and Atomic Design sub-skills.

#### Phase 1: Scope Definition

**Purpose:** Establish the behavioral context, define the target behavior, confirm wave entry criteria, and catalog available behavioral evidence.

**Activities:**
1. Identify the product domain, target users, and the specific action users should take but are not taking. Define the target behavior using Fogg's statement format: "After [CONTEXT], I will [SPECIFIC BEHAVIOR]" (Fogg, 2020, Chapters 14-15)
2. Confirm Wave 4 entry criteria are met: Wave 3 completed (Storybook with 5+ Atom stories AND 1 Persona Spectrum review), OR bypass condition satisfied (existing user base with analytics). *(Verification: check for `WAVE-3-SIGNOFF.md` in `skills/user-experience/output/`; if absent, ask user per H-31.)*
3. Catalog upstream inputs: check for `/ux-heuristic-eval` severity-rated findings (severity >= 2); if present, import finding IDs for bottleneck context
4. Catalog available behavioral evidence: abandonment rates, funnel data, session recordings, support tickets, interview excerpts. Classify as strong (quantitative), moderate (qualitative), or weak (anecdotal)
5. Establish observation scope: screens, flows, or interaction sequences containing the target behavior; current conversion rate (if known)

**Output:** Scope brief with the following required fields:

| Field | Description | Example |
|-------|-------------|---------|
| Product Domain | Application area and target user segment | "E-commerce checkout flow for first-time buyers" |
| Target Behavior Statement | Fogg format: "After [CONTEXT], I will [SPECIFIC BEHAVIOR]" | "After adding items to cart, I will complete purchase" |
| Observation Scope | Screens, flows, or interaction sequences under analysis | "Cart page through order confirmation (4 screens)" |
| Upstream Findings | Imported heuristic evaluation findings (if available), with finding IDs | "HE-003 (severity 3): unclear CTA placement" |
| Evidence Inventory | Available behavioral evidence classified as strong/moderate/weak | "Strong: 23% cart abandonment rate; Moderate: 3 user interviews; Weak: support ticket anecdotes" |
| Wave Entry Status | Wave 4 criteria verification result | "PASS: WAVE-3-SIGNOFF.md present, 7 Atom stories confirmed" |

#### Phase 2: Behavior Mapping

**Purpose:** Map the current state of each B=MAP factor, establishing a baseline assessment.

**Activities:**
1. Assess Motivation: evaluate each dimension (intrinsic, extrinsic, social) on the 1-5 scale. Cite specific evidence; mark inferences where no direct evidence exists.
2. Assess Ability: evaluate all six simplicity factors (1-5 each). Describe friction points or their absence. Identify the limiting simplicity factor.
3. Assess Prompts: classify by type (Facilitator/Signal/Spark), evaluate timing (appropriate/mistimed/absent) and placement (visible/hidden/competing). Record "prompt absent" if none exists.
4. Plot the user's approximate position on the motivation-ability plane. Describe whether the user is in the action zone and which factor(s) need to change.

**Output:** B=MAP state map: motivation scores, ability scores with limiting factor, prompt assessment, action-line position.

#### Phase 3: Bottleneck Diagnosis

**Purpose:** Apply the bottleneck identification algorithm to determine the primary constraint.

**Activities:**
1. Execute Step 1 (Prompt Assessment): evaluate prompt presence, type, timing, placement. If any criterion fails, classify as prompt bottleneck.
2. Execute Step 2 (Ability Assessment): if prompt is adequate, examine the limiting simplicity factor. If it scores 1-2, classify as ability bottleneck with the specific factor identified and evidence chain.
3. Execute Step 3 (Motivation Assessment): if ability is adequate, evaluate overall motivation. If majority of dimensions score 1-2, classify as motivation bottleneck with evidence.
4. Execute Step 4 (Multiple Bottleneck Assessment): if two or more factors are borderline (score 3), classify as multiple bottleneck.
5. Assign bottleneck severity: critical (zero conversion), major (conversion below 10% of expected), moderate (conversion 10-50% of expected). *(Heuristic thresholds: 10% and 50% are framework-internal heuristics. Adjust based on domain-specific baselines.)*

**Output:** Bottleneck diagnosis: primary factor, severity, evidence chain, algorithm trace, confidence assessment.

#### Phase 4: Intervention Design

**Purpose:** Recommend targeted interventions addressing the diagnosed bottleneck.

**Activities:**
1. Select intervention category based on diagnosed bottleneck (see Intervention Design Recommendations table). For ability bottlenecks, target the specific limiting simplicity factor.
2. Generate 3-5 specific interventions, each with: description, target factor, expected impact (high/medium/low), implementation effort (low/medium/high), and supporting reasoning.
3. Prioritize by effort-to-impact ratio: low-effort, high-impact first. Prompt and ability interventions before motivation interventions (Fogg, 2020).
4. Classify each intervention as direct (addresses primary bottleneck) or supporting (reinforces primary intervention).
5. Mark all intervention recommendations with LOW synthesis confidence per [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence).

**Output:** Prioritized interventions: description, target factor, impact, effort, direct/supporting, confidence (all LOW).

#### Phase 5: Synthesis and Handoff Preparation

**Purpose:** Synthesize findings, produce L0/L1/L2 output artifact, construct downstream handoff.

**Activities:**
1. Produce L0 executive summary: primary bottleneck, severity, top intervention, key findings
2. Produce L1 technical detail: full B=MAP assessment, algorithm trace, intervention list, evidence citations
3. Produce L2 strategic implications: behavioral pattern analysis, systemic trends, maturity assessment, behavior change roadmap
4. Compile Synthesis Judgments Summary: every AI judgment call with confidence classification and rationale
5. Prepare `/ux-heart-metrics` handoff: bottleneck diagnosis with HEART dimension mapping for measurement baseline
6. If CRISIS mode: add priority ranking and quick-win identification (prompt bottlenecks flagged as quick wins per Fogg, 2020)

**Output:** Complete output artifact per the Required Output Sections specification (L0 executive summary, L1 technical sections, L2 strategic implications, synthesis judgments, handoff data). Handoff payload for `/ux-heart-metrics`.

---

## Output Specification

### Output Location

```
skills/ux-behavior-design/output/{engagement-id}/ux-behavior-diagnostician-{topic-slug}.md
```

Where:
- `{engagement-id}` follows the pattern `UX-{NNNN}` (e.g., `UX-0001`)
- `{topic-slug}` is a kebab-case descriptor of the target behavior (e.g., `checkout-abandonment`, `onboarding-completion`, `plan-upgrade`)

### Required Output Sections

| Section | Level | Content |
|---------|-------|---------|
| **Executive Summary** | L0 | Primary bottleneck factor; bottleneck severity; top intervention recommendation; key findings for stakeholders and cross-framework synthesis input |
| **Engagement Context** | L1 | Product description, target users, target behavior statement, available evidence inventory, observation scope, upstream inputs, wave entry verification |
| **Behavior State Map** | L1 | Full B=MAP assessment: motivation scores (intrinsic, extrinsic, social; 1-5 each), ability scores (6 simplicity factors; 1-5 each with limiting factor identified), prompt assessment (type, timing, placement), action-line position |
| **Bottleneck Diagnosis** | L1 | Primary bottleneck factor with elimination algorithm trace; bottleneck severity; evidence chain; confidence assessment |
| **Intervention Recommendations** | L1 | Prioritized interventions (3-5) with: description, target factor, expected impact, implementation effort, direct/supporting classification; all marked LOW confidence |
| **Strategic Implications** | L2 | Behavioral pattern analysis; systemic bottleneck trends; behavior design maturity assessment; behavior change roadmap |
| **Synthesis Judgments Summary** | L1 | Each AI judgment call listed for synthesis confidence gate compliance |
| **Handoff Data** | L1 | Structured data for downstream sub-skills: bottleneck diagnosis with HEART metric mapping (for `/ux-heart-metrics` measurement baseline) |

**Synthesis Judgments Summary requirements:** MUST list every AI judgment (motivation ratings, simplicity scores, bottleneck classification, interventions) with confidence classification (HIGH/MEDIUM/LOW) and rationale. Each judgment row includes: finding ID, framework source (e.g., B=MAP factor, simplicity factor, intervention category), confidence level (HIGH/MEDIUM/LOW), and rationale explaining the classification basis and evidence chain. Follows the pattern in `skills/user-experience/rules/synthesis-validation.md` [STUB: EPIC-001].

### Templates

| Template | Path | Purpose |
|----------|------|---------|
| B=MAP Diagnosis Template | `skills/ux-behavior-design/templates/bmap-diagnosis-template.md` | B=MAP factor assessment with scoring tables, bottleneck algorithm trace, and intervention recommendation format |

---

## Routing

### Trigger Keywords

| Keyword | Routing Context |
|---------|----------------|
| behavior design | Direct match -- primary trigger |
| B=MAP | Direct match |
| Fogg model | Direct match |
| behavior bottleneck | Direct match |
| motivation analysis | In combination with UX/behavior context |
| ability analysis | In combination with UX/behavior context |
| prompt design | In combination with behavior/UX context (not general prompt engineering) |
| why users don't | Direct match (phrase) |
| user inaction | Direct match |
| behavior diagnosis | Direct match |
| tiny habits | In combination with UX/design context |
| action threshold | In combination with behavior/UX context |

### Lifecycle-Stage Routing Integration

This sub-skill is routed to by the `ux-orchestrator` in the following lifecycle-stage scenarios:

| Stage | User Intent | Route Condition |
|-------|-------------|-----------------|
| After launch | "Users not completing action" | Direct route to `/ux-behavior-design`; source: `skills/user-experience/rules/ux-routing-rules.md` Stage Routing Table (pending EPIC-001 completion) |
| After launch | Follow-up from heuristic evaluation | When `/ux-heuristic-eval` has identified severity >= 2 findings with behavioral implications; heuristic findings provide context for bottleneck diagnosis |
| CRISIS | Urgent UX problems (step 2) | CRISIS mode invokes Behavior Design as step 2 of the fixed 3-skill emergency sequence (Heuristic Eval -> **Behavior Design** -> HEART Metrics); source: `skills/user-experience/rules/ux-routing-rules.md` CRISIS Routing (pending EPIC-001 completion) |
| Any stage | "Fix a specific UX problem" (behavioral) | Qualification question: "Is the problem about user behavior or design quality?" -> Behavior: `/ux-behavior-design`; source: `skills/user-experience/rules/ux-routing-rules.md` Common Intent Resolution (pending EPIC-001 completion) |

### Wave Gating

This sub-skill is in **Wave 4** (Advanced Analytics). It requires Wave 3 completion before deployment:

**Entry criteria:** Wave 3: Storybook with 5+ Atom stories AND 1 Persona Spectrum review.

**Bypass condition:** Existing user base with analytics (skip Persona Spectrum prerequisite). This bypass recognizes that teams with an existing user base and analytics data have the behavioral evidence needed for B=MAP diagnosis, even without the Persona Spectrum review that Wave 3 inclusive design would normally provide.

---

## Cross-Framework Integration

### Upstream Inputs

This sub-skill receives context from other sub-skills when invoked as part of a multi-sub-skill workflow:

| From Sub-Skill | Handoff Artifact | Key Fields | Usage |
|----------------|-----------------|-----------|-------|
| `/ux-heuristic-eval` | Severity-rated findings | Finding ID, heuristic violated, severity (0-4), affected screen/flow | Heuristic findings with severity >= 2 provide context for behavioral diagnosis; high-severity findings identify specific UI locations where user behavior breaks down, guiding the B=MAP scope definition |

### Downstream Handoffs

This sub-skill produces artifacts that feed into other sub-skills via the Jerry handoff protocol (`docs/schemas/handoff-v2.schema.json`).

| To Sub-Skill | Handoff Artifact | Key Fields | Trigger |
|-------------|-----------------|-----------|---------|
| `/ux-heart-metrics` | Bottleneck diagnosis with HEART metric mapping | Bottleneck factor, bottleneck severity, affected screen/flow, candidate HEART metric category (Happiness/Engagement/Adoption/Retention/Task Success), intervention list | After bottleneck diagnosis is complete; HEART analyst establishes measurement baselines for the diagnosed bottleneck area |

**Handoff data format (handoff-v2 + ux-ext):**

```yaml
handoff:
  from_agent: ux-behavior-diagnostician
  to_agent: ux-heart-analyst
  task: "Establish HEART metric baselines for diagnosed behavioral bottleneck"
  success_criteria:
    - "Metric baselines established for affected HEART dimension"
    - "Target thresholds set for post-intervention measurement"
  artifacts:
    - "skills/ux-behavior-design/output/{engagement-id}/ux-behavior-diagnostician-{topic-slug}.md"
  key_findings:
    - "Primary bottleneck: {factor} ({severity})"
    - "Limiting simplicity factor: {factor_name} (score: {N}/5)"
  blockers: []
  confidence: 0.6
  criticality: C2
  ux_ext:
    bottleneck_factor: "{motivation|ability|prompt|multiple}"
    bottleneck_severity: "{critical|major|moderate}"
    affected_heart_dimension: "{happiness|engagement|adoption|retention|task_success}"
```

### Canonical Multi-Skill Workflow Sequences

This sub-skill participates in the following canonical sequences:

| Sequence | Skills Involved | This Sub-Skill's Role |
|----------|----------------|-----------------------|
| Evaluate to Diagnose to Measure | `/ux-heuristic-eval` then **`/ux-behavior-design`** then `/ux-heart-metrics` | Receives heuristic findings and traces them to behavioral root causes via B=MAP; hands off bottleneck diagnosis to HEART for measurement |
| CRISIS Emergency Sequence | `/ux-heuristic-eval` then **`/ux-behavior-design`** then `/ux-heart-metrics` | Step 2 of the fixed CRISIS 3-skill sequence; diagnoses behavioral root causes of urgent UX problems |

---

## Synthesis Hypothesis Confidence

Behavior Design outputs include synthesis hypotheses that carry confidence classifications per the synthesis validation protocol.

| Synthesis Step | Typical Confidence | Rationale |
|---------------|-------------------|-----------|
| B=MAP bottleneck diagnosis | MEDIUM | Fogg Behavior Model (Fogg, 2020) provides structured diagnosis but bottleneck attribution requires user-specific data. Framework constrains to three factors, reducing interpretive variance, but scores depend on evidence quality. |
| Design intervention recommendation | LOW | Intervention effectiveness depends on context-specific factors (demographics, domain, constraints) that training data cannot capture. Directionally sound per B=MAP but requires user testing (Fogg, 2020). |

**Gate enforcement:**
- **MEDIUM outputs (bottleneck diagnosis):** Include "Validation Required" section. Recommendations conditional on validation against 2-3 real user data points (interviews, analytics, or session recordings).
- **LOW outputs (intervention recommendations):** Intervention section tagged `[REFERENCE-ONLY]`. Banner: "Intervention recommendations are directional based on B=MAP analysis. Effectiveness requires validation through user testing or A/B experimentation."

**Note on confidence dynamics:** Bottleneck diagnosis can achieve HIGH synthesis confidence when converged with a second framework -- for example, when `/ux-heuristic-eval` identifies severity >= 3 findings corroborating the diagnosed bottleneck. Intervention recommendations remain LOW regardless of diagnostic confidence because effectiveness requires empirical testing.

---

## Quality Gate Integration

Behavior Design outputs are subject to the Jerry quality gate per H-13 and H-14:

| Quality Check | Threshold | Application |
|---------------|-----------|-------------|
| S-014 LLM-as-Judge scoring | >= 0.92 composite (C2+) | Applied at Phase 5 completion |
| Creator-critic-revision | Minimum 3 iterations (H-14) | Orchestrator manages revision cycles |
| Self-review (S-010) | Required before presenting | Self-review before returning to orchestrator |
| Wave transition gate | S-014 composite >= 0.85 | Applied at Wave 4 -> 5 transition |

**Scoring dimensions (Behavior Design interpretation):**

| Dimension | Weight | Interpretation |
|-----------|--------|----------------|
| Completeness | 0.20 | All B=MAP factors assessed; all six simplicity factors rated; prompt analysis included |
| Internal Consistency | 0.20 | Bottleneck diagnosis consistent with factor scores; interventions target diagnosed bottleneck |
| Methodological Rigor | 0.20 | Fogg model correctly applied; elimination algorithm followed; factor ratings evidence-based |
| Evidence Quality | 0.15 | Factor ratings cite evidence; evidence quality classified; inferences labeled |
| Actionability | 0.15 | Interventions specific, implementable, prioritized by effort-to-impact |
| Traceability | 0.10 | Findings trace to evidence; synthesis judgments documented; upstream findings cited |

### CI Gate Summary

The following CI gate criteria apply to this sub-skill (full gate definitions in `skills/user-experience/rules/ci-checks.md`):

| Gate | Check | Enforcement |
|------|-------|-------------|
| **No Agent tool access** | `disallowedTools: [Agent]` present in agent frontmatter; agent MUST NOT have Agent in `tools` list | L5 (CI): grep agent frontmatter for Agent tool presence |
| **P-003 forbidden action** | `capabilities.forbidden_actions` in `.governance.yaml` MUST include P-003 recursive subagent prohibition | L5 (CI): schema validation of governance YAML against `docs/schemas/agent-governance-v1.schema.json` |
| **Output schema validation** | Agent output MUST contain all Required Output Sections (Executive Summary, Engagement Context, Behavior State Map, Bottleneck Diagnosis, Intervention Recommendations, Strategic Implications, Synthesis Judgments Summary, Handoff Data) | L4 (post-tool): section heading presence check on output artifact |

---

## Degraded Mode Behavior

The `ux-behavior-diagnostician` operates at T2 (Read-Write) and does NOT have access to WebSearch, WebFetch, or Context7 MCP tools. Additionally, it operates on user-provided descriptions and artifacts rather than live behavioral analytics. The following degraded modes apply:

### No Real-Time Behavioral Data

When the user cannot provide quantitative behavioral data (analytics, funnel metrics, session recordings):

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| No conversion rate data | Cannot quantify bottleneck severity precisely | Ask for qualitative assessment: "How often does this fail?" Map: "never" = critical, "rarely" = major, "sometimes" = moderate |
| No funnel analytics | Cannot identify exact drop-off point | Ask user to describe the last step before abandonment |
| No session recordings | Cannot observe actual behavior patterns | Ask: (1) "What do users do instead of the target action?" (2) "At what step do users stop? Describe the last thing they do before abandoning." (3) "Have you observed any user confusion or frustration signals (support tickets, rage clicks, dead-end navigation)?" |
| No A/B test data | Cannot validate interventions empirically | Mark all interventions LOW confidence; recommend user testing |

**Degraded mode disclosure (P-022):**
```
[DEGRADED MODE] This output was produced without real-time behavioral analytics data.
Factor assessments are based on user-provided descriptions and available interface artifacts.
Limitations:
- Bottleneck severity estimated from qualitative descriptions, not quantitative data
- Ability factor scores may not reflect actual user friction without session recordings
- Intervention recommendations are directional and require empirical validation
```

### No Upstream Heuristic Evaluation

When invoked without prior `/ux-heuristic-eval` output (e.g., direct invocation rather than CRISIS sequence), the diagnostician performs its own high-level interface assessment based on provided screenshots or descriptions. This is less rigorous than a formal heuristic evaluation. Bottleneck diagnosis references screen locations and behaviors rather than heuristic finding IDs.

### No Screenshots or Design Artifacts

When the user provides only text descriptions without visual references, the diagnostician asks structured questions to compensate: prompt visibility and placement ("Where does the CTA appear? What else is visible around it?") and flow structure ("Describe the step sequence from entry to target action").

---

## Wave Architecture

### Wave 4: Advanced Analytics

This sub-skill is part of Wave 4 (Advanced Analytics), alongside `/ux-kano-model`.

**Entry criteria:** Wave 3 completed -- Storybook with 5+ Atom stories AND 1 Persona Spectrum review.

**Bypass condition:** Existing user base with analytics (skip Persona Spectrum prerequisite). Bypass requires 3-field documentation: unmet criterion, impact assessment ("behavior diagnosis proceeds without inclusive design context"), and remediation plan with target date.

**Wave transition to Wave 5:** Requires 30+ users for Kano survey OR 1 B=MAP bottleneck diagnosed.

---

## Constitutional Compliance

All agents in this sub-skill adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- worker agent, no Agent tool access | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user decisions on bottleneck classification or intervention priorities | Unauthorized action; trust erosion |
| P-022 | NEVER present bottleneck diagnoses as certain without disclosing evidence limitations; NEVER inflate factor scores without supporting evidence; NEVER omit the degraded mode disclosure when operating without behavioral data | Governance undermined; quality assessment invalidated |
| P-001 | NEVER present factor ratings or bottleneck classifications without citing the evidence or reasoning supporting the assessment | Unreliable outputs; unfounded claims propagate downstream |
| P-002 | NEVER leave bottleneck diagnoses or intervention recommendations in transient context only -- persist to files | Context rot vulnerability; artifacts lost on session compaction |

**Per-agent enforcement:** The `ux-behavior-diagnostician` agent declares:
- `constitution.principles_applied`: P-003, P-020, P-022, P-001, P-002 in `skills/ux-behavior-design/agents/ux-behavior-diagnostician.governance.yaml`
- `capabilities.forbidden_actions`: 3 entries in NPT-009 format referencing the constitutional triplet
- `disallowedTools: [Agent]` in `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md` frontmatter

### AI-Augmented Analysis Limitations

The Behavior Design diagnostician agent operates as an AI-augmented analysis tool. The following limitations apply to all outputs and MUST be disclosed per P-022 (no deception):

- **Bottleneck diagnosis is interpretive.** Factor assessment requires judgment. Different analysts may rate the same factors differently. The diagnostician provides structured reasoning but the team should validate against real user behavior.
- **Factor ratings depend on evidence quality.** Quantitative data (analytics, funnels, A/B tests) produces more reliable ratings than qualitative descriptions alone. The diagnostician classifies evidence quality and flags low-evidence assessments.
- **Motivation is the hardest factor to assess remotely.** Motivation involves internal psychological states that users may not articulate. Motivation assessments carry inherently higher uncertainty than ability or prompt assessments.
- **Intervention effectiveness is context-dependent.** All recommendations are directional, not guaranteed. Always validate through user testing or controlled experiments before committing to implementation.
- **The Fogg model simplifies a complex reality.** B=MAP reduces behavior to three factors for analytical tractability. Real behavior is influenced by additional factors (habit strength, environmental context, emotional state) not explicitly captured (Fogg, 2009).

---

## Registration

This sub-skill follows a parent-routed registration model per H-26. Sub-skills are routed through the parent `/user-experience` orchestrator; independent registration would create duplicate triggers (AP-02).

| Registration Point | Status | Detail |
|--------------------|--------|--------|
| `CLAUDE.md` skill table | Registered via parent | `/user-experience` registered; sub-skills not independently listed |
| `mandatory-skill-usage.md` trigger map | Routed via parent | "behavior design" keyword routes to parent, which dispatches here |
| `AGENTS.md` agent registry | Registered | `ux-behavior-diagnostician` listed under User-Experience Skill Agents |
| Parent SKILL.md agent table | Registered | Listed in `skills/user-experience/SKILL.md` [Available Agents] |

---

## Deployment Status

> **Wave 4 Sub-Skill -- Phase 1 Complete, Phase 2 Pending.**
>
> This sub-skill follows a two-phase implementation sequence:
>
> - **Wave 4 Phase 1 (this deliverable):** SKILL.md specification -- methodology, output format, routing integration, template stub, cross-framework integration, and quality gate criteria. This document is the Phase 1 artifact.
> - **Wave 4 Phase 2 (pending):** Agent implementation -- `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md` (agent definition with `<input>`, `<capabilities>`, `<methodology>`, `<output>` sections) and `skills/ux-behavior-design/agents/ux-behavior-diagnostician.governance.yaml` (governance metadata). Tracked under PROJ-022 EPIC-004.

---

## Quick Reference

### Common Workflows

| Need | Command Example |
|------|-----------------|
| Diagnose checkout abandonment | "Why aren't users completing the checkout process?" |
| Analyze onboarding drop-off | "Diagnose the behavioral bottleneck in our onboarding flow" |
| Understand CTA inaction | "Users see the upgrade button but don't click it -- what's blocking them?" |
| B=MAP factor analysis | "Analyze motivation, ability, and prompts for the signup action" |
| Post-launch behavior diagnosis | "Users are abandoning the form after step 3 -- diagnose why" |
| CRISIS behavioral diagnosis | "CRISIS: users are abandoning checkout -- urgent UX triage" (routes to full CRISIS sequence) |

### Agent Selection Hints

| Keywords | Routes To |
|----------|-----------|
| behavior design, B=MAP, Fogg model, behavior bottleneck, motivation analysis, ability analysis, prompt design, user inaction, action threshold, tiny habits | `ux-behavior-diagnostician` |
| heuristic, usability, Nielsen, severity, inspection, evaluation | `/ux-heuristic-eval` (not this sub-skill) |
| HEART, metrics, measurement, GSM, happiness, engagement | `/ux-heart-metrics` (not this sub-skill) |
| lean UX, hypothesis, assumption, experiment, build-measure-learn | `/ux-lean-ux` (not this sub-skill) |
| jobs to be done, JTBD, switch interview, user motivation | `/ux-jtbd` (not this sub-skill) |
| Kano, feature prioritization, must-be, attractive, performance | `/ux-kano-model` (not this sub-skill) |

---

## References

| Source | Content | Path |
|--------|---------|------|
| Parent SKILL.md | Sub-skill scope, wave architecture, routing, MCP dependencies, synthesis protocol | `skills/user-experience/SKILL.md` |
| Agent definition | Agent frontmatter, identity, expertise, guardrails | `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md` [PLANNED] |
| Agent governance | Tool tier, forbidden actions, output validation, constitutional compliance | `skills/ux-behavior-design/agents/ux-behavior-diagnostician.governance.yaml` [PLANNED] |
| UX routing rules | Lifecycle-stage routing, handoff data contracts, common intent resolution, CRISIS routing [PARTIAL: EPIC-001] | `skills/user-experience/rules/ux-routing-rules.md` |
| Synthesis validation | Confidence gate protocol, per-sub-skill confidence map, signal extraction criteria | `skills/user-experience/rules/synthesis-validation.md` [STUB: EPIC-001] |
| Wave progression | Wave 4 entry criteria, signoff requirements | `skills/user-experience/rules/wave-progression.md` |
| CI checks | P-003 enforcement, sub-skill validation gates | `skills/user-experience/rules/ci-checks.md` |
| B=MAP diagnosis template | Factor assessment tables, bottleneck algorithm trace, intervention format | `skills/ux-behavior-design/templates/bmap-diagnosis-template.md` |
| Skill standards | H-25/H-26 skill structure requirements | `.context/rules/skill-standards.md` |
| Agent development standards | H-34 dual-file architecture, tool tiers, handoff protocol | `.context/rules/agent-development-standards.md` |
| Quality enforcement | Quality gate thresholds, criticality levels, strategy catalog | `.context/rules/quality-enforcement.md` |
| Handoff schema | Canonical handoff schema v2 | `docs/schemas/handoff-v2.schema.json` |
| Agent governance schema | Governance YAML validation schema | `docs/schemas/agent-governance-v1.schema.json` |

### Requirements Traceability

| Source | Content | Path |
|--------|---------|------|
| PROJ-022 PLAN.md | Project plan: sub-skill scope, wave assignment, acceptance criteria, implementation phases | `projects/PROJ-022-user-experience-skill/PLAN.md` |
| EPIC-004 (Wave 4 Deployment) | Parent work item for Wave 4 sub-skill implementation including this sub-skill | PROJ-022 EPIC-004 in `projects/PROJ-022-user-experience-skill/WORKTRACKER.md` |
| ORCHESTRATION.yaml | Orchestration plan governing the build sequence for this sub-skill | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |

### External References

| Source | Citation |
|--------|----------|
| Fogg, B.J. (2009) | "A Behavior Model for Persuasive Design." Proceedings of the 4th International Conference on Persuasive Technology (Persuasive '09). Article No. 40. DOI: [10.1145/1541948.1541999](https://doi.org/10.1145/1541948.1541999). Original publication of B=MAP (then B=MAT). Defines motivator pairs, six simplicity factors, and three prompt types. |
| Fogg, B.J. (2020) | "Tiny Habits: The Small Changes That Change Everything." Houghton Mifflin Harcourt. Chapter 3: updated B=MAP with "Prompt" replacing "Trigger" and action line threshold model; Chapters 5-6: intervention difficulty gradient (Starter Step → Scaled Habit); Chapters 14-15: behavior statement format ("After I [anchor], I will [tiny behavior]") and scaling methodology. |
| Eyal, N. (2014) | "Hooked: How to Build Habit-Forming Products." Portfolio/Penguin. Complementary habit formation framework (Hook Model). Referenced for context, not directly applied. |
| Wendel, S. (2020) | "Designing for Behavior Change: Applying Psychology and Behavioral Economics." 2nd ed. O'Reilly. Chapters 5-7: practical design patterns for behavior change interventions targeting ability barriers (simplification strategies) and motivation barriers (framing, social proof, commitment devices). Referenced for intervention design patterns. |
| Fogg, B.J. (n.d.) | "Fogg Behavior Model" (living reference, actively maintained). [https://behaviormodel.org/](https://behaviormodel.org/) (accessed 2026-03-04). Canonical online resource for the B=MAP model, updated factor definitions, and current practitioner guidance. |

---

*Sub-Skill Version: 1.5.0*
*Parent Skill: `/user-experience` v1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Wave: 4 (Advanced Analytics)*
*SSOT: `skills/user-experience/SKILL.md`*
*Project: PROJ-022 User Experience Skill*
*Created: 2026-03-04*
