# TASK-067: Implement path-traversal guard in SubprocessSandboxAdapter

> **Type:** task
> **Status:** pending
> **Priority:** critical
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

Path validation: resolve all path arguments via pathlib.Path.resolve(); refuse if any path leaves packet_root.

---

## Acceptance Criteria

- [ ] Adapter rejects path arguments resolving outside packet_root with SandboxRefusalError
- [ ] Symlink test: adapter refuses paths whose lstat resolves outside packet_root
- [ ] Unit tests cover ≥10 path-traversal attempts
