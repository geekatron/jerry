# TASK-019: Update CLAUDE.md navigation table

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Criticality:** C2
> **Created:** 2026-02-21T23:59:00Z
> **Parent:** EN-001
> **Owner:** --
> **Effort:** 1
> **Activity:** documentation

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What this task requires |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical approach and constraints |
| [Related Items](#related-items) | Parent and related work |
| [History](#history) | Status changes |

---

## Description

Add references to `agent-development-standards.md` and `agent-routing-standards.md` in the CLAUDE.md Navigation table so the new rule files are discoverable. The Navigation section in CLAUDE.md is the primary discovery mechanism for rule files loaded at session start.

### Steps

1. Read `CLAUDE.md` Navigation table
2. Add a row for `agent-development-standards.md` under the coding/architecture/testing rules pointer
3. Add a row for `agent-routing-standards.md` under the coding/architecture/testing rules pointer
4. Verify no formatting regressions in the navigation table

---

## Acceptance Criteria

- [ ] AC-1: CLAUDE.md Navigation table includes a reference to `agent-development-standards.md`
- [ ] AC-2: CLAUDE.md Navigation table includes a reference to `agent-routing-standards.md`
- [ ] AC-3: Navigation table formatting is valid markdown (no broken rows or missing pipes)

---

## Implementation Notes

### Files to Modify

| File | Change |
|------|--------|
| `CLAUDE.md` | Add two rows to Navigation table for new rule files |

### Navigation Table Pattern

Follow the existing pattern in CLAUDE.md Navigation section. New rule files live in `.context/rules/` and are auto-loaded via `.claude/rules/` symlinks. The navigation entry should note both the need and the location.

Example pattern from existing entries:
```
| Coding/architecture/testing rules | `.context/rules/` (A) |
```

The new entries for agent standards can either extend the existing `.context/rules/ (A)` row description or add specific named rows for discoverability.

### Dependency

TASK-012 and TASK-013 should complete first so the files being referenced actually exist.

---

## Related Items

- **Parent:** [EN-001](../EN-001.md)
- **Depends on:** TASK-012 (agent-development-standards installed), TASK-013 (agent-routing-standards installed)
- **File modified:** `CLAUDE.md`

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-21 | pending | Created — depends on TASK-012 and TASK-013 completing first |
