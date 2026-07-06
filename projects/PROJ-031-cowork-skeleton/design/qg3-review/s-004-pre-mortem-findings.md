# Pre-Mortem Report: Phase 3 Design (Skeleton Generation + CI Regeneration + Attestation)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** phase3-skeleton-generation-design.md, phase3-ci-workflow-design.md, phase3-attestation-provenance-design.md
**Criticality:** C4
**Date:** 2026-06-30
**Reviewer:** adv-executor (S-004, QG-3 tournament, blind per blindness constraint)
**H-16 Compliance:** S-003 Steelman is Group-2 in the C4 group order and runs before Group-3 (challenge); S-004 is Group-3. H-16 satisfied structurally by tournament sequencing. Prior S-003 output not read (blindness constraint honored).
**Failure Scenario:** It is December 2026, six months post go-live. The PROJ-031 pipeline has failed in production. The dedicated repo `geekatron/jerry-cowork` contains a skeleton that (a) was attested for a different commit than the one actually pushed, (b) has been silently stale for 19 days because the D7 monitor falsely passed on a freshness failure, and (c) when auto-revert was manually triggered, it entered an infinite re-generation loop. No CRITICAL alert fired during the stale window. Three failure modes compounded simultaneously. I am investigating backward from this declared failure.

---

## Findings Summary

| ID | Severity | Finding | Section / Owner |
|----|----------|---------|-----------------|
| PM-001-Q3 | Critical | Git bundle round-trip (Job A → Job C) not validated — COMMIT_SHA identity not proven to survive cross-job transfer | CI workflow §CI-G-001 / CI-workflow→eng-devsecops |
| PM-002-Q3 | Critical | D7 monitor jq path for ATTESTED_COMMIT extraction is a Phase-6 placeholder — if wrong, tree-digest match always fails or always passes | CI workflow §verify-attestation / attestation→eng-infra |
| PM-003-Q3 | Critical | D8 content-safety scanner tool entirely undefined — the only technical gate on payload content has no concrete implementation path in the design | CI workflow §CI-G-003 / CI-workflow→eng-devsecops (pattern catalog owner: eng-architect) |
| PM-004-Q3 | Critical | Auto-revert creates an infinite loop when freshness failure is caused by a pipeline failure (not a tamper), because revert-to-last-good never fixes the missing new release | CI workflow §Job M2 / CI-workflow→eng-devsecops |
| PM-005-Q3 | Major | D7 freshness check compares elapsed time against the TAG's underlying commit's committer-date, not the tag creation time — any release where the commit predates the tag push by >2 h triggers a false-positive CRITICAL alert | CI workflow §freshness-check / CI-workflow→eng-devsecops |
| PM-006-Q3 | Major | Race condition between force-push (Job C step 1) and release publish (Job C step 2): D7 monitor running in this window sees new tip SHA but no new release asset — fails with CRITICAL tamper alert on a valid release | CI workflow §Job C / CI-workflow→eng-devsecops |
| PM-007-Q3 | Major | `generate-and-gate` job declares `contents: read` but G8 early-warning bands call `open_informational_issue()` which requires `issues: write` — informational pack-growth warnings are silently dropped or block the release | CI workflow §Per-Job Permissions / CI-workflow→eng-devsecops |
| PM-008-Q3 | Major | SBOM generation (`uv run cyclonedx-py environment`) is placed in the attestation job (Job B) which downloads only the TAR artifact — the source `pyproject.toml`/`uv.lock` are not present, producing a wrong-environment SBOM | attestation §7.2 / attestation→eng-infra |
| PM-009-Q3 | Major | `fetch-depth: 0` requirement appears only in the traceability matrix and is not in any workflow pseudocode step — Phase-6 implementers using the default (shallow) checkout will cause D5 to reject all releases whose source commit is outside the shallow cut-off | skeleton-gen §D-02, CI workflow traceability / CI-workflow→eng-devsecops |
| PM-010-Q3 | Major | G8 clone-time measurement runs as an actual clone on the GitHub Actions runner (fast network), not on a 10 Mbps reference connection — the hard-fail threshold (60 s) will never trigger even when CoWork users would time out | skeleton-gen §4 / skeleton-gen→nse-architecture |
| PM-011-Q3 | Minor | `last-good-validated` is a lightweight non-`v*` tag — not covered by the `v*` tag-protection ruleset (D5/REQ-039) — any source-repo write-collaborator can force-move it to manipulate auto-revert | CI workflow §auto-revert / spec→ps-architect/nse-requirements |
| PM-012-Q3 | Minor | Version sentinel file path is unspecified (design says ".claude/ or the projects/ stub") — inconsistency between releases silently breaks Fallback A (version-check skill reads wrong path) | skeleton-gen §6 / skeleton-gen→nse-architecture |
| PM-013-Q3 | Minor | `actions/attest` attestation job may require `artifact-metadata: write` permission in addition to `id-token: write` + `attestations: write` — flagged as unconfirmed in the design; if required and absent, every attestation step fails in production | attestation §2.2 / attestation→eng-infra |

---

## Detailed Findings

### PM-001-Q3: Git Bundle Round-Trip — COMMIT_SHA Identity Not Proven [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | Technical |
| **Likelihood** | High — CI-G-001 is an explicit design gap; no test exists yet |
| **Section** | CI workflow §§G9, Job C §download-bundle-and-artifact; Phase 6 gap CI-G-001 |
| **Strategy Step** | Step 3 — Technical Failure: implementation flaw in cross-job state transfer |

