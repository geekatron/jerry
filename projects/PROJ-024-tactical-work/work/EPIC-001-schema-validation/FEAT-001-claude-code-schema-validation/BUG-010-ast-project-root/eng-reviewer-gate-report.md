# eng-reviewer Final Gate Report — BUG-010 Containment Widening (PR #341)

> **Agent:** eng-reviewer (Final Review Gate / Quality Enforcer) — Step 7 of `/eng-team`.
> **Subject:** `jerry ast` path-containment scope widening (temp/scratchpad default roots + `--root` flag) and its two red-team remediations (H-01 temp-root ownership gate, H-02 broad-root ancestor-of-home warning).
> **Criticality:** C3 (AE-005 security-relevant, minimum C3). A parallel `/adversary` C4 tournament is being run by the orchestrator; this report does NOT duplicate it (applies an S-007 + S-010 lens and flags focus areas).
> **Branch:** `fix/BUG-010-ast-project-root` (uncommitted worktree). **Verdict:** APPROVE-WITH-CONDITIONS.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict, per-dimension roll-up, blocking items |
| [L1 Per-Dimension Findings](#l1-per-dimension-findings) | Architecture, security, tests, drift, adversarial — with evidence |
| [L1 Residual Findings](#l1-residual-findings) | Severity-ranked residuals for the C4 tournament |
| [L1 Evidence Log](#l1-evidence-log) | Command outputs |
| [L2 Strategic Implications](#l2-strategic-implications) | Posture, debt, tournament handoff |

---

## L0 Executive Summary

**GATE VERDICT: APPROVE-WITH-CONDITIONS.** No blocking items. Both CONFIRMED red-team findings (H-01, H-02) are remediated with dedicated, correctly-scoped regression tests. All specified suites pass (371/371), the A-07 path-traversal regression still passes, ruff/mypy are clean, and the BUG-010 entity is schema-valid and truthful. The change is engineering-complete and release-ready on its own merits.

The verdict is **APPROVE-WITH-CONDITIONS** (not unconditional APPROVE) for one governance reason and one policy reason, neither an engineering defect:

1. **R-013 / C3 gate:** the parallel `/adversary` C4 tournament required for this criticality is still running; final release clearance is contingent on it landing >= 0.95.
2. **One intentional-but-sharp policy asymmetry** (Residual F-1, LOW) should be explicitly confirmed with the owner during the tournament: an explicit `--root` pointed at a shared temp dir bypasses the very H-01 ownership gate that the *default* temp path now enforces. This is by design (user-discretion escape hatch) but deserves a conscious owner sign-off.

| # | Dimension | Verdict | Note |
|---|-----------|---------|------|
| 1 | Architecture (H-07 / H-10 / H-11 / H-12) | **PASS** | Interface imports inward only; function modules (H-10 N/A); mypy clean; all new fns + all 10 `ast_*` `root` params documented |
| 2 | Security-standard compliance | **PASS** (3 LOW residuals) | M-08/M-10/M-05 hold across all roots; H-01 gate correctly scoped + POSIX-guarded; H-02 ancestor-of-home closed; A-07 passes |
| 3 | Test coverage (H-20 / H-21) | **PASS-WITH-CONCERN** | Test-first attested + corroborated; both findings have regression tests; reconciliation seam correct; changed lines covered; file-level absolute % dominated by PRE-EXISTING untested handlers |
| 4 | Standards drift (CHANGELOG / entity) | **PASS** | Both CHANGELOG entries accurate; entity schema-valid, nav-valid, History truthful |
| 5 | Adversarial (S-007 + S-010 lens) | **PASS** | Constitutional triplet + P-001/P-002 satisfied; 3 LOW residuals surfaced for tournament focus |

**Blocking items: NONE.**

---

## L1 Per-Dimension Findings

### 1. Architecture Compliance — PASS

- **H-07 (layer isolation):** Both files remain in `src/interface/cli/` (outermost layer). `project_root.py` is stdlib-only (`os`, `sys`, `tempfile`, `pathlib`). `ast_commands.py` imports `src.domain.markdown_ast` and `src.interface.cli.project_root` — both **inward** imports, which the interface layer is permitted to make. No domain/application layer imports interface. No contamination. **PASS.**
- **H-10 (one public class/file):** Both changed source files contain **zero classes** (`grep -nE "^\s*class "` → none). H-10 constrains classes, not functions; function-only modules are N/A. **PASS.**
- **H-11 (type hints):** Every new/changed signature carries explicit hints (`get_containment_roots(...) -> list[Path]`, `_is_broad_containment_root(resolved: PurePath) -> bool`, `_check_temp_root_ownership(resolved: Path, file_path: str) -> str | None`, `root: str | None = None` on all 10 `ast_*` + `_read_file` + `_check_path_containment`). `mypy` reports **no issues**. **PASS.**
- **H-12 (docstrings):** All new functions have Google-style docstrings; all 10 modified `ast_*` docstrings document the new `root` parameter; the mandated user-discretion policy text is embedded in `get_containment_roots` and `_add_root_argument`. **PASS.**

### 2. Security-Standard Compliance — PASS (3 LOW residuals)

**Containment invariants across ALL allowed roots:**
- **M-08 (path containment):** `matched_root = next((r for r in allowed_roots if resolved.is_relative_to(r)), None)` — rejects when no root matches (`"Path escapes allowed containment roots"`). Correct generalization of the single-root check. **HOLDS.**
- **M-10 (symlink target):** `if not any(realpath.is_relative_to(r) for r in allowed_roots)` — realpath (defense-in-depth) checked against all roots; the primary `.resolve()` (symlink-following) check runs first. **HOLDS.**
- **M-05 (1 MB cap):** Unchanged; applied after containment for every root. **HOLDS.**

**H-01 ownership gate (temp-root, CWE-552/668/281) — correctly scoped:**
- Scoping via `_is_temp_default_root_match`: returns `False` when `explicit_root is not None` (explicit `--root` never gated) and `matched_root != allowed_roots[0]` otherwise. Because `get_containment_roots` always places the **project root first** and preserves order, a project-root match resolves to `allowed_roots[0]` and is never gated — even when the project itself lives under `/tmp` (order + `next()` short-circuit guarantee this). Only `tempfile.gettempdir()`/`/tmp` fallback matches are gated. **Correct.**
- POSIX-guarded: `_check_temp_root_ownership` returns `None` when `os.name == "nt"`; POSIX path compares `resolved.stat().st_uid` to `os.geteuid()`. **Correct.**
- Ordering: ownership check runs **before** the transparency note (a rejected match must not also print an "operating on temp" note). **Correct.**
- Fails open on `stat()` OSError — consistent with the existing size-check philosophy and bounded (a vanished/unstat-able path fails later at size-check or read). **Acceptable, documented.**

**H-02 broad-root warning (ancestor-of-home, incomplete-allowlist) — closed:**
- `_is_broad_containment_root` now returns `True` for filesystem/drive root (`len(parts) <= 1`), `resolved == home`, **and** any ancestor of home (`home.relative_to(resolved)` succeeds). Portable across `PurePath`/`PureWindowsPath` (guards both `ValueError` and `TypeError`). Closes `/home`, `/Users`, `C:\Users`, and `$HOME`'s parent — the exact gaps red-vuln confirmed. Descendants of home correctly NOT flagged. **Closed.**

**CWE coverage:** CWE-22 (A-07 test PASSES — traversal outside all roots rejected); CWE-59 (M-10 multi-root, red-vuln H-03/H-04 refuted); CWE-367 (write-time recheck reuses `get_containment_roots(root)` with the same `root` value as read — no read/write disagreement); CWE-552/668/281 (H-01 gate). **All addressed.**

Residuals F-1..F-3 (all LOW, owner-accepted-by-design or informational) in [Residual Findings](#l1-residual-findings).

### 3. Test Coverage (H-20 / H-21) — PASS-WITH-CONCERN

- **Test-first (H-20):** BUG-010 History attests "10 new tests written and RED-verified (`AttributeError`/assertion failures) before implementation; GREEN after." Corroborated: 24 test references to `_check_temp_root_ownership` / `_is_temp_default_root_match` / `_is_broad_containment_root` — functions that did not exist pre-implementation and would raise `AttributeError` at import/call in the RED phase. RED phase is attested (not independently replayable from the final GREEN state — the normal limitation for post-hoc gate review). **PASS.**
- **Both red-team findings have regression tests:** H-01 → `TestTempRootOwnershipGate` (owned-by-current-user allowed, foreign-uid rejected, project-root/explicit-root NOT gated under foreign uid, Windows `os.name` no-op, stat-OSError fail-open) + direct helper unit tests. H-02 → parametrized `test_is_broad_containment_root_when_ancestor_of_home_then_true` (linux/macos/generic) + `PureWindowsPath("C:\\Users")` + descendant-not-flagged + end-to-end stderr-warning propagation. **PASS.**
- **Reconciliation seam (critical):** The two pre-existing rejection tests (`..._file_outside_project_root_then_rejected`, `..._symlink_escapes_project_root_then_rejected`) each received the `_HARDCODED_TMP` + `tempfile.gettempdir` monkeypatch seam. Without it, `tmp_path`-derived "outside" fixtures (which live under the real system tempdir) would silently START PASSING containment — a false-negative that would gut two security-regression tests. **Correctly handled** — the single sharpest trap in this change.
- **Changed-line coverage:** `project_root.py` 94% (only the defensive `Path.home()` exception branch uncovered); `parser.py` 99% (only license-header lines); the new `ast_commands.py`/`main.py` BUG-010 lines (H-01 gate, multi-root match, ownership helper, `--root` exclusivity, temp transparency note, write-time recheck, `parse` dispatch) are covered. **371 passed.**

**CONCERN (non-blocking):** File-level absolute coverage reads `ast_commands.py` 75% / `main.py` 19% **in this test subset**. This is dominated by **pre-existing untested code**, not BUG-010 changes: `ast_detect`/`ast_sections`/`ast_metadata` have **zero tests anywhere in `tests/`** (a pre-existing RE-006/WI-017 gap — their post-read domain-processing bodies are the bulk of the ast_commands "missing" lines), and `main.py` contains dozens of non-`ast` command handlers unrelated to this change. BUG-010 touched those handlers only by adding a `root` param + one already-covered `_read_file(file_path, root)` line each. Additionally, 9 of 10 `_handle_ast` dispatch lines carrying `root=root` (reinject/detect/sections/metadata/render/frontmatter/validate/query/modify) are not directly integration-covered through `_handle_ast` (only `parse` is) — trivial, structurally-identical pass-throughs; each underlying `ast_X(root=...)` is unit-tested and `--root` parsing is verified for all 10 subcommands. CI gate is `--cov-fail-under=80` global on `--cov=src` (not the H-21 90% per-file); note the H-21(90%) vs CI(80%) standards-drift as a repo-level observation, not a BUG-010 regression.

### 4. Standards Drift — PASS

- **CHANGELOG:** `### Security` entry documents the red-team remediation (H-01 CWE-552/668/281 + H-02/H-08 allowlist) accurately; `### Fixed` entry documents the follow-up widening (temp defaults + `--root` + stderr warning/note). Both match the implemented diff. **PASS.**
- **BUG-010 entity:** `jerry ast validate --schema bug` → `is_valid: true`, `nav_table_valid: true`, `violation_count: 0`. Fix Approach + Acceptance Criteria updated (H-01/H-02 checked `[x]`); three truthful History rows matching the actual diff (scope widening, owner-resolved R-3/R-4, red-team remediation with the 149/149 & 371/371 counts). No status transition (remains `in_progress` under GH #337/#341 — appropriate). **Truthful (P-022). PASS.**

### 5. Adversarial Integration — S-007 + S-010 Lens — PASS

- **S-007 (Constitutional AI Critique):** P-001 (evidence-based — red-vuln cites exact reproductions; this gate cites command outputs), P-002 (persisted — this report + supporting docs), P-020 (owner directive respected: temp widening + `--root` discretion), P-022 (no deception — red-vuln disclosed its flawed negative-control and the modeled-vs-executed distinction; entity History is truthful), H-05 (this gate ran all Python via `env -u VIRTUAL_ENV uv run`). **No violations.**
- **S-010 (Self-Refine lens):** surfaced three LOW residuals (below) for the parallel C4 tournament. None is a defect in the delivered code; all are either owner-accepted-by-design or informational edges worth a conscious confirmation.

---

## L1 Residual Findings

| ID | Severity | Finding | Disposition |
|----|----------|---------|-------------|
| F-1 | LOW | **`--root`/H-01 asymmetry.** An explicit `--root /tmp` (not a filesystem root, not an ancestor of `$HOME`) neither triggers the H-02 broad-root warning nor the H-01 ownership gate, so it permits reading another user's shared-temp file — the exact exposure the *default* path now gates. Intentional (explicit `--root` = user-discretion escape hatch per owner directive) but the sharpest residual edge. | **Tournament focus:** confirm owner explicitly accepts that the escape hatch bypasses the ownership gate. Not a defect. |
| F-2 | LOW/info | **Read-path TOCTOU on shared temp.** The H-01 ownership `stat()` and the subsequent file read are a check-then-use window (CWE-367); an attacker on shared `/tmp` could swap the file between them. Bounded and inherent to read ops; write path is separately mitigated (mkstemp + `os.replace`, red-vuln H-05 refuted). Best-effort per owner directive. | Informational; note only. |
| F-3 | LOW/info | **Ownership gate fails open on `stat()` OSError.** Consistent with the existing size-check; bounded (a non-stat-able path fails later at size-check/read). | Informational; accepted as designed. |
| F-4 | LOW/info | **Pre-existing coverage gap** (NOT introduced here): `ast_detect`/`ast_sections`/`ast_metadata` have no tests; 9/10 `_handle_ast` `root=` dispatch lines not directly integration-covered. | Recommend a follow-up test-debt item; does not block BUG-010. |

---

## L1 Evidence Log

```
# Suites (H-05 compliant: env -u VIRTUAL_ENV uv run --project .)
pytest tests/unit/interface/cli/ tests/security/ tests/integration/cli/ -q   => 371 passed in 29.09s
pytest tests/security/.../TestA07PathTraversal::test_path_traversal_blocked -v => 1 passed  (CWE-22 regression HOLDS)

# Static analysis (4 changed source files)
ruff format --check  => 6 files already formatted
ruff check           => All checks passed!
mypy project_root.py ast_commands.py => Success: no issues found in 2 source files

# Coverage (subset: unit/interface/cli + security + integration/cli)
project_root.py  94%  (miss: defensive Path.home() exception branch 100-104)
parser.py        99%  (miss: license header 25-26)
ast_commands.py  75%  (miss: PRE-EXISTING untested detect/sections/metadata bodies + legacy error branches)
main.py          19%  (miss: dozens of unrelated non-ast handlers; 9/10 ast dispatch lines w/ root=)
CI gate: .github/workflows/ci.yml --cov-fail-under=80 (global --cov=src)

# Entity + architecture
jerry ast validate BUG-010...md --schema bug => is_valid:true nav:true violations:0
grep "^\s*class " (both changed src files)   => none (H-10 N/A)
imports: project_root stdlib-only; ast_commands -> src.domain (inward, allowed)  (H-07 PASS)

# Test-first corroboration
grep -c remediation-helper refs in the 2 test files => 8 + 16 = 24 (would AttributeError pre-impl)
Reconciliation seam present in BOTH pre-existing rejection tests (T-3) => confirmed
```

---

## L2 Strategic Implications

**Security posture vs. threat model:** The widening trades a strictly-project-scoped containment boundary for a project+temp default set plus an unbounded `--root` escape hatch — an explicit, owner-directed risk acceptance ("we can only do our reasonable best-effort"). The two remediations restore the *default* path to a defensible posture (ownership-gated temp access; honest broad-root transparency). The residual attack surface is concentrated entirely in the explicitly-opted-in `--root` path (F-1), which is the correct place for it to live under a user-discretion policy. Symlink (M-10), size (M-05), and traversal (CWE-22) invariants are provably preserved across the widened set.

**Quality trend:** red-lead → red-vuln (2 CONFIRMED, 8 refuted with positive assurance) → eng-lead plan → eng-backend test-first remediation → this gate. Both CONFIRMED findings closed with correctly-scoped fixes and regression tests; zero NEEDS-FIX (partially-broken safeguards) at any stage. The reconciliation-seam handling shows the test-integrity trap was understood and defused rather than tripped.

**Debt / follow-up (non-blocking):** (1) add happy-path tests for `ast_detect`/`ast_sections`/`ast_metadata` (pre-existing gap surfaced by this review, F-4); (2) integration-cover the other 9 `_handle_ast` `root=` dispatch lines; (3) reconcile the repo CI gate (80% global) with the H-21 90% expectation; (4) consider the `get_containment_roots` shape (default-set + exclusive override + testability seams) as a house pattern if a third filesystem-touching CLI surface appears, per eng-lead's SAMM note.

**Tournament handoff:** the parallel C4 `/adversary` tournament should focus its adversarial budget on **F-1** (the `--root`/H-01 asymmetry and whether the owner's acceptance is genuinely informed) and can treat F-2/F-3 as already-characterized bounded residuals. This gate found no engineering defect the tournament must fix — only one policy acceptance to confirm and a pre-existing test-debt item to log.

---

*eng-reviewer gate v1.0 — BUG-010 / PR #341. Verdict APPROVE-WITH-CONDITIONS: no blocking items; release clearance contingent on the parallel C4 `/adversary` tournament landing >= 0.95 (R-013) and owner confirmation of the F-1 `--root`/H-01 asymmetry. All checks run via `uv run` (H-05).*
