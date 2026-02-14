# TASK-002: Update skills/problem-solving/PLAYBOOK.md with creator-critic-revision cycles

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Activity:** DEVELOPMENT
> **Created:** 2026-02-14
> **Parent:** EN-707
> **Assignee:** ps-architect

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Change log |

---

## Summary

Update `skills/problem-solving/PLAYBOOK.md` to integrate creator-critic-revision cycles into each workflow phase (research, analysis, synthesis). Define when adversarial review is mandatory vs. optional based on criticality level (C1-C4), and document entry/exit criteria for each cycle.

---

## Acceptance Criteria

- [ ] PLAYBOOK.md integrates creator-critic-revision cycles into research phase
- [ ] PLAYBOOK.md integrates creator-critic-revision cycles into analysis phase
- [ ] PLAYBOOK.md integrates creator-critic-revision cycles into synthesis phase
- [ ] Mandatory vs. optional adversarial review defined per criticality level (C1-C4)
- [ ] Entry criteria for adversarial cycle documented (when to start critic review)
- [ ] Exit criteria for adversarial cycle documented (when revision is accepted)
- [ ] Document follows markdown navigation standards (NAV-001 through NAV-006)

---

## Implementation Notes

- Reference EPIC-002 EN-304 for the PS workflow phase integration design
- C1/C2 criticality should require full adversarial cycles; C3/C4 may allow abbreviated review
- Each cycle: creator produces output -> critic challenges -> creator revises -> score evaluated
- Align with S-014 LLM-as-Judge scoring methodology

---

## Related Items

- Parent: [EN-707: Problem-Solving Adversarial Mode](EN-707-problem-solving-adversarial.md)
- Depends on: EN-701 (SSOT for criticality levels)
- Blocks: TASK-006 (adversarial review)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated PLAYBOOK.md | Markdown | skills/problem-solving/PLAYBOOK.md |

### Verification

- [ ] Acceptance criteria verified
- [ ] PLAYBOOK.md renders correctly with navigation table
- [ ] Creator-critic-revision cycle is clearly documented with entry/exit criteria

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation from EN-707 task decomposition |
