# Quality Score Report: PROJ-031 CoWork Skeleton — Phase 1 Design Package (Iteration 2)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, top action item |
| [Scoring Context](#scoring-context) | Deliverables, strategy, SSOT reference |
| [Score Summary](#score-summary) | Composite vs. targets, delta from iteration 1 |
| [Dimension Scores](#dimension-scores) | 6-dimension table with evidence summaries and deltas |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence, gaps, improvement path |
| [Consolidated Remediation List](#consolidated-remediation-list) | 7 convergent-theme items for iteration 3 |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered repair actions |
| [Anti-Leniency Statement](#anti-leniency-statement) | Leniency bias counteraction record |
| [Leniency Bias Check](#leniency-bias-check) | Checklist |
| [Session Context](#session-context) | Handoff schema for orchestrator |

---

## L0 Executive Summary

**Score:** 0.801/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.78)

**One-line assessment:** Iteration-2 remediation closed six of the top-priority iteration-1 gaps (H-04 first-run UX, REQ-034 three-dimensional R-001 gate, NFR-006 staleness, inputs.target_tag, P-042 risk matrix, pre-push ordering), lifting the composite by +0.020 to 0.801, but five Critical findings remain unresolved — all converging on a single root pattern: the ADRs describe three mandatory compensating controls (pre-publication integrity gate, tag-name sanitization, runtime push-failure detection) as "required" or "MUST" while WS-3 contains zero corresponding SHALL requirements, leaving them implementation-optional and invisible to Phase-6 checklists; resolve IT3-001 through IT3-004 (the ADR-prose-vs-requirements gap and its downstream architecture, staleness, and R-001 proxy issues) before iteration 3 re-scoring.

---

## Scoring Context

| Field | Value |
|-------|-------|
| **Deliverable 1** | `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md` |
| **Deliverable 2** | `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md` |
| **Deliverable 3** | `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md` |
| **Deliverable Type** | Design Package (Requirements + Architecture Decision Records) |
| **Criticality Level** | C4 (AE-003 new ADRs; AE-005 security-relevant CI/token handling) |
| **Quality Target** | 0.95 (project-specified; exceeds constitutional minimum of 0.92 per H-13) |
| **Gate Threshold** | 0.92 (H-13) |
| **Scoring Strategy** | S-014 (LLM-as-Judge) |
| **SSOT Reference** | `.context/rules/quality-enforcement.md` |
| **Strategies Incorporated** | 8 of 8 (S-001, S-002, S-003, S-004, S-007, S-011, S-012, S-013) |
| **Prior Score (Iteration 1)** | 0.781 |
| **Score Delta** | +0.020 |
| **Scored** | 2026-06-26 |
| **Scorer** | adv-scorer (jerry:adv-scorer), Iteration 2 |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite (Iteration 2)** | 0.801 |
| **Prior Composite (Iteration 1)** | 0.781 |
| **Delta** | +0.020 |
| **Project Target** | 0.95 |
| **Gate Threshold (H-13)** | 0.92 |
| **Gap to Gate** | −0.119 |
| **Gap to Target** | −0.149 |
| **Verdict** | **REVISE** |
| **Strategy Findings Incorporated** | Yes — all 8 strategy reports |
| **Raw Critical findings across 8 strategies** | 11 (before deduplication) |
| **Deduplicated Critical themes** | 5 (integrity gate, R-001 proxy, staleness forgeability, tag sanitization absent as REQ, clone weight monitoring) |
| **Critical findings resolved from iteration 1** | 8 of 14 |
| **Iteration** | 2 |

---

## Dimension Scores

| Dimension | Weight | Score It-2 | Weighted | Score It-1 | Delta | Evidence Summary |
|-----------|--------|------------|----------|------------|-------|-----------------|
| Completeness | 0.20 | 0.80 | 0.160 | 0.77 | +0.03 | Gains: REQ-024a, REQ-034, NFR-006, inputs.target_tag, marketplace.json. Residue: pre-pub gate no REQ, tag sanitization no REQ, R-001 proxy-only, no CoWork smoke test, no clone-weight monitoring |
| Internal Consistency | 0.20 | 0.78 | 0.156 | 0.76 | +0.02 | Gains: directory lists reconciled, full SHA template, loop-safety completeness, L0 qualifier. Residue: ADR-001 GITHUB_REF_NAME wrong for workflow_dispatch (CC-002); NFR-006 trailer-check inconsistent with ADR tamper-evidence claim; ADR says "required" but no requirements match |
| Methodological Rigor | 0.20 | 0.80 | 0.160 | 0.78 | +0.02 | Gains: P-042 5×5 risk matrix, empirical ruleset inventory (id 12387947), REQ-022 pre-push ordering. Residue: R-001 still proxy-only (no CoWork install), staleness uses forgeable metric, single 10 Mbps clone reference, blank-target-tag undefined, validation timing unspecified |
| Evidence Quality | 0.15 | 0.80 | 0.120 | 0.79 | +0.01 | Gains: GitHub Docs URL added, empirical ruleset check with specific data, clone-weight thresholds quantified in ADR-001. Residue: R-001 foundational assumption user-reported (Anthropic silent), pack-size threshold in REQ-034(b) undefined, marketplace.json CoWork-runtime resolution unverified |
| Actionability | 0.15 | 0.82 | 0.123 | 0.80 | +0.02 | Gains: REQ-024a H-04 first-run UX, REQ-011 inputs.target_tag, NFR-006 staleness schedule, REQ-034 three-dimensional gate with artifact path. Residue: integrity gate no REQ (not actionable to implement), tag sanitization no WS-3 mandate, blank-target-tag resolution mechanism unspecified |
| Traceability | 0.10 | 0.82 | 0.082 | 0.80 | +0.02 | Gains: STK-003 → REQ-024a trace added. Residue: ADR-002 c-107 mandatory compensating controls trace to no REQ-xxx; tag sanitization ADR "MUST" traces to no WS-3; REQ-009 cross-references R-001 §Verification Approach but that section contains no symlink test dimension |
| **TOTAL** | **1.00** | | **0.801** | | **+0.020** | |

**Arithmetic check:** 0.160 + 0.156 + 0.160 + 0.120 + 0.123 + 0.082 = **0.801**

---

## Detailed Dimension Analysis

### Completeness (0.80/1.00) — Delta +0.03

**Evidence for improvement:**

Six iteration-1 Critical/Major completeness gaps were closed in iteration 2:
- REQ-024a added: Tutorial now SHALL include H-04 first-run experience with `<project-required>` resolution (closed DA-002/CC-002 from iteration 1)
- REQ-034 added: Three-dimensional R-001 machine-checkable gate with artifact at `verification/R001-clean-clone-count.md` (closed REM-001 from iteration 1 — partially)
- NFR-006 added: Weekly staleness-detection workflow requirement with Source-Commit trailer comparison (closed REM-006 from iteration 1 — partially)
- REQ-011 inputs.target_tag added: workflow_dispatch can now target specific past tags (closed REM-007 from iteration 1)
- Marketplace.json check added to REQ-005 (closed DA-003 from iteration 1)
- P-042 5×5 risk matrix added: R-001 (3×5=15 YELLOW border-high), R-007b (3×4=12 YELLOW) now numerically scored (closed REM-011)

**Remaining completeness gaps with source citations:**

1. **Pre-publication integrity gate absent from requirements** (PM-001 Critical, FM-001 Critical RPN-280, IN-001 Critical, RT-002 Critical, CV-001 Major, CC-004 Minor): ADR-002 §Branch-Protection Posture designates the post-push SHA equality check as a "mandatory compensating control" (c-107, "required"). ADR-001 §Tamper-Evidence calls for "add a pre-publication integrity gate that asserts `git rev-parse cowork-skeleton == <expected SHA>` before the branch is advertised as installable." Zero WS-3 requirements capture this. Phase 5/6 implementers reading requirements alone have no mandate to build this gate — the security control described as "required" in both ADRs is implementation-optional.

2. **Tag-name sanitization absent from requirements** (PM-003 Critical, FM-010 Major, CV-002 Major): ADR-001 §Tag-name sanitization (RT-04) states the generation script "MUST" validate GITHUB_REF_NAME against `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` and never interpolate `${{ github.ref_name }}` in `run:` blocks. Zero WS-3 requirements capture this. A classic shell injection vector is documented as "MUST" in ADR prose but absent from requirements.

3. **Runtime push-failure detection absent from requirements** (FM-005 Major aspirational only): ADR-002 §Branch-Protection Posture lists "runtime push-failure detection" as a mandatory compensating control alongside the integrity gate. The workflow SHALL detect when force-push fails (e.g., due to a new ruleset) and exit non-zero with a structured diagnostic. No REQ captures this.

4. **R-001 three-dimensional gate is proxy-only** (PM-002 Critical, CV-003 Major, FM-002 Critical RPN-252): REQ-034's three dimensions — tracked file count, compressed pack size, estimated clone time — are all proxy measurements. No acceptance criterion requires executing `claude plugin marketplace add geekatron/jerry@cowork-skeleton` in an actual CoWork environment. REQ-034's sufficiency claim ("All three dimensions must pass before any Phase 5 implementation script may execute") implies the gate establishes Phase 5 readiness, but it does not: CoWork may still refuse to install if the limit mechanism differs from the file-count assumption. Additionally, pack-size dimension (b) has no explicit PASS threshold in REQ-034 AC — only the 120-second clone-time threshold is specified.

5. **Clone-weight monitoring absent** (IN-002 Critical, FM-007 Major): Under Option A, `cowork-skeleton`'s `.git` inherits full `main` history on every release. Clone time and pack size grow monotonically. REQ-034's single-shot Phase-2 measurement doesn't account for this; NFR-006 checks the Source-Commit trailer, not clone weight. No requirement mandates periodic re-measurement. The ADR-001 fallback threshold (>250 MB pack or >60s clone at 10 Mbps) can be crossed silently between Phase-2 measurement and a future release.

6. **NFR-006 implementation story missing** (IN-003 Major): No STORY entity covers implementing `cowork-skeleton-staleness.yml`. The 5 existing stories cover generation script, stub, acceptance tests, STRIDE, and branch-protection config. The staleness workflow (NFR-006) has no implementation ownership path or permissions specification (`issues: write` required for GitHub issue creation, not declared).

7. **uv CoWork prerequisite undocumented** (DA-004 Major, CC-001 Major): REQ-004 and REQ-024a both specify `uv run jerry` as the H-04 bootstrap CLI invocation. But neither the Tutorial (REQ-024) nor the troubleshooting guide (REQ-027) requires documenting `uv` as a system prerequisite for CoWork plugin users, nor provides a recovery path for "`uv: command not found`" in the hook runtime.

**Improvement path:** IT3-001 (REQ-035 integrity gate, REQ-036 tag sanitization, push-failure detection), IT3-003 (REQ-034 smoke test + pack threshold + clone monitoring), IT3-006 (uv prerequisite in REQ-024/REQ-027).

---

### Internal Consistency (0.78/1.00) — Delta +0.02

**Evidence for improvement:**

Four concrete iteration-1 inconsistencies were resolved:
- ADR-001 c-003 / REQ-005 directory lists reconciled: both now show the 8-entry canonical plugin-retention surface, SSOT is ADR-001 c-003, REQ-005 sync note added (closed REM-008)
- Short-SHA template fixed: ADR-001 §Regeneration Commit Determinism now uses full 40-char SHA in commit message template (closed REM-009)
- Release.yml added to ADR-002 loop-safety guarantee #2 coverage (closed REM-018)
- L0 file count qualifier fixed: "approximately 1,744" (closed REM-020)
- REQ-016 priority correction (Should → Must) (closed REM-006 partially)

**Remaining internal consistency gaps:**

1. **ADR-001 GITHUB_REF_NAME pseudocode wrong for workflow_dispatch** (CC-002 Major): ADR-001 §Regeneration Commit Determinism pseudocode line 1 reads `TAG="${GITHUB_REF_NAME}"` with comment "# already validated against the allow-list." For a `push: tags` event, GITHUB_REF_NAME equals the tag name (correct). For a `workflow_dispatch` event — including the case where `inputs.target_tag` is provided — GITHUB_REF_NAME equals the triggering branch name (e.g., `main`). An implementer following this pseudocode verbatim for workflow_dispatch would assign `TAG="main"`, causing `git rev-parse "main^{commit}"` to resolve to HEAD of main (non-deterministic), breaking REQ-003 (bit-identical SHA) and NFR-005 (re-runnable for past tags). The pseudocode is inconsistent with REQ-011's workflow_dispatch + inputs.target_tag requirement.

2. **NFR-006 detection mechanism inconsistent with ADR tamper-evidence claim** (CV-004 Minor in CoVe, FM-003 Critical in FMEA, RT-004 Major in Red Team): ADR-001 §Tamper-Evidence states "any in-place modification... changes the tip SHA away from the deterministically expected value and is detectable by anyone who recomputes it." ADR-002 §Branch-Protection Posture calls the pre-publication integrity gate a mechanism that "converts 'unprotected' from a write-control gap into a verifiable-integrity property." But NFR-006 (the only periodic check with a backing requirement) compares the `Source-Commit:` trailer in the commit message — free-form text, forgeable by any push actor — not the tip SHA. A direct-push attacker who knows the correct tag SHA can write `Source-Commit: <correct-sha>` in their commit message and NFR-006 reports "no staleness" even though the branch content is compromised. The ADR claims a detectable property while the required check doesn't detect it.

3. **ADR describes "required" controls, requirements are silent** (CV-001 Major, PM-001 Critical, IN-001 Critical): ADR-002 c-107 states "artifact integrity MUST rest on a compensating control (deterministic-SHA tamper-evidence + pre-publication integrity gate)." ADR-001 §Tamper-Evidence calls the gate the "operationalization" of tamper-evidence. These claims create an expectation of an implemented control, but no WS-3 requirement mandates it. The deliverable body (ADRs) and the contract (requirements) are inconsistent on what is "required."

4. **Loop-safety guarantee #2 still incomplete** (CV-006 Minor): ADR-002 guarantee #2 names 3 of 6 repository workflows and states "three watched workflows named in REQ-014" — but REQ-014 names four workflows (adding cowork-skeleton.yml). CI.yml, pat-monitor.yml, and security-scan.yml are unmentioned (though independently verified safe in CoVe). Minor factual error, no functional risk.

5. **Idempotency proof "pure function of T" conflates tag-name string with tag-name-to-SHA resolution** (CV-005 Minor): The proof states "regenerate(T) is a pure function of T" but does not state the required assumption that T → S is a fixed mapping (i.e., tag T must be immutable). For the workflow_dispatch path, if a maintainer force-moves tag T, the proof silently breaks.

**Improvement path:** IT3-002 and IT3-005 (fix ADR-001 pseudocode for workflow_dispatch, architectural reframing of integrity gate); IT3-004 (align NFR-006 detection with ADR tamper-evidence claim).

---

### Methodological Rigor (0.80/1.00) — Delta +0.02

**Evidence for improvement:**

- P-042 5×5 numeric risk matrix added with R-001 (3×5=15 YELLOW border-high), R-007 (2×5=10), R-007b (3×4=12), R-003 (3×2=6), R-005 (2×4=8), R-006 (2×3=6) — arithmetic verified correct (closed REM-011)
- Empirical org-level ruleset inventory added to ADR-002: `gh api orgs/geekatron/rulesets` → HTTP 404; `gh api repos/geekatron/jerry/rulesets` → 1 ruleset (id 12387947, "Don't fuck with main", targeting `~DEFAULT_BRANCH`) — first-party verification with specific IDs and access date (closed REM-002 partially)
- REQ-022 pre-push ordering explicitly specified: "SHALL run as an automated in-workflow step BEFORE the force-push step" (closed REM-005)
- Tag-name sanitization security note added to ADR-001 (RT-04 subsection) (closed REM-016)
- Full 40-char SHA in commit message template (closed REM-009)
- REQ-034 three-dimensional verification approach (closed REM-001 partially)

**Remaining methodological rigor gaps:**

1. **R-001 verification is proxy-only — no actual CoWork installability test** (PM-002 Critical, FM-002 Critical RPN-252, IN-002 Critical, CV-003 Major): REQ-034's three proxy dimensions (file count, pack size, clone time) establish necessary but insufficient conditions for CoWork installability. The underlying assumption (CoWork's limit applies to clean-clone tracked-file count) is unverified by Anthropic documentation and undocumented externally. CoWork could apply the limit to local working directory (including .venv/), total git object count, or per-plugin-agent-load, all of which would make the proxy measurements pass while CoWork refuses to install. No acceptance criterion in any requirement tests actual CoWork installation.

2. **Staleness detection methodology uses forgeable proxy** (FM-003 Critical RPN-224, RT-004 Major, CV-004 Minor): The Source-Commit: trailer verification in NFR-006 is adequate for detecting "CI failed to run" (lazy staleness) but bypassable by targeted tampering. S-012 FMEA rates this Critical (RPN-224) due to Severity=7 (direct-push attacker succeeds undetected for full weekly interval) × Occurrence=4 × Detectability=8 (8=hard to detect via current method). The methodologically correct approach — comparing the live tip SHA to the independently-recomputable expected SHA — is described in ADR-001 but not required by any NFR.

3. **Clone-time estimate uses single optimistic 10 Mbps reference** (FM-007 Major RPN-168, IN-002 Critical): ADR-001 Option B fallback trigger (>60s clean clone on 10 Mbps) uses a bandwidth above the 30th-40th percentile of global broadband. A user at 2 Mbps experiences 5× longer clone times. If the pack size is 60 MB, the 10 Mbps estimate is 48s (pass) but the 2 Mbps actual time is 240s (timeout). No requirement extends the reference to multiple bandwidths or acknowledges this coverage gap.

4. **Validation timing for REQ-005/010 relative to force-push unspecified** (FM-012 Major RPN-105): REQ-022 explicitly states the pre-push diff gate runs BEFORE force-push. REQ-005 (8-directory presence) and REQ-010 (plugin.json agent path existence) do not specify whether their checks run before or after the push. If implemented as post-push V&V, a script bug that accidentally strips `.claude-plugin/` would not be caught before publication (though REQ-022's diff gate would catch this via a non-empty diff, the explicit ordering prevents ambiguity).

5. **No per-run SHA assertion requirement** (FM-005 Major RPN-168): ADR-001 §Regeneration Commit Determinism notes "CI SHA assertion where feasible" as a risk control — aspirational. No requirement mandates that the generation script recompute the expected SHA on every invocation and assert equality with the actual commit SHA produced. A future maintenance change to the commit message template would silently break idempotency until the next manual REQ-003 V&V re-run.

6. **Blank inputs.target_tag resolution mechanism undefined** (FM-008 Major RPN-144): REQ-011 describes `inputs.target_tag` with parameter description "defaults to latest pushed tag if blank" but the body of REQ-011 does not specify the resolution mechanism. Options — `git describe --tags --abbrev=0`, `git tag -l 'v*' --sort=-version:refname | head -1`, or GITHUB_REF_NAME (which is the triggering branch, not a tag, for workflow_dispatch) — have different behaviors and security properties. The description is in the parameter metadata string, not in the requirement body with an acceptance criterion.

**Improvement path:** IT3-003 (R-001 smoke test + clone-width reference), IT3-004 (NFR-006 non-forgeable SHA comparison), IT3-005 (fix GITHUB_REF_NAME pseudocode, define blank-target-tag resolution in REQ-011 body).

---

### Evidence Quality (0.80/1.00) — Delta +0.01

**Evidence for improvement:**

- Specific GitHub Docs URL added to ADR-002 References for GITHUB_TOKEN non-retrigger guarantee (closed REM-017)
- Empirical org-level ruleset inventory: `gh api orgs/geekatron/rulesets → 404; id 12387947 "Don't fuck with main" → ~DEFAULT_BRANCH only` with access date 2026-06-26 — highly traceable first-party evidence (closed REM-002)
- Clone-weight thresholds now quantified in ADR-001 (Option B trigger: >250 MB pack or >60s at 10 Mbps on a reference link) (closed REM-013 partially — clone weight thresholds are now stated, though not measured for current pack size)
- Tamper-evidence argument is now explicit in ADR-001 §Tamper-Evidence with a logical chain from determinism proof to detectability claim

**Remaining evidence quality gaps:**

1. **R-001 foundational assumption still user-reported** (CV-003 Major, FM-002 Critical, PM-002 Critical): The entire branch-stripping strategy rests on "CoWork's ~5,000-file plugin-load limit applies to the tracked file count of a clean-clone working tree." This is explicitly disclosed as an "unverified settled fact from user reports." Anthropic's Claude Code plugin documentation is silent on this limit. The deliverables honestly disclose this gap (R-001 §Statement, R-001 §Verification Approach: "still warrants empirical confirmation") which is a positive governance signal, but the foundational evidence quality remains low until empirical confirmation is obtained.

2. **Pack-size threshold in REQ-034(b) undefined** (CV-003 Major): REQ-034's three dimensions are required but only dimension (c) (clone time, 120s) has an explicit PASS/FAIL threshold. Dimension (b) (compressed pack size) records the measurement "in MB" but no requirement specifies what MB value constitutes PASS. The <250 MB fallback trigger in ADR-001 is the natural threshold, but it is not referenced in REQ-034 AC. This makes dimension (b) unverifiable as a gate — the PASS/FAIL determination cannot be confirmed.

3. **marketplace.json relative-path resolution unverified at CoWork runtime** (FM-009 Major RPN-144, IN-004 Major): REQ-005 verifies `git ls-files .claude-plugin/marketplace.json` returns non-empty. REQ-010 verifies agent path entries exist in `git ls-files`. Neither verifies that `source: "./"` in `marketplace.json` resolves correctly when CoWork loads the plugin via its cache path (`~/.claude/plugins/cache/`). The evidence for installability rests entirely on file presence in the git tree, not on runtime CoWork behavior.

4. **Symlink behavior in CoWork runtime unverified** (IN-004 Major): REQ-009 AC explicitly restricts its scope to "CI Linux environment." REQ-009 notes that "CoWork session symlink resolution is separately verified in R-001 §Verification Approach before Phase 5" but REQ-034 (the iteration-2 R-001 gate) specifies no symlink dimension. The cross-reference points to a verification that doesn't include the referenced test.

5. **SM-001-it2: decisive framing lacks falsifiability cross-reference** (SM-001-it2 Critical from Steelman, presentation-level): ADR-001's decisive framing ("CoWork installs tip tree only, so stripping projects/ is sufficient") is stated as a design fact without referencing REQ-034 as the test that would falsify it if wrong. The falsifiability chain exists (R-001 → REQ-034 → Phase-5 empirical) but is not connected back to the decisive framing in ADR-001. This is a presentation gap rather than a structural evidence gap but reduces the self-evidencing quality of the argument.

**Improvement path:** IT3-003 (add direct CoWork install as REQ-034 dimension, add explicit pack-size threshold), IT3-006 uv prerequisite (strengthens how-to evidence).

---

### Actionability (0.82/1.00) — Delta +0.02

**Evidence for improvement:**

- REQ-024a: Tutorial now SHALL include H-04 first-run experience (closed REM-004 — the Critical gap from iteration 1 where a CoWork user encountering `<project-required>` had no documented path)
- REQ-011 with inputs.target_tag: workflow_dispatch tag targeting is now specified in requirements (closed REM-007)
- REQ-022 pre-push gate: explicit in-workflow step ordering before force-push (closed REM-005)
- NFR-006: Actionable schedule-based check with specific comparison artifact (`Source-Commit:` trailer vs. latest v* tag SHA) and visible failure mode (job failure or GitHub issue)
- REQ-034: Three-dimensional gate with machine-readable artifact at `verification/R001-clean-clone-count.md` — Phase-5-blocking gate is now concrete
- S-010 Self-Refine iterations documented in all three deliverables — actionable revision history

**Remaining actionability gaps:**

1. **Pre-publication integrity gate: no REQ means no implementation mandate** (FM-001 Critical, PM-001 Critical, IN-001 Critical): The control described as "required" in ADR-002 §Branch-Protection Posture has no corresponding WS-3 SHALL. A Phase 5/6 engineer implementing the CI workflow from requirements alone has no contract item to build. The gate is architecturally necessary (it is the only mechanism for non-forgeable tamper detection) but actionably absent.

2. **Tag sanitization: no WS-3 mandate** (PM-003 Critical, FM-010 Major, CV-002 Major): ADR-001 RT-04 says the generation script "MUST" validate tag names and "NEVER interpolate `${{ github.ref_name }}` directly into a `run:` shell string." Without a WS-3 requirement, Phase 5/6 engineers using script templates with direct interpolation introduce a shell-injection surface while technically complying with all requirements.

3. **Blank inputs.target_tag resolution: no concrete procedure** (FM-008 Major RPN-144): REQ-011 mentions "defaults to latest pushed tag if blank" in the parameter description, not the requirement body, with no AC. An implementer has no defined action for blank-target-tag resolution. The three available mechanisms (`git describe`, `git tag -l`, or GITHUB_REF_NAME — which is wrong for workflow_dispatch) have different behaviors; no mechanism is specified.

4. **NFR-006 implementation story missing** (IN-003 Major): No STORY entity or workflow skeleton exists for the staleness-detection workflow. NFR-006's "OR" (job failure OR GitHub issue) introduces actionable ambiguity: if job-failure-only is implemented, the failing run may go unnoticed for a week; if GitHub-issue-creation is implemented, `issues: write` permission is required, not declared. The NFR is specified but the action path to implementation is unclear.

**Improvement path:** IT3-001 (REQ-035/036/037 for integrity gate, tag sanitization, push-failure), IT3-004 (NFR-006 revisions + implementation story), IT3-005 (blank-target-tag resolution in REQ-011 body).

---

### Traceability (0.82/1.00) — Delta +0.02

**Evidence for improvement:**

- STK-003 → REQ-024a trace added in Traceability Summary: the H-04 first-run UX requirement is now traced to the "immediately usable" stakeholder need (closed iteration-1 Critical gap)
- REQ-004a traces to ADR-001 stub determinism constraint (closed REM-010 partially)
- REQ-022 pre-push gate traces to REQ-019 (no secret leakage, supply-chain) and REQ-020 (least-privilege) — the traceability chain for security controls strengthened
- ADR-001 and ADR-002 cross-reference: the tamper-evidence argument cross-references both ADRs correctly; the integrity gate "owned by ADR-002 §Branch-Protection Posture" is clearly stated
- All 34 requirements (REQ-001–034, NFR-001–006) have V-method assignments and AC — zero orphan requirements

**Remaining traceability gaps:**

1. **ADR mandatory compensating controls → no REQ-xxx traceability** (CV-001 Major, FM-001 Critical, PM-001 Critical): ADR-002 c-107 asserts "artifact integrity MUST rest on a compensating control (deterministic-SHA tamper-evidence + pre-publication integrity gate)." ADR-001 §Tamper-Evidence says the gate is "operationalized in ADR-002 §Branch-Protection Posture." ADR-002 §Branch-Protection Posture calls the gate "required" and "mandatory." But the requirements document contains no traceability link from this ADR design decision to any WS-3 SHALL. A V&V engineer tracing from ADR-002 c-107 to implementation would reach a dead end in the requirements.

2. **Tag sanitization ADR "MUST" → no WS-3 requirement traceability** (CV-002 Major, PM-003 Critical): ADR-001 RT-04 describes a "MUST" security control. ADR-001 §Consequences/Security cross-references this note. But tracing the control forward from ADR to requirements to implementation returns no result: no REQ-xxx mandates tag validation or injection-safe shell variable passing.

3. **REQ-009 cross-references non-existent R-001 symlink dimension** (IN-004 Major): REQ-009 note states "CoWork session symlink resolution is separately verified in R-001 §Verification Approach before Phase 5." But REQ-034 (the R-001 machine-checkable gate) specifies three dimensions: (a) file count, (b) pack size, (c) clone time. No symlink dimension exists. The cross-reference is broken — REQ-009 points to a verification step that isn't there.

4. **PLAN.md trigger description misaligns with REQ-011** (CC-003 Minor): PLAN.md Confirmed Decision 2 describes the trigger as "GitHub Release published plus manual `workflow_dispatch`." REQ-011 specifies `push: tags: ['v*']` and `workflow_dispatch` — a different GitHub Actions event. The rationale in REQ-011 explains the refinement, but PLAN.md is not updated and there is no cross-reference note, leaving a trace gap for future reviewers consulting PLAN.md.

5. **Loop-safety guarantee #2 names "three watched workflows named in REQ-014" but REQ-014 names four** (CV-006 Minor): The guarantee claims to address REQ-014 but its enumeration is one short. A trace from REQ-014 to ADR-002 guarantee #2 leaves one workflow untraced by name.

**Improvement path:** IT3-001 (add REQ-035/036 to create traceability chain from ADR controls to requirements); IT3-005 (extend IT3-005 to cover REQ-011 body with blank-target-tag resolution, which also closes ADR→REQ trace for tag sanitization).

---

## Consolidated Remediation List

Seven convergent themes are deduplicated across all 8 strategy reports. Each item has a stable ID, severity, merged finding IDs, single primary owner (with align-role for second owner when both must act), and a concrete fix. Phase column: P1 = Phase-1 completeness/must-fix for QG-1 closure; P2 = Phase 2 (STRIDE, FMEA, security) scope but noted here for awareness.

| ID | Severity | Merged Finding IDs | Primary Owner | Align Owner | Fix | Phase |
|----|----------|--------------------|---------------|-------------|-----|-------|
| IT3-001 | Critical | PM-001, RT-001, RT-002, CV-001, CV-002, FM-001, FM-010, IN-001, CC-004 | nse-requirements | ps-architect | Add three WS-3 SHALL requirements that back the ADR mandatory compensating controls currently described only in ADR prose: **(a) REQ-035** — "The CI workflow SHALL compute the expected deterministic SHA for the release tag (by re-running the same inputs: source commit SHA, fixed identity, pinned date, fixed message template) and SHALL publish that SHA as a durable artifact (e.g., appended to the GitHub Release body via `gh release edit v{TAG} --notes-append`) before cowork-skeleton is referenced as installable in any GitHub Release, plugin registry, or documentation." AC: a simulated direct push to cowork-skeleton is detected by the next staleness run via SHA mismatch. **(b) REQ-036** — "The generation script SHALL validate both GITHUB_REF_NAME (for push:tags trigger) and inputs.target_tag (for workflow_dispatch trigger) against the allow-list `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` and SHALL exit non-zero if either fails validation. The validated tag value SHALL be assigned to a shell variable and consumed only via quoted shell expansion — NEVER via direct `${{ github.context_value }}` interpolation in a `run:` block." AC: workflow_dispatch run with inputs.target_tag=`; malicious_cmd; v0.0.0` exits non-zero before any git operation. **(c) REQ-037** — "The force-push step SHALL be wrapped to detect push failure (exit non-zero from `git push --force origin HEAD:cowork-skeleton`) and SHALL emit a structured diagnostic identifying the blocking ruleset or remote rejection message before the job fails." AC: simulate a non-zero push exit; CI step captures and emits the failure message. ps-architect aligns ADR-002 §Branch-Protection Posture to list REQ-035, REQ-036, and REQ-037 as the formal requirements backing the three compensating controls. | P1 |
| IT3-002 | Critical | DA-002, RT-001, RT-002, IN-001, FM-001, CC-004 | ps-architect | nse-requirements | Reframe the "pre-publication integrity gate" architecture in ADR-002. A gate placed inside `cowork-skeleton.yml` immediately after the force-push is asserting the SHA the same job just created — this is tautological and provides no protection against tampering that occurs after the job completes. **Architectural revision:** (a) `cowork-skeleton.yml` publishes the expected deterministic SHA to a durable external artifact (GitHub Release notes per REQ-035); (b) the NFR-006 staleness workflow (running weekly) independently retrieves the published SHA from the Release notes and asserts `git rev-parse cowork-skeleton == <published SHA>` — making the comparison temporally and contextually independent of the creating workflow. Document that "pre-publication" does not mean "inside the generating CI job" but rather "before the branch is actively distributed to users" — in practice, the continuous integrity monitoring from IT3-004 serves this purpose asynchronously. If synchronous protection is required, reconsider branch protection ruleset allowing only github-actions[bot] bypass (upgrade path documented in ADR-002). Update ADR-002 §Branch-Protection Posture to describe this 2-step publish+assert architecture. nse-requirements: REQ-035 (IT3-001a) operationalizes this. | P1 |
| IT3-003 | Critical | PM-002, CV-003, FM-002, FM-007, IN-002 | nse-requirements | — | Revise REQ-034 and add ongoing monitoring: **(a) REQ-034d** — "One dimension of the R-001 verification SHALL be a direct CoWork plugin-install attempt: install `geekatron/jerry@cowork-skeleton` in a running CoWork client (Claude Desktop or equivalent) on a reference machine and confirm the plugin loads without error within the 120-second timeout." This is the only dimension that directly tests STK-001 ("installs in Claude CoWork without triggering the plugin-load file-count limit"). **(b) REQ-034 dimension (b) PASS threshold** — add explicit: "compressed pack size SHALL be < 250 MB (the ADR-001 Option B fallback trigger)" to REQ-034 AC, making dimension (b) unambiguously verifiable. **(c) REQ-034 clone-time coverage** — add a 2 Mbps reference calculation alongside the 10 Mbps reference (10 Mbps represents ~30th–40th percentile global broadband; document coverage boundary). **(d) Clone-weight monitoring** — add to `cowork-skeleton.yml`: emit `git count-objects -vH | grep size-pack` to `$GITHUB_STEP_SUMMARY` on every run; hard-fail if size-pack exceeds 250 MB (triggers automatic Option B consideration); add to NFR-006: the staleness workflow SHALL also record `size-pack:` MB and alert (GitHub issue) when it exceeds 150 MB (60% of the 250 MB Option B trigger, providing advance warning of clone-weight growth). Note: under Option A, history grows monotonically across releases; the single Phase-2 snapshot measurement does not account for future growth — only continuous monitoring does. | P1 |
| IT3-004 | Critical | RT-004, CV-004, FM-003, IN-001, FM-006 | nse-requirements | — | Revise NFR-006 to add a non-forgeable comparison alongside the Source-Commit: trailer check. The trailer is free-form commit message text writable by any push actor — it is adequate for detecting lazy staleness (CI failed to regenerate) but bypassable for targeted tampering. **NFR-006 revision:** "The staleness workflow SHALL perform two checks: (1) [existing] compare the Source-Commit: trailer in `git log -1 cowork-skeleton` against the SHA of the latest v* tag on main — detects lazy staleness; AND (2) [new] retrieve the expected deterministic SHA published to the GitHub Release notes for the latest v* tag (per REQ-035) and assert that `git rev-parse cowork-skeleton` equals that published SHA — detects targeted direct-push tampering regardless of the commit message contents." NFR-006 AC SHALL demonstrate both check types: (a) a stale-CI scenario (Source-Commit: trailer mismatches latest tag) triggers check (1); (b) a forged-trailer scenario (commit with Source-Commit: set to the correct SHA value but with different tree content) is caught ONLY by check (2), confirming the two checks are complementary not redundant. | P1 |
| IT3-005 | Major | CC-002, FM-008, FM-010, CV-002 (ADR portion), CV-005 | ps-architect | nse-requirements | Fix ADR-001 pseudocode and extend sanitization coverage: **(a) ADR-001 §Regeneration Commit Determinism pseudocode** — the current line 1 `TAG="${GITHUB_REF_NAME}"` is correct only for `push: tags` events. Add a `workflow_dispatch` resolution block: `TAG="${INPUT_TARGET_TAG:-${GITHUB_REF_NAME}}"` — for workflow_dispatch with inputs.target_tag, GITHUB_REF_NAME equals the triggering branch (e.g., `main`), not a tag; `inputs.target_tag` must be used instead. The combined expression `${INPUT_TARGET_TAG:-${GITHUB_REF_NAME}}` covers both cases. **(b) Blank-target-tag resolution** — extend REQ-011 body (not only the parameter description string) to specify: "When inputs.target_tag is blank, the workflow SHALL resolve the tag by executing `git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=-version:refname | head -1` against a full `fetch-depth: 0` clone. The resolved tag SHALL undergo the same allow-list validation as an explicitly-provided tag before proceeding." AC: workflow_dispatch run with blank inputs.target_tag resolves to the most recent semantic-version tag and proceeds; a run where no v* tag exists exits non-zero with a diagnostic. **(c) RT-04 sanitization note extension** — extend ADR-001 §Tag-name sanitization to explicitly state: "inputs.target_tag is attacker-influenceable by any repository collaborator with `workflow_dispatch` permission; it requires the same allow-list validation as GITHUB_REF_NAME. The combined TAG assignment MUST be validated BEFORE the tag value is used in any shell command or commit message." nse-requirements: coordinate to ensure REQ-036 (IT3-001b) and REQ-011 body update are aligned with the revised pseudocode. | P1 |
| IT3-006 | Major | DA-004, CC-001 | nse-requirements | — | Document `uv` as a CoWork system prerequisite and add recovery path: **(a) REQ-024 Tutorial** — add a "Prerequisites" step before the `claude plugin marketplace add` instruction: "The Tutorial SHALL require documentation of uv (≥ 0.5) and Python (≥ 3.9) as system prerequisites, including the uv installation command (`curl -LsSf https://astral.sh/uv/install.sh | sh` or equivalent platform-specific instruction)." **(b) REQ-027 troubleshooting** — add "`uv` not found (hook execution failure)" as a named failure mode with resolution: install uv as per prerequisites. **(c) CoWork runtime prerequisite verification** — add a note analogous to REQ-009's CI/CoWork environment split: "Before Phase 5 completion, verify that CoWork's hook execution runtime PATH includes uv by running `hooks/session-start.py` in a clean CoWork session on a reference machine. Document the result in the R-001 verification artifact (REQ-034)." Rationale: `hooks/session-start.py` invokes `uv run jerry` per REQ-004 AC and REQ-024a AC; a fresh CoWork user who installs Jerry without uv receives a hook execution failure (`uv: command not found`) with no guidance (P-021 Transparency of Limitations violation per S-007 CC-001). | P1 |
| IT3-007 | Major | DA-003 | nse-requirements | — | Reanalyze R-007b consequence rating: current risk is R-007b (direct-push exploitation) at L=3, C=4 = 12 YELLOW. S-002 Devil's Advocate (DA-003) argues the cowork-skeleton risk profile differs fundamentally from the gh-pages analogy used to justify C=4: cowork-skeleton contains executable hooks (`hooks/session-start.py`, `hooks/`), CLI source (`src/`), and auto-loading rules (`.context/rules/`). A successful direct-push attack replacing hook content could cause malicious code to execute on CoWork user workstations when a Claude Code session starts — not only data integrity impact. Evaluate: if hook execution compromise on user machines is C=5 (Catastrophic), R-007b becomes L=3, C=5 = 15 YELLOW (border-high, near RED). At L=4 (probable, e.g., if a disgruntled contributor), C=5 = 20 → RED (requires explicit stakeholder escalation per P-042). **Required action:** the requirements document SHALL include a documented reanalysis of R-007b with explicit rationale for the selected C value. If C remains 4: document why hook execution attack on user machines is classified Major (C=4) not Catastrophic (C=5) — e.g., hooks are Python scripts requiring `uv` to execute, reducing attacker reach to environments with uv. If C is raised to 5: update risk score, flag as border-RED, and document stakeholder acceptance under P-042 and AE-005 (security-relevant, auto-C3 minimum). | P1 (risk register accuracy) |

---

## Improvement Recommendations (Priority Ordered)

| Priority | ID | Dimension Impact | Current State | Target | Recommendation |
|----------|----|-----------------|---------------|--------|----------------|
| 1 | IT3-001 | Completeness, Traceability | ADR mandatory controls with no REQ backing | REQ-035, REQ-036, REQ-037 added to WS-3 | Add three new requirements for integrity gate, tag sanitization, and push-failure detection |
| 2 | IT3-002 | Internal Consistency, Methodological Rigor | In-CI gate is tautological; architecture undefined | ADR-002 describes publish+assert architecture | Revise ADR-002 to describe the 2-step non-tautological integrity gate |
| 3 | IT3-004 | Internal Consistency, Methodological Rigor | NFR-006 uses forgeable Source-Commit trailer | NFR-006 adds non-forgeable tip SHA comparison | Revise NFR-006 with dual-check (trailer for staleness + tip SHA for tampering) |
| 4 | IT3-003 | Completeness, Methodological Rigor, Evidence Quality | REQ-034 proxy-only; no pack-size threshold; single bandwidth | REQ-034d adds CoWork install smoke test; dimension (b) has threshold; clone-weight monitoring ongoing | Revise REQ-034 with 4th dimension + threshold; add CI monitoring |
| 5 | IT3-005 | Internal Consistency, Actionability | GITHUB_REF_NAME pseudocode wrong for workflow_dispatch; blank target_tag undefined | ADR-001 pseudocode corrected; REQ-011 body specifies resolution mechanism | Fix ADR-001 pseudocode; extend REQ-011 with blank-target-tag resolution procedure |
| 6 | IT3-006 | Completeness, Actionability | uv prerequisite implicit; CoWork user with no uv gets hook failure with no guidance | REQ-024 Tutorial prerequisite step; REQ-027 failure mode | Add uv to prerequisites and troubleshooting guide |
| 7 | IT3-007 | Methodological Rigor, Evidence Quality | R-007b C=4 asserted without cowork-skeleton risk profile reanalysis | Documented reanalysis with explicit C-value rationale | Perform R-007b reanalysis; document rationale for C=4 or escalate to C=5 |

---

## Anti-Leniency Statement

This scoring actively counteracts leniency bias through the following mechanisms:

**1. Ambiguous scores resolved downward.**
Completeness was in the 0.80-0.83 range. The improvements are real (REQ-024a, REQ-034, NFR-006, inputs.target_tag, marketplace.json check) but 3 Critical-class and 7 Major-class completeness gaps remain, including the ADR mandatory controls cluster. Score resolved to 0.80.

Internal Consistency was in the 0.77-0.80 range. The GITHUB_REF_NAME pseudocode error is implementation-breaking for the workflow_dispatch path (not presentational), and the NFR-006 trailer-vs-tip-SHA inconsistency with the ADR tamper-evidence claim is a material logical gap. Score resolved to 0.78 (lower bound of range, per anti-leniency rule).

**2. The +0.020 composite delta is modest relative to the scope of iteration-2 remediation.** Six items from the 20-item iteration-1 remediation list were substantially addressed. A first-impression scoring of "the fixes are significant" would inflate the delta. The remaining Critical cluster — all converging on the same root pattern (ADR prose-vs-requirements gap) — has NOT been resolved, and several strategies independently rate this cluster Critical. The modest +0.020 reflects genuine improvement without discounting the residue.

**3. Critical findings from 6 of 8 strategies are reflected in dimension scores.** Strategies S-012 FMEA (3 Criticals, total RPN 2,087) and S-013 Inversion (2 Criticals) each independently identify the pre-publication integrity gate and R-001 proxy as Critical. S-004 Pre-Mortem (3 Criticals) and S-001 Red Team (2 Criticals) do the same. Five strategies find the same root issue: the steelman (S-003) and constitutional AI (S-007) confirm the design architecture is sound, but the latter still issues 2 Major findings targeting the same gaps.

**4. Score of 0.801 is commensurate with iteration-2 first-pass revision.** The deliverables have improved meaningfully from iteration 1. But 5 unresolved Critical themes (deduplicated), 0.119 gap to the H-13 gate, and 0.149 gap to the project target position these deliverables correctly at 0.801 — in the lower REVISE band (0.70-0.84), not the near-threshold REVISE band (0.85-0.91).

**5. No dimension scored above 0.82 without specific positive evidence.** The two highest scores (Actionability 0.82, Traceability 0.82) are grounded in the concrete improvements: REQ-024a and inputs.target_tag (Actionability), and the STK-003→REQ-024a trace addition (Traceability). These scores are higher than Completeness/Internal Consistency/Methodological Rigor specifically because the iteration-2 improvements had a larger relative impact on actionability and traceability dimensions, while the residue Critical cluster primarily impacts Completeness, Internal Consistency, and Methodological Rigor.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing the weighted composite
- [x] Evidence documented for each score — specific finding IDs and content citations provided for all 6 dimensions
- [x] Uncertain scores resolved downward — Completeness (0.80 not 0.82), Internal Consistency (0.78 not 0.80); documented in anti-leniency statement
- [x] Iteration-2 calibration considered — +0.020 delta is appropriate for scope of improvements made; 5 unresolved Critical themes depress the composite
- [x] No dimension scored above 0.82 without specific positive evidence; no dimension scored above 0.95
- [x] Critical findings from S-004 Pre-Mortem (PM-001, PM-002, PM-003), S-001 Red Team (RT-001, RT-002), S-012 FMEA (FM-001, FM-002, FM-003), and S-013 Inversion (IN-001, IN-002) are reflected in dimension scores — they are not discounted because iteration-2 made other genuine improvements
- [x] Weighted composite arithmetic verified: 0.160 + 0.156 + 0.160 + 0.120 + 0.123 + 0.082 = 0.801
- [x] Verdict (REVISE) matches the 0.70-0.84 score band definition exactly

---

## Session Context

```yaml
verdict: REVISE
composite_score: 0.801
prior_score: 0.781
delta: +0.020
threshold: 0.92
target: 0.95
gap_to_gate: -0.119
gap_to_target: -0.149
weakest_dimension: Internal Consistency
weakest_score: 0.78
critical_findings_count: 5  # deduplicated unique critical themes; 11 raw across 8 strategies
iteration: 2
improvement_recommendations:
  - "IT3-001 [Critical]: Promote 3 ADR mandatory compensating controls to WS-3 SHALL requirements — REQ-035 (integrity gate), REQ-036 (tag sanitization), REQ-037 (push-failure detection)"
  - "IT3-002 [Critical]: Reframe integrity gate architecture in ADR-002 as asynchronous publish+assert (CI publishes expected SHA; NFR-006 staleness workflow asserts live tip matches)"
  - "IT3-003 [Critical]: Revise REQ-034 — add CoWork install smoke test as 4th dimension, add explicit pack-size threshold (<250 MB), add clone-weight monitoring in cowork-skeleton.yml and NFR-006"
  - "IT3-004 [Critical]: Revise NFR-006 to add non-forgeable tip-SHA comparison alongside Source-Commit trailer check; dual-check: trailer for staleness detection, SHA for tampering detection"
  - "IT3-005 [Major]: Fix ADR-001 GITHUB_REF_NAME pseudocode for workflow_dispatch path (use INPUT_TARGET_TAG:-GITHUB_REF_NAME); add blank-target-tag resolution procedure to REQ-011 body"
  - "IT3-006 [Major]: Add uv as documented CoWork system prerequisite in REQ-024 Tutorial and REQ-027 troubleshooting guide"
  - "IT3-007 [Major]: Reanalyze R-007b Consequence rating — document whether executable hook injection justifies C=5 (Catastrophic) vs maintained C=4 (Major) with explicit rationale"
dimension_scores:
  completeness: {score: 0.80, delta: +0.03}
  internal_consistency: {score: 0.78, delta: +0.02}
  methodological_rigor: {score: 0.80, delta: +0.02}
  evidence_quality: {score: 0.80, delta: +0.01}
  actionability: {score: 0.82, delta: +0.02}
  traceability: {score: 0.82, delta: +0.02}
```

---

*Generated by: jerry:adv-scorer (adv-scorer)*
*Strategy: S-014 LLM-as-Judge*
*SSOT: `.context/rules/quality-enforcement.md`*
*Project: PROJ-031-cowork-skeleton*
*Workflow: cowork-skeleton-20260626-001 / QG-1 / Iteration 2*
*Date: 2026-06-26*
*H-15 Self-Review: Applied before persistence — all six dimension scores have specific evidence from deliverables and adversary reports; iteration-1 dimension scores referenced for delta computation; weighted arithmetic verified (0.160 + 0.156 + 0.160 + 0.120 + 0.123 + 0.082 = 0.801); verdict matches score range table (0.801 in 0.70-0.84 REVISE band); anti-leniency statement explains downward resolution for Completeness (0.80) and Internal Consistency (0.78); consolidated remediation table has 7 items with stable IDs, severities, merged finding IDs from all 8 strategies, primary and align owners, and concrete fixes; P-020 compliance: deliverables not edited; P-003 compliance: no subagents spawned.*
