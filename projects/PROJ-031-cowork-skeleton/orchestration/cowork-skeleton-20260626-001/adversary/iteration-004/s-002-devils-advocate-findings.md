# Devil's Advocate Report: PROJ-031 Revised Design (ADR-001 amended + ADR-003 + REQ-038–044)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** ADR-001 (Phase-2 amended), ADR-003 (new), phase1-requirements.md (REQ-038–044 + REQ-035/NFR-006 demotion)
**Criticality:** C4
**Date:** 2026-06-29
**Reviewer:** jerry:adv-executor (BLIND, Group C — Challenge; iteration-004)
**H-16 Compliance:** S-003 Steelman applied iteration-004 (confirmed: `adversary/iteration-004/s-003-steelman-findings.md` exists)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All 7 findings with severity and dimension |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, and response requirements for Critical and Major |
| [Recommendations](#recommendations) | Prioritised action list (P0 / P1 / P2) |
| [Scoring Impact](#scoring-impact) | Impact of findings on S-014 dimensions |

---

## Summary

Seven counter-arguments identified: 1 Critical, 4 Major, 2 Minor. The design's core architectural moves — dedicated repo, prevention-by-default, attestation anchor — are directionally sound and represent a genuine structural improvement over ADR-002. However, the Critical finding reveals that the headline claim ("direct-push is now PREVENTED, not merely detected") is accurate only for repo-admin actors; org-owner bypass of the non-overridable ruleset is acknowledged only as a detection residual while being narrated as outright prevention. Three Major findings weaken the security claims around attestation's user-facing value, the App private-key risk, and the enforceability of the two-admin-approval requirement for org registration. Recommend **REVISE** to add explicit trust-boundary statements, correct the prevention-scope claim, and document enforcement mechanisms for REQ-043 before proceeding to AG-04.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-i004 | "Non-overridable org-level ruleset" does not cover org-owner bypass — prevention claim is incomplete | Critical | ADR-003 D2: "which repo admins cannot override"; DR-02 bounded only by "audit-log alert" for the residual | Methodological Rigor |
| DA-002-i004 | Attestation (REQ-042/D4) has no user-facing verification path in the CoWork install flow | Major | REQ-042: "users SHALL use the attestation (verifiable via `gh attestation verify`)" — CoWork install invokes no attestation verification step | Evidence Quality |
| DA-003-i004 | GitHub App private key introduces same threat class (durable credential theft enabling skeleton forgery) as a classic PAT for the specific threat | Major | ADR-003 D3: "The App private key becomes the project's single long-lived secret (c-208, CR-03) — a new but bounded surface" | Methodological Rigor |
| DA-004-i004 | REQ-043 "minimum of two admin approvals" for org-registration change has no described technical enforcement mechanism | Major | REQ-043: "A minimum of two admin approvals SHALL be required for any registered-source change" — no GitHub API or workflow enforces this | Completeness |
| DA-005-i004 | D5/REQ-038–039 close rogue-tag path only for non-maintainer actors; implicit trust boundary not stated | Major | ADR-003 D5: "CI faithfully attests it. Branch protection (D2) is blind — CI is the legitimate pusher" — applies equally when a trusted maintainer pushes malicious content to `main` and tags it | Completeness |
| DA-006-i004 | ADR-001 body still says `tests/` is "retained today" — internal inconsistency with Phase-2 amendment | Minor | ADR-001 §Canonical Plugin-Retention Surface row 8: "retained today (1,744 ≪ 5,000)" contradicts Phase-2 amendment header and ADR-003 strip set | Internal Consistency |
| DA-007-i004 | REQ-035 backstop-monitor acceptance criterion (b) requires performing the exact action REQ-040 prevents — no governance path for test bypass | Minor | REQ-035 AC: "Simulate a direct push to dedicated repo default branch with a different tree" while REQ-040 prohibits all human direct push to that branch | Actionability |

---

## Detailed Findings

### DA-001-i004: "Non-Overridable Org-Level Ruleset" — Prevention Claim Incomplete for Org Owners [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR-003 §D2, §Consequences (Negative #3), §Options Considered (Dimension 2) |
| **Strategy Step** | Step 3 — counter-argument lenses: Unstated assumptions, Alternative interpretations |

**Claim Challenged:**

ADR-003 D2: "We will write-lock the dedicated repo's default branch with an org-level ruleset in which the CI identity… is the SOLE push bypass actor, with ZERO human write collaborators, **and which repo admins cannot override**." ADR-003 L0: "A malicious direct push is now **PREVENTED**, not merely detected — this resolves the Phase-1 'unprotected branch' Critical outright."

**Counter-Argument:**

GitHub's access control model has two distinct principal classes: **repo admins** (admin role scoped to a specific repository) and **org owners** (owner role for the entire organization with authority over org-level settings). An org-level ruleset **can be deleted or disabled by any org owner** — not by repo admins, which is the precise qualification stated in the ADR. Therefore the prevention claim "ZERO human write" is accurate only for repo-admin-class actors. An org owner who wants to push to `geekatron/jerry-cowork`'s default branch can: (1) disable or delete the org-level ruleset, (2) push directly, (3) optionally re-enable the ruleset. This sequence converts the protection back to detection-only for the org-owner threat surface.

The ADR's treatment of DR-02 ("admin-suppression") says it is "bounded by using an org-level ruleset repo-admins cannot override." This framing presents the "cannot override" property as the resolution of admin suppression, when it resolves only **repo-admin** suppression. The bounds on **org-owner** suppression are: "admin minimization, 2FA/SSO, audit-log alert, attestation backstop" — all detection or access-reduction controls, none prevention. The ADR does not explicitly name org-owner bypass as a residual; the DR-02 language implies it is closed while leaving it open.

**Evidence:**

ADR-003 §Consequences Negative #3: "A repo admin could toggle protection. Mitigation: org-level ruleset repo-admins cannot override." This is the explicit statement that conflates repo-admin and org-owner bypass. The word "admin" is used imprecisely throughout: "admin minimization, 2FA/SSO" appears in the DR-02 residual but without distinguishing between repo-admin (blocked) and org-owner (unbounded prevention-wise) principals.

ADR-003 L0 declares the Phase-1 Critical "resolved outright." This language appears in the executive summary read by approvers at AG-04 and overstates the protection class.

**Impact:**

If an org owner is compromised (social engineering, credential theft, insider threat), the entire prevention posture collapses to detection-only. For an artifact that "is code that runs on every user's session start" with one registration reaching every user at once (ADR-003 L0), a 24-hour detection window is a meaningful exposure. The C4 security story delivered to approvers at AG-04 is overstated.

**Dimension:** Methodological Rigor — the threat model analysis is incomplete for the org-owner principal class.

**Response Required:** Revise ADR-003 D2 and REQ-040 to explicitly name org-owner bypass as a residual, state the actual prevention claim as "prevention for all sub-org-owner actors," and document the org-owner-specific controls (minimum org owners, org-owner access review cadence, org-owner credential protection) separately from the repo-admin treatment. The L0 summary must be revised to reflect the conditional scope of prevention.

**Acceptance Criteria:** ADR-003 D2 and REQ-040 contain explicit language stating that the prevention claim applies to repo-admin-class actors; org-owner bypass is named as a distinct residual with its own mitigations enumerated (separate from repo-admin DR-02); the L0 claim "PREVENTED, not merely detected" is qualified with the org-owner caveat.

---

### DA-002-i004: Attestation Has No User-Facing Verification Path in CoWork Install Flow [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 §D4, REQ-042 |
| **Strategy Step** | Step 3 — counter-argument lenses: Unstated assumptions, Unaddressed risks |

**Claim Challenged:**

ADR-003 D4: "This resolves the Phase-1 5-strategy convergent Critical (SC-04)… The attestation is CI-only-writable and publicly verifiable — a genuinely independent reference." REQ-042: "integrity verification workflows and **users** SHALL use the attestation (verifiable via `gh attestation verify`) as the integrity anchor."

**Counter-Argument:**

"Publicly verifiable" and "actually verified by users" are not the same condition. The CoWork install flow is: `claude plugin marketplace add geekatron/jerry-cowork` → CoWork server-side registry → clone default branch → install. At no point in this flow does CoWork invoke `gh attestation verify`. Regular end users installing the plugin do not run CLI verification commands before use. Therefore, while the attestation is technically CI-only-writable and technically verifiable by anyone with `gh` CLI, it is in practice verified ONLY by: (a) the automated backstop monitor (REQ-035/NFR-006), and (b) security researchers or maintainers running manual checks.

REQ-042 states "users SHALL use the attestation" but provides no mechanism by which CoWork users perform this step during installation. The requirement is unimplementable in the user install context as written. The attestation serves as evidence for the backstop monitor — which is a real and valuable improvement — but this makes it a SECONDARY mechanism supporting the monitor, not a PRIMARY mechanism protecting users.

The net result: if D2 (prevention) fails (org-owner suppression) and the backstop monitor hasn't run since the last successful check (up to 24 hours under ≤ daily cadence), users install potentially tampered content with no attestation-based protection triggered in their session.

**Evidence:**

ADR-003 D4: "This replaces the Phase-1 publish-then-assert monitor as the PRIMARY integrity mechanism." But the reduced backstop monitor is retained (not deleted) and is the only automated entity actually calling the attestation comparator. The attestation's role in practice is: evidence store for the monitor. The monitor is the actual primary check. REQ-042 AC: "(b) `gh attestation verify <skeleton-tip-sha> --repo geekatron/jerry` exits zero" — this is a maintainer-executed command, not a user-install-time check.

**Impact:**

The attestation is described as resolving SC-04 "outright." In practice SC-04 is resolved for the maintainer/monitor view of integrity; it remains open for the user-install-time view. The gap between "technically verifiable" and "actually verified" at install time means tampered content can reach users between monitor runs.

**Dimension:** Evidence Quality — the primary evidence for the security improvement claim (attestation verification) lacks a mechanism in the critical user-install code path.

**Response Required:** ADR-003 D4 and REQ-042 must clarify that attestation verification in the user install flow is NOT currently possible through CoWork's client (no API hook); the attestation serves as evidence for the backstop monitor and manual checks. The "PRIMARY integrity mechanism" language should be revised to reflect that D2 (prevention) is the primary user-protecting mechanism, and attestation is the primary post-facto evidence mechanism. REQ-042 must remove "users SHALL use" or replace it with an accurate description of who performs verification.

**Acceptance Criteria:** ADR-003 D4 explicitly states that attestation verification occurs via the backstop monitor and manual maintainer checks, not in the user install flow; REQ-042 removes or qualifies the "users SHALL use" language; the D4 summary accurately names D2 (prevention) as the primary user-protective mechanism.

---

### DA-003-i004: GitHub App Private Key Threat Class Overstated as Structural Improvement [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 §D3, §Consequences (Negative #1) |
| **Strategy Step** | Step 3 — counter-argument lenses: Logical flaws, Alternative interpretations |

**Claim Challenged:**

ADR-003 D3 rejects classic PAT because "a CI compromise pivots back to `main` or any other repo the human owner can reach (CI-05/CR-01, elevation). Forbidden." The App token is presented as a qualitatively safer alternative.

**Counter-Argument:**

The classic PAT is correctly rejected for its **multi-repo scope** — an attacker who compromises the CI workflow gets access to many repos. The App private key (or deploy key) narrows the scope to one repo. This is a genuine improvement in blast radius. However, the ADR overstates the improvement when framed against the **specific threat being protected** (pushing malicious content to `geekatron/jerry-cowork`). For that specific threat:

- Classic PAT compromise: attacker can push malicious content to the skeleton repo (and others). OUTCOME: malicious skeleton delivered.
- App private key compromise: attacker can push malicious content to the skeleton repo (and only the skeleton repo). OUTCOME: **identical** — malicious skeleton delivered.

The design's key claim is "eliminates broad write-collaborator exposure" — true for OTHER repos, but not for the actual threat. The App private key is the project's "single long-lived secret" (ADR-003 own language, c-208/CR-03) that, if stolen, enables **indefinitely durable forgery** of the artifact until the key is rotated. This is the same threat class as PAT compromise for the relevant asset.

Additionally, the App private key (a PEM file in GitHub Actions Secrets) faces the same exfiltration vectors as a classic PAT in the same location: a compromised workflow step with access to the secret, an org owner with repository settings access, or a GitHub platform incident. The "short-lived minted token" property means no push-usable secret persists at scale — but the key to generate those tokens (the private key) persists permanently.

**Evidence:**

ADR-003 Consequences Negative #1: "New long-lived secret: the App private key (or deploy key). Theft enables durable forgery of the artifact (CR-03)." The ADR names the identical threat class but bounds it with "a new but bounded surface." The bounding is scope reduction (one repo), not threat-class reduction. The same sentence in the classic PAT section: "Theft enables durable forgery" is the same consequence, just narrower.

**Impact:**

The ADR's security comparison presents moving from PAT to App key as a class improvement. The actual improvement is scope reduction. The security story for C4 should present this accurately: the App key reduces blast radius but does not reduce the severity of compromise for the actual asset being protected.

**Dimension:** Methodological Rigor — the threat comparison conflates "blast radius" improvement with "prevention class" improvement for the specific threat.

**Response Required:** ADR-003 D3 must clarify the nature of the improvement: scope reduction (one repo), not threat-class reduction for the skeleton-push threat. The risk table entry for CR-03 should acknowledge that App private key theft enables the same skeleton-forgery outcome as a PAT, bounded to one repo. The Negative #1 consequence must be presented without "bounded" as a qualifier that understates the risk, given that the specific threat outcome (malicious skeleton to all users) is identical for the App key vs. PAT.

**Acceptance Criteria:** ADR-003 D3 explicitly states that the App private key improvement over classic PAT is "blast radius confinement (one repo vs. many)" rather than "eliminates the credential-theft threat"; the risk table entry for CR-03 names skeleton-forgery-to-all-users as the consequence of App key theft with the same impact rating as it would have for a PAT theft.

---

### DA-004-i004: REQ-043 "Minimum of Two Admin Approvals" Has No Technical Enforcement Mechanism [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | REQ-043, ADR-003 §D1 (org registration), §Consequences (Negative #2) |
| **Strategy Step** | Step 3 — counter-argument lenses: Unstated assumptions, Historical precedents of failure |

**Claim Challenged:**

REQ-043: "CoWork marketplace registration of `geekatron/jerry-cowork` as the canonical org plugin source SHALL be restricted to vetted org admins; **a minimum of two admin approvals SHALL be required** for any registered-source change."

**Counter-Argument:**

CoWork marketplace registration is an administrative action performed in org settings, not a GitHub-native workflow with PR review semantics. GitHub has no built-in feature that enforces "two admin approvals before changing which repo is registered as the org's CoWork source." There is no GitHub Actions workflow, no ruleset, and no org policy that mechanically blocks a single org admin from re-registering the marketplace source.

The two-admin-approval requirement therefore exists only as a **process control**: a documented policy (the runbook) stating that two admins must agree. A single compromised or malicious org admin can:
1. Access org settings for CoWork marketplace
2. Change the registered source to a typosquatted or attacker-controlled repo
3. All org users now install from the attacker's repo on next update

This is OR-01 (rogue org registration), rated HIGH impact in the ADR risk table. The control documented is: "vetted-admin restriction; canonical-name runbook; periodic verification; audit-log review." None of these are enforcement mechanisms; they are access controls (who can act) and detection controls (audit log). The "minimum of two admin approvals" requirement is the only language implying a technical gate — but no technical gate is described.

**Evidence:**

ADR-003 §Consequences Negative #2: "Trust concentrates at the org-admin registration. One bad or spoofed registration reaches every user (OR-01/02). Mitigation: vetted-admin restriction, canonical-repo-name runbook, periodic registered-source verification, audit-log review." None of these mitigations enforce the two-admin requirement; they reduce the population of actors and detect after-the-fact. REQ-043 AC: "Attempt to re-register without required approvals: blocked" — but no mechanism is described for producing the block.

**Impact:**

OR-01 is rated MED probability, HIGH impact. If the only control is a process policy with no technical enforcement, a single admin compromise collapses the org registration protection. For an artifact deployed to every user in an org on a single registration action, this is a high-consequence residual with detection-only mitigation.

**Dimension:** Completeness — REQ-043 mandates a two-admin-approval control but does not specify how it is technically enforced.

**Response Required:** REQ-043 must either: (a) name the specific technical mechanism that enforces two-admin approval (e.g., a separate "registration review" workflow requiring dual sign-off, or a GitHub environment protection rule wrapping the registration step), or (b) acknowledge that two-admin approval is a process control only and revise "SHALL be required" to reflect what is actually enforceable ("SHALL be documented in the runbook and audited quarterly"). The risk table entry for OR-01 must reflect the actual control class (process, not technical prevention).

**Acceptance Criteria:** REQ-043 either names a technical enforcement mechanism with a concrete implementation description, or revises the "minimum of two admin approvals SHALL be required" language to accurately reflect the process-only nature of the control; the risk table OR-01 entry is updated to reflect detection-class mitigation rather than prevention.

---

### DA-005-i004: D5/REQ-038–039 Leave Trusted-Maintainer Rogue-Build Path Undocumented [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 §D5, REQ-038, REQ-039 |
| **Strategy Step** | Step 3 — counter-argument lenses: Unstated assumptions, Unaddressed risks |

**Claim Challenged:**

ADR-003 D5: "The dedicated repo does NOT fix the rogue-tag attack. We will add (a) a tag-on-`main` provenance assertion in the generation workflow and (b) a `v*` tag-protection ruleset on the source repo." ADR-003 concludes this closes SC-02 and moves it from YELLOW to GREEN.

**Counter-Argument:**

D5's two controls — merge-base assertion (REQ-038) and tag protection (REQ-039) — together close the rogue-tag path for actors who CANNOT push to `main`. They do NOT close it for actors who CAN push to `main` AND CAN create tags (i.e., "designated maintainers" per REQ-039). A compromised or malicious maintainer who has both capabilities can:

1. Push malicious content to `main` (subject only to `main`'s branch protection, a separate control)
2. Create a `v*` tag pointing at that malicious commit on `main`
3. The provenance gate (REQ-038) PASSES — the tag commit IS an ancestor of `main`
4. CI faithfully builds, faithfully attests, and faithfully delivers the malicious skeleton to all users

The ADR acknowledges in L2: "With direct-push prevented (D2) and the anchor attested (D4), the one attack the architecture still cannot see is CI faithfully building from an illegitimate tag (D5). This is intrinsic to any 'CI is the trusted builder' model." But D5 only addresses EXTERNAL rogue tags (non-main commits). The **maintainer-compromise path** (malicious commit ON main, legitimately tagged) is explicitly stated as the "CI is the trusted builder" residual — but this residual is NEVER named explicitly in the threat model tables, requirements, or risk register.

The implicit trust assumption — "all designated tag creators and main-branch write-access holders are fully trusted" — is correct for normal threat modeling of a small open-source project. But for a C4 supply-chain review of an artifact that ships executable hooks to all org users at once, this trust assumption should be explicit, not implicit. A reader of ADR-003 could believe the design protects against any insider threat, when it protects only against external/unauthorized actors for the rogue-tag vector.

**Evidence:**

ADR-003 D5: "A collaborator pushes a well-formed `v9.9.9` tag pointing at a malicious commit (not on `main`)." The "(not on `main`)" qualification is the load-bearing phrase — it scopes D5 to non-main commits only. Maintainers who can push to `main` are explicitly trusted to do so. REQ-039: "restricting `v*` tag creation to the release pipeline / maintainers only" — "maintainers" retain tag-creation authority, which means the same people who can push to `main`.

**Impact:**

The threat model tables do not contain an entry for "compromised maintainer pushes malicious commit to `main`, tags it, and CI faithfully builds and attests it." This is the primary residual threat for the "CI is the trusted builder" model, and its absence from the explicit risk register means it will not be tracked, monitored, or revisited.

**Dimension:** Completeness — the threat model is missing an explicit entry for the maintainer-compromise trusted-builder path.

**Response Required:** ADR-003 D5 and the risk register must explicitly state: "The trust boundary for D5 controls is: protection applies for actors who cannot push to `main` AND cannot create `v*` tags. A trusted maintainer who can both push to `main` and create tags is an explicitly trusted principal; the controls do not protect against this class of compromise." A risk table entry must be added: "Trusted maintainer (main-write + tag-create) pushes malicious commit and tags it; Probability LOW, Impact HIGH; Mitigation: SLSA progress + code review on `main`; Residual: accepted trusted-principal assumption." This makes the trust boundary visible to AG-04 approvers.

**Acceptance Criteria:** ADR-003 D5 contains explicit language bounding the protection to "non-maintainer, non-main-write actors"; a new risk table row names the trusted-maintainer path with probability, impact, and explicit acceptance rationale; REQ-038 and REQ-039 include a traceability note to this acceptance.

---

### DA-006-i004: ADR-001 Body Retains "tests/ Retained Today" Prose — Contradiction with Phase-2 Amendment [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-001 §Canonical Plugin-Retention Surface (row 8, body prose) |
| **Strategy Step** | Step 3 — counter-argument lens: Contradicting evidence |

**Claim Challenged:**

ADR-001 §Canonical Plugin-Retention Surface, row 8 body text: "but are retained today (1,744 ≪ 5,000)" — referring to `docs/`, `runbooks/`, `overrides/`, `scripts/`, `tests/`.

**Counter-Argument:**

The ADR-001 Phase-2 amendment header (2026-06-28) explicitly states the strip set is extended to include `tests/`. ADR-003 §L1 pipeline specification and REQ-002 both confirm `git rm -r projects/ tests/`. The body prose of ADR-001 §Canonical Plugin-Retention Surface was not updated to reflect this change — it still describes `tests/` as retained. REQ-005 notes this inconsistency and says "Do NOT edit ADR-001; flagging for ps-architect" — which means the contradiction is known but deferred, leaving ADR-001 internally inconsistent with its own amendment header.

**Evidence:**

ADR-001 §Canonical Plugin-Retention Surface: "docs/, runbooks/, overrides/, scripts/, tests/ are not load-bearing for plugin function and MAY be stripped later if the file-count margin tightens (R-002) — but **are retained today** (1,744 ≪ 5,000)." ADR-001 Phase-2 amendment header: "extends the strip set to include `tests/`." REQ-002: "The skeleton generation script SHALL strip the `projects/` directory AND the `tests/` directory entirely."

**Impact:**

An implementer reading ADR-001's body without noting the amendment header will find contradictory instructions. The amendment is prominent but easy to miss when the body text affirmatively states `tests/` is "retained today." This is a maintenance-surface inconsistency in the SSOT document.

**Dimension:** Internal Consistency.

**Response Required:** ADR-001 §Canonical Plugin-Retention Surface body text should be updated (or the amendment header should be strengthened) to remove the "retained today" language about `tests/`. REQ-005's "Do NOT edit ADR-001; flagging for ps-architect" deferral should be closed.

---

### DA-007-i004: REQ-035 Backstop-Monitor Acceptance Test Requires Authorized Bypass of REQ-040 Prevention Control [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | REQ-035 AC (b), REQ-040 |
| **Strategy Step** | Step 3 — counter-argument lens: Unaddressed risks |

**Claim Challenged:**

REQ-035 AC (b): "Simulate a direct push to dedicated repo default branch with a different tree; confirm the event-driven monitor fires, detects the SHA mismatch, creates a GitHub issue, and exits non-zero."

**Counter-Argument:**

REQ-040 prohibits all human direct push to the dedicated repo's default branch via a non-overridable (for repo admins) org-level ruleset. REQ-035's acceptance test (b) requires performing exactly this action to validate the detection backstop. There is no documented governance path for temporarily bypassing the prevention control to run an acceptance test — the test cannot be executed by a human without either: (a) temporarily disabling the ruleset (which is itself a security-sensitive action with audit implications), or (b) using the CI bypass actor (which is the normal push path, not the "rogue push" path being tested).

This creates an operational tension: acceptance testing the detection backstop requires violating the prevention control. Without a documented test procedure, REQ-035's acceptance criterion (b) may never be exercised.

**Evidence:**

REQ-035 AC (b): "Simulate a direct push to dedicated repo default branch with a different tree" — direct push is prevented by REQ-040 for all non-CI actors. No documented test-mode bypass or CI-controlled test path for this acceptance criterion exists in the requirements.

**Impact:**

The detection backstop (NFR-006/REQ-035) may be untested in practice, reducing confidence that tamper detection would fire when needed.

**Dimension:** Actionability.

**Response Required:** REQ-035 should add a note on how acceptance criterion (b) is executed — e.g., using a test branch that does not have the ruleset applied, or a documented test that has the CI bypass actor push a deliberately wrong tree and verifies the monitor catches it. The procedure for the one-time ruleset-bypass test (if used) should be documented in the runbook with audit steps.

---

## Recommendations

### P0: Critical Findings — MUST resolve before AG-04 approval

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-001-i004 | Revise ADR-003 D2 and REQ-040 to explicitly name org-owner bypass as a distinct residual. Revise the L0 summary prevention claim to be scoped to "sub-org-owner actors." Add org-owner-specific mitigations to the DR-02 section (separate from repo-admin treatment). | ADR-003 D2 contains "org-owner bypass" explicitly named as a residual with its own mitigation block; L0 "PREVENTED" claim is qualified; REQ-040 reflects the accurate protection scope. |

### P1: Major Findings — SHOULD resolve before AG-04; require justification if not

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-002-i004 | Revise ADR-003 D4 and REQ-042 to accurately describe attestation's role: evidence for the backstop monitor and manual maintainer checks, not a user-install-time verification. Identify D2 (prevention) as the primary user-protective mechanism. | D4 and REQ-042 do not use "PRIMARY integrity mechanism" to describe attestation without qualification; REQ-042 removes or clarifies "users SHALL use"; D2 is named as the primary mechanism protecting end users at install time. |
| DA-003-i004 | Revise ADR-003 D3 risk entry for CR-03 to state the threat class accurately: App private key theft enables identical skeleton-forgery outcome for the specific threat, with blast radius limited to one repo. | D3 CR-03 row names skeleton-forgery-to-all-users as the consequence with the same impact rating it would have for PAT theft; the "bounded" qualifier does not obscure the per-repo threat severity. |
| DA-004-i004 | Revise REQ-043 to either specify a technical enforcement mechanism for two-admin approval or accurately describe the two-admin control as a process control with detection-only enforcement. Update the OR-01 risk table accordingly. | REQ-043 accurately describes the control class; "SHALL be required" replaced with achievable language if no technical gate exists; OR-01 risk entry reflects detection-class mitigation. |
| DA-005-i004 | Add an explicit risk table entry for the trusted-maintainer path to ADR-003 and a trust-boundary statement to D5 bounding its protection to non-maintainer actors. | ADR-003 D5 contains an explicit trust-boundary statement; risk table contains a "compromised maintainer (main-write + tag-create)" row with probability, impact, and explicit acceptance rationale visible at AG-04. |

### P2: Minor Findings — MAY resolve; acknowledgment sufficient

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-006-i004 | Remove or update the "retained today (1,744 ≪ 5,000)" language in ADR-001 §Canonical Plugin-Retention Surface to reflect the Phase-2 tests/ strip. Close the deferral noted in REQ-005. | ADR-001 §Canonical Plugin-Retention Surface body text does not describe `tests/` as retained. |
| DA-007-i004 | Add to REQ-035 a note on the test procedure for acceptance criterion (b), including how a "simulated rogue push" is performed without violating REQ-040's active ruleset. | REQ-035 AC (b) includes a concrete test path that does not require undocumented ruleset bypass. |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-004 (REQ-043 two-admin approval lacks mechanism) and DA-005 (trusted-maintainer risk path absent from threat model) leave material gaps in the security specification. |
| Internal Consistency | 0.20 | Negative | DA-001 (prevention claim vs. org-owner bypass residual) and DA-006 (ADR-001 body contradicts its own amendment) create contradictions within the deliverable set. |
| Methodological Rigor | 0.20 | Negative | DA-001 (incomplete threat model for org-owner principal) and DA-003 (overstated security class improvement for credential change) weaken the rigor of the security argument. |
| Evidence Quality | 0.15 | Negative | DA-002 (attestation cited as PRIMARY mechanism without a user-install verification path) reduces confidence in the evidence supporting the primary integrity claim. |
| Actionability | 0.15 | Slightly Negative | DA-007 (REQ-035 acceptance test has no implementation path) reduces actionability of the backstop testing requirement; all other requirements remain actionable. |
| Traceability | 0.10 | Neutral | Requirements trace to ADR decisions throughout. DA-005's trust-boundary absence does not break existing traces; it adds a missing entry. |

**Overall Assessment:** Targeted revision recommended (P0 + P1 findings are addressable without redesign). The core architectural direction — dedicated repo, prevention-by-default, attestation anchor — withstands scrutiny. The revisions needed are documentation accuracy, trust-boundary explicitness, and claims-scoping rather than design changes. The Critical finding (DA-001) is a documentation and framing issue, not a design invalidation; the prevention mechanism (D2) is sound within its actual scope. The design is close to acceptance-ready; P0 and P1 revisions are focused and achievable within one iteration.

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 1 (DA-001-i004)
- **Major:** 4 (DA-002-i004, DA-003-i004, DA-004-i004, DA-005-i004)
- **Minor:** 2 (DA-006-i004, DA-007-i004)
- **Protocol Steps Completed:** 5 of 5
- **H-16 Verified:** Yes (S-003 iteration-004 confirmed)
- **Template:** `.context/templates/adversarial/s-002-devils-advocate.md` v1.0.0
- **Deliverables Reviewed:** ADR-001 (amended 2026-06-28), ADR-003 (2026-06-28), phase1-requirements.md (Phase-2 update 2026-06-29)
- **Blindness Maintained:** No adversary directory content read during analysis
