# Pre-Mortem Report: PROJ-031 CoWork Skeleton — Phase 1 Deliverables (Iteration 3)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `phase1-requirements.md`, `ADR-001-skeleton-derived-branch-strategy.md`, `ADR-002-ci-token-push-strategy.md`
**Criticality:** C4
**Date:** 2026-06-26
**Reviewer:** jerry:adv-executor (Group C — Challenge; blind, independent)
**H-16 Compliance:** S-003 Steelman applied before finalization — confirmed in ADR-001 footer ("S-003 (Steelman of Options B and C) applied before finalization per H-15/H-16") and ADR-002 footer (same statement); requirements doc confirms S-010 + S-003 applied across all three iterations.
**Failure Scenario:** It is December 26, 2026. The cowork-skeleton CI has been running for six months. A security incident is reported: the live `cowork-skeleton` branch contained tampered `hooks/` files that exfiltrated user environment variables for an indeterminate window. Investigation reveals: (a) the scheduled integrity monitor had silently failed on three consecutive daily runs — a `gh release view` API rate-limit error left the monitor exiting zero without creating a GitHub issue; (b) REQ-034 dimension (d), the CoWork smoke test, was deferred to Phase 4 and was never executed before Phase 5 implementation began — users discovered a broken install experience in production, forcing a full strategy pivot review; (c) a `workflow_dispatch` run with a blank `inputs.target_tag` resolved to a pre-release tag `v1.1.0-rc.1`, which failed the allow-list and exited non-zero without a diagnostically clear error, leaving the skeleton stale; (d) the clone-weight telemetry step measured `size:` (loose-object count) instead of `size-pack:` (packed history), missing true pack growth and never triggering the early-warning band.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Temporal Perspective Shift](#temporal-perspective-shift) | Retrospective frame declaration |
| [Findings Summary](#findings-summary) | All findings in priority order |
| [Detailed Findings](#detailed-findings) | Critical and Major findings with evidence and mitigations |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 quality dimensions |
| [Execution Statistics](#execution-statistics) | Protocol completion and counts |

---

## Temporal Perspective Shift

It is December 26, 2026. This deliverable set has failed spectacularly. We are not predicting failure — we are explaining it after the fact. All failure causes below are stated in the retrospective: "this is what happened, and here is why the controls did not prevent it."

---

## Findings Summary

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-IT3-0626 | Detection SLA (≤ daily) permits tampered executable hooks to reach user workstations for up to 24 h — no formal risk-acceptance decision or SLA reduction path documented | Technical | High | Critical | P0 | Methodological Rigor |
| PM-002-IT3-0626 | REQ-034 dimension (d) smoke test legally deferred to Phase 4; strategy is validated only by proxies until then — full pivot risk persists throughout Phases 2–4 | Process | Medium | Critical | P0 | Completeness |
| PM-003-IT3-0626 | Event-driven monitor (`on: push`) does not fire on branch-delete-and-recreate tamper; detection falls back to the 24 h scheduled leg without documentation of this gap | Technical | Low | Major | P1 | Internal Consistency |
| PM-004-IT3-0626 | Clone-weight thresholds (150 MB / 250 MB) derived from a single unvalidated growth estimate (~2 MB/release); a sudden large-blob addition could skip the early-warning band and hit the hard-fail without warning | Assumption | Medium | Major | P1 | Evidence Quality |
| PM-005-IT3-0626 | REQ-036 blank-input fallback (`git tag -l … | head -1`) resolves pre-release tags before the allow-list filter; non-obvious edge cases left undocumented in acceptance criteria, causing implementer misinterpretation | Technical | Low | Major | P1 | Completeness |
| PM-006-IT3-0626 | Monitor workflow infrastructure failure (API rate limit, network error) causes silent detection gap — requirements specify behavior on mismatch but not on monitor-self-failure | Process | Medium | Major | P1 | Actionability |
| PM-007-IT3-0626 | ADR-002 build-status precondition ("require CI validation to pass before SHA is published") has no backing SHALL requirement — the same ADR-prose-vs-requirements gap IT3-001 targeted but missed | Process | Low | Major | P1 | Traceability |
| PM-008-IT3-0626 | Orphan-branch flip procedure (activated when size-pack > 250 MB) has no backing requirement, story, or approval process — CI hard-fail leaves skeleton stale until manual intervention | Resource | Low | Minor | P2 | Actionability |

---

## Detailed Findings

### PM-001-IT3-0626: Detection SLA (≤ Daily) Permits Executable-Hook Compromise Window [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | Technical |
| **Likelihood** | High — any repository collaborator can direct-push to the unprotected branch; GitHub push-event delivery is best-effort, not guaranteed (ADR-002 acknowledges this explicitly) |
| **Affected Dimension** | Methodological Rigor |
| **Priority** | P0 |

**Evidence:**

ADR-002 §Continuous Integrity Monitoring states: "Detection latency for the exact tamper event is therefore ≈ Actions scheduling latency (seconds–minutes)… Scheduled backstop: the **guaranteed** worst-case detection window equals **one scheduled interval**; this ADR sets the interval at **≤ 24 hours (daily)**."

ADR-002 §Risks table (R-007b): "Direct-push attack: repository collaborator pushes directly to unprotected cowork-skeleton branch… blast radius includes **executable hooks** on user workstations (IT3-007)…"

NFR-006 sets "≤ daily cadence" as the tamper-detection SLA. No requirement specifies a tighter SLA even for the executable-hook risk class. No risk-acceptance decision document is referenced for the 24 h window.

**Analysis:**

The requirements correctly identify that `cowork-skeleton` ships **executable hooks** to user workstations (`hooks/session-start.py`, pre-tool/stop gate scripts). A tamper event that occurs one second after a successful scheduled monitor run persists for up to 23 h 59 m before the next scheduled assert fires. During this window, any user who runs `claude plugin marketplace add geekatron/jerry@cowork-skeleton` receives the tampered hooks, which execute automatically at session start.

ADR-002 acknowledges this as "DETECTION, not prevention" and notes "residual exposure = up to one SLA interval." However, neither ADR-002 nor the requirements document contains a formal risk-acceptance decision recording that the 24 h executable-hook exposure window is acceptable. The R-007b risk row rates the consequence at C=4 (Major) with a note "pending Phase-2 STRIDE re-analysis for potential C=5 upgrade" — meaning the consequence rating used to accept the 24 h SLA may itself be understated.

There is also no documented SLA-reduction path. ADR-002 offers "prevention: branch protection" as the upgrade but gives no trigger condition for escalating from the 24 h detection posture. If Phase-2 STRIDE concludes C=5, the 24 h SLA is the fallback with no pre-designed tighter-SLA option.

**Mitigation:**

Add a formal risk-acceptance record to ADR-002 (or a Phase-2 entry) that: (a) states the exact accepted detection window (24 h) for the executable-hook threat class; (b) specifies the trigger condition that escalates from detection to prevention (branch protection); and (c) documents an intermediate SLA-tightening option such as increasing scheduled cadence to 4 h or 6 h pending Phase-2 STRIDE.

**Acceptance Criteria:** ADR-002 §Continuous Integrity Monitoring contains an explicit risk-acceptance table with: accepted detection window (hours), justification, and a named trigger condition for escalation to branch-protection prevention. NFR-006 cron expression is tightened or documents the accepted 24 h interval explicitly.

---

### PM-002-IT3-0626: Smoke-Test Deferral Creates Permanently Open Strategy Falsification Gap [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | Process |
| **Likelihood** | Medium — deferred items frequently become never-executed items in practice; the deferral condition ("CoWork runtime unavailable before Phase 2") has no enforcement mechanism |
| **Affected Dimension** | Completeness |
| **Priority** | P0 |

**Evidence:**

R-001 §Verification Approach (phase1-requirements.md, line 60): "dimension (d) MAY be deferred to Phase 4 if a CoWork runtime is unavailable before Phase 2; the artifact SHALL record 'DEFERRED — required before Phase 5' and Phase 5 is blocked until completed."

R-001 statement (phase1-requirements.md, line 57): "The entire skeleton strategy depends on it."

ADR-001 §Decisive Framing: "A Claude Code plugin install **clones the branch and materializes its working tree at the tip commit**… Therefore the only thing that affects the installed file count is **the tree at the branch tip** — not whether `projects/` ever existed in history… This single fact removes any reason to rewrite history."

REQ-034 AC (phase1-requirements.md, line 216): "dimension (d) documented result of `claude plugin marketplace add geekatron/jerry@cowork-skeleton` in a CoWork-compatible runtime (PASS = plugin loads within 120 s; FAIL = error or timeout; 'DEFERRED — required before Phase 5' if CoWork client unavailable before Phase 2)"

**Analysis:**

The R-001 §Verification Approach explicitly states dimension (d) "is the only dimension that directly falsifies the decisive framing in ADR-001." The decisive framing is the spine of the entire project strategy — if CoWork does not materialize the tip working tree (e.g., it counts uncompressed objects, git history depth, or local working directory), branch-stripping is the wrong lever.

Dimensions (a), (b), and (c) are all proxies. They verify: the tracked file count is under 5,000, the pack is under 250 MB, and the clone is under 120 s. None of them verify that CoWork itself accepts the installation. A repository could pass all three proxy dimensions and still fail CoWork's actual (undocumented) limit mechanism.

With the deferral explicitly permitted, Phases 2, 3, and 4 can proceed and complete before dimension (d) is tested. If the smoke test then fails — because the decisive framing is wrong — Phases 2–4 deliverables may all need revision or abandonment. There is no contingency plan for this scenario in the requirements: the fallback (pivot to local-plugin configuration) is mentioned only in R-001 §Fallback with no Phase-2 requirements or implementation plan.

Additionally, "Phase 5 is blocked until completed" relies entirely on process discipline. There is no automated gate — no CI check, no schema validation, no required artifact hash — that prevents Phase 5 from starting with a DEFERRED dimension (d).

**Mitigation:**

(1) Reduce the deferral window: dimension (d) SHALL be completed before Phase 3 begins (not Phase 4), giving time to pivot before the majority of implementation work. (2) Add an automated gate: Phase 3's ORCHESTRATION_PLAN.md quality gate SHALL reference `verification/R001-clean-clone-count.md` and fail QG-2 if dimension (d) is marked DEFERRED. (3) Add a Phase-2 contingency stub requirement: if dimension (d) fails, REQ-034-fallback SHALL define the scope-change escalation procedure (H-02 user decision, scope pivot requirements).

**Acceptance Criteria:** `verification/R001-clean-clone-count.md` is present with a PASS for dimension (d) before Phase 3 QG entry. If dimension (d) is DEFERRED after Phase 1 QG, a blocking Phase-2 item exists in the orchestration plan. ORCHESTRATION_PLAN.md Phase 3 gate explicitly checks dimension (d) completion status.

---

### PM-003-IT3-0626: Event-Driven Monitor Does Not Fire on Branch-Delete-and-Recreate Tamper [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Technical |
| **Likelihood** | Low — requires elevated permissions to delete a branch; however the branch is explicitly unprotected |
| **Affected Dimension** | Internal Consistency |
| **Priority** | P1 |

**Evidence:**

REQ-035 (phase1-requirements.md, line 151): "Event-driven fast path — on `on: push: branches: [cowork-skeleton]` (which fires on direct/non-CI pushes but NOT on `GITHUB_TOKEN`-made CI pushes)…"

ADR-002 §Continuous Integrity Monitoring: "whereas a **non-CI direct push** (the RT-01 actor, using their own credentials) **does** fire it."

REQ-021 (phase1-requirements.md, line 148): "`cowork-skeleton` branch SHALL be configured as a CI-owned, unprotected branch."

ADR-002 L0 Executive Summary: "Detection latency for the exact tamper event is therefore ≈ Actions scheduling latency (seconds–minutes)."

**Analysis:**

The deliverables claim the event-driven leg provides "seconds–minutes" detection for direct-push tampering. However, GitHub's `on: push: branches: [cowork-skeleton]` event fires only on push operations. If a threat actor deletes the `cowork-skeleton` branch entirely and recreates it (via `git push origin :cowork-skeleton` then `git push origin malicious:cowork-skeleton`), GitHub generates a `delete` event followed by a `create` event — not a `push` event. The monitor's `on: push` trigger does not fire.

The unprotected branch posture (REQ-021, ADR-002 Decision) means any collaborator with `contents: write` access can delete and recreate the branch. The "non-fast-forward" and "deletion" rules in the repo's only active ruleset target `~DEFAULT_BRANCH` (main), not `cowork-skeleton`.

In this scenario, detection falls back entirely to the scheduled ≤ daily backstop. The claim of "seconds–minutes" detection is correct for a force-push tamper but false for a delete-and-recreate tamper. This inconsistency could mislead Phase-2 STRIDE into accepting a stronger tamper-detection posture than actually exists.

**Mitigation:**

Add `on: delete` and `on: create` event triggers to the monitor workflow covering the `cowork-skeleton` branch, alongside the `on: push` trigger. Document in REQ-035 and NFR-006 that the event-driven leg covers push, delete, and create events. Update ADR-002's detection-latency claim to be specific about which tamper vectors achieve "seconds–minutes" detection.

**Acceptance Criteria:** NFR-006 AC functional test (2) includes a branch-delete-and-recreate scenario (not just a direct push) and confirms the event-driven leg fires within minutes. REQ-035 requirement text lists `push`, `delete`, and `create` events.

---

### PM-004-IT3-0626: Clone-Weight Thresholds Derived from Single Unvalidated Growth Estimate [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Assumption |
| **Likelihood** | Medium — the ~2 MB/release figure is described as "empirical" but is not measured across multiple releases; large binary additions to retained directories could cause sudden growth |
| **Affected Dimension** | Evidence Quality |
| **Priority** | P1 |

**Evidence:**

ADR-001 §Clone-Weight Decision: "every release adds ~1 commit plus accumulated history (empirically ~2 MB/release on this repo)."

REQ-034d (phase1-requirements.md, line 206): "The workflow SHALL exit non-zero and abort the release if `size-pack:` exceeds **250 MB**."

REQ-034d: "SHALL open a GitHub issue as a **non-blocking early warning** when `size-pack:` exceeds **150 MB** (~60% of the 250 MB trigger, approximately 40 s clone time at 10 Mbps reference)."

ADR-001 Consequences §Negative: "every release adds to it (~2 MB/release empirically)"

**Analysis:**

The ~2 MB/release growth rate appears in both ADR-001 and REQ-034d as the empirical basis for the thresholds. However, this figure is derived from a single data point ("empirically") with no source citation, no measured history span, and no accounting for the variability of git commit sizes. Commits that add large binary test fixtures, generated assets, or model files to retained directories (e.g., `skills/*/test_data/`, `src/`) could cause the pack to grow by 30–100 MB in a single release.

The consequences of threshold mis-calibration:
- **Wrong-field measurement:** If the CI implementation measures `size:` (loose objects) instead of `size-pack:` (packed history), the check is measuring the wrong quantity. The two fields appear adjacent in `git count-objects -vH` output and are easily confused. REQ-034d specifies `size-pack:` but the acceptance criteria do not include a field-name verification test.
- **Early-warning band too close to the hard-fail:** 150 MB is 60% of 250 MB, but if growth spikes by 100 MB in one release (e.g., large skills/transcript/test_data/ additions), the pack jumps from 100 MB to 200 MB, bypassing the 150 MB early-warning opportunity and approaching the 250 MB hard-fail with only one release of advance notice.
- **Reference network assumption:** The 40-second estimate at 10 Mbps is described as "approximately 30th percentile global broadband." CoWork users on lower-bandwidth connections (mobile, satellite) may hit the 120-second timeout at much lower pack sizes than 250 MB. The requirements do not address this.

**Mitigation:**

(1) Add a verification step in REQ-034d's acceptance criteria that explicitly checks the field name: "Inspect the workflow `git count-objects -vH` step to confirm it extracts the line matching `size-pack:` (not `size:`)." (2) Document the empirical basis for ~2 MB/release with a measurement history (at least 3 releases). (3) Add a requirement that the R-001 artifact (REQ-034) records baseline `size-pack:` so future per-release deltas can be compared. (4) Add a graduated warning: open a GitHub issue when growth in a single release exceeds 20 MB (a sudden-spike signal independent of absolute thresholds).

**Acceptance Criteria:** REQ-034d acceptance criteria include a field-name inspection test. `verification/R001-clean-clone-count.md` records the baseline `size-pack:` value. The CI implementation grep for the field includes the colon (`size-pack:`) to prevent false matching of `size:`.

---

### PM-005-IT3-0626: REQ-036 Blank-Input Fallback Has Undocumented Pre-Release Tag Edge Cases [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Technical |
| **Likelihood** | Low — pre-release tags are not the current release pattern, but the edge case creates implementer ambiguity regardless |
| **Affected Dimension** | Completeness |
| **Priority** | P1 |

**Evidence:**

REQ-036 (phase1-requirements.md, line 152): "when `inputs.target_tag` is blank — from `git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=-version:refname | head -1`"

ADR-001 §Regeneration Commit Determinism blank-input fallback (line 247): `TAG="$(git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=-version:refname | head -1)"`

REQ-036 allow-list: `^v[0-9]+\.[0-9]+(\.[0-9]+)?$`

REQ-036 AC (phase1-requirements.md, line 165): "(e) `workflow_dispatch` run with blank `inputs.target_tag` resolves to the most recent `v*` semantic-version tag and proceeds normally."

**Analysis:**

The glob pattern `v[0-9]*.[0-9]*.[0-9]*` in the fallback command matches `v1.0.0-rc.1` because the glob does not anchor at end of string. The sort (`--sort=-version:refname`) then places pre-release tags in an implementation-defined position relative to release tags (git's `version:refname` sort treats `v1.0.0-rc.1` as less than `v1.0.0`, so it would not appear as `head -1` normally — but edge behavior with `--sort=-version:refname` and pre-release suffixes varies by git version).

The allow-list `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` correctly rejects `v1.0.0-rc.1` (the hyphen is not in the pattern). So the workflow exits non-zero without pushing. This is the correct security behavior — but it leaves `cowork-skeleton` stale with no diagnostically clear error message about WHY the workflow failed (the error would be "tag fails the v* allow-list" — not "a pre-release tag was resolved; use explicit inputs.target_tag").

A second edge case: if the repository has NO `v*` tags yet, `head -1` returns an empty string. The allow-list check then tests `""` against `^v[0-9]+\.[0-9]+(\.[0-9]+)?$`, fails, and exits non-zero. This is correct but produces an opaque error for a common initial state.

Neither edge case is documented in REQ-036's acceptance criteria, creating implementation ambiguity.

**Mitigation:**

Add two acceptance criteria to REQ-036: "(f) `workflow_dispatch` with blank `inputs.target_tag` when the repository's most-recent tag is a pre-release tag (e.g., `v1.1.0-rc.1`): the workflow exits non-zero with an error message that explicitly states 'resolved tag is not a release tag; use explicit inputs.target_tag'; no push is made. (g) `workflow_dispatch` with blank `inputs.target_tag` when no `v*` tags exist: the workflow exits non-zero with an error message 'no release tags found'; no push is made." Also add a note in REQ-036 rationale documenting the two edge cases.

**Acceptance Criteria:** REQ-036 ACs include items (f) and (g). CI implementation includes a guard for empty `$TAG` before the allow-list check. Error messages are distinct from the generic allow-list failure to enable rapid diagnosis.

---

### PM-006-IT3-0626: Monitor Workflow Self-Failure Produces Silent Detection Gap [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Process |
| **Likelihood** | Medium — CI transient errors (API rate limits, network timeouts, GitHub API outages) occur regularly; the monitor is a long-running workflow with external dependencies |
| **Affected Dimension** | Actionability |
| **Priority** | P1 |

**Evidence:**

NFR-006 (phase1-requirements.md, line 230): "On ANY mismatch from either check, the workflow SHALL: **(a)** create a GitHub issue… AND **(b)** exit non-zero."

REQ-035 monitor behavior (phase1-requirements.md, line 151): "retrieve the published SHA from the Release notes and assert `git rev-parse cowork-skeleton` equals it; mismatch SHALL create a GitHub issue and exit non-zero."

ADR-002 §Continuous Integrity Monitoring: "Mandatory floor: **detect-and-alert** — on mismatch, open a GitHub issue and fail the run loudly (requires `issues: write`, IN-003)."

**Analysis:**

NFR-006 and REQ-035 specify the monitor's behavior on **mismatch** (tampered or stale branch). They do not specify the monitor's behavior on **self-failure** — when the monitor's own infrastructure fails before it can complete the comparison:

- `gh release view v{TAG} --json body` fails with a 403 (API rate limit) or 404 (no Release exists for this tag if the CI publish step failed earlier) — what does the monitor do?
- `git clone cowork-skeleton` times out (transient network issue) — what does the monitor do?
- `git rev-parse cowork-skeleton` returns non-zero (branch deleted) — what does the monitor do?

In none of these cases is a "mismatch" detected, so the requirements' SHALL clause does not trigger. The monitor can exit with code 0 (success) while having failed to perform the integrity check. This means three consecutive self-failures produce a silent detection gap of up to three days — the tamper-exposure window becomes unbounded in practice.

The requirements Quality Checklist (line 248) states "NFR-006 dual-check explicitly names two complementary failure modes" but neither failure mode is "the monitor itself fails." This is a specification gap.

**Mitigation:**

Add a requirement (or AC to NFR-006): "If the monitor workflow fails to complete either check due to an infrastructure error (API failure, clone timeout, branch not found), the workflow SHALL exit non-zero and SHALL emit a GitHub issue or `$GITHUB_STEP_SUMMARY` annotation indicating 'monitoring failed — integrity cannot be confirmed; manual verification required.'" Additionally, add `on: workflow_run` monitoring of the NFR-006 workflow itself so consecutive failures (N >= 2) generate an escalation alert.

**Acceptance Criteria:** NFR-006 AC includes a fifth functional test: "(5) Monitor self-failure — simulate a `gh release view` 403 error; confirm the monitor exits non-zero and emits a diagnostic annotation; confirm it does NOT exit zero silently."

---

### PM-007-IT3-0626: ADR-002 Build-Status Precondition Has No Backing SHALL Requirement [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Process |
| **Likelihood** | Low — the gap is specifically about a broken-but-correctly-SHA'd regeneration being advertised; requires CI to complete the generation step but fail a validation step |
| **Affected Dimension** | Traceability |
| **Priority** | P1 |

**Evidence:**

ADR-002 §Continuous Integrity Monitoring (line 238): "**Build-status precondition (R-007).** Require the build/validation CI status to pass before the expected SHA is published, so a broken (but correctly-SHA'd) regeneration is never advertised."

ADR-002 §Compensating Controls table (lines 243–254): CC-1 through CC-8 are listed with backing requirements. There is no CC entry for the build-status precondition. It appears only in a separate prose paragraph below the CC table.

Requirements §S-010 Self-Refine Iteration 3 (line 437): "[x] Every ADR-002 CC traces to at least one SHALL requirement"

**Analysis:**

IT3-001 was specifically designed to close the ADR-prose-vs-requirements gap. The requirements Quality Checklist self-certifies that "every ADR-002 CC traces to at least one SHALL requirement." However, the build-status precondition in ADR-002 was not assigned a CC number (CC-1 through CC-8) — it appears as an unnumbered prose paragraph following the CC table, outside the scope of the IT3-001 gap-closure sweep.

The practical consequence: the SHA publication step (REQ-035) could execute and publish the expected SHA even when the workflow's file-count assertion (REQ-006), plugin-surface validation (REQ-005/REQ-010), or pre-push equivalence check (REQ-022) has failed. This would advertise a SHA corresponding to a broken skeleton, and the integrity monitor would then assert that the broken skeleton is "correct" — a false negative for the quality gate.

The self-certifying checklist at line 437 "[x] Every ADR-002 CC traces to at least one SHALL requirement" is technically true (CC-1 through CC-8 all have traces) but misses this unnumbered precondition.

**Mitigation:**

Add the build-status precondition to ADR-002's CC table as CC-9. Add a corresponding requirement to WS-3: "REQ-038: The `cowork-skeleton.yml` workflow SHALL publish the expected deterministic SHA to the GitHub Release notes (REQ-035 CC-1) ONLY if and ONLY after all validation steps (REQ-005, REQ-006, REQ-010, REQ-022) have exited with code 0 in the same job run; the SHA publish step SHALL be positioned after all validation steps with an explicit `if: success()` condition or as the final step in a dedicated 'all-checks-passed' job." Add CC-9 to the Requirements Quality Checklist trace.

**Acceptance Criteria:** `cowork-skeleton.yml` has the SHA publish step annotated `if: success()` or positioned in a job that only runs on success. A test run where REQ-006 (file-count assertion) fails confirms no Release-notes publish occurs. REQ-038 appears in ADR-002 CC table and in WS-3 requirements.

---

### PM-008-IT3-0626: Orphan-Branch Flip Procedure Has No Backing Requirement [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Category** | Resource |
| **Likelihood** | Low — the 250 MB hard-fail trigger is estimated to be 100+ releases (~1–3 years) away at the current growth rate |
| **Affected Dimension** | Actionability |
| **Priority** | P2 |

**Evidence:**

ADR-001 §Clone-Weight Decision: "**Flip to Option B** — one-line change (`git checkout --orphan` instead of branch-from-tag); integrity-neutral post-IT3-004 | on warning-band breach or R-001 empirical pressure | constant-weight orphan becomes the new default."

REQ-034d hard-fail: "The workflow SHALL exit non-zero and abort the release if `size-pack:` exceeds **250 MB**."

No STORY, TASK, or requirement in phase1-requirements.md addresses the flip procedure itself.

**Analysis:**

When the 250 MB hard-fail triggers, `cowork-skeleton.yml` exits non-zero and does not update the branch. Users are then stuck at the prior release's skeleton indefinitely until a human intervenes. The "one-line change" in ADR-001 is technically accurate, but it requires: (a) human decision to execute the flip, (b) understanding which specific change to make, (c) testing the orphan variant, (d) re-running the workflow. None of these steps have a corresponding requirement, story, or defined escalation path.

The early-warning band (150 MB GitHub issue) is non-blocking and could be ignored. There is no requirement specifying how many warning cycles may pass before the flip becomes mandatory.

**Mitigation:**

Add a minor requirement to WS-5 or Risk Implications: "R-002-FLIP: If `cowork-skeleton.yml` emits a 150 MB early-warning issue for three consecutive releases, the maintainer SHALL create a TASK to execute the orphan-branch flip (ADR-001 Option B) in the following release cycle." Document the flip procedure in the Reference documentation (REQ-028 extension). This converts an ADR prose note into a traceable, actionable trigger.

**Acceptance Criteria:** Reference documentation includes a "Clone Weight Management" section with the flip procedure. R-002-FLIP criterion appears in Risk Implications with a defined trigger count.

---

## Recommendations

### P0 — Critical (MUST mitigate before QG-1 passage)

| ID | Mitigation Action | Acceptance Criterion |
|----|-------------------|---------------------|
| PM-001-IT3-0626 | Add explicit risk-acceptance record to ADR-002 for the 24 h executable-hook exposure window; specify trigger condition for escalation to branch-protection prevention; document intermediate SLA-tightening option (4 h or 6 h cadence) | ADR-002 contains a risk-acceptance table with: accepted window, justification, escalation trigger |
| PM-002-IT3-0626 | Tighten deferral deadline to Phase 3 (not Phase 4); add automated gate to QG-2 checking dimension (d) status; add Phase-2 contingency stub requirement for pivot scenario | Dimension (d) appears in ORCHESTRATION_PLAN.md Phase 3 gate; QG-2 fails if marked DEFERRED |

### P1 — Important (SHOULD mitigate before Phase 2 begins)

| ID | Mitigation Action | Acceptance Criterion |
|----|-------------------|---------------------|
| PM-003-IT3-0626 | Add `delete` and `create` event triggers to the NFR-006 monitor alongside `push`; add a functional test for branch-delete-and-recreate tamper | NFR-006 AC test (2) covers delete-and-recreate; monitor yaml includes `on: delete/create: branches: [cowork-skeleton]` |
| PM-004-IT3-0626 | Add field-name inspection test to REQ-034d AC; document empirical basis for ~2 MB/release; add sudden-spike early warning at single-release delta > 20 MB | REQ-034d AC specifies `grep '^size-pack:'`; `R001-clean-clone-count.md` records baseline pack |
| PM-005-IT3-0626 | Add REQ-036 ACs for pre-release tag and no-tags edge cases; add distinct error messages for each | REQ-036 ACs include items (f) and (g) |
| PM-006-IT3-0626 | Add NFR-006 AC for monitor self-failure: workflow exits non-zero and emits diagnostic; add `on: workflow_run` escalation for consecutive monitor failures | NFR-006 AC test (5) covers API failure scenario |
| PM-007-IT3-0626 | Add REQ-038 (build-status precondition); add CC-9 to ADR-002 CC table; SHA publish step conditioned on `if: success()` | REQ-038 appears in WS-3; ADR-002 CC table contains CC-9; test run confirms no SHA publish on validation failure |

### P2 — Monitor (MAY mitigate; acknowledge risk)

| ID | Mitigation Action | Acceptance Criterion |
|----|-------------------|---------------------|
| PM-008-IT3-0626 | Add flip-procedure documentation to Reference docs; add R-002-FLIP trigger (3 consecutive early warnings) to Risk Implications | Reference doc contains clone-weight section; Risk Implications contains R-002-FLIP row |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-002: REQ-034 dimension (d) deferral leaves the strategy's core assumption unverified throughout Phases 2–4; PM-007: build-status precondition has no backing requirement despite IT3-001 gap-closure sweep; PM-005: REQ-036 edge cases undocumented in ACs |
| Internal Consistency | 0.20 | Negative | PM-003: deliverables claim "seconds–minutes" event-driven detection but some tamper vectors (delete-and-recreate) fall back to 24 h, overstating coverage; ADR-002 detection-latency claim requires qualification |
| Methodological Rigor | 0.20 | Negative | PM-001: 24 h detection SLA accepted for executable-hook threat class without a formal risk-acceptance record or SLA-reduction path; PM-006: monitor self-failure scenario not addressed in the methodology |
| Evidence Quality | 0.15 | Negative | PM-004: ~2 MB/release growth rate is stated as empirical but has no measurement history; `size-pack:` field specification not verified in REQ-034d AC; clone-time estimate uses a reference bandwidth with no measured baseline |
| Actionability | 0.15 | Negative | PM-006: creator cannot implement correct monitor self-failure behavior without additional specification; PM-007: build-status precondition has no implementation path; PM-008: flip procedure undefined |
| Traceability | 0.10 | Negative | PM-007: ADR-002 §Build-status precondition (R-007) is unnumbered prose outside the CC-1 through CC-8 table and has no backing requirement — the same gap pattern IT3-001 targeted; self-certifying checklist missed it |

**Overall Assessment:** REVISE. Eight findings (2 Critical, 5 Major, 1 Minor) indicate meaningful gaps in the iteration-3 controls. The Critical findings are the tamper-exposure SLA (PM-001) and the smoke-test deferral falsification gap (PM-002), both of which must be addressed before QG-1 passage. The Major findings are implementer-facing ambiguities and specification omissions concentrated in the new requirements (REQ-035/036/037, NFR-006) introduced in iteration 3 — these are precisely the requirements most at risk of being built wrong or skipped due to under-specification.

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 2 (PM-001-IT3-0626, PM-002-IT3-0626)
- **Major:** 5 (PM-003 through PM-007-IT3-0626)
- **Minor:** 1 (PM-008-IT3-0626)
- **Protocol Steps Completed:** 6 of 6
- **H-16 Status:** Compliant (S-003 confirmed in all three deliverable footers)
- **H-15 Self-Review:** Applied before persistence — all findings have specific evidence, severity justified per template criteria, identifiers follow PM-{NNN}-IT3-0626 format, summary table matches detailed findings, no findings omitted or minimized per P-022

---

*Strategy: S-004 Pre-Mortem Analysis*
*Template: .context/templates/adversarial/s-004-pre-mortem.md (v1.0.0)*
*Deliverables reviewed:*
*  — projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md (iteration 3)*
*  — projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md (iteration 3)*
*  — projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md (iteration 3)*
*Grounding (read-only): projects/PROJ-031-cowork-skeleton/research/phase1-skeleton-ci-research.md, PLAN.md*
*Executed: 2026-06-26*
*Reviewer: jerry:adv-executor (Group C — Challenge; blind, independent)*
*Finding prefix: PM-NNN-IT3-0626*
