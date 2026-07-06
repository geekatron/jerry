# Strategy Execution Report: S-001 Red Team Analysis

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy metadata, deliverables, timestamp |
| [Threat Actor Profile](#threat-actor-profile) | Adversary goal, capability, motivation |
| [Findings Summary](#findings-summary) | RT-001 through RT-008 severity table |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, countermeasure per finding |
| [Defense Gap Assessment](#defense-gap-assessment) | Prioritization matrix per finding |
| [Scoring Dimension Impact](#scoring-dimension-impact) | Mapping findings to S-014 dimensions |
| [Overall Assessment](#overall-assessment) | Remediation verdict and ordering |
| [Execution Statistics](#execution-statistics) | Counts and protocol completion |

---

## Execution Context

| Attribute | Value |
|-----------|-------|
| **Strategy** | S-001 Red Team Analysis |
| **Execution ID** | I3 (Iteration 3, Group C — Challenge) |
| **Template** | `.context/templates/adversarial/s-001-red-team.md` v1.0.0 |
| **Deliverable 1** | `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md` (Iteration 3) |
| **Deliverable 2** | `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md` (Iteration 3) |
| **Deliverable 3** | `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md` (Iteration 3) |
| **Grounding** | `projects/PROJ-031-cowork-skeleton/research/phase1-skeleton-ci-research.md`; `PLAN.md` |
| **H-16 Compliance** | S-003 Steelman was applied prior to this strategy (C4 tournament ordering; adv-executor confirms prior strategies ran before S-001 per the tournament sequence) |
| **Reviewer Role** | BLIND, INDEPENDENT — Group C (Challenge). No prior iteration output read. |
| **Executed** | 2026-06-26 |
| **Iteration under review** | Iteration 3 defenses: async publish-then-assert integrity monitoring (REQ-035/NFR-006), tag sanitization (REQ-036), push-failure detection (REQ-037), non-forgeable SHA tamper-detection (NFR-006/ADR-002 §IT3-004) |

---

## Threat Actor Profile

| Field | Value |
|-------|-------|
| **Actor** | Malicious repository collaborator with write access (or a supply-chain actor who has compromised such a collaborator's credentials) |
| **Goal** | Install unauthorized executable content (hooks) on CoWork users' workstations via the `cowork-skeleton` branch, OR persistently evade the monitoring layer so that tampered content remains installed without detection |
| **Capability** | Full source-code read access (public ADR architecture is readable); GitHub `write` collaboration level (can push branches and tags, can create/edit releases via API, can call `gh release edit`); knowledge of the publish-then-assert integrity model from public ADR-002 |
| **Motivation** | Supply-chain compromise: `hooks/session-start.py` executes on every CoWork session start on user workstations; persistent hook injection is high-value. Detection evasion makes the window indefinite. |
| **Threat Vector Scope** | The actor targets the integrity model's reference surface (GitHub Release notes), the monitoring architecture (event-driven + scheduled), and the CI-trusted tag input path — not the `GITHUB_TOKEN` credential itself (that credential design is sound) |

---

## Findings Summary

| ID | Severity | Finding | Deliverable Section |
|----|----------|---------|---------------------|
| RT-001-I3 | **Critical** | Release notes are NOT a protected reference surface — same `contents: write` permission covers both branch push and release edit | ADR-002 §Continuous Integrity Monitoring; REQ-035 |
| RT-002-I3 | **Critical** | Named compensating control (integrity monitoring) provides zero detection for CI-triggered generation from an attacker-created well-formed `v*` tag | ADR-001 §Tag-name sanitization RT-003; ADR-002 §Continuous Integrity Monitoring |
| RT-003-I3 | **Major** | SHA-publish step failure leaves monitor with no reference value; NFR-006 and REQ-035 do not specify monitor behavior in this case, creating a potential perpetual blind spot | REQ-035 AC; NFR-006 AC |
| RT-004-I3 | **Major** | Admin-level actor can disable the monitor workflow, push malicious content, and re-enable — event-driven detection has no retroactive catch; scheduled backstop only provides ≤-daily coverage | NFR-006; REQ-035; ADR-002 §Continuous Integrity Monitoring |
| RT-005-I3 | **Major** | Monitor workflow has no self-health alerting requirement — if it fails to run (Actions outage, permission revocation), the effective tamper-detection SLA becomes unbounded with no notification | NFR-006; REQ-037 (analog absent for monitor) |
| RT-006-I3 | **Minor** | Fixed ≤-daily detection SLA is non-adaptive — no mechanism to tighten cadence as collaborator count grows or hook sensitivity increases | NFR-006; ADR-002 §Detection SLA |
| RT-007-I3 | **Minor** | Blank-input fallback error message is cryptic — empty-string tag failure message indistinguishable from injection-payload failure | REQ-036 AC |
| RT-008-I3 | **Minor** | Issue notification fidelity gap — no requirement for title, labels, assignees, or mention targets on the mismatch alert issue | REQ-035 AC; NFR-006 AC |

---

## Detailed Findings

### RT-001-I3: Release Notes Are Not a Protected Reference Surface

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR-002 §Continuous Integrity Monitoring; REQ-035 |
| **Strategy Step** | Step 2 (Attack Vector: Boundary Violations / Dependency Attacks) |
| **Exploitability** | High — attack requires only repository write access, which the defined threat actor (RT-01) already possesses |
| **Defense Status** | Missing — no requirement prevents a collaborator from calling `gh release edit` to overwrite the reference SHA |

**Evidence:**

ADR-002 §Continuous Integrity Monitoring states:

> "(1) Publish (synchronous, in `cowork-skeleton.yml`). After the force-push, CI publishes the expected deterministic tip SHA for the release to a **durable, off-branch, protected surface** — the GitHub **Release notes** for the `v*` tag (Releases are governed by `main`/release permissions, not by the unprotected branch)."

REQ-035 repeats this characterization: "publish the expected deterministic tip SHA for the release tag to the GitHub Release notes for that tag (e.g., `gh release edit v{TAG} --notes-append ...`) as a durable, off-branch, protected reference value."

**Analysis:**

The "protected surface" claim is architecturally false. GitHub Release notes are edited via the API using `contents: write` permission — the same permission scope held by:
(a) the `cowork-skeleton.yml` workflow (`permissions: contents: write`, per REQ-020/NFR-004), and
(b) any repository collaborator with "write" access — the same set of actors who can push directly to the unprotected `cowork-skeleton` branch (the defined RT-01 threat).

The distinguishing property of Release notes over the branch is that they cannot be corrupted by a branch push — but they CAN be overwritten via `gh release edit v{N} --notes "cowork-skeleton-sha: <attacker_sha>"`, which replaces the notes body and requires only `contents: write`.

**Attack chain:** A write-access collaborator who knows the ADR-002 architecture (public document) (1) pushes malicious content to `cowork-skeleton` directly; (2) immediately calls `gh release edit v{CURRENT_TAG} --notes "cowork-skeleton-sha: <malicious_sha>"`, replacing the reference SHA in the Release notes with the malicious tip SHA; (3) the scheduled monitor later retrieves the Release notes SHA, finds it matches the live tip → no mismatch → no alert. The event-driven monitor fires from the direct push (non-GITHUB_TOKEN) and IS likely to catch this — but only if it runs before step (2). The attacker can sequence step (2) before step (1) to eliminate that race.

**Phase-1 vs Phase-2 classification:** This is a **Phase-1 requirements defect** — the architectural claim that Release notes are a "protected surface" is embedded in the requirements (REQ-035) and must be corrected or the monitoring model must be redesigned. It is not a Phase-2 implementation detail.

**Recommendation:**

Replace GitHub Release notes with a genuinely more-protected reference surface. Options:
- **GitHub Actions Artifacts** (immutable once uploaded, not editable without admin access and a separate API scope) — store the expected SHA as a signed artifact of the `cowork-skeleton.yml` run.
- **Require `releases: write` as a separate, narrowly-granted workflow scope** distinct from `contents: write`, combined with a branch protection ruleset that grants `contents: write` for branch push but not release editing to collaborators. (GitHub fine-grained PAT scopes distinguish these; classic PATs and GITHUB_TOKEN do not.)
- **HMAC-sign the expected SHA** using a secret known only to CI and stored in GitHub Secrets (not editable without `secrets: write`). The monitor verifies the signature before trusting the reference value.
- Alternatively: acknowledge that the reference surface is equally trusted as the branch, and escalate to **branch protection + bypass actor** (the documented upgrade path in ADR-002) as the only prevention control.

---

### RT-002-I3: Named Compensating Control Is Blind to CI-Triggered Malicious Generation

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR-001 §Tag-name sanitization RT-003; ADR-002 §Continuous Integrity Monitoring |
| **Strategy Step** | Step 2 (Attack Vector: Rule Circumvention / Dependency Attacks) |
| **Exploitability** | Medium — requires write access to push both a commit AND a well-formed `v*` tag (no tag-protection ruleset exists per ADR-002 §Empirical finding) |
| **Defense Status** | Missing — the monitoring architecture provides no detection for this specific attack vector despite ADR-001 explicitly naming it as a compensating control |

**Evidence:**

ADR-001 §Tag-name sanitization states:

> "asserting that the resolved tag points at a commit reachable from `main` / produced by the release pipeline is a **provenance** control... and is delegated to the Phase-2 STRIDE threat model (STORY-004). Phase 1 commits only to syntactic safety here; the **deterministic-SHA integrity monitoring (ADR-002 §Continuous Integrity Monitoring) is the compensating detective control for a wrong-but-well-formed tag.**"

No tag-protection ruleset is documented; the only active ruleset ("Don't fuck with main", id 12387947) targets `~DEFAULT_BRANCH` with `non_fast_forward`, `deletion`, `pull_request` rules — none of which is tag protection. `cowork-skeleton` is unprotected; there is no documented protection on `v*` tag pushing.

**Analysis:**

The named compensating control ("deterministic-SHA integrity monitoring") is ineffective for this attack vector. The attack chain:

1. Collaborator (write access) pushes a malicious commit to any unprotected branch in the repo (e.g., a throwaway feature branch).
2. Creates and pushes a well-formed `v*` tag pointing at the malicious commit (e.g., `v9.9.9`). No tag-protection ruleset prevents this.
3. `cowork-skeleton.yml` fires on `push: tags: ['v*']`.
4. The tag `v9.9.9` passes the allow-list `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` (step 2 of REQ-036 pseudocode).
5. CI generates `cowork-skeleton` from the malicious commit tree (minus `projects/`), force-pushes it.
6. CI publishes the SHA of the **malicious** `cowork-skeleton` tip to the Release notes for `v9.9.9`.
7. The scheduled monitor: `git rev-parse cowork-skeleton` == SHA in Release notes for latest v* tag → **MATCH → NO ALERT**.
8. Event-driven monitor: CI used `GITHUB_TOKEN`, so the `push: branches: [cowork-skeleton]` event is NOT triggered (non-retrigger property). **NO ALERT** from that leg either.

The integrity monitoring detects UNAUTHORIZED modifications to the branch (a direct collaborator push not going through CI). It does NOT detect AUTHORIZED-by-CI modifications that originate from a malicious tag input, because CI itself acts as the "trusted" publisher of both the branch content AND the reference SHA — from the same attacker-influenced input.

**Why this is a Phase-1 defect, not merely an accepted Phase-2 deferral:** ADR-001 explicitly labels the monitoring as "the compensating detective control for a wrong-but-well-formed tag." That claim is factually incorrect. The Phase-1 requirements documents either need to (a) correct this claim (removing the assertion that the compensating control works), or (b) add a Phase-1 control that actually detects this attack (e.g., asserting the trigger tag is reachable from main's HEAD before generating). The deferred item is "provenance checking" — but the *claim* that monitoring compensates for its absence is a Phase-1 requirements defect.

**Recommendation:**

1. **Correct ADR-001's claim**: Remove or qualify the statement that "deterministic-SHA integrity monitoring is the compensating detective control for a wrong-but-well-formed tag." The honest statement is: "No Phase-1 detective control exists for this attack vector; Phase-2 STRIDE will address provenance checking."
2. **Add a Phase-1 provenance guard (optional but recommended)**: Before generating `cowork-skeleton`, assert `git merge-base --is-ancestor ${TAG}^{commit} origin/main` exits 0. This is a one-line check that blocks the attack without requiring STRIDE. This is the "partial Phase-1 coverage" referenced in the Phase-2 deferral table.
3. **Update Risk Implications table**: R-007 should note that the R-007 supply-chain risk rating assumes the actor compromises CI workflow steps (external dependency injection) — but this is a distinct, easier attack path through the tag-push mechanism with no existing Phase-1 detection.

---

### RT-003-I3: SHA-Publication Failure Leaves Monitor Without Reference Value

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | REQ-035 AC; NFR-006 AC; ADR-002 §Continuous Integrity Monitoring |
| **Strategy Step** | Step 2 (Attack Vector: Degradation Paths) |
| **Exploitability** | Low (accidental) / Medium (deliberate via API rate limit exhaustion) |
| **Defense Status** | Partial — REQ-035 mandates the publish step, but neither REQ-035 nor NFR-006 specifies monitor behavior when no SHA is found in Release notes |

**Evidence:**

REQ-035 requires: "CI SHALL publish the expected deterministic tip SHA for the release tag to the GitHub Release notes for that tag (e.g., `gh release edit v{TAG} --notes-append ...`)."

The four-scenario NFR-006 acceptance criteria test: (1) staleness; (2) tamper-detection; (3) clone-weight warning; (4) event-driven verification. **There is no test scenario for "SHA missing from Release notes for the current latest tag."**

ADR-002 §Continuous Integrity Monitoring documents the publish-then-assert model but does not specify the monitor's behavior when the "publish" leg has not yet executed or has failed: "The assert... retrieve the published SHA from the Release notes and assert `git rev-parse cowork-skeleton` equals it."

**Analysis:**

If the force-push succeeds but the `gh release edit` step fails (transient GitHub API error, rate limit, token expiry near job end), the Release notes for the latest `v*` tag have no `cowork-skeleton-sha:` entry. The scheduled monitor later runs and attempts to retrieve the SHA. Its behavior is not specified:

- **If it skips** (no SHA found = no assertion): the branch is live with new content and no reference exists. Any subsequent tamper push produces a mismatch with... nothing. The monitor would need a valid reference to compare against, and it has none. This state persists until the next successful CI run (next release tag) publishes a new SHA.
- **If it errors/exits non-zero** on missing SHA: the monitor creates a GitHub issue (or is supposed to), but this looks identical to a mismatch alert, confusing operators.
- **Race condition during a release**: During the window between force-push and SHA publication (both happen in the same workflow run, seconds apart), the event-driven monitor could fire (from a non-CI push) and encounter a missing SHA for the current release tag.

**Recommendation:**

Add a requirement specifying monitor behavior when no `cowork-skeleton-sha:` entry exists in the Release notes for the latest v* tag:
- **Preferred**: Treat "no SHA found for the tag" as a staleness signal (same cadence/behavior as the lazy-staleness check leg), create a GitHub issue, and exit non-zero. This is conservative and correct.
- Add a Phase-1 acceptance criterion to NFR-006: "(5) Missing SHA — simulate a missing `cowork-skeleton-sha:` entry in Release notes for the latest tag; confirm the monitor creates a GitHub issue and exits non-zero."
- The `gh release edit` step in `cowork-skeleton.yml` should have `if: always()` or equivalent to ensure it runs even if preceding steps fail, AND its own `if: failure()` handler per the REQ-037 pattern.

---

### RT-004-I3: Event-Driven Monitor Has a Suppression Window via Workflow Disable

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | NFR-006; REQ-035; ADR-002 §Continuous Integrity Monitoring |
| **Strategy Step** | Step 2 (Attack Vector: Boundary Violations) |
| **Exploitability** | Low — requires admin-level GitHub access (repository admin, not mere collaborator write) |
| **Defense Status** | Partial — scheduled backstop provides ≤-daily coverage, but the near-real-time detection claim depends on the event-driven leg being active |

**Evidence:**

ADR-002 §Continuous Integrity Monitoring: "Detection latency for the exact tamper event is therefore **≈ Actions scheduling latency (seconds–minutes)**, not days."

NFR-006 describes the event-driven fast path. Neither NFR-006 nor REQ-035 include a requirement to alert if the monitor workflow is disabled or has not run within the stated SLA.

**Analysis:**

A GitHub repository admin can disable any GitHub Actions workflow via `gh workflow disable <workflow-file>` (or via Settings → Actions). This requires admin-level access, not merely collaborator write access.

Attack chain (admin or compromised admin credential):
1. Admin disables `cowork-skeleton-monitor.yml` (or equivalent).
2. Pushes malicious content to `cowork-skeleton` using their credentials (non-GITHUB_TOKEN → normally triggers event-driven monitor, but monitor is disabled).
3. Re-enables the monitor.

The event-driven monitor does NOT fire retroactively for a push that occurred while it was disabled. The scheduled backstop provides detection within ≤ one scheduled interval — so the exposure window is up to one day, not seconds.

**Severity rationale (Major, not Critical):** The attack requires admin access — a higher privilege than collaborator write. The scheduled backstop IS specified and provides bounded detection. However, the deliverable's stated near-real-time detection capability (seconds–minutes) is contingent on the monitor being active, which is not itself a guaranteed property. For an executable-hook supply-chain artifact, this gap is worth documenting.

**Recommendation:**

1. Add a Phase-1 requirement: the monitor workflow SHALL emit a `$GITHUB_STEP_SUMMARY` heartbeat on each scheduled run including the timestamp of its last successful run. If two consecutive scheduled runs are missed (detectable via cron run history or a dedicated "watchdog" pattern), an alert is raised.
2. Acknowledge in ADR-002 §Limitations that the near-real-time detection claim depends on the monitor workflow being enabled and operative, which is controlled by repository admins.
3. The Phase-2 branch-protection escalation (which would require CI bypass actor for force-push) would also prevent admin-suppressed-monitor attacks IF the branch is protected — note this connection explicitly in the upgrade table.

---

### RT-005-I3: Monitor Workflow Has No Self-Health Alerting Requirement

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | NFR-006; REQ-016 (analog for `cowork-skeleton.yml`); ADR-002 §Detection SLA |
| **Strategy Step** | Step 2 (Attack Vector: Degradation Paths) |
| **Exploitability** | Low (requires an external triggering event: Actions outage, permission revocation) |
| **Defense Status** | Missing — no requirement equivalent to REQ-037 exists for the monitor workflow itself |

**Evidence:**

REQ-037 requires: "The `git push --force origin HEAD:cowork-skeleton` step SHALL be followed by a dedicated failure-detection step that executes on `if: failure()`... A rejected push SHALL NEVER produce a silent zero-exit-code outcome."

REQ-016 requires: "The CI workflow SHALL emit a job summary to `$GITHUB_STEP_SUMMARY` on every run (success and failure using `if: always()`)."

NFR-006 specifies what the monitor does on tamper-detection, but no requirement specifies what happens when the monitor **itself fails** (exits non-zero, or fails to execute).

**Analysis:**

The ≤-daily tamper-detection SLA (ADR-002, NFR-006) is a property of the scheduling configuration, not of successful monitor execution. If:
- GitHub Actions experiences an outage lasting > 24 hours (status.github.com events exist),
- The monitor's `GITHUB_TOKEN` loses `issues: write` permission (org policy change),
- The monitor is modified to have a syntax error (silently fails to parse),

...the monitor runs fail silently. There is no requirement analogous to REQ-037 or REQ-016 that would cause the monitor workflow to raise an alert when it itself cannot complete its detection work. The effective SLA degrades from ≤ daily to unbounded with no notification.

**Contrast with `cowork-skeleton.yml`:** That workflow has REQ-016 (`if: always()` job summary) and REQ-037 (`if: failure()` structured diagnostic). The monitor workflow, which is the primary security control for detecting tampering, has no equivalent requirements.

**Recommendation:**

Add requirements for monitor self-health:
- REQ-035 or a new REQ-038: The monitor workflow SHALL emit a `$GITHUB_STEP_SUMMARY` on every run regardless of outcome (`if: always()`).
- REQ-039: If the monitor workflow exits non-zero for any reason OTHER than a detected mismatch (i.e., the integrity check itself failed to execute), it SHALL create a distinct GitHub issue labeled "monitor-health" and exit non-zero.
- Optionally: configure GitHub-level alerting on scheduled workflow failures (Actions Settings → Notifications).

---

### RT-006-I3: Fixed Detection SLA Is Non-Adaptive to Threat Landscape Growth

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | NFR-006; ADR-002 §Detection SLA |
| **Strategy Step** | Step 2 (Attack Vector: Degradation Paths) |
| **Exploitability** | N/A — this is a design gap, not an exploitable vector |
| **Defense Status** | Partial — the ≤-daily SLA is specified and mitigates the risk at current scale |

**Evidence:**

ADR-002 §Detection SLA: "this ADR sets the interval at **≤ 24 hours (daily)** for the tamper assertion, given that the skeleton ships **executable hooks** to user workstations (IT3-007) and a weekly window is too long for that blast radius. The SLA is a Phase-1 requirement (cadence); the precise value and residual-risk acceptance are confirmed in Phase-2 (STRIDE, P-042/AE-005)."

No requirement specifies a mechanism to tighten the SLA as the threat landscape evolves (e.g., repository gains more collaborators, hooks gain more privileged capabilities, a security incident raises the threat level).

**Analysis:**

The ≤-daily SLA was chosen partly because hooks reach user workstations — which correctly reflects the blast radius. However, the SLA is a static Phase-1 commitment with no adaptive mechanism. As the codebase grows in collaborators and privilege, a ≤-daily window provides an increasing aggregate risk. This is a minor design omission (Phase-2 STRIDE is the appropriate vehicle for re-evaluation) but worth noting for the Phase-2 scope.

**Recommendation:**

Add a note to NFR-006 or the Phase-2 deferred items table: "Phase-2 STRIDE SHOULD evaluate whether the ≤-daily SLA remains appropriate given the post-STRIDE threat model, and SHOULD document trigger conditions for SLA tightening (e.g., > N collaborators, hook privilege escalation, prior incident)."

---

### RT-007-I3: Cryptic Operator Error Message for Blank-Input Tag Resolution Failure

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | REQ-036; ADR-001 §Regeneration Commit Determinism |
| **Strategy Step** | Step 2 (Attack Vector: Ambiguity Exploitation — operational) |
| **Exploitability** | N/A — operational robustness concern, not a security vulnerability |
| **Defense Status** | Effective (exits non-zero) — but the error message is non-actionable |

**Evidence:**

ADR-001 pseudocode (Regeneration Commit Determinism):
```bash
TAG="$(git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=-version:refname | head -1)"
# ...
if ! printf '%s' "${TAG}" | grep -Eq '^v[0-9]+\.[0-9]+(\.[0-9]+)?$'; then
  echo "::error::Refusing to build cowork-skeleton: tag '${TAG}' fails the v* allow-list." >&2
  exit 1
fi
```

REQ-036 AC (e): "`workflow_dispatch` run with blank `inputs.target_tag` resolves to the most recent v* semantic-version tag and proceeds normally." This covers the happy path but not the failure path (no matching tags).

**Analysis:**

When `inputs.target_tag` is blank AND `git tag -l` finds no matching `v*` tags (e.g., on a new repository or after all tags are deleted), `head -1` returns empty string. The error is: `"Refusing to build cowork-skeleton: tag '' fails the v* allow-list."` An operator encountering this cannot distinguish between:
- "Blank input and no v* tags exist in the repository"
- "Injection payload was sanitized"
- "tags not fetched — run `git fetch --tags` first"

This affects incident response speed if the workflow fails during a real recovery scenario.

**Recommendation:**

Add a guard before the allow-list check for the blank-resolved-tag case:
```bash
if [ -z "${TAG}" ]; then
  echo "::error::No v* tag found to resolve; ensure tags are fetched and at least one v* tag exists." >&2
  exit 1
fi
```
Document this in REQ-036 AC (e) as an additional negative test: "blank `inputs.target_tag` on a repository with no matching v* tags exits non-zero with a descriptive error message distinguishing empty-resolution from sanitization rejection."

---

### RT-008-I3: Issue Notification Fidelity Gap

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | REQ-035 AC; NFR-006 AC |
| **Strategy Step** | Step 2 (Attack Vector: Ambiguity Exploitation) |
| **Exploitability** | N/A — no active exploitation; issue is that the mandatory alert may be ineffective |
| **Defense Status** | Partial — issue creation is mandated but notification fidelity is unspecified |

**Evidence:**

REQ-035 AC (b): "confirm the event-driven monitor fires within minutes, detects the SHA mismatch, **creates a GitHub issue**, and exits non-zero."

NFR-006 text: "the workflow SHALL: **(a)** create a GitHub issue (the mandatory detect-and-alert response)."

No requirement specifies the issue title, labels, assignees, mention targets, or body structure.

**Analysis:**

The "detect-and-alert" floor is defined as issue creation. An unlabeled, unassigned GitHub issue in a busy repository may not trigger notifications to the right people (depending on Watch settings). An attacker who can observe issue creation (public repo) and close the issue (with triage-level write access) could partially suppress the alert. More practically, an issue without a label like `security` or `integrity-breach` or without a team mention (`@geekatron/security`) may sit unnoticed in a backlog during a real incident. The "alert" function of the issue is entirely dependent on notification configuration outside the workflow.

**Recommendation:**

Add to REQ-035 and NFR-006: the monitor-created issue SHALL include in its title the string "INTEGRITY MISMATCH" (or equivalent), SHALL apply a designated label (e.g., `integrity-alert`), and SHALL mention a designated team or individual in the body. The AC should verify these properties. This converts an unstructured issue into an actionable, findable security event.

---

## Defense Gap Assessment

| ID | Severity | Defense Status | Priority | Rationale |
|----|----------|----------------|----------|-----------|
| RT-001-I3 | Critical | Missing | P0 | "Protected surface" claim is architecturally false; whole integrity model rests on it |
| RT-002-I3 | Critical | Missing | P0 | Named compensating control provides zero detection; Phase-1 requirements defect |
| RT-003-I3 | Major | Partial | P1 | Publish failure → blind spot; no specified behavior; correctness gap in requirements |
| RT-004-I3 | Major | Partial | P1 | Scheduled backstop partially mitigates; admin-level suppression acknowledged gap |
| RT-005-I3 | Major | Missing | P1 | No analog to REQ-037/REQ-016 for the monitor workflow; silent SLA degradation |
| RT-006-I3 | Minor | Partial | P2 | Static SLA; Phase-2 STRIDE is the right vehicle |
| RT-007-I3 | Minor | Effective (exits non-zero) | P2 | No security risk; operational robustness gap |
| RT-008-I3 | Minor | Partial | P2 | Alert created but not reliably noticed; notification config outside workflow |

---

## Scoring Dimension Impact

| Dimension | Weight | Findings | Net Impact |
|-----------|--------|----------|------------|
| Completeness | 0.20 | RT-001-I3, RT-002-I3, RT-003-I3, RT-005-I3, RT-008-I3 | **Negative** — key security controls have unspecified behaviors or false architectural claims |
| Internal Consistency | 0.20 | RT-002-I3 | **Negative** — ADR-001 asserts integrity monitoring compensates for tag-provenance gap; this is demonstrably false |
| Methodological Rigor | 0.20 | RT-001-I3, RT-002-I3 | **Negative** — threat model relies on the Release notes being "more protected" without verifying this claim; the named compensating control was not validated against the attack it is supposed to compensate for |
| Evidence Quality | 0.15 | RT-001-I3, RT-004-I3 | **Negative** — the empirical ruleset inventory (well done) is not extended to verify Release note edit permissions; the admin-suppression gap is not acknowledged |
| Actionability | 0.15 | RT-003-I3, RT-005-I3, RT-007-I3, RT-008-I3 | **Negative** — unspecified monitor behaviors reduce actionability for implementers; error messages are cryptic |
| Traceability | 0.10 | RT-005-I3 | **Negative** — the monitor workflow's self-health requirements are not traced to any STK-xxx stakeholder need despite being a direct safety control |

---

## Phase-2 Deferral Assessment

The following findings are aligned with legitimate Phase-2 deferrals and are **accepted residual exposures**, not Phase-1 defects:

| Finding Aspect | Deferral Reference | Assessment |
|----------------|-------------------|------------|
| Auto-revert automation | ADR-002 §Compensating Controls Phase-2 placeholder; R-007b | Legitimately deferred; detection-not-prevention acknowledged |
| Branch-protection escalation to prevention | ADR-002 §Phase-2 Escalation Path | Legitimately deferred; documented upgrade path is coherent |
| Tag provenance checking | ADR-001 §Scope boundary RT-003; STORY-004 | The DEFERRAL is legitimate; the FALSE CLAIM that monitoring compensates for the absence is a Phase-1 defect (RT-002-I3) |
| R-007b consequence re-rating (C=4 → C=5) | STRIDE threat model | Legitimately deferred |

**The following are Phase-1 requirements defects that must be corrected in Phase-1** (not Phase-2 deferrals):
- **RT-001-I3**: The false "protected surface" claim in REQ-035 and ADR-002
- **RT-002-I3**: The false "compensating detective control" claim in ADR-001
- **RT-003-I3**: Missing specification for monitor behavior when Release notes have no SHA
- **RT-005-I3**: Missing self-health alerting requirement for the monitor workflow

---

## Overall Assessment

**Verdict: Major Remediation Required — Phase-1 Integrity Model Has Critical Architectural Defects**

The iteration-3 defenses are substantially improved over prior iterations. Tag sanitization (REQ-036), push-failure detection (REQ-037), the async publish-then-assert architecture (replacing the in-CI tautological gate), and the non-forgeable SHA comparator (IT3-004) are well-designed. The `GITHUB_TOKEN` choice and loop-safety argument remain sound.

However, two Critical findings represent architectural errors in the Phase-1 requirements that must be resolved before Phase-2:

1. **RT-001-I3** undermines the entire integrity monitoring architecture by treating GitHub Release notes as a "protected surface" when they are writable by the same actors who can tamper with the branch. A sophisticated attacker who has read ADR-002 can defeat the entire monitoring model in two API calls.

2. **RT-002-I3** is a false assurance claim: ADR-001 explicitly names integrity monitoring as the compensating control for the tag-provenance gap, but the monitoring architecture is structurally blind to CI-triggered generation from an attacker-controlled well-formed tag — precisely because CI both generates the malicious content AND publishes it as "expected."

The Major findings (RT-003, RT-004, RT-005) represent completeness gaps in the requirements (unspecified monitor behaviors, no self-health alerting) that would create operational blind spots during implementation.

**Minimum required actions before Phase-2:**
1. Correct RT-001-I3: Replace or harden the Release notes reference surface claim in REQ-035 and ADR-002
2. Correct RT-002-I3: Remove the false compensating-control claim in ADR-001; optionally add the Phase-1 provenance guard (`git merge-base --is-ancestor`)
3. Address RT-003-I3: Specify monitor behavior for missing Release notes SHA in REQ-035/NFR-006 AC
4. Address RT-005-I3: Add monitor self-health alerting requirement

---

## Execution Statistics

| Statistic | Value |
|-----------|-------|
| **Total Findings** | 8 |
| **Critical** | 2 (RT-001-I3, RT-002-I3) |
| **Major** | 3 (RT-003-I3, RT-004-I3, RT-005-I3) |
| **Minor** | 3 (RT-006-I3, RT-007-I3, RT-008-I3) |
| **Protocol Steps Completed** | 5 of 5 |
| **Attack Vectors Evaluated** | 5 categories (Ambiguity, Boundary, Rule Circumvention, Dependency, Degradation) |
| **Distinct Attack Scenarios Analyzed** | 16 (AT-1 through AT-16; 8 elevated to formal findings) |
| **Phase-2 Accepted Deferrals Identified** | 4 (auto-revert, branch protection, R-007b re-rating, tag provenance check itself) |
| **Phase-1 Requirements Defects Identified** | 4 (RT-001, RT-002, RT-003, RT-005) |
| **H-15 Self-Review** | Applied before persistence |

---

*Strategy: S-001 Red Team Analysis*
*Finding Prefix: RT-NNN-I3 (NNN = sequential; I3 = Iteration 3 execution)*
*Template: `.context/templates/adversarial/s-001-red-team.md` v1.0.0*
*Agent: jerry:adv-executor (claude-sonnet-4-6)*
*Project: PROJ-031-cowork-skeleton*
*Execution ID: I3 (Iteration 3, Group C — Challenge, Blind Reviewer)*
*Date: 2026-06-26*
