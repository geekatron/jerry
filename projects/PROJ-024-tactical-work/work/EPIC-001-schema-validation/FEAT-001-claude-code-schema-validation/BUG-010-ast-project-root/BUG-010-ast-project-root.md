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

**Redesign to Option C — user-declared trusted roots (PR #341, 2026-08-11):**
The initial scope-widening (auto-trusting `tempfile.gettempdir()`/`/tmp`) was
found insecure by a C4 adversarial tournament (index-based trust bypass,
write-path TOCTOU, fail-open ownership gate, uid-0 multi-tenant, `TMPDIR`
poisoning, stderr/JSON corruption — score 0.64 REVISE) and was **replaced**.
The default allowed set is now the user's project root **plus zero-or-more
explicitly user-declared `ast.trusted_roots` config entries** (read via
Jerry's layered config; env `JERRY_AST__TRUSTED_ROOTS`, note the double
underscore). No directory is auto-trusted; OS temp/scratchpad paths are never
in the default set. The temp-root **ownership gate was removed entirely**
(owner decision: trust is now explicit user declaration — cross-platform
consistent, and the gate never protected the root/administrator case). `--root`
remains an exclusive per-invocation override. A `--quiet` flag on all 10
subcommands suppresses stderr advisory notes so stdout JSON stays clean.
Config-input hygiene: blank/whitespace entries dropped; `JERRY_PROJECT` `..`
traversal fails closed; relative `ast.trusted_roots` entries warn-and-honor.
**Scratchpad access** now requires an explicit `ast.trusted_roots` entry or
`--root` (turnkey provisioning tracked in #372). M-08/M-10 containment +
symlink-escape checks are preserved and generalized across the allowed-root
set. Consolidated tournament record:
`adv-tournament-consolidated-optionc.md` (this folder).

---

## Acceptance Criteria

> **Note (2026-08-11):** the always-widen criteria (temp/scratchpad
> auto-trust, temp-root ownership gate) were **superseded by the Option C
> redesign** — see [Fix Approach](#fix-approach) and [History](#history).
> They are struck through below to preserve the record.

- [x] Failing tests written first (H-20 Red)
- [x] `jerry ast` commands accept files within the user's project root
      (`CLAUDE_PROJECT_DIR` env var, else cwd) regardless of where Jerry is
      installed
- [x] Root resolution logic exists once (shared `project_root.py` helper)
      and is used by both `ast_commands.py` and `adapter.py`
- [x] Default allowed roots = the project root **plus** explicitly-configured
      `ast.trusted_roots` entries; no temp/scratchpad directory is
      auto-trusted
- [x] `ast.trusted_roots` read via layered config (env
      `JERRY_AST__TRUSTED_ROOTS` — double underscore — then project config,
      then root config, then default empty); blank/whitespace entries
      dropped; relative entries warn-and-honor; a `JERRY_PROJECT` `..`
      traversal fails closed
- [x] `--root <path>` on all 10 `jerry ast` subcommands makes containment
      exclusive to that resolved path (a project-root file is REJECTED when
      `--root` points elsewhere)
- [x] `--quiet` on all 10 subcommands suppresses stderr advisory notes;
      stdout carries only the JSON/render payload
- [x] M-08/M-10 containment + symlink-escape preserved and generalized across
      the allowed-root set; `ast_modify` writes to the exact resolved path
      the write-time check validated (write-path TOCTOU closed, CWE-367)
- [x] Broad root (filesystem/drive root, `$HOME`, or an ancestor of `$HOME`)
      — for project, configured, AND `--root` — prints a one-line stderr
      WARNING and proceeds; `--quiet` suppresses
- [x] A match via a configured (non-project) trusted root prints a one-line
      stderr transparency note; project-root and `--root` matches do not
- [x] `tests/security/test_adversarial_parsers.py::TestA07PathTraversal`
      green; full suite green with >= 90% coverage (H-21); changelog entry
- [x] C4 adversarial tournament re-score >= 0.92 (S-014 final 0.928 PASS)
- [x] H-02/H-08: `_is_broad_containment_root` flags any ancestor of (or equal
      to) `$HOME` — cross-platform via `PurePath.relative_to()` (covers
      `/home`, `/Users`, `C:\\Users`) — retained under Option C
- [ ] ~~`jerry ast` accepts files under `tempfile.gettempdir()`/`/tmp` by
      default~~ **SUPERSEDED** by Option C (explicit `ast.trusted_roots`)
- [ ] ~~temp/scratchpad default-root R-4 transparency note~~ **SUPERSEDED** —
      generalized to configured-root matches
- [x] ~~H-01 temp-root ownership gate~~ **REMOVED** in Option C (owner
      decision: the gate was the source of two tournament Criticals and never
      protected the root/administrator case; trust is now explicit
      declaration)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-08-07 | in_progress | Created from GH #337 (filed 2026-08-05). Root cause confirmed in code; fix approach = reuse adapter.py's CLAUDE_PROJECT_DIR/cwd resolution via shared helper. Branch fix/BUG-010-ast-project-root off post-#340 main. |
| 2026-08-07 | in_progress | Scope widened per PR #341 owner review: default containment roots extended to temp/scratchpad dirs (`tempfile.gettempdir()`, `/tmp`); added `--root` exclusive-override flag across all `jerry ast` subcommands. eng-lead implementation plan produced; eng-backend executed test-first (H-20): 2 existing containment-rejection tests required a `tempfile.gettempdir`/`_HARDCODED_TMP` monkeypatch seam fix (pytest `tmp_path` lives inside the system tempdir and would otherwise falsely pass containment under the widened roots) — verified both tests fail without the seam before restoring it. Owner-resolved R-3 (broad-root stderr WARNING) and R-4 (temp-match stderr transparency note) implemented and test-covered. |
| 2026-08-07 | in_progress | red-team remediation (RED-BUG010, red-vuln findings): H-01 temp-root ownership gate (`_check_temp_root_ownership`, scoped via new `_is_temp_default_root_match` helper) added to `_check_path_containment` in `ast_commands.py`, closing the multi-user shared-`/tmp` read/write gap (CWE-552/CWE-668/CWE-281). H-02/H-08 `_is_broad_containment_root` widened in `project_root.py` to flag any ancestor of `$HOME` via `PurePath.relative_to()`, closing the `/home`/`/Users`/`C:\Users` incomplete-allowlist gap. eng-backend executed test-first (H-20): 10 new tests written and RED-verified (`AttributeError`/assertion failures) before implementation; GREEN after — 149/149 in the two changed test files, 371/371 across `tests/unit/interface/cli/` + `tests/security/` + `tests/integration/cli/`, `TestA07PathTraversal` re-confirmed green. `ruff format --check` and `ruff check` both exit 0. |
| 2026-08-11 | in_progress | Always-widen scope (auto-trust temp/`/tmp` + `_check_temp_root_ownership` gate) FAILED a C4 adversarial tournament (0.64 REVISE: index-based trust, write-path TOCTOU, fail-open ownership gate, uid-0 multi-tenant, `TMPDIR` poisoning, stderr/JSON corruption). **Redesigned to Option C** (owner-approved): default allowed set = project root + user-declared `ast.trusted_roots`; temp auto-trust AND the ownership gate removed; `--quiet` flag added; config-input hygiene (blank filter, `JERRY_PROJECT` `..` fail-closed, relative warn-and-honor). Pipeline: eng-lead plan -> eng-backend TDD -> red-team re-check (21 cases; 6 prior Criticals dissolved with PoCs; 3 config-hygiene findings AC-11/AC-18/AC-10 fixed) -> eng-reviewer PASS (S-014 0.955). Owner decisions: remove ownership gate; warn-and-honor relative entries; scratchpad de-scoped to explicit config (turnkey provisioning -> #372); config-adapter composition-root cleanup deferred as an optional purist nit (#373); Error->stdout deferred (#371); session-local config-layer gap filed (#370). Commits 62b429e8 -> da34a8b8 -> cce557c5. |
| 2026-08-11 | in_progress | Full C4 blind tournament (10 strategies + eng-reviewer) re-run on Option C @ cce557c5. Consolidated record: `adv-tournament-consolidated-optionc.md`. Six prior Criticals independently re-confirmed dissolved; residual = 1 write-path check-vs-use TOCTOU (corroborated by 5 strategies) plus small code/governance items. Fixes applied test-first: A-1 `ast_modify` now writes to the exact resolved path the write-time check validated (CWE-367 closed); A-2 broad-project-root warning; A-3 whitespace trusted-root entry stripped; A-4 stale docstring; A-5 dead `_get_repo_root` removed; A-6 remediation hint; A-7 Windows symlink-test guards. Governance reconciled: this entity, GH #337, `RESUME-HERE.md`, and a decisions + threat-model note. |
| 2026-08-12 | in_progress | S-014 final re-score: first pass 0.909 REVISE on three doc/consistency items (CHANGELOG Option C entry, `RESUME-HERE.md` self-contradiction, write-time error hint) — closed test-first, commits `a6240a4d` then `e00ed1c4`. **Re-score: 0.928 PASS** (`adv-s014-final-score-optionc.md`). Verified end-to-end via a real `.jerry/config.toml` + the live `jerry` CLI (project-root allow, configured-root allow + note, untrusted reject, `--root` override, env-var path, `--quiet` suppression). GH #371 (`Error:`->stdout, demonstrated during E2E) folded into this unit. Worktracker audit (`wt-audit-optionc.md`) + tidy applied. Acceptance criteria satisfied on the branch; status remains in_progress pending PR #341 merge to main (close-only-after-merge). |
