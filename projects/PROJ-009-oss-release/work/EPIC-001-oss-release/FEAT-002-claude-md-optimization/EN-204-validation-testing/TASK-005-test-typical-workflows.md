# TASK-005: Test Typical Workflows

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-005"
work_type: TASK
title: "Test Typical Workflows"
description: |
  Test typical workflows (project creation, work tracking) to ensure
  no regression from the CLAUDE.md optimization.

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
  - workflow

effort: 1
acceptance_criteria: |
  - Project context workflow works
  - Work item creation workflow works
  - Task tracking workflow works
  - No regressions detected
due_date: null

activity: TESTING
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

Execute typical Jerry workflows to ensure the CLAUDE.md optimization has not introduced any regressions.

### Workflow Test Cases

#### WF-1: Project Context Query

1. Ask: "What project am I working on?"
2. Verify Claude identifies active project from `<project-context>`

**Expected:** Correct project identified from SessionStart hook

#### WF-2: Work Item Creation Guidance

1. Ask: "How do I create a new Task?"
2. Invoke /worktracker if not already loaded
3. Verify correct guidance provided

**Expected:** Points to template, explains process

#### WF-3: Entity Hierarchy Navigation

1. Ask: "What is the parent of a Task?"
2. Verify correct answer

**Expected:** "Story, Bug, or Enabler"

#### WF-4: System Mapping Query

1. Ask: "I'm using Azure DevOps, what maps to a Story?"
2. Verify correct mapping

**Expected:** "Product Backlog Item (PBI)"

#### WF-5: CLI Usage

1. Ask: "How do I list work items?"
2. Verify CLI command provided

**Expected:** "`jerry items list`"

### Test Results

| Workflow | Status | Notes |
|----------|--------|-------|
| WF-1: Project Context | [ ] | - |
| WF-2: Work Item Creation | [ ] | - |
| WF-3: Entity Hierarchy | [ ] | - |
| WF-4: System Mapping | [ ] | - |
| WF-5: CLI Usage | [ ] | - |

### Acceptance Criteria

- [ ] All workflow tests pass
- [ ] No regressions detected
- [ ] Behavior matches pre-optimization

### Related Items

- Parent: [EN-204: Validation & Testing](./EN-204-validation-testing.md)

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 1 hour |
| Remaining Work | 1 hour |
| Time Spent | 0 hours |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
