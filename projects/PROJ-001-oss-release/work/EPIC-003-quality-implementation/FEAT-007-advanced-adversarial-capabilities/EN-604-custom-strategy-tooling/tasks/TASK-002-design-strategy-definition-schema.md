# TASK-002: Design strategy definition schema (YAML/JSON specification)

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
title: "Design strategy definition schema (YAML/JSON specification)"
description: |
  Design the strategy definition schema as a YAML/JSON specification based
  on the requirements from TASK-001. Define required fields, optional fields,
  validation constraints, and extensibility via custom metadata fields.
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
  - Strategy definition schema includes all required fields (name, description, steps, context, outcomes)
  - Schema validation catches missing required fields with clear error messages
  - Schema validation catches malformed values (empty strings, invalid references)
  - Schema supports extensibility via custom metadata fields (NFC-2)
  - Schema specification persisted to filesystem under EN-604 directory
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Design the strategy definition schema as a YAML/JSON specification based on the requirements from TASK-001. Define required fields (name, description, steps as ordered list, applicability context, expected outcomes), optional fields (author, version, tags, related strategies, effectiveness baseline), validation constraints (non-empty fields, step count limits, valid context references), and extensibility via custom metadata fields for domain-specific annotations.

### Acceptance Criteria

- [ ] Strategy definition schema includes all required fields (name, description, steps, context, outcomes)
- [ ] Schema validation catches missing required fields with clear error messages
- [ ] Schema validation catches malformed values (empty strings, invalid references)
- [ ] Schema supports extensibility via custom metadata fields (NFC-2)
- [ ] Schema specification persisted to filesystem under EN-604 directory

### Implementation Notes

- Depends on TASK-001 requirements for the authoritative specification
- Must complete before TASK-003 registration/discovery implementation
- Balance schema comprehensiveness with usability for teams
- Consider backward compatibility for future schema evolution

### Related Items

- Parent: [EN-604: Custom Strategy Creation Tooling](../EN-604-custom-strategy-tooling.md)
- Depends on: [TASK-001](./TASK-001-define-requirements-strategy-schema.md)
- Downstream: [TASK-003](./TASK-003-implement-registration-discovery.md) (depends on this task)

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
