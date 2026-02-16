# TASK-006: Create error-handling.md guide

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

Create `.context/guides/error-handling.md` covering: full exception hierarchy with code examples, DomainError base class implementation, each exception type with use cases and examples, error message formatting patterns, exception selection decision tree (flowchart: given this situation, throw this exception), re-raising patterns with `from e`.

### Acceptance Criteria

- [ ] Navigation table present (H-23/H-24)
- [ ] Full exception hierarchy code
- [ ] Decision tree for exception selection
- [ ] Error message examples
- [ ] All content from original error-handling-standards.md included

### Implementation Notes

Source content from TASK-001 recovered files (original `error-handling-standards.md` and error handling sections of `coding-standards.md`). Include the complete exception class hierarchy with code. Provide a decision tree that maps situations to exception types. Show error message formatting with concrete examples including entity type, ID, and suggested action.

### Related Items

- Parent: [EN-902: Companion Guide Files](EN-902-companion-guides.md)
- Depends on: TASK-001 (source content)
- Related: TASK-004 (coding practices -- complementary guide)

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
| error-handling.md guide | Documentation | `.context/guides/error-handling.md` |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Task created from EN-902 technical approach. |
