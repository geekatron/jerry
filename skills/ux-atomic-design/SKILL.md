---
name: ux-atomic-design
description: "Atomic Design component taxonomy sub-skill for the /user-experience parent skill. Implements Brad Frost's 5-level component hierarchy (Atoms, Molecules, Organisms, Templates, Pages) for design system architecture. Produces component inventories, design token audits, composition rules, and Storybook coverage reports. Invoke when teams need component taxonomy construction, design system architecture, Storybook integration, design token consistency analysis, or component reuse auditing. Invoked by ux-orchestrator during Wave 3 lifecycle-stage routing or when user intent is \"Building component system\" during the \"During design\" stage. Triggers: atomic design, component taxonomy, design tokens, Storybook, atoms molecules organisms, design system, component inventory, component library."
version: "1.2.0"
agents:
  - ux-atomic-architect
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
activation-keywords:
  - "atomic design"
  - "component taxonomy"
  - "design tokens"
  - "Storybook"
  - "atoms molecules organisms"
  - "design system architecture"
  - "component inventory"
  - "component library"
  - "design system"
---

<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/user-experience/SKILL.md | PARENT: /user-experience skill | REVISION: iter3 quality gate fixes — evidence quality (Phase 5 Activity 3 maturity thresholds labeled as heuristics with drift-ratio-based token governance criteria), actionability (Phase 5 Activity 3 coverage metric specified as component coverage from Phase 4 Activity 1; Phase 1 Activity 2 wave entry verification evidence source added) -->

# Atomic Design Sub-Skill

