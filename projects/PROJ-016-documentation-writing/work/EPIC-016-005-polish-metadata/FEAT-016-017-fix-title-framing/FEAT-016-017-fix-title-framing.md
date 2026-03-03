# FEAT-016-017: Fix title framing on BOOTSTRAP.md, CLAUDE-MD-GUIDE.md, prompt-templates.md

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

Fix title framing on 3 documents where the title/subtitle misrepresents the document's Diataxis quadrant. For example, a how-to guide titled "Understanding X" (explanation framing) or a reference doc titled "How to Use X" (how-to framing).

**Value Proposition:**
- Resolves 3 Minor findings from PROJ-015 audit
- Titles accurately signal the document type to users

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | BOOTSTRAP.md title reflects its actual quadrant (how-to) | [ ] |
| AC-2 | CLAUDE-MD-GUIDE.md title reflects its actual quadrant | [ ] |
| AC-3 | prompt-templates.md title reflects its actual quadrant (reference/how-to) | [ ] |
| AC-4 | Subtitles and opening paragraphs align with quadrant framing | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Title changes reviewed for downstream link breakage | [ ] |

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
| Source | PROJ-015 P2.2 | Remediation plan item |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P2.2 |
