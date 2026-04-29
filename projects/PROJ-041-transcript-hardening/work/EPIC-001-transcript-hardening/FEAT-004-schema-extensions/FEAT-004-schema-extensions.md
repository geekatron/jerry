# FEAT-004: Schema Extensions

<!--
TEMPLATE: Feature
PURPOSE: Four additive schema enhancements to extraction-report.json that close gaps surfaced by the audit
-->

> **Type:** feature
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-04-28T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** EPIC-001
> **Owner:** adam.nowak

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Feature delivers |
| [Children Stories/Enablers](#children-storiesenablers) | Story inventory |
| [Acceptance Criteria](#acceptance-criteria) | Feature-level acceptance |
| [Progress Summary](#progress-summary) | Overall progress |
| [Dependencies](#dependencies) | Inputs and downstream blocks |
| [Related Items](#related-items) | Hierarchy and references |
| [History](#history) | Status changes |

---

## Summary

Four additive schema enhancements to `extraction-report.json` and supporting structures, all surfaced by the same external audit. Each addresses a specific structural gap that today forces agents into ad-hoc behavior or silent loss of information.

| Story | Addition | Why |
|-------|----------|-----|
| STORY-013 | `provenance.editorial_conventions` block (ASR/stutter/speculation/paraphrase/consensus policies) | Without a sanctioned policy block, agents either silently rewrite (loses provenance) or invent ad-hoc bracketing (drift). |
| STORY-014 | `arithmetic_invariants` sub-block on stat blocks (`{computed, declared, match, computed_at_revision, scope_note?}`) | "Stat-block claims numbers it can't reproduce" defect class showed up across multiple adversary iterations on different surfaces. INV-EXT-001 (state count == array length) is the start; this generalizes the principle. |
| STORY-015 | `discussions[]` as 5th top-level entity type with `disc-NNN` anchor + mindmap symbols | Speech that's neither a decision nor a question (speculation, single-speaker factoid, raised-but-not-pursued items) currently force-fits into `decisions[]` with low-confidence (consensus inflation) or vanishes. |
| STORY-016 | `provenance.audit_basis` field (option (a) lighter touch) for cross-sidecar discoverability | Audit methodology evolves inside `_anchors.json.audit_breakdown` but `extraction-report.json` has no equivalent slot — readers consulting only the latter learn extraction methodology but cannot discover audit-methodology lineage. The two metadata files drift silently apart over a packet's lifetime. |

All four are additive (existing schemas continue to validate). Each Story is independent unless the table below states otherwise.

---

## Children Stories/Enablers

| ID | Type | Title | Status | Priority |
|----|------|-------|--------|----------|
| STORY-013 | Story | Add provenance.editorial_conventions block | pending | medium |
| STORY-014 | Story | Add arithmetic_invariants for stat blocks | pending | medium |
| STORY-015 | Story | Add discussions[] as 5th entity type | pending | medium |
| STORY-016 | Story | Add provenance.audit_basis for cross-sidecar discoverability | pending | low |

### Work Item Links

- [STORY-013: editorial_conventions](./STORY-013-editorial-conventions/STORY-013-editorial-conventions.md)
- [STORY-014: arithmetic_invariants](./STORY-014-arithmetic-invariants/STORY-014-arithmetic-invariants.md)
- [STORY-015: discussions[]](./STORY-015-discussions-entity/STORY-015-discussions-entity.md)
- [STORY-016: audit_basis](./STORY-016-audit-basis/STORY-016-audit-basis.md)

---

## Progress Summary

```
Stories: [....................]  0% (0/4 completed)
Overall: [....................]  0%
```

---

## Acceptance Criteria

- [ ] All 4 schema additions land in `extraction-report.json` schema v1.2 (or appropriate next minor version).
- [ ] Schemas validate (no JSON Schema errors).
- [ ] Golden packets in `test_data/` updated to demonstrate each new shape.
- [ ] FEAT-003 validators include checks for the new shapes (where applicable: STORY-014 arithmetic_invariants is mechanically reconciled by validator).
- [ ] STORY-015 (discussions[]) requires BUG-004 (seg-NNN regex) resolution before disc-NNN regex can be derived from it.
- [ ] ADR amendments recorded where required (STORY-013 → new ADR or ADR-001 amendment-002; STORY-014 → ADR-002 amendment-001; STORY-015 → ADR-001 + ADR-007 amendments).

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | FEAT-001 STORY-001 | ADR-007 vendoring must complete |
| Blocked By | FEAT-001 STORY-002 | ADR-007 must be ACCEPTED before schema additions reference it |
| Blocked By | FEAT-002 BUG-004 | STORY-015 (discussions[]) needs resolved seg-NNN regex |
| Cooperates | FEAT-003 | Validators encode the new shapes; schema additions and validator additions are paired work |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001](../EPIC-001-transcript-hardening.md)

### External

- Source: [#273 §C3.1, §C3.2, §C3.3](https://github.com/geekatron/jerry/issues/273) + [comment 2](https://github.com/geekatron/jerry/issues/273#issuecomment-4339392440)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Feature created. 4 Stories scaffolded with audit-stated rationale. |