**Evidence:**
The CI workflow design documents the gap explicitly: "CI-G-001 | Git state transfer between jobs. The generated local commit (G6) must travel from Job A to Job C. The `git archive` (G9) is a file archive — it packages the tree but not the git history. A `git bundle` is the standard mechanism … but bundle creation and restoration in the push job need explicit testing for correctness … Phase 6: test bundle round-trip; confirm `git push --force` from restored bundle produces the expected commit SHA."

Job C: "git bundle verify <bundle-file>" then "git fetch <bundle-file> HEAD:refs/remotes/bundle/HEAD" then "git push --force … HEAD:<default-branch>". The COMMIT_SHA used by the attestation (Job B, attesting the TAR artifact produced from COMMIT_SHA) and the commit actually pushed (Job C, via the bundle restore) must be identical. No design element proves this is so.

**Analysis:**
The git bundle captures a commit SHA. When Job C restores via `git fetch <bundle-file> HEAD:refs/remotes/bundle/HEAD`, HEAD in the restored context points to `refs/remotes/bundle/HEAD`, not to a local branch. The subsequent `git push --force HEAD:<default-branch>` pushes whatever HEAD resolves to after the fetch. If the bundle restore puts HEAD in detached or incorrect state, the pushed commit SHA may differ from the COMMIT_SHA that Job A computed, attested, and recorded in the release notes.

If the pushed SHA differs from the attested artifact's embedded COMMIT_SHA, the D7 monitor's tree-digest match (`expected_tip_sha != live_tip_sha`) will ALWAYS fail for every release, making the monitor permanently trigger CRITICAL alerts and auto-revert on every good release — a total pipeline collapse.

**Recommendation:**
Add an explicit SHA-validation step in Job C immediately after the bundle restore:
```bash
RESTORED_SHA=$(git rev-parse HEAD)
if [ "${RESTORED_SHA}" != "${COMMIT_SHA_FROM_JOB_OUTPUT}" ]; then
  echo "::error::Bundle restore SHA mismatch: expected ${COMMIT_SHA_FROM_JOB_OUTPUT}, got ${RESTORED_SHA}"
  exit 1
fi
```
Then assert post-push: immediately verify the dedicated-repo tip SHA via `git ls-remote` matches COMMIT_SHA. Mandate this as a Phase-6 blocking test before any live deployment. OWNER: CI-workflow→eng-devsecops.

**Acceptance Criteria:** Two independent workflow runs for the same release tag produce identical COMMIT_SHA values, and `git ls-remote geekatron/jerry-cowork HEAD` returns that COMMIT_SHA after push.

---

### PM-002-Q3: D7 jq Path for ATTESTED_COMMIT Is a Phase-6 Placeholder [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | Technical |
| **Likelihood** | High — the jq path is explicitly flagged as "a Phase-6 implementation detail; confirm against live attestation format" |
| **Section** | CI workflow §bind-to-live-tip; attestation §3.2 |
| **Strategy Step** | Step 3 — Technical Failure: design weakness in D7 monitor integrity check |

**Evidence:**
CI workflow design (§bind-to-live-tip): "Extract expected tip SHA from release metadata (Source-Commit: trailer in release notes): `expected_tip_sha = gh api ... | jq -r '.body' | grep 'Source-Commit:' | cut -d' ' -f2`"

Attestation design (§3.2): "Extract the source commit SHA from the SLSA provenance predicate: `ATTESTED_COMMIT=$(jq -r '.[0].verificationResult.statement.predicate.buildDefinition.resolvedDependencies[0].digest.gitCommit' "${WORK_DIR}/attestation.json")` — **Exact jq path is a Phase-6 implementation detail; confirm against live attestation format.**"

There is also a divergence between the two documents: the CI workflow reads `expected_tip_sha` from release-note text (Source-Commit trailer), while the attestation design reads `ATTESTED_COMMIT` from the SLSA predicate JSON. These are different values serving different purposes — neither document reconciles what is actually compared.

**Analysis:**
Two separate failure modes:

