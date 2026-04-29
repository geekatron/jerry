# TASK-115: Update ts-formatter.md agent prompt + ts-formatter.prompt.md checklist

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-009
> **Owner:** eng-backend

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Per the hook-mechanism decision, update the agent prompt to require post-render verify invocation. Add validation_status: PASS|FAIL to return contract.

---

## Acceptance Criteria

- [ ] ts-formatter.md updated to require post-render `verify`
- [ ] Return contract documents `validation_status` field
- [ ] Agent cannot report `completed` if verify exit code != 0
