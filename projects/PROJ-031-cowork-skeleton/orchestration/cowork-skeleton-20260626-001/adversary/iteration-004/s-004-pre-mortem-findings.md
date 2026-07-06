# Pre-Mortem Report: CoWork Skeleton Distribution — ADR-001, ADR-003, phase1-requirements

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverables:** ADR-001, ADR-003, `requirements/phase1-requirements.md`
**Criticality:** C4
**Date:** 2026-06-29
**Reviewer:** jerry:adv-executor (Group C — Challenge, blind independent)
**H-16 Compliance:** S-003 Steelman was applied in a prior group before this blind assessment; this executor's BLINDNESS directive prevents reading prior adversary outputs, but H-16 ordering was the orchestrator's responsibility. Proceeding per task instructions.
**Failure Scenario:** It is December 2026. The CoWork skeleton distribution failed. Org users received either tampered executable hooks, an outdated skeleton, or a non-functional installation. The post-mortem team is working backward from confirmed failure to root causes.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Temporal Perspective](#temporal-perspective) | Declared failure and retrospective frame |
| [Findings Summary](#findings-summary) | All findings with severity, category, priority |
| [Detailed Findings](#detailed-findings) | Evidence, root cause, prevention gap for each Critical and Major finding |
| [Recommendations](#recommendations) | P0 / P1 / P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Counts and protocol completion |

---

## Temporal Perspective

**Step 2 — Declared Failure (Mitchell et al. prospective-hindsight framing):**

It is December 2026, six months after the Phase-2 decisions were finalized. The skeleton distribution failed spectacularly. One or more of the following actually happened:

- Malicious hooks reached every org user's workstation via a tampered dedicated-repo default branch.
- The skeleton was stale by three releases and users were running outdated Jerry.
- The plugin failed to install because the file count or pack size breached CoWork's ceiling.
- A `tests/`-stripped skeleton failed at first session start because a hook or CLI path depended on something that was in `tests/`.

We are now explaining why, working backward, in past tense.

---

## Findings Summary

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-iter004 | App private key leaked; attacker pushed tampered hooks inside the 24-hour detection window | External | Medium | Critical | P0 | Internal Consistency |
| PM-002-iter004 | Dedicated-repo org ruleset removed during repo migration; prevention silently became detection-only | Process | Medium | Critical | P0 | Methodological Rigor |
| PM-003-iter004 | Attestation verification silent-failed when GitHub feature was unavailable; monitor fell through to forgeable secondary anchor without alerting | Assumption | Medium | Major | P1 | Evidence Quality |
| PM-004-iter004 | Org-registration repointed to a typosquat repo by an over-permissioned admin; two-admin approval requirement had no technical enforcement | External | Medium | Critical | P0 | Completeness |
| PM-005-iter004 | tests/ strip broke CLI or hook at runtime; no post-strip functional validation in CI | Technical | Medium | Major | P1 | Methodological Rigor |
| PM-006-iter004 | Cross-repo sync silently stopped for three releases; no meta-monitor on the generation workflow itself | Process | Medium | Major | P1 | Completeness |
| PM-007-iter004 | File count in retained directories crept from 1,417 toward 5,000 between releases; no early-warning threshold; limit breached on release N | Technical | Low | Minor | P2 | Completeness |

---

## Detailed Findings

### PM-001-iter004: GitHub App Private Key Leaked — 24-Hour Tampered-Hook Window [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | External |
| **Likelihood** | Medium |
| **Priority** | P0 |
| **Section** | ADR-003 D3, c-208; REQ-041; NFR-006 |
| **Affected Dimension** | Internal Consistency |

**Failure Cause:**
The GitHub App private key — the project's single long-lived secret per ADR-003 c-208 — leaked through a misconfigured CI log step or a compromised runner. The attacker minted App installation tokens at will. Because the App identity is the sole bypass actor on `geekatron/jerry-cowork` (REQ-040/D2), the attacker pushed a skeleton containing modified `hooks/session-start.py` directly to the dedicated-repo default branch. No attestation was generated (the push did not go through `cowork-skeleton.yml`). The NFR-006 scheduled tamper-detection monitor ran 23 hours later and detected the SHA mismatch, but by then approximately 12% of org users had installed the malicious hooks.

**Evidence:**
- ADR-003 D3 designates the App private key as "the project's single long-lived secret" (c-208) mitigated by "storing it only in source-repo secrets with minimal access and a rotation policy."
- REQ-041 states App tokens are "short-lived (~1h, automatically rotated)" — but this refers to the MINTED TOKEN, not the PRIVATE KEY. The private key itself has no stated rotation cadence in any requirement.
- NFR-006's tamper-detection SLA is "≤ daily" — explicitly a 24-hour upper bound on detection.
- ADR-003 Risks table: "App private key / deploy key theft (CR-03/V-06) | LOW–MED | HIGH | ... rotation; short-lived App tokens; deploy-key confinement" — acknowledged but no requirement formalizes the rotation schedule.

**Root Cause:**
No requirement specifies a mandatory App private key rotation cadence (e.g., "SHALL be rotated at least every 90 days"). No requirement mandates anomalous-push detection: a push to `geekatron/jerry-cowork` that has no corresponding `cowork-skeleton.yml` workflow run should trigger an alert, but there is no such requirement. The 24-hour detection window is designed into NFR-006 and accepted as an SLA, but no mitigation reduces that window (e.g., more frequent monitoring, or an event-driven alert on any push to the dedicated repo that lacks an associated attestation).

**Prevention Missing from Requirements:**
1. No REQ for App private key rotation cadence (c-208 says "rotation policy" but no REQ formalizes the schedule).
2. No REQ for detecting pushes to `geekatron/jerry-cowork` that do not have an associated `cowork-skeleton.yml` run (unattested pushes).
3. No REQ to reduce the tamper-detection SLA below 24 hours for the critical case of a credential compromise.

**Recommendation:**
Add a requirement: "The App private key SHALL be rotated at least every 90 days and SHALL be rotated immediately upon any suspected exposure; a rotation runbook SHALL be documented alongside REQ-043." Add a second requirement: "The integrity backstop monitor SHALL alert within 1 hour of any push to `geekatron/jerry-cowork` default branch that has no associated build-provenance attestation in the immutable release for the current tag." This converts the 24-hour scheduled check into a near-real-time alert for the unattested-push case.

**Acceptance Criteria:**
A REQ exists for 90-day key rotation with a runbook. A REQ exists for near-real-time alerting on unattested pushes. The monitoring workflow AC demonstrates the 1-hour alert fires when a push occurs without a corresponding attestation.

---

### PM-002-iter004: Dedicated-Repo Org Ruleset Removed During Repo Migration [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | Process |
| **Likelihood** | Medium |
| **Priority** | P0 |
| **Section** | ADR-003 D2; REQ-040; ADR-003 Consequences §Negative-3 |
| **Affected Dimension** | Methodological Rigor |

**Failure Cause:**
Six months in, the org decided to reorganize its GitHub org structure and transferred `geekatron/jerry-cowork` to a new org (`geekatron-plugins`). Org-level rulesets are scoped to the originating org; they do NOT follow a repo during a cross-org transfer. The dedicated repo arrived in the new org without any branch protection. Any human with write access could now push to the default branch. The next adversarial push happened within 48 hours. The tamper-detection monitor (NFR-006/REQ-035) ran the next day and caught it, but the window had already delivered compromised hooks to users who installed during the gap.

**Evidence:**
- ADR-003 D2 states: "We will write-lock the dedicated repo's default branch with an org-level ruleset in which the CI identity is the SOLE push bypass actor, with ZERO human write collaborators, and which repo admins cannot override."
- ADR-003 Consequences §Negative-3: "A repo admin could toggle protection. Mitigation: org-level ruleset repo-admins cannot override, admin minimization, audit alert, attestation backstop."
- REQ-040 AC: "`gh api orgs/geekatron/rulesets` confirms an active non-overridable org-level ruleset targets `geekatron/jerry-cowork`" — this is a SETUP-TIME check, not a continuously enforced invariant.
- There is no REQ that says "the CI workflow SHALL verify the org-level ruleset is active on the dedicated repo before each push."

**Root Cause:**
REQ-040 is a CONFIGURATION requirement verified once at setup. No CI step before each skeleton push asserts the ruleset still exists and still has the CI identity as the sole bypass actor. No monitor watches the ruleset CONFIGURATION STATE. If the ruleset is removed (by migration, by an org admin override, or by GitHub platform changes to ruleset semantics), the deliverables have no mechanism to detect the loss of prevention until AFTER a malicious push occurs.

**Prevention Missing from Requirements:**
1. REQ-021 Phase-2 language says "pre-deploy verification SHALL confirm the org ruleset is active on the dedicated repo before each push" — but REQ-021 is marked "Superseded by REQ-040" and its pre-push check is not carried into REQ-040's text or its CI allocation.
2. No REQ for a scheduled ruleset-configuration monitor (distinct from the tip-SHA tamper monitor) that asserts the bypass-actor list and ruleset enforcement level have not changed.
3. No REQ for a recovery runbook covering "what happens when the dedicated repo is transferred."

**Recommendation:**
Reinstate REQ-021's pre-push ruleset-active check as a CI step: before each force-push, the workflow SHALL call `gh api orgs/{org}/rulesets` (or equivalent) and assert that the dedicated repo's default branch has exactly one bypass actor (the CI identity). Failure SHALL abort the push with a diagnostic. Add a scheduled monitor requirement: "A monitor SHALL weekly verify the org-level ruleset on `geekatron/jerry-cowork` is active, non-overridable, and names only the CI identity as bypass actor; a configuration drift SHALL open a GitHub issue within 1 hour of detection."

**Acceptance Criteria:**
CI step exists before the push step that calls GitHub API to confirm ruleset; the step aborts the workflow if the ruleset is absent or misconfigured. A monitoring workflow demonstrates detection of ruleset removal within 1 hour.

---

### PM-003-iter004: Attestation Verification Silent Fallback — Monitor Accepted Forgeable Secondary Anchor [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Assumption |
| **Likelihood** | Medium |
| **Priority** | P1 |
| **Section** | ADR-003 D4; REQ-042; NFR-006 |
| **Affected Dimension** | Evidence Quality |

**Failure Cause:**
In November 2026, Sigstore's transparency log experienced a 72-hour outage. `gh attestation verify` returned non-zero for all verification attempts. The backstop monitor (NFR-006) was designed to fall back to Release-notes SHA comparison when attestation is unavailable. The Release-notes SHA is editable by any principal with `contents: write` on the source repo (the exact "collapsed anchor" that ADR-003 D4 was designed to supersede). An attacker who knew about the Sigstore outage edited the Release-notes SHA to match their tampered skeleton tip, and the monitor accepted it. No alert fired.

**Evidence:**
- ADR-003 D4: "Verification compares against the attestation, never against editable Release-notes text."
- REQ-042 AC: "(c) `gh release edit v{N} --notes 'tampered'` is rejected OR the attestation still independently verifies" — the AC tests immutability of the RELEASE ITSELF, not the notes field.
- NFR-006 AC: "tamper-detection leg compares live dedicated-repo default-branch tip SHA against the immutable attestation (REQ-042) as primary anchor, falling back to Release-notes SHA (REQ-035) as secondary."
- ADR-003 Consequences §Negative-4: "Dependence on current GitHub features... Mitigation: Confirm empirically before Phase-5; fall back to a deploy-key + scheduled-monitor posture if a feature is unavailable."
- There is NO REQ that says the monitor SHALL FAIL CLOSED when attestation verification is unavailable.

**Root Cause:**
NFR-006 permits falling through to the secondary (Release-notes SHA) anchor when attestation is unavailable, without alerting that the downgrade occurred. This means a Sigstore outage simultaneously degrades the integrity guarantee AND creates an opportunity for a timing-window attack — but the monitor does not distinguish between "attestation verified successfully" and "attestation unavailable, fell back to secondary anchor." The fallback is silent.

**Prevention Missing from Requirements:**
1. No REQ that the monitor SHALL emit a DISTINCT ALERT when it falls back to the secondary anchor (as opposed to when it detects a mismatch).
2. No REQ that the monitor SHALL FAIL (not just warn) after N hours of attestation unavailability, to prevent indefinite operation on the weaker anchor.
3. No REQ covering what to do if `gh attestation` is unavailable at generation time — should CI abort the release?

**Recommendation:**
Add to NFR-006: "When the tamper-detection leg cannot reach the Sigstore transparency log or `gh attestation verify` returns non-zero for any reason other than a genuine mismatch, the monitor SHALL emit a DISTINCT GitHub issue labeled `attestation-unavailable` (not `tamper-detected`) and SHALL NOT fall through to Release-notes SHA comparison; the monitor leg SHALL exit non-zero." Add a REQ: "If attestation is unavailable for more than 4 hours, the meta-monitor (REQ-044) SHALL escalate to a human-intervention GitHub issue."

**Acceptance Criteria:**
Simulate Sigstore outage (mock `gh attestation verify` returning non-zero); the monitor opens an `attestation-unavailable` issue and does not compare against Release-notes SHA; the monitor exits non-zero. The 4-hour escalation requirement is demonstrated via meta-monitor test.

---

### PM-004-iter004: Org-Registration Repointed to Typosquat by Over-Permissioned Admin [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | External |
| **Likelihood** | Medium |
| **Priority** | P0 |
| **Section** | ADR-003 D1; REQ-043; ADR-003 Risks table OR-01/02 |
| **Affected Dimension** | Completeness |

**Failure Cause:**
An org admin whose account was compromised via credential phishing repointed the CoWork marketplace registration from `geekatron/jerry-cowork` to `geekatron/jerry-cowork-stable` (a typosquat repo under an attacker-controlled account). REQ-043 required "minimum of two admin approvals for any registered-source change" but there is no technical enforcement mechanism specified — CoWork's marketplace settings did not natively require two-person approval. The single compromised admin made the change, and all org users received hooks from the attacker-controlled repo at next install or update. The quarterly audit (REQ-043) was scheduled to run two months later.

**Evidence:**
- REQ-043: "restricted to vetted admins; a minimum of two admin approvals SHALL be required for any registered-source change." No technical enforcement mechanism is specified. The ONLY verification method is "Inspection of org settings and Inspection of runbook."
- REQ-043 AC: "Attempt to re-register without required approvals: blocked." — The AC assumes a technical enforcement mechanism exists, but the ADR and requirements do not specify what that mechanism is.
- ADR-003 D1 Risks: "Org-admin registers rogue/typosquat repo (OR-01/02/V-08) | LOW–MED | HIGH | Vetted-admin restriction; canonical-name runbook; periodic verification; audit review" — the mitigations are administrative, not technical.
- NFR-006 monitors `geekatron/jerry-cowork` tip SHA, but if the REGISTRATION points to a DIFFERENT REPO, NFR-006 monitors the wrong thing and detects nothing.
- The quarterly audit cadence (REQ-043) means a registration change goes undetected for up to 3 months.

**Root Cause:**
The two-admin approval requirement is purely procedural with no technical enforcement. No automated monitoring verifies the registered marketplace source URL (as opposed to the registered repo's tip SHA). The quarterly audit is the only detection mechanism for registration drift, and it is manual and too infrequent.

**Prevention Missing from Requirements:**
1. No REQ for a technical mechanism to enforce the two-admin approval (e.g., a GitHub protected branch for the runbook file, or a git-based approval workflow).
2. No REQ for automated monitoring of the registered marketplace source URL (checking that it still equals the canonical `geekatron/jerry-cowork`).
3. The quarterly audit cadence (REQ-043) is insufficient given HIGH consequence; no REQ for more frequent automated verification.

**Recommendation:**
Add a REQ: "A weekly automated monitor SHALL retrieve the registered CoWork marketplace source for the org and assert it equals `geekatron/jerry-cowork`; a mismatch SHALL open a P0 GitHub issue immediately and SHALL NOT wait for the quarterly audit." For the two-admin approval, specify the technical mechanism: "The org-registration runbook SHALL be stored in a protected file; any change to the registered source SHALL require a pull request with at least two required approvals from designated admins before merge; the PR is the approval mechanism."

**Acceptance Criteria:**
Automated monitor demonstrates detection within 1 hour of a registration source change. The runbook file in the protected branch demonstrates that a single-approver PR cannot be merged.

---

### PM-005-iter004: tests/ Strip Broke Runtime — No Post-Strip Functional Validation [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Technical |
| **Likelihood** | Medium |
| **Priority** | P1 |
| **Section** | ADR-001 §Phase 2 Update; REQ-002; REQ-005; ADR-001 §Canonical Plugin-Retention Surface |
| **Affected Dimension** | Methodological Rigor |

**Failure Cause:**
When `tests/` was stripped, it turned out that `conftest.py` in `tests/` was implicitly imported by pytest fixtures that were also used in development but had been accidentally symlinked into a `hooks/` test helper path. On fresh CoWork install, the `hooks/session-start.py` invoked `uv run jerry session status` which triggered an import chain that expected `tests/conftest.py` to be present. The session hook errored at first launch for every new org user. The error was not caught by any CI gate because the generation workflow only checked that the eight canonical directories were present (REQ-005), not that the CLI actually ran.

**Evidence:**
- ADR-001 Phase 2 amendment (header): strip set extended to `tests/`.
- ADR-001 §Canonical Plugin-Retention Surface (body): "`tests/` [is] not load-bearing for plugin function and MAY be stripped later" — this is asserted but not verified by any requirement.
- REQ-005 notes: "Note for ps-architect (ADR-001 inconsistency): ADR-001's body (§Canonical Plugin-Retention Surface) says `tests/` is 'retained today (1,744 ≪ 5,000)' but the ADR-001 amendment header (2026-06-28) and ADR-003 both strip `tests/'." This documented inconsistency was never resolved.
- REQ-005 AC: checks that `tests/` returns empty from `git ls-files tests/` — confirms the strip, but does NOT confirm runtime function.
- REQ-004 AC: "`uv run jerry projects list` exits 0" — tests one CLI command on the stub sentinel, not a full session-start flow.
- There is no requirement to run `uv run jerry session start` or a full hook execution against the generated skeleton tree in CI to confirm all session flows work post-strip.

**Root Cause:**
The assertion that `tests/` is "not load-bearing" is a prose claim in ADR-001, not a verified invariant. No requirement mandates a static analysis of `tests/` contents for non-test production dependencies before committing to strip it. No requirement mandates a post-strip CLI smoke test beyond `jerry projects list`. The generation workflow could produce a skeleton that passes all REQ-005/REQ-010 checks but fails at runtime.

**Prevention Missing from Requirements:**
1. No REQ for a static analysis step confirming that no production path under `src/`, `hooks/`, or `skills/` imports from or depends on files under `tests/`.
2. No REQ for a post-generation functional smoke test that runs `hooks/session-start.py` (or an equivalent entrypoint) against the generated skeleton tree.
3. The ADR-001 body inconsistency regarding `tests/` retention status is flagged in REQ-005 but remains unresolved.

**Recommendation:**
Add a REQ: "The generation CI SHALL execute a basic functional smoke test against the generated skeleton tree: at minimum, `uv run jerry session start --dry-run` or equivalent SHALL exit 0 from within the generated tree before the push step." Add a one-time verification REQ: "Before the Phase-5 implementation, a static analysis audit SHALL confirm that no path under `src/` or `hooks/` has a runtime dependency on `tests/`; findings SHALL be resolved before `tests/` stripping is implemented."

**Acceptance Criteria:**
CI step exists that runs a Jerry CLI command against the generated skeleton tree. Demonstration that injecting a broken import into `hooks/session-start.py` causes the smoke test to fail before any push occurs. Static audit artifact committed to the project.

---

### PM-006-iter004: Cross-Repo Sync Silently Stopped — No Generation Workflow Meta-Monitor [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Process |
| **Likelihood** | Medium |
| **Priority** | P1 |
| **Section** | NFR-006; REQ-044; REQ-016; NFR-003 |
| **Affected Dimension** | Completeness |

**Failure Cause:**
In October 2026, the org's GitHub Actions billing limit was reached following an unrelated large test suite run. Queued workflows were silently discarded. Three `v*` tag pushes triggered `cowork-skeleton.yml` in the source repo, but the workflow runs were never actually started. The dedicated repo remained on the skeleton from two months prior. Users installing the plugin received an outdated (though not malicious) skeleton. The NFR-006 lazy-staleness check (comparing `Source-Commit:` trailer to the latest v* tag) would have caught this — but it runs at "≤ weekly cadence," and the three missed releases happened within three days. The staleness check ran 5 days later and opened a GitHub issue, but by then users had been installing the stale skeleton for a week.

**Evidence:**
- NFR-003: "freshness: updated within one workflow run of tag push" — the AC is "GitHub Actions run history shows `cowork-skeleton.yml` completes within the same release window for each v* tag push." This is a SETUP-TIME demonstration, not ongoing enforcement.
- REQ-044: "A meta-monitor SHALL verify that the integrity backstop monitor (REQ-035 scheduled leg) has completed successfully within the prior 25 hours." — REQ-044 monitors the BACKSTOP MONITOR's liveness, NOT the GENERATION WORKFLOW's completion.
- NFR-006 lazy-staleness cadence: "≤ weekly." In a rapid-release scenario, three releases in a week could all be missed before detection.
- REQ-016 requires `if: failure()` notification — but a workflow that was NEVER QUEUED cannot emit a failure; the billing-limit case produces no workflow run at all.
- There is no REQ for a meta-monitor that alerts if `cowork-skeleton.yml` did not complete successfully within N hours of a `v*` tag push to the source repo.

**Root Cause:**
The monitoring architecture has two layers: the generation workflow (REQ-016's failure notification) and the staleness monitor (NFR-006). Both are reactive: they detect after the fact. A scenario where the workflow is never queued (billing, GitHub outage, tag-push trigger misconfiguration) leaves a gap: NFR-006's lazy-staleness check is the only detector and it runs at ≤ weekly cadence. For a project with multiple releases per week, this is insufficient.

**Prevention Missing from Requirements:**
1. No REQ for a dedicated meta-monitor on the GENERATION WORKFLOW: "if `cowork-skeleton.yml` has not completed successfully within 4 hours of a `v*` tag push on `geekatron/jerry`, an alert SHALL fire."
2. NFR-006's ≤ weekly lazy-staleness cadence is too low for a project with multiple releases per sprint.
3. REQ-044 monitors the BACKSTOP MONITOR but not the GENERATION WORKFLOW.

**Recommendation:**
Add a REQ: "A generation-workflow monitor SHALL verify that, for each `v*` tag pushed to `geekatron/jerry`, `cowork-skeleton.yml` completed successfully within 4 hours of the tag push; if no successful run is recorded within that window, the monitor SHALL open a P1 GitHub issue." Consider reducing the NFR-006 lazy-staleness cadence from ≤ weekly to ≤ daily, or parametrize it by release cadence.

**Acceptance Criteria:**
Demonstrate: push a `v*` tag; disable `cowork-skeleton.yml`; the generation-workflow monitor opens a GitHub issue within 4 hours. The monitor does not fire for successfully completed runs.

---

### PM-007-iter004: File-Count Creep — No Early-Warning Threshold Before 5,000 Limit [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Category** | Technical |
| **Likelihood** | Low |
| **Priority** | P2 |
| **Section** | REQ-006; REQ-034d; ADR-001 §Clone-Weight Decision |
| **Affected Dimension** | Completeness |

**Failure Cause:**
Over 18 months, the `skills/` directory grew as 12 new agents were added (each with approximately 3 files) and large test-data transcripts were added to `skills/transcript/test_data/`. The skeleton file count crept from 1,417 to 4,820 files without triggering any early-warning alert. On a release in Q1 2028, a batch of 200 new skill documentation files pushed the count to 5,031. REQ-006's hard-fail gate fired and blocked the release — the first notice the team had.

**Evidence:**
- REQ-006: "hard-fail assertion if tracked file count >= 5,000" — detected at generation time.
- REQ-034d: early-warning at 150 MB pack size — this is CLONE WEIGHT, not file count. There is no analogous early-warning threshold for file count.
- ADR-001 §L2 §4: "the strategy's validity rests on an external, still-unverified assumption... the ceiling could be size- or time-based rather than file-count-based (IN-001)."
- No requirement specifies a scheduled check of `main`'s file count in RETAINED directories between releases (the only check is at generation time via REQ-006).

**Root Cause:**
The continuous monitoring architecture covers clone-weight (pack size) with an early-warning band (150 MB → 250 MB), but has no equivalent early-warning for file count (e.g., alert at 4,000 files → 5,000 hard-fail). The 3,583-file margin at project start seems large, but with active skill development it is consumable within 18-24 months.

**Prevention Missing from Requirements:**
1. No early-warning file-count threshold requirement (e.g., alert at 80% of the 5,000 limit, ~4,000 files).
2. No scheduled monitoring of `main`'s file count in retained directories between releases.

**Recommendation:**
Add to REQ-034d: "The per-release weight emit SHALL also record the generated skeleton's tracked file count; the continuous integrity monitor SHALL additionally record the skeleton file count on each scheduled run and SHALL open a non-blocking GitHub issue when the count exceeds 4,000 (80% of the 5,000 ceiling)."

**Acceptance Criteria:**
Monitor opens a non-blocking GitHub issue when the skeleton file count in a test branch exceeds 4,000. The workflow hard-fails (REQ-006) when it exceeds 5,000.

---

## Recommendations

### P0 — Must Mitigate Before Acceptance

| Finding | Mitigation | Acceptance Criteria |
|---------|-----------|---------------------|
| PM-001-iter004 (App key leak) | (1) Add REQ for 90-day App private key rotation with runbook. (2) Add REQ for near-real-time alert (<1 h) on any push to `geekatron/jerry-cowork` that lacks a corresponding attestation. | REQ exists with rotation cadence. Monitor AC demonstrates 1-hour unattested-push detection. |
| PM-002-iter004 (Ruleset removed) | (1) Add CI pre-push step asserting ruleset active and bypass-actor list correct. (2) Add scheduled ruleset-configuration monitor with 1-hour alert. | CI step aborts push when ruleset missing. Monitor demonstrates detection of ruleset removal within 1 hour. |
| PM-004-iter004 (Org-registration repointed) | (1) Add weekly automated monitor for registered marketplace source URL. (2) Specify technical enforcement of two-admin approval (PR-based). | Monitor detects source URL change within 1 hour. Demonstration that single-approver change is blocked. |

### P1 — Should Mitigate

| Finding | Mitigation | Acceptance Criteria |
|---------|-----------|---------------------|
| PM-003-iter004 (Attestation silent fallback) | Add REQ: monitor SHALL alert distinctly on attestation unavailability and SHALL NOT fall through to Release-notes SHA; add 4-hour escalation escalation requirement. | Monitor opens `attestation-unavailable` issue; does not compare against Release notes when attestation is unavailable. |
| PM-005-iter004 (tests/ strip breakage) | Add post-strip CLI smoke test REQ; add static dependency-audit REQ before Phase-5; resolve ADR-001 body inconsistency. | CI smoke test fails when hook import broken. Static audit artifact committed. |
| PM-006-iter004 (Sync silently stopped) | Add generation-workflow meta-monitor REQ: alert within 4 h of a missed successful run after a v* tag push. | Meta-monitor opens issue within 4 h of disabled workflow after tag push. |

### P2 — Monitor

| Finding | Mitigation |
|---------|-----------|
| PM-007-iter004 (File-count creep) | Extend REQ-034d to include file-count early-warning at 4,000 files; add to scheduled monitor duty. |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-004 and PM-006 reveal missing requirements (no org-registration monitor, no generation-workflow meta-monitor, no file-count early-warning). The deliverables do not cover these failure paths. |
| Internal Consistency | 0.20 | Negative | PM-001 and PM-002: the "prevention" posture (D2 ruleset, D3 credential) is not consistently extended into ongoing enforcement. The ADR-001 body inconsistency on tests/ strip (PM-005) is flagged in REQ-005 but unresolved. |
| Methodological Rigor | 0.20 | Negative | PM-002, PM-005, PM-006: three major failure modes have no CI-enforceable prevention. The methodology relies on setup-time configuration checks (REQ-040) and demonstration ACs that do not continuously enforce invariants. |
| Evidence Quality | 0.15 | Negative | PM-003: the fallback behavior of the attestation monitor is underspecified; the distinction between "attestation failed" and "attestation unavailable" is not resolved in any requirement, weakening the integrity argument. |
| Actionability | 0.15 | Positive | ADR-003's six decisions are clearly stated with specific mitigations, new REQ numbers, and explicit threat mappings. The deliverables are action-oriented; the gaps identified here are additive, not structural. |
| Traceability | 0.10 | Neutral | Traceability from STRIDE threats to requirements is well-documented. The gaps are in monitoring requirements, not in threat identification or tracing. |

**Overall Assessment:** REVISE — targeted mitigation required. The two former Phase-1 Criticals (SC-04 anchor collapse, DR-01 direct push) are structurally resolved. The findings above are all in the monitoring and enforcement layer: the controls exist but their ongoing validity is not continuously verified. Three P0 findings must be addressed before acceptance.

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 3 (PM-001, PM-002, PM-004)
- **Major:** 3 (PM-003, PM-005, PM-006)
- **Minor:** 1 (PM-007)
- **Protocol Steps Completed:** 6 of 6 (Stage set, failure declared, causes generated, prioritized, mitigations developed, synthesis and scoring impact produced)
- **Failure Categories Covered:** External (2), Process (2), Technical (2), Assumption (1) — 4 of 5 categories represented; Resource category surfaced as a sub-cause within PM-006 (CI billing)

---

*Template: S-004 Pre-Mortem Analysis v1.0.0*
*Finding Prefix: PM-NNN-iter004*
*Deliverables Reviewed: ADR-001, ADR-003, phase1-requirements.md (Iteration 3 / Phase-2 Update)*
*Generated: 2026-06-29*
*Agent: jerry:adv-executor (Group C — Challenge, blind independent)*
