# TASK-025: A/B Testing — Positive vs Negative vs Negative with Consequence

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-02-28
> **Parent:** EPIC-006
> **Owner:** orch-planner
> **Activity:** RESEARCH

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Summary

Design and execute A/B tests comparing three prompting approaches: positive-only framing, negative (bare prohibition), and negative with consequence (NPT-009 structured negation). Measure LLM compliance rates to validate the PROJ-014 research findings empirically.

---

## Content

### Description

The PROJ-014 research produced a taxonomy of 14 negative prompting patterns and concluded that NPT-009 (structured negation with consequence) outperforms bare prohibition (NPT-014). This task validates that conclusion through controlled A/B testing across representative prompting scenarios.

### Acceptance Criteria

- [x] Test design covering at least 3 representative constraint types (e.g., tool usage, output format, behavioral boundary) — 10 constraints selected, stratified across 3 tiers
- [x] Each variant tested: (A) positive-only, (B) negative bare prohibition, (C) negative with consequence — C1/C2/C3 across 3 models, 270 total invocations
- [x] Compliance rate measured for each variant across multiple runs — C1: 92.2%, C2: 97.8%, C3: 100.0%
- [x] Results documented with statistical significance assessment — McNemar p=0.016, pi_d=0.078, C4 gate PASS (0.954, 3 iterations)
- [x] Findings compared against PROJ-014 research predictions — structured negation (NPT-013) confirmed as equal-or-better; CONDITIONAL GO via PG-003

### Related Items

- Parent: [EPIC-006: Validation & Publication](./EPIC-006-validation-and-publication.md)
- Depends On: TASK-019 (C4 tournament — research findings)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Orchestration plan | Plan artifact | `orchestration/ab-testing-20260301-001/ORCHESTRATION_PLAN.md` |
| Orchestration state | State artifact | `orchestration/ab-testing-20260301-001/ORCHESTRATION.yaml` |
| Constraint selection | Design artifact | `orchestration/ab-testing-20260301-001/phase-0-design/constraint-selection.md` |
| Three-style rewrites | Design artifact | `orchestration/ab-testing-20260301-001/phase-0-design/three-style-rewrites.md` |
| Pressure scenarios | Design artifact | `orchestration/ab-testing-20260301-001/phase-0-design/pressure-scenarios.md` |
| Execution manifest | Tracking artifact | `orchestration/ab-testing-20260301-001/phase-0-design/execution-manifest.md` |
| 270 prompt files | Test artifact | `orchestration/ab-testing-20260301-001/phase-1-execution/prompts/` |
| 270 response files | Test artifact | `orchestration/ab-testing-20260301-001/phase-1-execution/responses/` |
| 297 scoring files | Scoring artifact | `orchestration/ab-testing-20260301-001/phase-2-scoring/scores/` |
| Compliance matrix | Analysis artifact | `orchestration/ab-testing-20260301-001/phase-2-scoring/compliance-matrix.md` |
| McNemar tables | Analysis artifact | `orchestration/ab-testing-20260301-001/phase-3-analysis/mcnemar-tables.md` |
| GO/NO-GO determination | Decision artifact | `orchestration/ab-testing-20260301-001/phase-3-analysis/go-no-go-determination.md` |
| 4 adversary gate reports | Quality artifact | `orchestration/ab-testing-20260301-001/adversary-gates/` |

### Verification

- [x] Acceptance criteria verified

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation |
| 2026-03-01 | In Progress | Orchestration scaffolding created. Workflow: ab-testing-20260301-001. |
| 2026-03-01 | Done | CONDITIONAL GO via PG-003. McNemar p=0.016, pi_d=0.078. C1: 92.2%, C2: 97.8%, C3: 100.0%. C4 gate PASS (0.954, 3 iterations). NPT-013 validated as equal-or-better. Unblocks TASK-035, TASK-037. |
