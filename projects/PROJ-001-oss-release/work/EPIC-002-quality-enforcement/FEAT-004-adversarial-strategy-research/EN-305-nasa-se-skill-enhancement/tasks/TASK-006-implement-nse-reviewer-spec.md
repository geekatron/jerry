# TASK-006: Implement nse-reviewer Agent Spec Updates

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
title: "Implement nse-reviewer agent spec updates"
description: |
  Update the nse-reviewer agent specification with adversarial critique modes, prompt templates,
  and workflows based on the design from TASK-003.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "nse-architecture"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-305"
tags:
  - "epic-002"
  - "feat-004"
effort: null
acceptance_criteria: |
  - nse-reviewer agent spec includes adversarial critique modes
  - Each mode has a complete prompt template and evaluation criteria
  - Modes are tagged with applicable SE review gates
  - Agent spec changes are backward-compatible with existing nse-reviewer behavior
  - Implementation matches the design from TASK-003
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Update the nse-reviewer agent specification with adversarial critique modes, prompt templates, and workflows based on the design from TASK-003. Implement the adversarial review capabilities that enable technical reviews to incorporate structured adversarial critiques at each relevant SE review gate.

### Acceptance Criteria

- [ ] nse-reviewer agent spec includes adversarial critique modes
- [ ] Each mode has a complete prompt template and evaluation criteria
- [ ] Modes are tagged with applicable SE review gates
- [ ] Agent spec changes are backward-compatible with existing nse-reviewer behavior
- [ ] Implementation matches the design from TASK-003

### Implementation Notes

Depends on TASK-003 (nse-reviewer design) and TASK-004 (review gate mapping). Uses nse-architecture agent. Can run in parallel with TASK-005 (nse-verification spec). Feeds into TASK-007 (SKILL.md update).

### Related Items

- Parent: [EN-305](../EN-305-nasa-se-skill-enhancement.md)
- Depends on: [TASK-003](./TASK-003-design-nse-reviewer-integration.md), [TASK-004](./TASK-004-map-strategies-to-review-gates.md)
- Feeds into: [TASK-007](./TASK-007-update-nse-skill-md.md)

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
