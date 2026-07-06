# Strategy Execution Report: FMEA — Failure Mode and Effects Analysis (S-012)

## Execution Context

- **Strategy:** S-012 (FMEA — Failure Mode and Effects Analysis)
- **Execution ID:** it006
- **Finding Prefix:** FM-NNN-it006
- **Template:** `.context/templates/adversarial/s-012-fmea.md`
- **Deliverable:** PROJ-031-cowork-skeleton (5 design artifacts — see Scope below)
- **Executed:** 2026-06-28T00:00:00Z
- **Tournament:** C4 Group E, iteration-006 (blind)
- **Criticality:** C4

**Scope — 5 Input Artifacts (read in full, no adversary/ files read per blindness constraint):**
1. `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md`
2. `projects/PROJ-031-cowork-skeleton/decisions/ADR-003-credential-protection-supply-chain.md`
3. `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md`
4. `projects/PROJ-031-cowork-skeleton/security/phase2-stride-threat-model.md`
5. `projects/PROJ-031-cowork-skeleton/security/phase2-attack-surface.md` (historical recon; threat-intelligence provenance only — SUPERSEDED banner respected)

**RPN Note (P-022):** All S/O/D/RPN values in this report are **estimates** based on design artifact review. No production system exists; no implemented components have been exercised.

---

## Executive Summary

FMEA of the PROJ-031 Jerry → CoWork dedicated-repo distribution pipeline identified **31 failure modes: 20 Critical, 11 Major, 0 Minor**. The highest-RPN mode is **FM-025-it006** (RTB-5: CoWork platform does not invoke `gh attestation verify` at install time; RPN=567 estimated) — a design boundary, not a remediable defect. The most operationally significant finding is **FM-026-it006** (CoWork update propagation to already-installed users is completely unverified; RPN=486 estimated), which undermines the core "automatically in sync" value proposition. Seven failure modes are classified as "missing by omission" — no named gate, no automated enforcement, and no Phase-5 remediation path documented; these require explicit ADR-003 revision before go-live.

---

## Findings Summary Table

All RPN values are **estimates** per P-022.

| ID | Component | Failure Mode | S | O | D | RPN (est.) | Severity | Type |
|---|---|---|---|---|---|---|---|---|
| FM-025-it006 | I: Distribution/Install | RTB-5: CoWork platform does not invoke `gh attestation verify` at install-time | 7 | 9 | 9 | 567 | Critical | Design boundary |
| FM-026-it006 | J: Update propagation | CoWork update propagation to already-installed users unverified (G-update unexamined black box) | 9 | 6 | 9 | 486 | Critical | Phase-5-deferred |
| FM-012-it006 | E: Monitor | Monitor exits 0 on unhandled crash — FM-033 silent-pass mode | 9 | 5 | 9 | 405 | Critical | Phase-5-deferred |
| FM-019-it006 | F: D8 content gate | D8 scanner crash → exit 0 → unscanned artifact attested and pushed | 9 | 5 | 9 | 405 | Critical | Phase-5-deferred |
| FM-017-it006 | F: D8 content gate | D8 gate placed after attestation+push in job dependency graph (attested artifact is unscanned) | 9 | 5 | 8 | 360 | Critical | Phase-5-deferred |
| FM-018-it006 | F: D8 content gate | D8 pattern catalog empty or unreviewed at launch (gate runs; catches nothing) | 9 | 5 | 8 | 360 | Critical | Phase-5-deferred |
| FM-013-it006 | E: Monitor | Freshness check absent; stale-but-validly-attested skeleton passes integrity check (IN-002/SC-07) | 8 | 5 | 8 | 320 | Critical | Phase-5-deferred |
| FM-009-it006 | D: Attestation gen/verify | D5 provenance gate designed-not-implemented; rogue-tag path fully open (FM-032) | 9 | 4 | 8 | 288 | Critical | Phase-5-deferred |
| FM-014-it006 | E: Monitor | Meta-monitor absent (REQ-044); monitor itself can be down for hours undetected | 7 | 5 | 8 | 280 | Critical | Phase-5-deferred |
| FM-029-it006 | K: Headroom | Live CoWork install smoke test (G-headroom dim-d) deferred; only 3 CI dimensions run | 8 | 5 | 7 | 280 | Critical | Phase-5-deferred |
| FM-001-it006 | A: Skeleton generation | Symlink `.claude/rules` → `.context/rules` broken in CoWork env (Linux CI passes; CoWork unverified) | 8 | 4 | 8 | 256 | Critical | Phase-5-deferred |
| FM-010-it006 | D: Attestation gen/verify | Attestation verify path unproven on target (`geekatron/jerry-cowork` does not yet exist) | 8 | 4 | 7 | 224 | Critical | Phase-5-deferred |
| FM-020-it006 | F: D8 content gate | D8 scan scope excludes `.claude/` or `commands/` — primary SC-08 attack surface unprotected | 8 | 4 | 7 | 224 | Critical | Phase-5-deferred |
| FM-007-it006 | C: Credential/App token | Fine-grained PAT interim credential becomes permanent; no automated credential-type enforcement | 8 | 4 | 7 | 224 | Critical | Missing by omission |
| FM-024-it006 | H: Org-marketplace reg. | No technical enforcement of two-admin approval for registration change (RTB-3 process-only) | 8 | 4 | 7 | 224 | Critical | Design boundary |
| FM-028-it006 | K: Headroom | CoWork enforces size/time ceiling but not file-count ceiling; file-count gate may falsely pass | 8 | 4 | 7 | 224 | Critical | Phase-5-deferred |
| FM-022-it006 | G: Auto-revert | Monitor opens issue but does not dispatch `workflow_dispatch`; REQ-053 auto-revert not triggered | 7 | 5 | 6 | 210 | Critical | Phase-5-deferred |
| FM-027-it006 | J: Update propagation | Go-live proceeds before G-update empirically verified (schedule-pressure process bypass) | 9 | 3 | 7 | 189 | Critical (S=9) | Phase-5-deferred |
| FM-023-it006 | H: Org-marketplace reg. | Org-admin registers rogue or typosquat repo; all org users receive malicious skeleton | 9 | 3 | 6 | 162 | Critical (S=9) | Phase-5-deferred |
| FM-003-it006 | A: Skeleton generation | `marketplace.json` absent from generated tree → all CoWork installs fail silently | 9 | 2 | 2 | 36 | Critical (S=9) | Phase-5-deferred |
| FM-006-it006 | C: Credential/App token | App private key without Environment-level deployment protection (REQ-045 designed, not enforced) | 8 | 3 | 8 | 192 | Major | Phase-5-deferred |
| FM-011-it006 | D: Attestation gen/verify | Per-job permissions isolation absent; `id-token` + `contents:write` co-located in single job | 8 | 4 | 6 | 192 | Major | Missing by omission |
| FM-021-it006 | G: Auto-revert | Auto-revert re-deploys undefined "last-good" tag (no specification for target determination) | 8 | 4 | 6 | 192 | Major | Missing by omission |
| FM-016-it006 | E: Monitor | Monitor workflow lacks `actions:write`; `workflow_dispatch` call silently fails | 7 | 5 | 5 | 175 | Major | Phase-5-deferred |
| FM-002-it006 | A: Skeleton generation | Dynamic content in stub `projects/README.md` breaks bit-identical idempotency | 7 | 4 | 6 | 168 | Major | Phase-5-deferred |
| FM-030-it006 | A: Skeleton generation | Plugin retention surface (ADR-001 c-003) out of sync with `plugin.json`; new agents silently excluded | 8 | 4 | 5 | 160 | Major | Missing by omission |
| FM-015-it006 | E: Monitor | Monitor `cowork-monitor.yml` hosted in dedicated repo; overwritten on every release cycle | 8 | 3 | 6 | 144 | Major | Missing by omission |
| FM-005-it006 | B: CI liveness | CI regeneration fails silently; REQ-049 ≤2h liveness window is post-failure detection only | 7 | 4 | 4 | 112 | Major | Phase-5-deferred |
| FM-031-it006 | K: Headroom | Clone weight grows monotonically under Option A (full-provenance history); no bounded ceiling | 5 | 7 | 3 | 105 | Major | Phase-5-deferred |
| FM-004-it006 | B: CI liveness | `workflow_dispatch` blank `inputs.target_tag` resolves unintended ref (IT3-005 pattern) | 7 | 3 | 5 | 105 | Major | Phase-5-deferred |
| FM-008-it006 | C: Credential/App token | Source `GITHUB_TOKEN` used for cross-repo push (non-viable; push fails with auth error at runtime) | 8 | 2 | 3 | 48 | Major (S=8) | Missing by omission |

