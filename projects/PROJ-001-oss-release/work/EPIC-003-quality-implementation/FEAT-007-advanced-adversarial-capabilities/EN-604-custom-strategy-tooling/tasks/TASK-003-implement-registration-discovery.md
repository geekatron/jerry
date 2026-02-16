# TASK-003: Implement registration/discovery mechanism

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
title: "Implement registration/discovery mechanism"
description: |
  Build the filesystem-based mechanism for registering and discovering
  custom adversarial strategies. Implement registration, discovery with
  filtering, and deregistration commands.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "ps-architect"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-604"
tags:
  - "epic-002"
  - "feat-007"
effort: null
acceptance_criteria: |
  - Registration command validates and adds strategy to catalog
  - Discovery command lists strategies with filtering by tag, domain, author
  - Deregistration command removes strategy from catalog
  - Strategy catalog is filesystem-based with one strategy per file (NFC-1)
  - Unit test coverage >= 90% for registration and discovery components
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Build the filesystem-based mechanism for registering and discovering custom adversarial strategies. Implement a registration command that validates strategy definitions against the schema and copies them to the catalog, a discovery command that lists available strategies with filtering by tag, domain, and author, and a deregistration command for removing obsolete strategies. The catalog must use one strategy per file in a strategies directory.

### Acceptance Criteria

- [ ] Registration command validates and adds strategy to catalog
- [ ] Discovery command lists strategies with filtering by tag, domain, author
- [ ] Deregistration command removes strategy from catalog
- [ ] Strategy catalog is filesystem-based with one strategy per file (NFC-1)
- [ ] Unit test coverage >= 90% for registration and discovery components

### Implementation Notes

- Depends on TASK-002 schema design for validation rules
- Must complete before TASK-004 integration testing
- Filesystem-based storage -- no database dependency
- Follow hexagonal architecture for the registration/discovery service

### Related Items

- Parent: [EN-604: Custom Strategy Creation Tooling](../EN-604-custom-strategy-tooling.md)
- Depends on: [TASK-002](./TASK-002-design-strategy-definition-schema.md)
- Downstream: [TASK-004](./TASK-004-integration-testing-selector-metrics.md) (depends on this task)

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
