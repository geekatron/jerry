# TASK-083: Verify rules reject `## Backlinks` H2 form; accept `<backlinks>` tag form

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-004
> **Owner:** ps-validator

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Direct test of BUG-005 resolution.

---

## Acceptance Criteria

- [ ] Packet with `## Backlinks` H2 fails CONTENT validation
- [ ] Packet with `<backlinks>` tag passes CONTENT validation
