# TASK-002: Create Hook Enforcement End-to-End Tests

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 0.1.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Summary

```yaml
id: "TASK-002"
work_type: TASK
title: "Create hook enforcement end-to-end tests"
description: |
  Write end-to-end tests for each hook type (PreToolUse, UserPromptSubmit, SessionStart)
  in realistic scenarios with actual file system state. Tests verify that hooks correctly
  enforce quality constraints when invoked with real inputs and produce correct enforcement
  outputs for downstream consumers.
classification: ENABLER
status: DONE
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-711"
tags:
  - "e2e-testing"
  - "hooks"
  - "enforcement"
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Create end-to-end tests for the three hook types that form L1 enforcement:

1. **PreToolUse hook** -- Test that the hook correctly intercepts tool invocations and applies quality constraints (e.g., blocking destructive operations without confirmation)
2. **UserPromptSubmit hook** -- Test that user prompts are correctly validated against quality rules before processing
3. **SessionStart hook** -- Test that session initialization correctly injects quality context, project state, and enforcement configuration

Tests must use realistic file system state (actual project directories, config files) rather than mocks, to validate true end-to-end behavior.

### Acceptance Criteria

- [ ] PreToolUse hook E2E tests implemented with realistic scenarios
- [ ] UserPromptSubmit hook E2E tests implemented with realistic scenarios
- [ ] SessionStart hook E2E tests implemented with realistic scenarios
- [ ] Tests use actual file system state (not mocked)
- [ ] Tests validate correct enforcement output format and content
- [ ] All tests pass via `uv run pytest tests/e2e/`

### Implementation Notes

- Use temporary directories with realistic project structure for test isolation
- Reference EN-703 (PreToolUse) and EN-705 (UserPromptSubmit) for hook specifications
- Test both enforcement (blocking) and advisory (warning) scenarios
- Verify hook output can be consumed by downstream layers

### Related Items

- Parent: [EN-711: E2E Integration Testing](EN-711-e2e-integration-testing.md)
- Blocks: TASK-007 (adversarial review of test completeness)
- Related: EN-703 (PreToolUse hook implementation), EN-705 (UserPromptSubmit hook implementation)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | 0 hours |
| Time Spent | — |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Hook E2E tests | Test suite | `tests/e2e/` |

### Verification

- [ ] Acceptance criteria verified
- [ ] All hook E2E tests pass
- [ ] Tests cover both enforcement and advisory scenarios
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation from EN-711 task decomposition |
