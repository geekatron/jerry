---
name: problem-solving
description: Structured problem-solving framework with specialized agents for research, analysis, architecture decisions, validation, synthesis, reviews, investigations, and reporting. Use when tackling complex problems that need systematic exploration, evidence-based decisions, and persistent artifacts.
version: "2.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch
activation-keywords:
  - "research"
  - "analyze"
  - "investigate"
  - "review"
  - "synthesize"
  - "validate"
  - "architecture decision"
  - "ADR"
  - "root cause"
  - "trade-off analysis"
  - "5 whys"
  - "problem solving"
---

# Problem-Solving Skill

> **Version:** 2.0.0
> **Framework:** Jerry Problem-Solving (PS)
> **Constitutional Compliance:** Jerry Constitution v1.0

## Purpose

The Problem-Solving skill provides a structured framework for tackling complex problems through specialized agents. Each agent produces **persistent artifacts** that survive context compaction and build a knowledge base over time.

### Key Capabilities

- **Structured Research** - Gather and document findings with source citations
- **Deep Analysis** - Root cause analysis, trade-offs, gap analysis, risk assessment
- **Architecture Decisions** - ADRs using Nygard format with L0/L1/L2 explanations
- **Validation** - Constraint verification with traceability matrices
- **Synthesis** - Cross-document pattern extraction and knowledge generation
- **Reviews** - Code, design, architecture, and security quality assessment
- **Investigations** - Failure analysis using 5 Whys, Ishikawa, FMEA
- **Reporting** - Status reports with health metrics and progress tracking

---

## When to Use This Skill

Activate when:

- Starting research on a new technology or approach
- Analyzing a problem to find root causes
- Making architectural decisions that need documentation
- Validating that constraints are satisfied
- Synthesizing findings across multiple documents
- Reviewing code, designs, or architecture
- Investigating failures or incidents
- Generating status or progress reports

---

## Available Agents

| Agent | Role | Output Location |
|-------|------|-----------------|
| `ps-researcher` | Research Specialist - Gathers information with citations | `docs/research/` |
| `ps-analyst` | Analysis Specialist - Deep analysis (5 Whys, FMEA, trade-offs) | `docs/analysis/` |
| `ps-architect` | Architecture Specialist - Creates ADRs with Nygard format | `docs/decisions/` |
| `ps-validator` | Validation Specialist - Verifies constraints with evidence | `docs/analysis/` |
| `ps-synthesizer` | Synthesis Specialist - Pattern extraction across documents | `docs/synthesis/` |
| `ps-reviewer` | Review Specialist - Code/design/security quality reviews | `docs/reviews/` |
| `ps-investigator` | Investigation Specialist - Root cause of failures | `docs/investigations/` |
| `ps-reporter` | Reporting Specialist - Status and progress reports | `docs/reports/` |

All agents produce output at three levels:
- **L0 (ELI5):** Executive summary for non-technical stakeholders
- **L1 (Software Engineer):** Technical implementation details
- **L2 (Principal Architect):** Strategic implications and trade-offs

---

## Invoking an Agent

### Option 1: Natural Language Request

Simply describe what you need:

```
"Research best practices for event sourcing in Python"
"Analyze the trade-offs between SQLite and PostgreSQL for this use case"
"Create an ADR for choosing Redis as our caching layer"
"Validate that all domain constraints are met"
"Investigate why the API timeout occurred"
```

The orchestrator will select the appropriate agent based on keywords and context.

### Option 2: Explicit Agent Request

Request a specific agent:

```
"Use ps-researcher to explore graph database options"
"Have ps-analyst do a 5 Whys on the login failures"
"I need ps-architect to create an ADR for the new persistence layer"
```

### Option 3: Task Tool Invocation

For programmatic invocation within workflows:

```python
Task(
    description="ps-researcher: Graph databases",
    subagent_type="general-purpose",
    prompt="""
You are the ps-researcher agent (v2.0.0).

## PS CONTEXT (REQUIRED)
- **PS ID:** work-024
- **Entry ID:** e-101
- **Topic:** Graph Database Options

## MANDATORY PERSISTENCE (P-002)
Create file at: docs/research/work-024-e-101-graph-databases.md

## RESEARCH TASK
Research graph database options for the Jerry framework.
Focus on: Gremlin compatibility, Python support, embedded options.
"""
)
```

---

## Orchestration Flow

### Sequential Chain Example

For complex problems requiring multiple perspectives:

