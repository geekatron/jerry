# FEAT-016-001: Decompose prompt-quality.md into explanation + 2 how-to guides + reference

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

Decompose `.context/rules/prompt-quality.md` — currently a mixed-quadrant document containing explanation content (why prompts matter), how-to guidance (how to write prompts, how to use the adversarial loop), and reference content (quality rubric, agent table). Split into 4 Diataxis-pure documents.

**Value Proposition:**
- Resolves 2 Major findings from PROJ-015 audit
- Each output document serves exactly one user need (understanding, doing, or looking up)

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `docs/explanation/prompt-quality.md` created — explains *why* the 5-element anatomy matters and the design philosophy behind the quality rubric | [ ] |
| AC-2 | `docs/how-to/write-effective-prompts.md` created — goal-oriented guide for writing prompts (not a tutorial; assumes competence) | [ ] |
| AC-3 | `docs/how-to/use-adversarial-critique.md` created — goal-oriented guide for invoking and configuring ps-critic loop | [ ] |
| AC-4 | `docs/reference/prompt-quality-rubric.md` created — pure reference: 7-criterion rubric table, scoring formula, tier definitions, agent selection table | [ ] |
| AC-5 | Original `.context/rules/prompt-quality.md` updated to link to new documents (not deleted — remains as rules context) | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Each output document passes /diataxis auditor with zero quadrant-mixing findings | [ ] |
| NFC-2 | ps-critic adversarial critique score >= 0.90 per document | [ ] |
| NFC-3 | All documents include Diataxis quadrant metadata in frontmatter | [ ] |

### Diataxis Agents

- `diataxis-explanation` for docs/explanation/prompt-quality.md
- `diataxis-howto` for docs/how-to/write-effective-prompts.md and use-adversarial-critique.md
- `diataxis-reference` for docs/reference/prompt-quality-rubric.md

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
| Source | PROJ-015 P1.1 | Remediation plan item |
| Input | .context/rules/prompt-quality.md | Source document to decompose |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P1.1 |
