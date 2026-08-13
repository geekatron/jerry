# S-010 Self-Refine — BUG-010 H-01 Ownership-Gate Robustness Review

> **Strategy:** S-010 Self-Refine (Group A, C4 tournament, PR #341)
> **Template:** `.context/templates/adversarial/s-010-self-refine.md`
> **Deliverable:** `fix/BUG-010-ast-project-root` branch — `src/interface/cli/{project_root,ast_commands,parser,main}.py` + tests, evaluated against `BUG-010-ast-project-root.md`, `eng-lead-implementation-plan.md`, `red-vuln-findings.md`
> **Criticality:** C4
> **Date:** 2026-08-07
> **Reviewer:** adv-executor (blind, Group A)
> **Iteration:** 1 of 1 (single-pass tournament execution)
> **Lens:** Robustness of the H-01 temp-root ownership gate — scope (temp-default matches only), Windows handling (`os.geteuid` absent → skip), exception handling (fail-open on `OSError`)

---

## 1. Header

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | BUG-010 containment widening + H-01/H-02 red-team remediation (PR #341 follow-up) |
| Criticality | C4 |
| Date | 2026-08-07 |
| Reviewer | adv-executor (Group A, blind) |
| Iteration | 1 of 1 |

**Adaptation note:** S-010 is normally self-review by the deliverable's own creator. This execution applies the same systematic-critique protocol as an independent, blind tournament reviewer (per the invoking orchestration), with Step 5 (Revise and Verify) reframed as "recommend revisions" rather than applying code changes — **assessment only, no code modified**, per task instruction.

---

## 2. Summary

The H-01 ownership gate (`_check_temp_root_ownership`, wired into `_check_path_containment`) correctly closes the multi-user shared-`/tmp` read exposure that red-vuln (RED-BUG010) confirmed and is well-scoped, well-tested, and well-documented for the **read path**. However, self-critique against the stated design goal — "read/write cannot disagree within one invocation" (the `ast_modify` docstring's own claim) — finds that goal is **false for the ownership dimension**: the write-time TOCTOU recheck block in `ast_modify` was updated for the containment-root widening but was never extended to call the ownership gate, so a file that passes ownership at read time is **not** re-verified at write time. Combined with a deliberate fail-open choice on `stat()` errors (which contradicts the sibling size-check's fail-closed behavior three lines away in the same function) and two narrower scope gaps (Windows `%TEMP%`-override assumption, `--root` pointed at a literal temp default), the ownership gate has real robustness gaps despite good engineering hygiene elsewhere. **Not ready for external review as-is** — 2 Critical findings identified.

---

## 3. Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-BUG010S010 | `ast_modify` write-time TOCTOU recheck omits the H-01 ownership gate | Critical | `ast_commands.py:677-682` calls `get_containment_roots(root)` + `is_relative_to` only; never calls `_check_temp_root_ownership` | Internal Consistency, Completeness |
| SR-002-BUG010S010 | Ownership check fails OPEN on `OSError`, contradicting the sibling fail-closed size check | Critical | `ast_commands.py:280-287` (`except OSError: pass`) vs. `ast_commands.py:356-365` (`except OSError as exc: return None, ...`); locked in by `test_check_temp_root_ownership_when_stat_oserror_then_fails_open` (test file L1693-1706) | Methodological Rigor, Internal Consistency |
| SR-003-BUG010S010 | Windows skip (`os.name == "nt"`) assumes default `%TEMP%` without verifying `TMP`/`TEMP` env overrides | Major | `ast_commands.py:260-264` docstring claims per-user isolation "under normal, non-elevated sessions" with no runtime check; only test is `test_check_temp_root_ownership_when_windows_then_skipped_without_crash` (no-crash only, not a safety assertion) | Methodological Rigor |
| SR-004-BUG010S010 | Explicit `--root` pointed at a literal temp-default root (e.g. `--root /tmp`) bypasses both the ownership gate AND all transparency notes (R-3, R-4) | Major | `_is_temp_default_root_match` (`ast_commands.py:207-208`) returns `False` unconditionally when `explicit_root is not None`; `_is_broad_containment_root` does not flag `/tmp` (neither filesystem root nor ancestor of home); `test_check_path_containment_when_explicit_root_given_then_no_transparency_note` confirms silence | Completeness, Internal Consistency |
| SR-005-BUG010S010 | Ownership-gate scoping is root-*identity*-based (index 0 = project root), not location-*safety*-based — a project root that itself resolves inside a shared temp tree bypasses the gate entirely | Minor | `_is_temp_default_root_match` (`ast_commands.py:181-209`) compares `matched_root != allowed_roots[0]`; no check that `allowed_roots[0]` (project root) is itself outside all temp roots | Completeness |
| SR-006-BUG010S010 | R-4 transparency note (`_warn_if_temp_root_match`) also not re-emitted at write time, mirroring SR-001 at lower stakes | Minor | `ast_commands.py:677-682` write-time block calls neither `_warn_if_temp_root_match` nor `_check_temp_root_ownership` | Internal Consistency |

---

## 4. Finding Details

### SR-001-BUG010S010: Write-time TOCTOU recheck omits the H-01 ownership gate

- **Severity:** Critical
- **Affected Dimension:** Internal Consistency, Completeness
- **Evidence:** `ast_modify`'s own docstring (`ast_commands.py:649-653`) states: *"root: ... Threaded identically into the read-time check and the write-time TOCTOU recheck below, so a single invocation never disagrees on the allowed containment set between read and write."* The actual write-time block:
  ```python
  # Re-verify path containment immediately before write (WI-020, M-21)
  if _ENFORCE_PATH_CONTAINMENT:
      allowed_roots = get_containment_roots(root)
      if not any(target_path.is_relative_to(r) for r in allowed_roots):
          print(f"Error: Path escapes allowed containment roots at write time: {file_path}")
          return 2
  ```
  (`ast_commands.py:677-682`) calls `get_containment_roots()` and checks *root containment only*. It never calls `_check_temp_root_ownership` (or `_check_path_containment`, which would include it). By contrast, the read path (`_read_file` → `_check_path_containment`, `ast_commands.py:342-345`) **does** run the ownership gate. No test in `test_ast_commands.py` exercises "read passes ownership at read time, then ownership disagrees at write time" — the only write-time recheck test (`test_ast_modify_when_root_given_and_write_target_outside_root_then_rejected_at_write_time`, L1403-1429) covers the `--root` mismatch case only, never ownership.
- **Impact:** The write-time recheck exists *specifically* to close TOCTOU windows between read and write (per its own WI-020/M-21 comment). Ownership is exactly the kind of attribute vulnerable to the same TOCTOU class as path containment (a symlink retarget between read and write can change both the resolved location *and* its owner). By re-verifying containment but not ownership, the write path retains exactly the CWE-552/CWE-668/CWE-281 exposure that H-01 was added to close — but only for `ast_modify`, the one function that can overwrite a file rather than merely read it. The function's own docstring makes an explicit correctness claim ("never disagrees... between read and write") that is now false for this dimension.
- **Recommendation:** Factor the ownership check into a call reachable from both sites — either (a) route the write-time recheck through `_check_path_containment(file_path, root)` instead of duplicating root-only logic, or (b) call `_is_temp_default_root_match` + `_check_temp_root_ownership` explicitly in the write-time block using the same `matched_root` derivation as the read path. Add a regression test mirroring the existing `--root` write-time test but for ownership (e.g., patch `_read_file` to simulate a read-time pass, then monkeypatch `os.geteuid` to disagree before the write-time block executes, asserting rejection).

### SR-002-BUG010S010: Ownership check fails OPEN on `OSError`

- **Severity:** Critical
- **Affected Dimension:** Methodological Rigor, Internal Consistency
- **Evidence:** `_check_temp_root_ownership` (`ast_commands.py:244-287`):
  ```python
  try:
      if resolved.stat().st_uid != os.geteuid():
          return f"Path in shared temp directory is owned by another user: {file_path}"
  except OSError:
      pass  # Fail open on stat error; the size-check stat() below still applies.
  ```
  Three lines away in the same function, `_check_path_containment`'s size check does the opposite:
  ```python
  try:
      size = resolved.stat().st_size
      if size > _MAX_FILE_SIZE_BYTES:
          return None, (...)
  except OSError as exc:
      return None, f"Cannot stat file: {exc}"
  ```
  (`ast_commands.py:356-365`) — this fails **closed** (rejects with an error) on the identical `OSError` condition. The ownership check's own comment claims consistency ("the size-check stat() below still applies") but the two branches are not consistent in *behavior* — only in the fact that both call `.stat()`. The fail-open behavior is deliberate and is locked in by `test_check_temp_root_ownership_when_stat_oserror_then_fails_open` (test file, L1693-1706), whose own docstring repeats the same "the pre-existing size-check stat() later ... applies its own OSError handling" framing without noting the directional mismatch.
- **Impact:** This is the exact question the tournament lens raises. A security gate that cannot determine the safety predicate (ownership, here) and defaults to *allow* inverts the standard fail-closed principle for access-control checks, and does so inconsistently with the immediately adjacent size-check gate in the same call chain. The `except OSError: pass` path is reachable via a transient stat failure — a permission error, an ENOENT from a raced deletion/recreation in a world-writable shared temp directory, or a filesystem hiccup — precisely the adversarial conditions H-01 was written to defend against. An attacker who can induce a stat() failure on the exact read (e.g., by racing a delete/recreate of the target under a shared `/tmp`) causes the newly-added protection to no-op rather than reject.
- **Recommendation:** Change `except OSError: pass` to fail closed, e.g. `except OSError as exc: return f"Cannot verify ownership of temp-root path: {file_path} ({exc})"`, mirroring the sibling size-check's pattern exactly. Update `test_check_temp_root_ownership_when_stat_oserror_then_fails_open` to assert rejection (rename to `..._then_fails_closed`). If a deliberate fail-open exception is still desired for a specific narrow scenario (e.g., file legitimately vanished before read, which `_read_file`'s own `resolved.exists()` check would catch anyway with its own "File not found" error), document that rationale explicitly rather than relying on the (incorrect) claim that it mirrors the size check.

### SR-003-BUG010S010: Windows skip assumes default `%TEMP%` without verifying env overrides

- **Severity:** Major
- **Affected Dimension:** Methodological Rigor
- **Evidence:** `_check_temp_root_ownership`'s docstring (`ast_commands.py:260-264`): *"Windows' per-user `%TEMP%` (`C:\Users\<user>\AppData\Local\Temp`) already structurally isolates temp directories by user under normal, non-elevated sessions, so this check is a deliberate no-op there rather than an oversight."* The code (`ast_commands.py:280-281`) unconditionally returns `None` (allow) whenever `os.name == "nt"`, with no check of what `tempfile.gettempdir()` actually resolved to for this invocation. `tempfile.gettempdir()` on Windows honors `TMP`/`TEMP`/`USERPROFILE` env vars in that priority order (CPython stdlib behavior); if any process or administrator sets `TMP`/`TEMP` to a shared network path or a shared local directory (a realistic scenario in managed/enterprise Windows environments, CI runners, or containerized Windows images), the "per-user by default" assumption silently breaks, and the ownership gate is unconditionally skipped regardless. This is the same *class* of gap red-vuln flagged for `_is_broad_containment_root` (H-02/H-08: an incomplete allowlist that checks a specific known-safe case rather than the general condition) — here applied to a bypass condition instead of a warning condition.
- **Impact:** On a non-default Windows configuration, `jerry ast` would read/write shared-temp files with **zero** ownership protection and **zero** signal that the assumption underlying the `os.name == "nt"` skip does not hold for this host. The gap is undetectable to the user (no warning, no error) and untested (the only Windows-path test, `test_check_temp_root_ownership_when_windows_then_skipped_without_crash`, asserts absence of a crash, not absence of risk).
- **Recommendation:** At minimum, add a `PureWindowsPath`-based unit test (as red-vuln already recommended for the related H-02/H-08 closure) verifying the code's behavior when `tempfile.gettempdir()` is monkeypatched to a non-default (e.g., shared/UNC) path on a simulated Windows environment, and decide explicitly (not by omission) whether that scenario should warn, degrade to the broad-root warning path, or remain silently accepted — the same three-way disposition red-vuln applied to R-3. This does not require implementing a Windows ownership-equivalent check (out of proportion, per red-vuln's own assessment) — only making the assumption's boundary condition observable and tested rather than implicit.

