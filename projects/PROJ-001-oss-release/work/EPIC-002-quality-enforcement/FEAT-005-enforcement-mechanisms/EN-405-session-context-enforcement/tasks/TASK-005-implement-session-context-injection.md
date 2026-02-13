# TASK-005: Implement Session Context Injection in Hook

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | YAML metadata |
| [Content](#content) | Description and acceptance criteria |
| [Time Tracking](#time-tracking) | Effort estimates |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Frontmatter

```yaml
id: "TASK-005"
work_type: TASK
title: "Implement session context injection in hook"
description: |
  Implement the session context injection mechanism in the SessionStart hook based
  on designs from TASK-003 and TASK-004. Modify session_start_hook.py to inject
  quality framework context at session initialization.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "ps-architect"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-405"
tags:
  - "epic-002"
  - "feat-005"
  - "enforcement"
effort: null
acceptance_criteria: |
  - Session context injection implemented in session_start_hook.py
  - Quality framework context injected at session start
  - Existing hook functionality preserved (project context, error handling)
  - Unit tests written for new injection logic
  - Implementation follows hexagonal architecture patterns
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Implement the session context injection mechanism in the SessionStart hook based on designs from TASK-003 and TASK-004. Modify session_start_hook.py to inject quality framework context at session initialization.

### Acceptance Criteria

- [ ] Session context injection implemented in session_start_hook.py
- [ ] Quality framework context injected at session start
- [ ] Existing hook functionality preserved (project context, error handling)
- [ ] Unit tests written for new injection logic
- [ ] Implementation follows hexagonal architecture patterns

### Implementation Notes

Depends on TASK-003 (hook design) and TASK-004 (integration design). Can be done in parallel with TASK-006.

### Related Items

- Parent: [EN-405](../EN-405-session-context-enforcement.md)
- Depends on: [TASK-003](./TASK-003-design-session-hook-enhancement.md), [TASK-004](./TASK-004-design-integration.md)
- Feeds into: [TASK-007](./TASK-007-code-review.md)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | -- |
| Remaining Work | -- |
| Time Spent | -- |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| -- | -- | -- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-12 | Created | Initial creation |
