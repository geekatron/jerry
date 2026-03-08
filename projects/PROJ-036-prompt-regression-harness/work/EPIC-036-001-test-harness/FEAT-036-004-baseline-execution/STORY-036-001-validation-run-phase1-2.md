# STORY-036-001: Execute Real Validation Run (Phase 1-2)

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

**I want** real API-generated outputs and G-Eval scores for all 5 target agents

**So that** I have verified baseline quality data to compare against future prompt changes

---

## Summary

Execute Phase 1 (agent output generation via Anthropic API) and Phase 2 (G-Eval scoring via DeepEvalAdapter) of the validation run for all 5 agents: ps-researcher, ps-analyst, ps-architect, ps-critic, adv-scorer. The existing scripts (`phase2_score.py`) and agent output files provide the infrastructure; this story executes them with real API calls.

**Scope:**
- Run `phase2_score.py` to generate real G-Eval composite scores for all 5 agents
- Generate fresh agent outputs if existing outputs are stale or were hand-written
- Populate `phase2-composites.json` with real scores
- Record actual API token costs in cost-ledger.md

---

## Acceptance Criteria

- [ ] All 5 agent output files (`{agent}-output.md`) contain real API-generated content
- [ ] `phase2-composites.json` contains real G-Eval composite scores (not orchestration-generated estimates)
- [ ] Per-agent score reports written to `validation-run/` directory
- [ ] Cost ledger Phase 2 row populated with actual input/output token counts and dollar cost

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
| Uses | `validation-run/phase2_score.py` | Scoring script with DeepEvalAdapter + criteria sets |
| Uses | `jerry/testing/evaluation/deepeval_adapter.py` | G-Eval scoring engine |
| Requires | `ANTHROPIC_API_KEY` | Valid API key in `.env` with sufficient credits (~$2.22 estimated) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-07 | Claude | pending | Story created; Phase 1-2 execution with real API calls |
