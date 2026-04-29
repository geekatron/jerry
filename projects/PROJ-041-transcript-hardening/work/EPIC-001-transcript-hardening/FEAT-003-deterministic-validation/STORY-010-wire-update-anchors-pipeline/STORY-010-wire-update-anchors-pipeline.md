# STORY-010: Wire `update-anchors` into `ts-formatter` write pipeline

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-003
> **Owner:** adam.nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Pipeline Integration](#pipeline-integration) | Where update-anchors runs |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** `ts-formatter` agent or fix-wave worker,
**I want** declared substrate counts to be automatically derived from walked truth at every write,
**So that** the "declare-then-attest" pattern is eliminated entirely — declared counts become a cache, never a hand-maintained assertion.

---

## Pipeline Integration

`ts-formatter` write pipeline: every time a packet's rendered .md files are written or modified, `update-anchors` runs and refreshes `_anchors.json` declared counts to match walked truth.

| Position | What happens |
|----------|--------------|
| After ts-formatter renders rendered .md files | Run `jerry transcript update-anchors <packet>` |
| Result | `_anchors.json` declared = walked; `last_walked_at` timestamp updated; `arithmetic_invariants.computed` (FEAT-004 STORY-014) refreshed |
| Fix-wave compatibility | Any future fix-wave agent that edits .md files runs the same pipeline; substrate stays in lockstep |

This is **the** integration that prevents iter-9-class regressions structurally. After STORY-010 lands, the substrate is mechanically derived rather than hand-attested at every write.

---

## Acceptance Criteria

- [ ] `ts-formatter` agent prompt updated: every write of a rendered .md file MUST be followed by `jerry transcript update-anchors <packet>`.
- [ ] If write pipeline is implemented as a hook (SubagentStop or PostToolUse): hook exists, runs `update-anchors`, fails the operation on sandbox refusal.
- [ ] Atomic write semantics: `update-anchors` failure does not leave the packet in inconsistent state.
- [ ] After STORY-010: re-running iter-9 audit reproduction shows declared == walked at every iteration.
- [ ] Existing `ts-formatter` golden test suite continues to pass.
- [ ] Performance: write pipeline adds <500ms overhead per .md file write on standard packets.
- [ ] `/eng-team` `eng-reviewer` confirms write pipeline changes do not break agent's primary purpose.
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Decide pipeline mechanism (PostToolUse hook vs prompt-discipline) | pending |
| TASK-002 | Update ts-formatter.md agent prompt | pending |
| TASK-003 | (If hook chosen) Implement PostToolUse hook | pending |
| TASK-004 | Update ts-formatter golden tests | pending |
| TASK-005 | Reproduce iter-9 audit case under new pipeline (declared == walked at every iter) | pending |
| TASK-006 | Run /eng-team eng-reviewer | pending |
| TASK-007 | Run /adversary C4 review | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-003](../FEAT-003-deterministic-validation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | STORY-008 | update-anchors CLI must exist |
| Blocked By | STORY-009 | Hook mechanism (if shared with verify) decided first |
| Blocks | EN-008 | Final adversary tournament must verify pipeline integrity |

### Source

- [#273 comment 1](https://github.com/geekatron/jerry/issues/273#issuecomment-4339264545) — gist proposal item 3

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. |
