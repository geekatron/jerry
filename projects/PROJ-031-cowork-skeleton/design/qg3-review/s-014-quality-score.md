# Quality Score Report: Phase-3 DESIGN (Skeleton Generation + CI Regeneration + Attestation)

## L0 Executive Summary

**Score:** 0.702/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.61)

**One-line assessment:** The design corpus is architecturally sophisticated and comprehensively traced, but three clusters of design-level defects — a semantically broken SHA-binding invariant that spans both attestation and monitor documents (DA-001), a silent determinism break from wrong GitHub Actions date-propagation mechanics (FM-007, RPN=315), and an unresolved version-sentinel path that triggers the D6 faithful-derivative gate on every release (FM-020) — prevent the design from being a correct implementation blueprint. Six distinct root issues are Critical and require design revision before Phase-5 gate validation begins; a further ten Major root issues require design document updates. The score is honest at 0.702; the design does not pass QG-3 at C4/≥0.92.

---

## Scoring Context

- **Deliverable:** Three Phase-3 design documents:
  - `projects/PROJ-031-cowork-skeleton/design/phase3-skeleton-generation-design.md` (FAD-PROJ031-3A-001)
  - `projects/PROJ-031-cowork-skeleton/design/phase3-ci-workflow-design.md` (FAD-PROJ031-3B-001, CI)
  - `projects/PROJ-031-cowork-skeleton/design/phase3-attestation-provenance-design.md` (FAD-PROJ031-3B-001, Infra)
