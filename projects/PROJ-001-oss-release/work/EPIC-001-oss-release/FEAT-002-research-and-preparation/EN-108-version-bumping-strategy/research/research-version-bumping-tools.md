# Research: Version Bumping Tools and Approaches

> **Document ID:** EN-108-TASK-001-R001
> **PS ID:** en108-task001
> **Entry ID:** e-001
> **Author:** ps-researcher (v2.2.0)
> **Date:** 2026-02-12
> **Status:** COMPLETE (v2 — revised per CRIT-001 feedback)
> **Project:** PROJ-001-oss-release
> **Parent Task:** TASK-001 Research Version Bumping Tools and Approaches
> **Parent Enabler:** EN-108 Version Bumping Strategy

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | ELI5 overview for stakeholders |
| [L1: Technical Analysis](#l1-technical-analysis) | Detailed tool evaluations (6 tools) with configuration examples |
| [Comparison Matrix](#comparison-matrix) | Side-by-side feature comparison including pre-release and pre-commit |
| [L2: Architectural Implications](#l2-architectural-implications) | Strategic fit, trade-offs, risks, pre-release versioning, and pre-commit assessment |
| [Recommendation](#recommendation) | Final recommendation with changelog strategy and alternatives |
| [References](#references) | All sources cited with star count disclaimer |

---

## L0: Executive Summary

Jerry needs to keep version numbers in sync across three files (pyproject.toml, plugin.json, and marketplace.json) whenever a release is made. Right now this is done manually, and the versions have already drifted apart -- pyproject.toml says 0.2.0, plugin.json says 0.1.0, and marketplace.json has both 1.0.0 and 0.1.0. We need a tool that can automatically figure out what the next version should be (based on commit messages following the "Conventional Commits" standard), update all three files at once, and integrate cleanly with our GitHub Actions CI/CD pipeline.

After evaluating six tools and approaches, the recommendation is **bump-my-version** as the primary version bumping engine, combined with a **custom GitHub Actions workflow** for orchestration. This combination provides the best fit for Jerry's specific constraints: it natively handles multi-file updates including nested JSON fields, is Python-native (installable via UV), requires no Node.js runtime, and is the most mature multi-file version bumping tool in the Python ecosystem. The custom GitHub Actions workflow wrapper gives us full control over when bumps trigger, how they interact with branch protection, and how they coordinate with the existing release pipeline. For changelog generation, **git-cliff** is recommended as a companion tool.

A strong alternative is **commitizen**, which offers a single-tool solution combining conventional commits parsing, version bumping, changelog generation, and pre-commit hook integration in a single Python-native package. Commitizen scores 7.5/10 for Jerry fit -- slightly below BMV's 8/10 due to less flexible multi-file configuration, but its broader feature set reduces overall maintenance burden.

The runner-up is **release-please** (Google), which is excellent for pure GitHub workflows with native JSONPath support for JSON file updates. The other tools evaluated (python-semantic-release, semantic-release for Node.js, and a fully custom approach) each have trade-offs that make them less suitable for Jerry's specific multi-file, multi-format needs.

---

## L1: Technical Analysis

### Tool 1: python-semantic-release (PSR)

**Repository:** [python-semantic-release/python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
**Language:** Python
**GitHub Stars:** ~2,000 (as of early 2025)
**Last Major Release:** v9.x series (actively maintained)
**License:** MIT

#### Overview

python-semantic-release is a Python implementation of the semantic versioning workflow. It parses Conventional Commits to determine version bumps, updates version locations, generates changelogs, creates Git tags, and can publish to PyPI. It is designed primarily for Python packages and has first-class pyproject.toml support.

#### Multi-File Support

PSR supports updating version in multiple locations via `version_toml` and `version_variables` configuration:

```toml
# pyproject.toml configuration for PSR
[tool.semantic_release]
version_toml = [
    "pyproject.toml:project.version",
]
version_variables = [
    "src/__init__.py:__version__",
]
```

**Limitation:** `version_toml` works for TOML files, and `version_variables` works for Python files with simple `__version__ = "X.Y.Z"` patterns. There is no native JSON file update capability. To update `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, you would need:
- A custom build hook/command to update JSON files post-bump
- Or a separate script triggered after PSR runs

**Critical Gap:** Cannot update nested JSON fields like `plugins[0].version` in marketplace.json natively. This is a showstopper for Jerry without supplementary scripting.

#### Conventional Commits Support

Excellent. PSR was built around Conventional Commits:
- `fix:` triggers PATCH bump
- `feat:` triggers MINOR bump
- `BREAKING CHANGE:` or `feat!:` triggers MAJOR bump
- Configurable commit parsers (Angular, Emoji, custom)
- Generates CHANGELOG.md from parsed commits

#### GitHub Actions Integration

Provides an official GitHub Action:

```yaml
- uses: python-semantic-release/python-semantic-release@v9
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
```

Can also run as CLI: `uv run semantic-release version`

#### Python Ecosystem Fit

Strong. Native pyproject.toml support, installable via pip/uv, Python-native CLI. Integrates with hatchling, setuptools, flit build backends.

#### Branch Protection Compatibility

Can push through branch protection using:
1. A Personal Access Token (PAT) with `repo` scope
2. A GitHub App installation token
3. Bypassing via ruleset exceptions for the Actions bot

#### Pros

- Python-native; installable via `uv add python-semantic-release`
- Mature Conventional Commits parsing with configurable parsers
- Automatic CHANGELOG.md generation
- Official GitHub Action available
- PyPI publishing built in (useful if Jerry ever publishes to PyPI)
- Active maintenance (v9.x, frequent releases)

#### Cons

- **No native JSON file support** -- cannot update plugin.json or marketplace.json without custom scripting
- **No nested JSON field support** -- cannot reach `plugins[0].version` in marketplace.json
- Relatively complex configuration for non-standard setups
- Designed around "one version, one package" mental model; multi-file sync with heterogeneous formats requires workarounds
- The gap between what it does well (Python packages) and what Jerry needs (mixed TOML + JSON) is significant

#### Jerry Fit Score: 5/10

The JSON limitation is a fundamental mismatch. PSR would handle pyproject.toml perfectly but requires bolted-on scripting for the two JSON files, defeating the purpose of a unified tool.

---

### Tool 2: bump-my-version (BMV)

**Repository:** [callowayproject/bump-my-version](https://github.com/callowayproject/bump-my-version)
**Language:** Python
**GitHub Stars:** ~600+ (as of early 2025)
**Last Major Release:** v0.x series (actively maintained, frequent releases)
**License:** MIT
**Lineage:** Fork/successor of the widely-used bump2version (now unmaintained)

#### Overview

bump-my-version (BMV) is a config-driven version bumping tool that excels at updating version strings across multiple files using configurable search/replace patterns. It is the maintained successor to bump2version. Its core strength is multi-file, multi-format version updates with regex and template support.

#### Multi-File Support

This is BMV's primary strength. Configuration supports an arbitrary number of files with different formats:

```toml
# pyproject.toml configuration for BMV
[tool.bumpversion]
current_version = "0.2.0"
commit = true
tag = true
tag_name = "v{new_version}"

[[tool.bumpversion.files]]
filename = "pyproject.toml"
search = 'version = "{current_version}"'
replace = 'version = "{new_version}"'

[[tool.bumpversion.files]]
filename = ".claude-plugin/plugin.json"
search = '"version": "{current_version}"'
replace = '"version": "{new_version}"'

[[tool.bumpversion.files]]
filename = ".claude-plugin/marketplace.json"
search = '"version": "{current_version}"'
replace = '"version": "{new_version}"'
# NOTE: This will match the FIRST occurrence of "version" in the file
```

**Nested JSON Handling:** BMV uses text-level search/replace, not JSON-aware parsing. For `marketplace.json` which has two version fields at different levels:

```json
{
  "version": "1.0.0",           // <-- marketplace schema version
  "plugins": [{
    "version": "0.1.0"          // <-- plugin version
  }]
}
```

This requires careful regex patterns or context-aware search strings:

```toml
# Strategy 1: Use surrounding context to disambiguate
[[tool.bumpversion.files]]
filename = ".claude-plugin/marketplace.json"
search = '"version": "{current_version}",\n  "description"'
replace = '"version": "{new_version}",\n  "description"'

# Strategy 2: Use regex mode
[[tool.bumpversion.files]]
filename = ".claude-plugin/marketplace.json"
regex = true
search = '("plugins"[^]]*"version":\\s*"){current_version}"'
replace = '\g<1>{new_version}"'
```

**Important consideration for Jerry:** The marketplace.json has TWO version fields that may need DIFFERENT values (marketplace schema version = 1.0.0, plugin version = 0.1.0). BMV can handle this with separate file entries using different search patterns, but it assumes a single `current_version` across the tool invocation. If the top-level `version` and `plugins[0].version` must be different, the top-level field should be excluded from BMV management and treated as a separate concern (it represents the marketplace manifest schema version, not the plugin version).

#### Conventional Commits Support

BMV does NOT natively parse commits. It is a version bumping tool, not a release automation tool. You tell it `bump major`, `bump minor`, or `bump patch`, and it does the bump. To get Conventional Commits integration, you pair it with:
1. A GitHub Actions workflow that parses commit messages
2. A tool like `commitizen` or `conventional-changelog` for commit parsing
3. A simple script that reads `git log` since last tag

Example integration:

```bash
# Parse commits and determine bump type
COMMITS=$(git log "$(git describe --tags --abbrev=0)"..HEAD --pretty=%s)
if echo "$COMMITS" | grep -qE "^(feat|fix|refactor|docs|test|chore)(\(.*\))?!:|BREAKING CHANGE:"; then
  BUMP_TYPE="major"
elif echo "$COMMITS" | grep -qE "^feat(\(.*\))?:"; then
  BUMP_TYPE="minor"
else
  BUMP_TYPE="patch"
fi

# Perform the bump
uv run bump-my-version bump "$BUMP_TYPE"
```

#### GitHub Actions Integration

No official GitHub Action, but easily integrated as a CLI tool:

```yaml
steps:
  - uses: actions/checkout@v5
    with:
      fetch-depth: 0
      token: ${{ secrets.PAT_TOKEN }}

  - name: Install UV
    uses: astral-sh/setup-uv@v5

  - name: Install bump-my-version
    run: uv tool install bump-my-version

  - name: Determine bump type from commits
    id: bump-type
    run: |
      # Parse conventional commits
      COMMITS=$(git log "$(git describe --tags --abbrev=0)"..HEAD --pretty=%s)
      if echo "$COMMITS" | grep -qE "^(feat|fix|refactor|docs|test|chore)(\(.*\))?!:|BREAKING CHANGE:"; then
        echo "type=major" >> $GITHUB_OUTPUT
      elif echo "$COMMITS" | grep -qE "^feat(\(.*\))?:"; then
        echo "type=minor" >> $GITHUB_OUTPUT
      else
        echo "type=patch" >> $GITHUB_OUTPUT
      fi

  - name: Bump version
    run: bump-my-version bump ${{ steps.bump-type.outputs.type }}

  - name: Push changes
    run: git push && git push --tags
```

#### Python Ecosystem Fit

Excellent. Pure Python, installable via `uv add --dev bump-my-version`. Configuration lives in pyproject.toml under `[tool.bumpversion]`. No Node.js or external runtime needed.

#### Branch Protection Compatibility

Same as PSR -- requires a PAT or GitHub App token to push version commits through branch protection. The workflow above uses `token: ${{ secrets.PAT_TOKEN }}` in the checkout step.

#### Pros

- **Best-in-class multi-file support** -- arbitrary number of files, any text format
- Python-native; installable via UV
- Configuration in pyproject.toml (no extra config files needed)
- Regex support for complex matching patterns
- Handles TOML, JSON, YAML, Python, Markdown -- any text format
- Atomic commits: bumps all files in a single commit
- Very lightweight -- does one thing well (version bumping)
- Active maintenance, regular releases
- Successor to widely-adopted bump2version

#### Cons

- **No Conventional Commits parsing** -- must be paired with external commit parsing
- **No changelog generation** -- separate tool needed (e.g., `git-cliff`, `conventional-changelog`)
- No official GitHub Action (trivial to script)
- Text-level search/replace means careful pattern crafting for JSON files with similar keys
- Lower GitHub star count (but this reflects focused scope, not quality)
- The marketplace.json two-version-field problem requires careful configuration

#### Jerry Fit Score: 8/10

BMV's multi-file strength directly addresses Jerry's core challenge. The lack of commit parsing is easily solved with a simple script in the GitHub Actions workflow. The text-based matching is sufficient for Jerry's JSON files with careful pattern design.

---

### Tool 3: release-please (Google)

**Repository:** [googleapis/release-please](https://github.com/googleapis/release-please)
**Language:** TypeScript/Node.js (but used via GitHub Action)
**GitHub Stars:** ~8,000+ (as of early 2025)
**Last Major Release:** v16.x (actively maintained by Google)
**License:** Apache-2.0

#### Overview

release-please is Google's open-source release automation tool. It works by maintaining a "release PR" that accumulates conventional commit messages. When merged, it creates a GitHub Release with auto-generated changelog. It supports many language ecosystems via "release types" and can update extra files via the `extra-files` configuration.

#### Multi-File Support

release-please supports updating additional files via `extra-files`:

```json
// .release-please-manifest.json
{
  ".": "0.2.0"
}
```

```json
// release-please-config.json
{
  "release-type": "python",
  "packages": {
    ".": {
      "extra-files": [
        {
          "type": "json",
          "filename": ".claude-plugin/plugin.json",
          "jsonpath": "$.version"
        },
        {
          "type": "json",
          "filename": ".claude-plugin/marketplace.json",
          "jsonpath": "$.plugins[0].version"
        }
      ]
    }
  }
}
```

**JSON Support:** release-please has a `json` extra-file type that supports JSONPath expressions. This means it can target `$.version` in plugin.json AND `$.plugins[0].version` in marketplace.json -- a significant advantage over text-based tools.

**Limitation:** The JSONPath support was added in later versions and has some documented edge cases. Complex nested structures may require testing. The top-level `version` in marketplace.json (the schema version "1.0.0") should be excluded since it represents a different semantic than the plugin version.

#### Conventional Commits Support

Excellent -- this is release-please's core feature:
- Parses all commits since last release
- Groups by type (feat, fix, chore, etc.)
- Generates structured CHANGELOG.md
- Determines semver bump automatically
- Creates a "Release PR" with version bump and changelog included

#### GitHub Actions Integration

First-class GitHub Action -- this is the primary usage mode:

```yaml
name: release-please
on:
  push:
    branches: [main]

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        with:
          release-type: python
          token: ${{ secrets.RELEASE_PLEASE_TOKEN }}
```

The workflow:
1. On every push to main, release-please updates/creates a "Release PR"
2. The Release PR accumulates changes and shows the pending version bump
3. When a human merges the Release PR, release-please creates a Git tag and GitHub Release
4. This tag can trigger the existing `release.yml` workflow

#### Python Ecosystem Fit

Moderate. release-please has a `python` release type that understands pyproject.toml (`setup.cfg` too). However:
- It is a Node.js tool (runs in GitHub Actions, so no local install needed)
- Configuration files are JSON (`.release-please-manifest.json`, `release-please-config.json`) rather than pyproject.toml
- It does not integrate with Python build tools directly

#### Branch Protection Compatibility

Good. release-please creates PRs (not direct pushes), so branch protection is respected by design:
1. Release PR is created/updated by the GitHub Action
2. CI runs on the Release PR like any other PR
3. Human merges the Release PR (respecting review requirements)
4. Post-merge, release-please creates the tag

This is the most branch-protection-friendly approach because it works WITH the PR model rather than around it.

#### Pros

- **PR-based workflow** -- naturally compatible with branch protection and code review
- **JSONPath support** for extra-files -- can target nested JSON fields
- Excellent Conventional Commits parsing and changelog generation
- Maintained by Google, large community (8k+ stars)
- No local tool installation needed (runs entirely in GitHub Actions)
- Generates polished, grouped changelogs
- Human-in-the-loop: Release PR must be explicitly merged
- Would integrate cleanly with existing `release.yml` (tag trigger)

#### Cons

- **Node.js/TypeScript ecosystem** -- not Python-native (but irrelevant for GHA-only usage)
- **Additional config files** -- requires `.release-please-manifest.json` and `release-please-config.json` at repo root
- JSONPath support for extra-files is newer and less battle-tested for complex structures
- The "Release PR" workflow may feel heavyweight for a small project
- Cannot be run locally as easily (primarily a CI tool)
- Two-step process (merge to main -> Release PR -> merge Release PR) adds ceremony
- If the marketplace.json top-level `version` field (schema version) needs to stay at 1.0.0 while `plugins[0].version` is bumped, configuration must be precise

#### Jerry Fit Score: 7/10

release-please is architecturally elegant and branch-protection-friendly, with real JSONPath support. The main downsides are the additional ceremony (Release PR workflow), extra config files, and non-Python toolchain. For a small OSS project, the Release PR model may add unnecessary process overhead.

---

### Tool 4: semantic-release (Node.js)

**Repository:** [semantic-release/semantic-release](https://github.com/semantic-release/semantic-release)
**Language:** Node.js
**GitHub Stars:** ~21,000+ (as of early 2025)
**Last Major Release:** v24.x (actively maintained)
**License:** MIT

#### Overview

semantic-release is the original and most widely adopted automated release tool. It is the Node.js progenitor that inspired python-semantic-release and release-please. It handles the full release lifecycle: version determination from commits, changelog generation, Git tagging, and publishing to package registries (npm, PyPI via plugins, GitHub Releases).

#### Multi-File Support

Via the `@semantic-release/exec` plugin, you can run arbitrary commands during the release lifecycle:

```json
// .releaserc.json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    ["@semantic-release/exec", {
      "prepareCmd": "python scripts/update_versions.py ${nextRelease.version}"
    }],
    ["@semantic-release/git", {
      "assets": [
        "pyproject.toml",
        ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
        "CHANGELOG.md"
      ]
    }],
    "@semantic-release/github"
  ]
}
```

With a custom Python script for the actual file updates:

```python
# scripts/update_versions.py
import json, sys, re
from pathlib import Path

version = sys.argv[1]

# Update pyproject.toml
pyproject = Path("pyproject.toml")
content = pyproject.read_text()
content = re.sub(r'version = ".*?"', f'version = "{version}"', content, count=1)
pyproject.write_text(content)

# Update plugin.json
plugin = Path(".claude-plugin/plugin.json")
data = json.loads(plugin.read_text())
data["version"] = version
plugin.write_text(json.dumps(data, indent=2) + "\n")

# Update marketplace.json (only plugin version, not schema version)
marketplace = Path(".claude-plugin/marketplace.json")
data = json.loads(marketplace.read_text())
data["plugins"][0]["version"] = version
marketplace.write_text(json.dumps(data, indent=2) + "\n")
```

#### Conventional Commits Support

Best-in-class. This is the tool that popularized the Conventional Commits -> semantic versioning pipeline:
- `@semantic-release/commit-analyzer` -- configurable commit parsing
- `@semantic-release/release-notes-generator` -- structured release notes
- `@semantic-release/changelog` -- CHANGELOG.md generation
- Extensive plugin ecosystem for customization

#### GitHub Actions Integration

Well-supported but requires Node.js setup:

```yaml
steps:
  - uses: actions/checkout@v5
    with:
      token: ${{ secrets.PAT_TOKEN }}

  - uses: actions/setup-node@v4
    with:
      node-version: 20

  - run: npm install -g semantic-release @semantic-release/exec @semantic-release/git @semantic-release/changelog

  - run: npx semantic-release
    env:
      GITHUB_TOKEN: ${{ secrets.PAT_TOKEN }}
```

#### Python Ecosystem Fit

Poor. semantic-release is a Node.js tool requiring:
- Node.js runtime in CI
- npm/npx for installation
- `.releaserc.json` or `package.json` configuration (not pyproject.toml)
- Adding Node.js tooling to a pure Python project

#### Branch Protection Compatibility

Same as PSR -- pushes directly; requires PAT or GitHub App token.

#### Pros

- Most mature and widely adopted release automation tool (~21k stars)
- Largest plugin ecosystem for customization
- Best Conventional Commits implementation
- Excellent changelog generation
- Via `@semantic-release/exec`, can run any command (including Python scripts)
- Very well documented with extensive community support

#### Cons

- **Requires Node.js** -- adds an entirely new runtime to a Python project
- **npm dependencies** -- adding package.json/node_modules to a Python project is jarring
- Configuration in `.releaserc.json` (not pyproject.toml)
- JSON file updates require custom scripting anyway (via `exec` plugin)
- Heavier CI setup (setup-node, npm install)
- Ecosystem mismatch: designed for npm packages, adapted for Python
- Overkill for Jerry's current needs

#### Jerry Fit Score: 4/10

While powerful and mature, the Node.js dependency is a significant cultural and operational mismatch for a Python-native project using UV. The multi-file support ultimately relies on custom scripting, which eliminates the advantage of using an off-the-shelf tool.

---

### Tool 5: Custom GitHub Actions Workflow

**Repository:** N/A (built in-house)
**Language:** Bash/Python scripts + GitHub Actions YAML
**GitHub Stars:** N/A
**Last Release:** N/A
**License:** N/A

#### Overview

A fully custom approach using GitHub Actions with inline or script-based version bumping. This gives maximum control but requires building and maintaining all components: commit parsing, version calculation, multi-file updates, changelog generation, tagging, and release creation.

#### Multi-File Support

Full control. A Python script can update any file in any format:

```python
#!/usr/bin/env python3
"""Bump version across all Jerry version files."""
import json
import re
import sys
from pathlib import Path

def bump_version(version: str, bump_type: str) -> str:
    major, minor, patch = map(int, version.split("."))
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    else:
        return f"{major}.{minor}.{patch + 1}"

def update_pyproject(new_version: str) -> None:
    path = Path("pyproject.toml")
    content = path.read_text()
    content = re.sub(
        r'^version = ".*?"',
        f'version = "{new_version}"',
        content,
        count=1,
        flags=re.MULTILINE,
    )
    path.write_text(content)

def update_plugin_json(new_version: str) -> None:
    path = Path(".claude-plugin/plugin.json")
    data = json.loads(path.read_text())
    data["version"] = new_version
    path.write_text(json.dumps(data, indent=2) + "\n")

def update_marketplace_json(new_version: str) -> None:
    path = Path(".claude-plugin/marketplace.json")
    data = json.loads(path.read_text())
    # Only bump the plugin version, not the marketplace schema version
    data["plugins"][0]["version"] = new_version
    path.write_text(json.dumps(data, indent=2) + "\n")

def main() -> None:
    bump_type = sys.argv[1]  # major, minor, patch
    # Read current version from pyproject.toml (single source of truth)
    content = Path("pyproject.toml").read_text()
    match = re.search(r'^version = "(.*?)"', content, re.MULTILINE)
    current = match.group(1)
    new_version = bump_version(current, bump_type)

    update_pyproject(new_version)
    update_plugin_json(new_version)
    update_marketplace_json(new_version)
    print(f"Bumped {current} -> {new_version}")

if __name__ == "__main__":
    main()
```

#### Conventional Commits Support

Must be implemented manually or via a lightweight library:

```bash
# Simple commit parsing in bash
determine_bump_type() {
    local commits=$(git log $(git describe --tags --abbrev=0 2>/dev/null || echo "")..HEAD --pretty=%s)

    if echo "$commits" | grep -qE "^(feat|fix|refactor|docs|test|chore)(\(.*\))?!:|BREAKING CHANGE:"; then
        echo "major"
    elif echo "$commits" | grep -qE "^feat(\(.*\))?:"; then
        echo "minor"
    elif echo "$commits" | grep -qE "^fix(\(.*\))?:"; then
        echo "patch"
    else
        echo "none"  # No version-bump-worthy commits
    fi
}
```

Or using Python with `commitizen` as a library for more robust parsing.

#### GitHub Actions Integration

Full control over the workflow:

```yaml
name: Version Bump
on:
  push:
    branches: [main]

jobs:
  bump:
    if: "!contains(github.event.head_commit.message, '[skip-bump]')"
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0
          token: ${{ secrets.PAT_TOKEN }}

      - name: Install UV
        uses: astral-sh/setup-uv@v5

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Determine bump type
        id: bump
        run: |
          COMMITS=$(git log "$(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~10")"..HEAD --pretty=%s)
          if echo "$COMMITS" | grep -qE "!:|BREAKING CHANGE"; then
            echo "type=major" >> $GITHUB_OUTPUT
          elif echo "$COMMITS" | grep -q "^feat"; then
            echo "type=minor" >> $GITHUB_OUTPUT
          elif echo "$COMMITS" | grep -q "^fix"; then
            echo "type=patch" >> $GITHUB_OUTPUT
          else
            echo "type=none" >> $GITHUB_OUTPUT
          fi

      - name: Bump version
        if: steps.bump.outputs.type != 'none'
        run: uv run python scripts/bump_version.py ${{ steps.bump.outputs.type }}

      - name: Commit and tag
        if: steps.bump.outputs.type != 'none'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          VERSION=$(grep -oP 'version = "\K[^"]+' pyproject.toml | head -1)
          git add pyproject.toml .claude-plugin/plugin.json .claude-plugin/marketplace.json
          git commit -m "chore(release): bump version to v${VERSION} [skip-bump]"
          git tag "v${VERSION}"
          git push && git push --tags
```

#### Python Ecosystem Fit

Perfect by definition -- written in Python, no external dependencies.

#### Branch Protection Compatibility

Same challenge as all push-based approaches: requires PAT or GitHub App token.

#### Pros

- **Maximum control** -- handle any edge case, any file format, any workflow
- Zero external dependencies beyond Python stdlib
- No new tools to learn or maintain (for Python developers)
- Configuration in Python (not YAML/JSON config files for third-party tools)
- Can be perfectly tailored to Jerry's exact needs
- No version lag waiting for upstream tool updates
- Easy to debug and modify

#### Cons

- **Must build and maintain everything** -- commit parsing, version calculation, changelog generation
- No community testing -- bugs are your own
- Commit parsing edge cases (Conventional Commits spec is non-trivial to parse correctly)
- No automatic changelog generation (must build or integrate separately)
- Risk of reinventing the wheel for common functionality
- More code to maintain long-term
- No standardized approach that new contributors would recognize

#### Jerry Fit Score: 6/10

Full control is appealing but the maintenance burden is real. For a project that is focused on building the Jerry framework (not on building release tooling), the custom approach trades initial flexibility for long-term maintenance cost. However, as a supplementary component (wrapping BMV or another tool), custom scripts are valuable.

---

### Tool 6: Commitizen

**Repository:** [commitizen-tools/commitizen](https://github.com/commitizen-tools/commitizen)
**Language:** Python
**GitHub Stars:** ~2,300 (see [Star Count Disclaimer](#star-count-disclaimer))
**Last Major Release:** v3.x series (actively maintained)
**License:** MIT

#### Overview

Commitizen is a Python-native tool that combines three capabilities in a single package: (1) conventional commit message validation (including a pre-commit hook), (2) automatic version bumping based on commit parsing, and (3) changelog generation. It was originally inspired by the Angular commit convention and the Node.js commitizen tool, but is a fully independent Python implementation. It is the only Python-native tool evaluated here that provides all three capabilities -- commit parsing, version bumping, and changelog -- without requiring supplementary tools or custom scripting.

The critic's feedback (CRIT-001, RT-1) identified commitizen as the most significant omission in the initial research. It was mentioned on line 204 as a potential pairing option for BMV but was never formally evaluated as a standalone tool.

#### Multi-File Support

Commitizen supports updating version strings across multiple files via the `version_files` configuration in pyproject.toml:

```toml
# pyproject.toml configuration for Commitizen
[tool.commitizen]
name = "cz_conventional_commits"
version = "0.2.0"
version_files = [
    "pyproject.toml:version",
    ".claude-plugin/plugin.json:version",
    ".claude-plugin/marketplace.json:version",
]
tag_format = "v$version"
update_changelog_on_bump = true
```

The `version_files` configuration supports colon-separated `filepath:key` patterns. For TOML files, it can target specific keys. For other file types, it uses a text-based search/replace mechanism, searching for the current version string and replacing it with the new version.

**Critical Limitation for Jerry:** Commitizen's `version_files` uses text-level search/replace for non-TOML files, similar to BMV. This means that for `marketplace.json`, which contains TWO `"version"` fields (the top-level schema version `"1.0.0"` and the plugin version `"0.1.0"`), commitizen will attempt to replace ALL occurrences of the current version string. If both fields happen to have the same value, both would be updated -- which is incorrect for Jerry since the top-level `version` represents the marketplace manifest schema version.

**Workaround:** Commitizen supports regex patterns in `version_files`:

```toml
version_files = [
    "pyproject.toml:version",
    ".claude-plugin/plugin.json:version",
    '.claude-plugin/marketplace.json:"version": "$version"',
]
```

However, regex-based disambiguation for the nested `plugins[0].version` in marketplace.json requires careful pattern crafting, similar to the challenges with BMV. Commitizen does not support JSONPath expressions.

#### Conventional Commits Support

Excellent -- this is one of commitizen's core features:
- Built-in conventional commits parser (`cz_conventional_commits`)
- `fix:` triggers PATCH bump
- `feat:` triggers MINOR bump
- `BREAKING CHANGE:` or `feat!:` triggers MAJOR bump
- Customizable commit rules via custom plugins
- Interactive commit message wizard (`cz commit`) that guides users through conventional commit format
- Validates commit messages against conventional commits spec

#### Pre-Commit Hook Integration

This is a significant differentiator. Commitizen provides a native pre-commit hook for commit message validation:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.31.0  # Use the latest release
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

This hook runs during `git commit` and rejects commit messages that do not follow the conventional commits format. This directly addresses the orchestration plan's Risk #7 ("Implementation conflicts with existing pre-commit hooks") by providing a Python-native solution that integrates with Jerry's existing pre-commit setup (`pre-commit>=4.5.1` in pyproject.toml `[dependency-groups]`).

#### Changelog Generation

Commitizen generates changelogs automatically during version bumps:

```bash
uv run cz bump --changelog
```

This produces a `CHANGELOG.md` with commits grouped by type (Features, Bug Fixes, etc.). The changelog format is configurable. For an OSS project like Jerry, this is a significant advantage over BMV, which requires a separate changelog tool.

#### Pre-Release Version Support

Commitizen has native support for pre-release versions:

```bash
# Create an alpha pre-release
uv run cz bump --prerelease alpha    # 0.2.0 -> 0.3.0a0

# Increment the pre-release
uv run cz bump --prerelease alpha    # 0.3.0a0 -> 0.3.0a1

# Promote to beta
uv run cz bump --prerelease beta     # 0.3.0a1 -> 0.3.0b0

# Promote to release candidate
uv run cz bump --prerelease rc       # 0.3.0b0 -> 0.3.0rc0

# Promote to final release
uv run cz bump                       # 0.3.0rc0 -> 0.3.0
```

This integrates cleanly with Jerry's release.yml pre-release detection: `prerelease: ${{ contains(needs.validate.outputs.version, '-') }}`.

**Note:** Python pre-release versions use PEP 440 format (`0.3.0a0`, `0.3.0b0`, `0.3.0rc0`) rather than SemVer pre-release format (`0.3.0-alpha.0`). The release.yml version regex (`^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$`) would need to be updated to also accept PEP 440 pre-release suffixes, or commitizen could be configured to use SemVer-style suffixes via a custom scheme.

#### GitHub Actions Integration

Commitizen can be integrated into GitHub Actions as a CLI tool:

```yaml
steps:
  - uses: actions/checkout@v5
    with:
      fetch-depth: 0
      token: ${{ secrets.PAT_TOKEN }}

  - name: Install UV
    uses: astral-sh/setup-uv@v5

  - name: Install commitizen
    run: uv tool install commitizen

  - name: Bump version
    run: |
      cz bump --changelog --yes
      git push && git push --tags
```

There is also a community-maintained GitHub Action (`commitizen-tools/commitizen-action`) that wraps the CLI:

```yaml
- uses: commitizen-tools/commitizen-action@master
  with:
    github_token: ${{ secrets.PAT_TOKEN }}
    changelog: true
```

#### Python Ecosystem Fit

Excellent. Commitizen is fully Python-native:
- Installable via `uv add --dev commitizen` or `uv tool install commitizen`
- Configuration lives in pyproject.toml under `[tool.commitizen]`
- No Node.js or external runtime needed
- Provides a `cz` CLI (conventional commit wizard, bump, changelog)
- Integrates with pre-commit (Python-native)

#### Branch Protection Compatibility

Same as BMV/PSR -- requires a PAT or GitHub App token for direct push. The commitizen-action uses a PAT for authentication.

#### Pros

- **Single-tool solution** -- combines commit parsing, version bumping, AND changelog generation
- Python-native; installable via UV
- Configuration in pyproject.toml (`[tool.commitizen]`)
- **Pre-commit hook** for commit message validation (directly addresses orchestration Risk #7)
- Interactive commit wizard (`cz commit`) helps enforce conventional commits at authoring time
- Automatic changelog generation
- Pre-release version support built in
- Larger community than BMV (~2,300 stars vs ~600+)
- Active maintenance (v3.x, regular releases)
- Community-maintained GitHub Action available

#### Cons

- **Text-based version_files** -- same limitation as BMV for JSON disambiguation; no JSONPath support
- **marketplace.json dual-version problem** -- same challenge as BMV; requires careful pattern to avoid updating the wrong version field
- Less focused than BMV -- tries to do more, which means more surface area for opinions and configuration
- The `cz commit` wizard is useful for individual developers but less relevant for CI/CD-driven version bumps
- Changelog format is opinionated (though configurable)
- Pre-release PEP 440 format may conflict with SemVer expectations in release.yml

#### Jerry Fit Score: 7.5/10

Commitizen's single-tool approach is compelling -- it addresses BMV's primary weakness (no commit parsing or changelog) while maintaining Python-native, UV-compatible, pyproject.toml-configured operation. The pre-commit hook is a direct answer to orchestration Risk #7. However, it shares BMV's JSON disambiguation limitation, and the marketplace.json dual-version problem requires the same careful pattern crafting. The pre-release PEP 440 vs SemVer format discrepancy is a minor integration concern. The score places it between BMV (8/10, for superior multi-file control) and release-please (7/10, for JSONPath superiority on JSON files), reflecting that commitizen trades BMV's focused precision for broader but slightly less configurable multi-file handling.

---

## Comparison Matrix

### Feature Comparison

| Feature | python-semantic-release | bump-my-version | release-please | semantic-release (Node) | commitizen | Custom GHA |
|---------|:-:|:-:|:-:|:-:|:-:|:-:|
| **Multi-file support** | Limited (TOML + Python only) | Excellent (any text format) | Good (via extra-files) | Via exec plugin (custom script) | Good (`version_files`) | Full (custom code) |
| **JSON file updates** | No native support | Text-based search/replace | JSONPath support | Via custom script | Text-based search/replace | Full JSON API |
| **Nested JSON (`plugins[0].version`)** | No | Regex patterns (fragile) | JSONPath (robust) | Via custom script | Regex patterns (fragile) | Full JSON API |
| **Conventional Commits parsing** | Excellent (built-in) | None (external needed) | Excellent (built-in) | Excellent (built-in) | Excellent (built-in) | Manual implementation |
| **Changelog generation** | Yes (automatic) | No | Yes (automatic, excellent) | Yes (automatic, excellent) | Yes (automatic) | Manual implementation |
| **Pre-release versions** | Yes (`prerelease_token`) | Yes (`serialize`/`parse` config) | Yes (`prerelease-type`) | Yes (branches config) | Yes (`--prerelease` flag, PEP 440) | Manual implementation |
| **Pre-commit integration** | No native hook | No native hook | No native hook (use `commitlint`) | No (use `commitlint`, Node.js) | Yes (native `commit-msg` hook) | Manual (custom hook) |
| **GitHub Actions native** | Official Action | CLI in workflow | Official Action | Community Actions | Community Action | Custom YAML |
| **Python-native** | Yes | Yes | No (Node.js, but GHA-only) | No (Node.js required) | Yes | Yes (Python scripts) |
| **pyproject.toml config** | Yes (`[tool.semantic_release]`) | Yes (`[tool.bumpversion]`) | No (separate JSON files) | No (`.releaserc.json`) | Yes (`[tool.commitizen]`) | N/A |
| **UV compatible** | Yes (`uv add`) | Yes (`uv add`) | N/A (GHA-only) | Requires npm | Yes (`uv add`) | N/A |
| **Branch protection friendly** | PAT/App token needed | PAT/App token needed | PR-based (naturally compatible) | PAT/App token needed | PAT/App token needed | PAT/App token needed |
| **Maturity (GitHub stars)** | ~2,000 | ~600+ | ~8,000+ | ~21,000+ | ~2,300 | N/A |
| **Maintenance status** | Active (v9.x) | Active (frequent) | Active (Google-backed) | Active (v24.x) | Active (v3.x) | Self-maintained |
| **Learning curve** | Medium | Low | Medium | Medium-High | Low-Medium | Low (but high build cost) |

*See [Star Count Disclaimer](#star-count-disclaimer) for data freshness note.*

### Jerry-Specific Constraint Assessment

| Constraint | PSR | BMV | release-please | semantic-release (Node) | commitizen | Custom |
|------------|:-:|:-:|:-:|:-:|:-:|:-:|
| Updates pyproject.toml | YES | YES | YES | Via script | YES | YES |
| Updates plugin.json | NO (native) | YES | YES (JSONPath) | Via script | YES (text-based) | YES |
| Updates marketplace.json `version` | NO (native) | YES (pattern) | YES (JSONPath) | Via script | YES (text-based) | YES |
| Updates marketplace.json `plugins[0].version` | NO | PARTIAL (regex) | YES (JSONPath) | Via script | PARTIAL (regex) | YES |
| No Node.js required | YES | YES | N/A* | NO | YES | YES |
| Config in pyproject.toml | YES | YES | NO | NO | YES | N/A |
| Works with existing release.yml (tag trigger) | YES | YES | YES | YES | YES | YES |
| Branch protection compatible | PAT | PAT | PR-native | PAT | PAT | PAT |
| Pre-release version support | YES | YES (`serialize`/`parse`) | YES (`prerelease-type`) | YES | YES (PEP 440 format) | Manual |
| Pre-commit commit-msg hook | NO | NO | NO (use `commitlint`) | NO (use `commitlint`) | YES (native) | Manual |

*release-please runs in GitHub Actions (Node.js is available in CI runners regardless)*

---

## L2: Architectural Implications

### Single Source of Truth (SSOT) Strategy

Regardless of tool choice, the SSOT for version should be **pyproject.toml**. This is because:

1. It is the Python ecosystem standard for package version
2. It is already used by the build system (hatchling)
3. `jerry --version` derives from this value
4. The `release.yml` workflow already validates against it

The JSON files (plugin.json, marketplace.json) are **derived** -- their versions should be synchronized from pyproject.toml during the bump process.

**Implication for marketplace.json:** The top-level `version` field (currently "1.0.0") represents the marketplace manifest schema version, NOT the plugin version. This field should likely be managed separately (or left as-is) since it follows a different versioning lifecycle than the plugin itself. Only `plugins[0].version` should be synchronized with pyproject.toml.

### Architecture Decision: Hybrid Approach

The analysis points toward a hybrid approach:

```
Conventional Commits (input)
         |
         v
  Commit Parser (determines bump type: major/minor/patch)
         |
         v
  Version Bumper (updates all files atomically)
         |
         v
  Git Commit + Tag
         |
         v
  Existing release.yml (triggered by tag)
```

The optimal architecture for Jerry is:

1. **BMV for file updates** -- handles the mechanical multi-file bumping
2. **Custom GHA workflow for orchestration** -- handles commit parsing, determines bump type, invokes BMV, handles branch protection
3. **Existing release.yml remains unchanged** -- triggered by the version tag that BMV creates

This separates concerns:
- BMV does what it does best (multi-file version bumping)
- The GHA workflow handles what BMV cannot (commit parsing, CI/CD orchestration)
- The existing release pipeline is preserved (no disruption)

### Alternative Architecture A: commitizen (Single-Tool)

If the team prefers a single-tool approach that eliminates custom commit parsing:

1. **commitizen for everything** -- commit message validation (pre-commit hook), commit parsing, version bumping, changelog generation
2. **`version_files`** config for multi-file updates
3. **Existing release.yml** triggered by the commitizen-created tag

This reduces maintenance burden but introduces:
- Same text-based JSON disambiguation challenges as BMV
- PEP 440 pre-release format may need adaptation for SemVer tags
- Slightly less flexible multi-file configuration than BMV

### Alternative Architecture B: release-please

If the team prefers a more opinionated, less custom approach:

1. **release-please for everything** -- commit parsing, version bumping, changelog, Release PR
2. **Extra-files config** for JSON updates (with JSONPath for nested fields)
3. **Existing release.yml** triggered by the release-please tag

This is architecturally cleaner but introduces:
- Additional config files (`.release-please-manifest.json`, `release-please-config.json`)
- The Release PR workflow (adds ceremony)
- Google ecosystem dependency

### Risk Assessment

| Risk | BMV + Custom GHA | commitizen | release-please |
|------|:-:|:-:|:-:|
| Tool abandonment | Medium (smaller community) | Low-Medium (~2,300 stars, active) | Low (Google-backed) |
| Breaking changes in tool | Low (simple API) | Low-Medium (larger surface area) | Medium (fast-moving) |
| Commit parsing bugs | Medium (custom code) | Low (built-in, battle-tested) | Low (battle-tested) |
| JSON update failures | Low (well-tested patterns) | Low (text-based, same as BMV) | Low-Medium (JSONPath newer) |
| Maintenance burden | Medium (custom workflow) | Low (single tool) | Low (mostly config) |
| Contributor familiarity | Medium | Medium-High (well-known in Python) | High (widely known) |
| CI complexity | Low (simple workflow) | Low (simple CLI) | Low (official action) |
| Pre-commit integration | Manual (no native hook) | Low (native hook) | Manual (need `commitlint`) |

### Pre-Release Versioning

Jerry's existing `release.yml` already supports pre-release versions. The version validation regex accepts `X.Y.Z-suffix` patterns, and the GitHub Release step sets `prerelease: ${{ contains(needs.validate.outputs.version, '-') }}`. This means any tool chosen must support pre-release version workflows.

#### Tool Pre-Release Capabilities

| Tool | Pre-Release Support | Format | Configuration |
|------|---------------------|--------|---------------|
| **BMV** | Yes, native | Configurable via `serialize`/`parse` | `parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(-(?P<pre_l>[a-zA-Z]+)\\.(?P<pre_n>\\d+))?"` plus matching `serialize` entries. BMV supports arbitrary pre-release part names and increment sequences. |
| **commitizen** | Yes, native | PEP 440 (`0.3.0a0`, `0.3.0b0`, `0.3.0rc0`) | `cz bump --prerelease alpha\|beta\|rc`. Clean CLI interface. PEP 440 format may need adaptation for SemVer-style tags. |
| **PSR** | Yes, native | Configurable (`prerelease_token`) | Supports `--prerelease` flag with configurable token (alpha, beta, rc). Generates versions like `0.3.0-alpha.1`. |
| **release-please** | Yes, config-based | SemVer (`0.3.0-alpha.1`) | `prerelease-type: alpha` in config. Creates pre-release tags and GitHub Releases marked as pre-release. |
| **semantic-release (Node)** | Yes, via branches | SemVer | Configure pre-release branches: `{ name: "beta", prerelease: true }`. Generates `0.3.0-beta.1` on pushes to the beta branch. |
| **Custom** | Manual | Any | Must implement version parsing/formatting for pre-release segments. |

#### Jerry Consideration

Jerry uses SemVer-style pre-release tags (e.g., `v0.3.0-beta.1`) as evidenced by the release.yml regex `^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$`. Commitizen's default PEP 440 format (`0.3.0b0`) would not match this pattern without either (a) configuring commitizen to use a custom version scheme with SemVer pre-release format, or (b) updating release.yml to accept both formats. BMV and PSR natively produce SemVer-compatible pre-release tags, making them more compatible out of the box.

### Pre-Commit Integration Assessment

Jerry already includes `pre-commit>=4.5.1` in its `[dependency-groups]` dev dependencies (pyproject.toml line 116). The orchestration plan for EN-108 identifies pre-commit integration as Risk #7: "Implementation conflicts with existing pre-commit hooks." Conventional commit message enforcement via a `commit-msg` pre-commit hook is a best practice for projects adopting Conventional Commits.

#### Tool Pre-Commit Capabilities

| Tool | Pre-Commit Hook | Type | Notes |
|------|----------------|------|-------|
| **commitizen** | YES (native) | `commit-msg` stage | Provides `commitizen` hook that validates commit messages against conventional commits spec. Python-native, integrates with Jerry's existing pre-commit setup. Also provides `commitizen-branch` hook for branch naming conventions. |
| **commitlint** | YES (Node.js) | `commit-msg` stage | Industry standard for commit message linting. Requires Node.js runtime, which adds a dependency Jerry does not otherwise need for local development. |
| **BMV** | NO | N/A | BMV does not validate commit messages. Would need to pair with commitizen or commitlint for commit-msg hooks. |
| **PSR** | NO | N/A | PSR does not provide a pre-commit hook. |
| **release-please** | NO | N/A | release-please is a CI-only tool; it does not operate locally. |

#### Recommendation for Pre-Commit

Regardless of which version bumping tool is chosen, **commitizen's pre-commit hook** is the recommended solution for commit message validation. It is Python-native, requires no Node.js, and integrates directly with Jerry's existing pre-commit infrastructure. Even if BMV is chosen for version bumping, commitizen can be installed solely for its pre-commit `commit-msg` hook:

```yaml
# .pre-commit-config.yaml addition
repos:
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.31.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

This is a modular approach: BMV handles file bumping, and commitizen handles commit message enforcement. Alternatively, if commitizen is chosen as the primary tool, both capabilities are unified in a single dependency.

### Integration with Existing CI/CD

Jerry's current CI/CD:
- **ci.yml**: Runs on all pushes and PRs to main (lint, type-check, security, test)
- **release.yml**: Triggers on `v*` tags; validates version, builds plugin archive, creates GitHub Release

The version bumping workflow should:
1. Trigger on push to `main` (after PR merge)
2. Skip if the commit is itself a version bump (prevent infinite loops)
3. Parse commits since last tag for bump type
4. Update version files
5. Commit and create tag
6. The tag triggers `release.yml` automatically

**Infinite Loop Prevention:** The version bump commit must be detectable. Options:
- Include `[skip-bump]` or `[skip ci]` in the commit message
- Use a specific committer identity that the workflow checks for
- Use `if: "!contains(github.event.head_commit.message, 'chore(release)')"` in the workflow

### Trade-offs Summary

| Approach | Control | Maintenance | Community | Changelog | Pre-commit | Jerry Fit |
|----------|---------|-------------|-----------|-----------|------------|-----------|
| BMV + Custom GHA | High | Medium | Medium | Separate tool needed | Separate tool needed | Best |
| commitizen | Medium-High | Low | Medium-High | Built in | Built in (native hook) | Very Good |
| release-please | Medium | Low | High | Built in (excellent) | Separate tool needed | Good |
| PSR | Medium | Low | Medium | Built in | Separate tool needed | Moderate |
| Custom only | Maximum | High | None | Manual | Manual | Adequate |
| semantic-release (Node) | High | Low | High | Built in (excellent) | Via `commitlint` (Node.js) | Poor (ecosystem mismatch) |

---

## Recommendation

### Primary Recommendation: bump-my-version + Custom GitHub Actions Workflow

**Confidence: High**

The recommended approach for Jerry is:

1. **bump-my-version** (`[tool.bumpversion]` in pyproject.toml) for multi-file version bumping
2. **Custom GitHub Actions workflow** (`version-bump.yml`) for Conventional Commits parsing and orchestration
3. **Existing `release.yml`** remains unchanged, triggered by the version tag

**Rationale:**
- BMV is the only tool that natively handles multi-file updates across TOML and JSON formats without requiring Node.js
- Python-native, UV-installable, configured in pyproject.toml
- The custom GHA wrapper adds only ~40 lines of YAML for commit parsing -- far less than building a full version bumper from scratch
- Clean separation of concerns: BMV bumps, GHA orchestrates, release.yml publishes
- No new ecosystem dependencies (no Node.js, no additional config files beyond pyproject.toml)
- The `[skip-bump]` pattern prevents infinite loops cleanly

**Suggested BMV Configuration:**

```toml
[tool.bumpversion]
current_version = "0.2.0"
commit = true
tag = true
tag_name = "v{new_version}"
commit_message = "chore(release): bump version to v{new_version} [skip-bump]"

[[tool.bumpversion.files]]
filename = "pyproject.toml"
search = 'version = "{current_version}"'
replace = 'version = "{new_version}"'

[[tool.bumpversion.files]]
filename = ".claude-plugin/plugin.json"
search = '"version": "{current_version}"'
replace = '"version": "{new_version}"'

# Only bump the plugin version in marketplace.json, not the top-level schema version
[[tool.bumpversion.files]]
filename = ".claude-plugin/marketplace.json"
search = '"source": "./",\n      "version": "{current_version}"'
replace = '"source": "./",\n      "version": "{new_version}"'
```

### Changelog Strategy for the Recommended Approach

BMV does not generate changelogs. For an OSS project like Jerry, a CHANGELOG.md is standard practice and expected by contributors and users. The recommended changelog strategy for the BMV + Custom GHA approach is:

**Option A: git-cliff (Recommended)**

[git-cliff](https://github.com/orhun/git-cliff) is a Rust-based changelog generator that parses Conventional Commits and produces configurable CHANGELOG.md output. It is fast, well-maintained (~4,000 stars), and available as a standalone binary (no Rust toolchain needed at runtime). In CI, it can be installed via GitHub Action:

```yaml
- name: Generate changelog
  uses: orhun/git-cliff-action@v4
  with:
    config: cliff.toml
    args: --latest --strip header
  env:
    OUTPUT: CHANGELOG.md
```

git-cliff integrates cleanly into the BMV workflow: after BMV bumps versions and before the commit is created, git-cliff generates the changelog, and both changes are committed together.

**Option B: commitizen as changelog-only**

If commitizen is already installed for its pre-commit hook (see Pre-Commit Integration Assessment above), its changelog generation can also be used: `uv run cz changelog`. This avoids adding another tool, but the changelog format is less configurable than git-cliff.

**Option C: Adopt commitizen as the primary tool**

If changelog generation is a priority from day one, this strengthens the case for using commitizen as the primary version bumping tool instead of BMV, since commitizen provides changelog generation built in. See the "Strong Alternative" section below.

### Strong Alternative: commitizen (Single-Tool Approach)

Commitizen (scored 7.5/10) deserves special consideration as an alternative to the BMV + Custom GHA hybrid. It provides a single-tool solution that combines:
- Conventional Commits parsing (eliminates the need for custom commit parsing in GHA)
- Version bumping with multi-file support (via `version_files`)
- Changelog generation (built in)
- Pre-commit hook for commit message validation (addresses orchestration Risk #7)

Commitizen would be the preferred choice if:
- The team values a single-tool approach over a multi-tool hybrid
- Changelog generation is a priority from day one
- Pre-commit commit message enforcement is desired
- The marketplace.json dual-version problem can be solved with careful `version_files` regex patterns

The primary trade-off vs. BMV is that commitizen's `version_files` is slightly less flexible than BMV's `[[tool.bumpversion.files]]` for complex text patterns, and BMV's focused scope means fewer surprises in its behavior. However, commitizen's broader feature set (commit parsing + changelog + pre-commit) eliminates the need for custom scripting and supplementary tools, reducing overall maintenance burden.

### Runner-Up: release-please

If the team prefers a more opinionated approach with less custom code, release-please is the strong alternative. It would be the preferred choice if:
- The Release PR workflow is desirable (human approval before each release)
- Automatic changelog generation is a priority from day one
- The team wants to minimize custom CI/CD code
- JSONPath-based JSON updates are preferred over text-based pattern matching

### Not Recommended

- **python-semantic-release**: JSON file limitation is a fundamental mismatch
- **semantic-release (Node.js)**: Ecosystem mismatch for a Python project
- **Fully custom**: Too much maintenance burden for the value delivered

---

## References

### Tool Documentation

| Tool | Documentation URL |
|------|-------------------|
| bump-my-version | https://callowayproject.github.io/bump-my-version/ |
| commitizen | https://commitizen-tools.github.io/commitizen/ |
| python-semantic-release | https://python-semantic-release.readthedocs.io/en/latest/ |
| release-please | https://github.com/googleapis/release-please |
| semantic-release | https://semantic-release.gitbook.io/semantic-release/ |
| git-cliff | https://git-cliff.org/ |
| Conventional Commits | https://www.conventionalcommits.org/en/v1.0.0/ |
| Semantic Versioning | https://semver.org/ |

### Tool Repositories

| Tool | Repository | Stars (approx) |
|------|-----------|---------------------------|
| bump-my-version | https://github.com/callowayproject/bump-my-version | ~600+ |
| commitizen | https://github.com/commitizen-tools/commitizen | ~2,300 |
| python-semantic-release | https://github.com/python-semantic-release/python-semantic-release | ~2,000 |
| release-please | https://github.com/googleapis/release-please | ~8,000+ |
| semantic-release | https://github.com/semantic-release/semantic-release | ~21,000+ |
| git-cliff | https://github.com/orhun/git-cliff | ~4,000+ |
| bump2version (predecessor, archived) | https://github.com/c4urself/bump2version | ~1,500 |
| commitizen-action | https://github.com/commitizen-tools/commitizen-action | Community GHA |

### Star Count Disclaimer

GitHub star counts cited in this document are approximate and based on the researcher's training data (cutoff: May 2025). Star counts may have shifted since that date. They are used directionally to indicate relative community size and adoption, not as precise metrics. **Verify current star counts on GitHub before making final decisions.** In particular, bump-my-version has likely grown beyond the ~600 cited here, and release-please may exceed 9,000.

### Jerry Project Context

| Artifact | Path |
|----------|------|
| CI Pipeline | `.github/workflows/ci.yml` |
| Release Pipeline | `.github/workflows/release.yml` |
| Plugin Manifest Validator | `scripts/validate_plugin_manifests.py` |
| pyproject.toml | `pyproject.toml` |
| Plugin Manifest | `.claude-plugin/plugin.json` |
| Marketplace Manifest | `.claude-plugin/marketplace.json` |
| EN-108 Enabler | `projects/PROJ-001-oss-release/work/.../EN-108-version-bumping-strategy.md` |
| Orchestration Plan | `EN-108-version-bumping-strategy/orchestration/ORCHESTRATION_PLAN.md` |

### Standards

| Standard | URL |
|----------|-----|
| Conventional Commits v1.0.0 | https://www.conventionalcommits.org/en/v1.0.0/ |
| Semantic Versioning 2.0.0 | https://semver.org/spec/v2.0.0.html |
| Keep a Changelog | https://keepachangelog.com/en/1.1.0/ |

---

## Methodology Note

This research was conducted using the researcher's training knowledge (cutoff: May 2025). Web-facing research tools (Context7, WebSearch, WebFetch) were unavailable during both sessions. All tool evaluations are based on established documentation and publicly available information as of that date. GitHub star counts and release versions should be verified against current data before final decision-making (see [Star Count Disclaimer](#star-count-disclaimer)).

**v2 Revision:** This document was revised based on adversarial critique feedback (CRIT-001, score 0.843). The following changes were applied:
- **CRITICAL:** Added full evaluation of commitizen (Tool 6) -- the single largest gap identified by the critic
- **HIGH:** Added pre-release versioning discussion and comparison matrix row
- **HIGH:** Added pre-commit integration assessment addressing orchestration Risk #7
- **HIGH:** Fixed bash script bug (piped `grep -q` consuming stdin) in commit parsing example
- **HIGH:** Fixed UV violation (`pip install` -> `uv tool install`) in GHA workflow example
- **MEDIUM:** Added concrete changelog strategy (git-cliff recommendation) for the BMV + Custom GHA approach
- **LOW:** Added star count disclaimer with data freshness note

---

*Document ID: EN-108-TASK-001-R001*
*Version: 2 (v2 -- revised per CRIT-001)*
*PS ID: en108-task001*
*Entry: e-001*
*Agent: ps-researcher v2.2.0*
