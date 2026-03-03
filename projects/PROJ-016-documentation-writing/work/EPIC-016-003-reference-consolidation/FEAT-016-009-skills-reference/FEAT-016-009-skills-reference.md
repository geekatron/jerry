# FEAT-016-009: Create Jerry Skills Reference (consolidate fragmented tables)

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

Create a consolidated Jerry Skills Reference document. Currently, skill information is fragmented across CLAUDE.md (quick reference table), mandatory-skill-usage.md (trigger map), and individual SKILL.md files. Users must check 3+ locations to understand what skills exist and how to invoke them.

**Value Proposition:**
- Resolves 2 Minor findings from PROJ-015 audit
- Single authoritative reference for all 15 skills with invocation syntax, agents, and trigger keywords

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `docs/reference/jerry-skills-reference.md` created | [ ] |
| AC-2 | Lists all 15 skills with: name, purpose, invocation syntax, agent list, trigger keywords | [ ] |
| AC-3 | Structured by the machinery (alphabetical or by domain group) | [ ] |
| AC-4 | Links to individual SKILL.md files for full details | [ ] |
| AC-5 | No how-to guidance, no explanatory prose — pure reference | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Passes /diataxis auditor with zero quadrant-mixing findings | [ ] |
| NFC-2 | ps-critic adversarial critique score >= 0.90 | [ ] |
| NFC-3 | Includes Diataxis quadrant metadata (reference) in frontmatter | [ ] |

### Diataxis Agent

- `diataxis-reference`

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
| Source | PROJ-015 P2.5 | Remediation plan item |
| Input | CLAUDE.md, mandatory-skill-usage.md, skills/*/SKILL.md | Source content to consolidate |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P2.5 |
