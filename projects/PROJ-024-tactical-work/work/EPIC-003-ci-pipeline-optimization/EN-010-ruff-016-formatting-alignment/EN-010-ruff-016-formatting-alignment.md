# EN-010: Ruff 0.16.1 Formatting Alignment

> **Type:** enabler
> **Status:** completed
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-08-05
> **Completed:** 2026-08-06
> **Parent:** EPIC-003
> **GitHub Issue:** [#339](https://github.com/geekatron/jerry/issues/339)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Enabler scope |
| [Problem Statement](#problem-statement) | Why this enabler exists |
| [Technical Approach](#technical-approach) | How the alignment is delivered |
| [Children (Tasks)](#children-tasks) | Task decomposition |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [History](#history) | Status changes |

---

## Summary

Align the repository with ruff 0.16.1's formatter so Dependabot PR [#334](https://github.com/geekatron/jerry/pull/334) (dev-tool group bump including ruff 0.15.22 → 0.16.1) can merge. Ruff 0.16 changed formatter behavior — notably formatting of Python code blocks embedded in Markdown — so `ruff format --check` flags dozens of `.context/` documentation files that were clean under 0.15, failing PR #334's Static Analysis job. No code defect; the formatting standard changed.

> **Note (2026-08-05):** EPIC-003 (CI Pipeline Optimization) was reopened from `completed` to host this follow-on CI maintenance enabler — it is thematically in-scope (CI pipeline health) and the reopen/close window is documented in EPIC-003's History for auditability.

---

## Problem Statement

The repo has a formatter version skew: the pre-commit ruff hook was already bumped to 0.16.1 (Dependabot PR #332, merged), while the project dev dependency pins ruff 0.15.22. Dependabot PR #334 aligns the dev dependency — and that alignment surfaces the accumulated formatting drift, turning PR #334 red and blocking all four dev-tool updates in its group (filelock, ruff, bump-my-version, pre-commit).

---

## Technical Approach

Apply the new formatter's output as a formatting-only commit pushed directly onto the Dependabot PR branch (`dependabot/uv/uv-minor-patch-15189980de`), using the branch's own locked ruff 0.16.1 so the formatting matches what CI checks. Verify `ruff format --check` and `ruff check` both pass locally before pushing. No logic changes.

---

## Children (Tasks)

| ID | Title | Status |
|----|-------|--------|
| TASK-036 | Reformat repository with ruff 0.16.1 on Dependabot PR #334 branch | completed (2026-08-05) |

---

## Acceptance Criteria

- [x] Formatting commits pushed to the Dependabot PR #334 branch; `ruff format --check` passes with ruff 0.16.1 over the full repository with no exclusions (commits 028f5294, 63dee470)
- [x] `ruff check` (lint) still passes after reformatting — no new violations introduced
- [x] All CI checks on PR #334 are green (15/15 pass, including full test matrix)
- [x] No behavioral changes: diff contains only formatting, legacy-entity schema conformance, 3 report renames, and changelog entries (full test suite green on PR #334)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-08-05 | in_progress | Created after owner merged PR #338 and asked why PR #334's CI was red. Root cause: ruff 0.16 formatter behavior change. GH issue #339 opened for H-32 parity. EPIC-003 reopened to host this enabler. |
| 2026-08-05 | completed | TASK-036 initial delivery: 157 live-doc files reformatted, but with a projects/** formatter exclusion (commits 028f5294, f891861d). PR #334 15/15 green. GH #339 closed. |
| 2026-08-06 | completed | Owner review on PR #340 rejected the exclusion (CHANGES_REQUESTED: shortcut to avoid work). Corrected in commit 63dee470: exclusion reverted, remaining 167 projects/ files reformatted, 8 legacy PROJ-001 entities schema-conformed, 3 misnamed critic reports renamed. PR #334 15/15 green with zero exclusions. |
