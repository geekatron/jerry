# FEAT-016-015: Write /prompt-engineering explanation (why structured prompts)

> **Type:** feature
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-02T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** EPIC-016-004
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

Write a Diataxis explanation document for the /prompt-engineering skill — explaining *why* structured prompt construction with the 5-element anatomy, NPT constraint patterns, and quality scoring produces better LLM outputs than ad-hoc prompting.

**Value Proposition:**
- Users understand *why* structured prompts matter and the research behind the 5-element anatomy

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `docs/explanation/prompt-engineering.md` created | [ ] |
| AC-2 | Explains *why* structured prompts outperform ad-hoc prompting | [ ] |
| AC-3 | Explains the 5-element anatomy and the research behind it | [ ] |
| AC-4 | Explains NPT patterns and negative prompting techniques | [ ] |
| AC-5 | Connects to PROJ-014 negative prompting research findings | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Passes /diataxis auditor with zero quadrant-mixing findings | [ ] |
| NFC-2 | ps-critic adversarial critique score >= 0.90 | [ ] |

### Diataxis Agent

- `diataxis-explanation`

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

- **Parent Epic:** [EPIC-016-004: Skill Explanations](../EPIC-016-004-skill-explanations.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Source | PROJ-015 P2.4 | Remediation plan item (explanation gap) |
| Reference | PROJ-014 | Negative prompting research findings |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P2.4 |
