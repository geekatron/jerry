---
name: ux-lean-ux
description: "Lean UX hypothesis-driven design sub-skill for the /user-experience parent skill. Facilitates Build-Measure-Learn cycles using Jeff Gothelf and Josh Seiden's Lean UX methodology (3rd ed. 2021). Produces hypothesis backlogs, assumption maps, MVP experiment designs, and validated learning logs. Invoke when teams need hypothesis-driven iteration, assumption mapping, experiment design, or validated learning documentation. Invoked by ux-orchestrator during Wave 2 lifecycle-stage routing or when user intent is \"testing hypotheses\" during the \"During design\" stage. Triggers: lean UX, hypothesis, assumption mapping, build-measure-learn, MVP experiment, validated learning, experiment design, hypothesis backlog."
version: "1.2.0"
agents:
  - ux-lean-ux-facilitator
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
activation-keywords:
  - "lean UX"
  - "hypothesis-driven design"
  - "assumption mapping"
  - "build-measure-learn"
  - "MVP experiment"
  - "validated learning"
  - "experiment design"
  - "hypothesis backlog"
  - "Lean UX hypothesis"
---

<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/user-experience/SKILL.md | PARENT: /user-experience skill | REVISION: Iter3 quality gate fixes -- ICE attribution correction, H-26 reference normalization, on_receive/on_send inline enumeration, agent table stub marker fix -->

# Lean UX Sub-Skill

