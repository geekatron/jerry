# TASK-105: CLI integration tests via entrypoint; performance test ~300ms target

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-007
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Test via the CLI entrypoint (subprocess), not internal API.

---

## Acceptance Criteria

- [ ] CLI tests exercise the actual CLI binary, not internal Python API
- [ ] Performance test confirms ~300ms target on standard packet
- [ ] JSON output validates against schema
