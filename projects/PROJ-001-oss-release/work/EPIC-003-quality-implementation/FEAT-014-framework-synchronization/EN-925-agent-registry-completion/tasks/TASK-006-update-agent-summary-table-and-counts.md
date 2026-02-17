# TASK-006: Update Agent Summary Table and Counts

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
id: "TASK-006"
work_type: TASK
title: "Update agent summary table and counts"
description: |
  Update the summary table in AGENTS.md to reflect the complete agent inventory across
  all skills. Ensure total counts, per-skill counts, and any overview statistics match
  the actual agent entries added by TASK-001 through TASK-005.
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
  - Summary table includes all skills with per-skill agent counts
  - Total agent count matches sum of all per-skill counts
  - Counts verified against actual agent files in skills/*/agents/
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Update the summary table in AGENTS.md to reflect the complete agent inventory across all skills. Ensure total counts, per-skill counts, and any overview statistics match the actual agent entries added by TASK-001 through TASK-005.

### Acceptance Criteria

- [ ] Summary table includes all skills with per-skill agent counts
- [ ] Total agent count matches sum of all per-skill counts
- [ ] Counts verified against actual agent files in skills/*/agents/

### Implementation Notes

Depends on TASK-001 through TASK-005 completion. Must be done after all per-skill sections are finalized to ensure accurate totals.

### Related Items

- Parent: [EN-925](../EN-925-agent-registry-completion.md)
- Depends on: [TASK-001](./TASK-001-add-ps-critic-to-problem-solving-section.md), [TASK-002](./TASK-002-add-nasa-se-agents-section.md), [TASK-003](./TASK-003-add-orchestration-agents-section.md), [TASK-004](./TASK-004-add-adversary-agents-section.md), [TASK-005](./TASK-005-add-transcript-worktracker-agents-sections.md)

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
