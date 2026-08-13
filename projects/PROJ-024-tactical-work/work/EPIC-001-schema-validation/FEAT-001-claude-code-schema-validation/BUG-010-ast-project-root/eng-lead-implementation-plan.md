# eng-lead Implementation Plan — BUG-010 Containment Scope Widening (PR #341 follow-up)

> **Step:** 2 of 8 (`/eng-team`) — Engineering Lead and Standards Enforcer
> **Subject:** Widen `jerry ast` path containment to include temp/scratchpad directories and an explicit `--root` override, per owner review comment on PR #341.
> **Status:** PLAN ONLY — no source files modified by this document.
> **Owner directive (verbatim, PR #341 review):** "allow the temp directories as well as those where Claude writes to a scratchpad. We should also allow that Explicit flag so the AST command can be used anywhere. It's at the user's discretion to approve the use of the command or to run and skip permissions. We can only do our reasonable best effort to protect the user."

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Timeline, standards decisions, risk summary, readiness |
| [L1 File-by-File Change Plan](#l1-file-by-file-change-plan) | Exact edits per file with line citations |
| [L1 Test Plan (H-20 Test-First)](#l1-test-plan-h-20-test-first) | Named test functions, Red-phase sequencing |
| [L1 Standards Mapping](#l1-standards-mapping) | H-05/H-07/H-10/H-11/H-20, CWE mapping, docstring policy text |
| [L1 Risks and Mitigations](#l1-risks-and-mitigations) | Table incl. explicit OPEN decisions |
| [L1 Worktracker Delta](#l1-worktracker-delta) | Exact BUG-010 entity edits |
| [L2 Strategic Implications](#l2-strategic-implications) | SAMM trajectory, maintainability, future evolution |
| [Handoff to eng-backend](#handoff-to-eng-backend) | Success criteria, sequencing, open decisions eng-backend must not resolve |

---

## L0 Executive Summary

1. **Scope:** Extend the BUG-010/#337 containment fix (PR #341, already merged-pending: `CLAUDE_PROJECT_DIR`/cwd via `project_root.py`) with two owner-approved widenings: (a) default allowed roots grow from a single project root to a *set* — project root + `tempfile.gettempdir()` + `/tmp` (when it exists) — to cover Claude Code scratchpads on macOS/Linux; (b) a new `--root <path>` flag on all 10 `jerry ast` subcommands that, when supplied, makes the allowed set *exactly* `{resolved --root}` (exclusive override, user-discretion escape hatch).
2. **New function:** `get_containment_roots(explicit_root: str | None = None) -> list[Path]` in `src/interface/cli/project_root.py`. Confirmed H-10-compliant: the file has zero classes today and this adds a second public function only — no violation.
3. **Threading required:** every `ast_*` public function in `ast_commands.py` (10 functions), `_read_file`, `_check_path_containment`, and the `ast_modify` write-time TOCTOU recheck (~line 507-514) all need a `root: str | None = None` parameter added and threaded through. `parser.py` needs a `--root` argument added to all 10 `jerry ast` subparsers. `main.py` `_handle_ast` needs `root=getattr(args, "root", None)` passed to all 10 call sites.
4. **`_get_repo_root()` retained unchanged** (decision, not open) — it becomes a legacy single-root convenience helper, no longer called by containment logic internally, but its existing dedicated test (`test_get_repo_root_when_claude_project_dir_set_then_returns_user_root`) stays green with zero changes. Minimizes diff and risk.
5. **Critical test reconciliation required:** `pytest`'s `tmp_path` fixture lives inside `tempfile.gettempdir()`. Two existing tests in `tests/unit/interface/cli/test_ast_commands.py` (`test_containment_when_file_outside_project_root_then_rejected`, `test_containment_when_symlink_escapes_project_root_then_rejected`) construct their "outside" fixtures from `tmp_path` — under the widened default roots these would silently start PASSING containment (false negative on the security check). The fix is two testability seams in `project_root.py`: a monkeypatchable `_HARDCODED_TMP: Path = Path("/tmp")` module constant, plus reliance on `tempfile.gettempdir()` being called at invocation time (not cached), so tests can fully control the allowed set and construct a genuinely-outside path. **This is a required Red-phase test fix, not optional cleanup — see [L1 Test Plan](#l1-test-plan-h-20-test-first) item T-3.**
6. **A-07 adversarial test unaffected:** `tests/security/test_adversarial_parsers.py::TestA07PathTraversal::test_path_traversal_blocked` calls `_read_file("../../etc/passwd")` with no `root` override and no containment-disabling fixture; two levels up from the repo-root test-runner cwd resolves outside the repo, outside any tempdir, and outside `/tmp` — it stays rejected under the new design. Verify, don't silently assume (T-8 below).
7. **Standards:** H-07 interface-layer isolation holds (`project_root.py`/`ast_commands.py` stay in `src/interface/cli/`, stdlib-only additions — `tempfile`). H-10 verified non-issue (function-only module). H-11/H-12 require full type hints + Google-style docstrings on the new function, including an explicit **user-discretion policy statement** in the `--root` exclusivity docstring (text supplied in [Standards Mapping](#l1-standards-mapping)). H-20 requires the reconciliation tests to be written and shown RED before any `project_root.py`/`ast_commands.py` edit lands.
8. **CWE mapping:** CWE-22 (Path Traversal) and CWE-59 (Improper Link Resolution / symlink following) remain the primary threats the widened surface must still defend against; CWE-367 (TOCTOU) covers the write-time recheck. The widened default surface is a **deliberate, owner-approved risk acceptance** (temp dirs are attacker-writable on shared multi-user hosts) with `--root` as an explicit user-discretion opt-in for "anywhere" — both documented in the risk table below.
9. **Open decisions eng-backend must NOT resolve unilaterally** (see [Risks table](#l1-risks-and-mitigations) and [Handoff](#handoff-to-eng-backend)): (a) whether `--root /` or another very broad root (e.g., `$HOME`, a filesystem root, a drive root) should print a warning, be silently allowed, or be capped/rejected; (b) whether to add a stderr warning whenever containment falls back to a temp-directory default root vs. project root (transparency vs. noise tradeoff).
10. **CI posture:** `ci.yml` runs the matrix on `ubuntu-latest`, `windows-latest`, `macos-latest` (line 253) — the hardcoded `/tmp` check must be a runtime `.exists()` guard (not import-time), so it degrades cleanly to "excluded" on Windows without special-casing `sys.platform`.

---

## L1 File-by-File Change Plan

### 1. `src/interface/cli/project_root.py` (34 lines today)

**Current structure** (full file read): module docstring (L4-11), `import os`/`from pathlib import Path` (L15-16), single public function `get_project_root()` (L19-33).

**Planned edits:**

| Location | Change |
|----------|--------|
| L4-11 (module docstring) | Extend to describe the containment-roots widening: project root **and** temp/scratchpad roots by default, exclusive override via explicit root. Cite BUG-010/GH #337 continuation and the PR #341 owner-review comment. |
| L15-16 (imports) | Add `import tempfile` (stdlib group, alphabetized before `from pathlib import Path` per `coding-standards.md` import grouping — `tempfile` sorts after `os` alphabetically, so order becomes `import os`, `import tempfile`, `from pathlib import Path`). |
| After L16, before `get_project_root` | Add module-level constant: `_HARDCODED_TMP: Path = Path("/tmp")` — a private, monkeypatchable seam (NOT resolved or existence-checked at import time; both happen inside `get_containment_roots` at call time so tests can override it per-test). Docstring-adjacent comment explains this is the macOS scratchpad nuance seam (Claude writes under `/tmp/claude-*` → `/private/tmp`, which is outside `$TMPDIR` on macOS). |
| After `get_project_root` (new function, end of file) | Add `get_containment_roots(explicit_root: str | None = None) -> list[Path]`. See pseudocode below. |

**`get_containment_roots` design (pseudocode — eng-backend implements test-first):**

```python
def get_containment_roots(explicit_root: str | None = None) -> list[Path]:
    """Resolve the set of allowed containment roots for AST path checks.

    When ``explicit_root`` is provided (the CLI ``--root`` flag), the
    allowed set is EXACTLY that one resolved path -- an exclusive
    override. This is a deliberate escape hatch: it is the user's
    discretion to point ``jerry ast`` at any directory they choose, or
    to run the surrounding tool with permission checks skipped. Jerry's
    containment check is best-effort defense against accidental
    traversal, not a security boundary against a user who has already
    chosen to grant the tool broad access via ``--root``.

    Without ``explicit_root``, the allowed set defaults to:
        1. The user's project root (``CLAUDE_PROJECT_DIR`` env var, else cwd).
        2. ``tempfile.gettempdir()``, resolved.
        3. ``/tmp``, resolved, when it exists on this filesystem.

    Roots 2 and 3 exist to cover Claude Code scratchpad writes: on
    macOS, ``tempfile.gettempdir()`` resolves under ``$TMPDIR``
    (``/var/folders/...``), while Claude's scratchpad directories live
    under ``/tmp/claude-*`` (canonically ``/private/tmp/...``) -- a
    different tree. Registering both covers both locations without
    hard-coding Claude-specific paths. On Windows, only
    ``tempfile.gettempdir()`` applies (``/tmp`` will not exist).

    Args:
        explicit_root: The user-supplied ``--root`` CLI value, or None.

    Returns:
        A de-duplicated, order-preserving list of resolved absolute
        Path objects. Exactly one entry when ``explicit_root`` is set.
    """
    if explicit_root is not None:
        return [Path(explicit_root).resolve()]

    roots: list[Path] = [get_project_root().resolve(), Path(tempfile.gettempdir()).resolve()]
    if _HARDCODED_TMP.exists():
        roots.append(_HARDCODED_TMP.resolve())

    # De-duplicate while preserving order (e.g. Linux CI: gettempdir()
    # often IS /tmp; dict.fromkeys() dedupes on Path.__eq__/__hash__).
    return list(dict.fromkeys(roots))
```

**Why `_HARDCODED_TMP` as a module constant instead of a literal `Path("/tmp")` inline:** it is the seam that lets tests neutralize the hardcoded-`/tmp` inclusion (`monkeypatch.setattr(project_root_module, "_HARDCODED_TMP", <nonexistent path>)`) without needing to fake filesystem-level `/tmp` non-existence, which is not reliably mockable across `os.path.exists`/`Path.exists` call sites and would be fragile on CI runners where `/tmp` genuinely exists.

**H-10 check:** file will contain zero classes/protocols before and after this change (two public functions only) — H-10 constrains *classes*, not functions; not a violation. Documented explicitly per the task's request to "verify cohesion vs H-10."

---

### 2. `src/interface/cli/ast_commands.py` (734 lines today)

**Import block (L42-51):** add `get_containment_roots` to the existing `from src.interface.cli.project_root import get_project_root` import (L51) → `from src.interface.cli.project_root import get_containment_roots, get_project_root`.

**`_get_repo_root()` (L159-171): UNCHANGED.** Decision (not open, low-risk, documented): retained verbatim as a legacy single-root helper. It is no longer called by `_check_path_containment` or `ast_modify`'s write-time recheck after this change, but it stays exercised by its existing dedicated test (`test_get_repo_root_when_claude_project_dir_set_then_returns_user_root`, `test_ast_commands.py:1036`) with zero test changes required. Rationale: `get_containment_roots()` calling into `ast_commands._get_repo_root()` would create an upward dependency from `project_root.py` into `ast_commands.py` (layering smell within the same `interface` layer, and unnecessary indirection); `get_containment_roots()` instead calls `get_project_root().resolve()` directly, duplicating one line rather than adding a cross-module call. Coverage impact: none (function still called, still tested).

**`_check_path_containment(file_path: str)` (L174-221) → `_check_path_containment(file_path: str, explicit_root: str | None = None)`:**

| Line(s) | Current | Planned |
|---------|---------|---------|
| L174 | `def _check_path_containment(file_path: str) -> tuple[Path \| None, str \| None]:` | Add param: `def _check_path_containment(file_path: str, explicit_root: str \| None = None) -> tuple[Path \| None, str \| None]:` |
| L175-187 (docstring) | Describes single repo-root containment | Update Args section to document `explicit_root`; update summary to describe multi-root / exclusive-override semantics; cite the owner-review scope widening. |
| L188 | `repo_root = _get_repo_root()` | `allowed_roots = get_containment_roots(explicit_root)` |
| L199-201 | `if not resolved.is_relative_to(repo_root): return None, f"Path escapes repository root: {file_path}"` | `if not any(resolved.is_relative_to(r) for r in allowed_roots): return None, f"Path escapes allowed containment roots: {file_path}"` |
| L203-207 | `if resolved != realpath: if not realpath.is_relative_to(repo_root): return None, f"Symlink target escapes repository root: {file_path}"` | `if resolved != realpath: if not any(realpath.is_relative_to(r) for r in allowed_roots): return None, f"Symlink target escapes allowed containment roots: {file_path}"` |
| L209-219 (M-05 size check) | Unchanged | Unchanged — per task scope, M-05 is explicitly out of scope for this widening. |

Per the agreed design item 3, `resolved` and `realpath` are checked *independently* against the full allowed-roots set (either may satisfy a different root than the other) — this matches the spec's literal wording ("resolved path AND symlink target must each fall within **at least one** allowed root") and is a direct generalization of the existing single-root logic, not a new policy choice.

**`_read_file(file_path: str)` (L224-257) → `_read_file(file_path: str, root: str | None = None)`:**

- L224: add `root: str | None = None` parameter; update docstring Args.
- L241: `resolved, error = _check_path_containment(file_path)` → `resolved, error = _check_path_containment(file_path, root)`.
- L247 (disabled-containment branch): unchanged.

**All 10 `ast_*` public functions — add `root: str | None = None` as the last parameter, threaded to `_read_file`:**

| Function | Signature line | `_read_file` call line | Edit |
|----------|----------------|------------------------|------|
| `ast_parse` | L260 | L273 | append `root: str \| None = None`; `_read_file(file_path, root)` |
| `ast_render` | L288 | L300 | same pattern |
| `ast_validate` | L310 | L340 | append after existing `nav: bool = False` param; `_read_file(file_path, root)` |
| `ast_query` | L419 | L435 | append after `json_output: bool = True`; `_read_file(file_path, root)` |
| `ast_frontmatter` | L451 | L464 | same pattern |
| `ast_modify` | L474 | L491 (read) + L507-514 (write recheck) | see below |
| `ast_reinject` | L559 | L572 | same pattern |
| `ast_detect` | L596 | L611 | same pattern |
| `ast_sections` | L634 | L650 | same pattern |
| `ast_metadata` | L677 | L692 | same pattern |

**`ast_modify` write-time TOCTOU recheck (L507-514) — the change called out explicitly in the task:**

Current:
```python
target_path = Path(file_path).resolve()

# Re-verify path containment immediately before write
if _ENFORCE_PATH_CONTAINMENT:
    repo_root = _get_repo_root()
    if not target_path.is_relative_to(repo_root):
        print(f"Error: Path escapes repository root at write time: {file_path}")
        return 2
```

Planned:
```python
target_path = Path(file_path).resolve()

# Re-verify path containment immediately before write (WI-020, M-21)
if _ENFORCE_PATH_CONTAINMENT:
    allowed_roots = get_containment_roots(root)
    if not any(target_path.is_relative_to(r) for r in allowed_roots):
        print(f"Error: Path escapes allowed containment roots at write time: {file_path}")
        return 2
```

This keeps the write-time recheck honoring the *same* `--root` exclusivity as the read-time check — an unmodified file's `root` argument flows identically to both the L491 read call and the L507-514 write recheck within one `ast_modify` invocation, so there is no window where read and write disagree on the allowed set.

**All other functions (`ast_render` through `ast_metadata`, `token_to_dict`, `node_to_dict`, helpers): docstrings updated (H-12) to document the new `root` parameter where present; no behavioral change beyond the threading above.**

---

### 3. `src/interface/cli/parser.py` (`_add_ast_namespace`, L569-729)

**Current structure:** one parser per subcommand (`parse_parser` L597-605, `render_parser` L608-616, `validate_parser` L619-638, `query_parser` L641-653, `frontmatter_parser` L656-664, `modify_parser` L667-685, `reinject_parser` L688-696, `detect_parser` L699-707, `sections_parser` L710-718, `metadata_parser` L721-729) — each already ends with `parser_var.add_argument("file", help=...)` (and, for `validate`/`query`/`modify`, additional named args after it).

**Planned edits:**

1. Add a new private helper **immediately before `_add_ast_namespace`** (before L569), following the file's existing pattern of small private `_add_*` helpers taking a parser argument:

```python
def _add_root_argument(parser: argparse.ArgumentParser) -> None:
    """Add the shared ``--root`` containment-override flag to an ast subparser.

    When supplied, path containment for this invocation is restricted
    to exactly the resolved ``--root`` directory (BUG-010 scope
    widening, PR #341 owner review) -- an explicit, user-discretion
    escape hatch so ``jerry ast`` can be pointed anywhere. Without this
    flag, the default allowed roots are the user's project root plus
    OS temp/scratchpad directories (see
    ``project_root.get_containment_roots``).

    Args:
        parser: The ast subcommand parser to add the flag to.
    """
    parser.add_argument(
        "--root",
        default=None,
        help=(
            "Restrict path containment to exactly this directory "
            "(overrides the default project-root + temp-dir allowed set). "
            "User discretion: use to run 'jerry ast' against any location."
        ),
    )
```

2. Call `_add_root_argument(<subparser>)` once for **each of the 10** subparsers, immediately after each subparser's `file` argument (and after any other existing arguments, for `validate`/`query`/`modify`, to keep `--root` visually last and consistent in generated `--help` output):
   - `parse_parser` — after L605
   - `render_parser` — after L616
   - `validate_parser` — after L638 (after `--nav`)
   - `query_parser` — after L653 (after `selector`)
   - `frontmatter_parser` — after L664
   - `modify_parser` — after L685 (after `--value`)
   - `reinject_parser` — after L696
   - `detect_parser` — after L707
   - `sections_parser` — after L718
   - `metadata_parser` — after L729

3. Update `_add_ast_namespace`'s docstring (L572-583) to mention the new `--root` flag applies to every listed subcommand.

**Why a shared helper instead of 10 inline `add_argument` calls:** DRY — a single source of truth for the flag's name, default, and help text avoids 10 near-identical blocks drifting out of sync (e.g., inconsistent help text wording), and keeps each subparser block's diff to one line.

---

### 4. `src/interface/cli/main.py` (`_handle_ast`, L393-452)

**Planned edits:** every one of the 10 dispatch lines (L427, L429, L431-435, L437, L439, L441, L443, L445, L447, L449) gets `root=getattr(args, "root", None)` appended as a keyword argument. Example diff for the two representative shapes:

```python
# Simple (parse/render/frontmatter/reinject/detect/sections/metadata) — 7 call sites
if args.command == "parse":
    return ast_parse(args.file, json_output, root=getattr(args, "root", None))
elif args.command == "render":
    return ast_render(args.file, root=getattr(args, "root", None))
...

# validate (named args) — 1 call site
elif args.command == "validate":
    return ast_validate(
        args.file,
        getattr(args, "schema", None),
        nav=getattr(args, "nav", False),
        root=getattr(args, "root", None),
    )

# query (positional selector) — 1 call site
elif args.command == "query":
    return ast_query(args.file, args.selector, json_output, root=getattr(args, "root", None))

# modify (named args) — 1 call site
elif args.command == "modify":
    return ast_modify(args.file, args.key, args.value, root=getattr(args, "root", None))
```

`getattr(args, "root", None)` (not `args.root`) matches the file's existing defensive pattern already used for `schema`/`nav` (L433-434) — safe even if a test constructs a bare `argparse.Namespace`/`FakeArgs` without a `root` attribute (see `TestMainAstRouting`, L931+, which uses hand-built `FakeArgs` classes).

**Docstring update (L393-408):** mention `root` pass-through in the Args description.

---

## L1 Test Plan (H-20 Test-First)

> All tests below MUST be written and shown RED (or, for the two reconciliation fixes, shown to still exercise the *original* red-flag scenario after the seam is added but before `project_root.py`/`ast_commands.py` are edited) before any production code in [File-by-File Change Plan](#l1-file-by-file-change-plan) is written. Coverage target: >= 90% line (H-21) on the touched files; the widened branches (temp-root match, `/tmp` existence branch, `--root` exclusivity, dedup) each need dedicated coverage — no branch should be reachable only incidentally.

### T-1. `tests/unit/interface/cli/test_project_root.py` — new `TestGetContainmentRoots` class

Existing file already imports `get_project_root`; add `get_containment_roots` and `tempfile` to imports, plus `import src.interface.cli.project_root as project_root_module` for seam monkeypatching.

| Test function | Scenario |
|----------------|----------|
| `test_get_containment_roots_when_no_explicit_root_then_includes_resolved_project_root` | Default set contains `get_project_root().resolve()`. |
| `test_get_containment_roots_when_no_explicit_root_then_includes_resolved_gettempdir` | Default set contains `Path(tempfile.gettempdir()).resolve()`. |
| `test_get_containment_roots_when_hardcoded_tmp_exists_then_includes_it` | Monkeypatch `_HARDCODED_TMP` to an existing directory (e.g., `tmp_path`); assert it's in the returned list. |
| `test_get_containment_roots_when_hardcoded_tmp_absent_then_excludes_it` | Monkeypatch `_HARDCODED_TMP` to `tmp_path / "does-not-exist"`; assert the returned list has exactly 2 entries (project root, gettempdir) and the nonexistent path is absent. |
| `test_get_containment_roots_when_gettempdir_equals_hardcoded_tmp_then_deduplicated` | Monkeypatch both `tempfile.gettempdir` and `_HARDCODED_TMP` to resolve to the same directory (simulating Linux CI where `TMPDIR=/tmp`); assert the returned list has no duplicate `Path` entries. |
| `test_get_containment_roots_when_explicit_root_given_then_returns_exactly_that_root` | `get_containment_roots("/some/dir")` returns `[Path("/some/dir").resolve()]` — length 1. |
| `test_get_containment_roots_when_explicit_root_given_then_excludes_project_root_and_tempdir` | With `explicit_root` set to a directory unrelated to project root/tempdir, assert neither the project root nor `tempfile.gettempdir()` appear in the result (exclusivity, not additive). |
| `test_get_containment_roots_when_explicit_root_is_relative_then_resolved_against_cwd` | `explicit_root="relative/dir"` with `monkeypatch.chdir(tmp_path)`; assert result resolves against cwd like `Path.resolve()` would. |

### T-2. `tests/unit/interface/cli/test_ast_commands.py::TestBug010ProjectRootContainment` — new tests

Add `import tempfile` and `import src.interface.cli.project_root as project_root_module` to the test file's imports (both needed for the seam monkeypatches in T-3 and the new tests below).

| Test function | Scenario |
|----------------|----------|
| `test_containment_when_file_in_gettempdir_with_different_project_dir_then_allowed` | **Scratchpad scenario, named explicitly in the task.** `monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "user-project"))` (a *different* directory than the temp file); create `tempfile.gettempdir()`-relative file via `tempfile.mkdtemp()` + write; assert `_check_path_containment(str(that_file))` returns `error is None`. This is the literal Claude-scratchpad-outside-project-root repro from the owner's comment. |
| `test_containment_when_file_in_slash_tmp_then_allowed` | **`/tmp` test, non-Windows only.** `@pytest.mark.skipif(sys.platform == "win32", reason="/tmp is POSIX-only")`. Guard with `if not Path("/tmp").exists(): pytest.skip(...)` for sandboxes without `/tmp`. Write a file under a fresh subdirectory of `/tmp` (e.g. `Path("/tmp") / f"jerry-test-{uuid.uuid4().hex}"`, cleaned up in a `finally`), with `CLAUDE_PROJECT_DIR` pointed elsewhere; assert allowed. |
| `test_containment_when_explicit_root_given_then_file_in_project_root_rejected` | **`--root` exclusivity, named explicitly in the task — CRITICAL.** `CLAUDE_PROJECT_DIR` set to `user_root`; target file lives inside `user_root`; call `_check_path_containment(str(target), explicit_root=str(other_root))` where `other_root` is an unrelated directory; assert `resolved is None` and `error` mentions escaping allowed roots. Proves `--root` is a true override, not additive. |
| `test_containment_when_explicit_root_given_then_file_in_explicit_root_allowed` | Companion positive case: same setup, `explicit_root=str(user_root)` matching the file's actual location; assert allowed even though `CLAUDE_PROJECT_DIR`/tempdir defaults are irrelevant. |
| `test_containment_when_symlink_escapes_from_temp_root_then_rejected` | **Symlink-escape-from-temp, named explicitly in the task.** Use the T-3 seam pattern (monkeypatched `_HARDCODED_TMP` + `tempfile.gettempdir`) to fully control the allowed temp root; place a symlink *inside* that controlled temp root pointing to a real file *outside* all allowed roots (including outside project root); assert rejected with the symlink-escape message. Confirms M-10 still catches symlink escapes even when the symlink itself sits inside a now-allowed temp root. |
| `test_read_file_when_root_argument_provided_then_threaded_to_containment_check` | Directly exercises `_read_file(file_path, root=...)` (not just `_check_path_containment`) to prove the parameter threading at the `_read_file` boundary, independent of any individual `ast_*` function. |
| `test_ast_modify_when_root_given_and_write_target_outside_root_then_rejected_at_write_time` | Exercises the L507-514 write-time recheck specifically: read succeeds (file is inside default roots) but `root="<unrelated dir>"` is passed, so the write-time recheck (not the read-time check) must be what rejects it. Distinguishes "rejected at read" from "rejected at write" failure modes — regression guard for the TOCTOU recheck being wired to the same `root` value as the read. |

### T-3. `tests/unit/interface/cli/test_ast_commands.py::TestBug010ProjectRootContainment` — REQUIRED fixes to existing tests (the reconciliation)

Both edits add the same two-line seam setup at the top of Arrange, using the module-level constants introduced in `project_root.py` ([File-by-File Change Plan §1](#1-srcinterfaceclicliproject_rootpy-34-lines-today)):

```python
monkeypatch.setattr(project_root_module, "_HARDCODED_TMP", tmp_path / "does-not-exist-tmp-marker")
monkeypatch.setattr(
    tempfile, "gettempdir", lambda: str(tmp_path / "controlled-tempdir-not-used-by-test")
)
```

| Test function (existing, `test_ast_commands.py`) | Required change |
|----------------------------------------------------|------------------|
| `test_containment_when_file_outside_project_root_then_rejected` (currently L1087) | Add the two-line seam at Arrange start, **before** `user_root`/`outside`/`target` are created. Without this, `outside = tmp_path / "elsewhere"` is inside the real `tempfile.gettempdir()` on macOS/Linux, and inside the real `/tmp` on Linux CI runners (where `tmp_path`'s base is under `/tmp` by default) — under the new default roots the file would be silently ALLOWED, flipping this security-regression test into a false pass. With the seam, `tmp_path`-derived paths are excluded from both temp default roots, so `outside` is genuinely outside all allowed roots and the test's original intent (M-08 rejection) is honestly preserved. |
| `test_containment_when_symlink_escapes_project_root_then_rejected` (currently L1108) | Same two-line seam addition, same rationale — `outside = tmp_path / "secret"` (the symlink target) is likewise inside the real tempdir/`/tmp` without the seam. |

**Verification step for eng-backend:** after adding the seam and the `project_root.py`/`ast_commands.py` changes, run both tests with the seam temporarily *removed* to confirm they now fail (proving the reconciliation was necessary, not cosmetic) — then restore the seam and confirm green. This is a manual double-check during the Red→Green cycle, not a permanent test artifact.

### T-4. `_disable_path_containment` autouse fixture (L54-65) interplay — no change required, verify only

The fixture sets `ast_commands_module._ENFORCE_PATH_CONTAINMENT = False` for the whole module by default, which short-circuits `_read_file`'s containment branch entirely (L240 `if _ENFORCE_PATH_CONTAINMENT:`) regardless of the roots logic. This means: (a) all pre-existing happy-path `ast_*` tests in this file remain unaffected by the widening (they never reach `_check_path_containment` at all); (b) every new test in T-2/T-3 that needs containment ENFORCED must explicitly re-enable it for that test, following the existing pattern already used implicitly by `TestBug010ProjectRootContainment` (that class's tests call `_check_path_containment`/`_get_repo_root` directly, bypassing `_read_file` and therefore the autouse flag entirely — confirm this remains true for all new T-2/T-3 tests that call `_check_path_containment` directly). For `test_ast_modify_when_root_given_and_write_target_outside_root_then_rejected_at_write_time` (which calls the public `ast_modify` function, going through `_read_file`), the test MUST explicitly override the fixture: `monkeypatch.setattr(ast_commands_module, "_ENFORCE_PATH_CONTAINMENT", True)` at the start of that test, then restore is automatic via monkeypatch's teardown (the outer autouse fixture's own teardown restores `original` afterward, which is safe because monkeypatch's `setattr` is undone before the fixture's `yield` resumes, per pytest's LIFO fixture teardown order — verify this ordering empirically in a spike run before relying on it, since two mechanisms are mutating the same module attribute).

### T-5. `tests/unit/interface/cli/test_ast_commands.py::TestParserAstNamespace` — parser routing test

| Test function | Scenario |
|----------------|----------|
| `test_ast_root_flag_parses_correctly` | `parser.parse_args(["ast", "parse", "file.md", "--root", "/some/dir"])` → `args.root == "/some/dir"`. |
| `test_ast_root_flag_defaults_to_none` | `parser.parse_args(["ast", "parse", "file.md"])` → `getattr(args, "root", None) is None`. |
| `test_ast_root_flag_available_on_every_subcommand` | Parametrized/looped over all 10 subcommands (`parse`, `render`, `validate`, `query`, `frontmatter`, `modify`, `reinject`, `detect`, `sections`, `metadata`) with each command's minimum required positional args, each with `--root /x` appended; assert `args.root == "/x"` for all 10. Prevents silent drift if a future subcommand is added without the flag. |

### T-6. `tests/unit/interface/cli/test_ast_commands.py::TestMainAstRouting` — main.py pass-through test

| Test function | Scenario |
|----------------|----------|
| `test_main_routes_ast_parse_with_root_flag` | Build a `FakeArgs` with `command="parse"`, `file=str(tmp_md_file)`, `root=<some dir containing tmp_md_file>`; call `_handle_ast(FakeArgs(), json_output=False)`; assert exit code 0, proving `root` reaches `ast_parse` and containment passes with an explicit root that actually contains the file. Mirror for `test_main_routes_ast_parse_with_root_flag_rejects_outside_root` (root that does NOT contain the file → exit code 2). |

### T-7. `tests/security/test_adversarial_parsers.py::TestA07PathTraversal` — verification only, no code change expected

`test_path_traversal_blocked` continues to call `_read_file("../../etc/passwd")` with no `root` kwarg (defaults to `None`) and without the `_disable_path_containment` fixture (that fixture lives only in `test_ast_commands.py`, is not autouse-imported into `test_adversarial_parsers.py`, and `_ENFORCE_PATH_CONTAINMENT` therefore reflects the real environment — `JERRY_DISABLE_PATH_CONTAINMENT` unset in the normal `pytest` invocation). **Action for eng-backend:** run this test unmodified after the widening lands and confirm it still asserts `exit_code != 0`; do not silently assume — the two levels of `..` from the pytest-invocation cwd (repo root under normal `uv run pytest` execution) resolve outside the repo, outside `tempfile.gettempdir()`, and outside `/tmp`, so it should remain rejected, but this must be an executed, observed regression check, not an inference. If CI ever invokes pytest with a `cwd` inside a temp directory (it currently does not, per `pyproject.toml` `testpaths = ["tests", "scripts/tests"]` with no `--basetemp`/cwd override observed), this assumption would need re-verification.

### T-8. `tests/integration/cli/test_ast_subprocess.py` — no new tests strictly required, note only

This module already sets `JERRY_DISABLE_PATH_CONTAINMENT=1` for all subprocess tests (L64), so it is unaffected by this widening and needs no changes. Not adding a `--root` subprocess-level test is an accepted scope reduction for this plan; eng-backend MAY add one (e.g., a subprocess invocation of `jerry ast parse <file> --root <dir>` with containment left ENABLED, verifying the flag survives real argv parsing end-to-end) as a stretch goal, but it is not required to satisfy the Acceptance Criteria in [Worktracker Delta](#l1-worktracker-delta).

---

## L1 Standards Mapping

| Standard | Applicability | Enforcement |
|----------|---------------|-------------|
| H-05 (UV-only) | All test/dev commands MUST run via `env -u VIRTUAL_ENV uv run --project <worktree> pytest ...` / `uv run mypy` / `uv run ruff`. | eng-backend command discipline; no `python`/`pip` direct invocation. |
| H-07 (layer isolation) | `project_root.py` and `ast_commands.py` remain in `src/interface/cli/` (outermost layer per `architecture-standards.md`); new imports are stdlib-only (`tempfile`). No domain/application/infrastructure layer is touched by this change, and none of the new code reaches inward into those layers or outward incorrectly. | Architecture test suite (`tests/architecture/`) should already enforce this generically; no new architecture test required since no new cross-layer import is introduced. |
| H-10 (one public class/protocol per file) | Verified non-issue: `project_root.py` has zero classes/protocols before and after (function-only module); H-10 does not constrain function count. Documented explicitly per task instruction. | N/A — no violation to enforce against. |
| H-11 (type hints) | `get_containment_roots(explicit_root: str \| None = None) -> list[Path]` and every threaded `root: str \| None = None` parameter across 10 `ast_*` functions, `_read_file`, `_check_path_containment` MUST carry explicit type hints. | `uv run mypy src/interface/cli/` strict mode (per `testing-standards.md`). |
| H-12 (docstrings) | `get_containment_roots` and `_add_root_argument` MUST have Google-style docstrings (Args/Returns) per `coding-standards.md`. All 10 modified `ast_*` docstrings MUST document the new `root` param. **User-discretion policy text** (verbatim, embed in `get_containment_roots` docstring and `_add_root_argument`'s `--root` help/docstring): *"When ``--root`` is supplied, path containment is restricted to exactly that directory — an explicit, user-discretion escape hatch so `jerry ast` can be used anywhere. Jerry's containment check is best-effort defense against accidental traversal, not a security boundary against a user who has already chosen to grant the tool broad access."* | AST-based docstring presence check (H-33/`/ast` tooling) + code review. |
| H-20 (test-first) | All tests in [L1 Test Plan](#l1-test-plan-h-20-test-first) MUST be written and observed RED (or, for T-3, observed to still catch the original defect) before the corresponding `project_root.py`/`ast_commands.py`/`parser.py`/`main.py` edits land. | Creator-critic-revision cycle; eng-qa verification in Step 4 of `/eng-team`. |
| H-21 (90% coverage) | New branches (temp-root inclusion, `/tmp` existence, dedup, `--root` exclusivity, write-time recheck with `root`) each need dedicated test coverage — no branch reachable only incidentally via an unrelated happy-path test. | `uv run pytest --cov` gate; CI blocks merge below 90% line coverage. |
| CWE-22 (Path Traversal) | Primary threat for the default-roots widening: containment must still reject `../../etc/passwd`-style escapes for ALL allowed roots, not just the project root (T-7 verification). | `_check_path_containment`'s `any(resolved.is_relative_to(r) for r in allowed_roots)` gate; T-1/T-2/T-3/T-7 tests. |
| CWE-59 (Improper Link Resolution / symlink following) | The realpath-vs-resolved independent check (M-10) must hold across the widened root set, including symlinks planted *inside* a now-allowed temp root pointing *outside* all roots (T-2 `test_containment_when_symlink_escapes_from_temp_root_then_rejected`). | Same gate function; dedicated symlink-from-temp test. |
| CWE-367 (TOCTOU) | The `ast_modify` write-time recheck (L507-514, WI-020/M-21) must be re-derived from `get_containment_roots(root)` at write time, using the same `root` value passed at read time within a single invocation, so the exclusivity guarantee of `--root` cannot be bypassed by a race between read-time and write-time root resolution. | T-2 `test_ast_modify_when_root_given_and_write_target_outside_root_then_rejected_at_write_time`. |

---

## L1 Risks and Mitigations

| # | Risk | Mitigation | Status |
|---|------|------------|--------|
| R-1 | `/tmp` (and `tempfile.gettempdir()`) is world-writable on shared multi-user systems; widening default containment to include it broadens the set of locations `jerry ast` will read/write without extra confirmation. | Accepted, owner-approved risk: the owner's review comment explicitly directs this widening ("allow the temp directories... It's at the user's discretion... We can only do our reasonable best effort"). Symlink checks (M-10/CWE-59) and the 1MB size cap (M-05) still apply inside temp roots exactly as inside the project root — no reduction in per-file scrutiny, only an expansion of *where* files may live. | **Accepted, not open** — documented policy per owner directive. |
| R-2 | Symlink TOCTOU: a symlink could validate at `_check_path_containment` time and be swapped (retargeted) before the subsequent read/write completes. | Pre-existing risk, not introduced by this change (`ast_modify` already re-verifies containment immediately before write at L507-514, now updated to reuse `get_containment_roots(root)`). No new mitigation required beyond preserving the existing recheck pattern and threading `root` into it identically at read and write time (T-2 dedicated test). | **Mitigated** — existing pattern preserved. |
| R-3 | `--root /` (filesystem root) or another maximally broad root (`$HOME`, a drive root on Windows) would make containment nearly meaningless while still nominally "passing" the check. | **OPEN DECISION — recommend but do not silently decide:** (a) allow silently (pure user-discretion interpretation of the owner's comment), (b) allow but print a stderr warning when the resolved `--root` is a filesystem root or equals `Path.home()`, or (c) reject/cap. **eng-lead recommendation: (b)** — a low-cost, non-blocking stderr warning preserves "best effort to protect the user" without overriding explicit user intent (which would contradict the owner's directive that this is the user's discretion). This MUST be confirmed by the user/PR owner before eng-backend implements it, since it is a UX/policy tradeoff, not a pure engineering detail. | **OPEN — requires owner/user confirmation, do not resolve unilaterally.** |
| R-4 | Silent default-root fallback: when no `--root` is given and the file happens to fall inside a temp directory rather than the project root, the user gets no signal that containment matched via the "wider" default set rather than their actual project. | **OPEN DECISION, secondary to R-3:** should `_check_path_containment` (or a caller) emit a stderr note when the matched root is a temp default rather than the project root, for transparency? **eng-lead recommendation:** defer — this is lower priority than R-3 and adds output-format risk (JSON-mode callers must not have stderr diagnostics leak into stdout JSON); flag as a follow-up enhancement rather than blocking this fix, but note it explicitly here so it isn't silently dropped. | **OPEN — recommend deferral, confirm with user before closing.** |
| R-5 | Windows: `Path("/tmp")` under `PureWindowsPath` semantics resolves as a drive-relative root (e.g., `X:\tmp` on the current drive) rather than "no such concept as /tmp." If such a directory happens to exist on a Windows CI runner or user machine, it would be silently included. | `_HARDCODED_TMP.exists()` is a runtime, not import-time, guard — on the `windows-latest` CI matrix leg (`ci.yml:253`) this will almost always evaluate `False` (no `X:\tmp` present) and correctly exclude it; if a Windows user genuinely has a `\tmp` directory at their current drive root, it becomes an allowed default root, which is a narrow edge case consistent with "best effort," not a regression from current behavior (today's single-root check has no Windows-specific gap either). | **Accepted, low-likelihood edge case** — documented, not blocking. |
| R-6 | Test reconciliation risk: if T-3's seam fix is skipped or done incorrectly, two existing security-regression tests silently stop testing what their names claim (false confidence in CI green). | T-3 mandates writing the seam BEFORE the production change, and mandates a manual verify-then-restore double-check (temporarily removing the seam to confirm the tests fail without it) as part of the Red→Green cycle. | **Mitigated by process** — see T-3. |
| R-7 | `--root` accepting a nonexistent directory: `get_containment_roots(explicit_root)` does not validate existence, so `--root /does/not/exist` silently "succeeds" at the containment-roots level (any file check against it will simply always fail `is_relative_to` unless the file itself is under that nonexistent path, which is impossible). | No behavior change needed — this mirrors the existing `get_project_root()` contract, which also never validates `CLAUDE_PROJECT_DIR`/cwd existence. Consistent, not a new gap. | **Accepted — consistent with existing contract, not open.** |

---

## L1 Worktracker Delta

Target entity: `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/BUG-010-ast-project-root.md`

Current entity is `status: in_progress` (frontmatter L1-10), with `## Fix Approach` (L53-57) describing only the PR #341 scope (shared `project_root.py` helper, `CLAUDE_PROJECT_DIR`/cwd), and 5 acceptance criteria (L59-65) that are already satisfied by PR #341. This is a **scope continuation within the same entity** (owner review comment on the same PR, same GH issue #337) — no new entity required.

**Edit 1 — `## Fix Approach` section (append, do not replace, after L57):**

```markdown
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
single root to "any of the allowed roots."
```

**Edit 2 — `## Acceptance Criteria` section (append 4 new checkboxes after existing L61-65, do not renumber/remove existing):**

```markdown
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
```

**Edit 3 — `## History` table (append row after L73):**

```markdown
| 2026-08-07 | in_progress | Scope widened per PR #341 owner review: default containment roots extended to temp/scratchpad dirs (`tempfile.gettempdir()`, `/tmp`); added `--root` exclusive-override flag across all `jerry ast` subcommands. eng-lead implementation plan produced; eng-backend to execute test-first (H-20). Two existing containment-rejection tests require a `tempfile.gettempdir`/`_HARDCODED_TMP` monkeypatch seam fix (pytest `tmp_path` lives inside the system tempdir and would otherwise falsely pass containment under the widened roots). |
```

**Schema validity check:** the frontmatter block (L1-10: Type, Status, Priority, Severity, Impact, Created, Parent, GitHub Issue) is untouched by these edits — no field changes, `status` remains `in_progress` (work continues under the same GH issue #337 / PR #341 thread, no status transition warranted by a plan-only artifact). Section structure (`## Summary`, `## Steps to Reproduce`, `## Root Cause`, `## Fix Approach`, `## Acceptance Criteria`, `## History`) and the navigation table (L12-21, H-23) are unaffected — appends only, no heading changes, no anchor-link changes. Validate with `uv run jerry ast validate <entity-path> --schema bug` after edits land (eng-backend responsibility, not performed by this plan).

**CHANGELOG.md note:** `CHANGELOG.md` `[Unreleased]/### Fixed` already has a BUG-010 bullet (for PR #341's `CLAUDE_PROJECT_DIR`/cwd fix, referencing `#337`). eng-backend SHOULD append a second `### Fixed` (or amend the existing) bullet for this widening, e.g.: *"**BUG-010 (follow-up)**: widen `jerry ast` containment defaults to include OS temp/scratchpad directories and add a `--root` exclusive-override flag, per PR #341 owner review (#337, #341)."* — satisfies the BUG-010 AC-5 "changelog entry added" for this increment specifically.

---

## L2 Strategic Implications

**SAMM trajectory:** this change sits in OWASP SAMM's *Implementation → Secure Build* and *Design → Security Requirements* practices. The project root/containment-roots pattern established here (a resolvable, testable, explicitly-overridable allowed-set function with a documented user-discretion boundary) is a reusable pattern for any future Jerry CLI surface that touches the filesystem outside the immediate project tree (e.g., future `jerry agents build` output paths, transcript ingestion from arbitrary user-supplied locations). Recommend this plan's `get_containment_roots` shape (default set + exclusive override + testability seams) become the house pattern, referenced from `agent-development-standards.md` or a new `path-containment-standards.md` if a third CLI surface needs the same treatment — avoid three independent reimplementations of "resolve allowed roots" drifting apart.

**Technical debt risk:** the `_get_repo_root()` retention (unchanged, now internally unused by containment logic) is a small, deliberate debt item — a future reader may reasonably ask "why does this exist and nothing calls it?" Recommend a one-line comment at its definition site (not scripted here, left to eng-backend judgment during implementation) noting it is retained solely for its existing test and as a documented single-root convenience accessor, superseded for containment purposes by `get_containment_roots`. If a future refactor removes it, that removal should be its own small, reviewed change — not bundled into this one.

**Maintainability:** threading a `root: str | None = None` parameter through 10 near-identical function signatures is repetitive by design (matches the existing repetitive `_read_file` call pattern already present in the file) rather than introducing a decorator or wrapper abstraction. This is a deliberate low-abstraction choice for this codebase's current size (734-line file, 10 flat functions) — recommend revisiting only if the `ast_*` function count grows materially (e.g., past ~15-20), at which point a shared `@with_containment_check` decorator or a small `AstCommandContext` dataclass carrying `file_path`/`root`/`json_output` would reduce duplication. Not recommended now — premature abstraction for the current scale.

**Dependency strategy:** no new third-party dependencies introduced; `tempfile` is stdlib. This keeps the security-relevant surface area minimal — no supply-chain risk assessment beyond what already applies to the existing dependency set.

---

## Handoff to eng-backend

**Task:** Implement the file-by-file plan above, test-first (H-20), in the order: (1) T-1/T-2/T-3 tests written and observed RED/verified per T-3's manual double-check, (2) `project_root.py` edits, (3) `ast_commands.py` edits, (4) `parser.py` edits + T-5 tests, (5) `main.py` edits + T-6 tests, (6) T-7 verification run (no code change expected), (7) worktracker entity edits, (8) CHANGELOG.md entry, (9) full suite green at >= 90% coverage (H-21), `uv run mypy`, `uv run ruff check`.

**Success criteria:**
- All named test functions in [L1 Test Plan](#l1-test-plan-h-20-test-first) exist, pass, and were observed RED before the corresponding implementation.
- `test_containment_when_file_outside_project_root_then_rejected` and `test_containment_when_symlink_escapes_project_root_then_rejected` pass WITH the seam and were manually confirmed to FAIL without it (T-3).
- `tests/security/test_adversarial_parsers.py::TestA07PathTraversal::test_path_traversal_blocked` passes unmodified (T-7).
- `--root` flag present and functional on all 10 `jerry ast` subcommands (T-5).
- Coverage >= 90% on `src/interface/cli/project_root.py` and `src/interface/cli/ast_commands.py`.

**Open decisions eng-backend must NOT resolve unilaterally (route back to user/PR owner for confirmation):**
1. **R-3:** whether `--root /` (or another maximally broad root such as `$HOME` or a drive root) should be silently allowed, allowed-with-stderr-warning (eng-lead recommendation), or capped/rejected.
2. **R-4:** whether to add a stderr transparency note when default containment matches via a temp-directory root rather than the project root (eng-lead recommendation: defer as follow-up, do not block this fix on it).

**Confidence:** 0.85 — plan is grounded in direct reads of all four touched files (exact line citations throughout) and the existing test suite's actual fixture behavior (confirmed via direct read of the reconciliation-affected tests and the A-07 adversarial test), not inference. Residual uncertainty is limited to the two explicitly-flagged open policy decisions (R-3/R-4) and one process-verification item (T-4's monkeypatch/fixture teardown ordering, flagged for empirical confirmation during implementation rather than assumed).
