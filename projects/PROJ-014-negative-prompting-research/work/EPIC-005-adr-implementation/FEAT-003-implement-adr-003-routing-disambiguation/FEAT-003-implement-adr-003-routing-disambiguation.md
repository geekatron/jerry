# FEAT-003: Implement ADR-003: Routing Disambiguation Standard

> **Type:** feature
> **Status:** pending
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

Implement ADR-003 (Routing Disambiguation Standard) in two components. Component A (unconditional): all 13 skills add routing disambiguation sections with consequence documentation — enumerate misrouting conditions, correct alternatives, and failure consequences. Component B (conditional on TASK-025 A/B testing): standardize framing vocabulary across routing disambiguation sections.

**Value Proposition:**
- Post-hoc routing auditability through consequence documentation
- Reduced misrouting impact through explicit alternative skill guidance
- Closes AP-01/AP-02 anti-pattern gaps at the skill level

---

## Acceptance Criteria

### Definition of Done

- [ ] Component A: All 13 skills have routing disambiguation sections
- [ ] Component A: Each section includes conditions, alternatives, and consequences
- [ ] Component A: Sections grounded in trigger map collision analysis
- [ ] Component B: Framing vocabulary standardized (conditional on TASK-025 results)

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | 7 new routing disambiguation sections added (skills currently without) | [ ] |
| AC-2 | 6 existing sections updated with consequence documentation | [ ] |
| AC-3 | All sections follow the ADR-003 template format | [ ] |

---

## Children Stories/Enablers

### Task Inventory

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| TASK-036 | Component A: Add routing disambiguation sections to all 13 skills | pending | high |
| TASK-037 | Component B: Framing vocabulary standardization (blocked by A/B testing) | pending | low |

### Task Links

- [TASK-036: Routing disambiguation sections](./TASK-036-routing-disambiguation-sections.md)
- [TASK-037: Framing vocabulary standardization](./TASK-037-framing-vocabulary-standardization.md)

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 2 |
| **Completed Tasks** | 0 |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-005: ADR Implementation](../EPIC-005-adr-implementation.md)

### References

- ADR-003: `orchestration/neg-prompting-20260227-001/phase-5/ADR-003-routing-disambiguation.md`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-28 | Claude | pending | Feature created |