1. **Release-note extraction failure.** `gh api ... | jq -r '.body' | grep 'Source-Commit:' | cut -d' ' -f2` breaks if the release notes body format differs from the template (e.g., trailing whitespace, Unicode in notes, GitHub's markdown escaping of backticks). Empty result → `expected_tip_sha` is empty → comparison `"" != live_tip_sha` → ALWAYS fires CRITICAL alert.

2. **SLSA predicate jq path failure.** The jq path `.[0].verificationResult.statement.predicate.buildDefinition.resolvedDependencies[0].digest.gitCommit` is specific to the SLSA Build Provenance v1 predicate schema from `actions/attest`. Any version change in the action, any schema migration, or any difference in how `gh attestation verify --format json` serializes the output causes this path to return null → `ATTESTED_COMMIT` is empty → comparison with `live_tip_sha` always fails → permanent CRITICAL alert on every monitor run.

Neither failure mode is loud: the script may produce an empty string rather than an error, satisfying `IF "" != live_tip_sha` as always-true. The integrity monitor becomes either a permanent false-alarm generator or (if empty-string comparison is handled with `|| true`) silently non-functional.

**Recommendation:**
(a) Validate the release-note extraction against a real `gh release create` output before Phase-6 implementation; use structured output (a dedicated JSON field, not text-parsing of `.body`). (b) Validate the SLSA jq path against a live `gh attestation verify --format json` output from the actual pinned `actions/attest` version. (c) Add explicit non-empty assertions for both `expected_tip_sha` and `ATTESTED_COMMIT` before the comparison: `[ -z "${ATTESTED_COMMIT}" ] && { echo "::error::ATTESTED_COMMIT extraction failed"; exit 1; }`. (d) Reconcile the two documents: decide whether D7 compares against the release-note trailer OR against the SLSA predicate commit — the monitor should do both as defense-in-depth, not choose one. OWNER: attestation→eng-infra (jq path), CI-workflow→eng-devsecops (release-note extraction).

**Acceptance Criteria:** Synthetic test: produce an attestation with a known COMMIT_SHA; run D7 monitor verification; confirm ATTESTED_COMMIT extracted equals the known COMMIT_SHA. Test with `--format json` output from the exact pinned `actions/attest` version.

---

### PM-003-Q3: D8 Content-Safety Scanner Entirely Undefined [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | Process |
| **Likelihood** | High — CI-G-003 is an explicit design gap with no concrete implementation path |
| **Section** | CI workflow §d8-content-safety-scan; Phase 6 gap CI-G-003; ADR-003 D8 |
| **Strategy Step** | Step 3 — Process Failure: missing review gate; incomplete gate sequencing |

**Evidence:**
CI workflow design (§d8-content-safety-scan): "`<content-safety-scanner> --fail-on-find skills/ commands/ .claude/ .context/ OR exit_1(...)`"

Phase 6 gap CI-G-003: "D8 scanner tool and pattern catalog. The content-safety scan pseudocode references `<content-safety-scanner>`. The concrete tool, pattern catalog (C1–C6), false-positive rate, and invocation flags are owned by eng-architect. This design fixes placement, scope, and fail-closed semantics only. Phase 6: consume eng-architect D8 output; integrate tool invocation into production YAML."

ADR-003 D8: "eng-architect (STRIDE): owns the pattern catalog and detector tool (the concrete indicator set, the scanner choice, severity tiers, false-positive handling)."

**Analysis:**
D8 is the ONLY technical control in the entire design that inspects the markdown content for prompt-injection payloads. Every other control (D2 branch lock, D4 attestation, D5 tag provenance, D7 monitor) proves the skeleton was faithfully built — none of them can detect a payload embedded in a SKILL.md or agent file.

With D8 defined only as `<content-safety-scanner>` with no concrete tool, no pattern catalog, and no specification of the scanner's output format or error codes, Phase-6 implementation faces three failure modes:
- **Scanner never implemented:** D8 gate is a no-op placeholder or is omitted entirely. Explicit-pattern prompt injection ships undetected.
- **Wrong scanner used:** A binary/code scanner (e.g., Trivy, Semgrep for code) is applied to markdown files. It produces zero true positives for LLM prompt injection and either blocks every release (constant false positives) or passes everything (zero detection).
- **Pattern catalog not defined before implementation:** Phase-6 implements an empty or generic pattern catalog; D8 passes all content trivially, providing false assurance of content safety.

The design explicitly acknowledges this dependency (eng-architect owns the catalog) but provides no interface contract, no acceptance criteria for the catalog, and no gate preventing Phase-6 from proceeding without it.

**Recommendation:**
(a) Add a Phase-5 blocking gate: D8 pattern catalog and scanner tool MUST be delivered by eng-architect with a minimum of C1-C6 documented patterns, an invocation specification, and a false-positive acceptance rate before Phase-6 implements the workflow. (b) Define an explicit handoff contract: the scanner must accept a directory path and exit non-zero on any match or internal error. (c) Add a synthetic acceptance test: insert a known C1 role-reversal indicator into a test SKILL.md; confirm the scanner exits non-zero. This test blocks Phase-6 implementation until D8 is concrete. OWNER: CI-workflow→eng-devsecops (integration), eng-architect (owns pattern catalog — must deliver before Phase-6).

**Acceptance Criteria:** G-content gate requires: (i) a named, pinned scanner tool; (ii) a documented pattern catalog C1-C6; (iii) a synthetic positive test passing; (iv) a false-positive rate verified against the real plugin surface (`skills/ commands/ .claude/ .context/` on `main`).

---

### PM-004-Q3: Auto-Revert Creates Infinite Loop on Pipeline Failure [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Category** | Technical |
| **Likelihood** | Medium — any transient pipeline failure (Actions quota, network error, workflow syntax error) triggers this loop |
| **Section** | CI workflow §Job M2, §freshness-check; ADR-003 D7(d) |
| **Strategy Step** | Step 3 — Technical Failure: design weakness in auto-revert topology |

**Evidence:**
D7 freshness check (CI workflow §freshness-check): "IF latest_src_tag != deployed_release_version: elapsed = now() - parse_time(latest_src_tag_time); IF elapsed > 2h: open_github_issue('[CRITICAL] D7 monitor: freshness failure…'); exit 1"

Auto-revert (CI workflow §auto-revert): "gh workflow run cowork-skeleton.yml --field target_tag=${last_good_tag}"

`last_good_tag = git describe --tags --exact-match $(git rev-parse last-good-validated)`

**Analysis:**
Scenario: Release `vN` is tagged at 9am. The `cowork-skeleton.yml` run for `vN` fails at 10am (e.g., transient GitHub API error during attestation). `last-good-validated` still points to `vN-1`. The D7 monitor runs at noon:
- `latest_src_tag = vN`
- `deployed_release_version = vN-1` (the push never completed for vN)
- `elapsed = 3h > 2h` → freshness failure → exits 1

The M2 auto-revert fires: dispatches `cowork-skeleton.yml` with `target_tag=vN-1`. This succeeds and pushes `vN-1`'s skeleton. Now:
- `deployed_release_version = vN-1` (still)
- `latest_src_tag = vN` (still, because it's a real release tag)
- On next monitor run: freshness failure fires AGAIN → auto-revert dispatches `vN-1` AGAIN

This is an infinite loop. `vN` is never deployed because:
1. The original failure might be transient (the underlying cause may have resolved), but auto-revert doesn't retry `vN` — it only reverts to `vN-1`
2. The freshness check will never pass because the deployed version is `vN-1` but the latest source tag is `vN`
3. Each auto-revert fires a new `cowork-skeleton.yml` run, consuming Actions quota

The design also has no mechanism to detect the loop: each auto-revert cycle opens a new CRITICAL issue but doesn't recognize the pattern as a revert loop. An operator would need to manually notice the repeated CRITICAL issues and intervene.

**Recommendation:**
(a) Add a revert-attempt counter: before dispatching auto-revert, record the current `latest_src_tag` and the revert target in the issue body. If the next monitor run finds `latest_src_tag` STILL != `deployed_release_version` AND the deployed version was just reverted to `last-good-validated` in the previous cycle, escalate to human-only (do not auto-dispatch again). (b) Add logic: if `latest_src_tag != last_good_tag`, attempt to re-generate `latest_src_tag` first (not revert to `last_good_tag`), and only fall back to revert if the `latest_src_tag` re-generation also fails. (c) Add a revert circuit breaker: after 2 consecutive revert dispatches for the same `latest_src_tag`, stop dispatching and post a human-escalation issue. OWNER: CI-workflow→eng-devsecops.

**Acceptance Criteria:** Synthetic test: (i) release vN fails during attestation; (ii) D7 monitor detects freshness failure; (iii) auto-revert dispatches vN-1; (iv) on second monitor cycle, the auto-revert circuit breaker fires (no second dispatch); (v) a human-escalation issue is opened.

---

### PM-005-Q3: D7 Freshness Check Uses Commit Date Not Tag Creation Time [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Technical |
| **Likelihood** | High — the version-bump workflow creates a commit then tags it; the commit date always precedes the tag push by some gap |
| **Section** | CI workflow §freshness-check |
| **Strategy Step** | Step 3 — Technical Failure: implementation flaw in freshness check timing |

**Evidence:**
CI workflow §freshness-check: "latest_src_tag_time = gh api repos/geekatron/jerry/git/refs/tags/${latest_src_tag} | jq -r '.object.url' | xargs gh api | jq -r '.committer.date'"

This fetches the **tag's underlying commit's committer date**. Not the tag's creation timestamp.

**Analysis:**
The Jerry release pipeline (`version-bump.yml` → `release.yml`) creates a commit then tags it. The version-bump commit is created at time T0. The `v*` tag is pushed at time T1, where T1 > T0. The gap T1-T0 depends on the `version-bump.yml` run time (minutes) and any manual delay.

When the D7 monitor runs at time T2 and `vN` has been tagged but not yet deployed (cowork-skeleton.yml is still running), it checks:
- `elapsed = T2 - T0` (commit date, NOT tag-push time T1)
- If T2 - T0 > 2h, the monitor fires a CRITICAL freshness alert

For a release where T0 = 9am, T1 = 9:05am (tag pushed), and T2 = 11:30am (monitor runs), the elapsed against the commit date is 2h30m. The CRITICAL alert fires even though the tag has only been deployed for 2h25m (within the 2h window from tag creation). This is a false positive.

Given that GitHub Actions CI pipelines for `cowork-skeleton.yml` are expected to take minutes, this false positive would fire routinely on every release run where the monitor happens to run early.

**Recommendation:**
Replace `committer.date` with the tag's tagger date or ref creation time. For lightweight tags: `gh api repos/geekatron/jerry/git/refs/tags/${latest_src_tag} | jq -r '.object.created_at'` (if available) or fall back to annotated-tag tagger date: `gh api repos/geekatron/jerry/git/tags/<tag_sha> | jq -r '.tagger.date'`. Mandate annotated tags for `v*` releases (annotated tags have a dedicated tagger date that is the tag-push time). This is consistent with how `release.yml` already works for GitHub Releases. OWNER: CI-workflow→eng-devsecops; spec→nse-requirements (REQ-049 should specify "elapsed since tag creation", not "elapsed since commit creation").

**Acceptance Criteria:** D7 freshness check uses the tag's tagger timestamp (not the commit committer date) for elapsed calculation; verified against a synthetic test where a commit predates its tag by >2h.

---

### PM-006-Q3: Race Condition Between Force-Push and Release Publish in Job C [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Technical |
| **Likelihood** | Medium — occurs whenever D7 monitor poll fires within the ~30-60s window between Job C step 1 and step 2 |
| **Section** | CI workflow §Job C (cross-repo-force-push then publish-immutable-release); CI workflow §Job M1 (bind-to-live-tip) |
| **Strategy Step** | Step 3 — Technical Failure: design weakness, ordering of operations |

**Evidence:**
Job C step sequence (CI workflow): (1) `cross-repo-force-push` → (2) `publish-immutable-release`

D7 monitor M1 step 1 (download): "Download the attested artifact from latest immutable release on dedicated repo: `gh release download --repo geekatron/jerry-cowork --pattern '*.tar'`"

D7 monitor M1 step 4 (tree-digest match): compare `expected_tip_sha` against `live_tip_sha`

**Analysis:**
After `cross-repo-force-push` completes, the dedicated repo's default branch tip is updated to the new `COMMIT_SHA`. The `live_tip_sha` (from `git ls-remote`) reflects the new SHA immediately. But the release asset (the TAR file the D7 monitor needs to download) is only published in the NEXT step (`publish-immutable-release`).

If D7 runs in this window:
- `gh release download --repo geekatron/jerry-cowork` returns the previous release's artifact (vN-1) because vN's release doesn't exist yet
- `expected_tip_sha` extracted from vN-1's release notes = vN-1's COMMIT_SHA
- `live_tip_sha = git ls-remote ... HEAD` = vN's COMMIT_SHA (already pushed)
- `expected_tip_sha (vN-1) != live_tip_sha (vN)` → CRITICAL tamper alert fires
- D7 exits 1 → auto-revert dispatches `last-good-validated` (= vN-1) → reverts the valid vN release

The `publish-immutable-release` step uses `gh release create` which takes ~10-30 seconds. The D7 monitor runs every 6 hours but can also be manually triggered. During the force-push/release-publish gap, a manual trigger or an unfortunate timing coincidence produces this false positive.

**Recommendation:**
Restructure Job C to publish the release BEFORE the force-push, or make the release atomic with the push: (a) Create the GitHub Release (on source repo, not dedicated repo) first with the artifact; then force-push; then create the dedicated-repo release pointing to the existing artifact. (b) Alternatively, add a post-push readiness check in Job C: after publishing the release, verify that `gh release download --repo geekatron/jerry-cowork --pattern "*.tar"` succeeds before the job exits, so the D7 monitor always finds a valid release once the pipeline completes. (c) Add a minimum wait or retry in the D7 monitor's release download step. OWNER: CI-workflow→eng-devsecops.

**Acceptance Criteria:** D7 monitor run initiated within 60s of force-push completion does not produce a false CRITICAL alert.

---

### PM-007-Q3: `generate-and-gate` Missing `issues: write` for G8 Early-Warning Issues [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Process |
| **Likelihood** | High — the permission gap is unambiguous from the per-job permissions table |
| **Section** | CI workflow §Per-Job Permissions Table; §g8-multi-dim-gate |
| **Strategy Step** | Step 3 — Process Failure: workflow gap, per-job permission mis-specification |

**Evidence:**
Per-job permissions table (CI workflow): "generate-and-gate | `contents: read` | Checkout (fetch-depth: 0) only; no source-repo write; git commit is local"

G8 gate (CI workflow §g8-multi-dim-gate): "IF file_count >= 3500: open_informational_issue('[INFO] file-count approaching ceiling')" and "IF pack_size_mb >= 150: open_informational_issue('[INFO] pack-size clone-weight warning')" and "IF clone_secs >= 40: open_informational_issue('[INFO] clone-weight: clone approaching limit')"

`gh issue create` requires GITHUB_TOKEN with `issues: write` permission, which the `generate-and-gate` job does not declare.

**Analysis:**
Opening a GitHub Issue via `gh issue create` fails at the API level if the GITHUB_TOKEN lacks `issues: write`. The failure from `gh issue create` produces a non-zero exit code.

If the implementation wraps with `|| true`: the early-warning issues are silently dropped. The pack-growth monitoring system (designed to give advance notice before the mandatory Option A→B orphan flip) never produces any notification. The team is blind to approaching limits until the hard-fail threshold (250 MB / 60s / 5000 files) is breached in production, at which point a RELEASE IS BLOCKED with no prior warning.

If the implementation does NOT wrap with `|| true`: every release where pack > 150 MB or clone time > 40s fails the release pipeline on a non-critical warning. Legitimate releases are blocked.

Either outcome defeats the purpose of the two-band monitoring design (REQ-034d / REQ-050).

**Recommendation:**
Add `issues: write` to the `generate-and-gate` job permissions, or restructure: move the informational-issue-opening to a post-gate step or a separate job that inherits `issues: write`. If the design intent is to keep `generate-and-gate` minimal, add a fourth job (`report`) with `issues: write` that only opens issues based on gate telemetry uploaded as job outputs. Document which job owns the issue-creation responsibility. OWNER: CI-workflow→eng-devsecops.

**Acceptance Criteria:** A workflow run where pack_size > 150 MB opens a non-blocking informational issue without blocking the release; the job exits 0 for early-warning conditions.

---

### PM-008-Q3: SBOM Generated in Attestation Job Lacking Source Checkout [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Technical |
| **Likelihood** | High — Job B downloads only the TAR artifact; `pyproject.toml`/`uv.lock` are not available |
| **Section** | attestation §7.2, §7.3 |
| **Strategy Step** | Step 3 — Technical Failure: design weakness, job placement |

**Evidence:**
Attestation design §7.2 (SBOM generation): "uv run cyclonedx-py environment -o 'sbom-jerry-cowork-${TAG}.cdx.json' --output-format JSON --schema-version 1.5"

Attestation design §7.3 (SBOM attestation step): "# In the attestation job, after the build-provenance attestation step"

CI workflow §Job B (attest): "download_artifact(<artifact-file>) — SHA-pinned actions/download-artifact; gh attestation attest <artifact-file> --repo geekatron/jerry"

Job B's only action is to download the TAR artifact and attest it. It does NOT checkout the source repo; it does NOT have access to `pyproject.toml` or `uv.lock`.

**Analysis:**
`uv run cyclonedx-py environment` generates a Software Bill of Materials from the current Python environment on the runner. In Job B, no `uv sync` or `uv install` has been run because neither the source repo nor its `pyproject.toml` is present. The runner's base environment has only what's available on `ubuntu-latest` (system Python, no Jerry dependencies). The SBOM generated would therefore enumerate:
- (a) Nothing — if `uv` isn't installed on the runner and the command fails
- (b) The runner's base system packages — completely wrong
- (c) A minimal set unrelated to Jerry's actual Python dependency surface

An incorrect SBOM that is then attested and published as `sbom-jerry-cowork-${TAG}.cdx.json` is WORSE than no SBOM: it provides false assurance to security auditors that dependency provenance is tracked, while actually providing no accurate information about the skeleton's real Python dependencies (src/, hooks/, pyproject.toml chain).

**Recommendation:**
Move the SBOM generation to Job A (`generate-and-gate`), where the source repo is checked out and `pyproject.toml`/`uv.lock` are available. Run `uv run cyclonedx-py environment` immediately after the checkout step. Upload the SBOM as an Actions artifact alongside the TAR. Job B (attestation) then downloads both the TAR and the SBOM and attests them. This preserves the job isolation (SBOM generation needs no elevated permissions) while ensuring the SBOM reflects the actual source dependency tree. OWNER: attestation→eng-infra.

**Acceptance Criteria:** The produced SBOM contains Jerry's actual declared Python dependencies from `pyproject.toml`/`uv.lock`; verified by comparing SBOM component list against `uv pip list --format=json` in the source environment.

---

### PM-009-Q3: `fetch-depth: 0` Not in Workflow Pseudocode Steps — D5 Fails for All Historical Tags [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Process |
| **Likelihood** | Medium — a Phase-6 implementer reading the workflow pseudocode steps will not see this requirement; it only appears in the traceability matrix |
| **Section** | CI workflow traceability matrix (row "G3 checkout fetch-depth: 0"); skeleton-gen §D-02; CI workflow §d5-provenance-gate |
| **Strategy Step** | Step 3 — Process Failure: workflow gap, missing explicit specification |

**Evidence:**
Traceability matrix (CI workflow): "G3 checkout fetch-depth: 0 | REQ-007 | ADR-001 §Determinism"

But the workflow pseudocode step (§g3-checkout) says only: "git checkout '${TAG}' # frozen released tree; fetch-depth: 0 already done"

The parenthetical "fetch-depth: 0 already done" implies the initial `actions/checkout` step set `fetch-depth: 0`, but this step is not shown in the pseudocode. The pseudocode begins at `resolve-and-validate-tag`, implying the implementer must infer that the `actions/checkout` action before all steps must set `fetch-depth: 0`.

The D5 provenance gate: "git fetch origin main --depth=1; git merge-base --is-ancestor '${SRC_SHA}' origin/main"

**Analysis:**
If `actions/checkout` is called with the default (`fetch-depth: 1`), only the latest commit is fetched. The runner then has only a shallow clone. When D5 runs `git merge-base --is-ancestor ${SRC_SHA} origin/main`, git must find `${SRC_SHA}` in the local history to determine ancestry. For a `workflow_dispatch` invoked with `target_tag=v0.30.0` (an older release), `SRC_SHA` points to a commit from months ago that is outside the shallow cut-off. `git merge-base --is-ancestor` on a shallow repo may:
- Return exit code 1 (not an ancestor) even for a legitimate ancestor commit — because the commit isn't in the visible history
- Return an error

Outcome: D5 rejects ALL releases older than the most recent commit, making `workflow_dispatch` re-generation of historical tags (needed for auto-revert) completely inoperable. This breaks the auto-revert mechanism in exactly the failure scenario where auto-revert is most needed (reverting to a previously-good release).

**Recommendation:**
Add `fetch-depth: 0` explicitly to the `actions/checkout` step in the workflow pseudocode in §cowork-skeleton.yml Design, not just in the traceability matrix. Add a comment: "fetch-depth: 0 is REQUIRED for: (1) Option A parent chain (G6), (2) D5 merge-base ancestry check for historical tags, (3) workflow_dispatch re-generation for auto-revert." OWNER: CI-workflow→eng-devsecops.

**Acceptance Criteria:** Workflow pseudocode explicitly declares `with: fetch-depth: 0` on the `actions/checkout` step; verified by `workflow_dispatch` with `target_tag=v0.30.0` (an older tag) passing D5 without error.

---

### PM-010-Q3: G8 Clone-Time Measurement Runs on High-Speed Runner, Not 10 Mbps Reference [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Category** | Assumption |
| **Likelihood** | High — GitHub Actions runners have network throughput orders of magnitude above 10 Mbps |
| **Section** | skeleton-gen §4 (multi-dim gate); CI workflow §g8-multi-dim-gate |
| **Strategy Step** | Step 3 — Assumption Failure: unstated assumption that runner speed ≈ reference network |

**Evidence:**
Skeleton-gen §4 dimension table: "(c) clone time | timed reference clone, or pack×bandwidth @ 10 Mbps | 120 s git-op timeout | > 60 s | > 40 s"

CI workflow §g8-multi-dim-gate: "clone_secs = timed_reference_clone() # 10 Mbps reference network (30th-pct global broadband)"

The design does not specify whether `timed_reference_clone()` is: (a) an actual timed clone on the CI runner, or (b) a formula: `pack_size_mb / 1.25 MB_per_second` (10 Mbps / 8 bits). If (a), the formula fails. If (b), the formula is not specified.

**Analysis:**
GitHub Actions `ubuntu-latest` runners are provisioned in Azure data centers with multi-Gbps internal bandwidth. An actual `git clone` of a 250 MB pack on a GitHub runner completes in approximately 1-3 seconds, not 60 seconds. An actual `timed_reference_clone()` on the runner would return ~1s, always far below the 60s hard-fail and 40s early-warning thresholds. The G8 clone-time gate (dimension c) would never trigger regardless of pack size.

If the formula approach is intended (`pack_size_mb / 1.25`), the design does not state this, and a Phase-6 implementer could use either approach. A 250 MB pack would give `250 / 1.25 = 200 seconds` via the formula — triggering the 60s hard-fail. But a 50 MB pack gives `40 seconds` — exactly at the early-warning threshold. These numbers are not cross-checked with the existing telemetry from the M3 job (which DOES do an actual timed clone separately).

The design also has the M3 monitor job in `cowork-monitor.yml` doing `timed reference clone of geekatron/jerry-cowork` — an actual clone — for telemetry. Why does M3 do an actual clone while G8 (supposedly) also does a "timed reference clone"? If both do actual clones, G8's clone-time gate is measuring runner latency, not user latency. The two jobs would always produce very different results, making the gate meaningless.

**Recommendation:**
(a) Define `timed_reference_clone()` explicitly as a formula: `CLONE_SECS_ESTIMATE = pack_size_mb / 1.25` (10 Mbps / 8). Remove the "timed reference clone" language from the G8 gate step to avoid confusion with M3's actual clone. (b) Align the G8 documentation: the G8 gate measures estimated clone time based on pack size; M3 measures actual clone time for telemetry. These serve different purposes and must not be confused. (c) Update REQ-006c to specify the formula-based measurement for the hard-fail gate. OWNER: skeleton-gen→nse-architecture; spec→nse-requirements (REQ-006c wording).

**Acceptance Criteria:** G8 clone-time measurement is a documented formula (`pack_size_mb / 1.25`), not an actual clone; verified by test that a 75 MB pack produces an estimated 60s time, triggering the hard-fail.

---

### PM-011-Q3: `last-good-validated` Tag Unprotected — Auto-Revert Target Manipulable [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Category** | Technical |
| **Likelihood** | Low — requires a source-repo write collaborator willing to act maliciously; bounded by RTB-2 |
| **Section** | CI workflow §advance-last-good-validated; ADR-003 D7(d) "last-good-validated tag advancement rule" |
| **Strategy Step** | Step 3 — Technical Failure: design weakness, protection gap |

**Evidence:**
ADR-003 D7: "'last-good-validated' SHALL be advanced to point at a release tag only after a full G-monitor pass cycle."

D5/REQ-039 applies `v*` tag protection (creation restricted to CI + maintainers), but `last-good-validated` is a non-`v*` lightweight tag. It is not in scope of the `v*` tag protection ruleset.

CI workflow §auto-revert: "last_good_tag = git describe --tags --exact-match $(git rev-parse last-good-validated); gh workflow run cowork-skeleton.yml --field target_tag=${last_good_tag}"

**Analysis:**
Any source-repo collaborator with `push` access can run `git tag -f last-good-validated <malicious-commit>; git push origin refs/tags/last-good-validated --force`. If the malicious commit is an ancestor of `main` (SC-06 surface), auto-revert then dispatches `cowork-skeleton.yml` with the malicious commit's tag, deploying it through the gated pipeline. D5 passes (ancestor of main), D6 passes (faithful derivative), D8 catches explicit patterns only.

This expands the SC-06 trusted-maintainer attack surface: instead of needing to create a `v*` tag (which is protected), the attacker needs only to move the unprotected `last-good-validated` tag. The attack requires less privilege than the baseline SC-06.

**Recommendation:**
Add `last-good-validated` to the source repo tag protection ruleset (or create a separate ruleset for `last-good-validated` restricting modification to CI only). Alternatively, use a protected branch rather than a tag for the last-good reference. OWNER: spec→ps-architect/nse-requirements (add to D5 ruleset scope or new REQ); attestation→eng-infra (provisioning).

**Acceptance Criteria:** Attempt by a non-CI principal to force-push `last-good-validated` is rejected by the ruleset.

---

### PM-012-Q3: Version Sentinel File Path Unspecified — Fallback A Silently Broken [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Category** | Assumption |
| **Likelihood** | Medium — the path ambiguity will be resolved ad-hoc in Phase 6, risking inconsistency |
| **Section** | skeleton-gen §6 (Fallback A — version sentinel A1); CI workflow §g5-static-stub |
| **Strategy Step** | Step 3 — Assumption Failure: unstated assumption about static path |

**Evidence:**
Skeleton-gen §6: "A1 — version sentinel | a static file in the generated tree (`.claude/` or the `projects/` stub), written by G5"

CI workflow §g5-static-stub: "write_static(<version-sentinel-path>)"

The path is explicitly left as a placeholder in both documents. The A2 version-check skill that reads it must know the path to function. If the A2 skill hardcodes one path and Phase-6 writes the sentinel to the other, Fallback A silently reports no version information.

**Recommendation:**
Choose and specify the sentinel path in the design (one of: `.claude/version`, `projects/.cowork-version`, `.claude-plugin/version`). Document the choice with rationale in skeleton-gen §6. Update the CI workflow pseudocode to use the concrete path. OWNER: skeleton-gen→nse-architecture.

**Acceptance Criteria:** skeleton-gen §6 specifies a single concrete path; CI workflow §g5-static-stub uses that path; A2 version-check skill reads from that path; verified by install test.

---

### PM-013-Q3: Attestation Job May Require `artifact-metadata: write` — Unconfirmed [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Category** | External |
| **Likelihood** | Low — may be resolved by confirming against the pinned action version in Phase 6; but if required and absent, ALL attestations fail |
| **Section** | attestation §2.2 |
| **Strategy Step** | Step 3 — External Failure: third-party action permission requirements |

**Evidence:**
Attestation design §2.2: "# artifact-metadata: write # Current actions/attest v4 documentation lists this as required; # Phase-6 MUST confirm exact permission set for the pinned version."

The job permissions block comments out `artifact-metadata: write` as potentially required but does not include it in the design.

**Analysis:**
If `actions/attest` at the pinned SHA requires `artifact-metadata: write` and this permission is absent from the attestation job, the action will fail with a permission error. Every attestation step fails → every push-and-release is skipped (by the `needs: attest` dependency) → NO release ever deploys. This would be caught in Phase-6 testing, but the design does not include a blocking test for it, and it could be missed if Phase-6 testing is done with a different action version than production.

**Recommendation:**
Make "confirm `artifact-metadata: write` requirement against the pinned `actions/attest` SHA" a Phase-6 blocking acceptance criterion (not just a comment). Add it to the CI-G-004 gap resolution checklist. OWNER: attestation→eng-infra.

**Acceptance Criteria:** Phase-6 documents the exact permission set required by the pinned `actions/attest` SHA; the attestation job YAML includes all required permissions; a test attestation run succeeds.

---

## Recommendations

### P0 — MUST mitigate before acceptance

| Finding | Mitigation | Acceptance Criteria |
|---------|-----------|---------------------|
| PM-001-Q3 | Add explicit post-restore SHA assertion in Job C; add post-push verification via `git ls-remote` in the pipeline | Two independent runs for same tag produce identical COMMIT_SHA; COMMIT_SHA matches dedicated-repo tip after push |
| PM-002-Q3 | Validate jq path against live `gh attestation verify --format json` output at the pinned version; add non-empty guards for ATTESTED_COMMIT and expected_tip_sha; reconcile release-note extraction vs SLSA predicate extraction | Synthetic COMMIT_SHA extraction matches known value; empty-result path exits non-zero |
| PM-003-Q3 | Block Phase-6 on delivery of D8 scanner tool and pattern catalog (C1-C6) from eng-architect; add synthetic positive test to Phase-5 gate G-content | `<content-safety-scanner>` is replaced with a named, pinned tool; synthetic injection triggers exit 1 |
| PM-004-Q3 | Add revert circuit breaker (max 2 consecutive reverts for same latest_src_tag); add logic to re-try latest_src_tag before reverting to last-good; human-escalation on circuit-breaker activation | Synthetic test: transient vN failure → auto-revert → circuit breaker fires on cycle 2; no infinite loop |

### P1 — SHOULD mitigate

| Finding | Mitigation | Acceptance Criteria |
|---------|-----------|---------------------|
| PM-005-Q3 | Use annotated tag tagger-date (not commit committer-date) for freshness elapsed calculation | D7 freshness uses `tagger.date`; verified with commit predating tag by 3h (no false positive) |
| PM-006-Q3 | Publish release BEFORE force-push in Job C, or add post-publish readiness verification | D7 monitor run within 60s of push does not produce false CRITICAL alert |
| PM-007-Q3 | Add `issues: write` to `generate-and-gate` job, or move informational-issue-opening to a dedicated `report` job | G8 early-warning issues are created successfully; release is NOT blocked by informational issues |
| PM-008-Q3 | Move `cyclonedx-py environment` to Job A (which has source checkout); upload SBOM as artifact for Job B attestation | SBOM component list matches Jerry's declared Python dependencies from `uv.lock` |
| PM-009-Q3 | Add explicit `fetch-depth: 0` to `actions/checkout` step in workflow pseudocode; add rationale comment | `workflow_dispatch` with historical tag passes D5 without error |
| PM-010-Q3 | Define clone-time as formula `pack_size_mb / 1.25`; remove "timed reference clone" from G8 gate; update REQ-006c | G8 clone-time threshold documented as formula; 75 MB pack → 60s estimate → hard-fail |

### P2 — MAY mitigate; acknowledge risk

| Finding | Risk | Monitoring |
|---------|------|------------|
| PM-011-Q3 | Malicious write-collaborator can manipulate `last-good-validated` → auto-revert deploys from attacker-controlled tag | Add `last-good-validated` to tag-protection ruleset; monitor for unexpected tag movements |
| PM-012-Q3 | Fallback A silently non-functional if sentinel path inconsistent | Specify concrete sentinel path in design before Phase-6 |
| PM-013-Q3 | Missing permission causes attestation failure for all releases | Confirm permission requirements against pinned action SHA in Phase-6 |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale (PM-NNN findings) |
|-----------|--------|--------|-----------------------------|
| Completeness | 0.20 | Negative | PM-003: D8 scanner is undefined (major gap); PM-012: sentinel path unspecified; PM-009: fetch-depth not stated in pseudocode steps |
| Internal Consistency | 0.20 | Negative | PM-002: CI workflow vs attestation design diverge on what D7 monitors compare (release-note text vs SLSA predicate); PM-010: G8 clone-time description ("timed reference clone") conflicts with CI runner reality; PM-005: freshness check uses wrong timestamp |
| Methodological Rigor | 0.20 | Negative | PM-001: CI-G-001 is an acknowledged design gap with no test commitment; PM-004: auto-revert loop not analyzed in the design; PM-006: force-push/publish race condition not addressed |
| Evidence Quality | 0.15 | Neutral | The design cites ADRs and requirements accurately; traceability matrix is thorough; evidential claims are well-grounded; findings here are from implementation gaps, not unsupported claims |
| Actionability | 0.15 | Negative | PM-007: permissions gap is not actionable from the current design (wrong permission declared); PM-008: SBOM job placement is concretely wrong; PM-003: "consume eng-architect D8 output" is a dependency with no interface contract |
| Traceability | 0.10 | Positive | Strong REQ/ADR traceability throughout all three documents; CI-G-001 through CI-G-006 gap registry is well-structured; Pending Validation sections are honest and specific |

---

## Execution Statistics

- **Total Findings:** 13
- **Critical:** 4
- **Major:** 6
- **Minor:** 3
- **Protocol Steps Completed:** 6 of 6
- **Execution ID:** Q3-0630
- **Categories covered:** Technical (9), Process (2), Assumption (2), External (1), Resource (0) — all 5 category lenses applied

---

*H-15 Self-Review Applied: All findings have specific evidence from the design documents. Severity classifications are justified against the Pre-Mortem criteria. Finding identifiers follow PM-NNN-Q3 format. Summary table matches detailed findings. No findings minimized. No sub-agents spawned (P-003). Honest about severity (P-022). Report persisted per P-002.*

*Strategy: S-004 Pre-Mortem Analysis | Template: .context/templates/adversarial/s-004-pre-mortem.md | Executed: 2026-06-30*
