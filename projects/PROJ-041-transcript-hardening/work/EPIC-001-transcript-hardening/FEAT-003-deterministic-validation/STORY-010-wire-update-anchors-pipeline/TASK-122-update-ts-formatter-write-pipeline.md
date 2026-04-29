# TASK-122: Update ts-formatter.md write-pipeline behavior

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-010
> **Owner:** eng-backend

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Per the decision: every rendered .md file write MUST be followed by `update-anchors`. Hook or prompt as decided.

---

## Acceptance Criteria

- [ ] ts-formatter.md updated with write-pipeline requirement
- [ ] If hook chosen: PostToolUse hook implementation
