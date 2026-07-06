# Devil's Advocate Report: PROJ-031 CoWork Skeleton — Phase 2 Design (5-Artifact Set)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** ADR-001, ADR-003, phase1-requirements.md, phase2-stride-threat-model.md, phase2-attack-surface.md
**Criticality:** C4
**Date:** 2026-06-29
**Reviewer:** adv-executor (iteration-005, Group C)
**Execution ID:** 20260629
**H-16 Compliance:** S-003 Steelman applied in Group B (prior group per tournament ordering: self-refine → steelman → challenge → verify → decompose → score). Confirmed.

---

## Summary

8 counter-arguments identified (1 Critical, 5 Major, 2 Minor). The design's central security claim — that D2 converts direct-push from detection to **prevention** — rests on an unvalidated GitHub feature configuration that has not been exercised on the actual target infrastructure (`geekatron/jerry-cowork` does not yet exist). The attestation anchor, framed as resolving the Phase-1 five-strategy convergent Critical, provides verification only through a scheduled CI job running every ≤6 hours; CoWork users receive zero install-time protection and most live YELLOW threats bypass attestation entirely. Neither the prevention posture nor the attestation anchor has been demonstrated to work as specified. The design acknowledges both gaps ("confirm empirically before Phase-5") but the current structure treats unconfirmed architectural properties as closed findings. **Recommend REVISE** to address the Critical finding (DA-001) and the five Major findings before AG-04 approval.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260629 | Prevention claim (D2) is unproven on actual target, conditionally bypassed by org-owners, and relies on a recent unvalidated GitHub feature | Critical | ADR-003 D2: "empirically validate before Phase-5"; RTB-1: org-owner can push tampered tree within ≤6h window | Methodological Rigor |
| DA-002-20260629 | Attestation anchor verifies nothing CoWork users can observe; sole automated verifier is D7 CI job; most YELLOW threats bypass attestation entirely | Major | ADR-003 RTB-5: "CoWork's install flow does NOT invoke `gh attestation verify`"; D7 is "sole automated verification path" | Evidence Quality |
| DA-003-20260629 | D7 ≤6h detection window is materially understated; GitHub scheduler imprecision + no mandatory auto-revert means actual attack exposure is substantially larger | Major | ADR-003 D7: "bounded by poll cadence (≤6h)"; no REQ mandating automatic revert on mismatch; meta-monitor SLA is 25h | Completeness |
| DA-004-20260629 | App private key ("single long-lived secret") protection controls are newly proposed with no acceptance criteria and no concrete implementation specifics | Major | ADR-003 RTB-4: "Theft enables durable forgery until D7 detects"; REQ-045, REQ-048 proposed with no ACs; CR-03 YELLOW (2×5=10) | Actionability |
| DA-005-20260629 | SC-06 trusted-maintainer compensating control (REQ-051 peer review) is purely procedural, added late, carries no ACs, and is inadequate for a small-org deployment | Major | ADR-003 RTB-2: "collusion of two maintainers... out of scope of automated control"; REQ-051 has no acceptance criteria; SC-06 only STRIDE threat with exclusively procedural control | Internal Consistency |
| DA-006-20260629 | REQ-047 org-registration monitor assumes unconfirmed Anthropic/GitHub API capabilities to query CoWork marketplace settings and subscribe to marketplace-settings webhooks | Major | ADR-003 RTB-3: "CoWork's org marketplace registration is a single-actor server-side setting"; REQ-047 cites no API endpoint; no empirical confirmation that audit-log webhook on "marketplace-settings change" event type exists | Evidence Quality |
| DA-007-20260629 | Attest-before-push job sequencing ("push SHALL NOT execute if attestation fails") is a workflow configuration assertion enforced by `needs:` + `if:` conditions, not a platform-level safety guarantee | Minor | ADR-003 D4: "If the attestation step fails or exits non-zero, the push SHALL NOT execute"; no dedicated CI test for attestation-failure → push-abort invariant | Traceability |
| DA-008-20260629 | D5 tag-on-main provenance assertion is entirely dependent on `main` integrity; its value collapses if REQ-051 (procedural peer review) fails, creating circular defense-in-depth | Minor | ADR-003 D5: "D5 does NOT cover the trusted-maintainer path"; assertion proves "on `main`", not "benign on `main`"; both controls (D5 and REQ-051) are interdependent for SC-06 coverage | Methodological Rigor |

---

## Detailed Findings

### DA-001-20260629: Prevention Claim Unproven and Conditionally Bypassed [CRITICAL]

**Claim Challenged:**
ADR-003 D2 states: "We will write-lock the dedicated repo's default branch with an org-level ruleset in which the CI identity (the GitHub App or deploy key of D3) is the SOLE push bypass actor, with ZERO human write collaborators, and which repo admins cannot override." The design describes this as converting the Phase-1 "unprotected branch" Critical "from detection to **prevention**."

