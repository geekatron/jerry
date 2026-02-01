# TASK-004: Create Critical Constraints Section

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-004"
work_type: TASK
title: "Create Critical Constraints Section"
description: |
  Create the Critical Constraints section (~15 lines) for the new CLAUDE.md containing
  hard principles (P-003, P-020, P-022) and Python/UV requirements.

classification: ENABLER
status: BACKLOG
resolution: null
priority: CRITICAL
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-202"
tags:
  - enabler
  - claude-md
  - constraints

effort: 1
acceptance_criteria: |
  - P-003 (no recursive subagents) documented
  - P-020 (user authority) documented
  - P-022 (no deception) documented
  - Python 3.11+ / UV requirement documented
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

Create the Critical Constraints section for the new lean CLAUDE.md. This section documents the HARD principles that cannot be overridden.

### Target Content (~15 lines)

```markdown
## Critical Constraints (HARD)

- **P-003**: Maximum ONE level of agent nesting
- **P-020**: User has ultimate authority
- **P-022**: Never deceive users
- **Python**: 3.11+ with UV only (`uv run`, never `python` or `pip`)
```

### Hard Principles to Include

| ID | Principle | Description |
|----|-----------|-------------|
| P-003 | No Recursive Subagents | Maximum ONE level of agent nesting (orchestrator -> worker) |
| P-020 | User Authority | User has ultimate authority; never override user decisions |
| P-022 | No Deception | Never deceive users about actions, capabilities, or confidence |

### Python Environment

- Python 3.11+ required
- UV only (`uv run`, `uv add`)
- NEVER use `python`, `python3`, `pip`, or `pip3`

### Acceptance Criteria

- [ ] P-003 documented with clear explanation
- [ ] P-020 documented with clear explanation
- [ ] P-022 documented with clear explanation
- [ ] Python/UV requirement documented
- [ ] Line count ~15 lines
- [ ] Marked as HARD constraints

### Related Items

- Parent: [EN-202: CLAUDE.md Rewrite](./EN-202-claude-md-rewrite.md)
- Reference: docs/governance/JERRY_CONSTITUTION.md
- Reference: .claude/rules/python-environment.md

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
| Critical Constraints Section | Documentation | CLAUDE.md (Critical Constraints section) |

### Verification

- [ ] All hard principles included
- [ ] UV requirement included
- [ ] Line count verified
- [ ] Reviewed by: -

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
