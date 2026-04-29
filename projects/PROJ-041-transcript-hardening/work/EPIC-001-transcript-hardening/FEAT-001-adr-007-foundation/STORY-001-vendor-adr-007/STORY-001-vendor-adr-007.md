# STORY-001: Vendor ADR-007 from jerry-core to public docs/adrs/

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Source and Destination](#source-and-destination) | Cross-repo file paths |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry user installing the public `/transcript` skill,
**I want** ADR-007 to ship in the public release at a discoverable path,
**So that** SKILL.md cross-references resolve and I can verify the canonical output rules my packets are claimed to follow.

---

## Summary

Copy `ADR-007-output-template-specification.md` from the jerry-core repository into this branch's public `docs/adrs/`. Update SKILL.md, ts-formatter.md, PLAYBOOK.md, and ts-formatter.prompt.md cross-references from the long jerry-core path to the short public path.

---

## Source and Destination

| Side | Path |
|------|------|
| **Source (jerry-core)** | Separate jerry-core repository, under its transcript-skill project's `FEAT-006-output-consistency/docs/decisions/` directory (filename: `ADR-007-output-template-specification.md`). Implementer resolves exact path against the local jerry-core checkout. |
| **Destination (this branch)** | `docs/adrs/ADR-007-output-template-specification.md` |

This is a cross-repo file copy (the two repositories are separate per user direction). Use `cp` and stage the file in this branch.

---

## Acceptance Criteria

- [ ] `docs/adrs/ADR-007-output-template-specification.md` exists at HEAD on `feat/PROJ-041-transcript-hardening`.
- [ ] The vendored copy is byte-identical to the jerry-core source at the time of copy (record source commit SHA in History).
- [ ] All references to ADR-007 in `skills/transcript/SKILL.md` use the `docs/adrs/` path (no remaining old jerry-core project paths).
- [ ] All references to ADR-007 in `skills/transcript/agents/ts-formatter.md` use the `docs/adrs/` path.
- [ ] All references in `skills/transcript/PLAYBOOK.md` (if present) and `skills/transcript/agents/ts-formatter.prompt.md` (if present) use the `docs/adrs/` path.
- [ ] `grep -r "transcript-skill/work/EPIC-001-transcript-skill" skills/transcript/` returns zero matches (no remaining references to the old jerry-core project path).
- [ ] All internal cross-references inside ADR-007 itself (links to other ADRs, schemas, etc.) resolve to the new location.
- [ ] **Suggested CI check:** Add a test that asserts every `docs/adrs/ADR-NNN*.md` file referenced from any `skills/*/SKILL.md` resolves to a real file (catches future packaging gaps).

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Copy ADR-007 from jerry-core to docs/adrs/ | pending |
| TASK-002 | Update skills/transcript/SKILL.md cross-references | pending |
| TASK-003 | Update skills/transcript/agents/ts-formatter.md cross-references | pending |
| TASK-004 | Update PLAYBOOK.md and ts-formatter.prompt.md cross-references | pending |
| TASK-005 | Add CI check: every SKILL.md ADR cross-reference resolves | pending |
| TASK-006 | Verify internal cross-references inside ADR-007 resolve in new location | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001](../FEAT-001-adr-007-foundation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocks | STORY-002 | Status promotion can't happen until file is in canonical location |
| Blocks | FEAT-002 (BUG-004, BUG-005) | ADR amendments need readable ADR in target location |
| Blocks | FEAT-003 | Validators reference ADR-007 §4 rule IDs |

### Source

- [#273 §C1](https://github.com/geekatron/jerry/issues/273)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. P0 foundation. |
