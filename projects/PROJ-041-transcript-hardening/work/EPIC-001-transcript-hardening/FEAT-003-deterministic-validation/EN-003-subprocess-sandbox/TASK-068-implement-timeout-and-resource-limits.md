# TASK-068: Implement timeout + resource limits

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

Default 5s wall-clock timeout; configurable up to 30s; hard kill at 60s. Output cap 1MB.

---

## Acceptance Criteria

- [ ] Adapter kills subprocess at configured timeout with SandboxTimeoutError
- [ ] Adapter caps stdout at 1MB with SandboxOutputOverflowError
- [ ] Unit tests verify timeout fires correctly
