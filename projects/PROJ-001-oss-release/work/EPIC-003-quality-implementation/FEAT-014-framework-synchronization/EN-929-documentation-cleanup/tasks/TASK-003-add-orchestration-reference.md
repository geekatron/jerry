# TASK-003: Add orchestration pattern reference to architecture-standards.md

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
title: "Add orchestration pattern reference to architecture-standards.md"
description: |
  Add a brief paragraph or subsection to architecture-standards.md that
  references orchestration patterns and their relationship to the hexagonal
  architecture. This bridges the gap between architecture and orchestration
  skill documentation.
classification: ENABLER
status: BACKLOG
resolution: null
priority: LOW
assignee: "ps-architect"
created_by: "Claude"
created_at: "2026-02-17"
updated_at: "2026-02-17"
parent_id: "EN-929"
tags:
  - "epic-003"
  - "feat-014"
  - "documentation"
effort: null
acceptance_criteria: |
  - architecture-standards.md contains orchestration pattern reference
  - Reference is consistent with existing document structure and formatting
  - Cross-reference to orchestration skill documentation is included
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Add a brief paragraph or subsection to architecture-standards.md that references orchestration patterns and their relationship to the hexagonal architecture. Currently, architecture-standards.md covers hexagonal layers, CQRS, and event sourcing but does not mention orchestration patterns, creating a gap between the architecture documentation and the orchestration skill. Adding this cross-reference improves discoverability.

### Acceptance Criteria

- [ ] architecture-standards.md contains an orchestration pattern reference paragraph or subsection
- [ ] Reference is consistent with existing document structure and formatting
- [ ] Cross-reference points to the orchestration skill documentation

### Implementation Notes

- Add to the Guidance (SOFT) section or as a new MEDIUM-tier standard
- Keep the addition concise -- a paragraph with a pointer, not a full orchestration guide
- This task can run in parallel with all other EN-929 tasks

### Related Items

- Parent: [EN-929: Minor Documentation Cleanup](../EN-929-documentation-cleanup.md)
- Parallel: [TASK-001](./TASK-001-clarify-adversarial-template-naming.md), [TASK-002](./TASK-002-document-agent-directory-distinction.md), [TASK-004](./TASK-004-verify-h16-rule-index.md), [TASK-005](./TASK-005-improve-adversary-usage-guidance.md)

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