> **Version:** 1.2.0
> **Framework:** Jerry User-Experience -- Lean UX
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Parent Skill:** `/user-experience` (`skills/user-experience/SKILL.md`)
> **Wave:** 2 (Data-Ready)
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
| [Methodology](#methodology) | Lean UX Build-Measure-Learn cycles, hypothesis format, ICE prioritization, assumption mapping, experiment types with selection guide |
| [MCP Dependencies](#mcp-dependencies) | Miro REQ with text-based fallback; Figma ENH; Context7 for Lean UX docs |
| [Output Specification](#output-specification) | Output location, L0/L1/L2 structure, required sections |
| [Routing](#routing) | Keywords and lifecycle-stage routing integration |
| [Cross-Framework Integration](#cross-framework-integration) | Handoff from Design Sprint and to HEART Metrics |
| [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence) | Confidence classifications for Lean UX outputs |
| [Constitutional Compliance](#constitutional-compliance) | Governing principles and AI-augmented analysis limitations |
| [Registration](#registration) | H-26 parent-routed registration model and AGENTS.md confirmation |
| [Deployment Status](#deployment-status) | Wave 2 stub agent status and implementation timeline |
| [Quick Reference](#quick-reference) | Common workflows and agent selection hints |
| [References](#references) | Full repo-relative paths, requirements traceability, external citations |

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Product managers, designers | [Purpose](#purpose), [When to Use This Sub-Skill](#when-to-use-this-sub-skill), [Quick Reference](#quick-reference) |
| **L1 (Developer)** | Engineers invoking the agent | [Invoking the Agent](#invoking-the-agent), [Methodology](#methodology), [Output Specification](#output-specification) |
| **L2 (Architect)** | Workflow designers, skill maintainers | [Cross-Framework Integration](#cross-framework-integration), [MCP Dependencies](#mcp-dependencies), [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence) |

---

## Purpose

The Lean UX sub-skill provides structured, hypothesis-driven design facilitation using Jeff Gothelf and Josh Seiden's Lean UX methodology (3rd edition, 2021). It targets tiny teams (1-5 people) who need to move beyond opinion-based design decisions toward evidence-based iteration through Build-Measure-Learn cycles.

This sub-skill is part of Wave 2 (Data-Ready), meaning it requires Wave 1 completion (at least 1 heuristic evaluation completed AND 1 JTBD job statement used in a product decision) before deployment. It bridges the gap between design evaluation (Wave 1) and quantitative measurement (Wave 2: HEART Metrics) by providing a structured experimentation framework.

### Key Capabilities

- **Hypothesis-Driven Design** -- Structures design decisions as testable hypotheses using the Lean UX format: "We believe [outcome] for [users] if [change] because [evidence]"
- **Assumption Mapping** -- Prioritizes unknowns using the 4-quadrant framework (Known/Unknown x High Risk/Low Risk) to focus experimentation on the highest-risk unknowns first
- **MVP Experiment Design** -- Designs minimum viable experiments (A/B tests, fake door tests, concierge MVP, Wizard of Oz, paper prototypes) with measurable success criteria
- **Validated Learning Documentation** -- Tracks hypothesis outcomes (confirmed/invalidated) with supporting evidence, building an organizational learning log
- **Hypothesis Backlog Management** -- Maintains a prioritized backlog of hypotheses with validation status, enabling systematic iteration across Build-Measure-Learn cycles
- **Build-Measure-Learn Cycle Tracking** -- Coordinates full cycles from hypothesis formulation through experiment execution to learning documentation

> **Source:** Key capabilities derived from parent SKILL.md [skills/user-experience/SKILL.md § Key Capabilities] ("Lean UX Facilitation -- Hypothesis-driven build-measure-learn cycles (Wave 2)") and [skills/user-experience/SKILL.md § Available Agents] ("Lean UX hypothesis and experiment facilitation").

---

## When to Use This Sub-Skill

Activate when:

- Designing or validating a hypothesis about a design change and its expected outcome
- Mapping and prioritizing assumptions about user behavior, value proposition, or implementation feasibility
- Designing an MVP experiment to test a specific hypothesis with measurable outcomes
- Documenting validated learning from completed experiments (hypothesis confirmed or invalidated)
- Managing a backlog of hypotheses through multiple Build-Measure-Learn iterations
- Iterating on an existing design during the "During design" lifecycle stage with a hypothesis-testing approach
- Transitioning from a Design Sprint (Wave 5) into structured iteration cycles

Do NOT use for:

- Evaluating an existing interface against usability heuristics -- use `/ux-heuristic-eval` (Nielsen's 10) instead. Lean UX focuses on forward-looking hypothesis testing, not backward-looking evaluation of existing designs.
- Measuring quantitative UX health metrics -- use `/ux-heart-metrics` (Google GSM) instead. Lean UX produces hypothesis validation status; HEART Metrics produces ongoing measurement baselines.
- Understanding user motivations and jobs -- use `/ux-jtbd` (Jobs-to-Be-Done) instead. Lean UX consumes job statements from JTBD; it does not perform user motivation research.
- Diagnosing why users fail to take a specific action -- use `/ux-behavior-design` (Fogg B=MAP) instead. Lean UX tests hypotheses about changes; behavior design diagnoses existing behavioral bottlenecks.
- Running a full rapid prototyping sprint -- use `/ux-design-sprint` (Design Sprint 2.0) instead. Lean UX operates on individual hypotheses; Design Sprint produces validated prototypes through a multi-day structured process.
- Accessibility compliance auditing -- use `/ux-inclusive-design` (WCAG 2.2) instead.
- Security-focused interface review -- use `/eng-team` instead.
- General research without UX hypothesis focus -- use `/problem-solving` instead.

> **Source:** Routing logic derived from [skills/user-experience/SKILL.md § Lifecycle-Stage Routing] ("During design: Iterating on existing design -> /ux-lean-ux OR /ux-heuristic-eval") and [skills/user-experience/rules/ux-routing-rules.md § Stage Routing Table], [skills/user-experience/rules/ux-routing-rules.md § Common Intent Resolution].

---

## Available Agents

| Agent | Role | Tier | Mode | Model | Output Location |
|-------|------|------|------|-------|-----------------|
| `ux-lean-ux-facilitator` | Lean UX hypothesis and experiment facilitation specialist | T4 | Systematic | Sonnet | `skills/ux-lean-ux/output/{engagement-id}/ux-lean-ux-facilitator-{topic-slug}.md` |

**STUB:** The agent definition file (`skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md`) currently contains frontmatter, identity, purpose, and guardrails sections only. Full agent body implementation (`<input>`, `<capabilities>`, `<methodology>`, `<output>` sections) is pending Wave 2 completion of PROJ-022 EPIC-003. The SKILL.md specifies the methodology and output contract that the agent will implement.

**Tool tier:** T4 (External) = Read, Write, Edit, Glob, Grep + WebSearch, WebFetch + Context7 MCP. The T4 tier enables access to external Lean UX methodology documentation via Context7 and web search for A/B testing framework references. Bash is intentionally excluded; T4 tier does not require shell access for MCP operations. See `agent-development-standards.md` [Tool Security Tiers] for full tier definitions.

The agent produces output at three levels per AD-M-004:
- **L0 (Executive Summary):** Top hypotheses with validation status; key assumptions identified; experiment recommendations for stakeholders and cross-framework synthesis input.
- **L1 (Technical Detail):** Full hypothesis backlog with Lean UX format statements, assumption map, experiment designs with success criteria, and validated learning log.
- **L2 (Strategic Implications):** Organizational learning patterns, hypothesis failure rate analysis, experimentation maturity assessment, and iteration velocity recommendations.

> **Source:** Agent specification from [skills/user-experience/SKILL.md § Available Agents] and ORCHESTRATION.yaml pipeline-wave2 phase-1 (artifact: `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md`).

---

## P-003 Compliance

The `/ux-lean-ux` sub-skill contains a single **worker** agent. It is invoked by the `ux-orchestrator` (T5) via the Agent tool. The agent does NOT have Agent tool access and MUST NOT spawn sub-agents.

```
MAIN CONTEXT (user request)
    |
    v
ux-orchestrator (T5, Opus, Integrative) -- parent orchestrator
    |
    +-- ux-lean-ux-facilitator (T4, Systematic, Sonnet) -- THIS sub-skill's worker
    +-- [other sub-skill workers...]
```

**Enforcement:**
- `disallowedTools: [Agent]` declared in `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md` frontmatter
- P-003 prohibition in `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.governance.yaml` `capabilities.forbidden_actions`
- CI gate validates no sub-skill agent has Agent access (documented in `skills/user-experience/rules/ci-checks.md`)

> **Source:** P-003 hierarchy from parent SKILL.md [P-003 Compliance].

---

## Invoking the Agent

This is a sub-skill invoked by the `ux-orchestrator`, not directly by users. Users interact with the parent `/user-experience` skill, which routes to this sub-skill based on lifecycle-stage triage.

### Via Natural Language (to parent skill)

```
"Help me test whether this design change will improve conversion"
"Map our riskiest assumptions about the onboarding flow"
"Design an experiment to validate our checkout hypothesis"
"Document what we learned from the A/B test results"
```

The `ux-orchestrator` routes these requests to `ux-lean-ux-facilitator` based on [skills/user-experience/rules/ux-routing-rules.md § Stage Routing Table]. Specifically, the "During design: Iterating on existing design" stage qualifies with "Testing hypotheses" intent (source: [ux-routing-rules.md § Stage Routing Table]).

### Via Explicit Agent Request (to parent skill)

```
"Use ux-lean-ux-facilitator to create a hypothesis backlog for the new pricing page"
"Have ux-lean-ux-facilitator design an experiment for the onboarding changes"
```

### Via Agent Tool (orchestrator internal)

The `ux-orchestrator` invokes the agent via the Agent tool:

```python
Agent(
    description="ux-lean-ux-facilitator: Lean UX hypothesis cycle for checkout redesign",
    subagent_type="jerry:ux-lean-ux-facilitator",
    prompt="""
## UX CONTEXT (REQUIRED)
- **Engagement ID:** UX-0001
- **Topic:** Checkout Flow Hypothesis Cycle
- **Product:** [product name and domain]
- **Target Users:** [user description]
- **Input:** [design change description, prior research, prototype reference]

## TASK
Facilitate a Lean UX hypothesis cycle for the checkout flow redesign.
1. Create hypothesis statements in Lean UX format
2. Map assumptions using the 4-quadrant framework
3. Design MVP experiments with measurable success criteria
4. Document validated learning from any completed experiments

## MANDATORY PERSISTENCE (P-002)
Create file at: skills/ux-lean-ux/output/UX-0001/ux-lean-ux-facilitator-checkout-flow.md
"""
)
```

> **Governance codification (AD-M-007):** The session_context contract (on_receive/on_send) is specified in `ux-lean-ux-facilitator.governance.yaml` per AD-M-007. Fields are enumerated below:

**on_receive fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `engagement_id` | string | Yes | UX engagement identifier (format: `UX-{NNNN}`) |
| `product_context` | string | Yes | Product name, domain, and target user description |
| `design_change` | string | Yes | Description of the design change or area under hypothesis testing |
| `prior_experiment_results` | array | No | Results from prior Build-Measure-Learn cycles (hypothesis ID, status, evidence) |
| `upstream_artifacts` | array | No | File paths to upstream handoff artifacts (JTBD findings, heuristic eval findings, Design Sprint outputs) |

**on_send fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hypothesis_backlog` | array | Yes | Hypothesis entries with ID, Lean UX format statement, status, and ICE score |
| `assumption_map` | object | Yes | 4-quadrant assumption map with quadrant assignments and movement tracking |
| `experiment_designs` | array | Yes | Per-hypothesis experiment designs with type, success criteria, and duration |
| `validated_learning_log` | array | Yes | Completed Build-Measure-Learn cycle entries with evidence and decisions |
| `synthesis_judgments` | array | Yes | AI judgment calls with confidence classification (HIGH/MEDIUM/LOW) and rationale |

> **Source:** Invocation pattern from parent SKILL.md [Invoking an Agent].

---

## Methodology

### Lean UX Hypothesis Format

Every design decision is structured as a testable hypothesis using the canonical Lean UX format (Gothelf & Seiden, 2021):

```
We believe [outcome]
for [users]
if [change]
because [evidence/reasoning]
```

| Component | Description | Example |
|-----------|-------------|---------|
| **Outcome** | The measurable result we expect | "a 15% increase in checkout completion" |
| **Users** | The specific user segment affected | "first-time buyers on mobile" |
| **Change** | The design change being tested | "we simplify the checkout to a single page" |
| **Evidence** | The reasoning or prior data supporting the hypothesis | "our heuristic evaluation found 3 major navigation issues in the current multi-step flow" |

Each hypothesis receives a unique ID (format: `HYP-{NNN}`) and tracks through the Build-Measure-Learn cycle with status: DRAFT, ACTIVE, VALIDATED, INVALIDATED, DEFERRED.

### Hypothesis Prioritization (ICE Scoring)

Hypotheses in the backlog are prioritized using ICE scoring to determine which to test first:

| Dimension | Question | Score Range |
|-----------|----------|-------------|
| **Impact** | If validated, how much will this move the target outcome metric? | 1 (minimal) - 10 (transformative) |
| **Confidence** | How confident are we that the hypothesis is correct, based on available evidence? | 1 (pure guess) - 10 (strong prior evidence) |
| **Ease** | How easy is it to design and run an experiment to test this hypothesis? | 1 (months of effort) - 10 (days of effort) |

**ICE score** = (Impact + Confidence + Ease) / 3. Hypotheses with higher ICE scores are tested first. When ICE scores are tied, prefer the hypothesis in the higher-risk assumption quadrant (Q1 > Q2 > Q4 > Q3). ICE scoring is intentionally lightweight -- for tiny teams, a 30-second scoring pass per hypothesis is sufficient. Re-score after each Build-Measure-Learn cycle as evidence changes confidence levels.

> **Source:** ICE scoring (Impact, Confidence, Ease) is a product prioritization framework originating from the growth hacking community (Sean Ellis, GrowthHackers, circa 2015). It is widely adopted in Lean UX contexts for lightweight hypothesis prioritization. Referenced in [skills/user-experience/rules/synthesis-validation.md § External Methodology Citations].

### Assumption Mapping

Assumptions are prioritized using a 4-quadrant framework that maps risk against knowledge:

```
                    HIGH RISK
                       |
    +---------+--------+--------+---------+
    |         |                 |         |
    |  Q2:    |    Q1:          |         |
    |  Known  |    Unknown      |         |
    |  High   |    High Risk    |         |
    |  Risk   |    (TEST FIRST) |         |
    |         |                 |         |
KNOWN --------+--------+--------+-------- UNKNOWN
    |         |                 |         |
    |  Q3:    |    Q4:          |         |
    |  Known  |    Unknown      |         |
    |  Low    |    Low Risk     |         |
    |  Risk   |    (DEFER)      |         |
    |         |                 |         |
    +---------+--------+--------+---------+
                       |
                    LOW RISK
```

| Quadrant | Name | Action | Priority |
|----------|------|--------|----------|
| **Q1** | Unknown + High Risk | Test first -- these are the riskiest unknowns that could invalidate the entire approach | HIGHEST |
| **Q2** | Known + High Risk | Monitor -- validated but high-impact; revisit if conditions change | MEDIUM |
| **Q3** | Known + Low Risk | Accept -- validated and low-impact; no action needed | LOW |
| **Q4** | Unknown + Low Risk | Defer -- unknown but low-impact; test only if resources allow | LOWEST |

**Assumption categories:** Assumptions are classified into three types per Lean UX methodology:
1. **Value assumptions** -- "Users want this outcome" (relates to JTBD job statements if available)
2. **Usability assumptions** -- "Users can accomplish this task" (relates to heuristic evaluation findings if available)
3. **Feasibility assumptions** -- "We can build this within constraints" (relates to technical implementation)

> **Source:** Gothelf & Seiden (2021), Chapter 4: "Assumptions." Assumption mapping quadrant framework.

### Experiment Types

The facilitator selects experiment types based on hypothesis characteristics, available resources, and desired confidence level:

| Experiment Type | Description | Best For | Confidence Level | Duration | Cost |
|----------------|-------------|----------|-----------------|----------|------|
| **A/B Test** | Controlled comparison of two variants with random user assignment | Quantitative outcome validation with sufficient traffic | HIGH | 1-4 weeks | Medium |
| **Fake Door Test** | Feature entry point exists but feature is not built; measures interest via click-through | Demand validation before building | MEDIUM | 1-2 weeks | Low |
| **Concierge MVP** | Human manually delivers the service the product would automate | Value validation for complex workflows | MEDIUM | 2-4 weeks | Medium |
| **Wizard of Oz** | User interacts with what appears automated but is human-operated behind the scenes | Usability and value validation for AI/automation features | MEDIUM | 1-2 weeks | Medium |
| **Paper Prototype** | Low-fidelity mockup tested with users in moderated sessions | Usability validation for early-stage concepts | LOW-MEDIUM | 1-3 days | Low |
| **Smoke Test** | Landing page or signup form gauging interest before building | Market demand validation | MEDIUM | 1-2 weeks | Low |
| **One-Question Survey** | Single focused question to existing users | Specific assumption validation | LOW | 1-3 days | Low |

**Experiment selection criteria:** The facilitator recommends an experiment type based on: (a) the assumption quadrant (Q1 assumptions need higher-confidence experiments), (b) the available user base (A/B tests require sufficient traffic), (c) the time and resource constraints of the team, and (d) the specificity of the hypothesis (broad hypotheses need exploratory experiments; narrow hypotheses need quantitative validation).

### Experiment Type Selection Guide

Use this decision matrix to select the right experiment type for a given hypothesis:

| If you need to... | Use experiment type | Time | Confidence | Minimum user base |
|---|---|---|---|---|
| Validate demand before building a feature | Fake door test | 1-2 weeks | MEDIUM | Existing traffic to host page |
| Test a new workflow end-to-end with real users | Wizard of Oz | 1-2 weeks | MEDIUM | 5-10 participants |
| Prove users will pay for or use a complex service | Concierge MVP | 2-4 weeks | MEDIUM | 5-15 participants |
| Quantitatively compare two design variants | A/B test | 1-4 weeks | HIGH | Sufficient traffic for statistical power |
| Validate usability of an early-stage concept | Paper prototype | 1-3 days | LOW-MEDIUM | 5 participants |
| Gauge market interest before investing effort | Smoke test | 1-2 weeks | MEDIUM | Existing traffic or ad spend |
| Validate a single specific assumption quickly | One-question survey | 1-3 days | LOW | Existing user base for distribution |

**Quick decision path:** (1) If you have sufficient traffic and a narrow, measurable hypothesis, use an **A/B test**. (2) If the feature does not exist yet, use a **fake door test** or **smoke test** to validate demand first. (3) If the hypothesis involves a complex workflow, use **Wizard of Oz** or **concierge MVP** depending on whether you need to test usability (Wizard of Oz) or value (concierge). (4) If you are in early concept stage, start with a **paper prototype**. (5) If you need a fast answer to a single question, use a **one-question survey**.

### Build-Measure-Learn Cycle

Each cycle follows the Lean UX iteration pattern:

| Phase | Name | Activities | Output |
|-------|------|-----------|--------|
| 1 | **Build** | Select hypothesis from backlog; design minimum viable experiment; define success metrics and criteria | Experiment design document with hypothesis ID, experiment type, duration, sample size, success criteria |
| 2 | **Measure** | Execute experiment; collect data per success criteria; document observations | Raw experiment data, metric observations, qualitative notes |
| 3 | **Learn** | Analyze results against success criteria; classify hypothesis as VALIDATED or INVALIDATED; document learning; update assumption map | Validated learning entry with evidence, updated hypothesis status, updated assumption quadrant positions |
| 4 | **Iterate** | Based on learning: pivot (change approach), persevere (continue with validated direction), or kill (abandon invalidated direction) | Updated hypothesis backlog; new hypotheses if pivoting; archival of invalidated hypotheses |

**Cycle duration guidance:** Lean UX emphasizes short cycles. For tiny teams (1-5 people), recommended cycle duration is 1-2 weeks. Cycles exceeding 4 weeks indicate the experiment scope is too large and should be decomposed into smaller hypotheses.

### Validated Learning Log

Every completed Build-Measure-Learn cycle produces a validated learning entry:

```
### Learning L-{NNN}: {brief description}

- **Hypothesis:** HYP-{NNN} -- {hypothesis statement}
- **Experiment:** {experiment type} -- {experiment description}
- **Duration:** {start date} to {end date}
- **Success Criteria:** {what was measured and the threshold}
- **Result:** VALIDATED | INVALIDATED
- **Evidence:** {specific data, metrics, or observations supporting the result}
- **Decision:** PIVOT | PERSEVERE | KILL
- **Next Action:** {what changes based on this learning}
```

> **Source:** Gothelf & Seiden (2021), Chapter 7: "MVPs and Experiments." Build-Measure-Learn cycle and experiment types.

---

## MCP Dependencies

### Dependency Matrix

| MCP Tool | Classification | Purpose | Fallback |
|----------|---------------|---------|----------|
| **Miro** | **REQ** | Collaborative assumption mapping boards, hypothesis backlog visualization, Build-Measure-Learn cycle tracking | Text-based exercise mode: assumption maps and hypothesis backlogs as structured markdown tables |
| **Figma** | ENH | Reference prototype artifacts in experiment designs; visual documentation of design changes being tested | Text description mode: design changes described textually; screenshot references where available |
| **Hotjar (Bridge)** | ENH | Access behavioral analytics data for experiment measurement (heatmaps, session recordings, funnel data) | Manual analytics input: user provides behavioral data via text description or exported reports |
| **Context7** | Available (current infrastructure) | Resolve and query Lean UX methodology documentation, A/B testing framework references | WebSearch fallback per MCP-001 (`mcp-tool-standards.md` [Error Handling]) |

### Miro Fallback: Text-Based Exercise Mode

When the Miro MCP adapter is unavailable (current state -- adapter implementation is post-PROJ-022 scope), the facilitator operates in text-based exercise mode:

- Assumption maps are produced as structured markdown tables with quadrant assignments
- Hypothesis backlogs are maintained as markdown tables with status columns
- Build-Measure-Learn cycle tracking uses text-based status updates
- **Limitations in text-based mode:**
  - Cannot create or update collaborative visual boards
  - Cannot visualize assumption movement between quadrants over time
  - Cannot embed experiment results alongside visual hypothesis boards
- Output carries a degraded mode disclosure per P-022:
  ```
  [DEGRADED MODE] This output was produced without Miro MCP access.
  Input was provided via text-based exercise mode. Some features are reduced:
  - Cannot create or update collaborative visual boards
  - Cannot visualize assumption movement between quadrants over time
  - Cannot embed experiment results alongside visual hypothesis boards
  ```

### Context7 Usage

Per MCP-001 (`.context/rules/mcp-tool-standards.md` [Context7 Integration]), Context7 is used when the facilitation references external Lean UX frameworks or experiment methodologies by name:

| Library/Framework | Usage |
|-------------------|-------|
| Lean UX (Gothelf & Seiden) | Hypothesis format, assumption mapping methodology, Build-Measure-Learn cycle structure |
| A/B testing frameworks | Experiment design patterns, sample size calculations, statistical significance thresholds |
| Google Optimize / similar | A/B test configuration patterns and metric setup |

Protocol: call `mcp__context7__resolve-library-id` with the framework name, then `mcp__context7__query-docs` with the resolved ID and specific query. If Context7 returns no results, fall back to WebSearch per `mcp-tool-standards.md` [Error Handling].

> **Source:** MCP dependency matrix from [skills/user-experience/SKILL.md § MCP Integration Architecture] (`/ux-lean-ux` row showing Figma ENH, Miro REQ, Hotjar ENH) and [skills/user-experience/rules/mcp-coordination.md § MCP Dependency Matrix], [skills/user-experience/rules/mcp-coordination.md § Degraded Mode Behavior].

---

## Output Specification

### Output Location

```
skills/ux-lean-ux/output/{engagement-id}/ux-lean-ux-facilitator-{topic-slug}.md
```

Where:
- `{engagement-id}` follows the pattern `UX-{NNNN}` (e.g., `UX-0001`)
- `{topic-slug}` is a kebab-case descriptor of the hypothesis cycle topic (e.g., `checkout-flow`, `onboarding-redesign`)

### Required Output Sections

| Section | Level | Content |
|---------|-------|---------|
| **Executive Summary** | L0 | Top 3-5 hypotheses with validation status; highest-risk assumptions; experiment recommendations for stakeholders and cross-framework synthesis input |
| **Engagement Context** | L1 | Product description, target users, design change under consideration, prior research inputs (JTBD findings, heuristic eval findings, Design Sprint outputs), MCP status |
| **Hypothesis Backlog** | L1 | Full hypothesis backlog with: hypothesis ID (HYP-{NNN}), Lean UX format statement, assumption category (value/usability/feasibility), status (DRAFT/ACTIVE/VALIDATED/INVALIDATED/DEFERRED), priority, linked experiment |
| **Assumption Map** | L1 | 4-quadrant assumption map with each assumption positioned in Q1-Q4, movement tracking between quadrants as evidence accumulates |
| **Experiment Designs** | L1 | Per-hypothesis experiment design with: experiment type, description, duration estimate, sample size, success criteria (metric + threshold), measurement method |
| **Validated Learning Log** | L1 | Chronological log of completed Build-Measure-Learn cycles with evidence, outcomes, and decisions (pivot/persevere/kill) |
| **Strategic Implications** | L2 | Organizational learning patterns (hypothesis validation rate, common failure modes), experimentation maturity assessment, iteration velocity recommendations, product strategy implications |
| **Synthesis Judgments Summary** | L1 | Each AI judgment call listed for synthesis confidence gate compliance (see note below) |
| **Handoff Data** | L1 | Structured data for downstream sub-skills: hypothesis IDs, validated/invalidated status, metric implications (for HEART Metrics consumption) |

**Synthesis Judgments Summary requirements:** This section MUST list every AI-generated judgment (assumption quadrant placement, hypothesis prioritization, experiment type recommendation) with a confidence classification (HIGH, MEDIUM, LOW) and a one-line rationale. This enables downstream consumers (including `/ux-heart-metrics` and the `ux-orchestrator` synthesis gate) to assess which findings are strongly supported versus which require additional validation. The format follows the Wave 1 synthesis judgments pattern established in `skills/user-experience/rules/synthesis-validation.md`.

### Templates

Two templates support the agent's output production:

| Template | Path | Purpose |
|----------|------|---------|
| Hypothesis Backlog Template | `skills/ux-lean-ux/templates/hypothesis-backlog-template.md` [PLANNED: Wave 2 Phase 2] | Lean UX hypothesis statement backlog with validation status tracking |
| Assumption Map Template | `skills/ux-lean-ux/templates/assumption-map-template.md` [PLANNED: Wave 2 Phase 2] | 4-quadrant assumption mapping and prioritization worksheet |

> **Source:** Output location from [skills/user-experience/SKILL.md § Available Agents] and ORCHESTRATION.yaml pipeline-wave2 phase-1 artifacts (hypothesis-backlog-template.md, assumption-map-template.md).

---

## Routing

### Trigger Keywords

| Keyword | Routing Context |
|---------|----------------|
| lean UX | Direct match -- primary trigger |
| hypothesis-driven design | Direct match |
| assumption mapping | Direct match |
| build-measure-learn | Direct match |
| MVP experiment | Direct match |
| validated learning | Direct match |
| experiment design | In combination with UX/design context |
| hypothesis backlog | Direct match |

### Lifecycle-Stage Routing Integration

This sub-skill is routed to by the `ux-orchestrator` in the following lifecycle-stage scenarios:

| Stage | User Intent | Route Condition |
|-------|-------------|-----------------|
| During design | "Iterating on existing design" | Qualification: "Testing hypotheses" (vs. "Evaluating existing interface" which routes to `/ux-heuristic-eval`); source: [ux-routing-rules.md § Stage Routing Table] |
| During design | Follow-up from Design Sprint | When `/ux-design-sprint` has completed with validated prototype; Design Sprint output feeds hypothesis generation |
| Any stage | "Test whether this change will work" | Hypothesis-driven intent detected; routes to Lean UX for experiment design |

### Wave Gating

This sub-skill is in **Wave 2** (Data-Ready). It requires Wave 1 completion before deployment:

**Entry criteria:** Wave 1 at least 1 heuristic evaluation completed AND 1 JTBD job statement used in a product decision.

**Bypass condition:** 2 sprint cycles elapsed with no Wave 1 completion; documented rationale required (3-field documentation per [skills/user-experience/SKILL.md § Wave Architecture]).

> **Source:** Routing integration from [skills/user-experience/rules/ux-routing-rules.md § Stage Routing Table] and [skills/user-experience/SKILL.md § Lifecycle-Stage Routing]. Wave assignment from [skills/user-experience/SKILL.md § Wave Architecture].

---

## Cross-Framework Integration

### Upstream Inputs

This sub-skill receives context from other sub-skills when invoked as part of a multi-sub-skill workflow:

| From Sub-Skill | Handoff Artifact | Key Fields | Usage |
|----------------|-----------------|-----------|-------|
| `/ux-design-sprint` | Validated prototype + Day 4 findings | Prototype description, interview findings, validated/invalidated hypotheses | Day 4 interview findings seed the initial hypothesis backlog; validated prototype becomes the baseline for Lean UX iterations |
| `/ux-jtbd` | Job statements + switch forces | Job statement text, push/pull forces, hiring criteria | Job statements inform value assumptions; switch forces identify high-risk areas for hypothesis generation |
| `/ux-heuristic-eval` | Severity-rated findings | Finding ID, heuristic violated, severity (0-4), affected screen/flow | Heuristic findings with severity >= 2 inform usability assumptions; high-severity findings suggest hypothesis candidates for remediation experiments |

### Downstream Handoffs

This sub-skill produces artifacts that feed into other sub-skills via the Jerry handoff protocol (`docs/schemas/handoff-v2.schema.json`).

| To Sub-Skill | Handoff Artifact | Key Fields | Trigger |
|-------------|-----------------|-----------|---------|
| `/ux-heart-metrics` | Validated/invalidated hypothesis backlog | Hypothesis ID, validated/invalidated status, metric implications | After experiment completion; HEART Metrics establishes ongoing measurement for validated hypotheses |

**Handoff threshold:** Only hypotheses with status VALIDATED or INVALIDATED (i.e., those that have completed at least one Build-Measure-Learn cycle) are included in cross-framework handoffs. Hypotheses with status DRAFT, ACTIVE, or DEFERRED remain in the hypothesis backlog but are not propagated downstream.

### Canonical Multi-Skill Workflow Sequences

This sub-skill participates in the following canonical sequences:

| Sequence | Skills Involved | This Sub-Skill's Role |
|----------|----------------|-----------------------|
| Sprint to Iterate to Measure | `/ux-design-sprint` then **`/ux-lean-ux`** then `/ux-heart-metrics` | Receives Design Sprint prototype; iterates through hypothesis cycles; feeds validated hypotheses to HEART Metrics |
| Evaluate to Iterate | `/ux-heuristic-eval` then **`/ux-lean-ux`** | Heuristic findings generate remediation hypotheses; Lean UX designs experiments to test fixes |

> **Source:** Handoff data contracts from [skills/user-experience/rules/ux-routing-rules.md § Handoff Data Contracts] and [skills/user-experience/SKILL.md § Cross-Sub-Skill Handoff Data] ("/ux-design-sprint -> /ux-lean-ux: Validated prototype + Day 4 findings" and "/ux-lean-ux -> /ux-heart-metrics: Validated/invalidated hypothesis backlog"). Canonical sequences from [skills/user-experience/SKILL.md § Canonical Multi-Skill Workflow Sequences].

---

## Synthesis Hypothesis Confidence

Lean UX outputs include synthesis hypotheses that carry confidence classifications per the synthesis validation protocol.

| Synthesis Step | Typical Confidence | Rationale |
|---------------|-------------------|-----------|
| Assumption mapping | MEDIUM | Assumptions are deliberately unvalidated per Lean UX methodology; the purpose of mapping is to identify what needs testing, not to assert validity |
| Hypothesis generation | MEDIUM | Hypotheses are by definition unproven propositions; Lean UX methodology (Gothelf & Seiden, 2021) treats them as starting points for experimentation, not conclusions |

**Gate enforcement:**
- **MEDIUM outputs:** Include a "Validation Required" section. Design recommendations are withheld until validation against real experiment data or expert review is provided. Assumption maps and hypothesis backlogs serve as structured starting points, not validated findings.

**Note on confidence dynamics:** Lean UX outputs are intentionally MEDIUM confidence because the methodology's entire purpose is to generate testable propositions. Confidence increases only when a hypothesis completes a Build-Measure-Learn cycle and transitions to VALIDATED status with supporting experiment evidence. Even then, individual hypothesis validation produces MEDIUM synthesis confidence (single-framework finding); HIGH synthesis confidence requires convergence with a second framework (e.g., HEART Metrics confirms the validated hypothesis with quantitative measurement).

> **Source:** Confidence classifications from [skills/user-experience/rules/synthesis-validation.md § Sub-Skill Synthesis Output Map] ("`/ux-lean-ux` Assumption mapping; hypothesis generation MEDIUM"). Gate enforcement from [skills/user-experience/SKILL.md § Synthesis Hypothesis Validation].

---

## Constitutional Compliance

All agents in this sub-skill adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- worker agent, no Agent tool access | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user decisions on hypothesis priority or experiment selection | Unauthorized action; trust erosion |
| P-022 | NEVER present hypotheses as validated without experiment evidence; NEVER inflate experiment confidence without data | Governance undermined; quality assessment invalidated |
| P-001 | NEVER present assumption classifications without reasoning for the quadrant placement | Unreliable outputs; unfounded claims propagate downstream |
| P-002 | NEVER leave hypothesis backlog or experiment designs in transient context only -- persist to files | Context rot vulnerability; artifacts lost on session compaction |

**Per-agent enforcement:** The `ux-lean-ux-facilitator` agent declares:
- `constitution.principles_applied`: P-003, P-020, P-022, P-001, P-002 in `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.governance.yaml`
- `capabilities.forbidden_actions`: 3 entries in NPT-009 format referencing the constitutional triplet
- `disallowedTools: [Agent]` in `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md` frontmatter

### AI-Augmented Analysis Limitations

The Lean UX facilitator agent operates as an AI-augmented analysis tool. The following limitations apply to all outputs and MUST be disclosed per P-022 (no deception):

- **Hypotheses are secondary-research-derived.** Lean UX hypotheses generated by the AI are based on secondary research, design pattern knowledge, and provided context -- not direct user observation. They are structured starting points for experimentation, not empirically grounded predictions.
- **Experiment interpretation is data-dependent.** Experiment results are interpreted from user-provided data (metrics, observations, reports), not from direct measurement by the agent. The quality of the "Learn" phase depends entirely on the quality and completeness of the data provided.
- **Assumption mapping reflects AI judgment.** Quadrant placements (Q1-Q4) are AI assessments based on available information. Real-world risk and knowledge levels may differ from AI-estimated positions.
- **Always validate with real user data.** Hypothesis validation, assumption mapping, and experiment design outputs should be confirmed through actual user research, behavioral analytics, and empirical measurement before making irreversible product decisions.

---

## Registration

This sub-skill follows a parent-routed registration model. Sub-skills are not independently registered in `CLAUDE.md` or `mandatory-skill-usage.md` because they are routed through the parent `/user-experience` orchestrator (`ux-orchestrator`). This is an explicit exception to the H-26 registration requirement (parent-routed model): parent skills own the CLAUDE.md and mandatory-skill-usage.md registration; sub-skills are discovered and dispatched by the parent orchestrator's internal routing logic.

| Registration Point | Status | Detail |
|--------------------|--------|--------|
| `CLAUDE.md` skill table | Registered via parent | `/user-experience` is registered in `CLAUDE.md`; sub-skills are not independently listed |
| `mandatory-skill-usage.md` trigger map | Routed via parent | The `/user-experience` trigger map row includes "lean UX" as a positive keyword (H-22); requests matching this keyword route to the parent skill, which dispatches to this sub-skill |
| `AGENTS.md` agent registry | Registered | `ux-lean-ux-facilitator` is listed in `AGENTS.md` under the User-Experience Skill Agents section |
| Parent SKILL.md agent table | Registered | `ux-lean-ux-facilitator` is listed in `skills/user-experience/SKILL.md` [Available Agents] |

> **H-26 parent-routed model rationale:** Independent registration of sub-skills would create duplicate trigger map entries and ambiguous routing (AP-02 Bag of Triggers). The parent orchestrator owns lifecycle-stage routing logic and dispatches to the correct sub-skill based on triage qualification, not keyword matching alone. Sub-skill agents are registered in `AGENTS.md` for discoverability but routing flows through the parent.

---

## Deployment Status

> **Wave 2 Sub-Skill -- Stub Agent.** This sub-skill is part of Wave 2 (Data-Ready) of PROJ-022. The companion agent file (`skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md`) is currently a stub -- it contains frontmatter, identity, purpose, and guardrails sections but lacks full `<input>`, `<capabilities>`, `<methodology>`, and `<output>` sections. Full agent implementation is pending Wave 2 completion of PROJ-022 EPIC-003. The SKILL.md itself is complete and specifies the methodology, output format, and routing integration that the agent will implement.

---

## Quick Reference

### Common Workflows

| Need | Command Example |
|------|-----------------|
| Create hypotheses for a design change | "Help me create hypotheses for the checkout redesign" |
| Map assumptions | "Map our riskiest assumptions about the new onboarding flow" |
| Design an experiment | "Design an experiment to test whether single-page checkout improves conversion" |
| Document validated learning | "Document what we learned from the A/B test on the pricing page" |
| Review hypothesis backlog | "Review the hypothesis backlog for the mobile app redesign" |
| Post-sprint iteration | "We completed a Design Sprint -- help us iterate on the validated prototype" |

### Agent Selection Hints

| Keywords | Routes To |
|----------|-----------|
| hypothesis, lean UX, assumption, experiment, build-measure-learn, validated learning, MVP | `ux-lean-ux-facilitator` |
| heuristic, usability, Nielsen, severity, inspection, evaluation | `/ux-heuristic-eval` (not this sub-skill) |
| HEART, metrics, measurement, GSM, happiness, engagement | `/ux-heart-metrics` (not this sub-skill) |
| jobs to be done, JTBD, switch interview, user motivation | `/ux-jtbd` (not this sub-skill) |
| design sprint, rapid prototyping, 4-day sprint | `/ux-design-sprint` (not this sub-skill) |

---

## References

| Source | Content | Path |
|--------|---------|------|
| Parent SKILL.md | Sub-skill scope, wave architecture, routing, MCP dependencies, synthesis protocol | `skills/user-experience/SKILL.md` |
| Agent definition | Agent frontmatter, identity, expertise, guardrails | `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md` |
| Agent governance | Tool tier, forbidden actions, output validation, constitutional compliance | `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.governance.yaml` |
| UX routing rules | Lifecycle-stage routing, handoff data contracts, common intent resolution | `skills/user-experience/rules/ux-routing-rules.md` |
| MCP coordination | Miro REQ dependency, degraded mode behavior, Context7 usage | `skills/user-experience/rules/mcp-coordination.md` |
| Synthesis validation | Confidence gate protocol, per-sub-skill confidence map | `skills/user-experience/rules/synthesis-validation.md` |
| Wave progression | Wave 2 entry criteria, signoff requirements | `skills/user-experience/rules/wave-progression.md` |
| CI checks | P-003 enforcement, sub-skill validation gates | `skills/user-experience/rules/ci-checks.md` |
| Lean UX methodology rules | Build-Measure-Learn cycle rules, hypothesis format validation | `skills/ux-lean-ux/rules/lean-ux-methodology-rules.md` [PLANNED: Wave 2 Phase 2] |
| MCP runbook | Miro integration operational procedures | `skills/ux-lean-ux/rules/mcp-runbook.md` [PLANNED: Wave 2 Phase 2] |
| Hypothesis backlog template | Hypothesis statement backlog with validation status | `skills/ux-lean-ux/templates/hypothesis-backlog-template.md` [PLANNED: Wave 2 Phase 2] |
| Assumption map template | 4-quadrant assumption mapping worksheet | `skills/ux-lean-ux/templates/assumption-map-template.md` [PLANNED: Wave 2 Phase 2] |
| Skill standards | H-25/H-26 skill structure requirements | `.context/rules/skill-standards.md` |
| Agent development standards | H-34 dual-file architecture, tool tiers, handoff protocol | `.context/rules/agent-development-standards.md` |
| Quality enforcement | Quality gate thresholds, criticality levels, strategy catalog | `.context/rules/quality-enforcement.md` |
| Handoff schema | Canonical handoff schema v2 | `docs/schemas/handoff-v2.schema.json` |
| Agent governance schema | Governance YAML validation schema | `docs/schemas/agent-governance-v1.schema.json` |

### Requirements Traceability

| Source | Content | Path |
|--------|---------|------|
| PROJ-022 PLAN.md | Project plan: sub-skill scope, wave assignment, acceptance criteria, implementation phases | `projects/PROJ-022-user-experience-skill/PLAN.md` |
| EPIC-003 (Wave 2 Deployment) | Parent work item for Wave 2 sub-skill implementation including this sub-skill | PROJ-022 EPIC-003 in `projects/PROJ-022-user-experience-skill/WORKTRACKER.md` |
| FEAT-009 | Feature entity for /ux-lean-ux sub-skill within EPIC-003 | PROJ-022 FEAT-009 in ORCHESTRATION_WORKTRACKER.md |
| ORCHESTRATION.yaml | Orchestration plan governing the build sequence for this sub-skill | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |

### External References

| Source | Citation |
|--------|----------|
| Gothelf, J. & Seiden, J. (2021) | "Lean UX: Applying Lean Principles to Improve User Experience." 3rd ed. O'Reilly. |
| Ries, E. (2011) | "The Lean Startup: How Today's Entrepreneurs Use Continuous Innovation to Create Radically Successful Businesses." Crown Business. Build-Measure-Learn cycle origin. |
| Bland, D. & Osterwalder, A. (2019) | "Testing Business Ideas: A Field Guide for Rapid Experimentation." Wiley. Experiment type catalog. |

---

*Sub-Skill Version: 1.2.0*
*Parent Skill: `/user-experience` v1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Wave: 2 (Data-Ready)*
*SSOT: `skills/user-experience/SKILL.md`*
*Project: PROJ-022 User Experience Skill*
*Created: 2026-03-04*
