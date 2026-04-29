# TASK-180: Phase 4 exploit attempts against SubprocessSandbox: ≥5 bypass classes

> **Type:** task
> **Status:** pending
> **Priority:** critical
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** EN-004
> **Owner:** red-exploit

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Attempted bypasses: command injection, path traversal, env poisoning, symlink escape, resource exhaustion.

---

## Acceptance Criteria

- [ ] sandbox-exploit-attempts.md persisted with ≥5 bypass attempts
- [ ] All bypasses blocked by SubprocessSandbox
- [ ] Any successful bypass triggers EN-003 re-open