**Counter-Argument:**
The prevention claim is architecturally aspirational, not operationally demonstrated. Three structural weaknesses invalidate it as a "closed" finding:

(1) **The org-owner bypass is not bounded prevention — it is a high-consequence residual for the exact principals who matter most.** RTB-1 states an org-owner "can modify or delete the org-level ruleset itself and then push directly" and "A malicious or compromised org-owner can push a tampered tree; harm is bounded to the ≤6h D7 detection window." For an artifact that ships executable session-start hooks to all org users via a single registration, the "highest-privilege principals can bypass this control" residual is not a minor edge case — it is the dominant attack path for a sufficiently motivated adversary. The design's Negative consequence §3 lists "Org-owner ruleset-suppression residual" but simultaneously claims "prevention" in L0, D2, and Consequences §Positive 1. These are contradictory framings.

(2) **The GitHub feature is recent, unvalidated, and self-acknowledged as requiring empirical confirmation.** ADR-003's S-010 Self-Refine Note (item 7) explicitly states: "the ruleset bypass-actor configuration on the dedicated repo... SHOULD be confirmed empirically before Phase-5." ADR-003 Negative §4 states: "Dependence on current GitHub features... immutable releases, build-provenance attestations, and ruleset bypass-actor semantics are recent (2025–2026)." The dedicated repo `geekatron/jerry-cowork` does not yet exist. The prevention posture is being approved (AG-04) based on a feature whose behavior has been validated against vendor documentation but has not been exercised on actual infrastructure.

(3) **The "org-admin cannot override" claim is semantically inconsistent.** ADR-003 D2 says "repo admins SHALL NOT be able to override it." But RTB-1 clarifies: "An org-owner / org-admin (a role above repo admin in GitHub's permission hierarchy) can modify or delete the org-level ruleset itself." The design uses "org-admin" in two different senses in the same document — one where "org-level ruleset cannot be overridden by repo admins" and another where "org-admin" (the role) can override it. This semantic confusion could cause implementors to believe the protection is stronger than it is.

**Evidence:** ADR-003 D2: "repo admins cannot override"; RTB-1: "org-admin can modify or delete the org-level ruleset"; S-010 item 7: "SHOULD be confirmed empirically before Phase-5"; Negative §4: "GitHub features... are recent (2025–2026)."

**Impact:** If the prevention posture is implemented and believed to "close" the direct-push threat vector, but either (a) the bypass-actor feature does not behave as documented, (b) an org-owner-level compromise occurs, or (c) the ruleset is misconfigured (org-admin ≠ repo-admin nuance missed), the design's entire second-order architecture (attestation, reduced monitor scope) rests on a foundation that never achieved its stated guarantee. The design would then have the detection capability of ADR-002 (a monitor) without ADR-002's honesty about "detection-only" posture.

**Dimension:** Methodological Rigor

**Response Required:** The design must either (a) empirically validate the bypass-actor configuration on `geekatron/jerry-cowork` before AG-04 approval (not deferred to Phase-5), or (b) reframe D2's claim from "prevention" to "strong deterrence with org-owner residual and detection backstop," with the implication that the security architecture remains detection-first until the empirical confirmation is complete.

**Acceptance Criteria:** Demonstrate via a live test on `geekatron/jerry-cowork` that (i) a non-bypass actor (human collaborator with write) is denied direct push, (ii) the CI identity (App/deploy key) can force-push as bypass actor, and (iii) a repo admin (non-org-owner) cannot modify the ruleset. Until this test exists, classify D2 as "prevention-pending-empirical-validation."

**Owner:** ADR → ps-architect

---

### DA-002-20260629: Attestation Verification Is CI-Internal Only; User-Facing Protection Absent [MAJOR]

**Claim Challenged:**
ADR-003 D4 states the attestation "resolves the Phase-1 5-strategy convergent Critical (SC-04)" by moving the integrity reference to "a CI-only-writable, publicly verifiable attestation." STRIDE threat model records SC-04 as "NOW-RESOLVED" and bands it to GREEN (1×5=5).

**Counter-Argument:**
The attestation resolves SC-04 for the STRIDE model but does not provide meaningful protection to the actual threat: CoWork users receiving and executing malicious hooks. The counter-position on "who actually verifies" is: the D7 scheduled CI job in the source repo is the **sole automated verifier**, running every ≤6 hours, with no user-facing component.

Examine what attestation actually protects against in the post-D2 threat landscape:

