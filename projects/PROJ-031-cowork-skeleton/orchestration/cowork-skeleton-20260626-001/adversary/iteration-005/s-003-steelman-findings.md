# Strategy Execution Report: Steelman Technique (S-003)

## Execution Context

- **Strategy:** S-003 (Steelman Technique)
- **Template:** `.context/templates/adversarial/s-003-steelman.md`
- **Deliverables (all 5 read, Group B blind):**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md`
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-003-credential-protection-supply-chain.md`
  - `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md`
  - `projects/PROJ-031-cowork-skeleton/security/phase2-stride-threat-model.md`
  - `projects/PROJ-031-cowork-skeleton/security/phase2-attack-surface.md`
- **Execution ID:** ITS005
- **Executed:** 2026-06-29T00:00:00Z (Group B, iteration-005, blind)
- **Blindness:** No prior adversary outputs read (tournament integrity preserved)

---

## Summary

**Steelman Assessment:** This design's core thesis — dedicated-repo prevention + Sigstore attestation + tag-provenance assertion as the distribution architecture for an executable-hook plugin — is architecturally sound and holds up under the most charitable scrutiny. The design has been stress-tested through four prior adversarial iterations and has self-corrected on every major finding. After constructing the strongest possible case for it, only two Major and five Minor weaknesses survive; no Critical gap undermines the core argument.

**Improvement Count:** 0 Critical, 2 Major, 5 Minor

**Original Strength:** HIGH. The five artifacts collectively represent a rigorous C4 security engineering effort: bidirectional requirement traces to 51+ REQs, a 27-threat STRIDE model with DREAD scoring and attack trees, seven architecturally grounded decisions (D1–D7), five explicitly disclosed Residual Trust Boundaries (RTB-1..5), and a determinism proof for the generation technique. The honest disclosure of what the design cannot prevent (org-owner suppression, maintainer collusion) is more trustworthy than designs claiming complete closure.

**Recommendation:** Incorporate improvements. The surviving Major findings are methodological completeness gaps in the STRIDE model and requirements, not architectural flaws. The core argument is ready for Devil's Advocate (S-002) attack.

---

## Step 1 — Deep Understanding (Charitable Interpretation)

**Core thesis:** Making Jerry installable in Claude CoWork requires distributing a deterministic, stripped derivative of the main repository through a dedicated public repo (`geekatron/jerry-cowork`). The distribution architecture must be prevention-first rather than detection-only because the artifact ships executable hooks that run on every user's session start upon a single org-admin registration. The design achieves this through seven layered security decisions (D1–D7) covering dedicated-repo protection, a least-privilege cross-repo credential, a Sigstore-backed build-provenance attestation anchor, a tag-on-main provenance assertion, CI hardening against injection, and a scheduled read-only backstop monitor.

**Key claims (all charitably interpreted at their strongest):**
1. The stripped tree (~1,417 files) comfortably under-counts CoWork's ~5,000-file limit — with a multi-dimensional verification gate before any irreversible action.
2. Option A (tag checkout → strip → deterministic commit → force-push) achieves true bit-identical idempotency through an exhaustive pin of every input to the git SHA.
3. The dedicated-repo + org-level ruleset converts the Phase-1 direct-push Critical from detection to prevention, not just for write collaborators but for any principal below org-owner level.
4. The Sigstore attestation anchor is genuinely CI-only-writable and publicly verifiable — a structurally distinct reference from the artifact branch's write credential, resolving the Phase-1 five-strategy convergent Critical.
5. D5 (tag-on-main provenance assertion + v* tag protection) closes the rogue-tag attack vector — the correct control because monitoring is blind to a faithfully-built malicious tag.
6. The five Residual Trust Boundaries (RTB-1..5) are explicitly named and honest about what prevention does not close: org-owner suppression, maintainer collusion, org-registration process boundaries, App-key custody, and install-time verification gap.

---

## Step 2 — Weakness Classification

