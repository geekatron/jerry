---
name: user-experience
description: "Parent orchestrator for AI-augmented UX methodology targeting tiny teams (1-5 people). Routes to 10 sub-skills by product lifecycle stage through criteria-gated waves. Invoke when team needs structured UX evaluation, user research, design systems, UX metrics, behavior diagnosis, feature prioritization, design sprints, or AI interaction design. Each sub-skill implements a proven UX framework with synthesis hypothesis confidence gates and MCP design tool integration. Triggers: UX, user experience, usability, heuristic evaluation, JTBD, lean UX, HEART metrics, atomic design, inclusive design, behavior design, Kano model, design sprint, AI-first design, UX audit, accessibility, design system, user research."
version: "1.0.0"
agents:
  - ux-orchestrator
  - ux-heuristic-evaluator
  - ux-jtbd-analyst
  - ux-lean-ux-facilitator
  - ux-heart-analyst
  - ux-atomic-architect
  - ux-inclusive-evaluator
  - ux-behavior-diagnostician
  - ux-kano-analyst
  - ux-sprint-facilitator
  - ux-ai-design-guide
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__memory-keeper__context_save, mcp__memory-keeper__context_get, mcp__memory-keeper__context_search
activation-keywords:
  - "user experience"
  - "UX evaluation"
  - "heuristic evaluation"
  - "jobs to be done"
  - "JTBD"
  - "lean UX"
  - "HEART metrics"
  - "atomic design"
  - "inclusive design"
  - "behavior design"
  - "Kano model"
  - "design sprint"
  - "AI-first design"
  - "usability"
  - "UX audit"
  - "user research"
  - "accessibility"
  - "design system"
  - "UX metrics"
---

<!-- NOTE: activation-keywords (19 entries) intentionally differ from mandatory-skill-usage.md trigger map.
     activation-keywords are SKILL.md-scoped terms for Claude Code agent discovery (H-26).
     The trigger map uses broader/narrower terms with negative keywords for routing disambiguation (H-36b).
     This asymmetry is by design per agent-routing-standards.md Enhanced Trigger Map specification:
     trigger map keywords are routing-optimized; activation-keywords are discovery-optimized. -->

# User-Experience Skill

