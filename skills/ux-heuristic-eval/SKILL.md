---
name: ux-heuristic-eval
description: "Nielsen heuristic evaluation sub-skill for the /user-experience parent skill. Evaluates interfaces against Nielsen's 10 usability heuristics, produces severity-rated findings on a 0-4 scale (Cosmetic to Catastrophic), and generates remediation recommendations with effort estimates. Invoke when teams need structured usability evaluation, interface review, heuristic audit, or severity-rated UX findings. Invoked by ux-orchestrator during Wave 1 lifecycle-stage routing or CRISIS mode triage. Triggers: heuristic evaluation, usability audit, Nielsen heuristics, interface review, severity rating, usability inspection, UX evaluation."
version: "1.0.0"
agents:
  - ux-heuristic-evaluator
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
activation-keywords:
  - "heuristic evaluation"
  - "usability audit"
  - "Nielsen heuristics"
  - "interface review"
  - "severity rating"
  - "usability inspection"
  - "UX evaluation"
  - "heuristic audit"
---

<!-- VERSION: 1.0.0 | DATE: 2026-03-04 | SOURCE: skills/user-experience/SKILL.md | PARENT: /user-experience skill -->

# Heuristic Evaluation Sub-Skill

> **Version:** 1.0.0
> **Framework:** Jerry User-Experience -- Heuristic Evaluation
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Parent Skill:** `/user-experience` (`skills/user-experience/SKILL.md`)
> **Wave:** 1 (Zero-Dependency)
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
| [Methodology](#methodology) | Nielsen's 10 heuristics, severity scale, evaluation workflow, single-evaluator reliability |
| [MCP Dependencies](#mcp-dependencies) | Figma REQ with screenshot-input fallback; Context7 for UX docs |
| [Output Specification](#output-specification) | Output location, L0/L1/L2 structure, required sections |
| [Routing](#routing) | Keywords and lifecycle-stage routing integration |
| [Cross-Framework Integration](#cross-framework-integration) | Handoff to Behavior Design, HEART Metrics, and CRISIS mode |
| [Synthesis Hypothesis Confidence](#synthesis-hypothesis-confidence) | Confidence classifications for heuristic evaluation outputs |
| [Constitutional Compliance](#constitutional-compliance) | Governing principles |
| [Registration](#registration) | H-26(c) parent-routed registration model and AGENTS.md confirmation |
| [Deployment Status](#deployment-status) | Wave 1 stub agent status and implementation timeline |
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

The Heuristic Evaluation sub-skill provides structured, evidence-based usability evaluation using Nielsen's 10 usability heuristics. It targets tiny teams (1-5 people) who lack dedicated UX evaluators by providing AI-augmented systematic interface inspection with severity-rated findings and actionable remediation recommendations.

This sub-skill is part of Wave 1 (Zero-Dependency), meaning it requires no prior wave completions and operates with minimal infrastructure. It is the foundation evaluation framework that other sub-skills build upon.

### Key Capabilities

- **Systematic Heuristic Inspection** -- Evaluates interfaces against all 10 of Nielsen's usability heuristics sequentially, ensuring complete coverage
- **Severity-Rated Findings** -- Each finding receives a 0-4 severity rating per Nielsen's severity taxonomy (Not a problem to Usability catastrophe) with evidence from the interface
- **Remediation Recommendations** -- Actionable fix suggestions with effort estimates (Low/Medium/High) for each finding
- **Multi-Screen Evaluation** -- Coordinates evaluation across multiple screens or flows with finding deduplication
- **Model Escalation** -- Default Haiku for high-volume checklist evaluation; auto-escalates to Sonnet for complex evaluations
- **Cross-Framework Feed** -- Findings feed directly into Behavior Design diagnosis and HEART Metrics measurement

> **Source:** Key capabilities derived from parent SKILL.md [Key Capabilities] (line 103: "Heuristic Evaluation -- Nielsen's 10 Heuristics with severity-rated findings (Wave 1)") and [Available Agents] (lines 152, 165).

---

## When to Use This Sub-Skill

Activate when:

- Evaluating an existing interface against established usability principles
- Conducting a structured usability audit with severity-rated findings
- Reviewing interface design quality during the "During design" lifecycle stage
- Performing interface review as part of a comprehensive UX audit (multi-sub-skill route with HEART Metrics)
- Executing CRISIS mode step 1 (identify UX issues via Nielsen's 10 heuristics)
- Evaluating AI product interfaces as an interim path when the AI-First Design sub-skill is not yet deployed
- Needing a baseline usability assessment before deeper behavioral or metrics analysis

Do NOT use for:

- Diagnosing why users fail to take a specific action -- use `/ux-behavior-design` (Fogg B=MAP) instead. Heuristic evaluation identifies design-level issues but does not trace behavioral root causes.
- Measuring quantitative UX health metrics -- use `/ux-heart-metrics` (Google GSM) instead. Heuristic evaluation produces qualitative findings, not metric baselines.
- Accessibility-specific compliance auditing -- use `/ux-inclusive-design` (WCAG 2.2) instead. Heuristic evaluation covers general usability; dedicated accessibility evaluation requires WCAG success criteria.
- Testing hypotheses about design changes -- use `/ux-lean-ux` (Lean UX) instead. Heuristic evaluation assesses existing interfaces, not hypothesis-driven experiments.
- Security-focused interface review -- use `/eng-team` instead. Heuristic evaluation applies usability principles, not security threat models.
- General research without UX evaluation focus -- use `/problem-solving` instead.

> **Source:** Routing logic derived from parent SKILL.md [Lifecycle-Stage Routing] (lines 295-334) and `skills/user-experience/rules/ux-routing-rules.md` [Stage Routing Table], [Common Intent Resolution].

---

## Available Agents

| Agent | Role | Tier | Mode | Model | Output Location |
|-------|------|------|------|-------|-----------------|
| `ux-heuristic-evaluator`** | Nielsen heuristic evaluation specialist | T4 | Systematic | Haiku* | `skills/ux-heuristic-eval/output/{engagement-id}/ux-heuristic-evaluator-{topic-slug}.md` |

*Haiku for high-volume checklist evaluation; escalates to Sonnet when: (1) critical finding count >= 3 (severity 3 or 4), (2) Figma MCP benchmark fails pre-launch threshold, or (3) evaluation spans > 50 screens. Escalation is automatic within the orchestrator's routing logic per AD-M-009 model selection justification.

**STUB: The agent definition file (`skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md`) currently contains frontmatter, identity, purpose, and guardrails sections only. Full agent body implementation (`<input>`, `<capabilities>`, `<methodology>`, `<output>` sections) is pending Wave 1 completion of PROJ-022 EPIC-002. The SKILL.md specifies the methodology and output contract that the agent will implement.

**Tool tier:** T4 (External) = Read, Write, Edit, Glob, Grep + WebSearch, WebFetch + Context7 MCP. The T4 tier enables access to external UX standards documentation via Context7 and web search. Bash is intentionally excluded; T4 tier does not require shell access for MCP operations. See `agent-development-standards.md` [Tool Security Tiers] for full tier definitions.

The agent produces output at three levels per AD-M-004:
- **L0 (Executive Summary):** Top 3-5 findings with severity ratings for stakeholders and cross-framework synthesis input.
- **L1 (Technical Detail):** Full evaluation of all 10 heuristics with per-finding evidence, severity rating, affected screens, and remediation recommendations.
- **L2 (Strategic Implications):** Cross-product usability patterns, organizational UX recommendations, and design evolution trajectory.

> **Source:** Agent specification from parent SKILL.md [Available Agents] (line 152) and agent stub at `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md`.

---

## P-003 Compliance

The `/ux-heuristic-eval` sub-skill contains a single **worker** agent. It is invoked by the `ux-orchestrator` (T5) via the Agent tool. The agent does NOT have Agent tool access and MUST NOT spawn sub-agents.

```
MAIN CONTEXT (user request)
    |
    v
ux-orchestrator (T5, Opus, Integrative) -- parent orchestrator
    |
    +-- ux-heuristic-evaluator (T4, Systematic, Haiku) -- THIS sub-skill's worker
    +-- [other sub-skill workers...]
```

**Enforcement:**
- `disallowedTools: [Agent]` declared in `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md` frontmatter
- P-003 prohibition in `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.governance.yaml` `capabilities.forbidden_actions`
- CI gate validates no sub-skill agent has Agent access (documented in `skills/user-experience/rules/ci-checks.md`)

> **Source:** P-003 hierarchy from parent SKILL.md [P-003 Compliance] (lines 174-196).

---

## Invoking the Agent

This is a sub-skill invoked by the `ux-orchestrator`, not directly by users. Users interact with the parent `/user-experience` skill, which routes to this sub-skill based on lifecycle-stage triage.

### Via Natural Language (to parent skill)

```
"Evaluate this dashboard design against Nielsen's heuristics"
"Run a usability audit on the settings page"
"Check this interface for usability issues"
```

The `ux-orchestrator` routes these requests to `ux-heuristic-evaluator` based on the [Stage Routing Table] in `skills/user-experience/rules/ux-routing-rules.md`.

### Via Explicit Agent Request (to parent skill)

```
"Use ux-heuristic-evaluator to audit the navigation patterns"
"Have ux-heuristic-evaluator evaluate the form design"
```

### Via Agent Tool (orchestrator internal)

The `ux-orchestrator` invokes the agent via the Agent tool:

```python
Agent(
    description="ux-heuristic-evaluator: Heuristic evaluation of settings page",
    subagent_type="jerry:ux-heuristic-evaluator",
    prompt="""
## UX CONTEXT (REQUIRED)
- **Engagement ID:** UX-0001
- **Topic:** Settings Page Heuristic Evaluation
- **Product:** [product name and domain]
- **Target Users:** [user description]
- **Input:** [screenshots, Figma link, or interface description]

## TASK
Perform a Nielsen heuristic evaluation of the settings page.
Evaluate all 10 heuristics. Rate severity 0-4 for each finding.
Produce ranked findings with remediation recommendations.

## MANDATORY PERSISTENCE (P-002)
Create file at: skills/ux-heuristic-eval/output/UX-0001/ux-heuristic-evaluator-settings-page.md
"""
)
```

> **Governance codification (AD-M-007):** The session_context contract (on_receive/on_send) is specified in `ux-heuristic-evaluator.governance.yaml` per AD-M-007. The on_receive steps validate engagement ID, product context, and prior evaluation findings. The on_send steps include severity-rated findings, heuristic coverage summary, and remediation recommendations.

> **Source:** Invocation pattern from parent SKILL.md [Invoking an Agent] (lines 200-250).

---

## Methodology

### Nielsen's 10 Usability Heuristics

The evaluation systematically applies each of Nielsen's 10 heuristics to every screen or flow under review. Each heuristic is evaluated independently to ensure complete coverage.

| # | Heuristic | Description | Evaluation Focus |
|---|-----------|-------------|------------------|
| H1 | **Visibility of System Status** | The system should keep users informed about what is going on through appropriate feedback within reasonable time | Loading indicators, progress bars, state changes, confirmation messages |
| H2 | **Match Between System and Real World** | The system should speak the users' language with words, phrases, and concepts familiar to the user | Terminology, metaphors, information ordering, cultural conventions |
| H3 | **User Control and Freedom** | Users often perform actions by mistake and need a clearly marked "emergency exit" to leave the unwanted state | Undo/redo, cancel actions, navigation back, escape routes |
| H4 | **Consistency and Standards** | Users should not have to wonder whether different words, situations, or actions mean the same thing | Internal consistency, platform conventions, industry standards |
| H5 | **Error Prevention** | Even better than good error messages is a careful design that prevents problems from occurring in the first place | Constraints, confirmations, defaults, input validation |
| H6 | **Recognition Rather Than Recall** | Minimize the user's memory load by making objects, actions, and options visible | Visible options, contextual help, recognizable patterns |
| H7 | **Flexibility and Efficiency of Use** | Accelerators may speed up interaction for expert users while remaining invisible to novice users | Shortcuts, customization, adaptive interfaces |
| H8 | **Aesthetic and Minimalist Design** | Dialogues should not contain information that is irrelevant or rarely needed | Visual clutter, information hierarchy, content prioritization |
| H9 | **Help Users Recognize, Diagnose, and Recover from Errors** | Error messages should be expressed in plain language, precisely indicate the problem, and constructively suggest a solution | Error message clarity, recovery guidance, actionable feedback |
| H10 | **Help and Documentation** | It may be necessary to provide help and documentation, focused on the user's task, listing concrete steps | Contextual help, documentation accessibility, task-oriented guidance |

> **Source:** Jakob Nielsen, "10 Usability Heuristics for User Interface Design" (1994, revised 2020). Nielsen Norman Group. Referenced in agent stub `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md` [identity/expertise] and parent SKILL.md [Key Capabilities] (line 103).

### Severity Rating Scale

Each finding receives a severity rating on the 0-4 scale. Severity determines remediation priority and influences cross-framework handoff decisions.

| Severity | Name | Definition | Remediation Priority |
|----------|------|------------|---------------------|
| **0** | Not a usability problem | No usability impact identified; does not need to be fixed | No action required |
| **1** | Cosmetic problem only | Cosmetic issue that need not be fixed unless extra time is available | Fix only if extra time is available |
| **2** | Minor usability problem | Users experience minor difficulty; low-priority fix | Low priority; fix in future release |
| **3** | Major usability problem | Significant usability problem; important to fix, high priority | High priority; important to fix |
| **4** | Usability catastrophe | Imperative to fix before product release; prevents task completion | Must fix before release |

**Cross-framework threshold:** Findings with severity >= 2 (Minor usability problem or higher) are included in handoffs to downstream sub-skills (Behavior Design, HEART Metrics). Findings with severity 0-1 (Not a problem, Cosmetic only) are included in the full report but not propagated to cross-framework handoffs unless specifically requested.

> **Source:** Severity scale from Jakob Nielsen, "Severity Ratings for Usability Problems" (1994). Referenced in agent governance file `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.governance.yaml` [output_filtering: all_findings_must_have_severity_rating] and parent SKILL.md [Available Agents] footnote (line 165: "severity-rated findings").

### Evaluation Workflow

The evaluation follows a 5-step systematic workflow.

| Step | Name | Input | Output | Validation |
|------|------|-------|--------|------------|
| 1 | **Input Collection** | Interface screenshots, Figma reference, or text description | Organized screen/flow inventory with input modality noted | At least one interface artifact provided; degraded mode disclosed if no Figma |
| 2 | **Systematic Evaluation** | Screen inventory + 10 heuristics checklist | Per-heuristic findings for each screen | All 10 heuristics evaluated for each screen; no heuristic skipped |
| 3 | **Severity Rating** | Raw findings | Severity-rated findings (0-4) with evidence | Every finding has a severity rating and specific interface evidence |
| 4 | **Deduplication and Ranking** | All severity-rated findings across screens | Deduplicated, ranked findings list | Duplicate findings across screens consolidated; ranked by severity descending |
| 5 | **Report Generation** | Ranked findings | L0/L1/L2 output artifact | Persisted to output location per P-002; all required sections present |

**Evaluation scope (Step 2):** The evaluator operates in one of two modes depending on the request:
- **Screen-level evaluation:** Individual screen assessed against all 10 heuristics. Use for detailed single-screen audits. A "screen" is any distinct view, state, or flow step that presents a unique interface to the user (e.g., a 5-step checkout wizard counts as 5 screens; a modal dialog counts as a separate screen from its parent view).
- **Flow-level evaluation:** Multi-screen user journey evaluated for heuristic violations across transitions. Use for task-completion analysis where cross-screen consistency and navigation continuity matter.
- **Default:** Screen-level for requests mentioning specific screens; flow-level for requests mentioning user tasks or journeys.

**Per-screen evaluation pattern:** For each screen or flow, the evaluator applies all 10 heuristics sequentially (H1 through H10). This systematic approach prevents the common evaluation bias of focusing only on obvious problems while missing less salient but equally important heuristic violations.

**AI-interaction heuristic supplement:** When the orchestrator routes to this sub-skill for AI product evaluation (lifecycle stage "During design: Building AI product" with AI-First Design enabler not completed), the evaluator supplements Nielsen's 10 with three additional AI interaction heuristics: (a) Transparency -- is the AI's decision-making process visible to the user? (b) Controllability -- can the user override, correct, or guide the AI? (c) Error Recovery -- can the user recover when the AI produces incorrect output? These supplementary heuristics are marked as `[AI-SUPPLEMENT]` in the findings to distinguish them from Nielsen's core 10.

> **Source:** AI-interaction supplement from parent SKILL.md [Lifecycle-Stage Routing] (line 312-313: "PAIR (interim)" defined as heuristic evaluation with AI-specific supplementary heuristics). Detailed routing logic in `skills/user-experience/rules/ux-routing-rules.md` [Stage Routing Table] "During design: Building AI product" row.

### Single-Evaluator Reliability Note

Nielsen's heuristic evaluation methodology recommends 3-5 independent evaluators for reliable usability problem detection. Research shows that individual evaluators typically find only 35% of usability problems, with the aggregate across 3-5 evaluators reaching 75-80% coverage (Nielsen, 1994c).

This sub-skill operates with a single AI evaluator. The AI evaluator compensates for the single-evaluator limitation through systematic heuristic coverage: it applies all 10 heuristics sequentially to every screen, eliminating the heuristic omission bias that human evaluators commonly exhibit (where individual evaluators unconsciously focus on a subset of heuristics aligned with their expertise). This systematic approach ensures no heuristic is skipped, which is the primary source of coverage loss in single-human-evaluator assessments.

**Acknowledged limitation (P-022):** A single AI evaluator cannot replicate the perspective diversity that multiple human evaluators provide. Context-specific usability issues -- those requiring domain expertise, cultural familiarity, or embodied interaction experience -- may be missed by AI evaluation alone. The AI evaluator may also exhibit systematic blind spots (e.g., overweighting visual design heuristics when evaluating from screenshots vs. underweighting interaction flow heuristics that require hands-on use).

**Recommendation for high-stakes evaluations:** For findings rated severity 3 (Major usability problem) or severity 4 (Usability catastrophe), supplement the AI evaluation with at least one human evaluator review before making major design decisions. This is especially important when: (a) the product serves specialized user populations, (b) findings will drive significant engineering investment, or (c) the evaluation was conducted in screenshot-input degraded mode without interactive observation.

---

## MCP Dependencies

### Dependency Matrix

| MCP Tool | Classification | Purpose | Fallback |
|----------|---------------|---------|----------|
| **Figma** | **REQ** | Inspect design layers, component states, responsive behavior, style tokens | Screenshot-input mode: user provides design screenshots as image inputs |
| **Storybook** | ENH | Browse live component stories for evaluation context | Manual component inventory: user provides component list and documentation links |
| **Context7** | Available (current infrastructure) | Resolve and query UX framework documentation (Nielsen Norman Group, WCAG references) | WebSearch fallback per MCP-001 (`mcp-tool-standards.md` [Error Handling]) |

### Figma Fallback: Screenshot-Input Mode

When the Figma MCP adapter is unavailable (current state -- adapter implementation is post-PROJ-022 scope), the evaluator operates in screenshot-input mode:

- Users provide design screenshots as image inputs or paste text descriptions of the interface
- The evaluation methodology remains identical; only the input modality changes
- **Limitations in screenshot-input mode:**
  - Cannot inspect component states (hover, focus, active, disabled)
  - Cannot verify responsive behavior across breakpoints
  - Cannot access style tokens or design system variables programmatically
- Output carries a degraded mode disclosure per P-022:
  ```
  [DEGRADED MODE] This evaluation was produced without Figma MCP access.
  Input was provided via screenshot-input mode. Some features are reduced:
  - Cannot inspect component states (hover, focus, active, disabled)
  - Cannot verify responsive behavior across breakpoints
  - Cannot access style tokens or design system variables programmatically
  ```

### Context7 Usage

Per MCP-001 (`.context/rules/mcp-tool-standards.md` [Context7 Integration]), Context7 is used when the evaluation references external UX frameworks or standards by name:

| Library/Framework | Usage |
|-------------------|-------|
| Nielsen Norman Group | Heuristic definitions, severity scale reference, evaluation methodology |
| WCAG 2.2 | Accessibility-adjacent heuristic evaluation (H10: Help and Documentation) |
| Material Design / platform guidelines | H4: Consistency and Standards -- platform convention references |

Protocol: call `mcp__context7__resolve-library-id` with the framework name, then `mcp__context7__query-docs` with the resolved ID and specific query. If Context7 returns no results, fall back to WebSearch per `mcp-tool-standards.md` [Error Handling].

> **Source:** MCP dependency matrix from parent SKILL.md [MCP Integration Architecture] (line 402: `/ux-heuristic-eval` row) and `skills/user-experience/rules/mcp-coordination.md` [MCP Dependency Matrix], [Figma Dependency Risk Profile].

---

## Output Specification

### Output Location

```
skills/ux-heuristic-eval/output/{engagement-id}/ux-heuristic-evaluator-{topic-slug}.md
```

Where:
- `{engagement-id}` follows the pattern `UX-{NNNN}` (e.g., `UX-0001`)
- `{topic-slug}` is a kebab-case descriptor of the evaluated interface (e.g., `settings-page`, `checkout-flow`)

### Required Output Sections

| Section | Level | Content |
|---------|-------|---------|
| **Executive Summary** | L0 | Top 3-5 findings by severity; overall usability assessment; heuristic coverage confirmation |
| **Evaluation Context** | L1 | Product description, target users, screens evaluated, input modality (Figma/screenshot/text), MCP status |
| **Findings by Heuristic** | L1 | Per-heuristic findings with: finding ID, heuristic violated, severity (0-4), affected screen/flow, evidence description, remediation recommendation, effort estimate (Low/Medium/High) |
| **Ranked Findings Summary** | L1 | All findings ranked by severity (descending), deduplicated across screens |
| **Remediation Roadmap** | L1 | Findings grouped by effort level with suggested implementation order |
| **Strategic Implications** | L2 | Cross-product usability patterns, organizational UX maturity observations, design evolution recommendations |
| **Synthesis Judgments Summary** | L1 | Each AI judgment call listed for synthesis confidence gate compliance |
| **Handoff Data** | L1 | Structured data for downstream sub-skills: finding IDs, heuristic references, severity ratings, affected screens (for Behavior Design and HEART Metrics consumption) |

### Finding Format

Each finding follows a consistent structure:

```
### Finding F-{NNN}: {brief description}

- **Heuristic:** H{N} -- {heuristic name}
- **Severity:** {0-4} ({Nielsen severity name})
- **Screen/Flow:** {affected screen or user flow}
- **Evidence:** {specific interface observation that demonstrates the violation}
- **Remediation:** {actionable fix recommendation}
- **Effort:** {Low | Medium | High}
```

> **Source:** Output location from parent SKILL.md [Available Agents] (line 152) and governance file `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.governance.yaml` [output.location].

---

## Routing

### Trigger Keywords

| Keyword | Routing Context |
|---------|----------------|
| heuristic evaluation | Direct match -- primary trigger |
| usability audit | Direct match |
| Nielsen heuristics | Direct match |
| interface review | Direct match |
| severity rating | In combination with UX/usability context |
| usability inspection | Direct match |
| UX evaluation | Direct match; may also trigger parent skill |

### Lifecycle-Stage Routing Integration

This sub-skill is routed to by the `ux-orchestrator` in the following lifecycle-stage scenarios:

| Stage | User Intent | Route Condition |
|-------|-------------|-----------------|
| During design | "Iterating on existing design" | Qualification: "Evaluating existing interface" (vs. "Testing hypotheses" which routes to `/ux-lean-ux`) |
| During design | "Building AI product" | When AI-First Design enabler is NOT completed or WSM < 7.80; supplements with AI-interaction heuristics |
| Any stage | "Comprehensive UX audit" | First sub-skill in multi-sub-skill route: `/ux-heuristic-eval` then `/ux-heart-metrics` |
| CRISIS | "Urgent UX problems" | Step 1 of fixed 3-skill CRISIS sequence |

### Wave Gating

This sub-skill is in **Wave 1** (Zero-Dependency). It requires only KICKOFF-SIGNOFF.md completion for deployment. No prior wave sub-skills need to be completed.

> **Source:** Routing integration from `skills/user-experience/rules/ux-routing-rules.md` [Stage Routing Table] and parent SKILL.md [Lifecycle-Stage Routing] (lines 295-334). Wave assignment from parent SKILL.md [Wave Architecture] (line 263).

---

## Cross-Framework Integration

### Downstream Handoffs

This sub-skill produces findings that feed into other sub-skills via the Jerry handoff protocol (`docs/schemas/handoff-v2.schema.json`).

| To Sub-Skill | Handoff Artifact | Key Fields | Trigger |
|-------------|-----------------|-----------|---------|
| `/ux-behavior-design` | Severity-rated findings | Finding ID, heuristic violated, severity (0-4), affected screen/flow | CRISIS mode step 1 to step 2; or explicit multi-sub-skill route |
| `/ux-heart-metrics` | Severity-rated findings with metric candidates | Finding ID, heuristic violated, severity (0-4), affected screen/flow, candidate HEART metric category (Happiness/Engagement/Adoption/Retention/Task success) | Comprehensive UX audit route; or CRISIS mode step 1 to step 3 (via step 2) |

**Handoff threshold:** Only findings with severity >= 2 (Minor usability problem, Major usability problem, Usability catastrophe) are included in cross-framework handoffs. Severity 0-1 findings remain in the evaluation report but are not propagated downstream.

### Upstream Inputs

This sub-skill may receive context from other sub-skills when invoked as part of a multi-sub-skill workflow:

| From Sub-Skill | Context Provided | Usage |
|----------------|-----------------|-------|
| `/ux-jtbd` | Job statements and user motivations | Informs evaluation of H2 (Match Between System and Real World) and H7 (Flexibility and Efficiency) |
| `/ux-atomic-design` | Component inventory | Informs evaluation of H4 (Consistency and Standards) across components |

### CRISIS Mode Role

In CRISIS mode (evaluate-diagnose-measure sequence), this sub-skill executes as **Step 1: Evaluate**. It produces an objective severity-rated inventory of UX problems that the subsequent sub-skills consume:

1. **This sub-skill** (Step 1): Identify UX issues via Nielsen's 10 heuristics -- produces severity-rated findings
2. `/ux-behavior-design` (Step 2): Diagnose behavioral root causes via Fogg B=MAP -- receives findings with severity >= 2
3. `/ux-heart-metrics` (Step 3): Quantify impact using HEART Goals-Signals-Metrics -- establishes metric baselines

> **Source:** Handoff data contracts from `skills/user-experience/rules/ux-routing-rules.md` [Handoff Data Contracts] and parent SKILL.md [Cross-Sub-Skill Handoff Data] (lines 474-487). CRISIS sequence from parent SKILL.md [Canonical Multi-Skill Workflow Sequences] (line 470) and `skills/user-experience/rules/ux-routing-rules.md` [CRISIS Routing].

---

## Synthesis Hypothesis Confidence

Heuristic evaluation outputs include synthesis hypotheses that carry confidence classifications per the synthesis validation protocol.

| Synthesis Step | Typical Confidence | Rationale |
|---------------|-------------------|-----------|
| Severity rating calibration across heuristics | MEDIUM | Severity ratings involve subjective judgment; calibration across Nielsen's 10 heuristics requires consistent application context |
| Comparative evaluation synthesis (cross-product or cross-version) | HIGH | Based on systematic checklist methodology with observable UI artifacts; HIGH when screenshots or screen recordings available as concrete evidence |

**Gate enforcement:**
- **HIGH outputs:** Include a "Synthesis Judgments Summary" listing each AI judgment call. Acknowledgment required before design recommendations are generated.
- **MEDIUM outputs:** Include a "Validation Required" section. Design recommendations are withheld until validation against real user data or expert review is provided.

> **Source:** Confidence classifications from `skills/user-experience/rules/synthesis-validation.md` [Sub-Skill Synthesis Output Map] (lines 58-59: `/ux-heuristic-eval` rows). Gate enforcement from parent SKILL.md [Synthesis Hypothesis Validation] (lines 338-372).

---

## Constitutional Compliance

All agents in this sub-skill adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- worker agent, no Agent tool access | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user decisions on finding priority or remediation approach | Unauthorized action; trust erosion |
| P-022 | NEVER inflate severity ratings without specific evidence from the interface | Governance undermined; quality assessment invalidated |
| P-001 | NEVER present findings without evidence from the interface under review | Unreliable outputs; unfounded claims propagate downstream |
| P-002 | NEVER leave evaluation output in transient context only -- persist to files | Context rot vulnerability; artifacts lost on session compaction |

**Per-agent enforcement:** The `ux-heuristic-evaluator` agent declares:
- `constitution.principles_applied`: P-003, P-020, P-022, P-001, P-002 in `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.governance.yaml`
- `capabilities.forbidden_actions`: 3 entries in NPT-009 format referencing the constitutional triplet
- `disallowedTools: [Agent]` in `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md` frontmatter

---

## Registration

This sub-skill follows a parent-routed registration model. Sub-skills are not independently registered in `CLAUDE.md` or `mandatory-skill-usage.md` because they are routed through the parent `/user-experience` orchestrator (`ux-orchestrator`). This is an explicit H-26(c) exception for sub-skills: parent skills own the CLAUDE.md and mandatory-skill-usage.md registration; sub-skills are discovered and dispatched by the parent orchestrator's internal routing logic.

| Registration Point | Status | Detail |
|--------------------|--------|--------|
| `CLAUDE.md` skill table | Registered via parent | `/user-experience` is registered in `CLAUDE.md`; sub-skills are not independently listed |
| `mandatory-skill-usage.md` trigger map | Routed via parent | The `/user-experience` trigger map row includes "heuristic evaluation" as a positive keyword (H-22); requests matching this keyword route to the parent skill, which dispatches to this sub-skill |
| `AGENTS.md` agent registry | Registered | `ux-heuristic-evaluator` is listed in `AGENTS.md` under the User-Experience Skill Agents section |
| Parent SKILL.md agent table | Registered | `ux-heuristic-evaluator` is listed in `skills/user-experience/SKILL.md` [Available Agents] |

> **H-26(c) exception rationale:** Independent registration of sub-skills would create duplicate trigger map entries and ambiguous routing (AP-02 Bag of Triggers). The parent orchestrator owns lifecycle-stage routing logic and dispatches to the correct sub-skill based on triage qualification, not keyword matching alone. Sub-skill agents are registered in `AGENTS.md` for discoverability but routing flows through the parent.

---

## Deployment Status

> **Wave 1 Sub-Skill -- Stub Agent.** This sub-skill is part of Wave 1 (Zero-Dependency) of PROJ-022. The companion agent file (`skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md`) is currently a stub -- it contains frontmatter, identity, purpose, and guardrails sections but lacks full `<input>`, `<capabilities>`, `<methodology>`, and `<output>` sections. Full agent implementation is pending Wave 1 completion of PROJ-022 EPIC-002. The SKILL.md itself is complete and specifies the methodology, output format, and routing integration that the agent will implement.

---

## Quick Reference

### Common Workflows

| Need | Command Example |
|------|-----------------|
| Evaluate a specific page | "Evaluate this settings page against Nielsen's 10 heuristics" |
| Full interface audit | "Run a heuristic evaluation across all screens of the checkout flow" |
| Severity assessment | "What are the most severe usability issues in this dashboard?" |
| AI interface evaluation | "Evaluate this AI assistant interface for usability" |
| CRISIS triage (step 1) | "CRISIS: users are abandoning checkout -- urgent UX triage" |
| Comprehensive audit | "Full UX audit of the onboarding experience" (routes to heuristic eval + HEART metrics) |

### Agent Selection Hints

| Keywords | Routes To |
|----------|-----------|
| heuristic, usability, Nielsen, severity, inspection, evaluation, interface review | `ux-heuristic-evaluator` |
| behavior, Fogg, B=MAP, motivation, ability, prompt, trigger | `/ux-behavior-design` (not this sub-skill) |
| HEART, metrics, measurement, GSM, happiness, engagement | `/ux-heart-metrics` (not this sub-skill) |
| accessibility, WCAG, ARIA, screen reader, contrast | `/ux-inclusive-design` (not this sub-skill) |

---

## References

| Source | Content | Path |
|--------|---------|------|
| Parent SKILL.md | Sub-skill scope, wave architecture, routing, MCP dependencies, synthesis protocol | `skills/user-experience/SKILL.md` |
| Agent definition | Agent frontmatter, identity, expertise, guardrails | `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md` |
| Agent governance | Tool tier, forbidden actions, output validation, constitutional compliance | `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.governance.yaml` |
| UX routing rules | Lifecycle-stage routing, CRISIS sequence, handoff data contracts | `skills/user-experience/rules/ux-routing-rules.md` |
| MCP coordination | Figma REQ dependency, degraded mode behavior, Context7 usage | `skills/user-experience/rules/mcp-coordination.md` |
| Synthesis validation | Confidence gate protocol, per-sub-skill confidence map | `skills/user-experience/rules/synthesis-validation.md` |
| Wave progression | Wave 1 entry criteria, signoff requirements | `skills/user-experience/rules/wave-progression.md` |
| CI checks | P-003 enforcement, sub-skill validation gates | `skills/user-experience/rules/ci-checks.md` |
| Skill standards | H-25/H-26 skill structure requirements | `.context/rules/skill-standards.md` |
| Agent development standards | H-34 dual-file architecture, tool tiers, handoff protocol | `.context/rules/agent-development-standards.md` |
| Quality enforcement | Quality gate thresholds, criticality levels, strategy catalog | `.context/rules/quality-enforcement.md` |
| Handoff schema | Canonical handoff schema v2 | `docs/schemas/handoff-v2.schema.json` |
| Agent governance schema | Governance YAML validation schema | `docs/schemas/agent-governance-v1.schema.json` |

### Requirements Traceability

| Source | Content | Path |
|--------|---------|------|
| PROJ-022 PLAN.md | Project plan: sub-skill scope, wave assignment, acceptance criteria, implementation phases | `projects/PROJ-022-user-experience-skill/PLAN.md` |
| EPIC-002 (Wave 1 Deployment) | Parent work item for Wave 1 sub-skill implementation including this sub-skill | PROJ-022 EPIC-002 in `projects/PROJ-022-user-experience-skill/WORKTRACKER.md` |
| ORCHESTRATION.yaml | Orchestration plan governing the build sequence for this sub-skill | `projects/PROJ-022-user-experience-skill/orchestration/ux-skill-build-20260303-001/ORCHESTRATION.yaml` |

### External References

| Source | Citation |
|--------|----------|
| Nielsen, J. (1994a) | "10 Usability Heuristics for User Interface Design." Nielsen Norman Group. |
| Nielsen, J. (1994b) | "Severity Ratings for Usability Problems." Nielsen Norman Group. |
| Nielsen, J. (1994c) | "How to Conduct a Heuristic Evaluation." Nielsen Norman Group. |
| Nielsen, J. (2020) | "10 Usability Heuristics for User Interface Design" (revised). Nielsen Norman Group. |

---

*Sub-Skill Version: 1.0.0*
*Parent Skill: `/user-experience` v1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Wave: 1 (Zero-Dependency)*
*SSOT: `skills/user-experience/SKILL.md`*
*Project: PROJ-022 User Experience Skill*
*Created: 2026-03-04*