---

## Detailed Findings — Critical

### FM-025-it006: RTB-5 — CoWork Platform Does Not Verify Attestation at Install Time

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 7 / 9 / 9 / 567 (estimated) |
| **Component** | I: Distribution/Install |
| **Type** | Design boundary |
| **Protocol Step** | Step 4: Prioritize (high-D, high-O) |

**Evidence:** ADR-003 RTB-5 states: "CoWork install flow does NOT invoke `gh attestation verify`; D7 monitor is the sole automated verifier (post-publication)." The trust gap is explicitly acknowledged as a residual trust boundary. O=9 because every single install exercises this gap.

**Analysis:** The install-time verification gap is permanent at this architecture layer — the CoWork platform controls the install flow, not the Jerry project. With O=9 (every install) and D=9 (no detection at install time, only post-publication by monitor), this is the highest-RPN mode in the model. A supply-chain compromise that subverts the attestation chain can deliver malicious content to all users simultaneously before the ≤6h monitor fires.

**Remediation:** OWNER: ADR → ps-architect. Partially mitigated by D7 fail-closed monitor. Document RTB-5 explicitly in go-live security acceptance as a permanent residual risk. Evaluate whether a wrapper install script invoking `gh attestation verify` before workspace activation is feasible on the CoWork platform. Log in project risk register with residual risk owner assigned.

---

### FM-026-it006: CoWork Update Propagation to Already-Installed Users Unverified

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 9 / 6 / 9 / 486 (estimated) |
| **Component** | J: Update propagation |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Insufficient), Step 4 (Prioritize) |

**Evidence:** ADR-001 Phase-5 gate G-update is defined but explicitly unverified: "CoWork update propagation UNVERIFIED for already-installed users — only install-time behavior confirmed; update behavior for existing users is an unexamined black box." STK-002 stakeholder requirement re-scoped as contingent on G-update.

**Analysis:** The core "automatically in sync" value proposition (STK-001) depends entirely on CoWork propagating skeleton updates to already-installed workspaces. This has never been empirically tested. S=9 (if updates do not propagate, users operate on stale or compromised skeleton they believe is current); D=9 (no automated check verifies installed-user version post-install). This is the most operationally significant finding in the model.

