# BUG-011: project-workflow.md Duplicates and Conflicts with /worktracker Skill Rules

> **Type:** bug
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** 2026-02-19
> **Parent:** EPIC-001
> **Owner:** --
> **Found In:** 0.2.3
> **Fix Version:** 0.2.4

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause details |
| [Children (Tasks)](#children-tasks) | Task breakdown for fix |
| [Evidence](#evidence) | Bug documentation and fix verification |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

`.context/rules/project-workflow.md` (auto-loaded at every session start via `.claude/rules/` hardlink) independently redefines project directory structure and project creation logic that is already authoritatively defined in the `/worktracker` skill rules (`skills/worktracker/rules/`). The session-start file carries a lossy subset of the worktracker directory structure with no cross-reference to the authoritative source, creating a maintenance risk where changes to the worktracker skill rules silently drift from the session-start definitions.

**Severity rationale:** Classified MAJOR due to maintenance risk of silent drift in a HARD-rule file (auto-loaded every session), not a confirmed functional failure. No behavioral error has been observed to date, but the drift risk is unbounded as worktracker rules evolve.

**Key Details:**
- **Symptom:** Independent definition of project directory structure (7-line simplified tree) and project creation logic with no cross-reference to the authoritative 90-line worktracker directory structure; workflow phases lack reference to WTI integrity rules
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

2. **Workflow phase cross-reference gap**: `project-workflow.md` lines 24-28 define before/during/after workflow phases. The worktracker behavior rules define WTI-001 through WTI-007 integrity rules. The workflow phases are a complementary high-level abstraction (not a conflicting redefinition) but lack any cross-reference to the WTI rules they should enforce. This is a missing-reference issue, not a competing-definition issue.

3. **Project creation logic**: `project-workflow.md` lines 49-62 define project resolution and creation logic. This should reference the worktracker directory structure rules for folder layout and the entity hierarchy for ID generation.

### Root Cause

**Primary:** The Jerry enforcement architecture separates session-start rules (`.context/rules/`, auto-loaded every session, L1 layer) from skill-scoped rules (`skills/*/rules/`, loaded on-demand). This architectural split means `project-workflow.md` operates at session start without access to `/worktracker` rules, creating pressure to inline structural content rather than reference it. The file was written as a standalone definition because the on-demand skill rules were not available at session start.

**Contributing:** `project-workflow.md` was created during EN-202 (CLAUDE.md rewrite, BUG-006: "Working with Jerry section lost") as a rescue of content being extracted from the monolithic CLAUDE.md. EN-201 (worktracker skill extraction) was developing the authoritative rules concurrently. The two were never reconciled — both define project structure independently.

### Contributing Factors

- EN-201 (worktracker skill extraction) and EN-202 (CLAUDE.md rewrite) were executed in the same session without cross-referencing
- `.context/rules/` files are auto-loaded (L1 layer), `skills/*/rules/` files are loaded on-demand — architectural separation makes duplication tempting
- No validation exists to detect duplication between `.context/rules/` and skill rule files
- The simplified structure in `project-workflow.md` may have been intentional (keeping session-start rules lightweight for context budget per L1 enforcement architecture) but was never documented as a deliberate subset — this makes it impossible to distinguish intentional summary from accidental duplication

---

## Children (Tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Rewrite `project-workflow.md` to reference worktracker skill rules as SSOT | done | 2 |
| TASK-002 | Verify no behavioral drift after rewrite (test session start behavior) | done | 1 |

---

## Evidence

### Bug Documentation

| Evidence | Type | Description | Date |
|----------|------|-------------|------|
| `.context/rules/project-workflow.md` lines 34-43 | File content | Inline 7-line project directory tree (competing definition) | 2026-02-19 |
| `skills/worktracker/rules/worktracker-directory-structure.md` | File content | Authoritative 90-line directory tree (SSOT) | 2026-02-19 |
| `/adversary` C2 review | Review output | SR-001 (CRITICAL), DA-001/DA-002 (MAJOR) — hardlink misidentification, session-start blind spot risk | 2026-02-19 |

### Fix Verification

| Evidence | Type | Description | Date |
|----------|------|-------------|------|
| Rewritten `project-workflow.md` | File | Inline tree removed, SSOT references added, minimal orientation retained | 2026-02-19 |
| TASK-002 verification | Test output | Hardlink (inode 51639207), H-04 present, references resolve, 3299 tests pass | 2026-02-19 |
| `/adversary` C3 review | Score report | S-014 score 0.970 (PASS). 8 strategies: S-010, S-003, S-002, S-004, S-007, S-012, S-013, S-014 | 2026-02-19 |

### Verification Checklist

- [x] Bug no longer reproducible with original steps
- [x] No new issues introduced

---

## Acceptance Criteria

### Fix Verification

- [x] AC-1: `project-workflow.md` references `skills/worktracker/rules/worktracker-directory-structure.md` as authoritative source for project structure — no inline competing definition
- [x] AC-2: Workflow phases include cross-reference to WTI integrity rules in `skills/worktracker/rules/worktracker-behavior-rules.md`
- [x] AC-3: Project creation logic references the worktracker directory structure for folder layout
- [x] AC-4: Minimal structural orientation retained at session start (per DA-002: Claude must have basic project navigation context without requiring `/worktracker` invocation)
- [x] AC-5: Session-start behavior unchanged (H-04 active project requirement still enforced)
- [x] AC-6: `/adversary` C3 review PASS — score 0.970 (threshold 0.92). 8 strategies executed across 2 iterations.

### Quality Checklist

- [x] Existing tests still passing (3299 passed, 63 skipped)
- [x] No new issues introduced

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-001: OSS Release Preparation](../EPIC-001-oss-release.md)

### Related Items

- **Causing Change:** [EN-202](../FEAT-003-claude-md-optimization/EN-202-claude-md-rewrite/) (CLAUDE.md Rewrite) — created `project-workflow.md` as standalone rule file during content rescue
- **Causing Change:** EN-201 (Worktracker Skill Extraction) — developed the authoritative worktracker rules concurrently without reconciliation
- **Conflicting Source:** `skills/worktracker/rules/worktracker-directory-structure.md` — authoritative directory structure
- **Conflicting Source:** `skills/worktracker/rules/worktracker-behavior-rules.md` — authoritative WTI rules
- **AE-002 Note:** Fix will touch `.context/rules/` (hardlink to `.claude/rules/`) — auto-C3 minimum criticality
- **GitHub Issue:** [#38](https://github.com/geekatron/jerry/issues/38)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Created. `project-workflow.md` independently redefines project structure, workflow phases, and project creation logic that is authoritatively defined in `/worktracker` skill rules. Two competing SSOTs for the same concepts. Root cause: EN-201/EN-202 concurrent execution without reconciliation. |
| 2026-02-19 | Claude | pending | /adversary C2 review (S-010, S-003, S-002, S-007). 1 CRITICAL (SR-001: hardlink misidentified as symlink), 6 MAJOR (DA-001 intentional-summary hypothesis, DA-002 session-start blind spot, SR-002 root cause hierarchy, SR-003 unresolvable EN refs, SR-004 workflow phases scope, CA-002 missing Evidence section), 7 MINOR. All addressed: elevated architectural root cause, added Evidence section, narrowed workflow scope to cross-reference gap, retained minimal structural orientation (DA-002), fixed hardlink references, added EN-201 to Related Items. |
| 2026-02-19 | Claude | done | Fix complete. TASK-001 (rewrite) and TASK-002 (verify) both done. /adversary C3 review: 8 strategies, 2 iterations, final score 0.970 (PASS). C3 findings applied: WTI IDs-only (no drift-prone names), HARD enforcement signal, dual-pattern note, /worktracker invocation in Project Resolution. All ACs verified. 3299 tests pass. |

---
