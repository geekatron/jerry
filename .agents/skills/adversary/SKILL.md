---
name: adversary
description: >-
  On-demand adversarial quality review of a finished deliverable. Use when the user wants a rigorous,
  formal critique, a quality score, or a tournament review of a document, design, ADR, plan, or code
  artifact — "adversarial review", "red team this", "devil's advocate", "steelman", "pre-mortem",
  "score this with LLM-as-Judge", "run a C3/C4 review", "quality gate". Selects strategies by
  criticality (C1-C4), executes adversarial strategy templates, and scores quality against a
  6-dimension weighted rubric (pass threshold >= 0.92 for C2+). Do NOT use for iterative
  creator-critic-revision loops, routine defect-only code review, binary pass/fail constraint
  validation, root-cause debugging, or when the user explicitly asked for a quick non-rigorous review.
---

# Adversary — Adversarial Quality Review Skill (Codex port)

> Ported from the Jerry Framework `/adversary` Claude skill (`skills/adversary/SKILL.md`).
> Codex has a single execution context and no sub-agent spawning, so the three "agents" are
> **roles** you adopt one at a time by loading the matching file in `references/`. Strategy selection,
> execution, and scoring methodology are identical to the Claude original.

## What this skill does

Runs a standalone adversarial review of an existing deliverable. The flow has three roles, run in
order:

1. **adv-selector** — maps the deliverable's criticality (C1-C4) to the required strategy set and
   produces an ordered execution plan. → `references/adv-selector.md`
2. **adv-executor** — loads and runs each selected strategy template against the deliverable,
   producing finding reports with severity (Critical/Major/Minor). → `references/adv-executor.md`
3. **adv-scorer** — applies the S-014 LLM-as-Judge rubric to produce per-dimension scores, a weighted
   composite, and a PASS/REVISE/ESCALATE verdict. Runs **last**. → `references/adv-scorer.md`

Adopt one role at a time. Do not try to spawn parallel agents.

## How to use it in Codex

1. **Determine criticality** (C1-C4) of the deliverable under review (see table below).
2. **adv-selector:** load `references/adv-selector.md`, produce the ordered strategy plan.
3. **adv-executor:** for each strategy in the plan, load its template from
   `references/strategies/s-NNN-<slug>.md` and run it; persist a finding report per strategy.
4. **adv-scorer:** load `references/adv-scorer.md`, feed it the aggregated findings, produce the
   composite score and verdict.

Persist artifacts to files — default `./reviews/<deliverable-slug>-<role>.md` unless the user gives a
path. A single strategy can be run on its own (e.g. "run Devil's Advocate on this ADR") by loading
adv-executor and just that one template.

## Roles

| Role | When to use it | Reference file |
|------|----------------|----------------|
| `adv-selector` | choose which strategies apply for a given criticality | `references/adv-selector.md` |
| `adv-executor` | run a strategy template (or all of them) against the deliverable | `references/adv-executor.md` |
| `adv-scorer` | produce a rubric quality score / pass-gate verdict | `references/adv-scorer.md` |

## Strategy catalog (10 strategies, 4 families)

Templates are bundled in this skill at `references/strategies/` (skill-relative). The executor loads
them on demand — this skill is self-contained and needs no files outside its own directory.

| ID | Strategy | Template file |
|----|----------|---------------|
| S-001 | Red Team Analysis | `references/strategies/s-001-red-team.md` |
| S-002 | Devil's Advocate | `references/strategies/s-002-devils-advocate.md` |
| S-003 | Steelman Technique | `references/strategies/s-003-steelman.md` |
| S-004 | Pre-Mortem Analysis | `references/strategies/s-004-pre-mortem.md` |
| S-007 | Constitutional AI Critique | `references/strategies/s-007-constitutional-ai.md` |
| S-010 | Self-Refine | `references/strategies/s-010-self-refine.md` |
| S-011 | Chain-of-Verification | `references/strategies/s-011-cove.md` |
| S-012 | FMEA | `references/strategies/s-012-fmea.md` |
| S-013 | Inversion Technique | `references/strategies/s-013-inversion.md` |
| S-014 | LLM-as-Judge | `references/strategies/s-014-llm-as-judge.md` |

> If a template file is missing, warn and ask for the corrected path — never silently skip a strategy.

## Criticality-based strategy selection

| Level | Context | Required strategies | Optional |
|-------|---------|---------------------|----------|
| C1 Routine | minor/reversible | S-010 | S-003, S-014 |
| C2 Standard | feature-level | S-007, S-002, S-014 | S-003, S-010 |
| C3 Significant | architecture/API | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 |
| C4 Critical | irreversible/governance | all 10 (tournament) | none — all required |

**H-16 ordering (hard):** S-003 (Steelman) MUST run before S-002 (Devil's Advocate) — strengthen the
argument before challenging it.

## Quality scoring (S-014 rubric)

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

**Threshold:** weighted composite >= 0.92 to PASS at C2+. Score strictly; when torn between two
adjacent scores, choose the lower (leniency-bias counteraction). Any Critical finding blocks PASS
regardless of composite score.

## Tournament mode (C4)

Run all 10 strategies in this deterministic order, scoring last:

```
A Self-review : S-010
B Strengthen  : S-003
C Challenge   : S-002, S-004, S-001
D Verify      : S-007, S-011
E Decompose   : S-012, S-013
F Score       : S-014   (ALWAYS LAST)
```

Aggregate all executor findings as evidence into the final S-014 score.

## When NOT to use this skill

- **Iterative creator-critic-revision loop** → use an embedded critique approach, not a one-shot review.
- **Routine defect-only code review** → full strategy execution is wasted overhead.
- **Binary pass/fail constraint validation** → this assesses quality dimensions, not compliance bits.
- **Root-cause debugging** → this evaluates deliverables, it doesn't diagnose causes.
- **User asked for a quick, non-rigorous review** → respect that; don't impose tournament overhead.

## Self-containment

This skill needs nothing outside its own `.agents/skills/adversary/` directory: the role prompts are
in `references/`, and all 10 strategy templates are bundled in `references/strategies/`. The thresholds,
strategy IDs, criticality levels, and rubric dimensions are embedded directly in this SKILL.md and the
role files, so no external SSOT file is required at runtime. You can copy this directory anywhere Codex
discovers skills and it will work standalone.

## Provenance

Derived from the Jerry Framework `/adversary` skill (`skills/adversary/SKILL.md`), its agent definitions
(`skills/adversary/agents/*.md`), the strategy templates originally in
`.context/templates/adversarial/` (now bundled here), and the quality SSOT
`.context/rules/quality-enforcement.md` (values embedded above). Listed for traceability only — none of
these are runtime dependencies of this Codex skill.
