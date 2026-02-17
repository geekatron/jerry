# TASK-001: Add ps-critic to Problem-Solving Agents Section

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
id: "TASK-001"
work_type: TASK
title: "Add ps-critic to problem-solving agents section"
description: |
  Add the ps-critic agent entry to the existing problem-solving section in AGENTS.md.
  Currently the problem-solving section lists 8 agents but omits ps-critic. Extract role,
  cognitive mode, and file path from the agent file and add in consistent format.
classification: ENABLER
status: BACKLOG
resolution: null
priority: CRITICAL
assignee: "ps-architect"
created_by: "Claude"
created_at: "2026-02-17"
updated_at: "2026-02-17"
parent_id: "EN-925"
tags:
  - "epic-003"
  - "feat-014"
  - "agent-registry"
effort: null
acceptance_criteria: |
  - ps-critic entry added to problem-solving section with role, file path, cognitive mode
  - Entry follows same format as existing 8 agents in the section
  - Problem-solving agent count updated to 9
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Add the ps-critic agent entry to the existing problem-solving section in AGENTS.md. Currently the problem-solving section lists 8 agents but omits ps-critic. Extract role, cognitive mode, and file path from the agent file and add in consistent format.

### Acceptance Criteria

- [ ] ps-critic entry added to problem-solving section with role, file path, cognitive mode
- [ ] Entry follows same format as existing 8 agents in the section
- [ ] Problem-solving agent count updated to 9

### Implementation Notes

Read `skills/problem-solving/agents/ps-critic.md` to extract required fields. Add entry to the existing problem-solving table in AGENTS.md.

### Related Items

- Parent: [EN-925](../EN-925-agent-registry-completion.md)

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
