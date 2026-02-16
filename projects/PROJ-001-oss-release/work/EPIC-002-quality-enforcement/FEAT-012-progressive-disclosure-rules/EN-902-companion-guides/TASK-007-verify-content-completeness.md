# TASK-007: Verify all original content exists in guide files

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** REVIEW
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

Compare the restored git history content (TASK-001) against the created guide files (TASK-002 through TASK-006). Create a coverage matrix: for each section of original content, identify which guide file contains it. Flag any gaps. Ensure guides contain ALL original content plus new additions.

### Acceptance Criteria

- [ ] Coverage matrix created
- [ ] 100% of original content mapped to guide files
- [ ] No gaps identified (or gaps documented with justification)
- [ ] Report with file-by-file comparison

### Implementation Notes

Create a structured comparison document. For each of the 10 original rule files, list every section heading and content block. Map each block to its destination guide file. Identify any content that was not restored. Verify that guide files contain additive content beyond what was in the originals (TC-5 requirement).

### Related Items

- Parent: [EN-902: Companion Guide Files](EN-902-companion-guides.md)
- Depends on: TASK-001, TASK-002, TASK-003, TASK-004, TASK-005, TASK-006 (all must be complete)

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
| Coverage matrix report | Analysis | --- |
| File-by-file comparison | Analysis | --- |
| Gap analysis (if any) | Analysis | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Task created from EN-902 technical approach. |
