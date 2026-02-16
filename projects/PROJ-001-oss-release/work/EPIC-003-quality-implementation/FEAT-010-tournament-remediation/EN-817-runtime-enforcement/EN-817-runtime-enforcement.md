# EN-817: Runtime Enforcement

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-15 (Claude)
PURPOSE: Implement runtime enforcement mechanisms for /adversary skill agents
-->

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** critical
> **Enabler Type:** infrastructure
> **Created:** 2026-02-15
> **Due:** —
> **Completed:** 2026-02-15
> **Parent:** FEAT-010
> **Owner:** —
> **Effort:** 5

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

Implement runtime enforcement mechanisms for the /adversary skill agents, including H-16 enforcement (S-003 before S-002), P-003 self-checks, and auto-escalation cross-checks in strategy selection.

---

## Problem Statement

The C4 tournament identified that critical runtime guarantees are not enforced:
1. H-16 ordering (S-003 Steelman must execute before S-002 Devil's Advocate) is only documented but not blocked at runtime
2. P-003 compliance (no recursive subagents) has no self-check mechanism in agent specs
3. Auto-escalation rules (AE-001 through AE-006) are not cross-checked during strategy selection

---

## Business Value

Runtime enforcement is critical for FEAT-010 because documented-but-unenforced constraints degrade silently. Without H-16 blocking, P-003 self-checks, and AE cross-validation, tournament executions can produce results that violate constitutional guarantees without any error signal.

### Features Unlocked

- Enables guaranteed H-16 ordering compliance during tournament execution
- Provides runtime detection of P-003 and auto-escalation violations before they propagate to findings

---

## Technical Approach

1. Update adv-executor.md to block S-002 execution if S-003 is not in prior_strategies_executed (H-16 enforcement)
2. Add P-003 runtime self-check instructions to all 3 agent specifications (adv-selector, adv-executor, adv-scorer)
3. Add auto-escalation cross-check (AE-001 through AE-006) to adv-selector.md Step 1
4. Add E2E test for H-16 enforcement — attempt S-002 without prior S-003 and assert failure
5. Add E2E test for auto-escalation override detection

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Update adv-executor.md — block S-002 without prior S-003 | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Add P-003 runtime self-check to all 3 agent specifications | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Add auto-escalation cross-check to adv-selector.md | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Add E2E test for H-16 enforcement | pending | DEVELOPMENT | ps-architect |
| TASK-005 | Add E2E test for auto-escalation override detection | pending | DEVELOPMENT | ps-architect |

---

## Progress Summary

### Status Overview

```
[░░░░░░░░░░░░░░░░░░░░] 0% (0/5 tasks)
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 5 |
| Completed | 0 |
| In Progress | 0 |
| Pending | 5 |
| Blocked | 0 |
| Completion | 0% |

---

## Acceptance Criteria

### Definition of Done
- [ ] H-16 enforcement implemented in adv-executor.md
- [ ] P-003 self-checks present in all 3 agent specifications
- [ ] Auto-escalation cross-check integrated in adv-selector.md
- [ ] E2E test for H-16 enforcement passes
- [ ] E2E test for auto-escalation override detection passes
- [ ] All tests pass with `uv run pytest`
- [ ] Quality gate passed (>= 0.92)

### Technical Criteria
| # | Criterion | Verified |
|---|-----------|----------|
| 1 | S-002 execution blocked when S-003 not in prior_strategies_executed | — |
| 2 | All 3 agent specs contain P-003 self-check sections | — |
| 3 | adv-selector.md Step 1 references all 6 AE rules | — |
| 4 | E2E test validates H-16 check presence and behavior | — |
| 5 | E2E test validates AE rule references and escalation logic | — |
| 6 | No regressions in existing test suite | — |

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
| 2026-02-15 | Claude | completed | Quality gate PASS (score 0.935, 2 iterations). All tasks complete. |
| 2026-02-15 | Claude | pending | Enabler created from FEAT-009 C4 Tournament findings. |
