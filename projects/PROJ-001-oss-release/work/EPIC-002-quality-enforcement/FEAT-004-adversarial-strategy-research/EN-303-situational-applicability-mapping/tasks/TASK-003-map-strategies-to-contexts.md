# TASK-003: Map Each Strategy to Contexts with Use/Avoid Guidance

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
title: "Map each strategy to contexts with use/avoid guidance"
description: |
  For each of the 10 selected strategies, create a complete applicability profile defining
  recommended contexts, contraindicated contexts, complementary pairings, preconditions,
  and expected outcomes.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "ps-architect"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-303"
tags:
  - "epic-002"
  - "feat-004"
effort: null
acceptance_criteria: |
  - All 10 selected strategies have complete applicability profiles
  - Each profile includes: when to use, when to avoid, pairings, preconditions, outcomes
  - Profiles reference the context taxonomy dimensions from TASK-001
  - Complementary and conflicting strategy pairings are explicitly identified
  - Profiles are structured for consumption by the decision tree in TASK-004
due_date: null
activity: DESIGN
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

For each of the 10 selected strategies (from EN-302), create a complete applicability profile. Each profile defines recommended contexts (when to use), contraindicated contexts (when to avoid), complementary pairings (strategies that work well together), preconditions (what must be true before applying), and expected outcomes (what the strategy produces).

### Acceptance Criteria

- [ ] All 10 selected strategies have complete applicability profiles
- [ ] Each profile includes: when to use, when to avoid, pairings, preconditions, outcomes
- [ ] Profiles reference the context taxonomy dimensions from TASK-001
- [ ] Complementary and conflicting strategy pairings are explicitly identified
- [ ] Profiles are structured for consumption by the decision tree in TASK-004

### Implementation Notes

Depends on TASK-001 (taxonomy) and TASK-002 (requirements). Core mapping work. Feeds into TASK-004 (decision tree).

### Related Items

- Parent: [EN-303](../EN-303-situational-applicability-mapping.md)
- Depends on: [TASK-001](./TASK-001-define-applicability-dimensions.md), [TASK-002](./TASK-002-define-mapping-requirements.md)
- Feeds into: [TASK-004](./TASK-004-create-strategy-decision-tree.md)

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
