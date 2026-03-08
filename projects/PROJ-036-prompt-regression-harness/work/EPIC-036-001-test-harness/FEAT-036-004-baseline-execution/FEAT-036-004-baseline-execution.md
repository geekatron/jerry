# FEAT-036-004: Baseline Collection and Validation Execution

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
-->

> **Type:** feature
> **Status:** pending
> **Priority:** critical
> **Impact:** high
> **Created:** 2026-03-07T00:00:00Z
> **Due:** —
> **Completed:** —
> **Parent:** EPIC-036-001
> **Owner:** —
> **Target Sprint:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature scope and objectives |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children Stories/Enablers](#children-storiesenablers) | Story inventory  |
| [Progress Summary](#progress-summary) | Completion metrics |
| [Related Items](#related-items) | Dependencies and references |
| [History](#history) | Status changes |

---

## Summary

Execute real API-backed validation runs against the 5 target agents (ps-researcher, ps-analyst, ps-architect, ps-critic, adv-scorer), collect N=30 baseline scores per agent via `BaselineStore`, run MR tests at statistically powered N>=20, and perform Layer 4 statistical comparison with real baselines. The gap analysis (FEAT-036-002) confirmed that all infrastructure is built but zero real API calls have been made — the cost ledger shows all dashes, Phase 4 used synthetic `random.Random(42)` baselines, and Phase 3 MR tests ran at N=5 smoke level only.

**Value Proposition:**
- Transform the test harness from a validated-but-dry infrastructure into a live regression detection system
- Establish real baseline scores for all 5 agents enabling actual regression detection on prompt changes
- Validate that the G-Eval scoring, MR framework, and statistical pipeline produce meaningful results with real API data

---

## Benefit Hypothesis

**We believe that** executing real API-backed validation runs and collecting N=30 baselines per agent

**Will result in** a production-ready regression detection system that catches prompt quality degradation before it reaches users

**We will know we have succeeded when** all 5 agents have N=30 baseline records in `BaselineStore`, Layer 4 can detect a 0.05 composite score drop with p<0.05, and the CI/CD pipeline blocks PRs that regress agent quality

---

## Acceptance Criteria

### Definition of Done

- [ ] All 5 agents have real API-generated output files (Phase 1)
- [ ] All 5 agents have G-Eval composite scores from real outputs (Phase 2)
- [ ] MR-001 and MR-003 tested at N>=20 for ps-researcher and ps-architect (Phase 3)
- [ ] N=30 baseline records per agent stored via `BaselineStore.store()` (Phase 3.5)
- [ ] Layer 4 statistical comparison run with real baselines (Phase 4)
- [ ] CI/CD workflow wired to run regression checks on PR (Phase 5)
- [ ] Cost ledger populated with actual API token costs
- [ ] All Stories completed

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Phase 2 G-Eval scores for all 5 agents using real API-generated outputs | [ ] |
| AC-2 | Phase 3 MR tests at N>=20 pass tolerance thresholds (delta <= 0.05 for MR-001, <= 0.03 for MR-003) | [ ] |
| AC-3 | `BaselineStore` contains N=30 records per agent with composite scores | [ ] |
| AC-4 | Layer 4 produces PASS/BLOCK/WARNING verdicts from real baselines vs candidates | [ ] |
| AC-5 | GitHub Actions workflow triggers regression check on test harness PRs | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Total API cost for baseline collection <= $30 (estimated $15-30 per gap-synthesis.md CG-009) | [ ] |
| NFC-2 | Baseline collection completes within 4 hours wall-clock time | [ ] |

---

## Children Stories/Enablers

### Story/Enabler Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| STORY-036-001 | Story | Execute Real Validation Run (Phase 1-2) | pending | critical | 3 |
| STORY-036-002 | Story | Execute Real MR Tests at N>=20 (Phase 3) | pending | high | 5 |
| STORY-036-003 | Story | Baseline Population N=30 per Agent | pending | critical | 8 |
| STORY-036-004 | Story | Phase 4 Real Baseline Comparison | pending | high | 3 |
| STORY-036-005 | Story | CI/CD Wiring for Automated Regression | pending | high | 5 |

### Work Item Links

- [STORY-036-001: Execute Real Validation Run (Phase 1-2)](./STORY-036-001-validation-run-phase1-2.md)
- [STORY-036-002: Execute Real MR Tests at N>=20 (Phase 3)](./STORY-036-002-mr-tests-n20.md)
- [STORY-036-003: Baseline Population N=30 per Agent](./STORY-036-003-baseline-population.md)
- [STORY-036-004: Phase 4 Real Baseline Comparison](./STORY-036-004-phase4-real-baselines.md)
- [STORY-036-005: CI/CD Wiring for Automated Regression](./STORY-036-005-ci-cd-wiring.md)

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Stories** | 5 |
| **Completed Stories** | 0 |
| **Total Effort (points)** | 24 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-036-001: Four-Layer Composite Test Harness](../EPIC-036-001-test-harness.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | FEAT-036-001 | Test harness infrastructure (building blocks in jerry/testing/) |
| Depends On | FEAT-036-002 | Gap analysis identifying CG-009 baseline population gap |
| Depends On | FEAT-036-003 | Gap closure remediation (P0 blockers resolved) |
| Informed By | CG-009 | Canonical gap: baseline population (Sprint 3 in gap-synthesis.md roadmap) |
| Informed By | execution-prompt-v1.md | 5-phase execution design for validation runs |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-07 | Claude | pending | Feature created; addresses the gap between built infrastructure and zero real API execution identified in FEAT-036-002 gap analysis |
