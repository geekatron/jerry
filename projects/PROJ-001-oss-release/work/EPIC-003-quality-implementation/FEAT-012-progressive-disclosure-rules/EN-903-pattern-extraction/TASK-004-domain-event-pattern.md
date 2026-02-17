# TASK-004: Create domain-event-pattern.py

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Created:** 2026-02-16
> **Parent:** EN-903

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description, acceptance criteria, implementation notes |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Content

### Description

Domain event class with `EVENT_TYPE` class variable, past tense naming, factory `@classmethod` for timestamps.

The pattern file should demonstrate:
- Domain event class with `EVENT_TYPE` class variable
- Past tense naming convention (e.g., `WorkItemCreated`, `StatusChanged`)
- Factory `@classmethod` that auto-generates timestamps
- Immutable event data using `@dataclass(frozen=True)`
- Google-style docstrings on all public functions/classes (H-12)
- Type annotations on all public functions (H-11)

### Acceptance Criteria

- [ ] Valid Python (passes ruff)
- [ ] Past tense naming convention used
- [ ] `EVENT_TYPE` class variable present
- [ ] Factory `@classmethod` present
- [ ] Module docstring explains purpose
- [ ] Usage notes as comments

### Implementation Notes

Reference `architecture-standards.md` for event naming: `{Noun}{PastVerb}` (e.g., `WorkItemCreated`). Cross-reference with actual events in `src/domain/` for consistency. Show both simple and complex event examples with payload data.

### Related Items

- Parent: [EN-903: Code Pattern Extraction](EN-903-pattern-extraction.md)
- Related patterns: TASK-003 (value object), TASK-005 (aggregate)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| domain-event-pattern.py | Pattern file | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] `uv run ruff check` passes on pattern file
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-903 code pattern extraction. |
