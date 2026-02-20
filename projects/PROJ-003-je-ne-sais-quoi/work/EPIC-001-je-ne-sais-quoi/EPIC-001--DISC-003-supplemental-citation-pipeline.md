# EPIC-001:DISC-003: Supplemental Citation Pipeline Pattern

> **Type:** discovery
> **Status:** VALIDATED
> **Priority:** MEDIUM
> **Impact:** MEDIUM
> **Created:** 2026-02-19
> **Completed:** 2026-02-19
> **Parent:** EPIC-001
> **Owner:** Claude (orchestrator)
> **Source:** Phase 1 supplemental pipeline execution

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Core finding: enrichment passes cause score regression requiring full critic cycle |
| [Context](#context) | Background on the supplemental pipeline |
| [Finding](#finding) | Score trajectory and regression analysis |
| [Evidence](#evidence) | Sources and citations |
| [Implications](#implications) | Impact on future enrichment workflows |
| [Relationships](#relationships) | Related work items |
| [Metadata](#metadata) | Machine-readable metadata |

---

## Summary

When a deliverable passes the quality gate but lacks proper citations, a supplemental pipeline (researcher-supplemental -> creator-supplemental -> critic-supplemental x 3 -> scorer-supplemental) can enrich the artifact without rewriting it. Key finding: the supplemental creator pass caused a score regression (0.930 -> 0.913) because large additions introduce execution-level defects even when the content is high-quality. The subsequent critic pass recovered and exceeded the previous score (0.953).

**Key Findings:**
- Large enrichment passes (adding citations, integrating new research) introduce their own defects even when content quality is high
- Score regression of -0.017 occurred post-enrichment, recovered +0.040 after full critic cycle
- The enrichment-not-rewrite approach preserves voice consistency while adding rigor

**Validation:** Score trajectory verified across 4 scored iterations (v0.4.0 through v0.8.0).

---

## Context

### Background

After the initial Phase 1 pipeline produced a 0.930-scoring persona doc with no web citations, the user directed a supplemental pipeline targeting >= 0.95 with proper references. The pipeline preserved the existing structure while adding citations, fixing errors, and integrating new information.

### Research Question

Can a supplemental enrichment pipeline improve citation quality without degrading an already quality-gated deliverable?

---

## Finding

### Score Trajectory Showing Regression-Then-Recovery

| Stage | Score | Delta | Notes |
|-------|-------|-------|-------|
| Post-R3 (v0.4.0) | 0.930 | -- | Pre-supplemental baseline |
| Post-creator-supplemental (v0.5.0) | 0.913 | -0.017 | Regression from citation defects |
| Post-R4 (v0.6.0) | 0.934 | +0.021 | Defects corrected |
| Post-R6 (v0.8.0) | 0.953 | +0.019 | Exceeds both original and raised threshold |

### Root Cause of Regression

The regression occurred because:
- Wingsuit citation was misattributed ([8] instead of [23, 28])
- References header falsely claimed all 35 sources were inline-cited (only 15 were)
- Vail ban was claimed present in narrative but was not actually integrated
- Epistemic note was incomplete about verified quote sources

### Lesson

Large enrichment passes (adding citations, integrating new research) require their own review cycle even when the underlying content is high-quality. The supplemental critic pass is not optional overhead -- it catches defects that the enrichment pass itself introduces.

---

## Evidence

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Artifact | ps-critic-001-review-r4.md (documents regression and corrections) | Phase 1 supplemental pipeline | 2026-02-19 |
| E-002 | Artifact | ps-creator-001-draft.md changelog (v0.5.0 through v0.9.0) | Phase 1 creator output | 2026-02-19 |
| E-003 | Artifact | adv-scorer-001-supplemental-quality-score.md (independent verification) | Phase 1 scoring output | 2026-02-19 |

---

## Implications

### Impact on Project

- Any future supplemental enrichment pass MUST include a full critic cycle (not abbreviated)
- Quality gate scores before and after enrichment should be compared to detect regression
- The enrichment-not-rewrite approach preserves voice consistency while adding rigor

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Enrichment passes skipped critic cycle due to "just adding citations" perception | MEDIUM | Document this pattern as mandatory: enrichment -> full critic cycle |
| Score regression goes undetected if pre/post comparison is not performed | LOW | Include pre/post scoring in enrichment pipeline templates |

---

## Relationships

### Related Discoveries

- DISC-002 Training Data Research Errors (triggered this supplemental pipeline)

### Informs

- Future orchestration pipeline designs involving enrichment passes
- ORCHESTRATION_PLAN.md pipeline templates

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-19 | Claude (orchestrator) | Created discovery |

---

## Metadata

```yaml
id: "EPIC-001:DISC-003"
parent_id: "EPIC-001"
work_type: DISCOVERY
title: "Supplemental Citation Pipeline Pattern"
status: VALIDATED
priority: MEDIUM
impact: MEDIUM
created_by: "Claude (orchestrator)"
created_at: "2026-02-19"
updated_at: "2026-02-19"
completed_at: "2026-02-19"
tags: [workflow-pattern, citation-quality, quality-gate]
source: "Phase 1 supplemental pipeline execution"
finding_type: PATTERN
confidence_level: HIGH
validated: true
```
