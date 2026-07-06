# Strategy Execution Report: Inversion Technique (S-013)

## Execution Context

- **Strategy:** S-013 (Inversion Technique)
- **Template:** `.context/templates/adversarial/s-013-inversion.md`
- **Deliverable:** Five artifacts: ADR-001, ADR-003, phase1-requirements.md, phase2-stride-threat-model.md, phase2-attack-surface.md (HISTORICAL banner)
- **Executed:** 2026-06-29T00:00:00Z
- **Reviewer:** adv-executor (iteration-006, Group E)
- **Criticality:** C4
- **H-16 Compliance:** S-003 Steelman applied in prior iterations (confirmed by tournament chain)
- **Goals Analyzed:** 8 | **Assumptions Mapped:** 18 | **Vulnerable Assumptions:** 10

---

## Summary

Inversion of the design objective ("guarantee this silently fails") surfaces three Critical and six Major structural weaknesses. The most concentrated fragility is the **update-propagation assumption (IN-001)**: the entire "automatically in sync" headline value rests on an unverified CoWork behavior, and if CoWork caches at install the design's primary user promise is false from day one with no current fallback path. Simultaneously, the **D5 provenance gate is designed-not-implemented (IN-002)** — the top-ranked residual attack vector (SC-02 rogue-tag) is open through Phase-5 with zero technical detection while it remains unimplemented. A third Critical (IN-003) reveals that all six Phase-5 gates are process controls with no technical enforcement mechanism, meaning delivery pressure can trivially bypass the entire gate set. Overall recommendation: **REVISE before go-live** — targeted mitigations for the three Criticals are mandatory; none require a design change, only implementation and enforcement work.

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| IN-001-it006s013 | **Critical** | CoWork update propagation to already-installed users is unverified — "automatically in sync" may be false for all existing users from day one | ADR-001 L2 §6, Risks; REQ-054/OQ-048 |
| IN-002-it006s013 | **Critical** | D5 (tag-on-main provenance + v* tag protection) is designed-not-implemented; the #1 ranked attack vector (SC-02 rogue-tag) is open through Phase-5 with zero technical detection controls | ADR-003 D5; STRIDE SC-02 |
| IN-003-it006s013 | **Critical** | Phase-5 go-live gates are process controls with no technical enforcement; delivery pressure can silently bypass all six gates | ADR-003 Phase-5 Validation Gate Set |
| IN-004-it006s013 | **Major** | RTB-1 (org-owner ruleset suppression) combined-attack path is unanalyzed: an org-owner can simultaneously suppress the branch ruleset AND interfere with the source-repo monitor | ADR-003 RTB-1; STRIDE DR-02 |
| IN-005-it006s013 | **Major** | D8 allow-list bloat is a viable long-term bypass vector for SC-06/SC-08; the allow-list has no maximum size, no annual review requirement, and no second technical control on the same path | ADR-003 D8; STRIDE D8 Detector Specification |
| IN-006-it006s013 | **Major** | D7 monitor fail-closed (FM-033) acceptance criteria do not cover all internal error modes (API rate limits, CLI tool absence, network timeout, malformed response); partial coverage leaves a silent-exit-0 window | ADR-003 D7; STRIDE SC-05; REQ-035 |
| IN-007-it006s013 | **Major** | G-headroom thresholds (250 MB pack, 60 s clone) are set relative to ADR-001 Option B flip triggers, NOT empirically derived from CoWork's actual ceiling; the ceiling dimension (file count vs size vs time) remains unverified | ADR-001 §4; REQ-034/REQ-006; R-001 |
| IN-008-it006s013 | **Major** | Org marketplace registration has no technical enforcement of two-admin approval (RTB-3); the incident-response SLA after the audit-log webhook fires is undefined — harm window is unbounded | ADR-003 RTB-3; REQ-043/REQ-047 |
| IN-009-it006s013 | **Minor** | The Option A → Option B (orphan) clone-weight flip is manual; when the early-warning band (150 MB / 40 s) is reached, a GitHub issue is opened but no automated mechanism proposes the one-line change | ADR-001 Clone-Weight Decision |
| IN-010-it006s013 | **Major** | D8 implementation (pattern catalog + scanner tooling + CI integration + G-content test) is not tracked by any worktracker STORY with an owner and deadline; a required security gate has no delivery path | ADR-003 D8 hand-off; STRIDE D8 Detector Specification; REQ-052 |

