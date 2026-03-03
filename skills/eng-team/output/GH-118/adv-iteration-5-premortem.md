# Pre-Mortem Report: PROJ-017 macOS Symlink Resolution Portability Fix

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** PROJ-017 Platform Portability Fix (GH-118 / BUG-017-006)
**Criticality:** C3 (platform portability changes, cross-platform impact)
**Date:** 2026-02-26
**Reviewer:** adv-executor (S-004)
**H-16 Compliance:** S-003 Steelman not applicable (iteration 5 of existing work; prior iterations included S-002, S-014)
**Failure Scenario:** It is August 2026 (6 months from now). The macOS symlink resolution fix has failed spectacularly. Jerry users on vanilla macOS (without Homebrew coreutils) report intermittent bootstrap failures. The production worktree creation script fails silently on 30% of macOS installations. The team has reverted the changes and is investigating why the portable solution did not work as expected.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | Pre-Mortem failure causes with PM-NNN identifiers |
| [Finding Details](#finding-details) | Detailed analysis of Critical and Major findings |
| [Recommendations](#recommendations) | Prioritized mitigation plan (P0/P1/P2) |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |

---

## Summary

**Overall Assessment:** The portability fix implementation contains **1 Critical** and **4 Major** failure causes that could lead to silent failures, inconsistent behavior across platforms, and user confusion. The fix assumes runtime conditions that may not hold (uv availability, PATH configuration), lacks comprehensive error handling and user guidance, and has insufficient test coverage for edge cases. The approach is fundamentally sound (prioritized fallback chain), but execution gaps create significant failure risk.

**Recommendation:** **REVISE** -- Address all P0 (Critical) and P1 (Major) findings before merge. The fix is 70% complete; targeted revisions will bring it to production-ready state. Focus on: (1) comprehensive error messaging with actionable guidance, (2) smoke test suite for all platform/environment combinations, (3) documentation updates with troubleshooting section, (4) validation of uv availability assumptions.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260226T1500 | `uv` assumed available but not installed on user's macOS; script fails with cryptic "uv: command not found" | Assumption | High | Critical | P0 | Methodological Rigor |
| PM-002-20260226T1500 | Silent fallback to basic `readlink` does not log degraded mode; user unaware of partial resolution | Process | Medium | Major | P1 | Actionability |
| PM-003-20260226T1500 | No smoke tests for vanilla macOS (no Homebrew, no `greadlink`); edge case undetected until production | Process | High | Major | P1 | Evidence Quality |
| PM-004-20260226T1500 | Error message "Install GNU coreutils or ensure uv is available" unhelpful when user has uv but PATH misconfigured | Technical | Medium | Major | P1 | Actionability |
| PM-005-20260226T1500 | Linux code path unchanged (still uses `readlink -f`); inconsistent fallback strategy across platforms | Technical | Low | Major | P1 | Internal Consistency |
| PM-006-20260226T1500 | No documentation update for macOS setup requirements; users do not know `greadlink` or `uv` are preferred | Process | Medium | Minor | P2 | Completeness |

---

## Finding Details

### PM-001-20260226T1500: `uv` Assumed Available But Not Installed [CRITICAL]

**Failure Cause:** The `realpath_portable()` function assumes that if `uv` is in PATH, it will successfully execute. However, on a fresh macOS installation where a user clones the Jerry repository but has not yet run `bootstrap`, `uv` will not be installed. The script's Priority 2 fallback (`uv run python`) will fail with "command not found," and the error message instructs the user to "ensure uv is available" without explaining how to install it.

**Category:** Assumption

**Likelihood:** High -- Fresh clones on macOS are common during onboarding; many users will not have `uv` pre-installed.

**Severity:** Critical -- Blocks bootstrap on vanilla macOS; user cannot proceed without external guidance. The fix was intended to remove the `greadlink` dependency, but introduced a new `uv` dependency that is not communicated clearly.

**Evidence:**
- `realpath_portable()` function lines 136-141 check `command -v uv` but do not distinguish between "uv not installed" vs. "uv installed but failed"
- Error guidance (lines 168-169) assumes user knows what `uv` is and how to install it
- No validation in bootstrap process that `uv` is available before symlink resolution is attempted

**Dimension:** Methodological Rigor -- The fix assumes a runtime precondition (uv availability) that is not guaranteed or validated.

**Mitigation:**
1. **Pre-check in bootstrap script:** Before invoking `realpath_portable()`, verify `uv` is available. If not, emit clear guidance: "Jerry requires uv for Python environment management. Install via: curl -LsSf https://astral.sh/uv/install.sh | sh"
2. **Fallback ordering revision:** Consider moving `uv run python` fallback AFTER basic `readlink` (Priority 3 becomes Priority 2). This degrades gracefully on vanilla macOS without blocking bootstrap.
3. **Error message enhancement:** Replace generic "ensure uv is available" with "Install uv via: curl -LsSf https://astral.sh/uv/install.sh | sh, then retry."

**Acceptance Criteria:**
- [ ] Bootstrap script validates `uv` availability before symlink operations
- [ ] Error message includes explicit installation command for `uv`
- [ ] Fallback chain does not hard-fail on missing `uv` if basic `readlink` can succeed

---

### PM-002-20260226T1500: Silent Fallback to Basic `readlink` [MAJOR]

**Failure Cause:** When Priority 1 (`greadlink`) and Priority 2 (`uv`) both fail, `realpath_portable()` silently falls back to basic `readlink` (Priority 3, lines 145-154). This fallback "works for simple cases" per the comment, but may not fully resolve nested symlinks. The script provides no log output indicating degraded mode, so the user is unaware that resolution quality has degraded. Six months later, a bug is traced to an unresolved nested symlink that the basic `readlink` fallback missed.

**Category:** Process

**Likelihood:** Medium -- Nested symlinks in Jerry repository are rare, but context distribution hooks create symlink chains that could exceed basic `readlink` capability.

**Severity:** Major -- Subtle corruption of symlink verification; does not fail loudly, but introduces silent data integrity risk.

**Evidence:**
- Lines 145-154: basic `readlink` fallback executes without logging
- Comment "may not fully resolve nested symlinks" acknowledges degraded behavior but does not surface it to user
- No test coverage for nested symlink scenarios in current implementation

**Dimension:** Actionability -- User has no signal that degraded fallback was used and cannot take corrective action.

**Mitigation:**
1. **Add logging for degraded fallback:** When Priority 3 (basic `readlink`) is used, emit `log_warn "Using degraded symlink resolution (basic readlink); install greadlink (brew install coreutils) or ensure uv is available for full resolution"`
2. **Test nested symlinks:** Add test case: create symlink A -> B -> C, verify `realpath_portable()` resolves to C regardless of which fallback is used
3. **Document limitations:** Update script header comment to note that basic `readlink` fallback has limited nested symlink support

**Acceptance Criteria:**
- [ ] Degraded fallback logs warning message visible to user
- [ ] Test case validates nested symlink resolution
- [ ] Script documentation notes fallback limitations

---

### PM-003-20260226T1500: No Smoke Tests for Vanilla macOS [MAJOR]

**Failure Cause:** The implementation lacks automated tests for the target environment: vanilla macOS without Homebrew coreutils and without `uv` pre-installed. The "Verification Results" section (lines 430-482) documents successful execution with `uv` available, but does not test the scenario where neither `greadlink` nor `uv` are present. Six months later, a contributor submits a PR that breaks basic `readlink` fallback, and CI does not catch it because there is no test matrix covering vanilla macOS.

**Category:** Process

**Likelihood:** High -- CI environments typically have package managers and dependencies pre-installed; vanilla macOS is rarely tested unless explicitly targeted.

**Severity:** Major -- Missing test coverage for the exact failure mode the fix is intended to address (macOS without GNU coreutils).

**Evidence:**
- "Verification Results" section shows testing only with `uv` available (Priority 2 fallback)
- No documented test matrix covering: (a) greadlink available, (b) uv available but no greadlink, (c) neither available (basic readlink only)
- No CI configuration file changes in implementation to enforce multi-platform testing

**Dimension:** Evidence Quality -- Fix lacks empirical validation of core use case (vanilla macOS bootstrap).

**Mitigation:**
1. **Add GitHub Actions test matrix:**
   ```yaml
   strategy:
     matrix:
       os: [ubuntu-latest, macos-latest]
       environment:
         - name: "vanilla"  # No greadlink, no uv
         - name: "homebrew" # greadlink available
         - name: "uv-only"  # uv available, no greadlink
   ```
2. **Create smoke test script:** `scripts/test-symlink-resolution.sh` that validates all three fallback paths
3. **Document test procedure:** Add "Testing" section to BUG-017-006.md with step-by-step manual validation for each fallback

**Acceptance Criteria:**
- [ ] CI test matrix includes vanilla macOS (no greadlink, no uv)
- [ ] Smoke test script validates all three fallback priorities
- [ ] Manual test procedure documented in bug entity file

---

### PM-004-20260226T1500: Unhelpful Error Message for PATH Misconfiguration [MAJOR]

**Failure Cause:** When `uv` is installed but not in the user's PATH (common on macOS where shell profile is not sourced in non-interactive contexts), the error message "Install GNU coreutils (brew install coreutils) or ensure uv is available" (lines 168-169) does not help the user diagnose the problem. The user sees "uv: command not found" even though `uv` is installed at `~/.local/bin/uv`. Six months later, support tickets accumulate with users unable to bootstrap because their shell PATH configuration is incorrect.

**Category:** Technical

**Likelihood:** Medium -- PATH issues are common on macOS, especially in non-interactive contexts (scripts invoked by IDE, CI, or hooks).

**Severity:** Major -- Creates user friction and support burden; the fix is present but user cannot discover how to make it work.

**Evidence:**
- Error message assumes `uv` is either "installed" or "not installed," ignoring the "installed but not in PATH" case
- No check for `~/.local/bin/uv` presence if `command -v uv` fails
- No guidance for users to add `uv` to PATH

**Dimension:** Actionability -- Error message does not guide user to correct solution for PATH misconfiguration.

**Mitigation:**
1. **Enhanced PATH check:** If `command -v uv` fails, check for `uv` at known installation paths:
   ```bash
   if [[ ! -x "$(command -v uv)" ]] && [[ -x "$HOME/.local/bin/uv" ]]; then
       log_error "uv found at $HOME/.local/bin/uv but not in PATH"
       log_error "Add to PATH: export PATH=\"\$HOME/.local/bin:\$PATH\""
       return 1
   fi
   ```
2. **Error message triage:** Emit different error messages for: (a) `uv` not installed anywhere, (b) `uv` installed but not in PATH
3. **Bootstrap PATH fix:** Jerry bootstrap script should ensure `~/.local/bin` is in PATH before invoking symlink operations

**Acceptance Criteria:**
- [ ] Script detects `uv` at `~/.local/bin/uv` even if not in PATH
- [ ] Error message differentiates "not installed" from "not in PATH"
- [ ] Bootstrap process validates PATH configuration before symlink operations

---

### PM-005-20260226T1500: Linux Code Path Unchanged [MAJOR]

**Failure Cause:** The `realpath_portable()` function is only invoked for macOS (lines 179-181, 232-233, 262-263). The Linux code path continues to use `readlink -f` directly (lines 183-184, 235-236, 264-265). This creates an inconsistency: if `uv` is unavailable on Linux, there is no fallback, but the same scenario on macOS has three fallback options. Six months later, a user reports Jerry bootstrap failure on a minimal Linux container that lacks GNU coreutils, and the team realizes the fix did not make the script truly portable -- it only addressed macOS.

**Category:** Technical

**Likelihood:** Low -- Most Linux distributions ship with GNU coreutils; `readlink -f` availability is near-universal on Linux.

**Severity:** Major -- Violates the stated goal of "platform portability"; the fix is incomplete.

**Evidence:**
- `resolve_symlink()` function line 183: Linux path uses `readlink -f` directly
- `is_within_tree()` function line 235: Linux path uses `readlink -f` directly
- `parse_args()` function line 264: Linux path uses `readlink -f` directly
- No `realpath_portable()` invocation on Linux code paths

**Dimension:** Internal Consistency -- Fix claims to be "portable" but only applies portability logic to macOS.

**Mitigation:**
1. **Unify code paths:** Use `realpath_portable()` for both macOS and Linux. Remove platform-specific branches.
   ```bash
   # Before (line 223-231):
   if [[ "$(uname)" == "Darwin" ]]; then
       target=$(realpath_portable "$symlink" 2>/dev/null) || true
   else
       target=$(readlink -f "$symlink" 2>/dev/null) || true
   fi

   # After:
   target=$(realpath_portable "$symlink" 2>/dev/null) || true
   ```
2. **Test on minimal Linux:** Add CI test with Alpine Linux or minimal Debian container to validate fallback chain on non-GNU systems
3. **Update fix scope:** Revise BUG-017-006 acceptance criteria to state "Works on macOS AND Linux without GNU coreutils"

**Acceptance Criteria:**
- [ ] `realpath_portable()` used for both macOS and Linux
- [ ] Test matrix includes minimal Linux container (Alpine or Debian slim)
- [ ] Fix scope updated to cover Linux portability

---

### PM-006-20260226T1500: No Documentation Update [MINOR]

**Failure Cause:** The fix does not update Jerry's setup documentation to explain that `greadlink` (via Homebrew coreutils) is the preferred method on macOS, or that `uv` is required for the fallback. Six months later, a new contributor on macOS experiences slow bootstrap performance (using basic `readlink` fallback) and opens a GitHub Issue asking why Jerry is so slow. The team realizes users are not aware they should install `greadlink` for optimal performance.

**Category:** Process

**Likelihood:** Medium -- Documentation gaps are common; users rely on documentation for setup guidance.

**Severity:** Minor -- Does not block functionality, but degrades user experience and creates support burden.

**Evidence:**
- No update to `docs/setup/macos.md` (if such file exists) or equivalent setup guide
- No mention of `greadlink` preference in bootstrap script comments
- No troubleshooting section for "slow bootstrap on macOS"

**Dimension:** Completeness -- Fix is incomplete without documentation of recommended setup and troubleshooting guidance.

**Mitigation:**
1. **Add macOS setup guide:** Create `docs/setup/macos.md` (or update existing) with:
   - **Recommended:** Install Homebrew coreutils (`brew install coreutils`) for optimal symlink resolution
   - **Required:** Ensure `uv` is installed and in PATH (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
   - **Troubleshooting:** If bootstrap is slow, check if `greadlink` is available (`command -v greadlink`)
2. **Update README.md:** Add macOS-specific setup note in platform requirements section
3. **Script header comment:** Update `verify-symlinks.sh` header with macOS setup guidance

**Acceptance Criteria:**
- [ ] Documentation includes macOS setup recommendations
- [ ] Troubleshooting section covers slow bootstrap and missing dependencies
- [ ] README.md notes macOS-specific requirements

---

## Recommendations

### P0 (Critical -- MUST Mitigate Before Acceptance)

| Finding ID | Mitigation | Acceptance Criteria |
|-----------|------------|---------------------|
| PM-001-20260226T1500 | Pre-check `uv` availability in bootstrap; enhance error message with installation command; revise fallback ordering to degrade gracefully | Bootstrap validates `uv` before symlink ops; error message includes installation command; fallback chain does not hard-fail on missing `uv` |

### P1 (Important -- SHOULD Mitigate)

| Finding ID | Mitigation | Acceptance Criteria |
|-----------|------------|---------------------|
| PM-002-20260226T1500 | Log warning when degraded fallback (basic `readlink`) is used; add nested symlink test case | Degraded fallback logs warning; test validates nested symlink resolution |
| PM-003-20260226T1500 | Add GitHub Actions test matrix for vanilla macOS; create smoke test script; document manual test procedure | CI tests vanilla macOS; smoke test validates all fallbacks; test procedure documented |
| PM-004-20260226T1500 | Enhanced PATH check for `~/.local/bin/uv`; differentiate "not installed" vs. "not in PATH" errors | Script detects `uv` at known paths; error messages differentiate cases |
| PM-005-20260226T1500 | Unify macOS and Linux code paths to use `realpath_portable()` universally; test on minimal Linux | Unified code path; minimal Linux CI test |

### P2 (Monitor -- MAY Mitigate; Acknowledge Risk)

| Finding ID | Mitigation | Acceptance Criteria |
|-----------|------------|---------------------|
| PM-006-20260226T1500 | Add macOS setup guide; update README.md; enhance script header comments | Documentation includes setup recommendations and troubleshooting |

---

## Scoring Impact

**Mapping to S-014 Scoring Dimensions:**

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-006-20260226T1500: Documentation gap. PM-005-20260226T1500: Linux portability incomplete. |
| Internal Consistency | 0.20 | Negative | PM-005-20260226T1500: Inconsistent fallback strategy between macOS and Linux. |
| Methodological Rigor | 0.20 | Negative | PM-001-20260226T1500: Assumes `uv` availability without validation. PM-003-20260226T1500: Lacks test coverage for target environment. |
| Evidence Quality | 0.15 | Negative | PM-003-20260226T1500: No empirical validation of vanilla macOS scenario. |
| Actionability | 0.15 | Negative | PM-002-20260226T1500: Silent degraded mode. PM-004-20260226T1500: Unhelpful error messages. |
| Traceability | 0.10 | Neutral | Clear implementation traceability from BUG-017-006 to eng-backend implementation. |

**Estimated Composite Score Impact:**
- **Without mitigations:** ~0.78 (5 of 6 dimensions negative; only Traceability neutral)
- **With P0 + P1 mitigations:** ~0.92 (addresses Critical and Major findings; minor documentation gap remains)
- **Target:** >= 0.95 (C3 engagement per owner feedback on GitHub Issue #118)

**Current Gap:** 0.95 - 0.78 = **0.17** (significant)

**Post-Mitigation Gap:** 0.95 - 0.92 = **0.03** (within threshold margin)

---

## Execution Statistics

- **Total Findings:** 6
- **Critical:** 1
- **Major:** 4
- **Minor:** 1
- **Protocol Steps Completed:** 6 of 6

---

## References

| Source | Content |
|--------|---------|
| BUG-017-006.md | Original bug entity defining the symlink resolution failure on macOS |
| eng-backend-implementation.md | Implementation artifact with code changes and verification results |
| verify-symlinks.sh | Final implementation of `realpath_portable()` function |
| S-004 Template | Pre-Mortem Analysis execution protocol |
| quality-enforcement.md | S-014 scoring dimensions and C3 criticality requirements |

---

*Pre-Mortem Analysis by adv-executor agent (S-004)*
*Date: 2026-02-26*
*Execution ID: 20260226T1500*
*Quality Threshold Target: >= 0.95 (C3 engagement)*
