# Quality Score Report: version-bump.yml Dual Filters (#187)

## L0 Executive Summary
**Score:** 0.839/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.72)
**One-line assessment:** The dual-filter implementation is functionally sound for the main code path, but four gaps prevent acceptance at the 0.95 bar: a vestigial/misleading `[skip-bump]` check on the `workflow_dispatch` branch, an unverified case-insensitivity claim, missing exclusions for `.claude/**` and `.claude-plugin/` from paths-ignore, and an absent `revert:` prefix in Filter B.

---

## Scoring Context
- **Deliverable:** `.github/workflows/version-bump.yml` (Filter A: `paths-ignore`, Filter B: job-level `if:` prefix checks)
- **Deliverable Type:** Code (GitHub Actions workflow)
- **Criticality Level:** C2 (CI pipeline, reversible in 1 day)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Research Reference:** `projects/PROJ-030-bugs/research/workflow-filtering-research.md`
- **Scored:** 2026-03-11

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.839 |
| **Threshold** | 0.95 (user-specified, overrides H-13 0.92 default) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no adv-executor report provided) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.80 | 0.160 | 8/10 no-bump prefixes covered; `revert:` missing; `.claude/**` and `.claude-plugin/` not excluded from paths-ignore |
| Internal Consistency | 0.20 | 0.85 | 0.170 | Path-ignore list and Filter B are complementary and non-conflicting; one vestigial `[skip-bump]` check on `workflow_dispatch` branch creates a false impression that manual runs can be suppressed |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | Research-driven choice of `paths-ignore` over `paths` is well-justified; dual-layer defense-in-depth is architecturally sound; workflow_dispatch independence correctly handled |
| Evidence Quality | 0.15 | 0.72 | 0.108 | `startsWith()` case-insensitivity claim cited but no direct quote from GitHub docs; squash-merge null-safety claim asserted but reference [7] quote not reproduced; research reference URL correct but inline citation in workflow comment uses a different URL than the research report |
| Actionability | 0.15 | 0.88 | 0.132 | Change is minimal, self-contained, and reversible; comments clearly explain each filter's purpose; the vestigial `[skip-bump]` on workflow_dispatch branch is confusing to future maintainers |
| Traceability | 0.10 | 0.85 | 0.085 | #187 referenced in both workflow comment and paths-ignore block; research report exists and is linked in commit context; workflow comment URL matches research reference [1] but does not link to the research file itself |
| **TOTAL** | **1.00** | | **0.839** | |

---

## Detailed Dimension Analysis

### Completeness (0.80/1.00)

**Evidence:**

Filter B covers 8 of the conventional commit no-bump prefixes:
- `ci:` / `ci(`
- `deps:` / `deps(`
- `docs:` / `docs(`
- `chore:` / `chore(`
- `style:` / `style(`
- `refactor:` / `refactor(`
- `test:` / `test(`
- `build:` / `build(`

Filter A (`paths-ignore`) excludes the correct set of clearly non-version-relevant top-level directories and file patterns. `pyproject.toml` is correctly NOT excluded (the version field lives there). `src/` is correctly NOT excluded.

**Gaps:**

1. **`revert:` prefix absent from Filter B.** The Conventional Commits v1.0 spec defines `revert:` as a first-class type. A commit like `revert: feat: add login endpoint` does not start with any of the 8 blocked prefixes, so it passes Filter B and triggers the job. The `jerry ci detect-bump-type` step then decides whether a revert warrants a bump. This is not a false version bump (the CLI decides), but it means the workflow wastes a runner on every revert commit when the intent of Filter B is to short-circuit obvious no-ops at the job level. The research report does not address `revert:` at all — this is a research gap that propagated into the implementation.

2. **`.claude/**` not in paths-ignore.** The research's recommended configuration (L2 section, line 248 of research) listed `.claude/**` as a candidate exclusion but the final implementation omits it. Changes to `.claude/rules/`, `.claude/settings.local.json`, etc. alone will trigger the workflow. The workflow then correctly returns `none` from the CLI, but a runner is allocated unnecessarily.

