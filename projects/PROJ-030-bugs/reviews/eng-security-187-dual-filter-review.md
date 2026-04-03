# Security Review: version-bump.yml Dual Filters (#187)

> Manual security code review of the dual-filter changes to `.github/workflows/version-bump.yml`.
> Reviewer: eng-security
> Date: 2026-03-11
> Scope: Dual filtering introduced by #187 — paths-ignore trigger filter (lines 20-49) and
>        commit-message prefix job-level if: condition (lines 109-135).

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Finding counts and immediate actions |
| [L1: Findings](#l1-findings) | Individual finding reports with evidence |
| [L2: Strategic Implications](#l2-strategic-implications) | Systemic patterns and posture assessment |
| [ASVS Verification](#asvs-verification) | Relevant ASVS chapters |

---

## L0: Executive Summary

**Overall security assessment: PASS with observations**

The dual-filter design is sound. No finding in this review represents a exploitable condition that can cause an unintended version bump or a meaningful denial-of-service against the release pipeline in a realistic threat model. The design correctly preserves manual-trigger freedom while reducing CI noise.

### Finding Counts

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 2 |
| Info | 3 |

### Top 3 Risk Areas

1. **workflow_dispatch access control** — Any user with `write` access to the repository can trigger a manual bump at any time. This is an accepted GitHub platform constraint but warrants explicit documentation.
2. **Commit message denylist completeness** — The current Filter B denylist matches known non-bump prefixes but does not cover all Conventional Commits specification types. A new prefix introduced in future without updating the denylist would run the version-bump workflow and detect "none", which is the correct safe-default behavior; this is a efficiency issue, not a security issue.
3. **`[skip ci]` bypass of both filters** — A push commit containing `[skip ci]` in its message bypasses GitHub's built-in skip mechanism at the workflow level, silencing version bumps silently. This is a pre-existing issue not introduced by #187, but the dual filters do not mitigate it.

### Recommended Immediate Actions

1. (INFO-002) Document in the workflow comment that `workflow_dispatch` requires write access, so the access model is visible to maintainers.
2. (LOW-001) Add a comment noting the `[skip ci]` bypass is a known accepted risk — it is already noted in the research doc but not surfaced in the workflow itself.
3. No code changes are required for correctness or security.

---

## L1: Findings

---

### FINDING-001 — workflow_dispatch Has No Access Restriction Beyond Repository Write

| Field | Value |
|-------|-------|
| Severity | Medium |
| CVSS 3.1 Vector | AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N |
| CVSS Score | 4.3 |
| CWE | CWE-306: Missing Authentication for Critical Function |
| Location | `version-bump.yml` lines 50-63 (`workflow_dispatch` trigger definition) |

**Description**

The `workflow_dispatch` trigger accepts any of `patch`, `minor`, or `major` as `bump_type` and an optional `prerelease` string. There is no explicit restriction on which repository actors can trigger this event. Access is gated entirely by GitHub's native repository `write` permission.

For a public or organization repository, anyone with write access — including organization members who have been granted broad write permission on automation repos — can trigger a major version bump, a prerelease, or an arbitrary bump type without any secondary approval step.

**Data Flow Trace**

```
github.com UI / API call → workflow_dispatch event
  → job condition: github.event_name == 'workflow_dispatch' → always passes
  → steps.bump: echo "type=${{ github.event.inputs.bump_type }}" → written to GITHUB_OUTPUT
  → Apply version bump step: bump-my-version bump "$BUMP_TYPE"
  → git push origin main --follow-tags
```

The `workflow_dispatch` branch of the `if:` condition (lines 111-112) unconditionally passes. It does not check `github.actor`, `github.event.sender.type`, or any allow-list. This is correct behavior by design but creates a low-friction path to an unreviewed version bump from any write-permissioned actor.

**Evidence**

```yaml
# Lines 109-112: workflow_dispatch always passes the job condition
if: >-
  (
    github.event_name == 'workflow_dispatch'
  ) ||
```

**Assessment**

This is a design characteristic, not a defect. GitHub's model is that `write` access is the authorization boundary. However, for a release pipeline that publishes signed artifacts and tags that trigger downstream automation (`release.yml`), a rogue or compromised write-access account can publish a version bump that misleads downstream consumers about the content of a release.

**Severity Rationale**

Scored Medium (4.3) rather than High because: (a) the attacker must already have repository write access (a significant prerequisite), (b) the resulting version bump does not execute arbitrary code on user machines — it only creates a tag and updates version numbers in source files, (c) the release pipeline runs `validate version sync` and CI checks that would fail if the codebase is genuinely broken. The primary impact is confusion and potential supply-chain noise, not code execution.

**Remediation Options**

Option A (no-change, document): Add a comment to the workflow documenting that `workflow_dispatch` is gated by repository write permission. Ensures maintainers make an informed decision.

Option B (environment protection): Configure a GitHub Environment named `production-release` with required reviewers, and set `environment: production-release` on the `bump` job. This forces a manual approval step before `workflow_dispatch` bumps execute. This has the side-effect of requiring approval for bot-triggered bumps from push events as well unless the environment is scoped to `workflow_dispatch` only.

Option C (actor allowlist): Add `github.actor == 'octocat' || github.actor == 'dependabot[bot]'` style allowlist. Fragile to team membership changes.

**Recommended:** Option A for now. Option B if this repository ever has external contributors with write access.

---

### FINDING-002 — `[skip ci]` in Any Merged Commit Silently Suppresses Version Bump

| Field | Value |
|-------|-------|
| Severity | Low |
| CVSS 3.1 Vector | AV:N/AC:H/PR:L/UI:R/S:U/C:N/I:N/A:L |
| CVSS Score | 2.6 |
| CWE | CWE-693: Protection Mechanism Failure |
| Location | `version-bump.yml` lines 12-49 (push trigger) |

**Description**

GitHub Actions evaluates a built-in keyword skip mechanism before path filters and before job-level `if:` conditions. If any push to `main` contains a commit message with `[skip ci]`, `[ci skip]`, `[no ci]`, `[skip actions]`, or `[actions skip]`, the entire workflow is silently bypassed. This includes squash-merged PRs whose squash commit body inherits individual commit messages containing these tokens.

Neither Filter A (paths-ignore) nor Filter B (commit prefix startsWith) mitigates this. Both filters are downstream of the built-in skip mechanism.

**Scenario**

A maintainer squash-merges a PR whose commit history contains one commit with message `fix: typo [skip ci]`. GitHub includes that individual commit message in the squash commit body. The `[skip ci]` token causes the workflow to never start. If that squash commit also bumped a version-relevant file with a `feat:` message, the version bump is missed.

The version bump is recoverable via `workflow_dispatch`, but the miss is silent — no CI failure, no notification.

**Evidence from research document** (`workflow-filtering-research.md`, section "Built-in Skip Mechanism"):
> "This applies to push and pull_request events only. This is evaluated BEFORE path filters and job-level if: conditions."

**Severity Rationale**

Low because: (a) this requires a commit message to contain the exact skip token, which is uncommon in normal development, (b) the impact is a missed automated bump, not incorrect behavior — the version does not get bumped when a human forgot to bump it, which is a recoverable state, (c) manual recovery via `workflow_dispatch` is always available.

**Remediation**

The safest mitigation is to configure the repository squash merge default message to "PR title only" under Settings > Pull Requests > Default commit message. This prevents individual commit messages from appearing in the squash commit body.

Additionally, add a comment in the workflow documenting this known bypass:

```yaml
# KNOWN LIMITATION: GitHub's built-in [skip ci] mechanism suppresses this workflow
# at the platform level, before path filters or job conditions are evaluated.
# If a push contains [skip ci], [ci skip], [no ci], [skip actions], or [actions skip]
# in any commit message (including squash commit bodies), the version bump will not run.
# Recovery: use workflow_dispatch to trigger a manual bump.
# Mitigation: configure repository squash merge default message to "PR title only".
```

---

### FINDING-003 — Filter B Denylist Is Correct but Has a Semantic Coverage Gap

| Field | Value |
|-------|-------|
| Severity | Low |
| CVSS 3.1 Vector | N/A — not exploitable, design observation |
| CVSS Score | N/A |
| CWE | N/A |
| Location | `version-bump.yml` lines 117-134 |

**Description**

Filter B denylists the following conventional commit prefixes: `ci:`, `ci(`, `deps:`, `deps(`, `docs:`, `docs(`, `chore:`, `chore(`, `style:`, `style(`, `refactor:`, `refactor(`, `test:`, `test(`, `build:`, `build(`, `revert:`, `revert(`.

The Conventional Commits specification also includes `perf:` as a type that can trigger a `fix`-level bump in some configurations. Jerry's bump detection (`uv run jerry ci detect-bump-type`) presumably handles `perf:` as a bump-worthy type. However, if `perf:` were ever added to the denylist in error, it would suppress a legitimate bump.

More substantively: the denylist is a denylist, not an allowlist. Any unrecognized prefix (e.g., a custom `infra:` type added by a future contributor) will pass through Filter B and run the `detect-bump-type` CLI, which will return `none`. This is the correct safe-default — the workflow runs, detects nothing to bump, and exits cleanly. No missed bump, no false bump.

**Why this is Low rather than Info**

The inverse failure mode is the concern: if a bump-worthy prefix (e.g., a future `security:` prefix treated as `fix:`-level by Jerry's CLI) were accidentally added to the denylist, legitimate bumps would be suppressed. This is a maintenance risk, not a current vulnerability.

**Evidence**

```yaml
# Lines 117-134: Filter B denylist
!startsWith(github.event.head_commit.message, 'ci:') &&
!startsWith(github.event.head_commit.message, 'ci(') &&
# ... 16 more prefix checks
!startsWith(github.event.head_commit.message, 'revert:') &&
!startsWith(github.event.head_commit.message, 'revert(')
```

Note: `perf:` and `perf(` are absent from the denylist, which is correct — `perf:` commits in Jerry's scheme may warrant a bump.

**Remediation**

Add a comment above the denylist documenting the maintenance rule:

```yaml
# Filter B: Skip known non-bump commit prefixes.
# MAINTENANCE RULE: Only add prefixes here that the detect-bump-type CLI
# treats as BumpType.NONE. Do NOT add prefixes that could be bump-worthy
# (feat:, fix:, perf:, or any prefix treated as fix-level by Jerry CLI).
# When in doubt, omit the prefix -- the CLI will return "none" safely.
```

---

### INFO-001 — `github.actor != 'github-actions[bot]'` Guard Is Correct After Filter Changes

| Field | Value |
|-------|-------|
| Severity | Info |
| Location | `version-bump.yml` line 116 |

**Description**

The guard `github.actor != 'github-actions[bot]'` prevents the version-bump workflow from re-triggering itself when the bot pushes the version bump commit back to main. This guard is placed in the non-`workflow_dispatch` branch of the `if:` condition (lines 113-135), which is correct.

After the dual-filter changes, the guard remains in the correct location and continues to function correctly. The paths-ignore filter (Filter A) would not catch the bot's push because the bot modifies `pyproject.toml`, `uv.lock`, and potentially other version files — none of which are in the paths-ignore list. Therefore, the actor guard is the load-bearing control that prevents the infinite loop, not Filter A.

**Verification**

The bot's commit message is set at line 224 as `git config user.name "github-actions[bot]"` and `bump-my-version` creates commits with this identity. The `github.actor` check correctly matches this actor.

**Conclusion:** No issue. The guard is still necessary, correctly placed, and correctly scoped to the non-`workflow_dispatch` branch.

---

### INFO-002 — `.github/**` in paths-ignore Means Workflow Changes Do Not Trigger Version Bump

| Field | Value |
|-------|-------|
| Severity | Info |
| Location | `version-bump.yml` line 49 |

**Description**

The paths-ignore list includes `.github/**` (line 49). This means a push that only modifies `.github/workflows/version-bump.yml` itself does not trigger the version-bump workflow. The comment on line 48 acknowledges this: "CI config (changes use ci: prefix, caught by Filter B)".

**Security Relevance**

An attacker with write access who wants to modify the version-bump workflow to introduce a malicious action (e.g., exfiltrating `secrets.VERSION_BUMP_PAT`) would push a change to `.github/workflows/version-bump.yml`. This change would not trigger the version-bump workflow. It would, however, trigger `ci.yml` (which runs on all branch pushes). The malicious version-bump workflow would only execute on the next push that does touch a non-.github file.

This means: a workflow modification and its first execution are in separate pushes. This creates a brief window where the malicious workflow exists in `main` but has not yet run.

**Is this a new issue introduced by #187?**

No. This is the standard GitHub Actions attack surface for any workflow with `contents: write` permission. It exists regardless of path filters. The `.github/**` exclusion does not make this worse; if it were absent, the version-bump workflow would simply run, detect "none" (no feat/fix commits), and exit cleanly.

**Conclusion:** Observation only. The `.github/**` exclusion is correct. It does not create or expand attack surface. Repository branch protection rules (requiring PR review before merge to main) are the correct mitigation for this class of concern.

---

### INFO-003 — Prerelease Shell Injection Validation Is Correct but Noted

| Field | Value |
|-------|-------|
| Severity | Info |
| Location | `version-bump.yml` lines 229-233 |

**Description**

The workflow correctly validates the `prerelease` input against `^[a-zA-Z0-9]+$` before using it in shell commands (lines 229-233). This mitigates CWE-78 shell injection via the free-form `workflow_dispatch` input.

The `bump_type` input is a restricted `choice` type (patch/minor/major), which GitHub enforces at the API level. No shell injection is possible via `bump_type`.

The `PRERELEASE` variable is used at lines 235-238 in a quoted context (`"$(... ${PRERELEASE}.1)"`) and the pattern check precedes its use. The validation is placed correctly — before the shell expansion.

**Conclusion:** No issue. Pre-existing fix (BUG-003/RISK-02) is correctly implemented and not regressed by the dual-filter changes.

---

## L2: Strategic Implications

### Security Posture Assessment

The dual-filter implementation is a CI efficiency improvement with no meaningful security regression. The workflow's security posture is unchanged from before #187. The three existing security controls remain intact:

1. **Actor guard** (`github.actor != 'github-actions[bot]'`) — prevents self-triggering loop.
2. **Prerelease input validation** (alphanumeric regex) — prevents shell injection via `workflow_dispatch`.
3. **clean working tree check** — fails loudly if the state before bump is unexpected, providing a supply-chain tripwire.

### Systemic Pattern: Defense-in-Depth Through Layering

The dual-filter design correctly applies defense-in-depth at two independent layers (trigger-level vs job-level) with different failure modes:

- **Filter A failure mode** (paths-ignore): If a non-relevant file is missing from the denylist, the workflow runs unnecessarily but safely (detect-bump-type returns "none"). Over-inclusion, not under-inclusion.
- **Filter B failure mode** (commit prefix denylist): If a non-bump prefix is missing from the denylist, the workflow runs unnecessarily but safely (same). If a bump-worthy prefix is wrongly added, bumps are missed. The risk is asymmetric in Filter B.

The current implementation correctly biases both filters toward over-triggering (safe default) rather than under-triggering (missed bump).

### Comparison with Threat Model Predictions

The research document (`workflow-filtering-research.md`) identified the `[skip ci]` bypass (FINDING-002) and the squash merge gotcha under "Risk Assessment". Both are correctly classified as medium-likelihood, medium-impact in the research. FINDING-002 aligns with this prior assessment.

FINDING-001 (workflow_dispatch access) was noted as a design characteristic in the research document's L2 section. The research correctly identified that version-bump is not a required check, which limits the blast radius of any filter manipulation.

### Recommendations for Security Architecture Evolution

1. If this repository introduces external contributors with write access, configure a GitHub Environment with required reviewers on the `bump` job for `workflow_dispatch` events. This is the only structural change that would meaningfully improve the security posture of this workflow.
2. The `VERSION_BUMP_PAT` secret scope should be audited periodically to confirm it has only the minimum required permissions (push to main + tag creation). This is out of scope for this review but relevant to the overall release pipeline threat model.
3. The lock-file integrity guard (lines 253-259) is a good supply-chain control. Consider failing hard (`exit 1`) instead of `::warning::` if the lock diff exceeds 2 lines, to make this an enforcement control rather than an advisory one. The current implementation emits a warning but continues.

---

## ASVS Verification

Relevant ASVS 5.0 chapters for a GitHub Actions release workflow:

| Chapter | Requirement | Status |
|---------|-------------|--------|
| V4 Access Control | V4.1.1: Authorization checks on all protected functions | PARTIAL — workflow_dispatch gated by GitHub write permission only; no environment protection |
| V4 Access Control | V4.2.1: Sensitive resources protected against IDOR | PASS — version files modified only by authenticated actor via PAT |
| V7 Error Handling | V7.1.1: Errors do not expose sensitive information | PASS — workflow outputs and summaries do not expose the PAT or secrets |
| V5 Validation | V5.2.3: Input validation on all user-supplied data | PASS — prerelease input validated against ^[a-zA-Z0-9]+$ before shell use |
| V9 Communication | V9.2.1: TLS for all external communications | PASS — all GitHub API calls over HTTPS by platform default |

---

*Review scope: `.github/workflows/version-bump.yml` lines 12-135 (dual filter changes)*
*CWE Top 25 2025 checks applied: CWE-78 (OS Command Injection), CWE-287 (Improper Authentication), CWE-306 (Missing Auth for Critical Function), CWE-693 (Protection Mechanism Failure)*
*Confidence: 0.90 — high confidence on all findings; INFO-002 threat scenario is theoretical and well-understood*
*Agent: eng-security*
*SSDF Practice: PW.7 (human-readable code review)*
