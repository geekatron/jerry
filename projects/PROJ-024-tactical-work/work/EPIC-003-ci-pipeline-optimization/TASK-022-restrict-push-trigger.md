# TASK-022: Restrict Push Trigger to Protected Branches Only

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-13
> **Parent:** EPIC-003
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

`on: push: branches: ["**"]` triggers full CI on ANY branch push. Combined with global PR write access (TASK-021), this is an unnecessary attack surface identified by the red-team assessment. Feature branch pushes should only trigger CI via PR.

---

## Acceptance Criteria

- [ ] `on: push: branches: [main, master]`
- [ ] `on: pull_request: branches: [main, master, "claude/**"]` unchanged
- [ ] Feature branch pushes only trigger CI via PR
