# TASK-002: Write SKILL.md

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** DONE
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Agents:** ps-architect
> **Created:** 2026-02-14
> **Parent:** EN-802

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Create `skills/adversary/SKILL.md` with overview, when to use, core rules, agent table, and quick reference. Follow the pattern established by `skills/problem-solving/SKILL.md`. The SKILL.md must map all 10 selected adversarial strategies (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014) to their agent roles and specify invocation triggers for proactive use per H-22.

### Acceptance Criteria

- [ ] `skills/adversary/SKILL.md` created
- [ ] Overview section describes the /adversary skill purpose and scope
- [ ] When to Use section specifies invocation triggers (critique, adversarial, quality review, scoring)
- [ ] Core Rules section defines HARD constraints for adversarial review execution
- [ ] Agent table maps strategies to agent roles (ps-critic, ps-researcher, nse-verification)
- [ ] Quick Reference section provides invocation syntax and common usage patterns
- [ ] File follows markdown navigation standards (H-23, H-24)
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items

- Parent: [EN-802: /adversary Skill Skeleton](EN-802-adversary-skill-skeleton.md)
- Depends on: TASK-001 (directory structure)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | 0 hours |
| Time Spent | — |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| `skills/adversary/SKILL.md` | Skill definition | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. Core skill definition -- enables /adversary invocation via H-22 trigger map. |
