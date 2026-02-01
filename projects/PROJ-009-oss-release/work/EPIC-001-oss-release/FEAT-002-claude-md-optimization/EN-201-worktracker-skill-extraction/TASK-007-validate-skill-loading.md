# TASK-007: Validate Skill Loads Correctly

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
| [Content](#content) | Description and test cases |
| [Time Tracking](#time-tracking) | Effort metrics |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-007"
work_type: TASK
title: "Validate Skill Loads Correctly"
description: |
  Validate that the /worktracker skill loads all entity and mapping information
  correctly when invoked.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-201"
tags:
  - enabler
  - validation
  - worktracker
  - testing

effort: 1
acceptance_criteria: |
  - /worktracker skill invocation successful
  - All rules files load correctly
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

After all rules files are created and SKILL.md is updated, validate that invoking `/worktracker` loads all the content correctly and makes it available for worktracker operations.

### Dependencies

This task depends on completion of:
- TASK-006: Update SKILL.md with navigation pointers

### Test Cases

#### TC-1: Skill Invocation

1. Start a Claude Code session
2. Invoke `/worktracker`
3. Verify skill loads without errors

**Expected:** Skill loads successfully with all rules

#### TC-2: Entity Hierarchy Access

1. After invoking `/worktracker`
2. Ask about entity hierarchy (e.g., "What entities can be children of a Feature?")
3. Verify correct information returned

**Expected:** Information matches worktracker-entity-hierarchy.md content

#### TC-3: System Mappings Access

1. After invoking `/worktracker`
2. Ask about system mappings (e.g., "How does a Story map to JIRA?")
3. Verify correct information returned

**Expected:** Information matches worktracker-system-mappings.md content

#### TC-4: Template References

1. After invoking `/worktracker`
2. Ask about creating a Task
3. Verify template location referenced correctly

**Expected:** Points to .context/templates/worktracker/TASK.md

### Acceptance Criteria

- [ ] TC-1: Skill invocation passes
- [ ] TC-2: Entity hierarchy access passes
- [ ] TC-3: System mappings access passes
- [ ] TC-4: Template references pass
- [ ] No errors or missing content identified

### Issue Tracking

If issues are found, document them here:

| Issue | Severity | Status | Resolution |
|-------|----------|--------|------------|
| - | - | - | - |

### Related Items

- Parent: [EN-201: Worktracker Skill Extraction](./EN-201-worktracker-skill-extraction.md)
- Dependencies: TASK-001 through TASK-006

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 1 hour |
| Remaining Work | 1 hour |
| Time Spent | 0 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Test Results | Documentation | (inline in this file) |

### Verification

- [ ] All test cases executed
- [ ] All test cases passed
- [ ] Reviewed by: -

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
