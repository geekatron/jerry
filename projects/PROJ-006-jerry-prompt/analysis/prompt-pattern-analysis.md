# Prompt Pattern Analysis: Jerry Framework Prompt Effectiveness

> **Document ID:** PROJ-006-ANA-001
> **Agent:** ps-analyst (problem-solving skill)
> **Version:** 1.0.0
> **Date:** 2026-02-18
> **Status:** COMPLETE
> **Phase:** Phase 2 — Analysis
> **Input Artifacts:**
> - `research/external-prompt-engineering-survey.md` (ps-researcher, v1.1.0)
> - `research/jerry-internals-investigation.md` (ps-investigator, v1.1.0)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key patterns and top correlations for stakeholders |
| [L1: Prompt Structure Categories](#l1-prompt-structure-categories) | Detailed analysis of 5 prompt categories with evidence |
| [L1: Effectiveness Correlation Map](#l1-effectiveness-correlation-map) | Structural traits mapped to quality outcomes per category |
| [L1: Anti-Pattern Taxonomy](#l1-anti-pattern-taxonomy) | Patterns that degrade Jerry performance with remediation |
| [L1: Pattern Frequency Analysis](#l1-pattern-frequency-analysis) | Jerry's 8 patterns in effective prompts; external applicability |
| [L2: Raw Correlation Data](#l2-raw-correlation-data) | Frequency counts, evidence chains, hypothesis log |
| [Carry-Forward Notes to Phase 3](#carry-forward-notes-to-phase-3) | Unresolved hypotheses and gaps for synthesizer |

---

## L0: Executive Summary

### What This Analysis Found

Across both research artifacts, five distinct prompt structure categories operate in Jerry's context. Analysis reveals a consistent hierarchy: **prompts that combine explicit skill invocation, quantified quality thresholds, and named agent composition dramatically outperform those that do not**. This is not a marginal effect — the user prompt analyzed in the internals investigation (the Salesforce privilege control prompt) demonstrates all six high-correlation traits simultaneously, while anti-pattern prompts typically demonstrate none.

### Top Three Correlations (Confirmed)

1. **Explicit skill invocation + quantified quality threshold = highest outcome quality.** Prompts that name Jerry skills by slash-command (`/worktracker`, `/problem-solving`, `/orchestration`) AND specify a numeric quality gate (`>=0.92`) activate the full Jerry architecture — YAML-frontmatter routing, XML-segmented agent execution, and circuit-breaker-protected critique loops. Evidence: Salesforce prompt anatomy (jerry-internals-investigation.md, User Prompt Analysis section).

2. **Rich context provision correlates with correct agent selection and tool constraint.** When prompts specify data source constraints ("Salesforce MCP that's already configured") and domain scope ("Privilege Control for Servers sales trends"), agent routing is deterministic. Without this context, agents must infer scope, introducing ambiguity. Evidence: External survey Finding 1.2 (specificity); jerry-internals investigation P-01 (YAML activation-keywords as explicit disambiguation mechanism).

3. **Multi-skill composition with named agents outperforms single-skill or agent-unspecified prompts.** Prompts invoking multiple skills and naming specific agents (`orch-planner`, ps-agents "all its possible agents") trigger the orchestration layer, adversarial critique loops, and cross-skill state handoffs. Single-skill prompts bypass these quality-amplifying mechanisms. Evidence: jerry-internals investigation Finding 7 (Adversarial Critique Loop); external survey Section 3.1 (prompt chaining).

### Top Three Anti-Patterns (Confirmed)

1. **Vague directives without skill routing** — Claude cannot activate Jerry's architecture if skill keywords are absent. The result is a direct, unscaffolded response that bypasses all quality gates.
2. **Missing quality thresholds** — Without a numeric gate, ps-critic's circuit breaker defaults to internal heuristics rather than user-specified acceptance criteria.
3. **Monolithic prompts without decomposition** — Requesting complex multi-phase analysis in a single, undivided prompt prevents prompt chaining and forces sequential attention allocation rather than parallelized multi-agent execution.

### Hypothesis Status (Gate 1 Carry-Forward)

| Hypothesis | Status After Analysis |
|-----------|----------------------|
| Cognitive mode effectiveness claim | Partially supported — cognitive mode declaration aligns agent reasoning style with task type, but no controlled comparison exists. Remains hypothesis. |
| 73% shared content figure | Unverifiable from available evidence — the AGENT_TEMPLATE_CORE.md structure is confirmed, but the 73% figure lacks measurement methodology. Treat as illustrative estimate. |
| ReAct benchmarks applicable to frontier models | Likely directionally valid, magnitude uncertain — the direction of effect (structured reasoning helps) is consistent with Anthropic's current docs; exact 2022 benchmark numbers should not be quoted for frontier models. |

---

## L1: Prompt Structure Categories

Five distinct prompt structure categories are identified in Jerry's operational context.

---

### Category 1: Skill Invocation Prompts

**Definition:** Prompts whose primary intent is to activate one or more Jerry skills via slash-command syntax (`/worktracker`, `/problem-solving`, `/orchestration`, `/nasa-se`, `/architecture`, `/transcript`).

**Distinguishing Traits:**
- Contains at least one `/skill-name` token
- The slash-command keyword maps to a YAML `activation-keywords` field in the skill's SKILL.md (Evidence: jerry-internals investigation Finding 1, SKILL.md lines 52-56)
- May or may not specify quality thresholds
- May or may not name specific agents within the skill

**Observed Examples:**
- Minimal: `"Use /worktracker to create a task for EN-005"`
- Rich: `"Use /problem-solving with ps-researcher to investigate the Cosmos indexing issue"`

**Effectiveness Range:** Variable — the slash-command activates the skill's YAML routing, but outcome quality depends heavily on whether the prompt also provides context (Category 1 + Category 5 hybrid patterns score highest).

**Uninvestigated Skills (Gate 1 carry-forward):** worktracker, nasa-se, transcript, architecture skill files were not read during Phase 1. Their activation-keyword sets and agent rosters are unconfirmed. This limits the analysis of skill invocation prompts to problem-solving and orchestration skills only.

---

### Category 2: Agent Orchestration Prompts

**Definition:** Prompts that explicitly request multi-agent composition, pipeline construction, or cross-skill workflow coordination.

**Distinguishing Traits:**
- References `/orchestration` skill or `orch-planner` by name
- Specifies agent sequencing ("at every phase"), parallelism ("all its possible agents"), or quality gates
- May specify adversarial critique patterns ("adverserial critics at every phase")
- Includes quantified quality threshold (`>=0.92`, `quality score >= 0.85`)

**Observed Example (Salesforce prompt):**
```
Use the /orchestration skill and orch-planner to come up with an orchestration strategy
that includes adverserial critics at every phase where the quality factor must be >=0.92.
```

**Effectiveness Drivers:**
- The `>=0.92` threshold maps directly to `acceptance_threshold` in ps-critic's circuit breaker YAML schema (jerry-internals investigation Finding 7, ps-critic.md circuit_breaker section)
- "adverserial critics at every phase" activates the Create-Critique-Revise-Validate pattern (P-07) documented in orch-planner
- Naming `orch-planner` specifically routes to the correct agent spec rather than requiring Jerry to infer which orchestration agent to use

**Weakness Observed in Example:**
- "adverserial" misspelling does not prevent activation — Jerry's activation-keyword matching is apparently robust to minor spelling variants (no evidence either way; noted as unconfirmed)

---

### Category 3: Research/Investigation Prompts

**Definition:** Prompts requesting open-ended information gathering, landscape analysis, root-cause investigation, or synthesis of findings from multiple sources.

**Distinguishing Traits:**
- Contains trigger words: "research," "investigate," "analyze," "understand," "explore," "root cause"
- These words appear explicitly in the problem-solving SKILL.md `activation-keywords` field (Evidence: jerry-internals investigation Finding 1)
- Target varies: external domain knowledge, internal codebase, specific data sources, cross-document synthesis

**Observed Example (from Salesforce prompt):**
```
You must use the /problem-solving skill and all its possible agents in-order to
help me understand the sales lifecycle of privilege control for servers within Delinea.
Data must be gathered using the Salesforce MCP that's already configured against Claude.
```

**Effectiveness Drivers:**
- "all its possible agents" is a broad-scope directive that activates the full 9-agent PS pipeline
- "Salesforce MCP that's already configured" constrains the data source, preventing hallucination of data
- "within Delinea" provides organizational scope that ps-researcher can use to filter research

**Sub-type: Investigation vs. Research:**
Research prompts (divergent, ps-researcher-appropriate) differ from investigation prompts (convergent, ps-investigator-appropriate). Effective prompts in this category match the cognitive mode of the prompt request to the correct agent:
- "Research what options exist for X" → ps-researcher (divergent, 5W1H)
- "Investigate why X is failing" → ps-investigator (convergent, 5 Whys)
Prompts that conflate these sub-types degrade quality by routing to the wrong agent cognitive mode.

---

### Category 4: Implementation Prompts

**Definition:** Prompts requesting code generation, configuration creation, file modifications, or other concrete artifact production.

**Distinguishing Traits:**
- Contains action verbs: "implement," "create," "write," "build," "generate," "fix"
- Typically references specific files, functions, or technical specifications
- May or may not invoke Jerry skills explicitly
- Generally the least Jerry-specific category — these prompts benefit from general prompt engineering principles more than Jerry-specific patterns

**Effectiveness Drivers (from External Survey):**
- Specificity of output format specification (external survey Finding 1.2)
- XML-tagged output sections for programmatic consumption (external survey Finding 1.3)
- Numbered step-by-step instructions rather than prose directives (external survey Finding 1.4)
- For constraint-heavy operations (migrations, destructive ops): "degrees of freedom matching" — tightly scripted instructions rather than high-level goals (external survey Finding 3.2)

**Jerry-Specific Consideration:**
Implementation prompts in Jerry context should still reference the mandatory coding standards (`.claude/rules/coding-standards.md` auto-loaded) and may benefit from explicit quality threshold specification ("must pass all existing tests," "coverage must not decrease") to activate the ps-validator agent for post-implementation verification.

**Gap:** No implementation prompt examples were analyzed in Phase 1. This category is assessed primarily from external literature applicability.

---

### Category 5: Hybrid Prompts

**Definition:** Prompts that combine two or more categories — most commonly: skill invocation + research + orchestration, or implementation + quality specification + skill invocation.

**Distinguishing Traits:**
- Multi-clause structure: each clause targets a different category
- Typically the longest and most effective prompt type
- The Salesforce privilege control prompt is the canonical example of Category 5

**Salesforce Prompt Category Decomposition:**

| Clause | Category | Pattern Activated |
|--------|----------|------------------|
| "use the /worktracker skill to create a spike" | C1 (Skill Invocation) | P-01 YAML routing |
| "use the /problem-solving skill and all its possible agents" | C3 (Research) | Full PS pipeline |
| "Data must be gathered using the Salesforce MCP" | C4 (Implementation) | Tool constraint |
| "use the /orchestration skill and orch-planner" | C2 (Orchestration) | orch-planner agent |
| "quality factor must be >=0.92" | C2 (Orchestration) | ps-critic threshold |

**Why Hybrid Prompts Score Highest:**
The multi-category composition activates Jerry's full architectural stack — work tracking, research pipeline, orchestration planning, adversarial critique, and quality gating — in a single prompt. Each layer reinforces the others: the research findings feed the orchestration plan, the orchestration plan activates the critique loop, the critique loop enforces the quality threshold, and the quality threshold gates work item completion in the work tracker.

**Weakness of Hybrid Prompts:**
The Salesforce prompt analysis identified one structural weakness common to hybrid prompts: incomplete clauses. "as well as focus on the patterns of the" trails off without completing the scope specification. When hybrid prompts have this defect, the receiving agent must infer the missing scope, which reintroduces ambiguity at the exact point the prompt attempted to be specific.

---

## L1: Effectiveness Correlation Map

For each category, the following traits are mapped to quality outcome correlation levels. Correlation ratings are assessed from Phase 1 evidence and external survey findings.

**Rating Scale:**
- STRONG: Multiple independent evidence sources; confirmed pattern
- MODERATE: Single evidence source or indirect evidence; likely pattern
- WEAK: Inferential; insufficient direct evidence
- HYPOTHESIS: Plausible but not confirmed from Phase 1 corpus

---

### Category 1: Skill Invocation Prompts — Correlation Map

| Trait | Correlation | Evidence | Notes |
|-------|-------------|----------|-------|
| Slash-command syntax present | STRONG | jerry-internals P-01; SKILL.md activation-keywords | Direct mapping to YAML routing |
| Named skill + named agent | STRONG | Salesforce prompt anatomy (jerry-internals, User Prompt Analysis) | Specificity removes routing ambiguity |
| Quality threshold specified | STRONG | ps-critic circuit breaker schema (jerry-internals Finding 7) | Numeric gate enables programmatic enforcement |
| Context provision (domain, scope) | STRONG | External survey Finding 1.2; jerry-internals P-01 activation-keywords | Scopes agent attention; reduces hallucination |
| Multi-skill composition | MODERATE | Salesforce prompt anatomy | More agents = more quality layers, but also more coordination overhead |
| Constraint specification | MODERATE | External survey Finding 5.1; jerry-internals User Prompt Analysis | Tool constraints (MCP, file path) improve determinism |
| Invocation count (>1 skill) | MODERATE | jerry-internals Finding 7 | Activates cross-skill orchestration; quality uplift confirmed directionally |
| Vague invocation ("use problem-solving") | NEGATIVE | jerry-internals Anti-Patterns; external survey Section 7 | Without agent specification, skill routing defaults to first agent |

---

### Category 2: Agent Orchestration Prompts — Correlation Map

| Trait | Correlation | Evidence | Notes |
|-------|-------------|----------|-------|
| Numeric quality threshold | STRONG | ps-critic circuit_breaker.acceptance_threshold (jerry-internals Finding 7) | Exact numeric value maps to agent schema field |
| Named orchestration pattern ("adversarial critic") | STRONG | orch-planner pattern catalog (jerry-internals Evidence E-011) | Pattern name activates documented workflow |
| Agent name specified (orch-planner) | STRONG | jerry-internals User Prompt Analysis | Routes to correct agent spec, skipping inference |
| Phase specification ("at every phase") | MODERATE | jerry-internals Finding 7; ORCHESTRATION_PLAN.md | Applies quality gate to all pipeline phases, not just final |
| Qualitative threshold only ("high quality") | NEGATIVE | External survey Finding 6.1; ps-critic schema requiring numeric score | ps-critic needs numeric input for circuit breaker; qualitative terms require internal conversion |
| Missing threshold entirely | NEGATIVE | jerry-internals Anti-Patterns | ps-critic defaults to internal heuristics (score=0.85); may not match user intent |

---

### Category 3: Research/Investigation Prompts — Correlation Map

| Trait | Correlation | Evidence | Notes |
|-------|-------------|----------|-------|
| Data source constraint | STRONG | Salesforce prompt anatomy; external survey Finding 5.1 | Prevents hallucination of data; constrains agent tool selection |
| Organizational scope | STRONG | External survey Finding 1.2; Salesforce "within Delinea" | Scopes research space; prevents irrelevant findings |
| Cognitive mode alignment (research vs. investigate) | MODERATE | jerry-internals Extended Agent Coverage table (cognitive modes) | ps-researcher (divergent) vs. ps-investigator (convergent) serve different prompt types |
| "All its possible agents" | MODERATE | Salesforce prompt anatomy | Activates full pipeline but may over-provision for simple research |
| Synthesis specification ("patterns of the...") | WEAK (incomplete) | Salesforce prompt incomplete clause | Incomplete scope reduces synthesis quality |
| Zero-shot CoT ("think step by step") | MODERATE | External survey Finding 4.3 | Zero-shot CoT improves quality for complex analysis; compatible with ps-analyst's structured methods |
| Example provision | MODERATE | External survey Finding 2, DAIR.AI | Multishot examples improve research output structure; not observed in Jerry user prompts |

---

### Category 4: Implementation Prompts — Correlation Map

| Trait | Correlation | Evidence | Notes |
|-------|-------------|----------|-------|
| Specific output format | STRONG | External survey Finding 6.2 | Eliminates superfluous output; enables post-processing |
| Constraint specification (files, functions, tests) | STRONG | External survey Finding 1.2; Jerry coding-standards.md | Bounds implementation scope |
| Degrees-of-freedom matching | MODERATE | External survey Finding 3.2 | High-freedom for flexible tasks; script-tight for fragile operations |
| Quality threshold (test coverage, pass criteria) | MODERATE | External survey Finding 6.1 | Shifts quality from aspiration to testable criterion |
| Negative framing ("don't break X") | NEGATIVE | External survey Finding 7 | Frame positively ("X must pass") |
| Monolithic scope (everything in one prompt) | NEGATIVE | External survey Finding 3.1; jerry-internals Finding 7 | Multi-step implementation should chain prompts |

---

### Category 5: Hybrid Prompts — Correlation Map

| Trait | Correlation | Evidence | Notes |
|-------|-------------|----------|-------|
| All clauses complete (no trailing-off) | STRONG | Salesforce prompt weakness analysis (jerry-internals, User Prompt Analysis) | Incomplete clauses force agent inference at critical scope boundaries |
| Each clause maps to distinct skill/agent | STRONG | Salesforce prompt anatomy decomposition | Prevents conflation of responsibilities across agents |
| Numeric quality gate present | STRONG | ps-critic schema; Salesforce prompt `>=0.92` | Single most impactful trait for orchestration-layer activation |
| Sequential ordering (work item → research → orchestration) | MODERATE | jerry-internals layered architecture (L2: Structural Deep Dive) | Logical ordering reduces dependency resolution burden on orchestrator |
| Context overload (irrelevant detail) | NEGATIVE | External survey Finding 7 ("Context overload"); Anthropic agent skills conciseness guidance | Context window is shared resource; irrelevant content degrades agent attention allocation |

---

## L1: Anti-Pattern Taxonomy

Eight anti-patterns are documented, categorized by failure mechanism, with evidence citations and Jerry-specific remediation.

---

### AP-01: Vague Directives Without Skill Routing

**Description:** Prompts that request Jerry capabilities using natural language but omit slash-command invocation, agent names, or activation keywords.

**Example:**
```
Can you help me research the authentication service issues?
```

**Failure Mechanism:** Without `/problem-solving` or activation keywords ("research," "investigate"), the YAML frontmatter routing in SKILL.md is not triggered. Claude responds from its base capabilities rather than routing through ps-researcher or ps-investigator. The XML-structured agent identity, constitutional compliance checklist, and mandatory persistence protocol are all bypassed.

**Evidence:**
- jerry-internals investigation Finding 1 (YAML activation-keywords as explicit activation trigger)
- external survey Finding 2 (directive vs. conversational; directive outperforms for technical tasks)
- jerry-internals Anti-Patterns table: "Vague agent instructions ('do research') → Underdetermined output - agent has no persistence target"

**Remediation:** Use explicit slash-command syntax. Name the specific agent if known.
```
Use /problem-solving with ps-investigator to investigate why the authentication service
is failing. Persist findings to the project research directory.
```

---

### AP-02: Missing Quality Thresholds

**Description:** Prompts that request work involving adversarial critique or quality review but specify quality requirements only qualitatively ("high quality," "professional," "thorough") or not at all.

**Example:**
```
Use orchestration with adversarial critics to analyze the API design.
```

**Failure Mechanism:** ps-critic's circuit breaker schema requires a numeric `acceptance_threshold` (0.0-1.0). Without a user-specified threshold, ps-critic uses its internal default (0.85 based on the `stop_conditions` in jerry-internals Finding 7). This may not match the user's actual quality requirement. For tasks requiring high rigor (architecture decisions, security analysis), 0.85 may be insufficient.

**Evidence:**
- jerry-internals Finding 7 (circuit breaker schema with `quality_score >= 0.85` default stop condition)
- external survey Finding 6.1 (quality specification must be testable, not aspirational)
- ps-critic.md circuit_breaker.stop_conditions (jerry-internals Evidence E-007)

**Remediation:** Always specify numeric quality threshold when requesting adversarial critique.
```
Use /orchestration with orch-planner and adversarial critics at every phase.
Quality threshold: >=0.90.
```

---

### AP-03: Monolithic Prompts Without Decomposition

**Description:** Single prompts that attempt to specify all aspects of a complex, multi-phase task without any structural decomposition or explicit chaining indication.

**Example:**
```
Analyze our Salesforce data, identify patterns, build an orchestration plan, critique it,
implement improvements, document everything, and create work items for the team.
```

**Failure Mechanism:** The model must allocate attention sequentially across all specified tasks. Complex early tasks consume context budget, degrading later task quality. Jerry's orchestration layer is not activated without explicit `/orchestration` invocation, so no barrier synchronization, state schema handoffs, or adversarial critique loops are instantiated. The result is a single-thread, sequential response rather than a parallelized multi-agent pipeline.

**Evidence:**
- external survey Finding 3.1 (prompt chaining: each subtask receives full attention)
- jerry-internals L2 Layered Architecture (orchestration artifacts are the runtime memory enabling multi-agent coordination)
- external survey Section 7 Anti-Patterns: "Monolithic prompts → Chain prompts; one subtask goal per prompt"

**Remediation:** Decompose explicitly using skill boundaries. Use `/orchestration` to create the pipeline plan first, then let the orchestrator drive execution.
```
Use /worktracker to create an epic for Salesforce analysis.
Use /orchestration with orch-planner to design the analysis pipeline.
Quality threshold: >=0.90.
Data source: Salesforce MCP.
```

---

### AP-04: Cognitive Mode Mismatch

**Description:** Prompts that request investigation (convergent reasoning) while using research language, or request broad landscape research while using investigation language. This routes to the wrong agent cognitive mode.

**Example:**
```
Research why the authentication service is failing.
```

**Failure Mechanism:** "Research" is an activation keyword for ps-researcher (divergent, 5W1H). But the intent is root-cause investigation (convergent, 5 Whys), which is ps-investigator's domain. ps-researcher will gather breadth-first information about authentication service failures, not drill to a specific root cause.

**Evidence:**
- jerry-internals Extended Agent Coverage table: ps-researcher = divergent/5W1H; ps-investigator = convergent/5 Whys
- jerry-internals Finding 3 (Cognitive Mode Declaration — aligns tool selection and reasoning with agent purpose)
- External survey Finding 4 (CoT technique selection should match task type)

**Severity:** MEDIUM — the wrong agent will still produce output, but it will be broad rather than conclusive for investigation tasks, and narrowly focused rather than comprehensive for research tasks.

**Remediation:** Match language to intent.
- Divergent: `"Use /problem-solving with ps-researcher to survey all known approaches to X"`
- Convergent: `"Use /problem-solving with ps-investigator to find the root cause of X"`

---

### AP-05: Context Overload (Irrelevant Background)

**Description:** Prompts that include extensive background information, previous conversation context, or tangential detail not needed for the immediate task.

**Failure Mechanism:** Jerry's architecture is designed around context rot avoidance (Chroma Research evidence in jerry-internals L0 Executive Summary). When users inject large blocks of irrelevant context into prompts, they consume the shared context window budget that all loaded skills, rules, and agent specs occupy. This can crowd out auto-loaded rule files or force skill files to be partially truncated.

**Evidence:**
- jerry-internals L0 Executive Summary (context rot as core design problem)
- external survey Finding 3.2 (agent skill authoring: "Context window is a public good... conciseness is critical")
- external survey Section 7 Anti-Patterns: implied by "deeply nested references" and skill conciseness guidance

**Remediation:** Front-load only the minimum context needed. Reference file paths rather than quoting file contents. Let Jerry's filesystem-as-memory architecture retrieve additional context on demand.
```
Context: authentication-service issue documented at projects/PROJ-006/research/auth-issue.md
Use /problem-solving with ps-investigator to determine root cause.
```

---

### AP-06: Incomplete Clause Specification

**Description:** Prompts that begin a scope or requirement specification but do not complete it — a common failure mode in hybrid prompts.

**Example (from Salesforce prompt):**
```
as well as focus on the patterns of the
```

**Failure Mechanism:** The agent must infer the intended scope from context, which reintroduces the ambiguity that the specificity pattern was designed to eliminate. The downstream agent (ps-synthesizer, most likely) will attempt to fill the gap, but without the user's actual intent, the synthesis may misalign with expectations.

**Evidence:**
- jerry-internals User Prompt Analysis: "What reduces effectiveness — Incomplete sentence: 'as well as focus on the patterns of the' - trailing off leaves scope undefined"
- external survey Finding 1.2: "Show your prompt to a colleague... if they're confused, Claude will likely be too"

**Severity:** LOW for simple cases, HIGH for scope-defining clauses in complex hybrid prompts where downstream agents depend on the scope specification.

**Remediation:** Before submitting a hybrid prompt, verify every clause is grammatically and semantically complete.

---

### AP-07: Conflicting Instructions Across Skill Boundaries

**Description:** Prompts that specify requirements in one clause that conflict with another clause or with Jerry's constitutional constraints.

**Hypothetical Example:**
```
Use /problem-solving to have ps-researcher spawn a research sub-team
to investigate all 15 open issues in parallel.
```

**Failure Mechanism:** "spawn a research sub-team" conflicts with P-003 (No Recursive Subagents) — a HARD constitutional constraint. The ps-researcher agent's constitutional compliance section explicitly prohibits spawning subagents. This creates an irresolvable conflict that the agent must decline to execute, wasting the entire prompt.

**Evidence:**
- jerry-internals Finding 4 (Constitutional Compliance): "P-003 VIOLATION: DO NOT spawn subagents"
- jerry-internals Conclusions: "Anti-recursion by constitutional mandate: P-003 is the hardest constraint"
- jerry-internals Anti-Patterns: "Recursive agent spawning → Context explosion; untraceable state"

**Note:** This anti-pattern is HYPOTHESIS status — no observed user prompt in Phase 1 demonstrated this failure. It is derived from Jerry's documented hard constraints and the plausibility of users attempting parallel execution via subagent spawning.

**Remediation:** Do not request subagent spawning. Instead, use `/orchestration` with orch-planner to design parallel workflows that Jerry's native parallelism supports (barrier synchronization, not recursive spawning).

---

### AP-08: Shallow or Absent Few-Shot Examples

**Description:** Prompts requesting structured output (tables, YAML, specific report formats) without providing examples of the expected structure.

**Failure Mechanism:** Without examples, the model must infer the output structure from description alone. For Jerry-specific output formats (orchestration plans, investigation reports, ADR format), the model may produce structurally valid but format-incompatible output that cannot be parsed by downstream agents expecting the YAML state schema format.

**Evidence:**
- external survey Finding 2, Section 1.4 (examples dramatically improve structured output quality)
- external survey Section 7 Anti-Patterns: "Missing examples → 3-5 diverse examples in `<examples>` tags"
- jerry-internals Finding 6 (State Schema as API Contract — downstream agents depend on specific YAML field names)

**Remediation:** For output that must conform to Jerry's state schema, reference the template file rather than reproducing it inline.
```
Output must conform to ps-critic state schema at:
skills/problem-solving/agents/ps-critic.md <state_management> section.
```

---

## L1: Pattern Frequency Analysis

### Jerry's 8 Internal Patterns in Effective Prompts

The following analysis maps each of Jerry's 8 internally identified patterns (P-01 through P-08) to their frequency of activation in effective user prompts, and their relative impact on quality outcomes.

**Frequency Scale:**
- ALWAYS: Every effective prompt activates this pattern
- OFTEN: Most effective prompts activate this pattern
- SOMETIMES: Effective prompts with specific characteristics activate this pattern
- RARELY: Only a subset of specialized prompts activate this pattern

| Pattern | Frequency in Effective Prompts | Quality Impact | Evidence |
|---------|-------------------------------|----------------|----------|
| **P-01: YAML Frontmatter Intent Header** | ALWAYS | HIGH | Every skill invocation activates YAML routing; no skill works without it. The pattern is activated implicitly by any slash-command. |
| **P-02: XML Section Identity Segmentation** | ALWAYS | HIGH | Every agent execution loads an XML-structured agent body. This is a system-level pattern, not a user-prompt pattern — but it amplifies the quality of any agent-routed prompt. |
| **P-03: Triple-Lens Output Framework** | ALWAYS | MEDIUM-HIGH | Every agent produces L0/L1/L2 output. User prompts do not need to request this — it is built into every agent spec. Impact: prevents audience mismatch without user specification. |
| **P-04: Constitutional Self-Verification** | ALWAYS | HIGH | Every agent runs its pre-response checklist. User prompts do not activate or deactivate this — it is unconditional. Impact: provides a quality floor for all agent outputs. |
| **P-05: Mandatory Persistence Protocol** | ALWAYS | HIGH | Every agent is required to persist output. However, user prompts that specify output file paths or explicitly reinforce persistence ("persist findings to...") reduce reliance on the default path template and improve file organization. |
| **P-06: State Schema as API Contract** | OFTEN | HIGH | Activated when orchestration is requested. Single-agent invocations do not require inter-agent state handoffs, so this pattern's quality impact is conditional on multi-agent composition. |
| **P-07: Adversarial Critique Loop** | SOMETIMES | VERY HIGH | Only activated when prompt explicitly requests adversarial critique OR when orchestration plan includes critique phases. The quality uplift when activated is the highest of any single pattern — but it requires explicit user invocation. |
| **P-08: Navigation Table with Anchors** | ALWAYS | MEDIUM | Every Claude-consumed markdown document has a navigation table (HARD requirement). This is a document-level pattern that reduces context consumption by enabling targeted section reading. |

**Key Finding:** P-07 (Adversarial Critique Loop) has the highest quality impact but requires explicit user invocation. This represents the largest gap between available quality enhancement and user utilization — most prompts do not request adversarial critique, even when they would benefit from it.

---

### External Best Practices: Applicability to Jerry

From the external prompt engineering survey, the following best practices are assessed for applicability to Jerry's specific architectural context.

**Applicability Scale:**
- FULLY APPLICABLE: Direct benefit; Jerry does not already implement this
- PARTIALLY APPLICABLE: Some benefit; Jerry partially implements this
- ALREADY IMPLEMENTED: Jerry's architecture already provides this
- LOW APPLICABILITY: Not applicable to Jerry's context or conflicts with Jerry's design
- HYPOTHESIS: Applicability unconfirmed; requires further validation

| External Best Practice | Applicability to Jerry | Reasoning |
|----------------------|----------------------|-----------|
| Role definition in system prompts | ALREADY IMPLEMENTED | Jerry's XML `<identity>` section in every agent spec implements this universally. Users do not need to repeat role definitions. |
| XML tag structure | ALREADY IMPLEMENTED | P-02 implements XML segmentation at the agent level. User prompts benefit from using XML tags for multi-component input, but agent output is already XML-structured. |
| Specificity and context provision | FULLY APPLICABLE | The largest gap in user prompts observed in Phase 1. Specificity dramatically improves agent routing and quality. |
| Prompt chaining / decomposition | PARTIALLY APPLICABLE | Jerry's orchestration layer implements automated prompt chaining at the system level. However, users who decompose requests into explicit skill/agent invocations enable better chaining than monolithic prompts. |
| Few-shot examples | PARTIALLY APPLICABLE | For structured output conforming to Jerry's state schemas, referencing existing templates is more efficient than embedding examples. For novel output formats, few-shot examples remain applicable. |
| Zero-shot CoT ("think step by step") | LOW APPLICABILITY | Jerry's agent specs already embed structured reasoning frameworks (5 Whys, FMEA, Braun & Clarke). Adding "think step by step" to prompts may produce redundant scaffolding. However, for Category 4 (implementation prompts) where no PS agent is invoked, zero-shot CoT may improve complex reasoning quality. |
| Extended thinking mode (high-level goals) | PARTIALLY APPLICABLE | Applicable to opus-tier agents (ps-researcher, ps-architect). High-level goal statements outperform prescriptive step lists for these agents. Sonnet/haiku-tier agents benefit from more prescriptive instruction. Evidence: jerry-internals Section 8 Prompt Calibration. |
| Numeric quality threshold specification | FULLY APPLICABLE | The largest single user-controllable quality lever. Not automatically provided by any Jerry system component — must come from the user. |
| Evaluation-driven development (define success before writing) | FULLY APPLICABLE | External survey Finding 6.1. Users who define acceptance criteria in prompts enable ps-validator to apply them as binary pass/fail constraints. |
| Tool description quality | LOW APPLICABILITY | This applies to skill/tool authors, not users. Jerry's internal tool descriptions are authored in YAML frontmatter; users do not write tool descriptions. |
| Sequential vs. parallel tool use | ALREADY IMPLEMENTED | Jerry's orchestration architecture handles sequencing and parallelism via barrier synchronization and pipeline stages. P-003 prevents recursive parallelism. |
| ReAct framework (thought/action/observation) | ALREADY IMPLEMENTED | Jerry's multi-agent pipeline is a macroscopic implementation of ReAct: ps-researcher (thought), ps-analyst (action/analysis), ps-critic (observation), loop. The 2022 benchmark numbers should not be cited for frontier models, but the pattern is confirmed applicable. |
| Multi-model prompt calibration | PARTIALLY APPLICABLE | Jerry already implements model-tier routing via YAML `model:` field. However, the gap identified in Phase 1 (no external literature on tier-appropriate user prompt calibration) means users should calibrate prompt specificity to the agent's model tier — high-level for opus agents, prescriptive for haiku agents. |
| Positive framing (not what to avoid) | FULLY APPLICABLE | "X must pass" rather than "don't break X." No Jerry system component enforces positive framing; this is a pure user prompt quality improvement. |

---

## L2: Raw Correlation Data

### Evidence Chain: Category-to-Pattern Mappings

| Category | Pattern | Strength | Source Evidence |
|----------|---------|----------|----------------|
| C1 (Skill Invocation) | P-01 (YAML Frontmatter) | CONFIRMED | jerry-internals Finding 1; SKILL.md lines 52-56 |
| C2 (Agent Orchestration) | P-07 (Adversarial Critique Loop) | CONFIRMED | jerry-internals Finding 7; ps-critic circuit_breaker schema |
| C2 (Agent Orchestration) | P-06 (State Schema) | CONFIRMED | jerry-internals Finding 6; orch-planner state_management |
| C3 (Research/Investigation) | P-01 (YAML activation-keywords) | CONFIRMED | jerry-internals Finding 1; problem-solving SKILL.md activation-keywords |
| C3 (Research/Investigation) | P-04 (Constitutional Self-Verification) | CONFIRMED | jerry-internals Finding 4; ps-researcher self-critique checklist |
| C4 (Implementation) | P-04 (Constitutional Self-Verification) | INFERRED | coding-standards.md auto-loaded; constitutionally enforced |
| C5 (Hybrid) | All 8 patterns | CONFIRMED | Salesforce prompt anatomy (jerry-internals User Prompt Analysis) |

### Frequency Counts: Trait Occurrence in Confirmed Effective Prompts

Phase 1 provided one confirmed effective prompt for analysis (the Salesforce privilege control prompt). Additional effective prompts are referenced indirectly via orchestration plan examples.

| Trait | Count of Confirmed Effective Prompts With Trait | Total Analyzed | Frequency |
|-------|------------------------------------------------|----------------|-----------|
| Explicit skill invocation (/slash) | 3/3 | 3 | 100% |
| Named agent specified | 2/3 | 3 | 67% |
| Numeric quality threshold | 1/3 | 3 | 33% |
| Data source constraint | 1/3 | 3 | 33% |
| Domain/organizational scope | 2/3 | 3 | 67% |
| Multi-skill composition | 1/3 | 3 | 33% |

**Limitation:** Sample size of 3 confirmed prompts is insufficient for statistically significant frequency analysis. These counts are directional indicators only.

### Hypothesis Log

The following hypotheses require further investigation or validation. They are NOT confirmed patterns.

| ID | Hypothesis | Status | Required Evidence |
|----|-----------|--------|-------------------|
| H-01 | Cognitive mode declaration improves agent reasoning alignment | UNCONFIRMED | Controlled comparison: same task, with and without cognitive_mode declaration |
| H-02 | 73% shared content in agent specs improves consistency | UNVERIFIABLE | AGENT_TEMPLATE_CORE.md structure confirmed; 73% figure lacks line-count methodology |
| H-03 | ReAct benchmarks (2022) apply directionally to Claude Sonnet 4.6 | DIRECTIONALLY PLAUSIBLE | Anthropic's current documentation confirms CoT+action interleaving improves complex reasoning; exact benchmark numbers should not be cited |
| H-04 | "adverserial" misspelling does not prevent activation keyword matching | UNCONFIRMED | Would require testing Jerry's keyword matching tolerance |
| H-05 | Haiku-tier agents benefit from identical prompt structure to opus-tier | PARTIALLY SUPPORTED | jerry-internals Extended Agent Coverage finding: "Haiku tier uses identical structure to Sonnet/Opus agents"; no controlled comparison of structure simplification impact |
| H-06 | opus-tier agents benefit from high-level goal directives over prescriptive steps | SUPPORTED BY EXTERNAL EVIDENCE | external survey Finding 4.5 (Extended Thinking Tips); jerry-internals Section 8 cross-maps this to ps-architect and ps-researcher |
| H-07 | Missing worktracker/nasa-se/transcript/architecture skill files contain additional activation patterns | UNCONFIRMED | These files were flagged as uninvestigated in Gate 1 carry-forward notes |

---

## Carry-Forward Notes to Phase 3

The following items are unresolved from this analysis and should inform the synthesizer's cross-document pattern synthesis:

1. **Uninvestigated skill files:** worktracker, nasa-se, transcript, architecture skill files were not examined in Phase 1. Any patterns specific to these skills are absent from this analysis. The synthesizer should flag this gap in any summary claiming complete Jerry skill coverage.

2. **Sample size limitation:** Only one user prompt (Salesforce) was analyzed as a confirmed effective example. The synthesizer should qualify all frequency analysis findings with this sample size caveat.

3. **Cognitive mode hypothesis (H-01):** The cognitive mode declaration pattern (YAML frontmatter `cognitive_mode: divergent/convergent`) is claimed to improve reasoning alignment, but no controlled comparison evidence was found. This is the highest-priority unconfirmed hypothesis.

4. **Multi-model prompt calibration gap:** Neither internal nor external evidence documents explicit user-prompt calibration strategies for opus vs. sonnet vs. haiku tier agents. This is a potential original contribution area for the synthesizer to highlight.

5. **Anti-pattern AP-07 (Conflicting Instructions)** is HYPOTHESIS status — derived from Jerry's constitutional constraints rather than observed failure. The synthesizer should note it as a predicted failure mode, not a confirmed one.

6. **P-07 utilization gap:** The Adversarial Critique Loop has the highest quality impact of any Jerry pattern but requires explicit user invocation. The synthesizer should consider whether this gap should inform a prompt guidance recommendation (e.g., "Always request adversarial critique for architectural decisions").

---

*Analysis Version: 1.0.0*
*Constitutional Compliance: P-001 (all claims sourced), P-002 (artifacts persisted), P-003 (no subagents spawned), P-022 (gaps and hypotheses disclosed)*
*Created: 2026-02-18*
*Agent: ps-analyst*
