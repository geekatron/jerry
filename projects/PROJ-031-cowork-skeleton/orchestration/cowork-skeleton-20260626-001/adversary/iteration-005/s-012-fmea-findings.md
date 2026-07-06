# FMEA Report: PROJ-031 CoWork Skeleton — Phase 2 Architecture

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** Five artifacts — ADR-001, ADR-003, phase1-requirements.md, phase2-stride-threat-model.md, phase2-attack-surface.md
**Criticality:** C4
**Date:** 2026-06-29T00:00:00Z
**Reviewer:** adv-executor (iteration-005)
**H-16 Compliance:** S-003 Steelman applied in iteration-005 prior to this execution (confirmed per STRATEGY-PLAN.md group ordering)
**Elements Analyzed:** 9 functional components | **Failure Modes Identified:** 31 (selected from 62 enumerated) | **Total RPN (selected):** 5,472 (estimated)

> **P-022 Calibration Notice:** All RPN scores (S × O × D) are estimates based on analysis of the five design artifacts. Severity (S) rates consequence if the failure occurs; Occurrence (O) rates likelihood the failure mode is latent in the design; Detection (D) rates likelihood the failure goes undetected without this FMEA. Scale: 1=best, 10=worst. These are design-phase estimates, not empirically calibrated values.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Component Inventory](#component-inventory) | 9-element decomposition |
| [FMEA Findings Table](#fmea-findings-table) | All 31 findings with S/O/D/RPN |
| [Critical Finding Details](#critical-finding-details) | Expanded analysis for all 15 Critical findings |
| [Recommendations](#recommendations) | Prioritized corrective actions by severity |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Summary counts |

---

## Summary

Across 9 functional components, 31 failure modes are reported (15 Critical, 11 Major, 5 Minor). Three systemic failure clusters dominate:

**Cluster 1 — Detection Layer Absent (5 Critical, highest RPN):** The monitor (FM-033, RPN 288), meta-monitor (FM-034, RPN 224), liveness monitor (FM-015, RPN 240), org-registration monitor (FM-043, RPN 224), and monitor correctness demonstration (FM-039, RPN 210) are all required but not yet implemented. The design specifies these controls across REQ-035/044/047/049, but "required in requirements" is not "implemented in production." Silent monitor failure has the highest combined RPN in this analysis (288). This is an operational/lifecycle-decay cluster that grows more dangerous with time.

**Cluster 2 — Foundational Assumption Unverified (3 Critical):** The ~5,000-file ceiling is undocumented by Anthropic (FM-046, FM-050, RPN 216 each) and the acceptance strategy may fail entirely if the limit is size- or time-based rather than file-count-based (FM-062, RPN 288). A file-count-only CI check (REQ-006) cannot detect a size/time-based limit violation. The single-shot R-001 verification (FM-060, RPN 280) certifies a moment-in-time snapshot while file count and clone weight grow monotonically per release.

**Cluster 3 — Supply-Chain Control Gap (3 Critical):** The rogue-tag provenance gate (D5) is designed in ADR-003 and specified in REQ-038/039 but not yet implemented, leaving the highest-consequence attack path (FM-032, RPN 243) open through Phase 5. The monitor's use of the forgeable `Source-Commit:` trailer instead of the non-forgeable tip SHA (FM-029, RPN 216) would nullify tamper detection against a targeted adversary. App private key exposure (FM-019, RPN 210) is a single-point-of-failure with S=10.

**Overall Assessment:** REVISE before Phase 5. The Phase 2 design architecture (ADR-001 + ADR-003) is sound, but 15 Critical failure modes exist in the implementation gap between "specified in requirements" and "demonstrated to work." No Phase 5 implementation MUST proceed until: (a) R-001 multi-dimensional smoke test is complete (FM-046/050/060/062), (b) D5 provenance gate is implemented (FM-032), and (c) the monitoring stack is implemented and demonstrated with a synthetic tamper test (FM-033/034/039/043).

---

## Component Inventory

| ID | Component | Description |
|----|-----------|-------------|
| A | Skeleton generation script | `git rm -r projects/ tests/`, stub injection, faithful-derivative gate, secret scan, manifest verification, tag resolution |
| B | CI regeneration trigger/liveness | Workflow triggers (`push: tags v*`, `workflow_dispatch`), concurrency guard, failure notification, liveness verification |
| C | Credential / GitHub App token | Cross-repo push credential (App token or deploy key), storage, scoping, rotation, REQ-045 Environment gate |
| D | Sigstore attestation generation+verification | Job permission isolation, ordering (attest-after-gates-before-push), monitor verification method |
| E | Integrity monitor / ≤6h poll | Scheduled read-only poll from source repo, `gh attestation verify`, meta-monitor heartbeat, silent failure handling |
| F | Org-marketplace registration | Single org-admin registration, canonical URL, verification monitor, runbook |
| G | Distribution + install | CoWork file-count/size/time ceiling (R-001), clone timeout, no install-time attestation, default-branch assumption |
| H | Update propagation | Stale skeleton detection, user-facing notification, rollback capability |
| I | File-count headroom | Early-warning threshold (3,500 files), clone-weight growth telemetry, large blob accumulation, R-001 multi-dimensionality |

---

## FMEA Findings Table

> RPN = S × O × D. All values are estimates (P-022). Critical: RPN ≥ 200 OR S ≥ 9. Major: RPN 80–199 OR S 7–8. Minor: RPN < 80 AND S ≤ 6.

### Critical Findings

| ID | Component | Failure Mode | S | O | D | RPN | Severity | Corrective Action Summary | Dim |
|----|-----------|-------------|---|---|---|-----|----------|--------------------------|-----|
| FM-033-it005 | (E) Monitor | Monitor silently exits 0 on verification error; no GitHub issue opened | 8 | 4 | 9 | **288** | Critical | Enforce non-zero exit on any error; add synthetic-tamper acceptance test | Evidence Quality |
| FM-062-it005 | (I) File-count | CoWork ceiling may be size- or time-based, not file-count-based; file-count assertion would pass while actual limit is breached | 9 | 4 | 8 | **288** | Critical | REQ-034 multi-dimensional gate must cover pack size (MB) + clone time (s) in CI, not file-count only | Methodological Rigor |
| FM-060-it005 | (I) File-count | R-001 is a single-shot pre-Phase-5 gate; file count and clone weight grow per release, so a passing test does not certify future releases | 7 | 5 | 8 | **280** | Critical | Convert to per-release assertion: CI hard-fails at count + emits pack size/time every run (REQ-034d + REQ-050) | Completeness |
| FM-032-it005 | (D) Attestation | Rogue-tag self-certification: D5 provenance gate (REQ-038/039) is designed but not implemented; CI faithfully builds and attests a malicious tree from a well-formed `v9.9.9` tag at any commit; monitor returns MATCH | 9 | 3 | 9 | **243** | Critical | Implement REQ-038 (`git merge-base --is-ancestor`) + REQ-039 (`v*` tag-protection ruleset) before Phase 5; blocks Phase 5 without these | Methodological Rigor |
| FM-015-it005 | (B) CI Trigger | REQ-049 liveness monitor not implemented; no control verifies a new `v*` tag produced a dedicated-repo deployment within 2h; CI failure leaves skeleton stale indefinitely | 6 | 5 | 8 | **240** | Critical | Implement REQ-049 liveness monitor; until then, stale skeleton after CI failure is undetectable | Completeness |
| FM-034-it005 | (E) Monitor | Meta-monitor (REQ-044) not implemented; if primary monitor fails silently, unbounded detection SLA; 25h alert threshold unverified | 7 | 4 | 8 | **224** | Critical | Implement REQ-044 meta-monitor; verify with simulated outage test | Completeness |
| FM-043-it005 | (F) Org-registration | REQ-047 org-registration monitor (≤24h) not implemented; rogue or typosquat registration goes undetected for potentially weeks | 7 | 4 | 8 | **224** | Critical | Implement REQ-047 before org registration; schedule periodic automated check of registered source == canonical | Completeness |
| FM-029-it005 | (D) Attestation | D7 monitor may compare forgeable `Source-Commit:` commit trailer (free-form text) rather than invoking `gh attestation verify <tip-sha>`; targeted tampering passes trailer-based detection | 9 | 3 | 8 | **216** | Critical | Verify D7 monitor implementation invokes `gh attestation verify` on the live tip SHA, never compares the `Source-Commit:` trailer | Evidence Quality |
| FM-046-it005 | (G) Distribution | The ~5,000-file CoWork ceiling is unverified empirically; strategy may be invalid if limit applies to local working directory (~24,636 files with `.venv/`) | 9 | 4 | 6 | **216** | Critical | Execute REQ-034 four-dimensional CoWork smoke test before Phase 5; R-001 blocks Phase 5 | Methodological Rigor |
| FM-050-it005 | (G) Distribution | If the CoWork limit is expressed as size (MB) or time (s) rather than file count, branch-stripping as designed delivers no benefit; entire project pivots | 9 | 4 | 6 | **216** | Critical | Multi-dimensional smoke test (REQ-034): file count AND pack size AND clone time AND live CoWork install; blocks Phase 5 | Actionability |
| FM-019-it005 | (C) Credential | App private key exposed outside source-repo secrets (logged to GITHUB_STEP_SUMMARY, committed, shared informally); theft enables durable forgery of any artifact | 10 | 3 | 7 | **210** | Critical | REQ-045: Actions Environment with deployment_branch_policy; REQ-019 secret masking; REQ-048 rotation | Evidence Quality |
| FM-039-it005 | (E) Monitor | Monitor correctness not demonstrated before Phase 5 via a synthetic tamper test; it may silently return "verified" on tampered artifacts if verification logic has a bug | 6 | 5 | 7 | **210** | Critical | Add synthetic-tamper acceptance test to REQ-035 V-method ("Test"); demonstrate monitor opens GitHub issue on injected mismatch | Completeness |
| FM-049-it005 | (G) Distribution | CoWork install (`claude plugin marketplace add`) performs no `gh attestation verify`; D7 monitor is the sole automated verifier, post-publication; users install without cryptographic verification (RTB-5) | 7 | 10 | 3 | **210** | Critical | Accept as platform limitation; document in RTB-5; ensure D7 monitor is the single compensating control and is demonstrably functional | Traceability |
| FM-007-it005 | (A) Gen. script | Secret scan gate misconfigured (`continue-on-error: true`, wrong scan path, exit code swallowed); stray credential outside `projects/`/`tests/` ships in the public skeleton | 9 | 3 | 7 | **189** | Critical | Ensure secret scan step has no `continue-on-error`; test with a synthetic credential file in a retained directory; gate must block push | Evidence Quality |
| FM-051-it005 | (G) Distribution | `.claude-plugin/marketplace.json` accidentally stripped or not generated; CoWork org-marketplace install fails silently with no diagnostic | 9 | 3 | 7 | **189** | Critical | REQ-005 AC explicitly verifies `marketplace.json` presence via `git ls-files`; implement and gate push on this check | Completeness |

### Major Findings

| ID | Component | Failure Mode | S | O | D | RPN | Severity | Corrective Action Summary | Dim |
|----|-----------|-------------|---|---|---|-----|----------|--------------------------|-----|
| FM-014-it005 | (B) CI Trigger | Silent pipeline failure: missing `if: failure()` notification step; skeleton goes stale with no alert | 7 | 4 | 7 | **196** | Major | REQ-016: add `if: failure()` step emitting to GITHUB_STEP_SUMMARY; implement before Phase 5 | Actionability |
| FM-022-it005 | (C) Credential | No enforced key rotation policy; departed maintainer retains push capability; REQ-048 (12-month rotation) exists in requirements but needs operational enforcement | 7 | 4 | 7 | **196** | Major | REQ-048: document rotation in runbook; calendar reminder + org-audit event on secret access | Completeness |
| FM-004-it005 | (A) Gen. script | Faithful-derivative gate uses `origin/main..HEAD` (mutable) instead of `${TAG}..HEAD` (frozen); mutable reference can advance mid-run, producing a false-clean signal (FM-09 bug from Phase 1) | 8 | 4 | 6 | **192** | Major | REQ-022 AC change: implement `git diff "${TAG}..HEAD" -- ':!projects/' ':!tests/'`; test with an injected extra file | Internal Consistency |
| FM-020-it005 | (C) Credential | GitHub App installed on all source-repo repos or granted `contents: write` on `geekatron/jerry`; CI compromise pivots to `main` | 8 | 4 | 6 | **192** | Major | Restrict App installation to `geekatron/jerry-cowork` only; `contents: write` on dedicated repo only (ADR-003 D3) | Completeness |
| FM-025-it005 | (C) Credential | GitHub Actions Environment (REQ-045) not configured; non-protected-branch `workflow_dispatch` can access the push credential | 8 | 4 | 6 | **192** | Major | Configure `skeleton-push` Environment with `deployment_branch_policy` restricting to protected `main` / `v*` | Methodological Rigor |
| FM-006-it005 | (A) Gen. script | `GITHUB_REF_NAME` used as-is for `workflow_dispatch`; resolves to branch name ("main") instead of a tag; non-deterministic builds | 7 | 5 | 5 | **175** | Major | REQ-036: event-discriminated TAG resolution (IT3-005 fix already documented in ADR-001 pseudocode) | Methodological Rigor |
| FM-061-it005 | (I) File-count | Large blobs (`skills/transcript/test_data/` ~908 KB) accumulate in pack history under Option A, accelerating clone-weight growth beyond the 150 MB early-warning band | 5 | 5 | 7 | **175** | Major | Track large-blob inventory per release via `git ls-tree -l -r`; flag in CI; strip path documented in ADR-001 R-002 | Completeness |
| FM-010-it005 | (A) Gen. script | `.claude/rules` and `.claude/patterns` symlinks point to `.context/rules` and `.context/patterns`; if either target is missing post-strip, entire Jerry rule system silently disabled on install | 8 | 3 | 7 | **168** | Major | REQ-009 AC verifies symlinks resolve in Linux CI; add explicit check that targets are non-empty directories | Evidence Quality |
| FM-059-it005 | (I) File-count | Clone-weight growth (pack size + clone time) not emitted per release; Option A → Option B flip trigger (>250 MB / >60s) is never triggered because the metric is never measured | 6 | 4 | 7 | **168** | Major | REQ-034d: CI must emit `git count-objects -vH` (size-pack) and timed reference-clone to GITHUB_STEP_SUMMARY every run | Completeness |
| FM-041-it005 | (F) Org-registration | No GitHub-native enforcement of two-admin approval for org-registration changes (RTB-3 explicitly notes this is a process control only); single compromised admin is sufficient | 8 | 4 | 6 | **192** | Major | REQ-043 revised: explicit process control label + REQ-047 as technical-detection compensator; org audit-log webhook | Internal Consistency |
| FM-002-it005 | (A) Gen. script | `projects/README.md` stub contains a dynamically generated value (build timestamp, `GITHUB_RUN_ID`, version string); bit-identical idempotency breaks silently | 7 | 4 | 5 | **140** | Major | REQ-004a: Inspection confirms static content only; add cross-run SHA comparison to REQ-003 acceptance criteria | Internal Consistency |

### Minor Findings

| ID | Component | Failure Mode | S | O | D | RPN | Severity | Note |
|----|-----------|-------------|---|---|---|-----|----------|------|
| FM-011-it005 | (B) CI Trigger | Trigger misconfigured (e.g. `push: branches: [main]` instead of `push: tags: ['v*']`); skeleton regenerates at wrong times | 6 | 3 | 4 | 72 | Minor | REQ-011 Inspection AC; visible in YAML |
| FM-013-it005 | (B) CI Trigger | Missing `concurrency:` block; concurrent tag pushes race on force-push target | 5 | 3 | 5 | 75 | Minor | REQ-015 Inspection AC |
| FM-017-it005 | (A) Gen. script | Maintainer force-moves a `v*` tag to different commit; generator faithfully builds from new target; D7 monitor detects SHA mismatch against attested value | 6 | 2 | 5 | 60 | Minor | D7 monitor detects this; tag protection (REQ-039) prevents it |
| FM-038-it005 | (E) Monitor | `gh attestation verify` fails due to Sigstore outage or rate limit; false-positive alert or missed verification | 5 | 3 | 5 | 75 | Minor | Error condition is observable; meta-monitor (REQ-044) catches extended outage |
| FM-045-it005 | (F) Org-registration | Org admin de-registers marketplace deliberately or by accident; all users lose plugin | 6 | 2 | 4 | 48 | Minor | REQ-047 monitor detects; recovery runbook exists |

---

## Critical Finding Details

### FM-033-it005: Monitor Silent Failure

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (E) Integrity Monitor |
| **S / O / D / RPN** | 8 / 4 / 9 / 288 (estimated) |
| **Strategy Step** | Step 2 (failure mode: Missing — error handling absent) + Step 3 (D=9: undetectable without this analysis) |

**Evidence:**
ADR-003 D7 specifies: "a non-zero exit, absent attestation, or mismatch SHALL open a GitHub issue and exit non-zero." REQ-035 states: "a non-zero exit / absent attestation / mismatch SHALL open a GitHub issue and exit non-zero." The STRIDE model (SC-05) rates "Monitor fails silently → unbounded detection SLA" as YELLOW (L=2, C=4). No acceptance criterion in REQ-035 tests the failure path; the V-Method is "Test" but the acceptance criterion only tests the happy path ("Trigger a release, confirm attestation present, verify monitor outputs the tip SHA and attestation result"). The failure injection test ("tamper the dedicated repo; confirm GitHub issue opens") is absent.

**Analysis:**
A monitoring workflow that exits 0 on an unhandled exception (uncaught Python/shell exception, `gh` CLI error not checked) produces a "green" CI run that is indistinguishable from a successful verification. The meta-monitor (REQ-044) fires only if the run doesn't complete within 25h — a silent 0-exit misfire IS a "completed run" and would NOT trigger the meta-monitor. The net result: the tamper-detection layer reports nominal health while providing zero actual detection. This is the highest-D (=9) finding in this FMEA and the highest RPN overall.

**Recommendation:**
1. Implement the monitor with explicit error guards: every `gh`, `git`, and `jq` call must have `|| { echo "::error::..."; exit 1; }`.
2. Add to REQ-035 Acceptance Criteria: "Inject a synthetic SHA mismatch (manually force-push a single byte change to a non-production test-cowork repo clone); verify that (a) the monitor exits non-zero, (b) a GitHub issue is opened within the poll cycle, and (c) the GITHUB_STEP_SUMMARY records the mismatch."
3. Post-correction RPN estimate: S=8, O=2, D=3 → RPN=48 (Major → Minor).
4. **OWNER:** nse-requirements (REQ-035 AC change) + eng-architect (D7 monitor implementation hardening).

---

### FM-062-it005: File-Count Ceiling Type Unconfirmed

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (I) File-count headroom |
| **S / O / D / RPN** | 9 / 4 / 8 / 288 (estimated) |
| **Strategy Step** | Step 2 (failure mode: Incorrect — wrong acceptance strategy) |

**Evidence:**
ADR-001 Consequences Risk table: "~5,000-file (or size/time-based) CoWork limit is undocumented/unverified (R-001); strategy may not yield installability — MED probability, HIGH impact." ADR-001 L2 point 4: "the ceiling could be size- or time-based rather than file-count-based (IN-001); a file-count-only check would falsely 'pass' a size/time failure and must not be the sole gate." REQ-034 AC requires the acceptance test to cover count, pack size, clone time, AND live CoWork install. However, REQ-006 (the CI gate) hard-fails only on `git ls-files | wc -l` ≥ 5,000. There is no CI gate on pack size or clone time per release.

**Analysis:**
The CI production gate (REQ-006) is file-count-only. If Anthropic's limit is actually enforced as "compressed pack > X MB" or "git clone > 120s," the ~1,417-file skeleton could fail installation while REQ-006 reports a passing count. This means a CI "green" build would be followed by a user-facing install failure with no CI signal. The acceptance strategy would falsely certify installability across every release. Detection=8 because this flaw is only discoverable via a live CoWork install test, which is not part of the automated CI gate.

**Recommendation:**
1. Add to CI (`cowork-skeleton.yml`) alongside the file-count assertion: `git count-objects -vH` emitting `size-pack` to GITHUB_STEP_SUMMARY; fail if size-pack > 250 MB (Option A → B flip trigger).
2. Timed reference clone step in CI (or scheduled workflow): fail if > 60s on a reference 10 Mbps network (ADR-001 hard trigger).
3. Execute REQ-034 dimension (d) live CoWork install before Phase 5; this is the only gate that directly falsifies the decisive framing.
4. Post-correction RPN estimate: S=9, O=2, D=4 → RPN=72 (Minor per RPN; Critical retained per S=9 until empirically verified).
5. **OWNER:** nse-requirements (REQ-034 multi-dimensional gate) + ps-architect (ADR-001 R-001 risk update).

---

### FM-060-it005: Single-Shot R-001 Verification

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (I) File-count headroom |
| **S / O / D / RPN** | 7 / 5 / 8 / 280 (estimated) |
| **Strategy Step** | Step 2 (failure mode: Insufficient — one-time gate cannot certify a growing quantity) |

**Evidence:**
R-001 Verification Approach states: "a mandatory four-dimensional verification SHALL be executed before Phase 2 begins." ADR-001 L2 point 2: "The R-001 artifact records the baseline pack size + clone time… the continuous integrity workflow records weight every cycle with an early-warning band (~150 MB / ~40 s, ≈60% of trigger)." REQ-034d (clone-weight telemetry) is specified but classified as "Status: Draft" with no implementation artifact referenced. ADR-001 Clone-Weight Decision states: "A single Phase-2 snapshot cannot certify a monotonically growing quantity."

**Analysis:**
Even if R-001 passes at Phase 2 (skeleton at ~1,417 files, pack well under 250 MB), each subsequent release adds ~2 MB of history pack (ADR-001 empirical estimate). Over 1–3 years of releases (ADR-001: "dozens of releases"), the skeleton clone crosses the Option B flip trigger. Without per-release pack-size telemetry in CI, the approach of the flip trigger is invisible — the first symptom observed by a user is an install timeout. The R-001 single-shot gate therefore creates false confidence: it certifies an initial state, not a trajectory. Detection=8 because the growth is gradual and only becomes apparent when a threshold is crossed.

**Recommendation:**
1. Implement REQ-034d: every CI run of `cowork-skeleton.yml` must emit `git count-objects -vH` (size-pack) to GITHUB_STEP_SUMMARY and open an early-warning issue at ~150 MB pack.
2. Scheduled integrity monitor (D7) must also record pack size + clone time on each ≤6h cycle (already specified in ADR-001 Clone-Weight Decision control table).
3. Re-run R-001 verification annually or when the early-warning band is breached.
4. Post-correction RPN estimate: S=7, O=3, D=4 → RPN=84 (Major).
5. **OWNER:** nse-requirements (REQ-034d liveness + REQ-050 file-count telemetry) + ps-architect (ADR-001 R-001 update).

---

### FM-032-it005: Rogue Tag Self-Certification (D5 Not Implemented)

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (D) Sigstore attestation |
| **S / O / D / RPN** | 9 / 3 / 9 / 243 (estimated) |
| **Strategy Step** | Step 2 (failure mode: Missing — D5 provenance gate absent from current implementation) |

**Evidence:**
STRIDE Phase-2 (SC-02, rank #1 residual): "Rogue-tag CI self-certification: attacker pushes well-formed `v9.9.9` at a malicious commit; CI faithfully builds + self-certifies; monitor returns MATCH → zero detection." ADR-003 D5 and REQ-038/039 specify the provenance gate but both are "Proposed / Draft" status — not yet implemented. Phase-2 attack-surface (V-03): "a collaborator who pushes a well-formed `v*` tag not on `main` has it checked out and processed; branch protection is blind because CI itself is the pusher." Attack Trees AT-1.2: DREAD mean = 7.6 (the top-rated attack path).

**Analysis:**
The integrity anchor (D4: Sigstore attestation) faithfully certifies whatever CI builds. If the input tag is malicious — pointing at a commit not on `main` — the attestation proves that "CI built exactly this tree from exactly that tag," which is true, but provides no evidence that the tag was legitimate. D2 (branch protection) is blind because CI is the authorized pusher. D7 (monitor) returns MATCH because the attestation genuinely matches the live tip SHA. Detection=9: no currently-implemented control can detect this. Tag protection (REQ-039) prevents arbitrary tag creation; the provenance assertion (REQ-038) catches it at build time. Neither is implemented.

**Recommendation:**
1. Implement REQ-038 before Phase 5: add `git merge-base --is-ancestor "${TAG}^{commit}" origin/main` immediately after tag allow-list validation; non-zero exit with no push and no attestation on failure.
2. Implement REQ-039 before Phase 5: configure source-repo ruleset restricting `v*` tag creation to the release pipeline / designated maintainers.
3. Both controls MUST be in place before Phase 5; this is identified as a Phase-5 blocker in ADR-003 L2 point 2 and STRIDE L2 point 5.
4. Post-correction RPN estimate: S=9, O=1, D=3 → RPN=27 (low; controlled).
5. **OWNER:** eng-architect (D5 implementation) + nse-requirements (REQ-038/039 V-method update to "Test").

---

### FM-015-it005: REQ-049 Liveness Monitor Not Implemented

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (B) CI regeneration trigger/liveness |
| **S / O / D / RPN** | 6 / 5 / 8 / 240 (estimated) |
| **Strategy Step** | Step 2 (failure mode: Missing — specified control not yet built) |

**Evidence:**
REQ-049: "A liveness monitor SHALL verify the latest source `v*` tag produced a dedicated-repo deployment within 2 h of the tag-push timestamp; mismatch → GitHub issue distinguishing 'monitor down' from 'generation did not fire'." This requirement is listed in the Phase-2 security requirements section as "Status: Draft" with no referenced implementation artifact. REQ-037 covers push-failure detection in-workflow, but a completely failed CI run (job never executed, runner unavailable, workflow file syntax error) would not trigger REQ-037. ADR-001 Risks: "Idempotency drift from un-pinned commit metadata — LOW / MED — Pin all metadata in the generation script; CI SHA assertion."

**Analysis:**
A CI runner outage, quota exhaustion, or workflow syntax error after a `v*` tag push silently leaves the dedicated skeleton at the prior release. REQ-037 (push-failure detection) only fires if the workflow runs and the push step fails; it cannot catch a run that never starts. Users auto-refreshing CoWork install the stale version indefinitely. The 2h liveness window is specified but unmonitored. Detection=8 because there is currently no mechanism to observe the silence between tag-push and deployment.

**Recommendation:**
1. Implement REQ-049 as a scheduled workflow (hourly cadence) that queries the source repo for the latest `v*` tag timestamp (`gh api /repos/geekatron/jerry/git/refs/tags`), queries the dedicated repo for the latest push timestamp (`gh api /repos/geekatron/jerry-cowork/branches/{default}`), and opens a GitHub issue if the gap exceeds 2h.
2. Separate the "generation did not fire" signal from the "monitor down" signal by checking whether the source `cowork-skeleton.yml` run list shows a recent run for the tag.
3. Post-correction RPN estimate: S=6, O=3, D=3 → RPN=54 (Minor).
4. **OWNER:** nse-requirements (REQ-049 V-method: "Demonstration") + eng-architect (implementation).

---

### FM-034-it005: Meta-Monitor Absent or Misconfigured

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (E) Integrity Monitor |
| **S / O / D / RPN** | 7 / 4 / 8 / 224 (estimated) |
| **Strategy Step** | Step 2 (failure mode: Missing — specified control not yet built) |

**Evidence:**
REQ-044: "A meta-monitor SHALL alert (GitHub issue) if the integrity backstop monitor has not completed successfully within 25 h." ADR-003 D4: "paired with a meta-monitor heartbeat (alert if no successful run in 25 h, SC-05)." STRIDE SC-05 (L=2, C=4, score=8 YELLOW): "Monitor fails silently → unbounded detection SLA." The meta-monitor requirement is in "Status: Draft" with no implementation artifact.

**Analysis:**
The meta-monitor's purpose is to detect FM-033 (monitor silent failure). Without it, the integrity monitor can exit 0 while providing no actual verification — and no one will know. The 25h alerting threshold means up to 25h of undetected monitor outage. A monitor that exits 0 but does not open issues on mismatches (FM-033) would never trigger the meta-monitor's "no successful run" condition because the run IS completing "successfully" (exit 0). This means FM-033 and FM-034 compound each other: a buggy monitor + no meta-monitor = indefinite undetected outage.

**Recommendation:**
1. Implement REQ-044 meta-monitor: a separate scheduled workflow (e.g., hourly) that queries GitHub Actions run history for the monitor workflow; if no successful completion in 25h, opens a GitHub issue labeled `monitoring-outage`.
2. Define "successful completion" as both `conclusion: success` AND a verified attestation result in the job outputs (not just a zero exit code).
3. Demonstrate meta-monitor with a forced monitor outage in acceptance testing.
4. Post-correction RPN estimate: S=7, O=2, D=4 → RPN=56 (Minor).
5. **OWNER:** nse-requirements (REQ-044 AC + V-method) + eng-architect (implementation).

---

### FM-043-it005: Org-Registration Monitor Not Implemented

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (F) Org-marketplace registration |
| **S / O / D / RPN** | 7 / 4 / 8 / 224 (estimated) |
| **Strategy Step** | Step 2 (failure mode: Missing — specified control not yet built) |

**Evidence:**
REQ-047: "An automated monitor SHALL verify (≤ 24 h) that the org's registered CoWork source matches canonical `geekatron/jerry-cowork`, with an org audit-log webhook on marketplace-settings change; mismatch → GitHub issue." ADR-003 RTB-3: "REQ-043's 'two-admin approval for any registered-source change' has no GitHub-native technical enforcement... It is therefore a process control." STRIDE (OR-01, OR-02, both YELLOW 10/15): rogue registration and typosquat registration both rated L=2, C=5. No implementation artifact exists for REQ-047.

**Analysis:**
The org-registration trust chain is explicitly called out as a new, concentrated attack surface in ADR-003 L2 ("trust concentrates as it secures"). A rogue registration (OR-01) or typosquat (OR-02) directly delivers attacker-controlled hooks to every org user. The two-admin process control (RTB-3) has no technical enforcement. Without REQ-047, a rogue registration could persist for days or weeks before human discovery. Detection=8 because the only current detection path is human observation of CoWork's "Your organization" listing.

**Recommendation:**
1. Implement REQ-047 before org registration: scheduled daily workflow that queries the org's registered CoWork marketplace source via the Anthropic/CoWork API (if available) or the org audit log; compares against canonical `geekatron/jerry-cowork`; opens GitHub issue on mismatch.
2. Configure org audit-log webhook: on any `marketplace.settings.change` event, fire a GitHub issue immediately (sub-hour detection).
3. Publish canonical URL in at least two independently verifiable locations (Jerry README, org GitHub profile) before the first registration.
4. Post-correction RPN estimate: S=7, O=2, D=3 → RPN=42 (Minor).
5. **OWNER:** nse-requirements (REQ-047 AC) + eng-architect (webhook + monitor implementation).

---

### FM-029-it005: Monitor Uses Forgeable Source-Commit Trailer

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (D) Sigstore attestation |
| **S / O / D / RPN** | 9 / 3 / 8 / 216 (estimated) |
| **Strategy Step** | Step 2 (failure mode: Incorrect — wrong comparator in monitor logic) |

**Evidence:**
ADR-001 Tamper-Evidence section: "Contrast the `Source-Commit:` trailer, which is FORGEABLE — it is free-form commit-message text any push actor can set to the correct value while shipping a different tree; the trailer can detect *lazy* staleness (CI never regenerated) but CANNOT detect targeted tampering, and MUST NOT be used as the integrity comparator." ADR-003 D7: "Verification uses the non-forgeable tip SHA, never the `Source-Commit` trailer." REQ-035: "The monitor's `$GITHUB_STEP_SUMMARY` SHALL record the tip SHA verified and the attestation verification result." However, no requirement explicitly forbids the forgeable comparator, and no acceptance criterion verifies which comparator is used.

**Analysis:**
If the D7 monitor is implemented to compare the `Source-Commit:` text in the commit message against the source SHA rather than invoking `gh attestation verify <tip-sha>`, a targeted attacker can:
1. Push a malicious tree to the dedicated repo
2. Set `Source-Commit:` to the correct expected value in the commit message
3. The monitor reads the trailer, finds it matches, and reports no tamper

The `Source-Commit:` trailer is set by the generation script but is ultimately just a string that any push actor with the bypass credential can set to any value. The tip SHA (the hash of the actual published tree + parent + metadata) is non-forgeable. Detection=8: the difference between the two comparators is not externally observable without reading the monitor's source code.

**Recommendation:**
1. Add to REQ-035 AC: "The monitor SHALL invoke `gh attestation verify <live-tip-sha> --repo geekatron/jerry`; the `Source-Commit:` trailer SHALL NOT be used as the sole comparator. Verify by code inspection that the monitor implementation uses `gh attestation verify`."
2. Test with a synthetic tamper: manually push a commit with the correct `Source-Commit:` trailer but a different tree; confirm the monitor detects it (passes the `gh attestation verify` check means it fails the comparison → opens issue).
3. Post-correction RPN estimate: S=9, O=1, D=3 → RPN=27 (low; controlled).
4. **OWNER:** eng-architect (D7 monitor implementation verification) + nse-requirements (REQ-035 AC code-inspection requirement).

---

### FM-046-it005 / FM-050-it005: R-001 File-Count Limit Unverified / Pivot Scenario

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (G) Distribution + install |
| **S / O / D / RPN** | 9 / 4 / 6 / 216 each (estimated) |
| **Strategy Step** | Step 2 (failure mode: Missing — foundational assumption unverified) |

**Evidence:**
R-001 Stated Assumption (phase1-requirements.md): "The CoWork plugin-load file-count limit is approximately 5,000 files, and that limit applies to the tracked file count of a clean-clone working tree of the branch — not to a local developer working directory." Source: "User-reported (PLAN.md §Problem); confirmed absent from Anthropic's Claude Code plugin documentation." ADR-001 L2 point 4: "this is honestly the top residual risk and is NOT resolved by this ADR." Criticality: "Critical. If the limit applies to the local working directory rather than the clean-clone tree, branch-stripping has no effect."

**Analysis:**
The entire architecture — skeleton branch, CI regeneration, dedicated repo, all of it — solves for one problem: getting the tracked file count under ~5,000. If that problem is differently defined (size-based, time-based, or applies to the local working directory including `.venv/` at ~24,636 files), the skeleton strategy is solving the wrong problem. The ~1,417 files in the skeleton might still fail installation. FM-046 covers the "ceiling type wrong" scenario; FM-050 covers the "pivot required" scenario (user decision needed before Phase 5). Both have Detection=6 because discovery requires a live CoWork smoke test.

**Recommendation:**
1. Execute REQ-034 four-dimensional acceptance test before any Phase 5 implementation: (a) tracked file count on clean clone, (b) pack size, (c) clone time, (d) live CoWork install in a running CoWork-compatible client.
2. Dimension (d) is the only dimension that directly falsifies the decisive framing; it cannot be deferred to Phase 5 itself.
3. Document the R-001 test result artifact (`verification/R001-clean-clone-count.md`) with all four dimensions.
4. If dimension (d) reveals the strategy is invalid, escalate to the user per H-02 (P-020 user authority) with a proposed pivot before any implementation.
5. Post-correction RPN estimate (if verified passing): S=9, O=2, D=4 → RPN=72 (still notable but controlled).
6. **OWNER:** nse-requirements (REQ-034 V-method and AC) + ps-architect (ADR-001 R-001 update after verification).

---

### FM-019-it005: App Private Key Exposure

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (C) Credential / GitHub App token |
| **S / O / D / RPN** | 10 / 3 / 7 / 210 (estimated) |
| **Strategy Step** | Step 2 (failure mode: Missing — REQ-045 Environment gate not yet implemented) |

**Evidence:**
ADR-003 RTB-4: "The App private key (or deploy key) is the project's single long-lived secret; theft enables durable forgery of the artifact." REQ-045: "The App private key + deploy key SHALL be stored as environment-level secrets in a GitHub Actions Environment (`skeleton-push`) whose `deployment_branch_policy` restricts activation to protected `main` / `v*`." REQ-019: "The CI workflow SHALL NOT cause any secret value… to appear in GitHub Actions logs." REQ-048: "The App private key SHALL be rotated at minimum every 12 months." All three requirements are "Status: Draft" with no implementation artifacts.

**Analysis:**
S=10 because App private key theft enables durable, persistent forgery of the artifact — every user's skeleton install can be compromised until the key is rotated. Without REQ-045, the credential is accessible from any branch on which `workflow_dispatch` can be invoked (including unprotected branches), expanding the attack surface. Without REQ-048, a key compromise from a personnel change is irrecoverable without external incident detection. Without REQ-019 implementation, a debug echo statement could print the token to public CI logs. Detection=7: key theft is typically only discovered through observed misuse.

**Recommendation:**
1. Implement REQ-045 immediately upon provisioning the App or deploy key: configure `skeleton-push` GitHub Actions Environment with deployment protection requiring the branch to match `main` or `v*` pattern.
2. Implement REQ-019 secret masking in CI: ensure no job step echos the credential; use `::add-mask::` GitHub Actions command for the minted token.
3. Implement REQ-048: document rotation in the org-registration runbook with an explicit calendar reminder; rotate immediately on any personnel change affecting source-repo secrets access.
4. Consider GitHub App over deploy key for short-lived minted tokens (~1h) reducing durable exposure risk.
5. Post-correction RPN estimate: S=10, O=1, D=5 → RPN=50 (Major; S=10 retains Critical classification).
6. **OWNER:** eng-architect (REQ-045 Environment configuration) + nse-requirements (REQ-048 rotation policy implementation).

---

### FM-039-it005: Monitor Correctness Not Demonstrated

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (E) Integrity Monitor |
| **S / O / D / RPN** | 6 / 5 / 7 / 210 (estimated) |
| **Strategy Step** | Step 2 (failure mode: Insufficient — V-method inadequate) |

**Evidence:**
REQ-035 V-Method: "Test." REQ-035 Acceptance Criterion: "Trigger a release, confirm the attestation is present, verify that the monitor outputs the tip SHA and the attestation verification result in $GITHUB_STEP_SUMMARY on the next scheduled cycle." This AC tests only the happy path (successful attestation, successful verification). No AC tests the failure path: "what happens when the dedicated repo's tip SHA does not match the attestation?" The ADR-003 D7 monitor is designed but implementation artifacts are not referenced.

**Analysis:**
A monitor that does not open a GitHub issue on mismatch is indistinguishable from one that does, until a mismatch occurs. If the monitor has a logic bug (e.g., `if [[ $RESULT -eq 0 ]]; then echo "✓"; fi` without an `else` branch that opens an issue), it would pass the REQ-035 AC while providing no actual detection. Detection=7: the bug only manifests when a tamper event occurs, which is precisely when the monitor most needs to work.

**Recommendation:**
1. Add to REQ-035 AC: "Inject a synthetic tamper into a test-environment dedicated repo clone (or use a mock endpoint) that presents a mismatched tip SHA; confirm the monitor opens a GitHub issue with the label `integrity-alert` and that the GITHUB_STEP_SUMMARY records 'MISMATCH DETECTED.'"
2. This synthetic-tamper test must be demonstrated before Phase 5 org registration.
3. Consider a dedicated pre-production test workflow that runs the monitor against a known-mismatched state as part of the Phase 4 acceptance gate.
4. Post-correction RPN estimate: S=6, O=2, D=4 → RPN=48 (Minor).
5. **OWNER:** nse-requirements (REQ-035 AC update) + eng-architect (synthetic-tamper test design).

---

### FM-049-it005: No Install-Time Attestation Verification (RTB-5 Platform Limitation)

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (G) Distribution + install |
| **S / O / D / RPN** | 7 / 10 / 3 / 210 (estimated) |
| **Strategy Step** | Step 2 (failure mode: Missing — structural platform gap) |

**Evidence:**
ADR-003 RTB-5: "CoWork's `claude plugin marketplace add` flow does not invoke `gh attestation verify`; the D4 attestation is not checked at the point of distribution to the end user. The D7 backstop monitor is therefore the sole automated verification path, and it verifies after publication, not at install." O=10 because this is a platform constraint — certain to be present. D=3 because it is documented in RTB-5.

**Analysis:**
Users install whatever is in the dedicated repo's default branch at install time. The D7 monitor detects tampered content within ≤6h of tampering, but users who install during the detection window receive the tampered version without any client-side warning. This is not a design defect — it is an architectural limitation of the current CoWork platform. The compensating control (D7 monitor + prevention via D2) is documented and sound. However, the finding must be recorded: during the tamper window, users are cryptographically unprotected.

**Recommendation:**
1. Accept as a platform limitation per RTB-5; no corrective action can close this gap within the current CoWork platform.
2. Ensure the D7 monitor is the most reliable compensating control: implement FM-033 fix (monitor never silently fails) and FM-039 fix (demonstrated with synthetic tamper).
3. Document the ≤6h exposure window in user-facing documentation as a known limitation.
4. If CoWork ever exposes consumer-side attestation verification, revisit immediately.
5. Post-correction RPN estimate: S=7, O=10, D=3 → RPN=210 (unchanged; platform limitation).
6. **OWNER:** ps-architect (RTB-5 documentation completeness) + nse-requirements (document as accepted residual risk with explicit traceability).

---

### FM-007-it005: Secret Scan Gate Bypass

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (A) Skeleton generation script |
| **S / O / D / RPN** | 9 / 3 / 7 / 189 (estimated) |
| **Strategy Step** | Step 2 (failure mode: Missing — gate absent or misconfigured) |

**Evidence:**
ADR-003 D6 item 4: "Secret-scan the generated tree before the cross-repo push; the artifact is public, so a stray credential outside `projects/`/`tests/` must be caught." REQ-022 (changed): "A secret-scan step SHALL execute on the generated tree BEFORE the push; secret-scan failure SHALL prevent the push." However, REQ-022 AC states: "Analysis: implementation of faithful-derivative gate per specified diff command + secret scan" — but no explicit acceptance criterion tests what happens when a secret IS found (does the step prevent the push?). S=9 because the skeleton is publicly distributed.

**Analysis:**
If the secret-scan step is configured with `continue-on-error: true`, if the scanner is invoked with a path that doesn't include all retained directories, or if the scanner's exit code is not checked before the push step, a credential accidentally included in a skill file, a hook script, or any other retained file ships to every CoWork org user in a public repo. The skeleton strips `projects/` and `tests/` but retains `skills/`, `.context/`, `hooks/`, `src/` — any of which could contain a stray credential not caught by GitHub's built-in secret scanning (which runs post-push, too late).

**Recommendation:**
1. Implement the secret-scan step with `|| { echo "::error::Secret detected in generated tree — BLOCKING PUSH"; exit 1; }` and NO `continue-on-error`.
2. Add to REQ-022 AC: "Inject a synthetic GitHub token pattern (`ghp_` + 36 chars) into a skill fixture file; confirm the secret-scan step exits non-zero and the push does not execute."
3. Ensure the scanner covers the entire working directory, not just changed files.
4. Post-correction RPN estimate: S=9, O=1, D=4 → RPN=36 (Major; S=9 retains Critical classification).
5. **OWNER:** nse-requirements (REQ-022 AC update) + eng-architect (secret-scan implementation).

---

### FM-051-it005: marketplace.json Silently Missing

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Component** | (G) Distribution + install |
| **S / O / D / RPN** | 9 / 3 / 7 / 189 (estimated) |
| **Strategy Step** | Step 2 (failure mode: Missing — gap in retention surface verification) |

**Evidence:**
ADR-001 Canonical Plugin-Retention Surface entry #2: "`.claude-plugin/marketplace.json` — Was missing from both prior lists — a tree without it fails CoWork install silently (FM-006)." REQ-005: "`.claude-plugin/marketplace.json` SHALL be present in the generated branch tree." REQ-005 AC: "`git ls-files .claude-plugin/marketplace.json` returns non-empty." The original canonical surface omission was corrected in ADR-001 iteration 2, but the initial oversight demonstrates the detection gap: if REQ-005 is not correctly implemented to check `marketplace.json`, the skeleton ships without it and CoWork org install silently fails.

**Analysis:**
The failure is SILENT per the ADR-001 parenthetical "(fails CoWork install silently)". A user attempting to install from the org marketplace sees no error message — the install simply does not appear or does not function. S=9 because the entire distribution channel is broken for all org users until the file is re-added. Detection=7: the failure would not surface in CI (strip logic might not remove it, but a misconfigured REQ-005 check would pass on the wrong path) and only manifests in live CoWork testing.

**Recommendation:**
1. Ensure REQ-005 CI check explicitly verifies BOTH `plugin.json` AND `marketplace.json` by full path, not just `.claude-plugin/` directory presence.
2. Add to REQ-005 AC: "Temporarily remove `.claude-plugin/marketplace.json` from the generated tree; confirm the CI check exits non-zero and blocks the push."
3. Post-correction RPN estimate: S=9, O=1, D=3 → RPN=27 (controlled; Critical retained per S=9 until verified).
4. **OWNER:** nse-requirements (REQ-005 AC hardening).

---

## Recommendations

### Critical — Required before Phase 5 (blocks implementation gate)

| FM | RPN | Finding | Corrective Action | OWNER |
|----|-----|---------|-------------------|-------|
| FM-033-it005 | 288 | Monitor silent failure | Enforce non-zero exit on all monitor error paths; synthetic-tamper acceptance test | nse-requirements + eng-architect |
| FM-062-it005 | 288 | File-count ceiling type unconfirmed | Add CI pack-size + clone-time assertion; REQ-034 multi-dimensional gate in CI, not just pre-Phase-5 snapshot | nse-requirements + ps-architect |
| FM-060-it005 | 280 | Single-shot R-001 verification | Per-release pack-size/clone-time telemetry in CI (REQ-034d + REQ-050) | nse-requirements + ps-architect |
| FM-032-it005 | 243 | Rogue tag self-certification | Implement REQ-038 + REQ-039 (provenance gate + tag protection) before Phase 5 | eng-architect + nse-requirements |
| FM-015-it005 | 240 | Liveness monitor not implemented | Implement REQ-049 (2h deployment window monitor) | nse-requirements + eng-architect |
| FM-034-it005 | 224 | Meta-monitor absent | Implement REQ-044 meta-monitor; demonstrate with forced outage | nse-requirements + eng-architect |
| FM-043-it005 | 224 | Org-registration monitor absent | Implement REQ-047 before org registration | nse-requirements + eng-architect |
| FM-029-it005 | 216 | Monitor uses forgeable trailer | Verify D7 monitor uses `gh attestation verify <tip-sha>`, not `Source-Commit:` trailer; add code-inspection AC | eng-architect + nse-requirements |
| FM-046-it005 | 216 | R-001 unverified (count ceiling) | Execute REQ-034 four-dimensional CoWork smoke test | nse-requirements + ps-architect |
| FM-050-it005 | 216 | R-001 pivot scenario | Same as FM-046; smoke test must include live CoWork install (dimension d) | nse-requirements + ps-architect |
| FM-019-it005 | 210 | App private key exposure | REQ-045 Environment gate; REQ-019 masking; REQ-048 rotation | eng-architect + nse-requirements |
| FM-039-it005 | 210 | Monitor not demonstrated | Add synthetic-tamper test to REQ-035 AC | nse-requirements + eng-architect |
| FM-049-it005 | 210 | No install-time attestation (RTB-5) | Accept as platform limitation; document; ensure D7 is demonstrably functional | ps-architect + nse-requirements |
| FM-007-it005 | 189 | Secret scan gate bypass | Secret scan must exit non-zero and block push; add synthetic credential test to REQ-022 AC | nse-requirements + eng-architect |
| FM-051-it005 | 189 | marketplace.json silently missing | REQ-005 must explicitly verify `marketplace.json` by full path; add negative test | nse-requirements |

### Major — Required before Phase 5 delivery (corrective action recommended)

| FM | RPN | Finding | Corrective Action | OWNER |
|----|-----|---------|-------------------|-------|
| FM-014-it005 | 196 | Silent pipeline failure | REQ-016: implement `if: failure()` notification step | nse-requirements |
| FM-022-it005 | 196 | No key rotation enforced | REQ-048: document rotation cadence + personnel-change trigger in runbook | nse-requirements + eng-architect |
| FM-004-it005 | 192 | Wrong faithful-derivative comparator | REQ-022 AC: use `${TAG}..HEAD` not `origin/main..HEAD`; negative test | nse-requirements + eng-architect |
| FM-020-it005 | 192 | App over-scoped installation | Restrict App to `geekatron/jerry-cowork` only, `contents: write` only | eng-architect |
| FM-025-it005 | 192 | REQ-045 Environment gate absent | Configure `skeleton-push` Environment with branch deployment policy | eng-architect |
| FM-041-it005 | 192 | Single-actor registration no technical enforcement | REQ-043 labels this process control; REQ-047 is technical-detection compensator | nse-requirements |
| FM-006-it005 | 175 | Wrong source ref on workflow_dispatch | REQ-036: event-discriminated TAG resolution (IT3-005 fix in ADR-001 pseudocode) | nse-requirements + eng-architect |
| FM-061-it005 | 175 | Large blob accumulation | Track blob sizes per release in CI; optional strip documented in ADR-001 R-002 | nse-requirements |
| FM-010-it005 | 168 | Symlink breakage | REQ-009 AC: verify symlink targets are non-empty in CI; add explicit content check | nse-requirements |
| FM-059-it005 | 168 | Clone-weight growth unreported | REQ-034d: emit `size-pack` to GITHUB_STEP_SUMMARY every CI run | nse-requirements |
| FM-002-it005 | 140 | Stub determinism breach | REQ-004a Inspection + cross-run SHA comparison in REQ-003 AC | nse-requirements |

### Minor — Improvement opportunities (address after Phase 5 gate passes)

| FM | RPN | Finding | Note |
|----|-----|---------|------|
| FM-011-it005 | 72 | Trigger misconfiguration | REQ-011 Inspection AC covers this |
| FM-013-it005 | 75 | Missing concurrency guard | REQ-015 Inspection AC covers this |
| FM-017-it005 | 60 | Force-moved tag | Tag protection (REQ-039) prevents; D7 monitor detects |
| FM-038-it005 | 75 | Sigstore outage causes false positive | Meta-monitor (REQ-044) bounds outage duration |
| FM-045-it005 | 48 | Marketplace de-registration | REQ-047 monitor + recovery runbook |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | **Negative** | Five monitoring/detection controls are specified but not implemented (FM-015, FM-034, FM-039, FM-043 + FM-033 monitor correctness). The foundational R-001 multi-dimensional gate is a one-time snapshot (FM-060), not continuous. Per-release telemetry (FM-059, FM-062) missing from CI. |
| Internal Consistency | 0.20 | **Negative** | The design explicitly states "monitor MUST NOT use the `Source-Commit:` trailer" (ADR-001, ADR-003 D7) but no AC enforces this (FM-029). The faithful-derivative gate is specified as `${TAG}..HEAD` but the Phase-1 FM-09 bug (wrong comparator) may persist if REQ-022 AC is not updated (FM-004). RTB-3 notes two-admin approval has no technical enforcement while REQ-043 requires it (FM-041). |
| Methodological Rigor | 0.20 | **Negative** | The rogue-tag path (FM-032, RPN 243) remains open because D5 is designed but unimplemented. R-001 verification relies on a file-count-only CI gate when the ceiling might be size/time-based (FM-062). Single-shot rather than continuous verification (FM-060) violates the ADR-001 design intent of "continuous monitoring." |
| Evidence Quality | 0.15 | **Negative** | App private key exposure (FM-019, S=10) has REQ-045 Environment gate unimplemented. Monitor silent failure (FM-033, RPN 288) means the primary evidence of integrity (attestation verification) may be inert. Secret scan gate bypass (FM-007) means the artifact may contain credentials in the public repo. |
| Actionability | 0.15 | **Negative** | R-001 pivot scenario (FM-050) requires user decision before Phase 5 but the multi-dimensional smoke test is not yet complete. Liveness monitor absence (FM-015) means staleness is not actionably detected. No user-facing update notification (FM-054) means security patches are invisible to users. |
| Traceability | 0.10 | **Mixed** | ADR→REQ traceability is well-documented across all five artifacts. RTB-5 (install-time verification gap, FM-049) is explicitly acknowledged as an accepted residual with stated rationale. However, several requirement ACs are incomplete (REQ-035, REQ-022, REQ-005) leaving the REQ→implementation trace open. |

**Overall Assessment:** The design (ADR-001 + ADR-003) is architecturally sound and addresses the Phase-1 criticals. The findings cluster around two categories: (1) monitoring controls specified but not yet demonstrated functional, and (2) the foundational R-001 assumption unverified. Neither category reflects flawed design thinking; both reflect the implementation gap inherent in "Proposed" status artifacts. The deliverable should be marked REVISE and the corrective actions above must be implemented before Phase 5 implementation begins.

---

## Execution Statistics

- **Total Findings:** 31 (selected from 62 enumerated across 9 components)
- **Critical:** 15 (RPN ≥ 200: 13; S ≥ 9 additional: 2 — FM-007, FM-051)
- **Major:** 11
- **Minor:** 5
- **Protocol Steps Completed:** 5 of 5
- **Highest-RPN Finding:** FM-033-it005 (Monitor Silent Failure) and FM-062-it005 (File-count ceiling type unconfirmed) — both estimated RPN = 288
- **Top Uncontrolled Finding by D-score:** FM-032-it005 (Rogue Tag Self-Certification) — D=9, RPN=243; D5 provenance gate not yet implemented; monitor returns MATCH on malicious build
- **Phase 5 Blockers:** FM-032 (D5 not implemented), FM-046/FM-050 (R-001 unverified), FM-033 (monitor silent failure), FM-034 (meta-monitor absent), FM-043 (org-registration monitor absent), FM-039 (monitor not demonstrated)

---

*Strategy: S-012 FMEA (Failure Mode and Effects Analysis)*
*Template: `.context/templates/adversarial/s-012-fmea.md` v1.0.0*
*Execution ID: it005*
*Executed: 2026-06-29*
*Agent: adv-executor*
*H-15 Self-Review: Applied before persistence — all Critical findings have specific evidence from the deliverables; severity classifications verified against RPN ≥ 200 / S ≥ 9 thresholds; summary table counts match detailed findings; no findings omitted or minimized.*
