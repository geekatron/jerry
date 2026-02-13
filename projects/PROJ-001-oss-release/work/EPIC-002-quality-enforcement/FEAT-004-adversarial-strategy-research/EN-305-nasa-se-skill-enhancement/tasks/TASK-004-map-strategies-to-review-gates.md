# TASK-004: Map Strategies to SE Review Gates

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
title: "Map strategies to SE review gates (SRR, PDR, CDR, TRR, FRR)"
description: |
  Map the 10 adversarial strategies to the 5 SE review gates (SRR, PDR, CDR, TRR, FRR),
  identifying which strategies are most effective at each gate based on the gate's specific
  concerns.
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
  - All 10 strategies are mapped to appropriate SE review gates
  - Each mapping includes rationale for why the strategy fits the gate
  - At least 2 strategies are recommended per review gate
  - Mapping identifies which strategies are contraindicated at specific gates
  - Mapping is documented in a matrix format for easy reference
due_date: null
activity: DESIGN
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Map the 10 adversarial strategies to the 5 SE review gates (SRR, PDR, CDR, TRR, FRR), identifying which strategies are most effective at each gate. Each review gate has different concerns (requirements completeness at SRR, design integrity at PDR/CDR, test coverage at TRR, readiness at FRR) and needs strategies specifically tailored to those concerns.

### Acceptance Criteria

- [ ] All 10 strategies are mapped to appropriate SE review gates
- [ ] Each mapping includes rationale for why the strategy fits the gate
- [ ] At least 2 strategies are recommended per review gate
- [ ] Mapping identifies which strategies are contraindicated at specific gates
- [ ] Mapping is documented in a matrix format for easy reference

### Implementation Notes

Depends on TASK-001 (requirements). Uses nse-architecture agent. Feeds into TASK-005 (nse-verification spec) and TASK-006 (nse-reviewer spec).

### Related Items

- Parent: [EN-305](../EN-305-nasa-se-skill-enhancement.md)
- Depends on: [TASK-001](./TASK-001-define-nse-skill-requirements.md)
- Feeds into: [TASK-005](./TASK-005-implement-nse-verification-spec.md), [TASK-006](./TASK-006-implement-nse-reviewer-spec.md)

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
