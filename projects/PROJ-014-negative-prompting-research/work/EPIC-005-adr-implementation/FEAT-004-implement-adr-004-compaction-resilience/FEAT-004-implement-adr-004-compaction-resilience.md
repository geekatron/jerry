# FEAT-004: Implement ADR-004: Compaction Resilience

> **Type:** feature
> **Status:** completed
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-02-28
> **Parent:** EPIC-005
> **Owner:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature description and value |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children Stories/Enablers](#children-storiesenablers) | Task inventory |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Dependencies and links |
| [History](#history) | Status changes |

---

## Summary

Implement ADR-004 (Compaction Resilience) across three independent decisions. Decision 1 (unconditional): establish PG-004 compaction testing requirement for all constraint-bearing artifacts. Decision 2 (timing conditional): add L2-REINJECT markers for H-04 and H-32 to close widest-failure-window Tier B enforcement gaps. Decision 3 (unconditional): add T-004 failure mode documentation to all constraint-bearing templates.

**Value Proposition:**
- Constraint survival verification through mandatory compaction testing
- Narrowed enforcement gaps for H-04/H-32 via L2-REINJECT markers
- Operational awareness of compaction failure modes through template documentation

---

## Acceptance Criteria

### Definition of Done

- [x] Decision 1: PG-004 compaction testing requirement documented and enforced
- [x] Decision 2: L2-REINJECT markers added for H-04 and H-32 within token budget
- [x] Decision 3: T-004 failure mode documentation added to constraint-bearing templates

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | PG-004 testing requirement integrated into testing-standards.md | [x] |
| AC-2 | H-04 and H-32 L2-REINJECT markers added within 850-token budget (~619/850 = 72.8%) | [x] |
| AC-3 | Constraint-bearing templates include compaction failure mode section (9 templates) | [x] |

---

## Children Stories/Enablers

### Task Inventory

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| TASK-038 | Decision 1: PG-004 Compaction testing requirement | completed | high |
| TASK-039 | Decision 2: Add L2-REINJECT markers for H-04 and H-32 | completed | high |
| TASK-040 | Decision 3: T-004 Failure mode documentation in templates | completed | medium |

### Task Links

- [TASK-038: PG-004 compaction testing](./TASK-038-pg004-compaction-testing.md)
- [TASK-039: L2-REINJECT markers for H-04 H-32](./TASK-039-l2-reinject-h04-h32.md)
- [TASK-040: T-004 failure mode documentation](./TASK-040-t004-failure-mode-docs.md)

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 3 |
| **Completed Tasks** | 3 |
| **Completion %** | 100% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-005: ADR Implementation](../EPIC-005-adr-implementation.md)

### References

- ADR-004: `orchestration/neg-prompting-20260227-001/phase-5/ADR-004-compaction-resilience.md`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-28 | Claude | pending | Feature created |
| 2026-02-28 | Claude | completed | All 3 decisions implemented. Commit: f5f892b2 |
