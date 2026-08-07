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

**Scope widening (PR #341 owner review, 2026-08-07):** Default containment
roots extend from the single project root to a set — project root +
`tempfile.gettempdir()` (resolved) + `/tmp` (resolved, when it exists) — via
new `project_root.get_containment_roots(explicit_root)`, covering Claude
Code scratchpad writes (macOS: `$TMPDIR` vs `/tmp/claude-*` are distinct
trees). A new `--root <path>` flag on every `jerry ast` subcommand makes the
allowed set *exactly* the resolved `--root` value when supplied (exclusive
override) — an explicit user-discretion escape hatch, consistent with the
owner's directive that Jerry can only provide reasonable best-effort
protection, not a hard boundary against a user's own choices. M-08/M-10
containment and symlink checks are preserved unchanged, generalized from a
single root to "any of the allowed roots." Two owner-resolved stderr
transparency behaviors (stdout is reserved for the JSON/render payload):
`--root` resolving to an unusually broad location (filesystem/drive root or
`$HOME`, detected portably via `Path.parts`/`Path.anchor`) prints a
one-line stderr WARNING and still proceeds (R-3); a path allowed only via a
temp/scratchpad default root (not the project root, not an explicit
`--root`) prints a one-line stderr transparency note (R-4).

---

## Acceptance Criteria

- [ ] Failing tests written first (H-20 Red): file inside cwd validates; file outside project root still rejected; `CLAUDE_PROJECT_DIR` honored; symlink escape still rejected; write-path re-check consistent
- [ ] `jerry ast` commands accept files within the user's project root (env var or cwd) regardless of where Jerry is installed
- [ ] M-08/M-10 containment security preserved: paths and symlink targets outside the resolved project root are still rejected
- [ ] Root resolution logic exists once (shared helper) and is used by both `ast_commands.py` and `adapter.py`
- [ ] Full test suite green with >= 90% coverage (H-20b); changelog entry added
- [ ] `jerry ast` commands accept files under `tempfile.gettempdir()` and
      `/tmp` (when present) by default, in addition to the project root —
      the Claude Code scratchpad scenario
- [ ] `--root <path>` flag exists on all 10 `jerry ast` subcommands and,
      when supplied, makes containment exclusive to that resolved path
      (a project-root file is REJECTED when `--root` points elsewhere)
- [ ] M-08/M-10 containment and symlink-escape checks verified against the
      widened root set, including a symlink planted inside an allowed temp
      root pointing outside all allowed roots
- [ ] `tests/security/test_adversarial_parsers.py::TestA07PathTraversal`
      re-verified green under the widened default roots (path traversal
      outside all roots still rejected)
- [ ] Broad `--root` (filesystem/drive root or `$HOME`) prints a one-line
      stderr WARNING and still proceeds (R-3); ordinary `--root` values do
      not warn
- [ ] A path allowed only via a temp/scratchpad default root (not the
      project root, not an explicit `--root`) prints a one-line stderr
      transparency note (R-4); project-root and explicit `--root` matches
      never print this note
- [x] H-01 (RED-BUG010, CWE-552/CWE-668/CWE-281): a temp-default-root
      match is additionally gated on file ownership (`resolved.stat().st_uid
      == os.geteuid()` on POSIX; no-op on Windows via `os.name` guard) —
      scoped strictly to temp-default matches, never the project root or
      an explicit `--root`; a foreign-owned temp-root file is rejected
      with a descriptive error
- [x] H-02/H-08 (RED-BUG010, incomplete-allowlist gap): `_is_broad_containment_root`
      widened to flag any ANCESTOR OF (or equal to) `$HOME` — not just the
      exact filesystem/drive root or exact `$HOME` — closing the `/home`,
      `/Users`, `$HOME`'s parent, and `C:\Users` coverage gaps via a
      single portable `PurePath.relative_to()` check (covers `PureWindowsPath`
      too, folding in the H-08 Windows caveat)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-08-07 | in_progress | Created from GH #337 (filed 2026-08-05). Root cause confirmed in code; fix approach = reuse adapter.py's CLAUDE_PROJECT_DIR/cwd resolution via shared helper. Branch fix/BUG-010-ast-project-root off post-#340 main. |
| 2026-08-07 | in_progress | Scope widened per PR #341 owner review: default containment roots extended to temp/scratchpad dirs (`tempfile.gettempdir()`, `/tmp`); added `--root` exclusive-override flag across all `jerry ast` subcommands. eng-lead implementation plan produced; eng-backend executed test-first (H-20): 2 existing containment-rejection tests required a `tempfile.gettempdir`/`_HARDCODED_TMP` monkeypatch seam fix (pytest `tmp_path` lives inside the system tempdir and would otherwise falsely pass containment under the widened roots) — verified both tests fail without the seam before restoring it. Owner-resolved R-3 (broad-root stderr WARNING) and R-4 (temp-match stderr transparency note) implemented and test-covered. |
| 2026-08-07 | in_progress | red-team remediation (RED-BUG010, red-vuln findings): H-01 temp-root ownership gate (`_check_temp_root_ownership`, scoped via new `_is_temp_default_root_match` helper) added to `_check_path_containment` in `ast_commands.py`, closing the multi-user shared-`/tmp` read/write gap (CWE-552/CWE-668/CWE-281). H-02/H-08 `_is_broad_containment_root` widened in `project_root.py` to flag any ancestor of `$HOME` via `PurePath.relative_to()`, closing the `/home`/`/Users`/`C:\Users` incomplete-allowlist gap. eng-backend executed test-first (H-20): 10 new tests written and RED-verified (`AttributeError`/assertion failures) before implementation; GREEN after — 149/149 in the two changed test files, 371/371 across `tests/unit/interface/cli/` + `tests/security/` + `tests/integration/cli/`, `TestA07PathTraversal` re-confirmed green. `ruff format --check` and `ruff check` both exit 0. |