**Remediation:** OWNER: requirements → nse-requirements; ADR → ps-architect. G-update MUST be a non-deferrable, explicit go-live gate. Test protocol: (1) install CoWork plugin in test workspace, (2) push new tagged release to `geekatron/jerry-cowork`, (3) verify update propagated to already-installed workspace within ≤2h. If CoWork does not propagate updates automatically, the entire distribution model requires architectural redesign before go-live. BLOCK go-live until G-update passes empirically.

---

### FM-012-it006: Monitor Silent-Exit-0 Crash Mode (FM-033)

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 9 / 5 / 9 / 405 (estimated) |
| **Component** | E: Integrity monitor / ≤6h freshness poll |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Missing), Step 3 (Rate — D=9 silent failure) |

**Evidence:** ADR-003 D7(c) explicitly flags: "FM-033 silent-exit-0 mode: Monitor that crashes and exits 0 appears to be working." The monitor is the last line of defense for post-publication integrity.

**Analysis:** A monitor that silently succeeds after crashing provides false security assurance. If the monitor exits 0 on an unhandled exception (common without defensive coding), a compromised or stale skeleton persists for ≤6h or indefinitely with no alert. D=9 because the failure mode is externally indistinguishable from a passing run — the CI job shows green.

**Remediation:** OWNER: ADR → ps-architect. Implement defensive exit strategy: `set -euo pipefail` in monitor shell script; all Python code wrapped in explicit exception handlers with `sys.exit(1)` on catch. G-monitor acceptance test: inject deliberate crash into monitor code, confirm CI job status is red (failure), confirm no false-positive suppression of alert. This test MUST be in the G-monitor suite before go-live.

---

### FM-019-it006: D8 Content Gate Not Fail-Closed (Scanner Crash → Exit 0)

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 9 / 5 / 9 / 405 (estimated) |
| **Component** | F: D8 content-safety gate |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Missing), Step 3 (Rate — D=9) |

**Evidence:** ADR-003 D8 specifies "Fail-closed D8: scanner crash → exit non-zero → no attestation/push" but this is "designed — operational validation pending [G-content]." The STRIDE model notes fail-closed is an eng-architect-owned specification, not yet validated.

**Analysis:** If the scanner implementation exits 0 on crash (common for many tools without explicit error handling), an unscanned artifact proceeds to attestation and push. SC-08 (prompt injection in retained markdown, STRIDE rank-2 threat) would pass undetected. This failure mode is indistinguishable from a clean scan externally.

**Remediation:** OWNER: STRIDE/security → eng-architect. Add explicit exit-code contract to D8 scanner specification: scanner MUST exit non-zero on any error (parse error, timeout, OOM, unhandled exception). G-content acceptance tests MUST include: (a) inject deliberate scanner crash, verify pipeline halts red; (b) inject known-bad SC-08 pattern, verify rejection and pipeline halt.

---

### FM-017-it006: D8 Gate Placed After Attestation+Push (Incorrect Job Dependency)

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 9 / 5 / 8 / 360 (estimated) |
| **Component** | F: D8 content-safety gate |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Incorrect ordering), Step 3 (Rate) |

**Evidence:** ADR-003 pipeline sequence correctly shows D8 before ATTEST in the main job. However, ADR-003 also describes ATTEST and push as separate jobs: "ATTEST tip SHA (D4, separate job: id-token+attestations, NO contents)" and "cross-repo force-push (D3, push job: contents:write only)." Without explicit `needs:` declarations enforcing D8-before-ATTEST dependency, a misconfigured workflow could run jobs in parallel or out of order.

**Analysis:** If D8 and the ATTEST job run in parallel (or if D8 is accidentally positioned after ATTEST), the attested artifact is unscanned. S=9 (attested-but-unscanned artifact is indistinguishable from a verified one); O=5 (implementation error risk during workflow construction); D=8 (no automated ordering check in CI YAML).

**Remediation:** OWNER: ADR → ps-architect; requirements → nse-requirements. Add REQ-0XX: content-safety gate (D8) SHALL complete and pass before attestation job is triggered. Add CI YAML contract: ATTEST job MUST declare `needs: [content-safety]`. Add G-content validation test: verify D8 job failure blocks ATTEST job from running.

---

### FM-018-it006: D8 Pattern Catalog Empty or Unreviewed at Launch

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 9 / 5 / 8 / 360 (estimated) |
| **Component** | F: D8 content-safety gate |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Insufficient), Step 3 (Rate) |

**Evidence:** STRIDE threat model documents D8 Pattern catalog C1-C6 (system-override/role-reversal, data-exfiltration directives, unauthorized agentic action, LLM control tokens, covert-channel/obfuscation, credential/secret solicitation) as eng-architect-owned. ADR-003 states "D8 pattern catalog handed to eng-architect but unspecified in ADR-003." No catalog content, no review process, no acceptance criteria appear in any of the 5 input artifacts.

**Analysis:** A content-safety gate that runs against an empty or unreviewed pattern catalog provides false assurance. SC-08 (STRIDE rank-2 threat by 10Y impact) targets the `.claude/` and `commands/` retained surfaces. With an empty catalog, the gate passes every build while catching nothing.

**Remediation:** OWNER: STRIDE/security → eng-architect. Specify D8 pattern catalog C1-C6 with at minimum one confirmed-positive test case per category. G-content acceptance criterion: each C1-C6 category MUST have a positive detection test that causes the gate to reject. Timeline gate: catalog must be specified and reviewed before G-provenance opens — catalog cannot be deferred to post-launch.