3. **`.claude-plugin/**` not in paths-ignore.** Same analysis as `.claude/**`. The research did not explicitly recommend excluding `.claude-plugin/`, and the implementation omits it. Plugin configuration changes alone would trigger the workflow.

4. **`uv.lock` not in paths-ignore.** A lockfile-only commit (e.g., manual `uv lock` run) triggers the workflow. Mitigated by Filter B if the commit uses `chore:`, but not mitigated for commits with non-conventional messages. Low severity since the job returns `none`.

Gaps 2-4 cause false-positive workflow runs (wasted runners) but not false version bumps — the CLI provides the authoritative gate. Gap 1 (`revert:`) is the more meaningful functional gap.

**Score calibration:** Rubric 0.7-0.89 band: "Most requirements addressed, minor gaps." The 8 covered prefixes are the most common. The missing `revert:` and three paths-ignore gaps are real but not catastrophic. Score: 0.80.

**Improvement Path:**

Add `!startsWith(github.event.head_commit.message, 'revert:')` and `!startsWith(github.event.head_commit.message, 'revert(')` to Filter B. Add `.claude/**`, `.claude-plugin/**`, and optionally `uv.lock` to `paths-ignore`.

---

### Internal Consistency (0.85/1.00)

**Evidence:**

The two filters are architecturally complementary with no conflicts:
- Filter A (trigger-level `paths-ignore`) prevents the workflow from starting when only non-version-relevant files change.
- Filter B (job-level `if:`) prevents the job from executing when the commit type cannot produce a version bump.
- The research correctly establishes these as AND-stacked layers (L1 section, "Interaction: Path Filters + Job-Level `if:`").
- The `workflow_dispatch` branch of the `if:` condition correctly excludes all prefix checks (manual dispatch always runs) — consistent with the comment on line 83 ("3. workflow_dispatch always runs (manual override)").
- `paths-ignore` correctly does not apply to `workflow_dispatch` — this is consistent with the research finding (Q2, Q13) and the comment on line 18 ("Does NOT affect workflow_dispatch").

**Gaps:**

1. **Vestigial `[skip-bump]` check on `workflow_dispatch` branch (lines 86-88).** The `if:` condition's `workflow_dispatch` branch includes `!contains(github.event.head_commit.message, '[skip-bump]')`. On `workflow_dispatch` events, `github.event.head_commit` is null (there is no associated push commit). The expression `contains(null, '[skip-bump]')` evaluates to false (safe per null coercion, research line 173), making `!contains(...)` always true. The check never fires. This creates an inconsistency between the comment ("workflow_dispatch always runs") and the code (which appears to allow suppression via `[skip-bump]`). A future maintainer may believe they can suppress manual runs by adding `[skip-bump]` somewhere, which is incorrect.

2. **Minor:** The comment on line 77 says "Not a version bump commit (prevent infinite loop)" but the actual check is `github.actor != 'github-actions[bot]'`, which catches all bot commits, not just version bumps. The comment is slightly narrower than the implementation. Not a functional issue.

**Improvement Path:**

Remove the `!contains(github.event.head_commit.message, '[skip-bump]')` clause from the `workflow_dispatch` branch, or add a comment explaining it is always-true-on-dispatch (null coercion). Update the infinite-loop comment to accurately reflect the bot-actor check scope.

---

### Methodological Rigor (0.92/1.00)

**Evidence:**

The methodological choices are well-reasoned and research-backed:

1. **`paths-ignore` over `paths` (denylist over allowlist):** The research correctly identifies that the set of irrelevant paths is smaller and more stable than the set of relevant paths (L2, "What NOT to Do", item 1). The implementation follows this recommendation. This is the correct engineering choice — an allowlist for a repository this size would require updating every time a new source directory is added.

2. **Job-level `if:` for commit message filtering:** The research establishes that trigger-level commit message filtering is impossible in GitHub Actions (Q6). The implementation correctly uses job-level conditions, consistent with the existing pattern.