- **Post-publication direct tamper (SC-03, GREEN after D2):** An attacker bypasses branch protection (already nearly prevented by D2) and modifies the dedicated branch. Attestation catches this — but this scenario is already rated L=1×I=5=5 (GREEN) after D2. Attestation provides additional detection for a GREEN-level threat.
- **Credential theft (CI-01/CR-03, YELLOW 2×5=10):** Attacker steals App key and pushes directly to the dedicated repo using the legitimate CI identity. This push bypasses CI entirely — **no attestation is created** because the attacker pushes directly without running the attestation workflow. Attestation does not protect this path.
- **Org-owner suppression (DR-02/RTB-1, YELLOW 2×5=10):** Admin suppresses ruleset and pushes. No CI attestation job runs. Attestation does not protect this path.
- **Org-registration attack (OR-01/02, YELLOW 2×5=10):** Different repo entirely registered. Attestation on `geekatron/jerry-cowork` is irrelevant. Does not protect this path.
- **Rogue-tag attack (SC-02, YELLOW 2×5=10):** CI faithfully builds AND attests the malicious tree. The attestation **matches**. Attestation actively works against detection here — it produces a passing result for a malicious artifact.

The calculation: attestation provides meaningful protection against exactly one threat that is already GREEN-level after branch protection. Against the four live YELLOW threats, attestation is either irrelevant or actively provides false assurance (rogue-tag case). The design's framing of "resolves the 5-strategy convergent Critical" overstates what attestation achieves in terms of user-facing protection.

The Phase-1 Critical (SC-04) was specifically that "the verifier and the verified share one lock" — Release notes writeable with the same `contents: write` as the branch. The design fixes this by moving to an immutable transparency log (Sigstore). But the threat behind SC-04 was users receiving malicious hooks, not "CI has a non-independent reference value." Users still receive no independent verification — the monitor does. The fix is architecturally correct (a genuine improvement) but does not resolve the threat it claims to close.

**Evidence:** ADR-003 RTB-5: "CoWork's install flow does **not** invoke `gh attestation verify`; the D4 attestation is not checked at the point of distribution to the end user. The D7 backstop monitor is therefore the **sole automated verification path**"; D4: "Verification compares against the attestation, never against editable Release-notes text" — but only the monitor does this comparison; SC-02 mitigation entry: "attestation matches — CI signed the malicious tree."

**Impact:** Stakeholders may believe attestation provides a chain-of-trust from CI to CoWork users. It does not. The actual chain is: CI builds → CI attests → D7 monitor verifies (every ≤6h) → GitHub issue opened on mismatch → human responds. Users at installation time have no protection beyond branch protection (D2). If D2 is bypassed (org-owner residual, credential theft), users install unverified content.

**Dimension:** Evidence Quality

**Response Required:** The design should accurately state: "The attestation resolves the SC-04 architectural flaw (non-independent reference value) but does not provide user-facing installation verification. Protection against the YELLOW threat cluster depends on D2 (branch protection) and D7 (monitor), not on user-facing attestation." The claim "resolves the 5-strategy Critical" should be qualified to "resolves the shared-key architectural flaw; user-facing protection remains bounded by D2+D7."

**Acceptance Criteria:** Threat-by-threat table showing which YELLOW threats are protected by attestation vs. other controls, with honest accounting of which threats reach users unverified if D2 and D7 both fail.

**Owner:** ADR → ps-architect; STRIDE/security → eng-architect

---

### DA-003-20260629: D7 ≤6h Detection Window Is Materially Understated [MAJOR]

**Claim Challenged:**
ADR-003 D7 states: "Detection SLA. Bounded by the poll cadence (≤6h) rather than near-real-time event delivery." The meta-monitor heartbeat (25h) is described as detecting monitor outages. The design presents "≤6h" as the attack exposure window for the residual credential-theft and admin-suppression paths.

**Counter-Argument:**
The "≤6h" detection SLA is a best-case maximum for the monitor trigger, not the actual attack exposure window. The full chain is:

**(a) GitHub Actions scheduler imprecision.** GitHub's `schedule` trigger is well-documented as imprecise under load, with delays of 15-60+ minutes during peak periods. The ADR does not acknowledge this, presenting "≤6h" as though the scheduler reliably fires at exactly 6-hour intervals. In practice, "≤6h" is aspirational; the scheduler SLA is "at some point after 6 hours."

**(b) Monitor execution time.** The D7 job reads the dedicated repo tip SHA, invokes `gh attestation verify`, and evaluates. This takes minutes. During this time the tampered artifact may be installed by users.

**(c) Issue-open to human-response latency.** D7 "opens a GitHub issue" on mismatch. The design does not specify: who is notified, what the response SLA is, or that any human is on-call. For a small-org project with a single maintainer, "GitHub issue" may have a response latency of hours to days.

