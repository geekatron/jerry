# TASK-002: Create repository-pattern.py

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

Repository port + filesystem adapter example. Include: `IRepository` protocol, filesystem adapter implementation, event sourcing integration.

The pattern file should demonstrate:
- `IRepository` protocol in domain layer with abstract methods
- Filesystem adapter implementation in infrastructure layer
- Event sourcing integration (load from events, append events)
- Proper layer separation (H-07: domain MUST NOT import infrastructure)
- Google-style docstrings on all public functions/classes (H-12)
- Type annotations on all public functions (H-11)

### Acceptance Criteria

- [ ] Valid Python (passes ruff)
- [ ] Port/adapter separation correct
- [ ] Follows H-07/H-08 layer rules
- [ ] Module docstring explains purpose
- [ ] Usage notes as comments

### Implementation Notes

Reference `architecture-standards.md` for naming conventions: port as `I{Noun}` (e.g., `IRepository`), adapter as `{Tech}{Entity}Adapter` (e.g., `FilesystemProjectAdapter`). Verify against actual implementations in `src/domain/` and `src/infrastructure/`.

### Related Items

- Parent: [EN-903: Code Pattern Extraction](EN-903-pattern-extraction.md)
- Related patterns: TASK-001 (command handler), TASK-005 (aggregate)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| repository-pattern.py | Pattern file | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] `uv run ruff check` passes on pattern file
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-903 code pattern extraction. |
