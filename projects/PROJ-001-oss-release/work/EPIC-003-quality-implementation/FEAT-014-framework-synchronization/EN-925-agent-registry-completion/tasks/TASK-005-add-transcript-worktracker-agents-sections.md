# TASK-005: Add Transcript and Worktracker Agents Sections (7 Agents)

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
title: "Add Transcript and Worktracker agents sections (7 agents)"
description: |
  Create new Transcript and Worktracker sections in AGENTS.md. Add all 4 transcript agents
  and all 3 worktracker agents. Read each agent file from skills/transcript/agents/ and
  skills/worktracker/agents/ to extract role, cognitive mode, and file path. Follow the
  same section format used for problem-solving agents.
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
  - New Transcript section created with all 4 transcript agents
  - New Worktracker section created with all 3 worktracker agents
  - Agent counts match actual files in respective skills/*/agents/ directories
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Create new Transcript and Worktracker sections in AGENTS.md. Add all 4 transcript agents and all 3 worktracker agents. Read each agent file from `skills/transcript/agents/` and `skills/worktracker/agents/` to extract role, cognitive mode, and file path. Follow the same section format used for problem-solving agents.

### Acceptance Criteria

- [ ] New Transcript section created with all 4 transcript agents listed
- [ ] New Worktracker section created with all 3 worktracker agents listed
- [ ] Agent counts match actual files in respective skills/*/agents/ directories

### Implementation Notes

Two smaller agent groups combined into one task. Read all files in `skills/transcript/agents/` and `skills/worktracker/agents/` and create two separate sections.

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
