# Jerry Prompt Best-Practices Guide

> **Document ID:** PROJ-006-SYN-001
> **Agent:** ps-synthesizer (problem-solving skill)
> **Version:** 1.0.0
> **Date:** 2026-02-18
> **Status:** COMPLETE
> **Phase:** Phase 3 — Synthesis
> **Input Artifacts:**
> - `research/external-prompt-engineering-survey.md` (ps-researcher, v1.1.0)
> - `research/jerry-internals-investigation.md` (ps-investigator, v1.1.0)
> - `analysis/prompt-pattern-analysis.md` (ps-analyst, v1.0.0)
> - `analysis/prompt-quality-rubric-taxonomy.md` (ps-architect, v1.0.0)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scope and Audience](#scope-and-audience) | What this guide covers and who it is for |
| [Introduction to Jerry's Prompt Ecosystem](#introduction-to-jerrys-prompt-ecosystem) | What Jerry is, context rot, and how prompts work |
| [Prompt Anatomy for Effective Jerry Prompts](#prompt-anatomy-for-effective-jerry-prompts) | The 5 structural elements that matter most |
| [Skill Invocation Patterns](#skill-invocation-patterns) | Single skill, multi-skill, and full orchestration |
| [Agent Composition Guidelines](#agent-composition-guidelines) | Model routing, agent selection, adversarial loops |
| [Quality Indicators and Measurable Outcomes](#quality-indicators-and-measurable-outcomes) | The quality rubric and how to use it |
| [Anti-Patterns Section](#anti-patterns-section) | What breaks Jerry prompts and how to fix it |
| [Worked Examples](#worked-examples) | Three annotated prompts from simple to complex |
| [Quick Reference Card](#quick-reference-card) | One-page cheat sheet |
| [Evidence and Traceability](#evidence-and-traceability) | Source citations for all recommendations |

---

## Scope and Audience

### What This Guide Covers

This guide covers how to write prompts that get the best results from Jerry. It synthesizes findings from:

- A survey of external prompt engineering literature (Anthropic, DAIR.AI, academic CoT and ReAct research)
- An investigation of Jerry's internal architecture (how skills, agents, and orchestration work)
- A pattern analysis mapping structural prompt traits to quality outcomes
- A quality rubric and prompt classification taxonomy

### Scope Limitation (S-001)

**The findings in this guide are grounded in analysis of Jerry's problem-solving and orchestration skills.** These two skills were investigated in depth. The worktracker, nasa-se, transcript, and architecture skills were not examined in Phase 1. Patterns described here are confirmed for problem-solving and orchestration; they are likely but not confirmed for the other skills.

### Who This Guide Is For

This guide is written for all Jerry users — from someone writing their first prompt to an experienced user composing complex multi-agent pipelines. Three experience levels correspond to three reading paths:

| Level | Recommended Sections |
|-------|---------------------|
| New to Jerry | [Introduction](#introduction-to-jerrys-prompt-ecosystem), [Anatomy](#prompt-anatomy-for-effective-jerry-prompts), [Anti-Patterns](#anti-patterns-section), [Worked Example 1](#example-1-simple-research-spike) |
| Familiar with Jerry | Full guide linearly |
| Building complex workflows | [Skill Invocation Patterns](#skill-invocation-patterns), [Agent Composition](#agent-composition-guidelines), [Quality Indicators](#quality-indicators-and-measurable-outcomes), [Worked Example 2](#example-2-multi-skill-orchestrated-workflow) |

---

## Introduction to Jerry's Prompt Ecosystem

### What Jerry Is

Jerry is a framework for behavior and workflow guardrails. It gives Claude a structured, persistent memory system organized around projects, work items, and specialized agents. When you write a prompt to Jerry, you are not just asking Claude a question — you are potentially activating a multi-agent pipeline with quality gates, adversarial critics, and filesystem-persisted state that survives across sessions.

The framework is built on a layered architecture:

```
Layer 5: CLAUDE.md (Root Context — always loaded)
  - Jerry identity, hard constraints, quick reference tables

Layer 4: .claude/rules/ (Standards — auto-loaded every session)
  - Coding standards, architecture standards, error handling

Layer 3: skills/{skill}/SKILL.md (Skill Context — loaded on invocation)
  - YAML frontmatter with activation-keywords, agent roster, Triple-Lens guide

Layer 2: skills/{skill}/agents/{agent}.md (Agent Context — loaded per agent)
  - XML-structured agent identity, constitutional checklist, state schema

Layer 1: Orchestration Artifacts (Runtime State — written by agents)
  - ORCHESTRATION.yaml, ORCHESTRATION_PLAN.md, phase artifacts
```

Each layer is loaded *only when needed*. This is not an accident — it is the core design principle that fights context rot.

### The Context Rot Problem

As a conversation grows, Claude's context window fills. Chroma Research has documented empirically that LLM performance degrades as context fills with content that is no longer relevant to the current task (https://research.trychroma.com/context-rot). Jerry's architecture fights this by keeping CLAUDE.md intentionally sparse and loading skill, agent, and orchestration context selectively.

**What this means for your prompts:** Prompts that include large amounts of background text you could instead reference by file path are fighting against Jerry's design. Lean on the filesystem. Say "Context: see projects/PROJ-006/research/auth-issue.md" rather than quoting the file's contents inline.

### How Jerry Processes Your Prompt

When you submit a prompt to Jerry, the following happens in sequence:

1. **Keyword matching**: Jerry scans your prompt for activation-keywords defined in each skill's YAML frontmatter. Words like "research," "investigate," "analyze," "orchestration," and "quality score" trigger skill loading.
2. **Explicit skill routing**: If you use `/skill-name` syntax (e.g., `/problem-solving`, `/orchestration`), that skill's context is loaded directly — no keyword matching required.
3. **Agent selection**: Within a loaded skill, the appropriate agent is selected based on your prompt content. Named agents (e.g., `orch-planner`, `ps-researcher`) are routed directly; unnamed references let Jerry infer the best fit.
4. **Execution**: The agent runs with its XML-structured identity, constitutional compliance checklist, and mandatory persistence protocol.
5. **Output persistence**: All agent outputs are written to the filesystem per the Mandatory Persistence Protocol (P-002).

The practical implication: **your prompt determines how much of Jerry's architecture gets activated.** A vague prompt activates none of it. A well-structured prompt activates the full stack.

---

## Prompt Anatomy for Effective Jerry Prompts

### The 5 Structural Elements

Analysis of effective Jerry prompts (including the canonical Salesforce privilege control example analyzed in the Phase 1/2 research) and of Jerry's internal architecture reveals five structural elements that have the highest correlation with quality outcomes:

| Element | What It Does | Example |
|---------|-------------|---------|
| **1. Explicit Skill Invocation** | Triggers YAML-based routing; loads the right agent context | `Use /problem-solving with ps-researcher...` |
| **2. Domain and Scope Specification** | Scopes agent attention; prevents hallucination of irrelevant findings | `...within Delinea, from 2024-01-01 to 2026-02-18` |
| **3. Data Source Constraint** | Tells agents which tools to use; eliminates ambiguity about data origin | `Data source: Salesforce MCP already configured against Claude` |
| **4. Numeric Quality Threshold** | Activates ps-critic's circuit breaker with the user's actual standard | `Quality factor must be >= 0.92` |
| **5. Output Specification** | Tells agents where to write and what format to use | `Output: research/privilege-control.md with L0/L1/L2 sections` |

### How These Elements Map to Jerry's Architecture

Each element maps to a specific Jerry mechanism:

```
Explicit Skill Invocation ──► YAML activation-keywords (Pattern P-01)
                               └─ Loads agent spec with XML identity priming

Domain/Scope Specification ──► Agent routing and research scoping
                               └─ Constrains ps-researcher's 5W1H exploration

Data Source Constraint ──────► Tool selection in <capabilities> section
                               └─ Channels MCP tool use; prevents hallucination

Numeric Quality Threshold ───► ps-critic circuit breaker schema
                               └─ acceptance_threshold field; stops at 0.92 not default 0.85

Output Specification ────────► Mandatory Persistence Protocol (Pattern P-05)
                               └─ Replaces default file path with user-specified path
```

### Visual Anatomy of an Effective Prompt

The following diagram shows the structure of a well-formed Jerry orchestration prompt, with each component labeled:

```
┌─────────────────────────────────────────────────────────────────────┐
│ WORK ITEM CREATION (optional anchor)                                │
│   Use /worktracker to create a Spike titled "..."                   │
│   └─ Creates traceability link between prompt and project state     │
├─────────────────────────────────────────────────────────────────────┤
│ SKILL INVOCATION + AGENT PIPELINE                                   │
│   Use /problem-solving with the following agents in order:          │
│   1. ps-researcher: [task]. Output: [path] with L0/L1/L2 sections  │
│   2. ps-analyst: [task]. Output: [path]                            │
│   └─ Explicit sequence; each agent named; each output specified     │
├─────────────────────────────────────────────────────────────────────┤
│ SCOPE AND DATA SOURCE                                               │
│   Domain: [specific topic within [org/system]]                      │
│   Time range: [start] to [end]                                      │
│   Data source: [named tool/MCP/codebase path]                       │
│   └─ Eliminates the two biggest sources of research ambiguity       │
├─────────────────────────────────────────────────────────────────────┤
│ ORCHESTRATION + QUALITY GATE                                        │
│   Use /orchestration and orch-planner to design the pipeline.       │
│   Include ps-critic adversarial critique after each phase.          │
│   Quality threshold: >= [number] per phase before proceeding.       │
│   └─ Activates adversarial loop; numeric gate overrides default     │
├─────────────────────────────────────────────────────────────────────┤
│ OUTPUT SPECIFICATION                                                │
│   Orchestration plan: orchestration/[id]/ORCHESTRATION_PLAN.md      │
│   └─ Prevents artifacts landing at default paths                    │
└─────────────────────────────────────────────────────────────────────┘
```

### The Golden Rule

Anthropic's documentation states: "Show your prompt to a colleague who has minimal context on the task and ask them to follow the instructions. If they're confused, Claude will likely be too."

For Jerry specifically: every missing element in the five-element anatomy forces Claude to make a structural decision you probably should have made. Missing quality threshold → ps-critic uses 0.85. Missing output path → artifacts go to default locations. Missing data source → agent infers or hallucinates the source.

---

## Skill Invocation Patterns

### Single Skill: When and How

Use a single skill when the task has one deliverable and maps cleanly to one skill's capabilities.

**The correct syntax:**
```
Use /problem-solving with ps-[agent-name] to [task].
Domain: [scope].
Data source: [source].
Output: [path] with [format].
```

**When to use each skill:**

| Skill | Use For | Primary Agents |
|-------|---------|---------------|
| `/worktracker` | Creating/updating work items; checking status | (directly managed) |
| `/problem-solving` | Research, investigation, analysis, synthesis, critique, validation, reporting | ps-researcher, ps-investigator, ps-analyst, ps-synthesizer, ps-critic, ps-reviewer, ps-architect, ps-validator, ps-reporter |
| `/orchestration` | Multi-phase workflows requiring coordination | orch-planner |
| `/nasa-se` | Requirements engineering, V&V, technical reviews | (se-specific agents) |
| `/architecture` | Design decisions, architectural guidance | (arch-specific agents) |

**Choosing the right problem-solving agent:**

```
Is the task open-ended exploration of a topic?
  YES → ps-researcher (divergent, breadth-first, 5W1H framework)
  NO  ↓

Is the task finding the root cause of a failure?
  YES → ps-investigator (convergent, 5 Whys, Ishikawa)
  NO  ↓

Is the task structured analysis with trade-offs?
  YES → ps-analyst (FMEA, trade-off matrix)
  NO  ↓

Is the task combining findings from multiple sources?
  YES → ps-synthesizer (Braun & Clarke thematic analysis)
  NO  ↓

Is the task making an architectural decision?
  YES → ps-architect (ADR Nygard format, C4, DDD)
  NO  ↓

Is the task reviewing existing code/design for quality?
  YES → ps-reviewer (SOLID, OWASP, Google review standards)
  NO  ↓

Is the task verifying binary pass/fail against criteria?
  YES → ps-validator (IEEE 1012, traceability matrix)
  NO  ↓

Is the task generating a status report or metrics summary?
  YES → ps-reporter (Agile status, DORA metrics)
  NO  ↓

Is the task adversarial quality scoring of an artifact?
  YES → ps-critic (Generator-Critic loop, 0.0-1.0 quality score)
```

**Single-skill example (Research Spike):**
```
Use /problem-solving with ps-researcher to survey external prompt engineering
best practices from 2023 to 2026.
Data source: web search (WebSearch and WebFetch tools).
Domain: LLM prompt engineering; focus on agentic and multi-agent patterns.
Output: research/external-prompt-engineering-survey.md with L0/L1/L2 sections.
```

### Multi-Skill Composition: Combining Skills

Use multi-skill composition when a task requires capabilities that span skill boundaries — for example, creating a work item while simultaneously running research.

**Common multi-skill combinations:**

| Combination | When to Use | Example Task |
|-------------|-------------|-------------|
| `/worktracker` + `/problem-solving` | Create a tracked work item AND execute research in the same prompt | "Create a spike and run the research" |
| `/problem-solving` + `/orchestration` | Run problem-solving agents within an orchestrated pipeline | Complex analysis with quality gates |
| `/worktracker` + `/orchestration` | Create work items that track an orchestrated workflow | Epic with orchestration plan |

**Multi-skill syntax:**
```
Use /worktracker to create a [type] titled "[title]" under [project].

Use /problem-solving with ps-researcher to [task].
Data source: [source].
Output: [path].

Use /orchestration and orch-planner to coordinate the above.
Quality threshold: >= [number].
```

**Key rule:** Order matters. Place work-item creation first (it creates the traceability anchor), research/analysis second, and orchestration coordination last (it wraps and sequences everything else).

### Orchestrated Workflows: Full Pipeline Prompts

Orchestrated workflows are the most powerful Jerry prompt pattern. They activate the full architectural stack: orch-planner creates an ORCHESTRATION_PLAN.md, agents execute in defined phases, ps-critic enforces quality gates between phases, and all artifacts persist to the filesystem.

**When to use orchestration:**
- The task has more than two distinct phases
- Quality assurance at phase boundaries matters (not just final output quality)
- Results need to be reproducible across sessions
- Multiple agents in sequence are needed

**The headline recommendation for orchestration (S-006):**

> The Adversarial Critique Loop — requesting ps-critic adversarial review at each phase boundary with a numeric quality threshold — is the single highest-impact pattern available in Jerry. It has the largest quality uplift of any prompt element. Most prompts that would benefit from it do not request it.
>
> If you are doing anything that matters — architecture decisions, security analysis, research synthesis that will inform real decisions — always include: "adversarial critics at every phase; quality factor must be >= [threshold]."

**Orchestrated workflow template:**
```
Use /worktracker to create a [type] titled "[title]" under [project].

Use /problem-solving to invoke the following agents in order:
1. ps-researcher: [specific task]. Data source: [source]. Output: [path] with L0/L1/L2.
2. ps-analyst: [specific task]. Input: researcher output. Output: [path].
3. ps-architect: [specific task]. Input: analyst output. Output: [path] in Nygard ADR format.

Use /orchestration and orch-planner to design the above as a pipeline.
Include ps-critic adversarial critique after each phase; quality threshold >= [number].
Output orchestration plan: orchestration/[workflow-id]/ORCHESTRATION_PLAN.md.
```

---

## Agent Composition Guidelines

### Model Routing: How Jerry Assigns Models

Jerry routes each agent to one of three Claude model tiers based on task complexity. This happens automatically via the `model:` field in each agent's YAML frontmatter — you do not need to specify a model tier in your prompts.

| Model Tier | Agents | Characteristics |
|------------|--------|----------------|
| **Opus** | ps-researcher, ps-architect | Open-ended exploration; complex multi-factor reasoning; architectural decisions |
| **Sonnet** | ps-analyst, ps-synthesizer, ps-critic, ps-reviewer, ps-investigator | Balanced analysis; structured evaluation; convergent reasoning |
| **Haiku** | ps-validator, ps-reporter | Fast structured tasks; binary pass/fail; metrics aggregation |

**What this means for prompt writing:**

When writing prompts for Opus-tier agents (ps-researcher, ps-architect), prefer **high-level goal directives** over prescriptive step-by-step instructions. Anthropic's Extended Thinking documentation states: "Claude often performs better with high-level instructions to just think deeply about a task rather than step-by-step prescriptive guidance." This is the correct calibration for Opus.

When writing prompts that will route to Haiku-tier agents (ps-validator, ps-reporter), be **maximally explicit and structured**. Haiku-tier agents benefit from tightly defined output formats and concrete acceptance criteria. Vague instructions produce worse results at this tier than at higher tiers.

Sonnet-tier agents (ps-analyst, ps-critic, ps-investigator, etc.) fall between these extremes — structured evaluation criteria and frameworks improve their output, but they do not need to be micromanaged.

### When to Request Specific Agents vs. Letting Jerry Choose

**Request a specific agent when:**
- You know the cognitive mode needed (divergent research vs. convergent investigation)
- You need a specific output format (ADR from ps-architect; binary pass/fail from ps-validator)
- You are chaining agents in a defined sequence
- You are inviting a specific critique role (adversarial critique via ps-critic)

**Let Jerry infer when:**
- The task is straightforward and the skill's activation-keywords are sufficient
- You are using a simple single-skill prompt with one clear deliverable
- You are uncertain which agent is most appropriate

**Warning:** Requesting the wrong agent does not produce an error — it produces output in the wrong cognitive mode. "Research why X is failing" routes to ps-researcher (divergent, breadth-first), when you actually wanted ps-investigator (convergent, root-cause). See [AP-04 Cognitive Mode Mismatch](#ap-04-cognitive-mode-mismatch) in the Anti-Patterns section.

### The Power of Adversarial Critic Loops

**This is the most important recommendation in this guide (S-006).**

The Adversarial Critique Loop (Pattern P-07) is Jerry's highest-impact quality mechanism. It is only activated when explicitly requested in a prompt. Most prompts do not request it.

**How it works:**

```
Phase N Output
    │
    ▼
ADVERSARIAL CRITIQUE (ps-critic)
  ├── Devil's Advocate: Challenge the core assumptions
  ├── Steelman: Find the strongest counter-arguments
  ├── Red Team: Attack for vulnerabilities and gaps
  └── Blue Team: Defend and validate the strongest points
    │
    ▼
REVISION (ps-architect or generator agent)
  └── Incorporates critique feedback
    │
    ▼
CIRCUIT BREAKER CHECK
  ├── quality_score >= acceptance_threshold → proceed to Phase N+1
  └── quality_score < threshold, iterations < 3 → loop back to critique
```

The circuit breaker prevents infinite loops: ps-critic stops after 3 iterations regardless, and also stops when quality score meets the threshold or when two consecutive iterations show no improvement.

**How to invoke the adversarial critique loop:**
```
Include ps-critic adversarial critique after each phase.
Quality threshold: >= 0.92.
```

Or more explicitly:
```
After each phase output, have ps-critic apply the four adversarial critique modes
(Devil's Advocate, Steelman, Red Team, Blue Team). The producing agent must revise
based on critique before proceeding to the next phase. Quality threshold: >= 0.90.
Maximum 3 critique iterations per phase.
```

**When to use it:**
- Architecture decisions (ADRs)
- Security analysis
- Research synthesis that will inform real decisions
- Any analysis where being wrong has significant consequences

**The utilization gap:** Analysis of Jerry's prompt patterns found that the Adversarial Critique Loop has the highest quality impact of any pattern but is the one most often omitted from prompts that would benefit from it. The default ps-critic circuit breaker threshold of 0.85 fires only if you explicitly request critique; without the request, no critique loop runs at all.

---

## Quality Indicators and Measurable Outcomes

### The Quality Rubric (Summary)

The full rubric is documented in `analysis/prompt-quality-rubric-taxonomy.md` (ps-architect, PROJ-006-ARCH-001). This section provides a practical summary.

**Seven scoring criteria (higher weight = more impact):**

| # | Criterion | Weight | Quick Test |
|---|-----------|--------|------------|
| C1 | Task Specificity | 20% | Count undefined terms and incomplete clauses |
| C2 | Skill Routing | 18% | Are skills named with `/skill` syntax? Agents named? |
| C3 | Context Provision | 15% | Is necessary context present without padding? |
| C4 | Quality Specification | 15% | Is there a numeric threshold or named review mechanism? |
| C5 | Decomposition | 12% | Are multi-step tasks broken into named phases? |
| C6 | Output Specification | 12% | Is output format, location, and structure explicit? |
| C7 | Positive Framing | 8% | Does the prompt state what to do, not what to avoid? |

**Score thresholds:**

| Score (0-100) | Tier | Expected Behavior |
|---------------|------|------------------|
| 90-100 | Exemplary | Completes without clarification; artifacts at correct paths; quality gates triggered at specified thresholds |
| 75-89 | Proficient | Functionally correct; artifacts may go to default paths; minor clarification may be needed |
| 50-74 | Developing | Completes primary task; structural decisions (paths, thresholds, order) made by Claude rather than user |
| 0-49 | Inadequate | Requires significant clarification; likely misses intent; multiple rework rounds |

**Scored example — the Salesforce privilege control prompt:**

The canonical example prompt from Phase 1 ("Claude use the /worktracker skill to create a spike...") scores 76.3 (Tier 3 — Proficient). Its C4 quality specification (3/3) and C2 skill routing (3/3) are exemplary. Its C6 output specification (1/3) and one incomplete clause (C1 deduction) are the primary gaps.

### How to Specify Quality Thresholds

Quality thresholds in Jerry prompts directly control ps-critic's circuit breaker `acceptance_threshold` field. Without a user-specified threshold, ps-critic defaults to 0.85.

**Threshold selection guidance:**

| Task Type | Recommended Threshold | Rationale |
|-----------|----------------------|-----------|
| Exploratory research / first drafts | 0.80-0.85 | Lower bar for early-stage exploration; iteration expected |
| Architecture decisions (ADRs) | 0.90-0.92 | High stakes; errors persist; adversarial review critical |
| Security analysis | 0.92-0.95 | Very high stakes; false confidence is costly |
| Status reports / summaries | 0.75-0.80 | Lower stakes; speed matters; ps-reporter handles well at Haiku |
| Code review / validation | 0.85-0.90 | Structured criteria make scoring reliable at this range |

**The 0.92 threshold pattern:** The Salesforce prompt's `>=0.92` threshold is calibrated to the "architecture + security" zone of the table above. This is a reasonable default for complex, consequence-bearing research. It is not a magic number — calibrate to the stakes of the specific task.

### Specifying Quality Without a Number (When Verbal Descriptors Are Acceptable)

Verbal quality descriptors ("ensure the analysis is thorough") are the weakest quality signal. They do not give ps-critic a numeric target, so the circuit breaker defaults to 0.85. However, verbal descriptors combined with a named review mechanism are better than no quality signal:

```
Have ps-critic review each phase output before proceeding.
Apply adversarial critique with the four-mode approach.
```

This is a C4 score of 2/3 — acceptable for lower-stakes tasks, but upgrade to a numeric threshold for anything consequential.

---

## Anti-Patterns Section

Eight anti-patterns degrade Jerry prompt quality. They are ordered by their frequency and impact, with the highest-impact patterns first. Each includes a before/after example.

---

### AP-01: Vague Directives Without Skill Routing (HIGHEST IMPACT)

**Why it fails:** Without `/skill-name` syntax or activation keywords, Jerry's YAML frontmatter routing is not triggered. Claude responds from its base capabilities rather than routing through the appropriate agent. The XML-structured agent identity, constitutional compliance checklist, mandatory persistence protocol, and state schema are all bypassed.

**Before:**
```
Can you help me research the authentication service issues?
```

**After:**
```
Use /problem-solving with ps-investigator to determine the root cause of
authentication service failures.
Domain: authentication-service in the inventory project (src/Delinea.Inventory.Logic/).
Data source: codebase and existing logs at projects/PROJ-006/research/.
Output: investigations/auth-service-root-cause.md.
```

**What changed:** Explicit skill invocation (routes to correct agent), cognitive mode alignment (ps-investigator for root-cause, not ps-researcher for survey), data source named, output path specified.

---

### AP-02: Missing Quality Thresholds

**Why it fails:** ps-critic's circuit breaker defaults to quality_score >= 0.85 when no threshold is specified. For high-stakes tasks (architecture decisions, security analysis), 0.85 may be insufficient. Without any threshold, no critique loop activates at all — ps-critic is simply not invoked.

**Before:**
```
Use orchestration with adversarial critics to analyze the API design.
```

**After:**
```
Use /orchestration and orch-planner to analyze the API design using ps-architect.
Include ps-critic adversarial critique after the initial design review.
Quality threshold: >= 0.90 before proceeding to implementation recommendations.
```

**What changed:** Numeric threshold added (0.90, appropriate for architecture); orch-planner named explicitly; adversarial critique request present.

---

### AP-03: Monolithic Prompts Without Decomposition

**Why it fails:** The model must allocate attention sequentially across all tasks in one pass. Complex early tasks consume context budget, degrading later tasks. Jerry's orchestration layer is not activated without explicit `/orchestration` invocation.

**Before:**
```
Analyze our Salesforce data, identify patterns, build an orchestration plan,
critique it, implement improvements, document everything, and create work items.
```

**After:**
```
Use /worktracker to create an Epic titled "Salesforce Analysis Pipeline" under PROJ-006.

Phase 1: Use /problem-solving with ps-researcher to gather Salesforce opportunity data
from 2024-01-01 to 2026-02-18. Data source: Salesforce MCP. Output: research/sf-data.md.

Phase 2: Use /problem-solving with ps-analyst to identify patterns. Input: Phase 1 output.
Output: analysis/sf-patterns.md.

Use /orchestration and orch-planner to sequence Phase 1 and Phase 2 with ps-critic
adversarial critique between phases. Quality threshold: >= 0.90.
Orchestration plan: orchestration/sf-analysis-20260218-001/ORCHESTRATION_PLAN.md.
```

**What changed:** Explicit phases with names; work item anchor; orchestration invoked with orch-planner; quality threshold specified; output paths for each phase.

---

### AP-04: Cognitive Mode Mismatch

**Why it fails:** Using "research" language routes to ps-researcher (divergent, 5W1H), but investigation tasks need ps-investigator (convergent, 5 Whys). ps-researcher produces broad landscape findings; ps-investigator produces a specific root cause.

**Before:**
```
Research why the authentication service is failing.
```

**After (for root-cause investigation):**
```
Use /problem-solving with ps-investigator to determine the root cause of
authentication service failures. Apply the 5 Whys methodology.
Domain: authentication-service in src/Delinea.Inventory.Logic/.
Output: investigations/auth-service-root-cause.md.
```

**After (for landscape research):**
```
Use /problem-solving with ps-researcher to survey all known authentication
patterns and known failure modes for token-based auth in .NET microservices.
Data source: web search + codebase.
Output: research/auth-patterns-survey.md with L0/L1/L2 sections.
```

**What changed:** Agent named explicitly; cognitive mode aligned with intent; task language matches agent methodology.

---

### AP-05: Context Overload (Irrelevant Background)

**Why it fails:** Jerry's architecture is designed around context rot avoidance. Large blocks of inline context consume the shared context window budget occupied by auto-loaded rules files, skill specs, and agent prompts. This can crowd out essential context or force partial truncation of skill files.

**Before:**
```
I've been working on this project for three months. The system uses CosmosDB for
storage and has a microservices architecture. We have five services: authentication,
inventory, reporting, billing, and notifications. The authentication service uses JWT
tokens with a 15-minute expiry. We recently migrated from NEST to Elasticsearch v9...
[300 more words of background]
Use /problem-solving with ps-investigator to find the root cause of auth failures.
```

**After:**
```
Context: project overview at projects/PROJ-006/PLAN.md; auth service details at
projects/PROJ-006/research/auth-service-overview.md.
Use /problem-solving with ps-investigator to determine the root cause of
authentication service failures.
Output: investigations/auth-root-cause.md.
```

**What changed:** Background moved to referenced files; prompt contains only the minimum context Claude does not already have from persistent sources (CLAUDE.md, auto-loaded rules).

---

### AP-06: Incomplete Clause Specification

**Why it fails:** Partially-specified scopes force the agent to infer intent. This is the hidden failure mode in otherwise well-structured prompts. The Salesforce prompt's incomplete clause ("as well as focus on the patterns of the") was identified in Phase 1 as the single gap that most reduces the prompt's C1 score.

**Before:**
```
Analyze the opportunities as a whole as well as focus on the patterns of the
```

**After:**
```
Analyze two dimensions:
1. Macro opportunity trends: total deal volume, average deal size, win/loss rates.
2. Sales lifecycle patterns: stage transition times, activities correlated with wins.
```

**What changed:** Incomplete trailing clause replaced with two explicit, complete scope dimensions. No inference required.

---

### AP-07: Conflicting Instructions Across Skill Boundaries (HYPOTHESIS)

**Note:** This anti-pattern is hypothesis-status. It is derived from Jerry's documented hard constraints rather than from an observed prompt failure. Flag: not a confirmed failure mode from Phase 1 evidence.

**Why it would fail:** Jerry's P-003 constitutional constraint (No Recursive Subagents) is the hardest constraint in the system. Any prompt requesting subagent spawning creates an irresolvable conflict. The agent declines, and the entire prompt execution is wasted.

**Example that would fail:**
```
Use /problem-solving to have ps-researcher spawn a research sub-team
to investigate all 15 open issues in parallel.
```

**Correct alternative:**
```
Use /orchestration and orch-planner to design a parallel investigation pipeline
for the 15 open issues. Each issue should be assigned to ps-investigator via
parallel barrier-sync pattern. Quality threshold: >= 0.88 per investigation.
```

**What changed:** Parallel execution requested through orch-planner's native barrier-sync pattern rather than through subagent spawning.

---

### AP-08: Missing Output Specification

**Why it fails:** When an output path is not specified, agents use the default path template from their invocation protocol. Default paths may not be where you expect them. Cross-session retrieval fails when artifacts are scattered at default locations rather than organized by project.

**Before:**
```
Use /problem-solving with ps-architect to design the persistence strategy.
```

**After:**
```
Use /problem-solving with ps-architect to evaluate three persistence options for
Jerry work items: (1) YAML files, (2) SQLite, (3) event store with JSON snapshots.
Evaluation dimensions: read latency, write simplicity, corruption recovery.
Output: decisions/ADR-001-persistence-strategy.md in Nygard ADR format.
```

**What changed:** Output path specified (decisions/ADR-001...); format specified (Nygard ADR); evaluation dimensions named (removes C1 ambiguity simultaneously).

---

## Worked Examples

### Example 1: Simple Research Spike (Annotated)

**The prompt:**
```
Use /problem-solving with ps-researcher to survey external prompt engineering
best practices from 2023 to 2026.
Data source: web search (WebSearch and WebFetch tools).
Domain: LLM prompt engineering; focus on agentic and multi-agent patterns.
Output: research/external-prompt-engineering-survey.md with L0/L1/L2 sections.
```

**Annotation:**

| Element | Text | Why It Works |
|---------|------|-------------|
| Skill invocation | `/problem-solving` | Loads problem-solving skill context via YAML routing |
| Agent selection | `ps-researcher` | Correct agent for divergent survey task (5W1H framework, opus model) |
| Data source | `web search (WebSearch and WebFetch tools)` | Tells ps-researcher exactly which tools to use; prevents hallucination |
| Domain scope | `LLM prompt engineering; focus on agentic and multi-agent patterns` | Narrows the breadth-first research; "agentic patterns" focus is the key constraint |
| Time scope | `from 2023 to 2026` | Bounds the research temporally; removes stale content risk |
| Output path | `research/external-prompt-engineering-survey.md` | Exact file path per Mandatory Persistence Protocol; cross-session retrievable |
| Output format | `with L0/L1/L2 sections` | Triggers Triple-Lens output framework; ensures usable output for multiple audiences |

**Rubric score:** Tier 3 (Proficient) — approximately 82/100. C4 quality specification is 0 (no threshold), which is acceptable for pure research that will be critiqued in a downstream phase. Upgrade to Tier 4 by adding a quality gate if this research feeds consequential decisions.

**What this prompt activates in Jerry's architecture:**
- YAML frontmatter routing in problem-solving SKILL.md (activation-keyword: "research")
- ps-researcher agent spec loaded (divergent cognitive mode, 5W1H framework, opus model)
- Constitutional compliance checklist runs before output
- Mandatory persistence to specified path

---

### Example 2: Multi-Skill Orchestrated Workflow (Annotated)

**Based on the Salesforce privilege control use case from Phase 1, revised to Tier 4.**

**The prompt:**
```
Use /worktracker to create a Spike titled "Privilege Control for Servers Sales Trends
Q1-2026" under PROJ-006.

Use /problem-solving to invoke the following agents in order:
1. ps-researcher: gather Salesforce opportunity data for Privilege Control for Servers
   from 2024-01-01 to 2026-02-18 via Salesforce MCP. Focus on: deal volume, stage
   transitions, win/loss patterns, and key activities correlated with closed-won.
   Output: research/privilege-control-salesforce-data.md with L0/L1/L2 sections.

2. ps-analyst: analyze the sales lifecycle patterns and macro opportunity trends
   from the researcher output. Apply FMEA analysis to identify risk patterns in
   the sales process.
   Output: analysis/privilege-control-analysis.md.

3. ps-architect: synthesize findings into strategic recommendations. Evaluate two
   strategic options: (A) intensified mid-funnel support, (B) top-of-funnel expansion.
   Dimensions: cost, time-to-impact, reversibility.
   Output: decisions/ADR-privilege-control-strategy.md in Nygard ADR format.

Use /orchestration and orch-planner to orchestrate the above pipeline.
Include ps-critic adversarial critique after each of the three phases.
Quality threshold: >= 0.92 per phase before proceeding.
Output orchestration plan: orchestration/privilege-control-20260218-001/ORCHESTRATION_PLAN.md.
```

**Annotation:**

| Element | Text | Why It Works |
|---------|------|-------------|
| Work item anchor | `/worktracker ... create a Spike` | Creates traceability to project state; named type and title |
| Agent 1 scope | `Salesforce MCP ... 2024-01-01 to 2026-02-18` | Data source + time range = zero ambiguity for research |
| Agent 1 focus | `deal volume, stage transitions, win/loss patterns...` | Four explicit research dimensions; no trailing-off (avoids AP-06) |
| Agent 2 method | `Apply FMEA analysis` | Names the methodology; ps-analyst knows FMEA; output is structured |
| Agent 3 options | `Option A: ..., Option B: ...` | Explicit options with dimensions = Decision Analysis type (ps-architect) |
| Adversarial loop | `ps-critic ... after each of the three phases` | Activates P-07 per-phase, not just at the end |
| Quality threshold | `>= 0.92 per phase` | Overrides ps-critic default (0.85); applies to each of 3 phases |
| Orchestration path | `orchestration/privilege-control-20260218-001/ORCHESTRATION_PLAN.md` | Exact path; discoverable across sessions |

**Rubric score:** Tier 4 (Exemplary) — approximately 94/100. All five structural elements present. Zero incomplete clauses. Numeric threshold present. Each agent has a named output path and format.

**Comparison to the original Salesforce prompt:**

| Issue in Original | Fixed In This Version |
|------------------|----------------------|
| Trailing incomplete clause ("patterns of the") | Four explicit research dimensions listed |
| No output paths specified | Each agent has explicit output path |
| No time scope | `2024-01-01 to 2026-02-18` added |
| Agent sequence implied | Agents numbered 1, 2, 3 with explicit sequence |
| No per-agent output format | Agent 3 specifies Nygard ADR format |

---

### Example 3: Implementation Task (Annotated)

**The prompt:**
```
Use /problem-solving with ps-reviewer to review the new UpdateAssetHandler
implementation for code quality and correctness.

Input artifact: src/Delinea.Inventory.Logic/Handlers/Commands/UpdateAssetHandler.cs
Review dimensions:
- SOLID principles compliance (especially SRP and DIP)
- NSubstitute mock setup correctness in UpdateAssetHandlerTests.cs
- Exception handling: must catch specific exceptions, not base Exception class
- Coverage: verify test coverage >= 90% on all branches

Output: reviews/update-asset-handler-review.md with CRITICAL/HIGH/MEDIUM/LOW
severity classification per finding.
```

**Annotation:**

| Element | Text | Why It Works |
|---------|------|-------------|
| Agent selection | `ps-reviewer` | Correct agent for code review (SOLID, OWASP, severity taxonomy) |
| Input artifact | `src/.../UpdateAssetHandler.cs` | Exact file path; no ambiguity about what is being reviewed |
| Review dimensions | Four specific, named dimensions | Gives ps-reviewer concrete criteria; prevents generic output |
| Coding standard alignment | `Exception handling: must catch specific...` | Aligns to auto-loaded coding-standards.md requirements |
| Coverage criterion | `test coverage >= 90%` | Numeric threshold (C4 quality signal); binary verifiable |
| Output format | `CRITICAL/HIGH/MEDIUM/LOW severity per finding` | ps-reviewer's native severity taxonomy; structured output |

**Rubric score:** Tier 3-4 (Proficient-Exemplary) — approximately 87/100. Strong C1 (specific dimensions), C2 (ps-reviewer named), C4 (coverage threshold). Would reach Tier 4 by adding explicit output path.

**Jerry-specific note:** The exception handling criterion in this prompt directly aligns with the auto-loaded coding standard (`.claude/rules/coding-standards.md`): "Always catch specific exceptions — Never catch the base Exception class." Prompts that explicitly reference or echo auto-loaded standards reinforce them and make ps-reviewer's review criteria unambiguous.

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────────┐
│              JERRY PROMPT QUICK REFERENCE                           │
├─────────────────────────────────────────────────────────────────────┤
│ THE 5 ELEMENTS (in order of impact)                                 │
│                                                                     │
│ 1. SKILL ROUTING    Use /problem-solving with ps-[agent]            │
│ 2. SCOPE            Domain: X. Time: start to end.                  │
│ 3. DATA SOURCE      Data source: [named tool or MCP]                │
│ 4. QUALITY GATE     Quality threshold: >= 0.90                      │
│ 5. OUTPUT PATH      Output: path/to/artifact.md with [format]       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ AGENT SELECTION                                                     │
│                                                                     │
│ Survey / landscape research       → ps-researcher (opus)            │
│ Root cause investigation          → ps-investigator (sonnet)        │
│ Structured trade-off analysis     → ps-analyst (sonnet)             │
│ Cross-document synthesis          → ps-synthesizer (sonnet)         │
│ Architecture decision (ADR)       → ps-architect (opus)             │
│ Code / design review              → ps-reviewer (sonnet)            │
│ Binary pass/fail validation       → ps-validator (haiku)            │
│ Status / metrics report           → ps-reporter (haiku)             │
│ Quality score with critique       → ps-critic (sonnet)              │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ TOP RECOMMENDATION (S-006)                                          │
│                                                                     │
│ For anything that matters, add this to your orchestration prompt:   │
│                                                                     │
│   Include ps-critic adversarial critique after each phase.          │
│   Quality threshold: >= [0.90 for architecture, 0.85 for research]  │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ ANTI-PATTERN CHECKLIST (before submitting)                          │
│                                                                     │
│ [ ] All clauses complete? (no trailing fragments)                   │
│ [ ] Skills named with /slash syntax?                                │
│ [ ] Data source named?                                              │
│ [ ] Quality threshold present?                                      │
│ [ ] Output path(s) specified?                                       │
│ [ ] All instructions state what TO DO (not what to avoid)?          │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ QUALITY TIER LOOKUP                                                 │
│                                                                     │
│ Score 90-100 → Tier 4 Exemplary    (no clarification needed)        │
│ Score 75-89  → Tier 3 Proficient   (works; default paths used)      │
│ Score 50-74  → Tier 2 Developing   (structural decisions by Claude) │
│ Score 0-49   → Tier 1 Inadequate   (significant clarification)      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Evidence and Traceability

All recommendations in this guide trace to evidence from Phase 1 and Phase 2 artifacts. The following table provides traceability for each major recommendation.

| Recommendation | Evidence Source | Evidence Type |
|---------------|-----------------|---------------|
| Use `/skill` syntax for invocation | jerry-internals-investigation.md, Finding 1 (YAML activation-keywords); prompt-pattern-analysis.md, Category 1 | Confirmed |
| Name specific agents when known | prompt-pattern-analysis.md, Category 1 Correlation Map; jerry-internals, User Prompt Analysis | Confirmed |
| Include numeric quality threshold | jerry-internals, Finding 7 (ps-critic circuit breaker schema); prompt-quality-rubric-taxonomy.md, C4 criterion | Confirmed |
| Adversarial critique loop is highest-impact | prompt-pattern-analysis.md, Pattern Frequency Analysis (P-07 "VERY HIGH" impact, "SOMETIMES" frequency — the gap) | Confirmed |
| Specify output path explicitly | jerry-internals, Finding 5 (Mandatory Persistence Protocol); prompt-quality-rubric-taxonomy.md, C6 criterion | Confirmed |
| Context rot: reference files instead of quoting | jerry-internals, L0 Executive Summary (Chroma Research citation); prompt-pattern-analysis.md, AP-05 | Confirmed |
| Opus agents benefit from high-level goals | external-prompt-engineering-survey.md, Section 4.5 (Extended Thinking Tips); jerry-internals, Section 8 cross-map | Confirmed (external); supported for Jerry (internal) |
| Haiku agents need explicit instructions | external-prompt-engineering-survey.md, Section 8.2; jerry-internals, Extended Agent Coverage | Supported |
| Cognitive mode: research vs. investigate language | jerry-internals, Extended Agent Coverage (cognitive_mode field); prompt-pattern-analysis.md, AP-04 | Hypothesis-supported (no controlled comparison exists) |
| 4 adversarial critique modes (Devil's Advocate etc.) | jerry-internals, Finding 7 (ORCHESTRATION_PLAN.md evidence) | Confirmed |
| ps-critic default threshold is 0.85 | jerry-internals, Finding 7 (circuit_breaker stop_conditions); prompt-quality-rubric-taxonomy.md, JE4 | Confirmed |
| Triple-Lens L0/L1/L2 output framework | jerry-internals, Finding 3; problem-solving SKILL.md lines 32-41 | Confirmed |
| AP-07 conflicting instructions (P-003 violation) | jerry-internals, Conclusions; prompt-pattern-analysis.md, AP-07 | Hypothesis (not observed in Phase 1) |

### Items Intentionally Not Covered

The following items are excluded from this guide with justification:

| Excluded Item | Reason |
|--------------|--------|
| Worktracker, nasa-se, transcript, architecture skill patterns | Not investigated in Phase 1; guide scope limited to confirmed findings (S-001) |
| Few-shot example construction for user prompts | Jerry's agent specs already embed examples; users reference templates, not construct examples inline |
| Context window token economics | No empirical baseline in existing literature; excluded per prompt-quality-rubric-taxonomy.md intentional exclusions |
| Model-tier selection by user | Jerry handles model routing internally via YAML `model:` field; users do not select model tiers |

---

*Guide Version: 1.0.0*
*Agent: ps-synthesizer*
*Constitutional Compliance: P-001 (all claims cited), P-002 (persisted to two paths), P-003 (no subagents), P-022 (hypotheses and scope limitations flagged)*
*Created: 2026-02-18*
*Source Artifacts: external-prompt-engineering-survey.md (v1.1.0), jerry-internals-investigation.md (v1.1.0), prompt-pattern-analysis.md (v1.0.0), prompt-quality-rubric-taxonomy.md (v1.0.0)*
