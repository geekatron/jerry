# Jerry Internal Architecture: Anatomy of Effective Prompts

> **Document ID:** PROJ-006-INV-001
> **Agent:** ps-investigator
> **Version:** 1.1.0
> **Date:** 2026-02-18
> **Status:** COMPLETE
> **Revision:** v1.1.0 — 2026-02-18 (ps-critic revision actions: Chroma Research citation added; extended agent coverage for all 9 PS agents; cross-mapping table added)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What Jerry's prompt architecture is and why it works |
| [L1: Detailed Findings](#l1-detailed-findings) | 8 specific prompt patterns with evidence |
| [L2: Structural Deep Dive](#l2-structural-deep-dive) | Architecture patterns, templates, anti-patterns |
| [Pattern Catalog](#pattern-catalog) | Consolidated listing of 8 identified patterns |
| [Extended Agent Coverage: All 9 Problem-Solving Agents](#extended-agent-coverage-all-9-problem-solving-agents) | Universal vs. selective patterns across the full agent portfolio |
| [Cross-Mapping: Jerry Patterns vs. External Survey Focus Areas](#cross-mapping-jerry-patterns-vs-external-survey-focus-areas) | Alignment/divergence table mapping 8 Jerry patterns to 7 survey focus areas |
| [User Prompt Analysis](#user-prompt-analysis) | Anatomy of the example Salesforce prompt |
| [Anti-Patterns](#anti-patterns) | Patterns that degrade performance |
| [Evidence Chain](#evidence-chain) | File references for all findings |

---

## L0: Executive Summary

Jerry's internal prompt architecture works because it solves a fundamental LLM problem: context rot. As conversations grow, LLM performance degrades because context fills with irrelevant information — this phenomenon is documented by Chroma Research (see: https://research.trychroma.com/context-rot), whose empirical findings show measurable performance degradation as context windows fill with accumulated but no longer relevant content. Jerry counters this by treating the filesystem as infinite memory - every agent, every skill, and every rule file is designed to be loaded selectively rather than all at once.

The most striking pattern in Jerry's internals is the use of structured XML sections inside agent specification files (`<identity>`, `<persona>`, `<capabilities>`, `<guardrails>`, `<constitutional_compliance>`). This structure mimics Anthropic's own recommended patterns for complex prompts. Each agent "knows" what it is, what it can do, what it cannot do, and how to validate its own output - all encoded in the prompt itself.

The effective user prompt analyzed in this investigation (the Salesforce privilege control prompt) works because it composes multiple skills explicitly (`/worktracker`, `/problem-solving`, `/orchestration`), names specific agents, sets a quantified quality threshold (>=0.92), and establishes a data source constraint (Salesforce MCP). It is dense with verbs, agent names, and outcome specifications - the opposite of vague natural language requests.

---

## L1: Detailed Findings

### Finding 1: YAML Frontmatter as Machine-Parseable Intent Header

**Pattern:** Every SKILL.md and agent spec file opens with a YAML frontmatter block.

**Evidence from `c:/AI/jerry/skills/problem-solving/SKILL.md` (lines 1-24):**
```yaml
---
name: problem-solving
description: Structured problem-solving framework with specialized agents...
version: "2.1.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch
activation-keywords:
  - "research"
  - "analyze"
  - "investigate"
  - "critique"
  - "quality score"
---
```

**Why it works:** The YAML frontmatter gives Claude a machine-parseable header before reading prose. The `activation-keywords` field is particularly effective - it creates an explicit mapping between user natural language triggers and skill activation. When a user says "research" or "quality score," the system knows to activate this skill. This is pattern-matching made explicit rather than relying on Claude to infer when to use a skill.

**Also seen in:** All agent spec files (`ps-investigator.md` lines 1-118, `ps-researcher.md` lines 1-116, `ps-critic.md` lines 1-135, `orch-planner.md` lines 1-138). The frontmatter in agent files adds `model: sonnet/opus/haiku` to specify which Claude model to use for each agent type.

---

### Finding 2: XML Section Tagging for Agent Identity Segmentation

**Pattern:** Agent body is wrapped in `<agent>` tag, with subsections in `<identity>`, `<persona>`, `<capabilities>`, `<guardrails>`, `<constitutional_compliance>`, `<invocation_protocol>`, `<output_levels>`, `<state_management>` tags.

**Evidence from `c:/AI/jerry/skills/problem-solving/agents/ps-investigator.md` (lines 120-474):**
```
<agent>
<identity>
You are **ps-investigator**, a specialized investigation agent...
**Role:** Investigation Specialist
**Cognitive Mode:** Convergent
</identity>

<persona>
**Tone:** Methodical and thorough
**Communication Style:** Direct
**Audience Adaptation:** L0/L1/L2
</persona>

<capabilities>
**Allowed Tools:** [table]
**Forbidden Actions (Constitutional):**
- **P-003 VIOLATION:** DO NOT spawn subagents...
</capabilities>
...
</agent>
```

**Why it works:** XML tags create semantic boundaries that Claude respects. The `<identity>` section tells Claude who it is (role identity priming). The `<persona>` section specifies communication style. The `<capabilities>` section creates explicit tool permission lists combined with explicit prohibitions. The constitutional compliance section creates a self-critique checklist that the agent runs before responding.

This structure is directly aligned with Anthropic's guidance on complex prompt design. The `AGENT_TEMPLATE_CORE.md` file (`c:/AI/jerry/skills/shared/AGENT_TEMPLATE_CORE.md`, line 148) explicitly documents this as "XML-Structured Agent Body (Anthropic Best Practice)".

---

### Finding 3: Triple-Lens Output Framework (L0/L1/L2)

**Pattern:** All agents and skill documents produce output at exactly three levels: L0 (ELI5 for stakeholders), L1 (Software Engineer detail), L2 (Principal Architect strategic view).

**Evidence from `c:/AI/jerry/skills/problem-solving/SKILL.md` (lines 32-41):**
```markdown
| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | New users, stakeholders | Purpose, When to Use |
| **L1 (Engineer)** | Developers invoking agents | Invoking an Agent |
| **L2 (Architect)** | Workflow designers | Orchestration Flow |
```

**Evidence from `c:/AI/jerry/skills/problem-solving/agents/ps-researcher.md` (lines 141-145):**
```
- **L0 (ELI5):** Accessible executive summary. Use analogies.
- **L1 (Software Engineer):** Technical findings with code examples.
- **L2 (Principal Architect):** Strategic implications, trade-offs, risks.
```

**Why it works:** The Triple-Lens framework solves the single hardest prompt engineering problem: audience mismatch. Instead of asking Claude to "write for a mixed audience" (vague), Jerry encodes explicit audience profiles with named levels. The agent knows L0 uses analogies, L1 uses code snippets, L2 uses trade-off analysis. This produces predictably structured output that serves multiple consumers simultaneously.

The same pattern appears in `c:/AI/jerry/skills/orchestration/SKILL.md` (lines 28-37), `c:/AI/jerry/skills/nasa-se/SKILL.md` (lines 53-62), and `c:/AI/jerry/skills/orchestration/PLAYBOOK.md` (lines 39-50). It is universal across all Jerry skills.

---

### Finding 4: Constitutional Compliance as Self-Verification Checklist

**Pattern:** Every agent has a `<constitutional_compliance>` section containing a checkbox list that the agent runs before generating output.

**Evidence from `c:/AI/jerry/skills/problem-solving/agents/ps-researcher.md` (lines 222-242):**
```markdown
**Self-Critique Checklist (Before Response):**
- [ ] P-001: Are all claims sourced with citations?
- [ ] P-002: Is research output persisted to file?
- [ ] P-004: Is the methodology documented?
- [ ] P-011: Are recommendations evidence-based?
- [ ] P-022: Am I transparent about what I couldn't find?
```

**The principle table pattern (from `ps-investigator.md`, lines 196-216):**
```markdown
| Principle | Enforcement | Agent Behavior |
|-----------|-------------|----------------|
| P-001 (Truth/Accuracy) | Soft | Root cause supported by evidence |
| P-002 (File Persistence) | **Medium** | ALL investigations persisted |
| P-003 (No Recursion) | **Hard** | Task tool single-level only |
| P-022 (No Deception) | **Hard** | Gaps and limitations acknowledged |
```

**Why it works:** Two mechanisms operate here simultaneously. First, the principle table creates explicit behavior mapping: each principle has an enforcement level (Soft/Medium/Hard) and a concrete behavioral requirement. Second, the checkbox list creates a pre-response verification protocol. This is the "constitutional AI" pattern applied at the individual agent level - the agent has internalized criteria for self-evaluation.

The bolding of "Hard" principles and the **Medium** and **Hard** emphasis in the table draws attention to the most critical constraints.

---

### Finding 5: Mandatory Persistence Protocol (P-002 Pattern)

**Pattern:** Every agent includes an explicit `<invocation_protocol>` section that repeats the file persistence requirement three times in different forms.

**Evidence from `c:/AI/jerry/skills/problem-solving/agents/ps-investigator.md` (lines 303-334):**
```markdown
## MANDATORY PERSISTENCE (P-002, c-009)

After completing investigation, you MUST:

1. **Create a file** using the Write tool at:
   `projects/${JERRY_PROJECT}/investigations/{ps_id}-{entry_id}-investigation.md`

2. **Follow the template** structure from:
   `templates/investigation.md`

3. **Link the artifact** by running:
   ```bash
   python3 scripts/cli.py link-artifact ...
   ```

DO NOT return transient output only. File creation AND link-artifact are MANDATORY.
```

**Why it works:** The persistence requirement is stated as a named protocol (MANDATORY PERSISTENCE), then enumerated as numbered steps, then restated as a prohibition ("DO NOT return transient output only"). The use of CAPS for "MANDATORY" and "MUST" creates visual salience. The concrete file path template (`projects/${JERRY_PROJECT}/...`) removes ambiguity about where to write. Repetition with variation (positive statement + numbered steps + negative prohibition) covers all mental paths an LLM might take.

This pattern appears identically in `ps-researcher.md` (lines 290-321), `ps-critic.md` (lines 381-399), and `orch-planner.md` (lines 366-379). It is a core Jerry pattern.

---

### Finding 6: State Schema as Agent Coordination Language

**Pattern:** Every agent defines a structured YAML output schema that serves as the inter-agent communication contract.

**Evidence from `c:/AI/jerry/skills/problem-solving/agents/ps-investigator.md` (lines 387-407):**
```yaml
investigator_output:
  ps_id: "{ps_id}"
  entry_id: "{entry_id}"
  artifact_path: "projects/${JERRY_PROJECT}/investigations/{filename}.md"
  severity: "{CRITICAL|HIGH|MEDIUM|LOW}"
  root_cause: "{summary}"
  confidence: "{high|medium|low}"
  corrective_actions: ["{CA-001}", "{CA-002}"]
  lessons: ["{LES-XXX}"]
  next_agent_hint: "ps-reporter for incident report"
```

**Evidence from `c:/AI/jerry/skills/problem-solving/agents/ps-critic.md` (lines 454-483):**
```yaml
critic_output:
  quality_score: {0.0-1.0}
  assessment: "EXCELLENT | GOOD | ACCEPTABLE | NEEDS_WORK | POOR"
  threshold_met: {true|false}
  recommendation: "ACCEPT | REVISE | ESCALATE"
  improvement_areas:
    - criterion: "{criterion_name}"
      current_score: {0.0-1.0}
```

**Why it works:** The YAML state schema serves as a typed API contract between agents. When `ps-critic` outputs `threshold_met: false`, the orchestrator knows to invoke the generator again without ambiguity. The `next_agent_hint` field provides routing guidance built into the output itself. The quantified `quality_score` (0.0-1.0) enables programmatic threshold evaluation. This is the Google ADK multi-agent pattern applied to prompt engineering.

---

### Finding 7: Adversarial Critique Loop Architecture

**Pattern:** Quality assurance is built into workflow patterns as a Generator-Critic-Revision-Validation cycle, with a circuit breaker.

**Evidence from `c:/AI/jerry/projects/PROJ-001-oss-release/orchestration/en001-bugfix-20260210-001/ORCHESTRATION_PLAN.md` (lines 248-291):**
```
STEP 1: CREATE (ps-architect-{task})
  └─ Agent implements the change

STEP 2: ADVERSARIAL CRITIQUE (ps-critic-{task})
  └─ Devil's Advocate: Challenge assumptions
  └─ Steelman: Find strongest counter-arguments
  └─ Red Team: Attack for vulnerabilities
  └─ Blue Team: Defend and validate

STEP 3: REVISE (ps-architect-{task}-rev)
  └─ Creator incorporates feedback

STEP 4: VALIDATE (ps-validator-{task})
  └─ Binary pass/fail against acceptance criteria
```

**Circuit breaker from `ps-critic.md` (lines 119-135):**
```yaml
circuit_breaker:
  max_iterations: 3
  improvement_threshold: 0.10
  stop_conditions:
    - "quality_score >= 0.85"
    - "iteration >= max_iterations"
    - "no_improvement_for_2_consecutive_iterations"
```

**Why it works:** The adversarial critique pattern transforms quality assurance from a human review step into an automated, structured process. The four critique modes (Devil's Advocate, Steelman, Red Team, Blue Team) are named roles that Claude can adopt sequentially. The circuit breaker prevents infinite refinement loops. This is "Constitutional AI meets workflow engineering."

The quantified criteria in the ORCHESTRATION_PLAN (`correctness: 0.30, completeness: 0.25, consistency: 0.20, safety: 0.15, clarity: 0.10`) create weighted evaluation - exactly the structure a ps-critic needs to produce a `quality_score`.

---

### Finding 8: Navigation Table with Anchor Links as Document Map

**Pattern:** Every Jerry markdown document (rules files, SKILL.md, agent specs, orchestration plans) begins with a navigation table that maps sections to anchor links.

**Evidence from `c:/AI/jerry/projects/PROJ-001-oss-release/orchestration/en001-bugfix-20260210-001/ORCHESTRATION_PLAN.md` (lines 13-25):**
```markdown
## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | High-level summary |
| [L1: Technical Plan](#l1-technical-plan) | Workflow diagram, phases |
| [L2: Implementation Details](#l2-implementation-details) | State schema |
| [Execution Constraints](#execution-constraints) | Constitutional constraints |
| [Success Criteria](#success-criteria) | Phase exit criteria |
```

**Evidence from `.claude/rules/markdown-navigation-standards.md` (lines 154-162) - the rule enforcing this:**
```
**NAV-001**: Navigation table present [HARD]
**NAV-002**: Table appears after frontmatter, before content [HARD]
**NAV-006**: Section names use anchor links [HARD]
```

**Why it works:** The navigation table solves Claude's linear document reading problem. According to Jerry's own research (cited in `markdown-navigation-standards.md`), Anthropic's platform documentation states: "A table of contents allows Claude to efficiently navigate and jump to specific sections as required." The anchor links are HARD requirements (not optional) because they enable targeted section retrieval rather than full document scanning.

---

## L2: Structural Deep Dive

### The Layered Prompt Architecture

Jerry's prompt system operates in five architectural layers:

```
Layer 5: CLAUDE.md (Root Context)
  - Identity: "Jerry is a framework for behavior and workflow guardrails"
  - Navigation table pointing to sub-systems
  - Hard constraints (P-003, P-020, P-022)
  - Quick reference tables

Layer 4: .claude/rules/ (Auto-Loaded Standards)
  - coding-standards.md
  - architecture-standards.md
  - error-handling-standards.md
  - mandatory-skill-usage.md
  - Loaded at session start, always in context

Layer 3: skills/{skill}/SKILL.md (Skill Invocation Context)
  - YAML frontmatter with activation-keywords
  - Triple-Lens document structure
  - Agent table with output locations
  - Invocation patterns (natural language, explicit, Task tool)
  - Loaded on demand when skill invoked

Layer 2: skills/{skill}/agents/{agent}.md (Agent Execution Context)
  - YAML frontmatter (identity, persona, capabilities, guardrails)
  - XML-structured agent body
  - Mandatory persistence protocol
  - State schema (inter-agent communication)
  - Self-critique checklist

Layer 1: Orchestration Artifacts (Runtime State)
  - ORCHESTRATION.yaml (SSOT, machine-readable)
  - ORCHESTRATION_PLAN.md (human-readable strategy)
  - ORCHESTRATION_WORKTRACKER.md (tactical tracking)
  - Phase artifacts (persisted agent outputs)
```

This layered architecture implements the Context Rot solution: each layer is loaded only when needed. The root CLAUDE.md is always loaded but intentionally sparse. The skills are loaded on invocation. The agent specs are loaded per-agent. The orchestration artifacts are the runtime memory.

### The Federated Template System

The `AGENT_TEMPLATE_CORE.md` (`c:/AI/jerry/skills/shared/AGENT_TEMPLATE_CORE.md`) reveals a sophisticated template composition system. It documents 9 extension points:

```
DOMAIN_NAME_PREFIX     - Agent name prefix (ps, nse)
DOMAIN_IDENTITY_EXTENSION - Additional identity fields
DOMAIN_FORBIDDEN_ACTIONS  - Additional forbidden actions
DOMAIN_INPUT_VALIDATION   - Domain-specific validation
DOMAIN_OUTPUT_FILTERING   - Additional filtering rules
DOMAIN_VALIDATION_FIELDS  - Domain-specific validation
DOMAIN_REFERENCES          - Domain references
DOMAIN_PRINCIPLES          - Additional constitution principles
DOMAIN_XML_SECTIONS        - Domain-specific XML sections
```

This means all Jerry agents share ~73% of their prompt content (the core template) while customizing 27% for domain-specific behavior. This is prompt DRY (Don't Repeat Yourself) applied at architectural scale.

### The Cognitive Mode Declaration

A subtle but significant pattern: every agent declares `cognitive_mode: "divergent"` or `cognitive_mode: "convergent"` in its YAML frontmatter and in the `<identity>` section.

- **Divergent** agents (ps-researcher): Explore broadly, gather multiple perspectives
- **Convergent** agents (ps-investigator, ps-critic): Drill down systematically to conclusions

This declaration primes Claude to adopt the appropriate reasoning style. The `ps-researcher` uses "5W1H Framework" (divergent exploration). The `ps-investigator` uses "5 Whys" (convergent drilling). The declaration aligns tool selection and reasoning pattern with agent purpose.

---

## Pattern Catalog

| # | Pattern Name | Where Found | Core Mechanism |
|---|-------------|-------------|----------------|
| P-01 | YAML Frontmatter Intent Header | All SKILL.md and agent specs | Machine-parseable activation keywords, model selection, tool allowlist |
| P-02 | XML Section Identity Segmentation | All agent body prompts | `<identity>`, `<persona>`, `<capabilities>`, `<guardrails>` tags |
| P-03 | Triple-Lens Output Framework | All skills and agent outputs | L0/L1/L2 mandatory output levels serving 3 distinct audiences |
| P-04 | Constitutional Self-Verification | All agent specs | Pre-response checklist + principle-behavior table |
| P-05 | Mandatory Persistence Protocol | All agent invocation protocols | Named protocol + numbered steps + prohibition restatement |
| P-06 | State Schema as API Contract | All agent state_management sections | Typed YAML output schema enabling inter-agent coordination |
| P-07 | Adversarial Critique Loop | Orchestration plans + ps-critic spec | Create-Critique-Revise-Validate with circuit breaker |
| P-08 | Navigation Table with Anchors | All Claude-consumed markdown files | Anchor-linked section table enabling targeted document reading |

---

## Extended Agent Coverage: All 9 Problem-Solving Agents

> **Revision Note**: The original investigation (v1.0.0) documented 3 agents (ps-investigator, ps-researcher, ps-critic). This section extends coverage to all 9 agents, identifying universal patterns and agent-specific variations.
> **Evidence**: E-005 through E-007 (original), E-016 through E-021 (extended)

### Full Agent Roster

| Agent | Model | Cognitive Mode | Primary Method | Output Location |
|-------|-------|---------------|----------------|-----------------|
| ps-researcher | opus | divergent | 5W1H Framework | `research/` |
| ps-analyst | sonnet | convergent | 5 Whys, FMEA, trade-off matrix | `analysis/` |
| ps-synthesizer | sonnet | convergent | Braun & Clarke thematic analysis | `synthesis/` |
| ps-critic | sonnet | convergent | Generator-Critic adversarial loop | `reviews/` (critique) |
| ps-reviewer | sonnet | convergent | SOLID, OWASP, Google code review | `reviews/` |
| ps-architect | opus | convergent | ADR Nygard format, C4, DDD | `decisions/` |
| ps-validator | haiku | convergent | IEEE 1012, traceability matrix | `analysis/` (validation) |
| ps-reporter | haiku | convergent | Agile status, DORA metrics | `reports/` |
| ps-investigator | sonnet | convergent | 5 Whys, Ishikawa, Pareto | `investigations/` |

(Sources: YAML `model:` fields in each agent spec; E-005 through E-021)

### Patterns Universal Across All 9 Agents

The following patterns appear in every agent spec without exception:

#### Universal Pattern A: YAML Frontmatter with `model:` Field

Every agent opens with a YAML frontmatter block that specifies the model tier. This is an extension of Pattern P-01 (YAML Frontmatter Intent Header) with a critical addition: the `model:` field enables routing to the appropriate Claude model tier. Three tiers are used: `opus` (complex reasoning), `sonnet` (balanced analysis), `haiku` (fast structured tasks).

Evidence: All 9 agent spec files, `model:` field in YAML frontmatter.

#### Universal Pattern B: XML-Structured Agent Body

Every agent uses `<agent>`, `<identity>`, `<persona>`, `<capabilities>`, `<guardrails>`, `<constitutional_compliance>`, `<invocation_protocol>`, `<output_levels>`, and `<state_management>` XML sections. This is Pattern P-02 (XML Section Identity Segmentation) and is universal.

Notable consistency: the `<invocation_protocol>` section always contains the identically-worded "MANDATORY PERSISTENCE (P-002, c-009)" block, the same forbidden actions for P-003, and the same `link-artifact` CLI command. This is the templated 73% of shared content described in Finding (L2, Federated Template System) using `AGENT_TEMPLATE_CORE.md`.

#### Universal Pattern C: Triple-Lens L0/L1/L2 Output

All 9 agents produce output at three levels. The audience definitions are consistent across all agents:
- L0: "ELI5 for non-technical stakeholders"
- L1: "Software Engineer" with code examples and technical details
- L2: "Principal Architect" with strategic implications

Evidence: `<output_levels>` section of all 9 agent specs.

#### Universal Pattern D: Self-Critique Checklist

Every agent has a pre-response self-critique checklist in `<constitutional_compliance>`. The checklist varies by agent but always includes: P-001 (evidence-based claims), P-002 (file persisted), P-022 (no deception/transparency about gaps). P-003 (no recursion) is present in the table but not always in the checkbox list (it is enforced as a Hard constraint rather than a soft checklist item).

Evidence: `<constitutional_compliance>` sections of all 9 agent specs.

#### Universal Pattern E: YAML State Schema with `next_agent_hint`

Every agent defines a typed YAML output schema that includes a `next_agent_hint` field. This creates a self-routing system where each agent suggests its downstream successor, enabling orchestrators to follow agent-defined workflow suggestions rather than hardcoding pipeline sequences.

The terminal agent (ps-reporter) is the only one with `next_agent_hint: null`, explicitly marking itself as a pipeline terminus.

Evidence: `<state_management>` sections of all 9 agent specs; ps-reporter.md lines 383: `next_agent_hint: null  # Reports are typically terminal`.

### Patterns Found in Some Agents But Not All

| Pattern | Agents With It | Agents Without It | Notes |
|---------|---------------|-------------------|-------|
| **Session Context Validation** (`<session_context_validation>` section) | All 9 | — | Universal in extended review |
| **WebSearch/WebFetch tools** | ps-researcher, ps-analyst, ps-synthesizer, ps-architect | ps-reviewer, ps-reporter, ps-validator, ps-critic, ps-investigator | External access agents are those doing open-ended research or design; evaluation/validation agents work only from provided artifacts |
| **mcp__context7__ tools** | ps-researcher, ps-analyst, ps-synthesizer, ps-architect | ps-reviewer, ps-reporter, ps-validator, ps-critic, ps-investigator | Same split as WebSearch — research/design agents access library docs; evaluation agents do not |
| **Prior Art citations in YAML** | All 9 (under `prior_art:`) | — | Universal: every agent cites academic or industry references for its methodology |
| **`cognitive_mode: divergent`** | ps-researcher only | All others (convergent) | ps-researcher is the only divergent (breadth-first) agent in the problem-solving skill |
| **Quantified quality score** | ps-critic only | All others | The 0.0-1.0 score, circuit breaker, and `threshold_met: {true|false}` output are unique to ps-critic |
| **Mermaid output format** | ps-architect only | All others | Architecture diagrams in C4 format; outputs `mermaid` in `output_formats` |
| **`validate-constraint` CLI call** | ps-validator only | All others | After file creation, ps-validator also runs `validate-constraint` for each constraint — an additional step beyond the standard `link-artifact` |

### Key Divergences from the Original 3-Agent Sample

The original investigation covered ps-investigator, ps-researcher, and ps-critic. Examining all 9 reveals several patterns that were not visible:

1. **The Haiku tier uses identical structure to Sonnet/Opus agents**: ps-reporter and ps-validator follow exactly the same XML structure and YAML format as heavier agents, but with `model: haiku`. The prompt format is not simplified for lighter models — only the task scope and output content differ. This challenges the assumption that Haiku-tier agents need different prompt formats.

2. **The researcher→analyst→synthesizer→architect pipeline is implicit in `next_agent_hint` routing**: Reading the state schemas of all agents reveals a coherent workflow: ps-researcher suggests ps-analyst, ps-analyst suggests ps-architect or ps-validator, ps-synthesizer suggests ps-architect or ps-reporter, ps-architect suggests ps-validator or ps-reviewer, ps-validator suggests ps-reporter. This is a documented workflow embedded in the agent specs themselves.

3. **ps-reporter has a unique prohibition**: Its constitutional compliance table includes P-010 (Task Tracking Integrity), which requires accurate reporting against WORKTRACKER. No other agent references P-010. This principle is specific to the reporting function.

4. **ps-reviewer covers 5 distinct review types**: code, design, architecture, security, documentation — with a severity taxonomy (CRITICAL/HIGH/MEDIUM/LOW/INFO) that maps to specific action requirements. This is the most complex output taxonomy of any agent in the portfolio.

---

## Cross-Mapping: Jerry Patterns vs. External Survey Focus Areas

> This table maps Jerry's 8 internal prompt patterns (Pattern Catalog) to the 7 focus areas from the External Prompt Engineering Survey. It shows where Jerry's patterns align with, extend, or diverge from industry best practices.

| Jerry Pattern | Survey Focus Area | Alignment | Notes |
|---------------|------------------|-----------|-------|
| **P-01: YAML Frontmatter Intent Header** | 1. Prompt Structure Patterns | EXTENDS | YAML frontmatter is not discussed in external sources; it provides machine-parseable role + capability declaration beyond what Anthropic's role prompting guidance describes |
| **P-01: YAML Frontmatter Intent Header** | 5. Agent/Tool Orchestration | EXTENDS | The `activation-keywords` field in YAML implements the Anthropic recommendation for skill discovery (Source 2), but codifies it in structured data rather than prose |
| **P-02: XML Section Identity Segmentation** | 1. Prompt Structure Patterns | ALIGNS | Directly implements Anthropic's XML tag recommendation ("game-changer"). Jerry extends the pattern by standardizing the specific tag names (`<identity>`, `<persona>`, `<capabilities>`) across all agents |
| **P-02: XML Section Identity Segmentation** | 2. Directive vs. Conversational Styles | ALIGNS | The `<identity>` section with explicit role declaration implements Anthropic's "most powerful use of system prompts" role prompting guidance |
| **P-03: Triple-Lens Output Framework** | 6. Quality Thresholds and Evaluation | EXTENDS | External sources recommend specifying output format (Survey Finding 6.2); Jerry extends this to a three-tier audience-aware output specification, which is not discussed in any surveyed source |
| **P-04: Constitutional Self-Verification** | 6. Quality Thresholds and Evaluation | ALIGNS | Implements Anthropic's "self-correction chains" pattern (Survey Finding 3.1: "chain prompts to have Claude review its own work"). Jerry formalizes this as a checkbox embedded in every agent spec |
| **P-05: Mandatory Persistence Protocol** | 7. Anti-Patterns | EXTENDS | No external source addresses the "transient output" anti-pattern for multi-session workflows. The P-002 persistence requirement is a Jerry-specific solution to context rot, grounded in Chroma Research (https://research.trychroma.com/context-rot) but not found in the external prompt engineering literature |
| **P-06: State Schema as API Contract** | 5. Agent/Tool Orchestration | ALIGNS | Partially aligns with Anthropic's guidance on passing XML-tagged output between prompts (Survey Finding 3.1). Jerry extends this to typed YAML schemas with `next_agent_hint` for self-routing |
| **P-06: State Schema as API Contract** | 3. Multi-Step/Compositional Prompting | ALIGNS | The state schema implements prompt chaining with structured handoffs, matching Survey Finding 3.1's "pass results as input to subsequent prompts" pattern |
| **P-07: Adversarial Critique Loop** | 4. Chain-of-Thought and Reasoning | EXTENDS | ReAct (Survey Finding 5.2) interleaves reasoning and action; Jerry extends this to inter-agent adversarial critique where separate specialized agents perform critique roles |
| **P-07: Adversarial Critique Loop** | 6. Quality Thresholds and Evaluation | ALIGNS | Implements Anthropic's "evaluation-driven development" (Survey Finding 6.1) and multi-step self-review chains. The circuit breaker (max 3 iterations) is a Jerry-specific addition |
| **P-08: Navigation Table with Anchors** | 3. Multi-Step/Compositional Prompting | ALIGNS | Directly implements Anthropic's agent skills best practice: "table of contents allows Claude to efficiently navigate and jump to specific sections" (Survey Source 2) |

### Summary of Cross-Mapping Insights

**Patterns with strong external backing (ALIGNS)**:
- P-02 (XML tags), P-04 (self-verification), P-06 (state schema/chaining), P-08 (navigation tables) all have direct citations in the external survey

**Patterns that extend or have no external equivalent (EXTENDS)**:
- P-01 (YAML frontmatter as structured activation), P-03 (Triple-Lens audiences), P-05 (persistence protocol against context rot), and the multi-model routing dimension of P-01 — none of these appear in the external literature as documented patterns

**Notable gap**: Survey Finding 8 (Prompt Calibration by Model Tier) identified in the External Survey revision exists as an implicit practice in Jerry (via YAML `model:` field), but has no external literature basis. Jerry's implementation is ahead of documented industry practice on this dimension.

---

## User Prompt Analysis

**The example prompt:**
```
Claude use the /worktracker skill to create a spike.
The spike is about: Privilege Control for Servers sales trends and behavior.
You must use the /problem-solving skill and all its possible agents in-order to
help me understand the sales lifecycle of privilege control for servers within Delinea.
Data must be gathered using the Salesforce MCP that's already configured against Claude.
You must analyze the opportunities as a whole as well as focus on the patterns of the
Use the /orchestration skill and orch-planner to come up with an orchestration strategy
that includes adverserial critics at every phase where the quality factor must be >=0.92.
```

**Anatomical breakdown:**

| Element | Text | Pattern Invoked |
|---------|------|-----------------|
| Work Item Creation | "use the /worktracker skill to create a spike" | Explicit skill invocation (P-01 activation-keywords) |
| Domain Context | "Privilege Control for Servers sales trends" | Topic scoping - tells ps-researcher what to research |
| Multi-Skill Composition | "/problem-solving skill and all its possible agents" | Forces ALL 8 PS agents into the workflow |
| Data Source Constraint | "Salesforce MCP that's already configured" | Tool constraint - channels data gathering |
| Analysis Scope | "analyze opportunities as a whole as well as focus on patterns" | Dual-level analysis (macro + pattern) |
| Orchestration | "use the /orchestration skill and orch-planner" | Explicit agent invocation (orch-planner) |
| Quality Specification | "adverserial critics at every phase" | Invokes adversarial critique loop pattern (P-07) |
| Quantified Threshold | "quality factor must be >=0.92" | Numeric quality gate for ps-critic circuit breaker |

**What makes it effective:**
1. **Verb density**: Every sentence contains action verbs (use, create, help, gather, analyze, come up with, includes)
2. **Explicit skill names**: `/worktracker`, `/problem-solving`, `/orchestration` - exact invocation syntax
3. **Agent name**: `orch-planner` - specific enough to load the right agent spec
4. **Quantified quality**: `>=0.92` maps directly to `acceptance_threshold` in ps-critic's circuit breaker
5. **Named pattern**: "adverserial critics at every phase" maps to Pattern 7/8 in the orchestration playbook
6. **Tool constraint**: "Salesforce MCP" - tells Claude which data source to use

**What reduces effectiveness:**
1. Incomplete sentence: "as well as focus on the patterns of the" - trailing off leaves scope undefined
2. Implicit scope: "all its possible agents" may not be appropriate for every phase
3. No file path specified: orchestration artifacts will go to default location which may not be what was intended

---

## Anti-Patterns

Based on the investigation, the following patterns would degrade Jerry prompt performance:

| Anti-Pattern | Why Harmful | Jerry's Solution |
|-------------|-------------|-----------------|
| Vague agent instructions ("do research") | Underdetermined output - agent has no persistence target | Mandatory Persistence Protocol (P-05): named file path required |
| Flat single-level output | Mismatches audience needs; either too technical or too vague | Triple-Lens L0/L1/L2 framework (P-03) |
| Unbounded quality loops | Infinite refinement; context window exhaustion | Circuit breaker in ps-critic: max 3 iterations (P-07) |
| Recursive agent spawning | Context explosion; untraceable state | P-003 Hard Constraint: one level only |
| No state schema | Inter-agent communication fails; state lost | YAML state output schema (P-06) |
| No navigation tables | Linear document reading wastes context | Navigation table HARD requirement NAV-001, NAV-006 (P-08) |
| Generic exception catching | Masks domain-specific errors | Specific exception types per domain (error-handling-standards.md) |
| Transient-only output | Context rot destroys findings on compaction | P-002 File Persistence mandate |

---

## Evidence Chain

| Evidence ID | Type | Source | Line Reference | Finding |
|-------------|------|--------|----------------|---------|
| E-001 | File | `c:/AI/jerry/CLAUDE.md` | Lines 1-81 | Root context structure: navigation table, hard constraints, quick reference |
| E-002 | File | `c:/AI/jerry/skills/problem-solving/SKILL.md` | Lines 1-370 | YAML frontmatter, activation-keywords, Triple-Lens audience table |
| E-003 | File | `c:/AI/jerry/skills/orchestration/SKILL.md` | Lines 1-530 | Orchestration skill: YAML frontmatter, Pattern catalog, State schema |
| E-004 | File | `c:/AI/jerry/skills/nasa-se/SKILL.md` | Lines 1-469 | NASA SE skill: 10 agents, Triple-Lens, constitutional compliance |
| E-005 | File | `c:/AI/jerry/skills/problem-solving/agents/ps-investigator.md` | Lines 1-572 | Full XML agent body, YAML frontmatter, state schema, constitutional checklist |
| E-006 | File | `c:/AI/jerry/skills/problem-solving/agents/ps-researcher.md` | Lines 1-576 | Divergent cognitive mode, 5W1H framework, Context7 integration |
| E-007 | File | `c:/AI/jerry/skills/problem-solving/agents/ps-critic.md` | Lines 1-713 | Quality score formula, circuit breaker, generator-critic pattern |
| E-008 | File | `c:/AI/jerry/skills/orchestration/agents/orch-planner.md` | Lines 1-407 | Orchestration planner: workflow ID strategy, pipeline alias resolution |
| E-009 | File | `c:/AI/jerry/skills/shared/AGENT_TEMPLATE_CORE.md` | Lines 1-384 | Federated template system: 9 extension points, 73% shared content |
| E-010 | File | `c:/AI/jerry/projects/PROJ-001-oss-release/orchestration/en001-bugfix-20260210-001/ORCHESTRATION_PLAN.md` | Lines 1-490 | Real orchestration example: adversarial critique loop, barrier sync |
| E-011 | File | `c:/AI/jerry/skills/orchestration/PLAYBOOK.md` | Lines 1-998 | 8 orchestration patterns, anti-pattern catalog, circuit breaker schema |
| E-012 | File | `c:/AI/jerry/.claude/rules/mandatory-skill-usage.md` | Lines 1-89 | Proactive skill invocation rules, trigger phrase mapping |
| E-013 | File | `c:/AI/jerry/.claude/rules/markdown-navigation-standards.md` | Lines 1-246 | NAV-001 through NAV-006 requirements, anchor link enforcement |
| E-014 | File | `c:/AI/jerry/.claude/rules/coding-standards.md` | Lines 1-270 | TYPE_CHECKING pattern, Protocol pattern, CQRS naming conventions |
| E-015 | External | Chroma Research (https://research.trychroma.com/context-rot) | N/A (web source) | Empirical evidence for context rot: LLM performance degrades as context fills with irrelevant content |
| E-016 | File | `c:/AI/jerry/skills/problem-solving/agents/ps-analyst.md` | Lines 1-554 | Convergent analysis agent: 5 Whys, FMEA, trade-off matrix; model: sonnet |
| E-017 | File | `c:/AI/jerry/skills/problem-solving/agents/ps-synthesizer.md` | Lines 1-593 | Synthesis agent: Braun & Clarke thematic analysis; PAT/LES/ASM generation; model: sonnet |
| E-018 | File | `c:/AI/jerry/skills/problem-solving/agents/ps-reviewer.md` | Lines 1-529 | Review agent: SOLID, OWASP, Google practices; severity taxonomy; model: sonnet |
| E-019 | File | `c:/AI/jerry/skills/problem-solving/agents/ps-reporter.md` | Lines 1-551 | Reporting agent: status/metrics/knowledge-summary; model: haiku |
| E-020 | File | `c:/AI/jerry/skills/problem-solving/agents/ps-validator.md` | Lines 1-512 | Validation agent: IEEE 1012, traceability matrix, binary pass/fail; model: haiku |
| E-021 | File | `c:/AI/jerry/skills/problem-solving/agents/ps-architect.md` | Lines 1-542 | Architecture agent: ADR Nygard format, C4, DDD; model: opus |

---

## Conclusions

Jerry's prompt architecture achieves effectiveness through seven design choices that work synergistically:

1. **Context management by design**: CLAUDE.md is intentionally sparse; full context is only loaded when needed. This fights context rot at the architectural level. The external empirical basis for this design choice is documented by Chroma Research (https://research.trychroma.com/context-rot), which demonstrates measurable performance degradation as context windows fill. Jerry's CLAUDE.md explicitly cites this research as the "Core Problem" the framework addresses (line 9: "Core Problem: Context Rot - LLM performance degrades as context fills. See [Chroma Research](https://research.trychroma.com/context-rot)").

2. **Structured identity priming**: The XML section pattern (`<identity>`, `<persona>`) provides role-priming that shapes all subsequent output without requiring the user to repeat role instructions.

3. **Explicit tool governance**: The `allowed_tools` list in YAML frontmatter plus the `<capabilities>` table plus the constitutional prohibitions create three-layer tool governance. Agents know what they can use, what they must not use, and why.

4. **Quantified quality gates**: Every quality requirement is expressed as a number (0.0-1.0 score), not a verbal description. This enables programmatic evaluation by the ps-critic agent.

5. **Self-enforcing persistence**: The MANDATORY PERSISTENCE protocol is stated in three ways (named protocol, numbered steps, prohibition) because human attention is variable. At least one of the three formulations will register.

6. **Anti-recursion by constitutional mandate**: P-003 (No Recursive Subagents) is the hardest constraint in the system. This prevents the most common catastrophic failure mode in multi-agent systems.

7. **Filesystem as memory**: All findings persist to structured file paths. This means a new Claude session can resume exactly where a previous one ended by reading the orchestration artifacts.

---

*Investigation Version: 1.1.0*
*Constitutional Compliance: P-001, P-002, P-003, P-004, P-011, P-022*
*Created: 2026-02-18*
*Revised: 2026-02-18 — ps-critic revision actions applied: (1) Chroma Research external citation added for context rot; (2) Extended agent coverage for all 9 PS agents (ps-analyst, ps-synthesizer, ps-reviewer, ps-reporter, ps-validator, ps-architect); (3) Cross-mapping table added (Jerry patterns vs. external survey focus areas)*
