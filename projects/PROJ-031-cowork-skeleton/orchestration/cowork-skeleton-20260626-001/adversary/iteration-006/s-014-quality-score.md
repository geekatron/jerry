# Quality Score Report: PROJ-031 CoWork Skeleton — Consolidated Design Package

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, one-line assessment |
| [Scoring Context](#scoring-context) | Deliverable, type, criticality, strategy |
| [Score Summary](#score-summary) | Weighted composite table |
| [Dimension Scores](#dimension-scores) | Per-dimension score and evidence summary |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Evidence, gaps, improvement path per dimension |
| [Delta vs Iteration-005](#delta-vs-iteration-005) | Which dimensions moved and why |
| [Improvement Recommendations](#improvement-recommendations) | Consolidated deduplicated remediation plan |
| [Fixable-vs-Inherent Assessment](#fixable-vs-inherent-assessment) | Root issue classification and ceiling assessment |
| [Leniency Bias Check](#leniency-bias-check) | Anti-leniency verification |

---

## L0 Executive Summary

**Score:** 0.82/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.78)

**One-line assessment:** The Claim-Status Convention added in iteration-006 materially closes the iteration-005 Internal Consistency drag (+0.15 on that dimension), bringing the composite from 0.724 to 0.82; however, 10 FIXABLE-NOW design-phase gaps — including a missing G-update fallback architecture, an unanalyzed compound rogue-tag/monitor attack path, no Phase-5 gate technical enforcement mechanism, and a factual ADR-001/ADR-003 contradiction on monitor operation — block the 0.92 threshold; after those 10 items are resolved, the honest design-phase ceiling is approximately 0.86–0.88, with the remaining gap to 0.92 being structural (inherent platform limits + Phase-5-gate residuals).

---

## Scoring Context

- **Deliverable:** Consolidated design package — 5 artifacts
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md`
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-003-credential-protection-supply-chain.md`
  - `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md`
  - `projects/PROJ-031-cowork-skeleton/security/phase2-stride-threat-model.md`
  - `projects/PROJ-031-cowork-skeleton/security/phase2-attack-surface.md` (historical recon)
- **Deliverable Type:** Design (ADR + Requirements + Security Architecture)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Strategy Findings Incorporated:** Yes — 9 strategy reports from iteration-006 blind tournament
  - Group A: s-010-self-refine-findings.md
  - Group B: s-003-steelman-findings.md
  - Group C: s-002-devils-advocate-findings.md, s-004-pre-mortem-findings.md, s-001-red-team-findings.md
  - Group D: s-007-constitutional-ai-findings.md, s-011-cove-findings.md
  - Group E: s-013-inversion-findings.md, s-012-fmea-findings.md
- **Scored:** 2026-06-29T00:00:00Z
- **Prior Scores:** iteration-004 = 0.74; iteration-005 = 0.724 (Internal Consistency = 0.68 dominant drag)
- **Calibration Applied:** C4 DESIGN-PHASE — Phase-5-deferred items (controls labeled "Designed — operational validation pending [G-x]") are APPROPRIATE and do NOT reduce scores. Only genuine design-phase gaps (unanalyzed attack paths, internal contradictions, missing fallback architecture, incorrect specifications) reduce scores.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.82 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE — Significant gaps, focused revision needed (0.70–0.84 band) |
| **Strategy Findings Incorporated** | Yes — 9 strategy reports ingested |
| **Critical Findings (from strategy reports)** | 18 distinct Critical-severity findings across all 9 strategies |
| **Distinct Root Issues (deduplicated)** | 10 FIXABLE-NOW root issues identified |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.78 | 0.156 | Package is comprehensive (28-threat STRIDE, full REQ set, 2 ADRs) but 8 material design-phase gaps: missing G-update fallback architecture, unanalyzed compound rogue-tag/monitor path, no Phase-5 gate evidence mechanism, ADR spec contradictions |
| Internal Consistency | 0.20 | 0.83 | 0.166 | Claim-Status Convention closes iteration-005's systemic P-222 overclaim problem; remaining: 1 factual contradiction (ADR-001 vs ADR-003 on monitor clone vs ls-remote), 1 implicit D5/D7 dependency not made explicit, 2 minor labeling gaps |
| Methodological Rigor | 0.20 | 0.82 | 0.164 | STRIDE+DREAD+attack trees+Claim-Status Convention+Phase-5 gate set is sophisticated C4 security methodology; gaps: RT-002 compound attack not analyzed, D8 gate criterion incomplete on semantic injection residual, Phase-5 gate technical enforcement absent |
| Evidence Quality | 0.15 | 0.83 | 0.1245 | CoVe register confirms 12/18 claims VERIFIED; Claim-Status Convention honestly distinguishes verified from designed; gaps: gh attestation verify syntax unverified (CV-005), REQ-047 webhook event type unconfirmed (CV-004) |
| Actionability | 0.15 | 0.82 | 0.123 | Phase-5 gate set with specific acceptance criteria and OWNER assignments is genuinely actionable; gaps: G-update fallback path completely unspecified (cannot act if G-update fails), D5/D8 have no tracked delivery stories, Phase-5 gate evidence mechanism absent |
| Traceability | 0.10 | 0.87 | 0.087 | ADR→STRIDE→REQ chain is exemplary; Claim-Status Convention provides Gate traceability; gaps: CV-006 cross-ADR citation error (ADR-001 cites ADR-003 D7 for a claim ADR-003 does not make), R1 stale REQ-043→REQ-047 reference |
| **TOTAL** | **1.00** | | **0.82** | |

---

## Detailed Dimension Analysis

### Completeness (0.78/1.00)

**Evidence of strength:**
The package covers an extraordinary breadth for a Phase-2 design deliverable: WS-1 through WS-5 requirements (REQ-001 through REQ-055+), two comprehensive ADRs (ADR-001 and ADR-003 with D1–D8), a 28-threat STRIDE model with DREAD scoring and two attack trees, the Claim-Status Convention (all Phase-2 controls tagged "Designed — operational validation pending [G-x]"), six Phase-5 non-deferrable gates, five Residual Trust Boundaries (RTB-1..5) with honest disclosures, the D8 Detector Specification (C1–C6 pattern taxonomy, allow-list mechanism, fail-closed requirement), and clone-weight telemetry with early-warning band.

**Genuine design-phase gaps:**

1. **G-update fallback not architected (DA-001-it6c, PM-001-I006, IN-001-it006s013):** The Phase-5 gate G-update specifies "CoWork delivers rebuilds to already-installed users — OR a manual update procedure is documented." The "OR" fallback has zero design content. No candidate fallback paths (versioned release branches, explicit user-facing update command) are specified. If G-update reveals CoWork caches at install time, the project has no designed response. ADR-001 L2 §6 acknowledges the risk clearly but does not design past it.

2. **RT-002 compound attack path entirely absent (RT-002-i6):** The combination REQ-053 `actions: write` + pre-G-provenance D5 gap enables a compound rogue-tag build path via monitor workflow compromise. If any Action in `cowork-monitor.yml` is unpinned (REQ-017 is scoped to `cowork-skeleton.yml` only), a compromised Action can use the monitor's `actions: write` to dispatch the generation workflow with a rogue tag. D5 (not yet implemented) is the only control that would stop this; its absence enables a faithfully-built, faithfully-attested malicious skeleton. This compound path is not analyzed anywhere in the five design artifacts.

3. **Phase-5 gate set has no technical enforcement (IN-003-it006s013):** All six Phase-5 gates are process controls — ADR-003 sections and requirements checklist entries. No technical mechanism prevents org-marketplace-registration from proceeding before all gates pass. There is no specified `phase5-gate-evidence.md` file requirement, no CI gate, no cryptographic proof of gate execution. Delivery pressure can silently bypass the entire gate set.

4. **`gh attestation verify` syntax may be wrong in spec (CV-005-i006):** ADR-003 D7 specifies `gh attestation verify <tip-sha> --repo geekatron/jerry`. The standard `gh attestation verify` interface is documented for file artifacts (binaries, OCI images), not raw git commit SHAs. No artifact tests or cites documentation for this invocation. If the syntax is incorrect, the entire attestation check in D7 fails or returns an error — the G-monitor acceptance criterion cannot be satisfied.

5. **Missing by omission — design spec gaps (FM-011, FM-015, FM-021, FM-030, FM-008):** (a) Per-job permissions isolation not specified: `id-token` and `contents:write` co-located in a single job per current spec — if a step in the attest phase is compromised, push credentials are available. (b) Monitor workflow hosting: `cowork-monitor.yml` would be overwritten on every CI force-push to the dedicated repo, silently deleting the monitor. (c) "Last-good" tag for auto-revert undefined: REQ-053 mandates auto-revert to "last-good" but no specification says how last-good is tracked or advanced. (d) Plugin retention surface (ADR-001 c-003) is a static 9-entry list — not auto-generated from plugin.json; new agents can be silently excluded from skeleton if c-003 is not manually updated.

**Improvement path:**
Close the 5 gap categories above: (1) specify 2 candidate G-update fallback paths, (2) analyze and document RT-002 compound path with REQ-017 scope extension and REQ-053→G-provenance cross-reference, (3) add `phase5-gate-evidence.md` spec, (4) verify and correct `gh attestation verify` syntax, (5) add per-job isolation, monitor hosting, last-good-tag, and retention-surface-generation specs to ADR-003. Estimated composite improvement: +0.05 on Completeness.

---

### Internal Consistency (0.83/1.00)

**Evidence of strength:**
The Claim-Status Convention — the primary iteration-006 quality investment — materially resolves the iteration-005 dominant drag (0.68 from systemic P-222 "NOW-RESOLVED" overclaims). All Phase-2 controls now carry "Designed — operational validation pending [G-x]" tags consistently throughout all five artifacts. RTB-1 through RTB-5 are honest about detection-only limitations. The D5 "blocks go-live" language is consistent across ADR-003, STRIDE, and requirements. The CoVe claim-verification register (C-10: "Claim-Status Convention applied consistently — VERIFIED") independently validates this.

**Gaps:**

1. **CV-006: Factual contradiction between ADR-001 and ADR-003 on monitor operation.** ADR-001 Clone-Weight Decision states: "The continuous integrity workflow clones the skeleton every cycle — see ADR-003 D7." ADR-003 D7 specifies: "Monitor reads the dedicated repo's live default-branch tip SHA (`git ls-remote / gh api`, read-only). Does NOT perform a full clone." These are mutually exclusive operations. If ADR-001 is correct, the clone-weight telemetry scheme works but ADR-003 underspecifies the monitor. If ADR-003 is correct, the clone-weight telemetry scheme claimed in ADR-001 is not implemented. One of these artifacts contains a false claim.

2. **RT-004: D7 freshness presents as rogue-tag protection but depends entirely on D5 (implicit dependency).** D7 description presents "attestation check + freshness check" as the monitoring posture, which to a naive reader implies comprehensive coverage. The freshness check (newest v* tag deployed) passes on a rogue-tag attack if CI faithfully builds from the rogue tag — freshness is only useful against failed-regeneration staleness (SC-07). The sole control against SC-02 (rogue tag) is D5, which is unimplemented. ADR-003 D7 does not state "D7 (freshness) provides zero protection against SC-02 — D5 is the load-bearing control for that path." This creates false confidence.

3. **CC-005/RT-001: Mixed messaging on D8 coverage.** Some locations in ADR-003 D8 and STRIDE SC-08 use "closes the trace" or equivalent language. Other locations in the same documents acknowledge "static scanning of natural-language instructions has false-negatives on novel phrasing — D8 reduces but does not fully close." The status field and the prose disclosure contradict each other. A reader scanning the STRIDE threat table gets a different signal than one reading the prose.

4. **CC-003: Allocation matrix REQ-040 row inconsistency.** The STRIDE risk register correctly carries "(G-prevention pending)" for R-007b. The allocation matrix row for REQ-040 (which maps D2 controls to R-007b) does not carry this qualifier. A reader scanning the allocation matrix sees a GREEN without knowing it is pending validation.

5. **R1 (s-010): REQ-043 body references REQ-047 as "≤24h automated polling monitor."** REQ-047 has been descoped to an audit-log webhook (OQ-047 descoped). The ≤24h automated polling reference is stale and contradicts the descope rationale.

**Improvement path:**
Fixes are mechanical: (1) reconcile ADR-001/ADR-003 monitor operation in one sentence, (2) add explicit D5 dependency statement to ADR-003 D7 text and REQ-049, (3) replace "closes the trace" in STRIDE SC-08 with "partially mitigates — pattern-catalog scope only; semantic injection residual open," (4) add "(G-prevention pending)" to allocation matrix REQ-040 row, (5) correct REQ-043 body reference to REQ-047. Estimated composite improvement: +0.05 on Internal Consistency.

---

### Methodological Rigor (0.82/1.00)

**Evidence of strength:**
The STRIDE + DREAD + attack-tree methodology is applied with genuine rigor: 28 threats across 5 areas, DREAD scoring with explicit rationale, AT-1 (malicious hook delivery) and AT-2 (defeat tamper detection) attack trees with multi-step kill-chain analysis, Phase-5 Validation Gate Set with non-deferrable AND-pass condition, per-gate acceptance criteria (some acceptance tests are multi-point), Claim-Status Convention as an operationalized honesty mechanism, per-job permissions isolation design (conceptually), and D8 Detector Specification with C1–C6 taxonomy including false-positive handling via hash-pinned allow-list. The RTB framework for acknowledging permanent residuals is methodologically appropriate and uncommon for this level of deliverable.

**Gaps:**

1. **RT-002 compound attack path not analyzed.** The combination of (unpinned Action in `cowork-monitor.yml`) + (monitor's `actions: write` permission) + (D5 unimplemented) creates a compound attack that is NEITHER PREVENTED NOR DETECTED. None of the three independent inputs (RT-002, FM-012, IN-006) identifying this gap are derived from speculation — each traces to specific spec text. The STRIDE methodology includes AT-1 and AT-2 but did not analyze this compound path involving the monitoring infrastructure itself as an attack surface.

2. **D8 gate criterion does not encode semantic injection residual (CC-001-20260628).** G-content acceptance criterion validates that C1/C2 synthetic patterns trigger blocking, but does not include: (a) a formal residual disclosure in the criterion itself, (b) any bound on the semantic injection surface left unmitigated, (c) any false-negative rate assessment for novel phrasing. At C4, gate criteria are the authoritative evidence of what was verified; prose disclosure of the residual is insufficient if the gate criterion treats the pattern-catalog coverage as equivalent to content safety. The gate label "G-content" and "the scanned artifact" language creates an implicit overconfidence signal.

3. **Phase-5 gate technical enforcement is absent (IN-003-it006s013).** The Claim-Status Convention is excellent for design-phase tracking, but the Phase-5 gate set has no process artifact that would physically prevent go-live without gate execution. The R-001 precedent within ADR-001 itself (a machine-checkable assumption verified before Phase-2) demonstrates the methodological pattern; applying this pattern consistently would require a specified `phase5-gate-evidence.md` with gate CI run IDs committed before org-registration.

4. **G-update-pre sequencing gap (CC-002-20260628).** The G-update assumption (CoWork update propagation to already-installed users) is labeled "load-bearing" and the R-001 precedent within ADR-001 establishes that load-bearing assumptions require pre-phase machine-checkable verification. By the R-001 precedent, G-update should gate Phase-5 ENTRY, not Phase-5 exit — otherwise Phase-5 implementation investment could be wasted if G-update reveals caching. The methodological inconsistency is that ADR-001 itself defines and applies this pre-phase check pattern, then doesn't apply it to G-update.

**Improvement path:**
(1) Add RT-002 compound path analysis to STRIDE with remediation spec (REQ-017 extension + G-actions-write-safe gate); (2) amend G-content acceptance criterion to encode semantic residual; (3) add `phase5-gate-evidence.md` mechanism; (4) add G-update-pre entry gate at Phase-5 entry per CC-002. Estimated improvement: +0.03.

---

### Evidence Quality (0.83/1.00)

**Evidence of strength:**
The CoVe S-011 claim-verification register independently assesses 18 load-bearing claims: 12 VERIFIED, 5 UNVERIFIED, 1 CONTRADICTED. The VERIFIED items include: ~1,417 files after stripping (C-01), Option A idempotency logic (C-04), D3 1h token expiry (C-09), Claim-Status Convention applied consistently (C-10), SC-02 at rank 1 YELLOW (C-11), D7 ls-remote operation (C-12, within ADR-003), G-update Phase-5 blocker (C-13), RTB-3 no technical enforcement (C-14), D8 pattern-category coverage (C-15), REQ-049 ≤2h SLA (C-16), Phase-5 AND-pass requirement (C-17). This is strong evidence discipline for a design-phase deliverable. The Claim-Status Convention itself is an evidence quality mechanism: it distinguishes "Designed" from "Implemented & validated" throughout, preventing the design from overclaiming its own evidence base.

**Gaps:**

1. **CV-005: `gh attestation verify` syntax unverified for raw git SHA.** ADR-003 D7 specifies `gh attestation verify <tip-sha> --repo geekatron/jerry` as the attestation check invocation. The standard `gh attestation verify` interface (GitHub CLI ≥ 2.49) is documented for file artifacts and OCI image digests — not raw git commit SHAs. Using a git commit SHA as the attestation subject is an atypical usage that may not be supported without additional flags. No artifact cites documentation confirming this syntax. If the syntax is wrong, the entire D7 attestation verification step requires redesign.

2. **CV-004: REQ-047 audit-log webhook event type implementability unverified.** The descope of OQ-047 (polling approach rejected because "no documented API endpoint") is well-reasoned. But the residual (REQ-047 audit-log webhook for CoWork marketplace-settings changes) faces the same documentation gap: if CoWork is an Anthropic-side feature not integrated into GitHub's native Apps/Marketplace API surface, CoWork registration changes may not generate GitHub org audit log events. No artifact confirms this specific event type exists in GitHub's documented webhook surface.

3. **CC-004: Audit-log webhook event type reliability unconfirmed.** The ADR describes the webhook as "near-real-time" detection, but the specific webhook event type for org CoWork registration/deregistration changes is not cited against GitHub documentation.

**Improvement path:**
(1) Test exact `gh attestation verify` invocation on actual Jerry release attestation and document verified syntax in ADR-003; (2) confirm or refute whether GitHub audit-log emits events for CoWork marketplace changes; if unconfirmed, amend RTB-3 characterization and track as OQ-049. Estimated improvement: +0.02.

---

### Actionability (0.82/1.00)

**Evidence of strength:**
The Phase-5 Validation Gate Set is the most actionable element of the package: 6 gates, each with specific acceptance criteria (not vague pass/fail conditions but specific test descriptions), AND-pass requirement, explicit "blocks go-live" language for the critical gates, and OWNER assignments (ps-architect, eng-architect, nse-requirements) distributed consistently throughout ADR-003 and STRIDE. The REQ-to-ADR traceability enables implementation teams to know which requirement implements which design decision. The Claim-Status Convention makes the action chain explicit: "this needs to happen before go-live [G-x]." The adversary strategy reports each produce specific, bounded, owner-tagged remediation recommendations.

**Gaps:**

1. **G-update fallback path completely unspecified (DA-001-it6c, SM-002-it006s3).** If G-update empirical testing reveals CoWork caches at install time, the design provides no actionable path forward. ADR-003 G-update gate says "OR a manual update procedure is documented" but provides zero content for what that procedure entails, who designs it, or what constitutes a minimal acceptable alternative. The team cannot act on this if G-update fails.

2. **D5 and D8 have no tracked delivery stories (IN-002, IN-010).** D5 (tag-on-main provenance assertion, REQ-038+REQ-039) is labeled "blocks go-live" but has no worktracker STORY, no implementation deadline, no CI check preventing deployment if absent. Same for D8 (pattern catalog + scanner + G-content test). A "blocks go-live" label in a design document is not a delivery mechanism; without tracked stories and named implementation owners, these are aspirations rather than scheduled work.

3. **Phase-5 gate evidence mechanism not specified (IN-003).** The Phase-5 Authorization Checklist exists in ADR-003 and requirements, but there is no specified process artifact (e.g., `phase5-gate-evidence.md`) that would make gate execution verifiable before org-registration. The actionability of the gate set is limited by the absence of a concrete proof-of-execution mechanism.

4. **CC-002: No user gate before Phase-5 implementation (P-020).** G-update validation is placed at Phase-5 exit (after full implementation). The R-001 precedent and P-020 (user authority) both argue for a G-update-pre gate at Phase-5 entry: if G-update reveals caching, the user can redirect the implementation before weeks of CI pipeline work are committed. The current sequencing defers this user decision to after maximum implementation investment.

5. **"Last-good" auto-revert target undefined (FM-021, SM-006-it006s3).** REQ-053 mandates auto-revert to "the last-good v* tag" but neither ADR-003 nor requirements define how "last-good" is tracked, when it is advanced, or how the monitor knows which version to revert to. The auto-revert mechanism is unactionable as specified.

**Improvement path:**
(1) Design minimum 2 G-update fallback candidates; (2) add delivery STORYs for D5 and D8; (3) specify phase5-gate-evidence.md; (4) add G-update-pre as Phase-5 entry decision; (5) define "last-good" tag advancement rule (propose: `last-good-validated` tag, advanced only after a full G-monitor pass cycle). Estimated improvement: +0.04.

---

### Traceability (0.87/1.00)

**Evidence of strength:**
The ADR-001 → ADR-003 → STRIDE → REQ chain is genuinely exemplary. The Claim-Status Convention tags each Phase-2 control to its Phase-5 gate (e.g., "Designed — operational validation pending [G-provenance]"), making the validation dependency traceable. The FMEA FM-NNN identifiers in ADR-003 cross-reference to STRIDE failure modes. The CoVe claim-verification register (18 claims with artifact traceability). The RTB designations with explicit source-of-constraint. STK-002 re-scoped and traced to REQ-054/OQ-048 with the Phase-5 gate link. The adversary strategy findings trace to specific ADR decision codes, requirement IDs, and STRIDE threat IDs throughout.

**Gaps:**

1. **CV-006: Broken cross-reference (Critical).** ADR-001 Clone-Weight Decision cites "see ADR-003 D7" as support for the claim that the monitor clones the skeleton. ADR-003 D7 does not specify a clone — it specifies `git ls-remote / gh api` (explicitly NOT a clone). The cross-reference is factually incorrect.

2. **R1 (s-010): Stale reference.** REQ-043 body text references REQ-047 as "≤24h automated polling monitor." REQ-047 was descoped from polling to audit-log webhook during iteration-006. The body text was not updated to reflect the descope, creating a traceability inconsistency within the requirements file.

3. **Missing story links for D5 and D8.** There are no worktracker STORY IDs traceable from REQ-038 (D5 ancestor assertion) or REQ-052 (D8 pattern catalog) to implementation delivery. The traceability chain stops at the requirement level with no "owned by STORY-NNN" link.

4. **CC-003: Allocation matrix inconsistency.** The STRIDE risk register carries "(G-prevention pending)" for R-007b. The allocation matrix row for REQ-040 (which maps D2 to R-007b) does not carry this qualifier. The same control has different pending-validation signals in two views of the same document.

**Improvement path:**
(1) Reconcile ADR-001 Clone-Weight Decision and ADR-003 D7 on monitor operation; (2) correct REQ-043 body reference; (3) add STORY IDs for D5/D8 implementation; (4) add G-prevention pending qualifier to allocation matrix. Estimated improvement: +0.02.

---

## Delta vs Iteration-005

| Dimension | Iter-005 (est.) | Iter-006 | Delta | Primary Driver |
|-----------|-----------------|----------|-------|----------------|
| Completeness | ~0.76 | 0.78 | +0.02 | D8 content-safety gate added; Phase-5 gate set formalized; Claim-Status Convention makes gaps visible rather than hidden |
| **Internal Consistency** | **0.68** | **0.83** | **+0.15** | **Claim-Status Convention replaces systemic P-222 overclaims ("NOW-RESOLVED", "is prevented") with honest "Designed — operational validation pending [G-x]" throughout all five artifacts** |
| Methodological Rigor | ~0.74 | 0.82 | +0.08 | STRIDE expanded (28 threats vs prior), attack trees AT-1/AT-2 added, D8 Detector Specification added, Phase-5 gate set with specific acceptance criteria added |
| Evidence Quality | ~0.79 | 0.83 | +0.04 | Claim-Status Convention provides evidence-layer honesty; new unverified claims (G-update, D5) are CORRECTLY labeled; prior overclaims removed |
| Actionability | ~0.74 | 0.82 | +0.08 | Phase-5 gate set with specific acceptance criteria and OWNER assignments dramatically increases actionability; Claim-Status Convention makes the action chain explicit |
| Traceability | ~0.82 | 0.87 | +0.05 | Claim-Status Convention + gate traceability; FM-NNN cross-references; RTB designations; Phase-5 gate set links |
| **COMPOSITE** | **0.724** | **0.82** | **+0.096** | |

**Why it moved:** The Claim-Status Convention was the single highest-leverage intervention. The iteration-005 dominant drag was Internal Consistency 0.68 caused by widespread achieved-present-tense claims for unbuilt controls across ADR-001 and ADR-003. The iteration-006 convention that ALL Phase-2 controls must carry "Designed — operational validation pending [G-x]" tags simultaneously resolved that systemic problem. The structural STRIDE/gate/D8 additions added smaller but meaningful improvements to Methodological Rigor and Actionability.

**What didn't move enough:** Completeness only improved +0.02 because while D8 and the gate set were added, several material design-phase gaps (G-update fallback, RT-002 compound path, Phase-5 enforcement mechanism) were introduced or remained. These represent genuinely new analysis from the iteration-006 blind tournament that the design does not yet address.

---

## Improvement Recommendations

### Priority-Ordered Remediation Plan (Deduplicated Root Issues)

All findings from 9 strategy reports have been deduplicated into 10 distinct root issues below. Each finding ID cluster confirms convergent evidence.

| Priority | Root Issue | Tag | OWNER | Finding IDs | Score Impact |
|----------|-----------|-----|-------|-------------|--------------|
| P0 | **R-001: Resolve ADR-001/ADR-003 internal contradiction on monitor operation (clone vs ls-remote)** | [FIXABLE-NOW] | ps-architect | CV-006-i006 | Internal Consistency, Completeness |
| P0 | **R-002: Specify G-update fallback architecture before Phase-3 + add G-update-pre Phase-5 entry gate** | [FIXABLE-NOW] | ps-architect (ADR-001 fallback), nse-requirements (REQ-054, CC-002 gate spec) | DA-001-it6c, PM-001-I006, CV-001-i006, IN-001-it006s013, CC-002-20260628, SM-002-it006s3 | Completeness, Actionability |
| P0 | **R-003: Analyze RT-002 compound attack path; extend REQ-017 to all workflow files; cross-reference REQ-053 to G-provenance** | [FIXABLE-NOW] | nse-requirements (REQ-017, REQ-053), ps-architect (ADR-003 D7 dep, Phase-5 gate) | RT-002-i6, RT-006-i6 | Completeness, Internal Consistency |
| P0 | **R-004: Amend G-content gate criterion and SC-08 threat status to encode semantic injection residual explicitly** | [FIXABLE-NOW] | eng-architect (D8 spec, STRIDE SC-08), nse-requirements (G-content criterion), ps-architect (risk band) | RT-001-i6, CC-001-20260628, CC-005-20260628, CV-003-i006, DA-004-it6c | Internal Consistency, Methodological Rigor |
| P1 | **R-005: Specify `phase5-gate-evidence.md` requirement; make org-registration runbook reference it** | [FIXABLE-NOW] | nse-requirements (Phase-5 checklist), ps-architect (ADR-003) | IN-003-it006s013 | Methodological Rigor, Actionability |
| P1 | **R-006: Verify and document correct `gh attestation verify` invocation syntax for the D7 monitor** | [FIXABLE-NOW] | eng-architect | CV-005-i006 | Evidence Quality, Completeness |
| P1 | **R-007: Fix minor labeling/reference inconsistencies** | [FIXABLE-NOW] | ps-architect (allocation matrix), nse-requirements (REQ-043 stale ref) | CC-003-20260628, R1 (s-010), CC-004-20260628 | Internal Consistency, Traceability |
| P1 | **R-008: Specify missing design elements: per-job isolation, monitor hosting, last-good tag, retention surface generation** | [FIXABLE-NOW] | ps-architect (ADR-003 revisions) | FM-011-it006, FM-015-it006, FM-021-it006, FM-030-it006 | Completeness |
| P2 | **R-009: Create tracked delivery STORYs for D5 and D8 implementation; link from ADR-003 and REQ-038/052** | [FIXABLE-NOW] | eng-architect (story creation), nse-requirements (REQ links) | IN-002-it006s013, IN-010-it006s013 | Actionability, Traceability |
| P2 | **R-010: Upgrade REQ-051 to two-reviewer SHALL for retained-surface PRs + add context-leakage review checklist** | [FIXABLE-NOW] | nse-requirements (REQ-051), ps-architect (RTB-2 compensating controls) | RT-001-i6, RT-003-i6, DA-004-it6c | Completeness, Methodological Rigor |

---

## Fixable-vs-Inherent Assessment

### Root Issue Classification

| Root Issue | Classification | Rationale |
|-----------|---------------|-----------|
| R-001: ADR-001/ADR-003 monitor contradiction | [FIXABLE-NOW] | Text reconciliation in 1–2 sentences |
| R-002: G-update fallback + G-update-pre gate | [FIXABLE-NOW] | Specify 2 candidate fallback paths; add gate entry spec |
| R-003: RT-002 compound attack path | [FIXABLE-NOW] | REQ-017 scope extension + ADR-003 cross-reference text |
| R-004: G-content gate criterion semantic residual | [FIXABLE-NOW] | Spec text amendment to gate criterion + status label |
| R-005: Phase-5 gate evidence mechanism | [FIXABLE-NOW] | Add `phase5-gate-evidence.md` file requirement to spec |
| R-006: `gh attestation verify` syntax | [FIXABLE-NOW] | Test invocation; document correct syntax in ADR-003 |
| R-007: Minor labeling inconsistencies | [FIXABLE-NOW] | 3–4 one-line text corrections |
| R-008: Missing design element specs | [FIXABLE-NOW] | Add per-job isolation, monitor hosting, last-good, retention surface specs |
| R-009: Tracked delivery STORYs for D5/D8 | [FIXABLE-NOW] | Create worktracker entries; add cross-references |
| R-010: REQ-051 two-reviewer upgrade | [FIXABLE-NOW] | Text amendment from "consider" to SHALL |
| D5 implementation (G-provenance gate) | [PHASE-5-GATE] | Requires CI code development + live pipeline testing |
| D8 implementation (G-content gate) | [PHASE-5-GATE] | Requires pattern catalog + scanner tool + CI integration |
| G-update empirical verification | [PHASE-5-GATE] | Requires live CoWork client + already-installed user session |
| G-prevention bypass-actor semantics | [PHASE-5-GATE] | Requires live geekatron/jerry-cowork repo creation + test |
| G-monitor fail-closed testing | [PHASE-5-GATE] | Requires monitor implementation + multi-path injection testing |
| G-headroom live CoWork install | [PHASE-5-GATE] | Requires live CoWork client + dedicated repo existence |
| RTB-5: CoWork install-time attestation | [INHERENT] | Platform limitation; CoWork controls its install flow |
| D8 semantic injection residual | [INHERENT] | Inherent limitation of static/regex scanning; can be bounded but not eliminated |
| RTB-1: Org-owner ruleset suppression | [INHERENT] | GitHub platform limitation; cannot restrict below org-owner tier |
| CoWork update propagation unknowability | [INHERENT] (partially) | Only resolvable by Anthropic documentation or live testing (transitions to [PHASE-5-GATE] once a test environment exists) |

### Fixable-vs-Inherent Fraction Statement

**Of the residual gap to 0.92 (approximately 0.10 composite points):**
- **[FIXABLE-NOW]: ~40–45%** — Items R-001 through R-010 are pure design artifact changes. Closing all 10 is estimated to improve the composite by approximately 0.04–0.05 points.
- **[PHASE-5-GATE]: ~30–35%** — Phase-5 gate validation items. These are explicitly beyond what design artifacts can deliver; they require live infrastructure and empirical testing.
- **[INHERENT]: ~20–25%** — Platform limitations (RTB-5, RTB-1, D8 semantic injection ceiling) that no design artifact can close.

### Design-Phase Ceiling Assessment

After resolving all 10 FIXABLE-NOW items, the estimated ceiling for this design-phase deliverable is approximately **0.86–0.88**.

Estimated post-FIXABLE-NOW dimension scores:
- Completeness: ~0.83 (+0.05)
- Internal Consistency: ~0.88 (+0.05)
- Methodological Rigor: ~0.85 (+0.03)
- Evidence Quality: ~0.85 (+0.02)
- Actionability: ~0.86 (+0.04)
- Traceability: ~0.89 (+0.02)

Estimated post-FIXABLE-NOW composite: **~0.86**

**The gap from ~0.86 to 0.92 is structural, not addressable by further artifact revision.**

The remaining structural gap consists of:
- D8 semantic injection as an inherent static-scanning limitation (~0.01–0.02 drag on Internal Consistency and Evidence Quality)
- Phase-5 gates that by definition cannot be validated at design time (~0.02–0.03 drag on Completeness and Evidence Quality)
- RTB-5 / RTB-1 as permanent platform limitations (~0.01 drag on Completeness)

**Verdict on ceiling:** More iteration on the current artifacts CAN push the composite from 0.82 toward ~0.86. The 0.92 C4 quality gate CANNOT be met by editing design artifacts alone. It requires Phase-5 operational validation to validate the designed controls and reduce the inherent/Phase-5-gate residual. This is not a defect in the design approach — it is the correct and honest posture for a C4 Phase-2 design deliverable with a comprehensive Phase-5 gate set. The design correctly tells you what it cannot yet know.

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.82
threshold: 0.92
weakest_dimension: Completeness
weakest_score: 0.78
critical_findings_count: 18
iteration: 6
improvement_recommendations:
  - "R-001: Resolve ADR-001/ADR-003 monitor contradiction (clone vs ls-remote) [FIXABLE-NOW]"
  - "R-002: Specify G-update fallback architecture + G-update-pre Phase-5 entry gate [FIXABLE-NOW]"
  - "R-003: Analyze RT-002 compound attack path; extend REQ-017 to all workflow files [FIXABLE-NOW]"
  - "R-004: Amend G-content gate criterion to encode semantic injection residual explicitly [FIXABLE-NOW]"
  - "R-005: Specify phase5-gate-evidence.md requirement + runbook step [FIXABLE-NOW]"
  - "R-006: Verify and document correct gh attestation verify syntax [FIXABLE-NOW]"
  - "R-007: Fix labeling inconsistencies (allocation matrix, REQ-043 stale ref, CC-004) [FIXABLE-NOW]"
  - "R-008: Specify per-job isolation, monitor hosting, last-good tag, retention surface generation [FIXABLE-NOW]"
  - "R-009: Create tracked delivery STORYs for D5 and D8 [FIXABLE-NOW]"
  - "R-010: Upgrade REQ-051 to two-reviewer SHALL for retained-surface PRs [FIXABLE-NOW]"
fixable_fraction: "~40-45% of residual gap is FIXABLE-NOW; ~30-35% is PHASE-5-GATE; ~20-25% is INHERENT"
design_phase_ceiling: "~0.86 after resolving all FIXABLE-NOW items; 0.92 requires Phase-5 operational validation"
```

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing weighted composite
- [x] Evidence documented for each score (specific finding IDs cited per dimension)
- [x] Uncertain scores resolved downward (Completeness at 0.78 not bumped to 0.80 despite excellent breadth)
- [x] First-draft calibration considered (this is iteration-006, not a first draft; 0.82 reflects genuine improvement from 0.724)
- [x] No dimension scored above 0.95 without exceptional evidence (Traceability at 0.87 is the highest)
- [x] C4 DESIGN-PHASE calibration applied: Phase-5-deferred items NOT penalized; only genuine design-phase gaps counted
- [x] FMEA raw critical count (20) NOT used directly; calibration note followed — distinct root issues extracted and deduplicated
- [x] Anti-leniency applied: composite held at 0.82 despite temptation to round to 0.85 given strong qualitative strengths; specific evidence for each gap required before accepting any score
- [x] Weighted composite verified: 0.78×0.20 + 0.83×0.20 + 0.82×0.20 + 0.83×0.15 + 0.82×0.15 + 0.87×0.10 = 0.156 + 0.166 + 0.164 + 0.1245 + 0.123 + 0.087 = 0.82

---

*Scoring Strategy: S-014 LLM-as-Judge*
*SSOT: `.context/rules/quality-enforcement.md`*
*Adversary Strategies Ingested: 9 (all Groups A–F, iteration-006 blind tournament)*
*Agent: adv-scorer v1.0.0*
*Project: PROJ-031-cowork-skeleton*
*Constitutional Compliance: P-001 (evidence-based), P-002 (persisted), P-003 (no sub-agents), P-022 (honest scoring, anti-leniency applied)*
*Scored: 2026-06-29*
