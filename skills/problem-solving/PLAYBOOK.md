# Problem-Solving Playbook

> **User Guide for the Problem-Solving Skill**
> Version: 2.0.0

This playbook teaches you how to use the Problem-Solving skill effectively. It covers invocation methods, orchestration patterns, and practical examples.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Understanding the Agents](#understanding-the-agents)
3. [How to Invoke](#how-to-invoke)
4. [Orchestration Patterns](#orchestration-patterns)
5. [Practical Examples](#practical-examples)
6. [Tips and Best Practices](#tips-and-best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### The 30-Second Version

1. **Describe your problem** - Just say what you need
2. **The right agent activates** - Based on keywords in your request
3. **Output is persisted** - A markdown file is created in `docs/`
4. **You can chain agents** - Sequence multiple agents for complex problems

### Example

```
You: "Research the best approach for implementing event sourcing in Python"

Claude: [Activates ps-researcher agent]
        [Researches topic with citations]
        [Creates docs/research/work-XXX-event-sourcing.md]
        [Returns L0/L1/L2 summary]
```

---

## Understanding the Agents

### The Agent Portfolio

| Agent | When to Use | What You Get |
|-------|-------------|--------------|
| **ps-researcher** | Exploring options, gathering information | Research report with sources |
| **ps-analyst** | Understanding why something happened | Root cause analysis, trade-off matrix |
| **ps-architect** | Making design decisions | ADR (Architecture Decision Record) |
| **ps-validator** | Checking if requirements are met | Validation report with evidence |
| **ps-synthesizer** | Finding patterns across documents | Pattern catalog, knowledge items |
| **ps-reviewer** | Assessing quality of work | Review findings with severity |
| **ps-investigator** | Debugging failures | Investigation report with corrective actions |
| **ps-reporter** | Getting status updates | Progress report with metrics |

### The L0/L1/L2 Output Format

Every agent produces output at three levels:

| Level | Audience | Content |
|-------|----------|---------|
| **L0 (ELI5)** | Non-technical stakeholders | Plain language summary |
| **L1 (Engineer)** | Software engineers | Technical details, code examples |
| **L2 (Architect)** | Principal architects | Strategic implications, trade-offs |

This means you get the right level of detail for your audience.

---

## How to Invoke

### Method 1: Natural Language (Recommended)

Just describe what you need. The orchestrator selects the right agent.

```
"Research React vs Vue for our frontend"
→ Activates ps-researcher

"Why are our tests so slow?"
→ Activates ps-analyst (root cause)

"Create an ADR for choosing PostgreSQL"
→ Activates ps-architect

"Check if we meet all the security requirements"
→ Activates ps-validator

"Find patterns across the 3 research documents"
→ Activates ps-synthesizer

"Review the new authentication module"
→ Activates ps-reviewer

"Figure out why the deploy failed yesterday"
→ Activates ps-investigator

"What's the status of Phase 3?"
→ Activates ps-reporter
```

### Method 2: Explicit Agent Request

Name the agent you want:

```
"Use ps-researcher to explore caching options"
"Have ps-analyst do a 5 Whys analysis"
"I need ps-architect for the database decision"
```

### Method 3: Chained Requests

Request a sequence:

```
"First research event sourcing options, then create an ADR for our choice"
```

This will:
1. Run ps-researcher → create research document
2. Run ps-architect → create ADR referencing the research

---

## Orchestration Patterns

### Pattern 1: Single Agent

For focused tasks, one agent is enough.

```
User: "Research graph databases for our use case"

Flow:
  ┌─────────────────┐
  │  ps-researcher  │ → docs/research/graph-databases.md
  └─────────────────┘
```

### Pattern 2: Sequential Chain

For complex problems, agents work in sequence.

```
User: "Investigate the API timeout, propose a fix, and validate the solution"

Flow:
  ┌──────────────────┐    ┌───────────────┐    ┌───────────────┐
  │ ps-investigator  │ →  │  ps-architect │ →  │  ps-validator │
  └──────────────────┘    └───────────────┘    └───────────────┘
         ↓                       ↓                     ↓
  docs/investigations/    docs/decisions/      docs/analysis/
  api-timeout.md          adr-fix.md           validation.md
```

### Pattern 3: Fan-Out (Parallel Research)

For broad exploration, multiple researchers in parallel.

```
User: "Research caching, message queues, and databases for our architecture"

Flow:
  ┌─────────────────┐
  │  ps-researcher  │ → docs/research/caching-options.md
  ├─────────────────┤
  │  ps-researcher  │ → docs/research/message-queue-options.md
  ├─────────────────┤
  │  ps-researcher  │ → docs/research/database-options.md
  └─────────────────┘
```

### Pattern 4: Fan-In (Synthesis)

After parallel work, synthesize findings.

```
User: "Synthesize the 3 research documents into patterns"

Flow:
  docs/research/caching.md ──────┐
  docs/research/queues.md  ──────┼→ ┌─────────────────┐
  docs/research/databases.md ────┘   │ ps-synthesizer  │
                                    └─────────────────┘
                                            ↓
                                    docs/synthesis/
                                    patterns.md
```

### Pattern 5: Research → Decision → Validation

The full decision workflow.

```
User: "We need to choose a caching solution"

Flow:
  ┌─────────────────┐    ┌───────────────┐    ┌───────────────┐
  │  ps-researcher  │ →  │  ps-architect │ →  │  ps-validator │
  │  (explore)      │    │  (decide)     │    │  (verify)     │
  └─────────────────┘    └───────────────┘    └───────────────┘
         ↓                       ↓                     ↓
  Research: Redis,       ADR: Choose Redis     Validation:
  Memcached, etc.        with rationale        Constraints met
```

---

## Practical Examples

### Example 1: Technology Selection

**Goal:** Choose between SQLite and PostgreSQL for the project.

```
Step 1: "Research SQLite vs PostgreSQL for embedded vs server use cases"

[ps-researcher activates]
Output: docs/research/work-024-e-001-sqlite-vs-postgres.md

Step 2: "Based on the research, create an ADR recommending the best choice"

[ps-architect activates]
Output: docs/decisions/work-024-e-002-adr-database-selection.md
```

### Example 2: Root Cause Analysis

**Goal:** Understand why tests are flaky.

```
"Analyze why our CI tests are flaky - do a 5 Whys"

[ps-analyst activates]
Output: docs/analysis/work-024-e-003-root-cause.md

Content includes:
- 5 Whys table with evidence
- Root cause: race conditions in test fixtures
- Recommendations with action items
```

### Example 3: Incident Investigation

**Goal:** Investigate production outage.

```
"Investigate the API outage on January 5th at 2:30 PM"

[ps-investigator activates]
Output: docs/investigations/work-024-e-004-investigation.md

Content includes:
- Timeline of events
- 5 Whys analysis
- Ishikawa diagram (6M categories)
- Corrective actions with owners
- FMEA for similar risks
```

### Example 4: Code Review

**Goal:** Review new authentication module.

```
"Review the authentication module for security issues"

[ps-reviewer activates]
Output: docs/reviews/work-024-e-005-security.md

Content includes:
- OWASP Top 10 assessment
- Findings by severity (Critical → Info)
- Code snippets with recommendations
- Overall assessment: PASS/NEEDS_WORK/FAIL
```

### Example 5: Cross-Document Synthesis

**Goal:** Find patterns across research documents.

```
"Synthesize the 4 research documents from last week into patterns"

[ps-synthesizer activates]
Output: docs/synthesis/work-024-e-006-synthesis.md

Content includes:
- Cross-reference matrix
- Pattern catalog (PAT-XXX)
- Lessons learned (LES-XXX)
- Assumptions identified (ASM-XXX)
```

---

## Tips and Best Practices

### 1. Be Specific

```
❌ "Analyze this"
✅ "Analyze why the database queries are slow using 5 Whys"

❌ "Research stuff"
✅ "Research event sourcing patterns in Python, focusing on libraries with Postgres support"
```

### 2. Provide Context

```
❌ "Create an ADR"
✅ "Create an ADR for choosing Redis as our caching layer.
    We need sub-millisecond latency and support for 100k concurrent connections."
```

### 3. Chain When Needed

For complex problems, break into steps:

```
"First, research the options. Then analyze trade-offs.
 Finally, create an ADR with our recommendation."
```

### 4. Reference Previous Work

```
"Based on the research in docs/research/caching-options.md,
 create an ADR for our caching decision."
```

### 5. Ask for Specific Output

```
"Generate a phase status report focusing on blockers and risks"
"Do a security review focusing on OWASP Top 10 issues"
```

---

## Troubleshooting

### "The wrong agent was selected"

Be more explicit:

```
"Use ps-analyst (not ps-researcher) to analyze the trade-offs"
```

### "Output wasn't saved"

This shouldn't happen (P-002 requires persistence), but if it does:

```
"Save the analysis to docs/analysis/my-analysis.md"
```

### "I need more detail at L1 level"

Ask for expansion:

```
"Expand the L1 technical section with more code examples"
```

### "The output is too long"

Ask for summary:

```
"Summarize just the L0 executive summary"
```

### "I want to continue from a previous analysis"

Reference the file:

```
"Continue the investigation from docs/investigations/api-timeout.md
 with the new log data I found"
```

---

## Output Locations Reference

| Agent | Output Directory | File Pattern |
|-------|-----------------|--------------|
| ps-researcher | `docs/research/` | `{id}-{topic}.md` |
| ps-analyst | `docs/analysis/` | `{id}-{analysis-type}.md` |
| ps-architect | `docs/decisions/` | `{id}-adr-{slug}.md` |
| ps-validator | `docs/analysis/` | `{id}-validation.md` |
| ps-synthesizer | `docs/synthesis/` | `{id}-synthesis.md` |
| ps-reviewer | `docs/reviews/` | `{id}-{review-type}.md` |
| ps-investigator | `docs/investigations/` | `{id}-investigation.md` |
| ps-reporter | `docs/reports/` | `{id}-{report-type}.md` |

---

*Playbook Version: 2.0.0*
*Last Updated: 2026-01-08*
