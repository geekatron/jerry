# ADR-RELEASE-001: GitHub Releases Pipeline

**Date**: 2026-01-12
**Status**: ACCEPTED
**Author**: Claude
**Related**: DISC-005, DISC-007, TD-013

---

## Context

Jerry Framework requires a release mechanism to distribute the Claude Code Plugin to users.

### Discovery Trail

1. **DISC-005**: Identified that release pipeline was missing from CI/CD despite ADR-CI-001 stating intent for public release
2. **DISC-007**: Clarified that Jerry is a **Claude Code Plugin**, not a standalone Python application
   - Original assumption: PyInstaller binaries for macOS/Windows
   - Correct model: Plugin archive containing `.claude/`, `skills/`, `src/`, `CLAUDE.md`

### Requirements

1. **R1**: Trigger release on semantic version tags (`v*`)
2. **R2**: Run CI checks before creating release
3. **R3**: Generate plugin archive artifacts (`.tar.gz`, `.zip`)
4. **R4**: Auto-generate release notes from commits
5. **R5**: Support pre-release versions (e.g., `v1.0.0-beta.1`)
6. **R6**: Provide checksums for download verification

---

## Decision

Implement a GitHub Releases workflow that:

### D1: Tag-Triggered Release

**Trigger**: `push` to tags matching `v*` pattern

```yaml
on:
  push:
    tags:
      - "v*"
```

**Rationale**: Standard semantic versioning convention. Tags are explicit release intentions.

### D2: CI Gates Before Release

**Approach**: Run lint, type check, and full test suite before building artifacts.

**Rationale**: No release should go out with failing tests or type errors. This is non-negotiable for quality.

### D3: Plugin Archive Structure

**Contents**:
```
jerry-plugin-X.Y.Z/
├── .claude/              # Claude Code hooks and configuration
├── .claude-plugin/       # Plugin manifest
├── skills/               # Natural language interfaces
├── src/                  # Hexagonal core
├── docs/                 # Documentation
├── scripts/              # CLI scripts
├── hooks/                # Additional hooks
├── CLAUDE.md             # Context for Claude Code
├── AGENTS.md             # Agent registry
├── GOVERNANCE.md         # Governance principles
├── README.md             # Project readme
├── pyproject.toml        # Project configuration
├── pytest.ini            # Test configuration
└── .gitignore            # Git ignore patterns
```

**Excluded**:
- `.git/` - Repository metadata
- `.github/` - CI/CD configuration
- `.venv/` - Virtual environment
- `projects/` - User project workspaces
- `tests/` - Test suite
- Cache directories (`.pytest_cache/`, `.ruff_cache/`, `.idea/`)

**Rationale**: Include everything needed for the plugin to function, exclude development artifacts.

### D4: Dual Archive Formats

**Formats**: `.tar.gz` and `.zip`

**Rationale**:
- `.tar.gz`: Standard for Linux/macOS, preserves permissions
- `.zip`: Native support on Windows, wider compatibility

### D5: SHA256 Checksums

**Approach**: Generate `checksums.sha256` file containing hashes for all artifacts.

**Rationale**: Allows users to verify download integrity, standard security practice.

### D6: Pre-release Detection

**Logic**: Version containing `-` is marked as pre-release (e.g., `v1.0.0-beta.1`, `v2.0.0-rc.1`)

**Rationale**: Semantic versioning convention. Pre-releases are not production-ready.

### D7: Auto-Generated Release Notes

**Approach**: Generate notes from git log between previous tag and current tag.

**Rationale**: Reduces manual work, ensures comprehensive change documentation.

---

## Consequences

### Positive

1. **Automated releases**: Tag push triggers full release workflow
2. **Quality gates**: CI must pass before artifacts are created
3. **Cross-platform**: Both `.tar.gz` and `.zip` formats available
4. **Verifiable**: SHA256 checksums for all artifacts
5. **Pre-release support**: Beta/RC versions clearly marked

### Negative

1. **No binary distribution**: Users must have Python 3.11+ for development features
2. **Manual tagging**: Release requires explicit `git tag` + `git push`
3. **No rollback automation**: Failed releases require manual cleanup

### Risks

1. **Tag-version mismatch**: Tag version may not match `pyproject.toml` version
   - Mitigation: Warning in workflow output (non-blocking)
2. **Large archive size**: Plugin may grow large with documentation
   - Mitigation: Monitor size in CI output

---

## Implementation

### Files Created

| File | Purpose |
|------|---------|
| `.github/workflows/release.yml` | Release workflow |
| `docs/INSTALLATION.md` | Installation guide |
| `decisions/ADR-RELEASE-001-github-releases.md` | This ADR |

### Workflow Jobs

| Job | Purpose | Dependencies |
|-----|---------|--------------|
| `validate` | Extract and validate version from tag | None |
| `ci` | Run lint, type check, tests | `validate` |
| `build` | Create plugin archives | `validate`, `ci` |
| `release` | Create GitHub Release with artifacts | `validate`, `build` |

---

## Verification

To verify the release pipeline:

1. **Create a test tag**:
   ```bash
   git tag v0.0.1
   git push origin v0.0.1
   ```

2. **Check GitHub Actions**:
   - Workflow should trigger on tag push
   - All jobs should pass
   - Release should appear at github.com/geekatron/jerry/releases

3. **Verify artifacts**:
   - Download `.tar.gz` and `.zip`
   - Verify checksums match
   - Extract and verify structure

---

## References

- [GitHub Actions: Creating releases](https://docs.github.com/en/actions/using-workflows/releasing-projects)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [softprops/action-gh-release](https://github.com/softprops/action-gh-release)
- DISC-005: Release Pipeline Missing from CI/CD
- DISC-007: TD-013 Misunderstood Distribution Model
