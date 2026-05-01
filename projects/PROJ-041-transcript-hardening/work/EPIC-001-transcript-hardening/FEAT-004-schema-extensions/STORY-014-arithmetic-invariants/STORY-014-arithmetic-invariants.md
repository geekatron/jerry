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
| [Summary](#summary) | What this story delivers |
| [Schema Addition](#schema-addition) | What gets added to stat blocks |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
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

## Summary

Add the optional `arithmetic_invariants` sub-block to stat blocks (\`{computed, declared, match, computed_at_revision, scope_note?}\`). Generalizes the substrate-coupling fix beyond _anchors.json: any stat block with declared counts gets a recompute pattern and a match boolean. update-anchors keeps `computed` in lockstep with walked truth at every write.

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

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/problem-solving` | `ps-architect` | Author ADR-002 amendment-001 capturing arithmetic_invariants design |
| 2 | `/problem-solving` | `ps-investigator` | Identify all stat blocks that need arithmetic_invariants (extraction_stats, chunk_metadata, _anchors.json audit blocks) |
| 3 | `/eng-team` | `eng-backend` | Update extraction-report.json + _anchors.json schemas with arithmetic_invariants sub-block |
| 4 | `/eng-team` | `eng-backend` | Extend FEAT-003 SCHEMA-* validators to recompute and assert match per invariant; extend FEAT-003 STORY-008 update-anchors to refresh `computed` field |
| 5 | `/eng-team` | `eng-qa` | Golden packet with populated arithmetic_invariants for each affected stat block |
| 6 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review |
| 7 | `/worktracker` | `wt-verifier` | Validate AC; close |

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

| ID | Title | Owner | Status |
|----|-------|-------|--------|
| [TASK-144](./TASK-144-author-adr-002-amendment-001.md) | Author ADR-002 amendment-001 capturing arithmetic_invariants design | `ps-architect` | pending |
| [TASK-145](./TASK-145-identify-stat-blocks-needing-invariants.md) | Identify all stat blocks that need arithmetic_invariants | `ps-investigator` | pending |
| [TASK-146](./TASK-146-update-schemas-with-invariants-block.md) | Update extraction-report.json + _anchors.json schemas with arithmetic_invariants sub-block | `eng-backend` | pending |
| [TASK-147](./TASK-147-extend-validators-and-update-anchors.md) | Extend FEAT-003 SCHEMA-* validators + update-anchors to recompute and refresh `computed` | `eng-backend` | pending |
| [TASK-148](./TASK-148-golden-packet-with-arithmetic-invariants.md) | Golden packet with populated arithmetic_invariants for each affected stat block | `eng-qa` | pending |
| [TASK-149](./TASK-149-run-adversary-c4-review.md) | Run /adversary C4 review | `adv-executor` | pending |
| [TASK-150](./TASK-150-validate-ac-and-close-story-014.md) | Validate STORY-014 AC and close | `wt-verifier` | pending |

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
