# C4 Tournament Adversarial Review — Iteration 3 of 5
## Deliverable: GitHub Issue Draft — Extract Project Tracker from Plugin Repository

> **Execution Context**
> - **Deliverable:** `work/gh-issues/issue-project-tracker-extraction.md`
> - **Criticality:** C4 (OSS release preparation; architectural separation; public-facing repository change)
> - **Tournament Iteration:** 3 of 5 | Elevated Threshold: >= 0.95
> - **Executed:** 2026-02-25
> - **H-16 Compliance:** S-003 (Steelman) executed before S-002, S-004, S-001 — SATISFIED
> - **Strategies:** S-014, S-003, S-013, S-007, S-002, S-004, S-010, S-012, S-011, S-001 (all 10)
> - **Prior Iteration Score:** 0.87 (REVISE) | Revision count: R-001-it2 through R-006-it2 applied

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

**Finding Prefix:** LJ-NNN-it3 (Iteration 3)

**Anti-leniency bias active.** When uncertain between adjacent scores, the lower score is assigned. All score justifications require specific evidence from the deliverable text.

---

### Dimension 1: Completeness (Weight: 0.20)

**Score: 0.92**

**Evidence for score:**

**Additions confirmed from Iteration 2 recommendations (positive):**

- **Developer guide content specified (R-005-it2 closed).** Phase 1 now includes a 7-item outline: prerequisites, macOS/Linux setup, Windows Developer Mode setup, WSL2 alternative, Windows junction alternative, verification step, fresh-clone note. This is the content minimum that was missing in Iteration 2. "The symlink is local to your machine — it is not tracked by git and must be recreated on each fresh clone" — precisely what was needed.
- **Size measurement method specified (FINDING-m3-it2 substantially closed).** Phase 3 now reads: "Measurement: perform a fresh `git clone` of the post-extraction Jerry repo and compare `du -sh` against the pre-extraction tag checkout." The gap around measurement method is closed; the fresh-clone specification is correct and matches what plugin users actually receive.
- **History preservation guarantee clarified (FINDING-m1-it2 closed).** Acceptance criteria now read: "History preservation guarantee: per-file `git log` and `git blame` for files within `projects/` are preserved; commit SHAs will differ from Jerry's; cross-directory commit context (commits touching both `projects/` and framework files) is split across the two repos." This is accurate and actionable. CV-002-it1/FINDING-m1-it2 is closed.
- **Developer fresh-clone experience addressed (IN-001-it2 closed).** Phase 2 now explicitly notes: "This graceful handling also covers the framework author's fresh clone before symlink setup — the experience should be identical to the plugin user case until the symlink is configured." IN-001-it2 is closed.
- **Long-term visibility deferred explicitly (PM-001-it2 closed).** Acceptance criteria include: "Repository visibility confirmed as private; content review and long-term visibility reassessment deferred to a separate issue." PM-001-it2 is closed.
- **fnmatch Python version note added (CV-001-it2 residual closed).** The technical note now specifies: "Python 3.9-3.12 behavior; Python 3.13+ adds an explicit `follow_symlinks` parameter." This closes the residual from CV-001-it2.
- **PROJ-001 naming clarified with directory names.** "Note on PROJ-001 naming: Three filesystem directories use the PROJ-001 prefix: `PROJ-001-oss-release/`, `PROJ-001-oss-documentation/`, and `PROJ-001-plugin-cleanup/`." Directory names now serve as disambiguating identifiers in the data table. This substantially closes FINDING-m2-it2.
- **Repository URL acceptance criterion added.** "Repository URL added to this issue after creation" — FINDING-M3-it2's acceptance criterion sub-item is now present.

**Remaining completeness gaps:**

- **H-32 worktracker entity link still absent.** The issue references Jerry's OSS release milestone (linked in "Why now") but does not reference the internal worktracker entity (story or enabler number) that this GitHub Issue implements. Per H-32, both must be present. This was CC-002-it2 (Minor) — still unaddressed. Impact: low for external readers; pattern violation for H-32 compliance.
- **`.context/rules/` audit scope still unquantified.** Phase 2 says "Audit all `projects/` path references in `.context/rules/` files" but does not state how many files or references are involved. An implementer cannot size this work item. This was partially noted in FINDING-M4 in Iteration 1 and remains a minor actionability gap.
- **No baseline CI test identification for symlink path tests.** Phase 3 says "verify `document_type.py` path patterns work correctly through a symlink" and "test added with symlinked fixture" in acceptance criteria, but the existing test file/fixture name is not specified. An implementer starting fresh does not know which tests already exist for this path. PM-002-it2 persists.
- **`distribution mechanism` precision gap persists.** "The plugin installation clones the full repository content" — the distinction between git clone (including full history) vs. tarball download (working tree only) is not clarified. DA-001-it2 residual persists. The 41 MB figure is the working tree; if it is a git clone, the total download is significantly larger.

**Score justification:** 0.92 — Very strong progress from 0.88. Developer guide content, measurement method, history guarantee, fresh-clone experience, visibility deferral, and fnmatch version are all now addressed. Four completeness gaps remain: H-32 worktracker link (Minor), audit scope unquantified (Minor), baseline CI test unidentified (Minor), distribution mechanism precision (Minor). The score rises from 0.88 to 0.92 because the previously Major-impact completeness items have been closed; remaining gaps are Minor.

---

### Dimension 2: Internal Consistency (Weight: 0.20)

**Score: 0.93**

**Evidence for score:**

**Consistency improvements (positive):**

- **Git tool recommendation is now unambiguous (FINDING-C1-it2 resolved).** The issue now reads: "`git subtree split` is the recommended approach — it creates a new branch in the Jerry repo containing only the `projects/` history without modifying Jerry's main history... Alternative: if `git-filter-repo` is preferred, first create a disposable clone to avoid operating on the live repository... Do NOT run `git-filter-repo` directly in the Jerry working directory without a `--source` flag — it will rewrite Jerry's history, removing all non-`projects/` files. This is irreversible." Primary tool is clear. Alternative is clearly secondary and safety-gated. Internal consistency between the primary recommendation and the alternative is restored.
- **`git subtree` usage disambiguation.** The alternatives table lists "Git subtree (embedded)" as rejected because it doesn't reduce installation size. The implementation uses `git subtree split` for *extraction*, not embedding. These are different operations with different effects. The issue does not explicitly disambiguate these two uses of the word "subtree" — but this surface confusion is diminished because the implementation section now labels the operation "recommended approach" with a rationale. The residual confusion is minor compared to Iteration 2.
- **Rollback + branch protection now consistent.** Rollback step 3 now reads: "verify branch protection rules permit force-push (temporary bypass may be required — re-enable immediately after)." This acknowledges the force-push authority gap identified in FINDING-m4-it2 / RT-003-it2. Internally consistent with the OSS release context where branch protection is expected.

**Remaining or new inconsistencies:**

1. **"git subtree" terminology still ambiguous in the Alternatives table vs. Implementation.** The Alternatives Considered table entry "Git subtree (embedded)" is listed as rejected with rationale: "Does not reduce installation size." The implementation section uses `git subtree split` — a command from the same `git subtree` tool family, but for a completely different purpose (extraction vs. embedding). A reader who sees "Git subtree: REJECTED" in the table and then `git subtree split` in the implementation will experience a naming collision even with the labels. The table entry could be renamed "Git subtree (in-place, embedded)" and the implementation note could say "Note: `git subtree split` is used here for history extraction only — not for the rejected in-place embedding approach." This is Minor because the current text is not technically wrong; it is confusing.

