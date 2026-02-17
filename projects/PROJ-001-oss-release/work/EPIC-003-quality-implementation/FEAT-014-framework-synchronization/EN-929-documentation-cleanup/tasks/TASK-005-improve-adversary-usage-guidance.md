# TASK-005: Improve "When NOT to Use" guidance in adversary SKILL.md

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
id: "TASK-005"
work_type: TASK
title: "Improve 'When NOT to Use' guidance in adversary SKILL.md"
description: |
  Expand the adversary SKILL.md "When to Use" and "When NOT to Use" sections
  to provide clearer guidance on adv-executor vs ps-critic selection, helping
  agents choose the correct review mechanism for their context.
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
  - Adversary SKILL.md "When to Use" section is comprehensive
  - Clear distinction between adv-executor and ps-critic use cases
  - Guidance helps agents select the correct review mechanism
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Expand the adversary SKILL.md "When to Use" and "When NOT to Use" sections to provide clearer guidance on when to use the adv-executor (adversarial review) versus ps-critic (standard critique). The current documentation may not give agents enough information to select the correct review mechanism for their context, leading to either over-application of adversarial review on routine work or under-application on work that warrants it.

### Acceptance Criteria

- [ ] Adversary SKILL.md "When to Use" section covers all appropriate use cases
- [ ] Clear decision guidance for adv-executor vs ps-critic selection is provided
- [ ] "When NOT to Use" section identifies scenarios where adversarial review adds unnecessary overhead

### Implementation Notes

- Reference criticality levels (C1-C4) to ground the guidance in existing framework concepts
- Keep guidance actionable with concrete examples or decision criteria
- This task can run in parallel with all other EN-929 tasks

### Related Items

- Parent: [EN-929: Minor Documentation Cleanup](../EN-929-documentation-cleanup.md)
- Parallel: [TASK-001](./TASK-001-clarify-adversarial-template-naming.md), [TASK-002](./TASK-002-document-agent-directory-distinction.md), [TASK-003](./TASK-003-add-orchestration-reference.md), [TASK-004](./TASK-004-verify-h16-rule-index.md)

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