### SR-004-BUG010S010: Explicit `--root /tmp` (or `--root <gettempdir()>`) bypasses both the ownership gate and all transparency notes

- **Severity:** Major
- **Affected Dimension:** Completeness, Internal Consistency
- **Evidence:** `_is_temp_default_root_match` (`ast_commands.py:181-209`) returns `False` unconditionally whenever `explicit_root is not None` — regardless of what that explicit root actually resolves to. `_is_broad_containment_root` (`project_root.py:63-117`) only flags filesystem/drive roots and ancestors-of-home; `/tmp` and `tempfile.gettempdir()`'s resolved value are neither, so `--root /tmp` triggers no R-3 warning either. `test_check_path_containment_when_explicit_root_given_then_no_transparency_note` (test file L1483-1504) confirms silence for an explicit root generically, but no test exercises the specific case where the explicit root *is* the same directory that would otherwise be a temp-default match.
- **Impact:** The design's stated rationale for exempting `--root` from the ownership gate and transparency notes is that it represents the user's own **deliberate** choice ("user discretion... not a security boundary against a user who has already chosen to grant the tool broad access"). That rationale is sound for an arbitrary directory the user names. It is weaker when the resolved `--root` happens to coincide with a well-known shared multi-tenant location (`/tmp`, `tempfile.gettempdir()`) — a user (or, more likely, a wrapper script or a default configuration that sets `--root "$TMPDIR"` for convenience) gets the exact CWE-552 exposure H-01 was built to close, with no ownership check and no signal, purely because the path arrived via `--root` instead of the default-fallback path. The two code paths (default-fallback temp match vs. explicit-root temp match) are functionally identical in risk but diverge completely in protection.
- **Recommendation:** When `explicit_root` resolves to a path equal to (or contained within) `tempfile.gettempdir()` or `/tmp`, apply the same ownership-gate and/or transparency-note treatment as the default-fallback case, rather than treating "explicit" as a blanket exemption. This is a narrower, more defensible carve-out than gating all `--root` values, and closes the specific gap where "explicit" and "default" produce identical filesystem exposure but different protection levels.

