# FEAT-016-019: Write tutorials for remaining 10 skills

> **Type:** feature
> **Status:** pending
> **Priority:** low
> **Impact:** medium
> **Created:** 2026-03-02T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** EPIC-016-005
> **Owner:** Claude
> **Target Sprint:**

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and value proposition |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done and criteria |
| [Children Stories/Enablers](#children-storiesenablers) | Story/enabler inventory |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Status changes and key events |

---

## Summary

Write Diataxis tutorials for the remaining 10 skills not covered by EPIC-016-002 (which covers /problem-solving, /orchestration, /worktracker). This includes tutorials for /adversary, /eng-team, /red-team, /nasa-se, /diataxis, /prompt-engineering, /transcript, /ast, /architecture, and /saucer-boy.

**Value Proposition:**
- Closes the remaining tutorial coverage gap from 20% to 100%
- Lower priority because these skills are less frequently used by new users

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | 10 tutorial files created in docs/tutorials/ | [ ] |
| AC-2 | Each tutorial follows Diataxis tutorial structure (prerequisites, steps, visible results, no alternatives) | [ ] |
| AC-3 | Skills covered: /adversary, /eng-team, /red-team, /nasa-se, /diataxis, /prompt-engineering, /transcript, /ast, /architecture, /saucer-boy | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Each passes /diataxis auditor with zero quadrant-mixing findings | [ ] |
| NFC-2 | ps-critic adversarial critique score >= 0.90 per tutorial | [ ] |

### Diataxis Agent

- `diataxis-tutorial`

---

## Children Stories/Enablers

_To be decomposed when implementation begins._

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Children** | 0 |
| **Completed** | 0 |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-016-005: Polish & Metadata](../EPIC-016-005-polish-metadata.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Source | PROJ-015 P3.5 | Remediation plan item (10 coverage gaps) |
| Depends On | EPIC-016-002 | Top 3 tutorials should be complete first (establish pattern) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P3.5 |
