# TASK-005: Multi-Pattern Orchestration Validation

> **Type:** task
> **Status:** completed
> **Priority:** low
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** EN-008
> **Owner:** --
> **Effort:** 2h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Description](#description) | What needs to be done |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Related Items](#related-items) | Links |
| [History](#history) | Status changes |

---

## Summary

Validate detection and checkpoint system with cross-pollinated and fan-out/fan-in orchestration patterns. Completed as part of parent enabler EN-008.

---

## Description

**Addresses:** AC-7 (PASS with caveat)

AC-7 specifies: "Works with all orchestration patterns (sequential, cross-pollinated, fan-out/fan-in)." The current validation observed that detection hooks are pattern-agnostic (they fire on `UserPromptSubmit` regardless of orchestration shape), which earned a PASS verdict. However, only the sequential pattern was actually exercised during PROJ-004 validation. Cross-pollinated and fan-out/fan-in patterns have not been empirically tested.

Create test scenarios that exercise the detection and checkpoint system with ORCHESTRATION.yaml files representing cross-pollinated and fan-out/fan-in patterns.

---

## Acceptance Criteria

- [ ] Test with ORCHESTRATION.yaml representing a cross-pollinated pipeline pattern
- [ ] Test with ORCHESTRATION.yaml representing a fan-out/fan-in pattern
- [ ] Verify `CheckpointService._build_resumption_state()` correctly reads both pattern types
- [ ] Verify `ResumptionContextGenerator` correctly renders resumption context for both patterns
- [ ] Verify `StalenessDetector` correctly detects staleness for both pattern types
- [ ] Tests added to `tests/unit/` or `tests/integration/` as appropriate
- [ ] All existing 3652 tests still pass

---

## Implementation Notes

Create ORCHESTRATION.yaml test fixtures for each pattern:

1. **Cross-pollinated:** Two pipelines with barrier sections, cross-pollination artifacts
2. **Fan-out/fan-in:** Single start phase, 3 parallel agent phases, synthesis phase

The key insight from validation is that the hooks themselves are pattern-agnostic. The main risk is in `CheckpointService` and `ResumptionContextGenerator` -- they need to handle ORCHESTRATION.yaml files with different structural shapes (barriers, fan-out groups, etc.).

---

## Related Items

- Parent: [EN-008](./EN-008-context-resilience-hardening.md)
- Validation Report: AC-7 (PASS with caveat -- only sequential validated)
- Related: REC-4 (criticality-adjusted threshold validation)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | pending | Created from ST-003 validation AC-7 caveat. |
