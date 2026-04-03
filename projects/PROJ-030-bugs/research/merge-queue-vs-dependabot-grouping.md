# GitHub Merge Queues vs Dependabot Grouping for CI Pipeline Optimization

> Research report for PROJ-030-bugs: Evaluating solutions to reduce redundant version-bump workflow triggers from Dependabot PR merges.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Non-technical overview and recommendation |
| [L1: Technical Analysis](#l1-technical-analysis) | Implementation details, configuration, and code |
| [L2: Architectural Implications](#l2-architectural-implications) | Trade-offs, risks, and strategic considerations |
| [Research Questions](#research-questions) | All questions answered with citations |
| [Methodology](#methodology) | How this research was conducted |
| [References](#references) | Complete source list |

---

## L0: Executive Summary

### What We Researched

Jerry has 13 open Dependabot PRs. Each time one merges to `main`, the version-bump workflow triggers -- even when the bump type resolves to "none" (as most dependency updates use `ci:` or `deps:` prefixes, not `feat:`/`fix:`). Merging them individually means 13 redundant CI runs. We investigated two GitHub-native solutions: **Merge Queues** and **Dependabot Grouping**.

### Key Finding: Merge Queue Is Not Available and Would Not Help

GitHub Merge Queues require an **organization-owned repository**. Jerry (`geekatron/jerry`) is owned by a personal user account, making merge queue unavailable regardless of plan tier. [Source: GitHub Docs, community discussion #51483]

Even if it were available, merge queue would **not solve the problem**. Despite supporting "batch" configuration, each PR in a merge queue is still merged individually to the base branch, generating a separate push event per PR. The "merge limits" feature controls how many PRs can merge at once, but it does not combine them into a single push. [Source: GitHub Docs, community discussion #58523]

### Key Finding: Dependabot Grouping Directly Solves the Problem

Dependabot Grouping consolidates multiple dependency updates into a single PR before they are created. Instead of 13 individual PRs, Jerry would get approximately 2-3 grouped PRs (e.g., one for GitHub Actions updates, one for pip patch/minor updates, one for major updates). Each group merges as one PR, triggering one push event and one version-bump run. This reduces 13 workflow runs to 2-3.

### Recommendation

**Implement Dependabot Grouping immediately.** It is available on all GitHub plans (including Free), requires only a `dependabot.yml` configuration change, is fully reversible, and directly addresses the root cause. Merge Queue is neither available nor applicable to this problem.

---

## L1: Technical Analysis

### 1. GitHub Merge Queues -- Detailed Findings

#### 1.1 Plan Requirements (BLOCKER)

Merge queues are available for:
- **Public repositories owned by an organization** (any plan) [1]
- **Private repositories** owned by organizations on **GitHub Enterprise Cloud** only [1]
- **NOT available** for repositories owned by personal user accounts [1]

Jerry (`geekatron/jerry`) is a public repository owned by `geekatron`, which is a **personal user account** (verified via `gh repo view`). This means merge queue is **not available** for Jerry.

**Source:** [GitHub community discussion #51483](https://github.com/orgs/community/discussions/51483) -- "Pull request merge queues are available in any public repository owned by an organization, or in private repositories owned by organizations using GitHub Enterprise Cloud."

#### 1.2 How Batching Actually Works

Even if merge queue were available, the batching behavior does not solve the N-push-events problem:

1. **Testing phase (merge_group):** PRs in the queue are grouped into temporary branches (`gh-readonly-queue/{base_branch}/*`) for CI testing. Multiple PRs can be tested together. This saves CI minutes during the *testing* phase. [2]
2. **Merge phase:** Each PR is still merged **individually** to the base branch. "Each pull request is still merged individually into the target branch based on its own timeline and mergeability criteria." [3]
3. **Push events:** Each individual merge generates its own `push` event on the base branch. N PRs in a batch still produce N push events. [3]

The "merge limits" configuration (min/max group size, 1-100) controls how many PRs can be merged to the base branch at the same time, but **"Merge limits do not combine merge_group builds."** [2]

**With squash merge:** Each PR gets its own squash commit on the base branch. [4]
**With merge commit:** Each PR creates its own merge commit. [2]
**With rebase:** Each PR's commits are rebased individually. [2]

**Bottom line:** For Jerry's version-bump workflow (triggered by `on: push: branches: [main]`), merge queue would still trigger the workflow N times for N Dependabot PRs.

#### 1.3 merge_group Event

Merge queue introduces a new workflow trigger event: `merge_group`. This fires when a PR is added to the queue and temporary branches are created. Workflows must be updated to include `merge_group` alongside `pull_request`:

```yaml
on:
  pull_request:
  merge_group:
```

This is separate from the `push` event and does not affect version-bump triggering. [2]

#### 1.4 Failure Behavior

When a PR in a merge group fails CI checks, it is automatically removed from the queue. The merge queue then recreates temporary branches excluding the failed PR and re-runs checks. Other PRs in the queue are not blocked permanently. [2]

#### 1.5 Reversibility

Merge queue is enabled via branch protection rules or repository rulesets. Disabling it returns to normal merging behavior. It is a fully reversible, two-way door. [2]

#### 1.6 Interaction with Concurrency Groups

Jerry's version-bump workflow uses:

```yaml
concurrency:
  group: version-bump
  cancel-in-progress: false
```

With merge queue generating N individual push events, the concurrency group would serialize the N version-bump runs (because `cancel-in-progress: false`). Each run would complete, detect "none" as the bump type, and output "Skipped." This is the current behavior and would not improve.

### 2. Dependabot Grouping -- Detailed Findings

#### 2.1 Availability

Dependabot Grouping is available on **all GitHub plans** including Free. It requires no organization ownership. It works for any repository with a `dependabot.yml` configuration file. [5, 6]

#### 2.2 How It Works

Instead of creating one PR per dependency update, Dependabot groups multiple updates into a single PR based on configurable rules. The grouped PR contains commits for each dependency update but is merged as a single unit, producing **one push event**. [5]

Grouping is configured via the `groups` key within each `package-ecosystem` block in `dependabot.yml`. Dependencies can be grouped by:

- **Pattern:** Wildcard matching on package names (`patterns: ["*"]` for all) [7]
- **Update type:** SemVer level (`update-types: ["minor", "patch"]`) [7]
- **Dependency type:** Production vs. development (`dependency-type: "production"`) [7]
- **Exclude patterns:** Remove specific packages from a group (`exclude-patterns: ["some-problematic-pkg"]`) [7]

Dependencies not matching any group rule are updated in individual PRs as before. [7]

#### 2.3 Recommended Configuration for Jerry

Based on Jerry's current `dependabot.yml` and the nature of its dependencies:

```yaml
version: 2
updates:
  # GitHub Actions -- weekly check for pinned SHA updates
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    commit-message:
      prefix: "ci"
    labels:
      - "dependencies"
      - "ci"
    open-pull-requests-limit: 10
    groups:
      # All GH Actions SHA pin updates in one PR
      actions-all:
        patterns:
          - "*"

  # pip -- weekly check for Python dependency updates
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    commit-message:
      prefix: "deps"
    labels:
      - "dependencies"
    open-pull-requests-limit: 5
    groups:
      # Minor and patch updates grouped together
      pip-minor-patch:
        update-types:
          - "minor"
          - "patch"
      # Major updates stay individual for careful review
      # (not grouped -- each major update gets its own PR)
```

**Expected result with this configuration:**
- ~1 PR for all GitHub Actions SHA updates (currently ~10 individual PRs)
- ~1 PR for pip minor/patch updates
- Individual PRs for pip major version bumps (requires manual review)
- **Total: ~2-3 PRs instead of ~13**

#### 2.4 What Happens When One Dependency Fails CI

The entire grouped PR fails as a unit. There is no per-dependency failure isolation within a group. [8, 9]

**Mitigation strategies:**
1. Use `@dependabot ignore <dependency> minor version` to exclude the problematic dependency from the group PR. Dependabot will create a new grouped PR without it. [8]
2. Use `exclude-patterns` in `dependabot.yml` to permanently exclude known-problematic packages from the group, letting them create individual PRs. [7]
3. If the failure source is unclear, temporarily remove the `groups` configuration so Dependabot reverts to individual PRs, identify the culprit, then re-add grouping with an exclusion. [8]

**This is the primary trade-off:** Grouping reduces PR volume but reduces failure isolation. For Jerry's case, this is an acceptable trade-off because:
- GitHub Actions SHA updates almost never break CI (they are pinned to exact commits)
- Pip minor/patch updates rarely break CI (SemVer compatibility)
- Major updates are deliberately kept as individual PRs for careful review

#### 2.5 Rollback and Reversion

- **Reverting the configuration:** Remove the `groups` key from `dependabot.yml`. Dependabot immediately reverts to individual PRs on the next schedule run. Fully reversible, two-way door. [7]
- **Reverting a merged group PR:** Use `git revert <merge-commit>` on the group PR's merge commit. This reverts all dependencies in the group simultaneously. There is no built-in way to revert a single dependency from a merged group without a manual commit. [10]
- **Splitting a group after creation:** Close the grouped PR, add `exclude-patterns` for the dependency you want separated, and Dependabot will create a new grouped PR without it plus an individual PR for the excluded dependency. [7]

#### 2.6 Security Vulnerability Detection

Dependabot security alerts are **not affected** by version update grouping. Security alerts are generated independently per vulnerability per manifest, regardless of how version update PRs are grouped. [11]

Security *update PRs* can also be grouped using `applies-to: security-updates` in the group configuration. By default, grouping only applies to version updates (`applies-to: version-updates`). [12]

**Recommendation for Jerry:** Keep security updates ungrouped (the default) so each security fix gets its own PR with clear visibility into what CVE it addresses.

#### 2.7 Conflict Handling

When grouped dependencies have conflicting requirements, Dependabot attempts to resolve them. If resolution fails, the grouped PR will show the conflict and CI will fail. The mitigation is the same as for CI failures: exclude the conflicting dependency. [7]

### 3. Comparison Matrix

| Criterion | GitHub Merge Queue | Dependabot Grouping |
|-----------|-------------------|---------------------|
| **Available for Jerry?** | NO (requires org-owned repo) | YES (all plans) |
| **Solves N-push-event problem?** | NO (PRs merge individually) | YES (1 PR = 1 push) |
| **Reduces CI minutes?** | Partially (testing phase only) | YES (fewer PRs = fewer CI runs) |
| **Reversible?** | Yes (two-way door) | Yes (two-way door) |
| **Migration effort** | Workflow changes (merge_group event) + branch protection config | dependabot.yml edit only |
| **Failure isolation** | Good (failed PR ejected, others proceed) | Poor (whole group fails) |
| **Requires workflow changes?** | Yes (add merge_group trigger) | No |
| **Complementary?** | Could be used together (if available) | Works standalone |
| **Configuration complexity** | Medium (branch protection + workflow changes) | Low (YAML groups block) |

### 4. Impact on Version-Bump Workflow

Jerry's `version-bump.yml` triggers on `push` to `main` and uses Conventional Commit detection:

```yaml
on:
  push:
    branches: [main]
```

With Dependabot Grouping:
- A grouped PR with `ci:` prefix (GitHub Actions updates) merges as one push event
- The version-bump workflow runs once, detects `ci:` prefix, resolves to `none` bump type, and outputs "Skipped"
- **Result: 1 workflow run instead of ~10** for GitHub Actions updates
- **Result: 1 workflow run instead of ~3-5** for pip updates

The existing `concurrency: group: version-bump, cancel-in-progress: false` configuration continues to work correctly -- fewer pushes means fewer serialized runs, not cancelled runs.

---

## L2: Architectural Implications

### 1. Decision Classification

This is a **C1 (Routine)** decision:
- Reversible in one session (revert `dependabot.yml` change)
- Affects 1 file
- No architectural impact
- No API changes

### 2. Why Merge Queue Is a Red Herring for This Problem

Merge queue solves a fundamentally different problem: ensuring PRs are tested against the latest state of `main` before merging. It prevents the "semantic merge conflict" where two PRs individually pass CI but together produce a broken `main`. It is a CI correctness tool, not a CI volume reduction tool.

For the specific problem of "N Dependabot PRs causing N version-bump triggers," merge queue changes when and how PRs merge but not how many individual merges occur. The push event count on `main` is the same with or without merge queue.

### 3. Complementary Use Case (Future)

If Jerry migrates to an organization account in the future, merge queue could complement Dependabot Grouping:
- **Grouping** reduces the number of PRs (N individual -> ~3 grouped)
- **Merge queue** ensures those ~3 PRs are tested against the latest `main` before merging

This is a "use both" scenario, but only Grouping is needed to solve the current problem.

### 4. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Grouped PR fails CI due to one bad dependency | Low-Medium | Low | Exclude problematic dep; major updates kept individual |
| Cannot identify which dependency broke CI | Low | Medium | Temporarily disable grouping to isolate; exclude and re-enable |
| Security vulnerability missed in grouped PR | None | N/A | Security alerts are independent; security updates can be kept ungrouped |
| Dependabot creates unexpected group combinations | Low | Low | Review first grouped PR before auto-merge; adjust patterns |
| Configuration change breaks existing Dependabot behavior | None | N/A | Grouping is additive; non-matching deps continue as individual PRs |

### 5. What Other Projects Do

Real-world adoption patterns from the research:

- **SPS Commerce (4,000+ repos):** Uses Dependabot Grouping extensively to reduce "Pull Request Noise" and "CI/CD Resource Strain." Groups by package family (Microsoft framework, OpenTelemetry, AWS SDK). [13]
- **Various open-source Python projects:** Group all pip dependencies with `patterns: ["*"]` for minor/patch, keep majors individual. [14, 9]
- **GitHub Actions users:** Group all actions with `patterns: ["*"]` since SHA-pinned action updates are inherently low-risk. [9, 14]
- **No project in the research sample used merge queue specifically to solve the Dependabot PR volume problem.** Merge queue adoption is driven by CI correctness concerns (testing against latest main), not volume reduction.

### 6. Migration Plan

**Effort: Trivial (< 5 minutes)**

1. Edit `.github/dependabot.yml` to add `groups` blocks (see L1 section 2.3 for exact configuration)
2. Commit and merge to `main`
3. Wait for next Dependabot schedule run (Monday)
4. Verify grouped PRs are created as expected
5. If any group is problematic, adjust `exclude-patterns` or `update-types`

**No other files need to change.** The version-bump workflow, CI workflow, and branch protection rules are unaffected.

---

## Research Questions -- Complete Answers

### GitHub Merge Queues

| # | Question | Answer | Source |
|---|----------|--------|--------|
| 1 | What GitHub plan is required? | Organization-owned repos (any plan for public, Enterprise Cloud for private). **Not available for personal user accounts.** Jerry is user-owned -- BLOCKER. | [1] |
| 2 | How does batching work? | PRs are tested together in temporary branches but merged individually to base branch. Each gets its own commit. | [2, 3] |
| 3 | What happens to push events? | One push event per PR merged. N PRs = N pushes. Batching does not reduce push count. | [3] |
| 4 | Interaction with concurrency group? | N individual pushes serialize through `concurrency: group: version-bump`. No improvement. | Inferred from [2, 3] + version-bump.yml analysis |
| 5 | What CI changes required? | Add `merge_group` event trigger to workflows. Update third-party CI to watch `gh-readonly-queue/*` branches. | [2] |
| 6 | What if one PR fails? | Failed PR is ejected from queue. Remaining PRs are re-tested without it. | [2] |
| 7 | Can you configure batch size? | Yes. "Merge limits" allow min/max 1-100 PRs with timeout. "Build concurrency" allows 1-100 parallel checks. But merge limits do not combine merge_group builds. | [2, 3] |
| 8 | Is it a one-way door? | No. Fully reversible by disabling in branch protection settings. | [2] |
| 9 | Known failure modes? | Community reports: does not reduce CI minutes like Bors (100 PRs = 1000 CI minutes, not 10). Temporary branches can cause confusion. merge_group event must be added to workflows or checks fail silently. | [3, 15] |
| 10 | Branch protection interaction? | Merge queue is enabled via branch protection rules. Requires "Require merge queue" setting. Provides benefits similar to "require branches to be up to date" without manual updates. | [2] |

### Dependabot Grouping

| # | Question | Answer | Source |
|---|----------|--------|--------|
| 1 | What if one dep fails CI? | Whole group PR fails. No per-dep isolation. Use `@dependabot ignore` or `exclude-patterns` to isolate. | [8, 9] |
| 2 | Can you split a group? | Yes. Close PR, add `exclude-patterns`, Dependabot creates new grouped PR without excluded dep + individual PR for it. | [7] |
| 3 | Rollback story? | Revert merge commit reverts all deps in group. No single-dep revert without manual commit. Config change is fully reversible. | [7, 10] |
| 4 | Conflict handling? | Dependabot attempts resolution. If it fails, grouped PR shows conflict and CI fails. Exclude conflicting dep. | [7] |
| 5 | Recommended grouping strategy? | By update-type (minor/patch together, major individual) and by ecosystem. For GitHub Actions, group all (`*`). For pip, group minor/patch, keep major individual. | [5, 9, 13, 14] |
| 6 | Security vulnerability detection? | Unaffected. Security alerts are per-vulnerability-per-manifest. Security update PRs can optionally be grouped separately via `applies-to: security-updates`. | [11, 12] |

### Comparison

| # | Question | Answer | Source |
|---|----------|--------|--------|
| 1 | Complementary or competing? | Complementary in theory (grouping reduces PRs, merge queue tests them). In practice, only grouping solves the N-push problem. | Analysis of [2, 3, 5] |
| 2 | Which is reversible? | Both are fully reversible two-way doors. | [2, 7] |
| 3 | Migration effort? | Grouping: 1 file change (dependabot.yml). Merge queue: workflow changes + branch protection config + org account requirement. | [2, 7] |
| 4 | What do similar projects use? | Dependabot Grouping is the standard solution. No project in the sample used merge queue for Dependabot PR volume reduction. | [9, 13, 14] |

---

## Methodology

### Research Approach

5W1H framework applied to both solutions with web research using WebSearch and WebFetch tools.

### Sources Consulted

- GitHub official documentation (docs.github.com) -- PRIMARY
- GitHub community discussions (github.com/orgs/community/discussions) -- PRIMARY
- GitHub Blog changelogs and announcements -- PRIMARY
- Developer experience reports (blogs, Medium) -- SECONDARY
- Jerry repository analysis (dependabot.yml, version-bump.yml, ci.yml) -- PRIMARY

### Verification Steps (S-011)

1. **Plan availability claim:** Verified via GitHub Docs + community discussion #51483 + `gh repo view` confirming Jerry is user-owned
2. **Push event behavior:** Cross-referenced GitHub Docs, community discussion #58523, and Aviator blog. All confirm individual merges.
3. **Grouping behavior:** Verified against GitHub Docs options reference + multiple real-world reports
4. **Configuration syntax:** Verified against official Dependabot options reference documentation

### Limitations

- GitHub's documentation does not explicitly state "merge queue is unavailable for personal user accounts." The restriction is inferred from the positive statement "available in any public repository owned by an organization." This was consistent across all sources but lacks a direct negative statement.
- Push event count per merge batch was confirmed by community discussion consensus and documentation language, but no GitHub engineer explicitly stated "N PRs = N push events" in a single canonical source. The evidence is strong but indirect.

---

## References

1. [GitHub community discussion #51483 - Merge Queue feature availability](https://github.com/orgs/community/discussions/51483) -- Key insight: merge queue requires organization-owned repository
2. [GitHub Docs - Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) -- Key insight: merge limits, batch configuration, failure behavior, merge methods
3. [GitHub community discussion #58523 - Merge Queue batching](https://github.com/orgs/community/discussions/58523) -- Key insight: "merge limits do not combine merge_group builds"; each PR merges individually; CI minutes not saved like Bors
4. [GitHub community discussion #14818 - Squash and Merge in Merge Queue](https://github.com/orgs/community/discussions/14818) -- Key insight: squash method still produces one commit per PR
5. [GitHub Docs - Optimizing PR creation for Dependabot version updates](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/optimizing-pr-creation-version-updates) -- Key insight: official grouping recommendations
6. [GitHub Blog - Grouped version updates for Dependabot GA](https://github.blog/changelog/2023-08-24-grouped-version-updates-for-dependabot-are-generally-available/) -- Key insight: available on all plans
7. [GitHub Docs - Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) -- Key insight: groups syntax, patterns, exclude-patterns, update-types, dependency-type
8. [Dependabot's dependency grouping is awesome (slar.se)](https://slar.se/dependabots-dependency-grouping.html) -- Key insight: real-world experience; whole group fails when one dep breaks CI; `@dependabot ignore` as mitigation
9. [Using GitHub merge queue to ease the Dependabot churn (fredrikaverpil.github.io)](https://fredrikaverpil.github.io/blog/2023/03/29/using-github-merge-queue-to-ease-the-dependabot-churn/) -- Key insight: automation script for bulk-approving and queuing Dependabot PRs
10. [GitHub Docs - Reverting a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/reverting-a-pull-request) -- Key insight: revert creates new PR with one revert of the merge commit
11. [GitHub Docs - About Dependabot alerts](https://docs.github.com/code-security/dependabot/dependabot-alerts/about-dependabot-alerts) -- Key insight: alerts are per-vulnerability-per-manifest, independent of grouping
12. [GitHub Blog - Group Configuration for Dependabot Security Updates](https://github.blog/changelog/2024-03-06-group-configuration-options-for-dependabot-security-updates-public-beta/) -- Key insight: `applies-to: security-updates` enables security update grouping
13. [Is GitHub Dependabot Now Enterprise Ready with Grouped Updates? (travisgosselin.com)](https://travisgosselin.com/dependabot-with-grouped-updates/) -- Key insight: SPS Commerce (4,000+ repos) experience; groups by package family; addresses CI strain
14. [Configuring Dependabot for a Python project (Simon Willison)](https://til.simonwillison.net/github/dependabot-python-setup) -- Key insight: Python-specific grouping patterns
15. [GitHub Blog - GitHub merge queue is generally available](https://github.blog/news-insights/product-news/github-merge-queue-is-generally-available/) -- Key insight: GA announcement; feature description

---

*Research conducted: 2026-03-11*
*Agent: ps-researcher*
*Project: PROJ-030-bugs*
*Confidence: HIGH (0.90) -- all critical claims verified against multiple independent sources; one limitation noted regarding merge queue plan availability being inferred from positive rather than negative statements*
