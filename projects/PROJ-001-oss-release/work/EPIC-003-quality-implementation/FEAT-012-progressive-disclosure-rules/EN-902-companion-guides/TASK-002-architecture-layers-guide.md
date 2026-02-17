# TASK-002: Create architecture-layers.md guide

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Agents:** --
> **Created:** 2026-02-16
> **Parent:** EN-902

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description, acceptance criteria, implementation notes |
| [Time Tracking](#time-tracking) | Effort estimates |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Content

### Description

Create `.context/guides/architecture-layers.md` covering: layer dependency rationale (why domain cannot import infrastructure), import boundary examples, hexagonal architecture explanation, CQRS theory and application, event sourcing concepts, composition root pattern. Include code examples showing correct and incorrect imports.

### Acceptance Criteria

- [ ] Navigation table present (H-23/H-24)
- [ ] Layer dependency rationale explained
- [ ] Code examples for correct/incorrect imports
- [ ] All content from original architecture-standards.md explanatory sections included

### Implementation Notes

Source content from TASK-001 recovered files (original `architecture-standards.md`). Focus on the "why" behind each layer constraint. Include concrete Python import examples showing both correct (allowed) and incorrect (forbidden) patterns. Explain hexagonal architecture in the context of Jerry's specific domain.

### Related Items

- Parent: [EN-902: Companion Guide Files](EN-902-companion-guides.md)
- Depends on: TASK-001 (source content)
- Related: TASK-003 (architecture patterns -- complementary guide)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | -- |
| Remaining Work | -- |
| Time Spent | -- |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| architecture-layers.md guide | Documentation | `.context/guides/architecture-layers.md` |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Task created from EN-902 technical approach. |
