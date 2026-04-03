# GitHub Actions Workflow Filtering Research

> Research on path filters, commit message conditions, and their interactions for version-bump.yml dual filtering (Issue #187).

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Non-technical overview of findings |
| [L1: Technical Analysis](#l1-technical-analysis) | Detailed syntax, examples, and edge cases |
| [L2: Architectural Implications](#l2-architectural-implications) | Trade-offs, risks, and recommended approach |
| [Research Questions](#research-questions) | Numbered answers to all 13 questions |
| [Methodology](#methodology) | Sources consulted and search approach |
| [References](#references) | Complete citation list |

---

## L0: Executive Summary

We researched how to add dual filtering to `version-bump.yml` so it only runs when commits could actually produce a version bump, skipping documentation-only or CI-config-only changes.

**Key findings:**

1. **Path filters work but have a critical interaction with branch protection.** Adding `paths:` or `paths-ignore:` to the push trigger will prevent the workflow from running when only excluded files change. However, if `version-bump.yml` is ever made a required status check, skipped workflows remain in "Pending" state and block merges. Since version-bump is NOT currently a required check (it only runs on push to main, not on PRs), this is not a concern for this specific workflow.

2. **Commit message filtering must use job-level `if:` conditions, not trigger-level syntax.** GitHub Actions has no `on.push.commit_message:` filter. The existing `if:` condition on the `bump` job already uses `github.event.head_commit.message` and this is the correct pattern. The `startsWith()` and `contains()` functions are available and case-insensitive.

3. **Path filters do NOT apply to `workflow_dispatch`.** This is exactly what we want -- manual triggers should always work regardless of which files changed. Each trigger event (`push`, `workflow_dispatch`) is evaluated independently.

4. **There is a known edge case with squash merges and path filters** where the squash commit message may accidentally contain `[skip ci]` from individual commit messages, causing GitHub's built-in skip mechanism to suppress the workflow entirely. This is configurable in repository settings.

**Recommendation:** Use `paths-ignore:` on the push trigger to exclude documentation, test, and workflow files. Keep commit message filtering at the job-level `if:` condition (which already exists). This gives maximum filtering with minimal risk.

---

## L1: Technical Analysis

### Path Filter Syntax

GitHub Actions supports two mutually exclusive approaches for path filtering on `push` events. You cannot use both `paths:` and `paths-ignore:` on the same event [1, 2].

**Option A -- `paths:` (allowlist):** Only trigger when specified paths change.

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'pyproject.toml'
      - '.claude-plugin/**'
```

**Option B -- `paths-ignore:` (denylist):** Trigger unless ONLY excluded paths change.

```yaml
on:
  push:
    branches: [main]
    paths-ignore:
      - '.github/workflows/**'
      - 'docs/**'
      - 'tests/**'
      - 'requirements-*.txt'
      - '*.md'
      - '!CHANGELOG.md'  # Exception: CHANGELOG.md changes may accompany version-relevant changes
```

**Negation with `!` prefix:** Within `paths:`, you can use `!` to exclude specific patterns after including broader ones. A `!` pattern after a positive match excludes that path. A positive pattern after a `!` re-includes it. Order matters. You must have at least one non-negated pattern if using `!` [2].

```yaml
on:
  push:
    paths:
      - 'src/**'
      - '!src/**/*.test.py'  # Exclude test files within src
```

### Combining `paths` with `branches`

When both `branches:` and `paths:` (or their `-ignore` variants) are specified, they combine as a logical AND -- both conditions must be satisfied for the workflow to trigger [1, 2].

```yaml
on:
  push:
    branches: [main]       # Must be push to main
    paths:                  # AND must change these paths
      - 'src/**'
```

This is the exact behavior we want: only run on pushes to main that touch version-relevant files.

### `workflow_dispatch` and Path Filters

Path filters are specified per event type. The `workflow_dispatch` event does not support `paths:` or `paths-ignore:`. Each trigger in the `on:` block is evaluated independently. Adding `paths-ignore:` to `push:` has no effect on `workflow_dispatch:` -- manual triggers always fire regardless of file changes [3, 4].

```yaml
on:
  push:
    branches: [main]
    paths-ignore:          # Only applies to push events
      - 'docs/**'
  workflow_dispatch:       # Always fires; path filters do not apply here
    inputs:
      bump_type: ...
```

**Source:** GitHub official documentation confirms path filtering is scoped to the event type [1, 4].

### Commit Message Filtering

GitHub Actions does NOT support commit message filtering in the `on:` trigger block. Commit message conditions must be implemented as job-level `if:` conditions [5, 6].

**Available functions (all case-insensitive) [7]:**

| Function | Syntax | Behavior |
|----------|--------|----------|
| `contains()` | `contains(string, substring)` | Returns true if string contains substring |
| `startsWith()` | `startsWith(string, prefix)` | Returns true if string starts with prefix |
| `endsWith()` | `endsWith(string, suffix)` | Returns true if string ends with suffix |

**Current version-bump.yml already uses this pattern correctly:**

```yaml
jobs:
  bump:
    if: >-
      !contains(github.event.head_commit.message, '[skip-bump]') &&
      github.actor != 'github-actions[bot]'
```

**To add prefix-based filtering for conventional commit types:**

```yaml
jobs:
  bump:
    if: >-
      (
        github.event_name == 'workflow_dispatch' &&
        !contains(github.event.head_commit.message, '[skip-bump]')
      ) ||
      (
        github.event_name != 'workflow_dispatch' &&
        !contains(github.event.head_commit.message, '[skip-bump]') &&
        github.actor != 'github-actions[bot]' &&
        !startsWith(github.event.head_commit.message, 'ci:') &&
        !startsWith(github.event.head_commit.message, 'ci(') &&
        !startsWith(github.event.head_commit.message, 'docs:') &&
        !startsWith(github.event.head_commit.message, 'docs(') &&
        !startsWith(github.event.head_commit.message, 'style:') &&
        !startsWith(github.event.head_commit.message, 'style(') &&
        !startsWith(github.event.head_commit.message, 'test:') &&
        !startsWith(github.event.head_commit.message, 'test(') &&
        !startsWith(github.event.head_commit.message, 'chore:') &&
        !startsWith(github.event.head_commit.message, 'chore(') &&
        !startsWith(github.event.head_commit.message, 'refactor:') &&
        !startsWith(github.event.head_commit.message, 'refactor(') &&
        !startsWith(github.event.head_commit.message, 'build:') &&
        !startsWith(github.event.head_commit.message, 'build(')
      )
```

**Important note on `startsWith()` case insensitivity [7]:** The `startsWith()` function is NOT case-sensitive per GitHub documentation. This means `startsWith(msg, 'ci:')` will match `CI:`, `Ci:`, and `ci:`. This aligns with the existing BUG-002 fix for case-insensitive conventional commit detection.

### `head_commit.message` Behavior

The `github.event.head_commit.message` field contains the **full commit message** including subject line and body, not just the first line [8, 9]. For push events, `head_commit` is the most recent (tip) commit in the push. Key behaviors:

- **Regular commits:** Contains the full git commit message (subject + body, separated by blank line)
- **Merge commits:** Contains the merge commit message, typically "Merge pull request #N from branch/name" followed by the PR description
- **Squash merges:** Contains the squash commit message, which by default includes the PR title and a list of squashed commit messages (configurable in repository settings)
- **Multi-line messages:** The full message including body is available. `startsWith()` only checks the beginning, so it effectively checks the subject line. `contains()` searches the entire message including body.
- **Null handling:** If `head_commit` is null (rare edge case), the expression evaluates falsy. The `!startsWith(null, 'ci:')` returns true (safe -- workflow runs) [7].

**Squash merge gotcha [10]:** When a PR is squash-merged, GitHub's default behavior may include individual commit messages in the squash commit body. If any individual commit message contained `[skip ci]` or `[skip actions]`, the built-in GitHub Actions skip mechanism may suppress the entire workflow. This is separate from custom `if:` conditions and is controlled by repository settings under Settings > General > Pull Requests > Default commit message.

### Built-in Skip Mechanism

GitHub Actions has a built-in mechanism that skips workflows when the commit message contains [11]:
- `[skip ci]`, `[ci skip]`, `[no ci]`, `[skip actions]`, `[actions skip]`

This applies to `push` and `pull_request` events only. This is evaluated BEFORE path filters and job-level `if:` conditions. It causes the entire workflow to be skipped (not just individual jobs), and skipped workflows remain in "Pending" state for branch protection purposes.

The version-bump workflow already guards against its own commits via `github.actor != 'github-actions[bot]'` and `[skip-bump]`. But be aware that a `[skip ci]` in any commit message pushed to main would prevent the version bump from running.

### Interaction: Path Filters + Job-Level `if:`

When both are used:

1. **Path filter evaluates first** (trigger level). If the path filter prevents the workflow from triggering, no jobs run at all.
2. **Job-level `if:` evaluates second.** If the workflow triggers (path filter passed), then each job's `if:` condition is evaluated independently.
3. **They stack as AND.** Both the path filter AND the job-level condition must be satisfied for the job to execute.

This means path filters provide the "coarse" filter (did version-relevant files change?) and the job-level `if:` provides the "fine" filter (is this a bump-worthy commit type?).

### Workflow-Skipped vs Job-Skipped: Branch Protection Impact

This distinction is critical for understanding the impact on `ci-success` and branch protection [12, 13]:

| Skip Type | Cause | Status | Branch Protection Impact |
|-----------|-------|--------|--------------------------|
| **Workflow skipped** | Path filter, branch filter, or `[skip ci]` in commit message | Remains "Pending" | **Blocks merge** if workflow is a required check |
| **Job skipped** | Job-level `if:` condition evaluates false | Reports "Success" | **Does not block merge** -- treated as passing |

**For version-bump.yml specifically:** This workflow is NOT a required status check. It runs on `push` to `main` (post-merge), not on PRs. The `ci-success` gate in `ci.yml` does not depend on version-bump. Therefore, whether the workflow is skipped or not has zero impact on PR merging. This makes path filtering safe to add.

### 300-File Diff Limit

GitHub compares changed files against the first 300 files returned by the filter [2]. If there are more than 300 changed files in a push and the matching files are not in the first 300 returned, the workflow will not run. Exception: if more than 1,000 commits are pushed or GitHub times out generating the diff, the workflow always runs regardless of path filters.

For the Jerry repository, individual merge commits are unlikely to exceed 300 changed files, so this is not a practical concern.

---

## L2: Architectural Implications

### Approach Comparison

| Approach | Filtering Power | Complexity | Risk | Branch Protection Safe |
|----------|----------------|------------|------|----------------------|
| **A: `paths-ignore:` only** | Moderate -- filters file-only changes | Low | Low | Yes (version-bump is not required check) |
| **B: Commit message `if:` only** | Moderate -- filters by commit type | Low | Low -- already partially in place | Yes (job-level skip = "Success") |
| **C: Both `paths-ignore:` + commit message `if:`** | High -- dual filtering | Medium | Low | Yes |
| **D: `dorny/paths-filter` action** | High -- per-job path conditions | Higher -- adds dependency | Medium -- supply chain risk | Yes (job-level skip) |

### Recommended Approach: C (Dual Filtering)

Use `paths-ignore:` at the trigger level AND commit message `startsWith()` checks at the job level. This provides defense-in-depth:

1. **Path filter catches** documentation-only, test-only, and workflow-only pushes (prevents the workflow from even starting)
2. **Commit message filter catches** conventional commit types that never produce version bumps (skips the job gracefully)

### Recommended `paths-ignore:` Configuration

```yaml
on:
  push:
    branches: [main]
    paths-ignore:
      - '.github/workflows/**'
      - '!.github/workflows/version-bump.yml'  # Changes to version-bump.yml itself SHOULD trigger
      - 'docs/**'
      - 'tests/**'
      - 'requirements-*.txt'
      - '*.md'
      - '!pyproject.toml'   # NOT ignored -- version lives here
      - '.context/**'
      - 'projects/**'
      - 'skills/**'
      - '.claude/**'
```

**Important design decision:** Should changes to `version-bump.yml` itself trigger the workflow? Arguments both ways:
- **Yes (include):** If someone changes the workflow logic, it should run to validate the changes. But on push to main, it runs the NEW code anyway.
- **No (exclude):** CI-only changes should not trigger a version bump. The workflow will detect "none" bump type anyway.

Recommendation: Exclude `.github/workflows/**` (the bump detection step will return "none" for CI-only commits regardless). Simpler exclusion with no functional impact.

### Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|------------|
| Squash merge includes `[skip ci]` from individual commits, suppressing version bump | Medium | Low (requires deliberate use in commit messages) | Configure repository: Settings > Pull Requests > Default commit message = "Pull request title" |
| Path filter prevents bump after mixed commit (src/ + docs/) | None | N/A | Path filter triggers if ANY changed file is outside the ignore list. A commit touching both `src/` and `docs/` will trigger the workflow. |
| `startsWith()` is case-insensitive, might match unintended prefixes | Low | Very Low | Conventional commit prefixes are well-defined; case insensitivity is a feature, not a bug (aligns with BUG-002 fix). |
| Future addition of version-bump as required check breaks path filtering | Medium | Low | Document in workflow comments that adding this to required checks requires the "Merge OK" gate pattern. |
| `head_commit.message` is null for some edge cases | Low | Very Low | `!startsWith(null, 'ci:')` returns `true` -- safe default (workflow runs). |

### Interaction with Existing `if:` Condition

The current `bump` job already has a complex `if:` condition handling `workflow_dispatch` vs push events, `[skip-bump]`, and bot detection. The commit prefix filtering should be added to the existing push-event branch of the condition, not as a separate mechanism.

### What NOT to Do

1. **Do not add `paths:` (allowlist) instead of `paths-ignore:`.** The repository has too many version-relevant directories to enumerate. An allowlist would require updating every time a new source directory is added. `paths-ignore:` is the correct choice because the set of irrelevant paths is smaller and more stable.

2. **Do not use `dorny/paths-filter` action.** This adds an external dependency with supply chain risk. The built-in `paths-ignore:` is sufficient for the version-bump use case since there is no branch protection concern.

3. **Do not put commit message filtering in a separate early job.** The existing `bump` job's `if:` condition is the correct location. Adding a separate gating job would waste a runner allocation for a simple string check.

---

## Research Questions

### Path Filters

**Q1: What is the exact syntax for `paths:` and `paths-ignore:` on push triggers? Which is better for our use case?**

Both syntaxes are documented in [1, 2]. `paths:` is an allowlist (only trigger when listed paths change). `paths-ignore:` is a denylist (trigger unless only listed paths change). They cannot be combined on the same event. For version-bump.yml, `paths-ignore:` is better because the set of "irrelevant" paths (docs, tests, workflows, markdown) is smaller and more stable than the set of "version-relevant" paths. See L1 section for full syntax.

**Q2: Do path filters work with `workflow_dispatch`?**

No. Path filters are scoped to the event type they are declared under. `workflow_dispatch` does not support `paths:` or `paths-ignore:`. Manual triggers always fire. Each event type in the `on:` block is evaluated independently [1, 3, 4]. This is exactly what we want.

**Q3: If a merge commit changes both `src/` and `.github/workflows/`, does the path filter trigger or not?**

Yes, it triggers. With `paths-ignore:`, the workflow only skips if ALL changed files match the ignore patterns. If even one file falls outside the ignore list (e.g., a file in `src/`), the workflow runs [1, 2].

**Q4: What happens with path filters on squash merges vs merge commits?**

There is a known issue where squash merges may not trigger path-filtered workflows reliably [10]. The root cause in most reported cases is that squash commits inherit `[skip ci]` or `[skip actions]` keywords from individual commit messages in the squash body, triggering GitHub's built-in skip mechanism. This is configurable via repository settings (default commit message format). For regular merge commits and rebase merges, path filters work correctly based on the file diff.

**Q5: Can you combine `paths:` with `branches:` on the same trigger?**

Yes. When both `branches:` and `paths:` (or their `-ignore` variants) are specified on the same trigger, they combine as a logical AND. Both conditions must be satisfied [1, 2]. Example: `push: branches: [main] + paths-ignore: ['docs/**']` means "trigger on push to main that changes at least one file outside docs/".

### Commit Message Filtering

**Q6: Can you filter on commit message in the `on:` block, or does it have to be a job-level `if:` condition?**

It must be a job-level `if:` condition. GitHub Actions does not support commit message filtering in the `on:` trigger block. The only built-in commit-message-based mechanism at the trigger level is the automatic `[skip ci]` / `[skip actions]` detection [5, 6, 11].

**Q7: What's the correct syntax for `github.event.head_commit.message` in an `if:` condition?**

```yaml
jobs:
  my-job:
    if: ${{ !startsWith(github.event.head_commit.message, 'docs:') }}
```

Or without the `${{ }}` wrapper (GitHub auto-wraps `if:` values in expression syntax) [7]:

```yaml
    if: "!startsWith(github.event.head_commit.message, 'docs:')"
```

Both forms are valid. The `${{ }}` form is more explicit.

**Q8: Does `head_commit.message` work correctly for merge commits?**

Yes, but the content differs by merge strategy [8, 9, 10]:
- **Regular merge:** Message is "Merge pull request #N from ..." -- will NOT match conventional commit prefixes like `ci:` or `docs:`, so the version-bump workflow would correctly run.
- **Squash merge:** Message is the PR title (configurable) -- if the PR title follows conventional commits (e.g., "ci: update workflow"), `startsWith()` would correctly match and skip.
- **Rebase merge:** Each commit retains its original message; `head_commit` is the tip commit.

**Q9: Can you use `startsWith()` or `contains()` in workflow `if:` conditions?**

Yes. Both are available as built-in expression functions. They are case-insensitive. You can also use `endsWith()`. Logical operators `&&`, `||`, and `!` are supported for combining conditions [7].

**Q10: What about multi-line commit messages -- does `head_commit.message` include the body?**

Yes, `head_commit.message` contains the full commit message including subject and body [8, 9]. `startsWith()` checks from the beginning of the string, so it effectively checks only the subject line (first line). `contains()` searches the entire message including the body. For conventional commit prefix matching, `startsWith()` is the correct function.

### Interactions

**Q11: Do path filters and job-level `if:` conditions stack (both must be true)?**

Yes. Path filters evaluate first at the trigger level. If the path filter prevents the workflow from triggering, no jobs run. If the workflow triggers, each job's `if:` is then evaluated independently. The effective behavior is AND: both the path filter must pass AND the job `if:` must pass for the job to run [1].

**Q12: If a path filter prevents the workflow from running, does the `ci-success` gate treat it as "skipped" or "not run"? Does this affect branch protection?**

When a workflow is skipped due to path filtering, its associated checks remain in "Pending" state [12, 13]. If that workflow were a required status check, it would block PR merging. However, version-bump.yml runs on `push` to `main` (post-merge), NOT on PRs. The `ci-success` job in `ci.yml` does not list version-bump as a dependency. Therefore, path filtering on version-bump has zero impact on PR merging or branch protection.

**Separately:** If a **job** is skipped due to a job-level `if:` condition, it reports its status as "Success" [12, 13]. This distinction (workflow skip = "Pending", job skip = "Success") is important for workflows that ARE required checks, but is not relevant for version-bump.

**Q13: What happens to queued `workflow_dispatch` if path filters are added -- does the manual trigger bypass path filters?**

Yes, manual triggers bypass path filters entirely. `paths:` and `paths-ignore:` are properties of specific event types (`push`, `pull_request`). They are not global workflow filters. `workflow_dispatch` has its own configuration (inputs, branches) that is completely independent of path filters on other events [1, 3, 4].

---

## Methodology

### Sources Consulted

1. GitHub official documentation (docs.github.com) -- workflow syntax, expressions, events, skipping runs
2. GitHub Community Discussions -- edge cases with path filters, squash merges, branch protection
3. Pantsbuild blog -- detailed analysis of workflow skip vs job skip distinction
4. DEV Community and Monadical -- practical guides on commit message filtering
5. Existing codebase -- version-bump.yml, ci.yml current implementations

### Search Strategy

- WebSearch for GitHub Actions documentation on path filters, commit message conditions, workflow_dispatch interaction
- WebFetch of official GitHub docs pages for exact syntax and behavioral guarantees
- WebSearch for known edge cases (squash merges, branch protection, 300-file limit)
- Direct code review of existing version-bump.yml and ci.yml to understand current architecture

### Verification

- Cross-referenced official GitHub documentation against community reports for consistency
- Verified `startsWith()` case-insensitivity claim against official expressions documentation
- Confirmed `workflow_dispatch` path-filter independence from multiple sources
- Verified branch protection impact by checking that version-bump is not a required check in ci.yml

---

## References

1. [Workflow syntax for GitHub Actions - GitHub Docs](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions) - Key insight: `paths` and `paths-ignore` syntax, mutual exclusivity, combination with `branches`
2. [Triggering a workflow - GitHub Docs](https://docs.github.com/actions/using-workflows/triggering-a-workflow) - Key insight: path filter evaluation, 300-file diff limit
3. [Events that trigger workflows - GitHub Docs](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows) - Key insight: `workflow_dispatch` has no path filter support; events are independent
4. [GitHub Actions Triggers: 5 Ways to Trigger a Workflow](https://codefresh.io/learn/github-actions/github-actions-triggers-5-ways-to-trigger-a-workflow-with-code/) - Key insight: path filters do not apply to workflow_dispatch
5. [Conditional GitHub action based on commit message - DEV Community](https://dev.to/mliakos/conditional-github-action-based-on-commit-message-2l02) - Key insight: `contains()` and `!` negation syntax for commit message filtering
6. [Filters with GitHub Actions - Monadical](https://monadical.com/posts/filters-github-actions.html) - Key insight: `head_commit.message` unavailable in `pull_request` events; full message content in push events
7. [Evaluate expressions in workflows and actions - GitHub Docs](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions) - Key insight: `startsWith()`, `contains()`, `endsWith()` are case-insensitive; null coercion behavior
8. [Push webhook event payload - GitHub Docs](https://docs.github.com/en/webhooks/webhook-events-and-payloads) - Key insight: `head_commit.message` contains full commit message (subject + body)
9. [Push webhook consistent head_commit - GitHub Changelog](https://github.blog/changelog/2021-10-01-the-push-webhook-payload-provides-a-consistent-head_commit-on-tag-creation/) - Key insight: `head_commit` always present for push events including tag creation
10. [Path filter not triggered on squash merge - GitHub Community Discussion #179965](https://github.com/orgs/community/discussions/179965) - Key insight: squash merge path filter issue often caused by inherited `[skip ci]` in commit body; configurable via repository settings
11. [Skipping workflow runs - GitHub Docs](https://docs.github.com/actions/managing-workflow-runs/skipping-workflow-runs) - Key insight: built-in `[skip ci]` mechanism; affects `push` and `pull_request` only; skipped checks remain "Pending"
12. [Skipping GitHub Actions jobs while keeping branch protection - Pantsbuild](https://www.pantsbuild.org/blog/2022/10/10/skipping-github-actions-jobs-without-breaking-branch-protection) - Key insight: workflow-level skip = "Pending" (blocks); job-level skip = "Success" (passes)
13. [Using conditions to control job execution - GitHub Docs](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-when-your-workflow-runs/using-conditions-to-control-job-execution) - Key insight: skipped jobs report "Success" status; debuggable via condition expression logs
14. [Branch protections with paths-ignore - GitHub Community Discussion #54877](https://github.com/orgs/community/discussions/54877) - Key insight: path-filtered skipped workflows remain "Pending" and block required checks
15. [Required if run feature request - GitHub Community Discussion #13690](https://github.com/orgs/community/discussions/13690) - Key insight: no "required if run" feature; workarounds include gate jobs and inverse workflows
16. [GitHub Actions: Understanding Push and Pull Request Triggers](https://iamachs.com/blog/github-actions/part-4-push-and-pull-request-triggers/) - Key insight: paths and branches combine as AND; mixed-file commits trigger if any file matches

---

*Research conducted: 2026-03-11*
*Agent: ps-researcher*
*Project: PROJ-030-bugs*
*Topic: GitHub Actions workflow filtering for version-bump.yml (#187)*
