# Analysis: Version Locations and Sync Strategy

> **PS ID:** en108-task002 | **Entry:** e-002 | **Type:** Gap Analysis
> **Agent:** ps-analyst v2.2.0 | **Date:** 2026-02-12
> **Project:** PROJ-001-oss-release | **Enabler:** EN-108 Version Bumping Strategy

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | ELI5 overview of findings |
| [L1: Technical Analysis](#l1-technical-analysis) | Detailed catalog and semantics |
| [L2: Architectural Implications](#l2-architectural-implications) | SSOT strategy, sync mechanism, risks |
| [Evidence Summary](#evidence-summary) | Tabular evidence from actual files |
| [Gap Analysis](#gap-analysis) | Current vs desired state |
| [Recommendations](#recommendations) | Prioritized action items |
| [References](#references) | Source files and citations |

---

## L0: Executive Summary

The Jerry project currently stores version numbers in **7 framework-level locations** across 5 files (plus 5 additional secondary/independent version fields and 6 skill-level versions), and the framework versions are **diverged from each other** -- the three primary version strings are `1.0.0`, `0.2.0`, and `0.1.0`, each appearing in different files with no automation keeping them synchronized. When a developer bumps a version, they must remember to update each location manually, which has clearly already failed (the values are out of sync today).

The root cause is that no Single Source of Truth (SSOT) has been defined, and no build-time or CI mechanism exists to propagate a version change from one authoritative file to the others. Additionally, the project has no `CHANGELOG.md` and the `__version__` strings in Python source code are hardcoded duplicates rather than being derived from the package metadata at runtime.

The solution path is well-defined: designate `pyproject.toml` as the SSOT (it is the Python packaging standard and already read by `uv`, `pip`, and the release workflow), then create a version-sync script that updates the other locations from that single value. This script should run as a pre-commit hook or CI check. The `__version__` strings in Python modules should be replaced with runtime reads from `importlib.metadata`, and existing tests that hardcode version values must be updated to avoid breakage. Implementation requires coordinating changes across 8+ locations in multiple formats (Python, JSON, Markdown), so while the strategy is conceptually simple, the execution demands care. Skill-level versions are intentionally independent and do NOT need to be synchronized with the framework version.

---

## L1: Technical Analysis

### Step 1: Complete Version Location Catalog

#### Primary Version Fields (Framework-Level)

| # | File | Field/Path | Current Value | Semantic Meaning |
|---|------|-----------|---------------|------------------|
| 1 | `pyproject.toml` | `project.version` | `"0.2.0"` | Python package version; read by `uv`, `pip`, `hatch` build system |
| 2 | `.claude-plugin/plugin.json` | `version` | `"0.1.0"` | Claude Code plugin manifest version |
| 3 | `.claude-plugin/marketplace.json` | `version` (top-level) | `"1.0.0"` | Marketplace manifest version (schema/format version?) |
| 4 | `.claude-plugin/marketplace.json` | `plugins[0].version` | `"0.1.0"` | Individual plugin version within marketplace listing |
| 5 | `src/__init__.py` | `__version__` | `"0.1.0"` | Python package version exposed at runtime |
| 6 | `src/interface/cli/parser.py` | `__version__` | `"0.1.0"` | CLI `--version` output string |
| 7 | `src/transcript/__init__.py` | `__version__` | `"0.1.0"` | Transcript bounded context version |

#### Secondary Version Fields (Non-Framework, Independent)

| # | File | Field/Path | Current Value | Semantic Meaning |
|---|------|-----------|---------------|------------------|
| 8 | `.claude/settings.json` | `version` | `"1.0"` | Claude Code settings schema version (NOT framework version) |
| 9 | `docs/schemas/session_context.json` | `version` | `"1.0.0"` | Session context schema version (NOT framework version) |
| 10 | `skills/transcript/schemas/DOMAIN-SCHEMA.json` | `version` | `"1.0.0"` | Transcript domain schema version (NOT framework version) |
| 11 | `CLAUDE.md` | inline text | `v0.1.0` | Documentation reference to CLI version |
| 12 | `.claude/statusline.py` | `__version__` (line 60) | `"2.1.0"` | ECW Status Line utility version (standalone component, NOT framework version) |

**Finding F-003 (decision):** `.claude/statusline.py` contains `__version__ = "2.1.0"` at line 60 and `Version: 2.1.0` in its docstring at line 6. This is a **self-contained, single-file utility** (ECW Status Line) that is designed to be copied independently to `~/.claude/statusline.py`. It has its own feature set, its own version lifecycle, and zero dependencies on the Jerry framework. **Decision: This version is intentionally independent (Domain E: Utility Versions) and SHOULD NOT be synchronized with the framework version.** The sync script should explicitly exclude this file. If the statusline is ever extracted into a separate distribution, its version will continue its own trajectory.

#### Skill-Level Versions (Intentionally Independent)

| Skill | SKILL.md YAML `version` | Display Version | Notes |
|-------|------------------------|-----------------|-------|
| worktracker | `1.1.0` | 1.1.0 | Independent skill lifecycle |
| orchestration | `2.1.0` | 2.1.0 | Independent skill lifecycle |
| problem-solving | `2.1.0` | 2.1.0 | Independent skill lifecycle |
| transcript | `2.5.0` | 2.4.1 (display mismatch!) | YAML says 2.5.0, display line says 2.4.1 |
| nasa-se | `1.1.0` | 1.1.0 | Independent skill lifecycle |
| architecture | `1.0.0` | n/a | No display version line |

**Finding F-001 (gap):** The transcript SKILL.md has a YAML frontmatter version of `2.5.0` but the display line reads `2.4.1`. This is an internal inconsistency within one file.

### Step 2: Version Semantics Analysis

#### Three Distinct Version Domains

**Domain A: Framework/Package Version** (SHOULD be synchronized)
- `pyproject.toml` `project.version` -- the Python package version
- `.claude-plugin/plugin.json` `version` -- the plugin version exposed to Claude Code
- `.claude-plugin/marketplace.json` `plugins[0].version` -- the version of the jerry-framework plugin in the marketplace
- `src/__init__.py` `__version__` -- runtime-accessible package version
- `src/interface/cli/parser.py` `__version__` -- CLI `jerry --version` output
- `src/transcript/__init__.py` `__version__` -- transcript BC version (should match framework)
- `CLAUDE.md` inline reference

These 7 locations all describe the same thing: "What version of Jerry is this?" They MUST be synchronized.

**Domain B: Marketplace Manifest Version** (AMBIGUOUS)
- `.claude-plugin/marketplace.json` top-level `version` field is currently `1.0.0`
- This is semantically unclear. The marketplace schema describes it as the "Semantic version" of the marketplace manifest itself.
- Investigation: The marketplace.json represents a "collection of plugins." Its top-level version could mean:
  - **Interpretation 1:** The marketplace schema/format version (like a `schema_version`). Under this interpretation, `1.0.0` means "this is format version 1 of the marketplace manifest."
  - **Interpretation 2:** The overall marketplace/bundle version, which should track the framework version.
- **Finding F-002 (decision-needed):** The marketplace schema (`schemas/marketplace.schema.json`) describes the `version` field generically as "Semantic version" without specifying whether it tracks the plugin version or is independent. Given that the marketplace currently contains exactly one plugin (jerry-framework), the most pragmatic approach is to synchronize it with the framework version. If the marketplace ever hosts multiple plugins with independent lifecycles, this decision should be revisited.

**Domain C: Schema/Config Versions** (Intentionally Independent)
- `.claude/settings.json` `version: "1.0"` -- Claude Code settings file format version
- `docs/schemas/session_context.json` `version: "1.0.0"` -- session handoff schema version
- `skills/transcript/schemas/DOMAIN-SCHEMA.json` `version: "1.0.0"` -- transcript domain schema version
- These are schema format versions with their own independent lifecycle. They SHOULD NOT be synchronized with the framework version.

**Domain D: Skill Versions** (Intentionally Independent)
- Each `skills/*/SKILL.md` has its own YAML `version` field
- Skills evolve independently (worktracker at 1.1.0, orchestration at 2.1.0, etc.)
- These SHOULD NOT be synchronized with the framework version.

**Domain E: Utility Versions** (Intentionally Independent)
- `.claude/statusline.py` `__version__ = "2.1.0"` -- ECW Status Line utility
- This is a standalone, single-file utility designed for independent distribution (copy to `~/.claude/`)
- It has zero framework dependencies (stdlib only) and its own feature lifecycle
- This SHOULD NOT be synchronized with the framework version
- The sync script must explicitly exclude this file to avoid accidental version overwrites

### Step 3: Single Source of Truth Evaluation

| Candidate | Authority | Tooling Support | Derivability | Recommendation |
|-----------|-----------|----------------|--------------|----------------|
| `pyproject.toml` | **HIGH** -- PEP 621 standard; Python packaging metadata spec | `uv`, `pip`, `hatch`, `importlib.metadata` all read it natively | All other files can derive from it via script | **RECOMMENDED SSOT** |
| `.claude-plugin/plugin.json` | MEDIUM -- Claude Code plugin standard | Claude Code reads it; no write tooling | pyproject.toml cannot easily derive from it | Not recommended |
| `.claude-plugin/marketplace.json` | LOW -- marketplace distribution metadata | No standard tooling reads it programmatically | Would need custom tooling to be SSOT | Not recommended |

**Rationale for `pyproject.toml` as SSOT:**

1. **PEP 621 Standard**: `pyproject.toml` is the Python community standard for declaring project metadata. Tools like `uv`, `pip`, `hatch`, and `setuptools` all read `project.version` natively.

2. **Runtime Derivation**: Python's `importlib.metadata.version("jerry")` can read the installed package version at runtime, eliminating the need for hardcoded `__version__` strings in source files.

3. **Release Workflow Integration**: The existing `.github/workflows/release.yml` already extracts and validates the version from `pyproject.toml` (lines 47-56), confirming it as the de facto authority for releases.

4. **Single Edit Point**: Developers bump the version in ONE file (`pyproject.toml`), and automation propagates to all others.

### Step 4: Sync Strategy Design

#### Architecture

```
pyproject.toml (SSOT)
    |
    +--> [version-sync script] +--> .claude-plugin/plugin.json       (JSON key replacement)
    |                          +--> .claude-plugin/marketplace.json   (JSON key replacement, both fields)
    |                          +--> CLAUDE.md                         (regex: **CLI** (vX.Y.Z) pattern)
    |
    +--> [importlib.metadata]  +--> src/__init__.py                   (runtime, no hardcoded value)
                               +--> src/interface/cli/parser.py       (runtime, no hardcoded value)
                               +--> src/transcript/__init__.py        (runtime, no hardcoded value)

EXCLUDED from sync (independent lifecycle):
    - .claude/statusline.py        (Domain E: Utility version, currently 2.1.0)
    - .claude/settings.json        (Domain C: Schema version)
    - skills/*/SKILL.md            (Domain D: Skill versions)
    - docs/schemas/*.json          (Domain C: Schema versions)
```

#### Sync Mechanism Options

| Option | Mechanism | Pros | Cons | Recommendation |
|--------|-----------|------|------|----------------|
| A: Pre-commit hook | `scripts/sync_versions.py` runs on commit | Catches drift before push; local enforcement | Requires dev setup; can be bypassed with `--no-verify` | **RECOMMENDED (primary)** |
| B: CI check | GitHub Actions step validates version consistency | Cannot be bypassed; catches all PRs | Only detects drift, doesn't auto-fix; feedback is delayed | **RECOMMENDED (secondary)** |
| C: Makefile/script | Manual `make version-bump VERSION=x.y.z` | Simple, explicit | Easy to forget; no enforcement | Useful as convenience wrapper |
| D: Bump tool (bump2version, python-semantic-release) | Dedicated version bumping tool | Feature-rich; handles tags, changelogs | Extra dependency; learning curve; may be over-engineered | Evaluate in TASK-001 |

**Recommended approach: A + B + C combined**

1. **`scripts/sync_versions.py`** -- A script that:
   - Reads version from `pyproject.toml`
   - Writes to `plugin.json`, `marketplace.json`, and `CLAUDE.md`
   - Validates all locations match
   - Can run in `--check` mode (CI) or `--fix` mode (developer)

2. **Pre-commit hook** -- Runs `sync_versions.py --check` before each commit. If versions are out of sync, the commit is rejected with an actionable error message.

3. **CI validation step** -- `.github/workflows/ci.yml` runs `sync_versions.py --check` as a required check. Belt-and-suspenders with the pre-commit hook.

4. **`__version__` elimination** -- Replace all hardcoded `__version__ = "0.1.0"` with:
   ```python
   from importlib.metadata import version
   __version__ = version("jerry")
   ```
   This means the Python source files never need updating; they read the installed metadata at runtime.

#### Marketplace `version` Decision

**Recommendation:** Synchronize `marketplace.json` top-level `version` with the framework version. Rationale:
- The marketplace currently contains exactly one plugin
- Having a separate version for a single-plugin marketplace adds confusion without value
- If multi-plugin support is added later, this can be revisited

---

## L2: Architectural Implications

### SSOT Architecture

```
                    AUTHORITATIVE
                   +--------------+
                   | pyproject.   |
                   |   toml       |
                   | version =    |
                   | "X.Y.Z"     |
                   +------+-------+
                          |
           +--------------+--------------+
           |              |              |
     [sync script]  [importlib]    [CI check]
           |              |              |
    +------v------+  +---v---+   +------v------+
    | plugin.json |  | src/  |   | Validates   |
    | market.json |  | __    |   | consistency |
    | CLAUDE.md   |  | init__|   | on every PR |
    | (regex)     |  | .py   |   +-------------+
    +-------------+  +-------+
         DERIVED      RUNTIME

    EXCLUDED (independent lifecycle):
    +-------------------------------------------+
    | .claude/statusline.py  (Domain E: v2.1.0) |
    | .claude/settings.json  (Domain C: v1.0)   |
    | skills/*/SKILL.md      (Domain D: varies) |
    | docs/schemas/*.json    (Domain C: v1.0.0) |
    +-------------------------------------------+
```

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Developer forgets to run sync script | Medium | Medium | Pre-commit hook enforces; CI validates |
| Pre-commit hook bypassed with `--no-verify` | Low | Medium | CI check catches it on PR |
| `importlib.metadata` fails in dev (not installed) | Medium | Low | Fallback: `__version__ = "dev"` or read pyproject.toml directly |
| Marketplace version semantics change in Claude Code platform | Low | High | Document decision; revisit when platform evolves |
| Skill versions confused with framework version | Low | Medium | Clear documentation; skill versions in SKILL.md frontmatter only |
| Tests break during `importlib.metadata` migration | High | Medium | Remove hardcoded version tests first; add metadata-based tests; run full suite before merging |
| Sync script accidentally updates statusline.py | Low | Low | Explicit exclusion list in sync script; statusline.py documented as Domain E |

### Impact on Release Workflow

The existing `release.yml` already:
- Extracts version from git tag (`v*`)
- Compares against `pyproject.toml` (lines 47-56)
- Issues a **warning** (not error) on mismatch

**Recommended changes to release.yml:**
1. Change the pyproject.toml check from warning to **error** (fail the release if versions don't match)
2. Add a step that runs `sync_versions.py --check` to validate all files are consistent
3. Consider auto-generating CHANGELOG from conventional commits

### Impact on Python Source

Three files currently hardcode `__version__`:

| File | Current | Proposed |
|------|---------|----------|
| `src/__init__.py` | `__version__ = "0.1.0"` | `from importlib.metadata import version; __version__ = version("jerry")` |
| `src/interface/cli/parser.py` | `__version__ = "0.1.0"` | Import from `src.__init__.__version__` or use `importlib.metadata` |
| `src/transcript/__init__.py` | `__version__ = "0.1.0"` | Import from `src.__init__.__version__` or use `importlib.metadata` |

**Note:** `importlib.metadata.version()` requires the package to be installed (`uv pip install -e .`). In development without installation, a fallback should be provided:

```python
try:
    from importlib.metadata import version
    __version__ = version("jerry")
except Exception:
    __version__ = "dev"
```

### Impact on Tests

The migration from hardcoded `__version__` to `importlib.metadata` will break existing tests that assert specific version values. Two test files are affected:

| File | Test | Current Assertion | Problem |
|------|------|-------------------|---------|
| `tests/interface/cli/unit/test_main_v2.py:189` | `TestVersionUpdate.test_version_is_0_1_0` | `assert __version__ == "0.1.0"` | Hardcodes a specific version; breaks on any version bump |
| `tests/interface/cli/unit/test_main.py:229-236` | `test_version_is_string` + `test_version_matches_expected_format` | `isinstance(__version__, str)` + semver regex match | These are **correct** and should be preserved |

**Recommended test migration strategy:**

1. **Remove `TestVersionUpdate.test_version_is_0_1_0`** (`test_main_v2.py:185-189`): This test hardcodes a specific version value and will break every time the version changes. It has no long-term value. If the intent is to verify the version is accessible, the semver format test in `test_main.py` already covers this.

2. **Keep and strengthen `test_version_is_string` and `test_version_matches_expected_format`** (`test_main.py:227-236`): These tests validate the version is a string matching semver format without coupling to a specific value. They will work correctly with `importlib.metadata`.

3. **Add a new test verifying `importlib.metadata` consistency:**
   ```python
   def test_version_matches_package_metadata(self):
       """Version should match the installed package metadata from pyproject.toml."""
       from importlib.metadata import version as pkg_version
       from src.interface.cli.parser import __version__

       assert __version__ == pkg_version("jerry")
   ```
   This test ensures that `__version__` is actually derived from package metadata rather than being a stale hardcoded value. It will fail if someone reintroduces a hardcoded `__version__` that diverges from `pyproject.toml`.

4. **Ensure `uv pip install -e .` is in the test environment setup**: Since `importlib.metadata.version()` requires the package to be installed, the CI pipeline and local test setup must include an editable install step. The Jerry project already uses `uv run pytest` which handles this via `pyproject.toml`.

**Finding F-004 (coupling):** Test files that hardcode specific version values create a maintenance burden where every version bump requires a test update. The recommended approach is to test version *properties* (is it a string? does it match semver? does it match package metadata?) rather than version *values*.

---

## Evidence Summary

| Evidence ID | Source File | Observation | Severity |
|------------|------------|-------------|----------|
| E-001 | `pyproject.toml:3` | `version = "0.2.0"` | Reference |
| E-002 | `.claude-plugin/plugin.json:3` | `"version": "0.1.0"` | Mismatch with E-001 |
| E-003 | `.claude-plugin/marketplace.json:3` | `"version": "1.0.0"` (top-level) | Mismatch; unclear semantics |
| E-004 | `.claude-plugin/marketplace.json:14` | `"version": "0.1.0"` (plugin entry) | Mismatch with E-001 |
| E-005 | `src/__init__.py:25` | `__version__ = "0.1.0"` | Mismatch with E-001 |
| E-006 | `src/interface/cli/parser.py:19` | `__version__ = "0.1.0"` | Mismatch with E-001; duplicated from E-005 |
| E-007 | `src/transcript/__init__.py:15` | `__version__ = "0.1.0"` | Mismatch with E-001 |
| E-008 | `CLAUDE.md:70` | `(v0.1.0)` inline | Mismatch with E-001 |
| E-009 | `.github/workflows/release.yml:47-56` | Validates tag vs pyproject.toml (warning only) | Design issue: should be error |
| E-010 | `skills/transcript/SKILL.md:4,211` | YAML=`2.5.0`, display=`2.4.1` | Internal inconsistency (not framework version) |
| E-011 | `.claude/settings.json:28` | `"version": "1.0"` | Independent schema version (no action needed) |
| E-012 | No CHANGELOG.md exists | Searched project root and docs/ | Gap |
| E-013 | `.claude/statusline.py:60` | `__version__ = "2.1.0"` | Independent utility version (Domain E); NOT framework version |
| E-014 | `.claude/statusline.py:6` | `Version: 2.1.0` (docstring) | Confirms statusline version in docstring header |
| E-015 | `tests/interface/cli/unit/test_main_v2.py:189` | `assert __version__ == "0.1.0"` | Hardcoded version assertion; will break on `importlib.metadata` migration |
| E-016 | `tests/interface/cli/unit/test_main.py:229-236` | semver format assertion on `__version__` | Correct test pattern; should be preserved |

---

## Gap Analysis

| Dimension | Current State | Desired State | Gap | Priority |
|-----------|---------------|---------------|-----|----------|
| **Version consistency** | 3 different values across 7 locations (`0.1.0`, `0.2.0`, `1.0.0`) | All framework-version locations show same value | **CRITICAL** -- Users and CI see conflicting versions | P0 |
| **Single Source of Truth** | No SSOT defined; each file edited independently | `pyproject.toml` is authoritative; all others derive | **HIGH** -- Root cause of drift | P0 |
| **Python `__version__`** | 3 hardcoded duplicate strings | Runtime derivation via `importlib.metadata` | **MEDIUM** -- Eliminates class of drift bugs | P1 |
| **Sync automation** | None (all manual) | Pre-commit hook + CI check + sync script | **HIGH** -- Prevents future drift | P0 |
| **Release validation** | Warning on tag/pyproject mismatch | Error (fail release) + full consistency check | **MEDIUM** -- Prevents releasing with mismatched versions | P1 |
| **Marketplace version semantics** | Unclear (`1.0.0` vs `0.1.0` in same file) | Documented decision; both fields track framework version | **MEDIUM** -- Ambiguity causes confusion | P1 |
| **CHANGELOG** | Does not exist | Auto-generated or manually maintained CHANGELOG.md | **LOW** -- Nice to have for OSS release | P2 |
| **CLI version output** | `jerry --version` shows hardcoded `0.1.0` | Shows actual framework version from SSOT | **HIGH** -- User-facing incorrect information | P0 |
| **CLAUDE.md inline version** | Hardcoded `v0.1.0` | Updated by sync script via regex | **LOW** -- Documentation accuracy | P2 |
| **Test version coupling** | `test_main_v2.py` hardcodes `"0.1.0"` | Tests validate version properties, not values | **MEDIUM** -- Blocks `importlib.metadata` migration | P1 |
| **Statusline version cataloged** | Not in version catalog | Documented as Domain E (independent) with explicit exclusion | **LOW** -- Completeness | P3 |
| **Transcript SKILL.md version mismatch** | YAML `2.5.0` vs display `2.4.1` | Consistent within file | **LOW** -- Skill-internal issue, not framework | P3 |

---

## Recommendations

### Immediate Actions (P0)

1. **Define SSOT**: Formally designate `pyproject.toml` `project.version` as the Single Source of Truth for the Jerry framework version.

2. **Create `scripts/sync_versions.py`**: A script that reads from `pyproject.toml` and writes to:
   - `.claude-plugin/plugin.json` (field: `version`) -- JSON key replacement
   - `.claude-plugin/marketplace.json` (fields: top-level `version` AND `plugins[0].version`) -- JSON key replacement
   - `CLAUDE.md` (inline version reference) -- regex replacement (see CLAUDE.md Strategy below)

   **CLAUDE.md Replacement Strategy:**

   The current version reference in `CLAUDE.md` (line 70) reads:
   ```
   **CLI** (v0.1.0): `jerry session start|end|status|abandon` | ...
   ```
   The sync script should use the regex pattern `\(v\d+\.\d+\.\d+\)` to locate and replace the version inline. Specifically:
   ```python
   import re
   pattern = r'\(v\d+\.\d+\.\d+\)'
   replacement = f'(v{new_version})'
   content = re.sub(pattern, replacement, content, count=1)
   ```
   **Risk mitigation**: If additional `(vX.Y.Z)` patterns are added to CLAUDE.md in the future, the `count=1` limit ensures only the first occurrence (the CLI version) is updated. For robustness, the script should additionally verify the match occurs on a line containing `**CLI**` to avoid false positives:
   ```python
   pattern = r'(\*\*CLI\*\*\s+)\(v\d+\.\d+\.\d+\)'
   replacement = rf'\1(v{new_version})'
   ```
   This anchored pattern is more resilient to document structure changes.

3. **Align all versions NOW**: Run the sync script (or manually update) to set all 7 locations to the current authoritative value `0.2.0`.

4. **Add CI validation**: Add a step to `.github/workflows/ci.yml` that runs `sync_versions.py --check`.

### Short-Term Actions (P1)

5. **Replace `__version__` hardcoding**: Use `importlib.metadata` in `src/__init__.py`, `src/interface/cli/parser.py`, and `src/transcript/__init__.py`.

6. **Fix test version coupling**: Remove `TestVersionUpdate.test_version_is_0_1_0` from `test_main_v2.py` (hardcoded value coupling). Keep the semver format test in `test_main.py`. Add a new test that validates `__version__` matches `importlib.metadata.version("jerry")` to enforce SSOT compliance at the test level. See "Impact on Tests" section for detailed migration plan.

7. **Harden release workflow**: Change the pyproject.toml version check in `release.yml` from warning to error.

8. **Document marketplace version semantics**: Add a comment in `marketplace.json` or an ADR explaining that the top-level `version` tracks the framework version.

9. **Pre-commit hook**: Add `sync_versions.py --check` as a pre-commit hook.

### Longer-Term Actions (P2/P3)

10. **CHANGELOG generation**: Evaluate conventional-changelog or python-semantic-release for auto-generating CHANGELOG.md from commit history.

11. **Fix transcript SKILL.md**: Align the YAML frontmatter version with the display version line.

12. **Document statusline version independence**: Add a comment in `.claude/statusline.py` noting that its `__version__` is intentionally independent from the Jerry framework version. This prevents future contributors from mistakenly including it in sync operations.

---

## References

### Source Files Analyzed

| File | Absolute Path |
|------|---------------|
| pyproject.toml | `pyproject.toml` |
| plugin.json | `.claude-plugin/plugin.json` |
| marketplace.json | `.claude-plugin/marketplace.json` |
| src/__init__.py | `src/__init__.py` |
| parser.py | `src/interface/cli/parser.py` |
| transcript/__init__.py | `src/transcript/__init__.py` |
| settings.json | `.claude/settings.json` |
| release.yml | `.github/workflows/release.yml` |
| ci.yml | `.github/workflows/ci.yml` |
| CLAUDE.md | `CLAUDE.md` |
| plugin.schema.json | `schemas/plugin.schema.json` |
| marketplace.schema.json | `schemas/marketplace.schema.json` |
| session_context.json | `docs/schemas/session_context.json` |
| statusline.py | `.claude/statusline.py` |
| test_main_v2.py | `tests/interface/cli/unit/test_main_v2.py` |
| test_main.py | `tests/interface/cli/unit/test_main.py` |

### Standards and Specifications

- [PEP 621 -- Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [importlib.metadata documentation](https://docs.python.org/3/library/importlib.metadata.html)
- Jerry Design Canon: `.claude/rules/coding-standards.md`
- Jerry Architecture Standards: `.claude/rules/architecture-standards.md`

### Related Work Items

- EN-108: Version Bumping Strategy (parent enabler)
- TASK-001: Research Version Bumping Tools
- TASK-003: Design Version Bumping Process (downstream consumer of this analysis)
- TASK-004: Implement Version Bumping
- TASK-005: Validate End-to-End

---

*Analysis completed by ps-analyst v2.2.0 on 2026-02-12*
*Iteration 2 revision on 2026-02-12 -- addressed IMP-001 (statusline.py), IMP-002 (test coupling), IMP-003 (CLAUDE.md regex), IMP-004 (complexity language)*
*Confidence: 0.94 (high -- all known version locations cataloged; test migration plan specified; CLAUDE.md replacement strategy defined; marketplace semantics slightly uncertain)*
