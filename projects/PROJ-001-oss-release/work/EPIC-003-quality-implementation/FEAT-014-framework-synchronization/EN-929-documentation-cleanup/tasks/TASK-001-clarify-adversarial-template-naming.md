# TASK-001: Clarify adversarial template naming in SKILL.md Dependencies section

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
title: "Clarify adversarial template naming in SKILL.md Dependencies section"
description: |
  Update the adversary SKILL.md Dependencies section to clarify that templates
  are static files (not generated), and document the naming and versioning
  conventions used for adversarial strategy templates.
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
  - SKILL.md Dependencies section clarifies templates are static files
  - Naming convention for template files is documented
  - Versioning approach for templates is explained
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Update the adversary SKILL.md Dependencies section to clarify that adversarial strategy templates are static files, not generated output. The current documentation may give the impression that templates are dynamically created. Add explicit naming convention guidance and explain the versioning approach used for template files.

### Acceptance Criteria

- [ ] SKILL.md Dependencies section clarifies templates are static files, not generated
- [ ] Naming convention for adversarial template files is documented
- [ ] Versioning approach for templates is explained

### Implementation Notes

- Use MEDIUM-tier language (SHOULD/RECOMMENDED) for naming conventions
- Ensure changes are consistent with the existing SKILL.md formatting style
- This task can run in parallel with all other EN-929 tasks

### Related Items

- Parent: [EN-929: Minor Documentation Cleanup](../EN-929-documentation-cleanup.md)
- Parallel: [TASK-002](./TASK-002-document-agent-directory-distinction.md), [TASK-003](./TASK-003-add-orchestration-reference.md), [TASK-004](./TASK-004-verify-h16-rule-index.md), [TASK-005](./TASK-005-improve-adversary-usage-guidance.md)

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
