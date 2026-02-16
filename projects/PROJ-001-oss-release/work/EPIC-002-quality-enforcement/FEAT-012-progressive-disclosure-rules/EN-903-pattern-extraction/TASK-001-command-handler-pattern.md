# TASK-001: Create command-handler-pattern.py

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

Canonical command handler implementation following CQRS conventions. Include: command class with `@dataclass`, handler class with type hints, port protocol, error handling pattern.

The pattern file should demonstrate:
- Command class using `@dataclass(frozen=True, slots=True)` with typed fields
- Handler class with `__call__` or `handle` method
- Primary port protocol (`ICommandHandler`)
- Proper error handling using the DomainError hierarchy
- Google-style docstrings on all public functions/classes (H-12)
- Type annotations on all public functions (H-11)

### Acceptance Criteria

- [ ] Valid Python (passes ruff)
- [ ] Follows naming conventions (H-11, H-12)
- [ ] Matches `src/` codebase style
- [ ] Module docstring explains purpose
- [ ] Usage notes as comments

### Implementation Notes

Reference `architecture-standards.md` for naming conventions: command class as `{Verb}{Noun}Command`, handler class as `{CommandOrQuery}Handler`. Cross-reference with actual implementations in `src/application/` for consistency.

### Related Items

- Parent: [EN-903: Code Pattern Extraction](EN-903-pattern-extraction.md)
- Related patterns: TASK-002 (repository), TASK-006 (exception hierarchy)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| command-handler-pattern.py | Pattern file | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] `uv run ruff check` passes on pattern file
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-903 code pattern extraction. |
