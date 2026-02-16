# EN-905: Bootstrap Exclusion & Validation

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
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

Ensure the bootstrap script (`scripts/bootstrap_context.py`) does NOT symlink `.context/guides/` to `.claude/guides/`. Guides must remain on-demand (not auto-loaded). Update bootstrap documentation.

**Technical Scope:**
- Verify current `bootstrap_context.py` does not already handle `.context/guides/`
- Add explicit exclusion comment and guard in bootstrap script
- Update `/bootstrap` SKILL.md to document guides exclusion rationale
- Add E2E test verifying guides directory is not in `.claude/` after bootstrap

---

## Problem Statement

The bootstrap script creates symlinks from `.claude/` to `.context/` for rules and patterns. If guides are accidentally symlinked, they would be auto-loaded at session start, defeating the purpose of progressive disclosure.

---

## Business Value

Guarantees the tiered loading architecture works correctly. Guides must only load when Claude explicitly reads them, preserving the token budget for enforcement rules.

### Features Unlocked

- Verified three-tier architecture (rules auto-loaded, patterns auto-loaded, guides on-demand)
- Protection against accidental guide auto-loading
- Documented bootstrap behavior for future contributors

---

## Technical Approach

1. **Verify current `bootstrap_context.py`** does not already handle `.context/guides/`.
2. **Add explicit exclusion comment and guard** in bootstrap script.
3. **Update `/bootstrap` SKILL.md** to document guides exclusion rationale.
4. **Add E2E test** verifying guides directory is not in `.claude/` after bootstrap.

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Activity | Owner |
|----|-------|--------|----------|-------|
| TASK-001 | Verify bootstrap script does NOT symlink .context/guides/ | BACKLOG | REVIEW | -- |
| TASK-002 | Add explicit exclusion guard in bootstrap_context.py | BACKLOG | DEVELOPMENT | -- |
| TASK-003 | Update /bootstrap SKILL.md with guides exclusion rationale | BACKLOG | DOCUMENTATION | -- |
| TASK-004 | E2E test: verify guides not in .claude/ after bootstrap | BACKLOG | DEVELOPMENT | -- |

### Task Dependencies

TASK-001 must complete first (verifies current behavior before modifying). TASK-002 and TASK-003 are independent of each other but depend on TASK-001. TASK-004 depends on TASK-002 completing (tests the guard that was added).

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

- [ ] `bootstrap_context.py` explicitly excludes `.context/guides/`
- [ ] SKILL.md documents exclusion rationale
- [ ] E2E test validates no `.claude/guides/` after bootstrap
- [ ] Quality gate passed (>= 0.92)

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | bootstrap_context.py has explicit guard against guides/ symlink | [ ] |
| TC-2 | `uv run python scripts/bootstrap_context.py --check` passes | [ ] |
| TC-3 | No `.claude/guides/` directory exists after full bootstrap | [ ] |
| TC-4 | SKILL.md documents the three-tier architecture | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | Updated bootstrap_context.py | `scripts/bootstrap_context.py` | Pending |
| 2 | Updated SKILL.md | `skills/bootstrap/SKILL.md` | Pending |
| 3 | E2E test | `tests/e2e/` | Pending |

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

- **Dependencies:** None (can run in parallel with EN-901/EN-902)
- **Related Enabler:** EN-901 (rules thinning -- bootstrap symlinks the thinned rules)
- **Related Enabler:** EN-902 (companion guides -- the content that must NOT be symlinked)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-16 | Claude | pending | Enabler created under FEAT-012. |
