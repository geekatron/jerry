# Quality Score Report: PROJ-031 CoWork Skeleton — Phase 1 Design Package

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, top action item |
| [Scoring Context](#scoring-context) | Deliverables, strategy, SSOT reference |
| [Score Summary](#score-summary) | Composite vs. targets |
| [Dimension Scores](#dimension-scores) | 6-dimension table with evidence summaries |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence, gaps, improvement path |
| [Consolidated Remediation List](#consolidated-remediation-list) | Deduplicated, owner-assigned action table |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered repair actions |
| [Anti-Leniency Statement](#anti-leniency-statement) | Leniency bias counteraction record |
| [Leniency Bias Check](#leniency-bias-check) | Checklist |

---

## L0 Executive Summary

**Score:** 0.781/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.76)

**One-line assessment:** The Phase 1 design package is structurally sound and well-evidenced in its majority but falls 0.17 below the 0.95 target due to a cluster of Critical and Major gaps concentrated in five areas: R-001 verification has no machine-enforceable gate, the unprotected branch posture lacks an automatic pre-push supply-chain integrity check, the ADR-001/REQ-005 plugin surface directory lists are inconsistent, the first-run CoWork user experience is untraceable to any documentation requirement, and the commit-message idempotency guarantee contains a self-contradicting short-SHA template. Revise and re-score before Phase 2 begins.

---

## Scoring Context

| Field | Value |
|-------|-------|
| **Deliverable 1** | `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md` |
| **Deliverable 2** | `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md` |
| **Deliverable 3** | `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md` |
| **Deliverable Type** | Design Package (Requirements + Architecture Decision Records) |
| **Criticality Level** | C4 (AE-002 `.github/` changes; AE-003 new ADRs; AE-005 security-relevant CI/token handling) |
| **Quality Target** | 0.95 (project-specified; exceeds constitutional minimum of 0.92 per H-13) |
| **Gate Threshold** | 0.92 (H-13) |
| **Scoring Strategy** | S-014 (LLM-as-Judge) |
| **SSOT Reference** | `.context/rules/quality-enforcement.md` |
| **Strategies Incorporated** | 8 of 8 (S-001, S-002, S-003, S-004, S-007, S-011, S-012, S-013) |
| **Scored** | 2026-06-26 |
| **Scorer** | adv-scorer (jerry:adv-scorer) |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.781 |
| **Project Target** | 0.95 |
| **Gate Threshold (H-13)** | 0.92 |
| **Gap to Gate** | −0.139 |
| **Gap to Target** | −0.169 |
| **Verdict** | **REVISE** |
| **Strategy Findings Incorporated** | Yes — 8 strategy reports |
| **Total findings across 8 strategies** | 69 (from counts in strategy reports) |
| **Critical findings** | 14 unique themes (see Consolidated Remediation List) |
| **Major findings** | 25+ (deduplicated into ~11 consolidation groups) |
| **Iteration** | 1 |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.77 | 0.154 | 33 requirements across 5 workstreams; notable gaps in org-ruleset check, marketplace.json, first-run UX docs, staleness detection NFR, R-001 multi-dimensional verification |
| Internal Consistency | 0.20 | 0.76 | 0.152 | ADR-001/REQ-005 directory list mismatch (commands/ absent from REQ-005; src/schemas/ absent from ADR-001); short-SHA vs. 40-char contradiction in commit template; REQ-016 SHALL/Should priority inconsistency |
| Methodological Rigor | 0.20 | 0.78 | 0.156 | NASA SE format applied correctly; ADR methodology sound; but P-042 5×5 risk matrix absent, org-level ruleset analysis missing, symlink validation uses wrong environment, R-001 verification tests only file count |
| Evidence Quality | 0.15 | 0.79 | 0.1185 | 15/22 CoVe claims independently verified; code-grounded Q4 finding; first-party CI workflow verification; gaps: GITHUB_TOKEN Docs URL missing, clone weight unquantified in MB, R-001 foundational assumption user-reported only |
| Actionability | 0.15 | 0.80 | 0.120 | Concrete acceptance criteria for all 33 requirements; gaps: no response plan when REQ-006 fires, workflow_dispatch tag selection underdefined, first-run UX unspecified for CoWork context |
| Traceability | 0.10 | 0.80 | 0.080 | Full STK→REQ bidirectional matrix; ADR cross-references; gaps: STK-003 not traced to any WS-4 documentation requirement; ADR-001 stub determinism constraint not mirrored as any REQ-xxx |
| **TOTAL** | **1.00** | | **0.781** | |

**Arithmetic check:** 0.154 + 0.152 + 0.156 + 0.119 + 0.120 + 0.080 = **0.781**

---

## Detailed Dimension Analysis

### Completeness (0.77/1.00)

**Evidence for score:**

The deliverables contain 33 formal requirements across 5 workstreams, each with explicit ADIT verification methods and grouped acceptance criteria. The STK→REQ bidirectional traceability matrix is populated. The NFRs (NFR-001 through NFR-005) cover the key non-functional properties (determinism, idempotency, freshness, least-privilege, recoverability). R-001 is explicitly documented as a named risk with a verification approach and fallback strategy — demonstrating intentional scope management rather than omission.

**Gaps with source citations:**

1. STK-003 "immediately usable / H-04 bootstrap" traces only to WS-1 technical requirements (REQ-004/005/009/010). Zero traces lead to any WS-4 documentation requirement covering the post-install first-run project creation flow for a CoWork plugin user (DA-002 Critical; CC-002 Major). A user encountering `<project-required>` on first CoWork session has no documented path to resolution.

2. REQ-021 designates `cowork-skeleton` as "unprotected" but its acceptance criterion (`gh api repos/.../protection` returns HTTP 404) verifies only repository-level branch protection. Org-level GitHub rulesets (`gh api orgs/geekatron/rulesets`) are a separate mechanism and not addressed in any requirement or ADR (DA-001 Critical; FM-012 Critical).

3. REQ-005 verifies seven directories but omits `.claude-plugin/marketplace.json`, the CoWork install entry point. A valid skeleton with a missing or invalid `marketplace.json` would fail CoWork installation silently (DA-003 Major; FM-006 Major).

4. No requirement addresses external monitoring for CI non-fire. REQ-016's `if:failure()` notification only activates when the workflow runs and fails — not when the workflow never fires at all (FM-001 Critical; IN-004 Major). This leaves the skeleton potentially stale indefinitely with no detection.

5. R-001's verification approach tests only tracked file count. The CoWork limit is undocumented externally and could be size-based (MB) or clone-time-based (seconds) rather than file-count-based. If the limit is not file-count-based, the entire branch-stripping strategy fails and the verification approach would not detect this (IN-001 Critical).

6. No Dependabot requirement exists for keeping pinned Action SHAs current after REQ-017 mandates SHA-pinning. SHA-pinning without automated refresh is an incomplete supply-chain control (PM-007 Major; FM-018 Major).

7. No soft-warning threshold for file-count drift. REQ-006 hard-fails at 5,000 but there is no NFR for an early-warning band (e.g., 85% = 4,250 files) that would allow proactive intervention before a release is blocked (DA-005 Major; PM-003 Major; IN-003 Major).

**Improvement path:**
Add REQ-024a (first-run H-04 CoWork documentation), REQ-034 (R-001 multi-dimensional verification gate with machine-checkable artifact), revise REQ-021 AC to cover org-level rulesets, add marketplace.json check to REQ-005, add a staleness-detection NFR (e.g., NFR-006), add REQ-017a (Dependabot), and add a soft-warning threshold to REQ-006.

---

### Internal Consistency (0.76/1.00)

**Evidence for score:**

The three deliverables are mutually reinforcing in their core logic. REQ-012/NFR-004 are consistent (GITHUB_TOKEN, least-privilege). REQ-003/NFR-001/NFR-002 form a coherent idempotency chain. REQ-014/REQ-023 provide overlapping loop-safety coverage intentionally. ADR-001 and ADR-002 cross-reference each other correctly. The CoVe report independently verified 15 of 22 testable claims as accurate. The ADR idempotency proof (commit SHA preimage enumeration) is logically complete.

**Gaps — concrete contradictions found:**

1. **ADR-001 c-003 vs. REQ-005 directory list mismatch (CC-003 Major):** ADR-001 constraint c-003 declares the plugin surface as `.claude-plugin/`, `skills/`, `commands/`, `.claude/`, `.context/`, `hooks/`. REQ-005 verifies `.claude-plugin/`, `skills/`, `.claude/`, `.context/`, `src/`, `schemas/`, `hooks/`. The discrepancies: `commands/` appears in ADR-001 but not REQ-005; `src/` and `schemas/` appear in REQ-005 but not ADR-001. A contributor reading one document would not see the complete picture from the other.

2. **Short-SHA vs. full SHA in ADR-001 commit message template (PM-004 Major):** ADR-001 §Regeneration Commit Determinism states "with **no** build timestamp or run ID" and the idempotency proof requires all message inputs to be invariant. But the template first line reads `build(cowork-skeleton): regenerate from <tag> (<short-sha>)`. Git's `--short` flag produces variable-length output as the repository grows (7 chars → 8 chars → more), making the commit message non-invariant and silently breaking the bit-identical SHA guarantee.

3. **REQ-016 SHALL vs. "Should" priority (PM-002 Major):** REQ-016 uses "SHALL" language (Must-tier per quality-enforcement.md §Tier Vocabulary) but its Priority column reads "Should." This creates ambiguity: an implementer reading the table column would treat the requirement as optional while the body text says it is mandatory.

4. **ADR-002 Loop-Safety Argument omits release.yml (CV-002 Minor):** Guarantee #2 (listener shape) names `version-bump.yml` and `docs.yml` but omits `release.yml`, which is named in REQ-014 as one of four workflows that must not be triggered. A reviewer tracing the loop-safety argument for `release.yml` must infer it from guarantee #1 rather than finding it stated in guarantee #2.

5. **L0 file count claim (CV-004 Minor):** `phase1-requirements.md` L0 states "1,744-file tree" (precise); actual count with the stub sentinel is ~1,745. ADR-001 L0 correctly qualifies with "~". Only the requirements doc L0 makes a precise claim that is off by one.

**Improvement path:**
ps-architect: Reconcile ADR-001 c-003 directory list against REQ-005 using `plugin.json` as the single authoritative source; fix the short-SHA template to full 40-char SHA; add release.yml to ADR-002 loop-safety guarantee #2.
nse-requirements: Correct REQ-016 Priority from "Should" to "Must"; align requirements directory list with reconciled ADR-001 c-003.

---

### Methodological Rigor (0.78/1.00)

**Evidence for score:**

The requirements apply NASA NPR 7123.1D Process 1 and Process 2 methodology correctly: stakeholder needs elicitation, formal SHALL statements, ADIT verification methods, bidirectional traceability. The ADRs follow Michael Nygard's ADR format with L0/L1/L2 structure, option comparison, steelmanned alternatives, and explicit constraint tables. S-010 Self-Refine is applied (documented in all three deliverables). H-16 Steelman-before-Devil's-Advocate is complied with. AE-002, AE-003, AE-005 auto-escalation rules are correctly identified. The C4 quality gate (≥0.95) is correctly specified. The three-guarantee loop-safety argument structure is methodologically sound. The idempotency proof is logically complete (independently verified by S-011).

**Gaps:**

1. **P-042 risk format missing (CC-001 Major):** The Risk Implications section uses qualitative notation ("M × Critical", "L × High") rather than the required P-042 5×5 numeric scoring (Likelihood 1-5 × Consequence 1-5 = numeric score). No RED/YELLOW/GREEN classification exists. R-001 at approximately Likelihood 3 × Consequence 5 = 15 sits on the YELLOW/RED boundary and cannot be properly escalated without numeric scoring.

2. **Org-level ruleset analysis absent (DA-001 Critical):** REQ-021's methodology analyzes only repository-level branch protection. GitHub organization rulesets (a separate protection mechanism introduced in 2023-2024) are neither analyzed in ADR-002 nor tested by any acceptance criterion. A pre-implementation check for existing org rulesets is a standard CI security analysis step that is missing.

3. **Input sanitization methodology absent (RT-04 Major):** The commit message template embeds `github.ref_name` (tag name), which is an untrusted, attacker-controllable value. SSDF/GitHub Actions security best practice requires sanitizing untrusted context values against a strict character set and passing them as environment variables rather than inline shell expressions. No requirement mandates tag name validation or shell-injection prevention.

4. **Symlink validation in wrong environment (PM-006 Major; IN-005 Major):** REQ-009 tests symlink resolution using `readlink -f` in the CI runner environment. CoWork installs the plugin to `~/.claude/plugins/cache/`. These are different directory layouts. Symlinks that resolve in a CI flat-checkout may not resolve in the CoWork cache path, particularly on Windows where `core.symlinks=false` causes git to store symlinks as text files.

5. **R-001 verification methodology narrow (IN-001 Critical):** The verification approach tests only tracked file count. CoWork's limit could be total repository size (MB), total git object count, or clone time (seconds against a 120-second timeout). None of these alternative limit dimensions are tested by the current R-001 verification approach. A verification methodology that falsifies only one of four possible limit types leaves the core assumption substantially unvalidated.

**Improvement path:**
nse-requirements: Add P-042 numeric risk scoring to Risk Implications section; expand R-001 verification approach to three dimensions (file count, compressed pack size, clone time); add REQ-009 cross-platform scope note; add tag name validation requirement. ps-architect: Add input sanitization security note to ADR-001; add org-level ruleset check to ADR-002 pre-implementation prerequisites.

---

### Evidence Quality (0.79/1.00)

**Evidence for score:**

The deliverables are grounded in first-party, independently verifiable evidence. The S-011 Chain-of-Verification independently read `.github/workflows/version-bump.yml`, `.github/workflows/docs.yml`, and `.github/workflows/release.yml` and verified the trigger configurations cited in ADR-002 and REQ-014. The Q4 research finding (FilesystemProjectAdapter.scan_projects RepositoryError) is code-grounded to specific file lines (52-53). The idempotency proof's enumeration of git commit SHA inputs is verified against git object model documentation. The `docs.yml` force-push pattern is verified as matching the proposed ADR-001 mechanism.

**Gaps:**

1. **GITHUB_TOKEN citation lacks URL (CV-005 Minor):** ADR-002's loop-safety guarantee #3 quotes GitHub: "events triggered by the `GITHUB_TOKEN`... will not create a new workflow run." The citation is "GitHub Docs" with no URL, no page title, and no access date. For a C4 security-critical deliverable where this guarantee is one of three independent invariants preventing an infinite CI loop, the citation must be traceable to a specific, stable URL.

2. **Clone weight unquantified in MB (DA-004 Major):** ADR-001 accepts the clone-weight risk of `fetch-depth: 0` as "LOW-MED" but provides no measurement: the compressed pack size of `main`'s git history in MB is not recorded, no estimated clone time on a reference network is documented, and no threshold is defined for switching to Option B (orphan branch). The risk classification is qualitative without quantitative backing.

3. **R-001 foundational assumption externally undocumented (IN-001 Critical):** The entire project strategy rests on the assumption that CoWork's ~5,000-file limit applies to the clean-clone tracked-file tree. This assumption is described as "confirmed absent from Anthropic's Claude Code plugin documentation" and sourced to "user-reported." The evidence for the specific mechanism of the limit is not in any Anthropic document and was not confirmed through empirical testing before Phase 1. The deliverable honestly discloses this gap (R-001 section), which is a positive signal, but the evidence quality for the core premise remains low.

4. **"88 agents, 2 commands" count in REQ-005 rationale unverified (CV-006 Minor):** The rationale cites specific quantities but no acceptance criterion verifies these counts, and the counts may drift across releases. The rationale uses the counts as qualitative support but they constitute an unsupported claim in the context of a C4 document.

**Improvement path:**
ps-architect: Add specific GitHub Docs URL with page title and access date to ADR-002 References; add measured pack-size estimate for `main`'s git history to ADR-001 Negative Consequences.
nse-requirements: Add clone size and clone time measurements to R-001 verification approach; change REQ-005 rationale from specific count to "all agents and commands declared in `.claude-plugin/plugin.json`."

---

### Actionability (0.80/1.00)

**Evidence for score:**

Every requirement has a concrete acceptance criterion with a specific observable artifact or measurement. V-methods (Test, Inspection, Demonstration, Analysis) are correctly assigned per NASA ADIT convention. REQ-001 through REQ-033 all have acceptance criteria that a V&V practitioner can execute. The ADRs provide concrete decisions with rationale — an engineer can implement the skeleton generation following Option A (4 git commands) without ambiguity about the core approach. The approval gate sequence (AG-01 through AG-10) is named and sequenced. Option B orphan fallback is pre-designed.

**Gaps:**

1. **First-run CoWork UX scenario has no actionable guidance (DA-002 Critical):** A first-time CoWork plugin user who installs the skeleton and encounters `<project-required>` from the SessionStart hook has no documented path. The tutorial (REQ-024-REQ-026) covers installation and troubleshooting but nothing tells this user "run `jerry session start` or use `/worktracker` to create your first project." The scenario is structurally untestable given the current requirements.

2. **No response plan when REQ-006 fires (DA-005 Major):** REQ-006 requires the script to exit non-zero when file count exceeds 5,000, but no requirement documents what to do when this happens: which directory to strip first, in what order, and who is responsible for the decision. An implementer facing a REQ-006 failure in a time-sensitive release context has no documented remediation procedure.

3. **workflow_dispatch tag selection underdefined (DA-006 Minor; FM-002 Critical):** REQ-018 tests "triggered twice for the same tag" but REQ-011 does not specify how the operator communicates which tag to target. Without an `inputs.target_tag` parameter, `workflow_dispatch` has no mechanism for targeting a specific past release. NFR-005 ("re-runnable at any time for any past tag") is not achievable without this.

4. **Branch protection drift has no runtime detection (FM-012 Critical):** ADR-002 documents upgrade paths (ruleset bypass, GitHub App) if org policy mandates protection, but no pre-push diagnostic step is specified that would produce an actionable error message when protection exists. A maintainer encountering CI failure due to a new org policy would not know to consult ADR-002.

**Improvement path:**
nse-requirements: Add REQ-024a for first-run H-04 documentation; add ordered strip-priority response plan to REQ-006 or a companion note; add `inputs.target_tag` to REQ-011. ps-architect: Add pre-push branch-protection diagnostic to ADR-002 as a recommended CI step.

---

### Traceability (0.80/1.00)

**Evidence for score:**

The Traceability Summary provides a complete bidirectional matrix from STK-001 through STK-006 down to all 33 requirements. Every requirement traces to at least one STK-xxx need. The Allocation Matrix maps every requirement to an implementation component (script, workflow, documentation, quality gate). ADR-001 and ADR-002 each have a References table citing primary, secondary, and first-party sources with explicit section pointers. ADR cross-references between ADR-001 and ADR-002 are bidirectional. The risk register connects risks to requirements.

**Gaps:**

1. **STK-003 → WS-4 trace absent (CC-002 Major; DA-002 Critical):** STK-003 states "immediately usable: H-04 bootstrap and SessionStart hook must function from the first session." The Traceability Summary shows four traces from STK-003, all pointing to WS-1 technical requirements. Zero traces point to any WS-4 documentation requirement. The tutorial (REQ-026) is not listed as satisfying any part of STK-003. A user-facing gap (no documented H-04 first-run flow) has no traceability path to the stakeholder need it would satisfy.

2. **ADR-001 stub determinism constraint not mirrored in any requirement (DA-007 Major; IN-007 Minor):** ADR-001 §Regeneration Commit Determinism states the stub MUST be static content. No REQ-xxx SHALL statement captures this constraint. STORY-002 is assigned stub authoring without a traceability link to a binding requirement. A reviewer auditing REQ-003 (bit-identical SHA) would not discover the stub dependency through requirements alone.

3. **ADR-002 Loop-Safety Argument coverage gap vs. REQ-014 (CV-002 Minor):** REQ-014 names four workflows that must not be triggered (cowork-skeleton.yml, release.yml, version-bump.yml, docs.yml). ADR-002 §Loop-Safety Argument guarantee #2 names only two workflows (version-bump.yml, docs.yml). A reader tracing REQ-014 coverage through ADR-002 cannot confirm release.yml is addressed without inferring it from guarantee #1.

4. **Direct-push attack vector not in risk register (CC-004 Minor):** R-007 in the Risk Implications table scopes supply-chain risk to "CI compromised." The distinct threat of a repository collaborator pushing directly to the unprotected `cowork-skeleton` branch — without CI involvement — is not listed as a sub-vector in R-007, creating a gap between the threat model and the requirement that unprotected posture (REQ-021) is meant to address.

**Improvement path:**
nse-requirements: Update Traceability Summary to add STK-003 → REQ-024a; add a formal stub static-content requirement in WS-1 with a trace from ADR-001; expand R-007 threat description; fix REQ-016 priority.
ps-architect: Add release.yml to ADR-002 Loop-Safety Argument guarantee #2; add forward reference from ADR-001 stub constraint to the new WS-1 requirement.

---

## Consolidated Remediation List

Each item merges all adversary findings pointing to the same root issue. Finding IDs listed are from the strategy reports (SM = Steelman, DA = Devil's Advocate, PM = Pre-Mortem, RT = Red Team, CC = Constitutional, CV = Chain-of-Verification, FM = FMEA, IN = Inversion).

| REM-ID | Severity | Merged Finding IDs | Owner | Fix |
|--------|----------|--------------------|-------|-----|
| REM-001 | Critical | PM-001, RT-06, CV-001, FM-019, FM-020, IN-001 | nse-requirements | Add REQ-034: "Before Phase 2 begins, a `verification/R001-clean-clone-count.md` artifact SHALL be created recording: (a) tracked file count on a clean clone of `main`, (b) total compressed pack size via `git count-objects -vH`, (c) clone time on a reference network, (d) whether the CoWork file-limit error reproduces on a clean-machine install of `main`." Expand R-001 §Verification Approach to document all three dimensions. The artifact MUST exist before Phase 5 scripts can execute. |
| REM-002 | Critical | DA-001, FM-012 | both (nse-requirements + ps-architect) | nse-requirements: Revise REQ-021 AC to include: "Confirm `gh api orgs/geekatron/rulesets` returns no ruleset restricting force-push to `cowork-skeleton`." Run this check before Phase 2. ps-architect: Add org-level ruleset verification as a pre-implementation prerequisite in ADR-002 §Branch-Protection Posture; document bypass options if a ruleset exists. |
| REM-003 | Critical | RT-01, IN-002, PM-005 | both (nse-requirements + ps-architect) | ps-architect: Revise ADR-002 §Branch-Protection Posture to recommend a GitHub ruleset on `cowork-skeleton` that (a) allows only `github-actions[bot]` to force-push and (b) blocks direct pushes from all other actors. Confirm this is compatible with GITHUB_TOKEN as the bypass actor. nse-requirements: Add a requirement (or revise REQ-021) mandating this ruleset, or document the accepted risk with explicit user approval. |
| REM-004 | Critical | DA-002, CC-002 | nse-requirements | Add REQ-024a: "The Tutorial SHALL include a step covering the H-04 first-run experience: what a CoWork plugin user sees when no active project exists (`<project-required>` from SessionStart hook) and how to create their first project using `/worktracker` or `jerry session start`." Update Traceability Summary: STK-003 → REQ-024a. Extend REQ-004 AC to test functional H-04 flow (not just no-crash). |
| REM-005 | Critical | RT-05, FM-017, IN-002 | nse-requirements | Revise REQ-022 AC: the `git diff v{N}..cowork-skeleton` equivalence check SHALL be an in-workflow automated step that runs BEFORE the force-push. If the diff is non-empty, the job exits non-zero and no push occurs. Change "after each CI run" to "pre-push gate within `cowork-skeleton.yml`." |
| REM-006 | Critical | FM-001, PM-002, IN-004 | nse-requirements | (a) Correct REQ-016 Priority from "Should" to "Must" to match its "SHALL" language. (b) Add NFR-006: "A staleness-detection workflow SHALL run at minimum weekly. It SHALL compare the `Source-Commit:` trailer in `git log -1 cowork-skeleton` to the SHA of the latest `v*` tag and fail visibly if they diverge, producing a GitHub notification or issue." |
| REM-007 | Critical | FM-002, DA-006 | nse-requirements | Revise REQ-011: "The `workflow_dispatch` trigger SHALL declare an optional `inputs.target_tag` parameter (description: 'v* release tag to regenerate from; defaults to latest if blank') so operators can target specific past tags." Revise REQ-018 AC to reference this input. This resolves NFR-005 ("re-runnable at any time for any past tag"). |
| REM-008 | Major | CC-003, DA-003, FM-006 | both (ps-architect + nse-requirements) | ps-architect: Revise ADR-001 constraint c-003 to use the canonical directory list derived from `.claude-plugin/plugin.json`. Confirm whether `commands/` exists in the repo. nse-requirements: Revise REQ-005 to use the same canonical list. Add to REQ-005 AC: "`git ls-files .claude-plugin/marketplace.json` returns non-empty." Clarify in REQ-005 rationale which directories are CoWork-plugin-surface vs. Jerry-CLI-required. |
| REM-009 | Major | PM-004, FM-010 | ps-architect | In ADR-001 §Regeneration Commit Determinism, change the commit message template subject line from `(<short-sha>)` to either the full 40-char SHA or `(<short-8-sha>)` with explicit `--short=8` flag. Add a note that the implementation in STORY-001 MUST use a fixed-length hash. Optionally add a CI assertion that regenerating the same tag twice produces an identical commit SHA across separate CI runs. |
| REM-010 | Major | DA-007, PM-008, CV-003, IN-007, FM-008 | both (nse-requirements + ps-architect) | nse-requirements: Add to WS-1 (or as REQ-003 sub-clause): "The `projects/README.md` sentinel SHALL contain only static prose — no timestamps, version strings, build identifiers, or generated values." Revise REQ-003 AC to require a cross-run idempotency test: two separate `workflow_dispatch` runs at different times for the same tag must produce an identical commit SHA. ps-architect: Add a forward reference from ADR-001 §Stub Determinism Constraint to this new requirement. |
| REM-011 | Major | CC-001 | nse-requirements | Replace the qualitative risk notation in the Risk Implications section with a full P-042 5×5 numeric matrix: define Likelihood (1=Rare, 5=Almost Certain) and Consequence (1=Negligible, 5=Critical) scales; compute numeric L×C score for each risk; add RED/YELLOW/GREEN column (>15=RED, 8-15=YELLOW, <8=GREEN). Escalate any RED risks (estimated: R-001 at 3×5=15, borderline RED/YELLOW) to explicit user attention per P-042. |
| REM-012 | Major | PM-007, FM-018 | nse-requirements | Add REQ-017a: "A Dependabot configuration (`package-ecosystem: github-actions`, `directory: /`) SHALL exist in `.github/dependabot.yml` covering `cowork-skeleton.yml`, producing automated PRs when upstream GitHub Action SHA pins become stale." Verify Dependabot is enabled for the repository before Phase 6 sign-off. |
| REM-013 | Major | SM-001, RT-02 | ps-architect | In ADR-001 §Consequences > Positive (or §Regeneration Commit Determinism), add an explicit tamper-detection paragraph: "Because `regenerate(T)` is a pure function, the expected commit SHA for any given release tag is computable independently. A SHA mismatch on the live `cowork-skeleton` branch is detectable by re-running the generator against the same tag and comparing — making the branch tamper-evident without additional attestation infrastructure." Consider publishing the expected SHA for each release in the GitHub Release notes (REQ-022 companion action). |
| REM-014 | Major | PM-006, FM-014, IN-005 | nse-requirements | Add to REQ-009: a note that the CI-level `readlink -f` test verifies the Linux CI environment only. Add to R-001 §Verification Approach: "Before Phase 5 completion: confirm `.claude/rules/` auto-loading functions correctly in an actual CoWork session (not just a CI `readlink -f` check)." Add to REQ-027 troubleshooting guide: Windows `core.symlinks=false` behavior as a known failure mode with the `git config core.symlinks true` workaround. |
| REM-015 | Major | DA-005, PM-003, IN-003 | nse-requirements | Add to REQ-006 (or a new NFR-006 sub-clause): "The generation script SHALL emit a structured warning (non-fatal) to `$GITHUB_STEP_SUMMARY` when the generated file count exceeds 4,250 (85% of the 5,000 ceiling) with a per-directory breakdown." Document the priority order for additional stripping (e.g., `skills/transcript/test_data/`, `tests/`, `docs/archive/`) if the count exceeds 4,250. |
| REM-016 | Minor | RT-04 | ps-architect | Add a security note to ADR-001 §Regeneration Commit Determinism: "The tag name (`github.ref_name`) MUST be validated in the generation script against the pattern `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` before use, and MUST be passed as a shell environment variable rather than embedded inline in git command strings, to prevent shell injection and commit-message trailer injection." |
| REM-017 | Minor | CV-005 | ps-architect | Add the specific GitHub Docs URL and access date for the GITHUB_TOKEN non-retrigger guarantee to ADR-002 References table. Suggested: "GitHub Docs — Triggering a workflow — Using the default GITHUB_TOKEN — https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/triggering-a-workflow#triggering-a-workflow-from-a-workflow [accessed 2026-06-26]." |
| REM-018 | Minor | CV-002 | ps-architect | Expand ADR-002 §Loop-Safety Argument guarantee #2 to explicitly name `release.yml`: "`release.yml` listens on `push: tags: 'v*'` only. A branch push to `cowork-skeleton` (neither `main` nor a tag) is invisible to all three watched workflows." |
| REM-019 | Minor | SM-001, CC-005 | nse-requirements | Update all acceptance criteria in WS-1 through WS-3 that reference Jerry CLI invocations to use `uv run jerry <subcommand>` (e.g., REQ-004 AC: "…`uv run jerry projects list` exits 0"). Add a note to WS-5 that V&V test scripts MUST use `uv run jerry` for any CLI invocation (H-05 compliance). |
| REM-020 | Minor | CV-004 | nse-requirements | Change `phase1-requirements.md` L0 Executive Summary from "1,744-file tree" to "approximately 1,744 tracked files (approximately 1,745 including the `projects/README.md` sentinel stub)" to align with REQ-002's "approximately" qualifier and the actual arithmetic. |

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | REM-ID | Current | Target | Recommendation |
|----------|-----------|--------|---------|--------|----------------|
| 1 | Completeness | REM-001 | R-001: process-only gate | REQ-034 with machine-checkable artifact | Create `verification/R001-clean-clone-count.md` as a mandatory prerequisite for Phase 5; expand verification to 3 dimensions |
| 2 | Completeness | REM-004 | No WS-4 requirement for first-run H-04 UX | REQ-024a added; STK-003 → REQ-024a trace | Add Tutorial requirement for CoWork first-project creation flow |
| 3 | Methodological Rigor | REM-002 | REQ-021 verifies repo-level only | REQ-021 AC covers org+repo rulesets | Run `gh api orgs/geekatron/rulesets` before Phase 2; update REQ-021 |
| 4 | Completeness / Traceability | REM-003 | Unprotected branch, no push-time gate | Branch ruleset or documented accepted risk | ps-architect revises ADR-002; nse-requirements revises REQ-021 posture |
| 5 | Completeness | REM-005 | REQ-022 AC: "after each CI run" (post-push, manual) | Automated pre-push gate in workflow | Revise REQ-022 AC to specify pre-push ordering |
| 6 | Completeness | REM-006 | REQ-016 priority "Should"; no staleness detection | REQ-016 priority "Must"; NFR-006 staleness probe | Correct priority; add scheduled staleness-detection workflow requirement |
| 7 | Actionability | REM-007 | workflow_dispatch: no tag input defined | REQ-011 specifies `inputs.target_tag` | Add `inputs.target_tag` optional parameter to REQ-011 |
| 8 | Internal Consistency | REM-008 | ADR-001 c-003 and REQ-005 use different directory lists | Single canonical list from `plugin.json` | Both owners reconcile; add marketplace.json check |
| 9 | Internal Consistency | REM-009 | Short-SHA in commit template vs. 40-char in proof | Full 40-char or fixed `--short=8` in template | ps-architect fixes ADR-001 template |
| 10 | Traceability / Completeness | REM-010 | Stub constraint: ADR-only, no SHA, no cross-run test | Formal SHALL requirement; cross-run REQ-003 AC | nse-requirements adds requirement; ps-architect adds forward reference |
| 11 | Methodological Rigor | REM-011 | Risk table: qualitative "M × Critical" | P-042 5×5 numeric scoring with RED/YELLOW/GREEN | nse-requirements reformats Risk Implications section |
| 12 | Methodological Rigor | REM-012 | No Dependabot for Actions | REQ-017a: Dependabot github-actions entry | nse-requirements adds REQ-017a |
| 13 | Evidence Quality | REM-013 | Tamper-detection argument only in requirements, not ADR-001 | Explicit tamper-detection paragraph in ADR-001 | ps-architect adds paragraph |
| 14 | Methodological Rigor | REM-014 | REQ-009 tests CI environment only; no cross-platform note | R-001 verification includes CoWork runtime symlink test; REQ-027 Windows note | nse-requirements amends REQ-009 and REQ-027 |
| 15 | Completeness | REM-015 | REQ-006 hard-fails at 5,000; no early warning | 85% soft-warning band; per-directory job summary | nse-requirements adds soft-warning to REQ-006 |
| 16 | Methodological Rigor | REM-016 | No tag name validation requirement | Security note and pattern validation in ADR-001 | ps-architect adds to ADR-001 §Determinism |
| 17 | Evidence Quality | REM-017 | GITHUB_TOKEN citation: "GitHub Docs" only | Full URL with access date in ADR-002 References | ps-architect updates References |
| 18 | Traceability | REM-018 | Loop-safety guarantee #2 omits release.yml | release.yml added to guarantee #2 | ps-architect one-line fix |
| 19 | Completeness | REM-019 | `jerry` in AC text without `uv run` | `uv run jerry` in all AC CLI references | nse-requirements updates AC text |
| 20 | Internal Consistency | REM-020 | L0: "1,744-file tree" (precise) | L0: "approximately 1,744 tracked files (~1,745 with stub)" | nse-requirements one-line fix |

---

## Anti-Leniency Statement

This scoring resists leniency bias through the following active counteractions:

1. **Ambiguous score resolved downward.** Internal Consistency was borderline between 0.77 (lower end of "minor inconsistencies" band) and 0.73 (upper end of "some contradictions" band). The 3 Major contradictions — cross-document directory list mismatch (CC-003), intra-document short-SHA vs. 40-char contradiction (PM-004), and SHALL vs. Should priority mismatch (PM-002) — are concrete, verifiable, and cross multiple deliverables. Score resolved to 0.76.

2. **First-draft calibration applied.** The score of 0.781 falls in the 0.65-0.80 typical first-draft range. Despite high quality in structure and format, the deliverables contain 14 Critical-severity findings across 8 independent adversary strategies. These are not presentational issues — they represent missing requirements (REM-004, REM-007), unverified assumptions with no technical gate (REM-001), incomplete security analysis (REM-002, REM-003), and self-contradicting technical specifications (REM-009, REM-010). A first design package at 0.78 is appropriate.

3. **No dimension scored above 0.80 without specific evidence.** The highest scores (Actionability 0.80, Traceability 0.80) are justified by: concrete acceptance criteria on all 33 requirements and a complete STK→REQ bidirectional matrix. These strengths are real but the gaps (REM-004, REM-007 for Actionability; REM-010, CC-002 for Traceability) prevent higher scores.

4. **Critical findings from adversary reports did not inflate scores.** The S-001 Red Team identified two Critical findings (RT-01: unprotected branch allows direct malicious write; RT-02: no user-verifiable install integrity) that directly reduce Methodological Rigor and Completeness. These were scored independently before reading the S-003 Steelman and S-007 Constitutional AI reports, which acknowledged the same strengths from a positive framing. The underlying issues remain regardless of the steelman.

5. **Score is 0.781, not rounded up to 0.80.** The mathematical result is 0.781. Rounding to "approximately 0.78" for communication, but 0.781 is the precise weighted composite.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing the weighted composite
- [x] Evidence documented for each score (specific finding IDs and content citations)
- [x] Uncertain scores resolved downward (Internal Consistency: 0.76 not 0.77; see anti-leniency statement)
- [x] First-draft calibration considered (0.65-0.80 typical first-draft range; 0.781 falls within it)
- [x] No dimension scored above 0.80 without specific positive evidence; none scored above 0.95
- [x] Critical findings from Red Team (RT-01, RT-02) and FMEA (FM-001, FM-002, FM-009, FM-012, FM-019, FM-020) are reflected in dimension scores, not discounted because other dimensions are strong

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.781
threshold: 0.92
target: 0.95
weakest_dimension: Internal Consistency
weakest_score: 0.76
critical_findings_count: 14
iteration: 1
improvement_recommendations:
  - "REM-001: Add REQ-034 (R-001 machine-checkable verification artifact) before Phase 2"
  - "REM-002: Run org-level ruleset check; update REQ-021 AC"
  - "REM-003: Add branch ruleset or document accepted risk for unprotected cowork-skeleton"
  - "REM-004: Add REQ-024a for H-04 first-run CoWork user experience"
  - "REM-005: Revise REQ-022 AC to pre-push automated gate"
  - "REM-006: Correct REQ-016 priority to Must; add staleness detection NFR-006"
  - "REM-007: Add inputs.target_tag to workflow_dispatch trigger (REQ-011)"
  - "REM-008: Reconcile ADR-001 c-003 / REQ-005 directory lists; add marketplace.json check"
  - "REM-009: Fix short-SHA in commit message template to full 40-char SHA"
  - "REM-010: Add formal stub static-content SHALL requirement; cross-run REQ-003 AC"
```

---

*Generated by:* jerry:adv-scorer (adv-scorer)
*Strategy:* S-014 LLM-as-Judge
*SSOT:* `.context/rules/quality-enforcement.md`
*Project:* PROJ-031-cowork-skeleton
*Workflow:* cowork-skeleton-20260626-001 / QG-1 / Iteration 1
*Date:* 2026-06-26
*H-15 Self-Review:* Applied before persistence — all six dimension scores have specific evidence from deliverables and adversary reports; weighted arithmetic verified (0.154 + 0.152 + 0.156 + 0.119 + 0.120 + 0.080 = 0.781); verdict matches score range table (0.781 in REVISE band 0.70-0.84); anti-leniency statement explains downward resolution of uncertain scores; consolidated remediation table has 20 items with stable IDs, severities, merged finding IDs, owners, and concrete fixes; no finding omitted per P-022.
