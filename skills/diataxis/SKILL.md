---
name: diataxis
description: >
  Four-quadrant documentation framework. Produces tutorials (learning by doing),
  how-to guides (goal-oriented tasks), reference documentation (authoritative description),
  and explanation (conceptual understanding) using the Diataxis methodology. Invoke when
  creating new documentation, auditing existing docs for quadrant mixing, or classifying
  documentation requests. Triggers: documentation, tutorial, how-to, howto, reference docs,
  explanation, diataxis, write docs, write documentation, write tutorial, create documentation,
  classify documentation, audit documentation, user guide, getting started, quickstart, API docs,
  developer guide, quadrant, doc type, how-to guide.
version: "0.1.0"
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
activation-keywords:
  - "documentation"
  - "tutorial"
  - "how-to"
  - "howto"
  - "how-to guide"
  - "reference docs"
  - "explanation"
  - "diataxis"
  - "write docs"
  - "write documentation"
  - "write tutorial"
  - "create documentation"
  - "classify documentation"
  - "audit documentation"
  - "user guide"
  - "getting started"
  - "quickstart"
  - "API docs"
  - "developer guide"
  - "quadrant"
  - "doc type"
---

# Diataxis Skill

> **Version:** 0.1.0
> **Framework:** Diataxis Four-Quadrant Documentation (diataxis.fr)
> **Constitutional Compliance:** Jerry Constitution v1.0
> **Knowledge Reference:** `docs/knowledge/diataxis-framework.md`

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose](#purpose) | What the skill does and key capabilities |
| [When to Use This Skill](#when-to-use-this-skill) | Activation conditions and exclusions |
| [Available Agents](#available-agents) | Agent roster with roles, tiers, and output locations |
| [P-003 Compliance](#p-003-compliance) | Single-level nesting hierarchy and architectural rationale |
| [Invoking an Agent](#invoking-an-agent) | Three invocation patterns with examples |
| [Templates](#templates) | Per-quadrant template references |
| [Integration Points](#integration-points) | Cross-skill connections |
| [Constitutional Compliance](#constitutional-compliance) | Principle mapping |
| [Quick Reference](#quick-reference) | Common workflows table |
| [References](#references) | All referenced file paths |

This SKILL.md serves multiple audiences:

## Document Audience (Triple-Lens)

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | New users, stakeholders | [Purpose](#purpose), [When to Use](#when-to-use-this-skill), [Quick Reference](#quick-reference) |
| **L1 (Engineer)** | Developers invoking agents | [Invoking an Agent](#invoking-an-agent), [Available Agents](#available-agents), [Templates](#templates) |
| **L2 (Architect)** | Workflow designers | [P-003 Compliance](#p-003-compliance), [Integration Points](#integration-points), [Constitutional Compliance](#constitutional-compliance) |

---

## Purpose

The Diataxis skill provides **four-quadrant documentation methodology** using the Diataxis framework (diataxis.fr). Instead of writing documentation as a single undifferentiated blob, this skill separates content into four types based on two axes: practical/theoretical and acquisition/application.

### Key Capabilities

- **Quadrant-Specific Writing** -- Four specialized writer agents, each encoding the quality criteria, anti-patterns, and voice for their quadrant
- **Documentation Classification** -- T1 classifier analyzes requests against the two Diataxis axes and returns structured quadrant assignment
- **Documentation Auditing** -- T2 auditor detects quadrant mixing, coverage gaps, and quality issues in existing documentation
- **Template-Driven Output** -- Per-quadrant templates enforce structural consistency
- **Self-Review Integration** -- Writer agents apply Diataxis-specific quality checks during H-15 self-review

### The Four Quadrants

|  | **Acquisition** (learning) | **Application** (working) |
|--|:--:|:--:|
| **Practical** (doing) | Tutorials | How-to Guides |
| **Theoretical** (understanding) | Explanation | Reference |

---

## When to Use This Skill

Activate when:

- Writing new documentation for any project or skill
- Converting existing documentation to follow Diataxis quadrant structure
- Classifying whether a documentation request should be a tutorial, guide, reference, or explanation
- Auditing existing docs for quadrant mixing (the #1 documentation anti-pattern)
- Producing per-quadrant templates for consistent documentation structure

**Do NOT use when:**

- Writing code, tests, or non-documentation artifacts (use `/eng-team`)
- Performing adversarial quality review of non-documentation deliverables (use `/adversary`)
- Writing requirements specifications (use `/nasa-se`)
- The user explicitly requests free-form writing without Diataxis structure -- respect user preference per P-020

### Misclassification Recovery

If a writer agent produces the wrong document type:
1. If you know the correct type: invoke the correct writer agent directly
2. If unsure: invoke `diataxis-classifier` with a `hint_quadrant` parameter to confirm. The classifier returns a confidence level (1.00/0.85/0.70); for confidence below 0.85, use the `hint_quadrant` parameter to guide classification before proceeding.

---

## Available Agents

| Agent | Role | Cognitive Mode | Model | Tier | Output Location |
|-------|------|---------------|-------|------|----------------|
| `diataxis-tutorial` | Tutorial Writer (learning-oriented) | systematic | sonnet | T2 | `projects/${JERRY_PROJECT}/docs/tutorials/` |
| `diataxis-howto` | How-to Guide Writer (goal-oriented) | systematic | sonnet | T2 | `projects/${JERRY_PROJECT}/docs/howto/` |
| `diataxis-reference` | Reference Writer (information-oriented) | systematic | sonnet | T2 | `projects/${JERRY_PROJECT}/docs/reference/` |
| `diataxis-explanation` | Explanation Writer (understanding-oriented) | divergent | opus | T2 | `projects/${JERRY_PROJECT}/docs/explanations/` |
| `diataxis-classifier` | Documentation Classifier | convergent | haiku | T1 | Inline result (no file output) |
| `diataxis-auditor` | Documentation Auditor | systematic | sonnet | T1 | Inline result; orchestrator persists to `projects/${JERRY_PROJECT}/audits/` |

---

## P-003 Compliance

All six agents are **workers** (invoked via Task by the caller). None include `Task` in their tools. The caller (user or orchestrator) is responsible for:

1. Invoking `diataxis-classifier` to determine the correct quadrant (optional when quadrant is unambiguous from the request)
2. Invoking the appropriate writer agent based on classification
3. Invoking `diataxis-auditor` for quality review

This design maintains P-003 single-level nesting: orchestrator -> worker only.

### Architectural Rationale

Four specialized writer agents (rather than one adaptive writer) is justified by cognitive mode differentiation: tutorial writing requires **systematic** step-by-step completeness, how-to writing requires **systematic** goal-oriented focus, reference writing requires **systematic** exhaustive coverage, and explanation writing requires **divergent** conceptual exploration. These are distinct reasoning patterns that produce measurably different output when encoded in agent identity rather than deferred to prompt-level switching. The classifier separates routing from writing; the auditor separates evaluation from production.

---

## Invoking an Agent

### Option 1: Natural Language Request

```
Write a tutorial for setting up Jerry's problem-solving skill.
```

The trigger map routes "write tutorial" to `/diataxis`, and the main context invokes `diataxis-tutorial`.

### Option 2: Explicit Agent Request

```
Use /diataxis with diataxis-classifier to classify this documentation request:
"How do I configure MCP servers in Jerry?"

Then use the appropriate writer agent based on the classification.
```

### Option 3: Task Tool Invocation (Programmatic)

Agent definitions in `skills/diataxis/agents/` follow the standard Jerry dual-file architecture (H-34). The orchestrator invokes them via the Task tool using the `jerry:diataxis-{agent}` subagent_type convention, which maps to the agent definition file at `skills/diataxis/agents/diataxis-{agent}.md`:

```
Task tool invocation:
  subagent_type: "jerry:diataxis-tutorial"
  prompt: "Write a tutorial for setting up your first Jerry project.
           Topic: Setting up your first Jerry project
           Prerequisites: Jerry installed, Claude Code configured
           Output: projects/PROJ-013-diataxis/samples/tutorial-first-project.md"
```

The same pattern applies to all six agents: `jerry:diataxis-classifier`, `jerry:diataxis-tutorial`, `jerry:diataxis-howto`, `jerry:diataxis-reference`, `jerry:diataxis-explanation`, `jerry:diataxis-auditor`. (Note: verify `jerry:` namespace support against your Claude Code version before programmatic deployment.)

---

## Templates

Per-quadrant templates are located at `skills/diataxis/templates/`:

| Template | Quadrant | Key Structural Elements |
|----------|----------|------------------------|
| `skills/diataxis/templates/tutorial-template.md` | Tutorial | Numbered steps; prerequisite block; "What you will achieve" intro; observable output per step |
| `skills/diataxis/templates/howto-template.md` | How-to Guide | Goal statement title; numbered task steps; "If you need X, do Y" variants |
| `skills/diataxis/templates/reference-template.md` | Reference | Table/definition-list structure; no narrative; standard entry format |
| `skills/diataxis/templates/explanation-template.md` | Explanation | Continuous prose sections; no numbered steps; "Why" framing |

---

## Integration Points

- **`/problem-solving`**: Research outputs may need documentation -- classifier determines which quadrant
- **`/nasa-se`**: Requirements and design artifacts feed reference documentation
- **`/adversary`**: Diataxis agents integrate with creator-critic-revision cycle (H-14) for C2+ deliverables
- **`/eng-team`**: Security documentation benefits from quadrant separation
- **Jerry's own docs**: The skill can improve Jerry's own documentation (reflexive use)

### Documentation Quality Gate

For C2+ documentation deliverables:
1. Writer agent produces document
2. `diataxis-auditor` reviews for quadrant mixing and quality criteria
3. S-014 scoring applied to final output via `/adversary` (adv-scorer agent) with 6-dimension weighted composite

---

## Constitutional Compliance

All agents comply with:
- **P-003** -- No recursive subagents. Workers cannot spawn sub-workers.
- **P-020** -- User authority. User can override quadrant classification. If a user explicitly requests a different quadrant or rejects a classification, the agent complies without requiring justification.
- **P-022** -- No deception. Agents are transparent about classification confidence and limitations.

---

## Quick Reference

| Need | Agent | Example | Output Location |
|------|-------|---------| ------|
| Write a tutorial | `diataxis-tutorial` | "Write a tutorial for setting up X" | `projects/${JERRY_PROJECT}/docs/tutorials/` |
| Write a how-to guide | `diataxis-howto` | "Write a how-to guide for deploying Y" | `projects/${JERRY_PROJECT}/docs/howto/` |
| Write reference docs | `diataxis-reference` | "Document the API for Z" | `projects/${JERRY_PROJECT}/docs/reference/` |
| Write an explanation | `diataxis-explanation` | "Explain why we chose architecture A" | `projects/${JERRY_PROJECT}/docs/explanations/` |
| Classify a doc request | `diataxis-classifier` | "What type of doc should 'Getting Started' be?" | Inline result (no file output) |
| Audit existing docs | `diataxis-auditor` | "Audit these files for quadrant mixing" | `projects/${JERRY_PROJECT}/audits/` |

---

## References

| Source | Content |
|--------|---------|
| `docs/knowledge/diataxis-framework.md` | Diataxis framework knowledge base |
| `skills/diataxis/rules/diataxis-standards.md` | Per-quadrant quality criteria, anti-patterns, detection heuristics, voice guidelines |
| `skills/diataxis/agents/diataxis-tutorial.md` | Tutorial writer agent definition |
| `skills/diataxis/agents/diataxis-howto.md` | How-to guide writer agent definition |
| `skills/diataxis/agents/diataxis-reference.md` | Reference writer agent definition |
| `skills/diataxis/agents/diataxis-explanation.md` | Explanation writer agent definition |
| `skills/diataxis/agents/diataxis-classifier.md` | Documentation classifier agent definition |
| `skills/diataxis/agents/diataxis-auditor.md` | Documentation auditor agent definition |
| `skills/diataxis/templates/tutorial-template.md` | Tutorial structural template |
| `skills/diataxis/templates/howto-template.md` | How-to guide structural template |
| `skills/diataxis/templates/reference-template.md` | Reference structural template |
| `skills/diataxis/templates/explanation-template.md` | Explanation structural template |

---

*Skill Version: 0.1.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: `.context/rules/skill-standards.md`*
*Created: 2026-02-26*
