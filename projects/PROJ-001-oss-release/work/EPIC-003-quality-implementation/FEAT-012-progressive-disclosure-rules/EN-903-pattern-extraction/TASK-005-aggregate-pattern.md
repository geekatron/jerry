# TASK-005: Create aggregate-pattern.py

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

Aggregate root with `apply_event()` and `collect_events()` methods, event sourcing pattern.

The pattern file should demonstrate:
- Aggregate root class with internal state
- `apply_event()` method for event application
- `collect_events()` method for pending event retrieval
- Event sourcing reconstruction from event stream
- Command methods that produce domain events
- Google-style docstrings on all public functions/classes (H-12)
- Type annotations on all public functions (H-11)

### Acceptance Criteria

- [ ] Valid Python (passes ruff)
- [ ] `apply_event` / `collect_events` present
- [ ] Event sourcing integration demonstrated
- [ ] Module docstring explains purpose
- [ ] Usage notes as comments

### Implementation Notes

Reference `architecture-standards.md` for aggregate guidance. Cross-reference with actual aggregates in `src/domain/` for consistency. Show the full lifecycle: create aggregate, execute commands, collect events, reconstruct from events.

### Related Items

- Parent: [EN-903: Code Pattern Extraction](EN-903-pattern-extraction.md)
- Related patterns: TASK-002 (repository), TASK-004 (domain event)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| aggregate-pattern.py | Pattern file | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] `uv run ruff check` passes on pattern file
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-903 code pattern extraction. |
