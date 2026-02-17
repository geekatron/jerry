# TASK-002: Audit Existing .claude/rules/ Files for Enforcement Gaps

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
id: "TASK-002"
work_type: TASK
title: "Audit existing .claude/rules/ files for enforcement gaps"
description: |
  Audit all existing .claude/rules/ files to identify enforcement gaps where Claude could
  bypass quality requirements. Catalog each gap with severity, bypass mechanism, and
  recommended fix. Produce a gap analysis report that informs the tiered enforcement
  strategy design.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "ps-investigator"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-404"
tags:
  - "epic-002"
  - "feat-005"
  - "enforcement"
effort: null
acceptance_criteria: |
  - All .claude/rules/ files audited systematically
  - Enforcement gaps identified with bypass mechanism descriptions
  - Each gap rated by severity (critical, high, medium, low)
  - Recommended fixes documented for each identified gap
  - Gap analysis report persisted to filesystem
due_date: null
activity: RESEARCH
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Audit all existing .claude/rules/ files to identify enforcement gaps where Claude could bypass quality requirements. Catalog each gap with severity, bypass mechanism, and recommended fix. Produce a gap analysis report that informs the tiered enforcement strategy design.

### Acceptance Criteria

- [ ] All .claude/rules/ files audited systematically
- [ ] Enforcement gaps identified with bypass mechanism descriptions
- [ ] Each gap rated by severity (critical, high, medium, low)
- [ ] Recommended fixes documented for each identified gap
- [ ] Gap analysis report persisted to filesystem

### Implementation Notes

Depends on TASK-001 (requirements). Outputs feed TASK-003 (tiered enforcement design).

### Related Items

- Parent: [EN-404](../EN-404-rule-based-enforcement.md)
- Depends on: [TASK-001](./TASK-001-define-rule-enforcement-requirements.md)
- Feeds into: [TASK-003](./TASK-003-design-tiered-enforcement.md)

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
