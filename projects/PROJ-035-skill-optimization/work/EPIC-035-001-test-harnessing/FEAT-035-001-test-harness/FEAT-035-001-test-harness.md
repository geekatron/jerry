# FEAT-035-001: Test Harness for LLM Prompt Evaluation and Safe Refactoring

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
-->

> **Type:** feature
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-06T00:00:00Z
> **Due:** —
> **Completed:** —
> **Parent:** EPIC-035-001
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

Build a comprehensive test harness that enables safe prompt refactoring and migration across LLM model versions and providers, with regression testing, behavioral evaluation, and statistical rigor.

**Value Proposition:**
- Safe prompt refactoring with behavioral regression detection
- Migration confidence across model versions and providers
- Evidence-based quality measurement for LLM prompt outputs

---

## Benefit Hypothesis

**We believe that** building a test harness for LLM prompt evaluation with regression testing and statistical rigor

**Will result in** safe, confident prompt refactoring and model migration without behavioral degradation

**We will know we have succeeded when** prompt changes can be validated against behavioral baselines with quantified confidence intervals before deployment

---

## Acceptance Criteria

- [x] Research phase produces verified survey of historical testing methodologies, industry frameworks, agent SDKs, and innovation approaches (4 deliverables, all externally sourced)
- [x] Cross-pollination synthesis maps historical methodologies to LLM testing equivalents with framework capability matrix
- [x] Analytical evaluation scores candidate approaches across 6 dimensions with FMEA risk analysis
- [x] Architecture Decision Record (ADR-001) recommends test harness architecture with evidence-traced rationale
- [x] All deliverables pass S-014 quality gate (>= 0.92 weighted composite) and NSE technical review

---

## Children Stories/Enablers

### Story/Enabler Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| — | — | To be decomposed after ADR-001 acceptance | — | — | — |

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Stories** | 0 |
| **Completed Stories** | 0 |
| **Total Enablers** | 0 |
| **Completed Enablers** | 0 |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-035-001: Test Harnessing](../EPIC-035-001-test-harnessing.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Builds On | PROJ-017 ADR-002 | Prior evaluation recommending promptfoo extension architecture |
| GitHub Issue | [#145](https://github.com/geekatron/jerry/issues/145) | Implementation tracking for Four-Layer Composite test harness |

### Artifacts

| Phase | Artifact | Path |
|-------|----------|------|
| Phase 1A | Historical Testing Methodologies Survey | `projects/PROJ-035-skill-optimization/research/historical-testing-methodologies.md` |
| Phase 1B | Industry Frameworks Survey | `projects/PROJ-035-skill-optimization/research/industry-frameworks-survey.md` |
| Phase 1C | Agent SDK Evaluation | `projects/PROJ-035-skill-optimization/research/agent-sdk-evaluation.md` |
| Phase 1D | Innovation Frameworks Survey | `projects/PROJ-035-skill-optimization/research/innovation-frameworks.md` |
| Phase 3 | Cross-Pollination Synthesis | `projects/PROJ-035-skill-optimization/analysis/cross-pollination-synthesis.md` |
| Phase 5 | Test Harness Evaluation (Trade-off + FMEA) | `projects/PROJ-035-skill-optimization/analysis/test-harness-evaluation.md` |
| Phase 7 | ADR-001 Test Harness Architecture | `projects/PROJ-035-skill-optimization/decisions/ADR-001-test-harness-architecture.md` |
| Phase 8 | Gate A Score (Iteration 2) | `projects/PROJ-035-skill-optimization/work/test-harness/adv/phase-7-scores/gate-a-adv-score-iter2.md` |
| Phase 8 | Gate B NSE Technical Review | `projects/PROJ-035-skill-optimization/work/test-harness/adv/phase-7-scores/gate-b-nse-review.md` |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-06 | Claude | in_progress | Feature created; 8-phase research pipeline planned |
| 2026-03-06 | ps-analyst | in_progress | Phase 5 analysis complete: test-harness-evaluation.md; Four-Layer Composite recommended (score 4.65/5.00); 10-item FMEA; PROJ-017 ADR-002 relationship mapped |
| 2026-03-06 | ps-architect | in_progress | Phase 7 ADR-001 complete: Four-Layer Composite recommended (Option B, 4.45/5.00 ADR matrix); Nygard format with L0/L1/L2 |
| 2026-03-06 | adv-scorer + nse-reviewer | in_progress | Phase 8 dual gate PASS: Gate A 0.939 (iter 2), Gate B PASS (Cat 2 findings resolved). All 8 phases complete. ADR-001 ready for human review per P-020. |
| 2026-03-06 | User | in_progress | ADR-001 ACCEPTED per P-020. GitHub Issue [#145](https://github.com/geekatron/jerry/issues/145) created for implementation tracking. Research phase complete; implementation phase begins. |
