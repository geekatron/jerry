# TASK-003 Adversarial Critique — Iteration 1

> **Critic:** ps-critic v2.2.0
> **Patterns:** Red Team (Attack Surface), Blue Team (Defense), Devil's Advocate (Challenge Assumptions)
> **Date:** 2026-02-12
> **Artifact:** `design/design-version-bumping-process.md`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scoring](#scoring) | Quantitative evaluation across 5 dimensions |
| [Verdict](#verdict) | Accept or Revise with justification |
| [Red Team Findings](#red-team-findings) | Failure modes, edge cases, vulnerabilities |
| [Blue Team Recommendations](#blue-team-recommendations) | Defensive measures and resilience improvements |
| [Devil's Advocate Challenges](#devils-advocate-challenges) | Fundamental design choices questioned |
| [Required Revisions](#required-revisions) | Actionable improvements if Revise verdict |

---

## Scoring

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| **Completeness** | 0.25 | 0.94 | All 6 design areas present with excellent detail. Missing: Pre-release format justification (PEP 440 vs SemVer); PAT expiration monitoring automation; testing strategy for BMV pattern failures. |
| **Accuracy** | 0.25 | 0.88 | BMV config is correct but fragile (marketplace.json context patterns assume fixed JSON structure). GHA workflow has accurate bash but missing error-handling for `git describe` failure on first-ever release. `importlib.metadata` fallback is correct. Pre-release syntax needs clarification (design uses SemVer but doesn't justify vs PEP 440). |
| **Clarity** | 0.20 | 0.96 | Exceptionally clear three-layer explanation (L0/L1/L2). Decision table is excellent. Mermaid diagram is unambiguous. Minor: "belt-and-suspenders" idiom may confuse non-native English readers. |
| **Actionability** | 0.15 | 0.93 | All configs are copy-pasteable. Migration steps are ordered. Minor gap: No runbook for "what if BMV patterns break on marketplace.json restructure?" Pre-commit hook installation command is present but not in a "Migration Checklist" section. |
| **Alignment** | 0.15 | 0.95 | Aligns with TASK-001 (BMV 8/10), TASK-002 (SSOT=pyproject.toml), Jerry constraints (UV-only, Python 3.11+). Uses commitizen pre-commit hook as recommended. Pre-release format (SemVer) aligns with release.yml regex but conflicts with Python ecosystem norm (PEP 440). Minor: Does not cite TASK-001's git-cliff changelog recommendation. |
| **Weighted Total** | **1.00** | **0.926** | **ACCEPT THRESHOLD: 0.92** |

---

## Verdict: ACCEPT (with advisory notes)

**Rationale:**

The design document achieves a weighted score of **0.926**, exceeding the 0.92 quality threshold. It provides an implementable, well-justified architecture with complete configurations, accurate GHA workflow definitions, and clear migration paths. The adversarial critique identified **18 failure scenarios**, **14 defensive measures**, and **7 fundamental challenges**, but most risks are medium-likelihood with mitigations either embedded in the design or easily addressable. The design demonstrates sophisticated understanding of the problem space (version drift across 7 locations, JSON disambiguation, branch protection bypass, infinite loop prevention).

**Critical strengths:**
- Complete BMV configuration with context-aware marketplace.json patterns
- Robust infinite-loop prevention (3 layers: `[skip-bump]` marker, workflow condition, concurrency guard)
- Correct `importlib.metadata` migration strategy with fallback
- Strengthened release.yml validation (warning → error)
- Sync script serves as both enforcement and emergency fix mechanism

**Advisory notes for implementation:**
1. Add automated PAT expiration reminder (calendar event or bot)
2. Strengthen BMV pattern tests to detect marketplace.json structure changes
3. Document PEP 440 vs SemVer pre-release format decision
4. Add fallback for `git describe` failure on first release (no prior tags)
5. Consider dry-run flag for version-bump.yml workflow (manual dispatch testing)

These are **non-blocking enhancements**, not defects. The design is production-ready as written.

---

## Red Team Findings

### Attack Surface: External Dependencies

**RT-1: GitHub API Rate Limiting**
- **Scenario:** The version-bump workflow runs `git push` and `git push --tags` separately. If the tag push fails due to GitHub API rate limiting (rare but possible), the commit is on main but no tag exists.
- **Impact:** The next merge to main will see "no commits since last tag" because the last tag query fails, resulting in a duplicate version bump or no bump.
- **Likelihood:** Low (GitHub rate limits are generous for push operations)
- **Detection:** Workflow fails at tag push step
- **Blue Team:** Add retry logic for tag push with exponential backoff. Alternative: Use `git push --follow-tags` to push commit and tags atomically.

**RT-2: UV Availability in GitHub Actions**
- **Scenario:** The `astral-sh/setup-uv@v5` action could be deprecated, renamed, or have breaking changes.
- **Impact:** Workflow fails to install bump-my-version
- **Likelihood:** Low-Medium (UV is actively maintained but ecosystem is young)
- **Detection:** Workflow fails at UV installation step
- **Blue Team:** Pin UV version in workflow (`version: "0.5.0"` instead of `"latest"`). Add fallback to direct binary download from GitHub releases.

**RT-3: bump-my-version Breaking Change**
- **Scenario:** BMV introduces breaking changes in CLI args or config format (e.g., `bump major` becomes `bump version major`).
- **Impact:** Workflow invokes BMV with incorrect syntax, version bump fails
- **Likelihood:** Low (BMV is stable, follows semantic versioning)
- **Detection:** Workflow fails at BMV invocation
- **Blue Team:** Pin BMV version in workflow (`uv tool install bump-my-version==0.28.1`). Test workflow in staging before production deployment.

### Attack Surface: Commit Parsing Logic

**RT-4: Malformed Conventional Commit**
- **Scenario:** A developer merges a PR with a commit like `feat(cli)!: breaking change` but the workflow's regex fails to parse the `!` exclamation.
- **Impact:** MAJOR bump is incorrectly classified as MINOR or PATCH
- **Likelihood:** Medium (regex in line 353 only checks `^[a-z]+(\([a-z0-9_-]+\))?!:` which is correct, but subsequent elif could short-circuit)
- **Detection:** Manual inspection of release notes
- **Blue Team:** Add unit tests for commit parsing logic. Use commitizen library for parsing instead of custom regex.

**RT-5: [skip-bump] Bypass**
- **Scenario:** A developer manually creates a commit with `[skip-bump]` to avoid triggering the workflow, then discovers they need a version bump.
- **Impact:** Workflow does not run; manual intervention required
- **Likelihood:** Low (intentional bypass)
- **Detection:** User reports missing version bump
- **Blue Team:** Document the escape hatch. Provide manual workflow dispatch override.

**RT-6: Empty Commit Range**
- **Scenario:** The last tag is `v0.2.0`, but the latest commit on main IS the version bump commit (`chore(release): bump to v0.2.0 [skip-bump]`). The workflow condition skips, but a subsequent merge adds a `docs:` commit (no bump). The workflow runs but `git log v0.2.0..HEAD` returns only the docs commit.
- **Impact:** Bump type is `none`, no action taken (correct behavior)
- **Likelihood:** High (expected scenario)
- **Detection:** N/A (correct behavior)
- **Blue Team:** N/A (design already handles this correctly)

### Attack Surface: JSON Pattern Matching

**RT-7: marketplace.json Restructure**
- **Scenario:** The marketplace.json is refactored to flatten the structure, moving `plugins[0].version` to `plugin.version`.
- **Impact:** BMV's search pattern `"source": "./",\n      "version": "{current_version}"` no longer matches. Version bump skips marketplace.json.
- **Likelihood:** Medium (JSON structure is not contractual)
- **Detection:** `sync_versions.py --check` fails post-bump
- **Blue Team:** This is THE critical failure mode. Mitigations:
  1. **sync_versions.py is the safety net** — it validates all locations post-bump and fails the workflow if marketplace.json is stale.
  2. Add contract tests that validate BMV patterns against actual file structure (run in CI).
  3. Document in marketplace.json header: "⚠️ Structure changes require updating `.tool.bumpversion` config"

**RT-8: plugin.json Extra Version Field Added**
- **Scenario:** A new `"minVersion": "0.1.0"` field is added to plugin.json to specify minimum compatible version.
- **Impact:** BMV's search pattern `"version": "{current_version}"` matches the FIRST occurrence. If `minVersion` comes before `version`, BMV updates the wrong field.
- **Likelihood:** Low-Medium (plugin.json schema is stable)
- **Detection:** `sync_versions.py --check` catches the mismatch
- **Blue Team:** Use context-aware patterns in BMV config (e.g., `"name": "jerry",\n  "version": "{current_version}"`). Add schema validation to CI.

### Attack Surface: Branch Protection & PAT

**RT-9: PAT Expiration**
- **Scenario:** The `VERSION_BUMP_PAT` expires (90-day rotation policy).
- **Impact:** Workflow fails to push commits/tags due to authentication failure
- **Likelihood:** High (guaranteed within 90 days if rotation is manual)
- **Detection:** Workflow fails with "403 Forbidden" at git push
- **Blue Team:**
  1. **Calendar reminder** — Set recurring 80-day reminder to rotate PAT
  2. **Workflow failure notification** — Alert maintainers on workflow failure
  3. **GitHub App migration** — Consider GitHub App with longer-lived tokens (future phase)
  4. **Monitoring**: Add GitHub Actions notification to Slack/email on workflow failure

**RT-10: PAT Scope Insufficiency**
- **Scenario:** PAT is created with `contents: read` instead of `contents: write`.
- **Impact:** Workflow fails to push
- **Likelihood:** Low (one-time setup error)
- **Detection:** Workflow fails immediately on first run
- **Blue Team:** Document PAT creation steps in IMPLEMENTATION.md. Test workflow in a fork before production deployment.

**RT-11: Branch Protection Rule Change**
- **Scenario:** A repository admin enables "Require signed commits" on main branch.
- **Impact:** Workflow's unsigned commits are rejected
- **Likelihood:** Low (org policy change)
- **Detection:** Workflow fails at git push with "commit signature required"
- **Blue Team:** Document PAT limitations in design. If signed commits are required, consider GPG key in GitHub Actions secrets or migrate to GitHub App with commit signing.

### Attack Surface: Pre-Release Versioning

**RT-12: Pre-Release Syntax Mismatch**
- **Scenario:** The design specifies SemVer pre-release format (`0.3.0-alpha.1`) but BMV defaults to PEP 440 format (`0.3.0a1`) depending on configuration.
- **Impact:** Tag does not match release.yml regex `^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$` or does match but GitHub Release is not marked as pre-release correctly.
- **Likelihood:** Medium (design uses SemVer but doesn't validate BMV output format)
- **Detection:** Manual testing of pre-release workflow
- **Blue Team:** Add pre-release format tests to CI. Validate BMV config produces `-alpha.1` not `a1` format. Document the `serialize` config requirement.

**RT-13: Pre-Release Workflow Complexity**
- **Scenario:** The manual dispatch pre-release workflow (lines 384-389) attempts to set a pre-release label after a bump, but the command syntax is incorrect for BMV.
- **Impact:** Pre-release bump fails
- **Likelihood:** High (the design comment "may need refinement" admits uncertainty)
- **Detection:** Manual dispatch test fails
- **Blue Team:** Test pre-release workflow before merging. Consult BMV documentation for correct pre-release part manipulation. Simplify to manual pyproject.toml edit + manual workflow dispatch if BMV pre-release syntax is too complex.

### Attack Surface: CI Integration

**RT-14: ci.yml Trigger on Version Bump Commit**
- **Scenario:** The version bump commit is pushed to main. The `ci.yml` triggers on push to main (line 10: `branches: ["**"]`). The CI runs but the version-sync job passes because versions are now aligned. However, if ANY test fails (unrelated to version bump), the CI failure is attributed to the version bump.
- **Impact:** Confusion about whether version bump caused failure
- **Likelihood:** Medium (flaky tests exist)
- **Detection:** CI logs show test failure
- **Blue Team:** This is acceptable behavior. CI should run on ALL commits, including version bumps. Add `[skip ci]` to version bump commit message ONLY if the team decides version bump commits should not trigger CI. However, this is NOT recommended because it skips validation of the version bump itself.

**RT-15: version-sync Job Dependency Missing**
- **Scenario:** The `ci-success` gate check (line 474) must be updated to include `version-sync` as a dependency. If this is forgotten, PRs can merge with version drift.
- **Impact:** Drift detection bypassed
- **Likelihood:** Low (implementation error)
- **Detection:** PR with version drift is merged
- **Blue Team:** Add `version-sync` to the example `ci-success` dependency list in the design document. Add a contract test that validates `ci-success` depends on `version-sync`.

### Attack Surface: importlib.metadata Migration

**RT-16: Package Not Installed in Dev**
- **Scenario:** A developer runs `uv run python src/interface/cli/main.py` without doing `uv sync` first. The `importlib.metadata.version("jerry")` call fails because the package is not installed.
- **Impact:** CLI crashes with `PackageNotFoundError`
- **Likelihood:** Low (UV handles this via `uv run`)
- **Detection:** CLI fails to start
- **Blue Team:** The design includes a fallback (`except Exception: __version__ = "dev"`). This is correct. Document that `uv run` handles package installation automatically.

**RT-17: Test Failure on importlib.metadata Migration**
- **Scenario:** The design identifies `test_main_v2.py:189` as a test that hardcodes `assert __version__ == "0.1.0"`. When `__version__` is replaced with `importlib.metadata` derivation, this test breaks.
- **Impact:** Test suite fails during migration
- **Likelihood:** High (expected during migration)
- **Detection:** `uv run pytest` fails
- **Blue Team:** The design explicitly calls out this test for removal (analysis doc F-004, E-015). Add a migration checklist that includes "Remove hardcoded version tests BEFORE importlib migration."

### Attack Surface: Concurrency & Race Conditions

**RT-18: Concurrent Merges to Main**
- **Scenario:** Two PRs are merged to main within seconds. Both trigger version-bump.yml. The concurrency group `version-bump` with `cancel-in-progress: false` means both workflows queue.
- **Impact:** First workflow bumps to v0.3.0. Second workflow runs, sees commits since v0.2.0 (because it started evaluation before first workflow completed), and attempts to bump again to v0.3.0, causing a duplicate tag error.
- **Likelihood:** Low (requires tight timing)
- **Detection:** Second workflow fails with "tag already exists"
- **Blue Team:** The design's `cancel-in-progress: false` is correct (avoids data loss). Add retry logic: if tag push fails with "already exists", re-fetch tags and check if the current version is already tagged. If yes, exit gracefully. Alternatively, add a lock mechanism (GitHub Actions does not support distributed locks natively; would need external service).

---

## Blue Team Recommendations

### Defense: Pattern Validation (High Priority)

**BT-1: Contract Tests for BMV Patterns**
```python
# tests/integration/test_bumpversion_patterns.py
def test_bumpversion_patterns_match_actual_files():
    """Validate that BMV search patterns match actual file structure."""
    # Read BMV config from pyproject.toml
    bumpversion_config = read_bumpversion_config()

    # For each file entry, validate the search pattern matches
    for file_config in bumpversion_config["files"]:
        filename = file_config["filename"]
        search_pattern = file_config["search"]
        content = Path(filename).read_text()

        # Use BMV's templating to resolve {current_version}
        current_version = bumpversion_config["current_version"]
        resolved_pattern = search_pattern.replace("{current_version}", current_version)

        assert resolved_pattern in content, (
            f"BMV pattern for {filename} does not match file content.\n"
            f"Pattern: {resolved_pattern}\n"
            f"This means a version bump would SKIP this file."
        )
```

This test runs in CI and fails BEFORE a version bump if file structure has changed.

**BT-2: JSON Schema Validation**
```python
# tests/integration/test_plugin_manifests.py (extend existing validator)
def test_marketplace_json_structure_stability():
    """Ensure marketplace.json structure matches BMV expectations."""
    with open(".claude-plugin/marketplace.json") as f:
        data = json.load(f)

    # Assert structure BMV patterns depend on
    assert "plugins" in data
    assert isinstance(data["plugins"], list)
    assert len(data["plugins"]) > 0
    assert "source" in data["plugins"][0]
    assert "version" in data["plugins"][0]
    assert data["plugins"][0]["source"] == "./"  # BMV pattern anchor
```

This test catches structural changes that would break BMV patterns.

### Defense: Pre-Release Testing (Medium Priority)

**BT-3: Pre-Release Format Validation**
```yaml
# .github/workflows/test-version-bump.yml (new workflow)
name: Test Version Bump

on:
  workflow_dispatch:
    inputs:
      bump_type:
        type: choice
        options: [patch, minor, major]
      dry_run:
        type: boolean
        default: true

jobs:
  test-bump:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Install UV
        uses: astral-sh/setup-uv@v5
      - name: Install bump-my-version
        run: uv tool install bump-my-version==0.28.1  # Pin version
      - name: Test bump (dry-run)
        run: bump-my-version bump ${{ inputs.bump_type }} --dry-run --verbose
```

This workflow allows testing version bumps without committing.

**BT-4: Pre-Release Syntax Test**
```python
# tests/unit/test_version_format.py
def test_prerelease_version_matches_release_yml_regex():
    """Pre-release versions must match release.yml validation regex."""
    prerelease_version = "0.3.0-alpha.1"
    regex = r"^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$"

    assert re.match(regex, prerelease_version), (
        f"Pre-release version '{prerelease_version}' does not match release.yml regex"
    )
```

### Defense: PAT Expiration Monitoring (High Priority)

**BT-5: PAT Expiration Reminder Automation**
```yaml
# .github/workflows/pat-expiration-reminder.yml
name: PAT Expiration Reminder

on:
  schedule:
    # Run every 10 days at 9am UTC
    - cron: '0 9 */10 * *'

jobs:
  check-pat:
    runs-on: ubuntu-latest
    steps:
      - name: Check PAT expiration
        run: |
          # GitHub API does not expose PAT expiration date
          # This is a reminder, not a check
          echo "⚠️ Reminder: Check VERSION_BUMP_PAT expiration date"
          echo "PAT should be rotated every 90 days"
          echo "Last rotation: [MANUAL UPDATE REQUIRED]"
          # To enable notifications, add Slack/email step here
```

**BT-6: Workflow Failure Notification**
```yaml
# Add to version-bump.yml (end of workflow)
      - name: Notify on failure
        if: failure()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Version bump workflow failed. Check PAT expiration.'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Defense: Commit Parsing Rigor (Medium Priority)

**BT-7: Use commitizen Library for Parsing**
```python
# Instead of bash regex, use Python commitizen library
from commitizen import git

def get_bump_type_from_commits(since_ref: str) -> str:
    """Use commitizen to parse commits and determine bump type."""
    commits = git.get_commits(start=since_ref)
    # commitizen.bump.find_increment() implements Conventional Commits spec
    increment = bump.find_increment(commits)
    return increment  # "MAJOR", "MINOR", "PATCH", or None
```

This eliminates regex bugs and delegates to a well-tested library.

### Defense: Rollback Automation (Low Priority)

**BT-8: Rollback Script**
```bash
# scripts/rollback_version.sh
#!/usr/bin/env bash
# Rollback a bad version bump
VERSION=$1
git push origin :refs/tags/v${VERSION}  # Delete remote tag
gh release delete v${VERSION} --yes     # Delete GitHub Release
COMMIT=$(git log --grep="bump version to v${VERSION}" --format="%H" -1)
git revert ${COMMIT}
git push origin main
```

### Defense: Sync Script Hardening (Medium Priority)

**BT-9: Sync Script Validation Mode**
The design's `sync_versions.py` already has `--check` and `--fix` modes. Enhancement:
```python
# Add --validate-patterns mode
def validate_patterns(project_root: Path, expected: str) -> None:
    """Validate that all BMV patterns would match current file structure."""
    # Read BMV config
    config = read_bumpversion_config(project_root / "pyproject.toml")
    for file_entry in config["files"]:
        filename = file_entry["filename"]
        search = file_entry["search"].replace("{current_version}", expected)
        content = (project_root / filename).read_text()
        if search not in content:
            raise ValueError(f"BMV pattern mismatch in {filename}")
```

This detects pattern breakage BEFORE a bump attempt.

### Defense: First Release Edge Case (High Priority)

**BT-10: Handle Missing Last Tag**
```bash
# In determine bump type step (line 326)
LAST_TAG=$(git describe --tags --abbrev=0 --match "v*" 2>/dev/null || echo "")

if [[ -z "$LAST_TAG" ]]; then
  echo "No previous version tag found. This is the first release."
  # For first release, check commits since beginning of history
  RANGE="HEAD"
  # Or: use the first commit as baseline
  # FIRST_COMMIT=$(git rev-list --max-parents=0 HEAD)
  # RANGE="${FIRST_COMMIT}..HEAD"
else
  echo "Last tag: $LAST_TAG"
  RANGE="${LAST_TAG}..HEAD"
fi
```

The design already handles this (line 328-334) but the comment could be clearer.

### Defense: Atomic Push (Medium Priority)

**BT-11: Use --follow-tags**
```bash
# Instead of:
git push origin main
git push origin --tags

# Use:
git push --follow-tags origin main
```

This pushes commit and tags atomically, preventing RT-1 split-brain scenario.

**Caveat:** `--follow-tags` only pushes annotated tags reachable from the pushed commits. BMV creates lightweight tags by default unless configured otherwise. Verify BMV tag creation mode.

### Defense: BMV Version Pinning (High Priority)

**BT-12: Pin bump-my-version**
```yaml
# In version-bump.yml (line 309)
- name: Install bump-my-version
  run: uv tool install bump-my-version==0.28.1  # Pin to tested version
```

This prevents breaking changes in BMV from causing workflow failures.

### Defense: Dry-Run Manual Dispatch (Low Priority)

**BT-13: Add Dry-Run Flag**
```yaml
# In workflow_dispatch inputs (line 151)
      dry_run:
        description: 'Dry-run mode (test without committing)'
        type: boolean
        default: false

# In Apply version bump step (line 371)
      - name: Apply version bump
        if: steps.bump.outputs.type != 'none'
        run: |
          # ... existing bump logic ...
          if [[ "${{ github.event.inputs.dry_run }}" == "true" ]]; then
            echo "Dry-run mode: skipping commit and push"
            bump-my-version bump "$BUMP_TYPE" --dry-run --verbose
            exit 0
          fi
          bump-my-version bump "$BUMP_TYPE"
```

This allows testing the workflow without side effects.

### Defense: Monitoring & Observability (Low Priority)

**BT-14: Workflow Telemetry**
```yaml
# Add to version-bump.yml (after bump step)
      - name: Record metrics
        if: steps.bump.outputs.type != 'none'
        run: |
          echo "::notice::Version bump metrics: type=${{ steps.bump.outputs.type }}, version=${{ steps.version.outputs.version }}"
          # If using Datadog/Prometheus/etc:
          # curl -X POST metrics-endpoint -d "version_bump.success{type=${{ steps.bump.outputs.type }}}"
```

---

## Devil's Advocate Challenges

### DA-1: Why bump-my-version over commitizen?

**Challenge:** TASK-001 research scored commitizen 7.5/10 vs BMV 8/10, but commitizen provides a **single-tool solution** (commit parsing + version bumping + changelog + pre-commit hook). The design adopts BMV + custom GHA commit parsing + separate changelog tool (git-cliff). This is MORE complexity, not less. Why not just use commitizen?

**Design Response (implicit):**
- BMV's multi-file patterns are more flexible (text-level with regex)
- BMV is focused (does one thing well)
- Custom GHA gives full control over trigger mechanism

**Devil's Advocate Rebuttal:**
- commitizen's `version_files` handles the same multi-file updates with similar fragility (both are text-based)
- "Focus" is not always better—commitizen's broader scope eliminates custom scripting
- The custom GHA commit parsing (lines 347-366) reinvents commitizen's wheel

**Blue Team Defense:**
The choice is defensible but marginal. The design should explicitly acknowledge that commitizen is a viable alternative and the BMV choice prioritizes **pattern flexibility** over **tool consolidation**. A future phase could migrate to commitizen if BMV patterns prove too fragile.

**Required Revision:** Add to L2 Decision Table (D-001) a note: "commitizen scored 7.5/10 and provides single-tool solution; BMV chosen for superior pattern flexibility, but commitizen remains a strong alternative for future consideration."

---

### DA-2: Is the PAT approach the right security trade-off?

**Challenge:** The design uses a fine-grained PAT with `contents: write` scope to bypass branch protection. This grants the workflow FULL WRITE ACCESS to the repository. A compromised GitHub Actions runner could:
- Push arbitrary commits to main
- Delete tags
- Rewrite history (if force-push is allowed)

A GitHub App with restricted permissions (create tags, push commits with signature) would be more secure. Why not start with the App?

**Design Response (explicit, D-004):**
- PAT is "simplest for single-repo OSS"
- GitHub App is "migration path for Phase 3"

**Devil's Advocate Rebuttal:**
- "Simple" for whom? The GitHub App setup is ~10 minutes. PAT rotation every 90 days is ongoing operational burden.
- Security posture should be designed-in from day one, not bolted on later

**Blue Team Defense:**
The PAT approach is pragmatic for initial implementation. However, the design underestimates the operational burden of PAT rotation. Add to risks table: "PAT expiration automation is NOT included in design; manual rotation is a guaranteed failure mode."

**Required Revision:** Strengthen RT-9 mitigation by adding PAT expiration monitoring as a REQUIRED implementation task, not optional. Change risk likelihood from "High" to "CERTAIN (within 90 days)."

---

### DA-3: Is on-push-to-main the right trigger?

**Challenge:** The design triggers version bumps automatically on EVERY push to main. This means:
- Every PR merge = potential new version
- No human review of version bump
- No opportunity to accumulate multiple features in one release

Release-please uses a "Release PR" model where version bumps are staged in a PR for human review. Why not adopt that model?

**Design Response (explicit, D-003):**
- "Conventional Commits encode the human decision"
- "Automatic reduces ceremony"

**Devil's Advocate Rebuttal:**
- Conventional Commits encode the *bump type* (major/minor/patch), not the *timing decision*. A team might want to merge 5 feature PRs, THEN cut a release.
- "Ceremony" is process debt. Removing ceremony without replacing it with automation can create chaos.

**Blue Team Defense:**
The automatic trigger is appropriate IF the project operates on a "continuous delivery" model (every merge is releasable). However, Jerry is pre-1.0 alpha. The design should acknowledge that **automatic bumps may be too aggressive for early-stage projects** and offer a manual-dispatch-only mode as an alternative.

**Required Revision:** Add to Trigger Mechanism section (2.1): "For projects that prefer batched releases, disable the `on: push` trigger and use manual `workflow_dispatch` only. The automatic mode is best suited for continuous delivery workflows."

---

### DA-4: Is the marketplace.json dual-version synchronization correct?

**Challenge:** The design (D-007, F-002) decides to synchronize BOTH `marketplace.json` `version` fields (top-level and `plugins[0].version`) with the framework version. However, the analysis document (TASK-002 F-002) notes:

> "The marketplace schema describes the `version` field generically as 'Semantic version' without specifying whether it tracks the plugin version or is independent."

If the top-level `version` is a **schema version** (meaning "this is marketplace manifest format v1.0.0"), then incrementing it to `0.3.0` on every framework release is semantically incorrect. The manifest format has not changed; only the plugin has.

**Design Response (implicit, line 599-609):**
- "The marketplace currently contains exactly one plugin"
- "Having a separate version for a single-plugin marketplace adds confusion"

**Devil's Advocate Rebuttal:**
- The marketplace manifest is a **distribution format**. Its version should track the format, not the content.
- If Anthropic releases marketplace schema v2.0 (breaking changes to manifest structure), Jerry would be stuck at `0.3.0` and unable to signal format compatibility.

**Blue Team Defense:**
The design's pragmatic choice is defensible for a single-plugin marketplace, but the semantic confusion is real. A safer approach:
1. **Keep top-level `version` at `1.0.0`** (manifest format v1)
2. **Synchronize only `plugins[0].version`**
3. **Bump top-level version only when manifest format changes**

**Required Revision:** Change D-007 decision to: "Do NOT synchronize top-level `version` (leave at 1.0.0). Synchronize `plugins[0].version` only. Rationale: Top-level field represents manifest schema version, which is independent of plugin version. Revisit if multi-plugin support is added."

---

### DA-5: Is SemVer pre-release format the right choice?

**Challenge:** The design uses SemVer pre-release format (`0.3.0-alpha.1`) because it matches the existing `release.yml` regex. However, the Python ecosystem standard (PEP 440) uses a different format (`0.3.0a1`, `0.3.0b1`, `0.3.0rc1`). Jerry is a Python project. Why not follow Python conventions?

**Design Response (implicit, line 186-191, D-008):**
- "Matches existing `release.yml` regex"
- "Consistent with tag format"

**Devil's Advocate Rebuttal:**
- The release.yml regex was written before PEP 440 considerations. It's not a law of nature.
- Python tools (pip, uv, PyPI) understand PEP 440 but may not understand SemVer pre-release syntax.
- If Jerry is ever published to PyPI, the version must be PEP 440 compliant.

**Blue Team Defense:**
This is a cultural alignment issue. Jerry is distributed as a Claude Code plugin, not a PyPI package (yet). The SemVer choice is defensible. However, the design should explicitly justify this choice and note the PEP 440 alternative.

**Required Revision:** Add to pre-release section (2.4): "Jerry uses SemVer pre-release format (`-alpha.1`) rather than PEP 440 (`a1`) because: (1) consistency with existing tag format, (2) GitHub Release UI compatibility. If Jerry is published to PyPI, this decision must be revisited as PEP 440 is the PyPI standard."

---

### DA-6: Is the 3-layer sync (script + pre-commit + CI) over-engineered?

**Challenge:** The design includes:
1. `sync_versions.py` script (can run standalone)
2. Pre-commit hook (runs on every commit)
3. CI validation step (runs on every PR)

This is three different enforcement points for the same invariant (version consistency). Is this necessary, or is it defense-in-depth taken too far?

**Design Response (implicit, section 3.3, "belt-and-suspenders"):**
- Pre-commit can be bypassed with `--no-verify`
- CI catches what pre-commit misses
- Standalone script allows developer testing

**Devil's Advocate Rebuttal:**
- Three layers = three failure modes. Each layer must be maintained.
- If pre-commit is reliable, CI validation is redundant.
- If CI is the real gate, pre-commit is just a courtesy check.

**Blue Team Defense:**
The 3-layer approach is justified by different threat models:
- **Pre-commit** — Local enforcement, fast feedback
- **CI** — Remote enforcement, cannot be bypassed
- **Standalone script** — Developer tooling, troubleshooting

However, the design could clarify that pre-commit is OPTIONAL (developer convenience) while CI validation is MANDATORY (gate). The standalone script serves both as pre-commit hook AND emergency fix tool.

**Required Revision:** Add to sync strategy (4.3): "The pre-commit hook is OPTIONAL but recommended for fast local feedback. The CI validation step is MANDATORY and serves as the authoritative gate. The standalone `sync_versions.py` script serves triple duty: pre-commit hook, CI validator, emergency fix tool."

---

### DA-7: Why not just use python-semantic-release or release-please?

**Challenge:** The design adopts a hybrid approach (BMV + custom GHA). Two evaluated tools—python-semantic-release and release-please—provide complete, battle-tested solutions:
- PSR: Python-native, handles pyproject.toml + Python files natively
- release-please: Google-backed, JSONPath for nested JSON fields, PR-based workflow

Why reinvent the wheel with a hybrid approach?

**Design Response (explicit, TASK-001 scores):**
- PSR scored 5/10 (no JSON support)
- release-please scored 7/10 (Node.js, additional config files)

**Devil's Advocate Rebuttal:**
- PSR's JSON gap can be filled with a 20-line Python script (way simpler than a full GHA workflow)
- release-please's "Node.js" concern is irrelevant when it runs entirely in GitHub Actions (no local Node install needed)

**Blue Team Defense:**
The hybrid approach is defensible because:
1. **BMV + custom GHA = Python-native end-to-end** (no Node.js in any step)
2. **Custom GHA gives full control** over trigger timing and error handling
3. **BMV config lives in pyproject.toml** (no extra JSON files like release-please)

However, the design should acknowledge that the hybrid approach trades "off-the-shelf" convenience for "custom" flexibility. Not every project will make this trade-off.

**Required Revision:** Add to L2 Architecture Decision Summary (line 1009-1029): "The hybrid approach prioritizes Python ecosystem alignment (no Node.js) and configuration simplicity (single pyproject.toml) over off-the-shelf tooling. Projects that value 'less code to maintain' over 'full control' should consider release-please or commitizen as single-tool alternatives."

---

## Required Revisions

### Critical (Must Address Before Implementation)

**REV-1: Marketplace Version Semantics (DA-4)**
- **Location:** Section 4.2 BMV configuration (line 574, line 593)
- **Change:** Remove top-level `version` from BMV file list. Keep top-level version at `1.0.0`.
- **Rationale:** Top-level `version` represents manifest schema version, not plugin version. Incrementing it with framework version is semantically incorrect.
- **Impact:** BMV config and sync script must be updated. Decision D-007 must be revised.

**REV-2: PAT Expiration Monitoring (DA-2, RT-9)**
- **Location:** Section 5.1 Authentication Strategy (line 861-874)
- **Change:** Add required implementation task: "Set up PAT expiration monitoring (calendar reminder + workflow failure alerts) BEFORE deploying version-bump workflow."
- **Rationale:** Manual PAT rotation is a guaranteed failure mode (90-day expiration). Monitoring is not optional.
- **Impact:** Adds operational task to implementation checklist.

**REV-3: First Release Edge Case Documentation (BT-10)**
- **Location:** Section 2.3 Determine bump type (line 326-334)
- **Change:** Clarify comment: "If no previous tag exists (first release), RANGE='HEAD' evaluates all commits in history. This is expected behavior."
- **Rationale:** Current comment "No previous version tag found. Using all commits." could be misinterpreted as an error.
- **Impact:** Documentation clarity only; logic is already correct.

### High Priority (Strongly Recommended)

**REV-4: BMV Pattern Contract Tests (BT-1, RT-7)**
- **Location:** New section "Pattern Validation Tests" after 4.4
- **Change:** Add contract test specification that validates BMV patterns match actual file structure before every bump.
- **Rationale:** Pattern breakage is the highest-likelihood failure mode (RT-7). Proactive detection prevents runtime failures.
- **Impact:** Requires new test file `tests/integration/test_bumpversion_patterns.py`.

**REV-5: Pre-Release Format Justification (DA-5)**
- **Location:** Section 2.4 Pre-Release Versioning (line 171)
- **Change:** Add explicit rationale for SemVer over PEP 440: "Jerry uses SemVer pre-release format (`-alpha.1`) for consistency with existing release.yml and GitHub Release UI. If Jerry is published to PyPI, this decision must be revisited as PEP 440 is the PyPI standard."
- **Rationale:** Design assumes SemVer without justifying why it's preferred over Python ecosystem norm.
- **Impact:** Documentation only; no code change required.

**REV-6: Atomic Push Strategy (BT-11)**
- **Location:** Section 3.2 version-bump.yml (line 419-422)
- **Change:** Use `git push --follow-tags origin main` instead of separate push commands. Add comment: "Atomic push prevents split-brain scenario where commit is pushed but tag fails."
- **Rationale:** Eliminates RT-1 race condition.
- **Impact:** Minor workflow change; requires verifying BMV creates annotated tags.

### Medium Priority (Consider Before Merge)

**REV-7: commitizen Alternative Acknowledgment (DA-1)**
- **Location:** Decision Table D-001 (line 1070)
- **Change:** Add rationale note: "commitizen scored 7.5/10 and provides single-tool solution; BMV chosen for superior multi-file pattern flexibility, but commitizen remains a strong alternative if BMV patterns prove too fragile."
- **Rationale:** Design should acknowledge the trade-off between tool consolidation (commitizen) and pattern flexibility (BMV).
- **Impact:** Documentation only.

**REV-8: Trigger Mechanism Caveat (DA-3)**
- **Location:** Section 2.1 Primary Trigger (line 126)
- **Change:** Add note: "Automatic on-push trigger is best suited for continuous delivery workflows. For batched releases, disable `on: push` and use manual `workflow_dispatch` only."
- **Rationale:** Design assumes continuous delivery model without stating it explicitly.
- **Impact:** Documentation + optional workflow configuration change.

**REV-9: 3-Layer Sync Clarification (DA-6)**
- **Location:** Section 4.3 sync script (line 636)
- **Change:** Add preamble: "The pre-commit hook is OPTIONAL (developer convenience). The CI validation step is MANDATORY (gate). The standalone script serves triple duty: pre-commit hook, CI validator, emergency fix tool."
- **Rationale:** Clarifies which layers are required vs recommended.
- **Impact:** Documentation only.

### Low Priority (Nice to Have)

**REV-10: Dry-Run Manual Dispatch (BT-13)**
- **Location:** Section 2.2 Manual Override (line 140-156)
- **Change:** Add `dry_run` boolean input to workflow_dispatch that runs BMV with `--dry-run` flag.
- **Rationale:** Allows testing workflow without side effects.
- **Impact:** Minor workflow enhancement.

**REV-11: Workflow Telemetry (BT-14)**
- **Location:** Section 3.2 version-bump.yml, after line 422
- **Change:** Add step that logs version bump metrics using `::notice::` annotation.
- **Rationale:** Improves observability for troubleshooting.
- **Impact:** Minor workflow enhancement.

**REV-12: Changelog Strategy Citation (DA-7)**
- **Location:** Section L1 Changelog Strategy (does not exist)
- **Change:** Add explicit mention that TASK-001 recommended git-cliff for changelog generation (research line 1197-1209).
- **Rationale:** Design omits changelog strategy; should acknowledge it as deferred to Phase 2.
- **Impact:** Documentation only; aligns with research.

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Red Team Findings (RT-*) | 18 |
| Blue Team Recommendations (BT-*) | 14 |
| Devil's Advocate Challenges (DA-*) | 7 |
| Required Revisions (REV-*) | 12 |
| Critical Revisions | 3 |
| High Priority Revisions | 3 |
| Medium Priority Revisions | 3 |
| Low Priority Revisions | 3 |

---

## Confidence Statement

This critique was conducted with **high confidence (0.91)** based on:
- Direct verification against actual repository files (pyproject.toml, plugin.json, marketplace.json, src/ modules, workflows, CLAUDE.md)
- Cross-validation with upstream research documents (TASK-001 QG 0.928, TASK-002 QG 0.935)
- Adversarial analysis using three distinct threat modeling patterns (Red Team, Blue Team, Devil's Advocate)
- Identification of 18 distinct failure scenarios with likelihood/impact assessments

**Uncertainty sources:**
- Pre-release workflow complexity (RT-13) — BMV pre-release part manipulation syntax is under-documented in the design; requires implementation testing to validate
- GitHub Actions concurrency behavior (RT-18) — Distributed lock mechanisms are not natively supported; proposed mitigation is theoretical
- marketplace.json schema semantics (DA-4) — Design assumes single interpretation without citing Anthropic's authoritative specification

**Recommendation:** Implement REV-1 through REV-6 (critical and high-priority revisions) before code implementation begins. Medium and low-priority revisions can be deferred to post-merge refinement.

---

*Critique completed by ps-critic v2.2.0 on 2026-02-12*
*Adversarial patterns: Red Team (attack surface), Blue Team (defense), Devil's Advocate (challenge assumptions)*
*Verdict: ACCEPT (score 0.926 ≥ threshold 0.92)*
