# TASK-004: Verify H-16 in quality-enforcement.md HARD Rule Index

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
id: "TASK-004"
work_type: TASK
title: "Verify H-16 in quality-enforcement.md HARD Rule Index"
description: |
  Verify that H-16 (Steelman before critique, S-003) appears correctly in
  the quality-enforcement.md HARD Rule Index table. If missing, add it in
  the correct position with proper source reference.
classification: ENABLER
status: BACKLOG
resolution: null
priority: LOW
assignee: "ps-critic"
created_by: "Claude"
created_at: "2026-02-17"
updated_at: "2026-02-17"
parent_id: "EN-929"
tags:
  - "epic-003"
  - "feat-014"
  - "review"
effort: null
acceptance_criteria: |
  - H-16 presence in HARD Rule Index is verified
  - If missing, H-16 is added with correct format matching existing entries
  - Row references S-003 (Steelman Technique) as source
due_date: null
activity: REVIEW
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Verify that H-16 (Steelman before critique, S-003) appears correctly in the quality-enforcement.md HARD Rule Index table. The gap analysis flagged this as a potential omission. If the entry is present, document confirmation. If missing, add it in the correct numerical position between H-15 and H-17, following the existing row format.

### Acceptance Criteria

- [ ] H-16 presence in HARD Rule Index is verified (present or added)
- [ ] If added, row format matches existing entries (ID, Rule, Source columns)
- [ ] Source reference correctly points to S-003 (Steelman Technique)

### Implementation Notes

- This is primarily a verification task -- check before making changes
- The HARD Rule Index is in the quality-enforcement.md file under the HARD Rule Index section
- AE-002 applies: changes to `.context/rules/` auto-escalate to C3 minimum
- This task can run in parallel with all other EN-929 tasks

### Related Items

- Parent: [EN-929: Minor Documentation Cleanup](../EN-929-documentation-cleanup.md)
- Parallel: [TASK-001](./TASK-001-clarify-adversarial-template-naming.md), [TASK-002](./TASK-002-document-agent-directory-distinction.md), [TASK-003](./TASK-003-add-orchestration-reference.md), [TASK-005](./TASK-005-improve-adversary-usage-guidance.md)

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
| 2026-02-17 | Created | Initial creation |
