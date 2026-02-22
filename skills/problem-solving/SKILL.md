---
name: problem-solving
description: Structured problem-solving framework with specialized agents for research, analysis, architecture decisions, validation, synthesis, reviews, investigations, and reporting. Use when tackling complex problems that need systematic exploration, evidence-based decisions, and persistent artifacts.
version: "2.2.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__memory-keeper__store, mcp__memory-keeper__retrieve, mcp__memory-keeper__search
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
  - "critique"
  - "quality score"
  - "iterative refinement"
  - "evaluate quality"
  - "improvement feedback"
---

# Problem-Solving Skill

> **Version:** 2.2.0
> **Framework:** Jerry Problem-Solving (PS)
> **Constitutional Compliance:** Jerry Constitution v1.0

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | New users, stakeholders | [Purpose](#purpose), [When to Use](#when-to-use-this-skill), [Quick Reference](#quick-reference) |
| **L1 (Engineer)** | Developers invoking agents | [Invoking an Agent](#invoking-an-agent), [Agent Details](#agent-details), [Adversarial Quality Mode](#adversarial-quality-mode) |
| **L2 (Architect)** | Workflow designers | [Orchestration Flow](#orchestration-flow), [State Passing](#state-passing-between-agents), [Adversarial Quality Mode](#adversarial-quality-mode) |

---

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
| `ps-critic` | **Quality Evaluator - Iterative refinement with quality scores** | `docs/critiques/` |
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

## Tool Invocation Examples

Each agent uses the allowed tools differently. Here are concrete examples:

### Research Tasks (ps-researcher)

```
1. Find existing research documents:
   Glob(pattern="docs/research/**/*.md")
   → Returns list of prior research to reference

2. Search for industry sources:
   WebSearch(query="event sourcing Python patterns 2026")
   → Find current industry guidance

3. Create research output (MANDATORY per P-002):
   Write(
       file_path="docs/research/work-024-e-001-event-sourcing.md",
       content="# Research: Event Sourcing in Python\n\n## L0: Executive Summary\n..."
   )
   → Persist findings - transient output VIOLATES P-002
```

### Analysis Tasks (ps-analyst)

```
1. Find prior analyses to reference:
   Glob(pattern="docs/analysis/**/*.md")

2. Search for specific patterns in codebase:
   Grep(pattern="try|except|raise", path="src/", output_mode="content", -C=2)
   → Find error handling patterns for root cause analysis

3. Read existing documentation:
   Read(file_path="docs/research/work-024-e-001-event-sourcing.md")
   → Load prior research to inform analysis

4. Create analysis output (MANDATORY per P-002):
   Write(
       file_path="docs/analysis/work-024-e-002-root-cause.md",
       content="# Root Cause Analysis: Build Failures\n\n## L0: Executive Summary\n..."
   )
```

### Architecture Tasks (ps-architect)

```
1. Find existing ADRs for consistency:
   Glob(pattern="docs/decisions/**/*.md")
   → Reference prior decisions

2. Research architectural patterns:
   WebFetch(url="https://martinfowler.com/eaaDev/EventSourcing.html",
            prompt="Extract key benefits and trade-offs of event sourcing")

3. Create ADR output (MANDATORY per P-002):
   Write(
       file_path="docs/decisions/work-024-e-003-adr-persistence.md",
       content="# ADR-042: Use Event Sourcing for Task History\n\n## Status\nPROPOSED\n..."
   )
```

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

## Adversarial Quality Mode

> **SSOT Reference:** `.context/rules/quality-enforcement.md` -- all thresholds, strategy IDs, and criticality levels are defined there. NEVER hardcode values; always reference the SSOT.

The problem-solving skill integrates the adversarial quality framework defined in EPIC-002. This enables structured creator-critic-revision cycles with strategy-specific adversarial review for all PS workflows.

### Strategy Catalog

The quality framework provides 10 selected adversarial strategies across 4 mechanistic families. See `.context/rules/quality-enforcement.md` (Strategy Catalog section) for the authoritative list with IDs S-001 through S-014, composite scores, and family classifications.

| Family | Strategies | PS Application |
|--------|-----------|----------------|
| **Iterative Self-Correction** | S-014 (LLM-as-Judge), S-007 (Constitutional AI Critique), S-010 (Self-Refine) | Quality scoring, constitutional compliance checks, self-review before output |
| **Dialectical Synthesis** | S-003 (Steelman Technique) | Strengthening arguments before critique, ensuring balanced analysis |
| **Role-Based Adversarialism** | S-002 (Devil's Advocate), S-004 (Pre-Mortem Analysis), S-001 (Red Team Analysis) | Challenging assumptions, anticipating failures, adversarial exploration |
| **Structured Decomposition** | S-013 (Inversion Technique), S-012 (FMEA), S-011 (Chain-of-Verification) | Systematic failure mode analysis, verification chains, inverse reasoning |

### Creator-Critic-Revision Cycle

Per H-14 (HARD rule), all C2+ deliverables MUST go through a minimum 3-iteration creator-critic-revision cycle.

**Cycle flow:**
1. **Creator** (any PS agent) produces deliverable
2. **Critic** (ps-critic, ps-reviewer, or MAIN CONTEXT) evaluates using S-014 (LLM-as-Judge) with dimension-level rubrics
3. **Revision** -- creator revises based on critic feedback
4. Repeat until quality threshold is met or circuit breaker triggers

**Quality scoring** uses the 6-dimension weighted composite defined in the SSOT:
- Completeness (0.20), Internal Consistency (0.20), Methodological Rigor (0.20), Evidence Quality (0.15), Actionability (0.15), Traceability (0.10)
- Threshold: >= 0.92 weighted composite for C2+ deliverables (H-13)
- Scoring mechanism: S-014 (LLM-as-Judge) with active leniency bias counteraction

**Circuit breaker:** Minimum 3 iterations REQUIRED (H-14). If no improvement after 2 consecutive iterations, ACCEPT_WITH_CAVEATS or escalate to user.

### Criticality-Based Activation

Strategy activation follows the SSOT criticality levels (C1-C4). See `.context/rules/quality-enforcement.md` (Criticality Levels section) for the authoritative mapping.

| Level | PS Context | Required Strategies | Typical PS Scenario |
|-------|-----------|---------------------|---------------------|
| **C1 (Routine)** | Simple research, status reports | S-010 (Self-Refine) | Single-topic research, progress report |
| **C2 (Standard)** | Analysis, design decisions, reviews | S-007, S-002, S-014 | Root cause analysis, ADR creation, code review |
| **C3 (Significant)** | Architecture decisions, cross-cutting analysis | C2 + S-004, S-012, S-013 | Multi-system impact analysis, architecture ADR |
| **C4 (Critical)** | Governance, irreversible decisions | All 10 selected strategies | Constitution changes, governance decisions |

**Auto-escalation rules** (AE-001 through AE-006 in the SSOT) apply to PS workflows. Key rules:
- AE-001: PS artifacts touching `docs/governance/JERRY_CONSTITUTION.md` = auto-C4
- AE-002: PS artifacts touching `.context/rules/` = auto-C3 minimum
- AE-003: New or modified ADR = auto-C3 minimum

### PS-Specific Strategy Selection

When selecting adversarial strategies for PS workflows, use these context-based recommendations:

| PS Task Type | Primary Strategy | Supporting Strategies | Rationale |
|-------------|------------------|----------------------|-----------|
| **Research** (ps-researcher) | S-011 (CoVe) | S-003 (Steelman), S-010 (Self-Refine) | Verify claims, strengthen findings, self-check |
| **Root Cause Analysis** (ps-analyst) | S-013 (Inversion) | S-004 (Pre-Mortem), S-012 (FMEA) | Challenge causal chain, anticipate failures |
| **Architecture Decisions** (ps-architect) | S-002 (Devil's Advocate) | S-003 (Steelman), S-004 (Pre-Mortem), S-014 (LLM-as-Judge) | Challenge assumptions, strengthen rationale, score quality |
| **Synthesis** (ps-synthesizer) | S-003 (Steelman) | S-013 (Inversion), S-014 (LLM-as-Judge) | Strengthen patterns, invert assumptions, score quality |
| **Code/Design Review** (ps-reviewer) | S-001 (Red Team) | S-007 (Constitutional AI), S-012 (FMEA) | Adversarial exploration, compliance check, failure modes |
| **Quality Critique** (ps-critic) | S-014 (LLM-as-Judge) | S-003 (Steelman), S-007 (Constitutional AI) | Structured scoring, balanced assessment, compliance |

### Mandatory Self-Review (H-15)

Per H-15 (HARD rule), all PS agents MUST perform self-review using S-010 (Self-Refine) before presenting any deliverable. This applies regardless of criticality level.

Per H-16 (HARD rule), agents MUST apply S-003 (Steelman Technique) before critiquing -- strengthen the argument first, then challenge it.

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

## Templates

Problem-solving artifacts should use standardized templates to ensure consistency.

**Location:** `docs/knowledge/exemplars/templates/`

| Template | Use For | Path |
|----------|---------|------|
| `adr.md` | Architecture Decision Records | `docs/knowledge/exemplars/templates/adr.md` |
| `research.md` | Research artifacts | `docs/knowledge/exemplars/templates/research.md` |
| `analysis.md` | Analysis artifacts | `docs/knowledge/exemplars/templates/analysis.md` |
| `deep-analysis.md` | Deep analysis | `docs/knowledge/exemplars/templates/deep-analysis.md` |
| `synthesis.md` | Synthesis documents | `docs/knowledge/exemplars/templates/synthesis.md` |
| `review.md` | Review artifacts | `docs/knowledge/exemplars/templates/review.md` |
| `investigation.md` | Investigation reports | `docs/knowledge/exemplars/templates/investigation.md` |
| `jrn.md` | Journal entries | `docs/knowledge/exemplars/templates/jrn.md` |
| `use-case-template.md` | Use case specifications | `docs/knowledge/exemplars/templates/use-case-template.md` |

**Usage:** When creating a new artifact, read the appropriate template first to ensure consistent structure and sections.

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

*Skill Version: 2.2.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Enhancement: EN-707 Adversarial quality mode integration (EPIC-003)*
*Last Updated: 2026-02-14*
