# TASK-066: Security boundary architecture: SubprocessSandbox port shape; hexagonal H-07 isolation

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** EN-003
> **Owner:** eng-architect

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Define the SubprocessSandbox Protocol contract per the threat model.

---

## Acceptance Criteria

- [ ] SubprocessSandbox Protocol declared in application/ports.py
- [ ] Port specifies: command allowlist, path validation, timeout, env sanitization, output cap
- [ ] H-07 isolation: port is in application layer; adapter is in infrastructure
