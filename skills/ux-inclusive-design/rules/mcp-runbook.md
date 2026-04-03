<!-- VERSION: 1.1.0 | DATE: 2026-03-04 | SOURCE: skills/user-experience/rules/mcp-coordination.md, skills/ux-inclusive-design/SKILL.md | PARENT: /ux-inclusive-design sub-skill | GOVERNANCE: .context/rules/mcp-tool-standards.md (MCP-001) | PROJECT: projects/PROJ-022-user-experience-skill/PLAN.md | REVISION: iter2 -- add MR-001 through MR-010 rule IDs, self-review checklist (S-010), quality gate integration section, Library ID verification note, retry timeout cross-reference, Step 5 Context7 trigger threshold, T3 tier note restructure -->

# MCP Runbook -- Inclusive Design Sub-Skill

> Operational MCP usage runbook for `/ux-inclusive-design`. Defines Context7 integration for WCAG 2.2 and ARIA APG 1.2 documentation lookup, Figma REQ dependency with screenshot-input mode fallback, Storybook ENH dependency, and failure handling. Operationalizes the parent `skills/user-experience/rules/mcp-coordination.md` rules for the inclusive design and accessibility evaluation domain.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context7 Usage for Inclusive Design](#context7-usage-for-inclusive-design) | When and how to use Context7 during accessibility evaluation |
| [Library ID Resolution Table](#library-id-resolution-table) | Pre-resolved library IDs for accessibility standards |
| [Figma MCP Dependency](#figma-mcp-dependency) | Current status, fallback mode, future adapter |
| [Screenshot-Input Mode Protocol](#screenshot-input-mode-protocol) | How to produce outputs when Figma is unavailable |
| [Storybook MCP Dependency](#storybook-mcp-dependency) | ENH classification, fallback approach |
| [MCP Failure Handling](#mcp-failure-handling) | Fallback paths for Context7, Figma, Storybook, and full MCP outage |
| [Tool Usage Constraints](#tool-usage-constraints) | T3 tier boundary, citation requirements |
| [Quality Gate Integration](#quality-gate-integration) | How MCP operational compliance maps to S-014 dimensions |
| [Self-Review Checklist](#self-review-checklist) | S-010 verification before output persistence |
| [References](#references) | Source document traceability |

---

## Context7 Usage for Inclusive Design

Per MCP-001 (`.context/rules/mcp-tool-standards.md` v1.3.1 [Context7 Integration]): Context7 MUST be used when the evaluation references an external accessibility standard, ARIA pattern, or component library documentation by name (MR-001). The `ux-inclusive-evaluator` agent is T3 (External) and has `mcp__context7__resolve-library-id` and `mcp__context7__query-docs` in its allowed tools.

**Operational state:** Context7 queries are available NOW for accessibility standard research (WCAG 2.2 success criteria definitions, ARIA APG design patterns, component library accessibility APIs). The protocol defined in this runbook governs the agent in both current and post-Wave-3-deployment states. See `skills/user-experience/rules/wave-progression.md` [Wave 3 Deployment Criteria] for deployment timeline tracking.

**Note:** The parent `mcp-coordination.md` [Context7 Usage] agent table should include `ux-inclusive-evaluator` upon Wave 3 deployment. The authoritative tool declaration is in the agent definition frontmatter (`skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md`).

### Protocol

1. Call `mcp__context7__resolve-library-id` with the library/framework name and the research question.
2. Call `mcp__context7__query-docs` with the resolved library ID and a specific query.
3. Respect the per-question call limit enforced by the tool; each distinct library resets the limit.
4. If `resolve-library-id` returns no matches, fall back to WebSearch for that library.

### When to Use Context7 During Evaluation

| Evaluation Step | Context7 Trigger | Example Query |
|-----------------|-----------------|---------------|
| WCAG 2.2 POUR Audit (Step 2) | Referencing a specific WCAG success criterion technique or sufficient technique | `resolve: "WCAG"` then `query: "success criterion 1.4.3 contrast minimum techniques sufficient advisory"` |
| WCAG 2.2 POUR Audit (Step 2) | Looking up WCAG 2.2-specific new criteria (added in 2.2) | `resolve: "WCAG"` then `query: "WCAG 2.2 new success criteria 2.4.11 focus appearance 2.4.12 focus not obscured 3.2.6 consistent help 3.3.7 redundant entry"` |
| Color Contrast (Step 3) | Referencing contrast computation methodology or technique details | `resolve: "WCAG"` then `query: "contrast ratio computation relative luminance formula technique G18 G145"` |
| Keyboard Navigation (Step 4) | Looking up ARIA APG keyboard interaction patterns for specific widgets | `resolve: "ARIA APG"` then `query: "keyboard interaction pattern tabs dialog menu combobox"` |
| Screen Reader Compatibility (Step 5) | Referencing ARIA role, state, or property definitions | `resolve: "ARIA"` then `query: "aria-live aria-atomic aria-relevant live region role alert"` |
| Screen Reader Compatibility (Step 5) | Looking up ARIA APG design pattern for a specific component | `resolve: "ARIA APG"` then `query: "dialog modal pattern aria-modal focus management"` |
| Screen Reader Compatibility (Step 5) | Referencing component library accessibility API documentation | `resolve: "Material UI"` then `query: "Button accessibility aria-label disabled state keyboard"` |
| Cognitive Load (Step 5) | Referencing readability formula or WCAG understandable principle techniques | `resolve: "WCAG"` then `query: "success criterion 3.1.5 reading level technique G86 readable"` |

### When NOT to Use Context7

| Scenario | Alternative |
|----------|-------------|
| General accessibility concepts already in evaluator knowledge (POUR principles, severity scale, Persona Spectrum methodology) | No tool call needed |
| Codebase-internal component markup inspection | Read/Grep the codebase |
| Prior evaluation results from this engagement | Read the engagement output files |
| Context7 already queried for the same library in this evaluation | Reuse prior results; respect call limit |
| General legal accessibility compliance concepts (ADA, EAA, Section 508) | WebSearch -- Context7 indexes technical specifications, not legal guidance |
| Microsoft Inclusive Design Toolkit methodology | WebSearch -- methodology is well-documented on microsoft.com/design/inclusive; Context7 may not index non-specification content |

### When to Query Context7 in the Evaluation Workflow

This subsection maps Context7 invocation to the 7-step evaluation workflow defined in `skills/ux-inclusive-design/rules/inclusive-design-rules.md` [Workflow Phase Sequencing Rules]. Context7 calls are made on-demand at specific steps, not front-loaded.

| Workflow Step | Context7 Action | Rationale |
|---------------|----------------|-----------|
| Step 1 (Context Gathering) | No Context7 needed | Context gathering operates on input artifacts and handoff data; no external standard lookups required |
| Step 2 (WCAG POUR Audit) | Query for specific WCAG success criterion techniques when evaluating a criterion and the evaluator needs technique implementation details. WebSearch escalation: if Context7 returns no results, search `"WCAG 2.2 success criterion {SC number} techniques"`. | On-demand invocation at the criterion level prevents bulk pre-loading of WCAG documentation |
| Step 3 (Color Contrast) | Query for contrast ratio computation methodology or specific technique details when the evaluator needs to verify threshold application. WebSearch escalation: if Context7 returns no results, search `"WCAG contrast ratio relative luminance computation"`. | Contrast computation methodology is stable; query only when technique-level detail is needed |
| Step 4 (Keyboard Navigation) | Query for ARIA APG keyboard interaction patterns when evaluating widget-specific keyboard behavior (tabs, dialogs, menus, comboboxes). WebSearch escalation: if Context7 returns no results for ARIA APG, search `"WAI ARIA APG {widget name} keyboard interaction pattern"`. | ARIA APG patterns define expected keyboard behavior per widget type; the evaluator needs these to assess conformance |
| Step 5 (Screen Reader + Cognitive Load) | Query for ARIA role/state/property definitions when evaluating ARIA implementation correctness. Query for component library accessibility APIs when the input artifact references a specific named design system (e.g., Material UI, Radix UI) and the evaluation requires verifying that component's accessibility properties (MR-002). Do not query when the evaluation is generic (no named component library referenced). WebSearch escalation: if Context7 returns no results, search `"ARIA specification {role or property name}"`. | ARIA specification details are essential for assessing semantic HTML and landmark correctness. Named design system threshold prevents unnecessary queries for generic evaluations |
| Step 6 (Persona Spectrum) | No Context7 needed | Persona Spectrum analysis uses Microsoft Inclusive Design methodology from evaluator knowledge; no external specification lookup required |
| Step 7 (Synthesis + Report) | No Context7 needed | Report synthesis operates on collected findings from Steps 2-6; no new external lookups needed |

---

## Library ID Resolution Table

Pre-resolved library identifiers for commonly queried accessibility standards. Use these as the initial `resolve-library-id` input to minimize resolution latency. If a pre-resolved ID fails, re-resolve with the library name.

| Library/Framework | Resolve Query | Expected Library Name | Usage Context |
|-------------------|--------------|----------------------|---------------|
| WCAG 2.2 | `"WCAG"` or `"Web Content Accessibility Guidelines"` | W3C WCAG | Success criteria definitions, techniques, conformance requirements |
| ARIA Specification | `"ARIA"` or `"WAI-ARIA"` | W3C ARIA | Role, state, and property definitions for assistive technology |
| ARIA APG 1.2 | `"ARIA APG"` or `"ARIA Authoring Practices Guide"` | W3C APG | Design pattern keyboard interaction, widget patterns |
| Material UI | `"Material UI"` or `"MUI"` | Material UI | Component accessibility API (Button, TextField, Dialog, etc.) |
| Radix UI | `"Radix UI"` or `"Radix Primitives"` | Radix UI | Accessible primitive components (Dialog, Popover, Select, etc.) |
| React ARIA | `"React ARIA"` or `"Adobe React ARIA"` | React ARIA | Accessibility hooks for React component libraries |
| Headless UI | `"Headless UI"` | Headless UI | Accessible headless UI components (Tailwind CSS ecosystem) |

**Note:** Library IDs are resolved dynamically by Context7. The "Expected Library Name" column is a reference hint; actual resolved names may vary. Always use the ID returned by `resolve-library-id`, not the expected name. Expected names verified against Context7 as of 2026-03-04. Re-verify if resolution fails on first attempt (MR-003).

---

## Figma MCP Dependency

### Current Status

**Figma MCP adapter: UNAVAILABLE.** Adapter implementation is post-PROJ-022 scope (see `projects/PROJ-022-user-experience-skill/PLAN.md` [Context]). The `/ux-inclusive-design` sub-skill has Figma classified as **REQ** in the parent MCP dependency matrix (`skills/user-experience/rules/mcp-coordination.md` [MCP Dependency Matrix]).

### Fallback Mode

The sub-skill operates in **screenshot-input mode** when Figma is unavailable. The evaluation methodology remains identical; the input modality and certain measurement capabilities change. See [Screenshot-Input Mode Protocol](#screenshot-input-mode-protocol) for operational details.

### What Changes When Figma Becomes Available

When the Figma MCP adapter is implemented and the orchestrator's MCP availability detection succeeds (probe protocol defined in `skills/user-experience/rules/mcp-coordination.md` [MCP Availability Detection]):

| Capability | Screenshot-Input Mode (current) | Figma MCP Mode (future) |
|------------|--------------------------------|------------------------|
| Color value extraction | Manual: user provides hex/RGB values | Automated: extract from design layers and tokens |
| Component hierarchy inspection | Visual assessment from screenshots | Programmatic: traverse component tree |
| Interactive state evaluation | Separate screenshots per state (hover, focus, active, disabled) | Automated: inspect all states from single component |
| Responsive behavior assessment | Screenshots at multiple breakpoints | Automated: evaluate at all defined breakpoints |
| Design token access | Not available; infer from visual presentation | Programmatic: access color palette, spacing, typography tokens |
| Focus indicator evaluation | Visual assessment from screenshots | Automated: extract focus indicator dimensions and colors |
| Contrast ratio computation | Manual computation from user-provided hex/RGB values | Automated: compute from extracted foreground/background colors |

The agent definition frontmatter and governance file will need updating when Figma MCP becomes available to add the Figma MCP tool to `tools` and update the tool tier if necessary.

---

## Screenshot-Input Mode Protocol

This section defines how the `ux-inclusive-evaluator` agent operates when the Figma MCP adapter is unavailable (current default).

### P-022 Degraded Mode Disclosure

The following disclosure banner MUST appear at the top of the evaluation output when operating in screenshot-input mode (MR-004). This is required by P-022 (no deception about capabilities) per `skills/user-experience/rules/mcp-coordination.md` [Degraded Mode Disclosure]:

```
[DEGRADED MODE] This output was produced without Figma MCP access.
Input was provided via screenshot-input mode. Some features are reduced:
- Cannot inspect design layers or component hierarchy programmatically
- Cannot extract exact color values for automated contrast ratio computation
- Cannot evaluate interactive states (animations, transitions, dynamic content)
- Cannot access design token definitions or systematic color palette information
```

Notify the user of screenshot-input mode status at evaluation start (before producing outputs), not only in the output report, per P-022 -- users must know the evaluation operates without design layer inspection functionality.

### Evaluation Capabilities in Screenshot-Input Mode

| Evaluation Step | Full Mode Capability | Screenshot-Input Mode Capability | Impact on Output Quality |
|-----------------|---------------------|--------------------------------|--------------------------|
| WCAG POUR Audit (Step 2) | Full programmatic + visual evaluation | Visual evaluation from screenshots only | MEDIUM: visual-only assessment cannot verify programmatic ARIA attributes; flag affected criteria as "Visual assessment -- verify with markup" |
| Color Contrast (Step 3) | Automated extraction and computation | Manual computation from user-provided values; visual flagging when values unavailable | HIGH: cannot confirm PASS without computed ratios; elements flagged for manual measurement |
| Keyboard Navigation (Step 4) | N/A (keyboard testing is structural in both modes) | Structural assessment from visual layout | MEDIUM: screenshot analysis infers tab order from visual layout but cannot verify actual keyboard behavior |
| Screen Reader Compatibility (Step 5) | Markup inspection + semantic analysis | Visual inference of semantic structure from screenshots | HIGH: cannot verify ARIA attributes, heading levels, or form label associations from screenshots alone |
| Cognitive Load (Step 5) | Full content analysis + readability computation | Visual content assessment; text extraction limited | LOW: cognitive load assessment is primarily qualitative; screenshots provide sufficient input for reading level and navigation consistency assessment |
| Persona Spectrum (Step 6) | Same in both modes | Same in both modes | NONE: Persona Spectrum analysis is based on interaction pattern identification, which operates identically from screenshots and Figma |

> **Impact rating attribution:** Impact ratings are defined as: HIGH = measurement precision significantly reduced, key findings require manual verification; MEDIUM = evaluation possible but with reduced precision, some findings require manual confirmation; LOW = minimal impact on output quality; NONE = no difference between modes. These are editorial assessments specific to screenshot-input mode. P-022 disclosure: these ratings reflect evaluator judgment about mode limitations, not empirical measurement.

### Screenshot Requirements for Evaluation

When operating in screenshot-input mode, the user SHOULD provide:

| Input Type | Purpose | Minimum Requirement |
|-----------|---------|---------------------|
| Full-page screenshots | WCAG POUR evaluation scope | At least 1 screenshot per page or screen being evaluated |
| Component-level screenshots | Atomic design component evaluation | 1 screenshot per component type (button, form field, card, etc.) |
| Interactive state screenshots | Focus and hover state evaluation | Separate screenshots for default, hover, focus, active, and disabled states |
| Responsive screenshots | Multi-breakpoint evaluation | Screenshots at mobile (375px), tablet (768px), and desktop (1440px) when responsive evaluation is in scope |
| Color specification | Contrast computation | Hex/RGB values for foreground and background colors of text and UI components |

---

## Storybook MCP Dependency

### Current Status

**Storybook MCP adapter: UNAVAILABLE.** Classification: **ENH** (Enhancement). The Storybook integration enhances accessibility evaluation by enabling component-level story inspection but is not required for the core evaluation workflow.

### Fallback Approach

When Storybook MCP is unavailable, the evaluator uses manual component inventory provided by the user:

| Storybook MCP Capability | Fallback Without Storybook |
|--------------------------|---------------------------|
| Browse component stories | User provides component list and documentation |
| Inspect component markup | User provides markup samples or references |
| View component accessibility properties | User provides component accessibility documentation or specifications |
| Test interactive component states | User provides screenshots of interactive states |

**No degraded mode banner is required** for Storybook unavailability because it is classified as ENH (not REQ) (MR-005). The evaluation output does not carry a Storybook-specific mode disclosure.

---

## MCP Failure Handling

### Context7 Unavailable

Per `mcp-tool-standards.md` v1.3.1 [Error Handling]:

| Failure Condition | Fallback Action |
|-------------------|----------------|
| `resolve-library-id` returns no matches | Fall back to WebSearch for that library. Note "Context7 no coverage" in the evaluation output next to the affected finding. WebSearch fallback query: `"{library name} {specific standard or criterion}"`. |
| `query-docs` returns empty or irrelevant results | Use WebSearch for the specific query. Note "Context7 no coverage" in the evaluation output. |
| Context7 tool-enforced call limit reached | Fall back to WebSearch for remaining queries for that library. |
| Context7 MCP server timeout (> 5 seconds with no response) or error | Continue evaluation without Context7. Use WebSearch for all external documentation lookups. Note the MCP outage in the evaluation report metadata. One retry attempted before declaring unavailable (MR-006), per `mcp-coordination.md` [MCP Availability Detection] detection protocol. Retry interval: 3 seconds after first failure (see `mcp-coordination.md` [MCP Availability Detection] for retry specification). |

### Figma MCP Unavailable (Current Default)

Since the Figma MCP adapter is not yet implemented, the Figma-unavailable state is the current default. No dynamic detection is needed; the evaluator always operates in screenshot-input mode.

When the Figma MCP adapter becomes available in the future and subsequently fails:

1. **Detect failure** via the orchestrator's Figma probe (defined in `mcp-coordination.md` [Future MCP Probes]).
2. **Fall back to screenshot-input mode** per [Screenshot-Input Mode Protocol](#screenshot-input-mode-protocol).
3. **Disclose degraded mode** per P-022 using the banner defined in [P-022 Degraded Mode Disclosure](#p-022-degraded-mode-disclosure).
4. **No blocking.** Figma outage does not block evaluation execution. The evaluation proceeds with reduced measurement precision in screenshot-input mode.

### Storybook MCP Unavailable (Current Default)

Storybook MCP is classified as ENH. Its unavailability does not trigger degraded mode or a P-022 disclosure banner.

1. **Continue evaluation** using the manual component inventory fallback.
2. **No disclosure required** beyond noting the input source in the Engagement Context section.

### Full MCP Server Outage

When the MCP server is completely unavailable (detected by the orchestrator's probe protocol per `skills/user-experience/rules/mcp-coordination.md` [MCP Availability Detection]):

1. **Continue evaluation** (MR-007). The accessibility evaluation methodology does not depend on MCP for core functionality. WCAG 2.2 evaluation, Persona Spectrum analysis, and all testing protocols are applied from the evaluator's built-in knowledge of W3C standards and Microsoft Inclusive Design methodology.
2. **Use WebSearch as fallback** for any external documentation lookups (WCAG technique details, ARIA pattern specifications, component library accessibility APIs) (MR-008).
3. **Disclose in output** per P-022: note that MCP tools were unavailable and external references were sourced via web search (MR-009).
4. **No blocking.** MCP outage does not block evaluation execution (MR-010). The evaluation proceeds with reduced reference precision but identical methodology.

---

## Tool Usage Constraints

### Tool Tier

The `ux-inclusive-evaluator` agent operates at **T3 (External)** per `agent-development-standards.md` v1.2.0 [Tool Security Tiers]. This tier includes:

- **T1 (Read-Only):** Read, Glob, Grep
- **T2 (Read-Write):** T1 + Write, Edit, Bash
- **T3 (External):** T2 + WebSearch, WebFetch, Context7 (`mcp__context7__resolve-library-id`, `mcp__context7__query-docs`)

> **Note:** Actual tools per agent definition frontmatter: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Context7 (no Bash). The tier breakdown above reflects the cumulative T3 tier model from `agent-development-standards.md` v1.2.0 [Tool Security Tiers]. The `ux-inclusive-evaluator` agent excludes Bash from its actual tool set -- Bash is not required for accessibility evaluation and is omitted from the agent definition frontmatter (`skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` `tools` field). The SKILL.md `allowed-tools` field (v1.1.0) confirms the same exclusion. The agent definition frontmatter is the authoritative tool declaration per H-34; actual tool availability is governed by that frontmatter, not the cumulative tier model.

### Prohibited Tools

| Tool | Reason |
|------|--------|
| Agent | Worker agent; P-003 prohibition. `disallowedTools: [Agent]` in agent frontmatter. |
| Memory-Keeper | No cross-session state requirement. Sub-skill state is engagement-scoped per P-002. All output persisted to `skills/ux-inclusive-design/output/{engagement-id}/`. |

### Citation Requirements

Per T3 tier constraints (`agent-development-standards.md` v1.2.0 [Tier Constraints]: "T3+ agents MUST declare citation guardrails"):

1. All external data referenced in outputs MUST include a citation (source name, document title, or URL).
2. Context7-sourced references MUST note the library and query used.
3. WebSearch-sourced references MUST include the URL.
4. Findings based solely on the evaluator's WCAG or Inclusive Design knowledge (no external lookup) do not require external citation but MUST reference the specific WCAG success criterion (e.g., "SC 1.4.3 Contrast Minimum") or Microsoft Inclusive Design principle (e.g., "Recognize Exclusion, Microsoft, 2016").

---

## Quality Gate Integration

How MCP operational compliance maps to the S-014 LLM-as-Judge quality dimensions for quality gate scoring (H-13, >= 0.92 for C2+ deliverables).

> **Source:** `.context/rules/quality-enforcement.md` [Quality Gate]. `skills/ux-inclusive-design/rules/inclusive-design-rules.md` [Quality Gate Integration].

### S-014 Dimension Mapping for MCP Compliance

| S-014 Dimension | Weight | MCP Compliance Mapping | Verification |
|----------------|--------|------------------------|--------------|
| Completeness | 0.20 | All required Context7 queries attempted for WCAG criterion technique lookups; P-022 degraded mode banner present when Figma is unavailable (MR-004); Library ID resolution table consulted (MR-003) | Count of Context7 queries attempted vs. WCAG criteria requiring technique detail |
| Internal Consistency | 0.20 | Context7 per-step trigger table aligns with evaluation workflow steps; screenshot-input mode capability table consistent with degraded mode disclosure banner | No contradictions between trigger table and actual invocation pattern |
| Methodological Rigor | 0.20 | Context7 two-step protocol followed (resolve then query); WebSearch escalation used on Context7 failure (MR-008); retry logic applied before declaring unavailable (MR-006) | Evidence of protocol adherence in evaluation report metadata |
| Evidence Quality | 0.15 | All Context7-sourced data cited with library name and query (citation requirements per T3 tier); WebSearch-sourced references include URL; knowledge-based references cite WCAG criterion or Microsoft principle | No uncited external references in evaluation output |
| Actionability | 0.15 | Screenshot requirements communicated to user at evaluation start (MR-004); failure handling steps actionable with explicit fallback paths; degraded mode impact ratings documented per evaluation step | User-facing degraded mode notification present before output production |
| Traceability | 0.10 | MCP status documented in evaluation report metadata; MR rule IDs traceable from self-review checklist to this runbook; MCP outage noted in report when applicable (MR-009) | All MR-prefixed rule IDs resolvable to this runbook |

---

## Self-Review Checklist

Before persisting evaluation output, verify all MCP-related compliance items below (S-010):

- [ ] 1. Context7 was used for external accessibility standard lookups per MCP-001 (MR-001)
- [ ] 2. Context7 queries for component libraries were triggered only when input references a named design system (MR-002)
- [ ] 3. Library ID resolution table was consulted before resolving library IDs (MR-003)
- [ ] 4. P-022 degraded mode disclosure banner is present if Figma MCP was unavailable (MR-004)
- [ ] 5. No degraded mode banner for ENH-classified Storybook dependency (MR-005)
- [ ] 6. One retry with 3-second interval was attempted before declaring Context7 unavailable (MR-006)
- [ ] 7. Evaluation continued without blocking on full MCP outage (MR-007)
- [ ] 8. WebSearch was used as fallback when Context7 returned no results or was unavailable (MR-008)
- [ ] 9. MCP outage is disclosed in evaluation output per P-022 (MR-009)
- [ ] 10. MCP outage did not block evaluation execution (MR-010)
- [ ] 11. All Context7-sourced references cite library name and query per T3 citation requirements
- [ ] 12. All WebSearch-sourced references include the URL per T3 citation requirements
- [ ] 13. Context7 was NOT used for topics in the "When NOT to Use" list (general concepts, codebase internals, prior results, legal guidance, Microsoft Inclusive Design methodology)

---

## References

| Source | Content | Path |
|--------|---------|------|
| Parent MCP coordination | MCP dependency matrix, degraded mode disclosure, Figma risk profile, Context7 usage mapping | `skills/user-experience/rules/mcp-coordination.md` |
| Framework MCP standards | MCP-001 Context7 governance, MCP-002 Memory-Keeper governance, canonical tool names, error handling | `.context/rules/mcp-tool-standards.md` (v1.3.1) |
| Sub-skill specification | Inclusive design methodology, output specification, MCP dependencies | `skills/ux-inclusive-design/SKILL.md` (v1.1.0) |
| Agent definition | Agent frontmatter, identity, methodology, capabilities, guardrails | `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` |
| ORCHESTRATION.yaml | Orchestration plan governing the build sequence for this sub-skill (schema v3.0.0) | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |
| PLAN.md | MCP adapter scope and post-PROJ-022 roadmap context | `projects/PROJ-022-user-experience-skill/PLAN.md` [Context] |
| Wave progression rules | Wave deployment criteria, Wave 3 entry requirements, signoff enforcement | `skills/user-experience/rules/wave-progression.md` |
| WCAG 2.2 | Web Content Accessibility Guidelines (WCAG) 2.2. W3C Recommendation, 05 October 2023 | W3C specification |
| ARIA APG 1.2 | ARIA Authoring Practices Guide (APG) 1.2. W3C Group Note, 2023 | W3C specification |
| Microsoft, 2016 | Microsoft Inclusive Design Toolkit. Microsoft Corporation, 2016 | microsoft.com/design/inclusive |

---

<!-- GOVERNANCE ID INDEX: MR-001 (Context7 MUST-use per MCP-001), MR-002 (component library query threshold), MR-003 (library ID verification), MR-004 (P-022 degraded mode disclosure), MR-005 (ENH no-disclosure rule), MR-006 (one-retry-before-unavailable), MR-007 (continue on full MCP outage), MR-008 (WebSearch fallback), MR-009 (MCP outage P-022 disclosure), MR-010 (non-blocking MCP outage), MCP-001 (Context7 MUST-use), P-002 (engagement-scoped persistence), P-022 (degraded mode disclosure), H-34 (agent definition schema validation), T3 citation guardrails (agent-development-standards.md Tier Constraints) -->

*Runbook: mcp-runbook.md (v1.1.0)*
*Sub-skill: `/ux-inclusive-design`*
*Parent skill: `/user-experience`*
*Parent MCP coordination: `skills/user-experience/rules/mcp-coordination.md`*
*MCP governance SSOT: `.context/rules/mcp-tool-standards.md` (MCP-001)*
*Agent: `ux-inclusive-evaluator` (T3, Systematic, Sonnet)*
*Project: PROJ-022 User Experience Skill*
*Created: 2026-03-04*
