# EPIC-016-001: Document Extraction & Revision

> **Type:** epic
> **Status:** pending
> **Priority:** high
> **Impact:** high
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

Decompose existing mixed-quadrant documents into Diataxis-pure documents and revise docs that violate quadrant boundaries. This epic addresses the 9 Major findings from PROJ-015 audit where existing docs mix tutorial, how-to, reference, and explanation content in single files.

**Key Objectives:**
- Decompose prompt-quality.md into explanation + 2 how-to guides + reference
- Create context-architecture.md explanation document
- Create hooks-architecture.md explanation document
- Revise INSTALLATION.md to remove marketing voice and extract explanation content

---

## Business Outcome Hypothesis

**We believe that** decomposing mixed-quadrant documents into Diataxis-pure documents

**Will result in** users finding the right information type (learning, doing, understanding, looking up) without wading through irrelevant content

**We will know we have succeeded when** each output document passes Diataxis purity audit with zero quadrant-mixing findings

---

## Children Features/Capabilities

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-016-001 | Decompose prompt-quality.md into explanation + 2 how-to guides + reference | pending | high | 0% |
| FEAT-016-002 | Create docs/explanation/context-architecture.md | pending | high | 0% |
| FEAT-016-003 | Create docs/explanation/hooks-architecture.md | pending | high | 0% |
| FEAT-016-004 | Revise INSTALLATION.md — remove marketing voice, extract explanation content | pending | high | 0% |

### Feature Links

- [FEAT-016-001: Decompose prompt-quality.md](./FEAT-016-001-decompose-prompt-quality/FEAT-016-001-decompose-prompt-quality.md)
- [FEAT-016-002: Context architecture explanation](./FEAT-016-002-context-architecture/FEAT-016-002-context-architecture.md)
- [FEAT-016-003: Hooks architecture explanation](./FEAT-016-003-hooks-architecture/FEAT-016-003-hooks-architecture.md)
- [FEAT-016-004: Revise INSTALLATION.md](./FEAT-016-004-revise-installation/FEAT-016-004-revise-installation.md)

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Features** | 4 |
| **Completed Features** | 0 |
| **In Progress Features** | 0 |
| **Pending Features** | 4 |
| **Feature Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent:** PROJ-016-documentation-writing

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | PROJ-015 | Remediation report provides work item source (P1.1-P1.4) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Epic created from PROJ-015 remediation items P1.1-P1.4 |