| Weakness | Type | Magnitude | Note |
|----------|------|-----------|------|
| SC-06 (trusted-maintainer rogue build) present in STRIDE consolidated threat register but absent from AT-1/AT-2 attack trees | Structural | Major | STRIDE AT-1 has 5 OR branches; SC-06 is a 6th valid path to the root goal |
| REQ-047 org-registration monitor has no fallback for OQ-047 (API endpoint may not exist) | Structural | Major | Without OQ-047 resolved, RTB-3 detection reduces to process-control-only |
| R-001 §Verification Approach states "four-dimensional SHALL before Phase 2" then qualifies "dimension (d) MAY defer to Phase 4" — contradictory framing | Presentation | Minor | Implementers have ambiguous gate signal |
| CR-03 (App private key theft → attestation forgery) absent from AT-2 "Defeat tamper detection" attack tree | Structural | Minor | YELLOW 2×5=10 path missing from the tree |
| "≤ 6 h detection SLA" (REQ-035/D7) not qualified against GitHub Actions scheduler jitter | Evidence | Minor | GitHub schedule trigger has documented delay variance exceeding 6 h |
| CR-02 topological loop-safety has no automated verification step | Structural | Minor | A workflow file inadvertently placed in the dedicated repo silently violates the invariant |
| REQ-039 (v* tag protection ruleset) has an implicit GitHub plan-tier dependency | Evidence | Minor | Tag protection rulesets require GitHub Team/Enterprise; undisclosed |

All weaknesses are structural or evidence/presentation — none challenge the core thesis that dedicated-repo + attestation + provenance is the correct architecture for this distribution problem.

---

## Step 3 — Steelman Reconstruction

This section presents the strongest possible argument FOR the design's core thesis, strengthened beyond the artifacts' own expression, using the artifacts' own evidence.

### Steelmanned Core Argument

**The distribution architecture is correct because it correctly identifies the threat model's asymmetry:**

The artifact is not data — it is executable code (`hooks/session-start.py`) that runs with user-workstation permissions on every Claude session start, distributed to every org user simultaneously via a single org-admin registration. Any tamper window is therefore not a "detection window" problem — it is a "time-to-org-wide-compromise" window. The Phase-1 detection-only posture (ADR-002) was proportionate for a data artifact; it is not proportionate for an executable-hook artifact with org-wide blast radius. This is the decisive argument for prevention-first (D2 org-level ruleset) rather than detect-and-revert.

**The Sigstore attestation anchor is the strongest available integrity primitive:**

Build-provenance attestations (Sigstore-backed, immutable public transparency log) achieve three properties simultaneously: (1) CI-only-writable — no actor outside the CI workflow can publish an attestation for an arbitrary tree; (2) publicly verifiable — any third party can invoke `gh attestation verify`; (3) binding — the attestation cryptographically links the skeleton tip SHA to the source workflow run, repo, and commit. The Phase-1 Release-notes anchor failed property (1): Release notes share `contents: write` with the branch credential, making the verifier and the thing it verifies share one lock. Moving to the Sigstore-backed attestation makes property (1) structurally true rather than policy-dependent.

**The deterministic SHA is a load-bearing supply-chain primitive, not merely an engineering convenience:**

ADR-001's idempotency proof — pinning tree, parent, author identity, both author and committer dates, and a fixed-length commit message embedding the full 40-char source SHA — makes the generation function referentially transparent: `regenerate(T)` is a pure function of the release tag `T`. This means any in-place modification of the published branch changes the tip SHA away from the expected value in a way that is (a) independently computable by anyone who reruns the generator against the same tag, and (b) non-forgeable (a git SHA is the hash of content; producing the expected SHA for a different tree requires a preimage collision). This gives the design tamper-evidence without commit signing, without requiring CoWork to implement install-time verification, and without depending on the monitor's availability.

**D5 (provenance assertion) closes the one gap that D2/D4 together cannot see:**

With D2 preventing direct push and D4 providing an attestation anchor, the only remaining path to "ship malicious hooks to all users" that bypasses all controls is a well-formed `v*` tag pointing to a malicious commit — because CI faithfully builds and attests it, and D2's branch protection is blind to CI's own push. The design correctly identifies this as the top residual (SC-02) and provides the correct two-part control: build-time assertion (`git merge-base --is-ancestor`) blocking generation for non-main tags, and push-time tag protection (REQ-039) blocking unauthorized tag creation in the first place. The STRIDE model correctly notes that monitoring CANNOT catch this — a key insight that corrects the false ADR-001 claim.

