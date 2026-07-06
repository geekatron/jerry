# Devil's Advocate Report: Phase-3 DESIGN (Skeleton Generation + CI Regeneration + Attestation)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** Phase-3 Design (3 docs):
- `design/phase3-skeleton-generation-design.md` (FAD-PROJ031-3A-001)
- `design/phase3-ci-workflow-design.md` (FAD-PROJ031-3B-001, eng-devsecops)
- `design/phase3-attestation-provenance-design.md` (FAD-PROJ031-3B-001, eng-infra)
**Spec reference:** `decisions/ADR-001`, `decisions/ADR-003`, `requirements/phase1-requirements.md`
**Criticality:** C4
**Date:** 2026-06-30
**Reviewer:** adv-executor (S-002 Devil's Advocate)
**H-16 Compliance:** Orchestrator-asserted (BLINDNESS constraint on `qg3-review/` prevents independent verification of S-003 output; orchestrator invoked S-002 in correct 6-group sequence position, constituting implicit assertion per RT-005 orchestration context)

---

## Summary

Six counter-arguments identified (1 Critical, 2 Major, 3 Minor). The Critical finding is load-bearing: the D7 monitor's tree-digest binding mechanism is semantically incoherent — the two design docs describe contradictory approaches, the attestation design's proposed jq path produces SRC_SHA (always ≠ G6_COMMIT_SHA), and the CI workflow design's fallback mechanism reintroduces the writable release-notes surface that ADR-003 explicitly condemned as the Phase-1 collapsed integrity anchor (SC-04). The Major findings concern the unvalidated git bundle round-trip (the mechanism enabling the primary engineering novelty of the three-job split) and the fact that auto-revert — the ADR-003 D7(d) SHALL — ships absent at go-live, reinstating the "unbounded-latency gap" it was written to close. The three Minor findings are bounded, addressable gaps. Recommendation: **REVISE** to resolve DA-001 and DA-002 before Phase-5 gate validation; DA-003 requires explicit acknowledgment that RT-005 is deferred past go-live.

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| DA-001 | **Critical** | D7 Tree-Digest Match Mechanism Is Semantically Broken | attestation §3.2 + CI-workflow monitor |
| DA-002 | **Major** | Git Bundle Round-Trip Is Unvalidated and Load-Bearing | CI-workflow §L0 + Pending CI-G-001 |
| DA-003 | **Major** | Auto-Revert Deferred Past Go-Live — ADR-003 D7(d) SHALL Not Satisfied | CI-workflow §cowork-monitor.yml |
| DA-004 | Minor | git archive TAR Bit-Stability Across Runner Image Updates Overstated | attestation §1.4 |
| DA-005 | Minor | SBOM IN Has No REQ Coverage, No Phase-5 Gate, Wrong Threat Surface | attestation §7 |
| DA-006 | Minor | Job C Source-Repo GITHUB_TOKEN `contents: write` Is Unjustified Dead Grant | CI-workflow Per-Job Permissions Table |

---

## Detailed Findings

### DA-001: D7 Tree-Digest Match Mechanism Is Semantically Broken

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | `phase3-attestation-provenance-design.md` §3.2 Steps 3–5; `phase3-ci-workflow-design.md` Job M1 `bind-to-live-tip` step |
| **Strategy Step** | Step 3 (Counter-arguments — logical flaws + contradicting evidence) |
| **OWNER** | eng-infra (attestation §3.2 primary), eng-devsecops (monitor implementation secondary) |

**Evidence:**

Attestation design §3.2 Step 3:
```bash
ATTESTED_COMMIT=$(jq -r \
  '.[0].verificationResult.statement.predicate.buildDefinition.resolvedDependencies[0].digest.gitCommit' \
  "${WORK_DIR}/attestation.json")
# Exact jq path is a Phase-6 implementation detail; confirm against live attestation format
```
Step 5 comparison:
```bash
if [ "${ATTESTED_COMMIT}" != "${LIVE_TIP}" ]; then
  echo "[CRITICAL] Tip SHA mismatch ..."
  exit 1
fi
```
Comment: "The G6 deterministic commit → ATTESTED_COMMIT corresponds to LIVE_TIP in a correctly deployed state."

CI workflow design Job M1 `bind-to-live-tip` step (parallel mechanism):
```bash
expected_tip_sha = gh api repos/geekatron/jerry-cowork/releases/latest \
  | jq -r '.body' | grep 'Source-Commit:' | cut -d' ' -f2
live_tip_sha = git ls-remote https://github.com/geekatron/jerry-cowork.git HEAD | cut -f1
IF expected_tip_sha != live_tip_sha: ...
```

ADR-003 D4 (the mandate): "never trusting the `Source-Commit` trailer."
ADR-003 Options D4 (the condemnation): "Release notes share `contents: write` — **collapsed** (5-strategy Critical SC-04)."

**Analysis:**

The devil's position: the D7 monitor's tree-digest binding is incoherent in both design documents and cannot detect the threat it claims to detect.

**Mechanism 1 (attestation design, Steps 3–5):**
GitHub's `actions/attest` produces a SLSA provenance v1 predicate. In that predicate, `buildDefinition.resolvedDependencies[0].digest.gitCommit` records the **source repository's trigger commit** — the commit the `v*` tag points to in `geekatron/jerry`. Call this `SRC_SHA`. The G6 deterministic regeneration commit (call it `G6_SHA`) is a **new commit produced inside the workflow**; it is an output, not an input, and appears nowhere in the SLSA predicate. `git ls-remote geekatron/jerry-cowork HEAD` returns `G6_SHA`. The comparison is therefore:

```
ATTESTED_COMMIT = SRC_SHA  (source repo trigger commit)
LIVE_TIP        = G6_SHA   (skeleton commit; parent=SRC_SHA in Option A)
```

These are structurally and permanently different. The comparison `ATTESTED_COMMIT != LIVE_TIP` will always fire, making the monitor permanently emit false positives — or, since the code has never been run (Phase-6 detail), it will fail on first execution. The comment that "`ATTESTED_COMMIT` corresponds to `LIVE_TIP` in a correctly deployed state" is incorrect.

**Mechanism 2 (CI workflow design, `bind-to-live-tip`):**
This reads `expected_tip_sha` from the release body ("Source-Commit: ${COMMIT_SHA}"). `COMMIT_SHA` here is `G6_SHA` (set after `git rev-parse HEAD` post-G6-commit). The comparison `expected_tip_sha != live_tip_sha` is `G6_SHA != G6_SHA` on a correct deployment — this mechanically works. However:
1. GitHub release bodies are **writable metadata**. `gh release edit` with `contents: write` on the dedicated repo modifies them.
2. If an org owner suppresses D2's ruleset (RTB-1) and grants write collaborators, the release body becomes tamperable. A tampered body can report an `expected_tip_sha` that matches a malicious LIVE_TIP, making the D7 monitor pass on a tampered tree.
3. ADR-003 D4 explicitly condemned release notes as an integrity anchor: "Release notes share `contents: write` — **collapsed** (5-strategy Critical SC-04)" and "Anchor moves to immutable release + attestation."

The design thus simultaneously: (a) describes Mechanism 1, which always fails; (b) falls back to Mechanism 2, which reintroduces the collapsed Phase-1 anchor; and (c) cites ADR-003 D4 as its foundation, which forbids Mechanism 2. The Sigstore attestation (`gh attestation verify`) proves the artifact is CI-built but does NOT bind it to the dedicated repo tip without touching mutable metadata. The design has not solved this binding.

**The design's own note acknowledges the gap**: "Exact jq path is a Phase-6 implementation detail; confirm against live attestation format" — but changing the jq path cannot fix the semantic mismatch: `resolvedDependencies[0].digest.gitCommit` will always yield SRC_SHA regardless of path refinement.

**Recommendation:**

One of three paths must be taken before Phase-5 gate validation:

1. **Add G6_SHA to the SLSA predicate as a custom subject.** Attest the artifact with an additional `subject-name: generated-commit-sha` / `subject-digest: sha256=... gitCommit: G6_SHA` so the predicate contains G6_SHA directly. This makes Mechanism 1 work correctly. Requires eng-infra to specify the attestation invocation with explicit subject metadata; requires eng-devsecops to extract from the correct predicate field.

2. **Recompute G6_SHA from the attested artifact in the monitor.** Since `regenerate(T)` is a pure function of the tag, the monitor can re-derive the expected G6_SHA from `ATTESTED_COMMIT` (SRC_SHA) by running the same deterministic commit algorithm. This is expensive but architecturally sound.

3. **Acknowledge Mechanism 2 is the actual implementation** and harden the release body against tampering by publishing it as a signed artifact in the Sigstore log (separate attestation call) or by deriving expected_tip_sha only from the verified attestation metadata, not the mutable release notes body.

Option 1 is the lowest-cost path. It must be in the design (not deferred to Phase-6) because it changes the attestation invocation in the CI workflow, which determines what the D7 monitor can verify.

---

### DA-002: Git Bundle Round-Trip Is Unvalidated and Load-Bearing

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `phase3-ci-workflow-design.md` §L0 Executive Summary + §Pending Validation CI-G-001 |
| **Strategy Step** | Step 3 (Counter-arguments — unaddressed risks + alternative interpretations) |
| **OWNER** | eng-devsecops (CI-G-001 owner) |

**Evidence:**

CI workflow design L0:
> "The primary engineering novelty in this design is the **per-job permissions isolation**... A git bundle bridges the generated commit between the generate-and-gate job and the push-and-release job (**Phase 6 implementation detail, flagged below**)."

CI-G-001 (Pending Validation):
> "The generated local commit (G6) must travel from Job A to Job C. The `git archive` (G9) is a file archive — it packages the tree but not the git history. A `git bundle` is the standard mechanism (`git bundle create <file> HEAD`), but bundle creation and restoration in the push job need explicit testing for correctness (empty parent, branch HEAD restoration)."
> Phase 6 action: "test bundle round-trip; confirm `git push --force` from restored bundle produces the expected commit SHA"

Generation design G6 algorithm (Option A):
> `IF provenance_mode == OPTION_A: base <- parent=SRC_SHA`

CI workflow design Job C step `download-bundle-and-artifact`:
> `git bundle verify <bundle-file>`
> `git fetch <bundle-file> HEAD:refs/remotes/bundle/HEAD`

**Analysis:**

The three-job split is described as the "primary engineering novelty" — the architectural mechanism that achieves per-job permission isolation without losing the deterministic SHA. The git bundle is the ONLY mechanism enabling this: Job A creates the G6 commit and produces the bundle; Job C restores the bundle and pushes.

Counter-position: this mechanism is unproven and likely to fail silently in its current specification.

**Git bundle prerequisites for Option A:** When `git bundle create <file> HEAD` is executed in Job A, git records the G6 commit's prerequisites — in Option A, the parent is `SRC_SHA`. The bundle header lists `SRC_SHA` as a required prerequisite. When Job C runs `git bundle verify <bundle-file>`, git checks that `SRC_SHA` exists in the local repository. Job C's design says only "download artifact + git bundle from artifact store, restore git state from bundle." The design does NOT specify that Job C performs a `git checkout` of the source repo or a `git fetch --depth=0` to ensure `SRC_SHA` is available. If Job C is a vanilla runner with no source checkout, `git bundle verify` will fail with: "error: Repository lacks these prerequisite commits."

**The Option B path has different behavior:** If `provenance_mode = OPTION_B` (orphan), the commit has no parent, the bundle has no prerequisites, and the restoration works on a bare runner. This means the design may work for Option B but fail for the currently-defaulted Option A.

**Why this is load-bearing:** The determinism contract (`commit_sha(T) = pure function of T`) depends on the bundle round-trip producing the exact same G6 commit SHA in Job C. If Job C cannot restore the bundle and instead re-creates the commit from the TAR archive tree, it would produce a DIFFERENT commit SHA (different parent in Option A, different identity, different timestamp unless all metadata is re-injected identically). The attested artifact's digest would be correct, but the `git push --force` would push a different tip SHA than expected, breaking the D7 monitor's expected_tip_sha match and the freshness check.

**The design acknowledges this but misclassifies its severity:** CI-G-001 is listed as a "Phase 6 implementation detail" in the Pending Validation section. This understates it. If the bundle round-trip is broken, the three-job split (the "primary engineering novelty") is architecturally broken. It is not a Phase-6 implementation detail — it is a design gap that requires resolution before Phase-3 is considered complete, because the correctness of the permission-isolation architecture depends on it.

**Response requirement:** The design must specify, for Job C: (a) whether a source-repo checkout (`fetch-depth: 0`) is required to supply SRC_SHA as the bundle prerequisite; (b) whether `git bundle verify` confirms the prerequisite is available before `git fetch`; (c) whether `git push --force` from the restored bundle HEAD produces an identical commit SHA to what Job A computed. A smoke-test result (run for one tag, compare Job A's `COMMIT_SHA` to `git rev-parse HEAD` in Job C after bundle restore) must be documented in the design before Phase-5 gate validation.

---

### DA-003: Auto-Revert Deferred Past Go-Live — ADR-003 D7(d) SHALL Not Satisfied

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `phase3-ci-workflow-design.md` §cowork-monitor.yml Design → Job M2 Auto-Revert; §G-actions-write-safe Enforcement |
| **Strategy Step** | Step 3 (Counter-arguments — unstated assumptions + contradicting evidence) |
| **OWNER** | eng-devsecops (monitor design) + nse-architecture (D7(d) SHALL compliance) |

**Evidence:**

ADR-003 D7(d) (the mandate):
> "Today detection only opens a GitHub issue; remediation is manual with **unbounded latency** (a weekend tamper could persist 48 h+). The monitor SHALL be coupled to **auto-revert**: on an integrity or freshness failure it triggers a `workflow_dispatch` re-generation of the **last-good-validated** `v*` tag... **close the unbounded-latency gap (RT-005)**."

CI workflow design Job M2 current status:
> "**Status before G-actions-write-safe:** OMITTED from workflow YAML. M1 opens a **CRITICAL issue for human escalation only**. No `actions: write` declared."

G-actions-write-safe gate conditions:
> "(i) ALL `.github/workflows/` files have SHA-pinned Actions [...] AND (ii) G-provenance PASSED (REQ-038 ancestor assertion + REQ-039 `v*` tag protection operational on live pipeline)"

ADR-003 Phase-5 Gate Set: G-provenance is labeled "Phase-5 blocker — go-live MUST NOT proceed" without it passing.

CI workflow design:
> "This is a deliberate two-phase evolution: the workflow ships in human-escalation mode and graduates to auto-revert only when the compound-path dependency is satisfied."

**Analysis:**

ADR-003 D7(d) uses SHALL — a HARD-tier requirement per the constitution's tier vocabulary ("MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL — Cannot override"). The design explicitly ships without auto-revert, in human-escalation-only mode, at go-live. The unbounded-latency gap that D7(d) was written to close (48 h+ exposure window) is reinstated at the moment the system goes live.

**The security rationale for deferral is sound:** The compound-path dependency (ADR-003 RT-002/R-003) — where unpinned monitor Actions + `actions: write` + pre-D5 provenance = an attacker can dispatch a rogue regeneration — is a genuine risk and the deferral is security-motivated. This is not disputed.

**The claim that D7(d) closes RT-005 is premature:** The design says auto-revert will close the gap "after G-actions-write-safe." But G-actions-write-safe requires G-provenance operational, which is a go-live BLOCKER. The earliest G-actions-write-safe can clear is during Phase-5 validation — which means auto-revert is at best available at go-live, not before. The design's "two-phase evolution" language suggests it is NOT expected to be available at go-live, making the design's Pending Validation entry "actions: write added to monitor only after G-actions-write-safe" a post-go-live item.

**This creates a compliance gap:** At go-live, the design delivers D7(a)/(b)/(c) (integrity check + freshness + fail-closed) but NOT D7(d) (auto-revert). ADR-003 D7(d) is a SHALL that includes auto-revert in the D7 definition. The Phase-5 Gate Set does not list auto-revert as a separate go-live blocker, implying the design considers it acceptable to go live without auto-revert. But ADR-003 D7(d) says the monitor "SHALL be coupled to auto-revert" — the design delivers the monitor uncoupled.

**Strongest counter-position the design would make:** The design is transparent (P-022), and the deferral is security-motivated. The detection SLA (≤6 h) plus human escalation provides bounded response even without auto-revert. The RT-002 compound path is a real threat that would be introduced prematurely. The design documents the path to closing the gap.

**Why this remains Major:** The ADR-003 D7(d) SHALL is not satisfied at go-live. This is a protocol violation — the design delivers a partial D7. The Phase-5 gate set does not include auto-revert as a go-live blocker, meaning the system can go live with D7(d) unimplemented. An explicit acknowledgment is needed: either (a) update the Phase-5 gate set to include an "auto-revert operational" gate (implying it IS a go-live requirement), or (b) explicitly downgrade D7(d) in ADR-003 from SHALL to SHOULD for the initial deployment, with a committed timeline for enablement. The current design leaves this ambiguous.

**Response requirement:** Add explicit language to the design (and ADR-003 if appropriate) classifying the auto-revert timeline: does the system go live with or without auto-revert? If without, is D7(d) considered satisfied, deferred, or reduced in severity? The phase gate set must reflect whichever answer is chosen.

---

### DA-004: git archive TAR Bit-Stability Across Runner Image Updates Overstated

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `phase3-attestation-provenance-design.md` §1.4 Determinism Proof; `phase3-skeleton-generation-design.md` §3(b) |
| **Strategy Step** | Step 3 (Counter-arguments — unstated assumptions) |
| **OWNER** | eng-infra (attestation §1.4) + nse-architecture (generation §3) |

**Evidence:**

Attestation design §1.4 Determinism Proof:
> "Since COMMIT_SHA(T) is invariant per T, and `git archive --format=tar` is a **pure function** of the commit SHA, `artifact_digest(T)` is invariant per T. Both `commit_sha(T)` and `artifact_digest(T)` are determined by T and nothing else — no wall-clock time, no runner identity, no GitHub run ID."

Attestation design §1.2:
> "Note: `git archive --format=tar.gz` may internally zero the MTIME field in modern git versions, but its behavior regarding the OS byte is **not standardized across git builds** and is therefore **unreliable** as the sole determinism guarantee."

Pending Validation:
> "`git archive --format=tar` produces bit-identical bytes on ubuntu-latest for the same COMMIT_SHA — Designed; must confirm empirically — Phase-6 two-run idempotency test"

**Analysis:**

The design correctly identifies and resolves the primary non-determinism source (gzip-mtime trap) by using plain TAR. The "pure function" claim in §1.4 is the counter-argument target.

`git archive --format=tar`'s TAR output is implementation-defined. The claim that it is a "pure function of the commit SHA" (bit-identical regardless of environment) depends on:
1. The git binary version producing identical TAR header bytes (TAR format: POSIX ustar vs GNU TAR vs PAX — different headers, different checksum algorithms)
2. GitHub Actions' `ubuntu-latest` runner image retaining the same git binary version across weekly image updates

Neither is guaranteed. The design acknowledges in §1.2 that even `git archive --format=tar.gz` has unstated OS-byte behavior across git builds. The same concern applies to the plain TAR: if GitHub updates `ubuntu-latest` from git 2.43 to git 2.45 between release vN and release vN+1, and git 2.45 changes a TAR header field (e.g., adds or removes a PAX extension header), the artifact digest for re-running vN changes. This breaks the idempotency proof: `artifact_digest(T)` is no longer a pure function of T — it also depends on the git binary version.

The impact: if a re-run of the same tag (e.g., workflow_dispatch for re-generation or the D7 monitor's re-attestation scenario) produces a different artifact digest, the Sigstore attestation anchored to the first run's digest will not verify against the re-run artifact. This is bounded by the Phase-6 idempotency test — but the test must be repeated across runner image updates, not just once at Phase-6.

**The design's own note ("not standardized across git builds") applies to its own plain-TAR solution.** This is not acknowledged explicitly. The "pure function" mathematical framing in §1.4 overstates certainty.

**Recommendation:** Narrow the §1.4 determinism proof to: "`git archive --format=tar` is bit-stable across re-runs on the SAME runner image version with the SAME git binary." Add a Pending Validation item: "artifact_digest(T) is stable across runner image versions (re-tested when ubuntu-latest updates git major/minor version)." Consider pinning the runner to a specific ubuntu release (`ubuntu-24.04` instead of `ubuntu-latest`) to decouple from weekly image churn. This is a 1-line change in the workflow and eliminates the runner-drift risk entirely for the attestation artifacts.

---

### DA-005: SBOM IN Has No REQ Coverage, No Phase-5 Gate, Wrong Threat Surface

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `phase3-attestation-provenance-design.md` §7; generation design §Decomposition & Hand-Off → eng-infra §5 |
| **Strategy Step** | Step 3 (Counter-arguments — alternative interpretations + scope creep risk) |
| **OWNER** | eng-infra (SBOM recommendation §7) + orchestrator (scope/REQ decision P-020) |

**Evidence:**

Generation design (eng-infra scope note):
> "SBOM (optional, SLSA trajectory; ADR-003 L2 §4): assess whether to emit an SBOM for the artifact as a defense-in-depth provenance addition; **new/optional, not required by any current REQ** — propose, do not assume (P-020)."

Attestation design §7 recommendation: "**IN** — Generate and Attest a CycloneDX SBOM"

ADR-003 D8 (the primary threat narrative):
> "The skeleton payload **is markdown instructions loaded into Claude** — `SKILL.md`, agent `.md`, and command files... None of them inspects **what the markdown instructions actually say**."

Attestation design Pending Validation (SBOM-related):
> - "SBOM CycloneDX schema version (1.5 specified; confirm cyclonedx-py version supports it)"
> - "Confirm whether `actions/attest` v4+ accepts both `subject-path` and `sbom-path` in a single call or requires two separate calls"

No Phase-5 gate named for SBOM validation.

**Analysis:**

The design recommends SBOM IN with a "near-zero cost" rationale. Counter-position: the cost is not near-zero, the coverage is aimed at the wrong threat surface, and the recommendation over-runs the scope set by the orchestrator's P-020 constraint.

**No REQ, no gate:** The generation design explicitly notes "new/optional, not required by any current REQ — propose, do not assume (P-020)." The attestation design makes the leap from "propose" to "IN" with a recommendation that pulls Phase-6 implementation effort toward a non-required deliverable while the Phase-5 gate set has no SBOM verification entry. An unvalidated SBOM deliverable adds maintenance burden (schema versions, attestation call count, cyclonedx-py version pinning) without acceptance criteria.

**Wrong threat surface:** The dominant threat this design addresses is the **markdown/LLM instruction surface** (D8 content-safety gate, ADR-003 D8 — "the skeleton payload IS markdown instructions loaded into Claude"). The SBOM covers the **Python dependency surface** (`pyproject.toml`/`uv.lock`). These are orthogonal threat surfaces. A CycloneDX SBOM of Python dependencies does not add any defense against prompt injection in skill files, agent files, or command files. An auditor seeing an attested SBOM may incorrectly infer the primary threat surface is covered.

**Two open validation items block SBOM:** The Pending Validation section lists "confirm whether `actions/attest` v4+ accepts both `subject-path` and `sbom-path` in a single call or requires two separate calls." If two calls are required, this adds a second attestation invocation in the attestation job — with additional permission considerations (`artifact-metadata: write` is listed as potentially required, currently under "confirm"). This is not near-zero complexity.

**Recommendation:** Demote SBOM to a post-go-live enhancement. Add a REQ (nse-requirements) if stakeholders accept it, which gives it an acceptance criterion and gate. The pre-go-live design document should record "SBOM: OUT for Phase-3; evaluate in Phase 7 after SLSA L3 validation." This respects P-020 ("propose, do not assume") and keeps Phase-6 scope focused on required deliverables.

---

### DA-006: Job C Source-Repo GITHUB_TOKEN `contents: write` Is Unjustified Dead Grant

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `phase3-ci-workflow-design.md` §Per-Job Permissions Table; Job C steps |
| **Strategy Step** | Step 3 (Counter-arguments — unstated assumptions + ADR-003 compliance drift) |
| **OWNER** | eng-devsecops (per-job permissions table) |

**Evidence:**

Per-Job Permissions Table:
> `push-and-release: contents: write (sole) — Matches REQ-020(a); **actual cross-repo push uses App token, not GITHUB_TOKEN**`

Job C steps that involve writes:
- `cross-repo-force-push`: uses `${DEDICATED_TOKEN}` (App token)
- `publish-immutable-release`: `gh release create ... --repo geekatron/jerry-cowork` — uses App token
- `push-failure-detection`: writes to `$GITHUB_STEP_SUMMARY` (no `contents` scope required)
- `job-summary`: writes to `$GITHUB_STEP_SUMMARY` (no `contents` scope required)
- `mint-app-token`: reads environment secrets (no `contents` scope on GITHUB_TOKEN required)
- `download-bundle-and-artifact`: reads from artifact store (Actions scope, not `contents`)

ADR-003 D6 item 5: "Minimal `permissions:` per job"
ADR-003 c-206: "The skeleton-push job MUST trigger only on verified release events... and MUST pin every Action to a commit SHA."

**Analysis:**

The parenthetical "(actual cross-repo push uses App token, not GITHUB_TOKEN)" in the permissions table is its own counter-argument: it acknowledges the `contents: write` grant on the source-repo GITHUB_TOKEN is not used for the primary purpose of Job C. None of Job C's enumerated steps requires source-repo `contents: write` via GITHUB_TOKEN:

- App token mint: requires no GITHUB_TOKEN permission (accesses env secrets via the `skeleton-push` environment, which is access-controlled at the environment level, not via GITHUB_TOKEN)
- Artifact download: uses the GitHub Actions artifact service, not `contents` scope
- `git push --force` to dedicated repo: authenticated via the App token (`${DEDICATED_TOKEN}`), not GITHUB_TOKEN
- `gh release create --repo geekatron/jerry-cowork`: authenticated via App token (note the `--repo geekatron/jerry-cowork` flag; this writes to the DEDICATED repo, using the App token scoped to that repo, not the source-repo GITHUB_TOKEN)
- Step summaries: no `contents` scope needed

The source-repo GITHUB_TOKEN's `contents: write` in Job C therefore appears to be a dead grant — it opens a source-repo write surface that is unused, conflicting with ADR-003 D6 item 5's minimal permissions requirement. A compromised Job C step (e.g., a supply-chain attack on an unpinned Action) could use the GITHUB_TOKEN `contents: write` to modify source-repo contents unexpectedly.

The `last-good-validated` tag advancement (which does require source-repo `contents: write`) belongs to the Monitor (Job M1), not to Job C.

**Note:** This may be an artifact of the design deferring REQ-020 refinement to Phase-6 (where the actual YAML is written). If so, it should be flagged as a Phase-6 implementation constraint rather than left as an unexplained permission.

**Recommendation:** The design should justify source-repo `contents: write` in Job C or reduce it to `contents: read`. If no step in Job C requires it (and none appears to), document the reduction explicitly: "Job C: GITHUB_TOKEN `contents: read` (all writes use the App token; source-repo write surface eliminated)." This is a one-line change in the YAML and eliminates an unnecessary attack surface.

---

## Response Requirements

### P0 — Must resolve before Phase-5 gate validation

| Finding | Required creator response |
|---------|--------------------------|
| **DA-001** | Specify a working, tamper-evident mechanism to bind the Sigstore attestation to the dedicated-repo live tip WITHOUT relying on mutable release notes. The jq path in attestation §3.2 must either be corrected to yield G6_SHA (requires adding G6_SHA to the SLSA predicate as a custom subject) or the release-notes mechanism must be replaced with an independent, non-writable binding. The two design docs must describe the SAME mechanism. |
| **DA-002** | Specify Job C's git environment (checkout needed? fetch-depth?), confirm `git bundle verify` works with Option A's SRC_SHA prerequisite in Job C's context, and provide a documented smoke-test result showing G6 SHA is identical before bundle creation (Job A) and after bundle restoration (Job C). |

### P1 — Should resolve before go-live; justification required if not

| Finding | Required creator response |
|---------|--------------------------|
| **DA-003** | Explicitly classify whether go-live proceeds with or without auto-revert. If without: (a) acknowledge D7(d) SHA is not delivered at go-live, (b) add a post-go-live gate for auto-revert enablement to the Phase-5 gate set or a separate Phase-7 gate, (c) acknowledge RT-005 gap persists at go-live. If with: G-actions-write-safe must clear during Phase-5, requiring SHA-pinning of ALL workflows to complete before go-live. |

### P2 — May resolve; acknowledgment sufficient

| Finding | Response |
|---------|----------|
| **DA-004** | Acknowledge runner-image drift risk; add a Pending Validation item for cross-image-version idempotency test; consider pinning `ubuntu-24.04`. |
| **DA-005** | Formally defer SBOM to post-go-live. Add REQ if stakeholders accept it; remove "IN" recommendation from Phase-3 design docs. |
| **DA-006** | Explicitly justify or eliminate source-repo `contents: write` from Job C in Phase-6 YAML planning notes. |

---

## Scoring Impact

| Dimension | Finding(s) | Net Impact | Rationale |
|-----------|------------|-----------|-----------|
| Internal Consistency | DA-001 | **Negative** | Two docs contradict on tree-digest mechanism; attestation's jq path always fails; CI workflow design reintroduces condemned anchor |
| Methodological Rigor | DA-001, DA-002 | **Negative** | Load-bearing mechanism (bundle round-trip) is unvalidated; tree-digest binding design is demonstrably incorrect |
| Evidence Quality | DA-004 | Neutral/Minor Negative | "Pure function" overstates mathematical certainty; runner-image drift unacknowledged |
| Completeness | DA-002, DA-003, DA-005 | **Negative** | Bundle round-trip spec incomplete; D7(d) SHALL unsatisfied; SBOM IN lacks REQ/gate |
| Actionability | DA-001, DA-002, DA-003 | **Negative** | Phase-5 gates cannot pass if DA-001 and DA-002 remain unresolved; DA-003 creates ambiguity in go-live criteria |
| Traceability | DA-006 | Minor Negative | Unexplained dead permission grant deviates from ADR-003 D6 minimal permissions |

**Overall assessment:** REVISE — two P0 findings (DA-001, DA-002) require design revision before Phase-5 gate validation can begin. DA-001 in particular is a Critical defect in the D7 monitor's core detection claim that the design has not answered.

---

## Execution Statistics
- **Total Findings:** 6
- **Critical:** 1 (DA-001)
- **Major:** 2 (DA-002, DA-003)
- **Minor:** 3 (DA-004, DA-005, DA-006)
- **Protocol Steps Completed:** 5 of 5 (Step 1: role adopted; Step 2: assumptions challenged; Step 3: counter-arguments constructed across 6 challenge points; Step 4: response requirements specified; Step 5: scoring impact synthesized)
- **Challenge Points Addressed (per task brief):**
  1. 3-job split / git bundle round-trip → DA-002 Major (NOT answered by design)
  2. git archive determinism across runner images → DA-004 Minor (PARTIALLY answered; empirical test deferred)
  3. D7 monitor SLSA-predicate SHA vs git ls-remote HEAD → DA-001 Critical (NOT answered; semantically broken)
  4. Auto-revert deferred / unbounded-latency gap → DA-003 Major (NOT satisfied at go-live)
  5. SBOM IN complexity vs scope → DA-005 Minor (design overruns its own P-020 constraint)
  6. ADR-003 gate ordering + per-job permissions → DA-006 Minor (minor drift: Job C dead `contents: write`; gate sequence otherwise faithful)

---

*Strategy: S-002 Devil's Advocate*
*Template: `.context/templates/adversarial/s-002-devils-advocate.md` v1.0.0*
*H-15 Self-Review: applied — all findings have direct evidence quotes; severity criteria stated; summary table matches detailed findings; no finding minimized.*
*P-003: No sub-agents spawned.*
*P-002: Report persisted to `design/qg3-review/s-002-devils-advocate-findings.md`.*
