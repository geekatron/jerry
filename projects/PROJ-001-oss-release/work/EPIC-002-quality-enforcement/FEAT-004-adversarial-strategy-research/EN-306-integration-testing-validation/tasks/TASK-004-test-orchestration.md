# TASK-004: Test Adversarial Loops in /orchestration

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
title: "Test adversarial loops in /orchestration"
description: |
  Test that the /orchestration skill correctly generates and executes adversarial feedback
  loops (creator->critic->revision cycles) as designed in EN-307.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "ps-validator"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-306"
tags:
  - "epic-002"
  - "feat-004"
effort: null
acceptance_criteria: |
  - orch-planner automatically generates creator->critic->revision cycles
  - orch-tracker correctly tracks adversarial quality scores
  - orch-synthesizer includes adversarial synthesis in outputs
  - Adversarial feedback loops execute correctly end-to-end
  - Quality gates at sync barriers enforce adversarial review completion
due_date: null
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Test that the /orchestration skill correctly generates and executes adversarial feedback loops (creator->critic->revision cycles) as designed in EN-307. Verify that orch-planner automatically embeds adversarial cycles, orch-tracker tracks quality scores, and orch-synthesizer produces adversarial synthesis outputs.

### Acceptance Criteria

- [ ] orch-planner automatically generates creator->critic->revision cycles
- [ ] orch-tracker correctly tracks adversarial quality scores
- [ ] orch-synthesizer includes adversarial synthesis in outputs
- [ ] Adversarial feedback loops execute correctly end-to-end
- [ ] Quality gates at sync barriers enforce adversarial review completion

### Implementation Notes

Depends on TASK-001 (test plan). Uses ps-validator agent. Can run in parallel with TASK-002 and TASK-003. Feeds into TASK-005 (cross-platform testing).

### Related Items

- Parent: [EN-306](../EN-306-integration-testing-validation.md)
- Depends on: [TASK-001](./TASK-001-create-integration-test-plan.md)
- Feeds into: [TASK-005](./TASK-005-cross-platform-testing.md)

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
