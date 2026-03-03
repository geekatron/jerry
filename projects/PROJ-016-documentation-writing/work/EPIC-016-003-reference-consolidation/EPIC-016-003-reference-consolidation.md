# EPIC-016-003: Reference Consolidation

> **Type:** epic
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-02T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** PROJ-016-documentation-writing
> **Owner:** Claude
> **Target Quarter:** FY26-Q1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key objectives |
| [Business Outcome Hypothesis](#business-outcome-hypothesis) | Expected business outcomes |
| [Children Features/Capabilities](#children-featurescapabilities) | Feature inventory and tracking |
| [Progress Summary](#progress-summary) | Overall epic progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Status changes and key events |

---

## Summary

Consolidate fragmented reference documentation and decompose mixed-quadrant reference/how-to docs. While Jerry has 100% reference coverage, the reference content is scattered across multiple files and mixed with how-to guide content. This epic creates authoritative, consolidated reference documents.

**Key Objectives:**
- Decompose prompt-templates.md into pure reference catalog + how-to guide
- Create consolidated Jerry Skills Reference from fragmented tables
- Create Jerry CLI Reference

---

## Business Outcome Hypothesis

**We believe that** consolidating reference documentation into authoritative single-source documents

**Will result in** users finding API details, configuration options, and skill parameters without searching multiple files

**We will know we have succeeded when** each reference document passes Diataxis reference criteria (information-oriented, austere, structured by the machinery)

---

## Children Features/Capabilities

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-016-008 | Decompose prompt-templates.md into reference catalog + how-to guide | pending | medium | 0% |
| FEAT-016-009 | Create Jerry Skills Reference (consolidate fragmented tables) | pending | medium | 0% |
| FEAT-016-010 | Create Jerry CLI Reference | pending | low | 0% |

### Feature Links

- [FEAT-016-008: Decompose prompt-templates.md](./FEAT-016-008-decompose-prompt-templates/FEAT-016-008-decompose-prompt-templates.md)
- [FEAT-016-009: Jerry Skills Reference](./FEAT-016-009-skills-reference/FEAT-016-009-skills-reference.md)
- [FEAT-016-010: Jerry CLI Reference](./FEAT-016-010-cli-reference/FEAT-016-010-cli-reference.md)

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Features** | 3 |
| **Completed Features** | 0 |
| **In Progress Features** | 0 |
| **Pending Features** | 3 |
| **Feature Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent:** PROJ-016-documentation-writing

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | PROJ-015 | Remediation report identifies reference gaps (P2.1, P2.5, P3.3) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Epic created from PROJ-015 remediation items P2.1, P2.5, P3.3 |
