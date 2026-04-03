---
name: ux-inclusive-design
description: "Inclusive design and WCAG 2.2 accessibility evaluation sub-skill for the /user-experience parent skill. Performs WCAG 2.2 compliance audits across Perceivable, Operable, Understandable, and Robust principles (conformance levels A, AA, AAA) and applies Microsoft Inclusive Design methodology including Persona Spectrum analysis (permanent, temporary, situational disabilities). Produces accessibility audit reports and persona spectrum analyses. Invoke when teams need accessibility compliance evaluation, WCAG conformance auditing, screen reader compatibility assessment, color contrast analysis, cognitive load evaluation, or inclusive design review. Invoked by ux-orchestrator during Wave 3 lifecycle-stage routing or when user intent is \"Check accessibility\" at any lifecycle stage. Triggers: accessibility, WCAG, ARIA, screen reader, contrast, cognitive load, inclusive, a11y, inclusive design, WCAG 2.2, persona spectrum."
version: "1.1.0"
model: sonnet
agents:
  - ux-inclusive-evaluator
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
activation-keywords:
  - "accessibility"
  - "WCAG"
  - "WCAG 2.2"
  - "ARIA"
  - "screen reader"
  - "contrast"
  - "cognitive load"
  - "inclusive design"
  - "a11y"
  - "persona spectrum"
  - "inclusive"
---

<!-- VERSION: 1.1.0 | DATE: 2026-03-04 | SOURCE: skills/user-experience/SKILL.md | PARENT: /user-experience skill | REVISION: Iter2 quality gate fixes -- complete Synthesis Hypothesis Confidence table (3 entries), model frontmatter, inline citations, severity cross-reference, reading level eval method, Nielsen severity alignment note -->

# Inclusive Design Sub-Skill

