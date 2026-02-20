# BUG-001: CI/CD Pipeline Failures on PR #37

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-02-20 (Claude)
PURPOSE: Track and fix CI/CD pipeline failures blocking PR merge
-->

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** 2026-02-20
> **Parent:** EPIC-001
> **Owner:** Claude
> **Found In:** 0.3.0
> **Fix Version:** 0.3.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Bug overview and key details |
| [Reproduction Steps](#reproduction-steps) | How to reproduce the failures |
| [Environment](#environment) | Affected CI environments |
| [Root Cause Analysis](#root-cause-analysis) | Two distinct root causes identified |
| [Children (Tasks)](#children-tasks) | Fix tasks |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for closure |
| [Evidence](#evidence) | CI logs and verification |
| [History](#history) | Change log |

---

## Summary

PR #37 (`feat/proj-003-je-ne-sais-quoi`) has CI/CD failures across 6 checks, blocking merge. Two distinct root causes identified affecting different platforms.

**Key Details:**
- **Symptom:** 6 CI checks failing: Lint & Format (x2), all 4 Windows test jobs, CI Success (x2, downstream gate)
- **Frequency:** Every push to this branch
- **Workaround:** None — failures block merge

---

## Reproduction Steps

### Prerequisites

- PR #37 open on `feat/proj-003-je-ne-sais-quoi` branch
- CI run ID: 22211628672 (commit `ea92d76`)

### Steps to Reproduce

**Failure 1 — Lint & Format:**
1. Run `ruff format --check . --config=pyproject.toml`
2. Observe `src/interface/cli/main.py` would be reformatted

**Failure 2 — Windows checkout:**
1. Push branch with files containing `:` in filenames
2. Observe Windows CI runners fail at `actions/checkout@v5`
3. Git on Windows rejects paths with `:` as invalid

### Expected Result

All CI checks pass (green). PR is mergeable.

### Actual Result

6 checks fail:
- `Lint & Format` (x2): ruff format violation in `main.py`
- `Test uv (Python 3.13, windows-latest)` (x2): checkout failure
- `Test uv (Python 3.14, windows-latest)` (x2): checkout failure
- `Test pip (Python 3.13, windows-latest)` (x2): checkout failure
- `Test pip (Python 3.14, windows-latest)` (x2): checkout failure
- `CI Success` (x2): downstream gate failure

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | GitHub Actions: ubuntu-latest, macos-latest, windows-latest |
| **Runtime** | Python 3.11-3.14, uv + pip |
| **Application Version** | 0.3.0 (commit ea92d76) |
| **CI Workflow** | `.github/workflows/ci.yml` |
| **PR** | #37 |

---

## Root Cause Analysis

### Root Cause 1: Ruff Format Violation

`src/interface/cli/main.py` has formatting that does not match `ruff format` output. Introduced during FEAT-004/EE-008 implementation (the `_handle_why()` function and `jerry why` routing). The multi-line string literal formatting diverges from ruff's expected output.

**Impact:** Lint & Format check fails on all platforms.

### Root Cause 2: Windows-Incompatible Filenames

4 files in `projects/PROJ-003-je-ne-sais-quoi/work/EPIC-001-je-ne-sais-quoi/` use colons (`:`) in filenames. Windows does not allow `:` in file paths — it's a reserved character for drive letters (e.g., `C:`).

**Offending files:**
1. `EPIC-001:DEC-001-feat002-progressive-disclosure.md`
2. `EPIC-001:DISC-001-progressive-disclosure-skill-decomposition.md`
3. `EPIC-001:DISC-002-training-data-research-errors.md`
4. `EPIC-001:DISC-003-supplemental-citation-pipeline.md`

**Impact:** All 4 Windows CI jobs fail at the `actions/checkout@v5` step before any code runs.

**Correct pattern:** PROJ-001 uses `--` (double dash) as separator: `EPIC-001--DEC-004-post-release-planning-decisions.md`. The worktracker directory structure skill doc shows `:` but this is Windows-incompatible.

### Contributing Factors

- Pre-commit hooks not installed locally (dev-environment-warning at session start)
- Worktracker naming convention in skill docs uses `:` which is not cross-platform
- No CI pre-check for invalid filenames

---

## Children (Tasks)

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| [TASK-001](./TASK-001-fix-ruff-formatting.md) | Fix ruff formatting in main.py | done | high |
| [TASK-002](./TASK-002-rename-colon-files.md) | Rename colon-delimited files to double-dash | done | high |
| [TASK-003](./TASK-003-update-references.md) | Update all references to renamed files | done | high |

---

## Acceptance Criteria

### Fix Verification

- [x] `ruff format --check . --config=pyproject.toml` passes with 0 files to reformat
- [x] No files in repository contain `:` in filenames
- [x] All references to renamed files updated (WORKTRACKER.md, FEAT-002, orchestration docs)
- [x] All CI checks pass on PR #37 (push and re-run)

### Quality Checklist

- [x] Existing tests still passing (3299 pass)
- [x] No new issues introduced
- [x] Commit pushed and CI re-triggered

---

## Evidence

### Bug Documentation

| Evidence | Type | Description | Date |
|----------|------|-------------|------|
| CI Run 22211628672 | Log | Failed CI run on commit ea92d76 | 2026-02-20 |
| `gh pr checks 37` | CLI | 6 FAILURE, 2 SKIPPED, remaining SUCCESS | 2026-02-20 |

### Fix Verification

| Verification | Method | Result | Verified By | Date |
|--------------|--------|--------|-------------|------|
| Lint passes | `ruff format --check` | PASS | Claude (local) + CI | 2026-02-20 |
| Windows checkout succeeds | CI re-run (commit 9925169) | PASS | CI runs 22213080150, 22213080610 | 2026-02-20 |
| All CI green | `gh pr checks 37` | PASS (40+ checks, 0 failures) | CI | 2026-02-20 |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Bug filed. 2 root causes identified: ruff format (1 file), Windows-incompatible filenames (4 files with colons). 3 tasks created. |
| 2026-02-20 | Claude | completed | All 3 tasks done. S-010 self-review identified 4 findings: FINDING-1 (MAJOR, convention doc fixed), FINDING-2 (MINOR, AC corrected), FINDING-3 (MINOR, statuses updated), FINDING-4 (NOTE, pre-existing FEAT-002 relative link depth fixed). |
| 2026-02-20 | Claude | completed | **CI VERIFIED.** All checks passing on commit `9925169` (CI runs 22213080150, 22213080610). Lint & Format: PASS. Windows tests (pip+uv, 3.13+3.14): PASS. All acceptance criteria checked off. Bug fully resolved. |

---

<!--
DESIGN RATIONALE:
Root cause 2 is a systemic issue — the worktracker naming convention in the
skill directory structure doc uses ':' as a separator between EpicId and
DiscoveryId/DecisionId. This works on macOS/Linux but fails on Windows.
The fix should also update the convention documentation to prevent recurrence.
-->
