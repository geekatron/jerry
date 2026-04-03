---
name: ux-heart-metrics
version: "1.2.0"
description: "HEART Metrics framework sub-skill for the /user-experience parent skill. Applies Google's HEART framework (Happiness, Engagement, Adoption, Retention, Task Success) using the Goals-Signals-Metrics (GSM) process to define measurable UX metrics for products and features. Invoked by ux-orchestrator when users need to measure UX health, define UX metrics, establish measurement baselines, or produce dashboard-ready metric specifications. Sub-skill of /user-experience; routed via ux-orchestrator lifecycle-stage triage. Triggers: HEART, metrics, happiness, engagement, adoption, retention, task success, GSM, measurement, UX metrics, dashboard, goals signals metrics."
activation-keywords:
  - HEART
  - HEART metrics
  - GSM
  - goals signals metrics
  - UX metrics
  - measurement
  - dashboard metrics
  - happiness metrics
  - engagement metrics
  - adoption metrics
  - retention metrics
  - task success metrics
  - baseline measurement
  - metric threshold
model: sonnet
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: PROJ-022-user-experience-skill/PLAN.md | PARENT: /user-experience skill | REVISION: iter2 precision fixes — evidence quality (Baymard specific citation, NPS bibliographic entry, Phase 5 dashboard citation), methodological rigor (goal adjudication guidance, signal-to-metric edge cases), internal consistency (tools/allowed-tools reconciliation, AGENTS.md section-name reference) -->

# HEART Metrics Sub-Skill

