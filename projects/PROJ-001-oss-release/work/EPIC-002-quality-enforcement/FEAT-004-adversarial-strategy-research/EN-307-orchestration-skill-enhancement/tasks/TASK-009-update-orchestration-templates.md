# TASK-009: Update Orchestration Templates

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
id: "TASK-009"
work_type: TASK
title: "Update orchestration templates to include adversarial sections"
description: |
  Update orchestration templates (ORCHESTRATION_PLAN.md, ORCHESTRATION.yaml,
  ORCHESTRATION_WORKTRACKER.md) to include adversarial sections by default.
classification: ENABLER
status: BACKLOG
resolution: null
priority: CRITICAL
assignee: "ps-architect"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-307"
tags:
  - "epic-002"
  - "feat-004"
effort: null
acceptance_criteria: |
  - ORCHESTRATION_PLAN.md template includes adversarial cycle sections
  - ORCHESTRATION.yaml template includes quality score schema
  - ORCHESTRATION_WORKTRACKER.md template includes adversarial tracking columns
  - Templates are backward-compatible (adversarial sections are optional/defaulted)
  - Templates are validated with sample data
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Update orchestration templates (ORCHESTRATION_PLAN.md, ORCHESTRATION.yaml, ORCHESTRATION_WORKTRACKER.md) to include adversarial sections by default. The plan template should include adversarial cycle diagrams, the YAML template should include quality score schema, and the worktracker template should include adversarial tracking columns.

### Acceptance Criteria

- [ ] ORCHESTRATION_PLAN.md template includes adversarial cycle sections
- [ ] ORCHESTRATION.yaml template includes quality score schema
- [ ] ORCHESTRATION_WORKTRACKER.md template includes adversarial tracking columns
- [ ] Templates are backward-compatible (adversarial sections are optional/defaulted)
- [ ] Templates are validated with sample data

### Implementation Notes

Depends on TASK-006 (orch-synthesizer spec). Uses ps-architect agent. Can run in parallel with TASK-007 and TASK-008. Feeds into TASK-010 (code review).

### Related Items

- Parent: [EN-307](../EN-307-orchestration-skill-enhancement.md)
- Depends on: [TASK-006](./TASK-006-implement-orch-synthesizer-spec.md)
- Feeds into: [TASK-010](./TASK-010-code-review.md)

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
