# Security Review: STORY-010 Plugin JSON Agent Sync

**Reviewer:** eng-security
**Date:** 2026-03-26
**Scope:** `.github/workflows/ci.yml` (frontmatter-validation job and ci-success gate), `scripts/check_plugin_agent_sync.py`, `.claude-plugin/plugin.json`
**Standard:** OWASP ASVS 5.0 (V5, V7, V9), CWE Top 25 2025
**CVSS Version:** 3.1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Findings by severity, top risks, immediate actions |
| [L1 Technical Detail](#l1-technical-detail) | Individual findings with CWE, CVSS, evidence, remediation |
| [L2 Strategic Implications](#l2-strategic-implications) | Security posture, patterns, architectural recommendations |
| [ASVS Verification Status](#asvs-verification-status) | Chapter-level pass/fail |
| [Artifact Coverage](#artifact-coverage) | Files reviewed and review completeness |

---

## L0 Executive Summary

### Finding Counts by Severity

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 2 |
| Low | 2 |
| Informational | 3 |
| **Total** | **7** |

### Overall Security Assessment

**PASS with remediation required.** No critical or high vulnerabilities were found. The three artifacts are structurally sound with good security hygiene: action pins are hash-locked, the changelog check correctly uses env vars to prevent shell injection (CLCHK-001), the drift script uses only stdlib and performs no shell execution, and all 89 plugin.json paths resolve to existing files entirely within `skills/`. Two medium findings require attention before merge.

### Top 3 Risk Areas

1. **Drift script not wired into CI (Medium):** `check_plugin_agent_sync.py` exists and functions correctly but is never called by any CI job. The sync guarantee it provides is entirely manual. Plugin drift can silently enter main without CI detection.

2. **MishaKav action pinned to mutable-branch reference label (Medium):** `MishaKav/pytest-coverage-comment` is SHA-pinned (correct) but the comment annotation reads `# main (2026-03-09)` rather than a version tag. This is a documentation correctness issue that misleads maintainers into believing the action tracks the `main` branch, which could cause an incorrect re-pin to a mutable ref during future maintenance.

3. **Banned YAML API check has a narrow false-negative (Low):** The `grep -v 'yaml\.safe_load('` suppression in the security job can incorrectly silence a genuine `yaml.load(` detection when both strings appear on the same line (e.g., inline comments). The probability is low but the suppression is logically inverted from intent.

### Recommended Immediate Actions

1. Add a CI job (or extend `plugin-validation`) to call `uv run python scripts/check_plugin_agent_sync.py` and wire it into the `ci-success` gate.
2. Update the MishaKav action comment from `# main (2026-03-09)` to a version tag or a clear SHA-date annotation.
3. Fix the YAML banned-API grep to use a positive match only, removing the `-v` suppression.

---

## L1 Technical Detail

---

### FINDING-001 (Medium) -- Drift Detection Script Not Called in CI

**CWE:** CWE-693 -- Protection Mechanism Failure
**CVSS 3.1 Base Score:** 5.3 (AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N)
**CVSS Vector:** AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N

**Location:** `.github/workflows/ci.yml` -- no reference to `check_plugin_agent_sync.py`

**Evidence:**

Search of `.github/workflows/ci.yml` returned zero matches for `check_plugin_agent_sync` or `plugin_agent_sync`. The `plugin-validation` job calls only `validate_plugin_manifests.py`. The `validate_plugin_manifests.py` script does not invoke the sync script internally (confirmed: grep of that file returned no sync reference). The `ci-success` gate therefore does not enforce plugin/disk parity.

The drift script itself is correct: it compares `skills/*/agents/*.md` on disk against the `agents` array in `plugin.json`, excludes `.graveyard`, and exits non-zero on drift. The detection logic works. The enforcement gap is purely the missing CI invocation.

**Impact:** An agent `.md` file can be added to `skills/` without being registered in `plugin.json`, or a path can be removed from disk while remaining in `plugin.json`, without any CI failure. The current 89-for-89 sync is correct but is not protected by automation.

**Data Flow Trace:**
```
Developer adds new agent file
  -> Git push -> CI pipeline runs
  -> plugin-validation job runs validate_plugin_manifests.py (schema only)
  -> check_plugin_agent_sync.py is NEVER called
  -> ci-success gate passes even with drift
  -> Drift silently enters main
```

**Remediation:** Add a step to the `plugin-validation` job (or a standalone `plugin-sync` job) and wire it into `ci-success`:

```yaml
# Option A: Add to existing plugin-validation job
- name: Check plugin/disk agent sync
  run: uv run python scripts/check_plugin_agent_sync.py

# Option B: Standalone job (add to ci-success needs list)
plugin-sync:
  name: Plugin Agent Sync
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
    - name: Install uv
      uses: astral-sh/setup-uv@e06108dd0aef18192324c70427afc47652e63a82 # v7.5.0
      with:
        version: "0.10.9"
    - name: Set up Python
      run: uv python install 3.14
    - name: Install dependencies
      run: uv sync --frozen
    - name: Check plugin/disk agent sync
      run: uv run python scripts/check_plugin_agent_sync.py
```

If using Option A, also add `plugin-sync` to the `ci-success` needs evaluation block. If extending `plugin-validation`, no `ci-success` changes are needed since `plugin-validation` is already gated.

---

### FINDING-002 (Medium) -- MishaKav Action Pinned to Mutable Branch Label

**CWE:** CWE-829 -- Inclusion of Functionality from Untrusted Control Sphere
**CVSS 3.1 Base Score:** 4.3 (AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N)
**CVSS Vector:** AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N

**Location:** `.github/workflows/ci.yml`, line 497

**Evidence:**

```yaml
uses: MishaKav/pytest-coverage-comment@6b219eafc7094a43abafd1fbd0c6c48de8cc2141 # main (2026-03-09)
```

The action is correctly SHA-pinned, which is the right security control for supply chain protection. However, the comment `# main (2026-03-09)` labels this as a `main` branch reference rather than a version tag. All other actions in the file use `# v{major}.{minor}.{patch}` comments (e.g., `# v6.0.2`, `# v7.5.0`, `# v8.0.1`). This inconsistency creates a maintenance risk: a future contributor performing pin updates may interpret `main` as a branch reference and re-pin using `@main` (a mutable ref), which would eliminate the supply-chain protection.

The current SHA `6b219eafc7094a43abafd1fbd0c6c48de8cc2141` does protect the running workflow from supply chain attacks. The risk is exclusively forward-looking: future maintenance of this pin.

**Remediation:** Determine the release tag that corresponds to SHA `6b219eafc7094a43abafd1fbd0c6c48de8cc2141` by checking the MishaKav/pytest-coverage-comment release history, then update the comment to match the convention used elsewhere:

```yaml
# Before (current):
uses: MishaKav/pytest-coverage-comment@6b219eafc7094a43abafd1fbd0c6c48de8cc2141 # main (2026-03-09)

# After (remediated - example if SHA corresponds to v1.x.x):
uses: MishaKav/pytest-coverage-comment@6b219eafc7094a43abafd1fbd0c6c48de8cc2141 # v1.x.x

# If no version tag exists for this SHA (action uses main only), annotate clearly:
uses: MishaKav/pytest-coverage-comment@6b219eafc7094a43abafd1fbd0c6c48de8cc2141 # SHA-pinned, no release tag; pinned 2026-03-09
```

---

### FINDING-003 (Low) -- Banned YAML API Check Has False-Negative Suppression Logic

**CWE:** CWE-1068 -- Inconsistency Between Implementation and Documented Design
**CVSS 3.1 Base Score:** 2.4 (AV:N/AC:H/PR:H/UI:R/S:U/C:N/I:L/A:N)

**Location:** `.github/workflows/ci.yml`, lines 101-108

**Evidence:**

```bash
if grep -rn 'yaml\.load(' src/ --include='*.py' | grep -v 'yaml\.safe_load('; then
  echo "ERROR: Found yaml.load() usage. Use yaml.safe_load() only (M-04b)."
  FOUND=1
fi
```

The pipeline `grep -rn 'yaml\.load('` finds lines containing `yaml.load(`. The `-v 'yaml\.safe_load('` then suppresses any line that also contains the string `yaml.safe_load(`. The intent is to exclude false positives from lines like `# Prefer yaml.safe_load() over yaml.load()`. However the suppression is applied after the match, meaning a genuine `yaml.load(something)` call on a line that also contains a comment referencing `yaml.safe_load()` would be silently suppressed -- a false negative. The pattern also does not catch `yaml.load(` if it is aliased through a variable (`loader = yaml.load; loader(data, Loader=yaml.UnsafeLoader)`).

The practical risk is low: this check supplements the `pip-audit` and `ruff` linting that already runs. A developer intentionally bypassing this check would be unlikely to craft such a line accidentally.

**Remediation:** Remove the `-v` suppression and rely on the grep pattern alone. The pattern `yaml\.load\(` is specific enough that inline `yaml.safe_load` comments on the same line are an extreme edge case not worth protecting against:

```bash
# Before:
if grep -rn 'yaml\.load(' src/ --include='*.py' | grep -v 'yaml\.safe_load('; then

# After:
if grep -rn 'yaml\.load(' src/ --include='*.py'; then
```

If false positives from comment lines are a genuine concern, tighten the primary pattern to exclude comment-only lines:

```bash
if grep -rn 'yaml\.load(' src/ --include='*.py' | grep -v '^\s*#'; then
```

---

### FINDING-004 (Low) -- No Type Validation on plugin.json Agents Array Elements

**CWE:** CWE-20 -- Improper Input Validation
**CVSS 3.1 Base Score:** 2.7 (AV:L/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N)

**Location:** `scripts/check_plugin_agent_sync.py`, line 102

**Evidence:**

```python
return set(data["agents"])
```

The function validates that the `agents` key exists in the parsed JSON, and that the JSON is valid, but does not validate that each element in the `agents` array is a string. If `plugin.json` contains a malformed agents array (e.g., `"agents": [{"path": "./skills/..."}]` or `"agents": [null, "./skills/..."]`), the `set()` call succeeds but the resulting set contains non-string elements. Subsequent set difference operations (`disk_agents - plugin_agents`) would complete without error but the non-string elements would never match any disk path string, producing false "stale" reports rather than an error.

The H-11 type annotation `set[str]` documents the intended contract but is not enforced at runtime. The exit code 2 (parse/IO error) would not fire, so the caller would receive a misleading exit code 1 (drift detected) rather than exit code 2 (parse error).

**Remediation:** Add element type validation after parsing:

```python
agents = data["agents"]
if not isinstance(agents, list):
    raise ValueError(f"plugin.json 'agents' key must be a list, got {type(agents).__name__}")
invalid = [item for item in agents if not isinstance(item, str)]
if invalid:
    raise ValueError(
        f"plugin.json 'agents' contains {len(invalid)} non-string element(s): "
        f"{invalid[:3]}{'...' if len(invalid) > 3 else ''}"
    )
return set(agents)
```

---

### FINDING-005 (Informational) -- skip-coverage Marker Unavailable on Pull Request Events

**CWE:** N/A (configuration clarity)
**Severity:** Informational

**Location:** `.github/workflows/ci.yml`, lines 334-351 and 435-452

**Evidence:**

```yaml
if: ${{ !contains(github.event.head_commit.message, '[skip-coverage]') }}
```

`github.event.head_commit` is only populated for `push` events. On `pull_request` events, `head_commit` is `null`. GitHub Actions evaluates `contains(null, '[skip-coverage]')` as `false`, meaning the coverage threshold always enforces on PRs regardless of commit message content. This is the safe behavior (coverage enforced), but it means PR authors cannot use `[skip-coverage]` to bypass coverage for refactoring PRs -- the marker only works on direct pushes to branches.

No code change is required. The behavior is safe. This should be documented in the CI README or as a comment in the YAML so maintainers do not spend time debugging why `[skip-coverage]` has no effect on PRs.

---

### FINDING-006 (Informational) -- coverage-report Job Absent from ci-success Gate

**CWE:** N/A (gate coverage)
**Severity:** Informational

**Location:** `.github/workflows/ci.yml`, lines 619-635

**Evidence:**

The `coverage-report` job is listed in `needs: [test-pip, test-uv]` at line 486 and runs only on `pull_request` events. It is correctly absent from the `ci-success` gate check block (lines 624-635), which mirrors the treatment of `changelog-check` (also PR-only). However, unlike `changelog-check`, there is no comment in `ci-success` explaining why `coverage-report` is excluded. If `coverage-report` fails (e.g., artifact download fails), the CI green light is unaffected.

This is intentional: `coverage-report` is a reporting job, not a quality gate. The actual coverage thresholds are enforced by `test-pip` and `test-uv` (`--cov-fail-under=80`). No code change required, but a comment mirroring the CLCHK-003 pattern would prevent confusion:

```yaml
# coverage-report only runs on PRs (if: github.event_name == 'pull_request').
# On push events it reports "skipped" -- this is expected, not a failure.
# Coverage thresholds are enforced by test-pip and test-uv jobs.
```

---

### FINDING-007 (Informational) -- Lint and Type-Check Jobs Use pip Directly (H-05 Scope Clarification)

**CWE:** N/A (framework standards boundary)
**Severity:** Informational

**Location:** `.github/workflows/ci.yml`, lines 40, 64-66, 87-96

**Evidence:**

The `lint`, `type-check`, and `security` jobs install Python tools using `pip install` directly rather than `uv`. H-05 mandates `uv run` for all Python execution and `uv add` for dependencies. These jobs use the `actions/setup-python` action rather than `astral-sh/setup-uv`, and install tools like `ruff`, `pyright`, and `pip-audit` via `pip install` with pinned versions.

**Assessment:** H-05 applies to the Jerry application source code and developer environment. Its purpose is to prevent environment corruption from mixed package manager usage in the project's Python environment. CI jobs that bootstrap standalone tools (ruff, pyright, pip-audit) in a throwaway runner environment do not share state with the project's uv-managed environment and are not subject to the same corruption risk H-05 addresses. The jobs that run application code (`plugin-validation`, `frontmatter-validation`, `cli-integration`, `test-uv`) correctly use `uv`. No remediation required. This finding documents that H-05 does not apply to CI bootstrap steps.

---

## ASVS Verification Status

| ASVS Chapter | Focus | Status | Notes |
|---|---|---|---|
| V1 -- Architecture | CI pipeline structure, trust boundaries | PASS | No privileged secrets exposed; permissions scoped to `contents: read` + `pull-requests: write` |
| V5 -- Validation, Sanitization, Encoding | Input handling in scripts and CI steps | PARTIAL PASS | FINDING-004 (missing element type validation in drift script); changelog check correctly uses env vars (CLCHK-001) |
| V7 -- Error Handling and Logging | Script exit codes, error output | PASS | Drift script has three distinct exit codes (0/1/2) correctly mapped; error output directed to stderr |
| V9 -- Communication | Supply chain / action integrity | PARTIAL PASS | All actions SHA-pinned (correct); FINDING-002 (comment annotation misleads maintainers on one action) |

---

## L2 Strategic Implications

### Security Posture Assessment

The three artifacts demonstrate sound security fundamentals: supply chain attacks are mitigated through consistent SHA pinning of all GitHub Actions, shell injection is explicitly addressed via environment variable isolation in the changelog check (CLCHK-001), the banned YAML API check enforces CWE-502 prevention (unsafe deserialization), and all 89 plugin.json paths are confirmed to resolve to real files within the `skills/` boundary with no path traversal opportunities.

The drift detection script is well-structured: it uses only Python stdlib (no shell execution, no subprocess, no eval), applies proper `.graveyard` exclusion, normalizes paths consistently with `as_posix()`, and provides three semantically distinct exit codes. The ASVS V7 (error handling) compliance is good.

### Systemic Vulnerability Patterns

**Pattern: Incomplete CI Wiring.** FINDING-001 reveals a recurring pattern where a script is written and validated in isolation but not integrated into the CI enforcement gate. This same pattern was present with the HARD rule ceiling check before it was added to `ci-success`. The drift script represents the third instance of this pattern (after `check_hard_rule_ceiling.py` and `check_spdx_headers.py`, both of which required explicit CI wiring). This suggests a process gap: new scripts in `scripts/` should require a paired CI job as a definition-of-done criterion.

**Pattern: Comment-as-Version Documentation Inconsistency.** FINDING-002 reflects a single exception to an otherwise consistent version-comment convention across all action pins. The inconsistency is not a runtime risk but creates a maintenance trap. The root cause is that `MishaKav/pytest-coverage-comment` does not publish semver releases, making the convention difficult to apply uniformly. The resolution is either explicit SHA-date annotation or a project-level policy decision about third-party actions without versioned releases.

### Comparison with Threat Model Predictions

No formal threat model artifact was provided for this review. The review was conducted against the stated OWASP ASVS chapters and CWE Top 25 focus areas. The findings align with the expected risk profile of a CI/CD pipeline and developer tooling script: supply chain (CWE-829) and input validation (CWE-20) are the relevant threat categories; injection and authentication threats are not applicable to these artifact types.

### Recommendations for Security Architecture Evolution

1. **CI wiring gate for scripts/.** Establish a convention that any script added to `scripts/` that is intended as a quality gate MUST have a corresponding CI job added in the same PR. Enforce this via a checklist item in the PR template or via a grep-based CI check that validates every `uv run python scripts/*.py` invocation in CI against the scripts directory contents.

2. **Standardize action annotation policy.** For third-party GitHub Actions without semver releases, adopt a consistent annotation pattern (e.g., `# SHA-pinned YYYY-MM-DD, no release tag`) and add this to the CI contribution guide. Prevents maintainer confusion during future pin updates.

3. **Runtime type validation for JSON inputs.** The drift script pattern of parsing JSON and treating array contents as typed without validation is a common source of silent failures. Consider adding a lightweight JSON Schema validation step for `plugin.json` itself (separate from the agent frontmatter schema validation), to catch malformed array structures before the drift check runs.

---

## Artifact Coverage

| File | Lines Reviewed | Review Completeness |
|---|---|---|
| `.github/workflows/ci.yml` | All 675 lines | Complete |
| `scripts/check_plugin_agent_sync.py` | All 227 lines | Complete |
| `.claude-plugin/plugin.json` | All 116 lines | Complete; all 89 paths verified against disk |
| `skills/` disk agents | 89 files enumerated | Path existence verified; content not reviewed |

**Review method:** Manual data flow tracing (Read, Grep, Bash verification of path resolution). No automated scanning tools were used. CWE Top 25 2025 checklist applied to artifact type (CI YAML, Python script, JSON manifest). ASVS 5.0 chapters V1, V5, V7, V9 verified.

**Confidence:** 0.90 -- High. All findings are evidence-based with code-level citations. The one area of lower confidence is the MishaKav action version mapping (FINDING-002), which requires external verification of the SHA against the upstream release history.
