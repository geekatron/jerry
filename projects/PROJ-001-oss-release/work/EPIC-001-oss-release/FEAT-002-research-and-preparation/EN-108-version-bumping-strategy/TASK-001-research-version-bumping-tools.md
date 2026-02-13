# TASK-001: Research Version Bumping Tools and Approaches

> **Type:** task
> **Status:** done
> **Priority:** high
> **Created:** 2026-02-12
> **Parent:** EN-108
> **Effort:** 2

---

## Summary

Research available tools and approaches for automated version bumping in a Python + Claude Code plugin project. Evaluate against Jerry's constraints (GitHub Actions CI, pre-commit hooks, branch protection on main).

## Scope

- Conventional Commits specification and enforcement
- `python-semantic-release` — Python-native, integrates with pyproject.toml
- `bump2version` / `bump-my-version` — config-driven, multi-file support
- `semantic-release` (Node.js) — widely adopted, GitHub Actions support
- GitHub Actions built-in approaches (e.g., release-please)
- Custom shell/Python scripts

## Acceptance Criteria

- [x] At least 4 tools/approaches evaluated (6 tools evaluated)
- [x] Pros/cons documented for each
- [x] Recommendation with rationale
- [x] Compatibility with Jerry's CI/CD assessed

## Output

Research artifact: `research-version-bumping-tools.md`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Task created |
| 2026-02-12 | Claude | done | Research complete. QG score: 0.928 (2 iterations). 6 tools evaluated. |
