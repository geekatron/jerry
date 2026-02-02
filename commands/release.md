# /release Command

Automates the release preparation and CI/CD handoff process.

---

## Usage

```
/release <version> [--dry-run]
```

### Arguments

- `version`: Semantic version (e.g., `0.2.0`, `1.0.0-beta.1`)
- `--dry-run`: Preview changes without committing

---

## Behavior

When invoked, this command:

1. **Validates** preconditions for release
2. **Updates** version numbers in relevant files
3. **Generates** changelog from Work Items
4. **Creates** release commit and tag
5. **Prepares** CI/CD handoff documentation

---

## Precondition Checks

Before proceeding, verify:

- [ ] All Work Items in current milestone are COMPLETED
- [ ] All tests passing (`python -m pytest`)
- [ ] No uncommitted changes in working directory
- [ ] Current branch is main/master or release branch
- [ ] Version follows semantic versioning
- [ ] Previous version tag exists (for changelog generation)

If any check fails, report the issue and stop.

---

## Version Update Locations

Update version in these files:

1. `pyproject.toml`: `version = "{new_version}"`
2. `src/__init__.py`: `__version__ = "{new_version}"`
3. `.claude-plugin/manifest.json`: `"version": "{new_version}"`

---

## Changelog Generation

Generate `CHANGELOG.md` entry from Work Items:

```markdown
## [{version}] - {YYYY-MM-DD}

### Added
- {WORK-xxx}: {title} (features with type=feature)

### Changed
- {WORK-xxx}: {title} (items with type=enhancement)

### Fixed
- {WORK-xxx}: {title} (items with type=bug)

### Security
- {WORK-xxx}: {title} (items with type=security)

### Deprecated
- {WORK-xxx}: {title} (items with type=deprecation)
```

---

## Release Commit

Create commit with message:

```
release: v{version}

Changes in this release:
- {summary of major changes}

Work Items: WORK-xxx, WORK-yyy, WORK-zzz
```

---

## Git Tag

Create annotated tag:

```bash
git tag -a v{version} -m "Release v{version}"
```

---

## CI/CD Handoff Document

Create `docs/plans/RELEASE_{version}.md`:

```markdown
# Release: v{version}

**Date**: {YYYY-MM-DD}
**Status**: READY_FOR_CI

## Pre-Release Checklist

- [x] Version updated in pyproject.toml
- [x] Version updated in src/__init__.py
- [x] Version updated in manifest.json
- [x] CHANGELOG.md updated
- [x] All tests passing
- [x] Release commit created
- [x] Tag created

## CI/CD Actions Required

1. [ ] Run full test suite on CI
2. [ ] Build distribution packages
3. [ ] Run security scan
4. [ ] Publish to package registry (if applicable)
5. [ ] Create GitHub release with changelog

## Rollback Plan

If issues discovered post-release:

1. Revert release commit: `git revert {commit_sha}`
2. Delete tag: `git tag -d v{version}`
3. Investigate and fix issues
4. Re-run /release with patch version

## Release Notes (for GitHub/announcement)

{Copy from CHANGELOG entry}
```

---

## Dry Run Output

When `--dry-run` is specified:

```
=== Release Dry Run: v{version} ===

Precondition Checks:
  [PASS] All Work Items completed
  [PASS] Tests passing
  [PASS] No uncommitted changes
  [PASS] On main branch
  [PASS] Valid semver

Files to Update:
  - pyproject.toml: 0.1.0 -> {version}
  - src/__init__.py: 0.1.0 -> {version}
  - manifest.json: 0.1.0 -> {version}

Changelog Preview:
  ## [{version}] - {date}
  ### Added
  - WORK-001: Add Work Tracker skill
  ...

Git Operations:
  - Commit: release: v{version}
  - Tag: v{version}

Run without --dry-run to execute.
```

---

## Example

```
User: /release 0.2.0

Claude: Running release preparation for v0.2.0...

Precondition Checks:
  [PASS] All Work Items in milestone completed
  [PASS] Tests passing (42 passed, 0 failed)
  [PASS] Working directory clean
  [PASS] On branch: main
  [PASS] Version 0.2.0 is valid semver

Updating versions...
  - pyproject.toml: 0.1.0 -> 0.2.0
  - src/__init__.py: 0.1.0 -> 0.2.0
  - manifest.json: 0.1.0 -> 0.2.0

Generating changelog...
  Added 3 entries to CHANGELOG.md

Creating release commit and tag...
  Commit: abc1234 - release: v0.2.0
  Tag: v0.2.0

Release v0.2.0 is ready!
CI/CD handoff document: docs/plans/RELEASE_0.2.0.md

Next steps:
1. Push to remote: git push origin main --tags
2. Monitor CI/CD pipeline
3. Verify deployment
```
