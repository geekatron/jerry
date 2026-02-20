# BUG-011: project-workflow.md Duplicates and Conflicts with /worktracker Skill Rules

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** --
> **Parent:** EPIC-001
> **Owner:** --
> **Found In:** 0.2.3
> **Fix Version:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause details |
| [Children (Tasks)](#children-tasks) | Task breakdown for fix |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

`.context/rules/project-workflow.md` (auto-loaded at every session start via `.claude/rules/` symlink) independently redefines project directory structure, workflow phases, and project creation logic that is already authoritatively defined in the `/worktracker` skill rules (`skills/worktracker/rules/`). This creates two competing sources of truth for the same concepts, where changes to the worktracker skill rules will not propagate to `project-workflow.md`, causing silent drift.

**Key Details:**
- **Symptom:** Two independent definitions of the same concepts — project directory structure, workflow lifecycle, project creation — with no cross-reference between them
- **Frequency:** Every session — `project-workflow.md` is auto-loaded at session start; `/worktracker` rules are loaded on skill invocation
- **Workaround:** Manually ensuring consistency between both files after any change

---

## Reproduction Steps

### Prerequisites

- Jerry Framework repository with `.context/rules/project-workflow.md` and `skills/worktracker/rules/*`

### Steps to Reproduce

1. Read `.context/rules/project-workflow.md` — observe "Project Structure" section (lines 34-43) defines a simplified 7-line directory tree
2. Read `skills/worktracker/rules/worktracker-directory-structure.md` — observe the authoritative 90-line directory tree with full entity hierarchy
3. Compare: `project-workflow.md` is a lossy subset that omits entity folder patterns, naming conventions, and containment rules
4. Read `.context/rules/project-workflow.md` "Workflow Phases" (lines 24-28) — defines before/during/after workflow
5. Read `skills/worktracker/rules/worktracker-behavior-rules.md` — defines WTI-001 through WTI-007 integrity rules
6. Compare: `project-workflow.md` workflow phases don't reference or enforce WTI rules

### Expected Result

- `.context/rules/project-workflow.md` should reference the worktracker skill rules as the authoritative source
- Project structure, workflow lifecycle, and entity rules should be defined in ONE place (worktracker skill)
- Session-start rules should provide pointers, not redefinitions

### Actual Result

- Two independent definitions of project structure exist
- Workflow phases in `project-workflow.md` don't reference WTI integrity rules
- No cross-reference between the files
- Changes to worktracker rules silently drift from `project-workflow.md`

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | All (framework-level issue) |
| **Runtime** | Claude Code with Jerry Framework |
| **Application Version** | Jerry 0.2.3 |
| **Configuration** | `.context/rules/project-workflow.md`, `skills/worktracker/rules/*` |
| **Deployment** | All Jerry development sessions |

---

## Root Cause Analysis

### Investigation Summary

Compared `.context/rules/project-workflow.md` against the authoritative worktracker skill rules in `skills/worktracker/rules/`. Found three categories of duplication:

1. **Directory structure duplication**: `project-workflow.md` lines 34-43 define a simplified project directory tree. `worktracker-directory-structure.md` defines the full 90-line authoritative tree. The simplified version is a lossy subset — it omits Epic/Feature/Enabler/Story entity folders, naming conventions (`{EntityId}-{slug}`), containment rules, and the distinction between project-based and repository-based patterns.

2. **Workflow phase overlap**: `project-workflow.md` lines 24-28 define before/during/after workflow phases. The worktracker behavior rules define WTI-001 (Real-Time State Updates), WTI-002 (No Closure Without Verification), WTI-003 (Truthful State), WTI-004 (Synchronize Before Reporting), WTI-005 (Atomic Task State), WTI-006 (Evidence-Based Closure), WTI-007 (Mandatory Template Usage). The workflow phases are a high-level abstraction that doesn't reference these enforcement rules.

3. **Project creation logic**: `project-workflow.md` lines 49-62 define project resolution and creation logic. This should reference the worktracker directory structure rules for folder layout and the entity hierarchy for ID generation.

### Root Cause

`project-workflow.md` was created during the EN-202 CLAUDE.md rewrite (BUG-006: "Working with Jerry section lost") as a rescue of content being extracted from the monolithic CLAUDE.md. It was written as a standalone rule file rather than as a reference/pointer to the worktracker skill rules. The worktracker skill rules were being developed concurrently in EN-201, and the two were never reconciled.

### Contributing Factors

- EN-201 (worktracker skill extraction) and EN-202 (CLAUDE.md rewrite) were executed in the same session without cross-referencing
- `.context/rules/` files are auto-loaded, so `project-workflow.md` takes effect at session start — before `/worktracker` is invoked
- No validation exists to detect duplication between `.context/rules/` and skill rule files
- The simplified structure in `project-workflow.md` may have been intentional at the time (keeping session-start rules lightweight) but was never documented as a deliberate subset

---

## Children (Tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Rewrite `project-workflow.md` to reference worktracker skill rules as SSOT | pending | 2 |
| TASK-002 | Verify no behavioral drift after rewrite (test session start behavior) | pending | 1 |

---

## Acceptance Criteria

### Fix Verification

- [ ] AC-1: `project-workflow.md` references `skills/worktracker/rules/worktracker-directory-structure.md` as authoritative source for project structure — no inline duplication
- [ ] AC-2: `project-workflow.md` references `skills/worktracker/rules/worktracker-behavior-rules.md` for WTI integrity rules — workflow phases point to WTI rules
- [ ] AC-3: Project creation logic references the worktracker directory structure for folder layout
- [ ] AC-4: No independent/conflicting definitions remain in `project-workflow.md`
- [ ] AC-5: Session-start behavior unchanged (H-04 active project requirement still enforced)

### Quality Checklist

- [ ] Existing tests still passing
- [ ] No new issues introduced

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-001: OSS Release Preparation](../EPIC-001-oss-release.md)

### Related Items

- **Causing Change:** EN-202 (CLAUDE.md Rewrite) — created `project-workflow.md` as standalone rule file during content rescue
- **Conflicting Source:** `skills/worktracker/rules/worktracker-directory-structure.md` — authoritative directory structure
- **Conflicting Source:** `skills/worktracker/rules/worktracker-behavior-rules.md` — authoritative WTI rules
- **AE-002 Note:** Fix will touch `.context/rules/` — auto-C3 minimum criticality
- **GitHub Issue:** [#38](https://github.com/geekatron/jerry/issues/38)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Created. `project-workflow.md` independently redefines project structure, workflow phases, and project creation logic that is authoritatively defined in `/worktracker` skill rules. Two competing SSOTs for the same concepts. Root cause: EN-201/EN-202 concurrent execution without reconciliation. |

---
