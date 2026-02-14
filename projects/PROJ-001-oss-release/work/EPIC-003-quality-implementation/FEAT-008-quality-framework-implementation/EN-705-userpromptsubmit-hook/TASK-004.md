# TASK-004: Unit and Integration Tests for Prompt Reinforcement

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
id: "TASK-004"
work_type: TASK
title: "Unit and Integration Tests for Prompt Reinforcement"
description: |
  Write unit tests for PromptReinforcementEngine (token budget validation,
  content assembly, error handling). Write integration test for the
  UserPromptSubmit hook end-to-end. Verify uv run pytest passes.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-705"
tags:
  - "testing"
  - "unit-tests"
  - "integration-tests"
  - "prompt-reinforcement"
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Write unit tests for the `PromptReinforcementEngine` covering token budget validation, content assembly, required section presence, and error handling. Write an integration test for the `hooks/user-prompt-submit.py` hook end-to-end simulating Claude Code's JSON stdin/stdout protocol. Verify all tests pass via `uv run pytest`.

## Acceptance Criteria

- [ ] Unit tests for engine content assembly (all required sections present)
- [ ] Unit tests for 600-token budget constraint (content within budget, trimming works)
- [ ] Unit tests for error handling (engine gracefully handles missing rules files)
- [ ] Integration test for hook end-to-end with simulated JSON stdin/stdout
- [ ] Integration test for fail-open behavior (engine error returns empty response)
- [ ] Test naming follows `test_{scenario}_when_{condition}_then_{expected}` convention
- [ ] `uv run pytest` passes with all new tests

## Implementation Notes

- Unit test location: `tests/unit/infrastructure/enforcement/test_prompt_reinforcement_engine.py`
- Integration test location: `tests/integration/test_user_prompt_submit_hook.py`
- Use AAA (Arrange-Act-Assert) pattern
- For integration tests, use `subprocess.run` to execute the hook with JSON input
- Mock rules files for unit tests to avoid filesystem dependency
- Test edge cases: empty rules directory, corrupted rules files, extremely long content

**Design Source:** testing-standards.md (BDD cycle, AAA pattern, test naming convention)

## Related Items

- Parent: [EN-705: UserPromptSubmit Quality Hook](EN-705-userpromptsubmit-hook.md)
- Depends on: TASK-001 (hook adapter), TASK-002 (engine), TASK-003 (fail-open)

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
