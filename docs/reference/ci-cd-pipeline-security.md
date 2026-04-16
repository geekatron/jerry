# CI/CD Pipeline Security Controls Reference

> Security controls applied across the Jerry Framework CI/CD pipeline workflows.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Workflows covered and control taxonomy |
| [Pipeline Job Structure](#pipeline-job-structure) | Jobs in `ci.yml` with purpose and trigger conditions |
| [Permission Model](#permission-model) | Top-level and job-level GitHub Actions permissions |
| [Push Trigger Scope](#push-trigger-scope) | Branch filter applied to push and pull_request events |
| [SHA Pinning](#sha-pinning) | GitHub Actions pinned to commit SHAs |
| [UV Binary Pinning](#uv-binary-pinning) | `astral-sh/setup-uv` version pinning |
| [Frozen Lockfile Enforcement](#frozen-lockfile-enforcement) | Lockfile enforcement across workflows |
| [Dependency Audit](#dependency-audit) | pip-audit scan via exported lockfile |
| [Skip-Bump Guard](#skip-bump-guard) | Infinite-loop and double-bump prevention in version-bump.yml |
| [Dependabot Configuration](#dependabot-configuration) | Risk-tiered dependency update management |
| [Scheduled Security Scan](#scheduled-security-scan) | Daily pip-audit for transitive CVE detection |
| [CODEOWNERS](#codeowners) | Required-review paths for security-sensitive files |
| [H-05 Compliance](#h-05-compliance) | UV-only Python environment enforcement in CI |

---

## Overview

The Jerry Framework CI/CD pipeline spans five GitHub Actions workflow files and one Dependabot configuration. The security controls documented here apply to supply chain integrity, reproducible builds, permission scoping, and workflow loop prevention.

**Workflow files covered:**

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | Main CI pipeline: static analysis, security, validation, plugin checks, CLI integration, test matrix |
| `.github/workflows/version-bump.yml` | Automated version bump on push to main |
| `.github/workflows/release.yml` | GitHub Release creation on `v*` tag push |
| `.github/workflows/docs.yml` | MkDocs deployment to GitHub Pages |
| `.github/workflows/pat-monitor.yml` | Weekly VERSION_BUMP_PAT liveness check |
| `.github/dependabot.yml` | Automated dependency update configuration |

---

## Pipeline Job Structure

All jobs are defined in `.github/workflows/ci.yml`.

**Job summary:**

| Job | Trigger | Runs on | Purpose |
|-----|---------|---------|---------|
| `static-analysis` | push, pull_request | ubuntu-latest | ruff check, ruff format --check, pyright |
| `security` | push, pull_request | ubuntu-latest | pip-audit full lockfile scan, banned YAML API check |
| `validation` | push, pull_request | ubuntu-latest | lockfile freshness, HARD rule ceiling, version sync, SPDX headers, adversarial templates, agent frontmatter |
| `plugin-validation` | push, pull_request | ubuntu-latest | plugin manifests, hook wrapper syntax, hook script syntax, plugin.json agent sync |
| `cli-integration` | push, pull_request | ubuntu-latest | subprocess CLI tests, MkDocs e2e validation, `jerry --help`, `jerry --version` |
| `test-uv` | push, pull_request | ubuntu/windows/macos x Python 3.11–3.14 (8 cells) | pytest suite with coverage |
| `coverage-report` | pull_request only | ubuntu-latest | Posts coverage comment to PR |
| `changelog-check` | pull_request only | ubuntu-latest | Validates CHANGELOG.md updated in PR |
| `ci-success` | always (gate) | ubuntu-latest | Aggregates all required job results; branch protection target |

**`ci-success` required jobs:**

`static-analysis`, `security`, `validation`, `plugin-validation`, `cli-integration`, `test-uv`, `changelog-check`

`changelog-check` result of `skipped` is treated as passing (it only runs on pull_request events; push events skip it).

**`coverage-report` is not in `ci-success`'s `needs` list.** It runs as a PR annotation step only and does not gate the branch protection check.

### `static-analysis` job

Merged replacement for the former `lint` and `type-check` jobs.

| Step | Command |
|------|---------|
| Check linting | `uv run ruff check . --config=pyproject.toml` |
| Check formatting | `uv run ruff format --check . --config=pyproject.toml` |
| Run type check | `uv run pyright src/` |

Dependencies installed via: `uv sync --frozen --extra dev`

### `security` job

| Step | Command |
|------|---------|
| Export dependencies | `uv export --no-hashes --frozen --all-extras --no-emit-project > /tmp/requirements.txt` |
| Audit dependencies | `uv run pip-audit --requirement /tmp/requirements.txt --strict --desc` |
| Check for banned YAML APIs | `grep -rn 'yaml\.load\('` and `yaml\.unsafe_load\(` in `src/` |

The banned YAML API check enforces M-04b: `yaml.load()` and `yaml.unsafe_load()` are prohibited; `yaml.safe_load()` is the required alternative. Exit code 1 on any match.

### `validation` job

Consolidates six formerly independent single-script jobs into one runner. Each former job is a named step.

| Step | Former job | Validation |
|------|-----------|------------|
| Verify uv.lock is fresh | `lockfile-check` | `uv lock --check` |
| Check HARD rule ceiling | `hard-rule-ceiling` | `uv run python scripts/check_hard_rule_ceiling.py` |
| Validate version consistency | `version-sync` | `uv run python scripts/sync_versions.py --check` |
| Validate SPDX license headers | `license-headers` | `uv run python scripts/check_spdx_headers.py` |
| Validate adversarial strategy templates | `template-validation` | `uv run python scripts/validate_templates.py --verbose` |
| Validate agent and skill frontmatter | `frontmatter-validation` | `uv run jerry agents validate-frontmatter` |

Dependencies installed via: `uv sync --frozen`

### `plugin-validation` job

| Step | Command |
|------|---------|
| Validate plugin manifests | `uv run python scripts/validate_plugin_manifests.py` |
| Validate hook wrappers syntax | `python3 -m py_compile hooks/session-start.py hooks/pre-compact.py hooks/pre-tool-use.py hooks/user-prompt-submit.py` |
| Validate hook scripts syntax | `uv run python -m py_compile` for each `.py` in `hooks/` and `scripts/` |
| Validate plugin.json agent sync | `uv run python scripts/check_plugin_agent_sync.py` |

Dependencies installed via: `uv sync --frozen --extra dev`

### `cli-integration` job

| Step | Command |
|------|---------|
| Run CLI subprocess tests | `uv run pytest tests/integration/cli/test_jerry_cli_subprocess.py -v --tb=short` |
| Run MkDocs e2e validation tests | `uv run pytest tests/e2e/test_mkdocs_research_validation.py -v --tb=short` |
| Verify jerry --help works | `PYTHONPATH="." uv run jerry --help` |
| Verify jerry --version works | `PYTHONPATH="." uv run jerry --version` |

Dependencies installed via: `uv sync --frozen --extra dev --extra test`

### `test-uv` job

| Parameter | Value |
|-----------|-------|
| OS matrix | `ubuntu-latest`, `windows-latest`, `macos-latest` |
| Python matrix | `3.11`, `3.12`, `3.13`, `3.14` |
| Excluded cells | windows+3.11, windows+3.12, macos+3.11, macos+3.12 |
| Active cells | 8 |
| `fail-fast` | `false` |
| Coverage threshold | `--cov-fail-under=80` |
| Skip marker | `[skip-coverage]` in commit message disables `--cov-fail-under` |
| Excluded test markers | `llm`, `subprocess` |

Coverage artifact upload and Codecov upload occur only for the `ubuntu-latest` + `3.14` cell.

### `coverage-report` job

| Parameter | Value |
|-----------|-------|
| Trigger | `pull_request` events only |
| `needs` | `test-uv` |
| `permissions.pull-requests` | `write` (only job with this permission) |
| Action | `MishaKav/pytest-coverage-comment` |
| Coverage input | `coverage.xml` from `coverage-report-uv` artifact |
| JUnit input | `junit-uv-3.14.xml` from `coverage-report-uv` artifact |

### `changelog-check` job

| Parameter | Value |
|-----------|-------|
| Trigger | `pull_request` events only |
| Exempt actors | `dependabot[bot]`, `github-actions[bot]` |
| Exempt marker | `[skip-changelog]` in PR title |
| Validation | CHANGELOG.md must appear in `git diff --name-only BASE...HEAD` and contain new content under `[Unreleased]` |
| Shell injection prevention | PR title passed via `env:` block (CLCHK-001), not inline `${{ }}` expansion |

### `ci-success` job

| Parameter | Value |
|-----------|-------|
| `if` condition | `always()` |
| Required results | `success` for all jobs except `changelog-check` |
| `changelog-check` accepted results | `success` or `skipped` |

---

## Permission Model

**Top-level permissions in `ci.yml`:**

```yaml
permissions:
  contents: read
```

All jobs inherit `contents: read` unless overridden at the job level.

**Job-level permission overrides:**

| Job | `contents` | `pull-requests` | Rationale |
|-----|-----------|-----------------|-----------|
| `coverage-report` | `read` (inherited) | `write` | Required to post PR comment via `MishaKav/pytest-coverage-comment` |
| All other jobs | `read` (inherited) | not granted | No PR write access needed |

`pull-requests: write` is scoped exclusively to `coverage-report`. No other job receives write permissions to the repository or pull requests.

---

## Push Trigger Scope

**`ci.yml` trigger configuration:**

```yaml
on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master, "claude/**"]
```

Push events trigger CI only on `main` and `master`. The wildcard `"**"` is not used. This prevents CI from running on every developer branch push.

Pull request events trigger CI for PRs targeting `main`, `master`, or any `claude/**` branch.

---

## SHA Pinning

GitHub Actions referenced by immutable commit SHA rather than floating version tag. A human-readable version comment accompanies each SHA.

**SHA-to-version mapping (current):**

| Action | SHA | Version |
|--------|-----|---------|
| `actions/checkout` | `de0fac2e4500dabe0009e67214ff5f5447ce83dd` | v6.0.2 |
| `astral-sh/setup-uv` | `cec208311dfd045dd5311c1add060b2062131d57` | v8.0.0 |
| `actions/upload-artifact` | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` | v7.0.1 |
| `actions/download-artifact` | `3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c` | v8.0.1 |
| `codecov/codecov-action` | `57e3a136b779b570ffcdbf80b3bdc90e7fab3de2` | v6.0.0 |
| `softprops/action-gh-release` | `b4309332981a82ec1c5618f44dd2e27cc8bfbfda` | v3.0.0 |
| `actions/github-script` | `3a2844b7e9c422d3c10d287c895573f7108da1b3` | v9.0.0 |
| `MishaKav/pytest-coverage-comment` | `287292879eaaff04116f36d3eb1a670f6e5df1a4` | main (2026-03-09) |

**Workflows where SHA-pinned actions appear:**

| Action | ci.yml | version-bump.yml | release.yml | docs.yml | pat-monitor.yml |
|--------|--------|------------------|-------------|----------|-----------------|
| `actions/checkout` | Yes | Yes | Yes | Yes | No |
| `astral-sh/setup-uv` | Yes (all uv jobs) | No | Yes | Yes | No |
| `actions/upload-artifact` | Yes (test-uv) | No | Yes | No | No |
| `actions/download-artifact` | Yes (coverage-report) | No | Yes | No | No |
| `codecov/codecov-action` | Yes (test-uv) | No | No | No | No |
| `softprops/action-gh-release` | No | No | Yes | No | No |
| `actions/github-script` | No | No | No | No | Yes |
| `MishaKav/pytest-coverage-comment` | Yes (coverage-report) | No | No | No | No |

**Maintenance:** Dependabot monitors the `github-actions` ecosystem and opens pull requests when new versions of pinned actions are available. See [Dependabot Configuration](#dependabot-configuration).

**Syntax example:**

```yaml
- uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
```

---

## UV Binary Pinning

The `astral-sh/setup-uv` action accepts a `version` parameter. All workflows that install `uv` specify `version: "0.10.9"`.

**Value:** `"0.10.9"`

**Workflows that apply this pin:**

| Workflow | Job(s) |
|----------|--------|
| `ci.yml` | static-analysis, security, validation, plugin-validation, cli-integration, test-uv |
| `version-bump.yml` | bump |
| `release.yml` | validate, ci |
| `docs.yml` | deploy |

**Configuration example:**

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@cec208311dfd045dd5311c1add060b2062131d57 # v8.0.0
  with:
    version: "0.10.9"
```

---

## Frozen Lockfile Enforcement

`uv sync --frozen` reads the existing `uv.lock` without modification. If the lockfile is inconsistent with `pyproject.toml`, `--frozen` exits with an error rather than silently updating the lockfile.

**Effect of `--frozen` in CI:**

| Behavior | Without `--frozen` | With `--frozen` |
|----------|--------------------|-----------------|
| Resolution mode | Full re-resolution against CI Python version | Reads existing lockfile verbatim |
| `uv.lock` modification | Possible (platform marker or bound changes) | Not possible |
| Working tree state | May become dirty | Remains clean |
| `bump-my-version` compatibility | Fails if working tree is dirty | Passes |

**Workflows and jobs using `uv sync --frozen`:**

| Workflow | Job | Command |
|----------|-----|---------|
| `ci.yml` | static-analysis | `uv sync --frozen --extra dev` |
| `ci.yml` | security | `uv sync --frozen` (dependency export only; see [Dependency Audit](#dependency-audit)) |
| `ci.yml` | validation | `uv sync --frozen` |
| `ci.yml` | plugin-validation | `uv sync --frozen --extra dev` |
| `ci.yml` | cli-integration | `uv sync --frozen --extra dev --extra test` |
| `ci.yml` | test-uv | `uv sync --frozen --extra test` |
| `version-bump.yml` | bump (Install project dependencies) | `uv sync --frozen` |
| `version-bump.yml` | bump (Validate version sync) | `uv sync --frozen` |
| `release.yml` | validate | `uv sync --frozen` |
| `release.yml` | ci | `uv sync --frozen --extra dev --extra test` |
| `docs.yml` | deploy | `uv sync --frozen --extra dev` |
| `security-scan.yml` | pip-audit | `uv sync --frozen --all-extras` |

**Clean working tree guard (version-bump.yml):**

After `uv sync --frozen` but before applying the version bump, `version-bump.yml` runs an explicit check:

```yaml
- name: Ensure clean working tree
  if: steps.bump.outputs.type != 'none'
  run: |
    if [[ -n "$(git status --porcelain)" ]]; then
      echo "::error::Working tree unexpectedly dirty before bump (uv sync --frozen should prevent this)"
      git diff --name-only
      exit 1
    fi
```

**`validation` job lockfile freshness check:**

The `validation` job runs `uv lock --check` (the `lockfile-check` step) before installing dependencies. This verifies the lockfile is consistent with `pyproject.toml` without modifying it.

---

## Dependency Audit

The `security` job scans the full locked dependency tree for known CVEs via pip-audit.

**Export command:**

```yaml
uv export --no-hashes --frozen --all-extras --no-emit-project > /tmp/requirements.txt
```

| Flag | Effect |
|------|--------|
| `--no-hashes` | Produces pip-compatible requirements format without hash directives |
| `--frozen` | Reads the existing lockfile; does not re-resolve |
| `--all-extras` | Includes all optional dependency groups (`dev`, `test`, etc.) |
| `--no-emit-project` | Excludes the project package itself from the output |

**Audit command:**

```yaml
uv run pip-audit --requirement /tmp/requirements.txt --strict --desc
```

| Flag | Effect |
|------|--------|
| `--requirement` | Audits the specified requirements file rather than the active environment |
| `--strict` | Exits non-zero if any package cannot be audited |
| `--desc` | Includes vulnerability descriptions in output |

The `security` job does not install standalone tools via `pip install`. All execution is via `uv run` within the project virtual environment.

---

## Skip-Bump Guard

The version-bump workflow (`version-bump.yml`) runs on every push to `main`. The job-level `if` expression prevents infinite loops and double-bumping.

**Guard conditions:**

| Trigger | Condition for job to run |
|---------|--------------------------|
| `workflow_dispatch` | `!contains(github.event.head_commit.message, '[skip-bump]')` |
| All other triggers (push to main) | `!contains(github.event.head_commit.message, '[skip-bump]')` AND `github.actor != 'github-actions[bot]'` |

**`[skip-bump]` marker:**

When a commit message contains the string `[skip-bump]`, the version-bump job does not run for that commit, regardless of how the workflow was triggered.

**`github.actor` check:**

`github.actor` is the authenticated identity set by GitHub from the token used to push the commit. It is not the `git config user.name` value. The version-bump commit is pushed using `github-actions[bot]` as the actor. Checking `github.actor` rather than the commit author name prevents spoofing via `git config user.name "github-actions[bot]"`.

**Complete `if` expression:**

```yaml
if: >-
  (
    github.event_name == 'workflow_dispatch' &&
    !contains(github.event.head_commit.message, '[skip-bump]')
  ) ||
  (
    github.event_name != 'workflow_dispatch' &&
    !contains(github.event.head_commit.message, '[skip-bump]') &&
    github.actor != 'github-actions[bot]'
  )
```

**Prerelease input validation:**

When `workflow_dispatch` is used with a `prerelease` label, the label is validated as alphanumeric-only before being passed to shell commands:

```yaml
if [[ -n "$PRERELEASE" && ! "$PRERELEASE" =~ ^[a-zA-Z0-9]+$ ]]; then
  echo "::error::Invalid prerelease label '$PRERELEASE'. Must be alphanumeric (e.g., alpha, beta, rc)."
  exit 1
fi
```

---

## Dependabot Configuration

**File:** `.github/dependabot.yml`

Dependabot monitors two package ecosystems with risk-tiered grouping.

**Risk-tiered update handling:**

| Update Type | uv | GitHub Actions | Review Level |
|-------------|-----|---------------|-------------|
| Patch + Minor | Grouped (1 PR) | Grouped (1 PR) | CI green = merge |
| Major | Individual PR | Individual PR | Manual review required |
| Security | Individual PR | Individual PR | Priority review |
| Transitive | Excluded (`allow: direct`) | N/A | Updates via parent dep |

**Transitive dependency policy:** Dependabot only opens PRs for direct dependencies declared in `pyproject.toml`. Transitive dependencies are excluded to prevent incompatible standalone bumps.

**Compensating control:** The scheduled security scan runs `pip-audit` daily against the locked dependency tree, catching transitive CVEs that Dependabot does not surface.

**Ecosystems configured:**

| Ecosystem | Directory | Schedule | Day | Commit prefix | PR limit | Grouping |
|-----------|-----------|----------|-----|---------------|----------|----------|
| `github-actions` | `/` | weekly | Monday | `ci` | 10 | minor+patch grouped |
| `uv` | `/` | weekly | Monday | `deps` | 10 | minor+patch grouped, direct only |

**Note:** Dependabot does not track version pins embedded in workflow `run:` blocks (e.g., `uv tool install 'bump-my-version==1.2.7'`). Those inline pins must be updated manually.

**Note:** `ruff` uses `0.x` versioning where `0.x` to `0.(x+1)` is semantically equivalent to a major release (new default-enabled lint rules). Dependabot classifies these as "minor."

---

## Scheduled Security Scan

**File:** `.github/workflows/security-scan.yml`

**Schedule:** Daily at 06:00 UTC.

**Permissions:**

| Permission | Value | Rationale |
|------------|-------|-----------|
| `contents` | `read` | Checkout only; no write operations |

**Job steps:**

| Step | Command |
|------|---------|
| Install dependencies | `uv sync --frozen --all-extras` |
| Run pip-audit | `uv run pip-audit --strict --desc` |
| Verify pip-audit executed | Checks `/tmp/pip-audit-output.txt` for non-empty output |

`--all-extras` installs all optional dependency groups (`dev`, `test`, `transcript`) before scanning. This matches the coverage of the `security` job in `ci.yml`, which exports with `--all-extras` before auditing. Without `--all-extras`, optional dependencies declared only in extras groups would be absent from the scheduled scan's virtual environment, leaving their transitive chains unaudited.

**Failure behavior:** Vulnerabilities found causes the workflow to fail with exit code 1 and posts results to the job summary. A separate verification step catches `pip-audit` silent failures (empty output).

---

## CODEOWNERS

**File:** `.github/CODEOWNERS`

Defines required reviewers for paths containing security-sensitive files. GitHub enforces at least one approval from a listed owner before a pull request targeting those paths can be merged, subject to branch protection rules.

**Pattern evaluation:** GitHub evaluates CODEOWNERS entries top-to-bottom; the last matching pattern wins.

**Protected paths:**

| Path pattern | Owner | Scope |
|--------------|-------|-------|
| `.github/workflows/` | `@geekatron` | All CI/CD workflow files |
| `.github/dependabot.yml` | `@geekatron` | Dependabot configuration |
| `.github/CODEOWNERS` | `@geekatron` | The CODEOWNERS file itself |
| `.pre-commit-config.yaml` | `@geekatron` | Pre-commit hook configuration |
| `.context/rules/` | `@geekatron` | Framework constraint rule files |
| `docs/governance/` | `@geekatron` | Governance documents |

---

## H-05 Compliance

H-05 requires that all Python execution uses `uv run` and that dependencies are managed with `uv add`. Direct invocation of `python`, `pip`, or `pip3` is prohibited.

**Application in CI:**

All jobs in `ci.yml` use `uv sync --frozen` to install dependencies and `uv run` to execute Python. No job uses `pip install` to install tools into the runner's system Python environment. The `security` job previously used standalone pip-installed tools; after EPIC-003, it uses `uv run pip-audit` exclusively.

**Compliant pattern (uv-managed environment):**

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@cec208311dfd045dd5311c1add060b2062131d57 # v8.0.0
  with:
    version: "0.10.9"
- name: Set up Python
  run: uv python install 3.14
- name: Install dependencies
  run: uv sync --frozen
- name: Run script
  run: uv run python scripts/example.py
```

**`release.yml` H-05 compliance note:**

`release.yml` uses `uv sync --frozen` and `uv run` exclusively. The comment `# EN-001/F-001: Use uv directly (H-05 compliance). No pip fallback.` marks this migration.

**VERSION_BUMP_PAT (pat-monitor.yml):**

The PAT monitor workflow performs only `curl` API calls and JavaScript execution via `actions/github-script`. It does not install Python dependencies and has no H-05 applicability.

**`version-bump.yml` PAT usage:**

The version-bump workflow checks out with a personal access token (`VERSION_BUMP_PAT`) rather than the default `GITHUB_TOKEN` to allow the bump commit to push through branch protection rules. The PAT is a fine-grained token scoped to the `geekatron/jerry` repository with `Contents: Read and write` permission and a 90-day expiration. The PAT Monitor workflow (`pat-monitor.yml`) runs weekly to detect expiration before it causes a version-bump failure.

---

## Related

- **Explanation:** `docs/explanation/ci-cd-supply-chain-security.md` — Supply chain security model
- **Reference:** `pyproject.toml` — Python dependency declarations and tool configuration
- **Source:** `.github/workflows/ci.yml` — Authoritative pipeline definition