---

### FM-013-it006: Freshness Check Absent — Stale-but-Attested Skeleton Passes Integrity Check

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 8 / 5 / 8 / 320 (estimated) |
| **Component** | E: Integrity monitor / ≤6h freshness poll |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Missing), Step 3 (Rate) |

**Evidence:** ADR-003 D7 specifies freshness check: "FRESHNESS: newest v* tag deployed ≤2h?" REQ-049 mandates liveness/freshness. However, the monitor is "Designed — operational validation pending [G-monitor]." IN-002/SC-07 (stale-but-validly-attested deployment) is explicitly identified in the design.

**Analysis:** Integrity-only verification (D4 attestation check alone) cannot distinguish "deployed correctly from latest tag" from "deployed correctly from 30-day-old tag." A CI regeneration failure that silently stops producing new skeletons would return PASS on the attestation check indefinitely — the skeleton was validly attested when generated. Freshness is the only control that detects IN-002.

**Remediation:** OWNER: ADR → ps-architect; requirements → nse-requirements. REQ-049 is defined; add G-monitor acceptance test: simulate stale deployment (block CI from firing for a release cycle), verify monitor fires FAIL within ≤6h. Verify REQ-049 ≤2h window implementation: "newest v* tag deployed ≤2h" means the latest source tag appears in the dedicated repo within 2h of its creation — not 2h since monitor last ran.

---

### FM-009-it006: D5 Provenance Gate Designed-Not-Implemented

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 9 / 4 / 8 / 288 (estimated) |
| **Component** | D: Sigstore attestation gen/verify |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Missing), Step 3 (Rate) |

**Evidence:** ADR-003 D5: "Designed — operational validation pending [G-provenance]; specified, NOT yet implemented (FM-032)." D5 is the provenance gate: the check that the source tag SHA was produced by authorized CI from the legitimate source repo.

**Analysis:** Without D5, a rogue tag (SC-02, STRIDE rank-1 threat by 10Y) bypasses source validation entirely. D2 (org-level ruleset, CI sole bypass actor) provides partial protection but D5 is the explicit verify-before-process gate inside the workflow. S=9 (rogue content distributed at scale to all CoWork users); D=8 (no runtime check; only post-hoc audit trail).

**Remediation:** OWNER: ADR → ps-architect; STRIDE/security → eng-architect. D5 MUST be implemented before G-provenance can pass. Implementation: verify source tag is signed, verify tag SHA matches expected format, verify triggering actor is authorized. G-provenance acceptance test: attempt workflow trigger with unsigned/rogue tag, verify D5 rejects it and pipeline halts.

---

### FM-014-it006: Meta-Monitor Absent — Monitor Outage Undetected for Hours

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 7 / 5 / 8 / 280 (estimated) |
| **Component** | E: Integrity monitor / ≤6h freshness poll |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Missing) |

**Evidence:** REQ-044 specifies meta-monitor (monitor-of-the-monitor). ADR-003 D7 does not describe a meta-monitor implementation. Phase-5 gate G-monitor acceptance criteria do not include meta-monitor validation in any of the 5 input artifacts.

**Analysis:** If the scheduled monitor workflow fails silently (runner outage, billing suspension, YAML parse error after a force-push overwrites it per FM-015), the failure is invisible. No alert fires. The security property degrades silently. A monitoring system with no availability tracking is untrustworthy as a security control. D=8 (no automated detection of monitor outage itself).

**Remediation:** OWNER: requirements → nse-requirements; ADR → ps-architect. Implement REQ-044: configure external Dead Man's Snitch or Pingdom webhook called by monitor at start of each run; absence of expected heartbeat within ≤8h triggers alert. Add G-monitor acceptance criterion: simulate scheduled workflow failure, verify external alert fires within ≤8h.

---

### FM-029-it006: Live CoWork Install Smoke Test Deferred — G-Headroom 4th Dimension Not Run

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 8 / 5 / 7 / 280 (estimated) |
| **Component** | K: File-count/size/time headroom |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Insufficient), Step 3 (Rate) |

**Evidence:** REQ-006 mandates multi-dimensional gate: file count AND pack size AND clone time. phase1-requirements.md notes the "MAY defer dimension (d)" clause has been removed — all 4 dimensions mandatory. Dimension (d) is a live CoWork install smoke test. This gate requires `geekatron/jerry-cowork` to exist, which it does not yet.

**Analysis:** CI gates verify dimensions measurable in GitHub Actions. A live CoWork install test is the only way to verify the generated skeleton is actually installable by the CoWork platform as a user workspace. Skipping this means the distribution model is unvalidated end-to-end until a real user encounters failure. D=7 (failure only detected when real user reports inability to install).

**Remediation:** OWNER: requirements → nse-requirements; ADR → ps-architect. G-headroom MUST include live CoWork install: install plugin from `geekatron/jerry-cowork`, verify plugin appears in workspace, verify `.claude/rules/` is populated. Prerequisite: `geekatron/jerry-cowork` must be created before this gate can run. Track as go-live blocker.

---

### FM-001-it006: Symlink `.claude/rules → .context/rules` Broken in CoWork Environment

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 8 / 4 / 8 / 256 (estimated) |
| **Component** | A: Skeleton generation |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Missing detection), Step 3 (Rate) |

