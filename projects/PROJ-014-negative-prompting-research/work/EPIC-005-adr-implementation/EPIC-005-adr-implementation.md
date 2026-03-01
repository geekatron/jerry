# EPIC-005: ADR Implementation

> **Type:** epic
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-28
> **Parent:** —
> **Owner:** Claude

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Epic description and objectives |
| [Children Features/Capabilities](#children-featurescapabilities) | Feature inventory |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Dependencies and links |
| [History](#history) | Status changes |

---

## Summary

Implement all 4 ADRs produced by PROJ-014 Phase 5. ADR-001 (NPT-014 Elimination) core implementation is complete. Remaining: ADR-001 post-implementation tasks, ADR-002 (Constitutional Triplet Upgrades), ADR-003 (Routing Disambiguation), ADR-004 (Compaction Resilience).

**Key Objectives:**
- ADR-001: Eliminate all NPT-014 instances (core DONE; post-implementation pending)
- ADR-002: Update guardrails template + governance schema (Phase 5A immediate; Phase 5B conditional on A/B testing)
- ADR-003: Add routing disambiguation sections to all 13 skills (Component A immediate; Component B conditional)
- ADR-004: PG-004 compaction testing + L2-REINJECT markers for H-04/H-32 + T-004 failure mode docs

---

## Children Features/Capabilities

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-001 | Implement ADR-001: NPT-014 Elimination | completed | high | 100% |
| FEAT-002 | Implement ADR-002: Constitutional Triplet Upgrades | in_progress | medium | 67% |
| FEAT-003 | Implement ADR-003: Routing Disambiguation | in_progress | medium | 50% |
| FEAT-004 | Implement ADR-004: Compaction Resilience | completed | medium | 100% |

### Feature Links

- [FEAT-001: Implement ADR-001: NPT-014 Elimination](./FEAT-001-implement-adr-001-npt-014-elimination/FEAT-001-implement-adr-001-npt-014-elimination.md)
- [FEAT-002: Implement ADR-002: Constitutional Triplet Upgrades](./FEAT-002-implement-adr-002-constitutional-upgrades/FEAT-002-implement-adr-002-constitutional-upgrades.md)
- [FEAT-003: Implement ADR-003: Routing Disambiguation](./FEAT-003-implement-adr-003-routing-disambiguation/FEAT-003-implement-adr-003-routing-disambiguation.md)
- [FEAT-004: Implement ADR-004: Compaction Resilience](./FEAT-004-implement-adr-004-compaction-resilience/FEAT-004-implement-adr-004-compaction-resilience.md)

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Features** | 4 |
| **Completed Features** | 2 |
| **Feature Completion %** | 50% |

---

## Related Items

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | TASK-016 | Phase 5 ADR production (ADR-001 through ADR-004) |
| Depends On | TASK-019 | C4 tournament PASS on final synthesis |

### References

- Implementation plan: `orchestration/adr001-implementation/ORCHESTRATION_PLAN.md`
- Phase 1 inventory: `orchestration/adr001-implementation/phase-1-npt014-inventory.md`
- GitHub Issue: [#122](https://github.com/geekatron/jerry/issues/122)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-28 | Claude | pending | Epic created |
| 2026-02-28 | Claude | in_progress | FEAT-001 execution started |
| 2026-02-28 | Claude | completed | FEAT-001 core implementation delivered |
| 2026-02-28 | Claude | in_progress | Reopened — FEAT-002/003/004 added for ADR-002/003/004; FEAT-001 post-implementation tasks added |
| 2026-02-28 | Claude | in_progress | FEAT-003 Component A done (TASK-036). FEAT-004 completed (TASK-038/039/040). 2/4 features done. |