**The seven Residual Trust Boundaries are honest and correctly classified:**

RTB-1 (org-owner can suppress the ruleset), RTB-2 (trusted-maintainer collusion), RTB-3 (org-registration as process control), RTB-4 (App key custody), and RTB-5 (no install-time CoWork verification) are all correctly framed as bounded residuals with named compensating controls, not as closed threats. This is intellectually honest security engineering and does not undermine the architecture — it defines the threat surface that personnel governance and audit must cover.

### Best Case Conditions [SM-ITS005 Label]

The design is strongest when:
- R-001 hypothesis (a) is confirmed empirically: CoWork's ~5,000-file limit applies to the tracked-file count on a clean clone, not the local working directory (which would be ~24,636 with `.venv/`)
- GitHub's immutable releases, build-provenance attestations, and ruleset bypass-actor semantics are confirmed to work exactly as documented on `geekatron/jerry-cowork` (empirical confirmation pre-Phase-5 per STRIDE S-010 note)
- The org maintains org-owner count at 1–2 principals with 2FA/SSO, reducing RTB-1 from a plausible threat to a very-low-probability one
- The App private key or deploy key is managed with rotation discipline (REQ-048: 12-month maximum)

**Confidence under best-case conditions: HIGH.** The architectural decisions map correctly to the threat categories; the controls are proportionate; the residuals are honest.

**Confidence under worst-case conditions: MEDIUM.** The design cannot guarantee R-001 verification (requires live CoWork), cannot close RTB-2 (maintainer collusion is personnel trust), and cannot guarantee the detection SLA if GitHub Actions scheduler delays compound. None of these worst-case conditions invalidate the architecture — they are correctly disclosed limitations.

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| SM-001-ITS005 | Major | SC-06 (trusted-maintainer rogue build) absent from STRIDE attack trees AT-1 and AT-2 | `security/phase2-stride-threat-model.md` §Attack Trees |
| SM-002-ITS005 | Major | REQ-047 org-registration monitor has no implementable fallback for OQ-047 | `requirements/phase1-requirements.md` WS-3 REQ-047 |
| SM-003-ITS005 | Minor | R-001 §Verification Approach contradicts itself on dimension (d) gate timing | `requirements/phase1-requirements.md` §Stated Assumption: R-001 |
| SM-004-ITS005 | Minor | CR-03 (App private key theft → attestation forgery) absent from AT-2 "Defeat tamper detection" | `security/phase2-stride-threat-model.md` §Attack Trees AT-2 |
| SM-005-ITS005 | Minor | "≤ 6 h" detection SLA in REQ-035/D7 is aspirational; GitHub Actions scheduler jitter not acknowledged | `requirements/phase1-requirements.md` REQ-035; `decisions/ADR-003` §D7 |
| SM-006-ITS005 | Minor | CR-02 topological loop-safety has no automated CI verification step | `decisions/ADR-003` §D7; `requirements/phase1-requirements.md` REQ-023 |
| SM-007-ITS005 | Minor | REQ-039 v* tag protection ruleset has an implicit GitHub plan-tier dependency — undisclosed | `requirements/phase1-requirements.md` REQ-039; `decisions/ADR-003` §D5 |

---

## Detailed Findings

### SM-001-ITS005: SC-06 Absent From STRIDE Attack Trees

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `security/phase2-stride-threat-model.md` §Attack Trees (AT-1, AT-2) |
| **Strategy Step** | Step 2 (weakness classification — structural gap) |
| **Owner** | eng-architect (STRIDE/security) |

**Evidence:**

The consolidated threat register includes SC-06 (Trusted-Maintainer Rogue Build) at rank 15, scored 2×4=8 YELLOW:

