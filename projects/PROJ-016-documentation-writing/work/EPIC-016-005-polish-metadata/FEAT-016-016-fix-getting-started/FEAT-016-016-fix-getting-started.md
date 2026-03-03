# FEAT-016-016: Fix getting-started.md — remove tutorial branching, compress digressions

> **Type:** feature
> **Status:** pending
> **Priority:** low
> **Impact:** low
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

Fix getting-started.md tutorial to remove branching paths ("if you want X, do A; if you want Y, do B") and compress conceptual digressions that break the tutorial flow. A Diataxis tutorial must present one clear path with no alternatives.

**Value Proposition:**
- Resolves 1 Minor finding (tutorial branching) and 2 Minor findings (digressions)

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | All tutorial branching removed — one clear path through the document | [ ] |
| AC-2 | Conceptual digressions moved to explanation docs or removed | [ ] |
| AC-3 | Each step has a single action and visible result | [ ] |
| AC-4 | Links to explanation docs for "why" questions | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Passes /diataxis auditor with zero quadrant-mixing findings | [ ] |
| NFC-2 | ps-critic adversarial critique score >= 0.90 | [ ] |

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
| Source | PROJ-015 P3.1, P3.2 | Remediation plan items |
| Depends On | FEAT-016-002 | Context architecture explanation should exist for digression extraction |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P3.1, P3.2 |
