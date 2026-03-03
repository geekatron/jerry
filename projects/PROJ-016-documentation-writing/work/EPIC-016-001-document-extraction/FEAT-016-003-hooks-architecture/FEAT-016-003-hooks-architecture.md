# FEAT-016-003: Create docs/explanation/hooks-architecture.md

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

Create a Diataxis explanation document covering Jerry's hooks architecture — the SessionStart hook, pre-commit hooks, project context injection, and how hooks integrate with the enforcement layers. PROJ-015 found 2 Major findings where hooks concepts were explained inline within INSTALLATION.md and getting-started.md rather than in dedicated explanation docs.

**Value Proposition:**
- Resolves 2 Major findings from PROJ-015 audit
- Users understand the *why* behind Jerry's hook-based enforcement design

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `docs/explanation/hooks-architecture.md` created with Diataxis explanation structure | [ ] |
| AC-2 | Explains *why* Jerry uses hooks for project context (SessionStart) | [ ] |
| AC-3 | Explains *why* pre-commit hooks enforce quality (L5 layer) | [ ] |
| AC-4 | Explains the hook lifecycle: session start -> work -> commit -> CI | [ ] |
| AC-5 | Connects hooks to the broader enforcement architecture (L1-L5) | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Passes /diataxis auditor with zero quadrant-mixing findings | [ ] |
| NFC-2 | ps-critic adversarial critique score >= 0.90 | [ ] |
| NFC-3 | Includes Diataxis quadrant metadata in frontmatter | [ ] |

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

- **Parent Epic:** [EPIC-016-001: Document Extraction & Revision](../EPIC-016-001-document-extraction.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Source | PROJ-015 P1.3 | Remediation plan item |
| Input | INSTALLATION.md | Contains hooks setup content to reference |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P1.3 |
