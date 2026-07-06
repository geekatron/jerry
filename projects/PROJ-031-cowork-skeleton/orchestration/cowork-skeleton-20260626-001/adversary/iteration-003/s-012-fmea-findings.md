# FMEA Report: PROJ-031 CoWork Skeleton — Phase 1 Deliverables (Iteration 3)

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverables:** `requirements/phase1-requirements.md` · `decisions/ADR-001-skeleton-derived-branch-strategy.md` · `decisions/ADR-002-ci-token-push-strategy.md`
**Criticality:** C4
**Date:** 2026-06-26
**Reviewer:** adv-executor (jerry:adv-executor, claude-sonnet-4-6)
**H-16 Compliance:** S-003 Steelman applied before this adversarial sequence (prior iterations confirmed)
**Execution ID:** it3-20260626
**Elements Analyzed:** 11 | **Failure Modes Identified:** 16 | **Total RPN:** 1,611

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Element Inventory](#element-inventory) | 11 analyzed elements across all three deliverables |
| [Summary](#summary) | Overall assessment and trend vs. prior iterations |
| [Findings Table](#findings-table) | 16 failure modes, RPN-sorted with S/O/D ratings |
| [Finding Details](#finding-details) | Expanded evidence for Critical and Major findings |
| [Recommendations](#recommendations) | Prioritized corrective actions with post-correction RPN estimates |
| [Scoring Impact](#scoring-impact) | S-014 dimension assessment |
| [Execution Statistics](#execution-statistics) | Count summary |

---

## Element Inventory

MECE decomposition of the three deliverables into 11 analyzable elements:

| ID | Element | Deliverable | Section |
|----|---------|-------------|---------|
| E1 | R-001 Four-Dimensional Verification Gate (REQ-034) | Requirements | WS-5 |
| E2 | REQ-035 Integrity Monitor Architecture (Publish + Event-driven + Scheduled) | Requirements | WS-3 |
| E3 | REQ-036 Tag-name Sanitization (event-discriminated resolution, allow-list, env: binding) | Requirements | WS-3 |
| E4 | REQ-037 + REQ-022 Push-Failure Detection and Pre-push Diff Gate | Requirements | WS-3 |
| E5 | REQ-034d Clone-Weight Telemetry (per-release emit, hard-fail, early warning) | Requirements | WS-5 |
| E6 | NFR-006 Staleness + Tamper-Detection Dual-Check (weekly staleness / daily tamper) | Requirements | NFR |
| E7 | ADR-001 Clone-Weight Decision (Option A default + continuous monitoring thresholds) | ADR-001 | Clone-Weight Decision |
| E8 | ADR-001 Idempotency Proof (commit determinism, metadata pinning, TAG resolution logic) | ADR-001 | Regeneration Commit Determinism |
| E9 | ADR-002 Continuous Integrity Monitoring (publish-then-assert, non-forgeable comparator) | ADR-002 | Branch-Protection Posture § |
| E10 | ADR-001 Canonical Plugin-Retention Surface (8 directories, marketplace.json, REQ-005 mirror) | ADR-001 | Canonical Plugin-Retention Surface |
| E11 | ADR-002 Loop-Safety Argument (three independent guarantees) | ADR-002 | Loop-Safety Argument |

---

## Summary

Eleven elements and 16 failure modes were identified and rated. The single Critical finding (FM-01, RPN 216) surfaces a trust-model gap in the publish-then-assert integrity architecture: the GitHub Release notes used as the reference anchor are writable by any repository collaborator with `write` access — the same permission level required to push to the unprotected `cowork-skeleton` branch. A coordinated attacker can update both simultaneously, defeating the tamper-detection system. This was not raised in prior iterations because the publish-then-assert architecture itself was introduced in iteration 3; it is the first time it can be analyzed as a failure mode.

Ten Major findings (RPN 90–196) include: monitor self-failure (no meta-monitoring), smoke-test circular dependency on Phase 5, detection-SLA window for executable hooks (24 h guaranteed worst case), permission-scope gaps for the monitor workflow, clone-weight threshold calibration on a 10 Mbps reference, early-warning non-binding status, ambiguous pre-push diff gate reference, event-discriminated TAG resolution implementation complexity, and publish-step failure leaving the reference anchor unestablished.

Five Minor findings cover trailing-forgeable staleness signal, blank-input fallback edge cases, tag immutability precondition, marketplace.json content verification, and REQ-005 / ADR-001 c-003 synchronization drift risk.

Total RPN 1,611 shows continued downward trend (iteration 1: 3,207 → iteration 2: 2,087 → iteration 3: 1,611), confirming that the ADR→REQ gap closure (REQ-035/036/037, NFR-006 dual-check) removed the highest-probability-of-occurrence failure modes from prior iterations. Remaining risk is concentrated in the newly introduced continuous-monitoring architecture. **Assessment: REVISE** — the Critical finding requires architectural remediation before Phase 5; the five Major findings rated RPN ≥ 120 require corrective action before Phase 6.

---

## Findings Table

Sorted by RPN (highest first). Execution ID suffix: `-it3`.

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-01-it3 | E2/E9 REQ-035 Reference Anchor | Release notes writable by the same write-level threat actor who can push to the unprotected branch; coordinated update of both defeats the publish-then-assert model entirely | 9 | 3 | 8 | 216 | Critical | Store expected SHA in an immutable surface only CI's GITHUB_TOKEN can write (e.g., a commit to a separate protected branch, or a cryptographically signed artifact); explicitly document that Release notes MUST NOT be edited manually by any collaborator | Evidence Quality, Internal Consistency |
| FM-06-it3 | E2/E6 NFR-006 Monitor Self-Failure | Scheduled cron unreliability or permission error causes the NFR-006 monitor to fail silently; no meta-monitoring exists to detect monitor failure; SLA is breached without alert | 7 | 4 | 7 | 196 | Major | Add a meta-monitor: a separate daily job that asserts the NFR-006 monitor produced a successful run within the last 25 h; alert via GitHub issue if not | Completeness, Methodological Rigor |
| FM-02-it3 | E6 NFR-006 Detection SLA | Guaranteed worst-case tamper-detection window is ≤ 24 h; during this interval a tampered branch shipping malicious executable hooks (session-start.py) is installable by any CoWork user | 8 | 3 | 6 | 144 | Major | Reduce the scheduled backstop cadence from ≤ daily to ≤ hourly; the event-driven leg already provides near-real-time detection for direct-push events but is best-effort | Methodological Rigor, Evidence Quality |
| FM-07-it3 | E2/E6 Permission-Scope Gaps | Monitor workflow's `issues: write` permission may be missing, misconfigured, or revoked by an org policy change; if absent the workflow may fail-open (no issue created) or fail silently | 6 | 4 | 6 | 144 | Major | Add CI lint rule: grep for `issues: write` in the monitor workflow; add an integration test that confirms an issue IS created when mismatch is injected | Completeness, Actionability |
| FM-04-it3 | E5/E7 Clone-Weight Threshold Calibration | The 250 MB hard-fail and 150 MB early-warning thresholds are calibrated to 10 Mbps (≈ 30th-percentile global broadband); VPN, mobile, and sub-10 Mbps connections will hit the 120 s git timeout at lower pack sizes | 6 | 4 | 6 | 144 | Major | Recalibrate thresholds using a 5 Mbps (≈ 20th-percentile) reference; document the reference bandwidth in the threshold definitions; add a second telemetry dimension at 5 Mbps simulated clone time | Evidence Quality, Actionability |
| FM-03-it3 | E1 Smoke-Test Circular Dependency | REQ-034 dimension (d) — the only direct falsification test for CoWork installability — is explicitly allowed to defer to Phase 4; if Phase 5 proceeds without dimension (d) completing, three phases of design and implementation rest entirely on proxy measurements | 8 | 4 | 4 | 128 | Major | Add an automated Phase-5 pre-execution gate: a CI check that reads `verification/R001-clean-clone-count.md` and refuses to proceed (non-zero exit) unless dimension (d) shows `PASS` (not `DEFERRED`); this converts a human-enforced gate to a machine-enforced gate | Completeness, Traceability |
| FM-13-it3 | E5/E7 Early-Warning Non-Binding | The 150 MB non-blocking early warning opens a GitHub issue but does not fail the release and has no SLA for human response; maintainers may defer the Option B flip until the hard 250 MB trigger, leaving users exposed to clone timeouts in the interim | 5 | 4 | 6 | 120 | Major | Assign the early-warning GitHub issue to a named maintainer with a P-002 response SLA; or escalate: convert early warning to blocking at 200 MB (leaving a 50 MB buffer before the hard fail) | Actionability, Completeness |
| FM-09-it3 | E4 Pre-push Diff Gate Reference Ambiguity | REQ-022 AC specifies `git diff v{N}..cowork-skeleton -- ':!projects/'` using the branch name; in the generation workflow, `cowork-skeleton` may resolve to the REMOTE old tip rather than the LOCAL generated content (HEAD); the gate could silently compare the wrong refs | 5 | 4 | 5 | 100 | Major | Update REQ-022 AC to specify `git diff v{N}..HEAD -- ':!projects/'` explicitly; add a CI unit test that injects a divergent file and confirms the gate triggers (currently Demonstration-only) | Methodological Rigor, Actionability |
| FM-14-it3 | E8 TAG Resolution Complexity | The event-discriminated TAG resolution (3-branch if/else: `push:tags` vs. `workflow_dispatch` + `inputs.target_tag` vs. blank-fallback `git tag -l`) is complex; an implementation error in any branch could silently resolve to the wrong source ref without failing the allow-list | 6 | 4 | 4 | 96 | Major | Add an explicit integration test for each of the three branches (push:tags, workflow_dispatch+input, blank-fallback); assert that each branch resolves to the intended tag; CI runs all three before any release | Internal Consistency, Methodological Rigor |
| FM-11-it3 | E9 Publish Step Failure | If `gh release edit` (the REQ-035 publish leg) fails — due to a permissions error, API rate limit, or GitHub outage — the reference anchor for the new release is never established; the scheduled monitor may then compare the live SHA against a stale prior release's SHA, producing false positives or false negatives | 6 | 3 | 5 | 90 | Major | Add an explicit post-publish verification step: after `gh release edit`, retrieve the release notes and grep for the just-published `cowork-skeleton-sha:` field; fail the job if the field is absent or mismatched | Completeness, Internal Consistency |
| FM-15-it3 | E10 REQ-005 / ADR-001 c-003 Sync Drift | ADR-001 c-003 is declared the SSOT; REQ-005 mirrors it verbatim; future maintenance could diverge the two without a machine-enforced consistency check | 5 | 3 | 5 | 75 | Minor | Add a CI lint step that diffs the directory list in REQ-005 against ADR-001 c-003 (grep-extractable tables) and fails on divergence | Traceability, Internal Consistency |
| FM-16-it3 | E10 marketplace.json Content Post-Strip | REQ-005 and ADR-001 c-003 verify marketplace.json is PRESENT; the acceptance criteria do not verify that `source: "./"` remains correct (not rewritten to an absolute path or corrupted) after the strip + stub injection | 6 | 2 | 5 | 60 | Minor | Add an acceptance criterion: after skeleton generation, `grep '"source": "./"' .claude-plugin/marketplace.json` returns non-empty | Completeness, Evidence Quality |
| FM-08-it3 | E8 Tag Immutability Precondition | The idempotency proof is a pure function of `T → S`; if a maintainer force-moves a `v*` tag to a different commit, the deterministic SHA changes for the same tag name; the monitor's stored reference SHA then mismatches the legitimately re-regenerated branch | 6 | 2 | 5 | 60 | Minor | Document tag immutability as an operational constraint in the deployment runbook; add a pre-generation check: `git rev-list -n 1 ${TAG}` must equal the SHA recorded in the Release notes for that tag (if it exists) before proceeding | Methodological Rigor |
| FM-05-it3 | E3 Blank-Input Edge Case | On `workflow_dispatch` with blank `inputs.target_tag`, the fallback `git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=-version:refname \| head -1` depends on git 2.7+ version-sort; if no matching tags exist, the command returns empty; subsequent allow-list check exits non-zero but the error message may be opaque | 4 | 3 | 4 | 48 | Minor | Add an explicit error message when the blank-fallback resolution returns empty: "No v*.*.* semver tags found; provide inputs.target_tag explicitly"; add REQ-036 AC (f): blank-input with no semver tags exits non-zero with this specific message | Actionability |
| FM-10-it3 | E6 Source-Commit Trailer Forgeability | The Source-Commit: trailer used for the lazy-staleness check (NFR-006 weekly leg) is explicitly forgeable; if FM-06 (monitor self-failure) occurs simultaneously with an adversarial direct push, trailer forgery provides false reassurance that the branch is "fresh" | 4 | 3 | 4 | 48 | Minor | Already mitigated by the dual-check design (tamper-detection uses non-forgeable tip SHA); ensure FM-06 meta-monitoring is implemented so the tamper-detection leg cannot be silently disabled | Internal Consistency |
| FM-17-it3 | E11 GitHub Non-Retrigger Dependency | Loop-safety guarantee (3) depends on GitHub's documented behavior that GITHUB_TOKEN pushes cannot re-trigger any workflow; if this behavior changes (GitHub policy update), guarantee (3) is removed and only guarantees (1) and (2) remain | 7 | 1 | 5 | 35 | Minor | Periodically verify this guarantee against current GitHub Docs (quarterly); include the GitHub Docs URL and access date in the workflow file as a comment; treat a future guarantee removal as AE-005 security-relevant trigger | Evidence Quality |

**Total RPN: 1,611**

---

## Finding Details

### FM-01-it3: Reference Anchor Mutability (Critical — RPN 216)

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E2 (REQ-035) / E9 (ADR-002 §Continuous Integrity Monitoring) |
| **Strategy Step** | Step 2 (failure mode enumeration: Incorrect) + Step 3 (rating) |

**Evidence:**

ADR-002 states: *"CI publishes the expected deterministic tip SHA for the release to a durable, off-branch, protected surface — the GitHub Release notes for the tag (Releases are governed by main/release permissions, not by the unprotected branch)."* (§Continuous Integrity Monitoring, emphasis added)

REQ-035 AC: *"After a CI regeneration run for tag v{N}, the GitHub Release for v{N} notes contain a cowork-skeleton-sha: field with the 40-character tip SHA."*

The key claim is that Release notes are a "protected surface" because they are "governed by main/release permissions." In GitHub's permission model, any repository collaborator with `write` access can: (a) push to an unprotected branch (`git push`) and (b) edit Release notes (`gh release edit`). These require the SAME permission level — there is no fine-grained separation between branch-write and release-edit access for classic `write`-level collaborators. Therefore, any actor who can tamper with the `cowork-skeleton` branch (threat actor RT-01 in ADR-002) can ALSO update the Release notes SHA to match the tampered commit, making the monitor's assertion `live_tip_sha == published_sha` return `true` even for a compromised branch.

**Analysis:**

The publish-then-assert architecture's security model depends on the reference anchor being harder to corrupt than the artifact it guards. If both can be modified by the same threat actor with identical credentials, the architecture provides no additional protection beyond what an in-branch check would provide. The event-driven monitor would still fire on the branch push (`push: branches: [cowork-skeleton]`), but an attacker updating Release notes and the branch nearly simultaneously (automation takes seconds) would defeat the comparison before the monitor retrieves the reference.

This is a design trust-model gap, not an implementation bug. The iteration-3 controls introduced the publish-then-assert model, which is the correct direction; the gap is in the protection level of the reference anchor.

**Recommendation:**

Store the expected SHA in a location that only the CI workflow's `GITHUB_TOKEN` (specifically, only `cowork-skeleton.yml`) can write to. Options:
1. A commit to a separate branch protected with a ruleset that only `github-actions[bot]` bypass actor can push to (this requires the Option C credential for writes, but READS are public — the monitor can read without credentials).
2. A GitHub Actions artifact attached to the workflow run (content-addressed, not modifiable after creation).
3. A signed hash stored in a protected `CODEOWNERS`-guarded file on `main`.

**Acceptance Criteria:** An actor with repository `write` access cannot update the reference anchor SHA to an arbitrary value without going through a protected-branch or CI-only path.

**Estimated post-correction RPN:** 9 × 1 × 4 = 36 (O drops from 3 to 1 if reference anchor requires CI-only write; D drops from 8 to 4 with monitoring of anchor writes).

---

### FM-06-it3: Monitor Self-Failure (Major — RPN 196)

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E2 (REQ-035) / E6 (NFR-006) |
| **Strategy Step** | Step 2 (Missing lens: no meta-monitoring) |

**Evidence:**

NFR-006: *"A monitoring workflow SHALL perform two independent, complementary checks on each scheduled run."* The AC specifies the monitoring workflow exists and has `issues: write`, and describes four functional test scenarios (staleness, tamper-detection, clone-weight early-warning, event-driven verification). There is no requirement that the monitor's own health is monitored.

ADR-002 §Continuous Integrity Monitoring: *"Scheduled backstop — bounded SLA. The NFR-006 integrity/staleness workflow runs on a fixed cadence... Backed by the NFR-006 revision (dual-check, below)."* No specification of what happens when the NFR-006 workflow itself fails to run (cron missed, permission error, GitHub Actions outage).

**Analysis:**

GitHub Actions documentation explicitly notes that scheduled workflows may be delayed or skipped under high load. A workflow that fails due to a permission error (e.g., `issues: write` revoked) will exit non-zero but produce no GitHub issue — the failure mode is a job-level failure, visible in Actions UI, but not explicitly alerted to maintainers. A missed cron produces no visible failure at all. In either case, the SLA is silently breached.

**Recommendation:**

Add a meta-monitor: a separate workflow on a non-cron trigger (e.g., triggered by repository dispatch or a separate daily cron with a 1-hour offset) that asserts the NFR-006 monitor's last successful run was within the SLA window. Alternatively, use GitHub's workflow_run trigger on the NFR-006 workflow to fire a secondary check on failure.

**Acceptance Criteria:** If the NFR-006 monitor does not complete successfully within 25 hours, a GitHub issue is automatically opened.

**Estimated post-correction RPN:** 7 × 4 × 3 = 84 (D drops from 7 to 3 with meta-monitoring).

---

### FM-02-it3: Detection SLA Window for Executable Hooks (Major — RPN 144)

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E6 (NFR-006) |
| **Strategy Step** | Step 2 (Insufficient: SLA may be too long for hook blast radius) |

**Evidence:**

ADR-002: *"This ADR sets the interval at ≤ 24 hours (daily) for the tamper assertion, given that the skeleton ships executable hooks to user workstations (IT3-007) and a weekly window is too long for that blast radius."*

NFR-006: *"tamper-detection check (≤ daily cadence — the explicit detection SLA)"*

REQ-035: event-driven path detects direct-push *"within minutes"* (best-effort, not guaranteed).

**Analysis:**

The guaranteed detection SLA is 24 hours. During this window, a tampered `cowork-skeleton` branch (containing malicious `hooks/session-start.py` or pre-tool gates) is installable by any CoWork user who runs `claude plugin marketplace add geekatron/jerry@cowork-skeleton`. The hooks execute on every Claude Code session start, with access to the user's working directory, secrets in `.env` files, and Claude API interactions. The 24-hour window is acknowledged in the ADR as acceptable given that the event-driven path provides near-real-time detection for direct-push events — but the event-driven path is best-effort (it fires on `push:` events which could be delayed or missed under GitHub Actions load).

**Recommendation:**

Reduce the scheduled backstop cadence from ≤ daily to ≤ hourly. The cost of an hourly monitor running a `git rev-parse` and API call is minimal; the reduction in guaranteed worst-case exposure window from 24 h to 1 h is significant given the executable-hook blast radius.

**Acceptance Criteria:** NFR-006 scheduled leg runs at `schedule: cron: '0 * * * *'` (hourly) for the tamper-detection check; the lazy-staleness check may remain weekly.

**Estimated post-correction RPN:** 8 × 3 × 3 = 72 (D drops from 6 to 3 with hourly cadence).

---

### FM-07-it3: Permission-Scope Gaps (Major — RPN 144)

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E2 (REQ-035) / E6 (NFR-006) |
| **Strategy Step** | Step 2 (Incorrect / Insufficient: permission fragility) |

**Evidence:**

REQ-035: *"The monitor workflow SHALL declare `issues: write` in its `permissions:` block."*
REQ-035 AC (e): *"Monitor workflow `permissions:` block declares `issues: write`."* Verified by inspection.

NFR-006: *"The workflow SHALL declare `issues: write` in its `permissions:` block."*

**Analysis:**

The `issues: write` permission is required at runtime for the monitor to create GitHub issues on mismatch detection. If this permission is missing, the monitor's `gh issue create` call will silently fail (or fail with a non-zero exit code that may or may not propagate depending on shell error handling). The acceptance criterion verifies the permission by inspection of the YAML file, which confirms the declaration is present — but does not confirm it is correctly scoped, correctly applied to the job (not just the workflow), or not overridden by an org-level restrictive policy.

The monitor workflow is described as a separate file from `cowork-skeleton.yml` (to enable independent event triggers). A separate workflow has separate permissions that must be independently maintained. Future org policy changes (e.g., a restrictive default-permission override) could silently remove `issues: write` without any CI failure until a mismatch event occurs.

**Recommendation:**

Add a CI lint check (L5 gate) that grep-verifies `issues: write` in the monitor workflow file on every PR to `main`; add a functional integration test in REQ-035 AC that specifically triggers a mismatch and verifies a GitHub issue IS created (not just that the workflow exits non-zero).

**Acceptance Criteria:** Integration test confirms that injecting a SHA mismatch causes a GitHub issue to be created; the test fails if the issue is not created within 5 minutes.

**Estimated post-correction RPN:** 6 × 4 × 3 = 72 (D drops from 6 to 3 with automated verification).

---

### FM-04-it3: Clone-Weight Threshold Calibration (Major — RPN 144)

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E5 (REQ-034d) / E7 (ADR-001 Clone-Weight Decision) |
| **Strategy Step** | Step 2 (Incorrect: reference bandwidth may not represent CoWork user base) |

**Evidence:**

ADR-001 Clone-Weight Decision: *"early-warning band ≈ 150 MB pack / 40 s (≈ 60% of the hard trigger)"*

REQ-034: *"(c) estimated clone time on a reference network connection in seconds, compared against CoWork's 120-second CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS threshold (note: 10 Mbps = ~30th percentile global broadband; document the reference bandwidth used)"*

**Analysis:**

The 250 MB hard-fail and 40-second thresholds assume 10 Mbps as the reference bandwidth, stated as "approximately 30th-percentile global broadband." However:
- CoWork users on corporate VPNs may have effectively 2–5 Mbps throughput to GitHub
- Mobile CoWork users (increasing CoWork use case) may have 1–3 Mbps
- The `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` default of 120,000 ms is a HARD wall-clock limit, not a throughput limit

At 5 Mbps, 250 MB would take approximately 400 seconds — far exceeding the 120-second timeout. The pack size that triggers the timeout at 5 Mbps is approximately 75 MB (120 s × 5 Mbps / 8). The current 250 MB hard-fail threshold is set at 3.3× the timeout-trigger size for 5 Mbps connections.

**Recommendation:**

Recalibrate using a 5 Mbps (approximately 20th-percentile) reference bandwidth. At 5 Mbps: timeout-trigger ≈ 75 MB; set early-warning at 50 MB (66% of 75 MB) and hard-fail at 75 MB. Document the reference bandwidth and the calculation in the threshold definitions in both REQ-034d and REQ-034.

**Acceptance Criteria:** Thresholds documented with reference bandwidth and calculation; R-001 dimension (c) artifact records clone time at both 10 Mbps and 5 Mbps reference bandwidths.

**Estimated post-correction RPN:** 5 × 4 × 4 = 80 (S drops from 6 to 5 as the more conservative threshold reduces impact; D drops from 6 to 4 with documented calibration).

---

### FM-03-it3: Smoke-Test Circular Dependency (Major — RPN 128)

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E1 (REQ-034 dimension d) |
| **Strategy Step** | Step 2 (Ambiguous: deferral creates a human-enforced gate that may not hold under schedule pressure) |

**Evidence:**

REQ-034: *"(d) a direct CoWork plugin-install smoke test: install `geekatron/jerry@cowork-skeleton` in a running CoWork-compatible client and confirm the plugin loads without error within the 120-second timeout — this is the only dimension that directly falsifies the decisive framing in ADR-001. (dimension (d) MAY be deferred to Phase 4 if a CoWork runtime is unavailable before Phase 2)"*

R-001 §Verification Approach: *"(d) MAY be deferred to Phase 4 completion if a CoWork runtime is unavailable; the artifact SHALL record 'DEFERRED — required before Phase 5' and Phase 5 is blocked until completed"*

**Analysis:**

Dimension (d) is explicitly the only test that directly falsifies the project's foundational assumption: that CoWork installs via clean-clone file count, not local working directory file count. The other three dimensions are proxies. If dimension (d) is deferred (likely, given CoWork runtime availability constraints) and Phase 5 execution begins before dimension (d) is confirmed, the entire strategy rests on proxy evidence. The Phase-5 gate is human-enforced (requires checking the R001-clean-clone-count.md artifact for dimension (d) PASS); there is no automated blocker preventing Phase 5 from proceeding with dimension (d) in DEFERRED state.

**Recommendation:**

Add an automated Phase-5 gate: a CI check (or a mandatory first step in the Phase 5 generation script) that reads `verification/R001-clean-clone-count.md`, parses dimension (d) for PASS/DEFERRED/FAIL, and refuses to proceed (non-zero exit) unless dimension (d) shows PASS. This converts a human-enforced gate to a machine-enforced gate.

**Acceptance Criteria:** Phase 5 generation script exits non-zero and prints a clear error message if `verification/R001-clean-clone-count.md` does not exist or contains `DEFERRED` or `FAIL` for dimension (d).

**Estimated post-correction RPN:** 8 × 2 × 4 = 64 (O drops from 4 to 2 with automated gate).

---

### FM-13-it3: Early-Warning Non-Binding Status (Major — RPN 120)

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E5 (REQ-034d) / E7 (ADR-001 Clone-Weight Decision) |
| **Strategy Step** | Step 2 (Insufficient: early warning may be ignored) |

**Evidence:**

REQ-034d: *"the continuous integrity monitor SHALL additionally record size-pack: and clone time on each scheduled run and SHALL open a GitHub issue as a non-blocking early warning when size-pack: exceeds 150 MB"*

ADR-001 Clone-Weight Decision: *"early-warning band (~150 MB / ~40 s, ≈60% of the hard trigger) enables the pre-designed orphan-branch flip (ADR-001 Option B) to be executed proactively"*

**Analysis:**

The 150 MB early warning opens a GitHub issue but does NOT fail the release and has no documented SLA for human response. In a busy project, GitHub issues can accumulate without action, especially if they lack direct assignment or an SLA. If the early warning is ignored or de-prioritized, the first HARD action is a release-blocking CI failure at 250 MB — which at 5 Mbps reference bandwidth (see FM-04) would already have caused user-facing install timeouts. There is no intermediate escalation between the non-blocking issue at 150 MB and the blocking failure at 250 MB.

**Recommendation:**

Assign the early-warning GitHub issue to a named maintainer with a documented 30-day response SLA; or escalate the threshold: make 200 MB blocking (50 MB buffer before hard fail), leaving 150 MB as a non-blocking first notice. This ensures at least one escalation path exists between the non-blocking warning and the hard fail.

**Acceptance Criteria:** The early-warning GitHub issue includes an assignee and a due date (or the 200 MB blocking threshold is implemented and tested).

**Estimated post-correction RPN:** 5 × 3 × 4 = 60 (O drops from 4 to 3 with assigned SLA; D drops from 6 to 4 with blocking escalation).

---

### FM-09-it3: Pre-push Diff Gate Reference Ambiguity (Major — RPN 100)

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E4 (REQ-022) |
| **Strategy Step** | Step 2 (Incorrect: acceptance criterion references branch name that may resolve to remote old tip) |

**Evidence:**

REQ-022 AC: *"`git diff v{N}..cowork-skeleton -- ':!projects/'` is executed as an automated in-workflow step BEFORE the force-push step; the step exits non-zero and the force-push is skipped if the diff is non-empty."*

**Analysis:**

In the generation workflow, `cowork-skeleton` in the diff command resolves to the REMOTE tracking reference (`origin/cowork-skeleton`, i.e., the previous release's skeleton). The LOCAL generated content is `HEAD` (the commit just created by the generation script). The acceptance criterion's diff `v{N}..cowork-skeleton` therefore compares the source tag against the OLD remote branch, not against the freshly generated local content — the gate would pass even if the local generated content were corrupted or divergent, because the check is comparing the wrong things.

The CORRECT command should be `git diff v{N}..HEAD -- ':!projects/'` (or explicitly `git diff ${TAG}^{tree} HEAD^{tree}`), which compares the source tag's tree against the locally generated tree before it is pushed.

**Recommendation:**

Update REQ-022 and its AC to use `HEAD` instead of the branch name `cowork-skeleton`: `git diff ${TAG}..HEAD -- ':!projects/'`. Update the Demonstration AC to confirm that a synthetic file injected into the LOCAL generated tree (before push) is caught by the gate.

**Acceptance Criteria:** Updated AC: `git diff ${TAG}..HEAD -- ':!projects/'` is executed before push; injecting a file into the locally generated tree causes the gate to exit non-zero and skip the force-push.

**Estimated post-correction RPN:** 5 × 3 × 3 = 45 (O drops from 4 to 3; D drops from 5 to 3 with corrected command).

---

### FM-14-it3: TAG Resolution Implementation Complexity (Major — RPN 96)

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E8 (ADR-001 Regeneration Commit Determinism) |
| **Strategy Step** | Step 2 (Ambiguous: 3-branch conditional is complex for implementation) |

**Evidence:**

ADR-001 §Regeneration Commit Determinism pseudocode:
```bash
if [ "${GITHUB_EVENT_NAME}" = "workflow_dispatch" ]; then
  if [ -n "${INPUT_TARGET_TAG}" ]; then
    TAG="${INPUT_TARGET_TAG}"
  else
    TAG="$(git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=-version:refname | head -1)"
  fi
else
  TAG="${GITHUB_REF_NAME}"
fi
```
Comment: *"WARNING: the naive one-liner TAG="${INPUT_TARGET_TAG:-${GITHUB_REF_NAME}}" is UNSOUND"*

**Analysis:**

The 3-branch conditional is correct per the ADR's analysis, but its complexity creates implementation risk: an implementer who misreads the warning or simplifies the logic (replacing the 3-branch with the naive one-liner) would silently produce non-deterministic skeletons on `workflow_dispatch` with blank `inputs.target_tag`, as `GITHUB_REF_NAME` would resolve to the triggering branch (`main`) not a tag. The allow-list check would catch `main` only if `main` doesn't match `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` — which it doesn't, so it would correctly exit non-zero. But this produces an opaque failure rather than a useful error.

The larger risk is a subtle implementation variant that happens to pass the allow-list in the wrong event context.

**Recommendation:**

Add a dedicated integration test suite for the TAG resolution logic, covering: (1) `push:tags` event with `GITHUB_REF_NAME=v0.31.5` → asserts `TAG=v0.31.5`; (2) `workflow_dispatch` with `INPUT_TARGET_TAG=v0.31.4` → asserts `TAG=v0.31.4`; (3) `workflow_dispatch` with blank `INPUT_TARGET_TAG` and `GITHUB_REF_NAME=main` → asserts `TAG` resolves to most recent semver tag (not `main`). Each test verifiable by dry-run without actual push.

**Acceptance Criteria:** CI runs the three-case test suite on every PR to `main` that touches `cowork-skeleton.yml`; all three cases pass.

**Estimated post-correction RPN:** 6 × 3 × 3 = 54 (O drops from 4 to 3; D drops from 4 to 3 with test coverage).

---

### FM-11-it3: Publish Step Failure Leaves Anchor Unestablished (Major — RPN 90)

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E9 (ADR-002 §Continuous Integrity Monitoring) |
| **Strategy Step** | Step 2 (Missing: no verification that publish step succeeded) |

**Evidence:**

REQ-035: *"After each successful force-push, `cowork-skeleton.yml` SHALL publish the expected deterministic tip SHA for the release tag to the GitHub Release notes (e.g., `gh release edit v{TAG} --notes-append "cowork-skeleton-sha: <40-char-sha>"`)."*

REQ-035 AC (a): *"After a CI regeneration run for tag v{N}, the GitHub Release for v{N} notes contain a cowork-skeleton-sha: field with the 40-character tip SHA."* — verified by Demonstration.

**Analysis:**

`gh release edit` is a GitHub CLI command that may fail due to: missing `contents: write` permission on the Release resource, a non-existent release for the tag, rate limiting, or transient API errors. If the publish step fails and the workflow continues (or fails non-zero but the branch was already pushed), the reference anchor for the new release is absent. On the next monitor run, the monitor either retrieves a stale prior release's SHA (false positive mismatch) or fails to find any `cowork-skeleton-sha:` field (error condition). Neither case is correctly handled by the current requirements — there is no post-publish verification step.

**Recommendation:**

Add a mandatory post-publish verification step immediately after `gh release edit`: retrieve the release notes via `gh release view v{TAG} --json body` and assert the `cowork-skeleton-sha:` field is present and matches the just-pushed SHA. If not, exit non-zero before the workflow reports success. Include this verification in the REQ-035 AC.

**Acceptance Criteria:** CI exits non-zero if the `cowork-skeleton-sha:` field is absent from release notes after the publish step; the field is verified to contain the correct 40-character SHA.

**Estimated post-correction RPN:** 6 × 1 × 5 = 30 (O drops from 3 to 1 with post-publish verification catching the failure before the workflow completes).

---

## Recommendations

### Critical Findings (RPN ≥ 200)

**FM-01-it3 (RPN 216): Protect the Reference Anchor Against the Same Threat Actor**

The reference anchor (Release notes SHA) must be writable only by CI, not by any `write`-level collaborator. Recommended migration path (in priority order):

1. **Short-term (Phase 6):** Add explicit operational documentation forbidding manual editing of the `cowork-skeleton-sha:` field in Release notes; add a monitor check that alerts if the Release notes were modified by a non-GITHUB_TOKEN actor (using GitHub's audit log API or comparing edit timestamps).
2. **Medium-term (Phase 2 / STRIDE):** Evaluate storing the reference SHA in a commit to a separate protected branch (e.g., `cowork-skeleton-provenance`) that requires `github-actions[bot]` as the sole push actor — this requires the Option C GitHub App credential only for writes to that branch, while the monitor reads it publicly.
3. **Long-term (Phase 2+ STRIDE):** Consider using signed artifacts (e.g., SLSA provenance attestation attached to the release) as the reference anchor, which requires a private key (CI-only) to write but is publicly verifiable to read.

Acceptance criteria: After remediation, a repository collaborator with `write` access who tampers with `cowork-skeleton` branch CANNOT update the reference anchor to match the tampered SHA without CI involvement.

Estimated post-correction RPN: 36 (from 216).

### Major Findings (RPN 80–199)

**FM-06-it3 (RPN 196):** Add meta-monitoring for the NFR-006 monitor itself. Estimated post-correction: 84.

**FM-02-it3 (RPN 144):** Increase scheduled tamper-detection check to hourly cadence (from ≤ daily). Estimated post-correction: 72.

**FM-07-it3 (RPN 144):** Add CI lint for `issues: write` and functional integration test for issue creation on mismatch. Estimated post-correction: 72.

**FM-04-it3 (RPN 144):** Recalibrate clone-weight thresholds using 5 Mbps reference bandwidth. Estimated post-correction: 80.

**FM-03-it3 (RPN 128):** Automate Phase-5 blocking gate that checks dimension (d) PASS before allowing generation script execution. Estimated post-correction: 64.

**FM-13-it3 (RPN 120):** Add assignee + SLA to early-warning issue, or escalate 200 MB as a blocking threshold. Estimated post-correction: 60.

**FM-09-it3 (RPN 100):** Update REQ-022 AC to use `HEAD` not `cowork-skeleton` branch name in the pre-push diff command. Estimated post-correction: 45.

**FM-14-it3 (RPN 96):** Add three-case integration test suite for TAG resolution logic. Estimated post-correction: 54.

**FM-11-it3 (RPN 90):** Add mandatory post-publish verification that `cowork-skeleton-sha:` field appears in release notes before the workflow reports success. Estimated post-correction: 30.

### Minor Findings (RPN < 80)

**FM-15-it3 (75):** CI lint for REQ-005 / ADR-001 c-003 synchronization.
**FM-16-it3 (60):** Add marketplace.json content AC (grep for `source: "./"`).
**FM-08-it3 (60):** Document tag immutability constraint in operational runbook.
**FM-05-it3 (48):** Add explicit error message for blank-input fallback with no semver tags.
**FM-10-it3 (48):** No additional action beyond implementing FM-06 meta-monitoring.
**FM-17-it3 (35):** Periodic verification of GitHub GITHUB_TOKEN non-retrigger guarantee with URL + access date in workflow comments.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-01 reveals a trust-model gap in the reference anchor (not covered by any existing requirement); FM-06 identifies missing meta-monitoring as a gap in the coverage of the monitoring architecture; FM-11 identifies a missing post-publish verification step |
| Internal Consistency | 0.20 | Negative | FM-09 (REQ-022 AC uses wrong git ref — branch name vs. HEAD) creates an inconsistency between the requirement intent and its acceptance criterion; FM-14 (TAG resolution logic) creates an implementation-vs-design consistency risk |
| Methodological Rigor | 0.20 | Negative | FM-04 (threshold calibration at wrong reference bandwidth) weakens the methodological basis for the clone-weight decision; FM-02 (24h SLA for executable hooks) is a methodological shortfall given the blast radius; FM-08 (tag immutability precondition) is documented as a precondition but not tested |
| Evidence Quality | 0.15 | Negative | FM-01 (reference anchor protection claim is not supported by GitHub permission analysis); FM-04 (10 Mbps reference is undocumented as a deliberate choice for CoWork users specifically) |
| Actionability | 0.15 | Negative | FM-13 (non-blocking early warning may not lead to action); FM-03 (human-enforced Phase-5 gate may be bypassed under schedule pressure); FM-05 (blank-input edge case produces opaque error) |
| Traceability | 0.10 | Neutral | Traceability is significantly improved in iteration 3 (ADR-002 CC-1 through CC-8 all have backing requirements). Remaining gap: FM-15 (REQ-005 / ADR-001 c-003 may drift). The iteration-3 remediation closure is the strongest signal here. |

**Net assessment:** Completeness, Internal Consistency, and Methodological Rigor all show negative impact from Major findings. Traceability is the one neutral dimension, reflecting the substantial improvement from closing the ADR→REQ gap. The Critical finding (FM-01) spans Evidence Quality and Internal Consistency.

---

## Execution Statistics

- **Total Findings:** 16
- **Critical:** 1 (FM-01)
- **Major:** 10 (FM-02, FM-03, FM-04, FM-06, FM-07, FM-09, FM-11, FM-13, FM-14, FM-07)
- **Minor:** 5 (FM-05, FM-08, FM-10, FM-15, FM-16, FM-17)
- **Total RPN:** 1,611
- **Prior Iteration RPNs:** Iteration 1 → 3,207; Iteration 2 → 2,087; Iteration 3 → 1,611 (−22.8% vs. iteration 2)
- **Protocol Steps Completed:** 5 of 5
- **H-15 Self-Review:** Applied before persistence

---

*Generated by: adv-executor (jerry:adv-executor, claude-sonnet-4-6)*
*Strategy: S-012 FMEA (Failure Mode and Effects Analysis)*
*Template: .context/templates/adversarial/s-012-fmea.md (v1.0.0)*
*Project: PROJ-031-cowork-skeleton*
*Iteration: 3 (QG-1 re-score)*
*Date: 2026-06-26*
