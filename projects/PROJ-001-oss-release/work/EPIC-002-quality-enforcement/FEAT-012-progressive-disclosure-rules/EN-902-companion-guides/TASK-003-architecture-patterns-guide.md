# TASK-003: Create architecture-patterns.md guide

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

Create `.context/guides/architecture-patterns.md` covering: command/query pattern rationale, repository pattern explanation, value object design, aggregate root patterns, domain event patterns, port/adapter naming rationale. Include CQRS file naming rationale and query verb selection guidance.

### Acceptance Criteria

- [ ] Navigation table present (H-23/H-24)
- [ ] All architecture patterns documented
- [ ] Naming convention rationale explained
- [ ] File naming patterns with examples

### Implementation Notes

Source content from TASK-001 recovered files (original `architecture-standards.md` and `file-organization.md`). Focus on pattern rationale (why commands return None, why queries return DTOs, why value objects are frozen). Include full examples of each naming convention with explanation of the naming logic.

### Related Items

- Parent: [EN-902: Companion Guide Files](EN-902-companion-guides.md)
- Depends on: TASK-001 (source content)
- Related: TASK-002 (architecture layers -- complementary guide)

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
| architecture-patterns.md guide | Documentation | `.context/guides/architecture-patterns.md` |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Task created from EN-902 technical approach. |
