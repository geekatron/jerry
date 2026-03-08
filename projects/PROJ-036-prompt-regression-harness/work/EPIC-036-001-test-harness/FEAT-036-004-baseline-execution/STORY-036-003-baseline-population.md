# STORY-036-003: Baseline Population N=30 per Agent

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** story
> **Status:** pending
> **Priority:** critical
> **Impact:** high
> **Created:** 2026-03-07T00:00:00Z
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-036-004
> **Owner:** —
> **Effort:** 8

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

**I want** N=30 real baseline score records per agent stored via `BaselineStore`

**So that** Layer 4 statistical comparison has sufficient power to detect 0.05 composite score regressions with p<0.05

---

## Summary

Execute 30 independent scoring runs per agent, each producing a `BaselineRecord` stored via `BaselineStore.store()`. This is CG-009 from the gap synthesis — the critical missing piece that transforms the statistical pipeline from synthetic-data validation into real regression detection. Each run generates a fresh agent output and scores it via `DeepEvalAdapter`, producing one composite score data point. N=30 exceeds the N>=20 minimum for Wilcoxon signed-rank (ADR-001) and provides adequate power for detecting meaningful quality changes.

**Scope:**
- Create a baseline collection script that loops 30 times per agent
- Each iteration: generate agent output via Anthropic API, score via DeepEvalAdapter, store via BaselineStore
- Track `model_version`, timestamp, and all 6 dimension scores per record
- Estimated cost: ~$15-30 in API credits (150 agent generations + 150 G-Eval scores)
- BaselineStore audit: verify N=30 records per agent after collection

---

## Acceptance Criteria

- [ ] `BaselineStore` contains exactly N=30 records for each of the 5 target agents
- [ ] Each record includes composite score, all 6 dimension scores, model_version, and timestamp
- [ ] `BaselineStore.audit()` reports complete baseline sets for all 5 agents
- [ ] Baseline score distributions are reasonable (mean within 0.10 of Phase 2 composites)
- [ ] Cost ledger baseline collection row populated (expected $15-30)

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
| Depends On | STORY-036-001 | Validates scoring pipeline works with real data before scaling to N=30 |
| Uses | `jerry/testing/baselines/store.py` | BaselineStore for persisting baseline records |
| Uses | `jerry/testing/evaluation/deepeval_adapter.py` | G-Eval scoring engine |
| Resolves | CG-009 | Canonical gap: baseline population (gap-synthesis.md Sprint 3) |
| Requires | `ANTHROPIC_API_KEY` | Valid API key with sufficient credits (~$15-30 estimated) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-07 | Claude | pending | Story created; resolves CG-009 (baseline population) — the critical chain dependency for regression detection |
