# TASK-108: Author atomic-write infrastructure adapter (temp file + rename)

> **Type:** task
> **Status:** pending
> **Priority:** critical
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-008
> **Owner:** eng-backend

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Atomic write semantics: no partial-update window.

---

## Acceptance Criteria

- [ ] AtomicWriteAdapter exists in infrastructure/
- [ ] Uses temp file + os.rename() pattern (POSIX atomic on same filesystem)
- [ ] Failure mid-write leaves _anchors.json unchanged