- **Deliverable Type:** Design
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-06-30T00:00:00Z
- **Strategy Findings Incorporated:** Yes — 3 reports (S-004 Pre-Mortem: 4C/6Maj/3Min; S-012 FMEA: 4C/20Maj/15Min; S-002 Devil's Advocate: 1C/2Maj/3Min). Total raw findings deduplicated before scoring.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | **0.702** |
| **Threshold** | 0.92 (H-13) |
| **Gap to Threshold** | −0.218 |
| **Verdict** | **REVISE** (Significant rework required) |
| **Strategy Findings Incorporated** | Yes — S-004 (13 findings), S-012 (39 failure modes), S-002 (6 findings), deduplicated to 16 distinct root issues |
| **Critical Raw Findings** | 9 distinct (4+4+1 across strategies; 6 deduplicated clusters) |
| **Auto-REVISE trigger** | Yes — 6 Critical findings block acceptance regardless of composite score |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.73 | 0.146 | Extensive pseudocode and gate registry, but D8 scanner has no named tool or interface contract (PM-003/CI-G-003), version sentinel path unresolved (FM-020), fetch-depth:0 absent from workflow pseudocode (FM-019/PM-009), git bundle restore step incomplete (FM-037), SBOM in wrong job (PM-008) |
| Internal Consistency | 0.20 | 0.61 | 0.122 | Two docs contradict on D7 tree-digest binding (DA-001: ATTESTED_COMMIT=SRC_SHA ≠ G6_SHA in one; mutable release-body in the other, condemned by ADR-003 SC-04); `export` mechanism for date propagation doesn't cross GitHub Actions step boundaries (FM-007, RPN=315); sentinel path conflict with D6 gate (FM-020); committer identity claimed pinned but mechanism absent (FM-014) |
| Methodological Rigor | 0.20 | 0.64 | 0.128 | Gate ordering and fail-closed semantics are sound; but: SHA-binding approach has a fundamental methodological error (SLSA predicate records SRC_SHA, not G6_SHA — DA-001); App private key accessible in wrong job (FM-040); no workflow-level `permissions: {}` deny-all (FM-018); D7 loop has no termination condition (FM-022); v* bypass too broad (FM-034) |
| Evidence Quality | 0.15 | 0.78 | 0.117 | REQ/ADR cross-references comprehensive; Pending Validation sections honest; P-222 tagging exemplary. Gaps: G8 ceiling values have no empirical basis (FM-012); git archive "pure function" claim overstated across runner image versions (DA-004/FM-015); Fallback A network egress unvalidated (FM-036) |
| Actionability | 0.15 | 0.68 | 0.102 | Phase-5 gate registry and CI-G-001/006 gap list are strong. But: following pseudocode for Job C bundle restore produces wrong commit pushed (FM-037 — missing HEAD checkout); following `export` date-pinning produces non-deterministic commits (FM-007); D7 monitor implementation per current design always fires false CRITICAL (DA-001); G8 `issues: write` missing so informational alerts silently fail (PM-007) |
| Traceability | 0.10 | 0.87 | 0.087 | Three comprehensive traceability matrices; function-to-owner N² table; ADR section-level citations; Pending Validation named-gate references. Minor gaps: Job C `contents: write` has no REQ/ADR citation (DA-006); D7(d) SHALL compliance gap not traced to a gate (DA-003) |
| **TOTAL** | **1.00** | | **0.702** | |

---

## Detailed Dimension Analysis

### Completeness (0.73/1.00)

**Evidence:**
The design corpus is unusually thorough for Phase-3: G1–G9 algorithm with language-agnostic pseudocode, three-job CI topology with step-level pseudocode, attestation design with concrete invocation sketches, D7 monitor with freshness + integrity + auto-revert, SLSA trajectory, SBOM recommendation, and 13 traceability matrix entries per document. The 8-directory retention-surface table, plugin.json-derived completeness check, and Option A→B flip parameter are all carefully designed. Phase-5 gate set (G-headroom, G-update-pre, G-provenance, G-content, G-monitor, G-actions-write-safe) is well-structured with named blockers.

**Gaps:**

1. **D8 content-safety scanner entirely undefined (PM-003-Q3, Critical).** The only gate that inspects the markdown payload for prompt-injection is specified as `<content-safety-scanner> --fail-on-find`. No named tool, no interface contract, no pattern catalog, no acceptance criteria for Phase-5 G-content. A Phase-6 implementer cannot use this as a blueprint.

2. **Version sentinel path unresolved (FM-020-QG3, Critical; PM-012-Q3, Minor).** The design specifies `.claude/ or the projects/ stub` without committing. If placed in `.claude/`, the D6 faithful-derivative gate (`git diff --quiet "${TAG}..HEAD" -- ':!projects/' ':!tests/'`) includes `.claude/` in its diff scope and fails every release because the sentinel is absent from TAG. This is a blocking implementation defect.

3. **`fetch-depth: 0` absent from Job A workflow pseudocode (FM-019-QG3, Major; PM-009-Q3, Major).** The traceability matrix mentions it, but the actual pseudocode starts at `resolve-and-validate-tag` with no `actions/checkout` step shown. A Phase-6 implementer using the default shallow clone breaks D5 (merge-base ancestor check) for all historical tags — breaking the auto-revert path exactly when it's most needed.

4. **git bundle restore missing explicit HEAD checkout (FM-037-QG3, Major).** Job C's `git fetch <bundle-file> HEAD:refs/remotes/bundle/HEAD` followed immediately by `git push --force ... HEAD:<default-branch>` pushes the source repo's HEAD, not the generated commit. The explicit `git checkout refs/remotes/bundle/HEAD` step is absent.

5. **SBOM generated in wrong job (PM-008-Q3, Major).** The attestation design places `uv run cyclonedx-py environment` in Job B, which downloads only the TAR artifact — `pyproject.toml`/`uv.lock` are absent. The produced SBOM reflects the runner's base environment, not Jerry's dependency surface.

**Improvement Path:**
Resolve ROOT-1 through ROOT-9 in the remediation plan below. The most impactful completeness fix is specifying the exact sentinel path (one line) and adding the D8 gate specification requirement. The design's structure is already correct for everything else — targeted additions, not rewrites.

---

### Internal Consistency (0.61/1.00)

**Evidence:**
The design intends to be internally consistent — the P-022 claim-status convention is applied throughout, the three-job split is described with clear rationale, and the ADR-001/ADR-003 design decisions are correctly consumed without being re-opened. Many elements are self-consistent.

**Contradictions found:**

1. **DA-001 (Critical — load-bearing): D7 tree-digest binding mechanism contradicts between documents.**
   - `phase3-attestation-provenance-design.md` §3.2 extracts `ATTESTED_COMMIT` from `.[0].verificationResult.statement.predicate.buildDefinition.resolvedDependencies[0].digest.gitCommit`. Per SLSA provenance v1, `resolvedDependencies[0].digest.gitCommit` records the **source repo's trigger commit** (SRC_SHA = the commit the `v*` tag points to in geekatron/jerry). The G6 deterministic skeleton commit (G6_SHA) is a workflow-produced output not represented in the SLSA predicate as a resolved dependency. The comparison `ATTESTED_COMMIT != LIVE_TIP` is therefore `SRC_SHA != G6_SHA` — always true in Option A (where G6's parent is SRC_SHA). The monitor fires a CRITICAL alert on every correct release.
   - `phase3-ci-workflow-design.md` §bind-to-live-tip uses `gh api ... | jq -r '.body' | grep 'Source-Commit:' | cut -d' ' -f2` — reading G6_SHA from the mutable release-notes body. This is the mechanism condemned in ADR-003 (Options D4 analysis): "Release notes share `contents: write` — collapsed (5-strategy Critical SC-04)." The design simultaneously reintroduces what ADR-003 rejected and cites ADR-003 D4 as its foundation.
   - These two mechanisms are mutually exclusive and both are described as the D7 binding approach.

