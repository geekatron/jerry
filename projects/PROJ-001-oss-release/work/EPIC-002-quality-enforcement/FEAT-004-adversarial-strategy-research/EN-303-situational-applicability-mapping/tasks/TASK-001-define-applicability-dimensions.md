# TASK-001: Define Applicability Dimensions and Context Taxonomy

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
title: "Define applicability dimensions and context taxonomy"
description: |
  Define the dimensions that determine strategy applicability and construct a context
  taxonomy. Dimensions include review target type, review phase, risk level, artifact
  maturity, and team composition.
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
  - At least 4 applicability dimensions are defined with clear value ranges
  - Each dimension has an enumerated set of possible values
  - Context taxonomy is structured for use in decision tree construction (TASK-004)
  - Dimensions cover the full range of Jerry's operational contexts
  - Taxonomy is documented in a format consumable by downstream tasks
due_date: null
activity: DESIGN
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Define the dimensions that determine strategy applicability and construct a context taxonomy. Dimensions include review target type (code, architecture, requirements, research), review phase (early exploration, design, implementation, validation), risk level (critical, high, medium, low), artifact maturity (draft, reviewed, approved), and team composition (single agent, multi-agent, human-in-loop).

### Acceptance Criteria

- [ ] At least 4 applicability dimensions are defined with clear value ranges
- [ ] Each dimension has an enumerated set of possible values
- [ ] Context taxonomy is structured for use in decision tree construction (TASK-004)
- [ ] Dimensions cover the full range of Jerry's operational contexts
- [ ] Taxonomy is documented in a format consumable by downstream tasks

### Implementation Notes

First of two parallel inputs to TASK-003 (mapping). Can run in parallel with TASK-002 (requirements).

### Related Items

- Parent: [EN-303](../EN-303-situational-applicability-mapping.md)
- Feeds into: [TASK-003](./TASK-003-map-strategies-to-contexts.md)

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
