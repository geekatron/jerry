# Chain-of-Verification Report: BUG-010 `jerry ast` Containment Scope Widening (PR #341)

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `src/interface/cli/{project_root,ast_commands,parser,main}.py` +
`tests/unit/interface/cli/{test_project_root,test_ast_commands}.py`, branch
`fix/BUG-010-ast-project-root`
**Criticality:** C4 (tournament, Group D)
**Date:** 2026-08-07
**Reviewer:** adv-executor (blind, isolated execution)
**H-16 Compliance:** Not confirmed applied for this execution (no S-003 Steelman output
supplied in context). CoVe proceeds per H-16 indirect status (S-011 is verification-
oriented, not critique-oriented) -- gap noted per protocol Step 1.
**Claims Extracted:** 11 | **Verified:** 7 | **Discrepancies:** 4 (0 Critical, 1 Major, 3 Minor)

---

## Summary

Extracted 11 testable claims from code comments, docstrings, the BUG-010 entity, the
eng-lead implementation plan, and the red-vuln findings report, then independently
verified each against the actual implementation. 7 of 11 claims are fully SUPPORTED by
direct code inspection (read/write root agreement, M-08/M-10 multi-root enforcement,
`--root` exclusivity, R-4 transparency-note scoping, root de-duplication, A-07 traversal
rejection, and the "temp/project/explicit" R-4 gating logic). Independent end-to-end
tracing of the assumption chain (per the assigned LENS: "cwd resolving inside a temp
tree") surfaced **one Major, previously undocumented discrepancy**: the H-01 ownership
gate and R-4 transparency note both key off `matched_root != allowed_roots[0]`, but
`allowed_roots[0]` (the "project root") is derived from unvalidated `Path.cwd()` --
if a user or CI runner invokes `jerry ast` from inside a shared/world-writable temp
directory without `CLAUDE_PROJECT_DIR` set, that directory is treated as the trusted
"project root" and silently exempted from both the ownership check and the transparency
note, reopening the exact CWE-552/668/281 exposure class the H-01 remediation was built
to close. Three Minor discrepancies (two documentation-drift items, one imprecise
error-handling claim) were also found. **Recommendation: REVISE** -- the Major finding
(CV-001) should be triaged before this increment is considered closed; the Minor
findings are documentation-quality items that do not block merge.

---

## Findings Table

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| CV-001-20260807T1500 | "H-01 ownership gate ... scoped exclusively to temp-default-root matches; the project root and an explicit `--root` remain pure user-discretion" | `ast_commands.py` `_check_temp_root_ownership` docstring; red-vuln-findings.md H-01 remediation | `allowed_roots[0]` (the "project root") is unvalidated `Path.cwd()`; when cwd resolves inside a shared/world-writable temp tree, files under it match index 0 first and bypass BOTH the ownership gate and the R-4 note -- the "project root" assumption of user-discretion is not enforced anywhere in code | **Major** | Internal Consistency, Methodological Rigor |
| CV-002-20260807T1500 | "When the resolved `--root` is unusually broad (a filesystem/drive root, or the user's home directory), a single-line, non-fatal WARNING is printed" | `project_root.py` `get_containment_roots` docstring | Omits the ancestor-of-home case (`/home`, `/Users`, `C:\Users`) that `_is_broad_containment_root` (which this function calls) actually implements per the H-02/H-08 remediation -- doc summary is stale relative to the function it summarizes | Minor | Traceability |
| CV-003-20260807T1500 | Ownership-check stat() failure "fails open ... consistent with the size check later in `_check_path_containment`, which applies its own handling" | `ast_commands.py` `_check_temp_root_ownership` docstring | The two `stat()` calls diverge in failure semantics: the ownership check literally fails **open** (`except OSError: pass` -> allows) while the size check literally fails **closed** (`except OSError as exc: return None, f"Cannot stat file: {exc}"` -> rejects) on the same error class; "consistent" implies matching behavior where the behaviors are opposite (net outcome converges only because the size check happens to run afterward on the same file) | Minor | Evidence Quality |
| CV-004-20260807T1500 | "Full test suite green with >= 90% coverage (H-20b)" | BUG-010-ast-project-root.md Acceptance Criteria (unchecked `- [ ]`) | No coverage percentage is cited anywhere in the deliverable set (BUG-010.md, eng-lead-implementation-plan.md, red-vuln-findings.md) -- only test **pass counts** (149/149, 371/371, 136/136 at three different points in time) are reported; the compound AC checkbox remains unchecked despite History entries describing the work as functionally complete | Minor (UNVERIFIABLE) | Traceability, Completeness |

**Finding ID Format:** `CV-{NNN}-20260807T1500` (execution session identifier).

---

## Claim-by-Claim Verification Table

| CL | Claim (paraphrased) | Source | VQ | Independent Verification | Result |
|----|----------------------|--------|----|---------------------------|--------|
| CL-001 | Read and write-time TOCTOU recheck never disagree on the allowed containment set within one `ast_modify` invocation | `ast_commands.py` `ast_modify` docstring L649-653 | What value does `get_containment_roots()` receive at the read call (`_read_file`, L659) vs. the write recheck (L679)? | Both sites call with the identical `root` parameter: read via `_read_file(file_path, root)` -> `_check_path_containment(file_path, root)` -> `get_containment_roots(root)` (L322); write via `allowed_roots = get_containment_roots(root)` (L679) directly. Same input, same deterministic function, no intervening state mutation between the two calls within one process invocation. | **VERIFIED** |
| CL-002 | Ownership-check `stat()` failure handling is "consistent with the size check" | `ast_commands.py` L272-287 vs L355-365 | Do both `stat()` OSError branches produce the same allow/reject outcome? | Ownership check (L285-286): `except OSError: pass` -> returns `None` (no error, **allowed**). Size check (L364-365): `except OSError as exc: return None, f"Cannot stat file: {exc}"` -> **rejected**. Opposite fail-open/fail-closed semantics on the same error class. | **MINOR DISCREPANCY** (CV-003) |
| CL-003 | M-08 (path escape) and M-10 (symlink escape) checks apply against the full multi-root allowed set, not just a single root | `ast_commands.py` L334 (`next((r for r in allowed_roots if ...` ) and L352 (`any(realpath.is_relative_to(r) for r in allowed_roots)`) | Does the escape check enumerate `allowed_roots`, or a single legacy `repo_root`? | Both L334 and L352 iterate `allowed_roots` (the full multi-root list from `get_containment_roots`), not the retired single-root `_get_repo_root()`. Confirmed no residual single-root containment path exists. | **VERIFIED** |
| CL-004 | `tests/security/test_adversarial_parsers.py::TestA07PathTraversal::test_path_traversal_blocked` still rejects `../../etc/passwd` under the widened default roots | eng-lead-implementation-plan.md T-7; BUG-010.md History (2026-08-07 entry: "`TestA07PathTraversal` re-confirmed green") | Does `_read_file("../../etc/passwd")` with no `--root` and no containment-disabling fixture resolve outside the project root, `tempfile.gettempdir()`, and `/tmp`? | Static trace: test file has no `_disable_path_containment` autouse fixture (that fixture is scoped to `test_ast_commands.py` only, confirmed by its `@pytest.fixture(autouse=True)` decorator living in that file). `_ENFORCE_PATH_CONTAINMENT` therefore reflects the real environment (`JERRY_DISABLE_PATH_CONTAINMENT` unset under normal `pytest` invocation). Under `uv run pytest` from repo root, `Path("../../etc/passwd").resolve()` lands two levels above the repo root -- outside the repo, outside `tempfile.gettempdir()`, outside `/tmp`. `matched_root` resolves to `None` -> rejected, `exit_code == 2`. Cross-corroborated by red-vuln-findings.md H-07 (executed, confirmed passing as part of a 136-test run) and BUG-010.md History (149/149, 371/371 pass counts). I did not execute pytest myself (no Bash tool available to this agent) -- this is a static-trace verification corroborated by a secondary source, not a first-party execution. | **VERIFIED** (static trace + corroborated, not independently executed) |
| CL-005 | `--root` is an exclusive override -- never additive with the project root or tempdir defaults | `project_root.py` `get_containment_roots` docstring; `parser.py` `_add_root_argument` help text | Does `get_containment_roots(explicit_root)` return anything beyond `[resolved_root]`? | L159-169: `if explicit_root is not None: ... return [resolved_root]` -- single-entry return, no project root or tempdir appended, confirmed by `test_get_containment_roots_when_explicit_root_given_then_excludes_project_root_and_tempdir` and `test_containment_when_explicit_root_given_then_file_in_project_root_rejected` (project-root file explicitly rejected when an unrelated `--root` is supplied). | **VERIFIED** |
| CL-006 | The R-4 transparency note fires only for a temp-default-root match, never for a project-root match or an explicit `--root` match | `ast_commands.py` `_warn_if_temp_root_match`/`_is_temp_default_root_match` docstrings | Does `_is_temp_default_root_match` return `False` for both the project-root and explicit-`--root` cases? | `_is_temp_default_root_match` (L181-209): `if explicit_root is not None: return False` (explicit root never notes); `return matched_root != allowed_roots[0]` (project root is always index 0 of the default set per L171, so a project-root match returns `False`). Confirmed by three dedicated tests: `test_check_path_containment_when_matched_via_temp_root_then_prints_transparency_note`, `..._project_root_then_no_transparency_note`, `..._explicit_root_given_then_no_transparency_note`. | **VERIFIED** |
| CL-007 | Coverage on changed files is >= 90% | BUG-010.md Acceptance Criteria | Is a coverage percentage reported anywhere in the deliverable set? | Grepped BUG-010.md, eng-lead-implementation-plan.md, red-vuln-findings.md for coverage evidence: only test **pass counts** appear (136/136 pre-remediation baseline per red-vuln; 149/149 and 371/371 post-remediation per BUG-010.md History). No `pytest --cov` output, percentage, or coverage report is cited. The AC checkbox itself remains `- [ ]` unchecked. I have no Bash tool access in this agent role and cannot execute `pytest --cov` myself to verify directly. | **UNVERIFIABLE** (CV-004) |
| CL-008 | H-01 ownership gate + R-4 note assumption: "the project root ... remain[s] pure user-discretion" (i.e., inherently trusted, never requiring the ownership gate) | `ast_commands.py` `_check_temp_root_ownership` docstring; red-vuln-findings.md H-01 remediation code sketch comment (`# ... never to the project root, never to an explicit --root -- both remain pure user-discretion as today`) | Does `get_project_root()` validate that `Path.cwd()` (its fallback when `CLAUDE_PROJECT_DIR` is unset) is not itself inside a shared/world-writable temp tree? | `project_root.py` L46-60: `get_project_root()` returns `Path(project_dir)` (unvalidated) or bare `Path.cwd()` -- zero validation of any kind, no broad-root check (unlike `--root`'s R-3 `_is_broad_containment_root` check, which the project-root path never invokes). Traced end-to-end: `get_containment_roots()` places `get_project_root().resolve()` at index 0 of `allowed_roots` (L171) unconditionally. `_check_path_containment`'s `matched_root = next((r for r in allowed_roots if resolved.is_relative_to(r)), None)` (L334) returns the **first** matching root in list order -- if cwd is `/tmp/scratch-project` (no `CLAUDE_PROJECT_DIR` set, e.g. a CI runner whose workspace lives under `/tmp`, or a user who `cd`'d into a scratch directory before running `jerry ast`), a file at `/tmp/scratch-project/foo.md` matches `allowed_roots[0]` (the "project root") **before** the tempdir/`/tmp` entries are even considered, even though `/tmp/scratch-project` is physically inside the same shared, world-writable filesystem tree the H-01 fix targets. `_is_temp_default_root_match(matched_root, allowed_roots, explicit_root)` then returns `False` (`matched_root == allowed_roots[0]`), so **both** the H-01 ownership gate (`_check_temp_root_ownership`) and the R-4 transparency note are skipped entirely. No test in `test_project_root.py` or `test_ast_commands.py` exercises "project root resolves inside a shared temp directory" as a scenario -- this path is untested and unmitigated. | **MATERIAL DISCREPANCY** (CV-001) |
| CL-009 | `_is_broad_containment_root` widening (H-02/H-08 remediation) is fully summarized in `get_containment_roots`'s own docstring | `project_root.py` `get_containment_roots` docstring L130-135 vs `_is_broad_containment_root` docstring L63-117 | Does `get_containment_roots`'s docstring text match the actual scope of the check it invokes? | `get_containment_roots` docstring: "unusually broad (a filesystem/drive root, or the user's home directory)" -- two cases only. `_is_broad_containment_root`'s own docstring and implementation (L96-117) additionally flag any **ancestor of** home (`/home`, `/Users`, `C:\Users`) via `home.relative_to(resolved)`. The summary in the caller's docstring under-describes the callee's actual behavior. | **MINOR DISCREPANCY** (CV-002) |
| CL-010 | The default allowed-roots list is de-duplicated while preserving order (project root always first) | `project_root.py` `get_containment_roots` docstring/comment L175-177 | Does `list(dict.fromkeys(roots))` preserve first-occurrence order, and is the project root always first? | `roots: list[Path] = [get_project_root().resolve(), Path(tempfile.gettempdir()).resolve()]` -- project root literally constructed as element 0. `dict.fromkeys()` preserves first-occurrence insertion order in Python 3.7+, so project root remains index 0 post-dedup unless it were itself a later duplicate of an earlier entry, which is structurally impossible (it IS the first entry). Confirmed by `test_get_containment_roots_when_gettempdir_equals_hardcoded_tmp_then_deduplicated`. | **VERIFIED** |
| CL-011 | M-10 secondary symlink check (`resolved != realpath`) is effectively defense-in-depth, not the primary line of defense, since `Path.resolve()` already follows symlinks | `ast_commands.py` L349-353 comment "Check symlink resolution matches (M-10)"; red-vuln-findings.md H-03 finding | Does `Path(file_path).resolve()` (L326, producing `resolved`) already follow symlinks to the same canonical target as `os.path.realpath()` (L331, producing `realpath`) on POSIX, making the `resolved != realpath` branch rarely/never true in practice? | Cross-referenced against red-vuln-findings.md H-03, which independently confirmed via executed reproduction that a symlink escape is "rejected at the **primary** `resolved = Path(file_path).resolve()` check, before the secondary M-10 check ever runs" -- because `Path.resolve()` already follows symlinks to their canonical target, `matched_root` is computed against the *target*, not the symlink's own location. This CoVe pass's independent static trace agrees with red-vuln's executed finding: no contradiction found. Not raised as a new finding since it is already documented (as an accepted defense-in-depth observation, not a defect) in the upstream red-team report. | **VERIFIED** (cross-source consistency confirmed, no new finding) |

---

## Finding Details

### CV-001: Project-root fallback bypasses the H-01 ownership gate and R-4 transparency note when cwd resolves inside a shared temp tree [MAJOR]

**Claim (from deliverable):** `_check_temp_root_ownership`'s docstring and the red-vuln
remediation both assert the ownership gate is "scoped exclusively to temp-default-root
matches; the project root and an explicit `--root` remain pure user-discretion ... and
are never gated here" -- implying the project root is inherently a deliberate, trusted
location that does not need the same scrutiny as the temp-default fallback roots.

**Source Document:** `src/interface/cli/ast_commands.py` (`_check_temp_root_ownership`
docstring, `_is_temp_default_root_match`); `src/interface/cli/project_root.py`
(`get_project_root`, `get_containment_roots`); `red-vuln-findings.md` H-01 remediation
code comment.

**Independent Verification:** `get_project_root()` performs **zero validation** on its
`Path.cwd()` fallback (`project_root.py` L46-60). `get_containment_roots()` places this
unvalidated value at `allowed_roots[0]` unconditionally (L171). `_check_path_containment`'s
`matched_root = next((r for r in allowed_roots if resolved.is_relative_to(r)), None)`
(L334) evaluates roots **in list order** and returns the first match. `_is_temp_default_root_match`
(L181-209) treats any match against `allowed_roots[0]` as "not a temp match" regardless
of what that root actually resolves to.

**Discrepancy:** If `CLAUDE_PROJECT_DIR` is unset and the invoking process's cwd is
itself inside a shared/world-writable temp directory (e.g., a CI runner whose workspace
is provisioned under `/tmp`, a container with an ephemeral tmpfs root, or a user who
`cd`'d into a scratch directory before invoking `jerry ast` without realizing it), that
directory is treated as the fully-trusted "project root" -- exempt from the H-01
ownership check (`resolved.stat().st_uid != os.geteuid()`) and exempt from the R-4
transparency note -- even though it is physically indistinguishable from the exact
`tempfile.gettempdir()`/`/tmp` locations the H-01 remediation was built to gate. This
reopens the same CWE-552 (Files Accessible to External Parties) / CWE-668 (Exposure of
Resource to Wrong Sphere) / CWE-281 (Improper Preservation of Permissions) exposure
class red-vuln confirmed and eng-backend closed for the *explicit* temp-root-match case,
via a code path (`get_project_root()`'s unvalidated cwd fallback) that neither the
eng-lead implementation plan nor the red-vuln assessment's Rules of Engagement
considered in scope.

**Severity:** Major -- undermines a stated security invariant ("project root remains
pure user-discretion") that is not actually enforced in code, is reachable under
realistic operating conditions (CI runners, sandboxed/ephemeral workspaces, careless
manual invocation) without any `--root` flag or environment-variable bypass, and is
untested by the existing suite (no test in `test_project_root.py` or
`test_ast_commands.py` constructs a cwd-inside-shared-temp scenario). Not rated Critical
because it requires an unusual (though plausible) deployment/invocation condition rather
than being reachable from Jerry's stated dominant deployment model (single-developer
laptop with a stable project directory).

**Dimension:** Internal Consistency (the "project root is always trusted" invariant
stated in code comments is contradicted by the actual validation-free resolution logic),
Methodological Rigor (the red-vuln RoE and eng-lead plan's threat model did not consider
this path).

**Correction:** Either (a) apply the same `_is_broad_containment_root`-style check to
the resolved project root itself (warn, and/or apply the H-01 ownership gate) when
`get_project_root()` resolves inside a known temp-default root
(`tempfile.gettempdir()`/`_HARDCODED_TMP`), or (b) explicitly document this as an
accepted residual risk (consistent with the project's existing pattern of documenting
accepted risks such as R-1/R-5/R-7 in the eng-lead plan) rather than asserting the
project root is unconditionally "pure user-discretion." Recommend routing back to the
PR owner for an explicit risk-acceptance decision, following the same pattern already
used for R-3/R-4 in the eng-lead plan.

---

### CV-002: `get_containment_roots` docstring under-describes the actual broad-root warning scope [MINOR]

**Claim (from deliverable):** "When the resolved `--root` is unusually broad (a
filesystem/drive root, or the user's home directory), a single-line, non-fatal WARNING
is printed to stderr" (`project_root.py` `get_containment_roots` docstring, L130-135).

**Source Document:** `src/interface/cli/project_root.py`, `_is_broad_containment_root`
docstring (L63-117) and implementation (L96-117).

**Independent Verification:** `_is_broad_containment_root` -- the function
`get_containment_roots` actually calls to decide whether to warn -- also flags any
**ancestor of** the resolved home directory (e.g., `/home`, `/Users`, `C:\Users`, or
`$HOME`'s parent), per the H-02/H-08 red-team remediation, via `home.relative_to(resolved)`.

**Discrepancy:** The caller-level docstring in `get_containment_roots` only mentions two
cases (exact filesystem/drive root, exact home directory) and omits the ancestor-of-home
case that is, per red-vuln's own findings, one of the two CONFIRMED remediations in this
increment. A reader relying solely on `get_containment_roots`'s docstring (without also
reading `_is_broad_containment_root`'s docstring) would underestimate the warning's
actual coverage.

**Severity:** Minor -- documentation completeness/drift only; the underlying behavior is
correct and more protective than the summary describes (no under-protection, only
under-documentation).

**Dimension:** Traceability.

**Correction:** Update `get_containment_roots`'s docstring line "(a filesystem/drive
root, or the user's home directory)" to "(a filesystem/drive root, the user's home
directory, or an ancestor of the home directory such as `/home`, `/Users`, or
`C:\Users`)" to match `_is_broad_containment_root`'s actual scope.

---

### CV-003: "Consistent with the size check" docstring claim conflates fail-open and fail-closed semantics [MINOR]

**Claim (from deliverable):** `_check_temp_root_ownership`'s docstring states the
ownership check "fails open on OSError, consistent with the size check later in
`_check_path_containment`, which applies its own handling" (`ast_commands.py`, Returns
section).

**Source Document:** `src/interface/cli/ast_commands.py` L272-287 (`_check_temp_root_ownership`)
and L355-365 (M-05 size check).

**Independent Verification:** The two `stat()` calls have opposite OSError semantics:
`_check_temp_root_ownership` (L283-286): `except OSError: pass` -> returns `None`
(**allows**). The size check (L363-365): `except OSError as exc: return None, f"Cannot
stat file: {exc}"` -> (**rejects**).

**Discrepancy:** "Consistent with" reads as "behaves the same as," but the two checks'
individual failure semantics are opposite (fail-open vs. fail-closed) on the identical
error class (`OSError` from `stat()`). The net practical outcome does converge in most
cases -- if the ownership check's `stat()` fails because the file genuinely cannot be
stat'd, the size check's own subsequent `stat()` call on the same file will typically
also fail and correctly reject -- but the docstring's wording implies matching per-check
behavior rather than a converging net outcome via a downstream check.

**Severity:** Minor -- no behavioral defect found (the net-effect reasoning holds); this
is a documentation-clarity finding that could mislead a future maintainer into assuming
both checks share identical error-handling semantics.

**Dimension:** Evidence Quality.

**Correction:** Reword to: "fails open on OSError (unlike the size check below, which
fails closed on its own OSError) -- the size check's independent stat() call on the same
path typically produces an equivalent net rejection when the file genuinely cannot be
stat'd."

---

## Recommendations

**Major (SHOULD correct before acceptance):**
- CV-001-20260807T1500: Route the cwd-inside-shared-temp gap back to the PR owner/user
  for an explicit risk-acceptance decision (mirroring the R-3/R-4 pattern already used
  in this increment), or implement the broad-root-style check against the resolved
  project root itself.

**Minor (MAY correct):**
- CV-002-20260807T1500: Update `get_containment_roots`'s docstring to mention the
  ancestor-of-home case.
- CV-003-20260807T1500: Reword `_check_temp_root_ownership`'s "consistent with the size
  check" language to describe the actual fail-open/fail-closed divergence.
- CV-004-20260807T1500: Either run and cite an actual `pytest --cov` percentage against
  `project_root.py`/`ast_commands.py`, or check off the AC box with the pass-count
  evidence already in hand and note coverage was not independently measured in this
  execution.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | CV-004: coverage AC unverified/unchecked despite otherwise-complete work |
| Internal Consistency | 0.20 | Negative | CV-001: "project root is pure user-discretion" invariant is asserted in code comments but not enforced by any check |
| Methodological Rigor | 0.20 | Negative | CV-001: red-vuln's RoE/threat model did not consider the cwd-inside-temp path; untested by the existing suite |
| Evidence Quality | 0.15 | Negative | CV-003: docstring claim conflates two opposite failure semantics |
| Actionability | 0.15 | Neutral | All findings include specific, mechanically-applicable corrections |
| Traceability | 0.10 | Negative | CV-002: caller docstring under-describes callee's actual (correct) broader scope |

---

## Execution Statistics

- **Total Findings:** 4
- **Critical:** 0
- **Major:** 1 (CV-001)
- **Minor:** 3 (CV-002, CV-003, CV-004)
- **Claims Extracted:** 11
- **Verified:** 7 (CL-001, CL-003, CL-004, CL-005, CL-006, CL-010, CL-011)
- **Discrepancies:** 4 (1 material/CL-008 -> CV-001; 2 minor documentation drift/CL-002, CL-009 -> CV-003, CV-002; 1 unverifiable/CL-007 -> CV-004)
- **Protocol Steps Completed:** 5 of 5

---

*Note on execution constraints: This adv-executor invocation has no Bash tool access
(per its T2 tool tier) and therefore could not execute `pytest`/`pytest --cov` directly.
Claims requiring test execution (CL-004, CL-007) were verified via static code trace and
cross-referenced against the corroborating evidence already present in
`red-vuln-findings.md` and `BUG-010-ast-project-root.md`, and are flagged accordingly
(VERIFIED-by-trace vs. UNVERIFIABLE) rather than falsely represented as first-party
executed verification, per P-022.*

---

## Note on Path Literals

This analysis discusses cross-platform filesystem path literals as code (not as
hardcoded developer-machine paths). The path forms referenced above:

```text
/home
/Users
C:\Users
C:\tmp
```

are Windows/POSIX root and home-ancestor examples evaluated by
`_is_broad_containment_root`, quoted here as literals under review.