2. **FM-007-QG3 (Critical, RPN=315): Shell `export` for date variables silently lost between GitHub Actions steps.**
   The generation design (§2 G6) and CI design (STEP g6) both specify `export GIT_AUTHOR_DATE = SRC_DATE`. In GitHub Actions, each `run:` step executes in a fresh shell process. A `export` in step N is NOT available in step N+1. The correct mechanism is `echo "GIT_AUTHOR_DATE=${SRC_DATE}" >> $GITHUB_ENV`. If G5 and G6 are separate named steps (as the CI design implies), the dates revert to wall-clock time on the G6 commit, silently producing a different commit SHA on every run for the same tag. The design claims commit-SHA determinism; the mechanism specified breaks it.

3. **FM-020-QG3 (Critical): Sentinel path conflicts with D6 gate.**
   Design §3 states the sentinel "may embed only the Source-Tag + full Source-Commit" and is written by G5. D6 uses `git diff --quiet "${TAG}..HEAD" -- ':!projects/' ':!tests/'`. If the sentinel is in `.claude/`, D6 detects it as a tree change vs TAG and fails. The design's Option B (`.claude/`) for the sentinel path is inconsistent with the D6 gate's exclusion scope.

4. **FM-014-QG3 (Major): §3(a) pin table claims committer identity is pinned; pseudocode uses only `--author` flag.**
   `--author` sets GIT_AUTHOR_NAME/EMAIL; GIT_COMMITTER_NAME/EMAIL derive from `actions/checkout` git config behavior, not from an explicit pin. The table claims both are pinned; the code only pins one.

5. **PM-005-Q3 / PM-010-Q3 (Major): Freshness timestamp and clone-time description internally conflicted.**
   Freshness check fetches `'.committer.date'` of the tag's underlying commit, but the ≤2h SLA is described as time-from-tag-push. These are different values that diverge by the tag-delay. G8 uses "timed reference clone, or pack×bandwidth @ 10 Mbps" but GitHub Actions runners have Gbps-class networks making an actual clone measure meaningless.

**Improvement Path:**
ROOT-1 (SHA-binding reconciliation) is the highest-leverage fix. ROOT-2 ($GITHUB_ENV propagation) eliminates FM-007. ROOT-3 (sentinel path) fixes FM-020. The remaining consistency issues (FM-014, PM-005, PM-010) each require targeted single-section edits.

---

### Methodological Rigor (0.64/1.00)

**Evidence:**
The design applies NASA SE Processes 3/4/17 correctly (functional decomposition, MECE element inventory in FMEA confirms coverage). The fail-closed gate train, ADR-003 D4 ordering constraint, per-job permission isolation, and SLSA L3 trajectory are methodologically sound. P-222 honesty about designed-not-validated controls is applied throughout.

**Gaps:**

1. **DA-001 (Critical): SHA-binding approach has a fundamental methodological error.** The monitor's tree-digest match cannot work using SLSA predicate fields as specified — the predicate records the source commit, not the generated skeleton commit. This is not an implementation detail that Phase-6 will fix; it requires a design-level correction (adding G6_SHA as a custom attestation subject or using a different binding mechanism).

2. **FM-040-QG3 (Major): App private key accessible in wrong job — least-privilege violation.** Job A declares `environment: skeleton-push`, which makes `COWORK_APP_PRIVATE_KEY` (an environment-level secret) accessible to the generation/gating job. Job A processes declared paths from `plugin.json` (a manifest that could be adversarially crafted in a supply-chain attack). The private key should be scoped to Job C only.

3. **FM-018-QG3 (Major): No explicit `permissions: {}` deny-all at workflow level.** The design documents a negative constraint ("No workflow-level permissions: block") as a comment. Without explicit `permissions: {}`, the workflow inherits GitHub's default token permissions. A Phase-6 implementer adding a convenience workflow-level `permissions: contents: write` grants write access to all three jobs, violating ADR-003 D4 A-1.

4. **FM-022-QG3 (Major) / PM-004-Q3 (Critical): D7 monitor loop has no termination condition.** After auto-revert deploys `last-good-validated` (vN-1) because vN's pipeline failed, the monitor's next cycle downloads vN's artifact (latest source release), extracts vN's G6_SHA, reads vN-1's G6_SHA as LIVE_TIP, finds mismatch, fires CRITICAL, and dispatches auto-revert to vN-1 again. This loop continues indefinitely. The design has no circuit breaker, no revert-attempt counter, no mechanism to recognize the intentional rollback state.

5. **FM-034-QG3 (Major): v* bypass includes "designated maintainers" — unnecessarily broad.** The design's intent is "releases are created only through the generation workflow." Allowing maintainers as bypass actors enables direct tag creation outside the gated path, contradicting the topology.

