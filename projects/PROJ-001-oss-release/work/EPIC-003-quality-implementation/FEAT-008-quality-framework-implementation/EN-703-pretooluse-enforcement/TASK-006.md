# TASK-006: Enhance pre_tool_use.py with Engine Integration

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
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Related Items](#related-items) | Cross-references and dependencies |
| [Evidence](#evidence) | Proof of completion |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-006"
work_type: TASK
title: "Enhance pre_tool_use.py with Engine Integration"
description: |
  Integrate the PreToolEnforcementEngine into the existing
  scripts/pre_tool_use.py hook. Route file write operations through
  the engine. Implement fail-open error handling so engine errors
  do not block user work.
classification: ENABLER
status: DONE
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-703"
tags:
  - "enforcement"
  - "pretooluse"
  - "hook-integration"
  - "fail-open"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Enhance the existing `scripts/pre_tool_use.py` hook to integrate with the `PreToolEnforcementEngine`. File write operations (Write, Edit tool calls) are routed through the engine for AST-based validation. The hook must implement fail-open error handling: if the engine raises an exception or encounters an error, the operation is allowed to proceed (logged but not blocked). This ensures enforcement never prevents legitimate user work due to engine bugs.

## Acceptance Criteria

- [ ] `scripts/pre_tool_use.py` enhanced to import and use `PreToolEnforcementEngine`
- [ ] File write operations (Write, Edit) routed through the engine for validation
- [ ] Engine violations result in blocking the tool call (returning reject/error response)
- [ ] Fail-open error handling: engine exceptions logged and operation allowed to proceed
- [ ] Non-Python files are passed through without enforcement
- [ ] Hook follows Claude Code's PreToolUse protocol (JSON stdin/stdout)
- [ ] No regression in existing pre_tool_use.py functionality

## Implementation Notes

- The existing `scripts/pre_tool_use.py` reads JSON from stdin with tool call details
- For Write/Edit tools, extract the file content and file path
- Only enforce on `.py` files within the `src/` directory
- Fail-open pattern: wrap engine call in try/except, log errors, allow operation
- The hook should instantiate the engine with all vector checkers registered
- Consider logging violations to a file for diagnostics

**Design Source:** EPIC-002 EN-403/TASK-003 (PreToolUse design)

## Related Items

- Parent: [EN-703: PreToolUse Enforcement Engine](EN-703-pretooluse-enforcement.md)
- Depends on: TASK-001 (engine class), TASK-002 through TASK-005 (vector checkers)

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
