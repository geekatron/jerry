# Dependabot Grouping CI Architecture Assessment

> C1 architecture assessment for PROJ-030-bugs. Evaluates how the proposed Dependabot grouping configuration interacts with Jerry's version-bump pipeline, supply chain security posture, and existing open PRs.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Assessment 1: Commit Prefix Resolution](#assessment-1-commit-prefix-resolution) | How `ci:` and `deps:` prefixes resolve through the bump detector |
| [Assessment 2: Major Pip Updates as Individual PRs](#assessment-2-major-pip-updates-as-individual-prs) | Supply chain security analysis |
| [Assessment 3: GitHub Actions Major Bumps](#assessment-3-github-actions-major-bumps) | Whether Actions major bumps should also be individual |
| [Assessment 4: open-pull-requests-limit and Grouping](#assessment-4-open-pull-requests-limit-and-grouping) | How the limit interacts with grouped PRs |
| [Assessment 5: Transition Behavior for Existing PRs](#assessment-5-transition-behavior-for-existing-prs) | What happens to the 13 open PRs |
| [Summary of Findings](#summary-of-findings) | Consolidated findings table |

---

## Assessment 1: Commit Prefix Resolution

**Question:** The proposed grouping uses `ci:` prefix for GitHub Actions updates and `deps:` prefix for pip updates. What bump type do these resolve to in the version-bump workflow?

**Answer: Both resolve to `BumpType.NONE`. The version-bump workflow will correctly skip these.**

The resolution path is:

1. A grouped Dependabot PR merges to `main`, producing one `push` event.
2. The version-bump workflow triggers and runs `uv run jerry ci detect-bump-type --since-tag`.
3. The `GitCommitLogReader` reads commits since the latest `v*` tag via `git log {tag}..HEAD`.
4. For each commit subject, `ConventionalCommit.parse()` extracts the `commit_type` field (the prefix before the colon).
5. The `bump_type` property checks the type against `_MINOR_TYPES = frozenset({"feat"})` and `_PATCH_TYPES = frozenset({"fix", "perf"})`.
6. Neither `ci` nor `deps` appears in either set, so both return `BumpType.NONE`.

The `BumpTypeDetector.detect()` method returns the highest-severity bump across all commits since the last tag. If the only new commits are Dependabot merges with `ci:` or `deps:` prefixes, the result is `BumpType.NONE`, and the workflow outputs "Skipped" without touching the version.

**Key interaction detail:** The `--since-tag` flag scans all commits since the latest tag, not just the one that triggered the push. This means if a `feat:` commit was merged before the Dependabot group, the grouped PR merge would trigger a version bump for that earlier `feat:` commit. This is correct behavior -- the bump detector is cumulative, not per-push. But it means the "skip" behavior for Dependabot merges only holds when no bump-worthy commits are pending.

**Grouped PR commit structure:** When Dependabot creates a grouped PR, it contains one commit per dependency update, each using the configured prefix. When this PR is squash-merged (Jerry's default merge strategy), GitHub produces a single squash commit whose subject is typically the PR title. The PR title for grouped updates follows the pattern `Bump the {group-name} group with N updates`. This does NOT match conventional commit format, which means `ConventionalCommit.parse()` will raise `CommitParseError`, the detector will catch the exception and skip the commit, and it resolves to `BumpType.NONE`.

If the PR is merge-committed instead of squash-merged, the individual `ci:` or `deps:` commits are preserved on `main`, and each individually resolves to `NONE` as analyzed above.

**Either merge strategy produces the correct result.** No changes to the version-bump workflow are needed.

---

## Assessment 2: Major Pip Updates as Individual PRs

**Question:** Is separating major pip updates into individual PRs the right call for Jerry's supply chain security posture?

**Answer: Yes. This is the correct decision, and the research report's recommendation aligns with Jerry's existing security controls.**

Rationale:

1. **Supply chain security context.** Jerry's version-bump workflow includes a lockfile diff guard (lines 187-192 of `version-bump.yml`) that warns when `uv.lock` changes more than the version field. This guard is designed to detect transitive dependency changes that could indicate a supply chain compromise. A major version bump is precisely the case most likely to introduce transitive dependency changes, making individual review critical.

2. **Major bumps change APIs.** A major version bump in a Python dependency signals breaking changes per SemVer. Jerry's codebase must be verified against the new API. Grouping major bumps together would obscure which dependency broke compatibility if CI fails.

3. **Current posture alignment.** Jerry pins GitHub Actions to commit SHAs (EN-001) and pins `bump-my-version` to an exact version (BUG-003/RISK-01). The existing security controls demonstrate a "trust but verify" philosophy for dependency updates. Keeping major pip updates individual is consistent with this posture.

4. **Volume is low.** Major pip version bumps are infrequent (typically 1-2 per quarter for a project of Jerry's size). The PR noise reduction from grouping comes almost entirely from minor/patch batching and Actions grouping. Keeping majors individual adds negligible overhead.

**One consideration:** The proposed config does not explicitly exclude major updates from the `pip-minor-patch` group -- it relies on `update-types: ["minor", "patch"]` to implicitly leave major updates ungrouped. This is the correct approach. Major updates that are not matched by any group rule fall through to individual PRs by default. No `exclude-patterns` are needed for this behavior.

---

## Assessment 3: GitHub Actions Major Bumps

**Question:** Should GitHub Actions updates be grouped together given the v5 to v6, v4 to v7 major bumps currently open? Or should Actions major bumps also be individual?

**Answer: Group them together. Actions major bumps are qualitatively different from pip major bumps and do not require individual review.**

Rationale:

1. **SHA pinning changes the risk model.** Jerry pins all GitHub Actions to commit SHAs (EN-001). When Dependabot proposes an Actions update, the PR changes a SHA hash. The semantic version in the comment (e.g., `# v5.0.0` to `# v6.0.0`) is informational only. What actually runs is determined by the SHA, not the version tag. This means a "major bump" in Actions is not the same trust boundary crossing as a major bump in a runtime Python dependency.

2. **Actions do not have transitive dependency risk.** A GitHub Action runs in its own container/environment. Updating `actions/checkout` from v5 to v6 does not change Jerry's Python dependency tree, lockfile, or runtime behavior. The lockfile diff guard in version-bump.yml would not even trigger.

3. **CI tests catch breakage.** If a new Actions version introduces an incompatible change (e.g., changed input names), the CI workflow itself will fail on the grouped PR before it can merge. The failure isolation trade-off is acceptable because: (a) Actions updates rarely break CI; (b) when they do, the failure message typically names the specific action; (c) the fallback is straightforward -- close the grouped PR, add `exclude-patterns` for the problematic action, and re-run.

4. **The alternative creates more noise, not more safety.** Splitting Actions into "major individual, minor/patch grouped" would produce 4-5 individual PRs for the current backlog (checkout v5 to v6, setup-python v5 to v6, etc.) plus a group for minor updates. This increases PR count without proportional security benefit.

**However, there is one exception to consider:** If Jerry adds a third-party, non-GitHub-authored Action (e.g., a community action for deployment, secrets scanning, or artifact management), major bumps to that action warrant closer review. For now, Jerry uses only first-party GitHub Actions (actions/checkout, actions/setup-python, actions/upload-artifact) and Astral's setup-uv action. All are high-trust publishers. The `patterns: ["*"]` grouping is appropriate at this publisher trust level.

**Recommendation:** Keep `patterns: ["*"]` for Actions. If a low-trust third-party Action is added in the future, split the group using `exclude-patterns` for that specific action.

---

## Assessment 4: open-pull-requests-limit and Grouping

**Question:** How does `open-pull-requests-limit` interact with grouping? Does a group count as 1 against the limit?

**Answer: Yes, a grouped PR counts as 1 against the limit.**

The `open-pull-requests-limit` counts open Dependabot PRs per ecosystem. A grouped PR is one PR, so it counts as 1 regardless of how many dependency updates it contains. Specifically:

- **github-actions ecosystem (limit: 10):** With `patterns: ["*"]` grouping, Dependabot creates at most 1 grouped PR for all Actions updates. That counts as 1 against the limit of 10. The remaining 9 slots are available for any dependencies that fall outside the group (which, with `["*"]`, is none). The limit of 10 is now over-provisioned but harmless.

- **pip ecosystem (limit: 5):** With `update-types: ["minor", "patch"]` grouping, Dependabot creates 1 grouped PR for all minor/patch updates (counts as 1) plus individual PRs for each major update. If there are 3 pending major updates, that is 1 (group) + 3 (individual majors) = 4 against the limit of 5. The limit of 5 is appropriate for this configuration.

**Implication:** The current `open-pull-requests-limit: 10` for github-actions could be reduced to 5 after grouping is enabled, since it is unlikely to need more than a few slots. However, reducing it provides no material benefit (Dependabot does not consume resources for unused limit headroom), so leaving it at 10 is fine.

---

## Assessment 5: Transition Behavior for Existing PRs

**Question:** What happens to the 13 currently-open Dependabot PRs when grouping is added -- does Dependabot close and re-create them as grouped?

**Answer: Dependabot will close the existing individual PRs and create new grouped PRs on the next scheduled run.**

The behavior is documented in GitHub's Dependabot options reference: when the `groups` configuration is added or modified, Dependabot evaluates all pending updates against the new group rules on the next scheduled run (Monday, per Jerry's config). Dependencies that now match a group are consolidated into a new grouped PR. The individual PRs for those dependencies are automatically closed by Dependabot with a comment indicating they have been superseded by the grouped PR.

**Expected transition for Jerry's 13 open PRs:**

| Current PRs | New State | Rationale |
|---|---|---|
| ~10 individual GitHub Actions PRs | Closed; replaced by 1 grouped PR (`actions-all` group) | All match `patterns: ["*"]` |
| ~2-3 individual pip minor/patch PRs | Closed; replaced by 1 grouped PR (`pip-minor-patch` group) | Match `update-types: ["minor", "patch"]` |
| Any individual pip major PRs | Remain open as individual PRs | Not matched by any group |

**Timing:** The transition happens on the next scheduled Dependabot run after the config change merges to `main` (Monday). There may be a brief period (up to 1 week) where both old individual PRs and new grouped PRs coexist if the schedule does not immediately trigger. Manually closing the old PRs is not necessary -- Dependabot handles the cleanup.

**One operational note:** The transition creates a burst of PR close/open activity in the repository's notification stream. This is a one-time event with no lasting impact.

---

## Summary of Findings

| # | Question | Finding | Action Required |
|---|----------|---------|-----------------|
| 1 | Commit prefix resolution | `ci:` and `deps:` both resolve to `BumpType.NONE`. Squash-merge PR titles also resolve to NONE (fail to parse, caught and skipped). No version-bump workflow changes needed. | None |
| 2 | Major pip updates as individual PRs | Correct decision. Aligns with existing supply chain controls (lockfile diff guard, SHA pinning philosophy). Major bumps are infrequent; individual review adds negligible overhead. | None |
| 3 | GitHub Actions major bumps | Group them. SHA pinning, first-party publisher trust, and CI-as-gatekeeper make individual review unnecessary. Re-evaluate if low-trust third-party Actions are added. | None; monitor publisher trust if new Actions added |
| 4 | open-pull-requests-limit interaction | Grouped PR counts as 1 against the limit. Current limits (10 for Actions, 5 for pip) are appropriate post-grouping. | None; optionally reduce Actions limit to 5 |
| 5 | Transition of existing PRs | Dependabot auto-closes individual PRs and creates grouped replacements on next scheduled run. One-time notification burst; no manual intervention needed. | None; expect PR close/open activity on next Monday |

**Overall assessment:** The proposed Dependabot grouping configuration from the research report is well-designed for Jerry's CI architecture. It interacts correctly with the version-bump workflow, maintains the supply chain security posture for high-risk updates (pip majors), and appropriately batches low-risk updates (Actions, pip minor/patch). No workflow, code, or infrastructure changes are required beyond the `dependabot.yml` edit.

---

*Assessment conducted: 2026-03-11*
*Agent: eng-architect*
*Project: PROJ-030-bugs*
*Criticality: C1 (Routine) -- single config file, fully reversible, no architectural impact*