### SR-005-BUG010S010: Ownership-gate scoping is root-identity-based, not location-safety-based

- **Severity:** Minor
- **Affected Dimension:** Completeness
- **Evidence:** `_is_temp_default_root_match(matched_root, allowed_roots, explicit_root)` (`ast_commands.py:181-209`) determines "is this a temp-default match" purely via `matched_root != allowed_roots[0]`, where `allowed_roots[0]` is always the project root when `explicit_root is None` (per `get_containment_roots`'s documented ordering). There is no check that the project root itself is disjoint from the temp roots.
- **Impact:** If `CLAUDE_PROJECT_DIR` is unset and the invoking process's cwd happens to be located under `tempfile.gettempdir()` or `/tmp` (e.g., a script that `cd`s into a scratch directory before invoking `jerry ast` without setting the env var), `get_project_root()` resolves to a path physically inside a shared temp tree, becomes `allowed_roots[0]`, and any file under it matches the project root (checked first in `_check_path_containment`'s `next(...)` scan) rather than the temp-default entries — even though it is, in fact, under a shared, potentially world-writable directory. The ownership gate is skipped entirely for this case since the match is classified "project root."
- **Recommendation:** Consider deriving `_is_temp_default_root_match` from actual filesystem location (is `matched_root` one of the OS temp roots, regardless of list index) rather than list-position identity, or explicitly document this as an accepted edge case (consistent with the existing R-7 "no existence validation" pattern already accepted elsewhere in this design) if judged low-priority.

