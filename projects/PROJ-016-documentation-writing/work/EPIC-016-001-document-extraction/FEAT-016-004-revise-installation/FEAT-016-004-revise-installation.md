# FEAT-016-004: Revise INSTALLATION.md — remove marketing voice, extract explanation content

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-02T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** EPIC-016-001
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

Revise INSTALLATION.md to be a pure Diataxis how-to guide. PROJ-015 audit found 1 Major finding (marketing/promotional voice) and 4 Minor findings (explanation content mixed in, conceptual tangents). Extract explanation content to the context-architecture and hooks-architecture explanation docs (FEAT-016-002, FEAT-016-003).

**Value Proposition:**
- Resolves 1 Major + 4 Minor findings from PROJ-015 audit
- INSTALLATION.md becomes a pure goal-oriented guide: "How to install Jerry"

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Marketing/promotional voice removed (phrases like "powerful framework", "game-changing") | [ ] |
| AC-2 | Explanation content extracted to docs/explanation/ docs (linked, not duplicated) | [ ] |
| AC-3 | Document follows how-to structure: goal statement, prerequisites, numbered steps, verification | [ ] |
| AC-4 | Each step has a single clear action with expected result | [ ] |
| AC-5 | No conceptual tangents — links to explanation docs for "why" questions | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Passes /diataxis auditor with zero quadrant-mixing findings | [ ] |
| NFC-2 | ps-critic adversarial critique score >= 0.90 | [ ] |
| NFC-3 | Includes Diataxis quadrant metadata in frontmatter | [ ] |

### Diataxis Agent

- `diataxis-howto`

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

- **Parent Epic:** [EPIC-016-001: Document Extraction & Revision](../EPIC-016-001-document-extraction.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Source | PROJ-015 P1.4 | Remediation plan item |
| Depends On | FEAT-016-002 | Context architecture explanation must exist before extracting content there |
| Depends On | FEAT-016-003 | Hooks architecture explanation must exist before extracting content there |
| Input | INSTALLATION.md | Source document to revise |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P1.4 |
