# TASK-109: Wire CLI command with --dry-run and --bucket flags; add last_walked_at audit trail

> **Type:** task
> **Status:** pending
> **Priority:** high
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

CLI surface: `jerry transcript update-anchors <packet> [--dry-run] [--bucket BUCKET]...`.

---

## Acceptance Criteria

- [ ] CLI parser supports all flags from spec
- [ ] --dry-run reports changes without writing
- [ ] Each successful write updates `last_walked_at` ISO-8601 timestamp
