# FMEA Report: PROJ-031 CoWork Skeleton — Dedicated-Repo + CI + Attestation Pipeline

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** ADR-001-skeleton-derived-branch-strategy.md + ADR-003-credential-protection-supply-chain.md + requirements/phase1-requirements.md
**Criticality:** C4
**Date:** 2026-06-29
**Reviewer:** jerry:adv-executor (Group E — Decompose, blind / independent)
**H-16 Compliance:** S-003 Steelman confirmed in prior strategy outputs (iteration-004 chain)
**Elements Analyzed:** 10 | **Failure Modes Identified:** 10 | **Total RPN:** 2,337

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Deliverable Decomposition](#deliverable-decomposition) | Element inventory with identifiers |
| [Findings Table](#findings-table) | All 10 failure modes with S/O/D/RPN |
| [Detailed Findings](#detailed-findings) | Critical and Major finding evidence and rationale |
| [Recommendations](#recommendations) | Prioritized corrective actions by severity |
| [Scoring Impact](#scoring-impact) | FMEA findings mapped to S-014 dimensions |

---

## Summary

FMEA of the dedicated-repo + CI + attestation pipeline identified **10 failure modes** across 10 elements: **5 Critical** (RPN >= 200 or Severity >= 9) and **5 Major** (RPN 80–199). The highest-RPN finding (FM-001-it004, RPN 567) is a hard requirement contradiction: REQ-020 forbids `id-token: write` while REQ-042 mandates a Sigstore-backed build-provenance attestation that requires exactly that permission — REQ-042 is unimplementable as written in a single-job workflow without amending REQ-020. The second Critical (FM-002-it004, RPN 378) is an architectural impossibility: GitHub Actions cannot subscribe to `push` events in a different repository, making REQ-035's event-driven monitor non-functional when placed in the source repo. Two additional Criticals reveal that attestations are produced but never verified at install time (FM-006-it004, RPN 294) and that a process-only two-admin-approval control for org-registration changes provides a 3-month detection window (FM-005-it004, RPN 252). Corrective actions are mandatory for all five Critical findings before Phase-5. **Assessment: REVISE — significant targeted corrections required before the pipeline can be considered implementable.**

---

## Deliverable Decomposition

Element inventory (MECE decomposition across ADR-001, ADR-003, and phase1-requirements.md):

| ID | Element | Source |
|----|---------|--------|
| E1 | Workflow permissions block (`cowork-skeleton.yml`) | REQ-020, REQ-042 |
| E2 | Cross-repo push credential lifecycle (App token / deploy key) | ADR-003 D3, REQ-041, c-208 |
| E3 | Tag provenance gate (rogue-tag prevention) | ADR-003 D5, REQ-038, REQ-039 |
| E4 | Org-level ruleset protection on dedicated repo | ADR-003 D2, REQ-040 |
| E5 | Attestation integrity anchor (production + verification) | ADR-003 D4, REQ-042, NFR-006 |
| E6 | Event-driven integrity monitor (cross-repo trigger design) | REQ-035(a), NFR-006 |
| E7 | Org-registration governance (CoWork marketplace) | ADR-003 D1, REQ-043 |
| E8 | tests/ strip set extension and runtime impact | ADR-001 Phase-2 amendment, REQ-002, REQ-005 |
| E9 | Skeleton staleness detection and NFR-003 freshness | NFR-003, NFR-006, REQ-035 |
| E10 | File-count growth monitoring between releases | REQ-006, REQ-034d |

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action Summary | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|--------------------------|---------------------|
| FM-001-it004 | E1 (Permissions block) | REQ-020 prohibits `id-token: write`; REQ-042 mandates Sigstore attestation requiring it — mutual contradiction | 9 | 9 | 7 | 567 | Critical | Amend REQ-020 to allow `id-token: write` in a dedicated attestation job; use per-job `permissions:` to isolate scopes | Internal Consistency |
| FM-002-it004 | E6 (Event-driven monitor) | GitHub Actions cannot trigger a source-repo workflow on push events in a different repo; REQ-035(a) event-driven fast-path is architecturally impossible as specified | 7 | 9 | 6 | 378 | Critical | Specify monitor placement explicitly; either place a read-only workflow in the dedicated repo or replace the event-driven leg with a more frequent scheduled poll | Completeness |
| FM-005-it004 | E7 (Org-registration governance) | "Two-admin-approval" in REQ-043 is a process control with no GitHub-native enforcement; a single compromised admin can re-register silently; quarterly audit yields a 3-month detection window | 9 | 4 | 7 | 252 | Critical | Add a technical guard (org audit-log webhook alert on marketplace settings change); reduce audit cadence to monthly minimum; specify the enforcement mechanism | Completeness |
| FM-006-it004 | E5 (Attestation anchor) | REQ-042 mandates attestation production; no requirement mandates automated consumer-side verification at install time or specifies the monitoring workflow's attestation verification command (`gh attestation verify`) | 7 | 6 | 7 | 294 | Critical | Add REQ to mandate `gh attestation verify --repo geekatron/jerry <tip-sha>` in the backstop monitor; document that end-user install cannot be gated on attestation (and explain the resulting residual risk) | Completeness |
| FM-003-it004 | E2 (Credential lifecycle) | `workflow_dispatch` trigger exposes the App private key (long-lived secret) to every collaborator who can invoke dispatch; a compromised dispatch run can exfiltrate the key via indirect channels even with SHA-pinned actions | 9 | 3 | 6 | 162 | Critical | Restrict `workflow_dispatch` to protected maintainer roles via environment protection rules; consider an environment-gated job requiring approval for the credential mint step | Methodological Rigor |
| FM-004-it004 | E4 (Org-level ruleset) | ADR-003 D2 claims the ruleset is "non-overridable by repo admins," but GitHub org owners (a distinct, higher role) can modify or delete org-level rulesets; the prevention claim doesn't hold against org-owner compromise | 8 | 3 | 7 | 168 | Major | Acknowledge in ADR-003 Risks table that org-owner compromise reopens DR-01; add org-owner count minimization and alert on org-owner change as explicit controls | Methodological Rigor |
| FM-007-it004 | E8 (tests/ strip set) | ADR-001's body states `tests/` is "retained today (1,744 ≪ 5,000)"; the Phase-2 amendment header and ADR-003 both strip it; REQ-010 verifies plugin.json agent paths but no acceptance criterion confirms no hook or src/ code has a runtime import or path dependency on `tests/` | 7 | 4 | 6 | 168 | Major | Add acceptance criterion to REQ-002 or REQ-010: install the skeleton on a clean clone and execute `uv run jerry projects list` and `uv run jerry session start` to confirm no runtime path error referencing `tests/`; correct ADR-001 body inconsistency | Completeness |
| FM-010-it004 | E5 (Attestation anchor) | The force-push to `geekatron/jerry-cowork` executes BEFORE attestation creation (per ADR-003 L1 "In CI after a successful push: create an immutable release and generate a build-provenance attestation"); if the job fails between push and attestation, the skeleton is live but permanently unattested for that release | 7 | 4 | 5 | 140 | Major | Reorder pipeline so attestation is created and published BEFORE force-push; alternatively, have the monitoring workflow detect missing attestation and alert immediately rather than silently failing verification | Methodological Rigor |
| FM-009-it004 | E10 (File-count growth) | REQ-034d monitors compressed pack size (MB) with a 150 MB early-warning band and a 250 MB hard-fail, but provides no equivalent proactive monitoring for file-count growth; the CI gate (REQ-006) hard-fails at generation time only, with no "approaching 5,000" early warning | 6 | 3 | 6 | 108 | Major | Add a file-count early-warning threshold (e.g., 3,500 files, ~68% of the 5,000 limit) emitted to `$GITHUB_STEP_SUMMARY` and as a non-blocking GitHub issue, mirroring the 150 MB / 250 MB pattern of REQ-034d | Completeness |
| FM-008-it004 | E9 (Staleness detection) | The lazy-staleness check in NFR-006 fires weekly; if the generation workflow fails silently on a `v*` tag push (GitHub Actions outage, concurrency serialization bug), users install a stale skeleton for up to 7 days before detection; the daily tamper-detection leg would not fire because the tip SHA still matches the previous release's expected value | 5 | 4 | 5 | 100 | Major | Add a per-release "generation success" signal (e.g., set a GitHub Actions output or write a release annotation); the staleness check should compare the dedicated-repo tip tag annotation to the LATEST source-repo v* tag, not just the `Source-Commit:` trailer | Actionability |

---

## Detailed Findings

### FM-001-it004: REQ-020 / REQ-042 Permissions Contradiction

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E1 — Workflow permissions block |
| **S / O / D** | 9 / 9 / 7 |
| **RPN** | 567 |
| **Post-correction RPN estimate** | ~70 (S=7, O=2, D=5) after splitting into two jobs with per-job permissions |

**Evidence:**

REQ-020 (requirements/phase1-requirements.md, WS-3):
> "The `permissions:` block in `cowork-skeleton.yml` SHALL declare `contents: write` as the sole permission entry and SHALL NOT include `actions: write`, `packages: write`, `id-token: write`, or any organization-level scope."

REQ-042 (requirements/phase1-requirements.md, WS-3 Phase-2):
> "The CI workflow SHALL create an immutable GitHub Release and a build-provenance attestation (Sigstore-backed, SLSA-aligned, e.g., `gh attestation`) binding the skeleton tip SHA to the specific workflow run, source commit SHA, and source repo at generation time."

ADR-003 D4 (decisions/ADR-003, L1 Technical Implementation):
> "In CI after a successful push: create an immutable release and generate a build-provenance attestation binding the skeleton tip SHA to the run/commit/repo."

**Analysis:** GitHub's `gh attestation attest` (and any Sigstore-backed OIDC workflow attestation) requires `id-token: write` in the `permissions:` block to request an OIDC JWT from GitHub's token endpoint, which Sigstore uses to bind the attestation to the workflow identity. REQ-020 explicitly and categorically forbids `id-token: write` in the workflow's permissions block. The two requirements are mutually exclusive when both apply to the same job in the same workflow file. A single-job `cowork-skeleton.yml` cannot satisfy both. This makes REQ-042 unimplementable as written, leaving the 5-strategy Critical SC-04 partially unresolved — ADR-003 resolves it in design but the requirements block its implementation.

**Recommendation:** Amend REQ-020 to read: "The push job `permissions:` block SHALL declare `contents: write` as the sole permission entry; an attestation job DEFINED IN THE SAME WORKFLOW MAY additionally declare `id-token: write` using per-job `permissions:` to isolate OIDC scope from the push credential." Add a per-job `permissions:` pattern to the L1 Technical Implementation in ADR-003 so implementers know to split the push and attestation into separate jobs.

**Acceptance Criteria:** REQ-020 amended; `cowork-skeleton.yml` implementation uses per-job `permissions:` with `contents: write` in the push job and `id-token: write` + `contents: write` in the attestation job; `gh attestation verify` succeeds after a CI run.

---

### FM-002-it004: Cross-Repo Event-Driven Monitor Architecturally Impossible

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E6 — Event-driven integrity monitor |
| **S / O / D** | 7 / 9 / 6 |
| **RPN** | 378 |
| **Post-correction RPN estimate** | ~84 (S=7, O=4, D=3) after redesigning with an explicit monitor placement decision |

**Evidence:**

REQ-035(a) (requirements/phase1-requirements.md, WS-3):
> "(a) Event-driven fast path — on `on: push: branches: [<dedicated-repo-default-branch>]`; retrieve the published SHA from Release notes and assert `git rev-parse HEAD` equals it; mismatch SHALL create a GitHub issue and exit non-zero."

Allocation Matrix (phase1-requirements.md, L2):
> "monitor is distinct from `cowork-skeleton.yml` to allow independent event triggers"

ADR-003 CR-02 (decisions/ADR-003, Confirmed distribution model):
> "dedicated repo has no push-back workflows (loop-safety by topology)"

**Analysis:** In GitHub Actions, a workflow's `on: push: branches:` trigger fires only when there is a push to the repository that HOSTS the workflow file. A workflow in `geekatron/jerry` (source repo) cannot subscribe to `push` events in `geekatron/jerry-cowork` (dedicated repo) via standard trigger syntax. The event-driven fast-path as specified can only work if the monitoring workflow is placed in the dedicated repo itself — but ADR-003 D1/D2 and REQ-023 require the dedicated repo to have no workflows that create feedback loops to the source repo. Even if read-only monitoring workflows are permitted in the dedicated repo (a distinction REQ-023 draws by saying "no workflow that PUSHES to the source repo"), this architectural option is never articulated or decided in the deliverables. The result is an unresolvable ambiguity: the fast-path trigger either cannot fire (if monitor is in source repo) or requires an undocumented design decision about dedicated-repo workflow presence.

**Recommendation:** Add Decision D7 to ADR-003: explicitly decide whether a read-only integrity-monitor workflow may reside in the dedicated repo. If yes, the event-driven leg becomes architecturally sound (workflow in dedicated repo subscribes to its own push events, creates issues in the dedicated repo). If no, replace the event-driven leg with a 1-hour or 6-hour scheduled poll rather than `on: push:`, and update the detection SLA accordingly. Amend REQ-035(a) to reflect the chosen design.

**Acceptance Criteria:** ADR-003 Decision D7 approved; REQ-035(a) rewritten with an implementable cross-repo monitor topology; the acceptance criterion "REQ-035 event-driven leg fires within minutes" is achievable in CI demonstration.

---

### FM-005-it004: Org-Registration Repointed — Process-Only Approval, 3-Month Detection Window

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E7 — Org-registration governance |
| **S / O / D** | 9 / 4 / 7 |
| **RPN** | 252 |
| **Post-correction RPN estimate** | ~108 (S=9, O=2, D=6) after adding technical enforcement and monthly audit |

**Evidence:**

REQ-043 (requirements/phase1-requirements.md, WS-3 Phase-2):
> "CoWork marketplace registration of `geekatron/jerry-cowork` as the canonical org plugin source SHALL be restricted to vetted org admins; a minimum of two admin approvals SHALL be required for any registered-source change. A runbook SHALL document the canonical repo full name (`geekatron/jerry-cowork`), the registration change protocol, and a periodic registered-source verification schedule (≤ quarterly audit)."

ADR-003 Risks table:
> "Org-admin registers rogue/typosquat repo (OR-01/02/V-08) | LOW–MED | HIGH | Vetted-admin restriction; canonical-name runbook; periodic verification; audit-log review (REQ-043)"

**Analysis:** Two failure modes compound here. First, "a minimum of two admin approvals" for registration changes is a process requirement with no specified GitHub-native technical enforcement mechanism. CoWork's marketplace does not natively enforce a two-admin approval workflow for org plugin source changes; this means the control depends entirely on organizational discipline. A single compromised or malicious org admin can re-register the plugin source unilaterally. Second, the "periodic registered-source verification schedule (≤ quarterly audit)" creates a detection window of up to 3 months during which all org users install from a rogue repo, executing attacker-controlled hooks on every session start. The consequence is a mass org-wide user compromise (blast radius = all org users; hooks execute on session start per ADR-003 L0).

**Recommendation:** (1) Specify a technical enforcement mechanism for the two-admin approval requirement — e.g., require registration changes to be made via a tracked GitHub Issue workflow with two admin approvals on the issue before any change is actioned. (2) Add an automated daily or weekly check (webhook or GitHub App) that reads the org CoWork registration and compares it to the canonical repo name in the runbook; alert on mismatch within 24 hours. (3) Reduce the runbook audit cadence to monthly, and add an org audit-log webhook alert on marketplace settings changes.

**Acceptance Criteria:** Technical enforcement mechanism documented and in place; automated daily verification of registered source implemented; monthly runbook audit schedule confirmed.

---

### FM-006-it004: Attestation Produced But Not Verified at Install Time

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E5 — Attestation integrity anchor |
| **S / O / D** | 7 / 6 / 7 |
| **RPN** | 294 |
| **Post-correction RPN estimate** | ~105 (S=7, O=3, D=5) after adding explicit monitoring-workflow verification command and documenting the install-time residual |

**Evidence:**

REQ-042 AC (requirements/phase1-requirements.md):
> "(b) `gh attestation verify <skeleton-tip-sha> --repo geekatron/jerry` exits zero and outputs the build-provenance attestation binding tip SHA to workflow run, source commit, and source repo"

NFR-006 (requirements/phase1-requirements.md, Non-Functional Requirements):
> "retrieve the expected deterministic tip SHA from the GitHub Release notes for the latest `v*` tag (per REQ-035) and assert that `git rev-parse HEAD` on the dedicated repo equals it; re-point anchor from editable Release-notes text to the immutable attestation (REQ-042) as the primary integrity reference"

ADR-003 D4: "Verification compares against the attestation, **never** against editable Release-notes text."

**Analysis:** REQ-042's acceptance criterion specifies that `gh attestation verify` can be run (condition: attestation exists and exits zero). However, no requirement mandates that the backstop monitoring workflow (NFR-006/REQ-035) actually invokes `gh attestation verify` as part of its scheduled run. The NFR-006 text says to "re-point anchor to the immutable attestation" but specifies the verification check as comparing `git rev-parse HEAD` to the "expected deterministic tip SHA" — which could be read as merely fetching the SHA from the Release-notes text and comparing it, without cryptographic attestation verification. At end-user install time, `claude plugin marketplace add geekatron/jerry@cowork-skeleton` proceeds without any attestation check; CoWork does not run `gh attestation verify` before installing a plugin. The result: the attestation exists as a forensic artifact but no automated system is specified to cryptographically verify it before content reaches users, weakening the "publicly verifiable" security claim to a manual-only property.

**Recommendation:** Add a new requirement: "The integrity backstop monitor (REQ-035/NFR-006) SHALL execute `gh attestation verify <live-tip-sha> --repo geekatron/jerry` as the primary tamper-detection check; a verification failure SHALL create a GitHub issue and exit non-zero." Add a note in ADR-003 L2 acknowledging that end-user install-time attestation verification is not currently feasible via CoWork's plugin mechanism and that the backstop monitor is the sole automated verification path, constituting a residual gap that the attestation backstop partially compensates for.

**Acceptance Criteria:** Monitoring workflow implementation includes `gh attestation verify` command; NFR-006 AC updated to require the verification command; the tamper-detection test scenario confirms `gh attestation verify` fails appropriately on a directly-pushed (tampered) skeleton tip.

---

### FM-003-it004: App Private-Key Scope Exposed to All workflow_dispatch Actors

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E2 — Cross-repo credential lifecycle |
| **S / O / D** | 9 / 3 / 6 |
| **RPN** | 162 |
| **Post-correction RPN estimate** | ~54 (S=9, O=1, D=6) after environment-gated credential access |

**Evidence:**

REQ-011 (requirements/phase1-requirements.md, WS-2):
> "The CI workflow SHALL trigger on `push: tags: ['v*']` and `workflow_dispatch` events"

ADR-003 c-208 (decisions/ADR-003, Constraints):
> "The App private key (or deploy key) is the project's single long-lived secret and MUST be stored only in source-repo secrets with minimal access and a rotation policy."

ADR-003 L0:
> "the cross-repo credential… one key that writes what everyone runs"

**Analysis:** `workflow_dispatch` grants any repository collaborator with that permission the ability to trigger `cowork-skeleton.yml`. Each triggered run mints a GitHub App installation token (or accesses the deploy key) from source-repo secrets. The requirement states the App private key has "minimal access" but does not specify a technical enforcement mechanism to limit who can invoke `workflow_dispatch`. In the default GitHub configuration, any write-level collaborator can trigger `workflow_dispatch`. A malicious or socially-engineered collaborator triggering repeated workflow runs exposes the long-lived App private key to the workflow execution context on each run. Even with SHA-pinned actions (REQ-017), an insider threat or a social-engineering attack that gets a malicious step merged into the workflow could exfiltrate the key. Key theft enables indefinite, undetected skeleton forgery until rotation.

**Recommendation:** Gate the `workflow_dispatch` trigger on a GitHub Actions Environment with an explicit approval requirement; the App private key and deploy key should be stored as environment-level secrets (accessible only to protected environments) rather than repository-level secrets. Add an environment-protection rule requiring at least one designated maintainer approval before any `workflow_dispatch` run can access the credential. Update c-208 with this specific technical constraint.

**Acceptance Criteria:** `workflow_dispatch` triggers go through an environment-gated approval before the credential-mint step; repository-level `workflow_dispatch` without environment approval cannot access the App key or deploy key secret.

---

### FM-004-it004: Org Owner Can Suppress Dedicated-Repo Ruleset

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E4 — Org-level ruleset protection |
| **S / O / D** | 8 / 3 / 7 |
| **RPN** | 168 |
| **Post-correction RPN estimate** | ~72 (S=8, O=1, D=9) after minimizing org-owner count and adding audit alert |

**Evidence:**

ADR-003 D2 (decisions/ADR-003):
> "which repo admins cannot override"

ADR-003 Consequences — Negative #3:
> "Admin-suppression residual on the dedicated repo (DR-02). A repo admin could toggle protection. Mitigation: org-level ruleset repo-admins cannot override, admin minimization, audit alert, attestation backstop."

**Analysis:** ADR-003 D2 correctly notes that the org-level ruleset cannot be overridden by repo admins. However, GitHub org OWNERS (a role above repo admins in the GitHub permission hierarchy) CAN modify, disable, or delete org-level rulesets. The deliverable conflates "repo admins cannot override" with "the ruleset cannot be suppressed," overlooking the org-owner role. An org with multiple owners (common in shared organizations) presents a wider attack surface than acknowledged. The attestation backstop (D4) would detect content tampering after the fact, but the combination of a suppressed ruleset and a legitimate-identity CI push (D3 credential still active) could produce an attested but maliciously-generated skeleton — D4 attests the faithful build, not the legitimacy of the trigger, so D4 does not compensate fully for a suppressed D2.

**Recommendation:** Add to ADR-003 Risks table: "Org-owner suppresses org-level ruleset (DR-02b) | LOW | HIGH | Minimize org-owner count to 2 or fewer; require MFA for all org owners; add org audit-log webhook alert on BOTH org-owner addition AND ruleset change events; document that D4 attestation does not substitute for D2 prevention in all scenarios." Specify the exact alert mechanism (e.g., GitHub audit log streaming to a notification channel).

**Acceptance Criteria:** Risks table updated; org-owner count documented and minimized; audit-log alert configured for ruleset changes.

---

### FM-007-it004: tests/ Strip Runtime Dependency Unverified

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E8 — tests/ strip set extension |
| **S / O / D** | 7 / 4 / 6 |
| **RPN** | 168 |
| **Post-correction RPN estimate** | ~42 (S=7, O=1, D=6) after adding runtime smoke-test AC |

**Evidence:**

ADR-001 body, Canonical Plugin-Retention Surface (decisions/ADR-001):
> "By contrast `docs/`, `runbooks/`, `overrides/`, `scripts/`, `tests/` are **not** load-bearing for plugin function and MAY be stripped later if the file-count margin tightens (R-002) — but are retained today (1,744 ≪ 5,000)."

ADR-001 Phase-2 amendment header:
> "extends the strip set to include **`tests/`**"

REQ-005 note (requirements/phase1-requirements.md):
> "Note for ps-architect (ADR-001 inconsistency): ADR-001's body (§Canonical Plugin-Retention Surface) says `tests/` is 'retained today (1,744 ≪ 5,000)' but the ADR-001 amendment header (2026-06-28) and ADR-003 both strip `tests/`."

**Analysis:** The requirements explicitly flag an inconsistency in ADR-001 between its body (which says `tests/` is retained) and the Phase-2 amendment header (which strips it). This inconsistency is a navigational hazard for implementers but the deeper risk is the lack of a runtime dependency check. REQ-010 verifies all agent paths declared in `plugin.json` exist after the strip, but it does not verify that `src/` code paths, `hooks/` scripts, or `.context/` configuration files have no runtime imports or `os.path.exists()`-style checks that depend on the presence of `tests/`. Python's import system can follow relative paths; if `hooks/session-start.py` or any `src/` module references `tests/` via a path expression, the plugin will fail silently on install. The R-001 smoke-test (REQ-034 dimension d) is deferred and may not happen before Phase 5.

**Recommendation:** (1) Correct ADR-001 body prose to remove the contradictory "retained today" statement in the Canonical Plugin-Retention Surface section. (2) Add acceptance criterion to REQ-002: "On a clean clone of `cowork-skeleton`, execute `uv run jerry projects list` and `uv run jerry session start --help`; both commands exit 0 with no FileNotFoundError, ModuleNotFoundError, or path-reference error mentioning `tests/`." (3) Add a static grep check in the CI validation step: `grep -r 'tests/' hooks/ src/ .context/ --include='*.py' --include='*.json' --include='*.md' | grep -v '#'` to surface any hard-coded `tests/` references before push.

**Acceptance Criteria:** ADR-001 body corrected; runtime AC added to REQ-002; CI grep check in place; clean-clone smoke-test passes.

---

### FM-010-it004: Force-Push Precedes Attestation (Temporal Window)

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E5 — Attestation integrity anchor |
| **S / O / D** | 7 / 4 / 5 |
| **RPN** | 140 |
| **Post-correction RPN estimate** | ~49 (S=7, O=1, D=7) after reordering pipeline or adding unattested-release detection |

**Evidence:**

ADR-003 D4 / L1 Technical Implementation (decisions/ADR-003):
> "In CI after a successful push: create an immutable release and generate a build-provenance attestation binding the skeleton tip SHA to the run/commit/repo."

ADR-003 Confirmed distribution model pipeline (decisions/ADR-003):
> Step 5 is `force-push to geekatron/jerry-cowork`, then attestation is post-push.

**Analysis:** The pipeline as specified performs the force-push to the dedicated repo (making the skeleton live and installable) and THEN creates the attestation. If the CI job fails between the push and the attestation creation (API rate limit, transient network error, GitHub attestation service outage, runner timeout), the skeleton version is live in the dedicated repo with no corresponding attestation. Because REQ-003 guarantees a bit-identical SHA on re-run, a `workflow_dispatch` re-run will regenerate the same skeleton and can re-attempt attestation. However, nothing in the requirements mandates or detects this "unattested release" state. A monitoring workflow attempting to verify the attestation for that tip SHA will fail, but if the monitoring workflow merely checks "tip SHA matches expected value" without checking "attestation exists," the failure is silent. During the unattested window (until the next scheduled backstop run), the security claim "CI-only-writable, publicly verifiable" is false for that release.

**Recommendation:** (1) Reorder the pipeline: create the immutable release and initiate the attestation signature BEFORE the force-push; include the attestation URL as a job output; only push if attestation succeeded. (2) Add a monitoring check: `gh attestation verify <tip-sha> --repo geekatron/jerry`; if this fails, raise a separate "unattested release" GitHub issue. (3) Add to REQ-042 AC: "If the attestation step fails, the force-push step SHALL NOT execute; the job SHALL exit non-zero with a diagnostic identifying the unattested-release condition."

**Acceptance Criteria:** Pipeline reordered so attestation precedes push; REQ-042 AC updated; monitoring workflow detects and alerts on unattested releases.

---

### FM-009-it004: File-Count Growth Unmonitored Between Releases

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E10 — File-count growth monitoring |
| **S / O / D** | 6 / 3 / 6 |
| **RPN** | 108 |
| **Post-correction RPN estimate** | ~36 (S=6, O=1, D=6) after adding early-warning threshold |

**Evidence:**

REQ-006 (requirements/phase1-requirements.md, WS-1):
> "The skeleton generation script SHALL assert that the tracked file count of the generated branch tree is less than 5,000 and SHALL exit with a non-zero exit code if this assertion is not satisfied."

REQ-034d (requirements/phase1-requirements.md, WS-5):
> "The workflow SHALL exit non-zero and abort the release if `size-pack:` exceeds **250 MB** … The continuous integrity monitor SHALL additionally record `size-pack:` and clone time on each scheduled run and SHALL open a GitHub issue as a **non-blocking early warning** when `size-pack:` exceeds **150 MB**."

**Analysis:** REQ-034d provides a two-tier monitoring pattern for compressed pack size: a 150 MB non-blocking early warning and a 250 MB hard-fail. No equivalent two-tier pattern exists for file count. The current skeleton is approximately 1,749 files (Phase-2 figure, including `tests/` strip); the limit is 5,000 files, giving 3,251 file headroom. Each new skill added to `skills/` (currently 88 agents under `skills/*/agents/`) may add 2–5 files; a major skills expansion could consume 500–1,000 files without warning. The first signal of a problem is a hard CI failure at release time (REQ-006), leaving no opportunity for advance remediation before a release is blocked. The asymmetry between the MB monitoring (proactive early warning) and the file-count monitoring (reactive hard-fail only) is an inconsistency in the monitoring architecture.

**Recommendation:** Amend REQ-034d to add: "The workflow SHALL additionally emit the tracked file count of the generated tree to `$GITHUB_STEP_SUMMARY` on every run. The continuous integrity monitor SHALL open a GitHub issue as a non-blocking early warning when the tracked file count exceeds **3,500 files** (~70% of the 5,000 CoWork limit, mirroring the 150 MB / 250 MB two-tier pattern of the size telemetry)." Mirror this in the NFR-006 monitoring duty list.

**Acceptance Criteria:** REQ-034d amended; `$GITHUB_STEP_SUMMARY` emits file count per run; scheduled monitor opens early-warning issue at 3,500 files; CI hard-fails at 5,000.

---

### FM-008-it004: Generation Workflow Stale — Weekly Detection Lag

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E9 — Skeleton staleness detection |
| **S / O / D** | 5 / 4 / 5 |
| **RPN** | 100 |
| **Post-correction RPN estimate** | ~40 (S=5, O=2, D=4) after adding generation-success signal and daily staleness check |

**Evidence:**

NFR-003 (requirements/phase1-requirements.md):
> "The `cowork-skeleton` branch SHALL be updated within one CI workflow run of a `v*` tag being pushed to the repository."

NFR-006 (requirements/phase1-requirements.md):
> "(1) Lazy-staleness check (≤ weekly cadence) — compare the `Source-Commit:` trailer … to the full SHA of the latest `v*` tag on source-repo `main`"

**Analysis:** NFR-003 mandates freshness within one workflow run of a tag push. However, if the generation workflow fails silently (GitHub Actions outage, runner timeout, concurrency deadlock), the dedicated repo remains at the prior release. The lazy-staleness check (NFR-006 leg 1) fires weekly, meaning users could install a stale skeleton for up to 7 days before detection. The daily tamper-detection check (NFR-006 leg 2) compares the live tip SHA to the expected SHA for the latest release — but if the workflow NEVER FIRED, the tip SHA still matches the PREVIOUS release's expected value, making the daily check pass without raising an alert about the missed generation. The staleness check is therefore dependent on the correct implementation of "compare to latest v* tag on main," and specifically on the monitoring workflow independently knowing what the latest source-repo tag is.

**Recommendation:** (1) Add a post-generation success signal: on successful push, write a GitHub Deployment status to `geekatron/jerry-cowork` with the tag version; the staleness check can compare the latest deployment version to the latest source-repo tag without relying on the `Source-Commit:` trailer. (2) Reduce the lazy-staleness cadence from weekly to daily or 12-hourly. (3) Add an explicit requirement: "The staleness monitor SHALL query the source repo for the latest `v*` tag and compare it to the dedicated repo's latest deployment tag; a mismatch of more than 2 hours after the tag push SHALL open a GitHub issue."

**Acceptance Criteria:** Staleness check fires within 24 hours of a missed generation; deployment-status mechanism captures the generation event independently of `Source-Commit:` trailer.

---

## Recommendations

### Critical Findings — Mandatory Corrective Actions

| ID | Corrective Action | Acceptance Criteria | Current RPN | Est. Post-Correction RPN |
|----|-------------------|--------------------:|-------------|--------------------------|
| FM-001-it004 | Amend REQ-020 to allow `id-token: write` in a dedicated attestation job using per-job `permissions:` isolation; update ADR-003 L1 with the two-job pipeline pattern | `gh attestation verify` succeeds after CI run; REQ-020 amended to distinguish push-job vs attestation-job scopes | 567 | ~70 |
| FM-002-it004 | Decide monitor placement (new ADR-003 D7); redesign event-driven trigger for the chosen topology; amend REQ-035(a) with implementable syntax | Event-driven leg fires within minutes of a dedicated-repo push in CI demonstration | 378 | ~84 |
| FM-006-it004 | Add requirement mandating `gh attestation verify` in backstop monitor; document install-time verification gap as a disclosed residual | Monitor CI run invokes `gh attestation verify`; AC updated; residual acknowledged in ADR-003 Risks | 294 | ~105 |
| FM-005-it004 | Add technical enforcement for two-admin approval; implement daily automated registered-source verification; reduce audit cadence to monthly | Automated verification fires daily; audit-log alert configured; monthly runbook audit confirmed | 252 | ~108 |
| FM-003-it004 | Gate `workflow_dispatch` on environment-protected credential access requiring maintainer approval; move App key/deploy key to environment-level secrets | `workflow_dispatch` without environment approval cannot access credential secret | 162 | ~54 |

### Major Findings — Recommended Corrective Actions

| ID | Corrective Action | Acceptance Criteria | Current RPN | Est. Post-Correction RPN |
|----|-------------------|--------------------:|-------------|--------------------------|
| FM-004-it004 | Document org-owner suppression risk in ADR-003 Risks; minimize org-owner count; add audit-log alert on org-owner role change AND ruleset modification | Risks table updated; org-owner count ≤ 2; alert configured | 168 | ~72 |
| FM-007-it004 | Correct ADR-001 body `tests/` inconsistency; add runtime smoke-test AC to REQ-002; add CI grep for `tests/` references in hooks/src | Clean-clone smoke-test passes; CI grep step in place | 168 | ~42 |
| FM-010-it004 | Reorder pipeline: attestation before force-push; add unattested-release detection in monitoring; update REQ-042 AC | Job fails before push if attestation fails; monitoring detects unattested releases | 140 | ~49 |
| FM-009-it004 | Add file-count early-warning threshold (3,500 files) to REQ-034d and NFR-006 monitoring duty | `$GITHUB_STEP_SUMMARY` emits file count; issue opened at 3,500 files | 108 | ~36 |
| FM-008-it004 | Add deployment-status success signal; reduce staleness check to daily; add explicit ">2 hours after tag push" staleness SLA | Staleness detection fires within 24 hours of a missed generation | 100 | ~40 |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | **Negative** | FM-002, FM-005, FM-006, FM-007, FM-009 — five findings represent absent or underspecified controls: event-driven monitor is unspecified in placement, org-registration verification is quarterly, attestation verification is not mandated, runtime dependency on tests/ is unchecked, file-count early warning is absent |
| Internal Consistency | 0.20 | **Negative** | FM-001, FM-007 — REQ-020 and REQ-042 cannot both be satisfied in a single-job workflow (hard contradiction); ADR-001 body contradicts the Phase-2 amendment header on tests/ retention |
| Methodological Rigor | 0.20 | **Negative** | FM-003, FM-004, FM-010 — three findings expose systematic gaps: workflow_dispatch credential exposure is not mitigated at the technical level, org-owner exemption from rulesets is unacknowledged, pipeline ordering creates an unattested window contrary to the stated "immutable anchor" posture |
| Evidence Quality | 0.15 | **Neutral** | Findings are grounded in specific requirement text and GitHub Actions documented behavior; the deliverables provide clear audit trails; however, no independent empirical verification has occurred (R-001 smoke-test deferred) |
| Actionability | 0.15 | **Negative** | FM-008 — the stale-skeleton detection SLA (weekly) is insufficient for a high-blast-radius plugin; corrective action is specific and implementable but requires a requirement change |
| Traceability | 0.10 | **Positive** | ADR-003 →  REQ-038–044 trace is complete; ADR-001 →  REQ-002/005 trace is accurate; STRIDE threat IDs are consistently cited across ADR and requirements; the allocation matrix provides clear component-to-requirement mapping |

---

## Execution Statistics

- **Total Findings:** 10
- **Critical:** 5 (FM-001, FM-002, FM-003, FM-005, FM-006)
- **Major:** 5 (FM-004, FM-007, FM-008, FM-009, FM-010)
- **Minor:** 0
- **Total RPN:** 2,337
- **Highest RPN:** FM-001-it004 (567) — REQ-020 / REQ-042 permissions contradiction
- **Protocol Steps Completed:** 5 of 5
- **Element Coverage:** 10 elements, all examined (MECE)
- **Failure Mode Lenses Applied:** All 5 (Missing, Incorrect, Ambiguous, Inconsistent, Insufficient) per element; concentrated findings in Incorrect (FM-001, FM-004, FM-007) and Missing (FM-002, FM-005, FM-006, FM-009) lenses

---

*Generated by: jerry:adv-executor (Group E — Decompose, blind/independent)*
*Strategy: S-012 FMEA | Template: .context/templates/adversarial/s-012-fmea.md v1.0.0*
*Iteration: iteration-004 | Execution ID: it004*
*Constitutional Compliance: P-003 (no subagents), P-020 (deliverables not modified), P-022 (findings not minimized)*
