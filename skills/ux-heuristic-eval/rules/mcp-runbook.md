<!-- VERSION: 1.8.0 | DATE: 2026-03-04 | SOURCE: skills/user-experience/rules/mcp-coordination.md, skills/ux-heuristic-eval/SKILL.md | PARENT: /ux-heuristic-eval sub-skill | GOVERNANCE: .context/rules/mcp-tool-standards.md (MCP-001) | PROJECT: projects/PROJ-022-user-experience-skill/PLAN.md | REVISION: iter8 C4 quality gap closure (0.948→0.95) -- removed probabilistic hedges in NNG Context7 rows (evidence quality), added version numbers to References table entries (traceability) -->

# MCP Runbook -- Heuristic Evaluation Sub-Skill

> Operational MCP usage runbook for `/ux-heuristic-eval`. Defines Context7 integration for UX framework documentation lookup, Figma fallback via screenshot-input mode, and failure handling. Operationalizes the parent `skills/user-experience/rules/mcp-coordination.md` rules for the heuristic evaluation domain.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context7 Usage for Heuristic Evaluation](#context7-usage-for-heuristic-evaluation) | When and how to use Context7 during evaluation |
| [Figma MCP Dependency](#figma-mcp-dependency) | Current status, fallback mode, future adapter |
| [Screenshot-Input Mode Protocol](#screenshot-input-mode-protocol) | How to accept and process screenshots when Figma is unavailable |
| [MCP Failure Handling](#mcp-failure-handling) | Fallback paths for Context7 and full MCP outage |
| [Tool Usage Constraints](#tool-usage-constraints) | T3 tier boundary, citation requirements |
| [References](#references) | Source document traceability |

---

## Context7 Usage for Heuristic Evaluation

Per MCP-001 (`.context/rules/mcp-tool-standards.md` v1.3.1 [Context7 Integration]): Context7 MUST be used when the evaluation references an external UX library, framework, or standard by name. The `ux-heuristic-evaluator` agent is T3 (External) and has `mcp__context7__resolve-library-id` and `mcp__context7__query-docs` in its allowed tools.

**Note:** The parent `mcp-coordination.md` Context7 agent table includes `ux-heuristic-evaluator` (added during Wave 1 deployment). The authoritative tool declaration is in the agent definition frontmatter (`skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md`).

### Protocol

1. Call `mcp__context7__resolve-library-id` with the library/framework name and the research question.
2. Call `mcp__context7__query-docs` with the resolved library ID and a specific query.
3. Respect the per-question call limit enforced by the tool; each distinct library resets the limit.
4. If `resolve-library-id` returns no matches, fall back to WebSearch for that library.

### When to Use Context7 During Evaluation

| Evaluation Step | Context7 Trigger | Example Query |
|----------------|-----------------|---------------|
| H1 (Visibility of System Status) | Referencing platform loading/feedback guidelines | `resolve: "Material Design"` then `query: "loading indicator feedback patterns"` |
| H4 (Consistency and Standards) | Looking up platform-specific design conventions | `resolve: "Apple Human Interface Guidelines"` then `query: "navigation bar consistency conventions"` |
| H5 (Error Prevention) | Referencing input validation patterns from a component library | `resolve: "Radix UI"` then `query: "form validation error prevention patterns"` |
| H9 (Error Recovery) | Looking up accessible error message standards | `resolve: "WCAG"` then `query: "error identification success criterion 3.3.1"` |
| H10 (Help and Documentation) | Referencing documentation accessibility standards | `resolve: "WCAG"` then `query: "help and input assistance guidelines"` |
| AI-supplement heuristics | Referencing AI interaction design patterns | `resolve: "Nielsen Norman Group"` then `query: "AI transparency and explainability UX guidelines"` (Context7 indexes software libraries, not UX consultancy content; NNG queries will fall back to WebSearch per MCP-001.) |
| Severity calibration | Referencing Nielsen's severity rating methodology | `resolve: "Nielsen Norman Group"` then `query: "severity ratings for usability problems scale"` (Context7 indexes software libraries, not UX consultancy content; NNG queries will fall back to WebSearch per MCP-001.) |

### When NOT to Use Context7

| Scenario | Alternative |
|----------|-------------|
| General usability concepts already in evaluator knowledge | No tool call needed |
| Codebase-internal UI component inspection | Read/Grep the codebase |
| Evaluating screenshot content against heuristics | Direct visual analysis; no external lookup needed |
| Context7 already queried for the same library in this engagement | Reuse prior results; respect call limit |

### When to Query Context7 in the 5-Step Workflow

This subsection maps Context7 invocation to the 5-step evaluation workflow defined in SKILL.md [Evaluation Workflow]. Context7 calls are made on-demand at specific steps, not front-loaded as a preparation phase.

| Workflow Step | Context7 Action | Rationale |
|---------------|----------------|-----------|
| Step 1 (Input Collection) | Query for product-specific accessibility guidelines when the product domain has specialized standards (e.g., healthcare HIPAA UX, financial WCAG-AAA) | Ensures evaluation scope accounts for domain-specific usability requirements before systematic evaluation begins |
| Step 2 (Systematic Evaluation) | Query for heuristic-specific best practices as needed while evaluating each heuristic | On-demand invocation minimizes unnecessary tool calls and respects the per-question call limit; query when the finding cites a named platform convention, component library, or accessibility standard as the basis for a violation (e.g., the evaluator states "this violates Material Design's navigation guidance" or "this fails WCAG 3.3.1") |
| Step 3 (Severity Rating) | No Context7 needed | Severity rating uses Nielsen's 0-4 scale applied from the evaluator's built-in knowledge; internal classification task |
| Step 4 (Deduplication and Ranking) | No Context7 needed | Deduplication and ranking operate on the evaluator's own findings; no external reference required |
| Step 5 (Report Generation / Self-Review) | Query for severity calibration benchmarks if uncertain about rating consistency (Resolve via WebSearch if Context7 returns no NNG results -- per the When to Use table above.) | Used only when the evaluator has severity ratings that are borderline between levels; resolves calibration uncertainty by referencing published severity examples |

---

## Figma MCP Dependency

### Current Status

**Figma MCP adapter: UNAVAILABLE.** Adapter implementation is post-PROJ-022 scope (see `projects/PROJ-022-user-experience-skill/PLAN.md` [Context]). The `/ux-heuristic-eval` sub-skill has Figma classified as **REQ** in the parent MCP dependency matrix (`skills/user-experience/rules/mcp-coordination.md` [MCP Dependency Matrix]).

### Fallback Mode

The sub-skill operates in **screenshot-input mode** when Figma is unavailable. The evaluation methodology remains identical; only the input modality changes. See [Screenshot-Input Mode Protocol](#screenshot-input-mode-protocol) for operational details.

### What Changes When Figma Becomes Available

When the Figma MCP adapter is implemented and the orchestrator's MCP availability detection succeeds (probe protocol defined in `skills/user-experience/rules/mcp-coordination.md` [MCP Availability Detection]):

| Capability | Screenshot-Input Mode (current) | Figma MCP Mode (future) |
|------------|--------------------------------|------------------------|
| Component state inspection | Not available | Inspect hover, focus, active, disabled states |
| Responsive behavior verification | Not available | Query breakpoint-specific layouts |
| Style token access | Not available | Read design tokens and variables programmatically |
| Layer and hierarchy inspection | Not available | Traverse component tree for structure analysis |
| Multi-screen navigation | Manual: user provides each screen | Automated: traverse Figma page/frame structure |
| Input modality | User-provided screenshots or text descriptions | Direct Figma file/frame access via API |

The agent definition frontmatter and governance file will need updating when Figma MCP becomes available to add the Figma MCP tool to `allowed-tools` and update the tool tier if necessary.

---

## Screenshot-Input Mode Protocol

This section defines how the `ux-heuristic-evaluator` agent accepts and processes design input when the Figma MCP adapter is unavailable (current default).

### Supported Input Formats

| Format | Suitability | Notes |
|--------|-------------|-------|
| PNG/JPG screenshots | Primary | Best for static screen evaluation; standard image input |
| PDF screen exports | Acceptable | Multi-page PDFs treated as multi-screen evaluation |
| Text descriptions of interface | Acceptable (reduced quality) | Used when no visual artifacts are available; evaluation limited to described elements only |
| Figma export URLs (public links) | Not viable | WebFetch retrieves HTML content; it cannot extract processable image data from Figma share URLs. For Figma content without the Figma MCP, users must provide screenshots directly. |

> **Text-Description Mode Caveats:** When evaluating from text descriptions only (no screenshots or visual artifacts), the following heuristics have elevated uncertainty. Findings for these heuristics SHOULD be flagged as "inferred from description; verify with screenshot or interactive evaluation."
>
> - **H1 (Visibility of System Status):** Dynamic state indicators (loading animations, progress bars, real-time updates) cannot be verified from text descriptions alone. Findings about feedback timing and visibility are LOW confidence.
> - **H3 (User Control and Freedom):** Navigation flows, escape routes, and undo/redo mechanisms require visual or interactive context to assess. Text descriptions rarely convey the full navigation structure.
> - **H5 (Error Prevention):** Validation patterns, input constraints, and confirmation dialogs are often under-described in text. Findings about error prevention mechanisms are inferred unless explicitly described.
> - **H7 (Flexibility and Efficiency):** Keyboard shortcuts, accelerators, and customization options are rarely mentioned in text descriptions. Findings for this heuristic are typically incomplete in text-only mode.
> - **H9 (Help Users Recover from Errors):** Error state handling, recovery messaging, and diagnostic guidance are difficult to assess without visual examples of error states. This is the highest-uncertainty heuristic in text-only mode (HIGH impact on finding confidence).

### What to Extract from Screenshots

The evaluator inspects each screenshot for the following, mapped to Nielsen's heuristics:

| Extraction Target | Relevant Heuristics | What to Look For |
|-------------------|-------------------|------------------|
| Navigation elements | H3 (User Control), H4 (Consistency) | Back buttons, breadcrumbs, escape routes, consistent placement |
| Feedback indicators | H1 (Visibility of System Status) | Loading states, progress bars, confirmation messages, state change cues |
| Labels and terminology | H2 (Match Real World) | User-facing language, jargon, metaphor appropriateness |
| Error states (if captured) | H5 (Error Prevention), H9 (Error Recovery) | Validation messages, error format, recovery guidance |
| Visual hierarchy | H8 (Aesthetic and Minimalist Design) | Clutter, information density, content prioritization |
| Interactive affordances | H6 (Recognition vs. Recall) | Button visibility, action discoverability, contextual hints |
| Help elements | H10 (Help and Documentation) | Tooltips, help icons, contextual guidance presence |

### Limitations of Screenshot-Based Evaluation

The following limitations MUST be disclosed in the output per P-022. The degraded mode banner (defined in `skills/user-experience/rules/mcp-coordination.md` [Degraded Mode Disclosure]) MUST appear at the top of the evaluation report:

```
[DEGRADED MODE] This evaluation was produced without Figma MCP access.
Input was provided via screenshot-input mode. Some features are reduced:
- Cannot inspect component states (hover, focus, active, disabled)
- Cannot verify responsive behavior across breakpoints
- Cannot access style tokens or design system variables programmatically
```

Notify the user of screenshot-input mode status at evaluation start (before analyzing input), not only in the output report, per P-022 (no deception about capabilities) -- users must know the evaluation operates under reduced observability.

**Heuristic-specific limitations in screenshot mode:**

| Heuristic | Limitation | Impact on Finding Confidence |
|-----------|-----------|------------------------------|
| H1 (Visibility of System Status) | Cannot observe dynamic feedback (loading animations, real-time updates) | Findings about dynamic feedback are LOW confidence; note as inferred |
| H3 (User Control and Freedom) | Cannot test undo/redo or cancel flows interactively | Findings limited to visible UI elements; flow-level assessment is inferred |
| H5 (Error Prevention) | Cannot trigger validation to observe error prevention behavior | Findings limited to visible constraints and defaults in the screenshot |
| H2 (Match Between System and Real World) | Cannot interact with dynamic content to assess terminology in context (e.g., dropdown labels, tooltip text not visible in screenshot) | LOW impact; most terminology is visible in static screenshots; findings about hidden labels are inferred |
| H6 (Recognition Rather Than Recall) | Cannot verify interactive discoverability (e.g., hover-revealed actions, contextual menus) | LOW impact; primary affordances are visible in screenshots; findings about hover-dependent discoverability are inferred |
| H7 (Flexibility and Efficiency) | Cannot observe keyboard shortcuts or accelerator behaviors | Findings limited to visible customization options |
| H8 (Aesthetic and Minimalist Design) | Cannot assess dynamic visual noise (animations, transitions, overlapping modal stacking) | LOW impact; static visual clutter and information density are directly observable from screenshots |
| H4 (Consistency and Standards) | Cross-screen consistency and platform hover/focus conventions are unobservable in static screenshots | MEDIUM impact; cross-screen analysis requires multiple screenshots of the same UI pattern |
| H9 (Help Users Recover from Errors) | Error states require triggering; screenshot mode cannot capture dynamic error presentation | HIGH impact; error recovery quality cannot be assessed without triggering error states |
| H10 (Help and Documentation) | Hover-triggered tooltips and contextual help are not visible in static screenshots | MEDIUM impact; help content accessibility limited to always-visible documentation |

> **Impact rating attribution:** Impact ratings are defined as: HIGH = finding cannot be assessed without interactive input; MEDIUM = finding partially observable with significant gaps expected; LOW = finding directly observable in static screenshots. These are editorial assessment specific to screenshot-input mode, not derived from `skills/user-experience/rules/synthesis-validation.md` (which defines HIGH/MEDIUM/LOW for cross-framework synthesis convergence gates, a different classification purpose). P-022 disclosure: these ratings reflect evaluator judgment about screenshot-mode limitations, not empirical measurement.

---

## MCP Failure Handling

### Context7 Unavailable

Per `mcp-tool-standards.md` v1.3.1 [Error Handling]:

| Failure Condition | Fallback Action |
|-------------------|----------------|
| `resolve-library-id` returns no matches | Fall back to WebSearch for that library. Note "Context7 no coverage" in the evaluation output next to the affected finding. |
| `query-docs` returns empty or irrelevant results | Use WebSearch for the specific query. Note "Context7 no coverage" in the evaluation output. |
| Context7 tool-enforced call limit reached | Fall back to WebSearch for remaining queries for that library. |
| Context7 MCP server timeout or error | Continue evaluation without Context7. Use WebSearch for all external documentation lookups. Note the MCP outage in the evaluation report metadata. One retry attempted before declaring unavailable, per `mcp-coordination.md` detection protocol. |

### Full MCP Server Outage

When the MCP server is completely unavailable (detected by the orchestrator's probe protocol per `skills/user-experience/rules/mcp-coordination.md` [MCP Availability Detection]):

1. **Continue evaluation.** The heuristic evaluation methodology does not depend on MCP for core functionality. Nielsen's 10 heuristics are applied from the evaluator's built-in knowledge.
2. **Use WebSearch as fallback** for any external documentation lookups (WCAG criteria, platform guidelines, severity scale references).
3. **Disclose in output** per P-022: note that MCP tools were unavailable and external references were sourced via web search.
4. **No blocking.** MCP outage does not block evaluation execution. The evaluation proceeds with reduced reference precision but identical methodology.

---

## Tool Usage Constraints

### Tool Tier

The `ux-heuristic-evaluator` agent operates at **T3 (External)** per `agent-development-standards.md` v1.2.0 [Tool Security Tiers]. This tier includes:

- **T1 (Read-Only):** Read, Glob, Grep
- **T2 (Read-Write):** Write, Edit, Bash
- **T3 (External):** WebSearch, WebFetch, Context7 (`mcp__context7__resolve-library-id`, `mcp__context7__query-docs`)

> **Note:** The SKILL.md (v1.0.0) `allowed-tools` entry has been corrected to exclude Bash, aligning with the agent definition frontmatter (T3 tier does not require shell access). The agent definition (`skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md` `tools` field) is the authoritative tool declaration per H-34. The tier breakdown above reflects the cumulative T3 tier model from `agent-development-standards.md`; actual tool availability for the agent is governed by the agent definition frontmatter.

### Prohibited Tools

| Tool | Reason |
|------|--------|
| Agent | Worker agent; P-003 prohibition. `disallowedTools: [Agent]` in agent frontmatter. |
| Memory-Keeper | No cross-session state requirement. Sub-skill state is engagement-scoped per P-002. All output persisted to `skills/ux-heuristic-eval/output/{engagement-id}/`. |

### Citation Requirements

Per T3 tier constraints (`agent-development-standards.md` v1.2.0 [Tier Constraints]: "T3+ agents MUST declare citation guardrails"):

1. All external data referenced in findings MUST include a citation (source name, document title, or URL).
2. Context7-sourced references MUST note the library and query used.
3. WebSearch-sourced references MUST include the URL.
4. Findings based solely on the evaluator's heuristic knowledge (no external lookup) do not require external citation but MUST reference the specific Nielsen heuristic by number and name.

---

## References

| Source | Content | Path |
|--------|---------|------|
| Parent MCP coordination | MCP dependency matrix, degraded mode disclosure, Figma risk profile, Context7 usage mapping | `skills/user-experience/rules/mcp-coordination.md` (v1.2.0) |
| Framework MCP standards | MCP-001 Context7 governance, MCP-002 Memory-Keeper governance, canonical tool names, error handling | `.context/rules/mcp-tool-standards.md` v1.3.1 |
| Sub-skill specification | Heuristic evaluation methodology, 5-step workflow, output specification, MCP dependencies | `skills/ux-heuristic-eval/SKILL.md` (v1.0.0) |
| ORCHESTRATION.yaml | Orchestration plan governing the build sequence for this sub-skill | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |
| PLAN.md | MCP adapter scope and post-PROJ-022 roadmap context | `projects/PROJ-022-user-experience-skill/PLAN.md` [Context] |

> **Resolved:** The parent `mcp-coordination.md` Context7 agent table now includes `ux-heuristic-evaluator` (added during Wave 1 deployment, mcp-coordination.md v1.2.0).

---

*Runbook: mcp-runbook.md (v1.8.0)*
*Sub-skill: `/ux-heuristic-eval`*
*Parent skill: `/user-experience`*
*Parent MCP coordination: `skills/user-experience/rules/mcp-coordination.md`*
*MCP governance SSOT: `.context/rules/mcp-tool-standards.md` (MCP-001)*
*Agent: `ux-heuristic-evaluator` (T3, Systematic, Haiku)*
*Project: PROJ-022 User Experience Skill*
*Created: 2026-03-04*
