# TASK-004: Create coding-practices.md guide

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

Create `.context/guides/coding-practices.md` covering: type hint edge cases and best practices, import ordering rationale, Google-style docstring full examples, TYPE_CHECKING pattern explanation, error handling decision tree (which exception to use when), error message formatting guide with examples.

### Acceptance Criteria

- [ ] Navigation table present (H-23/H-24)
- [ ] Type hint edge cases documented
- [ ] Docstring examples in full
- [ ] Error handling decision tree present
- [ ] All content from original coding-standards.md explanatory sections included

### Implementation Notes

Source content from TASK-001 recovered files (original `coding-standards.md`). Include complete Google-style docstring examples with all sections (Args, Returns, Raises). Provide a decision tree or flowchart for selecting the correct exception type. Cover edge cases like forward references, circular imports, and TYPE_CHECKING blocks.

### Related Items

- Parent: [EN-902: Companion Guide Files](EN-902-companion-guides.md)
- Depends on: TASK-001 (source content)
- Related: TASK-006 (error handling -- complementary guide)

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
| coding-practices.md guide | Documentation | `.context/guides/coding-practices.md` |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Task created from EN-902 technical approach. |