2. **Size criterion: 41 MB vs. ">= 40 MB" threshold.** The data table shows `projects/` = 41 MB. Phase 3 acceptance criterion: "Plugin installation size reduced by >= 40 MB." The 41 MB figure in the data table is the working tree size of `projects/`. The criterion says >= 40 MB reduction — achievable if the working tree shrinks by 40 MB. However: the `fresh git clone` measurement specified in Phase 3 measures the full clone (git objects + working tree). The git object store for `projects/` history may significantly exceed the working tree size. The 41 MB → >= 40 MB claim needs verification against the fresh clone measurement, not just the working tree measurement. Minor inconsistency: the measurement specification (fresh clone) and the data table claim (41 MB working tree size) may not align on what number to expect.

**Score justification:** 0.93 — Major improvement from 0.87. Primary critical inconsistency (git tool dual-recommendation) resolved. Rollback/branch-protection consistency added. Remaining inconsistencies are minor naming confusion and a measurement scope question. Score rises materially because the implementation-ambiguity-for-a-C4-irreversible-operation concern is addressed.

---

### Dimension 3: Methodological Rigor (Weight: 0.20)

**Score: 0.92**

**Evidence for score:**

**Rigor improvements (positive):**

- **Submodule rejection rationale corrected (FINDING-M1-it2 / R-002-it2 resolved).** New text: "submodule content is NOT included in a plain `git clone` (solving the plugin distribution size problem), but the development workflow for the framework author is more complex: every change to `jerry-projects` requires a separate commit in Jerry to update the submodule pointer — ongoing maintenance overhead the symlink bridge avoids entirely." This is factually correct. The previous error ("submodules are included in clone by default") is removed. The rejection now rests on correct grounds: UX friction and maintenance overhead. FINDING-M1-it2 is closed.
- **`git-filter-repo` safety protocol correct (RT-004-it2 / R-006-it2 closed).** The bold safety warning and clone-first procedure are present: "Do NOT run `git-filter-repo` directly in the Jerry working directory without a `--source` flag — it will rewrite Jerry's history, removing all non-`projects/` files. This is irreversible." The clone-first procedure is specified in full (6 commands). The critical risk from Iteration 2 is eliminated.
- **Rollback procedure is now specific (FINDING-M2-it2 / R-003-it2 resolved).** Step 3 now reads: "(a) check for open PRs against the migration commit — `gh pr list --base main` — and close or re-target them; (b) verify branch protection rules permit force-push (temporary bypass may be required — re-enable immediately after); (c) inform any collaborators of the force-push." Step 4 adds: "The repo will be private; deletion is clean if only the framework author has access. Confirm before deleting." FINDING-M2-it2 is closed.

**Remaining rigor gaps:**

1. **No risk register.** This was FM-001-it1 through FM-003-it1 in Iteration 1 and a gap noted again in Iteration 2. A C4 irreversible operation with a known high-RPN failure mode (git history rewrite) would benefit from even a two-row risk table. The FMEA findings from the adversarial review are not reflected in the issue itself. This is a MEDIUM gap for rigor — the absence is noted but the implementation sections adequately describe the mitigations even without a formal table.

2. **Distribution mechanism precision gap (DA-001-it2 residual).** "The plugin installation clones the full repository content" — the type of clone (full git clone vs. tarball download) determines the actual installation footprint. If users receive a git clone, they receive git history plus working tree, making the download potentially much larger than 41 MB. If they receive a tarball, 41 MB is approximately right. This distinction has direct methodological impact on the size-reduction claim. Still asserted, not evidenced.

3. **`.context/rules/` audit scope unspecified.** Phase 2: "Audit all `projects/` path references in `.context/rules/` files." How many references? An implementer cannot size this task. A one-line count ("approximately N references across M files") would close this.

4. **The claim "The `projects/` directory is not excluded by any distribution filter, `.gitattributes` export-ignore, or plugin manifest include/exclude rule"** — this is now more precisely stated than Iteration 1's `.npmignore` reference (which has been updated to `.gitattributes export-ignore`). But the claim is still asserted without inspection evidence. For a C4 issue, "not excluded by any filter" should cite a negative result from inspection: "I checked the `.claude-plugin/` manifest and `.gitattributes` — no exclusion rules present."

**Score justification:** 0.92 — Strong improvement from 0.87. The most critical rigor gap (git-filter-repo safety) is fully closed. Submodule rejection rationale is corrected. Rollback procedure is complete. Remaining gaps are: no risk register (MEDIUM), distribution mechanism asserted not evidenced (Minor), audit scope unquantified (Minor), no exclusion inspection evidence (Minor).

---

### Dimension 4: Evidence Quality (Weight: 0.15)

**Score: 0.91**

**Evidence for score:**

**Evidence improvements (positive):**

- **Fresh-clone measurement method specified.** Phase 3: "Measurement: perform a fresh `git clone` of the post-extraction Jerry repo and compare `du -sh` against the pre-extraction tag checkout. Fresh clone size (not working tree of an existing checkout) represents what plugin users actually receive." This is a technically sound measurement specification. It compares apples to apples (both measurements use the same checkout method). This closes FINDING-m3-it2 substantially.
- **History preservation guarantee now has specific claims.** The acceptance criterion distinguishes: "per-file `git log` and `git blame` for files within `projects/` are preserved; commit SHAs will differ from Jerry's; cross-directory commit context is split." These are verifiable specific claims. The "full history preservation" vagueness from Iterations 1 and 2 is resolved.
- **Submodule evidence now accurate.** The rejection rationale correction (submodules NOT included in plain clone) removes the incorrect claim that was weakening evidence quality.

**Remaining evidence gaps:**

1. **"Total lines in `projects/`": 635,075** — still no source cited for this count. Was this from `find projects/ -name "*.md" | xargs wc -l`? `git ls-files projects/ | xargs wc -l`? `cloc projects/`? Specific numbers without methodology weaken evidence quality. This was noted in Iteration 2 — still present.

2. **Distribution mechanism: "clones the full repository content"** — still not evidenced. If the `.claude-plugin/` manifest specifies the installation method, a direct quote or reference to that manifest would close this. Without it, the claim is plausible but unverified.

3. **"Git clone time and disk usage reduced for new contributors"** — still unquantified. Now less prominent given the fresh-clone measurement spec, but the claim in the Phase 3 list is still not supported by any baseline measurement.

4. **The fresh-clone measurement method has a subtle gap:** comparing `du -sh` of a fresh post-extraction clone against a fresh checkout of the `pre-extraction-tag` is sound. However: the pre-extraction tag lives in Jerry's history. A fresh clone of the current main branch will not have the pre-extraction working tree. The measurement procedure should specify: "checkout the pre-extraction tag in a separate clone, measure; then clone the extraction-complete main, measure; compare." Without this clarification, the measurement comparison method is ambiguous for an implementer doing it for the first time.

**Score justification:** 0.91 — Improvement from 0.90. Fresh-clone measurement and history guarantee are genuine evidence quality improvements. Deductions for unattributed line count, unverified distribution mechanism, and ambiguous comparison procedure. Not reaching 0.93 because two supporting claims (line count, distribution mechanism) remain unattributed assertions.

---

### Dimension 5: Actionability (Weight: 0.15)

**Score: 0.93**

**Evidence for score:**

**Actionability improvements (positive):**

- **Developer guide content specified (FINDING-M4-it2 / R-005-it2 closed).** The 7-item numbered list in Phase 1 provides implementers with the exact content requirements: prerequisites, setup commands (macOS/Linux, Windows Developer Mode, WSL2, junction), verification step, and fresh-clone note. An implementer can write `docs/development/project-tracker-setup.md` directly from this outline. This was the largest Actionability gap in Iteration 2.
- **Rollback step 3 is now actionable (FINDING-M2-it2 closed).** "check for open PRs against the migration commit — `gh pr list --base main` — and close or re-target them" is a specific command and action. "inform any collaborators" is still vague but the PR-specific guidance is now present.
- **Branch protection acknowledgment.** Step 3(b): "verify branch protection rules permit force-push (temporary bypass may be required — re-enable immediately after)" — this is actionable and addresses FINDING-m4-it2.
- **Jerry-projects deletion caveat.** Step 4: "The repo will be private; deletion is clean if only the framework author has access. Confirm before deleting." This is the caveat from FINDING-M2-it2/R-003-it2 — now present.
- **Developer fresh-clone experience explicit.** "This graceful handling also covers the framework author's fresh clone before symlink setup" — IN-001-it2 is closed.

