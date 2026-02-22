# TASK-027: Add L5 CI Enforcement Gate for HARD Rule Ceiling

## Document Sections

| Section | Purpose |
|---------|---------|
| [Metadata](#metadata) | Type, status, priority, parent |
| [Summary](#summary) | What and why |
| [Scope](#scope) | Implementation steps |
| [Acceptance Criteria](#acceptance-criteria) | Done conditions |
| [Dependencies](#dependencies) | Blocks and blocked-by |
| [History](#history) | Change log |

---

## Metadata

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Criticality:** C3 (AE-002 — touches `.context/rules/`)
> **Parent:** EN-002
> **Source:** DEC-001 D-004
> **Created:** 2026-02-21T23:50:00Z

---

## Summary

Add an L5 CI enforcement gate that counts HARD rules in `quality-enforcement.md` and fails the build if the count exceeds the ceiling. This prevents the failure mode that caused the original silent breach (25 -> 30 -> 35). The gate is immune to context rot because it operates deterministically at commit/CI time, not inside an LLM context window.

---

## Scope

1. Create a CI check script that parses the `quality-enforcement.md` HARD Rule Index and counts H-rules.
2. Compare the count against the ceiling value declared in the Tier Vocabulary table of the same file.
3. Fail with a clear error message if count > ceiling, including current count and ceiling value.
4. Add the script to the pre-commit hook chain.
5. Add unit tests covering edge cases (at ceiling, over ceiling, under ceiling).

---

## Acceptance Criteria

- [ ] CI check script exists and passes when rule count <= ceiling
- [ ] CI check script fails with a clear, actionable error message when rule count > ceiling
- [ ] Script is wired into the pre-commit hook chain
- [ ] Unit tests cover: at-ceiling (pass), over-ceiling (fail), under-ceiling (pass)

---

## Dependencies

**Blocked by:** TASK-026 (ceiling must be updated to 25 first so the gate enforces the correct value, not the old 35).

**Blocks:** None.

---

## History

| Date | Author | Note |
|------|--------|------|
| 2026-02-21 | system | Created from EN-002 implementation plan (DEC-001 D-004) |
