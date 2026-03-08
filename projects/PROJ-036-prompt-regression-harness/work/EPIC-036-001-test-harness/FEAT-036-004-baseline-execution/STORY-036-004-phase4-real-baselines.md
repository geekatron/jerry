# STORY-036-004: Phase 4 Real Baseline Comparison

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-07T00:00:00Z
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-036-004
> **Owner:** —
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a/I want/So that |
| [Summary](#summary) | Scope and context |
| [Acceptance Criteria](#acceptance-criteria) | Observable outcomes |
| [Progress Summary](#progress-summary) | Completion metrics |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** framework maintainer

**I want** Layer 4 statistical comparison run with real baselines from `BaselineStore`

**So that** the Wilcoxon signed-rank test and Wilson CI produce meaningful PASS/BLOCK/WARNING verdicts based on actual agent quality data

---

## Summary

Replace the synthetic `random.Random(42)` baselines in `phase4_stats.py` with real baseline data from `BaselineStore` (populated by STORY-036-003). Run `Layer4Pipeline` comparing real baselines against candidate scores, producing Wilcoxon signed-rank p-values, Wilson confidence intervals, and exit codes (0=PASS, 1=BLOCK, 2=WARNING) based on real data.

**Scope:**
- Modify `phase4_stats.py` (or create `phase4_real.py`) to load baselines from `BaselineStore` instead of generating synthetic arrays
- Run Layer 4 comparison for all 5 agents
- Validate that PASS/BLOCK/WARNING verdicts are meaningful with real data
- No API cost — this is a local computation on stored baseline data

---

## Acceptance Criteria

- [ ] Layer 4 comparison uses real baselines from `BaselineStore` (not synthetic)
- [ ] Wilcoxon signed-rank p-values computed for all 5 agents
- [ ] Wilson confidence intervals computed for all 5 agents
- [ ] Layer 4 JSON and Markdown reports written with real baseline statistics
- [ ] PASS/BLOCK/WARNING verdicts validated as sensible given real score distributions

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 0 |
| **Completed Tasks** | 0 |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-036-004: Baseline Collection and Validation Execution](./FEAT-036-004-baseline-execution.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | STORY-036-003 | Requires N=30 baselines in BaselineStore |
| Uses | `jerry/testing/layer4_stats.py` | Layer4Pipeline with Wilcoxon + Wilson |
| Uses | `jerry/testing/baselines/store.py` | BaselineStore for loading real baselines |
| Uses | `validation-run/phase4_stats.py` | Phase 4 script (needs real baseline modification) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-07 | Claude | pending | Story created; replaces synthetic baselines with real BaselineStore data |
