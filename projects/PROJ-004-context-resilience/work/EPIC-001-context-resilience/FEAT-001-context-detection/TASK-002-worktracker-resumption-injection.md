# TASK-002: WORKTRACKER.md Auto-Injection in Resumption

> **Type:** task
> **Status:** done
> **Priority:** low
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** EN-008
> **Owner:** --
> **Effort:** 1.5h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What needs to be done |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Related Items](#related-items) | Links |
| [History](#history) | Status changes |

---

## Description

**Addresses:** DoD-5 (PARTIAL)

DoD-5 specifies that the resumption prompt reads both ORCHESTRATION.yaml and WORKTRACKER.md to reconstruct context. Currently, ORCHESTRATION.yaml is read by `CheckpointService._build_resumption_state()` at checkpoint creation time and injected via `ResumptionContextGenerator`. WORKTRACKER.md is not automatically included.

Add a WORKTRACKER.md read step to `HooksSessionStartHandler.handle()` that appends a `<worktracker>` XML block to the session start context when the file exists.

---

## Acceptance Criteria

- [ ] `HooksSessionStartHandler.handle()` reads `<JERRY_PROJECT>/WORKTRACKER.md` when project is active
- [ ] WORKTRACKER.md content appended as `<worktracker>` XML block in `additionalContext`
- [ ] Fail-open: if WORKTRACKER.md not found or unreadable, no error; skip injection
- [ ] Token budget considered: WORKTRACKER.md content should be truncated if > 2000 tokens (configurable)
- [ ] Unit tests for injection (happy path + file not found + truncation)
- [ ] Existing 229 hook tests still pass

---

## Implementation Notes

**Key file:** `src/interface/cli/hooks/hooks_session_start_handler.py`

Per REC-3 from the validation report, add a Step 5 in `handle()` that reads `<JERRY_PROJECT>/WORKTRACKER.md` and appends a `<worktracker>` XML block to `context_parts` when found. The session start handler already reads project context and checkpoint data; this follows the same pattern.

Consider token budget impact: WORKTRACKER.md files can grow large. Implement a truncation strategy (e.g., include only the Summary and Epics sections, or cap at a configurable character limit).

---

## Related Items

- Parent: [EN-008](./EN-008-context-resilience-hardening.md)
- Validation Report: REC-3, DoD-5 (PARTIAL)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | pending | Created from ST-003 validation REC-3. |