3. **Dual-layer defense-in-depth:** Filter A catches file-only changes (documentation, tests); Filter B catches commit-type-only signals (ci:, chore:). A commit that touches `src/` with a `ci:` message would pass Filter A (src/ is not excluded) and be caught by Filter B. A documentation-only commit with a `feat:` message would be caught by Filter A before Filter B even evaluates. The layers are genuinely complementary.

4. **Rejection of `dorny/paths-filter`:** The research correctly argues this adds supply chain risk for no benefit when branch protection is not a concern (L2, "What NOT to Do", item 2). The implementation follows this.

5. **`workflow_dispatch` independence:** The implementation correctly allows manual triggers to bypass both filters, consistent with the research (Q2, Q13) and the operational need for emergency manual version bumps.

**Gaps:**

1. **`startsWith()` variant pairing (`ci:` and `ci(`):** The research template (lines 147-160) includes both `ci:` and `ci(` variants to handle scoped commits (`ci(github-actions): fix something`). The implementation correctly includes both variants for all 8 prefixes. This is rigorously thorough.

2. **No coverage of the `revert:` case in the methodology.** The research does not analyze how reverting a `feat:` commit should be handled. Should `revert: feat: ...` trigger a version bump? The methodology is silent on this. At 0.92, this is the only notable gap in an otherwise rigorous approach.

**Improvement Path:**

Address the `revert:` case in the research report and add explicit methodology notes on how revert commits interact with bump detection (either block `revert:` at Filter B or document that the CLI handles it).

---

### Evidence Quality (0.72/1.00)

**Evidence:**

The research report cites 16 references, mostly GitHub official documentation. The workflow comments reference the docs URL directly (line 19: `https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#onpushpull_requestpull_request_targetpathspaths-ignore`). This is a specific, accurate URL.

**Gaps:**

1. **`startsWith()` case-insensitivity claim — cited but not quoted.** The workflow comment at line 81 states "startsWith() is case-insensitive per GitHub Actions docs." The research at line 163 states "The `startsWith()` function is NOT case-sensitive per GitHub documentation." Reference [7] is cited ("Evaluate expressions in workflows and actions - GitHub Docs"). However, the research does not reproduce the specific text from the docs that confirms this. The GitHub expressions documentation does say string comparison functions are "case insensitive" but this applies to `==` and `!=` operators explicitly; the docs also state `startsWith()` and `contains()` are "case insensitive" in the same section. The claim is likely correct, but the scoring rubric requires that claims be supported by credible evidence — a citation without the quoted passage is weaker than a citation with it. This is the primary evidence quality weakness.

2. **Null-safety claim for `head_commit.message` on `workflow_dispatch` — asserted, not proven.** The research (line 173) states "`!startsWith(null, 'ci:')` returns `true` (safe)" with reference [7]. Reference [7] does describe null coercion ("null coerces to the empty string, 0, or false"), but the research does not quote the specific behavior. The implementation relies on this being safe, and it is a behavioral guarantee, not a derived claim.