**(d) No mandatory auto-revert.** Auto-revert is described in ADR-003 as "available and now easier" and mentioned in the STRIDE model under "RESPOND (RS)." But it is NOT mandated by any current REQ with an acceptance criterion. The design says "recommended as the RESPOND control" but REQ-037 covers push-failure detection, not post-tamper auto-revert. Without a mandatory auto-revert requirement, the recovery from a D7-detected tamper requires a human to manually trigger `workflow_dispatch`.

**(e) Meta-monitor adds 25h on top.** If the D7 monitor itself fails silently (SC-05), the meta-monitor alerts "if no successful run in 25h." So monitor failure → meta-monitor alert → human response → restore monitor → monitor fires → detects tamper → human responds → regenerates. The theoretical worst-case exposure is approximately 25h + human response + manual regeneration.

The combination of (a)-(e) means the actual attack window for executable hooks distributed org-wide could substantially exceed the design's "≤6h" framing. For a C4 artifact that ships code executing on every user's session start, this framing matters.

**Evidence:** ADR-003 D7: "bounded by the poll cadence (≤6h)"; REQ-044: "meta-monitor alert if no success in 25h"; ADR-003 Consequences §Negative: absent of any concrete auto-revert REQ with ACs; SC-05 mitigation: "alert if no success in 25h."

**Impact:** Stakeholders making a C4 risk acceptance decision based on "≤6h detection window" are not accounting for the realistic attack window, which could be 24-48h or more in degraded conditions. For an executable-hook artifact distributed org-wide, a 24h exposure window at C=5 impact is a materially different risk than a 6h window.

**Dimension:** Completeness

**Response Required:** (i) Acknowledge GitHub scheduler imprecision explicitly in the SLA claim (reframe to "typically within 6h; scheduler may add 15-60m; response SLA depends on human availability"). (ii) Add a mandatory auto-revert REQ with an acceptance criterion: on D7 mismatch, the monitor SHALL automatically trigger `workflow_dispatch` to regenerate (not open an issue and wait). (iii) Define a human-response SLA for GitHub issues opened by the monitor.

**Acceptance Criteria:** A REQ (auto-revert) exists with an AC that demonstrates: D7 detects a mismatch → `workflow_dispatch` fires automatically (not just "opens an issue") → skeleton is regenerated within N minutes. Until then, "≤6h" should not be stated as the detection SLA without caveats.

**Owner:** Requirements → nse-requirements; STRIDE/security → eng-architect

---

### DA-004-20260629: App Private Key Protection Controls Underspecified — "Single Long-Lived Secret" Lacks Testable Requirements [MAJOR]

**Claim Challenged:**
ADR-003 D3 (and RTB-4) identifies the App private key as "the project's single long-lived secret." The mitigation states: "source-repo secrets only; minimal access; rotation policy; short-lived minted tokens." REQ-041 mandates use of App/deploy key; REQ-045 and REQ-048 are newly proposed to govern the key.

**Counter-Argument:**
The design correctly identifies that the App private key is the highest-consequence secret in the architecture (theft → durable forgery of the artifact every org user installs). But the protection controls proposed are underspecified at the level required for a C4 deliverable:

**(a) REQ-045 and REQ-048 are proposed without acceptance criteria.** REQ-045 mandates storing the key as "environment-level secrets in a GitHub Actions Environment (`skeleton-push`) whose `deployment_branch_policy` restricts activation to protected `main` / `v*`." REQ-048 mandates rotation "at minimum every 12 months or immediately on personnel change." Both appear in the "Phase-2 RE-ADVERSARY remediation deltas" section — they are newly proposed requirements with no AC defined. Without an AC, there is no testable definition of "key stored correctly" or "rotation occurred within policy."

**(b) The deploy-key alternative has WEAKER controls specified.** ADR-003 presents GitHub App and deploy key as co-equal options. But the deploy key is a long-lived SSH key with no minting/expiry mechanism. REQ-048 says "App private key (and any deploy key) SHALL be rotated at minimum every 12 months." For a long-lived SSH key that grants write to the dedicated repo's default branch, a 12-month rotation cycle means the key could be stolen and used for up to 12 months before rotation detects the exposure. The design does not propose any detection of unauthorized deploy-key usage within a rotation interval.

**(c) D7 detection of credential-theft-induced tampering depends on D7 working.** CI-01/CR-03 (credential theft) is YELLOW (2×5=10). The design's compensating control for post-theft push is D7 (detect ≤6h). But if credential theft enables DIRECT push to the dedicated repo (bypassing CI and therefore bypassing attestation), D7 detects via tip-SHA mismatch against the attestation — but only if the attacker doesn't also forge the attestation, which they can't via Sigstore but can via the App identity if the App is also used for attestation. The design's per-job permissions isolation (separate attestation job vs. push job) partially addresses this, but the design does not specify whether the App installation is scoped to ONLY the dedicated repo or also to the source repo's attestation-publishing API surface.

