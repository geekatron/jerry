# FEAT-016-012: Write /orchestration explanation (why multi-agent coordination)

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

Write a Diataxis explanation document for the /orchestration skill — explaining *why* multi-agent coordination with state tracking, sync barriers, and quality gates produces better results than sequential single-agent work.

**Value Proposition:**
- Users understand *why* orchestration exists and when to use it vs. simple skill invocation

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `docs/explanation/orchestration.md` created | [ ] |
| AC-2 | Explains *why* multi-agent coordination outperforms sequential single-agent work | [ ] |
| AC-3 | Explains sync barriers, quality gates, and checkpointing concepts | [ ] |
| AC-4 | Explains cross-pollination between parallel pipelines | [ ] |
| AC-5 | Makes connections to /problem-solving and other skills | [ ] |

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
