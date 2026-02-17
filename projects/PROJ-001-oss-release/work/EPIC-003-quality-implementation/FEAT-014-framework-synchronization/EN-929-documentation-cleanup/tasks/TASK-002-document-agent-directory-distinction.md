# TASK-002: Document agent vs template file distinction in PS and NSE agent dirs

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
title: "Document agent vs template file distinction in PS and NSE agent dirs"
description: |
  Add brief README files to the problem-solving and nasa-se agent directories
  to distinguish agent definition files from template and extension files that
  coexist in those directories.
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
  - Agent directories contain README or equivalent distinguishing file types
  - README clearly identifies which files are agent definitions vs support files
  - Documentation follows H-23/H-24 navigation requirements if over 30 lines
due_date: null
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Add brief README files to the problem-solving (PS) and nasa-se (NSE) agent directories to clearly distinguish agent definition files from template files, extension files, and other support artifacts that coexist in those directories. This reduces confusion for users browsing the agent directories and helps agents understand which files to load.

### Acceptance Criteria

- [ ] Agent directories contain README or equivalent distinguishing file types
- [ ] README clearly identifies which files are agent definitions vs support/template files
- [ ] Documentation follows H-23/H-24 navigation requirements if over 30 lines

### Implementation Notes

- Keep READMEs concise; under 30 lines avoids H-23 navigation table requirement
- Use a simple file listing with brief descriptions for each file type
- This task can run in parallel with all other EN-929 tasks

### Related Items

- Parent: [EN-929: Minor Documentation Cleanup](../EN-929-documentation-cleanup.md)
- Parallel: [TASK-001](./TASK-001-clarify-adversarial-template-naming.md), [TASK-003](./TASK-003-add-orchestration-reference.md), [TASK-004](./TASK-004-verify-h16-rule-index.md), [TASK-005](./TASK-005-improve-adversary-usage-guidance.md)

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