> **Version:** 1.1.0
> **Framework:** Jerry User-Experience -- Inclusive Design
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
| [Methodology](#methodology) | WCAG 2.2 compliance audit, Microsoft Inclusive Design Persona Spectrum, accessibility testing protocols |
| [MCP Dependencies](#mcp-dependencies) | Figma REQ with screenshot-input fallback; Storybook ENH; Context7 for WCAG and ARIA docs |
| [Output Specification](#output-specification) | Output location, L0/L1/L2 structure, required sections |
| [Routing](#routing) | Keywords and lifecycle-stage routing integration |
| [Cross-Framework Integration](#cross-framework-integration) | Handoff from Atomic Design and Heuristic Eval; accessibility findings output |
| [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence) | Confidence classifications for Inclusive Design outputs |
| [Constitutional Compliance](#constitutional-compliance) | Governing principles and AI-augmented analysis limitations |
| [Registration](#registration) | H-26 parent-routed registration model and AGENTS.md confirmation |
| [Deployment Status](#deployment-status) | Wave 3 stub agent status and implementation timeline |
| [Quick Reference](#quick-reference) | Common workflows and agent selection hints |
| [References](#references) | Full repo-relative paths, requirements traceability, external citations |

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (Stakeholder)** | Product managers, designers, legal/compliance officers | [Purpose](#purpose), [When to Use This Sub-Skill](#when-to-use-this-sub-skill), [Quick Reference](#quick-reference) |
| **L1 (Developer)** | Engineers invoking the agent | [Invoking the Agent](#invoking-the-agent), [Methodology](#methodology), [Output Specification](#output-specification) |
| **L2 (Architect)** | Workflow designers, skill maintainers | [Cross-Framework Integration](#cross-framework-integration), [MCP Dependencies](#mcp-dependencies), [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence) |

---

## Purpose

The Inclusive Design sub-skill provides structured accessibility evaluation using two complementary frameworks: **WCAG 2.2 conformance auditing** (W3C, 2023) and **Microsoft Inclusive Design methodology** (Microsoft, 2016). It targets tiny teams (1-5 people) who need to ensure their products are accessible to the broadest possible range of users while meeting legal compliance requirements (ADA, EAA, Section 508).

This sub-skill is part of Wave 3 (Design System), meaning it requires Wave 2 completion (launched product with analytics OR 1 completed Lean UX hypothesis cycle) before deployment. It pairs with `/ux-atomic-design` in the "Build to Evaluate" canonical sequence: components are built using atomic design principles, then evaluated for accessibility compliance.

### Why Inclusive Design Matters for Tiny Teams

- **Legal compliance** -- The Americans with Disabilities Act (ADA; US DOJ, 2024), European Accessibility Act (EAA, effective June 2025; European Parliament, 2019), and Section 508 (US federal; 29 U.S.C. Section 794d) create legal obligations for digital accessibility. Non-compliance exposes organizations to litigation risk, particularly under Title III ADA case law.
- **Broader user reach** -- Microsoft's Persona Spectrum methodology reveals that designing for permanent disabilities simultaneously benefits users with temporary and situational impairments. Designing for one person with a permanent arm injury also serves someone with a broken arm (temporary) or a parent holding a child (situational). This expands the addressable user base beyond what accessibility compliance alone achieves.
- **Microsoft Inclusive Design principles** -- The methodology operates on three principles: (1) Recognize exclusion -- identify who is being excluded by current design decisions, (2) Solve for one, extend to many -- design for a person in the most constrained scenario and the solution benefits everyone, (3) Learn from diversity -- people with disabilities are experts on adaptation and workarounds that inform better design for all.
- **Cost efficiency** -- Addressing accessibility during design (Wave 3) is significantly less expensive than retrofitting after launch. Teams that evaluate accessibility alongside component design avoid the accumulation of accessibility debt.

### Key Capabilities

- **WCAG 2.2 Compliance Auditing** -- Systematic evaluation against WCAG 2.2 success criteria across four principles (Perceivable, Operable, Understandable, Robust) at conformance levels A, AA, and AAA
- **Persona Spectrum Analysis** -- Application of Microsoft Inclusive Design Persona Spectrum methodology to map permanent, temporary, and situational disability scenarios for each interaction pattern
- **Color Contrast Evaluation** -- Assessment of text and UI component color contrast ratios against WCAG 2.2 success criteria 1.4.3 (AA: 4.5:1 normal text, 3:1 large text) and 1.4.6 (AAA: 7:1 normal text, 4.5:1 large text)
- **Keyboard Navigation Assessment** -- Evaluation of keyboard-only operability including focus order, focus visibility, keyboard traps, and shortcut key conflicts per WCAG 2.2 Operable principle
- **Screen Reader Compatibility Review** -- Assessment of semantic HTML structure, ARIA landmark roles, live region announcements, and alternative text adequacy for assistive technology compatibility
- **Cognitive Load Assessment** -- Evaluation of information density, reading level, consistent navigation patterns, error prevention mechanisms, and input assistance per WCAG 2.2 Understandable principle

> **Source:** Key capabilities derived from parent SKILL.md [skills/user-experience/SKILL.md -- Key Capabilities] ("Inclusive Design Evaluation -- WCAG 2.2 compliance and Microsoft Inclusive Design (Wave 3)") and [skills/user-experience/SKILL.md -- Available Agents] ("Inclusive design and accessibility auditor").

---

## When to Use This Sub-Skill

Activate when:

- Auditing an existing interface or component for WCAG 2.2 conformance at A, AA, or AAA level
- Evaluating color contrast ratios for text, UI components, and graphical objects
- Assessing keyboard navigation completeness and focus management
- Reviewing screen reader compatibility and ARIA implementation
- Performing a Persona Spectrum analysis to map permanent, temporary, and situational disability scenarios
- Evaluating cognitive load and understandability of an interface
- Checking accessibility of components from an atomic design system (Build to Evaluate sequence)
- Responding to "Any stage: Check accessibility" routing from the ux-orchestrator
- Preparing accessibility documentation for legal compliance (ADA, EAA, Section 508)

Do NOT use for:

- Evaluating general usability heuristics beyond accessibility -- use `/ux-heuristic-eval` (Nielsen's 10) instead. Inclusive Design focuses specifically on accessibility; general usability evaluation is a broader scope.
- Building or cataloging a component library -- use `/ux-atomic-design` instead. Inclusive Design evaluates accessibility of components; it does not build the component taxonomy.
- Measuring quantitative UX health metrics -- use `/ux-heart-metrics` (Google GSM) instead. Inclusive Design produces qualitative accessibility findings; HEART Metrics produces ongoing measurement baselines.
- Designing experiments to test design changes -- use `/ux-lean-ux` instead. Inclusive Design evaluates current state; Lean UX tests hypotheses about changes.
- Diagnosing behavioral bottlenecks -- use `/ux-behavior-design` (Fogg B=MAP) instead. Inclusive Design evaluates accessibility barriers; behavior design diagnoses motivation/ability/prompt bottlenecks.
- Security-focused interface review or threat modeling -- use `/eng-team` instead.
- General research without accessibility focus -- use `/problem-solving` instead.

> **Source:** Routing logic derived from [skills/user-experience/SKILL.md -- Lifecycle-Stage Routing] ("Any stage: Check accessibility -> /ux-inclusive-design") and [skills/user-experience/rules/ux-routing-rules.md -- Stage Routing Table], [skills/user-experience/rules/ux-routing-rules.md -- Common Intent Resolution].

---

## Available Agents

| Agent | Role | Tier | Mode | Model | Output Location |
|-------|------|------|------|-------|-----------------|
| `ux-inclusive-evaluator` | Inclusive design and WCAG 2.2 accessibility auditor | T4 | Systematic | Sonnet | `skills/ux-inclusive-design/output/{engagement-id}/ux-inclusive-evaluator-{topic-slug}.md` |

**STUB:** The agent definition file (`skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md`) is planned for creation during Wave 3 implementation of PROJ-022 EPIC-004. The SKILL.md specifies the methodology and output contract that the agent will implement. Agent definition file and governance YAML will contain frontmatter, identity, purpose, guardrails, and full body sections (`<input>`, `<capabilities>`, `<methodology>`, `<output>`).

**Tool tier:** T4 (External) = Read, Write, Edit, Glob, Grep + WebSearch, WebFetch + Context7 MCP. The T4 tier enables access to external WCAG specifications, ARIA authoring practices, and accessibility API documentation via Context7 and web search. Bash is intentionally excluded; T4 tier does not require shell access for MCP operations. See `agent-development-standards.md` [Tool Security Tiers] for full tier definitions.

The agent produces output at three levels per AD-M-004:
- **L0 (Executive Summary):** Conformance level achieved (A, AA, AAA, or none); critical WCAG violations count; Persona Spectrum coverage summary; top remediation priorities for stakeholders and cross-framework synthesis input.
- **L1 (Technical Detail):** Full WCAG 2.2 success criteria evaluation by principle (POUR), per-criterion pass/fail with evidence, Persona Spectrum profiles for each interaction pattern, color contrast ratio measurements, keyboard navigation audit, screen reader compatibility findings, and remediation recommendations with WCAG success criteria references.
- **L2 (Strategic Implications):** Organizational accessibility maturity assessment, legal compliance gap analysis (ADA, EAA, Section 508), accessibility debt quantification, inclusive design adoption roadmap, and cross-product accessibility pattern analysis.

> **Source:** Agent specification from [skills/user-experience/SKILL.md -- Available Agents] and ORCHESTRATION.yaml pipeline-wave3 phase-2 (artifact: `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md`).

---

## P-003 Compliance

The `/ux-inclusive-design` sub-skill contains a single **worker** agent. It is invoked by the `ux-orchestrator` (T5) via the Agent tool. The agent does NOT have Agent tool access and MUST NOT spawn sub-agents.

```
MAIN CONTEXT (user request)
    |
    v
ux-orchestrator (T5, Opus, Integrative) -- parent orchestrator
    |
    +-- ux-inclusive-evaluator (T4, Systematic, Sonnet) -- THIS sub-skill's worker
    +-- [other sub-skill workers...]
```

**Enforcement:**
- `disallowedTools: [Agent]` declared in `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` frontmatter
- P-003 prohibition in `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.governance.yaml` `capabilities.forbidden_actions`
- CI gate validates no sub-skill agent has Agent access (documented in `skills/user-experience/rules/ci-checks.md`)

> **Source:** P-003 hierarchy from parent SKILL.md [P-003 Compliance].

---

## Invoking the Agent

This is a sub-skill invoked by the `ux-orchestrator`, not directly by users. Users interact with the parent `/user-experience` skill, which routes to this sub-skill based on lifecycle-stage triage.

### Via Natural Language (to parent skill)

```
"Audit this page for WCAG 2.2 AA compliance"
"Check the color contrast on our form components"
"Review this interface for screen reader compatibility"
"Map the persona spectrum for our checkout flow"
"Evaluate cognitive load on the settings page"
"Make this accessible"
```

The `ux-orchestrator` routes these requests to `ux-inclusive-evaluator` based on [skills/user-experience/rules/ux-routing-rules.md -- Stage Routing Table]. Specifically, the "Any stage: Check accessibility" route maps directly to `/ux-inclusive-design` without qualification question (source: [skills/user-experience/SKILL.md -- Common Intent-to-Route Resolution]).

### Via Explicit Agent Request (to parent skill)

```
"Use ux-inclusive-evaluator to review color contrast and screen reader compatibility"
"Have ux-inclusive-evaluator perform a WCAG 2.2 AAA audit of the navigation"
```

### Via Agent Tool (orchestrator internal)

The `ux-orchestrator` invokes the agent via the Agent tool:

```python
Agent(
    description="ux-inclusive-evaluator: WCAG 2.2 accessibility audit of checkout flow",
    subagent_type="jerry:ux-inclusive-evaluator",
    prompt="""
## UX CONTEXT (REQUIRED)
- **Engagement ID:** UX-0001
- **Topic:** Checkout Flow Accessibility Audit
- **Product:** [product name and domain]
- **Target Users:** [user description]
- **Target Conformance Level:** AA
- **Input:** [design screenshots, component inventory, markup references]

## TASK
Perform an inclusive design evaluation of the checkout flow.
1. Audit against WCAG 2.2 success criteria at the target conformance level
2. Evaluate color contrast ratios for all text and UI components
3. Assess keyboard navigation and focus management
4. Review screen reader compatibility and ARIA implementation
5. Produce Persona Spectrum analysis mapping permanent, temporary, and situational scenarios
6. Provide remediation recommendations with WCAG success criteria references

## MANDATORY PERSISTENCE (P-002)
Create file at: skills/ux-inclusive-design/output/UX-0001/ux-inclusive-evaluator-checkout-flow.md
"""
)
```

> **Governance codification (AD-M-007):** The session_context contract (on_receive/on_send) is specified in `ux-inclusive-evaluator.governance.yaml` per AD-M-007. Fields are enumerated below:

**on_receive fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `engagement_id` | string | Yes | UX engagement identifier (format: `UX-{NNNN}`) |
| `product_context` | string | Yes | Product name, domain, and target user description |
| `target_conformance_level` | enum | Yes | WCAG conformance target: `A`, `AA`, or `AAA` |
| `component_inventory` | array | No | File paths to component inventory from `/ux-atomic-design` (Storybook references, component taxonomy) |
| `design_artifacts` | array | No | File paths to design screenshots, mockups, or markup (Figma links or image inputs) |
| `upstream_artifacts` | array | No | File paths to upstream handoff artifacts (heuristic eval findings with accessibility subset, atomic design component inventory) |

**on_send fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `conformance_result` | object | Yes | Overall conformance level achieved (A, AA, AAA, or none) with pass/fail per principle (POUR) |
| `wcag_findings` | array | Yes | Per-success-criterion findings with criterion ID, principle, level, pass/fail, evidence, severity, and remediation |
| `persona_spectrum_analysis` | array | Yes | Per-interaction-pattern persona spectrum profiles mapping permanent, temporary, and situational disability scenarios |
| `contrast_ratios` | array | Yes | Color contrast measurements with element reference, foreground/background values, computed ratio, and pass/fail per target level |
| `keyboard_audit` | object | Yes | Keyboard navigation findings: focus order issues, keyboard traps, missing focus indicators, shortcut conflicts |
| `screen_reader_findings` | array | Yes | Screen reader compatibility issues: missing ARIA roles, inadequate alt text, live region problems, heading hierarchy |
| `remediation_priorities` | array | Yes | Prioritized remediation list with WCAG criterion reference, severity, effort estimate, and impact description |
| `synthesis_judgments` | array | Yes | AI judgment calls with confidence classification (HIGH/MEDIUM/LOW) and rationale |

> **Source:** Invocation pattern from parent SKILL.md [Invoking an Agent].

---

## Methodology

### Dual-Framework Approach

The evaluator applies two complementary frameworks in sequence:

1. **WCAG 2.2 Compliance Audit** -- Systematic, criterion-by-criterion evaluation against the W3C Web Content Accessibility Guidelines 2.2 (2023). Produces deterministic pass/fail results per success criterion.
2. **Microsoft Inclusive Design** -- Persona Spectrum analysis that maps each interaction pattern to permanent, temporary, and situational disability scenarios. Produces qualitative insights about who is excluded and how to extend solutions.

The dual-framework approach ensures both compliance coverage (WCAG addresses "what must be met") and design thinking coverage (Inclusive Design addresses "who is being excluded and why").

### WCAG 2.2 Compliance Audit

WCAG 2.2 organizes accessibility requirements into four principles (POUR), each containing guidelines with testable success criteria at three conformance levels (A, AA, AAA).

#### Four Principles (POUR)

| Principle | Letter | Focus | Example Guidelines |
|-----------|--------|-------|-------------------|
| **Perceivable** | P | Information and UI components must be presentable in ways users can perceive | Text alternatives (1.1), time-based media (1.2), adaptable content (1.3), distinguishable presentation (1.4) |
| **Operable** | O | UI components and navigation must be operable by all users | Keyboard accessible (2.1), enough time (2.2), seizure-safe (2.3), navigable (2.4), input modalities (2.5) |
| **Understandable** | U | Information and UI operation must be understandable | Readable (3.1), predictable (3.2), input assistance (3.3) |
| **Robust** | R | Content must be robust enough for reliable interpretation by assistive technologies | Compatible with current and future user agents (4.1) |

#### Conformance Levels

| Level | Scope | Typical Target | Legal Requirement |
|-------|-------|---------------|-------------------|
| **A** | Minimum accessibility -- addresses the most critical barriers | Minimum legal floor in some jurisdictions | ADA (case law baseline) |
| **AA** | Standard compliance target -- removes significant barriers for most users | Most common target for organizations | EAA (explicit requirement), Section 508 (federal), ADA (recommended) |
| **AAA** | Enhanced accessibility -- addresses barriers for specialized user needs | Aspirational; rarely achievable across an entire site | Not typically required by law; recommended for specific content types |

#### Success Criteria Evaluation Format

Each WCAG success criterion is evaluated using the following format:

```
### SC {X.Y.Z}: {Success Criterion Name} [{Level}]

- **Status:** PASS | FAIL | NOT APPLICABLE
- **Evidence:** {specific observation, measurement, or test result}
- **Affected Elements:** {UI element references, selectors, or screen locations}
- **Severity:** 0 (not a problem) | 1 (cosmetic) | 2 (minor barrier) | 3 (major barrier) | 4 (critical -- blocks access)
- **Remediation:** {specific fix with WCAG technique reference, e.g., "Apply ARIA-label per Technique ARIA14"}
```

The severity scale aligns with Nielsen's severity rating scale (Nielsen, 1994b) to enable cross-framework synthesis with `/ux-heuristic-eval` findings. Severity 0 in this sub-skill means "not an accessibility barrier" (equivalent to Nielsen's "not a usability problem" at severity 0); levels 1-4 maintain direct semantic correspondence between the two scales (1=cosmetic/minor, 2=minor barrier, 3=major barrier/usability problem, 4=critical/catastrophe). **Note:** While WCAG pass/fail status is a deterministic compliance check, the severity assignment (0-4) for each finding involves AI judgment about user impact and is classified as MEDIUM synthesis confidence (see [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence)).

### Microsoft Inclusive Design

Microsoft Inclusive Design methodology (Microsoft, 2016) complements WCAG compliance with a design-thinking approach that broadens the understanding of who benefits from accessible design.

#### Three Principles

| Principle | Description | Application |
|-----------|-------------|-------------|
| **Recognize exclusion** | Identify who is being excluded by current design decisions and how | For each interaction pattern, identify users who cannot complete the task due to permanent, temporary, or situational impairments |
| **Solve for one, extend to many** | Design for a person in the most constrained scenario; the solution benefits everyone | Remediation recommendations target the permanent disability scenario; benefits to temporary and situational users are documented |
| **Learn from diversity** | People who adapt to exclusion develop expertise that informs better design | Persona Spectrum profiles include adaptation strategies observed in the disability community |

#### Persona Spectrum Methodology

The Persona Spectrum maps each interaction pattern across three disability duration categories:

| Duration | Definition | Example (Visual) | Example (Motor) | Example (Auditory) | Example (Cognitive) |
|----------|-----------|-------------------|-----------------|--------------------|--------------------|
| **Permanent** | Long-term or lifelong disability | Blind user | Single arm user | Deaf user | Learning disability |
| **Temporary** | Short-term impairment due to injury, surgery, or condition | Post-cataract surgery | Arm in cast | Ear infection | Concussion |
| **Situational** | Context-dependent limitation due to environment or activity | Glare on screen outdoors | Carrying grocery bags | Loud restaurant | Distracted by children |

For each interaction pattern evaluated, the agent produces a Persona Spectrum profile:

```
### Persona Spectrum: {Interaction Pattern Name}

**Interaction:** {description of the user task/action}

| Disability Type | Permanent | Temporary | Situational |
|----------------|-----------|-----------|-------------|
| **Visual** | {scenario} | {scenario} | {scenario} |
| **Motor** | {scenario} | {scenario} | {scenario} |
| **Auditory** | {scenario} | {scenario} | {scenario} |
| **Cognitive** | {scenario} | {scenario} | {scenario} |

**Exclusion Points:** {specific design decisions that create barriers}
**Design Opportunity:** {how solving for permanent extends to all}
**Current Compliance:** {WCAG success criteria relevant to this pattern}
```

### Accessibility Testing Protocols

The evaluator applies the following testing protocols to produce evidence for WCAG findings:

#### Color Contrast Assessment

| Test | Method | Threshold (AA) | Threshold (AAA) | WCAG Criterion |
|------|--------|----------------|-----------------|----------------|
| Normal text contrast | Compute luminance ratio of foreground/background colors | >= 4.5:1 | >= 7:1 | 1.4.3 / 1.4.6 |
| Large text contrast | Large text: >= 18pt or >= 14pt bold | >= 3:1 | >= 4.5:1 | 1.4.3 / 1.4.6 |
| UI component contrast | Non-text UI components and graphical objects | >= 3:1 | >= 3:1 | 1.4.11 |
| Focus indicator contrast | Focus visible indicator against adjacent colors | >= 3:1 | >= 3:1 | 2.4.11 (new in 2.2) |

**Note on programmatic evaluation:** In text-only mode (Figma MCP unavailable), the evaluator cannot compute exact contrast ratios from design artifacts. In this mode, the evaluator documents color values provided by the user and applies the ratio formula, or flags elements where contrast appears insufficient based on visual inspection of screenshots. Exact ratios require hex/RGB values.

#### Keyboard Navigation Audit

| Test | Evaluation Criteria | WCAG Criterion |
|------|-------------------|----------------|
| Tab order completeness | All interactive elements reachable via Tab/Shift+Tab | 2.1.1 (A) |
| Focus visibility | Focus indicator visible on all focused elements | 2.4.7 (AA), 2.4.11 (AA, new in 2.2) |
| No keyboard traps | Focus can be moved away from all components | 2.1.2 (A) |
| Shortcut conflicts | Single character key shortcuts can be turned off or remapped | 2.1.4 (A, new in 2.1) |
| Skip navigation | Skip-to-content mechanism available | 2.4.1 (A) |
| Focus not obscured | Focused element not fully hidden by other content | 2.4.12 (AA, new in 2.2) |

#### Screen Reader Compatibility Review

| Test | Evaluation Criteria | WCAG Criterion |
|------|-------------------|----------------|
| Heading hierarchy | Logical heading structure (h1-h6) without skipped levels | 1.3.1 (A) |
| ARIA landmarks | Main, navigation, banner, contentinfo landmarks present and correct | 1.3.1 (A), 4.1.2 (A) |
| Alternative text | All non-decorative images have descriptive alt text; decorative images use empty alt | 1.1.1 (A) |
| Form labels | All form controls have programmatically associated labels | 1.3.1 (A), 3.3.2 (A) |
| Live regions | Dynamic content updates announced via ARIA live regions | 4.1.3 (AA) |
| Error identification | Error messages programmatically associated with the invalid field | 3.3.1 (A) |

#### Cognitive Load Assessment

| Test | Evaluation Criteria | WCAG Criterion |
|------|-------------------|----------------|
| Reading level | Content appropriate for the target audience's reading level (evaluate via Flesch-Kincaid readability formula where text is available; otherwise AI-assisted reading level assessment -- flag as MEDIUM synthesis confidence per [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence)) | 3.1.5 (AAA) |
| Consistent navigation | Navigation mechanisms consistent across pages/screens | 3.2.3 (AA) |
| Error prevention | Reversible submissions; confirmation for consequential actions | 3.3.4 (AA), 3.3.6 (AAA) |
| Input assistance | Labels, instructions, and suggestions provided for user input | 3.3.2 (A), 3.3.3 (AA) |
| Redundant entry | Information previously entered is auto-populated or selectable | 3.3.7 (A, new in 2.2) |
| Consistent help | Help mechanisms in consistent relative order across pages | 3.2.6 (A, new in 2.2) |

> **Source:** W3C (2023), WCAG 2.2 Recommendation. Microsoft (2016), Inclusive Design Toolkit. Persona Spectrum methodology adapted from Microsoft Inclusive Design Toolkit. Testing protocols derived from [skills/user-experience/SKILL.md -- Key Capabilities] ("Inclusive Design Evaluation -- WCAG 2.2 compliance and Microsoft Inclusive Design").

---

## MCP Dependencies

### Dependency Matrix

| MCP Tool | Classification | Purpose | Fallback |
|----------|---------------|---------|----------|
| **Figma** | **REQ** | Inspect design layers, extract color values for contrast computation, examine component states and responsive behavior, access design token definitions | Screenshot-input mode: user provides design screenshots as image inputs; color values provided manually for contrast computation |
| **Storybook** | ENH | Browse component stories to evaluate accessibility of interactive states, inspect component markup for ARIA implementation | Manual component inventory: user provides component list, markup samples, and documentation links |
| **Context7** | Available (current infrastructure) | Resolve and query WCAG 2.2 success criteria documentation, ARIA Authoring Practices Guide (APG), accessibility API documentation | WebSearch fallback per MCP-001 (`mcp-tool-standards.md` [Error Handling]) |

### Figma Fallback: Screenshot-Input Mode

When the Figma MCP adapter is unavailable (current state -- adapter implementation is post-PROJ-022 scope), the evaluator operates in screenshot-input mode:

- Design evaluation is performed from user-provided screenshot images
- Color contrast ratios require manually provided hex/RGB color values (cannot be extracted programmatically from screenshots)
- Component state evaluation (hover, focus, active, disabled) requires separate screenshots per state
- Responsive behavior assessment requires screenshots at multiple breakpoints
- **Limitations in screenshot-input mode:**
  - Cannot inspect design layers or component hierarchy programmatically
  - Cannot extract exact color values for automated contrast ratio computation
  - Cannot evaluate interactive states (animations, transitions, dynamic content)
  - Cannot access design token definitions or systematic color palette information
- Output carries a degraded mode disclosure per P-022:
  ```
  [DEGRADED MODE] This output was produced without Figma MCP access.
  Input was provided via screenshot-input mode. Some features are reduced:
  - Cannot inspect design layers or component hierarchy programmatically
  - Cannot extract exact color values for automated contrast ratio computation
  - Cannot evaluate interactive states (animations, transitions, dynamic content)
  - Cannot access design token definitions or systematic color palette information
  ```

### Context7 Usage

Per MCP-001 (`.context/rules/mcp-tool-standards.md` [Context7 Integration]), Context7 is used when the evaluation references external accessibility standards, ARIA patterns, or component library documentation by name:

| Library/Framework | Usage |
|-------------------|-------|
| WCAG 2.2 | Success criteria definitions, techniques, sufficient and advisory techniques references |
| ARIA Authoring Practices Guide (APG) | Design pattern implementations for accessible widgets (tabs, dialogs, menus, comboboxes) |
| ARIA specification | Role, state, and property definitions for assistive technology communication |
| Material UI / Radix UI / similar | Component accessibility API documentation for specific design system libraries |

Protocol: call `mcp__context7__resolve-library-id` with the framework name, then `mcp__context7__query-docs` with the resolved ID and specific query. If Context7 returns no results, fall back to WebSearch per `mcp-tool-standards.md` [Error Handling].

> **Source:** MCP dependency matrix from [skills/user-experience/SKILL.md -- MCP Integration Architecture] (`/ux-inclusive-design` row showing Figma REQ, Storybook ENH) and [skills/user-experience/rules/mcp-coordination.md -- MCP Dependency Matrix], [skills/user-experience/rules/mcp-coordination.md -- Degraded Mode Behavior].

---

## Output Specification

### Output Location

```
skills/ux-inclusive-design/output/{engagement-id}/ux-inclusive-evaluator-{topic-slug}.md
```

Where:
- `{engagement-id}` follows the pattern `UX-{NNNN}` (e.g., `UX-0001`)
- `{topic-slug}` is a kebab-case descriptor of the evaluated interface or component (e.g., `checkout-flow`, `form-components`, `navigation-system`)

### Required Output Sections

| Section | Level | Content |
|---------|-------|---------|
| **Executive Summary** | L0 | Conformance level achieved (A/AA/AAA/none); critical violation count by principle; Persona Spectrum coverage summary; top 3-5 remediation priorities for stakeholders and cross-framework synthesis input |
| **Engagement Context** | L1 | Product description, target users, target conformance level, input artifacts (design screenshots, component inventory, markup), MCP status |
| **WCAG 2.2 Compliance Audit** | L1 | Full success criteria evaluation organized by principle (POUR): per-criterion status (PASS/FAIL/N/A), evidence, affected elements, severity (0-4), and remediation with technique references |
| **Color Contrast Analysis** | L1 | Per-element contrast ratio measurements with foreground/background values, computed ratio, target threshold, and pass/fail status |
| **Keyboard Navigation Audit** | L1 | Tab order analysis, focus visibility assessment, keyboard trap detection, shortcut conflict identification |
| **Screen Reader Compatibility** | L1 | Heading hierarchy, ARIA landmark review, alternative text audit, form label association, live region evaluation, error identification |
| **Cognitive Load Assessment** | L1 | Reading level analysis, navigation consistency, error prevention mechanisms, input assistance evaluation |
| **Persona Spectrum Analysis** | L1 | Per-interaction-pattern Persona Spectrum profiles mapping permanent, temporary, and situational disability scenarios with exclusion points and design opportunities |
| **Remediation Priorities** | L1 | Prioritized remediation list with WCAG criterion reference, severity, effort estimate, impact, and design recommendation |
| **Strategic Implications** | L2 | Organizational accessibility maturity assessment, legal compliance gap analysis, accessibility debt quantification, inclusive design adoption roadmap, cross-product patterns |
| **Synthesis Judgments Summary** | L1 | Each AI judgment call listed for synthesis confidence gate compliance (see note below) |
| **Handoff Data** | L1 | Structured data for downstream sub-skills and cross-framework synthesis: WCAG findings with criterion references, Persona Spectrum profiles, conformance result, remediation priorities |

**Synthesis Judgments Summary requirements:** This section MUST list every AI-generated judgment (Persona Spectrum customization, severity assignment, remediation priority ranking, cognitive load assessment) with a confidence classification (HIGH, MEDIUM, LOW) and a one-line rationale. This enables downstream consumers (including the `ux-orchestrator` synthesis gate) to assess which findings are strongly supported versus which require additional validation. The format follows the synthesis judgments pattern established in `skills/user-experience/rules/synthesis-validation.md`.

### Templates

Two templates support the agent's output production:

| Template | Path | Purpose |
|----------|------|---------|
| Persona Spectrum Template | `skills/ux-inclusive-design/templates/persona-spectrum-template.md` [PLANNED: Wave 3 Phase 2] | Microsoft Inclusive Design Persona Spectrum worksheet with permanent/temporary/situational mapping |
| Accessibility Report Template | `skills/ux-inclusive-design/templates/accessibility-report-template.md` [PLANNED: Wave 3 Phase 2] | WCAG 2.2 compliance audit report with per-principle sections and remediation tracking |

> **Source:** Output location from [skills/user-experience/SKILL.md -- Available Agents] and ORCHESTRATION.yaml pipeline-wave3 phase-2 artifacts (persona-spectrum-template.md, accessibility-report-template.md).

---

## Routing

### Trigger Keywords

| Keyword | Routing Context |
|---------|----------------|
| accessibility | Direct match -- primary trigger |
| WCAG | Direct match |
| WCAG 2.2 | Direct match |
| ARIA | Direct match |
| screen reader | Direct match |
| contrast | In combination with UX/design/accessibility context |
| cognitive load | In combination with accessibility context |
| inclusive design | Direct match |
| a11y | Direct match |
| persona spectrum | Direct match |

### Lifecycle-Stage Routing Integration

This sub-skill is routed to by the `ux-orchestrator` in the following lifecycle-stage scenarios:

| Stage | User Intent | Route Condition |
|-------|-------------|-----------------|
| Any stage | "Check accessibility" | No qualification needed -- direct route to `/ux-inclusive-design` per [skills/user-experience/SKILL.md -- Lifecycle-Stage Routing] |
| Any stage | "Make this accessible" | No qualification needed -- routes directly; source: [skills/user-experience/SKILL.md -- Common Intent-to-Route Resolution] |
| During design | "Building component system" | In "Build to Evaluate" sequence: routes to `/ux-atomic-design` first, then `/ux-inclusive-design` for accessibility evaluation of the component inventory |
| Any stage | After `/ux-atomic-design` completion | Canonical sequence continuation: component inventory available as upstream handoff artifact |

### Wave Gating

This sub-skill is in **Wave 3** (Design System). It requires Wave 2 completion before deployment:

**Entry criteria:** Wave 2: launched product with analytics OR 1 completed Lean UX hypothesis cycle.

**Bypass condition:** Storybook already in use (skip Lean UX prerequisite for Atomic Design). Note: this bypass condition is defined for the Wave 3 pair (`/ux-atomic-design` and `/ux-inclusive-design`); the bypass allows teams with an existing component system to proceed to Wave 3 without completing Lean UX cycles.

> **Source:** Routing integration from [skills/user-experience/rules/ux-routing-rules.md -- Stage Routing Table] and [skills/user-experience/SKILL.md -- Lifecycle-Stage Routing]. Wave assignment from [skills/user-experience/SKILL.md -- Wave Architecture].

---

## Cross-Framework Integration

### Upstream Inputs

This sub-skill receives context from other sub-skills when invoked as part of a multi-sub-skill workflow:

| From Sub-Skill | Handoff Artifact | Key Fields | Usage |
|----------------|-----------------|-----------|-------|
| `/ux-atomic-design` | Component inventory with Storybook references | Component taxonomy (atoms, molecules, organisms, templates, pages), Storybook story references, design token definitions | Component inventory provides the evaluation scope for accessibility audit; Storybook references enable component-level accessibility testing; design tokens inform color contrast evaluation |
| `/ux-heuristic-eval` | Severity-rated findings with accessibility subset | Finding ID, heuristic violated (especially H4: Consistency and Standards, H7: Flexibility and Efficiency of Use, H10: Help and Documentation), severity (0-4), affected screen/flow | Heuristic findings related to accessibility (keyboard navigation, error visibility, consistent interface) provide context for targeted WCAG evaluation; severity ratings enable cross-framework convergence detection |

### Downstream Handoffs

This sub-skill produces artifacts that feed into cross-framework synthesis via the Jerry handoff protocol (`docs/schemas/handoff-v2.schema.json`).

| To Sub-Skill/Consumer | Handoff Artifact | Key Fields | Trigger |
|-----------------------|-----------------|-----------|---------|
| `ux-orchestrator` (synthesis) | WCAG findings + Persona Spectrum analysis | Conformance result, WCAG findings with criterion references, persona spectrum profiles, remediation priorities | After audit completion; findings feed cross-framework synthesis for convergence detection with heuristic eval and other sub-skill outputs |
| `/eng-team` (cross-skill) | Accessibility requirements for security integration | WCAG AA violations, ARIA implementation gaps, keyboard trap findings | When engineering team needs accessibility requirements for secure frontend patterns (source: [skills/user-experience/SKILL.md -- Cross-Skill Integration], `/eng-team` integration) |

**Handoff threshold:** Only findings with severity >= 2 (minor barrier or above) are included in cross-framework synthesis handoffs. Severity 0 (not a problem) and severity 1 (cosmetic) findings remain in the full audit report but are excluded from synthesis signal extraction to prevent noise in convergence detection.

### Canonical Multi-Skill Workflow Sequences

This sub-skill participates in the following canonical sequences:

| Sequence | Skills Involved | This Sub-Skill's Role |
|----------|----------------|-----------------------|
| Build to Evaluate | `/ux-atomic-design` then **`/ux-inclusive-design`** | Receives component inventory from Atomic Design; evaluates each component level (atoms through pages) for WCAG compliance and Persona Spectrum coverage |
| Evaluate to Diagnose to Measure | `/ux-heuristic-eval` then **`/ux-inclusive-design`** (accessibility subset) then `/ux-behavior-design` | Heuristic eval identifies accessibility-related findings; inclusive design provides detailed WCAG audit for those areas; behavior design diagnoses why accessibility barriers cause user drop-off |

> **Source:** Handoff data contracts from [skills/user-experience/rules/ux-routing-rules.md -- Handoff Data Contracts] and [skills/user-experience/SKILL.md -- Cross-Sub-Skill Handoff Data] ("/ux-atomic-design -> /ux-inclusive-design: Component inventory with Storybook references"). Canonical sequences from [skills/user-experience/SKILL.md -- Canonical Multi-Skill Workflow Sequences] ("Build to Evaluate: /ux-atomic-design then /ux-inclusive-design").

---

## Synthesis Hypothesis Confidence

Inclusive Design outputs include synthesis hypotheses that carry confidence classifications per the synthesis validation protocol.

| Synthesis Step | Typical Confidence | Rationale |
|---------------|-------------------|-----------|
| Persona Spectrum customization | MEDIUM | Persona Spectrums are heuristic models (Microsoft, 2016), not empirical profiles; the mapping of permanent/temporary/situational scenarios involves AI judgment about plausible user contexts rather than observed user data |
| Severity assignment (0-4 scale) | MEDIUM | Severity ratings involve AI interpretation of user impact against the Nielsen severity scale (Nielsen, 1994b); while WCAG pass/fail is deterministic, mapping a failure to a 0-4 severity level requires judgment about how much the barrier impedes real user tasks -- no objective algorithm exists for this mapping |
| Remediation priority ranking | MEDIUM | Prioritization requires AI judgment about relative user impact severity, affected population size, and estimated implementation effort (W3C, 2023; Microsoft, 2016); these factors are context-dependent and cannot be deterministically computed from WCAG criteria alone |
| Cognitive load assessment | MEDIUM | Reading level evaluation and information density assessments are heuristic (Nielsen, 1994b); readability formulas provide approximate guidance but the determination of whether content is "appropriate for the target audience" (WCAG 3.1.5) requires AI judgment about audience characteristics |

**Gate enforcement:**
- **MEDIUM outputs:** Include a "Validation Required" section. Design recommendations derived from Persona Spectrum analysis, severity assignments, remediation priority rankings, and cognitive load assessments are withheld until validation against real user observation, assistive technology user testing, or accessibility expert review is provided. Persona Spectrum profiles serve as structured hypotheses about who is excluded, not as validated user research findings. Severity and priority assignments serve as structured triage guidance, not as definitive impact measurements.

**Note on WCAG findings confidence:** WCAG 2.2 success criteria evaluations (pass/fail per criterion) do not go through the synthesis hypothesis confidence gate because they are deterministic compliance checks, not AI-generated abstractions. A WCAG criterion either passes or fails based on measurable criteria (W3C, 2023). However, the severity assignment (0-4) for each finding involves AI judgment and is classified as MEDIUM confidence in the table above. Persona Spectrum analysis, by contrast, is inherently interpretive and always receives MEDIUM confidence.

**Confidence upgrade path:** Persona Spectrum customization, severity assignment, and remediation priority confidence can increase to HIGH only through convergence with a second framework in cross-framework synthesis (per `skills/user-experience/rules/synthesis-validation.md` [Convergence Thresholds]: moderate convergence = 2 frameworks identifying the same problem with supporting evidence = HIGH). For example, if Persona Spectrum analysis identifies "situational visual impairment: glare on screen outdoors" as an exclusion point AND Heuristic Eval independently identifies low contrast as a severity-3 finding for the same component, the convergent finding receives HIGH synthesis confidence. Similarly, severity and priority assignments that align with quantitative HEART Metrics data (e.g., low Task Success rate confirms a severity-4 barrier) receive HIGH confidence through cross-framework corroboration.

> **Source:** Confidence classifications from [skills/user-experience/rules/synthesis-validation.md § Sub-Skill Synthesis Output Map] ("`/ux-inclusive-design` Persona Spectrum customization MEDIUM"). Gate enforcement from [skills/user-experience/SKILL.md § Synthesis Hypothesis Validation]. Severity scale from Nielsen (1994b). Convergence upgrade thresholds from [skills/user-experience/rules/synthesis-validation.md § Convergence Thresholds] ("Moderate convergence: 2 frameworks identify the same UX problem with supporting evidence = HIGH").

---

## Constitutional Compliance

All agents in this sub-skill adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- worker agent, no Agent tool access | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user decisions on target conformance level or remediation priority | Unauthorized action; trust erosion |
| P-022 | NEVER present WCAG pass/fail status without evidence; NEVER inflate conformance claims without criterion-level verification | Governance undermined; legal compliance assessment invalidated |
| P-001 | NEVER present accessibility findings without WCAG success criteria references or Persona Spectrum evidence | Unreliable outputs; unfounded compliance claims propagate downstream |
| P-002 | NEVER leave accessibility audit results or persona spectrum analyses in transient context only -- persist to files | Context rot vulnerability; artifacts lost on session compaction |

**Per-agent enforcement:** The `ux-inclusive-evaluator` agent declares:
- `constitution.principles_applied`: P-003, P-020, P-022, P-001, P-002 in `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.governance.yaml`
- `capabilities.forbidden_actions`: 3 entries in NPT-009 format referencing the constitutional triplet
- `disallowedTools: [Agent]` in `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` frontmatter

### AI-Augmented Analysis Limitations

The Inclusive Design evaluator agent operates as an AI-augmented analysis tool. The following limitations apply to all outputs and MUST be disclosed per P-022 (no deception):

- **WCAG evaluation is best-effort from available artifacts.** Full WCAG compliance testing requires manual testing with assistive technologies (screen readers, switch devices, voice control), automated testing tools (axe-core, Lighthouse, WAVE), and user testing with people who have disabilities. AI-based evaluation from design artifacts or screenshots provides a structured initial audit but does not replace comprehensive accessibility testing.
- **Persona Spectrum profiles are heuristic models.** The mapping of permanent, temporary, and situational disability scenarios is based on the Microsoft Inclusive Design Toolkit methodology and general knowledge of disability contexts. Real Persona Spectrums should be informed by interviews with people who have disabilities and observation of actual assistive technology usage.
- **Color contrast ratios are input-dependent.** In screenshot-input mode (Figma MCP unavailable), exact contrast ratios require user-provided hex/RGB values. Visual estimation from screenshots is not precise enough for compliance determination.
- **Screen reader compatibility is structural, not experiential.** The evaluator assesses semantic HTML structure and ARIA implementation from markup or descriptions, but cannot simulate the actual screen reader experience across different assistive technology combinations (JAWS, NVDA, VoiceOver with different browsers).
- **Always validate with real assistive technology users.** Accessibility audit outputs should be confirmed through manual testing with assistive technologies and, where possible, user testing with people who have disabilities before making compliance claims.

---

## Registration

This sub-skill follows a parent-routed registration model. Sub-skills are not independently registered in `CLAUDE.md` or `mandatory-skill-usage.md` because they are routed through the parent `/user-experience` orchestrator (`ux-orchestrator`). This is an explicit exception to the H-26 registration requirement (parent-routed model): parent skills own the CLAUDE.md and mandatory-skill-usage.md registration; sub-skills are discovered and dispatched by the parent orchestrator's internal routing logic.

| Registration Point | Status | Detail |
|--------------------|--------|--------|
| `CLAUDE.md` skill table | Registered via parent | `/user-experience` is registered in `CLAUDE.md`; sub-skills are not independently listed |
| `mandatory-skill-usage.md` trigger map | Routed via parent | The `/user-experience` trigger map row includes "accessibility" and "inclusive design" as positive keywords (H-22); requests matching these keywords route to the parent skill, which dispatches to this sub-skill |
| `AGENTS.md` agent registry | Registered | `ux-inclusive-evaluator` is listed in `AGENTS.md` under the User-Experience Skill Agents section |
| Parent SKILL.md agent table | Registered | `ux-inclusive-evaluator` is listed in `skills/user-experience/SKILL.md` [Available Agents] |

> **H-26 parent-routed model rationale:** Independent registration of sub-skills would create duplicate trigger map entries and ambiguous routing (AP-02 Bag of Triggers). The parent orchestrator owns lifecycle-stage routing logic and dispatches to the correct sub-skill based on triage qualification, not keyword matching alone. Sub-skill agents are registered in `AGENTS.md` for discoverability but routing flows through the parent.

---

## Deployment Status

> **Wave 3 Sub-Skill -- Planned.** This sub-skill is part of Wave 3 (Design System) of PROJ-022. The companion agent file (`skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md`) and governance file (`skills/ux-inclusive-design/agents/ux-inclusive-evaluator.governance.yaml`) are planned for creation during Wave 3 implementation of PROJ-022 EPIC-004. The SKILL.md itself is complete and specifies the methodology, output format, and routing integration that the agent will implement.

---

## Quick Reference

### Common Workflows

| Need | Command Example |
|------|-----------------|
| WCAG 2.2 AA compliance audit | "Audit this page for WCAG 2.2 AA compliance" |
| Color contrast check | "Check the color contrast on our form components" |
| Screen reader compatibility | "Review this interface for screen reader compatibility" |
| Persona Spectrum analysis | "Map the persona spectrum for our checkout flow" |
| Keyboard navigation audit | "Evaluate keyboard navigation on the settings page" |
| Cognitive load assessment | "Assess cognitive load on the onboarding flow" |
| Component accessibility | "Evaluate accessibility of our atomic design components" |
| Legal compliance review | "Review our product for EAA accessibility requirements" |

### Agent Selection Hints

| Keywords | Routes To |
|----------|-----------|
| accessibility, WCAG, ARIA, screen reader, contrast, cognitive load, inclusive, a11y, persona spectrum | `ux-inclusive-evaluator` |
| heuristic, usability, Nielsen, severity, inspection, evaluation | `/ux-heuristic-eval` (not this sub-skill) |
| atomic design, atoms, molecules, organisms, components, design tokens, Storybook | `/ux-atomic-design` (not this sub-skill) |
| HEART, metrics, measurement, GSM, happiness, engagement | `/ux-heart-metrics` (not this sub-skill) |
| lean UX, hypothesis, experiment, build-measure-learn | `/ux-lean-ux` (not this sub-skill) |
| behavior, Fogg, B=MAP, motivation, ability, prompt | `/ux-behavior-design` (not this sub-skill) |

---

## References

| Source | Content | Path |
|--------|---------|------|
| Parent SKILL.md | Sub-skill scope, wave architecture, routing, MCP dependencies, synthesis protocol | `skills/user-experience/SKILL.md` |
| Agent definition | Agent frontmatter, identity, expertise, guardrails | `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` [PLANNED: Wave 3] |
| Agent governance | Tool tier, forbidden actions, output validation, constitutional compliance | `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.governance.yaml` [PLANNED: Wave 3] |
| UX routing rules | Lifecycle-stage routing, handoff data contracts, common intent resolution | `skills/user-experience/rules/ux-routing-rules.md` |
| MCP coordination | Figma REQ dependency, degraded mode behavior, Context7 usage | `skills/user-experience/rules/mcp-coordination.md` |
| Synthesis validation | Confidence gate protocol, per-sub-skill confidence map | `skills/user-experience/rules/synthesis-validation.md` |
| Wave progression | Wave 3 entry criteria, signoff requirements | `skills/user-experience/rules/wave-progression.md` |
| CI checks | P-003 enforcement, sub-skill validation gates | `skills/user-experience/rules/ci-checks.md` |
| Inclusive design methodology rules | WCAG evaluation rules, Persona Spectrum methodology rules | `skills/ux-inclusive-design/rules/inclusive-design-methodology-rules.md` [PLANNED: Wave 3 Phase 2] |
| MCP runbook | Figma integration operational procedures for accessibility evaluation | `skills/ux-inclusive-design/rules/mcp-runbook.md` [PLANNED: Wave 3 Phase 2] |
| Persona Spectrum template | Microsoft Inclusive Design Persona Spectrum worksheet | `skills/ux-inclusive-design/templates/persona-spectrum-template.md` [PLANNED: Wave 3 Phase 2] |
| Accessibility report template | WCAG 2.2 compliance audit report template | `skills/ux-inclusive-design/templates/accessibility-report-template.md` [PLANNED: Wave 3 Phase 2] |
| Skill standards | H-25/H-26 skill structure requirements | `.context/rules/skill-standards.md` |
| Agent development standards | H-34 dual-file architecture, tool tiers, handoff protocol | `.context/rules/agent-development-standards.md` |
| Quality enforcement | Quality gate thresholds, criticality levels, strategy catalog | `.context/rules/quality-enforcement.md` |
| Handoff schema | Canonical handoff schema v2 | `docs/schemas/handoff-v2.schema.json` |
| Agent governance schema | Governance YAML validation schema | `docs/schemas/agent-governance-v1.schema.json` |

### Requirements Traceability

| Source | Content | Path |
|--------|---------|------|
| PROJ-022 PLAN.md | Project plan: sub-skill scope, wave assignment, acceptance criteria, implementation phases | `projects/PROJ-022-user-experience-skill/PLAN.md` |
| EPIC-004 (Wave 3 Deployment) | Parent work item for Wave 3 sub-skill implementation including this sub-skill | PROJ-022 EPIC-004 in `projects/PROJ-022-user-experience-skill/WORKTRACKER.md` |
| ORCHESTRATION.yaml | Orchestration plan governing the build sequence for this sub-skill | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |

### External References

| Source | Citation |
|--------|----------|
| W3C (2023) | Web Content Accessibility Guidelines (WCAG) 2.2. W3C Recommendation. 2023-10-05. |
| W3C (2023b) | ARIA Authoring Practices Guide (APG). W3C Working Group Note. |
| Microsoft (2016) | Microsoft Inclusive Design Toolkit. Persona Spectrum methodology. microsoft.com/design/inclusive. |
| Nielsen, 1994b | Nielsen, J. (1994). "Severity Ratings for Usability Problems." Nielsen Norman Group. Severity scale: 0 (not a problem) to 4 (usability catastrophe). |
| US DOJ (2024) | "Guidance on Web Accessibility and the ADA." U.S. Department of Justice, Civil Rights Division. |
| European Parliament (2019) | Directive (EU) 2019/882 -- European Accessibility Act (EAA). Effective June 2025. |
| Section 508 | Section 508 of the Rehabilitation Act (29 U.S.C. 794d). ICT accessibility standards for US federal agencies. |

---

*Sub-Skill Version: 1.1.0*
*Parent Skill: `/user-experience` v1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Wave: 3 (Design System)*
*SSOT: `skills/user-experience/SKILL.md`*
*Project: PROJ-022 User Experience Skill*
*Created: 2026-03-04*
*Revised: 2026-03-04 (iter2 quality gate)*
