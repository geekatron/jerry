# EN-711: E2E Integration Testing

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Create comprehensive end-to-end integration tests for the quality framework
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-02-14
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-008
> **Owner:** —
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Design Source](#design-source) | Traceability to EPIC-002 design artifacts |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Create comprehensive end-to-end integration tests validating cross-component interactions across all enforcement layers (L1-L5). Validates that the complete quality framework works as an integrated system, catching interaction failures that unit tests for individual layers would miss.

**Value Proposition:**
- Validates that the 5-layer quality architecture works as a coherent system
- Catches integration failures between hooks, rules, skills, and CI enforcement
- Provides regression protection against quality framework degradation
- Establishes performance benchmarks for token budget and latency
- Creates a comprehensive test suite runnable via `uv run pytest tests/e2e/`

**Technical Scope:**
- Cross-layer interaction tests (L1 hooks through L5 CI)
- Hook enforcement end-to-end tests (PreToolUse, UserPromptSubmit, SessionStart)
- Rule compliance validation tests (quality-enforcement.md referenced correctly)
- Session context injection verification
- Skill adversarial mode integration tests (PS, NSE, ORCH)
- Performance benchmarks (token budget, latency)

---

## Problem Statement

Individual enforcement layers (hooks, rules, skills, CI) may each pass their own tests but fail when interacting as a system. Without end-to-end integration testing, the quality framework has no validation that the complete enforcement pipeline works correctly. Specific risks:

1. **Integration gaps** -- A hook may correctly inject context that a rule file cannot parse, creating a silent enforcement failure.
2. **Cross-layer conflicts** -- Rule file optimization (EN-702) may produce rules that conflict with hook behavior (EN-703/EN-705), creating inconsistent enforcement.
3. **Regression vulnerability** -- Changes to one layer may break another layer's assumptions without any test detecting the regression.
4. **Performance degradation** -- The combined token cost of all enforcement layers may exceed budget without aggregate measurement.

---

## Technical Approach

1. **Create cross-layer interaction tests** -- Write tests that exercise the full enforcement pipeline: session start (L2) -> rule loading (L3) -> hook invocation (L1) -> skill adversarial mode (L4) -> CI verification (L5).
2. **Create hook enforcement E2E tests** -- Test each hook (PreToolUse, UserPromptSubmit, SessionStart) in realistic scenarios with actual file system state, verifying correct enforcement behavior.
3. **Create rule compliance validation tests** -- Verify that all rules reference the SSOT (quality-enforcement.md) correctly and that constant values are consistent across all enforcement points.
4. **Create session context injection tests** -- Verify that session start hook correctly injects quality context and that downstream components (rules, skills) correctly consume it.
5. **Create skill adversarial mode tests** -- Verify that PS, NSE, and ORCH skills correctly activate adversarial mode when triggered and produce quality-scored outputs.
6. **Create performance benchmarks** -- Measure token consumption and latency for the complete enforcement pipeline, establishing baseline benchmarks.

---

## Design Source

| Source | Content Used |
|--------|-------------|
| EPIC-002 EN-306 | Adversarial integration testing design, cross-layer test scenarios |
| EPIC-002 EN-406 | Enforcement integration testing design (204 test cases), test categorization |
| ADR-EPIC002-002 | 5-layer architecture (L1-L5), layer interaction specifications |
| EPIC-002 Final Synthesis | Integration validation requirements, performance benchmarks |

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Create cross-layer interaction tests (L1-L5) | pending | TESTING | nse-verification |
| TASK-002 | Create hook enforcement end-to-end tests | pending | TESTING | nse-verification |
| TASK-003 | Create rule compliance validation tests | pending | TESTING | nse-validation |
| TASK-004 | Create session context injection verification tests | pending | TESTING | nse-verification |
| TASK-005 | Create skill adversarial mode integration tests | pending | TESTING | nse-verification |
| TASK-006 | Create performance benchmarks (token budget, latency) | pending | TESTING | ps-analyst |
| TASK-007 | Adversarial review of test suite completeness | pending | TESTING | ps-critic |
| TASK-008 | Creator revision based on review findings | pending | DEVELOPMENT | ps-architect |

### Task Dependencies

```
TASK-001 (cross-layer) ──┐
TASK-002 (hooks) ────────┤
TASK-003 (rules) ────────├──> TASK-007 (adversarial review) ──> TASK-008 (revision)
TASK-004 (session) ──────┤
TASK-005 (skills) ───────┤
TASK-006 (benchmarks) ───┘
```

---

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Cross-layer interaction tests (L1-L5) implemented | [ ] |
| AC-2 | Hook enforcement end-to-end tests implemented | [ ] |
| AC-3 | Rule compliance validation tests implemented | [ ] |
| AC-4 | Session context injection verification tests implemented | [ ] |
| AC-5 | Skill adversarial mode integration tests implemented | [ ] |
| AC-6 | Performance benchmarks (token budget, latency) established | [ ] |
| AC-7 | All tests pass via `uv run pytest tests/e2e/` | [ ] |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-008: Quality Framework Implementation](../FEAT-008-quality-framework-implementation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-701 | SSOT must exist as the source of truth for test assertions |
| depends_on | EN-707 | PS adversarial mode must be implemented for skill integration tests |
| depends_on | EN-708 | NSE adversarial mode must be implemented for skill integration tests |
| depends_on | EN-709 | ORCH adversarial mode must be implemented for skill integration tests |
| depends_on | EN-710 | CI pipeline must be configured for L5 integration tests |
| related_to | EPIC-002 EN-306 | Adversarial integration testing design (source material) |
| related_to | EPIC-002 EN-406 | Enforcement integration testing design (source material) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created with 8-task decomposition. Comprehensive E2E integration testing validating the complete quality framework across all enforcement layers (L1-L5). |
