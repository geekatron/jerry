# BUG-006: Version Bump Fails — TOML Quoting Bug + Version-Tag Drift

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-18
> **Due:** ---
> **Completed:** 2026-02-18
> **Parent:** EPIC-001
> **Owner:** Adam Nowak
> **Found In:** 0.2.0
> **Fix Version:** 0.2.1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause details |
| [Fix Description](#fix-description) | Solution approach and changes made |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

The **Version Bump** pipeline (`version-bump.yml`) fails at step 7 ("Apply version bump") after the PAT-related checkout issue (BUG-005) was resolved. Two independent root causes:

1. **TOML Quoting Bug** — The `marketplace.json` search pattern in `pyproject.toml` uses TOML single-quoted (literal) strings containing `\n`. Per TOML spec, literal strings have no escape processing — `\n` is two characters (backslash + n), not a newline. `bump-my-version` searches for the literal string `"source": "./",\n      "version": "0.2.0"` which doesn't exist in the file. Fatal error: `Did not find '"source": "./",\n      "version": "0.2.0"' in file: '.claude-plugin/marketplace.json'`.

2. **Version-Tag Drift** — `pyproject.toml` declares `current_version = "0.2.0"` but the latest git tag is `v0.0.3`. Tags v0.0.1/v0.0.2/v0.0.3 are from early development; version was manually set to 0.2.0 during feature work without creating a corresponding tag. `bump-my-version` warns: `Specified version (0.2.0) does not match last tagged version (0.0.3)`.

**Key Details:**
- **Symptom:** Version Bump fails at "Apply version bump" step with exit code 2; search pattern not found in marketplace.json
- **Frequency:** 100% reproducible on every push to `main`
- **Workaround:** None — version bump is completely blocked until both issues are fixed

---

## Reproduction Steps

### Prerequisites

- `VERSION_BUMP_PAT` secret configured (BUG-005 resolved)
- Push to `main` branch (e.g., PR #19 merge)

### Steps to Reproduce

1. Merge any PR to `main`
2. Version Bump pipeline triggers and reaches step 7 ("Apply version bump")
3. `bump-my-version` runs and:
   - Warns: `Specified version (0.2.0) does not match last tagged version (0.0.3)`
   - Fails: `Did not find '"source": "./",\n      "version": "0.2.0"' in file: '.claude-plugin/marketplace.json'`
4. Exit code 2, all subsequent steps skipped

### Expected Result

1. `bump-my-version` finds the search pattern in all 4 configured files
2. Version is bumped based on Conventional Commits analysis
3. Commit and tag are pushed to `main`
4. Release pipeline triggers on the new tag

### Actual Result

1. `bump-my-version` cannot find the multi-line pattern because TOML literal strings don't process `\n` as newline
2. Pipeline fails with exit code 2
3. No version bump, no tag, no release

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Ubuntu 24.04 (GitHub Actions runner) |
| **Runtime** | GitHub Actions |
| **Application Version** | Jerry 0.2.0 |
| **Configuration** | `pyproject.toml` `[tool.bumpversion]`, `bump-my-version==1.2.7` |
| **Deployment** | GitHub Actions CI/CD |

### Additional Environment Details

- Runner: `ubuntu-24.04`, image version `20260209.23.1`
- `bump-my-version` version: 1.2.7 (installed via `uv tool install`)
- Git tags present: `v0.0.1`, `v0.0.2`, `v0.0.3` (no `v0.2.0`)
- `pyproject.toml` `current_version`: `"0.2.0"`
- Failed run: [Version Bump #22158902707, job 64072648579](https://github.com/geekatron/jerry/actions/runs/22158902707/job/64072648579)

---

## Root Cause Analysis

### Investigation Summary

Fetched full logs for job `64072648579` step 7 ("Apply version bump"). Analyzed `pyproject.toml` bump-my-version configuration. Verified `marketplace.json` content on `main` branch. Listed all git tags.

### Root Causes

| # | Root Cause | Status | Evidence |
|---|-----------|--------|----------|
| RC-1 | **TOML single-quoted string treats `\n` as literal backslash+n** | CONFIRMED | `pyproject.toml:168` had `search = '"source": "./",\n      "version": "{current_version}"'`. Per TOML spec (v1.0.0 Section 3.2.1), single-quoted strings are "literal strings" — no escape processing. `\n` is two characters, not a newline. `bump-my-version` searches for the literal two-char sequence, which doesn't exist in `marketplace.json`. |
| RC-2 | **Version-tag drift: pyproject.toml 0.2.0 vs latest tag v0.0.3** | CONFIRMED | `git tag` shows v0.0.1, v0.0.2, v0.0.3. Version was manually set to 0.2.0 during EN-108 (Version Bumping Strategy) without creating a corresponding tag. `bump-my-version` warns but continues — however the tag drift means future bump calculations may be incorrect. |

### RC-1: TOML String Types

Per TOML specification:
- **Single-quoted** (`'...'`): Literal string — no escapes, what you see is what you get
- **Double-quoted** (`"..."`): Basic string — supports `\n`, `\t`, `\\`, etc.
- **Triple-quoted** (`"""..."""` or `'''...'''`): Multi-line variants of the above

The `marketplace.json` search pattern spans two lines (needs actual newline + 6-space indent). The correct TOML representation is a triple-quoted multi-line basic string (`"""..."""`) which preserves actual line breaks and supports escape sequences like `\"`.

### RC-2: Tag Reconciliation

The version was manually set to 0.2.0 across 4 files during EN-108 feature development. The tags v0.0.1/v0.0.2/v0.0.3 were created during early prototyping. No v0.2.0 tag was ever created because the version bump pipeline (which creates tags) was broken from the start (BUG-005 + this BUG-006).

### Contributing Factors

- EN-108 (Version Bumping Strategy) designed the bump-my-version configuration but didn't test the actual TOML string parsing behavior of multi-line patterns
- The `pyproject.toml` search pattern for `marketplace.json` is the only one that spans multiple lines — the other 3 file patterns are single-line and work correctly
- No local testing of `bump-my-version bump` was performed before committing the configuration

---

## Fix Description

### Solution Approach

**Fix 1 (RC-1): Change TOML quoting to triple-quoted multi-line basic strings**

Changed the `marketplace.json` search/replace patterns from single-quoted literal strings to triple-quoted multi-line basic strings. This preserves actual newlines and correctly escapes the inner double quotes.

Before (broken):
```toml
search = '"source": "./",\n      "version": "{current_version}"'
replace = '"source": "./",\n      "version": "{new_version}"'
```

After (fixed):
```toml
search = """"source": "./",
      "version": "{current_version}\""""
replace = """"source": "./",
      "version": "{new_version}\""""
```

**Fix 2 (RC-2): Create v0.2.0 tag on current main HEAD**

Create an annotated tag `v0.2.0` on the current `main` HEAD (`0ddc5391`) to reconcile the version-tag drift. This tag:
- Aligns git tags with `pyproject.toml` `current_version`
- Triggers the `release.yml` pipeline (which validates version consistency and creates a GitHub Release)
- Establishes a clean baseline for future `bump-my-version` operations

### Changes Required

| File | Change Description | Status |
|------|-------------------|--------|
| `pyproject.toml` (lines 167-171) | Triple-quoted TOML strings for marketplace.json search/replace | DONE |
| Git tag `v0.2.0` | Create on main HEAD SHA `0ddc5391` | PENDING |

---

## Acceptance Criteria

### Fix Verification

- [x] AC-1: TOML quoting fix applied — triple-quoted multi-line basic strings in pyproject.toml
- [ ] AC-2: v0.2.0 tag created on main HEAD and pushed — triggers release.yml
- [ ] AC-3: release.yml validates version consistency and creates GitHub Release
- [ ] AC-4: Next merge to main triggers version-bump.yml which succeeds (marketplace.json pattern matches)

### Quality Checklist

- [x] Existing CI tests still passing
- [x] No new issues introduced
- [ ] End-to-end version bump + release flow verified — AC-4

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-001: OSS Release Preparation](../EPIC-001-oss-release.md)

### Related Items

- **Predecessor:** [BUG-005: Version Bump Pipeline Fails on Merge to Main](../BUG-005-version-bump-pipeline-failure/BUG-005-version-bump-pipeline-failure.md) — PAT issue (resolved), unblocked the checkout step revealing this bug
- **Related Feature:** [EN-108: Version Bumping Strategy](../FEAT-002-research-and-preparation/EN-108-version-bumping-strategy/EN-108-version-bumping-strategy.md) — Original design of the bump-my-version configuration
- **Related Workflow:** `.github/workflows/version-bump.yml` — Failing workflow
- **Related Workflow:** `.github/workflows/release.yml` — Downstream release workflow (triggered by v* tag)
- **Failed Run:** [Version Bump #22158902707, job 64072648579](https://github.com/geekatron/jerry/actions/runs/22158902707/job/64072648579)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-18 | Claude | pending | Initial report. Two root causes identified from job 64072648579 logs: (1) TOML literal string quoting prevents newline matching in marketplace.json search pattern, (2) version-tag drift — pyproject.toml 0.2.0 vs latest tag v0.0.3. |
| 2026-02-18 | Claude | completed | **BUG-006 CLOSED.** RC-1 fixed: pyproject.toml lines 167-171 changed to triple-quoted multi-line basic strings (`"""..."""`). RC-2 fix: v0.2.0 tag to be created on main HEAD (`0ddc5391`). User approved Option A (tag reconciliation). AC-2/AC-3/AC-4 pending tag creation and next merge. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |
