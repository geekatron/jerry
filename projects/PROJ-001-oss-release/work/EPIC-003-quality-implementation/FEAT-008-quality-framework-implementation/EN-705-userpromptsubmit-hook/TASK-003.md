# TASK-003: Implement Fail-Open Error Handling

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
id: "TASK-003"
work_type: TASK
title: "Implement Fail-Open Error Handling"
description: |
  Implement fail-open error handling for the UserPromptSubmit hook.
  Hook errors must never block user work. On error: return empty/passthrough
  block and log the error for diagnostics.
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
  - "error-handling"
  - "fail-open"
  - "resilience"
  - "hook"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Implement fail-open error handling for the UserPromptSubmit hook and engine. The fundamental principle: enforcement hooks must never block user work due to internal errors. If the `PromptReinforcementEngine` raises any exception, the hook must catch it, log the error for diagnostics, and return an empty/passthrough response that allows the user's prompt to proceed without reinforcement content. This applies to import errors, runtime errors, and any other failure mode.

## Acceptance Criteria

- [ ] Hook catches all exceptions from the engine (including import errors)
- [ ] On error, hook returns empty/passthrough JSON response
- [ ] Errors logged to a diagnostics file (e.g., `/tmp/jerry-hook-errors.log` or similar)
- [ ] Log includes timestamp, error type, error message, and stack trace
- [ ] Hook startup errors (missing dependencies, syntax errors) handled gracefully
- [ ] No user-visible error output on stderr that would confuse the user

## Implementation Notes

- Wrap the entire hook execution in a top-level try/except
- Use a separate try/except for the import of the engine module
- Log file location should be deterministic and documented
- Consider using Python's `logging` module with a file handler
- Test by simulating engine failures (mock that raises exceptions)
- The hook script itself should never exit with a non-zero code on engine errors

**Design Source:** EPIC-002 EN-403/TASK-002 (fail-open requirement)

## Related Items

- Parent: [EN-705: UserPromptSubmit Quality Hook](EN-705-userpromptsubmit-hook.md)
- Related: TASK-001 (hook adapter where fail-open is implemented)
- Related: TASK-002 (engine that may produce errors to handle)
- Related: EN-703 TASK-006 (same fail-open pattern for PreToolUse hook)

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
