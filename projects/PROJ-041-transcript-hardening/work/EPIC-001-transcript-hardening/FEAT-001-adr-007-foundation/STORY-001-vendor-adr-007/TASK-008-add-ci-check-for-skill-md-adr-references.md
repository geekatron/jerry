# TASK-008: Add CI check: every SKILL.md ADR cross-reference resolves

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-001
> **Owner:** eng-devsecops

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Add a CI step that asserts every `docs/adrs/ADR-NNN*.md` referenced from any `skills/*/SKILL.md` resolves to a real file. Catches future packaging gaps.

---

## Acceptance Criteria

- [ ] CI workflow step exists that grep-extracts ADR refs from SKILL.md files and verifies each resolves
- [ ] Test run shows all current SKILL.md ADR references resolve
- [ ] CI step blocks merge on broken ADR cross-references
