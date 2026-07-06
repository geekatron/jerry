# Pre-Mortem Report: PROJ-031 CoWork Skeleton Branch — Phase 1 Deliverables

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverables:**
- `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md`
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md`
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md`
**Criticality:** C4 (AE-003 auto-escalation on ADRs; AE-005 security-relevant CI)
**Date:** 2026-06-26
**Reviewer:** jerry:adv-executor (blind, independent)
**Execution ID:** 20260626
**H-16 Note:** S-004 is not subject to the H-16 S-002 pre-check. This is a standalone strategy execution.
**Failure Scenario:** It is 2026-12-26. The cowork-skeleton CI initiative has failed. The `cowork-skeleton` branch is stale or broken. Users attempting `claude plugin marketplace add geekatron/jerry@cowork-skeleton` either still hit the file-limit error OR install a branch that errors on boot. CI has been silently failing for multiple release cycles. Maintainers have abandoned maintenance because the system feels too fragile.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Failure Scenario Declaration](#failure-scenario-declaration) | Temporal perspective shift statement |
| [Findings Summary](#findings-summary) | All findings table with priority |
| [Detailed Findings](#detailed-findings) | PM-001 through PM-010 |
| [Recommendations](#recommendations) | P0 / P1 / P2 grouped mitigations |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Counts and protocol completion |

---

## Failure Scenario Declaration

It is 2026-12-26. We are analyzing why the cowork-skeleton initiative failed spectacularly. All causes below are stated as historical facts discovered in retrospect.

The cowork-skeleton branch entered production after Phase 5 implementation. Within six months, the following happened: the CI job silently began failing after a git action was updated and the SHA pin was stale; the `cowork-skeleton` branch fell two releases behind `main`; several users opened support requests because their plugin still hit the file-limit error (the R-001 assumption had never been empirically confirmed before implementation); one contributor pushed a hotfix directly to `cowork-skeleton` and lost their work on the next CI run; and maintainers, finding the system more brittle than expected, deprioritized fixes in favor of other work.

---

## Findings Summary

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260626 | R-001 assumption enters Phase 5 unverified — no technical enforcement gate | Assumption | Medium | Critical | P0 | Completeness |
| PM-002-20260626 | Silent CI failure leaves skeleton stale — failure notification is "Should" priority | Process | Medium | Major | P1 | Actionability |
| PM-003-20260626 | File count headroom erodes without proactive monitoring on `main` | Technical | Medium | Major | P1 | Completeness |
| PM-004-20260626 | Short-SHA in commit message template creates variable-length idempotency trap | Technical | Medium | Major | P1 | Internal Consistency |
| PM-005-20260626 | Force-push overwrites contributor commits silently — unprotected branch + docs-only mitigation | Process | Low | Major | P1 | Methodological Rigor |
| PM-006-20260626 | Symlink validation is Linux-CI-only — cross-platform install assumption unvalidated | Assumption | Low–Medium | Major | P1 | Evidence Quality |
| PM-007-20260626 | No automated Action SHA refresh — security patches accumulate undetected | Process | High | Major | P1 | Methodological Rigor |
| PM-008-20260626 | Stub static-content constraint not technically enforced — future idempotency risk | Process | Low | Minor | P2 | Traceability |
| PM-009-20260626 | CoWork clone timeout risk grows as repo history accumulates — no monitoring | Technical | Low–Medium | Minor | P2 | Actionability |
| PM-010-20260626 | GITHUB_TOKEN loop-safety guarantee depends on GitHub implementation behavior | External | Low | Minor | P2 | Methodological Rigor |

---

## Detailed Findings

### PM-001-20260626: R-001 Assumption Enters Phase 5 Unverified [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | Assumption |
| **Likelihood** | Medium |
| **Priority** | P0 |
| **Affected Dimension** | Completeness |
| **Deliverable Reference** | `phase1-requirements.md` §Stated Assumption R-001; ADR-001 §L2 ¶4 and Risks table row 1 |

**Failure Cause:** The cowork-skeleton strategy's core premise — that CoWork enforces its ~5,000-file limit against a clean-clone tracked-file count (not a local developer working directory that includes `.venv/` at 24,636 files) — is explicitly unverified. The requirements call this "the project's primary unresolved risk" and require empirical verification before Phase 5. But verification is enforced only through a human process gate (AG-01 user approval and STORY-003 completion). There is no technical artifact — no CI gate, no merge prerequisite, no script exit code — that blocks Phase 5 from starting if STORY-003 was never completed. Under timeline pressure or handoff confusion, Phase 5 implementation could proceed and produce a `cowork-skeleton` branch that solves a problem CoWork does not have in the way the design assumes. Users still encounter the file-limit error; the skeleton branch has zero effect.

**Evidence:** `phase1-requirements.md` §R-001: "Confirmed absent from Anthropic's Claude Code plugin documentation... still warrants empirical confirmation." ADR-001 §L2 ¶4: "The strategy's validity rests on an external, still-unverified assumption... this is honestly the top residual risk and is not resolved by this ADR."

**Prevention Gap:** The deliverables correctly identify the risk and define the verification approach, but the enforcement is purely process-based (AG-01 human sign-off). There is no CI job, script prerequisite, or blocking artifact (e.g., a `R001-VERIFIED.md` file that must exist in the branch before Phase 5 scripts can run) that would stop an automated or forgetful execution path from bypassing STORY-003.

**Mitigation:** Create a machine-checkable R-001 verification artifact: a `verification/R001-clean-clone-count.md` file that records the empirical clean-clone file count from STORY-003, plus a prerequisite check in the generation script that reads this file and exits non-zero if it is absent. Phase 5 CI cannot succeed without it.

**Acceptance Criteria:** The skeleton generation script contains a step that reads `verification/R001-clean-clone-count.md`, confirms the recorded clean-clone count is < 5,000, and exits non-zero if the file is absent or shows count >= 5,000. This artifact must exist before the Phase 5 workflow can complete successfully.

---

### PM-002-20260626: Silent CI Failure Leaves Skeleton Stale [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Process |
| **Likelihood** | Medium |
| **Priority** | P1 |
| **Affected Dimension** | Actionability |
| **Deliverable Reference** | `phase1-requirements.md` REQ-016 (WS-2 row 6): Priority column reads "Should" while the requirement body uses "SHALL" |

**Failure Cause:** REQ-016 is the only requirement governing failure visibility. It uses "SHALL" language (Must-tier) but is filed under Priority "Should" — creating an internal inconsistency that signals to implementers it may be optional. If the failure notification step is omitted during implementation (reasonable given the "Should" priority), CI failures are silent: the `cowork-skeleton` branch stalls at the last successful run with no observable signal. Furthermore, even a correctly implemented `$GITHUB_STEP_SUMMARY` and `if: failure()` notification step only fires when CI runs and fails — not when CI never runs at all (e.g., if the workflow file is accidentally deleted or the trigger misconfigured). There is no external health-check, status badge, or cron-based "is skeleton current?" probe in the design.

**Evidence:** `phase1-requirements.md` WS-2 table: REQ-016 Priority column = "Should". Acceptance criterion requires a "Demonstration on a test run that intentionally fails" — demonstrating that a failed run can be observed, but not that a non-running workflow is detectable.

**Prevention Gap:** Staleness detection requires a proactive probe (e.g., a daily cron job that compares the source tag embedded in `cowork-skeleton`'s last commit message against the latest `v*` tag). No such probe is specified.

**Mitigation:** (1) Correct the REQ-016 priority to "Must" to match its "SHALL" language. (2) Add a staleness-detection NFR: a status badge on `cowork-skeleton` (or in the repo README/docs) that shows whether the branch matches the latest `v*` tag. (3) Add a lightweight cron workflow (`on: schedule: cron: '0 9 * * 1'`) that reads the last commit message on `cowork-skeleton`, extracts the source tag, and compares it to `git tag -l 'v*' | sort -V | tail -1`; fails if they differ.

**Acceptance Criteria:** REQ-016 priority corrected to Must. Staleness-probe workflow defined. Test: simulate a missed CI run and confirm the probe fires within 24 hours.

---

### PM-003-20260626: File Count Headroom Erodes Without Proactive Monitoring [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Technical |
| **Likelihood** | Medium |
| **Priority** | P1 |
| **Affected Dimension** | Completeness |
| **Deliverable Reference** | `phase1-requirements.md` REQ-006; `phase1-requirements.md` §L2 Risk Implications R-002 (not listed — gap) |

**Failure Cause:** The current skeleton has ~1,744 tracked files against a ~5,000-file ceiling, providing a 3,256-file buffer. Jerry is an active, growing framework: skills, agents, templates, and documentation are added with each release. REQ-006 requires the generation script to exit non-zero when the count reaches or exceeds 5,000 — but this assertion only fires at generation time, after CI has already started. By the time the count crosses 5,000, CI has been failing silently (per PM-002) for possibly several release cycles, and the branch is correspondingly stale. There is no mechanism that warns when the tracked count in retained directories on `main` is approaching the limit — say, at 4,000 files (80%) or 4,500 files (90%).

**Evidence:** `phase1-requirements.md` REQ-006: "SHALL assert that the tracked file count of the generated branch tree is less than 5,000 and SHALL exit with a non-zero exit code if this assertion is not satisfied." No requirement covers an early-warning threshold. The risk register (`phase1-requirements.md` §Risk Implications) lists R-001 through R-007 from the ORCHESTRATION_PLAN, but does not include file-count headroom erosion as a risk.

**Prevention Gap:** No NFR defines an early-warning band (e.g., "warn at 85% of limit, fail at 100%"). No monitoring script or CI job checks the file count on `main` ahead of the generation cycle.

**Mitigation:** Add an NFR (NFR-006) requiring the generation script to emit a warning when the generated count exceeds 85% of the limit (4,250 files) and to fail at 100% (5,000). Additionally, add a periodic CI check (or extend the staleness probe from PM-002) that runs `git ls-files | wc -l` on `main`'s retained directories and posts a warning to `$GITHUB_STEP_SUMMARY` if the projected generated count exceeds 4,000.

**Acceptance Criteria:** Generation script emits a structured warning (non-zero advisory exit code or annotated step output) when generated count exceeds 4,250. Test: inject 2,600+ synthetic files into a retained directory and confirm warning fires before count reaches 5,000.

---

### PM-004-20260626: Short-SHA in Commit Message Creates Idempotency Trap [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Technical |
| **Likelihood** | Medium |
| **Priority** | P1 |
| **Affected Dimension** | Internal Consistency |
| **Deliverable Reference** | ADR-001 §Regeneration Commit Determinism, commit message template |

**Failure Cause:** ADR-001's commit message template uses `<short-sha>` in the subject line: `build(cowork-skeleton): regenerate from <tag> (<short-sha>)`. Git's short-SHA length is not fixed — it is the minimum number of characters needed to make the hash unique within the repository. As the repository accumulates commits, git may need 8 characters where it previously used 7 to avoid ambiguity. If `$(git rev-parse --short <commit>)` is used in the generation script, two executions against the same tag at different points in time could produce `abc1234` (7 chars) vs `abc12345` (8 chars) in the commit subject, producing different commit messages, different commit SHA preimages, and therefore different commit SHAs — silently breaking the bit-identical idempotency guarantee in REQ-003 and NFR-001. ADR-001's idempotency proof explicitly pins parent, identity, dates, and message, but treats the message as invariant without specifying that the short-sha must use a fixed length or be replaced with the full 40-char hash.

**Evidence:** ADR-001 §Regeneration Commit Determinism table, "Commit message" row: "fixed template embedding the source tag + 40-char source SHA, with **no** build timestamp or run ID." But the template itself shows `<short-sha>` (not 40 chars) in the first line. ADR-001 §Consequences (Negative) #2: "idempotency is discipline-dependent — bit-identical reproduction requires pinning... and the message." The message itself has a variable component.

**Prevention Gap:** The recommended commit message template in ADR-001 uses `<short-sha>` for readability in the subject line but does not specify that the implementation MUST use a fixed-length flag (e.g., `--short=40`) or substitute the full SHA. STORY-001 implementing the generation script may naturally use `git rev-parse --short`, introducing the variable.

**Mitigation:** Correct the ADR-001 commit message template to eliminate `<short-sha>` and replace it with either (a) the full 40-char source SHA or (b) a fixed-width abbreviation using `--short=8` (8-char minimum sufficient for all repositories under ~100,000 commits). Document in STORY-001 that `--short=8` or the full SHA MUST be used. Add a CI assertion (run after generation) that compares the regenerated commit SHA against the previous run for the same tag and fails if they differ.

**Acceptance Criteria:** Commit subject line uses a fixed-length hash (8 chars via `--short=8` or full 40-char). Idempotency test (REQ-003 acceptance criterion) passes across two executions at different points in repository history.

---

### PM-005-20260626: Force-Push Overwrites Contributor Commits Silently [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Process |
| **Likelihood** | Low |
| **Priority** | P1 |
| **Affected Dimension** | Methodological Rigor |
| **Deliverable Reference** | `phase1-requirements.md` REQ-021, REQ-028; ADR-002 §Branch-Protection Posture |

**Failure Cause:** The design intentionally keeps `cowork-skeleton` unprotected (REQ-021, ADR-002) to allow `GITHUB_TOKEN` force-push without a bypass actor. The sole mitigation for contributor confusion is documentation: REQ-028 requires a Reference document warning users not to commit directly to the branch. But a developer under time pressure who needs a quick fix in the plugin will push directly to `cowork-skeleton`, successfully (the branch is unprotected), and lose their work on the next release. The documentation warning is in the Reference doc — not in a branch description, CODEOWNERS, push hook, or pre-receive hook that would intercept the push at the point of action. The Reference doc may not be read until after the loss occurs.

**Evidence:** ADR-001 §Consequences (Negative) #3: "any contributor who mistakes `cowork-skeleton` for a development branch will have work overwritten on the next release. Mitigation: documentation + branch-protection posture." ADR-002 §Branch-Protection Posture: "keep `cowork-skeleton` unprotected... there is no human work on the branch to guard."

**Prevention Gap:** No at-push-time warning mechanism is specified. The GitHub branch description field (visible in the UI) could warn contributors without requiring branch protection. No CODEOWNERS entry prevents PR review requirements. No pre-receive hook or rulesets warning-mode is mentioned.

**Mitigation:** (1) Set the `cowork-skeleton` branch description (via GitHub API or STORY-005) to: "CI-OWNED — regenerated wholesale every release. Do NOT push directly: changes will be lost. See docs/reference/cowork-skeleton-branch.md." (2) Alternatively, add a GitHub ruleset in "warning mode" (not enforcement) that alerts pushers without blocking CI. (3) Document the recovery procedure (re-generate from the last affected tag via `workflow_dispatch`) in the Reference doc alongside the warning.

**Acceptance Criteria:** `cowork-skeleton` branch description set to a CI-ownership warning visible in GitHub UI without authentication. Recovery procedure documented in REQ-028 Reference doc.

---

### PM-006-20260626: Symlink Validation is Linux-CI-Only [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Assumption |
| **Likelihood** | Low–Medium |
| **Priority** | P1 |
| **Affected Dimension** | Evidence Quality |
| **Deliverable Reference** | `phase1-requirements.md` REQ-009; acceptance criterion for REQ-009 |

**Failure Cause:** REQ-009 requires that `.claude/rules` and `.claude/patterns` symlinks resolve to existing targets in the generated branch. The acceptance criterion uses `readlink -f` — a Linux-only command. The validation runs in CI (Linux GitHub Actions runner) and confirms symlinks resolve correctly on Linux. But CoWork is a Claude Code plugin and Claude Code runs on macOS and Windows. Git on Windows, by default (`core.symlinks=false`), stores symlinks as plain text files containing the link target path — they are not real filesystem symlinks. When Claude Code's auto-loading mechanism attempts to use `.claude/rules/` as a directory, it encounters a text file with contents like `../.context/rules`. The Jerry framework rules fail to load silently. All HARD rules (H-01 through H-36) become unenforced for Windows users of the CoWork plugin. The deliverables do not address this failure mode.

**Evidence:** `phase1-requirements.md` REQ-009 acceptance criterion: "`readlink -f .claude/rules` and `readlink -f .claude/patterns` both resolve to non-empty, existing paths." This test is Linux-specific. No requirement references Windows symlink behavior or cross-platform compatibility.

**Prevention Gap:** The deliverables assume a POSIX-compatible client environment for symlink resolution. No requirement specifies that CoWork installs on Windows are supported or that symlinks must be materialized correctly cross-platform. Research Q4 confirmed symlinks on `main` resolve on the CI/Linux environment, but did not address cross-platform behavior.

**Mitigation:** (1) Add a requirement (REQ-009a) specifying the expected CoWork client environments (macOS, Linux, Windows with Developer Mode, Windows without). (2) If Windows support is required: evaluate replacing symlinks with hard copies of rule files in the skeleton branch (simpler but doubles maintenance) or with a post-install hook that materializes them. (3) At minimum: add a known-limitations note to REQ-027 (How-To troubleshooting doc) documenting Windows symlink behavior as a known failure mode with the `core.symlinks=true` workaround.

**Acceptance Criteria:** Either (a) REQ-009 acceptance criterion includes a Windows-environment test using `git -c core.symlinks=false checkout` followed by Claude Code launch, confirming rules auto-load; or (b) documentation explicitly scopes CoWork support to macOS/Linux with a documented Windows workaround.

---

### PM-007-20260626: No Automated Action SHA Refresh Mechanism [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Process |
| **Likelihood** | High |
| **Priority** | P1 |
| **Affected Dimension** | Methodological Rigor |
| **Deliverable Reference** | `phase1-requirements.md` REQ-017; no counterpart requirement for update automation |

**Failure Cause:** REQ-017 mandates that all GitHub Actions in `cowork-skeleton.yml` be pinned to 40-character commit SHAs, not mutable tag aliases. This is correct supply-chain hygiene. However, pinned SHAs must be manually updated when upstream actions release security patches. The deliverables specify no automated update mechanism (Dependabot for Actions, Renovate, or a CI job that monitors upstream SHAs). As security patches are released for `actions/checkout`, `actions/setup-python`, or other pinned actions, the `cowork-skeleton.yml` workflow continues running on potentially vulnerable versions until a maintainer notices and manually updates the SHA. Given that `cowork-skeleton` CI runs are triggered by releases (not daily), the vulnerable window between a security patch and a SHA update could span multiple release cycles.

**Evidence:** `phase1-requirements.md` REQ-017: "All GitHub Actions referenced in `cowork-skeleton.yml` SHALL be pinned to their full 40-character commit SHA." No requirement, NFR, or workstream references automated SHA update tooling. The repo's `.github/workflows/` presumably has Dependabot configured for some dependencies (inference from the version-bump workflow pattern), but no requirement ensures `cowork-skeleton.yml` is included.

**Prevention Gap:** The supply-chain hardening goal (REQ-017, R-007) is incomplete without a corresponding automated update mechanism. SHA pinning creates security by preventing silent tag mutations but simultaneously creates a maintenance burden that is not accounted for in the requirements.

**Mitigation:** Add a requirement (REQ-017a) that a Dependabot `ecosystem: github-actions` entry exists in `.github/dependabot.yml` covering the `cowork-skeleton.yml` workflow, or that an equivalent automated PR mechanism exists. Verify Dependabot is enabled for GitHub Actions in the repository settings as part of Phase 6 acceptance.

**Acceptance Criteria:** `.github/dependabot.yml` contains an entry for `package-ecosystem: "github-actions"` with `directory: "/"` (or `".github/workflows/"`). Dependabot is confirmed active for the repository. Test: verify that a Dependabot PR updating a pinned action SHA would be automatically created within one week of a new action release.

---

### PM-008-20260626: Stub Static-Content Constraint Not Technically Enforced [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Category** | Process |
| **Likelihood** | Low |
| **Priority** | P2 |
| **Affected Dimension** | Traceability |
| **Deliverable Reference** | ADR-001 §Regeneration Commit Determinism ("Stub determinism constraint (c-001/c-006)"); ADR-001 §Risks row 5 |

**Failure Cause:** ADR-001 states: "the stub `projects/README.md` MUST be static content. Any generated date, version string, or run ID inside it changes the tree and breaks reproducibility. Authoring is STORY-002; this ADR fixes only its determinism property." The generation script does not validate the stub's content for dynamic values. A well-meaning maintainer who updates STORY-002 to include `<!-- Generated: {date} -->` or `Version: {version}` in the stub silently breaks bit-identical idempotency (REQ-003). Additionally, future changes to `FilesystemProjectAdapter.scan_projects()` could require the stub to have a specific format; there is no compatibility test that verifies the stub works with the current codebase version at generation time.

**Evidence:** ADR-001 §Risks table row 5: "Stub content includes a generated value → tree non-determinism | LOW | MED | Enforce static stub content (c-001); review in STORY-002." The mitigation is "review in STORY-002" — a human-in-the-loop process check, not a technical validation.

**Mitigation:** Add a pre-generation validation step in the script that confirms `projects/README.md`'s SHA matches a checked-in expected SHA (or that its content matches a pattern that excludes dynamic values). This could be as simple as a `git hash-object --stdin < expected_stub.txt` comparison.

**Acceptance Criteria:** Generation script contains a step validating stub content integrity. Test: modify stub content with a timestamp and confirm generation script exits non-zero.

---

### PM-009-20260626: CoWork Clone Timeout Risk Grows Without Monitoring [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Category** | Technical |
| **Likelihood** | Low–Medium |
| **Priority** | P2 |
| **Affected Dimension** | Actionability |
| **Deliverable Reference** | ADR-001 §Consequences (Negative) #1; ADR-001 §L2 ¶2; `phase1-requirements.md` REQ-027 |

**Failure Cause:** Option A (chosen) uses `fetch-depth: 0`, carrying `main`'s full commit history into the `cowork-skeleton` branch `.git`. As Jerry releases accumulate, `.git` grows. CoWork enforces a 120-second git operation timeout (`CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`). ADR-001 acknowledges this risk and designates Option B (orphan branch) as an escape hatch. However: (1) there is no monitoring of clone timing to detect when the threshold is being approached; (2) the orphan escape hatch requires implementing the orphan branch approach, which is not pre-implemented (it is "pre-designed"); (3) users who experience a clone timeout get an opaque error with no guidance. The How-To troubleshooting doc (REQ-027) mentions the timeout variable, but the Reference doc doesn't specify what clone size triggers the issue.

**Evidence:** ADR-001 §Consequences (Negative) #1: "Mitigation: Option B (orphan) escape hatch; optionally strip large blobs (R-002)." No metric defines "approaching the timeout threshold." REQ-027 is a "Should" priority requirement.

**Mitigation:** Add a CI step that records the `cowork-skeleton` clone size in bytes (e.g., `du -sh .git`) in the job summary on every successful run. Define an alert threshold (e.g., if `.git` exceeds 50MB, emit a warning: "Consider switching to Option B (orphan branch)"). Ensure the Option B escape-hatch implementation steps are defined in a runbook or STORY-X before they are needed.

**Acceptance Criteria:** Job summary includes clone size metric after each successful run. Runbook (or equivalent design doc) specifies the Option B activation procedure.

---

### PM-010-20260626: GITHUB_TOKEN Loop-Safety Depends on GitHub Implementation [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Category** | External |
| **Likelihood** | Low |
| **Priority** | P2 |
| **Affected Dimension** | Methodological Rigor |
| **Deliverable Reference** | ADR-002 §Loop-Safety Argument; `phase1-requirements.md` REQ-014 |

**Failure Cause:** ADR-002's loop-safety argument relies on three independent guarantees, the third being: "GITHUB_TOKEN pushes cannot re-trigger any workflow at all." This is based on GitHub's documented behavior ("events triggered by the GITHUB_TOKEN... will not create a new workflow run"). GitHub has changed the behavior of GITHUB_TOKEN in the past and could do so again. If GitHub modifies this behavior (e.g., to enable self-triggering by default for some workflow types), guarantee #3 fails, and the loop-safety argument now rests on only guarantees #1 (trigger shape: tags-only) and #2 (listener shape: `main`-only). Those two guarantees alone are sufficient, but the ADR's claim of "over-determined" loop-safety would no longer be accurate, and no monitoring would detect this change.

**Evidence:** ADR-002 §Loop-Safety Argument: "Loop-safety is **over-determined** — three independent guarantees each individually prevent an infinite regenerate-push loop." The third guarantee is an external dependency on GitHub's implementation, not a property of the workflow design.

**Mitigation:** Acknowledge in ADR-002 that guarantee #3 is an external dependency. Add a monitoring note: if a future GitHub change enables `GITHUB_TOKEN` workflow re-triggering by default, the design falls back to guarantees #1 and #2 (which remain valid). No redesign needed — this is a Minor risk given two remaining independent guarantees. Optionally add REQ-023a: "Verify annually or after GitHub Actions policy changes that `GITHUB_TOKEN`-pushed events do not create new workflow runs."

**Acceptance Criteria:** ADR-002 notes guarantee #3 is an external dependency. Review cadence defined (e.g., annual check or change-triggered review of GitHub Token behavior documentation).

---

## Recommendations

### P0 — Critical: MUST Mitigate Before Phase 5

| ID | Finding | Mitigation | Acceptance Criteria |
|----|---------|------------|---------------------|
| PM-001-20260626 | R-001 unverified before Phase 5 | Create machine-checkable verification artifact (`verification/R001-clean-clone-count.md`) + prerequisite check in generation script that exits non-zero if the file is absent | Generation script fails without `R001-clean-clone-count.md`; Phase 5 CI completion is technically blocked until verification is recorded |

### P1 — Important: SHOULD Mitigate Before Phase 5/6 Implementation

| ID | Finding | Mitigation | Acceptance Criteria |
|----|---------|------------|---------------------|
| PM-002-20260626 | Silent CI failure / staleness | Correct REQ-016 priority to Must; define staleness-detection probe | REQ-016 is a Must requirement; probe compares skeleton source tag vs. latest `v*` tag |
| PM-003-20260626 | File count headroom erosion | Add NFR-006 with 85% early warning band; add count monitoring on `main` | Script warns at 4,250 files; test passes with synthetic file injection |
| PM-004-20260626 | Short-SHA idempotency trap | Fix commit message template to use fixed-length SHA (`--short=8` or full 40-char) | Idempotency test passes across two executions at different repo history depths |
| PM-005-20260626 | Force-push overwrites contributor work | Set branch description CI-ownership warning; add recovery procedure to REQ-028 doc | Warning visible in GitHub UI; recovery procedure documented |
| PM-006-20260626 | Symlink validation Linux-only | Add cross-platform scope requirement; add Windows symlink failure to REQ-027 troubleshooting | Acceptance criterion includes Windows test OR scope is explicitly documented |
| PM-007-20260626 | No automated Action SHA refresh | Add Dependabot github-actions entry to `.github/dependabot.yml` | Dependabot PR would be created within one week of an upstream action release |

### P2 — Monitor: MAY Mitigate; Acknowledge Risk

| ID | Finding | Monitoring Approach |
|----|---------|---------------------|
| PM-008-20260626 | Stub static-content contract | Add generation-time stub content hash check; validate `jerry projects list` on each CI run |
| PM-009-20260626 | Clone timeout risk | Emit `.git` size in job summary; define Option B activation runbook |
| PM-010-20260626 | GITHUB_TOKEN external dependency | Document guarantee #3 as external; define annual review cadence |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-001: R-001 verification has no technical enforcement. PM-003: no file-count headroom monitoring. PM-007: SHA refresh automation absent. Three significant gaps in the coverage of the design. |
| Internal Consistency | 0.20 | Negative | PM-004: ADR-001's commit message template contradicts its own idempotency proof (short-SHA in subject vs. 40-char in body). PM-002: REQ-016 uses "SHALL" but Priority = "Should" — internal inconsistency in the requirements specification. |
| Methodological Rigor | 0.20 | Negative | PM-005: force-push overwrite mitigation relies on documentation alone. PM-007: SHA pinning without update automation is an incomplete security control. PM-010: loop-safety claim of "over-determined" rests on an external dependency for one of three guarantees. |
| Evidence Quality | 0.15 | Negative | PM-006: REQ-009 acceptance criterion uses `readlink -f` (Linux-only) without addressing cross-platform symlink behavior. The evidence base for CoWork installability is Linux/CI-centric. |
| Actionability | 0.15 | Negative | PM-002: no staleness-detection probe defined; maintainers have no actionable signal when CI silently fails. PM-009: clone timeout risk acknowledged but no monitoring defined to detect approach. |
| Traceability | 0.10 | Neutral | Requirements trace correctly to stakeholder needs. ADR-001 and ADR-002 document their evidence references. The main traceability gaps are forward-looking (PM-008: stub constraint not enforced in STORY-001/002). |

**Overall Assessment:** ACCEPT with P0 and P1 mitigations required. The design is architecturally sound: Option A (tag + rm + stub + force-push) is correct; `GITHUB_TOKEN` is correct; the loop-safety argument has two fully independent guarantees even without #3; the idempotency proof is almost complete. The failures enumerated here are implementation traps, process gaps, and unclosed assumption risks — not fundamental design errors. Addressing PM-001 (R-001 technical gate) and PM-004 (short-SHA fix) before Phase 5 is the minimum bar.

---

## Execution Statistics

- **Total Findings:** 10
- **Critical:** 1
- **Major:** 6
- **Minor:** 3
- **Protocol Steps Completed:** 6 of 6
  - Step 1: Stage set — failure scenario declared
  - Step 2: Temporal perspective shift established
  - Step 3: 10 failure causes generated across all 5 category lenses (Technical, Process, Assumption, External, Resource)
  - Step 4: Prioritized P0/P1/P2 matrix
  - Step 5: Mitigations with acceptance criteria for P0/P1 findings
  - Step 6: Scoring impact table and overall assessment

---

*Strategy: S-004 Pre-Mortem Analysis*
*Execution ID: 20260626*
*Reviewer: jerry:adv-executor (blind, independent)*
*Template: `.context/templates/adversarial/s-004-pre-mortem.md` v1.0.0*
*Project: PROJ-031-cowork-skeleton*
*Phase: 1 (Requirements and Architecture)*
*Quality Gate: QG-1*
