# TASK-003: Integrate Generator into session_start_hook.py

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
title: "Integrate Generator into session_start_hook.py"
description: |
  Add quality preamble injection into scripts/session_start_hook.py
  after the existing project context output. Emit the preamble as a
  <quality-context> XML block. Ensure no regression in existing
  project context resolution functionality.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-706"
tags:
  - "session-start"
  - "hook-integration"
  - "quality-context"
  - "L1"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Integrate the `SessionQualityContextGenerator` into the existing `scripts/session_start_hook.py` to inject the quality framework preamble at session start. The quality preamble is emitted as a `<quality-context>` XML block after the existing project context output (`<project-context>` or `<project-required>`). The integration must not cause any regression in the existing project context resolution functionality.

## Acceptance Criteria

- [ ] `SessionQualityContextGenerator` imported and invoked in `scripts/session_start_hook.py`
- [ ] Quality preamble emitted as `<quality-context>` XML block in hook output
- [ ] Preamble appears after existing project context output
- [ ] No regression in existing project context resolution (project-context, project-required, project-error tags)
- [ ] Fail-open on generator errors (log and skip preamble, do not break session start)
- [ ] Hook output remains valid for Claude Code's session start protocol

## Implementation Notes

- The existing `scripts/session_start_hook.py` handles JERRY_PROJECT resolution
- Add the quality context injection after the project context block
- Use try/except around generator invocation for fail-open behavior
- The `<quality-context>` block should be clearly separated from `<project-context>`
- Test with both valid and missing JERRY_PROJECT to ensure no regression
- The hook output is consumed by Claude Code's session initialization

**Design Source:** EPIC-002 EN-403/TASK-004 (SessionStart design)

## Related Items

- Parent: [EN-706: SessionStart Quality Context Enhancement](EN-706-sessionstart-quality-context.md)
- Depends on: TASK-001 (generator class), TASK-002 (token budget)
- Related: EN-705 TASK-001 (similar hook adapter integration pattern)

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
