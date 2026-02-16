# EN-904: Path Scoping Implementation

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-02-16
> **Parent:** FEAT-012
> **Effort:** 3

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

Add YAML frontmatter with `paths` field to Python-specific rule files so they only load when Claude is editing Python files. This reduces token overhead for non-Python sessions (documentation, worktracker, markdown editing).

**Technical Scope:**
- Add YAML frontmatter with `paths: ["src/**/*.py", "tests/**/*.py"]` to `architecture-standards.md`
- Same for `coding-standards.md`
- Same for `testing-standards.md`
- Test that rules load conditionally

---

## Problem Statement

All `.claude/rules/` files load unconditionally at session start. Python-specific rules (architecture layer boundaries, type hints, test pyramid) are irrelevant when editing markdown documentation or worktracker files, wasting tokens.

---

## Business Value

Path scoping reduces session-start token cost for non-Python tasks. A documentation session loads only documentation-relevant rules, keeping context lean.

### Features Unlocked

- Reduced token overhead for documentation-only sessions
- Context-appropriate rule loading based on file type being edited
- Leaner session start for non-Python workflows

---

## Technical Approach

1. **Add YAML frontmatter** with `paths: ["src/**/*.py", "tests/**/*.py"]` to `architecture-standards.md`.
2. **Same for `coding-standards.md`** with paths covering both `src/` and `tests/`.
3. **Same for `testing-standards.md`** with paths covering `tests/`.
4. **Test that rules load conditionally** -- verify Python sessions load scoped rules, non-Python sessions do not.

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Activity | Owner |
|----|-------|--------|----------|-------|
| TASK-001 | Add paths frontmatter to architecture-standards.md | BACKLOG | DEVELOPMENT | -- |
| TASK-002 | Add paths frontmatter to coding-standards.md | BACKLOG | DEVELOPMENT | -- |
| TASK-003 | Add paths frontmatter to testing-standards.md | BACKLOG | DEVELOPMENT | -- |
| TASK-004 | Verify path-scoped rules load correctly | BACKLOG | REVIEW | -- |

### Task Dependencies

TASK-001 through TASK-003 are independent and can be executed in parallel (each modifies a different file). TASK-004 depends on all three completing (verification requires all scoped files to exist).

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/4 completed)              |
| Effort:    [....................] 0% (0/3 points completed)       |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 4 |
| **Completed Tasks** | 0 |
| **Total Effort (points)** | 3 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] 3 rule files have paths frontmatter
- [ ] Rules load only when editing `.py` files
- [ ] Non-Python sessions have reduced token overhead
- [ ] Quality gate passed (>= 0.92)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | architecture-standards.md has paths frontmatter | [ ] |
| TC-2 | coding-standards.md has paths frontmatter | [ ] |
| TC-3 | testing-standards.md has paths frontmatter | [ ] |
| TC-4 | Manual verification that rules load conditionally | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | Scoped architecture-standards.md | `.context/rules/architecture-standards.md` | Pending |
| 2 | Scoped coding-standards.md | `.context/rules/coding-standards.md` | Pending |
| 3 | Scoped testing-standards.md | `.context/rules/testing-standards.md` | Pending |
| 4 | Verification report | -- | Pending |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All technical criteria verified
- [ ] Quality gate score >= 0.92
- [ ] Creator-critic-revision cycle completed (minimum 3 iterations)
- [ ] No regressions introduced

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-012: Progressive Disclosure Rules](../FEAT-012-progressive-disclosure-rules.md)

### Related Items

- **Depends On:** EN-901 (files must be thinned first before adding frontmatter)
- **Related Enabler:** EN-902 (companion guides complement path-scoped enforcement rules)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-16 | Claude | pending | Enabler created under FEAT-012. |