> **Version:** 1.2.0
> **Framework:** Jerry User-Experience / HEART Metrics (Google)
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Parent Skill:** `/user-experience` (`skills/user-experience/SKILL.md`)
> **Project:** PROJ-022 User Experience Skill | Wave 2 (Lean UX + Measurement)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Document Audience](#document-audience-triple-lens) | Triple-Lens audience guide |
| [Purpose](#purpose) | What `/ux-heart-metrics` does and key capabilities |
| [When to Use This Sub-Skill](#when-to-use-this-sub-skill) | Activation triggers, routing path, and scope boundaries |
| [Available Agents](#available-agents) | Single agent roster with role, model, and output location |
| [Invoking an Agent](#invoking-an-agent) | Three invocation methods and H-26(c) registration exception |
| [P-003 Compliance](#p-003-compliance) | Worker agent hierarchy position |
| [Methodology](#methodology) | HEART methodology adapted for AI-augmented UX measurement |
| [MCP Integration](#mcp-integration) | MCP dependencies and degraded mode behavior |
| [Output Specification](#output-specification) | Output format, location, and confidence classification |
| [Cross-Framework Integration](#cross-framework-integration) | How HEART output feeds into and receives from other sub-skills |
| [Synthesis Hypothesis Validation](#synthesis-hypothesis-validation) | Confidence gates for AI-synthesized metric recommendations |
| [Constitutional Compliance](#constitutional-compliance) | Governing principles |
| [Quick Reference](#quick-reference) | Common workflows and invocation examples |
| [References](#references) | Full repo-relative paths to all referenced files |

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Product managers, team leads | [Purpose](#purpose), [When to Use This Sub-Skill](#when-to-use-this-sub-skill), [Quick Reference](#quick-reference) |
| **L1 (Developer)** | Engineers invoking the sub-skill | [Methodology](#methodology), [Output Specification](#output-specification), [Available Agents](#available-agents) |
| **L2 (Architect)** | Workflow designers, skill maintainers | [Cross-Framework Integration](#cross-framework-integration), [P-003 Compliance](#p-003-compliance), [Synthesis Hypothesis Validation](#synthesis-hypothesis-validation) |

---

## Purpose

The `/ux-heart-metrics` sub-skill provides AI-augmented UX measurement using Google's HEART framework (Rodden, Hutchinson & Fu, 2010) for tiny teams (1-5 people) who need structured, dashboard-ready UX metrics without a dedicated analytics or UX research team. It guides teams through the Goals-Signals-Metrics (GSM) process to translate abstract UX goals into concrete, measurable indicators.

HEART shifts the team's thinking from "how do we know if our UX is good?" to "what specific user behaviors tell us our UX is improving?" -- enabling data-driven UX decisions even when dedicated analytics resources are limited.

### Key Capabilities

- **HEART Dimension Selection** -- Guides teams to select the subset of HEART dimensions (Happiness, Engagement, Adoption, Retention, Task Success) most relevant to their product or feature, since not all five apply to every context
- **Goals-Signals-Metrics (GSM) Process** -- Structured three-step process for each selected dimension: define the goal, identify behavioral signals, and specify measurable metrics
- **Goal Definition** -- Helps teams articulate what they are trying to improve in user-centered terms (not business metrics) for each selected HEART dimension
- **Signal Identification** -- Identifies observable user behaviors that indicate progress toward each goal, distinguishing leading and lagging indicators
- **Metric Specification** -- Produces dashboard-ready metric definitions including metric name, formula, data source, target threshold, measurement frequency, and alerting conditions
- **Baseline Establishment** -- Guides teams to establish current measurement baselines before implementing changes, enabling before/after comparison
- **Threshold Recommendation** -- Provides directional target values based on industry benchmarks or baseline measurement (LOW confidence -- requires domain-specific calibration)

### AI-Augmented Measurement Caveat

All HEART outputs from this sub-skill are synthesized from secondary research and established framework methodology rather than direct analysis of the product's actual analytics data. Synthesis outputs carry confidence levels that vary by output type:

- **Goal-metric mapping interpretation:** MEDIUM confidence -- the GSM process is methodologically grounded (Rodden, Hutchinson & Fu, 2010) but context-dependent
- **Metric threshold recommendation:** LOW confidence -- threshold values require domain-specific benchmarking data unavailable in training data

See [Synthesis Hypothesis Validation](#synthesis-hypothesis-validation) for the full confidence gate protocol.

> **Deployment status:** Wave 2 sub-skill. The agent definition (`skills/ux-heart-metrics/agents/ux-heart-analyst.md`) is currently a stub with frontmatter and core identity sections. Full implementation (complete `<methodology>`, `<input>`, `<capabilities>`, `<output>` XML-tagged body sections) is a Wave 2 deliverable of PROJ-022. The methodology documented in this SKILL.md describes the target behavior the agent will execute once fully implemented.

---

## When to Use This Sub-Skill

### Activation Path

This sub-skill is invoked by the `ux-orchestrator` agent via the `/user-experience` parent skill's lifecycle-stage routing. It is NOT invoked directly by users.

**Routing path:** User request reaches `/user-experience` via trigger keywords. The `ux-orchestrator` routes to `/ux-heart-metrics` when the user's intent matches:

| Stage Category | User Intent | Route |
|---------------|-------------|-------|
| After launch | "Measure UX health" | `/ux-heart-metrics` |
| Any stage | "Measure whether UX is working" | `/ux-heart-metrics` |
| Any stage | Comprehensive UX audit (multi-sub-skill) | `/ux-heuristic-eval` then `/ux-heart-metrics` |
| CRISIS | Urgent UX problems (step 3 of 3-skill sequence) | `/ux-heart-metrics` |

Source: `skills/user-experience/rules/ux-routing-rules.md` [Stage Routing Table].

### Trigger Keywords

| Keyword | Specificity |
|---------|------------|
| HEART | Primary |
| metrics | Primary |
| GSM | Primary |
| goals signals metrics | Primary |
| UX metrics | Primary |
| measurement | Primary |
| dashboard | Secondary |
| happiness | Secondary |
| engagement | Secondary |
| adoption | Secondary |
| retention | Secondary |
| task success | Secondary |
| baseline | Secondary |
| metric threshold | Secondary |

### Do NOT Use When

| Condition | Use Instead | Why |
|-----------|-------------|-----|
| Understanding what users want to accomplish | `/ux-jtbd` | JTBD discovers underlying jobs; HEART measures outcomes of addressing those jobs |
| Evaluating an existing design against usability standards | `/ux-heuristic-eval` | Heuristic evaluation assesses design quality against Nielsen's 10; HEART measures user behavior |
| Testing and iterating on a hypothesis | `/ux-lean-ux` | Lean UX manages the experiment cycle; HEART measures the outcome |
| Diagnosing why users fail to complete an action | `/ux-behavior-design` | Behavior design (Fogg B=MAP) diagnoses bottlenecks; HEART measures whether the fix worked |
| Prioritizing known features by satisfaction impact | `/ux-kano-model` | Kano classifies feature types; HEART measures impact after implementation |
| General research without UX focus | `/problem-solving` | HEART methodology is UX-specific; general research uses ps-researcher |

---

## Available Agents

| Agent | Role | Tier | Mode | Model | Output Location |
|-------|------|------|------|-------|-----------------|
| `ux-heart-analyst` | HEART metrics framework specialist | T2 | Systematic | Sonnet | `skills/ux-heart-metrics/output/{engagement-id}/ux-heart-analyst-{topic-slug}.md` |

**Single-agent sub-skill.** The `ux-heart-analyst` handles the full HEART methodology -- from dimension selection through metric specification. Complex multi-feature engagements are decomposed into multiple invocations by the `ux-orchestrator`, each targeting a specific product area or feature.

**Tool tier:** T2 (Read-Write). The analyst operates on user-provided data only and does not require external web access for its core methodology. The HEART framework is self-contained in the agent definition and methodology rules. See `skills/ux-heart-metrics/agents/ux-heart-analyst.md` for the full agent definition and `skills/ux-heart-metrics/agents/ux-heart-analyst.governance.yaml` for governance metadata.

---

## Invoking an Agent

### When to Use Each Option

- **Option 1 (Natural Language):** Best for most users. The `ux-orchestrator` handles routing, wave gating, and engagement context automatically. Use this unless you have a specific reason to bypass the orchestrator.
- **Option 2 (Explicit Agent):** When the user knows they specifically need HEART metrics and an engagement context is already established via the parent orchestrator. Direct invocation without an established engagement context bypasses wave gating and lifecycle-stage triage.
- **Option 3 (Agent Tool):** Used by `ux-orchestrator` internally for agent dispatch. Not typically invoked directly by users.

### Option 1: Natural Language Request

Describe your measurement need; the parent `/user-experience` orchestrator routes to `ux-heart-analyst`:

```
"Define HEART metrics for our checkout flow"
"Measure UX health for the onboarding experience"
"Set up a metrics dashboard for the new search feature"
"What metrics should we track after our redesign launches?"
"Establish UX baselines before the navigation update"
```

### Option 2: Explicit Agent Request

Request the agent by name:

```
"Use ux-heart-analyst to define GSM metrics for our settings page"
"Have ux-heart-analyst establish engagement baselines for the mobile app"
"I need ux-heart-analyst to specify task success metrics for the checkout"
```

### Option 3: Native Agent Invocation (Agent Tool)

The `ux-orchestrator` dispatches to `ux-heart-analyst` via Agent:

```python
Agent(
    description="ux-heart-analyst: HEART metrics for checkout flow",
    subagent_type="jerry:ux-heart-analyst",
    prompt="""
## UX CONTEXT (REQUIRED)
- **Engagement ID:** UX-0003
- **Topic:** Checkout Flow HEART Metrics
- **Product:** [product name and domain]
- **Target Users:** [user description]
- **Feature/Flow:** [specific feature or user flow]

## TASK
Define HEART metrics for the checkout flow using the GSM process.
Select applicable HEART dimensions. Produce goal definitions,
signal identification, and dashboard-ready metric specifications.
"""
)
```

Claude Code enforces the agent's `tools` frontmatter -- `ux-heart-analyst` only has access to its declared T2 tool tier (Read, Write, Edit, Glob, Grep).

### Registration (H-26(c) Exception)

`/ux-heart-metrics` is a **sub-skill** of `/user-experience` and is **NOT independently registered** in `CLAUDE.md` or `mandatory-skill-usage.md`. This is by design:

- **Routing:** Users invoke `/user-experience` (registered in `CLAUDE.md` and `mandatory-skill-usage.md`). The `ux-orchestrator` routes to `ux-heart-analyst` based on HEART-related keywords per the lifecycle-stage triage in `skills/user-experience/rules/ux-routing-rules.md`.
- **H-22 trigger map:** The `/user-experience` row in `mandatory-skill-usage.md` includes "HEART metrics, UX metrics" as positive keywords, which covers routing to this sub-skill through the parent orchestrator.
- **AGENTS.md:** The `ux-heart-analyst` agent IS registered in `AGENTS.md` under the User-Experience Skill Agents section, ensuring agent-level discoverability. Verified 2026-03-04.
- **H-26(c) exception rationale:** Sub-skills of orchestrated parent skills inherit routing through the parent's trigger map entry rather than maintaining independent trigger map rows. Independent registration would create duplicate routing paths that bypass the orchestrator's wave gating and lifecycle-stage triage, violating the single-entry-point design of the `/user-experience` skill architecture.

---

## P-003 Compliance

The `ux-heart-analyst` is a **worker agent** within the `/user-experience` orchestrator-worker topology. It does NOT have Agent tool access and MUST NOT spawn sub-agents.

```
MAIN CONTEXT (user request)
    |
    v
ux-orchestrator (T5, Opus, Integrative)
    |
    +-- ux-heart-analyst (T2, Systematic, Sonnet)  <-- THIS SUB-SKILL
    +-- [other sub-skill agents...]
```

**Enforcement:**
- `disallowedTools: [Agent]` declared in `skills/ux-heart-metrics/agents/ux-heart-analyst.md` frontmatter
- P-003 prohibition in `skills/ux-heart-metrics/agents/ux-heart-analyst.governance.yaml` `capabilities.forbidden_actions`
- CI gate validates no sub-skill agent has Agent access (documented in `skills/user-experience/rules/ci-checks.md`)

---

## Methodology

> **Note:** This methodology section describes target behavior for the fully-implemented `ux-heart-analyst` agent. The current agent definition is a Wave 2 stub; full implementation will follow this specification.

The `ux-heart-analyst` follows a structured HEART methodology adapted for AI-augmented UX measurement. The methodology applies Google's HEART framework through the Goals-Signals-Metrics (GSM) process.

### Theoretical Foundation

| Framework | Originators | Year | Core Contribution | Application in This Sub-Skill |
|-----------|------------|------|-------------------|-------------------------------|
| HEART Framework | Kerry Rodden, Hilary Hutchinson, Xin Fu (Google) | 2010 | Five user-centered dimensions for measuring UX at scale: Happiness, Engagement, Adoption, Retention, Task Success | Dimension selection, goal definition, and metric categorization |
| Goals-Signals-Metrics (GSM) | Kerry Rodden et al. (Google) | 2010 | Structured process to translate abstract UX goals into measurable metrics via observable behavioral signals | The core analytical workflow: Goal -> Signal -> Metric for each HEART dimension |

**Source:** Rodden, K., Hutchinson, H., & Fu, X. (2010). "Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications." Proceedings of CHI '10.

### HEART Dimensions

The HEART framework provides five complementary dimensions for measuring user experience. Not all five dimensions apply to every product or feature -- dimension selection is part of the methodology.

| Dimension | Definition | Measures | Example Signal |
|-----------|-----------|----------|---------------|
| **Happiness** | Subjective user satisfaction and attitudes | How users feel about the product | NPS score (calibrate against Bain & Company's industry-specific NPS benchmarks or internal historical data), satisfaction survey rating, sentiment in feedback |
| **Engagement** | User involvement and interaction depth | How much users interact with the product | Session frequency, feature usage depth, time on task (when desirable) |
| **Adoption** | New user uptake and feature discovery | How many new users start using the product/feature | New user signups, feature first-use rate, onboarding completion |
| **Retention** | Continued usage over time | How many users keep coming back | Week-over-week active user ratio, churn rate, renewal rate |
| **Task Success** | Effectiveness, efficiency, and error rate of user tasks | How well users accomplish their goals | Task completion rate, time-on-task, error rate, abandonment rate |

### Dimension Selection Guidelines

| Consideration | Guidance |
|--------------|---------|
| Product maturity | New products: focus on Adoption and Task Success. Mature products: focus on Engagement and Retention. |
| Product type | Transactional (e-commerce): Task Success and Happiness. Content/social: Engagement and Retention. |
| Feature vs. product | Feature-level analysis often requires only 2-3 dimensions. Product-level analysis may use all 5. |
| Team capacity | Tiny teams (1-5 people) should start with 2-3 dimensions to keep measurement manageable. |
| Available data | Select dimensions for which data sources exist or can be reasonably instrumented. |

### Goals-Signals-Metrics (GSM) Process

The GSM process is the core analytical workflow. It is applied sequentially for each selected HEART dimension.

#### Step 1: Goal Definition

**Purpose:** Articulate what the team is trying to improve in user-centered terms.

**Constraints on goals:**
- Goals describe user outcomes, not business outcomes (e.g., "Users complete checkout with confidence" not "Increase revenue")
- Goals are specific to the selected HEART dimension
- Goals are achievable and time-bounded where possible
- Each HEART dimension has exactly one goal statement

> **Goal adjudication:** When multiple goals are plausible for a single dimension, select the goal most directly tied to the product's current lifecycle stage. Document rejected alternatives in the GSM worksheet notes column.

**Goal format:**
```
[HEART Dimension] Goal: [User-centered outcome statement]
```

**Example:**
```
Task Success Goal: Users complete the checkout process without encountering errors or needing help.
```

#### Step 2: Signal Identification

**Purpose:** Identify observable user behaviors that indicate progress toward the goal.

**Activities:**
1. For each goal, brainstorm user behaviors that would indicate the goal is being met
2. Distinguish between leading signals (predictive) and lagging signals (outcome)
3. Assess signal observability: can this behavior be measured with available tooling?
4. Select 2-4 signals per dimension that are both observable and meaningful

**Signal types:**

| Type | Definition | Example |
|------|-----------|---------|
| **Leading** | Behavior that predicts future goal achievement | Feature exploration rate (predicts adoption) |
| **Lagging** | Behavior that confirms past goal achievement | 30-day retention rate (confirms ongoing value) |

#### Step 3: Metric Specification

**Purpose:** Define measurable proxies for each signal with dashboard-ready precision.

**Metric specification fields:**

| Field | Definition | Example |
|-------|-----------|---------|
| **Metric Name** | Descriptive name for the metric | "Checkout Completion Rate" |
| **HEART Dimension** | Which dimension this metric measures | Task Success |
| **Formula** | Precise calculation method | (Completed checkouts / Initiated checkouts) * 100 |
| **Data Source** | Where the raw data comes from | Analytics event: `checkout_completed`, `checkout_initiated` |
| **Measurement Frequency** | How often the metric is calculated | Daily, with weekly trend reports |
| **Target Threshold** | Goal value for the metric | >= 85% (Baymard Institute e-commerce checkout usability benchmark; calibrate against your own baseline -- see [Threshold Fallback Methodology](#threshold-fallback-methodology)) |
| **Alerting Condition** | When to trigger investigation | < 75% for 3 consecutive days |
| **Baseline** | Current measured value (or "TBD: measure before launch") | 78% (measured 2026-01-15 to 2026-01-30) |

> **Signal-to-metric edge cases:** When a single signal maps to multiple metrics, prefer the metric with the shortest feedback loop for iteration decisions. When no signal exists for a goal, flag this as a measurement gap requiring instrumentation investment before the metric can be tracked.

### Evaluation Workflow (planned -- target behavior)

The analyst follows a 5-phase sequential workflow. Each phase produces intermediate artifacts that feed the next.

#### Phase 1: Context Gathering (planned)

**Purpose:** Establish the product domain, feature scope, and available data sources.

**Inputs:** Product description, feature/flow being measured, existing analytics capabilities, user segments.

**Activities:**
1. Identify the product domain and the specific feature or flow to be measured
2. Catalog available data sources (analytics platforms, survey tools, error tracking)
3. Determine measurement maturity: are there existing metrics, or is this greenfield?
4. Identify user segments relevant to measurement (all users, new users, power users, etc.)

**Output:** Context brief documenting domain, feature scope, data source inventory, and measurement maturity.

#### Phase 2: Dimension Selection (planned)

**Purpose:** Select the HEART dimensions most relevant to the product or feature.

**Activities:**
1. Assess each of the five HEART dimensions against the feature/product context
2. Apply the dimension selection guidelines (product maturity, type, scope, capacity, data)
3. Recommend 2-3 dimensions for tiny teams; justify exclusion of dimensions not selected
4. Confirm dimension selection with the user (P-020: user decides which dimensions to measure)

**Output:** Selected dimensions with justification for inclusion and exclusion.

#### Phase 3: GSM Execution (planned)

**Purpose:** Apply the Goals-Signals-Metrics process for each selected dimension.

**Activities:**
1. Define one goal per selected dimension using the goal format
2. Identify 2-4 signals per dimension, classified as leading or lagging
3. Specify one metric per signal using the full metric specification fields
4. Assess data source availability for each metric
5. Flag metrics that require new instrumentation (data source does not yet exist)

**Output:** GSM table per dimension with goals, signals, and metric specifications.

#### Phase 4: Baseline and Threshold Setting (planned)

**Purpose:** Establish current baselines and define target thresholds.

**Activities:**
1. For each metric, determine if a baseline measurement exists
2. If baseline exists: record it with measurement date range
3. If baseline does not exist: specify measurement instructions (what to track, for how long)
4. Recommend target thresholds based on:
   - Industry benchmarks (when available -- cite source)
   - Percentage improvement over baseline (when baseline exists)
   - Domain-specific standards (e.g., WCAG for accessibility metrics)
5. Define alerting conditions: when should a metric trigger investigation?

**Output:** Baseline and threshold table per metric. Threshold recommendations carry LOW confidence (see [Synthesis Hypothesis Validation](#synthesis-hypothesis-validation)).

##### Threshold Fallback Methodology

When no baseline data exists for setting metric thresholds, follow this graduated approach:

| Step | Action | When to Use |
|------|--------|-------------|
| 1 | **Use industry benchmarks** from published studies as starting point (e.g., Baymard Institute for e-commerce, Bain & Company NPS benchmarks by industry) | Published benchmarks exist for the product type and metric category |
| 2 | **Run a 2-week baseline measurement** to establish a stable starting point before setting improvement targets | No published benchmarks match the product type, or the team wants product-specific data |
| 3 | **Set initial target as baseline + 10-15% improvement** over the measured or benchmarked value | Baseline (measured or benchmarked) is available; no domain-specific target exists |
| 4 | **Review and adjust after first measurement cycle** (typically 4-6 weeks of data collection) | Initial target is set; first cycle of real measurement data is available for recalibration |

> **Note:** All threshold values derived from this fallback methodology carry LOW confidence until validated against at least one full measurement cycle of actual product data. See [Synthesis Hypothesis Validation](#synthesis-hypothesis-validation) for confidence advancement criteria.

#### Phase 5: Dashboard Specification (planned)

**Purpose:** Produce a dashboard-ready specification that an engineering team can implement.

**Activities:**
1. Organize metrics by HEART dimension for dashboard layout
2. Specify visualization type per metric (counter, time series, funnel, etc.)
3. Define drill-down paths: what detail should be accessible from each metric?
4. Specify refresh frequency and data latency requirements
5. Produce the Synthesis Judgments Summary listing each AI judgment call

**Output:** Dashboard specification document with metric cards, layout guidance, and instrumentation requirements. Dashboard layout follows metric visualization best practices per Few, S. (2006). *Information Dashboard Design.* Analytics Press; and Rodden, K., Hutchinson, H., & Fu, X. (2010). "Measuring the User Experience on a Large Scale." Proc. CHI 2010, for HEART-specific metric card organization.

---

## MCP Integration

### MCP Dependency Summary

| MCP Tool | Classification | Usage |
|----------|---------------|-------|
| Hotjar (Bridge) | ENH | Session recording and heatmap data for behavioral signal enrichment (future adapter) |
| Context7 | Available (planned for ux-heart-analyst -- see note below) | HEART framework and analytics library documentation lookup |

Source: `skills/user-experience/rules/mcp-coordination.md` [MCP Dependency Matrix].

**No REQ MCP dependencies.** The `/ux-heart-metrics` sub-skill operates at full capability without any required MCP design tool integrations. This makes it suitable for the Free ($0) cost tier (source: `skills/user-experience/SKILL.md` [Cost Tiers]).

### Context7 Usage

> **Note:** `ux-heart-analyst` is not yet listed in `skills/user-experience/rules/mcp-coordination.md` [Context7 Usage] agent table. Context7 integration for this agent is planned for the Wave 2 MCP coordination update. The protocol below describes the target behavior once the agent is added to the coordination matrix.

Per MCP-001 (`.context/rules/mcp-tool-standards.md`), Context7 will be used when the analyst references external analytics frameworks or libraries by name:

| Library/Framework | Usage |
|-------------------|-------|
| Google HEART Framework | GSM process documentation, dimension definitions |
| Analytics libraries (e.g., Mixpanel, Amplitude) | Event tracking API documentation for metric data source specification |

**Protocol:** Call `mcp__context7__resolve-library-id` with the framework name, then `mcp__context7__query-docs` with the resolved ID and specific query. If Context7 returns no results, fall back to WebSearch per `mcp-tool-standards.md` [Error Handling].

### Degraded Mode

When Context7 is unavailable, the analyst falls back to WebSearch for framework documentation. The core HEART methodology is self-contained in the agent definition and `skills/ux-heart-metrics/rules/heart-methodology-rules.md` [PLANNED: Wave 2 Phase 2] -- external documentation lookup enhances precision but is not required for operation.

When Hotjar Bridge MCP becomes available (post-PROJ-022), the analyst will use it for behavioral signal enrichment (heatmaps, session recordings). Without Hotjar, signals are identified from user-provided analytics descriptions and domain knowledge. See `skills/user-experience/rules/mcp-coordination.md` [Future Adapter Fallbacks] for the full degraded mode specification.

### No Analytics Infrastructure

When the product has no analytics infrastructure at all (no event tracking, no dashboards, no data collection), the analyst shifts to **Measurement Plan** mode:

| Aspect | Behavior |
|--------|----------|
| **Output type** | Measurement Plan (instrumentation-first) instead of current-state analysis |
| **Instrumentation recommendations** | Defines an event taxonomy (event names, properties, triggers) and a data model for metric collection |
| **Metric specifications** | Produced as target definitions with `Baseline: TBD -- requires instrumentation` for all metrics |
| **Current-state analysis** | Not possible without data; output explicitly states this limitation per P-022 |
| **Threshold setting** | Deferred entirely; uses [Threshold Fallback Methodology](#threshold-fallback-methodology) Step 2 (run 2-week baseline measurement after instrumentation is live) |
| **Dashboard specification** | Produced as a forward-looking implementation spec, not a current-state visualization |

> **P-022 disclosure:** When operating in Measurement Plan mode, the output header includes: "[MEASUREMENT PLAN MODE] No analytics infrastructure detected. This output defines what to measure and how to instrument it. Current-state metric values are unavailable until instrumentation is implemented and baseline data is collected."

---

## Output Specification

### Output Location

```
skills/ux-heart-metrics/output/{engagement-id}/ux-heart-analyst-{topic-slug}.md
```

Where `{engagement-id}` follows the `UX-{NNNN}` pattern established by the `ux-orchestrator` and `{topic-slug}` is a kebab-case descriptor of the analysis topic.

### Output Structure

All outputs follow the L0/L1/L2 three-level structure per AD-M-004:

| Level | Content | Audience |
|-------|---------|----------|
| **L0 (Executive Summary)** | Selected HEART dimensions, top 3-5 metrics, key measurement gaps, strategic recommendation | Stakeholders, product managers |
| **L1 (Technical Detail)** | Full GSM tables per dimension, metric specifications with formulas and data sources, baseline/threshold tables, dashboard specification | Developers, UX practitioners, analytics engineers |
| **L2 (Strategic Implications)** | Measurement maturity assessment, instrumentation roadmap, metric interdependencies, organizational readiness for data-driven UX | Architects, strategy leads |

### Required Output Sections

| Section | Content | Confidence |
|---------|---------|------------|
| HEART Dimension Selection | Selected dimensions with inclusion/exclusion justification | MEDIUM |
| GSM Tables | Goal, Signals, Metrics per selected dimension | MEDIUM |
| Metric Specifications | Dashboard-ready definitions with formula, data source, frequency | MEDIUM |
| Baseline Assessment | Current measurement status per metric | MEDIUM |
| Threshold Recommendations | Target values and alerting conditions | LOW |
| Dashboard Specification | Layout, visualization types, drill-down paths | MEDIUM |
| Synthesis Judgments Summary | Enumerated list of AI judgment calls | Required (all outputs) |
| Validation Required | Placeholder for named validation source | Required (MEDIUM confidence) |

### Output Format Template

All `ux-heart-analyst` output artifacts SHOULD follow this structure. Copy and populate for each engagement.

```markdown
# HEART Metrics Analysis: {Topic}

## UX Context
- **Engagement ID:** {UX-NNNN}
- **Product:** {product name and domain}
- **Date:** {YYYY-MM-DD}
- **Feature/Flow:** {specific feature or user flow being measured}
- **Target Users:** {user segment description}
- **Synthesis Confidence:** {HIGH|MEDIUM|LOW}

## L0: Executive Summary
- {Key finding 1: selected HEART dimensions and rationale}
- {Key finding 2: highest-priority metric identified}
- {Key finding 3: critical measurement gap}
- {Key finding 4: strategic recommendation}
- {Key finding 5: immediate next step for the team}

## L1: Technical Detail

### HEART Dimension Selection
| Dimension | Selected | Rationale |
|-----------|----------|-----------|
| Happiness | {Yes/No} | {why included or excluded} |
| Engagement | {Yes/No} | {why included or excluded} |
| Adoption | {Yes/No} | {why included or excluded} |
| Retention | {Yes/No} | {why included or excluded} |
| Task Success | {Yes/No} | {why included or excluded} |

### GSM Table: {Dimension Name}
| Component | Content |
|-----------|---------|
| **Goal** | {User-centered outcome statement} |
| **Signal 1** | {Observable behavior} ({Leading/Lagging}) |
| **Signal 2** | {Observable behavior} ({Leading/Lagging}) |
| **Metric 1** | See specification below |
| **Metric 2** | See specification below |

(Repeat GSM table for each selected dimension.)

### Metric Specifications
| Metric Name | HEART Dimension | Formula | Data Source | Frequency | Target | Alert Condition | Baseline |
|-------------|----------------|---------|-------------|-----------|--------|-----------------|----------|
| {name} | {dimension} | {formula} | {source} | {frequency} | {target} | {condition} | {value or TBD} |

### Dashboard Specification
| Metric | Visualization | Drill-Down | Refresh |
|--------|--------------|------------|---------|
| {metric name} | {chart type} | {detail path} | {frequency} |

## L2: Strategic Implications
- {Measurement maturity assessment}
- {Instrumentation roadmap: what needs to be built to collect data}
- {Metric interdependencies: how dimensions relate to each other}
- {Organizational recommendations for data-driven UX practice}

## Synthesis Judgments Summary
1. {AI judgment call 1 -- e.g., "Selected Engagement over Adoption based on product maturity inference; no direct product analytics available"}
2. {AI judgment call 2 -- e.g., "Recommended 85% task completion target based on industry e-commerce benchmarks; actual baseline may differ"}
3. {AI judgment call N -- enumerate all significant AI inferences requiring human acknowledgment}

## Validation Required
- **Validation status:** PENDING
- **Required validation source:** {expert name, analytics data reference, or benchmark citation}
- **Minimum threshold:** {per Synthesis Hypothesis Validation protocol}
```

**Worked Example (Checkout Flow)**

The following shows populated rows from a HEART metrics analysis of an e-commerce checkout flow (engagement UX-0055):

*Dimension Selection:*
| Dimension | Selected | Rationale |
|-----------|----------|-----------|
| Task Success | Yes | Checkout is a goal-directed task; completion rate is the primary success indicator |
| Happiness | Yes | Post-purchase satisfaction directly affects repeat business |
| Retention | No | Retention is a product-level metric; checkout is a feature-level analysis |

*GSM Table:*
| Component | Content |
|-----------|---------|
| **Goal** | Users complete the checkout process without encountering errors or needing help |
| **Signal 1** | Checkout completion without error display (Lagging) |
| **Signal 2** | Time from cart to confirmation page (Leading) |
| **Metric 1** | Checkout Completion Rate |
| **Metric 2** | Checkout Duration (p50) |

*Metric Specification:*
| Metric Name | HEART Dimension | Formula | Data Source | Frequency | Target | Alert Condition | Baseline |
|-------------|----------------|---------|-------------|-----------|--------|-----------------|----------|
| Checkout Completion Rate | Task Success | (completed / initiated) * 100 | Analytics: `checkout_completed`, `checkout_initiated` | Daily | >= 85% (Baymard Institute e-commerce checkout usability benchmark) | < 75% for 3 days | 78% (2026-01-15 to 2026-01-30) |

---

## Cross-Framework Integration

HEART output serves as downstream measurement for multiple upstream sub-skills. The `ux-orchestrator` manages handoff data between sub-skills via the Jerry handoff protocol (`docs/schemas/handoff-v2.schema.json` -- planned; not yet committed to repository; schema specified in `.context/rules/agent-development-standards.md` [Handoff Protocol]).

### Upstream Handoff Contracts (Receives From)

| From Sub-Skill | Handoff Artifact | Key Fields | Use Case |
|---------------|-----------------|-----------|----------|
| `/ux-lean-ux` | Validated/invalidated hypothesis backlog | Hypothesis ID, validated/invalidated status, metric implications | Hypotheses inform which HEART metrics to track and which targets to set based on experiment outcomes |
| `/ux-heuristic-eval` | Severity-rated findings with metric candidates | Finding ID, heuristic violated, severity (0-4), affected screen/flow, candidate HEART metric category | Heuristic findings inform which HEART dimensions to prioritize and which signals to track |
| `/ux-behavior-design` (CRISIS sequence) | B=MAP bottleneck diagnosis | Bottleneck type (Motivation/Ability/Prompt), affected flow, severity | In CRISIS mode, bottleneck diagnoses inform metric baselines and alert thresholds |

Source: `skills/user-experience/rules/ux-routing-rules.md` [Handoff Data Contracts] and `skills/user-experience/SKILL.md` [Cross-Sub-Skill Handoff Data].

### Upstream Dependencies

| From | Artifact Received | Usage |
|------|-------------------|-------|
| `ux-orchestrator` | Engagement context (product domain, feature scope, UX capacity) | Scopes the HEART analysis to the relevant domain and feature |
| `/ux-lean-ux` (standard flow) | Hypothesis backlog with validation status | Maps validated/invalidated hypotheses to HEART dimension goals and signals |
| `/ux-heuristic-eval` (comprehensive audit and CRISIS) | Severity-rated findings | Drives dimension selection and signal prioritization based on identified UX problems |

### Integration Workflow Examples

**Sprint to Iterate to Measure (Canonical Sequence):**
```
/ux-design-sprint (validated prototype + Day 4 findings)
    |
    v
/ux-lean-ux (hypothesis-driven iteration;
            produces validated/invalidated hypothesis backlog)
    |
    v
/ux-heart-metrics (HEART metrics to quantify
                   hypothesis outcomes and track improvements)
```

**Evaluate to Diagnose to Measure (CRISIS Sequence):**
```
/ux-heuristic-eval (severity-rated findings)
    |
    v
/ux-behavior-design (B=MAP bottleneck diagnosis)
    |
    v
/ux-heart-metrics (metric baselines + targets
                   to track whether fixes improve UX)
```

**Comprehensive UX Audit:**
```
/ux-heuristic-eval (severity-rated findings + metric candidates)
    |
    v
/ux-heart-metrics (HEART metrics aligned to
                   heuristic findings for quantitative tracking)
```

---

## Synthesis Hypothesis Validation

All HEART outputs from this sub-skill carry confidence classifications that vary by output type, enforced by the confidence gate protocol defined in `skills/user-experience/rules/synthesis-validation.md`.

### Confidence Gate Behavior for HEART Metrics

| Output Type | Confidence | Gate Behavior |
|-------------|-----------|---------------|
| Goal-metric mapping interpretation | **MEDIUM** | Requires expert review OR validation against real analytics data before advancing to implementation decisions |
| Metric threshold recommendation | **LOW** | Output permanently labeled reference-only for threshold values; threshold section structurally tagged with `[REFERENCE-ONLY]`. Notice: "Threshold values reflect AI synthesis from industry benchmarks. They do not constitute validated targets for your product." |

Source: `skills/user-experience/rules/synthesis-validation.md` [Sub-Skill Synthesis Output Map] and `skills/user-experience/SKILL.md` [Sub-Skill Synthesis Output Map].

**Gate enforcement:** HEART output includes a "Validation Required" section with a placeholder for the named validation source (analytics data reference, domain expert, or benchmark study citation). Implementation recommendations for metric instrumentation are provided at MEDIUM confidence. Threshold values are always presented as reference-only at LOW confidence -- the team must calibrate against their own baseline data. The `ux-orchestrator` enforces this gate at handoff boundaries -- downstream consumers receive the confidence classification and propagate it per `skills/user-experience/rules/synthesis-validation.md` [Confidence Propagation].

### What "Validation" Means for HEART Metrics

Validation sources that advance MEDIUM to HIGH confidence:

| Validation Method | Minimum Threshold | Example |
|-------------------|------------------|---------|
| Analytics data correlation | 2+ weeks of actual metric data from the product | "Measured checkout completion rate at 78% over 14 days using Mixpanel event tracking" |
| Expert review by analytics practitioner | Named expert with measurement domain authority | "Reviewed by [Name], Head of Analytics at [Company]" |
| A/B test baseline | Control group data establishing pre-change measurement | "A/B test control group (n=500) establishes 82% task completion baseline" |
| Industry benchmark study with matching context | Published study matching product type and user segment | "Baymard Institute (2024) reports 69.8% average cart abandonment rate for e-commerce" |

Validation sources that advance LOW threshold recommendations to MEDIUM:

| Validation Method | Minimum Threshold | Example |
|-------------------|------------------|---------|
| Domain-specific baseline measurement | 4+ weeks of actual metric data establishing a stable baseline | "Measured 30-day retention at 42% over 6 weeks; threshold set at 50% (20% improvement target)" |
| Published industry benchmark with matched context | Peer-reviewed or major industry report matching product type | "SaaS benchmark report: median 30-day retention = 45%; set target at >= 45%" |

---

## Constitutional Compliance

| Principle | Requirement | Sub-Skill Application |
|-----------|-------------|----------------------|
| P-003 | NEVER spawn recursive subagents | Worker agent; no Agent tool access. Returns results to ux-orchestrator. |
| P-020 | NEVER override user intent | User decides which HEART dimensions to measure, which metrics to implement, and whether to act on LOW-confidence threshold recommendations. |
| P-022 | NEVER deceive about actions, capabilities, or confidence | Goal-metric mappings transparently classified as MEDIUM confidence. Threshold recommendations classified as LOW confidence with `[REFERENCE-ONLY]` tag. Synthesis Judgments Summary enumerates all AI judgment calls. |
| P-001 | NEVER present findings without evidence or source citations | All metric recommendations cite the HEART framework (Rodden, Hutchinson & Fu, 2010). Industry benchmarks cite specific studies. |
| P-002 | NEVER leave outputs in transient context only | All outputs persisted to `skills/ux-heart-metrics/output/{engagement-id}/`. |

---

## Quick Reference

### Common Workflows

| Need | Command Example |
|------|-----------------|
| Define UX metrics for a feature | "Define HEART metrics for our checkout flow" |
| Measure UX health post-launch | "Measure UX health for the new onboarding experience" |
| Establish baselines before a redesign | "Establish UX measurement baselines before the navigation update" |
| Create a metrics dashboard spec | "Specify a HEART metrics dashboard for the mobile app" |
| Quantify heuristic findings | "Map our heuristic evaluation findings to measurable HEART metrics" |
| CRISIS measurement | "CRISIS: users are abandoning checkout" (orchestrator includes HEART as step 3) |

### Agent Selection Hints

| Keywords | Routes To |
|----------|-----------|
| HEART, metrics, happiness, engagement, adoption, retention, task success, GSM, measurement, dashboard, UX metrics, baseline, threshold | `ux-heart-analyst` |

---

## References

### Agent Definition Files

| Agent | Definition | Governance |
|-------|-----------|------------|
| ux-heart-analyst | `skills/ux-heart-metrics/agents/ux-heart-analyst.md` | `skills/ux-heart-metrics/agents/ux-heart-analyst.governance.yaml` |

### Parent Skill

| Item | Location |
|------|----------|
| Parent SKILL.md | `skills/user-experience/SKILL.md` |
| Routing rules | `skills/user-experience/rules/ux-routing-rules.md` |
| Synthesis validation | `skills/user-experience/rules/synthesis-validation.md` |
| MCP coordination | `skills/user-experience/rules/mcp-coordination.md` |
| Wave progression | `skills/user-experience/rules/wave-progression.md` |
| CI checks | `skills/user-experience/rules/ci-checks.md` |

### Standards References

| Standard | Location |
|----------|----------|
| Agent Definition Format (H-34) | `.context/rules/agent-development-standards.md` |
| Skill Standards (H-25, H-26) | `.context/rules/skill-standards.md` |
| Quality Enforcement SSOT | `.context/rules/quality-enforcement.md` |
| Agent Routing Standards (H-36) | `.context/rules/agent-routing-standards.md` |
| MCP Tool Standards | `.context/rules/mcp-tool-standards.md` |
| Handoff Schema | `docs/schemas/handoff-v2.schema.json` (planned -- not yet committed to repository; schema specified in `.context/rules/agent-development-standards.md` [Handoff Protocol]) |

### Methodology Rules

| Item | Location |
|------|----------|
| HEART methodology rules (includes GSM template) | `skills/ux-heart-metrics/rules/heart-methodology-rules.md` [PLANNED: Wave 2 Phase 2] |

### Project Traceability

| Item | Location |
|------|----------|
| Project plan | `projects/PROJ-022-user-experience-skill/PLAN.md` |
| Parent work item | EPIC-003 (Wave 2 deployment) |
| Orchestration plan | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |

### HEART Framework References

| Framework | Source | Year | URL |
|-----------|--------|------|-----|
| HEART Framework (primary) | Kerry Rodden, Hilary Hutchinson, Xin Fu (Google) | 2010 | Rodden, K., Hutchinson, H., & Fu, X. (2010). "Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications." Proceedings of CHI '10, ACM. |
| Goals-Signals-Metrics (GSM) | Kerry Rodden (Google) | 2010 | Described within the HEART paper (Rodden et al., 2010). Also: Rodden, K. (2015). "How to Choose the Right UX Metrics for Your Product." Google Research Blog. |
| HEART Framework practitioner guide | Kerry Rodden | 2015 | Rodden, K. (2015). "Measuring the User Experience on a Large Scale." Google Ventures Library. Practical guidance for applying GSM process in product teams. |
| Baymard Institute UX Benchmark | Baymard Institute | 2020-2024 | Baymard Institute. "UX Benchmark" dataset (2020-2024). Available at https://baymard.com/ux-benchmark. Cart abandonment and checkout usability benchmarks. Note: practitioners should verify current benchmark values against the latest dataset release. |
| Net Promoter Score (NPS) | Fred Reichheld / Bain & Company | 2003 | Reichheld, F.F. (2003). "The One Number You Need to Grow." *Harvard Business Review*, 81(12), 46-54. Originally developed at Bain & Company with Satmetrix Systems. Industry-specific NPS benchmarks available via Bain & Company. |
| Information Dashboard Design | Stephen Few | 2006 | Few, S. (2006). *Information Dashboard Design: The Effective Visual Communication of Data.* Analytics Press. Best practices for metric visualization and dashboard layout. |

---

<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: PROJ-022-user-experience-skill/PLAN.md | PARENT: /user-experience skill | REVISION: iter2 precision fixes — evidence quality (Baymard specific citation, NPS bibliographic entry, Phase 5 dashboard citation), methodological rigor (goal adjudication guidance, signal-to-metric edge cases), internal consistency (tools/allowed-tools reconciliation, AGENTS.md section-name reference) -->
*Sub-Skill Version: 1.2.0*
*Parent Skill: `/user-experience` (`skills/user-experience/SKILL.md`)*
*Constitutional Compliance: Jerry Constitution v1.0 (P-003, P-020, P-022, P-001, P-002)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Project: PROJ-022 User Experience Skill | Wave 2*
*Created: 2026-03-04*
*Revised: 2026-03-04 (v1.2.0 — iter2 precision fixes: Baymard specific citation, NPS bibliographic entry, Phase 5 dashboard citation, goal adjudication guidance, signal-to-metric edge cases, tools/allowed-tools reconciliation, AGENTS.md section-name reference)*
*Agent: ux-heart-analyst*
