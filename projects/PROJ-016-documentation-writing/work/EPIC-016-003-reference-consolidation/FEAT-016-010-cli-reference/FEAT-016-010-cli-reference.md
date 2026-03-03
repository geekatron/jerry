# FEAT-016-010: Create Jerry CLI Reference

> **Type:** feature
> **Status:** pending
> **Priority:** low
> **Impact:** low
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

Create a comprehensive Jerry CLI Reference document. Currently, CLI commands are documented briefly in CLAUDE.md's Quick Reference section. A full reference should cover all commands, subcommands, flags, and output formats.

**Value Proposition:**
- Resolves 1 Minor finding from PROJ-015 audit
- Users have one place to look up any CLI command syntax

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `docs/reference/jerry-cli-reference.md` created | [ ] |
| AC-2 | Documents all CLI namespaces: session, items, projects, ast, ci | [ ] |
| AC-3 | Each command has: syntax, flags, examples, output format | [ ] |
| AC-4 | Structured by namespace (mirrors CLI structure) | [ ] |
| AC-5 | No how-to guidance — pure reference | [ ] |

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
| Source | PROJ-015 P3.3 | Remediation plan item |
| Input | src/interface/cli/parser.py | CLI source for accurate command documentation |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P3.3 |
