# Problem-Solving Orchestration

> **Technical Guide for Agent Orchestration**
> Version: 2.0.0

This document explains how the Problem-Solving agents are orchestrated, how state flows between them, and how to build custom workflows.

---

## Table of Contents

1. [Orchestration Architecture](#orchestration-architecture)
2. [Agent Selection](#agent-selection)
3. [State Management](#state-management)
4. [Workflow Patterns](#workflow-patterns)
5. [Building Custom Workflows](#building-custom-workflows)
6. [Constitutional Constraints](#constitutional-constraints)

---

## Orchestration Architecture

### Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     USER REQUEST                             │
│            "Research and decide on a caching solution"      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR                             │
│                                                              │
│  1. Parse request keywords                                  │
│  2. Match to agent capabilities                             │
│  3. Determine sequence (single/chain)                       │
│  4. Invoke agents via Task tool                             │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       ┌────────────┐  ┌────────────┐  ┌────────────┐
       │ps-researcher│  │ ps-analyst │  │ps-architect│
       └────────────┘  └────────────┘  └────────────┘
              │               │               │
              ▼               ▼               ▼
       ┌────────────┐  ┌────────────┐  ┌────────────┐
       │docs/research│  │docs/analysis│  │docs/decisions│
       └────────────┘  └────────────┘  └────────────┘
```

### Key Principles

1. **Single-Level Delegation (P-003)**
   - Orchestrator can invoke agents
   - Agents CANNOT invoke other agents
   - Maximum nesting depth: 1 level

2. **Mandatory Persistence (P-002)**
   - Every agent MUST create a file
   - No transient-only output allowed
   - Files survive context compaction

3. **State Passing**
   - Agents communicate via files
   - State keys reference output locations
   - No in-memory state sharing

---

## Agent Selection

### Keyword Matching

The orchestrator selects agents based on keywords in the user request:

| Keywords | Selected Agent |
|----------|----------------|
| research, explore, find, gather, investigate options, what are the options, compare | `ps-researcher` |
| analyze, root cause, trade-off, gap, risk, 5 whys, FMEA, why did | `ps-analyst` |
| ADR, architecture decision, design decision, choose, decide, should we use | `ps-architect` |
| validate, verify, constraint, test, evidence, check if, are we meeting | `ps-validator` |
| synthesize, patterns, themes, combine, meta-analysis, across documents | `ps-synthesizer` |
| review, quality, code review, security, OWASP, assess, evaluate code | `ps-reviewer` |
| investigate, failure, incident, debug, what happened, why did it fail | `ps-investigator` |
| report, status, progress, metrics, summary, how are we doing | `ps-reporter` |

### Priority Rules

When multiple keywords match, priority is:

1. **Explicit agent name** - "Use ps-researcher..." always wins
2. **Problem keywords** - "investigate failure" → ps-investigator
3. **Analysis keywords** - "analyze trade-offs" → ps-analyst
4. **Research keywords** - "research options" → ps-researcher

### Examples

```
"What are the best caching options?"
→ Keywords: "options" → ps-researcher

"Why are our tests flaky?"
→ Keywords: "why" → ps-analyst (root cause)

"Create an ADR for choosing Redis"
→ Keywords: "ADR", "choosing" → ps-architect

"Check if we meet the security requirements"
→ Keywords: "check if", "requirements" → ps-validator

"Find patterns across the research documents"
→ Keywords: "patterns", "across" → ps-synthesizer

"Review the authentication module"
→ Keywords: "review" → ps-reviewer

"What happened with the production outage?"
→ Keywords: "what happened" → ps-investigator

"Generate a status report for Phase 3"
→ Keywords: "status report" → ps-reporter
```

---

## State Management

### Output Keys

Each agent produces an output key that can be referenced by downstream agents:

```yaml
# ps-researcher
researcher_output:
  ps_id: "work-024"
  entry_id: "e-101"
  artifact_path: "docs/research/work-024-e-101-caching.md"
  summary: "Evaluated Redis, Memcached, and Hazelcast..."
  sources: ["redis.io", "memcached.org", "hazelcast.com"]
  next_agent_hint: "ps-architect for design decision"

# ps-analyst
analyst_output:
  ps_id: "work-024"
  entry_id: "e-102"
  artifact_path: "docs/analysis/work-024-e-102-root-cause.md"
  analysis_type: "root-cause"
  root_cause: "Database connection pool exhaustion"
  confidence: "high"
  next_agent_hint: "ps-architect for fix design"

# ps-architect
architect_output:
  ps_id: "work-024"
  entry_id: "e-103"
  artifact_path: "docs/decisions/work-024-e-103-adr-caching.md"
  adr_number: "ADR-015"
  decision: "Use Redis with Sentinel for HA"
  status: "PROPOSED"
  next_agent_hint: "ps-validator for design review"

# ps-validator
validator_output:
  ps_id: "work-024"
  entry_id: "e-104"
  artifact_path: "docs/analysis/work-024-e-104-validation.md"
  validated_count: 8
  total_count: 10
  pass_rate: "80%"
  gaps: ["c-007 performance benchmark", "c-009 disaster recovery"]
  next_agent_hint: "ps-reporter for status report"
```

### State Flow Between Agents

```
┌─────────────────┐
│  ps-researcher  │
│                 │
│  Creates:       │
│  researcher_    │
│  output         │
└────────┬────────┘
         │ References artifact_path
         ▼
┌─────────────────┐
│  ps-architect   │
│                 │
│  Reads:         │
│  researcher_    │
│  output.        │
│  artifact_path  │
│                 │
│  Creates:       │
│  architect_     │
│  output         │
└────────┬────────┘
         │ References artifact_path
         ▼
┌─────────────────┐
│  ps-validator   │
│                 │
│  Reads:         │
│  architect_     │
│  output.        │
│  artifact_path  │
└─────────────────┘
```

### Referencing Previous Output

When invoking a downstream agent, include the upstream artifact:

```python
Task(
    description="ps-architect: Caching ADR",
    subagent_type="general-purpose",
    prompt="""
You are the ps-architect agent (v2.0.0).

## PS CONTEXT (REQUIRED)
- **PS ID:** work-024
- **Entry ID:** e-103
- **Decision Topic:** Caching Solution

## UPSTREAM ARTIFACTS
- Research: docs/research/work-024-e-101-caching.md

Read the research document before creating the ADR.
Reference findings and sources in your decision rationale.

## MANDATORY PERSISTENCE (P-002)
Create file at: docs/decisions/work-024-e-103-adr-caching.md
"""
)
```

---

## Workflow Patterns

### Pattern 1: Single Agent

**Use When:** Task is focused and self-contained.

```
User: "Research graph database options"

Orchestrator:
  - Identifies: research task
  - Selects: ps-researcher
  - Invokes: Single Task

Output:
  - docs/research/work-024-e-001-graph-databases.md
```

### Pattern 2: Sequential Chain

**Use When:** Problem requires multiple perspectives in order.

```
User: "Research, analyze trade-offs, then decide on database"

Orchestrator:
  1. Invoke ps-researcher → docs/research/...
  2. Wait for completion
  3. Invoke ps-analyst with research reference → docs/analysis/...
  4. Wait for completion
  5. Invoke ps-architect with research + analysis → docs/decisions/...

State Flow:
  researcher_output → analyst_output → architect_output
```

### Pattern 3: Fan-Out (Parallel)

**Use When:** Multiple independent research streams.

```
User: "Research caching, queuing, and storage options"

Orchestrator:
  - Invoke 3x ps-researcher in parallel
  - Each with different topic
  - All run concurrently

Output:
  - docs/research/caching.md
  - docs/research/queuing.md
  - docs/research/storage.md
```

### Pattern 4: Fan-In (Synthesis)

**Use When:** Combining multiple documents into patterns.

```
User: "Synthesize the 3 research documents"

Orchestrator:
  - Invoke ps-synthesizer
  - Provide list of input documents
  - Agent reads all, extracts patterns

Input:
  - docs/research/caching.md
  - docs/research/queuing.md
  - docs/research/storage.md

Output:
  - docs/synthesis/architecture-patterns.md
```

### Pattern 5: Full Decision Workflow

**Use When:** End-to-end from research to validated decision.

```
User: "Help us decide on a caching solution, fully validated"

Orchestrator:
  1. ps-researcher: Explore options
  2. ps-analyst: Analyze trade-offs
  3. ps-architect: Create ADR
  4. ps-validator: Verify constraints
  5. ps-reporter: Generate status

State Chain:
  research → analysis → decision → validation → report
```

---

## Building Custom Workflows

### Prompt Template for Agent Invocation

```python
Task(
    description="ps-{agent-type}: {short-description}",
    subagent_type="general-purpose",
    prompt="""
You are the ps-{agent-type} agent (v2.0.0).

<agent_context>
<role>{role from agent spec}</role>
<task>{specific task}</task>
<constraints>
<must>Create file with Write tool at docs/{type}/</must>
<must>Include L0/L1/L2 output levels</must>
<must>{task-specific requirements}</must>
<must>Call link-artifact after file creation</must>
<must_not>Return transient output only (P-002)</must_not>
<must_not>{task-specific prohibitions}</must_not>
</constraints>
</agent_context>

## PS CONTEXT (REQUIRED)
- **PS ID:** {ps_id}
- **Entry ID:** {entry_id}
- **{Context-specific field}:** {value}

## UPSTREAM ARTIFACTS (if applicable)
- {artifact_type}: {path}

## MANDATORY PERSISTENCE (P-002)
After completing your task, you MUST:

1. Create file at: `docs/{type}/{ps_id}-{entry_id}-{slug}.md`
2. Include L0 (executive), L1 (technical), L2 (strategic) sections
3. Run: `python3 scripts/cli.py link-artifact {ps_id} {entry_id} FILE "{path}" "{description}"`

## YOUR TASK
{Detailed task description}
"""
)
```

### Chaining Example (Pseudocode)

```python
# Step 1: Research
research_result = Task(
    description="ps-researcher: Caching options",
    prompt="... research caching ..."
)

# Step 2: Analysis (references research)
analysis_result = Task(
    description="ps-analyst: Trade-off analysis",
    prompt=f"""
    ...
    ## UPSTREAM ARTIFACTS
    - Research: {research_result.artifact_path}
    ...
    """
)

# Step 3: Decision (references both)
decision_result = Task(
    description="ps-architect: Caching ADR",
    prompt=f"""
    ...
    ## UPSTREAM ARTIFACTS
    - Research: {research_result.artifact_path}
    - Analysis: {analysis_result.artifact_path}
    ...
    """
)
```

---

## Constitutional Constraints

### Hard Constraints (Cannot Be Overridden)

| Principle | Constraint | Implication |
|-----------|------------|-------------|
| P-003 | No Recursive Subagents | Agents CANNOT spawn other agents |
| P-020 | User Authority | User can override orchestrator decisions |
| P-022 | No Deception | Agents must disclose limitations |

### P-003 Enforcement

```
❌ VIOLATION: Agent spawning another agent
   ps-researcher → Task(ps-analyst) ← NOT ALLOWED

✅ CORRECT: Orchestrator spawning agents
   Orchestrator → Task(ps-researcher) ← ALLOWED
   Orchestrator → Task(ps-analyst) ← ALLOWED
```

### Medium Constraints (Logged, Requires Justification)

| Principle | Constraint | Implication |
|-----------|------------|-------------|
| P-002 | File Persistence | All output must be persisted |
| P-010 | Task Tracking | `projects/${JERRY_PROJECT}/WORKTRACKER.md` must be updated |

### Soft Constraints (Warnings)

| Principle | Constraint | Implication |
|-----------|------------|-------------|
| P-001 | Truth and Accuracy | Findings must be evidence-based |
| P-004 | Explicit Provenance | Sources must be cited |
| P-011 | Evidence-Based | Recommendations must have rationale |

---

## Error Handling

### Agent Failure

If an agent fails mid-chain:

1. **Preserve partial output** - Any files created are kept
2. **Log the failure** - Error documented in session
3. **Offer recovery** - User can retry or skip

### State Inconsistency

If state becomes inconsistent:

1. **Check artifact files** - Files are the source of truth
2. **Rebuild state** - Re-read artifact paths from files
3. **Continue from last artifact** - Reference the last successful output

### Timeout

If an agent times out:

1. **Partial output may exist** - Check output directory
2. **Retry with smaller scope** - Break task into pieces
3. **Manual completion** - User can finish the artifact

---

*Orchestration Guide Version: 2.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Last Updated: 2026-01-08*
