# TASK-004: Update orch-planner Agent Spec

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
title: "Update orch-planner agent spec to auto-embed adversarial cycles"
description: |
  Update the orch-planner agent specification to automatically generate creator->critic->revision
  cycles when creating orchestration plans, based on the design from TASK-002.
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
  - orch-planner agent spec includes adversarial cycle auto-embedding logic
  - Spec defines phase detection rules for when adversarial cycles are needed
  - Creator->critic->revision pattern is formally specified in the agent definition
  - Strategy selection for auto-embedding uses EN-303 decision tree
  - Agent spec changes are backward-compatible with existing orch-planner behavior
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Update the orch-planner agent specification to automatically generate creator->critic->revision cycles when creating orchestration plans. Implement the phase detection rules, adversarial cycle injection patterns, and strategy selection logic designed in TASK-002.

### Acceptance Criteria

- [ ] orch-planner agent spec includes adversarial cycle auto-embedding logic
- [ ] Spec defines phase detection rules for when adversarial cycles are needed
- [ ] Creator->critic->revision pattern is formally specified in the agent definition
- [ ] Strategy selection for auto-embedding uses EN-303 decision tree
- [ ] Agent spec changes are backward-compatible with existing orch-planner behavior

### Implementation Notes

Depends on TASK-002 (planner design). Uses ps-architect agent. Feeds into TASK-006 (orch-synthesizer spec).

### Related Items

- Parent: [EN-307](../EN-307-orchestration-skill-enhancement.md)
- Depends on: [TASK-002](./TASK-002-design-orch-planner-adversarial.md)
- Feeds into: [TASK-006](./TASK-006-implement-orch-synthesizer-spec.md)

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
