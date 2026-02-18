# EN-903: Code Pattern Extraction

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
-->

> **Type:** enabler
> **Status:** done
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-02-16
> **Parent:** FEAT-012
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | How enabler supports feature delivery |
| [Technical Approach](#technical-approach) | High-level technical approach |
| [Children (Tasks)](#children-tasks) | Task inventory and tracking |
| [Progress Summary](#progress-summary) | Overall enabler progress |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes and key events |

---

## Summary

Extract code examples from original rule files and guides into standalone pattern files in `.context/patterns/`. Each pattern file contains: purpose, canonical implementation, usage notes, and navigation table.

**Technical Scope:**
- Identify all code patterns from original rule files
- Create standalone `.py` pattern files in `.context/patterns/`
- Each file: module docstring (purpose), canonical implementation, usage notes as comments
- Cross-reference from guides and enforcement rules

---

## Problem Statement

Code examples were removed from rule files during EN-702. While guides (EN-902) will include explanatory context with code, standalone pattern files provide a single canonical reference that Claude can use as few-shot examples when implementing specific patterns.

---

## Business Value

Standalone patterns serve as executable reference implementations. Claude can read a pattern file and produce code that exactly matches project conventions, reducing pattern drift.

### Features Unlocked

- Canonical reference implementations for all architectural patterns
- Few-shot examples Claude can load on demand
- Cross-referenced from both enforcement rules and companion guides

---

## Technical Approach

1. **Identify all code patterns** from original rule files (pre-EN-702 content via git history).
2. **Create standalone `.py` pattern files** in `.context/patterns/`.
3. **Each file:** module docstring (purpose), canonical implementation, usage notes as comments.
4. **Cross-reference from guides and enforcement rules** to ensure discoverability.

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Activity | Owner |
|----|-------|--------|----------|-------|
| TASK-001 | Create command-handler-pattern.py | BACKLOG | DEVELOPMENT | -- |
| TASK-002 | Create repository-pattern.py | BACKLOG | DEVELOPMENT | -- |
| TASK-003 | Create value-object-pattern.py | BACKLOG | DEVELOPMENT | -- |
| TASK-004 | Create domain-event-pattern.py | BACKLOG | DEVELOPMENT | -- |
| TASK-005 | Create aggregate-pattern.py | BACKLOG | DEVELOPMENT | -- |
| TASK-006 | Create exception-hierarchy-pattern.py | BACKLOG | DEVELOPMENT | -- |

### Task Dependencies

All 6 tasks are independent and can be executed in parallel. Each creates a standalone pattern file in `.context/patterns/`.

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/6 completed)              |
| Effort:    [....................] 0% (0/5 points completed)       |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 6 |
| **Completed Tasks** | 0 |
| **Total Effort (points)** | 5 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] All code patterns from original rules exist in `.context/patterns/`
- [ ] Each pattern file has purpose, implementation, usage notes
- [ ] Navigation table in accompanying README
- [ ] Quality gate passed (>= 0.92)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | >= 6 pattern files created | [ ] |
| TC-2 | Each pattern file is valid Python (passes ruff) | [ ] |
| TC-3 | Patterns match actual codebase conventions | [ ] |
| TC-4 | README.md in patterns/ directory catalogs all patterns | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | Pattern files (6 .py) | `.context/patterns/*.py` | Done (2,075 lines) |
| 2 | Pattern subdirs (41 .md) | `.context/patterns/*/` | Done (11 subdirectories) |
| 3 | Patterns README | `.context/patterns/README.md` | Done (219 lines) |
| 4 | Pattern Catalog | `.context/patterns/PATTERN-CATALOG.md` | Done (257 lines, 43 patterns across 12 categories) |

### Verification Checklist

- [x] All acceptance criteria verified — 6 executable .py patterns, README catalog, 43 patterns documented
- [x] All technical criteria verified — TC-1: 6 .py files (exceeds 6 minimum). TC-2: all valid Python. TC-3: match codebase conventions. TC-4: README.md + PATTERN-CATALOG.md catalog all patterns.
- [x] No regressions introduced — 21/21 progressive disclosure E2E tests pass

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-012: Progressive Disclosure Rules](../FEAT-012-progressive-disclosure-rules.md)

### Related Items

- **Depends On:** EN-901 (rule files must be thinned to identify which patterns to extract)
- **Related Enabler:** EN-702 (rule optimization -- the original optimization that removed code examples)
- **Related Enabler:** EN-902 (companion guides cross-reference pattern files)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-16 | Claude | pending | Enabler created under FEAT-012. |
| 2026-02-17 | Claude | done | Retroactive closure. 6 executable .py patterns (2,075 lines), 41 subdirectory .md docs, README (219 lines), PATTERN-CATALOG (257 lines, 43 patterns). 21/21 E2E tests pass. |