6. **FM-011-QG3 / PM-010-Q3 (Major): Clone-time measurement method undefined.** G8c says "timed reference clone, or pack×bandwidth @ 10 Mbps" without specifying which. An actual clone on GitHub Actions runners (Gbps network) always returns ~1s, making the gate meaningless. A formula-based estimate is the correct approach but is not specified.

**Improvement Path:**
ROOT-1 (SHA-binding) addresses the methodological error. ROOT-6 (loop termination + circuit breaker) addresses FM-022/PM-004. ROOT-13/14/15 address the permission and bypass findings. ROOT-16 clarifies clone-time measurement.

---

### Evidence Quality (0.78/1.00)

**Evidence:**
The traceability matrices across all three documents are comprehensive — every design element cites a REQ and an ADR section. The references sections cite RFC 1952 (gzip mtime), GitHub CLI manual for `gh attestation verify`, the SLSA specification, and `actions/attest` repository. The Pending Validation sections honestly distinguish designed-not-validated from implemented-and-validated. P-222 compliance is exemplary.

**Gaps:**

1. **FM-012-QG3 (Major): G8 ceiling values have no documented empirical basis.** The thresholds (5,000 files / 250 MB / 60s) are stated as requirements (REQ-006a/b/c) but the design itself notes "file-count is the operative CoWork ceiling: unverified (may be size/time-based)" in Pending Validation. The ceilings are engineering assumptions pending G-headroom; this should be flagged explicitly in the design next to the threshold values.

2. **DA-004 (Minor) / FM-015-QG3 (Major): "Pure function" claim for `git archive` overstated.** The attestation design §1.4 states `git archive --format=tar` is a "pure function of the commit SHA" producing bit-identical output regardless of environment. This is not guaranteed across git version updates when `ubuntu-latest` is not pinned. The design correctly acknowledges TAR format behavior differences across git builds in §1.2 ("not standardized across git builds") but the §1.4 proof contradicts this caveat.

3. **FM-036-QG3 (Major): Fallback A network egress dependency unvalidated.** A2 version-check skill requires outbound GitHub API access from the CoWork sandbox. The design correctly flags this as conditional, but the evidence base for whether CoWork permits this egress is absent.

**Improvement Path:**
Add explicit "provisional pending G-headroom" annotation to the three G8 thresholds. Narrow the §1.4 determinism proof claim to "same runner image version." Add a Pending Validation item for cross-image idempotency testing.

---

### Actionability (0.68/1.00)

**Evidence:**
The Phase-5 gate registry (six named gates with Phase-5/6 resolution owners) and the CI-G-001 through CI-G-006 explicit gap registry are among the design's strongest features — they give clear, specific next steps. The pseudocode is sufficiently precise that a skilled implementer could use it as a starting point.

**Gaps:**

1. **DA-001 (Critical) + FM-037 (Major): Following the design as written produces incorrect behavior.** A Phase-6 implementer using attestation §3.2 SLSA predicate extraction will produce a monitor that always fires CRITICAL alerts. Following Job C's bundle restore pseudocode without an explicit `git checkout refs/remotes/bundle/HEAD` step before push will push the source repo's HEAD to the dedicated repo instead of the generated skeleton.

2. **FM-007-QG3 (Critical): Following the `export` date-pinning pattern produces non-deterministic commits.** The pseudocode's date-pinning mechanism doesn't work in GitHub Actions multi-step jobs. A Phase-6 implementer following the design produces a workflow that appears to succeed but generates different commit SHAs on every run.

3. **PM-007-Q3 (Major): G8 early-warning issue creation cannot work with current permission spec.** Job A has `contents: read`. Opening a GitHub Issue requires `issues: write`. The G8 pseudocode calls `open_informational_issue()` but the permission to do so is absent. Either the alerts silently fail or the job errors on the `gh issue create` call.

4. **PM-003-Q3 (Critical): D8 integration is not actionable without the pattern catalog.** "Consume eng-architect D8 output" is a dependency with no interface contract. A Phase-6 engineer cannot implement D8 integration without knowing the scanner tool, invocation flags, exit code semantics, and pattern list.

**Improvement Path:**
ROOT-1 (SHA-binding fix) and ROOT-4 (bundle HEAD checkout) directly unblock the most critical actionability failures. ROOT-2 ($GITHUB_ENV) eliminates the silent determinism break. Adding `issues: write` to the permissions table is a one-line design doc change (ROOT-8).

---

### Traceability (0.87/1.00)

**Evidence:**
All three design documents provide detailed traceability matrices linking every design element to one or more REQ numbers and ADR sections. The skeleton-gen document's 13-row matrix, CI-workflow's 30+ row matrix, and attestation design's 17-row INF-series matrix together provide comprehensive coverage. The function-to-owner N² table in the skeleton-gen design clearly delineates 3a vs. eng-devsecops vs. eng-infra scope. ADR section-level citations (not just ADR numbers) allow readers to find the exact rationale. The Pending Validation tables reference specific gate names.

