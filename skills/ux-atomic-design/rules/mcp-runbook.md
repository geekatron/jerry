<!-- VERSION: 1.1.0 | DATE: 2026-03-04 | SOURCE: skills/user-experience/rules/mcp-coordination.md (v1.2.0), skills/ux-atomic-design/SKILL.md (v1.2.0) | PARENT: /ux-atomic-design sub-skill | GOVERNANCE: .context/rules/mcp-tool-standards.md (MCP-001) | PROJECT: projects/PROJ-022-user-experience-skill/PLAN.md | REVISION: iter2 — add Phase 1-5 workflow timing map, timeout rationale, self-review checklist, quality gate integration, citation example, Library ID table reframing, version annotations -->

# MCP Runbook -- Atomic Design Sub-Skill

> Operational MCP usage runbook for `/ux-atomic-design`. Defines Context7 integration for component library documentation lookup (Material UI, Radix, Shadcn/ui, Storybook, Tailwind CSS, Chakra UI), Storybook REQ dependency with Manual Component Inventory Mode fallback, and failure handling. Operationalizes the parent `skills/user-experience/rules/mcp-coordination.md` rules for the Atomic Design component taxonomy domain.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context7 Usage for Atomic Design](#context7-usage-for-atomic-design) | When and how to use Context7 during taxonomy construction |
| [Library ID Resolution Table](#library-id-resolution-table) | Library name to Context7 ID mapping |
| [Query Patterns](#query-patterns) | Common Context7 query patterns for component library tasks |
| [Storybook MCP Dependency](#storybook-mcp-dependency) | Current status, fallback mode, future adapter |
| [Manual Component Inventory Mode Protocol](#manual-component-inventory-mode-protocol) | How to produce structured outputs when Storybook is unavailable |
| [MCP Failure Handling](#mcp-failure-handling) | Fallback paths for Context7 and full MCP outage |
| [Tool Usage Constraints](#tool-usage-constraints) | T3 tier boundary, citation requirements |
| [Quality Gate Integration](#quality-gate-integration) | How MCP-related outputs map to S-014 rubric dimensions |
| [Self-Review Checklist](#self-review-checklist) | S-010 verification for MCP compliance before output persistence |
| [References](#references) | Source document traceability |

---

## Context7 Usage for Atomic Design

Per MCP-001 (`.context/rules/mcp-tool-standards.md` v1.3.1 [Context7 Integration]): Context7 MUST be used when the taxonomy construction references an external component library, design system framework, or design token system by name. The `ux-atomic-architect` agent is T3 (External) and has `mcp__context7__resolve-library-id` and `mcp__context7__query-docs` in its allowed tools.

**Operational state:** Context7 queries are available NOW for component library documentation research (Material UI component API, Radix primitive patterns, Shadcn/ui implementation patterns, Storybook story format, Tailwind utility classes, Chakra UI theme tokens). The protocol defined in this runbook governs the agent in both current and post-Wave-3-deployment states. Post-deployment with Storybook MCP, Context7 additionally supports cross-referencing live story inspection results against component library documentation.

**Note:** The parent `mcp-coordination.md` [Context7 Usage] agent table lists `ux-atomic-architect` as a Context7-enabled agent. The authoritative tool declaration is in the agent definition frontmatter (`skills/ux-atomic-design/agents/ux-atomic-architect.md`).

### Protocol

1. Call `mcp__context7__resolve-library-id` with the library/framework name and the research question.
2. Call `mcp__context7__query-docs` with the resolved library ID and a specific query.
3. Respect the per-question call limit enforced by the tool; each distinct library resets the limit.
4. If `resolve-library-id` returns no matches, fall back to WebSearch for that library.

### When to Use Context7 During Taxonomy Construction

| Construction Phase | Context7 Trigger | Example Query |
|-------------------|-----------------|---------------|
| Phase 1: Scope Definition | Identifying the component library or design system framework used by the product | `resolve: "Material UI"` then `query: "component list available MUI components"` |
| Phase 2: Component Inventory | Looking up component API to determine atom vs. molecule classification | `resolve: "Radix UI"` then `query: "primitive component composition patterns select dialog"` |
| Phase 2: Component Inventory | Checking component variant documentation for variant count | `resolve: "Shadcn/ui"` then `query: "button variants size color style props"` |
| Phase 3: Design Token Audit | Querying design token architecture for a specific framework | `resolve: "Tailwind CSS"` then `query: "design tokens theme configuration colors spacing typography"` |
| Phase 3: Design Token Audit | Looking up theming API for token consistency comparison | `resolve: "Material UI"` then `query: "theme customization design tokens palette typography spacing"` |
| Phase 4: Storybook Coverage | Querying Storybook story format documentation for coverage assessment | `resolve: "Storybook"` then `query: "story format CSF3 component story file structure args"` |
| Phase 4: Storybook Coverage | Looking up Storybook addon configuration for coverage reporting | `resolve: "Storybook"` then `query: "coverage addon test-runner component coverage reporting"` |
| Phase 5: Synthesis | Cross-referencing component patterns against library documentation for consolidation assessment | `resolve: "Chakra UI"` then `query: "component API style props theme tokens composition"` |

### When NOT to Use Context7

| Scenario | Alternative |
|----------|-------------|
| General Atomic Design methodology concepts already in architect knowledge (Frost 2016) | No tool call needed |
| Codebase-internal component file inspection | Read/Grep the codebase |
| Prior engagement outputs or upstream heuristic evaluation findings | Read the engagement output files |
| Context7 already queried for the same library in this engagement | Reuse prior results from the current context window or from the engagement output file where prior query results were captured; do not re-query if the result is already available. Respect call limit. |
| General design system concepts not tied to a specific library | WebSearch |

### When to Query Context7 in the 5-Phase Workflow

This table maps each SKILL.md workflow phase to its Context7 usage, using the canonical Phase 1-5 numbering. Phases where Context7 is not needed are explicitly marked with rationale.

| Phase | SKILL.md Phase Name | Context7 Action | Rationale |
|-------|---------------------|----------------|-----------|
| **Phase 1** | Scope Definition | Resolve library IDs for the product's component library and design system framework | The architect needs to know which libraries are in use before constructing the inventory; Context7 identifies available documentation |
| **Phase 2** | Component Inventory | Query component APIs, composition patterns, variant props, and state documentation | Classification requires understanding component structure; Context7 provides authoritative API references for atom/molecule/organism determination |
| **Phase 3** | Design Token Audit | Query design token architecture, theme configuration, and utility class mappings | Token audit requires knowledge of the framework's token system structure; Context7 provides current token documentation |
| **Phase 4** | Storybook Coverage | Query Storybook story format (CSF3), coverage addons, and test-runner configuration | Coverage assessment requires understanding Storybook's documentation format and coverage reporting APIs |
| **Phase 5** | Synthesis | **No Context7 needed.** Synthesis aggregates findings from Phases 1-4 using existing engagement data. | Phase 5 operates on the architect's own findings; no external library documentation is required. Exception: cross-referencing a specific component pattern against library documentation for consolidation assessment may trigger a targeted query. |

> **Call limit note:** The Context7 per-question call limit resets per distinct library. A 5-phase engagement typically queries 2-4 libraries (component library + design token framework + Storybook + optional secondary library). Plan queries to resolve all libraries in Phase 1 and distribute remaining queries across Phases 2-4 within the per-library limit.

---

## Library ID Resolution Table

This table maps commonly referenced component libraries to their Context7 reference patterns. Context7 library IDs are resolved dynamically via `mcp__context7__resolve-library-id`; this table provides reference patterns for expected resolutions, not canonical IDs.

> **Verification note:** Library IDs reflect expected patterns as of 2026-03-04. Dynamic verification via `resolve-library-id` is required at execution time; actual IDs may differ from these reference patterns.

| Library Name | Resolve Query | Reference Usage (verify via resolve-library-id) | Fallback |
|-------------|---------------|----------------|----------|
| **Material UI (MUI)** | `"Material UI"` or `"MUI"` | Component patterns, theming API, design tokens | WebSearch: `"MUI component API" site:mui.com` |
| **Radix UI** | `"Radix UI"` or `"Radix"` | Accessible component API, composition patterns, primitive components | WebSearch: `"Radix UI primitives" site:radix-ui.com` |
| **Shadcn/ui** | `"Shadcn"` or `"shadcn/ui"` | Component implementation patterns, Tailwind token integration | WebSearch: `"shadcn/ui components" site:ui.shadcn.com` |
| **Storybook** | `"Storybook"` | Story format (CSF3), addon configuration, coverage reporting APIs | WebSearch: `"Storybook documentation" site:storybook.js.org` |
| **Tailwind CSS** | `"Tailwind CSS"` or `"Tailwind"` | Utility class taxonomy, design token mapping, responsive breakpoints | WebSearch: `"Tailwind CSS theme configuration" site:tailwindcss.com` |
| **Chakra UI** | `"Chakra UI"` or `"Chakra"` | Component API, style props, theme tokens | WebSearch: `"Chakra UI components" site:chakra-ui.com` |

> **Note:** Context7 library IDs may change as the library index is updated. Always use `resolve-library-id` for dynamic resolution rather than hardcoding IDs. The table above provides expected resolution patterns and WebSearch fallback queries per MCP-001.

---

## Query Patterns

Common Context7 query patterns organized by task type. These patterns provide the architect with repeatable query structures for frequent lookup needs during the 5-phase workflow.

> **Note:** Query patterns are representative examples; actual query precision may vary based on Context7 index content and library documentation coverage. Adjust query wording based on Context7 response quality -- if a query returns irrelevant results, refine with more specific terms or fall back to WebSearch.

### Component API Lookup

| Task | Library | Query Pattern |
|------|---------|---------------|
| List available components | Material UI | `"list of MUI components available categories"` |
| Check component props/API | Radix UI | `"{component name} props API composition children"` |
| Check component variants | Shadcn/ui | `"{component name} variants props className styling"` |
| Check component states | Any | `"{component name} states disabled loading error hover active"` |
| Check composition patterns | Radix UI | `"{component name} composition sub-components compound"` |

### Design Token Documentation

| Task | Library | Query Pattern |
|------|---------|---------------|
| Theme token structure | Material UI | `"theme customization createTheme palette typography spacing"` |
| Utility class mapping | Tailwind CSS | `"theme extend colors spacing fontSize configuration"` |
| Style props system | Chakra UI | `"style props theme tokens color space fontSize"` |
| CSS variable tokens | Radix UI | `"CSS custom properties tokens theme colors"` |
| Design token format | Tailwind CSS | `"design tokens tailwind config theme object structure"` |

### Storybook and Testing Patterns

| Task | Library | Query Pattern |
|------|---------|---------------|
| Story file format | Storybook | `"component story format CSF3 meta args render"` |
| Coverage setup | Storybook | `"test-runner coverage addon jest component testing"` |
| Interaction testing | Storybook | `"play function interaction testing user-event"` |
| Visual testing | Storybook | `"visual regression testing chromatic snapshot"` |
| Args and controls | Storybook | `"args argTypes controls component props documentation"` |

---

## Storybook MCP Dependency

### Current Status

**Storybook MCP adapter: UNAVAILABLE.** Adapter implementation is post-PROJ-022 scope (see `projects/PROJ-022-user-experience-skill/PLAN.md` [Context]). The `/ux-atomic-design` sub-skill has Storybook classified as **REQ** in the parent MCP dependency matrix (`skills/user-experience/rules/mcp-coordination.md` [MCP Dependency Matrix]).

### Fallback Mode

The sub-skill operates in **Manual Component Inventory Mode** when Storybook is unavailable. The taxonomy construction methodology remains identical; only the input modality changes. See [Manual Component Inventory Mode Protocol](#manual-component-inventory-mode-protocol) for operational details.

### What Changes When Storybook Becomes Available

When the Storybook MCP adapter is implemented and the orchestrator's MCP availability detection succeeds (probe protocol defined in `skills/user-experience/rules/mcp-coordination.md` [MCP Availability Detection]):

| Capability | Manual Component Inventory Mode (current) | Storybook MCP Mode (future) |
|------------|-------------------------------------------|----------------------------|
| Component discovery | User provides component list, screenshots, documentation | Programmatic browsing of live component stories |
| Variant enumeration | User describes variants textually | Automated extraction of args/controls from story definitions |
| State inspection | User lists known states; architect infers from descriptions | Programmatic inspection of story states (default, hover, disabled, error, loading) |
| Token usage verification | Text-based analysis of available documentation | Programmatic inspection of component style declarations and token references |
| Coverage calculation | Based on user-reported data; accuracy depends on inventory completeness | Automated: total stories / total components per hierarchy level |
| Composition verification | Manual cross-referencing of component descriptions | Programmatic analysis of component imports and composition trees |

The agent definition frontmatter and governance file will need updating when Storybook MCP becomes available to add Storybook MCP tools and update the tool tier if necessary.

---

## Manual Component Inventory Mode Protocol

This section defines how the `ux-atomic-architect` agent produces outputs when the Storybook MCP adapter is unavailable (current default).

### P-022 Degraded Mode Disclosure

The following banner MUST appear at the top of the architect's output when operating in Manual Component Inventory Mode:

```
[DEGRADED MODE] This output was produced without Storybook MCP access.
Input was provided via manual component inventory mode. Some features are reduced:
- Cannot browse or validate live component stories
- Cannot inspect component variants, states, or props interactively
- Cannot verify design token usage in component implementations
- Coverage assessment accuracy depends on user-provided inventory completeness
```

This banner MUST be included regardless of whether the user explicitly acknowledges the degraded mode. The disclosure is a P-022 (no deception) requirement, not a user preference.

### Structured Markdown Equivalents

When Storybook is unavailable, all component inspection outputs are produced from user-provided inputs:

| Storybook Capability | Manual Equivalent | Format |
|---------------------|-------------------|--------|
| Component story browsing | User-provided component list with descriptions | Markdown table: Component Name, Description, Variant Count (estimated), States (listed) |
| Variant inspection | User describes variants textually or provides screenshots | Markdown table: Component Name, Variant Name, Visual Description |
| State inspection | User lists known states; architect catalogs from descriptions | Markdown table: Component Name, States Documented (comma-separated) |
| Token usage verification | User provides design token documentation; architect cross-references | Markdown table: Component Name, Token Category, Token Used / Hardcoded Value |
| Coverage calculation | Architect calculates from the user-provided inventory as denominator | Coverage percentage with disclaimer about inventory completeness |
| Composition analysis | Architect infers composition from component descriptions and screenshots | Composition tree documented in text format with explicit inference markers |

### Limitations of Manual Component Inventory Mode

| Artifact Type | Limitation | Impact on Output Quality |
|---------------|-----------|--------------------------|
| Component Inventory | Cannot programmatically discover components; relies on user-provided list | HIGH: missing components not in the user's list will not appear in the inventory |
| Variant Count | Cannot extract variant count from story definitions; relies on user estimate | MEDIUM: variant counts may be approximate; exhaustive enumeration not possible |
| State Coverage | Cannot inspect component rendered states; relies on user-listed states | MEDIUM: states not listed by user will not be assessed for coverage |
| Design Token Audit | Cannot inspect CSS/style declarations programmatically; relies on documentation | HIGH: drift ratio accuracy limited by documentation completeness; hardcoded values in implementations may go undetected |
| Storybook Coverage | Cannot count stories programmatically; coverage based on user-reported data | HIGH: coverage percentages may be artificially inflated if user inventory is incomplete |
| Composition Verification | Cannot trace component import trees; relies on description-based inference | MEDIUM: composition rules inferred from descriptions; may miss non-obvious compositions |

> **Impact rating attribution:** Impact ratings defined as: HIGH = core analysis capability depends on user-provided data completeness; MEDIUM = information available but accuracy reduced; LOW = minimal impact. These are editorial assessments specific to manual inventory mode. P-022 disclosure: ratings reflect architect judgment about mode limitations.

---

## MCP Failure Handling

### Context7 Unavailable

Per `mcp-tool-standards.md` v1.3.1 [Error Handling]:

| Failure Condition | Fallback Action |
|-------------------|----------------|
| `resolve-library-id` returns no matches | Fall back to WebSearch for that library using the fallback query from the [Library ID Resolution Table](#library-id-resolution-table). Note "Context7 no coverage" in the output next to the affected finding. |
| `query-docs` returns empty or irrelevant results | Use WebSearch for the specific query. Note "Context7 no coverage" in the output. |
| Context7 tool-enforced call limit reached | Fall back to WebSearch for remaining queries for that library. |
| Context7 MCP server timeout (> 5 seconds with no response) or error | Continue taxonomy construction without Context7. Use WebSearch for all external documentation lookups. Note the MCP outage in the report metadata. One retry attempted before declaring unavailable, per `mcp-coordination.md` [MCP Availability Detection] detection protocol. Retry interval: immediate (no delay between first attempt and retry). *(5-second timeout rationale: operational heuristic -- MCP tool calls typically complete in < 2 seconds under normal network conditions; 5 seconds provides a 2.5x buffer for network latency spikes while preventing indefinite blocking that would stall the taxonomy construction workflow. Adjust based on observed MCP response times in the deployment environment.)* |

### Full MCP Server Outage

When the MCP server is completely unavailable (detected by the orchestrator's probe protocol per `skills/user-experience/rules/mcp-coordination.md` [MCP Availability Detection]):

1. **Continue taxonomy construction.** The Atomic Design methodology does not depend on MCP for core functionality. Component classification, composition rules, and hierarchy construction are applied from the architect's built-in knowledge of Frost's methodology.
2. **Use WebSearch as fallback** for any external documentation lookups (component library APIs, design token documentation, Storybook configuration patterns).
3. **Disclose in output** per P-022: note that MCP tools were unavailable and external references were sourced via web search.
4. **No blocking.** MCP outage does not block taxonomy construction. The architect proceeds with reduced reference precision but identical methodology.

### Storybook Unavailable (Current Default)

Since the Storybook MCP adapter is not yet implemented, the Storybook-unavailable state is the current default. No dynamic detection is needed; the architect always operates in Manual Component Inventory Mode.

When the Storybook MCP adapter becomes available in the future and subsequently fails:

1. **Detect failure** via the orchestrator's Storybook probe (defined in `mcp-coordination.md` [Future MCP Probes]).
2. **Fall back to Manual Component Inventory Mode** per [Manual Component Inventory Mode Protocol](#manual-component-inventory-mode-protocol).
3. **Disclose degraded mode** per P-022 using the banner defined in [P-022 Degraded Mode Disclosure](#p-022-degraded-mode-disclosure).
4. **No blocking.** Storybook outage does not block taxonomy construction. Component inventories are produced from user-provided inputs.

---

## Tool Usage Constraints

### Tool Tier

The `ux-atomic-architect` agent operates at **T3 (External)** per `agent-development-standards.md` v1.2.0 [Tool Security Tiers]. This tier includes:

- **T1 (Read-Only):** Read, Glob, Grep
- **T2 (Read-Write):** T1 + Write, Edit
- **T3 (External):** T2 + WebSearch, WebFetch, Context7 (`mcp__context7__resolve-library-id`, `mcp__context7__query-docs`)

> **Note:** The tier breakdown above reflects the T3 tier model from `agent-development-standards.md` v1.2.0 [Tool Security Tiers]. The `ux-atomic-architect` agent excludes Bash from its actual tool set -- Bash is not required for component taxonomy construction and is omitted from the agent definition frontmatter (`skills/ux-atomic-design/agents/ux-atomic-architect.md` `tools` field). The SKILL.md `allowed-tools` field (v1.2.0) confirms the same exclusion. The agent definition frontmatter is the authoritative tool declaration per H-34; actual tool availability is governed by that frontmatter, not the cumulative tier model.

### Prohibited Tools

| Tool | Reason |
|------|--------|
| Agent | Worker agent; P-003 prohibition. `disallowedTools: [Agent]` in agent frontmatter. |
| Memory-Keeper | No cross-session state requirement. Sub-skill state is engagement-scoped per P-002. All output persisted to `skills/ux-atomic-design/output/{engagement-id}/`. |

### Citation Requirements

Per T3 tier constraints (`agent-development-standards.md` v1.2.0 [Tier Constraints]: "T3+ agents MUST declare citation guardrails"):

1. All external data referenced in outputs MUST include a citation (source name, document title, or URL).
2. Context7-sourced references MUST note the library and query used.
3. WebSearch-sourced references MUST include the URL.
4. Findings based solely on the architect's Atomic Design methodology knowledge (no external lookup) do not require external citation but MUST reference the specific methodology component (e.g., "Frost, 2016, Chapter 2: Molecules" or "Storybook CDD guide, component coverage principle").

**Citation format example (Context7-sourced):**

```
The Button component exposes 5 variants (size: sm/md/lg, color: primary/secondary)
via props API. (Source: Material UI component documentation, queried via Context7
2026-03-04; query: "Button component props variants size color".)
```

**Citation format example (WebSearch-sourced):**

```
Radix UI primitives use a compound component pattern for composition.
(Source: Radix UI Primitives documentation, https://radix-ui.com/primitives/docs/overview/introduction, accessed 2026-03-04.)
```

---

## Quality Gate Integration

MCP-related outputs contribute to the S-014 quality gate dimensions (`.context/rules/quality-enforcement.md` Section "Quality Gate") as follows:

| S-014 Dimension | MCP Runbook Contribution |
|-----------------|--------------------------|
| **Evidence Quality** | Context7-sourced citations strengthen evidence; WebSearch fallback with URL provides secondary evidence; undisclosed degraded mode operation results in a 0 score per QG-003 |
| **Traceability** | Library IDs traced via `resolve-library-id`; query patterns documented per citation rule 2; MCP outage noted in metadata |
| **Completeness** | All 7 token categories queried when relevant; component API lookups cover all hierarchy levels assessed |
| **Actionability** | Context7 results translated into specific component classification evidence, not raw documentation dumps |
| **Methodological Rigor** | 2-step Context7 protocol followed consistently; failure handling applied per decision table |
| **Internal Consistency** | Same library ID used across all queries for a given library within the engagement; no conflicting Context7 and WebSearch results without reconciliation |

---

## Self-Review Checklist

Before persisting the output, the architect MUST verify MCP compliance (S-010, H-15):

| # | Check | Rule Reference |
|---|-------|---------------|
| 1 | Context7 used for all referenced external libraries (MCP-001) | MCP-001 |
| 2 | Library IDs resolved dynamically via `resolve-library-id`, not hardcoded | Library ID Resolution Table note |
| 3 | All Context7-sourced findings include library name and query citation | Citation rule 2 |
| 4 | All WebSearch-sourced findings include URL | Citation rule 3 |
| 5 | Degraded mode banner present if operating in Manual Component Inventory Mode | P-022 |
| 6 | MCP outage disclosed in report metadata if any MCP failure occurred during engagement | P-022, MCP Failure Handling |
| 7 | Context7 call limit respected per library; no unnecessary re-queries | Protocol step 3 |
| 8 | WebSearch fallback used (not silent skip) when Context7 returns no results | MCP Failure Handling |
| 9 | Phase 1-5 query timing followed per workflow timing map | 5-Phase Workflow table |
| 10 | No prohibited tools used (Agent, Memory-Keeper) | Tool Usage Constraints |

---

## References

| Source | Content | Path |
|--------|---------|------|
| Parent MCP coordination | MCP dependency matrix, degraded mode disclosure, Storybook risk profile, Context7 usage mapping | `skills/user-experience/rules/mcp-coordination.md` (v1.2.0) |
| Framework MCP standards | MCP-001 Context7 governance, MCP-002 Memory-Keeper governance, canonical tool names, error handling | `.context/rules/mcp-tool-standards.md` (v1.3.1) |
| Sub-skill specification | Atomic Design methodology, 5-phase workflow, output specification, MCP dependencies | `skills/ux-atomic-design/SKILL.md` (v1.2.0) |
| ORCHESTRATION.yaml | Orchestration plan governing the build sequence for this sub-skill (schema v3.0.0, created 2026-03-03) | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |
| PLAN.md | MCP adapter scope and post-PROJ-022 roadmap context (created 2026-03-03) | `projects/PROJ-022-user-experience-skill/PLAN.md` [Context] (unversioned -- project plan, not a versioned artifact) |
| Wave progression rules | Wave deployment criteria, Wave 3 entry requirements, signoff enforcement | `skills/user-experience/rules/wave-progression.md` (unversioned -- no VERSION header) |
| Atomic Design methodology | 5-level component hierarchy, composition rules, design token architecture | Frost, B. (2016). *Atomic Design.* Self-published. atomicdesign.bradfrost.com. |
| Storybook CDD guide | Component-Driven Development principles, coverage model | Storybook (2024). "Introduction to Storybook." storybook.js.org/tutorials/intro-to-storybook/ |

---

<!-- GOVERNANCE ID INDEX: MCP-001 (Context7 MUST-use), P-002 (engagement-scoped persistence), P-022 (degraded mode disclosure), H-34 (agent definition schema validation), T3 citation guardrails (agent-development-standards.md Tier Constraints) -->

*Runbook: mcp-runbook.md (v1.1.0)*
*Sub-skill: `/ux-atomic-design`*
*Parent skill: `/user-experience`*
*Parent MCP coordination: `skills/user-experience/rules/mcp-coordination.md`*
*MCP governance SSOT: `.context/rules/mcp-tool-standards.md` (MCP-001)*
*Agent: `ux-atomic-architect` (T3, Systematic, Sonnet)*
*Project: PROJ-022 User Experience Skill*
*Created: 2026-03-04*
