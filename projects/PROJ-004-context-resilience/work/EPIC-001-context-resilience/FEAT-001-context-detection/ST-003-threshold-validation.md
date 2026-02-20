# ST-003: Threshold Validation + Calibration Documentation

> **Type:** story
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 4h (timebox)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Scope |
| [Acceptance Criteria](#acceptance-criteria) | BDD scenarios and checklist |
| [Dependencies](#dependencies) | Relationships |
| [History](#history) | Status changes |

---

## Summary

Run a monitored session with the detection system active against a workflow with a different profile than the PROJ-001 FEAT-015 baseline. Collect per-operation token costs and fill trajectory. Compare against PROJ-001 calibration data. Document the calibration protocol.

---

## Acceptance Criteria

### BDD Scenarios (pytest-bdd)

```gherkin
Feature: Threshold calibration across workflow types

  Scenario: Monitored session completes with data collection
    Given the context monitoring system is operational (EN-006, EN-007)
    When a monitored session runs a non-PROJ-001 workflow
    Then per-operation token cost data should be collected
    And fill trajectory should be recorded

  Scenario: Calibration protocol document created
    When the calibration is complete
    Then docs/knowledge/context-resilience/calibration-protocol.md should exist
    And it should contain: when to recalibrate, how to collect data, how to interpret results
```

### Acceptance Checklist

- [ ] Monitored session completed against non-PROJ-001 workflow
- [ ] Per-operation token cost data collected
- [ ] Fill trajectory compared against PROJ-001 baseline
- [ ] Threshold adjustment recommendations documented
- [ ] Calibration protocol at `docs/knowledge/context-resilience/calibration-protocol.md`
- [ ] Document includes: recalibration triggers, data collection method, result interpretation

---

## Dependencies

**Depends On:** EN-002, EN-003, EN-004, EN-006, EN-007 (system must be operational)

**Enables:** Nothing directly

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Story created from CWI-09. |
