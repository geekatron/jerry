# FEAT-036-001: Test Harness Implementation

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
-->

> **Type:** feature
> **Status:** in_progress
> **Priority:** critical
> **Impact:** high
> **Created:** 2026-03-06T00:00:00Z
> **Due:** —
> **Completed:** —
> **Parent:** EPIC-036-001
> **Owner:** —
> **Target Sprint:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature scope and value proposition |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits |
| [Acceptance Criteria](#acceptance-criteria) | Verification criteria |
| [Children Stories/Enablers](#children-storiesenablers) | Work decomposition |
| [Progress Summary](#progress-summary) | Feature progress |
| [Related Items](#related-items) | Dependencies and references |
| [History](#history) | Status changes |

---

## Summary

Implement the Four-Layer Composite Test Harness architecture defined in PROJ-035 ADR-001 (ACCEPTED). Covers requirements derivation, system design, baseline generation, behavioral contracts, all four implementation layers, CI/CD integration, security assessment, V&V, test suite, and final engineering review.

**Value Proposition:**
- Automated prompt regression detection on every PR modifying agent definitions
- Three-tier evaluation: Smoke ($0), Standard (~$2), Full (~$5-8)
- Statistical rigor: Wilcoxon signed-rank with N >= 20 enforcement
- Oracle-safe assertions: metamorphic relations instead of exact-output comparison

---

## Benefit Hypothesis

**We believe that** implementing the Four-Layer Composite test harness from ADR-001

**Will result in** automated, statistically valid prompt regression detection that blocks PRs causing quality degradation

**We will know we have succeeded when** agent definition changes are automatically validated via CI/CD with regression classification (NO_REGRESSION / MARGINAL / REGRESSION) before merge

---

## Acceptance Criteria

- [ ] Requirements derived from ADR-001 with FMEA traceability (Phase 1A)
- [ ] System design with hexagonal architecture and STRIDE threat model (Phase 1B)
- [ ] Baseline protocol and test prompts for 5+ agents across 3+ cognitive modes (Phase 1C)
- [ ] Behavioral contracts with metamorphic relation tolerances (Phase 1D)
- [ ] Layer 1: promptfoo GitHub Action with three-tier workflow modes (Phase 3A)
- [ ] Layer 2: DeepEval evaluation backend with debiased LLM-as-Judge (Phase 3B)
- [ ] Layer 3: 5 universal metamorphic relations as custom DeepEval metrics (Phase 3C)
- [x] Layer 4: Statistical engine with Wilcoxon, Wilson, Bonferroni (Phase 3D) — **complete** (71/71 verification checks pass)
- [ ] CI/CD pipeline with Smoke/Standard/Full modes (Phase 3E)
- [ ] Security assessment of the harness itself (Phase 5A)
- [ ] V&V execution against requirements (Phase 5B)
- [ ] Test suite with 90% coverage, property-based tests (Phase 5C)
- [ ] All deliverables pass C4 quality gates (>= 0.95 S-014 weighted composite)
- [ ] Final dual gate: adversarial + NASA SE technical review (Phase 8)

---

## Children Stories/Enablers

### Story/Enabler Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| EN-036-001 | enabler | Model Flexibility for G-Eval Judge and Agent Execution | completed | medium | M |

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Stories** | 0 |
| **Completed Stories** | 0 |
| **Total Enablers** | 1 |
| **Completed Enablers** | 1 |
| **Completion %** | 100% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-036-001: Four-Layer Composite Test Harness](../EPIC-036-001-test-harness.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Architecture Source | PROJ-035 ADR-001 | ACCEPTED architecture decision |
| Shared Module | PROJ-017 jerry/testing/stats.py | Shared statistical module |
| GitHub Issue | [#145](https://github.com/geekatron/jerry/issues/145) | Implementation tracking |

### Artifacts

| Phase | Artifact | Path |
|-------|----------|------|
| Orchestration | Plan | `projects/PROJ-036-prompt-regression-harness/orchestration/harness-impl-20260306-001/ORCHESTRATION_PLAN.md` |
| Phase 3D | Stream 3D implementation report | `projects/PROJ-036-prompt-regression-harness/work/stream-3d-layer4-stats.md` |
| Phase 3D | Domain types | `jerry/testing/types.py` |
| Phase 3D | Statistical functions | `jerry/testing/stats.py` |
| Phase 3D | Baseline store | `jerry/testing/baselines/store.py` |
| Phase 3D | Report generator | `jerry/testing/reports/generator.py` |
| Phase 3D | Pipeline orchestrator | `jerry/testing/layer4_stats.py` |
| Phase 3D | Verification script | `projects/PROJ-036-prompt-regression-harness/work/verify_layer4.py` |
| Phase 7B | Cross-stream implementation synthesis (8 patterns, dependency map, quality trajectory) | `projects/PROJ-036-prompt-regression-harness/synthesis/implementation-synthesis.md` |
| Phase 7B | Consolidated risk register (28 items, 2 pre-production blockers, FMEA trajectory 1823->382) | `projects/PROJ-036-prompt-regression-harness/synthesis/risk-register-updated.md` |
| Phase 7B | Operational readiness assessment (NOT READY FOR PRODUCTION; 7-stage deployment sequence) | `projects/PROJ-036-prompt-regression-harness/synthesis/operational-readiness.md` |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-06 | Claude | in_progress | Feature created for 8-group implementation pipeline |
| 2026-03-07 | eng-backend | in_progress | Stream 3D (Phase 3D) complete: 7 modules, 71/71 verification checks pass, ruff clean |
| 2026-03-07 | ps-synthesizer | in_progress | Stream 7B (Cross-Synthesis) complete: 3 synthesis deliverables persisted; 8 cross-stream patterns (PAT-001–PAT-008); 28-item risk register (2 pre-production blockers: RR-001 input sanitization CVSS 6.5, RR-002 Docker digest CVSS 7.4); operational readiness verdict: NOT READY FOR PRODUCTION |