**Remaining actionability gaps:**

1. **Rollback: "inform any collaborators" still vague.** Step 3(c): "inform any collaborators of the force-push" — this is better than Iteration 2's "coordinate with any open PRs" but still does not specify: inform them of what? That the migration is being rolled back? That their local branches may need rebase? One sentence would close this: "Notify collaborators that the migration commit has been reverted; local branches referencing the migration commit must be rebased against the restored history."

2. **`.context/rules/` audit is unscoped.** Phase 2: "Audit all `projects/` path references in `.context/rules/` files." How many files? How many references? An implementer cannot plan this subtask. This was also noted in Completeness — minor but persistent.

3. **Phase 3 measurement procedure for size comparison has the ambiguous comparison issue noted in Evidence Quality** — the implementer needs to know to compare pre-extraction-tag checkout (not just current main) against post-extraction clone.

4. **Acceptance criteria: "All path references in `.context/rules/` audited; kept as historical provenance (documented)"** — this is an acceptance criterion but it is not verifiable. What does "documented" mean? A comment in each file? A summary table? One specific artifact.

**Score justification:** 0.93 — Substantial improvement from 0.88. Developer guide content, rollback specificity, and branch protection acknowledgment are all now actionable. Remaining gaps are minor: inform-collaborators vagueness, audit scope, measurement comparison procedure, and acceptance criterion verifiability.

---

### Dimension 6: Traceability (Weight: 0.10)

**Score: 0.90**

**Evidence for score:**

**Traceability improvements (positive):**

- **Hyperlinks to affected code files added (FINDING-M3-it2 / R-004-it2 substantially closed).** The Affected Components section now includes:
  - `[**src/domain/markdown_ast/document_type.py**](https://github.com/geekatron/jerry/blob/main/src/domain/markdown_ast/document_type.py#L98-L106)` — hyperlinked with line numbers
  - `[**src/infrastructure/adapters/configuration/layered_config_adapter.py**](https://github.com/geekatron/jerry/blob/main/src/infrastructure/adapters/configuration/layered_config_adapter.py)` — hyperlinked
  This directly addresses the traceability gap from Iterations 1 and 2.
- **OSS release milestone linked (R-004-it2 closed).** "Why now" section includes: "see [OSS Release milestone](https://github.com/geekatron/jerry/milestone/1)." This closes the external navigation gap for the upstream project context.
- **Governance note with ADR reference (R-004-it2 closed).** "This change formalizes the physical separation between the framework (tools, skills, code) and the framework author's workbench (project data, research artifacts, orchestration outputs). The conceptual distinction already exists in [worktracker directory structure standards]... An ADR documenting this architectural separation decision SHOULD be created in `docs/design/`." The ADR anchor is present. FINDING-M3-it2 / CC-001-it2 governance gap is substantially closed.
- **Repository URL acceptance criterion added (R-004-it2 closed).** "Repository URL added to this issue after creation" — traceable handoff from issue authoring to implementation phase.

**Remaining traceability gaps:**

1. **`skills/worktracker/rules/worktracker-directory-structure.md` is referenced but linked inline only in governance note.** The prose in "Plugin user experience" section references this file by path (`skills/worktracker/rules/worktracker-directory-structure.md`) without a hyperlink. The governance note links it — but the "Plugin user experience" prose reference is unlinked. Minor inconsistency.

2. **H-32 worktracker entity link still absent.** The GitHub issue does not reference the internal worktracker story or enabler that this issue implements. Per H-32 (GitHub Issue parity for jerry repo work items), both sides need a cross-reference. "Why now" links the OSS milestone but does not cite the internal entity (e.g., "Implements story STORY-NNN"). This has been Minor in both prior iterations — still unaddressed.

3. **The worktracker-directory-structure.md reference in governance note** uses a hyperlink but the link text wraps the rule file name, not a GitHub URL. Technically fine — a GitHub Issues render will not hyperlink a relative path. A full GitHub URL would be more navigable for external contributors.

4. **No ADR created yet.** The issue says an ADR "SHOULD be created in `docs/design/`" — it is referenced but not linked. This is appropriate for a to-be-created artifact; the acceptance criteria do not include "ADR created" as a required gate. For a C4 architectural decision, the absence of a required ADR is notable. Consider whether this should be an acceptance criterion or a separate issue. This is a judgment call rather than a defect.

**Score justification:** 0.90 — Substantial improvement from 0.78. The four hyperlinks, milestone link, and governance/ADR reference bring traceability from a weak dimension to a strong one. Remaining gaps: `worktracker-directory-structure.md` unlinked in prose (Minor), H-32 worktracker entity link (Minor), ADR not required as acceptance criterion (design choice, not a defect). The 0.78 → 0.90 gain of +0.12 is the largest dimensional improvement in Iteration 3.

---

### Composite Score Calculation

| Dimension | Weight | Score | Weighted Score |
|-----------|--------|-------|----------------|
| Completeness | 0.20 | 0.92 | 0.184 |
| Internal Consistency | 0.20 | 0.93 | 0.186 |
| Methodological Rigor | 0.20 | 0.92 | 0.184 |
| Evidence Quality | 0.15 | 0.91 | 0.137 |
| Actionability | 0.15 | 0.93 | 0.140 |
| Traceability | 0.10 | 0.90 | 0.090 |
| **Composite** | **1.00** | | **0.921** |

**Composite Score: 0.921**

**Verdict: REVISE** (threshold 0.95 elevated; gap = 0.029; standard threshold 0.92 gap = 0.001 — would barely pass standard gate)

**Leniency Bias Check:** Completeness held at 0.92 (not 0.94) because four minor gaps remain: H-32 worktracker link, audit scope unquantified, baseline CI test unidentified, distribution mechanism precision. Methodological Rigor held at 0.92 (not 0.94) because no risk register exists and two claims remain asserted-not-evidenced. Evidence Quality held at 0.91 (not 0.93) because the line count has no source and the distribution mechanism type is still unverified. Traceability held at 0.90 (not 0.93) because two minor links remain absent. No score was inflated beyond what the specific text warrants.

---

## Section 2: S-003 Steelman

**Finding Prefix:** SM-NNN-it3

### Summary

**Steelman Assessment:** The deliverable has made decisive progress in Iteration 3. All six Critical and Major findings from Iteration 2 are resolved. The issue is now substantially correct in its technical claims, complete in its implementation guidance, and safe to execute. The Iteration 2 regression (dangerous `git-filter-repo` command) is eliminated. The factual error in the submodule rationale is corrected. The traceability gap has been substantially closed.

**Improvement Count since Iteration 2:** 8 Major/Critical gaps closed. Net finding count trending downward. No new regressions introduced.

**Core argument strength:** Remains valid and is now well-supported across all dimensions. The fresh-clone measurement specification, history guarantee, and developer guide content elevate the issue from "nearly complete" to "production-ready for filing."

---

### Strongest Form of the Argument

The deliverable's strongest form at Iteration 3 is:

**This is a clean, well-evidenced, technically correct pre-release housekeeping operation with a reversible implementation plan and no known safety risks.** The 67%/63% statistics remain the decisive evidence: two-thirds of the repository is operational data that zero plugin users need. The symlink bridge achieves the three-way optimization that no alternative can match. The `git subtree split` primary recommendation is now clearly differentiated from the `git-filter-repo` alternative, with a bold safety warning and clone-first procedure that eliminates the catastrophic risk from Iteration 2. The submodule rejection rationale is factually correct. The rollback procedure is specific enough to execute under pressure. The developer guide content is specified.

