# TASK-001: Update INSTALLATION.md

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Content](#content) | Description and content to add |
| [Time Tracking](#time-tracking) | Effort metrics |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-001"
work_type: TASK
title: "Update INSTALLATION.md"
description: |
  Update INSTALLATION.md to explain the new CLAUDE.md structure and
  tiered context loading architecture.

classification: ENABLER
status: BACKLOG
resolution: null
priority: MEDIUM
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-205"
tags:
  - enabler
  - documentation
  - installation

effort: 1
acceptance_criteria: |
  - INSTALLATION.md updated
  - Tiered loading explained
  - Skill invocation mentioned
  - Clear for new users
due_date: null

activity: DOCUMENTATION
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

Update the INSTALLATION.md to include information about the new tiered context loading architecture and how to navigate the Jerry framework.

### Content to Add

1. **Context Architecture Overview**
   - Tier 1: CLAUDE.md (always loaded)
   - Tier 2: .claude/rules/ (auto-loaded)
   - Tier 3: Skills (on-demand)
   - Tier 4: Reference docs (explicit access)

2. **Skill Invocation**
   - How to use `/worktracker`, `/problem-solving`, etc.
   - When to invoke skills

3. **Navigation Guide**
   - Where to find what

### Acceptance Criteria

- [ ] Tiered architecture explained
- [ ] Skill invocation documented
- [ ] Navigation clear
- [ ] Suitable for new users

### Related Items

- Parent: [EN-205: Documentation Update](./EN-205-documentation-update.md)
- Target: docs/INSTALLATION.md

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 1 hour |
| Remaining Work | 1 hour |
| Time Spent | 0 hours |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