**Gaps:**

1. **DA-006 (Minor): Job C GITHUB_TOKEN `contents: write` has no REQ or ADR citation** despite all other permissions having one. The note says "Matches REQ-020(a)" but REQ-020(a) requires minimal permissions, not specifically `contents: write`. No step in Job C uses source-repo GITHUB_TOKEN `contents: write` (all writes use the App token). The grant appears to be a dead permission inconsistent with ADR-003 D6 item 5 (minimal permissions per job).

2. **DA-003 (Major): D7(d) SHALL compliance gap not traced to any gate or acknowledgment.** ADR-003 D7(d) is a SHALL-tier requirement for auto-revert. The design ships without auto-revert at go-live. No Phase-5 gate requires auto-revert to be operational before go-live; the design does not explicitly acknowledge the D7(d) deferral or classify it as SHOULD vs. SHALL for the initial deployment.

**Improvement Path:**
Reduce Job C `contents: write` to `contents: read` (or justify it explicitly with a REQ citation). Add an explicit D7(d) compliance classification to the monitor design section.

---

## Improvement Recommendations (Priority Ordered)

Deduplicated from 9 raw Critical findings across three strategies into 6 distinct root issues (P0) and 10 Major root issues (P1). Calibration note: FMEA decomposes one theme into many failure modes; where multiple findings share the same root cause (same design element, same fix), they are merged.

### P0 — MUST resolve before Phase-5 gate validation begins (Design-Level Defects)

| Priority | Root Issue | Distinct Findings | Current | Fix Type | Recommendation | Owner | Cross-Doc? |
|----------|-----------|-------------------|---------|----------|----------------|-------|-----------|
| 1 | **ROOT-1: SHA-binding contradiction** — ATTESTED_COMMIT=SRC_SHA always ≠ G6_SHA (LIVE_TIP); CI workflow falls back to mutable release-body (condemned ADR-003 SC-04) | DA-001 (Critical), PM-002-Q3 (Critical), FM-023-QG3 (Critical) | Completeness/Consistency | **[FIXABLE-NOW design fix]** | Option 1 (lowest cost): Add G6_SHA as a custom attestation subject (`subject-name: generated-commit` + `subject-digest`) in the `actions/attest` call so the SLSA predicate contains G6_SHA; update monitor to extract from that subject field. Option 2: Acknowledge Mechanism 2 (release-body) is the implementation, document why it does not violate SC-04 in the dedicated-repo context (release notes on geekatron/jerry-cowork are writeable only by CI under D2 ruleset), and harden with explicit non-empty guard. Both docs must agree on a SINGLE mechanism. | **[RECONCILIATION — spans attestation §2 + CI-workflow §bind-to-live-tip]** OWNER: eng-infra (attestation §2 attestation invocation), eng-devsecops (CI-workflow §bind-to-live-tip). Both docs must be updated together. | YES — binding invariant set once in attestation design (attestation invocation), mirrored in CI-workflow monitor |
| 2 | **ROOT-2: $GITHUB_ENV propagation** — `export GIT_*_DATE` is silently lost between GitHub Actions steps; commit dates revert to wall-clock time, breaking determinism on every release | FM-007-QG3 (Critical, RPN=315), FM-014-QG3 (Major) | Consistency/Rigor | **[FIXABLE-NOW design fix]** | In BOTH skeleton-gen §2 G6 and CI-workflow STEP g6: replace `export GIT_AUTHOR_DATE=SRC_DATE` with `echo "GIT_AUTHOR_DATE=${SRC_DATE}" >> $GITHUB_ENV`. Also add `GIT_COMMITTER_NAME` and `GIT_COMMITTER_EMAIL` via `$GITHUB_ENV` to pin committer identity (FM-014). Or collapse G5+G6 into a single `run:` block. Add idempotency test: two workflow runs for same tag must produce identical COMMIT_SHA. | eng-devsecops (CI pseudocode), nse-architecture (skeleton-gen pseudocode) | NO — same fix in two docs independently |
| 3 | **ROOT-3: Version sentinel path unresolved + D6 gate conflict** — if sentinel in `.claude/`, D6 faithful-derivative gate fails every release; enforcement of invariant-only content absent | FM-020-QG3 (Critical, RPN=216), PM-012-Q3 (Minor), FM-004-QG3 (Critical, RPN=252) | Completeness/Consistency | **[FIXABLE-NOW design fix]** | Specify exact path: `projects/.cowork-version` (under `:!projects/` D6 exclusion). Update skeleton-gen §2 G5 to use this concrete path. Add post-write assertion in G5 verifying content matches `^Source-Tag: v[0-9]+\.[0-9]+(\.[0-9]+)?\nSource-Commit: [0-9a-f]{40}\n$`. Update CI-workflow §g5-static-stub. | nse-architecture (skeleton-gen §2/§6) | NO — fix in skeleton-gen only; CI-workflow pseudocode follows automatically |
| 4 | **ROOT-4: git bundle round-trip — HEAD not repositioned after fetch, SHA not verified, Option A prerequisite unaddressed** | DA-002 (Major), PM-001-Q3 (Critical), FM-037-QG3 (Major), FM-038-QG3 (Major) | Completeness/Rigor | **[FIXABLE-NOW design fix]** | Add to Job C pseudocode: `git checkout refs/remotes/bundle/HEAD` between the fetch and push steps. Add SHA assertion: `[ "$(git rev-parse HEAD)" = "${COMMIT_SHA}" ] \|\| exit_1("bundle restore SHA mismatch")`. Specify whether Job C requires `git fetch origin/main --depth=1` to supply SRC_SHA as the Option A bundle prerequisite. Mandate a smoke-test result (Job A COMMIT_SHA = `git rev-parse HEAD` in Job C after restore) in Pending Validation before Phase-5. | eng-devsecops (CI-workflow §Job C) | NO — fix in CI-workflow only |
| 5 | **ROOT-5: D8 content-safety scanner entirely undefined — no named tool, no interface contract** | PM-003-Q3 (Critical), CI-G-003 | Completeness/Actionability | **[Phase-6 implementation detail, but Phase-5 GATE BLOCKER needed now]** | Add Phase-5 blocking gate in Pending Validation: "G-content gate REQUIRES eng-architect to deliver (i) named, pinned scanner tool; (ii) C1-C6 documented patterns; (iii) interface contract (directory-path-in, exit-nonzero-on-match-or-error); (iv) synthetic positive test passing." D8 gate MUST NOT ship in Phase-6 as `<content-safety-scanner>` placeholder. | eng-devsecops (D8 integration in CI-workflow), eng-architect (owns pattern catalog — must deliver before Phase-6), nse-requirements (add to Phase-5 gate checklist) | NO — gate spec added to CI-workflow Pending Validation |
| 6 | **ROOT-6: Auto-revert infinite loop + D7(d) SHALL compliance gap** — revert-to-last-good never fixes missing new release; D7(d) SHALL ships absent at go-live | PM-004-Q3 (Critical), FM-022-QG3 (Major), DA-003 (Major) | Rigor/Consistency | **[FIXABLE-NOW design fix for circuit breaker; explicit compliance decision required for D7(d)]** | (a) Loop: Add revert circuit breaker — if M2 dispatched a revert for the same `latest_src_tag` in the previous cycle AND `LIVE_TIP == last-good-validated-SHA`, suppress M2 and open a human-escalation CRITICAL issue instead. Add logic to attempt `latest_src_tag` re-generation first; only fall back to revert if re-generation also fails. (b) D7(d) compliance: Explicitly classify in the CI-workflow design whether go-live proceeds with or without auto-revert. If without: acknowledge D7(d) SHALL is not satisfied at go-live and add a post-go-live gate for auto-revert enablement. If with: make G-actions-write-safe a go-live blocker in the Phase-5 gate set. | eng-devsecops (CI-workflow §Job M2), nse-architecture (D7(d) compliance classification in design) | NO |

