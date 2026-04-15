# Post-Cleanup Supply Chain Risk Assessment

> eng-devsecops audit of Jerry CI/CD pipeline supply chain posture after EPIC-003 completion.
> Date: 2026-04-13 | Auditor: eng-devsecops | Scope: All 6 workflows + dependabot + pre-commit + pyproject.toml

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Finding totals by severity, pipeline health |
| [L1 Findings](#l1-findings) | Per-finding details with file:line, risk, remediation |
| [L2 Strategic Assessment](#l2-strategic-assessment) | Coverage gaps, tooling maturity, SLSA roadmap |

---

## L0 Executive Summary

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | 0 | -- |
| HIGH | 3 | Require remediation before next release |
| MEDIUM | 5 | Track for near-term remediation |
| LOW | 3 | Awareness and hardening opportunities |
| INFO | 3 | Positive observations / no action needed |
| **Total** | **14** | |

**Pipeline Health:** GOOD. No critical blockers. The EPIC-003 cleanup substantially improved the posture: all actions are SHA-pinned, uv is consistent at 0.10.9 across all workflows, lockfile enforcement is present on all install jobs, and secret scope is minimal. The remaining findings are hardening opportunities, not active vulnerabilities.

**Top 3 priorities:**
1. (HIGH) Pre-commit hooks use floating tags, not SHAs -- supply chain vector for developer machines
2. (HIGH) No build provenance or attestations in the release pipeline -- SLSA Level 0
3. (HIGH) pip-audit coverage gap between CI job and scheduled scan (different invocation methods)

---

## L1 Findings

### Finding 1 -- Pre-commit hooks pinned to floating tags

| Attribute | Value |
|-----------|-------|
| **Severity** | HIGH |
| **Category** | Pre-commit supply chain |
| **File:Line** | `.pre-commit-config.yaml:24`, `:42`, `:205` |

**Risk:** Three external pre-commit hook repos use floating version tags, not SHAs:
- `pre-commit/pre-commit-hooks` at `rev: v5.0.0` (tag, not SHA)
- `astral-sh/ruff-pre-commit` at `rev: v0.9.2` (tag, not SHA)
- `commitizen-tools/commitizen` at `rev: v4.4.1` (tag, not SHA)

A compromised GitHub repo owner (or a force-pushed tag) can silently replace the code at these tags. Unlike GitHub Actions where Dependabot monitors SHA pins, pre-commit hook tag pins are invisible to Dependabot and have no automated update mechanism.

**Impact:** Arbitrary code execution on developer machines during `git commit`. The hooks run with the developer's full filesystem and network access. The `ruff` hook has `--fix` enabled (line 46), meaning it writes to the working tree.

**Remediation:**
1. Pin all three external repos to full commit SHAs:
   ```yaml
   - repo: https://github.com/pre-commit/pre-commit-hooks
     rev: cef0300fd0fc4d2a87a85fa2093c6b283ea36f4b  # v5.0.0
   ```
2. Add a quarterly review process for pre-commit SHA updates (no Dependabot coverage exists for pre-commit repos).
3. Consider `pre-commit autoupdate --freeze` to automate SHA resolution.

---

### Finding 2 -- No build provenance or attestations (SLSA Level 0)

| Attribute | Value |
|-----------|-------|
| **Severity** | HIGH |
| **Category** | Build provenance |
| **File:Line** | `.github/workflows/release.yml` (entire file) |

**Risk:** The release pipeline produces `.tar.gz`, `.zip`, and `checksums.sha256` artifacts but generates no SLSA provenance attestations. Consumers cannot verify that a release artifact was built from the claimed source commit by the claimed CI system.

SHA256 checksums (line 184) verify integrity (the file was not corrupted in transit) but NOT provenance (the file was built from this source by this pipeline). An attacker who compromises the release job can replace both artifacts and checksums.

**Current SLSA Level:** 0 (no provenance)

**Impact:** No cryptographic proof that release artifacts correspond to the tagged source commit. Supply chain consumers must trust the GitHub Release page implicitly.

**Remediation:**
1. Add `actions/attest-build-provenance@v2` (GitHub-native, SHA-pinned) to the release job after artifact upload.
2. This produces SLSA Level 2 provenance (signed by GitHub Actions OIDC, non-falsifiable by project maintainers) at zero infrastructure cost.
3. Target: SLSA Level 2 for plugin archives.

```yaml
- name: Generate SLSA provenance
  uses: actions/attest-build-provenance@<sha>  # pin to SHA
  with:
    subject-path: |
      dist/*.tar.gz
      dist/*.zip
      dist/checksums.sha256
```

---

### Finding 3 -- pip-audit invocation inconsistency between CI and scheduled scan

| Attribute | Value |
|-----------|-------|
| **Severity** | HIGH |
| **Category** | Dependency audit coverage |
| **File:Line** | `ci.yml:87-90`, `security-scan.yml:67` |

**Risk:** The two pip-audit invocations use different methods, producing different coverage:

| Aspect | CI (ci.yml) | Scheduled (security-scan.yml) |
|--------|-------------|-------------------------------|
| Method | `uv export --all-extras --no-emit-project > /tmp/requirements.txt` then `pip-audit --requirement` | `uv run pip-audit --strict --desc` (against installed env) |
| Scope | All extras (dev, test, transcript) via `--all-extras` | Only base deps (installed via `uv sync --frozen` with no extras) |
| Extras covered | dev, test, transcript | **None** |

The scheduled scan (security-scan.yml) installs with `uv sync --frozen` (no `--extra` flags, line 57), then runs `pip-audit` against the installed environment. This means it does NOT audit `dev`, `test`, or `transcript` optional dependencies. A CVE in `pytest`, `ruff`, `pyright`, `mkdocs-material`, `pip-audit` itself, or `webvtt-py` would be caught by CI but missed by the scheduled scan during low-activity periods.

**Impact:** During periods with no PR activity, the scheduled scan provides incomplete coverage. The entire purpose of the scheduled scan (compensating for Dependabot's `allow: direct` policy on transitive deps) is undermined for optional dependency trees.

**Remediation:** Change `security-scan.yml` line 57 to install all extras:
```yaml
- name: Install dependencies
  run: uv sync --frozen --all-extras
```
Or, use the same `uv export` + `--requirement` pattern as ci.yml for parity.

---

### Finding 4 -- MishaKav/pytest-coverage-comment pinned to main branch SHA

| Attribute | Value |
|-----------|-------|
| **Severity** | MEDIUM |
| **Category** | Third-party action trust |
| **File:Line** | `ci.yml:371` |

**Risk:** `MishaKav/pytest-coverage-comment@287292879eaaff04116f36d3eb1a670f6e5df1a4` is SHA-pinned (good), but the comment says `# main (2026-03-09)` -- this is pinned to a main branch commit, not a release tag. The action is from a personal GitHub account (`MishaKav`), not an organization with security review processes.

This action has `pull-requests: write` permission (ci.yml:359) and executes JavaScript that parses coverage XML and writes PR comments. A compromised action could exfiltrate secrets available in the coverage-report job or inject malicious content into PR comments.

**Mitigating factors:** The SHA pin prevents silent updates. The job only has `contents: read` + `pull-requests: write` (no `contents: write`, no secret access beyond `GITHUB_TOKEN`).

**Remediation:**
1. Verify the pinned SHA corresponds to a tagged release (not just a main branch commit). Pin to a release tag SHA.
2. Consider replacing with `actions/github-script` to post coverage comments directly, eliminating the third-party dependency entirely.
3. Add this action to a quarterly review checklist for third-party action trust.

---

### Finding 5 -- softprops/action-gh-release is a non-GitHub-org action

| Attribute | Value |
|-----------|-------|
| **Severity** | MEDIUM |
| **Category** | Third-party action trust |
| **File:Line** | `release.yml:264` |

**Risk:** `softprops/action-gh-release@b4309332981a82ec1c5618f44dd2e27cc8bfbfda # v3.0.0` is from a personal GitHub account. It has access to `contents: write` permission and `GITHUB_TOKEN` (release.yml:276). It creates the GitHub Release and uploads artifacts.

**Mitigating factors:** SHA-pinned. Widely used in the ecosystem. The action is well-known and actively maintained.

**Remediation:**
1. Consider migrating to GitHub CLI (`gh release create`) in a shell step, eliminating the third-party dependency. This would reduce the third-party action surface to only `actions/*`, `astral-sh/*`, `codecov/*`, and `MishaKav/*`.
2. If keeping softprops, add to quarterly third-party review checklist.

---

### Finding 6 -- No SBOM generation anywhere in the pipeline

| Attribute | Value |
|-----------|-------|
| **Severity** | MEDIUM |
| **Category** | SBOM |
| **File:Line** | `.github/workflows/release.yml` (entire file), `pyproject.toml` |

**Risk:** No Software Bill of Materials (SBOM) is generated during build or release. Consumers of the Jerry plugin cannot programmatically enumerate the dependency tree. Executive Order 14028 and NIST SP 800-218 (SSDF) recommend SBOM generation for all software releases.

**Impact:** No machine-readable dependency inventory for consumers. Incident response (e.g., "does this project use library X?") requires manual inspection of `uv.lock`.

**Remediation:**
1. Add `anchore/sbom-action` (SHA-pinned) or `uv export --format cyclonedx` to the release build job.
2. Attach the SBOM as a release artifact alongside the checksums.
3. CycloneDX JSON format recommended for Python ecosystems.

---

### Finding 7 -- bump-my-version not tracked by Dependabot

| Attribute | Value |
|-----------|-------|
| **Severity** | MEDIUM |
| **Category** | Dependency pinning blind spot |
| **File:Line** | `version-bump.yml:231` |

**Risk:** `uv tool install 'bump-my-version==1.2.7'` is a pinned PyPI install that Dependabot does not track. The workflow comments acknowledge this (line 228-229): "Dependabot does NOT track `uv tool install` version pins... This pin must be updated manually." The recommended quarterly cadence may be insufficient for a tool that runs in a privileged context (contents:write + PAT).

**Impact:** If a vulnerability is discovered in bump-my-version, there is no automated alerting or PR creation. The tool has write access to the repository via `VERSION_BUMP_PAT`.

**Remediation:**
1. Add a scheduled job (or extend security-scan.yml) to check the latest `bump-my-version` version on PyPI and alert if the pinned version is outdated.
2. Alternatively, consider moving bump-my-version into `pyproject.toml` dev dependencies so Dependabot tracks it.

---

### Finding 8 -- security-events:write permission on security-scan.yml unused

| Attribute | Value |
|-----------|-------|
| **Severity** | MEDIUM |
| **Category** | Secret exposure / permission scope |
| **File:Line** | `security-scan.yml:37` |

**Risk:** The security-scan workflow declares `security-events: write` permission but no step in the workflow uploads SARIF or writes security events. This is an over-scoped permission.

**Impact:** If the workflow were compromised, the attacker would have unnecessary `security-events: write` access. Principle of least privilege violation.

**Remediation:** Remove `security-events: write` from the permissions block unless SARIF upload is planned. If SARIF upload is intended as a future enhancement, add a comment documenting the intent.

---

### Finding 9 -- Pre-commit pip-audit uses --skip-editable (coverage gap)

| Attribute | Value |
|-----------|-------|
| **Severity** | LOW |
| **Category** | Dependency audit coverage |
| **File:Line** | `.pre-commit-config.yaml:226` |

**Risk:** The local pre-commit pip-audit hook uses `--skip-editable`, which skips the `jerry` package itself. The comment (line 224) explains the rationale (local packages not on PyPI). However, the `--strict` flag is removed (line 223) because it conflicts with `--skip-editable`. This means local pip-audit runs are less strict than CI pip-audit runs.

**Impact:** Developer-local scans may miss warnings that CI would catch. Low severity because CI is the authoritative gate.

**Remediation:** Document this known gap. No code change needed -- CI is the enforcement point.

---

### Finding 10 -- docs.yml has contents:write for gh-pages deploy

| Attribute | Value |
|-----------|-------|
| **Severity** | LOW |
| **Category** | Permission scope |
| **File:Line** | `docs.yml:21-22` |

**Risk:** The docs workflow uses `contents: write` to push to the `gh-pages` branch via `mkdocs gh-deploy --force`. This is functionally required -- `mkdocs gh-deploy` pushes to a branch. However, `contents: write` also grants the ability to push to main or create/delete tags.

**Mitigating factors:** The workflow only triggers on push to main with specific path filters (`docs/**`, `mkdocs.yml`, `overrides/**`). The `GITHUB_TOKEN` is scoped to the repository. No custom secrets are used.

**Remediation:** Consider switching to GitHub Pages deployment via `actions/deploy-pages` which uses the more targeted `pages: write` + `id-token: write` permissions instead of broad `contents: write`. This is a lower-priority improvement.

---

### Finding 11 -- No Dependabot configuration for pre-commit hooks

| Attribute | Value |
|-----------|-------|
| **Severity** | LOW |
| **Category** | Dependency update automation |
| **File:Line** | `.github/dependabot.yml` (missing entry) |

**Risk:** Dependabot does not have a `pre-commit` ecosystem entry. The three external pre-commit repos (`pre-commit-hooks`, `ruff-pre-commit`, `commitizen`) will not receive automated update PRs. Updates must be performed manually via `pre-commit autoupdate`.

**Impact:** Pre-commit hooks may drift behind latest versions. Combined with Finding 1 (floating tags), this creates a scenario where known-vulnerable hook versions persist without alerting.

**Remediation:** Option A (preferred if Finding 1 is addressed with SHA pins): No action needed -- SHA pins prevent silent compromise regardless of version. Option B: Add a `pre-commit` ecosystem entry to dependabot.yml if Dependabot supports it in this configuration.

---

### Finding 12 (INFO) -- Action pinning posture is excellent

| Attribute | Value |
|-----------|-------|
| **Severity** | INFO |
| **Category** | Action pinning |

**Positive observation:** All 10 distinct GitHub Actions across all 6 workflows are pinned to full 40-character commit SHAs with version comments. No floating tags detected in any workflow file.

| Action | SHA | Version |
|--------|-----|---------|
| `actions/checkout` | `de0fac2e...` | v6.0.2 |
| `astral-sh/setup-uv` | `cec20831...` | v8.0.0 |
| `actions/upload-artifact` | `043fb46d...` | v7.0.1 |
| `actions/download-artifact` | `3e5f45b2...` | v8.0.1 |
| `codecov/codecov-action` | `57e3a136...` | v6.0.0 |
| `MishaKav/pytest-coverage-comment` | `28729287...` | main |
| `softprops/action-gh-release` | `b4309332...` | v3.0.0 |
| `actions/github-script` | `3a2844b7...` | v9.0.0 |

Dependabot is configured to monitor GitHub Actions on a weekly schedule with grouped minor/patch updates and individual major PRs.

---

### Finding 13 (INFO) -- uv version consistency is perfect

| Attribute | Value |
|-----------|-------|
| **Severity** | INFO |
| **Category** | uv binary pinning |

**Positive observation:** All 11 `setup-uv` invocations across all 5 workflows that use uv specify `version: "0.10.9"` consistently. Zero drift detected.

---

### Finding 14 (INFO) -- Lockfile enforcement is comprehensive

| Attribute | Value |
|-----------|-------|
| **Severity** | INFO |
| **Category** | Lockfile enforcement |

**Positive observation:** Every `uv sync` in CI, release, docs, and security-scan workflows uses `--frozen`. The version-bump workflow uses `UV_LOCKED=1` (environment variable, stricter than `--frozen`) and documents why `--frozen` is not used there (conflicts with UV_LOCKED). The lockfile freshness check (`uv lock --check`) runs in the validation job.

---

## L2 Strategic Assessment

### Third-Party Action Trust Summary

| Trust Level | Actions | Risk |
|-------------|---------|------|
| **GitHub-owned** | `actions/checkout`, `actions/upload-artifact`, `actions/download-artifact`, `actions/github-script` | Lowest -- maintained by GitHub |
| **Verified publisher** | `astral-sh/setup-uv`, `codecov/codecov-action` | Low -- organizations with established security practices |
| **Community (personal)** | `MishaKav/pytest-coverage-comment`, `softprops/action-gh-release` | Medium -- individual maintainers, no organizational security review |

**Recommendation:** Replace the 2 community/personal actions with GitHub-native alternatives (gh CLI, actions/github-script) to reduce the trust boundary to only GitHub-owned and verified-publisher actions.

### Secret Exposure Map

| Secret | Workflows | Jobs | Scope | Risk |
|--------|-----------|------|-------|------|
| `CODECOV_TOKEN` | ci.yml | test-uv (ubuntu, 3.14 only) | Codecov upload | Low -- read-only token, single job |
| `VERSION_BUMP_PAT` | version-bump.yml, pat-monitor.yml | bump, check-pat | contents:write to repo | Medium -- PAT with push access; compensated by 90-day rotation + monitoring |
| `GITHUB_TOKEN` | release.yml | release | contents:write for Release creation | Low -- automatically scoped, not a custom secret |

**Assessment:** Secret scope is minimal. The highest-risk secret (`VERSION_BUMP_PAT`) has monitoring (pat-monitor.yml) and a documented rotation policy (90 days).

### SLSA Maturity Assessment

| SLSA Level | Requirement | Jerry Status |
|------------|-------------|--------------|
| Level 0 | No provenance | **CURRENT STATE** |
| Level 1 | Documented build process | PARTIAL -- workflows are well-documented but no formal build definition |
| Level 2 | Signed provenance from hosted platform | NOT MET -- no attestations generated |
| Level 3 | Hardened build platform, non-falsifiable | NOT MET -- requires Level 2 first |

**Roadmap to Level 2:**
1. Add `actions/attest-build-provenance` to release.yml (1 step, Finding 2)
2. Add SBOM generation to release.yml (1 step, Finding 6)
3. Enable GitHub artifact attestations in repository settings

**Estimated effort:** 1-2 hours for Level 2. Level 3 requires hermetic builds (not recommended at current project scale).

### Transitive Dependency Visibility After requirements*.txt Removal

With requirements files removed, the transitive dependency visibility chain is:

```
Detection:     Dependabot (direct only) + pip-audit (CI: all extras) + pip-audit (scheduled: base only*)
Manifest:      pyproject.toml (direct deps)
Lock:          uv.lock (full transitive tree, machine-readable)
SBOM:          NONE*
Remediation:   Manual (bump direct dep or add explicit override)
```

`*` = gaps identified in Findings 3 and 6.

**Assessment:** The `uv.lock` file is the sole source of truth for the transitive dependency tree. The Dependabot `allow: direct` policy is compensated by pip-audit in CI (comprehensive) and the scheduled scan (incomplete per Finding 3). The missing SBOM (Finding 6) means there is no release-time snapshot of the dependency tree for consumers.

### Coverage Gap Summary

| Dimension | CI (per PR) | Scheduled (daily) | Pre-commit (local) | Gap |
|-----------|-------------|-------------------|-------------------|-----|
| SAST (ruff) | All source | -- | All source | None |
| Type check (pyright) | src/ | -- | src/ | None |
| Dep audit (pip-audit) | All extras | **Base only** | --skip-editable | **Finding 3** |
| YAML API ban | src/ | -- | -- | None (CI-only is sufficient) |
| Architecture boundaries | -- | -- | Python files | None |
| Lockfile freshness | `uv lock --check` | -- | -- | None (CI-only is sufficient) |
| DAST | -- | -- | -- | Not applicable (no running service) |
| Container scanning | -- | -- | -- | Not applicable (no containers) |
| Secrets scanning | -- | -- | `detect-private-key` | See note below |

**Secrets scanning note:** The pre-commit `detect-private-key` hook (line 37) catches private key files but does NOT scan for API keys, tokens, or other secret patterns. No Gitleaks or TruffleHog integration exists. This is a coverage gap, but rated LOW because Jerry is a framework (not a service with runtime secrets) and the repository is not public-facing with customer data.

---

*Audit completed: 2026-04-13*
*Auditor: eng-devsecops*
*Methodology: Manual review of all CI/CD configuration files against 10 audit dimensions*
*Next review: After SLSA Level 2 implementation or after next Dependabot major action bump*
