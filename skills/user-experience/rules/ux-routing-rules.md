<!-- VERSION: 1.2.0 | DATE: 2026-03-04 | SOURCE: SKILL.md (skills/user-experience/SKILL.md) Sections "Lifecycle-Stage Routing", "Wave Architecture", "Cross-Sub-Skill Handoff Data" | PARENT: /user-experience skill | REVISION: iter4 quality revision — annotated Multi-Sub-Skill Ordering Rules as UX-relative (distinct from RT-M-006 global priorities), added derived-entry note to Common Multi-Sub-Skill Combinations source comment for Comprehensive UX audit, added boundary condition note to onboard_displayed re-derivation heuristic -->

# UX Routing Rules

> Lifecycle-stage routing logic for the ux-orchestrator agent. Maps product lifecycle stages to sub-skill sequences and manages CRISIS routing. See also: `skills/user-experience/rules/wave-progression.md` (wave gate criteria), `skills/user-experience/rules/synthesis-validation.md` (synthesis confidence gates), `skills/user-experience/rules/mcp-coordination.md` (MCP availability routing).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Lifecycle Stage Router](#lifecycle-stage-router) | Product stage to sub-skill mapping |
| [Common Intent Resolution](#common-intent-resolution) | Ambiguous user intent to specific route |
| [Multi-Sub-Skill Routing](#multi-sub-skill-routing) | Sequential multi-sub-skill execution outside CRISIS mode |
| [CRISIS Routing](#crisis-routing) | Emergency 3-skill fixed sequence |
| [Wave-Aware Routing](#wave-aware-routing) | Routing behavior when sub-skills are not yet deployed |
| [Bypass Routing](#bypass-routing) | Wave bypass prompt presentation rules |
| [Cross-Sub-Skill Handoff](#cross-sub-skill-handoff) | Data contracts between sub-skills |
| [Session State Management](#session-state-management) | Engagement session state flags and lifecycle |

---

## Lifecycle Stage Router

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Lifecycle-Stage Routing" — 4-step sequential triage. Dispatch logic specification at SKILL.md line 321. -->

The orchestrator implements lifecycle-stage routing as a 4-step sequential triage:

1. **ONBOARD:** Display HIGH RISK user research warning (first invocation per engagement session; see [Session State Management](#session-state-management) for flag definition). Warning content: "AI-generated UX analysis reflects training data patterns, not your specific users. All synthesis hypotheses carry confidence classifications (HIGH/MEDIUM/LOW). Validate MEDIUM and LOW findings against real user data before making design decisions."
2. **CAPACITY CHECK:** Ask team UX time allocation. If < 20% of one person's time: recommend Wave 1 sub-skills only (P-020: user decides whether to accept the recommendation or override). This recommendation is based on team capacity constraints -- Wave 1 sub-skills (Heuristic Eval, JTBD) have the lowest operational overhead, making them appropriate for severely capacity-constrained teams. Note: the capacity recommendation is independent of cost tiers. The Free ($0) cost tier defined in `skills/user-experience/rules/mcp-coordination.md` [Cost Tiers] covers sub-skills across multiple waves (HEART W2, JTBD W1, Kano W4, Behavior Design W4), but those Wave 2-4 sub-skills require more sustained UX effort than a < 20% allocation supports. If >= 20% of one person's time: proceed to full stage triage with all deployed waves available.
3. **MCP CHECK:** Detect MCP availability via lightweight Context7 resolve call per `skills/user-experience/rules/mcp-coordination.md` [MCP Availability Detection]. Success criteria: Context7 `resolve-library-id` returns a valid library ID within 5 seconds (1 retry). Failure criteria: timeout > 5 seconds after retry, error response, or empty result. If unavailable: route to non-MCP fallback paths (text-only mode per `skills/user-experience/rules/mcp-coordination.md` [Degraded Mode Behavior]). Disclose MCP status to user per P-022.
4. **STAGE TRIAGE:** Route by product lifecycle stage using the table below.

### Stage Routing Table

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Lifecycle-Stage Routing" — route table. Wave assignments verified against `skills/user-experience/rules/wave-progression.md` [Wave Definitions]. -->

| Stage Category | User Intent | Routes To | Wave | Qualification Question | Decision Mapping |
|---------------|-------------|-----------|------|----------------------|-----------------|
| Before design | Don't know what to build | `/ux-jtbd` | 1 | -- | -- |
| Before design | Need to prioritize features | `/ux-kano-model` | 4 | -- | -- |
| Before design | Need validated prototype | `/ux-design-sprint` | 5 | -- (bypass prompt if Wave 5 not deployed) | -- |
| During design | Iterating on existing design | `/ux-lean-ux` OR `/ux-heuristic-eval` | 2 / 1 | "Are you testing hypotheses or evaluating an existing interface?" | "Testing hypotheses" -> `/ux-lean-ux`; "Evaluating existing interface" -> `/ux-heuristic-eval` (source: SKILL.md line 310 — Lean UX for hypothesis-driven iteration, Heuristic Eval for design quality evaluation) |
| During design | Building component system | `/ux-atomic-design` | 3 | -- | -- |
| During design | Building AI product | `/ux-ai-first-design` (if Enabler DONE + WSM >= 7.80) OR `/ux-heuristic-eval` with AI-interaction heuristic supplement | 5 / 1 | "Is the AI-First Design enabler completed?" | "Yes" + WSM >= 7.80 -> `/ux-ai-first-design`; "No" OR WSM < 7.80 -> `/ux-heuristic-eval` with AI-specific heuristic supplement. The supplement adds AI interaction heuristics (transparency, controllability, error recovery) to Nielsen's 10 as an interim evaluation path until the full AI-First Design sub-skill is deployed. (source: SKILL.md line 312-313 — "PAIR (interim)" defined as pairing heuristic evaluation with AI-specific supplementary heuristics) |
| After launch | Measure UX health | `/ux-heart-metrics` | 2 | -- | -- |
| After launch | Users not completing action | `/ux-behavior-design` | 4 | -- | -- |
| Any stage | Check accessibility | `/ux-inclusive-design` | 3 | -- | -- |
| Any stage | Comprehensive UX audit | `/ux-heuristic-eval` then `/ux-heart-metrics` | 1, 2 | -- | Multi-sub-skill route; see [Multi-Sub-Skill Routing](#multi-sub-skill-routing) (source: SKILL.md [Common Intent-to-Route Resolution] "Comprehensive UX audit" pattern) |
| CRISIS | Urgent UX problems | Fixed 3-skill sequence (see [CRISIS Routing](#crisis-routing)) | W1, W4, W2 | -- (user confirms CRISIS entry) | -- |

### Ambiguity Resolution Protocol

<!-- Source: `.context/rules/agent-routing-standards.md` Section "Multi-Skill Combination" — ordering protocol applied to UX sub-skill routing. -->

When STAGE TRIAGE produces multiple matches (e.g., "iterate on our accessible checkout"), the orchestrator resolves ambiguity by applying the ordering protocol defined in [Multi-Sub-Skill Routing](#multi-sub-skill-routing). If ambiguity remains after ordering: ask the user per H-31 with a structured question presenting the matched sub-skills and their purposes.

### No-Match Fallback

When the user's intent does not match any pattern in the Stage Routing Table:

1. Present the lifecycle stage categories (Before design / During design / After launch) and ask the user which best describes their situation per H-31.
2. If the user's response still does not match a known pattern: display the Stage Routing Table and ask which sub-skill best fits their need (presenting all options per H-31 structured question format -- progressively broader presentation reduces cognitive load while maintaining user authority over routing).
3. If the user's need falls outside all deployed sub-skills: acknowledge the gap transparently per P-022 and suggest alternative Jerry skills (e.g., `/problem-solving` for general UX research).

---

## Common Intent Resolution

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Common Intent-to-Route Resolution" (line 323) — common intent patterns derived from Stage Routing Table. These map natural-language user expressions to the appropriate sub-skill route and qualification question. -->

| User Says | Routes To | Qualification |
|-----------|----------|---------------|
| "Improve my UX" / "Make this more usable" | Heuristic Eval (existing) or Design Sprint (no design) | "Do you have an existing design?" -> Yes: `/ux-heuristic-eval`; No: `/ux-design-sprint` |
| "Fix a specific UX problem" | Behavior Design (behavioral) or Heuristic Eval (design-level) | "Is the problem about user behavior or design quality?" -> Behavior: `/ux-behavior-design`; Design quality: `/ux-heuristic-eval` |
| "Decide what to build" | JTBD (strategic) or Kano (prioritize known features) | "Are you defining the problem or prioritizing features?" -> Defining problem: `/ux-jtbd`; Prioritizing features: `/ux-kano-model` |
| "Measure whether UX is working" | HEART Metrics | No qualification needed |
| "Make this accessible" | Inclusive Design | No qualification needed |
| "Comprehensive UX audit" | Heuristic Eval + HEART Metrics (multi-sub-skill; see [Multi-Sub-Skill Routing](#multi-sub-skill-routing)) | No qualification needed |
| "CRISIS: urgent UX problems" | Emergency 3-skill sequence | No qualification needed (user confirms CRISIS entry) |

---

## Multi-Sub-Skill Routing

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Lifecycle-Stage Routing" — multi-sub-skill invocation. Ordering protocol from `.context/rules/agent-routing-standards.md` [Multi-Skill Combination] (RT-M-006, RT-M-007) applied to UX sub-skill routing. -->

When a user's intent maps to multiple sub-skills outside of CRISIS mode (e.g., "Comprehensive UX audit"), the orchestrator executes the sub-skills sequentially following the ordering protocol from `.context/rules/agent-routing-standards.md` [Multi-Skill Combination].

### Ordering Rules

| Priority (UX-relative) | Rule | UX Application | Source |
|------------------------|------|---------------|--------|
| 1 | Content before quality | Execute the content-producing sub-skill first, then the evaluation sub-skill (e.g., `/ux-heuristic-eval` produces findings before `/ux-heart-metrics` quantifies them) | `.context/rules/agent-routing-standards.md` [Multi-Skill Combination] RT-M-006 global priority 3 |
| 2 | Work before presentation | Execute the analytical sub-skill first, then the measurement sub-skill | `.context/rules/agent-routing-standards.md` [Multi-Skill Combination] RT-M-006 global priority 4 |
| 3 | If ambiguity remains | Ask user per H-31 with a structured question presenting the matched sub-skills and their purposes | `.context/rules/quality-enforcement.md` H-31 |

> **Priority numbering note:** Priority numbers in this table are relative to UX sub-skill routing (1-3) and do not correspond to the global priority numbers in `agent-routing-standards.md` [Multi-Skill Combination] RT-M-006, where these rules are numbered 3 and 4 respectively. The semantic ordering is identical; only the numbering differs because UX sub-skill routing does not use RT-M-006 priorities 1 (orchestration-first) and 2 (research-before-design), which apply at the inter-skill level.

### Multi-Sub-Skill Execution Protocol

| Step | Action | Validation |
|------|--------|----|
| 1 | Identify all matched sub-skills from [Stage Routing Table](#stage-routing-table) | Each sub-skill's wave must be deployed (see [Wave-Aware Routing](#wave-aware-routing)) |
| 2 | Apply ordering rules to determine execution sequence | Sequence follows content-before-quality ordering |
| 3 | Execute first sub-skill and collect output | Output validates per sub-skill's methodology |
| 4 | Pass handoff data to next sub-skill per [Cross-Sub-Skill Handoff](#cross-sub-skill-handoff) | Handoff artifact existence and key fields validated (see [Handoff Validation](#handoff-validation)) |
| 5 | Execute remaining sub-skills in sequence | Each receives prior sub-skill outputs |
| 6 | Produce cross-framework synthesis per `skills/user-experience/rules/synthesis-validation.md` [Cross-Framework Synthesis Protocol] | Synthesis triggered when 2+ sub-skill outputs exist for the same engagement |

### Common Multi-Sub-Skill Combinations

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Canonical Multi-Skill Workflow Sequences" (line 464) — multi-sub-skill patterns derived from Stage Routing Table and Common Intent Resolution table. Note: "Comprehensive UX audit" combination is a derived entry not directly listed in SKILL.md [Canonical Multi-Skill Workflow Sequences]; it is derived from SKILL.md [Common Intent-to-Route Resolution] + [Cross-Framework Synthesis Protocol] (line 377). See Handoff Data Contracts source comment (line 266) for full derivation attribution. -->

| User Intent | Sub-Skills | Execution Order | Rationale |
|------------|-----------|----------------|-----------|
| Comprehensive UX audit | `/ux-heuristic-eval` -> `/ux-heart-metrics` | Eval first (content), then Metrics (measurement) | Heuristic findings inform which HEART metrics to prioritize |
| Accessible design system | `/ux-atomic-design` -> `/ux-inclusive-design` | Atomic first (content), then Inclusive (quality) | Component inventory informs accessibility evaluation scope |
| Research-driven prototype | `/ux-jtbd` -> `/ux-design-sprint` | JTBD first (research), then Sprint (design) | Job statements feed sprint understanding phase |

### Constraints

- **Maximum 2 sub-skills** per non-CRISIS multi-sub-skill routing. Combinations exceeding 2 sub-skills escalate to user confirmation per RT-M-007 (source: `.context/rules/agent-routing-standards.md` [Multi-Skill Combination]).
- **CRISIS mode takes precedence.** If the user's intent matches CRISIS keywords (see [CRISIS Routing](#crisis-routing)), the fixed 3-skill CRISIS sequence executes instead of multi-sub-skill routing.
- **Wave gating applies.** If any sub-skill in the combination is not yet deployed, the orchestrator informs the user and offers alternatives per [Wave-Aware Routing](#wave-aware-routing).

---

## CRISIS Routing

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Lifecycle-Stage Routing" — CRISIS mode. Canonical sequence: "Evaluate to Diagnose to Measure" from SKILL.md Section "Canonical Multi-Skill Workflow Sequences" (line 470). -->

CRISIS mode executes a fixed 3-skill sequence for urgent UX problems. The sequence is not configurable -- the orchestrator selects the fixed route.

### CRISIS Entry

<!-- CRISIS keywords derived from SKILL.md [Common Intent-to-Route Resolution] (line 332) "CRISIS: urgent UX problems" pattern + SKILL.md [Lifecycle-Stage Routing] line 317 "CRISIS: Urgent UX problems" route. Keywords expanded to cover common natural-language expressions of UX urgency. -->

1. User indicates urgent UX problem (keywords: "CRISIS", "urgent UX", "users abandoning", "critical usability issue").
2. Orchestrator presents CRISIS confirmation: "CRISIS mode will execute a fixed 3-step sequence: (1) Heuristic Evaluation to identify design issues, (2) Behavior Design to diagnose behavioral root causes via Fogg B=MAP, (3) HEART Metrics to quantify impact. Proceed?"
3. User confirms entry (P-020 compliance: user authorizes the emergency sequence).

### CRISIS Execution Sequence

| Step | Sub-Skill | Wave | Purpose | Handoff to Next |
|------|-----------|------|---------|-----------------|
| 1 | `/ux-heuristic-eval` | 1 | Identify UX issues via Nielsen's 10 heuristics | Severity-rated findings (severity >= 2) |
| 2 | `/ux-behavior-design` | 4 | Diagnose behavioral root causes via Fogg B=MAP | Bottleneck diagnosis with motivation/ability/prompt breakdown |
| 3 | `/ux-heart-metrics` | 2 | Quantify impact using HEART Goals-Signals-Metrics | Metric baselines and target thresholds |

### CRISIS Rationale

The sequence follows the evaluate-diagnose-measure pattern (source: SKILL.md [Canonical Multi-Skill Workflow Sequences] line 470):
- **Evaluate:** Heuristic Eval produces an objective severity-rated inventory of UX problems (methodology: Nielsen's 10 heuristics with 0-4 severity scale).
- **Diagnose:** Behavior Design takes the highest-severity findings and traces them to behavioral bottlenecks (methodology: Fogg B=MAP -- is the user unable, unmotivated, or unprompted?).
- **Measure:** HEART Metrics establishes quantitative baselines so the team can track whether fixes actually improve the UX (methodology: Google's Goals-Signals-Metrics framework).

### CRISIS Synthesis

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Cross-Framework Synthesis Protocol" (line 375). Cross-reference: `skills/user-experience/rules/synthesis-validation.md` [Cross-Framework Synthesis Protocol] for authoritative synthesis protocol. -->

After the 3-skill CRISIS sequence completes, the orchestrator automatically produces a CRISIS synthesis report at `skills/user-experience/output/{engagement-id}/ux-orchestrator-crisis.md`. This synthesis follows the Cross-Framework Synthesis Protocol defined in `skills/user-experience/rules/synthesis-validation.md`, but with CRISIS-specific additions:
- **Priority ranking:** Findings are ranked by combined heuristic severity + behavioral bottleneck impact.
- **Quick-win identification:** Findings where the behavioral bottleneck is "prompt" (easiest to fix per Fogg model) are flagged as quick wins.
- **Metric coverage:** Each finding is mapped to a HEART metric so progress can be tracked.

---

## Wave-Aware Routing

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Wave Architecture" — wave-gated deployment. Cross-reference: `skills/user-experience/rules/wave-progression.md` [Wave State Tracking] for authoritative state detection rules. -->

The router checks wave signoff state before routing to gated sub-skills. Wave state is determined by the existence and validity of signoff files.

### Wave State Detection

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Wave Architecture" — signoff file gating. See also: `skills/user-experience/rules/wave-progression.md` [Wave State Tracking] for authoritative state detection rules, and `skills/user-experience/rules/wave-progression.md` [Signoff Requirements] for validation criteria. Signoff file locations verified against `skills/user-experience/rules/wave-progression.md` [Signoff File Locations] (6 files: KICKOFF through WAVE-5). -->

| File | Existence Indicates |
|------|-------------------|
| `skills/user-experience/output/KICKOFF-SIGNOFF.md` | Foundation complete; Wave 1 authorized |
| `skills/user-experience/output/WAVE-1-SIGNOFF.md` | Wave 1 complete; Wave 2 authorized |
| `skills/user-experience/output/WAVE-2-SIGNOFF.md` | Wave 2 complete; Wave 3 authorized |
| `skills/user-experience/output/WAVE-3-SIGNOFF.md` | Wave 3 complete; Wave 4 authorized |
| `skills/user-experience/output/WAVE-4-SIGNOFF.md` | Wave 4 complete; Wave 5 authorized |
| `skills/user-experience/output/WAVE-5-SIGNOFF.md` | Wave 5 complete; all waves deployed (full operational mode) |

### Routing Behavior for Unavailable Sub-Skills

When a user's intent routes to a sub-skill whose wave is not yet deployed:

1. **Inform:** "The sub-skill `/ux-{name}` is part of Wave {N}, which is not yet deployed." (P-022 compliance)
2. **Offer alternatives:**
   - If a Wave 1 sub-skill can partially address the need: suggest it with a disclaimer about scope limitations.
   - If no alternative exists: present the wave bypass mechanism.
3. **Bypass prompt:** If the user wants to proceed anyway, present the 3-field bypass documentation prompt (see [Bypass Routing](#bypass-routing)).

### Wave State Caching

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Wave Architecture" — wave state caching rules. Authoritative caching specification in `skills/user-experience/rules/wave-progression.md` [State Caching] — this section mirrors that specification for routing context; wave-progression.md is the authoritative source. -->

The orchestrator checks signoff files once per engagement session and caches the wave state. Cache invalidation occurs:
- On the next routing decision after a signoff file is committed during the session.
- At the start of each new engagement session.
- When a bypass is granted or resolved.

---

## Bypass Routing

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Wave Architecture" — bypass mechanism. Cross-reference: `skills/user-experience/rules/wave-progression.md` [Bypass Mechanism] for authoritative bypass field definitions and lifecycle. -->

Wave bypass allows routing to a sub-skill whose wave has not been formally signed off. Bypass requires user-approved 3-field documentation per P-020.

### Bypass Prompt

When a bypass is requested, the orchestrator presents:

```
Wave bypass requested for /ux-{name} (Wave {N}).

Please provide the following three fields:

1. UNMET CRITERION: Which wave {N} entry criterion is not met?
   Example: "No completed heuristic evaluation from Wave 1"

2. IMPACT ASSESSMENT: What is the risk of proceeding without this criterion?
   Example: "Sprint proceeds without prior framework calibration; findings may lack comparative baseline"

3. REMEDIATION PLAN: How will the unmet criterion be satisfied, and by when?
   Example: "Backfill Wave 1 heuristic evaluation within 2 sprints of Design Sprint completion"
```

### Bypass Documentation

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Wave Architecture" — bypass documentation structure. Cross-reference: `skills/user-experience/rules/wave-progression.md` [Bypass Mechanism] for authoritative bypass field definitions. -->

Bypass documentation is persisted at `skills/user-experience/output/{engagement-id}/wave-bypass-{wave-N}.md` with the following structure:

| Field | Content |
|-------|---------|
| Engagement ID | `UX-{NNNN}` |
| Sub-skill bypassed to | `/ux-{name}` |
| Wave bypassed | `{N}` |
| Unmet criterion | User-provided text |
| Impact assessment | User-provided text |
| Remediation plan | User-provided text with target date |
| Bypass approved by | User name or session ID |
| Bypass date | ISO 8601 date |

### Bypass Constraints

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Wave Transition Quality Gates" — bypass constraints. Cumulative ceiling: maximum 2 concurrent bypasses. -->

- **Cumulative ceiling:** Maximum 2 concurrent bypasses per team. If a team has 2 active bypasses, the orchestrator requires remediation of at least one before granting additional bypasses. Active bypass count is determined by scanning `skills/user-experience/output/{engagement-id}/wave-bypass-*.md` files and checking for the absence of a `Remediation completed` field (source: SKILL.md Section "Wave Transition Quality Gates").
- **Warning banner:** All sub-skill outputs produced under bypass carry a warning banner: "[WAVE BYPASS] This output was produced before Wave {N} entry criteria were met. See wave-bypass-{wave-N}.md for bypass documentation."
- **Bypass tracking:** Active bypasses are listed in the engagement directory and checked at each wave signoff. A wave signoff cannot complete if it has unresolved bypasses for that wave.

---

## Cross-Sub-Skill Handoff

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Cross-Sub-Skill Handoff Data" (line 474). Handoff protocol: `.context/rules/agent-development-standards.md` [Handoff Protocol]; canonical schema path `docs/schemas/handoff-v2.schema.json`. -->

Sub-skills exchange data via the Jerry handoff protocol (`docs/schemas/handoff-v2.schema.json`) with UX-specific artifact types.

### Handoff Data Contracts

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Cross-Sub-Skill Handoff Data" (line 474) — 6 handoff pairs plus the Heuristic Eval -> HEART Metrics pair derived from the "Comprehensive UX audit" composite route (SKILL.md line 377, Cross-Framework Synthesis Protocol). Key field names are derived from each sending sub-skill's output specification per the underlying UX methodology: JTBD key fields from switch interview protocol (Klement, 2016); Design Sprint fields from AJ&Smart Day 4 interview synthesis; Heuristic Eval fields from Nielsen severity classification (Nielsen, 1994); Atomic Design fields from Brad Frost's Storybook story schema; Lean UX fields from Gothelf & Seiden hypothesis backlog template. Authoritative field lists will be specified in each sub-skill agent's `<output>` section when deployed. -->

| From | To | Handoff Artifact | Key Fields |
|------|-----|-----------------|-----------|
| `/ux-jtbd` | `/ux-design-sprint` | Job statement + switch forces | Job statement text, push/pull forces, hiring criteria |
| `/ux-jtbd` | `/ux-kano-model` | Job-derived feature list | Feature names mapped to job steps |
| `/ux-design-sprint` | `/ux-lean-ux` | Validated prototype + Day 4 findings | Prototype description, interview findings, validated/invalidated hypotheses |
| `/ux-heuristic-eval` | `/ux-behavior-design` | Severity-rated findings | Finding ID, heuristic violated, severity (0-4), affected screen/flow |
| `/ux-heuristic-eval` | `/ux-heart-metrics` | Severity-rated findings with metric candidates | Finding ID, heuristic violated, severity (0-4), affected screen/flow, candidate HEART metric category (Happiness/Engagement/Adoption/Retention/Task success) |
| `/ux-atomic-design` | `/ux-inclusive-design` | Component inventory | Component names, atomic level (atom/molecule/organism), Storybook references |
| `/ux-lean-ux` | `/ux-heart-metrics` | Hypothesis backlog | Hypothesis ID, validated/invalidated status, metric implications |

### Handoff Validation

The orchestrator validates handoff data at each transition:

1. **Artifact existence:** All `artifacts` paths in the handoff resolve to existing files.
2. **Key fields present:** Required handoff fields for the specific sub-skill pair are non-empty (required fields per pair: see "Key Fields" column in the [Handoff Data Contracts](#handoff-data-contracts) table above).
3. **Confidence propagation:** The receiving sub-skill inherits the synthesis confidence level from the sending sub-skill's output (MEDIUM propagates as MEDIUM; LOW propagates as LOW; HIGH may be downgraded by the receiving sub-skill based on its own assessment). Confidence levels defined in `skills/user-experience/rules/synthesis-validation.md` [Confidence Gate Protocol].

---

## Session State Management

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Section "Lifecycle-Stage Routing" — "first invocation per session via session state flag" (line 300). Session scope defined by engagement ID per SKILL.md [Available Agents] output location pattern `{engagement-id}`. -->

The orchestrator maintains session state flags to manage routing behavior within an engagement session.

### State Flags

| Flag | Type | Initial Value | Set When | Reset When | Purpose |
|------|------|--------------|----------|------------|---------|
| `onboard_displayed` | boolean | `false` | ONBOARD warning displayed to user | New engagement session started (new engagement ID) | Prevents ONBOARD warning from repeating within the same engagement |
| `mcp_available` | boolean | `null` (unchecked) | MCP CHECK probe completes | New engagement session OR cache invalidation event | Caches MCP availability to avoid redundant probes |
| `wave_state` | integer (0-5) | `0` | Highest signoff file detected | New engagement session OR signoff file committed OR bypass event | Caches the highest authorized wave for routing decisions |
| `active_bypass_count` | integer | `0` | Bypass granted | Bypass remediated or new engagement session | Tracks concurrent bypasses against the cumulative ceiling (max 2) |

### Session Scope

A "session" in the routing context is scoped to an **engagement ID** (`UX-{NNNN}`). The engagement ID is established at the first routing decision and persists across all orchestrator invocations within that engagement. A new engagement ID resets all session state flags to their initial values. The engagement ID is carried in the orchestrator's output path: `skills/user-experience/output/{engagement-id}/`.

### State Storage

Session state flags are held in-memory by the ux-orchestrator agent during execution. They are not persisted to disk between separate orchestrator Agent invocations. At each new Agent invocation, the orchestrator re-derives state from disk artifacts:
- `onboard_displayed`: set to `true` if any output file exists in the engagement directory (implies a prior invocation has already displayed the warning). Boundary condition: this heuristic assumes engagement directories are not reused across separate sessions; if output files remain from a prior engagement that was not cleaned up, the warning may be incorrectly suppressed. In practice, the engagement ID scoping (`UX-{NNNN}`) makes this collision extremely unlikely.
- `mcp_available`: re-probed via MCP CHECK.
- `wave_state`: re-derived from signoff file scan per [Wave State Detection](#wave-state-detection).
- `active_bypass_count`: re-derived from bypass file scan per [Bypass Constraints](#bypass-constraints).

---

*Rule file: ux-routing-rules.md*
*Version: 1.2.0*
*Parent skill: /user-experience*
*Parent SKILL.md: `skills/user-experience/SKILL.md`*
*Sibling rules: `skills/user-experience/rules/wave-progression.md`, `skills/user-experience/rules/synthesis-validation.md`, `skills/user-experience/rules/mcp-coordination.md`, `skills/user-experience/rules/ci-checks.md`*
*Framework routing standards: `.context/rules/agent-routing-standards.md`*
*Handoff protocol: `.context/rules/agent-development-standards.md` [Handoff Protocol]*
*Created: 2026-03-03*
*Updated: 2026-03-04*
*Status: COMPLETE*
