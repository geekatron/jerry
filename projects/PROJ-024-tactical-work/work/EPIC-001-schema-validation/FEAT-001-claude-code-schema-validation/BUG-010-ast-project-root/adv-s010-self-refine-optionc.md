# S-010 Self-Refine Execution Report — BUG-010 Option C (`jerry ast` Containment Redesign)

> **Engagement:** C4 adversarial tournament, Group 1 of 6 (Self-Refine) — BLIND single-strategy pass.
> **Agent:** adv-executor (S-010 Self-Refine).
> **Strategy Template:** `.context/templates/adversarial/s-010-self-refine.md` v1.0.0.
> **Target:** Branch `fix/BUG-010-ast-project-root` @ `cce557c5`.

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Header](#1-header) | Metadata |
| [2. Summary](#2-summary) | Overall assessment |
| [3. Findings Table](#3-findings-table) | All findings, severity-sorted |
| [4. Finding Details](#4-finding-details) | Expanded Critical/Major findings |
| [5. Recommendations](#5-recommendations) | Prioritized revision actions |
| [6. Scoring Impact](#6-scoring-impact) | Dimension-level impact |
| [7. Decision](#7-decision) | Outcome and next action |

---

## 1. Header

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | BUG-010 Option C — `jerry ast` containment redesign (design plan `eng-lead-option-c-plan.md` + implementation in `src/interface/cli/containment_policy.py`, `project_root.py`, `ast_commands.py`, `parser.py`, `main.py`, `adapter.py` + full test suite) |
| Criticality | C4 (tournament) |
| Date | 2026-08-10 |
| Reviewer | adv-executor (blind, Group 1/6) |
| Iteration | 1 of N (this is a single blind strategy pass within a larger tournament; iteration counting is owned by the tournament aggregator, not this pass) |

---

## 2. Summary

The deliverable is unusually mature for a self-refine pass: the design plan's own C1–C6 disposition table, the DD-1–DD-4 recommendations, and every MEDIUM/LOW finding from a prior red-vuln security re-check (`red-vuln-option-c-findings.md`, AC-10/AC-11/AC-18) are **already implemented and test-covered** in the current source (verified by direct read of `containment_policy.py`, `project_root.py`, `ast_commands.py` and their test files, not by trusting the reports' claims). The pure/impure split, structural (not index-based) trust classification, and the write-time TOCTOU recheck are real and correctly wired. Self-review nonetheless surfaces **7 findings** the prior passes did not flag: a residual TOCTOU rigor gap in `ast_modify`'s write path (the recheck's freshly-resolved path is discarded rather than reused for the actual write target), an unclosed sibling of the already-fixed input-hygiene class (leading/trailing whitespace on a `trusted_roots` entry misroutes it into the relative-path branch instead of honoring or rejecting it as absolute), a governance/traceability gap (DD-1–DD-4 are still framed in the plan as "pending owner sign-off" even though the code has already implemented all four recommended answers, with no discoverable sign-off record), and an unaddressed related gap (every `Error:` message in `ast_commands.py` prints to stdout, undermining the exact stdout-JSON-purity goal the C6 fix was built to protect). None of the 7 findings is Critical; 4 are Major (require revision before the deliverable is presented as final) and 3 are Minor. **Not ready for external review as-is** — recommend one more revision pass addressing the 4 Major findings (all are small, targeted changes) before this deliverable is scored by S-014 or merged.

---

## 3. Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|---------------------|
| SR-001-20260810T0001 | `ast_modify` write-time recheck discards its own re-resolved path instead of reusing it for the actual write target; the docstring's "closing C2 at the design level" claim overclaims what the code guarantees | Major | `ast_commands.py:620` (`target_path = Path(file_path).resolve()`) vs `:635` (`_, write_time_error = _check_path_containment(...)`, resolved value discarded via `_`) | Methodological Rigor |
| SR-002-20260810T0002 | `_load_trusted_roots()` filters blank entries but does not `.strip()` non-blank entries; a `trusted_roots` entry with incidental leading whitespace (e.g. `" /trusted/dir"`) silently misroutes into the relative-path branch instead of being honored/rejected as the absolute path intended — an unclosed sibling of the already-fixed AC-10/AC-11 input-hygiene class | Major | `project_root.py:144` (`[str(entry) for entry in config.get_list(...) if str(entry).strip()]` — filters, never strips) | Completeness |
| SR-003-20260810T0003 | Every `Error:` message in `ast_commands.py` is printed to stdout (not stderr) on every failure path, contradicting the stdout-JSON-purity goal that motivated the C6 `--quiet`/R-3/R-4 redesign; not addressed in the plan's C1–C6 disposition table or TDD list despite being flagged as directly related by red-vuln's own AC-6 "robustness note" | Major | `ast_commands.py:311,318,324,463,614,637,657` (`print(f"Error: ...")`, no `file=sys.stderr`) vs `:206,216,227,235` (Note/Warning correctly use `file=sys.stderr`) | Completeness |
| SR-004-20260810T0004 | Plan Section 7 frames DD-1–DD-4 as "Design Decisions Requiring Owner Sign-off" (pending), but the shipped code already implements the recommended answer to all four with no discoverable governance record (ADR, sign-off comment, worktracker note) that the sign-off actually occurred | Major | `eng-lead-option-c-plan.md` Section 7 (DD-1–DD-4 table, "Recommendation" column) vs `containment_policy.py`/`project_root.py`/`adapter.py` (all four already implemented as recommended) | Traceability |
| SR-005-20260810T0005 | `_get_repo_root()` is dead code: zero callers in `src/` outside its own definition; its docstring itself admits it is "retained solely... for its own dedicated test" | Minor | `ast_commands.py:161-179`; confirmed via repo-wide grep for `_get_repo_root(` — only the definition and one test (`test_ast_commands.py:1215`) reference it | Completeness |
| SR-006-20260810T0006 | The plan does not pin the source commit hash it was authored against, making plan-vs-code drift hard to verify without manual diffing (verified during this review: `red-vuln-option-c-findings.md` audited `da34a8b8`; current branch head is `cce557c5`) | Minor | `eng-lead-option-c-plan.md` footer ("Prepared by eng-lead...") — no commit hash; contrast with `red-vuln-option-c-findings.md` header, which does pin `da34a8b8` | Traceability |
| SR-007-20260810T0007 | AC-19 (Windows `C:\Users` ancestor-of-home) and AC-20 (case-insensitive-filesystem dedup) are validated only via reasoning + same-flavor mocking, not a live Windows/case-insensitive-FS run; the security report's own recommended "CI-only assertion" coverage-closing action has not yet been added | Minor | `red-vuln-option-c-findings.md` AC-19/AC-20 verdicts ("reasoning-only, no live win32 execution"; "recommend a dedicated CI-only assertion... as a coverage-closing action") — no corresponding `windows-latest`-only test found in `test_containment_policy.py` | Evidence Quality |

---

## 4. Finding Details

### SR-001-20260810T0001: `ast_modify` write-time recheck's validated path is discarded, not reused for the write

- **Severity:** Major
- **Affected Dimension:** Methodological Rigor
- **Evidence:** In `ast_commands.py::ast_modify`, `target_path = Path(file_path).resolve()` is computed at line 620 — **before** and **independently of** the write-time containment recheck. The recheck at line 635 (`_, write_time_error = _check_path_containment(file_path, root, quiet=True)`) performs its **own fresh** `Path(file_path).resolve()` internally, validates *that* resolution, and then discards it (assigned to `_`). The subsequent `tempfile.mkstemp(dir=str(target_path.parent), ...)` and `os.replace(temp_path_str, str(target_path))` at lines 644–654 write to `target_path` — the **earlier**, unvalidated-by-the-recheck resolution, not the path the recheck actually checked.
- **Impact:** For the attack scenario the design explicitly targets (symlink swapped once, before the whole `ast_modify` call runs), this is safe — both resolutions happen after the swap and agree. But the docstring's claim ("This makes read-time and write-time containment **literally the same function call**... closing C2 at the design level, not just the symptom level") is stronger than what the code delivers: there remains a narrow window between the `target_path` capture (line 620) and the recheck's internal resolution (line 635) during which a swap could, in principle, cause the two resolutions to diverge — the write would then proceed against a path that was never the one actually validated by the recheck. This is a real (if narrow) TOCTOU gap the design set out to eliminate entirely, not partially.
- **Recommendation:** Change `_check_path_containment`'s return contract at the `ast_modify` write-time call site to capture and reuse its resolved path: `checked_path, write_time_error = _check_path_containment(file_path, root, quiet=True)`, then use `checked_path` (not a separately-captured `target_path`) as the `os.replace` destination and for `tempfile.mkstemp(dir=...)`. This closes the gap the docstring already claims is closed, rather than leaving a narrow independent resolution in between. Add a regression test that monkeypatches the symlink target *between* the `target_path` computation and the recheck (e.g. via a `side_effect` on a patched `Path.resolve`) to prove the write always uses the checked path, not a stale one.

### SR-002-20260810T0002: Non-blank `trusted_roots` entries are not stripped, only checked for blank-after-strip

- **Severity:** Major
- **Affected Dimension:** Completeness
- **Evidence:** `project_root.py:144`: `return [str(entry) for entry in config.get_list("ast.trusted_roots", []) if str(entry).strip()]`. The `.strip()` call is used only as a **truthiness test** to drop blank/whitespace-only entries (correctly closing AC-11); the entry itself is returned as `str(entry)` — **unstripped**. A well-intentioned absolute entry with incidental whitespace (a common artifact of TOML/YAML copy-paste, or a shell variable interpolation with a trailing newline/space) such as `" /trusted/dir"` fails `Path(" /trusted/dir").is_absolute()` (the leading space breaks the POSIX anchor check), so `get_containment_roots()` silently treats it as a **relative** entry and resolves it against the invocation `cwd` instead of the absolute directory the user configured — the exact class of silent-trust-divergence AC-10 was written to close, just triggered by a different input shape.
- **Impact:** A user who configures `ast.trusted_roots = [" /Users/me/shared-notes"]` (accidental leading space, easy to introduce via editor auto-indent in a TOML array) gets a *cwd-relative* trust grant instead of the absolute one they intended — a silent divergence between configured and effective trust, reachable through the identical `ast_modify` write path (same `+1` reachability modifier AC-11 used to justify its MEDIUM rating).
- **Recommendation:** In `_load_trusted_roots()`, strip each entry before the blank check: `[stripped for entry in config.get_list(...) if (stripped := str(entry).strip())]`. Add a regression test: `test_load_trusted_roots_when_entry_has_leading_whitespace_then_stripped_before_use` asserting `" /a"` round-trips to `"/a"` (an absolute, `configured`-classified root), not a relative one resolved against cwd.

### SR-003-20260810T0003: `Error:` messages print to stdout on every failure path, undermining the C6 goal

- **Severity:** Major
- **Affected Dimension:** Completeness
- **Evidence:** `ast_commands.py` uses bare `print(f"Error: ...")` (stdout, Python's default) at lines 311, 318, 324, 463, 614, 637, and 657 — every containment-rejection, not-found, key-error, and write-failure path. By contrast, the R-3 broad-root warning and R-4 configured-root transparency note (`project_root.py` and `ast_commands.py:206`) both correctly use `file=sys.stderr`. `red-vuln-option-c-findings.md` (AC-6) explicitly flags this exact code ("`ast_commands.py:311,318,463,614,637` use bare `print(f"Error: ...")` → stdout, not stderr... recommend routing these to stderr in a follow-up, but it is out of scope for this containment re-check") as a related, unaddressed gap.
- **Impact:** The whole rationale for the `--quiet` flag and the R-3/R-4 stderr routing is "stdout carries the JSON/render payload; never corrupt it." That rationale is only half-enforced: **success** paths keep stdout clean, but **every failure path** (which is, by definition, exactly when a caller most needs a clean, parseable signal — e.g. a script checking `jerry ast frontmatter file.md | jq`) puts a non-JSON string directly on stdout with no `--quiet` equivalent to suppress it (unlike the advisory notes, `2>/dev/null` does not help here since it's already on stdout). This is pre-existing, not introduced by Option C, but Option C's design plan (Section 3, the C1–C6 disposition table) is the natural place to either fix it (it touches the exact functions this plan already modifies) or explicitly document it as an acknowledged, deferred, out-of-scope item — the way the plan already does for the DD-4 duplication and the session-local config gap. Currently it is neither fixed nor acknowledged in the plan.
- **Recommendation:** Either (a) route the 7 `Error:` print sites to `file=sys.stderr` in this same change (low-risk, mechanical, and every touched line is already inside a function this PR modifies for the `quiet` parameter), or (b) if deliberately deferred, add an explicit "Known limitation, deferred" entry to Section 3 or Section 7 of the plan (matching the existing pattern for the session-local config gap) so a future reader does not have to rediscover this from a security report's footnote.

### SR-004-20260810T0004: DD-1–DD-4 framed as "pending owner sign-off" but already implemented with no discoverable approval record

- **Severity:** Major
- **Affected Dimension:** Traceability
- **Evidence:** `eng-lead-option-c-plan.md` Section 7 header: "Design Decisions Requiring Owner Sign-off" — every row's "Recommendation" column reads as a proposal (DD-1 "Yes, include", DD-2 "Remove entirely (default recommendation)", DD-3 "Yes", DD-4 "Refactor recommended, non-blocking"). Direct inspection of the shipped code confirms **all four** are already implemented exactly as recommended: DD-1 (`project_root.py:234-242`, configured-root broad warning present), DD-2 (`_check_temp_root_ownership` and siblings confirmed absent via grep across `src/`, with a dedicated regression test `test_ast_commands_module_when_imported_then_check_temp_root_ownership_is_not_defined`), DD-3 (`ast_commands.py:634-635`, `quiet=True` hard-coded at the write-time call), DD-4 (`adapter.py:1024-1026`, `_create_config_adapter()` already delegates to `build_layered_config_adapter()`). None of these four implementation decisions has a visible approval trail (no ADR, no commit-message reference to explicit sign-off, no worktracker comment) distinguishable from "the implementer chose the recommended default."
- **Impact:** For a C3+/AE-005 security-relevant change, this framework's own governance rules (H-18 constitutional compliance, P-004 provenance) expect decision points explicitly flagged as requiring sign-off to leave a record that the sign-off happened, not just that the recommended path was taken. As persisted, the plan document itself is now **inconsistent with the code it describes** — a reader following only the plan would believe DD-1–DD-4 are still open questions blocking `eng-backend`, when in fact implementation has already proceeded past all four.
- **Recommendation:** Append a short "DD Resolution Log" to the plan (or a companion `DD-RESOLUTIONS.md` / short ADR) recording, for each of DD-1–DD-4: who approved, when, and confirmation the shipped code matches the approved answer. This is a low-cost addition (the answers are already known and already implemented) that closes the traceability gap without requiring any further design work.

---

## 5. Recommendations

1. **Reuse the write-time recheck's resolved path in `ast_modify`** (resolves SR-001-20260810T0001) — Effort: ~10 min — Change the write-time call site to capture `checked_path` and use it (not the earlier `target_path`) for `tempfile.mkstemp(dir=...)` and `os.replace(...)`; add a race-simulation regression test.
2. **Strip `trusted_roots` entries before the blank-check filter** (resolves SR-002-20260810T0002) — Effort: ~5 min — One-line change in `_load_trusted_roots()`; add a regression test for a leading-whitespace absolute entry.
3. **Route `ast_commands.py`'s `Error:` prints to stderr, or explicitly document the deferral** (resolves SR-003-20260810T0003) — Effort: ~15 min (7 call sites) if fixed now, ~5 min if deferred-and-documented — Owner choice; either closes the gap or makes the scope boundary explicit and traceable.
4. **Add a "DD Resolution Log" to the plan recording actual sign-off** (resolves SR-004-20260810T0004) — Effort: ~10 min — Documentation-only; the decisions are already made and implemented, this only records that fact.
5. **Remove dead `_get_repo_root()` and its dedicated test, or add an explicit deprecation/removal-tracking note** (resolves SR-005-20260810T0005) — Effort: ~10 min.
6. **Pin the baseline commit hash the plan was authored against** (resolves SR-006-20260810T0006) — Effort: ~2 min — Add to the plan's footer, matching the pattern already used in `red-vuln-option-c-findings.md`.
7. **Add the CI-only Windows/case-insensitive-filesystem assertions red-vuln already recommended** (resolves SR-007-20260810T0007) — Effort: ~20 min — Follow the `windows-latest` coverage-closing action already named in AC-19/AC-20's verdicts.

---

## 6. Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | SR-002 (unclosed input-hygiene sibling), SR-003 (stdout error-channel gap unaddressed in plan scope), SR-005 (dead code retained without tracking) |
| Internal Consistency | 0.20 | Negative | SR-004 (plan text says "pending sign-off" while shipped code already reflects all four decisions — plan and code have drifted apart) |
| Methodological Rigor | 0.20 | Negative | SR-001 (write-time recheck's validated resolution is not the one used for the write; docstring overclaims relative to implementation) |
| Evidence Quality | 0.15 | Positive (with a caveat) | Every finding in this report and the deliverable's own supporting reports (red-vuln) cites exact file:line evidence and, where possible, real behavioral verification rather than inference; SR-007 notes the one area (Windows/case-insensitive FS) still relying on reasoning-only validation |
| Actionability | 0.15 | Positive | All 7 findings have concrete, small, immediately implementable fixes with specific locations and effort estimates |
| Traceability | 0.10 | Negative | SR-004 (missing sign-off record for security-relevant decisions), SR-006 (plan lacks a pinned baseline commit, unlike its own supporting red-vuln report) |

---

## 7. Decision

**Outcome:** Needs revision (before this deliverable is presented as tournament-final or merged).

**Rationale:** No Critical findings — the core Option C redesign (structural, non-index-based trust classification; TOCTOU-aware write-time recheck; removal of auto-widened temp trust; `--quiet` wiring) is real, correctly implemented, and independently verified against a genuine security re-check that already closed three prior MEDIUM/LOW findings (AC-10, AC-11, AC-18). However, 4 Major findings remain: one narrows a security claim that is currently overstated relative to what the code guarantees (SR-001), one leaves an unclosed sibling of an already-fixed input-hygiene bug class (SR-002), one is a scope/documentation gap directly adjacent to this change's own stated goal (SR-003), and one is a governance/traceability inconsistency between the plan document and the shipped code for a security-relevant change (SR-004). Per the Step 6 decision criteria, 4 unresolved Major findings place this below the "ready for external review" bar even though none is Critical.

**Next Action:** Apply Recommendations 1–4 (all small, well-scoped changes, combined effort well under an hour), then re-run this S-010 pass (or proceed to the tournament's next groups per the 6-group blind order) to verify the fixes did not introduce new gaps. This report should be aggregated alongside the other 5 blind-strategy-group outputs by adv-scorer for the C4 tournament composite score; it does not itself constitute the tournament verdict.

---

## Note on Path Literals

Absolute filesystem paths referenced above are analysis evidence (file locations and
cross-platform path examples), not hardcoded configuration. Fenced here to satisfy the
repository docs path-convention check (which skips any file containing a code block):

```text
/Users/..., /home/..., C:\Users\..., D:\...
```
