# TASK-001: Update skills/orchestration/SKILL.md with adversarial mode section

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
> **Parent:** EN-709
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

Update `skills/orchestration/SKILL.md` to add an adversarial mode section. This section must document phase gate enforcement, sync barrier quality checks, cross-pollination enhancement, and reference the SSOT (EN-701) for quality threshold constants and strategy encodings.

---

## Acceptance Criteria

- [ ] SKILL.md contains a new "Adversarial Mode" section
- [ ] Phase gate enforcement with quality thresholds documented
- [ ] Sync barrier quality check integration described
- [ ] Cross-pollination enhancement with adversarial strategy selection documented
- [ ] Quality threshold (>= 0.92) referenced from SSOT (EN-701)
- [ ] Document follows markdown navigation standards (NAV-001 through NAV-006)
- [ ] Navigation table updated to include new section

---

## Implementation Notes

- Reference EPIC-002 EN-307 for orchestration skill enhancement design
- Reference ADR-EPIC002-001 for phase gate definitions
- Phase gates are the key integration point: each phase output must pass adversarial review
- Sync barriers coordinate timing AND quality; document both dimensions
- Do NOT duplicate SSOT constants; reference EN-701 as the single source of truth

---

## Related Items

- Parent: [EN-709: Orchestration Adversarial Mode](EN-709-orchestration-adversarial.md)
- Depends on: EN-701 (SSOT must exist)
- Blocks: TASK-006 (adversarial review)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated SKILL.md | Markdown | skills/orchestration/SKILL.md |

### Verification

- [ ] Acceptance criteria verified
- [ ] SKILL.md renders correctly with navigation table
- [ ] SSOT references resolve to valid EN-701 content

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation from EN-709 task decomposition |