---

### P1 — SHOULD resolve before Phase-6 implementation (Design Document Updates)

| Priority | Root Issue | Distinct Findings | Fix Type | Recommendation | Owner |
|----------|-----------|-------------------|----------|----------------|-------|
| 7 | **ROOT-7: `fetch-depth: 0` absent from Job A workflow pseudocode** | FM-019-QG3, PM-009-Q3 | **[FIXABLE-NOW design fix]** | Add explicit `STEP actions-checkout: uses: actions/checkout@{PINNED_SHA} with: fetch-depth: 0` as the FIRST step in Job A pseudocode with comment: "REQUIRED for (1) Option A parent chain, (2) D5 merge-base check for historical tags, (3) workflow_dispatch auto-revert of historical tags." | eng-devsecops |
| 8 | **ROOT-8: `generate-and-gate` missing `issues: write` permission** | PM-007-Q3 | **[FIXABLE-NOW design fix]** | Add `issues: write` to Job A per-job permissions table. Or add a fourth non-blocking `report` job with `issues: write` that opens informational issues based on Job A telemetry outputs. | eng-devsecops |
| 9 | **ROOT-9: SBOM generation in wrong job (Job B lacks source checkout)** | PM-008-Q3 | **[FIXABLE-NOW design fix]** | Move `uv run cyclonedx-py environment` to Job A (which has source checkout); upload SBOM as Actions artifact alongside TAR; Job B attestation job downloads both and attests both. | eng-infra |
| 10 | **ROOT-10: Freshness check uses commit date, not tag creation time** | PM-005-Q3 | **[FIXABLE-NOW design fix]** | Replace `jq -r '.committer.date'` with annotated tag tagger date: mandate annotated tags for `v*` releases (which have a dedicated tagger timestamp = tag push time); update REQ-049 wording to specify "elapsed since tag creation, not since source commit." | eng-devsecops, nse-requirements |
| 11 | **ROOT-11: Race condition between force-push and release publish in Job C** | PM-006-Q3 | **[FIXABLE-NOW design fix]** | Restructure Job C: publish the release BEFORE force-push so the D7 monitor always finds a valid release asset once the live tip is updated. Or add a post-publish readiness verification before the job exits. | eng-devsecops |
| 12 | **ROOT-12: Workflow-level permissions not explicitly denied** | FM-018-QG3 | **[FIXABLE-NOW design fix]** | Add explicit `permissions: {}` at the workflow level in the CI pseudocode (not just a comment). Update Per-Job Permissions Table to note: "workflow-level: `permissions: {}` (deny all; each job declares its minimum)." | eng-devsecops |
| 13 | **ROOT-13: App private key accessible in wrong job** | FM-040-QG3 | **[FIXABLE-NOW design fix]** | Split environment roles: create a `skeleton-gate` environment (branch policy only, no App key) for Job A; keep `skeleton-push` (with App private key) for Job C only. | eng-infra |
| 14 | **ROOT-14: v* bypass includes "designated maintainers" — unnecessarily broad** | FM-034-QG3 | **[FIXABLE-NOW design fix]** | Remove "designated maintainers" from `bypass_actors` for `v*` tags. CI identity is the sole bypass actor. Human-initiated releases use `workflow_dispatch`, not direct tag push. | eng-infra |
| 15 | **ROOT-15: Clone-time measurement method undefined (runner network vs. formula)** | PM-010-Q3, FM-011-QG3 | **[FIXABLE-NOW design fix]** | Define G8c as formula: `CLONE_SECS_ESTIMATE = pack_size_mb / 1.25` (10 Mbps / 8 = 1.25 MB/s). Remove "timed reference clone" language from the G8 gate step. Clarify that M3 does an actual clone for telemetry; G8 uses a formula-based estimate. Update REQ-006c wording. | nse-architecture, nse-requirements |
| 16 | **ROOT-16: `last-good-validated` tag unprotected — auto-revert target manipulable** | PM-011-Q3 | **[FIXABLE-NOW design fix]** | Add `last-good-validated` to the source repo tag protection ruleset (or create a separate ruleset restricting modification to CI only). Update D5 scope note. | ps-architect/nse-requirements, eng-infra |

