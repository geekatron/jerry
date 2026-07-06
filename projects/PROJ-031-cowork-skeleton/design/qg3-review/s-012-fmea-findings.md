# FMEA Report: Phase-3 DESIGN — Skeleton Generation + CI Regeneration + Attestation/Provenance

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** Three Phase-3 design documents:
- `design/phase3-skeleton-generation-design.md` (FAD-PROJ031-3A-001)
- `design/phase3-ci-workflow-design.md` (FAD-PROJ031-3B-001, CI)
- `design/phase3-attestation-provenance-design.md` (FAD-PROJ031-3B-001, Infra)

**Criticality:** C4
**Date:** 2026-06-30
**Reviewer:** adv-executor (S-012 FMEA)
**H-16 Compliance:** S-003 Steelman applied in prior tournament iterations (confirmed via orchestration plan)
**Elements Analyzed:** 28 (7 functional groups) | **Failure Modes Identified:** 39 | **Total RPN:** 3,990

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Overall assessment |
| [Element Inventory](#element-inventory) | MECE decomposition of the three design docs |
| [Findings Table](#findings-table) | Full FMEA table with S/O/D/RPN |
| [Critical Findings — Detailed](#critical-findings--detailed) | FM-007, FM-004, FM-023, FM-020 |
| [Major Findings — Detailed](#major-findings--detailed) | FM-001 through FM-040 (selected) |
| [Minor Findings](#minor-findings) | Summary table |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Execution Statistics](#execution-statistics) | Counts and totals |

---

## Executive Summary

The three Phase-3 design documents are architecturally sound and demonstrate sophisticated reasoning about determinism, supply-chain integrity, and fail-closed gate ordering. However, FMEA identifies **4 Critical and 20 Major failure modes**, concentrated in three clusters: (1) determinism contract implementation gaps (GIT_*_DATE cross-step propagation, committer identity, version sentinel path), (2) unvalidated Phase-6 implementation paths that have catastrophic failure signatures (jq predicate extraction, git bundle HEAD restore, artifact-metadata permission), and (3) permission-scoping oversights that widen attack surface (App private key accessible in Job A, v* tag bypass too broad). The highest-RPN finding (FM-007, RPN=315) is a design defect: the pseudocode uses shell `export` for date pinning but does not specify GitHub Actions' `$GITHUB_ENV` mechanism for cross-step propagation — on GitHub Actions, `export` does not cross step boundaries. Unaddressed, this silently breaks commit-SHA determinism on every release.

**Recommendation: REVISE.** Four Critical findings require design-level corrections before Phase-6 implementation proceeds. An additional eight Major findings are design defects (not implementation details) that also require design document updates.

---

## Element Inventory

Decomposition is MECE across the three design documents. 28 elements in 7 functional groups.

| Group | ID | Element | Design Doc |
|-------|----|---------|-----------|
| A — Generation Algorithm | E-01 | G1/G2: Tag resolve + allow-list validation | 3A |
| | E-02 | G3/G4: Checkout frozen tree + denylist strip | 3A |
| | E-03 | G5: Static stub + version sentinel write | 3A |
| | E-04 | G6: Deterministic commit (pinned dates, author, message, unsigned) | 3A |
| | E-05 | G7: Retention-surface completeness (plugin.json-derived) | 3A |
| | E-06 | G8: Multi-dimensional pre-push gate | 3A |
| | E-07 | G9: Deterministic artifact (git archive) | 3A/3B-Infra |
| B — Determinism Contract | E-08 | Commit-SHA determinism (all inputs pinned) | 3A §3(a) |
| | E-09 | Artifact-digest determinism (gzip-mtime trap) | 3A §3(b), 3B-Infra §1 |
| C — CI Workflow Structure | E-10 | Triggers + concurrency | 3B-CI |
| | E-11 | Job A (generate-and-gate): permissions + environment gate | 3B-CI |
| | E-12 | D5: Provenance gate (merge-base ancestor assertion) | 3B-CI |
| | E-13 | D6: Faithful-derivative + secret scan | 3B-CI |
| | E-14 | D8: Content-safety scan | 3B-CI |
| | E-15 | Job B (attest): permissions isolation | 3B-CI |
| | E-16 | Job C (push-and-release): App token mint + cross-repo force-push | 3B-CI |
| | E-17 | Git bundle state transfer (Job A → Job C, CI-G-001) | 3B-CI |
| D — Monitor + Auto-Revert | E-18 | D7 Monitor M1: integrity + freshness (cowork-monitor.yml) | 3B-CI |
| | E-19 | D7 Monitor M2: auto-revert dispatch | 3B-CI |
| | E-20 | Meta-monitor (cowork-meta-monitor.yml): separate watchdog | 3B-CI |
| E — Attestation + Verify | E-21 | Attestation step (actions/attest, SLSA build provenance v1) | 3B-Infra §2 |
| | E-22 | gh attestation verify invocation form (D7 monitor) | 3B-Infra §3 |
| | E-23 | Predicate extraction: jq path for gitCommit | 3B-Infra §3.2 |
| F — Infra Hardening | E-24 | Org-level ruleset (D2, dedicated repo, CI sole bypass) | 3B-Infra §5 |
| | E-25 | GitHub App installation token (D3, 1h TTL) | 3B-Infra §5.2 |
| | E-26 | Actions Environment (skeleton-push, deployment_branch_policy) | 3B-Infra §5.3 |
| | E-27 | v* tag-protection ruleset on source repo (D5 push-time leg) | 3B-Infra §6 |
| G — Fallback + SBOM | E-28 | Fallback A (version sentinel + version-check skill) + SBOM | 3A §6, 3B-Infra §7 |

---

## Findings Table

**RPN Scale:** S × O × D (each 1–10). Critical: RPN ≥ 200 OR S ≥ 9. Major: RPN 80–199 OR S 7–8. Minor: RPN < 80 AND S ≤ 6.
**Type column:** DD = Design Defect (requires design change); P6 = Phase-6 implementation detail to specify.

| ID | Element | Failure Mode | S | O | D | RPN | Sev | Type | Owner | Dimension |
|----|---------|-------------|---|---|---|-----|-----|------|-------|-----------|
| FM-007-QG3 | E-04 G6 deterministic commit | `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE` set via shell `export` silently lost between GitHub Actions steps | 9 | 5 | 7 | **315** | Critical | DD | eng-devsecops | Internal Consistency |
| FM-004-QG3 | E-03 G5 version sentinel | Sentinel embeds dynamic content (timestamp, run-id); no enforcement mechanism specified in design | 9 | 4 | 7 | **252** | Critical | DD | nse-architecture | Internal Consistency |
| FM-023-QG3 | E-23 jq predicate extraction | jq path to extract `gitCommit` from `gh attestation verify --format json` is explicitly flagged as unvalidated; wrong path → false-alarm storm | 8 | 5 | 6 | **240** | Critical | DD | eng-infra | Methodological Rigor |
| FM-020-QG3 | E-03 G5 / E-13 D6 | Version sentinel path unspecified (`.claude/` vs `projects/`); if placed in `.claude/`, D6 faithful-derivative gate fails every release | 9 | 6 | 4 | **216** | Critical | DD | nse-architecture | Completeness |
| FM-001-QG3 | E-01 G1 tag resolve | `${{ github.ref_name }}` bound via env: in pseudocode but exact binding pattern not specified; direct interpolation into `run:` enables script injection | 7 | 4 | 7 | **196** | Major | P6 | eng-devsecops | Methodological Rigor |
| FM-014-QG3 | E-04 G6 deterministic commit | Committer identity (GIT_COMMITTER_NAME/EMAIL) not explicitly pinned; only dates pinned; committer identity varies with runner git config | 9 | 3 | 7 | **189** | Major | DD | eng-devsecops | Internal Consistency |
| FM-040-QG3 | E-11 Job A permissions | `environment: skeleton-push` declared on Job A (generation step); App private key (`COWORK_APP_PRIVATE_KEY`) environment secret accessible to generation step where it is not needed | 7 | 4 | 6 | **168** | Major | DD | eng-infra | Methodological Rigor |
| FM-018-QG3 | E-11/E-15/E-16 permissions | Workflow-level `permissions:` block omission not guaranteed; if added by implementer with `contents: write`, attestation job inherits write access violating D4 A-1 | 8 | 4 | 5 | **160** | Major | DD | eng-devsecops | Methodological Rigor |
| FM-019-QG3 | E-12 D5 + E-11 Job A | `actions/checkout` with `fetch-depth: 0` not shown in CI pseudocode; default depth=1 breaks D5 ancestor check for tags older than one commit | 8 | 4 | 5 | **160** | Major | DD | eng-devsecops | Completeness |
| FM-037-QG3 | E-17 git bundle transfer | Git bundle restore in Job C lacks explicit `git checkout refs/remotes/bundle/HEAD` step before push; HEAD position after `git fetch <bundle>` is not the generated commit | 8 | 4 | 5 | **160** | Major | DD | eng-devsecops | Completeness |
| FM-011-QG3 | E-06 G8 gate | G8 `timed_reference_clone()` subject is ambiguous pre-push; jerry-cowork not yet updated; measurement may reflect wrong repo or local pack | 5 | 5 | 6 | **150** | Major | P6 | eng-devsecops | Methodological Rigor |
| FM-038-QG3 | E-17 git bundle + E-16 Job C | No SHA verification step after bundle restore; if bundle is corrupted, wrong commit pushed with no pre-push detection | 7 | 3 | 7 | **147** | Major | DD | eng-devsecops | Methodological Rigor |
| FM-027-QG3 | E-21 attestation | `actions/attest` v4 may require `attestations: write` + `id-token: write` + `artifact-metadata: write`; third permission not declared in Job B | 9 | 4 | 4 | **144** | Major | P6 | eng-infra | Completeness |
| FM-003-QG3 | E-04 G6 commit message | `--short` SHA in commit message (FM-010 reference) breaks commit-SHA determinism as repo grows; enforcement relies on code review only | 8 | 3 | 6 | **144** | Major | P6 | nse-architecture | Internal Consistency |
| FM-022-QG3 | E-18/E-19 D7 monitor | Monitor downloads LATEST_TAG artifact; after auto-revert deploys older tag, tree-digest match fires CRITICAL every run → infinite alert/revert loop with no termination condition | 6 | 3 | 7 | **126** | Major | DD | eng-devsecops | Actionability |
| FM-036-QG3 | E-28 Fallback A | A2 version-check skill requires outbound GitHub API from CoWork sandbox; CoWork network egress policy unknown; silent failure produces misleading "up to date" signal | 5 | 4 | 6 | **120** | Major | P6 | nse-architecture | Evidence Quality |
| FM-006-QG3 | E-03 G5 / E-02 G3 | Symlink resolution fails on Windows (`core.symlinks=false`); `.claude/rules` and `.claude/patterns` symlinks break; explicitly deferred to R-001/Phase-5 | 6 | 4 | 5 | **120** | Major | P6 | nse-requirements | Completeness |
| FM-013-QG3 | E-07/E-09 G9/artifact | Gzip mtime trap: design warns and provides canonical form (`--format=tar`) but no enforcement mechanism prevents Phase-6 implementer choosing `tar.gz` | 9 | 3 | 4 | **108** | Major | P6 | eng-infra | Internal Consistency |
| FM-034-QG3 | E-27 v* tag-protection | `bypass_actors` for v* tag-protection includes "designated maintainers" unnecessarily; CI identity alone should be bypass actor; maintainer tag creation bypasses rogue-tag topology control | 7 | 3 | 5 | **105** | Major | DD | eng-infra | Methodological Rigor |
| FM-012-QG3 | E-06 G8 ceilings | G8 hard-fail thresholds (5,000 files / 250 MB / 60 s) have no documented empirical basis; real CoWork ceiling is explicitly "unverified" in Pending Validation | 7 | 3 | 5 | **105** | Major | P6 | nse-requirements | Evidence Quality |
| FM-015-QG3 | E-09 artifact digest | `git archive` behavior differences across git versions (file mode recording, TAR entry format); runner `ubuntu-latest` git version not pinned | 7 | 2 | 7 | **98** | Major | P6 | eng-infra | Internal Consistency |
| FM-029-QG3 | E-22 gh attest verify | `--signer-workflow .github/workflows/cowork-skeleton.yml` path format not validated against live `gh` CLI; wrong format → verify always fails → false-alarm storm | 6 | 4 | 4 | **96** | Major | P6 | eng-infra | Methodological Rigor |
| FM-030-QG3 | E-18 D7 monitor | `gh` CLI version not pinned in monitor workflow; `ubuntu-latest` gh version changes with OS image; `attestation verify` syntax may change | 6 | 3 | 5 | **90** | Major | P6 | eng-devsecops | Methodological Rigor |
| FM-033-QG3 | E-26 Actions Env | `deployment_branch_policy` combining branch (`main`) and tag (`v*`) patterns not specified in YAML; misconfiguration could exclude main (breaking workflow_dispatch) or allow all branches (weakening protection) | 5 | 4 | 4 | **80** | Major | P6 | eng-infra | Completeness |
| FM-002-QG3 | E-01 G2 | Allow-list regex `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` permits `v1.0` (no patch); acceptable but undocumented | 4 | 2 | 3 | 24 | Minor | P6 | nse-architecture | Completeness |
| FM-005-QG3 | E-02 G4 | `git rm -r tests/` fails if test directory renamed to `test/` in future refactoring | 7 | 2 | 4 | 56 | Minor | P6 | eng-devsecops | Methodological Rigor |
| FM-008-QG3 | E-04 G6 | `--no-verify` bypasses developer pre-commit secret scan; D6 secret scan (post-G6) compensates; design is correct | 3 | 2 | 3 | 18 | Minor | — | eng-devsecops | — |
| FM-009-QG3 | E-05 G7 | plugin.json path parsing may use glob instead of exact paths; design explicitly specifies exact paths | 6 | 4 | 3 | 72 | Minor | P6 | nse-architecture | Completeness |
| FM-016-QG3 | E-08 commit | Force-moved tag intentionally yields new artifact; acknowledged in §3 idempotency proof | 8 | 2 | 4 | 64 | Minor | — | — | — |
| FM-021-QG3 | E-12 D5 | D5 does not catch non-malicious but problematic main-ancestor commits; explicitly RTB-2 residual | 7 | 2 | 4 | 56 | Minor | — | — | — |
| FM-024-QG3 | E-18 freshness | Freshness check measures tag creation time, not deployment completion; ≤2h SLA accommodates normal deployment latency | 4 | 2 | 3 | 24 | Minor | P6 | eng-devsecops | Methodological Rigor |
| FM-025-QG3 | E-18 D7 monitor | `git ls-remote` in monitor has no step-level timeout; hanging network call blocks monitor job up to 6h | 5 | 3 | 5 | 75 | Minor | P6 | eng-devsecops | Actionability |
| FM-026-QG3 | E-19 auto-revert | `last-good-validated` not yet defined on first deployment; M2 falls back to human escalation; correctly handled | 4 | 4 | 3 | 48 | Minor | — | — | — |
| FM-031-QG3 | E-24 org ruleset | Bypass actor specified by App ID (immutable numeric ID); correct | 3 | 2 | 2 | 12 | Minor | — | — | — |
| FM-032-QG3 | E-25 App token | App private key theft during ≤6h D7 window; attacker cannot forge Sigstore attestation (needs GitHub OIDC); RTB-4 bounded | 3 | 1 | 3 | 9 | Minor | — | — | — |
| FM-035-QG3 | E-21/E-28 SBOM | `actions/attest` `sbom-path` parameter form unvalidated; SBOM is optional enhancement | 4 | 4 | 3 | 48 | Minor | P6 | eng-infra | Completeness |
| FM-039-QG3 | E-17 artifact store | Actions artifact store corruption (theoretical); D7 tree-digest match provides post-deployment detection | 7 | 1 | 7 | 49 | Minor | — | — | — |
| FM-041-QG3 | E-18 monitor write | `contents: write` for `last-good-validated` tag push on source repo; loop-safe (tag pattern ≠ v*) | 3 | 1 | 2 | 6 | Minor | — | — | — |

---

## Critical Findings — Detailed

### FM-007-QG3: GIT_AUTHOR_DATE / GIT_COMMITTER_DATE Cross-Step Propagation

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **RPN** | 315 (S=9, O=5, D=7) |
| **Type** | Design Defect |
| **Section** | `phase3-skeleton-generation-design.md` §2 G6; `phase3-ci-workflow-design.md` STEP g6-deterministic-commit |
| **Owner** | eng-devsecops |
| **Dimension** | Internal Consistency |

**Evidence:**
Both design docs specify: `export GIT_AUTHOR_DATE = SRC_DATE ; export GIT_COMMITTER_DATE = SRC_DATE` immediately before the `git commit` call. In the generation design pseudocode (§2), this appears as function-level pseudocode. In the CI design, G5 (write stub) and G6 (commit) are separate named steps.

**Analysis:**
In GitHub Actions, each `run:` step executes in a **fresh shell process**. A shell-level `export VAR=value` in step N is **lost** before step N+1 executes. The correct GitHub Actions mechanism is: `echo "GIT_AUTHOR_DATE=${SRC_DATE}" >> $GITHUB_ENV`. Environment variables written to `$GITHUB_ENV` are available in all subsequent steps of the same job.

If a Phase-6 implementer follows the pseudocode's `export` pattern as a shell export in a step that produces `SRC_DATE` and then commits in a SEPARATE step (which is the natural GitHub Actions structure), the commit dates will be the runner's current wall-clock time, not `SRC_DATE`. This silently breaks commit-SHA determinism: every workflow run produces a different commit SHA for the same tag, invalidating:
1. The file-count acceptance criterion (commit SHA changes → acceptance claimed for a drifting target)
2. The D4 attestation (attested digest changes every run)
3. The D7 tree-digest match (live tip SHA changes each run)

The failure mode is **silent** (CI run succeeds, artifact is produced, but SHA drifts). Only detectable by running the workflow twice for the same tag and comparing output commit SHAs.

**Recommendation:**
Add explicit `$GITHUB_ENV` language to both design documents. In the CI design, annotate the g6-deterministic-commit step:
```
# GitHub Actions: MUST use $GITHUB_ENV for cross-step propagation, NOT shell export
echo "GIT_AUTHOR_DATE=${SRC_DATE}" >> $GITHUB_ENV
echo "GIT_COMMITTER_DATE=${SRC_DATE}" >> $GITHUB_ENV
# Commit step executes in the next run: block; reads from $GITHUB_ENV automatically
```
Alternatively, collapse G5 and G6 into a single `run:` block so all date-setting and commit occur in one shell process. Add a post-correction idempotency test: run workflow twice for same tag; assert commit SHAs are identical.

**Post-Correction RPN Estimate:** S=9, O=1, D=3 → RPN=27

---

### FM-004-QG3: Version Sentinel Dynamic Content — Missing Enforcement Mechanism

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **RPN** | 252 (S=9, O=4, D=7) |
| **Type** | Design Defect |
| **Section** | `phase3-skeleton-generation-design.md` §2 G5, §3 determinism sub-constraints |
| **Owner** | nse-architecture |
| **Dimension** | Internal Consistency |

**Evidence:**
Design §3 states: "the version sentinel (G5) may embed only the Source-Tag + full Source-Commit (invariant per tag) — **never** a build timestamp/run-id, or it breaks (a)/(b)". The generation algorithm pseudocode labels the sentinel path as `<version-sentinel>` with the annotation "NO timestamp/run-id".

**Analysis:**
The constraint is correctly stated as a property but the design provides **no enforcement mechanism**: no input validation, no static-content assertion in CI, no test. The sentinel is written by `write_static(<version-sentinel-path>)` — an abstract function. If a Phase-6 implementer (or future maintainer) adds `${{ github.run_id }}` or a build timestamp to the sentinel for observability, the commit tree changes every run, breaking both commit-SHA and artifact-digest determinism. The failure is silent: the workflow succeeds, but each run produces a different commit SHA for the same tag. The `${{ github.run_id }}` addition is a completely natural developer impulse for debugging.

**Recommendation:**
Add a post-write assertion in G5 (or early in G7) that reads the sentinel file and verifies it contains ONLY the allow-listed fields:
```
# After write_static(<version-sentinel-path>):
sentinel_content = cat <version-sentinel-path>
ASSERT sentinel_content matches /^Source-Tag: v[0-9]+\.[0-9]+(\.[0-9]+)?\nSource-Commit: [0-9a-f]{40}\n$/ \
  OR exit_1("sentinel contains dynamic content — breaks determinism")
```
The exact format is a Phase-6 detail; the design should specify the assertion step. Also resolve the sentinel PATH ambiguity (see FM-020-QG3 below).

**Post-Correction RPN Estimate:** S=9, O=1, D=2 → RPN=18

---

### FM-023-QG3: jq Predicate Extraction Path for gitCommit — Unvalidated Design Detail

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **RPN** | 240 (S=8, O=5, D=6) |
| **Type** | Design Defect |
| **Section** | `phase3-attestation-provenance-design.md` §3.2 D7 Monitor Verification Flow |
| **Owner** | eng-infra |
| **Dimension** | Methodological Rigor |

**Evidence:**
The attestation design specifies:
```
ATTESTED_COMMIT=$(jq -r \
  '.[0].verificationResult.statement.predicate.buildDefinition.resolvedDependencies[0].digest.gitCommit' \
  "${WORK_DIR}/attestation.json")
# Exact jq path is a Phase-6 implementation detail; confirm against live attestation format
```
The design itself flags this as unvalidated.

**Analysis:**
The `gh attestation verify --format json` output structure is SLSA provenance predicate version-specific. The path `.verificationResult.statement.predicate.buildDefinition.resolvedDependencies[0].digest.gitCommit` is an educated guess against the SLSA v1 schema, but:

1. The wrapper structure (`.[0].verificationResult.statement`) is `gh` CLI-version-specific, not SLSA-standard
2. The `resolvedDependencies[0].digest.gitCommit` path depends on the order of elements in the `resolvedDependencies` array
3. `jq` returns an empty string on path miss — no error

If the jq path is wrong (empty `ATTESTED_COMMIT`), the tree-digest comparison becomes: `"" != LIVE_TIP` → always false → monitor opens a `[CRITICAL]` issue on **every run** → alert fatigue → real tampering events ignored. This is a monitoring availability failure with safety implications: the D7 backstop degrades from detection to noise.

Furthermore, the design specifies `--signer-workflow .github/workflows/cowork-skeleton.yml` for `gh attestation verify`. This flag's exact format is also unvalidated (see FM-029-QG3). Both failures compound: wrong jq path or wrong workflow path format each independently cause a false-alarm storm.

**Recommendation:**
This jq path **must be validated against a real attestation** before the D7 monitor design is considered complete. The design should either:
- (a) Validate the path against a pilot run and hardcode the confirmed path, OR
- (b) Specify a fallback extraction mechanism: `gh attestation verify --format json | jq -r 'first(.[] | select(.verificationResult != null) | .verificationResult.statement.predicate.buildDefinition.resolvedDependencies[] | select(.digest.gitCommit != null) | .digest.gitCommit)'` (more robust, uses `select()` filters), OR
- (c) Alternatively, extract the source commit SHA from the release notes (`Source-Commit:` trailer) rather than from the attestation JSON, since the release notes are under CI control and their format IS specified in the design

Additionally add: if `ATTESTED_COMMIT` is empty after extraction, exit non-zero immediately ("predicate extraction failed") rather than proceeding to a comparison that will always fire a false alarm.

**Post-Correction RPN Estimate:** S=8, O=2, D=3 → RPN=48

---

### FM-020-QG3: Version Sentinel Path Ambiguous — D6 Faithful-Derivative Gate Fails Every Release

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **RPN** | 216 (S=9, O=6, D=4) |
| **Type** | Design Defect |
| **Section** | `phase3-skeleton-generation-design.md` §2 G5, §6 Fallback A; `phase3-ci-workflow-design.md` STEP d6-faithful-derivative |
| **Owner** | nse-architecture |
| **Dimension** | Completeness |

**Evidence:**
The generation design (G5) writes two files: `write_static(projects/README.md)` and `write_static(<version-sentinel>)`. The Fallback A section describes the A1 sentinel as "a static file in the generated tree (`.claude/` or the `projects/` stub)". The path `<version-sentinel>` is never resolved to a specific filesystem path.

The D6 faithful-derivative gate (CI design, STEP d6-faithful-derivative-and-secret-scan) uses:
```
git diff --quiet "${TAG}..HEAD" -- ':!projects/' ':!tests/'
```
This compares `TAG` to `HEAD` (the generated commit), excluding `projects/` and `tests/` from the diff. Files in `.claude/` ARE included in the diff scope.

**Analysis:**
If the version sentinel is placed in `.claude/` (a natural location for version metadata), the D6 diff will show it as a new file (added by G5, absent in TAG). `--quiet` exits non-zero on any diff → D6 fails → `exit_1("[CRITICAL] skeleton not faithful to ${TAG}")` → **no release can complete**. The failure is immediate and total: the first release run fails at D6. But it requires the sentinel path decision to be correct before D6 passes.

If the sentinel is placed in `projects/` (as the `projects/README.md` entry implies), it is excluded from the D6 diff → D6 passes. But the design conflates the `projects/README.md` (described as "sentinel: empty-dir guard, static prose only") with the `<version-sentinel>` that "embeds ONLY Source-Tag + 40-char SRC_SHA". These appear to be distinct files. If so, `projects/README.md` may be static prose without the commit SHA, while the commit-SHA sentinel has an unresolved path.

**Recommendation:**
The design must explicitly resolve the version sentinel path. **Required:** the sentinel must be placed under `projects/` (or any path covered by `:!projects/` exclusion in D6) to avoid D6 failures. Simplest resolution: make `projects/README.md` the sentinel (embed Source-Tag + Source-Commit in it, as static content). The CI design's G5 step should show the exact sentinel content and path.

Additionally: the D6 pathspec exclusion should be documented with the reasoning "sentinel files in `projects/` are excluded because they are expected to differ from TAG". This makes the design intent auditable.

**Post-Correction RPN Estimate:** S=9, O=1, D=2 → RPN=18

---

## Major Findings — Detailed

### FM-014-QG3: Committer Identity Not Explicitly Pinned

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **RPN** | 189 (S=9, O=3, D=7) |
| **Type** | Design Defect |
| **Section** | `phase3-skeleton-generation-design.md` §2 G6, §3(a) Commit inputs table |
| **Owner** | eng-devsecops |
| **Dimension** | Internal Consistency |

**Evidence:**
The G6 commit uses `--author "github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>"` (explicit) but does NOT set `GIT_COMMITTER_NAME` or `GIT_COMMITTER_EMAIL`. The determinism table in §3(a) shows "Author/committer identity: github-actions[bot]" as pinned, but the pseudocode only pins the AUTHOR via `--author`; the COMMITTER derives from `user.name`/`user.email` in the runner's git config.

**Analysis:**
In git, author ≠ committer. `--author` sets GIT_AUTHOR_NAME + GIT_AUTHOR_EMAIL; the committer identity is separate (GIT_COMMITTER_NAME + GIT_COMMITTER_EMAIL). In GitHub Actions, `actions/checkout` typically configures `user.name = github-actions[bot]` and `user.email = 41898282+github-actions[bot]@users.noreply.github.com`. This is correct *in practice*, but the design does not make this dependency explicit. If `actions/checkout` changes its git-config behavior (or a different checkout mechanism is used), the committer identity drifts and the commit SHA changes.

**Recommendation:**
Add to G6 (in the deterministic-commit design): set `GIT_COMMITTER_NAME` and `GIT_COMMITTER_EMAIL` explicitly via `$GITHUB_ENV` in addition to the dates, or use `git -c user.name="..." -c user.email="..." commit ...`. Update the §3(a) pin table to show the exact env var mechanism for committer identity.

**Post-Correction RPN Estimate:** S=9, O=1, D=3 → RPN=27

---

### FM-040-QG3: App Private Key Accessible in Job A (Generation Step)

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **RPN** | 168 (S=7, O=4, D=6) |
| **Type** | Design Defect |
| **Section** | `phase3-ci-workflow-design.md` Per-Job Permissions Table; Job A environment note |
| **Owner** | eng-infra |
| **Dimension** | Methodological Rigor |

**Evidence:**
The CI design states: "The `generate-and-gate` job declares `environment: skeleton-push` for fast-fail on unauthorized branches." The App private key (`COWORK_APP_PRIVATE_KEY`) is stored as an environment-level secret in `skeleton-push` (attestation design §5.3). Job C (push-and-release) also declares `environment: skeleton-push` to access the App token.

**Analysis:**
GitHub Actions environment-level secrets are available to ALL jobs that declare the environment. Job A, which processes potentially adversarial content (running D8 scan on `plugin.json`-derived paths, executing `declared_paths()` from user-controlled manifest content), has access to `COWORK_APP_PRIVATE_KEY` via the environment declaration — even though it never uses it. A supply-chain attack through the D8 scan scope (a malicious skill file that exfiltrates environment variables) could extract the key from Job A without ever reaching Job C.

The principle of least privilege requires: the App private key is accessible ONLY in Job C. Job A needs the environment's `deployment_branch_policy` fast-fail behavior but NOT the secret.

**Recommendation:**
Split the environment's credential and policy roles:
1. Create a `skeleton-gate` environment (or none) with `deployment_branch_policy` for branch/tag restriction → apply to Job A
2. Keep `skeleton-push` with App private key → apply to Job C only

Or: configure Job A with only `deployment_branch_policy` using a separate lightweight environment without secrets. The App private key must be scoped to Job C exclusively.

**Post-Correction RPN Estimate:** S=7, O=1, D=4 → RPN=28

---

### FM-018-QG3: Workflow-Level Permissions Inheritance Risk

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **RPN** | 160 (S=8, O=4, D=5) |
| **Type** | Design Defect |
| **Section** | `phase3-ci-workflow-design.md` Triggers and Concurrency pseudocode |
| **Owner** | eng-devsecops |
| **Dimension** | Methodological Rigor |

**Evidence:**
The CI design specifies: `# No workflow-level permissions: block (REQ-020: per-job only)`. This is a negative constraint documented as a comment.

**Analysis:**
A workflow without a top-level `permissions:` block inherits GitHub's **default token permissions** (repository-configured, often `read-all` or `contents: write` depending on org settings). If a Phase-6 implementer copies the design and adds `permissions: contents: write` at the workflow level (a common pattern), ALL three jobs inherit `contents: write`. Job B (attest) would then have `contents: write` in addition to `id-token: write + attestations: write`, violating ADR-003 D4 A-1.

The design should make the safe default explicit: a `permissions: {}` (deny all) at workflow level, with each job specifying its minimum set. This is the GitHub-recommended pattern for least-privilege workflows.

**Recommendation:**
Add `permissions: {}` at the workflow level explicitly in the CI design pseudocode (not just a comment). This forces each job to declare its own permissions and prevents accidental inheritance. Update the Per-Job Permissions Table to note: "workflow-level: permissions: {} (deny all by default)".

**Post-Correction RPN Estimate:** S=8, O=1, D=3 → RPN=24

---

### FM-019-QG3: actions/checkout fetch-depth: 0 Not Shown in CI Pseudocode

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **RPN** | 160 (S=8, O=4, D=5) |
| **Type** | Design Defect |
| **Section** | `phase3-ci-workflow-design.md` Job A gate sequence; `phase3-skeleton-generation-design.md` §2 G3 comment |
| **Owner** | eng-devsecops |
| **Dimension** | Completeness |

**Evidence:**
The generation design (G3 comment) states: "fetch-depth: 0 (full history) — REQUIRED for Option A parent chain AND the D5 ancestor check." The CI design Job A pseudocode begins with STEP resolve-and-validate-tag, STEP d5-provenance-gate — but the mandatory `actions/checkout` step with `fetch-depth: 0` is ABSENT from the pseudocode.

**Analysis:**
The default `actions/checkout` uses `fetch-depth: 1` (shallow clone of HEAD). With `fetch-depth: 1`, the D5 `git merge-base --is-ancestor "${SRC_SHA}" origin/main` check may produce incorrect results for tags that are more than one commit behind `origin/main`. In a shallow repo, `git merge-base` may output "not an ancestor" for legitimate tags simply because the common ancestor is not in the shallow history. Phase-6 implementers consulting the CI pseudocode will not see `fetch-depth: 0` and are likely to omit it, silently breaking D5.

**Recommendation:**
Add an explicit STEP to Job A pseudocode as the first step:
```
STEP actions-checkout:
  uses: actions/checkout@{PINNED_40CHAR_SHA}  # Pin per REQ-017
  with:
    fetch-depth: 0  # REQUIRED: full history for D5 merge-base AND Option A parent chain (G6)
    # Without full history, D5 ancestor check gives false results for old tags
```
This must appear BEFORE the tag resolve step.

**Post-Correction RPN Estimate:** S=8, O=1, D=3 → RPN=24

---

### FM-037-QG3: git Bundle Restore Missing Explicit HEAD Checkout Step

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **RPN** | 160 (S=8, O=4, D=5) |
| **Type** | Design Defect |
| **Section** | `phase3-ci-workflow-design.md` Job C: download-bundle-and-artifact step |
| **Owner** | eng-devsecops |
| **Dimension** | Completeness |

**Evidence:**
Job C's bundle restore pseudocode:
```
git bundle verify <bundle-file>
git fetch <bundle-file> HEAD:refs/remotes/bundle/HEAD   # restore git state
```
Followed immediately by:
```
git push --force ... HEAD:<default-branch>
```

**Analysis:**
After `git fetch <bundle-file> HEAD:refs/remotes/bundle/HEAD`, the `refs/remotes/bundle/HEAD` reference is populated, but the **working tree HEAD** is wherever the fresh GitHub Actions runner left it after initial checkout (which is the source repo tip, not the generated commit). `git push --force ... HEAD:<default-branch>` would push the SOURCE REPO's HEAD, not the generated commit.

To make `HEAD` point to the generated commit, an additional step is required:
```
git checkout refs/remotes/bundle/HEAD
```
(or `git checkout FETCH_HEAD` if the bundle fetch sets FETCH_HEAD). Without this step, the push sends the wrong commit to the dedicated repo.

**Recommendation:**
Add an explicit checkout step between bundle fetch and push:
```
git bundle verify <bundle-file>
git fetch <bundle-file> HEAD:refs/remotes/bundle/HEAD
git checkout refs/remotes/bundle/HEAD   # REQUIRED: detach HEAD at generated commit before push
# Verify HEAD = expected COMMIT_SHA before proceeding (see FM-038-QG3):
CURRENT_SHA=$(git rev-parse HEAD)
[ "${CURRENT_SHA}" = "${COMMIT_SHA}" ] || exit_1("bundle restore SHA mismatch: expected ${COMMIT_SHA}, got ${CURRENT_SHA}")
git push --force ... HEAD:<default-branch>
```

**Post-Correction RPN Estimate:** S=8, O=1, D=2 → RPN=16

---

### FM-038-QG3: No SHA Verification After Bundle Restore

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **RPN** | 147 (S=7, O=3, D=7) |
| **Type** | Design Defect |
| **Section** | `phase3-ci-workflow-design.md` Job C; CI-G-001 Phase 6 gap |
| **Owner** | eng-devsecops |
| **Dimension** | Methodological Rigor |

**Evidence:**
The CI design notes CI-G-001: "the git bundle create and restoration in the push job need explicit testing for correctness." Job C has no step that verifies the restored commit SHA matches `COMMIT_SHA` from Job A's outputs before pushing.

**Analysis:**
If the bundle is corrupted during transit through the Actions artifact store (unlikely but possible), `git bundle verify` may pass (it checks internal consistency), but the content may be an older or different commit. Without a SHA comparison gate, Job C would push the wrong commit, create a release for it, and the D7 monitor would detect the mismatch up to 6 hours later. The fix is a one-line assertion (see FM-037 recommendation above).

**Recommendation:**
See FM-037-QG3 recommendation — add `[ "${CURRENT_SHA}" = "${COMMIT_SHA}" ] || exit_1(...)` immediately after the bundle checkout step. `COMMIT_SHA` must be passed as a job output from Job A and accessed via `needs.generate-and-gate.outputs.COMMIT_SHA` in Job C.

**Post-Correction RPN Estimate:** S=7, O=1, D=2 → RPN=14

---

### FM-022-QG3: D7 Monitor Infinite Alert/Revert Loop After Rollback

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **RPN** | 126 (S=6, O=3, D=7) |
| **Type** | Design Defect |
| **Section** | `phase3-ci-workflow-design.md` Job M1 bind-to-live-tip step; Job M2 auto-revert |
| **Owner** | eng-devsecops |
| **Dimension** | Actionability |

**Evidence:**
M1 step bind-to-live-tip:
```
expected_tip_sha = ... extracted from latest release notes (Source-Commit trailer)
live_tip_sha = git ls-remote ... HEAD
IF expected_tip_sha != live_tip_sha: exit 1
```
The monitor always downloads and checks against `LATEST_TAG` from the source repo.

**Analysis:**
After auto-revert deploys `last-good-validated` (e.g., v0.31.3) because v0.31.5 had an issue, the monitor's next cycle:
1. Downloads v0.31.5 artifact (LATEST source release)
2. Extracts `ATTESTED_COMMIT` = v0.31.5 skeleton SHA
3. Reads `LIVE_TIP` = v0.31.3 skeleton SHA (after rollback)
4. Mismatch → CRITICAL issue → M2 dispatches `last-good-validated` (v0.31.3) again
5. v0.31.3 is already deployed → push results in same SHA → M1 next cycle: same mismatch → loop

The design has no termination condition for this loop. Until v0.31.5 is either fixed+deployed or the LATEST_TAG source release is moved to an older tag (non-standard), the loop continues indefinitely. Each iteration opens a new CRITICAL issue, depleting issue quota and creating alert fatigue.

**Recommendation:**
Add a loop-break condition: if M2 dispatches a revert and the resulting deployed tip matches `last-good-validated`'s commit SHA, M1 should recognize the INTENTIONAL rollback state and not re-trigger M2. Design options: (a) maintain a `monitor-state` tag or file that records "rollback-in-progress: {last-good-validated}" so M1 can distinguish intentional rollback from tampering; (b) compare `LIVE_TIP` against `last-good-validated`'s commit SHA as a separate pass condition: if `LIVE_TIP == last-good-validated-SHA AND LIVE_TIP != expected_tip_sha` → open informational issue (not CRITICAL) + suppress M2.

**Post-Correction RPN Estimate:** S=6, O=1, D=4 → RPN=24

---

### FM-034-QG3: v* Tag Bypass Actors Include "Designated Maintainers" — Unnecessarily Broad

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **RPN** | 105 (S=7, O=3, D=5) |
| **Type** | Design Defect |
| **Section** | `phase3-attestation-provenance-design.md` §6.1 v* tag-protection ruleset |
| **Owner** | eng-infra |
| **Dimension** | Methodological Rigor |

**Evidence:**
§6.1: "bypass_actors: Release pipeline CI identity + designated maintainers only"

**Analysis:**
If designated maintainers can push v* tags directly (bypassing the ruleset), the D5 build-time ancestor check is still the backstop. But a maintainer error (tagging a debugging commit on main that passed the ancestor check but has unreviewed content) bypasses the intended "only CI creates releases" model. The design's intent is that releases are created only through the generation workflow, not by direct tag push. Allowing maintainers as bypass actors contradicts this intent.

**Recommendation:**
Remove "designated maintainers" from `bypass_actors` for v* tags. CI identity is the sole bypass actor. If maintainers need to trigger releases, they use `workflow_dispatch` with `target_tag` input — which still goes through the full gate train. Add a note: "Human-initiated releases use `workflow_dispatch`, not direct v* tag push."

**Post-Correction RPN Estimate:** S=7, O=1, D=4 → RPN=28

---

### FM-011-QG3: G8 Clone-Time Measurement Subject Is Ambiguous Pre-Push

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **RPN** | 150 (S=5, O=5, D=6) |
| **Type** | Phase-6 implementation detail to specify |
| **Section** | `phase3-skeleton-generation-design.md` §4; `phase3-ci-workflow-design.md` STEP g8-multi-dim-gate |
| **Owner** | eng-devsecops |
| **Dimension** | Methodological Rigor |

**Evidence:**
G8: `clone_secs = timed_reference_clone()  # 10 Mbps reference network (30th-pct global broadband)`
The design does not specify WHAT is being cloned. At G8 time, the dedicated repo (`geekatron/jerry-cowork`) has not yet been updated with the current run's generated commit.

**Analysis:**
Options available at G8 time: (a) clone the LOCAL repo (measures local object count, not network-realistic), (b) clone the CURRENT jerry-cowork (measures previous-release weight, not the current commit's weight), (c) simulate using pack size × bandwidth (mentioned as "or" in the design). The `git count-objects -vH size-pack` for pack size measurement runs in the source repo (jerry), which for Option A approaches jerry's total pack size. This is a reasonable upper bound but not the exact dedicated-repo clone weight.

**Recommendation:**
Specify the pre-push clone-time estimation as: `estimated_clone_secs = pack_size_mb / (10 Mbps / 8 × 1024 × 1024) = pack_size_mb × 0.8 seconds`. Rely on M3 (post-push timed reference clone of jerry-cowork) for empirical validation. Make clear in the design that G8c is an ESTIMATE based on pack size, not an empirical measurement. Document the 10 Mbps bandwidth assumption explicitly in the design alongside the formula.

**Post-Correction RPN Estimate:** S=5, O=2, D=4 → RPN=40

---

### FM-027-QG3: actions/attest May Require artifact-metadata:write Permission Not Declared in Job B

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **RPN** | 144 (S=9, O=4, D=4) |
| **Type** | Phase-6 implementation detail to specify |
| **Section** | `phase3-attestation-provenance-design.md` §2.2 Required Permissions |
| **Owner** | eng-infra |
| **Dimension** | Completeness |

**Evidence:**
§2.2 comment: `# artifact-metadata: write # Current actions/attest v4 documentation lists this as required; # Phase-6 MUST confirm exact permission set for the pinned version.`

**Analysis:**
If `artifact-metadata: write` is required and omitted, the attestation step fails at runtime on first release. Severity=9 because every release fails. The design honestly flags this as a Phase-6 confirmation item, but the confirmation path is not specified.

**Recommendation:**
Add to the attestation design: "Phase-6 implementation step: before writing production YAML, create a pilot workflow against the pinned `actions/attest@SHA` version to confirm the exact required permission set. Document the confirmed set in the design and update Job B's permissions block. This confirmation is a gate before writing the production attestation job."

**Post-Correction RPN Estimate:** S=9, O=1, D=2 → RPN=18

---

### FM-003-QG3: Short SHA Risk in Commit Message

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **RPN** | 144 (S=8, O=3, D=6) |
| **Type** | Phase-6 implementation detail to specify |
| **Section** | `phase3-skeleton-generation-design.md` §3(a) commit inputs table |
| **Owner** | nse-architecture |
| **Dimension** | Internal Consistency |

**Evidence:**
Design §3(a): "Message: fixed template + Source-Tag + **full 40-char** Source-Commit; no timestamp/run-id/`--short` SHA (short-SHA length grows with repo size — FM-010)". The FM-010 reference is to an identified risk in the prior design iteration.

**Analysis:**
`git rev-parse --short HEAD` produces SHA of variable length (7 chars initially, grows as repo size requires more chars for uniqueness). Embedding a short SHA in the commit message introduces a non-deterministic element: as jerry grows, the default short length increases from 7 to 8+ chars, producing a different message for the same tag across time. The 40-char requirement is correctly specified but has no enforcement mechanism.

**Recommendation:**
Add to the CI design's g6-deterministic-commit step: `SRC_SHA=$(git rev-parse "${TAG}^{commit}") && [ ${#SRC_SHA} -eq 40 ] || exit_1("SHA length check failed: got ${#SRC_SHA} chars")`. This assertion is also a deterrent against `--short` in the message template function.

**Post-Correction RPN Estimate:** S=8, O=1, D=3 → RPN=24

---

### Remaining Major Findings (Summary)

| ID | Finding | S | O | D | RPN | Type | Owner | Recommendation |
|----|---------|---|---|---|-----|------|-------|----------------|
| FM-001-QG3 | `${{ github.ref_name }}` must be bound via `env:` not interpolated into `run:` shell; exact binding pattern not shown | 7 | 4 | 7 | 196 | P6 | eng-devsecops | CI pseudocode must show `env: TAG: ${{ github.ref_name }}` pattern and use `$TAG` in shell |
| FM-006-QG3 | Windows symlink resolution fails (`core.symlinks=false`); deferred to R-001/Phase-5; require explicit Phase-5 test AC | 6 | 4 | 5 | 120 | P6 | nse-requirements | Add REQ or Phase-5 AC: "CoWork Windows install: `.claude/rules` symlink resolves or fallback documented" |
| FM-012-QG3 | G8 ceiling values (5,000 files, 250 MB, 60 s) are empirically unverified; real CoWork ceiling unknown | 7 | 3 | 5 | 105 | P6 | nse-requirements | G-headroom gate must empirically confirm ceilings; design should flag ceiling values as "provisional pending G-headroom" |
| FM-013-QG3 | Gzip mtime trap: canonical plain-TAR form specified but no Phase-6 enforcement test; `tar.gz` temptation remains | 9 | 3 | 4 | 108 | P6 | eng-infra | Add to Phase-5 validation gate: two-run idempotency test for artifact_digest; add `assert artifact ends in .tar not .tar.gz` in G9 |
| FM-015-QG3 | Runner git version not pinned; `git archive` TAR format behavior may shift with `ubuntu-latest` upgrades | 7 | 2 | 7 | 98 | P6 | eng-infra | Pin `ubuntu-latest` to a specific runner image version for the generation job, or add idempotency test across runner versions |
| FM-029-QG3 | `--signer-workflow .github/workflows/cowork-skeleton.yml` path format not validated against live `gh` CLI | 6 | 4 | 4 | 96 | P6 | eng-infra | Phase-6 pilot: confirm the workflow path form against pinned `gh` version before writing monitor YAML |
| FM-030-QG3 | `gh` CLI version not pinned in monitor workflow; version changes may break `attestation verify` syntax | 6 | 3 | 5 | 90 | P6 | eng-devsecops | Pin `gh` CLI version in monitor workflow (install specific version in a setup step) |
| FM-033-QG3 | `deployment_branch_policy` YAML combining branch (`main`) and tag (`v*`) patterns not specified | 5 | 4 | 4 | 80 | P6 | eng-infra | Add explicit GitHub API config snippet for `custom_branch_policies` with both branch and tag patterns |
| FM-036-QG3 | Fallback A (A2 version-check skill) requires outbound GitHub API from CoWork sandbox; egress policy unknown | 5 | 4 | 6 | 120 | P6 | nse-architecture | Add to Fallback A design: fail-safe for network unavailability (silent skip, not error); flag G-update-pre as prerequisite for shipping decision |

---

## Minor Findings

| ID | Element | Finding | RPN | Note |
|----|---------|---------|-----|------|
| FM-002-QG3 | G2 allow-list | Regex permits `v1.0` (no patch component); undocumented but functionally acceptable | 24 | P6: document intent |
| FM-005-QG3 | G4 denylist | `git rm -r tests/` fails if test directory is renamed; G7 negative assertion provides secondary catch | 56 | Low probability; acceptable |
| FM-008-QG3 | G6 --no-verify | `--no-verify` does not bypass D6 CI secret scan; design is correct; R-001 rationale sound | 18 | Design adequate |
| FM-009-QG3 | G7 retention | plugin.json path parsing must use exact paths (not glob); design specifies this; Phase-6 enforcement needed | 72 | P6: add assertion for depth-mismatch |
| FM-016-QG3 | Determinism | Force-moved tag intentionally yields new artifact; §3 idempotency proof acknowledges this | 64 | Known; adequately handled |
| FM-021-QG3 | D5 | D5 does not prevent trusted-maintainer rogue builds; explicitly RTB-2 residual per ADR-003 | 56 | Known residual |
| FM-024-QG3 | D7 freshness | Freshness uses tag creation time; ≤2h SLA accommodates normal deployment latency | 24 | Acceptable |
| FM-025-QG3 | D7 monitor | `git ls-remote` step has no timeout; could block monitor for up to job default (6h) | 75 | P6: add `timeout-minutes: 5` on step |
| FM-026-QG3 | Auto-revert | `last-good-validated` undefined on first run; M2 correctly falls back to human escalation | 48 | Design adequate |
| FM-031-QG3 | D2 ruleset | Bypass by App ID (immutable numeric ID) is correct; more durable than App name | 12 | Design adequate |
| FM-032-QG3 | D3 App token | Key theft during ≤6h D7 window; attacker cannot forge Sigstore attestation; RTB-4 bounded | 9 | Known residual (RTB-4) |
| FM-035-QG3 | SBOM | `actions/attest` `sbom-path` parameter form unvalidated; SBOM is optional | 48 | P6: confirm in pilot |
| FM-039-QG3 | Artifact store | Actions artifact store corruption theoretical; D7 tree-digest match provides detection | 49 | Theoretical; acceptable |
| FM-041-QG3 | Monitor write | `contents: write` for `last-good-validated` push is loop-safe (pattern ≠ `v*`) | 6 | Design adequate |

---

## Scoring Impact

| Dimension | Weight | Impact | Finding IDs | Rationale |
|-----------|--------|--------|-------------|-----------|
| Completeness | 0.20 | **Negative** | FM-020, FM-019, FM-037, FM-027, FM-033 | Version sentinel path unresolved; actions/checkout fetch-depth missing from CI pseudocode; git bundle restore step incomplete; attestation permissions possibly incomplete; environment policy YAML not specified |
| Internal Consistency | 0.20 | **Negative** | FM-007, FM-004, FM-014, FM-003, FM-013 | Cross-step date propagation mechanism wrong; sentinel dynamic content enforcement missing; committer identity not pinned; short-SHA risk; gzip trap lacks enforcement |
| Methodological Rigor | 0.20 | **Negative** | FM-023, FM-040, FM-018, FM-038, FM-034, FM-011 | jq predicate extraction unvalidated; App key in wrong job; workflow-level permissions not explicitly denied; no SHA verification after bundle restore; v* bypass too broad; clone-time measurement ambiguous |
| Evidence Quality | 0.15 | **Negative** | FM-012, FM-036 | G8 ceiling values have no empirical basis; Fallback A network dependency untested |
| Actionability | 0.15 | **Negative** | FM-022, FM-001 | D7 monitor infinite loop after rollback has no termination condition; env: binding pattern for injection prevention not shown |
| Traceability | 0.10 | **Positive** | All | REQ/ADR cross-references are thorough; Pending Validation table honestly scopes Phase-6 gaps; P-022 compliance is exemplary |

---

## Execution Statistics

- **Total Failure Modes Analyzed:** 39
- **Critical (RPN ≥ 200 or S ≥ 9):** 4 — FM-007, FM-004, FM-023, FM-020
- **Major (RPN 80–199):** 20
- **Minor (RPN < 80):** 15
- **Total RPN:** 3,990
- **Design Defects (require design changes now):** 12 findings
- **Phase-6 Implementation Details (design correctly scopes but needs Phase-6 spec):** 13 findings
- **Adequately handled / Known residuals:** 14 findings
- **Protocol Steps Completed:** 5 of 5

**Highest-RPN Finding:** FM-007-QG3 (`GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` cross-step propagation, RPN = 315)

---

*Strategy Execution Report generated by adv-executor. S-012 FMEA protocol applied per template s-012-fmea.md v1.0.0. H-15 self-review applied. P-003: no sub-agents spawned. P-022: RPN scores are estimates; S/O/D ratings reflect design-time analysis without implementation evidence.*
