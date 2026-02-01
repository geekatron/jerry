# TASK-002: Create Navigation Pointers Section

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-002"
work_type: TASK
title: "Create Navigation Pointers Section"
description: |
  Create the Navigation section (~20 lines) for the new CLAUDE.md containing
  pointers to find coding standards, skills, project context, and knowledge.

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
  - navigation

effort: 2
acceptance_criteria: |
  - Navigation table with Need and Location columns
  - All key locations documented
  - Skills referenced
  - Templates referenced
  - Section is ~20 lines
due_date: null

activity: DOCUMENTATION
original_estimate: 2
remaining_work: 2
time_spent: null
```

---

## Content

### Description

Create the Navigation section for the new lean CLAUDE.md. This section tells Claude how to find information rather than including all the information inline.

### Target Content (~20 lines)

```markdown
## Navigation

| Need | Location |
|------|----------|
| Coding standards | `.claude/rules/` (auto-loaded) |
| Work tracking | `/worktracker` skill |
| Problem solving | `/problem-solving` skill |
| Architecture | `/architecture` skill |
| Templates | `.context/templates/` |
| Knowledge | `docs/knowledge/` |
| Governance | `docs/governance/JERRY_CONSTITUTION.md` |
```

### Required Pointers

1. **Coding standards** -> `.claude/rules/` (auto-loaded by Claude Code)
2. **Work tracking** -> `/worktracker` skill
3. **Problem solving** -> `/problem-solving` skill
4. **Architecture** -> `/architecture` skill
5. **NASA SE** -> `/nasa-se` skill
6. **Orchestration** -> `/orchestration` skill
7. **Templates** -> `.context/templates/`
8. **Knowledge** -> `docs/knowledge/`
9. **Governance** -> `docs/governance/JERRY_CONSTITUTION.md`

### Acceptance Criteria

- [ ] Navigation table complete
- [ ] All key locations documented
- [ ] Skills listed with `/skill` format
- [ ] Auto-loaded content marked
- [ ] Line count ~20 lines

### Related Items

- Parent: [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)
- Reference: PLAN-CLAUDE-MD-OPTIMIZATION.md Appendix A

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 2 hours |
| Remaining Work | 2 hours |
| Time Spent | 0 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Navigation Section | Documentation | CLAUDE.md (Navigation section) |

### Verification

- [ ] All pointers listed
- [ ] Table format correct
- [ ] Line count verified
- [ ] Reviewed by: -

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
