# FEAT-016-008: Decompose prompt-templates.md into reference catalog + how-to guide

> **Type:** feature
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-02T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** EPIC-016-003
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

Decompose `.context/rules/prompt-templates.md` — currently a mixed reference/how-to document containing both template definitions (reference) and guidance on when/how to use each template (how-to). Split into a pure reference catalog of templates and a how-to guide for template selection.

**Value Proposition:**
- Resolves 1 Major finding from PROJ-015 audit
- Users looking up template syntax don't wade through selection guidance, and vice versa

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `docs/reference/prompt-templates-catalog.md` created — pure reference: all 6 templates with placeholder tables, syntax, and examples | [ ] |
| AC-2 | `docs/how-to/select-prompt-template.md` created — goal-oriented guide: "Which template should I use?" with decision tree | [ ] |
| AC-3 | Original `.context/rules/prompt-templates.md` updated to link to new documents | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Each output document passes /diataxis auditor with zero quadrant-mixing findings | [ ] |
| NFC-2 | ps-critic adversarial critique score >= 0.90 per document | [ ] |
| NFC-3 | All documents include Diataxis quadrant metadata in frontmatter | [ ] |

### Diataxis Agents

- `diataxis-reference` for docs/reference/prompt-templates-catalog.md
- `diataxis-howto` for docs/how-to/select-prompt-template.md

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

- **Parent Epic:** [EPIC-016-003: Reference Consolidation](../EPIC-016-003-reference-consolidation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Source | PROJ-015 P2.1 | Remediation plan item |
| Input | .context/rules/prompt-templates.md | Source document to decompose |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P2.1 |
