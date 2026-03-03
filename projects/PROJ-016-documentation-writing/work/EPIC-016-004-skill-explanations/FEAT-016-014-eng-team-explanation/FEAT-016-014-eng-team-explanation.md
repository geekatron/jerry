# FEAT-016-014: Write /eng-team explanation (why security-first engineering)

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

Write a Diataxis explanation document for the /eng-team skill — explaining *why* security-first engineering with 10 specialized agents (architecture through incident response) produces more secure software than bolt-on security reviews.

**Value Proposition:**
- Users understand *why* /eng-team exists and how it integrates security into every phase

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `docs/explanation/eng-team.md` created | [ ] |
| AC-2 | Explains *why* security-first engineering outperforms bolt-on security | [ ] |
| AC-3 | Explains the 8-step workflow and how agents map to SDL phases | [ ] |
| AC-4 | Explains integration with /red-team for threat-informed architecture | [ ] |
| AC-5 | Makes connections to NIST SSDF, MS SDL, OWASP ASVS frameworks | [ ] |

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
