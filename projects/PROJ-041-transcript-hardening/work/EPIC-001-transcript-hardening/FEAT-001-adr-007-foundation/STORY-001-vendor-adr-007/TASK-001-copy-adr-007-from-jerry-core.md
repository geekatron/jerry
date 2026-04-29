# TASK-001: Copy ADR-007 from jerry-core to docs/adrs/

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-001
> **Owner:** ps-architect

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Vendor `ADR-007-output-template-specification.md` from the jerry-core repository's transcript-skill project (`FEAT-006-output-consistency/docs/decisions/`) into this branch's public `docs/adrs/` directory. Preserve byte-identical content and record the jerry-core source commit SHA so the vendoring is reproducible and auditable.

This is the foundation Task for STORY-001 — all subsequent reference-update tasks (TASK-002 through TASK-005) depend on this file existing at the canonical path.

---

## Acceptance Criteria

- [ ] `docs/adrs/ADR-007-output-template-specification.md` exists in this branch
- [ ] `sha256sum` of vendored file matches `sha256sum` of jerry-core source at the recorded commit
- [ ] Source commit SHA recorded in STORY-001 History entry
- [ ] ADR-007 frontmatter (Type, Status, internal cross-references) byte-identical to jerry-core source
- [ ] No mutation of ADR-007 content during the vendoring step (status promotion happens in STORY-002, not here)
