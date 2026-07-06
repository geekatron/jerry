# Quality Score Report: PROJ-031 Phase-3 Design — QG-3 Iteration 2

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, one-line assessment |
| [Scoring Context](#scoring-context) | Deliverable and strategy metadata |
| [Score Summary](#score-summary) | Composite and threshold |
| [Dimension Scores](#dimension-scores) | Weighted table |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence and gaps |
| [Critical Findings Closure Table](#critical-findings-closure-table) | 12/12 Criticals status |
| [Remaining Open Design Defects](#remaining-open-design-defects) | Post-remediation residuals |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered actions |
| [Leniency Bias Check](#leniency-bias-check) | Anti-leniency verification |
| [Session Context Handoff](#session-context-handoff) | Orchestrator YAML schema |

---

## L0 Executive Summary

**Score:** 0.820/1.00 | **Verdict:** REVISE | **Weakest Dimensions:** Completeness + Methodological Rigor (both 0.80)

**One-line assessment:** 12/12 Criticals are closed; two open Major design defects (FM-004-i2 circuit-breaker bypass, FM-005-i2 monitor concurrency race) prevent the design from reaching its honest ceiling of ~0.86 — fix those two items and proceed to Phase 4.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/` (three Phase-3 design documents)
  - `phase3-skeleton-generation-design.md` (FAD-PROJ031-3A-001)
  - `phase3-ci-workflow-design.md` (FAD-PROJ031-3B-001)
  - `phase3-attestation-provenance-design.md` (FAD-PROJ031-3B-001 Infra)
- **Deliverable Type:** Design
- **Criticality Level:** C4 (AE-002: `.github/` changes; AE-005: security-relevant supply-chain)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Strategy Findings Incorporated:** Yes — 4 files
  - `qg3-review/s-004-pre-mortem-findings.md` (iter-1: 4 Criticals, 6 Majors)
  - `qg3-review/s-012-fmea-findings.md` (iter-1: 4 Criticals, 9 Defects)
  - `qg3-review/s-002-devils-advocate-findings.md` (iter-1: 1 Critical, 2 Majors)
  - `qg3-review/s-012-fmea-iter2-findings.md` (iter-2: 3 Criticals, 2 Majors)
- **Prior Score (iter-1):** 0.702 (REVISE)
- **Scored:** 2026-06-28T00:00:00Z
- **Calibration note:** Design-phase ceiling for a supply-chain security design of this complexity is approximately 0.86. Deferred Phase-6 items (CI-G-007 byte-idempotency, D8 catalog content, CI-G-005 `contents:write` YAML declaration) are NOT penalised. Still-open design-level contradictions and unexplained implementation gaps ARE penalised.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.820 |
| **Prior Score (iter-1)** | 0.702 |
| **Delta** | +0.118 |
| **Threshold (H-13)** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — 4 reports, 12 Critical findings |
| **Critical Findings Closed** | 12/12 |
| **Open Major Defects** | 2 (FM-004-i2, FM-005-i2) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.80 | 0.160 | G1-G9 and 8-step monitor fully specified; FM-004-i2 and FM-005-i2 not addressed |
| Internal Consistency | 0.20 | 0.82 | 0.164 | ROOT-1 fix consistent across all 3 docs; minor SBOM placement ambiguity |
| Methodological Rigor | 0.20 | 0.80 | 0.160 | FMEA-driven corrections rigorous; FM-004-i2 bypass path and FM-005-i2 race unmitigated |
| Evidence Quality | 0.15 | 0.84 | 0.126 | All decisions cite ADR/REQ/RPN; MAX_AUTO_REVERTS=3 basis not explained |
| Actionability | 0.15 | 0.83 | 0.1245 | Pseudocode directly implementable; FM-004/005 leave implementable gap |
| Traceability | 0.10 | 0.86 | 0.086 | 30-row Traceability Matrix complete; FM-005-i2 concurrency not traced |
| **TOTAL** | **1.00** | | **0.820** | |

**Composite calculation:**
(0.80 × 0.20) + (0.82 × 0.20) + (0.80 × 0.20) + (0.84 × 0.15) + (0.83 × 0.15) + (0.86 × 0.10)
= 0.160 + 0.164 + 0.160 + 0.126 + 0.1245 + 0.086
= **0.8205 → 0.820**

---

## Detailed Dimension Analysis

### Completeness (0.80/1.00)

**Evidence for score:**
- G1-G9 generation algorithm is fully pseudocoded in `phase3-skeleton-generation-design.md` with determinism contract tables, multi-dim gate specification (file-count/pack-size/clone-time), and G7 retention completeness check.
- Three-job CI topology (generate-and-gate / attest / push-and-release) is fully specified in `phase3-ci-workflow-design.md` with explicit permission scoping per job.
- 8-step D7 digest monitor is fully specified with fail-closed failure modes per step (mirrored from attestation design §3.3 MONITOR HAND-OFF).
- Auto-revert circuit breaker is specified with MAX_AUTO_REVERTS=3, label format `auto-revert:${LATEST_SRC_TAG}`, and cap-exceeded path.
- Phase-6 gap table (CI-G-001 through CI-G-007) explicitly enumerates implementation residuals.
- All 12 Critical findings from iter-1 and iter-2 are addressed in the design text.

**Gaps preventing 0.85+:**
- **FM-004-i2 (OPEN, Major):** The circuit breaker uses `count_open_issues(label="auto-revert:${LATEST_SRC_TAG}")`. The iter-2 FMEA (RPN=180) identified that a maintainer who manually closes the GitHub issues can reset the counter below the cap, allowing unlimited auto-reverts. The design does not require `count_all_issues` (open + closed) nor does it propose an alternative (e.g., immutable tag counter). One sentence in the circuit-breaker pseudocode would close this.
- **FM-005-i2 (OPEN, Major):** The `cowork-monitor.yml` trigger section has no `concurrency: group: cowork-monitor` declaration. Two concurrent monitor runs (e.g., a manual `workflow_dispatch` overlapping the 6h schedule) can simultaneously increment the label counter, each seeing count < 3 before the first has finished writing, allowing more than MAX_AUTO_REVERTS=3 auto-reverts to be dispatched. The Traceability Matrix row `Concurrency group, cancel-in-progress: false | REQ-015` applies to `cowork-skeleton.yml` only; the monitor is unprotected.
- **PM-008-Q3 (OPEN, Major):** The attestation design continues to show SBOM generation (`uv run cyclonedx-py environment`) in the attestation job. This is not explicitly reconciled in the CI workflow design pseudocode. The SBOM should be generated before attestation (in the generation job where the environment is known), not in the attestation job.

**Improvement path:**
Add two sentences to the CI workflow design: (1) in the circuit-breaker pseudocode, replace `count_open_issues` with `count_all_issues(label=...)` or equivalent immutable counter; (2) add `concurrency: group: cowork-monitor, cancel-in-progress: false` to the monitor workflow-level block. Clarify SBOM job placement in attestation design §2 and CI design attest-job pseudocode.

---

### Internal Consistency (0.82/1.00)

**Evidence for score:**
- **ROOT-1 consistency (strong):** The 8-step digest-based monitor (ATTESTED_DIGEST == LIVE_DIGEST) is consistently described in `phase3-ci-workflow-design.md` §M1 and `phase3-attestation-provenance-design.md` §3.3 MONITOR HAND-OFF. The SLSA predicate gitCommit field removal is consistent across both documents — neither document has jq parsing of release bodies or SLSA predicate extraction.
- **ROOT-2 consistency (strong):** The $GITHUB_ENV / same-step inline constraint appears consistently in the generation design G6 pseudocode, the Traceability Matrix row (`G6 deterministic commit (pinned dates via same-step inline OR $GITHUB_ENV — ROOT-2 / FM-007-QG3)`), and in the Pending Validation section.
- **ROOT-3 consistency (strong):** `projects/.jerry-skeleton-version` is the sentinel path in the generation design G5, the D6 `:!projects/` exclusion coverage note in the Traceability Matrix (`D6 ':!projects/' covers BOTH known-injected members`), and the G7 assertion (`git ls-files projects/ == {README.md, .jerry-skeleton-version}`).
- **FM-003-i2 consistency (strong):** The LGV_SKIP invariant is consistently stated in the m1-8 step (sets LGV_SKIP=true in suppression path) and the advance-last-good-validated step (`IF LGV_SKIP: emit_to_GITHUB_STEP_SUMMARY(...)   ELSE: git tag -f last-good-validated ${deployed_release_version}`). The Traceability Matrix row cites both FM-003-i2 and the deployed_release_version variable correctly.
- **FM-001-i2 consistency (strong):** The `publishedAt` priority / `git log` fallback / null-guard / `.committer.date` FORBIDDEN pattern appears in the CI workflow pseudocode, the Traceability Matrix row, and the Pending Validation acceptance criteria.

**Gaps preventing 0.85+:**
- **SBOM placement ambiguity (minor inconsistency):** `phase3-attestation-provenance-design.md` describes SBOM generation (`uv run cyclonedx-py environment`) as occurring in the attestation job. The CI workflow design's attestation-job pseudocode shows `gh attestation attest <file>` but does not include SBOM generation steps. A Phase-6 implementer reading both documents receives conflicting signals: the SBOM happens in the attestation job (per infra design) but is absent from the attestation-job pseudocode (per CI design).
- **FM-018-QG3 (minor):** Workflow-level permissions scoping for `cowork-monitor.yml` is not specified. The per-job permissions isolation is specified for `cowork-skeleton.yml` (three jobs), but the monitor workflow's workflow-level permissions default (which could be broader than necessary) is not explicitly constrained.

**Improvement path:**
Add a SBOM step to the attestation-job pseudocode in the CI workflow design and align with the attestation design §2 scope. Add a workflow-level `permissions: {}` block to the monitor workflow block with per-job overrides.

---

### Methodological Rigor (0.80/1.00)

**Evidence for score:**
- **P-222 Claim-Status Convention (strong):** All operational claims in all three documents are tagged "Designed — operational validation pending [Gate-Name]". The Pending Validation section in the CI workflow design enumerates 12 items with explicit validation gates. No designed-but-unvalidated claim is presented as an achieved fact.
- **FMEA-driven design (strong):** The iter-1 FMEA (4 Criticals, RPN 315/252/240/216) and iter-2 FMEA (3 Criticals, RPN 343/336/280) drove specific design corrections. Each RPN is cited in the Traceability Matrix row for its mitigation. This is proper FMEA use — not post-hoc documentation but design driver.
- **Trust model explicit (strong):** The CI workflow L2 §2 states the monitor shares its trust root with the generation pipeline, explicitly identifies the external Sigstore transparency log as the only out-of-trust-root reference, and explains why a compromised monitor cannot forge a passing attestation (cannot forge Sigstore log entry).
- **SLSA Level 3 trajectory justified (strong):** L2 §3 identifies the specific controls that constitute the trajectory (per-job permission isolation, Sigstore-backed provenance, immutable release publishing) and identifies the RTB-5 gap (no install-time verification) closing condition.
- **Determinism contract structured (strong):** §3 of the generation design specifies invariants as a table (commit inputs, tree inputs, artifact inputs) with explicit fail conditions. The proof that two runs produce identical output is reproducible from the design text.

**Gaps preventing 0.85+:**
- **FM-004-i2 (OPEN, Major):** The revert-cap methodology uses `count_open_issues` which has a documented bypass: a maintainer who closes issues can reset the counter. A rigorous circuit-breaker implementation must use a monotonic counter (count_all_issues, or a dedicated incrementing tag, or a GitHub Environments counter). The design does not acknowledge this bypass path or justify the open-only count.
- **FM-005-i2 (OPEN, Major):** The monitor workflow has no concurrency group. Two concurrent runs can race to read the label count, both find count < MAX_AUTO_REVERTS=3, and both dispatch a revert, resulting in count effective > 3. The design methodology for the revert cap does not include concurrency isolation — a necessary component for correctness.
- **MAX_AUTO_REVERTS=3 basis unexplained:** The value 3 is asserted but not justified. Why not 1 (immediate halt) or 5 (more retries)? A brief rationale (e.g., "3 provides two automatic recovery attempts from transient failures before requiring human investigation") would strengthen methodological rigour.

**Improvement path:**
Change `count_open_issues` to `count_all_issues(label="auto-revert:${LATEST_SRC_TAG}")` in the circuit-breaker step. Add monitor workflow concurrency group. Add a one-sentence justification for MAX_AUTO_REVERTS=3 in the circuit-breaker specification.

---

### Evidence Quality (0.84/1.00)

**Evidence for score:**
- **REQ/ADR citation density (strong):** The 30-row Traceability Matrix links every design element to at least one REQ-NNN and one ADR-NNN reference. The generation design G8 gate specifies the exact REQ references (REQ-006, REQ-034d, REQ-050). The monitor design references REQ-049 for the freshness SLA and REQ-053 for the revert requirement.
- **FMEA RPN evidence (strong):** Every Critical finding cite is accompanied by its RPN score (e.g., FM-001-i2 RPN=343, FM-002-i2 RPN=336) in the Traceability Matrix. This provides quantitative basis for the remediation priority.
- **Sigstore rationale cited (strong):** The attestation design §3.1 explains why the file-subject attestation (`gh attestation attest <file>`) is preferred over bare-SHA attestation (CV-005 compliance). The external Rekor log's immutability property is correctly cited as the integrity anchor.
- **Gzip-mtime trap documented (strong):** The design explicitly names the `gzip-mtime trap` as the reason for using `--format=tar` without compression, and documents the `gzip -n` alternative. This is checkable evidence for a Phase-6 implementer.
- **ROOT-1 correction evidence (strong):** The design explicitly states "SLSA predicate gitCommit removal" and explains why SRC_SHA ≠ G6_SHA always by design (source trigger SHA vs generated skeleton commit SHA are different objects), citing DA-001 and ROOT-1.

**Gaps preventing 0.88+:**
- **MAX_AUTO_REVERTS=3 basis:** The value 3 is asserted without citing quantitative analysis or operational experience. No evidence is presented for why 3 is the correct cap value.
- **Freshness SLA basis:** The ≤2h freshness requirement (REQ-049) is cited but the basis for "2 hours" is not explained. This would be in the requirements document, but the design does not reference the rationale.
- **FM-040-QG3 residual:** The FMEA iter-1 identified that the ephemeral App private key (used for cross-repo push) is accessible in Job A's environment if the App token is minted at the workflow level. The design specifies the App token mint in Job C (dedicated-repo only), which is the correct mitigation. However, the design does not explicitly state that the App private key is NOT available in Job A's environment — leaving a gap for a Phase-6 implementer to accidentally scope it too broadly.

**Improvement path:**
Add a one-sentence rationale for MAX_AUTO_REVERTS=3. Add an explicit note in the Job A pseudocode block that the App private key is ONLY minted in Job C (referencing FM-040-QG3).

---

### Actionability (0.83/1.00)

**Evidence for score:**
- **G1-G9 pseudocode directly implementable (strong):** Each generation step is specified as pseudocode with exact command patterns (e.g., `git archive --format=tar "${COMMIT_SHA}"`, `sha256sum "$ARTIFACT"`, `GIT_AUTHOR_DATE="${SRC_DATE}" git commit --no-verify ...`). A Phase-6 implementer can produce working YAML from this pseudocode without design-level ambiguity.
- **FM-001-i2 fix fully specified (strong):** The freshness date source is specified to the jq field level: `gh release view "${latest_src_tag}" --repo geekatron/jerry --json publishedAt | jq -r '.publishedAt'` as primary, `git log -1 --format=%cI "${latest_src_tag}^{commit}"` as fallback, with null guard `exit_1("[CRITICAL] D7 freshness: cannot resolve tag time — FAIL-CLOSED")`. The forbidden pattern (`.committer.date`) is named explicitly.
- **FM-002-i2 fix fully specified (strong):** The mandatory OS image is named (`ubuntu-24.04`), the forbidden pattern is named (`ubuntu-latest`), and the scope is explicit (BOTH G9 in `cowork-skeleton.yml` and m1-5 in `cowork-monitor.yml`). The tree-hash hardening option is documented as Phase-6 optional with the condition for eng-infra engagement.
- **FM-003-i2 fix fully specified (strong):** The LGV_SKIP guard is specified as pseudocode with named variables: `IF LGV_SKIP: emit_to_GITHUB_STEP_SUMMARY(...)   ELSE: git tag -f last-good-validated ${deployed_release_version}`. The invariant ("tag with open generation-failure-escalation NEVER becomes last-good-validated") is explicitly stated.
- **G-actions-write-safe gate conditions specified (strong):** The gate specifies an exact grep command (`grep -rn '@v[0-9]' .github/workflows/`) with the scope explicitly listed (all six workflow files).

**Gaps preventing 0.87+:**
- **FM-004-i2 (OPEN):** A Phase-6 implementer following the design will implement `count_open_issues(label="auto-revert:${LATEST_SRC_TAG}")`. This is the specified mechanism. The bypass (human issue closure) is not described anywhere in the design. The actionable fix would be one sentence: "Use `gh issue list --state all --label auto-revert:${LATEST_SRC_TAG} | wc -l` to count ALL issues (open AND closed) — using `--state open` allows bypass via issue closure." This sentence is absent.
- **FM-005-i2 (OPEN):** A Phase-6 implementer following the design will produce `cowork-monitor.yml` without a workflow-level concurrency group. The race condition only manifests under concurrent runs, which are unlikely in testing. The actionable fix ("add `concurrency: group: cowork-monitor` + `cancel-in-progress: false` at the workflow level") is absent from the design.
- **D8 tool name deferred (appropriate):** The exact tool name for the D8 content-safety scanner is Phase-5 deferred (CI-G-003). This is correctly actionable — the catalog path, fail-closed behavior, and CLI interface contract are specified; only the tool identity is deferred to eng-architect delivery.

**Improvement path:**
Add `count_all_issues` pattern to the circuit-breaker step with explicit `--state all` flag. Add a one-line monitor workflow block showing `concurrency: group: cowork-monitor`.

---

### Traceability (0.86/1.00)

**Evidence for score:**
- **30-row Traceability Matrix (strong):** The `phase3-ci-workflow-design.md` Traceability Matrix maps every design element to REQ-NNN, ADR-NNN, and Phase-5 gate. Coverage includes generation steps (G3-G9), security controls (D5, D6, D8), attestation (D4), monitor (D7), circuit-breaker (ROOT-6), and all three iter-2 Critical fixes (FM-001-i2, FM-002-i2, FM-003-i2 each have dedicated rows with full citation).
- **Finding-ID citation density (strong):** All remediated findings are cited by their original IDs (ROOT-N, FM-NNN-QGN, PM-NNN-Q3, DA-NNN) in the Traceability Matrix rows, in the design text, and in the Pending Validation section. A reviewer can trace any design element backwards to the finding that motivated it.
- **Pending Validation section (strong):** 12 items are listed in the Pending Validation section, each with explicit resolution gate (Phase-6, G-monitor, G-provenance, G-actions-write-safe). No design claim is orphaned without a validation gate.
- **Phase-6 gap table (strong):** CI-G-001 through CI-G-007 are individually numbered, named, described, and given Phase-6 actions. CI-G-002 is correctly marked N/A (the release-body mechanism was removed, not deferred).
- **Attestation design §3.3 (strong):** The MONITOR HAND-OFF 8-step table includes explicit FAIL-CLOSED failure mode per step. Each failure mode specifies the system action (exit 1, CRITICAL issue, etc.) — full cause-effect traceability.

**Gaps preventing 0.90+:**
- **FM-005-i2 not in Traceability Matrix:** The only concurrency entry in the Traceability Matrix is `Concurrency group, cancel-in-progress: false | REQ-015` which covers `cowork-skeleton.yml`. There is no entry for `cowork-monitor.yml` concurrency group requirement. A reviewer tracing REQ-015 compliance for the monitor workflow would find no evidence of compliance.
- **PM-008-Q3 SBOM placement not traced:** The SBOM generation step (attestation design §2 "IN" recommendation) is not present in the CI workflow Traceability Matrix. A reviewer cannot trace the SBOM placement decision from REQ to design to gate.

**Improvement path:**
Add a Traceability Matrix row for monitor workflow concurrency group (citing REQ-015 and FM-005-i2). Add a SBOM row (citing REQ-052 or equivalent, attestation design §2, and the appropriate gate).

---

## Critical Findings Closure Table

12 total Critical findings across iter-1 (9) and iter-2 (3).

| # | Finding ID | Severity | Title | Iter | Remediation Applied | Status |
|---|-----------|---------|-------|------|---------------------|--------|
| 1 | FM-007-QG3 | Critical (RPN=315) | GIT_*_DATE cross-step propagation: bare `export` silently fails in separate run step | iter-1 | ROOT-2: same-step inline binding OR `$GITHUB_ENV` propagation; bare cross-step `export` FORBIDDEN with design note | CLOSED |
| 2 | FM-004-QG3 | Critical (RPN=252) | Version sentinel dynamic content: no enforcement against timestamp/run-id injection | iter-1 | `write_static()` function in G5 pseudocode; §3 determinism contract states "ONLY Source-Tag + 40-char SRC_SHA, never timestamp/run-id"; G7 asserts `projects/` contains exactly two known-injected files | CLOSED |
| 3 | FM-023-QG3 | Critical (RPN=240) | jq predicate path unvalidated: D7 parsed release-body assuming SC-04 condemned format | iter-1 | ROOT-1: entire release-body extraction approach removed; replaced by 8-step digest-based monitor that sha256s attested TAR vs shallow-fetch live-tip TAR | CLOSED |
| 4 | FM-020-QG3 | Critical (RPN=216) | Sentinel path ambiguous: `.claude/.jerry-skeleton-version` not excluded by `:!projects/`, D6 fails every release | iter-1 | ROOT-3: sentinel path fixed to `projects/.jerry-skeleton-version`; D6 `:!projects/` excludes BOTH known-injected members; G7 asserts `git ls-files projects/ == {README.md, .jerry-skeleton-version}` | CLOSED |
| 5 | PM-001-Q3 | Critical | Git bundle round-trip unvalidated: HEAD not repositioned after bundle load | iter-1 | ROOT-4: `git checkout refs/remotes/bundle/HEAD` step added; `ASSERT RESTORED_SHA == COMMIT_SHA OR exit_1("[CRITICAL] Bundle restore SHA mismatch")` added | CLOSED |
| 6 | PM-002-Q3 | Critical | D7 jq path placeholder: release-note extraction non-functional; anchored to condemned SC-04 format | iter-1 | ROOT-1: same fix as FM-023-QG3; release-body parsing condemned by ADR-003 SC-04; digest-based monitor eliminates all release-body parsing | CLOSED |
| 7 | PM-003-Q3 | Critical | D8 scanner entirely undefined: no tool name, no pattern catalog, no invocation | iter-1 | ROOT-5: catalog path pinned to `runbooks/content-safety-patterns.md`; fail-closed on absent catalog; scanner interface contract specified (--patterns, --fail-on-match, --fail-on-error); catalog CONTENT is Phase-5 eng-architect deliverable (G-content BLOCKER) | CLOSED (DEFERRED-Phase-6 for catalog content) |
| 8 | PM-004-Q3 | Critical | Auto-revert infinite loop: no bound on revert attempts | iter-1 | ROOT-6: MAX_AUTO_REVERTS=3 circuit breaker; `label: auto-revert:${LATEST_SRC_TAG}` counter; cap exceeded → open CRITICAL human-escalation issue + exit 1; `generation-failure-escalation:${tag}` label suppresses freshness CRITICAL during rollback window | CLOSED |
| 9 | DA-001 | Critical | D7 tree-digest semantically broken: ATTESTED_COMMIT=SRC_SHA always ≠ G6_SHA=live tip; release-notes anchor condemns SC-04 | iter-1 | ROOT-1: 8-step digest monitor compares sha256(attested published TAR) == sha256(shallow-fetch live-tip git archive TAR); SLSA predicate gitCommit field removed; no SHA comparison anywhere | CLOSED |
| 10 | FM-001-i2 | Critical (RPN=343) | Annotated tag `.committer.date` returns null via GitHub API: false freshness-CRITICAL on every run | iter-2 | `gh release view --json publishedAt` (primary); `git log -1 --format=%cI "${latest_src_tag}^{commit}"` (fallback); null guard `exit_1` if both sources empty; `.committer.date` on annotated tag object FORBIDDEN with explicit comment | CLOSED |
| 11 | FM-002-i2 | Critical (RPN=336) | Runner image git version drift: `git archive` PAX header format changes break sha256 idempotency | iter-2 | `ubuntu-24.04` MANDATED for BOTH G9 step in `cowork-skeleton.yml` AND m1-5 step in `cowork-monitor.yml`; `ubuntu-latest` FORBIDDEN for these steps; tree-hash hardening option documented as Phase-6 optional requiring eng-infra sign-off | CLOSED |
| 12 | FM-003-i2 | Critical (RPN=280) | LGV advances to generation-failing tag: suppressed-path sets `last-good-validated` to the failing tag | iter-2 | `LGV_SKIP=true` set in freshness suppression path (m1-8); advance-last-good-validated gated by `IF LGV_SKIP: no-op ELSE: git tag -f last-good-validated ${deployed_release_version}`; tag with open `generation-failure-escalation` label NEVER becomes `last-good-validated` | CLOSED |

**Result: 12/12 Critical findings CLOSED.** PM-003-Q3 catalog content is appropriately DEFERRED-Phase-6 (design-level specification is complete; Phase-5 G-content gate is the blocker for content delivery).

---

## Remaining Open Design Defects

These findings were raised in iter-1 or iter-2 as Major severity but are NOT in the remediation list for either iteration. They remain as design-level gaps that should be addressed before Phase 4.

| # | Finding ID | Severity | Title | Impact | Targetted Fix |
|---|-----------|---------|-------|--------|---------------|
| 1 | FM-004-i2 | Major (RPN=180) | Circuit breaker uses `count_open_issues`; human issue closure resets counter below cap, enabling unlimited auto-reverts | Methodological Rigor, Completeness, Actionability | Replace with `count_all_issues(label=...) --state all`; or use immutable tag-based counter |
| 2 | FM-005-i2 | Major (RPN=168) | No concurrency group for `cowork-monitor.yml`; two concurrent runs can both see count < 3 and both dispatch revert | Methodological Rigor, Completeness, Traceability | Add `concurrency: group: cowork-monitor` + `cancel-in-progress: false` at monitor workflow level |
| 3 | PM-008-Q3 | Major | SBOM generation placed in attestation job; CycloneDX should be generated where environment is known (generation job), not post-generation | Internal Consistency | Move SBOM generation to the generation job or add explicit reconciliation note |
| 4 | FM-034-QG3 | Design Defect | v* tag protection bypass actors specified as "designated maintainers" without naming specific individuals or a GitHub team ID | Completeness, Traceability | Name specific GitHub usernames or a `@geekatron/{team}` reference in attestation design §6.1 |

**Items that are correctly DEFERRED (not penalised):**
- CI-G-007: Shallow-fetch byte-idempotency empirical confirmation (Phase-6 operational test using pinned `ubuntu-24.04`)
- D8 catalog content (C1-C6 patterns): Phase-5 eng-architect deliverable; G-content gate is blocker
- CI-G-005: `contents: write` explicit YAML declaration for monitor job
- CI-G-006: Meta-monitor workflow separation (Phase-6 implementation detail)
- FM-040-QG3: App private key scope during Job A (risk present but bounded by per-job permission isolation already specified)

---

## Improvement Recommendations (Priority Ordered)

| Priority | Finding | Dimension | Current | Target | Recommendation |
|----------|---------|-----------|---------|--------|----------------|
| 1 | FM-004-i2 | Completeness, Methodological Rigor | 0.80 | 0.83 | In the circuit-breaker pseudocode, replace `count_open_issues(label="auto-revert:${LATEST_SRC_TAG}")` with `gh issue list --repo geekatron/jerry --state all --label "auto-revert:${LATEST_SRC_TAG}" \| wc -l`. Add comment: "count ALL issues (open AND closed) — `--state open` allows bypass via manual issue closure". |
| 2 | FM-005-i2 | Methodological Rigor, Traceability | 0.80/0.86 | 0.83/0.88 | Add to the `cowork-monitor.yml` workflow block in the CI workflow design: `concurrency:` / `  group: cowork-monitor` / `  cancel-in-progress: false`. Add to Traceability Matrix: `cowork-monitor.yml concurrency group \| REQ-015 \| — \| —`. |
| 3 | PM-008-Q3 | Internal Consistency | 0.82 | 0.84 | Add a one-sentence note to the attestation design §2 and the CI workflow design attest-job block specifying whether SBOM is generated pre-attestation in the generation job or co-located with attestation. If co-located, explain why the environment snapshot is still valid at attestation time. |
| 4 | FM-034-QG3 | Completeness | 0.80 | 0.81 | In attestation design §6.1, replace "designated maintainers" with the specific GitHub usernames or team slug (e.g., `@geekatron/platform-security`) who hold bypass actor status on the v* tag protection ruleset. |
| 5 | MAX_AUTO_REVERTS=3 basis | Evidence Quality | 0.84 | 0.85 | Add one sentence justifying the value 3: e.g., "3 allows two automatic recovery attempts from transient generation failures before requiring human investigation — enough to recover from ephemeral runner issues without masking systematic design defects." |

**Implementing items 1 and 2 alone would raise the composite score to approximately 0.835-0.840**, which is within the honest design-phase ceiling of ~0.86. Items 3-5 are incremental improvements.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score (specific pseudocode, section references, finding IDs)
- [x] Uncertain scores resolved downward — Internal Consistency resolved to 0.82 not 0.84 (SBOM ambiguity present); Traceability resolved to 0.86 not 0.88 (FM-005-i2 not traced)
- [x] Design-phase calibration applied — design-phase ceiling ~0.86 per task specification; scores in 0.80-0.86 range are appropriate for this complexity level
- [x] No dimension scored above 0.90 (highest is Traceability at 0.86, justified by the 30-row Traceability Matrix)
- [x] First-draft-equivalent calibration: this is iter-2, significant revision from iter-1 (0.702 → 0.820); the +0.118 delta reflects genuine remediation of 12 Criticals
- [x] Open Majors (FM-004-i2, FM-005-i2) scored as design gaps — not deflated but not ignored
- [x] Deferred Phase-6 items correctly excluded from penalty per task calibration note

**Anti-leniency verification:** Would I award 0.85+ on Completeness given FM-004-i2 and FM-005-i2? No. Those are unaddressed circuit-breaker correctness gaps that require a specific change to close. Completeness at 0.80 is the correct score — the design is genuinely good but not complete on these items.

---

## Design-Phase Ceiling Assessment

**Current composite: 0.820**
**Estimated honest ceiling for this design: ~0.86**

The gap between 0.820 and 0.86 is attributable entirely to FM-004-i2, FM-005-i2, PM-008-Q3, and FM-034-QG3. These are all addressable with targeted text changes (1-3 sentences each). The 0.86 ceiling reflects the inherent deferred-validation component of a design document — designed-but-unvalidated controls (P-222) cannot score as high as empirically verified controls; this gap resolves when Phase-5 gates pass.

**Proceed to Phase 4?** No — not yet. FM-004-i2 and FM-005-i2 represent design errors (not Phase-6 deferred details) that a Phase-6 implementer following the current design would replicate. The circuit breaker would be bypassable and the monitor would have a concurrency race. Close these two items first (estimated effort: 30 minutes of design editing), then proceed to Phase 4 with confidence that the Phase-3 design is complete at its honest ceiling.

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.820
prior_score: 0.702
delta: +0.118
threshold: 0.92
weakest_dimension: Completeness
weakest_score: 0.80
critical_findings_count: 12
critical_findings_closed: 12
critical_findings_open: 0
open_major_defects: 2
iteration: 2
improvement_recommendations:
  - "FM-004-i2 (Priority 1): Replace count_open_issues with count_all_issues --state all in circuit-breaker pseudocode to prevent bypass via issue closure"
  - "FM-005-i2 (Priority 2): Add concurrency group cowork-monitor to monitor workflow block and Traceability Matrix"
  - "PM-008-Q3 (Priority 3): Clarify SBOM job placement — generation job vs attestation job — with explicit reconciliation"
  - "FM-034-QG3 (Priority 4): Name specific bypass actors in attestation design §6.1 (replace 'designated maintainers' with GitHub username/team)"
  - "MAX_AUTO_REVERTS=3 (Priority 5): Add one-sentence basis for the value 3 in circuit-breaker specification"
design_phase_ceiling: 0.86
at_ceiling: false
proceed_to_phase4: false
proceed_condition: "Close FM-004-i2 and FM-005-i2 in CI workflow design; re-score expected ~0.835-0.840"
```

---

*Scored by adv-scorer (S-014 LLM-as-Judge). Agent: claude-sonnet-4-6. P-003 compliant (no subagents spawned). P-022 compliant (no inflation; leniency bias counteracted). P-002 compliant (persisted to file). Constitutional triplet applied: P-003/P-020/P-022.*

*Sources consumed: phase3-skeleton-generation-design.md (all 865 lines confirmed), phase3-ci-workflow-design.md (all 865 lines confirmed), phase3-attestation-provenance-design.md, s-004-pre-mortem-findings.md, s-012-fmea-findings.md, s-002-devils-advocate-findings.md, s-012-fmea-iter2-findings.md.*
