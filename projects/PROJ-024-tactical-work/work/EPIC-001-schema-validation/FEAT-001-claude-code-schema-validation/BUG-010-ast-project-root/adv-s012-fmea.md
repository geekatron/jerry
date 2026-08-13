# FMEA Report: BUG-010 `jerry ast` Path-Containment Widening (PR #341)

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `src/interface/cli/{project_root,ast_commands,parser,main}.py` (containment logic) on branch `fix/BUG-010-ast-project-root`, plus `BUG-010-ast-project-root.md`, `eng-lead-implementation-plan.md`, `red-vuln-findings.md`
**Criticality:** C4 (Critical) -- tournament mode, Group E
**Date:** 2026-08-07
**Reviewer:** adv-executor (blind, isolated from other Group A-D/F+ reviewers)
**H-16 Compliance:** Not independently verified by this execution -- this agent runs S-012 only, blind to sibling strategies per the tournament's isolation instruction; S-003 Steelman ordering is the tournament orchestrator's responsibility, not re-verified here (P-022 disclosure).
**Elements Analyzed:** 11 | **Failure Modes Identified:** 12 | **Total RPN:** 2157

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Element Inventory](#element-inventory) | Step 1 decomposition |
| [Findings Table](#findings-table) | RPN-ranked failure modes |
| [Finding Details -- Critical](#finding-details--critical) | Full detail: FM-001..FM-005 |
| [Finding Details -- Major](#finding-details--major) | Full detail: FM-006..FM-009 |
| [Finding Details -- Minor](#finding-details--minor) | Brief: FM-010..FM-012 |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Summary

11 elements of the containment subsystem were decomposed and analyzed; 12 distinct failure modes were identified, **5 Critical (RPN >= 200)**, **4 Major (RPN 80-199)**, **3 Minor (RPN < 80)**. The highest-RPN finding, **FM-001 (RPN 432)**, shows that the H-01 ownership gate red-vuln added specifically to close the multi-tenant `/tmp` gap (CWE-552/668/281) is **silently bypassed whenever the resolved project root itself sits inside a temp/scratchpad tree** -- a realistic scenario for Claude Code agent sessions whose cwd or `CLAUDE_PROJECT_DIR` is a scratchpad path -- because the ownership-gate scoping logic (`_is_temp_default_root_match`) trusts `allowed_roots[0]` by **array index**, not by verifying that index-0 is not itself a shared/temp location. 8 of 12 failure modes (67%) have RPN > 80, exceeding the template's 30% systemic-issue threshold -- **this containment subsystem has a systemic quality issue**, not isolated defects. **Recommendation: REVISE.** The widening's core design (project root + temp defaults + exclusive `--root` override) and red-vuln's own H-01/H-02 remediations are sound for the cases they examined; the gaps found here are boundary/interaction cases (index-based vs. location-based trust, write-path propagation of the ownership gate, environment-variable-controlled root expansion, container UID convergence) that the prior red-team pass did not examine, corroborated in one case (FM-002) by the project's own test suite inadvertently exercising the exact bypass condition while asserting it as intended behavior.

---

## Element Inventory

| ID | Element | Location |
|----|---------|----------|
| E1 | `get_project_root()` | `project_root.py:46-60` |
| E2 | `_is_broad_containment_root()` | `project_root.py:63-117` |
| E3 | `get_containment_roots()` | `project_root.py:120-177` |
| E4 | `_is_temp_default_root_match()` | `ast_commands.py:181-209` |
| E5 | `_warn_if_temp_root_match()` | `ast_commands.py:212-241` |
| E6 | `_check_temp_root_ownership()` | `ast_commands.py:244-287` |
| E7 | `_check_path_containment()` | `ast_commands.py:290-367` |
| E8 | `_read_file()` | `ast_commands.py:370-406` |
| E9 | `ast_modify` write-time TOCTOU recheck + atomic write | `ast_commands.py:637-724` (recheck: 677-682) |
| E10 | `--root` CLI threading (`_add_root_argument` + 10 subparsers) | `parser.py:569-770` |
| E11 | `_handle_ast` root pass-through | `main.py:393-459` |

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-20260807-E | E4 (+E1, E5) | Project root resolves *inside* a temp/scratchpad tree (cwd or `CLAUDE_PROJECT_DIR` under `/tmp`); index-based trust (`matched_root != allowed_roots[0]`) skips the H-01 ownership gate AND the R-4 transparency note | 9 | 6 | 8 | **432** | Critical | Replace index-based trust with location-based: verify `allowed_roots[0]` is not itself under a temp-default root before exempting it from the ownership gate | Internal Consistency |
| FM-004-20260807-E | E6 | Root-owned (UID 0) processes in shared-temp containers converge: `st_uid == geteuid() == 0` for every tenant, so the ownership gate passes for ANY file regardless of true owner | 8 | 5 | 9 | **360** | Critical | Add a `geteuid()==0` disclosure warning; document that the ownership gate provides no protection under root-uid convergence | Methodological Rigor |
| FM-002-20260807-E | E3 (+E4) | `CLAUDE_PROJECT_DIR` set to (or de-duplicating with) a temp-default root collapses into index-0 via `dict.fromkeys()` ordering, bypassing the ownership gate via misconfiguration rather than cwd | 9 | 4 | 8 | **288** | Critical | Same fix as FM-001 (shared root cause) | Internal Consistency |
| FM-003-20260807-E | E9 | `ast_modify` write-time TOCTOU recheck re-verifies containment (`is_relative_to`) but does **not** re-invoke `_check_temp_root_ownership`; an attacker-substituted file at the target path inside a shared temp root can be silently overwritten by `os.replace()` | 7 | 4 | 8 | **224** | Critical | Re-invoke the ownership gate inside the write-time recheck, mirroring the read-time gate exactly | Completeness |
| FM-005-20260807-E | E3 | `_is_broad_containment_root` is only applied to explicit `--root`; a poisoned `TMPDIR`/`TEMP`/`TMP` env var silently expands the default allowed-root set with **zero** broad-root warning, even if it resolves to `/` or `$HOME` | 8 | 3 | 9 | **216** | Critical | Apply the broad-root check to `tempfile.gettempdir()`'s resolved value in the default branch too | Methodological Rigor |
| FM-007-20260807-E | E6 | Ownership-check `stat()` fails **open** on `OSError`; the size-check `stat()` later in the same function fails **closed** on the same class of error -- inconsistent fail posture on a security gate | 7 | 3 | 7 | **147** | Major | Make the ownership `stat()` fail-closed for temp-default matches, consistent with the size check | Internal Consistency |
| FM-006-20260807-E | E3 | Unguarded `tempfile.gettempdir()` call can raise in minimal/read-only containers or hardened CI runners, crashing the whole `jerry ast` invocation with an unhandled traceback instead of a graceful exit 2 | 6 | 3 | 8 | **144** | Major | Wrap `tempfile.gettempdir()` in `try/except OSError`, degrade to project-root-only with a stderr note | Evidence Quality |
| FM-008-20260807-E | E7/E8 | Read-time TOCTOU: symlink swap at `resolved`'s path between `_check_path_containment`'s resolve and `_read_file`'s `read_text()` is not re-verified (red-vuln's H-05 covered only the write path) | 6 | 2 | 9 | **108** | Major | Re-resolve and re-verify `resolved` immediately before `read_text()`, mirroring the existing write-time recheck pattern | Methodological Rigor |
| FM-009-20260807-E | E7 | Two independent, non-atomic `.stat()` calls (ownership check + size check) on the same resolved path create a secondary TOCTOU window for file substitution between the two checks | 5 | 2 | 8 | **80** | Major | Combine both checks into a single reused `os.stat()` result | Methodological Rigor |
| FM-012-20260807-E | E2 | `_is_broad_containment_root` only flags ancestors of `Path.home()`; other well-known multi-tenant mount points (`/mnt`, `/data`, NFS shares) supplied via `--root` get no transparency warning | 2 | 4 | 7 | 56 | Minor | Document as accepted scope limit; optional future widening | Traceability |
| FM-010-20260807-E | E2 | `Path.home()` raising `RuntimeError`/`OSError` silently disables the ancestor-of-home broad-root check with no degraded-detection signal | 3 | 3 | 6 | 54 | Minor | Emit a one-line stderr note when `Path.home()` cannot be determined | Evidence Quality |
| FM-011-20260807-E | E2/E10 | `Path("/tmp")` under `PureWindowsPath` resolves to a current-drive-relative `\tmp`; if such a directory exists on a Windows host it is silently included, contradicting the module docstring's "will not exist" claim (red-vuln R-5, accepted) | 4 | 2 | 6 | 48 | Minor | Document explicitly; low priority per red-vuln's existing acceptance | Traceability |

**Finding ID Format:** `FM-{NNN}-{execution_id}`, `execution_id = 20260807-E` (Group E, tournament date).

**Decision-point flags (per protocol Step 3):** 1 finding at RPN >= 200 with Severity >= 9 triggers automatic Critical (FM-001, FM-002); 8/12 findings (67%) exceed RPN 80, well past the 30% systemic-issue threshold.

---

## Finding Details -- Critical

### FM-001-20260807-E: Project-root-inside-temp-tree bypasses the H-01 ownership gate

**Element:** `_is_temp_default_root_match()` (`ast_commands.py:181-209`), cascading from `get_project_root()` (E1) and consumed by `_warn_if_temp_root_match()` (E5) and `_check_path_containment()` (E7).

**Failure Mode:** `_is_temp_default_root_match` classifies a containment match as "project root, therefore trusted" purely by **array-index equality** -- `matched_root != allowed_roots[0]` -- never by verifying that `allowed_roots[0]` (the resolved project root) is not *itself* located under a temp-default root. When `CLAUDE_PROJECT_DIR` is unset and `cwd` sits inside `tempfile.gettempdir()` or `/tmp` (a realistic condition for a Claude Code agent session whose working directory is a scratchpad path, as this very engagement's scratchpad directory demonstrates: `/private/tmp/claude-502/.../scratchpad`), `get_project_root()` returns that temp-tree path, `get_containment_roots()` places it at index 0, and every file check against it is treated as a "project root match" -- **exempt from both the H-01 ownership gate and the R-4 transparency note** -- even though the underlying directory is exactly the shared/world-writable location those two controls exist to gate.

**Effect:** The specific security control red-vuln added to close CWE-552/668/281 (multi-tenant `/tmp` read/write with no ownership check) is silently inert whenever the project root itself is a temp path. The user receives no signal (neither the ownership rejection nor the "operating on a temp/scratchpad path" note fires) that they are effectively running with containment disabled against a shared location.

**S/O/D Rationale:** S=9 (fully defeats the specific control the fix was built to add, with double silence -- no rejection, no transparency). O=6 (plausible and not exotic: any session where cwd is a temp/scratchpad directory and `CLAUDE_PROJECT_DIR` is unset triggers it; Jerry's own scratchpad convention documented in this session's environment context is a live instance of this pattern). D=8 (no test in `test_ast_commands.py`/`test_project_root.py` constructs a project root that is itself inside a temp-default root -- confirmed by direct read of all `TestBug010ProjectRootContainment` test names).

**Corrective Action:** In `_is_temp_default_root_match`, additionally check whether `allowed_roots[0]` (when `explicit_root is None`) resolves under `tempfile.gettempdir()` or `_HARDCODED_TMP`; if so, treat matches against it identically to a temp-default match (subject to the ownership gate and R-4 note) rather than exempting it by index alone.

**Acceptance Criteria:** A new test constructs `CLAUDE_PROJECT_DIR` (or unset + `monkeypatch.chdir`) pointing *inside* a controlled temp-default root, places a foreign-UID-owned file there, and asserts rejection with the ownership-gate error message -- proving the gate now fires even for an "index-0" match.

**Post-Correction RPN Estimate:** S=9, O=2, D=5 -> 90 (Major; occurrence and detection both drop sharply once the semantic check and regression test exist).

---

### FM-004-20260807-E: Root-UID convergence defeats the ownership gate in shared containers

**Element:** `_check_temp_root_ownership()` (`ast_commands.py:244-287`).

**Failure Mode:** The H-01 remediation compares `resolved.stat().st_uid != os.geteuid()`. In a container running as UID 0 (a common default for unhardened Dockerfiles and many CI runner images), **every** process on the shared host has `geteuid() == 0`, and every file -- regardless of which tenant/container actually wrote it -- typically also has `st_uid == 0` when written by a root-run process. The comparison becomes `0 != 0` for all files, which is always `False`: the check passes unconditionally for every file in the shared temp directory, exactly the multi-tenant scenario H-01 was designed to gate.

**Effect:** In precisely the deployment class where the threat is most realistic -- containerized CI, Kubernetes pods sharing an `emptyDir`/hostPath temp volume, sibling root-run containers on one node -- the ownership check provides **zero** protection, with no warning that its protection has degraded to none.

**S/O/D Rationale:** S=8 (defeats the specific control in a realistic, common deployment class). O=5 (root-in-container is common but not universal; many hardened setups drop privileges). D=9 (no test simulates UID convergence; the check "passes" cleanly with no error, warning, or log of any kind -- fully undetectable without this analysis).

**Corrective Action:** Add a disclosure: when `os.geteuid() == 0` (POSIX) and a temp-default match occurs, emit a stderr advisory ("Warning: running as root; the temp-directory ownership check provides no protection under UID 0") extending the existing R-4 transparency pattern. True mitigation requires process-level isolation (non-root execution, per-tenant `--root`), which is outside this codebase's control and should be documented as an operational recommendation.

**Acceptance Criteria:** A test monkeypatches `os.geteuid` to `0` and asserts the new disclosure warning fires on a temp-root match; documentation (README or runbook) states the root-uid-convergence limitation explicitly.

**Post-Correction RPN Estimate:** S=8, O=5, D=4 -> 160 (remains Major -- occurrence is unchanged since the underlying deployment pattern is unaffected by a disclosure fix, but detection improves sharply).

---

### FM-002-20260807-E: `CLAUDE_PROJECT_DIR`/temp-root de-duplication collapses trust boundary

**Element:** `get_containment_roots()` (`project_root.py:120-177`), specifically the `dict.fromkeys(roots)` de-duplication step, in combination with E4's index-based trust check.

**Failure Mode:** If `CLAUDE_PROJECT_DIR` is explicitly (or accidentally, e.g. via a misconfigured devcontainer/CI environment) set to a path equal to or coinciding with the resolved `tempfile.gettempdir()`/`_HARDCODED_TMP` value, `dict.fromkeys()` preserves first-occurrence order, so the surviving single entry sits at index 0 -- structurally identical to FM-001's bypass, but triggered by explicit misconfiguration/env-var collision rather than an unset-env cwd condition. **This is independently corroborated by the project's own test suite**: `test_containment_when_project_root_file_and_foreign_uid_then_still_allowed` (`test_ast_commands.py:1594`) sets `user_root = tmp_path / "user-project"` **without** monkeypatching the temp-root seams (`_HARDCODED_TMP`, `tempfile.gettempdir`) that the adjacent tests in the same class deliberately apply -- meaning `user_root`, derived from pytest's `tmp_path`, is *itself* located under the real system temp directory in that test run. The test asserts `error is None` and labels this "the ownership gate is scoped strictly to temp-default-root matches ... a project-root match is unaffected" -- which is correct as a description of current behavior, but the test's own fixture inadvertently demonstrates that a project root sitting inside the temp tree is treated as exempt, without the test author flagging this as the security-relevant edge case it is.

**Effect:** Same as FM-001 (silent ownership-gate + transparency-note bypass), reached via a distinct trigger (env-var value collision rather than implicit cwd placement), and evidenced by an existing test that currently validates the exempt behavior as intentional rather than testing for the gap.

**S/O/D Rationale:** S=9 (same control defeat as FM-001). O=4 (requires an explicit or accidental `CLAUDE_PROJECT_DIR` misconfiguration rather than a passive cwd condition -- somewhat less likely than FM-001 but realistic in CI/devcontainer misconfiguration). D=8 (the existing test's fixture demonstrates the condition occurs in practice within the test suite itself, yet no test or code comment flags it as a security boundary concern).

**Corrective Action:** Same fix as FM-001 (shared root cause: replace index-based trust with location-based verification). Additionally, retitle/annotate `test_containment_when_project_root_file_and_foreign_uid_then_still_allowed`'s docstring to note the `tmp_path`-under-tempdir coincidence explicitly, or re-seam it with `_HARDCODED_TMP`/`gettempdir` monkeypatches like its sibling tests, to avoid future confusion about whether this is intended behavior or an untested gap.

**Post-Correction RPN Estimate:** S=9, O=2, D=5 -> 90 (shared remediation with FM-001).

---

### FM-003-20260807-E: Write-time TOCTOU recheck omits the ownership gate

**Element:** `ast_modify` write-time recheck (`ast_commands.py:677-682`).

**Failure Mode:** The write-time recheck added for TOCTOU mitigation (WI-020/M-21) re-derives `allowed_roots = get_containment_roots(root)` and checks only `any(target_path.is_relative_to(r) for r in allowed_roots)` -- it does **not** call `_is_temp_default_root_match` + `_check_temp_root_ownership` again. Direct comparison of the read-time path (`_check_path_containment`, which does invoke the ownership gate) against the write-time recheck block confirms the ownership predicate is absent from the latter. Between the read-time ownership check (which passed) and the write-time `os.replace()`, another tenant with write access to the same shared temp directory could substitute a file they own at the exact target path; the write-time recheck would confirm only "still under an allowed root" and proceed to atomically overwrite whatever now occupies that path, without a fresh ownership recheck catching the substitution.

**Effect:** The H-01 remediation was propagated to the read path (`_check_path_containment`, invoked once at the top of `ast_modify` via `_read_file`) but **not** to the pre-existing write-time TOCTOU recheck pattern that the fix's own design doc (eng-lead plan) explicitly says reuses "the same `root` param" -- the plan verified `root`-value consistency between read and write, but not ownership-check consistency, which is a narrower but real gap in H-01's propagation.

**S/O/D Rationale:** S=7 (enables clobbering another tenant's file in a shared temp directory without a fresh ownership recheck -- CWE-283-adjacent; write consequences are more severe than the read-only exposure H-01 primarily targeted). O=4 (requires the target file to already have passed the read-time ownership check as belonging to the current user, then be swapped by another tenant before the write completes -- a narrower race than FM-001/002 but structurally guaranteed to succeed once the timing is hit, since no ownership check exists at write time at all). D=8 (undetectable by any current test -- confirmed by code inspection that the write-time block structurally cannot invoke an ownership check it never calls).

**Corrective Action:** Re-invoke `_is_temp_default_root_match(matched_root, allowed_roots, root)` + `_check_temp_root_ownership(target_path, file_path)` inside the write-time recheck block, exactly mirroring the read-time gate, before proceeding to `mkstemp`/`os.replace`.

**Acceptance Criteria:** A test places a foreign-UID-owned file at the write target (post-read-check, pre-write) inside a controlled temp root and asserts `ast_modify` returns a rejection at write time, not just at read time.

**Post-Correction RPN Estimate:** S=7, O=1, D=4 -> 28.

---

### FM-005-20260807-E: `TMPDIR`/`TEMP`/`TMP` env-var poisoning silently expands the default root set

**Element:** `get_containment_roots()` (`project_root.py:120-177`), default (non-`explicit_root`) branch.

**Failure Mode:** `_is_broad_containment_root` (the H-02 remediation) is invoked **only** inside the `if explicit_root is not None:` branch of `get_containment_roots` (lines 161-168). The default branch's `Path(tempfile.gettempdir()).resolve()` is added to `roots` unconditionally, with **no** broad-root check applied to it. `tempfile.gettempdir()` itself honors the `TMPDIR`/`TEMP`/`TMP` environment variables (Python stdlib documented behavior) before falling back to platform defaults. An attacker or misconfiguration that can influence the process environment -- a poisoned CI environment-variable injection, a compromised shell profile, a malicious `ENV TMPDIR=...` in a base container image, or an upstream tool that sets `TMPDIR` before invoking `jerry` -- can silently cause `tempfile.gettempdir()` to resolve to an attacker-chosen directory (including `/`, `$HOME`, or another maximally broad location), which is then added to the trusted default-root set with **zero** advisory output, unlike the identical broad-root condition reached via `--root`, which *does* warn.

**Effect:** An attacker with environment-variable-level influence (a materially lower bar than code execution in the target process) gains CLI-flag-equivalent power to expand `jerry ast`'s trusted root set to an arbitrary, potentially maximally-broad location -- entirely undetected by the transparency mechanism that was specifically built to warn about exactly this class of over-broad root.

**S/O/D Rationale:** S=8 (silent, unwarned expansion of the trust boundary to an attacker-controlled and potentially maximally broad location). O=3 (requires environment-variable-level influence -- realistic via CI injection, poisoned devcontainer/Dockerfile `ENV`, or a compromised pre-command hook, but not trivial). D=9 (fully undetectable -- no test exercises `TMPDIR`/`TEMP` override, and the broad-root check is structurally scoped away from this code path).

**Corrective Action:** Apply `_is_broad_containment_root` to the resolved `tempfile.gettempdir()` value in the default branch of `get_containment_roots` (and to `_HARDCODED_TMP.resolve()` if it differs from a hardcoded literal), emitting the same stderr WARNING used for the `--root` case.

**Acceptance Criteria:** A test monkeypatches `tempfile.gettempdir` to return `/` or `Path.home()` and asserts the broad-root WARNING fires even with no `--root` supplied.

**Post-Correction RPN Estimate:** S=8, O=3, D=4 -> 96.

---

## Finding Details -- Major

### FM-006-20260807-E: Unguarded `tempfile.gettempdir()` can raise, crashing the command

**Element:** `get_containment_roots()` (`project_root.py:171`).

**Failure Mode:** `roots: list[Path] = [get_project_root().resolve(), Path(tempfile.gettempdir()).resolve()]` calls `tempfile.gettempdir()` with no `try/except`. Per CPython docs, `gettempdir()` can raise `FileNotFoundError` when none of its candidate directories (`TMPDIR`/`TEMP`/`TMP`, then platform defaults) are usable -- realistic in minimal/read-only containers, hardened CI runners, or restrictive chroot/SELinux environments. `_is_broad_containment_root`'s `Path.home()` call has explicit `try/except (RuntimeError, OSError)` guarding it two functions away in the same module; `get_containment_roots`'s `gettempdir()` call has no equivalent guard.

**Effect:** In a constrained environment, **every** `jerry ast` command fails with an unhandled traceback and a non-standard exit code, even for a file that would have passed containment against the project root alone -- because the temp-root computation happens unconditionally before containment matching, with no fallback.

**S/O/D Rationale:** S=6 (denial of service for legitimate operations; breaks the tool entirely in that environment class, though it fails loud rather than silently permissive). O=3 (uncommon but realistic given Jerry's own CI matrix already targets multiple OS/hardening profiles). D=8 (no test simulates `gettempdir()` raising).

**Corrective Action:** Wrap the `tempfile.gettempdir()` call in `try/except OSError`, falling back to project-root-only with a one-line stderr note when temp-dir resolution fails, matching the guarding pattern already used for `Path.home()` in the same module.

**Post-Correction RPN Estimate:** S=4, O=3, D=3 -> 36.

---

### FM-007-20260807-E: Inconsistent fail-open/fail-closed `stat()` posture within one containment check

**Element:** `_check_temp_root_ownership()` (`ast_commands.py:280-287`) vs. the size-check `stat()` in `_check_path_containment()` (`ast_commands.py:356-365`).

**Failure Mode:** `_check_temp_root_ownership`'s `resolved.stat()` call fails **open** (`except OSError: pass`, returns `None` = no error) with the comment "fail open on stat error here; existing size-check stat() below still applies" -- but that later size-check `stat()` fails **closed** (`return None, f"Cannot stat file: {exc}"`). The comment's justification implies the later stat provides a compensating control, but the later check only enforces the 1 MB size limit, not ownership -- so ownership fail-open has no actual compensating control at all; a `stat()` failure (e.g., a race where the file is unlinked/replaced between the two calls) bypasses the ownership gate specifically, with the size check being an unrelated, non-substitute safeguard.

**Effect:** A narrow but real inconsistency: the same containment check fails safe for one property (size) and fails unsafe for another (ownership) on the identical file, under the identical failure class.

**S/O/D Rationale:** S=7 (weakens a security-relevant gate under a stat-failure/race condition). O=3 (requires a transient FS error or timing race -- narrow but not implausible in a shared temp directory under contention). D=7 (the fail-open *behavior* is unit-tested as designed, `test_check_temp_root_ownership_when_stat_oserror_then_fails_open`, but the *security implication* of that design choice -- that it has no compensating control -- is not analyzed or tested).

**Corrective Action:** Make the ownership `stat()` fail **closed** for temp-default-root matches specifically (reject with a descriptive error), consistent with the size check's posture, since fail-open on a security gate silently reintroduces the exact exposure the gate exists to close.

**Post-Correction RPN Estimate:** S=7, O=3, D=3 -> 63 (drops to Minor once consistency is restored and the choice is deliberately tested).

---

### FM-008-20260807-E: Read-time TOCTOU -- symlink swap between containment-check and actual read

**Element:** `_check_path_containment()` (E7) / `_read_file()` (E8) boundary.

**Failure Mode:** `_check_path_containment` resolves `file_path` once (`Path(file_path).resolve()`) and validates the resulting `resolved` path against the allowed roots. `_read_file` then calls `resolved.exists()` and `resolved.read_text(...)` against that already-resolved concrete path -- so swapping the *original* `file_path` symlink after the check does not redirect the read (the read target was already dereferenced). However, if the regular file *at* `resolved`'s exact final path is deleted and replaced by a **new** symlink between the containment check's resolve and `_read_file`'s `read_text()` call, `read_text()` (via `open()`) follows that newly planted symlink by default, since nothing re-verifies `resolved` is still a regular file (not a symlink) immediately before reading. Red-vuln's H-05 analysis examined the *write*-side TOCTOU recheck in detail but did not examine this narrower read-side gap between check and read.

**Effect:** A narrow-window symlink-swap race on the read path could cause `jerry ast parse/render/validate/...` to read and emit the contents of a file that was never checked for containment, into JSON/rendered output.

**S/O/D Rationale:** S=6 (information disclosure via a directory-confused read, output surfaces the foreign content). O=2 (requires attacker write access to the exact resolved path's containing directory plus precise timing between two Python statements -- a very tight window). D=9 (not tested at all; not covered by red-vuln's H-05 scope, which was specifically the write path).

**Corrective Action:** Re-resolve and re-verify the target path immediately before `read_text()` in `_read_file`, rejecting on mismatch against the already-checked `resolved` value -- extending the write-time TOCTOU-recheck pattern already used in `ast_modify` to the read path.

**Post-Correction RPN Estimate:** S=6, O=1, D=5 -> 30.

---

### FM-009-20260807-E: Secondary TOCTOU window between the ownership-check `stat()` and the size-check `stat()`

**Element:** `_check_path_containment()` (`ast_commands.py:290-367`).

**Failure Mode:** The ownership check (`_check_temp_root_ownership`, called around line 342-345) and the size check (lines 356-365) each independently call `.stat()` on the same `resolved` path, rather than sharing one `os.stat()` result. This creates a second, narrower TOCTOU window -- distinct from FM-008's check-to-read window -- during which the file at `resolved` could be swapped between the two stat calls (e.g., an attacker-owned small file swapped for a large one, or vice versa, altering which check applies to which physical file).

**Effect:** Inconsistent enforcement window: the ownership decision and the size decision may not both be evaluated against the same physical file content, in the narrow race between the two syscalls.

**S/O/D Rationale:** S=5 (moderate; enables inconsistent enforcement, not a full containment bypass by itself since containment/resolve already passed). O=2 (narrow race, requires attacker write access plus precise timing between two adjacent statements). D=8 (each check is individually correct in isolation, making the interaction easy to overlook; not tested).

**Corrective Action:** Combine both checks into a single `os.stat()` call whose result (`st_uid`, `st_size`) is reused for both the ownership gate and the size limit.

**Post-Correction RPN Estimate:** S=5, O=1, D=4 -> 20.

---

## Finding Details -- Minor

| ID | Summary | Note |
|----|---------|------|
| FM-010-20260807-E | `Path.home()` raising inside `_is_broad_containment_root` is caught and silently returns "not broad," with no signal that ancestor-of-home detection is degraded | Optional: emit a one-line stderr note when home cannot be determined |
| FM-011-20260807-E | `Path("/tmp")` under `PureWindowsPath` resolves current-drive-relative; a coincidental `C:\tmp` would be silently included, contradicting the docstring's "will not exist" claim | Already flagged by red-vuln as R-5, accepted low-likelihood risk; documented here for completeness of the requested Windows-TEMP analysis |
| FM-012-20260807-E | `_is_broad_containment_root` only flags ancestors of `Path.home()`, not other well-known multi-tenant mounts (`/mnt`, `/data`, NFS shares) supplied via `--root` | Accepted scope limit; optional future widening, not blocking |

---

## Recommendations

**Critical (mandatory before this branch merges/ships):**

1. **FM-001 + FM-002** (shared remediation, highest combined RPN: 720): Replace `_is_temp_default_root_match`'s index-based trust (`matched_root != allowed_roots[0]`) with a location-based check that also treats the project root as a temp-default match when it is itself resolved under `tempfile.gettempdir()`/`_HARDCODED_TMP`. Add a regression test with project root deliberately placed inside a controlled temp root plus a foreign-UID file, asserting rejection.
2. **FM-004**: Add a `geteuid() == 0` disclosure warning on temp-root matches; document the root-uid-convergence limitation explicitly in the fix's design docs and/or a user-facing runbook note.
3. **FM-003**: Re-invoke the ownership gate inside the `ast_modify` write-time TOCTOU recheck, not just the containment check.
4. **FM-005**: Extend `_is_broad_containment_root` coverage to the default-branch `tempfile.gettempdir()` value, closing the `TMPDIR`/`TEMP`/`TMP`-poisoning blind spot in the transparency mechanism.

**Major (recommended before merge, or as immediate fast-follow):**

5. **FM-007**: Align the ownership `stat()` fail posture with the size-check `stat()` (fail-closed for temp-default matches).
6. **FM-006**: Guard `tempfile.gettempdir()` with `try/except OSError`.
7. **FM-008**: Add a read-time TOCTOU recheck immediately before `read_text()`.
8. **FM-009**: Combine the two independent `stat()` calls into one shared result.

**Minor (optional, track as follow-up):** FM-010, FM-011, FM-012 -- documentation-only or low-priority hardening; no blocking action required.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-003: the H-01 ownership-gate fix was propagated to the read path but not the pre-existing write-time TOCTOU-recheck pattern -- an incomplete fix rollout within the same PR |
| Internal Consistency | 0.20 | Negative | FM-001/FM-002: index-based vs. location-based trust is internally inconsistent with the stated purpose of the ownership gate; FM-007: fail-open vs. fail-closed `stat()` posture is inconsistent within one function |
| Methodological Rigor | 0.20 | Negative | FM-004 (root-uid convergence), FM-005 (env-var-driven root expansion), FM-008/FM-009 (residual TOCTOU windows) show the threat model examined by red-vuln did not extend to environment-driven and interaction-level attack surfaces |
| Evidence Quality | 0.15 | Negative | FM-002 shows the existing test suite's own fixtures inadvertently exercise the FM-001-class bypass while documenting it as intended behavior, without flagging the coincidence as security-relevant; FM-006 shows an unguarded call with no corresponding test |
| Actionability | 0.15 | Positive | Every Critical/Major finding here has a concrete, code-level corrective action directly extending the existing H-01/H-02 remediation pattern (not a redesign) -- low-cost, targeted fixes consistent with the codebase's established style |
| Traceability | 0.10 | Neutral | All findings cite exact function/line locations and cross-reference red-vuln's H-01/H-02/H-05 findings by ID; FM-NNN identifiers map 1:1 to the element inventory |

---

*S-012 FMEA execution complete. Assessment only -- no source files modified. Findings persisted per P-002 for tournament aggregation (adv-scorer/orchestrator).*

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
