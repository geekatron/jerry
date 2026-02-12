# TASK-003: Create Active Project Section

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
| [Content](#content) | Description and key points |
| [Time Tracking](#time-tracking) | Effort metrics |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-003"
work_type: TASK
title: "Create Active Project Section"
description: |
  Create the Active Project section (~15 lines) for the new CLAUDE.md containing
  JERRY_PROJECT variable guidance and hook output interpretation.

classification: ENABLER
status: COMPLETE
resolution: DONE
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-202"
tags:
  - enabler
  - claude-md
  - project

effort: 1
acceptance_criteria: |
  - [x] JERRY_PROJECT variable documented
  - [x] Hook output tags explained
  - [x] Project context enforcement mentioned
  - [x] Section is ~15 lines
due_date: null

activity: DOCUMENTATION
original_estimate: 1
remaining_work: 0
time_spent: 0.5
```

---

## Content

### Description

Create the Active Project section for the new lean CLAUDE.md. This section explains how project context is managed and enforced.

### Target Content (~15 lines)

```markdown
## Active Project

**Set `JERRY_PROJECT` environment variable** to specify working project.
Session start hook provides project context via `<project-context>` or `<project-required>` tags.

Project context is enforced via SessionStart hook. See `scripts/session_start_hook.py`.
```

### Key Points to Include

1. **JERRY_PROJECT variable** - How to set active project
2. **Hook output tags** - `<project-context>`, `<project-required>`, `<project-error>`
3. **Enforcement** - Project context is required for substantial work
4. **Hook location** - Reference to scripts/session_start_hook.py

### Acceptance Criteria

- [x] JERRY_PROJECT variable documented
- [x] Hook output tags mentioned
- [x] Project enforcement explained
- [x] Line count ~15 lines (exactly 15 lines)
- [x] Brief and actionable

### Related Items

- Parent: [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)
- Reference: Current CLAUDE.md "Project Enforcement" section
- Reference: PLAN-CLAUDE-MD-OPTIMIZATION.md Appendix A

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
| Active Project Section | Documentation | CLAUDE.md (Active Project section) |

### Verification

- [x] Content matches target structure
- [x] Line count verified (15 lines)
- [x] Reviewed by: DISC-002 Adversarial Review (ps-critic score: 0.942)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
| 2026-02-01 | COMPLETE | Section created with DISC-002 review. ps-critic score: 0.942 (2 iterations). REM-001 addressed. Output: drafts/section-003-active-project.md |
