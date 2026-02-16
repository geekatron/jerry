# TASK-006: Create exception-hierarchy-pattern.py

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

Full DomainError hierarchy: `DomainError` base, `ValidationError`, `NotFoundError`, `InvalidStateError`, `InvalidStateTransitionError`, `InvariantViolationError`, `ConcurrencyError`, `QualityGateError`.

The pattern file should demonstrate:
- `DomainError` base class with common attributes
- `ValidationError(field, message)` for invalid input values
- `NotFoundError(entity_type, entity_id)` for entity not found
- `InvalidStateError(entity_type, entity_id, current_state)` for wrong state
- `InvalidStateTransitionError(current, target)` for state machine violations
- `InvariantViolationError(invariant, message)` for business rule violations
- `ConcurrencyError(entity_type, entity_id, expected, actual)` for version conflicts
- `QualityGateError(work_item_id, gate_level)` for quality check failures
- Error messages that include entity type, ID, and suggested action
- `from e` re-raising pattern shown
- Google-style docstrings on all public functions/classes (H-12)
- Type annotations on all public functions (H-11)

### Acceptance Criteria

- [ ] Valid Python (passes ruff)
- [ ] All 7 exception types present (plus base class)
- [ ] Error messages include entity type/ID/action
- [ ] `from e` re-raising shown
- [ ] Module docstring explains purpose
- [ ] Usage notes as comments

### Implementation Notes

Cross-reference with `src/shared_kernel/exceptions.py` for the actual implementation. The pattern file should match the codebase conventions exactly. Include usage examples showing how to raise and catch each exception type.

### Related Items

- Parent: [EN-903: Code Pattern Extraction](EN-903-pattern-extraction.md)
- Related patterns: TASK-001 (command handler error handling)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| exception-hierarchy-pattern.py | Pattern file | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] `uv run ruff check` passes on pattern file
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-903 code pattern extraction. |
