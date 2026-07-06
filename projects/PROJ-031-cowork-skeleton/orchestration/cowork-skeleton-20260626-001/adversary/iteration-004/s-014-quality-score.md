# Quality Score Report: PROJ-031 CoWork Skeleton — Phase-2 Consolidated Design

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Composite score, verdict, top action |
| [Scoring Context](#scoring-context) | Deliverables, criticality, strategy |
| [Score Summary](#score-summary) | Weighted composite vs gates |
| [Dimension Scores](#dimension-scores) | Six-dimension table with evidence |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Evidence, gaps, and improvement path per dimension |
| [Remediation — (A) MUST-FIX-NOW](#remediation-a-must-fix-now-contradictions) | Blocking consistency/contradiction fixes |
| [Remediation — (B) ADD Operational Hardening](#remediation-b-add-operational-hardening-requirements) | Missing security-critical requirements |
| [Remediation — (C) Phase-3+ Implementation Concerns](#remediation-c-phase-3-implementation-concerns) | Noted for future cycles; not required now |
| [Projected Post-Fix Score](#projected-post-fix-score) | Score estimate after (A)+(B) |
| [Leniency Bias Check](#leniency-bias-check) | H-15 self-review with anti-leniency statement |

---

## L0 Executive Summary

**Score:** 0.74/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.62)

**One-line assessment:** The Phase-2 dedicated-repo architecture is structurally sound with zero substantive architectural flaws found by Steelman and Inversion, but seven confirmed internal contradictions (including one Phase-blocking mutual exclusion: REQ-020 vs REQ-042) and seven missing operational-hardening requirements hold the composite to 0.74 — below both the 0.92 gate and the 0.95 C4 target; all (A) contradictions and (B) additions must be resolved before Phase-5 can proceed.

---

## Scoring Context

- **Deliverables scored:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md`
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-003-credential-protection-supply-chain.md`
  - `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md`
  - ADR-002 is superseded — excluded from scoring.
- **Deliverable Type:** ADR + Requirements (Architecture Decision Records and Engineering Requirements)
- **Criticality Level:** C4 (irreversible architecture/security/public; AE-002, AE-003, AE-005)
- **Quality Target:** >= 0.95 (project REQ-031); Gate: >= 0.92 (H-13)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Strategy Findings Incorporated:** Yes — all 8 iteration-004 findings (s-001 Red Team, s-002 Devil's Advocate, s-003 Steelman, s-004 Pre-Mortem, s-007 Constitutional AI, s-011 Chain-of-Verification, s-012 FMEA, s-013 Inversion)
- **Prior Score:** 0.824 (Phase-1; different design — NOT comparable; Phase-2 is a substantially hardened dedicated-repo model)
- **Iteration:** iteration-004 (post Phase-2 RE-ADVERSARY gate)
- **Scored:** 2026-06-29T00:00:00Z
- **Scored by:** jerry:adv-scorer (blind; P-003 compliant; P-020 — deliverables not modified)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.74 |
| **Threshold (H-13)** | 0.92 |
| **C4 Project Target (REQ-031)** | 0.95 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes (8 strategies, iteration-004) |
| **Prior Score** | 0.824 (Phase-1; different design — incomparable) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.73 | 0.146 | All 5 workstreams covered and REQ-038-044 added; 7 operational-hardening gaps missing (attestation verify mandate, repo-metadata monitor, key rotation cadence, gen-workflow liveness, file-count early-warning, REQ-035a architecturally impossible, no GH Actions Environment REQ) |
| Internal Consistency | 0.20 | 0.62 | 0.124 | 7 confirmed contradictions: REQ-020 vs REQ-042 (Phase-blocking), ADR-001 body vs amendment (unresolved in SSOT), ADR-003 L0 vs D2 body, NFR-006 self-contradiction, ADR-003 attestation workflow placement ambiguity, Requirements Quality Checklist self-assessment incorrect, file-count discrepancy |
| Methodological Rigor | 0.20 | 0.80 | 0.160 | STRIDE applied, Nygard ADR format, formal risk register, five-path integrity architecture, SLSA trajectory; gaps: REQ-035a cross-repo constraint not validated before writing, REQ-020/REQ-042 conflict not caught during Phase-2 extension, trusted-maintainer path absent from threat model |
| Evidence Quality | 0.15 | 0.77 | 0.1155 | Most claims well-evidenced and honestly qualified (S-010 epistemic note); gaps: ADR-003 L0 "prevented outright" unsupported for org-owner path, two-admin approval has no GitHub platform evidence, "resolves SC-04" conflates architectural anchor with operational verification |
| Actionability | 0.15 | 0.74 | 0.111 | Most ADR decisions have clear Phase allocation and acceptance criteria; gaps: REQ-042 unimplementable (REQ-020/REQ-042 conflict), REQ-035a unimplementable (cross-repo trigger impossible), key rotation cadence absent, "designated maintainers" undefined, NFR-006 `gh attestation verify` command not specified |
| Traceability | 0.10 | 0.85 | 0.085 | STK→REQ→ADR Decision→Component chain solid; Allocation Matrix complete; STRIDE IDs consistently cited; gaps: SC-04 "resolved" has no REQ tracing to operational verification; auto-revert deferred item remains open |
| **TOTAL** | **1.00** | | **0.74** | |

**Composite verification:** 0.146 + 0.124 + 0.160 + 0.1155 + 0.111 + 0.085 = 0.7415 → **0.74**

---

## Detailed Dimension Analysis

### Completeness (0.73/1.00)

**Evidence for score:**

The Phase-2 deliverables meaningfully extend Phase-1 completeness. WS-1 through WS-5 are all addressed. ADR-003 adds six formal decisions (D1-D6) with rationale, alternatives, and implementation specifications. REQ-038 through REQ-044 mirror each ADR-003 decision into verifiable requirements with ADIT methods and acceptance criteria. All ADR-002 compensating controls (CC-1 through CC-8) are carried through. WS-4 documentation requirements (Diataxis quad coverage, uv prerequisite, H-04 first-run experience) are comprehensive. WS-5 quality requirements (C4 tournament, S-014 >= 0.95, H-14 minimum 3 iterations, user approval gates) are clearly stated. NFR-001 through NFR-006 cover determinism, idempotency, freshness, least-privilege, recoverability, and monitoring.

**Gaps:**

1. **No REQ mandates `gh attestation verify` in the backstop monitor** — REQ-042 requires creating the attestation; nothing requires the monitoring workflow to invoke `gh attestation verify`. The "anchor is sound" (architectural resolution) is not backed by "anchor is verified" (operational resolution). (FM-006-it004, CV-004, IN-003-it4, DA-002)

2. **No REQ for dedicated-repo metadata drift monitoring** — ADR-003 D2 mentions "monitor on default-branch name and repo visibility" in prose, but no SHALL requirement mandates verifying repo visibility, default-branch name, or repo existence. A visibility → private or repo rename silently breaks all org user installations. (PM-002, RT-006, IN-004-it4)

3. **App private key rotation cadence absent** — c-208 says "a rotation policy" but no REQ specifies maximum rotation interval or trigger conditions. "Rotation policy" is aspirational without a defined schedule. (PM-001, IN-005-it4)

4. **Generation workflow liveness unmonitored** — REQ-044 monitors the backstop monitor liveness (25h window). No REQ monitors whether the generation workflow itself executed successfully for the latest v* tag. A silent generation failure leaves the skeleton stale up to 7 days. (PM-006, FM-008-it004)

5. **File-count early-warning absent** — REQ-034d has two-tier monitoring for size-pack (150 MB non-blocking early warning, 250 MB hard-fail). No equivalent two-tier exists for file count (only 5,000 hard-fail; no early warning at e.g., 3,500 files). (PM-007, FM-009-it004)

6. **REQ-035a event-driven monitor architecturally impossible in source repo** — `on: push: branches: [<dedicated-repo-default-branch>]` in a source-repo workflow cannot trigger on events in a different repository. The requirement as written is unimplementable. (CV-002, FM-002-it004, IN-002-it4)

7. **No GitHub Actions Environment REQ** — No requirement mandates an environment-gated, branch-restricted protection for the App private key or deploy key credential access, leaving `workflow_dispatch` as an exfiltration vector for any write-level collaborator. Proposed REQ-045 is absent. (RT-001, PM-001, FM-003-it004)

**Improvement path:**

Implement (A-2) to redesign REQ-035a with an architecturally viable topology. Implement (B-1) through (B-8) to add the seven operational-hardening requirements above. After these changes, Completeness reaches approximately 0.90.

---

### Internal Consistency (0.62/1.00)

**Evidence for score:**

The overall architectural narrative is coherent: ADR-003 D1-D6 decisions map cleanly to REQ-038-044, the STRIDE threat IDs are cited consistently, and the Phase-2 deferred items are explicitly resolved or forward-referenced. Steelman (S-003) and Inversion (S-013) independently found ZERO substantive architectural flaws — the design is structurally consistent.

However, seven confirmed contradictions are present:

1. **REQ-020 vs REQ-042 — Phase-blocking mutual exclusion** (5/8 strategies independently identified): REQ-020 declares `contents: write` as the "sole permission entry" and explicitly prohibits `id-token: write`. REQ-042 mandates Sigstore-backed build-provenance attestation (`gh attestation attest`/`actions/attest-build-provenance`), which GitHub requires `id-token: write` to execute. Both are SHALL requirements in the same document targeting the same workflow. Implementation of REQ-042 without violating REQ-020 is impossible in a single-job workflow. The Requirements Quality Checklist in the same document claims "Consistent: No conflicting requirements" — this self-assessment is factually incorrect. (CC-001-I004, CV-001, FM-001-it004, RT-002, IN-001-it4)

2. **ADR-001 body §Canonical Plugin-Retention Surface vs Phase-2 amendment header** (6/8 strategies flagged): Body says `tests/` "not load-bearing... but are retained today (1,744 ≪ 5,000)." Amendment header (2026-06-28) says "extends the strip set to include `tests/`." ADR-003 and REQ-002 confirm the strip. REQ-005 flags this inconsistency and defers to ps-architect — but the SSOT body section remains incorrect at C4 criticality. (CC-003-I004, CV-005, DA-006, SM-008, FM-007-it004, IN-007-it4)

3. **ADR-003 L0 "no human can push" vs D2 body DR-02 HIGH residual**: L0 and Consequences §Positive #1 use "no human can push" and "outright." D2 body explicitly retains DR-02 (admin-suppression) as HIGH impact and bounded by detection-only controls. Org-owners can modify org-level rulesets; the guarantee applies to principals below org-owner level, not universally. (DA-001, CC-002-I004, CV-003, FM-004-it004)

4. **NFR-006 self-contradiction within same sentence**: "retrieve the expected deterministic tip SHA from the GitHub Release notes... re-point anchor from editable Release-notes text to the immutable attestation (REQ-042) as the primary integrity reference." These are directly contradictory instructions about the verification mechanism within one requirement. (IN-003-it4, FM-006-it004, CV-004)

5. **ADR-003 pipeline diagram attestation workflow vs L1 text**: The Context pipeline diagram shows "release.yml → GitHub immutable Release + build-provenance attestation." ADR-003 L1 text says "In CI after a successful push: create an immutable release and generate a build-provenance attestation binding the skeleton tip SHA to the run/commit/repo" — placing the attestation in `cowork-skeleton.yml`. REQ-042's Allocation Matrix confirms `cowork-skeleton.yml` (attestation step). The diagram contradicts the L1 text and allocation. (CC-001-I004, CV-001)

6. **Requirements Quality Checklist "No conflicting requirements"** — directly contradicted by finding #1 above. A C4 document claiming internal consistency that it does not have is a material accuracy issue (P-001).

7. **ADR-003 pipeline diagram file count ~1,749 vs requirements L0 ~1,417**: ADR-003 Context diagram shows "skeleton ~1,749 files" (the pre-Phase-2 figure with projects/ only stripped). Requirements L0 states "approximately 1,417" after tests/ additionally stripped. (CC-004-I004, DA-006)

**Improvement path:**

Implement (A-1) to resolve REQ-020/REQ-042. Implement (A-2) to redesign REQ-035a. Implement (A-3) to reframe ADR-003 L0. Implement (A-4) to rewrite NFR-006 tamper-detection mechanism. Implement (A-5) to correct ADR-001 body. Implement (A-6) to correct ADR-003 file count. After these six targeted fixes, Internal Consistency reaches approximately 0.90.

---

### Methodological Rigor (0.80/1.00)

**Evidence for score:**

The Phase-2 methodology is genuinely rigorous in its foundational aspects:
- STRIDE threat modeling applied with formal threat IDs (SC-02, DR-01, DR-02, OR-01, CI-01, etc.)
- Nygard ADR format followed for both ADR-001 and ADR-003 with formal Alternatives, Consequences, and Risk Table sections
- Defense-in-depth architecture: three independent integrity paths (prevention via D2, attestation via D4, monitoring via NFR-006)
- CR-02 topological loop-safety analysis formally validates that the dedicated-repo cannot retrigger the source-repo
- SLSA Level 3 trajectory articulated with specific controls mapping (D2 → branch protection, D4 → build-provenance, D5 → tag provenance)
- ADIT verification methods assigned to every requirement
- P-042 5×5 numeric risk scoring applied consistently
- Phase-2 deferred items explicitly resolved with documented rationale
- S-010 epistemic qualification: "attestation mechanics validated against current GitHub vendor documentation, not yet exercised on geekatron/jerry-cowork" — appropriate confidence calibration

Both S-003 Steelman and S-013 Inversion found ZERO substantive architectural flaws, confirming the core methodology is sound.

**Gaps:**

1. **Platform constraint not validated before writing REQ-035a** — The event-driven monitor requirement was written specifying `on: push: branches: [<dedicated-repo-default-branch>]` in the source repo without verifying that GitHub Actions supports cross-repository event subscriptions. It does not. Sound methodology requires platform feasibility validation before writing SHALL requirements. (CV-002, FM-002-it004, IN-002-it4)

2. **Phase-2 requirements extension without cross-REQ conflict check** — REQ-042 (Sigstore attestation, added in Phase-2) conflicts with REQ-020 (Phase-1 permission constraint, not reviewed during extension). A rigorous Phase-2 requirements update methodology would have included a conflict scan against all existing REQs. (all strategies identifying REQ-020/REQ-042)

3. **Trusted-maintainer attack path absent from threat model** — A principal with `main` write access and `v*` tag creation rights can push a malicious commit to `main`, then push a `v*` tag pointing to it. The D5 provenance assertion (`git merge-base --is-ancestor`) PASSES because the tag IS an ancestor of main. This threat path is not documented in the STRIDE threat model. (DA-005)

**Improvement path:**

A-2 redesigning REQ-035a addresses gap #1. A-1 resolving the requirements conflict addresses gap #2. The trusted-maintainer gap would require an explicit threat model entry and a corresponding control (requiring peer review on all main-branch commits from principals with tag-create rights). This is a (C) item.

---

### Evidence Quality (0.77/1.00)

**Evidence for score:**

Most claims are well-evidenced and honestly qualified:
- ADR-003 S-010 Self-Refine Note explicitly discloses: "attestation mechanics validated against current GitHub vendor documentation, not yet exercised on geekatron/jerry-cowork" — appropriate epistemic qualification (P-011 COMPLIANT per S-007 assessment)
- GitHub App token TTL (~1h), Sigstore OIDC mechanics, and phase-1 empirical observations (R-001, current ruleset scope) are all properly referenced
- STRIDE threat IDs provide explicit traceability to the threat model
- Phase-2 deferred item resolutions are explicitly documented with rationale ("RESOLVED → REQ-038", "PARTIALLY DEFERRED (STILL OPEN)")
- P-004 (Explicit Provenance) confirmed COMPLIANT by S-007 constitutional review

**Gaps:**

1. **ADR-003 L0 "prevented outright" unsupported for org-owner path** — The claim that direct-push is "PREVENTED, not merely detected" is accurate for repository-collaborator-class principals. GitHub org-owners can modify or delete org-level rulesets and therefore retain the ability to push directly. "Prevented outright" or "no human can push" is not supported by GitHub platform documentation for org-owner-class actors. This is a P-022 (No Deception) calibration gap. (DA-001, CC-002-I004, CV-003, FM-004-it004)

2. **REQ-043 two-admin approval without platform enforcement evidence** — "A minimum of two admin approvals SHALL be required for any registered-source change" is stated as a SHALL requirement, but no evidence is cited that GitHub's CoWork marketplace org registration settings natively support a two-approver enforcement mechanism. The control as written may be policy-only with no technical enforcement. (DA-004, FM-005-it004)

3. **"Resolves SC-04" conflates architectural vs operational resolution** — ADR-003 D4 correctly establishes an architecturally sound integrity anchor (CI-only-writable, Sigstore-backed). But "resolves SC-04" implies the anchor is verified. No REQ mandates that any party verifies the attestation before harm occurs. The attestation exists as a forensic artifact until someone explicitly queries it. The claim that SC-04 is resolved is architecturally true but operationally incomplete. (CV-004, FM-006-it004, IN-003-it4, DA-002)

**Improvement path:**

A-3 reframes the L0 overclaim with appropriate confidence calibration. B-2 adds a mandatory `gh attestation verify` REQ to bridge the architectural-vs-operational resolution gap. B-3/B-4 add technical enforcement evidence for org-registration monitoring.

---

### Actionability (0.74/1.00)

**Evidence for score:**

The deliverables are highly actionable in their core design specifications:
- ADR-003 D1-D6 each include L1 Technical Implementation sections with concrete pipeline steps
- REQ-038-044 all have ADIT verification methods, explicit acceptance criteria, and Phase allocation
- The cowork-skeleton.yml pseudocode in ADR-001 and the faithful-derivative gate code in ADR-003 are implementable
- REQ-034/REQ-034d specify precise numerical thresholds (5,000 files, 250 MB hard-fail, 150 MB early warning, 40s clone time)
- NFR-006 specifies two independent monitoring legs with explicit cadences (weekly, daily)

**Gaps (Phase-blocking):**

1. **REQ-042 unimplementable as written** — REQ-042 mandates Sigstore attestation in `cowork-skeleton.yml`; REQ-020 forbids the permission required to execute it. A developer implementing Phase 6 cannot satisfy both requirements simultaneously. (RT-002, CC-001-I004, CV-001, FM-001-it004, IN-001-it4)

2. **REQ-035a event-driven trigger unimplementable** — The `on: push: branches: [<dedicated-repo-default-branch>]` trigger specified for the source-repo monitoring workflow cannot fire on events in a different repository. An implementer following this requirement cannot make the event-driven leg work. (CV-002, FM-002-it004, IN-002-it4)

**Gaps (underspecified):**

3. **App private key rotation cadence absent** — "rotation policy" (c-208) provides no implementable schedule. A developer maintaining the credential cannot determine compliance without a defined interval. (PM-001, IN-005-it4)

4. **"Designated maintainers" undefined** — REQ-039 restricts `v*` tag creation to "designated maintainers" without defining who qualifies, how they are added/removed, or the maximum count. Implementers cannot configure the tag-protection ruleset bypass list correctly. (IN-006-it4)

5. **NFR-006 tamper-detection command not specified** — NFR-006's tamper-detection leg says "re-point anchor to the immutable attestation" but does not specify the actual `gh attestation verify` command. An implementer following this requirement literally could implement the Release-notes SHA comparison (Phase-1 collapsed anchor) and satisfy all acceptance criteria. (IN-003-it4, FM-006-it004)

**Improvement path:**

A-1 resolves the two Phase-blocking actionability gaps. A-4 specifies the `gh attestation verify` command in NFR-006. B-5 adds the rotation cadence REQ. A-2 specifies an implementable monitor topology for REQ-035a. Defining "designated maintainers" in REQ-039 (scope, maximum count, governance) closes gap #4.

---

### Traceability (0.85/1.00)

**Evidence for score:**

Traceability is the strongest dimension:
- Full STK-xxx → REQ-xxx → ADR Decision → Component allocation chain present
- Traceability Summary at requirements end covers STK-001 through STK-006 with complete REQ trees
- Allocation Matrix maps all requirements to implementing component, interface, and Phase
- STRIDE threat IDs consistently cited in requirements rationale and ADR Consequences
- P-004 (Explicit Provenance) confirmed COMPLIANT by S-007 constitutional review
- Phase-2 deferred items forward-referenced (not orphaned) with resolution notes
- REQ-005 explicitly traces the ADR-001 body inconsistency for ps-architect

**Gaps:**

1. **SC-04 "resolved" lacks operational verification trace** — ADR-003 D4 claims SC-04 is resolved by the attestation anchor. The trace from "attestation exists" to "integrity is operationally verified" has no backing REQ. The resolution is architectural; no REQ traces to "someone verifies the attestation before harm occurs." (CV-004, IN-003-it4)

2. **Auto-revert recovery path remains open** — Phase-2 deferred item for auto-revert is marked "PARTIALLY DEFERRED (STILL OPEN)." The traceability from R-007b recovery to a concrete recovery mechanism is incomplete.

3. **Duplicate Allocation Matrix entries** — REQ-034d and REQ-035 each appear twice in the Allocation Matrix, indicating the Phase-2 document editing introduced duplicate rows. Minor but indicates incomplete consistency checking.

**Improvement path:**

B-2 (mandating `gh attestation verify` in the monitor) closes the SC-04 operational verification trace. The auto-revert item is a Phase-3+ concern. Duplicate rows should be cleaned as part of (A) document cleanup.

---

## Remediation — (A) MUST-FIX-NOW Contradictions

These fix internal consistency and actionability blockers. All are prerequisite to Phase-5/Phase-6 implementation.

| Priority | ID | Merged Finding IDs | Severity | Owner | Concrete Fix |
|----------|----|--------------------|----------|-------|--------------|
| A-1 | REQ-020 vs REQ-042 `id-token: write` | CC-001-I004, CV-001-20260629, FM-001-it004, RT-002, IN-001-it4 | Critical (Phase-blocking) | nse-requirements | Amend REQ-020 text: replace "The `permissions:` block in `cowork-skeleton.yml` SHALL declare `contents: write` as the **sole** permission entry" with "The push job `permissions:` block SHALL declare `contents: write` as the sole entry; a dedicated attestation job within the same workflow MAY additionally declare `id-token: write` and `attestations: write` using per-job `permissions:` isolation, tracing to REQ-042." Remove `id-token: write` from the forbidden-permissions list. Correct Requirements Quality Checklist item to: "Consistent: One resolved conflict identified and corrected (REQ-020/REQ-042; see amendment)." |
| A-2 | REQ-035a cross-repo event-driven monitor architecturally impossible | CV-002-20260629, FM-002-it004, IN-002-it4 | Critical (Phase-blocking) | nse-requirements + ps-architect | Two options: (Option A, preferred) Add ADR-003 Decision D7: "The event-driven integrity monitor workflow resides in `geekatron/jerry-cowork` as a read-only workflow; it subscribes to `on: push` events on its own default branch and SHALL NOT declare `contents: write` on the source repo." Update REQ-035(a) to: "Event-driven fast path: a read-only monitoring workflow in `geekatron/jerry-cowork` triggers on `on: push: branches: [skeleton]`, invokes `gh attestation verify`, and creates a GitHub issue on mismatch." Update REQ-023 to explicitly permit read-only monitoring workflows in the dedicated repo. (Option B) Retire the event-driven leg; replace with ≤6-hourly scheduled poll and update detection SLA accordingly. |
| A-3 | ADR-003 L0 "resolved outright / no human can push" overclaim | DA-001, CC-002-I004, CV-003-20260629, FM-004-it004 | Major (P-022 calibration) | ps-architect | In ADR-003 L0 item 1: Replace "resolved the Phase-1 'unprotected branch' Critical outright" with "reduces the Phase-1 'unprotected branch' Critical to a bounded residual (DR-02: LOW probability, HIGH impact), with prevention as the primary posture." In ADR-003 Consequences §Positive #1: Replace "no human can push the artifact branch" with "no human below org-owner level can push the artifact branch without explicitly disabling the org-level ruleset — an auditable, admin-minimized action (DR-02)." Add to D2 body: "Org-owners (a role above repo admins in GitHub's permission hierarchy) retain the ability to modify org-level rulesets; org-owner count minimization and 2FA/SSO are required compensating controls." |
| A-4 | NFR-006 self-contradiction: Release-notes SHA vs attestation | IN-003-it4, FM-006-it004, CV-004-20260629 | Major (verification mechanism) | nse-requirements | Rewrite NFR-006 tamper-detection check: Remove "retrieve the expected deterministic tip SHA from the GitHub Release notes for the latest v* tag (per REQ-035)." Replace with: "invoke `gh attestation verify <live-tip-sha> --repo geekatron/jerry` as the primary verification step; a non-zero exit or absent attestation SHALL constitute a tamper-detection trigger." Update REQ-035 AC(b) to: "the event-driven monitor fires, invokes `gh attestation verify <tip-sha> --repo geekatron/jerry`, confirms non-zero exit on a directly-pushed (tampered) tree, creates a GitHub issue, and exits non-zero." Add to ADR-003 D4 L2: "Note: end-user install-time attestation verification is not feasible via CoWork's plugin mechanism; the backstop monitor is the sole automated verification path." |
| A-5 | ADR-001 body `tests/` "retained today (1,744)" vs Phase-2 amendment | CC-003-I004, CV-005-20260629, DA-006, SM-008, FM-007-it004, IN-007-it4 | Major (SSOT accuracy) | ps-architect | In ADR-001 §Canonical Plugin-Retention Surface body, replace "but are retained today (1,744 ≪ 5,000)" with "Phase-2 amendment (2026-06-28): `tests/` is stripped as of this amendment per ADR-003 D1 pipeline specification; remaining directories (`docs/`, `runbooks/`, `overrides/`, `scripts/`) are retained today (~1,417 ≪ 5,000)." Remove REQ-005 deferral note "Do NOT edit ADR-001; flagging for ps-architect" once the body is corrected. |
| A-6 | ADR-003 pipeline diagram file count ~1,749 vs requirements ~1,417 | CC-004-I004 | Minor (accuracy) | ps-architect | In ADR-003 §Context pipeline diagram, update "DEDICATED geekatron/jerry-cowork ... ~1,749 files" to "~1,417 files" (or empirically measured post-strip value once R-001 is completed). |

---

## Remediation — (B) ADD Operational Hardening Requirements

These add missing SHALL requirements. All should be added before Phase-5 or Phase-6 as indicated.

| Priority | ID | Merged Finding IDs | Severity | Owner | Before Phase | Concrete Fix |
|----------|----|--------------------|----------|-------|-------------|--------------|
| B-1 | GitHub Actions Environment for workflow_dispatch key protection (REQ-045) | RT-001, PM-001, FM-003-it004 | High | nse-requirements | Phase-5 | Add REQ-045: "The App private key and deploy key SHALL be stored as environment-level secrets in a GitHub Actions Environment named `skeleton-push`. The `skeleton-push` environment SHALL declare `deployment_branch_policy` restricting activation to protected branches (`main`) and protected tags (`v*`). Any `workflow_dispatch` run SHALL require the `skeleton-push` environment to be activated before the credential mint step executes. Non-protected-branch `workflow_dispatch` invocations SHALL be rejected before accessing any credential." AC: A `workflow_dispatch` triggered from a feature branch cannot access the App private key secret; a `workflow_dispatch` from main proceeds normally after environment activation. |
| B-2 | Mandate `gh attestation verify` in backstop monitor | FM-006-it004, CV-004-20260629, IN-003-it4, DA-002 | High | nse-requirements | Phase-6 | Add to NFR-006 AC: "Tamper-detection check SHALL invoke `gh attestation verify <live-tip-sha> --repo geekatron/jerry` as the primary integrity verification; a non-zero exit, absent attestation, or attestation mismatch SHALL trigger a GitHub issue and job failure." Note: Partially overlaps with A-4 (which fixes NFR-006 text); B-2 specifically adds the mandate to the monitoring workflow's acceptance criteria. |
| B-3 | Monitor dedicated-repo metadata drift | PM-002, RT-006, IN-004-it4, FM-005-it004 | High | nse-requirements | Phase-6 | Add to REQ-040 or as REQ-045b: "A scheduled monitor SHALL verify at ≤ weekly cadence: (a) `geekatron/jerry-cowork` is publicly accessible via GitHub API (`gh api repos/geekatron/jerry-cowork` returns 200 with `private: false`); (b) the default branch name matches the configured value; (c) the repo exists and is accessible; (d) the org-level ruleset targeting the dedicated repo default branch remains active. A mismatch on any check SHALL open a GitHub issue." AC: Simulate repo renamed; confirm monitor opens issue within one scheduled cycle. |
| B-4 | Automated org-registration source monitoring | PM-004, FM-005-it004 | High | nse-requirements | Phase-6 | Add to REQ-043: "An automated daily or weekly monitor SHALL query the org CoWork registration source and verify it matches the canonical value (`geekatron/jerry-cowork`); any mismatch SHALL trigger a GitHub issue alert within 24 hours. The quarterly audit cadence SHALL be reduced to monthly minimum. An org audit-log webhook alert SHALL be configured for any marketplace settings change event." AC: Simulate registration repointed to a different repo; confirm automated monitor alerts within 24h. |
| B-5 | App private key and deploy-key rotation cadence | PM-001, IN-005-it4 | Medium | nse-requirements | Phase-5 | Add to REQ-041: "The App private key SHALL be rotated at minimum every 12 months or immediately upon any personnel change affecting source-repo secrets access, whichever is sooner. Deploy keys, if used, SHALL be rotated on the same schedule. The rotation schedule and most-recent rotation date SHALL be documented in the org-registration runbook (REQ-043)." AC: Runbook `runbooks/org-registration.md` contains an explicit rotation schedule section and rotation date log. |
| B-6 | Unattested-push alert and attestation-before-push ordering | FM-010-it004, FM-006-it004 | Medium | nse-requirements | Phase-6 | Add to REQ-042: "If the attestation step fails or exits non-zero, the force-push step SHALL NOT execute; the workflow SHALL exit non-zero with a diagnostic identifying the unattested-release condition. The monitoring workflow (NFR-006/REQ-035) SHALL additionally detect and alert (GitHub issue) if the live tip SHA has no corresponding build-provenance attestation." AC: Simulate attestation API failure mid-run; confirm force-push does not execute; confirm monitoring workflow alerts on the unattested tip SHA. |
| B-7 | Generation workflow liveness monitor | PM-006, FM-008-it004 | Medium | nse-requirements | Phase-6 | Add to REQ-044: "The meta-monitor SHALL additionally verify that the latest source-repo `v*` tag has a corresponding dedicated-repo deployment or `Source-Commit:` trailer update within 2 hours of the tag-push timestamp. A mismatch SHALL open a GitHub issue distinguishing 'backstop monitor not running' (existing REQ-044) from 'generation workflow did not fire for latest tag.'" AC: Disable the `cowork-skeleton.yml` workflow; push a v* tag; confirm the meta-monitor opens a generation-liveness issue within the next scheduled meta-monitor run (≤25h). |
| B-8 | File-count early-warning threshold | PM-007, FM-009-it004 | Low | nse-requirements | Phase-6 | Add to REQ-034d: "The workflow SHALL additionally emit the tracked file count of the generated tree to `$GITHUB_STEP_SUMMARY` on every run. The continuous integrity monitor (NFR-006) SHALL open a GitHub issue as a non-blocking early warning when the tracked file count exceeds 3,500 files (~70% of the 5,000 CoWork limit), mirroring the 150 MB / 250 MB two-tier pattern." AC: The scheduled monitor opens a non-blocking early-warning issue when the file count exceeds 3,500; the CI hard-fails at 5,000. |

---

## Remediation — (C) Phase-3+ Implementation Concerns

Noted for future revision cycles. Do NOT require for Phase-2 sign-off or the Phase-5/Phase-6 gate. These are architectural residuals and implementation-phase concerns to be addressed in Phase-3 design or during implementation.

| ID | Finding IDs | Concern |
|----|-------------|---------|
| C-1 | RT-004 | Faithful-derivative gate (`git diff --quiet ... ':!projects/' ':!tests/'`) does not verify the `tests/` strip was actually executed — a workflow omitting `git rm tests/` passes the gate silently. Add a post-strip verification step (e.g., `git ls-files tests/ | wc -l` asserts 0). Phase-3 implementation detail. |
| C-2 | RT-005 | REQ-044 meta-monitor placement is "dedicated repo or source repo" with no decision. Dedicated-repo placement may violate CR-02 loop-safety; source-repo placement shares threat root with monitored generation system. Explicit architecture decision needed in Phase-3. |
| C-3 | DA-002 | Attestation has no user-facing verification path in the CoWork install flow — `claude plugin marketplace add geekatron/jerry@cowork-skeleton` does not invoke `gh attestation verify`. The attestation is not verified at the point of distribution. Acknowledged residual gap; document explicitly in ADR-003 L2 risk register as a known limitation of the CoWork platform. Phase-3 documentation. |
| C-4 | DA-003 | App key vs classic PAT improvement is blast-radius reduction (one repo vs many), NOT threat-class reduction. For the specific skeleton-forgery threat, stealing the App key has equivalent consequence to stealing a targeted PAT. Rephrase ADR-003 D3 rationale to "reduces blast radius" rather than "reduces threat class." Minor precision fix for future ADR revision. |
| C-5 | DA-005 | Trusted-maintainer attack path undocumented: a principal with `main` write access and `v*` tag creation rights can push a malicious commit to `main`, then tag it — D5 provenance assertion PASSES. This path needs a threat model entry (e.g., SC-06 Trusted-Maintainer) and a mitigating control (peer review required for all main-branch commits from tag-create principals). Phase-3 STRIDE update. |
| C-6 | DA-004 | REQ-043 two-admin approval for org-registration change has no GitHub-native technical enforcement mechanism. A single compromised admin can re-register unilaterally. The process control should be supplemented with a technical workaround (e.g., GitHub App webhook that detects and alerts on single-actor registration change). Phase-3 governance hardening. |
| C-7 | FM-010-it004 | Pipeline ordering: force-push executes before attestation creation. A CI failure between push and attestation leaves the skeleton live but permanently unattested for that release. Consider pipeline reorder: attestation signature BEFORE force-push, or an explicit "unattested release" detection and re-attestation mechanism. Phase-5 implementation design. |
| C-8 | FM-008-it004 | Staleness detection SLA is ≤ weekly for the lazy check. Silent generation workflow failure could go undetected for up to 7 days. Reduce to ≤ daily once B-7 (generation workflow liveness monitor) is implemented. Depends on B-7. |

---

## Projected Post-Fix Score

### After (A) MUST-FIX-NOW only

| Dimension | Current | Projected |
|-----------|---------|-----------|
| Completeness | 0.73 | 0.78 |
| Internal Consistency | 0.62 | 0.88 |
| Methodological Rigor | 0.80 | 0.82 |
| Evidence Quality | 0.77 | 0.83 |
| Actionability | 0.74 | 0.84 |
| Traceability | 0.85 | 0.88 |
| **Composite** | **0.74** | **~0.83** |

### After (A) + (B) operational hardening

| Dimension | Current | Post-(A)+(B) |
|-----------|---------|-------------|
| Completeness | 0.73 | 0.90 |
| Internal Consistency | 0.62 | 0.90 |
| Methodological Rigor | 0.80 | 0.84 |
| Evidence Quality | 0.77 | 0.85 |
| Actionability | 0.74 | 0.90 |
| Traceability | 0.85 | 0.89 |
| **Composite** | **0.74** | **~0.88** |

Post-(A)+(B) composite verification:
(0.90 × 0.20) + (0.90 × 0.20) + (0.84 × 0.20) + (0.85 × 0.15) + (0.90 × 0.15) + (0.89 × 0.10)
= 0.180 + 0.180 + 0.168 + 0.128 + 0.135 + 0.089 = **0.880 ≈ 0.88**

**Note:** 0.88 is below the 0.92 gate. The remaining gap to 0.92 requires addressing the (C) items — particularly C-5 (trusted-maintainer threat model), C-7 (attestation ordering), and C-3 (explicit install-time gap documentation) — which improve Methodological Rigor and Evidence Quality. A post-(A)+(B)+(C) score of approximately **0.93-0.95** is projected.

---

## Leniency Bias Check (H-15 Self-Review)

- [x] Each dimension scored independently — no dimension score influenced by another
- [x] Evidence documented for each score — specific requirement IDs, ADR section references, and strategy finding IDs cited per dimension
- [x] Uncertain scores resolved downward — Internal Consistency held at 0.62 (not rounded up to 0.65) given confirmed BLOCKING contradiction and 6 additional Major+ inconsistencies; Actionability held at 0.74 (not 0.77) given two Phase-blocking unimplementable requirements
- [x] Calibration anchors applied: 0.74 composite for a substantial C4 design deliverable with sound architecture but significant internal contradictions is calibrated against "first drafts typically score 0.65-0.80"; this is above first-draft range reflecting the genuine Phase-2 hardening quality, but held below 0.85 by the 7 confirmed inconsistencies
- [x] No dimension scored above 0.95; Traceability at 0.85 is the highest score, justified by the complete STK→REQ→ADR→Component chain confirmed by S-007 constitutional review
- [x] High-scoring dimension verification for Traceability (0.85): (1) Full STK-001 through STK-006 trees in Traceability Summary; (2) Allocation Matrix maps all 44+ requirements to implementing component with Phase allocation; (3) STRIDE threat IDs cited in every ADR-003 decision rationale and corresponding REQ rationale
- [x] Low-scoring dimension verification: Internal Consistency (0.62) — 7 contradictions confirmed by 5+ independent strategies; Completeness (0.73) — 7 operational gaps confirmed by 2+ strategies each; Actionability (0.74) — 2 Phase-blocking unimplementable requirements confirmed by 5 strategies each
- [x] Weighted composite matches calculation: 0.146 + 0.124 + 0.160 + 0.1155 + 0.111 + 0.085 = 0.7415 → 0.74 ✓
- [x] Verdict matches score range: 0.74 falls in "0.70-0.84: REVISE — significant gaps, focused revision needed" ✓
- [x] Improvement recommendations are specific and actionable — each (A) item specifies exact REQ text changes; each (B) item specifies exact addition language and acceptance criteria

**Anti-Leniency Statement:**

This scoring was conducted with active leniency counteraction. The architecture of the Phase-2 design is genuinely sound — S-003 Steelman and S-013 Inversion independently found zero substantive architectural flaws, and this strength is reflected in the Methodological Rigor score of 0.80. However, the Internal Consistency score of 0.62 was not inflated: seven confirmed contradictions are present across the deliverable set, one of which (REQ-020/REQ-042) makes a Phase-6 requirement literally unimplementable. The Completeness score of 0.73 was not inflated: seven operational hardening requirements are absent, several of which are security-critical (key exfiltration via workflow_dispatch, repo metadata drift, org-registration repointing). The composite of 0.74 is lower than a superficial reading of a well-structured design document might suggest; it reflects the presence of blocking contradictions and material operational gaps that prevent the deliverable set from being sent to implementation in its current state.

---

*Scoring Strategy: S-014 LLM-as-Judge (template: `.context/templates/adversarial/s-014-llm-as-judge.md`)*
*SSOT: `.context/rules/quality-enforcement.md` (H-13 threshold >= 0.92, 6-dimension weighted composite)*
*Findings incorporated: s-001 Red Team, s-002 Devil's Advocate, s-003 Steelman, s-004 Pre-Mortem, s-007 Constitutional AI, s-011 Chain-of-Verification, s-012 FMEA, s-013 Inversion (all iteration-004)*
*Constitutional Compliance: P-001 (evidence-based), P-002 (persisted to file), P-003 (no subagents), P-004 (provenance cited), P-020 (deliverables not modified), P-022 (no score inflation)*
