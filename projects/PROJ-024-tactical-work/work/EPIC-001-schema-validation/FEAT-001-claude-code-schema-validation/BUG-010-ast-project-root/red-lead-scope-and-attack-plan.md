# red-lead Scope Statement and Attack Plan — BUG-010 Containment Widening

> **Engagement:** RED-BUG010 — white-box source-code security assessment of the `jerry ast` path-containment widening (PR #341 owner-review follow-up).
> **Agent:** red-lead (Engagement Lead and Scope Authority) — Step 1 of `/red-team`. MANDATORY FIRST agent; all downstream assessment agents validate against this scope.
> **Deliverable type:** Scope + Rules of Engagement + threat model + ranked attack plan. **METHODOLOGY AND PLAN ONLY** — no exploit execution, no code modification.
> **Methodology:** PTES Pre-Engagement Interactions + OSSTMM Section III (Regulatory Framework) + NIST SP 800-115 Chapter 3 (Planning), applied to a defensive white-box review of our own code.
> **Authorization:** Repo owner (geekatron) on-record request in PR #341 review — "leverage the /eng-team, /red-team and /adversary C4 to close this out." Engagement type: white-box source-code review of the changed files only. No live targets, no network, no external hosts.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Scope, RoE, top risks, most-likely findings in plain language |
| [L1 Scope Statement](#l1-scope-statement) | In-scope / out-of-scope, targets, authorization |
| [L1 Rules of Engagement](#l1-rules-of-engagement) | White-box code-only RoE, emergency stop, deconfliction |
| [L1 Threat Model of the Widened Surface](#l1-threat-model-of-the-widened-surface) | Attack surface delta, trust boundaries, CWE/ATT&CK framing |
| [L1 Ranked Attack Hypotheses](#l1-ranked-attack-hypotheses) | H-01..H-10 highest-risk first, each with test method + expected safe behavior |
| [L1 Severity Rubric](#l1-severity-rubric) | Scoring model the assessment agents apply |
| [L2 Strategic Implications](#l2-strategic-implications) | Systemic recommendations, methodology gaps, most-likely-finding call |
| [Agent Authorizations](#agent-authorizations) | Which /red-team agents may act and their technique allowlist |
| [Constitutional Compliance](#constitutional-compliance) | P-001/P-002/P-020/P-022 attestation |

---

## L0 Executive Summary

**What is being assessed.** A single, self-contained code change in the Jerry CLI that *widens* the `jerry ast` path-containment boundary. Before this change, the only directory a `jerry ast` command would operate inside was the user's project root (`CLAUDE_PROJECT_DIR`, else cwd). After the change, the default allowed set is `{project root, tempfile.gettempdir(), /tmp}` (deduplicated, `/tmp` gated on existence), **plus** a new `--root <path>` flag that makes the allowed set *exactly* `{that path}` (exclusive override). Two advisory stderr behaviors shipped: a broad-root warning when `--root` resolves to a filesystem/drive root or `$HOME`, and a temp-match transparency note when a file is allowed only via a temp default root.

**Scope in one line.** In scope: the six changed source files and their security-relevant call paths (containment resolution, symlink handling, size cap, write-time recheck, CLI plumbing). Out of scope: any live system, any network target, any host filesystem outside a throwaway test sandbox, and the pre-existing M-05 size-cap logic (unchanged by this widening).

**The core security trade-off.** The owner explicitly accepted a broadened default surface ("allow the temp directories... it's at the user's discretion... reasonable best effort") to fix a real usability bug (Claude Code scratchpads live outside the project tree). Our job is *not* to overturn that accepted risk — it is to verify that (a) the widening does exactly what was intended and nothing more, (b) the containment invariants that were *supposed* to survive (symlink escape rejection, write-time recheck, exclusive `--root`) actually do, and (c) the "best-effort protection" the owner promised is not silently full of holes.

**Top-line risk picture (before assessment executes — these are hypotheses, not confirmed findings):**

1. **Multi-user temp exposure (highest-value hypothesis).** The default set now includes `/tmp` and `gettempdir()` with **no file-ownership check**. On a shared multi-user host, `jerry ast parse /tmp/<other-user>/secret.md` would now pass containment where it was previously rejected. This is the hypothesis most likely to be judged a legitimate finding — its severity hinges on Jerry's real deployment model (single-user dev laptop vs. shared host).
2. **Broad-root warning coverage gap.** `_is_broad_containment_root` only catches the *exact* filesystem/drive root and the *exact* `$HOME`. It does **not** catch `--root /home`, `--root /Users`, or `$HOME`'s parent — each of which effectively disables containment across all users but emits no warning. A concrete, demonstrable gap in the promised "best effort."
3. Symlink-escape rejection, `--root` exclusivity, and the write-time TOCTOU recheck each *appear* correct in the code but must be positively verified, not assumed — several of them are only correct because `Path.resolve()` follows symlinks *before* the containment comparison.

**Most likely to yield a real finding in this specific code:** Hypothesis **H-01 (multi-user temp read/write, missing ownership check)** and Hypothesis **H-02 (broad-root warning gap)**. Everything else is expected to come back SAFE-if-tested; those two have concrete, code-grounded gaps.

---

## L1 Scope Statement

### Engagement metadata

| Field | Value |
|-------|-------|
| `engagement_id` | RED-BUG010 |
| `version` | 1.0 |
| Engagement type | White-box (source-available) static security assessment |
| Assessment class | Code review of a diff + targeted dynamic testing against the *real code in a throwaway sandbox* |
| Methodology | PTES Pre-Engagement + NIST SP 800-115 §3 (Planning) + OSSTMM §III |
| Authorization basis | On-record owner request, PR #341 review comment (defensive review of own code) |
| Time window | Single engagement session; no persistence across sessions |

### Authorized targets (allowlist — everything else is OUT OF SCOPE)

| # | Target | Type |
|---|--------|------|
| T-1 | `src/interface/cli/project_root.py` | Changed source (containment-root resolution) |
| T-2 | `src/interface/cli/ast_commands.py` | Changed source (containment check, read, write-time recheck) |
| T-3 | `src/interface/cli/parser.py` | Changed source (`--root` argument plumbing) |
| T-4 | `src/interface/cli/main.py` | Changed source (`--root` pass-through dispatch) |
| T-5 | The security-relevant call paths reachable from the above (symlink resolution, `is_relative_to` containment, `os.path.realpath` M-10 check, `tempfile.mkstemp`/`os.replace` atomic write) | Call-path analysis |
| T-6 | The associated tests (`tests/unit/interface/cli/test_project_root.py`, `tests/unit/interface/cli/test_ast_commands.py`, `tests/security/test_adversarial_parsers.py::TestA07PathTraversal`) as *evidence of coverage*, not as targets to attack | Test-adequacy review |

### In scope

- The **delta** introduced by this change: the multi-root default set, the `--root` exclusive override, the broad-root warning (`_is_broad_containment_root`), and the temp-match transparency note (`_warn_if_temp_root_match`).
- The containment invariants the change *claims* to preserve: CWE-22 traversal rejection, CWE-59 symlink-escape rejection (M-10), CWE-367 write-time TOCTOU recheck (M-21).
- Cross-platform correctness of breadth detection and containment on Windows path semantics (as a code-reasoning exercise; no Windows host is in scope to run against).

### Out of scope

- Any live host, service, network, or external system. **No exploit is run against any real filesystem outside a self-created disposable sandbox directory** (e.g., a fresh `mktemp -d` the assessor owns).
- The M-05 1 MB size cap logic itself (unchanged; only inherited by the new roots).
- The broader `jerry` CLI, other namespaces, the domain/markdown-AST parsers (except where a containment path reaches them).
- The `JERRY_DISABLE_PATH_CONTAINMENT=1` escape hatch as a *vulnerability* (it is an intentional, documented test-only bypass; note its existence but do not treat "containment can be disabled by an env var the user sets themselves" as a finding — it is user-discretion by design, consistent with `--root`).
- Social engineering, phishing, persistence, exfiltration, C2 — **none authorized** (see [Agent Authorizations](#agent-authorizations)); this is a code review.

---

## L1 Rules of Engagement

| RoE Field | Value |
|-----------|-------|
| Engagement style | White-box, source-available, read-only against source. Dynamic tests permitted ONLY against the real functions invoked in-process (pytest-style) or via `jerry ast` against files the assessor creates in a disposable sandbox. |
| Target boundary | The four changed files + their call paths. No probing of any path the assessor does not own. |
| Live-target prohibition | No network. No writes outside a disposable, assessor-owned sandbox dir. NEVER point a write-capable test (`ast_modify`) at any real user/system file. Never read a real file outside the sandbox to "prove" disclosure — construct a fixture that stands in for the victim file. |
| Destructive-op prohibition | No modification of production source, tests, or the worktracker by the assessment agents. Findings are reported, not patched, in this engagement. (P-020) |
| Credential / secrets rule | If any test constructs a stand-in "secret" file (e.g., a fake `passwd` or fake `id_rsa`), it MUST contain synthetic data only. NEVER read or echo a real credential, key, or any part of one (per standing operator directive). |
| Emergency stop | If any test would touch a path outside the disposable sandbox, or would write to `/tmp`/`gettempdir()` in a way that could collide with another process, HALT and report the design rather than execute. |
| Evidence handling | Findings + repro steps persisted to the BUG-010 engagement directory only. No evidence leaves the repo. Disposable sandbox dirs removed in a `finally`. |
| Deconfliction | This assessment runs in parallel with `/eng-team` and `/adversary` C4 on the same change. red-lead is the circuit-breaker authority: if an assessment agent flags `SCOPE_REVIEW_REQUIRED` (e.g., wants to test on a real multi-user host), route back here — the answer is "model it, do not execute it." |
| Reporting standard | Every hypothesis result must state: SAFE / FINDING / INCONCLUSIVE, with the exact code line(s) as evidence (P-001) and a severity per the [rubric](#l1-severity-rubric). |

---

## L1 Threat Model of the Widened Surface

### Trust boundaries (before vs. after)

```
BEFORE (single root):
  attacker-controlled input: file_path (CLI arg)
  trust boundary: is_relative_to(project_root)  ── one wall
  allowed region:  [ project_root ]

AFTER (widened):
  attacker-controlled input: file_path (CLI arg) + --root (CLI arg)
  trust boundary: any(is_relative_to(r) for r in allowed_roots)  ── three walls OR one user-chosen wall
  allowed region (default):  [ project_root ] ∪ [ gettempdir() ] ∪ [ /tmp ]
  allowed region (--root X):  [ X ]   (exclusive; project_root & tempdir NO LONGER allowed)
```

**The key structural observation** that shapes every hypothesis: containment is evaluated on `Path(file_path).resolve()` — i.e., the path is **fully symlink-resolved before** the `is_relative_to` comparison. This is what makes the symlink-escape defense mostly sound (a symlink to `/etc/passwd` resolves to `/etc/passwd`, which is under no allowed root, so it is rejected at the *primary* check, not merely the secondary M-10 check). It also means the widening's real risk is **not** symlink escape *out* of the allowed roots — it is that the allowed roots now legitimately include **world-writable, multi-tenant directories** (`/tmp`, `gettempdir()`) with **no per-file ownership gate**.

### Attack surface delta and ATT&CK/CWE framing

| Surface delta | Primary CWE | ATT&CK technique (framing) | Assessment concern |
|---------------|-------------|----------------------------|--------------------|
| `/tmp` + `gettempdir()` added to default allowed set | CWE-552 (Files Accessible to External Parties), CWE-668 (Exposure to Wrong Sphere) | T1005 Data from Local System / T1552.001 Credentials in Files (framing only) | Reads/writes of other users' temp files on a shared host now pass containment |
| No `st_uid`/ownership check on temp matches | CWE-281 (Improper Preservation of Permissions) | — | Widening trusts *location* but not *ownership* |
| `--root <path>` exclusive override | CWE-22 (Path Traversal), CWE-73 (External Control of File Name/Path) | T1083 File and Directory Discovery (framing) | User-directed; must verify it is exclusive (not additive) and that broad values warn |
| Broad-root warning `_is_broad_containment_root` | CWE-1284 (Improper Validation of Specified Quantity) / incomplete allowlist | — | Advisory control with coverage gaps (`/home`, `/Users`, home parent) |
| Symlink handling across N roots (M-10) | CWE-59 (Improper Link Resolution) | — | Must hold for ALL roots, not just project root |
| Write-time recheck in `ast_modify` | CWE-367 (TOCTOU) | — | Race between recheck and `os.replace`; wider world-writable staging area |
| Predictable temp staging (`mkstemp` in `target_path.parent`) | CWE-377 (Insecure Temporary File) | — | `mkstemp` is O_EXCL/0600 (secure) — verify no fallback to non-atomic write |
| Windows drive-relative `/tmp`, 8.3, ADS, UNC | CWE-22 / CWE-59 | — | Breadth detection via `PurePath.parts` untested on Windows flavor |

---

## L1 Ranked Attack Hypotheses

> Ordered highest-risk first. Each hypothesis states the concrete code under test, how the assessment agent should test it against the **real code** (in-process or sandbox), and the expected SAFE behavior. Assessment agents (red-vuln, red-exploit — code-review mode) execute these; red-lead does not.

### H-01 — Multi-user temp read/write with no ownership check (CWE-552 / CWE-668 / CWE-281) — HIGHEST RISK

**Claim to disprove:** "Widening the default set to `/tmp` and `gettempdir()` only exposes the current user's own scratchpads."

**Code under test:** `project_root.get_containment_roots()` lines ~147-153 (adds `gettempdir()` and `/tmp` unconditionally, existence-gated) and `ast_commands._check_path_containment` lines ~248-252 (`matched_root = next((r for r in allowed_roots if resolved.is_relative_to(r)), None)`). **There is no `resolved.stat().st_uid == os.geteuid()` check anywhere.**

**How to test (sandbox, single-user — model the multi-user case):**
1. In-process: `monkeypatch.setenv("CLAUDE_PROJECT_DIR", <projectA>)`. Create a stand-in "victim" file at `Path(tempfile.gettempdir()) / "victim-secret.md"` containing synthetic data (NOT a real secret). Call `_check_path_containment(str(victim_file))` with no `--root`.
2. Assert current behavior: it returns `(resolved, None)` — i.e., **ALLOWED**, and `_warn_if_temp_root_match` fires the stderr note. This demonstrates the tool will read a temp file that is *not* under the user's project.
3. Escalate the model: document that on a real shared host `gettempdir()`/`/tmp` contain *other users'* world-readable files, and that `ast_modify` (write path) would likewise pass the write-time recheck for a target under `/tmp` (subject to OS sticky-bit, which blocks rename-over-others'-files but not creation of new files or reads).
4. Confirm the negative control: the same file under a *sibling* non-temp directory outside the project is still rejected.

**Expected safe behavior (target state, NOT current):** A temp-root match should additionally require the resolved file to be owned by the current effective UID (`os.geteuid()`), OR the temp inclusion should be scoped to a per-user subtree (e.g., only `gettempdir()` which on macOS is already per-user `/var/folders/...`, and for `/tmp` restrict to `/tmp/claude-*` owned by the caller). **Current code does neither — this is the recommended finding.**

**Verdict framing:** If the assessor confirms allow-without-ownership-check, this is a **FINDING**. Severity: MEDIUM on a single-user dev laptop (the dominant deployment), HIGH on any shared/CI multi-tenant host. Recommend the ownership gate as remediation regardless, because it is cheap and preserves the owner's scratchpad use case.

### H-02 — Broad-root warning coverage gap (`_is_broad_containment_root`) (incomplete allowlist / CWE-1284-adjacent) — HIGH

**Claim to disprove:** "`--root` to an over-broad directory always warns the user (best-effort protection holds)."

**Code under test:** `project_root._is_broad_containment_root` lines ~63-93. Logic: returns True only when `len(resolved.parts) <= 1` (exact filesystem/drive root) OR `resolved == Path.home().resolve()` (exact home).

**How to test (in-process, pure — no filesystem needed):**
1. `get_containment_roots("/")` → assert warning fires (parts == `('/',)`, len 1). SAFE.
2. `get_containment_roots(str(Path.home()))` → assert warning fires. SAFE.
3. **`get_containment_roots("/home")` (Linux) or `get_containment_roots("/Users")` (macOS)** → parts len 2, not equal to home → **assert whether the warning fires. It does NOT.** This root contains *every* user's home directory yet emits no warning. → **FINDING (gap).**
4. `get_containment_roots(str(Path.home().parent))` → same class of gap (parent of home).
5. Capture stderr via `capsys` and assert on presence/absence of the `Warning: --root` line for each case.

**Expected safe behavior:** Breadth detection should also flag well-known multi-user parents (`/home`, `/Users`, `C:\Users`, home's parent) — or, more robustly, warn whenever the resolved root is an *ancestor of* `Path.home()` or has depth below a threshold. **Current code misses these — recommended finding, LOW-to-MEDIUM severity** (the warning is advisory/non-fatal, so the gap weakens transparency rather than enabling escape; the owner explicitly allows broad roots at user discretion).

### H-03 — Symlink escape from inside an allowed temp root (CWE-59 / M-10) — MEDIUM (expected SAFE, must verify)

**Claim to disprove:** "A symlink planted inside a now-allowed temp root, pointing outside all roots, is still rejected."

**Code under test:** `_check_path_containment` lines ~243-262. Primary check on `resolved = Path(file_path).resolve()` (symlink-followed) + secondary M-10 check `any(realpath.is_relative_to(r) for r in allowed_roots)` on `os.path.realpath`.

**How to test (sandbox):**
1. Create a disposable temp root you control; monkeypatch `_HARDCODED_TMP` and `tempfile.gettempdir` to that dir so the allowed temp set is fully controlled.
2. Inside it, create `link.md -> /etc/passwd` (or a synthetic file outside all roots).
3. `_check_path_containment(str(link))` → assert **rejected** with "escapes allowed containment roots" (because `.resolve()` yields `/etc/passwd`, under no root — caught at the *primary* check).
4. Variant: symlink inside temp root pointing to *another file inside the same temp root* → assert ALLOWED (in-root, by design; note this in the H-01 multi-user context — a symlink cannot be used to *escape*, but it can chain within the widened region).

**Expected safe behavior:** Escape rejected for all roots. Code path suggests SAFE because `.resolve()` normalizes before comparison and the secondary check iterates all roots. **Verify, do not assume** — this is the invariant the owner most needs preserved.

### H-04 — `--root` exclusivity + symlink combination (CWE-22 / CWE-59) — MEDIUM (expected SAFE, must verify)

**Claim to disprove:** "`--root X` is a true exclusive override and cannot be escaped via a symlink inside X."

**Code under test:** `get_containment_roots` lines ~135-145 (`if explicit_root is not None: return [resolved_root]`) + the containment check.

**How to test (sandbox):**
1. `_check_path_containment(str(file_in_project), explicit_root=str(unrelated_dir))` → assert **rejected** (proves exclusivity: a project-root file is rejected when `--root` points elsewhere).
2. `_check_path_containment(str(file_in_X), explicit_root=str(X))` → ALLOWED.
3. Inside `X`, create `link -> /etc/passwd`; `_check_path_containment(str(link), explicit_root=str(X))` → **rejected** (resolve escapes X).
4. `--root` pointing at a symlink *directory*: `X_link -> /etc`; `get_containment_roots(str(X_link))` resolves the root itself to `/etc`, then a file under it is checked against `/etc`. Document that resolving the root through a symlink is expected (root is user-chosen) but confirm it does not *additively* re-admit the project root.

**Expected safe behavior:** Exclusive and non-escapable. Expected SAFE from code reading.

### H-05 — Write-time TOCTOU race in `ast_modify` (CWE-367 / M-21) — MEDIUM (expected LOW-exploitability, verify mitigation intact)

**Claim to disprove:** "A symlink swap between the write-time recheck and `os.replace` lets a write land outside the allowed roots."

**Code under test:** `ast_modify` lines ~591-616: `target_path = Path(file_path).resolve()` → recheck `any(target_path.is_relative_to(r) ...)` → `tempfile.mkstemp(dir=target_path.parent)` → `os.replace(temp, str(target_path))`.

**How to test (code reasoning + sandbox):**
1. Confirm the recheck re-resolves at write time and reuses the same `root` value passed to the read (lines 596 vs. the read call) — so read and write cannot disagree on the allowed set within one invocation.
2. Confirm the write targets `target_path` (an already-resolved concrete path), and `os.replace` does **not** follow a final-component symlink (rename semantics replace the symlink itself). Model: even if an attacker swaps `target_path` to a symlink after line 599, `os.replace` overwrites the symlink, not its target → no write-through escape.
3. Confirm `mkstemp` (O_EXCL, 0600) is the *only* write mechanism (no fallback `open(path,'w')`). It is.
4. Residual window to document: `target_path.parent` on `/tmp` is world-writable; a stand-in test should confirm `mkstemp` still creates a private file there and that a hostile `.ast_modify_*.tmp` pre-creation cannot hijack the write (O_EXCL defeats predictable-name pre-creation → ties into H-06).

**Expected safe behavior:** Recheck + non-following `os.replace` + `mkstemp` = residual TOCTOU is low-exploitability. Expected SAFE-with-caveat; the widening's only contribution is a larger world-writable staging area, already covered by OS sticky-bit and O_EXCL.

### H-06 — Predictable/insecure temp staging on write (CWE-377) — LOW-MEDIUM (expected SAFE, verify)

**Claim to disprove:** "The `.ast_modify_*.tmp` staging file can be predicted/pre-created to hijack or corrupt the atomic write in a world-writable root."

**Code under test:** `tempfile.mkstemp(dir=..., suffix=".tmp", prefix=".ast_modify_")` line ~605.

**How to test:** Confirm `mkstemp` yields an unpredictable suffix and opens with `O_CREAT|O_EXCL|O_RDWR` at mode 0600 (stdlib guarantee). Assert a pre-existing file at a guessed name does not cause `mkstemp` to reuse it (O_EXCL). **Expected SAFE** — `mkstemp` is the correct primitive; flag only if any non-`mkstemp` temp path exists (none observed).

### H-07 — Path traversal against the widened default set (CWE-22) — MEDIUM (regression guard, expected SAFE)

**Claim to disprove:** "`../../etc/passwd` or an absolute `/etc/passwd` now passes because more roots exist."

**Code under test:** `_check_path_containment` primary check; regression anchor is `tests/security/test_adversarial_parsers.py::TestA07PathTraversal::test_path_traversal_blocked` (`_read_file("../../etc/passwd")`).

**How to test:**
1. Run the A-07 adversarial test **unmodified** and confirm it still asserts `exit_code != 0` under the widened defaults (the plan flags this as verify-not-assume; the resolved `../../etc/passwd` from repo-root cwd is outside project root, `gettempdir()`, and `/tmp`).
2. Add absolute-path variants: `_check_path_containment("/etc/passwd")`, `/etc/shadow`, `/root/.ssh/id_rsa` (synthetic stand-ins in sandbox) → all rejected.
3. Edge: a `../` chain that lands *inside* `/tmp` (e.g., from a cwd under `/tmp`, `../sibling`) → now ALLOWED by design; document as an intended consequence of the widening, cross-referenced to H-01.

**Expected safe behavior:** Absolute and relative traversal to non-allowed regions rejected; traversal that resolves *into* an allowed temp root is allowed by design (feeds H-01).

### H-08 — Windows path-semantics edge cases (CWE-22 / CWE-59) — LOW-MEDIUM (code-reasoning only; no Windows host in scope)

**Claim to disprove:** "Breadth detection and containment behave correctly under Windows path flavor."

**Code under test:** `_HARDCODED_TMP = Path("/tmp")` (drive-relative on Windows → `<cwd-drive>:\tmp`, existence-gated); `_is_broad_containment_root` via `PurePath.parts`; `is_relative_to`.

**How to reason/test (pure `PureWindowsPath`, no host):**
1. Drive-root breadth: `PureWindowsPath("C:\\").parts == ('C:\\',)` → len 1 → warning fires. SAFE.
2. UNC: `PureWindowsPath("\\\\host\\share").parts` → anchor is one element → len 1 → warns; `\\host\share\sub` → len 2 → no warn (document as gap, same class as H-02).
3. `/tmp` on Windows: `Path("/tmp")` → `WindowsPath('/tmp')` → resolves under current drive; `.exists()` gate means it is only added if `<drive>:\tmp` genuinely exists (rare). Document R-5 as accepted.
4. 8.3 short names (`PROGRA~1`) and ADS (`file.md::$DATA`): reason about whether `Path.resolve()` normalizes short→long consistently and whether `::$DATA` on a file *inside* an allowed root stays inside (it does — the stream is on an in-root file; not an escape, but note the size check reads the default stream while a stream read could differ). Flag any inconsistency between the form used for the root and the form used for the file as a *potential* mismatch to unit-test with `PureWindowsPath`.

**Expected safe behavior:** No escape; breadth-warning gaps mirror H-02. Since CI runs `windows-latest`, recommend a `PureWindowsPath`-based unit test for breadth detection even though live Windows exploitation is out of scope.

### H-09 — `_warn_if_temp_root_match` correctness / stdout-JSON integrity (robustness, not escape) — LOW

**Claim to disprove:** "The transparency note or broad-root warning can leak into stdout and corrupt JSON consumers, or can be suppressed to hide a temp match."

**Code under test:** `_warn_if_temp_root_match` (prints to `sys.stderr`) and the broad-root warning (also `sys.stderr`); JSON payloads print to stdout.

**How to test:** With `capsys`, assert the note/warning appear on **stderr only**, never stdout, so `jerry ast parse ... | jq` stays valid. Confirm the note fires for a temp-root match and is correctly suppressed for a project-root match and for explicit `--root`. **Expected SAFE** — stream separation is correct in the code.

### H-10 — `--root` relative-path and non-existent-path handling (CWE-73) — LOW

**Claim to disprove:** "A relative or non-existent `--root` produces surprising/unsafe containment."

**Code under test:** `Path(explicit_root).resolve()` (no existence validation, resolves relative to cwd).

**How to test:** `get_containment_roots("relative/dir")` under a known cwd → resolves against cwd (document as consistent with `get_project_root()`'s no-validation contract). `--root /does/not/exist` → returns `[/does/not/exist]`; any real file check fails `is_relative_to` → effectively rejects everything (fail-closed). **Expected SAFE / fail-closed.**

---

## L1 Severity Rubric

Assessment agents rate each confirmed finding on this model (CVSS-inspired, tuned for a local-CLI, defensive-tool threat model):

| Severity | Definition (for this engagement) | Example trigger |
|----------|----------------------------------|-----------------|
| **CRITICAL** | Containment fully defeated with attacker-controlled input under the *default* configuration (no `--root`, no env bypass), enabling read/write of arbitrary system files on a single-user host. | An unauthenticated `../` or symlink escapes all roots on default settings. (None hypothesized — expected none.) |
| **HIGH** | Containment escape or unauthorized cross-tenant access reachable under default config on a **shared/multi-user or CI host**, OR any write outside intended roots. | H-01 on a shared host (read/write other users' `/tmp` files). |
| **MEDIUM** | Access broadening that requires a specific-but-realistic environment (multi-user), OR a preserved-invariant that is only *narrowly* safe, OR a `--root`-gated escape (user-directed but exceeding stated intent). | H-01 on a single-user laptop; a symlink/`--root` combo that partially escapes. |
| **LOW** | Weakness in an *advisory* control (warning/transparency), robustness/coverage gap, or theoretical race with strong OS-level compensating controls. | H-02 (`/home` warning gap), H-05 residual TOCTOU, H-08/H-09/H-10. |
| **INFO / ACCEPTED** | Behaves as the owner explicitly accepted; documented risk, no action beyond noting. | Default temp inclusion *as a policy*; `JERRY_DISABLE_PATH_CONTAINMENT`; `--root` broad-root allowed-with-warning. |

**Severity modifiers:**
- **+1 level** if reachable via `ast_modify` (write) rather than read-only commands.
- **+1 level** if reachable with *no* `--root` and *no* env var (pure default config).
- **-1 level** if a standard OS control (sticky bit, `mkstemp` O_EXCL, per-user `$TMPDIR`) independently blocks exploitation.
- **Deployment context is decisive for H-01:** the assessor MUST state the assumed deployment model (single-user dev laptop = MEDIUM; shared host / shared CI runner = HIGH) rather than picking one silently.

---

## L2 Strategic Implications

**Methodology-selection rationale.** White-box source review (NIST SP 800-115 §3 planning + targeted §4 techniques) is the correct methodology here because the change is small, source is fully available, and the risk is *logic* (allowlist breadth, symlink resolution order, TOCTOU) rather than *reachability*. A black-box pentest would be wasteful; a full C4 tournament-grade code review of the containment invariants is proportionate to the change's security sensitivity (it is the tool's only filesystem sandbox).

**The one systemic recommendation.** The widening trusts *location* but not *ownership*. Every hypothesis that could become a real finding (H-01, and the multi-user framing of H-03/H-05) collapses to a single cheap mitigation: **for temp-root matches, additionally require `resolved.stat().st_uid == os.geteuid()`** (and reject world-writable-dir matches whose file the caller does not own). This preserves the owner's scratchpad use case exactly (Claude's own scratchpads are owned by the running user) while closing the cross-tenant exposure. It is the highest-leverage, lowest-cost change the assessment can recommend and should be the headline of the eventual red-reporter output.

**Second recommendation.** Harden `_is_broad_containment_root` to flag ancestors of `Path.home()` (catches `/home`, `/Users`, `C:\Users`, home's parent), so the "best-effort protection" the owner promised actually covers the obvious over-broad roots, not only the two exact edges.

**Coverage-gap note for downstream agents.** The change's own test suite is strong on the *intended* behaviors (T-1..T-8 in the eng-lead plan cover exclusivity, temp-match, symlink-from-temp rejection, and the A-07 regression). It does **not** test: (a) file-ownership on temp matches (because no such check exists — this is the finding), (b) the `_is_broad_containment_root` `/home`/`/Users` gap, (c) Windows breadth detection via `PureWindowsPath`. The assessment should treat the *absence* of these tests as corroborating evidence for H-01/H-02/H-08, not as a separate finding.

**Most-likely-finding call (explicit, as requested).** Of the ten hypotheses, exactly two have concrete, code-grounded gaps rather than "verify the invariant holds":
- **H-01 (multi-user temp, missing ownership check)** — the code demonstrably adds world-writable multi-tenant roots with no owner gate. This *will* reproduce; the only open question is severity (deployment-model dependent). **Most likely to be the engagement's headline finding.**
- **H-02 (broad-root warning gap for `/home`, `/Users`, home-parent)** — trivially reproducible in-process, purely deterministic, no environment needed. **Most likely to be the engagement's second finding.**

Everything else (H-03, H-04, H-05, H-06, H-07, H-08, H-09, H-10) is expected to return **SAFE** or **SAFE-with-documented-caveat** on inspection — the containment order (`resolve()` before compare), the exclusive `--root` return, the write-time recheck, and `mkstemp`/`os.replace` are all implemented correctly. Their value is *positive assurance* (proving the preserved invariants actually hold post-widening), which is exactly what the owner asked for by requesting a red-team pass.

---

## Agent Authorizations

| Agent | Authorized? | Technique allowlist (framing only — code review, not live attack) | Rationale |
|-------|-------------|-------------------------------------------------------------------|-----------|
| red-lead | Active (this doc) | Scope + RoE authoring | Mandatory first agent |
| red-vuln | **Authorized** | CWE-22, CWE-59, CWE-367, CWE-377, CWE-552, CWE-668 static analysis against T-1..T-5; execute H-01..H-10 as in-process/sandbox tests | Primary assessor for containment logic |
| red-exploit | **Authorized (code-review mode only)** | Construct proof-of-concept *test cases* against the real functions in a disposable sandbox; NO live-target exploitation, NO writes outside sandbox | Validate H-01/H-03/H-04/H-05 repros |
| red-reporter | **Authorized** | Aggregate findings, apply severity rubric, produce the engagement report | Terminal reporting |
| red-recon | Not required | — | White-box; source is already known |
| red-privesc, red-lateral, red-persist, red-exfil, red-social, red-infra | **NOT authorized** | — | Out of engagement type (no live systems, no network, no persistence/exfil/SE) |

**RoE-sensitive flags:** `social_engineering_authorized: false`, `persistence_authorized: false`, `exfiltration_authorized: false`. All gated OFF.

---

## Constitutional Compliance

- **P-001 (evidence-based):** Every hypothesis cites the exact function and line range in the actual changed code (read directly from `project_root.py` and the `git diff`), not the plan.
- **P-002 (persisted):** This scope + attack plan is persisted here; it is the load-bearing engagement artifact all downstream `/red-team` agents validate against.
- **P-003 (no recursive subagents):** red-lead authored this directly; it delegates *nothing* recursively.
- **P-020 (user authority):** The owner's accepted risk (default temp widening, `--root` at user discretion) is respected as policy, not overturned. The assessment recommends hardening; it does not mandate reversing the owner's decision.
- **P-022 (no deception):** Hypotheses are labeled as hypotheses, not confirmed findings; expected-SAFE items are called SAFE; the two likely findings are stated plainly with their severity uncertainty (deployment-model dependence) disclosed.

---

*red-lead engagement scope v1.0 — RED-BUG010. Methodology and plan only; no exploit executed, no code modified. Downstream: hand off to red-vuln (execute H-01..H-10), then red-reporter (severity + report).*
