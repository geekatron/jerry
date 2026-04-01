# Changelog

All notable changes to the Jerry Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CHANGELOG.md using Keep a Changelog format, enforced by CI (`changelog-check` job)
- CI enforcement: `changelog-check` job in `ci.yml` fails PRs that don't update CHANGELOG.md (exempts bots, `[skip-changelog]` escape hatch)
- Dependabot configuration for automated GitHub Actions and pip dependency updates (`.github/dependabot.yml`)
- Reference documentation for CI/CD pipeline security controls (`docs/reference/ci-cd-pipeline-security.md`)
- Explanation documentation for CI/CD supply chain security model (`docs/explanation/ci-cd-supply-chain-security.md`)
- Three Diataxis how-to guides for CI/CD operations: update SHA-pinned action, add CI job, add GitHub Actions dependency (#155, #156, #157)
- `SecurityEnforcementEngine` — consolidated pre-tool-use security enforcement with 82 tests covering blocked paths, sensitive files, dangerous commands, git force push blocking, PII/secrets detection (#150)
- `PatternLibraryAdapter` — wraps existing patterns.yaml for secrets/PII detection with T-06 compliance
- `SecurityRules` — injectable frozen dataclass for security rule definitions

### Fixed
- **BUG-001**: Memory-keeper MCP tool names corrected across 26 governance files — `store`/`retrieve`/`search`/`list`/`delete` replaced with actual API names `context_save`/`context_get`/`context_search`/`context_session_list`/`context_batch_delete` (#111)
- **BUG-002**: Version bump regex case sensitivity verified already implemented (src/version/ bounded context with case-insensitive regex) (#132)
- False-positive `cd` detection in `SecurityEnforcementEngine` — substring matching replaced with regex word-boundary matching to prevent blocking commands like `argocd`, `systemctl restart httpd`, `base64` (#234)
- 8 bypass vectors closed: null byte injection, non-string type confusion, subshell cd evasion, multi-space git push, two-stage download-execute, non-rm destructive deletion, path suffix false positives

### Changed
- `hooks.json`: PreToolUse consolidated from dual hooks (standalone script + CLI) to single CLI path; NotebookEdit added to matcher
- `hooks/pre-tool-use.py`: Updated wrapper with consolidation documentation
- `scripts/pre_tool_use.py`: Marked DEPRECATED — superseded by SecurityEnforcementEngine
- `version-bump.yml`: `workflow_dispatch` now respects `[skip-bump]` marker to prevent double-bumping (F-004)

### Security
- Memory-keeper MCP tool names corrected from wrong names (`store`/`retrieve`) to actual API names (`context_save`/`context_get`) in `.claude/settings.local.json`; wildcard `mcp__memory-keeper__*` retained for trusted server access

## [0.25.0] - 2026-03-09

### Fixed
- **BUG-003**: `version-bump.yml` fails because `uv sync` re-resolves dependencies and dirties `uv.lock` — replaced all bare `uv sync` with `uv sync --frozen` across CI workflows ([#151](https://github.com/geekatron/jerry/issues/151), [PR #152](https://github.com/geekatron/jerry/pull/152))
- **BUG-003/F-003**: Skip-bump guard changed from `author.name` (spoofable via `git config`) to `github.actor` (authenticated identity set by GitHub)

### Security
- **EN-001**: All GitHub Actions pinned to commit SHAs instead of floating tags to prevent supply-chain attacks via tag force-push ([#153](https://github.com/geekatron/jerry/issues/153), [PR #154](https://github.com/geekatron/jerry/pull/154))
  - `actions/checkout` — `@v5` → `@08c6903cd8c0fde910a37f88322edcfb5dd907a8`
  - `astral-sh/setup-uv` — `@v5` → `@d4b2f3b6ecc6e67c4457f6d3e41ec42d3d0fcb86`
  - `actions/upload-artifact` — `@v4` → `@ea165f8d65b6e75b540449e92b4886f43607fa02`
  - `actions/download-artifact` — `@v4` → `@95815c38cf2ff2164869cbab79da8d1f422bc89e`
  - `softprops/action-gh-release` — `@v2` → `@da05d552573ad5aba039eaac05058a918a7bf631`
  - `actions/github-script` — `@v7` → `@60a0d83039c74a4aee543508d2ffcb1c3799cdea`
  - `MishaKav/pytest-coverage-comment` — `@main` → SHA-pinned
- **EN-001**: `uv` binary pinned to `0.10.9` across all workflows (previously `version: "latest"` partially defeated SHA pinning)
- **EN-001**: `bump-my-version` pinned to exact version `1.2.7` to prevent supply-chain attacks via PyPI
- **EN-001**: Prerelease label input validated as alphanumeric-only to prevent shell injection via `workflow_dispatch`
- **EN-001**: Pip tool versions pinned in CI — `pyright==1.1.408`, `pip-audit==2.10.0`, `filelock==3.20.3`, `mypy==1.19.1`, `ruff==0.14.11`

### Changed
- **EN-001**: `release.yml` migrated from pip fallback to uv-only (`uv sync --frozen` + `uv run`) — H-05 compliance
- **EN-001**: `docs.yml` migrated from `actions/setup-python` + `pip install` to `astral-sh/setup-uv` + `uv sync --frozen --extra dev` — H-05 compliance
- **EN-001**: All `uv sync` calls across `ci.yml` now use `--frozen` flag for reproducible builds

## [0.24.0] - 2026-03-08

### Added
- Product Management and Product Marketing (`/pm-pmm`) skill with 5 specialized agents
- User Experience (`/user-experience`) skill with 10 framework specialist agents

---

> **Enforced**: The `changelog-check` CI job fails any PR that does not modify this file.
> Exempt: Dependabot PRs, version-bump bot commits, and PRs with `[skip-changelog]` in the title.
> The version-bump workflow promotes `[Unreleased]` entries to a versioned section when a new release tag is created.
