# STORY-036-002: Execute Real MR Tests at N>=20 (Phase 3)

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
> **Effort:** 5

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

**I want** metamorphic relation tests executed at statistically powered N>=20

**So that** MR tolerance thresholds are validated with real data and Wilcoxon signed-rank tests produce meaningful p-values

---

## Summary

Execute Phase 3 MR tests using `phase3_mr_smoke.py` (modified for N>=20) with real API calls. The current smoke test ran at N=5 and all 4 tests failed (deltas 0.0710-0.1120 exceeded tolerances 0.03-0.05). With real N>=20 data, MR tolerance thresholds can be properly calibrated and the `CalibrationRunner` at `jerry/testing/metamorphic/calibration.py` can establish empirical bounds.

**Scope:**
- Modify `phase3_mr_smoke.py` to use N>=20 (or create a new `phase3_mr_full.py`)
- Run MR-001 (ParaphraseConsistency) and MR-003 (IrrelevantContextAppendation) for ps-researcher and ps-architect
- Use CalibrationRunner to establish empirical tolerance thresholds from real data
- Record API costs (estimated ~$9.60+ for 80 variant generations + 80 G-Eval scores)

---

## Acceptance Criteria

- [ ] MR-001 and MR-003 executed at N>=20 for ps-researcher and ps-architect (4 MR tests total)
- [ ] CalibrationRunner produces empirical tolerance thresholds from real score distributions
- [ ] MR results report includes per-variant scores, mean delta, and statistical significance
- [ ] Tolerance thresholds updated in MR class constants if empirical data differs from defaults
- [ ] Cost ledger Phase 3 row populated with actual token costs

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
| Depends On | STORY-036-001 | Needs real agent outputs from Phase 1-2 |
| Uses | `validation-run/phase3_mr_smoke.py` | MR test script (needs N>=20 modification) |
| Uses | `jerry/testing/metamorphic/calibration.py` | CalibrationRunner for empirical threshold establishment |
| Uses | `jerry/testing/metamorphic/mr_001_paraphrase.py` | ParaphraseConsistency MR class |
| Uses | `jerry/testing/metamorphic/mr_003_context.py` | IrrelevantContextAppendation MR class |
| Requires | `ANTHROPIC_API_KEY` | Valid API key with sufficient credits (~$9.60+ estimated) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-07 | Claude | pending | Story created; MR tests at statistically powered N>=20 (ADR-001 requirement) |