---

## Detailed Findings

### IN-001-it006s013: CoWork Update Propagation Unverified — Headline Value at Risk [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Type** | Assumption (load-bearing, unverified) |
| **Section** | ADR-001 L2 §6, Risks row (PM-001/CV-001); REQ-054/OQ-048; STK-002 |
| **Strategy Step** | Step 1 (goal extraction — implicit goal G-2) and Step 4 (stress-test) |
| **Confidence in assumption** | Low |

**Anti-goal framing (Step 2):**
To guarantee the design fails at its "automatically in sync" objective, we need CoWork to cache the plugin tree at install time and only update on explicit user action (reinstall, "check for updates" button, or internal schedule). This is the default behavior for the overwhelming majority of plugin systems — app stores, IDE extensions, browser extensions — and there is currently zero empirical evidence that CoWork deviates from this norm.

**Evidence:**
ADR-001 L2 §6 states: "Whether CoWork delivers those rebuilds to **already-installed** users is an **unverified CoWork behavior** — a load-bearing assumption that MUST be empirically proven before go-live." The Risk table entry (PM-001/CV-001) reads: "MED probability, HIGH impact (every user silently runs a stale Jerry; new skills/agents referenced by H-22 don't exist)." REQ-054/OQ-048 in the requirements states this must be verified, and STK-002 is explicitly "re-scoped as contingent on G-update being verified." However, there is no concrete alternative delivery mechanism defined if G-update fails: the fallback is "alternate update path / documented manual procedure" — but neither is specified.

**Inversion consequence:**
If CoWork caches at install, the design's primary headline value is false from day one. Every org user who installed before a given Jerry release is silently running a stale version. Security fixes shipped in a new release do not reach existing users. New agents/skills introduced (e.g., by H-22 skill additions) are referenced in CLAUDE.md but missing from the installed plugin surface. The CI regeneration + cross-repo push mechanism works perfectly; the failure is the last-mile CoWork→session propagation.

**Why this is Critical at C4:**
The design explicitly acknowledges this as a "load-bearing assumption" (ADR-001). The failure is silent — no error, no warning — and affects every already-installed user. The fallback path is unspecified. No current control would reveal that existing users are running stale versions.

**Recommendation:**
1. G-update MUST be executed on a live CoWork instance with an existing plugin installation BEFORE any org-registration runbook begins. This is already a gate — the gap is that the contingency path is vague.
2. ADD to ADR-001 (or REQ-054): if G-update reveals caching, the project MUST choose between (a) a forced-update CoWork mechanism (if available), (b) an explicit "Jerry update" CLI command that reinstalls the plugin, or (c) re-scoping STK-002 to "current for new installs only; existing users must manually re-register." The choice must be user-approved (P-020) before go-live.
3. nse-requirements: strengthen OQ-048 to include the specific contingency resolution paths as acceptance criteria, not just the empirical test.

**Acceptance Criteria to resolve:**
(1) A force-push to `geekatron/jerry-cowork` on a live CoWork instance with an already-installed Jerry plugin results in the updated content appearing in the next user session within a documented bounded window — OR — (2) An alternative update mechanism is documented, user-approved, and the STK-002 claim is re-scoped to accurately reflect the update behavior.

**OWNER:** requirements → nse-requirements (OQ-048); ADR → ps-architect (ADR-001 L2 §6 contingency path)

---

