---
name: ux-jtbd
description: "Jobs-to-Be-Done research and analysis sub-skill for the /user-experience parent skill. Conducts JTBD job statement synthesis, switch interview analysis (Moesta/Spiek four forces), outcome-driven innovation (Ulwick ODI), and job mapping for tiny teams (1-5 people). Invoked by ux-orchestrator when users need to understand user motivations, map jobs to be done, identify switch triggers, or produce job maps with outcome expectations. Sub-skill of /user-experience; routed via ux-orchestrator lifecycle-stage triage. Triggers: JTBD, jobs to be done, switch interview, job mapping, user motivation, outcome, hiring criteria, user jobs, switch forces."
model: sonnet
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
---

<!-- VERSION: 1.0.0 | DATE: 2026-03-04 | SOURCE: PROJ-022-user-experience-skill/PLAN.md | PARENT: /user-experience skill -->

# JTBD Sub-Skill

> **Version:** 1.0.0
> **Framework:** Jerry User-Experience / Jobs-to-Be-Done
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Parent Skill:** `/user-experience` (`skills/user-experience/SKILL.md`)
> **Project:** PROJ-022 User Experience Skill | Wave 1 (Zero-Dependency)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Document Audience](#document-audience-triple-lens) | Triple-Lens audience guide |
| [Purpose](#purpose) | What `/ux-jtbd` does and key capabilities |
| [When to Use This Sub-Skill](#when-to-use-this-sub-skill) | Activation triggers, routing path, and scope boundaries |
| [Available Agents](#available-agents) | Single agent roster with role, model, and output location |
| [Invoking an Agent](#invoking-an-agent) | Three invocation methods and H-26(c) registration exception |
| [P-003 Compliance](#p-003-compliance) | Worker agent hierarchy position |
| [Methodology](#methodology) | JTBD methodology adapted for AI-augmented research |
| [MCP Integration](#mcp-integration) | MCP dependencies and degraded mode behavior |
| [Output Specification](#output-specification) | Output format, location, and confidence classification |
| [Cross-Framework Integration](#cross-framework-integration) | How JTBD output feeds into other sub-skills |
| [Synthesis Hypothesis Validation](#synthesis-hypothesis-validation) | Confidence gates for AI-synthesized job statements |
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

The `/ux-jtbd` sub-skill provides AI-augmented Jobs-to-Be-Done research and analysis for tiny teams (1-5 people) who lack the resources for traditional primary user research. It synthesizes job statements, switch forces, and outcome expectations from secondary research sources, producing structured artifacts that feed into downstream UX sub-skills.

JTBD shifts the team's thinking from "what features should we build?" to "what jobs are users trying to accomplish?" -- enabling demand-side innovation strategy even when direct user access is limited.

### Key Capabilities

- **Job Statement Synthesis** -- Produces structured job statements in the canonical format: "When [situation], I want to [motivation], so I can [expected outcome]"
- **Switch Interview Analysis** -- Applies Moesta/Spiek four forces framework (push, pull, anxiety, habit) to understand why users switch to or abandon products
- **Outcome-Driven Innovation** -- Applies Ulwick's ODI approach to identify underserved and overserved outcomes for innovation opportunity scoring
- **Job Mapping** -- Decomposes complex user jobs into sequential job steps with associated outcome expectations
- **Hiring Criteria Identification** -- Determines the criteria users apply when "hiring" a product for a specific job
- **Competitive Job Analysis** -- Maps how competing products address the same user jobs to identify differentiation opportunities

### AI-Augmented Research Caveat

All JTBD outputs from this sub-skill are synthesized from secondary research (competitive analysis, domain literature, product documentation, analogous contexts) rather than primary user interviews. Synthesis outputs carry **MEDIUM confidence** by default. This means:

- Job statements reflect AI-synthesized patterns from training data, not validated user motivations
- Switch forces are inferred from secondary evidence, not observed in real switch interviews
- All outputs require validation against real user data before informing design decisions

See [Synthesis Hypothesis Validation](#synthesis-hypothesis-validation) for the full confidence gate protocol.

> **Deployment status:** Wave 1 sub-skill. The agent definition (`skills/ux-jtbd/agents/ux-jtbd-analyst.md`) is currently a stub with frontmatter and core identity sections. Full implementation (complete `<methodology>`, `<input>`, `<capabilities>`, `<output>` XML-tagged body sections) is a Wave 1 deliverable of PROJ-022. The methodology documented in this SKILL.md describes the target behavior the agent will execute once fully implemented.

---

## When to Use This Sub-Skill

### Activation Path

This sub-skill is invoked by the `ux-orchestrator` agent via the `/user-experience` parent skill's lifecycle-stage routing. It is NOT invoked directly by users.

**Routing path:** User request reaches `/user-experience` via trigger keywords. The `ux-orchestrator` routes to `/ux-jtbd` when the user's intent matches:

| Stage Category | User Intent | Route |
|---------------|-------------|-------|
| Before design | "Don't know what to build" | `/ux-jtbd` |
| Before design | "Decide what to build" (strategic, defining the problem) | `/ux-jtbd` |
| Any stage | Understand user motivations, map user jobs | `/ux-jtbd` |

Source: `skills/user-experience/rules/ux-routing-rules.md` [Stage Routing Table].

### Trigger Keywords

| Keyword | Specificity |
|---------|------------|
| jobs to be done | Primary |
| JTBD | Primary |
| switch interview | Primary |
| job mapping | Primary |
| user motivation | Primary |
| hiring criteria | Primary |
| user jobs | Primary |
| outcome expectations | Secondary |
| switch forces | Secondary |
| push/pull forces | Secondary |
| demand-side innovation | Secondary |

### Do NOT Use When

| Condition | Use Instead | Why |
|-----------|-------------|-----|
| Prioritizing known features by satisfaction impact | `/ux-kano-model` | Kano classifies known features; JTBD discovers underlying jobs |
| Evaluating an existing design against usability standards | `/ux-heuristic-eval` | Heuristic evaluation assesses design quality, not user motivations |
| Measuring UX metrics after launch | `/ux-heart-metrics` | HEART measures outcomes; JTBD identifies the jobs driving those outcomes |
| Diagnosing why users fail to complete an action | `/ux-behavior-design` | Behavior design (Fogg B=MAP) diagnoses behavioral bottlenecks; JTBD maps the underlying job |
| General research without UX focus | `/problem-solving` | JTBD methodology is UX-specific; general research uses ps-researcher |

---

## Available Agents

| Agent | Role | Tier | Mode | Model | Output Location |
|-------|------|------|------|-------|-----------------|
| `ux-jtbd-analyst` | JTBD research and analysis specialist | T4 | Divergent | Sonnet | `skills/ux-jtbd/output/{engagement-id}/ux-jtbd-analyst-{topic-slug}.md` |

**Single-agent sub-skill.** The `ux-jtbd-analyst` handles the full JTBD methodology -- from context gathering through job statement synthesis. Complex multi-job engagements are decomposed into multiple invocations by the `ux-orchestrator`, each targeting a specific job domain.

**Tool tier:** T4 (External). The analyst uses WebSearch and WebFetch for secondary research (competitive analysis, domain literature, product reviews) and Context7 for JTBD framework documentation lookup. See `skills/ux-jtbd/agents/ux-jtbd-analyst.md` for the full agent definition and `skills/ux-jtbd/agents/ux-jtbd-analyst.governance.yaml` for governance metadata.

---

## Invoking an Agent

### When to Use Each Option

- **Option 1 (Natural Language):** Best for most users. The `ux-orchestrator` handles routing, wave gating, and engagement context automatically. Use this unless you have a specific reason to bypass the orchestrator.
- **Option 2 (Explicit Agent):** When the user knows they specifically need JTBD analysis and an engagement context is already established via the parent orchestrator. Direct invocation without an established engagement context bypasses wave gating and lifecycle-stage triage.
- **Option 3 (Agent Tool):** Used by `ux-orchestrator` internally for agent dispatch. Not typically invoked directly by users.

### Option 1: Natural Language Request

Describe your JTBD need; the parent `/user-experience` orchestrator routes to `ux-jtbd-analyst`:

```
"Map the jobs to be done for our onboarding flow"
"Identify switch triggers for our new feature"
"Run a JTBD interview analysis for our checkout experience"
"Understand why users are switching from [competitor]"
"What jobs are users hiring our product to do?"
```

### Option 2: Explicit Agent Request

Request the agent by name:

```
"Use ux-jtbd-analyst to analyze our user interview transcripts"
"Have ux-jtbd-analyst map job statements for the settings page"
"I need ux-jtbd-analyst to identify underserved outcomes in our workflow"
```

### Option 3: Native Agent Invocation (Agent Tool)

The `ux-orchestrator` dispatches to `ux-jtbd-analyst` via Agent:

```python
Agent(
    description="ux-jtbd-analyst: Jobs-to-Be-Done analysis for onboarding flow",
    subagent_type="jerry:ux-jtbd-analyst",
    prompt="""
## UX CONTEXT (REQUIRED)
- **Engagement ID:** UX-0001
- **Topic:** Onboarding Flow JTBD Analysis
- **Product:** [product name and domain]
- **Target Users:** [user description]

## TASK
Conduct a Jobs-to-Be-Done analysis for the onboarding flow.
Map functional, social, and emotional jobs. Identify switch triggers.
Produce job map with outcome expectations using Ulwick ODI format.
"""
)
```

Claude Code enforces the agent's `tools` frontmatter -- `ux-jtbd-analyst` only has access to its declared T4 tool tier (Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch).

### Registration (H-26(c) Exception)

`/ux-jtbd` is a **sub-skill** of `/user-experience` and is **NOT independently registered** in `CLAUDE.md` or `mandatory-skill-usage.md`. This is by design:

- **Routing:** Users invoke `/user-experience` (registered in `CLAUDE.md` and `mandatory-skill-usage.md`). The `ux-orchestrator` routes to `ux-jtbd-analyst` based on JTBD-related keywords per the lifecycle-stage triage in `skills/user-experience/rules/ux-routing-rules.md`.
- **H-22 trigger map:** The `/user-experience` row in `mandatory-skill-usage.md` includes "JTBD, jobs to be done" as positive keywords, which covers routing to this sub-skill through the parent orchestrator.
- **AGENTS.md:** The `ux-jtbd-analyst` agent IS registered in `AGENTS.md` under the User-Experience Skill Agents section (line 307), ensuring agent-level discoverability. Verified 2026-03-04.
- **H-26(c) exception rationale:** Sub-skills of orchestrated parent skills inherit routing through the parent's trigger map entry rather than maintaining independent trigger map rows. Independent registration would create duplicate routing paths that bypass the orchestrator's wave gating and lifecycle-stage triage, violating the single-entry-point design of the `/user-experience` skill architecture.

---

## P-003 Compliance

The `ux-jtbd-analyst` is a **worker agent** within the `/user-experience` orchestrator-worker topology. It does NOT have Agent tool access and MUST NOT spawn sub-agents.

```
MAIN CONTEXT (user request)
    |
    v
ux-orchestrator (T5, Opus, Integrative)
    |
    +-- ux-jtbd-analyst (T4, Divergent, Sonnet)  <-- THIS SUB-SKILL
    +-- [other sub-skill agents...]
```

**Enforcement:**
- `disallowedTools: [Agent]` declared in `skills/ux-jtbd/agents/ux-jtbd-analyst.md` frontmatter
- P-003 prohibition in `skills/ux-jtbd/agents/ux-jtbd-analyst.governance.yaml` `capabilities.forbidden_actions`
- CI gate validates no sub-skill agent has Agent access (documented in `skills/user-experience/rules/ci-checks.md`)

---

## Methodology

> **Note:** This methodology section describes target behavior for the fully-implemented `ux-jtbd-analyst` agent. The current agent definition is a Wave 1 stub; full implementation will follow this specification.

The `ux-jtbd-analyst` follows a structured JTBD research methodology adapted for AI-augmented secondary research. The methodology synthesizes three complementary JTBD approaches.

### Theoretical Foundations

| Approach | Originator | Core Contribution | Application in This Sub-Skill |
|----------|-----------|-------------------|-------------------------------|
| Jobs-to-Be-Done Theory | Clayton Christensen et al. (2016) | Products are "hired" for jobs; innovation comes from understanding why | Job statement format and hiring criteria identification |
| Outcome-Driven Innovation (ODI) | Anthony Ulwick (2005, 2016) | Jobs are stable; outcomes are measurable; innovation opportunity = importance + dissatisfaction | Outcome expectation mapping and opportunity scoring |
| Switch Interview Framework | Bob Moesta (2020) | Four forces drive switching behavior: push, pull, anxiety, habit | Switch force analysis for understanding adoption/abandonment |

### Job Statement Format

All job statements follow the canonical three-part format:

```
"When [situation], I want to [motivation], so I can [expected outcome]."
```

| Component | Definition | Example |
|-----------|-----------|---------|
| **Situation** | The context or circumstance triggering the job | "When I receive a new customer inquiry" |
| **Motivation** | The core action the user wants to accomplish | "I want to quickly assess their needs" |
| **Expected Outcome** | The desired end state or benefit | "so I can route them to the right team within 5 minutes" |

**Constraints on job statements:**
- Jobs describe the user's goal, not the product's features
- Jobs are solution-agnostic -- they do not reference specific products or implementations
- Jobs are stable over time -- underlying human motivations change slowly
- Each job statement targets a single functional, social, or emotional dimension

### Evaluation Workflow (planned -- target behavior)

The analyst follows a 5-phase sequential workflow. Each phase produces intermediate artifacts that feed the next.

#### Phase 1: Context Gathering (planned)

**Purpose:** Establish the product domain, target users, and competitive landscape.

**Inputs:** Product description, user segments, existing research (if any), competitive context.

**Activities:**
1. Identify the product domain and value proposition
2. Define primary user segments (who "hires" the product)
3. Survey the competitive landscape -- which products compete for the same jobs
4. Catalog existing user research, support tickets, reviews, or analytics data

**Output:** Context brief documenting domain, users, competitors, and available evidence sources.

#### Phase 2: Job Identification (planned)

**Purpose:** Discover the functional, social, and emotional jobs users are trying to accomplish.

**Activities:**
1. Analyze the product domain for core functional jobs (what users want to accomplish)
2. Identify social jobs (how users want to be perceived by others)
3. Identify emotional jobs (how users want to feel)
4. Map related jobs that cluster around the same use context
5. Distinguish between main jobs (primary purpose) and related jobs (adjacent needs)

**Job types:**

| Job Type | Definition | Example |
|----------|-----------|---------|
| **Functional** | The practical task the user wants to accomplish | "Organize project tasks by priority" |
| **Social** | How the user wants to be perceived | "Appear organized and in control to my team" |
| **Emotional** | How the user wants to feel | "Feel confident that nothing is falling through the cracks" |

**Output:** Draft job inventory with type classification and preliminary job statements.

#### Phase 3: Switch Force Analysis (planned)

**Purpose:** Apply the Moesta/Spiek four forces framework to understand switching behavior.

The four forces model explains why users switch between products (or from non-consumption to consumption):

```
PUSH (current situation pain)  +  PULL (new solution attraction)
                    vs.
ANXIETY (uncertainty about new)  +  HABIT (comfort with current)

Switch happens when PUSH + PULL > ANXIETY + HABIT
```

| Force | Direction | Description | Evidence Sources |
|-------|-----------|-------------|-----------------|
| **Push** | Drives change | Pain points, frustrations, and limitations of the current solution | Support tickets, negative reviews, churn data |
| **Pull** | Drives change | Attractive features, outcomes, and promises of the new solution | Marketing copy, positive reviews, trial signups |
| **Anxiety** | Resists change | Fears about switching: data loss, learning curve, cost, compatibility | FAQ pages, onboarding drop-off, trial abandonment |
| **Habit** | Resists change | Comfort with the current solution, workflow inertia, sunk costs | Feature usage patterns, integration depth, tenure data |

**Activities:**
1. For each identified job, catalog push forces (what pushes users away from their current approach)
2. Catalog pull forces (what attracts users to a new approach)
3. Catalog anxiety forces (what makes users hesitant to switch)
4. Catalog habit forces (what keeps users attached to their current approach)
5. Assess the force balance: do push+pull outweigh anxiety+habit?

**Output:** Switch force analysis per job, with force balance assessment.

#### Phase 4: Job Mapping (planned)

**Purpose:** Decompose each main job into sequential job steps with outcome expectations.

Job mapping follows Ulwick's ODI methodology: a job is decomposed into a universal job process (define, locate, prepare, confirm, execute, monitor, modify, conclude) adapted to the specific domain.

| Job Step | Universal Process | Description |
|----------|------------------|-------------|
| 1 | **Define** | Determine what needs to be accomplished |
| 2 | **Locate** | Find the inputs needed to accomplish the job |
| 3 | **Prepare** | Set up the environment or inputs for execution |
| 4 | **Confirm** | Verify readiness before executing |
| 5 | **Execute** | Perform the core action |
| 6 | **Monitor** | Track progress during execution |
| 7 | **Modify** | Make adjustments based on monitoring feedback |
| 8 | **Conclude** | Complete the job and transition to the next activity |

**Activities:**
1. Decompose each main job into sequential steps following the universal process
2. For each step, define 3-5 outcome expectations using Ulwick's three canonical outcome formats:
   - "Minimize the time it takes to [step action]"
   - "Minimize the likelihood of [undesired outcome]"
   - "Minimize the variability of [quality measure]"
3. Assess each outcome's importance (how much users care) and satisfaction (how well current solutions deliver)
4. Calculate opportunity score: Importance + max(Importance - Satisfaction, 0)

**Output:** Job map per main job with step-level outcome expectations and opportunity scores.

#### Phase 5: Job Statement Synthesis (planned)

**Purpose:** Produce final, validated job statements with hiring criteria and confidence classifications.

**Activities:**
1. Refine job statements into the canonical "When [situation], I want to [motivation], so I can [expected outcome]" format
2. Define hiring criteria: the measurable attributes users evaluate when "hiring" a product for each job
3. Rank jobs by strategic importance (opportunity score, force balance, job frequency)
4. Assign confidence classification per the synthesis hypothesis validation protocol
5. Produce the Synthesis Judgments Summary listing each AI judgment call

**Output:** Final job statement report with hiring criteria, confidence classifications, and synthesis judgments summary.

---

## MCP Integration

### MCP Dependency Summary

| MCP Tool | Classification | Usage |
|----------|---------------|-------|
| Miro | ENH | Board collaboration for job mapping workshops (future adapter) |
| Context7 | Available | JTBD framework documentation lookup |

Source: `skills/user-experience/rules/mcp-coordination.md` [MCP Dependency Matrix].

**No REQ MCP dependencies.** The `/ux-jtbd` sub-skill operates at full capability without any required MCP design tool integrations. This makes it a zero-dependency sub-skill suitable for Wave 1 deployment and the Free ($0) cost tier.

### Context7 Usage

Per MCP-001 (`.context/rules/mcp-tool-standards.md`), Context7 is used when the analyst references external JTBD frameworks or libraries by name:

| Library/Framework | Usage |
|-------------------|-------|
| Jobs-to-Be-Done framework | ODI methodology documentation, job statement format reference |
| Intercom JTBD | Switch interview framework documentation |

**Protocol:** Call `mcp__context7__resolve-library-id` with the framework name, then `mcp__context7__query-docs` with the resolved ID and specific query. If Context7 returns no results, fall back to WebSearch per `mcp-tool-standards.md` [Error Handling].

### Degraded Mode

When Context7 is unavailable, the analyst falls back to WebSearch for JTBD framework documentation. The core methodology is self-contained in the agent definition -- external documentation lookup enhances precision but is not required for operation.

When Miro MCP becomes available (post-PROJ-022), the analyst will use it for collaborative job mapping boards. Without Miro, job maps are produced as structured text tables. See `skills/user-experience/rules/mcp-coordination.md` [Future Adapter Fallbacks] for the full degraded mode specification.

---

## Output Specification

### Output Location

```
skills/ux-jtbd/output/{engagement-id}/ux-jtbd-analyst-{topic-slug}.md
```

Where `{engagement-id}` follows the `UX-{NNNN}` pattern established by the `ux-orchestrator` and `{topic-slug}` is a kebab-case descriptor of the analysis topic.

### Output Structure

All outputs follow the L0/L1/L2 three-level structure per AD-M-004:

| Level | Content | Audience |
|-------|---------|----------|
| **L0 (Executive Summary)** | Top 3-5 job statements, key switch forces, strategic recommendation | Stakeholders, product managers |
| **L1 (Technical Detail)** | Full job inventory, switch force analysis per job, job maps with outcome expectations, hiring criteria, opportunity scores | Developers, UX practitioners |
| **L2 (Strategic Implications)** | Competitive job landscape, unmet outcome opportunities, cross-product job patterns, innovation trajectory | Architects, strategy leads |

### Required Output Sections

| Section | Content | Confidence |
|---------|---------|------------|
| Job Statement Inventory | All identified jobs in canonical format with type classification | MEDIUM |
| Switch Force Analysis | Four forces per job with force balance assessment | MEDIUM |
| Job Map | Step-level decomposition with outcome expectations | MEDIUM |
| Hiring Criteria | Measurable attributes users apply when selecting a product | MEDIUM |
| Opportunity Scores | Importance + dissatisfaction scoring per outcome | MEDIUM |
| Synthesis Judgments Summary | Enumerated list of AI judgment calls | Required (all outputs) |
| Validation Required | Placeholder for named validation source | Required (MEDIUM confidence) |

### Output Format Template

All `ux-jtbd-analyst` output artifacts SHOULD follow this structure. Copy and populate for each engagement.

```markdown
# JTBD Analysis: {Topic}

## UX Context
- **Engagement ID:** {UX-NNNN}
- **Product:** {product name and domain}
- **Date:** {YYYY-MM-DD}
- **Target Users:** {user segment description}
- **Synthesis Confidence:** {HIGH|MEDIUM|LOW}

## L0: Executive Summary
- {Key finding 1: top functional job identified}
- {Key finding 2: dominant switch force pattern}
- {Key finding 3: highest-opportunity outcome}
- {Key finding 4: strategic recommendation}
- {Key finding 5: critical validation needed}

## L1: Technical Detail

### Functional Jobs
| Job Statement | Outcome Expectations | Priority | Source |
|---------------|---------------------|----------|--------|
| When [situation], I want to [motivation], so I can [outcome] | {3-5 outcomes} | {HIGH/MED/LOW} | {evidence source} |

### Social Jobs
| Job Statement | Outcome Expectations | Priority | Source |
|---------------|---------------------|----------|--------|
| When [situation], I want to [motivation], so I can [outcome] | {outcomes} | {priority} | {source} |

### Emotional Jobs
| Job Statement | Outcome Expectations | Priority | Source |
|---------------|---------------------|----------|--------|
| When [situation], I want to [motivation], so I can [outcome] | {outcomes} | {priority} | {source} |

### Switch Trigger Analysis (Four Forces)
| Force | Finding | Evidence |
|-------|---------|----------|
| **Push** (current pain) | {what drives users away from current solution} | {source} |
| **Pull** (new attraction) | {what attracts users to the new solution} | {source} |
| **Anxiety** (switching fear) | {what makes users hesitant to switch} | {source} |
| **Habit** (inertia) | {what keeps users attached to the current approach} | {source} |

**Force Balance Assessment:** {Push + Pull vs. Anxiety + Habit — does the balance favor switching?}

### Job Map
| Step | Universal Process | Domain-Specific Action | Importance | Satisfaction | Opportunity Score | Priority |
|------|------------------|----------------------|------------|-------------|-------------------|----------|
| 1 | Define | {action} | {importance} | {satisfaction} | {importance + max(importance - satisfaction, 0)} | {HIGH/MED/LOW} |
| 2 | Locate | {action} | {importance} | {satisfaction} | {score} | {priority} |
| 3 | Prepare | {action} | {importance} | {satisfaction} | {score} | {priority} |
| 4 | Confirm | {action} | {importance} | {satisfaction} | {score} | {priority} |
| 5 | Execute | {action} | {importance} | {satisfaction} | {score} | {priority} |
| 6 | Monitor | {action} | {importance} | {satisfaction} | {score} | {priority} |
| 7 | Modify | {action} | {importance} | {satisfaction} | {score} | {priority} |
| 8 | Conclude | {action} | {importance} | {satisfaction} | {score} | {priority} |

### Hiring Criteria
| Criterion | Measurement | Relative Weight |
|-----------|-------------|-----------------|
| {criterion name} | {how users evaluate this} | {HIGH/MED/LOW} |

## L2: Strategic Implications
- {Cross-product job patterns observed}
- {Unmet outcome opportunities ranked by opportunity score}
- {Organizational recommendations for validation and next steps}
- {Innovation trajectory: where demand-side gaps point}

## Synthesis Judgments Summary
1. {AI judgment call 1 — e.g., "Inferred push force from negative app store reviews; no direct user interview data"}
2. {AI judgment call 2 — e.g., "Classified job as functional rather than emotional based on outcome language patterns"}
3. {AI judgment call N — enumerate all significant AI inferences requiring human acknowledgment}

## Validation Required
- **Validation status:** PENDING
- **Required validation source:** {expert name, user data reference, or study citation}
- **Minimum threshold:** {per Synthesis Hypothesis Validation protocol}
```

**Worked Example (Onboarding Flow)**

The following shows populated rows from a JTBD analysis of a developer tool's onboarding flow (engagement UX-0042):

*Functional Job:*
| Job Statement | Outcome Expectations | Priority | Source |
|---------------|---------------------|----------|--------|
| When I am onboarding to a new tool, I want to understand its core value quickly so I can decide whether to invest time learning | Minimize the time it takes to identify the tool's primary use case | 8.2 | User interviews (3 participants) |

*Switch Force:*
| Force | Finding | Evidence |
|-------|---------|----------|
| **Push** (current pain) | Current onboarding takes 15+ minutes before first value | 3 interview transcripts |

*Job Map Steps:*
| Step | Universal Process | Domain-Specific Action | Importance | Satisfaction | Opportunity Score | Priority |
|------|------------------|----------------------|------------|-------------|-------------------|----------|
| 1 | Define | Determine what the tool does | 9.1 | 4.2 | 14.0 | HIGH |
| 2 | Locate | Find the feature that solves their problem | 7.8 | 6.1 | 9.5 | MEDIUM |

---

## Cross-Framework Integration

JTBD output serves as upstream research for multiple downstream sub-skills. The `ux-orchestrator` manages handoff data between sub-skills via the Jerry handoff protocol (`docs/schemas/handoff-v2.schema.json` — planned; not yet committed to repository).

### Downstream Handoff Contracts

| To Sub-Skill | Handoff Artifact | Key Fields | Use Case |
|-------------|-----------------|-----------|----------|
| `/ux-design-sprint` | Job statement + switch forces | Job statement text, push/pull forces, hiring criteria | Job statement feeds the Design Sprint challenge statement; switch forces inform the "How Might We" exercise in Day 1 |
| `/ux-kano-model` | Job-derived feature list | Feature names mapped to job steps | Each job step's outcome expectations generate candidate features for Kano classification |
| `/ux-lean-ux` | Job statements as hypothesis seeds | Job statement text, outcome expectations, hiring criteria | Jobs inform Lean UX hypothesis generation: "We believe [job outcome] will be achieved by [feature]" |

Source: `skills/user-experience/rules/ux-routing-rules.md` [Handoff Data Contracts] and `skills/user-experience/SKILL.md` [Cross-Sub-Skill Handoff Data].

### Upstream Dependencies

| From | Artifact Received | Usage |
|------|-------------------|-------|
| `ux-orchestrator` | Engagement context (product domain, user segments, UX capacity) | Scopes the JTBD analysis to the relevant domain and user segments |
| `/problem-solving` (ps-researcher) | Market research findings | Supplements JTBD competitive job analysis with broader market context (cross-skill integration) |

### Integration Workflow Examples

**Discovery to Sprint (Canonical Sequence):**
```
/ux-jtbd (job statements + switch forces)
    |
    v
/ux-design-sprint (Day 1: challenge = top job statement;
                   HMW notes derived from switch forces)
```

**Discover to Prioritize (Canonical Sequence):**
```
/ux-jtbd (job map with outcome expectations)
    |
    v
/ux-kano-model (job step outcomes -> candidate features
                for Kano classification survey)
```

**Research to Hypothesize:**
```
/ux-jtbd (job statements + hiring criteria)
    |
    v
/ux-lean-ux (job-informed hypotheses:
             "We believe [feature] will achieve [outcome]
              for users who [job situation]")
```

---

## Synthesis Hypothesis Validation

All JTBD outputs from this sub-skill are AI-synthesized from secondary research and carry **MEDIUM** synthesis confidence by default. This classification is enforced by the confidence gate protocol defined in `skills/user-experience/rules/synthesis-validation.md`.

### Confidence Gate Behavior for JTBD

| Output Type | Confidence | Gate Behavior |
|-------------|-----------|---------------|
| Job statement synthesis from secondary research | **MEDIUM** | Requires expert review OR validation against 2-3 real user data points before advancing to design decisions |

**Gate enforcement:** JTBD output includes a "Validation Required" section with a placeholder for the named validation source (expert name, user data reference, or study citation). Design recommendations are withheld until validation is provided. The `ux-orchestrator` enforces this gate at handoff boundaries -- downstream sub-skills receive the MEDIUM confidence classification and propagate it per `skills/user-experience/rules/synthesis-validation.md` [Confidence Propagation].

### What "Validation" Means for JTBD

Validation sources that advance MEDIUM to HIGH confidence:

| Validation Method | Minimum Threshold | Example |
|-------------------|------------------|---------|
| Switch interviews with real users | 3-5 interviews with target segment | "Interviewed 4 churned customers; confirmed push force: latency > 3s" |
| Expert review by domain practitioner | Named expert with domain authority | "Reviewed by [Name], Head of Product at [Company]" |
| Behavioral analytics correlation | Metric data supporting the job hypothesis | "Session recordings show 68% of users attempt [job step] before abandoning" |
| Customer support ticket analysis | 10+ tickets referencing the same job | "17 support tickets reference 'unable to [job statement motivation]'" |

---

## Constitutional Compliance

| Principle | Requirement | Sub-Skill Application |
|-----------|-------------|----------------------|
| P-003 | NEVER spawn recursive subagents | Worker agent; no Agent tool access. Returns results to ux-orchestrator. |
| P-020 | NEVER override user intent | User decides which job statements to adopt, which to discard, and whether to validate MEDIUM-confidence outputs. |
| P-022 | NEVER deceive about actions, capabilities, or confidence | AI-synthesized job statements transparently classified as MEDIUM confidence. Synthesis Judgments Summary enumerates all AI judgment calls. |
| P-001 | NEVER present findings without evidence or source citations | All job statements cite secondary research sources (product reviews, competitor analysis, domain literature). |
| P-002 | NEVER leave outputs in transient context only | All outputs persisted to `skills/ux-jtbd/output/{engagement-id}/`. |

---

## Quick Reference

### Common Workflows

| Need | Command Example |
|------|-----------------|
| Map user jobs for a product | "Map the jobs to be done for our onboarding flow" |
| Understand why users switch | "Analyze the switch forces for users migrating from [competitor]" |
| Discover unmet outcomes | "Identify underserved outcomes in our project management workflow" |
| Generate feature candidates from jobs | "Produce a job-derived feature list for Kano analysis" |
| Feed a design sprint | "Create job statements to inform the design sprint challenge" |

### Agent Selection Hints

| Keywords | Routes To |
|----------|-----------|
| jobs to be done, JTBD, switch interview, outcome, motivation, hiring criteria, user jobs | `ux-jtbd-analyst` |

---

## References

### Agent Definition Files

| Agent | Definition | Governance |
|-------|-----------|------------|
| ux-jtbd-analyst | `skills/ux-jtbd/agents/ux-jtbd-analyst.md` | `skills/ux-jtbd/agents/ux-jtbd-analyst.governance.yaml` |

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
| Handoff Schema | `docs/schemas/handoff-v2.schema.json` (planned — not yet committed to repository) |

### Project Traceability

| Item | Location |
|------|----------|
| Project plan | `projects/PROJ-022-user-experience-skill/PLAN.md` |
| Parent work item | EPIC-002 (Wave 1 deployment) |
| Orchestration plan | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |

### JTBD Framework References

| Framework | Source | Year | URL |
|-----------|--------|------|-----|
| Jobs-to-Be-Done Theory (primary) | Clayton Christensen et al. | 2016 | Christensen, C.M., Dillon, K., Hall, T., Duncan, D.S. (2016). *Competing Against Luck*. Harper Business. |
| Jobs-to-Be-Done Theory (foundational precursor) | Clayton Christensen | 2003 | Christensen, C.M. (2003). *The Innovator's Solution*. Harvard Business Review Press. |
| Outcome-Driven Innovation | Anthony Ulwick | 2005, 2016 | Ulwick, A.W. (2016). *Jobs to Be Done: Theory to Practice*. IDEA BITE PRESS. https://jobs-to-be-done.com/ |
| Switch Interview Framework (primary) | Bob Moesta | 2020 | Moesta, B. (2020). *Demand-Side Sales 101*. Lioncrest Publishing. |
| Switch Interview Framework (supplementary) | Bob Moesta, Chris Spiek, Alan Klement | 2014, 2016 | Moesta, B. and Spiek, C. (2014). *The Jobs-to-Be-Done Handbook: Practical Techniques for Improving Your Application of Jobs-to-Be-Done*. Re-Wired Group. Practitioner's guide to switch interview techniques. See also: Klement, A. (2016). *When Coffee and Kale Compete*. |

---

<!-- VERSION: 1.0.0 | DATE: 2026-03-04 | SOURCE: PROJ-022-user-experience-skill/PLAN.md | PARENT: /user-experience skill -->
*Sub-Skill Version: 1.0.0*
*Parent Skill: `/user-experience` (`skills/user-experience/SKILL.md`)*
*Constitutional Compliance: Jerry Constitution v1.0 (P-003, P-020, P-022, P-001, P-002)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Project: PROJ-022 User Experience Skill | Wave 1*
*Created: 2026-03-04*
*Agent: ux-jtbd-analyst*
