---
name: adversary
description: On-demand adversarial quality reviews using strategy templates. Selects strategies by criticality level, executes adversarial templates against deliverables, and scores quality using LLM-as-Judge rubric. Integrates with quality-enforcement.md SSOT.
version: "1.0.0"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
activation-keywords:
  - "adversarial review"
  - "adversary"
  - "adversarial quality review"
  - "strategy review"
  - "adversarial critique"
  - "rigorous critique"
  - "formal critique"
  - "run adversarial"
  - "quality scoring"
  - "LLM-as-Judge"
  - "strategy selection"
  - "tournament review"
  - "red team"
  - "devil's advocate"
  - "steelman"
  - "pre-mortem"
  - "C2 review"
  - "C3 review"
  - "C4 review"
  - "tournament mode"
  - "quality gate"
---

# Adversary Skill

> **Version:** 1.0.0
> **Framework:** Jerry Adversarial Quality (ADV)
> **Constitutional Compliance:** Jerry Constitution v1.0
> **SSOT Reference:** `.context/rules/quality-enforcement.md`

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | New users, stakeholders | [Purpose](#purpose), [When to Use](#when-to-use-this-skill), [When to Use /adversary vs ps-critic](#when-to-use-adversary-vs-ps-critic), [Quick Reference](#quick-reference) |
| **L1 (Engineer)** | Developers invoking agents | [Invoking an Agent](#invoking-an-agent), [Available Agents](#available-agents), [Dependencies](#dependencies--prerequisites), [Adversarial Quality Mode](#adversarial-quality-mode) |
| **L2 (Architect)** | Workflow designers | [P-003 Compliance](#p-003-compliance), [H-14 Integration](#integration-with-creator-critic-revision-cycle-h-14), [Constitutional Compliance](#constitutional-compliance), [Strategy Templates](#strategy-templates) |

---

## Purpose

The Adversary skill provides **on-demand adversarial quality reviews** using strategy templates from the Jerry quality framework. Unlike the problem-solving skill's integrated adversarial mode (which operates within creator-critic loops), the adversary skill is invoked explicitly when you need a standalone adversarial assessment of any deliverable.

### Key Capabilities

- **Strategy Selection** - Maps criticality levels (C1-C4) to the correct adversarial strategy sets per SSOT
- **Strategy Execution** - Loads and runs strategy templates against deliverables with structured finding classification
- **Quality Scoring** - Implements S-014 LLM-as-Judge rubric scoring with 6-dimension weighted composite
- **Criticality-Aware** - Automatically adjusts review depth based on deliverable criticality
- **Template-Driven** - All strategies follow standardized templates from `.context/templates/adversarial/`

---

## When to Use This Skill

Activate when:

- Applying adversarial strategies to a completed deliverable outside a creator-critic loop
- Scoring deliverable quality using the SSOT 6-dimension rubric
- Selecting the appropriate strategy set for a given criticality level
- Running a full C4 tournament review with all 10 strategies
- Pairing S-003 (Steelman) before S-002 (Devil's Advocate) per H-16
- Needing a standalone quality assessment without revision cycles

**Do NOT use when:**

- You need a creator-critic-revision loop (use `/problem-solving` with ps-critic instead)
- You need routine code review for quick defect checks (use ps-reviewer)
- You need constraint validation (use ps-validator)
- Working on routine code changes at C1 criticality — use self-review (S-010) only without full adversarial overhead
- Fixing defects or bugs with obvious solutions — use `/problem-solving` for root-cause analysis instead
- User explicitly requests a quick review without adversarial rigor — respect user preference per P-020

> **Note:** Use `/adversary` for adversarial code review (e.g., red team security review, tournament quality assessment of code artifacts). Use `ps-reviewer` for routine defect detection.

### Relationship to ps-critic

The adv-scorer and ps-critic agents share the same S-014 LLM-as-Judge rubric and 6-dimension weighted composite scoring methodology. They serve different workflow positions:

| Aspect | adv-scorer | ps-critic |
|--------|-----------|-----------|
| **Workflow** | Standalone/on-demand scoring | Embedded in creator-critic-revision loops |
| **Output** | Focused score report with L0 summary | L0/L1/L2 multi-level critique report |
| **Iteration** | May be invoked once or re-invoked for re-scoring | Iterates within the H-14 cycle |
| **Invocation** | Via `/adversary` skill | Via `/problem-solving` skill |

Both agents produce comparable scores from the same rubric; the choice depends on whether you need standalone assessment (adv-scorer) or iterative critique with revision guidance (ps-critic).

---

## Available Agents

| Agent | Role | Model | Output Location |
|-------|------|-------|-----------------|
| `adv-selector` | Strategy Selector - Maps criticality to strategy sets | haiku | Strategy selection plan |
| `adv-executor` | Strategy Executor - Runs strategy templates against deliverables | sonnet | Strategy execution reports |
| `adv-scorer` | Quality Scorer - LLM-as-Judge rubric scoring | sonnet | Quality score reports |

---

## P-003 Compliance

All adversary agents are **workers**, NOT orchestrators. The MAIN CONTEXT (Claude session) orchestrates the workflow.

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
  | adv- | | adv- | | adv- |   <-- Workers (max 1 level)
  |select| |exec  | |scorer|
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
"Run an adversarial review of this ADR at C3 criticality"
"Score this deliverable with LLM-as-Judge"
"What strategies should I apply for a C2 review?"
"Run Devil's Advocate and Steelman on this design document"
"Execute a full C4 tournament review on the architecture proposal"
```

The orchestrator will select the appropriate agent(s) based on keywords and context.

### Option 2: Explicit Agent Request

Request a specific agent:

```
"Use adv-selector to pick strategies for C3 criticality"
"Have adv-executor run S-002 Devil's Advocate on the ADR"
"I need adv-scorer to produce a quality score for this synthesis"
```

### Option 3: Task Tool Invocation

For programmatic invocation within workflows:

```python
Task(
    description="adv-selector: Strategy selection for C3",
    subagent_type="general-purpose",
    prompt="""
You are the adv-selector agent (v1.0.0).

## ADV CONTEXT (REQUIRED)
- **Criticality Level:** C3
- **Deliverable Type:** Architecture Decision Record
- **Deliverable Path:** docs/decisions/adr-042-persistence.md

## MANDATORY PERSISTENCE (P-002)
Create file at: {output_path}

## TASK
Select the strategy set for C3 criticality per SSOT.
"""
)
```

---

## Dependencies / Prerequisites

The adversary skill depends on external artifacts created by other enablers. These MUST be in place before the skill is fully operational.

### Strategy Template Files

All 10 strategy templates in `.context/templates/adversarial/` are created by separate enablers:

| Template | Source Enabler | Status |
|----------|---------------|--------|
| `s-001-red-team.md` | EN-809 | Created by EN-809 |
| `s-002-devils-advocate.md` | EN-806 | Created by EN-806 |
| `s-003-steelman.md` | EN-807 | Created by EN-807 |
| `s-004-pre-mortem.md` | EN-808 | Created by EN-808 |
| `s-007-constitutional-ai.md` | EN-805 | Created by EN-805 |
| `s-010-self-refine.md` | EN-804 | Created by EN-804 |
| `s-011-cove.md` | EN-809 | Created by EN-809 |
| `s-012-fmea.md` | EN-808 | Created by EN-808 |
| `s-013-inversion.md` | EN-808 | Created by EN-808 |
| `s-014-llm-as-judge.md` | EN-803 | Created by EN-803 |

**Naming Convention:** Templates follow the pattern `s-{NNN}-{slug}.md` where `{NNN}` is the strategy ID from the quality-enforcement SSOT and `{slug}` is a hyphenated descriptor (e.g., `s-002-devils-advocate.md`). These are static reference documents versioned alongside the codebase — they are not dynamically generated.

**Fallback behavior:** If a template file is not found, adv-executor MUST:
1. Emit a WARNING to the orchestrator with the missing template path
2. Request the corrected path from the orchestrator
3. Do NOT silently skip the strategy — the orchestrator decides whether to skip or provide an alternative

The skill skeleton (EN-802) defines the structure; the template enablers populate the content.

### SSOT File

- `.context/rules/quality-enforcement.md` -- MUST exist. All thresholds, strategy IDs, criticality levels, and quality dimensions are sourced from here.

---

## Adversarial Quality Mode

> **SSOT Reference:** `.context/rules/quality-enforcement.md` -- all thresholds, strategy IDs, criticality levels, and quality dimensions are defined there. NEVER hardcode values; always reference the SSOT.

### Strategy Catalog

The quality framework provides 10 selected adversarial strategies across 4 mechanistic families. See `.context/rules/quality-enforcement.md` (Strategy Catalog section) for the authoritative list.

| Family | Strategies | Adversary Application |
|--------|-----------|----------------------|
| **Iterative Self-Correction** | S-014 (LLM-as-Judge), S-007 (Constitutional AI Critique), S-010 (Self-Refine) | Quality scoring, constitutional compliance, self-review |
| **Dialectical Synthesis** | S-003 (Steelman Technique) | Strengthen arguments before critique (H-16 REQUIRED) |
| **Role-Based Adversarialism** | S-002 (Devil's Advocate), S-004 (Pre-Mortem Analysis), S-001 (Red Team Analysis) | Challenge assumptions, anticipate failures, adversarial exploration |
| **Structured Decomposition** | S-013 (Inversion Technique), S-012 (FMEA), S-011 (Chain-of-Verification) | Systematic failure mode analysis, verification chains |

### Strategy Templates

All strategies use standardized templates from `.context/templates/adversarial/`:

| Template | Strategy | Purpose |
|----------|----------|---------|
| `s-001-red-team.md` | S-001 Red Team Analysis | Adversarial exploration of attack surfaces |
| `s-002-devils-advocate.md` | S-002 Devil's Advocate | Challenge assumptions and key claims |
| `s-003-steelman.md` | S-003 Steelman Technique | Strengthen the best version of the argument |
| `s-004-pre-mortem.md` | S-004 Pre-Mortem Analysis | Anticipate failure modes |
| `s-007-constitutional-ai.md` | S-007 Constitutional AI Critique | Constitutional compliance verification |
| `s-010-self-refine.md` | S-010 Self-Refine | Iterative self-improvement |
| `s-011-cove.md` | S-011 Chain-of-Verification | Systematic claim verification |
| `s-012-fmea.md` | S-012 FMEA | Failure Mode and Effects Analysis |
| `s-013-inversion.md` | S-013 Inversion Technique | Invert key claims to find blind spots |
| `s-014-llm-as-judge.md` | S-014 LLM-as-Judge | Rubric-based quality scoring |

### Criticality-Based Strategy Selection

Per SSOT, strategy activation follows criticality levels:

| Level | Required Strategies | Optional Strategies |
|-------|---------------------|---------------------|
| **C1 (Routine)** | S-010 | S-003, S-014 |
| **C2 (Standard)** | S-007, S-002, S-014 | S-003, S-010 |
| **C3 (Significant)** | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 |
| **C4 (Critical)** | All 10 selected strategies | None (all required) |

### H-16 Ordering Constraint

**HARD rule:** S-003 (Steelman) MUST be applied before S-002 (Devil's Advocate). Always strengthen the argument before challenging it.

### Quality Scoring (S-014)

The SSOT defines 6 quality dimensions with weights:

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

**Threshold:** >= 0.92 weighted composite for C2+ deliverables (H-13)

**Leniency bias counteraction:** Score strictly against rubric criteria. When uncertain between adjacent scores, choose the lower one.

---

## When to Use /adversary vs ps-critic

Both `/adversary` and `ps-critic` apply adversarial strategies, but serve different workflow positions:

| Aspect | /adversary Skill | ps-critic Agent |
|--------|-----------------|----------------|
| **Use Case** | Standalone adversarial reviews, tournament scoring, strategy template execution | Embedded quality critique within creator-critic-revision loops |
| **Invocation** | Explicit on-demand (`/adversary` or natural language request) | Invoked by orchestrator within H-14 cycle |
| **Output Focus** | Strategy-specific findings (adv-executor) + quality score (adv-scorer) | L0/L1/L2 multi-level critique with dimension-level improvement guidance |
| **Iteration** | May be used once or re-invoked for re-scoring after revision | Iterates within the H-14 minimum 3-iteration cycle |
| **Strategy Coverage** | Full strategy set per criticality (C1-C4), including tournament mode (all 10) | Applies strategies appropriate to criticality, embedded in workflow |
| **Agents** | adv-selector, adv-executor, adv-scorer | ps-critic (single agent) |
| **Output Artifacts** | Strategy execution reports + quality score report | Critique report with improvement recommendations |

**When to Use Each:**

- **Use `/adversary` when:**
  - You need a formal adversarial review outside a creator-critic loop
  - You need tournament mode scoring with all 10 strategies (C4)
  - You need strategy-specific finding reports (adv-executor outputs)
  - You need standalone quality scoring with S-014 rubric
  - You need to apply a specific strategy template (e.g., "run S-002 Devil's Advocate on this ADR")

- **Use `ps-critic` when:**
  - You are within an orchestrated creator-critic-revision workflow
  - You need iterative improvement guidance across multiple revision cycles
  - You need lightweight iteration-level critique without full tournament overhead
  - You are working within `/problem-solving` or `/orchestration` skills

**Complementary Use:**

Both can work together:
- `ps-critic` applies strategies within workflows for embedded quality cycles
- `/adversary` orchestrates cross-strategy tournament reviews for C4 critical deliverables
- `ps-critic` uses the same S-014 rubric and dimension scoring as adv-scorer for consistency

---

## Tournament Mode

Tournament mode executes all 10 adversarial strategies against a C4 (Critical) deliverable in a deterministic sequence. This is the most comprehensive review level, required for irreversible decisions.

### Execution Order

All 10 strategies run in the recommended order from `skills/adversary/agents/adv-selector.md`:

- **Group A — Self-Review**: S-010 (Self-Refine)
- **Group B — Strengthen**: S-003 (Steelman Technique)
- **Group C — Challenge**: S-002 (Devil's Advocate), S-004 (Pre-Mortem Analysis), S-001 (Red Team Analysis)
- **Group D — Verify**: S-007 (Constitutional AI Critique), S-011 (Chain-of-Verification)
- **Group E — Decompose**: S-012 (FMEA), S-013 (Inversion Technique)
- **Group F — Score**: S-014 (LLM-as-Judge) — **ALWAYS LAST**

### Aggregation

Findings from all strategy execution reports are collected across all 9 executor runs. The adv-scorer agent (S-014) receives these aggregated findings as input evidence when producing the final composite score. Critical findings from any strategy block PASS regardless of score.

### Timing Expectations

A C4 tournament with all 10 strategies requires approximately 11 agent invocations:

1. **adv-selector** (1 invocation) — Strategy selection
2. **adv-executor** (9 invocations) — One per strategy from Groups A-E
3. **adv-scorer** (1 invocation) — Final scoring with S-014

Typical duration depends on deliverable size and complexity. Expect longer processing times for large architecture documents or governance changes.

---

## Integration with Creator-Critic-Revision Cycle (H-14)

H-14 mandates a minimum 3-iteration creator-critic-revision cycle for C2+ deliverables. The adversary skill is **not** a revision loop manager -- it provides standalone adversarial assessment. The integration boundary is:

1. **adv-scorer produces the quality score.** When invoked, adv-scorer evaluates the deliverable and returns a PASS/REVISE/ESCALATE verdict.
2. **If REVISE, the orchestrator feeds findings back to the creator agent.** The adversary skill's findings (from adv-executor) and score breakdown (from adv-scorer) provide actionable input for the next revision iteration.
3. **The adversary skill can be re-invoked for re-scoring.** After the creator revises, the orchestrator may invoke adv-scorer again (with the `Prior Score` context field) to track improvement across iterations.
4. **Minimum 3 iterations are the orchestrator's responsibility.** The adversary skill does not enforce iteration count -- it scores when asked. The orchestrator (or `/orchestration` skill) tracks the iteration count per H-14.

**Workflow position:** The adversary skill sits at the "critic" position within the H-14 cycle when used for quality scoring. It can replace or complement ps-critic depending on whether the orchestrator needs standalone scoring (adv-scorer) or iterative critique (ps-critic).

---

## Constitutional Compliance

All agents adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement |
|-----------|-------------|
| P-001: Truth and Accuracy | Findings based on evidence, scores based on rubrics |
| P-002: File Persistence | All outputs persisted to files |
| P-003: No Recursive Subagents | Agents are workers, not orchestrators |
| P-004: Explicit Provenance | Strategy IDs, template paths, and evidence cited |
| P-011: Evidence-Based | All findings tied to specific deliverable evidence |
| P-020: User Authority | User can override strategy selection and scoring |
| P-022: No Deception | Quality issues honestly reported, scores not inflated |

---

## Quick Reference

### Common Workflows

| Need | Agent | Command Example |
|------|-------|-----------------|
| Pick strategies for criticality | adv-selector | "What strategies for C3 review?" |
| Run a specific strategy | adv-executor | "Run S-002 Devil's Advocate on this ADR" |
| Score deliverable quality | adv-scorer | "Score this deliverable with LLM-as-Judge" |
| Steelman + Devil's Advocate pair | adv-executor | "Run Steelman then Devil's Advocate on this design" |
| Full C4 tournament | All three | "Run full C4 tournament review" |

### Agent Selection Hints

| Keywords | Likely Agent |
|----------|--------------|
| select, pick, which strategies, criticality, C1/C2/C3/C4 | adv-selector |
| run, execute, apply, template, strategy, findings | adv-executor |
| score, judge, rubric, dimensions, threshold, 0.92 | adv-scorer |

---

## References

| Source | Content |
|--------|---------|
| `.context/rules/quality-enforcement.md` | SSOT for thresholds, strategies, criticality levels |
| `.context/templates/adversarial/` | Strategy execution templates |
| `skills/problem-solving/SKILL.md` | Integrated adversarial quality mode (ps-critic) |
| `docs/governance/JERRY_CONSTITUTION.md` | Constitutional principles |
| ADR-EPIC002-001 | Strategy selection and composite scores |
| ADR-EPIC002-002 | 5-layer enforcement architecture |

---

*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Created: 2026-02-15*
