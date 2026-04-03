---
name: pm-pmm
description: "Product management and product marketing decision framework. Invoke when users need product strategy (PRDs, vision, roadmaps), customer insight (personas, journey maps, VOC), business analysis (business cases, market sizing, pricing), competitive intelligence (battle cards, win/loss, competitive analysis), or go-to-market planning (GTM plans, positioning, MRDs, buyer personas). Uses 18 validated industry frameworks organized around Cagan's Value Risk and Business Viability Risk domains. Supports discovery mode (hypothesis-driven) and delivery mode (stakeholder-ready). Trigger keywords - PRD, product requirements, roadmap, prioritize, RICE, persona, journey map, VOC, business case, market sizing, TAM, competitive analysis, battle card, GTM, go-to-market, positioning, messaging, MRD."
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
activation-keywords:
  - "PRD"
  - "product requirements"
  - "product strategy"
  - "product vision"
  - "roadmap"
  - "prioritize"
  - "RICE"
  - "Kano"
  - "persona"
  - "customer interview"
  - "journey map"
  - "VOC"
  - "voice of customer"
  - "customer discovery"
  - "pain points"
  - "churn analysis"
  - "NPS"
  - "business case"
  - "financial model"
  - "market sizing"
  - "TAM"
  - "SAM"
  - "SOM"
  - "pricing model"
  - "unit economics"
  - "LTV"
  - "CAC"
  - "competitive analysis"
  - "battle card"
  - "win/loss"
  - "Porter's"
  - "SWOT"
  - "competitive landscape"
  - "GTM"
  - "go-to-market"
  - "positioning"
  - "messaging"
  - "MRD"
  - "launch plan"
  - "sales enablement"
  - "buyer persona"
  - "product marketing"
  - "PLG"
  - "product-led growth"
  - "JTBD"
  - "north star metric"
  - "opportunity solution tree"
  - "product kata"
  - "break-even"
  - "NPV"
  - "IRR"
  - "revenue model"
  - "feasibility"
  - "Van Westendorp"
  - "Lean Canvas"
  - "Rule of 40"
  - "Magic Number"
  - "payback period"
  - "Blue Ocean"
  - "value curve"
  - "Crossing the Chasm"
  - "competitive threat"
  - "market intelligence"
---

# PM/PMM Skill

> **Version:** 1.0.0
> **Framework:** Jerry PM/PMM Decision Framework
> **Constitutional Compliance:** Jerry Constitution v1.0
> **SSOT Reference:** `.context/rules/quality-enforcement.md`
> **Architecture Reference:** PROJ-018 Issue #123

