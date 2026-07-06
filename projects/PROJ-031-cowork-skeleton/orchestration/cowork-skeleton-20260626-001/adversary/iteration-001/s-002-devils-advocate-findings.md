# Devil's Advocate Report: PROJ-031 Phase 1 Requirements and ADRs 001/002

**Strategy:** S-002 Devil's Advocate
**Deliverables:**
- `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md`
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md`
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md`
**Criticality:** C4
**Date:** 2026-06-26
**Reviewer:** adv-executor — jerry:adv-executor (S-002)
**H-16 Compliance:** S-003 Steelman confirmed applied — `iteration-001/s-003-steelman-findings.md` exists (verified via directory listing; content not read per blindness constraint)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All 7 findings with severity and affected dimension |
| [Detailed Findings](#detailed-findings) | Full DA-001 through DA-007 with evidence, analysis, and response requirements |
| [Recommendations](#recommendations) | P0, P1, P2 action list with acceptance criteria |
| [Scoring Impact](#scoring-impact) | S-014 dimension-level assessment |

---

## Summary

Seven counter-arguments identified (2 Critical, 4 Major, 1 Minor). The core skeleton strategy is sound, but two gaps could block Phase 5 before implementation begins: the GITHUB_TOKEN force-push analysis (ADR-002) does not address organization-level GitHub rulesets — the REQ-021 acceptance criterion only verifies repo-level branch protection and would pass even if an org ruleset is already blocking force-push; and the H-04 bootstrap story (REQ-004) demonstrates only that `jerry projects list` does not crash, not that a first-time CoWork plugin user can complete the full JERRY_PROJECT first-run workflow. Four Major findings cover the 7-directory plugin-load claim (includes non-plugin-surface dirs, omits marketplace.json), overstated provenance benefit for a tip-tree CoWork install with unquantified clone-weight risk, absent proactive file-count drift governance, and an unenforced stub-content static-content constraint deferred to STORY-002 without Phase 1 acceptance criteria. **Recommend REVISE — address Critical findings before Phase 2 proceeds.**

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260626 | Org-level GitHub rulesets not checked — REQ-021 AC verifies repo-level only; org rulesets can already block GITHUB_TOKEN force-push | Critical | REQ-021 AC: `gh api repos/.../branches/cowork-skeleton/protection returns HTTP 404`; ADR-002 risks: "Org policy later mandates protection → LOW" — no org-level check documented | Methodological Rigor |
| DA-002-20260626 | H-04 bootstrap incomplete — stub prevents RepositoryError but full JERRY_PROJECT first-run workflow in CoWork context is undocumented and unverified | Critical | REQ-004 AC: "jerry projects list exits 0 and prints 'No projects found'" — no-crash test only; WS-4 docs requirements omit first-run project-creation guide | Completeness |
| DA-003-20260626 | 7-directory check conflates Jerry-CLI-required dirs (schemas/, src/) with CoWork-plugin-surface dirs; marketplace.json unchecked | Major | REQ-005 rationale: "plugin surface (88 agents, skills tree, 2 commands)"; marketplace.json is the CoWork install entry point and is not verified | Methodological Rigor |
| DA-004-20260626 | Full-history "strong provenance" benefit overstated for tip-tree CoWork install; 120-second clone-weight timeout risk never quantified | Major | ADR-001 L0: "plugin install clones branch and materializes working tree at tip commit"; ADR-001 Decision: "git log and git diff work" — but history is not accessible to CoWork plugin users | Evidence Quality |
| DA-005-20260626 | No proactive file-count drift governance — REQ-006 hard-fail fires only during CI; no monitoring mechanism between releases | Major | REQ-006 AC: "script exits non-zero if count >= 5,000" (reactive only); ADR-001 L2 ¶5: future stripping candidates listed with no governance trigger defined | Completeness |
| DA-006-20260626 | workflow_dispatch trigger lacks explicit tag-selection input; REQ-018 "same tag" acceptance test is underdefined | Minor | REQ-018 AC: "workflow_dispatch triggered twice for the same tag" — operator cannot specify which tag without an `inputs:` block | Actionability |
| DA-007-20260626 | Stub static-content constraint deferred to STORY-002 without Phase 1 enforcement; REQ-003 acceptance test does not catch dynamic content across runs | Major | ADR-001 Determinism: "stub MUST be static content. Authoring is STORY-002; this ADR fixes only its determinism property"; REQ-003 AC same-run test would pass even with dynamic content | Traceability |

---

## Detailed Findings

### DA-001-20260626: Org-Level GitHub Rulesets Not Checked [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Deliverables** | ADR-002 §Branch-Protection Posture; phase1-requirements REQ-021 |
| **Strategy Step** | Step 2 (Assumption Challenge) + Step 3 (Unstated Assumptions lens) |

**Claim Challenged:**
> ADR-002 §Branch-Protection Posture: "Recommended posture: `cowork-skeleton` is UNPROTECTED, exactly like `gh-pages`."
> REQ-021 acceptance criterion: "`gh api repos/geekatron/jerry/branches/cowork-skeleton/protection` returns HTTP 404 (no protection configured)."

**Counter-Argument:**
GitHub has two distinct protection mechanisms that operate independently: repository-level branch protection rules (what ADR-002 analyzes and REQ-021 tests) and organization-level rulesets (a separate feature introduced in 2023 and generally available in 2024). Organization rulesets apply across ALL repositories in the organization unless branches are explicitly excluded. They can require status checks, forbid force-push, require linear history, and override a repository-level "unprotected" configuration. The `gh api repos/{owner}/{repo}/branches/{branch}/protection` endpoint — the one REQ-021 tests — reports ONLY repository-level branch protection. It returns HTTP 404 even if an org-level ruleset is actively restricting the branch.

The deliverables never: (1) check whether the `geekatron` org has active rulesets (`gh api orgs/geekatron/rulesets`); (2) verify that the `docs.yml`/`gh-pages` force-push precedent succeeds DESPITE any org rulesets; (3) require that `cowork-skeleton` be explicitly exempted from any applicable org rulesets as a pre-Phase-5 setup step.

ADR-002 §Risks acknowledges "Org policy later mandates protection on all branches → LOW | MED" as a FUTURE risk. But this is not only a future risk — if the `geekatron` org has an existing ruleset, the CI workflow would fail on its first live run, after all Phase 1–4 work is complete. This failure would not be caught by the REQ-021 acceptance criterion.

**Impact:** If a `geekatron` org ruleset already restricts `GITHUB_TOKEN` force-push, `cowork-skeleton.yml` fails on its first execution — after the full planning and requirements phase. This is a testable, pre-implementation verification gap, not a speculative risk.

**Dimension:** Methodological Rigor

**Response Required:** Before Phase 2 proceeds: (1) Run `gh api orgs/geekatron/rulesets` and document all active org-level rulesets. Confirm none restrict force-push to branches matching `cowork-skeleton`. (2) If a ruleset applies, document the bypass mechanism (ruleset exemption for the Actions actor, or GitHub App token upgrade per ADR-002 Option C) and add it as a mandatory Phase 6 prerequisite. (3) Revise REQ-021 acceptance criterion to include an org-level check: "Confirm no active org ruleset restricts GITHUB_TOKEN force-push to `cowork-skeleton`."

**Acceptance Criteria:** Phase 1 deliverables include a documented org-ruleset check result; REQ-021 acceptance criterion verifies both repo-level and org-level protection status.

---

### DA-002-20260626: H-04 Bootstrap Incomplete — First-Run JERRY_PROJECT Workflow Unverified [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Deliverables** | phase1-requirements REQ-004, STK-003, WS-4 (REQ-024–REQ-029) |
| **Strategy Step** | Step 2 (Assumption Challenge) + Step 3 (Unaddressed Risks lens) |

**Claim Challenged:**
> STK-003: "A fresh install of the plugin must be immediately usable: H-04 bootstrap (active-project requirement) and SessionStart hook must function from the first session."
> REQ-004 acceptance criterion: "On a clean clone of `cowork-skeleton`: `git ls-files projects/README.md` returns non-empty; `jerry projects list` exits 0 and prints 'No projects found.'"

**Counter-Argument:**
REQ-004 verifies that `jerry projects list` does not raise a `RepositoryError`. This is the no-crash precondition for H-04, not a demonstration that H-04 FUNCTIONS. H-04 states: "Active project REQUIRED. MUST NOT proceed without JERRY_PROJECT set."

In a real CoWork plugin session: (1) the plugin is loaded from `~/.claude/plugins/cache/geekatron-jerry@cowork-skeleton` (a read-only cache location); (2) a new user's session starts, JERRY_PROJECT is not set; (3) SessionStart hook returns `<project-required>` per CLAUDE.md; (4) Claude is instructed to use AskUserQuestion to select or create a project; (5) **gap:** the deliverables do not document how a CoWork plugin user creates a project or sets JERRY_PROJECT from within a CoWork session.

The L0 Executive Summary asserts "`projects/` is internal work history that CoWork users never need" — yet H-04 requires an active project for every session. The stub prevents a crash, but the deliverables do not resolve this contradiction: users DO need a project context to satisfy the SessionStart hook, and the mechanism for obtaining it in a CoWork plugin context is undocumented.

The WS-4 documentation requirements (REQ-024–REQ-029) cover: Tutorial (install command), How-To (sync/update, troubleshoot file-limit errors), Reference (skeleton branch facts), Explanation (version-alignment). None cover the first-run H-04 experience: how to create a project, set JERRY_PROJECT, or complete the `<project-required>` flow from within a CoWork session.

**Impact:** A first-time CoWork plugin user hits `<project-required>`, is prompted to "select/create project," but finds no documentation explaining how to do this in the CoWork context. The acceptance test for REQ-004 is run against a developer clone, not in a real CoWork session, so this failure mode is invisible at Phase 1.

**Dimension:** Completeness

**Response Required:** (1) Document how JERRY_PROJECT is set in a CoWork plugin session (config file, `jerry` CLI in a CoWork terminal, or another mechanism). (2) Add a documentation requirement to WS-4 covering the first-run H-04 experience for CoWork plugin users. (3) Revise REQ-004 acceptance criterion to include a functional H-04 test: "After `jerry projects list` returns 'No projects found,' user can create a project and JERRY_PROJECT is set correctly in the subsequent session."

**Acceptance Criteria:** A functional demonstration (or explicit documentation) that a first-time CoWork plugin user — starting from a fresh install with JERRY_PROJECT unset — can successfully complete the H-04 bootstrap flow within the first session.

---

### DA-003-20260626: 7-Directory Check Conflates CLI-Required with CoWork-Plugin-Surface; marketplace.json Unchecked [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Deliverables** | phase1-requirements REQ-005 |
| **Strategy Step** | Step 3 (Logical Flaws + Alternative Interpretations lenses) |

**Claim Challenged:**
> REQ-005: "The skeleton generation script SHALL verify that the following seven directories are present: `.claude-plugin/`, `skills/`, `.claude/`, `.context/`, `src/`, `schemas/`, `hooks/`."
> REQ-005 rationale: "These directories constitute the declared plugin surface (88 agents, skills tree, 2 commands)."

**Counter-Argument:**
The 7-directory list conflates two distinct categories. CoWork-plugin-surface directories (what CoWork's loader reads to install and run the plugin): `.claude-plugin/`, `skills/`, `.claude/`, `.context/`, `hooks/`. Jerry-CLI-required directories (needed for the `jerry` command-line tool to function): `src/` (Python source), `schemas/` (JSON Schema validation files used by CI tooling). `schemas/` contains agent governance schemas used in CI pipelines and developer tooling — CoWork's plugin loader does not read these files. Stripping `schemas/` would break CI validation but not the CoWork plugin install. `src/` is Python source; CoWork does not execute Python to load a plugin.

More critically: `.claude-plugin/marketplace.json` is the entry point for `claude plugin marketplace add geekatron/jerry@cowork-skeleton` (the install command specified in REQ-026). If `marketplace.json` is missing or syntactically invalid, the CoWork install command fails — but REQ-005's acceptance criterion (`git ls-tree --name-only HEAD {dir}/` returns non-empty) only checks that `.claude-plugin/` is a non-empty directory, not that `marketplace.json` exists or is valid.

**Impact:** REQ-005 provides false confidence that the 7-directory check guarantees plugin load. The most critical file for the install entry point (marketplace.json) is not checked. Including `schemas/` in a "plugin surface" check understates the specificity of what is actually being verified.

**Dimension:** Methodological Rigor

**Response Required:** (1) Add an explicit check for `.claude-plugin/marketplace.json` to the generation script and REQ-005 acceptance criterion. (2) Clarify the REQ-005 rationale: the 7 directories serve "Jerry CLI functionality and CoWork plugin load" — distinguish which directories are required for each purpose. (3) Consider verifying `marketplace.json` is syntactically valid JSON as part of the generation script's post-strip checks.

**Acceptance Criteria:** REQ-005 acceptance criteria enhanced to include: "`.claude-plugin/marketplace.json` is present in `git ls-files`"; the rationale distinguishes plugin-surface dirs from CLI-required dirs.

---

### DA-004-20260626: Full-History "Strong Provenance" Benefit Overstated for Tip-Tree CoWork Install; Clone-Weight Risk Unquantified [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Deliverables** | ADR-001 §Decision, §Regeneration Commit Determinism, §Consequences |
| **Strategy Step** | Step 3 (Alternative Interpretations + Contradicting Evidence lenses) |

**Claim Challenged:**
> ADR-001 §Decision: "Option A is the only option that simultaneously delivers determinism, achievable bit-identical idempotency, strong release provenance, and minimal tooling."
> ADR-001 §Consequences Positive: "Auditable provenance — the skeleton commit's parent is the exact v* release commit; `git log` and `git diff` against main work."
> ADR-001 §Rationale: "we choose provenance by default because (i) history weight affects only clone bandwidth."

**Counter-Argument:**
The provenance argument misaligns the benefit with the user population:

1. **Who benefits from git log / diff against main?** A developer who clones `cowork-skeleton` directly. **CoWork plugin users** receive the installed tip tree at `~/.claude/plugins/cache`; they do not have a git-navigable history in that location. ADR-001 itself states: "A Claude Code plugin install clones the branch and materializes its working tree at the tip commit." The history providing "strong provenance" is never visible to the end user installing the plugin through CoWork.

2. **Option B provides the same text provenance.** ADR-001's commit message template includes `Source-Tag: <tag>` and `Source-Commit: <40-char source SHA>`. This text-based provenance is present in an orphan commit (Option B) too — it lacks only the git-internal parent pointer. For supply-chain auditing, the commit message text is the primary human-readable evidence; the parent pointer adds git-native diff/log capability that is accessible only to maintainers with a direct clone, not CoWork plugin users.

3. **The 120-second clone-weight timeout risk is asserted as LOW-MED but never quantified.** The ADR acknowledges "on slow networks this risks CoWork's 120-second git-operation timeout" but provides no data: the compressed pack size of `main`'s git history in MB is not measured, and no estimated clone time on a representative slow network is documented. If the risk materializes, the "switch to Option B" escape hatch requires a new v* tag and CI run — blocking CoWork users on slow networks until the next release.

**Impact:** The Option A decision is defensible, but two of its three stated advantages are weaker than documented: the provenance benefit does not reach CoWork plugin users, and the counterbalancing clone-weight risk is unquantified. Option B (orphan) delivers the same installed tip-tree artifact, the same commit-message provenance text, and a lighter clone — the only concrete cost is the loss of the git-native parent link for maintainer workflows.

**Dimension:** Evidence Quality

**Response Required:** (1) Measure `main`'s compressed pack size (in MB) and estimate clone time on a representative network. Add this measurement to ADR-001. (2) Explicitly identify the intended audience for the git-native provenance benefit: if it is maintainers only (not CoWork plugin users), state this in the ADR. (3) Either accept the unquantified clone-weight risk explicitly (adding it to the risk register with a measurement trigger) or provide empirical data before Phase 5.

**Acceptance Criteria:** ADR-001 includes the git history compressed-pack size in MB and a note identifying whether the provenance benefit is available to CoWork plugin users or maintainers only.

---

### DA-005-20260626: No Proactive File-Count Drift Governance Mechanism [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Deliverables** | phase1-requirements REQ-006, ADR-001 §L2 ¶5 |
| **Strategy Step** | Step 2 (Assumption Challenge) + Step 3 (Unaddressed Risks lens) |

**Claim Challenged:**
> REQ-002: "targeting approximately 1,744 tracked files — comfortable margin under the ~5,000 limit."
> REQ-006: "The skeleton generation script SHALL exit with a non-zero exit code if the tracked file count assertion is not satisfied."
> ADR-001 §L2 ¶5: "If clone weight or the file-count margin tightens later, the same generation job can additionally strip `skills/transcript/test_data/` ~908 KB blobs, `tests/`, `docs/archive/` — none of which is needed today."

**Counter-Argument:**
REQ-006 is a reactive hard-fail: it fires DURING a release CI run when a `v*` tag is being processed. At that point, a count violation means the release fails, `cowork-skeleton` is NOT updated, and the maintainer must diagnose and triage — potentially during a time-sensitive security release. There is no mechanism to detect drift BEFORE a release is blocked.

The "comfortable margin" (1,744 of 5,000 = 3,256 files of headroom) is presented as a static fact, but the project is under active development. Every new agent file in `skills/`, every new template in `.context/templates/`, every new governance doc and ADR, every new worktracker entity in non-`projects/` directories adds to the count. ADR-001 §L2 ¶5 explicitly names three directories as future stripping candidates — acknowledging that they already exist in the retained tree and will eventually require action. No trigger for WHEN to act is defined, and no monitoring mechanism detects drift between releases.

The deliverables do not define: (a) the current per-directory file-count breakdown for retained directories; (b) an early-warning threshold; (c) what to strip first and in what order when REQ-006 fires; (d) who is responsible for triggering additional stripping.

**Impact:** If the file count drifts above 5,000 between releases, a scheduled release CI run fails with no prior warning. The response plan (strip additional directories) is described conceptually in ADR-001 §L2 ¶5 but is not a documented, executable procedure.

**Dimension:** Completeness

**Response Required:** (1) Add an NFR or note to REQ-006 acknowledging that it is a reactive control and documenting the accepted operational response: which directories to strip first (in priority order) when the assertion fires. (2) Document the current per-directory file-count breakdown for all retained directories so future growth can be attributed and monitored. (3) Optionally: add a scheduled (non-release) CI check or a per-PR file-count annotation with an early-warning threshold (e.g., >4,000 files triggers an advisory warning).

**Acceptance Criteria:** REQ-006 or a companion note documents a prioritized response plan specifying which directories to strip (in order) when the count assertion fires; current per-directory file-count breakdown is recorded in the requirements or ADR.

---

### DA-006-20260626: workflow_dispatch Lacks Explicit Tag-Selection Input [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Deliverables** | phase1-requirements REQ-011, REQ-018 |
| **Strategy Step** | Step 3 (Unaddressed Risks lens) |

**Claim Challenged:**
> REQ-011: "The CI workflow SHALL trigger on `push: tags: ['v*']` and `workflow_dispatch` events."
> REQ-018 acceptance criterion: "`workflow_dispatch` triggered twice for the same tag; `git log -1 --format='%H %s' cowork-skeleton` output is identical after both runs."

**Counter-Argument:**
REQ-018 tests "triggered twice for the same tag" but does not specify how the operator communicates WHICH tag to target for a manual dispatch. Without an explicit `inputs: source_tag:` block in the workflow YAML, `workflow_dispatch` has no mechanism for tag selection. If the workflow auto-selects the latest `v*` tag at run time, triggering a `workflow_dispatch` after a newer tag has been pushed regenerates `cowork-skeleton` from the newer tag — not the tag the operator intended. The "re-runnable at any time for any past tag" guarantee in NFR-005 becomes operationally ambiguous.

**Impact:** Recovery from a CI failure for a specific past release requires pushing a temporary tag or a workaround; the "trigger workflow_dispatch" recovery path in NFR-005 may not target the correct tag without an explicit input.

**Dimension:** Actionability

**Response Required:** Acknowledge in REQ-018 or add an implementation note: the `workflow_dispatch` trigger SHOULD declare `inputs: source_tag: description: 'v* tag to regenerate from (leave blank for latest)'` so operators can target a specific past tag. If the intent is "always regenerate from the latest tag," document this explicitly and revise NFR-005 accordingly.

**Acceptance Criteria:** Either the workflow YAML includes an optional `inputs: source_tag:` parameter, or REQ-018 explicitly documents that "regenerate for a specific past tag" requires pushing a new tag (not workflow_dispatch alone).

---

### DA-007-20260626: Stub Static-Content Constraint Deferred to STORY-002 Without Phase 1 Enforcement [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Deliverables** | ADR-001 §Regeneration Commit Determinism; phase1-requirements REQ-003, REQ-004, NFR-001 |
| **Strategy Step** | Step 2 (Assumption Challenge: cross-deliverable unstated dependency) |

**Claim Challenged:**
> ADR-001 §Regeneration Commit Determinism: "the stub `projects/README.md` MUST be static content. Any generated date, version string, or run ID inside it changes the tree and breaks reproducibility. Authoring is STORY-002; this ADR fixes only its determinism property."
> REQ-003 / NFR-001 acceptance criterion: "Script executed twice against the same tag SHA; `git rev-parse cowork-skeleton` returns an identical 40-character SHA on both executions."

**Counter-Argument:**
The bit-identical idempotency guarantee (REQ-003 / NFR-001) has a critical coupling to `projects/README.md` being static. That constraint is stated in ADR-001, deferred to STORY-002, and enforced by NO acceptance criterion in the current Phase 1 deliverables.

REQ-004 acceptance criterion checks "jerry projects list exits 0 and prints 'No projects found'" — it does not verify stub content. REQ-003 acceptance criterion checks "identical SHA on both executions" — but both executions happen within the SAME CI run (the same second). If the stub includes a generated value (e.g., `Generated: {date}`, a version string from `pyproject.toml`, or a build run ID), two same-run executions would still produce the same SHA because the timestamp resolves identically in the same second. The cross-run idempotency test — two separate CI runs minutes apart — is NOT specified in any REQ-003 acceptance criterion.

The consequence: a STORY-002 author who includes a `Generated: 2026-06-26` line in the README would not be warned by any existing acceptance criterion. The idempotency property silently breaks on the second release CI run.

**Impact:** The idempotency guarantee that REQ-003, NFR-001, and NFR-002 depend upon is critically coupled to a stub that does not yet exist, whose content is not specified in Phase 1, and whose static-content property is not verifiable with the current acceptance criteria. A single authoring decision in STORY-002 invalidates the idempotency proof.

**Dimension:** Traceability

**Response Required:** (1) Define the verbatim stub content (or a content hash) in Phase 1 deliverables as a fixed constraint — do not leave it to STORY-002 to determine independently. (2) Revise REQ-003 acceptance criterion to include a cross-run test: "Two separate `workflow_dispatch` runs triggered at different times for the same tag produce an identical `git rev-parse cowork-skeleton` SHA." (3) Add to REQ-004: "The `projects/README.md` content matches the verbatim text specified in [Phase 1 stub spec]" so STORY-002 authors cannot drift it.

**Acceptance Criteria:** Verbatim stub content (or hash) is committed in Phase 1 deliverables; REQ-003 acceptance criterion includes a cross-run idempotency test (not only a same-run test).

---

## Recommendations

### P0 — Critical (MUST resolve before Phase 2 proceeds)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-001-20260626 | Run `gh api orgs/geekatron/rulesets`; document all active org rulesets; confirm none restrict GITHUB_TOKEN force-push to `cowork-skeleton`; update REQ-021 AC to include org-level check | Phase 1 deliverables include org-ruleset check result; REQ-021 AC covers both repo-level and org-level protection |
| DA-002-20260626 | Document how JERRY_PROJECT is set in a CoWork plugin session; add a WS-4 documentation requirement for first-run project-creation guide; revise REQ-004 AC to include a functional H-04 test | REQ-004 AC demonstrates full H-04 flow (not just no-crash); WS-4 includes a first-run JERRY_PROJECT setup doc requirement |

### P1 — Major (SHOULD resolve; document justification if not)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-003-20260626 | Add `marketplace.json` existence check to REQ-005 AC; clarify that `schemas/`, `src/` are CLI-required, not CoWork-plugin-surface | REQ-005 AC includes `git ls-files .claude-plugin/marketplace.json`; rationale distinguishes plugin-surface from CLI-required dirs |
| DA-004-20260626 | Measure `main` git history compressed-pack size in MB; document whether provenance benefit is accessible to CoWork plugin users or maintainers only | ADR-001 includes measured pack size or explicit statement of audience for provenance benefit |
| DA-005-20260626 | Add a prioritized response plan to REQ-006 specifying which dirs to strip first when the count assertion fires; record current per-directory file-count breakdown | REQ-006 or companion note documents ordered strip-priority and current per-directory counts |
| DA-007-20260626 | Define verbatim stub content (or hash) in Phase 1; revise REQ-003 AC to include a cross-run idempotency test | Stub content committed in Phase 1; REQ-003 AC includes a two-separate-runs test |

### P2 — Minor (MAY resolve; acknowledgment sufficient)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-006-20260626 | Specify how workflow_dispatch selects the target tag; add `inputs: source_tag:` or document "always latest tag" design | REQ-018 documents the intended tag-selection behavior for manual dispatch |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | **Negative** | DA-002 (H-04 first-run gap in requirements and WS-4 docs), DA-005 (no proactive file-count drift governance) leave STK-003 and long-term sustainability underdocumented |
| Internal Consistency | 0.20 | **Neutral** | No internal contradictions found across the three deliverables; ADRs and requirements are mutually reinforcing |
| Methodological Rigor | 0.20 | **Negative** | DA-001 (org vs. repo-level branch protection not distinguished), DA-003 (7-directory check framing conflates two categories) weaken the CI strategy analysis |
| Evidence Quality | 0.15 | **Negative** | DA-004 (120s timeout risk unquantified; provenance benefit documented without audience analysis) reduces confidence in the Option A rationale |
| Actionability | 0.15 | **Negative** | DA-005 (no response plan when REQ-006 fires), DA-006 (workflow_dispatch tag-selection underdefined) reduce operational clarity |
| Traceability | 0.10 | **Negative** | DA-007 (critical idempotency constraint deferred to STORY-002 without Phase 1 acceptance criteria) leaves a cross-deliverable dependency unverified |

**Overall Assessment:** REVISE. Two Critical findings (DA-001, DA-002) identify pre-Phase-5 blockers that could either cause immediate CI failure on first live run or produce a first-run CoWork plugin user experience failure. Four Major findings reduce confidence across five of six S-014 dimensions. One Minor finding is operational guidance only. The core strategy — derived branch, GITHUB_TOKEN, deterministic commit, v* tag trigger — is sound. The gaps are concentrated in completeness of pre-implementation verification and evidence quality of two key design choices.

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 2 (DA-001, DA-002)
- **Major:** 4 (DA-003, DA-004, DA-005, DA-007)
- **Minor:** 1 (DA-006)
- **Protocol Steps Completed:** 5 of 5

---

*Strategy: S-002 Devil's Advocate*
*Template: `.context/templates/adversarial/s-002-devils-advocate.md` v1.0.0*
*Agent: jerry:adv-executor*
*Project: PROJ-031-cowork-skeleton*
*Workflow: cowork-skeleton-20260626-001 / QG-1*
*Date: 2026-06-26*
