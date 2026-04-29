# TASK-118: Test against iter-9 audit packet — agent correctly catches at exit

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-009
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Re-run iter-9 audit scenario through ts-formatter; confirm validator catches drift at agent exit (not at adversary review 30 min later).

---

## Acceptance Criteria

- [ ] Test reproduces iter-9 audit; validator catches drift at agent exit
- [ ] Total agent execution remains under 5s
- [ ] Test integrated into ts-formatter golden test suite
