# TASK-001: Start Fresh Claude Code Session for Baseline

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-001"
work_type: TASK
title: "Start Fresh Claude Code Session for Baseline"
description: |
  Start a fresh Claude Code session to establish a baseline for
  token count and context utilization measurement.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-204"
tags:
  - enabler
  - validation
  - testing

effort: 0.5
acceptance_criteria: |
  - Fresh session started
  - JERRY_PROJECT set correctly
  - SessionStart hook executes
  - Baseline established
due_date: null

activity: TESTING
original_estimate: 0.5
remaining_work: 0.5
time_spent: null
```

---

## Content

### Description

Start a completely fresh Claude Code session with the optimized CLAUDE.md to establish a baseline for measuring the optimization impact.

### Test Procedure

1. Close all existing Claude Code sessions
2. Set JERRY_PROJECT environment variable
3. Start new Claude Code session
4. Wait for SessionStart hook to complete
5. Note context load time (if observable)
6. Proceed to TASK-002 for token count verification

### Acceptance Criteria

- [ ] Fresh session started (no prior context)
- [ ] JERRY_PROJECT correctly set
- [ ] SessionStart hook executes successfully
- [ ] Project context loaded via `<project-context>` tag

### Related Items

- Parent: [EN-204: Validation & Testing](./EN-204-validation-testing.md)

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 0.5 hours |
| Remaining Work | 0.5 hours |
| Time Spent | 0 hours |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
