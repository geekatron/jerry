# TASK-002: Add NASA-SE Agents Section (10 Agents)

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
id: "TASK-002"
work_type: TASK
title: "Add NASA-SE agents section (10 agents)"
description: |
  Create a new NASA-SE section in AGENTS.md and add all 10 NASA-SE agents. Read each agent
  file from skills/nasa-se/agents/ to extract role, cognitive mode, and file path. Follow
  the same section format used for problem-solving agents.
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
  - New NASA-SE section created in AGENTS.md following problem-solving format
  - All 10 NASA-SE agents listed with role, file path, cognitive mode
  - Agent count matches actual files in skills/nasa-se/agents/
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Create a new NASA-SE section in AGENTS.md and add all 10 NASA-SE agents. Read each agent file from `skills/nasa-se/agents/` to extract role, cognitive mode, and file path. Follow the same section format used for problem-solving agents.

### Acceptance Criteria

- [ ] New NASA-SE section created in AGENTS.md following problem-solving format
- [ ] All 10 NASA-SE agents listed with role, file path, cognitive mode
- [ ] Agent count matches actual files in skills/nasa-se/agents/

### Implementation Notes

Largest agent group. Read all files in `skills/nasa-se/agents/` and create a comprehensive table entry for each.

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
