# Inversion Report: PROJ-031 CoWork Skeleton — Phase 1 Deliverables (Iteration 2)

**Strategy:** S-013 Inversion Technique
**Deliverables:** `requirements/phase1-requirements.md`, `decisions/ADR-001-skeleton-derived-branch-strategy.md`, `decisions/ADR-002-ci-token-push-strategy.md`
**Criticality:** C4
**Date:** 2026-06-26
**Reviewer:** adv-executor (Group E — Decompose), Iteration 2 Blind Run
**H-16 Compliance:** S-003 Steelman applied in Iteration 1 (confirmed per task context; adv-executor operating blind to prior findings)
**Goals Analyzed:** 7 | **Assumptions Mapped:** 10 | **Vulnerable Assumptions:** 7

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Step 1: Goals](#step-1-goals) | Seven primary goals extracted from the deliverables |
| [Step 2: Anti-Goals](#step-2-anti-goals) | Goal inversions — what would guarantee each failure |
| [Step 3: Assumption Map](#step-3-assumption-map) | Explicit and implicit assumptions with confidence ratings |
| [Step 4: Stress-Test Results](#step-4-stress-test-results) | Findings table — all vulnerable assumptions |
| [Step 5: Finding Details](#step-5-finding-details) | Critical and Major findings with evidence and mitigations |
| [Step 6: Scoring Impact](#step-6-scoring-impact) | S-014 dimension impact of identified gaps |
| [Recommendations](#recommendations) | Prioritized mitigation plan |

---

## Summary

The revised design has meaningfully strengthened its controls: the three-dimensional R-001 gate (REQ-034), the pre-push equivalence check (REQ-022), the staleness-detection workflow (NFR-006), and the tamper-evidence argument (ADR-001 §Tamper-Evidence + ADR-002 c-107) each close a real gap from iteration 1. However, inversion reveals that two controls **appear to close their failure mode without actually doing so**: the "pre-publication integrity gate" for the unprotected-branch direct-push attack (IN-01) is architecturally undefined in the requirements and tautological if placed inside the generating workflow; and the single-shot R-001 clone-time measurement (IN-02) does not account for monotonically growing clone weight under Option A across releases. Three Major gaps remain in staleness-detection permissions (IN-03), CoWork-runtime symlink verification (IN-04), and file-count margin monitoring (IN-05). Recommendation: **REVISE** — address IN-01 and IN-02 before Phase 2 gate.

---

## Step 1: Goals

| # | Goal | Type | Source |
|---|------|------|--------|
| G-01 | CoWork installs without hitting the ~5,000-file limit | Explicit | REQ-001, STK-001 |
| G-02 | Skeleton auto-syncs with `main` within one CI run per `v*` tag | Explicit | NFR-003, STK-002 |
| G-03 | Fresh CoWork install is immediately usable (H-04 bootstrap, SessionStart, `jerry projects list`) | Explicit | REQ-004/REQ-004a/REQ-009/REQ-010, STK-003 |
| G-04 | CI pipeline introduces no secret leakage, token over-scope, or supply-chain risk | Explicit | WS-3, STK-004 |
| G-05 | Same source tag always produces a bit-identical commit SHA (determinism / tamper-evidence) | Explicit | REQ-003, NFR-001, ADR-001 §Regeneration Commit Determinism |
| G-06 | The solution remains maintainable by future contributors with minimal tooling | Explicit | c-005, PLAN.md Goals |
| G-07 | All deliverables score >= 0.95 C4 composite before any irreversible action | Explicit | REQ-031, WS-5 |

---

## Step 2: Anti-Goals

For each goal: "To guarantee we FAIL to achieve this goal, we would..."

| G# | Anti-Goal (Failure Guarantee) | Does revised design avoid it? |
|----|-------------------------------|-------------------------------|
| G-01 | Never strip enough; or add files to retained directories until count creeps to >5,000 with no margin alarm | Partially — REQ-006 hard-fails at 5,000 but no margin-monitoring exists |
| G-02 | Let the tag trigger silently misfire with no detection; or let the staleness workflow itself lapse | Partially — NFR-006 adds a weekly check but implementation story and permissions are unspecified |
| G-03 | Break symlinks in the CoWork runtime (not just CI runner); or fail Windows users silently | No — symlink verification is CI-Linux only; CoWork runtime test gap persists |
| G-04 | Inject malicious content into the unprotected branch between CI runs without detection | Partially — "pre-publication integrity gate" is described but architecturally undefined |
| G-05 | Let clone-time drift past 120s threshold on slow networks as repository history grows | No — R-001 measured once at Phase 2; no periodic re-check exists |
| G-06 | Introduce manual sync requirements between two source-of-truth lists that inevitably diverge | Partially — ADR-001 c-003 / REQ-005 sync note exists but no automated check |
| G-07 | Let the quality gate pass despite a gap that a future adversary would exploit | This report surfaces remaining gaps |

---

## Step 3: Assumption Map

| ID | Assumption | Type | Confidence | Validation Status |
|----|------------|------|------------|-------------------|
| A-01 | The pre-publication integrity gate (c-107) provides effective protection against RT-01 direct-push attacks on the unprotected branch | Implicit | Low | Unvalidated — mechanism not specified in requirements |
| A-02 | The R-001 three-dimensional measurement taken once at Phase 2 remains valid for all future releases as repository history accumulates | Implicit | Medium | Logically flawed — Option A history grows monotonically |
| A-03 | NFR-006 staleness-detection workflow has sufficient permissions (and a concrete implementation story) to create visible failures | Implicit | Low | Unspecified — no implementation story; permissions not declared |
| A-04 | `.claude/rules` and `.claude/patterns` symlinks resolve correctly in the CoWork runtime (not just on the CI Linux runner) | Implicit | Low | Unvalidated — REQ-009 AC explicitly limits itself to CI Linux |
| A-05 | The file-count margin (~3,256 spare files) is stable; no retained directory will grow to threaten the 5,000 ceiling between the current release and future ones | Implicit | Medium | Inferred — no ongoing margin monitoring |
| A-06 | Git tags used for `inputs.target_tag` are immutable; moving a tag doesn't break idempotency re-runs | Implicit | Medium | Assumed — no prohibition on tag mutation |
| A-07 | The canonical surface list in ADR-001 c-003 and REQ-005 will remain in sync through future changes | Implicit | Medium | Partially — documented sync requirement exists but no automated check |
| A-08 | CoWork's plugin-load behavior (file-count ceiling, 120s timeout, relative-path `source: "./"`) is stable and won't change between releases | Explicit (documented uncertainty) | Low | Unvalidated per R-001 — acknowledged but undocumented CoWork dependency |
| A-09 | The "expected deterministic SHA" for the integrity gate is computed/published somewhere accessible to the gate itself | Implicit | Low | Unspecified — no requirement defines where or how this SHA is published |
| A-10 | Removing only `projects/` from `main` is sufficient to achieve installability with no functional degradation for CoWork users | Explicit (R-001 fallback clause) | Medium | Verified for file-count; unverified for end-to-end functional install |

---

## Step 4: Stress-Test Results

| ID | Assumption / Anti-Goal | Inversion | Plausibility | Severity | Affected Dimension |
|----|------------------------|-----------|--------------|----------|--------------------|
| IN-001-20260626T1500 | A-01 / A-09: Pre-publication integrity gate prevents RT-01 direct-push attacks | Gate never runs (undefined mechanism) OR is tautological (compares SHA CI just created to itself) | **High** — the requirements have no CI step that independently computes the expected SHA and compares it after each regeneration; ADR-002 says the gate is "required" but no REQ-xxx demands it | **Critical** | Methodological Rigor |
| IN-002-20260626T1500 | A-02: Single-shot R-001 clone-time measurement valid forever | Every future release adds history weight under Option A; clone time crosses 60s/250MB threshold silently between Phase 2 measurement and a later release | **High** — there is no re-measurement requirement in NFR-006 or any other NFR | **Critical** | Completeness |
| IN-003-20260626T1500 | A-03: NFR-006 staleness-detection workflow has correct permissions and a concrete implementation path | Staleness workflow needs `issues: write` permission to open a GitHub issue; `cowork-skeleton.yml` uses `contents: write` only; OR the workflow fails silently if `GITHUB_TOKEN` lacks issue-creation scope; no STORY covers this workflow | **High** — `GITHUB_TOKEN` defaults vary; issue creation requires `issues: write` not declared; no implementation story exists | **Major** | Completeness |
| IN-004-20260626T1500 | A-04: Symlinks resolve correctly in CoWork runtime | CoWork uses a non-standard file-materialization path (copy to `~/.claude/plugins/cache`) that may not resolve symlinks the same way as a standard `git clone`; Windows users with `core.symlinks=false` get text files | **High** — REQ-009 AC explicitly restricts itself to CI Linux; R-001 §Verification Approach does not include a symlink test; Windows is a documented known failure | **Major** | Evidence Quality |
| IN-005-20260626T1500 | A-05: File-count margin stable with no monitoring | Retained directories (`docs/`, `tests/`, `skills/`, `runbooks/`, `overrides/`, `scripts/`) gradually fill the 3,256-file margin; skeleton crosses 5,000 on a future release with no earlier warning | **Medium** — these directories are currently non-strip-targets by design; their growth is not monitored | **Major** | Completeness |
| IN-006-20260626T1500 | A-07: ADR-001 c-003 / REQ-005 remain in sync | A future ADR-001 update adds a new load-bearing directory but forgets to update REQ-005 (reproducing the iteration-1 divergence); no automated sync check exists | **Medium** — this is exactly what happened in iteration 1 | **Minor** | Internal Consistency |
| IN-007-20260626T1500 | A-06: Git tags are immutable for idempotency re-runs | A maintainer force-moves a `v*` tag (bad practice but unprevented); `workflow_dispatch` with that tag name now re-runs against a different commit SHA, breaking the idempotency proof | **Low** — bad practice but technically possible | **Minor** | Methodological Rigor |

---

## Step 5: Finding Details

### IN-001-20260626T1500: Pre-Publication Integrity Gate Is Architecturally Undefined [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Type** | Anti-Goal (G-04) |
| **Inverted Goal** | "Guarantee silent supply-chain compromise via direct push to unprotected branch" |
| **Plausibility** | High — direct collaboration push to an unprotected GitHub branch requires no special access |
| **Confidence in finding** | High |

**Evidence:**

ADR-002 §c-107 states: "artifact integrity MUST rest on a compensating control (deterministic-SHA tamper-evidence + pre-publication integrity gate)." ADR-002 §Branch-Protection Posture states: "Before `cowork-skeleton` is advertised/consumed as installable, assert `git rev-parse cowork-skeleton == <expected deterministic SHA>`."

However, no requirement in phase1-requirements.md specifies:
- A CI step, workflow job, or external process that computes the "expected deterministic SHA"
- Where the expected SHA is published (GitHub Release notes is suggested in ADR-001, but no REQ-xxx requires this)
- When "advertised/consumed as installable" occurs as a distinct checkpoint (the branch is force-pushed and instantly publicly readable — there is no subsequent publication step)

REQ-022 (pre-push equivalence check) verifies the *tree diff* before pushing — not the full commit SHA. The NFR-006 staleness check compares the `Source-Commit:` *trailer text* to the latest tag SHA — not the full branch commit SHA. No existing requirement closes the gap between "branch was regenerated" and "branch tip SHA was independently verified."

If the gate is placed INSIDE `cowork-skeleton.yml` (after the push), it is asserting the SHA the workflow just created against a value the workflow derived — which is tautological and provides no protection against a malicious action that replaces the branch content after the workflow completes. If the gate is supposed to run outside the workflow (e.g., in the staleness-detection workflow), it is not currently specified to do so.

**Consequence:** The unprotected-branch detective-only posture (ADR-002 Decision) relies on a gate that has no concrete implementation requirement. An adversary who directly pushes to `cowork-skeleton` would have their content installed by CoWork users until the next CI regeneration — potentially an entire release cycle — with no detection mechanism that is actually required by the current specifications.

**Recommendation:** Add a new requirement (REQ-XXX) that specifies: (a) the `cowork-skeleton.yml` workflow SHALL publish the regenerated commit SHA to a durable artifact (e.g., GitHub Release notes via `gh release edit v{TAG} --notes-append` or a workflow output), and (b) the staleness-detection workflow (NFR-006) SHALL additionally assert `git rev-parse cowork-skeleton == <SHA from published artifact>`, failing loudly if they diverge. This makes the gate asynchronous (runs in the scheduled staleness workflow, not inside the generating workflow) and non-tautological (uses an externally published value rather than a locally derived one).

**Acceptance Criteria:** (a) `cowork-skeleton.yml` has a step that emits the regenerated SHA to an external durable artifact; (b) the staleness-detection workflow reads the published SHA and asserts the live branch tip matches; (c) a simulated direct-push attack (push a dirty commit directly to `cowork-skeleton`) is detected and flagged by the next scheduled staleness run within one week.

---

### IN-002-20260626T1500: Single-Shot Clone-Time Measurement Ignores Monotonic History Growth [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Type** | Assumption Failure (A-02) |
| **Inverted Goal** | "Guarantee the skeleton exceeds the 120s clone-time limit on a future release" |
| **Plausibility** | High — Option A preserves full `main` history; each release adds ~1 commit + parent history |
| **Confidence in finding** | High |

**Evidence:**

ADR-001 §Decision specifies the Option B (orphan) fallback triggers when "a clean `git clone` of `cowork-skeleton`... exceeds **60 s** wall-clock **or** its compressed pack exceeds **250 MB**." ADR-001 §Negative Consequences states: "Clone weight under full provenance — `fetch-depth: 0` carries `main`'s history into the skeleton `.git`; on slow networks this risks CoWork's 120-second git-operation timeout."

REQ-034 requires a `verification/R001-clean-clone-count.md` artifact recording: (a) tracked file count, (b) compressed pack size, (c) estimated clone time — created **before Phase 2** and serving as the **Phase-2-blocking gate**.

Under Option A, `cowork-skeleton`'s `.git` inherits the **full `main` history** at each release. If the repository currently has a compressed pack of (say) 100 MB, adding 50 releases at 2 MB per release each would bring the pack to ~200 MB and approach the 250 MB threshold. The R-001 measurement at Phase 2 captures a single snapshot of the repository at release v0.31.x, not a projection of future growth.

No NFR or requirement specifies:
- A periodic re-measurement of clone time/pack size after Phase 2
- A threshold-proximity alert (e.g., warn at 150 MB pack, which is 60% of the 250 MB trigger)
- Automatic orphan-branch switch when the threshold is breached after Phase 2

The NFR-006 staleness-detection workflow checks `Source-Commit:` vs. latest tag — it does NOT measure clone weight. The hard-fail assertion in REQ-006 checks tracked file count at generation time — it does NOT measure clone time. Result: the 60 s/250 MB threshold can be breached silently at any release after Phase 2.

**Consequence:** The Option B (orphan) fallback trigger exists in ADR-001 as a "documented escape hatch," but there is no operational requirement to detect when that trigger condition has been met. CoWork users could encounter installation failures due to clone-time timeout starting from some future release, with no pre-release warning.

**Recommendation:** Add a requirement that the staleness-detection workflow (NFR-006 implementation) also measures `git count-objects -vH` (`size-pack:` field) on the `cowork-skeleton` branch and alerts (workflow failure or GitHub issue) when it exceeds 150 MB (60% of the 250 MB trigger). Additionally, add a CI check inside `cowork-skeleton.yml` that emits `size-pack:` to `$GITHUB_STEP_SUMMARY` on every run and exits non-zero if it exceeds the 250 MB threshold, triggering an automatic switch to Option B (orphan).

**Acceptance Criteria:** (a) `cowork-skeleton.yml` emits `size-pack:` to `$GITHUB_STEP_SUMMARY` and fails if it exceeds 250 MB; (b) the staleness-detection workflow alerts at 150 MB pack; (c) a simulated large-history scenario (inject synthetic objects into the repo) triggers the 250 MB gate before the skeleton is pushed.

---

### IN-003-20260626T1500: Staleness-Detection Workflow Has No Implementation Story and Ambiguous Permissions [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption Failure (A-03) |
| **Inverted Goal** | "Guarantee the skeleton goes perpetually stale with no alert" |
| **Plausibility** | High — implementation gaps in NFR-006 make this the most likely failure mode of the staleness control |

**Evidence:**

NFR-006 requires a staleness-detection workflow that "SHALL fail visibly — producing a GitHub Actions job failure OR creating a GitHub issue." This OR introduces ambiguity:

1. A GitHub Actions job failure alone only notifies maintainers if they monitor Actions dashboards. A GitHub issue creates a persistent tracked item. The choice matters for operational reliability.

2. Creating a GitHub issue requires `issues: write` permission. The ADR-002 decision chose `GITHUB_TOKEN` with `contents: write` only for the skeleton push workflow. The staleness-detection workflow has different capability requirements. Neither ADR-002 nor the requirements specifies the permissions block for the staleness-detection workflow. If that workflow inherits repository default (often `read` only) and the implementation uses `gh issue create`, the issue creation silently fails, leaving only a job-status failure — which is easy to miss.

3. No STORY in the worktracker covers the staleness-detection workflow. The implementation stories are STORY-001 (generation script), STORY-002 (stub), STORY-003 (acceptance tests), STORY-004 (STRIDE threat model), STORY-005 (branch-protection config). NFR-006 is a requirements artifact with no implementation artifact specified.

**Recommendation:** (a) Change NFR-006 "OR" to "AND" (job failure AND issue creation for maximum visibility). (b) Declare the staleness-detection workflow's `permissions:` block explicitly (`issues: write` + `contents: read`). (c) Create STORY-006 (or equivalent) to implement `cowork-skeleton-staleness.yml`.

**Acceptance Criteria:** (a) A new STORY entity covering NFR-006 implementation is created; (b) the workflow YAML declares explicit `permissions: issues: write` and `contents: read`; (c) a simulated staleness test produces BOTH a job failure AND a GitHub issue.

---

### IN-004-20260626T1500: Symlink Behavior in CoWork Runtime Unverified and Windows Gap Acknowledged But Not Fixed [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption Failure (A-04) |
| **Inverted Goal** | "Guarantee the plugin is broken on a fresh CoWork install" |
| **Plausibility** | High (Windows); Medium (non-standard CoWork runtime) |

**Evidence:**

REQ-009 AC states: "In `cowork-skeleton`: `readlink -f .claude/rules` and `readlink -f .claude/patterns` both resolve to non-empty, existing paths **(CI Linux environment)**." The requirement itself notes: "CoWork session symlink resolution is separately verified in R-001 §Verification Approach before Phase 5."

However, examining REQ-034 (the R-001 machine-checkable artifact requirement) reveals its three specified dimensions are: (a) tracked file count, (b) compressed pack size, (c) clone time. Symlink resolution in the CoWork runtime is NOT among these three dimensions. The cross-reference from REQ-009 to "R-001 §Verification Approach" is pointing to something that doesn't include a symlink test.

Additionally, REQ-027 (How-To troubleshooting guide) requires documenting Windows `core.symlinks=false` "as a known failure mode with the `git config core.symlinks true` workaround." This documents a failure but does not prevent it. Windows users who install the plugin without setting `core.symlinks=true` before cloning receive text files instead of symlinks, causing all `.context/rules/*.md` files to fail to auto-load into Claude Code — silently breaking the entire Jerry framework behavior.

**Recommendation:** (a) Add a fourth dimension to REQ-034 and the R-001 verification artifact: functional symlink verification in a CoWork-like environment (clone to `~/.claude/plugins/cache` equivalent on both Linux and Windows with default git config; verify `.claude/rules` resolves to the `.context/rules/` directory). (b) Revise REQ-027 to require the Tutorial to include a pre-install Windows warning with the `core.symlinks true` fix BEFORE the install step (not in a troubleshooting guide reached only after failure).

**Acceptance Criteria:** (a) R-001 artifact includes a symlink resolution test result; (b) Tutorial document presents the Windows symlink prerequisite before the `claude plugin marketplace add` step; (c) CI acceptance test for REQ-009 is re-run in a Windows-like environment (via a Windows runner or simulated).

---

### IN-005-20260626T1500: File-Count Margin Has No Ongoing Monitoring [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption Failure (A-05) |
| **Inverted Goal** | "Guarantee the skeleton eventually exceeds 5,000 files with no warning" |
| **Plausibility** | Medium — gradual growth in retained directories is expected |

**Evidence:**

The current margin is ~1,744 tracked files vs. 5,000 ceiling — approximately 3,256 spare files, ~65% of the ceiling. Retained (non-stripped) directories include: `docs/`, `tests/`, `skills/`, `runbooks/`, `overrides/`, `scripts/`, and `schemas/`. These are currently retained because they're not load-bearing AND the margin is comfortable, per ADR-001 §Canonical Plugin-Retention Surface.

REQ-006 provides a hard-fail assertion at generation time if the count reaches 5,000. But:
- This assertion only runs during `cowork-skeleton.yml` execution (triggered by `v*` tag push)
- Between releases, there is no visibility into whether `main` has accumulated files that will cause the next release to fail
- NFR-006 staleness-detection does NOT check file count — it checks only the `Source-Commit:` trailer
- No requirement alerts when the file count of `main`'s non-project directories crosses a warning threshold (e.g., 3,500 = 70% of the ceiling)

Result: the first indication of file-count creep is a CI failure at release time, not a pre-release warning.

**Recommendation:** Add a requirement that `cowork-skeleton.yml` emits the current skeleton file count to `$GITHUB_STEP_SUMMARY` on every run, and add a warning exit condition (not a failure) when the count exceeds 3,500 (70% of the 5,000 ceiling) to prompt maintainers to consider additional directory stripping. Additionally, the staleness-detection workflow MAY perform a spot-count of `main`'s non-project tracked files as a margin-health signal.

**Acceptance Criteria:** (a) `cowork-skeleton.yml` emits file count to `$GITHUB_STEP_SUMMARY`; (b) a simulated "margin pressure" test (inject synthetic files to approach 3,500) produces a warning-level notification before crossing the hard-fail threshold at 5,000.

---

### IN-006-20260626T1500: ADR-001 c-003 and REQ-005 Sync Has No Automated Verification [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Assumption Failure (A-07) |
| **Inverted Goal** | "Guarantee the canonical surface list diverges again" |
| **Plausibility** | Medium — iteration 1 divergence demonstrates it is a real failure mode |

**Evidence:** REQ-005 contains the note: "REQ-005 and ADR-001 c-003 must be kept in sync; changes to the surface list require updating both documents." This is a documentation discipline requirement with no automated check. The same divergence was the root cause of REM-008 in iteration 1. No CI test verifies the two lists match.

**Recommendation:** Add a CI lint step (e.g., a simple shell script or pytest) that parses the directory list from ADR-001 c-003 and REQ-005 and asserts they are identical. This converts a documentation discipline requirement into an automated gate.

**Acceptance Criteria:** CI lint exits non-zero when the two directory lists differ; the lint runs on PR and on `main` merge.

---

### IN-007-20260626T1500: Idempotency Proof Assumes Git Tag Immutability [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Assumption Failure (A-06) |
| **Inverted Goal** | "Guarantee `workflow_dispatch` re-runs produce a different SHA than the original run" |
| **Plausibility** | Low — tag mutation is bad practice and rare |

**Evidence:** ADR-001 §Idempotency Proof states: "Given tag `T` resolving to source commit `S`..." The proof assumes T → S is a fixed mapping. `git tag -f v0.31.5 <new-sha>` silently mutates this mapping. REQ-011 declares `inputs.target_tag` for re-runs but has no validation that the tag hasn't been moved.

**Recommendation:** Add a generation-script validation step that records the SHA the tag resolved to at first generation and asserts on re-runs that the same tag still resolves to the same SHA. If the SHA differs, emit a loud warning (the idempotency guarantee is broken for that tag).

**Acceptance Criteria:** The generation script exits with a warning when `git rev-parse <TAG>^{commit}` on a re-run differs from the SHA recorded in the `Source-Commit:` trailer of the existing `cowork-skeleton` branch.

---

## Step 6: Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | **Negative** | IN-002 (no periodic clone-time re-check), IN-003 (no NFR-006 implementation story), IN-005 (no file-count margin monitoring) — three gaps in coverage of ongoing operational controls |
| Internal Consistency | 0.20 | **Negative** | IN-001 (ADR-002 says integrity gate is "required" but no REQ-xxx operationalizes it; c-107 claims a control that doesn't exist in the requirements) and IN-006 (two SSoTs that must stay in sync manually) |
| Methodological Rigor | 0.20 | **Negative** | IN-001 (the detective control for the highest-risk scenario RT-01/R-007b is architecturally undefined); IN-002 (single-shot measurement used as a permanent gate for a monotonically changing quantity) |
| Evidence Quality | 0.15 | **Negative** | IN-004 (REQ-009 explicitly restricts its AC to CI Linux; cross-reference to R-001 symlink test is inaccurate — R-001 doesn't include a symlink test) |
| Actionability | 0.15 | **Mixed** | Most existing requirements are actionable. IN-001 and IN-003 leave significant implementation ambiguity. Recommendations above are concrete and add specificity. |
| Traceability | 0.10 | **Slightly Negative** | IN-001 (ADR-002 c-107 has no corresponding REQ-xxx); IN-004 (REQ-009 references R-001 §Verification Approach but that section doesn't contain a symlink test dimension) |

---

## Recommendations

### Critical (MUST mitigate before Phase 2 gate)

| ID | Mitigation | Acceptance Criteria |
|----|------------|---------------------|
| IN-001-20260626T1500 | Define the pre-publication integrity gate as a concrete requirement: (a) `cowork-skeleton.yml` emits the regenerated SHA to a durable published artifact (GitHub Release notes or workflow output); (b) NFR-006 staleness workflow independently retrieves the published SHA and asserts `git rev-parse cowork-skeleton == <published SHA>` | Simulated direct-push attack detected within one weekly staleness cycle |
| IN-002-20260626T1500 | Extend the staleness-detection workflow and/or `cowork-skeleton.yml` to measure `size-pack:` on every run; add a 250 MB hard-fail (automatic orphan-switch trigger) and a 150 MB warning; add these to REQ-034's scope as a 4th/5th dimension | Generated branch size emitted to `$GITHUB_STEP_SUMMARY`; CI fails at 250 MB; stakeholder alert at 150 MB |

### Major (SHOULD mitigate before Phase 5 — prior to irreversible CI actions)

| ID | Mitigation | Acceptance Criteria |
|----|------------|---------------------|
| IN-003-20260626T1500 | Create STORY-006 for NFR-006 implementation; declare `permissions: issues: write` + `contents: read` for the staleness workflow; change NFR-006 "OR" to "AND" | STORY entity exists; both failure modes produce workflow failure AND GitHub issue in acceptance test |
| IN-004-20260626T1500 | Add symlink resolution test to R-001 §Verification Approach as a 4th dimension; revise REQ-034 AC accordingly; move the Windows `core.symlinks` warning to a pre-installation prerequisite in the Tutorial (REQ-024a) | R-001 artifact contains symlink test result; Tutorial presents the Windows prerequisite before the install command |
| IN-005-20260626T1500 | Add a file-count margin warning (at 3,500 / 70% of ceiling) to `cowork-skeleton.yml` `$GITHUB_STEP_SUMMARY` | CI emits file count and warns before hitting the hard-fail threshold |

### Minor (MAY mitigate)

| ID | Mitigation |
|----|------------|
| IN-006-20260626T1500 | Add CI lint asserting ADR-001 c-003 directory list equals REQ-005 directory list |
| IN-007-20260626T1500 | Add generation-script validation that compares the resolved tag SHA to the `Source-Commit:` trailer on re-runs, warning if diverged |

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 2 (IN-001, IN-002)
- **Major:** 3 (IN-003, IN-004, IN-005)
- **Minor:** 2 (IN-006, IN-007)
- **Protocol Steps Completed:** 6 of 6
- **Goals Inverted:** 7 of 7
- **Assumptions Stress-Tested:** 10 (7 with Major+ consequences)
- **Recommendation:** REVISE — address IN-001 and IN-002 before Phase 2 gate

---

*Generated by: adv-executor (Group E — Decompose), Iteration 2 Blind Run*
*Strategy: S-013 Inversion Technique (template: `.context/templates/adversarial/s-013-inversion.md`)*
*Project: PROJ-031-cowork-skeleton*
*Date: 2026-06-26*
*P-003 compliance: no subagents spawned*
*P-020 compliance: deliverables not edited*
*H-15 compliance: self-review applied before write*
