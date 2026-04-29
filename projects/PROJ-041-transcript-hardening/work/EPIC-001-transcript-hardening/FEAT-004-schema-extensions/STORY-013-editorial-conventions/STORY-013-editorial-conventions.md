# STORY-013: Add `provenance.editorial_conventions` block

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
| [Schema Addition](#schema-addition) | What gets added to extraction-report.json |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** consumer of a transcript packet (human reviewer or downstream agent),
**I want** the per-session ASR-correction policy, stutter-preservation policy, speculation-marker policy, paraphrase-marker policy, and consensus-standard policy documented in the packet itself,
**So that** I know how to interpret narrative fields without inferring conventions from the prose.

---

## Schema Addition

Adds `provenance.editorial_conventions` to `extraction-report.json` schema v1.2 (optional sub-block).

```json
{
  "provenance": {
    "editorial_conventions": {
      "asr_correction_policy": "string (e.g., 'verbatim with [CANONICAL] disambiguation')",
      "stutter_preservation_policy": "string (e.g., 'preserved when meaningful, elided otherwise')",
      "speculation_marker_policy": "string (e.g., '[speculation] prefix in narrative fields')",
      "paraphrase_marker_policy": "string (e.g., '~ tilde wraps paraphrased content')",
      "consensus_standard_policy": "string (e.g., 'decisions require ≥2 speakers concurring')"
    }
  }
}
```

Without this block, agents either silently rewrite (loses provenance) or invent ad-hoc bracketing (drift). A documented `editorial_conventions` block solves this.

---

## Acceptance Criteria

- [ ] Schema field added to `extraction-report.json` schema v1.2 (or appropriate next minor version).
- [ ] Field is optional (existing packets without it continue to validate).
- [ ] At least one golden packet in `test_data/golden/` includes a populated editorial_conventions block.
- [ ] FEAT-003 SCHEMA-* validators pick up the new field automatically (rules read schemas).
- [ ] ADR amendment recorded (new ADR or ADR-001 amendment-002): captures decision and rationale.
- [ ] `ts-extractor` agent guidance updated: reference editorial_conventions block when emitting narrative fields.
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Draft schema addition for editorial_conventions block | pending |
| TASK-002 | Update extraction-report.json schema to v1.2 | pending |
| TASK-003 | Add golden packet with populated block | pending |
| TASK-004 | Update ts-extractor agent guidance | pending |
| TASK-005 | Author ADR amendment | pending |
| TASK-006 | Run /adversary C4 review | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-004](../FEAT-004-schema-extensions.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | FEAT-001 STORY-001, STORY-002 | ADR-007 vendored + ACCEPTED |
| Cooperates | FEAT-003 STORY-006 | SCHEMA-* validators inherit new field |

### Source

- [#273 §C3.1](https://github.com/geekatron/jerry/issues/273)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. |
