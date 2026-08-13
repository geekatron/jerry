# eng-lead Implementation Plan: BUG-010 Option C — User-Declared Trusted Roots

> Criticality C3+ (AE-005 security-relevant). Implementation-planning artifact only — no code in this
> document. Follow clean/hexagonal architecture (H-07, H-10, H-11) and TDD Red/Green/Refactor (H-20)
> throughout implementation. All Python execution via `uv run` (H-05).

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Timeline, key standards decisions, dependency risk, team readiness |
| [L1 Technical Detail](#l1-technical-detail) | Full implementation plan |
| [1. Module/File Layout](#1-modulefile-layout) | New/changed files, clean-arch layer, pure-policy signature |
| [2. `ast.trusted_roots` Config Contract](#2-asttrusted_roots-config-contract) | Type, default, precedence, env var, TOML example |
| [3. C1–C6 Resolution Mapping](#3-c1c6-resolution-mapping) | Dissolved-by-design vs. fixed-how, per tournament finding |
| [4. TDD Test List (Red First)](#4-tdd-test-list-red-first) | Ordered, split unit(pure)/unit(I-O)/integration/config-precedence |
| [5. Existing Test Inventory (Must Rewrite)](#5-existing-test-inventory-must-rewrite) | Tests asserting the old always-widen behavior |
| [6. Coverage Confirmation and `--quiet` Wiring](#6-coverage-confirmation-and---quiet-wiring) | H-21 ≥90% line coverage plan; commands needing `--quiet` |
| [7. Design Decisions Requiring Owner Sign-off](#7-design-decisions-requiring-owner-sign-off) | DD-1 through DD-4 |
| [L2 Strategic Implications](#l2-strategic-implications) | SAMM trajectory, technical debt, long-term maintainability |
| [Appendix: SSDF / MS SDL Mapping](#appendix-ssdf--ms-sdl-mapping) | Practice traceability |

---

## L0 Executive Summary

**Mandate:** Replace `jerry ast`'s current always-auto-widen containment policy (project root +
`tempfile.gettempdir()` + `/tmp`, unconditionally trusted with no user action) with **Option C**:
containment defaults to the project root plus zero-or-more **user-declared** `ast.trusted_roots`
entries read through the existing `LayeredConfigAdapter`. No directory is trusted unless the project
owns it or the user explicitly configured it. This is a pure policy substitution — no new I/O
mechanism, no new config system, no code outside `src/interface/cli/`.

**What this dissolves vs. fixes:**

| Tournament finding | Disposition |
|---|---|
| C1 — index-based (not location-based) trust bypass | **Dissolved by design.** Classification is now structural (`project`\|`configured`\|`explicit`), never array-index-based. The vulnerable comparison (`matched_root != allowed_roots[0]`) is deleted, not patched. |
| C2 — `ast_modify` write path skips the ownership gate | **Fixed.** Write-time recheck now calls the *same* `_check_path_containment` routine used at read time (full symlink/realpath re-verification), closing the TOCTOU gap. |
| C3 — ownership gate fails open on `stat()` OSError | **Dissolved by design (recommended removal).** The gate's sole rationale — safe auto-trust of shared OS temp — no longer exists; temp is not auto-trusted. Recommend deleting `_check_temp_root_ownership` entirely (owner sign-off required, DD-2). |
| C4 — same-UID/root multi-tenant defeats the gate | **Dissolved by design.** Same rationale as C3 — the gate it defeated is recommended for removal. |
| C5 — `TMPDIR`/`TEMP` poisoning silently widens the default set | **Dissolved by design.** `tempfile.gettempdir()` and `/tmp` are removed from the default set entirely; env-var poisoning of `TMPDIR` has zero effect on containment. |
| C6 — stderr/stdout merge corrupts JSON; no suppression | **Fixed.** New `--quiet` flag (default OFF, warnings ON) on all 10 `ast` subcommands suppresses R-3/R-4 stderr output; stdout is never touched by warnings today or after this change. |

**Team readiness:** No new dependencies, no new architecture layers, no schema migrations beyond one
TOML/env config key. Change surface is confined to 6 files in `src/interface/cli/` plus test files.
Estimated implementation: 1 TDD cycle (Red → Green → Refactor) per module, ~1–2 engineering days for
eng-backend, plus red-team re-check and `/adversary` re-score to ≥0.92 before merge to PR #341 (per
`RESUME-HERE.md` next-action sequence).

**Key standards decisions requiring explicit sign-off before eng-backend starts:** see
[Section 7](#7-design-decisions-requiring-owner-sign-off) — most consequential is DD-2 (remove vs.
retain the ownership gate for configured roots).

---

## L1 Technical Detail

### 1. Module/File Layout

All files are `src/interface/cli/` (interface layer per `architecture-standards.md`; H-07 layer
isolation is satisfied — no domain/application code touches path containment, and infrastructure
adapter instantiation (`LayeredConfigAdapter`) follows the **existing** in-repo precedent of
`CLIAdapter._create_config_adapter()`, which already instantiates infrastructure directly from the
interface layer. This is a pre-existing architectural exception, not one newly introduced by this
plan — flagged transparently, not silently propagated further than the existing pattern already
established).

| File | Status | Layer | Change |
|---|---|---|---|
| `src/interface/cli/containment_policy.py` | **NEW** | Interface (pure) | Pure containment policy: `ContainmentRoot` value object + `resolve_allowed_roots()` function + relocated `_is_broad_containment_root()`. Zero env/filesystem/config access. |
| `src/interface/cli/project_root.py` | **MODIFIED** | Interface (I/O adapter) | Remove `_HARDCODED_TMP`/`tempfile` auto-widen machinery. `get_containment_roots()` becomes an I/O-boundary wrapper around `resolve_allowed_roots()`; reads `ast.trusted_roots` via a new `LayeredConfigAdapter` factory. |
| `src/interface/cli/ast_commands.py` | **MODIFIED** | Interface (I/O + orchestration) | Delete `_check_temp_root_ownership`, `_is_temp_default_root_match`, `_warn_if_temp_root_match` (superseded). `_check_path_containment` matches by `ContainmentRoot.classification`, not index. `ast_modify` write-time recheck reuses `_check_path_containment` verbatim (C2 fix). All 10 `ast_*` functions gain a `quiet: bool = False` parameter. |
| `src/interface/cli/parser.py` | **MODIFIED** | Interface (CLI wiring) | New `_add_quiet_argument()` helper, called alongside `_add_root_argument()` on all 10 `ast` subparsers. |
| `src/interface/cli/main.py` | **MODIFIED** | Interface (CLI wiring) | `_handle_ast` reads `getattr(args, "quiet", False)` and threads it into every `ast_*` call alongside `root`. |
| `src/interface/cli/adapter.py` | **MODIFIED** | Interface (CLI wiring) | `CLIAdapter._create_config_adapter()` defaults dict gains `"ast.trusted_roots": []` (required by mandate — makes the key visible to `jerry config show`/`jerry config get`). |

#### 1.1 Pure policy module: `containment_policy.py`

**Public value object** (H-10: exactly one public class per file):

```python
@dataclass(frozen=True, slots=True)
class ContainmentRoot:
    """An allowed containment root with its trust classification."""

    path: Path
    classification: Literal["project", "configured", "explicit"]
    is_broad: bool
```

**Public pure-policy function signature** (matches the mandate's literal contract: "given resolved
project root + resolved configured roots + optional resolved explicit root → ordered allowed set +
per-root classification + broad-root flags"):

```python
def resolve_allowed_roots(
    project_root: Path,
    configured_roots: Sequence[Path],
    explicit_root: Path | None,
) -> list[ContainmentRoot]:
    """Pure containment policy (zero I/O). All inputs are pre-resolved by the caller.

    - explicit_root is not None -> returns EXACTLY one entry, classification="explicit",
      ignoring project_root and configured_roots entirely (unchanged --root exclusivity semantics).
    - explicit_root is None -> returns [project_root as "project"] + [each configured_root
      as "configured"], in that order, de-duplicated (first occurrence wins; a configured
      root that duplicates project_root is dropped, retaining the "project" classification).
    - is_broad is computed per-root via the relocated _is_broad_containment_root().
    """
```

**Private helper (relocated, unchanged logic):** `_is_broad_containment_root(resolved: PurePath) -> bool`
moves here verbatim from `project_root.py`. Rationale: `resolve_allowed_roots()` must compute
`is_broad` per root internally (mandate requirement), so the dependency must run
`containment_policy.py → (nothing else)`, not `project_root.py → containment_policy.py → project_root.py`
(a circular import). Moving the implementation — rather than leaving a re-export shim — keeps all pure
policy logic in one file with a single source of truth. **This changes the test import path**; see
[Section 5](#5-existing-test-inventory-must-rewrite).

No env, filesystem, or config access anywhere in this module. 100% of its branches are reachable with
plain `Path`/`PureWindowsPath` objects constructed in-memory — no `tmp_path` fixture required except
where `_is_broad_containment_root`'s `Path.home()` call is monkeypatched (same pattern the existing
test suite already uses).

#### 1.2 I/O adapter: `project_root.py`

```python
def get_project_root() -> Path:                                    # UNCHANGED
def build_layered_config_adapter(defaults: dict[str, Any]) -> Any: # NEW (local infra import, mirrors
                                                                     # CLIAdapter._create_config_adapter)
def _load_trusted_roots() -> list[str]:                            # NEW, private, I/O
def get_containment_roots(
    explicit_root: str | None = None,
    quiet: bool = False,
) -> list[ContainmentRoot]:                                        # REWRITTEN, return type changed
```

`get_containment_roots()` responsibilities (I/O boundary only — all decision logic delegates to
`resolve_allowed_roots()`):

1. Resolve `project_root = get_project_root().resolve()`.
2. If `explicit_root` given: resolve it; call `resolve_allowed_roots(project_root, [], resolved_explicit)`.
3. Else: call `_load_trusted_roots()` (reads `ast.trusted_roots` via `LayeredConfigAdapter.get_list`),
   resolve each entry to an absolute `Path`, call
   `resolve_allowed_roots(project_root, resolved_trusted, None)`.
4. For each returned `ContainmentRoot` with `is_broad=True`: print the existing R-3 stderr warning
   (for `classification="explicit"`, unchanged wording) or a new, analogous warning (for
   `classification="configured"` — see DD-1) — **unless `quiet=True`**.
5. Return the `list[ContainmentRoot]` (breaking change to the previous `list[Path]` return contract;
   this is a private interface-layer helper, not a published library API — all 2 call sites
   [`_check_path_containment`, `ast_modify`] are updated in the same change).

`_load_trusted_roots()` mirrors `CLIAdapter._create_config_adapter()`'s construction pattern exactly
(same `root_config_path`, `project_config_path`, `env_prefix="JERRY_"`) via the new shared
`build_layered_config_adapter()` factory, so `jerry ast` and `jerry config` resolve the identical
config file set with identical precedence. `tempfile` import and `_HARDCODED_TMP` are deleted.

**`build_layered_config_adapter()` rationale:** extracts the adapter-construction logic that
`CLIAdapter._create_config_adapter()` already contains, so it is written once and both call sites
(`adapter.py`, `project_root.py`) share it — closing a duplication gap rather than opening a new one.
This is a MEDIUM-tier recommendation (non-blocking refactor of `adapter.py` to call the shared
factory); the REQUIRED item is only that `project_root.py` gains its own read path and that
`adapter.py`'s defaults dict gains the new key (see [Section 7](#7-design-decisions-requiring-owner-sign-off), DD-4).

#### 1.3 Orchestration layer: `ast_commands.py`

Deleted (superseded, not refactored): `_check_temp_root_ownership`, `_is_temp_default_root_match`,
`_warn_if_temp_root_match`.

New: `_note_if_configured_root_match(matched: ContainmentRoot, file_path: str, quiet: bool) -> None`
— fires the R-4 generalized transparency note when `matched.classification == "configured"` and
`not quiet`. Wording changes from *"...jerry ast is operating on a temp/scratchpad path ({root})"* to
*"...jerry ast is operating outside the project root via a configured trusted root: {root}"* (mandate's
literal wording), stderr-only, one line, unconditionally after a successful containment match (never
after a rejection — same ordering discipline as the current code).

`_check_path_containment(file_path: str, explicit_root: str | None = None, quiet: bool = False) -> tuple[Path | None, str | None]`:

- `allowed_roots = get_containment_roots(explicit_root, quiet=quiet)` — now `list[ContainmentRoot]`.
- Match: `matched = next((r for r in allowed_roots if resolved.is_relative_to(r.path)), None)`.
- No match → unchanged `"Path escapes allowed containment roots"` error.
- `_note_if_configured_root_match(matched, file_path, quiet)` replaces the deleted
  `_warn_if_temp_root_match` call — no ownership-gate call at all (see DD-2).
- Symlink realpath check: `any(realpath.is_relative_to(r.path) for r in allowed_roots)` — same logic,
  new iterable shape.
- File-size check: unchanged.

`ast_modify()` write-time recheck (**C2 fix**, the mandate's core residual-fix requirement): replace
the current independent `get_containment_roots(root)` + `is_relative_to` re-derivation (lines ~677–682
today) with a **direct call to `_check_path_containment(file_path, root, quiet=True)`** on the
resolved target path. `quiet=True` is hard-coded for this specific internal call (not the CLI
`--quiet` flag's value) — a deliberate design choice (DD-3) to avoid printing the R-3/R-4 note twice
for one logical invocation (it already printed once at read time), while the containment
*enforcement* itself remains fully unconditional. This makes read-time and write-time containment
**literally the same function call**, not merely "the same algorithm re-implemented" — closing C2 at
the design level, not just the symptom level: a symlink swapped between the read and the write is
caught because `_check_path_containment` re-resolves via `os.path.realpath()` fresh, every call.

All 10 `ast_*` functions (`ast_parse`, `ast_render`, `ast_validate`, `ast_query`, `ast_frontmatter`,
`ast_modify`, `ast_reinject`, `ast_detect`, `ast_sections`, `ast_metadata`) gain `quiet: bool = False`,
threaded into `_read_file(file_path, root, quiet)` → `_check_path_containment(file_path, root, quiet)`.

#### 1.4 CLI wiring: `parser.py`, `main.py`, `adapter.py`

`parser.py`: new `_add_quiet_argument(parser: argparse.ArgumentParser) -> None`, structurally identical
to `_add_root_argument`, adding:

```python
parser.add_argument(
    "--quiet",
    action="store_true",
    default=False,
    help="Suppress stderr transparency notes and broad-root warnings for this invocation.",
)
```

Called immediately after every `_add_root_argument(...)` call inside `_add_ast_namespace()` — all 10
subparsers (`parse`, `render`, `validate`, `query`, `frontmatter`, `modify`, `reinject`, `detect`,
`sections`, `metadata`).

`main.py`: `_handle_ast` adds `quiet = getattr(args, "quiet", False)` (same defensive `getattr` pattern
already used for `root`) and passes `quiet=quiet` into every one of the 10 `ast_*` calls.

`adapter.py`: `_create_config_adapter()` defaults dict gains `"ast.trusted_roots": []` — **required by
the mandate** ("Register default `[]` in the `_create_config_adapter` defaults dict"). This does not
change `jerry ast`'s own config read (which uses `project_root.build_layered_config_adapter`, not
`CLIAdapter`), but makes the key discoverable/settable via `jerry config show`, `jerry config get
ast.trusted_roots`, and `jerry config set ast.trusted_roots ... --scope project|root` for UX symmetry.

---

### 2. `ast.trusted_roots` Config Contract

| Property | Value |
|---|---|
| **Key** | `ast.trusted_roots` |
| **Type** | List of strings (each an absolute directory path). `LayeredConfigAdapter.get_list()` coerces a scalar to a 1-element list if a non-list value is ever set by mistake. |
| **Default** | `[]` (empty list — zero trust beyond the project root, matching the mandate: "NO automatic temp/scratchpad trust"). |
| **Resolution** | Each entry is resolved via `Path(entry).resolve()` at read time in `_load_trusted_roots()`/`get_containment_roots()` — relative entries resolve against CWD (consistent with existing `--root` relative-path handling), which is a foot-gun for a security-relevant config key; **recommend documenting "use absolute paths" in the key's help text and `jerry config get` output**, not silently rejecting relative entries (MEDIUM, non-blocking). |
| **Precedence (as actually implemented by `LayeredConfigAdapter.get()`, verified against `src/infrastructure/adapters/configuration/layered_config_adapter.py`)** | 1. ENV `JERRY_AST__TRUSTED_ROOTS` (highest) → 2. Project config `projects/{JERRY_PROJECT}/.jerry/config.toml` → 3. Root/framework config `.jerry/config.toml` → 4. Code default `[]` (lowest). |

**Correction to the task brief's stated precedence and env var name — flagged per P-022 (no
deception):** the task brief describes a 5-layer precedence including `SESSION_LOCAL
(.jerry/local/context.toml)` ranked #2, and an env var form `JERRY_AST_TRUSTED_ROOTS` (single
underscore). Neither matches the actual, currently-wired mechanism this plan is required to reuse
("Config READ stays through the existing `LayeredConfigAdapter`. Do NOT invent a new config
mechanism"):

- `LayeredConfigAdapter.get()` (the class `CLIAdapter._create_config_adapter()` — and this plan's
  `build_layered_config_adapter()` — actually instantiate) implements **4 layers only**: ENV → PROJECT →
  ROOT → DEFAULT. There is no `local_config_path` parameter and no session-local file is ever read by
  `.get()`. A separate `ConfigSource` enum exists in `src/configuration/domain/value_objects/config_source.py`
  that *does* define a 5-layer model including `SESSION_LOCAL`, but it belongs to a different, currently
  unwired domain aggregate (`src/configuration/domain/aggregates/configuration.py`) — not the
  `LayeredConfigAdapter` this mandate requires reuse of. `jerry config set --scope local` writes to
  `.jerry/local/context.toml`, but nothing in the current `LayeredConfigAdapter.get()` reads that file
  back — this is a pre-existing gap in the codebase, out of scope for BUG-010, and is called out here
  only so the config contract table above is accurate rather than aspirational.
- The env var name follows `EnvConfigAdapter._config_to_env_key()`'s actual mapping:
  `key.upper().replace(".", "__")` — a **double** underscore separates namespace segments (one dot →
  `__`). For key `ast.trusted_roots`, the correct env var is **`JERRY_AST__TRUSTED_ROOTS`**, not
  `JERRY_AST_TRUSTED_ROOTS`. Using the single-underscore form would silently fail: `_env_to_config_key("JERRY_AST_TRUSTED_ROOTS")`
  produces the flat key `"ast_trusted_roots"` (no dot), which never matches `"ast.trusted_roots"` in
  `_get_nested()`'s dot-notation lookup — the env override would be silently ignored, a security-relevant
  footgun for a trust-declaration key. **The implementation and all documentation MUST use
  `JERRY_AST__TRUSTED_ROOTS`.**

**Env var value parsing** (per `EnvConfigAdapter._parse_value()`): a JSON array is the recommended
form (unambiguous, handles paths containing commas or spaces); a bare comma-separated string is also
accepted as a fallback (`_parse_value` splits on `,` when the value is unquoted and contains a comma).

```bash
# Recommended (JSON array — safe for paths with spaces/commas):
export JERRY_AST__TRUSTED_ROOTS='["/private/tmp/claude-502/session-abc/scratchpad"]'

# Also accepted (comma-separated, single entry works with or without a comma):
export JERRY_AST__TRUSTED_ROOTS="/private/tmp/claude-502/session-abc/scratchpad"
```

**TOML example** (`.jerry/config.toml` or `projects/{PROJECT}/.jerry/config.toml`):

```toml
[ast]
trusted_roots = [
    "/private/tmp/claude-502/session-abc/scratchpad",
    "/Users/me/shared-notes",
]
```

**Reachability confirmation:** `_get_nested(data, "ast.trusted_roots")` walks `data["ast"]["trusted_roots"]`
— TOML's native `[ast]` table + `trusted_roots = [...]` array syntax maps directly, no custom parsing
needed. Confirmed reachable at every layer the mandate requires (env, project, root/framework,
default); the session-local layer is explicitly flagged above as **not** reachable through
`LayeredConfigAdapter` today (out of scope; a documented gap, not a silent omission).

---

### 3. C1–C6 Resolution Mapping

Sourced from `adv-s014-tournament-score.md` (S-014 tournament aggregation, C4, score 0.64 REVISE,
9 blind strategy reports, deduped to 6 Critical clusters).

| ID | Tournament finding (verbatim summary) | Corroboration | Disposition | How |
|---|---|---|---|---|
| **C1** | `_is_temp_default_root_match` exempts `allowed_roots[0]` from the ownership gate/R-4 note by **array-index identity alone**, never verifying index-0 is itself outside a temp tree. Highest RPN in the tournament (432); contradicted by the independent `/eng-team` gate report, which called this "correct." | 6-way (S-001, S-004, S-007, S-010, S-011, S-012) | **Dissolved by design** | `_is_temp_default_root_match` is deleted outright, not patched. Classification (`project`\|`configured`\|`explicit`) is computed structurally per root inside `resolve_allowed_roots()` — there is no array index to misidentify. A project root that happens to resolve inside a temp tree is still classified `"project"` (unchanged trust posture — project root is always the user's own repository by construction of `get_project_root()`), but the entire C1 attack class (silently smuggling extra trust through index-0) has no surface left: index-0 is never treated as "safe by position," it is treated as `"project"` by *origin*. |
| **C2** | `ast_modify`'s write-time TOCTOU recheck never calls the ownership gate; docstring falsely claims read/write "never disagree." | 5-way (S-001, S-004, S-010, S-012, S-013) | **Fixed** | Write-time recheck now calls `_check_path_containment(file_path, root, quiet=True)` verbatim — the identical function used at read time, including fresh `os.path.realpath()` symlink re-resolution. A symlink swapped between read and write is caught because containment is re-verified from scratch, not re-derived from a cached `allowed_roots` list. See [1.3](#13-orchestration-layer-ast_commandspy) and TDD tests #40–#42. |
| **C3** | `_check_temp_root_ownership`'s `except OSError: pass` fails **open**, while the sibling size-check `stat()` 3 lines away fails **closed** on the identical error class; attacker-forceable (`RT-002`, deliberately unlink the target). | 4-way (S-001, S-004, S-010, S-012) | **Dissolved by design (recommend removal, owner sign-off DD-2)** | The gate existed solely to safely auto-trust shared OS temp directories. Under Option C, temp is never auto-trusted — a `configured` root is a deliberate, explicit user declaration (structurally identical trust posture to `--root`, which has never had an ownership gate). Recommend deleting `_check_temp_root_ownership` entirely rather than fixing its fail-open bug, since the control it protects no longer exists. If the owner instead elects to retain *some* ownership check for `configured` roots (residual defense-in-depth), it MUST fail **closed** per the mandate — see DD-2 for the explicit fallback design. |
| **C4** | Same-UID/root multi-tenant (containers/CI as uid 0, or a shared service-account UID) defeats the ownership gate's entire premise — `st_uid == geteuid()` is true for every tenant. | 4-way (S-001, S-004, S-012, S-013) | **Dissolved by design** | Same rationale as C3 — the gate this finding attacks is recommended for removal. If DD-2 resolves toward retaining a residual check, this finding must be re-litigated against that specific design (documented as a known limitation, matching the tournament's own minimum-acceptable remediation: "at minimum, a `geteuid()==0` disclosure warning"). |
| **C5** | `_is_broad_containment_root` is invoked only in the `--root` branch; the default branch's `tempfile.gettempdir()` gets no broadness check — `TMPDIR`/`TEMP`/`TMP` env poisoning can silently expand the default trusted-root set with zero warning. | 2-way direct (S-012) + 1 shared-pattern (S-004) | **Dissolved by design** | `tempfile.gettempdir()` and `_HARDCODED_TMP`/`/tmp` are removed from the default set entirely — there is no `TMPDIR`-derived path left in the allowed-roots computation for an attacker to poison. `TMPDIR`/`TEMP` env vars have **zero** effect on `jerry ast` containment after this change. (The *analogous* residual risk — a broad `configured` root via `ast.trusted_roots` — is addressed by DD-1's recommended symmetry extension of the R-3 warning, a new capability, not a fix to C5 itself.) |
| **C6** | R-4's transparency note corrupts JSON output under realistic merged-stream consumption (`2>&1`, `subprocess.run(capture_output=True)` + naive concatenation) — fires on the design's own stated primary use case (agent scratchpad ops); no suppression flag exists. | 2-way (S-002, S-004) | **Fixed** | New `--quiet` flag (default `False`, i.e. warnings ON by default per the mandate) on all 10 `ast` subcommands, threaded through `_read_file`/`_check_path_containment`/`get_containment_roots`, suppresses both R-3 (broad-root) and R-4 (configured-root transparency note) stderr output for the invocation. Documented in `--help` text per subcommand. Stdout is never touched by any warning path today or after this change (verified by every existing and new stderr-assertion test asserting `captured.out == ""`). |

---

### 4. TDD Test List (Red First)

Numbered in implementation order. Each is written to **fail first** against the current (pre-change)
code, then implementation proceeds file-by-file until green, then refactor. Naming follows
`test_{scenario}_when_{condition}_then_{expected}` per `testing-standards.md`.

#### 4.A Unit — Pure policy (`tests/unit/interface/cli/test_containment_policy.py`, NEW file)

Zero env/filesystem/config access except the pre-existing `Path.home()` monkeypatch pattern already
used for `_is_broad_containment_root`.

1. `test_resolve_allowed_roots_when_no_configured_and_no_explicit_then_returns_only_project_root`
2. `test_resolve_allowed_roots_when_configured_roots_given_then_appended_after_project_root_in_order`
3. `test_resolve_allowed_roots_when_configured_root_duplicates_project_root_then_deduped_keeping_project_classification`
4. `test_resolve_allowed_roots_when_duplicate_configured_roots_given_then_deduped_preserving_first_order`
5. `test_resolve_allowed_roots_when_explicit_root_given_then_returns_single_explicit_entry`
6. `test_resolve_allowed_roots_when_explicit_root_given_then_project_root_and_configured_roots_excluded`
7. `test_resolve_allowed_roots_when_project_root_is_broad_then_flagged_is_broad_true`
8. `test_resolve_allowed_roots_when_configured_root_is_broad_then_flagged_is_broad_true`
9. `test_resolve_allowed_roots_when_explicit_root_is_broad_then_flagged_is_broad_true`
10. `test_resolve_allowed_roots_when_all_roots_ordinary_then_is_broad_false_for_every_entry`
11. `test_resolve_allowed_roots_when_configured_roots_empty_then_returns_project_root_only`
12. `test_containment_root_when_constructed_then_is_frozen_and_hashable`

Relocated from `test_project_root.py::TestBroadRootWarning` (logic unchanged, import path changed —
see [Section 5](#5-existing-test-inventory-must-rewrite)):

13. `test_is_broad_containment_root_when_posix_filesystem_root_then_true`
14. `test_is_broad_containment_root_when_windows_drive_root_then_true`
15. `test_is_broad_containment_root_when_home_directory_then_true`
16. `test_is_broad_containment_root_when_ordinary_subdirectory_then_false`
17. `test_is_broad_containment_root_when_ancestor_of_home_then_true` (parametrized, 3 cases, unchanged)
18. `test_is_broad_containment_root_when_windows_users_ancestor_of_home_then_true`
19. `test_is_broad_containment_root_when_descendant_of_home_then_false`

#### 4.B Unit — I/O adapter (`tests/unit/interface/cli/test_project_root.py`, `TestGetContainmentRoots` rewritten)

20. `test_get_containment_roots_when_no_explicit_root_and_no_config_then_returns_only_project_root`
21. `test_get_containment_roots_when_no_explicit_root_then_never_includes_tempfile_gettempdir` (negative regression — proves auto-widen removed)
22. `test_get_containment_roots_when_no_explicit_root_then_never_includes_slash_tmp` (negative regression, POSIX-skippable)
23. `test_get_containment_roots_when_trusted_roots_configured_in_toml_then_included_after_project_root`
24. `test_get_containment_roots_when_trusted_roots_configured_via_env_then_included`
25. `test_get_containment_roots_when_explicit_root_given_then_configured_trusted_roots_ignored`
26. `test_get_containment_roots_when_explicit_root_is_broad_then_warns_on_stderr` (R-3 retained, new call signature)
27. `test_get_containment_roots_when_configured_root_is_broad_then_warns_on_stderr` (NEW — DD-1 symmetry)
28. `test_get_containment_roots_when_quiet_true_then_suppresses_broad_root_warning` (NEW — C6)
29. `test_get_containment_roots_when_explicit_root_is_relative_then_resolved_against_cwd` (retained)

Config-loading unit (`_load_trusted_roots`, same file or a new `TestLoadTrustedRootsConfig` class):

30. `test_load_trusted_roots_when_no_config_present_then_returns_empty_list`
31. `test_load_trusted_roots_when_root_config_toml_has_ast_trusted_roots_then_returns_list`
32. `test_load_trusted_roots_when_project_config_overrides_root_config_then_project_value_used`
33. `test_load_trusted_roots_when_env_var_set_then_env_value_overrides_all_file_config`

#### 4.C Unit — `ast_commands.py` containment (`tests/unit/interface/cli/test_ast_commands.py`)

34. `test_containment_when_file_in_configured_trusted_root_then_allowed`
35. `test_containment_when_file_in_gettempdir_and_not_configured_then_rejected` (**critical negative regression** — replaces the old default-allow assumption)
36. `test_containment_when_file_in_slash_tmp_and_not_configured_then_rejected` (negative regression, POSIX-skippable)
37. `test_containment_when_symlink_target_in_configured_root_then_allowed`
38. `test_containment_when_symlink_escapes_all_configured_roots_then_rejected`
39. `test_check_path_containment_when_matched_via_configured_root_then_prints_generalized_transparency_note` (R-4 wording assertion)
40. `test_check_path_containment_when_matched_via_project_root_then_no_transparency_note` (retained)
41. `test_check_path_containment_when_explicit_root_given_then_no_transparency_note` (retained)
42. `test_check_path_containment_when_quiet_true_then_suppresses_transparency_note` (NEW — C6)
43. `test_check_path_containment_when_quiet_true_then_suppresses_broad_root_warning` (NEW — C6, propagated through the `ast_commands` boundary)
44. `test_check_path_containment_when_explicit_root_is_broad_then_warns` (retained, R-3 propagation)

`ast_modify` write-path unification (**C2**, the mandate's core residual fix):

45. `test_ast_modify_when_symlink_swapped_between_read_and_write_then_rejected_at_write_time` (the actual TOCTOU attack: symlink resolves inside an allowed root at read time, is repointed outside all allowed roots before the write executes; asserts exit code 2 and the file is unmodified)
46. `test_ast_modify_when_root_given_and_write_target_outside_root_then_rejected_at_write_time` (retained, existing coverage)
47. `test_ast_modify_when_configured_root_match_then_transparency_note_prints_exactly_once` (regression proving the `quiet=True` internal write-time call does not double-print R-4)

Ownership-gate removal regression (only if DD-2 resolves to full removal):

48. `test_ast_commands_module_when_imported_then_check_temp_root_ownership_is_not_defined` (guards against silent reintroduction; skip/replace with a fail-closed unit test if DD-2 resolves to "retain, fail closed" instead)

#### 4.D Unit — config precedence (`tests/unit/infrastructure/adapters/configuration/test_layered_config_adapter.py`, additions)

49. `test_get_list_when_ast_trusted_roots_default_then_returns_empty_list`
50. `test_get_list_when_ast_trusted_roots_in_root_config_then_returns_configured_list`
51. `test_get_list_when_ast_trusted_roots_in_project_config_then_overrides_root_config`
52. `test_get_list_when_ast_trusted_roots_env_json_array_then_overrides_all_file_config`
53. `test_get_source_when_ast_trusted_roots_set_in_env_then_returns_env`
54. `test_env_to_config_key_when_ast_trusted_roots_env_var_used_then_maps_to_dotted_key` (pins the **double-underscore** env var name `JERRY_AST__TRUSTED_ROOTS` against `EnvConfigAdapter`, guarding the naming trap identified in [Section 2](#2-asttrusted_roots-config-contract))

#### 4.E Integration — subprocess (`tests/integration/cli/test_ast_subprocess.py`, NEW class `TestOptionCContainmentSubprocess`)

Requires a new fixture (containment **enabled**, unlike the existing module-wide
`env_with_pythonpath` fixture which sets `JERRY_DISABLE_PATH_CONTAINMENT=1`):

```python
@pytest.fixture
def env_with_containment_enabled(project_root: Path) -> dict[str, str]:
    """Like env_with_pythonpath but leaves path containment ENABLED."""
    env = os.environ.copy()
    ...
    env.pop("JERRY_DISABLE_PATH_CONTAINMENT", None)
    return env
```

55. `test_ast_parse_subprocess_when_file_in_tempdir_and_no_trusted_roots_then_rejected` (black-box negative regression)
56. `test_ast_parse_subprocess_when_file_in_configured_trusted_root_via_env_then_allowed` (sets `JERRY_AST__TRUSTED_ROOTS` pointing at a `tmp_path` subdirectory)
57. `test_ast_parse_subprocess_when_quiet_flag_given_then_stderr_empty_despite_configured_root_match`
58. `test_ast_parse_subprocess_when_no_quiet_and_configured_root_match_then_stderr_has_note`
59. `test_ast_modify_subprocess_when_symlink_swapped_before_write_then_rejected_and_file_unchanged` (end-to-end C2 regression)
60. `test_ast_parse_subprocess_when_root_flag_and_broad_root_then_warns_on_stderr_and_succeeds` (retained R-3 propagation, black-box)

---

### 5. Existing Test Inventory (Must Rewrite)

These tests currently assert the **old always-widen** behavior (default allowed set includes
`tempfile.gettempdir()`/`/tmp` unconditionally) or reference deleted functions. Each row states the
required action.

| File | Test(s) | Current assertion | Required action |
|---|---|---|---|
| `tests/unit/interface/cli/test_project_root.py` | `TestGetContainmentRoots::test_get_containment_roots_when_no_explicit_root_then_includes_resolved_gettempdir` | Default set always contains `tempfile.gettempdir()` | **DELETE.** Contradicts the mandate; replaced by new negative test #21. |
| " | `TestGetContainmentRoots::test_get_containment_roots_when_hardcoded_tmp_exists_then_includes_it` | Monkeypatched `_HARDCODED_TMP` (existing dir) is included | **DELETE.** `_HARDCODED_TMP` seam is removed entirely. |
| " | `TestGetContainmentRoots::test_get_containment_roots_when_hardcoded_tmp_absent_then_excludes_it` | Asserts `len(roots) == 2` (project + gettempdir) when `_HARDCODED_TMP` absent | **DELETE.** No `_HARDCODED_TMP` seam; default set has exactly 1 entry (project root) with no configured roots — see new test #20. |
| " | `TestGetContainmentRoots::test_get_containment_roots_when_gettempdir_equals_hardcoded_tmp_then_deduplicated` | Dedup of `gettempdir()`/`_HARDCODED_TMP` collision | **DELETE.** Dedup logic moves to `resolve_allowed_roots()` (project/configured dedup, tests #3–#4); this specific temp/temp collision no longer exists. |
| " | `TestBroadRootWarning` (whole class, 10 tests: lines 235–429) | Imports `_is_broad_containment_root` from `project_root` module | **MOVE, do not delete.** Relocate the class body to `test_containment_policy.py`; update the import from `from src.interface.cli.project_root import _is_broad_containment_root` to `from src.interface.cli.containment_policy import _is_broad_containment_root`. `test_get_containment_roots_when_explicit_root_is_broad_then_warns_on_stderr` and `test_get_containment_roots_when_explicit_root_is_home_then_warns_on_stderr` and `test_get_containment_roots_when_no_explicit_root_then_no_warning_regardless_of_project_root` stay in `test_project_root.py` (they exercise the I/O-boundary function, not the pure predicate) but keep working unchanged since `get_containment_roots()`'s R-3 stderr contract is preserved verbatim for the `--root` branch. |
| `tests/unit/interface/cli/test_ast_commands.py` | `TestBug010ProjectRootContainment::test_containment_when_file_in_gettempdir_with_different_project_dir_then_allowed` | A file under `tempfile.gettempdir()` validates by default | **INVERT.** Becomes negative regression #35 (`..._and_not_configured_then_rejected`); add a companion positive test (#34) using a configured trusted root instead of the raw temp dir. |
| " | `TestBug010ProjectRootContainment::test_containment_when_file_in_slash_tmp_then_allowed` | A file under `/tmp` validates by default | **INVERT.** Becomes negative regression #36. |
| " | `TestBug010ProjectRootContainment::test_containment_when_symlink_escapes_from_temp_root_then_rejected` | Uses the T-3 seam (`_HARDCODED_TMP`/`gettempdir` monkeypatch) to build a *controlled, allowed* temp root, then proves a symlink escaping it is still rejected | **REWRITE.** Replace the T-3 seam with a `monkeypatch`-configured `ast.trusted_roots` entry (via the new `_load_trusted_roots` seam, e.g. `monkeypatch.setattr(project_root_module, "_load_trusted_roots", lambda: [str(controlled_root)])`) as the allowed root, keeping the same symlink-escape assertion. Superseded by test #38 in the new numbering; fold into it rather than keeping both. |
| " | `TestBug010ProjectRootContainment::test_check_path_containment_when_matched_via_temp_root_then_prints_transparency_note` | R-4 fires for a temp-root match; asserts `"temp" in captured.err.lower()` | **REWRITE.** Becomes test #39: fixture uses a configured trusted root (not `_HARDCODED_TMP`/`gettempdir` monkeypatch); assertion text changes to the generalized wording (e.g. `"configured trusted root" in captured.err.lower()`, not `"temp"`). |
| " | `TestTempRootOwnershipGate` (whole class, 8 tests: lines 1541–1707) | H-01 ownership gate behavior: allow same-UID, reject foreign-UID temp-root matches; project-root/`--root` exemption; Windows no-op; fail-open on `stat()` OSError | **DELETE the whole class** if DD-2 resolves to full removal (recommended). The scenarios this class defends (foreign-UID file inside an *auto-trusted* temp root) cannot recur under Option C — a `configured` root is never auto-trusted, it is a deliberate user declaration, structurally identical in trust posture to `--root` (which has never had an ownership gate and is explicitly documented as pure user discretion). If DD-2 instead resolves to "retain a fail-closed ownership check scoped to `configured` roots," **REWRITE** rather than delete: invert `test_check_temp_root_ownership_when_stat_oserror_then_fails_open` to assert rejection (rename to `..._then_fails_closed`), and re-scope all "temp root" fixture setup (`_HARDCODED_TMP`/`gettempdir` monkeypatches) to `ast.trusted_roots` configuration instead. |
| `tests/integration/cli/test_ast_subprocess.py` | (none currently exist for containment/widening) | N/A — no existing subprocess-level containment tests to rewrite | **ADD ONLY** — new class per [4.E](#4e-integration--subprocess-testsintegrationclitest_ast_subprocesspy-new-class-testoptioncontainmentsubprocess), no deletions required. |

**Summary count:** 4 tests deleted outright (`test_project_root.py`), 10 tests relocated verbatim
(`TestBroadRootWarning` → `test_containment_policy.py`), 4 tests inverted/rewritten
(`test_ast_commands.py` temp-default-allow assertions and the R-4 wording test), 8 tests deleted or
rewritten pending DD-2 (`TestTempRootOwnershipGate`), 0 rewrites needed in the subprocess integration
file (pure addition). Net: implementation must not merge with any of the deleted/inverted assertions
still present and green — a green `test_containment_when_file_in_gettempdir_with_different_project_dir_then_allowed`
(old, unmodified) after this change would itself prove the fix regressed.

---

### 6. Coverage Confirmation and `--quiet` Wiring

**H-21 (≥90% line coverage) confirmation:**

| Module | New/changed lines | Test coverage source | Confidence |
|---|---|---|---|
| `containment_policy.py` (new) | ~60–80 lines (dataclass + function + relocated predicate) | Tests #1–#19 exercise every branch: explicit vs. default, dedup vs. no-dedup, broad vs. ordinary, for all 3 classifications | High — pure function, fully enumerable branch space, no I/O to mock around |
| `project_root.py` (rewritten `get_containment_roots`, new `_load_trusted_roots`/`build_layered_config_adapter`) | ~40–50 changed/added lines | Tests #20–#33 hit: explicit/default paths, config-present/absent, env/project/root precedence, broad-warning + quiet-suppression branches | High — `LayeredConfigAdapter`/`AtomicFileAdapter` are independently already covered; only the new call sites need direct exercise |
| `ast_commands.py` (deleted 3 functions, rewritten `_check_path_containment`/`ast_modify` write recheck, `quiet` threading across 10 functions) | ~-90 lines deleted, ~+50 lines added/changed (net negative — deletion reduces the coverage denominator) | Tests #34–#48 + subprocess #55–#60 hit: configured-match, rejected-unconfigured, symlink-escape, TOCTOU symlink-swap, quiet suppression (both R-3 and R-4), write-time unification | High — every new branch has a direct unit test; TOCTOU test (#45) is the highest-value new case (previously untested attack path) |
| `parser.py` (`_add_quiet_argument`, 10 call sites) | ~15 lines | Parametrized test mirroring the existing `test_ast_root_flag_available_on_every_subcommand` pattern, extended to assert `--quiet` on all 10 subcommands | High — parser wiring is declarative, trivially 100%-coverable |
| `main.py` (`_handle_ast` quiet threading) | ~10 lines | Extend `TestMainAstRouting` with a `quiet=True` routing assertion (parametrized across the 10 commands, or at minimum 1 representative + the existing `--root` pass-through pattern extended) | High |
| `adapter.py` (1 new defaults entry) | 1 line | `jerry config show`/`get` existing test coverage exercises the defaults dict already; add 1 assertion that `ast.trusted_roots` appears with value `[]` when unset | High |

Net effect on the repository-wide coverage ratio is expected to be **neutral-to-positive**: the
deleted code (`_check_temp_root_ownership`, `_is_temp_default_root_match`, `_warn_if_temp_root_match`,
`_HARDCODED_TMP`) was already 100%-covered by the tests being deleted in lockstep (Section 5), so the
denominator shrinks in proportion to the numerator. All *new* lines are covered by the Red-first test
list in Section 4 before the Green phase is considered complete — no implementation commit should land
without its corresponding test(s) already present and initially failing, per H-20.

Verification command (run via `uv run` per H-05): `uv run pytest tests/unit/interface/cli/ tests/unit/infrastructure/adapters/configuration/ tests/integration/cli/test_ast_subprocess.py --cov=src/interface/cli --cov=src/infrastructure/adapters/configuration --cov-report=term-missing`.

**`--quiet` flag wiring — commands requiring it:** all 10 `jerry ast` subcommands need `--quiet` wired
identically (every one of them routes through `_read_file` → `_check_path_containment`, so every one
of them can in principle trigger an R-3 or R-4 stderr note):

`parse`, `render`, `validate`, `query`, `frontmatter`, `modify`, `reinject`, `detect`, `sections`,
`metadata`.

Wiring points:
- `parser.py::_add_ast_namespace()` — add `_add_quiet_argument(x_parser)` next to each existing
  `_add_root_argument(x_parser)` call (10 call sites, mechanically identical to the existing pattern).
- `main.py::_handle_ast()` — add `quiet = getattr(args, "quiet", False)`; add `quiet=quiet` to each of
  the 10 `ast_*` function calls.
- `ast_commands.py` — every `ast_*` function signature gains `quiet: bool = False`, threaded to
  `_read_file(file_path, root, quiet)`; `ast_modify` additionally threads it to the human-facing
  read-time note (write-time internal recheck always uses `quiet=True` per DD-3, independent of the
  caller's flag value).

---

### 7. Design Decisions Requiring Owner Sign-off

| ID | Decision | Recommendation | Rationale |
|---|---|---|---|
| **DD-1** | Extend the R-3 broad-root stderr warning to `configured` roots (not just `--root`)? | **Yes, include.** | A broad `ast.trusted_roots` entry is the same trust posture as a broad `--root` (deliberate user configuration) — symmetry closes a gap the mandate didn't explicitly ask for but that follows directly from "explicit trust deserves visibility." Low implementation cost (reuses the same `_is_broad_containment_root` call already computed by `resolve_allowed_roots()` for every root, including `configured` ones). |
| **DD-2** | Remove `_check_temp_root_ownership` entirely, or retain a fail-closed variant scoped to `configured` roots? | **Remove entirely (default recommendation).** | The gate's sole rationale (safe auto-trust of *shared, multi-tenant* OS temp dirs) does not exist under Option C — `configured` roots are never auto-trusted, they are explicit per-user declarations, the same trust class as `--root` (which has never had an ownership gate). Retaining a check the design no longer needs adds a fail-closed-vs-fail-open decision surface, an OS-conditional (`os.name == "nt"`) branch, and 8 tests for defense-in-depth against a threat model (implicit multi-tenant sharing) that no longer applies to the resource being checked. **If the owner prefers defense-in-depth** (e.g., a `configured` root could still be a genuinely shared directory the user trusts but doesn't fully control write-ownership within), the fallback design is: keep `_check_temp_root_ownership`, scope it to `classification == "configured"` matches only (never `"project"`/`"explicit"`), and invert its `except OSError: pass` to `except OSError: return "<fail-closed message>"` — satisfying the mandate's explicit fallback requirement ("If any ownership check survives for configured roots, it MUST fail CLOSED, never open"). |
| **DD-3** | Should the `ast_modify` write-time recheck's internal `_check_path_containment` call always pass `quiet=True`, regardless of the CLI `--quiet` flag? | **Yes.** | Without this, a configured-root match would print the R-4 note twice per `ast modify` invocation (once at read, once at write) — a UX/log-noise regression, not a security one. The containment *check itself* remains fully unconditional (enforced every time); only the human-facing note is deduplicated. Documented explicitly so a future reader does not mistake this for silently weakening write-time enforcement. |
| **DD-4** | Should `adapter.py::_create_config_adapter()` be refactored to call the new shared `project_root.build_layered_config_adapter()` factory (eliminating the now-duplicated construction logic), or left as-is with only the new defaults-dict entry added? | **Refactor recommended, non-blocking.** | Reduces duplication and guarantees `jerry ast` and `jerry config` never drift on precedence/path resolution. Not required for BUG-010 to close (the mandate's REQUIRED item is only the defaults-dict entry); flagged as a fast-follow to avoid scope creep on a security-relevant PR that is already carrying a 0.64→≥0.92 quality-gate re-score obligation. |

---

## L2 Strategic Implications

**OWASP SAMM trajectory:** This change moves the `jerry ast` containment control from an **implicit,
code-derived trust boundary** (SAMM Design/Threat Assessment maturity: ad hoc — trust decisions
embedded in helper-function logic, invisible to the user and to config review) toward an **explicit,
declared trust boundary** (target: defined — trust is a first-class, versioned, auditable
configuration value subject to the same `jerry config show --source` visibility as every other Jerry
setting). This is a direct maturity improvement in SAMM's **Operations: Incident Management** and
**Design: Security Requirements** practices — a security reviewer can now answer "what does `jerry
ast` trust?" by running `jerry config get ast.trusted_roots`, rather than reading source code or a
tournament report. It also improves **Governance: Policy & Compliance** posture: `ast.trusted_roots`
is a policy artifact that can be set at the framework layer (`.jerry/config.toml`, shared across a
team via version control) or the project layer, giving organizations a config-as-code mechanism for
constraining `jerry ast`'s blast radius per-repository rather than relying on every engineer's local
OS temp-directory layout.

**Technical debt introduced/retired:**

- *Retired:* the entire index-based-trust code smell (C1) and its two downstream fragile assumptions
  (C3 fail-open, C4 same-UID convergence) are deleted, not patched — this is debt reduction, not debt
  deferral. The `_HARDCODED_TMP` seam (a private, test-only monkeypatch point that existed purely to
  make an implicit auto-trust decision testable) is also deleted; test doubles for the new design
  monkeypatch a genuine I/O boundary (`_load_trusted_roots`) rather than a magic constant.
- *Introduced (flagged, not hidden):* the `LayeredConfigAdapter` duplication between `adapter.py` and
  `project_root.py` (DD-4) is a small, explicitly-tracked debt item with a recommended fast-follow.
  The session-local config-layer gap (documented in [Section 2](#2-asttrusted_roots-config-contract))
  is **pre-existing**, not introduced by this change, but this plan is the first place it is written
  down precisely — worth a follow-up worktracker item (`ConfigSource.SESSION_LOCAL` is modeled in the
  domain but never wired into `LayeredConfigAdapter.get()`) so a future config key does not silently
  assume session-local override works when it currently cannot.

**Long-term maintainability:** the pure/impure split (`containment_policy.py` vs. `project_root.py`)
establishes a reusable pattern for any *future* Jerry CLI namespace that needs path-containment-style
policy decisions (the pure `ContainmentRoot`/`resolve_allowed_roots` shape generalizes beyond `ast` —
e.g., a hypothetical `jerry transcript` file-write containment policy could reuse the same value object
with a different classification vocabulary). The removal of OS-environment-dependent auto-trust also
removes a class of **non-reproducible CI failures**: a test or production run whose behavior depended
on `TMPDIR`/`/tmp` existing, being writable, or matching `gettempdir()` across macOS/Linux/CI runners
is now impossible by construction, because those paths are no longer inputs to the containment
decision at all.

**Dependency strategy evolution:** zero new third-party dependencies. The change deepens reliance on
two already-adopted internal seams (`LayeredConfigAdapter`, `EnvConfigAdapter`) rather than widening
the dependency surface — consistent with the mandate's "Do NOT invent a new config mechanism"
constraint and with Jerry's existing dependency-governance posture of preferring composition over new
libraries for CLI-internal policy logic.

---

## Appendix: SSDF / MS SDL Mapping

| Practice | Application to this plan |
|---|---|
| **PO.1** (define security requirements) | Section 3 (C1–C6 mapping) translates the C4 tournament's adversarial findings directly into implementation requirements; Section 7 (DD-1–DD-4) captures requirements decisions still open for explicit owner sign-off. |
| **PO.3** (supporting toolchains) | Section 6's coverage-verification command wires `pytest --cov` scoped to the changed packages; no new lint/format tooling required (existing `ruff`/`mypy` config in `testing-standards.md` applies unchanged). |
| **PS.1** (protect code from tampering) | N/A beyond existing repository controls (branch protection, PR review) — no new artifact-integrity mechanism introduced by this change. |
| **PS.2** (verify release integrity) | N/A — no release/build artifact changes; this is source-level policy logic only. |
| **MS SDL — Requirements phase** | This entire document *is* the Requirements-phase artifact: threat-model findings (tournament) → implementation requirements (Sections 1–6) → explicit residual-risk decisions requiring sign-off (Section 7) before eng-backend begins Design/Implementation. |

---

*Prepared by eng-lead. Inputs: `RESUME-HERE.md`, `adv-s014-tournament-score.md` (S-014 tournament
aggregation, C4, 0.64 REVISE), direct reads of `src/interface/cli/project_root.py`,
`src/interface/cli/ast_commands.py`, `src/interface/cli/adapter.py`,
`src/infrastructure/adapters/configuration/layered_config_adapter.py`,
`src/infrastructure/adapters/configuration/env_config_adapter.py`, `src/interface/cli/parser.py`,
`src/interface/cli/main.py`, and the existing test suites in
`tests/unit/interface/cli/test_project_root.py`, `tests/unit/interface/cli/test_ast_commands.py`,
`tests/integration/cli/test_ast_subprocess.py`. No source files modified by this planning pass. No
code written — this is a plan artifact only, per the task mandate. Persisted per P-002.*