**Evidence:** ADR-003 RTB-4: "App private key or deploy key is the project's single long-lived secret; theft enables durable forgery until D7 detects"; REQ-045, REQ-048: both "proposed" in "Phase-2 RE-ADVERSARY remediation deltas" section; D3: App token "preferred" and deploy key "alternative" presented as equivalent; no acceptance criterion for either REQ.

**Impact:** A C4 architectural claim that the new long-lived secret is "well-governed" is not substantiatable without concrete ACs. The design introduces a new YELLOW-level threat (CR-03) and proposes mitigation requirements without ACs — which means at AG-04 approval, the governance of the single most dangerous new asset is not yet testable.

**Dimension:** Actionability

**Response Required:** (i) Define ACs for REQ-045 (demonstrate that a `workflow_dispatch` invoked from a non-protected branch is rejected before credential access). (ii) Define ACs for REQ-048 (demonstrate rotation occurred within policy; provide a rotation runbook with step-by-step instructions). (iii) Specify whether App installation is scoped to `geekatron/jerry-cowork` only or also permits API access to source-repo secrets — if the latter, this creates a wider blast radius than claimed.

**Acceptance Criteria:** REQ-045 and REQ-048 each have a defined AC that can be tested by a maintainer within 30 minutes, without access to undocumented internal systems.

**Owner:** Requirements → nse-requirements; STRIDE/security → eng-architect

---

### DA-005-20260629: SC-06 Trusted-Maintainer Compensating Control Is Purely Procedural, Inadequate for Small-Org Scale, and Added Without ACs [MAJOR]

**Claim Challenged:**
ADR-003 RTB-2 identifies SC-06 (trusted-maintainer rogue build) and specifies the compensating control: "required peer review on `main` — a branch-protection ruleset requiring at least one independent approving review for every commit to `main`, enforced for all principals who also hold `v*` tag-create rights." REQ-051 mirrors this. ADR-003 states RTB-2 "Residual: collusion of two maintainers, or a compromised reviewer, is out of scope of automated control."

**Counter-Argument:**
SC-06 is the YELLOW threat (2×4=8) with the weakest compensating control in the entire threat register. It is the only YELLOW-level threat in the STRIDE model whose sole compensating control is procedural (no technical enforcement). Every other YELLOW threat has at least one technical control (ruleset, attestation, secret scope, SHA-pinning). SC-06's control is "peer review on `main`" enforced by a branch-protection ruleset — which itself is a configuration that a `main`-branch admin can modify.

**(a) "Independent reviewer" at small-org scale may mean one person.** The PROJ-031 design artifacts indicate a single-person or very small team org (`geekatron`). If the org has 2 principals with both `main`-write and `v*` tag-create rights, "at least one independent approving review" means the single other person who already shares maximal trust. This is not "independent" in the security sense — it is mutual trust with a single failure point.

**(b) The control is self-referentially circular at the trust boundary.** The `main`-branch protection ruleset that enforces peer review is itself modifiable by an org-owner (the same class of principal that RTB-1 says can suppress the dedicated-repo ruleset). So if an org-owner is the threat actor, they can (i) suppress `main` peer review, (ii) push a malicious commit, (iii) re-enable peer review. The compensating control for RTB-2 is bypassable by the same class of threat actor as RTB-1.

**(c) SC-06 was added late (iteration-004 remediation) as a "Methodological Rigor gap closed."** ADR-003 explicitly states: "This *threat* was absent from the Phase-2 STRIDE model" and was documented "pending the Phase-3 STRIDE update." REQ-051 is in the "Phase-2 RE-ADVERSARY remediation deltas" section with no acceptance criterion. The design treats SC-06 as mitigated with REQ-051, but REQ-051 has no AC, no verification method, and no definition of what "enforced for all principals who also hold `v*` tag-create rights" means in practice (how is this list maintained? how is it verified?).

**(d) The STRIDE model's own SC-06 label has an identifier collision.** ADR-003 notes: "the Phase-2 STRIDE model already uses the label `SC-06` for a *different* threat (two-repo drift / staleness, banded GREEN). The trusted-maintainer rogue build is tracked as `SC-06` in **this ADR**; the Phase-3 STRIDE update MUST reconcile the collision." This means the STRIDE model and the ADR are currently inconsistent on what SC-06 means — a traceability failure in a C4 deliverable.

**Evidence:** ADR-003 RTB-2: "Residual: collusion of two maintainers, or a compromised reviewer, is out of scope of automated control"; "This *threat* was absent from the Phase-2 STRIDE model"; STRIDE threat register: SC-06 = "two-repo drift" (GREEN, different threat); ADR-003 Requirement Deltas: REQ-051 in "Phase-2 RE-ADVERSARY remediation deltas" with no AC.

