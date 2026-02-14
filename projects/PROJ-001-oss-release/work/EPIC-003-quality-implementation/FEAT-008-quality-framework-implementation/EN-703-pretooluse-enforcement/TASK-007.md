# TASK-007: Unit and Integration Tests for Enforcement Engine

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Related Items](#related-items) | Cross-references and dependencies |
| [Evidence](#evidence) | Proof of completion |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-007"
work_type: TASK
title: "Unit and Integration Tests for Enforcement Engine"
description: |
  Write unit tests for each vector checker in isolation (V-038, V-039,
  V-040, V-041). Write integration test for the PreToolUse hook
  end-to-end with mock tool calls. Verify uv run pytest passes.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-703"
tags:
  - "testing"
  - "enforcement"
  - "unit-tests"
  - "integration-tests"
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Write comprehensive unit tests for each vector checker (V-038 import boundary, V-039 type hints, V-040 docstrings, V-041 one-class-per-file) in isolation, plus an integration test for the PreToolUse hook end-to-end with mock tool calls. Tests must cover happy path (compliant code passes), negative cases (violations detected), and edge cases (unusual but valid inputs). All tests must pass via `uv run pytest`.

## Acceptance Criteria

- [ ] Unit tests for V-038 import boundary checker (happy path, negative, edge cases)
- [ ] Unit tests for V-039 type hint checker (happy path, negative, edge cases)
- [ ] Unit tests for V-040 docstring checker (happy path, negative, edge cases)
- [ ] Unit tests for V-041 one-class-per-file checker (happy path, negative, edge cases)
- [ ] Unit tests for PreToolEnforcementEngine orchestration logic
- [ ] Integration test for pre_tool_use.py hook end-to-end with mock tool calls
- [ ] Fail-open behavior tested (engine error does not block operation)
- [ ] `uv run pytest` passes with all new tests

## Implementation Notes

- Test location: `tests/unit/infrastructure/enforcement/` for unit tests
- Test location: `tests/integration/` for hook integration test
- Use AAA (Arrange-Act-Assert) pattern
- Naming: `test_{scenario}_when_{condition}_then_{expected}`
- For integration test, simulate Claude Code's JSON stdin/stdout protocol
- Edge cases to consider:
  - Empty files
  - Files with syntax errors (engine should not crash)
  - Files with only comments
  - Nested classes (private inner classes)

**Design Source:** testing-standards.md (BDD cycle, test pyramid, AAA pattern)

## Related Items

- Parent: [EN-703: PreToolUse Enforcement Engine](EN-703-pretooluse-enforcement.md)
- Depends on: TASK-001 through TASK-006 (all implementation tasks)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| _None yet_ | — | — |

### Verification

- [ ] Acceptance criteria verified
- [ ] Code review passed
- [ ] Reviewed by: _pending_

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation |
