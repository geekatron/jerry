# TASK-005: Create Quick Reference Section

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
| [Content](#content) | Quick reference items |
| [Time Tracking](#time-tracking) | Effort metrics |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-005"
work_type: TASK
title: "Create Quick Reference Section"
description: |
  Create the Quick Reference section (~15 lines) for the new CLAUDE.md containing
  CLI command summary and skill invocation summary.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-202"
tags:
  - enabler
  - claude-md
  - reference

effort: 1
acceptance_criteria: |
  - CLI commands summarized
  - Skills listed
  - Key file locations noted
  - Section is ~15 lines
due_date: null

activity: DOCUMENTATION
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

Create the Quick Reference section for the new lean CLAUDE.md. This section provides at-a-glance reference for common operations.

### Target Content (~15 lines)

```markdown
## Quick Reference

**CLI**: `jerry session start|end` | `jerry items list|show` | `jerry projects list|context`

**Skills**: `/worktracker` | `/problem-solving` | `/nasa-se` | `/orchestration` | `/architecture`
```

### Quick Reference Items

1. **CLI Commands**
   - Session: `jerry session start|end|status`
   - Items: `jerry items list|show`
   - Projects: `jerry projects list|context|validate`

2. **Skills**
   - `/worktracker` - Work tracking
   - `/problem-solving` - PS framework
   - `/nasa-se` - NASA SE processes
   - `/orchestration` - Workflow coordination
   - `/architecture` - Architecture decisions

3. **Key Locations** (optional if space permits)
   - WORKTRACKER.md in project folder
   - Templates in `.context/templates/`

### Acceptance Criteria

- [ ] CLI commands listed concisely
- [ ] All key skills listed
- [ ] Format is scannable/compact
- [ ] Line count ~15 lines

### Related Items

- Parent: [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)
- Reference: Current CLAUDE.md CLI section

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 1 hour |
| Remaining Work | 1 hour |
| Time Spent | 0 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Quick Reference Section | Documentation | CLAUDE.md (Quick Reference section) |

### Verification

- [ ] CLI commands accurate
- [ ] Skills list complete
- [ ] Line count verified
- [ ] Reviewed by: -

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