---

### P2 — Bounded or post-go-live (acknowledgment sufficient)

| Root Issue | Finding(s) | Recommendation |
|-----------|------------|----------------|
| `artifact-metadata: write` possibly missing | PM-013-Q3, FM-027-QG3 | Make "confirm `artifact-metadata: write` requirement against pinned `actions/attest` SHA" a Phase-6 blocking acceptance criterion in CI-G-004 gap resolution checklist. Owner: eng-infra |
| git archive cross-runner image drift | DA-004 (Minor), FM-015-QG3 (Major) | Narrow §1.4 "pure function" claim to "same runner image version with same git binary"; add Pending Validation item for cross-image idempotency. Consider pinning `ubuntu-24.04` instead of `ubuntu-latest`. Owner: eng-infra |
| SBOM scope overruns P-020 constraint | DA-005 (Minor) | Formally defer SBOM to post-go-live Phase-7. Remove "IN" recommendation from Phase-3 design; add REQ only when stakeholders accept scope. Owner: eng-infra + orchestrator |
| Job C dead `contents: write` grant | DA-006 (Minor) | Reduce GITHUB_TOKEN Job C to `contents: read` (all writes use App token); document in Per-Job Permissions Table. Owner: eng-devsecops |
| `git ls-remote` step has no timeout | FM-025-QG3 (Minor) | Add `timeout-minutes: 5` to monitor's `git ls-remote` and `gh api` steps. Owner: eng-devsecops |
| G8 ceiling values empirically unverified | FM-012-QG3 (Major) | Annotate 5,000 / 250 MB / 60s thresholds as "provisional pending G-headroom empirical validation" in the design. Owner: nse-requirements |

---

## Binding Invariant Reconciliation Note

**CROSS-DOC RECONCILIATION REQUIRED before Phase-5 gate validation.**

The SHA-binding invariant — how the D7 monitor binds a Sigstore attestation to the live dedicated-repo tip — is currently defined differently and incorrectly in two design documents:

