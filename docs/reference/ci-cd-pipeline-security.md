# CI/CD Pipeline Security Controls Reference

> Security controls applied across the Jerry Framework CI/CD pipeline workflows.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Workflows covered and control taxonomy |
| [SHA Pinning](#sha-pinning) | GitHub Actions pinned to commit SHAs |
| [UV Binary Pinning](#uv-binary-pinning) | `astral-sh/setup-uv` version pinning |
| [Pip Tool Pinning](#pip-tool-pinning) | Version-pinned tools installed via pip in CI |
| [Frozen Lockfile Enforcement](#frozen-lockfile-enforcement) | Lockfile enforcement across workflows |
| [Skip-Bump Guard](#skip-bump-guard) | Infinite-loop and double-bump prevention in version-bump.yml |
| [Dependabot Configuration](#dependabot-configuration) | Risk-tiered dependency update management |
| [Scheduled Security Scan](#scheduled-security-scan) | Daily pip-audit for transitive CVE detection |
| [H-05 Compliance](#h-05-compliance) | UV-only Python environment enforcement in CI |

---

## Overview

The Jerry Framework CI/CD pipeline spans five GitHub Actions workflow files and one Dependabot configuration. The security controls documented here apply to supply chain integrity, reproducible builds, and workflow loop prevention.

**Workflow files covered:**

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | Main CI pipeline: lint, type-check, security, test matrix, validation jobs |
| `.github/workflows/version-bump.yml` | Automated version bump on push to main |
| `.github/workflows/release.yml` | GitHub Release creation on `v*` tag push |
| `.github/workflows/docs.yml` | MkDocs deployment to GitHub Pages |
| `.github/workflows/pat-monitor.yml` | Weekly VERSION_BUMP_PAT liveness check |
| `.github/dependabot.yml` | Automated dependency update configuration |

---

## SHA Pinning

GitHub Actions can be referenced by floating version tag (e.g., `@v5`) or by immutable commit SHA. Tag references are mutable: a maintainer or attacker can force-push a tag to point to a different commit, causing the CI pipeline to execute arbitrary code. SHA references resolve to exactly one commit and cannot be redirected.

All GitHub Actions across the Jerry CI/CD pipeline are pinned to commit SHAs. A human-readable version comment accompanies each SHA.

**SHA-to-version mapping (as of v0.25.0):**

| Action | SHA | Version |
|--------|-----|---------|
| `actions/checkout` | `08c6903cd8c0fde910a37f88322edcfb5dd907a8` | v5.0.0 |
| `actions/setup-python` | `8d9ed9ac5c53483de85588cdf95a591a75ab9f55` | v5.5.0 |
| `astral-sh/setup-uv` | `d4b2f3b6ecc6e67c4457f6d3e41ec42d3d0fcb86` | v5.4.2 |
| `actions/upload-artifact` | `ea165f8d65b6e75b540449e92b4886f43607fa02` | v4.6.2 |
| `actions/download-artifact` | `95815c38cf2ff2164869cbab79da8d1f422bc89e` | v4.2.1 |
| `codecov/codecov-action` | `4650159d642e33fdc30954ca22638caf0df6cac8` | v5.4.3 |
| `softprops/action-gh-release` | `da05d552573ad5aba039eaac05058a918a7bf631` | v2.2.2 |
| `actions/github-script` | `60a0d83039c74a4aee543508d2ffcb1c3799cdea` | v7.0.1 |
| `MishaKav/pytest-coverage-comment` | `26f986d2599c288bb62f623d29c2da98609e9cd4` | main (2026-03-09) |

**Workflows where SHA-pinned actions appear:**

| Action | ci.yml | version-bump.yml | release.yml | docs.yml | pat-monitor.yml |
|--------|--------|------------------|-------------|----------|-----------------|
| `actions/checkout` | Yes | Yes | Yes | Yes | No |
| `actions/setup-python` | Yes (lint, type-check, security) | No | No | No | No |
| `astral-sh/setup-uv` | Yes (uv-dependent jobs) | Yes | Yes | Yes | No |
| `actions/upload-artifact` | Yes | No | Yes | No | No |
| `actions/download-artifact` | Yes | No | Yes | No | No |
| `codecov/codecov-action` | Yes | No | No | No | No |
| `softprops/action-gh-release` | No | No | Yes | No | No |
| `actions/github-script` | No | No | No | No | Yes |
| `MishaKav/pytest-coverage-comment` | Yes (coverage-report job) | No | No | No | No |

**Maintenance:** Dependabot monitors the `github-actions` ecosystem and opens pull requests when new versions of pinned actions are available. See [Dependabot Configuration](#dependabot-configuration).

**Syntax example:**

```yaml
- uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8 # v5.0.0
```

---

## UV Binary Pinning

The `astral-sh/setup-uv` action accepts a `version` parameter. When set to `"latest"`, the action downloads whatever version of `uv` is current at the time the job runs. This partially defeats SHA pinning: even if the action itself is SHA-pinned, a change in the `uv` binary can alter dependency resolution behavior, produce different `uv.lock` outputs, or introduce regressions.

All workflows that install `uv` specify `version: "0.10.9"`.

**Value:** `"0.10.9"`

**Workflows that apply this pin:**

| Workflow | Job(s) |
|----------|--------|
| `ci.yml` | plugin-validation, template-validation, license-headers, cli-integration, test-uv, version-sync, hard-rule-ceiling |
| `version-bump.yml` | bump |
| `release.yml` | validate, ci |
| `docs.yml` | deploy |

**Configuration example:**

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@d4b2f3b6ecc6e67c4457f6d3e41ec42d3d0fcb86 # v5.4.2
  with:
    version: "0.10.9"
```

---

## Pip Tool Pinning

Several tools in `ci.yml` are installed via `pip install` with exact version pins. These tools run outside the `uv`-managed virtual environment. Pinning prevents PyPI package compromise or unexpected behavioral changes from affecting CI outcomes.

**Pinned pip-installed tools:**

| Tool | Pinned Version | Job | Purpose |
|------|---------------|-----|---------|
| `ruff` | `0.14.11` | lint, security | Linting and format checking |
| `pyright` | `1.1.408` | type-check | Static type analysis |
| `pip-audit` | `2.10.0` | security | Vulnerability scanning of installed packages |
| `filelock` | `3.20.3` | security | Dependency of audited packages; pinned to prevent drift |
| `mypy` | `1.19.1` | security | Audited alongside other packages |

**Note:** The `lint` job installs `ruff` via `pip install "ruff==0.14.11"`. The `security` job independently installs `filelock`, `mypy`, and `ruff` at the same pinned versions before running `pip-audit --strict`, ensuring the audit covers the exact set of packages used in other jobs.

**Configuration example (security job):**

```yaml
- name: Install and audit dependencies
  run: |
    pip install "filelock==3.20.3" "mypy==1.19.1" "ruff==0.14.11"
    pip-audit --strict
```

**`bump-my-version` pinning (version-bump.yml):**

`bump-my-version` is installed via `uv tool install` rather than `pip install`, but is also version-pinned:

| Tool | Pinned Version | Workflow | Purpose |
|------|---------------|----------|---------|
| `bump-my-version` | `1.2.7` | version-bump.yml | Version string update across all project files |

```yaml
- name: Install bump-my-version
  run: uv tool install 'bump-my-version==1.2.7'
```

---

## Frozen Lockfile Enforcement

`uv sync` resolves the project's dependencies from scratch, potentially updating `uv.lock` when the resolver produces different output for a given Python version or platform. `uv sync --frozen` reads the existing `uv.lock` without modification. If the lockfile is inconsistent with `pyproject.toml`, `--frozen` exits with an error rather than silently updating the lockfile.

**Effect of `--frozen` in CI:**

| Behavior | Without `--frozen` | With `--frozen` |
|----------|--------------------|-----------------|
| Resolution mode | Full re-resolution against CI Python version | Reads existing lockfile verbatim |
| `uv.lock` modification | Possible (platform marker or bound changes) | Not possible |
| Working tree state | May become dirty | Remains clean |
| `bump-my-version` compatibility | Fails if working tree is dirty | Passes |

The version-bump workflow uses `allow_dirty = false` (bump-my-version default). A dirty working tree caused by `uv.lock` modification aborts the version bump with an error. The `--frozen` flag prevents this condition.

**Workflows and jobs using `uv sync --frozen`:**

| Workflow | Job | Command |
|----------|-----|---------|
| `ci.yml` | plugin-validation | `uv sync --frozen --extra dev` |
| `ci.yml` | template-validation | `uv sync --frozen` |
| `ci.yml` | license-headers | `uv sync --frozen` |
| `ci.yml` | cli-integration | `uv sync --frozen --extra dev --extra test` |
| `ci.yml` | test-uv | `uv sync --frozen --extra test` |
| `ci.yml` | version-sync | `uv sync --frozen` |
| `ci.yml` | hard-rule-ceiling | `uv sync --frozen` |
| `version-bump.yml` | bump (Install project dependencies) | `uv sync --frozen` |
| `version-bump.yml` | bump (Validate version sync) | `uv sync --frozen` |
| `release.yml` | validate | `uv sync --frozen` |
| `release.yml` | ci | `uv sync --frozen --extra dev --extra test` |
| `docs.yml` | deploy | `uv sync --frozen --extra dev` |

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

This guard fails loudly when the tree is dirty, requiring a human to investigate rather than silently committing unreviewed changes.

---

## Skip-Bump Guard

The version-bump workflow (`version-bump.yml`) runs on every push to `main`. Without a guard, the workflow would trigger on its own version-bump commits, creating an infinite loop. A secondary risk is double-bumping: manually dispatching the workflow for a commit that already carries a `[skip-bump]` marker.

**Guard conditions:**

The job-level `if` expression evaluates two branches:

| Trigger | Condition for job to run |
|---------|--------------------------|
| `workflow_dispatch` | `!contains(github.event.head_commit.message, '[skip-bump]')` |
| All other triggers (push to main) | `!contains(github.event.head_commit.message, '[skip-bump]')` AND `github.actor != 'github-actions[bot]'` |

**`[skip-bump]` marker:**

When a commit message contains the string `[skip-bump]`, the version-bump job does not run for that commit, regardless of how the workflow was triggered. This prevents `workflow_dispatch` from re-bumping a commit already marked to skip.

**`github.actor` check:**

The `github.actor` field is the authenticated identity set by GitHub from the token used to push the commit. It is not the `git config user.name` value. The version-bump commit is pushed using `github-actions[bot]` as the actor. Checking `github.actor` rather than the commit author name prevents spoofing via `git config user.name "github-actions[bot]"`.

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

This prevents shell injection via the free-form `workflow_dispatch` string input.

---

## Dependabot Configuration

Dependabot monitors two package ecosystems with risk-tiered grouping (#188). Updates are classified by SemVer level and handled differently based on risk.

**File:** `.github/dependabot.yml`

**Risk-tiered update handling:**

| Update Type | pip | GitHub Actions | Review Level |
|-------------|-----|---------------|-------------|
| Patch + Minor | Grouped (1 PR) | Grouped (1 PR) | CI green = merge |
| Major | Individual PR | Individual PR | Manual review required |
| Security | Individual PR | Individual PR | Priority review |
| Transitive | Excluded (`allow: direct`) | N/A | Updates via parent dep |

**Transitive dependency policy:** Dependabot only opens PRs for direct dependencies declared in `pyproject.toml`. Transitive dependencies (e.g., `gherkin-official` via `pytest-bdd`) are excluded to prevent incompatible standalone bumps. Transitive deps update when their parent direct dep is bumped and `uv.lock` is regenerated.

**Compensating control:** The scheduled security scan (`.github/workflows/security-scan.yml`) runs `pip-audit` daily against the locked dependency tree, catching transitive CVEs that Dependabot will not surface.

**Ecosystems configured:**

| Ecosystem | Directory | Schedule | Day | Commit prefix | PR limit | Grouping |
|-----------|-----------|----------|-----|---------------|----------|----------|
| `github-actions` | `/` | weekly | Monday | `ci` | 10 | minor+patch grouped |
| `pip` | `/` | weekly | Monday | `deps` | 10 | minor+patch grouped, direct only |

**Note:** Dependabot does **not** track version pins embedded in workflow `run:` blocks (e.g., `uv tool install 'bump-my-version==1.2.7'`). Those inline pins must be updated manually.

**Note:** `ruff` uses `0.x` versioning where `0.x` to `0.(x+1)` is semantically major (new default-enabled lint rules). Dependabot classifies these as "minor" — review ruff grouped PRs with extra care.

## Scheduled Security Scan

A daily scheduled workflow scans the locked dependency tree for known CVEs, independent of PR activity.

**File:** `.github/workflows/security-scan.yml`

**Purpose:** The `allow: dependency-type: direct` Dependabot policy means transitive dependency compromises do not generate Dependabot PRs. This workflow compensates by running `pip-audit` on a schedule. Without it, transitive CVE detection latency is unbounded during low-activity periods.

**Schedule:** Daily at 06:00 UTC (before Monday Dependabot run).

**What it checks:** `uv run pip-audit --strict --desc` against the current `uv.lock`.

**Failure behavior:** If vulnerabilities are found, the workflow fails with exit code 1 and posts results to the job summary. A separate verification step catches `pip-audit` silent failures (empty output).

---

## H-05 Compliance

H-05 requires that all Python execution in the Jerry project uses `uv run` and that dependencies are managed with `uv add`. Direct invocation of `python`, `pip`, or `pip3` is prohibited.

**Application in CI:**

Jobs that use the project's virtual environment use `uv sync --frozen` to install dependencies and `uv run` to execute Python. Jobs that install standalone tools (linters, type checkers, auditors) may use `pip install` within the runner's system Python environment, outside the project's virtual environment. This is a distinct context: the runner system Python is not the project's managed environment.

**Compliant pattern (uv-managed environment):**

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@d4b2f3b6ecc6e67c4457f6d3e41ec42d3d0fcb86 # v5.4.2
  with:
    version: "0.10.9"
- name: Set up Python
  run: uv python install 3.14
- name: Install dependencies
  run: uv sync --frozen
- name: Run script
  run: uv run python scripts/example.py
```

**Tool installation context (outside uv-managed environment):**

The `lint`, `type-check`, and `security` jobs use the runner's system Python to install standalone tools via `pip install`. These tools do not interact with the project's `uv.lock` or virtual environment:

```yaml
- name: Install ruff
  run: pip install "ruff==0.14.11"
- name: Check linting
  run: ruff check . --config=pyproject.toml
```

**`release.yml` H-05 compliance note:**

`release.yml` previously used a pip fallback for dependency installation. As of v0.25.0, it uses `uv sync --frozen` and `uv run` exclusively. The comment `# EN-001/F-001: Use uv directly (H-05 compliance). No pip fallback.` marks this migration.

**VERSION_BUMP_PAT (pat-monitor.yml):**

The PAT monitor workflow performs only `curl` API calls and JavaScript execution via `actions/github-script`. It does not install Python dependencies and has no H-05 applicability.

**`version-bump.yml` PAT usage:**

The version-bump workflow checks out with a personal access token (`VERSION_BUMP_PAT`) rather than the default `GITHUB_TOKEN` to allow the bump commit to push through branch protection rules. The PAT is a fine-grained token scoped to the `geekatron/jerry` repository with `Contents: Read and write` permission and a 90-day expiration. The PAT Monitor workflow (`pat-monitor.yml`) runs weekly to detect expiration before it causes a version-bump failure.

---

## Related

- **How-To Guide:** Update a SHA-pinned GitHub Action when Dependabot opens a PR
- **Explanation:** About the Jerry Framework supply chain security model (EN-001)
- **Reference:** `pyproject.toml` — Python dependency declarations and tool configuration