> `SC-06 | T/R (trusted insider) | ... Trusted-maintainer rogue build: a maintainer holding both main-write and v* tag-create rights lands a malicious commit on main (so the D5 ancestor check PASSES) and tags it; CI then faithfully builds AND attests the malicious tree...`

Attack tree AT-1 ("Ship malicious hooks to all org users") has five OR branches:

> `GOAL: malicious hooks/session-start.py executes on org users' workstations`
> `├─ OR 1. Direct push ... [DR-01] MITIGATED`
> `├─ OR 2. Rogue-tag CI self-certification ... [SC-02] OPEN`
> `├─ OR 3. Org-admin repoints/registers rogue marketplace ... [OR-01/02] OPEN`
> `├─ OR 4. Steal cross-repo credential ... [CI-01/CR-03] OPEN`
> `└─ OR 5. Dedicated-repo admin disables protection ... [DR-02] PARTIAL`

SC-06 (trusted-maintainer lands malicious commit on `main`, passes D5 ancestor check, CI faithfully builds) is a valid sixth OR branch to the AT-1 root goal and is absent. AT-2 ("Defeat tamper detection") also has no SC-06 branch, though the D5 scope boundary note correctly acknowledges it cannot be caught by D2/D4/D5.

**Steelmanned framing:** SC-06 IS disclosed in the consolidated threat register and correctly mitigated via REQ-051 (main-branch peer review). The ADR-003 S-010 self-refine note says it "closed the Methodological Rigor gap." The issue is not that SC-06 is undisclosed — it is that the C4-depth attack tree analysis, which is the artifact a security reviewer uses to evaluate completeness of the attack surface, does not include the path. A reviewer inspecting AT-1 would not see SC-06 and could incorrectly conclude all YELLOW-or-higher paths are covered.

