# TASK-005: Create testing-practices.md guide

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

Create `.context/guides/testing-practices.md` covering: AAA pattern with full code examples, test naming convention rationale, fixture and factory patterns, mocking philosophy (what to mock vs not), coverage exclusion rationale, BDD red/green/refactor detailed walkthrough, property-based testing guidance.

### Acceptance Criteria

- [ ] Navigation table present (H-23/H-24)
- [ ] AAA code examples present
- [ ] Mocking guidelines with rationale
- [ ] BDD walkthrough complete
- [ ] All content from original testing-standards.md explanatory sections included

### Implementation Notes

Source content from TASK-001 recovered files (original `testing-standards.md` and `tool-configuration.md`). Include complete Python code examples for AAA pattern. Provide rationale for why domain objects should never be mocked. Walk through a full BDD red/green/refactor cycle with a concrete example from the Jerry codebase.

### Related Items

- Parent: [EN-902: Companion Guide Files](EN-902-companion-guides.md)
- Depends on: TASK-001 (source content)

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
| testing-practices.md guide | Documentation | `.context/guides/testing-practices.md` |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Task created from EN-902 technical approach. |
