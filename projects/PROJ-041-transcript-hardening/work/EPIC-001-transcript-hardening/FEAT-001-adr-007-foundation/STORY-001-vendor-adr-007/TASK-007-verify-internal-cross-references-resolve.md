# TASK-007: Verify all internal cross-references inside ADR-007 resolve in new location

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-001
> **Owner:** ps-validator

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Walk every link inside the vendored ADR-007 (links to other ADRs, schemas, agents) and verify each resolves to a real file in this branch.

---

## Acceptance Criteria

- [ ] Every internal link inside ADR-007 resolves to an existing file
- [ ] Any unresolvable link is documented and remediated (or marked dead with rationale)
- [ ] Validation report persisted at `verify-cross-refs.md` in STORY-001 directory
