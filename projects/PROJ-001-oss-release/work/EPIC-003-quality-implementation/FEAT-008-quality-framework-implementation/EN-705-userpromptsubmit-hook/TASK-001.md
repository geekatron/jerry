# TASK-001: Create hooks/user-prompt-submit.py Hook Adapter

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
id: "TASK-001"
work_type: TASK
title: "Create hooks/user-prompt-submit.py Hook Adapter"
description: |
  Create the Claude Code hook adapter at hooks/user-prompt-submit.py
  that intercepts the UserPromptSubmit event. Follows Claude Code's
  hook protocol (JSON stdin/stdout). Delegates enforcement logic
  to the PromptReinforcementEngine. Updates hooks configuration.
classification: ENABLER
status: DONE
resolution: null
priority: CRITICAL
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-705"
tags:
  - "hook"
  - "userpromptsubmit"
  - "L2"
  - "adapter"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Create the `hooks/user-prompt-submit.py` Claude Code hook adapter that intercepts the UserPromptSubmit event. This file follows Claude Code's hook protocol: reads JSON from stdin, writes JSON to stdout. It delegates all enforcement logic to the `PromptReinforcementEngine` class (separation of concerns per hexagonal architecture). Also update the hooks configuration (`.claude/hooks.json` or equivalent) to register the UserPromptSubmit event.

## Acceptance Criteria

- [ ] `hooks/user-prompt-submit.py` file created
- [ ] Hook reads JSON from stdin following Claude Code hook protocol
- [ ] Hook writes JSON to stdout with reinforcement preamble
- [ ] Hook delegates enforcement logic to `PromptReinforcementEngine`
- [ ] Hooks configuration updated with UserPromptSubmit event registration
- [ ] Hook is executable (`chmod +x`)
- [ ] Fail-open on import/startup errors (returns empty/passthrough)

## Implementation Notes

- Claude Code hooks protocol: hook receives event data as JSON on stdin, returns response as JSON on stdout
- The hook is a thin adapter -- it should contain minimal logic
- All reinforcement content assembly happens in the engine class (TASK-002)
- The hooks configuration file location depends on Claude Code's convention
- Reference existing hooks (e.g., `scripts/pre_tool_use.py`) for protocol patterns
- Must handle the case where the engine module is not importable (fail-open)

**Design Source:** EPIC-002 EN-403/TASK-002 (UserPromptSubmit design)

## Related Items

- Parent: [EN-705: UserPromptSubmit Quality Hook](EN-705-userpromptsubmit-hook.md)
- Related: TASK-002 (engine class this adapter delegates to)
- Related: TASK-003 (fail-open error handling detailed there)

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
