# STORY-015: Add `discussions[]` as 5th entity type

> **Type:** story
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-004
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Schema Addition](#schema-addition) | What gets added |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** consumer of a transcript packet,
**I want** a 5th top-level entity type for speech that's neither a decision nor a question (speculation, single-speaker factoid, raised-but-not-pursued items),
**So that** these don't force-fit into `decisions[]` with low-confidence (consensus inflation) or vanish entirely.

---

## Schema Addition

Adds `discussions[]` as new top-level array in `extraction-report.json` v1.2 (optional, alongside `decisions[]`, `questions[]`, `action_items[]`, `topics[]`).

| Surface | Addition |
|---------|----------|
| `extraction-report.json` schema | New `discussions[]` array, each item has `disc_id`, `speakers[]`, `summary`, `verbatim`, `topics[]`, `confidence` |
| Anchor format | `disc-NNN` regex (inherits `\d{3,}` from FEAT-002 BUG-004 resolution) |
| Mindmap symbols | `~` (mermaid), `[~]` (ascii) |
| Output template | New `## Discussion Items` H2 in `07-topics.md` (or designated topics file) |

ADRs to amend: ADR-001 (agent architecture: ts-extractor) + ADR-007 (output template: anchor format extension).

---

## Acceptance Criteria

- [ ] Schema field added: `discussions[]` array in extraction-report.json v1.2.
- [ ] Item schema specifies disc_id, speakers, summary, verbatim, topics, confidence.
- [ ] Anchor regex `^disc-\d{3,}$` registered in canonical schema.
- [ ] Output template updated: `## Discussion Items` H2 section in topics file.
- [ ] Mindmap symbols added: `~` for mermaid, `[~]` for ascii.
- [ ] FEAT-005 mindmap fixes (BUG-006 bracket-escape) extend to cover the new `[~]` ascii fallback symbol where rendered as Mermaid.
- [ ] `ts-extractor` agent updated: emits discussion items when speech is neither decision nor question.
- [ ] At least one golden packet exercises discussions[] (existing audit packet has 33 disc_links per the gist test output — use as basis).
- [ ] ADR-001 + ADR-007 amendments recorded.
- [ ] `/adversary` C4 ≥0.95 phase gate.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Author discussions[] schema in extraction-report.json | pending |
| TASK-002 | Register disc-NNN regex pattern | pending |
| TASK-003 | Update output template (topics file) with H2 section | pending |
| TASK-004 | Add mindmap symbols | pending |
| TASK-005 | Update ts-extractor agent guidance | pending |
| TASK-006 | Author ADR-001 + ADR-007 amendments | pending |
| TASK-007 | Add golden packet exercise discussions[] | pending |
| TASK-008 | Run /adversary C4 review | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-004](../FEAT-004-schema-extensions.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | FEAT-001 STORY-001, STORY-002 | ADR-007 vendored + ACCEPTED |
| Blocked By | FEAT-002 BUG-004 | seg-NNN regex resolution provides disc-NNN convention |
| Cooperates | FEAT-005 BUG-006 | New ascii `[~]` symbol must HTML-escape if rendered as Mermaid label |

### Source

- [#273 §C3.3](https://github.com/geekatron/jerry/issues/273)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Story created. |
