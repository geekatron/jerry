# FMEA Report: PROJ-031 CoWork Skeleton — Phase 1 Regeneration and CI Design

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverables:** `requirements/phase1-requirements.md`, `decisions/ADR-001-skeleton-derived-branch-strategy.md`, `decisions/ADR-002-ci-token-push-strategy.md`
**Criticality:** C4
**Date:** 2026-06-26
**Reviewer:** adv-executor (Group E — Decompose) — blind independent
**H-16 Compliance:** Prior strategies (S-003, S-007, S-002, S-004, S-011, S-001) confirmed in `iteration-001/` before this execution
**Elements Analyzed:** 10 | **Failure Modes Identified:** 20 | **Total RPN:** 3,207

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Element Inventory](#element-inventory) | Decomposition of the regeneration + CI design |
| [Findings Table](#findings-table) | All 20 failure modes ranked by RPN |
| [Finding Details — Critical](#finding-details--critical) | Expanded analysis for all 6 Critical findings |
| [Finding Details — Major](#finding-details--major) | Expanded analysis for all 12 Major findings |
| [Finding Details — Minor](#finding-details--minor) | Summary for 2 Minor findings |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Summary counts |

---

## Element Inventory

| ID | Element | Description |
|----|---------|-------------|
| EL-01 | CI Trigger and Activation | `push: tags: v*` and `workflow_dispatch` event handling; observability of workflow firing |
| EL-02 | Source Tag Checkout | `fetch-depth` choice, git configuration, tag type (annotated vs. lightweight), race with advancing `main` |
| EL-03 | `projects/` Stripping Logic | `git rm -r projects/` command; special git objects; residual file coverage |
| EL-04 | Stub Injection | `projects/README.md` sentinel creation; static content constraint |
| EL-05 | Deterministic Commit Construction | `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` pinning; commit message template; parent SHA; GPG signature absence |
| EL-06 | Force-Push Execution | `GITHUB_TOKEN` scope declaration; permissions block configuration; branch posture |
| EL-07 | Post-Push Verification | File-count assertion ordering; directory existence checks; symlink target validation; `plugin.json` paths |
| EL-08 | Loop-Safety and Concurrency | Concurrency group configuration; `cancel-in-progress: false` serialization behavior; workflow-dispatch + tag-push interaction |
| EL-09 | Supply-Chain Integrity | SHA-pinned actions policy; equivalence verification between skeleton and source tag; update cadence |
| EL-10 | R-001 Assumption Verification | Empirical verification gate before Phase 5; file-count limit applicability to clean-clone vs. local working tree |

---

## Findings Table

Sorted by RPN descending. Execution ID suffix: `262626E`.

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|--------------------|
| FM-019-262626E | EL-10 | No automated gate prevents Phase 5 from starting before R-001 empirically verified; process relies on human compliance with AG-01 | 10 | 5 | 6 | 300 | Critical | Methodological Rigor |
| FM-002-262626E | EL-01 | `workflow_dispatch` lacks a target-tag input parameter; manual recovery run targets HEAD or caller-specified ref, not the intended release tag | 7 | 6 | 7 | 294 | Critical | Completeness |
| FM-001-262626E | EL-01 | CI silently does not fire on `v*` tag push; no external monitoring exists to detect workflow non-activation (job-summary and `if:failure()` only run if the workflow fires) | 8 | 4 | 8 | 256 | Critical | Completeness |
| FM-009-262626E | EL-05 | `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` not pinned to source-commit date; git defaults to "now," making every re-run produce a different commit SHA | 7 | 5 | 7 | 245 | Critical | Methodological Rigor |
| FM-012-262626E | EL-06 | Org or repo branch ruleset applied to `cowork-skeleton` after initial deployment blocks `GITHUB_TOKEN` force-push; all future releases silently fail to update skeleton | 8 | 5 | 5 | 200 | Critical | Actionability |
| FM-020-262626E | EL-10 | R-001 assumption materializes: CoWork file-count limit applies to local working directory (including `.venv/` at 24,636 files) rather than clean-clone tree; branch-stripping yields no benefit | 10 | 4 | 5 | 200 | Critical | Evidence Quality |
| FM-018-262626E | EL-09 | SHA-pinned action update policy absent; stale pinned SHAs accumulate unpatched upstream vulnerabilities over releases without a defined review cadence | 5 | 6 | 6 | 180 | Major | Methodological Rigor |
| FM-008-262626E | EL-04 | Stub `projects/README.md` content includes a non-static generated value (timestamp, version string, run ID); tree is non-deterministic across runs | 6 | 4 | 7 | 168 | Major | Internal Consistency |
| FM-010-262626E | EL-05 | Commit message includes run-specific metadata (e.g., `$GITHUB_RUN_ID`, CI run URL); idempotency guarantee broken even when dates are pinned | 6 | 4 | 7 | 168 | Major | Internal Consistency |
| FM-014-262626E | EL-07 | REQ-009 symlink validation uses `readlink -f` to check path non-empty but does not verify the resolved target actually exists; broken symlinks pass validation | 7 | 4 | 6 | 168 | Major | Completeness |
| FM-017-262626E | EL-09 | REQ-022 supply-chain equivalence check (`git diff v{N}..cowork-skeleton -- ':!projects/'`) is manual-only; no automated CI step runs it post-push | 8 | 3 | 7 | 168 | Major | Evidence Quality |
| FM-006-262626E | EL-03 | `.claude-plugin/marketplace.json` (or equivalent top-level plugin manifest) is not in the REQ-005 seven-directory validation list and not covered by REQ-010 agent-path checks; silently absent if accidentally removed | 7 | 3 | 7 | 147 | Major | Completeness |
| FM-016-262626E | EL-08 | `cancel-in-progress: false` serializes queued runs but does not guarantee they target the same release tag; a `workflow_dispatch` queued behind a tag-triggered run executes against its own (potentially different) target ref | 5 | 4 | 6 | 120 | Major | Internal Consistency |
| FM-003-262626E | EL-02 | Full-history fetch (`fetch-depth: 0`, required for Option A provenance) on a slow network risks hitting CoWork's 120-second git-operation timeout during clone phase | 7 | 4 | 4 | 112 | Major | Methodological Rigor |
| FM-013-262626E | EL-07 | Requirements do not specify that the file-count assertion (REQ-006) must execute BEFORE the force-push; if ordered after, an over-limit skeleton is already published before detection | 7 | 4 | 4 | 112 | Major | Completeness |
| FM-007-262626E | EL-04 | Stub injection step fails or is skipped; `projects/README.md` absent from skeleton; fresh `jerry projects list` call raises uncaught `RepositoryError` | 8 | 3 | 4 | 96 | Major | Completeness |
| FM-015-262626E | EL-08 | Concurrency group name misconfigured (typo or different value in nested job); concurrent runs race on the force-push target, producing non-deterministic branch state | 6 | 3 | 5 | 90 | Major | Internal Consistency |
| FM-004-262626E | EL-02 | Lightweight tag re-pushed to a different commit before CI executes; skeleton built from wrong source commit SHA | 8 | 2 | 5 | 80 | Major | Methodological Rigor |
| FM-011-262626E | EL-06 | `permissions: contents: write` block omitted from workflow YAML; org default is read-only; push fails (fails closed, visible, but blocks release pipeline) | 7 | 3 | 3 | 63 | Minor | Completeness |
| FM-005-262626E | EL-03 | `git rm -r projects/` skips nested git special objects (submodule gitlinks or nested `.git/` directories); extra files linger in skeleton | 4 | 2 | 5 | 40 | Minor | Completeness |

---

## Finding Details — Critical

### FM-019-262626E: No Automated Gate for R-001 Verification Before Phase 5

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | EL-10 — R-001 Assumption Verification |
| **RPN** | 300 (S:10, O:5, D:6) |
| **Affected Dimension** | Methodological Rigor |
| **Strategy Step** | Step 3 + Step 4 (Severity/Occurrence/Detection rating + Corrective Action) |

**Evidence:**

`phase1-requirements.md` §Stated Assumption R-001 states: "This MUST be empirically verified before Phase 5 (skeleton script implementation) begins." The verification approach requires: "(a) attempt to install from the current `main` branch on a clean machine and confirm the CoWork limit error reproduces; (b) install from a branch with `projects/` stripped and confirm the error is resolved." However, the AG-01 approval gate (defined in the requirements summary) covers requirements approval — not an explicit R-001 verification artifact. REQ-033 requires user approval of "AG-01 through AG-10" before irreversible actions, but the approval gate itself could be granted without confirming that R-001 verification was performed and documented.

**Analysis:**

Severity 10: If the strategy is executed through Phase 5 without R-001 verification, and R-001's assumption proves wrong, the entire branch-stripping approach may be moot and implementation effort is wasted on an ineffective solution. Occurrence 5: Human process steps are frequently deferred under schedule pressure; the requirements state R-001 must be verified but provide no machine-enforced blocker. Detection 6: Discovery would occur during Phase 5 implementation or end-to-end testing, not before.

**Corrective Action:**

Add a separate tracked artifact (e.g., `requirements/r-001-verification-log.md`) whose existence and sign-off is an explicit prerequisite for AG-01. The orchestrator must check for this artifact before progressing. Alternatively, create a new approval gate AG-00 specifically covering R-001 empirical verification, positioned before AG-01 in the gate sequence. The verification log must record: machine type, clean-clone file count on current `main`, clean-clone file count on a stripped branch, and pass/fail conclusion.

**Post-Correction RPN estimate:** S:10, O:2, D:3 → RPN: 60 (gate enforces verification with artifact evidence)

---

### FM-002-262626E: `workflow_dispatch` Lacks Target-Tag Input Parameter

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | EL-01 — CI Trigger and Activation |
| **RPN** | 294 (S:7, O:6, D:7) |
| **Affected Dimension** | Completeness |
| **Strategy Step** | Step 2 (Missing failure mode lens) |

**Evidence:**

REQ-011 declares triggers as `push: tags: ['v*']` and `workflow_dispatch`. REQ-018 states: "executing `workflow_dispatch` for a previously processed `v*` tag SHALL produce an identical `cowork-skeleton` branch state to the initial execution for that tag." REQ-007 states: "The CI workflow SHALL build the `cowork-skeleton` branch from the specific `v*` tag commit that triggered the workflow." However, `workflow_dispatch` has no inherent mechanism to communicate "which tag commit triggered the workflow" — `GITHUB_REF` for a `workflow_dispatch` call reflects the branch or tag the dispatch was invoked on, not automatically the latest release tag. None of REQ-011, REQ-018, or ADR-001 define a `workflow_dispatch` input parameter for specifying the target tag, nor specify what the script uses as `<source_tag>` when dispatched manually.

**Analysis:**

Severity 7: A `workflow_dispatch` run that builds from the wrong source commit produces a skeleton with incorrect provenance, potentially including newer unreleased changes. Occurrence 6: Every manual recovery invocation (the stated purpose of `workflow_dispatch`) faces this ambiguity — it is a systematic gap, not an edge case. Detection 7: The skeleton tip tree may look correct; the embedded SHA in the commit message is the only way to verify it was built from the right source.

**Corrective Action:**

Add a `workflow_dispatch` inputs block to `cowork-skeleton.yml`:
```yaml
on:
  workflow_dispatch:
    inputs:
      target_tag:
        description: 'The v* release tag to regenerate from (e.g., v0.31.5)'
        required: true
        type: string
```
The generation script uses `${{ github.ref }}` when triggered by a tag push and `${{ inputs.target_tag }}` when triggered by `workflow_dispatch`. Update REQ-018 acceptance criterion to test `workflow_dispatch` with an explicit named tag input. Update REQ-011 and ADR-001 §Context to document this design.

**Post-Correction RPN estimate:** S:7, O:2, D:4 → RPN: 56

---

### FM-001-262626E: CI Silently Not Firing on `v*` Tag — No External Detection

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | EL-01 — CI Trigger and Activation |
| **RPN** | 256 (S:8, O:4, D:8) |
| **Affected Dimension** | Completeness |
| **Strategy Step** | Step 2 (Missing failure mode lens) |

**Evidence:**

REQ-016 requires a `$GITHUB_STEP_SUMMARY` step with `if: always()` and a failure notification step with `if: failure()`. ADR-002 §Branch-Protection Posture states: "surface failures inside the workflow — a `$GITHUB_STEP_SUMMARY` job summary with `if: always()`." Both mechanisms only activate when the workflow itself fires. If the workflow is never triggered (GitHub Actions quota exhaustion, workflow syntax error, tag naming mismatch, GitHub outage), neither the summary nor the failure notification executes. No requirement defines an external health-check or monitoring mechanism to detect when `cowork-skeleton.yml` fails to fire after a release.

**Analysis:**

Severity 8: A silently unfired workflow leaves `cowork-skeleton` stale; users who install the plugin after a release get the previous version without warning. Occurrence 4: GitHub outages, Actions quota limits, and configuration errors are real but infrequent. Detection 8: There is no proactive alert; discovery occurs only when users report stale installs or when a maintainer manually inspects the Actions tab.

**Corrective Action:**

Add a scheduled job (e.g., `cron: '0 8 * * 1'`) or a `workflow_run` trigger on `release.yml` completion that verifies the latest `v*` tag SHA matches the source SHA embedded in the current `cowork-skeleton` commit message. If divergent, emit a failure notification (Slack webhook or GitHub issue creation). Alternatively, document in the post-release maintenance runbook a required manual check: "After each release, confirm `cowork-skeleton.yml` completed in GitHub Actions."

**Post-Correction RPN estimate:** S:8, O:4, D:3 → RPN: 96 (external monitoring reduces detection difficulty)

---

### FM-009-262626E: `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` Not Pinned — Idempotency Broken

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | EL-05 — Deterministic Commit Construction |
| **RPN** | 245 (S:7, O:5, D:7) |
| **Affected Dimension** | Methodological Rigor |
| **Strategy Step** | Step 2 (Incorrect failure mode lens) |

**Evidence:**

ADR-001 §Regeneration Commit Determinism explicitly lists `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` pinned to "the source commit's committer date, set via `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE`." The idempotency proof is sound. However, this constraint is expressed in the ADR (an architecture decision) rather than in a requirement with an acceptance criterion. REQ-003 states "the skeleton generation script SHALL produce a bit-identical `cowork-skeleton` commit SHA on every execution" but REQ-003's acceptance criterion says only "Script executed twice against the same tag SHA; `git rev-parse cowork-skeleton` returns an identical 40-character SHA" — it does not specify the mechanism (date pinning) that must be implemented, nor does any requirement enumerate what environment variables the script must set. A developer implementing the script who reads requirements but not the ADR could omit the date pinning.

**Analysis:**

Severity 7: Un-pinned dates break NFR-001 (determinism), NFR-002 (idempotency), and the tamper-detection property of the supply-chain narrative. Occurrence 5: Default git behavior stamps "now" — omitting the pin is the default path, not an exception. Detection 7: Idempotency failure is only detectable by running the workflow twice for the same tag and comparing commit SHAs, which is not part of any automated CI gate.

**Corrective Action:**

Add to REQ-003 acceptance criteria: "The script sets `GIT_AUTHOR_DATE=$(git log -1 --format='%aD' <source_sha>)` and `GIT_COMMITTER_DATE=$(git log -1 --format='%cD' <source_sha>)` before executing `git commit`." Add a separate integration-test CI step (e.g., run the generation script twice in the same workflow against the same tag) that asserts SHA equality — this makes the idempotency guarantee directly verifiable in CI. Reference the ADR-001 idempotency proof explicitly from REQ-003.

**Post-Correction RPN estimate:** S:7, O:1, D:5 → RPN: 35

---

### FM-012-262626E: Org/Repo Branch Ruleset Applied to `cowork-skeleton` — CI Push Blocked

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | EL-06 — Force-Push Execution |
| **RPN** | 200 (S:8, O:5, D:5) |
| **Affected Dimension** | Actionability |
| **Strategy Step** | Step 2 (Incorrect/future-state failure mode) |

**Evidence:**

ADR-002 §Consequences (Negative) acknowledges: "Cannot force-push a *protected* `cowork-skeleton` — if org policy later mandates protection, `GITHUB_TOKEN` fails without a ruleset bypass actor." REQ-021 requires the branch to be "unprotected" but a requirement on the *project* cannot prevent an org admin from applying a repository or organization ruleset independently. ADR-002 §Branch-Protection Posture documents upgrade paths (Actions actor bypass, GitHub App token) but no runtime detection or alerting exists to identify when this protection policy changes.

**Analysis:**

Severity 8: Every release after the policy change would silently fail to update `cowork-skeleton`; skeleton becomes permanently stale. Occurrence 5: Org governance changes are routine in growing organizations; branch protection mandates are common security controls. Detection 5: The push step in `cowork-skeleton.yml` returns a non-zero exit code and CI fails, but the failure message ("protected branch") may not obviously point to the documented upgrade paths.

**Corrective Action:**

Add a pre-push diagnostic step to `cowork-skeleton.yml` that runs `gh api repos/{owner}/{repo}/branches/cowork-skeleton/protection --silent` and on 200 HTTP response (protection exists) emits: "CRITICAL: cowork-skeleton branch is now protected. Force-push blocked. See ADR-002 §Branch-Protection Posture for upgrade paths." Fail the job with an actionable error message. Additionally, add this scenario to the post-Phase-6 monitoring runbook.

**Post-Correction RPN estimate:** S:8, O:5, D:2 → RPN: 80 (detection drops from 5 to 2 with diagnostic step)

---

### FM-020-262626E: R-001 Assumption Materializes — Branch-Stripping Ineffective

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | EL-10 — R-001 Assumption Verification |
| **RPN** | 200 (S:10, O:4, D:5) |
| **Affected Dimension** | Evidence Quality |
| **Strategy Step** | Step 3 (Severity/Occurrence/Detection rating) |

**Evidence:**

`phase1-requirements.md` §Stated Assumption R-001 explicitly documents: "The CoWork plugin-load file-count limit is approximately 5,000 files, and that limit applies to the tracked file count of a clean-clone working tree of the branch — not to a local developer working directory." The fallback states: "Hypothesis (b) confirmed (local working-directory count): strategy pivots from branch-stripping to local-plugin configuration guidance; scope change escalated to user per H-02." ADR-001 §L2 ¶4 confirms: "Anthropic's public plugin docs document **no** file-count limit; the ~5,000 ceiling is a CoWork/Claude-Desktop runtime constraint... OQ-1/R-001."

**Analysis:**

Severity 10: If the limit measures a local working directory (`.venv/` alone adds 24,636 files), the `cowork-skeleton` branch at 1,744 files provides no installation advantage — the strategy must pivot entirely. Occurrence 4: The assumption is reasonable based on first-principles (CoWork clones the branch), but it has not been empirically confirmed. Detection 5: Would be discovered during Phase 5 acceptance testing if the acceptance criterion (REQ-001) is tested on a clean machine; could be missed if testing occurs on a dev machine with `.venv/` present.

**Corrective Action:**

Same root corrective action as FM-019: enforce R-001 verification before Phase 5 begins via a tracked artifact. The test must explicitly compare: (a) file count on a clean-clone working tree (no `.venv/`, no `__pycache__`), and (b) file count in a developer working directory with `.venv/` expanded. Both results must be documented. The CoWork installation must be attempted from both a stripped and unstripped branch on a clean machine to confirm error reproduction and resolution.

**Post-Correction RPN estimate:** After verification — if hypothesis holds: S:0 (resolved). If hypothesis fails: triggers scope pivot per R-001 fallback; RPN becomes N/A (pivot, not a quality failure of this deliverable).

---

## Finding Details — Major

### FM-018-262626E: SHA-Pinned Action Update Policy Absent

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-09 — Supply-Chain Integrity |
| **RPN** | 180 (S:5, O:6, D:6) |
| **Affected Dimension** | Methodological Rigor |

**Evidence:** REQ-017 requires all actions be SHA-pinned. ADR-002 does not define a cadence for re-pinning when upstream Actions release security patches. SHA-pinning prevents tag hijacking but creates a maintenance gap: stale pins mean known CVEs in Action dependencies go unpatched indefinitely.

**Corrective Action:** Add a Dependabot configuration for `.github/workflows/cowork-skeleton.yml` (`ecosystem: github-actions`) in `.github/dependabot.yml`. Alternatively, document a quarterly SHA-pin review in the maintenance runbook. **Post-correction RPN:** S:5, O:2, D:4 → 40.

---

### FM-008-262626E: Stub Content Contains Non-Static Generated Value

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-04 — Stub Injection |
| **RPN** | 168 (S:6, O:4, D:7) |
| **Affected Dimension** | Internal Consistency |

**Evidence:** ADR-001 §Determinism Constraint: "the stub `projects/README.md` MUST be static content. Any generated date, version string, or run ID inside it changes the tree and breaks reproducibility. Authoring is STORY-002." The constraint exists in the ADR but no requirement acceptance criterion verifies stub content is static.

**Corrective Action:** Add to REQ-003 (or a new REQ): "The stub `projects/README.md` MUST NOT contain `${{`, `$(date`, or any CI variable interpolation. The generation CI must verify this with `grep -E '\$\{|\\$\(' projects/README.md` returning empty." **Post-correction RPN:** S:6, O:1, D:5 → 30.

---

### FM-010-262626E: Commit Message Contains Run-Specific Metadata

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-05 — Deterministic Commit Construction |
| **RPN** | 168 (S:6, O:4, D:7) |
| **Affected Dimension** | Internal Consistency |

**Evidence:** ADR-001 §Deterministic Commit provides the commit message template with explicit note: "with **no** build timestamp or run ID." The natural developer impulse to add a CI run URL for traceability (e.g., `Run: https://github.com/…/actions/runs/${{ github.run_id }}`) would break idempotency. No requirement acceptance criterion audits the commit message for run-specific content.

**Corrective Action:** Add to REQ-008 acceptance criterion: "`git log -1 --format='%B' cowork-skeleton` contains exactly the Source-Tag, Source-Commit, and Generated-By fields and no other variable content; verified by regex `^build\(cowork-skeleton\): regenerate from v[0-9].* [0-9a-f]{40}`." **Post-correction RPN:** S:6, O:1, D:4 → 24.

---

### FM-014-262626E: Symlink Validation Does Not Verify Target Resolution

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-07 — Post-Push Verification |
| **RPN** | 168 (S:7, O:4, D:6) |
| **Affected Dimension** | Completeness |

**Evidence:** REQ-009 acceptance criterion: "`readlink -f .claude/rules` and `readlink -f .claude/patterns` both resolve to non-empty, existing paths." `readlink -f` on a dangling symlink returns the computed path even if the target does not exist; it does not fail. Git also tracks broken symlinks without error. A stripped branch that inadvertently removes `.context/rules/` would leave `.claude/rules` as a dangling symlink that passes `readlink -f` validation.

**Corrective Action:** Change REQ-009 acceptance criterion to: "`test -d $(readlink -f .claude/rules) && test -d $(readlink -f .claude/patterns)` returns exit 0; otherwise CI fails." The generation script should include `ls -la "$(readlink -f .claude/rules)" > /dev/null` or equivalent. **Post-correction RPN:** S:7, O:1, D:2 → 14.

---

### FM-017-262626E: Supply-Chain Equivalence Check Is Manual-Only

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-09 — Supply-Chain Integrity |
| **RPN** | 168 (S:8, O:3, D:7) |
| **Affected Dimension** | Evidence Quality |

**Evidence:** REQ-022 acceptance criterion: "`git diff v{N}..cowork-skeleton -- ':!projects/'` returns zero changed files." This diff is defined as a manual verification step ("Verified by Analysis + Demonstration after each CI run"). No automated CI step in the workflow executes this diff as a post-push gate.

**Corrective Action:** Add a final job in `cowork-skeleton.yml` (with `needs: [regenerate]`) that runs `git fetch && git diff origin/cowork-skeleton...refs/tags/${GITHUB_REF_NAME} -- ':!projects/'` and asserts zero output. Failure emits "SUPPLY CHAIN VIOLATION: unexpected diff between skeleton and source tag." **Post-correction RPN:** S:8, O:3, D:2 → 48.

---

### FM-006-262626E: `marketplace.json` / Plugin Manifest Not in Post-Strip Validation

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-03 — `projects/` Stripping |
| **RPN** | 147 (S:7, O:3, D:7) |
| **Affected Dimension** | Completeness |

**Evidence:** REQ-005 validates seven directories: `.claude-plugin/`, `skills/`, `.claude/`, `.context/`, `src/`, `schemas/`, `hooks/`. REQ-010 validates agent-path entries declared inside `.claude-plugin/plugin.json`. Neither requirement explicitly verifies the existence of `.claude-plugin/marketplace.json` (the CoWork marketplace manifest file). If `marketplace.json` is absent, CoWork cannot recognize the plugin, producing a silent install failure.

**Corrective Action:** Add to REQ-005 (or a new REQ) a verification that `git ls-files .claude-plugin/marketplace.json` returns non-empty. The generation script's validation block should explicitly check for this file alongside the seven directories. **Post-correction RPN:** S:7, O:1, D:2 → 14.

---

### FM-016-262626E: Queued Serialized Run May Target Different Release Tag

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-08 — Loop-Safety and Concurrency |
| **RPN** | 120 (S:5, O:4, D:6) |
| **Affected Dimension** | Internal Consistency |

**Evidence:** REQ-015 requires `concurrency: group: cowork-skeleton, cancel-in-progress: false` to serialize overlapping runs. However, with `cancel-in-progress: false`, a queued `workflow_dispatch` run executes after the current run completes, using its own (potentially different) `inputs.target_tag` or `GITHUB_REF`. If a `workflow_dispatch` recovery for `v0.31.4` is queued while a tag-triggered run for `v0.31.5` is executing, the resulting `cowork-skeleton` will point to `v0.31.4` after the queued run completes — overwriting the correct `v0.31.5` skeleton.

**Corrective Action:** Document in REQ-015 and REQ-018 that the concurrency group does not prevent version-ordering conflicts between concurrent tag-triggered and `workflow_dispatch` runs. Add a guard: if `inputs.target_tag` (for workflow_dispatch) resolves to a commit SHA older than the current `cowork-skeleton` source SHA, the workflow should log a warning and skip the push. This is addressed partially by FM-002 corrective action. **Post-correction RPN:** S:5, O:2, D:4 → 40.

---

### FM-003-262626E: Full-History Clone Weight Risks 120-Second Git Timeout

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-02 — Source Tag Checkout |
| **RPN** | 112 (S:7, O:4, D:4) |
| **Affected Dimension** | Methodological Rigor |

**Evidence:** ADR-001 §Decision: "Default to `fetch-depth: 0` to keep Option A's provenance benefit; this is the deliberate clone-weight cost noted above." ADR-001 §Consequences (Negative): "Clone weight under full provenance — `fetch-depth: 0` carries `main`'s history into the skeleton `.git`; on slow networks this risks CoWork's 120-second git-operation timeout." REQ-027 documents the timeout and `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` variable in the how-to guide. No requirement specifies a clone-timing threshold or an alert for approaching the limit. The ADR mentions Option B as "escape hatch" but no trigger condition (timing threshold) is defined for switching.

**Corrective Action:** Add to `cowork-skeleton.yml` a clone-timing measurement step: record the elapsed time for `git fetch --depth=0` and emit a warning to `$GITHUB_STEP_SUMMARY` if elapsed time > 60 seconds (50% of the 120-second CoWork limit). Define in ADR-001 §L2 ¶2 a formal trigger: "if clone time consistently exceeds 90 seconds in CI, activate Option B (orphan branch)." **Post-correction RPN:** S:7, O:2, D:2 → 28.

---

### FM-013-262626E: File-Count Assertion May Run AFTER Force-Push

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-07 — Post-Push Verification |
| **RPN** | 112 (S:7, O:4, D:4) |
| **Affected Dimension** | Completeness |

**Evidence:** REQ-006: "The skeleton generation script SHALL assert that the tracked file count of the generated branch tree is less than 5,000 and SHALL exit with a non-zero exit code if this assertion is not satisfied." REQ-006 does not specify that this assertion must execute before the `git push --force` command. The acceptance criterion only tests the exit code, not the ordering relative to the push. An implementation that validates post-push would publish an over-limit skeleton before detecting the error.

**Corrective Action:** Add ordering specification to REQ-006: "The file-count assertion MUST be executed as a pre-push gate within the generation script, before any `git push --force` invocation." Update acceptance criterion: "Inject a synthetic file; confirm the script exits non-zero AND that `git log cowork-skeleton` shows no new commits (push never executed)." **Post-correction RPN:** S:7, O:1, D:2 → 14.

---

### FM-007-262626E: Stub Injection Step Fails or Is Skipped

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-04 — Stub Injection |
| **RPN** | 96 (S:8, O:3, D:4) |
| **Affected Dimension** | Completeness |

**Evidence:** REQ-004 requires `projects/README.md` sentinel in the generated skeleton. ADR-001 §Background confirms this is load-bearing for `jerry projects list` (cites `FilesystemProjectAdapter.scan_projects` lines 52–53). The generation script must create this file and `git add` it before committing. If the creation step is skipped or fails (e.g., filesystem permission error, incorrect path), `git commit` would include no `projects/` directory. No explicit verification step before the commit checks that the stub exists in the git index.

**Corrective Action:** Add an assertion in the generation script immediately after stub creation: `git ls-files projects/README.md | grep -q 'projects/README.md' || { echo "STUB INJECTION FAILED"; exit 1; }`. This ensures the stub is tracked in the index before the commit proceeds. **Post-correction RPN:** S:8, O:1, D:1 → 8.

---

### FM-015-262626E: Concurrency Group Misconfiguration — Concurrent Runs Race

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-08 — Loop-Safety and Concurrency |
| **RPN** | 90 (S:6, O:3, D:5) |
| **Affected Dimension** | Internal Consistency |

**Evidence:** REQ-015 acceptance criterion: "`concurrency:` block present in `cowork-skeleton.yml` with `cancel-in-progress: false`." The criterion verifies presence but not that the group name is correct and used consistently in all jobs in the workflow. If the workflow has multiple jobs with different concurrency group names, serialization fails.

**Corrective Action:** Use a YAML anchor for the concurrency group name (e.g., `x-concurrency: &concurrency-group cowork-skeleton`) or reference a workflow-level environment variable. Add to REQ-015 acceptance criterion: "If the workflow defines multiple jobs, all jobs share the same concurrency group or the concurrency is defined at the workflow level." **Post-correction RPN:** S:6, O:1, D:3 → 18.

---

### FM-004-262626E: Lightweight Tag Re-Pushed to Different Commit

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | EL-02 — Source Tag Checkout |
| **RPN** | 80 (S:8, O:2, D:5) |
| **Affected Dimension** | Methodological Rigor |

**Evidence:** Neither the requirements nor the ADRs specify that `v*` tags must be annotated (immutable by convention) rather than lightweight (moveable). A lightweight tag can be deleted and re-pushed to a different commit. If this happens in the window between `workflow_dispatch` trigger and tag resolution in the script, the skeleton is built from the wrong commit.

**Corrective Action:** Add to REQ-007 or a new constraint: "All `v*` release tags MUST be annotated tags (type `tag` per `git cat-file -t`). The generation script MUST verify `git cat-file -t refs/tags/<tag>` returns `tag`, not `commit`; fail with exit 1 if lightweight." Lightweight tags are already unusual for versioned releases, so occurrence is low; the check adds clarity. **Post-correction RPN:** S:8, O:1, D:2 → 16.

---

## Finding Details — Minor

### FM-011-262626E: `permissions: contents: write` Block Omitted

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Element** | EL-06 — Force-Push Execution |
| **RPN** | 63 (S:7, O:3, D:3) |

**Evidence:** ADR-002 §Consequences (Negative): "Default `GITHUB_TOKEN` permission depends on repo/org settings — if the org default is read-only and the `permissions:` block is omitted, the push fails." REQ-020 requires the block. Fails closed (CI failure is visible); D:3 because the CI failure is immediately observable and the fix is a 1-line YAML addition. **Corrective Action:** REQ-020 is sufficient; ensure CI lint runs `grep 'contents: write' .github/workflows/cowork-skeleton.yml` in a YAML validation step. **Post-correction RPN:** S:7, O:1, D:2 → 14.

### FM-005-262626E: `git rm -r projects/` Skips Nested Git Special Objects

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Element** | EL-03 — `projects/` Stripping |
| **RPN** | 40 (S:4, O:2, D:5) |

**Evidence:** If any path under `projects/` is a git submodule (tracked as a gitlink), `git rm -r projects/` removes the gitlink entry but may leave `.git/modules/` references. In practice, Jerry's `projects/` contains no submodules today. The file-count assertion (REQ-006) and the expected ~1,744 file-count guard would catch inflation caused by this failure. **Corrective Action:** The file-count assertion in REQ-006 provides adequate compensation. No additional requirement change required. **Post-correction RPN:** S:4, O:1, D:4 → 16.

---

## Recommendations

### Critical — Mandatory Before Phase 5

| Priority | ID | Corrective Action | Est. RPN Reduction | Affected REQ/ADR |
|----------|----|-------------------|--------------------|-----------------|
| 1 | FM-019 | Add tracked `r-001-verification-log.md` artifact as a prerequisite for AG-01 sign-off | 300 → 60 (−240) | Orchestration plan + REQ-033 |
| 2 | FM-002 | Add `target_tag` input parameter to `workflow_dispatch` trigger; update REQ-018 acceptance criterion | 294 → 56 (−238) | REQ-011, REQ-018 |
| 3 | FM-001 | Add external monitoring (scheduled check or `workflow_run` trigger) comparing latest `v*` tag to skeleton commit message | 256 → 96 (−160) | REQ-016 |
| 4 | FM-009 | Add explicit `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` pinning requirement in REQ-003 acceptance criterion; add idempotency integration test in CI | 245 → 35 (−210) | REQ-003, ADR-001 |
| 5 | FM-012 | Add pre-push branch-protection diagnostic step to `cowork-skeleton.yml` emitting actionable error when protection exists | 200 → 80 (−120) | REQ-021, ADR-002 |
| 6 | FM-020 | Execute R-001 empirical verification and document result in `r-001-verification-log.md` before Phase 5 | 200 → 0 or pivot (−200) | R-001, REQ-001 |

**Total Critical RPN reduction if all corrective actions applied:** 1,495 → 327 (−1,168, 78% reduction)

### Major — Required Before Implementation Sign-Off

| Priority | ID | Corrective Action | Est. RPN Reduction |
|----------|----|-------------------|--------------------|
| 7 | FM-017 | Add automated post-push `git diff` equivalence check to `cowork-skeleton.yml` | 168 → 48 (−120) |
| 8 | FM-014 | Change REQ-009 acceptance criterion to `test -d $(readlink -f .claude/rules)` (target existence, not path string) | 168 → 14 (−154) |
| 9 | FM-006 | Add `marketplace.json` existence check to post-strip validation (REQ-005 extension) | 147 → 14 (−133) |
| 10 | FM-013 | Specify in REQ-006 that file-count assertion must precede force-push; update acceptance criterion to verify ordering | 112 → 14 (−98) |
| 11 | FM-018 | Add Dependabot config for `github-actions` ecosystem on `cowork-skeleton.yml` | 180 → 40 (−140) |
| 12 | FM-008 | Add stub static-content lint check to REQ-003; enforce no interpolation variables in `projects/README.md` | 168 → 30 (−138) |
| 13 | FM-010 | Add commit message regex acceptance criterion to REQ-008; prohibit `$GITHUB_RUN_ID` and run URLs | 168 → 24 (−144) |
| 14 | FM-003 | Add clone-timing measurement step; define Option B activation threshold (> 90 seconds) in ADR-001 | 112 → 28 (−84) |
| 15 | FM-007 | Add post-stub-creation git-index assertion in generation script | 96 → 8 (−88) |
| 16 | FM-016 | Document version-ordering risk; add version-guard logic in script (skip push if target older than current skeleton) | 120 → 40 (−80) |
| 17 | FM-015 | Use YAML anchor for concurrency group; update REQ-015 criterion to cover multi-job workflows | 90 → 18 (−72) |
| 18 | FM-004 | Add annotated-tag verification step to generation script; update REQ-007 | 80 → 16 (−64) |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| **Completeness** | 0.20 | Negative | FM-001 (no external workflow activation monitoring), FM-002 (workflow_dispatch design gap), FM-006 (marketplace.json not in validation), FM-007 (stub injection unverified), FM-013 (assertion ordering unspecified), FM-014 (symlink depth insufficient) — 6 findings point to missing design elements |
| **Internal Consistency** | 0.20 | Negative — Moderate | FM-008 and FM-010 (commit determinism constraints in ADR not reflected in requirements acceptance criteria); FM-015 and FM-016 (concurrency guard behavior partially analyzed but not fully specified across workflow scenarios) |
| **Methodological Rigor** | 0.20 | Negative — Moderate | FM-009 (date-pinning mechanism required by ADR but not enforced by any requirement acceptance criterion); FM-003 (Option B trigger threshold undefined); FM-004 (tag-type requirement absent); FM-018 (SHA-pin update cadence undefined); FM-019 (R-001 verification not gate-enforced) |
| **Evidence Quality** | 0.15 | Negative — Moderate | FM-017 (supply-chain equivalence manual-only, not automated); FM-020 (R-001 central assumption empirically unverified) |
| **Actionability** | 0.15 | Negative — Moderate | FM-012 (branch-protection drift has no runtime detection, only a documented upgrade path); FM-019 (R-001 gate relies entirely on human process) |
| **Traceability** | 0.10 | Negative — Minor | FM-002 and FM-006 represent design elements with no traceability from stakeholder needs to requirement — small gaps in an otherwise thorough traceability chain |

**Overall Assessment: REVISE.** The deliverable demonstrates rigorous systems engineering work with thorough ADR analysis, strong traceability, and a well-structured requirements set. Six Critical findings (total RPN 1,495) represent systemic risk concentration in workflow activation monitoring (EL-01), manual-recovery design (EL-01), commit determinism enforcement (EL-05), branch-protection drift (EL-06), and assumption verification gating (EL-10). The top two Critical findings (FM-019 and FM-002) are addressable through targeted requirements additions and do not require architectural rethinking. Corrective actions for all 6 Critical findings should be incorporated before AG-01 sign-off. The 12 Major findings strengthen implementation robustness when addressed during Phase 5/6 implementation design.

---

## Execution Statistics

| Metric | Value |
|--------|-------|
| **Total Findings** | 20 |
| **Critical** | 6 |
| **Major** | 12 |
| **Minor** | 2 |
| **Protocol Steps Completed** | 5 of 5 |
| **Elements Analyzed** | 10 |
| **Total RPN** | 3,207 |
| **Critical RPN Sum** | 1,495 |
| **Major RPN Sum** | 1,609 |
| **Minor RPN Sum** | 103 |
| **Highest-RPN Element** | EL-01 CI Trigger and Activation (550) |
| **Highest-RPN Finding** | FM-019-262626E (300) |
| **Strategy Template** | `.context/templates/adversarial/s-012-fmea.md` v1.0.0 |
| **Reviewer** | adv-executor (Group E — Decompose, blind independent) |

---

*H-15 Self-Review applied before persistence: all 20 findings have specific deliverable evidence; S/O/D ratings are justified and cross-calibrated; FM-NNN-262626E identifiers used consistently; summary table RPN column verified by S×O×D calculation; no findings omitted or severity minimized (P-022).*

*Generated: 2026-06-26 | PROJ-031-cowork-skeleton | cowork-skeleton-20260626-001 | QG-1 Phase 1*