### SR-006-BUG010S010: R-4 transparency note also not re-emitted at write time

- **Severity:** Minor
- **Affected Dimension:** Internal Consistency
- **Evidence:** Same write-time block as SR-001 (`ast_commands.py:677-682`) calls neither `_warn_if_temp_root_match` nor `_check_temp_root_ownership`. The read path emits the R-4 stderr note (`_warn_if_temp_root_match`, `ast_commands.py:212-241`) when a match is via a temp-default root; `ast_modify`'s write completes silently with no equivalent note.
- **Impact:** Low-severity (transparency-only, not a security control) but reinforces the pattern in SR-001: the write-time recheck block was updated for the containment-root widening itself but not for either of the two behaviors layered on top of it (ownership gate, transparency note) during the subsequent H-01/R-4 passes.
- **Recommendation:** Bundle with the SR-001 fix — if the write-time recheck is refactored to call `_check_path_containment` directly (option (a) under SR-001), the transparency note comes along for free via the same code path.

---

## 5. Recommendations

Prioritized action list:

1. **Extract/route the write-time recheck in `ast_modify` through the same ownership-gate logic as the read path** (resolves SR-001-BUG010S010, SR-006-BUG010S010). Highest priority — this is the one finding where the security control's own documented invariant ("read/write cannot disagree") is demonstrably false.
2. **Change `_check_temp_root_ownership`'s `except OSError` from fail-open to fail-closed**, matching the sibling size-check pattern in the same function (resolves SR-002-BUG010S010).
3. **Add a `PureWindowsPath`/monkeypatched-`gettempdir()` test for the Windows skip boundary condition** and make an explicit (not implicit) decision on non-default `%TEMP%` handling (resolves SR-003-BUG010S010).
4. **Apply ownership-gate/transparency treatment when an explicit `--root` resolves to a literal temp-default location** (resolves SR-004-BUG010S010).
5. **(Optional, low priority) Derive temp-default-match classification from actual location rather than list-index identity** (resolves SR-005-BUG010S010).

