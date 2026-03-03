# FEAT-016-018: Add Diataxis quadrant metadata to all user-facing docs

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

Add Diataxis quadrant metadata to all user-facing documentation files. This structural improvement enables tooling to classify, filter, and validate documents by quadrant. Should run after all other documentation work is complete.

**Value Proposition:**
- Structural improvement enabling automated quadrant validation
- Users and tooling can identify document type at a glance

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | All user-facing docs in docs/ have `diataxis_quadrant:` metadata | [ ] |
| AC-2 | Quadrant values are one of: tutorial, how-to, reference, explanation | [ ] |
| AC-3 | Metadata format is consistent across all files | [ ] |
| AC-4 | Mixed-quadrant docs that were not decomposed have `mixed` marker with notes | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Metadata does not break existing document rendering | [ ] |

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
| Source | PROJ-015 P3.4 | Remediation plan item |
| Depends On | EPIC-016-001 | Decomposed docs must exist first |
| Depends On | EPIC-016-002 | New tutorials must exist first |
| Depends On | EPIC-016-003 | New reference docs must exist first |
| Depends On | EPIC-016-004 | New explanation docs must exist first |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P3.4 |
