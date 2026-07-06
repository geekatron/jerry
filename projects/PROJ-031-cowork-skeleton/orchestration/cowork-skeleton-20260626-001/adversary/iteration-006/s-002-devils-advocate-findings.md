# Strategy Execution Report: S-002 Devil's Advocate

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, template, inputs, timestamp |
| [H-16 Compliance](#h-16-compliance) | Steelman pre-check disposition |
| [Summary](#summary) | Findings table — all severities |
| [Detailed Findings](#detailed-findings) | Critical and Major findings with evidence and remediation |
| [Minor Findings](#minor-findings) | DA-007 improvement opportunity |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized actions |
| [Scoring Impact](#scoring-impact) | Dimension-level quality impact assessment |
| [Execution Statistics](#execution-statistics) | Protocol completion and finding counts |

---

## Execution Context

- **Strategy:** S-002 (Devil's Advocate)
- **Template:** `.context/templates/adversarial/s-002-devils-advocate.md`
- **Deliverable 1:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md`
- **Deliverable 2:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-003-credential-protection-supply-chain.md`
- **Deliverable 3:** `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md`
- **Deliverable 4:** `projects/PROJ-031-cowork-skeleton/security/phase2-stride-threat-model.md`
- **Deliverable 5:** `projects/PROJ-031-cowork-skeleton/security/phase2-attack-surface.md` (historical pre-decision recon)
- **Executed:** 2026-06-28T00:00:00Z
- **Tournament:** iteration-006 — Group C (Devil's Advocate)
- **Criticality:** C4
- **Quality Gate:** >= 0.92
- **Blindness Scope:** Only the five artifacts above; no prior iteration outputs read

---

## H-16 Compliance

H-16 requires S-003 (Steelman) to precede S-002 (Devil's Advocate). This execution is Group C of the iteration-006 blind tournament, which places Group B (Steelman) before Group C (Devil's Advocate) by construction. The orchestrator's tournament ordering satisfies the spirit of H-16. The blindness constraint prohibits reading the S-003 output — the tournament structure is the H-16 enforcement mechanism, not the report file.

---

## Summary

| ID | Severity | Finding | Artifact |
|----|----------|---------|---------|
| DA-001-it6c | CRITICAL | REQ-054 / G-update: update-propagation assumption is unknowable from outside Anthropic; fallback alternative is unspecified | ADR-001 L0 / phase1-requirements.md REQ-054 |
| DA-002-it6c | MAJOR | D4 attestation (RTB-5): no install-time verification; D7 sole automated verifier with ≤6h lag; tampered content can reach users in the detection window | ADR-003 D4 / RTB-5 / D7 |
| DA-003-it6c | MAJOR | D5 / G-provenance is designed-NOT-implemented (FM-032); SC-02 rogue-tag attack (#1 residual, DREAD 7.6) remains fully open; blocks go-live | ADR-003 D5 / STRIDE SC-02 / AT-2 analysis |
| DA-004-it6c | MAJOR | D8 static markdown scanner bypassable by catalog-aware trusted-maintainer; pattern catalog readable by SC-06 threat; D8 only technical detection on this path | ADR-003 D8 / STRIDE SC-06/SC-08 / AT-1.6 |
| DA-005-it6c | MAJOR | D7 ≤6h detection SLA disproportionate to C=5 blast radius; monitor is "front line, not backstop" until G-prevention validates; auto-revert is unvalidated (G-monitor pending) | ADR-003 D7 / STRIDE Phase-1 Disposition |
| DA-006-it6c | MAJOR | D1/D2 prevention model durability rests on organizational process controls, not architecture; RTB-1 org-owner suppression is permanently detection-only; dedicated repo does not yet exist | ADR-003 D1/D2 / STRIDE DR-01/DR-02 / RTB-1 |
| DA-007-it6c | MINOR | Claim-Status Convention contains no gate-failure contingency for G-update; ALL 6 Phase-5 gates simultaneously unvalidated; circular dependencies between gates not sequenced | ADR-003 Phase-5 Gate Set |

---

## Detailed Findings

### DA-001-it6c: CRITICAL — REQ-054 Update Propagation Unknown; Fallback Has No Design

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Location** | ADR-001 §L0 "one honesty caveat for go-live"; `phase1-requirements.md` REQ-054 / OQ-048; STK-002 traceability row |
| **Strategy Step** | Step 3 — Counter-arguments: Unstated assumptions / Alternative interpretations |
| **OWNER** | requirements → nse-requirements (REQ-054 / OQ-048); ADR → ps-architect (G-update gate design) |

**Evidence:**

From `phase1-requirements.md`, line 444:
> `REQ-054  CoWork update-propagation STATED ASSUMPTION (UNVERIFIED): "automatically in sync" for existing users; OQ-048; Phase-5 G-update gate non-deferrable; STK-002 re-scoped as contingent on empirical verification`

From `phase1-requirements.md`, line 429 (STK-002 traceability header):
> `STK-002 (Auto-sync with main, no manual surgery — CONTINGENT on G-update / REQ-054 / OQ-048)`

From ADR-001 L0:
> "whether CoWork delivers those rebuilds to **already-installed** users is an **unverified CoWork behavior**"
> "we do not assert it works for existing users"

From ADR-003 Phase-5 Gate Set (G-update):
> "CoWork DELIVERS those rebuilds to already-installed users within a bounded window — OR a manual update procedure is documented and the 'automatically in sync' claim is re-scoped to apply only at install time."

**Analysis:**

The entire CI regeneration pipeline — ADR-001's Option A, the dedicated-repo model (D1), the freshness check (D7/REQ-049), the idempotency proof (REQ-003), all of it — exists to serve one goal: Jerry users get updated Jerry automatically when a new release ships. That is STK-002. That is the primary stakeholder value the project is built to deliver.

REQ-054 acknowledges that this goal is an unverified assumption about CoWork's internal behavior, outside the design team's visibility or control. If CoWork caches the plugin file tree at install time and refreshes only on explicit user action, no part of the designed system corrects this. The CI regeneration runs, the dedicated repo is updated, the attestation is produced — and zero existing users receive the update.

The design's response is G-update: "verify before go-live." But G-update's verification requirement involves observing live CoWork behavior on a running instance. This requires Anthropic's cooperation, documentation, or empirical testing on a live CoWork deployment. The design has no entry for: "what we will do if G-update is observed to fail." The only text in ADR-003 on this is the fallback condition: "OR a manual update procedure is documented and the 'automatically in sync' claim is re-scoped." This fallback converts an automated distribution channel into a manual one, defeating the project's central value proposition.

**Why it matters at C4:** The deliverable scope is "irreversible, architecture/governance/public." The skeleton repo, once org-registered with CoWork, reaches every user with one org-admin action. If the update-propagation assumption is false at the moment of org registration, the project has delivered a channel that can publish new Jerry releases but cannot deliver them to anyone already installed. Discovering this at Phase-5 (go-live authorization, after full implementation) means the entire pipeline is built and the value premise is unconfirmed. The fallback "alternate update path" has not been designed, specified, or reviewed. At C4, a load-bearing unknown of this magnitude — one that, if wrong, voids the headline stakeholder value — requires a designed alternative before the architecture can be considered complete, not after.

**Remediation:**

1. Design the G-update fallback explicitly BEFORE Phase-3 implementation begins. Two candidate alternatives: (a) versioned release branch strategy (separate branch per vX.Y.Z, user points to their last-installed version); (b) documented user-facing update command. Both must be designed sufficiently to evaluate whether the project's STK-002 promise can be kept in the G-update-fails scenario.
2. Add OQ-048 investigation as a gating activity before Phase-3 kickoff: reach out to Anthropic to clarify or test CoWork update propagation behavior. Document findings in a new decision.
3. If the empirical answer cannot be obtained before go-live, the project should formally re-scope STK-002 as "install-time sync only" before org registration, not after.

---

### DA-002-it6c: MAJOR — D4 Attestation Anchor Has No User-Side Verifier; RTB-5 is Permanent

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Location** | ADR-003 D4 / RTB-5 / D7; Phase-1 Critical Findings Disposition (#1 root cause) |
| **Strategy Step** | Step 3 — Counter-arguments: Unaddressed risks / Alternative interpretations |
| **OWNER** | ADR → ps-architect (RTB-5 treatment); STRIDE/security → eng-architect (D7 SLA adequacy) |

**Evidence:**

From ADR-003 RTB-5:
> "CoWork's `claude plugin marketplace add` flow does **not** invoke `gh attestation verify`. The D7 integrity monitor is the **sole automated verifier**."

From ADR-003 D4, "Verification reachability — disclosed residual (C-3)":
> The attestation is CI-only-writable and publicly verifiable, but verification is not invoked at install time.

From ADR-003 D7:
> "Detection SLA. Bounded by the poll cadence (≤ 6 h) rather than near-real-time event delivery."

From `phase2-stride-threat-model.md`, Phase-1 Critical Disposition Root Cause #1:
> "ADDRESSED-BY-DESIGN (G-prevention + G-monitor pending)" — integrity-anchor collapse is addressed by the attestation moving to an immutable, CI-only-writable surface.

**Analysis:**

The Devil's Advocate challenge: "publicly verifiable" means nothing if no party in the delivery chain verifies. The attestation architecture creates a chain: Source → CI → Attestation (CI-only-writable) → Dedicated Repo → CoWork → User workstation. The attestation anchors steps 1→3. Steps 3→5 are unanchored by any verification: CoWork installs what is on the dedicated repo default branch without inspecting the attestation. A user who installs the skeleton receives files whose only attestation consumer is the D7 backstop monitor, running post-publication with a ≤6h lag.

The practical implication: in the window between a tamper event (or a rogue-tag CI build — see DA-003) and D7 detection, CoWork users are installing content that CI-produced attestation cannot catch (because the rogue-tag path produces a valid attestation for a malicious tree) or that the user cannot independently verify (because CoWork's install flow doesn't invoke `gh attestation verify`). The attestation protects the developer's ability to DETECT tampering after the fact. It does not protect users from receiving tampered content during the detection window.

The design frames this correctly as RTB-5 — a platform limitation outside the team's control. The DA position is: the previous Critical (#1 root cause, Phase-1) was "integrity-anchor collapse." The Phase-2 disposition says it is "ADDRESSED-BY-DESIGN." But if the addressed integrity anchor provides no protection to users at the delivery step, the addressing is incomplete — it shifted the attack surface from "forge the release notes" to "exploit the ≤6h detection window before the monitor fires." The attack surface is smaller, but the protection gap for users in the delivery window is identical.

**Why it matters at C4:** ADR-003 explicitly states the artifact "executes on every user's session start" and "one org registration reaches every user." With C=5 blast radius and a ≤6h exposure window per delivery event, the gap between attestation production and user-side verification is the primary exposure interval for every release. Auto-revert (D7 coupled action) cannot un-install hooks already executing on user workstations during the tamper window.

**Remediation:**

1. RTB-5 treatment requires more than disclosure. Consider specifying a user-facing install-time verification step in the CoWork plugin README and adoption runbook: `gh attestation verify --repo geekatron/jerry <installed-file>`. Even if CoWork's install flow doesn't verify, the adoption runbook can require or recommend user verification.
2. Evaluate whether the D7 ≤6h poll cadence can be reduced for the post-publish window (e.g., a triggered ≤30-minute poll in the source CI workflow after successful publication) for the highest-risk interval.
3. Document in ADR-003 that RTB-5 is a platform limitation specific to CoWork's current plugin install flow — and that, if CoWork adds verification in a future release, D7 becomes defense-in-depth rather than the sole verifier.

---

### DA-003-it6c: MAJOR — D5/G-Provenance Designed-NOT-Implemented; SC-02 (#1 Residual, DREAD 7.6) Fully Open

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Location** | ADR-003 D5 / FM-032; `phase2-stride-threat-model.md` SC-02 / AT-2 analysis / Phase-1 disposition |
| **Strategy Step** | Step 3 — Counter-arguments: Contradicting evidence / Unaddressed risks |
| **OWNER** | STRIDE/security → eng-architect (provenance assertion implementation); ADR → ps-architect (D5 go-live gate) |

**Evidence:**

From ADR-003 D5:
> "Tag-on-main provenance assertion: `git merge-base --is-ancestor "${TAG}^{commit}" origin/main` plus `v*` tag-protection — **Designed — operational validation pending [G-provenance]; NOT YET IMPLEMENTED (FM-032)** — blocks go-live."

From `phase2-stride-threat-model.md`, AT-2 analysis (lines 362):
> "**Provenance (D5) and content-safety (D8) are therefore the two load-bearing residual controls — both designed, validation pending.**"

From STRIDE Phase-1 Critical Findings Disposition, Root Cause #2:
> "SC-02 (CI-triggered rogue tag) — **STILL-NEEDED** — #1 residual"

From AT-1 DREAD table:
> "AT-1.2 Rogue tag (SC-02) — DREAD mean **7.6** — CI is the pusher → branch protection blind; needs provenance (D5 designed-NOT-impl)"

From ADR-003 (SC-02 in STRIDE mirror):
> "D5: Tag-on-main provenance assertion. Status: **Designed — operational validation pending [G-provenance pending; FM-032]**; blocks go-live."

**Analysis:**

The design identifies SC-02 (rogue v* tag CI self-certification) as its own #1 residual threat, giving it DREAD mean 7.6 — the highest score in the AT-1 table. The attack is: a trusted maintainer (or compromised credential) creates a rogue `v*` tag on a non-main commit; CI triggers on the tag; CI faithfully builds, passes faithful-derivative checks (the content diff is against the malicious tag, which matches itself), and ATTESTS the malicious tree; the dedicated repo receives a properly-attested skeleton containing the attacker's payload; D7 monitor sees a valid attestation and a fresh deployment and passes. Every integrity control in the pipeline is blind because CI is the legitimate pusher and it certified the tree.

D5 (the tag-on-main provenance assertion) is the sole mitigation for this attack path. D5 is explicitly "designed-NOT-implemented" with an open FMEA issue (FM-032) and a Phase-5 go-live gate (G-provenance). No implementation work has begun.

The Devil's Advocate's challenge: this means the system currently has NO DEFENSE against its own self-identified #1 residual attack vector. The design is honest about this — "blocks go-live" — but at C4, "we know our #1 unmitigated attack but haven't started the mitigation" is not a satisfactory design posture for a system proposing to be accepted as architecture-of-record.

**Why it matters at C4:** A rogue-tag attack at DREAD 7.6 against a system delivering executable hooks to every org user (C=5 blast radius) is a high-impact, medium-reproducibility attack with a fully open execution path. D8 (content-safety scan) is listed as the only other technical detection on the SC-06→SC-08 path, but SC-02 bypasses D8 if the rogue tag contains a payload specifically designed against the known D8 pattern catalog (see DA-004). The SC-02 path remains the system's principal unaddressed vulnerability.

**Remediation:**

1. D5 implementation should be gated as a prerequisite for Phase-3 acceptance (it is already a go-live blocker; making it a Phase-3 prerequisite accelerates closure).
2. Add a FMEA FM-032 remediation timeline and owner to the STRIDE document. The current entry records the issue but not the expected closure sprint/phase.
3. Note in ADR-003 D5 that `git merge-base --is-ancestor` has a known attack bypass: if the source repo's v* tag protection (REQ-039) is misconfigured and a rogue tag is created on main itself (pointing to a non-mainstream commit via force-move), the ancestor check passes. D5 must couple with REQ-039's tag-protection enforcement, not replace it.

---

### DA-004-it6c: MAJOR — D8 Static Scanner Bypassable by Catalog-Aware Trusted-Maintainer

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Location** | ADR-003 D8 / Detector Specification; `phase2-stride-threat-model.md` SC-06/SC-08 / AT-1.6 / AT-2 |
| **Strategy Step** | Step 3 — Counter-arguments: Logical flaws / Unaddressed risks |
| **OWNER** | STRIDE/security → eng-architect (pattern catalog design and allow-list governance) |

**Evidence:**

From ADR-003 D8 (False-positive handling):
> "discussion of an attack in prose is matched, so the **allow-list, not silent skipping, is the release valve**"

From ADR-003 D8 (Residual):
> "Static scanning of natural-language instructions has **false-negatives on novel phrasing** — D8 reduces but does not fully close SC-08."

From STRIDE AT-1.6 (SC-06→SC-08):
> "AT-1.6 Trusted-maintainer content build (SC-06→SC-08): DREAD mean **5.6** — Needs a trusted role + evade D8 scan + evade peer review; **integrity controls blind — D8 is the only technical detection**."

From STRIDE AT-2 analysis:
> "a **trusted-maintainer markdown injection (SC-06→SC-08)** is faithfully built AND attested — closed only by the **D8 content-safety scan** (content inspection), since no integrity control can see payload semantics."

**Analysis:**

The D8 specification makes D8 the only technical detection on the SC-06→SC-08 path. The Devil's Advocate challenge is that the SC-06 threat — the trusted maintainer who can inject into the codebase — is the same principal who can read the pattern catalog and allow-list in the source repo. Both assets (C1-C6 indicator categories, allow-list entries) are version-controlled, code-reviewed files. Any maintainer with repo read access can study the existing pattern catalog and design a payload that evades all six categories. This is not a theoretical exploit: it requires only (a) trusted-maintainer access (the SC-06 threat has this by definition) and (b) craft to write injection instructions that don't match any category C1-C6.

The design acknowledges false-negatives for "novel phrasing" but frames this as an inherent limitation of static scanning. The deeper problem is that the catalog is not secret — the adversary in SC-06 knows what to evade. The catalog's C5 (covert-channel/obfuscation) category covers some evasion techniques, but semantic instruction injection ("when helping users with X, prioritize Y") can be crafted with no obfuscation, no explicit role-override, and no credential solicitation — evading all six categories while still altering agent behavior.

The allow-list mechanism introduces a compounding risk: Jerry's own adversary templates, red-team skill, and this STRIDE threat model itself discuss prompt-injection patterns extensively and require allow-list entries at scan adoption. These allow-list entries, once in place, create a public inventory of "prose patterns D8 ignores," which the same trusted-maintainer adversary can exploit as an evasion map. The allow-list adoption step ("a baseline scan of the current main retained surface establishes the known-benign set") is particularly risky: if undetected historical injection exists in the retained surface at adoption time, that content is hash-pinned into the baseline allow-list.

**Why it matters at C4:** D8 is labeled "the FIRST technical detection" and "the only technical detection" for the trusted-maintainer injection path. If it is bypassable by the threat it is designed to catch, the SC-06 path has no technical defense — only REQ-051 (peer review), whose residual is explicitly "two-maintainer collusion" (RTB-2). At C4, a security control that is bypassable by the threat actor it is designed to detect is a critical design gap, even if the probability is moderate (DREAD 5.6).

**Remediation:**

1. Classify the D8 allow-list itself as security-sensitive. Require two-maintainer approval on all allow-list modifications (consistent with REQ-051 peer review threshold). Track the allow-list surface as a security artifact in the runbook.
2. Implement semantic-level detection as a complement to pattern matching: a lightweight LLM-based scan of instruction files for behavioral intent, in addition to the C1-C6 regex/AST patterns. This adds a non-bypassable-by-catalog-study layer against novel phrasing.
3. Rotate the pattern catalog from a public source-code asset to a deployment-time-only asset: compile it into the CI workflow at execution time from a private secret store, preventing read access for contributors who cannot view organization secrets. This is a governance change that does not require new technology.

---

### DA-005-it6c: MAJOR — D7 Detection SLA Disproportionate to Blast Radius; Monitor is Front Line Until G-Prevention Validates

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Location** | ADR-003 D7 / REQ-035 / REQ-049 / REQ-053; `phase2-stride-threat-model.md` Phase-1 Disposition Root Cause #3 |
| **Strategy Step** | Step 3 — Counter-arguments: Unaddressed risks / Historical precedents |
| **OWNER** | ADR → ps-architect (D7 SLA decision); STRIDE/security → eng-architect (SC-03/SC-05 monitoring adequacy) |

**Evidence:**

From ADR-003 D7:
> "Detection SLA. Bounded by the poll cadence (≤ 6 h) rather than near-real-time event delivery."
> "Event-driven leg RETIRED — platform-impossible."

From STRIDE Phase-1 Critical Findings Disposition, Root Cause #3:
> "Addressed-By-Design; monitoring still load-bearing"
> "**Until G-prevention validates, the monitor is still the front line, not a backstop**."

From ADR-003 (D7 auto-revert / REQ-053):
> "an integrity/freshness failure dispatches `workflow_dispatch` re-generation of the last-good tag through the normal gated path; the monitor/automation needs **`actions: write`**"

From ADR-003:
> "the artifact executes on every user's session start" / "one org registration reaches every user at once"

From STRIDE meta-monitor (REQ-044):
> "meta-monitor watchdog — SC-05 mitigation"; heartbeat interval 25h.

**Analysis:**

The design re-rates R-007b (direct-push blast radius) to GREEN under the prevention posture (G-prevention pending). The STRIDE document itself notes: "until G-prevention validates, the monitor is still the front line, not a backstop." During the entire pre-go-live validation period — which includes G-prevention, the most infrastructure-intensive gate — the D7 monitor operates as the primary defense with a ≤6h detection SLA against executable hooks on a C=5 blast radius.

The ≤6h SLA means: if a tamper event occurs at T=0 (via any residual attack vector: rogue tag, credential theft, org-owner suppression), users may install and execute malicious hooks until T=6h. The auto-revert path requires: (1) D7 detects the failure, (2) dispatches `workflow_dispatch`, (3) the gated regeneration pipeline runs successfully through all D6 + D8 + D4 checks, (4) the corrected skeleton is force-pushed to the dedicated repo. Steps 2-4 add further latency after the 6h detection lag.

The meta-monitor's 25h heartbeat (REQ-044) means D7 itself can be down for up to 25h before alerting — creating a window where the defense is completely dark. The event-driven fast path was retired as platform-impossible, leaving the scheduled poll as the sole mechanism. For a system where "one org registration reaches every user at once" and the hooks "execute on every user's session start," the gap between detection and user exposure cannot be bounded below 6h with the current architecture.

**Why it matters at C4:** The blast radius (C=5, every org user, every session start) demands a detection SLA commensurate with impact. ≤6h was derived from reducing Phase-1's 24h worst-case — an improvement, but still potentially hundreds of sessions per user exposed before detection. The design's own note ("until G-prevention validates, the monitor is still the front line") acknowledges this is the current operational posture and not just a theoretical future concern.

**Remediation:**

1. Reduce D7 poll cadence to ≤1h for the window immediately following a new dedicated-repo deployment (e.g., a triggered delayed poll from the source CI workflow at T+30m, T+60m after publication). This narrows the maximum exposure window without requiring near-real-time infrastructure.
2. Explicitly test auto-revert end-to-end as part of G-monitor validation. Document the measured auto-revert latency (detect→recovered) as a Phase-5 gate acceptance criterion, not just the detection SLA.
3. Consider whether the 25h meta-monitor heartbeat is appropriate. A dead D7 monitor with a 25h alert lag means the front-line defense is dark for up to a day. Reduce meta-monitor window to ≤4h to ensure the primary monitor can be restored within one business shift.

---

### DA-006-it6c: MAJOR — D1/D2 Prevention Model Durability Rests on Org Process Controls, Not Architecture

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Location** | ADR-003 D1/D2 / RTB-1; `phase2-stride-threat-model.md` DR-01/DR-02; ADR-003 Negative #4 |
| **Strategy Step** | Step 3 — Counter-arguments: Unstated assumptions / Historical precedents |
| **OWNER** | ADR → ps-architect (D2 durability treatment); requirements → nse-requirements (REQ-040 / REQ-043 access review) |

**Evidence:**

From ADR-003 RTB-1:
> "Organization-owner can suppress the ruleset via the Org Settings UI — this is a **platform-level permission that cannot be restricted below that tier**. Mitigation: minimize org-owners, require 2FA/SSO, enable audit-log alerting. The residual is **detection-only**; prevention-below-org-owner is preserved."

From ADR-003 Negative #4:
> "Dependence on current GitHub features. Immutable releases, build-provenance attestations, and **ruleset bypass-actor semantics are recent (2025–2026)**."

From ADR-003 D2:
> "prevention-by-design, **empirically unvalidated [G-prevention pending]**; org-owner (not repo-admin) can suppress — detection-only residual (RTB-1)"

From requirements, REQ-040:
> "dedicated-repo org-level non-overridable ruleset; CI sole bypass; zero human write"

From requirements, REQ-043:
> "org marketplace registration admin minimization + runbook (**PROCESS control — no platform enforcement**); ≤ monthly audit"

**Analysis:**

The design claims "prevention-by-design" for direct push below the org-owner tier. This claim has two components the Devil's Advocate presses:

**Component 1 — Unverified feature semantics on a non-existent repo.** The dedicated repo `geekatron/jerry-cowork` has not been created. The bypass-actor ruleset semantics (a GitHub feature from September 2025, less than 12 months old) have not been exercised on the target configuration. G-prevention is a Phase-5 gate that will validate this — but the design declares "prevention-by-design" before that validation. This is architectural intention, not demonstrated prevention.

**Component 2 — Durability under organizational evolution.** The prevention model below org-owner tier is technically enforced by the ruleset (once validated). Above org-owner tier, the mitigation is: minimize org-owners, require 2FA/SSO, monthly access review (REQ-043 — a PROCESS control). These are the durable maintenance controls. Unlike technical controls, process controls degrade under: personnel turnover (new org-owners who are less security-aware), audit fatigue (≤monthly review, while a misconfigured org-owner grant could persist until the next review cycle), and feature change (GitHub modifying bypass-actor semantics in a future update — Negative #4). The design has no mitigation for GitHub changing bypass-actor behavior and thereby voiding the prevention claim without prior warning.

ADR-003 explicitly labels REQ-043 as "PROCESS control — no platform enforcement." The dedicated repo has no governance culture behind it (it doesn't exist), unlike `geekatron/jerry`'s established "Don't fuck with main" posture. A new repo under org-level protection is a single misconfiguration away from losing its prevention posture, with the next detection opportunity being the ≤weekly dedicated-repo metadata monitor (REQ-046).

**Why it matters at C4:** The prevention-by-design claim is the centerpiece of the D1/D2 architecture. It underpins the re-rating of R-007b to GREEN (direct-push PREVENTED) and the re-classification of DR-01 to target L=1. If the prevention model is not durable — if it degrades to detection-only as the organization evolves or as GitHub changes features — then the STRIDE model's risk register understates the residual risk.

**Remediation:**

1. Add a durability assessment to ADR-003 D2: specify what happens if GitHub modifies bypass-actor semantics in a future platform update, and what the detection mechanism would be for this (currently none).
2. Add a change-management requirement: any change to org-level security settings for `geekatron/jerry-cowork` requires an ADR update AND a re-run of G-prevention validation. This makes the prevention posture persistent, not one-time.
3. Evaluate whether a fully automated weekly ruleset-state check (not just detection of metadata drift per REQ-046) can be added to the D7 monitor, specifically verifying that the bypass-actor configuration is intact.

---

## Minor Findings

### DA-007-it6c: MINOR — Claim-Status Convention Has No Gate-Failure Contingency; Circular Gate Dependencies Unaddressed

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Location** | ADR-003 Phase-5 Validation Gate Set; ADR-003 Claim-Status Convention |
| **Strategy Step** | Step 3 — Counter-arguments: Unstated assumptions |
| **OWNER** | ADR → ps-architect (gate sequencing); requirements → nse-requirements (Phase-5 Authorization Checklist) |

**Evidence:**

From ADR-003 Phase-5 Gate Set (G-update):
> "CoWork DELIVERS those rebuilds to already-installed users within a bounded window — **OR** a manual update procedure is documented and the 'automatically in sync' claim is re-scoped"

From ADR-003 Gate Set preamble:
> "ALL six Phase-5 gates MUST AND-pass before go-live. No gate is deferrable."

**Analysis:**

The six Phase-5 gates have unacknowledged interdependencies: G-prevention must pass before the dedicated repo is trustworthy enough for G-monitor to test against. G-monitor requires the D4 attestation to be operational on the target, which requires G-prevention. G-content requires the D8 pattern catalog, which requires eng-architect delivery. These cascade dependencies are not sequenced — the gate set is listed as a flat AND-condition with no priority ordering.

More critically: if G-update fails permanently (CoWork cannot be empirically confirmed to propagate updates), the fallback condition (re-scope STK-002 + document manual procedure) fundamentally changes the project's value proposition. This outcome has no designed path forward — the "REQUIRED alternate update path" is a requirement on a thing that doesn't yet exist. The Claim-Status Convention is honest about what is pending, but it provides no guidance on what the project does if one gate cannot be passed.

**Remediation:**

1. Add an explicit gate-sequencing diagram to ADR-003: which gates are prerequisites for which others, and what the critical path is.
2. Define a circuit-breaker condition: if G-update empirical testing is not achievable by a specified date (e.g., before Phase-4 implementation completion), the project must formally choose between: (a) re-scoping STK-002 to install-time-only sync with a documented manual update flow; or (b) pausing implementation pending Anthropic engagement. Deferring this choice to Phase-5 means maximum wasted implementation effort if the answer is (b).

---

## Recommendations

### P0 — Must resolve before architecture approval

| Priority | ID | Action | OWNER |
|----------|----|--------|-------|
| P0 | DA-001-it6c | Design the G-update fallback BEFORE Phase-3 implementation. Specify what "alternate update path" means concretely. Add OQ-048 investigation as Phase-2 gating activity requiring Anthropic engagement or empirical CoWork testing. | requirements → nse-requirements |
| P0 | DA-003-it6c | Move D5 implementation (tag-on-main provenance assertion) from "Phase-5 go-live gate" to "Phase-3 implementation prerequisite." SC-02 at DREAD 7.6 with a fully open execution path is too high to carry through full implementation without closure. Add FM-032 remediation timeline to STRIDE. | STRIDE/security → eng-architect |

### P1 — Must resolve before Phase-4 integration testing

| Priority | ID | Action | OWNER |
|----------|----|--------|-------|
| P1 | DA-002-it6c | Add an explicit "RTB-5 user-facing verification" step to the adoption runbook. Evaluate whether a triggered ≤30m post-publish D7 poll is feasible. Document that RTB-5 is a platform limitation tied to CoWork's current install flow, not a permanent architectural commitment. | ADR → ps-architect |
| P1 | DA-004-it6c | Implement D8 allow-list governance controls: two-maintainer approval for all allow-list changes, security classification for the allow-list file. Evaluate semantic-detection complement to pattern matching. Evaluate private secret-store for pattern catalog to prevent catalog-aware evasion by trusted-maintainer threat. | STRIDE/security → eng-architect |
| P1 | DA-005-it6c | Add post-publish triggered D7 poll (≤1h delay after confirmed push) to reduce the maximum exposure window. Test auto-revert end-to-end latency as a G-monitor acceptance criterion. Reduce meta-monitor heartbeat window from 25h to ≤4h. | ADR → ps-architect |

### P2 — Should resolve before go-live

| Priority | ID | Action | OWNER |
|----------|----|--------|-------|
| P2 | DA-006-it6c | Add durability assessment for GitHub feature change risk (bypass-actor semantics) to ADR-003 D2. Add change-management requirement: any org-security-settings change requires ADR update + G-prevention re-validation. Evaluate automated weekly ruleset-state check. | ADR → ps-architect |
| P2 | DA-007-it6c | Add Phase-5 gate sequencing diagram with critical path and prerequisites. Define a circuit-breaker condition for G-update empirical failure with a date-gated decision point. | ADR → ps-architect |

---

## Scoring Impact

| Dimension | Weight | Pre-DA Assessment | Impact of Findings | Notes |
|-----------|--------|-------------------|--------------------|-------|
| Completeness | 0.20 | High | Negative | DA-001 reveals an undesigned alternative; DA-003 reveals an unimplemented critical control |
| Internal Consistency | 0.20 | High | Negative | DA-002 reveals the attestation-resolves-Critical claim is incomplete without user-side verification; DA-003 reveals the #1 residual is self-identified but unaddressed |
| Methodological Rigor | 0.20 | High | Moderate negative | DA-004 and DA-005 challenge two of the three designed residual controls (D8 and D7); design methodology is rigorous but controls have documented gaps |
| Evidence Quality | 0.15 | High | Low negative | Findings based on design's own disclosures (RTB-5, G-update, FM-032, DREAD tables) — not new external evidence |
| Actionability | 0.15 | High | Neutral | P0/P1/P2 recommendations are specific; design already names gates and owners |
| Traceability | 0.10 | High | Neutral | All findings traced to specific ADR-003 decision codes, STRIDE threat IDs, and requirements IDs |

**Overall Devil's Advocate impact:** The most significant dimension hit is Completeness (DA-001: no designed fallback) and Internal Consistency (DA-002/DA-003: attestation and rogue-tag claims are incomplete). The design's internal honesty (Claim-Status Convention, RTB-1/RTB-5 disclosures) mitigates Evidence Quality impact because all challenges are grounded in the design's own documented limitations. Methodological Rigor is strong but weakened by the D5 implementation gap and the D8 catalog-awareness vulnerability.

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 1 (DA-001-it6c)
- **Major:** 5 (DA-002-it6c through DA-006-it6c)
- **Minor:** 1 (DA-007-it6c)
- **Protocol Steps Completed:** 5 of 5
  - Step 1: Advocate Role Assumed — position: core decisions are under-justified at C4
  - Step 2: Assumptions Documented — 12 explicit, 8 implicit assumptions identified
  - Step 3: Counter-Arguments Constructed — 6 challenge areas pressed; 7 findings produced
  - Step 4: Response Requirements Assessed — design's response adequacy evaluated per finding
  - Step 5: Synthesized and Scored — Scoring Impact table completed
- **Artifacts Read:** 5 (2 partial: `phase1-requirements.md` lines 1-144 + 380-479; `phase2-stride-threat-model.md` lines 1-332 + 333-412)
- **Artifacts Written:** None (blindness constraint observed; no prior iteration outputs read)
- **Blindness Violations:** 0
- **H-16 Compliance:** Satisfied by tournament Group C ordering (Group B Steelman precedes)

---

*Strategy: S-002 Devil's Advocate*
*Finding Prefix: DA-NNN-it6c (iteration-006 Group C)*
*Template: `.context/templates/adversarial/s-002-devils-advocate.md` v1.0.0*
*Criticality: C4 — All tiers + tournament*
*Executed: 2026-06-28*
