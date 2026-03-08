# EPIC-036-001: Four-Layer Composite Test Harness

<!--
TEMPLATE: Epic
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.2
-->

> **Type:** epic
> **Status:** in_progress
> **Priority:** critical
> **Impact:** high
> **Created:** 2026-03-06T00:00:00Z
> **Due:** —
> **Completed:** —
> **Parent:** PROJ-036
> **Owner:** —
> **Target Quarter:** FY26-Q1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Epic scope and objectives |
| [Children Features/Capabilities](#children-featurescapabilities) | Feature inventory |
| [Progress Summary](#progress-summary) | Overall epic progress |
| [Related Items](#related-items) | Dependencies and references |
| [History](#history) | Status changes |

---

## Summary

Implement the Four-Layer Composite Test Harness architecture defined in PROJ-035 ADR-001. This harness enables safe prompt refactoring and regression detection across Jerry's 67 agent definitions by combining promptfoo CI/CD gating, DeepEval evaluation metrics, metamorphic relation assertions, and statistical comparison (Wilcoxon signed-rank + Wilson score intervals).

**Key Objectives:**
- Layer 1: promptfoo CI/CD regression gate (GitHub Action + YAML test cases)
- Layer 2: DeepEval pytest evaluation backend (debiased LLM-as-Judge)
- Layer 3: Metamorphic relation framework (5 universal MRs, oracle-safe assertions)
- Layer 4: Statistical comparison engine (Wilcoxon signed-rank + Wilson score intervals)

---

## Children Features/Capabilities

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-036-001 | Test Harness Implementation | in_progress | critical | 0% |
| FEAT-036-002 | Gap Analysis: Test Harness Integration Layer | in_progress | critical | 0% |
| FEAT-036-003 | Gap Closure Remediation | pending | critical | 0% |

### Feature Links

- [FEAT-036-001: Test Harness Implementation](./FEAT-036-001-implementation/FEAT-036-001-implementation.md)
- [FEAT-036-002: Gap Analysis: Test Harness Integration Layer](./FEAT-036-002-gap-analysis/FEAT-036-002-gap-analysis.md)
- [FEAT-036-003: Gap Closure Remediation](./FEAT-036-003-gap-closure/FEAT-036-003-gap-closure.md)

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Features** | 3 |
| **Completed Features** | 0 |
| **In Progress Features** | 2 |
| **Pending Features** | 1 |
| **Feature Completion %** | 0% |

---

## Related Items

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Architecture Source | PROJ-035 ADR-001 | ACCEPTED architecture decision defining the Four-Layer Composite |
| Shared Infrastructure | PROJ-017 ADR-002 | Complementary quality framework; shared jerry/testing/stats.py |
| Research Basis | PROJ-035 FEAT-035-001 | 8-phase research pipeline producing the architecture recommendation |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-06 | Claude | in_progress | Epic created for implementation of ACCEPTED ADR-001 |
