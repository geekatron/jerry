# TASK-017: Install pattern taxonomy into docs/knowledge

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

## Summary

Install the agent pattern taxonomy into `docs/knowledge/` as reference material.

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

Copy `ps-synthesizer-001-synthesis.md` from the PROJ-007 orchestration output to `docs/knowledge/agent-pattern-taxonomy.md`. This is the unified pattern taxonomy covering 57 problem-solving agent patterns and 10 NASA SE patterns. It serves as the evidence base for ADR-PROJ007-001 and ADR-PROJ007-002 and provides reference material for agent development work.

This is a C2 task (reference material only, does not touch `.context/rules/` or governance files).

### Steps

1. Locate source artifact: `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps-synthesizer-001-synthesis.md`
2. Copy to `docs/knowledge/agent-pattern-taxonomy.md`
3. Verify content matches source (no truncation, no corruption)

---

## Acceptance Criteria

- [ ] AC-1: `agent-pattern-taxonomy.md` exists at `docs/knowledge/agent-pattern-taxonomy.md`
- [ ] AC-2: Content matches source orchestration artifact

---

## Implementation Notes

### Files to Create

| File | Action |
|------|--------|
| `docs/knowledge/agent-pattern-taxonomy.md` | Copy from orchestration output |

### Note on Scope

This file is reference/knowledge material. It is NOT auto-loaded at session start and does NOT require a `.claude/rules/` symlink. It is accessible via the `docs/knowledge/` navigation pointer in CLAUDE.md.

---

## Related Items

- **Parent:** [EN-001](../EN-001.md)
- **Source artifact:** `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps-synthesizer-001-synthesis.md`
- **Evidence base for:** TASK-014 (ADR-PROJ007-001), TASK-015 (ADR-PROJ007-002)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-21 | pending | Created — awaiting installation of orchestration output |
