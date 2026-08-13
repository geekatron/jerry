# FMEA Report: BUG-010 Option C — `jerry ast` Containment Redesign

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `eng-lead-option-c-plan.md` + implementation (`src/interface/cli/containment_policy.py`,
`project_root.py`, `ast_commands.py`, `parser.py`, `main.py`, `adapter.py`) on
`fix/BUG-010-ast-project-root` @ `cce557c5`
**Criticality:** C4 (Critical — irreversible security control, public CLI surface, AE-005)
**Date:** 2026-08-10
**Reviewer:** adv-executor (blind Group 5/6 — Decompose, S-012 FMEA pass)
**H-16 Compliance:** Executed as a blind single-strategy tournament pass per orchestrator instruction;
S-003 Steelman is a separate blind pass in this tournament (not sequentially available to this
execution, consistent with the C4 tournament's blind-pass design — see `RESUME-HERE.md`).
**Elements Analyzed:** 14 | **Failure Modes Identified:** 18 | **Total RPN:** 1651

---

## Summary

Fourteen elements of the Option C containment redesign were decomposed (pure policy, I/O adapter,
orchestration/CLI wiring, config precedence, cross-platform semantics, and operational/migration
concerns) and examined against all five FMEA failure-mode lenses. Eighteen failure modes were
identified: one **Critical** (RPN 288 — the `ast_modify` write-time TOCTOU recheck computes and
discards a fresh resolved path but writes to a separately-captured, earlier-resolved `target_path`,
reopening a narrow race window in the exact control the design explicitly claims to close "at the
design level"), eight **Major** (RPN 80–199, spanning a silent config-precedence surprise, an
unflagged broad-root gap, a Windows `realpath`/`resolve()` divergence risk, and the documented
scratchpad-trust functional regression with no migration path), and nine **Minor** findings. The
implementation is otherwise disciplined and closely tracks its own design document (all 6 tournament
findings C1–C6 are dispositioned as claimed, and the DD-4 refactor was implemented ahead of its
"non-blocking" framing). **Recommendation: REVISE** — the single Critical finding (FM-001) must be
corrected before merge; the Major findings should be triaged and at minimum documented as accepted
residual risk with owner sign-off, mirroring the plan's own DD-1–DD-4 pattern.

---

## Element Inventory

| ID | Element | Description |
|----|---------|-------------|
| E-01 | `containment_policy.resolve_allowed_roots` | Pure classification/dedup of project + configured + explicit roots |
| E-02 | `containment_policy._is_broad_containment_root` | Broad-root heuristic (filesystem root, home, home-ancestor) |
| E-03 | `project_root.get_project_root` | Resolves `CLAUDE_PROJECT_DIR` / cwd as the always-trusted "project" root |
| E-04 | `project_root.build_layered_config_adapter` | Shared adapter factory + `JERRY_PROJECT` traversal fail-closed guard |
| E-05 | `project_root._load_trusted_roots` | Reads `ast.trusted_roots`, filters blank entries |
| E-06 | `project_root.get_containment_roots` | I/O orchestration: resolves roots, emits R-3/relative-path stderr warnings |
| E-07 | `ast_commands._check_path_containment` | Containment match + symlink re-verification (read path) |
| E-08 | `ast_commands.ast_modify` (write path) | TOCTOU recheck + atomic temp-file/rename write |
| E-09 | CLI wiring (`parser.py`, `main.py`) | `--quiet`/`--root` argument definitions and threading into all 10 `ast_*` calls |
| E-10 | `adapter.py::_create_config_adapter` | `ast.trusted_roots` defaults-dict entry; DD-4 refactor status |
| E-11 | Config precedence & env parsing | `LayeredConfigAdapter` (env > project > root > default) + `EnvConfigAdapter._parse_value` |
| E-12 | Cross-platform path semantics | Windows/macOS/Linux differences in `resolve()`, `realpath()`, case-sensitivity |
| E-13 | Operational/migration/UX | Scratchpad-trust regression, error message actionability, introspection tooling |
| E-14 | `_ENFORCE_PATH_CONTAINMENT` kill switch | Module-import-time env-gated bypass of all containment logic |

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-20260810T1400 | E-08 `ast_modify` | Write-time TOCTOU recheck's resolved path is discarded (`_`); actual write uses an earlier, separately-captured `target_path` | 9 | 4 | 8 | 288 | Critical | Reuse the recheck's returned resolved path as the literal write target; never re-derive | Methodological Rigor |
| FM-002-20260810T1400 | E-05/E-11 | `JERRY_AST__TRUSTED_ROOTS=""` (blank) silently overrides (not merges with) project/root TOML config, with no diagnostic | 5 | 5 | 7 | 175 | Major | Emit a stderr note when env is present-but-blank AND file config has non-empty entries | Internal Consistency |
| FM-003-20260810T1400 | E-02 `_is_broad_containment_root` | Monorepo/shared-checkout root (e.g. the whole Jerry repo, containing multiple users' `projects/`) is not flagged "broad" — only filesystem root / home / home-ancestor are | 6 | 4 | 7 | 168 | Major | Extend broad-root heuristic or document the gap explicitly in `--help`/config key docs | Completeness |
| FM-004-20260810T1400 | E-07/E-12 | `os.path.realpath()` vs `Path.resolve()` may diverge on Windows (`\\?\` extended-path prefix) for ordinary long paths, causing spurious symlink-branch rejections | 5 | 4 | 7 | 140 | Major | Normalize both resolutions (strip/compare `\\?\` consistently) before comparing; add a Windows long-path regression test | Evidence Quality |
| FM-005-20260810T1400 | E-03/E-06 | Broad **project** root (e.g. `CLAUDE_PROJECT_DIR=/`) never triggers a warning, even without `--quiet` — asymmetric with `configured`/`explicit` | 7 | 2 | 8 | 112 | Major | Emit the same R-3-style warning for a broad project root (non-fatal, informational) | Completeness |
| FM-006-20260810T1400 | E-13 | No default/migration bootstrap for existing scratchpad workflows; the design's own "primary use case" breaks immediately post-deploy | 6 | 9 | 2 | 108 | Major | Ship a documented `ast.trusted_roots` recommendation (e.g. in `RESUME-HERE.md`/release notes) and/or a first-run hint | Actionability |
| FM-007-20260810T1400 | E-13 | Containment-rejection error message never mentions `ast.trusted_roots` as the remediation path | 4 | 8 | 3 | 96 | Major | Append `"configure ast.trusted_roots to allow this location"` to the rejection message | Actionability |
| FM-008-20260810T1400 | E-14 | `_ENFORCE_PATH_CONTAINMENT` is cached at module import time; env leakage into a long-lived/child process permanently disables containment with no runtime signal | 8 | 2 | 6 | 96 | Major | Re-read the env var per-invocation (or log a one-time startup warning when disabled) | Internal Consistency |
| FM-009-20260810T1400 | E-02/E-12 | Cross-`PurePath`-flavour or cross-drive-letter home-ancestor comparisons silently resolve to "not broad" (`TypeError`/`ValueError` caught and swallowed) | 5 | 3 | 6 | 90 | Major | Add explicit same-flavour assertion/test; document the cross-drive limitation | Evidence Quality |
| FM-010-20260810T1400 | E-09 | `--quiet` threading across all 10 `ast_*` call sites is verified by only a "representative" subset per the plan's own Section 6, not exhaustive parametrization | 4 | 3 | 6 | 72 | Minor | Parametrize the quiet-wiring regression test across all 10 subcommands | Traceability |
| FM-011-20260810T1400 | E-13 | No introspection command to show which classification (`project`/`configured`/`explicit`) would resolve for a given path without a full validate/parse | 3 | 5 | 4 | 60 | Minor | Consider a `jerry ast --explain-containment` diagnostic (non-blocking) | Actionability |
| FM-012-20260810T1400 | E-09 | `_add_root_argument` docstring/help text still describes the pre-Option-C default ("OS temp/scratchpad directories") | 2 | 10 | 2 | 40 | Minor | Update docstring/help text to match Option C's actual default set | Traceability |
| FM-013-20260810T1400 | E-11 | `EnvConfigAdapter._parse_value` boolean/int/float coercion can misclassify a bare numeric/boolean-keyword path value | 3 | 2 | 6 | 36 | Minor | Document; or bypass generic coercion for the `ast.trusted_roots` key specifically | Internal Consistency |
| FM-014-20260810T1400 | E-11 | CSV-fallback env parsing splits a literal comma inside a single path into two entries (already self-documented) | 3 | 3 | 4 | 36 | Minor | Recommend JSON-array form in the key's own error/help output, not just the design doc | Evidence Quality |
| FM-015-20260810T1400 | E-10 | Design doc frames DD-4 as "non-blocking, not required" but the shipped code already implements it — doc/code drift | 2 | 6 | 3 | 36 | Minor | Update `eng-lead-option-c-plan.md` Section 7 to reflect DD-4 as resolved/implemented | Traceability |
| FM-016-20260810T1400 | E-04 | `JERRY_PROJECT` traversal fail-closed warning has no `quiet` parameter — inconsistent with every other stderr note in this feature | 2 | 6 | 3 | 36 | Minor | Either thread `quiet` through consistently, or document this one as intentionally non-suppressible | Internal Consistency |
| FM-017-20260810T1400 | E-05/E-06 | Relative `ast.trusted_roots` entries resolve against invocation CWD, not project root (documented, tested, warn-and-honor) | 4 | 4 | 2 | 32 | Minor | No action required beyond existing warning; consider a future MEDIUM-tier "reject relative" mode | Internal Consistency |
| FM-018-20260810T1400 | E-01 | A `configured` root that is a subdirectory of another already-added root is not deduplicated (harmless but produces redundant list entries/warnings) | 2 | 5 | 3 | 30 | Minor | Optional: collapse subdirectory-redundant entries in `resolve_allowed_roots` | Completeness |

---

## Finding Details (Critical and Major)

### FM-001-20260810T1400 — TOCTOU write-target divergence in `ast_modify`

- **Element:** E-08, `ast_commands.ast_modify` (`src/interface/cli/ast_commands.py:604-654`)
- **Failure Mode:** Incorrect / Insufficient. The write path executes, in order: (1) `_read_file`
  (read-time containment check, resolves `file_path` fresh); (2) `target_path = Path(file_path).resolve()`
  at line 620 — a **second, independent** resolve, captured for later use as the literal write
  destination; (3) the write-time TOCTOU recheck at line 634-635,
  `_, write_time_error = _check_path_containment(file_path, root, quiet=True)` — a **third**
  independent resolve, whose returned resolved path is discarded (bound to `_`); (4) `mkstemp`/`os.replace`
  write to `target_path` from step (2), never to the path actually validated in step (3).
- **Effect:** If an attacker swaps the symlink at `file_path` between steps (2) and (3) — e.g. from an
  outside target to an inside one, so the step-(3) check passes — the write in step (4) still targets
  the **step-(2)** resolution, which was never re-validated at the moment it is used. A single race
  (swap once, before `ast_modify` is even invoked) is exactly what the existing regression test
  (`test_ast_modify_when_symlink_swapped_between_read_and_write_then_rejected_at_write_time`) exercises
  and correctly rejects — but that test's swap happens *before* step (2), so steps (2) and (3) observe
  the *same* (already-swapped) resolution and agree by coincidence, not by construction. A second swap
  timed between steps (2) and (3) is not covered by any existing test, and the code's own structure
  (three independent `Path(file_path).resolve()` calls for what should be one logical decision) makes
  the check-then-use guarantee the design document claims ("literally the same function call... closing
  C2 at the design level") not actually hold for the value that is written.
- **S/O/D Rationale:** S=9 — this is a residual bypass of the exact security property (write-path
  containment) that C2 was the mandate's core requirement to fix; a successful race writes attacker
  content to a location that was never validated. O=4 — requires precisely-timed, adversary-controlled
  symlink manipulation; achievable with `inotify`-style event-driven synchronization rather than blind
  timing (a well-documented TOCTOU exploitation technique), not merely theoretical, but requires local
  filesystem write access to the target's ancestor directory. D=8 — undetectable by the current test
  suite (which validates the single-swap-before-invocation case only) and easy to miss on a design-level
  read, since the write-time recheck function call *looks* identical to the read-time one; only a
  line-level trace of which variable each of the three resolves feeds into reveals the gap.
- **Corrective Action:** Change the write-time recheck to return and use its own resolved path as the
  literal `os.replace()` destination — i.e., replace `_, write_time_error = _check_path_containment(...)`
  with `write_time_resolved, write_time_error = _check_path_containment(...)` and use
  `write_time_resolved` (not the earlier `target_path`) for both `tempfile.mkstemp(dir=...)` and
  `os.replace(...)`. This collapses the three independent resolves into two (read-time, write-time) and
  makes the value that is checked and the value that is written provably identical.
- **Acceptance Criteria:** A new test that swaps the symlink *between* the current `target_path` capture
  and the write-time recheck (not before `ast_modify` is invoked) must be rejected, and the file at the
  step-(2) resolution must remain unmodified.
- **Post-Correction RPN Estimate:** S=9 (unchanged — still security-relevant code), O=1 (race eliminated
  by construction), D=2 (covered by the new targeted test) → **18**.

### FM-002-20260810T1400 — Blank env var silently overrides file-configured trusted roots

- **Element:** E-05/E-11, `project_root._load_trusted_roots` + `LayeredConfigAdapter.get()`
- **Failure Mode:** Inconsistent. `LayeredConfigAdapter.get()` implements strict override (not merge)
  precedence: if `EnvConfigAdapter.has(key)` is `True`, the env value is returned unconditionally,
  regardless of whether project/root TOML config has its own (non-empty) value for the same key.
  `EnvConfigAdapter._parse_value("")` returns `""` (not `None`), so `has()` is `True` even for a blank
  env var — a common artifact of unresolved shell/CI variable interpolation (e.g. a templated `.env`
  file with an unset upstream variable). `_load_trusted_roots()`'s blank-filter then reduces this to
  `[]`, correctly avoiding the AC-11 cwd-widening bug, but **any TOML-configured trusted roots are
  never consulted at all** — the effective result is silent, total suppression of an operator's
  file-level configuration, indistinguishable from "no trusted roots were ever configured."
- **Effect:** An operator who has legitimately configured `ast.trusted_roots` in `.jerry/config.toml`
  will see `jerry ast` reject files they expect to be trusted, with `jerry config get ast.trusted_roots`
  reporting the env-sourced empty value and no signal that the file config was shadowed rather than
  absent. This is a debuggability/availability regression, not a security bypass (the fail direction is
  safe), but is exactly the kind of "config-precedence surprise" this review was asked to surface.
- **S/O/D Rationale:** S=5 (moderate — availability/diagnosability, not a security hole). O=5 (blank env
  var propagation from CI/container templating is a common, realistic failure class). D=7 (no log line
  or warning distinguishes "never configured" from "env-shadowed"; only `get_source()` inspection would
  reveal it, and nothing currently prompts the operator to check).
- **Corrective Action:** In `_load_trusted_roots()`, detect the case where the env source is present but
  parses to an empty/blank value while project or root file config has a non-blank `ast.trusted_roots`
  entry, and emit a one-line stderr note (respecting `quiet`) explaining that the environment variable
  is shadowing file configuration.
- **Acceptance Criteria:** A test with a non-empty TOML `ast.trusted_roots` and a blank
  `JERRY_AST__TRUSTED_ROOTS` env var asserts both (a) the effective trusted-roots list is empty (safe
  default preserved) and (b) a stderr diagnostic identifies the shadowing.
- **Post-Correction RPN Estimate:** S=5, O=5, D=2 → **50**.

### FM-003-20260810T1400 — Broad shared-checkout root not flagged by the broad-root heuristic

- **Element:** E-02, `containment_policy._is_broad_containment_root`
- **Failure Mode:** Insufficient. The heuristic flags only filesystem/drive roots and the home directory
  (or its ancestors). A `configured` root pointing at the Jerry monorepo checkout itself, or any other
  broad shared directory that is neither a filesystem root nor a home-directory ancestor (e.g. a shared
  team NFS mount, a CI workspace root containing multiple projects), receives **no** broad-root warning
  even though trusting it grants `jerry ast` access to sibling projects' files, secrets, and `.env`
  content in a shared-checkout deployment model.
- **Effect:** An operator configuring `ast.trusted_roots = ["/path/to/monorepo"]` (a plausible
  misconfiguration when someone "just wants jerry ast to work everywhere in my repo") gets zero
  transparency signal, unlike the equivalent home-directory case which is explicitly and correctly
  flagged.
- **S/O/D Rationale:** S=6 (broad but non-catastrophic — scoped to files within one shared checkout, not
  the whole filesystem). O=4 (plausible operator misconfiguration, not attacker-driven). D=7 (silently
  accepted; no code path warns).
- **Corrective Action:** Document the heuristic's scope limitation explicitly in the `ast.trusted_roots`
  help text/config docs ("broad-root detection covers filesystem roots and home-directory ancestors
  only; a large shared checkout will not be flagged"), and/or consider extending detection to
  well-known multi-project container markers (e.g. a directory containing multiple sibling
  `projects/PROJ-*` trees).
- **Acceptance Criteria:** Documentation update merged; optional heuristic extension covered by a new
  test if implemented.
- **Post-Correction RPN Estimate (docs-only fix):** S=6, O=4, D=3 → **72**.

### FM-004-20260810T1400 — `os.path.realpath()` / `Path.resolve()` Windows divergence risk

- **Element:** E-07/E-12, `ast_commands._check_path_containment`
- **Failure Mode:** Incorrect (cross-platform). `_check_path_containment` treats `resolved != realpath`
  as the *sole* signal that a symlink was involved and additionally re-verifies via `realpath`. On
  Windows, `os.path.realpath()` and `pathlib.Path.resolve()` are documented to diverge in their
  handling of the `\\?\` extended-length-path prefix in some Python/OS combinations — meaning
  `resolved != realpath` can be spuriously true for an **ordinary, non-symlinked** file (particularly
  long paths), triggering the extra `realpath`-based containment check against `allowed_roots`
  (computed via `Path.resolve()`, without the `\\?\` prefix). If the `\\?\`-prefixed string never
  textually matches any allowed root's `Path.resolve()` form, a legitimate file is rejected.
- **Effect:** Functional regression specific to Windows: certain valid, non-malicious file paths (long
  paths, or paths under directories that trigger extended-path normalization) could be rejected with
  "Symlink target escapes allowed containment roots" even though no symlink is involved.
- **S/O/D Rationale:** S=5 (breaks legitimate usage on one of three CI-tested platforms; not a security
  issue). O=4 (specific to certain Windows path lengths/locations, not universal, but the codebase's own
  CI matrix explicitly tests `windows-latest`, increasing the chance real paths eventually trigger it).
  D=7 (the 3-OS CI matrix uses short `tmp_path` fixtures that are unlikely to exercise the `\\?\`
  threshold, so this would likely surface only in real-world long-path usage, not CI).
- **Corrective Action:** Normalize both `resolved` and `realpath` to a common form (e.g. strip a leading
  `\\?\` before comparison, or use `os.path.realpath(file_path, strict=False)` consistently on both
  sides) before deciding whether the extra symlink-target check applies; add a Windows-specific
  regression test using a deliberately long path.
- **Acceptance Criteria:** A Windows CI test with a path length near/above 260 characters (or a path
  under a location known to trigger `\\?\` normalization) parses successfully with no false rejection.
- **Post-Correction RPN Estimate:** S=5, O=2, D=3 → **30**.

### FM-005-20260810T1400 — Broad project root never warned, even without `--quiet`

- **Element:** E-03/E-06, `get_project_root` / `get_containment_roots`
- **Failure Mode:** Missing. `get_containment_roots()` explicitly and deliberately skips the R-3 broad-root
  warning for the `"project"` classification (confirmed by
  `test_get_containment_roots_when_no_explicit_root_then_no_warning_regardless_of_project_root`), on the
  stated rationale that "the project root is always the user's own repository by construction of
  `get_project_root()`." That construction depends entirely on `CLAUDE_PROJECT_DIR` (or, absent it, cwd)
  being correctly scoped — an environmental precondition, not an invariant the code enforces.
- **Effect:** If `CLAUDE_PROJECT_DIR` is ever misconfigured to a very broad location (e.g. `/`, a
  container's root filesystem, or cwd happens to be `/` in a broken entrypoint), containment is
  effectively disabled for the entire invocation, and — uniquely among all three classifications — the
  user receives **no** signal of this, not even in verbose (non-`--quiet`) mode.
- **S/O/D Rationale:** S=7 (if triggered, blast radius equals an unwarned filesystem-root trust grant —
  the worst-case containment outcome). O=2 (requires environmental misconfiguration, not user/attacker
  choice; low likelihood in normal Claude Code / CLI operation). D=8 (by design, silent in all modes).
- **Corrective Action:** Extend the R-3-style warning to the `"project"` classification as well
  (informational, non-fatal, matching the `configured`/`explicit` treatment) — this closes the one
  asymmetry in an otherwise-consistent transparency model without changing the underlying trust
  decision.
- **Acceptance Criteria:** A test with a monkeypatched broad `CLAUDE_PROJECT_DIR` asserts a stderr
  warning is printed (and suppressed under `--quiet`, consistent with the other two classifications).
- **Post-Correction RPN Estimate:** S=7, O=2, D=2 → **28**.

### FM-006-20260810T1400 — No migration path for the scratchpad-trust functional regression

- **Element:** E-13, operational/deployment
- **Failure Mode:** Missing. Option C's core mandate ("NO automatic temp/scratchpad trust") is a
  deliberate, well-reasoned security improvement, but it is also, by the design document's own words, a
  break of "the design's own stated primary use case (agent scratchpad ops)." No default
  `ast.trusted_roots` bootstrap, first-run detection, or even a repo-level `.jerry/config.toml` entry
  for this repository's own scratchpad convention was found (`grep` for `trusted_roots` across the repo
  returns no non-test, non-source configuration file).
- **Effect:** Every existing workflow, skill, or agent that writes to a Claude Code scratchpad directory
  and then calls `jerry ast validate`/`parse`/`modify` against it will begin failing with exit code 2
  immediately upon this change landing, until every operator independently discovers and configures
  `ast.trusted_roots`.
- **S/O/D Rationale:** S=6 (workflow interruption across many callers, not data loss or security harm —
  the fail direction is safe). O=9 (near-certain to affect the documented primary use case immediately).
  D=2 (trivially detected — the CLI fails loudly on the very next invocation).
- **Corrective Action:** Ship migration guidance alongside the change (e.g. a `RESUME-HERE.md`/release
  note snippet showing the recommended `ast.trusted_roots` entry for scratchpad directories), and
  consider whether the framework's own bootstrap/session-start tooling should offer to configure it.
- **Acceptance Criteria:** Migration note merged in the same PR; optionally, a `jerry ast` first-failure
  hint (see FM-007) covers the same gap at the point of failure.
- **Post-Correction RPN Estimate:** S=6, O=9, D=1 → **54** (Detection improves once guidance exists;
  Occurrence is inherent to the deliberate behavior change and does not reduce).

### FM-007-20260810T1400 — Rejection error message omits remediation guidance

- **Element:** E-13, `ast_commands._check_path_containment`
- **Failure Mode:** Insufficient. The sole rejection message,
  `f"Path escapes allowed containment roots: {file_path}"`, states the failure but not the fix. A
  first-time operator hitting this (see FM-006) has no in-tool signal that `ast.trusted_roots` is the
  intended remediation mechanism.
- **Effect:** Increased support burden / time-to-resolution for every operator who first encounters this
  error without having read the design document.
- **S/O/D Rationale:** S=4 (pure actionability gap). O=8 (fires on essentially every un-configured
  scratchpad/out-of-project access attempt post-deploy). D=3 (the failure itself is loud and immediate;
  only the *remediation path* is undiscoverable, which is a mild, quickly-Googled/asked gap rather than
  a silent one).
- **Corrective Action:** Extend the error message: `"Path escapes allowed containment roots: {file_path}. `
  `To allow this location, add it to the 'ast.trusted_roots' config key (see 'jerry config --help')."`
- **Acceptance Criteria:** Updated message text asserted by an existing or new unit test.
- **Post-Correction RPN Estimate:** S=4, O=8, D=1 → **32**.

### FM-008-20260810T1400 — Import-time caching of the containment kill switch

- **Element:** E-14, `_ENFORCE_PATH_CONTAINMENT`
- **Failure Mode:** Incorrect/Insufficient. `_ENFORCE_PATH_CONTAINMENT` is computed once, at module
  import time, from `JERRY_DISABLE_PATH_CONTAINMENT`. This is a pre-existing mechanism (not introduced
  by Option C), but Option C's entire hardening effort is gated behind it: if this variable is ever set
  to `"1"` and leaks into a non-test process (e.g. a subprocess that inherits environment from a test
  harness, CI job, or a long-lived worker that forked before the variable was cleared), **all** of the
  Option C containment logic — including the newly-fixed C1–C6 items — is bypassed silently, with no
  startup log line indicating containment is disabled.
- **Effect:** Complete containment bypass for the process lifetime if triggered; the risk is orthogonal
  to (not introduced by) Option C, but Option C raises the stakes of this pre-existing kill switch by
  making it the single point of failure for six distinct hardening fixes at once.
- **S/O/D Rationale:** S=8 (total containment bypass if triggered). O=2 (requires env leakage from a
  test/CI context into a production invocation — a known class of CI/subprocess hygiene bug, but not
  routine). D=6 (no runtime signal that containment is disabled; only discoverable via source inspection
  or by noticing containment doesn't fire when expected).
- **Corrective Action:** At minimum, print a one-time stderr warning at the point `_ENFORCE_PATH_CONTAINMENT`
  is `False` and any `ast_*` command actually runs, so a leaked env var is immediately visible rather
  than silently discovered later.
- **Acceptance Criteria:** A test asserts a stderr warning fires on the first `ast_*` invocation when
  `JERRY_DISABLE_PATH_CONTAINMENT=1` is set outside the dedicated subprocess-test fixture context.
- **Post-Correction RPN Estimate:** S=8, O=2, D=2 → **32**.

### FM-009-20260810T1400 — Cross-flavour/cross-drive home-ancestor detection gap

- **Element:** E-02/E-12, `_is_broad_containment_root`
- **Failure Mode:** Insufficient (cross-platform). The home-ancestor check compares `resolved` (which
  may be a `PureWindowsPath` per the function's documented cross-flavour testability) against
  `Path.home()` (always the *host's native* flavour). A `PureWindowsPath` evaluated on a POSIX host (or,
  on native Windows, a path on a different drive letter than the resolved home directory, e.g. via a
  mapped/junctioned drive) causes `resolved == home` to be `False` and `home.relative_to(resolved)` to
  raise `ValueError`/`TypeError` (both caught, both treated as "not broad") — silently under-flagging a
  genuinely broad root rather than erring toward caution.
- **Effect:** A configured or explicit root that is, in effect, an ancestor of the user's home directory
  on a different drive letter (a realistic Windows enterprise pattern with mapped network drives) would
  not receive the broad-root warning.
- **S/O/D Rationale:** S=5 (transparency gap, not a containment bypass — the *matching* logic in
  `_check_path_containment` is unaffected; only the *warning* is missed). O=3 (requires a Windows
  multi-drive/junction environment). D=6 (silent, undocumented as a limitation).
- **Corrective Action:** Document the cross-drive/cross-flavour limitation explicitly in the function's
  docstring (it currently documents the cross-flavour *testability* feature but not this side effect),
  and add a same-flavour precondition assertion at the `resolve_allowed_roots` boundary in production
  code paths (test-only cross-flavour use would be unaffected).
- **Acceptance Criteria:** Docstring updated; optional test documenting the known limitation explicitly
  (as already done for `test_is_broad_containment_root_when_home_undeterminable_then_false`).
- **Post-Correction RPN Estimate:** S=5, O=3, D=2 → **30**.

---

## Recommendations

**Critical (mandatory before merge):**

| FM-NNN | Corrective Action | Est. RPN Reduction |
|--------|--------------------|---------------------|
| FM-001 | Reuse the write-time recheck's own resolved path as the literal `os.replace()`/`mkstemp` destination instead of the earlier, separately-captured `target_path` | 288 → 18 |

**Major (recommended before merge, or explicit owner-accepted residual risk per the plan's own DD pattern):**

| FM-NNN | Corrective Action | Est. RPN Reduction |
|--------|--------------------|---------------------|
| FM-002 | Warn when env-sourced `ast.trusted_roots` is blank but file config has non-blank entries | 175 → 50 |
| FM-003 | Document (or extend) the broad-root heuristic's shared-checkout blind spot | 168 → 72 |
| FM-004 | Normalize `Path.resolve()`/`os.path.realpath()` comparison on Windows; add long-path test | 140 → 30 |
| FM-005 | Extend the R-3 broad-root warning to the `"project"` classification | 112 → 28 |
| FM-006 | Ship scratchpad-trust migration guidance alongside the change | 108 → 54 |
| FM-007 | Add remediation text (`ast.trusted_roots`) to the containment rejection error message | 96 → 32 |
| FM-008 | Emit a startup warning when `_ENFORCE_PATH_CONTAINMENT` is disabled at first `ast_*` invocation | 96 → 32 |
| FM-009 | Document the cross-drive/cross-flavour home-ancestor detection limitation | 90 → 30 |

**Minor (improvement opportunities, optional):** FM-010 through FM-018 — see Findings Table; primarily
test-coverage exhaustiveness, stale docstrings, and doc/code drift (FM-015) that should be swept up in
the same PR at low cost.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-003, FM-005, FM-018: broad-root detection and dedup have documented coverage gaps beyond the primary filesystem-root/home cases |
| Internal Consistency | 0.20 | Negative | FM-002, FM-008, FM-016: env-override-vs-file-config precedence, kill-switch visibility, and `--quiet` threading each have one inconsistent corner |
| Methodological Rigor | 0.20 | Negative | FM-001: the write-time TOCTOU recheck does not actually enforce the "same resolved value used for check and write" guarantee the design document claims — the single highest-severity finding in this pass |
| Evidence Quality | 0.15 | Negative | FM-004, FM-009, FM-014: cross-platform claims ("works identically... for POSIX and Windows") are not fully substantiated by the current test suite for the specific divergences identified |
| Actionability | 0.15 | Negative | FM-006, FM-007, FM-011: the deliberate scratchpad-trust regression ships without in-tool remediation guidance or a migration note |
| Traceability | 0.10 | Negative | FM-010, FM-012, FM-015: one stale docstring, one non-exhaustive regression test, and one doc/code drift item (DD-4) reduce audit confidence, though all are low-cost fixes |

**Element with highest total RPN:** E-08 (`ast_modify` write path) — 288 (FM-001 alone), reflecting that
the single most consequential residual gap sits in the exact function the mandate's core requirement
(C2 TOCTOU fix) targeted.

**Overall assessment:** Targeted corrections required. FM-001 is a specific, code-verified logic gap in
a security-critical function and should block merge until fixed (the fix itself is small and low-risk —
reuse an already-computed return value). The Major findings are largely transparency/diagnosability gaps
in an otherwise carefully-reasoned and well-tested redesign (18 tests already cover configurations this
review independently arrived at, e.g. blank-env, relative-root, and broad-root-warning suppression
scenarios) rather than fundamental design flaws; several are reasonable to accept as documented residual
risk following the same DD-1–DD-4 sign-off pattern already used elsewhere in this plan.
