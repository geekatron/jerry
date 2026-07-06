# Chain-of-Verification Report: ADR-001, ADR-003, phase1-requirements.md (Phase 2)

**Strategy:** S-011 Chain-of-Verification
**Deliverables:** ADR-001-skeleton-derived-branch-strategy.md, ADR-003-credential-protection-supply-chain.md, requirements/phase1-requirements.md
**Criticality:** C4
**Date:** 2026-06-29
**Reviewer:** jerry:adv-executor (blind, Group D — Verify)
**H-16 Compliance:** S-003 Steelman applied prior to this iteration (confirmed per orchestration plan)
**Claims Extracted:** 16 | **Verified:** 9 | **Discrepancies:** 7 (2 Critical, 2 Major, 3 Minor collapsed to 1 Minor)
**Execution ID:** 20260629

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall verdict and verification rate |
| [Findings Table](#findings-table) | All findings at a glance |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, recommendation per finding |
| [Claim Inventory](#claim-inventory) | All 16 claims extracted and their disposition |
| [Traceability Check: D1–D6 to REQ](#traceability-check-d1d6-to-req) | Per-control trace status |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Protocol step completion |

---

## Summary

Sixteen testable claims were extracted from the three deliverables. Nine were independently verified as correct. Seven discrepancies were found, of which two are Critical (internal contradictions that make requirements unimplementable), two are Major (unverified security claims and missing verification gate), and one is Minor (in-document prose inconsistency already flagged in REQ-005). The most consequential finding is a direct contradiction between REQ-020 (forbids `id-token: write`) and REQ-042 (requires Sigstore attestation, which mandates `id-token: write`): one of these requirements must be relaxed before Phase 5. A second Critical finding concerns REQ-035's event-driven monitor, which cannot be implemented as described because GitHub Actions workflows cannot trigger on push events in a different repository. The deliverables are assessed **REVISE before Phase 5**: the two Critical findings are phase-blocking; the two Major findings require architectural clarification. Do not proceed to Phase 5 implementation until CV-001 and CV-002 are resolved.

---

## Findings Table

| ID | Severity | Target | Verification / Traceability Gap | Dimension |
|----|----------|--------|---------------------------------|-----------|
| [CV-001-20260629](#cv-001-20260629) | Critical | REQ-020 vs REQ-042 | REQ-020 forbids `id-token: write`; Sigstore attestation (REQ-042) requires it — mutual exclusion | Internal Consistency |
| [CV-002-20260629](#cv-002-20260629) | Critical | REQ-035 event-driven leg | GitHub Actions cannot trigger cross-repo; source-repo workflow cannot listen to push events in dedicated repo | Internal Consistency |
| [CV-003-20260629](#cv-003-20260629) | Major | ADR-003 D2 + REQ-040 | "Direct-push PREVENTED" claim; REQ-040 AC tests repo-admin bypass but not org-owner bypass | Evidence Quality |
| [CV-004-20260629](#cv-004-20260629) | Major | ADR-003 D4 + REQ-042 | "Resolves SC-04" claim; no REQ mandates attestation verification before installation — detection is scheduled (≤ 24 h), not pre-install | Completeness |
| [CV-005-20260629](#cv-005-20260629) | Minor | ADR-001 §Canonical Surface body | Body prose says `tests/` "retained today"; Phase 2 amendment strips it — prose not updated | Internal Consistency |

---

## Detailed Findings

### CV-001-20260629

**Title:** REQ-020 and REQ-042 Are Directly Contradictory on `id-token: write`

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Target** | REQ-020 (`cowork-skeleton.yml` permissions) and REQ-042 (Sigstore attestation) |
| **Strategy Step** | Step 4: Consistency Check |

**Claim (REQ-020):**
> "The `permissions:` block in `cowork-skeleton.yml` SHALL declare `contents: write` as the sole permission entry and SHALL NOT include `actions: write`, `packages: write`, `id-token: write`, or any organization-level scope."

**Claim (REQ-042):**
> "The CI workflow SHALL create an immutable GitHub Release and a build-provenance attestation (Sigstore-backed, SLSA-aligned, e.g., `gh attestation`) binding the skeleton tip SHA to the specific workflow run, source commit SHA, and source repo at generation time."

**Independent Verification:**

GitHub's `gh attestation` command (and the underlying Sigstore mechanism) generates an OIDC token to sign the attestation. This requires the `id-token: write` permission in the GitHub Actions job. This is documented in GitHub's artifact attestation documentation and confirmed across all Sigstore/SLSA implementations on GitHub: without `id-token: write`, the OIDC endpoint is unavailable and the attestation step fails.

ADR-003 §D4 (L1 Technical Implementation) states: "In CI after a successful push: create an immutable release for the tag and generate a build-provenance attestation binding the skeleton tip SHA to the run/commit/repo." This confirms the attestation step runs in `cowork-skeleton.yml` AFTER the push, meaning the attestation step must be in that workflow.

The attestation binds the SKELETON TIP SHA, which is only known after the force-push completes. Therefore the attestation cannot be pre-computed in `release.yml` (which runs in parallel and has no access to the skeleton tip SHA at the time it runs). The attestation must be created within `cowork-skeleton.yml` — which is forbidden from having `id-token: write` by REQ-020.

ADR-003's pipeline diagram shows the release attestation in `release.yml`, but REQ-042 explicitly requires binding the SKELETON TIP SHA, which only exists post-push in `cowork-skeleton.yml`. No reconciliation of this timing gap is provided.

**Discrepancy:** REQ-042 is unimplementable without `id-token: write` in `cowork-skeleton.yml`. REQ-020 forbids `id-token: write` in `cowork-skeleton.yml`. Satisfying both simultaneously is impossible.

**Recommendation:** Choose one of: (A) Amend REQ-020 to permit `id-token: write` in a dedicated attestation job within `cowork-skeleton.yml`, with a job-level `permissions:` override (narrowed to that job only), and update REQ-020 to say "the push job SHALL declare only `contents: write`"; (B) Create a separate workflow triggered by the `cowork-skeleton.yml` push event that runs after the push, holds `id-token: write`, and creates the attestation — with REQ-042 updated to name this separate workflow; (C) If the attestation uses the SOURCE commit SHA (not the skeleton tip SHA), clarify this in REQ-042 and move the attestation step to `release.yml`. Option A is simplest and preserves the spirit of REQ-020 (least-privilege per job).

---

### CV-002-20260629

**Title:** REQ-035 Event-Driven Monitor Cannot Trigger Cross-Repo in GitHub Actions

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Target** | REQ-035 (event-driven fast path), NFR-006 (event-driven detection leg), requirements Allocation Matrix |
| **Strategy Step** | Step 4: Consistency Check |

**Claim (REQ-035):**
> "Event-driven fast path — on `on: push: branches: [<dedicated-repo-default-branch>]`; retrieve the published SHA from Release notes and assert `git rev-parse HEAD` equals it; mismatch SHALL create a GitHub issue and exit non-zero."

**Claim (Allocation Matrix):**
> "REQ-035 | ... | `on: push: branches: [cowork-skeleton]` event trigger + `on: schedule:` ≤ daily..."

**Independent Verification:**

GitHub Actions workflow triggers are scoped to the repository in which the workflow file resides. A workflow in `geekatron/jerry` (source repo) CANNOT trigger on `on: push: branches: [...]` events in `geekatron/jerry-cowork` (dedicated repo). Cross-repository event triggers are not supported by GitHub Actions for standard GitHub organizations. The only cross-repo trigger mechanism is `repository_dispatch`, which requires a deliberate API call from the push actor — not a passive event listener.

The Allocation Matrix still references `on: push: branches: [cowork-skeleton]` — the Phase-1 in-repo branch name. Under Phase 2, the skeleton is in `geekatron/jerry-cowork`, a separate repository. The event-driven monitor, if placed in the SOURCE repo, cannot receive push events from the DEDICATED repo.

For the event-driven path to work, the monitor workflow would need to reside IN `geekatron/jerry-cowork`. ADR-003 §D2/D4 notes the dedicated repo has "no push-back workflows (read/monitor only)" — implying read-only monitoring workflows are permitted. However, REQ-023 says "the dedicated repo SHALL NOT contain any workflow that pushes to the source repo." If the monitor only creates GitHub issues (in its own repo or via API) and does not push to `geekatron/jerry`, it may be permitted topologically. But REQ-035, REQ-023, and the Allocation Matrix have not been reconciled to reflect this placement.

**Discrepancy:** The event-driven monitor as specified (source-repo workflow triggers on dedicated-repo push events) is architecturally impossible with GitHub Actions. The requirements and allocation matrix were not updated from Phase 1 (in-repo branch) to Phase 2 (cross-repo dedicated-repo) architecture for this leg.

**Recommendation:** Amend REQ-035 and the Allocation Matrix to clarify that the event-driven monitor workflow resides in `geekatron/jerry-cowork` (the dedicated repo), triggered by `on: push` to its default branch. Explicitly confirm this is topologically safe (monitor only creates issues, never pushes to source repo). Update REQ-023 to permit read-only/monitoring workflows in the dedicated repo. If this re-architecture is not acceptable, the event-driven fast path must be removed and REQ-035 must be reduced to the scheduled-only backstop — with the detection SLA increasing from "near-real-time" to ≤ daily.

---

### CV-003-20260629

**Title:** "Direct-Push PREVENTED" Claim Unverified for Org-Owner Bypass Path

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Target** | ADR-003 D2, REQ-040 acceptance criterion, Risk Table (R-007b → GREEN) |
| **Strategy Step** | Step 3: Independent Verification |

**Claim (ADR-003 D2):**
> "This converts the Phase-1 direct-push Critical (old R-007b) from detection to prevention (DR-01: likelihood 3→1, → GREEN). A write collaborator on `geekatron/jerry` has no access to the separate repo; a human cannot push the artifact branch at all."

**Claim (ADR-003 D2, residual modes):**
> "admin-suppression (DR-02 — a repo admin disabling the ruleset) is bounded by using an org-level ruleset repo-admins cannot override"

**Claim (REQ-040 acceptance criterion):**
> "Simulation: attempt a direct push to `geekatron/jerry-cowork` default branch with a non-CI credential; push is rejected. Attempt by a repo admin to override the ruleset: rejected."

**Independent Verification:**

In GitHub's organization model, there are two distinct roles: **repository admins** and **organization owners**. Org-level rulesets can be configured to prevent repo admins from overriding them. However, **organization owners** have administrative control over org-level rulesets themselves — they can modify, disable, or delete org-level rulesets. This is documented in GitHub's ruleset documentation: org owners can manage org-level rulesets directly in org settings; this access is not blocked by the ruleset itself.

An org owner can: (1) modify the org-level ruleset to add themselves as a bypass actor, (2) push directly to the dedicated repo's default branch, (3) remove themselves from bypass actors. The audit log records all ruleset changes, but this constitutes detection (DR-02), not prevention. REQ-040's acceptance criterion tests "repo admin bypass" — not "org owner bypass." These are different roles.

ADR-003's DR-02 mitigation (audit log alert on ruleset change) correctly categorizes this as bounded-detection, not prevention. The disconnect is that D2's primary claim uses the word PREVENTION and rates DR-01 → GREEN, while the org-owner path remains in the DR-02 category with detection mitigations only.

**Discrepancy:** The "direct-push PREVENTED" claim and R-007b → GREEN rating are accurate for repository-collaborator-level principals. They are NOT accurate for org owners, who retain the ability to modify the ruleset itself. REQ-040's acceptance criterion does not test org-owner bypass. The risk table rates R-007b GREEN based on the prevention posture, but this rating applies only to non-admin push paths; the org-owner path remains YELLOW (DR-02) at best.

**Recommendation:** Amend ADR-003 D2 to state "direct-push prevented for all principals except org owners, who retain ruleset modification rights (DR-02 admin-suppression — mitigated by audit alert, admin minimization, and attestation backstop; not technically prevented)." Update R-007b in the risk table to distinguish: direct-push by non-admin collaborators → GREEN (prevented); direct-push via org-owner ruleset suppression → YELLOW (detection-bounded, DR-02). Amend REQ-040's acceptance criterion to add: "Attempt by an org owner to override the ruleset: blocked or detected within the audit-log SLA." This does not require changing the control — only the precision of the claim.

---

### CV-004-20260629

**Title:** "Attestation Resolves SC-04" — No Pre-Install Verification REQ Exists

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Target** | ADR-003 D4, REQ-042, requirements traceability for SC-04 resolution claim |
| **Strategy Step** | Step 3: Independent Verification / Step 4: Consistency Check |

**Claim (ADR-003 D4):**
> "This resolves the Phase-1 5-strategy convergent Critical (SC-04): the old anchor (Release notes) shared `contents: write` with the branch it was supposed to verify... The attestation is CI-only-writable and publicly verifiable — a genuinely independent reference."

**Claim (ADR-003 L0):**
> "Anchor integrity in something CI alone can write. The integrity reference moves from editable Release notes to a GitHub immutable release + build-provenance attestation — a publicly verifiable, CI-only-writable surface."

**Independent Verification:**

REQ-042 mandates CREATING the attestation. It has no counterpart requirement that any party VERIFIES the attestation before installation. The verification path is:

- **REQ-042 AC (b):** "`gh attestation verify <skeleton-tip-sha> --repo geekatron/jerry` exits zero" — this is a TEST step executed during V&V, not an operational pre-install gate.
- **NFR-006 / REQ-035:** Backstop monitor verifies attestation on a ≤ daily scheduled cadence — a post-publish, periodic check.
- **REQ-043:** Org admin registration runbook — no attestation verification step required.
- **CoWork install flow:** When a user's CoWork client installs the plugin (on org registration), there is no attestation verification step. CoWork clones the dedicated repo's default branch; it does not invoke `gh attestation verify`.

The old anchor (Release notes) was "broken" because a writer could tamper with both the artifact AND the reference value using the same credential. The attestation is CI-only-writable, which is a genuine improvement. However, "publicly verifiable" means the attestation CAN be verified by anyone who runs `gh attestation verify` — not that it IS verified before each install. Between a tamper event and the next scheduled backstop monitor run (up to 24 h), a tampered skeleton remains installable by all org users with no warning.

The claim "resolves SC-04" is accurate in the sense that the anchor is now structurally sound (CI-only-writable, non-forgeable). The gap is that "resolution" implies the integrity check is active; it is passive until someone queries the attestation.

**Discrepancy:** No requirement mandates attestation verification in the installation path or prior to serving the skeleton to users. SC-04's resolution is architectural (the anchor is sound) but not operational (no one is required to check the anchor before installation). The ADR should distinguish between "the anchor is trustworthy" and "the anchor is verified." The former is true; the latter has no backing REQ.

**Recommendation:** Add a REQ (or augment REQ-043) requiring: "The periodic registered-source verification (REQ-043 quarterly audit) SHALL include running `gh attestation verify` against the live dedicated-repo default-branch tip SHA and confirming it matches the expected attestation." This closes the operational gap. Optionally, document in the org-registration runbook that the attestation is the authoritative integrity check, so administrators know to verify it during audits and incident response. Do not claim SC-04 is "resolved" without at least one required operational verification step.

---

### CV-005-20260629

**Title:** ADR-001 Body Prose Says `tests/` "Retained Today"; Phase 2 Amendment Strips It

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Target** | ADR-001 §Canonical Plugin-Retention Surface (body, line ~108) |
| **Strategy Step** | Step 4: Consistency Check |

**Claim (ADR-001 body, §Canonical Plugin-Retention Surface):**
> "By contrast `docs/`, `runbooks/`, `overrides/`, `scripts/`, `tests/` are not load-bearing for plugin function and MAY be stripped later if the file-count margin tightens (R-002) — but are retained today (1,744 ≪ 5,000)."

**Independent Verification:**

ADR-001 amendment header (lines 3–5): "extends the strip set to include `tests/`." ADR-003 pipeline L1: `git rm -r projects/ tests/`. REQ-002: "The skeleton generation script SHALL strip the `projects/` directory AND the `tests/` directory entirely." REQ-005 explicitly flags this: "Note for ps-architect (ADR-001 inconsistency): ADR-001's body... says `tests/` is 'retained today (1,744 ≪ 5,000)' but the ADR-001 amendment header (2026-06-28) and ADR-003 both strip `tests/'."

The IMPLEMENTATION intent is correct everywhere (strip `tests/`). REQ-002 and REQ-005 acceptance criteria correctly require `git ls-files tests/` to return empty. REQ-005 already flags this inconsistency and defers correction to ps-architect.

**Discrepancy:** The ADR-001 body was not updated when the Phase 2 amendment was applied. The body prose contradicts both the amendment header and every downstream artifact. This is a known inconsistency already documented in REQ-005, but it remains unfixed in ADR-001.

**Recommendation:** Update ADR-001 §Canonical Plugin-Retention Surface body to strike "but are retained today (1,744 ≪ 5,000)" and replace with "Phase 2 amendment: `tests/` is stripped per the 2026-06-28 amendment header; remaining entries (`docs/`, `runbooks/`, `overrides/`, `scripts/`) are retained pending future margin decisions (R-002)." This is a prose correction only; no implementation change is needed.

---

## Claim Inventory

| CL-ID | Claim | Source | Type | Disposition |
|-------|-------|--------|------|-------------|
| CL-001 | D2 traces to REQ-040 with verifiable AC (repo-admin bypass test) | ADR-003 §Requirement Deltas; REQ-040 | Traceability | VERIFIED |
| CL-002 | D3 traces to REQ-041 with verifiable AC (credential type inspection) | ADR-003 §Requirement Deltas; REQ-041 | Traceability | VERIFIED |
| CL-003 | D4 traces to REQ-042 (create attestation) and REQ-035 (secondary SHA) | ADR-003 §Requirement Deltas; REQ-042; REQ-035 | Traceability | VERIFIED (creation trace); FINDING CV-004 (verification gap) |
| CL-004 | D5 traces to REQ-038 (provenance assertion) + REQ-039 (tag protection), both with verifiable ACs | ADR-003 §Requirement Deltas; REQ-038; REQ-039 | Traceability | VERIFIED |
| CL-005 | D6 traces to REQ-017, REQ-019, REQ-022, REQ-036, all with verifiable ACs | ADR-003 §Requirement Deltas; REQ-017/019/022/036 | Traceability | VERIFIED |
| CL-006 | REQ-020 forbids `id-token: write` in `cowork-skeleton.yml` | REQ-020 | Behavioral | VERIFIED (requirement text confirmed) |
| CL-007 | REQ-042 requires Sigstore attestation binding skeleton tip SHA | REQ-042 | Behavioral | VERIFIED (requirement text confirmed) |
| CL-008 | Sigstore `gh attestation` requires `id-token: write` | GitHub Actions documentation | Behavioral | MATERIAL DISCREPANCY → CV-001 |
| CL-009 | REQ-035 event-driven fast path: `on: push: branches: [<dedicated-repo-default-branch>]` in source repo | REQ-035; Allocation Matrix | Behavioral | MATERIAL DISCREPANCY → CV-002 |
| CL-010 | GitHub Actions workflows cannot trigger on push events in a different repository | GitHub Actions documentation | Behavioral | VERIFIED (confirms CV-002 discrepancy) |
| CL-011 | "Direct-push PREVENTED for ALL humans" — R-007b → GREEN | ADR-003 D2; Risk Table | Security claim | MATERIAL DISCREPANCY → CV-003 |
| CL-012 | REQ-040 AC tests repo-admin bypass | REQ-040 AC text | Behavioral claim | VERIFIED (AC text confirmed; org-owner not tested → CV-003) |
| CL-013 | "Attestation is publicly verifiable" / "resolves SC-04" | ADR-003 D4 | Security claim | MINOR DISCREPANCY → CV-004 |
| CL-014 | No REQ mandates attestation verification before installation | REQ-042; REQ-043; NFR-006; CoWork install flow | Absence claim | VERIFIED (no such REQ found) → CV-004 |
| CL-015 | ADR-001 body: `tests/` "retained today (1,744 ≪ 5,000)" | ADR-001 §Canonical Plugin-Retention Surface body | Internal consistency | MATERIAL DISCREPANCY → CV-005 (already flagged by REQ-005) |
| CL-016 | GitHub App installation token is short-lived (~1h) | ADR-003 D3; REQ-041 | Behavioral | VERIFIED (consistent with GitHub App token documentation) |

---

## Traceability Check: D1–D6 to REQ

| Decision | REQ(s) | Verifiable AC? | Status |
|----------|--------|----------------|--------|
| D1: Dedicated repo as distribution target | REQ-002, REQ-012, REQ-040, REQ-043 (implied throughout) | No standalone REQ; embedded in others | ACCEPTABLE (ADR governs; REQs reference) |
| D2: Dedicated-repo protection (prevention) | REQ-040 | Yes — but org-owner bypass not tested | PARTIAL — see CV-003 |
| D3: Cross-repo push credential | REQ-041 | Yes | VERIFIED |
| D4: Integrity anchor — attestation | REQ-042 (creation), REQ-035 (backstop), REQ-044 (meta-monitor) | Creation: Yes; verification before install: No REQ | PARTIAL — see CV-004; see CV-001 for `id-token` blocker; see CV-002 for event-driven leg |
| D5: Residual provenance — tag-on-main + tag protection | REQ-038, REQ-039 | Yes (both ACs verifiable) | VERIFIED |
| D6: CI runner hardening | REQ-017, REQ-019, REQ-022, REQ-036 | Yes (all ACs verifiable) | VERIFIED |

---

## Scoring Impact

| S-014 Dimension | Weight | Impact | Finding(s) | Rationale |
|-----------------|--------|--------|------------|-----------|
| Completeness | 0.20 | Negative | CV-002, CV-004 | REQ-035 event-driven path is unspecified for cross-repo; pre-install attestation verification has no REQ |
| Internal Consistency | 0.20 | Negative | CV-001, CV-002, CV-005 | REQ-020 vs REQ-042 mutual exclusion; event-driven trigger impossible; ADR-001 body vs amendment |
| Methodological Rigor | 0.20 | Neutral | CV-003 | The control itself (org-level ruleset) is sound; the overstatement is in claim precision, not method |
| Evidence Quality | 0.15 | Negative | CV-003 | "Direct-push PREVENTED" claim insufficiently qualified for org-owner path; risk rating overstated |
| Actionability | 0.15 | Negative | CV-001 | REQ-042 is unimplementable as-written — blocks Phase 5 implementation |
| Traceability | 0.10 | Negative | CV-004 | D4's SC-04 resolution claim has no corresponding REQ requiring operational verification |

---

## Execution Statistics

- **Protocol Steps Completed:** 5 of 5
- **Total Claims Extracted:** 16
- **Verified:** 9
- **Minor Discrepancy:** 1 (CV-005)
- **Material Discrepancy:** 5 (CV-001 through CV-004, CL-011 sub-finding)
- **Unverifiable:** 0
- **Total Findings:** 5
  - Critical: 2 (CV-001, CV-002)
  - Major: 2 (CV-003, CV-004)
  - Minor: 1 (CV-005)
- **Verification Rate:** 9/16 = 56% (below 80% target; driven by the cross-repo architectural gap and the `id-token` contradiction)
- **Overall Assessment:** REVISE — Two Critical findings must be resolved before Phase 5.

---

*Generated by:* jerry:adv-executor (blind independent reviewer — Group D Verify)
*Strategy:* S-011 Chain-of-Verification (template: `.context/templates/adversarial/s-011-cove.md`)
*Blindness constraint honored:* No files under `adversary/` read during this execution.
*Self-review (H-15):* Applied — all findings carry specific evidence; severity classifications justified; no finding omitted or minimized (P-022).
