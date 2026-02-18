# BUG-005: Version Bump Pipeline Fails on Merge to Main

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-18
> **Due:** ---
> **Completed:** ---
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

The **Version Bump** pipeline (`version-bump.yml`) fails immediately on every push to `main` because the `Checkout repository` step requires a Personal Access Token (PAT) via `${{ secrets.VERSION_BUMP_PAT }}`, but this secret is not configured in the GitHub repository. The checkout step fails with: `Input required and not supplied: token`.

Additionally, the **CI** pipeline (`ci.yml`) runs independently on the same push event and succeeds, despite the upstream version bump having failed. This is a workflow design issue: CI and Version Bump are independent parallel workflows triggered by the same `push` event, with no dependency relationship between them. This means a successful CI run can produce a false sense of confidence, masking the broken version bump.

**Key Details:**
- **Symptom:** Version Bump fails at `Checkout repository` step; CI runs and passes independently
- **Frequency:** 100% reproducible on every push to `main`
- **Workaround:** Manual version bump via `workflow_dispatch` with PAT configured, or configure the `VERSION_BUMP_PAT` secret

---

## Reproduction Steps

### Prerequisites

- PR merged to `main` branch (e.g., PR #19)
- `VERSION_BUMP_PAT` secret NOT configured in repo settings

### Steps to Reproduce

1. Merge any PR to `main`
2. Observe two GitHub Actions workflows triggered simultaneously:
   - **Version Bump** (run [22158902707](https://github.com/geekatron/jerry/actions/runs/22158902707))
   - **CI** (run [22158902717](https://github.com/geekatron/jerry/actions/runs/22158902717))
3. Version Bump fails at step 2 (`Checkout repository`) with error:
   ```
   ##[error]Input required and not supplied: token
   ```
4. All subsequent steps (3-10) are skipped
5. CI pipeline runs independently and succeeds (all 26 jobs pass)

### Expected Result

1. Version Bump pipeline checks out the repo, determines bump type from Conventional Commits, applies the version bump, pushes the tag, which then triggers the Release pipeline
2. CI should either (a) have a dependency on Version Bump success, or (b) be clearly documented as independent

### Actual Result

1. Version Bump fails at checkout because `secrets.VERSION_BUMP_PAT` is undefined
2. No version bump occurs, no tag is created, no release is triggered
3. CI runs and passes independently, creating a misleading green status

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Ubuntu 24.04 (GitHub Actions runner) |
| **Runtime** | GitHub Actions |
| **Application Version** | Jerry 0.2.0 |
| **Configuration** | `.github/workflows/version-bump.yml` uses `${{ secrets.VERSION_BUMP_PAT }}` |
| **Deployment** | GitHub Actions CI/CD |

### Additional Environment Details

- Runner: `ubuntu-24.04`, image version `20260209.23.1`
- Actions versions: `actions/checkout@v5`, `astral-sh/setup-uv@v5`
- Token permissions granted: `contents: write`, `metadata: read`
- The `GITHUB_TOKEN` default token has `contents: write` but is NOT used by the checkout step (workflow explicitly uses `secrets.VERSION_BUMP_PAT` instead)

---

## Root Cause Analysis

### Investigation Summary

Analyzed both GitHub Actions runs (`22158902707` for Version Bump, `22158902717` for CI) and all 4 workflow files (`ci.yml`, `version-bump.yml`, `release.yml`, `pat-monitor.yml`).

### Root Causes

| # | Root Cause | Status | Evidence |
|---|-----------|--------|----------|
| RC-1 | **Missing `VERSION_BUMP_PAT` secret** | CONFIRMED | `version-bump.yml:54` uses `token: ${{ secrets.VERSION_BUMP_PAT }}` in the checkout step. Error message: `Input required and not supplied: token`. When the secret is undefined, the `token` input evaluates to empty string, which `actions/checkout@v5` rejects as missing required input. |
| RC-2 | **CI pipeline has no dependency on Version Bump** | CONFIRMED | `ci.yml` triggers on `push: branches: ["**"]` — a wildcard matching ALL branches including `main`. `version-bump.yml` also triggers on `push: branches: [main]`. Both workflows are triggered by the same push event as independent, parallel workflows. There is no `workflow_run` or `needs` dependency between them. |

### RC-1: Why is `VERSION_BUMP_PAT` needed?

The version bump workflow needs to push a commit and tag back to `main`. The default `GITHUB_TOKEN` provided by GitHub Actions has limited scope:
- It CAN push to the branch, but pushes made with `GITHUB_TOKEN` do NOT trigger subsequent workflows (by design, to prevent infinite loops)
- The `release.yml` workflow triggers on `push: tags: ["v*"]` — if the tag is created with `GITHUB_TOKEN`, the Release workflow would NOT fire
- A PAT (Personal Access Token) with `repo` scope bypasses this limitation, allowing the version bump commit + tag to trigger the Release pipeline

The workflow was designed correctly (EN-108: Version Bumping Strategy), but the PAT was never created and configured as a repository secret.

### RC-2: Why does CI run independently?

The CI workflow (`ci.yml`) is designed to run on ALL pushes to ANY branch:
```yaml
on:
  push:
    branches: ["**"]
```

This is correct for development branches (you want CI on every push). However, for pushes to `main`, the intended flow is:

```
Push to main → Version Bump → (tag push) → Release
                    ↑ CI also runs (independent)
```

The CI and Version Bump workflows are separate YAML files in `.github/workflows/`, and GitHub Actions treats each as an independent workflow. There is no built-in mechanism to make one block the other unless:
1. One workflow uses `workflow_run` event to depend on another, OR
2. Branch protection rules require specific status checks

### Contributing Factors

- **EN-108 (Version Bumping Strategy)** designed the PAT-based approach but the actual secret was never provisioned in GitHub repo settings
- The `pat-monitor.yml` workflow exists to monitor PAT health, suggesting the PAT was planned but not yet configured
- No documentation in INSTALLATION.md or CONTRIBUTING.md about the required GitHub secrets for CI/CD
- The `if` condition in `version-bump.yml` (line 47) passes correctly — the failure is at step execution, not job-level filtering

---

## Fix Description

### Solution Approach

**Fix 1 (REQUIRED): Configure `VERSION_BUMP_PAT` repository secret**

Create a GitHub Personal Access Token (classic or fine-grained) with `repo` scope and add it as `VERSION_BUMP_PAT` in the repository's Settings > Secrets and variables > Actions.

**Token requirements:**
- **Scope:** `repo` (full control of private repositories) for classic PAT, or `contents: write` for fine-grained PAT
- **Expiration:** Set per org policy (recommended: 90 days with `pat-monitor.yml` alerting)
- **Name in GitHub Secrets:** `VERSION_BUMP_PAT`

**Fix 2 (RECOMMENDED): Add fallback to `GITHUB_TOKEN`**

If `VERSION_BUMP_PAT` is not configured, the workflow should fall back to `GITHUB_TOKEN` with a warning that the Release pipeline won't be triggered automatically:

```yaml
- name: Checkout repository
  uses: actions/checkout@v5
  with:
    fetch-depth: 0
    token: ${{ secrets.VERSION_BUMP_PAT || github.token }}
```

Add a warning step:
```yaml
- name: Warn if using default token
  if: ${{ !secrets.VERSION_BUMP_PAT }}
  run: |
    echo "::warning::VERSION_BUMP_PAT not configured. Using GITHUB_TOKEN."
    echo "::warning::Release pipeline will NOT be triggered automatically."
```

**Fix 3 (RECOMMENDED): Document CI/CD workflow dependencies**

Add a section to CONTRIBUTING.md documenting:
- Required GitHub secrets (`VERSION_BUMP_PAT`)
- Workflow dependency diagram (push → Version Bump → tag → Release; push → CI independently)
- Why CI and Version Bump are intentionally independent (CI validates code quality; Version Bump handles versioning)

**Fix 4 (OPTIONAL): Add CI exclusion for version bump commits**

Prevent CI from running redundantly on version bump commits (which are auto-generated and already validated):

```yaml
# In ci.yml, add to push filter:
on:
  push:
    branches: ["**"]
    # Skip CI on version bump commits (already validated by version-bump.yml)
    # Note: This requires the [skip ci] convention in bump commit messages
```

Or use the existing `github-actions[bot]` author check:
```yaml
jobs:
  lint:
    if: github.event.head_commit.author.name != 'github-actions[bot]'
```

### Changes Required

| File | Change Description | Status |
|------|-------------------|--------|
| GitHub repo settings | Add `VERSION_BUMP_PAT` secret | PENDING (manual) |
| `.github/workflows/version-bump.yml` | Add `GITHUB_TOKEN` fallback + warning | PENDING |
| `CONTRIBUTING.md` | Document required GitHub secrets and workflow dependencies | PENDING |
| `.github/workflows/ci.yml` | (Optional) Skip CI on bot commits | PENDING |

---

## Acceptance Criteria

### Fix Verification

- [ ] AC-1: `VERSION_BUMP_PAT` secret is configured in GitHub repo settings
- [ ] AC-2: Version Bump pipeline succeeds on push to `main` (checkout, bump, tag, push)
- [ ] AC-3: Release pipeline is triggered by the version tag created by Version Bump
- [ ] AC-4: If `VERSION_BUMP_PAT` is missing, workflow falls back to `GITHUB_TOKEN` with warning (not a hard failure)
- [ ] AC-5: CONTRIBUTING.md documents required GitHub secrets and CI/CD workflow diagram
- [ ] AC-6: CI pipeline behavior on `main` is documented (independent of Version Bump by design)

### Quality Checklist

- [ ] Version bump + release end-to-end flow verified
- [ ] Existing CI tests still passing
- [ ] No new issues introduced
- [ ] Documentation updated

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-001: OSS Release Preparation](../EPIC-001-oss-release.md)

### Related Items

- **Related Feature:** [EN-108: Version Bumping Strategy](../FEAT-002-research-and-preparation/EN-108-version-bumping-strategy/EN-108-version-bumping-strategy.md) — Original design of the version bump pipeline
- **Related Workflow:** `.github/workflows/version-bump.yml` — Failing workflow
- **Related Workflow:** `.github/workflows/ci.yml` — Independent CI workflow
- **Related Workflow:** `.github/workflows/release.yml` — Downstream release workflow (never triggered)
- **Related Workflow:** `.github/workflows/pat-monitor.yml` — PAT health monitoring (suggests PAT was planned)
- **Failed Run:** [Version Bump #22158902707](https://github.com/geekatron/jerry/actions/runs/22158902707)
- **Independent Run:** [CI #22158902717](https://github.com/geekatron/jerry/actions/runs/22158902717)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-18 | Adam Nowak | pending | Initial report. Version Bump fails on merge to main. CI runs independently and passes. Two root causes: (1) missing `VERSION_BUMP_PAT` secret, (2) no workflow dependency between CI and Version Bump. |
| 2026-02-18 | Claude | pending | Investigation complete. RC-1 confirmed: `secrets.VERSION_BUMP_PAT` undefined causes checkout failure. RC-2 confirmed: `ci.yml` triggers on `push: branches: ["**"]` independently. PAT is required for tag-triggered Release pipeline. 4 fix proposals documented. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |
