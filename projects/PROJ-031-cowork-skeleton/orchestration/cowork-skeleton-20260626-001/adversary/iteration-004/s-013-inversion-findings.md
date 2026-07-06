# Inversion Report: ADR-001, ADR-003, and Phase-1 Requirements (RE-ADVERSARY Gate — Iteration 4)

**Strategy:** S-013 Inversion Technique
**Deliverables:** ADR-001-skeleton-derived-branch-strategy.md, ADR-003-credential-protection-supply-chain.md, requirements/phase1-requirements.md
**Criticality:** C4
**Date:** 2026-06-29
**Reviewer:** jerry:adv-executor (blind, independent — Group E Decompose, RE-ADVERSARY gate)
**H-16 Compliance:** S-003 Steelman confirmed applied in prior iterations (RE-ADVERSARY gate follows Phase-2 full tournament)
**Goals Analyzed:** 6 | **Assumptions Mapped:** 14 | **Vulnerable Assumptions:** 7

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Goals and Inversions](#goals-and-inversions) | The six goals inverted to anti-goals |
| [Assumption Map](#assumption-map) | All assumptions with confidence and validation status |
| [Findings Table](#findings-table) | Classified findings with severity |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, and recommendations per finding |
| [Recommendations](#recommendations) | Prioritized mitigation list |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Summary

Six goals were inverted to anti-goals; 14 assumptions were extracted and stress-tested. Seven survive as findings: four Major and three Minor. No Critical assumptions were found — the Phase-2 hardening genuinely closes the Phase-1 Critical cluster. However, two of the four Major findings are implementation-blocking contradictions embedded in the requirements themselves: (1) REQ-020 explicitly forbids `id-token: write` while REQ-042 mandates a Sigstore attestation that requires it, and (2) the event-driven fast path (REQ-035a) cannot be triggered cross-repo without adding workflows to the dedicated repo, contradicting the loop-safe no-workflow topology. A third Major finding shows that NFR-006/REQ-035 still describe Release-notes SHA retrieval despite the Phase-2 intent to re-point verification to the immutable attestation. A fourth covers the absence of any SHALL requirement for detecting silent dedicated-repo metadata changes (rename, visibility change, default-branch swap) that would break all user installations. The three Minor findings concern operational governance gaps. Overall assessment: **REVISE** — the Phase-2 design is structurally sound but two internal requirement contradictions must be resolved before Phase-5 implementation can proceed correctly.

---

## Goals and Inversions

| # | Goal (explicit / inferred) | Anti-Goal: "To GUARANTEE failure..." | Coverage in Design |
|---|---------------------------|--------------------------------------|-------------------|
| G-001 | Installable under CoWork file limit (REQ-001, REQ-034) | Ship skeleton whose count or pack size exceeds the actual runtime limit | Partially closed: file-count gate REQ-006 + pack-size hard-fail REQ-034d; R-001 dimension (d) smoke-test MAY be deferred |
| G-002 | Bit-identical determinism / idempotency (REQ-003, ADR-001 c-001/c-002) | Let any dynamic value (timestamp, run ID, short SHA) enter the commit tree or message | Closed: static stub REQ-004a, pinned dates, full 40-char SHA |
| G-003 | No silent compromise (ADR-003 D2/D4/D5) | Deliver unauthorized content without any alert within a bounded window | Partially closed: D2 prevents direct-push; D5 closes rogue tag; residual paths (credential theft, admin suppression) rely on the backstop monitor |
| G-004 | Supply-chain integrity via attestation (D4, REQ-042) | Produce an attestation that is never verified, or one that cannot be created at all | **Gap**: REQ-020 blocks permission needed to create attestation; monitor verification mechanism ambiguous |
| G-005 | Branch currency / anti-staleness (NFR-003, NFR-006) | Let a silent CI failure leave the dedicated repo stale indefinitely without alert | Closed for scheduled detection (daily backstop + meta-monitor); event-driven fast path is architecturally problematic |
| G-006 | Maintainability / reversibility (ADR-001 c-005, REQ-043) | Create operational knowledge gaps that make recovery impossible without the original author | Partially closed: runbooks required, but no rotation-interval mandate and no runbook-currency requirement |

---

## Assumption Map

| ID | Assumption | Type | Confidence | Validation | Consequence if Wrong |
|----|-----------|------|------------|------------|----------------------|
| A-001 | GitHub immutable releases + attestation + ruleset bypass-actor semantics are available and behave as documented (2025-2026 GA features) | Technical | Medium | Cited vendor docs; NOT yet empirically confirmed on geekatron/jerry-cowork (ADR-003 Negative #4) | D4 integrity anchor fails; fall back to deploy-key + scheduled-monitor posture |
| A-002 | `gh attestation attest` can execute within workflow permissions as specified in REQ-020 (`contents: write` only) | Technical | **Low** | NOT validated — `id-token: write` is required per GitHub OIDC attestation spec, explicitly forbidden by REQ-020 | Attestation step fails at runtime; primary integrity anchor (D4) never created |
| A-003 | The backstop monitor verifies the live tip SHA using `gh attestation verify`, not merely a Release-notes SHA string comparison | Technical | **Low** | NFR-006/REQ-035 text still describes Release-notes retrieval; ADR-003 L1 says "verify against attestation" — contradictory | Monitor uses collapsed Phase-1 anchor (editable Release notes) instead of Sigstore; SC-04 re-opens |
| A-004 | A GitHub Actions workflow in the SOURCE repo can be triggered by push events to the DEDICATED repo | Technical | **Low** | GitHub Actions does not natively support cross-repo event subscriptions; REQ-035a specifies `on: push: branches: [<dedicated-repo-default-branch>]` | Event-driven fast path cannot exist in source repo; must live in dedicated repo (requiring workflows there) or not at all |
| A-005 | Dedicated-repo visibility changes and default-branch rename/deletion will be detected promptly | Process | **Low** | No SHALL requirement mandates monitoring these; only ADR-003 D2 prose mentions it ("monitor on default-branch name and repo visibility") | Visibility → private or branch rename silently breaks all user installations; no alert fires |
| A-006 | App private key / deploy key is rotated on a defined schedule preventing extended exposure after potential compromise | Process | **Low** | No SHALL requirement specifies a rotation interval; c-208 says "rotation policy" without schedule | Compromised key allows silent sustained unauthorized pushes until discovered by other means |
| A-007 | `v*` tag protection only permits "designated maintainers" — a well-defined, governed set of principals | Process | Medium | REQ-039 uses phrase "designated maintainers" with no definition, governance process, or periodic review requirement | Scope creep: unauthorized principals gain tag-creation rights; D5 provenance gate weakened |
| A-008 | `git merge-base --is-ancestor` in CI uses a freshly fetched `origin/main` that accurately reflects the protected main branch | Technical | High | Logically sound given ADR-001 IT3-005 event-discriminated TAG resolution; main is ruleset-protected | Low risk |
| A-009 | The dedicated-repo branch protection ruleset cannot be overridden by org OWNERS (only repo admins are blocked) | Technical | Medium | GitHub org-level rulesets CAN be modified by org owners; design relies on admin-minimization + audit alerts (DR-02) | An org owner can suppress protection; direct-push reverts from prevention to detection |
| A-010 | The R-001 CoWork smoke-test (dimension d) will be completed before Phase-5 implementation | Process | Medium | REQ-034 MAY defer dimension (d) to Phase 4; Phase-5 blocked until complete | Skeleton distribution fails silently for users if actual CoWork limit is size/time-based |
| A-011 | Stripping `tests/` does not remove any file referenced by hooks, skills, or src/ at runtime | Technical | High | REQ-010 checks plugin.json agent paths; no analogous check for runtime file references in src/ or hooks/ | Silent runtime failure in CoWork session if any retained component imports from tests/ |
| A-012 | ADR-001's canonical retention surface list is correct and consistent — both the amendment header and the body agree on what is stripped | Documentation | **Low** | REQ-005 explicitly flags that ADR-001 body says "tests/ retained today (1,744 ≪ 5,000)" while amendment header and ADR-003 strip it | Maintainer following ADR-001 body text alone omits tests/ strip; unexpected file count |
| A-013 | REQ-043's two-admin-approval requirement for registration changes is technically enforceable via GitHub's org settings | Process | Medium | GitHub org marketplace registration settings may not support a native two-approver gate; the requirement may be policy-only | Registration changes proceed with one actor; runbook is the sole control |
| A-014 | The meta-monitor (REQ-044) correctly asserts the scheduled backstop ran — not just that a run appeared successful while being suppressed | Technical | Medium | GitHub Actions workflow run status can be marked successful by an attacker with CI access; the meta-monitor checks liveness not correctness | Watchdog confirms the compromised monitor is "running fine"; suppression goes undetected |

---

## Findings Table

| ID | Inverted Goal / Failed Assumption | Type | Confidence | Severity | Affected Deliverable | Dimension |
|----|----------------------------------|------|------------|----------|----------------------|-----------|
| IN-001-it4 | A-002: REQ-020 blocks `id-token: write` required for REQ-042 attestation | Assumption | Low | **Major** | REQ-020 vs. REQ-042, ADR-003 D4 | Methodological Rigor |
| IN-002-it4 | A-004: Event-driven fast path (REQ-035a) cannot be triggered cross-repo | Assumption | Low | **Major** | REQ-035, NFR-006, ADR-003 D4 | Internal Consistency |
| IN-003-it4 | A-003: Backstop monitor verification mechanism ambiguous — Release notes vs. attestation | Assumption | Low | **Major** | NFR-006, REQ-035, ADR-003 D4 | Evidence Quality |
| IN-004-it4 | A-005: No SHALL requirement for dedicated-repo metadata change monitoring | Anti-Goal | N/A | **Major** | REQ-040, ADR-003 D2 | Completeness |
| IN-005-it4 | A-006: App private key / deploy-key rotation interval unspecified | Assumption | Low | Minor | c-208, REQ-041, ADR-003 D3 | Actionability |
| IN-006-it4 | A-007: "Designated maintainers" for v* tag protection undefined | Assumption | Medium | Minor | REQ-039, ADR-003 D5 | Completeness |
| IN-007-it4 | A-012: ADR-001 body text contradicts Phase-2 amendment on tests/ strip | Assumption | Low | Minor | ADR-001 §Canonical Plugin-Retention Surface | Internal Consistency |

---

## Detailed Findings

### IN-001-it4: REQ-020 Prohibits `id-token: write` Required by Attestation (REQ-042) [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption (A-002) |
| **Inverted Goal** | G-004 Supply-chain integrity via attestation |
| **Inversion** | "To guarantee the attestation is never created" → "Keep REQ-020 as written; `gh attestation attest` fails at runtime" |
| **Plausibility** | HIGH — GitHub's OIDC-based Sigstore attestation (`gh attestation attest`) requires `id-token: write` (OIDC token endpoint) in the calling workflow. REQ-020 explicitly lists `id-token: write` as forbidden. |
| **Affected Deliverable** | REQ-020 (WS-3) and REQ-042 (WS-3 Phase-2), ADR-003 D4 |
| **Dimension** | Methodological Rigor |

**Evidence:**

REQ-020 states: "The `permissions:` block in `cowork-skeleton.yml` SHALL declare `contents: write` as the sole permission entry and SHALL NOT include `actions: write`, `packages: write`, `id-token: write`, or any organization-level scope."

ADR-003 D4 states: "We will anchor artifact integrity in a GitHub immutable release plus a build-provenance attestation (Sigstore-backed, immutable public transparency log; SLSA-aligned) produced by CI..."

REQ-042 states: "The CI workflow SHALL create an immutable GitHub Release and a build-provenance attestation (Sigstore-backed, SLSA-aligned, e.g., `gh attestation`)..."

GitHub's `gh attestation attest` command and the `actions/attest-build-provenance` Action both require `id-token: write` to obtain an OIDC token from GitHub's OIDC endpoint, which is the mechanism by which Sigstore receives a verifiable identity assertion for signing.

**Analysis:**

REQ-020 was authored for Phase-1 and correctly restricted permissions to `contents: write` for the source-repo-only force-push. Phase-2 added REQ-042 (attestation) without updating REQ-020 to accommodate it. The result is that both requirements cannot be simultaneously satisfied: a workflow with only `contents: write` cannot call `gh attestation attest` successfully. If REQ-020 is taken as written, `cowork-skeleton.yml` will fail the attestation step at Phase-5 implementation. If REQ-020 is ignored to permit attestation, the implementation violates an explicit security requirement. The primary integrity anchor (D4, resolving the 5-strategy SC-04 Critical) is unimplementable as specified.

A secondary question is whether `attestations: write` (a newer permission scope used by some GitHub attestation workflows) could substitute for `id-token: write`; either way, REQ-020's prohibition blocks it.

**Recommendation:**

Amend REQ-020 to permit the minimal additional permission set required for attestation (`id-token: write` or `attestations: write`, scoped to the attestation job step only). Confirm the exact permission requirement empirically in the Phase-5 implementation environment before Phase-5 begins. Acceptance criteria: `gh attestation attest` completes without permission error on a test run; the workflow `permissions:` block is updated with explicit justification referencing REQ-042.

---

### IN-002-it4: Event-Driven Fast Path (REQ-035a) Cannot Be Triggered Cross-Repo [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption (A-004) |
| **Inverted Goal** | G-003 No silent compromise / G-005 Branch currency |
| **Inversion** | "To guarantee a malicious push to the dedicated repo goes undetected for ≥ 25 hours" → "Make the event-driven fast path architecturally impossible so only the daily scheduled backstop runs" |
| **Plausibility** | HIGH — GitHub Actions workflows in a source repo cannot subscribe to push events in a different repository using the standard `on: push: branches:` trigger. |
| **Affected Deliverable** | REQ-035 (event-driven leg), NFR-006, ADR-003 D4 |
| **Dimension** | Internal Consistency |

**Evidence:**

REQ-035 specifies: "(a) Event-driven fast path — on `on: push: branches: [<dedicated-repo-default-branch>]`; retrieve the published SHA from Release notes and assert `git rev-parse HEAD` equals it; mismatch SHALL create a GitHub issue and exit non-zero."

ADR-003 §Loop-Safety (CR-02) states: "the dedicated repo has no push-back workflows (read/monitor only)" and "This invariant must be asserted in config and review."

ADR-003 D2 residual modes: "Extra-actor addition (DR-03) is bounded by periodic access review." The topology diagram shows the dedicated repo with "no push-back workflows (loop-safety by topology)."

**Analysis:**

GitHub Actions' `on: push: branches:` trigger fires only when the repository HOSTING the workflow receives a push matching the branch pattern. A workflow in `geekatron/jerry` cannot fire on pushes to `geekatron/jerry-cowork`. For REQ-035a to work, the workflow must live in the dedicated repo.

However, if the dedicated repo hosts monitoring workflows, this creates tension with the "no workflows" premise of the loop-safe topology (ADR-003 CR-02). The design distinguishes "no push-back workflows" (not all workflows), so read-only monitor workflows in the dedicated repo are technically permissible by REQ-023's text. But this is not stated anywhere as the intended implementation, and it creates a new surface: any workflow in the dedicated repo using the cross-repo credential could potentially write back to the source repo if misconfigured.

The result: REQ-035a's "event-driven fast path" either (a) does not exist (detection window is ≤25h, not "within minutes"), or (b) requires an undocumented monitoring workflow in the dedicated repo. Neither is currently specified. A designer implementing REQ-035a in the source repo will fail; one who adds it to the dedicated repo has no requirement mandating that workflow's scope, permissions, or write-back prohibition.

**Recommendation:**

Clarify the architecture for REQ-035a: (1) explicitly decide whether the event-driven fast path lives in the dedicated repo as a read-only workflow, (2) if yes, add a requirement mandating that the dedicated-repo monitoring workflow has no `contents: write` permission on the source repo, or (3) retire the event-driven fast path and acknowledge that the detection SLA is ≤25h (scheduled backstop). Update ADR-003 D4 and the topology diagram to reflect the chosen architecture. Acceptance criteria: the implementation architecture for REQ-035a is unambiguously specified; no workflow in the dedicated repo has write access to the source repo.

---

### IN-003-it4: Backstop Monitor Verification Mechanism Ambiguous — Release-Notes SHA vs. Attestation [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption (A-003) |
| **Inverted Goal** | G-004 Supply-chain integrity via attestation |
| **Inversion** | "To guarantee the attestation is never verified in production" → "Write the monitoring requirement to describe Release-notes SHA retrieval while adding a clause claiming it re-points to attestation" |
| **Plausibility** | HIGH — the ambiguity already exists in the requirement text as written. |
| **Affected Deliverable** | NFR-006, REQ-035 (both WS-3), ADR-003 D4 |
| **Dimension** | Evidence Quality |

**Evidence:**

NFR-006 (Phase-2 update): "...tamper-detection check (≤ daily cadence — the explicit detection SLA) — retrieve the expected deterministic tip SHA from the **GitHub Release notes** for the latest v* tag (per REQ-035) and assert that `git rev-parse HEAD` on the dedicated repo equals it; **re-point anchor from editable Release-notes text to the immutable attestation (REQ-042)** as the primary integrity reference..."

The same requirement sentence instructs both "retrieve from Release notes" AND "re-point to attestation" — these are contradictory. The retrieval mechanism (Release-notes SHA string) is unchanged from Phase-1; only a closing clause asserts a re-point without changing the mechanism.

ADR-003 D4 states unambiguously: "Verification compares against the attestation, NEVER against editable Release-notes text."

REQ-035 acceptance criterion (b): "Simulate a direct push... confirm the event-driven monitor fires, detects the SHA mismatch, creates a GitHub issue." This criterion does not specify that `gh attestation verify` is used; it is satisfied by comparing `git rev-parse HEAD` to a Release-notes SHA string.

**Analysis:**

An implementer following the acceptance criterion of REQ-035 (detect SHA mismatch → create issue) can satisfy it entirely via Release-notes SHA comparison — the same mechanism that collapsed in Phase-1 (SC-04). The collapsed anchor was: Release notes are editable with `contents: write`. If the backstop monitor uses Release-notes SHA comparison instead of `gh attestation verify`, the primary integrity anchor is the Release notes — not the Sigstore attestation. The ADR-003 claim that SC-04 is resolved depends on the backstop actually calling `gh attestation verify`, but no requirement mandates this.

Additionally, `gh attestation verify` requires a different permission than `contents: write` and needs GitHub CLI access. If the monitoring workflow runs with only `contents: write`, it may not be able to execute `gh attestation verify` — the same permission gap as IN-001-it4.

**Recommendation:**

Rewrite NFR-006's tamper-detection mechanism to explicitly mandate `gh attestation verify <tip-sha> --repo geekatron/jerry` as the verification step, replacing the Release-notes SHA retrieval. Update REQ-035's acceptance criterion to require that the acceptance test invokes `gh attestation verify` and confirms it exits zero. Confirm that the monitoring workflow has the permissions needed for this command. Acceptance criteria: NFR-006 contains no mention of Release-notes SHA as the comparator for tamper-detection; the acceptance test explicitly exercises `gh attestation verify`.

---

### IN-004-it4: No SHALL Requirement for Dedicated-Repo Metadata Change Monitoring [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Anti-Goal |
| **Inverted Goal** | G-005 Branch currency / G-003 No silent compromise |
| **Inversion** | "To guarantee a silent stale or broken install for all users" → "Change the dedicated repo visibility to private, rename the default branch, or delete the repo — no alert fires" |
| **Plausibility** | MEDIUM — requires admin access, but no technical control prevents it and no detection requirement covers it. |
| **Affected Deliverable** | REQ-040, ADR-003 D2 (residual modes) |
| **Dimension** | Completeness |

**Evidence:**

ADR-003 D2 (residual modes): "Default-branch swap / rename / delete / make-private (DR-04/05) are bounded by org ownership controls, a monitor on default-branch name and repo visibility, and a recovery runbook."

REQ-040 specifies only: "default branch SHALL be protected by an org-level ruleset... repo admins SHALL NOT be able to override the org-level ruleset." REQ-040 contains no requirement to monitor repo visibility, default-branch name, or repo existence.

No requirement across REQ-038–044 or NFR-001–006 mandates alert-on-visibility-change, alert-on-default-branch-rename, or periodic repo-existence verification. The closest is REQ-043 (quarterly audit of registered source), which checks whether the org registration points to the correct repo — but does not check whether the repo itself is still public, still named `geekatron/jerry-cowork`, and still has the correct default branch name.

**Analysis:**

The following changes to the dedicated repo would silently break ALL org users' installations:
- Repo renamed (`geekatron/jerry-cowork` → anything else): CoWork clones the registered URL, which now 404s.
- Repo made private: CoWork cannot clone; all installs fail with no user-facing explanation tied to the cause.
- Default branch renamed: CoWork clones the default branch (per confirmed install mechanism), gets unexpected content.

All three require admin access, and ADR-003 D2 mentions monitoring them. But without a SHALL requirement, the monitoring is aspirational. The org-level ruleset (REQ-040) protects against unauthorized pushes to the branch but cannot prevent an org owner from renaming the repo or changing its visibility — these are settings changes, not push events.

**Recommendation:**

Add a SHALL requirement (proposed: REQ-045) mandating a scheduled monitor that verifies (a) `geekatron/jerry-cowork` is public via GitHub API, (b) the default branch name matches the expected value, and (c) the repo exists and is accessible. Alerts (GitHub issues) on any mismatch. Run at ≤ weekly cadence. Acceptance criteria: the monitor detects and alerts within one scheduled cycle on a simulated visibility change or repo rename.

---

### IN-005-it4: App Private Key / Deploy-Key Rotation Interval Unspecified [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Assumption (A-006) |
| **Inverted Goal** | G-003 No silent compromise |
| **Inversion** | "To guarantee persistent unauthorized push capability after key theft" → "Never rotate the key; 'rotation policy' exists only as a prose clause with no enforced interval" |
| **Plausibility** | MEDIUM — key rotation is a recognized operational gap in long-lived projects. |
| **Affected Deliverable** | ADR-003 D3 (c-208), REQ-041 |
| **Dimension** | Actionability |

**Evidence:**

ADR-003 D3 / c-208: "stored only in source-repo secrets with minimal access and a rotation policy." REQ-041 mentions "rotation schedule if used" for deploy keys. Neither specifies a maximum rotation interval.

ADR-003 Negative #1: "Theft enables durable forgery of the artifact (CR-03). Mitigation: source-repo secrets only, minimal access, rotation; short-lived App tokens; deploy-key confinement."

**Analysis:**

A GitHub App's private key is a long-lived secret. GitHub App installation tokens are short-lived (~1h), but the private key that mints them is not. If the private key is compromised, an attacker can mint arbitrarily many short-lived tokens and push to the dedicated repo at will. Without a defined rotation interval (e.g., annually or on personnel change), the "rotation policy" is unenforceable. For deploy keys, GitHub has no built-in expiry; rotation is entirely manual.

**Recommendation:**

Add to REQ-041 (or a sub-requirement): "The App private key SHALL be rotated at minimum every 12 months, or immediately on any personnel change affecting access to source-repo secrets, whichever is sooner. Deploy keys SHALL be rotated on the same schedule. The rotation schedule SHALL be documented in the org-registration runbook (REQ-043)." Acceptance criteria: runbook contains explicit rotation schedule; rotation event is verifiable in GitHub's App audit log.

---

### IN-006-it4: `v*` Tag Protection "Designated Maintainers" Scope Undefined [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Assumption (A-007) |
| **Inverted Goal** | G-003 No silent compromise (via rogue tag) |
| **Inversion** | "To guarantee a rogue v* tag can be created without bypassing the provenance assertion" → "Add yourself to the 'designated maintainers' list — an undefined, ungoverned set" |
| **Plausibility** | LOW-MEDIUM — requires some level of access, but governance gap is real. |
| **Affected Deliverable** | REQ-039, ADR-003 D5 |
| **Dimension** | Completeness |

**Evidence:**

REQ-039: "restricting `v*` tag creation to the release pipeline (CI bot) and **designated maintainers only**; unauthorized `v*` tag creation by arbitrary collaborators SHALL be blocked."

"Designated maintainers" is used without definition in REQ-039, ADR-003 D5, or anywhere in the requirements. No requirement specifies who may be a designated maintainer, how they are added/removed, or how often the list is audited.

**Analysis:**

Tag protection rulesets on GitHub can bypass the check: who is on the bypass list? REQ-039 says "CI bot + designated maintainers" — if this bypass list is informal and unaudited, it may expand over time. D5 is the "top residual" per ADR-003; weakening it silently increases SC-02 risk. The inversion: to guarantee a rogue tag could eventually be created, gradually add team members as "designated maintainers" until the list is large enough that a social-engineering or credential-theft attack on any one of them succeeds.

**Recommendation:**

Amend REQ-039 to define: (a) a maximum number of bypass principals for `v*` tag creation (e.g., ≤ 3 named maintainers plus the CI bot), (b) a governance process for adding/removing principals (e.g., matching the two-approver threshold in REQ-043), and (c) a periodic review cadence (≤ quarterly). Acceptance criteria: the `v*` tag protection ruleset bypass list has ≤ N named principals; the list is reviewed on a documented schedule.

---

### IN-007-it4: ADR-001 Body Text Contradicts Phase-2 Amendment on `tests/` Strip [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Assumption (A-012) |
| **Inverted Goal** | G-006 Maintainability |
| **Inversion** | "To guarantee a maintainer omits the tests/ strip and ships an oversized skeleton" → "Leave the authoritative ADR-001 body saying tests/ is retained while the amendment header says it is stripped" |
| **Plausibility** | LOW — a careful reader will reconcile the amendment; less careful ones may be confused. |
| **Affected Deliverable** | ADR-001 §Canonical Plugin-Retention Surface |
| **Dimension** | Internal Consistency |

**Evidence:**

ADR-001 §Canonical Plugin-Retention Surface (body text): "by contrast `docs/`, `runbooks/`, `overrides/`, `scripts/`, `tests/` are NOT load-bearing for plugin function and MAY be stripped later if the file-count margin tightens (R-002) — **but are retained today (1,744 ≪ 5,000)**."

ADR-001 Phase-2 amendment header (2026-06-28): "the strip set is extended to include `tests/`."

ADR-003 pipeline specification: "`git rm -r projects/ tests/`."

REQ-002: "SHALL strip the `projects/` directory AND the `tests/` directory entirely."

REQ-005 notes: "**Note for ps-architect (ADR-001 inconsistency):** ADR-001's body (§Canonical Plugin-Retention Surface) says `tests/` is 'retained today (1,744 ≪ 5,000)'..."

**Analysis:**

The body of ADR-001 — the section specifically titled as the canonical and authoritative retention surface list — states tests/ is retained. The amendment modifies this decision in a header addendum. An implementer reading only the body text of ADR-001 §Canonical Plugin-Retention Surface (the labeled SSOT for c-003) would believe tests/ is retained and omit the strip. The file count would then be ~1,744 instead of ~1,417, still under 5,000 but inconsistent with all other documents. This also means the generated commit SHAs would differ from those verified in QG-2 testing.

**Recommendation:**

Update ADR-001 §Canonical Plugin-Retention Surface body text to explicitly remove the "retained today" clause for `tests/` and replace it with "stripped as of Phase-2 amendment (2026-06-28) per ADR-003 pipeline specification." REQ-005 removes its flag note once the body is corrected. Acceptance criteria: no internal contradiction between ADR-001's body and amendment header on the strip set; grep for "retained today" in ADR-001 returns no result applying to tests/.

---

## Recommendations

### MUST Mitigate (Major)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| IN-001-it4 | Amend REQ-020 to permit the minimal permission set (`id-token: write` or `attestations: write`) required by `gh attestation attest`, scoped to the attestation step. Confirm empirically before Phase-5. | `gh attestation attest` completes without permission error; REQ-020 updated with explicit justification referencing REQ-042. |
| IN-002-it4 | Clarify the REQ-035a event-driven fast path architecture: decide whether it lives in the dedicated repo as a read-only workflow or is retired in favor of ≤25h scheduled backstop. Document the chosen architecture in ADR-003 D4 and REQ-035. | REQ-035a has an unambiguous implementation target; if retained, the dedicated-repo workflow has no source-repo write permissions (verifiable by Inspection). |
| IN-003-it4 | Rewrite NFR-006 tamper-detection mechanism to mandate `gh attestation verify <tip-sha> --repo geekatron/jerry`; remove Release-notes SHA as the comparator; update REQ-035 acceptance criterion to require `gh attestation verify` invocation. | NFR-006 and REQ-035 contain no Release-notes SHA retrieval for tamper-detection; acceptance test explicitly exercises attestation verification. |
| IN-004-it4 | Add REQ-045 mandating a scheduled monitor for dedicated-repo visibility, default-branch name, and repo existence; alert (GitHub issue) on any mismatch; run ≤ weekly. | Monitor detects and alerts within one scheduled cycle on a simulated visibility change or repo rename (Demonstration). |

### SHOULD Mitigate (Minor)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| IN-005-it4 | Add explicit rotation interval (≤ 12 months or on personnel change) to REQ-041 for App private key and deploy key; document in org-registration runbook. | REQ-041 contains explicit SHALL rotation interval; runbook section documents rotation schedule. |
| IN-006-it4 | Define "designated maintainers" in REQ-039: maximum count, governance process, review cadence. | REQ-039 specifies maximum bypass-principal count and review schedule; ruleset bypass list is auditable. |
| IN-007-it4 | Correct ADR-001 §Canonical Plugin-Retention Surface body text to remove "retained today" for tests/. | No contradiction between ADR-001 body and amendment header on tests/ strip (Inspection). |

---

## Scoring Impact

| Dimension | Weight | Impact | Finding(s) | Rationale |
|-----------|--------|--------|-----------|-----------|
| Completeness | 0.20 | **Negative** | IN-004-it4, IN-006-it4 | Missing SHALL requirements for repo-metadata monitoring (DR-04/05) and undefined governance scope for designated maintainers leave audit obligations unformalized |
| Internal Consistency | 0.20 | **Negative** | IN-002-it4, IN-007-it4 | REQ-035a event-driven path is architecturally inconsistent with the no-workflow dedicated-repo topology; ADR-001 body contradicts its own amendment on tests/ strip |
| Methodological Rigor | 0.20 | **Negative** | IN-001-it4 | Attestation-based integrity anchor (resolving SC-04 Critical) is unimplementable under REQ-020's permission restriction; the primary integrity control cannot execute |
| Evidence Quality | 0.15 | **Negative** | IN-003-it4 | NFR-006/REQ-035 monitoring mechanism is textually ambiguous — Release-notes SHA retrieval vs. `gh attestation verify` — undermining the claim that the backstop actually verifies the Sigstore anchor |
| Actionability | 0.15 | **Negative** | IN-005-it4 | App private key rotation interval is unspecified; "rotation policy" is aspirational without a defined schedule |
| Traceability | 0.10 | Neutral | — | Traceability from ADR decisions to requirements is sound; all Phase-2 decisions have corresponding SHALL requirements (REQ-038–044); findings are gaps in those requirements' internal logic, not missing traces |

**Overall impact:** Four Major findings across four different scoring dimensions indicate targeted revisions are required to the requirements documents. None of the findings invalidates the core architectural approach (dedicated repo + attestation + provenance gate + protection ruleset). The Phase-2 hardening is structurally sound; the gaps are within the requirements' own internal consistency and completeness, not in the threat model or the control selection.

---

*Generated by: jerry:adv-executor (blind, independent — Group E Decompose)*
*Strategy: S-013 Inversion Technique (template: .context/templates/adversarial/s-013-inversion.md)*
*Template Finding Prefix: IN-NNN-{execution_id}, execution_id = it4*
*Deliverables reviewed: ADR-001, ADR-003, phase1-requirements.md*
*Supporting (not reviewed): security/phase2-stride-threat-model.md, security/phase2-attack-surface.md*
*H-15 Self-Review: Applied before persistence — all findings have specific evidence; severity classifications justified; finding identifiers consistent; summary table matches detailed sections; no findings minimized.*
*Constitutional Compliance: P-001 (evidence-based), P-002 (persisted to file), P-003 (no subagents), P-004 (provenance cited), P-011 (evidence per finding), P-022 (severity not inflated or minimized)*