**Evidence:** ADR-001 canonical plugin-retention surface (c-003) lists `.claude/rules` as a symlink to `.context/rules`. The skeleton retains both `.context/` and `.claude/` directories but behavior of symlinks in the CoWork install environment is unverified. Linux CI passes because it resolves symlinks natively. D=8: this failure would only be detected by a live install test (G-headroom dim-d, currently deferred).

**Analysis:** If the CoWork platform does not resolve symlinks at install time (or presents them as broken), `.claude/rules/` is empty or broken in every installed workspace. This silently disables all L1 rule enforcement for CoWork users — the foundational behavioral constraint layer of the Jerry framework. No user-visible error on install.

**Remediation:** OWNER: ADR → ps-architect. Add G-headroom acceptance criterion: verify `.claude/rules/` is populated (not empty, not broken symlink) in installed CoWork workspace. Consider flattening: replace symlink with explicit directory copy in skeleton generation script if CoWork platform does not resolve symlinks.

---

### FM-010-it006: Attestation Verify Path Unproven on Target Repository

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 8 / 4 / 7 / 224 (estimated) |
| **Component** | D: Sigstore attestation gen/verify |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Missing), Step 3 (Rate) |

**Evidence:** `geekatron/jerry-cowork` does not yet exist. All attestation generation and verification logic is designed against a non-existent target repository. G-provenance gate is the named remediation path.

**Analysis:** Sigstore/GitHub attestation has non-trivial path requirements: repository must exist, `id-token` permissions must be granted in the correct job scope, `gh attestation verify` must be invoked with correct artifact path and `--owner` flag. None of these have been exercised on the actual target repo. A smoke test in CI using a dummy artifact does not substitute for end-to-end path validation on the actual distribution repo.

**Remediation:** OWNER: ADR → ps-architect. G-provenance acceptance: run complete generate → attest → verify cycle on actual `geekatron/jerry-cowork` before go-live. This requires the dedicated repo to be created as a prerequisite gate. Create `geekatron/jerry-cowork` as the first go-live prerequisite.

---

### FM-020-it006: D8 Scan Scope Excludes `.claude/` or `commands/`

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 8 / 4 / 7 / 224 (estimated) |
| **Component** | F: D8 content-safety gate |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Insufficient scope), Step 3 (Rate) |

**Evidence:** STRIDE identifies SC-08 (prompt injection in retained markdown) targeting `.claude/` and `commands/` as rank-2 threat. D8 pattern catalog C1-C6 is eng-architect-owned but unspecified. Scan scope is not documented in any of the 5 input artifacts.

**Analysis:** If D8 scans only `projects/README.md` (the stub content) and not the retained `.claude/`, `commands/`, or `.context/rules/` directories, the primary attack surface (SC-08) is unprotected. The gate runs, passes clean on stub content, and prompt-injected rule files propagate undetected to all CoWork workspaces. The only CONTENT threat in the STRIDE model (SC-08 / RT-001 / PM-003) is exclusively in this retained surface.

**Remediation:** OWNER: STRIDE/security → eng-architect. D8 scan scope MUST explicitly include `.claude/`, `commands/`, `.context/rules/`. Add REQ-0XX: D8 scan scope SHALL cover all directories in the plugin-retention surface (ADR-001 c-003 canonical 9-entry list). G-content test: inject known SC-08 pattern into `.claude/rules/` file, verify D8 catches it and pipeline halts.

---

### FM-007-it006: Fine-Grained PAT Interim Credential Becomes Permanent

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 8 / 4 / 7 / 224 (estimated) |
| **Component** | C: Credential/App token |
| **Type** | Missing by omission |
| **Protocol Step** | Step 2 (Enumerate — Incorrect/decayed state), Step 3 (Rate) |

**Evidence:** ADR-003 D3 specifies GitHub App token (1h) as the preferred credential, with fine-grained PAT as interim. No automated enforcement, expiry check, or credential-type migration gate exists in any of the 5 input artifacts. No Phase-5 gate is named for credential type enforcement. This is "missing by omission."

**Analysis:** "Interim" credentials become permanent through organizational inertia. A fine-grained PAT has longer effective lifetime than a 1h App token, broader blast radius if leaked (person-scoped, not org-App-scoped), and is associated with a personal GitHub account. The migration from PAT to App token has no technical enforcement. D=7: only detected by manual credential audit triggered by process reminder.

**Remediation:** OWNER: requirements → nse-requirements; ADR → ps-architect. Add REQ-0XX: go-live credential MUST be GitHub App token (not PAT). Add G-prevention acceptance criterion: verify App installation exists in geekatron org, verify CI workflow uses App-generated token (verify via `github.actor` contains `[bot]` suffix). Add 90-day post-launch calendar reminder for credential type audit.

---

### FM-024-it006: No Technical Enforcement of Two-Admin Approval for Registration Change

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 8 / 4 / 7 / 224 (estimated) |
| **Component** | H: Org-marketplace registration |
| **Type** | Design boundary |
| **Protocol Step** | Step 2 (Enumerate — Insufficient), Step 3 (Rate) |

**Evidence:** ADR-003 RTB-3: "Org-admin registration change requires two-admin approval (process control only)." No GitHub platform mechanism enforces two-person integrity for marketplace registration changes.

**Analysis:** A compromised or rogue org-admin can change the CoWork marketplace registration without any technical barrier. Process controls degrade over time and under social engineering pressure. S=8 (all org users affected by registration change directing to rogue repo); D=7 (change visible in audit log, but not in real time — discovery depends on audit frequency).

