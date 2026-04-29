# TASK-062: Author conftest.py with fixtures and stub adapters

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** EN-002
> **Owner:** eng-qa

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Pytest fixtures load golden packets; stub adapters wire PacketValidator hermetically.

---

## Acceptance Criteria

- [ ] tests/transcript/validation/conftest.py exists
- [ ] Fixtures auto-discover golden packets via glob
- [ ] Stub adapters (FilesystemPacketLoader stub, SubprocessSandbox stub) wire PacketValidator
