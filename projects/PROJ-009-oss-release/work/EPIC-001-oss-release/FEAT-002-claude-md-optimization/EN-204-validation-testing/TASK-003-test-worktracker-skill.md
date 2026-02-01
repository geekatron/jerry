# TASK-003: Test /worktracker Skill Invocation

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Content](#content) | Description, test cases, results |
| [Time Tracking](#time-tracking) | Effort metrics |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-003"
work_type: TASK
title: "Test /worktracker Skill Invocation"
description: |
  Test that the /worktracker skill loads correctly and provides
  all entity hierarchy and mapping information.

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
  - skill

effort: 1
acceptance_criteria: |
  - /worktracker skill invokes successfully
  - Entity hierarchy information accessible
  - System mappings information accessible
  - Template references work
due_date: null

activity: TESTING
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

Test that invoking `/worktracker` loads all the extracted content and makes it available for worktracker operations.

### Test Cases

#### TC-1: Basic Invocation

1. Invoke `/worktracker`
2. Verify skill loads without errors

**Expected:** Skill loads successfully

#### TC-2: Entity Hierarchy Access

1. After invocation, ask: "What entities can be children of a Feature?"
2. Verify correct answer returned

**Expected:** "Story, Enabler" (from entity hierarchy rules)

#### TC-3: System Mappings Access

1. After invocation, ask: "How does a Story map to JIRA?"
2. Verify correct answer returned

**Expected:** "Story -> Story" (from system mappings rules)

#### TC-4: Directory Structure Access

1. After invocation, ask: "What is the directory structure for an Epic?"
2. Verify correct answer returned

**Expected:** Correct directory structure from rules

#### TC-5: Template References

1. After invocation, ask: "Where is the Task template?"
2. Verify correct path returned

**Expected:** ".context/templates/worktracker/TASK.md"

### Test Results

| Test Case | Status | Notes |
|-----------|--------|-------|
| TC-1: Basic Invocation | [ ] | - |
| TC-2: Entity Hierarchy | [ ] | - |
| TC-3: System Mappings | [ ] | - |
| TC-4: Directory Structure | [ ] | - |
| TC-5: Template References | [ ] | - |

### Acceptance Criteria

- [ ] All test cases pass
- [ ] Entity hierarchy accessible
- [ ] System mappings accessible
- [ ] Templates referenceable

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
