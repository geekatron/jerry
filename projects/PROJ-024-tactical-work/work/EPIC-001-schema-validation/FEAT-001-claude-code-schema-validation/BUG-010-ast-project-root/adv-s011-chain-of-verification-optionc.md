# S-011 Chain-of-Verification Report — BUG-010 Option C `jerry ast` Containment

> **Strategy:** S-011 (Chain-of-Verification), BLIND single-strategy pass, Group 4 of 6 (Verify).
> **Deliverable under review:** `eng-lead-option-c-plan.md` (claims/plan) cross-checked against
> `red-vuln-option-c-findings.md` (prior red-team pass) and the actual shipped source on branch
> `fix/BUG-010-ast-project-root` @ `cce557c5`.
> **Method:** Extracted concrete, falsifiable factual claims from the deliverable; verified each
> against `src/interface/cli/containment_policy.py`, `project_root.py`, `ast_commands.py`,
> `parser.py`, `main.py`, `adapter.py`, and the corresponding test files, using direct source
> reads and `grep`-based structural corroboration. **No Bash tool was available in this agent
> session** — verification is static/source-trace based (line-cited), not live-executed
> (`uv run pytest` / `uv run python` PoCs were not run by this pass; see Verification Method
> Disclosure at the end of this report).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Claim-by-Claim Verification Table](#claim-by-claim-verification-table) | Summary verdicts |
| [Claim 1 — C2 TOCTOU Closure](#claim-1--c2-toctou-closure-partially-true) | Detailed trace of `ast_modify`'s write-time recheck |
| [Claim 2 — Six Prior Criticals Dissolved](#claim-2--six-prior-criticals-dissolved-partially-true) | C1–C6 re-verification |
| [Claim 3 — Coverage / Test-Count Claims](#claim-3--coverage--test-count-claims-partially-verified) | Test presence corroboration |
| [Claim 4 — No Temp Path Feeds the Allowed Set](#claim-4--no-temp-path-feeds-the-allowed-set-verified) | grep evidence |
| [Claim 5 — DD-1..DD-4 Implemented as Described](#claim-5--dd-1dd-4-implemented-as-described-verified-exceeds-plan-on-dd-4) | Design-decision trace |
| [Discrepancies (Severity-Classified)](#discrepancies-severity-classified) | Findings requiring owner attention |
| [Verification Method Disclosure](#verification-method-disclosure) | P-022 honesty note on tooling limits |

---

## Claim-by-Claim Verification Table

| # | Claim (source) | Verdict | Evidence |
|---|---|---|---|
| 1 | "C2 write-path TOCTOU is closed — read-time and write-time are the same function call / a symlink swapped between read and write is caught" (`eng-lead-option-c-plan.md` L39, L188-197; corroborated `red-vuln-option-c-findings.md` AC-2) | **PARTIALLY-TRUE** | `ast_commands.py:620,634-638,654` — see [Claim 1](#claim-1--c2-toctou-closure-partially-true) |
| 2 | "the six prior Criticals are dissolved" (`eng-lead-option-c-plan.md` L34-43, Section 3) | **PARTIALLY-TRUE** (5/6 fully verified; C2's "Fixed" disposition inherits Claim 1's caveat) | See [Claim 2](#claim-2--six-prior-criticals-dissolved-partially-true) |
| 3 | "Estimated ... coverage confirmation ... net effect neutral-to-positive" / 60-test TDD list (`eng-lead-option-c-plan.md` Section 4, Section 6) | **PARTIALLY VERIFIED** (structural presence of named tests confirmed; exact pass/fail + coverage % not independently executed) | See [Claim 3](#claim-3--coverage--test-count-claims-partially-verified) |
| 4 | "no temp path feeds the allowed set" / `tempfile.gettempdir()`/`/tmp`/`_HARDCODED_TMP` removed from default containment (`eng-lead-option-c-plan.md` L42, L156; `red-vuln-option-c-findings.md` AC-5) | **VERIFIED** | See [Claim 4](#claim-4--no-temp-path-feeds-the-allowed-set-verified) |
| 5 | DD-1..DD-4 implemented as described (`eng-lead-option-c-plan.md` Section 7) | **VERIFIED** (DD-4 exceeds the plan's own "non-blocking, optional" framing) | See [Claim 5](#claim-5--dd-1dd-4-implemented-as-described-verified-exceeds-plan-on-dd-4) |

---

## Claim 1 — C2 TOCTOU Closure (PARTIALLY-TRUE)

**Claim, quoted:** *"Write-time recheck now calls the same `_check_path_containment` routine used at
read time (full symlink/realpath re-verification), closing the TOCTOU gap"* (plan L39) and *"This
makes read-time and write-time containment literally the same function call, not merely 'the same
algorithm re-implemented' — closing C2 at the design level ... a symlink swapped between the read
and the write is caught because `_check_path_containment` re-resolves via `os.path.realpath()`
fresh, every call"* (plan L194-197).

**Trace of `ast_modify` (`src/interface/cli/ast_commands.py`):**

```
604   source, exit_code = _read_file(file_path, root, quiet)      # READ-TIME check (1st resolve)
...
620   target_path = Path(file_path).resolve()                     # WRITE-TARGET capture (2nd resolve,
                                                                    #   independent of the check below)
...
634   if _ENFORCE_PATH_CONTAINMENT:
635       _, write_time_error = _check_path_containment(file_path, root, quiet=True)  # WRITE-TIME
                                                                    #   check (3rd resolve, INTERNAL to
                                                                    #   _check_path_containment; its own
                                                                    #   resolved value is discarded via `_,`)
636       if write_time_error is not None:
637           print(...)
638           return 2
...
644   temp_fd, temp_path_str = tempfile.mkstemp(dir=str(target_path.parent), ...)
...
654   os.replace(temp_path_str, str(target_path))                 # ACTUAL WRITE uses target_path
                                                                    #   from line 620, NOT the value
                                                                    #   validated at line 635
```

**Finding:** The claim is true in the narrow sense that `_check_path_containment` (the same
function used at read time) is invoked again at write time, and it does perform a fresh
`os.path.realpath()` resolution internally (`ast_commands.py:248,253`). But the claim's stronger
assertion — "literally the same function call" closes the race, i.e. that the value validated by
the write-time check is the value actually written to — does **not** hold structurally:

- `target_path` (the argument to `os.replace()` at line 654, the actual write destination) is
  captured via its **own, separate** `Path(file_path).resolve()` call at **line 620**, which runs
  **before** the write-time recheck at line 635.
- The write-time recheck at line 635 performs **its own, independent** `Path(file_path).resolve()`
  internally (inside `_check_path_containment`, at `ast_commands.py:248`) — a **third** resolution
  of the same `file_path` string. Its result is explicitly discarded (`_, write_time_error = ...`)
  and never fed back into `target_path` or into the `os.replace()` call.
- Consequently, the value that is *checked* (line 635's internal resolve) and the value that is
  *used* for the write (`target_path` from line 620) are **two separate resolutions of the same
  live filesystem path**, not one shared, atomically-reused value. This is the textbook shape of a
  Check-Then-Use (TOCTOU, CWE-367) defect: whatever is validated is not guaranteed to be what is
  subsequently acted upon, because a filesystem mutation (symlink retarget) occurring **between the
  two `resolve()` calls** (line 620 and the internal call inside line 635) would cause `target_path`
  and the check's resolution to diverge.
- The **specific, narrower** attack this decoupling enables (not tested by the existing suite):
  attacker retargets the symlink to an out-of-bounds location so that `target_path` (line 620)
  captures the **out-of-bounds** resolution, then retargets it **back** to an in-bounds location
  before line 635's internal resolve runs. The write-time check would then see (and pass) the
  **in-bounds** retargeted path, while `target_path` — captured earlier, before the second swap —
  still holds the **out-of-bounds** resolution, and `os.replace(temp_path_str, str(target_path))`
  would write to that out-of-bounds location despite the check having passed.
- **What the existing regression test actually proves** (`tests/unit/interface/cli/test_ast_commands.py:1549-1598`,
  `test_ast_modify_when_symlink_swapped_between_read_and_write_then_rejected_at_write_time`): only
  the **single-swap** scenario — symlink swapped once, after the read, and left swapped through both
  `target_path` capture and the write-time check. In that scenario `target_path` (line 620) and the
  check's internal resolution (line 635) are computed from the **same, unchanged** post-swap
  symlink state (no further mutation occurs between the two calls in the test), so they agree, and
  the test correctly observes rejection. `red-vuln-option-c-findings.md` AC-2 exercises the
  identical single-swap shape and reaches the same (correct, for that shape) DISSOLVED verdict.
  Neither the plan's TDD list (Section 4, test #45) nor `red-vuln`'s AC-2 constructs the two-phase
  swap-then-swap-back-around-the-capture-point scenario described above.

**Practical exploitability caveat (P-022 honesty note):** the window between line 620 and the
internal resolve inside line 635 is a handful of CPython bytecode instructions with no explicit
I/O yield in the Python-level code between them; however, `Path.resolve()` itself performs multiple
`stat()`/`readlink()`-class syscalls per path component internally, each of which is a legitimate
kernel-scheduling boundary. Classic local symlink-race exploits (CWE-367) are conventionally
demonstrated via a spin/retry loop toggling the symlink at high frequency until the race is won —
this is a well-documented, if fiddly, local-attacker technique, not a purely theoretical concern.
This pass did **not** construct or run a live PoC for the double-swap scenario (no Bash tool
available in this session — see [Verification Method Disclosure](#verification-method-disclosure));
the finding is a **structural/design** verification (the code demonstrably checks one resolution
and writes to a different, earlier one), not a confirmed live race-win. Recommend the owner
construct an actual concurrent-process or `ctypes`/`os.fork()`-based race PoC (or a monkeypatched
`Path.resolve()` call-counter test asserting `target_path`'s resolution and the write-time check's
internal resolution are the *same object/call*, not merely equal in the non-adversarial case)
before closing this out.

**Verdict: PARTIALLY-TRUE.** The single-swap TOCTOU (the scenario the deliverable's own PoC and
test target) is genuinely closed. The deliverable's stronger, unqualified claim — "literally the
same function call," implying the checked value and the used value are one and the same — is not
structurally accurate: `target_path` is captured independently, before the check, and the check's
own resolution is never reused for the write. See [Discrepancy A](#discrepancies-severity-classified).

---

## Claim 2 — Six Prior Criticals Dissolved (PARTIALLY-TRUE)

Re-verified each row of `eng-lead-option-c-plan.md` Section 3 against the shipped source:

| ID | Claim | Verdict | Evidence |
|---|---|---|---|
| C1 | Index-based trust bypass dissolved — classification is structural, never array-index | **VERIFIED** | `containment_policy.py:110-173` (`resolve_allowed_roots`) computes `classification` per-root by origin (`"project"`/`"configured"`/`"explicit"`), never by list position. `grep` for `\[0\]`/`allowed_roots\[` across `containment_policy.py`/`ast_commands.py`: zero matches. `_check_path_containment` matches via `next((r for r in allowed_roots if ...), None)` (`ast_commands.py:257`) — a linear predicate scan, not an index lookup. |
| C2 | Write path TOCTOU fixed | **PARTIALLY-TRUE** | See [Claim 1](#claim-1--c2-toctou-closure-partially-true) above. |
| C3 | Ownership gate `except OSError: pass` fail-open dissolved | **VERIFIED** | `grep` for `_check_temp_root_ownership\|geteuid\|st_uid` across `src/interface/cli/`: zero matches. The two remaining `except OSError` blocks in the containment path (`ast_commands.py:249` resolve, `:278` stat) both **return an error result** (fail-closed), not `pass`. A dedicated regression test (`TestOwnershipGateRemoved::test_ast_commands_module_when_imported_then_check_temp_root_ownership_is_not_defined`, `test_ast_commands.py:1781-1784+`) guards against silent reintroduction. |
| C4 | Same-UID/multi-tenant gate defeat dissolved | **VERIFIED** | Same rationale/evidence as C3 — the gate this finding attacked does not exist in the shipped code. |
| C5 | `TMPDIR`/`TEMP` poisoning of the default set dissolved | **VERIFIED** | See [Claim 4](#claim-4--no-temp-path-feeds-the-allowed-set-verified) below. |
| C6 | `--quiet` flag added, suppresses R-3/R-4 stderr only | **VERIFIED** | `parser.py:597-617` (`_add_quiet_argument`), called at 10 subcommand sites (confirmed for `parse`/`render` explicitly at `parser.py:662,674`; pattern is mechanically identical for the remaining 8 per the file's own docstrings). `main.py:432` (`quiet = getattr(args, "quiet", False)`) threaded into all 10 `ast_*` call sites (`main.py:435,437,444,447,449,451,453,455,457,459`). All warning/note `print()` calls in `project_root.py:216-242` and `ast_commands.py:202-207` target `file=sys.stderr` explicitly; the JSON/render payload `print()` calls in `ast_commands.py` (e.g. `:358,384,456,502,545,572,679,715,762,809,856`) have no `file=` argument, i.e. default to stdout — consistent with "stdout is never touched." |

**Verdict: PARTIALLY-TRUE.** 5 of 6 dispositions (C1, C3, C4, C5, C6) are fully verified as claimed.
C2's "Fixed" disposition carries the same caveat documented in Claim 1 — the *class* of TOCTOU
attack the deliverable's own PoC targets is closed, but the "literally the same function call"
framing overstates what the code actually guarantees for the specific write-target value.

---

## Claim 3 — Coverage / Test-Count Claims (PARTIALLY VERIFIED)

**Claim, quoted:** Section 4 lists 60 numbered TDD tests across 5 sub-sections (4.A–4.E); Section 6
claims "Net effect on the repository-wide coverage ratio is expected to be **neutral-to-positive**"
and gives a per-module confidence table.

**What was verified (structural presence, via direct reads + targeted grep):**

| Plan reference | Verified present? | Evidence |
|---|---|---|
| `test_containment_policy.py` (new file, tests #1–19) | **YES** — 20 `def test_` matches found (1 more than the plan's 19; consistent with "at least the claimed set exists," not a discrepancy) | `Grep count` on the file |
| `TestOwnershipGateRemoved` (DD-2 guard, plan test #48) | **YES** | `test_ast_commands.py:1781-1784` |
| `TestTempRootOwnershipGate` (old class) deleted per Section 5 | **YES — confirmed absent** | `grep` for the class name across `tests/unit/interface/cli/`: only a comment reference remains (`test_ast_commands.py:1776`, explicitly noting its removal), no live class definition |
| `test_get_containment_roots_when_no_explicit_root_then_includes_resolved_gettempdir` / `_hardcoded_tmp` tests deleted per Section 5 | **YES — confirmed absent** | `grep` for both names: zero matches anywhere under `tests/unit/interface/cli/` |
| `test_ast_modify_when_symlink_swapped_between_read_and_write_then_rejected_at_write_time` (plan test #45) | **YES** | `test_ast_commands.py:1549` |
| `test_ast_modify_when_configured_root_match_then_transparency_note_prints_exactly_once` (plan test #47) | **YES** | `test_ast_commands.py:1600` |
| `TestOptionCContainmentSubprocess` class + `test_ast_parse_subprocess_when_file_in_tempdir_and_no_trusted_roots_then_rejected` (#55) + `test_ast_modify_subprocess_when_symlink_swapped_before_write_then_rejected_and_file_unchanged` (#59) | **YES** | `tests/integration/cli/test_ast_subprocess.py:514,517,595` |
| `test_layered_config_adapter.py` additions (#49–54, `ast.trusted_roots` precedence/env-key tests) | **YES (class of tests present)** | `grep` for `get_list_when_ast_trusted_roots\|env_to_config_key_when_ast_trusted_roots\|get_source_when_ast_trusted_roots` matched in `test_layered_config_adapter.py` |
| `test_project_root.py::TestGetContainmentRoots` rewritten tests (#20–29) | **YES (class of tests present)** | `grep` for `get_containment_roots_when_no_explicit_root_then_never_includes\|get_containment_roots_when_configured_root_is_broad_then_warns\|load_trusted_roots_when` matched in `test_project_root.py` |

**What was NOT independently verified in this pass:** exact aggregate test counts against the plan's
literal numbering (1–60), pass/fail status of the full suite, and the actual H-21 (≥90% line)
coverage percentage. This agent session had **no Bash tool** available and could not run
`uv run pytest ... --cov=...` as the deliverable's own verification command (plan Section 6)
specifies. All test-presence evidence above is structural (file reads + `grep`), not execution
results.

**Verdict: PARTIALLY VERIFIED.** Every specifically-named test this pass checked for is present in
the expected location with matching intent (docstrings and assertions match the plan's stated
scenario). No contradicting evidence was found — nothing suggests the coverage/test-count claims
are false. However, "PASS" cannot be issued for the quantitative coverage-percentage claim, because
it was not independently executed. See [Discrepancy B](#discrepancies-severity-classified) (process
gap, not a code defect).

---

## Claim 4 — No Temp Path Feeds the Allowed Set (VERIFIED)

**Claim, quoted:** *"`tempfile.gettempdir()` and `_HARDCODED_TMP`/`/tmp` are removed from the
default set entirely"* (plan L307/C5 row); *"No env, filesystem, or config access anywhere in
[`containment_policy.py`]"* (plan L120).

**Evidence:**
- `grep` for `_check_temp_root_ownership|geteuid|st_uid|_HARDCODED_TMP` across `project_root.py`
  and `containment_policy.py`: **zero matches** in either file.
- `project_root.py` imports: `os`, `sys`, `pathlib.Path`, `typing.Any`, and the local
  `containment_policy` module — **no `tempfile` import at all** (confirmed by direct read of the
  full import block, `project_root.py:30-37`).
- `containment_policy.py` imports: `collections.abc.Sequence`, `dataclasses.dataclass`,
  `pathlib.Path/PurePath`, `typing.Literal` only — zero env, filesystem, or config access, matching
  the "pure" claim verbatim.
- `ast_commands.py` **does** import `tempfile` (`ast_commands.py:36`), but exclusively for
  `tempfile.mkstemp(dir=str(target_path.parent), ...)` at line 644 — atomic-write staging **inside
  the already-validated containment root**, not a containment-root source. This is a distinct,
  legitimate use unrelated to the removed default-widening mechanism; the plan's own text
  acknowledges this staging use is retained (Section 4.C test #44's docstring references `os.replace`
  atomicity, unaffected by this claim).
- Default containment set with no `ast.trusted_roots` configured is exactly
  `[project_root as "project"]` per `resolve_allowed_roots()` (`containment_policy.py:152-159`,
  called via `get_containment_roots()` → `resolve_allowed_roots(project_root, trusted_resolved, None)`
  at `project_root.py:212`, with `trusted_resolved = []` when `_load_trusted_roots()` returns `[]`).

**Verdict: VERIFIED.** No code path derives a containment root from `tempfile.gettempdir()`,
`TMPDIR`/`TEMP`/`TMP`, or a hardcoded `/tmp` constant anywhere in the current containment decision
path. The claim holds without qualification.

---

## Claim 5 — DD-1..DD-4 Implemented as Described (VERIFIED; exceeds plan on DD-4)

| DD | Plan's recommendation | Verdict | Evidence |
|---|---|---|---|
| DD-1 | Extend R-3 broad-root warning to `configured` roots (symmetry with `--root`) | **VERIFIED** | `project_root.py:223-242` — the `for root in roots:` warning loop branches on `root.classification == "explicit"` (existing R-3 wording) **and** `root.classification == "configured"` (new DD-1 wording: `"...ast.trusted_roots) is an unusually broad containment root..."`), both gated only on `root.is_broad`, both suppressed by `quiet=True`. |
| DD-2 | Remove `_check_temp_root_ownership` entirely (recommended default) | **VERIFIED** | Confirmed absent by grep (see Claim 4); removal-guard regression test present (`TestOwnershipGateRemoved`, `test_ast_commands.py:1781+`). |
| DD-3 | `ast_modify`'s internal write-time recheck always passes `quiet=True`, independent of the caller's `--quiet` | **VERIFIED** | `ast_commands.py:635`: `_check_path_containment(file_path, root, quiet=True)` — hardcoded literal `True`, not the function's own `quiet` parameter. Confirmed behaviorally-intended by dedicated test `test_ast_modify_when_configured_root_match_then_transparency_note_prints_exactly_once` (`test_ast_commands.py:1600`), which asserts `captured.err.count("configured trusted root") == 1` (not 2). |
| DD-4 | Refactor `adapter.py::_create_config_adapter()` to call the shared `build_layered_config_adapter()` factory ("non-blocking, optional fast-follow," plan L502) | **VERIFIED — exceeds plan framing** | `adapter.py:999-1041` (`_create_config_adapter`) **already** delegates to `project_root.build_layered_config_adapter()` (`adapter.py:1024-1026`), not a duplicated `LayeredConfigAdapter(...)` construction. The method's own docstring (`adapter.py:1002-1007`) states this was done. The plan explicitly frames DD-4 as a non-blocking, optional fast-follow "not required for BUG-010 to close" (plan L502) — the shipped code has already implemented it, which is a **positive** discrepancy (deliverable undersells completed scope), not a defect. |

**Verdict: VERIFIED.** All four design decisions are implemented exactly as their respective
recommendations describe, with DD-4 implemented in full despite the plan explicitly marking it
optional/non-blocking.

---

## Discrepancies (Severity-Classified)

### Discrepancy A — MAJOR: C2 write-time check validates a different resolution than the one used for the write

- **Claim contradicted:** "read-time and write-time containment are literally the same function
  call" / "closing the TOCTOU gap" (`eng-lead-option-c-plan.md` L39, L194-197).
- **Location:** `src/interface/cli/ast_commands.py:620` (`target_path` capture, independent
  `Path.resolve()` call) vs. `:635` (`_check_path_containment`'s own internal, independent
  `Path.resolve()` call at `:248`, whose result is discarded via `_,`) vs. `:654` (`os.replace`
  writes to `target_path` from line 620, not to any value produced by the check at line 635).
- **Nature:** Structural/design gap (CWE-367-shaped: check and use are two separate resolutions of
  the same live path, not a single shared, reused value). The specific double-swap exploit shape
  (retarget out-of-bounds before `target_path` capture, retarget back in-bounds before the check
  runs) is not covered by the deliverable's own TDD list (test #45) nor by `red-vuln`'s AC-2 PoC,
  both of which test only the simpler single-swap-and-stay-swapped shape.
- **Severity rationale:** Not CRITICAL — exploitation requires winning a race across two
  back-to-back `Path.resolve()` calls with no intervening I/O yield at the Python level (a very
  tight window), and this pass did not construct or run a live PoC to confirm actual exploitability
  (no Bash tool in this session). Not MINOR — the underlying design defect is real and
  independently verifiable from source alone (the check's resolved value is provably discarded and
  never reused for the write), and it directly contradicts the deliverable's strongest specific
  security claim about this exact code path.
- **Recommended action:** Either (a) have `_check_path_containment` return its resolved path and
  have `ast_modify` use *that* value (not a separately-captured `target_path`) for the
  `tempfile.mkstemp`/`os.replace` calls, closing the gap between "checked" and "used" entirely; or
  (b) add a monkeypatched-`Path.resolve`-call-counter regression test proving `target_path` and the
  write-time check's internal resolution are backed by the same single resolution, not two
  independent ones; or (c) construct a live race PoC (concurrent process/thread toggling the
  symlink around the line-620/line-635 window) to determine actual exploitability before deciding
  whether (a) is required or the residual risk is acceptable as documented.

### Discrepancy B — MINOR: Coverage/test-count claims not independently executed in this pass

- **Claim contradicted:** None directly (no evidence found that Section 4/6's coverage claims are
  false) — this is a **verification-completeness** gap, not a factual falsification.
- **Nature:** Process/tooling limitation. This agent session had no Bash tool available, so
  `uv run pytest ... --cov=...` (the deliverable's own stated verification command, plan Section 6)
  could not be run. All test-presence evidence in [Claim 3](#claim-3--coverage--test-count-claims-partially-verified)
  is structural (file reads + grep), confirming named tests exist with matching intent, but not
  confirming they pass or that the H-21 ≥90% line-coverage threshold is actually met.
- **Severity rationale:** MINOR — no contradicting evidence surfaced; this is a disclosed gap in
  *this verification pass's* coverage, not a defect in the deliverable itself.
- **Recommended action:** A separate pass (or the owner directly) should run
  `uv run pytest tests/unit/interface/cli/ tests/unit/infrastructure/adapters/configuration/ tests/integration/cli/test_ast_subprocess.py --cov=src/interface/cli --cov=src/infrastructure/adapters/configuration --cov-report=term-missing`
  and confirm (1) 100% pass, (2) ≥90% line coverage on the changed modules, before treating H-21 as
  satisfied.

---

## Verification Method Disclosure

Per P-001 (truth/accuracy) and P-022 (no deception): this pass consisted of direct `Read` of the
full text of `containment_policy.py`, `project_root.py`, `ast_commands.py`, `adapter.py`, and
targeted regions of `parser.py`/`main.py`, plus their corresponding test files, cross-referenced
against every literal claim quoted above. `Grep` was used to confirm absence of removed symbols
(`_check_temp_root_ownership`, `_HARDCODED_TMP`, etc.) and presence of specifically-named tests.
**No Bash tool was available in this agent session** (the adv-executor agent's declared toolset for
this invocation was Read/Write/Edit/Glob/Grep/WebSearch/WebFetch only) — the task instructions'
suggestion to run `uv run pytest`/`uv run python` for behavioral verification could not be acted on.
Every verdict above is therefore a **static source-trace verification**, not a live execution
result; Discrepancy A in particular is a structural finding (provable from source alone: the
check's resolved value is discarded and never reused for the write) rather than a confirmed live
race-win, and is flagged as such rather than overstated as a proven exploit.

---

*S-011 Chain-of-Verification execution — BUG-010 Option C, blind pass, Group 4 (Verify). Persisted
per P-002 at
`projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/adv-s011-chain-of-verification-optionc.md`.*
