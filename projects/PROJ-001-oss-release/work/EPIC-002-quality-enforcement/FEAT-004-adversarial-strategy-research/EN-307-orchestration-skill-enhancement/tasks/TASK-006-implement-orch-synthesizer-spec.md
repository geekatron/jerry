# TASK-006: Update orch-synthesizer Agent Spec

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
title: "Update orch-synthesizer to include adversarial synthesis"
description: |
  Update the orch-synthesizer agent specification to include adversarial synthesis in final
  workflow outputs, summarizing adversarial findings, quality scores, and improvement patterns.
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
  - orch-synthesizer agent spec includes adversarial synthesis section
  - Synthesis aggregates adversarial findings across all workflow phases
  - Quality score trends are summarized in synthesis output
  - Improvement patterns from adversarial cycles are captured
  - Agent spec changes are backward-compatible with existing orch-synthesizer behavior
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Update the orch-synthesizer agent specification to include adversarial synthesis in final workflow outputs. The synthesizer should aggregate adversarial findings across all workflow phases, summarize quality score trends, and capture improvement patterns from creator->critic->revision cycles.

### Acceptance Criteria

- [ ] orch-synthesizer agent spec includes adversarial synthesis section
- [ ] Synthesis aggregates adversarial findings across all workflow phases
- [ ] Quality score trends are summarized in synthesis output
- [ ] Improvement patterns from adversarial cycles are captured
- [ ] Agent spec changes are backward-compatible with existing orch-synthesizer behavior

### Implementation Notes

Depends on TASK-004 (orch-planner spec) and TASK-005 (orch-tracker spec). Uses ps-architect agent. Feeds into TASK-007, TASK-008, and TASK-009 (documentation and templates).

### Related Items

- Parent: [EN-307](../EN-307-orchestration-skill-enhancement.md)
- Depends on: [TASK-004](./TASK-004-implement-orch-planner-spec.md), [TASK-005](./TASK-005-implement-orch-tracker-spec.md)
- Feeds into: [TASK-007](./TASK-007-update-orchestration-skill-md.md), [TASK-008](./TASK-008-update-orchestration-playbook-md.md), [TASK-009](./TASK-009-update-orchestration-templates.md)

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
