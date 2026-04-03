<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: skills/user-experience/rules/mcp-coordination.md, skills/ux-lean-ux/SKILL.md | PARENT: /ux-lean-ux sub-skill | GOVERNANCE: .context/rules/mcp-tool-standards.md (MCP-001) | PROJECT: projects/PROJ-022-user-experience-skill/PLAN.md -->

# MCP Runbook -- Lean UX Sub-Skill

> Operational MCP usage runbook for `/ux-lean-ux`. Defines Context7 integration for Lean UX methodology documentation lookup, Miro REQ dependency with text-based exercise mode fallback, and failure handling. Operationalizes the parent `skills/user-experience/rules/mcp-coordination.md` rules for the Lean UX hypothesis-driven design domain.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context7 Usage for Lean UX](#context7-usage-for-lean-ux) | When and how to use Context7 during facilitation |
| [Miro MCP Dependency](#miro-mcp-dependency) | Current status, fallback mode, future adapter |
| [Text-Based Exercise Mode Protocol](#text-based-exercise-mode-protocol) | How to produce structured markdown outputs when Miro is unavailable |
| [MCP Failure Handling](#mcp-failure-handling) | Fallback paths for Context7 and full MCP outage |
| [Tool Usage Constraints](#tool-usage-constraints) | T3 tier boundary, citation requirements |
| [References](#references) | Source document traceability |

---

## Context7 Usage for Lean UX

Per MCP-001 (`.context/rules/mcp-tool-standards.md` v1.3.1 [Context7 Integration]): Context7 MUST be used when the facilitation references an external Lean UX library, framework, or experiment methodology by name. The `ux-lean-ux-facilitator` agent is T3 (External) and has `mcp__context7__resolve-library-id` and `mcp__context7__query-docs` in its allowed tools.

**Operational state:** Context7 queries are available NOW in stub mode for Lean UX methodology research (hypothesis format references, assumption mapping framework documentation, experiment design pattern lookup). The protocol defined in this runbook governs the agent in both stub mode and post-Wave-2-deployment. Post-deployment, Context7 additionally supports live experiment data lookup when experiment frameworks are referenced by name during active facilitation cycles. See `skills/user-experience/rules/wave-progression.md` [Wave 2 Deployment Criteria] for deployment timeline tracking.

**Note:** The parent `mcp-coordination.md` [Context7 Usage] agent table should include `ux-lean-ux-facilitator` upon Wave 2 deployment. Tracked in `skills/user-experience/rules/wave-progression.md` [Wave 2 Deployment Criteria]. The authoritative tool declaration is in the agent definition frontmatter (`skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md`).

### Protocol

1. Call `mcp__context7__resolve-library-id` with the library/framework name and the research question.
2. Call `mcp__context7__query-docs` with the resolved library ID and a specific query.
3. Respect the per-question call limit enforced by the tool; each distinct library resets the limit.
4. If `resolve-library-id` returns no matches, fall back to WebSearch for that library.

### When to Use Context7 During Facilitation

| Facilitation Step | Context7 Trigger | Example Query |
|-------------------|-----------------|---------------|
| Hypothesis Formulation | Referencing the canonical Lean UX hypothesis format or structure | `resolve: "Lean UX"` then `query: "hypothesis format we believe outcome for users if change"` |
| Assumption Mapping | Looking up Lean UX assumption categorization methodology | `resolve: "Lean UX"` then `query: "assumption mapping four quadrant framework risk knowledge"` |
| ICE Scoring | Referencing ICE prioritization framework details (Sean Ellis / GrowthHackers, circa 2015) | `resolve: "Lean UX"` then `query: "ICE scoring impact confidence ease hypothesis prioritization"` (Context7 indexes software libraries, not product management content; ICE queries may fall back to WebSearch per MCP-001. WebSearch fallback query: `"ICE scoring framework impact confidence ease" site:growthhackers.com OR site:itamargilad.com`; cite source URL per citation rule 3.) |
| Experiment Design (A/B testing) | Looking up A/B testing statistical methodology or framework patterns | `resolve: "Optimizely"` then `query: "A/B test sample size calculation statistical significance"` |
| Experiment Design (general) | Referencing experiment design patterns from testing frameworks | `resolve: "Google Optimize"` then `query: "experiment configuration metric setup goals"` (Google Optimize was discontinued Sept 2023; Context7 may return no results. Fall back to WebSearch per MCP-001. WebSearch fallback query: `"Google Analytics 4 experiment configuration goals metrics" site:support.google.com OR "VWO experiment setup"` -- GA4 Experiments and VWO are current replacements; cite source URL per citation rule 3.) |
| Build-Measure-Learn Cycle | Referencing Lean UX iteration methodology details | `resolve: "Lean UX"` then `query: "build measure learn cycle iteration pivot persevere"` |
| Validated Learning Documentation | Looking up learning log structure and decision frameworks | `resolve: "Lean UX"` then `query: "validated learning documentation outcomes evidence"` |

### When NOT to Use Context7

| Scenario | Alternative |
|----------|-------------|
| General hypothesis-driven design concepts already in facilitator knowledge | No tool call needed |
| Codebase-internal product code inspection for experiment context | Read/Grep the codebase |
| Prior experiment results or hypothesis backlog from this engagement | Read the engagement output files |
| Context7 already queried for the same library in this engagement | Reuse prior results; respect call limit |
| General business or product strategy concepts | WebSearch |

### When to Query Context7 in the Build-Measure-Learn Workflow

This subsection maps Context7 invocation to the Build-Measure-Learn cycle defined in SKILL.md [Methodology]. Context7 calls are made on-demand at specific phases, not front-loaded as a preparation phase.

| Workflow Phase | Context7 Action | Rationale |
|----------------|----------------|-----------|
| Hypothesis Formulation (pre-cycle) | Query for Lean UX hypothesis format specifics when structuring a new hypothesis that references a named methodology or framework. WebSearch escalation: if Context7 returns no results, search `"Lean UX hypothesis format we believe that"`. | Ensures hypothesis statements follow the canonical Lean UX format; query when the facilitator cites Gothelf & Seiden's methodology by name |
| Assumption Mapping (pre-cycle) | Query for assumption categorization methodology when mapping assumptions into the 4-quadrant framework and the team references Lean UX assumption types (value/usability/feasibility) by name. WebSearch escalation: if Context7 returns no results, search `"Lean UX assumption mapping quadrant risk knowledge"`. | On-demand invocation minimizes unnecessary tool calls; query when the mapping cites Lean UX methodology for quadrant assignment criteria |
| Phase 1 (Build) | Query for experiment design patterns when the selected experiment type references a named A/B testing framework or statistical methodology. WebSearch escalation: if Context7 returns no results for the named framework, search `"{framework name} experiment configuration setup"`. | Ensures experiment designs follow established patterns; query when the facilitator cites a specific testing framework (e.g., Optimizely, LaunchDarkly) for configuration guidance |
| Phase 2 (Measure) | Query for statistical significance or sample size methodology when the experiment references a named statistical framework or testing library. WebSearch escalation: if Context7 returns no results, search `"{framework name} sample size calculator statistical significance"`. | Used when measurement requires specific statistical methodology beyond the facilitator's built-in knowledge |
| Phase 3 (Learn) | No Context7 needed | Learning analysis operates on the experiment's own data and the facilitator's built-in Lean UX knowledge; no external reference required |
| Phase 4 (Iterate) | No Context7 needed | Pivot/persevere/kill decisions are applied from the facilitator's built-in Lean UX knowledge against the validated learning data |

---

## Miro MCP Dependency

### Current Status

**Miro MCP adapter: UNAVAILABLE.** Adapter implementation is post-PROJ-022 scope (see `projects/PROJ-022-user-experience-skill/PLAN.md` [Context]). The `/ux-lean-ux` sub-skill has Miro classified as **REQ** in the parent MCP dependency matrix (`skills/user-experience/rules/mcp-coordination.md` [MCP Dependency Matrix]).

### Fallback Mode

The sub-skill operates in **text-based exercise mode** when Miro is unavailable. The facilitation methodology remains identical; only the output modality changes. See [Text-Based Exercise Mode Protocol](#text-based-exercise-mode-protocol) for operational details.

### What Changes When Miro Becomes Available

When the Miro MCP adapter is implemented and the orchestrator's MCP availability detection succeeds (probe protocol defined in `skills/user-experience/rules/mcp-coordination.md` [MCP Availability Detection]):

| Capability | Text-Based Exercise Mode (current) | Miro MCP Mode (future) |
|------------|-------------------------------------|------------------------|
| Assumption mapping visualization | Structured markdown tables with quadrant assignments | Interactive Miro board with drag-and-drop quadrant positioning |
| Hypothesis backlog visualization | Markdown tables with status columns | Visual Miro board with card-based hypothesis tracking |
| Assumption movement tracking | Text-based status updates noting quadrant changes | Visual movement between quadrants on the board as evidence accumulates |
| Build-Measure-Learn cycle tracking | Markdown timeline with phase status | Visual cycle board with experiment cards linked to hypothesis cards |
| Collaborative workshop exercises | Text descriptions of exercises with structured outputs | Real-time collaborative board creation and facilitation |
| Experiment results embedding | Results documented inline in markdown tables | Results attached to hypothesis cards alongside visual boards |

The agent definition frontmatter and governance file will need updating when Miro MCP becomes available to add the Miro MCP tool to `tools` and update the tool tier if necessary.

---

## Text-Based Exercise Mode Protocol

This section defines how the `ux-lean-ux-facilitator` agent produces outputs when the Miro MCP adapter is unavailable (current default).

### Structured Markdown Equivalents

When Miro is unavailable, all visual board outputs are produced as structured markdown:

| Miro Board Type | Text-Based Equivalent | Format |
|-----------------|----------------------|--------|
| Assumption Map Board | 4-quadrant markdown table | Table with columns: Assumption ID, Description, Category (value/usability/feasibility), Quadrant (Q1-Q4), Risk Level, Evidence Status |
| Hypothesis Backlog Board | Hypothesis backlog markdown table | Table with columns: HYP-ID, Lean UX Format Statement, Status (DRAFT/ACTIVE/VALIDATED/INVALIDATED/DEFERRED), ICE Score, Linked Experiment, Quadrant |
| Build-Measure-Learn Cycle Board | Cycle tracking markdown sections | Per-cycle section with Phase, Status, Duration, Key Metrics, Decision |
| Experiment Design Board | Experiment design markdown template | Structured sections per experiment: Type, Description, Duration, Sample Size, Success Criteria, Measurement Method |
| Workshop Exercise Board | Exercise output as structured markdown | Numbered steps with participant inputs, outputs, and decisions documented textually |

### Example: Text-Based Assumption Map

```markdown
### Assumption Map -- {engagement topic}

| ID | Assumption | Category | Quadrant | Risk | Evidence |
|----|-----------|----------|----------|------|----------|
| A-001 | Users want single-page checkout | Value | Q1 (Unknown + High Risk) | HIGH | No prior data |
| A-002 | Users can complete checkout in < 2 min | Usability | Q2 (Known + High Risk) | HIGH | Heuristic eval found 3 navigation issues |
| A-003 | Mobile payment API supports our flow | Feasibility | Q3 (Known + Low Risk) | LOW | API docs confirmed |
| A-004 | Users prefer guest checkout | Value | Q4 (Unknown + Low Risk) | LOW | Anecdotal reports only |
```

### Limitations of Text-Based Exercise Mode

The following limitations MUST be disclosed in the output per P-022. The degraded mode banner (defined in `skills/user-experience/rules/mcp-coordination.md` [Degraded Mode Disclosure]) MUST appear at the top of the facilitation output:

```
[DEGRADED MODE] This output was produced without Miro MCP access.
Input was provided via text-based exercise mode. Some features are reduced:
- Cannot create or update collaborative visual boards
- Cannot visualize assumption movement between quadrants over time
- Cannot embed experiment results alongside visual hypothesis boards
```

Notify the user of text-based exercise mode status at facilitation start (before producing outputs), not only in the output report, per P-022 (no deception about capabilities) -- users must know the facilitation operates without collaborative board functionality.

**Artifact-specific limitations in text-based mode:**

| Artifact Type | Limitation | Impact on Output Quality |
|---------------|-----------|--------------------------|
| Assumption Map | Cannot visualize spatial positioning or drag-and-drop movement between quadrants | MEDIUM: quadrant assignments are documented but spatial relationships and movement over time are less intuitive in table format |
| Hypothesis Backlog | Cannot provide card-based visual overview of hypothesis portfolio | LOW: table format conveys all information; visual card layout is a convenience, not a data gap |
| Build-Measure-Learn Cycle Board | Cannot show cycle progression as a visual timeline with linked cards | LOW: markdown sections capture all cycle data; timeline visualization is a convenience enhancement |
| Workshop Exercises | Cannot support real-time collaborative editing or voting on shared boards | HIGH: collaborative exercises lose real-time multi-participant interaction; text-based mode is sequential, not concurrent |
| Experiment Results | Cannot embed results alongside hypothesis cards on visual boards | LOW: results are documented in validated learning log entries; visual proximity to hypotheses is a convenience |

> **Impact rating attribution:** Impact ratings are defined as: HIGH = core collaborative functionality unavailable; MEDIUM = information conveyed but with reduced intuitiveness or spatial context; LOW = all information present, visual enhancement only. These are editorial assessments specific to text-based exercise mode. P-022 disclosure: these ratings reflect facilitator judgment about text-mode limitations, not empirical measurement.

---

## MCP Failure Handling

### Context7 Unavailable

Per `mcp-tool-standards.md` v1.3.1 [Error Handling]:

| Failure Condition | Fallback Action |
|-------------------|----------------|
| `resolve-library-id` returns no matches | Fall back to WebSearch for that library. Note "Context7 no coverage" in the facilitation output next to the affected finding. |
| `query-docs` returns empty or irrelevant results | Use WebSearch for the specific query. Note "Context7 no coverage" in the facilitation output. |
| Context7 tool-enforced call limit reached | Fall back to WebSearch for remaining queries for that library. |
| Context7 MCP server timeout (> 5 seconds with no response) or error | Continue facilitation without Context7. Use WebSearch for all external documentation lookups. Note the MCP outage in the facilitation report metadata. One retry attempted before declaring unavailable, per `mcp-coordination.md` [MCP Availability Detection] detection protocol. |

### Full MCP Server Outage

When the MCP server is completely unavailable (detected by the orchestrator's probe protocol per `skills/user-experience/rules/mcp-coordination.md` [MCP Availability Detection]):

1. **Continue facilitation.** The Lean UX methodology does not depend on MCP for core functionality. Build-Measure-Learn cycles, hypothesis formulation, assumption mapping, and experiment design are applied from the facilitator's built-in knowledge of Gothelf & Seiden's methodology.
2. **Use WebSearch as fallback** for any external documentation lookups (Lean UX methodology details, A/B testing frameworks, statistical significance references, experiment design patterns).
3. **Disclose in output** per P-022: note that MCP tools were unavailable and external references were sourced via web search.
4. **No blocking.** MCP outage does not block facilitation execution. The facilitation proceeds with reduced reference precision but identical methodology.

### Miro Unavailable (Current Default)

Since the Miro MCP adapter is not yet implemented, the Miro-unavailable state is the current default. No dynamic detection is needed; the facilitator always operates in text-based exercise mode.

When the Miro MCP adapter becomes available in the future and subsequently fails:

1. **Detect failure** via the orchestrator's Miro probe (defined in `mcp-coordination.md` [Future MCP Probes]).
2. **Fall back to text-based exercise mode** per [Text-Based Exercise Mode Protocol](#text-based-exercise-mode-protocol).
3. **Disclose degraded mode** per P-022 using the banner defined in [Limitations of Text-Based Exercise Mode](#limitations-of-text-based-exercise-mode).
4. **No blocking.** Miro outage does not block facilitation execution. Assumption maps and hypothesis backlogs are produced as structured markdown.

---

## Tool Usage Constraints

### Tool Tier

The `ux-lean-ux-facilitator` agent operates at **T3 (External)** per `agent-development-standards.md` v1.2.0 [Tool Security Tiers]. This tier includes:

- **T1 (Read-Only):** Read, Glob, Grep
- **T2 (Read-Write):** T1 + Write, Edit, Bash
- **T3 (External):** T2 + WebSearch, WebFetch, Context7 (`mcp__context7__resolve-library-id`, `mcp__context7__query-docs`)

> **Note:** The tier breakdown above reflects the cumulative T3 tier model from `agent-development-standards.md` v1.2.0 [Tool Security Tiers]. The `ux-lean-ux-facilitator` agent excludes Bash from its actual tool set -- Bash is not required for Lean UX facilitation and is omitted from the agent definition frontmatter (`skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md` `tools` field). The SKILL.md `allowed-tools` field (v1.2.0) confirms the same exclusion. The agent definition frontmatter is the authoritative tool declaration per H-34; actual tool availability is governed by that frontmatter, not the cumulative tier model.

### Prohibited Tools

| Tool | Reason |
|------|--------|
| Agent | Worker agent; P-003 prohibition. `disallowedTools: [Agent]` in agent frontmatter. |
| Memory-Keeper | No cross-session state requirement. Sub-skill state is engagement-scoped per P-002. All output persisted to `skills/ux-lean-ux/output/{engagement-id}/`. |

### Citation Requirements

Per T3 tier constraints (`agent-development-standards.md` v1.2.0 [Tier Constraints]: "T3+ agents MUST declare citation guardrails"):

1. All external data referenced in outputs MUST include a citation (source name, document title, or URL).
2. Context7-sourced references MUST note the library and query used.
3. WebSearch-sourced references MUST include the URL.
4. Findings based solely on the facilitator's Lean UX methodology knowledge (no external lookup) do not require external citation but MUST reference the specific methodology component (e.g., "Gothelf & Seiden, 2021, Chapter 4: Assumptions" or "ICE scoring framework").

---

## References

| Source | Content | Path |
|--------|---------|------|
| Parent MCP coordination | MCP dependency matrix, degraded mode disclosure, Miro risk profile, Context7 usage mapping | `skills/user-experience/rules/mcp-coordination.md` (v1.2.0) |
| Framework MCP standards | MCP-001 Context7 governance, MCP-002 Memory-Keeper governance, canonical tool names, error handling | `.context/rules/mcp-tool-standards.md` (v1.3.1) |
| Sub-skill specification | Lean UX methodology, Build-Measure-Learn cycle, output specification, MCP dependencies | `skills/ux-lean-ux/SKILL.md` (v1.2.0) |
| ORCHESTRATION.yaml | Orchestration plan governing the build sequence for this sub-skill (schema v3.0.0, created 2026-03-03) | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |
| PLAN.md | MCP adapter scope and post-PROJ-022 roadmap context (created 2026-03-03) | `projects/PROJ-022-user-experience-skill/PLAN.md` [Context] |
| Wave progression rules | Wave deployment criteria, Wave 2 entry requirements, signoff enforcement | `skills/user-experience/rules/wave-progression.md` |
| Lean UX methodology source | Build-Measure-Learn cycle foundation, hypothesis format, assumption mapping framework | Gothelf, J. & Seiden, J. (2021). *Lean UX* (3rd ed.). O'Reilly. See also `skills/ux-lean-ux/SKILL.md` References. |

---

<!-- GOVERNANCE ID INDEX: MCP-001 (Context7 MUST-use), P-002 (engagement-scoped persistence), P-022 (degraded mode disclosure), H-34 (agent definition schema validation), AD-M-006 (persona governance), T3 citation guardrails (agent-development-standards.md Tier Constraints) -->

*Runbook: mcp-runbook.md (v1.2.0)*
*Sub-skill: `/ux-lean-ux`*
*Parent skill: `/user-experience`*
*Parent MCP coordination: `skills/user-experience/rules/mcp-coordination.md`*
*MCP governance SSOT: `.context/rules/mcp-tool-standards.md` (MCP-001)*
*Agent: `ux-lean-ux-facilitator` (T3, Systematic, Sonnet)*
*Project: PROJ-022 User Experience Skill*
*Created: 2026-03-04*
*Revised: 2026-03-04 (v1.2.0 -- iter2 quality gate revisions: Gothelf & Seiden References entry, T2 tier SSOT alignment with Bash, Google Optimize WebSearch fallback query, stub agent operational state clarification)*
