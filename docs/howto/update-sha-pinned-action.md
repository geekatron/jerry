# How to Update a SHA-Pinned GitHub Action

> Update a GitHub Actions SHA pin when Dependabot opens a PR or you need to manually advance an action to a new release.

## Before You Begin

You need:
- Write access to the `geekatron/jerry` repository
- `git` and `gh` CLI installed and authenticated
- The [SHA-to-version mapping table](../reference/ci-cd-pipeline-security.md#sha-pinning) open for reference

---

## Scenario A: Dependabot Has Opened a PR

### 1. Open the Dependabot PR

In the PR, review the diff. Dependabot updates both the SHA and the inline version comment in every workflow file where the action appears. Verify:

- The `uses:` line changed from the old SHA to a new SHA
- The trailing comment changed from the old version to the new version (e.g., `# v5.0.0` -> `# v5.1.0`)
- Every workflow file listed in the [Workflows where SHA-pinned actions appear](../reference/ci-cd-pipeline-security.md#sha-pinning) table for this action is included in the diff

If Dependabot updated only some workflow files but the table shows more, proceed to [Scenario B, Step 3](#3-find-the-commit-sha-for-the-new-release) to complete the remaining files manually.

### 2. Check the action's release on GitHub

Navigate to the action's GitHub releases page (e.g., `https://github.com/actions/checkout/releases`) and confirm the new tag exists and corresponds to the SHA in the PR diff.

### 3. Merge and update the reference document

If the diff is correct and CI passes, merge the PR.

Dependabot PRs do not update `docs/reference/ci-cd-pipeline-security.md`. After merging, update the SHA-to-version mapping table in the reference doc with the new SHA and version — follow [Scenario B, Step 5](#5-update-the-sha-to-version-mapping-table) as a post-merge commit.

If CI fails, check the [Verification](#verification) section below.

---

## Scenario B: Manual Update

### 1. Identify which workflows need updating

Open the [Workflows where SHA-pinned actions appear](../reference/ci-cd-pipeline-security.md#sha-pinning) table. Note every workflow file that lists "Yes" for the action you are updating.

### 2. Identify the current SHA and version

Open the [SHA-to-version mapping table](../reference/ci-cd-pipeline-security.md#sha-pinning) and record the current SHA and version for the action.

### 3. Find the commit SHA for the new release

On the action's GitHub releases page, open the release you want to pin to (e.g., `https://github.com/actions/checkout/releases/tag/v5.1.0`).

Copy the full commit SHA that the release tag points to:

```bash
# Resolve a release tag to its commit SHA
git ls-remote https://github.com/actions/checkout.git refs/tags/v5.1.0
```

The output looks like:

```
abc123def456...   refs/tags/v5.1.0
```

If `git ls-remote` returns two lines — one for `refs/tags/v5.1.0` and one for `refs/tags/v5.1.0^{}` — the tag is annotated. Use the SHA from the `^{}` line (the dereferenced commit SHA):

```bash
git ls-remote https://github.com/actions/checkout.git refs/tags/v5.1.0^{}
```

If only one line is returned (no `^{}` line), the tag is lightweight and the SHA is already the commit. Use it directly.

### 4. Update every workflow file

For each workflow file identified in Step 1, replace the old SHA and version comment. The pattern is:

```yaml
# Before
- uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8 # v5.0.0

# After
- uses: actions/checkout@<new-sha> # v5.1.0
```

Use search-and-replace across all affected files to avoid missing an occurrence. Every `uses:` line for this action must be updated — the same action may appear in multiple jobs within one workflow file.

If you are updating `actions/checkout` as an example, the affected files are `ci.yml`, `version-bump.yml`, `release.yml`, and `docs.yml`.

### 5. Update the SHA-to-version mapping table

Open `docs/reference/ci-cd-pipeline-security.md` and update the SHA-to-version mapping table under the [SHA Pinning](../reference/ci-cd-pipeline-security.md#sha-pinning) section:

```markdown
| `actions/checkout` | <new-sha> | v5.1.0 |
```

Replace both the SHA and the version string for the action row.

### 6. Commit and push

```bash
git add .github/workflows/ docs/reference/ci-cd-pipeline-security.md
git commit -m "ci: pin actions/checkout to v5.1.0 (<new-sha>)"
git push
```

---

## Verification

After merging (Scenario A) or pushing (Scenario B), confirm CI passes:

```bash
gh run list --branch main --limit 5
```

Open the failing run if any job is red:

```bash
gh run view <run-id> --log-failed
```

If a job fails with an error like `uses: actions/checkout@<sha> is not a valid SHA`, the SHA was copied incorrectly. Re-run [Step 3](#3-find-the-commit-sha-for-the-new-release) and verify you used the dereferenced commit SHA, not the tag object SHA.

To confirm an action resolved to the expected version during a run, open the run's job log and look for the action's own startup output, which typically prints the action version.

---

## Troubleshooting

**Problem:** Dependabot updated only one workflow file but the action appears in several.
**Solution:** Manually apply the new SHA to the remaining workflow files following [Scenario B, Steps 4-5](#4-update-every-workflow-file). Then push a fixup commit before merging the Dependabot PR, or merge it and follow up immediately.

**Problem:** `git ls-remote` returns two lines for a tag (one without `^{}` and one with).
**Solution:** Use the SHA from the line ending in `^{}`. That is the commit SHA. The other line is the annotated tag object SHA, which GitHub Actions will reject.

**Problem:** CI fails on the `changelog-check` job after a Dependabot merge.
**Solution:** Dependabot PRs are exempt from the changelog requirement. If you manually pushed the update, add a `[skip-changelog]` marker to the PR title or add a `CHANGELOG.md` entry under `[Unreleased]`.

---

## Related

- **Reference:** [CI/CD Pipeline Security Controls](../reference/ci-cd-pipeline-security.md#sha-pinning) — SHA-to-version mapping table and workflow matrix
- **Explanation:** [About the Jerry CI/CD Supply Chain Security Model](../explanation/ci-cd-supply-chain-security.md) — Why SHA pinning is used and how the pipeline security model is designed