## Document Audience (Triple-Lens)

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | New users, stakeholders | [Purpose](#purpose), [When to Use](#when-to-use-this-skill), [Quick Reference](#quick-reference) |
| **L1 (Engineer)** | Developers invoking agents | [Available Agents](#available-agents), [Invoking an Agent](#invoking-an-agent), [Discovery vs Delivery Mode](#discovery-vs-delivery-mode), [Framework Catalog](#framework-catalog) |
| **L2 (Architect)** | Workflow designers | [P-003 Compliance](#p-003-compliance), [Cross-Agent Data Flow](#cross-agent-data-flow), [Integration Points](#integration-points-with-other-skills), [Artifact Ownership Matrix](#artifact-ownership-matrix) |

---

## Purpose

The PM/PMM skill provides a **decision-focused product management and product marketing capability** for the Jerry Framework. It helps PMs and PMMs make better product decisions by ensuring every decision is grounded in evidence, structured by proven frameworks, and documented as a living artifact.

### What It Does

- **Product Strategy:** Creates PRDs, product vision documents, roadmaps, and use case specifications grounded in JTBD, RICE, Kano, Playing to Win, and Opportunity Solution Tree frameworks
- **Customer Insight:** Builds JTBD-oriented personas, customer journey maps with Moments of Truth, and VOC research reports synthesized from interview data
- **Business Analysis:** Produces business cases, TAM/SAM/SOM market sizing, and pricing strategy analysis using Van Westendorp, Lean Canvas, and SaaS financial metrics
- **Competitive Intelligence:** Delivers competitive analysis with Porter's Five Forces, Blue Ocean value curves, battle cards with talk tracks, and win/loss pattern analysis
- **Go-to-Market:** Creates GTM plans with Dunford positioning, MRDs, and buying-committee buyer personas

### Core Design Principles

1. **Cagan's Two Risks:** Organized around Value Risk ("Will they buy/use it?") and Business Viability Risk ("Does it work for the business?"). Usability Risk and Feasibility Risk are out of scope.
2. **Discovery Before Delivery:** Every agent defaults to discovery mode. Validates assumptions cheaply before committing to polished artifacts.
3. **18 Validated Frameworks:** Not name-drops -- each framework is operationalized with methodology steps that produce canonical output structures.
4. **Evidence, Not Intuition:** All claims require evidence citations or explicit hypothesis marking with confidence levels.

---

## When to Use This Skill

**Activate when:**

- Building a new product or feature and need to define what to build and why
- Creating or updating product requirements (PRDs) with prioritization frameworks
- Understanding customers through personas, journey maps, or VOC research
- Assessing business viability through business cases, market sizing, or pricing analysis
- Analyzing the competitive landscape or creating battle cards
- Planning go-to-market strategy, positioning, messaging, or launch execution
- Needing structured product/market frameworks rather than ad-hoc analysis

**Do NOT use when:**

- Writing code, designing architecture, or making technical implementation decisions (use `/architecture` or `/eng-team`)
- Running adversarial quality reviews on deliverables (use `/adversary`)
- Performing root cause analysis on bugs or failures (use `/problem-solving`)
- Creating UX wireframes or design specifications (out of scope -- Usability Risk)
- Managing work items or tracking project status (use `/worktracker`)
- Parsing transcripts or meeting notes (use `/transcript`)
- Deploying, testing, or managing CI/CD (use `/eng-team`)

### Negative Keywords (Prevent False Routing)

These keywords in a request should suppress `/pm-pmm` routing:

| Keyword | Routes To Instead |
|---------|-------------------|
| code review | `/problem-solving` or `/eng-team` |
| architecture, ADR | `/architecture` |
| engineering, implementation | `/eng-team` |
| deployment, CI/CD | `/eng-team` |
| testing, test coverage | `/eng-team` |
| infrastructure pricing, cloud pricing | `/eng-team` (not product pricing) |
| adversarial, tournament | `/adversary` |
| transcript, VTT, SRT | `/transcript` |
| penetration test, exploit | `/red-team` |

---

## Available Agents

| Agent | Decision Question | Risk Domain | Model | Status |
|-------|------------------|-------------|-------|--------|
| `pm-product-strategist` | "What should we build, and why?" | Value + Viability (strategy) | opus | **Tier 1 -- Active** |
| `pm-customer-insight` | "Who are our customers, and what do they need?" | Value Risk | opus | **Tier 1 -- Active** |
| `pm-market-strategist` | "How do we bring this to market?" | Viability Risk (GTM) | opus | **Tier 1 -- Active** |
| `pm-business-analyst` | "Is this worth investing in?" | Viability Risk (financial) | sonnet | **Tier 2 -- Active** |
| `pm-competitive-analyst` | "Who are we up against?" | Viability Risk (market) | sonnet | **Tier 2 -- Active** |

### Agent-to-Artifact Ownership

| Agent | Primary Artifacts | Count |
|-------|-------------------|-------|
| pm-product-strategist | PRD, Product Vision, Roadmap, Use Cases | 4 |
| pm-customer-insight | User Personas, Customer Journey Maps, VOC Research Reports | 3 |
| pm-market-strategist | GTM Plan, MRD, Buyer Personas | 3 |
| pm-business-analyst | Business Case, Market Sizing (TAM/SAM/SOM) | 2 |
| pm-competitive-analyst | Competitive Analysis, Battle Cards, Win/Loss Analysis | 3 |
| **Total** | | **15** |

### Agent Selection Hints

| User Says | Route To | Rationale |
|-----------|----------|-----------|
| "Write a PRD" / "product requirements" / "roadmap" / "prioritize features" | pm-product-strategist | Owns all product requirements and prioritization artifacts |
| "Create personas" / "journey map" / "customer interviews" / "VOC" / "pain points" | pm-customer-insight | Owns user personas, journey maps, VOC research |
| "GTM plan" / "positioning" / "messaging" / "buyer persona" / "launch plan" | pm-market-strategist | Owns GTM, MRD, buyer personas |
| "Business case" / "TAM" / "market sizing" / "pricing model" / "unit economics" | pm-business-analyst | Owns business cases, market sizing, pricing analysis |
| "Competitive analysis" / "battle card" / "win/loss" / "Porter's" / "SWOT" | pm-competitive-analyst | Owns competitive analysis, battle cards, win/loss reports |

---

## P-003 Compliance

All PM/PMM agents are **workers**, NOT orchestrators. The MAIN CONTEXT (Claude session) orchestrates all workflows.

```
P-003 AGENT HIERARCHY:
======================

  +-------------------+
  | MAIN CONTEXT      |  <-- Orchestrator (Claude session)
  | (orchestrator)    |
  +-------------------+
     |        |        |
     v        v        v
  +------+ +------+ +------+
  | pm-  | | pm-  | | pm-  |   <-- Tier 1 Workers
  |prod- | |cust- | |mkt-  |
  |strat | |insght| |strat |
  +------+ +------+ +------+

  +------+ +------+
  | pm-  | | pm-  |   <-- Tier 2 Workers (Active)
  |biz-  | |comp- |
  |anlst | |anlst |
  +------+ +------+

  - Agents CANNOT invoke other agents.
  - Agents CANNOT spawn subagents.
  - Agents do NOT have the Task tool.
  - Only MAIN CONTEXT orchestrates the sequence.
  - All cross-agent data flows through file artifacts.
```

---

## Invoking an Agent

### Option 1: Natural Language Request

Simply describe what you need:

```
"Create a PRD for the self-service onboarding feature"
"Build personas for our platform engineering customers"
"Create a GTM plan with positioning for our developer platform"
"Help me prioritize these features using RICE"
"Map the customer journey for enterprise onboarding"
"Write an MRD for the APAC market expansion"
```

The orchestrator selects the appropriate agent based on keywords and context.

### Option 2: Explicit Agent Request

Request a specific agent:

```
"Use pm-product-strategist to create a product vision using Playing to Win"
"Have pm-customer-insight build a persona for DevOps engineers"
"I need pm-market-strategist to create Dunford positioning for our launch"
```

### Option 3: Multi-Agent Workflow

Request work that spans multiple agents (orchestrated by main context):

```
"Research our customers, then create a PRD grounded in the persona data"
  -> pm-customer-insight (personas) -> pm-product-strategist (PRD with persona cross-refs)

"Position our product and then create a GTM launch plan"
  -> pm-market-strategist (positioning hypothesis) -> pm-market-strategist (GTM plan)

"Analyze the competitive landscape and build a business case for our platform"
  -> pm-competitive-analyst (competitive analysis) -> pm-business-analyst (business case with competitive context)

"Size the market, analyze competitors, and create pricing recommendations"
  -> pm-business-analyst (TAM/SAM/SOM) -> pm-competitive-analyst (competitive pricing) -> pm-business-analyst (pricing strategy)
```

---

## Discovery vs Delivery Mode

Every agent operates in two modes. **Discovery is always the default.**

| Dimension | Discovery Mode | Delivery Mode |
|-----------|---------------|---------------|
| **Purpose** | Explore, hypothesize, validate assumptions | Produce stakeholder-ready artifacts |
| **Output length** | 1-2 pages | Full framework depth (5-20 pages) |
| **Framework depth** | Lightweight application, key dimensions only | Complete framework execution with all sections |
| **Evidence standard** | Hypotheses with stated confidence | Data-validated claims with citations |
| **Audience** | PM/PMM internal working document | Cross-functional stakeholders, executives |
| **Status** | `discovery` | `delivery` or `final` |
| **Default?** | Yes -- always start here | Explicit user request required |

### Mode Selection

```
IF user explicitly says "delivery" or "full" or "stakeholder-ready":
    mode = delivery
ELIF prior discovery artifact exists for this topic:
    mode = delivery (suggest upgrade, confirm with user per P-020)
ELSE:
    mode = discovery (default)
```

### Why Discovery First?

Discovery before delivery prevents the most expensive PM failure mode: building a polished artifact for a product nobody wants. Discovery validates assumptions cheaply (1-2 pages, hypothesis-driven). Delivery commits resources to documentation (5-20 pages, evidence-validated).

---

## Framework Catalog

18 primary frameworks mapped to agents. Each framework is operationalized with methodology steps in the agent's `<methodology>` section.

### pm-product-strategist Frameworks (6)

| # | Framework | Operationalization |
|---|-----------|-------------------|
| 1 | Opportunity Solution Trees (Torres) | Tree structure: outcome root, opportunity branches, solution leaves with evidence links and confidence |
| 2 | JTBD (Christensen/Ulwick) -- secondary | Decomposes needs into functional/emotional/social jobs; Opportunity Scoring |
| 3 | RICE Prioritization (Intercom) | Scores: Reach, Impact, Confidence, Effort; dimension-level breakdown table |
| 4 | Kano Model | Feature classification: Must-Have, Performance, Delighter; questionnaire pairs |
| 5 | Product Kata (Perri) | Cycle: Direction -> Current State -> Next Target Condition -> First Step |
| 6 | Playing to Win (Lafley & Martin) | Strategy cascade: Aspiration, Where to Play, How to Win, Capabilities, Systems |

**Supporting methods:** ICE/MoSCoW/WSJF (alternative prioritization), North Star Metric (vision anchoring), Story Mapping (use case organization)

### pm-customer-insight Frameworks (4)

| # | Framework | Operationalization |
|---|-----------|-------------------|
| 7 | JTBD (Christensen/Ulwick) -- primary | Functional/emotional/social jobs with importance/satisfaction scoring |
| 8 | Customer Development (Blank) | Four phases: Discovery, Validation, Creation, Building with evidence |
| 9 | Moments of Truth (P&G/Google) | Maps ZMOT, FMOT, SMOT, UMOT at each journey stage |
| 10 | Service Blueprint (Shostack) | Five-lane blueprint: physical evidence, customer/frontstage/backstage/support |

**Supporting methods:** NPS/CSAT/CES measurement, Opportunity Scoring (Ulwick/ODI)

### pm-market-strategist Frameworks (3)

| # | Framework | Operationalization |
|---|-----------|-------------------|
| 11 | Positioning Framework (Dunford) | 5-step: competitive alternatives, attributes, value, segment, category |
| 12 | PMF Survey (Ellis) | "Very disappointed" test design, 40% threshold, segment analysis |
| 13 | Lauchengco PMM Model | 4-role mapping: Ambassador, Strategist, Storyteller, Evangelist |

**Supporting methods:** Crossing the Chasm (adoption lifecycle, bowling alley), StoryBrand (messaging narrative)

### pm-business-analyst Frameworks (3)

| # | Framework | Operationalization |
|---|-----------|-------------------|
| 14 | Van Westendorp PSM | Four price-point questions, price sensitivity curves |
| 15 | Lean Canvas / BMC | 9-block canvas: Problem, Solution, Metrics, UVP, Channels, etc. |
| 16 | SaaS Financial Metrics | Rule of 40, LTV:CAC, NRR, Magic Number with BVP benchmarks |

**Supporting methods:** Good-Better-Best pricing, Conjoint analysis, NPV/IRR/break-even

### pm-competitive-analyst Frameworks (3)

| # | Framework | Operationalization |
|---|-----------|-------------------|
| 17 | Porter's Five Forces | All 5 forces assessed with high/medium/low rating and evidence |
| 18 | Blue Ocean / Value Curve | Value curve with eliminate-reduce-raise-create actions |
| -- | Crossing the Chasm (Moore) -- shared | Technology Adoption Lifecycle position, bowling alley targeting |

**Supporting methods:** SWOT Analysis, Gartner MQ / Forrester Wave, Category Design

---

## Artifact Ownership Matrix

Every artifact has exactly one primary owner. Contributing agents provide inputs but do not produce the artifact.

| # | Artifact | Primary Agent | Contributors | Sensitivity Default |
|---|----------|--------------|-------------|-------------------|
| 1 | PRD | pm-product-strategist | pm-customer-insight | internal |
| 2 | Product Vision | pm-product-strategist | pm-business-analyst | internal |
| 3 | Roadmap | pm-product-strategist | pm-business-analyst, pm-customer-insight | internal |
| 4 | Use Cases | pm-product-strategist | pm-customer-insight | internal |
| 5 | User Personas | pm-customer-insight | -- | confidential |
| 6 | Journey Maps | pm-customer-insight | -- | confidential |
| 7 | VOC Reports | pm-customer-insight | -- | confidential |
| 8 | Business Case | pm-business-analyst | pm-product-strategist, pm-competitive-analyst | restricted |
| 9 | Market Sizing | pm-business-analyst | pm-competitive-analyst | restricted |
| 10 | Competitive Analysis | pm-competitive-analyst | pm-market-strategist | restricted |
| 11 | Battle Cards | pm-competitive-analyst | pm-market-strategist | restricted |
| 12 | Win/Loss Analysis | pm-competitive-analyst | pm-market-strategist | restricted |
| 13 | GTM Plan | pm-market-strategist | pm-competitive-analyst, pm-customer-insight | internal |
| 14 | MRD | pm-market-strategist | pm-competitive-analyst, pm-product-strategist | internal |
| 15 | Buyer Personas | pm-market-strategist | pm-competitive-analyst | internal |

---

## Cross-Agent Data Flow

All agent interactions are mediated by the Jerry main context (orchestrator). No agent invokes another agent directly. Data flows through file artifacts.

| From | To | Data | Mechanism |
|------|-----|------|-----------|
| pm-customer-insight | pm-product-strategist | Persona file paths, VOC themes, JTBD statements | File paths in handoff artifacts array |
| pm-customer-insight | pm-market-strategist | User persona references for buyer-user alignment | cross_refs frontmatter |
| pm-competitive-analyst | pm-market-strategist | Competitive positioning, battle card references | File paths in handoff |
| pm-competitive-analyst | pm-business-analyst | Competitive pricing data, market share estimates | Orchestrator passes file paths in handoff |
| pm-business-analyst | pm-product-strategist | Market sizing, feasibility verdict | cross_refs frontmatter |
| pm-business-analyst | pm-market-strategist | Pricing model, packaging recommendations | Orchestrator passes file paths in handoff |
| pm-product-strategist | pm-market-strategist | Product strategy, feature differentiation | cross_refs frontmatter |
| pm-product-strategist | pm-business-analyst | Product scope, investment estimation inputs | Orchestrator passes file paths in handoff |

### Conflict Resolution

When agents produce conflicting recommendations:
1. Orchestrator surfaces both outputs with explicit conflict statement
2. Presents the evidence from each agent
3. Asks the user to decide (P-020: User Decides)
4. Does NOT silently pick a winner

---

## Integration Points with Other Skills

| # | Skill | Integration | Details |
|---|-------|-------------|---------|
| 1 | `/worktracker` | Bidirectional | Artifact IDs (PM-PS-001) link to worktracker entities (FEAT-042) via cross_refs. Roadmap items map to Epics/Features/Stories. |
| 2 | `/adversary` | Unidirectional | PM/PMM artifacts at C2+ submitted for quality review using 6-dimension weighted composite. Minimum 3-iteration creator-critic-revision cycle per H-14. |
| 3 | `/problem-solving` | Unidirectional | ps-researcher feeds pm-product-strategist and pm-competitive-analyst with external research. ps-analyst supports pm-business-analyst with root cause analysis. |
| 4 | `/architecture` | Bidirectional | ADR decisions inform PRD technical constraints. Product requirements referenced in ADR context. |
| 5 | `/nasa-se` | Unidirectional | PRD requirements flow to SE verification. Requirements IDs appear in V&V traceability matrix. |
| 6 | `/use-case` | Unidirectional | pm-product-strategist use cases feed to `/use-case` for slicing and implementation planning. |

---

## Quick Reference

### Common Workflows

| Need | Agent | Example Prompt |
|------|-------|---------------|
| Write a PRD | pm-product-strategist | "Create a PRD for the self-service onboarding feature using RICE prioritization" |
| Create product vision | pm-product-strategist | "Build a product vision using Playing to Win for our developer platform" |
| Build personas | pm-customer-insight | "Create JTBD-oriented personas for our platform engineering customers" |
| Map customer journey | pm-customer-insight | "Map the enterprise onboarding journey with Moments of Truth" |
| Synthesize VOC | pm-customer-insight | "Analyze these 12 interview transcripts and extract VOC themes" |
| Position product | pm-market-strategist | "Create Dunford positioning for our developer platform launch" |
| Plan GTM | pm-market-strategist | "Design a go-to-market plan for APAC expansion" |
| Create buyer personas | pm-market-strategist | "Build buyer personas for the enterprise buying committee" |
| Prioritize backlog | pm-product-strategist | "Prioritize these 8 features using RICE scoring" |
| Assess PMF | pm-market-strategist | "Design a PMF survey using the Ellis 40% test" |
| Build business case | pm-business-analyst | "Create a business case for the self-service platform with NPV analysis" |
| Size market | pm-business-analyst | "Calculate TAM/SAM/SOM for the developer platform market" |
| Analyze pricing | pm-business-analyst | "Run Van Westendorp pricing analysis for our enterprise tier" |
| Analyze competitors | pm-competitive-analyst | "Analyze the competitive landscape using Porter's Five Forces" |
| Create battle cards | pm-competitive-analyst | "Build battle cards for our top 3 competitors with talk tracks" |
| Analyze win/loss | pm-competitive-analyst | "Analyze Q1 win/loss patterns from our sales data" |

### Routing Keyword Quick-Map

| Keywords | Agent |
|----------|-------|
| PRD, product requirements, roadmap, prioritize, RICE, Kano, product vision, product strategy, "what to build", opportunity, north star, feature prioritization | pm-product-strategist |
| persona, customer interview, journey map, VOC, voice of customer, churn, NPS, CSAT, CES, customer discovery, pain points, user needs | pm-customer-insight |
| GTM, go-to-market, positioning, messaging, MRD, launch plan, sales enablement, buyer persona, product marketing, PLG, category | pm-market-strategist |
| business case, financial model, market sizing, TAM, SAM, SOM, pricing, unit economics, LTV, CAC, NRR, NPV, break-even, feasibility, revenue model, Van Westendorp, Lean Canvas, Rule of 40, Magic Number, payback period | pm-business-analyst |
| competitive analysis, battle card, win/loss, competitor, Porter's, SWOT, competitive landscape, differentiation, market intelligence, competitive threat, Blue Ocean, value curve, Crossing the Chasm | pm-competitive-analyst |

> **Persona routing disambiguation:** Standalone "persona" routes to pm-customer-insight (user personas). "buyer persona" routes to pm-market-strategist (buying committee personas). This distinction aligns with the user persona vs. buyer persona ownership boundary.

---

## Trigger Map Entry

For registration in `mandatory-skill-usage.md`:

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
|---|---|---|---|---|
| product strategy, PRD, product requirements, roadmap, prioritize, RICE, customer insight, persona, journey map, VOC, voice of customer, business case, market sizing, TAM, pricing, unit economics, competitive analysis, battle card, win/loss, GTM, go-to-market, positioning, messaging, MRD, launch plan, product marketing, buyer persona, JTBD, north star, Kano, product vision | code review, architecture, engineering, implementation, deployment, testing, CI/CD, infrastructure pricing, cloud pricing, adversarial, transcript, penetration test, exploit, strategy (standalone) | 9 | "product strategy" OR "product requirements" OR "market sizing" OR "go-to-market" OR "competitive analysis" OR "business case" OR "buyer persona" (phrase match) | `/pm-pmm` |

> **Priority 9 rationale:** Below /ast (8) and /adversary (7), ensuring /pm-pmm does not capture general analysis or AST requests. PM/PMM domain terms provide sufficient specificity via compound triggers. Standalone "strategy" replaced with compound "product strategy" to avoid collision with /problem-solving.

---

## Dependencies / Prerequisites

### Templates (Phase 4)

15 artifact templates in `skills/pm-pmm/templates/` will be created during Phase 4 (naming: `{NN}-{artifact-slug}.template.md`). Templates cover all 15 artifact types from the Artifact Ownership Matrix. Each template includes both discovery and delivery mode sections.

### SSOT Files

- `.context/rules/quality-enforcement.md` -- Quality gate thresholds, criticality levels, adversarial strategies
- `.context/rules/agent-development-standards.md` -- H-34 dual-file architecture, tool tiers
- `docs/schemas/agent-governance-v1.schema.json` -- Governance YAML validation schema

---

## Constitutional Compliance

All agents adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement |
|-----------|-------------|
| P-001: Truth and Accuracy | Framework application produces canonical structures. Claims based on evidence. |
| P-002: File Persistence | All outputs persisted to `docs/pm-pmm/` filesystem. |
| P-003: No Recursive Subagents | All agents are workers. No agent has the Task tool. Main context orchestrates. |
| P-011: Evidence-Based | All claims tied to data, citations, or stated as hypotheses with confidence levels. |
| P-020: User Authority | Conflicting recommendations surface both sides. User decides. Never override. |
| P-022: No Deception | Discovery artifacts labeled as hypotheses. Confidence levels reported honestly. |

---

## References

| Source | Content |
|--------|---------|
| GitHub Issue #123 | Full PM/PMM skill specification |
| `eng/phase-1-research/architecture.md` | 5-agent architecture, artifact ownership, data flows |
| `eng/phase-1-research/frontmatter-schema.md` | Frontmatter fields, governance YAML structures |
| `.context/rules/quality-enforcement.md` | Quality gate SSOT |
| `.context/rules/agent-development-standards.md` | H-34 dual-file architecture |
| `docs/schemas/agent-governance-v1.schema.json` | Governance YAML schema |
| `docs/governance/JERRY_CONSTITUTION.md` | Constitutional principles |

---

## Context Budget Note

> This SKILL.md exceeds the typical ~500-token Tier 1 budget due to the skill's scope (5 agents, 18 frameworks, 15 artifacts). The triple-lens navigation table enables selective section loading. Framework catalog and cross-agent data flow sections are reference material that agents load selectively via Tier 2/3.

---

*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Architecture: PROJ-018 PM/PMM Skill, Issue #123*
*Created: 2026-03-01*
