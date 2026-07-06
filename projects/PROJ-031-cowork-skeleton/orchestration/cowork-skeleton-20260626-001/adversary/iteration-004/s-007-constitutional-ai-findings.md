# Constitutional Compliance Report: PROJ-031 Phase-2 Revised Design

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** ADR-001, ADR-003, phase1-requirements.md (Phase-2 revised design)
**Criticality:** C4 (AE-003 ADRs → C3 minimum; AE-005 security-relevant → C3 minimum; orchestration target C4 >= 0.95)
**Date:** 2026-06-29T00:00:00Z
**Reviewer:** jerry:adv-executor (blind, independent — Group D Verify)
**Constitutional Context:** JERRY_CONSTITUTION.md v1.0 (P-001 through P-043), quality-enforcement.md H-Rule Index (H-01 through H-36), markdown-navigation-standards.md (H-23)
**Blindness:** No prior adversary output consulted per task specification.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall constitutional compliance assessment |
| [Findings Table](#findings-table) | All findings with severity and affected dimension |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, and remediation for each finding |
| [Compliant Checks](#compliant-checks) | Notable checks that passed (H-04/H-05, governance retention) |
| [Remediation Plan](#remediation-plan) | Prioritised P0/P1/P2 actions |
| [Scoring Impact](#scoring-impact) | Constitutional compliance score and S-014 dimension mapping |

---

## Summary

PARTIAL compliance with the Jerry Constitution and HARD Rule Index: **1 Critical, 2 Major, 1 Minor** finding.

The dominant defect is a **hard internal contradiction** in `phase1-requirements.md`: REQ-020 explicitly forbids `id-token: write` as a workflow permission while REQ-042 (added in the Phase-2 update) mandates a Sigstore-backed build-provenance attestation, which GitHub's `gh attestation attest` requires `id-token: write` to produce. The two MUST requirements are mutually exclusive and block Phase-6 implementation. A P-022 calibration defect in ADR-003's L0 ("resolves…outright") overstates the direct-push guarantee relative to the body's own DR-02 residual. A prose consistency defect in ADR-001's body section contradicts its own amendment header on whether `tests/` is stripped. ADR-003 quotes a pre-tests-strip file count in its pipeline diagram.

**Constitutional Compliance Score: 0.78 — REJECTED** (below 0.85 threshold; H-13 applies). Revision required before Phase-5 implementation gate.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-I004 | P-001 (Truth/Accuracy); Internal Consistency | HARD (internal requirement coherence) | Critical | REQ-020 forbids `id-token: write`; REQ-042 mandates Sigstore attestation requiring `id-token: write` | Internal Consistency |
| CC-002-I004 | P-022 (No Deception) | HARD | Major | ADR-003 L0 says critical "resolved outright"; D2 explicitly retains DR-02 admin-suppression residual | Evidence Quality |
| CC-003-I004 | P-001 (Truth/Accuracy) | MEDIUM | Major | ADR-001 body §Canonical Plugin-Retention Surface says `tests/` "retained today"; amendment header and ADR-003 confirm it is stripped | Internal Consistency |
| CC-004-I004 | P-001 (Truth/Accuracy) | SOFT | Minor | ADR-003 Context pipeline shows "~1,749 files"; requirements L0 says "approximately 1,417" after tests/ strip | Completeness |

---

## Detailed Findings

### CC-001-I004: REQ-020 vs REQ-042 — Mutually Exclusive MUST Requirements [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Documents** | `phase1-requirements.md` WS-3 |
| **Principle** | P-001 (Truth/Accuracy); Internal Consistency |
| **Affected Dimension** | Internal Consistency |

**Evidence:**

REQ-020 (WS-3, original Phase-1 requirement, unchanged in Phase-2 update):
> "The `permissions:` block in `cowork-skeleton.yml` SHALL declare `contents: write` as the **sole** permission entry and SHALL NOT include `actions: write`, `packages: write`, **`id-token: write`**, or any organization-level scope."

REQ-042 (WS-3 Phase-2, added by ADR-003 mirror):
> "The CI workflow SHALL create an immutable GitHub Release and a **build-provenance attestation (Sigstore-backed, SLSA-aligned, e.g., `gh attestation`)** binding the skeleton tip SHA to the specific workflow run, source commit SHA, and source repo at generation time."

Allocation Matrix (phase1-requirements.md):
> "REQ-042 | `.github/workflows/cowork-skeleton.yml` (attestation step) | `gh attestation` (Sigstore-backed); immutable release; tip SHA bound to workflow run + source commit + source repo | Phase 6"

ADR-003 L1 confirms the attestation must be created *after* the cross-repo push, in `cowork-skeleton.yml`:
> "In CI after a successful push: create an **immutable release** for the tag and generate a **build-provenance attestation** binding the skeleton tip SHA to the run/commit/repo."

**Analysis:**

GitHub's `gh attestation attest` (and the equivalent `actions/attest-build-provenance`) requires `id-token: write` in the workflow `permissions:` block to obtain an OIDC token for Sigstore. Without `id-token: write`, the attestation step fails at runtime. There is no alternative mechanism to create a Sigstore-backed build-provenance attestation on GitHub Actions without this permission.

The attestation must bind the **skeleton tip SHA**, which is only known after `cowork-skeleton.yml` has generated and pushed the skeleton. The attestation therefore cannot live in `release.yml` (which runs before or concurrently with `cowork-skeleton.yml`). The ADR-003 Context pipeline diagram showing `release.yml → "GitHub immutable Release + build-provenance attestation"` is itself inconsistent with ADR-003's own L1 text and REQ-042's Allocation, adding an internal ADR-003 ambiguity on top of the requirements conflict.

Additionally, the Requirements Quality Checklist in the same document claims "Consistent: No conflicting requirements" — this self-assessment is factually incorrect with respect to REQ-020 and REQ-042.

**Remediation (P0 — must fix before Phase-6):**

Option A (preferred): Add `id-token: write` and `attestations: write` to the `cowork-skeleton.yml` permissions block and update REQ-020 accordingly:
```yaml
permissions:
  contents: write
  id-token: write
  attestations: write
```
Update REQ-020 rationale to explain that the Phase-2 attestation requirement (REQ-042) necessitates these additional OIDC and attestations write permissions.

Option B: Move the attestation step to a dedicated post-publication workflow (`cowork-skeleton-attest.yml`) with its own `permissions:` block that includes `id-token: write`, scoping `cowork-skeleton.yml` to `contents: write` only. Update REQ-042 Allocation to reflect the split.

Both options require correcting the Requirements Quality Checklist claim "No conflicting requirements."

---

### CC-002-I004: P-022 Over-Claim — "Resolved Outright" vs Acknowledged Residual [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Document** | `ADR-003-credential-protection-supply-chain.md` §L0, §Consequences Positive #1 |
| **Principle** | P-022 (No Deception) — confidence calibration |
| **Affected Dimension** | Evidence Quality |

**Evidence:**

ADR-003 L0 Executive Summary, item 1:
> "A malicious direct push is now **prevented**, not merely detected — this **resolves the Phase-1 'unprotected branch' Critical outright**."

ADR-003 Consequences §Positive #1:
> "Direct-push prevention — the Phase-1 unprotected-branch Critical (R-007b) is structurally closed: **no human can push** the artifact branch (D2)."

ADR-003 D2, same document:
> "Residual modes, **explicitly retained** (P-222): **admin-suppression** (DR-02 — a repo admin disabling the ruleset) is bounded by using an org-level ruleset repo-admins cannot override, admin minimization, 2FA/SSO, an audit-log alert on ruleset change, and the out-of-band attestation anchor (D4)..."

ADR-003 Risk Table §Consequences:
> "Dedicated-repo admin suppresses protection (DR-02) | LOW | **HIGH** | Org-level non-overridable ruleset; admin minimization; audit alert; attestation backstop"

**Analysis:**

P-022 requires agents not to overstate confidence levels. The L0 summary uses the term "outright" (without qualification) and the Consequences section says "no human can push," both of which would lead an L0 reader to conclude the risk is fully eliminated.

The same document's D2 body explicitly retains DR-02 as a HIGH-impact residual. Beyond repo-level admins, GitHub org-owners hold super-admin capabilities that can modify or disable org-level rulesets — a platform-level architectural reality the ADR does not acknowledge. The phrase "repo-admins cannot override" is accurate (GitHub org-level rulesets do restrict repo admin override), but org-owners retain the ability to disable or modify the org-level ruleset itself. This means the guarantee is "humans below org-owner cannot push," which is materially different from "no human can push."

The word "outright" in the L0 and "no human can push" in Consequences are in direct tension with DR-02 (HIGH impact, acknowledged LOW probability) and the org-owner bypass path. A technically diligent reader of the L0 alone would form a materially incorrect view of the residual risk posture. The S-010 Self-Refine Note says "Did not over-claim 'all resolved'" — but the L0 does say "outright," a contradiction within the ADR itself.

**Remediation (P1 — revise before user approval at AG-04):**

1. Replace "resolves the Phase-1 'unprotected branch' Critical **outright**" with a calibrated claim, e.g.: "reduces the Phase-1 'unprotected branch' Critical to a bounded residual (DR-02: LOW probability, HIGH impact), with prevention now the primary posture."

2. Replace "no human can push the artifact branch" in Consequences Positive #1 with "no human below org-owner level can push the artifact branch without explicitly disabling the org-level ruleset — an auditable, admin-minimized action (DR-02)."

3. Explicitly note in D2 that org-owners (as distinct from repo admins) retain ability to modify org-level rulesets, and specify that org-owner minimization is a required compensating control.

---

### CC-003-I004: ADR-001 Body Not Updated for tests/ Strip Amendment [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Document** | `ADR-001-skeleton-derived-branch-strategy.md` §Canonical Plugin-Retention Surface |
| **Principle** | P-001 (Truth/Accuracy) |
| **Affected Dimension** | Internal Consistency |

**Evidence:**

ADR-001 §Canonical Plugin-Retention Surface body (2026-06-26 original text, not updated):
> "By contrast `docs/`, `runbooks/`, `overrides/`, `scripts/`, `tests/` are **not** load-bearing for plugin function and MAY be stripped later if the file-count margin tightens (R-002) — but are **retained today** (1,744 ≪ 5,000)."

ADR-001 amendment header (2026-06-28):
> "the confirmed distribution mechanism…**extends the strip set to include `tests/`**."

ADR-003 Context pipeline (same date, 2026-06-28):
> "git rm -r projects/ **tests/**"

REQ-002 (phase1-requirements.md):
> "The skeleton generation script SHALL strip the `projects/` directory **AND the `tests/` directory** entirely from the generated branch."

REQ-005 (phase1-requirements.md) flags this explicitly:
> "ADR-001's body (§Canonical Plugin-Retention Surface) says `tests/` is 'retained today (1,744 ≪ 5,000)' but the ADR-001 amendment header (2026-06-28) and ADR-003 both strip `tests/`…Do NOT edit ADR-001; flagging for ps-architect."

**Analysis:**

The ADR-001 body, the authoritative document for the Canonical Plugin-Retention Surface (which REQ-005 explicitly defers to as SSOT), contains an unambiguous factual error: it says `tests/` is "retained today" when the authoritative amendment header, ADR-003, and the requirements all confirm it is stripped. A consumer reading the §Canonical Plugin-Retention Surface section to understand what is and is not in the skeleton receives incorrect information.

REQ-005 acknowledges this inconsistency but defers the correction to ps-architect with a "Do NOT edit" instruction — meaning the error is known but deliberately left in the SSOT. At C4 criticality, a known factual error in the SSOT document for the plugin-retention surface is a Major internal consistency violation regardless of the existence of a downstream flag.

**Remediation (P1 — correct in next ADR-001 revision or via a targeted amendment):**

Update the §Canonical Plugin-Retention Surface body paragraph to reflect the amendment:
- Replace "but are retained today (1,744 ≪ 5,000)" with "but `tests/` is stripped as of the Phase-2 amendment (2026-06-28); the others (`docs/`, `runbooks/`, `overrides/`, `scripts/`) remain retained today (~1,417 ≪ 5,000)."
- Update the file count in the sentence from 1,744 to ~1,417 to reflect the extended strip.

Note: REQ-005's "Do NOT edit ADR-001; flagging for ps-architect" defers but does not exempt this correction. A C4 SSOT document with a known factual error in its authoritative section cannot remain unrevised indefinitely; the flag is a routing mechanism, not a waiver.

---

### CC-004-I004: File Count Discrepancy ADR-003 (~1,749) vs Requirements (~1,417) [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Document** | `ADR-003-credential-protection-supply-chain.md` §Context pipeline diagram |
| **Principle** | P-001 (Truth/Accuracy) |
| **Affected Dimension** | Completeness |

**Evidence:**

ADR-003 §Context pipeline diagram:
> "DEDICATED  geekatron/jerry-cowork  (PUBLIC; default branch = skeleton **~1,749 files**)"

Phase1-requirements.md §L0 Executive Summary:
> "Removing both produces approximately **1,417** tracked files that fit comfortably under the limit."

ADR-001 L0 (projects/ only stripped):
> "stripping `projects/` reduces this to **~1,744 files**"

**Analysis:**

~1,749 in ADR-003 closely matches ADR-001's pre-amendment figure of ~1,744 (projects/ only stripped). When ADR-003 extended the strip set to include `tests/`, the pipeline diagram file count was not updated to reflect the new ~1,417 figure. While this is a documentation accuracy issue rather than a design defect (the implementation specifications are consistent in stripping tests/), an L0 reviewer of ADR-003 would read an incorrect file count for the distribution artifact.

**Remediation (P2 — correct for accuracy):**

Update ADR-003 §Context pipeline diagram to read "skeleton ~1,417 files" (or "skeleton ~1,400–1,450 files" if a tighter empirical count is not yet available).

---

## Compliant Checks

The following protocol checks were evaluated and found **COMPLIANT**. These are documented for completeness and to confirm the prompt's specific questions on H-04/H-05 and governance retention.

| Check | Finding |
|-------|---------|
| **H-04 bootstrap after tests/ strip** | COMPLIANT. `hooks/` (session-start.py) and `src/` (Jerry CLI) are both in the canonical retention surface (ADR-001 rows 7–8) and are NOT stripped. H-04's "active project required" bootstrap is fully intact. |
| **H-05 UV-only after tests/ strip** | COMPLIANT. `tests/` contains the test suite, not the runtime. The Jerry CLI in `src/` continues to use `uv run`; `uv.lock` is a root-level file not subject to the strip. |
| **`.context/rules` + `.claude` enforcement** | COMPLIANT. `.claude/` (row 5) and `.context/` (row 6) are both in the retention surface. The `.claude/rules/` symlink to `../.context/rules/*.md` is preserved; all constitutional enforcement files ship with the skeleton. |
| **H-23 (Navigation tables)** | COMPLIANT. All three deliverables contain navigation tables with anchor links. |
| **P-020 (User Authority — approval gates)** | COMPLIANT. ADR-001 Status notes "PENDING (user)"; ADR-003 Status notes "PENDING (user) per P-020." AG-02 and AG-04 are correctly identified as pre-approval gates. |
| **AE-003 (ADR → C3 minimum)** | COMPLIANT. Both ADRs are classified C4, exceeding the C3 minimum. |
| **AE-005 (Security-relevant → C3 minimum)** | COMPLIANT. C4 classification exceeds the C3 minimum for security-relevant content. |
| **P-004 (Explicit Provenance)** | COMPLIANT. ADRs cite external references with numbered tables; requirements trace to stakeholder needs and ADR references. |
| **P-011 (Evidence-Based)** | COMPLIANT. ADR-003's S-010 Self-Refine Note discloses that attestation mechanics are "validated against current GitHub vendor documentation, not yet exercised on geekatron/jerry-cowork" — an appropriate epistemic qualification. |

---

## Remediation Plan

**P0 (Critical — must resolve before Phase-6 implementation):**

- **CC-001-I004:** Resolve the REQ-020 vs REQ-042 permission conflict. Either (A) add `id-token: write` + `attestations: write` to REQ-020 and update the `cowork-skeleton.yml` permissions block, or (B) move the attestation step to a separate workflow with its own permissions. Correct the Requirements Quality Checklist claim "No conflicting requirements." Clarify in ADR-003 whether the attestation step belongs to `cowork-skeleton.yml` or `release.yml` (the Context pipeline diagram and L1 text are inconsistent on this).

**P1 (Major — revise before user approval at AG-04 and before Phase-5 gate):**

- **CC-002-I004:** Rephrase ADR-003 L0 and Consequences Positive #1 to calibrate confidence: replace "outright" and "no human can push" with scoped claims that accurately reflect the DR-02 residual and org-owner bypass path. Add explicit mention of org-owner privilege as a governance control point.

- **CC-003-I004:** Update ADR-001 §Canonical Plugin-Retention Surface body to reflect the Phase-2 amendment: remove "retained today (1,744 ≪ 5,000)" and state that `tests/` is stripped (with updated file count ~1,417) while the other listed directories remain retained.

**P2 (Minor — correct for accuracy before Phase-5):**

- **CC-004-I004:** Update ADR-003 §Context pipeline diagram file count from "~1,749" to "~1,417" (or the empirically measured post-strip value) to reflect the extended tests/ strip set.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (Minor) | CC-004: ADR-003 pipeline diagram states incorrect file count |
| Internal Consistency | 0.20 | Negative (Critical + Major) | CC-001: mutually exclusive MUST requirements in same document; CC-003: ADR-001 body contradicts its own amendment header |
| Methodological Rigor | 0.20 | Neutral | No constitutional findings affect process rigor; five-step S-007 protocol applied fully |
| Evidence Quality | 0.15 | Negative (Major) | CC-002: L0 confidence level inconsistent with body evidence and residual acknowledgment |
| Actionability | 0.15 | Neutral | REQ-042 is actionable but blocked by CC-001; recommendations are specific |
| Traceability | 0.10 | Neutral | No traceability violations; requirements trace to stakeholder needs; ADRs cite evidence |

**Constitutional Compliance Score:**

```
1.00
- 1 Critical  × 0.10 = 0.10
- 2 Major     × 0.05 = 0.10
- 1 Minor     × 0.02 = 0.02
─────────────────────────────
= 0.78
```

**Threshold Determination: REJECTED** (0.78 < 0.85 minimum band; H-13 applies)

The deliverable set cannot proceed to the Phase-5 implementation gate in its current form. CC-001 (Critical) is the blocking defect: two MUST requirements governing the same workflow's permissions block are mutually exclusive. Resolution is unambiguous and implementable (add `id-token: write` scope to REQ-020 / split workflow). CC-002 and CC-003 are revision items that improve P-022 calibration and document accuracy before user approval at AG-04.

---

## Execution Statistics

- **Total Findings:** 4
- **Critical:** 1 (CC-001-I004)
- **Major:** 2 (CC-002-I004, CC-003-I004)
- **Minor:** 1 (CC-004-I004)
- **Protocol Steps Completed:** 5 of 5
- **Compliant Checks Noted:** 9

---

*Strategy: S-007 Constitutional AI Critique v1.0.0*
*Template: .context/templates/adversarial/s-007-constitutional-ai.md*
*Constitutional Reference: docs/governance/JERRY_CONSTITUTION.md v1.0, quality-enforcement.md (H-01 through H-36)*
*Execution: adv-executor (blind, independent, Group D — Verify)*
*Output: projects/PROJ-031-cowork-skeleton/orchestration/cowork-skeleton-20260626-001/adversary/iteration-004/s-007-constitutional-ai-findings.md*
