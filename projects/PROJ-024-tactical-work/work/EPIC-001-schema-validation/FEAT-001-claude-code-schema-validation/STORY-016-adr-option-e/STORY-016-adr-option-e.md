# STORY-016: Add Option E to Tier Model ADR

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Close the gap between the 5-option explainer and the 4-option ADR
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** medium
> **Created:** 2026-03-28T18:00:00Z
> **Due:**
> **Completed:** 2026-03-28T20:00:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** framework decision-maker reviewing the tier model ADR

**I want** all five identified options evaluated in a single document

**So that** I can compare every option on equal footing before approving the implementation

---

## Summary

The tier model options explainer (`tier-model-options-explainer.md`) documents 5 options (A-E), but the ADR (`ADR-STORY015-001-tier-model-renumbering.md`) only evaluates 4 (A-D). Option E (Tier + Tags Hybrid) was identified by the industry research phase and has strong precedent (Linux capabilities, Deno permissions, emerging AI agent frameworks). The ADR must evaluate all 5 options to be authoritative.

**Skills informing this story:**
- `/problem-solving` (ps-architect): Add Option E evaluation to ADR using Nygard format
- `/adversary` (adv-scorer): Re-score the updated ADR at C4 >= 0.95

---

## Acceptance Criteria

### /problem-solving (ps-architect)

- [ ] Option E added to ADR Options Considered section with same structure as A-D (diagram, aspect table, key trade-off)
- [ ] Option E scored in the Evaluation Matrix against all 7 criteria
- [ ] Weighted totals recalculated with 5 options
- [ ] Sensitivity analysis updated to include Option E
- [ ] Recommendation section updated to address why Option A is preferred over Option E
- [ ] FMEA updated with Option E-specific failure modes (schema change risk)

### /adversary (C4 quality gate)

- [ ] Updated ADR scores >= 0.95 on S-014 6-dimension rubric
- [ ] No critical or major findings in the re-score

---

## Children (Tasks)

| ID | Title | Status | Owner | Skill |
|----|-------|--------|-------|-------|
| TASK-001 | Add Option E evaluation section to ADR | pending | -- | /problem-solving |
| TASK-002 | Update evaluation matrix and sensitivity analysis | pending | -- | /problem-solving |
| TASK-003 | Re-run C4 adversarial review of updated ADR | pending | -- | /adversary |

---

## Related Items

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Depends On | STORY-015 | ADR must exist before Option E can be added |
| Informed By | research/industry-tier-patterns.md | Option E sourced from industry research |
| Informed By | tier-model-options-explainer.md | Option E already described at L0/L1/L2 |
| Blocks | STORY-017 | Rule file changes depend on finalized ADR |
| Blocks | STORY-018 | Migration depends on finalized ADR |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-28 | adam.nowak | pending | Created -- ADR has 4 options, explainer has 5; gap identified by user |
| 2026-03-28 | claude | completed | Option E added to ADR with 7-criteria scoring, sensitivity analysis, FMEA. ADR re-scored 0.950 (C4 PASS). |