**Impact:** SC-06 represents an attacker who has already passed all technical controls (D2, D4, D5) and whose malicious build is faithfully attested. The design's compensating control (peer review) is bypassable by the threat actor class (org-owner), inadequate at small-org scale, unverifiable without ACs, and tracking-inconsistent between artifacts. For a C4 deliverable affecting executable hooks distributed org-wide, the sole procedural YELLOW-level control being inadequately specified is a meaningful gap.

**Dimension:** Internal Consistency

**Response Required:** (i) REQ-051 must define an acceptance criterion: how is the list of "principals holding `v*` tag-create rights" maintained and verified? Who audits it? (ii) The SC-06 identifier collision between STRIDE model and ADR-003 must be resolved in the Phase-3 STRIDE update before AG-04 approval, so traceability is unambiguous. (iii) The design should honestly state whether "required peer review" is achievable as an independent control at current org scale (e.g., does the org have at least 2 principals who can independently review?).

**Acceptance Criteria:** SC-06 has a consistent identifier across all artifacts; REQ-051 has a testable AC; the "independent reviewer" pool is documented and verified to contain at least 2 principals who could satisfy the separation-of-duties requirement.

**Owner:** STRIDE/security → eng-architect; requirements → nse-requirements; ADR → ps-architect (identifier collision)

---

### DA-006-20260629: REQ-047 Org-Registration Monitor Assumes Unconfirmed API Capabilities [MAJOR]

**Claim Challenged:**
ADR-003 RTB-3 specifies the compensating control for org-registration single-actor attack: "an automated monitor (REQ-047) queries the org's registered CoWork source ≤ daily and alerts on any drift from the canonical `geekatron/jerry-cowork`, plus an org audit-log webhook on marketplace-settings changes." REQ-047 states: "An automated monitor SHALL verify (≤24h) that the org's registered CoWork source matches canonical `geekatron/jerry-cowork`, with an org audit-log webhook on marketplace-settings change."

**Counter-Argument:**
REQ-047 implicitly requires two platform capabilities whose existence has not been established:

**(a) A programmatic API to query the org's currently registered CoWork marketplace source.** ADR-003 itself says "CoWork's org marketplace registration is a single-actor server-side setting." The design cites no GitHub API endpoint or Anthropic API that exposes the registered marketplace source to programmatic query. The org marketplace registration is described as performed "server-side" via "Anthropic server-side API" — but whether this setting is queryable via a GitHub org API (e.g., `GET /orgs/{org}/settings/...`) or any other programmatic means is not confirmed. If no such API exists, REQ-047's "automated monitor" must rely on manual verification, degrading from "automated" to "process control" — the same characterization the design applies to the two-admin approval process it describes as inadequate.

**(b) A GitHub org audit-log webhook event type for "marketplace-settings change."** REQ-047 proposes "an org audit-log webhook on marketplace-settings change." GitHub's audit log webhook does support various event types, but the specific event type for CoWork marketplace registration changes is not confirmed to exist. GitHub's audit log covers organization settings changes generically, but CoWork-specific settings (which are Anthropic-side integrations) may not generate GitHub audit log events at all — they may be recorded only in Anthropic's own audit infrastructure.

