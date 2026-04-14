# CI Pipeline DevSecOps Review

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Total findings, pipeline health, critical blockers |
| [L1 Technical Detail](#l1-technical-detail) | Per-issue findings with evidence, severity, remediation |
| [L2 Strategic Implications](#l2-strategic-implications) | Coverage gaps, tooling evolution, SLSA maturity |

---

## L0 Executive Summary

**Pipeline:** `ci.yml` -- Jerry Framework CI, 707 lines, 29 jobs
**Review date:** 2026-04-13
**Reviewer:** eng-devsecops

### Finding Totals

| Severity | Count | Categories |
|----------|-------|------------|
| HIGH | 2 | Supply chain risk, governance violation |
| MEDIUM | 3 | Audit scope gap, pip-test value, consistency |
| LOW | 2 | Job count, coverage threshold gap |
| INFO | 1 | Observation only |

### Pipeline Health

The pipeline has a well-intentioned security posture: pinned action SHAs, locked uv version, a `lockfile-check` job, and a `pip-audit` job. The structural problem is that three jobs (`lint`, `type-check`, `security`) operate entirely outside the governance envelope that the rest of the pipeline enforces. The `test-pip` matrix adds 8 jobs that provide meaningful portability signal but duplicate the `test-uv` matrix at significant CI cost with unclear security differentiation.

### Critical Blockers Requiring Immediate Attention

1. **[HIGH]** The `type-check` job installs the full project in editable mode via `pip install -e ".[dev]"` with no lockfile. This is the only job in the pipeline that resolves dependencies at runtime against the live PyPI index without a pinned manifest. If any dev dependency is compromised on PyPI, the type-check job will silently install the malicious version.

2. **[HIGH]** The `security` job audits only 3 hand-selected packages (`filelock`, `mypy`, `ruff`), not the full dependency tree. The `pip-audit --strict` command therefore only reports CVEs for those 3 packages, producing a false-compliance signal. The audit does not cover `pyright`, `pytest`, `coverage`, or any transitive dependencies.

---

## L1 Technical Detail

### Finding 1 -- Mixed pip/uv: Governance Inconsistency [HIGH]

**Evidence:**
- `lint` job, line 40: `pip install "ruff==0.14.11"` -- standalone, pinned, no project deps
- `type-check` job, lines 63-66: `python -m pip install --upgrade pip`, `pip install "pyright==1.1.408"`, `pip install -e ".[dev]" || pip install -e .`
- `security` job, lines 86-96: `pip install "pip-audit==2.10.0"`, then `pip install "filelock==3.20.3" "mypy==1.19.1" "ruff==0.14.11"`, then `pip-audit --strict`
- All other jobs: `uv sync --frozen` or `uv sync --frozen --extra ...`

**Security concern (differentiated by job):**

`lint` -- Low risk. `ruff==0.14.11` is pinned. No project dependencies installed. The only supply chain attack surface is the ruff package itself. Risk is bounded. The inconsistency is a governance concern, not a material security concern.

`type-check` -- HIGH risk. `pip install -e ".[dev]"` resolves the full `[dev]` optional dependency group against the live PyPI index with no lockfile constraint. The `|| pip install -e .` fallback silently swallows the failure if `[dev]` resolution fails and installs the bare package instead, potentially masking missing type stubs. In the event a transitive dev dependency is typosquatted or compromised after the last `uv.lock` commit, `type-check` will install the malicious version while `test-uv` (which uses `--frozen`) is protected.

`security` -- HIGH risk. The explicit `pip install` of 3 packages followed by `pip-audit --strict` audits only those 3 packages. `pip-audit --strict` audits the currently installed environment -- which at that point contains only `pip-audit` itself plus those 3 packages. The actual project dependencies (pyright, pytest, coverage, mkdocs-material, and their transitives) are never installed in the security job environment, so `pip-audit` cannot find CVEs in them.

**Remediation:**

For `lint`: Replace with the official `astral-sh/ruff-action` or install ruff via uv tool:
```yaml
- name: Install uv
  uses: astral-sh/setup-uv@cec208311dfd045dd5311c1add060b2062131d57
  with:
    version: "0.10.9"
- name: Install ruff
  run: uv tool install ruff==0.14.11
- name: Check linting
  run: uv tool run ruff check . --config=pyproject.toml
```

For `type-check`: Install pyright via uv tool and sync project deps via uv:
```yaml
- name: Install uv
  uses: astral-sh/setup-uv@cec208311dfd045dd5311c1add060b2062131d57
  with:
    version: "0.10.9"
- name: Set up Python
  run: uv python install 3.14
- name: Install dependencies
  run: uv sync --frozen --extra dev
- name: Run pyright
  run: uv run pyright src/
```

For `security` (pip-audit scope fix -- see Finding 2):
```yaml
- name: Install uv
  uses: astral-sh/setup-uv@cec208311dfd045dd5311c1add060b2062131d57
  with:
    version: "0.10.9"
- name: Set up Python
  run: uv python install 3.14
- name: Audit dependencies
  run: uvx pip-audit --require-hashes -r <(uv export --frozen --no-dev --format requirements-txt)
```

---

### Finding 2 -- pip-audit Scope Gap: False Compliance Signal [HIGH]

**Evidence (lines 85-96):**
```yaml
- name: Install pip-audit
  run: |
    python -m pip install --upgrade pip
    pip install "pip-audit==2.10.0"
- name: Install and audit dependencies
  run: |
    pip install "filelock==3.20.3" "mypy==1.19.1" "ruff==0.14.11"
    pip-audit --strict
```

**Analysis:** `pip-audit --strict` with no `--requirement` or `--project` argument audits the packages currently installed in the active environment. At the time this command runs, that environment contains: `pip-audit` itself, `filelock`, `mypy`, `ruff`, and their transitive dependencies -- a total of perhaps 8-12 packages. The full project dependency tree (which includes `pyright`, `pytest`, `pytest-cov`, `coverage`, `mkdocs-material`, `pymdown-extensions`, and their transitives) is never installed, so `pip-audit` cannot report CVEs against those packages.

The `# EN-001: Pin versions to prevent supply chain drift` comment suggests the intent is drift protection, but pinning 3 packages while leaving the rest unaudited creates an audit coverage gap that is invisible in the CI output. A reader of the CI log will see `pip-audit --strict` pass and incorrectly conclude the full dependency tree is clean.

**Remediation:** Audit directly from the frozen lockfile to get full coverage:
```yaml
- name: Install uv
  uses: astral-sh/setup-uv@cec208311dfd045dd5311c1add060b2062131d57
  with:
    version: "0.10.9"
- name: Set up Python
  run: uv python install 3.14
- name: Audit all dependencies via lockfile
  run: |
    # Export the full frozen dependency set and audit it
    uv export --frozen --format requirements-txt --all-extras > /tmp/audit-reqs.txt
    uvx pip-audit --strict --requirement /tmp/audit-reqs.txt
```

This approach audits every package in `uv.lock` including all optional extras, is reproducible (always the same packages since the lockfile is frozen), and eliminates the manual 3-package list that will drift as dependencies change.

---

### Finding 3 -- test-pip Matrix: Security Theater vs. Portability Signal [MEDIUM]

**Evidence (lines 307-408):** 8-job matrix (3 OS x 4 Python versions, minus 4 excluded combinations) running the same pytest suite as `test-uv`. Comment on line 305: "Uses standard pip/venv for maximum portability."

**Analysis:** The `test-pip` matrix does provide genuine value, but it is not security value -- it is portability validation. The two matrices test different things:

| Dimension | test-pip | test-uv |
|-----------|----------|---------|
| Installation method | pip + requirements-test.txt + pip install -e . | uv sync --frozen |
| Subprocess tests | Included (some) | Excluded (-m "not subprocess") |
| HTML coverage | Generated | Skipped |
| mkdocs-material | Explicitly installed | Not available (not in --extra test) |
| OS coverage | 3 OS | 3 OS |
| Python versions | 3.11-3.14 | 3.11-3.14 |

The pip matrix is testing that the package installs and runs correctly when users install it via `pip install jerry` from PyPI -- a legitimate concern for a published package. It is not providing security differentiation.

**The H-05 tension:** The Jerry framework mandates `uv run` for all execution (H-05). The `test-pip` matrix runs `pytest` directly (not `uv run pytest`), which technically violates H-05 in the CI environment. This is probably intentional (the point is to test pip-installed behavior), but it creates a tension: the framework says uv-only, but CI tests pip compatibility.

**Assessment:** If Jerry is distributed as a PyPI package and users are expected to `pip install jerry`, keep the pip matrix. Label the job comment accurately: "Validates pip installability for PyPI users." If Jerry is internal-only and always consumed via uv, the pip matrix adds 8 jobs of CI cost with zero benefit. The current comment "maximum portability" is ambiguous about which user population this serves.

**Recommendation:** Retain the pip matrix if Jerry is a public PyPI package. Add a `requirements-test.txt` hash check or pin all versions with hashes to prevent unpinned transitive dependency installation in the pip matrix. If internal-only, remove the pip matrix and reduce from 29 to 21 jobs.

---

### Finding 4 -- Coverage Threshold: 80% vs. H-20 [MEDIUM]

**Evidence (lines 357, 461):** Both matrices use `--cov-fail-under=80`.

**Analysis:** The framework rule H-20 mandates 90% line coverage. The pipeline enforces 80%. The 10-point gap means branches that are mandated to be covered by H-20 can fail in the source and still pass CI.

**Remediation:** Raise to `--cov-fail-under=90` in both matrices. If there is a documented justification for the lower threshold (e.g., a planned incremental approach), that justification should be captured in the ADR referenced at line 2 of the pipeline.

---

### Finding 5 -- plugin-validation: python3 vs uv run [MEDIUM]

**Evidence (lines 162-165):**
```yaml
- name: Validate hook wrappers syntax
  run: |
    python3 -m py_compile hooks/session-start.py
    python3 -m py_compile hooks/pre-compact.py
    python3 -m py_compile hooks/pre-tool-use.py
    python3 -m py_compile hooks/user-prompt-submit.py
```

**Analysis:** This step uses the bare `python3` command (system Python), violating H-05. The subsequent step (line 173) correctly uses `uv run python -m py_compile`. The inconsistency means hook wrappers are compiled against a different Python interpreter than hook scripts. On macOS GitHub runners, `python3` may be 3.x from Homebrew; on ubuntu-latest it is typically the system Python 3.10. Since the job already installs Python 3.14 via uv, using `python3` here silently ignores that setup.

**Remediation:** Replace `python3` with `uv run python`:
```yaml
- name: Validate hook wrappers syntax
  run: |
    uv run python -m py_compile hooks/session-start.py
    uv run python -m py_compile hooks/pre-compact.py
    uv run python -m py_compile hooks/pre-tool-use.py
    uv run python -m py_compile hooks/user-prompt-submit.py
```

---

### Finding 6 -- coverage-report: Unpinned Action SHA [LOW]

**Evidence (line 527):**
```yaml
uses: MishaKav/pytest-coverage-comment@287292879eaaff04116f36d3eb1a670f6e5df1a4 # main (2026-03-09)
```

**Analysis:** All other actions in the pipeline use commit SHAs. This action also uses a SHA, which is correct. However, the comment `# main (2026-03-09)` indicates this SHA points to the tip of the `main` branch as of March 9, 2026 -- not a tagged release. The SHA is pinned, so the action is reproducible. The risk is that `main` branch of third-party actions can contain arbitrary, non-release code. The SHA pinning mitigates the supply chain risk (the code won't change without a PR updating the SHA), but the comment should clarify this is a commit-to-main pin, not a release pin.

**Recommendation:** Document this explicitly in the comment: `# main commit 2026-03-09, no release tag available`. No code change required. Consider raising a PR to the MishaKav/pytest-coverage-comment repo requesting release tags.

---

### Finding 7 -- Job Count: 29 Jobs, Consolidation Opportunities [LOW]

**Evidence:** ci-success job (lines 648-693) depends on 14 named jobs; 8 pip matrix + 8 uv matrix jobs = 16 additional.

**Consolidation candidates without coverage loss:**

| Option | Jobs Saved | Trade-off |
|--------|-----------|-----------|
| Merge `lint` into `type-check` (both are Python static analysis, same OS/Python version) | 1 | Slower feedback if type-check is slow; failing lint still blocks type-check |
| Merge `lockfile-check` into `security` (both are dependency integrity checks) | 1 | Minor conceptual mismatch; lockfile-check is fast and gives a clearer signal separately |
| Merge `template-validation` into `plugin-validation` (both validate non-code assets) | 1 | Longer job; less granular failure signal |
| Merge `version-sync` and `hard-rule-ceiling` into a single `governance-checks` job | 1 | Both are lightweight script checks; no capability loss |

Maximum savings without functional change: 4 jobs, from 29 to 25. The `test-pip` matrix removal (if justified) saves 8 additional.

---

### Finding 8 -- [skip-coverage] Commit Message Flag [INFO]

**Evidence (lines 362-365, 463-466):**
```yaml
if: ${{ !contains(github.event.head_commit.message, '[skip-coverage]') }}
continue-on-error: ${{ contains(github.event.head_commit.message, '[skip-coverage]') }}
```

**Analysis:** This pattern allows bypassing the coverage gate by adding `[skip-coverage]` to a commit message. The implementation uses `head_commit.message`, which on PR events may not be the commit that triggered the PR but rather the most recent commit on the branch. The bypass is intentional and documented, but it should be noted that any contributor can bypass the coverage gate unilaterally without reviewer approval. If coverage enforcement is a security-relevant property (e.g., ensuring security-critical code paths are tested), this bypass should require an explicit label set by a maintainer rather than a commit message string any contributor can add.

**Recommendation:** If the coverage threshold is raised to 90% per Finding 4, consider restricting the bypass to maintainer-applied PR labels rather than commit message strings.

---

## L2 Strategic Implications

### Supply Chain Security Posture

The pipeline has good instincts: SHA-pinned actions, pinned uv version, `--frozen` lockfile enforcement on test jobs. The gap is that three legacy jobs (`lint`, `type-check`, `security`) predate the uv adoption and were never migrated. This creates a two-tier supply chain posture within a single workflow: jobs 1-3 operate without lockfile protection while jobs 4-14 are fully governed.

**Recommended remediation sequence:**
1. Fix `type-check` pip install first (Finding 1, HIGH) -- highest SLSA impact
2. Fix `security` audit scope second (Finding 2, HIGH) -- false compliance is more dangerous than no compliance
3. Migrate `lint` to uv (Finding 1, LOW portion) -- low risk but removes the inconsistency
4. Fix `python3` in plugin-validation (Finding 5, MEDIUM) -- quick fix

### SAST/SCA Coverage Assessment

| Category | Tool | Status | Gap |
|----------|------|--------|-----|
| SAST | None configured | ABSENT | No static security analysis beyond banned-API grep |
| SCA (dependency CVEs) | pip-audit | Partial | Audit scope covers only 3 of N packages (Finding 2) |
| Secrets scanning | None | ABSENT | No Gitleaks or TruffleHog configured |
| Container scanning | N/A | N/A | No container images |
| IaC scanning | N/A | N/A | No IaC in scope |
| SBOM | None | ABSENT | No SBOM generation |

**Recommended additions (priority order):**

1. **Secrets scanning (Gitleaks):** Add a `secrets-scan` job before `security`. A single leaked credential in history invalidates all other controls. GitHub Actions provides `gitleaks/gitleaks-action` with SHA pinning support.

2. **SAST (Semgrep):** Add a `semgrep` job running the `p/python` ruleset. The existing banned-YAML-API grep (lines 98-113) is a manual implementation of what Semgrep automates. Semgrep has an official GitHub Action with SHA pinning support.

3. **Full SCA via pip-audit on lockfile (Finding 2 fix):** This is the highest-priority item. Once fixed, SCA coverage becomes comprehensive.

4. **SBOM generation:** Add a `sbom` job using `anchore/sbom-action` generating a CycloneDX SBOM artifact on releases. This addresses SLSA Level 1 documentation requirements.

### SLSA Maturity Assessment

| Level | Requirement | Current Status |
|-------|-------------|----------------|
| L1 | Automated build | Partial -- build runs in CI but no provenance artifact |
| L1 | Documentation of build process | Present -- ADR-CI-001 referenced |
| L2 | Hosted platform build | Present -- GitHub Actions |
| L2 | Signed provenance | ABSENT -- no `actions/attest-build-provenance` configured |
| L3 | Hardened build | ABSENT -- no ephemeral credentials, no non-falsifiable attestations |

Current effective SLSA level: 1 (borderline). Adding `actions/attest-build-provenance` on the release workflow (out of scope for this review but implied by the pipeline structure) would achieve L2.

### False Positive Assessment

No false positives in this review. All findings are grounded in specific line references from the pipeline. The HIGH findings are definitively exploitable gaps (unrestricted pip resolution in `type-check`, proven-incomplete audit scope in `security`). The MEDIUM findings are policy mismatches with documented governance rules (H-05, H-20). Confidence: HIGH on Findings 1-5, MEDIUM on Findings 6-8 (operational concerns without confirmed incidents).

---

*Generated by eng-devsecops | SSDF alignment: PW.7 (automated analysis), PS.1 (supply chain protection)*
*Pipeline source: /tmp/ci-yml-main.txt (707 lines, 29 jobs)*
*Review scope: Supply chain, SCA coverage, installation consistency, job optimization*