```
User Request: "I need to understand why our tests are slow and fix it"

1. ps-researcher → Gather data on test execution patterns
   Output: docs/research/work-024-e-001-test-performance.md

2. ps-analyst → Apply 5 Whys to identify root cause
   Output: docs/analysis/work-024-e-002-root-cause.md

3. ps-architect → Create ADR for proposed solution
   Output: docs/decisions/work-024-e-003-adr-test-optimization.md

4. ps-validator → Verify solution meets constraints
   Output: docs/analysis/work-024-e-004-validation.md
```

### State Passing Between Agents

Agents can reference each other's output using state keys:

| Agent | Output Key | Provides |
|-------|------------|----------|
| ps-researcher | `researcher_output` | Research findings, sources |
| ps-analyst | `analyst_output` | Root cause, recommendations |
| ps-architect | `architect_output` | Decision, alternatives |
| ps-validator | `validator_output` | Validation status, gaps |
| ps-synthesizer | `synthesizer_output` | Patterns, themes |
| ps-reviewer | `reviewer_output` | Findings, assessment |
| ps-investigator | `investigator_output` | Root cause, corrective actions |
| ps-reporter | `reporter_output` | Metrics, health status |

---

## Mandatory Persistence (P-002)

All agents MUST persist their output to files. This ensures:

1. **Context Rot Resistance** - Findings survive session compaction
2. **Knowledge Accumulation** - Artifacts build project knowledge base
3. **Auditability** - Decisions can be traced and reviewed
4. **Collaboration** - Outputs can be shared and referenced

### Output Structure

```
docs/
├── research/           # ps-researcher outputs
│   └── {ps-id}-{entry-id}-{topic}.md
├── analysis/           # ps-analyst and ps-validator outputs
│   └── {ps-id}-{entry-id}-{analysis-type}.md
├── decisions/          # ps-architect ADRs
│   └── {ps-id}-{entry-id}-adr-{slug}.md
├── synthesis/          # ps-synthesizer outputs
│   └── {ps-id}-{entry-id}-synthesis.md
├── reviews/            # ps-reviewer outputs
│   └── {ps-id}-{entry-id}-{review-type}.md
├── investigations/     # ps-investigator outputs
│   └── {ps-id}-{entry-id}-investigation.md
└── reports/            # ps-reporter outputs
    └── {ps-id}-{entry-id}-{report-type}.md
```

---

## Constitutional Compliance

All agents adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement |
|-----------|-------------|
| P-001: Truth and Accuracy | Findings based on evidence, sources cited |
| P-002: File Persistence | All outputs persisted to files |
| P-003: No Recursive Subagents | Agents cannot spawn nested agents |
| P-004: Explicit Provenance | Reasoning and sources documented |
| P-011: Evidence-Based | Recommendations tied to evidence |
| P-022: No Deception | Limitations and gaps disclosed |

---

## Quick Reference

### Common Workflows

| Need | Agent | Command Example |
|------|-------|-----------------|
| Research a topic | ps-researcher | "Research OAuth2 implementation patterns" |
| Find root cause | ps-analyst | "Analyze why builds are failing" |
| Document a decision | ps-architect | "Create ADR for choosing PostgreSQL" |
| Verify constraints | ps-validator | "Validate domain layer constraints" |
| Find patterns | ps-synthesizer | "Synthesize findings from the 3 research docs" |
| Review code quality | ps-reviewer | "Review the new authentication module" |
| Investigate incident | ps-investigator | "Investigate the production outage" |
| Status report | ps-reporter | "Generate phase status report" |

### Agent Selection Hints

| Keywords | Likely Agent |
|----------|--------------|
| research, explore, find, gather, investigate options | ps-researcher |
| analyze, root cause, trade-off, gap, risk, 5 whys, FMEA | ps-analyst |
| ADR, architecture decision, design, choose, decide | ps-architect |
| validate, verify, constraint, test, evidence | ps-validator |
| synthesize, patterns, themes, combine, meta-analysis | ps-synthesizer |
| review, quality, code review, security, OWASP | ps-reviewer |
| investigate, failure, incident, debug, what happened | ps-investigator |
| report, status, progress, metrics, summary | ps-reporter |

---

## Agent Details

For detailed agent specifications, see:

- `skills/problem-solving/agents/ps-researcher.md`
- `skills/problem-solving/agents/ps-analyst.md`
- `skills/problem-solving/agents/ps-architect.md`
- `skills/problem-solving/agents/ps-validator.md`
- `skills/problem-solving/agents/ps-synthesizer.md`
- `skills/problem-solving/agents/ps-reviewer.md`
- `skills/problem-solving/agents/ps-investigator.md`
- `skills/problem-solving/agents/ps-reporter.md`

---

*Skill Version: 2.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Last Updated: 2026-01-08*
