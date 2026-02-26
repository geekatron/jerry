# C4 Tournament Adversarial Review — Iteration 2 of 5
## Deliverable: GitHub Issue Draft — Extract Project Tracker from Plugin Repository

> **Execution Context**
> - **Deliverable:** `work/gh-issues/issue-project-tracker-extraction.md`
> - **Criticality:** C4 (OSS release preparation; architectural separation; public-facing repository change)
> - **Tournament Iteration:** 2 of 5 | Elevated Threshold: >= 0.95
> - **Executed:** 2026-02-25
> - **H-16 Compliance:** S-003 (Steelman) executed before S-002, S-004, S-001 — SATISFIED
> - **Strategies:** S-014, S-003, S-013, S-007, S-002, S-004, S-010, S-012, S-011, S-001 (all 10)
> - **Prior Iteration Score:** 0.77 (REJECTED) | Revision count: R-001 through R-011 applied

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Section 1: S-014 LLM-as-Judge Scoring](#section-1-s-014-llm-as-judge-scoring) | 6-dimension rubric scoring with anti-leniency |
| [Section 2: S-003 Steelman](#section-2-s-003-steelman) | Strongest form of the deliverable's argument |
| [Section 3: Consolidated Findings (All 10 Strategies)](#section-3-consolidated-findings-all-10-strategies) | Full finding catalog with severity and evidence |
| [Section 4: Revision Recommendations](#section-4-revision-recommendations) | R-001 through R-NNN with before/after text |
| [Section 5: Voice Assessment](#section-5-voice-assessment) | Saucer Boy persona compliance |
| [Section 6: Gap Analysis to 0.95](#section-6-gap-analysis-to-095) | Honest assessment and remaining distance |
| [Section 7: Delta Analysis](#section-7-delta-analysis) | What improved, what regressed, what is new |

---

## Section 1: S-014 LLM-as-Judge Scoring

**Finding Prefix:** LJ-NNN-it2 (Iteration 2)

**Anti-leniency bias active.** When uncertain between adjacent scores, the lower score is assigned. All score justifications require specific evidence from the deliverable text.

---

### Dimension 1: Completeness (Weight: 0.20)

**Score: 0.88**

**Evidence for score:**

The revision incorporated substantial improvements from Iteration 1:

**Additions confirmed (positive):**
- Rollback procedure added with 4 numbered steps: checkpoint tag, `git reset --hard`, force-push coordination, tag preservation until validation passes — this closes FINDING-C2/R-002
- Windows symlink note added: "Symlink creation requires Developer Mode enabled or Administrator privileges (`mklink /D projects <path-to-jerry-projects>`). Contributors on Windows SHOULD use WSL2 or a directory junction (`mklink /J`) as an alternative" — this closes FINDING-M1/R-004
- Alternatives Considered section added with 5 options evaluated — this closes FINDING-C1/R-001
- Repository visibility decision made explicit: "Create `geekatron/jerry-projects` as a **private** repository. Rationale: `projects/` contains security research artifacts..." — this closes RT-002/R-010
- Contributor migration notice added to Phase 1 — this closes FINDING-M4/R-007
- `projects/README.md` ownership resolved: stub remains in Jerry — this closes FINDING-M5/R-008
- Total repo size context added: "60 MB across 3,791 files... 19 MB and 1,378 files" — this closes FINDING-M2/R-005
- Git tool recommendation updated to `git subtree split` + `git-filter-repo` — this closes FINDING-C3/R-003
- CI pipeline update addressed: "Update GitHub Actions CI pipeline to ensure no test step assumes `projects/` exists. CI runs on a clean checkout without any symlink — CI MUST pass in this configuration" — this closes RT-001/R-009
- CLI behavior specified with exit code 0 and exact message — this closes FINDING-M3/R-006
- Distribution mechanism clarified: "Claude Code plugin system" and "clones or downloads the full repository content" — this partially closes DA-001/R-011

**Remaining completeness gaps:**

- **No worktracker entity link or GitHub milestone reference.** "Why now" mentions Jerry's OSS release preparation but provides no link to the corresponding issue, milestone, or internal entity. For a C4 OSS release issue, the upstream tracking context is still missing. CC-001-it1 was a minor finding in Iteration 1 — it remains unaddressed.
- **`docs/development/project-tracker-setup.md` content unspecified.** The issue calls for creating this file but gives no content outline. The Windows note mentions the path but nothing tells an implementer what the file should contain (prerequisite steps, platform variants, git clone instructions for jerry-projects). For an actionable issue this is a meaningful gap.
- **Per-project breakdown still contains the PROJ-001 naming anomaly.** The table note says "The naming convention evolved organically" but does not clarify which is the real PROJ-001 or how to resolve the identifier conflict. CV-003-it1 (3 entries with PROJ-001) remains unaddressed. Minor but present.
- **"Plugin installation size reduced by >= 40 MB"** — the acceptance criterion specifies ">= 40 MB" but the data shows a 41 MB `projects/` directory against a 60 MB total repo. The criterion is achievable. However, no measurement method is specified for validation. The acceptance criterion remains partially unverifiable.

**Score justification:** 0.88 — Major completeness gaps from Iteration 1 are closed (rollback, alternatives, Windows, visibility, CLI spec). Remaining gaps are real but smaller: missing worktracker/milestone link, unspecified developer guide content, unresolved PROJ-001 naming, unmeasured validation method for size criterion.

---

### Dimension 2: Internal Consistency (Weight: 0.20)

**Score: 0.87**

**Evidence for score:**

**Consistency improvements (positive):**
- `projects/README.md` ambiguity resolved: table now shows it stays in Jerry, Phase 1 says "Update `projects/README.md` to a stub." These are now consistent.
- CI validation requirement is now consistent with rollback procedure — the rollback tag preservation note reads "Do NOT remove the pre-extraction tag until Phase 3 validation gates pass and at least one full CI cycle succeeds on main" — internally coherent.

**Remaining or new inconsistencies:**

1. **New inconsistency: git subtree vs. git-filter-repo framing.** The issue says "Extract `projects/` history using `git subtree split --prefix=projects/ HEAD -b projects-split`, then push to the new repo: `git push <jerry-projects-remote> projects-split:main`. Avoid `git filter-branch` (deprecated since Git 2.24 in favor of `git-filter-repo`). If `git-filter-repo` is available, the equivalent is: `git-filter-repo --path projects/ --target <new-repo-path>`."

   The parenthetical says `git filter-branch` is deprecated "in favor of `git-filter-repo`" — but the **primary recommendation** in the sentence before is `git subtree split`, not `git-filter-repo`. The deprecation note implies the replacement is `git-filter-repo`, which creates ambiguity: is the implementer supposed to use `git subtree split` (the first option) or `git-filter-repo` (the "modern equivalent" mentioned in the deprecation note)? The framing suggests they are equivalent alternatives, but they produce meaningfully different results (`subtree split` creates a branch; `filter-repo` rewrites history or creates a new repo). An implementer has to choose between two documented options with no guidance on which is preferred.

2. **Alternatives Considered table vs. rollback section tension.** The Alternatives Considered section includes "Git submodule — Rejected: does not solve the plugin distribution problem — submodules are included in clone by default unless sparse checkout is configured." But the Phase 1 implementation uses `git subtree split`, which is listed in the table as a different alternative ("Git subtree (embedded) — Rejected: Does not reduce installation size"). The selected approach is "Symlink bridge" but the implementation *mechanism* (`git subtree split`) is the same tool as the rejected "Git subtree (embedded)" alternative. This is not actually an inconsistency in the proposal — the subtree split command is used for *extraction* not for *embedding* — but it creates surface-level confusion for readers who parse the alternatives table and see "Git subtree" as rejected.

3. **Phase 3 validation: "Plugin installation size reduced by >= 40 MB"** — the data table shows `projects/` = 41 MB. The rollback criterion says to preserve the pre-extraction tag "until Phase 3 validation gates pass." But Phase 3 does not specify a measurement procedure, so the gate cannot deterministically pass or fail. Minor internal inconsistency.

**Score justification:** 0.87 — Primary inconsistency from Iteration 1 (README ownership) resolved. New inconsistency introduced (git subtree split vs. git-filter-repo framing). Subtree tool confusion is real but not fatal. Score holds below 0.90 because the dual-option git tool recommendation without selection guidance is a genuine implementation impediment.

---

### Dimension 3: Methodological Rigor (Weight: 0.20)

**Score: 0.87**

**Evidence for score:**

**Rigor improvements (positive):**
- Alternatives Considered section added with 5 options, each with explicit rejection rationale. This closes the largest single Methodological Rigor gap from Iteration 1.
- `git filter-branch` deprecated; `git subtree split` and `git-filter-repo` offered as replacements with commands specified.
- Rollback procedure is now a numbered 4-step process with specific git commands.
- Repository visibility decision made with rationale: private because PROJ-008 and PROJ-009 contain sensitive material.
- Technical note on `fnmatch`/`pathlib` symlink behavior is now appropriately hedged: "This must be tested, not assumed."

**Remaining rigor gaps:**

1. **Alternatives rejection rationales are partially weak.** The "Git submodule" rejection says: "Does not solve the plugin distribution problem — submodules are included in clone by default unless sparse checkout is configured." This is partially true — `git clone --recurse-submodules` is not the default for most `git clone` invocations, and a submodule *not* initialized on clone would indeed reduce the distribution size. The rejection rationale conflates submodule behavior (not included unless recursed) with the problem (included by default). A rigorous rejection would acknowledge that non-recursive clone *does* exclude the submodule, then explain why this is still worse than the symlink approach (e.g., "Contributors would need to explicitly initialize the submodule to access it, creating a confusing two-step setup"). The current rationale may mislead implementers about how submodules work.

2. **`git subtree split` vs `git-filter-repo` — no selection guidance.** Two tools are recommended without stating which is preferred or under what conditions to use each. For a C4 issue specifying an irreversible operation, this is a methodological gap — the issue should recommend one primary tool and note the alternative.

3. **No risk register (upgraded, not new).** The FMEA findings from Iteration 1 (FM-001-it1 through FM-003-it1) are not reflected in any explicit risk register or mitigation table. The issue now has rollback and visibility decisions, but it does not enumerate known risks with likelihood/impact. For a C4 irreversible operation, a lightweight risk table would substantially improve methodological rigor.

4. **"Full history preservation" remains underspecified (CV-002-it1 persists).** The issue still says "full git history preservation" without clarifying what guarantee is being made (commit SHAs differ in the new repo, cross-directory context is lost). The technical note on fnmatch/pathlib improves one CV finding, but CV-002-it1 is not addressed.

**Score justification:** 0.87 — Substantial improvement from 0.70 in Iteration 1. Alternatives analysis added, rollback specified, tools improved. Remaining gaps: weak submodule rejection rationale, dual-tool ambiguity, no risk register, "full history" still undefined. Score held below 0.90 because the git tool recommendation section is genuinely ambiguous for implementers.

---

### Dimension 4: Evidence Quality (Weight: 0.15)

**Score: 0.90**

**Evidence for score:**

**Evidence improvements (positive):**
- Total repo size context added: "The Jerry framework's git-tracked content totals 60 MB across 3,791 files. The `projects/` directory is 41 MB (67% by size) and 2,413 files (63% by count). Remove `projects/` and the framework is 19 MB and 1,378 files." This is specific, verifiable, and directly answers the "relative impact" question from Iteration 1. Strong.
- "67% by size, 63% by file count" percentage calculations are now in the data table.
- Distribution mechanism clarified: "Claude Code plugin system... clones or downloads the full repository content — including `projects/`." This substantiates the claim that users receive the full 41 MB.
- Repository visibility decision backed by specific content rationale: PROJ-008 and PROJ-009 are named as the sensitivity concern.

**Remaining evidence gaps:**

1. **"The `projects/` directory is not excluded by any distribution filter, `.npmignore`, or package manifest"** — this is asserted but not verified in the issue. Is there a `.gitattributes` export-ignore? Is there a `.claude-plugin` manifest that defines included files? The claim is plausible but the issue does not provide evidence that these mechanisms are absent. For a C4 issue, "not excluded by any filter" should be backed by inspection evidence, not assertion.

2. **The data table row "Total lines in `projects/`": 635,075** — no source for this count is provided. This is a specific number that implies measurement. Was it from `find projects/ -name "*.md" | xargs wc -l`? Or `git ls-files projects/ | xargs wc -l`? Minor but unattributed specific claims weaken evidence quality.

3. **"Git clone time and disk usage reduced for new contributors"** — still unquantified. No baseline clone time measurement. This is now less important given the relative size data, but the claim remains unverified.

**Score justification:** 0.90 — Strong improvement from 0.86. The relative context addition makes the primary evidence compelling. Deductions for unverified "no distribution filter" claim and unattributed line count. Score held at 0.90, not higher, because two supporting claims remain asserted rather than evidenced.

---

### Dimension 5: Actionability (Weight: 0.15)

**Score: 0.88**

**Evidence for score:**

**Actionability improvements (positive):**
- CLI behavior now specified with exit code and example message: "exit code 0 with a human-readable informational message (e.g., 'No projects directory found. Use the worktracker skill to create projects in your repository.')."
- `jerry projects context` and `jerry projects validate` explicitly follow same pattern.
- Rollback procedure now numbered with specific git commands.
- Contributor migration notice specified (CHANGELOG entry, guidance for local clones).
- Windows note is specific and actionable (two alternatives provided: WSL2, directory junction).
- Acceptance criteria checklist is comprehensive and mostly concrete.

**Remaining actionability gaps:**

1. **`docs/development/project-tracker-setup.md` — content not specified.** The acceptance criteria say "Symlink setup documented in `docs/development/project-tracker-setup.md` (macOS/Linux symlink, Windows junction alternative)" but no content outline exists. An implementer knows the file must exist but not what it must contain. For a deliverable specification, the minimum required content should be enumerated.

2. **"Force-push only if the migration was already pushed to remote (coordinate with any open PRs)"** — the rollback step 3 says "Force-push only if the migration was already pushed to remote." This is sound advice but "coordinate with any open PRs" is not actionable. What does coordination require? Close the PRs? Wait until they are merged? Add a base branch reassignment? The rollback procedure is almost there but this step is incomplete.

3. **"Delete the jerry-projects repo if it was already created"** — rollback step 4. This is actionable but does not address the git history that was pushed. If `git subtree split` pushed to jerry-projects, deleting the GitHub repo removes it from the web interface but does not affect anyone who cloned it. If no one cloned it, this is fine. If someone did, the procedure is incomplete. The issue should note: "If jerry-projects has not been cloned by anyone other than the framework author, deletion is clean. Otherwise, notify affected parties."

4. **Phase 2 audit scope for `.context/rules/` references is still partially deferred.** The issue says: "Decision: keep the references as-is." This is now a decision (better than "either approach is acceptable"), but "Audit all `projects/` path references in `.context/rules/` files" remains un-enumerated. How many files? How many references? An implementer does not know the scope of this work item.

**Score justification:** 0.88 — Solid improvement from 0.79. CLI behavior, rollback, contributor notice are now actionable. Remaining gaps: developer guide content unspecified, rollback coordination step vague, `.context/rules/` audit unscoped. Not at 0.90 because the developer guide is a new deliverable with no defined content.

---

### Dimension 6: Traceability (Weight: 0.10)

**Score: 0.78**

**Evidence for score:**

**Traceability improvements (positive):**
- The Affected Components section now lists specific code paths with file names and line ranges: "`src/domain/markdown_ast/document_type.py` (path patterns at lines 98-106)"
- Distribution mechanism described with reference to `.claude-plugin/` manifest.
- Repository visibility decision includes rationale tracing to named PROJ-008 and PROJ-009.

**Remaining traceability gaps:**

1. **No link to OSS release milestone or parent GitHub issue.** The "Why now" section references Jerry's OSS release preparation but provides no GitHub issue number, milestone link, or worktracker entity reference. An external contributor reading this issue cannot trace to the project that motivates it. This was FINDING-m3 in Iteration 1 (Minor) — it remains unaddressed.

2. **Code files named but not linked.** `src/domain/markdown_ast/document_type.py` is referenced with line numbers (98-106) but no GitHub URL. On GitHub this issue will render without hyperlinks to the affected code. External contributors cannot navigate. This was FINDING-m2 in Iteration 1 (Minor) — it remains unaddressed.

3. **`skills/worktracker/rules/worktracker-directory-structure.md` is referenced by name in prose** ("Plugin users who adopt Jerry's worktracker skill create projects in their own repositories using the repository-based placement pattern already defined in `skills/worktracker/rules/worktracker-directory-structure.md`") but not linked. Same traceability pattern as FINDING-m2.

4. **`geekatron/jerry-projects` — no repository URL.** The issue proposes creating the repo but does not link to it (not yet created at time of writing, which is expected, but the acceptance criterion does not include "repository URL added to this issue after creation").

5. **No ADR referenced.** This is an architectural decision (separating the workbench from the tool). An ADR or reference to worktracker directory structure standards would anchor this decision in the governance record. This was mentioned in CC-001-it1 and SM-008-it1 in Iteration 1 — still unaddressed.

**Score justification:** 0.78 — Modest improvement from 0.72 (Iteration 1) due to line-number references added to code files. Core gaps persist: no GitHub links to code, no OSS release milestone link, no ADR reference. The gap from 0.78 to 0.90+ requires adding 6-8 hyperlinks and a governance anchor — low effort, high traceability payoff.

---

### Composite Score Calculation

| Dimension | Weight | Score | Weighted Score |
|-----------|--------|-------|----------------|
| Completeness | 0.20 | 0.88 | 0.176 |
| Internal Consistency | 0.20 | 0.87 | 0.174 |
| Methodological Rigor | 0.20 | 0.87 | 0.174 |
| Evidence Quality | 0.15 | 0.90 | 0.135 |
| Actionability | 0.15 | 0.88 | 0.132 |
| Traceability | 0.10 | 0.78 | 0.078 |
| **Composite** | **1.00** | | **0.869** |

**Composite Score: 0.87**

**Verdict: REVISE** (threshold 0.95 elevated; gap = 0.08; standard threshold 0.92 gap = 0.05)

**Leniency Bias Check:** Multiple scores were held at the lower adjacent value where uncertainty existed. Internal Consistency held at 0.87 (not 0.90) because the git tool dual-recommendation is a real implementer impediment. Methodological Rigor held at 0.87 (not 0.90) because the submodule rejection rationale is factually imprecise and no risk register exists. Traceability held at 0.78 because the gap in hyperlinks and governance anchor is not trivial.

---

## Section 2: S-003 Steelman

**Finding Prefix:** SM-NNN-it2

### Summary

**Steelman Assessment:** The deliverable has made substantial progress toward its strongest form. The Iteration 2 revisions address the most significant structural weaknesses from Iteration 1: alternatives analysis, rollback plan, git tool correction, visibility decision, CLI behavior specification. The issue is now materially more complete and rigorous than it was at 0.77.

**Improvement Count since Iteration 1:** 9 Critical/Major gaps closed. 3 new findings introduced. Net progress: strong.

**Core argument strength:** The central thesis remains valid and is now better supported. The relative size context (67% of tracked content, 19 MB clean framework) is the decisive evidence addition — it transforms "43 MB is big" into "43 MB is two-thirds of everything." This is the right evidence for the right argument.

---

### Strongest Form of the Argument

The deliverable's strongest form at Iteration 2 is:

**This is the right pre-release housekeeping operation, done the right way, with the right evidence.** The 67% / 63% statistics are not just compelling — they reveal an architectural incoherence that has been building since Jerry's early development. The `projects/` directory is the workbench the tool was built on. Shipping the workbench with the tool is not just wasteful; it misrepresents what Jerry *is* to every new user who clones it. The first git clone impression matters for an OSS release. A user who runs `du -sh jerry/` and sees 60 MB (vs. the expected ~5-20 MB for a Python CLI tool) has already formed a negative opinion before reading a single line of documentation.

The symlink bridge is the correct solution because it achieves the three-way optimization: (1) plugin users get a minimal, professional distribution; (2) the framework author retains seamless development workflow via symlink; (3) project history is preserved in a dedicated repository with full commit provenance. No alternative achieves all three simultaneously: git submodules sacrifice UX, git subtree embedded sacrifices distribution size, .gitignore-only sacrifices history, sparse checkout sacrifices user experience for new cloners.

The private repository decision for `jerry-projects` is sound — it closes the security concern around PROJ-008 and PROJ-009 while deferring the visibility upgrade to a separate content review. This is the correct risk-appropriate default.

The implementation phasing (Prepare → Update References → Validate) maps cleanly to the risk profile: do the irreversible operations last, validate in both environments, preserve the rollback checkpoint until validation passes.

**Strongest remaining argument for this form of the proposal:** The symlink setup is a one-time, five-minute configuration for the framework author. The benefit is permanent — every future clone by every future plugin user gets a 19 MB professional distribution instead of a 60 MB author's workbench. The asymmetry is decisive.

---

### Steelman Improvement Findings (Iteration 2)

| ID | Improvement | Severity | Affected Dimension |
|----|-------------|----------|--------------------|
| SM-001-it2 | Resolve git subtree split vs. git-filter-repo dual-recommendation: pick one primary tool | Major | Methodological Rigor, Internal Consistency |
| SM-002-it2 | Fix submodule rejection rationale accuracy (submodules NOT included in non-recursive clones) | Major | Methodological Rigor |
| SM-003-it2 | Add hyperlinks to affected code files (document_type.py, layered_config_adapter.py, worktracker-directory-structure.md) | Minor | Traceability |
| SM-004-it2 | Add OSS release milestone/GitHub issue link to "Why now" | Minor | Traceability |
| SM-005-it2 | Specify minimum content for docs/development/project-tracker-setup.md | Minor | Actionability |

---

## Section 3: Consolidated Findings (All 10 Strategies)

> Strategies executed: S-014, S-003, S-013, S-007, S-002, S-004, S-010, S-012, S-011, S-001
> H-16 compliance: S-003 executed before S-002, S-004, S-001 — CONFIRMED

---

### Critical Findings

#### FINDING-C1-it2: Git Tool Recommendation is Ambiguous — Two Tools, No Selection Guidance
**Strategy Source:** S-010 (Self-Refine), S-011 (Chain-of-Verification), S-002 (Devil's Advocate)
**Severity:** Critical (for an irreversible C4 operation, implementation ambiguity at the key operation is Critical)
**Section:** "Implementation / Phase 1: Prepare"

**Evidence from deliverable:**
> "Extract `projects/` history using `git subtree split --prefix=projects/ HEAD -b projects-split`, then push to the new repo: `git push <jerry-projects-remote> projects-split:main`. Avoid `git filter-branch` (deprecated since Git 2.24 in favor of `git-filter-repo`). If `git-filter-repo` is available, the equivalent is: `git-filter-repo --path projects/ --target <new-repo-path>`."

**Analysis:** This section presents two tools — `git subtree split` (primary) and `git-filter-repo` (conditional "if available"). The deprecation note says `git filter-branch` was deprecated "in favor of `git-filter-repo`" — which signals `git-filter-repo` is the recommended modern tool. But the primary recommendation is `git subtree split`. An implementer reading this faces a real choice: use the first tool listed (subtree split) or the "modern equivalent" (filter-repo)?

These tools behave differently:
- `git subtree split` extracts the subtree's history into a new branch *within the Jerry repo*, then that branch is pushed to the new remote. The Jerry repo retains the full history. No commit rewriting in Jerry.
- `git-filter-repo --path projects/ --target <new-repo-path>` creates a new repository from the filtered history. It can be run non-destructively with `--source`. Without `--source`, it rewrites the current repo's history.

The `--target` flag in `git-filter-repo` makes it operate on a copy, which is safer. But the lack of `--source` specification means an implementer following the command literally may run it against the live Jerry repo. This is a material risk for a C4 irreversible operation.

**Why it is a problem:** An implementer doing this for the first time has no basis to choose between the two tools. The wrong choice (or wrong flags on git-filter-repo) could corrupt Jerry's commit history. For an OSS release with a public repository, this is a Critical-severity gap.

**Recommended fix:** See R-001-it2.

---

### Major Findings

#### FINDING-M1-it2: Git Submodule Rejection Rationale is Factually Imprecise
**Strategy Source:** S-002 (Devil's Advocate), S-013 (Inversion), S-011 (Chain-of-Verification)
**Severity:** Major
**Section:** "Alternatives considered"

**Evidence from deliverable:**
> "Git submodule: Rejected: submodule UX is notoriously poor (requires `--recurse-submodules` on clone, confuses contributors unfamiliar with submodule workflows). Does not solve the plugin distribution problem — submodules are included in clone by default unless sparse checkout is configured."

**Analysis:** The claim "submodules are included in clone by default" is factually incorrect. Git submodules are explicitly **NOT** initialized on a regular `git clone`. They are only populated if the user runs `git clone --recurse-submodules` OR `git submodule update --init` after cloning. A plain `git clone jerry` of a repo with a `projects/` submodule would result in an *empty* `projects/` directory — the user would get zero bytes of project data, not 41 MB.

This means the *distribution size* argument against git submodule is invalid. The correct rejection argument for git submodule is:
1. **UX complexity:** Contributors who do want project data must take extra steps (clone with `--recurse-submodules`, or run `git submodule update --init` after cloning)
2. **Symlink is simpler for the framework author's development workflow** than submodule management
3. **Submodule commits create pointer conflicts** — any change to `jerry-projects` requires a commit update in Jerry

The current rationale will mislead future readers who understand git submodules and wonder why the rejection was justified.

**Why it is a problem:** An incorrect rejection rationale in an Alternatives Considered section is a methodological integrity failure. If a future contributor reads this and knows submodules aren't included by default, they will question the entire analysis. The issue is C4 and will be a permanent record in the OSS release history.

**Recommended fix:** See R-002-it2.

---

#### FINDING-M2-it2: Rollback Procedure Incomplete — "Coordinate with Open PRs" Not Actionable
**Strategy Source:** S-004 (Pre-Mortem), S-012 (FMEA)
**Severity:** Major
**Section:** "Implementation / Phase 1 — Rollback procedure"

**Evidence from deliverable:**
> "3. Force-push only if the migration was already pushed to remote (coordinate with any open PRs)"

**Analysis:** "Coordinate with any open PRs" is not a procedure — it is a reminder. An implementer executing rollback during a live failure does not have time to determine coordination strategy ad hoc. The rollback procedure should specify: "Close or re-target any open PRs that have the migration commit as a base. GitHub will not automatically update PR base branches on force-push. After force-push, notify PR authors to rebase against the restored history."

Additionally: "Delete the jerry-projects repo if it was already created" (step 4) does not address the case where `jerry-projects` has been cloned by a collaborator. If this is a private repository with only the framework author as member, deletion is safe. The procedure should note this assumption explicitly.

**Recommended fix:** See R-003-it2.

---

#### FINDING-M3-it2: Traceability — No GitHub Links, No ADR Reference, No Milestone Link
**Strategy Source:** S-007 (Constitutional AI), S-011 (Chain-of-Verification), S-010 (Self-Refine)
**Severity:** Major (upgraded from Minor in Iteration 1 because 4+ unaddressed traceability items now represent a pattern, not an oversight)
**Section:** Multiple locations

**Evidence from deliverable:**
- Code files referenced by name only: "`src/domain/markdown_ast/document_type.py` (path patterns at lines 98-106)" — no GitHub URL
- "`skills/worktracker/rules/worktracker-directory-structure.md`" — no link
- "Why now" references OSS release preparation — no milestone or issue link
- `geekatron/jerry-projects` — no repository URL (expected, but no acceptance criterion to add it post-creation)
- No ADR referenced for this architectural separation decision

**Why it is a problem:** This is a C4 OSS release issue that will be publicly visible on GitHub. External contributors — the target audience — cannot navigate from this issue to any of the affected artifacts. Four separate traceability items were identified as Minor in Iteration 1 and none were addressed. At Iteration 2, the pattern of non-address makes this a Major finding. The effort required (adding 5-6 hyperlinks) is approximately 10 minutes of work.

**Recommended fix:** See R-004-it2.

---

#### FINDING-M4-it2: `docs/development/project-tracker-setup.md` — No Content Specification
**Strategy Source:** S-010 (Self-Refine), S-004 (Pre-Mortem)
**Severity:** Major
**Section:** "Implementation / Phase 1" and Acceptance Criteria

**Evidence from deliverable:**
> "Document the symlink setup in `docs/development/project-tracker-setup.md`"
> (Acceptance criterion) "Symlink setup documented in `docs/development/project-tracker-setup.md` (macOS/Linux symlink, Windows junction alternative)"

**Analysis:** The acceptance criterion implies the document exists and has certain content (symlink setup, Windows alternative). But the issue does not specify:
- Prerequisites (git clone jerry-projects first)
- The exact commands to run on macOS/Linux
- The exact commands to run on Windows
- Whether the `projects/` path must be relative (so it works across developer machines) or whether absolute paths are acceptable
- How to verify the setup worked (e.g., `ls -la projects/` should show the symlink)

For a developer guide that will be used by future framework contributors, these omissions mean the implementer must write a complete technical document without any content guidance from the issue. This is an actionability gap that would generate a low-quality first version of the setup guide.

**Recommended fix:** See R-005-it2.

---

### Minor Findings

#### FINDING-m1-it2: CV-002-it1 Persists — "Full Git History Preservation" Still Underspecified
**Strategy Source:** S-011 (Chain-of-Verification)
**Severity:** Minor
**Section:** "Implementation / Phase 1" and Acceptance Criteria

**Evidence from deliverable:**
> "geekatron/jerry-projects private repository created with history extracted from `projects/`"

The acceptance criterion implies "full history preservation" but does not define what that means. Specifically: do commit SHAs in jerry-projects match jerry's commit SHAs? (No — they are new SHAs created by the split). Can contributors `git blame` a file in jerry-projects and see the original author? (Yes). Does cross-directory commit context survive? (No — commits that changed both `projects/` files and framework files will be split across the two repos).

This is a Minor finding because the practical impact is low (most contributors do not need cross-directory git blame), but for an OSS release record, imprecision in the guarantee statement is notable.

---

#### FINDING-m2-it2: CV-003-it1 Persists — PROJ-001 Naming Anomaly Unaddressed
**Strategy Source:** S-011 (Chain-of-Verification)
**Severity:** Minor
**Section:** Data table

**Evidence from deliverable:**
> "Note on PROJ-001 naming: Three entries use the PROJ-001 identifier (oss-release, oss-documentation, plugin-cleanup). These are separate sub-projects under the PROJ-001 umbrella. The naming convention evolved organically..."

The note explains the anomaly but does not resolve the ambiguity for the data table. The "14 project directories" count in the metrics row needs cross-checking: the table lists 14 rows (including README), but only 11 distinct PROJ-NNN identifiers. The note says "11 with content, 2 empty shells, 1 README" — this matches the table. The PROJ-001 anomaly is now explained but the identifier collision is still present. For a data table used as evidence, identifier collisions should be clarified (e.g., rename to PROJ-001a, PROJ-001b) or footnoted with the actual directory names.

---

#### FINDING-m3-it2: Phase 3 Validation Criterion Unmeasurable
**Strategy Source:** S-012 (FMEA), S-007 (Constitutional)
**Severity:** Minor
**Section:** "Implementation / Phase 3: Validate" and Acceptance Criteria

**Evidence from deliverable:**
> "Plugin installation size reduced by >= 40 MB (measure: compare `du -sh` of Jerry repo with and without `projects/PROJ-*`)"

The acceptance criterion now specifies a measurement approach (`du -sh`) — which is an improvement. However, `du -sh` of the git working tree includes untracked files and git objects. The more precise measurement is `git count-objects -v` or comparing `du -sh .git` with and without the history. For a public OSS claim that "installation size reduced by >= 40 MB," the measurement method should match what users actually experience (a fresh clone size, not a working tree size). Consider: "Measure `du -sh` of a fresh `git clone` without the pre-extraction history vs. the post-extraction clone."

---

#### FINDING-m4-it2: Rollback Step 3 Assumes Force-Push Authority
**Strategy Source:** S-001 (Red Team)
**Severity:** Minor
**Section:** Rollback procedure

**Evidence from deliverable:**
> "3. Force-push only if the migration was already pushed to remote (coordinate with any open PRs)"

Force-pushing to a public OSS repository's main branch after an OSS release requires branch protection bypass. If Jerry has branch protection enabled (likely for an OSS release), force-push to main is prohibited by default. The rollback procedure assumes force-push is available. If branch protection blocks it, the procedure fails. The issue should note: "Ensure branch protection rules allow force-push for the migration period, or use a temporary rollback branch and PR."

---

### S-007 Constitutional AI Findings (CC-NNN-it2)

#### CC-001-it2: Repository Visibility Decision — RESOLVED
**Severity:** Resolved (was Major/FM-003-it1 in Iteration 1)
**Analysis:** The issue now explicitly states "Create `geekatron/jerry-projects` as a **private** repository" with rationale citing PROJ-008 and PROJ-009 sensitivity. The Constitutional concern (inadvertent exposure of sensitive security research) is addressed.

#### CC-002-it2: H-32 GitHub Issue Parity — Still Missing
**Severity:** Minor
**Analysis:** The issue itself is a GitHub Issue draft. However, it does not reference a corresponding internal worktracker entity (story or enabler) that this issue implements. Per H-32, worktracker and GitHub issues must have parity. The "Why now" section references OSS release preparation but does not link a worktracker story/enabler number. This is unaddressed from Iteration 1.

#### CC-003-it2: No Constitutional Violations Found
**Analysis:** The proposal does not affect agent definitions, HARD rules, or governance documents. P-003, P-020, P-022 are not implicated.

---

### S-001 Red Team Findings (RT-NNN-it2)

#### RT-001-it2: CI Pipeline Update — SUBSTANTIALLY ADDRESSED
**Severity:** Resolved (was Critical in Iteration 1)
**Evidence from deliverable:**
> "Update GitHub Actions CI pipeline to ensure no test step assumes `projects/` exists. CI runs on a clean checkout without any symlink — CI MUST pass in this configuration. Add a CI comment or `.github/workflows/` annotation documenting that `projects/` is intentionally absent in CI."

This directly addresses RT-001-it1. The requirement is now explicit and in the acceptance criteria: "GitHub Actions CI pipeline updated to pass without `projects/` directory; no test step assumes its presence." This is correctly specified.

#### RT-002-it2: Repository Visibility — RESOLVED
**Severity:** Resolved (was Critical in Iteration 1)
**Analysis:** Private repository decision now explicit with rationale.

#### RT-003-it2: Branch Protection Rule Interaction with Rollback (New)
**Severity:** Minor
**Analysis:** See FINDING-m4-it2.

#### RT-004-it2: `git-filter-repo --target` Flag Behavior — Risk of Destructive Operation
**Severity:** Critical (new finding)
**Strategy Source:** S-001 (Red Team)
**Section:** "Implementation / Phase 1: Prepare"

**Evidence from deliverable:**
> "If `git-filter-repo` is available, the equivalent is: `git-filter-repo --path projects/ --target <new-repo-path>`"

**Analysis:** `git-filter-repo` with `--path` and `--target` is used to create a new repository from filtered history. However, the `--path` flag without `--source` means the command operates on the **current repository** (Jerry) as its source. By default, `git-filter-repo` **rewrites the current repository's history** to remove everything *not* matching `--path projects/`. This means running this command in the Jerry repo would:
1. Delete all non-`projects/` files from Jerry's history
2. Write the filtered history to `<new-repo-path>`

This is the *opposite* of what is intended. The intended behavior is to create a `jerry-projects` repo containing only the `projects/` subtree — not to strip Jerry down to only `projects/`.

The correct `git-filter-repo` invocation for this use case would be:
```
git clone <jerry-repo> <temp-clone>
cd <temp-clone>
git-filter-repo --path projects/ --subdirectory-filter projects/
git remote add origin <jerry-projects-remote>
git push origin main
```

Or with `--source`:
```
git-filter-repo --source <jerry-repo-path> --target <new-repo-path> --path projects/
```

Without this correction, an implementer following the issue literally and running `git-filter-repo --path projects/ --target <new-repo-path>` in the Jerry repo directory risks catastrophic history corruption (all non-projects files removed from Jerry's history).

**Why it is a problem:** This is a C4 irreversible operation on a public repository. An incorrect `git-filter-repo` invocation without `--source` that is run from the Jerry repo could corrupt Jerry's entire git history. This is the most serious new finding in Iteration 2.

**Recommended fix:** See R-006-it2.

---

### S-004 Pre-Mortem Findings (PM-NNN-it2)

#### PM-001-it2: Long-Term Archival Strategy — Still Missing
**Severity:** Minor (same as Iteration 1, PM-001-it1)
**Analysis:** If `geekatron/jerry-projects` is private and the framework author leaves the project, historical decision records and research artifacts become inaccessible to future maintainers. The issue does not address long-term archival. Now that the visibility decision (private) has been made, this gap is more concrete. A brief note ("long-term visibility reassessment deferred to a separate issue") would close this.

#### PM-002-it2: CI Test Baseline Not Specified
**Severity:** Minor
**Analysis:** PM-002-it1 persists. The issue says verify `document_type.py` and `layered_config_adapter.py` work through symlinks, but does not specify what CI currently tests for these paths. Without a baseline, "verify it still works" is not a meaningful acceptance criterion. One line identifying the relevant test file/fixture would close this.

---

### S-002 Devil's Advocate Findings (DA-NNN-it2)

#### DA-001-it2: Distribution Mechanism — Partially Addressed, One Residual Gap
**Severity:** Minor (downgraded from Major in Iteration 1)
**Evidence from deliverable:**
> "**Distribution mechanism:** Jerry ships as a Claude Code plugin via the `.claude-plugin/` manifest. When users install Jerry through Claude Code's plugin system, the plugin installation clones or downloads the full repository content — including `projects/`. The `projects/` directory is not excluded by any distribution filter, `.npmignore`, or package manifest."

**Analysis:** This substantially addresses DA-001-it1. The mechanism is now specified. However: "clones or downloads the full repository content" is ambiguous — does it clone the git repo (in which case all history is included) or does it download a tarball/zip (in which case only the working tree is included, no git history). If the plugin system downloads a zip, the 41 MB is the working tree size (expected). If it clones, the 41 MB is the working tree plus potentially the full git history (which would be much larger). The exact mechanism matters for the size claim.

**Recommended fix:** Clarify: "plugin installation downloads a zip/tarball (no git history)" or "plugin installation performs a git clone (includes full history)."

#### DA-002-it2: Symlink is a Development Convenience — Acknowledged, Not Resolved
**Severity:** Minor (same as Iteration 1)
**Analysis:** The issue now states the symlink purpose clearly but does not address the deeper assumption that the framework author wants `projects/` to appear to be "inside" Jerry. This is a design preference, not an architectural requirement. The issue should state it as a preference: "The symlink bridge is the selected approach because the framework author's development workflow benefits from having `projects/` accessible within the Jerry working tree."

---

### S-012 FMEA Findings (FM-NNN-it2)

#### FM-001-it2: git subtree split — Risk REDUCED, Residual Risk from git-filter-repo Instruction
| Attribute | Value |
|-----------|-------|
| Component | `git subtree split` + `git-filter-repo` command in Phase 1 |
| Failure Mode | `git-filter-repo` run without `--source` corrupts Jerry's history |
| Effect | All non-`projects/` files removed from Jerry's git history |
| Cause | Missing `--source` flag; ambiguous documentation |
| Severity | 10 (irreversible history corruption on public repo) |
| Occurrence | 4 (implementers unfamiliar with git-filter-repo likely to follow instructions literally) |
| Detection | 2 (immediately apparent after running the command) |
| RPN | 80 — elevated despite low occurrence because severity is maximum |
| Mitigation | Fix the `git-filter-repo` command to include `--source` or rewrite as clone-then-filter procedure. See RT-004-it2. |

#### FM-002-it2: Symlink resolution — Risk STABLE (Addressed in Issue, Not Yet Tested)
| Attribute | Value |
|-----------|-------|
| Component | `document_type.py` + `layered_config_adapter.py` path resolution |
| Failure Mode | `pathlib.Path.glob()` symlink traversal behavior |
| Effect | `jerry projects list` fails for framework author |
| Severity | 5 |
| Occurrence | 3 |
| Detection | 3 |
| RPN | 45 |
| Status | Issue now correctly states "must be tested, not assumed." Acceptance criterion includes test requirement. |

#### FM-003-it2: Security data exposure — RESOLVED
| Status | Resolved: private repository decision made with explicit rationale. |

---

### S-013 Inversion Findings (IN-NNN-it2)

#### IN-001-it2: What Would Make This Issue Fail After Implementation?

Applying inversion: what does failure look like after this issue is implemented?

1. **Failure mode: Framework author's local Jerry setup stops working after symlink.** The `jerry projects` commands require the symlink to be configured. If the framework author clones Jerry on a new machine, they get a non-functional `projects/` path until they configure the symlink. The issue documents the setup, but the `layered_config_adapter.py` config loading may throw on missing directory before the developer can configure it. No graceful fallback for the *developer* case (as opposed to the plugin user case).

   **Finding:** The graceful-handling requirement specifies "exit 0 for plugin users" but the same code path affects the framework author on a fresh clone before symlink setup. The developer experience on fresh clone is unaddressed.

2. **Failure mode: The CI annotation gets stripped out during a later workflow refactor.** The issue says "Add a CI comment or `.github/workflows/` annotation documenting that `projects/` is intentionally absent in CI." A comment is not a test. A future CI refactor could remove the comment without triggering a test failure, silently breaking the "intentionally absent" documentation.

   **Finding:** The CI documentation should be a CI test, not just a comment. A test that explicitly asserts `projects/` does not exist (or that the tests pass without it) is more durable than a comment.

3. **Failure mode: A future contributor adds `projects/` test fixtures back.** Without an explicit CI gate, nothing prevents a future test from assuming `projects/` exists. The acceptance criterion says "no test step assumes its presence" — but there is no mechanism to enforce this continuously.

#### IN-002-it2: What If the Problem Framing Is Wrong?

The issue frames the problem as "plugin users receive project data they don't want." But the Claude Code plugin system may have other distribution controls (sparse clone, LFS, partial download). If the plugin system supports sparse checkout automatically, the `projects/` exclusion might be achievable with a `.gitattributes` export-ignore without any external repository. This possibility is addressed in the alternatives (sparse checkout was rejected because it "requires user action post-clone") — but the rejection does not address whether the *plugin system itself* could configure sparse checkout automatically.

This is a minor alternative scenario, not a decisive objection. The symlink bridge is still the stronger solution. But the dismissal of sparse checkout should acknowledge whether the Claude plugin system offers any native filtering.

---

### S-011 Chain-of-Verification Findings (CV-NNN-it2)

#### CV-001-it2: fnmatch/pathlib Technical Note — SUBSTANTIALLY IMPROVED
**Severity:** Resolved for the primary claim; Minor residual
**Evidence from deliverable:**
> "`fnmatch.fnmatch()` operates on path strings, not filesystem lookups — it will match regardless of symlinks. The question is whether the path strings produced by `pathlib.Path.glob()` or `os.walk()` traversal include or exclude the symlink resolution. On macOS/Linux, `pathlib.Path.glob()` follows symlinks by default. This must be tested, not assumed."

**Analysis:** The Iteration 2 text correctly separates the fnmatch behavior (string matching) from the pathlib traversal (filesystem lookup that follows symlinks). This is technically accurate and is a substantial improvement over "Python's `fnmatch` and `pathlib` resolve symlinks transparently." However, there is a minor residual gap: "On macOS/Linux, `pathlib.Path.glob()` follows symlinks by default" — this is correct, but the behavior can be affected by `follow_symlinks=False` in some Python versions (3.13+ adds explicit parameter). The statement should be: "On macOS/Linux, `pathlib.Path.glob()` follows symlinks by default (Python 3.9-3.12 behavior; behavior may vary in Python 3.13+)."

#### CV-002-it2: "Full Git History Preservation" — Still Underspecified
**Severity:** Minor (same as Iteration 1, CV-002-it1)
**Analysis:** The issue still uses "history extracted from `projects/`" without clarifying what guarantee is being made. See FINDING-m1-it2.

#### CV-003-it2: PROJ-001 Naming — Acknowledged But Not Resolved
**Severity:** Minor (same as Iteration 1, CV-003-it1)
**Analysis:** The note explains the anomaly. See FINDING-m2-it2.

---

### S-010 Self-Refine Findings (SR-NNN-it2)

#### SR-001-it2: Phase 1/2/3 Bridge Sentence — Added and Working
**Severity:** Resolved (was Minor in Iteration 1)
**Evidence from deliverable:**
> "Three phases. Same as any good line: scout the terrain, read the features, commit to the exit."

This is the implementation section bridge sentence requested in Iteration 1. It lands well — "scout the terrain" (Prepare), "read the features" (Update references), "commit to the exit" (Validate) maps cleanly to the three phases. Closes SR-001-it1.

#### SR-002-it2: Phase 2 Audit Scope — RESOLVED
**Severity:** Resolved (was Major in Iteration 1)
**Evidence from deliverable:**
> "Decision: keep the references as-is. They document provenance and do not functionally depend on reading project files at runtime."

The "either approach is acceptable" ambiguity from Iteration 1 is now a decision. This closes SR-002-it1.

#### SR-003-it2: Distribution Mechanism Note Is Partially Self-Referential
**Severity:** Minor
**Evidence from deliverable:**
> "The `projects/` directory is not excluded by any distribution filter, `.npmignore`, or package manifest."

The reference to `.npmignore` is odd for a Python Claude plugin. `.npmignore` is a Node.js packaging construct. Its mention implies the plugin might distribute via npm, which is unlikely for a Python CLI tool. This should be replaced with the Python equivalents: `MANIFEST.in` (for sdist), `.gitattributes` export-ignore, or the plugin manifest's include/exclude rules.

---

## Section 4: Revision Recommendations

| ID | Priority | Finding Source | Section | Issue |
|----|----------|----------------|---------|-------|
| R-001-it2 | Critical | FINDING-C1-it2, RT-004-it2 | Phase 1 git tool guidance | Dual-tool ambiguity + dangerous git-filter-repo usage |
| R-002-it2 | Major | FINDING-M1-it2 | Alternatives Considered | Submodule rejection rationale is factually incorrect |
| R-003-it2 | Major | FINDING-M2-it2 | Rollback procedure | "Coordinate with open PRs" not actionable; jerry-projects deletion caveat |
| R-004-it2 | Major | FINDING-M3-it2 | Multiple | Add hyperlinks to code, milestone link, ADR reference |
| R-005-it2 | Major | FINDING-M4-it2 | Phase 1 + Acceptance Criteria | Specify minimum content for developer guide |
| R-006-it2 | Critical | RT-004-it2 | Phase 1 | Fix git-filter-repo command (missing --source / unsafe invocation) |

---

### R-001-it2 Detail: Resolve Git Tool Recommendation

**Current text (Phase 1):**
> "Extract `projects/` history using `git subtree split --prefix=projects/ HEAD -b projects-split`, then push to the new repo: `git push <jerry-projects-remote> projects-split:main`. Avoid `git filter-branch` (deprecated since Git 2.24 in favor of `git-filter-repo`). If `git-filter-repo` is available, the equivalent is: `git-filter-repo --path projects/ --target <new-repo-path>`."

**Recommended replacement:**
> "Extract `projects/` history using `git subtree split --prefix=projects/ HEAD -b projects-split`, then push to the new repo: `git push <jerry-projects-remote> projects-split:main`. This is the recommended approach — it creates a new branch in the Jerry repo containing only the `projects/` history without modifying Jerry's main history. Avoid `git filter-branch` (deprecated since Git 2.24). Alternative: if `git-filter-repo` is preferred, first create a clone to avoid operating on the live repository: `git clone <jerry-repo-path> /tmp/jerry-projects-extract && cd /tmp/jerry-projects-extract && git-filter-repo --path projects/ --subdirectory-filter projects/ && git remote add origin <jerry-projects-remote> && git push origin main`. Do NOT run `git-filter-repo` directly in the Jerry working directory without a `--source` flag — it will rewrite Jerry's history."

---

### R-002-it2 Detail: Fix Submodule Rejection Rationale

**Current text (Alternatives Considered):**
> "Git submodule: `projects/` becomes a tracked submodule pointing to jerry-projects. Versioned dependency, no OS symlink required. | Rejected: submodule UX is notoriously poor (requires `--recurse-submodules` on clone, confuses contributors unfamiliar with submodule workflows). Does not solve the plugin distribution problem — submodules are included in clone by default unless sparse checkout is configured."

**Recommended replacement:**
> "Git submodule: `projects/` becomes a tracked submodule pointing to jerry-projects. Versioned dependency, no OS symlink required. | Rejected: submodule UX creates friction for contributors (requires `git submodule update --init` after cloning, or `git clone --recurse-submodules`; uninitialized submodule appears as empty directory). While submodule content is NOT included in a plain `git clone` (solving the plugin distribution size problem), the development workflow for the framework author is more complex: every `jerry-projects` change requires a separate commit in Jerry to update the submodule pointer. The symlink bridge provides equivalent access with simpler maintenance."

---

### R-003-it2 Detail: Complete Rollback Procedure

**Current text (Rollback):**
> "3. Force-push only if the migration was already pushed to remote (coordinate with any open PRs)
> 4. Delete the jerry-projects repo if it was already created"

**Recommended replacement:**
> "3. Force-push only if the migration was already pushed to remote. Before force-pushing to main: (a) check for open PRs against the migration commit — `gh pr list --base main` — and close or re-target them; (b) inform any collaborators of the force-push; (c) verify branch protection rules permit force-push (temporary bypass may be required). GitHub does not automatically update PR base branches on force-push.
> 4. Delete the jerry-projects repo if it was already created, provided no external collaborators have cloned it. The jerry-projects repo created in Phase 1 will be private; deletion is clean if only the framework author has access. Confirm this before deletion."

---

### R-004-it2 Detail: Add Hyperlinks and Governance Anchors

Add to "Affected components" section:
- `src/domain/markdown_ast/document_type.py` → link to `https://github.com/geekatron/jerry/blob/main/src/domain/markdown_ast/document_type.py#L98-L106`
- `src/infrastructure/adapters/configuration/layered_config_adapter.py` → link to GitHub file
- `skills/worktracker/rules/worktracker-directory-structure.md` → link to file

Add to "Why now" section:
- Link to the OSS release GitHub milestone or issue (e.g., `See #NNN for the OSS release milestone`)

Add to "Proposed strategy" section (or a new "Governance" section):
- "This change implements a physical separation of the workbench from the tool, formalizing the conceptual distinction already documented in `skills/worktracker/rules/worktracker-directory-structure.md` (project-based vs. repository-based placement patterns). An ADR documenting this architectural separation decision SHOULD be created: see `docs/design/` for the ADR format."

Add acceptance criterion:
- "`geekatron/jerry-projects` repository URL added to this issue after creation"

---

### R-005-it2 Detail: Specify Developer Guide Minimum Content

**Add to Phase 1 (after "Document the symlink setup"):**

> "The `docs/development/project-tracker-setup.md` guide MUST include:
> 1. **Prerequisites:** git clone of `geekatron/jerry-projects` at a local path of your choice
> 2. **macOS/Linux setup:** `ln -s <path-to-jerry-projects> <path-to-jerry>/projects`
> 3. **Windows setup (Developer Mode):** `mklink /D projects <path-to-jerry-projects>` (run from Jerry directory)
> 4. **Windows setup (WSL2 alternative):** Use WSL2 with the macOS/Linux instructions
> 5. **Windows setup (no elevated privileges):** `mklink /J projects <path-to-jerry-projects>` (directory junction)
> 6. **Verification:** `ls -la projects/` (macOS/Linux) or `dir projects` (Windows) should show the symlink or junction
> 7. **Note:** The symlink is not tracked by git; it must be recreated when cloning Jerry on a new machine"

---

### R-006-it2 Detail: Fix git-filter-repo Command (Critical Safety Fix)

This is subsumed into R-001-it2 — see that recommendation. The key fix is: do NOT present `git-filter-repo --path projects/ --target <new-repo-path>` as a safe single-line command without the explicit `--source` flag or the clone-first procedure.

---

## Section 5: Voice Assessment

### Saucer Boy Persona Compliance

**Overall Voice Score: 9.5/10** (improved from 9/10 in Iteration 1)

**What the revision added (positive):**

The requested bridge sentence is now present and it lands:
> "Three phases. Same as any good line: scout the terrain, read the features, commit to the exit."

This is textbook McConkey. The skiing-to-implementation mapping is clean: scouting terrain = Prepare (you don't commit without reading), reading features = Update references (technical due diligence), commit to exit = Validate (no second-guessing on the way down). The rhythm is good. Three short clauses. No wasted words.

**Existing voice elements that hold up under re-examination:**
- "Your plugin cache should be a quiver, not a garage sale." — Still the best line in the issue.
- "Ship the skis, not the trip journal." — Precise. Framework = skis. Projects = trip journal. The semantic compression is elegant.
- "The mountain doesn't care about your trip journal. But your pack weight cares a lot." — The callback at the close still works. The "but" creates the turn — the mountain's indifference is abstract; pack weight is concrete. That contrast is McConkey's move: the peak doesn't care about your gear drama, but gravity does.

**What prevents 10/10:**
The "Technical note" paragraph in Phase 2 (`fnmatch.fnmatch()` operates on path strings, not filesystem lookups...) is necessarily technical but reads as a completely different voice — consulting engineering, not McConkey. This is appropriate for the content, but the transition back to technical voice in the middle of the implementation section creates a minor friction. The issue would benefit from one sentence before the technical note that re-anchors: "Before you drop in, know your terrain." or similar. This is a preference, not a defect.

**Voice integrity check:** None of the new revision text clashes with the McConkey persona. The rollback procedure is necessarily dry and should be — McConkey does not freestyle when someone's in a tree well. Technical precision in dangerous moments is its own form of voice discipline.

---

## Section 6: Gap Analysis to 0.95

### Current Score: 0.87 | Target: 0.95 | Gap: 0.08

The gap has closed from 0.18 (Iteration 1) to 0.08 (Iteration 2). This is real progress. The remaining gap is addressable in Iteration 3 but requires discipline.

### Dimension-Level Gap Analysis

| Dimension | Current | Target | Gap | Closing Action |
|-----------|---------|--------|-----|----------------|
| Completeness | 0.88 | 0.95 | 0.07 | Add developer guide content spec, worktracker link, measurement method for size criterion |
| Internal Consistency | 0.87 | 0.95 | 0.08 | Fix git tool dual-recommendation; this single fix raises the score materially |
| Methodological Rigor | 0.87 | 0.95 | 0.08 | Fix submodule rejection rationale; fix git-filter-repo safety issue; add risk register |
| Evidence Quality | 0.90 | 0.95 | 0.05 | Verify distribution mechanism (zip vs. git clone); attribute line count source |
| Actionability | 0.88 | 0.95 | 0.07 | Specify developer guide content; complete rollback coordination step |
| Traceability | 0.78 | 0.93 | 0.15 | Add 5-6 hyperlinks + milestone link + ADR reference. This is the largest gap. |

### What Drives the Remaining Gap

**Traceability (0.78 → 0.93):** This is the largest single gap and has the highest improvement leverage per unit of effort. Adding 5-6 hyperlinks and a milestone reference requires approximately 15 minutes of work and would contribute 0.015 to the composite score. The ADR reference requires one sentence.

**Internal Consistency (0.87 → 0.95):** Resolving the git tool dual-recommendation (R-001-it2) is a single paragraph rewrite that closes a genuine implementer confusion. This would raise Internal Consistency to ~0.93, contributing 0.012 to the composite.

**Methodological Rigor (0.87 → 0.95):** Fixing the submodule rejection rationale (R-002-it2) and the git-filter-repo safety issue (R-006-it2) are both targeted text changes. Together, they close the precision gap without requiring new sections.

**Projected Iteration 3 Score** (if R-001-it2 through R-006-it2 all applied):

| Dimension | Current | Post-R-001-to-006 | Gain |
|-----------|---------|-------------------|------|
| Completeness | 0.88 | 0.92 | +0.04 |
| Internal Consistency | 0.87 | 0.93 | +0.06 |
| Methodological Rigor | 0.87 | 0.93 | +0.06 |
| Evidence Quality | 0.90 | 0.93 | +0.03 |
| Actionability | 0.88 | 0.93 | +0.05 |
| Traceability | 0.78 | 0.93 | +0.15 |
| **Composite** | **0.87** | **~0.928** | **+0.058** |

Iteration 3 projection: ~0.928 — approaching standard threshold (0.92) but still below the C4 elevated threshold (0.95). The remaining gap from 0.928 to 0.95 in Iteration 4 will require:

1. Verification evidence for the fnmatch/pathlib behavior (a passing test result cited in the issue)
2. Clarification of "full history preservation" guarantee
3. Any remaining precision gaps surfaced in Iteration 3 review

### Honest Assessment

The issue is well-built and getting better. The core architectural argument is sound. The revisions applied in Iteration 2 demonstrate good-faith engagement with the Iteration 1 findings — 9 Critical/Major gaps were closed. The remaining gap is dominated by two categories:

1. **Traceability** — the easiest gap to close (hyperlinks, milestone link, ADR note) but requires knowing the actual GitHub URLs
2. **Methodological precision** — specifically the git tool recommendation section, which now contains a genuinely dangerous instruction (the `git-filter-repo` command without `--source`) that must be fixed before any implementation begins

The `git-filter-repo` safety issue (RT-004-it2, FINDING-C1-it2) is the most urgent finding in Iteration 2. It is not a quality polish item — it is a command that, if followed literally, risks irreversible corruption of Jerry's git history on a public OSS repository. This must be addressed before the issue is filed.

---

## Section 7: Delta Analysis

### What Improved from Iteration 1 to Iteration 2

| Finding | Iteration 1 Severity | Iteration 2 Status | Evidence |
|---------|---------------------|-------------------|---------|
| No alternatives analysis (FINDING-C1) | Critical | Resolved | "Alternatives Considered" table added with 5 options |
| No rollback plan (FINDING-C2) | Critical | Resolved (with caveats) | 4-step rollback procedure added |
| `git filter-branch` deprecated (FINDING-C3) | Critical | Resolved (with new issue) | `git subtree split` + `git-filter-repo` now documented |
| Windows symlink missing (FINDING-M1) | Major | Resolved | Windows note with `mklink /D` and WSL2 alternative added |
| Missing relative repo size (FINDING-M2) | Major | Resolved | 60 MB total, 19 MB without `projects/`, percentages added |
| CLI "graceful" underspecified (FINDING-M3) | Major | Resolved | Exit code 0 + exact message specified |
| Contributor migration missing (FINDING-M4) | Major | Resolved | CHANGELOG entry + contributor guidance added |
| `projects/README.md` ambiguity (FINDING-M5) | Major | Resolved | Stub stays in Jerry; table updated |
| CI pipeline update missing (RT-001) | Critical | Resolved | Explicit requirement in Phase 2 + acceptance criteria |
| Repository visibility missing (RT-002) | Critical | Resolved | Private with rationale |
| Distribution mechanism unclear (DA-001) | Major | Substantially resolved | Claude Code plugin + `.claude-plugin/` manifest specified |
| Bridge sentence missing (SR-001) | Minor | Resolved | "Three phases. Same as any good line..." added |
| Phase 2 audit deferred (SR-002) | Major | Resolved | "Decision: keep as-is" stated |
| fnmatch/pathlib claim imprecise (CV-001) | Major | Substantially resolved | String vs. filesystem distinction now correct |

**14 findings from Iteration 1 closed or substantially addressed.** This is strong execution against the revision recommendations.

---

### What Regressed from Iteration 1 to Iteration 2

| Issue | Analysis |
|-------|---------|
| Git tool recommendation now has two options | The introduction of `git-filter-repo` as an alternative (correctly replacing the deprecated `git filter-branch`) created a new ambiguity. Iteration 1 had one (wrong) tool; Iteration 2 has two (correct but undifferentiated) tools. The attempt to provide a modern alternative introduced choice paralysis. |
| `git-filter-repo` command is dangerous without `--source` | The new recommendation contains a command that, run literally in the Jerry repo, would rewrite history destructively. This is a new Critical finding introduced by the revision. |

---

### What Remains Unaddressed from Iteration 1

| Finding | Iteration 1 Severity | Still Present | Notes |
|---------|---------------------|---------------|-------|
| No link to affected code files (FINDING-m2) | Minor | Yes | Line numbers added but no GitHub URLs |
| "Why now" missing external link (FINDING-m3) | Minor | Yes | OSS release mentioned but not linked |
| "Full history preservation" underspecified (CV-002) | Major | Yes (as minor) | Still imprecise; lower impact now |
| PROJ-001 naming anomaly (CV-003) | Minor | Yes | Note added but not resolved |
| No ADR reference (CC-001/SM-008) | Minor | Yes | Pattern of non-address makes this Major in aggregate |
| Worktracker entity link (CC-001) | Minor | Yes | |
| Long-term archival strategy (PM-001) | Major | Yes (as minor) | Private repo makes this more concrete |

---

### New Findings Introduced in Iteration 2

| Finding | Severity | Source | Description |
|---------|---------|--------|-------------|
| FINDING-C1-it2 | Critical | RT-004-it2 | `git-filter-repo` command without `--source` is destructively unsafe |
| FINDING-M1-it2 | Major | S-002, S-013 | Submodule rejection rationale is factually incorrect |
| FINDING-M2-it2 | Major | S-004, S-012 | Rollback "coordinate with PRs" step is not actionable |
| FINDING-m4-it2 | Minor | S-001 | Rollback assumes force-push authority; branch protection not addressed |
| IN-001-it2 (sub) | Minor | S-013 | Developer fresh-clone experience before symlink setup is unaddressed |

---

## Execution Statistics

| Strategy | Finding Prefix | Critical | Major | Minor | Protocol Steps |
|----------|---------------|---------|-------|-------|----------------|
| S-014 (LLM-as-Judge) | LJ-NNN-it2 | 0 | 0 | 0 | 7/7 (scoring) |
| S-003 (Steelman) | SM-NNN-it2 | 0 | 2 | 3 | 6/6 |
| S-013 (Inversion) | IN-NNN-it2 | 0 | 1 | 1 | Contributed to M1, m5 |
| S-007 (Constitutional) | CC-NNN-it2 | 0 | 1 | 1 | 5/5 |
| S-002 (Devil's Advocate) | DA-NNN-it2 | 0 | 0 | 2 | Contributed to M1 |
| S-004 (Pre-Mortem) | PM-NNN-it2 | 0 | 1 | 2 | 4/4 |
| S-010 (Self-Refine) | SR-NNN-it2 | 0 | 1 | 1 | 4/4 |
| S-012 (FMEA) | FM-NNN-it2 | 1 | 0 | 1 | 5/5 (FMEA tables) |
| S-011 (Chain-of-Verification) | CV-NNN-it2 | 0 | 0 | 2 | 5/5 |
| S-001 (Red Team) | RT-NNN-it2 | 1 | 0 | 1 | 4/4 |
| **Totals** | | **2** | **6** | **14** | **10/10 strategies** |

**Total Findings: 22** (down from 21 in Iteration 1; net finding reduction despite iteration progress because 14 findings closed and 5 new ones introduced)

---

*Adversarial Review Version: Iteration 2 of 5*
*Strategy: C4 Tournament (all 10 strategies)*
*H-16 Compliance: S-003 before S-002, S-004, S-001 — CONFIRMED*
*Anti-leniency: Active — lower adjacent score assigned when uncertain*
*Agent: adv-executor (adv-scorer integrated)*
