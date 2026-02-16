# TASK-001: Restore original rule file content from git history

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** RESEARCH
> **Agents:** --
> **Created:** 2026-02-16
> **Parent:** EN-902

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description, acceptance criteria, implementation notes |
| [Time Tracking](#time-tracking) | Effort estimates |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Content

### Description

Use `git show` to recover the full content of all 10 `.context/rules/` files from the commit immediately before EN-702 optimization (~314993a^ or the commit before the EN-702 changes). Save recovered content as reference files in a temporary working directory for guide creation.

### Acceptance Criteria

- [ ] All 10 original files recovered
- [ ] Content saved for reference
- [ ] Token count of originals measured

### Implementation Notes

Use `git show <commit>:<path>` for each of the 10 `.context/rules/` files. Store recovered content in EN-902 working directory or a temporary location for comparison during TASK-002 through TASK-006. Measure approximate token count of each original file to understand the scope of deleted content.

### Related Items

- Parent: [EN-902: Companion Guide Files](EN-902-companion-guides.md)
- Blocks: TASK-002, TASK-003, TASK-004, TASK-005, TASK-006 (provides source content)

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
| Recovered original rule files | Reference | --- |
| Token count measurements | Analysis | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Task created from EN-902 technical approach. |
