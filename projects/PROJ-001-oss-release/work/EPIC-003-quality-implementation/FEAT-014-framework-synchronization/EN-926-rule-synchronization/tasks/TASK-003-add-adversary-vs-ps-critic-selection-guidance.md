# TASK-003: Add Adversary vs ps-critic Selection Guidance to Adversary SKILL.md

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
id: "TASK-003"
work_type: TASK
title: "Add adversary vs ps-critic selection guidance to adversary SKILL.md"
description: |
  Add when-to-use guidance to the adversary SKILL.md that distinguishes the /adversary
  skill from the ps-critic agent in the problem-solving skill. Clarify when each should
  be used, including criteria for selection based on criticality level, strategy needs,
  and review type.
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
  - Adversary SKILL.md includes when-to-use section distinguishing from ps-critic
  - Selection criteria cover criticality level, strategy needs, and review type
  - Guidance is actionable and unambiguous
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Add when-to-use guidance to the adversary SKILL.md that distinguishes the /adversary skill from the ps-critic agent in the problem-solving skill. Clarify when each should be used, including criteria for selection based on criticality level, strategy needs, and review type.

### Acceptance Criteria

- [ ] Adversary SKILL.md includes when-to-use section distinguishing from ps-critic
- [ ] Selection criteria cover criticality level, strategy needs, and review type
- [ ] Guidance is actionable and unambiguous

### Implementation Notes

Modifies `skills/adversary/SKILL.md`. The key distinction: ps-critic provides general critique within the problem-solving workflow; /adversary provides formal strategy-based quality reviews aligned with the quality enforcement framework (S-001 through S-014).

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
