# TASK-001: Design metrics collection architecture (events, collectors, storage)

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
title: "Design metrics collection architecture (events, collectors, storage)"
description: |
  Design the metrics collection infrastructure following hexagonal architecture
  principles. Define domain events emitted by adversarial review processes,
  a metrics collector port with filesystem adapter, and an event aggregation
  pipeline.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "ps-architect"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-605"
tags:
  - "epic-002"
  - "feat-007"
effort: null
acceptance_criteria: |
  - Metrics collection captures ReviewStarted, ReviewCompleted, and DefectFound events
  - Metrics collector defined as application-layer port with filesystem infrastructure adapter
  - Event aggregation pipeline computes per-strategy metrics from raw events
  - Storage format uses filesystem-based JSON files (no database dependency, NFC-1)
  - Architecture follows hexagonal principles (domain events, ports, adapters, NFC-2)
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Design the metrics collection infrastructure following hexagonal architecture principles. Define domain events emitted by adversarial review processes (ReviewStarted, ReviewCompleted, DefectFound), a metrics collector port at the application layer with a filesystem adapter at the infrastructure layer, and an event aggregation pipeline that computes per-strategy metrics from raw events. Storage format uses JSON files in a metrics directory, one file per strategy per time period.

### Acceptance Criteria

- [ ] Metrics collection captures ReviewStarted, ReviewCompleted, and DefectFound events
- [ ] Metrics collector defined as application-layer port with filesystem infrastructure adapter
- [ ] Event aggregation pipeline computes per-strategy metrics from raw events
- [ ] Storage format uses filesystem-based JSON files (no database dependency, NFC-1)
- [ ] Architecture follows hexagonal principles (domain events, ports, adapters, NFC-2)

### Implementation Notes

- Follow hexagonal architecture patterns from `.claude/rules/architecture-standards.md`
- Domain events should be immutable value objects per coding standards
- Can execute in parallel with TASK-002 and TASK-003
- Metrics collection must add < 100ms latency to review completion (NFC-7)

### Related Items

- Parent: [EN-605: Effectiveness Metrics Dashboard & A/B Testing Framework](../EN-605-metrics-and-ab-testing.md)
- Parallel: [TASK-002](./TASK-002-define-effectiveness-scoring.md), [TASK-003](./TASK-003-implement-ab-testing-framework.md)
- Downstream: [TASK-004](./TASK-004-qa-testing-metrics-ab.md) (depends on this task)

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