**Remediation:** OWNER: ADR → ps-architect. Accept as RTB-3 design boundary. Mitigations: (a) reduce org-admins to minimum viable count, (b) enable GitHub audit log streaming to external SIEM with real-time alert on marketplace registration change event, (c) add monitor scope extension: verify registration still points to `geekatron/jerry-cowork` on every ≤6h cycle, (d) document RTB-3 explicitly in go-live security acceptance.

---

### FM-028-it006: CoWork Enforces Size/Time Ceiling But Not File-Count Ceiling

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 8 / 4 / 7 / 224 (estimated) |
| **Component** | K: File-count/size/time headroom |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Inconsistent), Step 3 (Rate) |

**Evidence:** ADR-001 REQ-006: multi-dimensional gate: "file count AND pack size AND clone time." ADR-001 describes the CoWork platform's own ceiling as size/time-based (IN-001 reference pattern). No file-count ceiling exists on the CoWork platform side; this dimension is Jerry-internal only.

**Analysis:** If the CI file-count threshold is miscalibrated (too permissive), a skeleton that exceeds the operational file-count ceiling reaches users. The CoWork platform will install it (no platform-side rejection), but IDE performance degrades, context window floods, and `.claude/rules/` processing overhead increases. Detection: O=4 (error is possible on calibration miss), D=7 (only detected by live install smoke test or user reports).

**Remediation:** OWNER: ADR → ps-architect; requirements → nse-requirements. Add G-headroom acceptance criterion: verify current skeleton file count is substantially below threshold (target: ≤80% of CI gate limit). Document file-count threshold with rationale. Add CI alerting at 80% of threshold (early warning band). Investigate whether CoWork platform provides file-count metrics post-install.

---

### FM-022-it006: Monitor Opens Issue But Does Not Dispatch `workflow_dispatch` for Auto-Revert

| Attribute | Value |
|---|---|
| **Severity** | Critical |
| **S / O / D / RPN** | 7 / 5 / 6 / 210 (estimated) |
| **Component** | G: Auto-revert (REQ-053, actions:write) |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Missing), Step 3 (Rate) |

**Evidence:** ADR-003 REQ-053: "auto-revert SHALL [trigger] workflow_dispatch." Monitor is "Designed — operational validation pending." No implementation specification for the `workflow_dispatch` trigger mechanism exists in the 5 input artifacts.

**Analysis:** If the monitor implements only issue-opening (softer response) without triggering the revert workflow, the security property degrades from auto-revert to human-in-the-loop revert. Depending on response time, this creates a window potentially hours wide during which a compromised skeleton remains deployed. D=6 (failure visible via GitHub Issue, but no automated response fires and no SLA is enforced).

**Remediation:** OWNER: ADR → ps-architect; requirements → nse-requirements. Specify `workflow_dispatch` API call in monitor implementation: `gh workflow run regenerate.yml --repo geekatron/jerry --field target_tag=<last_good>`. G-monitor acceptance test: trigger monitor failure condition, verify `workflow_dispatch` fires within 5 minutes, verify skeleton is reverted within ≤2h. Distinct from FM-016 (missing `actions:write` permission preventing dispatch from succeeding).

---

### FM-027-it006: Go-Live Before G-Update Empirically Verified

| Attribute | Value |
|---|---|
| **Severity** | Critical (S=9) |
| **S / O / D / RPN** | 9 / 3 / 7 / 189 (estimated) |
| **Component** | J: Update propagation |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 4: Prioritize (schedule-pressure bypass) |

**Evidence:** G-update is defined as a Phase-5 gate. STK-002 is re-scoped as contingent on G-update. There is no technical blocker preventing go-live without G-update passing — only a process commitment. The "contingent on G-update" phrasing could be misread as "STK-002 is optional" rather than "G-update is non-deferrable."

**Analysis:** Under schedule pressure, teams defer gates described as contingent. S=9: if users are told CoWork "automatically stays in sync" before this is empirically verified, and updates do not propagate, users trust a false security property indefinitely. O=3 (requires schedule pressure AND misreading of gate language). D=7 (failure detected when users report stale skeletons or when G-update is eventually run).

**Remediation:** OWNER: requirements → nse-requirements. Add explicit REQ-0XX: G-update SHALL pass before go-live is approved. Add language clarifying: STK-002 re-scope means the scope is deferred, NOT that G-update itself is optional. G-update is non-deferrable regardless of STK-002 contingency status.

---

### FM-023-it006: Org-Admin Registers Rogue or Typosquat Repository

| Attribute | Value |
|---|---|
| **Severity** | Critical (S=9) |
| **S / O / D / RPN** | 9 / 3 / 6 / 162 (estimated) |
| **Component** | H: Org-marketplace registration |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — OR-01/OR-02), Step 3 (Rate) |

**Evidence:** STRIDE threat model SC-02 (rogue tag) is rank-1 by 10Y impact. FM-024 (RTB-3 process-only control for registration change) is a direct precondition. STRIDE also documents OR-01 (typosquat registration) and OR-02 (registration redirect attack).

**Analysis:** A compromised org-admin (or social engineering success) could change the CoWork marketplace registration from `geekatron/jerry-cowork` to a rogue repository. All CoWork users in the org receive skeleton from the rogue repo on next update cycle. S=9 (all users receive malicious skeleton); O=3 (requires compromised admin, rare but not negligible for long-lived deployments); D=6 (visible in GitHub audit log with 24-hour lag).

