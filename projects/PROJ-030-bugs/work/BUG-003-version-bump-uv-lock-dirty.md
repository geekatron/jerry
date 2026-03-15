# BUG-003: version-bump workflow fails — uv.lock dirty after uv sync

> **Type:** bug
> **Status:** completed
> **Priority:** critical
> **Impact:** critical
> **Severity:** critical
> **Created:** 2026-03-09T00:00:00Z
> **Due:**
> **Completed:** 2026-03-09T00:00:00Z
> **Parent:** PROJ-030-bugs
> **Owner:** Claude
> **Found In:** 0.24.0
> **Fix Version:** 0.25.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Steps to Reproduce](#steps-to-reproduce) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause details |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

The `version-bump.yml` GitHub Actions workflow fails because `uv sync` resolves dependencies against Python 3.14 and modifies `uv.lock`, making the git working directory dirty. `bump-my-version` is configured with `allow_dirty = false` and exits with error code 2.

Additionally, ~40 version bump commits exist (v0.3.0 through v0.24.0) with zero corresponding git tags — only v0.0.1 through v0.2.2 exist as tags. The `--since-tag` flag in `jerry ci detect-bump-type` scans the entire commit history back to v0.2.2, causing every merge to main to trigger a bump attempt.

**Key Details:**
- **Symptom:** Version bump workflow fails with "Git working directory is not clean: M uv.lock"
- **Frequency:** Every workflow run where `uv sync` modifies `uv.lock` (intermittent, depends on Python version drift)
- **Workaround:** Manual `workflow_dispatch` after resetting `uv.lock` locally

---

## Steps to Reproduce

### Prerequisites

- Jerry Framework repository with version-bump.yml workflow
- GitHub Actions runner with Python 3.14

### Steps to Reproduce

1. Push a conventional commit (e.g., `feat: new feature`) to main
2. Version-bump workflow triggers
3. `uv python install 3.14` installs Python 3.14
4. `uv sync` resolves dependencies against Python 3.14 and modifies `uv.lock`
5. `bump-my-version bump "minor"` fails because `uv.lock` is dirty and `allow_dirty = false`

### Expected Result

Version bump succeeds: commit created, tag created, pushed to main.

### Actual Result

Workflow exits with error code 2: "Git working directory is not clean: M uv.lock"

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | ubuntu-latest (GitHub Actions) |
| **Browser/Runtime** | Python 3.14 via `uv python install 3.14` |
| **Application Version** | 0.24.0 |
| **Configuration** | `pyproject.toml` line 158: `allow_dirty = false` |
| **Deployment** | GitHub Actions CI |

---

## Root Cause Analysis

### Root Cause

`uv sync` without `--frozen` re-resolves dependencies against the current Python interpreter. When the CI Python version (3.14) differs from the version used to generate `uv.lock` locally, the lockfile is updated with new resolution markers, making the working directory dirty.

### Contributing Factors

- No `--frozen` flag on `uv sync` in CI (CI should install from lockfile, not re-resolve)
- `allow_dirty = false` correctly prevents unintended files from being committed, but no lockfile reset step exists
- ~40 missing git tags cause `--since-tag` to scan full history, amplifying the impact (every merge triggers a bump)
- Bump commit message format mismatch: commits use "Bump version: X -> Y" but pyproject.toml configures "chore(release): ..."

---

## Acceptance Criteria

### Fix Verification

- [ ] Version-bump workflow succeeds on push to main without `uv.lock` dirty error
- [ ] `uv sync --frozen` used in CI to prevent lockfile modification
- [ ] Fail-fast guard added before bump-my-version: if tree is unexpectedly dirty despite `--frozen`, fail loudly with diagnostic output instead of silently recovering
- [ ] Missing git tags created for all version bump commits (v0.3.0 through v0.24.0)
- [ ] `--since-tag` correctly scans only commits since the most recent tag

### Quality Checklist

- [ ] Existing tests still passing
- [ ] No new issues introduced
- [ ] Workflow tested via `workflow_dispatch`

---

## Related Items

### Hierarchy

- **Parent:** [PROJ-030-bugs](../WORKTRACKER.md)

### Related Items

- **GitHub Issue:** [#151](https://github.com/geekatron/jerry/issues/151)
- **Related Bug:** [BUG-002](BUG-002-version-bump-case-sensitivity.md) — prior version-bump workflow bug
- **Failed Run:** GitHub Actions run #22785344352
- **Security Review:** [bug-003-devsecops-security-review.md](../reviews/bug-003-devsecops-security-review.md)
- **Steelman:** [bug-003-s003-steelman.md](../reviews/bug-003-s003-steelman.md)
- **Attack Surface:** [bug-003-red-recon-attack-surface.md](../reviews/bug-003-red-recon-attack-surface.md)
- **Quality Score:** [bug-003-quality-score.md](../reviews/bug-003-quality-score.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-09 | Claude | pending | Initial report from GitHub Issue #151 |
| 2026-03-09 | Claude | in_progress | Investigation and fix started |
| 2026-03-09 | Claude | completed | Fixed with uv sync --frozen + SHA-pinned actions. Spawned EN-001 for systemic CI hardening. |
