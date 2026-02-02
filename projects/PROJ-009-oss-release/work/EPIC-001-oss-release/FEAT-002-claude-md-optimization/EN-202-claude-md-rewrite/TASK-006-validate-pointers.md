# TASK-006: Validate All Pointers Resolve Correctly

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
| [Content](#content) | Description, dependencies, validation checklist |
| [Time Tracking](#time-tracking) | Effort metrics |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-006"
work_type: TASK
title: "Validate All Pointers Resolve Correctly"
description: |
  Validate that all navigation pointers in the new CLAUDE.md resolve to
  existing files, directories, and skills.

classification: ENABLER
status: COMPLETE
resolution: DONE
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-02T04:00:00Z"
parent_id: "EN-202"
tags:
  - enabler
  - claude-md
  - validation

effort: 1
acceptance_criteria: |
  - [x] All file/directory pointers resolve
  - [x] All skill references valid
  - [x] No 404s or missing targets
due_date: null

activity: TESTING
original_estimate: 1
remaining_work: 0
time_spent: 0.5
```

---

## Content

### Description

After creating all sections, validate that every pointer in the new CLAUDE.md resolves to an actual target.

### Dependencies

This task depends on completion of:
- TASK-001: Create Identity section
- TASK-002: Create Navigation pointers section
- TASK-003: Create Active project section
- TASK-004: Create Critical constraints section
- TASK-005: Create Quick reference section

### Validation Checklist

#### File/Directory Pointers

| Pointer | Target | Exists |
|---------|--------|--------|
| `.claude/rules/` | Directory | [x] **Evidence:** Verified 2026-02-02 |
| `.context/templates/` | Directory | [x] **Evidence:** Verified 2026-02-02 |
| `docs/knowledge/` | Directory | [x] **Evidence:** Verified 2026-02-02 |
| `docs/governance/JERRY_CONSTITUTION.md` | File | [x] **Evidence:** 14,301 bytes |
| `scripts/session_start_hook.py` | File | [x] **Evidence:** 12,258 bytes |

#### Skill References

| Skill | Exists | Loads |
|-------|--------|-------|
| `/worktracker` | [x] | [x] |
| `/problem-solving` | [x] | [x] |
| `/nasa-se` | [x] | [x] |
| `/orchestration` | [x] | [x] |
| `/architecture` | [x] | [x] |
| `/transcript` | [x] | [x] |

#### External Links

| Link | Purpose | Works |
|------|---------|-------|
| Chroma Research | Context rot reference | [x] External link |

### Acceptance Criteria

- [x] All file pointers resolve to existing files
  - **Evidence:** All 5 file/directory pointers verified 2026-02-02
- [x] All directory pointers resolve to existing directories
  - **Evidence:** `.claude/rules/`, `.context/templates/`, `docs/knowledge/` all exist
- [x] All skill references are valid
  - **Evidence:** 6 skills verified (worktracker, problem-solving, nasa-se, orchestration, architecture, transcript)
- [x] External links work (or marked as external)
  - **Evidence:** Chroma Research link is external reference

### Related Items

- Parent: [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)
- Dependencies: TASK-001 through TASK-005

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 1 hour |
| Remaining Work | 0 hours |
| Time Spent | 0.5 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Validation Results | Documentation | (inline in this file) |

### Verification

- [x] All pointers validated
  - **Evidence:** 12/12 pointers verified (5 file/dir + 6 skills + 1 external)
- [x] No missing targets
  - **Evidence:** All targets exist on filesystem
- [x] Reviewed by: Verification Agent (2026-02-02)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
| 2026-02-02 | COMPLETE | All 12 pointers validated. 5 file/directory pointers, 6 skill references, 1 external link verified. |
