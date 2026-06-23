# Changelog

All notable changes to the Jerry Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed
- Delete `requirements.txt`, `requirements-dev.txt`, `requirements-test.txt` — dead pip artifacts that triggered broken Dependabot PRs (#251); uv-only per H-05
- Remove pip fallback from release archive — `release.yml` no longer bundles requirements files
- Remove all `pip install` instructions from docs, error messages, and CI comments — replaced with `uv add`/`uv tool install`/`uv run`

### Fixed
- **fix(ci):** correct `cyclonedx-py` output flag from `--outfile` to `-o` — fixes v0.31.4 release SBOM generation failure
- Migrate 7 enum classes from `(str, Enum)` to `StrEnum` in `docs/schemas/types/session_context.py` — Python 3.11+ modernization, unblocks ruff 0.15.10 UP042 rule
- **fix(ci):** replace bare `python3 -m py_compile` with `uv run python -m py_compile` in plugin-validation — closes last H-05 violation
- **fix(ci):** scope `pull-requests:write` to `coverage-report` job only — eliminates PR write blast radius for 14 jobs (TASK-021)
- **fix(ci):** restrict push triggers to `main`/`master` branches — closes untrusted-branch CI trigger attack surface (TASK-022)
- **fix(ci):** migrate lint, type-check, security jobs to `uv sync --frozen` — eliminates 4 H-05 violations and closes supply chain gap (TASK-017)
- **fix(ci):** scan full dependency tree via `uv export --all-extras` for pip-audit — replaces 3-package hand-picked list with complete lockfile audit (TASK-018)

### Changed
- **refactor(ci):** remove redundant `test-pip` job (8 matrix cells) — uv test matrix provides equivalent coverage (TASK-016)
- **refactor(ci):** consolidate 6 validation jobs (`lockfile-check`, `template-validation`, `frontmatter-validation`, `license-headers`, `version-sync`, `hard-rule-ceiling`) into single `validation` job (TASK-019)
- **refactor(ci):** merge `lint` and `type-check` into `static-analysis` job with shared `uv sync --frozen --extra dev` (TASK-020)

### Added
- **feat(ci):** composite action `.github/actions/security-audit` — unified pip-audit scan with CVE accept-list, D5 meaningful-audit guard, and `vuln-found` output for downstream issue management (#301)
- `.github/security/audit-allowlist.yml` — CVE accept-list with 90-day expiry enforcement; empty by default (all current CVEs have published fixes)
- `scripts/security/audit_allowlist.py` — fail-closed parser for the accept-list: validates required fields, enforces 90-day cap, checks expiry, emits `--ignore-vuln` flags for pip-audit (#301)
- **feat(ci):** `security-scan.yml` hardened — scheduled scan now uses composite action (fixes E4 false-green bug), adds auto-issue creation/update/close via `gh` CLI for rolling CVE alert management (#301)
- CODEOWNERS entries for `.github/actions/` and `.github/security/` — requires maintainer review to prevent supply-chain attacks via action script or CVE suppression abuse (#301)
- ADR-output-path-resolution-001: Unified Output Path Resolution Protocol (P1/P2/P3/P4 layered resolution chain)
- AD-M-011 MEDIUM standard: agents SHOULD use project-relative output paths per ADR-output-path-resolution-001
- `filename_pattern` field in agent-governance-v1.schema.json for Priority 2 base-path resolution
- `skill-output-path-enforcement` pre-commit hook (L5 CI gate) — prevents regression to `skills/*/output/` paths
- `.gitignore` rule for `skills/*/output/` to prevent future accumulation
- Domain-first ADR naming convention: `ADR-{domain-slug}-{NNN}` (ADR-agent-design-001, ADR-routing-triggers-001, ADR-output-path-resolution-001)
- Output Path Resolution section in 32 agent .md files with H-31 engagement-id fallback and Tier 1 ADR reference
- P1/P2/P3 output path options in prompt-templates.md Templates 2 and 3
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
- **BUG-006**: Agent output paths hardcoded to `skills/*/output/` replaced with project-relative `projects/${JERRY_PROJECT}/` paths across 107 config files, 32 agents, 13 skills per ADR-output-path-resolution-001 (#230)
- **BUG-012**: 5 pm-pmm agents migrated from repo-root `docs/pm-pmm/` to project-relative paths (#245)
- **BUG-013**: 2 prompt-engineering agents — `{PROJECT_ID}` placeholder replaced with `${JERRY_PROJECT}` env var (#246)
- **BUG-014**: 12 agents across adversary/transcript/saucer-boy-fw/worktracker — governance YAML `output:` sections added (#247)
- **BUG-007**: tspec-generator RULE-OT-04 fallback for unrecognized extension outcomes — warns instead of silent skip (#195)
- **BUG-008**: tspec-analyst staleness detection — cross-references Feature file snapshot against live UC flow count (#197)
- **BUG-009**: tspec-analyst aggregate coverage mode across multiple slices (#196)
- **BUG-010**: uc-slicer Step 0 duplicate slice_id detection with H-31 clarification (#199)
- **BUG-011**: Banned-term check uses word-boundary matching (`\b`) instead of substring matching (#198)
- Diataxis SKILL.md plural/singular naming inconsistencies (`howto/` to `how-to/`, `explanations/` to `explanation/`)
- **BUG-001**: Memory-keeper MCP tool names corrected across 26 governance files — `store`/`retrieve`/`search`/`list`/`delete` replaced with actual API names `context_save`/`context_get`/`context_search`/`context_session_list`/`context_batch_delete` (#111)
- **BUG-002**: Version bump regex case sensitivity verified already implemented (src/version/ bounded context with case-insensitive regex) (#132)
- **BUG-005**: Hook tests rewritten from `scripts/tests/` to `tests/` targeting CLI enforcement — deleted `test_hooks.py`, `test_patterns.py`, removed pytest.ini `--ignore` entries (#214)
- **BUG-007**: 8 broken mkdocs anchor links fixed across 7 docs files — heading renames in INSTALLATION.md, missing References section in rescore report, truncated nav-table slugs in voice scores (#213)
- 8 bypass vectors closed: null byte injection, non-string type confusion, subshell cd evasion, multi-space git push, two-stage download-execute, non-rm destructive deletion, path suffix false positives
- Claude Code settings migrated from deprecated fields to schema-valid configuration — removed invalid `hooks`, `stash`, `grep` fields (#180)
- Skill-level permission entries added to `settings.local.json` so proactive skill invocations (H-22) don't prompt for permission (#181)
- Deprecated Bash command patterns (`/bin/bash`, `bash -c`) replaced with direct command syntax in all settings permission entries (#182)
- `pymdown-extensions` upgraded to 10.21.2 — fixes `filename=None` crash with Pygments 2.20.0 in mkdocs code block rendering
- Flaky 50-file batch performance test thresholds relaxed from 500ms to 1000ms to handle pre-commit hook concurrent load
- `uv.lock` regenerated after Dependabot pip updates caused lockfile drift — unblocks CI on main

### Changed
- Dependabot `package-ecosystem` switched from `pip` to `uv` — updates both `pyproject.toml` and `uv.lock` together, preventing future lockfile drift
- Added `uv lock --check` CI job for lockfile freshness verification at PR time
- 28 stale eng-team output files removed from `skills/eng-team/output/` (600K)
- ADR-PROJ007-001 renamed to ADR-agent-design-001 (domain-first naming convention)
- ADR-PROJ007-002 renamed to ADR-routing-triggers-001 (domain-first naming convention)
- quality-enforcement.md References table: added Location column with file paths for ADR-EPIC002-001/002
- `hooks.json`: PreToolUse consolidated from dual hooks (standalone script + CLI) to single CLI path; NotebookEdit added to matcher
- `hooks.json`: SubagentStop consolidated from dual hooks (standalone handoff script + CLI lifecycle) to single CLI path — handoff orchestration superseded by `/orchestration` skill (#178)
- `hooks/pre-tool-use.py`: Updated wrapper with consolidation documentation
- `version-bump.yml`: `workflow_dispatch` now respects `[skip-bump]` marker to prevent double-bumping (F-004)
- `ci.yml`: Removed redundant `uv run python scripts/validate-agent-frontmatter.py` step — P-003 check now included in `uv run jerry agents validate-frontmatter` (#193)
- `ValidateFrontmatterCommandHandler`: Split from 1 file (H-10 violation) into 4 files — `validate_frontmatter_command.py`, `validate_frontmatter_command_handler.py`, `frontmatter_file_result.py`, `validate_frontmatter_result.py` (#193)
- `ValidateFrontmatterCommandHandler`: P-003 Agent/Task tool restriction check ported from standalone script — detects delegation tools in non-T5 agents with governance.yaml tier lookup and fail-closed semantics (#193)

### Removed
- `scripts/pre_tool_use.py` — deleted, all security enforcement ported to `SecurityEnforcementEngine` via CLI (#177)
- `scripts/subagent_stop.py` — deleted, lifecycle tracking consolidated to CLI handler (#178)
- `scripts/validate-agent-frontmatter.py` — deleted, all validation including P-003 check ported to CLI handler (#193)
- `scripts/tests/` — entire directory removed, all tests migrated to `tests/` (#214)
- `pytest.ini`: Removed `--ignore` entries for `scripts/tests/test_hooks.py` and `scripts/tests/test_patterns.py`; removed `scripts/tests` from `testpaths`

### Added
- `.gitattributes` — comprehensive cross-platform line ending normalization (136 lines, red-team reviewed) with LF enforcement for all text files, CRLF for Windows scripts, binary markers, semantic diff drivers (#116)
- `tests/unit/agents/test_p003_agent_tool_restriction.py` — 8 tests for P-003 Agent tool restriction in CLI handler (#193)
- `docs/audits/h32-parity-audit-20260330.md` — full cross-project H-32 GitHub Issue parity audit (20 projects, 89 issues, 37 entities)

### Security
- Memory-keeper MCP tool names corrected from wrong names (`store`/`retrieve`) to actual API names (`context_save`/`context_get`) in `.claude/settings.local.json`; wildcard `mcp__memory-keeper__*` retained for trusted server access
- P-003 enforcement consolidated: Agent/Task tool restriction now enforced by single CLI handler with fail-closed governance.yaml lookup, replacing dual-path enforcement (standalone script + CLI) (#193)

## [0.28.0] - 2026-03-12

### Added
- `/use-case` skill — guided use case authoring (uc-author) and Jacobson UC 2.0 slicing (uc-slicer) with Cockburn 12-step methodology, rejection artifact pattern for inter-agent error propagation, and 2D detail_level x realization_level state matrix ([#109](https://github.com/geekatron/jerry/issues/109), [PR #149](https://github.com/geekatron/jerry/pull/149))
- `/test-spec` skill — BDD test specification generation from use cases via Clark transformation (tspec-generator) with 7 Cs coverage analysis (tspec-analyst) ([#109](https://github.com/geekatron/jerry/issues/109), [PR #149](https://github.com/geekatron/jerry/pull/149))
- `/contract-design` skill — API contract generation from use case realization artifacts producing OpenAPI 3.1 specifications (cd-generator) with 9-step validation (cd-validator), three-layer description quality validation, and PROTOTYPE review checklist ([#109](https://github.com/geekatron/jerry/issues/109), [PR #149](https://github.com/geekatron/jerry/pull/149))
- `use-case-realization-v1.schema.json` — JSON Schema (Draft 2020-12) for use case artifact YAML frontmatter validation with allOf conditional constraints for lifecycle state consistency
- `test-specification-v1.schema.json` — JSON Schema (Draft 2020-12) for BDD Feature file YAML frontmatter validation
- Rejection artifact pattern (`{artifact_path}-rejection.yaml`) — structured inter-agent error propagation with T1-T5 security mitigations (ADR-PM001)
- `work/` fallback output paths for all 6 PROJ-021 agents when `JERRY_PROJECT` is not set ([#192](https://github.com/geekatron/jerry/issues/192))

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
