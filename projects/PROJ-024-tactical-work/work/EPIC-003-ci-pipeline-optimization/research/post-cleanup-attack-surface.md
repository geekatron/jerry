# Post-Cleanup CI/CD Attack Surface Reconnaissance

> red-recon assessment of the Jerry CI/CD pipeline attack surface after EPIC-003 consolidation (29 to 17 jobs) and pip residue cleanup. Fresh reconnaissance -- no prior findings referenced.
>
> Date: 2026-04-13
> Agent: red-recon
> ATT&CK Phase: TA0043 Reconnaissance (T1592, T1596)
> Scope: `.github/workflows/*.yml`, `.github/dependabot.yml`, `pyproject.toml`

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Risk overview for stakeholders |
| [L1: Workflow Inventory](#l1-workflow-inventory) | Complete enumeration of workflows, permissions, triggers, secrets |
| [L1: Third-Party Action Inventory](#l1-third-party-action-inventory) | All external actions with trust assessment |
| [L1: Expression Injection Audit](#l1-expression-injection-audit) | All `${{ }}` expressions in `run:` blocks |
| [L1: Secret and Token Scope](#l1-secret-and-token-scope) | Per-secret blast radius analysis |
| [L1: Dependency Supply Chain Surface](#l1-dependency-supply-chain-surface) | Package manager attack surface |
| [L2: Threat Actor x Vector Matrix](#l2-threat-actor-x-vector-matrix) | Exploitability, impact, mitigation per actor |
| [L2: Attack Vector Detail](#l2-attack-vector-detail) | Per-vector deep analysis |
| [L2: Mitigations Present](#l2-mitigations-present) | What is already defended |
| [L2: Recommended Hardening](#l2-recommended-hardening) | Prioritized remediation actions |

---

## L0: Executive Summary

The CI/CD pipeline is in a materially strong posture. The EPIC-003 cleanup and pip removal reduced the attack surface meaningfully. Key structural strengths: all actions are SHA-pinned, no `pull_request_target` trigger exists, PR-triggered workflows have minimal permissions (`contents: read`), and the changelog check correctly uses environment variables for untrusted PR data instead of inline interpolation.

**Residual risk concentration is in two areas:**

1. **VERSION_BUMP_PAT** -- A personal access token with `contents: write` scoped to the repository, used in `version-bump.yml`. This is the single highest-value target. If compromised, it can push directly to `main`, bypassing branch protection rules that the default `GITHUB_TOKEN` cannot bypass. The PAT is exposed to the `actions/checkout` step and available in the workflow environment. The blast radius is: arbitrary code on `main`, tag creation, release triggering.

2. **Third-party action `MishaKav/pytest-coverage-comment`** -- Pinned by SHA but from a single-maintainer repository. This action receives `pull-requests: write` permission and processes coverage XML files. It is the weakest link in the third-party action chain. A maintainer compromise of this action could write arbitrary PR comments (social engineering vector) or exfiltrate coverage data.

**What improved with the cleanup:**
- requirements*.txt deletion eliminated `requirements.txt` as a dependency confusion vector (no more pip-parseable files).
- All Python execution uses `uv` with `--frozen` or `UV_LOCKED=1`, preventing lockfile tampering during CI.
- Consolidation from 29 to 17 jobs reduced the blast radius of runner compromise (fewer parallel execution environments).

**What did NOT change:**
- The VERSION_BUMP_PAT blast radius is unchanged.
- Third-party action trust boundaries are unchanged.
- The `contents: write` permission on `release.yml`, `docs.yml`, and `version-bump.yml` is inherent to their function.

---

## L1: Workflow Inventory

### Workflow Permission and Trigger Map

| Workflow | Trigger | Permissions | Secrets Accessed | Untrusted Actor Can Trigger? |
|----------|---------|-------------|-----------------|------------------------------|
| `ci.yml` | push to main/master; PR to main/master/claude/** | `contents: read` (top-level); `pull-requests: write` (coverage-report job only) | `CODECOV_TOKEN` | Yes (any fork PR) |
| `release.yml` | tag push `v*` | `contents: write` | `GITHUB_TOKEN` (implicit) | No (requires push access to create tags) |
| `version-bump.yml` | push to main; `workflow_dispatch` | `contents: write` | `VERSION_BUMP_PAT` | No (push to main requires merge permission) |
| `docs.yml` | push to main (paths: docs/**, mkdocs.yml, overrides/**) | `contents: write` | None (uses `GITHUB_TOKEN` implicitly via git push) | No (push to main only) |
| `pat-monitor.yml` | schedule (weekly Monday 09:00 UTC); `workflow_dispatch` | `contents: read`, `issues: write` | `VERSION_BUMP_PAT` | No (schedule/dispatch only) |
| `security-scan.yml` | schedule (daily 06:00 UTC); `workflow_dispatch` | `contents: read`, `security-events: write` | None | No (schedule/dispatch only) |

### Key Observations

1. **Only `ci.yml` is triggerable by untrusted external contributors** (via `pull_request`). It has `contents: read` top-level -- safe.
2. **No `pull_request_target` trigger anywhere.** This is the single most important security property -- eliminates the most common GitHub Actions privilege escalation vector.
3. **Three workflows have `contents: write`:** `release.yml`, `version-bump.yml`, `docs.yml`. All three require trusted triggers (tag push or push to main).
4. **`workflow_dispatch` on `version-bump.yml`** is accessible to anyone with repo write access. This is documented and accepted in the workflow comments.

---

## L1: Third-Party Action Inventory

All actions are SHA-pinned. No action uses a mutable tag reference.

| Action | SHA Pin | Claimed Version | Maintainer | Trust Level | Receives Secrets? | Has Write Perms? |
|--------|---------|-----------------|------------|-------------|-------------------|------------------|
| `actions/checkout` | `de0fac2e...` | v6.0.2 | GitHub (1st party) | High | `VERSION_BUMP_PAT` (version-bump.yml via `token:` param) | Inherits workflow perms |
| `astral-sh/setup-uv` | `cec20831...` | v8.0.0 | Astral (uv maintainer) | High | No | No |
| `actions/upload-artifact` | `043fb46d...` | v7.0.1 | GitHub (1st party) | High | No | No |
| `actions/download-artifact` | `3e5f45b2...` | v8.0.1 | GitHub (1st party) | High | No | No |
| `codecov/codecov-action` | `57e3a136...` | v6.0.0 | Codecov (3rd party, major vendor) | Medium-High | `CODECOV_TOKEN` | No |
| `MishaKav/pytest-coverage-comment` | `28729287...` | main (2026-03-09) | Single maintainer | Medium-Low | No direct secrets | `pull-requests: write` |
| `softprops/action-gh-release` | `b4309332...` | v3.0.0 | Community (popular) | Medium | `GITHUB_TOKEN` (via env) | `contents: write` (inherits) |
| `actions/github-script` | `3a2844b7...` | v9.0.0 | GitHub (1st party) | High | `GITHUB_TOKEN` (implicit) | `issues: write` (pat-monitor) |

### Trust Boundary Findings

**FINDING-001 (Medium): `MishaKav/pytest-coverage-comment` is the weakest third-party action.**
- Single-maintainer repository.
- Pinned to a commit on `main` branch, not a release tag (comment says "main (2026-03-09)").
- Receives `pull-requests: write` permission.
- Processes untrusted coverage XML generated during test runs.
- If the maintainer account is compromised and the SHA is ever rotated (via Dependabot), a malicious version could: write arbitrary PR comments, potentially exfiltrate PR metadata.
- Mitigating factor: SHA-pinned, so current deployment is frozen to a known-good commit.

**FINDING-002 (Low): `softprops/action-gh-release` has `contents: write` and `GITHUB_TOKEN`.**
- Popular community action for release creation.
- Receives the most powerful permission combination in the pipeline.
- Mitigating factor: only runs on tag push (trusted trigger), SHA-pinned.

**FINDING-003 (Low): `codecov/codecov-action` receives `CODECOV_TOKEN`.**
- Codecov has had past security incidents (April 2021 bash uploader compromise).
- Current version is SHA-pinned, uses the official action (not bash uploader).
- `fail_ci_if_error: false` means a Codecov outage/compromise does not block CI.
- Token scope: Codecov upload only, not repo-scoped.

---

## L1: Expression Injection Audit

Expression injection occurs when `${{ }}` containing untrusted data is placed directly in a `run:` block, allowing an attacker to inject arbitrary shell commands.

### Untrusted Data Sources in `${{ }}` Expressions

| Expression | Location | In `run:` Block? | Untrusted? | Verdict |
|------------|----------|-------------------|------------|---------|
| `${{ github.event.pull_request.title }}` | ci.yml:401 | No (in `env:` block) | Yes | **SAFE** -- passed via env var `PR_TITLE`, not inline in shell |
| `${{ github.actor }}` | ci.yml:402 | No (in `env:` block) | Partially | **SAFE** -- env var `PR_ACTOR` |
| `${{ github.event.pull_request.base.sha }}` | ci.yml:403 | No (in `env:` block) | Low | **SAFE** -- env var `BASE_SHA` |
| `${{ github.event.head_commit.message }}` | ci.yml:306-310 | No (in `if:` condition) | Yes | **SAFE** -- `if:` conditions are evaluated by GitHub, not shell |
| `${{ github.event.head_commit.message }}` | version-bump.yml:177-196 | No (in `if:` condition) | Yes | **SAFE** -- `if:` conditions are evaluated by GitHub, not shell |
| `${{ github.event.inputs.bump_type }}` | version-bump.yml:249 | Yes (in `run:` block) | Controlled | **SAFE** -- `choice` input, restricted to `patch`/`minor`/`major` |
| `${{ github.event.inputs.prerelease }}` | version-bump.yml:250-251 | Yes (in `run:` block) | Yes (free-form string) | **MITIGATED** -- alphanumeric regex validation at line 299 |
| `${{ github.event_name }}` | version-bump.yml:248 | Yes (in `run:` block) | No | **SAFE** -- system-controlled value |
| `${{ steps.bump.outputs.type }}` | version-bump.yml:288 | Yes (in `run:` block) | No | **SAFE** -- from own step output |
| `${{ steps.bump.outputs.prerelease }}` | version-bump.yml:289 | Yes (in `run:` block) | No | **SAFE** -- from own step output (originally from validated input) |
| `${{ steps.version.outputs.version }}` | version-bump.yml:374,386-388 | Yes (in `run:` block) | No | **SAFE** -- extracted from pyproject.toml by own step |
| `${{ needs.validate.outputs.version }}` | release.yml:46,56,129,etc. | Yes (in `run:` blocks) | No | **SAFE** -- extracted from git tag by validate job |
| `${{ matrix.python-version }}` | ci.yml:285 | Yes (in `run:` block) | No | **SAFE** -- controlled matrix values |
| `${{ needs.*.result }}` | ci.yml:450-469 | Yes (in `run:` block) | No | **SAFE** -- GitHub-controlled job result enum |
| `${{ steps.pat-check.outputs.status }}` | pat-monitor.yml:73 | No (in `script:` JS) | No | **SAFE** -- from own step, HTTP status code |
| `${{ secrets.VERSION_BUMP_PAT }}` | pat-monitor.yml:32,54,60 | Yes (in `run:` block) | No | **SAFE** (secret, not attacker-controlled) -- but exposure to shell |

### Injection Audit Verdict

**No expression injection vulnerabilities found.** The codebase demonstrates correct patterns:
- Untrusted PR data (`title`, `actor`, `base.sha`) is passed via `env:` block, not inline interpolation (CLCHK-001 pattern).
- `head_commit.message` is only used in `if:` conditions (GitHub-evaluated, not shell-evaluated).
- The `prerelease` free-form input has explicit alphanumeric validation before use.
- `bump_type` uses `choice` type restricting to three values.

---

## L1: Secret and Token Scope

### Secret: `VERSION_BUMP_PAT`

| Property | Value |
|----------|-------|
| Type | Fine-grained Personal Access Token |
| Documented scope | Repository: `geekatron/jerry` only; Permission: `Contents: Read and write` |
| Used in | `version-bump.yml` (checkout with push capability), `pat-monitor.yml` (liveness check) |
| Why it exists | Push version bump commits and tags to `main` through branch protection rules |
| Rotation policy | 90-day expiration with weekly monitoring (`pat-monitor.yml`) |
| Blast radius if compromised | Push arbitrary commits to `main`; create/delete tags; trigger `release.yml` (which creates GitHub Releases with `contents: write`); trigger `version-bump.yml` via `workflow_dispatch`; trigger `docs.yml` by pushing to docs paths on main |

**FINDING-004 (High): VERSION_BUMP_PAT is a privileged credential with broad blast radius.**
- Can bypass branch protection rules (that is its explicit purpose).
- A compromised PAT enables: (1) pushing malicious code to main, (2) creating a malicious tag that triggers the release pipeline, (3) deploying a compromised plugin archive via the release workflow, (4) deploying malicious docs via the docs workflow.
- The PAT is exposed in shell environment during `pat-monitor.yml` API calls (in `curl` command lines). This is standard practice but means the token value is in process memory and potentially in shell history within the runner.
- Mitigation: Fine-grained (not classic), single-repo scope, 90-day rotation, weekly monitoring. These are good controls but do not reduce the blast radius -- they reduce the window of exposure.

### Secret: `CODECOV_TOKEN`

| Property | Value |
|----------|-------|
| Type | Codecov upload token |
| Used in | `ci.yml` (test-uv job, Codecov upload step) |
| Scope | Upload coverage data to Codecov for this repository |
| Blast radius if compromised | Attacker could upload fake coverage data to Codecov; cannot modify repo |
| Exposure | Only in `ci.yml` which runs on PR triggers; secret is NOT available to fork PRs (GitHub default for `pull_request` trigger) |

**Risk: Low.** Token is narrowly scoped and the action is configured with `fail_ci_if_error: false`.

### Secret: `GITHUB_TOKEN` (implicit)

| Property | Value |
|----------|-------|
| Used in | `release.yml` (explicit env var for `softprops/action-gh-release`), `docs.yml` (implicit git push) |
| Scope | Scoped to the workflow's declared `permissions` |
| In `release.yml` | `contents: write` -- can create releases, push to branches |
| In `docs.yml` | `contents: write` -- can push to `gh-pages` branch |

**Risk: Low.** The `GITHUB_TOKEN` is automatically scoped and cannot bypass branch protection. It is only available in workflows triggered by trusted events (tag push, push to main).

---

## L1: Dependency Supply Chain Surface

### Post-Cleanup State

| Property | Before Cleanup | After Cleanup |
|----------|---------------|---------------|
| Dependency manifests | `pyproject.toml` + `uv.lock` + `requirements*.txt` | `pyproject.toml` + `uv.lock` only |
| Package manager in CI | `uv` + residual `pip` commands | `uv` only |
| Lockfile enforcement | `--frozen` (most jobs) | `--frozen` or `UV_LOCKED=1` (all jobs) |
| `pip install` commands | None in workflows (already clean) | None |
| `requirements.txt` files | Existed (even if unused) | Deleted |

### Direct Dependencies (from `pyproject.toml`)

| Group | Count | Packages |
|-------|-------|----------|
| Runtime | 10 | jsonschema, webvtt-py, tiktoken, filelock, markdown-it-py, mdformat, mdit-py-plugins, pyyaml, requests, pygments, pymdown-extensions |
| Dev (optional-deps) | 4 | mypy, ruff, filelock, jsonschema |
| Test (optional-deps) | 4 | pytest, pytest-archon, pytest-bdd, pytest-cov |
| Dev (dependency-groups) | 8 | mkdocs-material, pip-audit, pip-licenses, pre-commit, pyright, pytest, pytest-cov, ruff |

### Supply Chain Controls

| Control | Status |
|---------|--------|
| Lockfile (`uv.lock`) | Present and enforced (`--frozen`/`UV_LOCKED=1`) |
| Dependency audit | `pip-audit` in CI (security job) and daily scheduled scan (`security-scan.yml`) |
| Dependabot | Configured for `uv` ecosystem with `allow: direct` (transitive deps excluded from PRs) |
| Action pinning | All actions SHA-pinned |
| `bump-my-version` install | Exact version pin (`==1.2.7`) via `uv tool install` -- NOT tracked by Dependabot |

**FINDING-005 (Medium): `bump-my-version==1.2.7` is installed via `uv tool install` and is NOT tracked by Dependabot.**
- The workflow comments acknowledge this: "This pin must be updated manually. Check PyPI for new releases quarterly."
- If `bump-my-version` on PyPI is compromised, the version-bump workflow would install and execute malicious code with `contents: write` permission and `VERSION_BUMP_PAT` access.
- The exact version pin prevents silent upgrades but does NOT detect if the pinned version itself is retroactively compromised (unlikely but possible via PyPI yank+re-upload attack, though PyPI prevents re-upload of deleted versions).
- No hash verification on `uv tool install`.

**FINDING-006 (Low): Transitive dependency blind spot is compensated but not eliminated.**
- `allow: dependency-type: direct` means Dependabot will not create PRs for transitive dependency vulnerabilities.
- Compensating control: daily `security-scan.yml` runs `pip-audit` which catches known CVEs in transitives.
- Gap: zero-day compromises of transitive packages (no CVE yet) would not be detected by either Dependabot or pip-audit. This is an inherent limitation.
- The `dependabot.yml` D3 section documents this gap well with remediation steps.

---

## L2: Threat Actor x Vector Matrix

### Actor 1: External Contributor (Fork + PR)

| Vector | Exploitability | Impact | Mitigation Status | Notes |
|--------|---------------|--------|-------------------|-------|
| V1: PR-triggered code execution | Easy | Low | Mitigated | `pull_request` trigger runs fork code in read-only context; no secrets exposed; no write permissions |
| V2: Expression injection via PR title/body | Hard | Medium | Mitigated | PR title passed via `env:` block (CLCHK-001), not inline in shell |
| V3: Malicious test code in PR | Easy | Low | Mitigated | Tests run in ephemeral GitHub-hosted runner; no secrets; `contents: read` only |
| V4: Coverage XML poisoning | Medium | Low | Partially Mitigated | Coverage XML is generated by fork code, processed by `pytest-coverage-comment` action with `pull-requests: write`; action is SHA-pinned but processes attacker-controlled data |
| V5: Dependency confusion via PR | Medium | Low | Mitigated | `uv sync --frozen` prevents lockfile modification; PR cannot add new dependencies without lockfile change |
| V6: `[skip-coverage]` in commit message | Easy | Low | Accepted | Attacker can skip coverage threshold by including `[skip-coverage]` in commit message; only affects their own PR CI, not main |

**Actor 1 Summary: Low residual risk.** The `pull_request` trigger (not `pull_request_target`) is the critical control. Fork PRs cannot access secrets and run with `contents: read` only.

### Actor 2: Collaborator (Push Access to Branches)

| Vector | Exploitability | Impact | Mitigation Status | Notes |
|--------|---------------|--------|-------------------|-------|
| V7: `workflow_dispatch` on `version-bump.yml` | Easy | High | Partially Mitigated | Any write-access user can trigger arbitrary version bumps; prerelease input has alphanumeric validation; bump_type is choice-restricted |
| V8: Push malicious code to branch, merge via PR | Medium | High | Mitigated by review | Requires PR approval (if branch protection enforces reviews); CI runs on PR |
| V9: Push to `claude/**` branch triggering CI | Easy | Low | Mitigated | CI runs on these branches but with `contents: read` only; no elevated permissions |
| V10: Dependabot PR approval | Medium | Medium | Partially Mitigated | Collaborator could approve and merge a malicious Dependabot PR (if supply chain compromised); CI provides automated gate |

**Actor 2 Summary: Medium residual risk.** The `workflow_dispatch` on `version-bump.yml` is the primary concern. A rogue collaborator could push arbitrary version bumps, but the damage is limited to version number manipulation (not code injection, since they still need to merge code to main).

### Actor 3: Compromised Dependency

| Vector | Exploitability | Impact | Mitigation Status | Notes |
|--------|---------------|--------|-------------------|-------|
| V11: Malicious PyPI package (direct dep) | Medium | Critical | Partially Mitigated | Lockfile pinning prevents silent upgrades; Dependabot PR required for update; pip-audit detects known CVEs; zero-day compromise undetected |
| V12: Malicious PyPI package (transitive dep) | Medium | Critical | Partially Mitigated | Not tracked by Dependabot; daily pip-audit compensates for known CVEs; zero-day undetected; lockfile pins exact versions |
| V13: Malicious GitHub Action update | Hard | Critical | Mitigated | SHA-pinning prevents silent updates; Dependabot PR required for SHA rotation; manual review required |
| V14: `bump-my-version` PyPI compromise | Hard | Critical | Partially Mitigated | Exact version pin, but no hash verification; not tracked by Dependabot; manual quarterly review |
| V15: Typosquatting / dependency confusion | Medium | High | Mitigated | uv resolves from `pyproject.toml` with locked versions; no `requirements.txt` to confuse; no internal package index configured (no confusion vector) |

**Actor 3 Summary: Medium-High residual risk for direct deps (mitigated by lockfile + audit); Medium for transitives (daily audit compensates). The `bump-my-version` gap (FINDING-005) is the most notable untracked dependency.**

### Actor 4: Compromised Maintainer Account

| Vector | Exploitability | Impact | Mitigation Status | Notes |
|--------|---------------|--------|-------------------|-------|
| V16: Direct push to main | Easy | Critical | No mitigation beyond account security | Full repo access; can push code, create tags, trigger all workflows |
| V17: Modify workflow files | Easy | Critical | No mitigation beyond account security | Can add `pull_request_target`, remove SHA pins, add secret exfiltration steps |
| V18: Exfiltrate `VERSION_BUMP_PAT` | Easy | Critical | Partially Mitigated | PAT is in repo secrets; maintainer can read it via workflow modification; 90-day rotation limits window |
| V19: Create malicious release | Easy | Critical | No mitigation | Can push tag, release workflow creates GitHub Release automatically |
| V20: Modify Dependabot config | Easy | High | No mitigation | Can remove grouping, change `allow` policy, introduce malicious update patterns |
| V21: Disable branch protection | Easy | Critical | No mitigation beyond account security | Full admin access |

**Actor 4 Summary: Critical residual risk (inherent to full account access). Mitigations are organizational: MFA enforcement, SSO, PAT rotation, audit logs.** This threat actor is outside the scope of CI/CD hardening -- it requires identity and access management controls.

---

## L2: Attack Vector Detail

### V4: Coverage XML Poisoning (Detailed)

**Attack path:** External contributor creates a PR with malicious test code that generates a crafted `coverage.xml`. The `test-uv` job produces this XML on the ubuntu-latest/3.14 matrix cell. The `coverage-report` job downloads this artifact and passes it to `MishaKav/pytest-coverage-comment`.

**What the action does with the data:** Parses coverage XML and JUnit XML to generate a PR comment with coverage statistics and badge.

**Risk:** If the action has a parsing vulnerability (XML entity expansion, command injection via crafted paths in coverage report), the attacker could potentially:
- Write arbitrary content to PR comments (social engineering).
- Cause the action to fail or hang (DoS).
- In worst case, execute code in the runner with `pull-requests: write` token.

**Mitigating factors:**
- Action is SHA-pinned.
- `coverage-report` job only runs `if: github.event_name == 'pull_request'` -- correct.
- The runner is ephemeral (GitHub-hosted).
- The `pull-requests: write` scope cannot modify repository contents.

**Residual risk:** Low-Medium. The SHA pin is the primary defense.

### V7: `workflow_dispatch` Version Bump (Detailed)

**Attack path:** Collaborator with write access triggers `workflow_dispatch` on `version-bump.yml` with `bump_type: major` and a crafted `prerelease` string.

**Defenses in place:**
- `bump_type` is a `choice` input -- restricted to `patch`, `minor`, `major`.
- `prerelease` is validated: `if [[ -n "$PRERELEASE" && ! "$PRERELEASE" =~ ^[a-zA-Z0-9]+$ ]]; then exit 1; fi`.
- The workflow uses `VERSION_BUMP_PAT` to push, so the commit bypasses branch protection.

**What a rogue collaborator can do:**
- Trigger arbitrary major version bumps (e.g., jump from 0.31.3 to 1.0.0).
- Create release tags that trigger the release pipeline.
- Cannot inject code (only version number manipulation).

**Residual risk:** Medium. Version manipulation is disruptive but not a code integrity compromise.

### V14: `bump-my-version` Compromise (Detailed)

**Attack path:** `uv tool install 'bump-my-version==1.2.7'` downloads from PyPI on every `version-bump.yml` run. If PyPI is compromised or the package is hijacked:
1. Malicious `bump-my-version` installs and executes in the runner.
2. The runner has `VERSION_BUMP_PAT` in the environment (via checkout step).
3. The runner has `contents: write` permission.
4. Malicious code could: exfiltrate the PAT, push arbitrary code to main, create malicious tags/releases.

**Why this is hard to exploit:**
- PyPI prevents re-upload of deleted versions (FINDING-005 note).
- The exact version pin means only `1.2.7` is installed, not `latest`.
- An attacker would need to compromise the `bump-my-version` maintainer account on PyPI.

**What would improve the posture:**
- Adding hash verification: `uv tool install 'bump-my-version==1.2.7' --verify-hashes` (if uv supports this for tool install).
- Alternatively, vendoring the tool or using a pre-built Docker image.

---

## L2: Mitigations Present

| Mitigation | Controls | Strength |
|------------|----------|----------|
| SHA-pinned actions | All 8 third-party actions use full SHA pins | Strong |
| No `pull_request_target` | Eliminates the most common fork-based privilege escalation | Strong |
| Minimum permissions | `ci.yml` top-level is `contents: read`; elevated perms only on specific jobs | Strong |
| Env var injection prevention | CLCHK-001 pattern for PR title/actor/SHA | Strong |
| Lockfile enforcement | `--frozen` on all `uv sync` in CI; `UV_LOCKED=1` in version-bump | Strong |
| Concurrency controls | `cancel-in-progress` on ci.yml; `cancel-in-progress: false` on version-bump (prevents race) | Strong |
| Prerelease input validation | Alphanumeric regex validation on free-form `workflow_dispatch` input | Strong |
| Daily security scanning | `security-scan.yml` runs pip-audit independent of PR activity | Strong |
| PAT rotation monitoring | Weekly `pat-monitor.yml` checks PAT validity; creates issue on failure | Medium |
| Bot commit filtering | `github-actions[bot]` actor filter prevents infinite bump loops | Strong |
| Dependabot direct-only | `allow: dependency-type: direct` reduces transitive PR noise | Medium |
| GitHub-hosted runners | All workflows use `ubuntu-latest` / `windows-latest` / `macos-latest` | Strong (ephemeral) |

---

## L2: Recommended Hardening

### Priority 1 (High Impact, Feasible)

| # | Recommendation | Vector Addressed | Effort |
|---|---------------|-----------------|--------|
| R1 | **Add CODEOWNERS file** requiring review for `.github/workflows/` changes. Currently no CODEOWNERS file exists. This prevents a collaborator from modifying workflow files without designated reviewer approval. | V8, V17, V20 | Low |
| R2 | **Evaluate replacing `MishaKav/pytest-coverage-comment`** with a GitHub-maintained alternative or an inline `github-script` step that posts coverage. Removes the single-maintainer trust dependency. | V4, FINDING-001 | Medium |
| R3 | **Add hash verification for `bump-my-version` install** or vendor the tool. Research whether `uv tool install` supports `--require-hashes` or equivalent. | V14, FINDING-005 | Low |

### Priority 2 (Moderate Impact)

| # | Recommendation | Vector Addressed | Effort |
|---|---------------|-----------------|--------|
| R4 | **Add GitHub Environment with required reviewers** for `version-bump.yml` `workflow_dispatch`. This prevents a single collaborator from triggering arbitrary version bumps without approval. | V7 | Low |
| R5 | **Document the `bump-my-version` quarterly review cadence** in a maintenance runbook and create a recurring issue/calendar reminder. The current comment in the workflow is insufficient for operational tracking. | FINDING-005 | Low |
| R6 | **Consider separate fine-grained PAT per workflow** if GitHub supports it. Currently `VERSION_BUMP_PAT` is shared between `version-bump.yml` and `pat-monitor.yml`. Separation would reduce blast radius of a PAT leak from the monitor workflow. | FINDING-004 | Low |

### Priority 3 (Low Impact / Long-term)

| # | Recommendation | Vector Addressed | Effort |
|---|---------------|-----------------|--------|
| R7 | **Enable GitHub's required status checks** on the `ci-success` job for branch protection. Verify this is configured (not visible from workflow files alone). | V8 | Low (config change) |
| R8 | **Monitor Codecov action for security advisories.** Codecov has had past incidents; maintain awareness of their security posture. | FINDING-003 | Ongoing |
| R9 | **Consider artifact attestation** for release archives. GitHub now supports artifact attestation via `actions/attest-build-provenance`. This would provide SLSA-level provenance for the plugin archives. | V19 | Medium |

---

## Self-Hosted Runner Assessment

**Finding: No self-hosted runners are used.** All workflows specify `ubuntu-latest`, `windows-latest`, or `macos-latest` (GitHub-hosted). This eliminates the persistent runner risk entirely:
- No credential persistence between runs.
- No lateral movement from runner to internal network.
- No runner registration token to protect.
- Ephemeral runners are destroyed after each job.

This is the correct posture for an open-source project accepting external PRs.

---

*Reconnaissance Version: 1.0.0*
*Agent: red-recon*
*Constitutional Compliance: P-003 (no subagent spawning), P-020 (user authority), P-022 (no deception -- all findings evidence-based)*
*Scope: Authorized CI/CD pipeline reconnaissance within PROJ-024-tactical-work engagement*