---

## 6. Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | SR-001, SR-004, SR-005 identify write-path and `--root`-scoping cases the H-01/R-4 remediation does not cover |
| Internal Consistency | 0.20 | Negative | SR-001/SR-002/SR-006 show the code's own docstring claims (write/read parity, "consistent with the size check") contradicted by the implementation |
| Methodological Rigor | 0.20 | Negative | SR-002 (fail-open choice not justified against the fail-closed sibling pattern), SR-003 (unverified environmental safety assumption) |
| Evidence Quality | 0.15 | Positive | Every finding traces to exact line ranges and existing test names; the deliverable's own extensive test suite corroborates rather than contradicts the findings (e.g., the fail-open test explicitly locks in the behavior under critique) |
| Actionability | 0.15 | Positive | Each finding has a precise, line-scoped fix and, where applicable, a concrete test-change recommendation |
| Traceability | 0.10 | Positive | All findings cite the specific function, line range, and (where relevant) the specific existing/missing test |

---

## 7. Decision

**Outcome:** Needs revision — Critical findings present (SR-001, SR-002).

**Rationale:** Per the S-010 protocol, Critical findings make revision mandatory before external/final acceptance. SR-001 is the most consequential: the H-01 ownership gate's core purpose (close CWE-552/668/281 for shared temp-directory access) is only half-implemented — the read path enforces it, the write path (the more consequential of the two, since it can overwrite another user's file rather than merely disclose its contents) does not, despite the function's own docstring claiming read/write parity. SR-002 shows the implemented gate defaults to permissive behavior under exactly the failure condition (stat() error under a contested, world-writable shared directory) where an adversary is most likely to be operating. Neither gap was surfaced by the eng-lead plan or red-vuln's assessment (both scoped their write-time analysis to path containment, not ownership), which is consistent with S-010's role as a distinct lens from red-team/constitutional review — self-refine caught an internal-consistency gap between a documented invariant and its implementation, not a novel attack scenario per se.

**Next Action:** Route SR-001/SR-002 fixes to eng-backend before merge. SR-003/SR-004 (Major) should be resolved or explicitly risk-accepted with owner sign-off, consistent with how R-3/R-4 were already handled as open decisions in the eng-lead plan. SR-005/SR-006 (Minor) may be deferred as documented follow-ups.

---

*S-010 Self-Refine execution — RED-BUG010/BUG-010 tournament, Group A, blind. No code modified. No other adversarial strategy's output was consulted in producing this report.*
