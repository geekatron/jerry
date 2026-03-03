---
name: prompt-engineering
description: Structured prompt construction and quality validation for Jerry Framework. Invoke when building structured prompts, generating NPT-009/NPT-013 constraints, or scoring prompt quality. Guides users through the 5-element prompt anatomy, generates formatted constraints with XML wrapping, and scores prompts against the 7-criterion rubric.
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep
activation-keywords:
  - "/prompt-engineering"
  - "build prompt"
  - "create prompt"
  - "prompt template"
  - "NPT pattern"
  - "constraint generation"
  - "prompt quality"
  - "score prompt"

---

# Prompt Engineering Skill

> **Version:** 1.0.0
> **Framework:** Jerry Framework v0.9.0
> **Constitutional Compliance:** Jerry Constitution v1.0
> **SSOT Reference:** `.context/rules/prompt-quality.md`, `.context/rules/prompt-templates.md`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | What this skill does and why |
| [When to Use This Skill](#when-to-use-this-skill) | Triggers and use cases |
| [Available Agents](#available-agents) | Agent registry with routing guide |
| [Invoking an Agent](#invoking-an-agent) | Three invocation options (natural language, explicit, Task tool) |
| [Quick Reference](#quick-reference) | Copy-paste examples for common tasks |
| [Routing Disambiguation](#routing-disambiguation) | When this skill is the wrong choice |
| [Constitutional Compliance](#constitutional-compliance) | Principle mapping with consequences |
| [Architecture Notes](#architecture-notes) | Design rationale and references |

---

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | Users new to prompt engineering | [Overview](#overview), [When to Use](#when-to-use-this-skill), [Quick Reference](#quick-reference) |
| **L1 (Engineer)** | Developers building prompts and constraints | [Available Agents](#available-agents), [Quick Reference](#quick-reference), [Architecture Notes](#architecture-notes) |
| **L2 (Architect)** | Framework maintainers and skill designers | [Routing Disambiguation](#routing-disambiguation), [Constitutional Compliance](#constitutional-compliance), [Architecture Notes](#architecture-notes) |

---

## Overview

The Prompt Engineering skill operationalizes PROJ-014 negative prompting research findings into a reusable tool for constructing high-quality structured prompts within the Jerry Framework. PROJ-014 validated that NPT-013 structured negation (NEVER + consequence + alternative) achieves 100% compliance vs 92.2% for positive-only framing (p=0.016, CONDITIONAL GO via PG-003).

### Core Capabilities

- **Interactive Prompt Builder:** Walks users through the 5-element prompt anatomy (routing, scope, data source, quality gate, output path) producing XML-wrapped structured prompts.
- **NPT Constraint Generator:** Converts intent descriptions into NPT-009/NPT-013 formatted constraints with `<forbidden_actions>` and `<constraint>` XML wrapping.
- **Prompt Quality Scorer:** Evaluates prompts against the 7-criterion rubric (C1 Task Specificity through C7 Positive Framing) and returns dimension scores with improvement suggestions.

### NPT Format Reference

| Format | Structure | Use Case |
|--------|-----------|----------|
| NPT-009 | `{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}` | Agent forbidden actions, constitutional guardrails |
| NPT-013 | `NEVER {action} -- Consequence: {impact}. Instead: {alternative}` | Behavioral constraints, routing rules, methodology guardrails |

---

## When to Use This Skill

Invoke `/prompt-engineering` when you need to:

- Build a structured Jerry prompt from scratch using the 5-element anatomy.
- Generate NPT-009 or NPT-013 formatted constraints for agent definitions, rule files, or skill documentation.
- Score an existing prompt against the 7-criterion rubric to identify quality gaps.
- Convert positive-only instructions to structured negation format per PROJ-014 findings.
- Produce XML-wrapped constraint blocks (`<forbidden_actions>`, `<constraint>`) for agent governance YAML.

NEVER invoke this skill when:
- Task requires adversarial quality review of a deliverable -- Consequence: prompt engineering generates constraints and scores prompts, not deliverables; quality assessment of artifacts requires `/adversary` with S-014 rubric scoring
- Task requires research, analysis, or root cause investigation -- Consequence: prompt engineering is a construction tool, not an analytical methodology; no research capability, no causal investigation; use `/problem-solving` instead
- Task is executing an existing prompt template from `.context/rules/prompt-templates.md` -- Consequence: template execution does not require prompt construction; the 5 templates are self-contained and ready to use with placeholder substitution
- Task is modifying agent definition YAML frontmatter or governance files -- Consequence: agent definition structure follows `agent-development-standards.md` schema, not prompt anatomy; use direct file editing with schema validation per H-34

See [Routing Disambiguation](#routing-disambiguation) for full exclusion conditions with consequences.

---

## Available Agents

| Agent | File | Model | Cognitive Mode | Purpose |
|-------|------|-------|----------------|---------|
| `pe-builder` | `skills/prompt-engineering/agents/pe-builder.md` | opus | integrative | Interactive prompt assembly -- walks user through 5 elements, generates XML-wrapped structured prompt |
| `pe-constraint-gen` | `skills/prompt-engineering/agents/pe-constraint-gen.md` | sonnet | systematic | NPT pattern selector and constraint formatter -- takes intent, outputs NPT-009/NPT-013 XML blocks |
| `pe-scorer` | `skills/prompt-engineering/agents/pe-scorer.md` | haiku | convergent | Prompt quality scorer -- evaluates against 7-criterion rubric, returns dimension scores + improvement suggestions |

### Agent Routing Guide

| Keywords in Request | Likely Agent | Rationale |
|---------------------|--------------|-----------|
| build, create, construct, assemble, walk me through, 5 elements | pe-builder | Interactive prompt construction with element-by-element guidance |
| constraint, NPT, forbidden, NEVER, consequence, XML, guardrail | pe-constraint-gen | Systematic constraint formatting using NPT pattern catalog |
| score, evaluate, rate, quality, rubric, dimensions, improve | pe-scorer | Convergent evaluation against 7-criterion rubric |

### P-003 Compliance

All prompt engineering agents are **workers**, NOT orchestrators. The MAIN CONTEXT (Claude session) orchestrates the workflow.

```
P-003 AGENT HIERARCHY:
======================

  +-------------------+
  | MAIN CONTEXT      |  <-- Orchestrator (Claude session)
  | (orchestrator)    |
  +-------------------+
     |        |        |
     v        v        v
  +------+ +------+ +------+
  | pe-  | | pe-  | | pe-  |   <-- Workers (max 1 level)
  |build | |const | |score |
  +------+ +------+ +------+

  Agents CANNOT invoke other agents.
  Agents CANNOT spawn subagents.
  Only MAIN CONTEXT orchestrates the sequence.
```

---

## Invoking an Agent

### Option 1: Natural Language Request

Simply describe what you need:

```
"Build a prompt for researching authentication patterns for a .NET microservice"
"Generate NPT-013 constraints for a research agent that must not hallucinate sources"
"Score this prompt against the quality rubric"
"Convert these positive instructions to NPT-009 format for agent governance"
```

The orchestrator selects the appropriate agent based on keywords and context.

### Option 2: Explicit Agent Request

Request a specific agent:

```
"Use pe-builder to walk me through constructing a C3 orchestration prompt"
"Have pe-constraint-gen produce NPT-009 forbidden actions for a T3 research agent"
"I need pe-scorer to evaluate this prompt and tell me what to fix"
```

### Option 3: Task Tool Invocation

For programmatic invocation within workflows:

```python
Task(
    description="pe-constraint-gen: Generate NPT-013 constraints",
    subagent_type="general-purpose",
    prompt="""
You are the pe-constraint-gen agent (v1.0.0).

## INPUT
- **Intent:** Prevent hallucinated source citations in a research agent
- **Target Context:** Agent governance YAML forbidden_actions
- **NPT Format:** NPT-009 (governance YAML context)

## REFERENCE
Load pattern reference: skills/prompt-engineering/rules/npt-pattern-reference.md

## TASK
Generate NPT-009 formatted constraints for the specified intent.
Persist output to: {output_path}
"""
)
```

---

## Quick Reference

### Build a Structured Prompt

```
"Build a prompt for researching authentication patterns for a .NET microservice project"
```

pe-builder walks through: (1) skill routing, (2) domain scope, (3) data source, (4) quality gate, (5) output path. Produces a complete XML-wrapped prompt.

### Generate NPT-013 Constraints

```
"Generate NPT-013 constraints for a new research agent that must not hallucinate sources"
```

pe-constraint-gen produces XML blocks:

```xml
<forbidden_actions>
  <constraint format="NPT-013">
    NEVER fabricate or hallucinate source citations -- Consequence: downstream agents
    build analysis on nonexistent evidence, compounding errors through the pipeline.
    Instead: explicitly state when no source is available and mark confidence as low.
  </constraint>
</forbidden_actions>
```

### Score an Existing Prompt

```
"Score this prompt against the quality rubric:
'Research authentication patterns and write them up somewhere'"
```

pe-scorer returns dimension-level scores (C1-C7) with weighted composite and specific improvement suggestions per failing criterion.

### Common Workflows

| Need | Agent | Example |
|------|-------|---------|
| Build prompt from scratch | pe-builder | "Help me build a prompt for a C3 architecture decision" |
| Generate agent guardrails | pe-constraint-gen | "Generate NPT-009 forbidden actions for a T3 research agent" |
| Convert positive to negation | pe-constraint-gen | "Convert these DOs to NPT-013 format: 'Always cite sources'" |
| Evaluate prompt quality | pe-scorer | "Score this prompt and tell me what to fix" |
| Full build-and-score cycle | pe-builder + pe-scorer | "Build a prompt for X, then score it" |
| Build, score, iterate | pe-builder + pe-scorer (loop) | "Build a prompt for X, score it, and iterate until it reaches 90+" |

**End-to-End Build-Score-Iterate Workflow:**

```
1. pe-builder constructs prompt (5-element anatomy)
2. pe-scorer evaluates prompt (7-criterion rubric)
3. If score < target: pe-builder revises based on scorer findings
4. Repeat steps 2-3 until score >= target or 3 iterations reached
```

Default target: >= 90 for standard prompts; adjust per `prompt-quality.md` threshold table. The orchestrator (main context) coordinates this loop. Agents do not call each other (P-003).

---

## Integration Points

| Skill/Resource | Relationship | Integration Pattern |
|----------------|-------------|---------------------|
| `/adversary` | Distinct scope | `/adversary` scores **deliverables** against S-014 quality gate; `/prompt-engineering` scores **prompts** against the 7-criterion rubric. Different rubrics, different targets. |
| `/problem-solving` | Consumer | ps-researcher, ps-analyst, and other agents consume prompts constructed by pe-builder. The prompt quality directly affects downstream research quality. |
| `.context/rules/prompt-templates.md` | Complement | Templates provide ready-to-use prompts with placeholder substitution. pe-builder constructs **new** prompts when no template fits. Use templates first; invoke pe-builder when templates are insufficient. |
| `.context/rules/prompt-quality.md` | Source rubric | pe-scorer implements the 7-criterion rubric defined in prompt-quality.md. The rubric is the SSOT; pe-scorer operationalizes it. |

---

## Routing Disambiguation

> When this skill is the wrong choice and what happens if misrouted.

| Condition | Use Instead | Consequence of Misrouting |
|-----------|-------------|--------------------------|
| Adversarial quality review of a deliverable | `/adversary` | Prompt engineering scores prompts against the 7-criterion rubric, not deliverables against the S-014 quality gate; wrong rubric applied, wrong scoring dimensions used |
| Research, analysis, or investigation tasks | `/problem-solving` | Prompt engineering constructs prompts, not research artifacts; no analytical methodology, no data source access, no root cause investigation |
| Requirements, design, or architecture work | `/nasa-se` | Prompt engineering produces prompts and constraints, not requirements specifications or architecture documents; wrong deliverable type |
| Executing an existing prompt template | Direct template use | Template execution requires placeholder substitution only; invoking prompt engineering adds unnecessary construction overhead to a ready-to-use artifact |
| Agent definition schema validation | `/ast` or direct H-34 validation | Agent governance YAML follows JSON Schema validation per H-34, not prompt quality rubric; wrong validation mechanism applied |
| Transcript parsing or meeting notes | `/transcript` | Prompt engineering has no audio/VTT/SRT processing capability; fundamentally different domain |

---

## Constitutional Compliance

All agents adhere to the **Jerry Constitution v1.0**:

> **P-002 scope note:** P-002 applies to pe-builder and pe-constraint-gen (`output.required: true`). pe-scorer supports optional file persistence (`output.required: false`); inline scoring output is permitted per its evaluation-only role.

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-002 | NEVER produce transient-only output -- persist all artifacts to files | Work products lost on session end; no audit trail; downstream agents cannot reference output |
| P-003 | NEVER spawn recursive subagents -- max 1 level | Agent hierarchy violation; uncontrolled token consumption |
| P-004 | NEVER omit source attribution for generated constraints | Constraint provenance untraceable; reviewers cannot verify NPT pattern compliance |
| P-020 | NEVER override user intent -- ask before destructive ops | Unauthorized action; trust erosion |
| P-022 | NEVER deceive about actions, capabilities, or confidence | Governance undermined; quality assessment invalidated |

---

## Architecture Notes

### Design Rationale

This skill operationalizes three knowledge sources into reusable tooling:

1. **PROJ-014 Research Findings:** NPT-013 structured negation achieves statistically significant compliance improvement over positive-only framing. The pe-constraint-gen agent encodes this finding into a systematic constraint generation workflow.
2. **Prompt Quality Rubric:** The 7-criterion rubric from `.context/rules/prompt-quality.md` is encoded as the pe-scorer evaluation framework. Scoring uses the same weighted formula: `total = sum((raw_score_N / 3) * weight_N * 100)`.
3. **5-Element Prompt Anatomy:** The pe-builder agent implements the structured prompt construction pattern from `.context/rules/prompt-quality.md` (routing, scope, data source, quality gate, output path).

### References

| Source | Content |
|--------|---------|
| `.context/rules/prompt-quality.md` | 7-criterion rubric, 5-element anatomy, anti-patterns |
| `.context/rules/prompt-templates.md` | 5 copy-paste templates (research spike, implementation, orchestration, architecture, batch) |
| `skills/prompt-engineering/rules/npt-pattern-reference.md` | NPT pattern catalog (NPT-009, NPT-013 formats) |
| `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-6/final-synthesis.md` | PROJ-014 research synthesis (NPT-013 validation data: 100% vs 92.2%, p=0.016) |
| `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/ab-testing/ab-testing-synthesis.md` | A/B testing results (CONDITIONAL GO via PG-003) |
| `.context/rules/agent-development-standards.md` | Agent definition schema, guardrails template, forbidden action format |
| `.context/rules/quality-enforcement.md` | Quality gate SSOT, criticality levels, enforcement architecture |
| `projects/PROJ-006-jerry-prompt/` | PROJ-006 research: 5-element anatomy derivation, quality rubric development, template validation |

---

*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: `.context/rules/prompt-quality.md`, `.context/rules/prompt-templates.md`*
*Source: PROJ-014 Negative Prompting Research*
*Created: 2026-03-01*
