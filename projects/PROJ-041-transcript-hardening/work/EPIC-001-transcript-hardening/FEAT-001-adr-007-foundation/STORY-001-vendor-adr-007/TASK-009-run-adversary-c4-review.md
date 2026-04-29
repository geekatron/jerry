# TASK-009: Run /adversary C4 review (≥0.95)

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-001
> **Owner:** adv-executor

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

adv-selector → adv-executor → adv-scorer against the STORY-001 deliverables (vendored ADR + cross-reference updates + CI check). Threshold ≥0.95 per project-wide stricter-than-SSOT direction.

---

## Acceptance Criteria

- [ ] adv-selector strategy plan persisted in STORY-001 directory
- [ ] adv-executor execution report persisted
- [ ] adv-scorer composite ≥0.95 with per-dimension breakdown persisted
- [ ] Any sub-threshold finding remediated and re-scored