3. **Squash merge path filter issue (reference [10]) — attributed to a community discussion, not official docs.** The research correctly flags this as a "known issue" but the evidence is a community discussion thread (#179965), not GitHub's official documentation. The claim that the root cause is "inherited `[skip ci]` from commit body" is plausible but not definitively confirmed by GitHub engineering.

4. **Branch protection claim is correct but relies on current state.** The research argues path filtering is safe because version-bump is not a required status check. This is verified by reviewing `ci.yml`. The claim is evidence-grounded, but there is no reference to the specific `ci.yml` lines that confirm this. A reader cannot independently verify without reading the other file.

**Score calibration:** Rubric 0.5-0.69: "Some claims unsupported." Rubric 0.7-0.89: "Most claims supported." The primary claims (paths-ignore syntax, workflow_dispatch independence, Filter B syntax) are all well-supported. The case-insensitivity claim is the most load-bearing unsupported claim — if it were wrong, the entire Filter B would fail to catch uppercase-prefixed commits. However, it is likely correct and there is a citation. Score: 0.72.

**Improvement Path:**

Reproduce the exact quote from the GitHub expressions docs confirming `startsWith()` case-insensitivity. Add a direct quote from reference [7] on null coercion. Add a reference to the specific `ci.yml` job that confirms version-bump is not a required check.

---

### Actionability (0.88/1.00)

**Evidence:**

1. **Change is minimal and self-contained.** Filter A adds 13 lines to the `on.push` block. Filter B adds 16 lines to the existing `if:` condition. Both changes are isolated to `version-bump.yml`.

2. **Reversible in minutes.** Removing the `paths-ignore` block or the `startsWith()` conditions restores the prior behavior exactly. No migration, no data changes, no downstream effects.

3. **Comments explain the design rationale.** Lines 15-19 explain Filter A's design choice (denylist vs allowlist, workflow_dispatch independence, docs URL). Lines 77-83 explain Filter B's purpose and the case-insensitivity property.

4. **Well-integrated with existing code.** Filter B slots into the existing `if:` structure without restructuring it. The `workflow_dispatch` and `push` branches are cleanly separated.

**Gaps:**

1. **Vestigial `[skip-bump]` check on `workflow_dispatch` branch creates a maintenance trap.** A future engineer reading lines 86-88 may believe they can suppress an unwanted manual dispatch by pushing a commit with `[skip-bump]` in the message. This is incorrect — the check always evaluates to true on `workflow_dispatch`. The comment "3. workflow_dispatch always runs" contradicts the presence of the check. This reduces actionability because the code is not self-evidently correct to a reader unfamiliar with null coercion behavior.

2. **No test or canary for Filter B.** There is no automated test that exercises the `if:` condition to verify it blocks the expected prefixes. The implementation relies entirely on manual verification. This is acceptable for a YAML condition (no testing framework supports it natively), but a comment documenting test scenarios would help.

**Improvement Path:**

Remove or annotate the vestigial `[skip-bump]` check. Add a comment block listing the expected skip scenarios (e.g., "A commit like `ci: update pipeline` should skip; a commit like `feat: add feature` should run").

---

### Traceability (0.85/1.00)

**Evidence:**

1. **#187 is referenced in the workflow comments** (line 15: `# #187 Filter A:` and line 77: `# 2. Not a non-bump conventional commit prefix (#187 Filter B)`). The issue number is traceable.

2. **Research report exists** at `projects/PROJ-030-bugs/research/workflow-filtering-research.md` and was clearly consulted — the implementation matches the research recommendations closely (dual filtering, paths-ignore over paths, same prefix set, same workflow_dispatch handling).

3. **The workflow comment URL** (line 19) is a specific GitHub docs anchor, traceable to the exact syntax documentation section.

**Gaps:**

1. **The workflow does not reference the research report.** Lines 15-19 reference GitHub docs and #187 but do not link to the research file. A future maintainer making changes to the filter would benefit from knowing the research exists. The research contains important context (squash merge edge case, branch protection implications, 300-file limit, `revert:` gap) that is not summarized in the workflow.

2. **The research report does not self-reference the implementation.** The research does not include a "Applied in" or "Status" section pointing back to the workflow file it informed. Traceability is one-directional (implementation could trace to research if it referenced it; research cannot point to implementation).

3. **Comment on line 81 ("startsWith() is case-insensitive per GitHub Actions docs") has no inline URL.** The rationale is cited in the research report but not in the workflow comment itself. A maintainer relying only on the workflow file cannot trace this claim to its source without reading the research report.

**Improvement Path:**

Add a comment referencing the research file path (e.g., `# See: projects/PROJ-030-bugs/research/workflow-filtering-research.md`). Add a URL to the expressions docs in the case-insensitivity comment. Add an "Applied in" section to the research report pointing to `version-bump.yml`.

---

## Critical Check Results

| Check | Result | Detail |
|-------|--------|--------|
| Does "Merge pull request #N from dependabot/..." bypass Filter B? | PASS (correct) | Regular merge commit messages do not start with any blocked prefix. The workflow correctly runs and evaluates for a version bump. Dependabot's own default title format ("Bump X from Y to Z") also passes Filter B. |
| Is `github.event.head_commit.message` the right field for squash merges? | PASS with caveat | For squash merges, this field contains the PR title (the squash commit message). If the PR title is "feat: add feature", Filter B correctly allows the run. If the PR title is "ci: update workflow", Filter B correctly skips. Behavior is correct but depends on PR title discipline. The null-safety on `workflow_dispatch` is safe per null coercion. |
| Does paths-ignore accidentally exclude pyproject.toml? | PASS | `pyproject.toml` is NOT in the paths-ignore list. Version bumps correctly trigger when pyproject.toml changes. |
| Does paths-ignore accidentally exclude .claude-plugin/? | FAIL (gap, not blocker) | `.claude-plugin/` is NOT excluded. Changes to this directory alone trigger the workflow unnecessarily. No false version bumps result (the CLI returns `none`), but a runner is wasted. The research recommended `.claude/**` but did not address `.claude-plugin/`. |

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.72 | 0.88 | Reproduce the exact GitHub docs quote confirming `startsWith()` case-insensitivity. Add the sentence from `https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/evaluate-expressions-in-workflows-and-actions#functions` that confirms case insensitivity. Add inline URL to the case-insensitivity comment in the workflow (line 81). |
| 2 | Completeness | 0.80 | 0.90 | Add `!startsWith(github.event.head_commit.message, 'revert:')` and `!startsWith(github.event.head_commit.message, 'revert(')` to Filter B. Add `.claude/**` and `.claude-plugin/**` to `paths-ignore`. |
| 3 | Internal Consistency | 0.85 | 0.94 | Remove the vestigial `!contains(github.event.head_commit.message, '[skip-bump]')` from the `workflow_dispatch` branch of the `if:` condition, or add a comment explaining it always evaluates to true due to null coercion and is present for documentation purposes only. |
| 4 | Traceability | 0.85 | 0.94 | Add a comment in version-bump.yml referencing the research report path. Add an "Applied in" section to the research report pointing to `.github/workflows/version-bump.yml`. |
| 5 | Actionability | 0.88 | 0.94 | Add a comment block near Filter B listing the expected skip and run scenarios (e.g., "ci: update pipeline -> skipped; feat: add feature -> runs; Merge pull request #42 -> runs"). |

---

## Composite Score Verification

```
Completeness:          0.80 * 0.20 = 0.160
Internal Consistency:  0.85 * 0.20 = 0.170
Methodological Rigor:  0.92 * 0.20 = 0.184
Evidence Quality:      0.72 * 0.15 = 0.108
Actionability:         0.88 * 0.15 = 0.132
Traceability:          0.85 * 0.10 = 0.085
                                    -------
TOTAL:                              0.839
```

Threshold: 0.95. Gap: 0.111. **REVISE.**

---

## Leniency Bias Check
- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Evidence Quality held at 0.72, not rounded up to 0.75)
- [x] First-draft calibration considered (implementation is close to a first draft of this filter; gaps are real)
- [x] No dimension scored above 0.95 without exceptional evidence (Methodological Rigor at 0.92 is the highest; justified by thorough research-backed design)
- [x] Critical checks all evaluated explicitly before scoring
- [x] Score 0.839 is below the 0.95 threshold; REVISE verdict is correct

---

## Session Context (adv-scorer -> orchestrator)

```yaml
verdict: REVISE
composite_score: 0.839
threshold: 0.95
weakest_dimension: evidence_quality
weakest_score: 0.72
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Reproduce exact GitHub docs quote confirming startsWith() case-insensitivity; add inline URL to line 81 comment"
  - "Add revert: / revert( to Filter B; add .claude/** and .claude-plugin/** to paths-ignore"
  - "Remove vestigial [skip-bump] check from workflow_dispatch branch or annotate null-coercion behavior"
  - "Add research report path reference to workflow comments; add Applied-in section to research report"
  - "Add expected skip/run scenario examples near Filter B"
```
