# EN-819: SSOT Consistency & Template Resilience

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-15 (Claude)
PURPOSE: Consolidate REVISE band to SSOT and add template resilience
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-15
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-010
> **Owner:** —
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Business Value](#business-value) | How this enabler supports parent feature delivery |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Current completion status |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Consolidate REVISE band definition to quality-enforcement.md SSOT, update all templates to reference SSOT instead of locally defining the band, define malformed template fallback behavior, and add resilience testing.

---

## Problem Statement

The REVISE band (0.85-0.91) is currently defined independently in multiple strategy templates rather than sourced from quality-enforcement.md (the SSOT). This creates a consistency risk where templates could drift from the authoritative definition. Additionally, there is no defined behavior for when a malformed template is encountered during execution.

---

## Business Value

Consolidating the REVISE band to SSOT supports FEAT-010 by eliminating a class of consistency errors identified in the C4 tournament. When templates define scoring bands locally, any update to quality-enforcement.md creates silent drift. Malformed template fallback behavior ensures graceful degradation rather than undefined behavior during execution.

### Features Unlocked

- Enables single-point scoring band updates that propagate consistently across all templates
- Provides defined failure mode for malformed templates instead of undefined execution behavior

---

## Technical Approach

1. Move REVISE band definition (0.85-0.91) from templates to quality-enforcement.md as SSOT
2. Update all templates to reference REVISE band from SSOT instead of defining locally
3. Define malformed template fallback behavior in adv-executor.md — emit CRITICAL finding and halt
4. Add E2E test for malformed template detection

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Move REVISE band definition to quality-enforcement.md SSOT | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Update all templates to reference REVISE band from SSOT | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Define malformed template fallback behavior in adv-executor.md | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Add E2E test for malformed template detection | pending | DEVELOPMENT | ps-architect |

---

## Progress Summary

### Status Overview

```
[░░░░░░░░░░░░░░░░░░░░] 0% (0/4 tasks)
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 4 |
| Completed | 0 |
| In Progress | 0 |
| Pending | 4 |
| Blocked | 0 |
| Completion | 0% |

---

## Acceptance Criteria

### Definition of Done
- [ ] REVISE band defined in quality-enforcement.md SSOT only
- [ ] All 10 templates reference SSOT for REVISE band (no local definitions)
- [ ] Malformed template fallback defined: emit CRITICAL + halt
- [ ] E2E test validates malformed template detection
- [ ] All acceptance criteria verified via creator-critic-revision cycle
- [ ] Quality gate passed (>= 0.92)

### Technical Criteria
| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | quality-enforcement.md contains authoritative REVISE band definition | [ ] |
| TC-2 | Zero local REVISE band definitions in templates | [ ] |
| TC-3 | adv-executor.md specifies CRITICAL finding + halt for malformed templates | [ ] |
| TC-4 | E2E tests pass (`uv run pytest tests/e2e/`) | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | — | — | Pending |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All technical criteria verified
- [ ] Quality gate score >= 0.92
- [ ] Creator-critic-revision cycle completed (minimum 3 iterations)
- [ ] No regressions introduced

---

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-010: Tournament Remediation](../FEAT-010-tournament-remediation.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-15 | Claude | pending | Enabler created from FEAT-009 C4 Tournament findings. |
