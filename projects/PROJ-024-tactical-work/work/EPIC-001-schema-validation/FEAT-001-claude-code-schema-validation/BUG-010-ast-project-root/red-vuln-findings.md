# red-vuln Findings — BUG-010 Containment Widening (RED-BUG010)

> **Agent:** red-vuln (Vulnerability Analyst) — Step 2 of `/red-team`, executing under the scope and Rules of Engagement authored by red-lead.
> **Engagement:** RED-BUG010 — white-box source-code security assessment of the `jerry ast` path-containment widening (PR #341 owner-review follow-up).
> **Scope document (authoritative):** [`red-lead-scope-and-attack-plan.md`](red-lead-scope-and-attack-plan.md)
> **Deliverable type:** Executed hypothesis verdicts (H-01..H-10) with in-process/sandbox evidence, severity, and remediation. No exploit run against any live or real-user target; no production source or tests modified.
> **Methodology:** PTES Vulnerability Analysis phase + NIST SP 800-115 Ch. 5, applied to a white-box code review per red-lead's threat model.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Verdict counts, headline findings, plain-language risk |
| [L1 Verdict Table](#l1-verdict-table) | All 10 hypotheses: ID, CWE, verdict, severity, evidence, remediation |
| [L1 Detailed Findings — CONFIRMED](#l1-detailed-findings--confirmed) | H-01, H-02 full evidence and remediation detail |
| [L1 Detailed Findings — REFUTED (Positive Assurance)](#l1-detailed-findings--refuted-positive-assurance) | H-03..H-07, H-09, H-10 |
| [L1 Detailed Findings — Code-Reasoning Only](#l1-detailed-findings--code-reasoning-only) | H-08 (Windows, no host in scope) |
| [L2 Strategic Implications](#l2-strategic-implications) | Remediation priority, test-suite gap closure, handoff to eng-backend |
| [Methodology and Evidence Provenance](#methodology-and-evidence-provenance) | Probe script location, existing-test corroboration, honesty caveats |
| [Constitutional Compliance](#constitutional-compliance) | P-001/P-002/P-020/P-022 attestation |

---

## L0 Executive Summary

All 10 ranked hypotheses from the red-lead attack plan were executed against the **real, shipped code** (`src/interface/cli/project_root.py`, `src/interface/cli/ast_commands.py`) via in-process function calls in a disposable sandbox, exactly as the plan specified. Result: **the plan's predictions were correct in every case.**

**2 CONFIRMED findings** (both predicted by red-lead as the most-likely headline findings):

- **H-01 — Multi-user temp read/write, no ownership check** (CWE-552 / CWE-668 / CWE-281). Confirmed: a temp-root match is allowed with **zero** `st_uid`/`geteuid()` ownership gate anywhere in the code. Severity is deployment-model-dependent: **MEDIUM** on a single-user dev laptop (dominant deployment), **HIGH** on a shared/CI multi-tenant host.
- **H-02 — Broad-root warning coverage gap** (`_is_broad_containment_root`, incomplete-allowlist class). Confirmed: `--root /home`, `--root /Users`, and `--root $HOME/..` (home's parent) all fail to trigger the "unusually broad" stderr warning, even though each effectively disables containment across every user on the host. Severity **LOW** (advisory-only control; the underlying `--root` behavior itself is accepted, user-discretion policy — only the *transparency* is gapped).

**8 REFUTED / SAFE (positive assurance)**, meaning red-vuln actively demonstrated the invariant holds rather than assuming it:

- H-03 (symlink escape from temp root) — rejected. H-04 (`--root` exclusivity + symlink) — exclusive, non-additive, non-escapable. H-05 (write-time TOCTOU) — recheck + `mkstemp` + `os.replace` intact. H-06 (predictable temp staging) — `mkstemp` is the sole write primitive, mode `0o600` confirmed. H-07 (path traversal) — all traversal/absolute-path variants rejected under the widened default set. H-08 (Windows semantics) — drive-root case SAFE; UNC-subpath case has the **same coverage-gap class as H-02** (code-reasoning only, no Windows host in scope per RoE — treated as a documentation note, not a new distinct finding). H-09 (stdout/stderr stream separation) — advisory text never leaks onto stdout; JSON integrity preserved. H-10 (relative/non-existent `--root`) — resolves against cwd as documented; non-existent root is fail-closed.

**Deployment-model disclosure (per rubric requirement):** This assessment states both deployment models explicitly rather than picking one silently. Jerry's primary distribution today is a single-developer CLI/plugin run on a personal machine (H-01 = MEDIUM in that model). If Jerry is ever run on a shared host, CI runner with a shared `/tmp`, or multi-tenant container image where multiple principals can write to the same `gettempdir()`/`/tmp`, H-01 escalates to **HIGH** under the same code path with no additional attacker capability required.

**Count:** 2 CONFIRMED (1 MEDIUM/HIGH-dependent, 1 LOW) · 0 NEEDS-FIX (no partially-broken safeguard found) · 8 REFUTED (positive assurance, including 1 with a documented Windows-only coverage-gap caveat under H-08).

---

## L1 Verdict Table

| ID | CWE | Verdict | Severity | Evidence excerpt | Remediation |
|----|-----|---------|----------|-------------------|-------------|
| **H-01** | CWE-552, CWE-668, CWE-281 | **CONFIRMED** | MEDIUM (single-user laptop) / **HIGH** (shared/CI multi-tenant host); +1 level if reached via `ast_modify` (write) | `_check_path_containment(str(victim))` on a synthetic file placed directly under `gettempdir()` (no `CLAUDE_PROJECT_DIR` relation) → `(resolved, None)` = **ALLOWED**. `grep st_uid\|geteuid` across both changed files → **zero matches**. Negative control (genuinely outside all roots, isolated via monkeypatched temp seams) → correctly **rejected**, proving the allow path is real and not a probe artifact. | Add an ownership gate: for matches against a **temp-default root only** (not the project root, not an explicit `--root`), additionally require `resolved.stat().st_uid == os.geteuid()` before allowing. POSIX-only; on Windows (`os.geteuid` does not exist), gate on `os.name == "nt"` and skip the UID check (Windows temp dirs are per-user by OS default: `%TEMP%` resolves to `C:\Users\<user>\AppData\Local\Temp`, so the exposure class is materially smaller there) — see remediation detail below. |
| **H-02** | CWE-1284-adjacent (incomplete allowlist) | **CONFIRMED** | LOW (advisory-control gap only; underlying `--root` broad-access behavior is accepted owner policy) | `get_containment_roots("/home")`, `get_containment_roots("/Users")`, `get_containment_roots(str(Path.home().parent))` → stderr warning **absent** in all three cases (deterministic, captured via `capsys`-equivalent). `get_containment_roots("/")` and `get_containment_roots(str(Path.home()))` → warning **fires** correctly (existing behavior confirmed intact). | Widen `_is_broad_containment_root`: warn when `resolved` is an **ancestor of `Path.home().resolve()`** (catches `/home`, `/Users`, `C:\Users`, home's parent, and any deeper multi-user parent) in addition to the existing exact-filesystem-root and exact-home checks. See code sketch below. |
| H-03 | CWE-59 | REFUTED (positive assurance) | — (verified SAFE) | Symlink inside an isolated, fully-monkeypatched allowed temp root pointing to a synthetic file outside all roots → `_check_path_containment` returns `"Path escapes allowed containment roots: ..."` (rejected at the **primary** `resolved = Path(file_path).resolve()` check, before the secondary M-10 check ever runs). Symlink to a file **inside** the same temp root → allowed by design (documented, not a defect). | None required. |
| H-04 | CWE-22, CWE-59 | REFUTED (positive assurance) | — (verified SAFE) | (1) Project-root file rejected under `--root` elsewhere — exclusivity proven. (2) File inside `X` allowed under `--root X`. (3) Symlink inside `X` escaping to outside → rejected. (4) `--root` pointing at a symlinked directory resolves to **exactly one** allowed root (`len(roots) == 1`), with no additive re-admission of the project root. | None required. |
| H-05 | CWE-367 | REFUTED (positive assurance) | — (verified SAFE-with-caveat) | Source inspection confirms: write-time recheck present (`"Re-verify path containment immediately before write"` block, reusing the same `root` param as the read call — read/write cannot disagree within one invocation); `tempfile.mkstemp` used; `os.replace` used (atomic rename semantics — replaces the symlink itself, does not follow a final-component symlink to write through it); no fallback `open(path, "w")` write path exists inside `ast_modify`. | None required. Residual TOCTOU window (attacker races between recheck at line ~597 and the `mkstemp`/`os.replace` sequence) is bounded by OS rename atomicity and is the same class the M-21 mitigation already targets — not a new gap introduced by the widening, only a larger world-writable staging area when the matched root is `/tmp`/`gettempdir()` (this is the H-01 exposure, not a distinct TOCTOU escalation). |
| H-06 | CWE-377 | REFUTED (positive assurance) | — (verified SAFE) | `tempfile.mkstemp(dir=..., suffix=".tmp", prefix=".ast_modify_")` executed exactly as called in `ast_modify`; resulting file mode confirmed `0o600` via `os.stat().st_mode & 0o777`. `mkstemp`'s `O_CREAT\|O_EXCL\|O_RDWR` contract is a stdlib guarantee not overridable from the call site; no non-`mkstemp` temp-write path exists in the module. | None required. |
| H-07 | CWE-22 | REFUTED (positive assurance) | — (verified SAFE; regression-guard held) | `_check_path_containment` on `"../../etc/passwd"`, `"/etc/passwd"`, `"/etc/shadow"`, `"/root/.ssh/id_rsa"` → all **rejected** under the widened defaults. Traversal that lands in a **sibling** of an allowed temp root (not itself a registered root) → also rejected, confirming the widening only admits the exact registered roots, not their parents/siblings. Existing regression test `tests/security/test_adversarial_parsers.py::TestA07PathTraversal` re-run unmodified against current code: **passes** (part of the 136/136 pass run below). | None required. |
| H-08 | CWE-22, CWE-59 | **REFUTED for drive-root case (SAFE)**; documented coverage-gap caveat for UNC-subpath case, same class as H-02 | LOW-MEDIUM (code-reasoning only — no Windows host in scope per RoE) | `PureWindowsPath("C:\\").parts == ('C:\\\\',)` → `_is_broad_containment_root` returns `True` (warns, as expected). `PureWindowsPath("\\\\host\\share").parts` → single anchor element → `True` (warns). `PureWindowsPath("\\\\host\\share\\sub").parts` → 2 elements → `False` (does **not** warn, despite still denoting an entire shared multi-user network share). `PureWindowsPath("C:\\Users").parts` → 2 elements → `False` (same `/Users`-class gap as H-02, on Windows). No live Windows host was used, per RoE — this is code-reasoning against `PureWindowsPath` only, exactly as the plan specifies. | Fold into the H-02 remediation (ancestor-of-home / well-known-multi-user-parent check) — `Path.home()`-ancestor logic is portable across `PurePath`/`PureWindowsPath` when expressed via `.parts` comparison rather than `Path.home()` object equality; a `PureWindowsPath`-based unit test (`tests/unit/interface/cli/test_project_root.py`) is recommended, as red-lead's plan notes CI already runs `windows-latest`. |
| H-09 | Robustness (no CWE — advisory-control correctness) | REFUTED (positive assurance) | — (verified SAFE) | `capsys`-equivalent capture: temp-root-match note appears **only** on stderr (never stdout); correctly **suppressed** for a project-root match; broad-root `--root /` warning appears **only** on stderr (never stdout). JSON payload integrity for `jerry ast ... \| jq` consumers is preserved. | None required. |
| H-10 | CWE-73 | REFUTED (positive assurance) | — (verified SAFE / fail-closed) | `get_containment_roots("relative/dir")` under a known cwd resolves to `cwd/relative/dir` exactly, consistent with `get_project_root()`'s documented no-validation contract. `get_containment_roots("/does/not/exist/...")` returns `[that path]` with no existence check (as documented); a real file checked against that non-existent root is correctly **rejected** (`is_relative_to` fails for everything) — fail-closed by construction, not fail-open. | None required. |

---

## L1 Detailed Findings — CONFIRMED

### H-01 — Multi-user temp read/write with no ownership check

**CWE-552** (Files Accessible to External Parties), **CWE-668** (Exposure of Resource to Wrong Sphere), **CWE-281** (Improper Preservation of Permissions).

**Code under test:**
- `src/interface/cli/project_root.py:147-153` — `get_containment_roots()` unconditionally adds `Path(tempfile.gettempdir()).resolve()` and (existence-gated) `_HARDCODED_TMP.resolve()` (`/tmp`) to the default allowed set. No per-file, per-user, or per-owner gate is applied to either root.
- `src/interface/cli/ast_commands.py:260` — `matched_root = next((r for r in allowed_roots if resolved.is_relative_to(r)), None)`. Containment is evaluated purely on **location** (is the resolved path under an allowed root) — there is no ownership/UID predicate anywhere in the containment check.

**Reproduction (executed against the real functions, in a disposable sandbox, synthetic data only):**

1. Set `CLAUDE_PROJECT_DIR` to a throwaway project directory `project_a`.
2. Write a synthetic stand-in "victim" file (`SYNTHETIC-NOT-A-REAL-SECRET: token=deadbeef`) directly under `tempfile.gettempdir()` — **not** under `project_a`.
3. Call `_check_path_containment(str(victim))` with no `--root`.
4. **Result:** `(resolved_path, None)` — **ALLOWED**. The stderr transparency note (`Note: '<path>' is outside the project root; jerry ast is operating on a temp/scratchpad path (...)`) fires correctly, confirming the tool *knows* it left the project but proceeds anyway with no further gate.
5. Grep of both changed source files for `st_uid`/`geteuid` → **zero matches**, confirming no ownership check exists to bypass; the widening genuinely lacks this control rather than having a broken one.
6. Negative control (methodologically corrected — see [Methodology](#methodology-and-evidence-provenance)): a file in a directory that is **neither** the project root **nor** any allowed temp root (isolated via monkeypatching both temp-root seams so the control is not accidentally re-admitted by the host's real `/tmp`) → correctly **rejected** with `"Path escapes allowed containment roots"`. This proves the H-01 allow-path is the genuine temp-root-matching behavior, not a test artifact.

**Escalation to the real-world multi-user case (modeled, per RoE — not executed against any real other-user file):** On a shared host or CI runner, `gettempdir()`/`/tmp` are shared, often world-readable, multi-tenant directories. Any process running `jerry ast parse <other-user-temp-file>` with no `--root` would pass containment under the current code, reading a file it does not own. For `ast_modify` (write path), the same containment check gates the write-time recheck (`ast_commands.py:596-599`); the OS sticky bit on `/tmp` (`drwxrwxrwt`) blocks **overwriting/renaming another user's existing file**, but does **not** block Jerry from **reading** another user's file, nor from **creating a new file** in the shared temp directory.

**Deployment-model-dependent severity (explicit, per rubric requirement):**

| Deployment model | Severity | Rationale |
|---|---|---|
| Single-user dev laptop (Jerry's dominant current deployment: Claude Code plugin/CLI on a personal machine) | **MEDIUM** | The "other user" in `gettempdir()` is the same OS user; no cross-tenant exposure, but the tool still reads/writes outside the stated project boundary without an explicit `--root` grant — a scope-creep/accidental-disclosure risk, not a cross-tenant one. |
| Shared/CI multi-tenant host (multiple OS users or containers sharing `/tmp`) | **HIGH** | Reachable under **default configuration** (no `--root`, no env bypass) and constitutes unauthorized cross-tenant read access; +1 severity level applies per the rubric's "reachable under default config, no `--root`, no env var" modifier. |

**Remediation (minimal, cheap, preserves the owner's accepted use case):**

```python
# In _check_path_containment, after matched_root is determined and BEFORE
# returning success, add an ownership gate scoped ONLY to temp-default
# matches (never to the project root, never to an explicit --root -- both
# remain pure user-discretion as today):

if explicit_root is None and matched_root != allowed_roots[0]:  # temp-root match, not project root
    if os.name != "nt":  # os.geteuid() does not exist on Windows
        try:
            if resolved.stat().st_uid != os.geteuid():
                return None, f"Path is a temp-root match not owned by the current user: {file_path}"
        except OSError:
            pass  # fail open on stat error here; existing size-check stat() below still applies
```

**Windows caveat (explicitly addressed, since `os.geteuid()` does not exist there):** Do not attempt a UID-equivalent check on Windows. `tempfile.gettempdir()` on Windows already resolves to a **per-user** path (`%TEMP%` → `C:\Users\<user>\AppData\Local\Temp` under normal, non-elevated sessions), so the cross-tenant exposure class this remediation targets is structurally much smaller on Windows than on POSIX shared-`/tmp` hosts. The portable approach is therefore: **gate on `os.name`, not on a Windows-side ownership API** — apply the `st_uid`/`geteuid()` check when `os.name != "nt"`, and rely on Windows' existing per-user temp-directory isolation for the Windows case (optionally, a future hardening could additionally check `win32security`-based owner SID via `pywin32`, but that is a new dependency and out of proportion to this fix — not recommended here).

---

### H-02 — Broad-root warning coverage gap

**CWE-1284-adjacent** (incomplete allowlist / improper validation of specified quantity — the check enumerates two specific "broad" cases rather than a general rule).

**Code under test:** `src/interface/cli/project_root.py:63-93`, `_is_broad_containment_root()`. Logic: `True` only when `len(resolved.parts) <= 1` (exact filesystem/drive root) **or** `resolved == Path.home().resolve()` (exact home directory, by object equality).

**Reproduction (deterministic, in-process, no filesystem writes needed beyond the resolve calls):**

| `--root` candidate | Class | Warning fires? |
|---|---|---|
| `/` | Exact filesystem root | **True** (SAFE — as designed) |
| `Path.home()` (this host: `/Users/adam.nowak`) | Exact `$HOME` | **True** (SAFE — as designed) |
| `/home` | Linux multi-user parent | **False** — GAP |
| `/Users` | macOS multi-user parent | **False** — GAP |
| `Path.home().parent` (`/Users` on this host) | Parent of `$HOME` | **False** — GAP (same as above on macOS; distinct concrete path on Linux, e.g. `/home`) |

Each of the three gap cases contains **every user's home directory** on the host — functionally as broad as the filesystem root for containment purposes — yet the advisory warning the code promises ("best-effort protection... a single-line, non-fatal WARNING... noting that containment is effectively disabled") does not fire. The underlying `--root` behavior (proceeding anyway) is intentional owner-accepted policy and is **not** the finding; the gap is purely in the *transparency* mechanism.

**Severity: LOW.** Per the rubric, this is a weakness in an advisory control with no escape-or-bypass consequence (the invocation would proceed identically with or without the warning — the finding is that the user isn't told). The owner explicitly accepts broad `--root` values at user discretion; this finding only means the promised transparency doesn't fully cover the "obvious over-broad roots" class red-lead flagged.

**Remediation:**

```python
def _is_broad_containment_root(resolved: PurePath) -> bool:
    if len(resolved.parts) <= 1:
        return True
    try:
        home = Path.home().resolve()
    except (RuntimeError, OSError):
        return False
    if resolved == home:
        return True
    # NEW: also flag any ancestor of the user's home directory -- catches
    # /home, /Users, C:\Users, and home's parent generically, without
    # hard-coding platform-specific well-known paths.
    try:
        home.relative_to(resolved)
        return resolved != home  # already handled by the equality check above; guards double-count
    except ValueError:
        return False
```

Note: `home.relative_to(resolved)` raises `ValueError` when `resolved` is *not* an ancestor of `home`, so the `try`/`except ValueError` pattern is the correct portable "is ancestor of" test across `PurePath`/`PureWindowsPath` without needing OS-specific well-known-path lists (`/home`, `/Users`, `C:\Users` all fall out of this generically, since they are literal ancestors of `Path.home()` on their respective platforms). This closes both the H-02 POSIX gap and the H-08 `C:\Users` gap with one change.

---

## L1 Detailed Findings — REFUTED (Positive Assurance)

> Per red-lead's L2 note, these are "exactly what the owner asked for by requesting a red-team pass" — proof that the preserved invariants actually hold post-widening, not assumption. Each was actively demonstrated against the real code, not inferred from reading.

**H-03 (symlink escape from allowed temp root):** A symlink planted inside a fully-isolated, monkeypatched allowed temp root, pointing at a synthetic file outside all roots, is rejected at the **primary** check — `Path(file_path).resolve()` follows the symlink before `is_relative_to()` ever runs, so the resolved target (outside all roots) fails containment directly; the secondary M-10 `os.path.realpath` check is a defense-in-depth backstop, not the only line of defense. A symlink to a file *inside* the same temp root is allowed, which is by design (it does not escape the widened region — this is the H-01 exposure, not a new symlink-specific one).

**H-04 (`--root` exclusivity + symlink):** `get_containment_roots(explicit_root=...)` returns exactly one entry (`[resolved_root]`), confirmed via `len(roots) == 1` and confirming the project root is never additively re-admitted, including when `--root` itself resolves through a symlinked directory. A project-root file is rejected when `--root` points elsewhere (exclusivity, not additive union). A symlink inside `X` pointing outside `X` is rejected by the same primary-check mechanism as H-03.

**H-05 (write-time TOCTOU):** Source inspection (not merely assumed — the exact recheck block, `mkstemp` call, and `os.replace` call were located and their invariants checked programmatically) confirms the write path re-verifies containment immediately before writing, using the identical `root` parameter passed to the read (no read/write disagreement possible within one invocation), then stages via `tempfile.mkstemp` (private, `O_EXCL`) and commits via `os.replace` (atomic rename that replaces the symlink itself rather than following it). The residual TOCTOU window between recheck and replace is the same low-exploitability class the M-21 mitigation already targets; the widening's only contribution is a larger world-writable staging *directory* when the matched root is `/tmp`/`gettempdir()` — which collapses to the H-01 finding, not a new TOCTOU escalation.

**H-06 (predictable temp staging):** `tempfile.mkstemp(dir=..., suffix=".tmp", prefix=".ast_modify_")` was executed exactly as `ast_modify` calls it; the resulting file's mode bits were directly inspected and confirmed `0o600`. No non-`mkstemp` write path exists in the module.

**H-07 (path traversal regression):** `"../../etc/passwd"`, `"/etc/passwd"`, `"/etc/shadow"`, and `"/root/.ssh/id_rsa"` (all synthetic/nonexistent stand-ins — no real system file was read or touched) are all rejected under the widened default containment set. The existing `tests/security/test_adversarial_parsers.py::TestA07PathTraversal` regression suite was re-run **unmodified** against the current code and passes (see [Methodology](#methodology-and-evidence-provenance)).

**H-09 (stream separation):** stderr/stdout separation was directly captured and verified: the temp-match note and the broad-root warning both appear exclusively on stderr; the temp-match note is correctly suppressed for a project-root match. `jerry ast ... | jq` JSON-consumer integrity is preserved.

**H-10 (relative/non-existent `--root`):** A relative `--root` value resolves against the current working directory exactly as `get_project_root()`'s documented no-validation contract implies. A non-existent `--root` path returns that literal (unresolved-to-anything-real) path as the sole allowed root; any real file check against it is correctly rejected — fail-closed, not fail-open.

---

## L1 Detailed Findings — Code-Reasoning Only

### H-08 — Windows path-semantics edge cases

Per the RoE ("no Windows host is in scope to run against"), this was executed as pure `PureWindowsPath` reasoning against the real `_is_broad_containment_root` function — no live Windows host, no emulation layer. Findings:

- **Drive root (`C:\\`) — SAFE.** `.parts == ('C:\\',)`, length 1, warns correctly.
- **UNC share root (`\\host\share`) — SAFE.** The UNC anchor is a single `parts` element, so this also warns.
- **UNC subpath (`\\host\share\sub`) — coverage gap, same class as H-02.** 2 `parts` elements → does not warn, despite the share itself still being a whole-network multi-user root once you're inside it.
- **`C:\Users` — coverage gap, same class as H-02.** Not flagged by the current exact-home-only check; would be closed by the H-02 remediation's ancestor-of-home logic (`.relative_to()` works identically across `PurePath` and `PureWindowsPath`).

This is folded into the H-02 remediation rather than tracked as a separate finding, per red-lead's framing that H-08 gaps are "the same class" — but the *portable* fix (ancestor-of-home via `.relative_to()`, not an OS-specific string list) closes both simultaneously, and a `PureWindowsPath`-based unit test is recommended given CI already runs `windows-latest`.

---

## L2 Strategic Implications

**Remediation priority for eng-backend, ranked:**

1. **H-01 ownership gate** (highest leverage, cheapest fix — red-lead's own L2 assessment agrees this is "the highest-leverage, lowest-cost change the assessment can recommend"). Scoped strictly to temp-default-root matches; does not touch the project-root path or the `--root` escape hatch, so it preserves the owner's scratchpad use case exactly while closing the cross-tenant exposure. Requires an `os.name` branch for the Windows caveat (no `os.geteuid()` there).
2. **H-02/H-08 combined remediation** (ancestor-of-home check in `_is_broad_containment_root`, via `PurePath.relative_to()` rather than an OS-specific string list) — single code change closes both the POSIX (`/home`, `/Users`) and Windows (`C:\Users`) coverage gaps, plus the UNC-subpath case, with one portable predicate.

**No NEEDS-FIX findings.** Every hypothesis that reached a verdict was either a clean CONFIRMED (real gap, no partial mitigation to salvage) or a clean REFUTED (invariant fully holds) — there were no partially-broken safeguards in this specific change.

**Test-suite gap closure (corroborating evidence, per red-lead's L2 coverage-gap note):** The existing test suite (`tests/unit/interface/cli/test_project_root.py`, `tests/unit/interface/cli/test_ast_commands.py`, `tests/security/test_adversarial_parsers.py::TestA07PathTraversal` — 136 tests, all passing, executed read-only as part of this assessment) does **not** contain any test asserting on `st_uid`/ownership (because no such check exists — confirmed via grep, zero matches) and does **not** contain any test asserting the warning fires (or fails to fire) for `/home`, `/Users`, or `Path.home().parent`. This absence corroborates H-01 and H-02 as genuine gaps rather than untested-but-present behavior. **Recommendation for eng-qa/eng-backend:** add regression tests for both remediations before merge — an ownership-mismatch test (requires either `monkeypatch`-ing `os.geteuid` or constructing a file the test process does not own, which is itself awkward in a single-user CI runner; a `monkeypatch.setattr("os.geteuid", lambda: <different-uid>)` pattern is the practical approach) and a `parametrize`-driven `_is_broad_containment_root` test across `/home`, `/Users`, `Path.home().parent`, and a `PureWindowsPath("C:\\Users")` case.

**Handoff:** This report is ready for red-reporter aggregation and for direct hand-off to eng-backend for the fix pass. No further red-team agents are required — red-exploit's code-review-mode validation of H-01/H-03/H-04/H-05 is effectively subsumed by the executed reproductions in this report (all four were run against the real functions, not merely modeled), but red-exploit may still be invoked per the original engagement authorization if the orchestrator wants a second independent pass before the fix ships.

---

## Methodology and Evidence Provenance

**Probe script (not committed to the repo; scratchpad-only, per assessment-only constraint):** `/private/tmp/claude-502/-Users-adam-nowak-workspace-GitHub-geekatron-jerry-wt-feat-proj-024-tactical-work-6/de0b3d7c-1390-42d5-a79d-8f234300b4ed/scratchpad/redvuln/probe_h01_h10.py`. Directly imports and calls `_is_broad_containment_root`, `get_containment_roots`, and `_check_path_containment` from the real, unmodified source modules. All sandbox directories were created via `tempfile.TemporaryDirectory()`/`tempfile.mkdtemp()` (assessor-owned, disposable, removed on exit) and all "victim"/"secret" file contents are synthetic placeholder strings — no real credential, key, or system file was read, written, or echoed at any point.

**Corrected negative control (transparency note, per P-022):** The first draft of the H-01 negative control was methodologically flawed — it used `tempfile.TemporaryDirectory()` for the "outside all roots" control file, but that helper creates directories *under* `gettempdir()`, which is itself an allowed root by design. That meant the control would have passed containment via the temp root regardless of whether the ownership-check gap existed, making it a worthless control. This was caught and corrected before finalizing the verdict: both temp-root seams (`_HARDCODED_TMP`, `tempfile.gettempdir`) were monkeypatched to a fully isolated, test-owned directory, and the negative-control file was placed in a **separate** directory that is neither the project root nor the (now-isolated) allowed temp root. The corrected control demonstrates genuine rejection, and the finding stands unchanged (H-01 remains CONFIRMED) — the correction affects evidence quality, not the verdict.

**Existing-test corroboration:** `env -u VIRTUAL_ENV uv run --project . pytest tests/unit/interface/cli/test_project_root.py tests/unit/interface/cli/test_ast_commands.py tests/security/test_adversarial_parsers.py::TestA07PathTraversal -q` → **136 passed**, executed read-only as evidence of existing coverage (T-6 in red-lead's scope), not attacked or modified.

**Honesty disclosure on reproducibility (P-022):** The H-01 multi-user cross-tenant scenario was **modeled**, not executed against a real second OS user or a real shared host — the RoE explicitly prohibits touching any file the assessor does not own, and this environment has only one available UID. The reproduction executed and shown above demonstrates the **necessary precondition** (temp-root match is allowed with no ownership check) with full certainty; the cross-tenant consequence on a genuinely shared host is a direct, low-uncertainty logical extension of that precondition (the same code path, the same absent check, a different UID on the other side), not a separate untested claim. This is stated explicitly per the assignment's instruction to "state reproducibility honestly."

---

## Constitutional Compliance

- **P-001 (evidence-based):** Every verdict cites the exact reproduction executed against the real code, with file/line references to the source under test and the probe script location.
- **P-002 (persisted):** This report is persisted at the engagement path specified by the task; the probe script (throwaway, not production code or tests) is persisted to the session scratchpad per the task's instruction, not to the repository.
- **P-003 (no recursive subagents):** red-vuln executed all hypotheses directly; no subagent was spawned.
- **P-020 (user authority):** No production source or test file was modified. The owner's accepted risk (default temp widening, `--root` at user discretion) is respected as policy; remediations are recommendations for eng-backend, not unilateral changes.
- **P-022 (no deception):** The flawed initial negative control was disclosed and corrected in the open, not silently fixed. Deployment-model dependence for H-01's severity is stated explicitly rather than picked silently. The H-01 cross-tenant scenario is labeled as modeled/logically-extended, not falsely claimed as directly executed against a second real user.

---

*red-vuln assessment v1.0 — RED-BUG010. All 10 hypotheses executed against real code in a disposable sandbox; no exploit against any live or real-user target; no production source or test file modified. Downstream: red-reporter (aggregate + report), eng-backend (fix pass on H-01 + H-02/H-08 remediations).*
