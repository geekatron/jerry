# TASK-007: Update NSE SKILL.md with Adversarial Capabilities

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
id: "TASK-007"
work_type: TASK
title: "Update NSE SKILL.md with adversarial capabilities"
description: |
  Update the /nasa-se SKILL.md to document all adversarial capabilities added to the skill,
  including adversarial modes for nse-verification and nse-reviewer, review gate mappings,
  and usage examples.
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
  - NSE SKILL.md documents all adversarial capabilities for nse-verification and nse-reviewer
  - Review gate mapping (strategy to SRR/PDR/CDR/TRR/FRR) is included
  - Usage examples are provided for each adversarial mode
  - Documentation follows the Triple-Lens format (L0/L1/L2)
  - Documentation is consistent with agent spec definitions
due_date: null
activity: DOCUMENTATION
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Update the /nasa-se SKILL.md to document all adversarial capabilities added to the skill. Include adversarial modes for nse-verification and nse-reviewer agents, review gate mappings showing which strategies apply at which gates, and usage examples for invoking adversarial modes during SE reviews.

### Acceptance Criteria

- [ ] NSE SKILL.md documents all adversarial capabilities for nse-verification and nse-reviewer
- [ ] Review gate mapping (strategy to SRR/PDR/CDR/TRR/FRR) is included
- [ ] Usage examples are provided for each adversarial mode
- [ ] Documentation follows the Triple-Lens format (L0/L1/L2)
- [ ] Documentation is consistent with agent spec definitions

### Implementation Notes

Depends on TASK-005 (nse-verification spec) and TASK-006 (nse-reviewer spec). Uses nse-architecture agent. Feeds into TASK-008 (adversarial review) and TASK-009 (technical review).

### Related Items

- Parent: [EN-305](../EN-305-nasa-se-skill-enhancement.md)
- Depends on: [TASK-005](./TASK-005-implement-nse-verification-spec.md), [TASK-006](./TASK-006-implement-nse-reviewer-spec.md)
- Feeds into: [TASK-008](./TASK-008-adversarial-review.md), [TASK-009](./TASK-009-technical-review.md)

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
