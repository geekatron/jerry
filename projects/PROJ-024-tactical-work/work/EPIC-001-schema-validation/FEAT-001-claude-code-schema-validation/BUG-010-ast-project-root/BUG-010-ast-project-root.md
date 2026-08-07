# BUG-010: jerry ast Rejects All Files Outside the Plugin's Own Install Tree

> **Type:** bug
> **Status:** in_progress
> **Priority:** high
> **Severity:** major
> **Impact:** high
> **Created:** 2026-08-07
> **Parent:** FEAT-001
> **GitHub Issue:** [#337](https://github.com/geekatron/jerry/issues/337)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What's broken |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the failure |
| [Root Cause](#root-cause) | Why it's broken |
| [Fix Approach](#fix-approach) | Design of the correction |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [History](#history) | Status changes |

---

## Summary

Every `jerry ast` subcommand rejects any file outside the Jerry plugin's own installation directory with `Path escapes repository root`. The path-containment guard resolves "repository root" by walking up from `ast_commands.py`'s own `__file__` to the first `pyproject.toml` — which is always the installed plugin's root, never the user's project. The entire `ast` namespace is therefore unusable against real user repositories, the only place users keep their documents. Meanwhile `jerry config path` resolves the project root correctly (`CLAUDE_PROJECT_DIR` env var, else current working directory), so the CLI already contains the right resolution logic — the `ast` namespace just doesn't use it.

---

## Steps to Reproduce

1. Install Jerry as a plugin (e.g., `~/.claude/plugins/marketplaces/jerry-framework`).
2. From a user project directory, run `jerry ast validate` against one of that project's own documents:

```bash
# cwd = the user's project (contains projects/PROJ-001-example/PLAN.md)
uv run --project ~/.claude/plugins/marketplaces/jerry-framework \
  jerry ast validate projects/PROJ-001-example/PLAN.md
```

3. Observe: `Error: Path escapes repository root: ...` with exit code 2; no parsing attempted. Absolute path forms fail identically.
4. Contrast: `jerry config path` from the same directory correctly reports the user's project as the project root.

---

## Root Cause

`src/interface/cli/ast_commands.py` `_get_repo_root()` (line 158, v0.31.7) anchors root resolution to `Path(__file__).resolve()` and walks parents for a `pyproject.toml` — always finding the plugin's own. `_check_path_containment()` (line 176) then enforces the M-08/M-10 security containment against that wrong root, and the write-time TOCTOU re-check (line 513) repeats it.

---

## Fix Approach

Extract the CLI's existing, correct resolution (`CLAUDE_PROJECT_DIR` env var → else `Path.cwd()`, as implemented in `adapter.py` `_get_project_root()`) into a shared helper module `src/interface/cli/project_root.py`, and use it from both `ast_commands.py` (replacing the `__file__` walk) and `adapter.py` (removing the duplicate). The M-08/M-10 containment and symlink checks remain fully intact — only the anchor changes to the user's project root. BDD test-first per H-20.

---

## Acceptance Criteria

- [ ] Failing tests written first (H-20 Red): file inside cwd validates; file outside project root still rejected; `CLAUDE_PROJECT_DIR` honored; symlink escape still rejected; write-path re-check consistent
- [ ] `jerry ast` commands accept files within the user's project root (env var or cwd) regardless of where Jerry is installed
- [ ] M-08/M-10 containment security preserved: paths and symlink targets outside the resolved project root are still rejected
- [ ] Root resolution logic exists once (shared helper) and is used by both `ast_commands.py` and `adapter.py`
- [ ] Full test suite green with >= 90% coverage (H-20b); changelog entry added

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-08-07 | in_progress | Created from GH #337 (filed 2026-08-05). Root cause confirmed in code; fix approach = reuse adapter.py's CLAUDE_PROJECT_DIR/cwd resolution via shared helper. Branch fix/BUG-010-ast-project-root off post-#340 main. |