The strongest case for this issue is not just that extraction is correct — it is that the *method* of extraction is now explicitly safe, reversible, and well-documented. For a C4 OSS release decision that will be executed exactly once and cannot be undone cleanly, "safe, reversible, well-documented" is the standard that matters.

**What still prevents this from being the best possible version of itself:** The distribution mechanism (git clone vs. tarball) is asserted but not evidenced. The line count has no attribution. The `projects/` exclusion claim has no inspection evidence. These are minor — the issue's credibility does not hinge on them — but they are the remaining precision gaps that separate "very good" from "excellent."

---

### Steelman Improvement Findings (Iteration 3)

| ID | Improvement | Severity | Affected Dimension |
|----|-------------|----------|--------------------|
| SM-001-it3 | Attribute the 635,075 line count (cite command or measurement source) | Minor | Evidence Quality |
| SM-002-it3 | Clarify distribution mechanism: git clone vs. tarball | Minor | Evidence Quality, Internal Consistency |
| SM-003-it3 | Link `skills/worktracker/rules/worktracker-directory-structure.md` in prose | Minor | Traceability |
| SM-004-it3 | Specify measurement comparison procedure: pre-extraction tag checkout vs. post-extraction clone | Minor | Actionability, Evidence Quality |
| SM-005-it3 | Add worktracker entity link (H-32 compliance) | Minor | Traceability |

---

## Section 3: Consolidated Findings (All 10 Strategies)

> Strategies executed: S-014, S-003, S-013, S-007, S-002, S-004, S-010, S-012, S-011, S-001
> H-16 compliance: S-003 executed before S-002, S-004, S-001 — CONFIRMED

---

### Critical Findings

**No Critical findings in Iteration 3.** The two Critical findings from Iteration 2 (FINDING-C1-it2: dangerous `git-filter-repo` command; RT-004-it2: history rewrite risk) are both resolved in Iteration 3. No new Critical findings identified.

---

### Major Findings

**No Major findings in Iteration 3.** All six Major findings from Iteration 2 are resolved:
- FINDING-M1-it2 (Submodule rejection rationale): Closed
- FINDING-M2-it2 (Rollback "coordinate with PRs" vague): Closed
- FINDING-M3-it2 (No hyperlinks, no milestone link, no ADR): Closed
- FINDING-M4-it2 (Developer guide content unspecified): Closed
- FM-001-it2 (git-filter-repo safety): Closed via R-001-it2
- DA-001-it1 (Distribution mechanism): Substantially addressed but with Minor residual

**No new Major findings identified in Iteration 3.**

---

### Minor Findings

