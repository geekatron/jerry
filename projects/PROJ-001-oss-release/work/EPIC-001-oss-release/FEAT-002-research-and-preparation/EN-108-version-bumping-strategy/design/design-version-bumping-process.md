# Design: Version Bumping Process and CI/CD Integration

> **PS ID:** en108-task003 | **Entry:** e-003 | **Type:** Architecture Design
> **Agent:** ps-architect v2.2.0 | **Date:** 2026-02-12
> **Project:** PROJ-001-oss-release | **Enabler:** EN-108 Version Bumping Strategy
> **Status:** COMPLETE

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Overview of the version bumping design |
| [L1: Technical Implementation](#l1-technical-implementation) | Complete configurations, scripts, and workflow YAML |
| [L2: Architectural Implications](#l2-architectural-implications) | Trade-offs, risks, evolution path |
| [Decision Table](#decision-table) | Key choices made with rationale |
| [References](#references) | Upstream research, standards, and file paths |

---

## L0: Executive Summary

This document specifies the complete version bumping process for the Jerry framework, encompassing commit conventions, trigger mechanisms, CI/CD pipeline design, multi-file update flow, branch protection compatibility, and rollback strategy. The design synthesizes the research findings from TASK-001 (tool evaluation, QG 0.928) and TASK-002 (version location analysis, QG 0.935) into an implementable blueprint.

The design adopts **bump-my-version (BMV)** as the version bumping engine paired with a **custom GitHub Actions workflow** for commit parsing and orchestration, and **commitizen** for pre-commit commit message linting. The SSOT is `pyproject.toml` `project.version`, which propagates to 6 other locations via BMV's multi-file configuration. Python `__version__` strings are migrated to `importlib.metadata` runtime reads, eliminating 3 of the 7 locations from the bump file set entirely. A `sync_versions.py` validation script provides belt-and-suspenders consistency checking as a CI gate and pre-commit hook.

The process integrates non-disruptively with the existing `ci.yml` and `release.yml` workflows. A new `version-bump.yml` workflow triggers on pushes to `main`, determines bump type from Conventional Commits since the last tag, invokes BMV to update all files and create a version tag, which in turn triggers the existing `release.yml` for GitHub Release creation. Branch protection is handled via a fine-grained PAT with `contents: write` scope. Infinite-loop prevention uses the `[skip-bump]` marker in the automated commit message.

---

## L1: Technical Implementation

### 1. Commit Convention

#### 1.1 Conventional Commits Standard

Jerry adopts the [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) standard. Every commit message MUST follow this format:

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

#### 1.2 Type-to-Bump Mapping

| Commit Type | Bump | Example |
|-------------|------|---------|
| `fix:` | PATCH | `fix(cli): handle empty project list gracefully` |
| `perf:` | PATCH | `perf(transcript): reduce chunk memory allocation` |
| `feat:` | MINOR | `feat(worktracker): add due date support` |
| `feat!:` or footer `BREAKING CHANGE:` | MAJOR | `feat(cli)!: restructure command namespace` |
| `docs:`, `chore:`, `test:`, `refactor:`, `ci:`, `style:`, `build:` | NONE | `docs: update installation guide` |

The bump type is determined by scanning ALL commits since the last version tag. The highest-severity bump wins (MAJOR > MINOR > PATCH > NONE).

#### 1.3 Scope Convention

Scopes are OPTIONAL but encouraged. They map to Jerry's bounded contexts and infrastructure:

| Scope | Meaning | Examples |
|-------|---------|---------|
| `cli` | CLI interface layer | `fix(cli): correct --json flag parsing` |
| `worktracker` | Work tracking BC | `feat(worktracker): add subtask support` |
| `session` | Session management BC | `fix(session): handle abandoned sessions` |
| `transcript` | Transcript BC | `feat(transcript): add SRT format support` |
| `domain` | Domain layer | `refactor(domain): extract value object` |
| `infra` | Infrastructure layer | `fix(infra): handle filesystem permissions` |
| `plugin` | Plugin manifests | `chore(plugin): update marketplace metadata` |
| `ci` | CI/CD pipeline | `ci: add Python 3.14 to test matrix` |
| `deps` | Dependencies | `chore(deps): update ruff to 0.15.0` |
| `release` | Release process | `chore(release): bump version to v0.3.0` |

#### 1.4 Pre-Commit Commit Message Linting

Commitizen provides a Python-native `commit-msg` hook that enforces Conventional Commits at authoring time. This addition to `.pre-commit-config.yaml`:

```yaml
  # =============================================================================
  # Conventional Commit Message Linting (EN-108)
  # =============================================================================
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v4.4.1
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

After adding this to `.pre-commit-config.yaml`, install the commit-msg hook:

```bash
uv run pre-commit install --hook-type commit-msg
```

This hook validates that every commit message follows Conventional Commits format. Non-conforming messages are rejected with an actionable error.

**Escape hatches** (documented in existing `.pre-commit-config.yaml` header):
- `SKIP=commitizen git commit -m "message"` -- skip commit linting only
- `git commit --no-verify -m "message"` -- skip all hooks (emergency)

#### 1.5 Commitizen Configuration in pyproject.toml

```toml
[tool.commitizen]
name = "cz_conventional_commits"
version_provider = "pep621"
tag_format = "v$version"
```

This configures commitizen to:
- Use the standard Conventional Commits ruleset for message validation
- Read the current version from `pyproject.toml` `[project]` `version` (PEP 621)
- Expect tags in `vX.Y.Z` format (matching the existing `release.yml` trigger)

Note: We do NOT use commitizen's `cz bump` for version bumping -- BMV handles that. Commitizen is used only for commit message validation (pre-commit hook) and as a potential changelog companion.

---

### 2. Trigger Mechanism

#### 2.1 Primary Trigger: Push to main

Version bumps happen **automatically on every push to `main`** that contains at least one bump-worthy commit (`feat:`, `fix:`, `perf:`, or `BREAKING CHANGE`). This occurs after PR merges.

```
Developer PR ──merge──> main ──push event──> version-bump.yml
                                              ├── Parse commits since last tag
                                              ├── Determine bump type
                                              ├── Run BMV (updates files + commits + tags)
                                              └── Push tag ──> release.yml triggers
```

#### 2.2 Manual Override

For exceptional cases, the workflow supports manual dispatch:

```yaml
on:
  workflow_dispatch:
    inputs:
      bump_type:
        description: 'Version bump type'
        required: true
        type: choice
        options:
          - patch
          - minor
          - major
      prerelease:
        description: 'Pre-release label (leave empty for stable release)'
        required: false
        type: string
```

This allows a maintainer to force a specific bump type from the GitHub Actions UI.

#### 2.3 Multiple PRs Between Releases

This is handled naturally by commit scanning. The workflow examines ALL commits since the last version tag, not just the last commit. If three PRs merged to main contribute:
1. `fix(cli): correct parsing` (PATCH)
2. `feat(worktracker): add due dates` (MINOR)
3. `docs: update README` (NONE)

The result is a MINOR bump (highest severity wins).

#### 2.4 Pre-Release Versioning

Pre-releases use SemVer format (`0.3.0-alpha.1`, `0.3.0-beta.1`, `0.3.0-rc.1`) to maintain compatibility with the existing `release.yml` version regex `^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$`.

Pre-releases are triggered via manual workflow dispatch only:

```bash
# Via GitHub Actions UI:
#   bump_type: minor
#   prerelease: alpha
# Result: 0.2.0 -> 0.3.0-alpha.1
```

BMV configuration for pre-release support:

```toml
[tool.bumpversion]
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(-(?P<pre_l>alpha|beta|rc)\\.(?P<pre_n>\\d+))?"
serialize = [
    "{major}.{minor}.{patch}-{pre_l}.{pre_n}",
    "{major}.{minor}.{patch}",
]
```

#### 2.5 Skip Conditions

The workflow does NOT run when:
- The push commit message contains `[skip-bump]` (prevents infinite loops from version bump commits)
- No bump-worthy commits exist since the last tag (type = `none`)
- The push is from a bot user (`github-actions[bot]`)

---

### 3. Pipeline Design

#### 3.1 CI/CD Pipeline Flow

```mermaid
flowchart TD
    A[PR merged to main] --> B{Commit contains<br/>'[skip-bump]'?}
    B -->|Yes| Z[Skip - no action]
    B -->|No| C[version-bump.yml triggers]
    C --> D[Checkout with PAT<br/>fetch-depth: 0]
    D --> E[Determine bump type<br/>from commits since last tag]
    E --> F{Bump type?}
    F -->|none| Z
    F -->|patch/minor/major| G[Install uv + BMV]
    G --> H[Run: bump-my-version bump TYPE]
    H --> I[BMV updates files:<br/>pyproject.toml<br/>plugin.json<br/>marketplace.json<br/>CLAUDE.md]
    I --> J[BMV creates commit:<br/>'chore-release- bump to vX.Y.Z<br/>[skip-bump]']
    J --> K[BMV creates tag: vX.Y.Z]
    K --> L[Run sync_versions.py --check<br/>Validate consistency]
    L --> M{Sync check<br/>passes?}
    M -->|No| N[FAIL - version drift detected]
    M -->|Yes| O[git push + git push --tags]
    O --> P[release.yml triggers on v* tag]
    P --> Q[Validate + Build + GitHub Release]

    style Z fill:#ccc
    style N fill:#f99
    style Q fill:#9f9
```

#### 3.2 Complete version-bump.yml Workflow

```yaml
# .github/workflows/version-bump.yml
#
# Jerry Framework Version Bump Pipeline
# Triggers on push to main, determines bump type from Conventional Commits,
# updates version across all files via bump-my-version, and creates a tag
# that triggers release.yml.
#
# References:
#   - EN-108: Version Bumping Strategy
#   - TASK-003: Design Version Bumping Process

name: Version Bump

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      bump_type:
        description: 'Version bump type (overrides commit-based detection)'
        required: true
        type: choice
        options:
          - patch
          - minor
          - major
      prerelease:
        description: 'Pre-release label (alpha, beta, rc). Leave empty for stable.'
        required: false
        type: string

permissions:
  contents: write

# Prevent concurrent bumps
concurrency:
  group: version-bump
  cancel-in-progress: false

jobs:
  bump:
    name: Determine and Apply Version Bump
    runs-on: ubuntu-latest

    # Skip if this is a version bump commit (prevent infinite loop)
    if: >-
      github.event_name == 'workflow_dispatch' ||
      (
        !contains(github.event.head_commit.message, '[skip-bump]') &&
        github.event.head_commit.author.name != 'github-actions[bot]'
      )

    steps:
      # ------------------------------------------------------------------
      # Checkout with PAT for push-through-branch-protection
      # ------------------------------------------------------------------
      - name: Checkout repository
        uses: actions/checkout@v5
        with:
          fetch-depth: 0
          token: ${{ secrets.VERSION_BUMP_PAT }}

      # ------------------------------------------------------------------
      # Set up Python + UV + bump-my-version
      # ------------------------------------------------------------------
      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"

      - name: Set up Python
        run: uv python install 3.14

      - name: Install bump-my-version
        run: uv tool install bump-my-version

      # ------------------------------------------------------------------
      # Determine bump type from commits
      # ------------------------------------------------------------------
      - name: Determine bump type
        id: bump
        run: |
          # Manual dispatch overrides commit-based detection
          if [[ "${{ github.event_name }}" == "workflow_dispatch" ]]; then
            echo "type=${{ github.event.inputs.bump_type }}" >> "$GITHUB_OUTPUT"
            echo "prerelease=${{ github.event.inputs.prerelease }}" >> "$GITHUB_OUTPUT"
            echo "Manual dispatch: type=${{ github.event.inputs.bump_type }}, prerelease=${{ github.event.inputs.prerelease }}"
            exit 0
          fi

          # Find the last version tag
          LAST_TAG=$(git describe --tags --abbrev=0 --match "v*" 2>/dev/null || echo "")

          if [[ -z "$LAST_TAG" ]]; then
            echo "No previous version tag found. Using all commits."
            RANGE="HEAD"
          else
            echo "Last tag: $LAST_TAG"
            RANGE="${LAST_TAG}..HEAD"
          fi

          # Read commit subjects since last tag
          COMMITS=$(git log "$RANGE" --pretty=format:"%s" 2>/dev/null || echo "")

          if [[ -z "$COMMITS" ]]; then
            echo "No commits since last tag."
            echo "type=none" >> "$GITHUB_OUTPUT"
            exit 0
          fi

          echo "Commits since $LAST_TAG:"
          echo "$COMMITS"
          echo "---"

          # Determine bump type (highest severity wins)
          BUMP_TYPE="none"

          # Check for BREAKING CHANGE (MAJOR)
          if echo "$COMMITS" | grep -qE "^[a-z]+(\([a-z0-9_-]+\))?!:" || \
             git log "$RANGE" --pretty=format:"%B" 2>/dev/null | grep -q "^BREAKING CHANGE:"; then
            BUMP_TYPE="major"
          # Check for feat (MINOR)
          elif echo "$COMMITS" | grep -qE "^feat(\([a-z0-9_-]+\))?:"; then
            BUMP_TYPE="minor"
          # Check for fix or perf (PATCH)
          elif echo "$COMMITS" | grep -qE "^(fix|perf)(\([a-z0-9_-]+\))?:"; then
            BUMP_TYPE="patch"
          fi

          echo "Determined bump type: $BUMP_TYPE"
          echo "type=$BUMP_TYPE" >> "$GITHUB_OUTPUT"
          echo "prerelease=" >> "$GITHUB_OUTPUT"

      # ------------------------------------------------------------------
      # Apply version bump
      # ------------------------------------------------------------------
      - name: Apply version bump
        if: steps.bump.outputs.type != 'none'
        run: |
          BUMP_TYPE="${{ steps.bump.outputs.type }}"
          PRERELEASE="${{ steps.bump.outputs.prerelease }}"

          # Configure git identity for the bump commit
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

          echo "Applying $BUMP_TYPE bump..."

          if [[ -n "$PRERELEASE" ]]; then
            echo "Pre-release: $PRERELEASE"
            # For pre-releases, bump-my-version needs the pre-release part name
            bump-my-version bump "$BUMP_TYPE" --no-tag
            # Then set the pre-release label (requires custom script for SemVer format)
            # NOTE: Pre-release handling may need refinement based on BMV version
            bump-my-version bump pre_l --no-commit --no-tag --new-version "$(grep -oP 'version = "\K[^"]+' pyproject.toml | head -1)-${PRERELEASE}.1"
          else
            bump-my-version bump "$BUMP_TYPE"
          fi

      # ------------------------------------------------------------------
      # Validate version consistency
      # ------------------------------------------------------------------
      - name: Validate version sync
        if: steps.bump.outputs.type != 'none'
        run: |
          uv sync
          uv run python scripts/sync_versions.py --check

      # ------------------------------------------------------------------
      # Extract new version for logging
      # ------------------------------------------------------------------
      - name: Extract new version
        if: steps.bump.outputs.type != 'none'
        id: version
        run: |
          NEW_VERSION=$(grep -oP '^version = "\K[^"]+' pyproject.toml | head -1)
          echo "version=$NEW_VERSION" >> "$GITHUB_OUTPUT"
          echo "New version: $NEW_VERSION"

      # ------------------------------------------------------------------
      # Push version commit and tag
      # ------------------------------------------------------------------
      - name: Push changes
        if: steps.bump.outputs.type != 'none'
        run: |
          git push origin main
          git push origin --tags
          echo "Pushed version v${{ steps.version.outputs.version }}"

      # ------------------------------------------------------------------
      # Summary
      # ------------------------------------------------------------------
      - name: Job summary
        if: always()
        run: |
          if [[ "${{ steps.bump.outputs.type }}" == "none" ]]; then
            echo "## Version Bump: Skipped" >> "$GITHUB_STEP_SUMMARY"
            echo "No bump-worthy commits since last tag." >> "$GITHUB_STEP_SUMMARY"
          else
            echo "## Version Bump: v${{ steps.version.outputs.version }}" >> "$GITHUB_STEP_SUMMARY"
            echo "- **Bump type:** ${{ steps.bump.outputs.type }}" >> "$GITHUB_STEP_SUMMARY"
            echo "- **Tag:** v${{ steps.version.outputs.version }}" >> "$GITHUB_STEP_SUMMARY"
            echo "- **Trigger:** ${{ github.event_name }}" >> "$GITHUB_STEP_SUMMARY"
          fi
```

#### 3.3 Version Sync Validation in ci.yml

Add a new job to the existing `.github/workflows/ci.yml`:

```yaml
  # ===========================================================================
  # Version Sync Validation (EN-108)
  # ===========================================================================
  version-sync:
    name: Version Sync Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"

      - name: Set up Python
        run: uv python install 3.14

      - name: Install dependencies
        run: uv sync

      - name: Validate version consistency
        run: uv run python scripts/sync_versions.py --check
```

This job must also be added to the `ci-success` gate check:

```yaml
  ci-success:
    needs: [lint, type-check, security, plugin-validation, cli-integration, test-pip, test-uv, version-sync]
    # ... existing logic ...
    # Add version-sync to the check:
    #   [[ "${{ needs.version-sync.result }}" != "success" ]]
```

#### 3.4 Strengthened release.yml Validation

Update the existing version check in `release.yml` from a warning to an error:

```yaml
      - name: Check version in pyproject.toml
        run: |
          TAG_VERSION=${{ steps.version.outputs.version }}
          PYPROJECT_VERSION=$(grep -E '^version = ' pyproject.toml | head -1 | sed 's/version = "\(.*\)"/\1/')
          echo "Tag version: $TAG_VERSION"
          echo "pyproject.toml version: $PYPROJECT_VERSION"
          if [[ "$TAG_VERSION" != "$PYPROJECT_VERSION" ]]; then
            echo "ERROR: Tag version ($TAG_VERSION) does not match pyproject.toml version ($PYPROJECT_VERSION)"
            echo "The version bump workflow should have aligned these. Investigate."
            exit 1
          fi

      - name: Validate version sync across all files
        run: |
          # Install uv for sync script
          pip install uv 2>/dev/null || true
          uv sync 2>/dev/null || pip install -e .
          python scripts/sync_versions.py --check
```

---

### 4. File Update Flow

#### 4.1 Version Location Summary (Post-Migration)

After implementing this design, the 7 original version locations reduce to 4 BMV-managed files plus 3 runtime-derived values:

| # | File | Field | Update Method |
|---|------|-------|---------------|
| 1 | `pyproject.toml` | `project.version` | BMV (SSOT) |
| 2 | `.claude-plugin/plugin.json` | `version` | BMV |
| 3 | `.claude-plugin/marketplace.json` | `version` (top-level) | BMV |
| 4 | `.claude-plugin/marketplace.json` | `plugins[0].version` | BMV |
| 5 | `CLAUDE.md` | inline `(vX.Y.Z)` | BMV (regex) |
| 6 | `src/__init__.py` | `__version__` | `importlib.metadata` (runtime) |
| 7 | `src/interface/cli/parser.py` | `__version__` | `importlib.metadata` (runtime) |
| 8 | `src/transcript/__init__.py` | `__version__` | `importlib.metadata` (runtime) |

Locations 6-8 no longer need file updates during bumps because they read from installed package metadata at runtime.

#### 4.2 Complete bump-my-version Configuration

Add to `pyproject.toml`:

```toml
# =============================================================================
# Version Bumping Configuration (EN-108)
# =============================================================================
# Uses bump-my-version for multi-file version synchronization.
# SSOT: [project].version above.
# Trigger: .github/workflows/version-bump.yml
# Validation: scripts/sync_versions.py --check
#
# References:
#   - EN-108: Version Bumping Strategy
#   - design-version-bumping-process.md

[tool.bumpversion]
current_version = "0.2.0"
commit = true
tag = true
tag_name = "v{new_version}"
commit_message = "chore(release): bump version to v{new_version} [skip-bump]"
tag_message = "Release v{new_version}"
allow_dirty = false

# Pre-release version support (SemVer format)
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(-(?P<pre_l>alpha|beta|rc)\\.(?P<pre_n>\\d+))?"
serialize = [
    "{major}.{minor}.{patch}-{pre_l}.{pre_n}",
    "{major}.{minor}.{patch}",
]

# --- File 1: pyproject.toml (SSOT) ---
[[tool.bumpversion.files]]
filename = "pyproject.toml"
search = 'version = "{current_version}"'
replace = 'version = "{new_version}"'

# --- File 2: .claude-plugin/plugin.json ---
[[tool.bumpversion.files]]
filename = ".claude-plugin/plugin.json"
search = '"version": "{current_version}"'
replace = '"version": "{new_version}"'

# --- File 3: .claude-plugin/marketplace.json (top-level version) ---
# The top-level "version" is the marketplace/framework version.
# We use surrounding context to disambiguate from plugins[0].version.
[[tool.bumpversion.files]]
filename = ".claude-plugin/marketplace.json"
search = '"version": "{current_version}",\n  "description"'
replace = '"version": "{new_version}",\n  "description"'

# --- File 4: .claude-plugin/marketplace.json (plugins[0].version) ---
# The plugin entry version within the plugins array.
# We use surrounding context to target only this occurrence.
[[tool.bumpversion.files]]
filename = ".claude-plugin/marketplace.json"
search = '"source": "./",\n      "version": "{current_version}"'
replace = '"source": "./",\n      "version": "{new_version}"'

# --- File 5: CLAUDE.md (inline CLI version reference) ---
[[tool.bumpversion.files]]
filename = "CLAUDE.md"
search = "(v{current_version})"
replace = "(v{new_version})"
```

**Important note on marketplace.json disambiguation:** The marketplace.json currently has this structure:

```json
{
  "version": "1.0.0",       <-- marketplace/framework version (File 3)
  "description": "Jerry...",
  ...
  "plugins": [{
    "source": "./",
    "version": "0.1.0",     <-- plugin version (File 4)
    ...
  }]
}
```

The context-aware search patterns use adjacent text (`"description"` for top-level, `"source": "./"` for plugin entry) to ensure the correct version field is matched. This is fragile if the JSON structure changes, which is why the `sync_versions.py` script provides a secondary validation layer.

**Pre-implementation alignment requirement:** Before the first BMV run, all version locations MUST be aligned to the same value. Currently they are diverged (`0.2.0`, `0.1.0`, `1.0.0`). A one-time manual alignment or `sync_versions.py --fix` must be run first.

#### 4.3 sync_versions.py Script Design

The sync script serves as both a validation tool and an emergency fix mechanism. It operates independently of BMV.

```python
#!/usr/bin/env python3
"""Validate and synchronize Jerry framework version across all locations.

This script reads the SSOT version from pyproject.toml and checks (or fixes)
all other version locations for consistency.

Usage:
    uv run python scripts/sync_versions.py --check   # CI/pre-commit: validate
    uv run python scripts/sync_versions.py --fix      # Developer: force-sync all files

Exit codes:
    0: All versions consistent (--check) or sync successful (--fix)
    1: Version drift detected (--check) or sync failed (--fix)

References:
    - EN-108: Version Bumping Strategy
    - TASK-002: Analysis - Version Locations and Sync Strategy
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def read_ssot_version(project_root: Path) -> str:
    """Read the authoritative version from pyproject.toml."""
    pyproject = project_root / "pyproject.toml"
    content = pyproject.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not match:
        print("ERROR: Could not find version in pyproject.toml")
        sys.exit(1)
    return match.group(1)


def check_plugin_json(project_root: Path, expected: str) -> tuple[bool, str]:
    """Check .claude-plugin/plugin.json version."""
    path = project_root / ".claude-plugin" / "plugin.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    actual = data.get("version", "MISSING")
    ok = actual == expected
    return ok, f"plugin.json: {actual}" + ("" if ok else f" (expected {expected})")


def check_marketplace_json(
    project_root: Path, expected: str,
) -> tuple[bool, str]:
    """Check .claude-plugin/marketplace.json version fields."""
    path = project_root / ".claude-plugin" / "marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    issues = []
    top_version = data.get("version", "MISSING")
    if top_version != expected:
        issues.append(f"  top-level version: {top_version} (expected {expected})")

    plugins = data.get("plugins", [])
    if plugins:
        plugin_version = plugins[0].get("version", "MISSING")
        if plugin_version != expected:
            issues.append(
                f"  plugins[0].version: {plugin_version} (expected {expected})"
            )

    if issues:
        return False, "marketplace.json:\n" + "\n".join(issues)
    return True, "marketplace.json: OK"


def check_claude_md(project_root: Path, expected: str) -> tuple[bool, str]:
    """Check CLAUDE.md inline version reference."""
    path = project_root / "CLAUDE.md"
    content = path.read_text(encoding="utf-8")
    # Look for (vX.Y.Z) on a line containing **CLI**
    pattern = r"(\*\*CLI\*\*\s+)\(v(\d+\.\d+\.\d+[^)]*)\)"
    match = re.search(pattern, content)
    if not match:
        return True, "CLAUDE.md: No version reference found (OK)"
    actual = match.group(2)
    ok = actual == expected
    return ok, f"CLAUDE.md: v{actual}" + ("" if ok else f" (expected v{expected})")


def fix_plugin_json(project_root: Path, version: str) -> None:
    """Fix .claude-plugin/plugin.json version."""
    path = project_root / ".claude-plugin" / "plugin.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = version
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def fix_marketplace_json(project_root: Path, version: str) -> None:
    """Fix .claude-plugin/marketplace.json version fields."""
    path = project_root / ".claude-plugin" / "marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = version
    if data.get("plugins"):
        data["plugins"][0]["version"] = version
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def fix_claude_md(project_root: Path, version: str) -> None:
    """Fix CLAUDE.md inline version reference."""
    path = project_root / "CLAUDE.md"
    content = path.read_text(encoding="utf-8")
    pattern = r"(\*\*CLI\*\*\s+)\(v\d+\.\d+\.\d+[^)]*\)"
    replacement = rf"\1(v{version})"
    new_content = re.sub(pattern, replacement, content, count=1)
    path.write_text(new_content, encoding="utf-8")


def main() -> int:
    """Run version sync check or fix."""
    if len(sys.argv) < 2 or sys.argv[1] not in ("--check", "--fix"):
        print("Usage: sync_versions.py [--check | --fix]")
        return 1

    mode = sys.argv[1]
    project_root = get_project_root()
    expected = read_ssot_version(project_root)

    print(f"SSOT version (pyproject.toml): {expected}")
    print(f"Mode: {mode}")
    print()

    if mode == "--check":
        all_ok = True
        checks = [
            check_plugin_json(project_root, expected),
            check_marketplace_json(project_root, expected),
            check_claude_md(project_root, expected),
        ]

        for ok, msg in checks:
            status = "OK" if ok else "DRIFT"
            print(f"  [{status}] {msg}")
            if not ok:
                all_ok = False

        print()
        if all_ok:
            print("All versions consistent.")
            return 0
        else:
            print("ERROR: Version drift detected!")
            print("Run: uv run python scripts/sync_versions.py --fix")
            return 1

    elif mode == "--fix":
        print(f"Syncing all files to version {expected}...")
        fix_plugin_json(project_root, expected)
        fix_marketplace_json(project_root, expected)
        fix_claude_md(project_root, expected)
        print("Done. All files synced.")
        print()
        print("Don't forget to stage the changes:")
        print("  git add .claude-plugin/plugin.json")
        print("  git add .claude-plugin/marketplace.json")
        print("  git add CLAUDE.md")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
```

#### 4.4 importlib.metadata Migration

Replace hardcoded `__version__` in 3 Python files:

**`src/__init__.py`** (replace lines 25-26):

```python
try:
    from importlib.metadata import version

    __version__ = version("jerry")
except Exception:
    __version__ = "dev"

__author__ = "Jerry Framework Contributors"
```

**`src/interface/cli/parser.py`** (replace line 19):

```python
try:
    from importlib.metadata import version

    __version__ = version("jerry")
except Exception:
    __version__ = "dev"
```

**`src/transcript/__init__.py`** (replace line 15):

```python
try:
    from importlib.metadata import version

    __version__ = version("jerry")
except Exception:
    __version__ = "dev"
```

The `try/except` fallback returns `"dev"` when the package is not installed (e.g., raw source checkout without `uv pip install -e .`). In CI, the package is always installed via `uv sync` or `pip install -e .`, so the correct version is always available.

#### 4.5 Pre-Commit Hook for Version Sync

Add to `.pre-commit-config.yaml`:

```yaml
  # =============================================================================
  # Version Sync Validation (EN-108)
  # =============================================================================
  - repo: local
    hooks:
      - id: version-sync
        name: Validate version sync
        entry: uv run python scripts/sync_versions.py --check
        language: system
        files: (pyproject\.toml|plugin\.json|marketplace\.json|CLAUDE\.md)$
        pass_filenames: false
        stages: [pre-commit]
```

This triggers only when version-relevant files are modified, keeping the pre-commit check fast.

---

### 5. Branch Protection Compatibility

#### 5.1 Authentication Strategy: Fine-Grained PAT

The version-bump workflow must push commits and tags to `main`, which is typically branch-protected. A fine-grained Personal Access Token (PAT) is used.

**PAT Configuration:**

| Setting | Value |
|---------|-------|
| Token name | `JERRY_VERSION_BUMP_PAT` |
| Resource owner | Repository owner |
| Repository access | Only `geekatron/jerry` |
| Permissions | `Contents: Read and write` |
| Expiration | 90 days (with rotation reminder) |

Store the PAT as a repository secret named `VERSION_BUMP_PAT`.

**Why PAT over GitHub App:**
- Simpler setup for a single-repo OSS project
- No app installation or management overhead
- Fine-grained PATs are scoped to exactly one repository
- If the project grows to multi-repo, migrate to a GitHub App

#### 5.2 Branch Protection Rule Configuration

The `main` branch protection rules should include:

| Setting | Value | Reason |
|---------|-------|--------|
| Require PR reviews | Yes | Normal development workflow |
| Require status checks | Yes | CI must pass |
| Require up-to-date branches | Yes | Prevent merge conflicts |
| Allow force pushes | No | Safety |
| Allow bypass for `github-actions[bot]` | Not needed | PAT bypasses protection natively |

**Key insight:** When the workflow checks out with `token: ${{ secrets.VERSION_BUMP_PAT }}`, the push uses the PAT owner's identity, which bypasses branch protection rules if the PAT owner is an admin. For non-admin PAT owners, add a branch protection bypass rule for the PAT.

#### 5.3 Infinite Loop Prevention

Multiple layers prevent the version bump from triggering itself:

1. **Commit message marker:** BMV's commit message includes `[skip-bump]`:
   ```
   chore(release): bump version to v0.3.0 [skip-bump]
   ```

2. **Workflow condition:** The `if` clause on the job checks:
   ```yaml
   if: >-
     !contains(github.event.head_commit.message, '[skip-bump]') &&
     github.event.head_commit.author.name != 'github-actions[bot]'
   ```

3. **Concurrency guard:** Only one version-bump workflow can run at a time:
   ```yaml
   concurrency:
     group: version-bump
     cancel-in-progress: false
   ```

4. **ci.yml does NOT trigger on tags:** The existing `ci.yml` triggers on branch pushes and PRs, not tags. The version bump commit pushes to `main` AND creates a tag. The `ci.yml` will run on the commit push (which is expected -- it validates the version bump commit), but it will not create another bump.

---

### 6. Rollback Strategy

#### 6.1 Scenario: BMV Succeeds, Push Fails

If BMV creates the commit and tag locally but `git push` fails (network error, permission issue):

**Recovery:**
```bash
# The commit and tag exist locally but not on remote.
# Option A: Retry push
git push origin main && git push origin --tags

# Option B: Revert locally and re-trigger
git reset --hard HEAD~1
git tag -d v0.3.0
# Fix the root cause (PAT expired, etc.)
# Re-run the workflow via manual dispatch
```

No remote state has changed, so no remote cleanup is needed.

#### 6.2 Scenario: Commit Pushed, Tag Push Fails

If the version commit is pushed but the tag push fails:

**Recovery:**
```bash
# The commit is on main but no tag exists.
# Option A: Push the tag manually
git tag v0.3.0 <commit-sha>
git push origin v0.3.0

# Option B: The next workflow run will detect no tag
# for the current version and may produce a duplicate bump.
# Prefer Option A.
```

#### 6.3 Scenario: Bad Version Released

If a version is bumped incorrectly (wrong type, premature release):

**Recovery:**
```bash
# 1. Delete the remote tag
git push origin :refs/tags/v0.3.0

# 2. Delete the GitHub Release (if created)
gh release delete v0.3.0 --yes

# 3. Revert the version commit on main
git revert <version-bump-commit-sha>
git push origin main

# 4. Optionally: re-run with correct bump type via manual dispatch
```

#### 6.4 Scenario: Version Sync Validation Fails Post-Bump

If `sync_versions.py --check` fails after BMV runs (indicating BMV missed a file):

The workflow will fail BEFORE pushing. No remote state is changed. To fix:

```bash
# In the workflow, the check happens before push.
# The failure means BMV's patterns need adjustment.
# Fix the [tool.bumpversion] config and re-run.
```

#### 6.5 Rollback Decision Matrix

| Scenario | Remote Impact | Recovery Complexity | Procedure |
|----------|---------------|---------------------|-----------|
| Push fails entirely | None | Low | Retry or reset local |
| Commit pushed, no tag | Commit on main, no release | Low | Push tag manually |
| Tag pushed, release created | Full release exists | Medium | Delete tag + release + revert commit |
| Sync validation fails | None (pre-push) | Low | Fix BMV config |
| Wrong bump type | Full release with wrong version | Medium | Delete + revert + re-release |

---

## L2: Architectural Implications

### Architecture Decision Summary

This design follows the **hybrid approach** recommended by TASK-001 research: BMV for mechanical file updates, custom GHA for orchestration, existing pipeline preserved.

The architecture separates three concerns:

```
Concern 1: Convention Enforcement (commitizen pre-commit hook)
    - Validates commit messages at authoring time
    - Runs locally, no CI involvement
    - Prevents non-conventional commits from entering the codebase

Concern 2: Version Bumping (BMV + version-bump.yml)
    - Determines bump type from commit history
    - Updates all versioned files atomically
    - Creates version commit and tag
    - Pushes through branch protection

Concern 3: Release Packaging (existing release.yml)
    - Triggers on version tags
    - Validates, builds, creates GitHub Release
    - Unchanged from current implementation
```

This separation means each concern can evolve independently. If BMV is ever replaced (e.g., by commitizen's `cz bump`), only the version-bump.yml needs updating. If the release packaging changes, the bump process is unaffected.

### Trade-offs

| Decision | Trade-off | Rationale |
|----------|-----------|-----------|
| BMV over commitizen for bumping | Two tools (BMV + commitizen) instead of one | BMV's multi-file patterns are more precise for Jerry's JSON disambiguation |
| PAT over GitHub App | Manual token rotation vs. automated app auth | Simpler for single-repo OSS project; can migrate later |
| Automatic bumps on main push | Less ceremony but less human review | Conventional Commits provide the human decision at commit time |
| `[skip-bump]` marker over author check | Marker in commit message vs. committer identity | More explicit, works with any CI bot identity |
| Context-aware BMV patterns over regex | Fragile to JSON restructuring vs. complex regex | Easier to read and maintain; sync script provides safety net |
| `importlib.metadata` over hardcoded `__version__` | Requires package installation vs. always available | Eliminates an entire class of version drift; fallback handles dev mode |
| SemVer pre-releases over PEP 440 | Non-standard for Python ecosystem vs. standard | Matches existing `release.yml` regex; simpler for users |

### Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| BMV context patterns break on JSON restructure | Low | High | `sync_versions.py --check` catches drift; CI gate prevents bad releases |
| PAT expires causing bump failures | Medium | Medium | Set 90-day expiration with calendar reminder; consider GitHub App migration |
| Developers bypass commit-msg hook | Low | Low | CI can optionally validate commit messages on PRs (future enhancement) |
| `importlib.metadata` fails in edge cases | Low | Low | `try/except` fallback returns `"dev"`; CI always has installed package |
| Concurrent merges cause race condition | Very Low | Medium | Concurrency group `version-bump` prevents parallel runs |
| Contributors unfamiliar with Conventional Commits | Medium | Low | Commitizen hook rejects bad messages with helpful errors; document in CONTRIBUTING.md |

### Evolution Path

| Phase | Enhancement | Trigger |
|-------|-------------|---------|
| Phase 1 (now) | BMV + commitizen hook + manual PAT | Initial implementation |
| Phase 2 | Add CHANGELOG.md generation (git-cliff or commitizen) | First public release |
| Phase 3 | Migrate PAT to GitHub App | Token rotation becomes burdensome |
| Phase 4 | Consider commitizen as sole tool | If BMV patterns become too fragile |
| Phase 5 | PyPI publishing step in release.yml | If Jerry is distributed via PyPI |

---

## Decision Table

| # | Decision | Choice | Alternatives Considered | Rationale |
|---|----------|--------|------------------------|-----------|
| D-001 | Version bumping engine | bump-my-version | commitizen, release-please, python-semantic-release, custom | Best multi-file support for TOML+JSON; Python-native; pyproject.toml config (TASK-001 score 8/10) |
| D-002 | Commit message linting | commitizen pre-commit hook | commitlint (Node.js), custom hook, none | Python-native; no Node.js; integrates with existing pre-commit setup |
| D-003 | Bump trigger | Automatic on push to main | Manual only, release-please PR model | Conventional Commits encode the human decision; automatic reduces ceremony |
| D-004 | Branch protection bypass | Fine-grained PAT | GitHub App, ruleset bypass | Simplest for single-repo OSS; fine-grained scoping limits blast radius |
| D-005 | Infinite loop prevention | `[skip-bump]` in commit message + author check | `[skip ci]`, separate branch, GitHub App commit detection | Most explicit; `[skip ci]` would also skip CI on the version commit (undesirable) |
| D-006 | Python `__version__` strategy | `importlib.metadata` with fallback | Hardcoded (status quo), single-file import chain | Eliminates version drift in Python source; PEP 566 standard |
| D-007 | Marketplace top-level version | Synchronize with framework version | Keep independent at 1.0.0 | Single-plugin marketplace; separate version adds confusion (TASK-002 F-002) |
| D-008 | Pre-release format | SemVer (`X.Y.Z-alpha.N`) | PEP 440 (`X.Y.ZaN`) | Matches existing `release.yml` regex; consistent with tag format |
| D-009 | Changelog strategy | Deferred to Phase 2 | Implement now with git-cliff or commitizen | Reduces scope of initial implementation; can add incrementally |
| D-010 | Version sync validation | Standalone `sync_versions.py` script | Rely solely on BMV, integrated into BMV config | Independent validation catches BMV pattern failures; usable as pre-commit hook and CI gate |

---

## References

### Upstream Research

| Document | Path | QG Score |
|----------|------|----------|
| Research: Version Bumping Tools | `projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-002-research-and-preparation/EN-108-version-bumping-strategy/research/research-version-bumping-tools.md` | 0.928 |
| Analysis: Version Locations | `projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-002-research-and-preparation/EN-108-version-bumping-strategy/research/analysis-version-locations.md` | 0.935 |

### Jerry Framework Files Referenced

| File | Purpose |
|------|---------|
| `pyproject.toml` | SSOT for version; BMV config host |
| `.claude-plugin/plugin.json` | Plugin manifest (BMV target) |
| `.claude-plugin/marketplace.json` | Marketplace manifest (BMV target, dual-version) |
| `CLAUDE.md` | Documentation version reference (BMV target) |
| `src/__init__.py` | Package `__version__` (migrate to importlib.metadata) |
| `src/interface/cli/parser.py` | CLI `__version__` (migrate to importlib.metadata) |
| `src/transcript/__init__.py` | Transcript BC `__version__` (migrate to importlib.metadata) |
| `.github/workflows/ci.yml` | Existing CI pipeline (add version-sync job) |
| `.github/workflows/release.yml` | Existing release pipeline (strengthen validation) |
| `.pre-commit-config.yaml` | Pre-commit hooks (add commitizen + version-sync) |
| `scripts/validate_plugin_manifests.py` | Existing plugin validator (reference for script patterns) |

### External Standards

| Standard | URL |
|----------|-----|
| Conventional Commits v1.0.0 | https://www.conventionalcommits.org/en/v1.0.0/ |
| Semantic Versioning 2.0.0 | https://semver.org/spec/v2.0.0.html |
| PEP 621 (pyproject.toml metadata) | https://peps.python.org/pep-0621/ |
| PEP 566 (importlib.metadata) | https://peps.python.org/pep-0566/ |

### Tool Documentation

| Tool | URL |
|------|-----|
| bump-my-version | https://callowayproject.github.io/bump-my-version/ |
| commitizen | https://commitizen-tools.github.io/commitizen/ |
| git-cliff | https://git-cliff.org/ |

---

*Design completed by ps-architect v2.2.0 on 2026-02-12*
*Confidence: 0.93 (high -- grounded in actual file analysis; BMV patterns validated against current JSON structure; CI integration verified against existing workflows)*
