# TASK-012: Install agent-development-standards into rules

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Criticality:** C3 (AE-002)
> **Created:** 2026-02-21T23:59:00Z
> **Parent:** EN-001
> **Owner:** --
> **Effort:** 1
> **Activity:** deployment

---

## Summary

Install agent-development-standards into `.context/rules/` and create `.claude/rules/` symlink for auto-loading.

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

Copy `ps-architect-003-agent-development-standards.md` from the PROJ-007 orchestration output to `.context/rules/agent-development-standards.md`. Create a symlink in `.claude/rules/` so the file auto-loads at session start. Verify content integrity against the source artifact.

**AE-002 applies:** This task touches `.context/rules/` — auto-C3 minimum criticality. The installed file will be auto-loaded into every Claude Code session via the `.claude/rules/` symlink mechanism.

### Steps

1. Locate source artifact: `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/` (ps-architect-003-agent-development-standards.md)
2. Copy to `.context/rules/agent-development-standards.md`
3. Create symlink: `.claude/rules/agent-development-standards.md` → `../../.context/rules/agent-development-standards.md`
4. Verify content matches source (no truncation, no corruption)
5. Verify symlink resolves correctly

---

## Acceptance Criteria

- [ ] AC-1: `agent-development-standards.md` exists at `.context/rules/agent-development-standards.md`
- [ ] AC-2: Symlink exists at `.claude/rules/agent-development-standards.md` and resolves correctly
- [ ] AC-3: Content of installed file matches source orchestration artifact (content integrity)
- [ ] AC-4: Session start auto-loads the file (symlink mechanism verified)

---

## Implementation Notes

### Files to Create

| File | Action |
|------|--------|
| `.context/rules/agent-development-standards.md` | Copy from orchestration output |
| `.claude/rules/agent-development-standards.md` | Symlink to `.context/rules/` file |

### Symlink Pattern

Follow existing symlink pattern in `.claude/rules/`. Verify with `ls -la .claude/rules/` before creating.

### AE-002 Note

Touching `.context/rules/` is auto-C3. Self-review (S-010) required before marking done.

---

## Related Items

- **Parent:** [EN-001](../EN-001.md)
- **AE-002:** Touches `.context/rules/` — auto-C3 minimum
- **Source artifact:** `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps-architect-003-agent-development-standards.md`
- **Companion:** TASK-013 installs the companion routing standards file

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-21 | pending | Created — awaiting installation of orchestration output |
