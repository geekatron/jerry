# TASK-004: Create Session Context Injection Verification Tests

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
| [Related Items](#related-items) | Dependencies and hierarchy |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Summary

```yaml
id: "TASK-004"
work_type: TASK
title: "Create session context injection verification tests"
description: |
  Write tests that verify the session start hook correctly injects quality context
  into the session and that downstream components (rules, skills) correctly consume
  the injected context. Validates the L2 enforcement layer and its integration with
  L3 (rules) and L4 (skills).
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-711"
tags:
  - "e2e-testing"
  - "session-context"
  - "injection-verification"
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Create tests that validate session context injection and consumption:

1. **Context injection** -- Verify that the session start hook produces correct XML tags (`<project-context>`, `<project-required>`, `<project-error>`) with quality enforcement data
2. **Context consumption by rules** -- Verify that rule files can parse and apply the injected context correctly
3. **Context consumption by skills** -- Verify that skills receive and use session quality context for enforcement decisions
4. **Missing context handling** -- Verify that missing or malformed session context is detected and reported (not silently ignored)

### Acceptance Criteria

- [ ] Session context injection tests verify correct XML tag output
- [ ] Tests verify rules correctly consume injected quality context
- [ ] Tests verify skills correctly consume injected quality context
- [ ] Tests verify missing/malformed context is detected and handled
- [ ] All tests pass via `uv run pytest tests/e2e/`

### Implementation Notes

- Reference the session start hook at `scripts/session_start_hook.py`
- Test with various JERRY_PROJECT values (valid, invalid, missing)
- Verify XML tag format matches contract specification
- Test both happy path (valid project) and error paths (missing project, invalid ID)

### Related Items

- Parent: [EN-711: E2E Integration Testing](EN-711-e2e-integration-testing.md)
- Blocks: TASK-007 (adversarial review of test completeness)
- Related: EN-704 (session context optimization)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Session context tests | Test suite | `tests/e2e/` |

### Verification

- [ ] Acceptance criteria verified
- [ ] All session context tests pass
- [ ] Tests cover valid, invalid, and missing project scenarios
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation from EN-711 task decomposition |