**Remediation:** OWNER: STRIDE/security → eng-architect; ADR → ps-architect. Accept as residual risk at the platform boundary. Mitigations: (a) audit log streaming with real-time alert (see FM-024), (b) add to monitor scope: each ≤6h cycle verifies registration target is `geekatron/jerry-cowork`, (c) minimum-admin-count policy, (d) document in go-live security acceptance with residual risk owner.

---

### FM-003-it006: `marketplace.json` Absent from Generated Tree

| Attribute | Value |
|---|---|
| **Severity** | Critical (S=9) |
| **S / O / D / RPN** | 9 / 2 / 2 / 36 (estimated) |
| **Component** | A: Skeleton generation |
| **Type** | Phase-5-deferred |
| **Protocol Step** | Step 2 (Enumerate — Missing), Step 3 (Rate) |

**Evidence:** ADR-001 c-003 canonical plugin-retention surface: `.claude-plugin/` MUST contain BOTH `plugin.json` AND `marketplace.json`. If the strip set accidentally removes `marketplace.json` or it is absent from the source repo, all CoWork installs fail.

**Analysis:** S=9 (all installs fail); O=2 (low probability given explicit retention surface specification); D=2 (immediately visible — CI headroom gate fails or all users simultaneously report installation failure). Despite low RPN (36 estimated), classified Critical by S=9 rule. The well-detected nature means this is a low-priority remediation target relative to the high-D failure modes.

**Remediation:** OWNER: ADR → ps-architect. Add CI assertion: verify `.claude-plugin/marketplace.json` exists in generated tree before force-push. Add G-headroom acceptance criterion: verify CoWork can read and parse `marketplace.json` during live install smoke test. Track `marketplace.json` creation as a prerequisite item before dedicated repo creation.

---

## Detailed Findings — Major

| ID | Failure Mode | S | O | D | RPN (est.) | Type | Remediation Owner |
|---|---|---|---|---|---|---|---|
| FM-006-it006 | App private key without Environment-level deployment protection (REQ-045 designed, not enforced) | 8 | 3 | 8 | 192 | Phase-5-deferred | ADR → ps-architect |
| FM-011-it006 | Per-job permissions isolation absent: `id-token` + `contents:write` co-located in single job | 8 | 4 | 6 | 192 | Missing by omission | ADR → ps-architect; STRIDE → eng-architect |
| FM-021-it006 | Auto-revert re-deploys undefined "last-good" tag (no specification for target determination) | 8 | 4 | 6 | 192 | Missing by omission | ADR → ps-architect; requirements → nse-requirements |
| FM-016-it006 | Monitor workflow lacks `actions:write`; `workflow_dispatch` call silently fails at runtime | 7 | 5 | 5 | 175 | Phase-5-deferred | ADR → ps-architect |
| FM-002-it006 | Dynamic content in stub `projects/README.md` breaks bit-identical idempotency | 7 | 4 | 6 | 168 | Phase-5-deferred | ADR → ps-architect |
| FM-030-it006 | Plugin retention surface (ADR-001 c-003) out of sync with `plugin.json`; new agents silently excluded | 8 | 4 | 5 | 160 | Missing by omission | ADR → ps-architect |
| FM-015-it006 | Monitor `cowork-monitor.yml` hosted in dedicated repo; overwritten on every release cycle | 8 | 3 | 6 | 144 | Missing by omission | ADR → ps-architect |
| FM-005-it006 | CI regeneration fails silently; REQ-049 ≤2h liveness window is post-failure detection only | 7 | 4 | 4 | 112 | Phase-5-deferred | requirements → nse-requirements |
| FM-031-it006 | Clone weight grows monotonically under Option A full-provenance; no bounded ceiling before flip | 5 | 7 | 3 | 105 | Phase-5-deferred | ADR → ps-architect |
| FM-004-it006 | `workflow_dispatch` with blank `inputs.target_tag` resolves unintended ref (IT3-005 pattern) | 7 | 3 | 5 | 105 | Phase-5-deferred | ADR → ps-architect |
| FM-008-it006 | Source `GITHUB_TOKEN` used for cross-repo push (non-viable; fails with auth error at runtime) | 8 | 2 | 3 | 48 | Missing by omission | ADR → ps-architect |

**FM-011 analysis:** Co-locating `id-token` (attestation) and `contents:write` (push) permissions in a single job means a compromised step in the attestation phase has access to push credentials. Remediation: split into two jobs with explicit `permissions:` declarations; attest job gets only `id-token: write` + `attestations: write`; push job gets only `contents: write`. This is missing by omission — no existing ADR section or requirement specifies per-job permission isolation.

**FM-015 analysis:** `cowork-monitor.yml` is hosted in `geekatron/jerry-cowork`. Every CI regeneration overwrites `geekatron/jerry-cowork` via force-push. If `cowork-monitor.yml` is not explicitly in the plugin-retention surface (c-003), it is deleted on every push cycle, disabling the monitor silently. Remediation: either add `cowork-monitor.yml` to c-003 canonical retention surface, OR host the monitor in `geekatron/jerry` (source repo) with cross-repo dispatch.

**FM-021 analysis:** REQ-053 mandates auto-revert but specifies no target version. "Last-good" requires a validated-deployment history. Remediation: define `last-good` tracking: advance a dedicated tag `last-good-validated` only after a full G-monitor pass cycle. Auto-revert deploys this tag, not an arbitrary earlier version.