#### FINDING-m1-it3: Distribution Mechanism Type Unverified
**Strategy Source:** S-002 (Devil's Advocate), S-011 (Chain-of-Verification)
**Severity:** Minor
**Section:** "The problem / Distribution mechanism"

**Evidence from deliverable:**
> "When users install Jerry through Claude Code's plugin system, the plugin installation clones the full repository content — including `projects/`. The `projects/` directory is not excluded by any distribution filter, `.gitattributes` export-ignore, or plugin manifest include/exclude rule."

**Analysis:** "Clones the full repository content" — if this is a full git clone (including history), the total download is significantly more than 41 MB (the working tree size). The git object store for a repository with 14 projects, thousands of commits, and binary-adjacent markdown content could easily be 50-100+ MB. If it is a shallow clone or tarball, 41 MB is approximately correct. The type of clone directly affects the credibility of the size-reduction claim. This was DA-001-it2 (Minor downgrade from Major) — still present as a Minor precision gap.

**Recommended fix:** Add one sentence: "The plugin system performs a [full git clone / shallow clone / zip download — verify the exact mechanism from the `.claude-plugin/` manifest documentation]." Or cite the actual mechanism with evidence from the manifest file inspection.

---

#### FINDING-m2-it3: Line Count Unattributed
**Strategy Source:** S-011 (Chain-of-Verification), S-010 (Self-Refine)
**Severity:** Minor
**Section:** Data table

**Evidence from deliverable:**
> "| Total lines in `projects/` | 635,075 |"

**Analysis:** 635,075 is a specific, verifiable number. It implies measurement. No measurement method is specified. For a C4 issue that will be public-facing, unattributed statistics invite skepticism. The fix is a parenthetical: "(measured: `git ls-files projects/ | xargs wc -l`)" or equivalent. This was FINDING-m2 from Iteration 1 (Evidence Quality) — persists as Minor.

---

#### FINDING-m3-it3: Measurement Comparison Procedure Ambiguous
**Strategy Source:** S-012 (FMEA), S-010 (Self-Refine)
**Severity:** Minor
**Section:** "Implementation / Phase 3: Validate"

**Evidence from deliverable:**
> "Plugin installation size reduced by >= 40 MB. Measurement: perform a fresh `git clone` of the post-extraction Jerry repo and compare `du -sh` against the pre-extraction tag checkout."

**Analysis:** The fresh-clone measurement specification is an improvement from Iteration 2's `du -sh` working tree comparison. However: "compare `du -sh` against the pre-extraction tag checkout" — this comparison requires two separate clone operations:
1. Clone Jerry post-extraction at current main → measure size
2. Clone or checkout Jerry at the pre-extraction tag → measure size

The second operation requires clarification: does the implementer need to clone the current repo and checkout the pre-extraction tag? Or clone a separate copy at the tag? If main has rebased or otherwise modified history after the extraction, the pre-extraction tag may not be available in a fresh clone. The measurement procedure should explicitly state: "Create two separate fresh clone directories: one at the pre-extraction tag (`git clone <jerry-repo> /tmp/jerry-pre && cd /tmp/jerry-pre && git checkout <pre-extraction-tag>`) and one at the post-extraction HEAD. Compare `du -sh` of each."

---

#### FINDING-m4-it3: `worktracker-directory-structure.md` Unlinked in Prose
**Strategy Source:** S-011 (Chain-of-Verification)
**Severity:** Minor
**Section:** "Plugin user experience"

**Evidence from deliverable:**
> "Users who adopt Jerry's worktracker skill create projects in their own repositories using the repository-based placement pattern already defined in `skills/worktracker/rules/worktracker-directory-structure.md`."

**Analysis:** This file is referenced by path but not hyperlinked. The governance note in "Affected components" uses a hyperlink for this file: "[worktracker directory structure standards]". The prose reference in "Plugin user experience" is a dead reference for external GitHub readers. Minor — the governance note link partially compensates — but the reference pattern is inconsistent within the issue.

---

#### FINDING-m5-it3: H-32 Worktracker Entity Reference Missing
**Strategy Source:** S-007 (Constitutional AI), CC-002-it2 persistent
**Severity:** Minor
**Section:** Entire issue (no internal worktracker reference present)

**Evidence from deliverable:**
No worktracker story or enabler number is referenced anywhere in the issue.

**Analysis:** Per H-32, GitHub Issues in the jerry repository must have a corresponding worktracker entity. The issue should reference the internal entity number in the body: "Implements: [STORY-NNN or ENABLER-NNN]" or in the Related Items section. This was CC-002-it2 — still Minor, still unaddressed. For public OSS issues, this may be acceptable to omit from the GitHub issue body (the internal reference is for the worktracker, not for external contributors). The finding is Minor but persistent.

---

#### FINDING-m6-it3: "Inform Collaborators" Rollback Step Vague
**Strategy Source:** S-004 (Pre-Mortem), S-010 (Self-Refine)
**Severity:** Minor
**Section:** "Implementation / Rollback procedure"

**Evidence from deliverable:**
> "3. Force-push only if the migration was already pushed to remote. Before force-pushing to main: (a) check for open PRs against the migration commit — `gh pr list --base main` — and close or re-target them; (b) verify branch protection rules permit force-push (temporary bypass may be required — re-enable immediately after); (c) inform any collaborators of the force-push."

**Analysis:** Steps (a) and (b) are now specific and actionable. Step (c) "inform any collaborators" — inform them of what? That the force-push is happening, yes, but also: their local branches that reference the migration commit need to be rebased against the restored history. Without this, collaborators who did a `git pull` after the migration will have the migration commit in their local history, and the force-push will cause divergence. One additional sentence: "Collaborators who pulled the migration commit must run `git fetch origin && git rebase origin/main` to realign their local branches."

---

#### FINDING-m7-it3: Audit Scope Unspecified
**Strategy Source:** S-010 (Self-Refine)
**Severity:** Minor
**Section:** "Implementation / Phase 2: Update references"

**Evidence from deliverable:**
> "Audit all `projects/` path references in `.context/rules/` files — these are informational references to source artifacts (ADR provenance, phase synthesis outputs)."

**Analysis:** "All `projects/` path references in `.context/rules/` files" — how many? A quick `grep -r "projects/" .context/rules/ | wc -l` would yield a specific count. Providing this count (e.g., "approximately 23 references across 8 files") gives the implementer an effort estimate for this subtask. This is a minor precision gap that has persisted through all three iterations. Cost to fix: one line.

---

### S-007 Constitutional AI Findings (CC-NNN-it3)

#### CC-001-it3: Repository Visibility — RESOLVED (Iteration 2)
**Severity:** Resolved

#### CC-002-it3: H-32 GitHub Issue Parity — Still Minor
**Severity:** Minor
**Analysis:** See FINDING-m5-it3. The worktracker entity reference is absent from the issue body. For an external-facing OSS issue, this is a low-impact compliance gap; the worktracker exists as the internal SSOT. Not a blocking finding for issue filing.

#### CC-003-it3: No Constitutional Violations Found
**Analysis:** No changes to agent definitions, HARD rules, or governance documents. P-003, P-020, P-022 not implicated.

---

### S-001 Red Team Findings (RT-NNN-it3)

#### RT-001-it3: CI Pipeline Requirement — RESOLVED (Iteration 2)
**Severity:** Resolved

#### RT-002-it3: Repository Visibility — RESOLVED (Iteration 2)
**Severity:** Resolved

#### RT-003-it3: Branch Protection Acknowledgment — RESOLVED
**Severity:** Resolved
**Evidence:** Rollback step 3(b) now reads: "verify branch protection rules permit force-push (temporary bypass may be required — re-enable immediately after)." This closes RT-003-it2.

#### RT-004-it3: git-filter-repo Safety Risk — RESOLVED
**Severity:** Resolved
**Evidence:** Bold safety warning present: "Do NOT run `git-filter-repo` directly in the Jerry working directory without a `--source` flag — it will rewrite Jerry's history, removing all non-`projects/` files. This is irreversible." Clone-first procedure specified. RT-004-it2 is closed.

#### RT-005-it3: Plugin Manifest Not Inspected (New — Minor)
**Severity:** Minor
**Strategy Source:** S-001 (Red Team)
**Section:** "The problem / Distribution mechanism"

**Evidence from deliverable:**
> "The `projects/` directory is not excluded by any distribution filter, `.gitattributes` export-ignore, or plugin manifest include/exclude rule."

**Analysis:** This claim is asserted but not verified by inspection evidence. The `.claude-plugin/` manifest exists in the repository — it can be read to confirm whether include/exclude rules are present. For a C4 issue making a public claim ("no distribution filter"), an implementer or external contributor could easily falsify this by finding a filter that was overlooked. The fix is a one-sentence inspection result: "Verified: `.claude-plugin/manifest.json` contains no path exclusion rules; `.gitattributes` has no export-ignore directives." This transforms an assertion into evidence.

---

### S-004 Pre-Mortem Findings (PM-NNN-it3)

#### PM-001-it3: Long-Term Archival Strategy — RESOLVED
**Severity:** Resolved
**Evidence:** Acceptance criterion: "Repository visibility confirmed as private; content review and long-term visibility reassessment deferred to a separate issue." PM-001-it2 is closed.

#### PM-002-it3: CI Test Baseline Not Specified — Persists
**Severity:** Minor
**Analysis:** Phase 3 says "verify `document_type.py` path patterns work correctly through a symlink (test added with symlinked fixture)." The acceptance criterion says "test added" — but what existing test does this augment or replace? An implementer does not know which test file to modify. One reference: "Extend `tests/unit/test_document_type.py` (or the symlink integration test suite)" would close this.

#### PM-003-it3: No Dry-Run Option Documented
**Severity:** Minor (new finding)
**Strategy Source:** S-004 (Pre-Mortem)
**Section:** "Implementation / Phase 1: Prepare"

**Analysis:** The implementation describes an irreversible sequence: create tag → extract history → push to new repo → remove from Jerry → update gitignore. There is no dry-run option mentioned. For a C4 irreversible operation, a pre-flight check sequence would substantially reduce risk. Example: before `git rm -r --cached projects/PROJ-*`, run `git status --short` to confirm the staging area is clean; before pushing to the jerry-projects remote, confirm the correct remote is configured with `git remote -v`. These are operational safety checks that would catch configuration errors before the irreversible steps. A one-item pre-flight checklist in Phase 1 would close this.

---

### S-002 Devil's Advocate Findings (DA-NNN-it3)

#### DA-001-it3: Distribution Mechanism — Minor Residual
**Severity:** Minor (same as Iteration 2 downgrade)
**Analysis:** See FINDING-m1-it3. The "clones the full repository content" assertion is the residual gap.

#### DA-002-it3: Symlink Preference Not Restated as Preference
**Severity:** Minor (persists from Iteration 2)
**Analysis:** The symlink bridge is selected, but the issue does not explicitly frame this as the framework author's development preference rather than an architectural requirement. The symlink is a local developer convenience — it could be replaced by any filesystem path management approach the author prefers. This is a very minor framing issue; the practical impact is zero.

---

### S-012 FMEA Findings (FM-NNN-it3)

#### FM-001-it3: git-filter-repo Safety Risk — RESOLVED
| Attribute | Value |
|-----------|-------|
| Status | Resolved in Iteration 3 |
| Resolution | Clone-first procedure specified; bold safety warning present |
| RPN | 0 (mitigated) |

#### FM-002-it3: Symlink Resolution — Risk STABLE
| Attribute | Value |
|-----------|-------|
| Component | `document_type.py` + `layered_config_adapter.py` path resolution |
| Failure Mode | `pathlib.Path.glob()` symlink traversal behavior |
| Effect | `jerry projects list` fails for framework author |
| Severity | 5 |
| Occurrence | 3 |
| Detection | 3 |
| RPN | 45 |
| Status | Issue correctly states "must be tested, not assumed." Acceptance criterion includes test. Risk is documented and acceptance-gated. |

#### FM-003-it3: Distribution Mechanism — Low Risk
| Attribute | Value |
|-----------|-------|
| Component | Size reduction claim |
| Failure Mode | Claim is 41 MB reduction but actual reduction is smaller (git history not included in tarball measurement) |
| Effect | Public credibility of size claim weakened |
| Severity | 3 |
| Occurrence | 3 |
| Detection | 4 |
| RPN | 36 |
| Status | Minor — see FINDING-m1-it3 |

#### FM-004-it3: No Dry-Run Checklist — Low-Medium Risk
| Attribute | Value |
|-----------|-------|
| Component | Phase 1 implementation steps |
| Failure Mode | Implementer pushes to wrong remote or removes wrong paths |
| Effect | Partial extraction or wrong-repo push |
| Severity | 6 (recoverable via tag, but requires rollback procedure) |
| Occurrence | 2 |
| Detection | 4 |
| RPN | 48 |
| Mitigation | Add pre-flight check: `git remote -v` before push; `git status --short` before `git rm`. See PM-003-it3. |

---

### S-013 Inversion Findings (IN-NNN-it3)

#### IN-001-it3: Developer Fresh-Clone Experience — RESOLVED
**Severity:** Resolved
**Evidence:** "This graceful handling also covers the framework author's fresh clone before symlink setup — the experience should be identical to the plugin user case until the symlink is configured." IN-001-it2 is closed.

#### IN-002-it3: Sparse Checkout via Plugin System — Residual Minor
**Severity:** Minor (same as Iteration 2)
**Analysis:** The sparse checkout alternative rejection does not address whether the Claude plugin system itself supports native filtering. If the plugin installer supports `.gitattributes` export-ignore natively, the external repo approach might be avoidable. This is academic — the symlink bridge is still the stronger solution — but the dismissal is incomplete for a C4-level alternatives analysis.

#### IN-003-it3: What If `jerry-projects` Outlives Jerry?
**Severity:** Minor (new finding)
**Strategy Source:** S-013 (Inversion)
**Analysis:** Applying inversion: what if the framework author stops maintaining Jerry but `jerry-projects` contains valuable decision records and research artifacts that future maintainers need? The private repository model makes this data inaccessible. The "long-term visibility reassessment deferred to a separate issue" acceptance criterion acknowledges this. However, the issue does not specify who is responsible for that reassessment or what triggers it. One sentence: "The long-term visibility reassessment should be triggered at OSS public release or when a second maintainer is added, whichever comes first." This converts a vague deferral into a concrete trigger.

---

### S-010 Self-Refine Findings (SR-NNN-it3)

#### SR-001-it3: Voice Bridge — RESOLVED (Iteration 2)
**Severity:** Resolved

#### SR-002-it3: Phase 2 Audit Decision — RESOLVED (Iteration 2)
**Severity:** Resolved

#### SR-003-it3: .npmignore Reference — RESOLVED
**Severity:** Resolved
**Evidence:** "The `projects/` directory is not excluded by any distribution filter, `.gitattributes` export-ignore, or plugin manifest include/exclude rule." The `.npmignore` reference from Iteration 2 is replaced with `.gitattributes export-ignore` and plugin manifest — Python-appropriate terminology. SR-003-it2 is closed.

#### SR-004-it3: git-filter-repo vs. git subtree "REJECTED" Surface Confusion
**Severity:** Minor (persists from Iteration 2)
**Evidence:**
> Alternatives table: "Git subtree (embedded)... Does not reduce installation size... Rejected"
> Implementation: "Extract `projects/` history using `git subtree split --prefix=projects/...`"

**Analysis:** The naming collision between "git subtree (embedded): REJECTED" and "git subtree split (extraction): RECOMMENDED" is less confusing in Iteration 3 because the implementation now labels `git subtree split` as "the recommended approach" and explains what it does. A reader who carefully reads both sections should understand they are different operations. But a skimming reader will see "Git subtree: REJECTED" in alternatives and then `git subtree split` in implementation and wonder why. A rename of the alternatives entry to "Git subtree embedding (in-place)" would fully disambiguate at minimal cost.

---

### S-011 Chain-of-Verification Findings (CV-NNN-it3)

#### CV-001-it3: fnmatch/pathlib Technical Note — RESOLVED
**Severity:** Resolved
**Evidence:** "Python 3.9-3.12 behavior; Python 3.13+ adds an explicit `follow_symlinks` parameter." CV-001-it2 residual is closed.

#### CV-002-it3: History Preservation Guarantee — RESOLVED
**Severity:** Resolved
**Evidence:** "History preservation guarantee: per-file `git log` and `git blame` for files within `projects/` are preserved; commit SHAs will differ from Jerry's; cross-directory commit context (commits touching both `projects/` and framework files) is split across the two repos." FINDING-m1-it2 / CV-002-it1 is closed.

#### CV-003-it3: PROJ-001 Naming — SUBSTANTIALLY RESOLVED
**Severity:** Resolved (substantially)
**Evidence:** "Note on PROJ-001 naming: Three filesystem directories use the PROJ-001 prefix: `PROJ-001-oss-release/`, `PROJ-001-oss-documentation/`, and `PROJ-001-plugin-cleanup/`... The directory names (shown in parentheses above) are the disambiguating identifiers." FINDING-m2-it2 is substantially closed; the identifier collision is explained and the filesystem names serve as disambiguators.

#### CV-004-it3: Distribution Mechanism — Verify
**Severity:** Minor (persists, see FINDING-m1-it3)

---

## Section 4: Revision Recommendations

| ID | Priority | Finding Source | Section | Issue |
|----|----------|----------------|---------|-------|
| R-001-it3 | Minor | FINDING-m1-it3, DA-001-it3 | "The problem / Distribution mechanism" | Clarify clone vs. tarball type |
| R-002-it3 | Minor | FINDING-m2-it3 | Data table | Attribute 635,075 line count |
| R-003-it3 | Minor | FINDING-m3-it3 | Phase 3 measurement | Clarify measurement comparison procedure |
| R-004-it3 | Minor | FINDING-m4-it3 | "Plugin user experience" | Add hyperlink to worktracker-directory-structure.md |
| R-005-it3 | Minor | FINDING-m5-it3 | Issue body (meta) | Add worktracker entity reference (H-32) |
| R-006-it3 | Minor | FINDING-m6-it3 | Rollback step 3(c) | Specify collaborator rebase guidance |
| R-007-it3 | Minor | FINDING-m7-it3 | Phase 2 | Add audit scope count |
| R-008-it3 | Minor | RT-005-it3 | "Distribution mechanism" | Add manifest inspection evidence |
| R-009-it3 | Minor | PM-003-it3 | Phase 1 pre-flight | Add dry-run pre-flight checklist |
| R-010-it3 | Minor | IN-003-it3 | Acceptance criteria | Specify long-term visibility reassessment trigger |

---

### R-001-it3 Detail: Clarify Distribution Mechanism Type

**Current text:**
> "the plugin installation clones the full repository content — including `projects/`"

**Recommended replacement:**
> "the plugin installation [performs a full `git clone` / downloads a zip/tarball of the repository — verify the exact mechanism from `.claude-plugin/` manifest documentation] — including `projects/`. If the plugin system performs a full git clone, the installation footprint exceeds the 41 MB working tree size by the size of the git object store; if it downloads a zip, the working tree size is the correct measure."

**Alternatively (if the mechanism is known):** Replace the bracketed text with the confirmed mechanism and cite the manifest or plugin documentation as the source.

---

### R-002-it3 Detail: Attribute Line Count

**Current text:**
> "| Total lines in `projects/` | 635,075 |"

**Recommended replacement:**
> "| Total lines in `projects/` | 635,075 (measured: `git ls-files projects/ \| xargs wc -l`) |"

Or add a footnote to the data table.

---

### R-003-it3 Detail: Clarify Measurement Comparison Procedure

**Current text:**
> "Measurement: perform a fresh `git clone` of the post-extraction Jerry repo and compare `du -sh` against the pre-extraction tag checkout."

**Recommended replacement:**
> "Measurement: create two separate fresh clone directories — (1) clone Jerry post-extraction at current HEAD (`git clone <jerry-repo> /tmp/jerry-post && du -sh /tmp/jerry-post`); (2) clone Jerry and checkout the pre-extraction tag (`git clone <jerry-repo> /tmp/jerry-pre && cd /tmp/jerry-pre && git checkout <pre-extraction-tag> && du -sh /tmp/jerry-pre`). Compare the sizes. The difference should be >= 40 MB."

---

### R-004-it3 Detail: Link worktracker-directory-structure.md in Prose

**Current text (Plugin user experience section):**
> "Users who adopt Jerry's worktracker skill create projects in their own repositories using the repository-based placement pattern already defined in `skills/worktracker/rules/worktracker-directory-structure.md`."

**Recommended replacement:**
> "Users who adopt Jerry's worktracker skill create projects in their own repositories using the repository-based placement pattern already defined in [`skills/worktracker/rules/worktracker-directory-structure.md`](https://github.com/geekatron/jerry/blob/main/skills/worktracker/rules/worktracker-directory-structure.md)."

---

### R-005-it3 Detail: Add Worktracker Entity Reference

**Add to issue body** (in a Related Items section or at the top of the body):
> "**Related:** Implements [STORY-NNN / ENABLER-NNN] in PROJ-001 worktracker. Jerry repo H-32 compliance."

This is a meta-change to the GitHub Issue body format, not to the rendered content.

---

### R-006-it3 Detail: Specify Collaborator Rebase Guidance

**Current text:**
> "(c) inform any collaborators of the force-push."

**Recommended replacement:**
> "(c) inform any collaborators of the force-push. Collaborators who pulled the migration commit must run `git fetch origin && git rebase origin/main` to realign their local branches with the restored history."

---

### R-007-it3 Detail: Add Audit Scope Count

**Current text:**
> "Audit all `projects/` path references in `.context/rules/` files"

**Recommended replacement:**
> "Audit all `projects/` path references in `.context/rules/` files (estimated: run `grep -r 'projects/' .context/rules/ | wc -l` to get the current count before starting)"

---

### R-008-it3 Detail: Add Manifest Inspection Evidence

**Current text:**
> "The `projects/` directory is not excluded by any distribution filter, `.gitattributes` export-ignore, or plugin manifest include/exclude rule."

**Recommended replacement:**
> "The `projects/` directory is not excluded by any distribution filter, `.gitattributes` export-ignore, or plugin manifest include/exclude rule. (Verified: inspected `.claude-plugin/` manifest and `.gitattributes` — no path exclusion rules present as of this writing.)"

---

### R-009-it3 Detail: Add Pre-Flight Safety Checks

**Add to Phase 1: Prepare**, before "Remove `projects/PROJ-*` directories from Jerry's git tracking":

> **Pre-flight checks (run before irreversible steps):**
> - `git remote -v` — confirm the correct `<jerry-projects-remote>` is configured before push
> - `git status --short` — confirm staging area is clean before `git rm -r --cached`
> - `git log --oneline -5` — confirm you are on the correct branch before any history operations

---

### R-010-it3 Detail: Specify Visibility Reassessment Trigger

**Current text:**
> "Repository visibility confirmed as private; content review and long-term visibility reassessment deferred to a separate issue."

**Recommended replacement:**
> "Repository visibility confirmed as private; content review and long-term visibility reassessment deferred to a separate issue. Suggested trigger: reassess visibility when (a) Jerry reaches first public OSS release and external contributors are active, or (b) a second maintainer is added, whichever comes first."

---

## Section 5: Voice Assessment

### Saucer Boy Persona Compliance

**Overall Voice Score: 9.5/10** (same as Iteration 2)

**Existing voice elements that continue to hold:**

The three core lines remain intact and continue to carry the issue's personality:
- "Your plugin cache should be a quiver, not a garage sale." — Still the best line. The compression is perfect: quiver (precision tool) vs. garage sale (accumulated junk). The reader gets the architectural distinction in six words.
- "Ship the skis, not the trip journal." — Tight and precise. The semantic mapping is clear: skis = framework tools, trip journal = project history. No wasted syllables.
- "Three phases. Same as any good line: scout the terrain, read the features, commit to the exit." — This landed in Iteration 2 and still lands. The cadence matches the three-phase structure. "Commit to the exit" earns its weight: in skiing, you commit to your exit before you drop in; in this migration, you commit to the validation phase before you finalize.
- "The mountain doesn't care about your trip journal. But your pack weight cares a lot." — The callback at the close works. The contrast between abstract (mountain's indifference) and concrete (pack weight) is the McConkey move: translate principle into consequence.

**What the Iteration 3 revisions do to the voice:**

The Iteration 3 additions are primarily technical precision patches: bold safety warning, clone-first procedure, corrected submodule rationale, rollback specifics. These are dry by design and do not attempt voice insertion — which is correct. The implementation section is where McConkey steps back and lets the procedure speak. Technical precision in dangerous terrain is its own form of voice discipline.

**The one voice note from Iteration 2 that persists:**

The Phase 2 technical note (`fnmatch.fnmatch()` operates on path strings...) remains a distinct voice register — engineering consultation mode. The Iteration 2 review suggested a re-anchor sentence before it. This has not been added, which is defensible — the technical note is sandwiched between implementation steps and does not jar unless you are actively listening for voice. A "know your terrain before you drop in" bridge sentence before the technical note would smooth the transition, but this is a preference, not a defect.

**What would reach 10/10:**

The safety warning is bold and clear ("Do NOT run `git-filter-repo` directly...") but it reads as technical documentation, not as McConkey. A one-line voice cue above the warning — "One more thing before you drop in." — would frame the danger without breaking the procedure format. Optional, not required.

---

## Section 6: Gap Analysis to 0.95

### Current Score: 0.921 | Target: 0.95 | Gap: 0.029

The gap has closed from 0.08 (Iteration 2) to 0.029 (Iteration 3). This is meaningful progress. The gap is now entirely composed of Minor findings — no Critical or Major gaps remain. The question for Iteration 4 is whether the Minor findings collectively block the elevated 0.95 threshold.

### Dimension-Level Gap Analysis

| Dimension | Current | Target | Gap | Primary Blocking Item | Effort to Close |
|-----------|---------|--------|-----|-----------------------|-----------------|
| Completeness | 0.92 | 0.95 | 0.03 | Distribution mechanism type; audit scope count; H-32 link | Low — 3 targeted additions |
| Internal Consistency | 0.93 | 0.95 | 0.02 | git subtree terminology disambiguation; size metric clarification | Low — rename one table entry, add one sentence |
| Methodological Rigor | 0.92 | 0.95 | 0.03 | No risk register; distribution mechanism assertion | Low-Medium — risk register is 4-row table |
| Evidence Quality | 0.91 | 0.95 | 0.04 | Distribution type unverified; line count unattributed; measurement procedure ambiguous | Low — cite source, add parenthetical |
| Actionability | 0.93 | 0.95 | 0.02 | Collaborator rebase guidance; audit scope; measurement procedure | Low — 2 targeted sentences |
| Traceability | 0.90 | 0.95 | 0.05 | `worktracker-directory-structure.md` unlinked in prose; H-32 worktracker entity | Low — 2 hyperlinks |

### What Drives the Remaining Gap

**Evidence Quality (0.91 → 0.95):** This is the largest dimensional gap (0.04) and has the most room for targeted improvement. The distribution mechanism type verification (R-001-it3), line count attribution (R-002-it3), and manifest inspection evidence (R-008-it3) are all one-line additions. Together they address the "asserted-not-evidenced" pattern that has been holding this dimension below 0.93 across all three iterations.

**Traceability (0.90 → 0.95):** The `worktracker-directory-structure.md` prose link (R-004-it3) and H-32 worktracker entity (R-005-it3) are low-effort additions. The ADR "SHOULD be created" is already noted; making it an acceptance criterion would add one checkbox.

**Methodological Rigor (0.92 → 0.95):** A minimal risk register (FM-002-it3 and FM-004-it3 only — the remaining open FMEA items) would close the "no risk register" gap. A 4-row table with Component/Failure Mode/Mitigation/Status columns would be proportionate to the issue's scope.

### Projected Iteration 4 Score (if R-001-it3 through R-010-it3 all applied)

| Dimension | Current | Post-R | Gain |
|-----------|---------|--------|------|
| Completeness | 0.92 | 0.95 | +0.03 |
| Internal Consistency | 0.93 | 0.95 | +0.02 |
| Methodological Rigor | 0.92 | 0.95 | +0.03 |
| Evidence Quality | 0.91 | 0.95 | +0.04 |
| Actionability | 0.93 | 0.96 | +0.03 |
| Traceability | 0.90 | 0.95 | +0.05 |
| **Composite** | **0.921** | **~0.950** | **+0.029** |

**Iteration 4 projection: ~0.950 — at or just above the C4 elevated threshold.** The remaining items are all Minor and addressable in a single revision pass. There is no structural gap remaining; the issue's architecture is sound. Iteration 4 should cross the 0.95 threshold if all 10 recommendations are applied.

### Honest Assessment

The Iteration 3 deliverable is in excellent shape. The two critical safety risks from Iteration 2 are eliminated. The factual error in the alternatives table is corrected. The traceability has been substantially repaired. The developer guide content is specified. No new regressions were introduced.

The remaining gap to 0.95 is entirely composed of Minor precision items: attributing a number, linking two files, clarifying a measurement procedure, adding a pre-flight checklist. None of these require structural changes. The issue can be filed as-is in a REVISE state (0.921) — it is technically correct and safe to implement. The 10 remaining recommendations in R-001-it3 through R-010-it3 are polish that would justify the elevated 0.95 threshold for a C4 OSS release decision.

---

## Section 7: Delta Analysis

### What Improved from Iteration 2 to Iteration 3

| Finding | Iteration 2 Severity | Iteration 3 Status | Evidence |
|---------|---------------------|-------------------|---------|
| FINDING-C1-it2: git-filter-repo dangerous (R-001-it2) | Critical | **Resolved** | Bold safety warning + clone-first procedure |
| RT-004-it2: git-filter-repo history rewrite risk | Critical | **Resolved** | Subsumed in R-001-it2; identical fix |
| FINDING-M1-it2: Submodule rejection factually incorrect (R-002-it2) | Major | **Resolved** | "content is NOT included in a plain git clone" |
| FINDING-M2-it2: Rollback "coordinate with PRs" vague (R-003-it2) | Major | **Resolved** | `gh pr list --base main`; branch protection note; deletion caveat |
| FINDING-M3-it2: No hyperlinks, no milestone, no ADR (R-004-it2) | Major | **Resolved** | Links to document_type.py#L98-L106, layered_config_adapter.py, milestone/1, governance note |
| FINDING-M4-it2: Developer guide content unspecified (R-005-it2) | Major | **Resolved** | 7-item numbered outline in Phase 1 |
| FINDING-m1-it2: History preservation underspecified | Minor | **Resolved** | "per-file git log/blame preserved; SHAs differ; cross-directory context split" |
| FINDING-m2-it2: PROJ-001 naming anomaly | Minor | **Substantially Resolved** | Directory names in parentheses as disambiguators |
| FINDING-m3-it2: Phase 3 measurement unmeasurable | Minor | **Substantially Resolved** | Fresh git clone comparison method specified |
| FINDING-m4-it2: Rollback assumes force-push authority | Minor | **Resolved** | Rollback step 3(b): branch protection acknowledgment |
| IN-001-it2: Developer fresh-clone unaddressed | Minor | **Resolved** | "graceful handling also covers the framework author's fresh clone" |
| PM-001-it2: Long-term archival unaddressed | Minor | **Resolved** | "content review and long-term visibility reassessment deferred to a separate issue" |
| CV-001-it2: fnmatch Python version residual | Minor | **Resolved** | "Python 3.13+ adds an explicit `follow_symlinks` parameter" |
| SR-003-it2: `.npmignore` wrong for Python | Minor | **Resolved** | Replaced with `.gitattributes export-ignore` and plugin manifest |

**14 findings from Iteration 2 closed or substantially resolved.** This matches the pattern from Iteration 1 → Iteration 2 (14 findings closed then as well). The revision process is working.

---

### What Regressed from Iteration 2 to Iteration 3

**No regressions identified.** The Iteration 3 revisions are precise and do not introduce internal contradictions, new safety risks, or new factual errors. The git-filter-repo fix in particular is better than what was in Iteration 2 — the clone-first procedure is technically sound, the safety warning is appropriately prominent, and the primary/alternative differentiation is clear.

---

### What Remains Unaddressed

| Finding | First Appeared | Current Severity | Notes |
|---------|---------------|-----------------|-------|
| Distribution mechanism: git clone vs. tarball (DA-001-it1) | Iteration 1 (Major) | Minor | Downgraded; persists |
| H-32 worktracker entity link (CC-002-it1) | Iteration 1 (Minor) | Minor | Low-impact for OSS issue |
| Line count unattributed (Evidence) | Iteration 1 (Minor) | Minor | One-line fix |
| Audit scope unquantified (Phase 2) | Iteration 1 (Minor) | Minor | One-line fix |
| git subtree naming ambiguity (SR) | Iteration 2 (Minor) | Minor | Table rename |

---

### New Findings Introduced in Iteration 3

| Finding | Severity | Source | Description |
|---------|---------|--------|-------------|
| FINDING-m3-it3 | Minor | FM, S-010 | Measurement comparison procedure ambiguous (pre-extraction tag checkout method) |
| RT-005-it3 | Minor | S-001 | Plugin manifest not inspected to verify exclusion claim |
| PM-003-it3 | Minor | S-004 | No dry-run pre-flight checklist for Phase 1 irreversible steps |
| IN-003-it3 | Minor | S-013 | Visibility reassessment trigger not specified |

All four new findings are Minor. No Critical or Major findings introduced in Iteration 3. The new findings are genuine precision gaps surfaced by deeper strategy analysis of the revised text — not regressions from the revision process.

---

## Execution Statistics

| Strategy | Finding Prefix | Critical | Major | Minor | Protocol Steps |
|----------|---------------|---------|-------|-------|----------------|
| S-014 (LLM-as-Judge) | LJ-NNN-it3 | 0 | 0 | 0 | 7/7 (scoring) |
| S-003 (Steelman) | SM-NNN-it3 | 0 | 0 | 5 | 6/6 |
| S-013 (Inversion) | IN-NNN-it3 | 0 | 0 | 2 | Contributed to m7, m3 |
| S-007 (Constitutional) | CC-NNN-it3 | 0 | 0 | 1 | 5/5 |
| S-002 (Devil's Advocate) | DA-NNN-it3 | 0 | 0 | 2 | Contributed to m1 |
| S-004 (Pre-Mortem) | PM-NNN-it3 | 0 | 0 | 3 | 4/4 |
| S-010 (Self-Refine) | SR-NNN-it3 | 0 | 0 | 2 | 4/4 |
| S-012 (FMEA) | FM-NNN-it3 | 0 | 0 | 3 | 5/5 (FMEA tables) |
| S-011 (Chain-of-Verification) | CV-NNN-it3 | 0 | 0 | 2 | 5/5 |
| S-001 (Red Team) | RT-NNN-it3 | 0 | 0 | 2 | 4/4 |
| **Totals** | | **0** | **0** | **22** | **10/10 strategies** |

**Total Active Findings: 10** (FINDING-m1-it3 through RT-005-it3 and PM-003-it3, IN-003-it3 — all Minor)
**Finding reduction:** 22 net findings in Iteration 2 → 10 net findings in Iteration 3. This is the correct direction.

---

*Adversarial Review Version: Iteration 3 of 5*
*Strategy: C4 Tournament (all 10 strategies)*
*H-16 Compliance: S-003 before S-002, S-004, S-001 — CONFIRMED*
*Anti-leniency: Active — lower adjacent score assigned when uncertain*
*Agent: adv-executor (adv-scorer integrated)*
