# EPIC-003: CI Pipeline Optimization — Remove Pip Matrix, Fix Supply Chain Gaps, Consolidate Jobs

> **Type:** epic
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-13
> **Parent:** PROJ-024
> **Branch:** `feat/PROJ-024-tactical-work-3`
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Epic scope and motivation |
| [Children Features/Capabilities](#children-featurescapabilities) | Work streams decomposed from this epic |
| [Progress Summary](#progress-summary) | Current status of all work items |
| [Work Items](#work-items) | Task decomposition table |
| [Dependency Graph](#dependency-graph) | Task dependency visualization |
| [Execution Phases](#execution-phases) | Phased execution plan |

---

## Children Features/Capabilities

| Work Stream | Items | Description |
|-------------|-------|-------------|
| Security Hardening | TASK-017, TASK-018, TASK-021, TASK-022 | Migrate jobs to uv, fix pip-audit scope, restrict permissions and triggers |
| Job Consolidation | TASK-016, TASK-019, TASK-020 | Remove pip matrix, merge validation and static-analysis jobs |

---

## Summary

The Jerry CI pipeline has 29 jobs per PR run. A cross-skill assessment (eng-devsecops, problem-solving, red-team, user-experience) identified 7 remediations that reduce this to ~19 jobs while closing 3 supply chain gaps, eliminating 4 H-05 violations, and reducing compute cost by ~30 min per run.

**Assessment reports** are stored in `research/` within this epic directory, copied from the original PROJ-030 review location.

| Metric | Before | After |
|--------|--------|-------|
| Total jobs | 29 | ~19 |
| H-05 violations | 4 | 0 |
| Supply chain gaps | 3 (type-check live PyPI, pip-audit scope, pip matrix) | 0 |
| Compute per run | ~45 min | ~15 min |
| PR status checks | 29 | ~19 |

---

## Progress Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1 — Security Hardening | TASK-017, TASK-018, TASK-021, TASK-022 | completed |
| Phase 2 — Consolidation | TASK-016, TASK-019, TASK-020 | pending |

---

## Work Items

| ID | Type | Title | Status | Phase | Dependencies |
|----|------|-------|--------|-------|--------------|
| TASK-016 | Task | Remove pip test matrix (8 jobs) | pending | 2 | TASK-017 |
| TASK-017 | Task | Migrate lint, type-check, security to uv | completed | 1 | -- |
| TASK-018 | Task | Fix pip-audit to scan full dependency tree | completed | 1 | -- |
| TASK-019 | Task | Consolidate 6 validation jobs into 1 | pending | 2 | -- |
| TASK-020 | Task | Merge lint + type-check into static-analysis | pending | 2 | TASK-017 |
| TASK-021 | Task | Scope pull-requests:write to coverage-report only | completed | 1 | -- |
| TASK-022 | Task | Restrict push trigger to protected branches only | completed | 1 | -- |

---

## Dependency Graph

```mermaid
graph TD
    TASK-017[TASK-017: Migrate to uv] --> TASK-016[TASK-016: Remove pip matrix]
    TASK-017 --> TASK-020[TASK-020: Merge static-analysis]
    TASK-018[TASK-018: Fix pip-audit scope]
    TASK-019[TASK-019: Consolidate validations]
    TASK-021[TASK-021: Scope PR write permission]
    TASK-022[TASK-022: Restrict push trigger]

    subgraph "Phase 1 — Security Hardening"
        TASK-017
        TASK-018
        TASK-021
        TASK-022
    end

    subgraph "Phase 2 — Consolidation"
        TASK-016
        TASK-019
        TASK-020
    end
```

---

## Execution Phases

### Phase 1 — Security Hardening (independent, parallelizable)

| Task | Description |
|------|-------------|
| TASK-017 | Migrate lint, type-check, security jobs from pip to uv |
| TASK-018 | Fix pip-audit to scan full dependency tree |
| TASK-021 | Scope pull-requests:write to coverage-report job only |
| TASK-022 | Restrict push trigger to protected branches (main, master) |

These 4 tasks are independent and can be executed in parallel. They address security hardening and H-05 compliance with no functional changes to pipeline behavior.

### Phase 2 — Consolidation (after Phase 1 dependencies)

| Task | Description | Dependency |
|------|-------------|------------|
| TASK-016 | Remove pip test matrix (8 jobs) | TASK-017 must complete first |
| TASK-019 | Consolidate 6 validation jobs into 1 | Independent |
| TASK-020 | Merge lint + type-check into static-analysis | TASK-017 must complete first |

Phase 2 tasks perform job consolidation. TASK-016 and TASK-020 depend on TASK-017 (uv migration) completing first. TASK-019 is independent.

All 7 tasks can be delivered in a single PR.