**FM-030 analysis:** The canonical plugin-retention surface (ADR-001 c-003: 9 static entries) does not auto-update as new agents are added to `skills/*/agents/*.md`. If `plugin.json` references a new agent but the retention surface does not include its parent directory, the agent is stripped from the skeleton silently. Remediation: generate retention surface dynamically from `plugin.json` agent manifest at skeleton generation time, rather than maintaining a static list.

**FM-008 analysis:** The source repo's `GITHUB_TOKEN` is scoped to `geekatron/jerry` only. Cross-repo push to `geekatron/jerry-cowork` requires an App token or deploy key (D3). Any workflow that falls back to `GITHUB_TOKEN` for the push step fails with a 403 auth error at runtime. This is a non-silent failure (push job fails red) but represents a design gap if the fallback credential is left unspecified. Classified as missing by omission: no fallback specification exists.

---

## Remediation Priority Matrix

| Priority | Failure Modes | Phase-5 Gate | Owner |
|---|---|---|---|
| **P0: Go-live blocker** | FM-026, FM-027 — G-update unverified (core value proposition unvalidated) | G-update | nse-requirements + ps-architect |
| **P0: Go-live blocker** | FM-012, FM-019 — Silent-exit-0: monitor + D8 gate | G-monitor, G-content | ps-architect + eng-architect |
| **P0: Go-live blocker** | FM-009 — D5 provenance gate not implemented | G-provenance | ps-architect + eng-architect |
| **P1: Critical — before first release** | FM-017, FM-018, FM-020 — D8 pipeline order, empty catalog, wrong scope | G-content | eng-architect |
| **P1: Critical — before first release** | FM-013, FM-014, FM-022, FM-016 — Freshness, meta-monitor, dispatch, actions:write | G-monitor | ps-architect |
| **P1: Critical — before first release** | FM-001, FM-010, FM-029 — Symlink, attest path, live smoke test | G-headroom, G-provenance | ps-architect |
| **P1: Critical — before first release** | FM-028 — File-count ceiling miscalibration | G-headroom | ps-architect |
| **P2: Missing by omission — spec before G-gates open** | FM-007 (PAT→App), FM-011 (per-job isolation), FM-015 (monitor hosting), FM-021 (last-good), FM-030 (retention surface) | ADR-003 rev | ps-architect |
| **P3: Design boundary — accept and document** | FM-025 (RTB-5: install-time verify), FM-024 (RTB-3: two-admin) | Risk register | ps-architect |
| **P4: Low RPN / well-detected** | FM-003, FM-008, FM-031, FM-002, FM-004, FM-005 | G-headroom, G-prevention | ps-architect |

---

## Scoring Impact Assessment

Per FMEA findings, the design has significant Phase-5-deferred risk concentrated in the D8 content gate (3 Critical findings at RPN ≥ 360), monitor liveness (4 Critical findings at RPN ≥ 280), and update propagation (2 Critical findings, highest operational impact). The "missing by omission" category (6 findings: FM-007, FM-008, FM-011, FM-015, FM-021, FM-030) represents gaps with no named Phase-5 remediation path — these require explicit ADR-003 revision.

| Dimension (S-014) | Impact Assessment |
|---|---|
| Completeness | Moderate gap — 6 missing-by-omission findings; D8 scope, last-good determination, per-job permission isolation, retention surface auto-generation not specified in any artifact |
| Internal Consistency | Minor gap — pipeline ordering ambiguity (FM-017: D8 vs. ATTEST job dependency) and monitor hosting conflict (FM-015: monitor overwritten by the very pipeline it monitors) create internal contradictions |
| Methodological Rigor | Moderate gap — D5 provenance gate specified but not implemented; D8 pattern catalog unspecified; G-update defined as a gate but missing empirical validation plan |
| Evidence Quality | Strong — all findings trace to specific ADR section, REQ number, STRIDE threat ID, or RTB designation |
| Actionability | Strong — all findings include OWNER tag (ps-architect / nse-requirements / eng-architect) and named Phase-5 gate or ADR revision target |
| Traceability | Strong — FM IDs, component labels, Phase-5 gate names, and STRIDE/ADR cross-references provided throughout |

---

## Execution Statistics

- **Total Findings:** 31
- **Critical:** 20
- **Major:** 11
- **Minor:** 0
- **Phase-5-Deferred (named gate exists; control designed, validation pending):** 23
- **Missing by Omission (no named gate, no automated enforcement):** 6 (FM-007, FM-008, FM-011, FM-015, FM-021, FM-030)
- **Design Boundary (platform limitation; accept and document as residual risk):** 2 (FM-024, FM-025)
- **Protocol Steps Completed:** 5 of 5 (Decompose → Enumerate → Rate → Prioritize → Synthesize)
- **Highest RPN:** FM-025-it006, RPN=567 (estimated) — RTB-5: CoWork install-time attestation not verified by platform
- **Most Operationally Critical:** FM-026-it006, RPN=486 (estimated) — CoWork update propagation to installed users completely unverified (S=9, D=9)
- **P0 Go-Live Blockers:** FM-026 (G-update), FM-027 (G-update bypass), FM-012 (monitor silent-exit-0), FM-019 (D8 not fail-closed), FM-009 (D5 not implemented)

---

*All S/O/D/RPN values are estimates per P-022. No production system exists; all ratings derived from design artifact review of 5 input files. BLINDNESS constraint honored: no files under `…/adversary/` were read.*

*adv-executor v1.0.0 | S-012 FMEA | Strategy template: `.context/templates/adversarial/s-012-fmea.md` | Executed: 2026-06-28*
