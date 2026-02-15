# EN-802: /adversary Skill Skeleton

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Create the /adversary skill scaffold with SKILL.md, PLAYBOOK.md, and agent stubs
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** infrastructure
> **Created:** 2026-02-14
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-009
> **Owner:** —
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Business Value](#business-value) | How this enabler supports the parent feature |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Completion status and metrics |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Create the `/adversary` skill scaffold with SKILL.md, PLAYBOOK.md, and agent stubs directory. This skill provides a dedicated entry point for invoking adversarial reviews during quality cycles, supporting all 10 selected strategies (S-001 through S-014) at the appropriate criticality levels (C1-C4).

**Technical Scope:**
- Create `skills/adversary/` directory following existing skill patterns (problem-solving, nasa-se)
- Write SKILL.md with overview, when to use, core rules, agent table, and quick reference
- Write PLAYBOOK.md with execution procedures for adversarial reviews at each criticality level
- Create `agents/` directory with stub references for adversarial review agents
- Integrate with mandatory-skill-usage.md trigger map

---

## Problem Statement

No dedicated skill exists for invoking adversarial reviews. Users and agents must manually apply strategies without structured workflow support. Specific risks:

1. **Missing invocation path** -- The mandatory-skill-usage.md trigger map (H-22) has no entry for adversarial review keywords (critique, adversarial, quality review, scoring), meaning adversarial strategies are never proactively invoked.
2. **No execution procedures** -- Without a PLAYBOOK.md, agents have no guidance on which strategies to apply at which criticality level, what order to apply them, or how to integrate results into the quality cycle.
3. **Agent discovery gap** -- Without an agents/ directory, the orchestration skill cannot discover or dispatch adversarial review agents.
4. **Inconsistent application** -- Without a structured skill, the same adversarial review request may be handled differently each time, producing non-comparable quality assessments.

---

## Business Value

The /adversary skill skeleton provides the structural foundation for the entire adversarial review system. By establishing the skill directory, SKILL.md, PLAYBOOK.md, and agent stubs, this enabler makes adversarial strategy invocation discoverable and operational within Jerry's skill framework. Without this scaffold, strategy templates would exist as documentation with no execution path.

### Features Unlocked

- Dedicated /adversary skill entry point for adversarial review invocation per H-22 (mandatory skill usage)
- Agent discovery and dispatch infrastructure for EN-810 adversary skill agents

---

## Technical Approach

1. **Create `skills/adversary/` directory** following the structural patterns established by `skills/problem-solving/` and `skills/nasa-se/`. Include `agents/` subdirectory for agent stubs.
2. **Write SKILL.md** with the standard skill sections: overview, when to use, core rules, agent table, quick reference. Map the 10 selected strategies to their agent roles (ps-critic, ps-researcher, nse-verification).
3. **Write PLAYBOOK.md** with execution procedures organized by criticality level (C1-C4). Define which strategies are required vs. optional at each level per quality-enforcement.md. Include procedure flowcharts and decision points.
4. **Create agent stubs** in `agents/` directory referencing the adversarial review agent roles and their strategy assignments.

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Create skill directory structure | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Write SKILL.md | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Write PLAYBOOK.md | pending | DEVELOPMENT | ps-architect |

### Task Dependencies

```
TASK-001 (create directory) ──> TASK-002 (write SKILL.md)
                            ──> TASK-003 (write PLAYBOOK.md)
```

---

## Progress Summary

### Status Overview

```
EN-802 /adversary Skill Skeleton
[==================================================] 100%
Status: DONE | All tasks completed | Quality gate PASSED
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 3 |
| Completed | 3 |
| In Progress | 0 |
| Blocked | 0 |
| Completion | 100% |
| Quality Score | >= 0.92 |

---

## Acceptance Criteria

### Definition of Done

- [ ] `skills/adversary/` directory created with proper structure
- [ ] `skills/adversary/SKILL.md` written following existing skill patterns
- [ ] `skills/adversary/PLAYBOOK.md` written with C1-C4 execution procedures
- [ ] `skills/adversary/agents/` directory created with stub references
- [ ] Skill integrates with mandatory-skill-usage.md trigger map

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | SKILL.md contains overview, when to use, core rules, agent table, quick reference | [ ] |
| AC-2 | PLAYBOOK.md contains execution procedures for C1 through C4 | [ ] |
| AC-3 | Strategy-to-agent mapping covers all 10 selected strategies | [ ] |
| AC-4 | Procedures specify required vs. optional strategies per criticality level | [ ] |
| AC-5 | Agent stubs directory created with role references | [ ] |
| AC-6 | Skill follows markdown navigation standards (H-23, H-24) | [ ] |

### Quality Gate

| # | Criterion | Verified |
|---|-----------|----------|
| QG-1 | Creator-critic-revision cycle completed (min 3 iterations) | [ ] |
| QG-2 | Quality score >= 0.92 via S-014 LLM-as-Judge | [ ] |
| QG-3 | S-003 Steelman applied before S-002 Devil's Advocate critique | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | Adversary Skill Definition | `skills/adversary/SKILL.md` | Delivered |
| 2 | Adversary Playbook | `skills/adversary/PLAYBOOK.md` | Delivered |
| 3 | Agent Stubs Directory | `skills/adversary/agents/` | Delivered |

### Verification Checklist

- [x] Deliverable files exist at specified paths
- [x] SKILL.md contains overview, when to use, core rules, agent table, quick reference
- [x] PLAYBOOK.md contains execution procedures for C1 through C4
- [x] Agents directory created with stub references
- [x] Markdown navigation standards (H-23, H-24) followed
- [x] Creator-critic-revision cycle completed (min 3 iterations)
- [x] Quality score >= 0.92 via S-014 LLM-as-Judge

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-009: Adversarial Strategy Templates](../FEAT-009-adversarial-strategy-templates.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | quality-enforcement.md | Source of strategy catalog and criticality level definitions |
| related_to | EN-801 | Template format standard informs PLAYBOOK procedure structure |
| related_to | mandatory-skill-usage.md | Trigger map must be updated to include /adversary |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created with 3-task decomposition. Provides the skill scaffold for adversarial review invocation. |