**(c) RTB-3 explicitly labels this as detect-and-respond.** The design says: "a single compromised org-owner can re-register to a rogue/typosquat repo; the two-admin rule does not stop the action, and harm occurs in the detection window before REQ-047 alerts." With a 24-hour SLA and org-wide installation on next refresh, this means all org users could be running malicious hooks for up to 24 hours before REQ-047 detects the registration change. If the monitoring capability is degraded (because the API doesn't exist), this becomes unbounded detection.

The design's reference to this area as "OQ-047's undocumented monitoring endpoint" in orchestration context is structurally apt: the monitoring depends on an endpoint that has not been documented as existing.

**Evidence:** ADR-003 RTB-3: "CoWork's org marketplace registration is a single-actor server-side setting"; "technical-detection compensator: automated monitor (REQ-047) queries the org's registered CoWork source"; no API endpoint cited; REQ-047: "org audit-log webhook on marketplace-settings change" with no cited GitHub API webhook event type confirming this exists for CoWork settings.

**Impact:** If neither the programmatic query API nor the marketplace-settings webhook event exists, REQ-047 degrades to a manual "check periodically" process with a 24-hour best-case detection window that cannot be automated. The design then has no automated detection for OR-01/02 (YELLOW 2×5=10), the org-registration attacks. The "24h" SLA in REQ-047 would become aspirational documentation rather than an enforced control.

**Dimension:** Evidence Quality

**Response Required:** Before AG-04 approval, confirm: (i) the specific API endpoint or mechanism by which an automated monitor can query the org's currently registered CoWork source; (ii) the specific GitHub audit-log webhook event type (or Anthropic-side equivalent) triggered by marketplace-settings changes; (iii) if neither exists, redesign REQ-047 as a documented manual check with explicit SLA and runbook, not as an "automated monitor."

**Acceptance Criteria:** A proof-of-concept script demonstrates that the registered CoWork source can be queried programmatically and that a registration change fires an observable webhook/event within the stated detection window.

**Owner:** STRIDE/security → eng-architect; requirements → nse-requirements

---

### DA-007-20260629: Attest-Before-Push Job Sequencing Is a Workflow Configuration Invariant, Not a Platform Safety Guarantee [MINOR]

**Claim Challenged:**
ADR-003 D4 states: "If the attestation step fails or exits non-zero, the push SHALL NOT execute" and "Attestation ordering — no live-unattested window (C-7 / item 6b)." REQ-042 mirrors: "if attestation fails, the push SHALL NOT execute (no live-unattested artifact)."

**Counter-Argument:**
This invariant is enforced by GitHub Actions job dependencies (`needs:` + `if: needs.attest.result == 'success'`), which are workflow-file configuration, not a platform-level safety guarantee. A workflow edit that removes the `needs:` dependency, changes the `if:` condition, or adds a separate push step without the attestation prerequisite would silently break this invariant without violating any platform constraint. There is no dedicated CI test for "attest-fails → push-aborts" in the current requirements. REQ-022 covers the faithful-derivative gate test; there is no equivalent acceptance criterion for attestation-failure behavior.

**Evidence:** ADR-003 D4: attestation ordering described in prose; no REQ with AC for "push aborts on attestation failure"; REQ-017 (SHA-pin Actions) provides defense-in-depth but does not test the job-dependency invariant.

**Dimension:** Traceability

**Response Required:** Add an acceptance criterion to REQ-042 explicitly testing the attestation-failure → push-abort behavior: inject a deliberate attestation failure in a test run and confirm the push job does not execute and the dedicated branch is not updated. This is a Minor finding because SHA-pinning and code review provide reasonable defense-in-depth, but the explicit test would make the invariant verifiable.

**Owner:** Requirements → nse-requirements

---

### DA-008-20260629: D5 Provenance Assertion Has Circular Dependency on `main` Integrity via Procedural REQ-051 [MINOR]

**Claim Challenged:**
ADR-003 D5 claims the tag-on-main provenance assertion (`git merge-base --is-ancestor`) "closes the rogue-tag path" as the "top residual." Combined with `v*` tag protection, this is framed as addressing SC-02.

**Counter-Argument:**
D5 closes the rogue-tag path for non-maintainer actors. But D5 explicitly acknowledges it "does NOT cover the trusted-maintainer path." The compensating control for the trusted-maintainer path is REQ-051 (peer review on `main`). This creates a circular defense structure:

- D5's value against trusted-maintainer rogue build: none (ADR-003 explicitly)
- REQ-051's coverage of trusted-maintainer rogue build: procedural only (DA-005 above)
- Therefore D5 + REQ-051 together cover non-maintainer rogue-tag (via D5) + trusted-maintainer rogue-tag (via REQ-051 procedural)

The circularity: REQ-051 is the sole technical backstop for D5's gap, and REQ-051 is itself bypassable by an org-owner. So D5 + REQ-051 fails against an org-owner threat actor via the same path as RTB-1. For a C4 design, the claim that "top residual (SC-02) addressed by D5" should note explicitly that D5's coverage is limited to the non-maintainer attack surface and that the full SC-02 threat is only bounded when REQ-051 holds.

**Evidence:** ADR-003 D5: "D5 does NOT cover the trusted-maintainer path (SC-06)"; RTB-2: "D2 is blind, D4 matches, D5 passes" for trusted-maintainer path; REQ-051: purely procedural, no ACs.

**Dimension:** Methodological Rigor

**Response Required:** Qualify the D5 coverage claim: "D5 closes the rogue-tag path for non-maintainer actors. For principals with both `main`-write and `v*` tag-create rights, D5 provides no additional protection beyond REQ-051 (peer review on `main`)."

**Owner:** ADR → ps-architect

---

## Recommendations

### P0 (Critical — MUST resolve before acceptance)

| ID | Action | Acceptance Criteria | Owner |
|----|--------|---------------------|-------|
| DA-001 | Empirically validate D2 bypass-actor configuration on `geekatron/jerry-cowork` before AG-04, or reframe prevention claim to "prevention-pending-empirical-validation" | Live test showing non-bypass human denied; CI identity allowed; repo-admin cannot modify ruleset | ps-architect |

### P1 (Major — SHOULD resolve; require justification if not)

| ID | Action | Acceptance Criteria | Owner |
|----|--------|---------------------|-------|
| DA-002 | Qualify "resolves the 5-strategy Critical" to "resolves the shared-key architectural flaw; YELLOW threats and user-facing install gap remain" | Threat-by-threat table showing which YELLOW threats attestation covers vs. does not; RTB-5 promoted from disclosure to explicit limitation on the SC-04 resolution claim | ps-architect; eng-architect |
| DA-003 | Add mandatory auto-revert REQ with AC; reframe "≤6h" SLA to include scheduler imprecision and human-response latency caveats | REQ exists: D7 mismatch → automatic `workflow_dispatch` fires → skeleton regenerated; AC tested on a live mismatch event | nse-requirements; eng-architect |
| DA-004 | Add ACs for REQ-045 and REQ-048; specify whether App installation scope includes source-repo attestation API | REQ-045 AC: demonstrate non-protected-branch dispatch rejected before credential access; REQ-048 AC: rotation runbook with step-by-step instructions, completable in <30 min | nse-requirements; eng-architect |
| DA-005 | Resolve SC-06 identifier collision between STRIDE model and ADR-003 before AG-04; add AC to REQ-051 including "independent reviewer pool" definition and maintenance process | SC-06 has one definition across all artifacts; REQ-051 AC includes list of qualifying principals and audit mechanism | ps-architect; eng-architect; nse-requirements |
| DA-006 | Confirm programmatic API for org's registered CoWork source and audit-log webhook event type for marketplace-settings changes; if unconfirmed, redesign REQ-047 as documented manual process | Proof-of-concept script demonstrating programmatic query of registered source; OR explicit redesign of REQ-047 as manual check with explicit SLA | eng-architect; nse-requirements |

### P2 (Minor — MAY resolve; acknowledgment sufficient)

| ID | Action | Acceptance Criteria | Owner |
|----|--------|---------------------|-------|
| DA-007 | Add AC to REQ-042 for attestation-failure → push-abort behavior | Test run demonstrating push job does not execute when attestation job fails | nse-requirements |
| DA-008 | Qualify D5 coverage claim to state it applies only to non-maintainer actors | ADR-003 D5 text updated to: "closes rogue-tag for non-maintainer actors; trusted-maintainer path remains bounded by REQ-051 alone" | ps-architect |

---

## Scoring Impact

Mapping Devil's Advocate findings to S-014 scoring dimensions (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10).

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | **Negative** | DA-003: D7 protection window materially understated; DA-006: org-registration monitor coverage incomplete if API unconfirmed |
| Internal Consistency | 0.20 | **Negative** | DA-005: SC-06 identifier collision between STRIDE model and ADR-003; DA-001: "prevention" claim contradicted by RTB-1 org-owner bypass in same document |
| Methodological Rigor | 0.20 | **Negative** | DA-001: prevention claim rests on unempirical feature validation; DA-005: sole YELLOW threat with purely procedural control, added late, no ACs; DA-008: D5 coverage claim overstated for trusted-maintainer path |
| Evidence Quality | 0.15 | **Negative** | DA-002: attestation "resolves SC-04" overstated — YELLOW threats bypass attestation; DA-006: no cited API for REQ-047 monitoring capability |
| Actionability | 0.15 | **Negative** | DA-004: REQ-045 and REQ-048 proposed without ACs; DA-003: no mandatory auto-revert REQ; DA-007: no test for attest-fail → push-abort invariant |
| Traceability | 0.10 | **Negative** | DA-005: SC-06 identifier collision breaks cross-artifact traceability; DA-007: attest-before-push invariant not traceable to a testable REQ AC |

**Overall Assessment:** 1 Critical, 5 Major, 2 Minor findings. The design's core architectural moves (dedicated-repo isolation, attestation anchor) are directionally correct and represent genuine improvements over the Phase-1 posture. However, the design consistently overclaims the strength of its controls — "prevention" for an unvalidated configuration, "resolves" for a threat that remains open for users, "≤6h window" for a materially larger exposure — while underspceifying the requirements that would close these gaps (REQ-045, REQ-048, REQ-051, REQ-047 all lack ACs). At C4 quality target (≥0.95), these gaps require targeted revision before AG-04 approval. **REVISE — address all P0 and P1 findings.**

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 1
- **Major:** 5
- **Minor:** 2
- **Protocol Steps Completed:** 5 of 5

---

*Strategy: S-002 Devil's Advocate | Template: `.context/templates/adversarial/s-002-devils-advocate.md`*
*Deliverables: ADR-001, ADR-003, phase1-requirements.md, phase2-stride-threat-model.md, phase2-attack-surface.md*
*Executed: 2026-06-29T00:00:00Z | Execution ID: 20260629*
*Constitutional compliance: P-003 (no sub-agents), P-022 (no overstated confidence), P-002 (persisted)*
