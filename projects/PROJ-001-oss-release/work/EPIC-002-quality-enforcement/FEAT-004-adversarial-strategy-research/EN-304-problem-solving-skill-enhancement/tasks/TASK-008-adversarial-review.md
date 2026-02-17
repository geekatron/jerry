# TASK-008: Adversarial Review (Red Team + Blue Team)

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
title: "Adversarial review (Red Team + Blue Team)"
description: |
  Apply Red Team and Blue Team adversarial strategies to the /problem-solving skill changes
  themselves. Red Team challenges fundamental design decisions. Blue Team stress-tests the
  implementation for gaps, inconsistencies, and edge cases.
classification: ENABLER
status: BACKLOG
resolution: null
priority: CRITICAL
assignee: "ps-critic"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-304"
tags:
  - "epic-002"
  - "feat-004"
effort: null
acceptance_criteria: |
  - Red Team review challenges fundamental design decisions with documented findings
  - Blue Team review identifies implementation gaps and edge cases
  - Each finding includes severity, description, and recommended action
  - All critical findings are resolved or escalated
  - Adversarial review feedback is documented for verification traceability
due_date: null
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Apply Red Team and Blue Team adversarial strategies to the /problem-solving skill changes themselves. Red Team challenges the fundamental design decisions (are the mode definitions correct? is the invocation protocol sound?). Blue Team stress-tests the implementation for gaps, inconsistencies, and edge cases in the mode specifications and documentation.

### Acceptance Criteria

- [ ] Red Team review challenges fundamental design decisions with documented findings
- [ ] Blue Team review identifies implementation gaps and edge cases
- [ ] Each finding includes severity, description, and recommended action
- [ ] All critical findings are resolved or escalated
- [ ] Adversarial review feedback is documented for verification traceability

### Implementation Notes

Depends on TASK-007 (code review). Uses ps-critic agent with Red Team and Blue Team modes. Feeds into TASK-009 (requirements verification).

### Related Items

- Parent: [EN-304](../EN-304-problem-solving-skill-enhancement.md)
- Depends on: [TASK-007](./TASK-007-code-review.md)
- Feeds into: [TASK-009](./TASK-009-verification-against-requirements.md)

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
