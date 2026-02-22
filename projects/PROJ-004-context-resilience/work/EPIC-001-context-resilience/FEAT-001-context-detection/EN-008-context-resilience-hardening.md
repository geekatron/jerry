# EN-008: Context Resilience Hardening

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 14-20h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | Features unlocked |
| [Children (Tasks)](#children-tasks) | Task inventory |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Technical Approach](#technical-approach) | Implementation approach |
| [Dependencies](#dependencies) | Relationships |
| [History](#history) | Status changes |

---

## Summary

Address the 5 PARTIAL acceptance criteria items identified during FEAT-001 validation (ST-003) plus a critical configuration gap discovered post-validation. These items represent hardening work that moves the context resilience system from "functionally complete" to "production-grade."

**Technical Scope:**
- Structured checkpoint field extraction from ORCHESTRATION.yaml (TASK-001)
- WORKTRACKER.md auto-injection into resumption context (TASK-002)
- Checkpoint write-back to ORCHESTRATION.yaml resumption section (TASK-003)
- Automated E2E integration test for exhaust-clear-resume-complete (TASK-004)
- Multi-pattern orchestration validation (TASK-005)
- Context window size configuration (TASK-006) -- config key exists but disconnected; different subscriptions/models have different windows

---

## Problem Statement

FEAT-001 validation (ST-003) produced 20 PASS, 5 PARTIAL, and 1 DEFERRED results. The 5 PARTIAL items represent gaps where the implementation is functional but not fully meeting the acceptance criteria as specified. These are tracked as recommendations REC-1 through REC-4 in the validation report.

**Source:** `projects/PROJ-004-context-resilience/orchestration/feat001-impl-20260220-001/impl/phase-6-validation/st-003-exec/validation-report.md`

---

## Business Value

Completing these tasks promotes all 5 PARTIAL verdicts to PASS, achieving full FEAT-001 acceptance criteria compliance.

### Features Unlocked

- Structured checkpoint data enables downstream tooling to parse checkpoint state without YAML text scanning
- WORKTRACKER.md injection provides richer resumption context for new sessions
- Automated E2E test prevents regression in the detection-checkpoint-resumption pipeline

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| [TASK-001](./TASK-001-structured-checkpoint-fields.md) | Structured checkpoint field extraction | pending | 2h | -- |
| [TASK-002](./TASK-002-worktracker-resumption-injection.md) | WORKTRACKER.md auto-injection in resumption | pending | 1.5h | -- |
| [TASK-003](./TASK-003-checkpoint-yaml-writeback.md) | Checkpoint write-back to ORCHESTRATION.yaml | pending | 2h | -- |
| [TASK-004](./TASK-004-e2e-integration-test.md) | Automated E2E integration test | pending | 3h | -- |
| [TASK-005](./TASK-005-multi-pattern-validation.md) | Multi-pattern orchestration validation | pending | 2h | -- |
| [TASK-006](./TASK-006-context-window-configuration.md) | Context window size detection and configuration | pending | 6-8h | -- |

---

## Acceptance Criteria

### Definition of Done

- [ ] All 6 child tasks completed
- [ ] DoD-4 promoted from PARTIAL to PASS (structured fields)
- [ ] DoD-5 promoted from PARTIAL to PASS (WORKTRACKER.md injection)
- [ ] AC-4 promoted from PARTIAL to PASS (checkpoint write-back)
- [ ] DoD-7/NFC-1 promoted from PARTIAL to PASS (automated E2E test)
- [ ] AC-7 promoted from PARTIAL to PASS (multi-pattern validation)
- [ ] All existing 3652 tests still pass (no regression)
- [ ] Context window size configurable per subscription/model (TASK-006)
- [ ] 90% line coverage maintained (H-21)

---

## Technical Approach

Address the 5 PARTIAL acceptance criteria items identified during FEAT-001 validation (ST-003) plus a critical configuration gap. Hardening work moves the context resilience system from functionally complete to production-grade through structured checkpoint fields, WORKTRACKER.md injection, YAML write-back, E2E testing, multi-pattern validation, and context window configuration.

---

## Dependencies

**Depends On:** EN-001 through EN-007 (all complete), ST-003 validation report

**Enables:** Full FEAT-001 acceptance criteria compliance

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Enabler created from ST-003 validation report. 5 PARTIAL items tracked as TASK-001 through TASK-005. |
| 2026-02-20 | Claude | pending | TASK-006 added: context window size hardcoded to 200K, config key exists but disconnected. Different subscriptions/models have different context windows; auto-detection insufficient. |
