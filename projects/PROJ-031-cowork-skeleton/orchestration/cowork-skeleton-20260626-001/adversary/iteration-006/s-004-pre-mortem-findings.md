# Pre-Mortem Report: PROJ-031 CoWork Skeleton Distribution

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** 5 design artifacts — ADR-001, ADR-003, phase1-requirements.md, phase2-stride-threat-model.md, phase2-attack-surface.md (historical recon)
**Criticality:** C4
**Date:** 2026-06-29T00:00:00Z
**Reviewer:** adv-executor (blind, iteration-006 Group C)
**H-16 Compliance:** S-003 Steelman confirmed present in prior strategy outputs (iteration-006 Group B); H-16 satisfied.
**Failure Scenario:** It is June 2027. The PROJ-031 CoWork skeleton distribution has failed in production. The composite failure: (a) multiple users are silently running a stale Jerry skeleton from their install date because CoWork caches the plugin at install and never propagated updates; (b) a rogue v* tag shipped malicious hooks before D5 provenance controls were implemented; (c) a freshness-check silent-failure left users on a known-buggy skeleton for 23 days. Each failure was traceable to a designed-but-unvalidated control that was deferred under delivery pressure or a monitoring path that exited 0 when it should have exited non-zero.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Failure Scenario Declaration](#failure-scenario-declaration) | Temporal perspective shift — analyzing from the retrospective frame |
| [Findings Summary](#findings-summary) | All 8 findings by priority |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, remediation per finding |
| [Recommendations](#recommendations) | Prioritized mitigation plan (P0/P1/P2) |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Counts and protocol completion |

---

## Failure Scenario Declaration

**Step 2 (Temporal Perspective Shift):** It is June 2027. The PROJ-031 CoWork skeleton distribution launched in Q4 2026. We are now conducting a retrospective investigation. We are NOT predicting failure — we are explaining it after the fact.

The declared failure manifests across three independently observable symptoms:

1. **Stale distribution (most widespread harm):** A critical security fix shipped in Jerry v0.35.0 never reached users who installed the plugin before that release. CoWork caches the plugin tree at install and refreshes only on explicit user reinstall — a behavior that was explicitly listed as an "unverified load-bearing assumption" (ADR-001 L2 §6, PM-001/CV-001) but whose empirical verification gate (G-update) was treated as deferrable.

2. **Rogue skeleton shipped (most severe harm):** A compromised collaborator account pushed `v99.1.0` pointing at a malicious commit. The D5 provenance assertion (`git merge-base --is-ancestor`) existed in the design (ADR-003 D5, REQ-038) but was never implemented in the live pipeline — FM-032 had been open for months. The first D8 content-safety attempt blocked the payload; the second, subtler attempt evaded the static pattern catalog.

3. **Silent staleness undetected for 23 days:** A breaking API change in the GitHub CLI broke the freshness check in the D7 monitor, which then exited 0 silently instead of failing closed — the FM-033 "silent-exit-0" failure mode that REQ-035 explicitly prohibits. The meta-monitor (REQ-044) saw "successful run" and never alerted.

Working backward: all three traces lead to controls that were **designed but not validated** (per the Phase-2 Claim-Status Convention) and gates that were reclassified from "hard blockers" to "monitored risks" under delivery pressure.

---

## Findings Summary

| ID | Severity | Finding | Category | Likelihood | Priority | Affected Dimension |
|----|----------|---------|---------|------------|---------|-------------------|
| PM-001-I006 | Critical | G-update gate deferred: users silently stranded on install-time skeleton version forever | Assumption | High | P0 | Completeness |
| PM-002-I006 | Critical | D5 provenance gate designed-not-implemented at go-live: rogue-tag CI self-certification window stays open | Process | High | P0 | Methodological Rigor |
| PM-003-I006 | Critical | Org-marketplace webhook endpoint becomes stale: silent re-registration undetected for weeks | External/Process | Low | P1 | Methodological Rigor |
| PM-004-I006 | Major | D7 monitor silent-exits 0 on unhandled CLI error: freshness failure invisible to meta-monitor | Technical | Medium | P1 | Internal Consistency |
| PM-005-I006 | Major | Clone-weight dimensions (b)(c) deferred from multi-dimensional gate: install breaks at month 10 | Technical | Medium | P1 | Completeness |
| PM-006-I006 | Major | D8 allow-list creep over operational lifetime bypasses content-safety gate | Resource/Process | Medium | P1 | Actionability |
| PM-007-I006 | Major | G-prevention bypass-actor semantics never confirmed on live ruleset before go-live | Process | Low | P2 | Evidence Quality |
| PM-008-I006 | Minor | REQ-010 agent-path glob too shallow: new nested agent structures silently absent from skeleton | Technical | Low | P2 | Completeness |

---

## Detailed Findings

### PM-001-I006: G-update Gate Deferred — Users Stranded on Install-Time Skeleton Forever [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR-001 L2 §6 (PM-001/CV-001); ADR-003 Phase-5 Validation Gate Set (G-update); REQ-054 / OQ-048; STK-002 |
| **Strategy Step** | Step 3 — Assumption Failure category lens |

**Evidence:**
ADR-001 L2 §6 states verbatim: "The promise that the skeleton is 'automatically in sync when a new Jerry ships' ... assumes that **updating the dedicated repo's default branch propagates to ALREADY-INSTALLED users.** Only CoWork's *install-time* behavior is confirmed... its **update** behavior for existing users is an **unexamined black box.** ... **Per P-022 this ADR does NOT assert that sync works for already-installed users — it is explicitly an unverified, load-bearing assumption.**"

The Phase-5 Authorization Checklist (ADR-003, consolidated in requirements §Phase-5 Authorization Checklist) names G-update: "a force-push to `geekatron/jerry-cowork` reaches an already-installed user's session within a documented window; **OR** a manual update procedure is documented and the 'automatically in sync' claim is re-scoped." STK-002 in the requirements is explicitly marked: "automatically in sync ... **contingent on G-update being verified (REQ-054 / OQ-048)**."

ADR-001 Risks table: "CoWork does NOT propagate updates to already-installed users | MED | HIGH (every user silently runs a stale Jerry; new skills/agents referenced by H-22 don't exist)."

**Analysis:**
The failure chain: the G-update gate was listed as a hard blocker in the Phase-5 Authorization Checklist, but it requires access to a live CoWork-compatible client and an already-installed user session — conditions that are difficult to synthesize in a CI/test environment. Under delivery pressure, the team accepted a written procedure as a substitute for empirical proof. This is the canonical "the gate set existed on paper but was bypassed" failure mode the task prompt explicitly asks Pre-Mortem to surface.

If CoWork (consistent with common plugin-host behavior) caches the plugin tree at install and refreshes only on explicit reinstall or a user-initiated "check for updates," then every user runs the skeleton from their first install date. The CI regeneration pipeline works perfectly; the last-mile CoWork→session propagation is the unvalidated gap. A critical security fix in Jerry v0.35.0 (shipped 4 months post-launch) never reaches existing users. H-22 (mandatory skill invocation) references new skills that do not exist in installed skeletons. STK-002 ("automatically in sync") is false for every user from day one.

This is the **single most plausible failure the current design does not adequately guard against**, because the entire distribution value proposition (STK-002) rests on an assumption that is explicitly unverified and cannot be tested without live CoWork infrastructure.

**Missing / Insufficient Control:**
G-update is declared a hard Phase-5 blocker in the authorization checklist (REQ-054 / OQ-048), but the requirements do not specify what constitutes acceptable empirical proof, who owns the live-client test environment, or what the fallback is if the test reveals caching. The "OR a manual update procedure is documented" escape hatch could be used to satisfy the gate without verifying the assumption — which is precisely the bypass risk.

**Recommendation:**
1. Add a concrete acceptance criterion to REQ-054: the empirical test MUST be performed on a **real CoWork-compatible client with an already-installed plugin** (not a fresh install or a synthetic test), and the result MUST be either (a) confirmed propagation within a bounded window (document the window), or (b) confirmed caching with a documented, user-facing manual update procedure shipped as WS-4 documentation before go-live.
2. The "automatically in sync" claim (STK-002, L0 summary) MUST be scoped precisely in all user-facing documentation before go-live — either confirmed or replaced with "requires manual reinstall to receive updates."
3. G-update MUST NOT be satisfied by documentation or design analysis alone — only empirical testing on a live client counts.
4. OWNER: nse-requirements (tighten REQ-054 acceptance criterion; add ownership of live-client test environment to G-update gate spec).

---

### PM-002-I006: D5 Provenance Gate Designed-Not-Implemented at Go-Live — Rogue-Tag Window Stays Open [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR-003 D5; STRIDE SC-02; REQ-038/REQ-039; FM-032 |
| **Strategy Step** | Step 3 — Process Failure category lens |

**Evidence:**
ADR-003 D5 states: "**Status: Designed — operational validation pending [G-provenance] (FM-032).** Both legs (REQ-038 ancestor assertion, REQ-039 `v*` tag-protection ruleset) are **specified but NOT yet implemented.** Until **G-provenance** proves them on the live pipeline..., the rogue-tag self-certification path (SC-02) **remains open through Phase-5.**" ADR-003 continues: "this is an explicit **Phase-5 blocker** — go-live MUST NOT proceed with D5 in designed-only status."

STRIDE Consolidated Threat Register ranks SC-02 as Rank 1 (2×5=10, YELLOW), disposition "STILL-NEEDED." ADR-003 Phase-5 Authorization Checklist: "G-provenance: a non-ancestor tag → non-zero exit, no attestation, no push; arbitrary v* tag creation is denied (FM-032 / SC-02)."

REQ-038 and REQ-039 are listed as "Status: Draft" in the requirements. They have no acceptance test in the CI suite at the time of writing — confirmed by the absence of any test for "non-ancestor tag → non-zero exit" in the WS-3 section's acceptance criteria table.

**Analysis:**
The failure chain: SC-02 (rogue-tag CI self-certification) is the top-ranked threat in the STRIDE model. It is explicitly designed to be blocked by D5 (tag-on-main provenance assertion + v* tag protection), but D5 is "designed, not implemented" (FM-032). The Phase-5 G-provenance gate is supposed to enforce this before go-live. Under delivery pressure, the team interprets "designed-not-implemented" as "we have the plan, implementation is trivially short." The git merge-base check is 3 lines of bash — easy to add "in a follow-up sprint." That sprint never happens before go-live because there is no CI gate that blocks deployment when REQ-038/REQ-039 are unimplemented.

A collaborator account is compromised 5 months post-launch. The attacker pushes `v99.1.0` pointing at a commit off `main`. CI checks out the tag, runs the provenance assertion... which is absent from the pipeline. CI faithfully builds, runs D8 (which blocks the first injection attempt), but the attacker makes a second attempt with subtler phrasing (a C5/C6-class payload that evades the current pattern catalog). CI attests the tree, force-pushes to the dedicated repo, and publishes the immutable release. D7 monitor returns PASS (the attestation matches what CI built — it faithfully certified the rogue build). Every org user receives the malicious skeleton.

The "blocking go-live" language exists in the design but has no enforcement mechanism in the requirements — no CI gate, no explicit workflow condition that refuses to proceed unless D5 is implemented and G-provenance has passed.

**Missing / Insufficient Control:**
The Phase-5 Authorization Checklist (ADR-003) lists G-provenance as a hard blocker. However, the requirements do not include a CI check that verifies the provenance assertion is present and active in the pipeline before deploying to production. Without an automated guard, the gate is only as strong as the team's discipline under pressure.

**Recommendation:**
1. Add a PRE-RELEASE CI check that asserts the D5 provenance gate code (`git merge-base --is-ancestor`) is present in `cowork-skeleton.yml` before any release can proceed. This is a lint/grep check, not a runtime test — it prevents accidental omission.
2. Add a mandatory CI test in `cowork-skeleton.yml`'s own test suite (triggered on `push` to `main`) that: (a) creates a synthetic non-ancestor tag, (b) attempts to build the skeleton from it, and (c) asserts the workflow exits non-zero with no push. This transforms G-provenance from a one-time Phase-5 gate into a continuously-enforced property.
3. REQ-038's acceptance criterion should be added to the main `ci.yml` regression suite, not only to a one-time Phase-5 validation.
4. OWNER: eng-architect (owns the implementation spec for the pipeline check); nse-requirements (owns REQ-038 with the additional pre-release lint-check requirement).

---

### PM-003-I006: Org-Marketplace Webhook Endpoint Becomes Stale — Silent Re-Registration Undetected [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR-003 RTB-3; REQ-043; REQ-047; Phase-5 Authorization Checklist |
| **Strategy Step** | Step 3 — External/Process Failure category lens |

**Evidence:**
ADR-003 RTB-3 states: "REQ-043's 'two-admin approval for any registered-source change' has **no GitHub-native technical enforcement** — CoWork's org marketplace registration is a single-actor server-side setting. It is therefore a **process control, not a prevented state.**" REQ-047 specifies: "An org audit-log webhook SHALL alert on CoWork marketplace-settings changes (near-real-time)..." and: "A ≤ 24 h automated-polling monitor is **descoped as unactionable** — GitHub exposes no documented API endpoint for the org's registered CoWork source (CV-006/DA-006)."

The Risks table in ADR-003: "Org-admin registers rogue/typosquat repo (OR-01/02/V-08) | LOW-MED | HIGH." The STRIDE model Consolidated Threat Register ranks OR-01 and OR-02 at Rank 3 and 4 (both 2×5=10, YELLOW).

The sole automated detection is REQ-047's webhook. The sole periodic check is "≤ monthly manual verification against the canonical geekatron/jerry-cowork." There is no acknowledgment that the webhook endpoint itself must be monitored for liveness.

**Analysis:**
The failure chain: RTB-3 acknowledges the org-registration control is detect-and-respond, not prevent. The detection mechanism (REQ-047 audit-log webhook) requires a live, reachable endpoint. The ≤ monthly manual verification is the backstop. However:

1. The webhook endpoint hosting is not governed by the same operational standards as the main pipeline. If the endpoint is hosted on an ephemeral platform (free-tier hosting, a developer's personal server), it can become unreachable without any monitoring.
2. The meta-monitor (REQ-044) monitors whether the D7 monitor ran successfully. It does NOT monitor whether the REQ-047 webhook is alive.
3. There is no "webhook liveness" check in the monitoring architecture.
4. The ≤ monthly manual verification window means up to 30 days of undetected re-registration.

Failure scenario: an org owner account is compromised. The attacker re-registers the marketplace from `geekatron/jerry-cowork` to a lookalike repo. The REQ-047 webhook fires, but the webhook endpoint is sleeping (or was silently decommissioned when the developer who owned it left the team 3 months earlier). The D7 integrity monitor checks the attestation for `geekatron/jerry-cowork`'s tip — which still passes, because the legitimate repo is intact. The D7 monitor does NOT check what CoWork marketplace source is registered. Users receive the attacker's plugin. The next monthly manual check is 18 days away.

**Missing / Insufficient Control:**
The design acknowledges this residual (RTB-3) but does not specify: (a) who owns the webhook endpoint's operational liveness, (b) how the webhook endpoint is monitored for reachability, or (c) a fallback detection path if the webhook endpoint is unavailable. The ≤ monthly manual verification is the only backstop, and its cadence is insufficient for a CRITICAL-consequence path.

**Recommendation:**
1. Add explicit ownership and liveness monitoring of the REQ-047 webhook endpoint to the operational runbook — the endpoint must be treated as a security-critical component, not an afterthought.
2. Add a weekly (not monthly) registered-source verification for the first 6 months post-launch, tightening to monthly only after operational stability is confirmed.
3. Add a "webhook reachability check" to the D7 monitor's meta-monitor (REQ-044) scope: if the REQ-047 webhook endpoint is unreachable for >48 h, open a GitHub issue.
4. Consider publishing the canonical repo URL in a cryptographically-verifiable location (e.g., a signed git tag or the attestation metadata) so a user can independently verify the expected source even without the webhook.
5. OWNER: ADR → ps-architect (expand RTB-3 with webhook liveness governance); nse-requirements (add webhook-liveness REQ and tighter verification cadence for initial launch period).

---

### PM-004-I006: D7 Monitor Silent-Exits 0 on Unhandled CLI Error — Freshness Failure Invisible to Meta-Monitor [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 D7(c); REQ-035 (fail-closed); REQ-044 (meta-monitor); FM-033; G-monitor gate criterion (iii) |
| **Strategy Step** | Step 3 — Technical Failure category lens |

**Evidence:**
ADR-003 D7(c): "**Fail-closed — never silently exit 0 (FM-033).** The monitor SHALL treat **any** verification error — non-zero `gh attestation verify` exit, absent attestation, SHA mismatch, freshness gap, OR an **internal monitor error** (network failure, missing tool, unparseable output) — as a **tamper/failure trigger**: open a GitHub issue **and** exit non-zero. A monitor that cannot complete its check MUST NOT report success; an unhandled error path that `exit 0`s is the FM-033 silent-failure mode (RPN 288) and is explicitly forbidden."

G-monitor gate criterion (iii): "an injected monitor error does **not** `exit 0`." REQ-035 fail-closed AC: "any non-zero exit / absent attestation / mismatch / freshness gap / **internal monitor error** SHALL open an issue AND exit non-zero." REQ-044 meta-monitor: "A meta-monitor SHALL alert if the integrity backstop monitor has not completed **successfully** within 25 h."

The key risk: if the main monitor exits 0 due to an internal error (the FM-033 failure mode), the meta-monitor interprets this as "completed successfully" and does NOT alert. The meta-monitor is designed to catch "no run in 25 h," not "run that silently misreports success."

**Analysis:**
The failure chain: The D7 freshness check (REQ-049) calls `git ls-remote --tags geekatron/jerry` to get the latest v* tag. The GitHub CLI tool (`gh`) used in this check is pinned to a SHA per REQ-017 — for the Actions step that invokes `gh`. However, if `gh` is invoked as a shell command (not as a GitHub Action), it may use the runner's bundled version, which is NOT SHA-pinned. A runner image update upgrades the bundled `gh` CLI to a version with a breaking API change. The freshness check's argument parsing fails with an unhandled exception at the bash level. The monitor's error-handling catches the `git ls-remote` failure but not the downstream CLI parse error (the catch block only covers the attestation-verify path, not the freshness-check path). The freshness check function returns 0 (the default bash function exit). The monitor reports "freshness: OK" when it actually never checked.

The meta-monitor sees "successful run" (exit 0) and does NOT alert. A CI failure left `geekatron/jerry-cowork` at `vN-1`'s skeleton. Users run the stale skeleton for 23 days until the next successful release regenerates it.

**Missing / Insufficient Control:**
The G-monitor gate criterion (iii) requires testing that "an injected monitor error does not exit 0." This test was performed for the attestation-verify path but not for the freshness-check path (two distinct code paths). The requirement for fail-closed behavior applies to both, but the acceptance test was underspecified — it tested one injection point, not all injection points.

**Recommendation:**
1. REQ-035's fail-closed acceptance criterion must specify that the negative-path test covers EACH code path independently: (a) attestation-verify failure, (b) freshness-check failure (CLI error, parse error, network timeout), (c) meta-infrastructure failure (can't read `geekatron/jerry-cowork` tip SHA). One synthetic-tamper injection per path.
2. The meta-monitor (REQ-044) should additionally alert when the monitor exits 0 but produced no attestation-verify result (i.e., the monitor ran but its output is absent or unparseable). This catches the "successfully did nothing" failure mode.
3. The `gh` CLI invocation in the freshness check must be version-pinned (either as a versioned tool in `uv` or as a specific `gh` binary version) — not relying on the runner's bundled version.
4. OWNER: eng-architect (implementation spec for multi-path fail-closed testing); nse-requirements (expand REQ-035 acceptance criteria to enumerate all code paths requiring negative-path testing).

---

### PM-005-I006: Clone-Weight Dimensions (b)(c) Deferred from Multi-Dimensional Gate — Install Breaks at Month 10 [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-001 Consequences Negative §1 (continuous monitoring); REQ-006 (multi-dimensional gate); REQ-034d (per-release telemetry); ADR-001 L2 §4 (unverified 5,000-file limit) |
| **Strategy Step** | Step 3 — Technical/Operational Decay category lens |

**Evidence:**
REQ-006 states: "The skeleton generation script SHALL perform a **multi-dimensional** gate... and SHALL exit non-zero if ANY of the following hard-fail conditions is not satisfied: (a) tracked file count < 5,000; (b) compressed pack size < 250 MB; (c) estimated reference-network clone duration does not exceed 60 s... A file-count-only gate cannot falsify a size/time-based CoWork ceiling (FM-062/IN-001)."

ADR-001 Consequences Negative §1: "Clone weight under full provenance grows MONOTONICALLY — `fetch-depth: 0` carries `main`'s history into the skeleton `.git`, and every release adds to it (~2 MB/release empirically)... the R-001 artifact records the baseline pack size + clone time, AND `cowork-skeleton.yml` emits per-release weight (hard-fail at > 250 MB), AND the continuous integrity workflow records weight every cycle with an **early-warning band (~150 MB / ~40 s, ≈60% of trigger)**."

The acceptance criterion for REQ-006: "(b) Inject large blobs to push pack-size above 250 MB; confirm script exits non-zero and branch is NOT updated. (c) Simulate estimated clone time exceeding 60 s; confirm script exits non-zero."

**Analysis:**
The failure chain: REQ-006 clearly specifies three dimensions. However, implementing dimensions (b) and (c) requires: (b) measuring git pack size in the CI runner and comparing against a threshold, plus the early-warning issue-opening logic; (c) measuring clone time in CI, which requires a separate timed clone step against a reference network simulation. Both are non-trivial to implement accurately in a standard CI runner. Under delivery pressure and with the file count well under the ceiling at launch (~1,417 vs 5,000), dimensions (b) and (c) of REQ-006 are deprioritized as "we have massive headroom on file count, the other dimensions are academic." The per-release weight emit (REQ-034d) is implemented, but the early-warning issue-opening step (which requires opening a GitHub issue at ~150 MB) is not implemented — only the hard-fail condition is partially implemented.

At month 10, with ~50 releases at ~2 MB/release, the pack size has grown to ~260 MB, exceeding the 250 MB hard-fail threshold. New users installing the plugin experience 65+ second clone times (CoWork's 120-second timeout is not exceeded, but network variability occasionally trips it). The per-release hard-fail gate (dimension b) should have blocked the release at month 9 (~250 MB), but because dimension (b) was never implemented in the generation script, the release proceeds. Dimension (c) was similarly absent.

**Missing / Insufficient Control:**
REQ-006 dimensions (b) and (c) are specified but the acceptance criteria tests them only in principle ("Inject large blobs to push pack-size above 250 MB") — there is no pre-release CI check that continuously monitors whether the implementation is present and correctly implemented. The early-warning band (150 MB / 40 s) exists only in ADR-001's design prose, not in a concrete requirement with a monitoring owner.

**Recommendation:**
1. REQ-006 acceptance criteria must include a concrete CI test that verifies dimensions (b) and (c) are IMPLEMENTED (not just specified): a CI lint step that greps `cowork-skeleton.yml` for the pack-size comparison and clock-time measurement code, and a test injection that verifies each path.
2. The early-warning band (150 MB / 40 s) must be converted from ADR-001 prose into a numbered requirement (proposed: REQ-034e) with an explicit owner (nse-requirements) and a monitoring mechanism (GitHub issue opened automatically by the monitor, not requiring a human to read the GITHUB_STEP_SUMMARY).
3. OWNER: nse-requirements (add REQ-034e for early-warning band as a formal requirement; update REQ-006 acceptance criteria to mandate implementation-presence checks).

---

### PM-006-I006: D8 Allow-List Creep Over Operational Lifetime Bypasses Content-Safety Gate [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | STRIDE D8 Detector Specification (False-positive handling); ADR-003 D8; REQ-052; REQ-051 |
| **Strategy Step** | Step 3 — Resource/Process Failure (lifecycle decay) category lens |

**Evidence:**
The STRIDE D8 Detector Specification (phase2-stride-threat-model.md §D8) acknowledges false-positive risk: "Jerry's own legitimate corpus *discusses* prompt injection (this very threat model, `/adversary` strategy templates, red-team agent docs)." The false-positive handling specifies: "an explicit, **version-controlled, code-reviewed allow-list** keyed by `{file path + rule id + content hash}` — a hash-pinned exception so an approved benign match cannot silently widen to cover an altered line."

The allow-list mechanism relies on: (a) the content hash being file-level (or narrower), (b) every allow-list addition being code-reviewed under REQ-051's "markdown-instruction review step," and (c) the second-reviewer recommendation ("consider a second independent reviewer for PRs touching `skills/`/`commands/`/`.claude/`/`.context/`" — REQ-051 uses "consider," a SOFT tier obligation).

**Analysis:**
The failure chain: The Jerry adversary corpus legitimately contains pattern-catalog-triggering content — `skills/adversary/agents/adv-executor.md` discusses and reproduces prompt-injection examples as educational content. At launch, these are known-benign baselines. Over 12 months, the adversary corpus grows by ~40 new files. Each new file that triggers C1-C4 patterns requires an allow-list exception. After 18 allow-list additions across 6 PRs (each individually reasonable), a developer facing a 3-week backlog of falsely-blocked releases adds 4 exceptions in a single PR with a comment "these are all in our adversary corpus, obviously benign." The reviewer approves.

Two of the 4 exceptions use a file-path-level allow-list entry (not file-path + content-hash) because the specific line content changes frequently as the adversary templates are iterated. This silently creates a class-based bypass: any C1 match in those two files passes without the content-hash check. Three months later, a compromised maintainer account adds a prompt-injection line to one of those two files. D8 checks the file against the allow-list, finds the path-level exception, and passes the release.

**Missing / Insufficient Control:**
The STRIDE D8 Detector Specification requires "hash-pinned exception" but does not specify that path-level (without content-hash) exceptions are FORBIDDEN. REQ-051's second-reviewer recommendation is SOFT ("consider"), not SHALL. There is no annual review of the allow-list to prune stale or overly-broad exceptions.

**Recommendation:**
1. The allow-list format must explicitly FORBID path-only exceptions — every entry MUST include both file path AND content hash (at minimum line-level hash). This must be enforced by the scanner's allow-list validation step.
2. REQ-051's "consider a second independent reviewer" for PRs touching the retained surface should be promoted to SHOULD (MEDIUM tier) for allow-list additions specifically, given the security impact.
3. Add a mandatory semi-annual allow-list review as part of the operational runbook: any exception older than 6 months without a recent justification review is automatically re-enabled for blocking. This combats the accumulation dynamic.
4. Add a CI lint step that counts allow-list exceptions and opens a GitHub issue if the count exceeds a threshold (e.g., 10 exceptions), prompting a human review.
5. OWNER: eng-architect (owns the pattern catalog and allow-list format enforcement); nse-requirements (owns REQ-052 with addition of allow-list governance requirements).

---

### PM-007-I006: G-prevention Bypass-Actor Semantics Never Confirmed on Live Ruleset Before Go-Live [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 D2; Phase-5 Gate G-prevention; STRIDE DR-01; claim-status "Designed — operational validation pending [G-prevention]" |
| **Strategy Step** | Step 3 — Process Failure category lens |

**Evidence:**
ADR-003 D2: "This decision **is designed to convert** the Phase-1 direct-push Critical (old R-007b) **from detection to prevention-by-design** — but it is **not yet an achieved fact**. Per the Claim-Status Convention this control is **Designed — operational validation pending [G-prevention]**: `geekatron/jerry-cowork` does not exist, no ruleset is applied, and GitHub's **bypass-actor semantics on an org-level ruleset are recent (Sep 2025) and untested on this target**."

G-prevention gate: "(i) a write-collaborator direct push is **rejected**; (ii) the CI App/deploy-key push **succeeds**; (iii) a repository administrator **cannot** override the ruleset (DA-001 / IN-003)."

ADR-003 D2 notes the Sep 2025 feature recency of bypass-actor semantics and that they are "untested on this target." The dedicated repo `geekatron/jerry-cowork` does not yet exist in the design phase.

**Analysis:**
The failure chain: GitHub's org-level ruleset bypass-actor feature (GA Sep 2025) is specified but not yet proven to work exactly as ADR-003 D2 describes for the specific combination of: (a) an org-level ruleset (not a repo-level ruleset), (b) a GitHub App identity as the sole bypass actor, (c) a dedicated repo where the force-push target is the default branch. GitHub's ruleset documentation describes this capability in general terms; the specific interaction between org-level rulesets and default-branch force-push by an App bypass actor may have edge cases not covered by the documentation.

If G-prevention is never empirically tested (i.e., a write-collaborator direct push is never confirmed to be rejected), the architecture operates under an ASSUMED prevention posture rather than a confirmed one. Under delivery pressure, G-prevention is satisfied by: "We configured the ruleset correctly per the docs, and there are no known bugs." A month post-launch, a GitHub platform update changes the bypass-actor semantics for org-level rulesets in a subtle way (rule order evaluation changes). A write-collaborator who should be denied can now push directly. The D7 monitor detects this via attestation mismatch (the collaborator's push has no attestation) and triggers auto-revert within 6 h. But the malicious push was live for up to 6 h before detection.

**Missing / Insufficient Control:**
G-prevention passes the Phase-5 gate with a manual documentation check rather than an automated live rejection test. The gate's criterion (i) requires demonstrating that a write-collaborator direct push IS REJECTED — but "demonstrated" is not defined with sufficient precision to ensure it is re-tested after platform updates.

**Recommendation:**
1. G-prevention must include a re-test trigger: any change to the dedicated repo's ruleset OR any GitHub platform announcement about ruleset changes must trigger a re-run of the G-prevention acceptance test.
2. The G-prevention acceptance test should be automated as a quarterly scheduled job (or part of a periodic security review), not only a one-time Phase-5 gate.
3. OWNER: eng-architect (owns G-prevention test implementation); ps-architect (owns ADR-003 D2 claim — add re-test trigger language).

---

### PM-008-I006: REQ-010 Agent-Path Glob Too Shallow — New Nested Agent Structures Silently Absent [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | REQ-010; ADR-001 Canonical Plugin-Retention Surface; plugin.json agent declarations |
| **Strategy Step** | Step 3 — Technical Failure category lens |

**Evidence:**
REQ-010: "The skeleton generation script SHALL verify that all agent-path entries declared in `.claude-plugin/plugin.json` resolve to existing files in the generated branch tree."

ADR-001 Canonical Plugin-Retention Surface: "all 88 agents resolve under `skills/*/agents/*.md` (confirmed against `plugin.json` `agents[]`)." The current agent structure is one level deep: `skills/{skill-name}/agents/{agent-name}.md`.

The acceptance criterion for REQ-010: "Every `path:` entry in `.claude-plugin/plugin.json` agent declarations resolves to a file present in `git ls-files` on `cowork-skeleton`."

**Analysis:**
The failure chain: A future Jerry skill introduces a sub-organization of agents: `skills/new-skill/agents/subgroup/agent.md`. The plugin.json is correctly updated to reference this path. However, the REQ-010 verification script was implemented using a glob pattern `skills/*/agents/*.md` (matching the existing convention), not by reading the actual plugin.json and checking each declared path against git ls-files. When a subsequent refactoring accidentally changes a git-rm pattern that strips `skills/new-skill/agents/subgroup/` (e.g., a shell glob expansion issue), the verification passes (the glob matches the old pattern) but the declared agent file is absent. CoWork loads the plugin but silently fails to load the missing skill.

**Missing / Insufficient Control:**
REQ-010's acceptance criterion correctly specifies checking "every `path:` entry in `plugin.json`" — if implemented correctly (reading plugin.json and checking each entry), this WOULD catch the issue. The risk is that the implementation uses a structural assumption (current agent depth) rather than the specification (plugin.json as the source of truth). The acceptance criterion does not verify that the implementation reads plugin.json directly vs. uses a glob assumption.

**Recommendation:**
1. REQ-010's acceptance criterion should be augmented to explicitly require that the verification reads `.claude-plugin/plugin.json` as input and performs an exact path check per declared agent — NOT a glob-based check. Add a test with a `plugin.json` that declares a nested path to verify the implementation handles it correctly.
2. OWNER: nse-requirements (update REQ-010 acceptance criterion to specify implementation approach).

---

## Recommendations

### P0 — Critical: MUST Mitigate Before Go-Live Authorization

**PM-001-I006 — G-update: empirical verification of CoWork update propagation**

Acceptance criteria: Before go-live, perform an empirical test on a live CoWork-compatible client: (a) install `geekatron/jerry-cowork` from an earlier skeleton release; (b) force-push a new release to `geekatron/jerry-cowork`; (c) observe whether the already-installed user's session reflects the new content within a documented time window WITHOUT manual reinstall. If the test reveals caching: (a) document a mandatory manual-update procedure for users; (b) re-scope STK-002 "automatically in sync" to "requires reinstall to receive updates"; (c) add the procedure to WS-4 documentation. Either outcome satisfies G-update; the gap is that the test has not been performed.

**PM-002-I006 — G-provenance: implement REQ-038/REQ-039 and add continuous CI regression test**

Acceptance criteria: (a) The generation script contains `git merge-base --is-ancestor "${TAG}^{commit}" origin/main` and exits non-zero + no-push on failure. (b) A CI test in the repo's main CI suite exercises this path with a synthetic non-ancestor tag and asserts non-zero exit. (c) A `v*` tag-protection ruleset is applied to the source repo restricting tag creation. (d) G-provenance passes: a live non-ancestor `v*` tag attempt is rejected with no attestation and no push.

### P1 — Important: SHOULD Mitigate Before or Shortly After Launch

**PM-003-I006 — Org-marketplace webhook: add webhook liveness monitoring and tighten verification cadence**

Acceptance criteria: (a) The REQ-047 webhook endpoint is monitored for liveness by the D7 meta-monitor (REQ-044 scope expanded). (b) The initial post-launch verification cadence is weekly for the first 3 months, tightening to monthly thereafter. (c) The operational runbook names an owner for the webhook endpoint and specifies a recovery procedure if it becomes unreachable.

**PM-004-I006 — D7 fail-closed: expand G-monitor negative-path testing to all code paths**

Acceptance criteria: REQ-035 acceptance criteria expanded to require negative-path injection testing for each code path: (a) attestation-verify failure → exit non-zero + issue; (b) freshness-check CLI error → exit non-zero + issue; (c) internal script error → exit non-zero + issue; (d) meta-monitor must alert when main monitor exits 0 but produces no attestation-verify result.

**PM-005-I006 — Clone-weight: implement REQ-006 dimensions (b) and (c) and early-warning band**

Acceptance criteria: (a) REQ-006 dimensions (b) (pack-size <250 MB) and (c) (clone-time <60 s) are implemented in `cowork-skeleton.yml` with hard-fail exit on violation. (b) Early-warning band (~150 MB / ~40 s) opens a GitHub issue when crossed. (c) A new REQ-034e requires this monitoring as a formal SHALL.

**PM-006-I006 — D8 allow-list: add governance controls and prohibit path-only exceptions**

Acceptance criteria: (a) The allow-list format requires file-path + content-hash (not path-only); the scanner validates this and rejects path-only entries. (b) A semi-annual allow-list review process is documented in the operational runbook with an explicit owner. (c) A CI lint step opens a GitHub issue when allow-list size exceeds 10 exceptions. (d) REQ-051 second-reviewer recommendation is SHOULD (not CONSIDER) for allow-list-touching PRs.

### P2 — Monitor: MAY Mitigate; Acknowledge Risk

**PM-007-I006 — G-prevention re-test trigger**

Acknowledge risk: G-prevention operates on recently-GA GitHub features (Sep 2025 bypass-actor semantics). Recommend: add a quarterly re-test of the acceptance criteria and a trigger for re-testing on any GitHub platform changelog entry mentioning ruleset or bypass-actor changes.

**PM-008-I006 — REQ-010 implementation-approach clarification**

Acknowledge risk: Minor quality gap. Recommend updating REQ-010 acceptance criterion to specify that the implementation reads plugin.json directly (not via glob) and add a test with a nested agent path to guard against implementation drift.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-001-I006 (G-update unverified assumption): the design explicitly leaves the headline value proposition (STK-002 "automatically in sync") as an unverified assumption with no fallback WS-4 documentation scoped to the caching scenario. PM-005-I006 (REQ-006 dimensions b/c deferred): the multi-dimensional gate is specified but the lifecycle of its enforcement is not contractually guaranteed. |
| Internal Consistency | 0.20 | Negative | PM-004-I006 (D7 fail-closed): ADR-003 D7(c) requires fail-closed on "internal monitor error" but the G-monitor acceptance test only covers one injection point. The fail-closed requirement is internally consistent but the test coverage is not. PM-007-I006 (G-prevention): the architecture claims "prevention-by-design" with consistent claim-status tagging, but there is no mechanism to re-validate this claim after platform updates. |
| Methodological Rigor | 0.20 | Negative | PM-002-I006 (D5 designed-not-implemented): the top-ranked threat (SC-02) has its primary control in "designed" status with no CI gate enforcing implementation before go-live. PM-003-I006 (webhook endpoint liveness): the process control architecture does not account for the operational decay of the webhook endpoint itself — a gap in the monitoring-of-monitoring chain. |
| Evidence Quality | 0.15 | Neutral | The design is extensively evidence-based and consistently cites sources. The Claim-Status Convention (P-022) is well-applied. The gaps identified are in operational lifecycle (not design reasoning). Evidence quality is strong for the design phase; operational evidence for post-go-live controls is inherently absent (by definition of Phase-2 status). |
| Actionability | 0.15 | Negative | PM-006-I006 (D8 allow-list creep): the allow-list governance is under-specified for operational lifecycle — no cadence review, no count threshold, no prohibition on path-only exceptions. Without these operational guardrails, the D8 gate degrades predictably over time. |
| Traceability | 0.10 | Positive | The design's traceability is strong: every finding above traces to a specific ADR decision, requirement number, STRIDE threat ID, or risk register entry. The Claim-Status Convention ensures designed controls are not mistaken for validated ones. The ADR→REQ traces and the mirror hand-off mechanisms are exemplary. Minor gap: no traceability from operational runbook items (webhook liveness, allow-list review cadence) back to formal requirements. |

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 3 (PM-001-I006, PM-002-I006, PM-003-I006)
- **Major:** 4 (PM-004-I006, PM-005-I006, PM-006-I006, PM-007-I006)
- **Minor:** 1 (PM-008-I006)
- **Protocol Steps Completed:** 6 of 6
- **Failure Categories Covered:** Assumption (PM-001), Process (PM-002, PM-004, PM-007), External/Process (PM-003), Technical (PM-004, PM-005, PM-008), Resource/Process (PM-006)
- **Focus per task prompt:** Operational/lifecycle decay findings — PM-003, PM-005, PM-006 are pure lifecycle-decay findings. "Gate set existed on paper but was bypassed" findings — PM-001 (G-update deferred), PM-002 (D5 designed-not-implemented, G-provenance bypassed under pressure), PM-004 (G-monitor negative-path testing underspecified).
- **H-15 Self-Review:** Completed. All findings have specific evidence from the deliverables. Severity classifications are justified. Finding identifiers follow PM-{NNN}-I006 format. Summary table matches detailed findings. No findings minimized.

---

*Strategy: S-004 Pre-Mortem Analysis*
*Template: .context/templates/adversarial/s-004-pre-mortem.md*
*Deliverables reviewed:*
*  - projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md*
*  - projects/PROJ-031-cowork-skeleton/decisions/ADR-003-credential-protection-supply-chain.md*
*  - projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md*
*  - projects/PROJ-031-cowork-skeleton/security/phase2-stride-threat-model.md*
*  - projects/PROJ-031-cowork-skeleton/security/phase2-attack-surface.md (historical recon)*
*Executed: 2026-06-29T00:00:00Z*
*Execution ID: I006*
*Blindness constraint: No files under adversary/ were read per tournament rules.*
