# TASK-001: Add /adversary Triggers to mandatory-skill-usage.md H-22

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
id: "TASK-001"
work_type: TASK
title: "Add /adversary triggers to mandatory-skill-usage.md H-22"
description: |
  Update mandatory-skill-usage.md to include /adversary in the H-22 trigger map. Add
  appropriate trigger keywords (quality review, critique, adversarial, tournament, red team,
  devil's advocate) and update the H-22 rule text to include adversarial quality reviews.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "ps-architect"
created_by: "Claude"
created_at: "2026-02-17"
updated_at: "2026-02-17"
parent_id: "EN-926"
tags:
  - "epic-003"
  - "feat-014"
  - "rule-sync"
effort: null
acceptance_criteria: |
  - /adversary added to trigger map with keywords: quality review, critique, adversarial, tournament, red team, devil's advocate
  - H-22 rule text updated to mention adversarial quality reviews
  - Existing triggers for /problem-solving, /nasa-se, /orchestration unchanged
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Update mandatory-skill-usage.md to include /adversary in the H-22 trigger map. Add appropriate trigger keywords (quality review, critique, adversarial, tournament, red team, devil's advocate) and update the H-22 rule text to include adversarial quality reviews.

### Acceptance Criteria

- [ ] /adversary added to trigger map with appropriate keywords
- [ ] H-22 rule text updated to mention adversarial quality reviews
- [ ] Existing triggers for /problem-solving, /nasa-se, /orchestration unchanged

### Implementation Notes

Modifies `.context/rules/mandatory-skill-usage.md`. This is an AE-002 auto-C3 change (touches `.context/rules/`).

### Related Items

- Parent: [EN-926](../EN-926-rule-synchronization.md)

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
