# TASK-008: Adversarial Review (Devil's Advocate + Steelman)

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
id: "TASK-008"
work_type: TASK
title: "Adversarial review (ps-critic with Devil's Advocate + Steelman)"
description: |
  Apply Devil's Advocate and Steelman adversarial strategies to the /nasa-se skill changes.
  Devil's Advocate challenges assumptions and design decisions. Steelman constructs the
  strongest possible counter-arguments to validate robustness.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "ps-critic"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-305"
tags:
  - "epic-002"
  - "feat-004"
effort: null
acceptance_criteria: |
  - Devil's Advocate review challenges assumptions with documented findings
  - Steelman review constructs strongest counter-arguments to validate robustness
  - Each finding includes severity, description, and recommended action
  - All critical findings are resolved or escalated
  - Review passes with no critical findings remaining
due_date: null
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Apply Devil's Advocate and Steelman adversarial strategies to the /nasa-se skill changes. Devil's Advocate challenges assumptions and design decisions in the adversarial integration. Steelman constructs the strongest possible counter-arguments to validate the robustness of the review gate mappings and agent enhancements.

### Acceptance Criteria

- [ ] Devil's Advocate review challenges assumptions with documented findings
- [ ] Steelman review constructs strongest counter-arguments to validate robustness
- [ ] Each finding includes severity, description, and recommended action
- [ ] All critical findings are resolved or escalated
- [ ] Review passes with no critical findings remaining

### Implementation Notes

Depends on TASK-007 (SKILL.md update). Uses ps-critic agent with Devil's Advocate and Steelman modes. Feeds into TASK-009 (technical review).

### Related Items

- Parent: [EN-305](../EN-305-nasa-se-skill-enhancement.md)
- Depends on: [TASK-007](./TASK-007-update-nse-skill-md.md)
- Feeds into: [TASK-009](./TASK-009-technical-review.md)

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