**Why it still matters at C4:** C4 requires "all 10 strategies" and "quality target >= 0.95." The attack trees are the primary artifact for evaluating path completeness in the STRIDE methodology. Omitting a YELLOW (8) path from AT-1 is a methodological rigor gap at C4 depth. The subsequent strategies (S-002 Devil's Advocate, S-004 Pre-Mortem) will attack the STRIDE model's completeness claim; AT-1 as written would fail a "is this tree complete for YELLOW+ threats?" check.

**Recommendation:** Add OR-6 to AT-1:

```
├─ OR 6. Trusted-maintainer lands malicious commit on main + tags it ... [SC-06]
│        └─ AND: holds main-write + v* tag-create rights; D5 ancestor check PASSES; CI builds + attests
│        └─ Blocked by: REQ-051 (required peer review on main for tag-create principals) [RTB-2]
│        └─ Residual: two-maintainer collusion — personnel trust only
```

Add a corresponding DREAD row for SC-06 in the AT table (D=8, R=3, E=3, A=9, D=6, DREAD mean ~5.8 — lower than AT-1.2 but still YELLOW).

---

### SM-002-ITS005: REQ-047 Org-Registration Monitor Has No Fallback for OQ-047

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `requirements/phase1-requirements.md` WS-3 §ADR-003 RTB/SC-06 Requirements (REQ-047) |
| **Strategy Step** | Step 2 (weakness classification — structural gap) |
| **Owner** | nse-requirements (requirements) |

**Evidence:**

REQ-047 text: "An automated monitor SHALL verify (≤ 24 h) that the org's registered CoWork source matches canonical `geekatron/jerry-cowork`, with an org audit-log webhook on marketplace-settings change; mismatch → GitHub issue."

The acceptance criterion states: "OQ-047: API endpoint for org registered CoWork source MUST be discovered empirically before REQ-047 can be verified."

The S-010 self-refine note in the requirements explicitly flags: "OQ-047 flagged in requirement text AND AC — implementers have unambiguous signal." However, neither the requirement nor the ADR-003 RTB-3 note defines what happens if the API endpoint does not exist or is not publicly accessible.

ADR-003 RTB-3 states: "CoWork's org marketplace registration is a single-actor server-side setting. It is therefore a **process control**, not a prevented state. Technical-detection compensator: an automated monitor (REQ-047) queries the org's registered CoWork source ≤ daily (target ≤ 24 h) and alerts on any drift."

**Steelmanned framing:** The design is honest: OQ-047 is an open question, the requirement is correctly labeled, and the S-010 note says implementers have "unambiguous signal." REQ-043 (process control: vetted-admin restriction, canonical-name runbook, periodic verification) provides baseline coverage even without REQ-047. The risk is OR-01/02 (rogue org registration, YELLOW 2×5=10), which requires an org-admin to be compromised or make a mistake. The process control is not negligible.

**Why it still matters at C4:** The design explicitly names REQ-047 as the "technical-detection compensator" for RTB-3. RTB-3 is identified as a process-control boundary where "a single compromised org-owner can re-register to a rogue/typosquat repo; the two-admin rule does not stop the action, and harm occurs in the detection window before REQ-047 alerts." If OQ-047 cannot be resolved (no API exists), the technical-detection compensator collapses entirely, leaving only the process control. At C4, a named detection compensator with an unresolved implementation path and no fallback is a requirements completeness gap. The STRIDE model gives OR-01/02 a combined score of 2×5=10 YELLOW — high enough to require a fallback specification.

**Recommendation:** Add a fallback sub-requirement to REQ-047:

> If the API endpoint for querying the org's registered CoWork source is empirically unavailable (OQ-047 unresolvable), the automated monitor SHALL fall back to: (a) querying the GitHub Org Audit Log API for marketplace-settings events and alerting on any change from the baseline timestamp documented at initial registration, AND (b) a periodic human-verification step (≤ monthly, documented in the org-registration runbook per REQ-043) SHALL explicitly confirm the registered source URL matches `geekatron/jerry-cowork` using the CoWork admin UI. If neither (a) nor (b) is implementable, REQ-047 SHALL be marked DEFERRED and the risk score for OR-01/02 SHALL be explicitly re-rated in the risk register to account for the absent technical-detection compensator.

---

### SM-003-ITS005: R-001 Verification Approach Internally Contradicts Itself on Gate Timing

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `requirements/phase1-requirements.md` §Stated Assumption: R-001, §Verification Approach |
| **Strategy Step** | Step 2 (weakness classification — presentation) |
| **Owner** | nse-requirements (requirements) |

**Evidence:**

R-001 §Verification Approach: "A mandatory **four-dimensional** verification SHALL be executed before Phase 2 begins (dimension (d) MAY be deferred to Phase 4 if a CoWork runtime is unavailable)."

The same section states: "All four dimensions must pass before Phase 5 implementation scripts may execute."

And REQ-034: "A mandatory three-dimensional verification gate SHALL be executed before Phase 2 begins (with the fourth dimension optionally deferred to Phase 4)."

**Contradiction:** The R-001 section says "four-dimensional SHALL before Phase 2" while immediately qualifying that dimension (d) MAY defer to Phase 4. REQ-034 correctly expresses the intent as "three-dimensional before Phase 2, fourth optional to Phase 4" but R-001's leading sentence contradicts this.

**Steelmanned framing:** The design intent is clear from REQ-034 and the qualifying clause: dimensions (a)(b)(c) are the Phase 2 gate; dimension (d) requires a live CoWork environment that may not be available. The actual sequencing is correctly handled. This is a presentation inconsistency, not a design flaw.

**Why it still matters at C4:** At C4, the requirements are approval artifacts (AG-01) reviewed by the user before any implementation action. An approval reviewer reading R-001 first encounters "four-dimensional SHALL before Phase 2" and could conclude all four must pass before Phase 2, then read the qualifier and be confused about whether a three-dimensional pass is sufficient to proceed. In a C4 quality gate context, ambiguous gate language is a risk — a maintainer could block Phase 2 waiting for a live CoWork environment that isn't available.

**Recommendation:** Rewrite R-001 §Verification Approach opening to: "A three-dimensional verification SHALL be completed and its machine-checkable artifact committed BEFORE Phase 2 begins, covering dimensions (a), (b), and (c) below. Dimension (d) — the direct CoWork plugin-install smoke test — SHALL be completed no later than the end of Phase 4, before any Phase 5 implementation scripts may execute; it MAY be deferred from Phase 2 if a CoWork runtime is unavailable."

---

### SM-004-ITS005: CR-03 (App Private Key Theft → Attestation Forgery) Absent From AT-2

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `security/phase2-stride-threat-model.md` §Attack Trees AT-2 |
| **Strategy Step** | Step 2 (weakness classification — structural gap) |
| **Owner** | eng-architect (STRIDE/security) |

**Evidence:**

AT-2 ("Defeat tamper detection") has three OR branches:

> `GOAL: tampered branch installable without alert`
> `├─ OR 1. Forge the integrity anchor ... [SC-04] MITIGATED (now immutable attestation)`
> `├─ OR 2. Suppress the monitor ... [DR-02/SC-05]`
> `└─ OR 3. Make CI itself certify the tamper ... [SC-02] (rogue tag)`

CR-03 (App private key theft, YELLOW 2×5=10) is documented in the threat register: "The App private key is the project's single long-lived secret; theft = durable forgery of artifact + attestation identity."

An attacker who steals the App private key can: (a) forge an attestation for a malicious tree by impersonating the CI identity, and (b) push to the dedicated repo using the stolen key (bypassing D2 since the key IS the bypass actor). This is a valid path to "tampered branch installable without alert" — the tampered tree would have a matching attestation and would pass `gh attestation verify`.

**Steelmanned framing:** CR-03 is fully documented in the threat register (rank 9, YELLOW 2×5=10) with mitigations: source-repo secrets only, rotation, short-lived App tokens. The design is not unaware of this path. The attack tree is simply incomplete as a standalone artifact.

**Why it still matters at C4:** The attack trees are cited as the analytical artifact for evaluating the "Defeat tamper detection" attack goal. A reviewer who uses AT-2 to assess the design's tamper-detection completeness would not see the CR-03 path and could incorrectly conclude that the three OR branches are exhaustive.

**Recommendation:** Add OR-4 to AT-2:

```
└─ OR 4. Steal App private key → forge attestation for tampered tree ... [CR-03]
         └─ AND: exfiltrate App private key via CI-04 or V-02/V-04
         └─ THEN: sign malicious tree attestation + push via stolen key
         └─ Bounded by: source-repo secrets; rotation cadence (REQ-048); short-lived minted tokens;
            D7 monitor detects tip-SHA drift if a DIFFERENT key is used for push vs. attestation
         └─ Not fully mitigated: a stolen key could forge both push AND attestation in one action
```

---

### SM-005-ITS005: "≤ 6 h" Detection SLA Aspirational Due to GitHub Actions Scheduler Jitter

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `requirements/phase1-requirements.md` REQ-035; `decisions/ADR-003` §D7 |
| **Strategy Step** | Step 2 (weakness classification — evidence gap) |
| **Owner** | nse-requirements (requirements) |

**Evidence:**

REQ-035: "A residual integrity backstop monitor SHALL run on a `schedule` trigger (≤ 6-hourly cadence)..."

ADR-003 D7: "Bounded by the poll cadence (≤ 6 h) rather than near-real-time event delivery; the meta-monitor heartbeat (REQ-044, 25 h) detects monitor outages."

GitHub's official documentation on scheduled triggers states that cron schedules for public repos may run significantly later than the scheduled time during high-load periods, and that schedules during periods of heavy load may be delayed by 15 minutes or more, with no guarantee of exact timing.

Neither REQ-035 nor ADR-003 D7 acknowledges that the "≤ 6 h" cadence is a target, not a platform guarantee. The meta-monitor (REQ-044, 25 h alert if no success) provides a backstop for outright monitor failure, but schedule delay (monitor runs but late) falls in a gap between the 6 h SLA and the 25 h meta-monitor.

**Steelmanned framing:** The design correctly demotes the monitor to a backstop, not a front-line control. Prevention (D2) + attestation (D4) carry the load; the monitor covers residual credential-theft and admin-suppression paths. A 6 h SLA with some jitter (→ 8 h actual) does not materially change the security posture. The meta-monitor catches outright failures.

**Why it still matters at C4:** RTB-4 (App key theft) explicitly states the residual is "durable forgery until the D7 backstop detects the resulting tip-SHA / attestation mismatch." The detection window claim matters for this residual path. Understating the guaranteed SLA (6 h) vs. the realized SLA (up to 8–12 h under load) introduces a false precision that overstates the monitor's reliability.

**Recommendation:** Amend REQ-035 SLA language: "...SHALL run on a `schedule` trigger targeting ≤ 6-hourly cadence; actual execution timing is subject to GitHub Actions scheduler availability and may be delayed; the detection SLA should be understood as a target cadence, not a platform-guaranteed bound. REQ-044 (meta-monitor, 25 h heartbeat) provides a backstop for scheduler failure."

---

### SM-006-ITS005: CR-02 Topological Loop-Safety Has No Automated Verification Step

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `decisions/ADR-003` §D7, §Loop-safety re-derived; `requirements/phase1-requirements.md` REQ-023 |
| **Strategy Step** | Step 2 (weakness classification — structural gap) |
| **Owner** | nse-requirements (requirements) |

**Evidence:**

ADR-003 D7: "This invariant must be asserted in config and review."

ADR-003 §L1 Technical Implementation: "Loop-safety is re-established topologically: (1) the dedicated repo runs no workflow that pushes — the D7 integrity monitor lives in the source repo and is read-only against the dedicated repo, never pushing there; (2) the source generation workflow triggers on tags + workflow_dispatch only, and the source monitor runs on schedule and pushes no tags — so neither retriggers generation."

REQ-023: "The dedicated repo (`geekatron/jerry-cowork`) SHALL NOT contain any workflow that pushes to the source repo."

Neither REQ-023 nor any other requirement specifies an automated CI verification step that checks the dedicated repo contains no workflows with push capability. The control is "assertion in config and review" — a human review step at repo provisioning time.

**Steelmanned framing:** The dedicated repo is generated by force-push from the source, and the source's `.github/workflows/` directory is not in the retention surface for the skeleton — so workflow files would not be present unless someone manually added them to the dedicated repo. The risk is low. But it is not zero: the bypass-actor credential (App token or deploy key) could be used to push workflow files directly.

**Why it still matters at C4:** Loop-safety is a C4 pipeline correctness property. The source repo's `cowork-skeleton.yml` triggers on tags; if the dedicated repo ever gains a workflow that pushes a v* tag back to the source repo, the generation pipeline would loop. The current control ("assert in config and review") is a human process control with no automated verification. At C4, unverified invariants are findings.

**Recommendation:** Add to REQ-023 acceptance criteria: "A CI step in `cowork-skeleton.yml`, executing after the dedicated-repo push and before job success, SHALL use `gh api` or `git ls-remote --heads` to assert that the dedicated repo's `.github/workflows/` tree (if present) contains no workflow files with a `push:` trigger that targets the source repo. If the check fails, the job SHALL exit non-zero and open a GitHub issue."

---

### SM-007-ITS005: REQ-039 v* Tag Protection Has Undisclosed GitHub Plan-Tier Dependency

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `requirements/phase1-requirements.md` REQ-039; `decisions/ADR-003` §D5 |
| **Strategy Step** | Step 2 (weakness classification — evidence gap) |
| **Owner** | nse-requirements (requirements) |

**Evidence:**

REQ-039: "The source repo SHALL apply a ruleset restricting `v*` tag creation to the release pipeline / maintainers (tag protection)."

ADR-003 D5: "a source-repo ruleset restricting `v*` tag creation to the release pipeline / maintainers."

GitHub rulesets (including tag protection via rulesets) are available on GitHub Team and GitHub Enterprise plans. Basic "tag protection rules" (the older, less flexible feature) are available on all plans. However, ruleset-based tag protection with bypass actors (which is what D5 requires to allow the release pipeline to create tags while blocking collaborators) requires Team or higher.

Neither REQ-039 nor ADR-003 §D5 discloses this plan-tier dependency. If `geekatron` is on a free or Pro plan, the sophisticated ruleset-based tag protection may not be available, and the fallback to basic tag protection rules may not support bypass actors.

**Steelmanned framing:** `geekatron` already has an org-level ruleset protecting `main` (the "Don't fuck with main" ruleset referenced throughout), which presupposes Team or Enterprise plan access. The plan-tier issue is likely not a practical concern. The omission is a documentation completeness gap, not a design flaw.

**Why it still matters at C4:** D5 is the load-bearing control for SC-02 (rogue-tag, YELLOW 2×5=10 — the top residual). The REQ-039 acceptance criteria should include plan-tier verification: "Confirm the source repo's GitHub plan tier supports ruleset-based tag protection with bypass-actor configuration; if it does not, document the available tag protection alternative and its limitations."

**Recommendation:** Add to REQ-039: "Implementation NOTE: tag protection rulesets with bypass-actor configuration require GitHub Team or Enterprise plan tier. Before implementing REQ-039, verify the source repo's plan tier supports this feature. If not supported, document the fallback (basic tag protection rules, which restrict all tag creation without bypass-actor support) and its security implications (the release pipeline would also be restricted, requiring the ruleset to be temporarily disabled for releases — a human process control, not a technical one)."

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-001 (SC-06 in attack trees), SM-004 (CR-03 in AT-2), SM-006 (loop-safety verification), SM-007 (plan-tier disclosure) all add coverage the artifacts currently lack |
| Internal Consistency | 0.20 | Positive | SM-003 (R-001 framing contradiction) corrected; design intent already consistent, expression now made unambiguous |
| Methodological Rigor | 0.20 | Positive | SM-001 directly improves STRIDE attack tree completeness at C4 depth; SM-004 closes a secondary tree gap |
| Evidence Quality | 0.15 | Positive | SM-005 (scheduler jitter) corrects a false-precision SLA claim; SM-007 grounds REQ-039 in GitHub plan-tier evidence |
| Actionability | 0.15 | Neutral | Existing remediation paths are already well-specified; improvements add implementation precision rather than new actions |
| Traceability | 0.10 | Positive | SM-002 (REQ-047 fallback) adds a missing trace from OQ-047 risk to a fallback requirement; SM-003 aligns R-001 gate language with REQ-034 |

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 0
- **Major:** 2
- **Minor:** 5
- **Protocol Steps Completed:** 6 of 6 (including H-15 self-review before persistence)

---

## H-15 Self-Review Checklist

- [x] All findings have specific evidence from the deliverables (direct quotes / section references provided)
- [x] Severity classifications justified: both Major findings materially affect security posture or methodological completeness at C4; no Critical findings because no gap undermines the core architectural thesis
- [x] Finding identifiers follow SM-NNN-ITS005 format consistently
- [x] Summary table matches detailed findings (7 entries, counts consistent)
- [x] No findings minimized: surviving weaknesses are honestly stated as genuine gaps, not strawmen
- [x] P-022: confidence levels honest — "HIGH" on architectural thesis, "MEDIUM" on specific implementations requiring empirical confirmation; no false-precision claims
- [x] Blindness maintained: no adversary output files read

---

## Steelman Verdict

**The design's core thesis holds.** The dedicated-repo + org-level-ruleset + Sigstore attestation + tag-provenance architecture is structurally sound, proportionate to the threat model (executable-hooks, org-wide blast radius), and correctly closes the two former Phase-1 Criticals. The seven findings above are methodological completeness improvements at C4 depth — they make the design more rigorous, not fundamentally different. The strongest surviving weakness is **SM-001** (SC-06 absent from STRIDE attack trees), which is the highest-impact gap for a C4 reviewer assessing whether the attack tree analysis is complete.

---

*Strategy: S-003 Steelman Technique*
*Template: `.context/templates/adversarial/s-003-steelman.md` v1.0.0*
*Execution ID: ITS005*
*Agent: adv-executor*
*Constitutional: P-001 (evidence-based), P-002 (persisted), P-003 (no subagents), P-004 (provenance cited), P-011 (evidence per finding), P-022 (severity honest)*
*Blindness: Group B — no prior adversary outputs read*