### IN-002-it006s013: D5 Designed-Not-Implemented — Top Attack Vector Open Through Phase-5 [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Type** | Anti-Goal (necessary control absent) |
| **Section** | ADR-003 D5; STRIDE SC-02 (#1 in Consolidated Threat Register); Phase-5 gate G-provenance |
| **Strategy Step** | Step 2 (anti-goal: guarantee integrity failure) and Step 4 (stress-test) |
| **Confidence in assumption** | Low (explicitly flagged FM-032) |

**Anti-goal framing (Step 2):**
To guarantee that a bad actor can ship malicious hooks to all CoWork org users despite all other controls, we need them to push a well-formed `v9.9.9` tag pointing at a commit that does NOT trace to `main`. The D5 provenance gate (`git merge-base --is-ancestor`) would block this — but D5 is explicitly "designed, NOT yet implemented (FM-032)." While D5 is unimplemented, the attack path is open.

**Evidence:**
ADR-003 D5 states: "**Status: Designed — operational validation pending [G-provenance] (FM-032).** Both legs (REQ-038 ancestor assertion, REQ-039 `v*` tag-protection ruleset) are **specified but NOT yet implemented**. Until **G-provenance** proves them on the live pipeline [...] the rogue-tag self-certification path (SC-02) **remains open through Phase-5**." STRIDE SC-02 is ranked #1 in the Consolidated Threat Register (2×5=10, YELLOW). The attack path is: collaborator with tag-push access (a subset of write access, often granted more broadly than branch-push rights) → creates `v9.9.9` at a malicious commit → CI faithfully builds, D5 PASSES (because D5 isn't implemented), D4 ATTESTS the malicious tree, D7 returns PASS → malicious hooks shipped to all org users.

**Inversion consequence:**
With D5 unimplemented, there is ZERO technical detection for the rogue-tag path. The attestation (D4) certifies a faithfully-built malicious artifact. The monitor (D7) confirms the tip matches the attested value. The branch protection (D2) is irrelevant — CI is the legitimate pusher. The only thing blocking this vector is the absence of a motivated attacker with tag-push credentials, which is not a control.

**Why this is Critical at C4:**
SC-02 is the #1-ranked threat in the STRIDE model for the dedicated-repo architecture. D5 is the sole control and it is not implemented. The design explicitly acknowledges it "blocks Phase-5 until G-provenance passes" — but there is no worktracker STORY, no implementation deadline, and no CI check preventing go-live if D5 remains unimplemented. Process discipline alone is insufficient for a C4 security control.

**Recommendation:**
1. Create a worktracker STORY for D5 implementation (REQ-038: ancestor assertion in `cowork-skeleton.yml`; REQ-039: `v*` tag-protection ruleset on source repo) with eng-architect as owner and a hard deadline before Phase-5 begins.
2. Add a CI lint check in `main` that verifies the `cowork-skeleton.yml` workflow contains the ancestor assertion step before any `v*` tag can be pushed.
3. ADR-003 D5 should be promoted to the same priority as the credential (D3) in the implementation sequence — it is the top residual and the only control for the #1 attack vector.

**Acceptance Criteria to resolve:**
G-provenance synthetic test: a `v*` tag pointing at a commit NOT on `main` causes `cowork-skeleton.yml` to exit non-zero with no attestation produced and no push to `geekatron/jerry-cowork`. A `v*` tag-creation-protection ruleset rejects tag creation by a non-authorized actor.

**OWNER:** ADR → ps-architect; STRIDE/security → eng-architect; requirements → nse-requirements (REQ-038/039)

---

### IN-003-it006s013: Phase-5 Gates Are Process Controls With No Technical Enforcement [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Type** | Anti-Goal (systematic bypass path) |
| **Section** | ADR-003 Phase-5 Validation Gate Set; Claim-Status Convention |
| **Strategy Step** | Step 2 (anti-goal: guarantee controls are bypassed) and Step 4 |
| **Confidence in assumption** | Low-Medium |

**Anti-goal framing (Step 2):**
To guarantee that the design's security posture is theater rather than substance, we only need delivery pressure to cause go-live before the Phase-5 gates are executed. The authorization rule states "Go-live SHALL NOT proceed unless EVERY gate PASSES" — but there is no technical mechanism that PREVENTS go-live if the gates haven't run.

**Evidence:**
ADR-003 explicitly flags this risk: "IN-004: today *all* WS-3 controls are Draft, so go-live could otherwise proceed with zero security controls actually working." The Phase-5 Validation Gate Set is a document section in ADR-003 and a checklist in the requirements — both are process controls. The org-marketplace-registration runbook (the physical go-live action) is described but not yet written; it contains no CI gate or cryptographic proof that each Phase-5 test was executed. From the STRIDE model: all six gates (G-prevention, G-update, G-provenance, G-content, G-monitor, G-headroom) are "Designed — operational validation pending" — none is "Implemented & validated." A single human decision (org-admin registration) could execute before all tests are complete.

**Inversion consequence:**
If Phase-5 gates are skipped under time pressure, the following gaps remain live at go-live: (1) D2 ruleset bypass-actor semantics unverified — direct push still possible for principals not below org-owner; (2) D5 unimplemented — rogue-tag attack path fully open; (3) D8 untested — no technical protection for prompt injection in the markdown payload; (4) D7 freshness/fail-closed behavior unverified — monitor may report false-green on stale or tampered content; (5) CoWork update propagation unverified — "automatically in sync" value claim potentially false; (6) File ceiling dimension unverified — skeleton may not install on real CoWork. Under delivery pressure, any or all of these could be in an unvalidated state at org-registration time.

**Why this is Critical at C4:**
The Claim-Status Convention is excellent at tracking "designed vs validated" status, but it relies on the person doing the registration to CHECK the checklist. There is no technical barrier. This is intrinsically fragile for a C4 irreversible action (org marketplace registration reaches every user immediately).

**Recommendation:**
1. ADD a `phase5-gate-evidence.md` file requirement to the repo: before the org-registration runbook can be executed, this file MUST be committed (via a reviewed PR to `main`) containing CI run IDs, timestamps, and pass verdicts for each of the six gates.
2. The org-registration runbook MUST begin with a step that verifies `phase5-gate-evidence.md` exists and was committed after the start of Phase-5 testing.
3. Consider making the org-marketplace-registration itself require two-admin approval (process) with the gate-evidence file as a required artifact in the approval workflow.

**Acceptance Criteria to resolve:**
A `phase5-gate-evidence.md` file exists in the repo, committed via reviewed PR, containing a dated CI run ID and pass verdict for each of G-prevention, G-update, G-provenance, G-content, G-monitor, and G-headroom. The org-registration runbook's first step references this file.

**OWNER:** requirements → nse-requirements (Phase-5 authorization checklist + evidence-file requirement); ADR → ps-architect (ADR-003)

---

### IN-004-it006s013: RTB-1 Combined-Attack Path Unanalyzed [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Anti-Goal (combination attack unaddressed) |
| **Section** | ADR-003 RTB-1; STRIDE DR-02 |
| **Strategy Step** | Step 3 (implicit assumption mapping) and Step 4 |

**Anti-goal framing:**
To guarantee that an organization owner can cause lasting harm without triggering the detection backstop, they need to: (1) suppress the org-level ruleset, (2) push malicious content directly, AND (3) disable or delay the D7 monitor (which lives in `geekatron/jerry` on `main`, a repo they also control as org-owner).

**Evidence:**
ADR-003 RTB-1 analyzes DR-02 in isolation: "An organization owner can modify or delete the org-level ruleset itself and then push directly. [...] detection-only." The compensating control is "the out-of-band attestation backstop (D4) within the D7 detection window." But the D7 monitor is a scheduled workflow (`cowork-monitor.yml`) on the SOURCE repo (`geekatron/jerry`) whose `main` branch is controlled by the same org. An organization owner who can suppress the dedicated-repo ruleset also has the ability to disable or modify `cowork-monitor.yml` on the source repo — disabling the sole detection mechanism for the period between the tamper and the next human audit-log review.

**Inversion consequence:**
The combination of (suppressed ruleset + direct push + disabled monitor) removes the ≤6h detection SLA entirely. Without the monitor, the tamped content persists until a human notices via the meta-monitor heartbeat (≤25h) — or longer if the meta-monitor is also disabled.

**Why this is Major (not Critical):**
RTB-1 is acknowledged as detection-only for org-owners; this finding adds specificity to the combined-attack path rather than identifying a new gap. The finding is Major because the combined-attack analysis is absent from the current documentation, which means the detection SLA assumption ("≤6h") is not proven to hold when the organization owner is the threat actor.

**Recommendation:**
1. Extend ADR-003 RTB-1 with a combined-attack analysis: "An organization owner can suppress the artifact branch ruleset AND modify `cowork-monitor.yml` in the source repo. In this scenario, the ≤6h detection SLA does NOT hold."
2. Add a compensating control: the meta-monitor heartbeat (REQ-044, 25h) should send to an EXTERNAL destination (e.g., a personal email/SMS to a named second person) rather than only a GitHub issue — so that a compromised org cannot suppress both the monitor AND the GitHub notification.

**OWNER:** STRIDE/security → eng-architect (RTB-1 extended analysis); requirements → nse-requirements (REQ-044 external notification)

---

### IN-005-it006s013: D8 Allow-List Bloat Erodes Pattern Coverage Over Time [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption (long-term degradation) |
| **Section** | ADR-003 D8; STRIDE D8 Detector Specification (False-positive handling) |
| **Strategy Step** | Step 4 (stress-test D8 assumption over time) |

**Anti-goal framing:**
To guarantee the D8 content-safety gate becomes ineffective over time, we need the allow-list to grow without bounds as legitimate Jerry content (adversary templates, red-team docs) matches injection pattern categories. Each time a false positive is added to the allow-list, the effective coverage of that pattern shrinks. With a large enough allow-list, the gate becomes a rubber stamp.

**Evidence:**
STRIDE D8 Detector Specification acknowledges: "Jerry's own legitimate corpus *discusses* prompt injection (this very threat model, `/adversary` strategy templates, red-team agent docs)." The false-positive handling mechanism relies on a "version-controlled, code-reviewed allow-list keyed by `{file path + rule id + content hash}`." However: (1) there is no maximum allow-list size defined; (2) there is no periodic review requirement for allow-list entries; (3) there is no second independent technical control on the SC-06/SC-08 trusted-maintainer path.

**Inversion consequence:**
Over 12–24 months as the Jerry corpus grows (new adversary strategies, new red-team docs, new constraint templates), the allow-list grows. Each entry is individually justified and individually hash-pinned. But the collective effect is that an increasing fraction of the retained markdown surface is exempt from pattern matching. A sophisticated attacker who knows the allow-list content could craft an injection that mimics an existing allow-listed pattern.

**Recommendation:**
1. Add a maximum allow-list entry count (e.g., ≤20 entries) before a security review is required.
2. Add a quarterly allow-list audit requirement: verify each entry is still necessary and that no two entries cover overlapping content.
3. Add a second independent technical control on the SC-06 path: a diff-based alert (separate GitHub check) that flags commits touching `skills/**/*.md`, `commands/**/*.md`, `.claude/**`, or `.context/**` for mandatory security-team review — independent of D8.

**OWNER:** STRIDE/security → eng-architect (D8 Detector Specification extension); requirements → nse-requirements (REQ-052 extension)

---

### IN-006-it006s013: D7 Monitor Fail-Closed Coverage Incomplete [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption (FM-033 false-closed scenario coverage) |
| **Section** | ADR-003 D7; STRIDE SC-05; REQ-035 fail-closed AC |
| **Strategy Step** | Step 4 (stress-test FM-033 assumption) |

**Anti-goal framing:**
To guarantee the D7 monitor reports false-green while not actually checking, we need an internal error (not a tamper event) to cause the monitor to exit 0. Specifically: GitHub API rate limit → the `gh attestation verify` command returns a rate-limit error; the monitor catches it and... does what?

**Evidence:**
G-monitor acceptance criterion (iii) states: "an injected monitor error does NOT `exit 0`." This is present and correct. However, the synthetic tests specified are: (i) synthetic tip-tamper, (ii) simulated generation failure (stale tip), (iii) injected monitor error. The "injected monitor error" test is unspecified — what injection? The ADR-003 D7(c) section says "any non-zero exit / absent attestation / SHA mismatch / freshness gap / **internal monitor error**" — listing internal monitor error as a trigger. But the acceptance test doesn't enumerate what TYPES of internal errors must be tested.

**Missing coverage:**
- `gh` CLI not installed or updated (exits with non-zero but possibly different than expected)
- GitHub API rate limit (HTTP 429 from `gh api`)
- Network timeout (connection refused, DNS failure)
- Malformed API response (JSON parse error)
- `git ls-remote` returning unexpected output format
- `actions: write` permission revoked mid-run (auto-revert dispatch fails)

**Recommendation:**
Extend G-monitor acceptance criteria to require explicit testing of at least 4 distinct internal-error injection scenarios in addition to the synthetic tamper. The fail-closed test harness should mock each external dependency (GitHub API, `gh` CLI, `git ls-remote`) to simulate each failure mode and verify the monitor exits non-zero and opens a GitHub issue.

**OWNER:** STRIDE/security → eng-architect (SC-05 extension); requirements → nse-requirements (REQ-035 AC extension)

---

### IN-007-it006s013: G-Headroom Thresholds Not Derived From CoWork's Actual Ceiling [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption (R-001 ceiling dimension unverified) |
| **Section** | ADR-001 L2 §4; REQ-006 (multi-dimensional gate); R-001; Phase-5 gate G-headroom |
| **Strategy Step** | Step 3 (A-T1) and Step 4 |

**Anti-goal framing:**
To guarantee the skeleton fails to install on CoWork despite passing all internal CI gates, we need the CoWork ceiling to be based on a different metric than what the CI gates check. The CI gates are: (a) file count < 5,000, (b) pack size < 250 MB, (c) estimated clone time < 60 s. But the 250 MB and 60 s thresholds are derived from the ADR-001 Option B flip trigger — not from empirical CoWork ceiling data. If CoWork uses a 100 MB pack threshold, the skeleton could have a 180 MB pack and pass the CI gate while failing CoWork install.

**Evidence:**
ADR-001 L2 §4 states: "if CoWork instead counts a local working directory (`.venv` ≈ 24,636 files), branch-stripping is the wrong lever." The R-001 verification approach says "a file-count-only pass is INSUFFICIENT (FM-062/IN-001)" — correctly requiring multi-dimensional verification. But the multi-dimensional thresholds in REQ-006 (250 MB, 60 s) are set to match ADR-001's Option B flip trigger, not to match CoWork's actual enforcement dimensions.

**G-headroom as specified** requires "a direct CoWork plugin-install smoke test" — this is the live-CoWork dimension (d) that was previously subject to a deferral clause (PM-002, now removed). G-headroom is therefore well-designed but still pending.

**Inversion consequence:**
If G-headroom is executed with only the CI-internal metrics (a, b, c) but without the live CoWork smoke test (d), the gate passes despite the skeleton potentially failing real CoWork install. The PM-002 "MAY defer dimension (d)" clause has been removed, but the test still hasn't been run.

**Recommendation:**
1. G-headroom acceptance must include deliberately crafted test skeletons that slightly exceed each threshold to empirically confirm WHICH dimension(s) CoWork enforces.
2. Add to REQ-034/G-headroom: the test must include install attempts on a live CoWork instance with skeletons at (a) 5,001 files, (b) 251 MB pack, and (c) a simulated 61-second clone — to determine which triggers the CoWork rejection, not just whether the current skeleton passes.

**OWNER:** requirements → nse-requirements (REQ-034 + G-headroom extended test criteria)

---

### IN-008-it006s013: Org Marketplace Registration SLA Gap — Undefined Harm Window [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption (RTB-3 process-control completeness) |
| **Section** | ADR-003 RTB-3; REQ-043; REQ-047 |
| **Strategy Step** | Step 3 (A-P3) and Step 4 |

**Anti-goal framing:**
To guarantee that a rogue marketplace registration causes maximum harm, we need it to go undetected long enough for a significant fraction of org users to install the malicious plugin. The current control is: "org audit-log webhook SHALL alert on CoWork marketplace-settings changes (near-real-time)." But "near-real-time" detection with no defined response SLA means harm duration depends entirely on how quickly a human responds to the webhook alert — which could be hours or days on weekends or during off-hours.

**Evidence:**
ADR-003 RTB-3: "A single compromised org-owner can re-register to a rogue/typosquat repo; the two-admin rule does not stop the action, and harm occurs in the detection window before the webhook/verification surfaces it." REQ-047 specifies the webhook + ≤monthly manual verification but does NOT specify a response SLA or a maximum acceptable harm duration.

**Inversion consequence:**
If org-registration is tampered at 5pm Friday, the webhook fires, a GitHub issue is created — but no human responds until Monday morning. Over that weekend, every new CoWork session for every org user that updates their plugin receives malicious hooks. The number of affected users scales with the detection window.

**Recommendation:**
1. ADD to REQ-047: a named incident responder with a defined SLA for acting on the webhook alert (e.g., "the named org-admin-on-call must re-register to the canonical repo within 2 hours of the webhook firing, 24/7").
2. ADD to the org-registration runbook: a verification script that checks the currently registered marketplace source matches `geekatron/jerry-cowork` — runnable by any team member as a spot-check.
3. Define the "canonical repo full name" as an immutable constant in the Jerry org documentation, committed to `main`, so re-registration requires no judgment call.

**OWNER:** requirements → nse-requirements (REQ-047 + SLA extension); ADR → ps-architect (ADR-003 RTB-3)

---

### IN-009-it006s013: Option A → Option B Flip Requires Manual Human Action [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Assumption (A-Tm2 — slow-growing risk) |
| **Section** | ADR-001 Clone-Weight Decision; Consequences §Negative 1 |
| **Strategy Step** | Step 4 (stress-test A-Tm2) |

**Anti-goal framing:**
To guarantee that clone weight quietly exceeds the 60s / 250 MB trigger without human action, we need the early-warning band alert (150 MB / 40s GitHub issue) to be opened but not acted upon — for example, during a period when the team is not actively monitoring the issue backlog.

**Evidence:**
ADR-001 Clone-Weight Decision table shows the early-warning band generates a GitHub issue. But a GitHub issue is only useful if someone reads and acts on it promptly. The one-line code change (Option B flip) requires a new release to take effect.

**Inversion consequence:**
Clone weight crosses the 150 MB early-warning band; a GitHub issue is opened; it sits in the backlog for several weeks; the repo continues releasing; weight crosses the 250 MB hard trigger; the next release CI hard-fails. At this point, the flip to Option B is urgent and reactive rather than proactive as intended. The integrity-neutral flip (post-IT3-004) is designed to be easy, but "easy" doesn't prevent it from being delayed.

**Recommendation:**
Consider automating the Option B flip as a GitHub Actions workflow that opens a PR with the one-line change when the early-warning band is reached, rather than just opening an issue. This makes the response actionable without human judgment.

**OWNER:** ADR → ps-architect (ADR-001 — future consideration)

---

### IN-010-it006s013: D8 Implementation Has No Tracked Delivery Story [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption (A-R1 — delivery dependency) |
| **Section** | ADR-003 D8 hand-off; STRIDE D8 Detector Specification; REQ-052 |
| **Strategy Step** | Step 3 (A-R1) and Step 4 |

**Anti-goal framing:**
To guarantee D8 is never implemented before go-live, we need the "mirror hand-off" from ADR-003 to eng-architect to remain an informal document instruction without a worktracker story, owner, or deadline. Without tracking, D8 is subject to the same delivery-pressure bypass as the Phase-5 gates (IN-003).

**Evidence:**
ADR-003 D8 states: "The concrete pattern catalog, detector tooling, and false-positive tuning are **handed off** (see below)." The Mirror Hand-Off section lists "eng-architect (STRIDE): owns the **pattern catalog and detector tool**" and "nse-requirements: owns the **binding SHALL**." The requirements have REQ-052, which creates the SHALL. But a SHALL in a requirements document does not automatically become a tracked implementation worktracker entity.

**Inversion consequence:**
D8 is the only technical control that inspects the markdown payload content (SC-08). If D8 is not implemented before Phase-5, the trusted-maintainer rogue-build path (SC-06/SC-08, 2×5=10, YELLOW) has zero technical controls — only human peer review (REQ-051), which RT-002 demonstrated is insufficient alone. G-content cannot pass if the scanner isn't built.

**Recommendation:**
1. Create a worktracker STORY under PROJ-031 (or the appropriate parent work item) for D8 implementation with: owner = eng-architect, deliverables = (pattern catalog committed to source repo, scanner tool SHA-pinned in workflow, G-content synthetic test passing), and a deadline that makes it a dependency of Phase-5.
2. REQ-052 should link to this story so the requirements trace is complete.
3. The ADR-003 Mirror Hand-Off should reference the story ID as the tracked delivery artifact.

**OWNER:** requirements → nse-requirements (REQ-052 + story link); STRIDE/security → eng-architect (story creation)

---

## Execution Statistics

- **Total Findings:** 10
- **Critical:** 3 (IN-001, IN-002, IN-003)
- **Major:** 6 (IN-004, IN-005, IN-006, IN-007, IN-008, IN-010)
- **Minor:** 1 (IN-009)
- **Protocol Steps Completed:** 6 of 6
- **Goals Analyzed:** 8 (G-1 Installability, G-2 Auto-Sync, G-3 Integrity, G-4 Security Posture, G-5 Phase-5 Gates, G-6 Governance, G-7 No False Confidence, G-8 [implicit] CoWork update propagation)
- **Assumptions Mapped:** 18 (A-T1..T12, A-P1..P6, A-R1..R2, A-E1..E6, A-Tm1..Tm3)

---

## Scoring Impact (S-014 Dimensions)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | **Negative** | IN-001: headline value ("automatically in sync") contingent on unverified assumption with no concrete fallback path specified; IN-002: D5 (required provenance control) unimplemented; IN-010: D8 (required content gate) untracked |
| Internal Consistency | 0.20 | **Negative** | IN-003: Phase-5 gates are "non-deferrable" by process rule but technically deferrable in practice; IN-004: RTB-1 combined-attack analysis is missing while RTB-1 individual-actor analysis is present — creates a false completeness signal |
| Methodological Rigor | 0.20 | **Negative** | IN-005: D8 allow-list bloat not analyzed as a systematic failure mode; IN-006: FM-033 fail-closed requirement underspecified for internal error types; IN-007: G-headroom thresholds derived from ADR-001 flip trigger, not CoWork's actual ceiling |
| Evidence Quality | 0.15 | **Neutral–Positive** | The Claim-Status Convention is well-applied; "designed vs validated" distinction is consistently maintained; explicit P-022 honesty throughout; slight negative from IN-002 (FM-032 evidence present but gap not elevated to implementation priority) |
| Actionability | 0.15 | **Negative** | IN-003: Phase-5 authorization checklist lacks technical enforcement mechanism; IN-010: D8 has a binding SHALL but no tracked delivery path; IN-008: webhook SLA undefined |
| Traceability | 0.10 | **Slightly Negative** | ADR→STRIDE→REQ trace is generally strong; gap at IN-002 (no STORY for D5 implementation) and IN-010 (no STORY for D8 implementation) |

---

## Recommendations Summary

### Critical — MUST mitigate before go-live

| Finding | Action | OWNER |
|---------|--------|-------|
| IN-001-it006s013 | Execute G-update on live CoWork with already-installed plugin; define concrete contingency path (update mechanism OR re-scoped STK-002); user approval required (P-020) before go-live | nse-requirements (OQ-048); ps-architect (ADR-001) |
| IN-002-it006s013 | Create tracked STORY for D5 implementation (REQ-038 + REQ-039); make D5 a deployment pre-requisite with CI enforcement; G-provenance synthetic test before Phase-5 | ps-architect; eng-architect |
| IN-003-it006s013 | Add `phase5-gate-evidence.md` file requirement committed via reviewed PR before org-registration runbook executes; include CI run IDs for all 6 gates | nse-requirements (Phase-5 checklist); ps-architect |

### Major — SHOULD mitigate before go-live

| Finding | Action | OWNER |
|---------|--------|-------|
| IN-004-it006s013 | Extend ADR-003 RTB-1 with combined-attack analysis; add external (non-GitHub) out-of-band alert for ruleset changes | eng-architect (STRIDE) |
| IN-005-it006s013 | Add max allow-list size (≤20 entries), quarterly review requirement, second independent technical control on SC-06 path | eng-architect; nse-requirements |
| IN-006-it006s013 | Extend G-monitor acceptance criteria to cover ≥4 internal error injection scenarios (API rate limit, CLI absent, network timeout, malformed response) | eng-architect; nse-requirements (REQ-035) |
| IN-007-it006s013 | G-headroom test must include synthetic skeletons exceeding each threshold independently to empirically confirm which dimension CoWork enforces | nse-requirements (REQ-034) |
| IN-008-it006s013 | Add incident-response SLA to REQ-047; define on-call org-admin role with time-to-respond requirement | nse-requirements (REQ-047) |
| IN-010-it006s013 | Create worktracker STORY for D8 implementation owned by eng-architect; link REQ-052 to story; make story a Phase-5 dependency | nse-requirements; eng-architect |

### Minor — MAY mitigate

| Finding | Action | OWNER |
|---------|--------|-------|
| IN-009-it006s013 | Automate the Option B flip PR when the early-warning band (150 MB / 40 s) is reached | ps-architect (ADR-001, future) |

---

*Report generated by: adv-executor (adv-executor v1.0.0)*
*Strategy: S-013 Inversion Technique v1.0.0*
*Tournament: PROJ-031 iteration-006 Group E*
*Self-review: H-15 applied — all findings have specific evidence, severity is justified, IN-NNN identifiers follow template prefix format, summary table matches detailed findings, no findings minimized*
