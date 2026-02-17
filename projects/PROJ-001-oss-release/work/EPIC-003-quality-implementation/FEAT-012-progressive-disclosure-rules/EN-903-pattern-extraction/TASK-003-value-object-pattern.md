# TASK-003: Create value-object-pattern.py

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

Frozen dataclass with validation in `__post_init__`. Include: `@dataclass(frozen=True, slots=True)`, validation examples, factory `@classmethod`.

The pattern file should demonstrate:
- `@dataclass(frozen=True, slots=True)` declaration
- Validation logic in `__post_init__` raising `ValidationError`
- Factory `@classmethod` for alternative construction
- Equality based on value (built-in with frozen dataclass)
- Google-style docstrings on all public functions/classes (H-12)
- Type annotations on all public functions (H-11)

### Acceptance Criteria

- [ ] Valid Python (passes ruff)
- [ ] Uses `frozen=True, slots=True`
- [ ] Validation in `__post_init__`
- [ ] Module docstring explains purpose
- [ ] Usage notes as comments

### Implementation Notes

Reference `architecture-standards.md` value object guidance. Cross-reference with actual value objects in `src/domain/` and `src/shared_kernel/` for consistency. Show both simple (single-field) and complex (multi-field with cross-field validation) examples.

### Related Items

- Parent: [EN-903: Code Pattern Extraction](EN-903-pattern-extraction.md)
- Related patterns: TASK-004 (domain event), TASK-005 (aggregate)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| value-object-pattern.py | Pattern file | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] `uv run ruff check` passes on pattern file
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-903 code pattern extraction. |
