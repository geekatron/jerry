# red-vuln Option C Execution Report — BUG-010 `jerry ast` Containment (Trusted Roots)

> **Engagement:** RED-BUG010 (re-check pass 2) — red-vuln execution of red-lead's Option C attack plan (AC-1..AC-21).
> **Agent:** red-vuln (Vulnerability Analyst) — executes against `projects/.../BUG-010-ast-project-root/red-lead-option-c-attack-plan.md`.
> **Target:** Branch `fix/BUG-010-ast-project-root` @ `da34a8b8`. Files under test: `containment_policy.py`, `project_root.py`, `ast_commands.py`, `env_config_adapter.py`, `layered_config_adapter.py`, `parser.py`.
> **Method:** White-box source review + in-process behavioral PoC (real shipped functions, sandboxed `mkdtemp` fixtures) + one real end-to-end `uv run jerry ast` CLI invocation. No production source modified; no writes outside disposable sandboxes; no real credentials used (synthetic placeholder strings only).
> **Authorization:** Per red-lead RoE — repo owner (geekatron), PR #341 defensive review.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict counts, ranked findings, headline call |
| [L1 Group A — Confirm Prior Criticals Dissolved (AC-1..AC-6)](#l1-group-a--confirm-prior-criticals-dissolved-ac-1ac-6) | C1–C6 re-verification results |
| [L1 Group B — New Option C Surface (AC-7..AC-18)](#l1-group-b--new-option-c-surface-ac-7ac-18) | trusted_roots config-channel results |
| [L1 Group C — Cross-Platform Correctness (AC-19..AC-21)](#l1-group-c--cross-platform-correctness-ac-19ac-21) | Windows/case-sensitivity/POSIX-assumption results |
| [L1 Ranked Findings](#l1-ranked-findings) | Confirmed findings with severity, repro, fix |
| [L2 Strategic Implications](#l2-strategic-implications) | Systemic recommendation, coverage disclosure |
| [Constitutional Compliance](#constitutional-compliance) | P-001/P-002/P-020/P-022 attestation |

---

## L0 Executive Summary

**21/21 attack cases executed.** 17 DISSOLVED (secure) or SAFE-by-construction, **3 CONFIRMED FINDINGS**, 1 case (AC-19) DISSOLVED-with-disclosed-limitation (reasoning + same-flavor-mocked validation only; no live Windows host available in this environment).

Option C's headline claim holds: the pass-1 Criticals (C1 index-trust, C2 TOCTOU, C3/C4 ownership fail-open, C5 temp-channel widening, C6 quiet-suppression) are genuinely dissolved by construction, not merely patched — every Group A case reproduced the expected-SAFE behavior against the real `da34a8b8` code, including an actual read→write symlink-swap TOCTOU PoC against `ast_modify` that confirmed rejection.

The residual risk is exactly where red-lead predicted: the config channel. Three real findings confirmed, all in the LOW–MEDIUM band, all in the "trusts declared strings without normalization" class:

| # | Case | Finding | Severity |
|---|------|---------|----------|
| 1 | AC-11 | Empty/whitespace `ast.trusted_roots` entry silently resolves to and trusts `cwd` | **MEDIUM** |
| 2 | AC-18 | `JERRY_PROJECT` path traversal can steer the project-config file read outside the `projects/` tree | **MEDIUM** |
| 3 | AC-10 | Relative `ast.trusted_roots` entries are invocation-cwd-dependent (including upward `..` escape) with zero runtime signal | **LOW** |

No finding reaches CRITICAL or HIGH under this engagement's rubric: none defeats containment under pure default config with zero config-channel action, and none is a write escape independent of a config-channel precondition.

---

## L1 Group A — Confirm Prior Criticals Dissolved (AC-1..AC-6)

### AC-1 — C1: No residual index/position-based trust in classification
**Precondition:** Default set with ≥2 `configured` entries. **Steps:** Built `resolve_allowed_roots()` with two configured roots in both orders; nested the project root inside a configured tree; duplicated a configured root against the project root. **Observed:** `grep -nE "allowed_roots\[|roots\[|.\[0\]"` against `containment_policy.py`/`ast_commands.py` returned zero matches. Reordering `[conf_a, conf_b]` → `[conf_b, conf_a]` did not change any classification (`project` always first regardless of position, `configured` for the rest). A project root nested inside a configured tree stayed classified `"project"`. A configured root duplicating the project root deduped to 2 entries, retaining `"project"` classification (`containment_policy.py:152-172`).
**VERDICT: DISSOLVED (secure).** Classification is purely origin-derived; no index-based trust signal exists anywhere in the enforcement path.

### AC-2 — C2: `ast_modify` read→write symlink swap caught by write-time re-resolution
**Precondition:** `link.md` inside the project root, initially pointing to an in-root target; `_ENFORCE_PATH_CONTAINMENT=True`.
**Steps (real PoC against the shipped `ast_modify`):** (1) `_read_file(link.md)` succeeds (link → in-root target). (2) Attacker action: `link.md` unlinked and re-symlinked to `outside/secret.md` (a synthetic-content file entirely outside all allowed roots). (3) Ran the identical write-time recheck `ast_modify` performs (`_check_path_containment`, `ast_commands.py:634-638`) and then the full `ast_modify()` call end-to-end.
**Observed:**
```
Step 3 (write-time recheck): REJECTED -- Path escapes allowed containment roots: .../project/link.md
Full ast_modify() call with link pointing outside: exit_code= 2
Outside secret file unmodified? True
```
Also confirmed: (a) an in-root symlink write succeeds and lands on the dereferenced real target (`inroot_target.md` content updated correctly, not a stale path); (b) a swap to a *different* allowed (`configured`) root also succeeds and writes the resolved target, not a stale one.
**VERDICT: DISSOLVED (secure).** `ast_modify`'s write-time recheck is literally the same function (`_check_path_containment`) called at read time, including a fresh `os.path.realpath()`. A read→write symlink swap to an outside target is rejected before any write occurs (`ast_commands.py:620,634-638,654`); the outside file was verified byte-for-byte unmodified after the PoC.

### AC-3 — C3/C4: Ownership/UID gate fully removed; no fail-open on a security decision
**Steps:** `grep -nE "st_uid|geteuid|os\.name|_check_temp_root_ownership|_is_temp_default_root_match"` across `ast_commands.py`, `project_root.py`, `containment_policy.py`. Audited every `except` on the enforcement path (`ast_commands.py:249` resolve error, `:278` stat error).
**Observed:** Zero matches (grep returncode 1). Both audited excepts return an error result — fail-closed, never silently pass.
**VERDICT: DISSOLVED (secure).** No ownership/UID logic survives in `da34a8b8`; DD-2 removal confirmed by absence, not inference.

### AC-4 — C3 residual: broad-detection fail-open changes an *enforcement* outcome
**Precondition:** `Path.home()` monkeypatched to raise `RuntimeError`.
**Steps:** Called `_is_broad_containment_root(Path("/"))` and on an ordinary directory under the raising-home condition; then called `resolve_allowed_roots(ordinary, [Path("/")], None)` under the same condition to check whether the *allow/deny* decision (root inclusion) is affected.
**Observed:**
```
Path.home() raises -> filesystem root still broad: True
Path.home() raises -> ordinary dir broad: False
roots still include broad configured root (allowed, just flagged): [(..., 'project', False), ('/', 'configured', True)]
```
**VERDICT: DISSOLVED (secure).** `Path.home()` failure suppresses only the ancestor-of-home *warning* path (`containment_policy.py:88-94`); the drive-root check (`len(parts)<=1`, `:86`) is unaffected, and root *inclusion* in `resolve_allowed_roots` never depends on `is_broad`.

### AC-5 — C5: No `tempfile`/`TMPDIR`/`/tmp` feeds the allowed-root set
**Steps:** `grep` for `gettempdir|_HARDCODED_TMP|tempfile|TMPDIR` in `project_root.py`/`containment_policy.py` (matches only in docstrings/comments); `grep` for `tempfile` in `ast_commands.py` (only `mkstemp` write-staging at `:644`). Behavioral: set `TMPDIR` to an attacker-chosen directory, force `tempfile.tempdir = None` to pick it up, call `get_containment_roots()` with no `--root`/no config, and attempt to read a file placed under `gettempdir()`.
**Observed:**
```
tempfile.gettempdir() now reports: .../attacker_tmp
default containment roots: [(.../project, 'project')]
Read of file under gettempdir() by default: REJECTED
```
**VERDICT: DISSOLVED (secure).** Default allowed set is exactly `[project_root]`; `TMPDIR`/`TEMP`/`TMP` have zero effect on containment; a `gettempdir()` file is rejected by default.

### AC-6 — C6: `--quiet` never suppresses enforcement; no advisory note reaches stdout
**Precondition:** A `configured`-root match (R-4 note condition).
**Steps:** Ran `_read_file` with `quiet=False` and `quiet=True` against (a) a file under a configured root, (b) a file outside all roots; captured stdout/stderr separately for each; ran `ast_modify` against the outside file to confirm the hard-coded `quiet=True` write-time recheck (`ast_commands.py:635`, DD-3) still enforces.
**Observed:**
```
quiet=False: allowed_configured_root_read code=0 stderr_has_note=True stdout_has_note=False
quiet=True:  allowed_configured_root_read code=0 stderr_has_note=False stdout_has_note=False
quiet=False/True: outside_file_read code=2 (identical both states)
ast_modify on outside file (write-time recheck forced quiet=True): 2
```
**VERDICT: DISSOLVED (secure).** `--quiet` (and the internal hard-coded `quiet=True` at write time) suppresses only stderr advisory text; the allow/deny outcome is bit-for-bit identical in both states; no advisory note reached stdout in any run.
**Robustness note (not escalated, pre-existing, not a Group-C/C6 regression):** `ast_commands.py:311,318,463,614,637` use bare `print(f"Error: ...")` → **stdout**, not stderr. This replaces (not corrupts) the JSON payload for a JSON consumer piping `jerry ast ... | jq`, and was already true before this redesign. Recommend routing these to stderr in a follow-up, but it is out of scope for this containment re-check.

---

## L1 Group B — New Option C Surface (AC-7..AC-18)

### AC-7 — `ast.trusted_roots` precedence order is exactly env > project > root > default
**Steps:** Configured distinguishable values at root config (`R`), project config (`P`, anchored via `JERRY_PROJECT`), and env (`E`); read back at each layering combination; then removed `JERRY_PROJECT` to confirm the project layer is skipped, not silently substituted.
**Observed:** `root-only → [R]`; `root+project → [P]` (project wins); `root+project+env → [E]` (env wins); `no JERRY_PROJECT → [R]` (falls through to root, project layer correctly absent).
**VERDICT: DISSOLVED (secure).** Precedence is exactly env > project > root > `[]`; project config path anchors to `get_project_root().resolve()` (`project_root.py:85,90`), never the Jerry install tree.

### AC-8 — Env-key mapping: single-underscore mis-form is a safe no-op, not a silent widen
**Steps:** Set `JERRY_AST_TRUSTED_ROOTS` (single underscore), the correct `JERRY_AST__TRUSTED_ROOTS`, and an over-underscored `JERRY_AST__TRUSTED__ROOTS`; read `_load_trusted_roots()` after each.
**Observed:** `single-underscore → []` (safe no-op); `correct form → ['/correct']`; `over-underscored → []` (safe no-op).
**VERDICT: DISSOLVED (secure).** Only the exact double-underscore form takes effect (`env_config_adapter.py:69-82`, `key.lower().replace("__", ".")`); every mis-form fails safe, none widens trust.

### AC-9 — Env value parsing: scalar/CSV/JSON coercion cannot inject an unintended root
**Steps:** Exercised `JERRY_AST__TRUSTED_ROOTS` as JSON array, bare CSV, single scalar, and a value containing an un-quoted comma inside a path.
**Observed:** JSON/CSV/scalar all parsed to exactly the declared paths. The comma-in-path case (`/a,b/x`) split into `['/a', 'b/x']` per the unquoted-CSV heuristic (`env_config_adapter.py:145-147`).
**VERDICT: DISSOLVED for security purposes; correctness foot-gun noted (INFO, not ranked).** No crafted value produced a *broader* set than declared — the comma-split only mangles a path the same user who wrote the config already controls; it does not synthesize a new attacker-controlled root. Recommend documenting "avoid literal commas in `ast.trusted_roots` string-form entries; use the TOML array form" as a usability note, not a security fix.

### AC-10 — Relative `trusted_roots` entry resolves against cwd (invocation-dir-dependent trust) — **FINDING (LOW)**
**Precondition:** `ast.trusted_roots = "scratch"` (relative), invocation cwd variable.
**Steps:** Set the relative entry; called `get_containment_roots()` from cwd `A/B`, then from cwd `X/Y`; separately tested `../shared`.
**Observed:**
```
cwd=A/B: configured root -> A/B/scratch
cwd=X/Y: configured root -> X/Y/scratch   (a DIFFERENT, possibly-nonexistent directory)
cwd=A/B, entry='../shared': configured root -> A/shared   (upward escape via ..)
```
No warning or note is emitted for a relative entry at any point — the "foot-gun" is only documented in a source docstring (`project_root.py:109-111`), never surfaced to the user at runtime.
**VERDICT: FINDING CONFIRMED.** Identical configuration silently trusts a different absolute directory depending on where `jerry ast` happens to be invoked from, and a `..`-laden entry escapes upward with zero signal. See [Ranked Findings](#l1-ranked-findings) #3.

### AC-11 — Empty/whitespace `trusted_roots` entry silently resolves to cwd — **FINDING (MEDIUM), highest-value case**
**Precondition:** `JERRY_AST__TRUSTED_ROOTS=""` (or a stray `""`/whitespace entry via CSV trailing comma or a TOML array), `CLAUDE_PROJECT_DIR` ≠ cwd.
**Steps (in-process trace, then real end-to-end CLI PoC):**
1. Traced the exact data flow: `EnvConfigAdapter._parse_value("")` → `""` (`env_config_adapter.py:115-117`) → `get_list()` wraps to `['']` (no filtering) → `_load_trusted_roots()` returns `['']` (`project_root.py:118`) → `get_containment_roots()` does `Path(entry).resolve()` per raw entry with **no falsy/blank filter** (`project_root.py:174`) → `Path("").resolve()` == `cwd`.
2. Confirmed a CSV trailing-comma entry (`"/a,"` → `["/a", ""]`) and a whitespace-only entry (`"  "`) both reach `Path(...).resolve()` unfiltered and both resolve to (or under) cwd.
3. Ran the **real shipped CLI**: `CLAUDE_PROJECT_DIR=<project> JERRY_AST__TRUSTED_ROOTS="" uv run jerry ast frontmatter <file-under-cwd-outside-project>` from a cwd distinct from the project root.
**Observed (real CLI transcript):**
```
STDOUT:
{
  "key": "value"
}
STDERR:
Note: '.../cwd_outside_project/secret.md' is outside the project root; jerry ast is
operating outside the project root via a configured trusted root: .../cwd_outside_project.
EXIT CODE: 0
```
No `Warning:` (broad-root) line fired — cwd is essentially never "broad" by the `_is_broad_containment_root` definition, so the *only* signal a user gets is the generic R-4 "operating outside project root via a configured trusted root" note, which looks identical to a legitimately-configured trusted root and gives no indication the trust originated from a degenerate empty value.
**VERDICT: FINDING CONFIRMED**, matching red-lead's pre-assessment exactly. See [Ranked Findings](#l1-ranked-findings) #1.

### AC-12 — Configured root that is a symlink resolves safely (no additive escape)
**Steps:** Configured a symlinked directory (`link_root -> real_root`) as a trusted root; separately configured a symlink pointing to `/`.
**Observed:** The configured root resolved to `real_root` only; `link_root` itself never appeared in the allowed set (no double-trust). The symlink-to-`/` case correctly flagged `is_broad=True` and fired the R-3/DD-1 warning for its *resolved* target.
**VERDICT: DISSOLVED (secure).** `Path(entry).resolve()` (`project_root.py:174`) fully dereferences before both classification and broadness checks; no lexical/symlink divergence.

### AC-13 — Configured root containing `..` is normalized before trust
**Steps:** Configured `<nested>/../..` (collapses to a shallower ancestor); read back the resolved, classified root.
**Observed:** The entry collapsed exactly to the expected ancestor before both broadness detection and containment comparison — no lexical-vs-real mismatch.
**VERDICT: DISSOLVED (secure).**

### AC-14 — `is_relative_to` is component-wise, not string-prefix (sibling escape)
**Steps:** Project root `.../a/b`; file at sibling `.../a/bc/secret.md`; attempted read via `_read_file`.
**Observed:** `code=2` (rejected). `is_relative_to` correctly treats `/a/bc` as NOT inside `/a/b`.
**VERDICT: DISSOLVED (secure).** No string `startswith`/prefix logic exists; component-wise `Path.is_relative_to` is used throughout (`ast_commands.py:257,266`).

### AC-15 — Project root resolving inside a configured (or temp) tree does not re-open C1
**Steps:** Nested `CLAUDE_PROJECT_DIR` inside an `ast.trusted_roots`-configured directory; read a project-root file (expect no R-4 note) and an outer-configured-only file (expect R-4 note).
**Observed:** Project entry stayed classified `"project"` (first, per `resolve_allowed_roots`); project-root file read cleanly with no note; outer-configured-only file read with the R-4 note firing correctly.
**VERDICT: DISSOLVED (secure).** Nesting is benign; classification remains purely origin-based.

### AC-16 — Broad configured root: warning fires for `configured`, broadness detection is complete (POSIX)
**Steps:** Configured each of filesystem root `/`, exact `$HOME`, and `$HOME`'s parent (ancestor-of-home) as `ast.trusted_roots`; captured stderr for each. Additionally tested **two simultaneous broad `configured` entries** to confirm the warning is emitted per-entry, not just for the first.
**Observed:** All three shapes flagged `is_broad=True` and fired the distinct `configured`-classification warning wording; invocation proceeded in every case (DD-1 accepted policy). Two-broad-entries test emitted exactly 2 warnings, one per entry.
**VERDICT: DISSOLVED (secure) on POSIX.** The H-02 fix is present and wired to the `configured` classification (`project_root.py:189-197`), not only `explicit`; coverage is complete for every configured entry, not just the first match.

### AC-17 — `--root` exclusivity cannot be combined with configured roots to widen
**Steps:** Set both `--root X` and `ast.trusted_roots` (a different directory); called `get_containment_roots(explicit_root=X)`; attempted reads of a configured-root file and a project-root file under `--root X`.
**Observed:** Returned set was exactly `[X as "explicit"]`. Both the configured-root file and the project-root file were **rejected** under `--root X` (`code=2` for both).
**VERDICT: DISSOLVED (secure).** `--root` is a true exclusive override; configured roots and project root are entirely ignored when it is set (`project_root.py:169-171`).

### AC-18 — Config read cannot be steered to a file outside the user's project — **FINDING (MEDIUM)**
**Steps:** Set `JERRY_PROJECT="../../elsewhere"` with a real `projects/` directory present under the project root (the realistic case — every actual Jerry project has one); planted a `config.toml` with a distinct `ast.trusted_roots` value at the traversed-to location outside the `projects/` tree; called `build_layered_config_adapter()` / `_load_trusted_roots()`.
**Observed (two-stage confirmation):**
1. With no `projects/` directory present, `Path.exists()` on the unresolved `root/projects/../../elsewhere/.jerry/config.toml` returned `False` (OS path resolution requires the intermediate `projects/` component to exist), so the naive test did **not** reproduce.
2. With `projects/` created (the realistic condition for every real Jerry project), the exact same traversal **did** reproduce:
```
_load_trusted_roots() -> ['/tmp/attacker-planted']
get_containment_roots() -> [(<project>, 'project'), ('/private/tmp/attacker-planted', 'configured')]
```
**VERDICT: FINDING CONFIRMED.** `project_config_path = root / "projects" / jerry_project / ".jerry" / "config.toml"` (`project_root.py:88-90`) performs no validation that `jerry_project` stays within `projects/`; a `..`-laden `JERRY_PROJECT` value causes the project-config file to be read from an attacker-reachable location outside the project tree whenever that location exists on disk. See [Ranked Findings](#l1-ranked-findings) #2.

---

## L1 Group C — Cross-Platform Correctness (AC-19..AC-21)

### AC-19 — Windows broad-root detection completeness (drive root, `C:\Users`, UNC)
**Steps:** (1) Flavor-independent check: evaluated `PureWindowsPath("C:\\")` and `PureWindowsPath("\\\\host\\share")` against `_is_broad_containment_root` directly (the `len(parts)<=1` branch is pure and needs no OS support). (2) Same-flavor validation: since this assessment runs on macOS/POSIX, `Path.home()` natively returns a `PosixPath`, so any `PureWindowsPath` compared against it hits the function's own `(ValueError, TypeError)` guard and returns `False` — this is a **test-harness limitation, not evidence of a real gap**. To validate the underlying algorithm itself, `Path.home` was monkeypatched to a same-flavor `PureWindowsPath`-derived stand-in (`.resolve()` returning self) representing `C:\Users\alice`, and `_is_broad_containment_root(PureWindowsPath("C:\\Users"))` was re-evaluated under that same-flavor condition.
**Observed:**
```
PureWindowsPath("C:\\")                  -> True   (drive root, flavor-independent)
PureWindowsPath("\\\\host\\share")       -> True   (UNC share root, flavor-independent)
PureWindowsPath("C:\\Users") vs POSIX Path.home()          -> False  (cross-flavor TypeError guard; harness artifact)
PureWindowsPath("C:\\Users") vs same-flavor mocked WinHome -> True   (algorithm correctly flags it)
PureWindowsPath("\\\\host\\share\\sub") (UNC subpath)      -> False  (documented residual, same class as H-08)
```
**VERDICT: DISSOLVED for the algorithm, with an honest limitation disclosed (P-022).** The `len(parts)<=1` and `relative_to()`-based ancestor-of-home logic (`containment_policy.py:86-107`) is flavor-agnostic pure `pathlib` with no POSIX-specific assumption baked in — same-flavor mocking proves `C:\Users` is correctly flagged when `Path.home()` is genuinely Windows-flavored (i.e., on a real Windows host). **This assessment did NOT execute on a live win32 interpreter**; the full wiring through `get_containment_roots()`'s `configured` classification on an actual Windows host was reasoned and same-flavor-mocked, not behaviorally observed end-to-end. CI (`windows-latest`, already in the plan's stated scope) is the authoritative validation surface; recommend a dedicated CI-only assertion for this exact case as a coverage-closing action, not because a defect is suspected.

### AC-20 — Case-sensitivity of `is_relative_to` on case-insensitive filesystems
**Steps:** Reasoned through the direction of risk (can case variance ever *admit* an out-of-root path?) and confirmed the pure-pathlib behavior: `Path("/a/B/c").is_relative_to(Path("/a/b"))` is `False` (case-sensitive comparison, confirmed by direct evaluation).
**VERDICT: DISSOLVED / SAFE by construction.** Containment always compares two already-`resolve()`'d absolute paths; `resolve()` (not `is_relative_to`) performs any case canonicalization for paths that exist on disk. There is no code path where an out-of-root path's resolved form becomes a case-variant of an in-root path's resolved form — they resolve to different real filesystem entries by definition. Worst case is over-rejection (fail-closed), never admission of an outside path.

### AC-21 — POSIX-only assumptions in resolution/realpath/`os.replace` on Windows
**Steps:** Source-level audit of `os.path.realpath` (`ast_commands.py:253`), `os.replace` (`:654`), and `tempfile.mkstemp` mode semantics (`:644`) for Windows-specific behavior differences.
**Observed/Reasoned:** `os.path.realpath` follows NTFS reparse points/junctions since Python 3.8+; the containment DECISION logic (`resolved == realpath` check, `:264-267`) is platform-agnostic and applies identically to a junction pointing outside all allowed roots. `os.replace` is atomic on Windows too (via `MoveFileExW`); a locked-target `PermissionError` is an `OSError` subclass already caught at `:656` and returns exit code 2 — fail-closed availability degradation, never a containment relaxation. `mkstemp`'s `0o600` mode is a no-op on Windows (ACL-based instead), but the staging temp file is created **inside the already-allowed containment root** (`dir=str(target_path.parent)`, `:645`) — not a shared/multi-tenant OS temp directory (that channel was removed entirely by Option C) — so a weaker staging-file ACL only matters to principals who already have access to the trusted directory itself, which is the same threat model as any other file already inside that root.
**VERDICT: DISSOLVED / SAFE (advisory/availability differences only).** No Windows-specific behavior widens the allow/deny decision beyond what POSIX allows. Honest limitation: reasoning-only, no live win32 execution.

---

## L1 Ranked Findings

### #1 — AC-11: Empty/whitespace `ast.trusted_roots` entry silently trusts cwd — **MEDIUM**

- **CWE:** CWE-73 (External Control of File Name or Path), CWE-1284-adjacent (incomplete input validation on a security-relevant config value).
- **Location:** `src/interface/cli/project_root.py:173-174` (`get_containment_roots()`: `trusted_resolved = [Path(entry).resolve() for entry in trusted_raw]` — no filter for empty/whitespace entries before `_load_trusted_roots()`'s raw list, `project_root.py:100-118`, reaches `Path(entry).resolve()`). Root-cause upstream contributor: `src/infrastructure/adapters/configuration/env_config_adapter.py:115-117` (`_parse_value("")` returns `""` rather than treating empty as "unset") and `:145-147`/`get_list` (CSV trailing comma yields a stray `""` element).
- **Deployment model / preconditions:** Any host, single-user or shared. Requires (a) the `ast.trusted_roots` config channel to yield a degenerate empty/whitespace entry — plausible via empty env-var interpolation (`JERRY_AST__TRUSTED_ROOTS="$SOME_VAR"` where `SOME_VAR` is unset/empty in a script or CI job), a trailing comma in CSV form, or a stray `""` in a TOML array — **and** (b) invocation `cwd` differs from `CLAUDE_PROJECT_DIR`/project root, which is a normal occurrence (Claude Code scratchpad workflows, CI runners, any wrapper script that `cd`s before invoking `jerry`).
- **Severity rationale:** MEDIUM per the engagement rubric ("access broadening requiring a specific-but-realistic condition — config-channel influence, cwd ≠ project root"). **+1 modifier applied:** reachable via `ast_modify` (write path shares the identical `get_containment_roots()` plumbing), pushing to the upper MEDIUM band. Not HIGH: does not defeat containment under *pure* default config (a degenerate config-channel input, even if unintentional, is a precondition). Not LOW: unlike AC-10, the user took **no** deliberate trust-granting action at all — the widening is a pure side effect of an empty string, with a transparency note that reads identically to a legitimately-configured root.
- **Minimal reproduction (verified against the real shipped CLI):**
  ```bash
  # cwd != project root; JERRY_AST__TRUSTED_ROOTS is an empty string (e.g. from an
  # unset shell variable interpolated into it, or a CI job template)
  cd /some/attacker-influenceable/directory
  CLAUDE_PROJECT_DIR=/real/project \
    JERRY_AST__TRUSTED_ROOTS="" \
    jerry ast frontmatter /some/attacker-influenceable/directory/anything.md
  # -> exit 0, file content printed; only a generic "Note: ... operating outside the
  #    project root via a configured trusted root" fires -- no broad-root Warning,
  #    because cwd is (almost always) not "broad".
  ```
- **Recommended fix:** In `_load_trusted_roots()` (`project_root.py:100-118`), filter `entry.strip()` truthiness before returning: `return [str(entry) for entry in config.get_list("ast.trusted_roots", []) if str(entry).strip()]`. This closes the empty/whitespace/CSV-trailing-comma/TOML-stray-`""` cases in one change and requires no schema change.

### #2 — AC-18: `JERRY_PROJECT` traversal steers the project-config read outside `projects/` — **MEDIUM**

- **CWE:** CWE-22 (Path Traversal), CWE-20 (Improper Input Validation).
- **Location:** `src/interface/cli/project_root.py:88-90` (`build_layered_config_adapter()`: `project_config_path = root / "projects" / jerry_project / ".jerry" / "config.toml"` — `jerry_project` is `os.environ.get("JERRY_PROJECT")` verbatim, unvalidated).
- **Deployment model / preconditions:** **Shared/multi-tenant host required for realistic exploitation** (e.g., a CI runner with a shared filesystem across pipelines/jobs, where `JERRY_PROJECT` is derived from a templated or PR-influenced value). On a single-user laptop this is not attacker-reachable — the user would have to attack their own filesystem, which is not a privilege boundary. Requires a pre-existing `config.toml` at the traversed-to location containing `ast.trusted_roots`; the traversal alone does not fabricate a trust grant, it only widens *which file* gets read as configuration.
- **Severity rationale:** MEDIUM, explicitly deployment-model-gated per the rubric's instruction to "state the assumed deployment model explicitly for any multi-tenant-dependent case." No `-1` compensating-control offset applies (no OS control independently blocks the traversal — confirmed reproduced end-to-end). Not HIGH: HIGH requires reachability "under default config" — this requires both an externally-influenced `JERRY_PROJECT` value AND a pre-positioned file, which is a two-hop precondition, not default-config reachability.
- **Minimal reproduction (verified in-process against the real shipped functions):**
  ```python
  # project/ has a real 'projects/' subdirectory (true of every real Jerry project)
  # elsewhere/.jerry/config.toml (OUTSIDE project/projects/) contains:
  #   [ast]
  #   trusted_roots = ["/tmp/attacker-planted"]
  os.environ["CLAUDE_PROJECT_DIR"] = str(project)
  os.environ["JERRY_PROJECT"] = "../../elsewhere"
  pr._load_trusted_roots()  # -> ['/tmp/attacker-planted']  (attacker-controlled)
  ```
- **Recommended fix:** In `build_layered_config_adapter()` (`project_root.py:88-90`), resolve `project_config_path` and verify `project_config_path.resolve().is_relative_to(root / "projects")` before passing it to `LayeredConfigAdapter`; if not, ignore the project-config layer (fall through to root/default) and optionally warn.

### #3 — AC-10: Relative `ast.trusted_roots` entries are cwd-dependent with zero runtime signal — **LOW**

- **CWE:** CWE-426 (Untrusted Search Path) / CWE-1284-adjacent (missing normalization warning on a security-relevant config value).
- **Location:** `src/interface/cli/project_root.py:173-174` (no relative-path rejection, normalization, or warning before `Path(entry).resolve()`); the hazard is documented only in a source docstring (`project_root.py:109-111`), never surfaced to the user at runtime.
- **Deployment model / preconditions:** Any host. Requires the user to have **deliberately** configured a relative `ast.trusted_roots` entry (bounded by user intent, unlike Finding #1) — the risk is that the *effective* trusted directory silently varies with invocation cwd, including an upward `..` escape, with no transparency signal comparable to the R-3/R-4 mechanisms already used elsewhere in the same file.
- **Severity rationale:** LOW per the rubric ("weakness in an advisory control / transparency gap"). This is explicitly the class red-lead pre-labeled "at worst a documented usability hazard, not an escape beyond user intent" — confirmed accurate by this PoC, which is why it is NOT rated MEDIUM despite the demonstrated `..` upward escape: the user chose to declare a relative entry, and every resulting resolution stays within paths reachable from a cwd the user themselves controls at invocation time.
- **Minimal reproduction:**
  ```python
  os.environ["JERRY_AST__TRUSTED_ROOTS"] = "scratch"
  # cwd = A/B  -> configured root resolves to A/B/scratch
  # cwd = X/Y  -> configured root resolves to X/Y/scratch  (a DIFFERENT directory)
  os.environ["JERRY_AST__TRUSTED_ROOTS"] = "../shared"
  # cwd = A/B  -> configured root resolves to A/shared  (upward escape via ..)
  ```
- **Recommended fix:** Same input-hygiene pass as Finding #1 — in `_load_trusted_roots()` or `get_containment_roots()`, detect non-absolute entries (`not Path(entry).is_absolute()`) and either reject them with a clear error, or emit an R-3/R-4-style stderr warning naming the resolved cwd-relative path so the effective trust grant is never silent.

---

## L2 Strategic Implications

**The redesign's core claim is validated, not merely plausible.** Every Group A case (C1–C6) was proven against the real `da34a8b8` source with behavioral PoCs, not inference from reading — including a genuine read→write symlink-swap TOCTOU attempt against `ast_modify` that was rejected exactly as the write-time-recheck design intends, and a real end-to-end CLI PoC (not just internal function calls) for the highest-value new-surface hypothesis (AC-11).

**One systemic root cause underlies all three confirmed findings:** the trust decision accepts declared configuration strings (`ast.trusted_roots` entries, `JERRY_PROJECT`) without normalizing or validating them before they influence either the *resolved directory* (AC-10, AC-11) or the *file read as configuration* (AC-18). A single input-hygiene pass closes all three:

1. In `_load_trusted_roots()`: strip and drop empty/whitespace entries (closes #1/AC-11).
2. In the same function or `get_containment_roots()`: reject or warn on non-absolute entries before resolution (closes #3/AC-10).
3. In `build_layered_config_adapter()`: verify the resolved `project_config_path` stays under `root / "projects"` before treating it as a config source (closes #2/AC-18).

None of these three findings reaches CRITICAL or HIGH: none defeats containment under pure default configuration with zero config-channel action, and the one write-reachable case (#1) still requires a degenerate (if plausible) input on the config channel as a precondition. This is consistent with red-lead's L2 framing — Option C genuinely shifted the residual risk from "auto-trusted OS temp, no ownership gate" (dissolved) to "declared config strings, no normalization" (the three findings above), and did not silently reintroduce any of the six prior Critical clusters.

**Coverage disclosure (P-022):** AC-19 (Windows `C:\Users` ancestor-of-home) was validated via same-flavor `PureWindowsPath` mocking, not a live win32 interpreter — this assessment ran entirely on macOS. The mocked validation gives high confidence the algorithm itself is correct (it is pure, flavor-agnostic `pathlib` logic with no POSIX-coupling), but the full `get_containment_roots()` → `configured`-classification wiring was not behaviorally observed end-to-end on Windows. Recommend a CI-only (`windows-latest`) assertion for `PureWindowsPath("C:\\Users")` broadness under the `configured` classification as a coverage-closing action, not because a defect is suspected.

**Test-suite coverage gap confirmation:** consistent with red-lead's L2 guidance, the eng-lead TDD list does not appear to cover an empty-string `trusted_roots` entry (AC-11), a relative entry's cwd-dependence as an adversarial (not just descriptive) case (AC-10), or the `JERRY_PROJECT` traversal case (AC-18) at all. All three gaps are corroborated by this pass's confirmed findings; recommend adding regression tests for each of the three fixes above.

---

## Constitutional Compliance

- **P-001 (evidence-based):** Every verdict cites exact file:line ranges in the shipped `da34a8b8` source and includes either a real behavioral PoC transcript (in-process, real functions) or, for one real CLI invocation (AC-11), a captured `uv run jerry ast` stdout/stderr/exit-code transcript. AC-19/AC-21 are explicitly disclosed as reasoning-plus-mocked, not behaviorally observed on a live Windows host.
- **P-002 (persisted):** This report is persisted at `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/red-vuln-option-c-findings.md`.
- **P-020 (user authority):** No production source, test, or worktracker file was modified. All PoCs ran in disposable `mkdtemp` sandboxes; the one file touched outside a sandbox was this report itself. Findings are reported for the owner's decision, not unilaterally patched.
- **P-022 (no deception):** Every DISSOLVED verdict is backed by an actual executed check, not inferred from reading the code. Every FINDING states its exact precondition and deployment-model dependency rather than being presented as unconditionally exploitable. The AC-19/AC-21 reasoning-only limitation is stated plainly, not omitted.

---

*red-vuln execution report — RED-BUG010, Option C @ da34a8b8. Downstream: red-reporter for engagement-level severity aggregation and stakeholder reporting.*
