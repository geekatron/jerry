# TASK-004: Implement Version Bumping Automation

> **Type:** task
> **Status:** done
> **Priority:** high
> **Created:** 2026-02-12
> **Parent:** EN-108
> **Effort:** 2

---

## Summary

Implement the version bumping solution designed in TASK-003. This includes tooling configuration, GitHub Actions workflow, and version file synchronization.

## Implementation Scope

- Configure chosen version bumping tool
- Create/update GitHub Actions workflow
- Set up commit convention enforcement (if applicable)
- Implement multi-file version sync
- Handle branch protection token/permissions

## Dependencies

- TASK-003 (design must be approved first)

## Acceptance Criteria

- [x] Tool configured and committed (BMV in pyproject.toml)
- [x] GitHub Actions workflow created (version-bump.yml)
- [x] Version files update correctly on trigger (4 file targets)
- [x] Commit convention enforced (commitizen pre-commit hook)
- [x] No manual steps required for version bump

## Output

Code changes: GitHub Actions workflow, tool configuration, sync scripts (if needed).

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Task created |
| 2026-02-12 | Claude | done | Commit 8bab29f: 13 files, +520/-27. BMV + commitizen configured, version-bump.yml created, CI version-sync job added, sync_versions.py created, importlib.metadata migration, pre-commit hooks added, release.yml hardened, PAT monitor created. |
