# FEAT-016-011: Write /problem-solving explanation (why structured problem-solving matters)

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

Write a Diataxis explanation document for the /problem-solving skill — explaining *why* structured problem-solving with specialized agents outperforms unstructured LLM interaction, the cognitive mode taxonomy, and how the 9 agents decompose complex problems.

**Value Proposition:**
- Fills the explanation gap for Jerry's most-used skill
- Users understand *why* they should use ps-researcher vs ps-investigator vs ps-analyst

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `docs/explanation/problem-solving.md` created | [ ] |
| AC-2 | Explains *why* structured problem-solving outperforms ad-hoc LLM queries | [ ] |
| AC-3 | Explains the cognitive mode taxonomy and how agents map to modes | [ ] |
| AC-4 | Explains the creator-critic-revision cycle and why iteration matters | [ ] |
| AC-5 | Makes connections to /orchestration for multi-phase workflows | [ ] |

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

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P2.4 |
