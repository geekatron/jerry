# TASK-003: Write PLAYBOOK.md

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

Create `skills/adversary/PLAYBOOK.md` with execution procedures for adversarial reviews at each criticality level (C1-C4). The playbook must specify which strategies are required vs. optional at each level, the execution order, decision points for iteration vs. acceptance, and integration with the creator-critic-revision cycle. Reference quality-enforcement.md for per-criticality strategy sets.

### Acceptance Criteria

- [ ] `skills/adversary/PLAYBOOK.md` created
- [ ] C1 (Routine) procedure defined: required strategies (S-010), optional strategies (S-003, S-014)
- [ ] C2 (Standard) procedure defined: required strategies (S-007, S-002, S-014), optional strategies (S-003, S-010)
- [ ] C3 (Significant) procedure defined: required strategies (C2 + S-004, S-012, S-013), optional (S-001, S-003, S-010, S-011)
- [ ] C4 (Critical) procedure defined: all 10 selected strategies required
- [ ] Execution order specified for each criticality level
- [ ] Decision points documented (iterate vs. accept, escalate vs. resolve)
- [ ] Integration with creator-critic-revision cycle documented
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
| `skills/adversary/PLAYBOOK.md` | Playbook | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. Execution procedures for adversarial reviews -- critical for consistent quality cycle application. |
