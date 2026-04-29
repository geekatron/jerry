# STORY-014: Add `arithmetic_invariants` for stat blocks

> **Type:** story
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-004
> **Owner:** adam.nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Schema Addition](#schema-addition) | What gets added to stat blocks |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** consumer of a stat block in a transcript packet,
**I want** every declared count to ship with a recompute pattern, computed value, declared value, match boolean, and revision id,
**So that** stat-block claims that don't reproduce are mechanically detectable.

---

## Schema Addition

Adds `arithmetic_invariants` sub-block to stat blocks (`extraction_stats.confidence_summary`, `chunk_metadata`, `_anchors.json` audit blocks).

```json
{
  "arithmetic_invariants": {
    "computed": <number>,
    "declared": <number>,
    "match": <boolean>,
    "computed_at_revision": "string (commit SHA or packet revision identifier)",
    "scope_note": "string (optional, describes computation method)"
  }
}
```

The audit identified "stat-block claims numbers it can't reproduce" as a defect class that showed up across multiple iterations on different surfaces. INV-EXT-001 (state count == array length) is the start; this generalizes the principle.

FEAT-003 STORY-008 (`update-anchors`) keeps `arithmetic_invariants.computed` in lockstep with walked truth.

---

## Acceptance Criteria

- [ ] Schema field added to all relevant stat blocks per ADR-002 amendment-001.
- [ ] Field is optional (existing packets without it continue to validate).
- [ ] Validators (FEAT-003) recompute and assert `computed == declared` per invariant.
- [ ] FEAT-003 STORY-008 (`update-anchors`) refreshes `computed` on every write.
- [ ] At least one golden packet includes populated arithmetic_invariants for each affected stat block.
- [ ] ADR-002 amendment-001 records the decision.
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Identify all stat blocks that need arithmetic_invariants | pending |
| TASK-002 | Author schema addition | pending |
| TASK-003 | Update extraction-report.json + _anchors.json schemas | pending |
| TASK-004 | Add validators in FEAT-003 SCHEMA family for the new shapes | pending |
| TASK-005 | Update FEAT-003 STORY-008 update-anchors to refresh computed | pending |
| TASK-006 | Author ADR-002 amendment-001 | pending |
| TASK-007 | Run /adversary C4 review | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-004](../FEAT-004-schema-extensions.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | FEAT-001 STORY-001, STORY-002 | ADR-007 vendored + ACCEPTED |
| Cooperates | FEAT-003 STORY-006, STORY-008 | Validators encode invariants; update-anchors refreshes computed |

### Source

- [#273 §C3.2](https://github.com/geekatron/jerry/issues/273)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. |
