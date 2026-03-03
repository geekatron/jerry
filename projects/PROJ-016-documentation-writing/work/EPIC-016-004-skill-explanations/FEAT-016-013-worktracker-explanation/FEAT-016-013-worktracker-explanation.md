# FEAT-016-013: Write /worktracker explanation (why persistent work tracking)

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

Write a Diataxis explanation document for the /worktracker skill — explaining *why* persistent work tracking with entity hierarchy, template enforcement, and WTI rules matters for multi-session LLM workflows where context rot destroys state.

**Value Proposition:**
- Users understand *why* worktracker exists (Context Rot solution for task state)

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `docs/explanation/worktracker.md` created | [ ] |
| AC-2 | Explains *why* persistent work tracking is needed (Context Rot problem for task state) | [ ] |
| AC-3 | Explains the entity hierarchy design and why it mirrors enterprise project management | [ ] |
| AC-4 | Explains WTI rules and why integrity constraints matter | [ ] |
| AC-5 | Connects to the broader Jerry philosophy (filesystem as memory) | [ ] |

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