> **Version:** 1.0.0
> **Framework:** Jerry User-Experience
> **Constitutional Compliance:** Jerry Constitution v1.0
> **SSOT References:** GitHub Issue #138 (Architecture Spec), PROJ-022 PLAN.md, ADR-PROJ007-001 (Agent Definition Format)
> **Project:** PROJ-022 User Experience Skill | GitHub Issue [#138](https://github.com/geekatron/jerry/issues/138)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Document Audience](#document-audience-triple-lens) | Triple-Lens audience guide |
| [Purpose](#purpose) | Skill overview and key capabilities |
| [When to Use This Skill](#when-to-use-this-skill) | Activation triggers and scope boundaries |
| [Available Agents](#available-agents) | 11-agent roster with roles, models, and output locations |
| [P-003 Compliance](#p-003-compliance) | Orchestrator-worker hierarchy diagram |
| [Invoking an Agent](#invoking-an-agent) | Three invocation methods with examples |
| [Wave Architecture](#wave-architecture) | 5-wave criteria-gated deployment model |
| [Lifecycle-Stage Routing](#lifecycle-stage-routing) | Orchestrator triage by product stage |
| [Synthesis Hypothesis Validation](#synthesis-hypothesis-validation) | 3-tier confidence gate protocol |
| [MCP Integration Architecture](#mcp-integration-architecture) | Dependency matrix, cost tiers, fallback paths |
| [Cross-Skill Integration](#cross-skill-integration) | Integration with eng-team, red-team, adversary, orchestration, and others |
| [Constitutional Compliance](#constitutional-compliance) | Governing principles |
| [Quick Reference](#quick-reference) | Common workflows and agent selection hints |
| [References](#references) | Full repo-relative paths to all referenced files |

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | New users, product managers | [Purpose](#purpose), [When to Use This Skill](#when-to-use-this-skill), [Quick Reference](#quick-reference) |
| **L1 (Developer)** | Engineers invoking agents | [Invoking an Agent](#invoking-an-agent), [Available Agents](#available-agents), [Lifecycle-Stage Routing](#lifecycle-stage-routing) |
| **L2 (Architect)** | Workflow designers, skill maintainers | [Wave Architecture](#wave-architecture), [MCP Integration Architecture](#mcp-integration-architecture), [Synthesis Hypothesis Validation](#synthesis-hypothesis-validation) |

---

## Purpose

The User-Experience skill provides AI-augmented UX methodology for tiny teams (1-5 people) through 11 agents (1 orchestrator + 10 framework specialists). Each agent encapsulates a proven UX framework, produces **persistent artifacts** that survive context compaction, enforces methodological rigor via synthesis hypothesis confidence gates, and builds a cumulative product UX knowledge base.

The skill targets teams where UX is a part-time responsibility -- calibrated for 20-50% of one person's time in Waves 1-2, with Waves 3-5 as aspirational progression.

### Key Capabilities

- **Heuristic Evaluation** -- Nielsen's 10 Heuristics with severity-rated findings (Wave 1)
- **Jobs-to-Be-Done Analysis** -- User motivation research, switch interviews, job mapping (Wave 1)
- **Lean UX Facilitation** -- Hypothesis-driven build-measure-learn cycles (Wave 2)
- **HEART Metrics** -- Google's Goals-Signals-Metrics (GSM) framework for UX measurement (Wave 2)
- **Atomic Design** -- Brad Frost's 5-level component taxonomy (Wave 3)
- **Inclusive Design Evaluation** -- WCAG 2.2 compliance and Microsoft Inclusive Design (Wave 3)
- **Behavior Diagnosis** -- Fogg B=MAP bottleneck analysis (Wave 4)
- **Kano Feature Prioritization** -- Must-be / Performance / Attractive classification (Wave 4)
- **Design Sprint Facilitation** -- AJ&Smart Design Sprint 2.0 four-day process (Wave 5)
- **AI-First Interaction Design** -- AI interface patterns and trust calibration (Wave 5, CONDITIONAL)

> **Deployment Status (v1.0.0):** The skill architecture is fully specified but sub-skills deploy incrementally through the wave model. Currently deployed: `ux-orchestrator` (Wave 0 Foundation). Wave 1-5 sub-skill agents are **not yet deployed** — invoking the skill before their wave completes will route to only the currently-available sub-skills. The orchestrator discloses deployment state to users per P-022 and offers the wave bypass mechanism for urgent needs. See [Wave Architecture](#wave-architecture) for the full deployment timeline.

---

## When to Use This Skill

Activate when:

- Evaluating an existing interface against usability heuristics
- Conducting user research to understand motivations (JTBD, switch interviews)
- Designing or validating a Lean UX hypothesis and experiment cycle
- Defining or measuring UX metrics using the HEART framework
- Building or auditing a component library using atomic design principles
- Auditing for accessibility compliance (WCAG 2.2, inclusive design)
- Diagnosing why users fail to take a desired action (Fogg B=MAP)
- Prioritizing features by user satisfaction impact (Kano analysis)
- Running a structured design sprint for rapid prototyping
- Designing AI-powered interfaces or conversational interactions
- Performing a comprehensive multi-framework UX audit (orchestrator routes to 2+ agents)
- Urgent UX triage via crisis mode (3-skill emergency sequence)

Do NOT use for:

- Security-focused code review or threat modeling (use `/eng-team`)
- Systems engineering requirements or V&V (use `/nasa-se`)
- General research without UX focus (use `/problem-solving`)
- Adversarial quality review of deliverables (use `/adversary`)
- Offensive security testing (use `/red-team`)
- Architecture design without user-facing concerns (use `/architecture`)
- Documentation writing (use `/diataxis`)

---

## Available Agents

| Agent | Role | Tier | Mode | Model | Wave | Output Location |
|-------|------|------|------|-------|------|-----------------|
| `ux-orchestrator` | Parent orchestrator: routing, wave gating, cross-framework synthesis | T5 | Integrative | Opus | 0 | `skills/user-experience/output/{engagement-id}/ux-orchestrator-{topic-slug}.md` |
| `ux-heuristic-evaluator` | Nielsen heuristic evaluation specialist | T4 | Systematic | Haiku* | 1 | `skills/ux-heuristic-eval/output/{engagement-id}/ux-heuristic-evaluator-{topic-slug}.md` |
| `ux-jtbd-analyst` | Jobs-to-Be-Done research and analysis | T4 | Divergent | Sonnet | 1 | `skills/ux-jtbd/output/{engagement-id}/ux-jtbd-analyst-{topic-slug}.md` |
| `ux-lean-ux-facilitator` | Lean UX hypothesis and experiment facilitation | T4 | Systematic | Sonnet | 2 | `skills/ux-lean-ux/output/{engagement-id}/ux-lean-ux-facilitator-{topic-slug}.md` |
| `ux-heart-analyst` | HEART metrics framework specialist | T2 | Systematic | Sonnet | 2 | `skills/ux-heart-metrics/output/{engagement-id}/ux-heart-analyst-{topic-slug}.md` |
| `ux-atomic-architect` | Atomic design component taxonomy architect | T4 | Systematic | Sonnet | 3 | `skills/ux-atomic-design/output/{engagement-id}/ux-atomic-architect-{topic-slug}.md` |
| `ux-inclusive-evaluator` | Inclusive design and accessibility auditor | T4 | Systematic | Sonnet | 3 | `skills/ux-inclusive-design/output/{engagement-id}/ux-inclusive-evaluator-{topic-slug}.md` |
| `ux-behavior-diagnostician` | Fogg B=MAP behavior bottleneck diagnosis | T2 | Convergent | Sonnet | 4 | `skills/ux-behavior-design/output/{engagement-id}/ux-behavior-diagnostician-{topic-slug}.md` |
| `ux-kano-analyst` | Kano model feature classification and prioritization | T2 | Convergent | Sonnet | 4 | `skills/ux-kano-model/output/{engagement-id}/ux-kano-analyst-{topic-slug}.md` |
| `ux-sprint-facilitator` | AJ&Smart Design Sprint 2.0 facilitation | T4 | Systematic | Opus | 5 | `skills/ux-design-sprint/output/{engagement-id}/ux-sprint-facilitator-{topic-slug}.md` |
| `ux-ai-design-guide` | AI-first interaction design specialist (CONDITIONAL) | T4 | Divergent | Opus | 5 | `skills/ux-ai-first-design/output/{engagement-id}/ux-ai-design-guide-{topic-slug}.md` |

**Tool tier key:** T2 = Read-Write (Read, Write, Edit, Glob, Grep, Bash); T4 = External (T2 + WebSearch, WebFetch, Context7 MCP, Memory-Keeper); T5 = Orchestration (T4 + Agent). See `agent-development-standards.md` [Tool Security Tiers] for full definitions. All tier assignments follow the principle of least privilege (AR-006) — T2 agents (ux-heart-analyst, ux-behavior-diagnostician, ux-kano-analyst) operate on user-provided data only; T4 agents access external UX standards and documentation.

*Haiku for high-volume checklist evaluation; escalates to Sonnet when: (1) heuristic severity is "critical" (>= 3 critical findings), (2) Figma MCP benchmark fails pre-launch threshold, or (3) evaluation spans > 50 screens. Escalation is automatic within the orchestrator's routing logic per AD-M-009 model selection justification.

All agents produce output at three levels per AD-M-004:
- **L0 (Executive Summary):** Key findings in 3-5 bullets for stakeholders and cross-framework synthesis.
- **L1 (Technical Detail):** Full methodology execution with evidence, design recommendations, and component specifications.
- **L2 (Strategic Implications):** Cross-product patterns, organizational UX recommendations, and design evolution trajectory.

---

## P-003 Compliance

The `/user-experience` skill enforces strict single-level nesting per H-01/P-003. Only `ux-orchestrator` has Agent tool access. All 10 sub-skill agents are workers that MUST NOT include Agent in their tool list.

```
MAIN CONTEXT (user request)
    |
    v
ux-orchestrator (T5, Opus, Integrative) -- routes, gates, synthesizes
    |
    +-- ux-heuristic-evaluator    (T4, Systematic, Haiku)     [Wave 1]
    +-- ux-jtbd-analyst           (T4, Divergent, Sonnet)     [Wave 1]
    +-- ux-lean-ux-facilitator    (T4, Systematic, Sonnet)    [Wave 2]
    +-- ux-heart-analyst          (T2, Systematic, Sonnet)    [Wave 2]
    +-- ux-atomic-architect       (T4, Systematic, Sonnet)    [Wave 3]
    +-- ux-inclusive-evaluator    (T4, Systematic, Sonnet)    [Wave 3]
    +-- ux-behavior-diagnostician (T2, Convergent, Sonnet)    [Wave 4]
    +-- ux-kano-analyst           (T2, Convergent, Sonnet)    [Wave 4]
    +-- ux-sprint-facilitator     (T4, Systematic, Opus)      [Wave 5]
    +-- ux-ai-design-guide        (T4, Divergent, Opus)       [Wave 5 COND]
```

**Enforcement:** Sub-skill agents declare `disallowedTools: [Agent]` in `.md` frontmatter. CI gate validates no sub-skill agent has Agent access (documented in `skills/user-experience/rules/ci-checks.md`). Each `.governance.yaml` includes Agent prohibition in `capabilities.forbidden_actions` with P-003 consequence statement.

---

## Invoking an Agent

### Option 1: Natural Language Request

Describe your UX need; the orchestrator routes to the appropriate agent:

```
"Evaluate this dashboard design against Nielsen's heuristics"
"Map the jobs to be done for our onboarding flow"
"Set up a Lean UX experiment for the new search feature"
"Define HEART metrics for the checkout experience"
"Audit this form for WCAG 2.2 AA compliance"
"Run a design sprint for the new mobile navigation"
"Comprehensive UX audit of the settings page"
"CRISIS: users are abandoning checkout -- urgent UX triage"
```

### Option 2: Explicit Agent Request

Request a specific agent by name:

```
"Use ux-heuristic-evaluator to audit the navigation patterns"
"Have ux-kano-analyst classify our backlog features"
"I need ux-inclusive-evaluator to review color contrast and screen reader compatibility"
```

### Option 3: Native Agent Invocation (Agent Tool)

The orchestrator invokes sub-skill agents as named subagents via Agent:

```python
Agent(
    description="ux-heuristic-evaluator: Heuristic evaluation of settings page",
    subagent_type="ux-heuristic-evaluator",
    prompt="""
## UX CONTEXT (REQUIRED)
- **Engagement ID:** UX-0001
- **Topic:** Settings Page Heuristic Evaluation
- **Product:** [product name and domain]
- **Target Users:** [user description]

## TASK
Perform a Nielsen heuristic evaluation of the settings page.
Evaluate all 10 heuristics. Rate severity 0-4 for each finding.
Produce ranked findings with remediation recommendations.
"""
)
```

Claude Code enforces each agent's `tools` frontmatter -- worker agents only have access to their declared tool tier (T2 or T4).

---

## Wave Architecture

Sub-skills deploy in 5 criteria-gated waves. Waves are **deployment phases** for incremental skill build-out, not runtime execution order. At runtime, the orchestrator routes to any deployed sub-skill based on user need.

### Wave Definitions

| Wave | Name | Sub-Skills | Entry Criteria | Bypass Condition |
|------|------|-----------|----------------|-----------------|
| **0** | Foundation | `ux-orchestrator` + rules + templates | PROJ-022 plan approved | N/A |
| **1** | Zero-Dependency | `/ux-heuristic-eval`, `/ux-jtbd` | KICKOFF-SIGNOFF.md completed with MCP ownership assignments | N/A (first wave) |
| **2** | Data-Ready | `/ux-lean-ux`, `/ux-heart-metrics` | Wave 1: at least 1 heuristic eval completed AND 1 JTBD job statement used in a product decision | 2 sprint cycles elapsed with no Wave 1 completion; documented rationale |
| **3** | Design System | `/ux-atomic-design`, `/ux-inclusive-design` | Wave 2: launched product with analytics OR 1 completed Lean UX hypothesis cycle | Storybook already in use (skip Lean UX prerequisite for Atomic Design) |
| **4** | Advanced Analytics | `/ux-behavior-design`, `/ux-kano-model` | Wave 3: Storybook with 5+ Atom stories AND 1 Persona Spectrum review | Existing user base with analytics (skip Persona Spectrum prerequisite) |
| **5** | Process Intensives | `/ux-design-sprint`, `/ux-ai-first-design` (COND) | Wave 4: 30+ users for Kano survey OR 1 B=MAP bottleneck diagnosed; AI-First: Enabler DONE + WSM >= 7.80 | Design Sprint can proceed without Kano prerequisite if team has existing user research |

> **Design Sprint early-access note:** Design Sprint is placed in Wave 5 because it requires facilitation infrastructure (Figma + Miro REQ MCPs) and benefits from prior framework exposure. However, teams at product inception ("don't know what to build") who need Design Sprint immediately can use the wave bypass mechanism (3-field documentation: unmet criterion = "no prior wave completion", impact assessment = "sprint proceeds without prior framework calibration", remediation = "backfill Wave 1-2 sub-skills post-sprint"). The lifecycle-stage router handles this: the "Before design: Need validated prototype" route maps to `/ux-design-sprint` regardless of wave state — the orchestrator presents the bypass prompt if Wave 5 is not yet deployed. This ensures P-020 compliance: the user decides whether to proceed with bypass, not the system.

### Wave Transition Quality Gates

Each wave transition is a quality checkpoint. The orchestrator checks `WAVE-{N}-SIGNOFF.md` existence before routing to Wave N+1 sub-skills.

| Transition | Quality Check | Threshold |
|-----------|---------------|-----------|
| Wave 0 to 1 | KICKOFF-SIGNOFF.md completeness | All fields populated (pass/fail) |
| Wave 1 to 2 | Wave 1 deliverables quality scoring | S-014 composite >= 0.85 on heuristic eval report |
| Wave 2 to 3 | Wave 2 deliverables + usage evidence | S-014 composite >= 0.85 + documented usage artifact |
| Wave 3 to 4 | Wave 3 deliverables + Storybook artifact | S-014 composite >= 0.85 + Storybook story count verification |
| Wave 4 to 5 | Wave 4 deliverables + user data evidence | S-014 composite >= 0.85 + user count or behavioral data artifact |

> **Threshold justification (0.85 vs H-13 0.92):** Wave transition gates assess sub-skill *deployment readiness* — whether a sub-skill produces useful output for end users. This is distinct from H-13's 0.92 threshold, which governs C2+ *deliverable quality* (agent definitions, rule files, governance artifacts). The 0.85 threshold reflects that wave gates evaluate operational output quality rather than governance artifact quality. Formal threshold derivation is tracked in `ADR-PROJ022-002-wave-criteria-gates.md` (pending); the threshold may be revised upward as calibration data from Wave 1 deployments becomes available.

**Wave bypass:** Requires 3-field documentation (unmet criterion, impact assessment, remediation plan with target date). Bypass state produces a warning banner on all sub-skill outputs from the bypassed wave. **Cumulative ceiling:** Maximum 2 concurrent bypasses per team. If a team has 2 active bypasses, the orchestrator requires remediation of at least one before granting additional bypasses. This prevents accumulation of technical UX debt through unbounded wave skipping.

### Wave Signoff Enforcement

- `WAVE-N-SIGNOFF.md` is a closure deliverable -- wave completion is not recognized until the signoff file passes schema validation (all required fields non-empty) and is committed to the repository
- Wave transitions tracked via `/worktracker` entities
- Templates provided: `skills/user-experience/templates/kickoff-signoff-template.md`, `skills/user-experience/templates/wave-signoff-template.md`

---

## Lifecycle-Stage Routing

The orchestrator routes requests through a multi-stage triage based on product lifecycle stage:

```
1. ONBOARD: Display HIGH RISK user research warning (first invocation per session)
2. CAPACITY CHECK: Ask team UX time allocation
   -> If < 20% of one person's time: recommend Wave 1 sub-skills only (P-020: user decides)
3. MCP CHECK: Detect MCP availability
   -> If MCP unavailable: route to non-MCP fallback paths
4. STAGE TRIAGE: Route by product stage
   |
   +-- "Before design: Don't know what to build"     -> /ux-jtbd
   +-- "Before design: Need to prioritize features"   -> /ux-kano-model
   +-- "Before design: Need validated prototype"        -> /ux-design-sprint
   +-- "During design: Iterating on existing design"   -> /ux-lean-ux OR /ux-heuristic-eval
   +-- "During design: Building component system"      -> /ux-atomic-design
   +-- "During design: Building AI product"            -> /ux-ai-first-design (if Enabler DONE)
   |                                                     OR /ux-heuristic-eval + PAIR (interim)
   +-- "After launch: Measure UX health"               -> /ux-heart-metrics
   +-- "After launch: Users not completing action"     -> /ux-behavior-design
   +-- "Any stage: Check accessibility"                -> /ux-inclusive-design
   +-- "CRISIS: Urgent UX problems"                    -> Emergency 3-skill sequence:
                                                          Heuristic Eval -> Behavior Design -> HEART
```

**Dispatch logic:** The orchestrator implements lifecycle-stage routing as a 4-step sequential triage within its `<methodology>` section. Each step is deterministic: (1) ONBOARD fires once per session via session state flag, (2) CAPACITY CHECK uses a single structured question per P-020, (3) MCP CHECK probes Context7 availability via a lightweight resolve call, (4) STAGE TRIAGE matches user intent against the route table above. If STAGE TRIAGE produces multiple matches (e.g., "iterate on our accessible checkout"), the orchestrator applies the ordering protocol from `agent-routing-standards.md` [Multi-Skill Combination]: content before quality, work before presentation. If ambiguity remains after ordering, the orchestrator asks the user per H-31 rather than guessing. The CRISIS path bypasses normal triage and executes a fixed 3-skill sequence; the user confirms entry into CRISIS mode but does not select individual sub-skills (P-020 compliance: user authorizes the emergency sequence, orchestrator selects the fixed route). Full CRISIS mode behavior will be specified in the ux-orchestrator agent `<methodology>` section (EPIC-001).

### Common Intent-to-Route Resolution

| User Says | Routes To | Qualification Question |
|-----------|----------|----------------------|
| "Improve my UX" / "Make this more usable" | Heuristic Eval (existing design) or Design Sprint (no design yet) | "Do you have an existing design?" |
| "Fix a specific UX problem" | Behavior Design (behavioral) or Heuristic Eval (design-level) | "Is the problem about user behavior or design quality?" |
| "Decide what to build" | JTBD (strategic) or Kano (prioritize known features) | "Are you defining the problem or prioritizing features?" |
| "Measure whether UX is working" | HEART Metrics | No qualification needed |
| "Make this accessible" | Inclusive Design | No qualification needed |
| "CRISIS: urgent UX problems" | Emergency 3-skill sequence | No qualification needed |

Routing logic is documented in `skills/user-experience/rules/ux-routing-rules.md`.

---

## Synthesis Hypothesis Validation

Multiple sub-skills produce AI-generated abstractions ("synthesis hypotheses") that may reflect training data biases rather than the team's specific users. A 3-tier confidence gate fires at skill invocation time.

### Confidence Gate Protocol

| Confidence | Gate Behavior | Advancement Rule |
|------------|--------------|-----------------|
| **HIGH** | User reviews output + acknowledges specific AI judgment calls via Synthesis Judgments Summary | Advances to design decisions after enumerated acknowledgment |
| **MEDIUM** | Requires expert review OR validation against 2-3 real user data points | Cannot advance to design decisions without named validation source |
| **LOW** | Output permanently labeled reference-only; design recommendation section structurally omitted | Cannot be overridden by any user action |

### Sub-Skill Synthesis Output Map

| Sub-Skill | Synthesis Step | Typical Confidence |
|-----------|---------------|-------------------|
| `/ux-jtbd` | Job statement synthesis from secondary research | MEDIUM |
| `/ux-lean-ux` | Assumption mapping; hypothesis generation | MEDIUM |
| `/ux-design-sprint` | Day 4 interview thematic analysis | HIGH |
| `/ux-design-sprint` | Day 2 sketch selection rationale | MEDIUM |
| `/ux-inclusive-design` | Persona Spectrum customization | MEDIUM |
| `/ux-kano-model` | Directional classification (5-8 respondents) | MEDIUM |
| `/ux-kano-model` | Feature priority conflict interpretation | LOW |
| `/ux-behavior-design` | B=MAP bottleneck diagnosis | MEDIUM |
| `/ux-behavior-design` | Design intervention recommendation | LOW |
| `/ux-heart-metrics` | Goal-metric mapping interpretation | MEDIUM |
| `/ux-heart-metrics` | Metric threshold recommendation | LOW |
| `/ux-ai-first-design` | AI interaction pattern recommendations | LOW |

### Gate Enforcement

- **HIGH:** Output includes a "Synthesis Judgments Summary" listing each AI judgment call. Acknowledgment prompt required before design recommendations are generated.
- **MEDIUM:** Output includes a "Validation Required" section with placeholder for named validation source (expert name, user data reference, or study citation). Design recommendations withheld until validation is provided.
- **LOW:** Output template structurally omits the design recommendation section. Tagged with `[REFERENCE-ONLY]` in title. Notice: "This output reflects AI synthesis from training data. It does not contain design recommendations."

Full protocol documented in `skills/user-experience/rules/synthesis-validation.md`.

### Cross-Framework Synthesis Protocol

When the orchestrator invokes multiple sub-skills for the same engagement (e.g., Heuristic Eval + HEART Metrics for a post-launch UX assessment), it produces a cross-framework synthesis after all sub-skill outputs are available:

**Trigger:** Two or more sub-skill outputs exist for the same engagement ID.

**Mechanism (4-step sequential):**

1. **Signal Extraction:** The orchestrator reads each sub-skill output's findings/recommendations sections and extracts actionable signals (findings rated severity >= 2 for heuristic eval; metrics below target for HEART; unvalidated assumptions for Lean UX; etc.).
2. **Convergence Detection:** Signals from different frameworks that point to the same UX problem are grouped. Convergent signals (2+ frameworks identify the same issue) receive HIGH synthesis confidence. Single-framework signals receive MEDIUM.
3. **Contradiction Identification:** Signals from different frameworks that recommend opposing actions are flagged as contradictions. Contradictions always receive LOW synthesis confidence with both positions presented and no resolution attempted — the user decides (P-020).
4. **Unified Output:** A synthesis report is produced with three sections: (a) Convergent Findings (HIGH confidence), (b) Single-Framework Findings (MEDIUM), (c) Contradictions (LOW, user decision required). Each finding traces back to its source sub-skill output by engagement ID and finding number.

**Output location:** `skills/user-experience/output/{engagement-id}/ux-orchestrator-synthesis.md`

**Failure mode:** If synthesis confidence is LOW across > 50% of findings, the orchestrator adds a banner: "Cross-framework synthesis produced mostly low-confidence results. Consider validating individual sub-skill outputs independently before acting on synthesis recommendations." This is a P-022 compliance mechanism — the orchestrator does not overstate the value of synthesis when evidence is weak.

**Scope limitation (v1.0.0):** Cross-framework synthesis operates on textual output from sub-skills. It does not access MCP design artifacts directly — synthesis inputs are the sub-skill reports, not raw Figma/Miro data. Future versions may add MCP-aware synthesis if usage patterns warrant it.

---

## MCP Integration Architecture

### Sub-Skill MCP Dependency Matrix

| Sub-Skill | Figma | Miro | Storybook | Zeroheight | Hotjar (Bridge) | Whimsical |
|-----------|-------|------|-----------|------------|-----------------|-----------|
| `/ux-heuristic-eval` | **REQ** | -- | ENH | -- | -- | -- |
| `/ux-jtbd` | -- | ENH | -- | -- | -- | -- |
| `/ux-lean-ux` | ENH | **REQ** | -- | -- | ENH | -- |
| `/ux-heart-metrics` | -- | -- | -- | -- | ENH | -- |
| `/ux-atomic-design` | ENH | -- | **REQ** | ENH | -- | -- |
| `/ux-inclusive-design` | **REQ** | -- | ENH | -- | -- | -- |
| `/ux-behavior-design` | -- | ENH | -- | -- | ENH | -- |
| `/ux-kano-model` | -- | ENH | -- | -- | -- | -- |
| `/ux-design-sprint` | **REQ** | **REQ** | -- | -- | -- | ENH |
| `/ux-ai-first-design` | **REQ** | -- | ENH | -- | -- | -- |

**REQ** = Required (degraded mode + explicit error on failure). **ENH** = Enhancement (cosmetic limitation on failure).

### Figma Dependency Risk Profile

Figma is the highest-risk MCP dependency: 4 sub-skills require it, 2 are enhanced by it (6 of 10 total connections).

| Sub-Skill | Non-Figma Fallback |
|-----------|-------------------|
| `/ux-heuristic-eval` | Screenshot-input mode: user provides design screenshots as image inputs |
| `/ux-design-sprint` | Miro-only mode: sprint exercises in Miro; manual prototype reference |
| `/ux-inclusive-design` | Screenshot-input mode: manual component screenshots for evaluation |
| `/ux-ai-first-design` | Manual design description: text-based interaction pattern analysis |

### Cost Tiers

| Tier | Monthly Cost | Sub-Skills Available |
|------|-------------|---------------------|
| **Free** | $0 | HEART, JTBD, Kano, Behavior Design (+ Storybook for Atomic Design) |
| **Minimal** | ~$46 | + Heuristic Eval, Design Sprint, Lean UX, Inclusive Design, AI-First Design |
| **Full Enhancement** | ~$145-245 | All 10 with full enhancement MCPs |

### Current Jerry MCP Integration

| MCP Tool | Usage | Agents |
|----------|-------|--------|
| Context7 (resolve-library-id) | Resolve UX framework libraries and design system packages | ux-atomic-architect, ux-ai-design-guide, ux-sprint-facilitator |
| Context7 (query-docs) | Query component library documentation, accessibility API docs | ux-atomic-architect, ux-inclusive-evaluator, ux-ai-design-guide, ux-sprint-facilitator |

### Fallback: Text-Only Mode

When MCP tools are unavailable, all agents operate in text-only mode: users provide design descriptions, screenshots, or markup instead of live design artifacts. The agent methodology remains identical; only the input modality changes. Agents MUST note "text-only mode -- no live design artifact access" in their output.

MCP coordination registry documented in `skills/user-experience/rules/mcp-coordination.md`.

---

## Cross-Skill Integration

### Integration Matrix

| Jerry Skill | Integration Type | Direction | Details |
|-------------|-----------------|-----------|---------|
| `/problem-solving` | Research support | Upstream | `ps-researcher` provides market research for JTBD competitive job analysis; `ps-analyst` supports Kano survey data interpretation |
| `/adversary` | Quality enforcement | Applied to outputs | S-014 quality scoring on UX deliverables at wave transitions; full adversarial critique for C2+ artifacts per H-13/H-14 |
| `/worktracker` | Operational tracking | Infrastructure | Tracks UX work items: sub-skill stories, wave transition tasks, Enabler status |
| `/orchestration` | Workflow coordination | Coordinates sub-skills | Manages multi-framework workflows; barrier-sync between sub-skills |
| `/nasa-se` | Requirements handoff | Downstream | UX requirements from JTBD job statements and heuristic findings feed into technical requirements and V&V criteria |
| `/diataxis` | Documentation method | Complementary | Component documentation (from Atomic Design) and design system guides use Diataxis methodology |
| `/eng-team` | Security integration | Complementary | Inclusive design findings feed into eng-security accessibility review; component taxonomy informs secure frontend patterns |
| `/ast` | Entity validation | Infrastructure | Worktracker entities for UX work items validated via AST-based frontmatter extraction (H-33) |

### Canonical Multi-Skill Workflow Sequences

| Sequence | Skills Involved | Use Case |
|----------|----------------|----------|
| Discovery to Sprint | `/ux-jtbd` then `/ux-design-sprint` | JTBD job statement feeds Design Sprint challenge statement |
| Sprint to Iterate to Measure | `/ux-design-sprint` then `/ux-lean-ux` then `/ux-heart-metrics` | Sprint produces prototype; Lean UX iterates; HEART measures |
| Evaluate to Diagnose to Measure | `/ux-heuristic-eval` then `/ux-behavior-design` then `/ux-heart-metrics` | Crisis mode for urgent UX problems |
| Build to Evaluate | `/ux-atomic-design` then `/ux-inclusive-design` | Build components, then evaluate accessibility |
| Discover to Prioritize | `/ux-jtbd` then `/ux-kano-model` | Discover jobs, then prioritize features |

### Cross-Sub-Skill Handoff Data

Handoffs use the Jerry handoff protocol (schema specified in `agent-development-standards.md` [Handoff Protocol]; canonical path `docs/schemas/handoff-v2.schema.json`, pending file creation) with UX-specific artifact types:

| From | To | Handoff Artifact |
|------|-----|-----------------|
| `/ux-jtbd` | `/ux-design-sprint` | Job statement + switch forces |
| `/ux-jtbd` | `/ux-kano-model` | Job-derived feature list |
| `/ux-design-sprint` | `/ux-lean-ux` | Validated prototype + Day 4 findings |
| `/ux-heuristic-eval` | `/ux-behavior-design` | Severity-rated findings |
| `/ux-atomic-design` | `/ux-inclusive-design` | Component inventory with Storybook references |
| `/ux-lean-ux` | `/ux-heart-metrics` | Validated/invalidated hypothesis backlog |

Handoff schema documented in `skills/user-experience/rules/ux-routing-rules.md` [PARTIAL: EPIC-001 — routing table populated with stage mappings, qualification questions, and common intent resolution; full handoff schema pending].

---

## Constitutional Compliance

All agents adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- max 1 level | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user intent -- ask before destructive ops | Unauthorized action; trust erosion |
| P-022 | NEVER deceive about actions, capabilities, or confidence | Governance undermined; quality assessment invalidated |
| P-001 | NEVER present findings without evidence or source citations | Unreliable outputs; unfounded claims propagate downstream |
| P-002 | NEVER leave outputs in transient context only -- persist to files | Context rot vulnerability; artifacts lost on session compaction |
| P-004 | NEVER omit reasoning provenance or source documentation | Untraceable decisions; audit trail broken |
| P-011 | NEVER make recommendations without supporting evidence | Unsupported recommendations; confidence inflated without basis |

**Per-agent enforcement:** Every agent (orchestrator + 10 sub-skill agents) declares in `.governance.yaml`:
- `constitution.principles_applied`: P-003, P-020, P-022 (minimum; additional principles per agent)
- `capabilities.forbidden_actions`: Minimum 3 entries in NPT-009 format referencing the constitutional triplet
- Sub-skill agents: `disallowedTools: [Agent]` in `.md` frontmatter (P-003 enforcement)
- Domain-specific forbidden actions added per agent role

---

## Quick Reference

### Common Workflows

| Need | Agent | Command Example |
|------|-------|-----------------|
| Usability audit | ux-heuristic-evaluator | "Evaluate this dashboard against Nielsen's 10 heuristics" |
| User motivation research | ux-jtbd-analyst | "Map the jobs to be done for onboarding" |
| Experiment design | ux-lean-ux-facilitator | "Create a Lean UX hypothesis for the new search feature" |
| UX metrics definition | ux-heart-analyst | "Define HEART metrics for the checkout flow" |
| Component taxonomy | ux-atomic-architect | "Build an atomic design inventory for the form components" |
| Accessibility audit | ux-inclusive-evaluator | "Audit this page for WCAG 2.2 AA compliance" |
| Behavior diagnosis | ux-behavior-diagnostician | "Diagnose why users abandon signup using Fogg B=MAP" |
| Feature prioritization | ux-kano-analyst | "Classify these backlog features using Kano analysis" |
| Rapid prototyping | ux-sprint-facilitator | "Facilitate a design sprint for the mobile navigation redesign" |
| AI interaction design | ux-ai-design-guide | "Design the conversational UX for the AI assistant feature" |
| Comprehensive audit | ux-orchestrator | "Full UX audit of the settings experience" |
| Urgent triage | ux-orchestrator | "CRISIS: users are abandoning checkout" |

### Agent Selection Hints

| Keywords | Likely Agent |
|----------|--------------|
| heuristic, usability, Nielsen, severity, inspection, evaluation, interface review | ux-heuristic-evaluator |
| jobs to be done, JTBD, switch interview, outcome, motivation, hiring criteria, user jobs | ux-jtbd-analyst |
| lean UX, hypothesis, experiment, MVP, validated learning, assumption, build-measure-learn | ux-lean-ux-facilitator |
| HEART, metrics, happiness, engagement, adoption, retention, task success, GSM, measurement | ux-heart-analyst |
| atomic design, atoms, molecules, organisms, components, design tokens, design system | ux-atomic-architect |
| accessibility, WCAG, ARIA, screen reader, contrast, cognitive load, inclusive, a11y | ux-inclusive-evaluator |
| behavior, Fogg, B=MAP, motivation, ability, prompt, trigger, nudge, behavioral bottleneck | ux-behavior-diagnostician |
| Kano, must-be, attractive, one-dimensional, satisfaction, feature classification, delighter | ux-kano-analyst |
| design sprint, map, sketch, decide, prototype, test, GV sprint, rapid validation | ux-sprint-facilitator |
| AI design, conversational UX, prompt design, trust calibration, AI-first, LLM interface, agentic | ux-ai-design-guide |

### Routing Disambiguation

| Condition | Use Instead | Why |
|-----------|-------------|-----|
| Security-focused review or threat modeling | `/eng-team` | UX methodology produces usability findings, not threat models |
| Adversarial quality review or tournament | `/adversary` | UX agents evaluate design quality, not deliverable quality |
| General research without UX focus | `/problem-solving` | 11 UX agents loaded when task requires general methodology |
| Systems engineering or V&V | `/nasa-se` | UX produces user-centered requirements, not system-level V&V |
| Offensive security testing | `/red-team` | UX methodology produces usability reports, not penetration findings |

---

## References

### Agent Definition Files

> **Status key:** `Exists (stub)` = stub file created with frontmatter and minimal sections. `[PLANNED: Wave N]` = file not yet created; created during that wave's implementation in PROJ-022.

| Agent | Definition | Governance | Status |
|-------|-----------|------------|--------|
| ux-orchestrator | `skills/user-experience/agents/ux-orchestrator.md` | `skills/user-experience/agents/ux-orchestrator.governance.yaml` | Exists (stub) |
| ux-heuristic-evaluator | `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md` | `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.governance.yaml` | Exists (stub) |
| ux-jtbd-analyst | `skills/ux-jtbd/agents/ux-jtbd-analyst.md` | `skills/ux-jtbd/agents/ux-jtbd-analyst.governance.yaml` | Exists (stub) |
| ux-lean-ux-facilitator | `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md` | `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.governance.yaml` | [PLANNED: Wave 2] |
| ux-heart-analyst | `skills/ux-heart-metrics/agents/ux-heart-analyst.md` | `skills/ux-heart-metrics/agents/ux-heart-analyst.governance.yaml` | [PLANNED: Wave 2] |
| ux-atomic-architect | `skills/ux-atomic-design/agents/ux-atomic-architect.md` | `skills/ux-atomic-design/agents/ux-atomic-architect.governance.yaml` | [PLANNED: Wave 3] |
| ux-inclusive-evaluator | `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` | `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.governance.yaml` | [PLANNED: Wave 3] |
| ux-behavior-diagnostician | `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md` | `skills/ux-behavior-design/agents/ux-behavior-diagnostician.governance.yaml` | [PLANNED: Wave 4] |
| ux-kano-analyst | `skills/ux-kano-model/agents/ux-kano-analyst.md` | `skills/ux-kano-model/agents/ux-kano-analyst.governance.yaml` | [PLANNED: Wave 4] |
| ux-sprint-facilitator | `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` | `skills/ux-design-sprint/agents/ux-sprint-facilitator.governance.yaml` | [PLANNED: Wave 5] |
| ux-ai-design-guide | `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` | `skills/ux-ai-first-design/agents/ux-ai-design-guide.governance.yaml` | [PLANNED: Wave 5] |

### Rule Files

> Rule files are [STUB: EPIC-001 Foundation] — stub files created during PROJ-022 Foundation phase with section structure and TODO markers. Full implementation in EPIC-001.

| Rule File | Purpose | Status |
|-----------|---------|--------|
| `skills/user-experience/rules/ux-routing-rules.md` | Lifecycle-stage triage logic, cross-sub-skill handoff schema | [PARTIAL: EPIC-001] |
| `skills/user-experience/rules/synthesis-validation.md` | 3-tier synthesis hypothesis confidence gates | [STUB: EPIC-001] |
| `skills/user-experience/rules/wave-progression.md` | Wave state tracking and ABANDON log | [STUB: EPIC-001] |
| `skills/user-experience/rules/mcp-coordination.md` | MCP server coordination registry, maintenance owner | [STUB: EPIC-001] |
| `skills/user-experience/rules/ci-checks.md` | CI test gate specifications (P-003 enforcement) | [STUB: EPIC-001] |
| `skills/user-experience/rules/metrics-plan.md` | Post-launch metrics measurement plan | [PLANNED: EPIC-008] |

### Templates

> Template files are [STUB: EPIC-001 Foundation] — stub files created during PROJ-022 Foundation phase with template structure. Full implementation in EPIC-001.

| Template | Purpose | Status |
|----------|---------|--------|
| `skills/user-experience/templates/kickoff-signoff-template.md` | KICKOFF-SIGNOFF.md for Wave 0 to 1 transition | [STUB: EPIC-001] |
| `skills/user-experience/templates/wave-signoff-template.md` | WAVE-N-SIGNOFF.md for wave transitions | [STUB: EPIC-001] |

### Project and Spec Links

| Item | Location |
|------|----------|
| GitHub Issue (authoritative spec) | [#138](https://github.com/geekatron/jerry/issues/138) |
| Issue body (main spec) | `projects/PROJ-020-feature-enhancements/work/issue-drafts/gh-ready/issue-body.md` |
| Tech spec (agents, MCP, cognitive modes) | `projects/PROJ-020-feature-enhancements/work/issue-drafts/gh-ready/comment-2-tech-spec.md` |
| Appendices (directory structure, scores) | `projects/PROJ-020-feature-enhancements/work/issue-drafts/gh-ready/comment-3-appendices.md` |
| Acceptance criteria | `projects/PROJ-020-feature-enhancements/work/issue-drafts/gh-ready/comment-1-acceptance-criteria.md` |
| PROJ-022 PLAN.md | `projects/PROJ-022-user-experience-skill/PLAN.md` |
| PROJ-022 WORKTRACKER.md | `projects/PROJ-022-user-experience-skill/WORKTRACKER.md` |

### Standards References

| Standard | Location |
|----------|----------|
| Agent Definition Format (H-34) | `.context/rules/agent-development-standards.md` |
| Agent Governance Schema | `docs/schemas/agent-governance-v1.schema.json` |
| Skill Standards (H-25, H-26) | `.context/rules/skill-standards.md` |
| Quality Enforcement SSOT (H-13, H-14) | `.context/rules/quality-enforcement.md` |
| Mandatory Skill Usage (H-22) | `.context/rules/mandatory-skill-usage.md` |
| Agent Routing Standards (H-36) | `.context/rules/agent-routing-standards.md` |
| Handoff Schema | `docs/schemas/handoff-v2.schema.json` (canonical path per `agent-development-standards.md`; file pending creation) |
| ADR: UX Skill Architecture | `projects/PROJ-022-user-experience-skill/decisions/ADR-PROJ022-001-ux-skill-architecture.md` (PROVISIONAL) |
| ADR: Wave Criteria Gates | `projects/PROJ-022-user-experience-skill/decisions/ADR-PROJ022-002-wave-criteria-gates.md` (PROVISIONAL) |
| MCP Tool Standards | `.context/rules/mcp-tool-standards.md` |

### UX Framework References

| Framework | Source | Year | URL |
|-----------|--------|------|-----|
| Nielsen's 10 Usability Heuristics | Jakob Nielsen, Nielsen Norman Group | 1994 (updated 2024) | https://www.nngroup.com/articles/ten-usability-heuristics/ |
| Jobs-to-Be-Done | Clayton Christensen, Anthony Ulwick (ODI) | 2003/2016 | https://jobs-to-be-done.com/jobs-to-be-done-a-framework-for-customer-needs-c883cbbbe61f |
| Lean UX | Jeff Gothelf and Josh Seiden | 2013 (3rd ed. 2021) | https://www.jeffgothelf.com/lean-ux-book/ |
| Google HEART Framework | Kerry Rodden, Hilary Hutchinson, Xin Fu | 2010 | https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/ |
| Atomic Design | Brad Frost | 2016 | https://atomicdesign.bradfrost.com/ |
| WCAG 2.2 | W3C Web Accessibility Initiative | 2023 | https://www.w3.org/TR/WCAG22/ |
| Microsoft Inclusive Design | Microsoft | 2016 | https://inclusive.microsoft.design/ |
| Fogg Behavior Model | BJ Fogg, Stanford Persuasive Tech Lab | 2009 (B=MAP 2019) | https://behaviormodel.org/ |
| Kano Model | Noriaki Kano et al. | 1984 | Kano, N., Seraku, N., Takahashi, F., & Tsuji, S. (1984). Attractive Quality and Must-Be Quality. *Journal of the Japanese Society for Quality Control*, 14(2), 39-48. |
| AJ&Smart Design Sprint 2.0 | Jake Knapp / AJ&Smart | 2016/2019 | https://ajsmart.com/design-sprint |

### Research Provenance

| Artifact | Location | Created | Quality Gate |
|----------|----------|---------|-------------|
| Architecture Vision | `projects/PROJ-020-feature-enhancements/work/analysis/ux-skill-architecture-vision.md` | 2026-03-03 | C3 initial score 0.83, iterated to C4 |
| Framework Selection Analysis | `projects/PROJ-020-feature-enhancements/work/analysis/ux-framework-selection.md` | 2026-03-03 | C3 (part of architecture vision pipeline) |
| UX Frameworks Survey | `projects/PROJ-020-feature-enhancements/work/research/ux-frameworks-survey.md` | 2026-03-02 | C3 research (ps-researcher) |
| Tiny Teams Research | `projects/PROJ-020-feature-enhancements/work/research/tiny-teams-research.md` | 2026-03-02 | C3 research (ps-researcher) |
| MCP Design Tools Survey | `projects/PROJ-020-feature-enhancements/work/research/mcp-design-tools-survey.md` | 2026-03-02 | C3 research (ps-researcher) |
| Tournament Reports (Iter 1-8) | `projects/PROJ-020-feature-enhancements/work/issue-drafts/tournament-iter1/` through `tournament-iter8/` | 2026-03-03 | C4 tournament (8 iterations, final spec passed) |

---

*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: `.context/rules/quality-enforcement.md` (thresholds), GitHub Issue #138 (spec)*
*PROJ-022: User Experience Skill*
*Last Updated: 2026-03-03*
