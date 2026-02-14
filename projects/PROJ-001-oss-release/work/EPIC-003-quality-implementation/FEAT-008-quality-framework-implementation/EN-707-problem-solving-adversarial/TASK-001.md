# TASK-001: Update skills/problem-solving/SKILL.md with adversarial mode section

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

Update `skills/problem-solving/SKILL.md` to add an adversarial mode section. This section must document the available adversarial strategies, activation triggers, quality threshold requirements (>= 0.92), and reference the SSOT (EN-701) for strategy encodings and constants.

---

## Acceptance Criteria

- [ ] SKILL.md contains a new "Adversarial Mode" section
- [ ] All 10 selected adversarial strategies are documented with brief descriptions
- [ ] Activation triggers for adversarial mode are defined (mandatory vs. optional contexts)
- [ ] Quality threshold (>= 0.92) is referenced from SSOT (EN-701)
- [ ] Strategy catalog reference links to EN-701 SSOT
- [ ] Document follows markdown navigation standards (NAV-001 through NAV-006)
- [ ] Navigation table updated to include new section

---

## Implementation Notes

- Reference EPIC-002 EN-304 for PS skill enhancement design and agent-strategy mappings
- Reference ADR-EPIC002-001 for the 10 selected strategies
- Do NOT duplicate SSOT constants; reference EN-701 as the single source of truth
- Ensure the adversarial mode section is positioned logically within the existing SKILL.md structure

---

## Related Items

- Parent: [EN-707: Problem-Solving Adversarial Mode](EN-707-problem-solving-adversarial.md)
- Depends on: EN-701 (SSOT must exist)
- Blocks: TASK-006 (adversarial review)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated SKILL.md | Markdown | skills/problem-solving/SKILL.md |

### Verification

- [ ] Acceptance criteria verified
- [ ] SKILL.md renders correctly with navigation table
- [ ] SSOT references resolve to valid EN-701 content

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation from EN-707 task decomposition |
