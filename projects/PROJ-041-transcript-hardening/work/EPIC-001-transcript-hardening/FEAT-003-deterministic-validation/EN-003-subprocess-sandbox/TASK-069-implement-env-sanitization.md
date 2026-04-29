# TASK-069: Implement env var sanitization

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** EN-003
> **Owner:** eng-infra

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Subprocess inherits minimal sanitized env: only PATH=/usr/bin:/bin and explicit allowlist.

---

## Acceptance Criteria

- [ ] Adapter strips all env vars except PATH
- [ ] PATH set to /usr/bin:/bin only
- [ ] Unit tests verify LD_PRELOAD, PYTHONPATH, etc. cannot leak in