| Document | Described mechanism | Problem |
|----------|--------------------|----|
| `phase3-attestation-provenance-design.md` §3.2 | Extract `gitCommit` from SLSA predicate | SLSA predicate records SRC_SHA (source trigger commit), not G6_SHA (generated skeleton commit); comparison always fails |
| `phase3-ci-workflow-design.md` §bind-to-live-tip | Parse G6_SHA from release-notes body (`.body \| grep 'Source-Commit:'`) | Mechanically works, but release-notes body is mutable metadata condemned in ADR-003 SC-04 |

**Resolution path (pick one, update BOTH docs consistently):**

- **Option A (recommended):** Add G6_SHA as an explicit attestation subject or predicate metadata in the `actions/attest` call (attestation §2 must be updated to specify this). The monitor then extracts G6_SHA from that subject field, not from `resolvedDependencies[0].digest.gitCommit`. This makes the Sigstore attestation the authoritative, tamper-evident binding. **Sets the invariant in the attestation design (§2) and the monitor must mirror it (CI-workflow §bind-to-live-tip).**

- **Option B:** Formally adopt release-body extraction as the mechanism. Acknowledge this uses mutable metadata but argue that under D2 (org-level ruleset, CI sole bypass on dedicated repo), the release body on `geekatron/jerry-cowork` can only be modified by CI — different from the SC-04 scenario which concerned the source repo. Add explicit non-empty guards for `expected_tip_sha`. **Sets the invariant in the CI-workflow design (§bind-to-live-tip) and the attestation design must remove the contradictory SLSA predicate extraction (§3.2 steps 3-5 must be rewritten).**

Both options require updates to both documents simultaneously. The binding invariant cannot be set in one document and ignored in the other.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing the composite
- [x] Evidence documented for each score — specific finding IDs and design sections cited
- [x] Uncertain scores resolved downward (e.g., Internal Consistency scored 0.61 not 0.70 despite extensive traceability, because the DA-001 contradiction is fundamental to the design's core claim)
- [x] First-draft calibration considered — this is a sophisticated design document; anchoring to 0.65-0.80 for first drafts; the score of 0.702 is above the lower bound given the genuine strengths in structure, traceability, and gate design
- [x] No dimension scored above 0.95 without exceptional evidence — Traceability at 0.87 is the highest, justified by three comprehensive matrices and exemplary P-222 honesty
- [x] Anti-leniency applied: the DA-001 finding is architecturally load-bearing (the D7 monitor's core detection claim is demonstrably wrong per the SLSA predicate schema), scored as a genuine contradiction rather than an "implementation detail to be resolved in Phase-6"

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.702
threshold: 0.92
weakest_dimension: Internal Consistency
weakest_score: 0.61
critical_findings_count: 9  # raw; 6 distinct deduplicated clusters
iteration: 1
improvement_recommendations:
  - "ROOT-1: Resolve SHA-binding contradiction — specify working tamper-evident D7 binding (ATTESTED_COMMIT=SRC_SHA, not G6_SHA) — RECONCILIATION spans attestation §2 + CI-workflow §bind-to-live-tip"
  - "ROOT-2: Fix $GITHUB_ENV cross-step propagation for GIT_AUTHOR/COMMITTER_DATE (export silently lost between steps — FM-007, RPN=315)"
  - "ROOT-3: Specify exact version sentinel path under projects/ (FM-020 — sentinel in .claude/ breaks D6 every release)"
  - "ROOT-4: Add git checkout refs/remotes/bundle/HEAD + SHA assertion to Job C bundle restore (FM-037)"
  - "ROOT-5: Add Phase-5 blocking gate for D8 scanner delivery from eng-architect before Phase-6 (PM-003)"
  - "ROOT-6: Add auto-revert circuit breaker; explicitly classify D7(d) SHALL go-live compliance (PM-004/DA-003)"
  - "ROOT-7: Add explicit actions/checkout fetch-depth:0 as first step in Job A pseudocode (FM-019)"
  - "ROOT-8: Add issues:write to generate-and-gate or create report job (PM-007)"
  - "ROOT-9: Move SBOM generation to Job A where source checkout is available (PM-008)"
  - "ROOT-10: Use annotated tag tagger date for freshness elapsed calculation (PM-005)"
  - "ROOT-11: Publish release before force-push in Job C to close race condition (PM-006)"
  - "ROOT-12: Add explicit permissions:{} deny-all at workflow level (FM-018)"
  - "ROOT-13: Scope App private key to Job C only — split skeleton-push environment (FM-040)"
  - "ROOT-14: Remove designated maintainers from v* tag bypass actors (FM-034)"
  - "ROOT-15: Define G8c clone-time as formula pack_size_mb/1.25, not actual clone (PM-010)"
  - "ROOT-16: Protect last-good-validated tag against non-CI modification (PM-011)"
```

---

*S-014 LLM-as-Judge | adv-scorer v1.0.0 | H-15 self-review applied | P-003 no sub-agents spawned | P-022 honest scoring — score is 0.702, below 0.92 threshold | P-002 persisted to file*