> **Version:** 1.2.0
> **Framework:** Jerry User-Experience -- Atomic Design
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Parent Skill:** `/user-experience` (`skills/user-experience/SKILL.md`)
> **Wave:** 3 (Design System)
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
| [Methodology](#methodology) | Brad Frost's 5-level hierarchy, design tokens, composition rules, Storybook coverage model, 5-phase execution procedure |
| [MCP Dependencies](#mcp-dependencies) | Storybook REQ with manual fallback; Figma ENH; Zeroheight ENH; Context7 for component library docs |
| [Output Specification](#output-specification) | Output location, L0/L1/L2 structure, required sections |
| [Routing](#routing) | Keywords and lifecycle-stage routing integration |
| [Cross-Framework Integration](#cross-framework-integration) | Handoff from heuristic evaluation and to inclusive design |
| [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence) | Confidence classifications for Atomic Design outputs |
| [Constitutional Compliance](#constitutional-compliance) | Governing principles and AI-augmented analysis limitations |
| [Registration](#registration) | H-26 parent-routed registration model and AGENTS.md confirmation |
| [Deployment Status](#deployment-status) | Wave 3 stub agent status and implementation timeline |
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

The Atomic Design sub-skill provides structured component taxonomy architecture using Brad Frost's Atomic Design methodology (2016). It targets tiny teams (1-5 people) who need to move beyond ad-hoc component creation toward a systematic, hierarchical design system that promotes consistency, reuse, and scalability across their product interface.

This sub-skill is part of Wave 3 (Design System), meaning it requires Wave 2 completion (launched product with analytics OR 1 completed Lean UX hypothesis cycle) before deployment. It bridges the gap between iterative experimentation (Wave 2) and accessibility evaluation (Wave 3: Inclusive Design) by providing a structured component inventory that the inclusive design evaluator can audit.

### Key Capabilities

- **5-Level Component Taxonomy** -- Classifies interface elements into Atoms, Molecules, Organisms, Templates, and Pages following Brad Frost's hierarchy, establishing a shared vocabulary for design and development
- **Design Token Auditing** -- Inventories and validates design tokens (colors, typography, spacing, breakpoints) for consistency across the component hierarchy, identifying token drift and redundancy
- **Component Inventory Construction** -- Produces comprehensive inventories of existing components with classification level, Storybook coverage status, reuse frequency, and variant count
- **Composition Rule Documentation** -- Documents valid composition patterns (which atoms compose which molecules, which molecules compose which organisms) to prevent inconsistent component assembly
- **Storybook Integration Assessment** -- Evaluates component library documentation coverage in Storybook, identifying components without stories, missing states, and undocumented variants
- **Component Reuse Analysis** -- Identifies duplicate or near-duplicate components that should be consolidated, quantifying reuse opportunities and estimating design debt reduction

> **Source:** Key capabilities derived from parent SKILL.md [skills/user-experience/SKILL.md Section "Key Capabilities"] ("Atomic Design -- Brad Frost's 5-level component taxonomy (Wave 3)") and [skills/user-experience/SKILL.md Section "Available Agents"] ("Atomic design component taxonomy architect").

---

## When to Use This Sub-Skill

Activate when:

- Building or refactoring a component library and need a systematic classification framework
- Auditing an existing design system for component hierarchy completeness and consistency
- Inventorying components with their Storybook coverage status for gap identification
- Analyzing design token consistency across a component hierarchy (colors, typography, spacing)
- Documenting composition rules between atoms, molecules, and organisms
- Identifying duplicate or near-duplicate components for consolidation
- Preparing a component inventory for downstream accessibility evaluation
- Transitioning from ad-hoc component creation to a structured design system during the "During design" lifecycle stage

Do NOT use for:

- Evaluating an existing interface against usability heuristics -- use `/ux-heuristic-eval` (Nielsen's 10) instead. Atomic Design classifies components; heuristic evaluation assesses usability quality.
- Accessibility compliance auditing -- use `/ux-inclusive-design` (WCAG 2.2) instead. Atomic Design produces the component inventory that inclusive design evaluates for accessibility. Use this sub-skill first, then pass the inventory to `/ux-inclusive-design`.
- Testing hypotheses about design changes -- use `/ux-lean-ux` (Lean UX) instead. Atomic Design structures components; Lean UX tests whether design changes improve outcomes.
- Measuring quantitative UX health metrics -- use `/ux-heart-metrics` (Google GSM) instead. Atomic Design focuses on component architecture, not metric measurement.
- Understanding user motivations and jobs -- use `/ux-jtbd` (Jobs-to-Be-Done) instead. Atomic Design operates at the component level, not the user motivation level.
- Diagnosing why users fail to take a specific action -- use `/ux-behavior-design` (Fogg B=MAP) instead. Atomic Design focuses on structural component classification, not behavioral diagnosis.
- Running a full rapid prototyping sprint -- use `/ux-design-sprint` (Design Sprint 2.0) instead.
- Security-focused interface review -- use `/eng-team` instead.
- General research without UX component focus -- use `/problem-solving` instead.

> **Source:** Routing logic derived from [skills/user-experience/SKILL.md Section "Lifecycle-Stage Routing"] ("During design: Building component system -> /ux-atomic-design") and [skills/user-experience/rules/ux-routing-rules.md Section "Stage Routing Table"], [skills/user-experience/rules/ux-routing-rules.md Section "Common Intent Resolution"].

---

## Available Agents

| Agent | Role | Tier | Mode | Model | Output Location |
|-------|------|------|------|-------|-----------------|
| `ux-atomic-architect` | Atomic design component taxonomy architect | T4 | Systematic | Sonnet | `skills/ux-atomic-design/output/{engagement-id}/ux-atomic-architect-{topic-slug}.md` |

**STUB:** The agent definition file (`skills/ux-atomic-design/agents/ux-atomic-architect.md`) is pending Wave 3 Phase 2 implementation as part of PROJ-022 EPIC-003. The SKILL.md specifies the methodology and output contract that the agent will implement.

**Tool tier:** T4 (External) = Read, Write, Edit, Glob, Grep + WebSearch, WebFetch + Context7 MCP. The T4 tier enables access to external component library documentation (Material UI, Radix, Shadcn/ui) via Context7 and web search for Storybook configuration patterns. Bash is intentionally excluded; T4 tier does not require shell access for MCP operations. See `.context/rules/agent-development-standards.md` [Tool Security Tiers] for full tier definitions.

The agent produces output at three levels per AD-M-004:
- **L0 (Executive Summary):** Top component reuse opportunities; design token consistency score; Storybook coverage percentage; key findings for stakeholders and cross-framework synthesis input.
- **L1 (Technical Detail):** Full 5-level component inventory with classification, composition rules, design token audit, Storybook coverage report, and variant documentation.
- **L2 (Strategic Implications):** Design system maturity assessment, component consolidation roadmap, design debt quantification, and design system evolution recommendations.

> **Source:** Agent specification from [skills/user-experience/SKILL.md Section "Available Agents"] and ORCHESTRATION.yaml pipeline-wave3 phase-1.

---

## P-003 Compliance

The `/ux-atomic-design` sub-skill contains a single **worker** agent. It is invoked by the `ux-orchestrator` (T5) via the Agent tool. The agent does NOT have Agent tool access and MUST NOT spawn sub-agents.

```
MAIN CONTEXT (user request)
    |
    v
ux-orchestrator (T5, Opus, Integrative) -- parent orchestrator
    |
    +-- ux-atomic-architect (T4, Systematic, Sonnet) -- THIS sub-skill's worker
    +-- [other sub-skill workers...]
```

**Enforcement:**
- `disallowedTools: [Agent]` declared in `skills/ux-atomic-design/agents/ux-atomic-architect.md` frontmatter
- P-003 prohibition in `skills/ux-atomic-design/agents/ux-atomic-architect.governance.yaml` `capabilities.forbidden_actions`
- CI gate validates no sub-skill agent has Agent access (documented in `skills/user-experience/rules/ci-checks.md`)

> **Source:** P-003 hierarchy from parent SKILL.md [P-003 Compliance].

---

## Invoking the Agent

This is a sub-skill invoked by the `ux-orchestrator`, not directly by users. Users interact with the parent `/user-experience` skill, which routes to this sub-skill based on lifecycle-stage triage.

### Via Natural Language (to parent skill)

```
"Build an atomic design inventory for the form components"
"Audit our design system for component hierarchy completeness"
"Map our components into atoms, molecules, and organisms"
"Check Storybook coverage for our component library"
"Analyze design token consistency across the UI"
"Identify duplicate components we should consolidate"
```

The `ux-orchestrator` routes these requests to `ux-atomic-architect` based on [skills/user-experience/rules/ux-routing-rules.md Section "Stage Routing Table"]. Specifically, the "During design: Building component system" stage routes to `/ux-atomic-design` (source: [ux-routing-rules.md Section "Stage Routing Table"]).

### Via Explicit Agent Request (to parent skill)

```
"Use ux-atomic-architect to classify our checkout page components"
"Have ux-atomic-architect audit design tokens across the navigation system"
```

### Via Agent Tool (orchestrator internal)

The `ux-orchestrator` invokes the agent via the Agent tool:

```python
Agent(
    description="ux-atomic-architect: Atomic design component taxonomy for checkout flow",
    subagent_type="jerry:ux-atomic-architect",
    prompt="""
## UX CONTEXT (REQUIRED)
- **Engagement ID:** UX-0001
- **Topic:** Checkout Flow Component Taxonomy
- **Product:** [product name and domain]
- **Target Users:** [user description]
- **Input:** [component screenshots, Storybook URL, design system documentation]

## TASK
Construct an atomic design component inventory for the checkout flow.
1. Classify all interface elements into Atoms, Molecules, Organisms, Templates, Pages
2. Audit design tokens for consistency (colors, typography, spacing)
3. Document composition rules between levels
4. Assess Storybook coverage and identify gaps
5. Identify duplicate or near-duplicate components for consolidation

## MANDATORY PERSISTENCE (P-002)
Create file at: skills/ux-atomic-design/output/UX-0001/ux-atomic-architect-checkout-flow.md
"""
)
```

> **Governance codification (AD-M-007):** The session_context contract (on_receive/on_send) is specified in `ux-atomic-architect.governance.yaml` per AD-M-007. Fields are enumerated below:

**on_receive fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `engagement_id` | string | Yes | UX engagement identifier (format: `UX-{NNNN}`) |
| `product_context` | string | Yes | Product name, domain, and target user description |
| `component_scope` | string | Yes | Description of the UI scope under analysis (page, flow, or full product) |
| `design_system_references` | array | No | URLs or file paths to existing design system documentation, Storybook instance, or component library |
| `upstream_artifacts` | array | No | File paths to upstream handoff artifacts (heuristic evaluation findings, design screenshots) |

**on_send fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `component_inventory` | array | Yes | Classified components with level (atom/molecule/organism/template/page), variant count, and reuse frequency |
| `design_token_audit` | object | Yes | Token categories (color, typography, spacing, breakpoints) with consistency scores and drift instances |
| `composition_rules` | array | Yes | Documented composition patterns: which lower-level components compose which higher-level components |
| `storybook_coverage` | object | Yes | Coverage percentage, components without stories, missing states and variants |
| `consolidation_candidates` | array | Yes | Duplicate or near-duplicate component pairs with similarity assessment and consolidation recommendation |
| `synthesis_judgments` | array | Yes | AI judgment calls with confidence classification (HIGH/MEDIUM/LOW) and rationale |

> **Source:** Invocation pattern from parent SKILL.md [Invoking an Agent].

---

## Methodology

### Brad Frost's 5-Level Hierarchy

Atomic Design (Frost, 2016) structures interface components into five distinct levels, each building on the level below. The metaphor borrows from chemistry: atoms combine into molecules, molecules combine into organisms, and so on. This creates a shared vocabulary between designers and developers that maps directly to component library organization.

#### Level 1: Atoms

Atoms are the foundational building blocks of the interface -- the smallest functional units that cannot be decomposed further in a meaningful way.

| Category | Examples | Design Token Association |
|----------|---------|------------------------|
| HTML elements | Buttons, inputs, labels, headings, paragraphs, images | Typography tokens, color tokens |
| Design tokens | Color palette, type scale, spacing scale, border radius, shadow | Token definition (not usage) |
| Icons | Icon set entries, icon sizes | Size tokens, color tokens |
| Form elements | Text input, checkbox, radio button, toggle, select | Spacing tokens, border tokens, color tokens |

**Atom identification criteria:** A UI element is an atom if: (a) it serves a single, specific function, (b) it cannot be decomposed into smaller meaningful components, and (c) it maps to a single HTML element or a tightly-coupled element group (e.g., label + input when inseparable). Design tokens are atoms because they define a single visual property value.

#### Level 2: Molecules

Molecules are simple groups of atoms functioning together as a unit. A molecule has a single responsibility composed from multiple atomic parts.

| Pattern | Atoms Combined | Single Responsibility |
|---------|---------------|----------------------|
| Search form | Label atom + Input atom + Button atom | Accepts a search query |
| Form field | Label atom + Input atom + Error message atom | Captures one data value with validation |
| Media object | Image atom + Heading atom + Paragraph atom | Displays a content preview |
| Nav item | Icon atom + Label atom | Represents one navigation option |
| Card header | Avatar atom + Heading atom + Timestamp atom | Identifies card authorship and recency |

**Molecule identification criteria:** A UI group is a molecule if: (a) it combines 2-5 atoms, (b) it serves a single, describable purpose, and (c) removing any atom degrades or breaks its function. If a group serves multiple distinct purposes, it is likely an organism.

> **Boundary adjudication -- molecule vs. organism:** When a component group is ambiguous (e.g., a complex form field with 5 atoms that could be interpreted as serving multiple sub-purposes), apply this tie-breaker: if the group contains other molecules as children, classify as organism regardless of atom count. If all children are atoms and the group can be described with a single verb-noun phrase (e.g., "captures search query"), classify as molecule. If uncertain after these checks, classify as organism and document the rationale -- over-classifying as organism is safer than under-classifying because organisms carry explicit layout logic documentation that molecules do not.

#### Level 3: Organisms

Organisms are complex, distinct sections of an interface composed of molecules and atoms. Organisms form recognizable sections of a page.

| Pattern | Components Combined | Section Role |
|---------|-------------------|--------------|
| Header | Logo atom + Navigation molecule + Search form molecule + User menu molecule | Global site navigation and identity |
| Product card grid | Multiple Product card organisms (each = image + title + price + CTA) | Displays a collection of product options |
| Comment thread | Comment molecule (avatar + text + timestamp) repeated + Reply form molecule | Displays conversation with reply capability |
| Sidebar navigation | Nav group organisms (heading + nav item molecules) | Section-level wayfinding |
| Footer | Link list molecules + Social icons molecule + Copyright atom | Global site information and legal |

**Organism identification criteria:** A UI section is an organism if: (a) it combines multiple molecules and/or atoms, (b) it represents a distinct, recognizable section of an interface, (c) it could be reused in different template contexts, and (d) it has its own internal layout logic. When a component group meets criteria (a) and (b) but is uncertain on (c) and (d), check: does the group serve multiple distinct user purposes simultaneously (e.g., navigation AND search AND user identity)? If yes, classify as organism. If the group serves a single purpose but is structurally complex (many atoms), see the molecule boundary adjudication note above.

#### Level 4: Templates

Templates are page-level layout structures that define the arrangement of organisms without specific content. Templates use placeholder content to show the structural composition.

| Pattern | Organisms Arranged | Layout Purpose |
|---------|-------------------|----------------|
| Product listing template | Header + Filter sidebar + Product card grid + Pagination + Footer | E-commerce browse layout |
| Dashboard template | Header + Sidebar nav + Metric cards + Data table + Footer | Analytics overview layout |
| Article template | Header + Hero image + Content body + Author bio + Comment thread + Footer | Long-form content layout |
| Settings template | Header + Settings sidebar nav + Settings form + Footer | Preference management layout |

**Template identification criteria:** A layout is a template if: (a) it arranges organisms into a complete page structure, (b) it uses placeholder content rather than real data, (c) it defines the spatial relationships between organisms, and (d) multiple pages could instantiate the same template with different content.

#### Level 5: Pages

Pages are specific instances of templates populated with real, representative content. Pages are the highest fidelity representation and the point where the design system meets actual user data.

| Template Instance | Real Content Applied | Validation Purpose |
|-------------------|---------------------|-------------------|
| Product listing page | 24 products with real images, prices, descriptions | Validates template handles variable content lengths, image ratios, price formats |
| Dashboard page | Real metrics, 30-day data range, 5 alert notifications | Validates template handles data density, empty states, alert states |
| Article page | 2,500-word article, 15 comments, 3 inline images | Validates template handles long-form content, nested comments, image placement |

**Page validation criteria:** Pages validate that templates work with real content by testing: (a) content length variation (short, medium, long), (b) empty states (no data, loading states), (c) error states (failed loads, invalid data), (d) edge cases (very long titles, special characters, missing images).

### Design Token Architecture

Design tokens are the sub-atomic foundation of the component hierarchy -- the named values that atoms consume. Token auditing ensures consistency across the entire design system.

| Token Category | Examples | Consistency Check |
|---------------|---------|-------------------|
| **Color** | Primary, secondary, surface, error, text, border | No unnamed hex/rgb values in components; all colors reference token names |
| **Typography** | Font family, font size scale, line height, font weight | No magic number font sizes; all text styles reference token scale |
| **Spacing** | Margin scale, padding scale, gap scale | No arbitrary pixel values; all spacing references token scale |
| **Breakpoints** | Mobile, tablet, desktop, wide | Consistent breakpoint values across all responsive components |
| **Elevation** | Shadow levels (none, low, medium, high) | Shadow values match defined elevation tokens |
| **Border** | Border width, border radius, border style | Consistent radius and width across similar component types |
| **Motion** | Duration, easing, transition types | Animation timing consistent with motion token definitions |

**Token drift detection:** The architect identifies "token drift" -- instances where components use hardcoded values instead of design token references. Token drift is quantified as: `drift_ratio = hardcoded_values / total_style_values`. A drift ratio above 0.20 (20% hardcoded values) indicates significant design system inconsistency and is flagged as a HIGH priority finding. *(Heuristic threshold: the 0.20 value is a framework-internal heuristic derived from the reasoning that a design system where more than 1 in 5 style values bypass the token system has lost meaningful token governance. Adjust based on team design system maturity -- nascent systems may tolerate 0.30; mature systems should target < 0.10.)*

### Composition Rules

Composition rules document valid assembly patterns between hierarchy levels. These rules prevent inconsistent component usage and serve as the structural backbone of the design system.

| Rule Type | Description | Example |
|-----------|-------------|---------|
| **Atom-to-Molecule** | Which atoms combine into which molecules | Button atom + Input atom + Label atom = Search form molecule |
| **Molecule-to-Organism** | Which molecules compose which organisms | Search form molecule + Nav item molecules + Logo atom = Header organism |
| **Organism-to-Template** | Which organisms arrange into which templates | Header + Sidebar + Content area + Footer = Dashboard template |
| **Forbidden compositions** | Combinations that violate design system intent | Organism inside another organism at the same hierarchy level (nesting violation) |
| **Optional compositions** | Components that may or may not appear in a parent | Error message atom is optional within Form field molecule |

### Storybook Coverage Model

Storybook coverage measures how well the component library is documented with interactive stories. Coverage assessment operates at three granularity levels:

| Coverage Level | Description | Target |
|---------------|-------------|--------|
| **Component coverage** | Percentage of classified components with at least one Storybook story | >= 80% for atoms, >= 60% for molecules/organisms |
| **State coverage** | Percentage of component states (default, hover, active, disabled, error, loading) documented | >= 70% for atoms, >= 50% for molecules |
| **Variant coverage** | Percentage of component variants (size, color, style) with individual stories | >= 60% for atoms, >= 40% for molecules |

> **Coverage target rationale (heuristic thresholds):** These percentage targets are framework-internal heuristics, not industry-standard benchmarks. The rationale: atoms are the foundation of the entire hierarchy -- higher coverage targets (80%/70%/60%) reflect their outsized reuse impact (a single undocumented atom affects every molecule and organism that consumes it). Molecules and organisms have lower targets (60%/50%/40%) because their higher structural complexity makes exhaustive documentation costlier per component, and their reuse frequency is typically lower than atoms. Adjust all thresholds based on team capacity and design system maturity. See Storybook's "Component-Driven Development" guide (storybook.js.org/tutorials/intro-to-storybook/) for the principle that foundational components warrant the highest documentation investment.

**Coverage gap identification:** Components without any Storybook story are flagged as "undocumented" and prioritized by: (a) reuse frequency (high-reuse undocumented components are highest priority), (b) hierarchy level (atoms first, as they are the foundation), (c) complexity (components with multiple states/variants need documentation more urgently).

### Execution Phases

> **Note:** This execution procedure describes target behavior for the fully-implemented `ux-atomic-architect` agent. The current agent definition is a Wave 3 stub; full implementation will follow this specification.

The architect follows a 5-phase sequential workflow. Each phase produces intermediate artifacts that feed the next. This mirrors the Phase 1-5 structure established by the HEART metrics and Lean UX sub-skills.

#### Phase 1: Scope Definition

**Purpose:** Establish the component scope, confirm wave entry criteria, and determine the MCP operating mode (Storybook-connected or manual inventory).

**Activities:**
1. Identify the product domain, target users, and the specific screens, flows, or feature areas to be inventoried
2. Confirm Wave 3 entry criteria are met: Wave 2 completed (launched product with analytics OR 1 completed Lean UX hypothesis cycle), OR bypass condition satisfied (Storybook already in use). *(Verification: check for a `WAVE-2-SIGNOFF.md` artifact or prior `/ux-lean-ux` or `/ux-heart-metrics` output artifacts in `skills/user-experience/output/`; if no documentary evidence is found, ask the user to confirm which wave entry condition is satisfied per H-31.)*
3. Catalog upstream inputs: check for `/ux-heuristic-eval` severity-rated findings with component inconsistency citations (heuristic #4); if present, import finding IDs to inform refactoring priorities
4. Determine MCP operating mode: probe for Storybook MCP adapter availability; if unavailable, activate Manual Component Inventory Mode and prepare P-022 degraded mode disclosure
5. Establish design system references: identify the component library (e.g., Material UI, Radix, Shadcn/ui, custom), design token documentation, and existing Storybook instance URL (if any)

**Output:** Scope brief documenting: product domain, component scope boundaries (which screens/flows are in scope), upstream heuristic findings (if any), MCP mode (connected/manual), and design system references.

#### Phase 2: Component Inventory Construction

**Purpose:** Systematically identify and classify all components within the defined scope using the 5-level hierarchy.

**Activities:**
1. Inventory atoms first: scan each in-scope screen/flow for foundational elements (buttons, inputs, labels, icons, form elements) using the atom identification criteria; record component name, variant count, and design token association
2. Inventory molecules second: identify groups of 2-5 atoms that function together as a unit using the molecule identification criteria; apply the boundary adjudication tie-breaker when classification is ambiguous (see molecule vs. organism adjudication note above)
3. Inventory organisms third: identify distinct interface sections composed of molecules and atoms using the organism identification criteria; verify each candidate meets all four criteria (combines molecules/atoms, recognizable section, reusable across templates, has internal layout logic)
4. Inventory templates fourth: identify page-level layout structures that arrange organisms using the template identification criteria; verify templates use placeholder content rather than real data
5. Inventory pages fifth: identify specific template instances populated with real content; document which template each page instantiates and what content variations it tests
6. Cross-check completeness: verify that every molecule references at least one atom, every organism references at least one molecule, every template references at least one organism, and every page references exactly one template; flag orphaned components (referenced by no parent) and dangling references (parent references a non-existent child)

**Output:** Complete 5-level component inventory with: component name, classification level, variant count, reuse frequency, composition parent(s), and Storybook story status (documented/undocumented/partial). Orphaned components and dangling references listed separately.

#### Phase 3: Design Token Audit

**Purpose:** Audit design token consistency across all inventoried components, per the Design Token Architecture specification.

**Activities:**
1. For each of the 7 token categories (color, typography, spacing, breakpoints, elevation, border, motion), catalog the defined token values from the design system documentation
2. Inspect component implementations (via Storybook stories, design file inspection, or user-provided documentation) for token usage vs. hardcoded values
3. Calculate the drift ratio per token category: `drift_ratio = hardcoded_values / total_style_values`; flag any category with drift ratio above the 0.20 heuristic threshold
4. Assess token naming convention consistency: are token names systematic (e.g., `color-primary-500`) or ad hoc (e.g., `blue3`, `mainColor`)?
5. Identify cross-component token inconsistencies: cases where two components use different tokens for the same visual purpose (e.g., two different spacing tokens for card padding)

**Output:** Design token audit with: per-category token inventory, drift ratio per category, drift instances (component name + hardcoded value + suggested token replacement), naming convention assessment, and cross-component inconsistency list.

#### Phase 4: Storybook Coverage Assessment

**Purpose:** Assess how well the component library is documented with interactive Storybook stories.

**Activities:**
1. For each hierarchy level (atoms, molecules, organisms, templates, pages), count total components and components with at least one Storybook story; calculate component coverage percentage
2. For documented components at the atom and molecule level, assess state coverage: count documented states (default, hover, active, disabled, error, loading) vs. total applicable states
3. For documented components at the atom and molecule level, assess variant coverage: count variants with individual stories vs. total variants
4. Compare coverage percentages against the heuristic targets (component: >= 80% atoms, >= 60% molecules/organisms; state: >= 70% atoms, >= 50% molecules; variant: >= 60% atoms, >= 40% molecules)
5. Prioritize undocumented components using the coverage gap identification criteria: reuse frequency first, hierarchy level second (atoms before molecules), complexity third

**Output:** Storybook coverage report with: per-level component coverage, state coverage, variant coverage, coverage percentages vs. targets, and prioritized list of undocumented components with coverage gap severity.

#### Phase 5: Synthesis and Handoff Preparation

**Purpose:** Synthesize findings across all phases, identify consolidation opportunities, assess design system maturity, and prepare the handoff for downstream sub-skills.

**Activities:**
1. Identify consolidation candidates: scan the component inventory for duplicate or near-duplicate component pairs (similar name, overlapping purpose, or shared composition); assess similarity and recommend consolidation with estimated effort
2. Quantify design debt: count components with drift ratio violations, undocumented Storybook stories, orphaned components, and naming inconsistencies; produce a design debt score
3. Assess design system maturity: classify as nascent (< 30% component coverage, no token governance — drift ratio > 0.30), developing (30-60% component coverage, partial token governance — drift ratio 0.15-0.30), mature (60-80% component coverage, systematic tokens — drift ratio 0.05-0.15), or optimized (> 80% component coverage, full token governance — drift ratio < 0.05, composition rules enforced). *(Heuristic thresholds: coverage percentage refers to component coverage from Phase 4 Activity 1; state and variant coverage are secondary factors. The tier boundaries are framework-internal heuristics derived from the principle that a design system with < 30% documented components lacks the critical mass for systematic reuse, while > 80% reflects near-comprehensive coverage. Token governance levels are operationalized via drift ratio ranges from the Design Token Architecture section. Adjust thresholds based on team context and design system maturity stage.)*
4. Produce the L0 executive summary: component count by hierarchy level, design token consistency score, Storybook coverage percentage, top 3-5 consolidation opportunities
5. Produce the L2 strategic implications: design system maturity assessment, consolidation roadmap, design debt reduction trajectory, governance recommendations
6. Compile the Synthesis Judgments Summary: list every AI judgment call (component classification decisions, drift ratio assessments, consolidation recommendations) with confidence classification (HIGH/MEDIUM/LOW) and one-line rationale per the synthesis validation protocol
7. Prepare the `/ux-inclusive-design` handoff: extract the component inventory subset that meets the handoff threshold (classification level assigned AND at least name and variant count) with Storybook story URLs where available

**Output:** Complete output artifact per the Required Output Sections specification (L0 executive summary, L1 technical sections, L2 strategic implications, synthesis judgments, handoff data). Design system maturity classification. Handoff payload for `/ux-inclusive-design`.

> **Source:** Frost, B. (2016). "Atomic Design." Self-published. atomicdesign.bradfrost.com. Storybook coverage model informed by Storybook "Component-Driven Development" guide (storybook.js.org/tutorials/intro-to-storybook/, 2024). Execution phase structure follows the Phase 1-5 pattern established by `skills/ux-heart-metrics/SKILL.md` and `skills/ux-lean-ux/SKILL.md`.

---

## MCP Dependencies

### Dependency Matrix

| MCP Tool | Classification | Purpose | Fallback |
|----------|---------------|---------|----------|
| **Storybook** | **REQ** | Browse component stories, validate coverage, inspect component variants and states | Manual component inventory: user provides component list, documentation links, and screenshot references |
| **Figma** | ENH | Reference design file component structures, inspect layer hierarchy and style tokens | Text description mode: component structures described textually; screenshot references where available |
| **Zeroheight** | ENH | Query design system documentation for token definitions, usage guidelines, and component specifications | Text-based design system reference: user provides design token documentation and component guidelines |
| **Context7** | Available (current infrastructure) | Resolve and query component library documentation (Material UI, Radix, Shadcn/ui, Storybook API) | WebSearch fallback per MCP-001 (`.context/rules/mcp-tool-standards.md` [Error Handling]) |

### Storybook Fallback: Manual Component Inventory Mode

When the Storybook MCP adapter is unavailable (current state -- adapter implementation is post-PROJ-022 scope), the architect operates in manual component inventory mode:

- Component inventories are produced from user-provided component lists, screenshots, and documentation links
- Storybook coverage assessment relies on user-reported coverage data rather than automated story inspection
- Component state and variant documentation is based on textual descriptions rather than live story browsing
- **Limitations in manual mode:**
  - Cannot browse or validate live component stories programmatically
  - Cannot inspect component variants, states, or props interactively
  - Cannot verify design token usage in component implementations
  - Coverage assessment accuracy depends on completeness of user-provided inventory
- Output carries a degraded mode disclosure per P-022:
  ```
  [DEGRADED MODE] This output was produced without Storybook MCP access.
  Input was provided via manual component inventory mode. Some features are reduced:
  - Cannot browse or validate live component stories
  - Cannot inspect component variants, states, or props interactively
  - Cannot verify design token usage in component implementations
  - Coverage assessment accuracy depends on user-provided inventory completeness
  ```

### Context7 Usage

Per MCP-001 (`.context/rules/mcp-tool-standards.md` [Context7 Integration]), Context7 is used when the analysis references external component libraries or design system frameworks by name:

| Library/Framework | Usage |
|-------------------|-------|
| Material UI (MUI) | Component pattern documentation, design token structure, theming API |
| Radix UI | Accessible component API docs, composition patterns, primitive components |
| Shadcn/ui | Component implementation patterns, Tailwind token integration |
| Storybook | Story format documentation, addon configuration, coverage reporting APIs |
| Tailwind CSS | Utility class taxonomy, design token mapping, responsive breakpoint system |
| Chakra UI | Component API documentation, style props, theme tokens |

Protocol: call `mcp__context7__resolve-library-id` with the library name, then `mcp__context7__query-docs` with the resolved ID and specific query. If Context7 returns no results, fall back to WebSearch per `.context/rules/mcp-tool-standards.md` [Error Handling].

> **Source:** MCP dependency matrix from [skills/user-experience/SKILL.md Section "MCP Integration Architecture"] (`/ux-atomic-design` row showing Figma ENH, Storybook REQ, Zeroheight ENH) and [skills/user-experience/rules/mcp-coordination.md Section "MCP Dependency Matrix"], [skills/user-experience/rules/mcp-coordination.md Section "Degraded Mode Behavior"].

---

## Output Specification

### Output Location

```
skills/ux-atomic-design/output/{engagement-id}/ux-atomic-architect-{topic-slug}.md
```

Where:
- `{engagement-id}` follows the pattern `UX-{NNNN}` (e.g., `UX-0001`)
- `{topic-slug}` is a kebab-case descriptor of the component scope (e.g., `checkout-flow`, `navigation-system`, `full-product`)

### Required Output Sections

| Section | Level | Content |
|---------|-------|---------|
| **Executive Summary** | L0 | Component count by hierarchy level; design token consistency score; Storybook coverage percentage; top 3-5 consolidation opportunities; key findings for stakeholders and cross-framework synthesis input |
| **Engagement Context** | L1 | Product description, target users, component scope, design system references, upstream inputs (heuristic evaluation findings, design screenshots), MCP status |
| **Component Inventory** | L1 | Full 5-level component inventory with: component name, classification level (atom/molecule/organism/template/page), variant count, reuse frequency, Storybook story status (documented/undocumented/partial), composition parent(s) |
| **Design Token Audit** | L1 | Token categories inventoried (color, typography, spacing, breakpoints, elevation, border, motion); consistency score per category; drift instances (hardcoded values); token naming convention assessment |
| **Composition Rules** | L1 | Documented assembly patterns between hierarchy levels; forbidden compositions; optional compositions; composition diagram (text-based hierarchy) |
| **Storybook Coverage Report** | L1 | Component coverage percentage; state coverage percentage; variant coverage percentage; undocumented components prioritized by reuse frequency; coverage gaps by hierarchy level |
| **Consolidation Candidates** | L1 | Duplicate or near-duplicate component pairs; similarity assessment; consolidation recommendation with estimated effort; design debt quantification |
| **Strategic Implications** | L2 | Design system maturity assessment (nascent/developing/mature/optimized); component consolidation roadmap; design debt reduction trajectory; design system governance recommendations |
| **Synthesis Judgments Summary** | L1 | Each AI judgment call listed for synthesis confidence gate compliance (see note below) |
| **Handoff Data** | L1 | Structured data for downstream sub-skills: component inventory with Storybook references (for `/ux-inclusive-design` accessibility audit consumption) |

**Synthesis Judgments Summary requirements:** This section MUST list every AI-generated judgment (component classification level assignment, design token consistency scoring, consolidation recommendations) with a confidence classification (HIGH, MEDIUM, LOW) and a one-line rationale. This enables downstream consumers (including `/ux-inclusive-design` and the `ux-orchestrator` synthesis gate) to assess which findings are strongly supported versus which require additional validation. The format follows the synthesis judgments pattern established in `skills/user-experience/rules/synthesis-validation.md`.

### Templates

| Template | Path | Purpose |
|----------|------|---------|
| Component Inventory Template | `skills/ux-atomic-design/templates/component-inventory-template.md` [PLANNED: Wave 3 Phase 2] | 5-level component inventory with classification, coverage, and composition columns |

> **Source:** Output location from [skills/user-experience/SKILL.md Section "Available Agents"] and ORCHESTRATION.yaml pipeline-wave3 phase-1 artifacts.

---

## Routing

### Trigger Keywords

| Keyword | Routing Context |
|---------|----------------|
| atomic design | Direct match -- primary trigger |
| component taxonomy | Direct match |
| design tokens | Direct match |
| Storybook | In combination with UX/design context |
| atoms molecules organisms | Direct match (phrase) |
| design system architecture | Direct match |
| component inventory | Direct match |
| component library | In combination with UX/design/audit context |

### Lifecycle-Stage Routing Integration

This sub-skill is routed to by the `ux-orchestrator` in the following lifecycle-stage scenarios:

| Stage | User Intent | Route Condition |
|-------|-------------|-----------------|
| During design | "Building component system" | Direct route to `/ux-atomic-design`; source: [ux-routing-rules.md Section "Stage Routing Table"] |
| During design | Follow-up from heuristic evaluation | When `/ux-heuristic-eval` has identified component inconsistency findings; severity-rated findings inform component refactoring priorities |
| Any stage | "Audit our component library" or "Classify our components" | Component-focused intent detected; routes to Atomic Design for taxonomy construction |

### Wave Gating

This sub-skill is in **Wave 3** (Design System). It requires Wave 2 completion before deployment:

**Entry criteria:** Wave 2: launched product with analytics OR 1 completed Lean UX hypothesis cycle.

**Bypass condition:** Storybook already in use (skip Lean UX prerequisite for Atomic Design). This bypass recognizes that teams with an existing Storybook setup have already demonstrated design system maturity that the Wave 2 prerequisites are designed to establish.

> **Source:** Routing integration from [skills/user-experience/rules/ux-routing-rules.md Section "Stage Routing Table"] and [skills/user-experience/SKILL.md Section "Lifecycle-Stage Routing"]. Wave assignment from [skills/user-experience/SKILL.md Section "Wave Architecture"].

---

## Cross-Framework Integration

### Upstream Inputs

This sub-skill receives context from other sub-skills when invoked as part of a multi-sub-skill workflow:

| From Sub-Skill | Handoff Artifact | Key Fields | Usage |
|----------------|-----------------|-----------|-------|
| `/ux-heuristic-eval` | Severity-rated findings | Finding ID, heuristic violated, severity (0-4), affected screen/flow, affected component | Heuristic findings with severity >= 2 that cite component inconsistency (heuristic #4 "Consistency and Standards") inform component refactoring priorities; high-severity component-related findings suggest atoms or molecules that need redesign or consolidation |

### Downstream Handoffs

This sub-skill produces artifacts that feed into other sub-skills via the Jerry handoff protocol (`docs/schemas/handoff-v2.schema.json`).

| To Sub-Skill | Handoff Artifact | Key Fields | Trigger |
|-------------|-----------------|-----------|---------|
| `/ux-inclusive-design` | Component inventory with Storybook references | Component name, classification level, Storybook story URL (if available), variant list, design token usage | After component inventory is complete; inclusive design evaluator audits each component for WCAG 2.2 AA accessibility compliance |

**Handoff threshold:** Only components with classification level assigned (atom through page) and at least a name and variant count are included in cross-framework handoffs. Components identified but not yet classified remain in the inventory but are not propagated to the inclusive design evaluator.

### Canonical Multi-Skill Workflow Sequences

This sub-skill participates in the following canonical sequences:

| Sequence | Skills Involved | This Sub-Skill's Role |
|----------|----------------|-----------------------|
| Build to Evaluate | **`/ux-atomic-design`** then `/ux-inclusive-design` | Produces the component inventory; inclusive design evaluates each component for accessibility compliance |
| Evaluate to Refactor to Evaluate | `/ux-heuristic-eval` then **`/ux-atomic-design`** then `/ux-inclusive-design` | Heuristic findings identify component issues; Atomic Design refactors the taxonomy; inclusive design validates accessibility |

> **Source:** Handoff data contracts from [skills/user-experience/rules/ux-routing-rules.md Section "Handoff Data Contracts"] and [skills/user-experience/SKILL.md Section "Cross-Sub-Skill Handoff Data"] ("/ux-atomic-design -> /ux-inclusive-design: Component inventory with Storybook references"). Canonical sequences from [skills/user-experience/SKILL.md Section "Canonical Multi-Skill Workflow Sequences"].

---

## Synthesis Hypothesis Confidence

Atomic Design outputs include synthesis hypotheses that carry confidence classifications per the synthesis validation protocol.

| Synthesis Step | Typical Confidence | Rationale |
|---------------|-------------------|-----------|
| Component taxonomy completeness assessment | MEDIUM | Taxonomy assessment depends on Storybook coverage (Frost, 2016); partial coverage yields partial assessment -- the architect may miss components not visible in the provided inventory |
| Design token consistency analysis | LOW | Token consistency across a full system requires inspection of all component variants; AI sampling may miss edge cases where hardcoded values override token references in specific states or responsive breakpoints |

**Gate enforcement:**
- **MEDIUM outputs (taxonomy completeness):** Include a "Validation Required" section. Design recommendations for taxonomy restructuring are withheld until validation against the full Storybook instance or a manual component audit confirms the inventory is complete.
- **LOW outputs (token consistency):** Output template structurally omits design token remediation recommendations. Title tagged with `[REFERENCE-ONLY]` for the token consistency section. Banner: "Token consistency analysis reflects AI sampling of available component documentation. It does not represent a comprehensive token audit."

**Note on confidence dynamics:** Component taxonomy completeness can achieve HIGH synthesis confidence when converged with a second framework -- for example, when `/ux-heuristic-eval` identifies component inconsistency findings that corroborate the taxonomy gaps found by `/ux-atomic-design`. Design token consistency remains LOW because comprehensive token auditing requires programmatic inspection of every component variant's style declarations, which exceeds AI text-analysis capabilities.

> **Source:** Confidence classifications from [skills/user-experience/rules/synthesis-validation.md Section "Sub-Skill Synthesis Output Map"] ("`/ux-atomic-design` Component taxonomy completeness assessment MEDIUM" and "`/ux-atomic-design` Design token consistency analysis LOW"). Gate enforcement from [skills/user-experience/SKILL.md Section "Synthesis Hypothesis Validation"].

---

## Constitutional Compliance

All agents in this sub-skill adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- worker agent, no Agent tool access | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user decisions on component classification or consolidation priorities | Unauthorized action; trust erosion |
| P-022 | NEVER present component coverage as complete without disclosing inventory scope limitations; NEVER inflate design token consistency scores without comprehensive evidence | Governance undermined; quality assessment invalidated |
| P-001 | NEVER present component classifications without reasoning for the hierarchy level assignment | Unreliable outputs; unfounded claims propagate downstream |
| P-002 | NEVER leave component inventories or design token audits in transient context only -- persist to files | Context rot vulnerability; artifacts lost on session compaction |

**Per-agent enforcement:** The `ux-atomic-architect` agent declares:
- `constitution.principles_applied`: P-003, P-020, P-022, P-001, P-002 in `skills/ux-atomic-design/agents/ux-atomic-architect.governance.yaml`
- `capabilities.forbidden_actions`: 3 entries in NPT-009 format referencing the constitutional triplet
- `disallowedTools: [Agent]` in `skills/ux-atomic-design/agents/ux-atomic-architect.md` frontmatter

### AI-Augmented Analysis Limitations

The Atomic Design architect agent operates as an AI-augmented analysis tool. The following limitations apply to all outputs and MUST be disclosed per P-022 (no deception):

- **Component classification is judgment-based.** The boundary between molecules and organisms, or between organisms and templates, involves subjective judgment. Different designers may classify the same component group differently. The architect provides classification rationale but the team should review and adjust classifications to match their design system conventions.
- **Storybook coverage is inventory-dependent.** Coverage percentages are calculated from the components identified in the inventory. If the provided component scope is incomplete, coverage percentages will be artificially inflated. Manual mode (without Storybook MCP) produces less accurate coverage assessments.
- **Design token analysis is sampling-based.** The architect analyzes design tokens from available documentation and component descriptions, not from programmatic inspection of CSS/style declarations. Hardcoded values in component implementations may not be detected through text-based analysis alone.
- **Composition rules reflect common patterns.** Documented composition rules are based on the provided component inventory and common design system patterns. Actual valid compositions in a specific design system may differ based on context-specific requirements.
- **Always validate with the live component library.** Component inventories, coverage reports, and token audits should be confirmed against the actual Storybook instance, design files, and codebase before making design system restructuring decisions.

---

## Registration

This sub-skill follows a parent-routed registration model. Sub-skills are not independently registered in `CLAUDE.md` or `mandatory-skill-usage.md` because they are routed through the parent `/user-experience` orchestrator (`ux-orchestrator`). This is an explicit exception to the H-26 registration requirement (parent-routed model): parent skills own the CLAUDE.md and mandatory-skill-usage.md registration; sub-skills are discovered and dispatched by the parent orchestrator's internal routing logic.

| Registration Point | Status | Detail |
|--------------------|--------|--------|
| `CLAUDE.md` skill table | Registered via parent | `/user-experience` is registered in `CLAUDE.md`; sub-skills are not independently listed |
| `mandatory-skill-usage.md` trigger map | Routed via parent | The `/user-experience` trigger map row includes "atomic design" as a positive keyword (H-22); requests matching this keyword route to the parent skill, which dispatches to this sub-skill |
| `AGENTS.md` agent registry | Registered | `ux-atomic-architect` is listed in `AGENTS.md` under the User-Experience Skill Agents section |
| Parent SKILL.md agent table | Registered | `ux-atomic-architect` is listed in `skills/user-experience/SKILL.md` [Available Agents] |

> **H-26 parent-routed model rationale:** Independent registration of sub-skills would create duplicate trigger map entries and ambiguous routing (AP-02 Bag of Triggers). The parent orchestrator owns lifecycle-stage routing logic and dispatches to the correct sub-skill based on triage qualification, not keyword matching alone. Sub-skill agents are registered in `AGENTS.md` for discoverability but routing flows through the parent.

---

## Deployment Status

> **Wave 3 Sub-Skill -- Stub Agent.** This sub-skill is part of Wave 3 (Design System) of PROJ-022. The companion agent file (`skills/ux-atomic-design/agents/ux-atomic-architect.md`) is pending implementation as part of PROJ-022 EPIC-003. Full agent implementation (`<input>`, `<capabilities>`, `<methodology>`, `<output>` sections) will follow the SKILL.md specification of methodology, output format, and routing integration defined here.

---

## Quick Reference

### Common Workflows

| Need | Command Example |
|------|-----------------|
| Build component taxonomy | "Build an atomic design inventory for the dashboard components" |
| Audit design tokens | "Audit design token consistency across our form components" |
| Check Storybook coverage | "Check Storybook coverage for our component library" |
| Find duplicate components | "Identify duplicate components we should consolidate" |
| Document composition rules | "Document which atoms compose which molecules in our navigation" |
| Prepare for accessibility audit | "Create a component inventory to hand off to inclusive design review" |

### Agent Selection Hints

| Keywords | Routes To |
|----------|-----------|
| atomic design, component taxonomy, design tokens, Storybook, design system, component inventory, component library, atoms, molecules, organisms | `ux-atomic-architect` |
| heuristic, usability, Nielsen, severity, inspection, evaluation | `/ux-heuristic-eval` (not this sub-skill) |
| accessibility, WCAG, inclusive, persona spectrum, a11y | `/ux-inclusive-design` (not this sub-skill) |
| lean UX, hypothesis, assumption, experiment, build-measure-learn | `/ux-lean-ux` (not this sub-skill) |
| HEART, metrics, measurement, GSM, happiness, engagement | `/ux-heart-metrics` (not this sub-skill) |
| jobs to be done, JTBD, switch interview, user motivation | `/ux-jtbd` (not this sub-skill) |

---

## References

| Source | Content | Path |
|--------|---------|------|
| Parent SKILL.md | Sub-skill scope, wave architecture, routing, MCP dependencies, synthesis protocol | `skills/user-experience/SKILL.md` |
| Agent definition | Agent frontmatter, identity, expertise, guardrails | `skills/ux-atomic-design/agents/ux-atomic-architect.md` [PLANNED] |
| Agent governance | Tool tier, forbidden actions, output validation, constitutional compliance | `skills/ux-atomic-design/agents/ux-atomic-architect.governance.yaml` [PLANNED] |
| UX routing rules | Lifecycle-stage routing, handoff data contracts, common intent resolution | `skills/user-experience/rules/ux-routing-rules.md` |
| MCP coordination | Storybook REQ dependency, degraded mode behavior, Context7 usage | `skills/user-experience/rules/mcp-coordination.md` |
| Synthesis validation | Confidence gate protocol, per-sub-skill confidence map | `skills/user-experience/rules/synthesis-validation.md` |
| Wave progression | Wave 3 entry criteria, signoff requirements | `skills/user-experience/rules/wave-progression.md` |
| CI checks | P-003 enforcement, sub-skill validation gates | `skills/user-experience/rules/ci-checks.md` |
| Component inventory template | 5-level component inventory with classification and coverage columns | `skills/ux-atomic-design/templates/component-inventory-template.md` [PLANNED: Wave 3 Phase 2] |
| Skill standards | H-25/H-26 skill structure requirements | `.context/rules/skill-standards.md` |
| Agent development standards | H-34 dual-file architecture, tool tiers, handoff protocol | `.context/rules/agent-development-standards.md` |
| Quality enforcement | Quality gate thresholds, criticality levels, strategy catalog | `.context/rules/quality-enforcement.md` |
| Handoff schema | Canonical handoff schema v2 | `docs/schemas/handoff-v2.schema.json` |
| Agent governance schema | Governance YAML validation schema | `docs/schemas/agent-governance-v1.schema.json` |

### Requirements Traceability

| Source | Content | Path |
|--------|---------|------|
| PROJ-022 PLAN.md | Project plan: sub-skill scope, wave assignment, acceptance criteria, implementation phases | `projects/PROJ-022-user-experience-skill/PLAN.md` |
| EPIC-003 (Wave 3 Deployment) | Parent work item for Wave 3 sub-skill implementation including this sub-skill | PROJ-022 EPIC-003 in `projects/PROJ-022-user-experience-skill/WORKTRACKER.md` |
| ORCHESTRATION.yaml | Orchestration plan governing the build sequence for this sub-skill | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |

### External References

| Source | Citation |
|--------|----------|
| Frost, B. (2016) | "Atomic Design." Self-published. atomicdesign.bradfrost.com. The foundational text defining the 5-level component hierarchy. |
| Storybook Docs (2024) | "Introduction to Storybook" and "Component-Driven Development" guides. storybook.js.org/tutorials/intro-to-storybook/. Component documentation and testing tool for UI development; coverage model and story-per-component principles inform the Storybook Coverage Model in this sub-skill. |
| Material Design (Google) | Material Design system. material.io. Reference implementation of design token architecture and component taxonomy. |

---

*Sub-Skill Version: 1.2.0*
*Parent Skill: `/user-experience` v1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Wave: 3 (Design System)*
*SSOT: `skills/user-experience/SKILL.md`*
*Project: PROJ-022 User Experience Skill*
*Created: 2026-03-04*
